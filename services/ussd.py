# services/ussd.py

from utils.constants import PREFIXES, CITIES, MESSAGES
from utils.user_session import (
    get_ussd_session,
    update_ussd_session,
    reset_ussd_session,
    log_emergency_alert,
)
from services.weather import get_flood_risk
from services.sms import send_sms_alert


async def ussd_handler(payload: dict) -> dict:
    session_id = payload.get("sessionId")
    phone = payload.get("phoneNumber", "").lstrip("+")
    text = payload.get("text", "").strip()

    # Basic validation
    if not session_id or not phone:
        return {"response": "END Service error. Please try again later."}

    # Detect country from phone prefix
    country_code = phone[:3]
    country = PREFIXES.get(country_code, "nigeria")

    # Reset session on first interaction or when user enters 99
    if text == "" or text == "99":
        reset_ussd_session(session_id, phone, country)

    # Retrieve or create persistent session
    ussd_session = get_ussd_session(session_id, phone, country)

    # Determine language
    if country == "nigeria":
        lang = "pidgin"
    elif country == "ghana":
        lang = "english"
    else:  # Cameroon
        lang = ussd_session.lang or "french"  # default to French

    response = ""

    # =============== USSD FLOW ===============

    if ussd_session.step == "start":
        welcome_key = "pidgin" if lang == "pidgin" else lang
        response = "CON " + MESSAGES["welcome"][welcome_key]
        ussd_session.step = "choose_lang" if country == "cameroon" else "choose_city"
        update_ussd_session(ussd_session)

    elif ussd_session.step == "choose_lang":
        response = "CON " + MESSAGES["choose_lang"]["french"]

        if text == "1":
            ussd_session.lang = "french"
            ussd_session.step = "choose_city"
            update_ussd_session(ussd_session)
        elif text == "2":
            ussd_session.lang = "english"
            ussd_session.step = "choose_city"
            update_ussd_session(ussd_session)

    elif ussd_session.step == "choose_city":
        # Display appropriate city menu
        if country == "nigeria":
            city_menu = MESSAGES["choose_city"]["pidgin"]
        elif country == "ghana":
            city_menu = MESSAGES["choose_city"]["english_gh"]
        elif lang == "french":
            city_menu = MESSAGES["choose_city"]["french"]
        else:
            city_menu = MESSAGES["choose_city"]["english_cm"]

        response = "CON " + city_menu

        # User selects a city
        if text in ["1", "2"]:
            city_idx = int(text) - 1
            cities_list = list(CITIES[country].keys())
            selected_city = cities_list[city_idx]
            ussd_session.selected_city = selected_city

            # Get flood risk
            lat, lon = CITIES[country][selected_city]
            risk_level = await get_flood_risk(lat, lon)

            # Store risk temporarily for next step
            ussd_session.temp_risk = risk_level
            update_ussd_session(ussd_session)

            # Show risk message + emergency option
            risk_msg = MESSAGES[f"risk_{risk_level}"][lang]
            post_menu = MESSAGES["post_risk_menu"][lang]
            response = "CON " + risk_msg + "\n\n" + post_menu
            ussd_session.step = "post_risk"
            update_ussd_session(ussd_session)

            # Auto-send SMS if high risk
            if risk_level == "high":
                alert_msg = MESSAGES["risk_high"][lang]
                sms_body = f"High Flood Alert - {selected_city}: {alert_msg}"
                await send_sms_alert("+" + phone, sms_body)

    elif ussd_session.step == "post_risk":
        # User is at "I am in danger" menu
        if text == "1":
            city = ussd_session.selected_city or "Unknown Location"
            risk = ussd_session.temp_risk or "unknown"

            # Log emergency to database
            log_emergency_alert(phone, city, country, risk)

            # Send confirmation SMS
            confirm_msg = MESSAGES["danger_confirmed"][lang]
            sms_body = f"EMERGENCY REPORTED!\nLocation: {city}\n{confirm_msg}"
            await send_sms_alert("+" + phone, sms_body)

            # End session with thanks
            response = "END " + confirm_msg + "\n\n" + MESSAGES["danger_thanks"][lang]

            # Reset session
            ussd_session.step = "start"
            ussd_session.selected_city = None
            ussd_session.temp_risk = None
            if country == "cameroon":
                ussd_session.lang = None
            update_ussd_session(ussd_session)

        elif text == "99":
            # Return to main menu
            ussd_session.step = "start"
            ussd_session.selected_city = None
            ussd_session.temp_risk = None
            update_ussd_session(ussd_session)

            welcome_key = "pidgin" if lang == "pidgin" else lang
            response = "CON " + MESSAGES["welcome"][welcome_key]

        else:
            response = "END Invalid option. " + MESSAGES["end"][lang]

    else:
        # Fallback
        response = "END " + MESSAGES["end"][lang]
        ussd_session.step = "start"
        update_ussd_session(ussd_session)

    return {"response": response}
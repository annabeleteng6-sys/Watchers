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


def detect_country(phone: str) -> str:
    return PREFIXES.get(phone[:3], "nigeria")


def resolve_language(country: str, session_lang: str | None) -> str:
    if country == "nigeria":
        return "pidgin"
    if country == "ghana":
        return "english"
    return session_lang or "french"


def build_city_menu(country: str, lang: str) -> str:
    cities = list(CITIES[country].keys())
    lines = []
    if lang == "french":
        lines.append("Choisissez votre ville :")
    else:
        lines.append("Choose your city:")
    
    for i, city in enumerate(cities, 1):
        lines.append(f"{i}. {city}")
    
    back_text = "Retour" if lang == "french" else "Back"
    lines.append(f"99. {back_text}")
    
    return "\n".join(lines)


async def ussd_handler(payload: dict) -> str:
    session_id = payload.get("sessionId")
    phone = payload.get("phoneNumber", "").lstrip("+")
    text = payload.get("text", "").strip()

    if not session_id or not phone:
        return "END Service unavailable. Try again later."

    country = detect_country(phone)

    # Reset on first interaction or 99
    if text == "" or text == "99":
        reset_ussd_session(session_id, phone, country)

    session = get_ussd_session(session_id, phone, country)
    lang = resolve_language(country, session.lang)

    # Welcome / Start
    if session.step == "start":
        welcome_key = "pidgin" if lang == "pidgin" else "english"
        if country == "cameroon":
            session.step = "choose_lang"
        else:
            session.step = "choose_city"
        update_ussd_session(session)
        return "CON " + MESSAGES["welcome"][welcome_key]

    # Cameroon Language Selection
    if session.step == "choose_lang":
        if text == "1":
            session.lang = "french"
        elif text == "2":
            session.lang = "english"
        else:
            return "CON " + MESSAGES["choose_lang"]["french"]

        session.step = "choose_city"
        update_ussd_session(session)
        return "CON " + build_city_menu(country, session.lang)

    # City Selection (All Countries)
    if session.step == "choose_city":
        if text == "99":
            reset_ussd_session(session_id, phone, country)
            return "CON " + MESSAGES["welcome"]["pidgin" if lang == "pidgin" else "english"]

        if not text.isdigit() or not (1 <= int(text) <= len(CITIES[country])):
            return "CON " + build_city_menu(country, lang)

        city_idx = int(text) - 1
        city = list(CITIES[country].keys())[city_idx]
        lat, lon = CITIES[country][city]

        risk = await get_flood_risk(lat, lon)

        session.selected_city = city
        session.temp_risk = risk
        session.step = "post_risk"
        update_ussd_session(session)

        risk_msg = MESSAGES[f"risk_{risk}"][lang]
        post_menu = MESSAGES["post_risk_menu"][lang]

        # Send high alert SMS only once
        if risk == "high" and not getattr(session, "alert_sent", False):
            await send_sms_alert("+" + phone, f"⚠️ HIGH FLOOD ALERT in {city}\n{risk_msg}")
            session.alert_sent = True
            update_ussd_session(session)

        return "CON " + risk_msg + "\n\n" + post_menu

    # Post-Risk: I am in danger
    if session.step == "post_risk":
        if text == "1":
            log_emergency_alert(
                phone,
                session.selected_city or "Unknown Location",
                country,
                session.temp_risk or "unknown"
            )
            confirm = MESSAGES["danger_confirmed"][lang]
            thanks = MESSAGES["danger_thanks"][lang]
            await send_sms_alert("+" + phone, f"🚨 EMERGENCY REPORTED\nLocation: {session.selected_city}\n{confirm}")
            reset_ussd_session(session_id, phone, country)
            return "END " + confirm + "\n\n" + thanks

        if text == "99":
            reset_ussd_session(session_id, phone, country)
            return "CON " + MESSAGES["welcome"]["pidgin" if lang == "pidgin" else "english"]

        return "END Invalid option."

    # Fallback
    reset_ussd_session(session_id, phone, country)
    return "END " + MESSAGES["end"][lang]
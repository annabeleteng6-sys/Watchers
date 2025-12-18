# utils/constants.py

# 5 major/flood-prone cities per country with coordinates (lat, lon)
CITIES = {
    "nigeria": {
        "Lagos": (6.5244, 3.3792),
        "Abuja": (9.0765, 7.3986),
        "Port Harcourt": (4.8156, 7.0498),
        "Yenagoa": (4.9267, 6.2676),
        "Lokoja": (7.8024, 6.7430),
    },
    "ghana": {
        "Accra": (5.6037, -0.1870),
        "Kumasi": (6.6666, -1.6163),
        "Ho": (6.6119, 0.4705),
        "Tamale": (9.4034, -0.8393),
        "Bolgatanga": (10.7856, -0.8514),
    },
    "cameroon": {
        "Yaoundé": (3.8667, 11.5167),
        "Douala": (4.0511, 9.7679),
        "Maroua": (10.5910, 14.3159),
        "Garoua": (9.3016, 13.3934),
        "Kousséri": (12.0769, 15.0306),
    },
}

PREFIXES = {
    "234": "nigeria",
    "233": "ghana",
    "237": "cameroon",
}

# Helper to dynamically build city menu with numbers
def build_city_menu_text(cities: dict, lang: str = "english") -> str:
    lines = ["Choose your city:" if lang != "french" else "Choisissez votre ville :"]
    for i, city in enumerate(cities.keys(), 1):
        lines.append(f"{i}. {city}")
    lines.append("99. Back" if lang != "french" else "99. Retour")
    return "\n".join(lines)

MESSAGES = {
    "welcome": {
        "pidgin": "Welcome! Check flood risk for your area.\n1. Continue",
        "english": "Welcome! Check flood risk for your area.\n1. Continue",
        "french": "Bienvenue ! Vérifiez le risque d'inondation dans votre région.\n1. Continuer",
    },
    "choose_lang": {
        "french": "Choisissez la langue :\n1. Français\n2. English",
    },
    # City menus are now dynamic — no need to hardcode
    # Use build_city_menu_text(CITIES[country], lang) in ussd.py
    "risk_low": {
        "pidgin": "Low flood risk. Small rain dey come, but no worry.",
        "english": "Low flood risk. Light rain expected, stay safe.",
        "french": "Faible risque d'inondation. Pluie légère prévue.",
    },
    "risk_medium": {
        "pidgin": "Medium flood risk. Heavy rain fit come. Dey careful!",
        "english": "Medium flood risk. Heavy rain possible. Be cautious.",
        "french": "Risque moyen d'inondation. Forte pluie possible. Soyez prudent.",
    },
    "risk_high": {
        "pidgin": "HIGH FLOOD ALERT! Heavy rain go fall. Move to higher ground now!",
        "english": "HIGH FLOOD ALERT! Heavy rainfall expected. Evacuate to higher ground!",
        "french": "ALERTE INONDATION ÉLEVÉE ! Fortes pluies prévues. Évacuez vers un terrain plus élevé !",
    },
    "post_risk_menu": {
        "pidgin": "1. I am in danger - Send help!\n99. Main menu",
        "english": "1. I am in danger - Send help!\n99. Main menu",
        "french": "1. Je suis en danger - Envoyez de l'aide !\n99. Menu principal",
    },
    "danger_confirmed": {
        "pidgin": "Help request received! Authorities don notify. Stay safe!",
        "english": "Emergency alert sent! Help is being notified. Stay safe!",
        "french": "Alerte d'urgence envoyée ! Les secours sont informés. Restez en sécurité !",
    },
    "danger_thanks": {
        "pidgin": "Thank you for reporting. Stay safe!",
        "english": "Thank you for reporting. Stay safe!",
        "french": "Merci d'avoir signalé. Restez en sécurité !",
    },
    "end": {
        "pidgin": "Thank you. Stay safe o!",
        "english": "Thank you. Stay safe!",
        "french": "Merci. Restez en sécurité !",
    },
}
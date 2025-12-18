import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
AT_USERNAME = os.getenv("AT_USERNAME", "sandbox")
AT_API_KEY = os.getenv("AT_API_KEY")
AT_SMS_FROM = os.getenv("AT_SMS_FROM", "on_watch")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./flood_alert.db")
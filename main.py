# main.py

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from services.ussd import ussd_handler
from services.weather import get_flood_risk
from database.base import create_db_and_tables
from utils.user_session import log_emergency_alert
from services.sms import send_sms_alert


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="OnWatch - Flood Alert System",
    description="Real-time flood risk alerts and emergency reporting via USSD and mobile app.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "message": "OnWatch is live 🌧️🚨",
        "endpoints": {
            "ussd": "/ussd (POST)",
            "mobile_risk": "/api/risk?lat=X&lon=Y",
            "mobile_sos": "/api/sos (POST)",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "OnWatch"}


# USSD Callback
@app.post("/ussd")
async def ussd_endpoint(
    sessionId: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(""),
    serviceCode: str = Form(...),
):
    payload = {
        "sessionId": sessionId,
        "phoneNumber": phoneNumber,
        "text": text,
        "serviceCode": serviceCode,
    }
    return await ussd_handler(payload)


# Mobile: Get flood risk
@app.get("/api/risk")
async def get_risk(lat: float, lon: float):
    risk_level = await get_flood_risk(lat, lon)
    messages = {
        "low": {"en": "Low flood risk.", "pidgin": "No worry.", "fr": "Faible risque."},
        "medium": {"en": "Medium risk — be cautious.", "pidgin": "Dey careful!", "fr": "Risque moyen."},
        "high": {"en": "HIGH ALERT!", "pidgin": "HIGH ALERT!", "fr": "ALERTE ÉLEVÉE!"}
    }
    return {
        "risk_level": risk_level,
        "message": messages[risk_level],
        "coordinates": {"lat": lat, "lon": lon},
        "timestamp": datetime.utcnow().isoformat()
    }


# Mobile: SOS Report
@app.post("/api/sos")
async def sos_report(
    phone: str,
    lat: float,
    lon: float,
    note: str | None = None,
    photo: UploadFile | None = File(None)
):
    if not phone.strip():
        raise HTTPException(status_code=400, detail="Phone number is required")

    location = f"GPS: {lat},{lon}"
    log_emergency_alert(phone, location, "mobile_app", "sos")

    if photo:
        contents = await photo.read()
        print(f"[SOS Photo] {len(contents)} bytes from {phone}")

    sms_body = f"ONWATCH SOS RECEIVED! Location: {lat},{lon}. Help coordinated."
    await send_sms_alert("+" + phone, sms_body)

    return {"status": "success", "message": "Emergency reported and confirmed"}
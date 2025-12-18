# main.py

from fastapi import FastAPI, Form, Request  # Add Request or use Form fields
from services.ussd import ussd_handler
from database.base import create_db_and_tables

app = FastAPI(title="OnWatch - Flood Risk Alert")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# NEW: Accept form data properly
@app.post("/ussd")
async def ussd_endpoint(
    sessionId: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(""),
    serviceCode: str = Form(...)  # Optional, but good to include
):
    payload = {
        "sessionId": sessionId,
        "phoneNumber": phoneNumber,
        "text": text,
        "serviceCode": serviceCode
    }
    return await ussd_handler(payload)

# Optional: Add a simple root for health check
@app.get("/")
def home():
    return {"message": "OnWatch is live 🌧️🚨", "docs": "/docs"}
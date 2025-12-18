# main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from services.ussd import ussd_handler
from database.base import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="OnWatch - Flood Alert USSD System",
    description="USSD-based flood risk alerts and emergency reporting for Nigeria, Ghana, and Cameroon.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "message": "OnWatch USSD Flood Alert System is live 🌧️🚨",
        "ussd_callback": "/ussd (POST → plain text)",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "OnWatch USSD"}


# USSD Callback — returns plain text for Africa's Talking
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
    response_text = await ussd_handler(payload)
    return PlainTextResponse(response_text)
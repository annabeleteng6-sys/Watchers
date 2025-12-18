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


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "OnWatch USSD backend live"}


# THIS IS THE CRITICAL ENDPOINT
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
    return PlainTextResponse(response_text)  # ← Plain text, no JSON!
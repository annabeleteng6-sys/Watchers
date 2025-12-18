from fastapi import FastAPI
from services.ussd import ussd_handler
from database.base import create_db_and_tables

app = FastAPI(title="Flood Risk USSD Alert")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/ussd")
async def ussd_endpoint(payload: dict):
    return await ussd_handler(payload)
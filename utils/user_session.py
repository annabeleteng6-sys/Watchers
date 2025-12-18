from sqlmodel import select
from models import USSDSession, EmergencyAlert
from database.session import get_sync_session
from datetime import datetime

def get_ussd_session(session_id: str, phone: str, country: str) -> USSDSession:
    db = get_sync_session()
    try:
        statement = select(USSDSession).where(USSDSession.session_id == session_id)
        result = db.exec(statement)
        ussd_session = result.first()

        if not ussd_session:
            ussd_session = USSDSession(
                session_id=session_id,
                phone_number="+" + phone if not phone.startswith("+") else phone,
                country=country,
                step="start",
            )
            db.add(ussd_session)
            db.commit()
            db.refresh(ussd_session)
        return ussd_session
    finally:
        db.close()

def update_ussd_session(ussd_session: USSDSession) -> None:
    db = get_sync_session()
    try:
        ussd_session.last_updated = datetime.utcnow()
        db.add(ussd_session)
        db.commit()
        db.refresh(ussd_session)
    finally:
        db.close()

def reset_ussd_session(session_id: str, phone: str, country: str) -> None:
    db = get_sync_session()
    try:
        statement = select(USSDSession).where(USSDSession.session_id == session_id)
        result = db.exec(statement)
        ussd_session = result.first()
        if ussd_session:
            ussd_session.lang = None
            ussd_session.step = "start"
            ussd_session.selected_city = None
            ussd_session.temp_risk = None
            ussd_session.last_updated = datetime.utcnow()
            db.add(ussd_session)
            db.commit()
    finally:
        db.close()

def log_emergency_alert(phone: str, city: str, country: str, risk_level: str | None = None) -> None:
    db = get_sync_session()
    try:
        alert = EmergencyAlert(
            phone_number="+" + phone if not phone.startswith("+") else phone,
            city=city,
            country=country,
            risk_level=risk_level,
        )
        db.add(alert)
        db.commit()
    finally:
        db.close()
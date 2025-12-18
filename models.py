from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class USSDSession(SQLModel, table=True):
    session_id: str = Field(primary_key=True)
    phone_number: str = Field(index=True)
    country: str
    lang: Optional[str] = None
    step: str = "start"
    selected_city: Optional[str] = None
    temp_risk: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class EmergencyAlert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str = Field(index=True)
    city: str
    country: str
    reported_at: datetime = Field(default_factory=datetime.utcnow)
    risk_level: Optional[str] = None
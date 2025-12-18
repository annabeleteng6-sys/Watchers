from sqlmodel import SQLModel
from database.session import engine
from models import USSDSession, EmergencyAlert

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
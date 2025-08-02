from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"

    unique_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    caller_number = Column(String(20), nullable=False)
    receiver_number = Column(String(20), nullable=False)
    call_started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    call_answered = Column(Boolean, default=False)
    call_rejected = Column(Boolean, default=False)
    call_ended_at = Column(DateTime, nullable=True)
    call_duration_seconds = Column(Integer, nullable=True)

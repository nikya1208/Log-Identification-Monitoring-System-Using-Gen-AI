
# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogEntryCreate(BaseModel):
    log_message: str
    severity: str

class LogEntryResponse(BaseModel):
    id: int
    timestamp: datetime
    log_message: str
    severity: str
    processed: bool

    class Config:
        from_attributes = True  # Ensures compatibility with SQLAlchemy models

class AnomalyDetectionResult(BaseModel):
    log_id: int
    anomaly_detected: bool
    description: Optional[str] = None

class AlertRequest(BaseModel):  #  Added missing AlertRequest model
    message: str
    severity: str
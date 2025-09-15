# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\models.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class LogEntry(Base):
    """Table to store log entries."""
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    log_message = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    processed = Column(Boolean, default=False)

    # Relationship with AnomalyDetectionResult
    anomalies = relationship("AnomalyDetectionResult", back_populates="log")

class AnomalyDetectionResult(Base):
    """Table to store anomaly detection results."""
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("logs.id"), nullable=False)
    anomaly_detected = Column(Boolean, default=False)
    description = Column(String, nullable=True)

    # Relationship with LogEntry
    log = relationship("LogEntry", back_populates="anomalies")

class Alert(Base):
    """Table to store triggered alerts."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)  # e.g., ERROR, WARNING
    message = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


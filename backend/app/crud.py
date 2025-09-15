# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\crud.py
from sqlalchemy.orm import Session
from app import models, schemas

def create_log_entry(db: Session, log: schemas.LogEntryCreate):
    db_log = models.LogEntry(log_message=log.log_message, severity=log.severity)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.LogEntry).offset(skip).limit(limit).all()

def get_log_by_id(db: Session, log_id: int):
    return db.query(models.LogEntry).filter(models.LogEntry.id == log_id).first()

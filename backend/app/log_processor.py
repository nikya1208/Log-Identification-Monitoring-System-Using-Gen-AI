# app/log_processor.py
import asyncio
from app.database import SessionLocal
from app.models import LogEntry
from app.ai_model import detect_anomalies

async def process_logs():
    while True:
        db = SessionLocal()
        logs = db.query(LogEntry).filter(LogEntry.processed == False).all()

        for log in logs:
            if detect_anomalies(log.log_message):
                print(f"Anomaly detected in log: {log.id}")
            log.processed = True
            db.commit()

        db.close()
        await asyncio.sleep(5)  # Poll every 5 seconds

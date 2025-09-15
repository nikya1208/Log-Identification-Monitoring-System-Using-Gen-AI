# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\routes\log_routes.py

# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from datetime import datetime

# from app.schemas.log_schema import LogEntryCreate
# from app.database import SessionLocal
# from app.models.log_model import LogEntry  # Your SQLAlchemy model
# from app.ai_model import detect_anomalies
# from app.routes.ws import broadcast_log, broadcast_alert

# router = APIRouter()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/logs/")
# async def create_log(
#     log: LogEntryCreate,
#     db: Session = Depends(get_db)
# ):
#     """
#     1. Insert the log into the database
#     2. Run anomaly detection
#     3. Broadcast the log (and an alert if it's anomalous)
#     """
#     # 1. Perform anomaly detection
#     is_anomaly = detect_anomalies(log.message)

#     # 2. Create & save the LogEntry
#     db_log = LogEntry(
#         timestamp=log.timestamp,
#         level=log.severity,         # Assuming your schema's 'severity' maps to model's 'level'
#         message=log.message,
#         source=log.service_name,    # Assuming schema's 'service_name' maps to model's 'source'
#         is_anomaly=is_anomaly
#     )
#     try:
#         db.add(db_log)
#         db.commit()
#         db.refresh(db_log)
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"DB error: {e}")

#     # 3. Broadcast the new log
#     await broadcast_log({
#         "timestamp": db_log.timestamp.isoformat(),
#         "level": db_log.level,
#         "message": db_log.message,
#         "source": db_log.source,
#         "is_anomaly": db_log.is_anomaly
#     })

#     # 4. If anomalous, broadcast an alert
#     if is_anomaly:
#         await broadcast_alert({
#             "title": "Anomaly Detected",
#             "message": f"Anomaly in service `{db_log.source}`: {db_log.message}",
#             "severity": "HIGH",
#             "timestamp": datetime.utcnow().isoformat(),
#             "type": "alert"
#         })

#     return {"message": "Log created successfully", "log": {
#         "id": db_log.id,
#         "timestamp": db_log.timestamp,
#         "level": db_log.level,
#         "message": db_log.message,
#         "source": db_log.source,
#         "is_anomaly": db_log.is_anomaly
#     }}





# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\routes\log_routes.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.log_schema import LogEntryCreate
from app.database import SessionLocal
from app.models.log_model import LogEntry
from app.ai_model import detect_anomalies
from app.routes.ws import broadcast_log, broadcast_alert

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/logs/")
async def create_log(
    log: LogEntryCreate,
    db: Session = Depends(get_db)
):
    """
    1. Use Trie cache + AI to check anomaly
    2. Store the log
    3. Broadcast via WebSocket
    4. Alert if anomalous
    """
    try:
        # 1. Detect anomaly (uses cache internally)
        is_anomaly = detect_anomalies(log.message)

        # 2. Save the log
        db_log = LogEntry(
            timestamp=log.timestamp,
            level=log.severity,
            message=log.message,
            source=log.service_name,
            is_anomaly=is_anomaly
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        # 3. Broadcast log
        await broadcast_log({
            "timestamp": db_log.timestamp.isoformat(),
            "level": db_log.level,
            "message": db_log.message,
            "source": db_log.source,
            "is_anomaly": db_log.is_anomaly
        })

        # 4. If anomaly, alert
        if is_anomaly:
            await broadcast_alert({
                "title": "Anomaly Detected",
                "message": f"Anomaly in service `{db_log.source}`: {db_log.message}",
                "severity": "HIGH",
                "timestamp": datetime.utcnow().isoformat(),
                "type": "alert"
            })

        return {
            "message": "Log created successfully",
            "log": {
                "id": db_log.id,
                "timestamp": db_log.timestamp,
                "level": db_log.level,
                "message": db_log.message,
                "source": db_log.source,
                "is_anomaly": db_log.is_anomaly
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Log insert error: {e}")

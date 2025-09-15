# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\routes\logs.py

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import datetime
from app.routes.ws import broadcast_log  #  WebSocket broadcast

router = APIRouter()

# Sample in-memory log DB (replace with PostgreSQL or any DB)
logs_db = [
    {"timestamp": "2025-04-04T15:00:00", "level": "ERROR", "message": "Database connection failed", "source": "backend"},
    {"timestamp": "2025-04-04T15:05:00", "level": "INFO", "message": "User login successful", "source": "auth"},
    {"timestamp": "2025-04-04T15:10:00", "level": "WARNING", "message": "High memory usage detected", "source": "monitoring"},
    # ...more logs
]

class LogEntry(BaseModel):
    timestamp: datetime.datetime
    level: str
    message: str
    source: str

@router.get("/", response_model=List[LogEntry])
def get_logs(
    level: Optional[str] = Query(None, description="Filter logs by level"),
    source: Optional[str] = Query(None, description="Filter logs by source"),
    keyword: Optional[str] = Query(None, description="Search logs by keyword")
) -> List[LogEntry]:
    """
    Retrieve logs with optional filters:
    - `level`: Filter logs by level (INFO, ERROR, WARNING, etc.)
    - `source`: Filter logs by source (backend, auth, etc.)
    - `keyword`: Search logs by message content
    """
    filtered_logs = logs_db

    if level:
        filtered_logs = [log for log in filtered_logs if log["level"].lower() == level.lower()]
    if source:
        filtered_logs = [log for log in filtered_logs if log["source"].lower() == source.lower()]
    if keyword:
        filtered_logs = [log for log in filtered_logs if keyword.lower() in log["message"].lower()]

    return filtered_logs

@router.post("/", response_model=LogEntry)
async def add_log(log: LogEntry):
    """
    Add a new log entry and broadcast it via WebSocket.
    """
    log_data = log.dict()
    logs_db.append(log_data)

    await broadcast_log(log_data)  #  Real-time broadcast to clients

    return log


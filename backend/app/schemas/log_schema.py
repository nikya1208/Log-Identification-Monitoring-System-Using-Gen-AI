# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\schemas\log_schema.py
from pydantic import BaseModel
from datetime import datetime

class LogEntryCreate(BaseModel):
    service_name: str
    severity: str
    message: str
    timestamp: datetime

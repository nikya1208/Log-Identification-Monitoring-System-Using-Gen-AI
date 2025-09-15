# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\routes\test_ws.py
from fastapi import APIRouter
from app.routes.ws import broadcast_log, broadcast_alert

router = APIRouter()

@router.get("/test/log")
async def test_log():
    await broadcast_log({
        "message": "Test log from backend 🚀",
        "level": "INFO",
        "timestamp": "2025-04-05 12:05:00"
    })
    return {"status": "log sent"}

@router.get("/test/alert")
async def test_alert():
    await broadcast_alert({
        "title": " Critical Alert",
        "message": "Disk usage exceeded 90%",
        "severity": "critical",
        "timestamp": "2025-04-05 12:05:30"
    })
    return {"status": "alert sent"}

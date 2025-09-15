# app/routes/__init__.py
from fastapi import APIRouter
from app.routes import logs, alerts

router = APIRouter()
router.include_router(logs.router, prefix="/logs", tags=["Logs"])
router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

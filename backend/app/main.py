# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\main.py

# import logging
# import os
# import asyncio
# from datetime import datetime

# from fastapi import FastAPI, BackgroundTasks, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
# from prometheus_fastapi_instrumentator import Instrumentator

# # Local imports
# from app.database import engine
# from app.config import settings
# from app.utils.smtp_server import send_email_alert, send_slack_alert
# from app.routes.ws_manager import manager
# from app.routes.ws import simulate_logs, broadcast_alert

# # ✅ Create logs directory
# os.makedirs("logs", exist_ok=True)

# # ✅ Setup logging
# logging.basicConfig(
#     filename="logs/app.log",
#     format="%(asctime)s %(levelname)s %(name)s - %(message)s",
#     level=logging.INFO,
# )

# # ✅ Initialize FastAPI
# app = FastAPI(
#     title="Log Monitoring API",
#     version="1.0",
#     description="API for log identification, filtering, and monitoring."
# )

# logging.info("🚀 Log Monitoring API starting...")

# # ✅ Serve static files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("app/static/favicon.ico")

# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title="Log Monitoring API Docs",
#         favicon_url="/static/favicon.ico"
#     )

# @app.get("/redoc", include_in_schema=False)
# async def custom_redoc_html():
#     return get_redoc_html(
#         openapi_url=app.openapi_url,
#         title="Log Monitoring ReDoc",
#         favicon_url="/static/favicon.ico"
#     )

# # ✅ Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Prometheus metrics
# Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# # ✅ Include routers
# try:
#     from app.routes import logs, alerts, ws
#     app.include_router(logs.router, prefix="/logs", tags=["Logs"])
#     app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
#     app.include_router(ws.router)  # includes /ws/logs and /ws/alerts
#     logging.info("✅ Routers registered")
# except Exception as e:
#     logging.error(f"❌ Failed to register routers: {e}")

# # ✅ Root endpoint
# @app.get("/")
# def read_root():
#     logging.info("✅ Root endpoint accessed")
#     return {
#         "message": "Log Monitoring System is Running",
#         "database_url": settings.database_url,
#         "email_sender": settings.email_sender,
#         "email_receiver": settings.email_receiver,
#         "slack_channel": settings.slack_channel
#     }

# # ✅ Test email/slack alerts
# @app.post("/test-alert")
# def test_alert(background_tasks: BackgroundTasks):
#     subject = "Test Alert: Email from FastAPI"
#     body = "This is a test email sent from your FastAPI app."
#     message = "Test Slack Alert: FastAPI app is working!"

#     background_tasks.add_task(send_email_alert, subject, body)
#     background_tasks.add_task(send_slack_alert, message)

#     logging.info("✅ Test alert triggered via Email & Slack.")
#     return {"message": "Test alerts triggered (Email & Slack)."}

# # ✅ Test log WebSocket broadcast
# @app.get("/test/log")
# async def test_log_ws():
#     await manager.broadcast_json({
#         "type": "log",
#         "level": "INFO",
#         "message": "Test log message from FastAPI WebSocket",
#         "timestamp": datetime.utcnow().isoformat()
#     })
#     logging.info("✅ Test WebSocket log sent")
#     return {"status": "WebSocket log broadcasted"}

# # ✅ Test alert WebSocket broadcast
# @app.get("/test/alert")
# async def test_alert_ws():
#     await broadcast_alert({
#         "title": "Test Alert from FastAPI WebSocket",
#         "message": "This is a test alert for WebSocket verification.",
#         "severity": "HIGH",
#         "timestamp": datetime.utcnow().isoformat(),
#         "type": "alert",
#     })
#     logging.warning("⚠️ Test WebSocket alert sent")
#     return {"status": "WebSocket alert broadcasted"}

# # ✅ Fallback WebSocket endpoints (if `ws.router` fails to load)
# @app.websocket("/ws/logs")
# async def fallback_ws_logs(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text("✅ WebSocket /ws/logs is working!")
#     await websocket.close()

# @app.websocket("/ws/alerts")
# async def fallback_ws_alerts(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text("✅ WebSocket /ws/alerts is working!")
#     await websocket.close()

# # ✅ Start simulated logs on startup
# @app.on_event("startup")
# async def start_simulator():
#     logging.info("🔁 Starting log simulator...")
#     asyncio.create_task(simulate_logs())

# # ✅ Local dev
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)



# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\main.py

# import logging
# import os
# import asyncio
# from datetime import datetime

# from fastapi import FastAPI, BackgroundTasks, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
# from prometheus_fastapi_instrumentator import Instrumentator

# # Local imports
# from app.database import engine
# from app.config import settings
# from app.utils.smtp_server import send_email_alert, send_slack_alert
# from app.routes.ws_manager import manager
# from app.routes.ws import simulate_logs, broadcast_alert

# #  Create log directory shared with Promtail
# log_dir = "/var/log/fastapi"
# os.makedirs(log_dir, exist_ok=True)
# log_file = os.path.join(log_dir, "app.log")

# #  Setup file logging for Promtail
# file_handler = logging.handlers.RotatingFileHandler(
#     log_file, maxBytes=10 * 1024 * 1024, backupCount=5
# )
# formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
# file_handler.setFormatter(formatter)

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logger.addHandler(file_handler)

# #  Initialize FastAPI
# app = FastAPI(
#     title="Log Monitoring API",
#     version="1.0",
#     description="API for log identification, filtering, and monitoring."
# )

# logging.info(" Log Monitoring API starting...")

# #  Serve static files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("app/static/favicon.ico")

# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title="Log Monitoring API Docs",
#         favicon_url="/static/favicon.ico"
#     )

# @app.get("/redoc", include_in_schema=False)
# async def custom_redoc_html():
#     return get_redoc_html(
#         openapi_url=app.openapi_url,
#         title="Log Monitoring ReDoc",
#         favicon_url="/static/favicon.ico"
#     )

# #  Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #  Prometheus metrics
# Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# #  Include routers
# try:
#     from app.routes import logs, alerts, ws
#     app.include_router(logs.router, prefix="/logs", tags=["Logs"])
#     app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
#     app.include_router(ws.router)
#     logging.info(" Routers registered")
# except Exception as e:
#     logging.error(f" Failed to register routers: {e}")

# @app.get("/")
# def read_root():
#     logging.info(" Root endpoint accessed")
#     return {
#         "message": "Log Monitoring System is Running",
#         "database_url": settings.database_url,
#         "email_sender": settings.email_sender,
#         "email_receiver": settings.email_receiver,
#         "slack_channel": settings.slack_channel
#     }

# @app.post("/test-alert")
# def test_alert(background_tasks: BackgroundTasks):
#     subject = "Test Alert: Email from FastAPI"
#     body = "This is a test email sent from your FastAPI app."
#     message = "Test Slack Alert: FastAPI app is working!"

#     background_tasks.add_task(send_email_alert, subject, body)
#     background_tasks.add_task(send_slack_alert, message)

#     logging.info(" Test alert triggered via Email & Slack.")
#     return {"message": "Test alerts triggered (Email & Slack)."}

# @app.get("/test/log")
# async def test_log_ws():
#     await manager.broadcast_json({
#         "type": "log",
#         "level": "INFO",
#         "message": "Test log message from FastAPI WebSocket",
#         "timestamp": datetime.utcnow().isoformat()
#     })
#     logging.info(" Test WebSocket log sent")
#     return {"status": "WebSocket log broadcasted"}

# @app.get("/test/alert")
# async def test_alert_ws():
#     await broadcast_alert({
#         "title": "Test Alert from FastAPI WebSocket",
#         "message": "This is a test alert for WebSocket verification.",
#         "severity": "HIGH",
#         "timestamp": datetime.utcnow().isoformat(),
#         "type": "alert",
#     })
#     logging.warning(" Test WebSocket alert sent")
#     return {"status": "WebSocket alert broadcasted"}

# @app.websocket("/ws/logs")
# async def fallback_ws_logs(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text(" WebSocket /ws/logs is working!")
#     await websocket.close()

# @app.websocket("/ws/alerts")
# async def fallback_ws_alerts(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text(" WebSocket /ws/alerts is working!")
#     await websocket.close()

# @app.on_event("startup")
# async def start_simulator():
#     logging.info(" Starting log simulator...")
#     asyncio.create_task(simulate_logs())

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)



# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\main.py

# import logging
# import os
# import asyncio
# from datetime import datetime
# from logging.handlers import RotatingFileHandler

# from fastapi import FastAPI, BackgroundTasks, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
# from prometheus_fastapi_instrumentator import Instrumentator

# # Local imports
# from app.database import engine
# from app.config import settings
# from app.utils.smtp_server import send_email_alert, send_slack_alert
# from app.routes.ws_manager import manager
# from app.routes.ws import simulate_logs, broadcast_alert

# # === Setup Logging Directory ===
# log_dir = "/var/log/fastapi"
# os.makedirs(log_dir, exist_ok=True)
# log_file = os.path.join(log_dir, "app.log")

# file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
# formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
# file_handler.setFormatter(formatter)

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logger.addHandler(file_handler)

# # === Initialize FastAPI App ===
# app = FastAPI(
#     title="Log Monitoring API",
#     version="1.0",
#     description="API for log identification, filtering, and monitoring."
# )

# logging.info("Log Monitoring API starting...")

# # === Static Files & Docs ===
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("app/static/favicon.ico")

# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title="Log Monitoring API Docs",
#         favicon_url="/static/favicon.ico"
#     )

# @app.get("/redoc", include_in_schema=False)
# async def custom_redoc_html():
#     return get_redoc_html(
#         openapi_url=app.openapi_url,
#         title="Log Monitoring ReDoc",
#         favicon_url="/static/favicon.ico"
#     )

# # === CORS Middleware ===
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # === Prometheus Instrumentation (moved outside startup event) ===
# instrumentator = Instrumentator(
#     should_group_status_codes=True,
#     should_ignore_untemplated=True,
#     should_respect_env_var=False,
#     excluded_handlers=["/favicon.ico"],
# )
# instrumentator.instrument(app).expose(app, endpoint="/metrics")
# logging.info("Prometheus metrics instrumentation added.")

# # === Startup Event ===
# @app.on_event("startup")
# async def startup_event():
#     logging.info("Starting log simulator...")
#     asyncio.create_task(simulate_logs())

# # === Include Routers ===
# try:
#     from app.routes import logs, alerts, ws
#     app.include_router(logs.router, prefix="/logs", tags=["Logs"])
#     app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
#     app.include_router(ws.router)
#     logging.info("Routers registered")
# except Exception as e:
#     logging.error(f"Failed to register routers: {e}")

# # === Root Endpoint ===
# @app.get("/")
# def read_root():
#     logging.info("Root endpoint accessed")
#     return {
#         "message": "Log Monitoring System is Running",
#         "database_url": settings.database_url,
#         "email_sender": settings.email_sender,
#         "email_receiver": settings.email_receiver,
#         "slack_channel": settings.slack_channel
#     }

# # === Test Endpoints ===
# @app.post("/test-alert")
# def test_alert(background_tasks: BackgroundTasks):
#     subject = "Test Alert: Email from FastAPI"
#     body = "This is a test email sent from your FastAPI app."
#     message = "Test Slack Alert: FastAPI app is working!"
#     background_tasks.add_task(send_email_alert, subject, body)
#     background_tasks.add_task(send_slack_alert, message)
#     logging.info("Test alert triggered via Email & Slack.")
#     return {"message": "Test alerts triggered (Email & Slack)."}

# @app.get("/test/log")
# async def test_log_ws():
#     await manager.broadcast_json({
#         "type": "log",
#         "level": "INFO",
#         "message": "Test log message from FastAPI WebSocket",
#         "timestamp": datetime.utcnow().isoformat()
#     })
#     logging.info("Test WebSocket log sent")
#     return {"status": "WebSocket log broadcasted"}

# @app.get("/test/alert")
# async def test_alert_ws():
#     await broadcast_alert({
#         "title": "Test Alert from FastAPI WebSocket",
#         "message": "This is a test alert for WebSocket verification.",
#         "severity": "HIGH",
#         "timestamp": datetime.utcnow().isoformat(),
#         "type": "alert",
#     })
#     logging.warning("Test WebSocket alert sent")
#     return {"status": "WebSocket alert broadcasted"}

# # === Fallback WebSocket Routes ===
# @app.websocket("/ws/logs")
# async def fallback_ws_logs(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text("WebSocket /ws/logs is working!")
#     await websocket.close()

# @app.websocket("/ws/alerts")
# async def fallback_ws_alerts(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text("WebSocket /ws/alerts is working!")
#     await websocket.close()

# # === Run with Uvicorn if Standalone ===
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)



# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\main.py

import logging
import os
import asyncio
from datetime import datetime
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from prometheus_fastapi_instrumentator import Instrumentator

# Local imports
from app.database import engine
from app.config import settings
from app.utils.smtp_server import send_email_alert, send_slack_alert
from app.routes.ws_manager import manager
from app.routes.ws import simulate_logs, broadcast_alert

# === Setup Logging Directory ===
log_dir = "/var/log/fastapi"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")

file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# === Initialize FastAPI App ===
app = FastAPI(
    title="Log Monitoring API",
    version="1.0",
    description="API for log identification, filtering, and monitoring."
)

logging.info("Log Monitoring API starting...")

# === Static Files & Docs ===
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Log Monitoring API Docs",
        favicon_url="/static/favicon.ico"
    )

@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="Log Monitoring ReDoc",
        favicon_url="/static/favicon.ico"
    )

# === CORS Middleware ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Prometheus Instrumentation ===
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    excluded_handlers=["/favicon.ico"],
)
instrumentator.instrument(app).expose(app, endpoint="/metrics")
logging.info("Prometheus metrics instrumentation added.")

# === Startup Event ===
@app.on_event("startup")
async def startup_event():
    logging.info("Starting log simulator...")
    asyncio.create_task(simulate_logs())

# === Include Routers ===
try:
    from app.routes import logs, alerts, ws
    app.include_router(logs.router, prefix="/logs", tags=["Logs"])
    app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
    app.include_router(ws.router)
    logging.info("Routers registered")
except Exception as e:
    logging.error(f"Failed to register routers: {e}")

# === Root Endpoint ===
@app.get("/")
def read_root():
    logging.info("Root endpoint accessed")
    return {
        "message": "Log Monitoring System is Running",
        "database_url": settings.database_url,
        "email_sender": settings.email_sender,
        "email_receiver": settings.email_receiver,
        "slack_channel": settings.slack_channel
    }

# === Test Endpoints ===
@app.post("/test-alert")
def test_alert(background_tasks: BackgroundTasks):
    subject = "Test Alert: Email from FastAPI"
    body = "This is a test email sent from your FastAPI app."
    message = "Test Slack Alert: FastAPI app is working!"
    background_tasks.add_task(send_email_alert, subject, body)
    background_tasks.add_task(send_slack_alert, message)
    logging.info("Test alert triggered via Email & Slack.")
    return {"message": "Test alerts triggered (Email & Slack)."}

@app.get("/test/log")
async def test_log_ws():
    await manager.broadcast_json({
        "type": "log",
        "level": "INFO",
        "message": "Test log message from FastAPI WebSocket",
        "timestamp": datetime.utcnow().isoformat()
    })
    logging.info("Test WebSocket log sent")
    return {"status": "WebSocket log broadcasted"}

@app.get("/test/alert")
async def test_alert_ws():
    await broadcast_alert({
        "title": "Test Alert from FastAPI WebSocket",
        "message": "This is a test alert for WebSocket verification.",
        "severity": "HIGH",
        "timestamp": datetime.utcnow().isoformat(),
        "type": "alert",
    })
    logging.warning("Test WebSocket alert sent")
    return {"status": "WebSocket alert broadcasted"}

# === Run with Uvicorn if Standalone ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

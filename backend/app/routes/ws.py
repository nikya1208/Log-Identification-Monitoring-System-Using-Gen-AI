# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\routes\ws.py

# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from typing import List
# from datetime import datetime
# import asyncio
# import random
# import json

# router = APIRouter()

# # -------------------------
# # WebSocket Connection Manager
# # -------------------------

# class ConnectionManager:
#     def __init__(self):
#         self.clients: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.clients.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         if websocket in self.clients:
#             self.clients.remove(websocket)

#     async def broadcast_json(self, message: dict):
#         disconnected = []
#         for client in self.clients:
#             try:
#                 await client.send_text(json.dumps(message, ensure_ascii=False))
#             except WebSocketDisconnect:
#                 disconnected.append(client)
#             except Exception as e:
#                 print(f"⚠️ Error sending message: {e}")
#                 disconnected.append(client)
#         for dc in disconnected:
#             self.disconnect(dc)

# # Create separate managers for logs and alerts
# log_manager = ConnectionManager()
# alert_manager = ConnectionManager()

# # -------------------------
# # WebSocket Routes
# # -------------------------

# @router.websocket("/ws/logs")
# async def websocket_logs(websocket: WebSocket):
#     await log_manager.connect(websocket)
#     print(f"📡 [LOG WS] Client connected. Total: {len(log_manager.clients)}")
#     try:
#         while True:
#             await asyncio.sleep(60)  # Passive wait to keep connection alive
#     except WebSocketDisconnect:
#         log_manager.disconnect(websocket)
#         print(f"❌ [LOG WS] Client disconnected. Total: {len(log_manager.clients)}")

# @router.websocket("/ws/alerts")
# async def websocket_alerts(websocket: WebSocket):
#     await alert_manager.connect(websocket)
#     print(f"📡 [ALERT WS] Client connected. Total: {len(alert_manager.clients)}")
#     try:
#         while True:
#             await asyncio.sleep(60)
#     except WebSocketDisconnect:
#         alert_manager.disconnect(websocket)
#         print(f"❌ [ALERT WS] Client disconnected. Total: {len(alert_manager.clients)}")

# # -------------------------
# # Public Broadcast Methods
# # -------------------------

# async def broadcast_log(log: dict):
#     if isinstance(log.get("timestamp"), datetime):
#         log["timestamp"] = log["timestamp"].isoformat()
#     await log_manager.broadcast_json({"type": "log", **log})

# async def broadcast_alert(alert: dict):
#     if isinstance(alert.get("timestamp"), datetime):
#         alert["timestamp"] = alert["timestamp"].isoformat()
#     await alert_manager.broadcast_json({"type": "alert", **alert})

# # -------------------------
# # Dummy Messages
# # -------------------------

# MESSAGES = [
#     ("CPU usage is high", "WARNING", "Server-1"),
#     ("Memory leak detected", "ERROR", "App-Engine"),
#     ("New user login", "INFO", "Auth-Service"),
#     ("Disk space below threshold", "WARNING", "Storage-Node"),
#     ("Backup completed successfully", "INFO", "Backup-Service"),
#     ("Service restarted unexpectedly", "ERROR", "API-Gateway"),
#     ("Database connection established", "INFO", "DB-Connector"),
#     ("Configuration file updated", "INFO", "Admin-Console"),
#     ("Unusual traffic detected", "WARNING", "Firewall"),
#     ("SSL certificate expired", "ERROR", "Web-Server")
# ]

# # -------------------------
# # Dummy Log Simulation
# # -------------------------

# async def simulate_logs():
#     while True:
#         msg, level, source = random.choice(MESSAGES)
#         await broadcast_log({
#             "message": msg,
#             "level": level,
#             "source": source,
#             "timestamp": datetime.now().isoformat()
#         })
#         await asyncio.sleep(2)

# # -------------------------
# # Dummy Alert Simulation
# # -------------------------

# async def simulate_alerts():
#     while True:
#         title = random.choice(["Disk Space Low", "Memory Leak", "CPU Overload", "High Latency"])
#         message = random.choice([
#             "Warning: Disk space is critically low.",
#             "Error: Memory consumption exceeds the threshold.",
#             "Alert: CPU usage has spiked above normal levels.",
#             "Critical: Latency is higher than expected in service XYZ."
#         ])
#         severity = random.choice(["HIGH", "WARNING", "INFO"])
        
#         await broadcast_alert({
#             "title": title,
#             "message": message,
#             "severity": severity,
#             "timestamp": datetime.now().isoformat()
#         })
#         await asyncio.sleep(5)



# app/routes/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
import asyncio
import random
import json

router = APIRouter()

__all__ = ["simulate_logs", "broadcast_alert"]

class ConnectionManager:
    def __init__(self):
        self.clients: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.clients:
            self.clients.remove(websocket)

    async def broadcast_json(self, message: dict):
        for client in self.clients[:]:
            try:
                await client.send_text(json.dumps(message))
            except WebSocketDisconnect:
                self.disconnect(client)
            except Exception as e:
                print(f"⚠️ Error broadcasting: {e}")
                self.disconnect(client)

# Managers
log_manager = ConnectionManager()
alert_manager = ConnectionManager()

@router.websocket("/ws/logs")
async def ws_logs(websocket: WebSocket):
    await log_manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        log_manager.disconnect(websocket)

@router.websocket("/ws/alerts")
async def ws_alerts(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)

# Broadcast APIs
async def broadcast_log(log: dict):
    log["timestamp"] = log.get("timestamp", datetime.utcnow().isoformat())
    await log_manager.broadcast_json({"type": "log", **log})

async def broadcast_alert(alert: dict):
    alert["timestamp"] = alert.get("timestamp", datetime.utcnow().isoformat())
    await alert_manager.broadcast_json({"type": "alert", **alert})

# Dummy messages
DUMMY_MESSAGES = [
    ("CPU usage is high", "WARNING", "Server-1"),
    ("Memory leak detected", "ERROR", "App-Engine"),
    ("New user login", "INFO", "Auth-Service"),
    ("Disk space low", "WARNING", "Storage"),
    ("Backup successful", "INFO", "Backup"),
    ("Unexpected restart", "ERROR", "Gateway"),
    ("DB connected", "INFO", "Database"),
    ("Config updated", "INFO", "Admin"),
    ("Suspicious traffic", "WARNING", "Firewall"),
    ("SSL expired", "ERROR", "Web Server")
]

# Log simulator
async def simulate_logs():
    while True:
        msg, level, source = random.choice(DUMMY_MESSAGES)
        await broadcast_log({
            "message": msg,
            "level": level,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        })
        await asyncio.sleep(2)

# Alert simulator
async def simulate_alerts():
    while True:
        title = random.choice(["Disk Low", "Memory Leak", "CPU Spike"])
        message = random.choice([
            "Disk space is low.",
            "Memory usage is high.",
            "CPU load critical."
        ])
        severity = random.choice(["INFO", "WARNING", "HIGH"])
        await broadcast_alert({
            "title": title,
            "message": message,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        })
        await asyncio.sleep(5)
7
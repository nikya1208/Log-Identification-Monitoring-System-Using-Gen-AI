# app/services/websocket_manager.py
from fastapi import WebSocket
from typing import List
import json

active_connections: List[WebSocket] = []

async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

def disconnect(websocket: WebSocket):
    if websocket in active_connections:
        active_connections.remove(websocket)

async def broadcast(log_data: dict):
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(log_data))
        except:
            disconnected.append(connection)

    for conn in disconnected:
        active_connections.remove(conn)

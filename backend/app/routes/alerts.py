# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\routes\alerts.py
from fastapi import APIRouter, HTTPException, BackgroundTasks, Body
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import asyncio

from app.config import settings
from app.routes.ws_manager import manager  # Using ConnectionManager

router = APIRouter()

# Slack Configuration
SLACK_BOT_TOKEN = settings.slack_bot_token
SLACK_CHANNEL = settings.slack_channel

# Email Configuration
SMTP_SERVER = settings.email_host
SMTP_PORT = settings.email_port
EMAIL_SENDER = settings.email_sender
EMAIL_USERNAME = settings.email_username
EMAIL_PASSWORD = settings.email_password
EMAIL_RECEIVER = settings.email_receiver

# In-memory store
alerts = []

def send_email_alert(subject: str, message: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print(f" Email sent: {subject}")
    except Exception as e:
        print(f" Email send failed: {e}")

def send_slack_alert(message: str):
    try:
        client = WebClient(token=SLACK_BOT_TOKEN)
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        if not response["ok"]:
            print(f" Slack API error: {response['error']}")
        else:
            print(" Slack alert sent.")
    except SlackApiError as e:
        print(f" Slack exception: {e.response['error']}")

@router.post("/")
async def trigger_alert(
    level: str = Body(..., embed=True),
    message: str = Body(..., embed=True),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Trigger alerts and send via Email, Slack, and WebSocket manager."""
    allowed_levels = ["ALERT","ERROR", "WARNING", "CRITICAL"]
    level_upper = level.upper()

    if level_upper not in allowed_levels:
        raise HTTPException(status_code=400, detail=f"Allowed levels: {allowed_levels}")

    timestamp = datetime.utcnow().isoformat()
    formatted = f" *{level_upper}* Alert: {message}"

    alert_data = {
        "type": "alert",
        "severity": level_upper,
        "message": message,
        "timestamp": timestamp,
    }

    alerts.append(alert_data)

    # Background Slack + Email
    subject = f"{level_upper} Alert - {message}"
    background_tasks.add_task(send_email_alert, subject, formatted)
    background_tasks.add_task(send_slack_alert, formatted)

    #  Broadcast to all WebSocket clients using manager
    asyncio.create_task(manager.broadcast_json(alert_data))

    return {"status": " Alert sent", "alert": alert_data}

@router.get("/")
def get_alerts():
    """Return list of alerts as JSON array"""
    return alerts  #  FIXED: frontend expects a list, not a dict



# app/services/alert_service.py
from app.email_alerts import send_email_alert
from app.schemas import AlertRequest

def process_alert(alert: AlertRequest):
    """
    Process an alert and trigger an email notification if conditions are met.
    """
    if alert.severity.lower() == "critical":
        send_email_alert(log_message=alert.message, severity=alert.severity)
    return {"message": "Alert processed"}

#backend/app/email_alerts.py
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)

def send_email_alert(log_message: str, severity: str):
    """
    Sends an email alert for log monitoring.
    """
    subject = f" Log Alert: {severity.upper()}"
    body = f"A new log entry requires attention:\n\n🔹 Severity: {severity}\n🔹 Message: {log_message}"

    sender_email = settings.email_username
    receiver_email = settings.email_username  # You can change this to a different recipient
    smtp_server = settings.email_host
    smtp_port = settings.email_port
    smtp_user = settings.email_username
    smtp_pass = settings.email_password

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        logging.info(f" Email alert sent successfully to {receiver_email}")

    except Exception as e:
        logging.error(f" Failed to send email alert: {e}")

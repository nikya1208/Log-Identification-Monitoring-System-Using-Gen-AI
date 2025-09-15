# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\utils\smtp_server.py

# import smtplib
# from email.message import EmailMessage
# import requests
# from app.config import settings


# def send_email_alert(subject: str, body: str):
#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = settings.email_sender
#     msg["To"] = settings.email_receiver
#     msg.set_content(body)

#     print(" Preparing to send email alert...")
#     print(f" From: {settings.email_sender}")
#     print(f" To: {settings.email_receiver}")
#     print(f" Subject: {subject}")

#     try:
#         with smtplib.SMTP(settings.email_host, settings.email_port) as server:
#             server.set_debuglevel(1)  # 🔍 Enable SMTP debug output
#             server.starttls()  # Secure connection
#             server.login(settings.email_username, settings.email_password)

#             #  Check if sender is same as authenticated user
#             if settings.email_username != settings.email_sender:
#                 print(" Warning: Gmail may block sending from a different 'From' address.")
#                 print(" Use the same value for EMAIL_USERNAME and EMAIL_SENDER in your .env")

#             server.send_message(msg)
#         print(" Email sent successfully.")
#     except smtplib.SMTPAuthenticationError as e:
#         print(" SMTP Authentication failed. Double-check Gmail App Password and username.")
#         print(e)
#     except Exception as e:
#         print(f" Email Error: {e}")


# def send_slack_alert(message: str):
#     slack_url = "https://slack.com/api/chat.postMessage"
#     headers = {"Authorization": f"Bearer {settings.slack_bot_token}"}
#     payload = {
#         "channel": settings.slack_channel,
#         "text": message
#     }

#     response = requests.post(slack_url, json=payload, headers=headers)
#     if response.status_code != 200 or not response.json().get("ok"):
#         print(" Slack API Error:", response.json())
#     else:
#         print(" Slack message sent.")



# app/utils/smtp_server.py

import smtplib
from email.message import EmailMessage
import requests
import logging
from app.config import settings

def send_email_alert(subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.email_sender
    msg["To"] = settings.email_receiver
    msg.set_content(body)

    logging.info("Preparing to send email alert...")
    logging.info(f"From: {settings.email_sender}")
    logging.info(f"To: {settings.email_receiver}")
    logging.info(f"Subject: {subject}")

    try:
        with smtplib.SMTP(settings.email_host, settings.email_port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(settings.email_username, settings.email_password)

            if settings.email_username != settings.email_sender:
                logging.warning("Gmail may block sending if 'From' and login emails differ.")

            server.send_message(msg)
            logging.info("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        logging.error("SMTP Authentication failed. Check App Password and email username.")
        logging.error(e)
    except smtplib.SMTPException as e:
        logging.error("SMTP Exception occurred.")
        logging.error(e)
    except Exception as e:
        logging.error(f"Email sending error: {e}")

def send_slack_alert(message: str):
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {settings.slack_bot_token}"}
    payload = {
        "channel": settings.slack_channel,
        "text": message
    }

    try:
        response = requests.post(slack_url, json=payload, headers=headers)
        if response.status_code != 200 or not response.json().get("ok"):
            logging.error("Slack API Error: %s", response.json())
        else:
            logging.info("Slack message sent.")
    except Exception as e:
        logging.error("Slack alert sending failed: %s", str(e))

# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\email_test.py

import smtplib
from email.message import EmailMessage

EMAIL_USERNAME = "shindenikhil1208@gmail.com"
EMAIL_PASSWORD = "mmzekrelfbhbhxzp"  # ✅ App Password (16-char, no spaces)
EMAIL_RECEIVER = "santoshshinde1921@gmail.com"

msg = EmailMessage()
msg["Subject"] = "✅ FastAPI Gmail Test"
msg["From"] = EMAIL_USERNAME
msg["To"] = EMAIL_RECEIVER
msg.set_content("This is a test email sent using raw smtplib.")

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.set_debuglevel(1)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Error sending email:", e)

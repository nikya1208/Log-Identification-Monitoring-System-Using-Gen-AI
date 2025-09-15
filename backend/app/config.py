# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\config.py

# from pydantic_settings import BaseSettings
# from pydantic import ConfigDict
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# class Settings(BaseSettings):
#     database_url: str = os.getenv("DATABASE_URL", "")
#     secret_key: str = os.getenv("SECRET_KEY", "")
#     email_host: str = os.getenv("EMAIL_HOST", "")
#     email_port: int = int(os.getenv("EMAIL_PORT", 587))  # Ensure port is an integer
#     email_username: str = os.getenv("EMAIL_USERNAME", "")
#     email_password: str = os.getenv("EMAIL_PASSWORD", "")
    
#     #  Added Missing Email Sender & Receiver
#     email_sender: str = os.getenv("EMAIL_SENDER", "")
#     email_receiver: str = os.getenv("EMAIL_RECEIVER", "")

#     #  Add Slack Bot Token
#     slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN", "")

#     #  Add Slack Channel
#     slack_channel: str = os.getenv("SLACK_CHANNEL", "")

#     #  Only use model_config for Pydantic v2
#     model_config = ConfigDict(
#         extra="allow",              # Allows extra fields
#         env_file=".env",            # Automatically loads from .env file
#         env_file_encoding="utf-8"   # Encoding type
#     )

# # Create settings instance
# settings = Settings()

# #  Debugging messages to confirm loaded settings
# print(f" Database URL: {settings.database_url}")
# print(f" Email Host: {settings.email_host}")
# print(f" Email Sender: {settings.email_sender or ' Not Found!'}")
# print(f" Email Receiver: {settings.email_receiver or ' Not Found!'}")
# print(f" Slack Bot Token: {'Loaded' if settings.slack_bot_token else ' Not Found!'}")
# print(f" Slack Channel: {'Loaded' if settings.slack_channel else ' Not Found!'}")


# backend/app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    email_host: str
    email_port: int = 587
    email_username: str
    email_password: str
    email_sender: str
    email_receiver: str
    slack_bot_token: str
    slack_channel: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )


# Create settings instance
settings = Settings()

# Debug prints (optional)
print(f"Database URL: {settings.database_url}")
print(f"Email Host: {settings.email_host}")
print(f"Email Sender: {settings.email_sender or 'Not Found!'}")
print(f"Email Receiver: {settings.email_receiver or 'Not Found!'}")
print(f"Slack Bot Token: {'Loaded' if settings.slack_bot_token else 'Not Found!'}")
print(f"Slack Channel: {'Loaded' if settings.slack_channel else 'Not Found!'}")

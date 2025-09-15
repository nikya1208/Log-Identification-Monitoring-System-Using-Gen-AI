


# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use DATABASE_URL from config.py
DATABASE_URL = settings.database_url

if not DATABASE_URL:
    logger.error("DATABASE_URL is not set in the environment variables!")
    raise ValueError("DATABASE_URL is missing!")

# Create the database engine with connection pooling
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# Session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for SQLAlchemy
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Debugging message to confirm the database engine is initialized
logger.info("Database engine initialized successfully!")

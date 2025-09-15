# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\tests\test_api.py

import sys
import os

# Ensure the `app` module is found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

test_client = TestClient(app)

def test_root():
    """Test the root (/) endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200

    expected_keys = {"message", "database_url", "email_host"}
    response_json = response.json()
    
    assert isinstance(response_json, dict)
    assert expected_keys.issubset(response_json.keys())

def test_get_logs():
    """Test retrieving all logs."""
    response = test_client.get("/logs/")
    assert response.status_code == 200

    logs = response.json()
    assert isinstance(logs, list)
    assert all("timestamp" in log and "level" in log and "message" in log for log in logs)

def test_get_logs_filtered():
    """Test retrieving logs with filtering by level and source."""
    response = test_client.get("/logs/?level=ERROR&source=backend")
    assert response.status_code == 200

    logs = response.json()
    assert isinstance(logs, list)

    # Ensure only logs matching the filter exist
    assert all(log["level"] == "ERROR" and log["source"] == "backend" for log in logs)

def test_get_logs_keyword_search():
    """Test retrieving logs using keyword search."""
    response = test_client.get("/logs/?keyword=memory")
    assert response.status_code == 200

    logs = response.json()
    assert isinstance(logs, list)
    
    # Ensure only logs containing the keyword are returned
    assert all("memory" in log["message"].lower() for log in logs)

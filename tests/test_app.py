import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test root redirect

def test_root_redirect():
    # Arrange
    # TestClient is already set up
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307
    assert "Mergington High School" in response.text or response.is_redirect

# Test activities listing

def test_get_activities():
    # Arrange
    # TestClient is already set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()

# Test signup for activity

def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200 or response.status_code == 201 or response.status_code == 204
    # Optionally check participant added
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]

# Test signup for invalid activity

def test_signup_for_activity_invalid():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404

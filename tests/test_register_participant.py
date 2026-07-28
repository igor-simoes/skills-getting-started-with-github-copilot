from pathlib import Path
import sys
from fastapi.testclient import TestClient
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


client = TestClient(app)


def test_signup_success():
    """Should successfully sign up a student for an existing activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@email.com"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Signed up newstudent@email.com for Chess Club"}
    
    # Check if the email was actually added to the data structure
    assert "newstudent@email.com" in activities["Chess Club"]["participants"]


def test_signup_activity_not_found():
    """Should return a 404 error when the activity does not exist."""
    response = client.post(
        "/activities/Basketball/signup",
        params={"email": "student@email.com"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_registered():
    """Should return a 400 error if the student is already signed up for the activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@email.com"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_missing_email_parameter():
    """Should return a 422 validation error if the email query parameter is missing."""
    response = client.post("/activities/Chess Club/signup")
    
    assert response.status_code == 422
    
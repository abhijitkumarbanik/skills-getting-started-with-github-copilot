from fastapi.testclient import TestClient
import pytest

def test_get_activities(client: TestClient):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

def test_signup_for_activity(client: TestClient):
    """Test signing up for an activity"""
    email = "test@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Verify the participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate(client: TestClient):
    """Test signing up when already registered"""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client: TestClient):
    """Test signing up for non-existent activity"""
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_from_activity(client: TestClient):
    """Test unregistering from an activity"""
    email = "michael@mergington.edu"  # Existing participant in Chess Club
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Verify the participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_unregister_nonexistent_participant(client: TestClient):
    """Test unregistering a non-existent participant"""
    response = client.post("/activities/Chess Club/unregister?email=nonexistent@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
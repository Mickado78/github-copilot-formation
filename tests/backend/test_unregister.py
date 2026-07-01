from urllib.parse import quote

from src.app import activities


def test_unregister_participant_from_activity_success(client):
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{quote('Chess Club')}/participants/{quote(email)}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_participant_unknown_activity_returns_404(client):
    response = client.delete(
        f"/activities/{quote('Unknown Club')}/participants/{quote('student@mergington.edu')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_missing_returns_404(client):
    response = client.delete(
        f"/activities/{quote('Chess Club')}/participants/{quote('not-enrolled@mergington.edu')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"

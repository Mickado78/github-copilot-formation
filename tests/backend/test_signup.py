from urllib.parse import quote

from src.app import activities


def test_signup_for_activity_success(client):
    email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{quote('Chess Club')}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_activity_unknown_activity_returns_404(client):
    response = client.post(
        f"/activities/{quote('Unknown Club')}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_duplicate_email_returns_400(client):
    existing_email = activities["Chess Club"]["participants"][0]

    response = client.post(
        f"/activities/{quote('Chess Club')}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_activity_name_supports_url_encoding(client):
    email = "encoded.student@mergington.edu"

    response = client.post(
        f"/activities/{quote('Programming Class')}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in activities["Programming Class"]["participants"]

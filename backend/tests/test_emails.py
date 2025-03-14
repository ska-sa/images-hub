"""This file is responsible for testing the emails enpoint using pytest"""
import os
from dotenv import load_dotenv
from main import app

URL = "http://localhost:5000/api/v1/emails"
load_dotenv()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

def test_send_email() -> None:
    """This function tests the functionality of POST emails endpoint"""
    email_data = {
        "receiver_email_address": "shlabisa@sarao.ac.za",
        "subject": "Send Email Test",
        "body": "This is a test email from the Images Hub Team"
    }

    with app.test_client() as client:
        response = client.post(URL, headers=headers, json=email_data)
        email_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(email_dict, dict)
        assert "message" in email_dict
        assert email_dict["message"] == "Email sent successfully!"

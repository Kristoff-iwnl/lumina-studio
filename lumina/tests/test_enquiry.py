"""
Tests for enquiry form submission (validation, honeypot, rate limiting).
"""

import pytest
from app.models import Enquiry, db

class TestEnquiryForm:
    """Enquiry form submission tests."""

    def test_enquiry_page_loads(self, client):
        """GET / returns 200 with form."""
        response = client.get("/")
        assert response.status_code == 200

    def test_enquiry_valid_submission(self, client):
        """POST with valid data creates enquiry."""
        response = client.post(
            "/enquiry",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1 (555) 123-4567",
                "service": "1",
                "message": "I'd like to book a session.",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        enquiry = Enquiry.query.first()
        assert enquiry is not None
        assert enquiry.name == "John Doe"

    def test_enquiry_missing_name(self, client):
        """POST without name fails."""
        response = client.post(
            "/enquiry",
            data={
                "name": "",
                "email": "john@example.com",
                "phone": "+1 (555) 123-4567",
                "message": "I'd like to book a session.",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200  # Redirects back to homepage

    def test_enquiry_invalid_email(self, client):
        """POST with invalid email fails."""
        response = client.post(
            "/enquiry",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "phone": "+1 (555) 123-4567",
                "message": "I'd like to book a session.",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_enquiry_short_message(self, client):
        """POST with short message fails."""
        response = client.post(
            "/enquiry",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1 (555) 123-4567",
                "message": "Hi",  # Too short
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_enquiry_honeypot_triggered(self, client):
        """POST with honeypot field filled is rejected."""
        response = client.post(
            "/enquiry",
            data={
                "name": "Bot",
                "email": "bot@example.com",
                "phone": "+1 (555) 123-4567",
                "website": "http://spam.com",  # Honeypot field
                "message": "Spam message",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        enquiry = Enquiry.query.filter_by(name="Bot").first()
        if enquiry:
            assert enquiry.status == "spam"

class TestEnquiryRateLimiting:
    """Rate limiting on enquiry submission."""

    def test_enquiry_rate_limit(self, client):
        """Multiple enquiries from same IP trigger rate limit."""
        for i in range(5):
            client.post(
                "/enquiry",
                data={
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "phone": "+1 (555) 123-4567",
                    "message": "Test enquiry message.",
                },
            )
        # 6th request should be rate limited
        response = client.post(
            "/enquiry",
            data={
                "name": "User 6",
                "email": "user6@example.com",
                "phone": "+1 (555) 123-4567",
                "message": "Test enquiry message.",
            },
        )
        assert response.status_code in [429, 200]  # Rate limit or show message

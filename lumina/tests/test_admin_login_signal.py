"""
Tests for Companion Brief 4: Signal Admin Login Variant.
"""

import pytest

class TestAdminLoginSignal:
    """Test suite for Signal admin login variant."""

    def test_signal_login_page_loads(self, client):
        """Verify /auth/login?variant=signal loads successfully with 200 OK."""
        response = client.get("/auth/login?variant=signal")
        assert response.status_code == 200
        html = response.data.decode("utf-8")

        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'login.css' in html
        assert 'entry-guard.js' in html
        assert 'video-guard.js' in html

    def test_signal_login_success(self, client, admin_user):
        """Verify successful login with valid credentials using signal variant."""
        # Get signal login page first to get CSRF token
        client.get("/auth/login?variant=signal")

        response = client.post(
            "/auth/login?variant=signal",
            data={
                "email": "admin@lumina.com",
                "password": "Admin123"
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Dashboard" in response.data or b"Admin" in response.data

    def test_signal_login_wrong_password(self, client):
        """Verify invalid password returns generic error message."""
        client.get("/auth/login?variant=signal")

        response = client.post(
            "/auth/login?variant=signal",
            data={
                "email": "admin@lumina.com",
                "password": "WrongPassword123"
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Incorrect username or password" in response.data

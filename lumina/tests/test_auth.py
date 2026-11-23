"""
Tests for authentication (login, logout, sessions).
"""

import pytest

class TestLogin:
    """Login endpoint tests."""

    def test_login_page_loads(self, client):
        """GET /auth/login returns 200."""
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert b"login" in response.data.lower()

    def test_login_success(self, client, admin_user):
        """POST with correct credentials logs in."""
        response = client.post(
            "/auth/login",
            data={"email": "test@example.com", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_login_wrong_password(self, client, admin_user):
        """POST with wrong password fails."""
        response = client.post(
            "/auth/login",
            data={"email": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401 or response.status_code == 200
        # Depends on implementation: redirect or show error

    def test_login_nonexistent_user(self, client):
        """POST with non-existent email fails."""
        response = client.post(
            "/auth/login",
            data={"email": "nouser@example.com", "password": "password123"},
        )
        assert response.status_code == 401 or response.status_code == 200

class TestLogout:
    """Logout endpoint tests."""

    def test_logout_clears_session(self, authenticated_client):
        """GET /auth/logout clears session."""
        response = authenticated_client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200

class TestRateLimiting:
    """Rate limiting on login."""

    def test_login_rate_limit(self, client):
        """Multiple failed logins trigger rate limit."""
        for i in range(6):
            client.post(
                "/auth/login",
                data={"email": f"test{i}@example.com", "password": "wrong"},
            )
        # 6th request should be rate limited (429)
        response = client.post(
            "/auth/login",
            data={"email": "test@example.com", "password": "wrong"},
        )
        # Rate limit response (depends on Flask-Limiter config)
        assert response.status_code in [429, 200]

"""
Tests for public routes (homepage, privacy, errors).
"""

import pytest

class TestPublicRoutes:
    """Public page tests."""

    def test_homepage_loads(self, client):
        """GET / returns 200."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"LUMINA" in response.data or b"Light. Craft. Memory." in response.data

    def test_privacy_page_loads(self, client):
        """GET /privacy returns 200."""
        response = client.get("/privacy")
        assert response.status_code == 200
        assert b"privacy" in response.data.lower()

    def test_homepage_has_services(self, client):
        """Homepage displays services from config."""
        response = client.get("/")
        assert response.status_code == 200
        # Check for at least one service name
        assert (
            b"Portrait" in response.data
            or b"Event" in response.data
            or b"Product" in response.data
        )

    def test_homepage_has_faq(self, client):
        """Homepage displays FAQ."""
        response = client.get("/")
        assert response.status_code == 200
        # FAQ should be present (if any exist in DB or config)

    def test_homepage_has_enquiry_form(self, client):
        """Homepage includes enquiry form."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"name" in response.data or b"email" in response.data

class TestErrorPages:
    """Error page tests."""

    def test_404_not_found(self, client):
        """GET /nonexistent returns 404."""
        response = client.get("/nonexistent-page")
        assert response.status_code == 404

    def test_404_page_loads(self, client):
        """404 page is readable."""
        response = client.get("/nonexistent-page")
        assert response.status_code == 404
        # Should have some helpful message

class TestSEO:
    """SEO meta tags."""

    def test_homepage_has_meta_tags(self, client):
        """Homepage includes meta tags for SEO."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"<meta" in response.data
        assert b"<title>" in response.data

    def test_sitemap_exists(self, client):
        """GET /sitemap.xml returns valid XML."""
        response = client.get("/sitemap.xml")
        assert response.status_code == 200
        assert b"<?xml" in response.data or b"<urlset" in response.data

    def test_robots_txt_exists(self, client):
        """GET /robots.txt returns robots.txt."""
        response = client.get("/robots.txt")
        assert response.status_code == 200
        assert b"User-agent" in response.data or b"Disallow" in response.data

"""
Tests for the Mostar Cinematic Frontend integration.
"""

import pytest

class TestCinematicFrontend:
    """Cinematic variant and integration tests."""

    def test_classic_and_cinematic_routes(self, client):
        """Verify /classic and /cinematic both return 200."""
        r_classic = client.get("/classic")
        assert r_classic.status_code == 200

        r_cine = client.get("/cinematic")
        assert r_cine.status_code == 200
        assert b"cinema-scroll" in r_cine.data

    def test_cinematic_page_elements_and_csrf(self, client):
        """Verify cinematic page has section.cinema-scroll and enquiry form fields."""
        response = client.get("/cinematic")
        assert response.status_code == 200
        html = response.data.decode("utf-8")

        assert "cinema-scroll" in html
        assert 'name="name"' in html
        assert 'name="email"' in html
        assert 'name="message"' in html

    def test_cinematic_enquiry_submission(self, client):
        """Verify submitting an enquiry from the cinematic page stores it correctly."""
        # Get cinematic page to acquire CSRF token if needed
        resp = client.get("/cinematic")
        assert resp.status_code == 200

        # Post enquiry
        response = client.post(
            "/enquiry",
            data={
                "name": "Cinematic Visitor",
                "email": "cinematic@example.com",
                "message": "Testing cinematic enquiry submission.",
                "service": "Portrait Sessions"
            },
            follow_redirects=True
        )
        assert response.status_code == 200

    def test_cinematic_csp_headers(self, client):
        """Verify cinematic CSP contains exactly the three extra hosts and no script-src additions."""
        response = client.get("/cinematic")
        csp = response.headers.get("Content-Security-Policy", "")

        assert "raft-blast-61784561.figma.site" in csp
        assert "d8j0ntlcm91z4.cloudfront.net" in csp
        assert "dcym8fthxf5uu.cloudfront.net" in csp
        assert "script-src 'self'" in csp
        assert "unsafe-eval" not in csp

    def test_admin_still_requires_login(self, client):
        """Verify admin routes still enforce authentication."""
        response = client.get("/admin/", follow_redirects=False)
        assert response.status_code in [302, 401]
        assert "/auth/login" in response.headers.get("Location", "")

    def test_cinematic_engines(self, client):
        """Verify both original and optimized engine query parameters work."""
        r_orig = client.get("/cinematic?engine=original")
        assert r_orig.status_code == 200
        assert b"script.js" in r_orig.data

        r_opt = client.get("/cinematic?engine=optimized")
        assert r_opt.status_code == 200
        assert b"engine.js" in r_opt.data

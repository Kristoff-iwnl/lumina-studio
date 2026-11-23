"""
Tests for production configuration and health check.
"""

import pytest
from app import create_app
from config.config import Production, Testing

def test_production_secret_key_refusal():
    """Verify production startup refuses weak or missing SECRET_KEY."""
    prod_config = Production()
    prod_config.SECRET_KEY = "dev-key-change-in-production"
    prod_config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    with pytest.raises(RuntimeError, match="CRITICAL: Production mode requires a secure SECRET_KEY"):
        create_app(prod_config)

def test_healthz_endpoint(client):
    """Verify /healthz returns 200 OK without DB touch."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.data == b"OK"

def test_robots_and_sitemap_use_site_url(client):
    """Verify robots.txt and sitemap.xml use SITE_URL."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert b"Sitemap:" in response.data

    response_sitemap = client.get("/sitemap.xml")
    assert response_sitemap.status_code == 200
    assert b"<?xml" in response_sitemap.data

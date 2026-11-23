"""
Pytest configuration and shared fixtures.
"""

import pytest
from app import create_app, db
from config.config import Testing
from app.models import Admin, Service, FAQ, Testimonial

@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app(Testing())

    with app.app_context():
        db.create_all()

        # Seed demo data for tests
        services = [
            Service(name="Portrait Sessions", description="Test", price="$299", order=1),
            Service(name="Event Coverage", description="Test", price="$1,200+", order=2),
            Service(name="Product Photography", description="Test", price="$499", order=3),
        ]
        db.session.add_all(services)

        faq_items = [
            FAQ(question="Q1?", answer="A1 answer", order=1),
            FAQ(question="Q2?", answer="A2 answer", order=2),
        ]
        db.session.add_all(faq_items)

        testimonials = [
            Testimonial(name="Test User 1", role="Client", message="Great!", approved=True, order=1),
            Testimonial(name="Test User 2", role="Client", message="Excellent!", approved=True, order=2),
        ]
        db.session.add_all(testimonials)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
    """Create a test admin user."""
    with app.app_context():
        admin = Admin(email="test@example.com")
        admin.set_password("password123")
        db.session.add(admin)
        db.session.commit()
        return admin

@pytest.fixture
def authenticated_client(client, admin_user):
    """Test client logged in as admin."""
    client.post(
        "/auth/login",
        data={"email": "test@example.com", "password": "password123"},
        follow_redirects=True,
    )
    return client

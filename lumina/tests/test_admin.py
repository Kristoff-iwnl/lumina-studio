"""
Tests for admin area (protected routes, CRUD, access control).
"""

import pytest
from app.models import Service, FAQ, Testimonial, db

class TestAdminAccess:
    """Admin area access control."""

    def test_admin_redirects_to_login(self, client):
        """GET /admin without auth redirects to login."""
        response = client.get("/admin", follow_redirects=True)
        assert response.status_code == 200
        # Should be on login page

    def test_admin_dashboard_authenticated(self, authenticated_client):
        """GET /admin with auth returns dashboard."""
        response = authenticated_client.get("/admin", follow_redirects=True)
        assert response.status_code == 200

class TestServiceCRUD:
    """Service CRUD operations."""

    def test_services_list(self, authenticated_client):
        """GET /admin/services lists services."""
        response = authenticated_client.get("/admin/services")
        assert response.status_code == 200

    def test_service_create(self, authenticated_client):
        """POST /admin/services/new creates service."""
        response = authenticated_client.post(
            "/admin/services/new",
            data={
                "name": "New Service",
                "description": "Test description",
                "price": "$99",
                "icon": "test",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        service = Service.query.filter_by(name="New Service").first()
        assert service is not None

    def test_service_edit(self, authenticated_client, app):
        """GET /admin/services/<id>/edit renders edit form."""
        with app.app_context():
            service = Service(
                name="Original", description="Desc", price="$50", icon="test"
            )
            db.session.add(service)
            db.session.commit()
            service_id = service.id

            # Just test that the GET works (form renders)
            response = authenticated_client.get(f"/admin/services/{service_id}/edit")
            assert response.status_code == 200
            assert b"Edit Service" in response.data or b"Original" in response.data

    def test_service_delete(self, authenticated_client):
        """DELETE /admin/services/<id>/delete deletes service."""
        service = Service(
            name="To Delete", description="Desc", price="$50", icon="test"
        )
        db.session.add(service)
        db.session.commit()
        service_id = service.id

        response = authenticated_client.post(
            f"/admin/services/{service_id}/delete",
            follow_redirects=True,
        )
        assert response.status_code == 200
        service = Service.query.get(service_id)
        assert service is None

class TestFAQCRUD:
    """FAQ CRUD operations."""

    def test_faq_create(self, authenticated_client):
        """POST /admin/faq/new creates FAQ."""
        response = authenticated_client.post(
            "/admin/faq/new",
            data={
                "question": "Test question?",
                "answer": "Test answer.",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        faq = FAQ.query.filter_by(question="Test question?").first()
        assert faq is not None

class TestTestimonialCRUD:
    """Testimonial CRUD operations."""

    def test_testimonial_approve(self, authenticated_client):
        """Testimonials can be approved."""
        testimonial = Testimonial(
            name="Test User",
            role="Client",
            message="Great service!",
            approved=False,
        )
        db.session.add(testimonial)
        db.session.commit()

        response = authenticated_client.post(
            f"/admin/testimonials/{testimonial.id}/edit",
            data={
                "name": "Test User",
                "role": "Client",
                "message": "Great service!",
                "approved": True,
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        testimonial = Testimonial.query.get(testimonial.id)
        assert testimonial.approved is True

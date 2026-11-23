"""
Admin routes: dashboard, enquiry management, CRUD for content.
"""

import csv
from io import StringIO
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from app.models import db, Enquiry, Service, FAQ, Testimonial
from app.forms import ServiceForm, FAQForm, TestimonialForm

admin_bp = Blueprint("admin", __name__)

# Require login for all admin routes
@admin_bp.before_request
@login_required
def before_request():
    """Ensure user is logged in."""
    pass

@admin_bp.route("/")
def dashboard():
    """Admin dashboard overview."""
    enquiry_counts = {
        "new": Enquiry.query.filter_by(status="new").count(),
        "contacted": Enquiry.query.filter_by(status="contacted").count(),
        "done": Enquiry.query.filter_by(status="done").count(),
        "spam": Enquiry.query.filter_by(status="spam").count(),
    }
    recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(5).all()

    return render_template("admin/dashboard.html", enquiry_counts=enquiry_counts, recent_enquiries=recent_enquiries)

# ============================================
# ENQUIRY MANAGEMENT
# ============================================

@admin_bp.route("/enquiries")
def enquiries_list():
    """List all enquiries with search and filter."""
    status = request.args.get("status", "")
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Enquiry.query

    if status and status in ["new", "contacted", "done", "spam"]:
        query = query.filter_by(status=status)

    if search:
        query = query.filter(
            (Enquiry.name.ilike(f"%{search}%")) |
            (Enquiry.email.ilike(f"%{search}%")) |
            (Enquiry.phone.ilike(f"%{search}%"))
        )

    enquiries = query.order_by(Enquiry.created_at.desc()).paginate(page=page, per_page=20)

    return render_template("admin/enquiries.html", enquiries=enquiries, status=status, search=search)

@admin_bp.route("/enquiries/<int:enquiry_id>")
def view_enquiry(enquiry_id):
    """View enquiry detail."""
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    return render_template("admin/enquiry_detail.html", enquiry=enquiry)

@admin_bp.route("/enquiries/<int:enquiry_id>/status", methods=["POST"])
def update_enquiry_status(enquiry_id):
    """Update enquiry status."""
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    new_status = request.form.get("status")

    if new_status in ["new", "contacted", "done", "spam"]:
        enquiry.status = new_status
        db.session.commit()
        flash(f"Enquiry marked as {new_status}.", "success")
    else:
        flash("Invalid status.", "error")

    return redirect(url_for("admin.view_enquiry", enquiry_id=enquiry_id))

@admin_bp.route("/enquiries/<int:enquiry_id>/delete", methods=["POST"])
def delete_enquiry(enquiry_id):
    """Delete enquiry."""
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    db.session.delete(enquiry)
    db.session.commit()
    flash("Enquiry deleted.", "success")
    return redirect(url_for("admin.enquiries_list"))

# ============================================
# SERVICES CRUD
# ============================================

@admin_bp.route("/services")
def services_list():
    """List all services."""
    services = Service.query.order_by(Service.order).all()
    return render_template("admin/services.html", services=services)

@admin_bp.route("/services/new", methods=["GET", "POST"])
def create_service():
    """Create new service."""
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            icon=form.icon.data,
        )
        db.session.add(service)
        db.session.commit()
        flash("Service created.", "success")
        return redirect(url_for("admin.services_list"))

    return render_template("admin/service_form.html", form=form, title="New Service")

@admin_bp.route("/services/<int:service_id>/edit", methods=["GET", "POST"])
def edit_service(service_id):
    """Edit service."""
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()

    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        service.price = form.price.data
        service.icon = form.icon.data
        db.session.commit()
        flash("Service updated.", "success")
        return redirect(url_for("admin.services_list"))

    elif request.method == "GET":
        form.name.data = service.name
        form.description.data = service.description
        form.price.data = service.price
        form.icon.data = service.icon

    return render_template("admin/service_form.html", form=form, service=service, title="Edit Service")

@admin_bp.route("/services/<int:service_id>/delete", methods=["POST"])
def delete_service(service_id):
    """Delete service."""
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted.", "success")
    return redirect(url_for("admin.services_list"))

# ============================================
# FAQ CRUD
# ============================================

@admin_bp.route("/faq")
def faq_list():
    """List all FAQs."""
    faq_items = FAQ.query.order_by(FAQ.order).all()
    return render_template("admin/faq.html", faq_items=faq_items)

@admin_bp.route("/faq/new", methods=["GET", "POST"])
def create_faq():
    """Create new FAQ."""
    form = FAQForm()
    if form.validate_on_submit():
        faq = FAQ(question=form.question.data, answer=form.answer.data)
        db.session.add(faq)
        db.session.commit()
        flash("FAQ created.", "success")
        return redirect(url_for("admin.faq_list"))

    return render_template("admin/faq_form.html", form=form, title="New FAQ")

@admin_bp.route("/faq/<int:faq_id>/edit", methods=["GET", "POST"])
def edit_faq(faq_id):
    """Edit FAQ."""
    faq = FAQ.query.get_or_404(faq_id)
    form = FAQForm()

    if form.validate_on_submit():
        faq.question = form.question.data
        faq.answer = form.answer.data
        db.session.commit()
        flash("FAQ updated.", "success")
        return redirect(url_for("admin.faq_list"))

    elif request.method == "GET":
        form.question.data = faq.question
        form.answer.data = faq.answer

    return render_template("admin/faq_form.html", form=form, faq=faq, title="Edit FAQ")

@admin_bp.route("/faq/<int:faq_id>/delete", methods=["POST"])
def delete_faq(faq_id):
    """Delete FAQ."""
    faq = FAQ.query.get_or_404(faq_id)
    db.session.delete(faq)
    db.session.commit()
    flash("FAQ deleted.", "success")
    return redirect(url_for("admin.faq_list"))

# ============================================
# TESTIMONIALS CRUD
# ============================================

@admin_bp.route("/testimonials")
def testimonials_list():
    """List all testimonials."""
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template("admin/testimonials.html", testimonials=testimonials)

@admin_bp.route("/testimonials/new", methods=["GET", "POST"])
def create_testimonial():
    """Create new testimonial."""
    form = TestimonialForm()
    if form.validate_on_submit():
        testimonial = Testimonial(
            name=form.name.data,
            role=form.role.data,
            message=form.message.data,
            approved=form.approved.data,
        )
        db.session.add(testimonial)
        db.session.commit()
        flash("Testimonial created.", "success")
        return redirect(url_for("admin.testimonials_list"))

    return render_template("admin/testimonial_form.html", form=form, title="New Testimonial")

@admin_bp.route("/testimonials/<int:testimonial_id>/edit", methods=["GET", "POST"])
def edit_testimonial(testimonial_id):
    """Edit testimonial."""
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    form = TestimonialForm()

    if form.validate_on_submit():
        testimonial.name = form.name.data
        testimonial.role = form.role.data
        testimonial.message = form.message.data
        testimonial.approved = form.approved.data
        db.session.commit()
        flash("Testimonial updated.", "success")
        return redirect(url_for("admin.testimonials_list"))

    elif request.method == "GET":
        form.name.data = testimonial.name
        form.role.data = testimonial.role
        form.message.data = testimonial.message
        form.approved.data = testimonial.approved

    return render_template("admin/testimonial_form.html", form=form, testimonial=testimonial, title="Edit Testimonial")

@admin_bp.route("/testimonials/<int:testimonial_id>/delete", methods=["POST"])
def delete_testimonial(testimonial_id):
    """Delete testimonial."""
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    db.session.delete(testimonial)
    db.session.commit()
    flash("Testimonial deleted.", "success")
    return redirect(url_for("admin.testimonials_list"))

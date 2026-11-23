"""
Public routes: homepage, enquiry form, privacy, errors.
"""

import json
import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_limiter.util import get_remote_address
from app import limiter
from app.models import db, Enquiry, Service, FAQ, Testimonial
from app.forms import EnquiryForm

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    """Homepage (serves cinematic by default)."""
    return cinematic()

@public_bp.route("/classic")
def classic():
    """Classic variant."""
    services = Service.query.order_by(Service.order).all()
    faqs = FAQ.query.order_by(FAQ.order).all()
    testimonials = Testimonial.query.filter_by(approved=True).order_by(Testimonial.order).all()

    form = EnquiryForm()

    return render_template(
        "index.html",
        services=services,
        faqs=faqs,
        testimonials=testimonials,
        form=form,
        now=datetime.utcnow(),
    )

@public_bp.route("/cinematic")
def cinematic():
    """Cinematic Mostar variant."""
    services = Service.query.order_by(Service.order).all()
    faqs = FAQ.query.order_by(FAQ.order).all()
    testimonials = Testimonial.query.filter_by(approved=True).order_by(Testimonial.order).all()

    form = EnquiryForm()
    engine = request.args.get("engine", os.environ.get("CINEMATIC_ENGINE", "original")).lower()

    return render_template(
        "cinematic/index.html",
        services=services,
        faqs=faqs,
        testimonials=testimonials,
        form=form,
        now=datetime.utcnow(),
        engine=engine,
    )

@public_bp.route("/enquiry", methods=["POST"])
@limiter.limit("5 per hour")
def submit_enquiry():
    """Handle enquiry form submission with honeypot and time-trap."""
    form = EnquiryForm()

    # Honeypot: hidden field that should be empty
    honeypot = request.form.get("website", "").strip()
    if honeypot:
        # Silently reject bot submission
        enquiry = Enquiry(
            name=form.name.data or "Bot",
            email=form.email.data or "",
            phone=form.phone.data or "",
            message=form.message.data or "Honeypot triggered",
            status="spam",
        )
        db.session.add(enquiry)
        db.session.commit()
        flash("Thank you. We'll be in touch soon.", "success")
        return redirect(url_for("public.index"))

    # Time-trap: form must be submitted within 2 hours
    form_timestamp = request.form.get("timestamp", "")
    if form_timestamp:
        try:
            form_time = datetime.fromisoformat(form_timestamp)
            if datetime.utcnow() - form_time > timedelta(hours=2):
                flash("Form expired. Please try again.", "error")
                return redirect(url_for("public.index"))
        except (ValueError, TypeError):
            pass

    if form.validate_on_submit():
        enquiry = Enquiry(
            name=form.name.data,
            email=form.email.data or None,
            phone=form.phone.data or None,
            service=form.service.data or None,
            preferred_date=form.preferred_date.data or None,
            message=form.message.data,
            status="new",
        )
        db.session.add(enquiry)
        db.session.commit()

        # Optional: Send email notification (if SMTP configured)
        send_enquiry_notification(enquiry)

        flash("Thank you! We received your inquiry and will contact you within 24 hours.", "success")
        return redirect(url_for("public.index"))

    # Form validation failed
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "error")

    return redirect(url_for("public.index"))

def send_enquiry_notification(enquiry):
    """Send email notification to admin (if SMTP configured)."""
    if not current_app.config.get("MAIL_SERVER"):
        return  # SMTP not configured

    try:
        from flask_mail import Mail, Message
        mail = Mail(current_app)
        msg = Message(
            subject=f"New Enquiry: {enquiry.name}",
            recipients=[current_app.config.get("MAIL_DEFAULT_SENDER")],
            body=f"""
New enquiry received:

Name: {enquiry.name}
Email: {enquiry.email}
Phone: {enquiry.phone}
Service: {enquiry.service}
Preferred Date: {enquiry.preferred_date}

Message:
{enquiry.message}

---
View in admin: {url_for('admin.view_enquiry', enquiry_id=enquiry.id, _external=True)}
            """,
        )
        mail.send(msg)
    except ImportError:
        current_app.logger.warning("flask_mail not installed; skipping email notification")
    except Exception as e:
        current_app.logger.error(f"Failed to send enquiry email: {e}")

@public_bp.route("/privacy")
def privacy():
    """Privacy notice page."""
    return render_template("privacy.html")

@public_bp.route("/sitemap.xml")
def sitemap():
    """Generate sitemap.xml for SEO."""
    base_url = request.host_url.rstrip("/")
    urls = [
        {"loc": base_url, "changefreq": "weekly", "priority": 1.0},
        {"loc": f"{base_url}/privacy", "changefreq": "yearly", "priority": 0.5},
    ]

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += f'  </url>\n'
    xml += '</urlset>'

    return xml, 200, {"Content-Type": "application/xml"}

@public_bp.route("/robots.txt")
def robots():
    """Generate robots.txt for SEO."""
    return """User-agent: *
Allow: /
Disallow: /admin
Disallow: /auth

Sitemap: """ + url_for("public.sitemap", _external=True), 200, {"Content-Type": "text/plain"}

@public_bp.route("/schema.json")
def schema():
    """JSON-LD LocalBusiness schema for SEO."""
    config = current_app.site_config
    business = config.get("business", {})

    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": business.get("name", "Business"),
        "description": business.get("description", ""),
        "url": request.host_url.rstrip("/"),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": business.get("address", ""),
        },
        "telephone": business.get("phone", ""),
        "email": business.get("email", ""),
    }

    return jsonify(schema)

@public_bp.errorhandler(404)
def not_found(error):
    """404 error handler."""
    return render_template("404.html"), 404

@public_bp.errorhandler(500)
def server_error(error):
    """500 error handler."""
    return render_template("500.html"), 500

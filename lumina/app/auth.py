"""
Authentication blueprint: login, logout, session management.
"""

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import db, Admin
from app.forms import LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Admin login page supporting classic and signal variants."""
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()

        if admin and admin.check_password(form.password.data):
            login_user(admin, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Incorrect username or password.", "error")

    # Determine variant: query param takes precedence, then config/env, default "classic"
    variant = request.args.get("variant")
    if not variant:
        variant = current_app.config.get("ADMIN_LOGIN_VARIANT") or os.environ.get("ADMIN_LOGIN_VARIANT", "classic")
    variant = variant.lower()

    template = "auth/login_signal.html" if variant == "signal" else "login.html"

    return render_template(template, form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    """Logout admin."""
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("public.index"))

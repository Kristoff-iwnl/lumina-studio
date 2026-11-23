import os
import json
from pathlib import Path
from flask import Flask, render_template, request, current_app
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

from config.config import config
from app.models import db, Admin

# Load environment variables
load_dotenv()

# Initialize extensions
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
login_manager = LoginManager()

def create_app(config_obj=None):
    """Application factory."""
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    if config_obj is None:
        config_obj = config
    app.config.from_object(config_obj)

    # Production safety checks for SECRET_KEY
    app_env = os.environ.get("APP_ENV") or os.environ.get("FLASK_ENV", "development")
    if app_env.lower() == "production" or getattr(config_obj, "DEBUG", True) is False:
        secret_key = app.config.get("SECRET_KEY")
        if not secret_key or len(secret_key) < 32 or secret_key == "dev-key-change-in-production":
            raise RuntimeError("CRITICAL: Production mode requires a secure SECRET_KEY of at least 32 characters!")

    # ProxyFix middleware
    trusted_proxies = app.config.get("TRUSTED_PROXY_COUNT", 1)
    if trusted_proxies > 0 and app_env.lower() == "production":
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=trusted_proxies, x_proto=trusted_proxies, x_host=trusted_proxies, x_prefix=trusted_proxies)

    # Ensure instance folder exists
    Path(app.config["INSTANCE_PATH"]).mkdir(exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Load site config
    @app.before_request
    def load_site_config():
        """Load site.json into app context."""
        try:
            with open(app.config["SITE_CONFIG_PATH"]) as f:
                app.site_config = json.load(f)
        except FileNotFoundError:
            app.site_config = {}

    # Context processor: make site config available in all templates
    @app.context_processor
    def inject_config():
        return {"config": getattr(app, "site_config", {})}

    # Register blueprints
    from app.routes_public import public_bp
    from app.routes_admin import admin_bp
    from app.auth import auth_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/login")
    @app.route("/admin/login")
    def global_login_redirect():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    # Health check route (no DB touch)
    @app.route("/healthz")
    def healthz():
        return "OK", 200, {"Content-Type": "text/plain"}

    # Error handlers
    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    @app.after_request
    def set_security_headers(response):
        frontend_variant = os.environ.get("FRONTEND_VARIANT") or current_app.config.get("FRONTEND_VARIANT", "cinematic")
        is_cinematic = request.path.startswith("/cinematic") or request.path.startswith("/auth/login") or (request.path == "/" and frontend_variant.lower() == "cinematic")
        if is_cinematic:
            csp = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' https://raft-blast-61784561.figma.site https://d8j0ntlcm91z4.cloudfront.net data:; "
                "font-src 'self' https://dcym8fthxf5uu.cloudfront.net data:; "
                "media-src 'self' https://d8j0ntlcm91z4.cloudfront.net; "
                "connect-src 'self';"
            )
        else:
            csp = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "font-src 'self'; "
                "media-src 'self'; "
                "connect-src 'self';"
            )
        response.headers["Content-Security-Policy"] = csp

        # HSTS in production over HTTPS
        app_env = os.environ.get("APP_ENV") or os.environ.get("FLASK_ENV", "development")
        if app_env.lower() == "production":
            response.headers["Strict-Transport-Security"] = "max-age=300"

        return response

    # CLI commands
    @app.cli.command()
    def create_admin():
        """Create first admin user."""
        import getpass

        with app.app_context():
            if Admin.query.first():
                print("Admin already exists.")
                return

            email = input("Admin email: ").strip()
            if not email:
                print("Email is required.")
                return

            password = getpass.getpass("Password (hidden): ")
            if len(password) < 8:
                print("Password must be at least 8 characters.")
                return

            admin = Admin(email=email)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin created: {email}")

    @app.cli.command()
    def init_db():
        """Initialize database."""
        with app.app_context():
            db.create_all()
            print("Database initialized.")

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    return app

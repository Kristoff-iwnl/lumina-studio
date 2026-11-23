import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Flask config
class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or f"sqlite:///{BASE_DIR / 'instance' / 'lumina.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 8 * 60 * 60  # 8 hours

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get("RATELIMIT_STORAGE_URL") or "memory://"

    # Email (optional, off by default)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@lumina.studio")

    # Site config path
    SITE_CONFIG_PATH = BASE_DIR / "config" / "site.json"
    INSTANCE_PATH = BASE_DIR / "instance"
    FRONTEND_VARIANT = "cinematic"
    ADMIN_LOGIN_VARIANT = "signal"

class Development(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class Testing(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing form submission
    SESSION_COOKIE_SECURE = False

class Production(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

# Select config based on environment
env = os.environ.get("FLASK_ENV", "development").lower()
if env == "testing":
    config = Testing()
elif env == "production":
    config = Production()
else:
    config = Development()

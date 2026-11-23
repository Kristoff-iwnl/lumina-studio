# LUMINA — Cinematic Photography Studio & Admin Hub

A production-grade Flask web application for a photography studio featuring a high-end cinematic public frontend, a secure Signal admin login, and a Capitalio-inspired admin dashboard with real-time SQLite ORM management.

> *Note: This is a production-ready demo concept built for professional photography studios.*

## 🌟 Live Demo & Preview
- **Live Demo / Repository:** [GitHub Repository — Kristoff-iwnl/lumina-studio](https://github.com/Kristoff-iwnl/lumina-studio)
- **Admin Login:** `/auth/login?variant=signal` (Credentials: `admin@lumina.com` / `Admin123`)

---

## ✨ Features
- **Dual Public Frontend:**
  - **Cinematic Variant (Default):** Interactive scroll engine, video background, and immersive visual storytelling.
  - **Classic Variant:** Clean, traditional photography studio landing page.
- **Client Enquiry System:** Honeypot bot protection, time-trap validation, rate-limiting (`flask-limiter`), and optional email notifications (`flask-mail`).
- **Secure Authentication & Admin Hub:**
  - Signal admin login variant with local/CloudFront falcon video stream.
  - Capitalio Shadcn-inspired admin dashboard with real-time enquiry stats, client avatars, recent submissions table, and management hubs (Services, FAQs, Testimonials, Enquiries).
- **Security & Compliance:** Strict Content Security Policy (CSP), CSRF protection (`Flask-WTF`), HTTPOnly/Secure cookies, ProxyFix support, and HSTS headers.

---

## 🛠️ Tech Stack
- **Backend:** Python 3.12, Flask 3.x, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-Limiter
- **Database:** SQLite (`instance/app.db`)
- **Frontend:** Vanilla JS, CSS3, Custom Glassmorphism UI
- **Testing:** Pytest (47 comprehensive tests)

---

## 🚀 Quick Start (Local Development)

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/Kristoff-iwnl/lumina-studio.git
cd lumina-studio
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r lumina/requirements.txt
pip install -r lumina/requirements-dev.txt
```

### 3. Initialize Database & Create Admin
```bash
cd lumina
flask --app wsgi db upgrade
flask --app wsgi create-admin
```

### 4. Run Development Server
```bash
python wsgi.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📋 Environment Variables

| Variable | Default | Description |
|---|---|---|
| `FLASK_ENV` | `development` | Flask environment mode (`development` vs `production`). |
| `APP_ENV` | `development` | Application environment mode. |
| `SECRET_KEY` | `dev-key-...` | Cryptographic signing key (Required in production: ≥ 32 chars). |
| `DATABASE_URL` | `sqlite:///instance/app.db` | SQLite database URI. |
| `FRONTEND_VARIANT` | `cinematic` | Default public website variant (`cinematic` vs `classic`). |
| `ADMIN_LOGIN_VARIANT` | `signal` | Admin login variant (`signal` vs `classic`). |
| `DEMO_MODE` | `false` | Enables read-only demo mode with sample data and banner. |
| `TRUSTED_PROXY_COUNT` | `1` | Number of proxy headers to trust for IP rate limiting and HTTPS scheme detection. |
| `SITE_URL` | `http://127.0.0.1:5000` | Canonical site URL for sitemap, robots.txt, and Open Graph tags. |

---

## 🧪 Running Tests
```bash
pytest lumina/tests/
```

---

## 📦 Deployment Guides
- [Deploying to PythonAnywhere (Free Tier)](docs/DEPLOY_PYTHONANYWHERE.md)
- [Deploying to Render (Free Tier)](docs/DEPLOY_RENDER.md)
- [Pre-Deploy Checklist](docs/PRE_DEPLOY_CHECKLIST.md)
- [SQLite Backup & Restore Guide](docs/BACKUP.md)

---

## 📝 Credits & Assets
- **Fonts:** Ogg Text & Inter (Licensed / CDN)
- **Cinematic Assets & Icons:** Figma & CloudFront CDN
- **Background Video:** Fictional promotional video stream (Verified / Demo)

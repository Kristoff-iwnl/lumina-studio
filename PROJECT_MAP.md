# LUMINA Project Map & Architecture

## 1. Stack & Architecture
- **Language / Runtime:** Python 3.12+
- **Framework:** Flask 3.x with Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-Limiter, Flask-WTF / WTForms.
- **Database:** SQLite (`instance/app.db` by default) via SQLAlchemy ORM.
- **Frontend:** Dual-variant architecture (`classic` and `cinematic` Mostar scroll variant), Capitalio Shadcn-inspired admin dashboard, Vanilla JS / CSS.
- **Entry Points:** 
  - Application factory: `lumina/app/__init__.py:create_app()`
  - WSGI server script: `lumina/wsgi.py`
  - CLI runner: `flask` CLI (`flask run`, `flask init-db`, `flask create-admin`, `flask db upgrade`)

## 2. Configuration & Environment Variables
Config is loaded from `config/config.py`, `config/site.json`, and `.env` (via `python-dotenv`).

| Variable | Default | Description |
|---|---|---|
| `FLASK_APP` | `lumina/wsgi.py` | Flask application entry point. |
| `FLASK_ENV` | `production` / `development` | Flask environment mode. |
| `SECRET_KEY` | None (required in prod) | Cryptographic signing key for sessions and CSRF. |
| `DATABASE_URL` / `DATABASE_PATH` | `instance/app.db` | SQLite database file path. |
| `FRONTEND_VARIANT` | `cinematic` | Default public website variant (`cinematic` vs `classic`). |
| `CINEMATIC_ENGINE` | `original` | Cinematic scroll animation engine mode. |
| `ADMIN_LOGIN_VARIANT` | `signal` | Admin login page variant (`signal` vs `classic`). |
| `DEMO_MODE` | `false` | Enables read-only demo mode with sample data and banner. |
| `RATELIMIT_STORAGE_URI` | `memory://` | Flask-Limiter storage backend URI. |
| `TRUSTED_PROXY_COUNT` | `1` | Number of proxy headers to trust for IP rate limiting and HTTPS scheme detection. |
| `SITE_URL` | `http://127.0.0.1:5000` | Canonical site URL for sitemap, robots.txt, and Open Graph metadata. |
| `MAIL_SERVER` / `MAIL_DEFAULT_SENDER` | None | SMTP configuration for email enquiry notifications. |

## 3. Database, Migrations & CLI Commands
- **Location:** SQLite database file stored at `instance/app.db`.
- **Migrations:** Managed via Flask-Migrate (`migrations/`). Run upgrades with `flask db upgrade`.
- **CLI Commands:**
  - `flask init-db`: Creates database tables.
  - `flask create-admin`: Interactive prompt to create an administrator user with a secure password hash.
  - `flask seed`: Seeds initial sample data when DB is empty.

## 4. Static Assets & File Sizes
- **Local Static Files (`lumina/app/static/`):**
  - Cinematic engine scripts (`opt/engine.js`, `script.js`, `nav-anchors.js`, etc.)
  - Stylesheets (`css/main.css`, `css/admin.css`, `cinematic/styles.css`, etc.)
  - Media & Images (`app/static/images/`, `app/static/videos/aurora-bg.mp4`)
  - Admin Login local assets (`lumina/app/static/admin-login/falcon.mp4`, `poster.webp`)
- **Third-Party CDN Assets:**
  - Fonts: `https://dcym8fthxf5uu.cloudfront.net/fonts/`
  - Cinematic background images and textures: `https://raft-blast-61784561.figma.site/_assets/`
  - CloudFront CDN icons and video streams: `https://d8j0ntlcm91z4.cloudfront.net/`
- **Large Files (> 1 MB):**
  - Video files (`falcon.mp4`, `aurora-bg.mp4`, reference `.mp4` files) exceed 1 MB and are kept locally or streamed via CloudFront.

## 5. Security & Content Security Policy (CSP)
- **CSP Headers (Cinematic & Admin Login):**
  - `default-src 'self';`
  - `script-src 'self';`
  - `style-src 'self' 'unsafe-inline';`
  - `img-src 'self' https://raft-blast-61784561.figma.site https://d8j0ntlcm91z4.cloudfront.net data:;`
  - `font-src 'self' https://dcym8fthxf5uu.cloudfront.net data:;`
  - `media-src 'self' https://d8j0ntlcm91z4.cloudfront.net;`
  - `connect-src 'self';`

## 6. Test Suite
- **Count:** 44 automated tests (`pytest lumina/tests/`).
- **Run command:** `pytest lumina/tests/`

## 7. Files That Should Never Be Public
- `instance/` (contains SQLite `.db` database files)
- `.env`, `.env.local`, `.env.production` (contains `SECRET_KEY`, database credentials, SMTP passwords)
- `venv/`, `.venv/` (Python virtual environment)
- `.pytest_cache/`, `__pycache__/`, `*.pyc`
- `backups/`, `assets_src/`

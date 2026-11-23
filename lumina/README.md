# LUMINA — Premium Photography Studio Website

A production-grade, reusable small-business website template. Built for LUMINA (demo), re-skinnale for any service business in under an hour by editing `config/site.json`.

## Quick Start

### Requirements
- Python 3.11+
- pip

### Setup (5 minutes)

```bash
# Clone/download and enter the directory
cd lumina

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env from example
cp .env.example .env

# Initialize database and create first admin
flask db upgrade
flask create-admin
# Follow the prompt to set your password

# Load demo data (optional, for development)
python seed.py

# Run the app
flask run
# Visit http://localhost:5000
```

### Config

All business content lives in `config/site.json`:
- Business name, tagline, hours
- Services, FAQ, testimonials
- Contact details, social links
- Theme colours (accent pair, fonts)

Edit this file and restart the app to re-skin. No code changes needed.

### Admin Area

- **URL**: http://localhost:5000/admin
- **Login**: Use credentials from `flask create-admin`
- **Manage**: Enquiries, services, FAQ, testimonials, site settings

### Deploying

SQLite requires a persistent disk. For Heroku, Railway, Render:
- Set `DATABASE_URL` environment variable pointing to a persistent volume
- Or use a managed PostgreSQL database (update `config.py` to accept `postgres://` URLs)

See `ARCHITECTURE.md` for database schema and `DECISIONS.md` for trade-offs.

## Project Structure

```
lumina/
├── app/                          # Flask application
│   ├── __init__.py              # App factory
│   ├── models.py                # SQLAlchemy models
│   ├── auth.py                  # Login/logout, session management
│   ├── forms.py                 # WTForms (enquiry, login, admin CRUD)
│   ├── routes_public.py         # Home, privacy, 404, 500
│   ├── routes_admin.py          # /admin, enquiries, content CRUD
│   ├── templates/               # Jinja templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── privacy.html
│   │   ├── login.html
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── enquiries.html
│   │   │   ├── services.html
│   │   │   ├── faq.html
│   │   │   ├── testimonials.html
│   │   │   └── settings.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css         # Custom properties, glass, gradients
│   │   │   └── print.css        # Print stylesheet
│   │   ├── js/
│   │   │   ├── main.js          # Scroll reveals, form handling
│   │   │   └── hero-3d.js       # Three.js hero (loaded dynamically)
│   │   └── vendor/
│   │       └── three.min.js     # Vendored Three.js
├── config/
│   ├── site.json                # All business content + theme
│   ├── config.py                # Flask config, database URL, secrets
├── migrations/                  # Flask-Migrate (Alembic)
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures
│   ├── test_auth.py
│   ├── test_enquiry.py
│   ├── test_admin.py
│   ├── test_crud.py
│   └── test_routes.py
├── seed.py                      # Demo data (clearly fictional)
├── requirements.txt
├── .env.example
├── .gitignore
├── wsgi.py                      # Entry point for production
├── ARCHITECTURE.md              # Request flow, file-by-file explanation
├── DECISIONS.md                 # Trade-offs and rationale
├── CREDITS.md                   # Asset licenses
└── pytest.ini
```

## Development

### Run tests

```bash
pytest --cov=app --cov-report=term-missing
```

### Check Lighthouse

```bash
# Run the app, then in another terminal:
npm install -g lighthouse
lighthouse http://localhost:5000 --chrome-flags="--headless --no-sandbox"
```

### Make migrations

```bash
flask db migrate -m "Description of change"
flask db upgrade
```

## Features

✅ **Dark-first design** with frosted glass and gradient accents  
✅ **3D hero** (Three.js, mouse parallax, pauses when off-screen)  
✅ **Enquiry form** with honeypot, rate limiting, validation  
✅ **Admin panel** (login required, sessions, rate limiting)  
✅ **SEO**: sitemap.xml, robots.txt, JSON-LD LocalBusiness  
✅ **Accessibility**: WCAG AA, keyboard navigation, prefers-reduced-motion  
✅ **Security**: CSRF, parameterised queries, CSP, no inline scripts  
✅ **Tests**: 80%+ coverage, pytest + optional Playwright smoke test  
✅ **Performance**: Lighthouse 90+, lazy load 3D, pause WebGL when hidden  

## License

Demo / portfolio use. Modify as you wish. See `CREDITS.md` for third-party licenses.

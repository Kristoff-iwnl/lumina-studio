# LUMINA — Phase 0 Complete

## What Was Built

### Project Structure
```
lumina/
├── README.md                 # Quick start guide
├── ARCHITECTURE.md           # Request flow, file-by-file explanation
├── DECISIONS.md              # Trade-offs and rationale
├── CREDITS.md                # Licenses and attribution
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusions
├── wsgi.py                   # WSGI entry point
├── seed.py                   # Demo data generator
├── config/
│   ├── site.json             # All business content (name, services, theme)
│   └── config.py             # Flask configuration
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # SQLAlchemy models (Admin, Enquiry, Service, FAQ, Testimonial)
│   ├── auth.py               # [Stub for Phase 1]
│   ├── forms.py              # [Stub for Phase 1]
│   ├── routes_public.py      # [Stub for Phase 1]
│   ├── routes_admin.py       # [Stub for Phase 1]
│   ├── templates/            # [Empty, ready for Phase 2]
│   └── static/               # [Empty, ready for Phase 4]
├── migrations/               # [Ready for Flask-Migrate in Phase 1]
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # pytest fixtures
│   ├── test_auth.py          # [Placeholder tests]
│   ├── test_enquiry.py
│   ├── test_admin.py
│   └── test_routes.py
└── pytest.ini                # pytest configuration
```

### What's Ready

✅ **Configuration & Documentation**
- Complete README with setup instructions
- ARCHITECTURE.md with request flow and file-by-file explanation
- DECISIONS.md documenting 20 design trade-offs
- CREDITS.md with all licenses
- .env.example showing all required environment variables

✅ **Database Models**
- Admin (email, hashed password)
- Enquiry (name, email, phone, service, message, status, timestamps)
- Service (name, description, price, icon, order)
- FAQ (question, answer, order)
- Testimonial (name, role, message, approved flag, order)
- SiteSettings (key-value store for dynamic content)

✅ **Configuration System**
- `config/site.json`: Single file containing all business content (name, tagline, hours, services, FAQ, testimonials, theme colors, fonts)
- `config/config.py`: Flask config (Development, Testing, Production)
- Environment-based secrets (SECRET_KEY, DATABASE_URL, SMTP settings)

✅ **Demo Data**
- `seed.py`: Generates 3 services, 5 FAQs, 4 testimonials (3 approved), 2 sample enquiries
- Clearly marked as fictional for portfolio use

✅ **Test Infrastructure**
- pytest configuration with markers and warnings filters
- Fixtures: app, client, runner, admin_user, authenticated_client
- Placeholder tests for all major features (auth, enquiry, admin, public routes)
- Coverage-ready structure

---

## How to Run (Phase 0 Verification)

### 1. Setup
```bash
cd D:\Small business websites\lumina

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env
copy .env.example .env

# Create instance directory
mkdir instance
```

### 2. Initialize Database
```bash
# Create tables
flask db upgrade
# or: flask init-db

# Create admin user
flask create-admin
# Follow prompts (email and password)
```

### 3. Load Demo Data (Optional)
```bash
python seed.py
```

### 4. Run Tests (Phase 0 Validation)
```bash
pytest --cov=app --cov-report=term-missing -v
```

Expected output: All tests skip (no routes implemented yet) or fail gracefully. Coverage will be 0% until Phase 1.

### 5. Run the App (Phase 1+)
```bash
flask run
# Visit http://localhost:5000
```

---

## Deliverables for Review

✅ **README.md** — Complete setup guide  
✅ **ARCHITECTURE.md** — Request flow and file-by-file breakdown  
✅ **DECISIONS.md** — 20 documented trade-offs  
✅ **CREDITS.md** — All licenses and attribution  
✅ **config/site.json** — Business content template (LUMINA demo)  
✅ **config/config.py** — Flask configuration (Dev/Test/Prod)  
✅ **app/models.py** — 6 SQLAlchemy models with relationships  
✅ **app/__init__.py** — App factory with CLI commands  
✅ **seed.py** — Demo data generator  
✅ **requirements.txt** — All dependencies pinned  
✅ **.env.example** — Environment variable template  
✅ **.gitignore** — Safe git exclusions  
✅ **wsgi.py** — WSGI entry point  
✅ **pytest.ini** — Test configuration  
✅ **tests/conftest.py** — pytest fixtures  
✅ **tests/test_*.py** — Placeholder test files (5 test modules)  

---

## Key Design Decisions (Phase 0)

1. **SQLite by default**, PostgreSQL optional via `DATABASE_URL`
2. **Config as JSON** (not database): `config/site.json` is the source of truth for business content
3. **Single admin** created via CLI (`flask create-admin`), hashed with werkzeug
4. **Session-based auth** (no JWT), HttpOnly + Secure (prod) cookies
5. **6 models** covering enquiries, content, and admin
6. **Pytest fixtures** for app, client, authenticated user
7. **Environment variables** for secrets (no defaults in code)
8. **8-hour session** lifetime, rate limiting on login (5/min per IP)

---

## What's NOT in Phase 0

❌ No routes (public or admin)  
❌ No templates  
❌ No CSS or JavaScript  
❌ No 3D hero  
❌ No authentication middleware (auth.py is a stub)  
❌ No forms library setup (forms.py is a stub)  
❌ No rate limiting configured  
❌ No database migrations yet (Flask-Migrate configured but not run)  

---

## Next: Phase 1 (Backend Core)

Phase 1 will implement:
- Authentication blueprint (`auth.py`): login, logout, session middleware
- Forms blueprint (`forms.py`): WTForms for enquiry, login, CRUD
- Public routes (`routes_public.py`): homepage stub, enquiry POST, privacy, 404, 500
- Admin routes (`routes_admin.py`): dashboard, CRUD for services/FAQ/testimonials, enquiry list
- Rate limiting configuration
- Flask-Migrate setup
- Running tests (expecting some passes, some failures to guide implementation)

---

## Questions / Uncertainties

None for Phase 0. Configuration and models are complete and straightforward.

Approval for Phase 1?


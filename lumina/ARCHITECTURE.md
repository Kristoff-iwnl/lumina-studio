# LUMINA — Architecture

## Overview

LUMINA is a production-grade, reusable small-business website template. It's designed to be re-skinned in under an hour by editing `config/site.json`.

### Tech Stack
- **Backend**: Flask 2.3, SQLAlchemy ORM, SQLite (or PostgreSQL)
- **Frontend**: Server-rendered Jinja2 templates, vanilla CSS (custom properties), vanilla JavaScript (ES modules)
- **3D**: Three.js (vendored, dynamically imported)
- **Security**: CSRF (Flask-WTF), rate limiting (Flask-Limiter), parameterised queries
- **Tests**: pytest with coverage

---

## Request Flow

```
1. User visits homepage (GET /)
   ↓
2. Public route handler loads site.json into app context
   ↓
3. Jinja template renders with config data (business name, hours, services, theme)
   ↓
4. Browser receives HTML + CSS + vanilla JS
   ↓
5. JS loads Three.js hero dynamically (after first paint, if not reduced-motion)
   ↓
6. User interacts: form submission → POST /enquiry
   ↓
7. Rate limiter checks IP (5 per hour)
   ↓
8. WTForms validates (honeypot, CSRF token, field lengths)
   ↓
9. Time-trap checked (form must be submitted within reasonable window)
   ↓
10. Data written to database, optional email sent
    ↓
11. User sees confirmation

Admin flow:
1. User visits /admin
2. Auth middleware redirects to /auth/login if not authenticated
3. POST login validates credentials, sets session cookie (8 hours, HttpOnly)
4. Rate limiter: 5 attempts per minute per IP
5. Authenticated user can CRUD services, FAQ, testimonials, view enquiries
6. All forms have CSRF tokens
7. Session timeout or logout clears cookie
```

---

## File-by-File Explanation

### `app/__init__.py` (App Factory)
- **Purpose**: Flask application factory, initializes extensions
- **Key Functions**:
  - `create_app()`: Creates Flask app with config, blueprints, CLI commands
  - `load_site_config()`: Loads `config/site.json` on every request (or cache if needed for perf)
  - `create_admin`: CLI command to create first admin (password hashed with werkzeug)
  - `inject_config()`: Context processor to make config available in all templates
- **Security**: SECRET_KEY from environment, CORS headers, CSP
- **Note**: Database connection and migrations are handled by Flask-Migrate

### `app/models.py` (ORM Models)
- **Admin**: Email + hashed password, `check_password()` method
- **Enquiry**: name, email, phone, service, message, status, timestamps. Indexed on status and created_at for fast filtering
- **Service**: name, description, price, icon, order (for sorting)
- **FAQ**: question, answer, order
- **Testimonial**: name, role, message, approved flag (only approved ones display), order
- **SiteSettings**: Key-value store for dynamic settings (hours, contact, social links)
- **Note**: All use SQLAlchemy ORM, parameterised queries by default, timestamps auto-managed

### `app/auth.py` (Authentication Blueprint)
- **Routes**:
  - `GET /auth/login` → renders login form
  - `POST /auth/login` → validates email/password, rate-limited (5 per minute per IP), sets session cookie
  - `GET /auth/logout` → clears session
- **Security**:
  - Passwords checked with werkzeug (bcrypt-style hashing)
  - Session: HttpOnly, Secure (in production), SameSite=Lax, 8-hour expiry
  - Rate limiting on login endpoint
  - CSRF token on login form

### `app/forms.py` (WTForms)
- **EnquiryForm**: name (2–80 chars), email or phone (validated), service dropdown, message (10–2000 chars), honeypot field
- **LoginForm**: email, password
- **ServiceForm**, **FAQForm**, **TestimonialForm**: Used by admin to create/edit
- **All forms**: CSRF protection, field validators

### `app/routes_public.py` (Public Blueprint)
- **Routes**:
  - `GET /` → render homepage (services, FAQ, testimonials from DB, config theme)
  - `POST /enquiry` → handle form submission (validate, honeypot, rate limit, store, optional email)
  - `GET /privacy` → privacy notice (what data is stored, why, retention)
  - `404`, `500` → custom error pages
- **Rate Limiting**: 5 enquiries per hour per IP
- **Honeypot**: Hidden field that should be empty; if filled, treat as spam
- **Time-Trap**: Check that form was posted within 2 hours of page load (rough CSRF variant)

### `app/routes_admin.py` (Admin Blueprint)
- **Routes** (all require login):
  - `GET /admin` → dashboard (enquiry counts by status, recent enquiries)
  - `GET /admin/enquiries` → list with search, filter, pagination
  - `GET /admin/enquiries/<id>` → view detail, mark as contacted/done/spam
  - `POST /admin/enquiries/<id>/delete` → delete enquiry
  - `GET /admin/enquiries/export` → CSV export
  - `GET /admin/services`, `POST /admin/services`, etc. → CRUD for services, FAQ, testimonials
  - `GET /admin/settings` → edit hours, contact, social links (stored in SiteSettings or config)
- **Access Control**: All routes check `@login_required`
- **CSRF**: All POST/DELETE forms have tokens

### `config/site.json` (Business Config)
- **Structure**:
  - `business`: name, tagline, email, phone, address, hours (object), social links
  - `theme`: accentPrimary, accentSecondary, dark, light, fontDisplay, fontBody
  - `hero`: headline, subheadline, CTA text
  - `services`: array of {name, description, price, icon}
  - `howItWorks`: 3-step process
  - `faq`: array of {question, answer}
  - `testimonials`: array of {name, role, message, approved}
  - `seo`: site name, description, keywords, og image
- **Note**: This is the **only file** a client edits to rebrand. All HTML/CSS/JS references these values

### `config/config.py` (Flask Config)
- **Config Classes**: Base, Development, Testing, Production
- **Settings**:
  - `SECRET_KEY`: from environment (required in production)
  - `SQLALCHEMY_DATABASE_URI`: SQLite by default, can override with `DATABASE_URL` env var
  - `SESSION_COOKIE_SECURE`: False in dev, True in production
  - `PERMANENT_SESSION_LIFETIME`: 8 hours
  - `RATELIMIT_STORAGE_URL`: Memory or Redis
- **Note**: `SITE_CONFIG_PATH` points to `config/site.json`

### `app/templates/base.html` (Base Template)
- **Includes**:
  - `<head>`: Meta tags (viewport, charset, SEO, Open Graph)
  - CSS import: `main.css`
  - JavaScript: `main.js` (vanilla, ES modules)
  - Prefers-reduced-motion media query
- **Block Structure**: `{% block content %}` for child templates
- **Context**: `config` is available from `inject_config()` context processor

### `app/templates/index.html` (Homepage)
- **Sections**:
  - Hero: 3D canvas (loaded dynamically), headline, subheadline, CTA buttons
  - Trust strip: hours, location, phone, WhatsApp link
  - Services: Cards from database
  - How it works: 3-step process
  - Gallery/Work: Placeholder (SVG or CSS art, no external images)
  - Testimonials: Only approved ones, hidden if none exist
  - FAQ: Accessible accordion
  - Enquiry form: Client-side and server-side validation
  - Footer: Contact, social links, privacy link, sitemap link
- **Data Binding**: All dynamic data from `config` dictionary
- **Note**: No inline scripts; all JS in `main.js`

### `app/templates/admin/` (Admin Templates)
- `dashboard.html`: Overview, recent enquiries
- `enquiries.html`: List, search, filter, actions
- `services.html`, `faq.html`, `testimonials.html`: CRUD forms
- `settings.html`: Edit hours, contact, social

### `app/static/css/main.css` (Main Stylesheet)
- **Custom Properties**: `--accent-primary`, `--accent-secondary`, `--dark`, `--light`, `--font-display`, `--font-body`
- **Design Tokens**:
  - Frosted glass: `backdrop-filter: blur(10px)`, solid fallback
  - Gradients: Accent pair on dark base
  - Motion: Scroll-reveal (fade + rise), hover lift, parallax (respects prefers-reduced-motion)
  - Typography: System fonts (or self-hosted)
- **Responsive**: Mobile-first, breakpoints at 768px, 1024px
- **Print**: Separate `print.css` (optional)

### `app/static/js/main.js` (Vanilla JavaScript)
- **Modules**:
  - `initScrollReveal()`: Fade + rise on scroll (Intersection Observer)
  - `initHoverEffects()`: Lift on card/button hover
  - `initFormValidation()`: Client-side form checks before submit
  - `initMobileMenu()`: Hamburger toggle (if needed)
  - `loadHeroThreeJS()`: Dynamic import of `hero-3d.js` (after first paint)
- **Event Listeners**: DOMContentLoaded, scroll, resize, visibility change
- **Accessibility**: Keyboard navigation, focus management

### `app/static/js/hero-3d.js` (Three.js 3D Scene)
- **Procedural Geometry**: Low-poly glass/iridescent shapes (no external models)
- **Interactivity**: Mouse parallax (gentle), scroll response
- **Performance**: Pause when tab hidden or hero off-screen, cap DPR at 2 (1.5 mobile)
- **Fallback**: Static gradient image if WebGL unavailable or prefers-reduced-motion
- **Note**: Loaded dynamically after first paint to avoid blocking

### `seed.py` (Demo Data)
- **Clearly Fictional**: All names, emails, testimonials are demos
- **Usage**: `python seed.py` populates DB with 3 services, 5 FAQs, 4 testimonials, 2 enquiries
- **Purpose**: Portfolio and testing

### `tests/` (Pytest)
- **Fixtures** (`conftest.py`): App, client, runner, test database
- **test_auth.py**: Login success/failure, rate limit, logout, session
- **test_enquiry.py**: Form validation, honeypot, time-trap, rate limit
- **test_admin.py**: Protected routes, CRUD, access control
- **test_routes.py**: Homepage, privacy, 404, 500
- **Coverage**: 80%+ on backend code

---

## Database Schema

```sql
-- Admin
id (PK), email (UNIQUE), password_hash, created_at

-- Enquiry
id (PK), name, email, phone, service, preferred_date, message, status (INDEX), created_at (INDEX), updated_at

-- Service
id (PK), name, description, price, icon, order, created_at

-- FAQ
id (PK), question, answer, order, created_at

-- Testimonial
id (PK), name, role, message, approved (INDEX), order, created_at

-- SiteSettings
id (PK), key (UNIQUE), value, updated_at
```

---

## Security Model

1. **Authentication**: Admin email + password (werkzeug hashing), sessions only
2. **CSRF**: Flask-WTF tokens on all forms
3. **Rate Limiting**: Flask-Limiter (IP-based)
   - Login: 5 per minute
   - Enquiry: 5 per hour
4. **Input Validation**: WTForms field validators + custom honeypot logic
5. **SQL Injection**: Prevented by ORM (parameterised queries)
6. **XSS**: Jinja2 auto-escapes by default, no inline scripts
7. **CSP**: Strict (no inline, no eval, Three.js from vendor/)
8. **Headers**: X-Content-Type-Options, Referrer-Policy, frame-ancestors none
9. **Secrets**: .env for SECRET_KEY, MAIL credentials, DATABASE_URL

---

## Performance Considerations

1. **3D Hero**: Loaded after first paint, paused when hidden
2. **Database**: Indexed on (enquiry.status, enquiry.created_at) for admin list queries
3. **CSS**: Custom properties for theme (no CSS-in-JS), minimal selectors
4. **JS**: Vanilla ES modules, no jQuery, code-split hero 3D
5. **Images**: SVG or CSS only in v1 (no file uploads)
6. **Fonts**: Self-hosted (no external CDN at runtime)
7. **Caching**: Session caching for site.json (optional, if reloading every request is slow)

---

## Extensibility

### Adding a New Admin Feature (e.g., Newsletter Signup)
1. Add model: `class NewsletterSubscriber(db.Model): ...`
2. Run migration: `flask db migrate -m "Add newsletter"`
3. Add route in `routes_admin.py`
4. Add template in `templates/admin/`
5. Add form in `forms.py`
6. Export/import as needed

### Re-Skinning for a New Client
1. Edit `config/site.json`: name, services, hours, colors, fonts
2. Run `seed.py` if custom testimonials/FAQ
3. Admin creates content via `/admin`
4. Deploy with new config

### Switching to PostgreSQL
1. Set `DATABASE_URL=postgresql://...` in `.env`
2. Flask-SQLAlchemy auto-detects, ORM code unchanged
3. Run migrations: `flask db upgrade`

---

## Deployment Notes

- **Persistent Disk Required**: SQLite needs a writable instance/ folder
- **Environment Variables**: SECRET_KEY, DATABASE_URL (optional), MAIL settings (optional)
- **Session Security**: Set `SESSION_COOKIE_SECURE=True` and use HTTPS
- **Rate Limiting**: In-memory by default (single-process). For multi-process, use Redis: `RATELIMIT_STORAGE_URL=redis://...`
- **Static Files**: Serve via CDN or `flask static` in development


# LUMINA — Decisions & Trade-Offs

This document records design decisions and their rationale.

---

## 1. SQLite by Default, PostgreSQL Optional

**Decision**: Use SQLite for development and small deployments; allow PostgreSQL via `DATABASE_URL`.

**Rationale**:
- SQLite is zero-config, perfect for a portfolio demo
- Requires persistent disk on cloud hosts (noted in README)
- For scaling, client can switch to PostgreSQL without code changes (Flask-SQLAlchemy handles both)

**Trade-off**: Single-process only with in-memory rate limiting; for multi-process production, Redis needed.

---

## 2. Vanilla JavaScript (No React/Vue)

**Decision**: Server-rendered Jinja templates + vanilla JS (ES modules).

**Rationale**:
- Simpler build, no npm/webpack overhead
- Fast first paint, SEO-friendly
- Three.js 3D hero is the only dynamic load (async import)
- Easier for clients to modify HTML/CSS without JS knowledge

**Trade-off**: No reactive state management; form handling is traditional POSTs. Acceptable for a brochure site with one form.

---

## 3. Three.js Loaded Dynamically After First Paint

**Decision**: Hero 3D canvas is not blocking; loaded with dynamic import after DOMContentLoaded.

**Rationale**:
- Fast Time to Interactive (TTI)
- User sees hero headline before WebGL initializes
- Respects `prefers-reduced-motion` (static gradient fallback)
- Falls back gracefully if WebGL unavailable

**Trade-off**: Slight delay before 3D animation starts. Acceptable for perceived performance.

---

## 4. Session-Based Auth (No JWT/OAuth)

**Decision**: Traditional session cookies, no JWT.

**Rationale**:
- Simpler for a small admin area (5–10 users max)
- HttpOnly cookies prevent XSS token theft
- Built-in to Flask-Login

**Trade-off**: Not suitable for multi-server deployments without sticky sessions or shared session store (Redis).

---

## 5. Honeypot + Time-Trap (Not CAPTCHA)

**Decision**: Hidden form field + submission window check, no visual CAPTCHA.

**Rationale**:
- Better UX (no puzzle-solving)
- Catches 90% of bot submissions
- Lightweight

**Trade-off**: Sophisticated bots may bypass. For high-volume spam, add CAPTCHA or email verification.

---

## 6. Admin-Only, No Public Sign-Up

**Decision**: Single admin account created via CLI; no public registration.

**Rationale**:
- Smaller attack surface
- Simple access control (all authenticated users have full admin access)
- Suitable for 1–3 team members managing the site

**Trade-off**: Not scalable to many admins with role-based access. For future: add roles (admin, editor, viewer).

---

## 7. Config as JSON File, Not Database

**Decision**: `config/site.json` is the source of truth for business content (name, services, theme).

**Rationale**:
- Client edits one file to re-skin (no database migration needed)
- Version control friendly
- Clear separation: config (static) vs. content (database)

**Trade-off**: Config not live-editable via admin UI (Phase 1). Future: sync JSON to SiteSettings table.

---

## 8. Self-Hosted Fonts, No CDN at Runtime

**Decision**: Fonts vendored locally; no Google Fonts CDN call.

**Rationale**:
- Privacy (no external requests to third parties)
- Better performance (no DNS/HTTP roundtrip)
- Works offline

**Trade-off**: Add font files to git (or store separately). WOFF2 format keeps size small.

---

## 9. SVG/CSS Art for Gallery, No Image Uploads (v1)

**Decision**: Placeholder gallery using CSS/SVG; no file uploads in v1.

**Rationale**:
- Simpler security model (no file validation, malicious uploads)
- Faster first release
- Placeholder is clear in UI

**Trade-off**: Real portfolio images require manual design. For v2: add file uploads with strict MIME type checks.

---

## 10. Rate Limiting on IP Address, Not Account

**Decision**: Flask-Limiter uses IP address as key (5 enquiries/hour per IP).

**Rationale**:
- No account lookup needed
- Prevents single-IP spam floods
- Works for anonymous enquiries

**Trade-off**: Corporate networks behind a proxy share one IP (may hit limit faster). Consider email-based rate limiting in v2.

---

## 11. Optional Email Notifications, Off by Default

**Decision**: Enquiry form can email admin if MAIL_* environment variables set; off by default.

**Rationale**:
- Reduces complexity and dependencies
- Avoids email provider setup overhead
- Admin can check `/admin/enquiries` instead

**Trade-off**: Client must check admin panel for new enquiries. For better UX: enable SMTP in production.

---

## 12. No Analytics or Third-Party Tracking

**Decision**: No Google Analytics, Mixpanel, or similar scripts.

**Rationale**:
- Privacy-first design
- Faster page load
- No vendor lock-in
- Focus on core functionality

**Trade-off**: Client has no traffic insights. For future: self-hosted analytics (Plausible, Fathom) or opt-in.

---

## 13. Single-Page Layout (No Multiple Pages)

**Decision**: Homepage + privacy + admin area. No blog, portfolio sub-pages, etc.

**Rationale**:
- Simpler scope, faster to build and maintain
- Suitable for service businesses (hours, services, enquiry form, testimonials)
- SEO still possible with meta tags and JSON-LD

**Trade-off**: Not suitable for portfolio photographers with 100+ projects. For v2: add portfolio section or blog.

---

## 14. SQLAlchemy ORM, Not Raw SQL

**Decision**: All database queries via SQLAlchemy ORM.

**Rationale**:
- Parameterised queries (prevents SQL injection)
- Auto-escaping
- Migrations handled by Alembic

**Trade-off**: Slightly more overhead than raw SQL. Acceptable for small datasets.

---

## 15. Lighthouse 90+ Target (Not 100)

**Decision**: Performance target is 90 for Performance, Accessibility, Best Practices, and SEO.

**Rationale**:
- 90+ is excellent and realistic
- 100 often requires micro-optimizations with diminishing returns
- 90+ is sufficient for SEO and user experience

**Trade-off**: Some optimizations (inline critical CSS, font subsetting) deferred to v2.

---

## 16. WCAG AA (Not AAA)

**Decision**: Accessibility compliance target is WCAG 2.1 Level AA.

**Rationale**:
- AA is legally compliant in most jurisdictions
- AAA requires extreme contrast and other hard-to-maintain standards
- Balances accessibility with design aesthetics

**Trade-off**: Some colour contrasts may not meet AAA. Full compliance requires manual testing with screen readers.

---

## 17. Flask-WTF for Forms (Not Manual CSRF)

**Decision**: Use Flask-WTF middleware and form library for CSRF protection.

**Rationale**:
- Handles CSRF tokens automatically
- Field validators built-in
- Integrates with Jinja2 template forms

**Trade-off**: Slight boilerplate for each form class. Worth the security.

---

## 18. Environment Variables for Secrets (Not .env in repo)

**Decision**: `.env` is in `.gitignore`; `.env.example` shows structure without secrets.

**Rationale**:
- Prevents accidental commit of SECRET_KEY, database passwords
- Standard practice
- .env.example serves as documentation

**Trade-off**: New developer must copy `.env.example` and fill in values. Clear in README.

---

## 19. Dynamic Import for Hero 3D (Not Inline)

**Decision**: Three.js hero loaded via `import()` after page ready, not in main bundle.

**Rationale**:
- Main page is usable before 3D loads
- User sees hero headline immediately
- WebGL fails gracefully with static fallback

**Trade-off**: Hero animation has a slight delay. Better UX than blocking on 3D.

---

## 20. Admin CRUD vs. Config JSON

**Decision**: Site theme (colors, fonts) comes from config JSON. Content (services, FAQ, testimonials) can be edited via admin UI.

**Rationale**:
- Separation of concerns: design vs. content
- Clients rarely change theme after launch
- Clients frequently update services/testimonials

**Trade-off**: No live theme editor. For v2: add theme customizer with color preview.

---

## Future Considerations (v2+)

- [ ] Booking slots (calendar integration)
- [ ] Email confirmations to customer
- [ ] Image uploads with strict validation
- [ ] Light theme toggle
- [ ] Multi-language support
- [ ] Newsletter signup
- [ ] Google Analytics or self-hosted analytics
- [ ] SEO blog/portfolio section
- [ ] Role-based admin access
- [ ] Automated backups for SQLite (or migrate to PostgreSQL)


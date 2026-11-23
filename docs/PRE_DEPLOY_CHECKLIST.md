# Pre-Deploy Checklist

- [ ] **Secrets & Keys:** `SECRET_KEY` is set to a secure random string (≥ 32 chars) and never committed to git.
- [ ] **Environment Variables:** `APP_ENV=production`, `SITE_URL` points to the correct production domain, and proxy count is configured (`TRUSTED_PROXY_COUNT=1`).
- [ ] **Demo Mode:** `DEMO_MODE=true` configured if deploying to an ephemeral free-tier host.
- [ ] **Admin Account:** Created securely via `flask create-admin` (or auto-seeded in demo mode).
- [ ] **Database & Migrations:** Ran `flask db upgrade` successfully.
- [ ] **Health Check:** `/healthz` returns `200 OK`.
- [ ] **HTTPS & Security:** Secure cookie flags and HSTS headers verified.
- [ ] **Robots & Sitemap:** `/robots.txt` disallows `/admin` and `/auth`, and `/sitemap.xml` returns correct URLs.
- [ ] **Testing:** All automated pytest tests pass successfully (`pytest lumina/tests/`).
- [ ] **Browser Console:** Verified both classic and cinematic variants and admin login load without console errors or CSP violations.

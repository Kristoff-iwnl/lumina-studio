# Pre-Deploy Checklist

## Configuration & Security

- [ ] `APP_ENV=production` is configured.
- [ ] `SECRET_KEY` is a secure random value of at least 32 characters and is not committed to Git.
- [ ] `SITE_URL` points to the correct production domain.
- [ ] `TRUSTED_PROXY_COUNT` matches the hosting provider's proxy configuration.
- [ ] HTTPS is enabled and secure cookie settings are verified.
- [ ] Security headers and Content Security Policy are checked.

## Database & Admin

- [ ] Database configuration points to the intended production database.
- [ ] Database migrations have been applied successfully:

  ```bash
  flask --app wsgi db upgrade
  ```

- [ ] Admin account has been created explicitly:

  ```bash
  flask --app wsgi create-admin
  ```

- [ ] Database persistence and backup strategy are confirmed.
- [ ] For ephemeral hosting, understand that local SQLite data may be lost after restarts or redeployments.

## Deployment Verification

- [ ] `/healthz` returns `200 OK`.
- [ ] Homepage and static assets load correctly.
- [ ] Admin login works.
- [ ] Enquiry submission and admin enquiry management work.
- [ ] `/robots.txt` and `/sitemap.xml` return the expected content.
- [ ] Both classic and cinematic frontend variants are checked if enabled.
- [ ] Browser console has no unexpected errors or Content Security Policy violations.

## Testing

- [ ] Automated tests pass:

  ```bash
  pytest lumina/tests/
  ```

- [ ] Production environment variables are reviewed before deployment.
- [ ] No `.env` files, database files, backups, or private credentials are committed to Git.

## Demo Deployment Notes

- [ ] Set `DEMO_MODE=true` only when intentionally deploying a demo.
- [ ] Confirm what demo mode changes in the application before enabling it.
- [ ] Do not treat demo mode as a substitute for persistent database storage or backups.
- [ ] Create an admin account explicitly if admin access is required.
# Reversion Guide for LUMINA Admin Login Signal Redesign

To revert the admin login back to the classic variant:

1. **Environment Configuration:**
   Set `ADMIN_LOGIN_VARIANT=classic` in your environment or `.env` file, or update `config/config.py` / `config/site.json` so that `ADMIN_LOGIN_VARIANT` defaults to `"classic"`.

2. **Query Parameter override:**
   You can also test classic mode directly at any time by visiting `/auth/login?variant=classic`.

3. **Git Reversion (if git is initialized):**
   ```bash
   git checkout v4-before-admin-login
   ```

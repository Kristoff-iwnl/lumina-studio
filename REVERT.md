# Reversion Guide for LUMINA Deployment Prep

To revert to the pre-deployment state (baseline before production preparation):

1. **Git Reversion:**
   ```bash
   git checkout v5-before-deploy-prep
   ```

2. **Variant Reversion:**
   - Classic public variant: visit `/classic` or set `FRONTEND_VARIANT=classic`.
   - Classic admin login: visit `/auth/login?variant=classic` or set `ADMIN_LOGIN_VARIANT=classic`.

# Architectural & Design Decisions (DECISIONS.md)

## Decision Log — Production Readiness & Deployment Prep

1. **Dual Variant Frontend Architecture:**
   - **What:** Maintained both `classic` and `cinematic` public frontends, with `cinematic` serving as default root (`/`).
   - **Why:** Preserves maximum flexibility and visual impact while keeping 100% of backend SQLite models and routes intact.

2. **Capitalio Admin Dashboard Integration:**
   - **What:** Redesigned admin dashboard using Capitalio Shadcn-inspired glassmorphism components.
   - **Why:** Delivers a modern, professional operations hub for studio management.

3. **Production Security & Proxy Fix:**
   - **What:** Enforced `SECRET_KEY` length checks in production mode, configured ProxyFix via `TRUSTED_PROXY_COUNT`, and added secure session/CSRF cookie flags & HSTS headers.
   - **Why:** Ensures safe deployment behind reverse proxies (Render, PythonAnywhere, Nginx) with correct client IP ratelimiting and HTTPS scheme detection.

4. **License Selection Request:**
   - **Note for User:** Please choose an open-source license (e.g., MIT, Apache 2.0, or BSD-3-Clause) for your repository. Once chosen, add the corresponding `LICENSE` file to the root of the project.

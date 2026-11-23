# Architectural & Design Decisions (DECISIONS.md)

## Decision Log — Companion Brief 4: Admin Login Redesign (Signal Variant)

1. **Variant Switch Mechanism:**
   - **What:** Implemented `ADMIN_LOGIN_VARIANT` configuration / environment variable (defaulting to `"classic"`), alongside dynamic query parameter support (`?variant=signal` or `?variant=classic`) for side-by-side comparison in development.
   - **Why:** Allows zero-downtime dual-variant testing and safe rollout without disrupting existing admin login flows.

2. **Template Independence (`auth/login_signal.html`):**
   - **What:** Standalone HTML document without template inheritance (`{% extends %}`), embedding exact CSS, JS, and font definitions per the Signal design spec.
   - **Why:** Ensures pixel-locked visual fidelity without interference from global layout stylesheets.

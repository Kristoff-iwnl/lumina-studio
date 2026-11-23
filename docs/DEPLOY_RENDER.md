# Deploying LUMINA to Render

## Prerequisites

- A Render account connected to the GitHub repository: `Kristoff-iwnl/lumina-studio`.

## Step-by-Step Deployment Guide

### 1. Create a Web Service

- Open your Render Dashboard.
- Select **New +** → **Web Service**.
- Connect `Kristoff-iwnl/lumina-studio`.

### 2. Configure Service Settings

- **Name:** `lumina-studio`
- **Environment:** `Python`
- **Root Directory:** Leave blank (repository root).
- **Build Command:**

  ```bash
  pip install -r lumina/requirements.txt && cd lumina && flask --app wsgi db upgrade
  ```

- **Start Command:**

  ```bash
  gunicorn --chdir lumina --workers 1 --threads 4 --bind 0.0.0.0:$PORT wsgi:app
  ```

- **Plan:** Free (or your preferred plan).

### 3. Configure Environment Variables

Add these in the Render Dashboard:

| Variable | Value |
|---|---|
| `APP_ENV` | `production` |
| `SECRET_KEY` | Generate a secure random key of at least 32 characters |
| `DEMO_MODE` | `true` |
| `FRONTEND_VARIANT` | `cinematic` |
| `ADMIN_LOGIN_VARIANT` | `signal` |
| `TRUSTED_PROXY_COUNT` | `1` |
| `SITE_URL` | Your Render service URL, e.g. `https://your-app.onrender.com` |

Do not commit production secrets to GitHub.

### 4. Deploy and Verify

Click **Create Web Service**. Render will build and deploy the application.

After deployment, verify:

- Homepage loads correctly.
- `/healthz` returns `OK`.
- Static assets load correctly.
- Admin login page loads correctly.

### Important Notes

- Render's free service filesystem is ephemeral. Local SQLite data can be lost when the service restarts or redeploys.
- `DEMO_MODE=true` does not provide persistent database storage. Use a persistent database solution if you need to retain enquiries and admin data.
- Check Render's current plan limitations before deploying.
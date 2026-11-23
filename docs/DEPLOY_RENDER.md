# Deploying LUMINA to Render (Free Tier)

## Prerequisites
- A free [Render](https://render.com/) account connected to your GitHub repository (`Kristoff-iwnl/lumina-studio`).

## Step-by-Step Deployment Guide

1. **Create Web Service:**
   - In your Render Dashboard, click **New +** and select **Web Service**.
   - Connect your GitHub repository (`Kristoff-iwnl/lumina-studio`).

2. **Configure Service Settings:**
   - **Name:** `lumina-studio`
   - **Environment:** `Python 3`
   - **Build Command:** 
     ```bash
     pip install -r lumina/requirements.txt && flask --app lumina.wsgi db upgrade
     ```
   - **Start Command:** 
     ```bash
     gunicorn --workers 1 --threads 4 --bind 0.0.0.0:$PORT wsgi:app
     ```
   - **Plan:** Free

3. **Environment Variables:**
   Add the following environment variables in the Render dashboard:
   - `APP_ENV` = `production`
   - `SECRET_KEY` = *(Click Generate or enter a 32+ character secure key)*
   - `DEMO_MODE` = `true` *(Recommended for free tier since local filesystem is ephemeral)*
   - `FRONTEND_VARIANT` = `cinematic`
   - `ADMIN_LOGIN_VARIANT` = `signal`
   - `TRUSTED_PROXY_COUNT` = `1`
   - `SITE_URL` = `https://your-render-app-url.onrender.com`

4. **Deploy:**
   Click **Create Web Service**. Render will build and deploy your application automatically. The built-in health check (`/healthz`) will monitor uptime.

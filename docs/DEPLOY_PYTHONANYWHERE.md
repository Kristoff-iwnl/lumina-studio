# Deploying LUMINA to PythonAnywhere (Free Tier)

## Prerequisites
- A free [PythonAnywhere](https://www.pythonanywhere.com/) account.
- Note: PythonAnywhere free tier blocks outbound internet requests except to a whitelist of API endpoints.

## Step-by-Step Deployment Guide

1. **Clone Repository & Setup Virtual Environment:**
   Open a Bash console in PythonAnywhere and clone your repository:
   ```bash
   git clone https://github.com/Kristoff-iwnl/lumina-studio.git
   cd lumina-studio
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r lumina/requirements.txt
   ```

2. **Initialize Database & Create Admin:**
   ```bash
   export FLASK_APP=lumina.wsgi
   export APP_ENV=production
   export SECRET_KEY=your_secure_random_key_of_at_least_32_characters
   flask db upgrade
   flask create-admin
   ```

3. **Configure WSGI Web App:**
   - Go to the **Web** tab in your PythonAnywhere dashboard and add a new web app (choose Flask, Python 3.12).
   - Set the source code path to: `/home/yourusername/lumina-studio`
   - Set the virtual environment path to: `/home/yourusername/lumina-studio/venv`
   - Click on the WSGI configuration file link (`/var/www/yourusername_pythonanywhere_com_wsgi.py`) and replace its contents with:
     ```python
     import sys
     import os

     path = '/home/yourusername/lumina-studio'
     if path not in sys.path:
         sys.path.append(path)

     os.environ['APP_ENV'] = 'production'
     os.environ['SECRET_KEY'] = 'your_secure_random_key_of_at_least_32_characters'
     os.environ['DATABASE_URL'] = 'sqlite:////home/yourusername/lumina-studio/instance/app.db'

     from wsgi import app as application
     ```

4. **Configure Static Files:**
   In the PythonAnywhere **Web** tab, map static files:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/lumina-studio/lumina/app/static/`

5. **Reload Web App:**
   Click the **Reload** button at the top of the Web tab. Your site is now live!

*Note: PythonAnywhere free accounts require you to click a "Re-enable" button every 3 months to keep the web app active.*

# Deploying LUMINA to PythonAnywhere

This guide covers deploying LUMINA on PythonAnywhere using Python 3.12 and a virtual environment.

## 1. Prerequisites

- A PythonAnywhere account.
- Your GitHub repository: [lumina-studio](https://github.com/Kristoff-iwnl/lumina-studio).
- Python 3.12 support on your PythonAnywhere account.

## 2. Clone the Repository

Open a Bash console on PythonAnywhere:

```bash
git clone https://github.com/Kristoff-iwnl/lumina-studio.git
cd ~/lumina-studio
```

If the repository already exists, navigate to it and pull the latest changes:

```bash
cd ~/lumina-studio
git pull origin deploy/ready
```

## 3. Create a Virtual Environment

Create a Python 3.12 virtual environment:

```bash
mkvirtualenv --python=/usr/bin/python3.12 lumina312
```

Activate it whenever you open a new console:

```bash
workon lumina312
```

Install dependencies:

```bash
pip install -r ~/lumina-studio/lumina/requirements.txt
```

## 4. Initialize the Database

Navigate to the application directory:

```bash
cd ~/lumina-studio/lumina
```

Run database migrations:

```bash
flask --app wsgi db upgrade
```

Create the first administrator account:

```bash
flask --app wsgi create-admin
```

Follow the prompts to enter your administrator email and password.

## 5. Configure the Web Application

In your PythonAnywhere dashboard:

1. Open the Web tab.
2. Create a new web application.
3. Select Manual Configuration.
4. Choose Python 3.12.
5. Set the source code directory to:

```text
/home/yourusername/lumina-studio
```

6. Set the virtual environment to:

```text
/home/yourusername/.virtualenvs/lumina312
```

Replace `yourusername` with your actual PythonAnywhere username.

## 6. Configure the WSGI File

Open the WSGI configuration file linked in the Web tab.

Use the following structure, replacing the username and secret key with your own values:

```python
import os
import sys

project_path = "/home/yourusername/lumina-studio"
app_path = os.path.join(project_path, "lumina")

if app_path not in sys.path:
    sys.path.insert(0, app_path)

os.environ["APP_ENV"] = "production"
os.environ["SECRET_KEY"] = "YOUR_SECURE_SECRET_KEY"
os.environ["DATABASE_URL"] = (
    "sqlite:////home/yourusername/lumina-studio/"
    "lumina/instance/lumina.db"
)
os.environ["SITE_URL"] = "https://yourusername.pythonanywhere.com"
os.environ["TRUSTED_PROXY_COUNT"] = "1"

from wsgi import app as application
```

Important:
- Use a strong, unique secret key of at least 32 characters.
- Never commit production secrets to GitHub.
- Keep the database path consistent with the actual application configuration.

## 7. Configure Static Files

In the Web tab, add a static files mapping:

| URL | Directory |
|---|---|
| `/static/` | `/home/yourusername/lumina-studio/lumina/app/static/` |

Replace `yourusername` with your PythonAnywhere username.

## 8. Reload and Verify

Click Reload in the Web tab.

Check the following:

- Homepage loads correctly.
- Admin login works.
- Admin dashboard loads.
- Enquiry submissions work.
- Static images, CSS, and JavaScript load correctly.
- `/healthz` returns `200 OK`.

If something goes wrong, inspect the error log from the Web tab.

## 9. Database Backups

The default SQLite database is located at:

```text
lumina/instance/lumina.db
```

Refer to [BACKUP.md](BACKUP.md) for backup and restore instructions.

## 10. Important Production Notes

- Keep production secrets outside the public repository.
- Back up the SQLite database regularly.
- Monitor application error logs.
- Configure a persistent database strategy before using the application for real client data.
- PythonAnywhere free accounts have hosting and outbound network limitations. Check the current PythonAnywhere documentation for plan-specific restrictions.
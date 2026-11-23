# SQLite Backup & Restore Guide

## 1. Safety & Architecture
LUMINA uses SQLite stored at `instance/app.db`. Because SQLite is a file-based database, backing up and restoring is simple, fast, and does not require complex database server daemons.

## 2. Backup Procedure (Safe Online Backup)
To create a safe backup of the active SQLite database while the application is running (without locking or stopping the server):

```bash
# Using SQLite command-line tool
sqlite3 instance/app.db ".backup instance/app_backup_$(date +%Y%m%d_%H%M%S).db"
```

Alternatively, you can copy the database file directly when no write transactions are active:
```bash
cp instance/app.db instance/app_backup.db
```

## 3. Restore Procedure
To restore the database from a backup file:
```bash
# Stop the application server
# Replace active database with backup
cp instance/app_backup.db instance/app.db
# Restart the application server
```

## 4. Hosting Note (Ephemeral Filesystem Warning)
**Warning for Render Free Tier / Ephemeral Hosts:**
Render and similar free-tier hosting providers use ephemeral filesystems. Any local changes made to SQLite (`instance/app.db`) — such as admin edits or client enquiries — may be reset on server restarts or redeploys. 
- For permanent production workloads, configure a persistent disk mount on Render or migrate to PostgreSQL (`DATABASE_URL=postgresql://...`).
- When running in `DEMO_MODE=true`, sample data and demo enquiries are automatically re-seeded on startup if the database is empty.

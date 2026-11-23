# SQLite Backup & Restore Guide

## 1. Database Location

LUMINA uses SQLite as its default database.

The default database location, relative to the repository root, is:

```text
lumina/instance/lumina.db
```

If `DATABASE_URL` is configured through an environment variable, the application will use that database location instead.

## 2. Creating a Backup

SQLite provides a backup command that can safely create a consistent backup while the database is in use.

Run this from the repository root:

```bash
sqlite3 lumina/instance/lumina.db ".backup 'lumina/instance/lumina_backup.db'"
```

For a timestamped backup:

```bash
sqlite3 lumina/instance/lumina.db ".backup 'lumina/instance/lumina_backup_$(date +%Y%m%d_%H%M%S).db'"
```

Keep backups somewhere safe and separate from the live application.

Do not commit database files or backups to the public GitHub repository.

## 3. Restoring a Backup

Before restoring:

1. Stop or temporarily disable the application.
2. Keep a copy of the current database in case the restore needs to be reversed.
3. Verify that the backup file is valid.

Restore the backup from the repository root:

```bash
cp lumina/instance/lumina_backup.db lumina/instance/lumina.db
```

Restart the application and verify that the website and admin dashboard work correctly.

## 4. Hosting Considerations

Some free hosting providers use ephemeral filesystems. Database changes stored locally may be lost when the service restarts or redeploys.

For persistent production workloads, use a persistent disk or a managed database such as PostgreSQL.

If deploying on an ephemeral filesystem, do not rely on the local SQLite database as permanent storage.
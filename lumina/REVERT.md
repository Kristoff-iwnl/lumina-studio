# Revert Instructions

If any issues arise during the performance pass, you can revert using any of the following methods:

## Method 1: Set Environment Variables to Original
Set `CINEMATIC_ENGINE=original` and `FRONTEND_VARIANT=classic`:
```powershell
$env:CINEMATIC_ENGINE="original"
$env:FRONTEND_VARIANT="classic"
python lumina/wsgi.py
```

## Method 2: Restore from Pre-Perf Backup Zip
Extract the safety backup archive `backups/cinematic-before-perf.zip` into the project root directory:
```powershell
Expand-Archive -Path "backups/cinematic-before-perf.zip" -DestinationPath "." -Force
```

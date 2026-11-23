"""
Optimize assets or copy fetched assets from assets_src/ to app/static/cinematic/assets/
with fallback.
"""

import shutil
from pathlib import Path

def optimize_assets():
    src_dir = Path("assets_src")
    dest_dir = Path("app/static/cinematic/assets")
    dest_dir.mkdir(parents=True, exist_ok=True)

    if not src_dir.exists():
        print("assets_src not found. Run fetch_assets.py first.")
        return

    for item in src_dir.iterdir():
        if item.is_file():
            dest_path = dest_dir / item.name
            shutil.copy2(item, dest_path)
            print(f"Copied {item.name} to {dest_path}")

    print("Assets placed in static/cinematic/assets.")

if __name__ == "__main__":
    optimize_assets()

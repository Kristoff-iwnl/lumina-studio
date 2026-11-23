"""
Fetch remote assets for local fallback and record URLs and sha256 hashes in assets.lock.json.
"""

import os
import hashlib
import json
import urllib.request
from pathlib import Path

ASSETS_MAP = {
    "font": "https://dcym8fthxf5uu.cloudfront.net/fonts/247a073c-29f5-4a89-aa3a-741020f346fc/OggText-Medium.woff2",
    "sky": "https://raft-blast-61784561.figma.site/_assets/v11/16b5007d9c93971e26ffe4e0e3e37946f6bd538c.png",
    "back_four": "https://raft-blast-61784561.figma.site/_assets/v11/8a7f8af50e0ce92ec2e228e7b0b4112178c51cf1.png",
    "bazaar": "https://raft-blast-61784561.figma.site/_assets/v11/864afe00e41e2fa20a5aa546e15cb807e0f81384.png",
    "split_left": "https://raft-blast-61784561.figma.site/_assets/v11/7536d7b60a1fce482cf6edf3f0bffd3bad5d0f8a.png",
    "split_right": "https://raft-blast-61784561.figma.site/_assets/v11/392db6a6a6b98e868bd7f8d3f55bb719d51e5028.png",
    "bridge": "https://raft-blast-61784561.figma.site/_assets/v11/c6a6d8ef49bca43f708aa852692942c45ec950d4.png",
    "frame_two": "https://raft-blast-61784561.figma.site/_assets/v11/ba75252bab2b1c510987b74837770f7bc8a6b2d4.png",
    "icon1": "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260730_230438_d526b8b6-8a2e-4e3b-9993-3908acae03a7.png",
    "icon2": "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260730_230442_140bc25b-b165-4249-904a-f708bff6970e.png",
    "icon3": "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260730_230448_825949c9-ccdb-4857-b4a6-e349eccc9010.png"
}

def fetch_assets():
    src_dir = Path("assets_src")
    src_dir.mkdir(exist_ok=True)
    lock_data = {}

    for name, url in ASSETS_MAP.items():
        print(f"Fetching {name} from {url}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read()
                ext = url.split("?")[0].split(".")[-1]
                filename = f"{name}.{ext}" if not url.endswith(f".{ext}") else os.path.basename(url)
                file_path = src_dir / filename
                with open(file_path, "wb") as f:
                    f.write(content)

                sha256_hash = hashlib.sha256(content).hexdigest()
                lock_data[name] = {
                    "url": url,
                    "local_path": str(file_path),
                    "sha256": sha256_hash
                }
        except Exception as e:
            print(f"Error fetching {name}: {e}")

    with open("assets.lock.json", "w") as f:
        json.dump(lock_data, f, indent=2)
    print("Assets fetched and recorded in assets.lock.json.")

if __name__ == "__main__":
    fetch_assets()

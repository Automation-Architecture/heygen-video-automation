#!/usr/bin/env python3
"""
Fetch available HeyGen avatars and voices, with 24-hour caching.
Only shows custom (user-created) avatars by default. Stock avatars have
human-readable string IDs; custom avatars have 32-char hex UUID IDs.

Usage:
  python3 execution/list_heygen_avatars.py           # custom avatars only, use cache if fresh
  python3 execution/list_heygen_avatars.py --refresh  # force fresh fetch
  python3 execution/list_heygen_avatars.py --all      # include stock avatars
"""

import re
import sys
import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

HEX_UUID_RE = re.compile(r'^[0-9a-f]{32}$')

HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY")
CACHE_PATH = Path(__file__).parent.parent / ".tmp/heygen_catalog.json"
CACHE_TTL_HOURS = 24


def heygen_get(path):
    req = urllib.request.Request(
        f"https://api.heygen.com{path}",
        headers={"X-Api-Key": HEYGEN_API_KEY, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error: HeyGen API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Network error reaching HeyGen: {e.reason}", file=sys.stderr)
        sys.exit(1)


def is_custom_avatar(avatar_id):
    """Custom avatars have 32-char hex UUID IDs. Stock avatars use human-readable string IDs."""
    return bool(HEX_UUID_RE.match(avatar_id))


def fetch_avatars():
    data = heygen_get("/v2/avatars")
    avatars = data.get("data", {}).get("avatars", [])
    seen = set()
    result = []
    for a in avatars:
        avatar_id = a["avatar_id"]
        if avatar_id not in seen:
            seen.add(avatar_id)
            result.append({
                "name": a.get("avatar_name", avatar_id),
                "avatar_id": avatar_id,
                "custom": is_custom_avatar(avatar_id),
            })
    return result


def fetch_voices():
    data = heygen_get("/v2/voices")
    voices = data.get("data", {}).get("voices", [])
    return [
        {
            "name": v.get("name", v.get("voice_id")),
            "voice_id": v["voice_id"],
            "language": v.get("language", ""),
            "gender": v.get("gender", ""),
            # Custom voice clones have no preview_audio; stock voices have an S3 URL
            "custom": v.get("preview_audio") is None,
        }
        for v in voices
    ]


def load_cache():
    if not CACHE_PATH.exists():
        return None
    try:
        catalog = json.loads(CACHE_PATH.read_text())
        cached_at = datetime.fromisoformat(catalog["cached_at"])
        age = datetime.now(timezone.utc) - cached_at
        if age < timedelta(hours=CACHE_TTL_HOURS):
            return catalog
    except (KeyError, ValueError):
        pass
    return None


def save_cache(catalog):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(catalog, indent=2))


def main():
    if not HEYGEN_API_KEY:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    force_refresh = "--refresh" in sys.argv
    show_all = "--all" in sys.argv

    if not force_refresh:
        cached = load_cache()
        if cached:
            print(f"# (from cache, fetched {cached['cached_at']})", file=sys.stderr)
            catalog = cached
        else:
            catalog = None
    else:
        print("# --refresh: forcing fresh fetch from HeyGen API...", file=sys.stderr)
        catalog = None

    if catalog is None:
        print("# Fetching from HeyGen API...", file=sys.stderr)
        avatars = fetch_avatars()
        voices = fetch_voices()
        catalog = {
            "avatars": avatars,
            "voices": voices,
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }
        save_cache(catalog)

    output = dict(catalog)
    if not show_all:
        output["avatars"] = [a for a in catalog["avatars"] if a.get("custom")]
        output["voices"] = [v for v in catalog["voices"] if v.get("custom")]

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

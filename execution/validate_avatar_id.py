#!/usr/bin/env python3
"""
Validate that a HeyGen avatar ID exists on the account.
Checks both standard avatars (avatar_id) and talking photos (talking_photo_id).

Usage: python3 execution/validate_avatar_id.py <avatar_id>

Reads HEYGEN_API_KEY from environment.
Exits 0 if found, 1 if not found or on error.
"""

import json
import os
import sys
import urllib.request
import urllib.error

HEYGEN_BASE = "https://api.heygen.com"


def fetch_catalog(api_key: str) -> tuple[list, list]:
    """Returns (avatars, talking_photos) from /v2/avatars."""
    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/avatars",
        headers={"X-Api-Key": api_key},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HeyGen API returned {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e

    data = body.get("data", {})
    avatars = data.get("avatars", [])
    talking_photos = data.get("talking_photos", [])
    return avatars, talking_photos


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_avatar_id.py <avatar_id>", file=sys.stderr)
        sys.exit(1)

    avatar_id = sys.argv[1].strip()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        avatars, talking_photos = fetch_catalog(api_key)
    except RuntimeError as e:
        print(f"Error fetching catalog: {e}", file=sys.stderr)
        sys.exit(1)

    # Check standard avatars
    avatar_match = next((a for a in avatars if a.get("avatar_id") == avatar_id), None)
    if avatar_match:
        name = avatar_match.get("avatar_name") or "(unnamed)"
        print(f"OK: avatar '{name}' ({avatar_id}) found [standard avatar].")
        sys.exit(0)

    # Check talking photos
    photo_match = next((t for t in talking_photos if t.get("talking_photo_id") == avatar_id), None)
    if photo_match:
        name = photo_match.get("talking_photo_name") or "(unnamed)"
        print(f"OK: avatar '{name}' ({avatar_id}) found [talking photo].")
        sys.exit(0)

    print(
        f"NOT FOUND: avatar ID '{avatar_id}' does not exist on this HeyGen account.\n"
        f"Check the HeyGen dashboard or run execution/list_heygen_avatars.py to see available avatars.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Add additional photos to an existing Photo Avatar Group.

Run this after create_photo_avatar_group.py to add the remaining
source images (max 4 image_keys per call).

Usage:
  python3 execution/add_photos_to_group.py \\
    --group_id <group_id> \\
    --image_keys "image/.../original,image/.../original,..."

Reads HEYGEN_API_KEY from environment.
Prints {"status": "ok", "group_id": "...", "added": N} to stdout on success.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

HEYGEN_BASE = "https://api.heygen.com"
MAX_KEYS_PER_CALL = 4


def add_photos(group_id: str, image_keys: list[str], api_key: str) -> dict:
    """Add image_keys to an existing avatar group."""
    if len(image_keys) > MAX_KEYS_PER_CALL:
        raise ValueError(
            f"Max {MAX_KEYS_PER_CALL} image_keys per call; got {len(image_keys)}. "
            "Split into multiple calls."
        )

    payload = json.dumps({
        "group_id": group_id,
        "image_keys": image_keys,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/photo_avatar/avatar_group/add",
        data=payload,
        headers={
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            response = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HeyGen API returned {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error reaching HeyGen: {e.reason}") from e

    # Check for API-level errors
    if response.get("error"):
        raise RuntimeError(f"API error: {response['error']}")

    return {
        "status": "ok",
        "group_id": group_id,
        "added": len(image_keys),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Add photos to a HeyGen Photo Avatar Group (max 4 per call)"
    )
    parser.add_argument("--group_id", required=True, help="Group ID from create_photo_avatar_group.py")
    parser.add_argument(
        "--image_keys",
        required=True,
        help="Comma-separated image_keys from upload_photo_asset.py",
    )
    args = parser.parse_args()

    keys = [k.strip() for k in args.image_keys.split(",") if k.strip()]
    if not keys:
        print("Error: no image_keys provided", file=sys.stderr)
        sys.exit(1)

    if len(keys) > MAX_KEYS_PER_CALL:
        print(
            f"Error: max {MAX_KEYS_PER_CALL} image_keys per call; got {len(keys)}. "
            "Split into multiple calls.",
            file=sys.stderr,
        )
        sys.exit(1)

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Adding {len(keys)} photo(s) to group {args.group_id} ...", file=sys.stderr)

    try:
        result = add_photos(args.group_id, keys, api_key)
    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Create a Photo Avatar Group in HeyGen (first step of training pipeline).

A group is a container that holds source photos and trains a LoRA model
to give the avatar consistent identity, head motion, and micro-expressions.

Usage:
  python3 execution/create_photo_avatar_group.py \\
    --name "Bob Commentator" \\
    --image_key "image/.../original"

Reads HEYGEN_API_KEY from environment.
Prints {"group_id": "...", "name": "...", "status": "pending"} to stdout on success.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

HEYGEN_BASE = "https://api.heygen.com"


def create_group(name: str, image_key: str, api_key: str) -> dict:
    """Create a photo avatar group with one seed image."""
    payload = json.dumps({
        "name": name,
        "image_key": image_key,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/photo_avatar/avatar_group/create",
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

    data = response.get("data", response)
    # API may return group_id or id — check both
    group_id = data.get("group_id") or data.get("id")
    if not group_id:
        raise RuntimeError(f"No group_id in response: {json.dumps(response)}")

    return {
        "group_id": group_id,
        "name": data.get("name", name),
        "status": data.get("status", "pending"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Create a HeyGen Photo Avatar Group"
    )
    parser.add_argument("--name", required=True, help="Display name for the avatar group")
    parser.add_argument("--image_key", required=True, help="image_key from upload_photo_asset.py")
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Creating avatar group '{args.name}' ...", file=sys.stderr)

    try:
        result = create_group(args.name, args.image_key, api_key)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result))


if __name__ == "__main__":
    main()

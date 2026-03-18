#!/usr/bin/env python3
"""
Trigger LoRA training for a HeyGen Photo Avatar Group.

⚠️  COST WARNING: This call costs $4 per invocation. Claude will always
    confirm with the user before running this script.

Training builds a LoRA model from your uploaded photos, enabling:
  - Expressive head motion
  - Micro-expressions
  - Consistent identity across generated looks

Training takes up to 30 minutes. Use poll_avatar_training.py to wait
for completion.

Usage:
  python3 execution/train_photo_avatar_group.py --group_id <group_id>

Reads HEYGEN_API_KEY from environment.
Prints {"status": "training_started", "group_id": "..."} to stdout on success.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

HEYGEN_BASE = "https://api.heygen.com"


def start_training(group_id: str, api_key: str) -> dict:
    """Trigger training for the avatar group. Costs $4."""
    payload = json.dumps({"group_id": group_id}).encode("utf-8")

    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/photo_avatar/train",
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

    if response.get("error"):
        raise RuntimeError(f"API error: {response['error']}")

    return {
        "status": "training_started",
        "group_id": group_id,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Start HeyGen Photo Avatar Group training ($4/call)"
    )
    parser.add_argument("--group_id", required=True, help="Group ID from create_photo_avatar_group.py")
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Starting training for group {args.group_id} ...", file=sys.stderr)
    print("NOTE: Training costs $4. Use poll_avatar_training.py to track progress.", file=sys.stderr)

    try:
        result = start_training(args.group_id, api_key)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result))


if __name__ == "__main__":
    main()

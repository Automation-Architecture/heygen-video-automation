#!/usr/bin/env python3
"""
Poll HeyGen until Photo Avatar Group training completes.

Mirrors poll_heygen_video.py: stderr for progress, stdout for final JSON.

Status progression: in_progress → success | failed

Usage:
  python3 execution/poll_avatar_training.py \\
    --group_id <group_id> \\
    [--interval 30] \\
    [--max_wait 1800]

Reads HEYGEN_API_KEY from environment.
Prints {"status": "success", "group_id": "..."} to stdout on success.
Exits 1 on failure or timeout.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

HEYGEN_BASE = "https://api.heygen.com"


def log(msg: str) -> None:
    """Write progress to stderr so stdout stays clean for JSON output."""
    print(msg, file=sys.stderr, flush=True)


def get_training_status(group_id: str, api_key: str) -> dict | None:
    """Fetch current training status. Returns None on 404."""
    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/photo_avatar/train/status/{group_id}",
        headers={"X-Api-Key": api_key},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HeyGen API error {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error reaching HeyGen: {e.reason}") from e


def poll_training(group_id: str, interval: int, max_wait: int, api_key: str) -> None:
    log(f"Polling training status for group: {group_id}")
    log(f"Interval: {interval}s | Max wait: {max_wait}s ({max_wait // 60} min)")

    deadline = time.time() + max_wait

    while time.time() < deadline:
        try:
            response = get_training_status(group_id, api_key)
        except RuntimeError as e:
            print(json.dumps({"status": "failed", "group_id": group_id, "error": str(e)}))
            sys.exit(1)

        if response is None:
            log(f"  [{datetime.now().strftime('%H:%M:%S')}] status: not found (404) — may still be queued")
            time.sleep(interval)
            continue

        data = response.get("data", response)
        status = data.get("status") or response.get("status")
        log(f"  [{datetime.now().strftime('%H:%M:%S')}] status: {status}")

        if status == "success":
            print(json.dumps({"status": "success", "group_id": group_id}))
            return

        if status == "failed":
            error = data.get("error") or data.get("message") or "unknown error"
            print(json.dumps({"status": "failed", "group_id": group_id, "error": error}))
            sys.exit(1)

        # in_progress or other — keep polling
        time.sleep(interval)

    print(json.dumps({"status": "timeout", "group_id": group_id}))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Poll HeyGen Photo Avatar Group training until complete"
    )
    parser.add_argument("--group_id", required=True, help="Group ID from create_photo_avatar_group.py")
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Polling interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--max_wait",
        type=int,
        default=1800,
        help="Maximum wait time in seconds (default: 1800 = 30 min)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        poll_training(args.group_id, args.interval, args.max_wait, api_key)
    except RuntimeError as e:
        print(json.dumps({"status": "failed", "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()

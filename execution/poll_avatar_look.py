#!/usr/bin/env python3
"""
Poll HeyGen until a Photo Avatar look generation completes.

Mirrors poll_heygen_video.py: stderr for progress, stdout for final JSON.

The response shape for the completed look is undocumented — this script
prints the full `data` dict on success so Claude can identify the look ID
field and update directives/upgrade_photo_avatar.md with the actual field name.

Usage:
  python3 execution/poll_avatar_look.py \\
    --generation_id <generation_id> \\
    [--interval 15] \\
    [--max_wait 600]

Reads HEYGEN_API_KEY from environment.
Prints {"status": "success", "generation_id": "...", "data": {...}} to stdout.
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


def get_look_status(generation_id: str, api_key: str) -> dict | None:
    """Fetch current look generation status. Returns None on 404."""
    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/photo_avatar/generation/{generation_id}",
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


def poll_look(generation_id: str, interval: int, max_wait: int, api_key: str) -> None:
    log(f"Polling look generation: {generation_id}")
    log(f"Interval: {interval}s | Max wait: {max_wait}s")

    deadline = time.time() + max_wait

    while time.time() < deadline:
        try:
            response = get_look_status(generation_id, api_key)
        except RuntimeError as e:
            print(json.dumps({"status": "failed", "generation_id": generation_id, "error": str(e)}))
            sys.exit(1)

        if response is None:
            log(f"  [{datetime.now().strftime('%H:%M:%S')}] status: not found (404) — may still be queued")
            time.sleep(interval)
            continue

        data = response.get("data", response)
        status = data.get("status") or response.get("status")
        log(f"  [{datetime.now().strftime('%H:%M:%S')}] status: {status}")

        if status in ("success", "completed", "done"):
            # Print full data so Claude can identify the look ID field
            log("  SUCCESS — printing full data dict for look ID identification:")
            print(json.dumps({
                "status": "success",
                "generation_id": generation_id,
                "data": data,
            }))
            return

        if status in ("failed", "error"):
            error = data.get("error") or data.get("message") or "unknown error"
            print(json.dumps({
                "status": "failed",
                "generation_id": generation_id,
                "error": error,
            }))
            sys.exit(1)

        # pending / in_progress — keep polling
        time.sleep(interval)

    print(json.dumps({"status": "timeout", "generation_id": generation_id}))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Poll HeyGen Photo Avatar look generation until complete"
    )
    parser.add_argument("--generation_id", required=True, help="generation_id from generate_avatar_look.py")
    parser.add_argument(
        "--interval",
        type=int,
        default=15,
        help="Polling interval in seconds (default: 15)",
    )
    parser.add_argument(
        "--max_wait",
        type=int,
        default=600,
        help="Maximum wait time in seconds (default: 600 = 10 min)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        poll_look(args.generation_id, args.interval, args.max_wait, api_key)
    except RuntimeError as e:
        print(json.dumps({"status": "failed", "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()

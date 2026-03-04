#!/usr/bin/env python3
"""
List HeyGen voices available on this account.

Custom voices (cloned/uploaded) have preview_audio: null.
Stock voices have an S3 preview URL.

Usage:
  python3 execution/list_heygen_voices.py          # custom voices only (default)
  python3 execution/list_heygen_voices.py --all    # all voices

Reads HEYGEN_API_KEY from environment.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

HEYGEN_BASE = "https://api.heygen.com"


def list_voices(api_key):
    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/voices",
        headers={"X-Api-Key": api_key},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HeyGen API returned {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error reaching HeyGen: {e.reason}") from e

    return body.get("data", {}).get("voices", [])


def main():
    parser = argparse.ArgumentParser(description="List HeyGen voices")
    parser.add_argument("--all", action="store_true", help="Show all voices including stock")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of table")
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        voices = list_voices(api_key)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not args.all:
        # Custom voices have preview_audio: null; stock voices have an S3 URL
        voices = [v for v in voices if v.get("preview_audio") is None]
        label = f"Custom/team voices ({len(voices)} found — note: some may belong to other team members and be inaccessible)"
    else:
        label = f"All voices ({len(voices)} found)"

    if args.json:
        print(json.dumps(voices, indent=2))
        return

    print(f"# {label}\n")
    if not voices:
        print("  (none found)")
        return

    # Print table
    print(f"  {'voice_id':<36}  {'name':<30}  {'gender':<8}  {'language':<12}  preview_audio")
    print(f"  {'-'*36}  {'-'*30}  {'-'*8}  {'-'*12}  {'-'*20}")
    for v in voices:
        vid = v.get("voice_id", "—")
        name = (v.get("display_name") or v.get("name") or "—")[:30]
        gender = v.get("gender", "—")[:8]
        lang = (v.get("language") or v.get("locale") or "—")[:12]
        preview = v.get("preview_audio") or "(none)"
        print(f"  {vid:<36}  {name:<30}  {gender:<8}  {lang:<12}  {preview}")


if __name__ == "__main__":
    main()

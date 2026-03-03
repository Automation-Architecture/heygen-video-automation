#!/usr/bin/env python3
"""
Submit a video to HeyGen Video Agent and return the video_id.
Usage: python3 execution/generate_heygen_video.py --prompt "<text>" --avatar_id "<id>" [--orientation portrait|landscape]

Reads HEYGEN_API_KEY from environment.
Prints {"video_id": "<id>"} to stdout on success.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

HEYGEN_BASE = "https://api.heygen.com"


def generate_video(prompt: str, avatar_id: str, orientation: str, api_key: str) -> str:
    payload = json.dumps({
        "prompt": prompt,
        "config": {
            "avatar_id": avatar_id,
            "orientation": orientation,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v1/video_agent/generate",
        data=payload,
        headers={
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HeyGen API returned {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error reaching HeyGen: {e.reason}") from e

    video_id = body.get("data", {}).get("video_id")
    if not video_id:
        raise RuntimeError(f"no video_id in response: {json.dumps(body)}")

    return video_id


def main():
    parser = argparse.ArgumentParser(description="Submit a HeyGen Video Agent job")
    parser.add_argument("--prompt", required=True, help="Full video prompt text")
    parser.add_argument("--avatar_id", required=True, help="HeyGen custom avatar UUID")
    parser.add_argument("--orientation", default="portrait", choices=["portrait", "landscape"],
                        help="Video orientation (default: portrait)")
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        video_id = generate_video(args.prompt, args.avatar_id, args.orientation, api_key)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"video_id": video_id}))


if __name__ == "__main__":
    main()

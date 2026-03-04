#!/usr/bin/env python3
"""
Submit a video to HeyGen V2 generate endpoint (fast path: ~1 min render).

Supports both avatar types:
  - Standard avatar (Jeff): --avatar_type avatar
  - Talking photo (Bob, Bud, Pro Golfer, Cart Girl): --avatar_type talking_photo

Uses Avatar IV motion engine by default (use --no_avatar_iv to disable).

Usage:
  python3 execution/generate_heygen_video_v2.py \\
    --avatar_id <id> \\
    --avatar_type (avatar|talking_photo) \\
    --voice_id <id> \\
    --script "Your spoken script text here" \\
    [--orientation portrait|landscape] \\
    [--no_avatar_iv]

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

DIMENSIONS = {
    "portrait": {"width": 1080, "height": 1920},
    "landscape": {"width": 1920, "height": 1080},
}


def generate_video(avatar_id, avatar_type, voice_id, script, orientation, use_avatar_iv, api_key):
    if avatar_type == "talking_photo":
        character = {
            "type": "talking_photo",
            "talking_photo_id": avatar_id,
        }
    else:
        character = {
            "type": "avatar",
            "avatar_id": avatar_id,
        }

    payload_dict = {
        "video_inputs": [
            {
                "character": character,
                "voice": {
                    "type": "text",
                    "voice_id": voice_id,
                    "input_text": script,
                },
            }
        ],
        "dimension": DIMENSIONS[orientation],
    }

    if use_avatar_iv:
        payload_dict["use_avatar_iv_model"] = True

    payload = json.dumps(payload_dict).encode("utf-8")

    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/video/generate",
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

    # V2 API returns {"data": {"video_id": "..."}, "error": null}
    video_id = (
        body.get("data", {}).get("video_id")
        or body.get("video_id")
    )
    if not video_id:
        raise RuntimeError(f"no video_id in response: {json.dumps(body)}")

    return video_id


def main():
    parser = argparse.ArgumentParser(
        description="Submit a HeyGen V2 video job (fast path, ~1 min render)"
    )
    parser.add_argument("--avatar_id", required=True, help="HeyGen avatar UUID")
    parser.add_argument(
        "--avatar_type",
        required=True,
        choices=["avatar", "talking_photo"],
        help="'avatar' for Jeff (standard avatar), 'talking_photo' for the other 4",
    )
    parser.add_argument("--voice_id", required=True, help="HeyGen voice UUID")
    parser.add_argument("--script", required=True, help="The spoken script text")
    parser.add_argument(
        "--orientation",
        default="portrait",
        choices=["portrait", "landscape"],
        help="Video orientation (default: portrait)",
    )
    parser.add_argument(
        "--no_avatar_iv",
        action="store_true",
        help="Disable Avatar IV motion engine (fall back to standard engine)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    use_avatar_iv = not args.no_avatar_iv

    try:
        video_id = generate_video(
            avatar_id=args.avatar_id,
            avatar_type=args.avatar_type,
            voice_id=args.voice_id,
            script=args.script,
            orientation=args.orientation,
            use_avatar_iv=use_avatar_iv,
            api_key=api_key,
        )
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"video_id": video_id}))


if __name__ == "__main__":
    main()

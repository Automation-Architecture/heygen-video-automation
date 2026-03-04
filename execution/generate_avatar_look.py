#!/usr/bin/env python3
"""
Generate a new look (appearance) from a trained Photo Avatar Group.

⚠️  COST WARNING: This call costs $1 per invocation. Claude will always
    confirm with the user before running this script.

A "look" is a generated photorealistic appearance for your avatar. The
resulting look ID is what you pass to generate_heygen_video_v2.py as
the talking_photo_id for video generation.

IMPORTANT: The prompt MUST include the word "Avatar" (HeyGen requirement).

Usage:
  python3 execution/generate_avatar_look.py \\
    --group_id <group_id> \\
    --prompt "Avatar in broadcast studio, professional attire, front-facing" \\
    [--orientation square] \\
    [--pose half_body] \\
    [--style Realistic]

Reads HEYGEN_API_KEY from environment.
Prints {"generation_id": "..."} to stdout on success.
Use poll_avatar_look.py to wait for completion and retrieve the look ID.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

HEYGEN_BASE = "https://api.heygen.com"


def generate_look(
    group_id: str,
    prompt: str,
    orientation: str,
    pose: str,
    style: str,
    api_key: str,
) -> str:
    """Generate a look from a trained avatar group. Costs $1."""
    if "avatar" not in prompt.casefold():
        raise ValueError(
            "Prompt must include the word 'Avatar' (HeyGen API requirement). "
            "Add 'Avatar' anywhere in the prompt text."
        )

    payload = json.dumps({
        "group_id": group_id,
        "prompt": prompt,
        "orientation": orientation,
        "pose": pose,
        "style": style,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v2/photo_avatar/look/generate",
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

    data = response.get("data", response)
    generation_id = data.get("generation_id") or data.get("id")
    if not generation_id:
        raise RuntimeError(f"No generation_id in response: {json.dumps(response)}")

    return generation_id


def main():
    parser = argparse.ArgumentParser(
        description="Generate a look from a trained HeyGen Photo Avatar Group ($1/call)"
    )
    parser.add_argument("--group_id", required=True, help="Trained group ID")
    parser.add_argument(
        "--prompt",
        required=True,
        help="Description of the look. Must include the word 'Avatar'.",
    )
    parser.add_argument(
        "--orientation",
        default="square",
        choices=["square", "portrait", "landscape"],
        help="Image orientation (default: square)",
    )
    parser.add_argument(
        "--pose",
        default="half_body",
        choices=["half_body", "close_up", "full_body"],
        help="Avatar pose (default: half_body)",
    )
    parser.add_argument(
        "--style",
        default="Realistic",
        help="Visual style (default: Realistic)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Generating look for group {args.group_id} ...", file=sys.stderr)
    print("NOTE: Look generation costs $1. Use poll_avatar_look.py to retrieve the look ID.", file=sys.stderr)

    try:
        generation_id = generate_look(
            group_id=args.group_id,
            prompt=args.prompt,
            orientation=args.orientation,
            pose=args.pose,
            style=args.style,
            api_key=api_key,
        )
    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"generation_id": generation_id}))


if __name__ == "__main__":
    main()

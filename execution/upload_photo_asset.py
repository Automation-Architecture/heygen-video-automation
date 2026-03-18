#!/usr/bin/env python3
"""
Upload a photo asset to HeyGen for use in Photo Avatar creation.

This is the only script in this project that uses multipart/form-data
(manual CRLF boundary construction — no JSON body).

Usage:
  python3 execution/upload_photo_asset.py --file .tmp/bob_photos/bob_01.jpg

Reads HEYGEN_API_KEY from environment.
Prints {"image_key": "image/.../original"} to stdout on success.
"""

import argparse
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error
import uuid

HEYGEN_BASE = "https://api.heygen.com"


def build_multipart(file_path: str) -> tuple[bytes, str]:
    """Build multipart/form-data body manually (CRLF required by spec)."""
    boundary = uuid.uuid4().hex
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        file_data = f.read()

    CRLF = b"\r\n"
    parts = []
    parts.append(f"--{boundary}".encode())
    parts.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
    parts.append(f"Content-Type: {content_type}".encode())
    parts.append(b"")
    parts.append(file_data)
    parts.append(f"--{boundary}--".encode())

    body = CRLF.join(parts) + CRLF
    ct_header = f"multipart/form-data; boundary={boundary}"
    return body, ct_header


def upload_asset(file_path: str, api_key: str) -> str:
    """Upload file to /v1/asset and return image_key."""
    body, content_type = build_multipart(file_path)

    req = urllib.request.Request(
        f"{HEYGEN_BASE}/v1/asset",
        data=body,
        headers={
            "X-Api-Key": api_key,
            "Content-Type": content_type,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            response = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HeyGen API returned {e.code}: {body_text}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error reaching HeyGen: {e.reason}") from e

    # API returns {"data": {"url": "...", "key": "image/.../original"}, "error": null}
    image_key = (
        response.get("data", {}).get("key")
        or response.get("key")
    )
    if not image_key:
        raise RuntimeError(f"No image_key in response: {json.dumps(response)}")

    return image_key


def main():
    parser = argparse.ArgumentParser(
        description="Upload a photo asset to HeyGen (returns image_key)"
    )
    parser.add_argument("--file", required=True, help="Path to image file (jpg/png/webp)")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Uploading {args.file} ...", file=sys.stderr)

    try:
        image_key = upload_asset(args.file, api_key)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"image_key": image_key}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Poll HeyGen for the most recently submitted video and return its URL when ready.
Usage: python3 execution/poll_heygen_video.py [video_id]
  - If video_id is provided, polls that specific video
  - If not, polls the most recently created video in the account
"""

import sys
import time
import os
import json
import urllib.request
import urllib.error
from datetime import datetime

POLL_INTERVAL = 15   # seconds between checks
MAX_WAIT = 1800      # 30 minutes max (queue can be slow; confirmed videos render 12–30 min after submission)


def log(msg):
    """Write progress messages to stderr so stdout stays clean for JSON output."""
    print(msg, file=sys.stderr, flush=True)


def heygen_get(path, api_key):
    req = urllib.request.Request(
        f"https://api.heygen.com{path}",
        headers={"X-Api-Key": api_key}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # Video Agent videos may 404 for 12–30 min while queued
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HeyGen API error {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error reaching HeyGen: {e.reason}") from e


def get_latest_video_id(api_key):
    log("# No video_id provided — fetching most recent video from account.")
    log("# Note: if the video was just submitted, it may not appear yet. Wait a few seconds and retry if needed.")
    data = heygen_get("/v1/video.list?limit=1", api_key)
    videos = data.get("data", {}).get("videos", [])
    if not videos:
        raise RuntimeError("No videos found in HeyGen account")
    return videos[0]["video_id"]


def poll_video(video_id, api_key):
    log(f"Polling HeyGen for video: {video_id}")
    deadline = time.time() + MAX_WAIT

    while time.time() < deadline:
        try:
            data = heygen_get(f"/v1/video_status.get?video_id={video_id}", api_key)
        except RuntimeError as e:
            print(json.dumps({"status": "failed", "video_id": video_id, "error": str(e)}))
            sys.exit(1)

        if data is None:
            log(f"  [{datetime.now().strftime('%H:%M:%S')}] status: indexing (404 — normal for Video Agent; V2 videos should not 404, retrying...)")
            time.sleep(POLL_INTERVAL)
            continue

        status = data.get("data", {}).get("status")
        log(f"  [{datetime.now().strftime('%H:%M:%S')}] status: {status}")

        if status == "completed":
            video_url = data.get("data", {}).get("video_url")
            if not video_url:
                print(json.dumps({"status": "failed", "video_id": video_id, "error": "completed but no video_url in response"}))
                sys.exit(1)
            print(json.dumps({
                "status": "completed",
                "video_id": video_id,
                "video_url": video_url
            }))
            return

        if status == "failed":
            error = data.get("data", {}).get("error", "unknown error")
            print(json.dumps({"status": "failed", "video_id": video_id, "error": error}))
            sys.exit(1)

        time.sleep(POLL_INTERVAL)

    print(json.dumps({"status": "timeout", "video_id": video_id}))
    sys.exit(1)


if __name__ == "__main__":
    HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY")
    if not HEYGEN_API_KEY:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        video_id = sys.argv[1] if len(sys.argv) > 1 else get_latest_video_id(HEYGEN_API_KEY)
        poll_video(video_id, HEYGEN_API_KEY)
    except RuntimeError as e:
        print(json.dumps({"status": "failed", "error": str(e)}))
        sys.exit(1)

#!/usr/bin/env python3
"""
Poll a GitHub PR until Copilot posts a review comment, then trigger auto-fix.

Polls the PR comments endpoint every --interval seconds. When a comment from
Copilot is found (login contains "copilot"), posts "@Copilot fix" as a new
PR comment to trigger Copilot's auto-fix workflow.

Usage:
  python3 execution/poll_copilot_review.py \\
    --repo Automation-Architecture/heygen-video-automation \\
    --pr 3 \\
    [--interval 30] \\
    [--max_wait 1800]

Requires: gh CLI authenticated (uses `gh api` for all calls).
Prints {\"status\": \"fix_requested\", \"comment_id\": ...} to stdout on success.
Exits 1 on timeout or error.
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def gh_api(path: str) -> list | dict:
    result = subprocess.run(
        ["gh", "api", path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh api {path} failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def post_comment(repo: str, pr: int, body: str) -> int:
    """Post a comment on the PR. Returns the new comment ID."""
    owner, name = repo.split("/")
    result = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/issues/{pr}/comments",
            "--method", "POST",
            "--raw-field", f"body={body}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to post comment: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    return data["id"]


def find_copilot_comment(repo: str, pr: int) -> dict | None:
    """Return the first PR comment whose author login contains 'copilot', or None."""
    comments = gh_api(f"repos/{repo}/issues/{pr}/comments")
    for comment in comments:
        login = comment.get("user", {}).get("login", "").lower()
        if "copilot" in login:
            return comment
    return None


def poll(repo: str, pr: int, interval: int, max_wait: int) -> None:
    log(f"Polling PR #{pr} in {repo} for Copilot review comment")
    log(f"Interval: {interval}s | Max wait: {max_wait}s")

    deadline = time.time() + max_wait

    while time.time() < deadline:
        try:
            comment = find_copilot_comment(repo, pr)
        except RuntimeError as e:
            print(json.dumps({"status": "failed", "error": str(e)}))
            sys.exit(1)

        if comment:
            log(f"  [{datetime.now().strftime('%H:%M:%S')}] Copilot comment found (id={comment['id']})")
            log("  Posting @Copilot fix ...")
            try:
                fix_comment_id = post_comment(repo, pr, "@copilot open a new pull request to apply changes based on the comments in this thread")
            except RuntimeError as e:
                print(json.dumps({"status": "failed", "error": str(e)}))
                sys.exit(1)

            print(json.dumps({
                "status": "fix_requested",
                "pr": pr,
                "copilot_comment_id": comment["id"],
                "fix_comment_id": fix_comment_id,
            }))
            return

        log(f"  [{datetime.now().strftime('%H:%M:%S')}] No Copilot comment yet — waiting {interval}s")
        time.sleep(interval)

    print(json.dumps({"status": "timeout", "pr": pr}))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Poll GitHub PR for Copilot review comment, then post @Copilot fix"
    )
    parser.add_argument("--repo", required=True, help="owner/repo (e.g. Automation-Architecture/heygen-video-automation)")
    parser.add_argument("--pr", required=True, type=int, help="PR number")
    parser.add_argument("--interval", type=int, default=30, help="Poll interval in seconds (default: 30)")
    parser.add_argument("--max_wait", type=int, default=1800, help="Max wait in seconds (default: 1800 = 30 min)")
    args = parser.parse_args()

    try:
        poll(args.repo, args.pr, args.interval, args.max_wait)
    except RuntimeError as e:
        print(json.dumps({"status": "failed", "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()

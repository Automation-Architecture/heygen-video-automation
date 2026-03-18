# Execution Scripts

Deterministic Python scripts that handle API calls, polling, and file operations. All scripts use Python standard library only (no pip installs required).

Every script reads `HEYGEN_API_KEY` from the environment via `os.environ.get()`.

## Video Generation

| Script | Purpose |
|--------|---------|
| `generate_heygen_video_v2.py` | Fast path (~1 min) — V2 endpoint + Avatar IV engine |
| `generate_heygen_video.py` | Cinematic path (12–30 min) — Video Agent endpoint |
| `poll_heygen_video.py` | Poll for video completion, return playable URL (handles 404 gracefully) |

## Avatar & Voice Discovery

| Script | Purpose |
|--------|---------|
| `validate_avatar_id.py` | Confirm avatar ID exists on the HeyGen account |
| `list_heygen_avatars.py` | Fetch and cache available avatars (24-hour TTL) |
| `list_heygen_voices.py` | List available voices — custom and stock |

## Photo Avatar Pipeline

Used to upgrade talking photos to trained Photo Avatars with Avatar IV motion.

| Script | Purpose |
|--------|---------|
| `upload_photo_asset.py` | Upload photo to HeyGen (multipart form-data) |
| `create_photo_avatar_group.py` | Create Photo Avatar Group container |
| `add_photos_to_group.py` | Add photos to existing group (up to 4 per call) |
| `train_photo_avatar_group.py` | Trigger LoRA training ($4/call) |
| `poll_avatar_training.py` | Poll until training completes |
| `generate_avatar_look.py` | Generate photorealistic look from trained group ($1/call) |
| `poll_avatar_look.py` | Poll until look generation completes |

## GitHub Automation

| Script | Purpose |
|--------|---------|
| `poll_copilot_review.py` | Poll PR for Copilot review, then post auto-fix request |

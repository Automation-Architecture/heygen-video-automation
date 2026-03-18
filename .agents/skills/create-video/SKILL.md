---
name: create-video
description: Create a HeyGen avatar video for Golfers Unite. Use when the user says "make a video", "create a video", "generate a social post", "create an avatar video", "I want a Jeff video", "film a video", or any variant asking to produce a GU avatar video with or without a topic hint. Do NOT use for general video editing, YouTube uploads, or non-HeyGen video tasks.
---

# Create Avatar Video

Read and follow `directives/create_avatar_video.md` in full, starting at Step 0.

## Topic Hint

If the user provided a topic in their message, use it as the starting topic for script research in Step 1 (pass it to the web search query instead of searching generically). Still present the avatar menu first before doing any research.

If no topic was provided, proceed with the standard workflow — search for the next upcoming PGA Tour event.

## Reminders

- Always present the avatar menu (Step 0) and wait for selection before any script work.
- Use web search for tournament research (Exa MCP if available, otherwise standard web search).
- Do not proceed past Step 0 without explicit user confirmation of the avatar choice.
- The full workflow, avatar IDs, persona templates, and visual prompts are in `directives/`.

## Execution Scripts

All scripts live in `execution/` and are called via bash with `HEYGEN_API_KEY` from `.env`:

| Script | Purpose |
|--------|---------|
| `execution/validate_avatar_id.py` | Validate avatar exists on HeyGen account |
| `execution/generate_heygen_video_v2.py` | Fast path (~1 min) — V2 + Avatar IV engine |
| `execution/generate_heygen_video.py` | Cinematic path (12-30 min) — Video Agent |
| `execution/poll_heygen_video.py` | Poll for video completion, return URL |
| `execution/list_heygen_voices.py` | List available HeyGen voices |

## Avatar Registry

| # | Avatar | ID | Type |
|---|--------|-----|------|
| 1 | Jeff | `ccce0126b55f418e858ce9c7047eff1a` | avatar |
| 2 | Bob Commentator | `7c5124f727b840bdb2fa66380ade0a0f` | talking_photo |
| 3 | Bud The Caddy | `35a38a2bfbfe4d5ea33f1a8b8434aa06` | talking_photo |
| 4 | Pro Golfer | `3c4b06f3ae6b42adb456f7022f4dc9d1` | talking_photo |
| 5 | Golf Cart Girl | `5de5fb82755e4ea198450101ae360c79` | talking_photo |

## Voice IDs (Fast Path Only)

| Avatar | Voice ID | Voice Name |
|--------|----------|------------|
| Jeff | `58aef04cd30741e9ac705f9a6ce0d907` | jeff (cloned) |
| Bob Commentator | `06c816b952f14fa9b3a6c42aa151f731` | William Prescott - Broadcaster |
| Bud The Caddy | `f38a635bee7a4d1f9b0a654a31d050d2` | Chill Brian |
| Pro Golfer | `0f50a7a5577e4cd583ba738094956899` | Marcus - Professional |
| Golf Cart Girl | `084760b4922a44599575c770070ec2d7` | Peppy Stella |

## Render Paths

After avatar selection and script approval, ask the user which render path:

- **Fast (~1 min):** Single talking-head scene. Uses `generate_heygen_video_v2.py` with `--avatar_id`, `--avatar_type`, `--voice_id`, `--script`, `--orientation portrait`.
- **Cinematic (12-30 min):** Multi-scene production (drone open, avatar A-roll, gallery B-roll, branded outro). Uses `generate_heygen_video.py` with `--prompt`, `--avatar_id`, `--orientation portrait`. Prompt must be <= 245 chars total.

## Post-Render

After polling completes with a video URL, post to Slack #crm-uat with the avatar name, topic, and video URL.

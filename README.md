# GU Avatar Video

HeyGen avatar video creation for Golfers Unite, triggered from Claude Code.

## What It Does

You start a conversation in Claude Code, say what video you want (or just say "make a video"), and Claude walks you through the rest:

1. **Pick an avatar** — Claude presents the full roster and asks which character you want
2. **Research + script** — Claude searches for the next PGA Tour event (via Exa), then presents 3 script options with different angles (venue history, player storyline, competitive stakes, etc.)
3. **Pick or refine** — choose one of the 3 options, request tweaks, or provide your own script
4. **Choose your render path** — Fast (talking head, Avatar IV motion, ~1 min) or Cinematic (multi-scene drone + B-roll + branded outro, ~12–30 min)
5. **Get the URL** — Claude returns the video URL when rendering is complete

## Avatars

| # | Avatar | Character | HeyGen ID |
|---|--------|-----------|-----------|
| 1 | **Jeff** | Golfers Unite founder — friendly, direct, like a friend at the clubhouse | `ccce0126b55f418e858ce9c7047eff1a` |
| 2 | **Bob Commentator** | Senior Tour announcer — grave, authoritative, five decades on the mic | `7c5124f727b840bdb2fa66380ade0a0f` |
| 3 | **Bud The Caddy** | Career looper — irreverent, funny, unfiltered | `35a38a2bfbfe4d5ea33f1a8b8434aa06` |
| 4 | **Pro Golfer** | Rookie Tour pro — focused, disciplined, earned his card the hard way | `3c4b06f3ae6b42adb456f7022f4dc9d1` |
| 5 | **Golf Cart Girl** | Beverage cart — playful, punchy, always smirking | `5de5fb82755e4ea198450101ae360c79` |

Each avatar has both a cinematic prompt template (for Video Agent) and a voice ID + motion prompt (for the fast Avatar IV path), all defined in `directives/avatar_personas.md`.

## Prerequisites

- Claude Code
- HeyGen account with API access and the GU custom avatars configured
- Exa API key (for PGA Tour research)

## Setup

### 1. Fill in `.env`

| Variable | Description |
|----------|-------------|
| `HEYGEN_API_KEY` | From HeyGen → Settings → API |
| `EXA_API_KEY` | For PGA Tour tournament research |

## Usage

Open Claude Code in this directory and prompt naturally:

> "Make a video for this week's tournament."

> "Create a Jeff video about The Masters."

> "I want a Bud The Caddy video — here's the script: [text]"

Claude will handle research, script drafting, video triggering, and polling.

## Project Structure

```
directives/
  create_avatar_video.md   # Main SOP: Steps 0–3 (avatar → script → trigger → poll)
  create_script.md         # Sub-directive: Exa research + 3-option script drafting
  avatar_personas.md       # Character profiles, tone guides, visual defaults

execution/
  validate_avatar_id.py          # Confirms avatar ID exists on account
  list_heygen_avatars.py         # Discovers custom avatars, caches 24h
  list_heygen_voices.py          # Lists available voices (custom and stock)
  generate_heygen_video.py       # Cinematic path: submits job to Video Agent, returns video_id
  generate_heygen_video_v2.py    # Fast path: submits V2 job with Avatar IV, returns video_id
  poll_heygen_video.py           # Polls HeyGen until video is ready, prints URL

docs/
  heygen_api.md                          # HeyGen API reference
  heygen-photo-avatar-to-avatar-iv-guide.md  # Upgrade path: talking photos → trained Photo Avatars with Avatar IV

.env                       # API keys (never commit)
.mcp.json                  # Project-scoped MCP config (intentionally empty — defer to ~/.claude/mcp.json)
.tmp/                      # Cache and intermediate files (never committed)
```

## Render Paths

| | Fast Path (Avatar IV / V2) | Cinematic Path (Video Agent) |
|---|---|---|
| Script | `execution/generate_heygen_video_v2.py` | `execution/generate_heygen_video.py` |
| Render time | **~1 min** | 12–30 min |
| Output | Single-scene talking head | Multi-scene: drone open → avatar → B-roll → branded outro |
| Avatar motion | Photorealistic (Avatar IV) | Basic lip-sync (talking photos) |
| Voice | Explicit `voice_id` per avatar | Auto from avatar |
| Prompt | Script text only | Script + cinematic suffix (≤ 245 chars total) |

Both paths use the same `execution/poll_heygen_video.py` for status polling.

## Known Behaviour

- **HeyGen 404 window:** Video Agent videos return 404 for the first several minutes after triggering (normal — still indexing). The polling script retries automatically. V2 fast-path videos do NOT have this 404 window.
- **Render time:** Fast path ~1 min; Video Agent 12–30 min when queue is busy.
- **Video URL expiry:** Pre-signed URLs expire after **7 days** (both paths).
- **Voice selection:** Fast path requires explicit `voice_id` per avatar (see `directives/avatar_personas.md`). Video Agent auto-selects voice from the avatar.
- **Custom voice trap:** The `/v2/voices` API returns custom voices from all team members. Voices with `preview_audio: null` may not be accessible for video generation if they belong to another team member. Jeff's cloned voice is confirmed accessible; all other avatars use stock voices.

## Maintaining This README

This README should stay in sync with `CLAUDE.md` and the directives in `directives/`. When the user flow changes — new avatars, new script steps, API endpoint changes — update this file alongside the relevant directive.

# GU Avatar Video

HeyGen avatar video creation for Golfers Unite, triggered from Claude Code.

## What It Does

You start a conversation in Claude Code, say what video you want (or just say "make a video"), and Claude walks you through the rest:

1. **Pick an avatar** — Claude presents the full roster and asks which character you want
2. **Research + script** — Claude searches for the next PGA Tour event (via Exa), then presents 3 script options with different angles (venue history, player storyline, competitive stakes, etc.)
3. **Pick or refine** — choose one of the 3 options, request tweaks, or provide your own script
4. **Video generation** — Claude fills in the avatar's persona-specific cinematic prompt template with the approved script and venue context (drone opening, avatar A-roll, course B-roll, branded outro — all grounded in the specific tournament venue), calls HeyGen directly via `execution/generate_heygen_video.py`, and starts polling
5. **Get the URL** — Claude returns the video URL when rendering is complete (~5–10 min)

## Avatars

| # | Avatar | Character | HeyGen ID |
|---|--------|-----------|-----------|
| 1 | **Jeff** | Golfers Unite founder — friendly, direct, like a friend at the clubhouse | `ccce0126b55f418e858ce9c7047eff1a` |
| 2 | **Bob Commentator** | Senior Tour announcer — grave, authoritative, five decades on the mic | `924e085127e14867814dc5f99d2f6419` |
| 3 | **Bud The Caddy** | Career looper — irreverent, funny, unfiltered | `35a38a2bfbfe4d5ea33f1a8b8434aa06` |
| 4 | **Pro Golfer** | Rookie Tour pro — focused, disciplined, earned his card the hard way | `1fd5fe07a84749fc88143d0640841d46` |
| 5 | **Golf Cart Girl** | Beverage cart — playful, punchy, always smirking | `fee86c5c0bbe45f7954d2bd31046b6f9` |

Each avatar has a pre-configured voice in HeyGen (no `voice_id` needed) and a full cinematic production template defined in `directives/avatar_personas.md` — 4-scene structure, camera angle direction (drone, low-angle, gallery POV), lighting guidance (natural sunlight, dappled shadows), persona-specific on-course locations, and a venue context slot that gets filled with the specific tournament location for every video.

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
  validate_avatar_id.py       # Confirms avatar ID exists on account (checks avatars + talking photos)
  list_heygen_avatars.py      # Discovers custom avatars/voices, caches 24h
  generate_heygen_video.py    # Submits job to HeyGen Video Agent, returns video_id
  poll_heygen_video.py        # Polls HeyGen until video is ready, prints URL

docs/
  heygen_api.md            # HeyGen API reference

.env                       # API keys (never commit)
.mcp.json                  # Project-scoped MCP config (intentionally empty — defer to ~/.claude/mcp.json)
.tmp/                      # Cache and intermediate files (never committed)
```

## Known Behaviour

- **HeyGen 404 window:** Video Agent videos return 404 for the first ~4 minutes after triggering. The polling script handles this gracefully and retries automatically.
- **Render time:** ~5–10 minutes for short videos (Video Agent does full scene production).
- **Video URL expiry:** Pre-signed URLs from Video Agent expire after **7 days**.
- **Voice selection:** Voices are pre-configured per avatar in HeyGen. Do not pass `voice_id`.

## Maintaining This README

This README should stay in sync with `CLAUDE.md` and the directives in `directives/`. When the user flow changes — new avatars, new script steps, API endpoint changes — update this file alongside the relevant directive.

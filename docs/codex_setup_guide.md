# Codex Setup Guide — GU Avatar Video

How to create Golfers Unite avatar videos using OpenAI Codex (via ChatGPT).

## Prerequisites

- **ChatGPT plan:** Plus, Pro, Business, Edu, or Enterprise
- **HeyGen API key:** From HeyGen → Settings → API
- **GitHub access:** To this repository

## Setup (One-Time)

### 1. Open Codex

Go to [chatgpt.com/codex](https://chatgpt.com/codex) (or click "Codex" in the ChatGPT sidebar).

### 2. Connect the Repository

Click **"New task"** → connect your GitHub account if not already linked → select the **gu-avatar-video** repository.

### 3. Add the HeyGen API Key

1. Open **Codex Settings** (gear icon)
2. Go to **Environments**
3. Add an **environment variable** (not a secret):
   - Name: `HEYGEN_API_KEY`
   - Value: your HeyGen API key

> **Why environment variable and not secret?** Secrets are removed before the agent phase starts. The video generation scripts need `HEYGEN_API_KEY` during agent execution, so it must be an environment variable.

### 4. Verify (Optional)

Run a quick test task:

```
python3 execution/validate_avatar_id.py ccce0126b55f418e858ce9c7047eff1a
```

If it prints Jeff's avatar details, you're good.

## Usage

Start a new Codex task and type any of these:

- `$create-video` — launches the full workflow (avatar menu → script → render)
- `$create-video The Masters 2026` — starts with a specific topic
- `Make a video about this week's PGA Tour event` — implicit trigger
- `I want a Jeff video` — implicit trigger with avatar hint

### What Happens

1. **Pick an avatar** — Codex presents the 5-avatar menu and waits for your choice
2. **Research + script** — Codex searches for PGA Tour event info and drafts 3 script options
3. **Pick or refine** — choose one, tweak it, or provide your own
4. **Choose render path:**
   - **Fast (~1 min)** — single talking-head, photorealistic Avatar IV motion
   - **Cinematic (12–30 min)** — multi-scene: drone open → avatar A-roll → gallery B-roll → branded outro
5. **Get the URL** — Codex returns the video URL when rendering completes

## Avatars

| # | Avatar | Character |
|---|--------|-----------|
| 1 | **Jeff** | GU founder — friendly, direct, clubhouse vibe |
| 2 | **Bob Commentator** | Senior Tour announcer — grave, authoritative |
| 3 | **Bud The Caddy** | Career looper — irreverent, funny, unfiltered |
| 4 | **Pro Golfer** | Rookie Tour pro — confident, focused |
| 5 | **Golf Cart Girl** | Beverage cart — playful, punchy, smirking |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `HEYGEN_API_KEY not set` | Add the key as an environment variable in Codex Settings → Environments |
| Avatar validation fails | Check that the HeyGen account has the GU custom avatars configured |
| Video stuck / 404 for a long time | Normal for cinematic path (12–30 min). Check HeyGen dashboard if it exceeds 30 min |
| Skill not found | Make sure you're running from the repo root. Codex looks for `.agents/skills/` there |

## Notes

- All scripts use Python standard library only — no pip installs required
- Video URLs expire after 7 days
- Fast path renders in ~1 min; cinematic path takes 12–30 min when HeyGen's queue is busy
- The skill and scripts are identical to the Claude Code version — same directives, same execution layer

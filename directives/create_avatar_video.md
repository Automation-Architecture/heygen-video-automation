# Directive: Create Avatar Video

## Goal
Given a topic or script, produce a HeyGen avatar video and return the video URL.

## Inputs
| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `script` | No | Generated in Step 0 | The spoken text for the avatar |
| `avatar_id` | No | User selects in Step 0 | Chosen from known avatar list |
| `orientation` | No | `portrait` | Portrait (9:16) for social; landscape (16:9) for web |
| `title` | No | First 50 chars of script | Used for reference |

Note: `voice_id` is no longer an input. Video Agent determines voice from the avatar automatically. Jeff's custom avatar uses his cloned voice.

## Community Context
This is a golf community. Jeff is the founder. Videos are short, conversational check-ins about upcoming PGA Tour events, tournament news, and community updates. Jeff's tone is friendly, knowledgeable, and direct — like he's talking to a friend at the clubhouse.

## Step 0: Select Avatar

**Always do this first, before any script work.**

Present the user with this list and ask which avatar they want:

| # | Avatar | ID |
|---|--------|-----|
| 1 | Jeff | `185ac6a5133141cdbe5ad30729dfb0b5` |
| 2 | Bob Commentator | `924e085127e14867814dc5f99d2f6419` |
| 3 | Bud The Caddy | `35a38a2bfbfe4d5ea33f1a8b8434aa06` |
| 4 | Pro Golfer | `1fd5fe07a84749fc88143d0640841d46` |
| 5 | Golf Cart Girl | `fee86c5c0bbe45f7954d2bd31046b6f9` |

Ask: "Which avatar would you like to use for this video?"

Wait for the user to confirm before proceeding. Use the selected `avatar_id` in Step 2.

Each avatar has a pre-configured voice in HeyGen — no `voice_id` needed.

## Step 1: Draft the Script (if not provided)

**Recommended path:** Follow `directives/create_script.md` as a sub-directive. It handles
PGA tournament research via Exa and 3-option script drafting with dynamically chosen angles.
Use the persona notes in `directives/avatar_personas.md` for the selected avatar's tone and
visual defaults. When complete, it returns a final `script`.

**Fast path:** If the user provides a script directly, accept it and proceed to Step 2.

**Inline path (fallback only):** If `create_script.md` is unavailable or the user wants
a quick single draft:
1. Use Exa MCP to look up the next upcoming PGA Tour tournament (name, dates, venue)
2. Write ~45 words in the selected avatar's voice from `directives/avatar_personas.md`
3. Present for approval, incorporate feedback, lock in the final script

## Step 2: Build the Prompt and Trigger the Workflow

Use the avatar selected in Step 0 and the approved script from Step 1.

### Building the prompt

Each avatar has a ready-to-use `### Video Agent Prompt` section in `directives/avatar_personas.md`. Find the selected avatar's entry, copy its prompt template verbatim, then make two substitutions:

1. Replace `[INSERT APPROVED SCRIPT HERE]` with the approved script.
2. Replace `[INSERT TOURNAMENT VENUE CONTEXT HERE]` with the `venue_context` from the script handoff (Step 5 of `create_script.md`).

**If no venue context is available** (e.g., user provided a script directly without going through research), use this generic fallback:
> "A PGA Tour venue — manicured fairways, well-groomed bentgrass greens, natural course beauty with galleries lining the holes. Classic parkland feel with sunlight through tree-lined corridors."

The venue context grounds the B-roll and scenery in the specific tournament location. It's what makes Bay Hill look like Bay Hill and Augusta look like Augusta — not a generic course.

### Trigger call

Run the direct HeyGen script. Capture the `video_id` from stdout and pass it to Step 3.

```bash
HEYGEN_API_KEY=<key> python3 execution/generate_heygen_video.py \
  --prompt "<full prompt text built above>" \
  --avatar_id "<avatar_id>" \
  --orientation portrait
```

On success, this prints:
```json
{ "video_id": "<id>" }
```

Extract the `video_id` from that output and use it in Step 3. The script exits non-zero on any error.

## Step 3: Poll for Completion (run immediately after triggering)

After triggering, pass the `video_id` from Step 2 to the polling script:

```bash
HEYGEN_API_KEY=<key> python3 execution/poll_heygen_video.py <video_id>
```

This polls every 15 seconds and prints the video URL when ready.

**Important timing note:** Video Agent videos take ~3–4 minutes before they become queryable.
The polling script handles this gracefully — it will log "indexing (404)" during the initial
window and automatically retry. Total render time is typically 5–10 minutes for short videos.

## Expected Output
```json
{
  "status": "completed",
  "video_id": "<heygen video id>",
  "video_url": "https://files2.heygen.ai/..."
}
```

## Error Cases
- **Rendering failed**: Script exits with status `failed` and the error message.
- **Timeout (>10 min)**: Script exits with `timeout` — check HeyGen dashboard directly.
- **Script trigger fails**: Check `HEYGEN_API_KEY` is set and the avatar_id is a valid HeyGen UUID.

## Notes
- Video Agent rendering typically takes 5–10 minutes (longer than v2 due to scene production)
- Video URLs are pre-signed and expire after 7 days (Video Agent) vs 24 hours (v2)
- Avatar/voice catalog is cached in `.tmp/heygen_catalog.json`; run with `--refresh` to force an update
- Video Agent does not support `voice_id` — voice is determined by the avatar
- Jeff's custom avatar (`185ac6a5133141cdbe5ad30729dfb0b5`) automatically uses his cloned voice

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

Note: `voice_id` is only required for the fast-path (V2) render. Video Agent determines voice from the avatar automatically — no `voice_id` needed for the cinematic path. Voice IDs for all avatars are defined in `directives/avatar_personas.md`.

## Community Context
This is a golf community. Jeff is the founder. Videos are short, conversational check-ins about upcoming PGA Tour events, tournament news, and community updates. Jeff's tone is friendly, knowledgeable, and direct — like he's talking to a friend at the clubhouse.

## Step 0: Select Avatar

**Always do this first, before any script work.**

Present the user with this list and ask which avatar they want:

| # | Avatar | ID | Status |
|---|--------|-----|--------|
| 1 | Jeff | `ccce0126b55f418e858ce9c7047eff1a` | ✓ verified |
| 2 | Bob Commentator | `924e085127e14867814dc5f99d2f6419` | ✓ verified |
| 3 | Bud The Caddy | `35a38a2bfbfe4d5ea33f1a8b8434aa06` | ✓ verified |
| 4 | Pro Golfer | `1fd5fe07a84749fc88143d0640841d46` | ✓ verified |
| 5 | Golf Cart Girl | `fee86c5c0bbe45f7954d2bd31046b6f9` | ✓ verified |

Ask: "Which avatar would you like to use for this video?"

Wait for the user to confirm. Then immediately run **Step 0.5** before any script work.

### Step 0.5: Validate Avatar ID

Run this immediately after the user picks an avatar:

```bash
HEYGEN_API_KEY=<key> python3 execution/validate_avatar_id.py <avatar_id>
```

- **Exit 0 (found):** proceed to Step 1.
- **Exit 1 (not found):** stop. Tell the user the avatar ID is not on their HeyGen account and ask them to verify it in the HeyGen dashboard or pick a different avatar. Do NOT proceed to script work or video generation with an unverified avatar ID.

Use the confirmed `avatar_id` in Step 2.

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

## Step 2: Choose Render Path and Trigger the Workflow

Use the avatar selected in Step 0 and the approved script from Step 1.

**Ask the user which render path they want:**

| | Fast Path (Avatar IV / V2) | Cinematic Path (Video Agent) |
|---|---|---|
| Render time | **~1 min** | 12–30 min |
| Output | Single-scene talking head | Multi-scene: drone open → avatar → B-roll → branded outro |
| Avatar motion | Photorealistic (Avatar IV engine) | Basic lip-sync (talking photos) |
| Voice | Explicit voice_id required | Auto from avatar |

If the user doesn't specify, ask: "Fast (~1 min, single talking head) or Cinematic (12–30 min, multi-scene with B-roll and branded outro)?"

---

### Fast Path: Avatar IV / V2

Each avatar's `Voice ID (fast-path)` and `### Fast-Path (V2) Motion Prompt` are in `directives/avatar_personas.md`.

Pass the approved script verbatim — do **not** append the cinematic suffix.

```bash
HEYGEN_API_KEY=<key> python3 execution/generate_heygen_video_v2.py \
  --avatar_id "<avatar_id>" \
  --avatar_type "<avatar|talking_photo>" \
  --voice_id "<voice_id>" \
  --script "<approved script text>" \
  --orientation portrait
```

Avatar types:
- Jeff → `--avatar_type avatar`
- Bob, Bud, Pro Golfer, Golf Cart Girl → `--avatar_type talking_photo`

On success, prints `{ "video_id": "<id>" }`. Pass to Step 3.

---

### Cinematic Path: Video Agent

**⚠ Hard limit: 245 chars total.** Video Agent silently rejects longer prompts — it returns a `video_id` but the video never renders (persistent 404). Count characters before submitting.

Each avatar has a compact `### Video Agent Prompt` template in `directives/avatar_personas.md`. The template is structured as:

```
[SCRIPT] [CINEMATIC SUFFIX]
```

Where the cinematic suffix (~55–65 chars) encodes the 4-scene structure (B-roll open → avatar A-roll → energy B-roll → branded outro) in a tight phrase. To build the final prompt:

1. Take the approved script and tighten it to fit within the avatar's script budget (total - suffix length). Drop contractions, trim filler, preserve all key facts and the persona's voice.
2. Append the avatar's cinematic suffix verbatim.
3. Count total characters. Must be ≤ 245.

```bash
HEYGEN_API_KEY=<key> python3 execution/generate_heygen_video.py \
  --prompt "<full prompt text built above>" \
  --avatar_id "<avatar_id>" \
  --orientation portrait
```

On success, prints `{ "video_id": "<id>" }`. Pass to Step 3.

## Step 3: Poll for Completion (run immediately after triggering)

After triggering, pass the `video_id` from Step 2 to the polling script:

```bash
HEYGEN_API_KEY=<key> python3 execution/poll_heygen_video.py <video_id>
```

This polls every 15 seconds and prints the video URL when ready.

**Important timing note:** Video Agent rendering takes **12–30 minutes** when the queue is busy.
The polling script handles the initial 404 window gracefully — it logs "indexing (404)" and retries.
Do NOT assume a job failed just because it's still 404 at 10 minutes. The poll script now waits up
to 30 minutes. If it times out, check the HeyGen dashboard or `video.list` — the video may have
rendered after the timeout window.

## Step 4: Notify Slack

After Step 3 completes, post to **#crm-uat** using the Slack MCP.

**On success:**
```
✅ GU Avatar Video Ready
Avatar: <avatar name>
Topic: <topic or first ~50 chars of script>
▶️ <video_url>
```

**On failure or timeout:**
```
❌ GU Avatar Video Failed
Avatar: <avatar name>
Topic: <topic or first ~50 chars of script>
Error: <error message or "timeout — check HeyGen dashboard">
```

Use the `conversations_add_message` tool from the `slack` MCP to post the message to channel `#crm-uat`. The bot must be invited to that channel for the post to succeed.

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
- **Timeout (>30 min)**: Script exits with `timeout` — check HeyGen dashboard directly.
- **Script trigger fails**: Check `HEYGEN_API_KEY` is set and the avatar_id is a valid HeyGen UUID.

## Notes
- **Fast path (V2):** ~1 min render, Avatar IV photorealistic motion, explicit `voice_id` required
- **Cinematic path (Video Agent):** 12–30 min render, multi-scene production (drone + B-roll + outro), voice auto from avatar
- Video URLs expire after 7 days (both paths)
- Video Agent does not support `voice_id` — voice is determined by the avatar
- Voice IDs for all avatars are in `directives/avatar_personas.md`; also discoverable via `execution/list_heygen_voices.py`

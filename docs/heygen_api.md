# HeyGen API Reference

Source: https://docs.heygen.com/docs/quick-start
Last reviewed: 2026-03-03

---

## Authentication

All requests require an API key header:

```
x-api-key: <your HEYGEN_API_KEY>
```

Obtain the token from HeyGen Settings → API section.

---

## Core Capabilities

| Capability | Notes |
|---|---|
| Avatar video generation | Use a custom avatar + voice + script to produce a video |
| Video Agent | Fastest path — text prompt to video, no avatar setup needed |
| Digital Twin creation | Enterprise only — build a high-fidelity avatar from training footage |
| Photo Avatar creation | Build an avatar from a photo |
| Video Translation | Translate an existing video into another language |

---

## Endpoints We Use

### List All Avatars

```
GET https://api.heygen.com/v2/avatars
```

Returns `avatars` (standard/custom) and `talking_photos` arrays.

**Avatar object fields:**
| Field | Type | Notes |
|---|---|---|
| `avatar_id` | string | Use this to generate videos |
| `avatar_name` | string | Display name |
| `gender` | string | |
| `preview_image_url` | string | |
| `preview_video_url` | string | |
| `premium` | boolean | |
| `type` | string | Avatar classification |
| `tags` | array | e.g. `"NEW"`, `"AVATAR_IV"` |
| `default_voice_id` | string | Associated voice |

**Filtering heuristic for custom avatars:** UUID regex `^[0-9a-f]{32}$` (stock avatars use human-readable IDs like `Abigail_expressive_20240617`).

---

### List All Voices

```
GET https://api.heygen.com/v2/voices
```

Returns all available voices.

**Filtering heuristic for custom voices:** `preview_audio: null` (stock voices have an S3 preview URL).

---

### Retrieve Video Status

```
GET https://api.heygen.com/v1/video_status.get?video_id=<id>
```

**Status values:**
| Status | Meaning |
|---|---|
| `pending` | Queued, not yet started |
| `waiting` | In waiting state |
| `processing` | Currently rendering |
| `completed` | Done — download URL available |
| `failed` | Rendering failed (e.g., script too long) |

**Response when completed:**
- `video_url` — pre-signed download URL (refreshed on each status check; valid 7 days)
- `video_id`
- `status`

Recommended poll interval: every 15 seconds. Typical render time: 5–10 minutes for Video Agent videos. Expect 404 for the first ~4 minutes after triggering (normal — handled by `poll_heygen_video.py`).

---

## Constraints & Limits

| Constraint | Limit |
|---|---|
| Script text | < 5,000 characters |
| Audio duration | ≤ 10 minutes (600 seconds) |
| Video file input | MP4, max 100MB, < 2K resolution |
| Image input | JPG/PNG, max 50MB, < 2K |
| Audio input | WAV/MP3, max 50MB |
| Video output frame rate | 25fps |
| Dimension range | 128–4096px (width and height) |
| Max scenes per video | 50 |
| Free plan resolution cap | 720p |

---

## Pricing (Pay-As-You-Go)

| Asset | Engine | Cost |
|---|---|---|
| Public Avatar | Engine III | $0.0167/sec |
| Public Avatar | Engine IV | $0.10/sec |
| Digital Twin | Engine III | $0.0333/sec |
| Digital Twin | Engine IV | $0.10/sec |
| Photo Avatar | Engine III | $0.0167/sec |
| Photo Avatar | Engine IV | $0.10/sec |
| Video Agent | — | $0.0333/sec |
| Translation (Speed) | — | $0.05/sec |
| Translation (Precision) | — | $0.10/sec |
| Text-to-Speech (Starfish) | — | $0.000333/sec |

Photo Avatar operations: $1/call (generation, look, motion); $4/call (training).

---

## Digital Twin Creation (Enterprise Only)

Workflow for creating a new custom avatar from real video footage:

1. **Prepare materials** — two MP4 files at publicly accessible URLs:
   - Training footage: ≥ 2 min, 720p+, clear speech, well-lit
   - Consent statement: video explicitly granting permission to use footage
2. **Submit creation request** — `POST /reference/submit-video-avatar-creation-request`
   - Params: `training_footage_url`, `video_consent_url`, `avatar_name`
   - Returns: `avatar_id`
3. **Poll creation status** — `GET /reference/check-digital-twin-generation-status?avatar_id=<id>`
   - Statuses: `in_progress`, `complete`, `failed`
4. **Use avatar** — once `complete`, use `avatar_id` in video generation calls

**Common failure reasons:** invalid training footage format, inaccessible download URL.

---

## Video Agent (Primary Endpoint for GU Videos)

```
POST https://api.heygen.com/v1/video_agent/generate
```

Single natural-language `prompt` drives the entire production — script, visuals, pacing, and scene structure. Voice is auto-selected from the avatar; no `voice_id` needed.

**Request body:**
| Field | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string | Yes | Full production brief — see Prompt Engineering below |
| `config.avatar_id` | string | Yes | Custom avatar UUID |
| `config.orientation` | string | Yes | `portrait` (9:16) or `landscape` (16:9) |

**Response:**
```json
{ "video_id": "<id>" }
```

Poll with `/v1/video_status.get`. Expect 404 for the first ~4 minutes (normal — video is indexing). Total render time: 5–10 minutes for short videos. URLs expire after 7 days.

---

### Prompt Engineering for Video Agent

Source: [HeyGen Video Agent Prompt Guide](https://www.heygen.com/blog/video-agent-prompt-guide) (Jan 2026)

**The three baseline controls** (set these first, in the prompt):
- Avatar: specify the avatar or say "no avatar" for voice-over only
- Duration: `~20 seconds` or let Auto decide based on content
- Aspect ratio: portrait or landscape (also set via `config.orientation`)

**The biggest upgrade:** Paste the full spoken script directly into the prompt. The agent follows it scene-by-scene while improving flow, timing, and visuals automatically.

**Visual style matters:** Without explicit style direction, visuals can look inconsistent between scenes. Define:
- Color palette: use exact hex codes (e.g., `"Use #1E3A5F as primary navy, #2D5A27 as golf green"`)
- Font family if applicable
- Media type preferences per scene: motion graphics, AI-generated images/video, or stock footage

**Media type guide:**
| Type | Best for |
|---|---|
| Motion graphics | Stats, lists, chapter cards, lower thirds, data overlays |
| AI-generated images/video | Custom scenarios, stylized visuals, product mockups |
| Stock footage | Real-world establishing shots, emotional moments, industry scenes |

**Scene-by-scene structure** (use when precision matters):
```
Scene 1: [Type — Motion Graphics / A-roll / B-roll]
Visual: [exact description]
VO: "[spoken script]"
Duration: ~N seconds

Scene 2: ...
```

**Recommended prompt additions for clean, professional output:**
```
Use minimal, clean styled visuals. Leverage motion graphics as B-roll and A-roll overlays.
Use AI-generated video when necessary. When real-world footage is needed, use stock media.
Include an intro sequence, outro sequence, and chapter breaks using motion graphics.
```

**Attachments:** You can upload images, videos, or PDFs alongside the prompt. The agent will extract content and use uploaded media as B-roll or reference. Add context: `"Reference the attached PDF for accurate specs"` or `"Use the attached screenshot as B-roll when discussing features"`.

---

## Other Capabilities (Not Currently Used)

- **Video Translation** — `POST /v1/video_translate/translate` — upload video, get back dubbed version
- **Templates** — generate videos from pre-built HeyGen templates
- **Personalized Videos** — bulk variable-substitution videos from a single template
- **Streaming Avatar** — real-time interactive avatar (legacy SDK)
- **Webhooks** — event callbacks for video completion
- **HeyGen MCP Server** — direct Claude integration (alternative to n8n)

---

## Related Docs

- Full API Reference: https://docs.heygen.com/reference
- Limits & pricing: https://docs.heygen.com/reference/limits
- Digital Twin guide: https://docs.heygen.com/docs/video-avatars-api
- Photo Avatar guide: https://docs.heygen.com/docs/photo-avatars-api
- HeyGen MCP Server: https://docs.heygen.com/docs/heygen-mcp-server
- Webhooks: https://docs.heygen.com/docs/using-heygens-webhook-events

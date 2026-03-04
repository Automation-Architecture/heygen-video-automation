# HeyGen Photo Avatar → Avatar IV Upgrade Guide

## Your Situation

You have 4 "talking photos" in HeyGen that produce basic lip-synced video, plus 1 true avatar (likely a Digital Twin created from video footage). The talking photos are limited — they animate a still image with simple mouth movement but lack expressive gestures, head motion, and emotional delivery.

The upgrade path converts each talking photo into a **trained Photo Avatar** with multiple looks, then generates videos using the **Avatar IV engine** for dramatically better output quality.

---

## What You'll Gain

- **Avatar IV motion engine**: Interprets vocal tone, rhythm, and emotion to generate photorealistic facial movements, head tilts, natural pauses, and micro-expressions
- **Custom motion prompts**: Direct your avatar's gestures and expressions per video
- **Multiple "looks"**: Generate different outfits, backgrounds, and poses for each avatar via text prompts
- **Consistent identity**: LoRA model training locks in each person's facial features across all generated looks
- **1080p default output** with Avatar IV

---

## Overview: The 8-Step Pipeline

```
Step 1: Upload high-quality photos (Upload Asset API)
Step 2: Create Avatar Groups — one per person (Create Photo Avatar Group API)
Step 3: Add additional photos to each group (Add Looks API)
Step 4: Train each Avatar Group (Train Photo Avatar Group API)
Step 5: Check training status (Get Training Job Status API)
Step 6: Generate new "looks" via prompts (Generate Photo Avatar Looks API)
Step 7: (Optional) Add motion/sound to static looks (Add Motion API)
Step 8: Generate Avatar IV videos (Create Avatar IV Video API or V2 API with use_avatar_iv_model)
```

---

## Step 1: Upload High-Quality Source Photos

Before anything else, you need good source photos for each of your 4 avatars. Upload them via the **Upload Asset API**.

**Photo best practices:**
- Front-facing with even lighting and visible facial features
- High-resolution (1080p+ minimum)
- Mix of angles, expressions (smiling, neutral, serious), and outfit styles
- Close-up and half-body shots
- Minimal background distractions
- Choose photos that match the expression/tone you want your avatar to have — Avatar IV uses the source photo's expression as a baseline

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v1/asset \
  --header 'x-api-key: <YOUR_API_KEY>' \
  --header 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/avatar_photo.jpg'
```

**Response** — save the `image_key` for each upload:
```json
{
  "data": {
    "image_key": "image/47b2367366d94ee79894ed1f692b33ae/original"
  }
}
```

> **Do this for all source photos across your 4 avatars.** Aim for 3-5 photos per person for best training results.

---

## Step 2: Create an Avatar Group (One Per Person)

Each of your 4 talking photos becomes its own Avatar Group. This groups all photos of the same subject together.

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v2/photo_avatar/avatar_group/create \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'X-Api-Key: <YOUR_API_KEY>' \
  --data '{
    "name": "Avatar 1 - Brad",
    "image_key": "image/47b2367366d94ee79894ed1f692b33ae/original"
  }'
```

**Response** — save the `group_id`:
```json
{
  "error": null,
  "data": {
    "id": "0b1b8dabd16f40a2b2ae6599790bba05",
    "group_id": "0b1b8dabd16f40a2b2ae6599790bba05",
    "name": "Avatar 1 - Brad",
    "status": "pending"
  }
}
```

> **Repeat for each of your 4 avatars**, giving each a descriptive name.

---

## Step 3: Add More Photos to Each Group

Add the remaining photos for each person to their respective Avatar Group.

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v2/photo_avatar/avatar_group/add \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>' \
  --data '{
    "group_id": "0b1b8dabd16f40a2b2ae6599790bba05",
    "image_keys": [
      "image/KEY_2/original",
      "image/KEY_3/original",
      "image/KEY_4/original"
    ]
  }'
```

> You can add up to **4 image_keys at a time**. If you have more, make multiple calls.

---

## Step 4: Train the Avatar Group

This is the critical step — it builds a **LoRA model** that learns the subject's unique features, expressions, and characteristics. This ensures all future generated "looks" maintain a consistent identity.

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v2/photo_avatar/train \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>' \
  --data '{
    "group_id": "0b1b8dabd16f40a2b2ae6599790bba05"
  }'
```

> **Repeat for all 4 Avatar Groups.** Training takes time — move to the next step to monitor progress.

---

## Step 5: Check Training Status

Poll this endpoint until training completes.

**API Call:**
```bash
curl --request GET \
  --url https://api.heygen.com/v2/photo_avatar/train/status/0b1b8dabd16f40a2b2ae6599790bba05 \
  --header 'accept: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>'
```

**Status values:**
- `in_progress` — still training, check back later
- `success` — ready for look generation
- `failed` — check your source photos and retry

---

## Step 6: Generate New "Looks" via Prompts

Once trained, you can create unlimited variations of each avatar — different outfits, scenes, poses, and backgrounds — all while maintaining the person's identity.

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v2/photo_avatar/look/generate \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>' \
  --data '{
    "group_id": "0b1b8dabd16f40a2b2ae6599790bba05",
    "prompt": "Avatar in professional business attire, smiling, modern office background",
    "orientation": "square",
    "pose": "half_body",
    "style": "Realistic"
  }'
```

**Response:**
```json
{
  "error": null,
  "data": {
    "generation_id": "c37388c94f614948ad96b8cf75c7a09f"
  }
}
```

**Check look generation status:**
```bash
curl --request GET \
  --url https://api.heygen.com/v2/photo_avatar/generation/c37388c94f614948ad96b8cf75c7a09f \
  --header 'accept: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>'
```

**Prompt tips:**
- Always include "Avatar" in the prompt (e.g., "Avatar in business attire, smiling")
- Be specific about clothing, scene, and expression
- Parameters: `orientation` (square, front), `pose` (half_body, full_body, hands on hips), `style` (Realistic, etc.)

> **Pro tip:** Focus on generating looks that match the types of videos you actually plan to make — each look consumes Premium Credits.

---

## Step 7: (Optional) Add Motion to Static Looks

If you want to preview motion on a specific look before creating full videos:

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v2/photo_avatar/add_motion \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>' \
  --data '{
    "id": "PHOTO_AVATAR_LOOK_ID"
  }'
```

---

## Step 8: Generate Avatar IV Videos

You have **two paths** to generate videos with your upgraded avatars:

### Path A: Dedicated Avatar IV Endpoint (Recommended for quick, single-scene videos)

This is the simplest route — upload a photo and get an Avatar IV video directly.

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v2/video/av4/generate \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>' \
  --data '{
    "image_key": "image/YOUR_AVATAR_LOOK_KEY/original",
    "video_title": "Client Intro Video",
    "script": "Hi, welcome to our AI automation platform...",
    "voice_id": "YOUR_VOICE_ID",
    "custom_motion_prompt": "Friendly smile, occasional hand gestures while speaking",
    "enhance_custom_motion_prompt": true
  }'
```

**Key parameters:**
- `image_key` — from your uploaded/generated avatar look
- `script` — the text the avatar will speak
- `voice_id` — get from List All Voices (V2) API: `GET /v2/voices`
- `custom_motion_prompt` — describe the gestures and expressions you want
- `enhance_custom_motion_prompt` — set `true` to let AI refine your motion prompt

> **Limit:** Avatar IV Photo-to-Video maxes out at **3 minutes** regardless of plan.

### Path B: V2 Video Generate Endpoint (For multi-scene, studio-quality production)

Use this for longer videos or when combining Avatar IV with other scenes, backgrounds, and music.

**API Call:**
```bash
curl --request POST \
  --url https://api.heygen.com/v2/video/generate \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>' \
  --data '{
    "video_inputs": [{
      "character": {
        "type": "talking_photo",
        "talking_photo_id": "YOUR_TALKING_PHOTO_ID"
      },
      "voice": {
        "type": "text",
        "voice_id": "YOUR_VOICE_ID",
        "input_text": "Your script text here..."
      }
    }],
    "use_avatar_iv_model": true
  }'
```

**The key flag is `use_avatar_iv_model: true`** — this switches the motion engine from the basic unlimited model to Avatar IV for your talking photos.

> When using in Studio mode, each individual scene/script box is limited to 180 seconds, but you can chain multiple scenes for longer videos.

### Getting Your Avatar and Voice IDs

**List all avatar groups:**
```bash
curl --request GET \
  --url https://api.heygen.com/v2/photo_avatar/avatar_groups \
  --header 'accept: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>'
```

**List avatars in a group (to get talking_photo_id):**
```bash
curl --request GET \
  --url https://api.heygen.com/v2/photo_avatar/avatar_group/GROUP_ID \
  --header 'accept: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>'
```

**List available voices:**
```bash
curl --request GET \
  --url https://api.heygen.com/v2/voices \
  --header 'accept: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>'
```

### Check Video Status

```bash
curl --request GET \
  --url https://api.heygen.com/v1/video_status.get?video_id=VIDEO_ID \
  --header 'accept: application/json' \
  --header 'x-api-key: <YOUR_API_KEY>'
```

**Status values:** `pending` → `processing` → `completed` (with video URL) or `failed`

---

## Credit Costs for Avatar IV

Avatar IV always consumes **Premium Credits** — there is no unlimited tier for it.

- **Standard Avatar IV**: 3 seconds of video = 1 Premium Credit (3:1 ratio)
- **With Custom Motion Prompt**: 3 seconds of video = 2 Premium Credits (essentially 1.5:1 ratio — higher quality costs more)
- HeyGen only charges for actual seconds of avatar generation, not total video length (pauses/silence are free)
- You can mix Avatar IV scenes with unlimited (Avatar III) scenes in Studio to conserve credits

---

## Quick Checklist for Your 4 Avatars

For **each** of your 4 talking photos, run through this sequence:

| # | Action | Endpoint | Key Output |
|---|--------|----------|------------|
| 1 | Upload 3-5 high-quality photos | `POST /v1/asset` | `image_key` per photo |
| 2 | Create Avatar Group | `POST /v2/photo_avatar/avatar_group/create` | `group_id` |
| 3 | Add remaining photos | `POST /v2/photo_avatar/avatar_group/add` | confirmation |
| 4 | Train the group | `POST /v2/photo_avatar/train` | training initiated |
| 5 | Poll training status | `GET /v2/photo_avatar/train/status/{group_id}` | `success` |
| 6 | Generate looks | `POST /v2/photo_avatar/look/generate` | `generation_id` → new looks |
| 7 | Generate Avatar IV video | `POST /v2/video/av4/generate` | `video_id` |
| 8 | Check video status | `GET /v1/video_status.get` | video download URL |

---

## Key Documentation Links

- **Photo Avatar Overview**: https://docs.heygen.com/docs/photo-avatars-api
- **Create & Train Groups**: https://docs.heygen.com/docs/create-and-train-photo-avatar-groups
- **Photo Avatar Endpoints Reference**: https://docs.heygen.com/docs/v2-photo-avatar-endpoints-generation-training-and-looks
- **Create Avatar IV Videos**: https://docs.heygen.com/docs/create-avatar-iv-videos
- **Create Avatar Video V2**: https://docs.heygen.com/reference/create-an-avatar-video-v2
- **Avatar IV Complete Guide**: https://help.heygen.com/en/articles/11269603-heygen-avatar-iv-complete-guide
- **Choosing Avatar Engines**: https://help.heygen.com/en/articles/11734785-choosing-the-right-avatar-engine-on-heygen-add-motion-vs-avatariv

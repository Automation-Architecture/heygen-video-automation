# Directive: Upgrade a Talking Photo to a Trained Photo Avatar

## Purpose

Upgrade any of the four "talking photo" avatars (Bob, Bud, Pro Golfer, Golf Cart Girl) from a basic static image to a fully-trained Photo Avatar with:
- Expressive head motion (LoRA-trained model)
- Micro-expressions
- Consistent identity across generated looks

The upgrade produces a new **look ID** that replaces the existing `talking_photo_id` in all scripts — no API call changes needed.

---

## Cost Summary

| Step | Cost |
|------|------|
| Photo upload | Free |
| Create group | Free |
| Add photos | Free |
| **Train group** | **$4 per attempt** |
| **Generate look** | **$1 per look** |
| Polling | Free |

**Always confirm the $4 and $1 charges with the user before running those scripts.**

---

## Phase 0: Photo Preparation (User Action Required)

The avatar must exist as a series of 3–5 consistent source photos before any scripts run. **You cannot download the original talking photo from HeyGen's API** — use the HeyGen dashboard (`app.heygen.com/avatar/my-avatars`) to view the current image as reference, then generate fresh high-quality images.

### Staging Directory

Place photos in `.tmp/<avatar_slug>_photos/`. For Bob: `.tmp/bob_photos/`

Acceptable formats: `.jpg`, `.jpeg`, `.png`, `.webp`
Recommended resolution: 1024×1024 or higher, front-lit, centered face.

### AI Image Prompts Per Avatar

**Bob Commentator** — broadcast sports announcer, late 60s
> "photorealistic broadcast sports announcer, late 60s, silver-grey hair neatly combed, authoritative dignified expression, dark sport coat and tie, broadcast studio background, front-facing portrait, studio lighting, 8k resolution"

Suggested variations (generate 3–5):
1. Neutral half-body, looking at camera
2. Slight nod, close-up on face
3. Eyes raised, reflective expression
4. Serious full-face, slightly turned
5. Three-quarter profile, jacket visible

**Bud The Caddy** — weathered caddy, outdoors
> "photorealistic golf caddy, 50s, weathered tan face, white caddy bib, golf course background, friendly expression, outdoor lighting, front-facing portrait, 8k resolution"

**Pro Golfer** — athletic male golfer
> "photorealistic professional golfer, 30s, athletic build, polo shirt, golf course background, confident expression, front-facing portrait, natural daylight, 8k resolution"

**Golf Cart Girl** — upbeat young woman at golf course
> "photorealistic young woman, 20s, bright smile, casual golf attire, golf cart and course in background, front-facing portrait, sunny natural lighting, 8k resolution"

---

## Orchestration Sequence

Claude runs these steps in order once `.tmp/<slug>_photos/` is populated.

### Step 1: Upload All Photos

Run for each photo file:
```bash
source .env && python3 execution/upload_photo_asset.py --file .tmp/bob_photos/bob_01.jpg
```
Collect `image_key` from each output. You need at least 1 for group creation; subsequent ones added in Step 3.

### Step 2: Create Avatar Group

Use the **first** `image_key`:
```bash
source .env && python3 execution/create_photo_avatar_group.py \
  --name "Bob Commentator" \
  --image_key "image/.../original"
```
Capture `group_id` from output. Record it in `directives/avatar_personas.md`.

### Step 3: Add Remaining Photos

For remaining image_keys (max 4 per call):
```bash
source .env && python3 execution/add_photos_to_group.py \
  --group_id <group_id> \
  --image_keys "image/.../original,image/.../original,..."
```
If you have more than 4 remaining keys, make multiple calls (first 4, then the rest).

### Step 4: Confirm Training Cost with User

Before running training, confirm:
> "Training will cost $4. Ready to proceed?"

Only run Step 5 after explicit user confirmation.

### Step 5: Start Training

```bash
source .env && python3 execution/train_photo_avatar_group.py --group_id <group_id>
```

### Step 6: Poll Training

Training takes up to 30 minutes:
```bash
source .env && python3 execution/poll_avatar_training.py --group_id <group_id>
```
Wait for `{"status": "success", "group_id": "..."}`.

### Step 7: Confirm Look Generation Cost with User

Before generating a look, confirm:
> "Look generation will cost $1. Ready to proceed?"

Only run Step 8 after explicit user confirmation.

### Step 8: Generate a Look

The prompt **must** include the word "Avatar":
```bash
source .env && python3 execution/generate_avatar_look.py \
  --group_id <group_id> \
  --prompt "Avatar as broadcast sports announcer, dark sport coat, broadcast studio, half-body, front-facing" \
  --orientation square \
  --pose half_body \
  --style Realistic
```

### Step 9: Poll Look Generation

```bash
source .env && python3 execution/poll_avatar_look.py --generation_id <generation_id>
```

Output includes `"data": {...}` — the full API response. Inspect the `data` dict to find the field containing the new avatar/look ID. Common candidates: `avatar_id`, `talking_photo_id`, `look_id`, `id`. **Update this directive with the actual field name once confirmed.**

> **Unknown field as of 2026-03-04:** The `data` response shape is undocumented. `poll_avatar_look.py` prints the full dict intentionally.

### Step 10: Record New IDs

Update these files with the new look ID (and group ID):
- `directives/avatar_personas.md` — Bob's Avatar ID → new look ID; add Group ID note
- `directives/create_avatar_video.md` — Step 0 avatar table
- `CLAUDE.md` — Avatar table

### Step 11: Validate New ID

```bash
source .env && python3 execution/validate_avatar_id.py <new_look_id>
```

Note: `validate_avatar_id.py` queries `/v2/avatars` which may not include Photo Avatar Group looks. If validation fails but the look ID came from a successful poll, the ID is likely valid. In that case, skip to Step 12 and validate implicitly via video generation.

If needed, also try: `GET /v2/photo_avatar/avatar_groups` to list groups and their associated look IDs (no script for this yet — use curl or create one).

### Step 12: Test Video

Generate a short test video with the new ID:
```bash
source .env && python3 execution/generate_heygen_video_v2.py \
  --avatar_id <new_look_id> \
  --avatar_type talking_photo \
  --voice_id 06c816b952f14fa9b3a6c42aa151f731 \
  --script "Testing the new Bob Commentator look. Looking sharp!" \
  --orientation portrait
```
Then poll: `source .env && python3 execution/poll_heygen_video.py`

Compare motion quality to the old Bob ID (`924e085127e14867814dc5f99d2f6419`).

---

## Repeating for Other Avatars

The exact same sequence applies to Bud, Pro Golfer, and Golf Cart Girl. Use the persona-specific AI image prompt from Phase 0. Staging directories:
- `.tmp/bud_photos/`
- `.tmp/pro_golfer_photos/`
- `.tmp/cart_girl_photos/`

---

## Edge Cases & Gotchas

**multipart/form-data in upload_photo_asset.py**
This is the only script that doesn't use a JSON body. It manually builds CRLF multipart boundaries. If HeyGen rejects the upload with a 400, check that the file extension is recognized (jpg, png, webp) and that the file isn't corrupted.

**group_id vs. look_id**
- `group_id`: Used for training management; not used in video generation.
- `look_id` (or whatever field `poll_avatar_look.py` reveals): Used as `talking_photo_id` in video scripts.
- Record both in `avatar_personas.md`.

**Photo quality matters**
Training costs $4 per attempt. Poor-quality or inconsistent source photos produce a bad model. Before training, verify:
- Images are front-facing (or near-front)
- Consistent lighting across shots
- No heavy filters or distortion
- At least 3 photos minimum; 5 is better

**validate_avatar_id.py scope**
The script currently only queries `/v2/avatars` (standard avatars + talking photos). Trained Photo Avatar look IDs may not appear there. The real validation is a successful video generation.

**Look generation prompt**
The word "Avatar" must appear in the prompt (HeyGen enforces this). The `generate_avatar_look.py` script raises a clear error if it's missing.

**Training failure**
If `poll_avatar_training.py` returns `"status": "failed"`, check:
1. Photo count (minimum 3 required)
2. Photo quality (see above)
3. HeyGen dashboard for error details

You may need to create a new group with better photos (another $4).

---

## Record of Upgrades

| Avatar | Group ID | Look ID | Trained | Date |
|--------|----------|---------|---------|------|
| Bob Commentator | `924e085127e14867814dc5f99d2f6419` | `7c5124f727b840bdb2fa66380ade0a0f` | Yes | 2026-03-04 |
| Bud The Caddy | — | — | No | — |
| Pro Golfer | `3c4b06f3ae6b42adb456f7022f4dc9d1` | `3c4b06f3ae6b42adb456f7022f4dc9d1` | Yes | 2026-03-04 |
| Golf Cart Girl | `fee86c5c0bbe45f7954d2bd31046b6f9` | `5de5fb82755e4ea198450101ae360c79` | Yes | 2026-03-04 |

*(Update this table after each successful upgrade)*

# Avatar Personas Registry

## Golfers Unite — Brand Context

**Mission:** Unite golfers worldwide through curated access, exclusive value, and authentic storytelling.

**Tagline:** "Where Golf Culture Connects." / "Curated for the Culture."

**What it is:** A modern golf culture and membership platform. Not a discount card — a movement. Blends editorial golf culture with premium membership benefits: exclusive deals on gear/travel/instruction, event access, and a global community.

**Brand voice:** Editorial, smart, and inclusive. Not transactional — emotional. Every video should feel like a trusted insider, not a press release.

**What to reinforce in scripts:** Community identity, insider access, the culture of the game. Scripts should feel like the persona is part of your golf circle. Occasional natural references to "the community" or members are welcome, but keep it organic.

---

## Fast-Path Voice Notes

**Jeff's voice** (`58aef04cd30741e9ac705f9a6ce0d907`) is his cloned voice — confirmed accessible for video generation.

**Other custom voices** visible in `list_heygen_voices.py` (Brooks, Nicholas, Ricky, Annie variants, Gabriela) appear to belong to other team members and return `TTS_VOICE_UNAVAILABLE_ERR`. Use stock HeyGen voices (those with a `preview_audio` URL) for all non-Jeff avatars. The voice IDs listed per avatar below are stock voices selected for persona fit.

To discover available stock voices: `python3 execution/list_heygen_voices.py --all`

---

## Video Agent Prompt Format

Each avatar has a compact `### Video Agent Prompt` template: a tightened script + a ~60-char cinematic suffix encoding 4 visual beats (drone/wide open → avatar course-side → energy B-roll → branded outro). Current templates target ~220 chars total.

**Prompt length testing in progress.** We know ~220 chars works reliably. We know ~2600 chars appeared to fail (those jobs never appeared in the video list). A 1472-char prompt rendered successfully. The true ceiling is unknown — we're deliberately starting compact and expanding the suffix with each new video to probe the limit. When a longer suffix works, update the template and note the new confirmed ceiling here.

| Chars tested | Result | Date |
|---|---|---|
| ~244 | ✓ renders reliably | 2026-03-03 |
| ~900 | 🧪 testing — expanded cinematic prompt (natural script + scene-by-scene visual direction) | 2026-03-03 |
| ~1472 | ✓ rendered once | 2026-03-03 |
| ~2600 | ✗ never appeared in list | 2026-03-03 |

---

## Jeff

**Avatar ID:** `ccce0126b55f418e858ce9c7047eff1a`
**Avatar Type:** `avatar` (standard)
**Voice ID (fast-path):** `58aef04cd30741e9ac705f9a6ce0d907` (jeff — cloned voice)
**Role:** Golf community founder

### Tone & Style
- Friendly, knowledgeable, direct — like talking to a friend at the clubhouse
- Conversational and genuine, not a broadcaster
- Concise and specific; no filler phrases
- Comfortable with golf jargon (the tour, the cut, the field, FedEx Cup) without overdoing it
- Ends with a reason to stay engaged: check back, tune in, follow along

### Example Phrases
- "One of the most iconic stops on tour"
- "Stay tuned right here for play-by-play, news, and updates"
- "A loaded field this week"
- "Should be a great week of golf"
- "Keep an eye on [player] this week"

### Things to Avoid
- Overly formal broadcast language ("Welcome to our coverage of...")
- Superlatives without substance ("The most incredible tournament ever!")
- Starting every script with "Hey everyone" — vary the opener
- Exceeding 50 words

### Script Length
~45 words. Range: 35–50. Hard cap at 50. Under 20 seconds spoken.

### Visual Environment
- **Orientation:** portrait (9:16) — Instagram Reels, TikTok, Stories
- **Style:** Clean, minimal. Modern golf aesthetic — editorial, premium but inclusive. Simple background evoking golf culture (dark navy, golf green, or clean studio). Avatar clearly visible, centered, well-lit.
- **Voice:** Determined automatically by HeyGen from avatar — do NOT pass `voice_id`.

### Video Agent Prompt

```
[SCRIPT] Drone open, Jeff course-side, gallery B-roll, navy outro.
```

Build: Replace `[SCRIPT]` with the tightened approved script. Drop contractions and trim filler to fit. The script names the tournament and venue — Video Agent infers course visuals from that context. The suffix encodes the 4-scene structure: aerial drone B-roll open → Jeff course-side portrait in natural light → gallery energy cuts (drone + eye-level + low angle) → Golfers Unite dark navy outro card.

### Fast-Path (V2) Motion Prompt

```
Warm, direct. Slight forward lean. Natural hand gesture mid-script. Confident close.
```

Used with `generate_heygen_video_v2.py` (Avatar IV engine, ~1 min render). Pass the approved script verbatim as `--script`; do not include the cinematic suffix.

---

## Bob Commentator

**Avatar ID:** `924e085127e14867814dc5f99d2f6419`
**Avatar Type:** `talking_photo`
**Voice ID (fast-path):** `06c816b952f14fa9b3a6c42aa151f731` (William Prescott - Broadcaster — authoritative, dignified)
**Role:** Senior Tour announcer, five decades on the mic

### Tone & Style
- Grave, measured, authoritative — the voice of the game's history
- Speaks in complete, considered sentences; never rushed
- Deep reverence for the traditions and legends of the Tour
- References past champions and historic rounds naturally, from memory
- Occasionally wistful — he's seen the great ones come and go

### Example Phrases
- "In all my years covering this tournament..."
- "We haven't seen pressure like this since [historic moment]"
- "The galleries here remember what this course demands"
- "This young man has a chance to write his name in the record books"
- "Augusta — or Pebble — or St. Andrews — has a way of sorting things out"

### Things to Avoid
- Casual slang or humor — Bob does not joke
- Modern internet-speak or trend references
- Breathless excitement; Bob's gravitas is his whole thing
- Exceeding 55 words

### Script Length
~45 words. Range: 35–55. Hard cap at 55. Bob speaks deliberately — every word earns its place.

### Visual Environment
- **Orientation:** portrait (9:16) — Instagram Reels, TikTok, Stories
- **Style:** Classic broadcast aesthetic. Dark wood paneling or press box feel. Dignified, timeless.
- **Voice:** Determined automatically by HeyGen from avatar — do NOT pass `voice_id`.

### Video Agent Prompt

```
[SCRIPT] Aerial open, Bob broadcast elevated, reverent gallery, dark outro.
```

Build: Replace `[SCRIPT]` with the tightened approved script. Bob speaks deliberately — every word earns its place, so trim without softening. The suffix encodes the 4-scene structure: slow aerial drone B-roll open → Bob at elevated broadcast position with dignified framing → reverent gallery wide shots and fairway panoramics → dark mahogany/navy outro card. No flashy transitions — slow dissolves only.

### Fast-Path (V2) Motion Prompt

```
Grave and measured. Slow, deliberate head nod. Eyes focused at camera. Still, commanding.
```

Used with `generate_heygen_video_v2.py` (Avatar IV engine, ~1 min render). Pass the approved script verbatim as `--script`.

---

## Bud The Caddy

**Avatar ID:** `35a38a2bfbfe4d5ea33f1a8b8434aa06`
**Avatar Type:** `talking_photo`
**Voice ID (fast-path):** `f38a635bee7a4d1f9b0a654a31d050d2` (Chill Brian — casual, laid-back)
**Role:** Career looper — Nantucket summers, Palm Beach winters, zero tax returns

### Backstory
Bud has been on the bag for thirty years, working private clubs up and down the Eastern Seaboard. Spends summers at a club in Nantucket, winters at The Medalist in Palm Beach. He hasn't filed taxes since 2009, has a standing bet on every major, and knows every shortcut on every course he's ever walked. He is genuinely funny, unfiltered, and 100% not worried about consequences.

### Tone & Style
- Irreverent, quick, self-aware — like a caddy who knows he's the smartest guy on the bag loop
- Drops inside golf knowledge casually, like it's obvious
- Light gambling references are natural and on-brand ("I've got money on this")
- Self-deprecating about his lifestyle without shame
- Never mean — chaotic neutral, not cynical

### Example Phrases
- "Look, I've seen this play out a thousand times on the bag..."
- "I wouldn't say I have a system, but I've got a system"
- "The smart money — my money, which is a loose term — is on..."
- "I've been on this green in every weather condition known to man"
- "Don't tell the IRS I said this, but..."

### Things to Avoid
- Overly polished or corporate language
- Anything that sounds like a press release
- Making the gambling feel dark or problematic — keep it light and self-aware
- Exceeding 55 words

### Script Length
~45 words. Range: 35–55. Bud talks like he walks — efficient but colorful.

### Visual Environment
- **Orientation:** portrait (9:16) — Instagram Reels, TikTok, Stories
- **Style:** Casual, outdoorsy. On-course feel — natural light, turf in the background, the vibe of a man who's been outside his whole life.
- **Voice:** Determined automatically by HeyGen from avatar — do NOT pass `voice_id`.

### Video Agent Prompt

```
[SCRIPT] Low fairway open, Bud on-course casual, caddy B-roll, earthy outro.
```

Build: Replace `[SCRIPT]` with the tightened approved script. Keep the best joke or insider line — that's the whole video. The suffix encodes the 4-scene structure: ground-level low-angle fairway B-roll open (bag at frame edge, rope-line energy) → Bud casual on-course in natural outdoor light → caddy's-eye B-roll cuts (yardage checks, player tough lies, dawn range warmup) → warm earthy palette Golfers Unite outro.

### Fast-Path (V2) Motion Prompt

```
Casual, loose. Slight smirk. One knowing shrug mid-script. Relaxed close.
```

Used with `generate_heygen_video_v2.py` (Avatar IV engine, ~1 min render). Pass the approved script verbatim as `--script`.

---

## Pro Golfer

**Avatar ID:** `1fd5fe07a84749fc88143d0640841d46`
**Avatar Type:** `talking_photo`
**Voice ID (fast-path):** `0f50a7a5577e4cd583ba738094956899` (Marcus - Professional — direct, focused)
**Role:** Rookie Tour pro — just earned his card this season

### Backstory
He's been grinding for this his entire life. Mini-tours, Q-School, Korn Ferry — he paid his dues. Now he's here and he is not messing around. He trains every day, studies every course, and takes absolutely nothing for granted. He's young, serious, and already sounds like a veteran.

### Tone & Style
- Focused, disciplined, genuine — no hype, just intent
- Speaks from personal experience: what it took to get here, what it takes to stay
- Deep respect for the competition — nothing is ever easy at this level
- Occasionally lets competitive fire show through, but stays composed
- Relatable but aspirational — he represents the work behind the dream

### Example Phrases
- "I've been preparing for courses like this my whole career"
- "You don't get to this level without respecting the process"
- "Every shot matters — you learn that fast out here"
- "The field this week is tough. That's what I signed up for."
- "I'm not here to make up the numbers"

### Things to Avoid
- Casualness or humor that undercuts the seriousness
- Bravado or trash talk — he's competitive, not arrogant
- Generic sports clichés ("take it one shot at a time") — make it feel real
- Exceeding 50 words

### Script Length
~40 words. Range: 30–50. He's efficient. Says what needs saying and gets back to work.

### Visual Environment
- **Orientation:** portrait (9:16) — Instagram Reels, TikTok, Stories
- **Style:** Modern, athletic. Practice facility or on-course setting. Clean gear, focused energy.
- **Voice:** Determined automatically by HeyGen from avatar — do NOT pass `voice_id`.

### Video Agent Prompt

```
[SCRIPT] Range open, Pro practice tee portrait, approach shots, stark outro.
```

Build: Replace `[SCRIPT]` with the tightened approved script. No filler — every word should sound like it cost something. The suffix encodes the 4-scene structure: pre-dawn practice range B-roll open (irons on the range, low-angle pin approach) → Pro on practice tee, forward-facing portrait with sharp clean lighting → approach shots/green-reading/ball-tracking cuts (ground-level and drone mixed) → stark black/deep navy Golfers Unite outro card.

### Fast-Path (V2) Motion Prompt

```
Focused, intense. Direct eye contact throughout. Minimal movement. Determined close.
```

Used with `generate_heygen_video_v2.py` (Avatar IV engine, ~1 min render). Pass the approved script verbatim as `--script`.

---

## Golf Cart Girl

**Avatar ID:** `fee86c5c0bbe45f7954d2bd31046b6f9`
**Avatar Type:** `talking_photo`
**Voice ID (fast-path):** `084760b4922a44599575c770070ec2d7` (Peppy Stella — playful, bright)
**Role:** The beverage cart girl — the soul of the round

### Backstory
She runs the cart, she knows everyone's drink order, and she will absolutely roast you with a smile on her face. She's been doing this long enough to have heard every bad golf joke and still finds new ones to drop. Flirty, funny, and completely unbothered.

### Tone & Style
- Light, playful, flirty without being inappropriate — think smirking, not scandalous
- Delivers drink orders and golf takes with equal confidence
- Short, punchy jokes — the kind that land and disappear before anyone can object
- Smiles implied in every line; you can hear the smirk
- Keeps golf content light and fun — not analytical, not serious

### Example Phrases
- "Alright, who needs a drink and who needs a lesson? I only carry one of those."
- "The round's not going great, but the Modelo's ice cold — you're welcome."
- "Nobody's playing better than the guy who stopped checking his scorecard."
- "I've seen a lot of golf out here. Most of it from the safe distance of my cart."
- "Cold beer, warm weather, live golf. You're basically living the dream."

### Things to Avoid
- Anything too serious or analytical
- Crossing from flirty into inappropriate — keep it PG-13
- Long setups — her jokes land fast or not at all
- Exceeding 45 words

### Script Length
~35 words. Range: 25–45. Short, snappy, always with a punchline.

### Visual Environment
- **Orientation:** portrait (9:16) — Instagram Reels, TikTok, Stories
- **Style:** Bright, sunny, on-course. Beverages visible if possible. Warm and inviting — feels like you just flagged down the cart.
- **Voice:** Determined automatically by HeyGen from avatar — do NOT pass `voice_id`.

### Video Agent Prompt

```
[SCRIPT] Sunny gallery open, Cart Girl cart-path portrait, fans B-roll, gold outro.
```

Build: Replace `[SCRIPT]` with the tightened approved script. Keep the punchline — it's the whole video. The suffix encodes the 4-scene structure: wide sunny gallery walking B-roll open (fans in hats, blue sky, cart path energy) → Cart Girl on cart-path with smirking casual portrait framing, beverages in background → fan reaction/crowd B-roll cuts (birdie reactions, packed 18th, fairway walks) → bright punchy gold/coral Golfers Unite outro card.

### Fast-Path (V2) Motion Prompt

```
Light, playful smirk throughout. One quick eyebrow raise. Breezy, confident close.
```

Used with `generate_heygen_video_v2.py` (Avatar IV engine, ~1 min render). Pass the approved script verbatim as `--script`.

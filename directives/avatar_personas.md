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

**Avatar ID (Look):** `7c5124f727b840bdb2fa66380ade0a0f` ← use this for video generation
**Group ID:** `<SET_FROM_create_photo_avatar_group.py_OUTPUT>` (Photo Avatar Group — management only; must be the group_id returned by the group-create call for Bob's photo avatar)
**Other Look IDs:** `4bfacbefb81843a68a6ffb2d0fca1f38`, `3776b2391b9f440a8e820e20a8ae5fe4`
**Avatar Type:** `talking_photo`
**Voice ID (fast-path):** `06c816b952f14fa9b3a6c42aa151f731` (William Prescott - Broadcaster — authoritative, dignified)
**Role:** Senior Tour announcer, five decades on the mic

### Tone & Style
- Grave, measured, authoritative — the voice of the game's history
- Speaks in complete, considered sentences; never rushed
- Deep reverence for the traditions and legends of the Tour
- References past champions and historic rounds naturally, from memory — by name, by year, by what it meant
- Occasionally wistful — he's seen the great ones come and go

### Historical Perspective

Bob's defining quality is that he *was there*. He covered Nicklaus, Palmer, and Watson in their prime. He was in the press box for every defining moment of the last five decades. His scripts should feel like they're coming from memory — specific, earned, unrepeatable.

**Every Bob script must include at least one historically specific anchor:**
- A past champion at this venue, by name — and ideally the year or number of wins
- A defining moment: a shot, a collapse, a comeback that shaped what this tournament means
- A record or streak: multiple wins, lowest rounds, wire-to-wire dominance
- A direct comparison between a current player and a legend: "We haven't seen [X] since [player] in [year]"

**Bob is never generic.** He doesn't say "great players have stood on this tee." He says "Palmer won here eight times — and this course never made it easy for him." Generic reverence is someone else's territory. Bob has receipts.

**Before scripting Bob, always research via Exa:**
1. Past champions at this specific event — especially multiple-time winners and records
2. Defining historic moments at this venue: famous shots, collapses, comebacks, duels
3. Venue history: age, designer, signature holes, course records, what makes it distinctive
4. Current player storylines with historical context (record chase, comeback, rival dynamic)

Use these facts to give Bob at least one specific, grounded historical reference per script. Vague reverence is not enough — Bob was in the booth when it happened.

### Example Phrases
- "Arnold Palmer won here eight times. Eight. And this course never once made it simple."
- "We haven't seen back-to-back champions at [venue] since [name] in [year]. This field will need to earn it the same way."
- "I was covering this tournament the last time someone came from six back on Sunday. The gallery didn't believe it. The player did."
- "The galleries here have a memory. They've watched the best in the world come undone on this closing stretch."
- "This young man has a chance to write his name beside [legend's] in the record books — and he knows it."
- "The last time this course saw a field this strong was [year]. [Player] won, and it still wasn't comfortable."
- "In fifty years on the mic, I have watched this venue sort out the pretenders from the champions. It will do so again."

### Things to Avoid
- Casual slang or humor — Bob does not joke
- Modern internet-speak or trend references
- Breathless excitement; Bob's gravitas is his whole thing
- Generic reverence without a specific fact behind it — "great champions have stood here" is not enough for Bob
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

**Avatar ID (Look):** `3c4b06f3ae6b42adb456f7022f4dc9d1` ← use this for video generation
**Group ID:** `<INSERT_PRO_GOLFER_GROUP_ID_FROM_create_photo_avatar_group.py>` (Photo Avatar Group — management only; use the actual `group_id` returned by the script)
**Avatar Type:** `talking_photo`
**Voice ID (fast-path):** `0f50a7a5577e4cd583ba738094956899` (Marcus - Professional — direct, focused)
**Role:** Rookie Tour pro — just earned his card this season

### Backstory
He's been grinding for this his entire life. Mini-tours, Q-School, Korn Ferry — he paid his dues. Now he's here and he's not shy about it. He's young, talented, and knows it. Over-confident in the way only a 22-year-old with a brand new Tour card can be. He talks like someone who thinks he's already won — not arrogant in a mean way, just genuinely certain the game bends to him. He hasn't been humbled yet. That's what makes him compelling.

### Tone & Style
- Young, brash, self-assured — the kid who walked into Q-School and never once doubted himself
- Talks like he belongs here, because he does — and he'll remind you
- Mixes real course knowledge with low-key swagger ("Yeah, Bay Hill's tough. I'm good.")
- Drops "I" a lot — this is his moment and he knows it
- Not trash talk, not manufactured hype — just genuine over-confidence from someone who earned the right
- Casual speech patterns: contractions, clipped sentences, thinks in punchy takes

### Example Phrases
- "Yeah, I'm ready for this one."
- "The field is stacked. Still like my chances."
- "I didn't grind through Korn Ferry to play it safe."
- "Bay Hill's supposed to be hard. I've been working on hard."
- "People sleep on me. That's fine."
- "First time playing here as a card holder. Feels right."

### Things to Avoid
- Overly polished or veteran-sounding language — he's 22, not 38
- Humble or self-deprecating takes — that's not him yet
- Generic sports clichés ("take it one shot at a time") — make it feel real and personal
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
Confident, relaxed. Slight smirk. Direct eye contact, unbothered energy. Casual but locked in.
```

Used with `generate_heygen_video_v2.py` (Avatar IV engine, ~1 min render). Pass the approved script verbatim as `--script`.

---

## Golf Cart Girl

**Avatar ID (Look):** `5de5fb82755e4ea198450101ae360c79` ← use this for video generation
**Group ID:** `<INSERT_GOLF_CART_GIRL_GROUP_ID_FROM_create_photo_avatar_group.py>` (Photo Avatar Group — management only; use the actual `group_id` returned by the script)
**Other Look IDs:** `0a82d07f691a4ecfb0996ddee280037a`
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

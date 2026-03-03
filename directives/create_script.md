# Directive: Create Script

Sub-directive of `create_avatar_video.md` (Step 1). Can also be used standalone.

## Goal
Produce an approved, persona-matched video script (~45 words) ready for video generation.

## Inputs
| Field | Required | Notes |
|-------|----------|-------|
| `avatar` | Yes | Selected in Step 0 of create_avatar_video.md, or chosen here if standalone |
| `tournament` | No | Auto-researched via Exa if not provided |
| `angle` | No | Claude picks dynamically from 3 generated options |

---

## Step 1: Confirm Avatar (standalone only)

If called as a sub-directive, the avatar is already selected — skip this step.

If used standalone, present the avatar list from `create_avatar_video.md` Step 0 and ask which avatar to use. Load their persona details from `directives/avatar_personas.md`.

---

## Step 2: Research the Tournament

If the user has not specified a tournament:

1. Use the Exa MCP tool to search for the next upcoming PGA Tour event:
   `"PGA Tour next tournament 2026 schedule"`
2. Extract: tournament name, dates, venue, city, and 1–2 notable facts:
   - Defending champion
   - Venue or format history
   - Player storylines (comeback, rivalry, Grand Slam chase, Ryder Cup implications)
   - Prize purse if unusually large
   - Field strength or notable absences
3. If multiple events appear, pick the soonest one by start date.
4. Also capture **venue visual context** for use in video production — write a 2–3 sentence description covering:
   - Venue name and city
   - Course type (links, parkland, desert, mountain, etc.)
   - Signature visual elements (famous hole, water hazards, elevation changes, tree coverage, grandstands)
   - Atmosphere and crowd character (boisterous, intimate, historic, party-like)

   **Examples:**
   - Bay Hill: *"Bay Hill Club & Lodge, Orlando, Florida. Arnold Palmer's classic parkland design — tree-lined fairways, signature 18th finishing over water, lush and manicured. Known for raucous Arnie's Army galleries and the dramatic closing stretch."*
   - Augusta: *"Augusta National Golf Club, Augusta, Georgia. Immaculately manicured parkland with undulating Bermuda fairways and fast bentgrass greens. Famous for azalea-lined holes, Amen Corner's drama, and near-silent, reverent galleries."*
   - Pebble Beach: *"Pebble Beach Golf Links, Monterey Peninsula, California. Iconic coastal links cut into clifftops above Stillwater Cove — ocean views on nearly every hole, crashing Pacific surf, dramatic coastal wind. The 18th hugs the shoreline."*

5. Write a brief internal summary before drafting scripts.

**Error:** If Exa returns no results, ask the user for the tournament name.

---

## Step 3: Generate 3 Script Options

Write 3 scripts in the selected avatar's voice using their style guide from `directives/avatar_personas.md`.

### Requirements (each option):
- Word count: use the selected avatar's script length from `directives/avatar_personas.md` (ranges vary — Jeff/Pro Golfer cap at 50, Bob/Bud at 55, Golf Cart Girl at 45). Never exceed the avatar's hard cap.
- Opens with a natural hook — do NOT start every script with "Hey everyone"
- Clear tournament info: viewer should know what event, when, and where
- Ends with a reason to stay engaged with the community

### Angle selection:
Choose 3 angles most appropriate for this specific tournament — not the same 3 every week.

Draw from:
- Venue or course history
- Player storyline (defending champ, Grand Slam chase, comeback, rivalry)
- Competitive stakes (FedEx Cup, Ryder Cup qualification, playoff spot)
- Unusual circumstances (first-time venue, weather, schedule change)
- Community hook (watch party, fantasy golf value, best betting angle)
- Field strength or past drama at this venue
- Hype and anticipation

### Output format:
```
Option 1 [Angle: <label>]
"<script text>"

Option 2 [Angle: <label>]
"<script text>"

Option 3 [Angle: <label>]
"<script text>"
```

---

## Step 4: User Selection and Iteration

1. Present all 3 options
2. Ask: "Which script would you like to use? Or I can rework any option or generate new variations."
3. Handle:
   - **User picks a number** → proceed to Step 5
   - **User requests a tweak** → revise, re-present, confirm
   - **User wants a different angle** → generate 1–3 new options
   - **User provides their own script** → accept as-is, proceed to Step 5
4. Do not proceed until the user has explicitly approved a script.

---

## Step 5: Output Handoff

When a script is approved:

```
## Script Approved

Avatar: [name]
Avatar ID: [id]
Orientation: [portrait | landscape]
Angle: [label]
Word count: [N]

Script: "[full approved script text]"

Venue context: "[2–3 sentence visual description of the tournament venue — course type, signature visuals, atmosphere]"

---
Ready to hand off to create_avatar_video.md Step 2.
```

Note: `voice_id` is not included — Video Agent uses the avatar's associated voice automatically.
Note: `venue_context` is used in Step 2 of create_avatar_video.md to fill in `[INSERT TOURNAMENT VENUE CONTEXT HERE]` in the prompt template.

---

## Error Cases

| Situation | Action |
|-----------|--------|
| Exa returns no upcoming tournaments | Ask user for tournament name; research directly |
| User has no preference among options | Suggest Option 1 but confirm before proceeding |
| Script runs long | Trim to 50 words max; preserve core message and persona voice |

---

## Notes

- Exa MCP is preferred over built-in WebSearch (`EXA_API_KEY` in `.env`)
- When an angle or phrase works especially well, add it to the avatar's `Example Phrases` in `avatar_personas.md`

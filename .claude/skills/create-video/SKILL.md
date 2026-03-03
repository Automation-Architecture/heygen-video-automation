---
name: create-video
description: Create a HeyGen avatar video for Golfers Unite. Use when the user says "make a video", "create a video", "generate a social post", "create an avatar video", "I want a Jeff video", "film a video", or any variant asking to produce a GU avatar video with or without a topic hint.
argument-hint: "[optional topic, e.g. The Masters 2026]"
---

# Create Avatar Video

Read and follow `directives/create_avatar_video.md` in full, starting at Step 0.

## Topic Hint

If the user provided a topic argument, it is: `$ARGUMENTS`

If `$ARGUMENTS` is non-empty, use it as the starting topic for script research in Step 1 (pass it to the Exa search query instead of searching generically). Still present the avatar menu first before doing any research.

If `$ARGUMENTS` is empty, proceed with the standard workflow — Exa will search for the next upcoming PGA Tour event.

## Reminders

- Always present the avatar menu (Step 0) and wait for selection before any script work.
- Use Exa MCP for tournament research, not WebSearch or WebFetch.
- Do not proceed past Step 0 without explicit user confirmation of the avatar choice.
- The full workflow, avatar IDs, persona templates, and visual prompts are in `directives/`.

# Agent Instructions

You operate within a 3-layer architecture: directives (what to do), orchestration (you), execution (deterministic scripts).

## This Project
HeyGen avatar video generation triggered directly from Claude Code.

**To create a video:** use `/create-video [optional topic]`, or read `directives/create_avatar_video.md` and follow it. Always present the avatar menu (Step 0) and confirm selection with the user before working on the script or triggering the workflow.

**Two render paths** (Step 2 in the directive asks the user to choose):
- **Fast path** (~1 min): `execution/generate_heygen_video_v2.py` — V2 endpoint + Avatar IV engine. Single talking-head scene with photorealistic motion. Requires `voice_id` per avatar (defined in `directives/avatar_personas.md`).
- **Cinematic path** (12–30 min): `execution/generate_heygen_video.py` — Video Agent endpoint. Multi-scene production with drone open, avatar A-roll, gallery B-roll, branded outro. Voice is auto-selected from the avatar.

**Avatar personas and prompt templates:** `directives/avatar_personas.md` defines each avatar's character, tone guide, `voice_id` (fast path), `### Fast-Path (V2) Motion Prompt`, and `### Video Agent Prompt` (cinematic path, ≤ 245 chars total with cinematic suffix).

**⚠ Video Agent is slow when queued:** Video Agent jobs take 12–30 minutes when HeyGen's queue is busy. A persistent 404 from the status endpoint does NOT mean the job failed — it means it's still queued. The poll script waits up to 30 minutes. If it times out, check the video list (`/v1/video.list`) or HeyGen dashboard. V2 fast-path videos do NOT have a 404 window.

**Avatar IDs (HeyGen):** All IDs verified. Re-validate only if avatars are modified in HeyGen (`execution/validate_avatar_id.py <id>`). Manage avatars at `app.heygen.com/avatar/my-avatars`.

| Avatar | ID | Type | Status |
|--------|-----|------|----|
| Jeff | `ccce0126b55f418e858ce9c7047eff1a` | standard avatar | ✓ verified |
| Bob Commentator | `7c5124f727b840bdb2fa66380ade0a0f` | trained photo avatar (look) | ✓ verified |
| Bud The Caddy | `35a38a2bfbfe4d5ea33f1a8b8434aa06` | talking photo | ✓ verified |
| Pro Golfer | `3c4b06f3ae6b42adb456f7022f4dc9d1` | trained photo avatar (look) | ✓ verified |
| Golf Cart Girl | `5de5fb82755e4ea198450101ae360c79` | trained photo avatar (look) | ✓ verified |

## The 3-Layer Architecture

**Layer 1 – Directives** (`directives/`)
SOPs in Markdown. Define goals, inputs, tools, outputs, edge cases.

**Layer 2 – Orchestration (you)**
Read directives, call execution tools in the right order, handle errors, update directives with learnings.

**Layer 3 – Execution** (`execution/`)
Deterministic Python scripts. Handle API calls, polling, file operations.

## Operating Principles

**1. Check for tools first**
Before writing a script, check `execution/` per your directive. Only create new scripts if none exist.

**2. Self-anneal when things break**
- Read error message and stack trace
- Fix the script and test it again (unless it uses paid tokens/credits/etc—in which case check with user first)
- Update the directive with what you learned (API limits, timing, edge cases)

**3. Update directives as you learn**
Directives are living documents. When you discover API constraints, better approaches, common errors, or timing expectations—update the directive. Don't create or overwrite directives without asking unless explicitly told to.

**4. Keep README.md in sync**
When user-facing behavior changes — new avatars, script flow changes, API endpoint updates, setup requirements — update `README.md` alongside the relevant directive. The README is the human-readable front door to this project and should always reflect how the system actually works.

## Self-Annealing Loop

Errors are learning opportunities. When something breaks:
1. Fix the error
2. Update the script
3. Test it
4. Update the directive
5. System is now stronger

## File Organization

- `directives/` — SOPs (the instruction set)
- `execution/` — Python scripts (the tools)
- `docs/` — API and platform reference documentation
- `.tmp/` — Intermediate files, never committed, always regeneratable
- `.env` — API keys and config
- `.mcp.json` — Project-scoped MCP config (empty; defers to global config at `~/.claude/mcp.json`)


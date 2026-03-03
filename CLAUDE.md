# Agent Instructions

You operate within a 3-layer architecture: directives (what to do), orchestration (you), execution (deterministic scripts).

## This Project
HeyGen avatar video generation triggered directly from Claude Code.

**To create a video:** read `directives/create_avatar_video.md` and follow it. Always present the avatar menu (Step 0) and confirm selection with the user before working on the script or triggering the workflow.

**Avatar personas and prompt templates:** `directives/avatar_personas.md` defines each avatar's character, tone guide, and a ready-to-use `### Video Agent Prompt` template with full cinematic production direction — 4-scene structure (venue B-roll open, avatar A-roll, course action B-roll, branded outro), camera angle guidance (drone, low, eye-level, gallery POV), lighting direction (natural sunlight, dappled shadows), and persona-specific location flavoring. Orchestration consists of finding the selected avatar's template and making two substitutions: `[INSERT APPROVED SCRIPT HERE]` with the approved script, and `[INSERT TOURNAMENT VENUE CONTEXT HERE]` with the venue visual context from tournament research. No manual prompt engineering needed.

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


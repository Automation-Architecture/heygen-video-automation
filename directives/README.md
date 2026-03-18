# Directives

SOPs (Standard Operating Procedures) in Markdown. These define goals, inputs, tools, outputs, and edge cases for the orchestration layer (Claude Code or Codex).

Directives are living documents — update them when you discover API constraints, better approaches, or timing expectations.

## Files

| Directive | Purpose |
|-----------|---------|
| `create_avatar_video.md` | Main workflow: avatar selection → script → render → poll → Slack notify (Steps 0–4) |
| `create_script.md` | Sub-directive: PGA Tour research via Exa + 3-option script drafting with dynamic angles |
| `avatar_personas.md` | Character profiles, tone guides, voice IDs, Video Agent prompt templates, fast-path motion prompts |
| `upgrade_photo_avatar.md` | Upgrade path: talking photo → trained Photo Avatar Group with Avatar IV motion |

# OpenAI Codex Skills Reference

Source: https://developers.openai.com/codex/skills

## What Are Skills?

Skills extend Codex with task-specific capabilities by packaging instructions, resources, and optional scripts. They build on the [open agent skills standard](https://agentskills.io). Skills are available in the Codex CLI, IDE extension, and Codex app.

**Progressive disclosure:** Codex starts with each skill's metadata (`name`, `description`, file path, and optional metadata from `agents/openai.yaml`). It loads the full `SKILL.md` instructions only when it decides to use a skill.

## Directory Structure

```
my-skill/
  SKILL.md           # Required: instructions + metadata
  scripts/           # Optional: executable code
  references/        # Optional: documentation
  assets/            # Optional: templates, resources
  agents/
    openai.yaml      # Optional: UI config, policy, dependencies
```

## SKILL.md Format

```markdown
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```

- `name` and `description` are **required** frontmatter fields.
- The description drives implicit matching — write it with clear scope and boundaries.
- Body contains imperative instructions with explicit inputs and outputs.

## agents/openai.yaml (Optional Metadata)

```yaml
interface:
  display_name: "Optional user-facing name"
  short_description: "Optional user-facing description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt to use the skill with"

policy:
  allow_implicit_invocation: false  # default: true

dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      description: "OpenAI Docs MCP server"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
```

### Fields

| Section | Field | Purpose |
|---------|-------|---------|
| `interface` | `display_name` | User-facing name in Codex app |
| `interface` | `short_description` | User-facing description |
| `interface` | `icon_small` / `icon_large` | Asset paths for icons |
| `interface` | `brand_color` | Hex color value |
| `interface` | `default_prompt` | Surrounding context prompt |
| `policy` | `allow_implicit_invocation` | `false` = explicit `$skill` only; default `true` |
| `dependencies` | `tools` | Tool requirements (e.g., MCP servers) |

## Where to Save Skills (Discovery Paths)

Codex reads skills from four scope levels, scanning `.agents/skills` directories:

| Scope | Path | Use Case |
|-------|------|----------|
| REPO | `$CWD/.agents/skills` | Current working directory |
| REPO | `$CWD/../.agents/skills` | Parent folder (nested repos) |
| REPO | `$REPO_ROOT/.agents/skills` | Repository root (team-shared) |
| USER | `$HOME/.agents/skills` | Personal skills across all repos |
| ADMIN | `/etc/codex/skills` | Machine/container system defaults |
| SYSTEM | Bundled with Codex | OpenAI-provided defaults |

- Codex supports **symlinked** skill folders.
- If two skills share the same `name`, Codex **does not merge** them — both appear in skill selectors.
- Codex detects new skills automatically; restart if one doesn't appear.

## Invocation

### Explicit
Reference skills via `/skills` command or `$skill-name` mention:
```
$create-video The Masters 2026
```

### Implicit
Codex automatically selects skills when the user's task matches the skill `description`. Controlled by `policy.allow_implicit_invocation` (default: `true`).

### Via API (App Server)
```json
{
  "method": "turn/start",
  "id": 101,
  "params": {
    "threadId": "thread-1",
    "input": [
      {
        "type": "text",
        "text": "$skill-creator Add a new skill for triaging flaky CI."
      },
      {
        "type": "skill",
        "name": "skill-creator",
        "path": "/Users/me/.codex/skills/skill-creator/SKILL.md"
      }
    ]
  }
}
```

## Installing Skills

Use the built-in installer:
```bash
$skill-installer linear
```

### Manual Configuration

In `~/.codex/config.toml`:
```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Restart Codex after modifying configuration.

## Best Practices

- Keep each skill focused on one job.
- Prefer instructions over scripts unless you need deterministic behavior or external tooling.
- Write imperative steps with explicit inputs and outputs.
- Test prompts against skill descriptions to confirm trigger behavior.
- Write descriptions with clear scope and boundaries for reliable implicit matching.

## External References

- [OpenAI Skills Repository](https://github.com/openai/skills)
- [Agent Skills Specification](https://agentskills.io/specification)

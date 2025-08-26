# Simple Project-Level Hooks

Hooks can be configured globally or per-project. Project hooks override global ones.

## Hook Locations

- **Global**: `~/.claude/settings.json` (all projects)
- **Project**: `.claude/settings.json` (this project only)

## Basic Examples

### Biome Project
`.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [{
          "type": "command",
          "command": "echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_input.file_path // empty' | xargs -r biome check --apply"
        }]
      }
    ]
  }
}
```

### Prettier Project
`.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [{
          "type": "command",
          "command": "echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_input.file_path // empty' | xargs -r prettier --write"
        }]
      }
    ]
  }
}
```

### TypeScript Project with Tests
`.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [{
          "type": "command",
          "command": "echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_input.file_path // empty' | xargs -r prettier --write"
        }]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [{
          "type": "command",
          "command": "npm run typecheck"
        }]
      }
    ]
  }
}
```

### Rust Project
`.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [{
          "type": "command",
          "command": "echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_input.file_path // empty' | grep -E '\\.rs$' | xargs -r rustfmt"
        }]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "cargo clippy --fix --allow-dirty && cargo test"
        }]
      }
    ]
  }
}
```

## Global Safety Hooks

Keep these in `~/.claude/settings.json` for all projects:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [{
          "type": "command",
          "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', '.git/', 'node_modules/']) else 0)\""
        }]
      }
    ]
  }
}
```

## Setup

1. Create `.claude/` directory in your project
2. Add `settings.json` with hooks for your tools
3. Commit to version control with the project

That's it. Simple, project-specific hooks that work with whatever tools you're using.
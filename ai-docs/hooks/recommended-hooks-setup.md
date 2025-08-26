# Recommended Claude Code Hooks for Multi-Agent Development

This guide provides tested, production-ready hooks that complement the multi-agent system and enforce quality standards automatically.

## Essential Quality Gates

### 1. Automatic Linting & Formatting (PostToolUse)

**Purpose**: Ensure consistent code formatting after any file modification by agents.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_input.file_path // empty' | while read -r file_path; do if [[ \"$file_path\" =~ \\.(ts|tsx|js|jsx)$ ]] && [[ -f \"$file_path\" ]]; then npx prettier --write \"$file_path\" 2>/dev/null || echo \"No prettier config found for $file_path\"; fi; done"
          }
        ]
      }
    ]
  }
}
```

**Benefits**: 
- Eliminates formatting inconsistencies between agents
- Ensures code follows project style guidelines
- Reduces noise in code reviews

### 2. Comprehensive Quality Validation (PreToolUse)

**Purpose**: Block dangerous operations and validate file modifications.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command", 
            "command": "python3 -c \"import json, sys, os; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); protected=['.env', 'package-lock.json', 'pnpm-lock.yaml', '.git/', 'node_modules/']; sys.exit(2 if any(p in path for p in protected) else 0)\""
          }
        ]
      }
    ]
  }
}
```

**Benefits**:
- Prevents accidental modification of critical files
- Protects lock files and environment configurations
- Provides safety guardrails for autonomous agent operations

## Agent-Specific Automation

### 3. Post-Frontend Quality Check (SubagentStop)

**Purpose**: Automatically trigger comprehensive testing after UI changes.

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "frontend-ui-specialist",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v npm >/dev/null 2>&1 && [[ -f package.json ]]; then echo '🎨 Frontend changes detected - running quality checks...'; npm run lint --silent && npm run typecheck --silent && echo '✅ Quality checks passed'; else echo '⚠️  No npm/package.json found, skipping quality checks'; fi"
          }
        ]
      }
    ]
  }
}
```

### 4. Backend Validation (SubagentStop)

**Purpose**: Run database and backend validation after backend agent changes.

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "backend-database-engineer", 
        "hooks": [
          {
            "type": "command",
            "command": "if [[ -f package.json ]] && grep -q '\"typecheck\"' package.json; then echo '🗄️  Backend changes detected - validating...'; npm run typecheck --silent && echo '✅ Backend validation passed'; else echo 'ℹ️  No typecheck script found'; fi"
          }
        ]
      }
    ]
  }
}
```

## Documentation Automation

### 5. Auto-Update Documentation (PostToolUse)

**Purpose**: Keep ai-docs/ current when architectural files change.

Create `.claude/hooks/update_docs.py`:

```python
#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

# Files that trigger documentation updates
WATCHED_FILES = {
    'package.json': 'dependencies changed',
    'tsconfig.json': 'TypeScript config modified', 
    'tailwind.config.js': 'styling config updated',
    'next.config.js': 'Next.js config changed',
    'drizzle.config.ts': 'database config modified'
}

try:
    data = json.load(sys.stdin)
    file_path = data.get('tool_input', {}).get('file_path', '')
    
    if not file_path:
        sys.exit(0)
        
    filename = os.path.basename(file_path)
    
    if filename in WATCHED_FILES:
        print(f"📚 {WATCHED_FILES[filename]} - consider updating relevant ai-docs/")
        
        # Optional: Touch a marker file to remind about documentation updates
        docs_dir = Path('./ai-docs')
        if docs_dir.exists():
            marker = docs_dir / '.needs-update'
            marker.write_text(f"{file_path}: {WATCHED_FILES[filename]}\n")
            
except Exception as e:
    print(f"Documentation hook error: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block operations on doc hook failures
```

Hook configuration:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/update_docs.py"
          }
        ]
      }
    ]
  }
}
```

## Notification & Feedback

### 6. Agent Activity Notifications

**Purpose**: Desktop notifications for long-running agent operations.

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v notify-send >/dev/null 2>&1; then notify-send 'Claude Agent' \"$(echo \"$CLAUDE_HOOK_DATA\" | jq -r '.subagent_name // \"Agent\"') completed task\"; fi"
          }
        ]
      }
    ]
  }
}
```

### 7. Build Validation (Stop)

**Purpose**: Run full project validation when agents finish major work.

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ -f package.json ]] && grep -q '\"build\"' package.json; then echo '🔨 Running final build check...'; timeout 60 npm run build --silent >/dev/null 2>&1 && echo '✅ Build successful' || echo '⚠️  Build failed - check for issues'; fi"
          }
        ]
      }
    ]
  }
}
```

## Advanced Hooks

### 8. Screenshot After UI Changes

**Purpose**: Automatically capture UI state after frontend agent modifications.

Create `.claude/hooks/ui_screenshot.py`:

```python
#!/usr/bin/env python3
import json
import sys
import os
import subprocess
from datetime import datetime

try:
    data = json.load(sys.stdin)
    file_path = data.get('tool_input', {}).get('file_path', '')
    
    # Only screenshot for UI-related file changes
    ui_extensions = ['.tsx', '.jsx', '.css', '.scss', '.vue', '.svelte']
    
    if not any(file_path.endswith(ext) for ext in ui_extensions):
        sys.exit(0)
        
    # Create screenshots directory
    screenshot_dir = '.claude/screenshots'
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"ui_change_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)
    
    print(f"📸 UI file changed: {os.path.basename(file_path)}")
    print(f"Consider taking a screenshot to document changes: {filename}")
    
except Exception as e:
    print(f"Screenshot hook error: {e}", file=sys.stderr)
    sys.exit(0)
```

### 9. Performance Monitoring

**Purpose**: Track agent performance and identify bottlenecks.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ): START: $(echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_name')\" >> ~/.claude/performance.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*", 
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ): END: $(echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_name')\" >> ~/.claude/performance.log"
          }
        ]
      }
    ]
  }
}
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Make sure required tools are available
npm install -g prettier  # For formatting hooks
pip3 install --user jq   # For JSON processing (if not system-installed)

# Create hooks directory
mkdir -p .claude/hooks
chmod +x .claude/hooks/*.py  # Make Python hooks executable
```

### 2. Configure Hooks

Use the `/hooks` command in Claude Code:

1. Run `/hooks`
2. Select the hook event (PreToolUse, PostToolUse, etc.)
3. Add matchers for specific tools
4. Paste the hook commands from above
5. Choose user or project settings

### 3. Test Your Hooks

```bash
# Test with a simple file edit
echo "console.log('test');" > test.js

# Check if formatting hook worked
cat test.js  # Should be prettier-formatted if configured

# Check performance log
tail ~/.claude/performance.log
```

## Best Practices

### Hook Safety
- Always include error handling in custom scripts
- Use `sys.exit(0)` in Python hooks to avoid blocking operations
- Test hooks thoroughly before deploying to teams

### Performance Considerations  
- Keep hooks lightweight and fast
- Use timeouts for potentially long-running operations
- Consider async execution for non-blocking operations

### Team Adoption
- Start with essential quality gates (linting, formatting)
- Gradually add more sophisticated automation
- Document hook purposes and maintenance procedures
- Version control hook scripts in `.claude/hooks/`

### Debugging Hooks
- Check `~/.claude/claude.log` for hook execution details
- Add debug output to hook scripts during development
- Use the performance monitoring hook to identify slow operations

These hooks create a robust, automated quality system that complements your multi-agent development workflow while maintaining the flexibility to adapt to different project requirements.
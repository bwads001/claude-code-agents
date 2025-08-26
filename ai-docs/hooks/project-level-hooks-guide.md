# Project-Level Hooks Guide

This guide provides flexible, project-aware hook configurations that adapt to different tooling choices (ESLint/Prettier, Biome, Oxlint, etc.).

## Philosophy: Detect, Don't Dictate

Instead of enforcing specific tools globally, hooks should detect what's available in each project and use the appropriate commands.

## Smart Detection Hook Templates

### 1. Universal Format/Lint Hook

Create `.claude/hooks/smart_format.sh`:

```bash
#!/usr/bin/env bash
# Smart formatter that detects available tools

FILE_PATH=$(echo "$CLAUDE_HOOK_DATA" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to check if config file exists
config_exists() {
  [[ -f "$1" ]] || [[ -f ".$1" ]]
}

# Detect and run appropriate formatter
format_file() {
  local file="$1"
  local ext="${file##*.}"
  
  # Check for Biome first (it's fast!)
  if config_exists "biome.json" && command_exists biome; then
    echo "🚀 Formatting with Biome"
    biome format --write "$file" 2>/dev/null
    return
  fi
  
  # Check for Oxlint (Rust ecosystem)
  if command_exists oxlint && [[ -f ".oxlintrc.json" ]]; then
    echo "🦀 Linting with Oxlint"
    oxlint "$file" --fix 2>/dev/null
    return
  fi
  
  # Check for Prettier
  if config_exists "prettierrc" && command_exists prettier; then
    echo "✨ Formatting with Prettier"
    prettier --write "$file" 2>/dev/null
    return
  fi
  
  # Check for ESLint
  if config_exists "eslintrc" && command_exists eslint; then
    echo "📝 Linting with ESLint"
    eslint --fix "$file" 2>/dev/null
    return
  fi
  
  # Language-specific fallbacks
  case "$ext" in
    rs)
      if command_exists rustfmt; then
        echo "🦀 Formatting with rustfmt"
        rustfmt "$file" 2>/dev/null
      fi
      ;;
    go)
      if command_exists gofmt; then
        echo "🐹 Formatting with gofmt"
        gofmt -w "$file" 2>/dev/null
      fi
      ;;
    py)
      if command_exists black; then
        echo "⚫ Formatting with Black"
        black "$file" 2>/dev/null
      elif command_exists ruff; then
        echo "⚡ Formatting with Ruff"
        ruff format "$file" 2>/dev/null
      fi
      ;;
  esac
}

# Only format code files
if [[ "$FILE_PATH" =~ \.(ts|tsx|js|jsx|rs|go|py|vue|svelte)$ ]]; then
  format_file "$FILE_PATH"
fi
```

### 2. Project-Aware Quality Gates

Create `.claude/hooks/project_quality_check.py`:

```python
#!/usr/bin/env python3
"""
Project-aware quality checker that adapts to available tools
"""
import json
import os
import sys
import subprocess
from pathlib import Path

def command_exists(cmd):
    """Check if a command exists"""
    return subprocess.run(
        ["which", cmd], 
        capture_output=True, 
        text=True
    ).returncode == 0

def find_package_json():
    """Find package.json in current or parent directories"""
    current = Path.cwd()
    while current != current.parent:
        pkg_json = current / "package.json"
        if pkg_json.exists():
            return pkg_json
        current = current.parent
    return None

def get_npm_scripts():
    """Extract available npm scripts"""
    pkg_json = find_package_json()
    if not pkg_json:
        return {}
    
    try:
        with open(pkg_json) as f:
            data = json.load(f)
            return data.get("scripts", {})
    except:
        return {}

def detect_project_stack():
    """Detect the project's tech stack and available tools"""
    stack = {
        "formatter": None,
        "linter": None,
        "type_checker": None,
        "test_runner": None,
        "build_tool": None
    }
    
    # Check for Biome (all-in-one)
    if Path("biome.json").exists():
        stack["formatter"] = "biome"
        stack["linter"] = "biome"
    
    # Check for Oxlint
    elif Path(".oxlintrc.json").exists():
        stack["linter"] = "oxlint"
    
    # Check for traditional JS tools
    elif Path(".prettierrc").exists() or Path(".prettierrc.json").exists():
        stack["formatter"] = "prettier"
    
    if Path(".eslintrc").exists() or Path(".eslintrc.json").exists():
        stack["linter"] = "eslint"
    
    # Check package.json scripts
    scripts = get_npm_scripts()
    
    # Detect from npm scripts
    if "lint" in scripts:
        stack["linter"] = "npm run lint"
    if "format" in scripts:
        stack["formatter"] = "npm run format"
    if "typecheck" in scripts or "type-check" in scripts:
        stack["type_checker"] = scripts.get("typecheck", "npm run type-check")
    if "test" in scripts:
        stack["test_runner"] = "npm test"
    if "build" in scripts:
        stack["build_tool"] = "npm run build"
    
    # Rust project detection
    if Path("Cargo.toml").exists():
        stack["formatter"] = "cargo fmt"
        stack["linter"] = "cargo clippy"
        stack["test_runner"] = "cargo test"
        stack["build_tool"] = "cargo build"
    
    # Go project detection
    if Path("go.mod").exists():
        stack["formatter"] = "go fmt"
        stack["linter"] = "golangci-lint" if command_exists("golangci-lint") else "go vet"
        stack["test_runner"] = "go test"
        stack["build_tool"] = "go build"
    
    # Python project detection  
    if Path("pyproject.toml").exists():
        if command_exists("ruff"):
            stack["formatter"] = "ruff format"
            stack["linter"] = "ruff check"
        elif command_exists("black"):
            stack["formatter"] = "black ."
        
        if command_exists("mypy"):
            stack["type_checker"] = "mypy"
        
        if command_exists("pytest"):
            stack["test_runner"] = "pytest"
    
    return stack

def run_quality_checks():
    """Run appropriate quality checks for the project"""
    stack = detect_project_stack()
    
    print(f"🔍 Detected project stack: {json.dumps(stack, indent=2)}")
    
    failed_checks = []
    
    # Run available checks
    for check_type, command in stack.items():
        if command:
            print(f"Running {check_type}: {command}")
            try:
                if command.startswith("npm"):
                    result = subprocess.run(command.split(), capture_output=True, text=True)
                else:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    failed_checks.append(check_type)
                    print(f"❌ {check_type} failed")
                else:
                    print(f"✅ {check_type} passed")
            except Exception as e:
                print(f"⚠️  Could not run {check_type}: {e}")
    
    if failed_checks:
        print(f"\n⚠️  Quality checks failed: {', '.join(failed_checks)}")
        sys.exit(1)
    else:
        print("\n✅ All quality checks passed!")

if __name__ == "__main__":
    run_quality_checks()
```

### 3. Project-Specific Hook Configuration

Instead of global hooks, each project gets `.claude/hooks.json`:

```json
{
  "project": "my-biome-project",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/smart_format.sh"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/project_quality_check.py"
          }
        ]
      }
    ]
  }
}
```

## Tool-Specific Optimizations

### Biome (Fast & Modern)
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "command": "if [[ -f biome.json ]]; then biome check --apply \"$file_path\"; fi"
          }
        ]
      }
    ]
  }
}
```

### Oxlint (Rust Speed)
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "command": "if command -v oxlint >/dev/null && [[ -f .oxlintrc.json ]]; then oxlint --fix \"$file_path\"; fi"
          }
        ]
      }
    ]
  }
}
```

### Mixed Ecosystem Projects
For projects using multiple languages:

```bash
#!/usr/bin/env bash
# Polyglot formatter hook

FILE="$1"
EXT="${FILE##*.}"

case "$EXT" in
  # JavaScript/TypeScript
  js|jsx|ts|tsx)
    if [[ -f biome.json ]]; then
      biome format --write "$FILE"
    elif command -v oxlint >/dev/null; then
      oxlint --fix "$FILE"
    elif [[ -f .prettierrc ]]; then
      prettier --write "$FILE"
    fi
    ;;
    
  # Rust
  rs)
    cargo fmt -- "$FILE"
    cargo clippy --fix -- "$FILE"
    ;;
    
  # Go
  go)
    gofmt -w "$FILE"
    golangci-lint run --fix "$FILE"
    ;;
    
  # Python
  py)
    if command -v ruff >/dev/null; then
      ruff format "$FILE"
      ruff check --fix "$FILE"
    elif command -v black >/dev/null; then
      black "$FILE"
    fi
    ;;
esac
```

## Project Templates

### Quick Setup Script

Create `.claude/setup-hooks.sh`:

```bash
#!/usr/bin/env bash

echo "🎣 Setting up project-aware hooks..."

# Detect primary language/framework
if [[ -f "package.json" ]]; then
  echo "📦 JavaScript/TypeScript project detected"
  
  # Check for formatter preference
  if [[ -f "biome.json" ]]; then
    echo "🚀 Using Biome for formatting/linting"
    FORMATTER="biome"
  elif [[ -f ".oxlintrc.json" ]]; then
    echo "🦀 Using Oxlint for linting"
    FORMATTER="oxlint"
  elif [[ -f ".prettierrc" ]]; then
    echo "✨ Using Prettier for formatting"
    FORMATTER="prettier"
  else
    echo "🤔 No formatter detected, skipping format hooks"
    FORMATTER="none"
  fi
  
elif [[ -f "Cargo.toml" ]]; then
  echo "🦀 Rust project detected"
  FORMATTER="rustfmt"
  
elif [[ -f "go.mod" ]]; then
  echo "🐹 Go project detected"
  FORMATTER="gofmt"
  
elif [[ -f "pyproject.toml" ]]; then
  echo "🐍 Python project detected"
  FORMATTER="ruff"
fi

# Create appropriate hooks configuration
cat > .claude/hooks.json <<EOF
{
  "project": "$(basename $PWD)",
  "detected_formatter": "$FORMATTER",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/smart_format.sh"
          }
        ]
      }
    ]
  }
}
EOF

echo "✅ Project hooks configured for $FORMATTER"
```

## Best Practices

1. **Keep detection logic in hooks**, not in global config
2. **Fail gracefully** when tools aren't available
3. **Cache detection results** for performance (optional)
4. **Version control** `.claude/hooks/` directory with project
5. **Document** tool preferences in project README

## Example: Multi-Tool Project

```
my-project/
├── .claude/
│   ├── hooks/
│   │   ├── smart_format.sh      # Auto-detects formatter
│   │   ├── quality_check.py     # Runs available checks
│   │   └── setup.sh             # Initial setup
│   └── hooks.json               # Project-specific config
├── biome.json                   # Your current formatter choice
├── .prettierrc.json            # Fallback if Biome isn't installed
└── package.json                # Scripts for any tool
```

This way, you can experiment with new tools without breaking your workflow!
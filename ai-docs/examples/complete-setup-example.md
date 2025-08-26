# Complete Multi-Agent + Hooks Setup Example

This example shows how to set up the complete development system for a Next.js project using the git-based agent system.

## Directory Structure

```
my-project/
├── .claude/
│   ├── hooks/            # Project-specific hook scripts
│   └── ai-docs/         # Project documentation
├── ~/.claude/           # Git repository with agent system
│   ├── agents/          # 8 specialized agents + orchestration
│   ├── ai-docs/         # Global documentation & examples
│   └── settings.json    # Hook configurations
└── src/                 # Project source code
```

## Step 1: Install Agent System (Git-based)

```bash
# Clone the agent repository to ~/.claude
git clone git@github.com:bwads001/claude-code-agents.git ~/.claude

# Verify installation
ls ~/.claude/agents/
# Should show:
# - CLAUDE.md                    # Main orchestration patterns
# - project-manager.md           # Planning & context management
# - feature-architect-planner.md # Complex feature planning
# - backend-database-engineer.md # Database, APIs, server logic
# - frontend-ui-specialist.md    # UI components, styling
# - code-quality-reviewer.md     # Testing, quality gates
# - documentation-specialist.md  # Research, technical docs
# - file-refactor-organizer.md   # Code organization
# - git-workflow-specialist.md   # Branch management, worktrees
```

## Step 2: Set Up Project Documentation Structure

```bash
# Create project ai-docs structure  
mkdir -p .claude/ai-docs/{architecture,features,troubleshooting,planning/{active,backlog,completed}}

# Create initial CLAUDE.md with project context
cat > CLAUDE.md << 'EOF'
# CLAUDE.md

This file provides guidance to Claude Code when working with this Next.js project.

## Development Commands

```bash
npm run dev         # Start development server  
npm run build       # Production build
npm run lint        # ESLint checks
npm run typecheck   # TypeScript validation
npm test           # Run test suite
```

## Architecture Overview

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS v4
- **Database**: PostgreSQL with Drizzle ORM
- **State**: Zustand for client state
- **UI**: shadcn/ui components

## Quality Gates (REQUIRED)

ALL code changes must pass:
```bash
npm run lint && npm run typecheck && npm run test
```

## Agent Usage

This project uses specialized Claude Code agents:
- Project status & planning: Use `project-manager` for context and progress tracking
- Complex features: Use `feature-architect-planner` for implementation planning
- UI/styling work: Use `frontend-ui-specialist` for components and design
- Database/backend: Use `backend-database-engineer` for APIs and data
- Code review: Use `code-quality-reviewer` with comprehensive testing
- Research/docs: Use `documentation-specialist` for library research
- Large files (>300 lines): Use `file-refactor-organizer` for organization
- Git workflows: Use `git-workflow-specialist` for branching and worktrees

Orchestration happens at the main Claude level using patterns in ~/.claude/agents/CLAUDE.md
EOF
```

## Step 3: Configure Essential Hooks

Create hook configuration in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_input.file_path // empty' | while read -r file_path; do if [[ \"$file_path\" =~ \\.(ts|tsx|js|jsx)$ ]] && [[ -f \"$file_path\" ]]; then npx prettier --write \"$file_path\" 2>/dev/null && echo \"✅ Formatted $file_path\"; fi; done"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write", 
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); protected=['.env', 'package-lock.json', 'pnpm-lock.yaml', '.git/']; sys.exit(2 if any(p in path for p in protected) else 0)\""
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "frontend-ui-specialist",
        "hooks": [
          {
            "type": "command", 
            "command": "echo '🎨 Frontend changes - running quality checks...' && npm run lint --silent && npm run typecheck --silent && echo '✅ Quality passed'"
          }
        ]
      },
      {
        "matcher": "backend-database-engineer",
        "hooks": [
          {
            "type": "command",
            "command": "echo '🗄️ Backend changes - validating...' && npm run typecheck --silent && echo '✅ Backend validated'"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ -f package.json ]] && grep -q '\"build\"' package.json; then echo '🔨 Final build check...' && timeout 30 npm run build --silent >/dev/null 2>&1 && echo '✅ Build successful' || echo '⚠️ Build failed'; fi"
          }
        ]
      }
    ]
  }
}
```

## Step 4: Create Custom Hook Scripts

```bash
# Create hooks directory
mkdir -p .claude/hooks

# Documentation update hook
cat > .claude/hooks/update_docs.py << 'EOF'
#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

WATCHED_FILES = {
    'package.json': 'dependencies changed',
    'tsconfig.json': 'TypeScript config modified',
    'tailwind.config.js': 'styling config updated', 
    'next.config.js': 'Next.js config changed'
}

try:
    data = json.load(sys.stdin)
    file_path = data.get('tool_input', {}).get('file_path', '')
    filename = os.path.basename(file_path) if file_path else ''
    
    if filename in WATCHED_FILES:
        print(f"📚 {WATCHED_FILES[filename]} - consider updating ai-docs/")
        
except Exception as e:
    sys.exit(0)  # Don't block on documentation hook errors
EOF

chmod +x .claude/hooks/update_docs.py
```

## Step 5: Example Workflow Usage

### Adding a New Feature

```bash
# 1. Check project status and create implementation plan
> Use project-manager to review current project status, then feature-architect-planner to create a detailed user dashboard implementation plan.

# 2. Orchestrate implementation from main thread
> Based on the planning document, implement the user dashboard by coordinating:
> - backend-database-engineer for analytics schema and APIs  
> - frontend-ui-specialist for dashboard UI components
> - code-quality-reviewer for comprehensive testing
> - git-workflow-specialist for feature branch management

# This follows orchestration patterns in ~/.claude/agents/CLAUDE.md
```

### Integrating a New Library

```bash  
# Use documentation specialist first
> Use the documentation-specialist to research integrating React Query and create a comprehensive guide in ai-docs/

# Then coordinate implementation from main thread
> Implement React Query integration by coordinating backend-database-engineer and frontend-ui-specialist based on the research guide
```

### UI Enhancement Iteration

```bash
# Start the QA ↔ Frontend feedback loop
> Use the frontend-ui-specialist to improve the dashboard mobile responsiveness

# This triggers:  
# 1. UI changes by frontend-ui-specialist
# 2. Automatic formatting via PostToolUse hook
# 3. Quality checks via SubagentStop hook
# 4. Playwright testing by code-quality-reviewer
# 5. Iterative improvements based on QA feedback
```

## Step 6: Monitoring & Maintenance

### Check Hook Performance
```bash
# View recent hook activity
tail -f ~/.claude/claude.log | grep hook

# Monitor build status  
grep "Build" ~/.claude/claude.log | tail -10
```

### Update Documentation
```bash
# Check for documentation update reminders
if [[ -f .claude/ai-docs/.needs-update ]]; then
  cat .claude/ai-docs/.needs-update
fi
```

### Agent Performance
```bash
# See which agents are being used most
grep -o 'subagent_name.*' ~/.claude/claude.log | sort | uniq -c | sort -nr
```

## Advanced Customizations

### Project-Specific Agents

Create `.claude/agents/project-specialist.md`:

```markdown
---
name: project-specialist  
description: Expert in this specific project's patterns and business logic. Use for project-specific optimizations and domain knowledge questions.
tools: Read, Grep, Glob, Edit
---

You are an expert in this Next.js project's specific patterns and requirements.

Key project context:
- Uses App Router with Server Components by default
- Custom authentication with next-auth
- Multi-tenant architecture with org-based routing
- Real-time features with WebSockets

Always check existing patterns in the codebase before implementing new features.
```

### Custom Quality Gates

Add project-specific validation:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_HOOK_DATA\" | jq -e '.tool_input.file_path | test(\"\\\\.tsx?$\")' >/dev/null; then echo \"$CLAUDE_HOOK_DATA\" | jq -r '.tool_input.content' | grep -q 'console.log' && echo '⚠️ Console.log detected in TypeScript file' && exit 2; fi; exit 0"
          }
        ]
      }
    ]
  }
}
```

This complete setup creates a sophisticated, automated development environment where:

1. **Agents handle specialized tasks** with domain expertise
2. **Hooks enforce quality** and maintain consistency automatically  
3. **Documentation stays current** through automated reminders
4. **Quality gates prevent issues** before they reach production
5. **Performance is monitored** to optimize the development process

The result is an autonomous development system where the main Claude thread orchestrates specialized agents while hooks maintain high code quality and enable rapid, reliable feature development.
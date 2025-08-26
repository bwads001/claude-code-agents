# Hook Development Guide for Multi-Agent Workflows

This guide shows how to create custom Claude Code hooks that enhance the multi-agent orchestration system with automated quality gates, notifications, and workflow automation.

## Hook System Overview

Hooks are shell commands that execute automatically at specific points in Claude Code's lifecycle. In multi-agent workflows, hooks provide:

- **Quality Gates**: Automatic validation after agent work
- **Agent Coordination**: Triggering follow-up agents based on changes  
- **Context Preservation**: Adding project state to agent invocations
- **Workflow Automation**: Reducing manual orchestration overhead

## Hook Events for Multi-Agent Systems

### PreToolUse Hooks
**Trigger**: Before any tool execution (including agent invocations)  
**Use Cases**: 
- Block dangerous operations before agents execute them
- Add context before agent starts working
- Validate agent inputs and permissions

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-agent-context.py"
          }
        ]
      }
    ]
  }
}
```

### PostToolUse Hooks  
**Trigger**: After tool execution completes  
**Use Cases**:
- Quality validation after agent work
- Automatic formatting/cleanup
- Trigger follow-up agents
- Update project documentation

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command", 
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-edit-quality.py"
          }
        ]
      }
    ]
  }
}
```

### SubagentStop Hooks
**Trigger**: When agent (Task tool) completes  
**Use Cases**:
- Validate agent deliverables 
- Update planning documents
- Trigger next agent in sequence
- Quality gates specific to agent work

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "backend-database-engineer",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-backend-changes.py"
          }
        ]
      }
    ]
  }
}
```

### UserPromptSubmit Hooks
**Trigger**: When user submits prompt, before Claude processes it  
**Use Cases**:
- Add current project context to prompts
- Load active planning documents  
- Inject environment status
- Block sensitive prompts

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/inject-project-context.py"
          }
        ]
      }
    ]
  }
}
```

### Stop Hooks
**Trigger**: When main Claude thread finishes responding  
**Use Cases**:
- Final quality validation
- Update project status
- Trigger automated follow-up tasks
- Archive completed work

## Hook Configuration Patterns

### Project-Specific Hook Scripts

Store hook scripts in `.claude/hooks/` and reference them using `$CLAUDE_PROJECT_DIR`:

```bash
# Create hooks directory
mkdir -p .claude/hooks

# Store project-specific hook
cat > .claude/hooks/agent-quality-gate.py << 'EOF'
#!/usr/bin/env python3
"""Quality gate for agent outputs"""
import json
import sys
import subprocess

# Load hook input
data = json.load(sys.stdin)
tool_name = data.get("tool_name", "")

# Run project-specific quality checks
if tool_name == "Task":  # Agent execution
    # Run linting, type checking, tests
    result = subprocess.run(["npm", "run", "lint"], capture_output=True)
    if result.returncode != 0:
        print("Quality gate failed: Linting errors found", file=sys.stderr)
        print(result.stderr.decode(), file=sys.stderr)
        sys.exit(2)  # Block with feedback to Claude
EOF

chmod +x .claude/hooks/agent-quality-gate.py
```

### Configuration in Settings
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/agent-quality-gate.py"
          }
        ]
      }
    ]
  }
}
```

## Multi-Agent Hook Patterns

### Agent Context Injection (Cheat Codes)

Automatically pre-load agents with comprehensive project context so they don't have to discover basic project information every time:

```python
#!/usr/bin/env python3
"""Project context injection - give agents 'cheat codes' about the codebase"""
import json
import sys
import os
import subprocess
from pathlib import Path

def get_project_structure():
    """Get project directory structure using available tools"""
    try:
        # Try tree first (most readable)
        if subprocess.run(["which", "tree"], capture_output=True).returncode == 0:
            result = subprocess.run(
                ["tree", "-d", "-L", "3", "-I", "node_modules|.git|dist|build"], 
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return f"**Directory Structure:**\n```\n{result.stdout}\n```"
        
        # Fallback to git ls-files (works in any git repo)
        result = subprocess.run(
            ["git", "ls-files", "--", "*.md", "*.json", "*.ts", "*.tsx", "*.js", "*.jsx"], 
            capture_output=True, text=True
        )
        if result.returncode == 0:
            files = result.stdout.strip().split('\n')
            structure = {}
            for file in files[:50]:  # Limit to prevent overwhelming
                parts = file.split('/')
                current = structure
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = None
            
            return f"**Key Files Structure:**\n```\n{format_structure(structure)}\n```"
            
    except Exception as e:
        print(f"Structure error: {e}", file=sys.stderr)
    
    return "**Project Structure:** Unable to determine"

def format_structure(structure, indent=0):
    """Format nested structure dictionary"""
    lines = []
    for key, value in structure.items():
        prefix = "  " * indent + ("├── " if indent > 0 else "")
        if value is None:  # File
            lines.append(f"{prefix}{key}")
        else:  # Directory
            lines.append(f"{prefix}{key}/")
            lines.extend(format_structure(value, indent + 1).split('\n')[:-1])
    return '\n'.join(lines) + '\n'

def get_key_documentation():
    """Get essential project documentation content"""
    docs = []
    
    # Project CLAUDE.md (most important for agents)
    if os.path.exists("CLAUDE.md"):
        with open("CLAUDE.md") as f:
            content = f.read()[:2000]  # First 2000 chars
            docs.append(f"**Project Guidance (CLAUDE.md):**\n{content}...")
    
    # README for project overview
    for readme in ["README.md", "readme.md"]:
        if os.path.exists(readme):
            with open(readme) as f:
                content = f.read()[:1000]  # First 1000 chars
                docs.append(f"**Project Overview ({readme}):**\n{content}...")
            break
    
    # Package.json for tech stack
    if os.path.exists("package.json"):
        try:
            with open("package.json") as f:
                import json as jsonlib
                pkg = jsonlib.load(f)
                deps = list(pkg.get("dependencies", {}).keys())[:10]
                dev_deps = list(pkg.get("devDependencies", {}).keys())[:10]
                scripts = list(pkg.get("scripts", {}).keys())
                
                docs.append(f"""**Tech Stack (package.json):**
- Dependencies: {', '.join(deps)}
- DevDeps: {', '.join(dev_deps)}  
- Scripts: {', '.join(scripts)}""")
        except:
            pass
    
    return "\n\n".join(docs)

def get_active_planning_docs():
    """Get current active planning documents"""
    plans = []
    plans_dir = Path("ai-docs/planning/active")
    
    if plans_dir.exists():
        for plan_file in list(plans_dir.glob("*.md"))[:3]:  # Limit to 3 most recent
            try:
                with open(plan_file) as f:
                    content = f.read()[:800]  # First 800 chars
                    plans.append(f"**Active Plan ({plan_file.stem}):**\n{content}...")
            except:
                continue
    
    return "\n\n".join(plans) if plans else ""

def get_recent_changes():
    """Get recent git changes for context"""
    try:
        # Recent commits
        result = subprocess.run(
            ["git", "log", "--oneline", "-n", "5"], 
            capture_output=True, text=True
        )
        recent_commits = result.stdout if result.returncode == 0 else ""
        
        # Current branch and status
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"], 
            capture_output=True, text=True
        )
        current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
        
        status_result = subprocess.run(
            ["git", "status", "--porcelain"], 
            capture_output=True, text=True
        )
        changes = len(status_result.stdout.strip().split('\n')) if status_result.stdout.strip() else 0
        
        return f"""**Git Context:**
- Current branch: {current_branch}
- Uncommitted changes: {changes} files
- Recent commits:
{recent_commits}"""
        
    except:
        return "**Git Context:** Not available"

def get_architecture_docs():
    """Get key architecture documentation"""
    arch_docs = []
    
    # Check for architecture docs in ai-docs
    arch_paths = [
        "ai-docs/nextjs-architecture.md",
        "ai-docs/architecture-diagram.md", 
        "ai-docs/drizzle-orm-guide.md",
        "ai-docs/zustand-nextjs-guide.md",
        "ai-docs/manufacturing-architecture.md"  # Domain-specific
    ]
    
    for arch_path in arch_paths:
        if os.path.exists(arch_path):
            try:
                with open(arch_path) as f:
                    content = f.read()[:600]  # First 600 chars
                    filename = os.path.basename(arch_path)
                    arch_docs.append(f"**{filename}:**\n{content}...")
                    
                if len(arch_docs) >= 2:  # Limit to prevent overwhelming
                    break
            except:
                continue
    
    return "\n\n".join(arch_docs) if arch_docs else ""

def get_quality_standards():
    """Extract quality standards and commands"""
    standards = []
    
    # Look for quality commands in CLAUDE.md
    if os.path.exists("CLAUDE.md"):
        try:
            with open("CLAUDE.md") as f:
                content = f.read()
                # Extract command patterns
                import re
                
                # Look for npm/pnpm commands
                commands = re.findall(r'((?:npm|pnpm|yarn)\s+run\s+\w+)', content)
                if commands:
                    unique_commands = list(set(commands[:5]))
                    standards.append(f"**Quality Commands:** {', '.join(unique_commands)}")
                
                # Look for file size limits
                size_limits = re.findall(r'(\d+)\s*lines?\s*(?:maximum|limit|max)', content, re.IGNORECASE)
                if size_limits:
                    standards.append(f"**File Size Limit:** {size_limits[0]} lines maximum")
        except:
            pass
    
    return "\n".join(standards) if standards else ""

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    if tool_name == "Task":  # Agent about to be invoked
        tool_input = data.get("tool_input", {})
        agent_name = tool_input.get("subagent_type", "unknown")
        
        print(f"🧠 Injecting project context for {agent_name} agent...", file=sys.stderr)
        
        # Gather comprehensive project context
        context_sections = []
        
        # 1. Project structure (always useful)
        structure = get_project_structure()
        if structure:
            context_sections.append(structure)
        
        # 2. Key documentation (critical for decision making)
        docs = get_key_documentation()
        if docs:
            context_sections.append(docs)
        
        # 3. Active plans (for context on current work)
        plans = get_active_planning_docs()
        if plans:
            context_sections.append(plans)
        
        # 4. Architecture patterns (for implementation guidance)
        arch = get_architecture_docs()
        if arch:
            context_sections.append(arch)
        
        # 5. Quality standards (for compliance)
        standards = get_quality_standards()
        if standards:
            context_sections.append(standards)
        
        # 6. Recent changes (for context awareness)
        changes = get_recent_changes()
        if changes:
            context_sections.append(changes)
        
        # Output context for agent to receive
        if context_sections:
            context = f"""## 🎯 Project Context Cheat Sheet

{chr(10).join(context_sections)}

---
*This context was automatically injected to help you understand the project without discovery phase.*
"""
            print(context)  # This goes to agent as context
        
        print(f"✅ Context injection complete for {agent_name}", file=sys.stderr)

except Exception as e:
    print(f"Context injection error: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block agent execution on context errors
```

#### Hook Configuration for Context Injection

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/agent-context-injection.py",
            "timeout": 15000
          }
        ]
      }
    ]
  }
}
```

#### What Gets Injected as "Cheat Codes"

1. **Project Structure** - Directory layout using `tree`, `git ls-files`, or `ls`
2. **Key Documentation** - CLAUDE.md, README.md, package.json highlights  
3. **Active Planning** - Current plans from `ai-docs/planning/active/`
4. **Architecture Guides** - Key architecture docs agents should know
5. **Quality Standards** - Required commands, file size limits, coding standards
6. **Git Context** - Current branch, recent commits, uncommitted changes

#### Cross-Platform Compatibility

```python
# Universal project structure detection
def get_universal_structure():
    """Works on any system without external dependencies"""
    structure = {}
    
    # Walk filesystem manually
    for root, dirs, files in os.walk('.'):
        # Skip hidden and build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'build']]
        
        level = root.replace('.', '').count(os.sep)
        if level < 3:  # Limit depth
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1) 
            for file in files:
                if file.endswith(('.md', '.json', '.ts', '.tsx', '.js', '.jsx')):
                    print(f'{subindent}{file}')
```

#### Benefits of Context Injection

- **Consistent Performance** - Agents always start with full project awareness
- **Faster Execution** - No time wasted on discovery phase
- **Better Decisions** - Agents have complete context for architectural choices
- **Reduced Tool Usage** - Less redundant reading of documentation
- **Domain Awareness** - Agents understand business context immediately

#### Agent-Specific Context Filtering

```python
# Customize context based on agent type
AGENT_CONTEXT_FILTERS = {
    "backend-database-engineer": [
        "drizzle-orm-guide.md",
        "database schema files",
        "server actions patterns"
    ],
    "frontend-ui-specialist": [
        "shadcn-ui-guide.md", 
        "component patterns",
        "tailwind configuration"
    ],
    "code-quality-reviewer": [
        "testing patterns",
        "quality commands",
        "linting configuration"
    ]
}
```

This approach transforms agents from "blank slate discoverers" into "context-aware specialists" who hit the ground running with complete project knowledge.

### Traditional Context Injection (Simple)

Add project state before agent invocations:

```python
#!/usr/bin/env python3
"""Inject project context before agent execution"""
import json
import sys
import os
from pathlib import Path

def get_active_plans():
    """Get current active planning documents"""
    plans_dir = Path("ai-docs/planning/active")
    if not plans_dir.exists():
        return ""
    
    plans = []
    for plan_file in plans_dir.glob("*.md"):
        with open(plan_file) as f:
            content = f.read()
            plans.append(f"## {plan_file.stem}\n{content[:500]}...")
    
    return "\n\n".join(plans)

def get_recent_changes():
    """Get recent git changes for context"""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "log", "--oneline", "-n", "5"], 
            capture_output=True, text=True
        )
        return f"Recent changes:\n{result.stdout}"
    except:
        return ""

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    if tool_name == "Task":  # Agent about to be invoked
        context_parts = []
        
        # Add active planning context
        plans = get_active_plans()
        if plans:
            context_parts.append(f"**Active Plans:**\n{plans}")
        
        # Add recent changes context
        changes = get_recent_changes() 
        if changes:
            context_parts.append(f"**Recent Changes:**\n{changes}")
        
        # Output context for Claude to see
        if context_parts:
            context = "\n\n".join(context_parts)
            print(f"**Project Context for Agent:**\n{context}")

except Exception as e:
    print(f"Error injecting context: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on context injection errors
```

### Agent-Specific Quality Gates

Different validation for different agent types:

```python
#!/usr/bin/env python3
"""Agent-specific quality validation"""
import json
import sys
import subprocess
from pathlib import Path

AGENT_VALIDATIONS = {
    "backend-database-engineer": [
        ("npm run typecheck", "TypeScript validation"),
        ("npm run test -- --testPathPattern=server", "Backend tests"),
    ],
    "frontend-ui-specialist": [
        ("npm run lint", "Frontend linting"),
        ("npm run typecheck", "TypeScript validation"),
        ("npm run test -- --testPathPattern=components", "Component tests"),
    ],
    "code-quality-reviewer": [
        ("npm run build", "Production build"),
        ("npm run test", "Full test suite"),
    ],
}

def run_validation(command, description):
    """Run a validation command and return result"""
    try:
        result = subprocess.run(
            command.split(), 
            capture_output=True, 
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, f"Timeout running {description}"
    except Exception as e:
        return False, f"Error running {description}: {e}"

# Main execution  
try:
    data = json.load(sys.stdin)
    
    # Extract agent name from subagent stop event
    tool_input = data.get("tool_input", {})
    agent_name = tool_input.get("subagent_type", "")
    
    if agent_name in AGENT_VALIDATIONS:
        print(f"🔍 Running quality gates for {agent_name}...")
        
        failed_checks = []
        for command, description in AGENT_VALIDATIONS[agent_name]:
            success, error_output = run_validation(command, description)
            
            if success:
                print(f"✅ {description} passed")
            else:
                print(f"❌ {description} failed")
                failed_checks.append((description, error_output))
        
        if failed_checks:
            print("\n🚫 Quality gate failures:", file=sys.stderr)
            for desc, error in failed_checks:
                print(f"- {desc}: {error}", file=sys.stderr)
            sys.exit(2)  # Block with feedback to agent
        else:
            print("✅ All quality gates passed")
            
except Exception as e:
    print(f"Error in quality validation: {e}", file=sys.stderr)
    sys.exit(1)  # Non-blocking error
```

### Agent Chain Automation

Automatically trigger follow-up agents based on completed work:

```python
#!/usr/bin/env python3
"""Trigger follow-up agents based on completed work"""
import json
import sys
import os

AGENT_CHAINS = {
    "feature-architect-planner": {
        "next_agents": ["backend-database-engineer", "frontend-ui-specialist"],
        "condition": "implementation_plan_created"
    },
    "backend-database-engineer": {
        "next_agents": ["frontend-ui-specialist"],
        "condition": "schema_changes_made"
    },
    "frontend-ui-specialist": {
        "next_agents": ["code-quality-reviewer"],
        "condition": "components_created"
    }
}

def check_condition(agent_name, condition):
    """Check if condition is met for triggering next agents"""
    if condition == "implementation_plan_created":
        return os.path.exists("ai-docs/planning/active/")
    elif condition == "schema_changes_made":
        # Check if database schema files were modified
        return any(
            os.path.exists(p) for p in [
                "lib/db/schema/",
                "drizzle/",
                "migrations/"
            ]
        )
    elif condition == "components_created":
        # Check if component files were created/modified
        return os.path.exists("components/")
    return False

def suggest_next_agents(completed_agent):
    """Suggest next agents in chain"""
    chain = AGENT_CHAINS.get(completed_agent)
    if not chain:
        return None
        
    if check_condition(completed_agent, chain["condition"]):
        return chain["next_agents"]
    return None

# Main execution
try:
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input", {})
    completed_agent = tool_input.get("subagent_type", "")
    
    next_agents = suggest_next_agents(completed_agent)
    if next_agents:
        suggestions = []
        for agent in next_agents:
            suggestions.append(f"- Use {agent} to continue implementation")
        
        feedback = f"""
🔄 **Suggested Next Steps:**
Based on {completed_agent} completing their work, consider:

{chr(10).join(suggestions)}

This follows the orchestration patterns in agents/CLAUDE.md for optimal workflow.
"""
        
        print(feedback, file=sys.stderr)  # Feedback to main Claude thread
        
except Exception as e:
    print(f"Error in agent chaining: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on automation errors
```

## Hook Integration with Project Structure

### Directory Layout for Hooks
```
project-root/
├── .claude/
│   ├── hooks/
│   │   ├── agent-context.py          # Context injection
│   │   ├── quality-gates.py          # Validation hooks  
│   │   ├── agent-chains.py           # Workflow automation
│   │   ├── notification-system.py    # Custom notifications
│   │   └── project-sync.py           # Planning doc updates
│   └── settings.json                 # Hook configurations
├── ai-docs/
│   ├── planning/active/              # Referenced by hooks
│   └── architecture/                 # Agent context source
└── ...
```

### Hook Configuration Management

Use the `/hooks` command for interactive configuration:

```bash
# Open hook configuration interface
/hooks

# Select hook event type
# Choose matcher pattern  
# Add hook command
# Save to project or user settings
```

**Recommended Workflow:**
1. Develop hook script in `.claude/hooks/`
2. Test hook script manually with sample JSON input
3. Configure hook using `/hooks` command
4. Test with actual agent workflows
5. Iterate and refine based on results

## Advanced Hook Patterns

### AI-Generated TTS Completion Notifications

Create engaging audio feedback when agents complete their work using AI-generated summaries and text-to-speech:

```python
#!/usr/bin/env python3
"""TTS completion notification with ElevenLabs and AI-generated messages"""
import json
import sys
import requests
import random
import os
from pathlib import Path

# ElevenLabs voices (mix of professional and character voices)
VOICES = [
    {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "accent": "American Female"},
    {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi", "accent": "American Female"}, 
    {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "accent": "British Female"},
    {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni", "accent": "British Male"},
    {"id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli", "accent": "British Young"},
    {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh", "accent": "American Male"},
]

def generate_completion_message(agent_name, agent_output):
    """Generate contextual completion message based on agent work"""
    agent_messages = {
        "backend-database-engineer": [
            "Database changes are locked and loaded!",
            "Your backend is bulletproof now!",
            "Schema updates deployed like a boss!",
        ],
        "frontend-ui-specialist": [
            "UI looking fresh and responsive!",
            "Components are pixel perfect, chief!",
            "Frontend magic is complete!",
        ],
        "code-quality-reviewer": [
            "Code quality check: all systems green!",
            "Tests passing, ship it!",
            "Quality gates satisfied, you're good to go!",
        ],
        "feature-architect-planner": [
            "Master plan is ready for execution!",
            "Architecture blueprint completed!",
            "Implementation roadmap locked in!",
        ],
    }
    
    # Get agent-specific messages or fallback to generic
    messages = agent_messages.get(agent_name, [
        "Mission accomplished, ready for the next challenge!",
        "Task complete, what's our next move?",
        "All done here, boss!",
    ])
    
    # Add context based on what was accomplished
    if "error" in agent_output.lower() or "failed" in agent_output.lower():
        return random.choice([
            "Hit a snag, but I've got details for you.",
            "Ran into some issues, check the output.",
            "Not quite there yet, needs your attention.",
        ])
    elif "created" in agent_output.lower() or "implemented" in agent_output.lower():
        return random.choice(messages + [
            "Fresh code hot off the press!",
            "Implementation complete, ready to rock!",
        ])
    elif "updated" in agent_output.lower() or "modified" in agent_output.lower():
        return random.choice([
            "Updates deployed successfully!",
            "Modifications complete, looking good!",
        ])
    
    return random.choice(messages)

def text_to_speech(text, voice_id, api_key):
    """Convert text to speech using ElevenLabs API"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,  # More stable for notifications
            "similarity_boost": 0.8,  # Higher similarity 
            "style": 0.2,  # Slight style for character
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            # Save audio to temp file
            audio_file = "/tmp/claude_agent_completion.mp3"
            with open(audio_file, "wb") as f:
                f.write(response.content)
            
            # Play audio based on platform
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=True)
            elif system == "Linux":
                subprocess.run(["aplay", audio_file], check=True)
            elif system == "Windows":
                subprocess.run([
                    "powershell", "-c", 
                    f"(New-Object Media.SoundPlayer '{audio_file}').PlaySync()"
                ], check=True)
            
            return True
            
    except Exception as e:
        print(f"TTS Error: {e}", file=sys.stderr)
        return False

def fallback_system_sound():
    """Play system sound as fallback"""
    import subprocess
    import platform
    
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
        elif system == "Linux":
            subprocess.run(["aplay", "/usr/share/sounds/alsa/Front_Left.wav"])
        elif system == "Windows":
            subprocess.run([
                "powershell", "-c", 
                "[console]::beep(800,300)"
            ])
    except:
        pass  # Silent fallback

# Main hook execution
try:
    data = json.load(sys.stdin)
    hook_event = data.get("hook_event_name", "")
    
    if hook_event == "SubagentStop":
        # Get agent details
        tool_input = data.get("tool_input", {})
        tool_response = data.get("tool_response", "")
        
        agent_name = tool_input.get("subagent_type", "unknown-agent")
        agent_output = str(tool_response)
        
        # Generate contextual message
        message = generate_completion_message(agent_name, agent_output)
        
        # Pick random voice for variety
        voice = random.choice(VOICES)
        
        # Get API key from environment
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        
        if api_key and len(message) < 500:  # Reasonable length limit
            # Convert to speech and play
            if text_to_speech(message, voice["id"], api_key):
                print(f"🔊 {agent_name} completion: '{message}' ({voice['name']})")
            else:
                print(f"🔊 TTS failed, using system sound for {agent_name}")
                fallback_system_sound()
        else:
            # Fallback to system sound
            print(f"🔊 {agent_name} completed (no TTS available)")
            fallback_system_sound()
            
    elif hook_event == "Stop":
        # Main thread completion - simpler message
        message = "All agents complete, ready for your next request!"
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        
        if api_key:
            voice = random.choice(VOICES)
            if not text_to_speech(message, voice["id"], api_key):
                fallback_system_sound()
        else:
            fallback_system_sound()

except Exception as e:
    print(f"TTS completion hook error: {e}", file=sys.stderr)
    fallback_system_sound()  # Always provide some notification
```

#### Hook Configuration for TTS Notifications

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/tts-completion.py",
            "timeout": 45000
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command", 
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/tts-completion.py",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

#### Setup Requirements

```bash
# Install required Python packages
pip install requests

# Set ElevenLabs API key in environment
export ELEVENLABS_API_KEY="your-api-key-here"

# Add to your shell profile for persistence
echo 'export ELEVENLABS_API_KEY="your-api-key-here"' >> ~/.zshrc

# Make hook script executable
chmod +x .claude/hooks/tts-completion.py
```

#### Features of TTS Completion System

- **Agent-Specific Messages**: Different completion messages for different agent types
- **Context Awareness**: Messages adapt based on success/failure and work type
- **Voice Variety**: Randomly selects from different voices and accents
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Graceful Fallback**: Uses system sounds if TTS fails
- **Performance**: Includes timeouts and length limits for reliability

#### Customization Options

```python
# Add custom voices for specific agents
AGENT_VOICES = {
    "code-quality-reviewer": "ErXwobaYiN019PkySvjV",  # Antoni (serious British)
    "frontend-ui-specialist": "EXAVITQu4vr4xnSDxMaL",  # Bella (creative British) 
    "backend-database-engineer": "TxGEqnHWrfWFTfGW9XjX",  # Josh (technical American)
}

# Add personality-based message styles
PERSONALITY_STYLES = {
    "professional": ["Task completed successfully.", "Work finished."],
    "casual": ["All done!", "Ready to roll!", "We're good to go!"],
    "enthusiastic": ["Boom! Nailed it!", "Absolutely crushing it!", "Mission complete!"],
}
```

This creates an engaging development experience where agents "speak" their completion status, making it easier to stay aware of progress during long coding sessions without constantly monitoring the screen.

### Multi-Agent Coordination Hook

Coordinate multiple agents working in parallel:

```python
#!/usr/bin/env python3
"""Multi-agent coordination and conflict prevention"""
import json
import sys
import fcntl
import time
from pathlib import Path

LOCK_FILE = Path(".claude/agent-coordination.lock")
STATE_FILE = Path(".claude/agent-state.json")

def acquire_lock():
    """Acquire coordination lock"""
    try:
        LOCK_FILE.parent.mkdir(exist_ok=True)
        lock_fd = open(LOCK_FILE, 'w')
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except (IOError, OSError):
        return None

def get_agent_state():
    """Get current agent coordination state"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"active_agents": [], "file_locks": {}}

def update_agent_state(agent_name, files_being_modified):
    """Update agent state with current work"""
    state = get_agent_state()
    
    # Add agent to active list
    if agent_name not in state["active_agents"]:
        state["active_agents"].append(agent_name)
    
    # Lock files being modified
    for file_path in files_being_modified:
        state["file_locks"][file_path] = agent_name
    
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def check_conflicts(agent_name, files_to_modify):
    """Check for file conflicts with other agents"""
    state = get_agent_state()
    conflicts = []
    
    for file_path in files_to_modify:
        if file_path in state["file_locks"]:
            existing_agent = state["file_locks"][file_path]
            if existing_agent != agent_name:
                conflicts.append((file_path, existing_agent))
    
    return conflicts

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    if tool_name == "Task":  # Agent starting
        tool_input = data.get("tool_input", {})
        agent_name = tool_input.get("subagent_type", "unknown")
        
        # Acquire coordination lock
        lock_fd = acquire_lock()
        if not lock_fd:
            print("Another agent coordination in progress, waiting...", file=sys.stderr)
            time.sleep(2)  # Brief delay
            sys.exit(0)
        
        try:
            # Extract files this agent might modify (heuristic)
            files_to_modify = []
            prompt = tool_input.get("prompt", "")
            
            # Simple heuristic - look for file mentions
            import re
            file_patterns = re.findall(r'[\w\-_./]+\.(ts|tsx|js|jsx|md|json)', prompt)
            files_to_modify.extend(file_patterns)
            
            # Check for conflicts
            conflicts = check_conflicts(agent_name, files_to_modify)
            if conflicts:
                conflict_msg = "\n".join([
                    f"- {file}: locked by {agent}" 
                    for file, agent in conflicts
                ])
                print(f"⚠️ File conflicts detected:\n{conflict_msg}", file=sys.stderr)
                print("Consider coordinating agent execution order", file=sys.stderr)
            
            # Update state
            update_agent_state(agent_name, files_to_modify)
            
        finally:
            lock_fd.close()
            LOCK_FILE.unlink(missing_ok=True)

except Exception as e:
    print(f"Error in agent coordination: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on coordination errors
```

### Planning Document Synchronization

Keep planning documents in sync with actual implementation:

```python
#!/usr/bin/env python3
"""Synchronize planning documents with implementation progress"""
import json
import sys
import os
from pathlib import Path
import re

def update_planning_status(agent_name, completed_tasks):
    """Update planning documents with completion status"""
    active_dir = Path("ai-docs/planning/active")
    if not active_dir.exists():
        return
    
    for plan_file in active_dir.glob("*.md"):
        try:
            with open(plan_file, 'r') as f:
                content = f.read()
            
            modified = False
            for task in completed_tasks:
                # Look for task checkboxes and mark as completed
                pattern = rf'- \[ \] (.*{re.escape(task)}.*)'
                replacement = r'- [x] \1'
                
                new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                if new_content != content:
                    content = new_content
                    modified = True
            
            if modified:
                with open(plan_file, 'w') as f:
                    f.write(content)
                print(f"📋 Updated planning status in {plan_file.name}")
                
        except Exception as e:
            print(f"Error updating {plan_file}: {e}", file=sys.stderr)

def extract_completed_tasks(agent_name, tool_response):
    """Extract completed tasks from agent response"""
    response_text = str(tool_response)
    
    # Agent-specific task extraction
    if agent_name == "backend-database-engineer":
        tasks = re.findall(r'(?:created|implemented|added) ([^.]+)', response_text, re.IGNORECASE)
    elif agent_name == "frontend-ui-specialist":
        tasks = re.findall(r'(?:component|page|styling) ([^.]+)', response_text, re.IGNORECASE)
    else:
        # Generic task extraction
        tasks = re.findall(r'(?:completed|finished|implemented) ([^.]+)', response_text, re.IGNORECASE)
    
    return tasks

# Main execution
try:
    data = json.load(sys.stdin)
    hook_event = data.get("hook_event_name", "")
    
    if hook_event == "SubagentStop":
        tool_input = data.get("tool_input", {})
        tool_response = data.get("tool_response", "")
        
        agent_name = tool_input.get("subagent_type", "")
        completed_tasks = extract_completed_tasks(agent_name, tool_response)
        
        if completed_tasks:
            update_planning_status(agent_name, completed_tasks)
            print(f"✅ Synced {len(completed_tasks)} completed tasks to planning docs")

except Exception as e:
    print(f"Error syncing planning documents: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on sync errors
```

## Hook Debugging and Testing

### Testing Hook Scripts

Test hooks locally before deployment:

```bash
# Create test input
cat > test-hook-input.json << 'EOF'
{
  "session_id": "test-123",
  "cwd": "/path/to/project",
  "hook_event_name": "PostToolUse", 
  "tool_name": "Task",
  "tool_input": {
    "subagent_type": "backend-database-engineer",
    "prompt": "Implement user authentication"
  },
  "tool_response": {
    "success": true,
    "message": "Created authentication system with login/logout"
  }
}
EOF

# Test hook script
cat test-hook-input.json | .claude/hooks/agent-quality-gate.py
```

### Hook Performance Monitoring

Add performance tracking to hooks:

```python
#!/usr/bin/env python3
"""Performance monitoring wrapper for hooks"""
import json
import sys
import time
import os
from pathlib import Path

PERF_LOG = Path(".claude/hook-performance.log")

def log_performance(hook_name, duration, success):
    """Log hook performance metrics"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp},{hook_name},{duration:.3f},{success}\n"
    
    PERF_LOG.parent.mkdir(exist_ok=True)
    with open(PERF_LOG, 'a') as f:
        f.write(log_entry)

# Wrapper for actual hook logic
def main_hook_logic():
    """Your actual hook implementation goes here"""
    # ... hook implementation ...
    pass

# Main execution with performance tracking
hook_name = os.path.basename(__file__)
start_time = time.time()
success = True

try:
    main_hook_logic()
except Exception as e:
    success = False
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(1)
finally:
    duration = time.time() - start_time
    log_performance(hook_name, duration, success)
```

## Security and Best Practices

### Security Guidelines
- **Validate all inputs** from hook JSON data
- **Quote shell variables** properly: `"$variable"`
- **Use absolute paths** with `$CLAUDE_PROJECT_DIR`
- **Limit file access** to project directories
- **Avoid sensitive data** in hook outputs

### Performance Best Practices
- **Set timeouts** for long-running operations
- **Avoid blocking hooks** for non-critical validations  
- **Use exit code 0** for informational outputs
- **Cache expensive computations** across hook invocations
- **Log performance metrics** for optimization

### Integration Best Practices
- **Test hooks independently** before integration
- **Use consistent JSON output format** for structured feedback
- **Coordinate with team** on shared hook configurations
- **Version control hook scripts** in `.claude/hooks/`
- **Document hook behavior** for team members

This guide provides the foundation for creating sophisticated hook-based automation that enhances multi-agent workflows while maintaining reliability and performance.
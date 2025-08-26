# Output Styles

Output styles allow you to adapt Claude Code for different types of workflows while keeping its core capabilities. This directory contains **orchestration-focused output styles** that change how Claude coordinates agents and manages workflows.

## What Are Output Styles?

Output styles directly modify Claude Code's system prompt to change its behavior. They're like "modes" that transform Claude from a general coding assistant into a specialized workflow orchestrator.

**Key Concepts:**
- Output styles **replace** the default Claude Code system prompt
- They preserve tool access but change behavioral patterns
- Multiple output styles can be switched between during development
- Settings are saved per-project in `.claude/settings.local.json`

**Reference:** [Anthropic Output Styles Documentation](https://docs.anthropic.com/en/docs/claude-code/output-styles)

## Available Orchestration Styles

### 🔍 Research Orchestrator (`orchestrator-research.md`)
**When to Use:** "I need to understand this codebase/library/concept"

**Primary Agents:** documentation-specialist, general-purpose  
**Workflow:** Explore → Document → Share insights  
**Focus:** Discovery, learning, knowledge building  
**Output:** Comprehensive documentation and understanding  

**Activate:** `/output-style research`

---

### 📋 Planning Orchestrator (`orchestrator-planning.md`)  
**When to Use:** "I need to design a feature/solution"

**Primary Agents:** feature-architect-planner, documentation-specialist, project-manager  
**Workflow:** Research → Design → Document requirements  
**Focus:** Requirements gathering, architecture decisions, comprehensive planning  
**Output:** Implementation-ready plans and specifications  

**Activate:** `/output-style planning`

---

### ⚡ Execution Orchestrator (`orchestrator-execution.md`)
**When to Use:** "I have a plan, let's build it"

**Primary Agents:** backend/frontend specialists, code-quality-reviewer, git-workflow-specialist  
**Workflow:** Start workflow → Implement → Quality gates → Deliver  
**Focus:** Following plans, building features, testing, shipping  
**Output:** Working software ready for human review  

**Activate:** `/output-style execution`

## How to Use Output Styles

### Quick Commands
```bash
# Access the menu
/output-style

# Switch directly
/output-style research
/output-style planning  
/output-style execution

# Return to default
/output-style default
```

### Typical Development Flow
```bash
# 1. Research Phase - Understand the domain
/output-style research
"Help me understand how authentication works in this Next.js app"

# 2. Planning Phase - Design the solution  
/output-style planning
"Design a user profile management system with role-based access"

# 3. Execution Phase - Build the feature
/output-style execution
"Implement the user profile system from the planning docs"
```

## Output Style Integration

These orchestration styles work seamlessly with the broader agent system:

### **Three-Layer Architecture**
1. **Output Styles** (this directory) → Workflow orchestration mode
2. **Universal CLAUDE.md** (`agents/CLAUDE.md`) → Agent delegation patterns  
3. **Project CLAUDE.md** (project root) → Domain context and tech stack

### **Agent System Integration**
- All styles use the same specialized agents from `agents/` directory
- Agents maintain their expertise but receive mode-appropriate coordination
- Quality hooks (`hooks/`) work consistently across all styles

### **Quality Automation**
- Hooks handle automated quality gates (lint, typecheck, code validation)
- Output styles focus on workflow coordination, not tool execution
- Manual quality assessment handled by code-quality-reviewer agent

## Creating Custom Output Styles

### Using Claude Code Helper
```bash
/output-style:new I want an output style that focuses on security audits and vulnerability assessment
```

### Manual Creation
Create new `.md` files in this directory with this structure:

```markdown
---
name: My Custom Style
description: Brief description for the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering tasks.
[Your custom system prompt instructions here...]

## Specific Behaviors
[Define how Claude should behave in this mode...]
```

### File Locations
- **User-level styles:** `~/.claude/output-styles` (available across all projects)
- **Project-level styles:** `.claude/output-styles` (project-specific only)

## Key Differences from Related Features

### vs. CLAUDE.md Files
- **Output Styles:** Replace the entire system prompt, change fundamental behavior
- **CLAUDE.md:** Add project context as user messages, supplement existing behavior

### vs. Agents (`agents/` directory)
- **Output Styles:** Affect the main coordination loop and orchestration patterns
- **Agents:** Specialized tools for specific tasks, invoked by the main loop

### vs. Hooks (`hooks/` directory)  
- **Output Styles:** Change coordination behavior and workflow patterns
- **Hooks:** Automate specific actions at tool execution points

### vs. Custom Slash Commands
- **Output Styles:** "Stored system prompts" that change fundamental behavior
- **Slash Commands:** "Stored prompts" that execute specific one-time actions

## Advanced Usage Patterns

### Mode Switching Within Sessions
```bash
# Start with research
/output-style research
"Research GraphQL integration patterns"

# Switch to planning once you understand the domain  
/output-style planning
"Design a GraphQL API based on the research findings"

# Switch to execution when ready to build
/output-style execution  
"Implement the GraphQL API from the planning documents"
```

### Project-Specific Customization
Each output style can be customized per project by creating local versions:

```bash
# Copy system style to project level
cp ~/.claude/output-styles/orchestrator-execution.md .claude/output-styles/

# Customize for project-specific needs
# Edit .claude/output-styles/orchestrator-execution.md
```

## Troubleshooting

### Style Not Working as Expected
1. Check that you're in the correct mode: `/output-style`
2. Verify agents are properly configured in `agents/` directory
3. Ensure hooks are registered in `settings.json`
4. Check project CLAUDE.md for conflicting instructions

### Style Not Available
1. Verify file exists in `output-styles/` directory
2. Check file has proper YAML frontmatter
3. Restart Claude Code if recently added
4. Check file permissions (should be readable)

### Switching Between Styles
- Output style changes apply immediately
- Previous conversation context remains but behavior changes
- Use `/clear` if you need fresh context with the new style

## Best Practices

### Choose the Right Style
- **Research:** When you don't understand the domain or technology
- **Planning:** When you know what to build but need to design how
- **Execution:** When you have clear requirements and want to implement

### Style-Specific Tips
- **Research Style:** Focus on questions and exploration, don't rush to implementation
- **Planning Style:** Spend time on requirements and acceptance criteria
- **Execution Style:** Follow plans strictly, delegate to appropriate agents

### Project Integration
- Create project-specific styles for unique workflows
- Document style preferences in project CLAUDE.md
- Train team members on when to use each style

This orchestration system transforms Claude Code from a coding assistant into a **workflow-aware development orchestrator**, enabling more effective multi-agent coordination and better development outcomes.
# Specialized Agents

This directory contains **specialized agent definitions** that extend Claude Code with domain-specific expertise. Agents are sub-assistants that handle specific tasks while the main Claude instance orchestrates the overall workflow through direct delegation.

## What Are Agents?

Agents are specialized versions of Claude designed for focused domains. They have their own system prompts, tool access, and behavioral patterns, enabling expert-level assistance without the complexity of multi-tier orchestration.

**Core Architecture:**
- **Main thread orchestration**: YOU coordinate all agent work directly
- **Hook-based automation**: Quality gates and context injection handled automatically
- **Output style integration**: Agents adapt behavior based on research/planning/execution modes
- **Domain specialization**: Each agent focuses on specific expertise areas

**Key Principles:**
- Agents are invoked by the main Claude instance using the `Task` tool
- Each agent has specialized knowledge for specific domains
- Agents cannot call other agents - all coordination happens at the main level
- Hooks automatically provide context and handle quality validation
- Agents report back with comprehensive context for main thread integration

**Reference:** [Anthropic Agents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## Available Specialized Agents

### 🏗️ **Architecture & Planning**

#### **feature-architect-planner**
- **Purpose:** Complex feature planning with architectural considerations
- **Use When:** Breaking down large features, designing system interactions, creating implementation roadmaps
- **Expertise:** Requirements analysis, technical specifications, system design
- **Integration:** Works with hooks for automatic context injection, creates plans for other agents

#### **project-manager** 
- **Purpose:** Planning documentation lifecycle and workflow state management
- **Use When:** Moving plans through lifecycle (backlog→active→completed), coordinating development phases
- **Expertise:** Planning document organization, workflow state tracking, development coordination
- **Integration:** Manages ai-docs/planning/ structure, coordinates with all other agents

---

### 💻 **Implementation Specialists**

#### **backend-database-engineer**
- **Purpose:** Database schema, migrations, server logic, API development
- **Use When:** Any backend/database work - delegate all server-side implementation
- **Expertise:** Database design, ORM patterns, server actions, API routes, performance optimization
- **Integration:** Automatic context injection includes database patterns from ai-docs/

#### **frontend-ui-specialist**
- **Purpose:** UI components, styling, visual elements, design systems
- **Use When:** Any UI/component work - delegate all frontend implementation
- **Expertise:** Component architecture, responsive design, accessibility, CSS frameworks
- **Integration:** Receives design patterns and component standards automatically via hooks

---

### 🔧 **Code Quality & Organization**

#### **code-quality-reviewer**
- **Purpose:** Manual quality assessment, integration testing, user experience validation
- **Use When:** Quality validation beyond automated tools - hooks handle lint/typecheck automatically
- **Expertise:** Integration testing, UX validation, accessibility assessment, manual QA processes
- **Integration:** Works with automated hooks - focuses on what automation can't handle

#### **file-refactor-organizer**
- **Purpose:** Breaking down large files (>300 lines), improving code organization
- **Use When:** Files exceed size limits, code structure needs improvement, before major commits
- **Expertise:** Component extraction, module organization, dependency management
- **Integration:** Triggered by size limits, works with git-workflow-specialist for clean commits

---

### 📚 **Knowledge & Documentation**

#### **documentation-specialist**
- **Purpose:** Technical documentation, library research, knowledge management
- **Use When:** Research new libraries/patterns, create documentation, fill knowledge gaps
- **Expertise:** Library integration research, best practices documentation, ai-docs/ maintenance
- **Integration:** Creates and maintains ai-docs/ content that hooks automatically inject to other agents

---

### 🔄 **Workflow Management**

#### **git-workflow-specialist**
- **Purpose:** Git operations, branch strategies, commit hygiene, worktree management
- **Use When:** Any git operation - delegate all git work for consistency and expertise
- **Expertise:** Branch management, commit standards, parallel development, merge strategies, worktrees
- **Integration:** Essential for parallel orchestration workflow with tmux + worktrees

## How to Use Agents

### Main Thread Orchestration Pattern

**Your Role:** Coordinate agents directly based on task requirements
**Agent Role:** Execute specialized work and report back with context
**Hook Role:** Automatically inject context and validate quality

```bash
# Main thread decides and coordinates:
"I need user authentication implemented"
↓
1. Use project-manager to move plan from backlog → active
2. Use feature-architect-planner if detailed planning needed
3. Use backend-database-engineer for database/API work
4. Use frontend-ui-specialist for UI components
5. Use code-quality-reviewer for integration testing
6. Use git-workflow-specialist for commits and PR
7. Use project-manager to move plan to completed
```

### Agent Selection Decision Tree

1. **Git operations needed?** → `git-workflow-specialist`
2. **Files >300 lines?** → `file-refactor-organizer`
3. **Database/API work?** → `backend-database-engineer` 
4. **UI/component work?** → `frontend-ui-specialist`
5. **Quality validation needed?** → `code-quality-reviewer`
6. **Library research needed?** → `documentation-specialist`
7. **Complex feature planning?** → `feature-architect-planner`
8. **Planning docs management?** → `project-manager`

### Mandatory Delegation Rules

**CRITICAL: DO NOT perform actions directly when an agent specialist exists.**

**❌ Instead of:**
- "Let me create this component..."
- "I'll run the tests..."  
- "Let me commit these changes..."

**✅ Always say:**
- "I'll use frontend-ui-specialist to create this component..."
- "I'll use code-quality-reviewer for testing and quality validation..."
- "I'll use git-workflow-specialist to commit these changes..."

## Integration with Hook System

### Automatic Quality Pipeline

Your system eliminates manual quality management through hooks:

```
Agent Invocation → Context Injection Hook → Agent Work → Validation Hook
      ↓                    ↓                    ↓              ↓
  Task Decision      Auto-inject context    Expert work    Auto-validate
```

### Hook-Handled Automation

- **Context Injection:** Agents automatically receive project structure, ai-docs/, git context
- **Quality Validation:** Lint, typecheck, and code standards handled automatically
- **Performance Monitoring:** Agent usage patterns tracked and optimized
- **Result Validation:** Agent outputs checked against quality standards

### What Agents Focus On

Since hooks handle automation, agents focus purely on:
- **Domain expertise:** Deep knowledge in their specialization
- **Complex reasoning:** Decisions that require domain understanding
- **Integration guidance:** How their work connects to the broader system
- **Context-aware implementation:** Using injected context effectively

## Output Style Integration

Agents adapt their behavior based on your current workflow mode:

### Research Mode (`/output-style research`)
- **documentation-specialist:** Primary agent for exploration and learning
- **All agents:** Focus on discovery and understanding over implementation
- **Integration:** Emphasis on documenting findings in ai-docs/

### Planning Mode (`/output-style planning`)
- **feature-architect-planner:** Primary agent for design and specifications
- **project-manager:** Coordinates planning document lifecycle
- **Integration:** Creates implementation-ready plans for execution mode

### Execution Mode (`/output-style execution`)
- **Backend/Frontend specialists:** Primary agents for implementation
- **git-workflow-specialist:** Essential for parallel development coordination
- **Integration:** Follows established plans, focuses on delivery and quality

## Parallel Orchestration Workflow

Perfect for your tmux + git worktrees setup:

### Multi-Pane Development
```bash
# Pane 1: Shared dev branch
project-manager: Coordinates overall development state

# Pane 2: Feature A (auth worktree)
backend-database-engineer + frontend-ui-specialist: Auth implementation

# Pane 3: Feature B (inventory worktree)  
backend-database-engineer + frontend-ui-specialist: Inventory system

# Pane 4: Feature C (reporting worktree)
documentation-specialist + backend-database-engineer: Report system
```

### Git Worktree Coordination
- **git-workflow-specialist:** Handles all worktree operations, branch management
- **Enhanced statusline:** Shows worktree context, change counts, total worktrees
- **Context hooks:** Automatically inject worktree-specific context to agents

## Agent Configuration Structure

Each agent is defined by a Markdown file in this directory:

```markdown
---
name: agent-name
description: Clear description with usage guidance and examples
model: sonnet
color: color-name
tools: comma,separated,tool,list
---

# Agent System Prompt
Detailed instructions for specialized behavior and domain expertise.

## Integration Requirements  
How the agent works with hooks, other agents, and the main orchestration thread.

## Reporting Standards
Expected output format and context information for main thread integration.
```

## Best Practices

### Agent Coordination
- **Trust the specialization:** Agents are experts in their domains with automatic context
- **Provide clear task context:** Specific requirements and integration points
- **Review agent reports:** Integration guidance and next steps for main thread
- **Update ai-docs:** When agents discover new patterns or solutions

### Quality Assurance
- **Let hooks handle automation:** No manual lint/typecheck in conversations  
- **Use code-quality-reviewer:** For complex testing and manual validation
- **Coordinate through main thread:** All agent-to-agent work flows through you
- **Maintain documentation:** Agents contribute to ai-docs/ for future context injection

### Workflow Optimization
- **Match agents to output styles:** Research agents for discovery, implementation agents for execution
- **Batch related work:** Coordinate frontend + backend + quality for complete features
- **Use git-workflow-specialist:** For all git operations in parallel development
- **Monitor through hooks:** Performance and usage patterns automatically tracked

This agent system transforms Claude Code into a **specialized development team** with automatic quality gates, seamless context management, and expert coordination - all orchestrated through your direct main-thread control.
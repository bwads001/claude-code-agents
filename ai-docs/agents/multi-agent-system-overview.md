# Multi-Agent Development System

This document provides a comprehensive overview of the specialized Claude Code agents and their orchestration patterns.

## Agent Architecture

Our multi-agent system follows the **orchestrator-worker pattern** with the `lead-developer-orchestrator` coordinating specialized agents through explicit Task tool delegation.

### Core Agents

| Agent | Purpose | Model | Key Capabilities |
|-------|---------|-------|------------------|
| `lead-developer-orchestrator` | Project coordination & agent orchestration | Sonnet | Task delegation, quality gates, workflow coordination |
| `feature-architect-planner` | Feature planning & breakdown | Opus | Complex planning, ai-docs/planning integration, objective-based tasks |
| `backend-database-engineer` | Database & backend development | Sonnet | Schema design, migrations, Server Actions, API development |
| `frontend-ui-specialist` | UI/UX development & styling | Sonnet | React components, responsive design, QA feedback integration |
| `code-quality-reviewer` | Comprehensive code review & testing | Opus | Playwright testing, multi-device QA, accessibility validation |
| `file-refactor-organizer` | Code organization & refactoring | Sonnet | Breaking down large files, maintaining 300-line rule |
| `documentation-specialist` | Research & technical documentation | Opus | Context7 MCP research, ai-docs/ management, library integration guides |
| `git-workflow-specialist` | Git workflow & branch management | Sonnet | Feature branches, git worktrees, commit hygiene, parallel development |

## Agent Orchestration Patterns

### 1. New Feature Implementation
```
1. feature-architect-planner → Create implementation plan in ai-docs/planning/active/
2. backend-database-engineer → Schema and backend services
3. frontend-ui-specialist → UI components and user interactions
4. code-quality-reviewer → Comprehensive review and testing
5. file-refactor-organizer → Clean up any files >300 lines
```

### 2. Library Integration Workflow
```
1. documentation-specialist → Research library and create ai-docs/ guide
2. feature-architect-planner → Plan integration approach
3. backend/frontend specialists → Implementation based on guide
4. code-quality-reviewer → Validate integration
5. documentation-specialist → Update patterns and lessons learned
```

### 3. QA ↔ Frontend Enhancement Loop
```
1. frontend-ui-specialist → Initial UI implementation
2. code-quality-reviewer → Playwright testing across devices + accessibility
3. frontend-ui-specialist → Address QA findings with specific visual evidence
4. Repeat 2-3 until quality standards met
5. code-quality-reviewer → Final integration review
```

### 4. Parallel Development with Git Worktrees
```
1. git-workflow-specialist → Set up separate worktrees for each development stream
2. feature-architect-planner → Plan Feature A, B, and Hotfix C independently
3. Parallel execution:
   - Worktree A: backend-database-engineer + frontend-ui-specialist (Feature A)
   - Worktree B: frontend-ui-specialist + documentation-specialist (Feature B)  
   - Worktree C: backend-database-engineer (Critical Hotfix)
4. git-workflow-specialist → Coordinate commits and prevent conflicts
5. code-quality-reviewer → Independent validation in each worktree
6. git-workflow-specialist → Strategic merge coordination
7. code-quality-reviewer → Integration testing post-merge
```

## Key Design Principles

### Specialization Over Generalization
- Each agent has a focused domain of expertise
- Clear boundaries prevent overlap and confusion
- Enables parallel execution of independent tasks

### Context Engineering
- Detailed task delegation with specific objectives and boundaries
- All agents reference project-specific context from `./ai-docs/`
- Integration points clearly defined between agent responsibilities

### Quality-First Development
- Built-in quality gates enforced through agent workflows
- Comprehensive testing with Playwright MCP across device sizes
- TypeScript strict mode compliance across all agents

### Domain-Agnostic Design
- Agents adapt to any project by reading `./ai-docs/` for patterns
- No hard-coded technology assumptions
- Project-specific standards discovered rather than assumed

## Agent Communication & Coordination

### Lead Developer Responsibilities
1. **Task Analysis & Agent Selection** - Choose appropriate agent for each task type
2. **Detailed Task Delegation** - Provide clear objectives, context boundaries, output formats
3. **Parallel Coordination** - Prevent file conflicts, sequence dependent tasks
4. **Context Engineering** - Ensure each agent gets project-specific context

### Inter-Agent Dependencies
- **Schema First**: Database changes before UI implementation
- **Documentation Driven**: Research and document before implementation
- **QA Integration**: Continuous feedback loops between UI and quality review
- **File Organization**: Proactive refactoring before commits

## Advanced Capabilities

### Multi-Device Testing
The code-quality-reviewer uses Playwright MCP to:
- Test responsive design across desktop, tablet, phone viewports
- Capture screenshots at specific breakpoints where UI issues occur
- Validate accessibility compliance (keyboard nav, screen readers, ARIA)
- Document UI problems with visual evidence and viewport dimensions

### Knowledge Management
The documentation-specialist maintains:
- Library integration guides with Context7 MCP research
- Architectural decision records for significant technical choices
- Troubleshooting guides for common issues and solutions
- Cross-referenced documentation system in ai-docs/

### Autonomous Development Capability
The system enables:
- Independent feature development with minimal human intervention
- Self-improving knowledge base through documentation updates
- Quality enforcement through automated review cycles
- Scalable architecture that adapts to project complexity

## Usage Guidelines

### When to Use Each Agent
- **Complex feature planning**: feature-architect-planner
- **Database/API work**: backend-database-engineer  
- **UI/styling tasks**: frontend-ui-specialist
- **Code review needs**: code-quality-reviewer
- **Large file cleanup**: file-refactor-organizer
- **Research/documentation**: documentation-specialist
- **Git workflow management**: git-workflow-specialist
- **Project coordination**: lead-developer-orchestrator

### Best Practices
1. **Always start with lead-developer-orchestrator** for complex multi-step tasks
2. **Use documentation-specialist** before adding new libraries or complex features
3. **Leverage the QA feedback loop** for iterative UI improvements
4. **Use git-workflow-specialist** for proper branch management and parallel development
5. **Leverage git worktrees** for simultaneous feature development without conflicts
6. **Maintain ai-docs/** as the single source of truth for project patterns
7. **Trust agent specialization** - don't try to make one agent do everything

This multi-agent system creates a sophisticated, autonomous development environment that scales with project complexity while maintaining high code quality and architectural consistency.
# Multi-Agent Development System

This document provides a comprehensive overview of the specialized Claude Code agents and their orchestration patterns.

## Agent Architecture

Our multi-agent system follows a **main-thread orchestration pattern** where the primary Claude instance directly coordinates specialized agents. This approach ensures:

- **Direct Control**: Main Claude thread maintains full context and makes orchestration decisions
- **Agent Specialization**: Each agent focuses on domain expertise without coordination overhead  
- **Comprehensive Reporting**: All agents provide detailed reports back to main thread for continued orchestration
- **Context Preservation**: Main thread maintains project state across agent invocations

**Key Architectural Change**: Agents cannot call other agents in Claude Code. All coordination happens at the main Claude level using orchestration patterns defined in `~/.claude/agents/CLAUDE.md`.

### Core Agents

| Agent | Purpose | Model | Key Capabilities |
|-------|---------|-------|------------------|
| `project-manager` | Planning documentation & context management | Sonnet | Planning lifecycle, project status, context summaries, orchestration assistance |
| `feature-architect-planner` | Feature planning & breakdown | Opus | Complex planning, ai-docs/planning integration, objective-based tasks |
| `backend-database-engineer` | Database & backend development | Sonnet | Schema design, migrations, Server Actions, API development |
| `frontend-ui-specialist` | UI/UX development & styling | Sonnet | React components, responsive design, accessibility |
| `code-quality-reviewer` | Comprehensive code review & testing | Opus | Playwright testing, multi-device QA, quality gates |
| `file-refactor-organizer` | Code organization & refactoring | Sonnet | Breaking down large files (>300 lines), modular organization |
| `documentation-specialist` | Research & technical documentation | Opus | Context7 MCP research, ai-docs/ management, library guides |
| `git-workflow-specialist` | Git workflow & branch management | Sonnet | Worktrees, commit hygiene, parallel development |

## Agent Orchestration Patterns

### 1. New Feature Implementation
```
1. project-manager → Review active plans and project status
2. feature-architect-planner → Create implementation plan in ai-docs/planning/active/
3. git-workflow-specialist → Create feature branch/worktree
4. backend-database-engineer → Schema and backend services
5. frontend-ui-specialist → UI components and user interactions
6. code-quality-reviewer → Comprehensive review and testing
7. file-refactor-organizer → Clean up any files >300 lines
8. project-manager → Update planning docs to completed
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
- Agents report comprehensively back to main thread for continued orchestration

### Main-Thread Orchestration
- Main Claude instance makes all coordination decisions
- Agents cannot call other agents - all coordination flows through main thread
- Orchestration patterns defined in `~/.claude/agents/CLAUDE.md` guide decision-making
- Context preserved across agent interactions through comprehensive reporting

### Context Engineering
- Main thread provides detailed task delegation with specific objectives and boundaries
- All agents reference project-specific context from `./ai-docs/`
- Integration points coordinated by main thread based on agent reports

### Quality-First Development
- Built-in quality gates enforced through agent workflows
- Comprehensive testing with Playwright MCP across device sizes
- TypeScript strict mode compliance across all agents

### Domain-Agnostic Design
- Agents adapt to any project by reading `./ai-docs/` for patterns
- No hard-coded technology assumptions
- Project-specific standards discovered rather than assumed

## Agent Communication & Coordination

### Main Claude Thread Responsibilities
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

### Orchestrated Development Capability
The system enables:
- Coordinated feature development with main-thread orchestration
- Self-improving knowledge base through documentation updates
- Quality enforcement through orchestrated review cycles
- Scalable architecture where main thread coordinates increasing agent complexity

## Usage Guidelines

### When to Use Each Agent
- **Complex feature planning**: feature-architect-planner
- **Database/API work**: backend-database-engineer  
- **UI/styling tasks**: frontend-ui-specialist
- **Code review needs**: code-quality-reviewer
- **Large file cleanup**: file-refactor-organizer
- **Research/documentation**: documentation-specialist
- **Git workflow management**: git-workflow-specialist
- **Project coordination**: project-manager

### Best Practices
1. **Use project-manager** to review active plans and coordinate complex multi-step tasks
2. **Use documentation-specialist** before adding new libraries or complex features
3. **Leverage the QA feedback loop** for iterative UI improvements
4. **Use git-workflow-specialist** for proper branch management and parallel development
5. **Leverage git worktrees** for simultaneous feature development without conflicts
6. **Maintain ai-docs/** as the single source of truth for project patterns
7. **Trust agent specialization** - don't try to make one agent do everything

This multi-agent system creates a sophisticated, autonomous development environment that scales with project complexity while maintaining high code quality and architectural consistency.
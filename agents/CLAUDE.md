# Claude Code Agent Orchestration Patterns

This document contains orchestration patterns for working with specialized agents. These patterns should be used by the main Claude instance when coordinating development tasks.

## Agent Orchestration Workflow

When implementing features or fixes, follow these orchestration patterns to effectively utilize specialized agents:

### Available Agents and Their Roles

- **project-manager**: Planning documentation management, project state tracking, context maintenance
- **feature-architect-planner**: Comprehensive implementation planning for complex features
- **backend-database-engineer**: Database schema, migrations, API routes, server logic
- **frontend-ui-specialist**: UI components, styling, responsive design, accessibility
- **code-quality-reviewer**: Code review, testing, quality gates, manual QA
- **documentation-specialist**: Library research, technical documentation, knowledge management
- **file-refactor-organizer**: Breaking down large files (>300 lines), code organization
- **git-workflow-specialist**: Branch management, worktrees, commit hygiene

### Orchestration Patterns

#### Complete Feature Implementation Workflow
```
🚀 START-OF-WORK (project-manager):
1. Use project-manager to move plan from backlog → active
2. Use project-manager to validate requirements and acceptance criteria
3. Use feature-architect-planner if implementation plan is missing

🔧 IMPLEMENTATION PHASE:
4. Use documentation-specialist to research new libraries/patterns
5. Use git-workflow-specialist to create feature branch/worktree
6. Use backend-database-engineer for schema changes and APIs
7. Use frontend-ui-specialist for UI components
8. Use file-refactor-organizer if files exceed 300 lines

✅ END-OF-WORK (project-manager orchestrated):
9. Use code-quality-reviewer for comprehensive testing and validation
10. Use project-manager to verify QA completion and acceptance criteria
11. Use git-workflow-specialist for commits, push, and PR creation
12. Use project-manager to move plan from active → completed → archived
13. Use project-manager to coordinate human code review readiness
```

#### Library/Framework Integration
```
1. Use documentation-specialist to research and document library
2. Use backend-database-engineer or frontend-ui-specialist for implementation
3. Use code-quality-reviewer to validate integration
4. Use documentation-specialist to create integration guide in ai-docs/
```

#### Bug Fix Implementation
```
1. Use code-quality-reviewer to analyze issue and gather diagnostics
2. Use documentation-specialist to research solutions
3. Use appropriate specialist (backend/frontend) for fix
4. Use code-quality-reviewer to validate fix
```

#### Performance Optimization
```
1. Use code-quality-reviewer to identify bottlenecks
2. Use documentation-specialist to research optimization techniques
3. Use backend-database-engineer for database/API optimizations
4. Use frontend-ui-specialist for UI/bundle optimizations
5. Use code-quality-reviewer to validate improvements
```

#### Parallel Feature Development
```
1. Use project-manager to review all active plans
2. Use git-workflow-specialist to set up separate worktrees
3. Assign specialists to different worktrees:
   - Feature A: backend + frontend in worktree-A
   - Feature B: frontend + documentation in worktree-B
4. Use git-workflow-specialist for merge coordination
5. Use code-quality-reviewer for integration testing
```

### Quality Gates Before Completion

Before considering any feature complete, ensure:
- [ ] All planning requirements implemented
- [ ] Database changes validated (backend-database-engineer)
- [ ] UI responsive and accessible (frontend-ui-specialist)
- [ ] Quality gates pass (code-quality-reviewer)
- [ ] Documentation complete (documentation-specialist)
- [ ] Files under 300 lines (file-refactor-organizer)
- [ ] Clean git history (git-workflow-specialist)
- [ ] Planning docs updated (project-manager)

### Mandatory Agent Delegation

**CRITICAL: DO NOT perform actions directly when an agent specialist exists. Always delegate to the appropriate agent.**

**Proactive Agent Triggers (USE IMMEDIATELY when detected):**
- **START of any feature/task** → project-manager (move backlog → active, validate requirements)
- **END of any feature/task** → project-manager (verify QA, acceptance criteria, orchestrate delivery)
- **ANY git operation** → git-workflow-specialist (commits, branches, worktrees, merges)
- **ANY file >300 lines** → file-refactor-organizer 
- **ANY database/API work** → backend-database-engineer
- **ANY UI/component work** → frontend-ui-specialist
- **ANY testing/quality checks** → code-quality-reviewer (lint, typecheck, tests, manual QA)
- **ANY new library integration** → documentation-specialist first
- **ANY complex feature request** → feature-architect-planner
- **ANY planning doc updates** → project-manager

### Agent-First Philosophy

**Instead of:**
- "Let me commit these changes..." ❌
- "I'll create a new component..." ❌  
- "Let me run npm run lint && npm run typecheck..." ❌
- "Let me run the tests..." ❌

**Always say:**
- "I'll use git-workflow-specialist to commit these changes..." ✅
- "I'll use frontend-ui-specialist to create this component..." ✅
- "I'll use code-quality-reviewer to run quality checks..." ✅
- "I'll use code-quality-reviewer to validate the implementation..." ✅

## Project-Specific CLAUDE.md Instructions

When working in a specific project, create or update the project's **root CLAUDE.md file** (not in ai-docs) with:

1. **Project-Specific Standards**
   - TypeScript strict mode requirements
   - File organization patterns
   - Naming conventions
   - Testing requirements

2. **Domain Context**
   - Business requirements
   - Compliance needs
   - Performance constraints
   - Security considerations

3. **Technology Stack**
   - Framework preferences
   - State management approach
   - CSS framework
   - Backend patterns (Server Actions vs API routes)

4. **Quality Gates**
   - Lint commands
   - Typecheck commands
   - Test commands
   - Build commands

5. **Agent Customization**
   - Project-specific agent priorities
   - Domain-specific orchestration patterns
   - Custom quality criteria

### File Structure Clarification

**Two separate CLAUDE.md files serve different purposes:**
- **Project root `/CLAUDE.md`**: Main project guidance (tech stack, quality gates, agent patterns)
- **`ai-docs/planning/active/CLAUDE.md`**: Planning workflow and feature development guidance

### Example Project Root CLAUDE.md Update

```markdown
## Agent Orchestration for [Project Name]

### Project-Specific Patterns
- Always use backend-database-engineer for Supabase operations
- Prefer Server Actions over API routes
- Use frontend-ui-specialist for all Shadcn UI components
- Run `npm run lint && npm run typecheck` via code-quality-reviewer

### Domain Requirements
- Healthcare compliance: HIPAA considerations
- Financial data: PCI compliance needed
- User data: GDPR requirements

### Quality Standards
- No 'any' types in TypeScript
- Files must be under 300 lines
- All components need loading states
- Database operations require transactions
```

## Integration with Main Claude Thread

The main Claude instance should:
1. Use these patterns to coordinate agent work
2. Update project-specific CLAUDE.md files with discovered patterns
3. Use project-manager agent to maintain context and planning docs
4. Batch agent invocations when possible for efficiency
5. Follow the orchestration patterns appropriate to the task type

Remember: Agents cannot call other agents. All orchestration happens at the main Claude level.
# Planning Directory Structure

This directory manages feature planning and implementation tracking for the multi-agent system.

## Directory Organization

### `/active/`
**Purpose**: Currently being implemented features and improvements  
**Usage**: Active development plans that agents reference for context  
**Lifecycle**: Move to `/completed/` when implementation finished  

### `/backlog/` 
**Purpose**: Future planned work and feature requests  
**Usage**: Prioritized list of upcoming agent system enhancements  
**Lifecycle**: Move to `/active/` when development starts  

### `/completed/`
**Purpose**: Archived completed work for reference and patterns  
**Usage**: Historical record of successful implementations  
**Lifecycle**: Reference for similar future work  

## Agent Integration

### project-manager Agent
- Reviews `/active/` for current system status
- Moves completed plans from `/active/` to `/completed/`
- Identifies planning gaps and outdated documentation
- Provides status summaries referencing specific planning docs

### feature-architect-planner Agent  
- Creates detailed plans in `/active/` directory
- References completed patterns from `/completed/`
- Ensures new plans align with existing architecture
- Updates plans based on implementation feedback

### Other Agents
- Reference active plans for context during implementation
- Follow patterns established in completed plans
- Report implementation status back for planning updates

## Planning Document Lifecycle

```
1. Feature Request → /backlog/feature-name-plan.md
2. Development Starts → Move to /active/
3. Implementation Complete → Move to /completed/ 
4. Future Reference → Patterns used in new plans
```

## Document Naming Convention

Use descriptive names that indicate scope and purpose:
- `agent-creation-workflow-improvements.md` 
- `hook-performance-optimization-plan.md`
- `mcp-integration-security-enhancements.md`
- `documentation-system-reorganization.md`

## Template Reference

For planning document structure, reference:
- Existing plans in `/completed/` for patterns
- Project-specific examples in actual projects (e.g., lit-erp)
- Agent orchestration patterns in `agents/CLAUDE.md`
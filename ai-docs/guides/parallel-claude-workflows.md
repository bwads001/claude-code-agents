# Parallel Claude Workflows

Based on Anthropic's best practices for multi-agent coordination and parallel development.

## Core Patterns

### 1. Parallel Review Pattern
- **Main Claude**: Implements features
- **Review Claude**: Quality gates and testing
- **Coordination**: Git worktrees for isolated work

### 2. Explore-Plan-Execute Pattern
- **Explorer Agent**: Research and discovery
- **Architect Agent**: Planning and design
- **Implementation Agents**: Specialized execution
- **Quality Agent**: Validation and testing

### 3. Parallel Specialization Pattern
- **Frontend Specialist**: UI/UX implementation
- **Backend Specialist**: API and data layer
- **DevOps Specialist**: Infrastructure and deployment
- **Coordination**: Shared context through planning docs

## Git Worktree Setup

```bash
# Create parallel workspaces
git worktree add ../project-frontend main
git worktree add ../project-backend main
git worktree add ../project-review main

# Each Claude instance works in isolated directory
# Merge results through standard git workflow
```

## Hook Integration Points

### PreToolUse: Parallel Launch
```python
# Detect complex tasks requiring parallel agents
if task_complexity > threshold:
    launch_parallel_agents(task_breakdown)
```

### PostToolUse: Result Coordination
```python
# Merge outputs from parallel agents
merge_agent_results(agent_outputs)
validate_combined_result()
```

## Context Sharing Strategies

1. **Shared Planning Docs**: Common understanding across agents
2. **Git-based Handoffs**: Clean state transitions
3. **Structured Output Formats**: Predictable result merging
4. **Progress Tracking**: TodoWrite for coordination

## Performance Considerations

- Parallel agents can reduce task time by 90% for complex problems
- Token usage scales linearly with agent count
- Reserve for high-value, complex tasks requiring extensive exploration
- Early detection of task complexity determines parallel vs sequential approach
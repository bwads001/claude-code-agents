# Agent Coordination and Handoff Patterns

Advanced orchestration patterns for multi-agent development workflows based on Anthropic best practices.

## Core Coordination Principles

### 1. Explicit Task Decomposition
- Lead agent breaks complex tasks into clear, specific subtasks
- Each subagent receives explicit objectives and output format guidance
- Task boundaries prevent overlap and confusion

### 2. Separation of Concerns
- Give agents distinct tools and exploration paths
- Avoid overlapping responsibilities between agents
- Use specialized contexts for focused execution

### 3. Progressive Task Refinement
- Start with broad queries, progressively narrow focus
- Use extended thinking mode for visible reasoning
- Implement scaling rules based on task complexity

## Handoff Patterns

### Sequential Handoff
```
Architect Agent (planning) → 
Frontend Agent (UI) → 
Backend Agent (API) → 
Quality Agent (testing)
```

### Parallel Coordination
```
Main Thread: Task decomposition
├─ Frontend Agent: UI implementation
├─ Backend Agent: API development  
├─ Database Agent: Schema design
└─ Merge: Integration and testing
```

### Review Chain Pattern
```
Implementation Agent → 
Code Quality Agent → 
Documentation Agent → 
Final Review
```

## Context Handoff Mechanisms

### 1. Planning Document Handoffs
- Architect creates comprehensive plan
- Implementation agents reference plan sections
- Quality agent validates against original requirements

### 2. Git-based State Transfer
- Each agent works in isolated branches
- Clean merge points for state transitions
- Atomic commits enable rollback if needed

### 3. Structured Output Contracts
```json
{
  "agent": "backend-database-engineer",
  "output_format": {
    "schema_changes": "SQL DDL statements",
    "api_endpoints": "OpenAPI specification",
    "testing_notes": "Test scenarios and edge cases"
  },
  "handoff_to": "frontend-ui-specialist",
  "context_provided": "API contracts and data models"
}
```

## Coordination Triggers

### Complexity Detection
```python
# Trigger parallel agents for complex tasks
if task_complexity_score > 7:
    launch_parallel_agents(task_breakdown)
elif task_complexity_score > 4:
    use_sequential_handoff()
else:
    single_agent_execution()
```

### Quality Gate Checkpoints
- Each agent output validated before handoff
- Failed quality gates trigger refinement cycles
- Success enables next agent in chain

### Context Window Management
- Monitor token usage per agent
- Use compression agents for long contexts
- Implement context pruning strategies

## Error Recovery Patterns

### Rollback and Retry
- Git-based state rollback on failures
- Refined prompt generation for retries
- Maximum retry limits prevent infinite loops

### Alternative Agent Selection
- Fallback to different specialist on failures
- Cross-training agents for redundancy
- Escalation to human review when needed

## Performance Optimization

### Parallel Execution Benefits
- 90% time reduction for complex research tasks
- Independent context windows prevent interference
- Simultaneous exploration of solution space

### Token Efficiency
- Context sharing through structured documents
- Avoid redundant information in agent prompts
- Use compression techniques for large handoffs

### Monitoring and Metrics
- Track agent success rates by task type
- Monitor token usage per coordination pattern
- Identify bottlenecks in handoff chains

## Implementation Checklist

- [ ] Task complexity scoring system
- [ ] Agent output validation hooks
- [ ] Structured handoff format definitions
- [ ] Parallel execution orchestration
- [ ] Error recovery and retry logic
- [ ] Performance monitoring integration
- [ ] Git-based state management
- [ ] Context compression strategies
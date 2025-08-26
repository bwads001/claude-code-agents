# Multi-Agent System Debugging & Troubleshooting Guide

This guide provides systematic approaches to diagnosing and resolving issues in the multi-agent orchestration system.

## Common Issue Categories

### 1. Agent Selection and Invocation Issues
### 2. Agent Performance and Context Problems  
### 3. Hook Execution and Configuration Issues
### 4. MCP Integration and Tool Access Problems
### 5. Orchestration and Coordination Failures
### 6. Project Setup and Configuration Issues

## Diagnostic Tools and Commands

### Basic Diagnostics

#### Check Agent Availability
```bash
# List all available agents
/agents

# Check agent file existence
ls ~/.claude/agents/
ls .claude/agents/

# Validate agent file format
head -20 ~/.claude/agents/backend-database-engineer.md
```

#### Debug Mode
```bash
# Run Claude Code with full debugging
claude --debug

# Monitor specific debug output
claude --debug 2>&1 | grep -E "(agent|hook|mcp)"

# Check Claude log files
tail -f ~/.claude/claude.log
```

#### Hook Configuration Check
```bash
# Check hook configuration
/hooks

# Validate settings JSON
jq . ~/.claude/settings.json
jq . .claude/settings.json
```

### Advanced Diagnostics

#### Agent Performance Analysis
```bash
# Monitor agent execution times
grep -E "Task.*duration" ~/.claude/claude.log | tail -20

# Check agent memory usage
ps aux | grep claude

# Monitor file system changes during agent execution
fswatch . | ts '[%H:%M:%S]'
```

#### MCP Server Status
```bash
# Test MCP server connectivity
echo '{"method": "tools/list"}' | npx @context7/mcp-server
echo '{"method": "tools/list"}' | npx @neondatabase/mcp-server

# Check MCP configuration
cat ~/.claude.json | jq .mcpServers

# Monitor MCP tool usage
grep "mcp__" ~/.claude/claude.log | tail -20
```

## Issue-Specific Troubleshooting

### Agent Selection Issues

#### Problem: Wrong agent being selected
**Symptoms:**
- Claude uses general approach instead of specialized agent
- Wrong agent type invoked for task
- Agent not invoked at all when expected

**Diagnostic Steps:**
1. Check agent descriptions for keyword matching:
```bash
grep -n "description:" ~/.claude/agents/*.md
grep -n "description:" .claude/agents/*.md
```

2. Verify agent file format:
```bash
# Check YAML frontmatter syntax
head -10 ~/.claude/agents/problematic-agent.md
```

3. Test explicit invocation:
```bash
# In Claude Code
> Use the backend-database-engineer agent to create user schema
```

**Solutions:**
- **Improve descriptions**: Add trigger keywords like "use proactively", "immediately after"
- **Fix YAML syntax**: Ensure proper frontmatter formatting
- **Remove conflicts**: Check for duplicate agent names
- **Explicit requests**: Use "Use the [agent-name] agent" for specific tasks

#### Problem: Agent not found or available
**Symptoms:**
- "Agent not found" errors
- Agent doesn't appear in `/agents` list
- File exists but agent not loaded

**Diagnostic Steps:**
1. Check file location and naming:
```bash
# Verify file structure
find ~/.claude/agents -name "*.md"
find .claude/agents -name "*.md"

# Check filename matches agent name
grep "^name:" ~/.claude/agents/*.md
```

2. Validate file permissions:
```bash
ls -la ~/.claude/agents/
ls -la .claude/agents/
```

3. Test file syntax:
```bash
# Check for YAML parsing errors
python3 -c "
import yaml
with open('~/.claude/agents/agent-name.md') as f:
    content = f.read()
    parts = content.split('---')
    if len(parts) >= 3:
        yaml.safe_load(parts[1])
    else:
        print('Invalid frontmatter format')
"
```

**Solutions:**
- **Fix file naming**: Ensure filename matches `name` field
- **Correct permissions**: `chmod 644` for agent files
- **Fix YAML syntax**: Validate frontmatter format
- **Restart session**: Use `/clear` to reload agent definitions

### Agent Performance Issues

#### Problem: Agent taking too long or timing out
**Symptoms:**
- Agent invocations hang indefinitely
- Timeout errors during agent execution
- Slow response times from agents

**Diagnostic Steps:**
1. Monitor agent execution:
```bash
# Watch agent processes
watch -n 1 'ps aux | grep -E "(claude|node)" | head -10'

# Check system resources
top -p $(pgrep claude)
```

2. Check task complexity:
```bash
# Review agent prompts for complexity
grep -A 20 "tool_input" ~/.claude/claude.log | tail -50
```

3. Test with simpler tasks:
```bash
# Try minimal agent invocation
> Use the file-refactor-organizer agent to check if any files are over 300 lines
```

**Solutions:**
- **Break down complex tasks**: Split large requests into smaller agent tasks
- **Optimize agent prompts**: Remove unnecessary instructions
- **Increase timeout**: Configure longer timeouts in hooks if needed
- **Check system resources**: Ensure adequate memory and CPU

#### Problem: Agent providing poor quality outputs
**Symptoms:**
- Agent responses don't meet expectations
- Missing required information in agent reports
- Agent not following established patterns

**Diagnostic Steps:**
1. Review agent system prompts:
```bash
# Check agent prompt quality
cat ~/.claude/agents/problematic-agent.md
```

2. Analyze recent agent outputs:
```bash
# Check agent response patterns
grep -A 50 "tool_response.*Task" ~/.claude/claude.log | tail -100
```

3. Compare with working agents:
```bash
# Compare successful agent prompts
diff ~/.claude/agents/working-agent.md ~/.claude/agents/problematic-agent.md
```

**Solutions:**
- **Improve system prompts**: Add specific instructions and examples
- **Add reporting requirements**: Include mandatory reporting sections
- **Use reference patterns**: Copy successful agent prompt structures
- **Test iteratively**: Refine prompts based on actual outputs

### Hook Execution Issues

#### Problem: Hooks not executing
**Symptoms:**
- Expected hook behavior not occurring
- No hook output in debug logs
- Hook scripts never run

**Diagnostic Steps:**
1. Check hook configuration:
```bash
# Verify hook is registered
/hooks

# Check settings file syntax
jq . ~/.claude/settings.json
jq . .claude/settings.json
```

2. Test hook script manually:
```bash
# Create test input and run hook
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.txt"}}' | \
  .claude/hooks/your-hook-script.py
```

3. Check hook permissions:
```bash
ls -la .claude/hooks/
# Should show executable permissions (x)
```

**Solutions:**
- **Fix JSON syntax**: Validate settings.json files
- **Make scripts executable**: `chmod +x .claude/hooks/script.py`
- **Check matchers**: Ensure hook matcher patterns are correct
- **Test script logic**: Run hooks manually with test data

#### Problem: Hook errors or failures  
**Symptoms:**
- Hook scripts exit with errors
- Hook outputs show in stderr
- Hooks blocking operations unexpectedly

**Diagnostic Steps:**
1. Check hook execution logs:
```bash
# Monitor hook execution
claude --debug 2>&1 | grep -E "(hook|Hook)"

# Check specific hook errors
grep -A 5 -B 5 "hook.*error" ~/.claude/claude.log
```

2. Test hook script independently:
```bash
# Run hook with debug output
bash -x .claude/hooks/failing-hook.py < test-input.json
```

3. Validate hook input/output format:
```bash
# Check JSON input format
echo '{"test": "data"}' | jq . | .claude/hooks/hook.py
```

**Solutions:**
- **Add error handling**: Wrap hook logic in try/catch blocks
- **Validate inputs**: Check JSON format and required fields
- **Fix exit codes**: Use appropriate exit codes (0=success, 2=block, others=error)
- **Debug step-by-step**: Add print statements for debugging

### MCP Integration Issues

#### Problem: MCP tools not available to agents
**Symptoms:**
- Agent reports MCP tool not found
- MCP tools don't appear in agent tool lists
- MCP operations fail silently

**Diagnostic Steps:**
1. Check MCP server configuration:
```bash
# Verify MCP servers are configured
cat ~/.claude.json | jq .mcpServers

# Test MCP server connectivity
echo '{"method": "tools/list"}' | npx @context7/mcp-server
```

2. Check agent tool permissions:
```bash
# Look for tools field in agent definition
grep -A 5 "tools:" ~/.claude/agents/agent-name.md

# Check if agent inherits all tools (no tools field)
head -10 ~/.claude/agents/agent-name.md
```

3. Test MCP tools directly:
```bash
# In Claude Code, test MCP tool access
> List available MCP tools
```

**Solutions:**
- **Configure MCP servers**: Add missing servers to ~/.claude.json
- **Check credentials**: Verify API keys and authentication
- **Fix agent permissions**: Remove `tools:` field or add specific MCP tools
- **Restart Claude**: MCP configuration changes require restart

#### Problem: MCP tool authentication failures
**Symptoms:**
- "Authentication failed" errors
- API key or credential errors
- MCP tools return permission denied

**Diagnostic Steps:**
1. Check credential configuration:
```bash
# Verify environment variables (don't show values)
env | grep -E "(NEON|GITHUB|API)" | cut -d= -f1

# Check MCP server environment
cat ~/.claude.json | jq '.mcpServers[].env'
```

2. Test credentials directly:
```bash
# Test Neon API key
curl -H "Authorization: Bearer $NEON_API_KEY" https://console.neon.tech/api/v2/projects

# Test other API credentials according to service documentation
```

**Solutions:**
- **Update credentials**: Refresh expired API keys
- **Fix environment variables**: Set required environment variables
- **Check permissions**: Ensure API keys have necessary permissions
- **Verify service status**: Check if MCP services are operational

### Orchestration Issues

#### Problem: Agents not working together effectively
**Symptoms:**
- Duplicate work across agents
- Agents making conflicting changes
- Poor handoff between agents

**Diagnostic Steps:**
1. Review orchestration patterns:
```bash
# Check main orchestration guidance
cat ~/.claude/agents/CLAUDE.md

# Review project-specific patterns
cat CLAUDE.md | grep -A 20 "orchestration"
```

2. Analyze agent interaction logs:
```bash
# Track agent sequence and timing
grep "Task.*duration" ~/.claude/claude.log | head -20

# Check for concurrent agent execution
grep -E "Task.*started|Task.*completed" ~/.claude/claude.log
```

**Solutions:**
- **Use sequential orchestration**: Coordinate agents in proper order
- **Improve handoff reporting**: Ensure agents provide comprehensive reports
- **Use git-workflow-specialist**: For parallel development coordination
- **Update orchestration patterns**: Refine patterns based on experience

#### Problem: Context loss between agents
**Symptoms:**
- Agents repeat work or analysis
- Agents miss important project context
- Inconsistent implementation approaches

**Diagnostic Steps:**
1. Check context preservation:
```bash
# Review agent reporting patterns
grep -A 10 "REPORTING BACK" ~/.claude/agents/*.md
```

2. Analyze context flow:
```bash
# Check project context files
ls -la ai-docs/
cat ai-docs/planning/active/*.md | head -50
```

**Solutions:**
- **Improve agent reporting**: Add comprehensive reporting sections
- **Use project-manager**: For context tracking and handoff
- **Maintain ai-docs**: Keep project documentation current
- **Use context injection hooks**: Add project state to agent inputs

## Performance Optimization

### Agent Performance Tuning

#### Optimize Agent System Prompts
```markdown
# Good: Specific, focused prompt
---
name: schema-specialist
description: Database schema design and migrations only
tools: Read, Edit, Write, Bash
---

You are a database schema specialist. Create schemas and migrations only.
Provide schema code and migration steps. Report schema changes made.

# Bad: Vague, unfocused prompt  
---
name: backend-helper
description: Help with backend tasks
---

You help with various backend development tasks including but not limited to...
[500 lines of instructions]
```

#### Reduce Agent Complexity
```bash
# Break complex agents into focused specialists
Before: full-stack-developer (does everything)
After: 
  - schema-specialist (database only)
  - api-specialist (endpoints only) 
  - validation-specialist (data validation only)
```

### System Performance Monitoring

#### Track Agent Usage Patterns
```python
#!/usr/bin/env python3
"""Agent performance monitoring"""
import re
from collections import defaultdict

def analyze_agent_performance(log_file):
    """Analyze agent execution patterns"""
    agent_stats = defaultdict(lambda: {'count': 0, 'total_time': 0})
    
    with open(log_file) as f:
        for line in f:
            # Match agent execution patterns
            match = re.search(r'Task\((.*?)\).*duration: (\d+\.?\d*)ms', line)
            if match:
                agent = match.group(1)
                duration = float(match.group(2))
                
                agent_stats[agent]['count'] += 1
                agent_stats[agent]['total_time'] += duration
    
    # Print performance summary
    for agent, stats in agent_stats.items():
        avg_time = stats['total_time'] / stats['count']
        print(f"{agent}: {stats['count']} calls, avg {avg_time:.1f}ms")

# Usage
analyze_agent_performance('~/.claude/claude.log')
```

## Best Practices for Prevention

### Agent Design Best Practices
- **Single responsibility**: Each agent should have one clear purpose
- **Comprehensive reporting**: Always report back to main thread
- **Error handling**: Handle edge cases gracefully
- **Tool efficiency**: Only request necessary tools
- **Context awareness**: Reference project patterns from ai-docs

### Hook Design Best Practices  
- **Fail gracefully**: Don't block operations for non-critical hooks
- **Validate inputs**: Check JSON format and required fields
- **Use timeouts**: Prevent hooks from hanging indefinitely
- **Log appropriately**: Use stdout for data, stderr for errors
- **Test thoroughly**: Test hooks with various input scenarios

### System Integration Best Practices
- **Version control**: Keep agent definitions and hooks in git
- **Document dependencies**: Clear README for MCP setup
- **Test systematically**: Validate agent interactions regularly  
- **Monitor performance**: Track agent usage and timing
- **Coordinate team usage**: Shared standards for agent/hook development

## Emergency Procedures

### System Recovery
```bash
# Reset to clean state
/clear

# Disable all hooks temporarily
mv ~/.claude/settings.json ~/.claude/settings.json.backup
mv .claude/settings.json .claude/settings.json.backup

# Test with minimal configuration
claude --debug

# Restore configurations one at a time
cp ~/.claude/settings.json.backup ~/.claude/settings.json
```

### Agent System Backup and Restore
```bash
# Backup entire agent system
tar -czf claude-agent-backup-$(date +%Y%m%d).tar.gz ~/.claude/agents .claude/

# Restore from backup
tar -xzf claude-agent-backup-20240101.tar.gz

# Selective restore of specific agents
cp backup/agents/working-agent.md ~/.claude/agents/
```

This guide provides systematic approaches to identifying and resolving issues in multi-agent systems. Use the diagnostic steps to identify root causes, then apply the appropriate solutions to restore functionality.
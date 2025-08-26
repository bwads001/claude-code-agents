# MCP Integration Guide for Multi-Agent Systems

This guide shows how to integrate Model Context Protocol (MCP) servers with the multi-agent orchestration system, providing agents with specialized external capabilities.

## MCP Overview

MCP servers extend Claude Code with additional tools and resources. Popular MCP servers include:

- **Context7**: Library documentation and code examples
- **Playwright**: Browser automation and testing
- **Neon**: Database operations and management  
- **Memory**: Persistent context and entity tracking
- **Filesystem**: Enhanced file operations
- **GitHub**: Repository management and API access

## MCP Server Configuration

### Configuration Location
MCP servers are configured in your main Claude configuration file:
- **Location**: `~/.claude.json` (not in the `.claude/` agent directory)
- **Scope**: Available to all Claude Code sessions
- **Security**: Contains sensitive credentials, never commit to git

### Example Configuration
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-playwright"]
    },
    "neon": {
      "command": "npx",
      "args": ["-y", "@neondatabase/mcp-server"],
      "env": {
        "NEON_API_KEY": "your-neon-api-key"
      }
    }
  }
}
```

### Agent System Separation
**Important**: Keep MCP configuration separate from the agent system:

```
~/.claude.json          # MCP server configurations (sensitive)
~/.claude/              # Agent system (shareable via git)
├── agents/             # Agent definitions
├── ai-docs/            # Documentation  
└── .gitignore          # Excludes ~/.claude.json
```

## MCP Tool Access in Agents

### Default Behavior: Full MCP Access
Agents inherit all MCP tools when the `tools` field is omitted:

```markdown
---
name: research-specialist
description: Research libraries and create documentation using Context7
# No tools field = inherits all MCP tools
---

You are a research specialist with access to Context7 MCP for library documentation.
Use Context7 tools to research libraries thoroughly before implementation.
```

### Selective MCP Access
Agents can be limited to specific MCP tools:

```markdown
---
name: database-specialist
description: Database operations specialist using Neon MCP
tools: Read, Edit, Write, mcp__neon__run_sql, mcp__neon__create_project
---

You are a database specialist with access to Neon database operations.
Use Neon MCP tools for database management and SQL operations.
```

### MCP Tool Naming Pattern
MCP tools follow the pattern: `mcp__<server>__<tool>`

Examples:
- `mcp__context7__get_library_docs` - Get library documentation
- `mcp__playwright__browser_navigate` - Browser navigation
- `mcp__neon__run_sql` - Execute SQL queries
- `mcp__memory__create_entities` - Create memory entities

## Agent-Specific MCP Integration Patterns

### Research and Documentation Agent
```markdown
---
name: documentation-specialist
description: Research libraries and create technical documentation
tools: Read, Write, Edit, mcp__context7__resolve_library_id, mcp__context7__get_library_docs
---

You are a technical documentation specialist with access to Context7 for library research.

**Research Workflow:**
1. Use `mcp__context7__resolve_library_id` to find the correct library ID
2. Use `mcp__context7__get_library_docs` to get comprehensive documentation
3. Create detailed integration guides in `ai-docs/library-guides/`
4. Include code examples and best practices

**Documentation Standards:**
- Always verify library compatibility with project tech stack
- Include installation instructions and configuration
- Provide working code examples
- Document common patterns and gotchas
- Reference official documentation sources

**Reporting Back:**
Report the library guide created, key integration patterns discovered, and any compatibility concerns for the main thread to coordinate implementation.
```

### QA and Testing Agent
```markdown
---
name: qa-automation-specialist  
description: Automated testing using browser automation and cross-device validation
tools: Read, mcp__playwright__browser_navigate, mcp__playwright__browser_click, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_snapshot
---

You are a QA automation specialist using Playwright for comprehensive testing.

**Testing Workflow:**
1. Navigate to application pages using Playwright browser tools
2. Test user workflows across different viewport sizes
3. Capture screenshots of UI issues or successful states
4. Validate accessibility and keyboard navigation
5. Test form submissions and data handling

**Cross-Device Testing:**
- Desktop: 1920x1080 viewport
- Tablet: 768x1024 viewport  
- Mobile: 375x667 viewport
- Test responsive breakpoints and component behavior

**Issue Documentation:**
- Screenshot evidence of issues with viewport dimensions
- Specific steps to reproduce problems
- Accessibility compliance validation
- Performance observations

Always provide specific, actionable feedback with visual evidence.
```

### Database Operations Agent
```markdown
---
name: database-engineer
description: Database schema design and operations using Neon database platform
tools: Read, Edit, Write, mcp__neon__run_sql, mcp__neon__create_branch, mcp__neon__prepare_database_migration
---

You are a database engineer with access to Neon database operations.

**Database Development Workflow:**
1. Use `mcp__neon__create_branch` for safe schema changes
2. Design schema updates with proper relationships
3. Use `mcp__neon__prepare_database_migration` for complex changes
4. Test migrations thoroughly before applying to main branch
5. Document schema decisions and migration strategies

**Safety Practices:**
- Always create branches for schema experiments
- Test data migrations with realistic datasets
- Validate performance impact of index changes
- Ensure foreign key constraints maintain data integrity
- Document rollback procedures for complex migrations

**Integration with Project:**
- Follow project's database patterns in `lib/db/schema/`
- Coordinate with frontend agents for API contract changes
- Update TypeScript types after schema changes
- Ensure migration compatibility with existing data
```

## MCP Integration in Orchestration Workflows

### Library Integration Workflow
```
1. Use documentation-specialist with Context7 MCP to research library
2. Create integration guide in ai-docs/library-guides/
3. Use backend-database-engineer or frontend-ui-specialist for implementation  
4. Use qa-automation-specialist with Playwright MCP for validation
5. Update project patterns based on successful integration
```

### Feature Development with Database Changes
```
1. Use project-manager to review requirements
2. Use database-engineer with Neon MCP for schema design
3. Use backend-database-engineer for API implementation
4. Use frontend-ui-specialist for UI components
5. Use qa-automation-specialist with Playwright MCP for end-to-end testing
6. Use code-quality-reviewer for final validation
```

### Research-Driven Development
```
1. Use documentation-specialist with Context7 MCP to research solutions
2. Create technical spike documentation in ai-docs/
3. Use feature-architect-planner for implementation strategy
4. Coordinate specialist agents based on research findings
5. Use qa-automation-specialist for validation against research criteria
```

## Project-Specific MCP Configurations

### Cannabis ERP Example
For the cannabis ERP project, MCP integration enhances compliance and testing:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "neon": {
      "command": "npx", 
      "args": ["-y", "@neondatabase/mcp-server"],
      "env": {
        "NEON_API_KEY": "your-api-key"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-playwright"]
    }
  }
}
```

**Agent Usage Patterns:**
- **documentation-specialist**: Research cannabis compliance frameworks
- **database-engineer**: Design METRC-compliant data schemas  
- **qa-automation-specialist**: Test multi-location inventory workflows
- **backend-database-engineer**: Implement traceability APIs

### Project CLAUDE.md Integration
Update your project's CLAUDE.md to reference MCP capabilities:

```markdown
## MCP Integration

This project uses MCP servers for enhanced capabilities:

### Available MCP Tools
- **Context7**: Library research and documentation (`mcp__context7__*`)
- **Neon Database**: Schema management and SQL operations (`mcp__neon__*`)
- **Playwright**: Browser testing and UI validation (`mcp__playwright__*`)

### Agent MCP Usage
- **documentation-specialist**: Uses Context7 for library research
- **database-engineer**: Uses Neon for schema operations
- **qa-automation-specialist**: Uses Playwright for testing
- **backend-database-engineer**: May use Neon for database operations
- **frontend-ui-specialist**: May use Playwright for UI testing

### MCP Tool Patterns
```bash
# Research new library
> Use documentation-specialist to research React Query integration with Context7

# Database operations  
> Use database-engineer to create customer tier schema with Neon

# UI testing
> Use qa-automation-specialist to test responsive dashboard with Playwright
```
```

## Hooks Integration with MCP Tools

### MCP Tool Monitoring Hook
Track MCP tool usage across agents:

```python
#!/usr/bin/env python3
"""Monitor MCP tool usage in multi-agent workflows"""
import json
import sys
import re
from pathlib import Path

MCP_LOG = Path(".claude/mcp-usage.log")

def log_mcp_usage(tool_name, agent_type, success):
    """Log MCP tool usage"""
    import time
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp},{tool_name},{agent_type},{success}\n"
    
    MCP_LOG.parent.mkdir(exist_ok=True)
    with open(MCP_LOG, 'a') as f:
        f.write(log_entry)

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    if tool_name.startswith("mcp__"):
        # Extract MCP server and tool
        mcp_match = re.match(r'mcp__([^_]+)__(.+)', tool_name)
        if mcp_match:
            server, tool = mcp_match.groups()
            
            # Get agent context if available
            tool_input = data.get("tool_input", {})
            agent_type = tool_input.get("subagent_type", "main_thread")
            
            # Log successful MCP tool usage
            log_mcp_usage(f"{server}::{tool}", agent_type, True)
            print(f"📊 Logged MCP usage: {server}::{tool} by {agent_type}")

except Exception as e:
    print(f"Error logging MCP usage: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on logging errors
```

### MCP Error Handling Hook
Provide better error messages for MCP failures:

```python
#!/usr/bin/env python3
"""Enhanced error handling for MCP tool failures"""
import json
import sys

MCP_ERROR_SOLUTIONS = {
    "context7": {
        "library_not_found": "Try different library name variations or check spelling",
        "rate_limit": "Wait before making additional Context7 requests",
        "network_error": "Check internet connection and Context7 service status"
    },
    "neon": {
        "auth_error": "Verify NEON_API_KEY in ~/.claude.json configuration",
        "database_not_found": "Check project ID and database name spelling",
        "connection_timeout": "Neon database may be starting up, try again"
    },
    "playwright": {
        "browser_not_installed": "Run: npx playwright install",
        "page_load_timeout": "Increase timeout or check page URL",
        "element_not_found": "Verify element selector and page load state"
    }
}

def provide_mcp_solution(server, error_msg):
    """Provide specific solution for MCP errors"""
    solutions = MCP_ERROR_SOLUTIONS.get(server, {})
    
    for error_type, solution in solutions.items():
        if error_type in error_msg.lower():
            return solution
    
    return f"Check {server} MCP server configuration and network connectivity"

# Main execution for PostToolUse hook
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_response = data.get("tool_response", {})
    
    if tool_name.startswith("mcp__") and not tool_response.get("success", True):
        # Extract MCP server name
        server = tool_name.split("__")[1]
        error_msg = tool_response.get("error", "Unknown error")
        
        solution = provide_mcp_solution(server, error_msg)
        
        feedback = f"""
🔧 **MCP Tool Error - {server}**
Error: {error_msg}

**Suggested Solution:**
{solution}

**General Troubleshooting:**
1. Check MCP server configuration in ~/.claude.json
2. Verify network connectivity and service status  
3. Review MCP server documentation for specific requirements
"""
        
        print(feedback, file=sys.stderr)  # Feedback to Claude

except Exception as e:
    print(f"Error in MCP error handling: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on error handling errors
```

## MCP Server Management

### Installing MCP Servers
```bash
# Context7 for library documentation
npm install -g @context7/mcp-server

# Playwright for browser automation  
npm install -g @anthropic-ai/mcp-server-playwright
npx playwright install  # Install browsers

# Neon for database operations
npm install -g @neondatabase/mcp-server
```

### Testing MCP Integration
```bash
# Test Context7 connection
echo '{"method": "tools/list"}' | npx @context7/mcp-server

# Test Neon with API key
NEON_API_KEY=your-key echo '{"method": "tools/list"}' | npx @neondatabase/mcp-server

# Test Playwright installation
npx playwright --version
```

### Debugging MCP Issues
```bash
# Run Claude Code with debug output
claude --debug

# Check MCP server logs
tail -f ~/.claude/claude.log | grep -i mcp

# Validate MCP configuration
cat ~/.claude.json | jq .mcpServers
```

## Security and Best Practices

### Security Guidelines
- **Keep credentials secure** in `~/.claude.json` (never commit)
- **Use environment variables** for sensitive MCP configuration
- **Limit agent tool access** to only required MCP tools
- **Validate MCP tool outputs** before using in production
- **Monitor MCP tool usage** for unexpected behavior

### Performance Best Practices  
- **Cache MCP responses** when possible to avoid repeated calls
- **Use specific MCP tools** rather than broad permission grants
- **Set timeouts** for MCP operations in hooks
- **Monitor MCP service limits** and rate limiting
- **Test MCP integration** thoroughly in development

### Integration Best Practices
- **Document MCP dependencies** in project README
- **Version pin MCP servers** for consistency across team
- **Test MCP server updates** before deploying
- **Coordinate MCP tool usage** across agents to avoid conflicts
- **Provide fallback behavior** when MCP tools are unavailable

This guide provides comprehensive patterns for integrating MCP servers into multi-agent workflows, enhancing agent capabilities while maintaining security and reliability.
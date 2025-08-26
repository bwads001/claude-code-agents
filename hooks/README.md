# Quality Automation Hooks

This directory contains **quality automation hooks** that provide automatic validation, context injection, and performance monitoring for Claude Code workflows. Hooks execute automatically at specific points during tool usage, creating a seamless quality assurance layer.

## What Are Hooks?

Hooks are scripts that execute automatically when Claude Code uses specific tools. They run in the background to provide context, validate quality, and monitor performance without interrupting the development workflow.

**Key Concepts:**
- Hooks execute automatically at defined trigger points (PreToolUse, PostToolUse)
- They can inject context, validate outputs, or perform monitoring
- Hooks should **never block** workflow - they warn but don't stop execution
- Multiple hooks can run for the same trigger event

**Reference:** [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)

## Hook System Architecture

### **Hook Types**
- **PreToolUse:** Execute before a tool is called (context injection, preparation)
- **PostToolUse:** Execute after a tool completes (validation, monitoring, cleanup)

### **Hook Configuration**
Hooks are registered in `settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [{ "type": "command", "command": "/path/to/hook.py" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit", 
        "hooks": [{ "type": "command", "command": "/path/to/validator.py" }]
      }
    ]
  }
}
```

## Available Quality Automation Hooks

### 🧠 **agent-context-injection.py** (PreToolUse)
**Trigger:** Before any `Task` tool (agent invocation)  
**Purpose:** Inject project context so agents don't waste time on discovery

#### **What It Does:**
- Provides project directory structure automatically
- Lists available documentation in `ai-docs/` 
- Includes current git branch context
- Agent-specific focus areas (backend vs frontend vs QA)

#### **Agent-Specific Context:**
```python
AGENT_FOCUS = {
    "backend-database-engineer": "database, server logic, APIs",
    "frontend-ui-specialist": "UI components, styling, client-side", 
    "code-quality-reviewer": "testing, linting, quality gates"
}
```

#### **Benefits:**
- Eliminates agent discovery phase
- Provides consistent project context
- Reduces token usage by preventing redundant exploration
- Ensures agents know what documentation is available

---

### ⚡ **agent-performance-monitor.py** (PreToolUse)  
**Trigger:** Before any `Task` tool (agent invocation)  
**Purpose:** Track agent usage patterns and suggest optimizations

#### **What It Does:**
- Records agent invocation frequency and task complexity
- Tracks daily usage patterns across different agents
- Suggests batching for repetitive simple tasks
- Identifies optimization opportunities

#### **Metrics Tracked:**
- Total agent calls per agent type
- Average task complexity scores
- Recent call patterns (last 24 hours)
- Daily statistics and agent distribution

#### **Smart Suggestions:**
- "Consider combining simple tasks to reduce overhead"
- "Detected repetitive tasks - consider batch processing"
- Performance trends and usage optimization tips

---

### ✅ **agent-result-validator.py** (PostToolUse)
**Trigger:** After any `Task` tool (agent completion)  
**Purpose:** Validate agent text responses meet quality standards

#### **Quality Gates by Agent Type:**
- **All Agents:** No `TODO:`, `FIXME:`, compatibility bloat, or `console.log`
- **Backend Engineer:** Must contain database/API patterns, no debugging cruft
- **Frontend Specialist:** Must contain component patterns, no `alert()` calls
- **Code Quality Reviewer:** Must contain testing patterns, no skipped tests
- **Feature Architect:** Must have structured output, no uncertain language

#### **Universal Anti-Patterns Blocked:**
```python
UNIVERSAL_FORBIDDEN = [
    r"TODO:|FIXME:",
    r"backwards? compatib",  # Prevents compatibility bloat
    r"in a real (implementation|app|application|world|scenario)", 
    r"console\.log"
]
```

#### **Benefits:**
- Prevents low-quality agent outputs
- Blocks compatibility bloat and debugging remnants
- Ensures agents give concrete implementation vs theoretical advice
- Maintains consistent quality standards across all agents

---

### 🔍 **file-content-validator.py** (PostToolUse)
**Trigger:** After `Edit`, `Write`, or `MultiEdit` tools  
**Purpose:** Validate actual code files meet quality standards

#### **Code Quality Patterns Blocked:**
```python
FILE_FORBIDDEN = [
    r"TODO:",
    r"FIXME:", 
    r"console\.log\(.*\);?\s*$",  # Standalone console.log lines
    r"backwards?\s+compatib",     # Compatibility bloat
    r"alert\(",
    r"debugger;?"
]
```

#### **Smart File Detection:**
- Only validates code files (`.js`, `.ts`, `.py`, `.go`, etc.)
- Shows specific line numbers and matched patterns
- Provides actionable feedback for fixing issues
- Non-blocking - warns but doesn't prevent edits

#### **Benefits:**
- Prevents debugging cruft from reaching version control
- Eliminates compatibility bloat at the source
- Maintains code quality without manual oversight
- Works automatically on every file modification

## Hook Integration with Agent System

### **Seamless Quality Pipeline**
```
PreToolUse Hooks → Agent Execution → PostToolUse Hooks
     ↓                    ↓                 ↓
Context Injection → Specialized Work → Quality Validation
Performance Monitor   Expert Analysis   Result Validation
                                       File Content Check
```

### **Division of Labor**
- **Hooks Handle:** Automatic validation, context injection, performance tracking
- **Agents Handle:** Complex reasoning, domain expertise, implementation
- **Main Claude:** Orchestration, decision-making, workflow coordination

### **Quality Gate Redundancy Removal**
With hooks handling automatic validation:
- Agents no longer run `lint`/`typecheck` manually
- code-quality-reviewer focuses on manual testing and UX validation  
- Backend/frontend agents focus on implementation, not tool execution
- Quality validation happens automatically and consistently

## Hook Development Guidelines

### **Hook Script Structure**
```python
#!/usr/bin/env python3
"""Hook description and purpose"""
import json
import sys

def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        
        # Hook logic here
        if tool_name == "Task":
            # Handle agent invocation
            pass
            
        # Provide feedback to stderr (visible to user)
        print("✅ Hook completed successfully", file=sys.stderr)
        
    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Never block workflow

if __name__ == "__main__":
    main()
```

### **Hook Best Practices**
1. **Never Block Workflow:** Always `sys.exit(0)` on errors
2. **Provide Feedback:** Use `sys.stderr` for user-visible messages
3. **Fast Execution:** Keep hooks lightweight and quick
4. **Error Handling:** Gracefully handle all failure modes
5. **Useful Output:** Provide actionable feedback and suggestions

### **Hook Input/Output**
- **Input (stdin):** JSON with `tool_name`, `tool_input`, `tool_result` 
- **User Feedback (stderr):** Progress messages and warnings
- **Return Code:** 0 = success (even on validation failures)

## Creating Custom Hooks

### **Hook Registration**
Add to `settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/custom-hook.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### **Matcher Patterns**
- **Single Tool:** `"Task"`, `"Edit"`, `"Read"`
- **Multiple Tools:** `"Edit|Write|MultiEdit"`
- **All Tools:** `".*"`
- **Pattern Matching:** Full regex support

### **Hook Types**
- **command:** Execute shell script/binary
- **python:** Execute Python code directly (if supported)

## Advanced Hook Patterns

### **Conditional Execution**
```python
# Only run for specific agent types
agent_type = tool_input.get("subagent_type", "")
if agent_type in ["backend-database-engineer", "frontend-ui-specialist"]:
    # Run validation
    pass
```

### **Context-Aware Validation**
```python
# Different validation based on file type
file_path = tool_input.get("file_path", "")
if file_path.endswith(('.ts', '.tsx')):
    # TypeScript-specific validation
elif file_path.endswith(('.py')):  
    # Python-specific validation
```

### **Progressive Enhancement**
```python
# Provide increasingly sophisticated analysis
basic_check = validate_basic_patterns(content)
if basic_check.passed:
    advanced_check = validate_advanced_patterns(content)
    if advanced_check.passed:
        security_check = validate_security_patterns(content)
```

## Troubleshooting Hook Issues

### **Hook Not Executing**
1. Check hook is registered in `settings.json`
2. Verify file path is absolute and executable (`chmod +x hook.py`)
3. Ensure matcher pattern matches the tool being used
4. Check timeout is sufficient for hook execution

### **Hook Failing Silently** 
1. Test hook manually: `echo '{"tool_name":"Test"}' | ./hook.py`
2. Check Python path and script permissions
3. Verify JSON parsing handles all expected inputs
4. Add debug logging to identify failure points

### **Hook Blocking Workflow**
1. Ensure all code paths call `sys.exit(0)`
2. Wrap all logic in try/catch blocks
3. Set reasonable timeout values in settings
4. Test with various input scenarios

### **Performance Issues**
1. Profile hook execution time
2. Cache expensive operations when possible  
3. Use lazy loading for heavy imports
4. Consider async patterns for I/O operations

## Integration with Development Workflow

### **Invisible Quality Gates**
Hooks work seamlessly in the background:
```bash
# User workflow remains the same
claude "Implement user authentication"

# But hooks automatically:
# 1. Inject project context before agent runs
# 2. Monitor performance and usage patterns  
# 3. Validate agent output quality
# 4. Check file content for code quality issues
```

### **Quality Feedback Loop**
```
Code → Automatic Validation → Immediate Feedback → Correction → Quality
  ↑                                                             ↓
  ←←←←←←←←←← Continuous Improvement ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### **Development Team Benefits**
- **Consistent Quality:** Same standards applied automatically across all work
- **Reduced Overhead:** No manual quality gate execution required
- **Early Detection:** Issues caught immediately vs. during review
- **Knowledge Sharing:** Context injection spreads project knowledge
- **Performance Optimization:** Usage monitoring identifies improvement opportunities

## Best Practices for Hook Usage

### **Hook Selection Strategy**
- **Use PreToolUse** for context injection and preparation
- **Use PostToolUse** for validation and monitoring
- **Keep hooks focused** on single responsibilities
- **Chain hooks** for complex validation pipelines

### **Quality Gate Design**
- **Block only critical issues** that prevent functionality
- **Warn about quality concerns** that need attention
- **Provide actionable feedback** with specific recommendations
- **Maintain consistent standards** across all validation points

### **Performance Considerations**
- **Monitor hook execution time** and optimize slow hooks
- **Use appropriate timeouts** to prevent workflow blocking  
- **Cache expensive operations** across hook invocations
- **Consider hook impact** on overall development velocity

This hook system transforms Claude Code into a **self-validating development environment** where quality gates operate automatically and consistently, freeing developers to focus on creative problem-solving while maintaining high standards.
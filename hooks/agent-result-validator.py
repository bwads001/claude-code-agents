#!/usr/bin/env python3
"""Post-agent execution result validation and quality gates"""
import json
import sys
import re

# Universal forbidden patterns for all agents
UNIVERSAL_FORBIDDEN = [
    r"TODO:|FIXME:",
    r"backwards? compatib",
    r"in a real (implementation|app|application|world|scenario)",
    r"console\.log"
]

# Quality criteria by agent type
QUALITY_GATES = {
    "backend-database-engineer": {
        "required_patterns": [r"migration|schema|query|database|server|action|api|endpoint|route"],
        "forbidden_patterns": [],  # Uses universal only
        "min_lines": 5
    },
    "frontend-ui-specialist": {
        "required_patterns": [r"component|jsx?|tsx?|css"],
        "forbidden_patterns": [r"alert\("],  # Additional to universal
        "min_lines": 10
    },
    "code-quality-reviewer": {
        "required_patterns": [r"test|spec|coverage|lint"],
        "forbidden_patterns": [r"skipped|disabled|ignored"],  # Additional to universal
        "min_lines": 3
    },
    "feature-architect-planner": {
        "required_patterns": [r"## |### |\* "],  # Structured output
        "forbidden_patterns": [r"I think|Maybe|Perhaps"],  # Additional to universal
        "min_lines": 20
    }
}

def validate_agent_result(agent_name, result_text):
    """Validate agent output against quality criteria"""
    if not result_text or len(result_text.strip()) < 10:
        return False, "Output too short or empty"
    
    criteria = QUALITY_GATES.get(agent_name)
    if not criteria:
        return True, "No specific criteria defined"
    
    # Check minimum length
    lines = result_text.split('\n')
    if len(lines) < criteria.get('min_lines', 1):
        return False, f"Output too short: {len(lines)} lines, need {criteria['min_lines']}"
    
    # Check required patterns
    required = criteria.get('required_patterns', [])
    for pattern in required:
        if not re.search(pattern, result_text, re.IGNORECASE):
            return False, f"Missing required content pattern: {pattern}"
    
    # Check forbidden patterns (universal + agent-specific)
    forbidden = UNIVERSAL_FORBIDDEN + criteria.get('forbidden_patterns', [])
    for pattern in forbidden:
        if re.search(pattern, result_text, re.IGNORECASE):
            return False, f"Contains forbidden pattern: {pattern}"
    
    return True, "Quality gates passed"

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    if tool_name == "Task":
        tool_input = data.get("tool_input", {})
        tool_result = data.get("tool_result", "")
        agent_name = tool_input.get("subagent_type", "unknown")
        
        print(f"🔍 Validating {agent_name} result...", file=sys.stderr)
        
        is_valid, message = validate_agent_result(agent_name, str(tool_result))
        
        if is_valid:
            print(f"✅ {message}", file=sys.stderr)
        else:
            print(f"⚠️ Quality gate failed: {message}", file=sys.stderr)
            print(f"Consider refining the task prompt or agent instructions", file=sys.stderr)

except Exception as e:
    print(f"Validation error: {e}", file=sys.stderr)
    sys.exit(0)  # Never block workflow
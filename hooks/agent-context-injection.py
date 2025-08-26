#!/usr/bin/env python3
"""Simple universal context injection for any project type"""
import json
import sys
import os
import subprocess

# Agent-specific focus areas - what they care about
AGENT_FOCUS = {
    "backend-database-engineer": "database, server logic, APIs",
    "frontend-ui-specialist": "UI components, styling, client-side",
    "code-quality-reviewer": "testing, linting, quality gates",
    "feature-architect-planner": "architecture, planning, requirements",
    "documentation-specialist": "documentation, guides, patterns"
}

# Universal instruction for all agents to check available docs
UNIVERSAL_READING_INSTRUCTION = "**💡 TIP:** Check ai-docs/ for established patterns and requirements before implementing."

def get_project_structure():
    """Get directory structure - try tree, fallback gracefully"""
    try:
        # Try tree if available
        result = subprocess.run(["tree", "-d", "-L", "2", "-I", "node_modules|.git|dist|build|target"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return f"**Directory Structure:**\n```\n{result.stdout}\n```"
    except:
        pass
    
    # Simple fallback - just list top-level directories
    try:
        dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
        dirs.sort()
        return f"**Top-level directories:** {', '.join(dirs)}"
    except:
        return "**Project Structure:** Unable to determine"

def get_git_context():
    """Get basic git info if available"""
    try:
        branch = subprocess.run(["git", "branch", "--show-current"], 
                              capture_output=True, text=True, timeout=3)
        if branch.returncode == 0:
            return f"**Current branch:** {branch.stdout.strip()}"
    except:
        pass
    return ""

def get_ai_docs():
    """List available documentation in ai-docs directory"""
    if not os.path.exists("ai-docs"):
        return ""
    
    try:
        docs = []
        for root, dirs, files in os.walk("ai-docs"):
            # Skip hidden directories and limit depth
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            level = root.count(os.sep) - 1  # ai-docs is level 0
            if level > 2:  # Limit depth
                continue
                
            for file in files:
                if file.endswith('.md') and not file.startswith('.'):
                    # Get relative path from ai-docs
                    rel_path = os.path.relpath(os.path.join(root, file), "ai-docs")
                    docs.append(rel_path)
        
        if docs:
            docs.sort()
            return f"**Available Documentation (ai-docs/):**\n{chr(10).join([f'- {doc}' for doc in docs])}"
    except:
        pass
    
    return ""

def get_reading_instruction():
    """Simple universal instruction to check docs"""
    return UNIVERSAL_READING_INSTRUCTION

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    if tool_name == "Task":
        tool_input = data.get("tool_input", {})
        agent_name = tool_input.get("subagent_type", "unknown")
        
        focus = AGENT_FOCUS.get(agent_name, "general development")
        print(f"🧠 Injecting context for {agent_name}...", file=sys.stderr)
        
        context_parts = []
        
        # Basic project structure
        structure = get_project_structure()
        if structure:
            context_parts.append(structure)
        
        # Git context if available
        git_info = get_git_context()
        if git_info:
            context_parts.append(git_info)
        
        # Available documentation
        ai_docs = get_ai_docs()
        if ai_docs:
            context_parts.append(ai_docs)
            # Add universal reading instruction if docs exist
            context_parts.append(get_reading_instruction())
        
        if context_parts:
            context = f"""## 🎯 {agent_name.replace('-', ' ').title()} Context

**Focus:** {focus}

{chr(10).join(context_parts)}

---
*Project context auto-injected. Follow reading instructions for consistent implementation.*
"""
            print(context)
        
        print(f"✅ Basic context injected for {agent_name}", file=sys.stderr)

except Exception as e:
    print(f"Context injection error: {e}", file=sys.stderr)
    sys.exit(0)  # Never block agent execution
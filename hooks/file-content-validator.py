#!/usr/bin/env python3
"""Validate file content after agents modify code"""
import json
import sys
import re
import os

# Universal forbidden patterns in code files
FILE_FORBIDDEN = [
    r"TODO:",
    r"FIXME:",
    r"console\.log\(.*\);?\s*$",  # Standalone console.log lines
    r"alert\(",
    r"debugger;?",
    r"backwards?\s+compatib",  # "backward compatible" or "backwards compatible"  
    r"compatib.*layer",  # "compatibility layer"
    r"for\s+compatib",  # "for compatibility"
    r"legacy\s+support",
    r"//.*compatib",  # Comments about compatibility
    r"/\*.*compatib.*\*/"  # Block comments about compatibility
]

def validate_file_content(file_path, content):
    """Check file content for forbidden patterns"""
    if not content:
        return True, "Empty file"
    
    violations = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and pure whitespace
        if not line.strip():
            continue
            
        for pattern in FILE_FORBIDDEN:
            if re.search(pattern, line, re.IGNORECASE):
                # Extract the matching part for clearer error
                match = re.search(pattern, line, re.IGNORECASE)
                matched_text = match.group(0) if match else pattern
                violations.append(f"Line {line_num}: '{matched_text.strip()}'")
    
    if violations:
        return False, f"Code quality violations:\n" + "\n".join(violations)
    
    return True, "File content validated"

def should_validate_file(file_path):
    """Check if file should be validated based on extension"""
    code_extensions = {
        '.js', '.jsx', '.ts', '.tsx', '.py', '.go', '.rs', '.java', 
        '.c', '.cpp', '.h', '.hpp', '.php', '.rb', '.swift', '.kt'
    }
    
    _, ext = os.path.splitext(file_path.lower())
    return ext in code_extensions

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    # Only validate file modification tools
    if tool_name in ["Edit", "Write", "MultiEdit"]:
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        
        if not should_validate_file(file_path):
            # Skip non-code files
            sys.exit(0)
        
        print(f"🔍 Validating code quality in {os.path.basename(file_path)}...", file=sys.stderr)
        
        # Try to read the file content (post-modification)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            is_valid, message = validate_file_content(file_path, content)
            
            if is_valid:
                print(f"✅ Code quality check passed", file=sys.stderr)
            else:
                print(f"⚠️ Code quality issues found:", file=sys.stderr)
                print(f"{message}", file=sys.stderr)
                print(f"Consider removing compatibility bloat and debugging remnants", file=sys.stderr)
                
        except FileNotFoundError:
            # File might not exist yet (Write tool creating new file)
            pass
        except Exception as e:
            print(f"File validation error: {e}", file=sys.stderr)

except Exception as e:
    print(f"File validator error: {e}", file=sys.stderr)
    sys.exit(0)  # Never block workflow
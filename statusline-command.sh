#!/bin/bash

# Enhanced statusline for parallel orchestration with tmux + git worktrees
# Provides context for multi-session development workflow

# Make sure script is executable
chmod +x "$0" 2>/dev/null

# Read JSON input from stdin
input=$(cat)

# Extract values from JSON
model_name=$(echo "$input" | jq -r '.model.display_name')
current_dir=$(echo "$input" | jq -r '.workspace.current_dir')
project_dir=$(echo "$input" | jq -r '.workspace.project_dir')

# Get current directory name for display
dir_name=$(basename "$current_dir")

# Enhanced Git & Worktree Detection
cd "$current_dir" 2>/dev/null || cd "$project_dir" 2>/dev/null
git_info=""
worktree_info=""

if git rev-parse --git-dir >/dev/null 2>&1; then
    # Get current branch
    branch=$(git branch --show-current 2>/dev/null)
    if [ -z "$branch" ]; then
        # Fallback for detached HEAD
        branch="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
    fi
    
    # Detect if we're in a git worktree
    git_dir=$(git rev-parse --git-dir)
    if [[ "$git_dir" == *"/.git/worktrees/"* ]]; then
        # Extract worktree name from git dir path
        worktree_name=$(basename "$(dirname "$git_dir")" | sed 's/^.*worktrees\///')
        worktree_info="(wt:$worktree_name)"
    fi
    
    # Count total worktrees (if in a repo with worktrees)
    worktree_count=""
    if command -v git worktree >/dev/null 2>&1; then
        total_worktrees=$(git worktree list 2>/dev/null | wc -l)
        if [ "$total_worktrees" -gt 1 ]; then
            worktree_count="🔀 $total_worktrees"
        fi
    fi
    
    # Get uncommitted changes count (lines modified)
    changes=""
    if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
        # Count modified lines (additions + deletions)
        unstaged=$(git diff --numstat 2>/dev/null | awk '{sum += $1 + $2} END {print sum+0}')
        staged=$(git diff --cached --numstat 2>/dev/null | awk '{sum += $1 + $2} END {print sum+0}')
        total_changes=$((unstaged + staged))
        
        if [ "$total_changes" -gt 0 ]; then
            changes=" +$total_changes"
        fi
    fi
    
    git_info="🌿 $branch$changes $worktree_info"
fi

# No tmux pane info needed - user manages panes manually

# Output Style Detection (if user is in specific mode)
output_style=""
if [ -f ".claude/settings.local.json" ]; then
    style=$(jq -r '.outputStyle // empty' .claude/settings.local.json 2>/dev/null)
    if [ -n "$style" ] && [ "$style" != "null" ]; then
        case "$style" in
            *"research"*) output_style="🔍 Research" ;;
            *"planning"*) output_style="📋 Planning" ;;
            *"execution"*) output_style="⚡ Execution" ;;
            *) output_style="🎯 $(echo "$style" | sed 's/.*\///;s/\.md$//' | tr '-' ' ' | sed 's/\b\w/\u&/g')" ;;
        esac
    fi
fi

# Build status line components in optimal order for parallel orchestration
status_parts=()

# Core model info
if [ -n "$model_name" ]; then
    status_parts+=("🤖 $model_name")
fi

# Output style (if active) - helpful for workflow context
if [ -n "$output_style" ]; then
    status_parts+=("$output_style")
fi

# Directory info
if [ -n "$dir_name" ]; then
    status_parts+=("📁 $dir_name")
fi

# Enhanced git info (branch + worktree + changes)
if [ -n "$git_info" ]; then
    status_parts+=("$git_info")
fi

# Worktree count (critical for parallel development)
if [ -n "$worktree_count" ]; then
    status_parts+=("$worktree_count")
fi

# Join parts with separator
IFS=" • "
status_line="${status_parts[*]}"

# Output with proper formatting
printf "%s" "$status_line"
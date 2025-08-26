#!/usr/bin/env python3
"""Monitor agent performance and suggest optimizations"""
import json
import sys
import os
import time
from datetime import datetime, timedelta

METRICS_FILE = os.path.expanduser("~/.claude/agent-metrics.json")

def load_metrics():
    """Load existing agent performance metrics"""
    try:
        if os.path.exists(METRICS_FILE):
            with open(METRICS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {
        "agents": {},
        "daily_stats": {},
        "last_cleanup": datetime.now().isoformat()
    }

def save_metrics(metrics):
    """Save updated metrics"""
    try:
        os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
        with open(METRICS_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)
    except Exception as e:
        print(f"Failed to save metrics: {e}", file=sys.stderr)

def record_agent_invocation(agent_name, task_description):
    """Record agent usage and performance"""
    metrics = load_metrics()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize agent stats
    if agent_name not in metrics["agents"]:
        metrics["agents"][agent_name] = {
            "total_calls": 0,
            "recent_calls": [],
            "avg_complexity": 0
        }
    
    # Initialize daily stats
    if today not in metrics["daily_stats"]:
        metrics["daily_stats"][today] = {
            "total_calls": 0,
            "agents_used": set(),
            "parallel_sessions": 0
        }
    
    # Record invocation
    agent_stats = metrics["agents"][agent_name]
    agent_stats["total_calls"] += 1
    agent_stats["recent_calls"].append({
        "timestamp": datetime.now().isoformat(),
        "task": task_description[:100],  # Truncate long descriptions
        "complexity": estimate_task_complexity(task_description)
    })
    
    # Keep only recent calls (last 24 hours)
    cutoff = datetime.now() - timedelta(hours=24)
    agent_stats["recent_calls"] = [
        call for call in agent_stats["recent_calls"] 
        if datetime.fromisoformat(call["timestamp"]) > cutoff
    ]
    
    # Update daily stats
    daily = metrics["daily_stats"][today]
    daily["total_calls"] += 1
    daily["agents_used"] = list(set(daily.get("agents_used", []) + [agent_name]))
    
    # Calculate average complexity
    if agent_stats["recent_calls"]:
        complexities = [call["complexity"] for call in agent_stats["recent_calls"]]
        agent_stats["avg_complexity"] = sum(complexities) / len(complexities)
    
    save_metrics(metrics)
    return metrics

def estimate_task_complexity(task_description):
    """Estimate task complexity from description"""
    complexity_keywords = {
        "implement": 3, "create": 3, "build": 4, "design": 4,
        "refactor": 3, "migrate": 4, "integrate": 4,
        "fix": 2, "update": 2, "modify": 2,
        "analyze": 2, "review": 2, "document": 2,
        "test": 2, "debug": 3, "optimize": 3
    }
    
    words = task_description.lower().split()
    base_complexity = 1
    
    for word in words:
        if word in complexity_keywords:
            base_complexity = max(base_complexity, complexity_keywords[word])
    
    # Adjust for task length
    if len(task_description) > 200:
        base_complexity += 1
    
    return min(base_complexity, 5)  # Cap at 5

def suggest_optimizations(metrics, agent_name):
    """Suggest optimizations based on usage patterns"""
    suggestions = []
    agent_stats = metrics["agents"].get(agent_name, {})
    
    # High frequency suggestions
    if agent_stats.get("total_calls", 0) > 10:
        if agent_stats.get("avg_complexity", 0) < 2:
            suggestions.append("Consider combining simple tasks to reduce overhead")
    
    # Pattern analysis
    recent_calls = agent_stats.get("recent_calls", [])
    if len(recent_calls) > 5:
        # Check for repeated similar tasks
        recent_tasks = [call["task"] for call in recent_calls[-5:]]
        if len(set(recent_tasks)) < 3:
            suggestions.append("Detected repetitive tasks - consider batch processing")
    
    return suggestions

# Main execution
try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    if tool_name == "Task":
        tool_input = data.get("tool_input", {})
        agent_name = tool_input.get("subagent_type", "unknown")
        task_description = tool_input.get("prompt", "")
        
        print(f"📊 Recording {agent_name} invocation...", file=sys.stderr)
        
        metrics = record_agent_invocation(agent_name, task_description)
        suggestions = suggest_optimizations(metrics, agent_name)
        
        agent_stats = metrics["agents"][agent_name]
        print(f"Agent calls: {agent_stats['total_calls']} (avg complexity: {agent_stats['avg_complexity']:.1f})", file=sys.stderr)
        
        for suggestion in suggestions:
            print(f"💡 {suggestion}", file=sys.stderr)

except Exception as e:
    print(f"Monitoring error: {e}", file=sys.stderr)
    sys.exit(0)  # Never block workflow
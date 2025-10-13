# data/db.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load from .env file
load_dotenv()



# read once at import time
_SUPABASE_URL = os.getenv("SUPABASE_URL")
_SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not _SUPABASE_URL or not _SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")

supa: Client = create_client(_SUPABASE_URL, _SUPABASE_KEY)
# ---- simple CRUD helpers ----
def insert(table: str, row: dict | list[dict]):
    resp = supa.table(table).insert(row).execute()
    data = resp.data
    if not data:
        raise RuntimeError("insert returned no data")
    first = data[0] if isinstance(data, list) else data
    try:
        return first["id"]
    except (TypeError, KeyError):
        raise RuntimeError("insert result missing 'id'")

def upsert(table: str, row: dict | list[dict], on_conflict: str | None = None):
    """Insert or update. For tables with unique constraints like weekly_schedules."""
    kwargs = {}
    if on_conflict:
        kwargs['on_conflict'] = on_conflict
    
    resp = supa.table(table).upsert(row, **kwargs).execute()
    data = resp.data
    if not data:
        raise RuntimeError("upsert returned no data")
    first = data[0] if isinstance(data, list) else data
    try:
        return first["id"]
    except (TypeError, KeyError):
        raise RuntimeError("upsert result missing 'id'")


def select(table: str, filters: dict | None = None) -> list[dict]:
    """Return list of dicts."""
    q = supa.table(table).select("*")
    if filters:
        for k, v in filters.items():
            q = q.eq(k, v)
    return q.execute().data

def update(table: str, filters: dict, values: dict) -> list[dict]:
    """Return updated rows."""
    q = supa.table(table).update(values)
    for k, v in filters.items():
        q = q.eq(k, v)
    return q.execute().data

def delete(table: str, filters: dict) -> list[dict]:
    """Return deleted rows."""
    q = supa.table(table).delete()
    for k, v in filters.items():
        q = q.eq(k, v)
    return q.execute().data



# data/db.py (add these optimized functions)

from datetime import datetime
from collections import defaultdict

# Day order for comparison
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_active_tasks(user_id: str) -> list[dict]:
    """
    Get all active tasks for a user and handle missed tasks.
    Optimized with batch operations - minimal DB queries.
    
    Args:
        user_id: The user ID to get active tasks for
        
    Returns:
        List of active tasks with 'today' flag set
    """
    # Get current day info
    current_day = datetime.now().strftime("%A")  # "Monday", "Tuesday", etc.
    current_day_index = DAYS.index(current_day)
    
    # Single query: Get all active tasks for user
    active_tasks = select("tasks", filters={"user_id": user_id, "status": "active"})
    
    if not active_tasks:
        return []
    
    # Separate tasks: find which ones are missed
    tasks_to_mark_missed = []
    milestones_needing_promotion = set()
    
    for task in active_tasks:
        if task.get("day"):
            try:
                task_day_index = DAYS.index(task["day"])
                
                # Check if missed (current day is past task day)
                if current_day_index > task_day_index:
                    tasks_to_mark_missed.append(task["id"])
                    milestones_needing_promotion.add(task["milestone_id"])
            except ValueError:
                # Invalid day name, skip
                continue
    
    # Batch operations if there are missed tasks
    if tasks_to_mark_missed:
        # Batch update: Mark all missed tasks at once
        for task_id in tasks_to_mark_missed:
            update(
                "tasks",
                filters={"id": task_id},
                values={"status": "missed", "updated_at": datetime.now().isoformat()}
            )
        
        # Batch query: Get next pending tasks for all affected milestones
        all_next_tasks = []
        for milestone_id in milestones_needing_promotion:
            pending = select("tasks", filters={"milestone_id": milestone_id, "status": "pending"})
            if pending:
                all_next_tasks.extend(pending)
        
        # Group by milestone and get first (lowest rank) for each
        milestone_next_task = {}
        for task in sorted(all_next_tasks, key=lambda t: t.get("rank", 999)):
            mid = task["milestone_id"]
            if mid not in milestone_next_task:
                milestone_next_task[mid] = task
        
        # Batch update: Activate all next tasks at once
        for next_task in milestone_next_task.values():
            update(
                "tasks",
                filters={"id": next_task["id"]},
                values={"status": "active", "updated_at": datetime.now().isoformat()}
            )
        
        # Re-query active tasks after updates
        active_tasks = select("tasks", filters={"user_id": user_id, "status": "active"})
    
    # Add 'today' flag to all active tasks
    for task in active_tasks:
        task["today"] = (task.get("day") == current_day)
    
    return active_tasks


def complete_task(task_id: str) -> dict | None:
    """
    Complete a task and activate the next one.
    Optimized with minimal queries.
    
    Args:
        task_id: The ID of the task to complete
        
    Returns:
        The newly activated task, or None if milestone completed
    """
    # Get task info (single query with filter)
    tasks = select("tasks", filters={"id": task_id})
    
    if not tasks:
        raise ValueError(f"Task {task_id} not found")
    
    task = tasks[0]
    milestone_id = task["milestone_id"]
    
    # Mark as completed
    update(
        "tasks",
        filters={"id": task_id},
        values={"status": "completed", "updated_at": datetime.now().isoformat()}
    )
    
    # Get next pending task (single query)
    next_tasks = select("tasks", filters={"milestone_id": milestone_id, "status": "pending"})
    
    if not next_tasks:
        return None  # Milestone completed
    
    # Sort by rank and get first
    next_tasks.sort(key=lambda t: t.get("rank", 999))
    next_task = next_tasks[0]
    
    # Activate it
    update(
        "tasks",
        filters={"id": next_task["id"]},
        values={"status": "active", "updated_at": datetime.now().isoformat()}
    )
    
    return next_task


# ===== BONUS: Bulk operations for better performance =====

def get_active_tasks_summary(user_id: str) -> dict:
    """
    Get a summary of active tasks grouped by milestone.
    Useful for dashboard views.
    
    Returns:
        {
            'total_active': int,
            'due_today': int,
            'overdue': int,
            'tasks_by_milestone': {milestone_id: task, ...}
        }
    """
    tasks = get_active_tasks(user_id)
    
    summary = {
        'total_active': len(tasks),
        'due_today': sum(1 for t in tasks if t.get('today')),
        'overdue': 0,  # Could add logic to check if day is past
        'tasks_by_milestone': {t['milestone_id']: t for t in tasks}
    }
    
    return summary
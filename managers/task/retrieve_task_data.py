# data/tasks.py

from datetime import datetime

from managers.db import select, update

# Day order for comparison
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_active_tasks(user_id: str) -> list[dict]:
    """
    Get ALL active tasks for user across all milestones.
    Handles missed task detection and automatic promotion.
    Returns all active tasks (not filtered by day).
    """
    current_day = datetime.now().strftime("%A")
    current_day_index = DAYS.index(current_day)
    
    # Get all active tasks for user
    active_tasks = select("tasks", filters={"user_id": user_id, "status": "active"})
    
    if not active_tasks:
        return []
    
    # Find missed tasks
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
                continue
    
    # Batch operations if there are missed tasks
    if tasks_to_mark_missed:
        # Mark all missed tasks
        for task_id in tasks_to_mark_missed:
            update(
                "tasks",
                filters={"id": task_id},
                values={"status": "missed", "updated_at": datetime.now().isoformat()}
            )
        
        # Get next pending tasks for affected milestones
        milestone_next_task = {}
        for milestone_id in milestones_needing_promotion:
            pending = select("tasks", filters={"milestone_id": milestone_id, "status": "pending"})
            if pending:
                # Sort by rank and get first
                pending.sort(key=lambda t: t.get("rank", 999))
                milestone_next_task[milestone_id] = pending[0]
        
        # Activate all next tasks
        for next_task in milestone_next_task.values():
            update(
                "tasks",
                filters={"id": next_task["id"]},
                values={"status": "active", "updated_at": datetime.now().isoformat()}
            )
        
        # Re-query active tasks after updates
        active_tasks = select("tasks", filters={"user_id": user_id, "status": "active"})
    
    return active_tasks


def get_today_tasks(user_id: str) -> list[dict]:
    """
    Get ONLY tasks scheduled for today.
    Returns tasks where day matches current day.
    """
    current_day = datetime.now().strftime("%A")
    
    # Get all active tasks (handles missed automatically)
    all_active = get_active_tasks(user_id)
    
    # Filter for today only
    today_tasks = [t for t in all_active if t.get("day") == current_day]
    
    return today_tasks


def complete_task(task_id: str) -> dict | None:
    """
    Complete a task and activate the next one.
    Returns the newly activated task, or None if milestone completed.
    """
    # Get task info
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
    
    # Get next pending task
    next_tasks = select("tasks", filters={"milestone_id": milestone_id, "status": "pending"})
    
    if not next_tasks:
        return None
    
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
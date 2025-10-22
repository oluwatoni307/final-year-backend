from .model import TaskDecompositionOutput
from ..db import insert, select

TASKS_TABLE = "tasks"

def tasks_week_total(task_output: TaskDecompositionOutput):   
    week_totals = {}
    for task in task_output.tasks:
        week = task.week_number
        if week not in week_totals:
            week_totals[week] = 0
        week_totals[week] += 1
        
    return week_totals
def save_tasks_for_milestone(task_output: TaskDecompositionOutput, milestone_id: str):
    """
    Saves all tasks for a given milestone to the tasks table.
    Maps TaskSpecification fields to the database schema.
    Returns list of saved task records with their IDs.
    """
  
    if not task_output.tasks:
        return []
    
    saved_tasks = []
    week_total = tasks_week_total(task_output)

    
    for idx, task_spec in enumerate(task_output.tasks):
        # Build description with all task metadata
        detailed_description = f"""
**Objective:** {task_spec.objective}

**Task Type:** {task_spec.task_type}
**Cognitive Load:** {task_spec.cognitive_load}
**Time Allocated:** {task_spec.time_allocated}

**Specific Actions:**
{chr(10).join(f"- {action}" for action in task_spec.specific_actions)}

**Success Metric:** {task_spec.success_metric}
        """.strip()

        row = {
            "milestone_id": milestone_id,
            "name": task_spec.title,
            "description": detailed_description,
            "rank": idx,
            "status": "active"if idx == 0 else "pending",
            "day": task_spec.day,
          "allocated_minutes": task_spec.time_allocated,
            "week_details":{"week_number": task_spec.week_number,"missed":0,"completed":0,"total":week_total.get(task_spec.week_number,0)},
        }
        
        inserted_task = insert(TASKS_TABLE, row)
        saved_tasks.append(inserted_task)
    
    return saved_tasks


def get_milestone_tasks(milestone_id: str, status: str|None = None):
    """
    Retrieves all tasks for a milestone, optionally filtered by status.
    Returns tasks ordered by rank.
    """
    filters = {'milestone_id': milestone_id}
    
    if status:
        filters['status'] = status
    
    tasks = select(
        TASKS_TABLE,
        filters=filters
    )
    
    # Sort by rank if multiple tasks returned
    if tasks and isinstance(tasks, list):
        tasks.sort(key=lambda t: t.get('rank', 0))
    
    return tasks


def update_task_status(task_id: str, status: str, completion_description: str|None = None):
    """
    Updates task status and optionally adds completion description.
    Status must be: 'pending', 'active', or 'completed'
    """
    from ..db import update
    
    if status not in ['pending', 'active', 'completed']:
        raise ValueError(f"Invalid status: {status}. Must be pending, active, or completed.")
    
    update_data = {
        "status": status,
        "updated_at": "now()"  # PostgreSQL function
    }
    
    if completion_description:
        update_data["completion_description"] = completion_description
    
    updated = update(TASKS_TABLE, {"task_id":task_id}, update_data)
    return updated


# def schedule_task(task_id: str, timeslot_start: str, timeslot_end: str, week_number: int|None = None):
#     """
#     Schedules a task by setting its timeslot and optional week number.
    
#     Args:
#         task_id: UUID of the task
#         timeslot_start: ISO format timestamp with timezone
#         timeslot_end: ISO format timestamp with timezone
#         week_number: Optional week number for organization
#     """
#     from ..db import update
    
#     update_data = {
#         "timeslot_start": timeslot_start,
#         "timeslot_end": timeslot_end,
#         "updated_at": "now()"
#     }
    
#     if week_number is not None:
#         update_data["week_number"] = week_number
    
#     updated = update(TASKS_TABLE, task_id, update_data)
#     return updated


# def mark_task_for_today(task_id: str, is_today: bool = True):
#     """
#     Marks or unmarks a task for today's focus.
#     """
#     from ..db import update
    
#     updated = update(TASKS_TABLE, task_id, {
#         "today": is_today,
#         "updated_at": "now()"
#     })
#     return updated


# def get_today_tasks(milestone_id: str = None):
#     """
#     Retrieves all tasks marked for today.
#     Optionally filters by milestone_id.
#     """
#     filters = {'today': True}
    
#     if milestone_id:
#         filters['milestone_id'] = milestone_id
    
#     tasks = select(TASKS_TABLE, filters=filters)
    
#     if tasks and isinstance(tasks, list):
#         tasks.sort(key=lambda t: t.get('rank', 0))
    
#     return tasks
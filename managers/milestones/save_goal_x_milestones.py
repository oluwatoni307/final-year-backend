from .model import milestones
from managers.goal.model import GoalOutput, GoalSave
from managers.goal.save_goal import save_goal

# data/goal_repo.py
from uuid import UUID
from ..db import insert, select

TABLE = "milestones"


def save_goal_x_milestone(milestones: milestones, goal: GoalSave):
    """
    Saves goal and all milestones. Sets first milestone as active.
    Returns the active milestone from DB with its ID.
    """
    goal_id = save_goal(goal, milestones.goal_name, milestones.goal_description)
    
    if not milestones.milestones:
        return None
    
    for idx, milestone in enumerate(milestones.milestones):
        row = {
            "goal_id": goal_id,
            "objective": milestone.objective,
            "description": milestone.description,   
            "success_criteria": milestone.success_criteria,
            "target_date": milestone.targetDate.isoformat(),
            "enables": milestone.enables,
            "status": "active" if idx == 0 else "pending",
        }
        insert(TABLE, row)
    
    # Query for the active milestone we just created
    active_milestone = select(
        TABLE,
        filters={'goal_id': goal_id, 'status': 'active'},
    )
    
    return active_milestone

        
        
        
        
        
        
        
        

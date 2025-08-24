from .model import milestones
from managers.goal.model import GoalOutput
from managers.goal.save_goal import save_goal

# data/goal_repo.py
from uuid import UUID
from ..db import insert

TABLE = "milestones"


def save_goal_x_milestone(milestones: milestones, goal: GoalOutput):
    """
    Sets the first milestone.status = 'active' and others = 'pending'.
    Idempotent in the sense that it always marks the first provided milestone active.
    Returns the active milestone object (or None if no milestones provided).
    """
    # save_goal returns the created goal id (keep variable name consistent but avoid shadowing built-in)
    created_id = save_goal(goal, milestones.goal_name, milestones.goal_description)
    goal_id = created_id

    active_milestone = None



    for idx, milestone in enumerate(milestones.milestones):
        status = "active" if idx == 0 else "pending"
        # capture the first milestone as the active one
        if idx == 0:
            active_milestone = milestone

        row = {
            "goal_id": goal_id,
            "objective": milestone.objective,
            "success_criteria": milestone.success_criteria,
            "targetDate": milestone.targetDate,
            "enables": milestone.enables,
            "status": status,
        }
        # Insert each milestone into the database
        insert(TABLE, row)

    return active_milestone

        
        
        
        
        
        
        
        

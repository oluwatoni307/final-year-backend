from .model import GoalOutput, GoalSave

# data/goal_repo.py
from uuid import UUID
from ..db import insert



TABLE = "goals"
# do not forget to add the new columns to the database schema
def save_goal(goal_obj: GoalSave, goal_name, goal_description) -> dict:
    """
    goal_obj can contain any extra fields.
    We cherry-pick the columns we need and stringify the rest.
    """
    
    row = {
        "goal_name": goal_name,
        # "user_id":     goal_obj.userId,
        "goal_analysis": str(goal_obj),
        "description": goal_description,
        # "deadline":    goal_obj.date,
        "status":      "active",
    }
    return insert(TABLE, row)




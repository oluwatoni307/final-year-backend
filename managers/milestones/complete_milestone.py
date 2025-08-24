from ..db import update
from managers.milestones.model import status_state  

def complete_milestone(milestone_id, goal_id) :
    # Sets milestone.status = 'completed'.
    # Also advances the next pending milestone to 'active'.
    update(
        "milestones",
        
        {"id": milestone_id},
        {"status": status_state.completed.value}
    )
    new_milestone =update(
        "milestones",
        {"id": milestone_id+1},
        {"status": status_state.active.value},)
    
    if new_milestone == []:
        update("goals", {"id": goal_id}, {"status": status_state.completed.value})
        
    return new_milestone

    

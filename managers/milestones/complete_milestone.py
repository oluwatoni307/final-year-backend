from managers.milestones.evaluate_milestone import evaluate
from ..db import update
from managers.milestones.model import status_state  
from managers.db import supa


def complete_milestone(milestone_id) :
    # Sets milestone.status = 'completed'.
    # Also advances the next pending milestone to 'active'.
    
    # fetch completion for all tasks under this 
    res = supa.table("tasks").select("completion").eq("milestone_id", milestone_id).execute()
    completions = [t["completion"] for t in (res.data or [])]
    feedback = evaluate(completions)
    
    # Get rank and goal_id of current milestone
    rank_res = supa.table("milestones").select("rank, goal_id").eq("milestone_id", milestone_id).execute()
    current_milestone = rank_res.data[0] if rank_res.data else None
    
    if not current_milestone:
        return True, feedback  # Milestone not found
    
    current_rank = current_milestone["rank"]
    goal_id = current_milestone["goal_id"]
    
    # Complete current milestone
    update(
        "milestones",
        {"id": milestone_id},
        {"status": status_state.completed.value, "completion_details": feedback}
    )
    
    # Find and activate next milestone (same goal_id, rank+1)
    next_milestone_res = supa.table("milestones").select("*").eq("goal_id", goal_id).eq("rank", current_rank + 1).execute()
    
    if next_milestone_res.data:
        next_milestone = next_milestone_res.data[0]
        new_milestone = update(
            "milestones",
            {"id": next_milestone["id"]},
            {"status": status_state.active.value}
        )
        return new_milestone, feedback
    else:
        # No more milestones, mark goal as completed
        update("goals", {"id": goal_id}, {"status": status_state.completed.value})
        return True, feedback
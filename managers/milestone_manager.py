from managers.db import select
from managers.goal.model import GoalOutput
from managers.task_manager import TaskManager
from .milestones.model import milestones
from .milestones.create_milestone import milestone_creator
from .milestones.save_goal_x_milestones import save_goal_x_milestone
from .milestones.complete_milestone import complete_milestone

from .milestones.timeslot_master import timeMaster

class MilestoneManager:
    # 4️⃣  Triggered only after GoalManager.verify_and_save
    
    
    def create_milestones(self,goal) -> None:
        """
        Returns N milestone objects ready to be bulk-inserted into Supabase
        (status = 'pending').
        """
        # 4️⃣  Triggered only after GoalManager.verify_and_save
        gen_milestones = milestone_creator(goal)
        save_goal_x_milestone(gen_milestones, goal)
        
        return
        

    

    def complete_milestone(self, milestone_id, goal_id) -> None:
        """
        Sets milestone.status = 'completed'.
        Also advances the next pending milestone to 'active'.
        """
        new_milestone =complete_milestone(milestone_id, goal_id)
        if new_milestone != []:
            timetable =timeMaster(new_milestone, [])# type: ignore 
            TaskManager.create_tasks(new_milestone, new_milestone[0]["id"])
        
        # calls TaskManager.create_tasks
         # 5️⃣  Only the *currently active* milestone is passed to TaskManager
         
         
 
    @staticmethod   
    def return_milestone(goal_id): #type: ignore
        raw_milestones = select("milestones", {"goal_id": goal_id})
        
        # Transform database fields to match Flutter model expectations
        formatted_milestones = []
        for milestone in raw_milestones:
            formatted_milestone = {
    "id": milestone.get("id"),
    "milestone_id": milestone.get("id"),  # Flutter expects this too
    "objective": milestone.get("objective"),
    "success_criteria": milestone.get("success_criteria"),
    "rank": milestone.get("rank"),
    "target_date": milestone.get("target_date"),
    "status": milestone.get("status"),
    "completion_rate": milestone.get("completion_rate"),
    "assigned_timeslot": milestone.get("assigned_timeslot")
}

            formatted_milestones.append(formatted_milestone)
        
        return {
            "goal_id": goal_id,
            "milestones": formatted_milestones
        }
            
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
    
    
    def create_milestones(self,goal: GoalOutput) -> None:
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
            TaskManager.create_tasks(new_milestone) # pyright: ignore[reportArgumentType]
        
        # calls TaskManager.create_tasks
         # 5️⃣  Only the *currently active* milestone is passed to TaskManager
         
         
 
    @staticmethod   
    def return_milestone(goal_id) : #type: ignore
        milestones =  select("milestones", {"goal_id": goal_id})
        return milestones  
        
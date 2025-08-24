from .goal.model import goal_input, GoalOutput, Goal
from .goal.analyze_draft import goal_definer
from .milestones.save_goal_x_milestones import save_goal_x_milestone
from .milestones.create_milestone import milestone_creator
from .db import select
from .milestones.timeslot_master import timeMaster
from .task_manager import TaskManager

class GoalManager:
    # 1️⃣  Initial entry point
    @staticmethod
    def analyse_draft( goal_raw: goal_input) :
        """
        Accepts the user’s free-text goal.
        Returns a DraftGoal object containing:
          - draft_id (UUID generated here, NOT yet stored in DB)
          - analysed_description (re-phrased / enriched)
          - proposed_tags: list[str]
          - proposed_deadline: datetime | None
        """
        goal_info = goal_definer(goal_raw)
        return goal_info
      
        

    # 2️⃣  User says “Yes, this is what I meant”
    @staticmethod
    def verify_and_save( confirmed: GoalOutput):
        # goal = save_goal(confirmed)
        # return goal
      #   call on milestone_manager.create_milestones(goal)
        """
        `VerifiedGoalPayload` contains:
          - draft_id
          - final_description  (may equal analysed_description or be tweaked)
          - deadline
          - other metadata
        The function:
          - inserts a *new* goal row into Supabase
          - returns the complete Goal row (with DB-generated goal_id)
        """
        milestones = milestone_creator(confirmed)
        active_milestone =save_goal_x_milestone(milestones,confirmed)
        
        timetable =timeMaster(active_milestone, [])# type: ignore 
        TaskManager.create_tasks(active_milestone) # pyright: ignore[reportArgumentType]
        
        # save_goal(confirmed, goal_name="test",goal_description="test")
        return
        
    @staticmethod      
    def getGoals():
          goals =  select("goals")
          return goals

    # 3️⃣  User edits → treat as brand-new
    #     No special function needed; caller simply calls `analyse_draft` again
    #     with the new text (creates a new draft_id).
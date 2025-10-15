from managers.milestones.model import WeeklySchedule
from .goal.model import GoalSave, goal_input, GoalOutput, Goal
from .goal.analyze_draft import goal_definer
from .milestones.save_goal_x_milestones import save_goal_x_milestone
from .milestones.create_milestone import milestone_creator
from .db import select, update, upsert
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
    def verify_and_save(confirmed: GoalSave):
      """
      1. Check if user has existing weekly schedule
      2. If yes, pull it; if no, use empty WeeklySchedule
      3. Create milestones and schedule time
      """
      # Get or create empty schedule
      existing_schedule = GoalManager.get_user_schedule("test")
      
      # Create milestones
      milestones = milestone_creator(confirmed)
      active_milestone = save_goal_x_milestone(milestones, confirmed)
      
      if active_milestone is not None:
          # Pass existing schedule (or empty one) to timeMaster
          timetable = timeMaster(active_milestone, existing_schedule)
          
          # Save the updated schedule back
          GoalManager.save_user_schedule("test", timetable.updated_schedule)
        #   update(
        #       "milestones",
        #       {"id": active_milestone[0]["id"]},
        #       {"assigned_timeslot": timetable.updated_schedule.model_dump()}
        #     )
          # Create
          
          TaskManager.create_tasks(active_milestone, active_milestone[0]["id"])
      
      return
    
    @staticmethod
    def get_user_schedule(user_id: str) -> WeeklySchedule:
        """Get user's schedule or return empty if none exists"""
        try:
            result = select(
                'weekly_schedules',
                filters={'user_id': user_id},
            )
            
            return WeeklySchedule(**result[0]['schedule_data'])
        
        except Exception:
            # No schedule exists, return empty
            return WeeklySchedule(
                monday=[],
                tuesday=[],
                wednesday=[],
                thursday=[],
                friday=[],
                saturday=[],
                sunday=[]
            )

    @staticmethod
    def save_user_schedule(user_id: str, schedule: WeeklySchedule):
        """Save/update user's weekly schedule"""
        upsert('weekly_schedules', {
            'user_id': user_id,
            'schedule_data': schedule.model_dump()
        })


    @staticmethod
    def getGoals():
        goals =select("goals", filters={"user_id": "test123"})
        return goals
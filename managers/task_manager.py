from uuid import UUID

from managers.task.retrieve_task_data import get_today_tasks
from managers.task.save_task import save_tasks_for_milestone
from managers.task.complete_task import task_grader
from models import HabitOut, HomeDataOut, InsightOut, ProgressOut
from managers.db import DAYS, get_active_tasks, select, update

from .milestones.model import milestone
from .task.model import Task, TaskSpecification
from .task.create_task import task_creator

def generate_insight(daily_completed_tasks, daily_total, weekly_completed_tasks, weekly_total):
    raise NotImplementedError


class TaskManager:
    # 6️⃣  Called immediately after MilestoneManager.mark_active
    @staticmethod
    def create_tasks( active_milestone, context,milestone_id: str):
        """
        Returns task objects ready for insert (status = 'pending').
        """
        task_creator_response = task_creator(active_milestone, context)
        save_tasks_for_milestone(task_creator_response, milestone_id)
        return

    @staticmethod
    def get_task_completion_data(task_id: str): # type: ignore
        """Get task completion data for the completion form"""
        result = select("tasks", {"id": task_id})
        if not result:
            return {}
        
        task = result[0]
        return {
            "id": task["id"],
            "name": task.get("name") or task["description"],
            "description": task["description"],
            "completion_description": task.get("completion_description") or "",
            "status": task["status"]
        }



    
    @staticmethod
    def complete_task(task_id, task):
        # """Set task.status = 'completed'."""
        from managers.milestone_manager import MilestoneManager

        response, remaining_task, milestone_id =task_grader(task_id, task)
        if remaining_task == 0:
            print("🎉 Milestone completed!")
            # Do something special, like update milestone status
            MilestoneManager.complete_milestone(milestone_id)
       
        return response
    
    
    
    
    
    @staticmethod
    def return_task_list(milestone_id: str): # type: ignore
        tasklist = select("tasks", {"milestone_id": milestone_id})
        return tasklist
    
    

    def generate_insight(daily_completed_tasks, daily_total, weekly_completed_tasks, weekly_total): # type: ignore
        raise NotImplementedError
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] 
    
    @staticmethod
    def get_home_data(user_id: str) -> dict:
        """
        Build complete home page data structure.
        Weekly progress based on rank + day combination.
        Week = contiguous tasks by rank where days don't go backwards.
        """
        
        # Get today's and all active tasks
        today_tasks = get_today_tasks(user_id)
        all_active_tasks = get_active_tasks(user_id)
        
        # Handle empty state
        if not all_active_tasks:
            return {
                "todayHabits": [],
                "progress": {
                    "dailyDone": 0,
                    "dailyTotal": 0,
                    "weeklyDone": 0,
                    "weeklyTotal": 0
                },
                "insight": {
                    "text": "No active tasks. Time to plan your next steps! 🎯"
                }
            }
        
        # Build today's habits
        today_habits = []
        for task in today_tasks:
            habit = {
                "id": task["id"],
                "name": task.get("name") or task["description"],
                "minutes": task.get("allocated_minutes", "N/A"),
                "isCompleted": (task["status"] == "completed")
            }
            today_habits.append(habit)
        
        # Collect weekly tasks for each active milestone
        all_weekly_tasks = []
        
        for active_task in all_active_tasks:
            milestone_id = active_task["milestone_id"]
            
            # Get all tasks for this milestone, sorted by rank
            milestone_tasks = select("tasks", filters={"milestone_id": milestone_id})
            milestone_tasks.sort(key=lambda t: t.get("rank", 999))
            
            # Find active task position
            active_index = next(
                (i for i, t in enumerate(milestone_tasks) if t["id"] == active_task["id"]),
                None
            )
            
            if active_index is None:
                continue
            
            active_rank = active_task["rank"]
            
            # === FIND WEEK START: Walk backwards until week boundary ===
            week_start_rank = active_rank
            
            for i in range(active_index - 1, -1, -1):
                curr_task = milestone_tasks[i]
                next_task = milestone_tasks[i + 1]
                
                # Stop if no day assigned
                if not curr_task.get("day") or not next_task.get("day"):
                    break
                
                try:
                    curr_day_index = DAYS.index(curr_task["day"])
                    next_day_index = DAYS.index(next_task["day"])
                    
                    # Week boundary: day goes backwards (e.g., Friday -> Monday)
                    if curr_day_index > next_day_index:
                        break
                    
                    week_start_rank = curr_task["rank"]
                except ValueError:
                    break
            
            # === FIND WEEK END: Walk forwards until week boundary ===
            week_end_rank = active_rank
            
            for i in range(active_index + 1, len(milestone_tasks)):
                prev_task = milestone_tasks[i - 1]
                curr_task = milestone_tasks[i]
                
                # Stop if no day assigned
                if not curr_task.get("day") or not prev_task.get("day"):
                    break
                
                try:
                    prev_day_index = DAYS.index(prev_task["day"])
                    curr_day_index = DAYS.index(curr_task["day"])
                    
                    # Week boundary: day goes backwards (e.g., Sunday -> Monday)
                    if curr_day_index < prev_day_index:
                        break
                    
                    week_end_rank = curr_task["rank"]
                except ValueError:
                    break
            
            # === GET TASKS IN WEEK RANGE ===
            week_tasks = [
                t for t in milestone_tasks 
                if t["rank"] >= week_start_rank and t["rank"] <= week_end_rank
            ]
            
            all_weekly_tasks.extend(week_tasks)
        
        # === CALCULATE PROGRESS ===
        daily_completed = len([t for t in today_tasks if t["status"] == "completed"])
        daily_total = len(today_tasks)
        
        weekly_completed = len([t for t in all_weekly_tasks if t["status"] == "completed"])
        weekly_total = len(all_weekly_tasks)
        
        progress = {
            "dailyDone": daily_completed,
            "dailyTotal": daily_total,
            "weeklyDone": weekly_completed,
            "weeklyTotal": weekly_total
        }
        
        # === PREPARE INSIGHT DATA ===
        daily_completed_tasks = [
            {
                "name": t.get("name") or t["description"],
                "description": t["description"],
                "milestone_id": t["milestone_id"]
            }
            for t in today_tasks if t["status"] == "completed"
        ]
        
        weekly_completed_tasks = [
            {
                "name": t.get("name") or t["description"],
                "description": t["description"],
                "milestone_id": t["milestone_id"]
            }
            for t in all_weekly_tasks if t["status"] == "completed"
        ]
        
        # === GENERATE INSIGHT (Simple version - replace with AI if needed) ===
        daily_done = len(daily_completed_tasks)
        
        if daily_done == 0:
            insight_text = "Let's get started! Complete your first task today. 💪"
        elif daily_done == daily_total and daily_total > 0:
            insight_text = f"Amazing! You've completed all {daily_total} tasks today! 🎉"
        else:
            insight_text = f"Great progress! {daily_done}/{daily_total} tasks done today, {weekly_completed}/{weekly_total} this week. Keep going! 🚀"
        
        insight = {
            "text": insight_text
        }
        
        # === RETURN ===
        return {
            "todayHabits": today_habits,
            "progress": progress,
            "insight": insight
        }
        

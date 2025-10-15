# backend/app/main.py
from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field # pyright: ignore[reportMissingImports]
from datetime import datetime
from typing import Dict, List, Literal, Optional
from managers.Goal_Manger import GoalManager
from managers.goal.model import GoalSave, goal_input, GoalOutput
from managers.milestone_manager import MilestoneManager
from  managers.milestones.model import milestones
from managers.task.model import Task, TaskSpecification
from managers.task_manager import TaskManager
from sample import *
from models import HabitOut, HomeDataOut, InsightOut, MonthlyAnalyticsOut, ProgressOut

app = FastAPI(title="Stub API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- INPUT / OUTPUT MODELS ----------


# ---------- ENDPOINTS ----------

@app.get("/home", response_model=HomeDataOut)
def get_homedata():
    """Return home screen data with today's habits, progress, and insights"""
    try:
        return TaskManager.get_home_data("test123")
    except Exception as e:
        # Log the error (add your logging here)
        print(f"Error fetching home data: {e}")
        
        # Return a safe fallback response
        return HomeDataOut(
            todayHabits=[],
            progress=ProgressOut(dailyDone=0, dailyTotal=0, weeklyDone=0, weeklyTotal=0),
            insight=InsightOut(text="Unable to load data right now. Please try again! 🔄")
        )

@app.get("/goals")
def list_goals(): 
    goals = GoalManager.getGoals()
    return goals

@app.post("/goals/analyze", response_model=GoalOutput)
def analyze_goal(payload: goal_input): 
    goal = GoalManager.analyse_draft(payload)
    print(goal)
    return goal

@app.post("/goals/verify_and_save")
def verify_and_save_goal(payload: GoalSave) -> dict:
        """Verify and save a goal in a single step."""
        GoalManager.verify_and_save(payload)
        return {"status": "ok"}



@app.get("/goals/{goal_id}/milestones")
def get_milestones(goal_id: str): 
 milestones =   MilestoneManager.return_milestone(goal_id)
 return milestones
    # return get_sample_milestone_data()

    

@app.get("/milestones/{milestone_id}/tasks")
def get_tasks(milestone_id: str): 
    tasks =TaskManager.return_task_list(milestone_id)
    return tasks
 


@app.get("/tasks/{task_id}/completion")
def get_task_completion(task_id: str):
    """Get task completion data for the completion form"""
 
    return TaskManager.get_task_completion_data(task_id)
    

@app.patch("/tasks/{task_id}")
def update_task_completion(task_id: str, payload: TaskSpecification):
    """Update task completion status and user notes"""
    response = TaskManager.complete_task(payload)
    return response

@app.get("/analytics/daily")
def daily_analytics():
    """Get daily analytics data"""
    sample_data = ()
    return sample_data

@app.get("/analytics/monthly", response_model=MonthlyAnalyticsOut)
def monthly_analytics():
    """Get monthly analytics data"""
    sample_data = ()
    return 

@app.get("/schedule", response_model=dict)
def get_schedule():
    return {
        "monday": [
            {"day": "Monday", "time_slot": "09:00-09:30", "minutes": 30, "milestone_title": "Flutter Study – Ch3"},
            {"day": "Monday", "time_slot": "18:00-18:45", "minutes": 45, "milestone_title": "Gym – Upper Body"},
        ],
        "tuesday": [
            {"day": "Tuesday", "time_slot": "08:00-08:25", "minutes": 25, "milestone_title": "Meditation"},
        ],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": [],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# backend/app/main.py
from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field # pyright: ignore[reportMissingImports]
from datetime import datetime
from typing import Dict, List, Literal, Optional
from managers.Goal_Manger import GoalManager
from managers.goal.model import goal_input, GoalOutput
from managers.milestone_manager import MilestoneManager
from  managers.milestones.model import milestones
from managers.task.model import Task
from managers.task_manager import TaskManager
from sample import *

app = FastAPI(title="Stub API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- INPUT / OUTPUT MODELS ----------

class HabitOut(BaseModel):
    id: str
    name: str
    minutes: int
    isCompleted: bool = False

class ProgressOut(BaseModel):
    dailyDone: int
    dailyTotal: int
    weeklyDone: int
    weeklyTotal: int

class InsightOut(BaseModel):
    text: str

class HomeDataOut(BaseModel):
    todayHabits: List[HabitOut]
    progress: ProgressOut
    insight: InsightOut

class GoalOut(BaseModel):
    id: str
    name: str
    completion_rate: float
    is_completed: bool

class MilestoneOut(BaseModel):
    objective: str
    success_criteria: str
    targetDate: datetime
    enables: str
    status: Literal["pending", "active", "completed"]
    assigned_timeslot: Optional[str] = None

class DailyAnalyticsOut(BaseModel):
    habit_completion_rate: float
    goal_completion_rate: float
    last_7_days_habit: Dict[str, float]
    goals_breakdown: List[Dict[str, float]]

class MonthlyAnalyticsOut(BaseModel):
    habits_achieved: int
    goals_achieved: int
    days_active: int
    weekly_habit_completion: List[float]
    weekly_goals_achieved: List[int]
    insight: str

# ---------- ENDPOINTS ----------

@app.get("/home", response_model=HomeDataOut)
def get_home_data():
    """Return home screen data with today's habits, progress, and insights"""
    return HomeDataOut(
        todayHabits=[
            HabitOut(
                id="h1",
                name="Morning Meditation",
                minutes=15,
                isCompleted=True
            ),
            HabitOut(
                id="h2", 
                name="Read Technical Book",
                minutes=30,
                isCompleted=False
            ),
            HabitOut(
                id="h3",
                name="Exercise",
                minutes=45,
                isCompleted=True
            ),
            HabitOut(
                id="h4",
                name="Practice Guitar",
                minutes=20,
                isCompleted=False
            ),
            HabitOut(
                id="h5",
                name="Journal Writing",
                minutes=10,
                isCompleted=False
            )
        ],
        progress=ProgressOut(
            dailyDone=2,
            dailyTotal=5,
            weeklyDone=12,
            weeklyTotal=35
        ),
        insight=InsightOut(
            text="You're 40% through your daily habits! Keep going - you've got this! 💪"
        )
    )

@app.get("/goals")
def list_goals(): 
    # goals = GoalManager.getGoals()
    # return goals
    return get_sample_goal_data()


@app.post("/goals/analyze", response_model=GoalOutput)
def analyze_goal(payload: goal_input): 
    goal = GoalManager.analyse_draft(payload)
    print(goal)
    return goal

@app.post("/goals")
def save_goal(payload: GoalOutput) -> dict:
    GoalManager.verify_and_save(payload)
    return {"status": "ok"}

@app.get("/goals/{goal_id}/milestones")
def get_milestones(goal_id: str): 
#  milestones =   MilestoneManager.return_milestone(goal_id)
#  return milestones
    return get_sample_milestone_data()

    

@app.get("/milestones/{milestone_id}/tasks")
def get_tasks(milestone_id: str): 
    # tasks =TaskManager.return_task_list(milestone_id)
    # return tasks
    return get_sample_task_data()


@app.get("/tasks/{task_id}/completion")
def get_task_completion(task_id: str):
    """Get task completion data for the completion form"""
    return get_sample_task_completion_data()
    # return TaskManager.get_task_completion_data(task_id)
    

@app.patch("/tasks/{task_id}")
def update_task_completion(task_id: str, payload: dict):
    """Update task completion status and user notes"""
    # TaskManager.update_task_completion(task_id, payload)
    return {"status": "ok"}

@app.get("/analytics/daily")
def daily_analytics():
    """Get daily analytics data"""
    sample_data = get_sample_daily_analytics()
    return sample_data

@app.get("/analytics/monthly", response_model=MonthlyAnalyticsOut)
def monthly_analytics():
    """Get monthly analytics data"""
    sample_data = get_sample_monthly_analytics()
    return MonthlyAnalyticsOut(**sample_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from datetime import datetime
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel


class HabitOut(BaseModel):
    id: str
    name: str
    minutes: int = 0  # Default to 0 if not provided
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
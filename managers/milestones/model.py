from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime



class status_state(str, Enum):
    active = "active"
    completed = "completed"
    pending = "pending"




class milestone(BaseModel):
    index: int
    description: str = Field(description=" brief description of the milestone")
    objective: str = Field(description=" What are you building/developing/ achieving")
    success_criteria: str = Field(description=" specific mesurable completion condition")
    targetDate: datetime = Field(description="specific end date")
    enables: str = Field(description="what does it make possible for the next milestone")
    status: status_state = status_state.pending
    
    
    
class milestones (BaseModel):
    goal_id: int
    goal_name: str
    goal_description: str
    context: str
    milestones : list[milestone] = Field(description=" list of milestones")
    
from typing import List, Literal, Dict, Optional

# ====== MODELS FOR INPUT ======

# ====== INPUT MODELS ======

class MilestoneInput(BaseModel):
    milestone_id: str
    title: str
    objective: str
    success_criteria: str
    target_date: str  # ISO format YYYY-MM-DD

class TimeSlotEntry(BaseModel):
    milestone_id: str
    time_slot: str  # "HH:MM-HH:MM"
    allocated_minutes: int
    priority_score: int  # 0-100
    flexibility: Literal["low", "medium", "high"]

class WeeklySchedule(BaseModel):
    monday: List[TimeSlotEntry] = []
    tuesday: List[TimeSlotEntry] = []
    wednesday: List[TimeSlotEntry] = []
    thursday: List[TimeSlotEntry] = []
    friday: List[TimeSlotEntry] = []
    saturday: List[TimeSlotEntry] = []
    sunday: List[TimeSlotEntry] = []

class TimeMasterInput(BaseModel):
    milestone: MilestoneInput
    existing_schedule: WeeklySchedule

# ====== MODELS FOR OUTPUT ======

class MilestoneTimeSlot(BaseModel):
    day: str  # "Monday", "Tuesday", etc.
    time_slot: str  # "09:00-09:30"
    minutes: int

class MilestoneScheduleSummary(BaseModel):
    milestone_id: str
    time_slots: List[MilestoneTimeSlot]
    total_minutes: int

class TimeMasterOutput(BaseModel):
    updated_schedule: WeeklySchedule  # Full context
    milestone_summaries: List[MilestoneScheduleSummary]  # All affected milestones
class evaluation_feedback(BaseModel):
    user_eval: str
    system_eval: str
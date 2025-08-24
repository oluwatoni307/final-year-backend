from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime



class status_state(str, Enum):
    active = "active"
    completed = "completed"
    pending = "pending"




class milestone(BaseModel):
    
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

class MilestoneInput(BaseModel):
    """Represents a single milestone to be scheduled"""
    title: str
    objective: str
    success_criteria: str
    target_date: str  # ISO format date string (YYYY-MM-DD)
    enables: str  # What this milestone enables next

class TimeSlotEntry(BaseModel):
    """Represents an existing time commitment in the user's schedule"""
    milestone_id: str
    time_slot: str  # Format: "HH:MM-HH:MM"
    allocated_minutes: int
    priority_score: int  # 0-100
    flexibility: Literal["low", "medium", "high"]

class ExistingTimetable(BaseModel):
    """Structure of the user's current schedule by day"""
    monday: List[TimeSlotEntry] = []
    tuesday: List[TimeSlotEntry] = []
    wednesday: List[TimeSlotEntry] = []
    thursday: List[TimeSlotEntry] = []
    friday: List[TimeSlotEntry] = []
    saturday: List[TimeSlotEntry] = []
    sunday: List[TimeSlotEntry] = []

class TimekeeperInput(BaseModel):
    """Complete input structure for the Timekeeper service"""
    milestone: MilestoneInput
    existing_timetable: ExistingTimetable


# ====== MODELS FOR OUTPUT ======

class ScheduledTimeSlot(BaseModel):
    """Represents a scheduled time slot with resistance metrics"""
    milestone_id: str
    time_slot: str  # Format: "HH:MM-HH:MM"
    allocated_minutes: int
    priority_score: int  # 0-100
    flexibility: Literal["low", "medium", "high"]
    resistance_score: int  # 0-100, lower = easier integration

class OptimizedTimetable(BaseModel):
    """Complete output timetable structure organized by day"""
    monday: List[ScheduledTimeSlot] = []
    tuesday: List[ScheduledTimeSlot] = []
    wednesday: List[ScheduledTimeSlot] = []
    thursday: List[ScheduledTimeSlot] = []
    friday: List[ScheduledTimeSlot] = []
    saturday: List[ScheduledTimeSlot] = []
    sunday: List[ScheduledTimeSlot] = []


class Timekeeperoutput(BaseModel):
    """Complete input structure for the Timekeeper service"""
    milestoneslot: ScheduledTimeSlot
    OptimizedTimetable: OptimizedTimetable

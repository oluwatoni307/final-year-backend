from pydantic import BaseModel, Field
from typing import List

class Activity(BaseModel):
    """A single scheduled activity with essential details only."""
    
    title: str = Field(
        ..., 
        description="Name of the activity (e.g., 'Spanish Vocabulary', 'Morning Workout')"
    )
    
    day: str = Field(
        ...,
        description="Day of the week (e.g., 'Monday', 'Tuesday')"
    )
    
    start_time: str = Field(
        ...,
        description="Start time in HH:MM format (e.g., '07:45', '14:30')"
    )
    
    end_time: str = Field(
        ..., 
        description="End time in HH:MM format (e.g., '08:15', '15:00')"
    )
    
    duration_minutes: int = Field(
        ...,
        description="How long the activity lasts in minutes (e.g., 30, 45, 60)"
    )
    
    resistance_score: int = Field(
        ...,
        description="Difficulty to maintain from 0-100 (lower = easier to stick with)"
    )

class WeeklySchedule(BaseModel):
    """Complete weekly schedule with list of activities."""
    
    activities: List[Activity] = Field(
        ...,
        description="All scheduled activities for the week"
    )

# Simple example for LLM reference
EXAMPLE = {
    "activities": [
        {
            "title": "Fitness Routine",
            "day": "Monday", 
            "start_time": "06:30",
            "end_time": "07:30",
            "duration_minutes": 60,
            "resistance_score": 15
        },
        {
            "title": "Spanish Vocabulary",
            "day": "Monday",
            "start_time": "07:45", 
            "end_time": "08:15",
            "duration_minutes": 30,
            "resistance_score": 15
        }
    ]
}
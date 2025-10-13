from typing import List, Literal
from pydantic import BaseModel, Field  # type: ignore

# === INPUT MODEL ===
class MilestoneInput(BaseModel):
    """The only input: a single milestone to decompose"""
    milestone_id: str
    objective: str
    success_criteria: str
    target_date: str
    enables: str
    timeslot: List  # "HH:MM-HH:MM"
    previous_milestone_data : str

# === OUTPUT MODEL ===
class TaskSpecification(BaseModel):
    task_id: str
    task_type: Literal["encoding", "consolidation", "retrieval", "application", "assessment"]
    title: str
    objective: str
    specific_actions: List[str]
    time_allocated: str
    cognitive_load: Literal["low", "medium", "high"]
    success_metric: str
    day: str = Field(description="Day of the week assigned for this . Monday, Tuesday, etc.")
    week_number: int = Field(description="Week number   for the taskwithin the milestone timeline, starting from 1")

class TaskDecompositionOutput(BaseModel):
    tasks: List[TaskSpecification]



# Task_completion    

class rating_model(BaseModel):
    rating: int
    feedaback: str
 
 
class Task(TaskSpecification):
    description: str
    rating: rating_model
    status: Literal["pending", "active", "completed"]
    
    
    

from typing import List, Literal
from pydantic import BaseModel # type: ignore

# === INPUT MODEL ===
class MilestoneInput(BaseModel):
    """The only input: a single milestone to decompose"""
    milestone_id: str
    objective: str
    success_criteria: str
    target_date: str
    enables: str

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

class TaskDecompositionOutput(BaseModel):
    tasks: List[TaskSpecification]
    
class Task(TaskSpecification):
    description: str
    rating: int
    status: Literal["pending", "active", "completed"]
    
    
class rating(BaseModel):
    rating: int
    comment: str
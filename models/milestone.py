from enum import Enum
from pydantic import BaseModel, Field # pyright: ignore[reportMissingImports]
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
    context: str
    
    milestones : list[milestone] = Field(description=" list of milestones")
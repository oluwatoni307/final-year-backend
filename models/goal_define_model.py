from typing_extensions import Literal
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum



class option(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class goal_input(BaseModel):
    statement: str
    date: str
    importance: int
    context: str = Field(..., description="full context necessaryly including skills you have to complete task")
   
   
   
class goal_output(BaseModel):
    goal_type: str
    specific: int
    complexity: option
    motivation: Literal["Intrinsic", "Extrinsic", "Mixed"]
    skill_level: Literal["None", "Small", "Large"]
    dependencies: Literal["Independent", "Some", "Many"]
    measurability:Literal ["Quantitative", "Qualitative", "Milestone"]
    decomposability: option
    urgency: option
    autonomy: Literal["Self-Directed","Guided","Imposed"]
    readiness: option
    
    

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
    date: datetime
    importance: int
    context: str = Field(..., description="full context necessaryly including skills you have to complete task")
   
   
   
from typing import Literal, Optional
from pydantic import BaseModel

class GoalOutput(BaseModel):
    # === PART B: 12 DERIVED PARAMETERS ===
    
    goal_type: Literal["Achievement", "Learning", "Habit", "Maintenance"]
    specific: int  # 1-10 specificity score
    complexity: Literal["Simple", "Moderate", "Complex"]
    motivation: Literal["Intrinsic", "Extrinsic", "Mixed"]
    skill_level: Literal["None", "Small", "Large"]
    dependencies: Literal["Independent", "Some", "Many"]
    measurability: Literal["Quantitative", "Qualitative", "Milestone"]
    decomposability: Literal["High", "Medium", "Low"]
    urgency: Literal["High", "Medium", "Low"]
    autonomy: Literal["Self-Directed", "Guided", "Imposed"]
    readiness: Literal["Ready", "Pre-Ready", "Not Ready"]
    identity_alignment: Literal["High", "Medium", "Low"]

    # === PART C: GOAL PROFILE OUTPUT ===
    goal_classification: str  # e.g., "High-Autonomy Learning Goal"
    complexity_rating: float  # 1.0 - 10.0, e.g., 7.2
    success_probability: Literal["High", "Medium", "Low"]
    recommended_approach: str  # e.g., "Break into weekly sprints with progress reviews"


class Goal(BaseModel):
    id: str 
    userId:str
    date: datetime
    goal_type: Literal["Achievement", "Learning", "Habit", "Maintenance"]
    specific: int  # 1-10 specificity score
    complexity: Literal["Simple", "Moderate", "Complex"]
    motivation: Literal["Intrinsic", "Extrinsic", "Mixed"]
    skill_level: Literal["None", "Small", "Large"]
    dependencies: Literal["Independent", "Some", "Many"]
    measurability: Literal["Quantitative", "Qualitative", "Milestone"]
    decomposability: Literal["High", "Medium", "Low"]
    urgency: Literal["High", "Medium", "Low"]
    autonomy: Literal["Self-Directed", "Guided", "Imposed"]
    readiness: Literal["Ready", "Pre-Ready", "Not Ready"]
    identity_alignment: Literal["High", "Medium", "Low"]
    goal_classification: str
    complexity_rating: float  # 1.0 - 10.0
    success_probability: Literal["High", "Medium", "Low"]
    recommended_approach: str
    
    
class GoalSave(BaseModel):
    """Combines user input with key analysis fields for saving"""
    
    # From GoalInput
    user_id: str
    statement: str
    date: datetime
    importance: int
    context: str
    
    # Key fields from GoalOutput
    goal_classification: str
    complexity_rating: float
    recommended_approach: str
    success_probability: str
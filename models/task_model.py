from enum import Enum
from grpc import Status
from pydantic import BaseModel, Field
from typing import List, Optional



class status_state(str, Enum):
    active = "active"
    completed = "completed"
    pending = "pending"

class Task(BaseModel):
    """A learning task with essential specification details"""
    
    task_id: str = Field(
        ...,
        description="Unique identifier for this task (e.g., 'spanish_vocab_01', 'math_algebra_basic')"
    )
    
    task_type: str = Field(
        ...,
        description="Type of learning task: encoding, consolidation, retrieval, application, or assessment"
    )
    
    title: str = Field(
        ...,
        description="Clear, action-oriented task name (e.g., 'Practice Spanish Present Tense Verbs')"
    )
    
    objective: str = Field(
        ...,
        description="Specific learning outcome this task achieves (e.g., 'Master 20 common Spanish verbs in present tense')"
    )
    
    time_allocated: int = Field(
        ...,
        description="Duration in minutes needed to complete this task"
    )
    
    cognitive_load: str = Field(
        ...,
        description="Mental effort required: low, medium, or high"
    )
    
    materials_needed: List[str] = Field(
        ...,
        description="List of resources required (e.g., ['textbook', 'flashcards', 'audio_files'])"
    )
    
    success_metric: str = Field(
        ...,
        description="How to measure if the task is completed successfully (e.g., '80% accuracy on practice quiz')"
    )
    
    
    difficulty_level: int = Field(
        ...,
        description="Difficulty on 1-10 scale where 1 is very easy and 10 is very hard"
    )
    
    prerequisite_tasks: List[str] = Field(
        default_factory=list,
        description="List of task IDs that must be completed before this task"
    )
    
    enables_tasks: List[str] = Field(
        default_factory=list,
        description="List of task IDs that become available after completing this task"
    )
    
    spacing_interval: int = Field(
        ...,
        description="Number of days since last similar task for optimal spaced repetition"
    )
    status: status_state = status_state.pending

class TaskSequence(BaseModel):
    """Collection of related learning tasks"""
    
    tasks: List[Task] = Field(
        ...,
        description="List of all tasks in this learning sequence"
    )
    
    sequence_title: Optional[str] = Field(
        None,
        description="Name for this collection of tasks"
    )

# Simple example
EXAMPLE = {
    "tasks": [
        {
            "task_id": "spanish_verbs_01",
            "task_type": "encoding",
            "title": "Learn 10 Basic Spanish Verbs",
            "objective": "Memorize conjugation of 10 common Spanish verbs in present tense",
            "time_allocated": 25,
            "cognitive_load": "medium",
            "materials_needed": ["verb_list", "conjugation_chart"],
            "success_metric": "Correctly conjugate 8 out of 10 verbs",
            "difficulty_level": 4,
            "prerequisite_tasks": [],
            "enables_tasks": ["spanish_verbs_02"],
            "spacing_interval": 0
        },
        {
            "task_id": "spanish_verbs_02", 
            "task_type": "consolidation",
            "title": "Practice Spanish Verb Conjugations",
            "objective": "Reinforce previously learned verb conjugations through repetition",
            "time_allocated": 15,
            "cognitive_load": "low",
            "materials_needed": ["flashcards"],
            "success_metric": "Complete 50 flashcard reviews with 90% accuracy",
            "difficulty_level": 3,
            "prerequisite_tasks": ["spanish_verbs_01"],
            "enables_tasks": ["spanish_conversation_01"],
            "spacing_interval": 2
        }
    ]
}
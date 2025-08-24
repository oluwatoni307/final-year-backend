from typing import Dict, List
from ..db import select, insert, update




from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from .model import  milestone, ExistingTimetable, TimekeeperInput, ScheduledTimeSlot, OptimizedTimetable, Timekeeperoutput



def timeMaster(Milestone: milestone, existing_timetable: ExistingTimetable) -> OptimizedTimetable:
    """
    Generate a course outline based on the course name and description.
    """
    time_model = model.with_structured_output(OptimizedTimetable)
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are an expert in course design. "
                "Generate a detailed course outline based on the provided course name and description."
            ),
            HumanMessage(
                content=str(Milestone)
            ),
        ]
    )

    response:OptimizedTimetable = time_model.invoke(prompt) # type: ignore
    update_timeslot(response)
    return response



    
def update_timeslot(timetable: OptimizedTimetable) -> Dict[str, List[Dict[str, str]]]:
    """ sample timeslot data structure
    {
  "spanish_grammar_m1": [
    {"timeslot": "07:45-08:15", "allocated_minutes": 30},
    {"timeslot": "19:30-19:45", "allocated_minutes": 15},
    {"timeslot": "14:00-14:45", "allocated_minutes": 45}
  ],
  "fitness_routine_m1": [
    {"timeslot": "06:30-07:30", "allocated_minutes": 60}
  ],
  "project_report_m2": [
    {"timeslot": "12:00-12:30", "allocated_minutes": 30}
  ]
}"""
    timeslots = {}
    for day_name in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        day_slots = getattr(timetable, day_name, [])
        for slot in day_slots:
            if slot.milestone_id not in timeslots:
                timeslots[slot.milestone_id] = []
            timeslots[slot.milestone_id].append({
                "timeslot": slot.time_slot,
                "allocated_minutes": slot.allocated_minutes,
            })
            
    for milestone_id in timeslots:
        update(
            "milestones",
            {"id": milestone_id},
            {"sessions": timeslots[milestone_id]}  # Assuming all milestones are set to active
        )
        
    return timeslots
            
            
            
        
        
from typing import Dict, List
from ..db import select, insert, update




from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from .model import TimeMasterOutput, milestone,WeeklySchedule
from .prompt import TIME_MASTER_SYSTEM_PROMPT

def timeMaster(Milestone, existing_timetable) -> TimeMasterOutput:
    """
    Generate a course outline based on the course name and description.
    """
    time_model = model.with_structured_output(TimeMasterOutput)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TIME_MASTER_SYSTEM_PROMPT),
            ("user", "{milestone}\n\nExisting Timetable:\n{existing_timetable}"),
        ]
    )

    formatted_prompt = prompt.invoke({
        "milestone": str(Milestone),
        "existing_timetable": str(existing_timetable)
    })
    response:TimeMasterOutput = time_model.invoke(formatted_prompt) # type: ignore
    update_timeslot(response)
    return response



def update_timeslot(timetable: TimeMasterOutput) -> Dict[str, List[Dict[str, str]]]:
    """Sample timeslot data structure
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
    
    # Use milestone_summaries - it's already grouped by milestone_id
    for summary in timetable.milestone_summaries:
        timeslots[summary.milestone_id] = []
        for slot in summary.time_slots:
            timeslots[summary.milestone_id].append({
                "day": slot.day,
                "timeslot": slot.time_slot,
                "allocated_minutes": slot.minutes
            })
    
    # Update database for each milestone
    for milestone_id in timeslots:
        update(
            "milestones",
            {"id": milestone_id},
            {"assigned_timeslot": timeslots[milestone_id]}
        )
    
    return timeslots
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from models.goal_define_model import  goal_output, goal_input
from models.milestone import milestone
from models.timetable_model import WeeklySchedule


def timetable(milestone: milestone):
    """
    Generate a course outline based on the course name and description.
    """
    time_model = model.with_structured_output(WeeklySchedule)
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are an expert in course design. "
                "Generate a detailed course outline based on the provided course name and description."
            ),
            HumanMessage(
                content=f"Course Name: "
            ),
        ]
    )

    response:WeeklySchedule = time_model.invoke(prompt) # type: ignore
    # save to timetable_db
    
    
  
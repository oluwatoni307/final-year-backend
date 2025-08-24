from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from models.goal_define_model import  goal_output, goal_input


def goal_definer(goal_info: goal_input):
    """
    Generate a course outline based on the course name and description.
    """
    goal_def = model.with_structured_output(goal_output)
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

    response:goal_output = goal_def.invoke(prompt) # type: ignore
    return response
    
    
  
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from .model import  milestones


def milestone_creator(goal):
    """
    Generate a course outline based on the course name and description.
    """
    milestone_model = model.with_structured_output(milestones)
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are an expert in course design. "
                "Generate a detailed course outline based on the provided course name and description."
            ),
            HumanMessage(
                content=str(goal)
            ),
        ]
    )

    response:milestones = milestone_model.invoke(prompt) # type: ignore
    return response
    
    
  
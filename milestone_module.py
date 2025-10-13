from langchain_core.messages import HumanMessage, SystemMessage # pyright: ignore[reportMissingImports]
from langchain_core.prompts import ChatPromptTemplate # pyright: ignore[reportMissingImports]
from langchain_core.output_parsers import StrOutputParser # pyright: ignore[reportMissingImports]
from ai_model import model
from models.goal_define_model import goal_output # type: ignore
from models.milestone import  milestone # type: ignore


def milestone_master(goal_info: goal_output):
    """
    Generate a course outline based on the course name and description.
    """
    milestone_model = model.with_structured_output(list[milestone])
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

    response:list[milestone] = milestone_model.invoke(prompt) # type: ignore
    return response
    
    
    
  
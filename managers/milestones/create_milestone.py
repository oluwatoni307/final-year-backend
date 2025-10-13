from langchain_core.prompts import ChatPromptTemplate
from ai_model import model
from .model import milestones
from .prompt import MILESTONE_SYSTEM_PROMPT


def milestone_creator(goal):
    """
    Generate a course outline based on the course name and description.
    """
    milestone_model = model.with_structured_output(milestones)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", MILESTONE_SYSTEM_PROMPT),
            ("user", "{goal}"),
        ]
    )

    formatted_prompt = prompt.invoke({"goal": str(goal)})
    response: milestones = milestone_model.invoke(formatted_prompt)  # type: ignore
    return response
from langchain_core.prompts import ChatPromptTemplate
from ai_model import model
from .model import evaluation_feedback
from .prompt import MILESTONE_SYSTEM_PROMPT


def evaluate(feedback):
    """
    Generate a course outline based on the course name and description.
    """
    milestone_model = model.with_structured_output(evaluation_feedback)
    #TODO:Create the prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", ""),
            ("user", "{feedback}"),
        ]
    )

    formatted_prompt = prompt.invoke({"feedback": str(feedback)})
    response: evaluation_feedback = milestone_model.invoke(formatted_prompt)  # type: ignore
    return response
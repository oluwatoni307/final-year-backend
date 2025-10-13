from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from .model import TaskDecompositionOutput
from .prompt import TASK_MANAGER_PROMPT


def task_creator(goal):
    """
    Generate a course outline based on the course name and description.
    """
    task_model = model.with_structured_output(TaskDecompositionOutput)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TASK_MANAGER_PROMPT),
            ("user", "{goal}"),
        ]
    ).invoke({"goal": str(goal)})
    response:TaskDecompositionOutput = task_model.invoke(prompt) # type: ignore
    response.tasks[0]
    return response
    
    
  
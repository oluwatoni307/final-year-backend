from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from .model import  rating_model, TaskSpecification
from ..db import update


def task_maker(task: TaskSpecification):
    """
    Generate a course outline based on the course name and description.
    """
    marker_model = model.with_structured_output(rating_model)
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are an expert in course design. "
                "Generate a detailed course outline based on the provided course name and description."
            ),
            HumanMessage(
                content=str(task)
            ),
        ]
    )

    response:rating_model = marker_model.invoke(prompt) # type: ignore
    update("tasks", {"task_id": task.task_id}, {"completed":{"rating": response.rating, "feedback": response.feedaback, "status": "completed"}, "status": "completed"})
    return response
    
    
  
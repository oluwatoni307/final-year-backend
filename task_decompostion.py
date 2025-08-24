from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from task_model import TaskSequence

def task(milestone:TaskSequence):
    """
    Generate a course outline based on the course name and description.
    """
    task_model = model.with_structured_output(TaskSequence)
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

    response:TaskSequence = task_model.invoke(prompt) # type: ignore
    return response
    
    
    
  
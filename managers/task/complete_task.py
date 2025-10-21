from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from .model import  rating_model, TaskSpecification
from ..db import supa



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
    result = supa.rpc(
        'complete_task_and_check',
        {
            'p_task_id': task.task_id,
            'p_rating': response.rating,
            'p_feedback': response.feedback
        }
    ).execute().data

    remaining_tasks = result['remaining_tasks']
    milestone_id = result['milestone_id']

    if remaining_tasks == 0:
        print(f"🎉 Milestone {milestone_id} completed!")
        # Update milestone status or do something else
        
    return response, remaining_tasks, milestone_id
        
    
  
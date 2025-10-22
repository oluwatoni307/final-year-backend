from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model
from .model import rating_model, TaskSpecification
from ..db import supa

TASK_GRADER_PROMPT = """You are an expert task evaluator for educational and productivity tasks. 

Your job is to:
1. Analyze the user's completion description against the task requirements
2. Evaluate if the completion meets the task objective and success metrics
3. Provide a fair rating and constructive feedback

RATING SCALE (1-10):
- 1-3: Incomplete or does not address the task objective
- 4-5: Partially complete, missing key elements or success metrics
- 6-7: Satisfactory completion, meets basic requirements
- 8-9: Strong completion, exceeds expectations in some areas
- 10: Exceptional completion, fully meets all criteria with excellence

GRADING CRITERIA:
✓ Does the completion address the specific actions required?
✓ Does it align with the task objective?
✓ Does it meet or approach the success metric?
✓ Is the effort appropriate for the cognitive load and time allocated?

FEEDBACK GUIDELINES:
- Start with what was done well (be specific)
- Address how well they met the objective and success metrics
- If not perfect, provide 1-2 actionable suggestions for improvement
- Keep feedback concise (2-4 sentences), encouraging, and growth-focused
- End on a positive or motivational note

Remember: Recognize genuine effort and progress, even if execution isn't perfect.

OUTPUT FORMAT:
You must return a response with exactly these two fields:
- rating: An integer between 1 and 10 (inclusive)
- feedback: A string containing 2-4 sentences of constructive feedback"""

def task_grader(task_id, task):
    """
    Generate a course outline based on the course name and description.
    """
    marker_model = model.with_structured_output(rating_model)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         TASK_GRADER_PROMPT
        ),
        ("user", "{task}"),
    ]).invoke({"task": str(task)})

    response: rating_model = marker_model.invoke(prompt)  # type: ignore
    
    result = supa.rpc(
        'complete_task_and_check',
        {
            'p_task_id': task_id,
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
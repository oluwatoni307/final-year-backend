# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from ai_model import model
# from .model import  rating, TaskSpecification


# def task_maker(task: TaskSpecification):
#     """
#     Generate a course outline based on the course name and description.
#     """
#     marker_model = model.with_structured_output(rating)
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             SystemMessage(
#                 content="You are an expert in course design. "
#                 "Generate a detailed course outline based on the provided course name and description."
#             ),
#             HumanMessage(
#                 content=str(task)
#             ),
#         ]
#     )

#     response:rating = marker_model.invoke(prompt) # type: ignore
#     return response
    
    
  
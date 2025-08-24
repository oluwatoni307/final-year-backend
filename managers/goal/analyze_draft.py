from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_model import model  # imports the "model" object from ai_model.py
from .model import  GoalOutput, goal_input
from .prompt import goal_prompt

from langchain_core.prompts import ChatPromptTemplate
from ai_model import model
from .model import GoalOutput, goal_input

prompt = ChatPromptTemplate.from_messages([
    ("system", goal_prompt),
    ("human", "{goal_info}"),
])

goal_chain = prompt | model.with_structured_output(GoalOutput)

def goal_definer(goal_info: goal_input):
    return goal_chain.invoke({"goal_info": str(goal_info)})
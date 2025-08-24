from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os



from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()  # Load DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up SQLModel engine
engine = create_engine(DATABASE_URL, echo=True) # type: ignore

def get_session():
    return Session(engine)


from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str



def save(goal, milestones):
    pass
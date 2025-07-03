from sqlmodel import SQLModel, Field, create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")


class Foundation(SQLModel, table=True):
    __tablename__: str = "foundations"
    
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    image_url: str
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    deleted_at: datetime = Field(default=None, nullable=True)
    
class Donation(SQLModel, table=True):
    __tablename__: str = "donations"
    
    id: int = Field(default=None, primary_key=True)
    person_name: str
    amount: float
    created_at: datetime = Field(default=datetime.now(), nullable=False)

class GoalCategory(SQLModel, table=True):
    __tablename__: str = "goal_categories"
    
    id: int = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    max_amount: float = Field(
        default=100, nullable=False,
        description="Maximum amount of money that can be donated to this goal"
    )
    
class Goal(SQLModel, table=True):
    __tablename__: str = "goals"
    
    id: int = Field(default=None, primary_key=True)
    description: str
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    category_id: int = Field(foreign_key="goal_categories.id")
    foundation_id: int = Field(foreign_key="foundations.id")
    donation_id: int = Field(foreign_key="donations.id")


URL_CONNECTION = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(URL_CONNECTION)
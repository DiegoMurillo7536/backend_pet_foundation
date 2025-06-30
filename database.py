from sqlmodel import SQLModel, Session, select
from models.models import engine
from typing import Callable, TypeVar

T = TypeVar('T')

def create_db_and_tables():
    """
    Create all tables in the database

    Raises:
        Exception: Raise an exception if the tables cannot be created
    """
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        raise Exception(f"Error creating tables: {e}")

def with_db_session(operation: Callable[[Session], T]) -> T:
    """
    Execute an operation with a database session
    
    Args:
        operation: Function that takes a session and returns a result
        
    Returns:
        The result of the operation
    """
    with Session(engine) as session:
        return operation(session)

def execute_query(query: SQLModel):
    """
    Execute a query and return results
    
    Args:
        query: SQLModel query to execute
        
    Returns:
        Query results
    """
    return with_db_session(lambda session: session.exec(query))

if __name__ == "__main__":
    create_db_and_tables()
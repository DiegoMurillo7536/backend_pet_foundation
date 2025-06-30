from models.models import Goal
from database import with_db_session
from datetime import datetime
from logging import getLogger
from repositories.base_repository import BaseRepository

class GoalRepository(BaseRepository):
    
    def create(self, goal: Goal):
        return with_db_session(lambda session: self._insert_goal(session, goal))
    
    def _insert_goal(self, session, goal: Goal):
        session.add(goal)
        session.commit()
        return goal
    
    def get_by_id(self, id: int):
        return with_db_session(lambda session: self._fetch_goal_by_id(session, id))
    
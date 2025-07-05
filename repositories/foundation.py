from sqlmodel import select
from sqlalchemy import text
from models.models import Foundation
from database import with_db_session
from datetime import datetime
from repositories.base_repository import BaseRepository
from repositories.queries import queries
from exeptions.exeption import QueryNotFoundError

class FoundationRepository(BaseRepository):
    
    def get_all(self):
        return with_db_session(self._fetch_all_foundations)
    
    def get_by_id(self, id: int):
        return with_db_session(lambda session: self._fetch_foundation_by_id(session, id))

    def create(self, foundation: Foundation):
        """
        Create a new foundation in the database
        
        Args:
            foundation: Foundation object to create
            
        Returns:
            The created foundation with its ID
        """
        return with_db_session(lambda session: self._insert_foundation(session, foundation))
    
    def delete(self, foundation_id: int):
        return with_db_session(lambda session: self._delete_foundation(session, foundation_id))
    
    def update(self, foundation_id: int, foundation: Foundation):
        return with_db_session(lambda session: self._update_foundation(session, foundation_id, foundation))
    
    # Private methods - Database operations
    def _fetch_all_foundations(self, session):
        """Fetch all foundations from database"""
        result = session.exec(select(Foundation).where(Foundation.deleted_at == None))
        foundations = list(result.all())
        return foundations
    
    def _fetch_foundation_by_id(self, session, foundation_id: int):
        """Fetch a specific foundation by ID"""
        result = session.exec(select(Foundation).where(Foundation.id == foundation_id))
        return result.first()
    
    def _insert_foundation(self, session, foundation: Foundation):
        """Insert a new foundation into database"""
        session.add(foundation)
        session.commit()
        session.refresh(foundation)
        return foundation
    
    def _delete_foundation(self, session, foundation_id: int):
        """Delete a foundation from database"""
        foundation_to_delete = session.exec(select(Foundation).where(Foundation.id == foundation_id)).first()
        if foundation_to_delete:
            foundation_to_delete.deleted_at = datetime.now()
            session.commit()
            return foundation_to_delete
        return None
    
    def _update_foundation(self, session, foundation_id: int, foundation: Foundation):
        """Update a foundation in database"""
        foundation_to_update = session.exec(select(Foundation).where(Foundation.id == foundation_id)).first()
        if foundation_to_update:
            self._update_fields(foundation_to_update, foundation)
            session.commit()
            return foundation_to_update
        return None
    
    def get_all_with_goals_and_actual_amount_by_id(self, foundation_id: int):
        """Public method to get all foundations with goals and actual amount"""
        return with_db_session(lambda session: self._get_all_with_goals_and_actual_amount_native_sql(session, foundation_id))
    
    def _get_all_with_goals_and_actual_amount_native_sql(self, session, foundation_id: int):
        """Fetch all foundations with goals and actual amount using native SQL"""
        native_query = queries.get('get_foundation_with_goals_and_actual_amount')
        if native_query is None:
            raise QueryNotFoundError("get_foundation_with_goals_and_actual_amount")
        result = session.exec(text(native_query), params={'foundation_id': foundation_id})
        foundations_data = result.all()
        return [
            {
                'total_amount': row[0] if row[0] is not None else 0,
                'goal_amount': row[1] if row[1] is not None else 0
            }
            for row in foundations_data
        ]

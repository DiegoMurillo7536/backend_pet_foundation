from sqlmodel import select
from sqlalchemy import func, text
from models.models import Foundation, Goal, Donation, GoalCategory
from database import with_db_session
from datetime import datetime
from repositories.base_repository import BaseRepository


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
        result = session.exec(select(Foundation).where(Foundation.deleted_at.is_(None)).order_by(Foundation.id.asc()))
        foundations = list(result.all())
        self.logger.info(f"Found {len(foundations)} foundations")
        return foundations
    
    def _fetch_foundation_by_id(self, session, foundation_id: int):
        """Fetch a specific foundation by ID"""
        result = session.exec(select(Foundation).where(Foundation.id == foundation_id and Foundation.deleted_at is None))
        self.logger.info(f"Found foundation {result.first()}")
        return result.first()
    
    def _insert_foundation(self, session, foundation: Foundation):
        """Insert a new foundation into database"""
        session.add(foundation)
        session.commit()
        session.refresh(foundation)
        self.logger.info(f"Inserted foundation {foundation}")
        return foundation
    
    def _delete_foundation(self, session, foundation_id: int):
        """Delete a foundation from database"""
        foundation_to_delete = session.exec(select(Foundation).where(Foundation.id == foundation_id)).first()
        self.logger.info(f"Foundation to delete: {foundation_to_delete}")
        if foundation_to_delete:
            self.logger.info(f"Deleting foundation {foundation_to_delete.id}")
            foundation_to_delete.deleted_at = datetime.now()
            session.commit()
            return foundation_to_delete
        self.logger.error(f"Foundation {foundation_id} not found")
        return None
    
    def _update_foundation(self, session, foundation_id: int, foundation: Foundation):
        """Update a foundation in database"""
        foundation_to_update = session.exec(select(Foundation).where(Foundation.id == foundation_id)).first()
        self.logger.info(f"Foundation to update: {foundation_to_update}")
        if foundation_to_update:
            self._update_fields(foundation_to_update, foundation)
            session.commit()
            return foundation_to_update
        self.logger.error(f"Foundation {foundation_id} not found")
        return None

    def get_all_with_goals(self):
        return with_db_session(self._fetch_all_foundations_with_goals)
    
    def get_all_with_goals_and_actual_amount(self):
        """Public method to get all foundations with goals and actual amount"""
        return with_db_session(self._get_all_with_goals_and_actual_amount)
    
    def get_all_with_goals_and_actual_amount_native_sql(self):
        """Public method to get all foundations with goals and actual amount using native SQL"""
        return with_db_session(self._get_all_with_goals_and_actual_amount_native_sql)
    
    def _get_all_with_goals_and_actual_amount(self, session):
        """Fetch all foundations with goals and actual amount from database"""
        
        # Crear la query con LEFT JOINs y funciones de agregación
        query = (
            select(
                Foundation.name,
                func.sum(Donation.amount).label('total_amount'),
                GoalCategory.max_amount.label('goal_amount')
            )
            .select_from(Foundation)
            .outerjoin(Goal, Foundation.id == Goal.foundation_id)
            .outerjoin(Donation, Goal.donation_id == Donation.id)
            .outerjoin(GoalCategory, Goal.category_id == GoalCategory.id)
            .group_by(Foundation.name, GoalCategory.max_amount)
        )
        
        result = session.exec(query)
        foundations_data = result.all()
        
        self.logger.info(f"Found {len(foundations_data)} foundations with aggregated data")
        
        # Convertir los resultados a una lista de diccionarios para facilitar el uso
        return [
            {
                'foundation_name': row[0],
                'total_amount': row[1] if row[1] is not None else 0,
                'goal_amount': row[2] if row[2] is not None else 0
            }
            for row in foundations_data
        ]
    
    def _get_all_with_goals_and_actual_amount_native_sql(self, session):
        """Fetch all foundations with goals and actual amount using native SQL"""
        
        # Query SQL nativa exactamente como la tienes en tu archivo
        native_query = text("""
            SELECT 
                f.name,
                SUM(d.amount) AS total_amount,
                gc.max_amount AS goal_amount
            FROM foundations f
            LEFT JOIN goals g ON f.id = g.foundation_id
            LEFT JOIN donations d ON g.donation_id = d.id
            LEFT JOIN goal_categories gc ON g.category_id = gc.id
            GROUP BY f.name, gc.max_amount
        """)
        
        result = session.exec(native_query)
        foundations_data = result.all()
        
        self.logger.info(f"Found {len(foundations_data)} foundations with native SQL")
        
        # Convertir los resultados a una lista de diccionarios
        return [
            {
                'foundation_name': row[0],
                'total_amount': row[1] if row[1] is not None else 0,
                'goal_amount': row[2] if row[2] is not None else 0
            }
            for row in foundations_data
        ]
from models.models import Donation, Goal
from database import with_db_session
from repositories.base_repository import BaseRepository
from repositories.queries import queries
from exeptions.exeption import QueryNotFoundError
from sqlalchemy import text

class DonationRepository(BaseRepository):
    
    def create(self, donation: Donation, goal_category_id: int, foundation_id: int, description: str):
        """
        Create a donation and its associated goal in a single transaction
        """
        def _create_in_transaction(session):
            # Create donation
            session.add(donation)
            session.commit()
            session.refresh(donation)
            self.logger.info(f"Donation created: {donation}")
            # Create goal
            goal = Goal(
                description=description,
                category_id=goal_category_id,
                foundation_id=foundation_id,
                donation_id=donation.id
            )
            session.add(goal)
            session.commit()
            self.logger.info(f"Goal created: {goal}")
            return donation

        return with_db_session(_create_in_transaction) 
    
    def get_donors_by_foundation_id(self, foundation_id: int):
        """
        Get all donors by foundation id
        """
        return with_db_session(lambda session: self._get_donors_by_foundation_id_native_sql(session, foundation_id))
    
    def _get_donors_by_foundation_id_native_sql(self, session, foundation_id: int):
        """Get all donors by foundation id using native SQL"""
        native_query = queries.get('get_donors_by_foundation_id')
        if native_query is None:
            raise QueryNotFoundError("get_donors_by_foundation_id")
        result = session.exec(text(native_query), params={'foundation_id': foundation_id})
        donors_data = result.all()
        return [
            {
                'person_name': row[0],
                'amount': row[1]
            }
            for row in donors_data
        ]


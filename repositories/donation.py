from models.models import Donation, Goal
from database import with_db_session
from datetime import datetime
from repositories.base_repository import BaseRepository

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

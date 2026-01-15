"""Staff service for employee management."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from core.logger import setup_logger
from memory import Staff, StaffSchema

logger = setup_logger(__name__)


class StaffService:
    """Service for managing staff members."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_staff(self, staff: StaffSchema) -> Staff:
        """Create a new staff member."""
        try:
            db_staff = Staff(
                id=str(uuid.uuid4()),
                name=staff.name,
                role=staff.role,
                email=staff.email,
                phone=staff.phone,
                hire_date=staff.hire_date,
                status=staff.status,
                performance_rating=staff.performance_rating,
            )
            self.db.add(db_staff)
            self.db.commit()
            self.db.refresh(db_staff)
            logger.info(f"Created staff member: {db_staff.name}")
            return db_staff
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating staff: {e}")
            raise

    def get_staff(self, staff_id: str) -> Optional[Staff]:
        """Get staff member by ID."""
        try:
            return self.db.query(Staff).filter(Staff.id == staff_id).first()
        except Exception as e:
            logger.error(f"Error getting staff {staff_id}: {e}")
            return None

    def get_staff_by_name(self, name: str) -> Optional[Staff]:
        """Get staff member by name."""
        try:
            return self.db.query(Staff).filter(
                Staff.name.ilike(f"%{name}%")
            ).first()
        except Exception as e:
            logger.error(f"Error getting staff by name: {e}")
            return None

    def get_all_staff(self, status: Optional[str] = None) -> List[Staff]:
        """Get all staff members, optionally filtered by status."""
        try:
            query = self.db.query(Staff)
            if status:
                query = query.filter(Staff.status == status)
            return query.order_by(Staff.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting all staff: {e}")
            return []

    def get_staff_by_role(self, role: str) -> List[Staff]:
        """Get staff members by role."""
        try:
            return self.db.query(Staff).filter(Staff.role == role).all()
        except Exception as e:
            logger.error(f"Error getting staff by role {role}: {e}")
            return []

    def update_staff(self, staff_id: str, staff: StaffSchema) -> Optional[Staff]:
        """Update staff member details."""
        try:
            db_staff = self.db.query(Staff).filter(Staff.id == staff_id).first()
            if not db_staff:
                logger.warning(f"Staff not found: {staff_id}")
                return None

            db_staff.name = staff.name
            db_staff.role = staff.role
            db_staff.email = staff.email
            db_staff.phone = staff.phone
            db_staff.status = staff.status
            db_staff.performance_rating = staff.performance_rating

            self.db.commit()
            self.db.refresh(db_staff)
            logger.info(f"Updated staff: {staff_id}")
            return db_staff
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating staff {staff_id}: {e}")
            raise

    def update_performance(
        self,
        staff_id: str,
        rating: float,
    ) -> Optional[Staff]:
        """Update staff performance rating."""
        try:
            db_staff = self.db.query(Staff).filter(Staff.id == staff_id).first()
            if not db_staff:
                logger.warning(f"Staff not found: {staff_id}")
                return None

            if not 0.0 <= rating <= 5.0:
                raise ValueError("Rating must be between 0.0 and 5.0")

            db_staff.performance_rating = rating
            self.db.commit()
            self.db.refresh(db_staff)
            logger.info(f"Updated performance rating for {staff_id}: {rating}")
            return db_staff
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating performance: {e}")
            raise

    def delete_staff(self, staff_id: str) -> bool:
        """Delete a staff member."""
        try:
            db_staff = self.db.query(Staff).filter(Staff.id == staff_id).first()
            if not db_staff:
                logger.warning(f"Staff not found: {staff_id}")
                return False

            self.db.delete(db_staff)
            self.db.commit()
            logger.info(f"Deleted staff: {staff_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting staff {staff_id}: {e}")
            raise

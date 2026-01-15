"""Customer service for customer management."""

import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from core.logger import setup_logger
from memory import Customer, CustomerSchema

logger = setup_logger(__name__)


class CustomerService:
    """Service for managing customers."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_customer(self, customer: CustomerSchema) -> Customer:
        """Create a new customer."""
        try:
            db_customer = Customer(
                id=str(uuid.uuid4()),
                name=customer.name,
                email=customer.email,
                phone=customer.phone,
                address=customer.address,
                total_purchases=customer.total_purchases,
                purchase_count=customer.purchase_count,
            )
            self.db.add(db_customer)
            self.db.commit()
            self.db.refresh(db_customer)
            logger.info(f"Created customer: {db_customer.name}")
            return db_customer
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating customer: {e}")
            raise

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        try:
            return self.db.query(Customer).filter(Customer.id == customer_id).first()
        except Exception as e:
            logger.error(f"Error getting customer {customer_id}: {e}")
            return None

    def get_customer_by_name(self, name: str) -> Optional[Customer]:
        """Get customer by name."""
        try:
            return self.db.query(Customer).filter(
                Customer.name.ilike(f"%{name}%")
            ).first()
        except Exception as e:
            logger.error(f"Error getting customer by name: {e}")
            return None

    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        try:
            return self.db.query(Customer).order_by(Customer.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting all customers: {e}")
            return []

    def update_customer(self, customer_id: str, customer: CustomerSchema) -> Optional[Customer]:
        """Update customer details."""
        try:
            db_customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
            if not db_customer:
                logger.warning(f"Customer not found: {customer_id}")
                return None

            db_customer.name = customer.name
            db_customer.email = customer.email
            db_customer.phone = customer.phone
            db_customer.address = customer.address

            self.db.commit()
            self.db.refresh(db_customer)
            logger.info(f"Updated customer: {customer_id}")
            return db_customer
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating customer {customer_id}: {e}")
            raise

    def record_purchase(
        self,
        customer_id: str,
        amount: float,
    ) -> Optional[Customer]:
        """Record a purchase for a customer."""
        try:
            db_customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
            if not db_customer:
                logger.warning(f"Customer not found: {customer_id}")
                return None

            db_customer.total_purchases += amount
            db_customer.purchase_count += 1
            db_customer.last_purchase_date = datetime.utcnow()

            self.db.commit()
            self.db.refresh(db_customer)
            logger.info(f"Recorded purchase for customer {customer_id}: {amount}")
            return db_customer
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error recording purchase: {e}")
            raise

    def get_top_customers(self, limit: int = 10) -> List[Customer]:
        """Get top customers by purchase amount."""
        try:
            return self.db.query(Customer).order_by(
                Customer.total_purchases.desc()
            ).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting top customers: {e}")
            return []

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer."""
        try:
            db_customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
            if not db_customer:
                logger.warning(f"Customer not found: {customer_id}")
                return False

            self.db.delete(db_customer)
            self.db.commit()
            logger.info(f"Deleted customer: {customer_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting customer {customer_id}: {e}")
            raise

"""Order/Transaction service for sales management."""

import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from core.logger import setup_logger
from memory import Transaction, TransactionSchema

logger = setup_logger(__name__)


class OrderService:
    """Service for managing transactions and orders."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_transaction(
        self,
        transaction: TransactionSchema,
    ) -> Transaction:
        """Create a new transaction."""
        try:
            db_transaction = Transaction(
                id=str(uuid.uuid4()),
                customer_id=transaction.customer_id,
                customer_name=transaction.customer_name,
                items=transaction.items,
                subtotal=transaction.subtotal,
                tax=transaction.tax,
                total=transaction.total,
                payment_method=transaction.payment_method,
                notes=transaction.notes,
            )
            self.db.add(db_transaction)
            self.db.commit()
            self.db.refresh(db_transaction)
            logger.info(f"Created transaction: {db_transaction.id} - Total: {db_transaction.total}")
            return db_transaction
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating transaction: {e}")
            raise

    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID."""
        try:
            return self.db.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()
        except Exception as e:
            logger.error(f"Error getting transaction {transaction_id}: {e}")
            return None

    def get_all_transactions(self, limit: int = 100) -> List[Transaction]:
        """Get all transactions, newest first."""
        try:
            return self.db.query(Transaction).order_by(
                Transaction.created_at.desc()
            ).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting all transactions: {e}")
            return []

    def get_customer_transactions(self, customer_id: str) -> List[Transaction]:
        """Get all transactions for a customer."""
        try:
            return self.db.query(Transaction).filter(
                Transaction.customer_id == customer_id
            ).order_by(Transaction.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting customer transactions: {e}")
            return []

    def get_transactions_by_date(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Transaction]:
        """Get transactions within a date range."""
        try:
            return self.db.query(Transaction).filter(
                Transaction.created_at >= start_date,
                Transaction.created_at <= end_date,
            ).order_by(Transaction.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting transactions by date: {e}")
            return []

    def calculate_daily_sales(self) -> float:
        """Calculate total sales for today."""
        try:
            from datetime import date
            today = date.today()
            transactions = self.db.query(Transaction).filter(
                Transaction.created_at >= datetime.combine(today, datetime.min.time()),
                Transaction.created_at <= datetime.combine(today, datetime.max.time()),
            ).all()
            
            return sum(t.total for t in transactions)
        except Exception as e:
            logger.error(f"Error calculating daily sales: {e}")
            return 0.0

    def get_payment_method_breakdown(self) -> dict:
        """Get sales breakdown by payment method."""
        try:
            transactions = self.db.query(Transaction).all()
            breakdown = {}
            
            for t in transactions:
                method = t.payment_method
                if method not in breakdown:
                    breakdown[method] = 0.0
                breakdown[method] += t.total
            
            return breakdown
        except Exception as e:
            logger.error(f"Error getting payment method breakdown: {e}")
            return {}

    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction."""
        try:
            db_transaction = self.db.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()
            if not db_transaction:
                logger.warning(f"Transaction not found: {transaction_id}")
                return False

            self.db.delete(db_transaction)
            self.db.commit()
            logger.info(f"Deleted transaction: {transaction_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting transaction {transaction_id}: {e}")
            raise

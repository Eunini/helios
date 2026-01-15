"""State store for persistent business state."""

import uuid
from datetime import datetime
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from core.logger import setup_logger
from .business_model import BusinessMetrics

logger = setup_logger(__name__)


class StateStore:
    """Manages persistent business state in database."""

    def __init__(self, db: Session):
        """Initialize state store with database session."""
        self.db = db

    def record_metrics(
        self,
        total_cash: float,
        total_inventory_value: float,
        daily_sales: float = 0.0,
        daily_transactions: int = 0,
        period: str = "today",
    ) -> str:
        """Record business metrics snapshot."""
        try:
            metrics = BusinessMetrics(
                id=str(uuid.uuid4()),
                total_cash=total_cash,
                total_inventory_value=total_inventory_value,
                daily_sales=daily_sales,
                daily_transactions=daily_transactions,
                period=period,
            )
            self.db.add(metrics)
            self.db.commit()
            logger.info(f"Recorded metrics for period: {period}")
            return metrics.id
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error recording metrics: {e}")
            raise

    def get_latest_metrics(self, period: str = "today") -> Optional[Dict[str, Any]]:
        """Get latest recorded metrics."""
        try:
            metrics = self.db.query(BusinessMetrics).filter(
                BusinessMetrics.period == period
            ).order_by(BusinessMetrics.recorded_at.desc()).first()
            
            if metrics:
                return {
                    "total_cash": metrics.total_cash,
                    "total_inventory_value": metrics.total_inventory_value,
                    "daily_sales": metrics.daily_sales,
                    "daily_transactions": metrics.daily_transactions,
                    "recorded_at": metrics.recorded_at,
                }
            return None
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return None

    def get_metrics_history(
        self,
        period: str = "today",
        limit: int = 24,
    ) -> list[Dict[str, Any]]:
        """Get historical metrics."""
        try:
            metrics_list = self.db.query(BusinessMetrics).filter(
                BusinessMetrics.period == period
            ).order_by(BusinessMetrics.recorded_at.desc()).limit(limit).all()
            
            return [
                {
                    "total_cash": m.total_cash,
                    "total_inventory_value": m.total_inventory_value,
                    "daily_sales": m.daily_sales,
                    "daily_transactions": m.daily_transactions,
                    "recorded_at": m.recorded_at,
                }
                for m in metrics_list
            ]
        except Exception as e:
            logger.error(f"Error getting metrics history: {e}")
            return []

    def calculate_inventory_value(self, db: Session) -> float:
        """Calculate total inventory value."""
        from .business_model import Product
        
        try:
            total = 0.0
            products = db.query(Product).all()
            for product in products:
                total += product.price * product.quantity
            return total
        except Exception as e:
            logger.error(f"Error calculating inventory value: {e}")
            return 0.0

    def calculate_total_cash(self, db: Session) -> float:
        """Calculate total cash from transactions."""
        from .business_model import Transaction
        
        try:
            result = db.query(Transaction).all()
            if not result:
                return 0.0
            
            total = sum(t.total for t in result)
            return total
        except Exception as e:
            logger.error(f"Error calculating cash: {e}")
            return 0.0

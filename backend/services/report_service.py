"""Report service for business intelligence."""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core.logger import setup_logger
from memory import Transaction, Product, Customer, Staff
from typing import Dict, Any

logger = setup_logger(__name__)


class ReportService:
    """Service for generating business reports and analytics."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def get_daily_summary(self, date: datetime = None) -> Dict[str, Any]:
        """Get daily business summary."""
        if date is None:
            date = datetime.utcnow().date()
        
        try:
            start = datetime.combine(date, datetime.min.time())
            end = datetime.combine(date, datetime.max.time())

            transactions = self.db.query(Transaction).filter(
                Transaction.created_at >= start,
                Transaction.created_at <= end,
            ).all()

            total_sales = sum(t.total for t in transactions)
            transaction_count = len(transactions)
            avg_transaction = total_sales / transaction_count if transaction_count > 0 else 0

            return {
                "date": date.isoformat(),
                "total_sales": total_sales,
                "transaction_count": transaction_count,
                "average_transaction": avg_transaction,
                "total_tax_collected": sum(t.tax for t in transactions),
            }
        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")
            return {}

    def get_weekly_summary(self, weeks_back: int = 0) -> Dict[str, Any]:
        """Get weekly business summary."""
        try:
            today = datetime.utcnow().date()
            start_date = today - timedelta(days=today.weekday() + (weeks_back * 7))
            end_date = start_date + timedelta(days=6)

            start = datetime.combine(start_date, datetime.min.time())
            end = datetime.combine(end_date, datetime.max.time())

            transactions = self.db.query(Transaction).filter(
                Transaction.created_at >= start,
                Transaction.created_at <= end,
            ).all()

            total_sales = sum(t.total for t in transactions)
            transaction_count = len(transactions)

            return {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_sales": total_sales,
                "transaction_count": transaction_count,
                "average_daily_sales": total_sales / 7 if transaction_count > 0 else 0,
            }
        except Exception as e:
            logger.error(f"Error generating weekly summary: {e}")
            return {}

    def get_inventory_report(self) -> Dict[str, Any]:
        """Get detailed inventory report."""
        try:
            products = self.db.query(Product).all()
            
            total_items = sum(p.quantity for p in products)
            total_value = sum(p.price * p.quantity for p in products)
            
            low_stock = [p for p in products if p.quantity <= p.reorder_level]
            out_of_stock = [p for p in products if p.quantity == 0]

            return {
                "total_products": len(products),
                "total_items": total_items,
                "total_value": total_value,
                "low_stock_count": len(low_stock),
                "out_of_stock_count": len(out_of_stock),
                "low_stock_items": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "quantity": p.quantity,
                        "reorder_level": p.reorder_level,
                    }
                    for p in low_stock[:10]
                ],
            }
        except Exception as e:
            logger.error(f"Error generating inventory report: {e}")
            return {}

    def get_customer_report(self) -> Dict[str, Any]:
        """Get detailed customer report."""
        try:
            customers = self.db.query(Customer).all()
            
            total_revenue = sum(c.total_purchases for c in customers)
            avg_revenue_per_customer = total_revenue / len(customers) if customers else 0

            top_customers = sorted(
                customers,
                key=lambda c: c.total_purchases,
                reverse=True
            )[:10]

            return {
                "total_customers": len(customers),
                "total_revenue": total_revenue,
                "average_customer_value": avg_revenue_per_customer,
                "top_customers": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "total_purchases": c.total_purchases,
                        "purchase_count": c.purchase_count,
                    }
                    for c in top_customers
                ],
            }
        except Exception as e:
            logger.error(f"Error generating customer report: {e}")
            return {}

    def get_staff_report(self) -> Dict[str, Any]:
        """Get detailed staff report."""
        try:
            staff_members = self.db.query(Staff).all()
            
            by_role = {}
            for staff in staff_members:
                if staff.role not in by_role:
                    by_role[staff.role] = []
                by_role[staff.role].append(staff)

            avg_rating = sum(s.performance_rating for s in staff_members) / len(staff_members) if staff_members else 0

            return {
                "total_staff": len(staff_members),
                "average_performance_rating": avg_rating,
                "staff_by_role": {
                    role: [
                        {
                            "id": s.id,
                            "name": s.name,
                            "performance_rating": s.performance_rating,
                            "status": s.status,
                        }
                        for s in staff_list
                    ]
                    for role, staff_list in by_role.items()
                },
            }
        except Exception as e:
            logger.error(f"Error generating staff report: {e}")
            return {}

    def get_comprehensive_report(self) -> Dict[str, Any]:
        """Get comprehensive business report."""
        try:
            return {
                "generated_at": datetime.utcnow().isoformat(),
                "daily_summary": self.get_daily_summary(),
                "inventory": self.get_inventory_report(),
                "customers": self.get_customer_report(),
                "staff": self.get_staff_report(),
            }
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return {}

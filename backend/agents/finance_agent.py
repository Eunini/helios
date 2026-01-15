"""Finance agent for financial tracking and reporting."""

from typing import Dict, Any
import uuid
from agents.base_agent import BaseAgent
from core.logger import setup_logger

logger = setup_logger(__name__)


class FinanceAgent(BaseAgent):
    """Agent for managing financial operations."""

    def __init__(self):
        """Initialize finance agent."""
        super().__init__(
            name="FinanceAgent",
            description="Manages financial tracking and cash flow"
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute financial task.

        Args:
            task: Task containing financial details

        Returns:
            Execution result with financial status
        """
        task_id = task.get("id", str(uuid.uuid4()))
        description = task.get("description", "")

        try:
            logger.info(f"FinanceAgent executing: {description}")

            # Retrieve financial context
            context = self.retrieve_business_context(description, n_results=5)

            # Process financial transaction
            finance_result = self._process_financial_transaction(description, context)

            # Store transaction in memory
            self.store_memory(
                content=f"Financial Transaction: {description}\nResult: {finance_result}",
                memory_type="financial_transaction",
                metadata={"task_id": task_id, "transaction_type": finance_result.get("type")},
            )

            self.log_execution(
                task_id=task_id,
                task_description=description,
                status="completed",
                result=finance_result,
            )

            return {
                "status": "completed",
                "transaction": finance_result,
                "message": finance_result.get("message", "Transaction processed"),
            }

        except Exception as e:
            logger.error(f"Error in FinanceAgent: {e}")
            self.log_execution(
                task_id=task_id,
                task_description=description,
                status="failed",
                error=str(e),
            )
            return {
                "status": "failed",
                "error": str(e),
            }

    def _process_financial_transaction(self, description: str, context: list) -> Dict[str, Any]:
        """Process financial transaction."""
        description_lower = description.lower()

        # Sales transaction
        if any(word in description_lower for word in ["sale", "sold", "purchase", "buy"]):
            return self._process_sale(description)

        # Payment
        elif any(word in description_lower for word in ["payment", "paid", "refund"]):
            return self._process_payment(description)

        # Expense
        elif any(word in description_lower for word in ["expense", "cost", "spent"]):
            return self._process_expense(description)

        else:
            return {
                "type": "general_transaction",
                "message": f"Financial transaction processed: {description}",
                "details": {},
            }

    def _process_sale(self, description: str) -> Dict[str, Any]:
        """Process sales transaction."""
        return {
            "type": "sale",
            "message": f"Sale recorded: {description}",
            "details": {
                "category": "revenue",
                "status": "recorded",
            },
        }

    def _process_payment(self, description: str) -> Dict[str, Any]:
        """Process payment."""
        return {
            "type": "payment",
            "message": f"Payment processed: {description}",
            "details": {
                "category": "cash_flow",
                "status": "processed",
            },
        }

    def _process_expense(self, description: str) -> Dict[str, Any]:
        """Process expense."""
        return {
            "type": "expense",
            "message": f"Expense recorded: {description}",
            "details": {
                "category": "expense",
                "status": "recorded",
            },
        }

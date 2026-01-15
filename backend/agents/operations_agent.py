"""Operations agent for inventory and logistics management."""

from typing import Dict, Any, Optional
import uuid
from agents.base_agent import BaseAgent
from core.logger import setup_logger

logger = setup_logger(__name__)


class OperationsAgent(BaseAgent):
    """Agent for managing operations and inventory."""

    def __init__(self):
        """Initialize operations agent."""
        super().__init__(
            name="OperationsAgent",
            description="Manages inventory and daily operations"
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute operational task.

        Args:
            task: Task containing operation details

        Returns:
            Execution result with status and details
        """
        task_id = task.get("id", str(uuid.uuid4()))
        description = task.get("description", "")

        try:
            logger.info(f"OperationsAgent executing: {description}")

            # Retrieve relevant business context
            context = self.retrieve_business_context(description, n_results=5)

            # Determine operation type and execute
            operation_result = self._execute_operation(description, context)

            # Store result in memory
            self.store_memory(
                content=f"Operation: {description}\nResult: {operation_result}",
                memory_type="operation_execution",
                metadata={"task_id": task_id, "operation_type": operation_result.get("type")},
            )

            self.log_execution(
                task_id=task_id,
                task_description=description,
                status="completed",
                result=operation_result,
            )

            return {
                "status": "completed",
                "operation": operation_result,
                "message": operation_result.get("message", "Operation completed"),
            }

        except Exception as e:
            logger.error(f"Error in OperationsAgent: {e}")
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

    def _execute_operation(self, description: str, context: list) -> Dict[str, Any]:
        """Execute operation based on description."""
        description_lower = description.lower()

        # Inventory operations
        if any(word in description_lower for word in ["add", "receive", "stock", "inventory"]):
            return self._process_inventory_addition(description)

        # Stock operations
        elif any(word in description_lower for word in ["remove", "sold", "sale", "transaction"]):
            return self._process_stock_removal(description)

        # General operations
        else:
            return {
                "type": "general",
                "message": f"Operation processed: {description}",
                "details": {},
            }

    def _process_inventory_addition(self, description: str) -> Dict[str, Any]:
        """Process inventory addition operation."""
        # Example: "Add 50 bottles of Coke, N100 each from supplier ABC"
        return {
            "type": "inventory_addition",
            "message": f"Processed inventory addition: {description}",
            "details": {
                "action": "add",
                "status": "pending_confirmation",
            },
        }

    def _process_stock_removal(self, description: str) -> Dict[str, Any]:
        """Process stock removal operation."""
        # Example: "Sold 10 units of product X"
        return {
            "type": "stock_removal",
            "message": f"Processed stock removal: {description}",
            "details": {
                "action": "remove",
                "status": "pending_confirmation",
            },
        }

"""Communications agent for customer and staff interactions."""

from typing import Dict, Any
import uuid
from agents.base_agent import BaseAgent
from core.logger import setup_logger

logger = setup_logger(__name__)


class CommunicationsAgent(BaseAgent):
    """Agent for managing communications."""

    def __init__(self):
        """Initialize communications agent."""
        super().__init__(
            name="CommunicationsAgent",
            description="Manages customer and staff communications"
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute communications task.

        Args:
            task: Task containing communication details

        Returns:
            Execution result with communication status
        """
        task_id = task.get("id", str(uuid.uuid4()))
        description = task.get("description", "")

        try:
            logger.info(f"CommunicationsAgent executing: {description}")

            # Retrieve communication context
            context = self.retrieve_business_context(description, n_results=5)

            # Process communication
            comm_result = self._process_communication(description, context)

            # Store in memory
            self.store_memory(
                content=f"Communication: {description}\nResult: {comm_result}",
                memory_type="communication",
                metadata={"task_id": task_id, "comm_type": comm_result.get("type")},
            )

            self.log_execution(
                task_id=task_id,
                task_description=description,
                status="completed",
                result=comm_result,
            )

            return {
                "status": "completed",
                "communication": comm_result,
                "message": comm_result.get("message", "Communication processed"),
            }

        except Exception as e:
            logger.error(f"Error in CommunicationsAgent: {e}")
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

    def _process_communication(self, description: str, context: list) -> Dict[str, Any]:
        """Process communication based on type."""
        description_lower = description.lower()

        # Customer communication
        if any(word in description_lower for word in ["customer", "client", "notify"]):
            return self._process_customer_communication(description)

        # Staff communication
        elif any(word in description_lower for word in ["staff", "employee", "alert", "notify staff"]):
            return self._process_staff_communication(description)

        else:
            return {
                "type": "general_communication",
                "message": f"Communication processed: {description}",
                "details": {},
            }

    def _process_customer_communication(self, description: str) -> Dict[str, Any]:
        """Process customer communication."""
        return {
            "type": "customer_communication",
            "message": f"Customer communication queued: {description}",
            "details": {
                "target": "customer",
                "status": "queued",
                "channels": ["sms", "email"],
            },
        }

    def _process_staff_communication(self, description: str) -> Dict[str, Any]:
        """Process staff communication."""
        return {
            "type": "staff_communication",
            "message": f"Staff alert issued: {description}",
            "details": {
                "target": "staff",
                "status": "issued",
                "channels": ["in_app", "email"],
            },
        }

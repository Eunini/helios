"""Insight agent for analytics and recommendations."""

from typing import Dict, Any
import uuid
from agents.base_agent import BaseAgent
from core.logger import setup_logger

logger = setup_logger(__name__)


class InsightAgent(BaseAgent):
    """Agent for analyzing business data and providing insights."""

    def __init__(self):
        """Initialize insight agent."""
        super().__init__(
            name="InsightAgent",
            description="Provides analytics and business insights"
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute insight task.

        Args:
            task: Task containing analysis details

        Returns:
            Execution result with insights and recommendations
        """
        task_id = task.get("id", str(uuid.uuid4()))
        description = task.get("description", "")

        try:
            logger.info(f"InsightAgent executing: {description}")

            # Retrieve business context
            context = self.retrieve_business_context(description, n_results=10)

            # Generate insights
            insights = self._generate_insights(description, context)

            # Store insights in memory
            self.store_memory(
                content=f"Business Insights: {description}\nInsights: {insights}",
                memory_type="business_insight",
                metadata={"task_id": task_id, "insight_type": insights.get("type")},
            )

            self.log_execution(
                task_id=task_id,
                task_description=description,
                status="completed",
                result=insights,
            )

            return {
                "status": "completed",
                "insights": insights,
                "message": insights.get("message", "Insights generated"),
            }

        except Exception as e:
            logger.error(f"Error in InsightAgent: {e}")
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

    def _generate_insights(self, description: str, context: list) -> Dict[str, Any]:
        """Generate business insights."""
        description_lower = description.lower()

        # Sales insights
        if any(word in description_lower for word in ["sales", "revenue", "performance"]):
            return self._analyze_sales(description, context)

        # Inventory insights
        elif any(word in description_lower for word in ["inventory", "stock", "product"]):
            return self._analyze_inventory(description, context)

        # Customer insights
        elif any(word in description_lower for word in ["customer", "trend", "behavior"]):
            return self._analyze_customers(description, context)

        else:
            return {
                "type": "general_analysis",
                "message": f"Business analysis: {description}",
                "recommendations": [],
                "details": {},
            }

    def _analyze_sales(self, description: str, context: list) -> Dict[str, Any]:
        """Analyze sales data."""
        return {
            "type": "sales_analysis",
            "message": f"Sales performance analysis: {description}",
            "recommendations": [
                "Monitor peak sales hours for staffing optimization",
                "Consider promotions during low-demand periods",
                "Analyze product mix for cross-selling opportunities",
            ],
            "details": {
                "metric": "sales_performance",
                "trend": "analysis_pending",
            },
        }

    def _analyze_inventory(self, description: str, context: list) -> Dict[str, Any]:
        """Analyze inventory data."""
        return {
            "type": "inventory_analysis",
            "message": f"Inventory analysis: {description}",
            "recommendations": [
                "Review reorder levels for fast-moving items",
                "Consider supplier consolidation to reduce costs",
                "Implement ABC analysis for inventory management",
            ],
            "details": {
                "metric": "inventory_health",
                "status": "analysis_pending",
            },
        }

    def _analyze_customers(self, description: str, context: list) -> Dict[str, Any]:
        """Analyze customer data."""
        return {
            "type": "customer_analysis",
            "message": f"Customer analysis: {description}",
            "recommendations": [
                "Develop loyalty program for repeat customers",
                "Target high-value customer segments with promotions",
                "Implement customer feedback system for continuous improvement",
            ],
            "details": {
                "metric": "customer_satisfaction",
                "status": "analysis_pending",
            },
        }

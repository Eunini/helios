"""Planner agent for high-level task planning."""

from typing import Dict, Any, List
import json
from agents.base_agent import BaseAgent
from core.logger import setup_logger

logger = setup_logger(__name__)


class PlannerAgent(BaseAgent):
    """Agent responsible for planning and agent coordination."""

    def __init__(self):
        """Initialize planner agent."""
        super().__init__(
            name="PlannerAgent",
            description="Plans tasks and coordinates other agents"
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze task and determine which agents are needed.

        Args:
            task: Task with description and context

        Returns:
            Plan with recommended agents and execution steps
        """
        task_id = task.get("id", "unknown")
        description = task.get("description", "")

        try:
            logger.info(f"PlannerAgent analyzing task: {description}")

            # Get context from memory
            context = self.retrieve_business_context(description, n_results=3)

            # Use LLM to plan the task
            prompt = self._build_planning_prompt(description, context)
            response = self.llm.invoke(prompt)
            
            # Parse the response
            plan = self._parse_plan(response.content)

            # Store the plan in memory
            self.store_memory(
                content=f"Task Plan: {description}\n\nPlan: {json.dumps(plan)}",
                memory_type="task_plan",
                metadata={"task_id": task_id},
            )

            self.log_execution(
                task_id=task_id,
                task_description=description,
                status="completed",
                result=plan,
            )

            return {
                "status": "completed",
                "plan": plan,
                "agents_needed": plan.get("agents", []),
                "execution_steps": plan.get("steps", []),
            }

        except Exception as e:
            logger.error(f"Error in PlannerAgent: {e}")
            self.log_execution(
                task_id=task_id,
                task_description=description,
                status="failed",
                error=str(e),
            )
            return {
                "status": "failed",
                "error": str(e),
                "plan": None,
            }

    def _build_planning_prompt(self, task_description: str, context: List[Dict]) -> str:
        """Build prompt for LLM planning."""
        context_text = "\n".join([
            f"- {doc['content'][:200]}" for doc in context
        ]) if context else "No previous context available"

        return f"""
You are a business planning expert. Analyze the following task and determine which agents should handle it.

TASK: {task_description}

BUSINESS CONTEXT:
{context_text}

AVAILABLE AGENTS:
1. OperationsAgent - Manages inventory and logistics
2. FinanceAgent - Handles financial transactions and accounting
3. CommunicationsAgent - Manages customer and staff communications
4. InsightAgent - Provides analytics and recommendations

Please respond with a JSON object containing:
{{
    "agents": ["Agent1", "Agent2"],
    "steps": ["Step 1", "Step 2"],
    "priority": "high/normal/low",
    "estimated_time": "minutes",
    "risks": ["Risk 1", "Risk 2"]
}}

Respond ONLY with valid JSON, no additional text.
"""

    def _parse_plan(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into plan structure."""
        try:
            # Extract JSON from response
            import json
            
            # Try direct parse
            plan = json.loads(response)
            return plan
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            logger.warning("Could not parse plan response as JSON, using fallback")
            return {
                "agents": ["OperationsAgent"],
                "steps": ["Process the task"],
                "priority": "normal",
                "estimated_time": "5",
                "risks": [],
            }

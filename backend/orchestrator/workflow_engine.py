"""Workflow engine for coordinating complex agent workflows."""

from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from core.logger import setup_logger

logger = setup_logger(__name__)


class WorkflowEngine:
    """Engine for orchestrating complex multi-agent workflows."""

    def __init__(self):
        """Initialize workflow engine."""
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def create_workflow(
        self,
        workflow_id: str,
        steps: List[Dict[str, Any]],
        description: str = "",
    ) -> str:
        """
        Create a new workflow.

        Args:
            workflow_id: Unique workflow identifier
            steps: List of workflow steps
            description: Workflow description

        Returns:
            Workflow ID
        """
        self.workflows[workflow_id] = {
            "id": workflow_id,
            "description": description,
            "steps": steps,
            "status": "created",
            "created_at": datetime.utcnow(),
            "executed_at": None,
        }

        logger.info(f"Workflow created: {workflow_id}")
        return workflow_id

    def execute_workflow(
        self,
        workflow_id: str,
        context: Dict[str, Any],
        executor: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Execute a workflow.

        Args:
            workflow_id: Workflow to execute
            context: Execution context
            executor: Optional custom executor function

        Returns:
            Workflow execution result
        """
        if workflow_id not in self.workflows:
            logger.error(f"Workflow not found: {workflow_id}")
            return {"status": "failed", "error": "Workflow not found"}

        workflow = self.workflows[workflow_id]

        try:
            logger.info(f"Executing workflow: {workflow_id}")
            workflow["status"] = "executing"
            workflow["executed_at"] = datetime.utcnow()

            results = []
            for step in workflow["steps"]:
                step_result = self._execute_step(step, context, executor)
                results.append(step_result)

                if not step_result.get("success", False):
                    logger.error(f"Workflow step failed: {step.get('name')}")
                    workflow["status"] = "failed"
                    return {
                        "status": "failed",
                        "workflow_id": workflow_id,
                        "error": f"Step failed: {step.get('name')}",
                        "results": results,
                    }

            workflow["status"] = "completed"
            logger.info(f"Workflow completed: {workflow_id}")

            execution_record = {
                "workflow_id": workflow_id,
                "status": "completed",
                "executed_at": datetime.utcnow(),
                "results": results,
            }
            self.execution_history.append(execution_record)

            return {
                "status": "completed",
                "workflow_id": workflow_id,
                "results": results,
            }

        except Exception as e:
            logger.error(f"Workflow execution error: {e}")
            workflow["status"] = "failed"
            return {
                "status": "failed",
                "workflow_id": workflow_id,
                "error": str(e),
            }

    def _execute_step(
        self,
        step: Dict[str, Any],
        context: Dict[str, Any],
        executor: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """Execute a single workflow step."""
        step_name = step.get("name", "unknown")
        logger.debug(f"Executing step: {step_name}")

        try:
            if executor:
                # Use custom executor if provided
                result = executor(step, context)
            else:
                # Default step execution
                result = {
                    "step": step_name,
                    "success": True,
                    "result": step.get("default_result", {}),
                }

            result["success"] = result.get("success", True)
            return result

        except Exception as e:
            logger.error(f"Step execution failed: {step_name} - {e}")
            return {
                "step": step_name,
                "success": False,
                "error": str(e),
            }

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow details."""
        return self.workflows.get(workflow_id)

    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows."""
        return list(self.workflows.values())

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent execution history."""
        return self.execution_history[-limit:]

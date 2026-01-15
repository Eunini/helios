"""Task manager for coordinating agent execution."""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque
from sqlalchemy.orm import Session
from core.logger import setup_logger
from core.config import get_settings
from memory.business_model import Task
from agents import (
    PlannerAgent,
    OperationsAgent,
    FinanceAgent,
    CommunicationsAgent,
    InsightAgent,
)

logger = setup_logger(__name__)


class TaskManager:
    """Manages task queue and agent coordination."""

    def __init__(self, db: Session):
        """Initialize task manager."""
        self.db = db
        self.settings = get_settings()
        self.task_queue: deque = deque()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.completed_tasks: Dict[str, Dict[str, Any]] = {}

        # Register agents
        self.agents = {
            "PlannerAgent": PlannerAgent(),
            "OperationsAgent": OperationsAgent(),
            "FinanceAgent": FinanceAgent(),
            "CommunicationsAgent": CommunicationsAgent(),
            "InsightAgent": InsightAgent(),
        }

        logger.info("TaskManager initialized with agents")

    def submit_task(self, description: str, priority: str = "normal") -> str:
        """
        Submit a new task to the queue.

        Args:
            description: Task description
            priority: Task priority (low, normal, high, critical)

        Returns:
            Task ID
        """
        if len(self.task_queue) >= self.settings.MAX_TASK_QUEUE_SIZE:
            logger.warning("Task queue is full")
            raise RuntimeError("Task queue is full")

        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "result": None,
            "error": None,
        }

        # Store in database
        try:
            db_task = Task(
                id=task_id,
                description=description,
                priority=priority,
                status="pending",
            )
            self.db.add(db_task)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error storing task in database: {e}")
            self.db.rollback()

        # Add to queue (high priority tasks go to front)
        if priority == "critical":
            self.task_queue.appendleft(task)
        else:
            self.task_queue.append(task)

        logger.info(f"Task submitted: {task_id} - {description}")
        return task_id

    def process_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Process the next task in the queue.

        Returns:
            Task result or None if queue is empty
        """
        if not self.task_queue:
            logger.debug("Task queue is empty")
            return None

        task = self.task_queue.popleft()
        task_id = task["id"]

        logger.info(f"Processing task: {task_id}")
        self.active_tasks[task_id] = task

        try:
            # Step 1: Use PlannerAgent to plan the task
            planner = self.agents["PlannerAgent"]
            plan_result = planner.execute(task)

            if plan_result["status"] != "completed":
                raise Exception(f"Planning failed: {plan_result.get('error')}")

            plan = plan_result.get("plan", {})
            agents_to_use = plan.get("agents", ["OperationsAgent"])

            # Step 2: Execute with appropriate agents
            execution_results = []
            for agent_name in agents_to_use:
                if agent_name in self.agents:
                    agent = self.agents[agent_name]
                    result = agent.execute(task)
                    execution_results.append({
                        "agent": agent_name,
                        "result": result,
                    })

            # Step 3: Aggregate results
            task["status"] = "completed"
            task["result"] = {
                "plan": plan,
                "execution_results": execution_results,
            }

            # Update database
            self._update_task_status(task_id, "completed", task["result"])

            self.completed_tasks[task_id] = task
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]

            logger.info(f"Task completed: {task_id}")
            return task

        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            task["status"] = "failed"
            task["error"] = str(e)

            # Update database
            self._update_task_status(task_id, "failed", error=str(e))

            self.completed_tasks[task_id] = task
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]

            return task

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a task."""
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        elif task_id in self.completed_tasks:
            return self.completed_tasks[task_id]
        else:
            # Check database
            try:
                db_task = self.db.query(Task).filter(Task.id == task_id).first()
                if db_task:
                    return {
                        "id": db_task.id,
                        "description": db_task.description,
                        "status": db_task.status,
                        "result": db_task.result,
                        "error": db_task.error,
                    }
            except Exception as e:
                logger.error(f"Error getting task status: {e}")

        return None

    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall queue and task status."""
        return {
            "queue_size": len(self.task_queue),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "agents": list(self.agents.keys()),
        }

    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent."""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            return {
                "name": agent.name,
                "id": agent.id,
                "description": agent.description,
                "execution_history": agent.get_execution_history()[-10:],  # Last 10
            }
        return None

    def _update_task_status(
        self,
        task_id: str,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        """Update task status in database."""
        try:
            db_task = self.db.query(Task).filter(Task.id == task_id).first()
            if db_task:
                db_task.status = status
                db_task.result = result
                db_task.error = error
                self.db.commit()
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            self.db.rollback()

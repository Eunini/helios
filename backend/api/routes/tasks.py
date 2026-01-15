"""Task endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core import get_db, logger
from memory import TaskSchema
from orchestrator import TaskManager

router = APIRouter()

# Task manager will be injected from main.py
async def get_task_manager(db: Session = Depends(get_db)) -> TaskManager:
    """Get task manager instance."""
    from api.main import task_manager
    if not task_manager:
        raise HTTPException(status_code=500, detail="Task manager not initialized")
    return task_manager


@router.post("/", response_model=TaskSchema)
async def submit_task(
    description: str,
    priority: str = "normal",
    task_manager: TaskManager = Depends(get_task_manager),
):
    """Submit a new task."""
    try:
        task_id = task_manager.submit_task(description, priority)
        return {
            "id": task_id,
            "description": description,
            "priority": priority,
            "status": "pending",
        }
    except Exception as e:
        logger.error(f"Error submitting task: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: str,
    task_manager: TaskManager = Depends(get_task_manager),
):
    """Get task status and details."""
    task = task_manager.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/process-next")
async def process_next_task(
    task_manager: TaskManager = Depends(get_task_manager),
):
    """Process the next task in queue."""
    try:
        task = task_manager.process_next_task()
        if not task:
            return {"status": "queue_empty", "message": "No tasks in queue"}
        return task
    except Exception as e:
        logger.error(f"Error processing task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queue/status")
async def get_queue_status(
    task_manager: TaskManager = Depends(get_task_manager),
):
    """Get queue and task status."""
    return task_manager.get_queue_status()

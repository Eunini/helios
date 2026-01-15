"""Agent management endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from core import logger
from api.main import task_manager

router = APIRouter()


@router.get("/")
async def list_agents():
    """List all available agents."""
    if not task_manager:
        raise HTTPException(status_code=500, detail="Task manager not initialized")
    
    agents_info = []
    for agent_name, agent in task_manager.agents.items():
        agents_info.append({
            "name": agent.name,
            "id": agent.id,
            "description": agent.description,
        })
    
    return {"agents": agents_info}


@router.get("/{agent_name}")
async def get_agent_status(
    agent_name: str,
):
    """Get status of a specific agent."""
    if not task_manager:
        raise HTTPException(status_code=500, detail="Task manager not initialized")
    
    status = task_manager.get_agent_status(agent_name)
    if not status:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_name}")
    
    return status


@router.get("/queue/status")
async def get_queue_status():
    """Get overall queue and agent status."""
    if not task_manager:
        raise HTTPException(status_code=500, detail="Task manager not initialized")
    
    return task_manager.get_queue_status()

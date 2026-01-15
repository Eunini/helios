"""Tests for agents."""

import pytest
from agents import (
    PlannerAgent,
    OperationsAgent,
    FinanceAgent,
    CommunicationsAgent,
    InsightAgent,
)


def test_planner_agent_initialization():
    """Test planner agent initialization."""
    agent = PlannerAgent()
    assert agent.name == "PlannerAgent"
    assert agent.id is not None


def test_operations_agent_initialization():
    """Test operations agent initialization."""
    agent = OperationsAgent()
    assert agent.name == "OperationsAgent"
    assert agent.id is not None


def test_finance_agent_initialization():
    """Test finance agent initialization."""
    agent = FinanceAgent()
    assert agent.name == "FinanceAgent"
    assert agent.id is not None


def test_communications_agent_initialization():
    """Test communications agent initialization."""
    agent = CommunicationsAgent()
    assert agent.name == "CommunicationsAgent"
    assert agent.id is not None


def test_insight_agent_initialization():
    """Test insight agent initialization."""
    agent = InsightAgent()
    assert agent.name == "InsightAgent"
    assert agent.id is not None


@pytest.mark.asyncio
async def test_operations_agent_execution():
    """Test operations agent execution."""
    agent = OperationsAgent()
    task = {
        "id": "test-task-1",
        "description": "Add 50 bottles of Coke, N100 each",
    }
    
    result = agent.execute(task)
    assert result["status"] == "completed"
    assert "operation" in result


@pytest.mark.asyncio
async def test_finance_agent_execution():
    """Test finance agent execution."""
    agent = FinanceAgent()
    task = {
        "id": "test-task-2",
        "description": "Record sale of 10 units, total N5000",
    }
    
    result = agent.execute(task)
    assert result["status"] == "completed"
    assert "transaction" in result

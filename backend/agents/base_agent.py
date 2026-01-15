"""Base agent class for autonomous operation."""

import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from core.logger import setup_logger
from core.config import get_settings
from memory.vector_store import get_vector_store

logger = setup_logger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, name: str, description: str = ""):
        """Initialize agent with name and description."""
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.settings = get_settings()
        self.vector_store = get_vector_store()
        self.execution_history: List[Dict[str, Any]] = []

        # Initialize LLM
        self.llm = self._init_llm()

    def _init_llm(self):
        """Initialize language model."""
        try:
            if self.settings.ANTHROPIC_API_KEY:
                return ChatAnthropic(
                    model=self.settings.LLM_MODEL,
                    temperature=self.settings.LLM_TEMPERATURE,
                    max_tokens=self.settings.LLM_MAX_TOKENS,
                )
            elif self.settings.GOOGLE_API_KEY:
                return ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    temperature=self.settings.LLM_TEMPERATURE,
                )
            else:
                raise ValueError("No LLM API key configured")
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            raise

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task. Must be implemented by subclasses.

        Args:
            task: Task dictionary with description and parameters

        Returns:
            Result dictionary with outcome and status
        """
        pass

    def retrieve_business_context(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant business context from memory."""
        try:
            if not self.settings.ENABLE_VECTOR_STORE:
                return []
            
            results = self.vector_store.search(query, n_results=n_results)
            logger.debug(f"Retrieved {len(results)} context documents for: {query}")
            return results
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []

    def store_memory(
        self,
        content: str,
        memory_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Store information in vector memory."""
        try:
            if not self.settings.ENABLE_VECTOR_STORE:
                return None

            meta = {
                "type": memory_type,
                "agent": self.name,
                "timestamp": datetime.utcnow().isoformat(),
                **(metadata or {}),
            }
            
            doc_id = self.vector_store.add_document(content, meta)
            logger.debug(f"Stored memory: {memory_type} -> {doc_id}")
            return doc_id
        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return None

    def log_execution(
        self,
        task_id: str,
        task_description: str,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        """Log execution details."""
        execution_record = {
            "task_id": task_id,
            "task_description": task_description,
            "status": status,
            "result": result,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.execution_history.append(execution_record)
        
        if status == "completed":
            logger.info(f"Agent {self.name} completed task {task_id}")
        elif status == "failed":
            logger.error(f"Agent {self.name} failed task {task_id}: {error}")

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get agent's execution history."""
        return self.execution_history

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"

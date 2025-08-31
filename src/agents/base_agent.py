import logging
from datetime import datetime
from typing import Any, Dict


class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.logger = self._setup_logger()
        self.context_manager = ContextManager()
        self.memory_store = MemoryStore()

    def _setup_logger(self):
        """Setup logger for the agent"""
        logger = logging.getLogger(f"Agent.{self.name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def handle(self, task: str) -> str:
        """
        Handle task with context and memory management

        Args:
            task: Task description or data

        Returns:
            Result string
        """
        try:
            self.logger.info(f"Handling task: {task}")

            # Create task context
            task_context = {
                "task": task,
                "timestamp": datetime.now().isoformat(),
                "agent": self.name,
            }

            # Add to history
            self.context_manager.add_to_history(task_context)

            # Check memory for relevant information
            relevant_memories = self._retrieve_relevant_memories(task)
            task_context["memories"] = relevant_memories

            # Process task with context
            result = self._process_with_context(task, task_context)

            # Store result in memory
            self._store_memory(task, result, task_context)

            # Update context
            self.context_manager.update_context(f"last_{self.name}_result", result)

            self.logger.info(f"Task handled successfully: {task}")
            return result

        except Exception as e:
            error_msg = f"Error in {self.name} handling task '{task}': {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return f"[{self.name}] Error: {str(e)}"

    def _process_with_context(self, task: str, context: dict) -> str:
        """
        Process task with context - to be implemented by subclasses

        Args:
            task: Task description
            context: Context information

        Returns:
            Result string
        """
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

    def _retrieve_relevant_memories(self, task: str) -> list:
        """
        Retrieve relevant memories for task

        Args:
            task: Task description

        Returns:
            List of relevant memories
        """
        # Simple keyword-based memory retrieval
        # In a real implementation, this would use RAG or similar techniques
        keywords = task.lower().split()
        relevant_memories = []

        for keyword in keywords:
            memories = self.memory_store.retrieve_by_keyword(keyword)
            relevant_memories.extend(memories)

        # Return unique memories, limit to 5
        unique_memories = []
        seen = set()
        for memory in relevant_memories:
            memory_id = memory.get("id")
            if memory_id not in seen:
                unique_memories.append(memory)
                seen.add(memory_id)
                if len(unique_memories) >= 5:
                    break

        return unique_memories

    def _store_memory(self, task: str, result: str, context: dict):
        """
        Store interaction in memory

        Args:
            task: Task description
            result: Task result
            context: Context information
        """
        memory_item = {
            "agent": self.name,
            "task": task,
            "result": result,
            "context": context,
            "timestamp": datetime.now().isoformat(),
        }

        self.memory_store.store(memory_item)
        self.logger.debug(f"Stored memory for task: {task}")


class ContextManager:
    """Simple context manager for agents"""

    def __init__(self, max_history: int = 50):
        self.context = {}
        self.history = []
        self.max_history = max_history

    def update_context(self, key: str, value: any):
        """Update context with new information"""
        self.context[key] = value

    def add_to_history(self, interaction: dict):
        """Add interaction to history"""
        self.history.append(interaction)
        # Maintain history size limit
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]

    def get_context(self) -> dict:
        """Get current context"""
        return self.context.copy()

    def get_history(self) -> list:
        """Get interaction history"""
        return self.history.copy()


class MemoryStore:
    """Simple memory storage for agents"""

    def __init__(self):
        self.memories = []
        self.keyword_index = {}

    def store(self, memory_item: dict):
        """
        Store memory item

        Args:
            memory_item: Memory item to store
        """
        # Add ID if not present
        if "id" not in memory_item:
            import uuid

            memory_item["id"] = str(uuid.uuid4())

        self.memories.append(memory_item)

        # Index by keywords
        self._index_memory(memory_item)

    def _index_memory(self, memory_item: dict):
        """Index memory by keywords"""
        task = memory_item.get("task", "").lower()
        result = memory_item.get("result", "").lower()
        content = task + " " + result

        # Extract keywords (simple approach)
        words = content.split()
        keywords = [
            word for word in words if len(word) > 3
        ]  # Words longer than 3 characters

        for keyword in keywords:
            if keyword not in self.keyword_index:
                self.keyword_index[keyword] = []
            self.keyword_index[keyword].append(memory_item)

    def retrieve_by_keyword(self, keyword: str) -> list:
        """
        Retrieve memories by keyword

        Args:
            keyword: Keyword to search for

        Returns:
            List of matching memories
        """
        keyword_lower = keyword.lower()
        return self.keyword_index.get(keyword_lower, [])

    def retrieve_recent(self, limit: int = 10) -> list:
        """
        Retrieve most recent memories

        Args:
            limit: Maximum number of memories to retrieve

        Returns:
            List of recent memories
        """
        return self.memories[-limit:] if self.memories else []

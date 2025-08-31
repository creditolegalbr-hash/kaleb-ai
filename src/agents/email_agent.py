# src/agents/email_agent.py

from .base_agent import BaseAgent


class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmailAgent")

    def _process_with_context(self, task: str, context: dict) -> str:
        # Use context and memories to enhance response
        memories = context.get("memories", [])
        memory_context = "\n".join(
            [
                f"Previous interaction: {mem.get('task', '')} -> {mem.get('result', '')}"
                for mem in memories[:3]  # Use top 3 memories
            ]
        )

        if memory_context:
            return f"[{self.name}] Processando email: {task}\nContexto relevante:\n{memory_context}"
        else:
            return f"[{self.name}] Processando email: {task}"

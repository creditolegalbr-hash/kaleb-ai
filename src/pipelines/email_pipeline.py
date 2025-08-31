from agents.email_agent import EmailAgent

from .base_pipeline import BasePipeline


class EmailPipeline(BasePipeline):
    def __init__(self):
        super().__init__("EmailPipeline")
        self.email_agent = EmailAgent()
        self.add_step(self.process_email)
        self.add_step(self.analyze_content)
        self.add_step(self.determine_action)
        self.add_step(self.execute_action)

    def process_email(self, data: dict) -> dict:
        # Process raw email data
        # Extract subject, body, sender, etc.
        result = self.email_agent.handle(data.get("task", ""))
        data["processed_email"] = result
        return data

    def analyze_content(self, data: dict) -> dict:
        # Send to NLP/RAG system
        # Extract key information, sentiment, intent
        # For now, we'll simulate this with basic keyword analysis
        task = data.get("task", "").lower()
        if "urgent" in task or "asap" in task:
            data["priority"] = "high"
        elif "later" in task or "tomorrow" in task:
            data["priority"] = "low"
        else:
            data["priority"] = "normal"
        return data

    def determine_action(self, data: dict) -> dict:
        # Based on analysis, determine next action
        # Options: reply, classify, forward, archive
        task = data.get("task", "").lower()
        if "reply" in task or "respond" in task:
            data["action"] = "reply"
        elif "forward" in task:
            data["action"] = "forward"
        elif "archive" in task or "file" in task:
            data["action"] = "archive"
        else:
            data["action"] = "classify"
        return data

    def execute_action(self, data: dict) -> dict:
        # Execute the determined action
        action = data.get("action", "classify")
        if action == "reply":
            data["result"] = f"Auto-replied to email: {data.get('task', '')}"
        elif action == "forward":
            data["result"] = f"Forwarded email: {data.get('task', '')}"
        elif action == "archive":
            data["result"] = f"Archived email: {data.get('task', '')}"
        else:
            data["result"] = f"Classified email: {data.get('task', '')}"
        return data

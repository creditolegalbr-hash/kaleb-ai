from agents.support_agent import SupportAgent

from .base_pipeline import BasePipeline


class SupportPipeline(BasePipeline):
    def __init__(self):
        super().__init__("SupportPipeline")
        self.support_agent = SupportAgent()
        self.add_step(self.receive_request)
        self.add_step(self.triage_request)
        self.add_step(self.respond_or_escalate)
        self.add_step(self.create_ticket)

    def receive_request(self, data: dict) -> dict:
        # Handle incoming support request
        data["request_received"] = True
        data["reception_time"] = self._get_current_time()
        return data

    def triage_request(self, data: dict) -> dict:
        # Use SupportAgent to triage
        task = data.get("task", "")
        triage_result = self.support_agent.handle(f"Triage support request: {task}")
        data["triage_result"] = triage_result

        # Determine priority and category
        priority, category = self._determine_priority_and_category(task)
        data["priority"] = priority
        data["category"] = category

        return data

    def respond_or_escalate(self, data: dict) -> dict:
        # Automatically respond or escalate
        priority = data.get("priority", "low")
        category = data.get("category", "general")

        if priority == "high" or category in ["technical", "security"]:
            data["action"] = "escalate"
            data["response"] = (
                f"Escalating {category} issue with {priority} priority to specialist team"
            )
        else:
            data["action"] = "respond"
            data["response"] = self._generate_auto_response(category, priority)

        return data

    def create_ticket(self, data: dict) -> dict:
        # Create ticket in support system
        data["ticket_created"] = True
        data["ticket_id"] = self._generate_ticket_id()
        data["ticket_details"] = {
            "id": data["ticket_id"],
            "priority": data.get("priority", "low"),
            "category": data.get("category", "general"),
            "status": "open",
            "created_at": data.get("reception_time", self._get_current_time()),
        }
        return data

    def _get_current_time(self) -> str:
        from datetime import datetime

        return datetime.now().isoformat()

    def _generate_ticket_id(self) -> str:
        import uuid

        return "TICKET-" + str(uuid.uuid4())[:8].upper()

    def _determine_priority_and_category(self, task: str) -> tuple:
        task_lower = task.lower()

        # Determine priority
        if any(
            word in task_lower
            for word in ["urgent", "asap", "emergency", "critical", "immediately"]
        ):
            priority = "high"
        elif any(word in task_lower for word in ["soon", "later", "whenever"]):
            priority = "low"
        else:
            priority = "medium"

        # Determine category
        if any(word in task_lower for word in ["password", "login", "account"]):
            category = "account"
        elif any(word in task_lower for word in ["error", "bug", "crash", "technical"]):
            category = "technical"
        elif any(word in task_lower for word in ["security", "hack", "breach"]):
            category = "security"
        elif any(word in task_lower for word in ["billing", "payment", "invoice"]):
            category = "billing"
        elif any(word in task_lower for word in ["feature", "request", "suggestion"]):
            category = "feature"
        else:
            category = "general"

        return priority, category

    def _generate_auto_response(self, category: str, priority: str) -> str:
        responses = {
            "account": "We've received your account issue and are working on it. Please check your email for further instructions.",
            "technical": "Our technical team has been notified about your issue. We'll contact you as soon as we have a solution.",
            "billing": "We've forwarded your billing inquiry to our finance team. They will contact you within 24 hours.",
            "feature": "Thank you for your feature suggestion. We've added it to our development roadmap.",
            "general": "We've received your request and will respond as soon as possible.",
        }

        base_response = responses.get(category, responses["general"])
        priority_note = ""
        if priority == "high":
            priority_note = (
                " This is marked as high priority and will be addressed immediately."
            )
        elif priority == "low":
            priority_note = " This will be addressed in our regular support cycle."

        return base_response + priority_note

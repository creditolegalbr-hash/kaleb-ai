from agents.scheduler_agent import SchedulerAgent

from .base_pipeline import BasePipeline


class SchedulerPipeline(BasePipeline):
    def __init__(self):
        super().__init__("SchedulerPipeline")
        self.scheduler_agent = SchedulerAgent()
        self.add_step(self.receive_request)
        self.add_step(self.check_availability)
        self.add_step(self.create_event)
        self.add_step(self.send_invitation)

    def receive_request(self, data: dict) -> dict:
        # Parse meeting request details
        task = data.get("task", "")
        data["request_received"] = True
        data["meeting_details"] = self._parse_meeting_request(task)
        return data

    def check_availability(self, data: dict) -> dict:
        # Use SchedulerAgent to check calendar
        meeting_details = data.get("meeting_details", {})
        availability_check = self.scheduler_agent.handle(
            f"Check availability for {meeting_details.get('time', 'requested time')}"
        )
        data["availability"] = availability_check
        data["is_available"] = "available" in availability_check.lower()
        return data

    def create_event(self, data: dict) -> dict:
        # Create event in Google Calendar (simulated)
        if data.get("is_available", False):
            meeting_details = data.get("meeting_details", {})
            event_creation = self.scheduler_agent.handle(
                f"Create event: {meeting_details.get('title', 'Meeting')} at {meeting_details.get('time', 'requested time')}"
            )
            data["event_created"] = True
            data["event_details"] = event_creation
        else:
            data["event_created"] = False
            data["error"] = "No available time slot"
        return data

    def send_invitation(self, data: dict) -> dict:
        # Send invitation to participants
        if data.get("event_created", False):
            participants = data.get("meeting_details", {}).get("participants", [])
            if participants:
                data["invitation_sent"] = True
                data["invitation_details"] = (
                    f"Invitations sent to {', '.join(participants)}"
                )
            else:
                data["invitation_sent"] = False
                data["invitation_details"] = "No participants specified"
        else:
            data["invitation_sent"] = False
            data["invitation_details"] = "Event not created, invitation not sent"
        return data

    def _parse_meeting_request(self, task: str) -> dict:
        # Simple parsing of meeting request (in real implementation, this would use NLP)
        import re

        # Extract time
        time_pattern = r"(\d{1,2}[:\d]{2}?\s*(?:AM|PM|am|pm)?)"
        times = re.findall(time_pattern, task)
        meeting_time = times[0] if times else "unknown time"

        # Extract participants (emails)
        email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
        participants = re.findall(email_pattern, task)

        # Extract title (keywords after "meeting" or "discuss")
        title_keywords = []
        if "meeting" in task.lower():
            parts = task.lower().split("meeting")
            if len(parts) > 1:
                title_keywords = parts[1].strip().split()[:5]  # First 5 words
        elif "discuss" in task.lower():
            parts = task.lower().split("discuss")
            if len(parts) > 1:
                title_keywords = parts[1].strip().split()[:5]  # First 5 words

        title = " ".join(title_keywords) if title_keywords else "General Meeting"

        return {"title": title, "time": meeting_time, "participants": participants}

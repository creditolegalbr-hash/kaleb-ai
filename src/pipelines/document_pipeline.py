from agents.document_agent import DocumentAgent

from .base_pipeline import BasePipeline


class DocumentPipeline(BasePipeline):
    def __init__(self):
        super().__init__("DocumentPipeline")
        self.document_agent = DocumentAgent()
        self.add_step(self.receive_document)
        self.add_step(self.process_content)
        self.add_step(self.classify_document)
        self.add_step(self.store_document)
        self.add_step(self.extract_metadata)

    def receive_document(self, data: dict) -> dict:
        # Handle incoming document
        data["document_received"] = True
        data["reception_time"] = self._get_current_time()
        return data

    def process_content(self, data: dict) -> dict:
        # Use DocumentAgent to process
        task = data.get("task", "")
        processing_result = self.document_agent.handle(
            f"Process document content: {task}"
        )
        data["processing_result"] = processing_result
        return data

    def classify_document(self, data: dict) -> dict:
        # Classify document type
        task = data.get("task", "").lower()
        if "contract" in task or "agreement" in task:
            doc_type = "contract"
        elif "invoice" in task or "bill" in task:
            doc_type = "invoice"
        elif "report" in task:
            doc_type = "report"
        elif "email" in task:
            doc_type = "email"
        else:
            doc_type = "general"

        data["document_type"] = doc_type
        data["classification_confidence"] = 0.95  # Simulated confidence score
        return data

    def store_document(self, data: dict) -> dict:
        # Store in appropriate location
        doc_type = data.get("document_type", "general")
        storage_paths = {
            "contract": "contracts/",
            "invoice": "invoices/",
            "report": "reports/",
            "email": "emails/",
            "general": "documents/",
        }

        storage_path = storage_paths.get(doc_type, "documents/")
        data["storage_path"] = storage_path
        data["stored"] = True
        data["document_id"] = self._generate_document_id()
        return data

    def extract_metadata(self, data: dict) -> dict:
        # Extract document metadata
        task = data.get("task", "")
        metadata = {
            "title": self._extract_title(task),
            "author": self._extract_author(task),
            "keywords": self._extract_keywords(task),
            "page_count": self._estimate_page_count(task),
            "file_size": self._estimate_file_size(task),
        }
        data["metadata"] = metadata
        return data

    def _get_current_time(self) -> str:
        from datetime import datetime

        return datetime.now().isoformat()

    def _generate_document_id(self) -> str:
        import uuid

        return str(uuid.uuid4())

    def _extract_title(self, task: str) -> str:
        # Simple title extraction
        words = task.split()
        if len(words) > 5:
            return " ".join(words[:5]) + "..."
        return task

    def _extract_author(self, task: str) -> str:
        # Simple author extraction (in real implementation, this would use NLP)
        authors = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown"]
        for author in authors:
            if author.split()[0].lower() in task.lower():
                return author
        return "Unknown Author"

    def _extract_keywords(self, task: str) -> list:
        # Simple keyword extraction
        common_words = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
        }
        words = task.lower().split()
        keywords = [
            word for word in words if word not in common_words and len(word) > 3
        ]
        return list(set(keywords))[:10]  # Return unique keywords, max 10

    def _estimate_page_count(self, task: str) -> int:
        # Simple page count estimation
        word_count = len(task.split())
        # Roughly 250 words per page
        return max(1, word_count // 250)

    def _estimate_file_size(self, task: str) -> str:
        # Simple file size estimation
        char_count = len(task)
        # Roughly 1KB per 1000 characters
        size_kb = char_count // 1000
        return f"{max(1, size_kb)} KB"

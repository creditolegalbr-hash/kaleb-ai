from agents.document_agent import DocumentAgent
from agents.finance_agent import FinanceAgent

from .base_pipeline import BasePipeline


class FinancePipeline(BasePipeline):
    def __init__(self):
        super().__init__("FinancePipeline")
        self.finance_agent = FinanceAgent()
        self.document_agent = DocumentAgent()
        self.add_step(self.receive_document)
        self.add_step(self.extract_data)
        self.add_step(self.validate_data)
        self.add_step(self.store_data)
        self.add_step(self.generate_report)

    def receive_document(self, data: dict) -> dict:
        # Handle incoming financial document
        data["document_received"] = True
        data["document_type"] = "financial"
        return data

    def extract_data(self, data: dict) -> dict:
        # Use DocumentAgent with OCR/NLP
        # For simulation, we'll extract basic financial data
        task = data.get("task", "")
        result = self.document_agent.handle(f"Extract financial data from: {task}")
        data["extracted_data"] = {
            "document_processed": result,
            "amount": self._extract_amount(task),
            "vendor": self._extract_vendor(task),
            "date": self._extract_date(task),
        }
        return data

    def validate_data(self, data: dict) -> dict:
        # Use FinanceAgent to validate
        extracted_data = data.get("extracted_data", {})
        validation_result = self.finance_agent.handle(
            f"Validate financial data: {extracted_data}"
        )
        data["validation_result"] = validation_result
        data["is_valid"] = "valid" in validation_result.lower()
        return data

    def store_data(self, data: dict) -> dict:
        # Store in database or spreadsheet
        # For simulation, we'll just mark it as stored
        if data.get("is_valid", False):
            data["stored"] = True
            data["storage_location"] = "financial_database"
        else:
            data["stored"] = False
            data["error"] = "Invalid data, not stored"
        return data

    def generate_report(self, data: dict) -> dict:
        # Generate automatic financial report
        if data.get("stored", False):
            data["report"] = (
                f"Financial report generated for {data.get('extracted_data', {}).get('vendor', 'unknown vendor')}"
            )
        else:
            data["report"] = "No report generated due to validation errors"
        return data

    def _extract_amount(self, task: str) -> str:
        # Simple amount extraction (in real implementation, this would use NLP/OCR)
        import re

        amounts = re.findall(r"\$\d+(?:\.\d+)?", task)
        return amounts[0] if amounts else "unknown"

    def _extract_vendor(self, task: str) -> str:
        # Simple vendor extraction
        vendors = ["Amazon", "Google", "Microsoft", "Apple", "Samsung"]
        for vendor in vendors:
            if vendor.lower() in task.lower():
                return vendor
        return "unknown vendor"

    def _extract_date(self, task: str) -> str:
        # Simple date extraction
        import re

        dates = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", task)
        return dates[0] if dates else "unknown date"

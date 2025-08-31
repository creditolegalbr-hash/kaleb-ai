import logging
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAdapter(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.service_name = config.get("service_name")
        self.base_url = config.get("base_url")
        self.auth_type = config.get("auth_type", "none")
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Setup logger for the adapter"""
        logger = logging.getLogger(f"Adapter.{self.service_name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    @abstractmethod
    def execute(self, request: dict) -> dict:
        """
        Execute request to external service

        Args:
            request: Request data

        Returns:
            Response data
        """
        pass

    def _prepare_request(self, request: dict) -> dict:
        """Prepare request with authentication and headers"""
        # Add authentication
        auth_headers = self._get_auth_headers()
        if "headers" not in request:
            request["headers"] = {}
        request["headers"].update(auth_headers)

        # Add default headers
        request["headers"]["User-Agent"] = "IntelligentAutomation/1.0"

        return request

    def _get_auth_headers(self) -> dict:
        """Get authentication headers"""
        if self.auth_type == "api_key":
            return {"Authorization": f'Bearer {self.config["api_key"]}'}
        elif self.auth_type == "basic":
            # Implement basic auth
            pass
        return {}

    def _handle_response(self, response: dict) -> dict:
        """Handle and process response"""
        if response.get("status_code", 200) >= 400:
            raise Exception(f"Request failed: {response.get('error')}")
        return response.get("data", {})

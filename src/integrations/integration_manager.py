import logging
from typing import Any, Dict

from .base_adapter import BaseAdapter


class IntegrationManager:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.adapters = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Setup logger for the integration manager"""
        logger = logging.getLogger("IntegrationManager")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def register_adapter(self, service_name: str, adapter: BaseAdapter):
        """Register integration adapter"""
        self.adapters[service_name] = adapter
        self.logger.info(f"Registered adapter for service: {service_name}")

    def get_adapter(self, service_name: str) -> BaseAdapter:
        """Get registered adapter by service name"""
        return self.adapters.get(service_name)

    def execute_request(self, service_name: str, request: dict) -> dict:
        """Execute request through integration adapter"""
        adapter = self.get_adapter(service_name)
        if not adapter:
            error_msg = f"No adapter registered for service: {service_name}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            self.logger.info(f"Executing request for service: {service_name}")
            result = adapter.execute(request)
            self.logger.info(
                f"Request completed successfully for service: {service_name}"
            )
            return result
        except Exception as e:
            error_msg = f"Error executing request for service {service_name}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise Exception(error_msg)

    def is_service_enabled(self, service_name: str) -> bool:
        """Check if service is enabled in configuration"""
        service_config = self.config.get("integrations", {}).get(service_name, {})
        return service_config.get("enabled", False)

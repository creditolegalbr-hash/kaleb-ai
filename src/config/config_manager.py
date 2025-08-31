import logging
import os
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    def __init__(self, config_paths: list = None):
        self.config_paths = config_paths or ["config/default.yaml"]
        self.config = {}
        self.logger = self._setup_logger()
        self._load_configuration()

    def _setup_logger(self):
        """Setup logger for the config manager"""
        logger = logging.getLogger("ConfigManager")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _load_configuration(self):
        """Load configuration from all sources"""
        for path in self.config_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        config_data = yaml.safe_load(file) or {}
                        # Merge with existing configuration
                        self.config = self._merge_configs(self.config, config_data)
                        self.logger.info(f"Loaded configuration from {path}")
                except Exception as e:
                    self.logger.error(f"Failed to load configuration from {path}: {e}")
            else:
                self.logger.warning(f"Configuration file not found: {path}")

        self.logger.info("Configuration loading completed")

    def _merge_configs(self, base_config: dict, new_config: dict) -> dict:
        """Merge two configuration dictionaries"""
        merged = base_config.copy()
        for key, value in new_config.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation supported)"""
        keys = key.split(".")
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """Set configuration value by key (dot notation supported)"""
        keys = key.split(".")
        config = self.config

        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value

    def reload(self):
        """Reload configuration from sources"""
        self.config = {}
        self._load_configuration()

    def get_all(self) -> dict:
        """Get all configuration"""
        return self.config.copy()

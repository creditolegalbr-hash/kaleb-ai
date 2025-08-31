# Configuration Management System

## Overview

The configuration management system provides a centralized, secure, and flexible way to manage all configuration settings for the intelligent automation system. This document outlines the design, implementation, and usage of the configuration management framework.

## Configuration Architecture

### Core Components

1. **ConfigManager**: Central configuration manager
2. **ConfigLoader**: Loads configuration from various sources
3. **ConfigValidator**: Validates configuration integrity
4. **ConfigEncryptor**: Handles encryption of sensitive data
5. **EnvironmentManager**: Manages environment-specific configurations
6. **ConfigWatcher**: Monitors configuration changes

### ConfigManager

```python
import os
import yaml
from typing import Any, Dict, Optional

class ConfigManager:
    def __init__(self, config_paths: list = None):
        self.config_paths = config_paths or [
            'config/default.yaml',
            'config/local.yaml',
            'config/secrets.yaml'
        ]
        self.config = {}
        self.environment = os.getenv('AUTOMATION_ENV', 'development')
        self.config_loader = ConfigLoader()
        self.config_validator = ConfigValidator()
        self.config_encryptor = ConfigEncryptor()
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from all sources"""
        for path in self.config_paths:
            if os.path.exists(path):
                config_data = self.config_loader.load(path)
                # Decrypt sensitive data if needed
                if 'secrets' in path:
                    config_data = self.config_encryptor.decrypt_config(config_data)
                # Merge with existing configuration
                self.config = self._merge_configs(self.config, config_data)
        
        # Load environment-specific configuration
        env_config_path = f'config/{self.environment}.yaml'
        if os.path.exists(env_config_path):
            env_config = self.config_loader.load(env_config_path)
            self.config = self._merge_configs(self.config, env_config)
        
        # Validate configuration
        self.config_validator.validate(self.config)
    
    def _merge_configs(self, base_config: dict, new_config: dict) -> dict:
        """Merge two configuration dictionaries"""
        merged = base_config.copy()
        for key, value in new_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation supported)"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (dot notation supported)"""
        keys = key.split('.')
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
    
    def get_environment(self) -> str:
        """Get current environment"""
        return self.environment
```

### ConfigLoader

```python
import yaml
import json
import os
from typing import Dict, Any

class ConfigLoader:
    def load(self, path: str) -> Dict[Any, Any]:
        """Load configuration from file"""
        _, ext = os.path.splitext(path)
        
        with open(path, 'r', encoding='utf-8') as file:
            if ext.lower() in ['.yaml', '.yml']:
                return yaml.safe_load(file) or {}
            elif ext.lower() == '.json':
                return json.load(file)
            else:
                raise ValueError(f"Unsupported configuration format: {ext}")
    
    def save(self, path: str, config: Dict[Any, Any]):
        """Save configuration to file"""
        _, ext = os.path.splitext(path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as file:
            if ext.lower() in ['.yaml', '.yml']:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            elif ext.lower() == '.json':
                json.dump(config, file, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"Unsupported configuration format: {ext}")
```

### ConfigValidator

```python
from typing import Dict, Any
from jsonschema import validate, ValidationError

class ConfigValidator:
    def __init__(self):
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[Any, Any]:
        """Load configuration schema"""
        # This would typically load from a schema file
        return {
            "type": "object",
            "properties": {
                "agents": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "boolean"},
                        "finance": {"type": "boolean"},
                        "scheduler": {"type": "boolean"},
                        "document": {"type": "boolean"},
                        "support": {"type": "boolean"}
                    }
                },
                "integrations": {
                    "type": "object",
                    "properties": {
                        "google_calendar": {"type": "object"},
                        "email_service": {"type": "object"},
                        "database": {"type": "object"},
                        "file_storage": {"type": "object"}
                    }
                },
                "logging": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "string"},
                        "file_path": {"type": "string"},
                        "max_bytes": {"type": "number"},
                        "backup_count": {"type": "number"}
                    }
                }
            }
        }
    
    def validate(self, config: Dict[Any, Any]) -> bool:
        """Validate configuration against schema"""
        try:
            validate(instance=config, schema=self.schema)
            return True
        except ValidationError as e:
            raise ConfigurationException(
                f"Configuration validation failed: {e.message}",
                error_code="CONFIG_VALIDATION_FAILED"
            )
```

### ConfigEncryptor

```python
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class ConfigEncryptor:
    def __init__(self):
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def _get_encryption_key(self) -> bytes:
        """Get encryption key from environment or generate one"""
        key = os.getenv('CONFIG_ENCRYPTION_KEY')
        if key:
            return key.encode()
        else:
            # Generate a key from a password
            password = os.getenv('CONFIG_ENCRYPTION_PASSWORD', 'default_password')
            salt = b'salt_1234567890'  # In production, use a random salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_value(self, value: str) -> str:
        """Encrypt a single value"""
        encrypted_bytes = self.cipher_suite.encrypt(value.encode())
        return base64.urlsafe_b64encode(encrypted_bytes).decode()
    
    def decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt a single value"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode())
        decrypted_bytes = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()
    
    def encrypt_config(self, config: Dict[Any, Any]) -> Dict[Any, Any]:
        """Encrypt sensitive configuration values"""
        encrypted_config = {}
        sensitive_keys = ['password', 'api_key', 'secret', 'token']
        
        for key, value in config.items():
            if isinstance(value, dict):
                encrypted_config[key] = self.encrypt_config(value)
            elif isinstance(value, str) and any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                encrypted_config[key] = self.encrypt_value(value)
            else:
                encrypted_config[key] = value
        
        return encrypted_config
    
    def decrypt_config(self, config: Dict[Any, Any]) -> Dict[Any, Any]:
        """Decrypt sensitive configuration values"""
        decrypted_config = {}
        sensitive_keys = ['password', 'api_key', 'secret', 'token']
        
        for key, value in config.items():
            if isinstance(value, dict):
                decrypted_config[key] = self.decrypt_config(value)
            elif isinstance(value, str) and any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                try:
                    decrypted_config[key] = self.decrypt_value(value)
                except Exception:
                    # If decryption fails, keep original value
                    decrypted_config[key] = value
            else:
                decrypted_config[key] = value
        
        return decrypted_config
```

## Environment Management

### EnvironmentManager

```python
import os
from typing import Dict, Any

class EnvironmentManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.environment = self.config_manager.get_environment()
    
    def get_environment_config(self) -> Dict[Any, Any]:
        """Get environment-specific configuration"""
        return {
            'development': {
                'logging': {
                    'level': 'DEBUG',
                    'console_output': True
                },
                'integrations': {
                    'test_mode': True
                }
            },
            'staging': {
                'logging': {
                    'level': 'INFO',
                    'console_output': False
                },
                'integrations': {
                    'test_mode': False
                }
            },
            'production': {
                'logging': {
                    'level': 'WARNING',
                    'console_output': False
                },
                'integrations': {
                    'test_mode': False
                }
            }
        }.get(self.environment, {})
    
    def is_development(self) -> bool:
        """Check if current environment is development"""
        return self.environment == 'development'
    
    def is_production(self) -> bool:
        """Check if current environment is production"""
        return self.environment == 'production'
    
    def get_database_config(self) -> Dict[Any, Any]:
        """Get environment-specific database configuration"""
        base_config = self.config_manager.get('database', {})
        
        # Override with environment-specific settings
        env_overrides = {
            'development': {
                'host': 'localhost',
                'port': 5432,
                'database': 'automation_dev'
            },
            'staging': {
                'host': 'staging-db.example.com',
                'port': 5432,
                'database': 'automation_staging'
            },
            'production': {
                'host': 'prod-db.example.com',
                'port': 5432,
                'database': 'automation_prod'
            }
        }
        
        env_config = env_overrides.get(self.environment, {})
        return {**base_config, **env_config}
```

## Configuration File Structure

### Default Configuration

```yaml
# config/default.yaml
system:
  name: "Intelligent Automation System"
  version: "1.0.0"
  debug: false

agents:
  email: true
  finance: true
  scheduler: true
  document: true
  support: true

logging:
  level: "INFO"
  file_path: "logs/automation.log"
  max_bytes: 10485760  # 10MB
  backup_count: 5
  console_output: false

error_handling:
  retry:
    max_retries: 3
    backoff_factor: 1.0
    jitter: true
  notifications:
    critical_errors: true

memory:
  context_manager:
    max_history: 100
  memory_store:
    type: "sqlite"
    path: "memory.db"

integrations:
  google_calendar:
    enabled: false
    max_rate_limit: 100
  email_service:
    enabled: false
    max_rate_limit: 50
  database:
    enabled: false
    max_connections: 10
  file_storage:
    enabled: false
    max_rate_limit: 200
```

### Development Configuration

```yaml
# config/development.yaml
system:
  debug: true

logging:
  level: "DEBUG"
  console_output: true

error_handling:
  notifications:
    critical_errors: false

memory:
  memory_store:
    path: "memory_dev.db"

integrations:
  google_calendar:
    enabled: false  # Disable in development
  email_service:
    enabled: false  # Disable in development
  database:
    enabled: true
    host: "localhost"
    port: 5432
    database: "automation_dev"
    username: "dev_user"
    password: "dev_password"
  file_storage:
    enabled: true
    type: "local"
    path: "storage/dev"
```

### Production Configuration

```yaml
# config/production.yaml
system:
  debug: false

logging:
  level: "WARNING"
  console_output: false
  file_path: "/var/log/automation/automation.log"

error_handling:
  notifications:
    critical_errors: true

memory:
  memory_store:
    path: "/var/lib/automation/memory.db"

integrations:
  google_calendar:
    enabled: true
    max_rate_limit: 1000
  email_service:
    enabled: true
    max_rate_limit: 1000
  database:
    enabled: true
    host: "prod-db.internal"
    port: 5432
    database: "automation_prod"
    username: "prod_user"
    # password will be in secrets.yaml
  file_storage:
    enabled: true
    type: "s3"
    bucket: "automation-prod"
    region: "us-east-1"
```

### Secrets Configuration

```yaml
# config/secrets.yaml
# This file should be encrypted or have restricted access
integrations:
  database:
    password: "ENCRYPTED_VALUE_HERE"
  google_calendar:
    client_id: "ENCRYPTED_VALUE_HERE"
    client_secret: "ENCRYPTED_VALUE_HERE"
  email_service:
    api_key: "ENCRYPTED_VALUE_HERE"
  file_storage:
    access_key: "ENCRYPTED_VALUE_HERE"
    secret_key: "ENCRYPTED_VALUE_HERE"
```

## Integration with System Components

### Agent Configuration

```python
class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.config_manager = ConfigManager()
        self.logger = Logger(name, self.config_manager.get('logging', {}))
        
    def is_enabled(self) -> bool:
        """Check if agent is enabled in configuration"""
        return self.config_manager.get(f'agents.{self.name.lower()}', True)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get agent-specific configuration"""
        return self.config_manager.get(f'agents.{self.name.lower()}.{key}', default)

class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmailAgent")
        
        # Check if agent is enabled
        if not self.is_enabled():
            raise ConfigurationException(
                "EmailAgent is disabled in configuration",
                error_code="AGENT_DISABLED"
            )
        
        # Get agent-specific configuration
        self.max_email_size = self.get_config('max_email_size', 10485760)  # 10MB
        self.default_sender = self.get_config('default_sender', 'noreply@example.com')
```

### Integration Configuration

```python
class IntegrationManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.adapters = {}
        self._setup_integrations()
    
    def _setup_integrations(self):
        """Setup integrations based on configuration"""
        integrations_config = self.config_manager.get('integrations', {})
        
        for service_name, service_config in integrations_config.items():
            if service_config.get('enabled', False):
                self._setup_integration(service_name, service_config)
    
    def _setup_integration(self, service_name: str, service_config: dict):
        """Setup specific integration"""
        adapter_map = {
            'google_calendar': GoogleCalendarAdapter,
            'email_service': EmailAdapter,
            'database': DatabaseAdapter,
            'file_storage': FileStorageAdapter
        }
        
        adapter_class = adapter_map.get(service_name)
        if adapter_class:
            adapter = adapter_class(service_config)
            self.adapters[service_name] = adapter
```

## Configuration Change Monitoring

### ConfigWatcher

```python
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigWatcher(FileSystemEventHandler):
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.observer = Observer()
        self._setup_watcher()
    
    def _setup_watcher(self):
        """Setup file system watcher"""
        config_dir = 'config'
        self.observer.schedule(self, config_dir, recursive=False)
        self.observer.start()
    
    def on_modified(self, event):
        """Handle file modification event"""
        if not event.is_directory and event.src_path.endswith(('.yaml', '.yml', '.json')):
            # Add a small delay to ensure file write is complete
            time.sleep(1)
            # Reload configuration
            self.config_manager.reload()
    
    def stop(self):
        """Stop the watcher"""
        self.observer.stop()
        self.observer.join()
```

## Usage Examples

### Basic Configuration Usage

```python
# Initialize configuration manager
config_manager = ConfigManager()

# Get configuration values
log_level = config_manager.get('logging.level', 'INFO')
database_host = config_manager.get('integrations.database.host', 'localhost')

# Set configuration values (runtime changes)
config_manager.set('system.debug', True)

# Get agent-specific configuration
email_enabled = config_manager.get('agents.email', True)
```

### Environment-Specific Configuration

```python
# Set environment via environment variable
# export AUTOMATION_ENV=production

config_manager = ConfigManager()
env_manager = EnvironmentManager(config_manager)

# Get environment-specific database configuration
db_config = env_manager.get_database_config()
print(f"Database host: {db_config['host']}")
```

### Secure Configuration Handling

```python
# Initialize encryptor
config_encryptor = ConfigEncryptor()

# Encrypt sensitive configuration
sensitive_config = {
    'database': {
        'password': 'my_secret_password'
    }
}

encrypted_config = config_encryptor.encrypt_config(sensitive_config)
# Store encrypted_config in secrets.yaml

# Decrypt configuration
decrypted_config = config_encryptor.decrypt_config(encrypted_config)
```

### Configuration Validation

```python
# Initialize validator
config_validator = ConfigValidator()

# Validate configuration
try:
    config_validator.validate(config_manager.config)
    print("Configuration is valid")
except ConfigurationException as e:
    print(f"Configuration error: {e}")
```

## Best Practices

### 1. Configuration Organization
- Separate default, environment-specific, and secret configurations
- Use clear, descriptive key names
- Group related settings under common namespaces

### 2. Security
- Never store secrets in version control
- Encrypt sensitive configuration values
- Use environment variables for critical secrets
- Restrict file permissions on configuration files

### 3. Environment Management
- Use consistent environment names (development, staging, production)
- Override settings appropriately for each environment
- Test configuration changes in non-production environments

### 4. Validation
- Validate configuration at startup
- Provide clear error messages for invalid configuration
- Use schema validation for complex configurations

### 5. Monitoring
- Monitor configuration changes in production
- Log configuration access for security auditing
- Alert on unauthorized configuration changes

## Benefits

1. **Flexibility**: Easy to configure for different environments
2. **Security**: Secure handling of sensitive configuration data
3. **Maintainability**: Centralized configuration management
4. **Reliability**: Configuration validation prevents runtime errors
5. **Scalability**: Supports complex configuration hierarchies
6. **Observability**: Configuration change monitoring and logging
7. **Portability**: Environment-independent configuration structure
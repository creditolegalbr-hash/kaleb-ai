# Error Handling and Logging Framework

## Overview

A comprehensive error handling and logging framework is essential for maintaining a robust and maintainable intelligent automation system. This document outlines the design and implementation of error handling patterns, logging strategies, and monitoring capabilities.

## Error Handling Architecture

### Core Components

1. **ErrorHandler**: Centralized error handling manager
2. **CustomExceptions**: Domain-specific exception classes
3. **ErrorContext**: Contextual information for errors
4. **RetryManager**: Retry logic for transient failures
5. **FallbackHandler**: Fallback mechanisms for critical failures

### ErrorHandler

```python
class ErrorHandler:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.logger = Logger("ErrorHandler")
        self.notification_handler = NotificationHandler()
        
    def handle_error(self, exception: Exception, context: dict = None) -> dict:
        """Handle error with context and logging"""
        error_info = self._extract_error_info(exception, context)
        
        # Log error
        self.logger.error(error_info['message'], extra=error_info)
        
        # Notify if critical
        if self._is_critical_error(error_info):
            self.notification_handler.send_alert(error_info)
        
        # Determine response
        response = self._determine_response(error_info)
        
        return response
    
    def _extract_error_info(self, exception: Exception, context: dict = None) -> dict:
        """Extract detailed error information"""
        return {
            'type': type(exception).__name__,
            'message': str(exception),
            'context': context or {},
            'timestamp': datetime.now().isoformat(),
            'traceback': self._get_traceback(),
            'severity': self._determine_severity(exception)
        }
    
    def _get_traceback(self) -> str:
        """Get formatted traceback"""
        import traceback
        return traceback.format_exc()
    
    def _determine_severity(self, exception: Exception) -> str:
        """Determine error severity"""
        critical_errors = (SystemExit, KeyboardInterrupt, MemoryError)
        if isinstance(exception, critical_errors):
            return 'critical'
        elif isinstance(exception, (ValueError, TypeError)):
            return 'error'
        else:
            return 'warning'
    
    def _is_critical_error(self, error_info: dict) -> bool:
        """Check if error is critical"""
        return error_info['severity'] == 'critical'
    
    def _determine_response(self, error_info: dict) -> dict:
        """Determine appropriate response to error"""
        return {
            'status': 'error',
            'error': error_info['message'],
            'error_type': error_info['type'],
            'timestamp': error_info['timestamp']
        }
```

### Custom Exception Classes

```python
class BaseAutomationException(Exception):
    """Base exception for automation system"""
    def __init__(self, message: str, error_code: str = None, context: dict = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now()

class AgentException(BaseAutomationException):
    """Exception related to agent operations"""
    pass

class PipelineException(BaseAutomationException):
    """Exception related to pipeline operations"""
    pass

class IntegrationException(BaseAutomationException):
    """Exception related to external integrations"""
    pass

class ConfigurationException(BaseAutomationException):
    """Exception related to configuration issues"""
    pass

class MemoryException(BaseAutomationException):
    """Exception related to memory operations"""
    pass
```

## Logging Framework

### Logger Implementation

```python
import logging
import json
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name: str, config: dict = None):
        self.name = name
        self.config = config or {}
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with handlers and formatters"""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.config.get('level', logging.INFO))
        
        # Create formatter
        formatter = JsonFormatter(
            '%(timestamp)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.config.get('file_path', f'{self.name}.log'),
            maxBytes=self.config.get('max_bytes', 10485760),  # 10MB
            backupCount=self.config.get('backup_count', 5)
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler for development
        if self.config.get('console_output', False):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def info(self, message: str, extra: dict = None):
        """Log info message"""
        self.logger.info(message, extra=extra or {})
    
    def warning(self, message: str, extra: dict = None):
        """Log warning message"""
        self.logger.warning(message, extra=extra or {})
    
    def error(self, message: str, extra: dict = None):
        """Log error message"""
        self.logger.error(message, extra=extra or {})
    
    def debug(self, message: str, extra: dict = None):
        """Log debug message"""
        self.logger.debug(message, extra=extra or {})
    
    def critical(self, message: str, extra: dict = None):
        """Log critical message"""
        self.logger.critical(message, extra=extra or {})
```

### JSON Formatter

```python
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        """Format log record as JSON"""
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields
        if hasattr(record, 'extra'):
            log_entry.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)
```

## Integration with Agents

### BaseAgent with Error Handling

```python
class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.logger = Logger(name)
        self.error_handler = ErrorHandler()
        
    def handle(self, task: dict) -> dict:
        """Handle task with error handling"""
        try:
            self.logger.info(f"Processing task: {task.get('task', 'Unknown')}")
            
            # Validate input
            self._validate_input(task)
            
            # Process task
            result = self._process_task(task)
            
            self.logger.info(f"Task completed successfully")
            return result
            
        except Exception as e:
            # Handle error
            error_context = {
                'agent': self.name,
                'task': task,
                'timestamp': datetime.now().isoformat()
            }
            
            error_response = self.error_handler.handle_error(e, error_context)
            
            # Log error response
            self.logger.error(
                f"Error processing task: {error_response['error']}",
                extra=error_response
            )
            
            return error_response
    
    def _validate_input(self, task: dict):
        """Validate input task"""
        if not isinstance(task, dict):
            raise ValueError("Task must be a dictionary")
        
        if 'task' not in task:
            raise ValueError("Task must contain 'task' field")
    
    def _process_task(self, task: dict) -> dict:
        """Process task - to be implemented by subclasses"""
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")
```

### Enhanced Agent Implementation

```python
class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmailAgent")
        self.integration_manager = IntegrationManager()
        self._setup_integrations()
    
    def _setup_integrations(self):
        """Setup email integration with error handling"""
        try:
            email_config = self._load_config('email_config.yaml')
            email_adapter = EmailAdapter(email_config)
            self.integration_manager.register_adapter('email', email_adapter)
            self.logger.info("Email integration setup completed")
        except ConfigurationException as e:
            self.logger.error(f"Failed to load email configuration: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to setup email integration: {e}")
            raise IntegrationException(
                "Failed to setup email integration",
                error_code="EMAIL_SETUP_FAILED",
                context={'error': str(e)}
            )
    
    def _process_task(self, task: dict) -> dict:
        """Process email task with error handling"""
        try:
            task_description = task.get('task', '')
            
            # Parse email request
            email_request = self._parse_email_request(task_description)
            
            # Validate email request
            self._validate_email_request(email_request)
            
            # Send email with retry logic
            retry_manager = RetryManager(max_retries=3)
            result = retry_manager.execute_with_retry(
                lambda: self._send_email(email_request)
            )
            
            return {
                'status': 'success',
                'message': f'Email sent successfully to {result.get("recipient")}',
                'email_id': result.get('id'),
                'timestamp': datetime.now().isoformat()
            }
            
        except ValueError as e:
            raise AgentException(
                f"Invalid email request: {e}",
                error_code="INVALID_EMAIL_REQUEST",
                context={'task': task}
            )
        except IntegrationException:
            raise
        except Exception as e:
            raise AgentException(
                f"Failed to process email task: {e}",
                error_code="EMAIL_PROCESSING_FAILED",
                context={'task': task, 'error': str(e)}
            )
```

## Retry Logic

### RetryManager

```python
import time
import random
from typing import Callable, Any

class RetryManager:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0, 
                 jitter: bool = True):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.jitter = jitter
    
    def execute_with_retry(self, func: Callable) -> Any:
        """Execute function with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func()
            except Exception as e:
                last_exception = e
                
                # Check if we should retry
                if self._should_retry(e) and attempt < self.max_retries:
                    # Calculate delay with exponential backoff
                    delay = self._calculate_delay(attempt)
                    
                    # Add jitter to prevent thundering herd
                    if self.jitter:
                        delay *= (0.5 + random.random() * 0.5)
                    
                    time.sleep(delay)
                else:
                    # Max retries exceeded or non-retryable error
                    break
        
        raise last_exception
    
    def _should_retry(self, exception: Exception) -> bool:
        """Determine if exception should be retried"""
        # Non-retryable errors
        non_retryable = (
            ValueError, TypeError, ConfigurationException, 
            AgentException  # Assuming these are user errors
        )
        
        if isinstance(exception, non_retryable):
            return False
        
        # Retryable errors
        retryable = (
            ConnectionError, TimeoutError, IntegrationException
        )
        
        if isinstance(exception, retryable):
            return True
        
        # For other exceptions, check error message
        error_message = str(exception).lower()
        retryable_patterns = ['timeout', 'connection', 'temporary']
        
        return any(pattern in error_message for pattern in retryable_patterns)
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff"""
        return self.backoff_factor * (2 ** attempt)
```

## Fallback Mechanisms

### FallbackHandler

```python
class FallbackHandler:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.logger = Logger("FallbackHandler")
    
    def execute_with_fallback(self, primary_func: Callable, 
                            fallback_func: Callable = None,
                            fallback_data: dict = None) -> Any:
        """Execute function with fallback option"""
        try:
            return primary_func()
        except Exception as e:
            self.logger.warning(f"Primary function failed: {e}")
            
            # Try fallback if available
            if fallback_func:
                try:
                    self.logger.info("Executing fallback function")
                    return fallback_func(fallback_data)
                except Exception as fallback_e:
                    self.logger.error(f"Fallback function also failed: {fallback_e}")
                    # Re-raise original exception
                    raise e
            else:
                # No fallback, re-raise exception
                raise e
    
    def execute_with_multiple_fallbacks(self, functions: list) -> Any:
        """Execute multiple functions in order until one succeeds"""
        last_exception = None
        
        for func, name in functions:
            try:
                self.logger.info(f"Trying function: {name}")
                return func()
            except Exception as e:
                self.logger.warning(f"Function {name} failed: {e}")
                last_exception = e
        
        # All functions failed
        raise last_exception
```

## Monitoring and Metrics

### MetricsCollector

```python
import time
from collections import defaultdict

class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(lambda: defaultdict(int))
        self.timings = defaultdict(list)
    
    def record_success(self, component: str, operation: str):
        """Record successful operation"""
        self.metrics[component][f"{operation}_success"] += 1
    
    def record_error(self, component: str, operation: str, error_type: str = None):
        """Record error"""
        self.metrics[component][f"{operation}_error"] += 1
        if error_type:
            self.metrics[component][f"error_{error_type}"] += 1
    
    def record_timing(self, component: str, operation: str, duration: float):
        """Record operation timing"""
        self.timings[f"{component}_{operation}"].append(duration)
    
    def get_metrics(self) -> dict:
        """Get current metrics"""
        return dict(self.metrics)
    
    def get_timing_stats(self) -> dict:
        """Get timing statistics"""
        stats = {}
        for key, timings in self.timings.items():
            if timings:
                stats[key] = {
                    'count': len(timings),
                    'avg': sum(timings) / len(timings),
                    'min': min(timings),
                    'max': max(timings)
                }
        return stats

# Global metrics collector
metrics_collector = MetricsCollector()
```

### Decorator for Metrics Collection

```python
from functools import wraps

def monitor_performance(component: str, operation: str):
    """Decorator to monitor function performance"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                metrics_collector.record_success(component, operation)
                return result
            except Exception as e:
                metrics_collector.record_error(
                    component, operation, type(e).__name__
                )
                raise
            finally:
                duration = time.time() - start_time
                metrics_collector.record_timing(component, operation, duration)
        
        return wrapper
    return decorator

# Usage example
@monitor_performance("EmailAgent", "send_email")
def send_email(self, email_data: dict) -> dict:
    # Email sending implementation
    pass
```

## Configuration

### Error Handling Configuration

```yaml
# error_handling_config.yaml
error_handling:
  logging:
    level: "INFO"
    file_path: "logs/automation.log"
    max_bytes: 10485760  # 10MB
    backup_count: 5
    console_output: true
  
  retry:
    max_retries: 3
    backoff_factor: 1.0
    jitter: true
  
  notifications:
    critical_errors: true
    error_threshold: 5  # Send alert after 5 errors in 1 minute
    channels:
      - "email"
      - "slack"
  
  fallback:
    enabled: true
    max_fallback_depth: 3
```

## Usage Examples

### Basic Error Handling in Agent

```python
class FinanceAgent(BaseAgent):
    def _process_task(self, task: dict) -> dict:
        try:
            # Process financial data
            result = self._process_financial_data(task)
            
            # Record success metric
            metrics_collector.record_success("FinanceAgent", "process_task")
            
            return result
            
        except ValueError as e:
            # Handle validation errors
            metrics_collector.record_error("FinanceAgent", "process_task", "ValueError")
            raise AgentException(
                f"Invalid financial data: {e}",
                error_code="INVALID_FINANCIAL_DATA"
            )
        except IntegrationException as e:
            # Handle integration errors
            metrics_collector.record_error("FinanceAgent", "process_task", "IntegrationException")
            # Try fallback method
            fallback_handler = FallbackHandler()
            return fallback_handler.execute_with_fallback(
                lambda: self._process_task(task),
                lambda data: self._process_with_fallback(data),
                task
            )
```

### Retry with Exponential Backoff

```python
class DocumentAgent(BaseAgent):
    def _upload_document(self, document: dict) -> dict:
        retry_manager = RetryManager(
            max_retries=5,
            backoff_factor=2.0,
            jitter=True
        )
        
        return retry_manager.execute_with_retry(
            lambda: self.integration_manager.execute_request(
                'file_storage',
                {
                    'method': 'upload_file',
                    'data': document
                }
            )
        )
```

### Comprehensive Logging

```python
class SupportAgent(BaseAgent):
    def _process_task(self, task: dict) -> dict:
        # Log task start
        self.logger.info(
            "Processing support request",
            extra={
                'task_id': task.get('id'),
                'request_type': task.get('type'),
                'priority': task.get('priority', 'normal')
            }
        )
        
        try:
            # Process support request
            result = self._handle_support_request(task)
            
            # Log successful completion
            self.logger.info(
                "Support request processed successfully",
                extra={
                    'task_id': task.get('id'),
                    'resolution': result.get('resolution'),
                    'duration': result.get('processing_time')
                }
            )
            
            return result
            
        except Exception as e:
            # Log error with full context
            self.logger.error(
                "Failed to process support request",
                extra={
                    'task_id': task.get('id'),
                    'error': str(e),
                    'error_type': type(e).__name__
                }
            )
            raise
```

## Benefits

1. **Reliability**: Comprehensive error handling prevents system crashes
2. **Debugging**: Detailed logging helps identify and fix issues quickly
3. **Resilience**: Retry logic and fallback mechanisms handle transient failures
4. **Monitoring**: Metrics collection enables performance monitoring
5. **Maintainability**: Consistent error handling patterns across components
6. **User Experience**: Graceful error handling provides better user feedback
7. **Operational Efficiency**: Automated alerts and notifications for critical issues
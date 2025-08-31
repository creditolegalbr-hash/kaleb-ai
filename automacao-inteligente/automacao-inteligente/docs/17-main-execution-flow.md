# Main Execution Flow Enhancement

## Overview

The main execution flow is the entry point for the intelligent automation system. This document outlines the enhancements needed to create a more robust, flexible, and user-friendly main execution flow that can handle various input methods, provide better error handling, and support different execution modes.

## Current Limitations

The current main.py has several limitations:
1. Hard-coded agent instantiation
2. No configuration support
3. Limited error handling
4. No input validation
5. No support for different execution modes
6. No logging or monitoring
7. No graceful shutdown handling

## Enhanced Main Execution Flow

### Core Components

1. **ApplicationManager**: Central application manager
2. **InputHandler**: Handles different input sources
3. **ExecutionEngine**: Core execution engine
4. **OutputFormatter**: Formats output for different targets
5. **SignalHandler**: Handles system signals gracefully
6. **HealthMonitor**: Monitors system health

### ApplicationManager

```python
import sys
import signal
import argparse
from typing import Dict, Any
import logging

class ApplicationManager:
    def __init__(self):
        self.config_manager = None
        self.logger = None
        self.user_agent = None
        self.signal_handler = None
        self.health_monitor = None
        self.is_running = False
    
    def initialize(self, args: argparse.Namespace = None):
        """Initialize the application"""
        try:
            # Parse command line arguments
            self.args = args or self._parse_arguments()
            
            # Setup logging
            self._setup_logging()
            self.logger.info("Initializing application")
            
            # Load configuration
            self._load_configuration()
            
            # Setup signal handlers
            self._setup_signal_handlers()
            
            # Initialize components
            self._initialize_components()
            
            # Start health monitoring
            self._start_health_monitoring()
            
            self.logger.info("Application initialized successfully")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to initialize application: {e}")
            else:
                print(f"Failed to initialize application: {e}")
            sys.exit(1)
    
    def _parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="Intelligent Automation System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py --mode interactive
  python main.py --task "Send quarterly report" --type email
  python main.py --config config/production.yaml
  python main.py --batch tasks.json
            """
        )
        
        parser.add_argument(
            '--mode', 
            choices=['interactive', 'single', 'batch', 'service'],
            default='interactive',
            help='Execution mode (default: interactive)'
        )
        
        parser.add_argument(
            '--task',
            help='Single task to execute (for single mode)'
        )
        
        parser.add_argument(
            '--type',
            help='Task type for single task execution'
        )
        
        parser.add_argument(
            '--config',
            help='Configuration file path'
        )
        
        parser.add_argument(
            '--batch',
            help='Batch file with multiple tasks'
        )
        
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )
        
        parser.add_argument(
            '--version', '-V',
            action='version',
            version='Intelligent Automation System 1.0.0'
        )
        
        return parser.parse_args()
    
    def _setup_logging(self):
        """Setup application logging"""
        logging_config = {
            'level': logging.DEBUG if self.args.verbose else logging.INFO,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'handlers': [
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('logs/application.log')
            ]
        }
        
        logging.basicConfig(**logging_config)
        self.logger = logging.getLogger('ApplicationManager')
    
    def _load_configuration(self):
        """Load application configuration"""
        config_paths = []
        
        if self.args.config:
            config_paths.append(self.args.config)
        
        config_paths.extend([
            'config/default.yaml',
            'config/local.yaml'
        ])
        
        self.config_manager = ConfigManager(config_paths)
        self.logger.info("Configuration loaded successfully")
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        self.signal_handler = SignalHandler(self)
        signal.signal(signal.SIGINT, self.signal_handler.handle_signal)
        signal.signal(signal.SIGTERM, self.signal_handler.handle_signal)
    
    def _initialize_components(self):
        """Initialize application components"""
        # Initialize UserAgent
        self.user_agent = UserAgent(
            "MainUserAgent", 
            self.config_manager.config
        )
        
        self.logger.info("Application components initialized")
    
    def _start_health_monitoring(self):
        """Start health monitoring"""
        self.health_monitor = HealthMonitor(self.config_manager)
        self.health_monitor.start()
        self.logger.info("Health monitoring started")
    
    def run(self):
        """Main application execution loop"""
        try:
            self.is_running = True
            self.logger.info(f"Starting application in {self.args.mode} mode")
            
            if self.args.mode == 'interactive':
                self._run_interactive_mode()
            elif self.args.mode == 'single':
                self._run_single_task_mode()
            elif self.args.mode == 'batch':
                self._run_batch_mode()
            elif self.args.mode == 'service':
                self._run_service_mode()
            
            self.logger.info("Application execution completed")
            
        except Exception as e:
            self.logger.error(f"Application error: {e}", exc_info=True)
            sys.exit(1)
        finally:
            self.shutdown()
    
    def _run_interactive_mode(self):
        """Run interactive mode"""
        self.logger.info("Entering interactive mode")
        print("Intelligent Automation System - Interactive Mode")
        print("Type 'help' for available commands or 'quit' to exit")
        
        while self.is_running:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input:
                    self._process_interactive_command(user_input)
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' or 'exit' to exit the application")
            except EOFError:
                break
    
    def _run_single_task_mode(self):
        """Run single task mode"""
        if not self.args.task:
            self.logger.error("Task is required for single mode")
            print("Error: Task is required for single mode")
            sys.exit(1)
        
        task_type = self.args.type or self.user_agent.route_task(self.args.task)
        
        self.logger.info(f"Executing single task: {self.args.task} (type: {task_type})")
        
        result = self.user_agent.perform_task(task_type, self.args.task)
        self._output_result(result)
    
    def _run_batch_mode(self):
        """Run batch mode"""
        if not self.args.batch:
            self.logger.error("Batch file is required for batch mode")
            print("Error: Batch file is required for batch mode")
            sys.exit(1)
        
        self.logger.info(f"Executing batch tasks from: {self.args.batch}")
        
        try:
            batch_tasks = self._load_batch_file(self.args.batch)
            results = []
            
            for i, task_data in enumerate(batch_tasks):
                if not self.is_running:
                    break
                
                task = task_data.get('task')
                task_type = task_data.get('type') or self.user_agent.route_task(task)
                
                self.logger.info(f"Executing batch task {i+1}/{len(batch_tasks)}: {task}")
                
                result = self.user_agent.perform_task(task_type, task)
                results.append({
                    'task': task,
                    'type': task_type,
                    'result': result
                })
                
                # Output result
                self._output_result(result)
            
            # Save batch results
            self._save_batch_results(results)
            
        except Exception as e:
            self.logger.error(f"Batch execution failed: {e}")
            print(f"Batch execution failed: {e}")
            sys.exit(1)
    
    def _run_service_mode(self):
        """Run service mode"""
        self.logger.info("Starting service mode")
        print("Intelligent Automation System - Service Mode")
        print("Service started. Press Ctrl+C to stop.")
        
        # This would implement a service loop that listens for tasks
        # from queues, APIs, or other sources
        while self.is_running:
            try:
                # Check for new tasks (from queue, API, etc.)
                task = self._get_next_task()
                if task:
                    result = self.user_agent.perform_task(
                        task['type'], 
                        task['task'],
                        task.get('context')
                    )
                    self._handle_task_result(task, result)
                
                # Sleep briefly to prevent busy waiting
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Service error: {e}")
    
    def _show_help(self):
        """Show help information"""
        help_text = """
Available commands:
  help          - Show this help
  quit/exit     - Exit the application
  status        - Show system status
  config        - Show current configuration
  tasks         - List available task types
  <task>        - Execute a task (e.g., "Send email to client")
        """
        print(help_text)
    
    def _process_interactive_command(self, command: str):
        """Process interactive command"""
        if command.lower() == 'status':
            self._show_status()
        elif command.lower() == 'config':
            self._show_config()
        elif command.lower() == 'tasks':
            self._show_task_types()
        else:
            # Treat as task execution
            task_type = self.user_agent.route_task(command)
            result = self.user_agent.perform_task(task_type, command)
            self._output_result(result)
    
    def _show_status(self):
        """Show system status"""
        status = {
            'mode': self.args.mode,
            'is_running': self.is_running,
            'health': self.health_monitor.get_status() if self.health_monitor else 'unknown',
            'uptime': self._get_uptime()
        }
        print(f"System Status: {status}")
    
    def _show_config(self):
        """Show current configuration"""
        if self.config_manager:
            import json
            print("Current Configuration:")
            print(json.dumps(self.config_manager.config, indent=2))
    
    def _show_task_types(self):
        """Show available task types"""
        task_types = [
            'email - Process email tasks',
            'finance - Handle financial operations',
            'scheduler - Manage scheduling and calendar',
            'document - Process documents and files',
            'support - Handle support requests'
        ]
        print("Available Task Types:")
        for task_type in task_types:
            print(f"  {task_type}")
    
    def _load_batch_file(self, file_path: str) -> list:
        """Load batch tasks from file"""
        import json
        import os
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Batch file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _save_batch_results(self, results: list):
        """Save batch execution results"""
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"batch_results_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.logger.info(f"Batch results saved to: {output_file}")
        print(f"Batch results saved to: {output_file}")
    
    def _get_next_task(self):
        """Get next task for service mode"""
        # This would implement logic to get tasks from queues, APIs, etc.
        # For now, return None to prevent busy waiting in example
        return None
    
    def _handle_task_result(self, task: dict, result: dict):
        """Handle task result in service mode"""
        # This would implement result handling logic
        self.logger.info(f"Task completed: {task.get('task')} - Result: {result}")
    
    def _output_result(self, result: dict):
        """Output result in appropriate format"""
        output_formatter = OutputFormatter()
        output_formatter.format_and_output(result, self.args.verbose)
    
    def _get_uptime(self) -> str:
        """Get application uptime"""
        # Implementation would track start time and calculate uptime
        return "unknown"
    
    def shutdown(self):
        """Graceful shutdown"""
        if not self.is_running:
            return
        
        self.logger.info("Shutting down application")
        self.is_running = False
        
        # Stop health monitoring
        if self.health_monitor:
            self.health_monitor.stop()
        
        # Cleanup resources
        self._cleanup_resources()
        
        self.logger.info("Application shutdown completed")
    
    def _cleanup_resources(self):
        """Cleanup application resources"""
        # Close database connections, file handles, etc.
        pass
```

### SignalHandler

```python
import signal
import sys

class SignalHandler:
    def __init__(self, app_manager):
        self.app_manager = app_manager
        self.shutdown_requested = False
    
    def handle_signal(self, signum, frame):
        """Handle system signals"""
        signal_name = signal.Signals(signum).name
        
        if not self.shutdown_requested:
            print(f"\nReceived signal {signal_name} ({signum}). Shutting down gracefully...")
            self.app_manager.logger.info(f"Received signal {signal_name} ({signum})")
            self.shutdown_requested = True
            self.app_manager.shutdown()
        else:
            print("\nForce shutdown requested. Exiting immediately.")
            self.app_manager.logger.warning("Force shutdown requested")
            sys.exit(1)
```

### HealthMonitor

```python
import threading
import time
from typing import Dict, Any

class HealthMonitor:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.is_running = False
        self.thread = None
        self.status = {
            'system': 'unknown',
            'components': {},
            'last_check': None
        }
    
    def start(self):
        """Start health monitoring"""
        self.is_running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop health monitoring"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                self._perform_health_check()
                time.sleep(self.config_manager.get('health.check_interval', 30))
            except Exception as e:
                if self.config_manager:
                    logger = logging.getLogger('HealthMonitor')
                    logger.error(f"Health check error: {e}")
    
    def _perform_health_check(self):
        """Perform system health check"""
        import psutil
        import datetime
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        self.status = {
            'system': 'healthy' if cpu_percent < 90 and memory.percent < 90 else 'degraded',
            'components': {
                'cpu': {
                    'percent': cpu_percent,
                    'status': 'healthy' if cpu_percent < 80 else 'warning' if cpu_percent < 90 else 'critical'
                },
                'memory': {
                    'percent': memory.percent,
                    'available': memory.available,
                    'status': 'healthy' if memory.percent < 80 else 'warning' if memory.percent < 90 else 'critical'
                },
                'disk': {
                    'percent': (disk.used / disk.total) * 100,
                    'free': disk.free,
                    'status': 'healthy' if (disk.used / disk.total) < 0.8 else 'warning' if (disk.used / disk.total) < 0.9 else 'critical'
                }
            },
            'last_check': datetime.datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict[Any, Any]:
        """Get current health status"""
        return self.status.copy()
```

### OutputFormatter

```python
import json
from typing import Dict, Any

class OutputFormatter:
    def format_and_output(self, result: Dict[Any, Any], verbose: bool = False):
        """Format and output result"""
        if verbose:
            self._output_verbose(result)
        else:
            self._output_compact(result)
    
    def _output_verbose(self, result: Dict[Any, Any]):
        """Output result in verbose format"""
        print("Task Result:")
        print(json.dumps(result, indent=2, default=str))
    
    def _output_compact(self, result: Dict[Any, Any]):
        """Output result in compact format"""
        if result.get('success', False):
            print(f"✓ {result.get('result', 'Task completed successfully')}")
        else:
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
```

## Configuration Files

### Main Configuration

```yaml
# config/default.yaml
application:
  name: "Intelligent Automation System"
  version: "1.0.0"
  mode: "interactive"
  
  health:
    check_interval: 30  # seconds
    cpu_threshold: 80
    memory_threshold: 80
    disk_threshold: 80
  
  logging:
    level: "INFO"
    file: "logs/application.log"
    max_size: 10485760  # 10MB
    backup_count: 5
  
  input:
    timeout: 30  # seconds for interactive mode
  
  output:
    format: "compact"  # or "verbose"
```

## Usage Examples

### Command Line Usage

```bash
# Interactive mode (default)
python main.py

# Single task execution
python main.py --mode single --task "Send quarterly report to management" --type email

# Batch execution
python main.py --mode batch --batch tasks.json

# Service mode
python main.py --mode service

# With custom configuration
python main.py --config config/production.yaml

# Verbose output
python main.py --verbose
```

### Batch File Format

```json
[
  {
    "task": "Send welcome email to new customer",
    "type": "email"
  },
  {
    "task": "Generate monthly financial report",
    "type": "finance"
  },
  {
    "task": "Schedule team meeting for next week",
    "type": "scheduler"
  }
]
```

## Enhanced Main.py

```python
#!/usr/bin/env python3
"""
Intelligent Automation System Main Entry Point
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from application_manager import ApplicationManager

def main():
    """Main entry point"""
    app_manager = ApplicationManager()
    app_manager.initialize()
    app_manager.run()

if __name__ == "__main__":
    main()
```

## Benefits

1. **Flexibility**: Multiple execution modes for different use cases
2. **Robustness**: Comprehensive error handling and graceful shutdown
3. **Usability**: Interactive mode with helpful commands
4. **Monitoring**: Health monitoring and system status
5. **Configuration**: Flexible configuration management
6. **Logging**: Comprehensive logging for debugging
7. **Scalability**: Service mode for continuous operation
8. **Maintainability**: Modular design with clear separation of concerns
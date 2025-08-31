# Testing Framework

## Overview

A comprehensive testing framework is essential for ensuring the quality, reliability, and maintainability of the intelligent automation system. This document outlines the testing strategy, framework design, and implementation approach for testing agents, pipelines, and integrations.

## Testing Strategy

### Testing Principles

1. **Comprehensive Coverage**: Test all critical paths and edge cases
2. **Automated Testing**: Automate all tests for continuous integration
3. **Isolation**: Tests should be independent and isolated
4. **Speed**: Tests should execute quickly
5. **Reliability**: Tests should produce consistent results
6. **Maintainability**: Tests should be easy to update and maintain

### Testing Types

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test interactions between components
3. **System Tests**: Test the complete system behavior
4. **Performance Tests**: Test system performance under load
5. **Security Tests**: Test security aspects of the system
6. **Regression Tests**: Ensure new changes don't break existing functionality

## Testing Framework Architecture

### Core Components

1. **TestRunner**: Central test execution manager
2. **TestSuite**: Collection of related tests
3. **TestCase**: Individual test implementation
4. **TestFixture**: Setup and teardown for tests
5. **MockManager**: Mock object management
6. **AssertionLibrary**: Enhanced assertion capabilities
7. **TestReporter**: Test result reporting

### TestRunner

```python
import unittest
import sys
from typing import List, Type
import xmlrunner

class TestRunner:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.test_loader = unittest.TestLoader()
        self.test_runner = None
        self._setup_runner()
    
    def _setup_runner(self):
        """Setup test runner based on configuration"""
        output_format = self.config.get('output_format', 'text')
        
        if output_format == 'xml':
            self.test_runner = xmlrunner.XMLTestRunner(
                output=self.config.get('output_dir', 'test-reports')
            )
        else:
            self.test_runner = unittest.TextTestRunner(
                verbosity=self.config.get('verbosity', 2)
            )
    
    def run_tests(self, test_suite: unittest.TestSuite) -> unittest.TestResult:
        """Run test suite and return results"""
        return self.test_runner.run(test_suite)
    
    def run_test_class(self, test_class: Type[unittest.TestCase]) -> unittest.TestResult:
        """Run all tests in a test class"""
        suite = self.test_loader.loadTestsFromTestCase(test_class)
        return self.run_tests(suite)
    
    def run_test_module(self, module_name: str) -> unittest.TestResult:
        """Run all tests in a module"""
        suite = self.test_loader.loadTestsFromModule(__import__(module_name))
        return self.run_tests(suite)
    
    def run_all_tests(self, test_directory: str = 'tests') -> unittest.TestResult:
        """Run all tests in directory"""
        suite = self.test_loader.discover(
            start_dir=test_directory,
            pattern=self.config.get('pattern', 'test_*.py')
        )
        return self.run_tests(suite)
```

### Base Test Case

```python
import unittest
import tempfile
import os
from unittest.mock import Mock, patch
from datetime import datetime

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_start_time = datetime.now()
        self.temp_dir = tempfile.mkdtemp()
        self.mock_config = self._create_mock_config()
        
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Reset any global state
        self._reset_global_state()
    
    def _create_mock_config(self) -> dict:
        """Create mock configuration for testing"""
        return {
            'agents': {
                'email': True,
                'finance': True,
                'scheduler': True,
                'document': True,
                'support': True
            },
            'logging': {
                'level': 'DEBUG',
                'console_output': False
            },
            'memory': {
                'context_manager': {
                    'max_history': 10
                }
            }
        }
    
    def _reset_global_state(self):
        """Reset any global state that might affect other tests"""
        pass
    
    def assertDictContainsSubset(self, subset: dict, dictionary: dict, msg: str = None):
        """Assert that dictionary contains subset"""
        missing_keys = set(subset.keys()) - set(dictionary.keys())
        if missing_keys:
            self.fail(f"Missing keys in dictionary: {missing_keys}")
        
        for key, expected_value in subset.items():
            actual_value = dictionary[key]
            self.assertEqual(
                expected_value, actual_value,
                f"Key '{key}': expected {expected_value}, got {actual_value}"
            )
    
    def create_mock_agent(self, agent_name: str) -> Mock:
        """Create mock agent for testing"""
        mock_agent = Mock()
        mock_agent.name = agent_name
        mock_agent.handle.return_value = {
            'status': 'success',
            'message': f'{agent_name} processed task successfully'
        }
        return mock_agent
```

## Unit Testing

### Agent Unit Tests

```python
# tests/test_agents/test_base_agent.py
import unittest
from unittest.mock import Mock, patch
from src.agents.base_agent import BaseAgent

class TestBaseAgent(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.agent = BaseAgent("TestAgent")
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.name, "TestAgent")
    
    def test_handle_method_raises_not_implemented(self):
        """Test that handle method raises NotImplementedError"""
        with self.assertRaises(NotImplementedError) as context:
            self.agent.handle({"task": "test"})
        
        self.assertIn("Este método deve ser implementado pelas subclasses", 
                     str(context.exception))

# tests/test_agents/test_email_agent.py
from src.agents.email_agent import EmailAgent

class TestEmailAgent(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.agent = EmailAgent()
    
    def test_email_agent_initialization(self):
        """Test EmailAgent initialization"""
        self.assertEqual(self.agent.name, "EmailAgent")
    
    def test_handle_method_returns_string(self):
        """Test that handle method returns a string"""
        result = self.agent.handle("Send test email")
        self.assertIsInstance(result, str)
        self.assertIn("EmailAgent", result)
        self.assertIn("Send test email", result)
    
    @patch('src.agents.email_agent.EmailAgent.handle')
    def test_handle_method_calls(self, mock_handle):
        """Test that handle method is called correctly"""
        mock_handle.return_value = "[EmailAgent] Test response"
        result = self.agent.handle("Test task")
        
        mock_handle.assert_called_once_with("Test task")
        self.assertEqual(result, "[EmailAgent] Test response")
```

### Pipeline Unit Tests

```python
# tests/test_pipelines/test_base_pipeline.py
import unittest
from unittest.mock import Mock

class BasePipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps = []
    
    def add_step(self, step_function):
        self.steps.append(step_function)
    
    def process(self, data: dict) -> dict:
        result = data.copy()
        for step in self.steps:
            try:
                result = step(result)
            except Exception as e:
                result['error'] = str(e)
                break
        return result

class TestBasePipeline(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.pipeline = BasePipeline("TestPipeline")
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization"""
        self.assertEqual(self.pipeline.name, "TestPipeline")
        self.assertEqual(len(self.pipeline.steps), 0)
    
    def test_add_step(self):
        """Test adding steps to pipeline"""
        def test_step(data):
            return data
        
        self.pipeline.add_step(test_step)
        self.assertEqual(len(self.pipeline.steps), 1)
    
    def test_process_empty_pipeline(self):
        """Test processing with no steps"""
        data = {"test": "data"}
        result = self.pipeline.process(data)
        self.assertEqual(result, data)
    
    def test_process_with_steps(self):
        """Test processing with steps"""
        def step1(data):
            data['step1'] = True
            return data
        
        def step2(data):
            data['step2'] = True
            return data
        
        self.pipeline.add_step(step1)
        self.pipeline.add_step(step2)
        
        data = {"original": "data"}
        result = self.pipeline.process(data)
        
        self.assertTrue(result['step1'])
        self.assertTrue(result['step2'])
        self.assertEqual(result['original'], 'data')
```

## Integration Testing

### Agent Integration Tests

```python
# tests/test_integration/test_agent_integration.py
import unittest
from src.agents.user_agent import UserAgent
from src.agents.email_agent import EmailAgent
from src.agents.finance_agent import FinanceAgent

class TestAgentIntegration(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_agent = UserAgent("TestUserAgent")
    
    def test_user_agent_initializes_agents(self):
        """Test that UserAgent initializes agents correctly"""
        # This would test the enhanced UserAgent implementation
        pass
    
    def test_perform_email_task(self):
        """Test performing email task through UserAgent"""
        result = self.user_agent.perform_task("email", "Send quarterly report")
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get('success', False))
        self.assertIn('EmailAgent', result.get('result', ''))
    
    def test_perform_finance_task(self):
        """Test performing finance task through UserAgent"""
        result = self.user_agent.perform_task("finance", "Generate invoice")
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get('success', False))
        self.assertIn('FinanceAgent', result.get('result', ''))
```

### Pipeline Integration Tests

```python
# tests/test_integration/test_pipeline_integration.py
import unittest
from unittest.mock import Mock, patch

class TestPipelineIntegration(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Setup for pipeline integration tests
        pass
    
    @patch('src.pipelines.email_pipeline.EmailPipeline')
    @patch('src.agents.email_agent.EmailAgent')
    def test_email_pipeline_integration(self, mock_agent, mock_pipeline):
        """Test email pipeline integration with EmailAgent"""
        # Setup mocks
        mock_agent_instance = Mock()
        mock_agent_instance.handle.return_value = {
            'status': 'success',
            'message': 'Email processed'
        }
        mock_agent.return_value = mock_agent_instance
        
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.process.return_value = {
            'status': 'success',
            'result': 'Email sent successfully'
        }
        mock_pipeline.return_value = mock_pipeline_instance
        
        # Test integration
        # This would test the actual integration logic
        
    def test_pipeline_error_handling(self):
        """Test pipeline error handling"""
        # Test that errors are properly handled and propagated
        pass
```

## System Testing

### End-to-End Tests

```python
# tests/test_system/test_end_to_end.py
import unittest
import tempfile
import os
from src.main import main

class TestEndToEnd(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.output_file = os.path.join(self.temp_dir, 'output.txt')
    
    def test_main_execution(self):
        """Test main execution flow"""
        # Capture stdout
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            main()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        
        # Assert expected output
        self.assertIn("Processando email", output)
        self.assertIn("Processando tarefa financeira", output)
        self.assertIn("Agendando", output)
        self.assertIn("Gerenciando documentos", output)
        self.assertIn("Suporte ao cliente", output)
    
    def test_system_with_config(self):
        """Test system with custom configuration"""
        # Test system behavior with different configurations
        pass
```

## Performance Testing

### Load Testing Framework

```python
# tests/test_performance/test_load.py
import unittest
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from src.agents.user_agent import UserAgent

class TestLoadPerformance(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_agent = UserAgent("PerformanceTestAgent")
    
    def test_single_task_performance(self):
        """Test performance of single task execution"""
        start_time = time.time()
        
        result = self.user_agent.perform_task("email", "Performance test email")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertTrue(result.get('success', False))
        self.assertLess(execution_time, 1.0)  # Should complete in less than 1 second
    
    def test_concurrent_task_performance(self):
        """Test performance under concurrent load"""
        def execute_task(task_data):
            return self.user_agent.perform_task(task_data['type'], task_data['task'])
        
        tasks = [
            {'type': 'email', 'task': f'Test email {i}'} for i in range(10)
        ]
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(execute_task, tasks))
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert all tasks completed successfully
        success_count = sum(1 for result in results if result.get('success', False))
        self.assertEqual(success_count, len(tasks))
        
        # Assert reasonable performance (less than 5 seconds for 10 tasks)
        self.assertLess(execution_time, 5.0)
    
    def test_memory_usage(self):
        """Test memory usage during execution"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Execute multiple tasks
        for i in range(100):
            self.user_agent.perform_task("email", f"Memory test email {i}")
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert reasonable memory usage (less than 50MB increase)
        self.assertLess(memory_increase, 50)
```

## Mocking and Stubbing

### Mock Manager

```python
# tests/test_utils/mock_manager.py
from unittest.mock import Mock, patch, MagicMock
import boto3
import requests

class MockManager:
    def __init__(self):
        self.mocks = {}
    
    def mock_external_service(self, service_name: str, **kwargs):
        """Create mock for external service"""
        if service_name == 'google_calendar':
            return self._mock_google_calendar(**kwargs)
        elif service_name == 'email_service':
            return self._mock_email_service(**kwargs)
        elif service_name == 'database':
            return self._mock_database(**kwargs)
        elif service_name == 'file_storage':
            return self._mock_file_storage(**kwargs)
        else:
            raise ValueError(f"Unknown service: {service_name}")
    
    def _mock_google_calendar(self, **kwargs):
        """Mock Google Calendar API"""
        mock_calendar = Mock()
        mock_calendar.events().insert().execute.return_value = {
            'id': 'test_event_id',
            'summary': kwargs.get('summary', 'Test Event'),
            'start': {'dateTime': '2023-01-01T10:00:00Z'},
            'end': {'dateTime': '2023-01-01T11:00:00Z'}
        }
        return mock_calendar
    
    def _mock_email_service(self, **kwargs):
        """Mock email service"""
        mock_email = Mock()
        mock_email.send.return_value = {
            'id': 'test_email_id',
            'status': 'sent'
        }
        return mock_email
    
    def _mock_database(self, **kwargs):
        """Mock database connection"""
        mock_db = Mock()
        mock_db.execute.return_value = kwargs.get('return_value', [])
        return mock_db
    
    def _mock_file_storage(self, **kwargs):
        """Mock file storage service"""
        mock_storage = Mock()
        mock_storage.upload.return_value = {
            'id': 'test_file_id',
            'url': 'https://storage.example.com/test_file'
        }
        return mock_storage
```

## Test Configuration

### Test Configuration Files

```yaml
# tests/config/test_config.yaml
testing:
  database:
    type: "sqlite"
    path: ":memory:"  # In-memory database for testing
  
  logging:
    level: "DEBUG"
    file_path: "logs/test.log"
    console_output: false
  
  integrations:
    google_calendar:
      enabled: false  # Disable real API calls
    email_service:
      enabled: false
    database:
      enabled: true
    file_storage:
      enabled: false
  
  memory:
    context_manager:
      max_history: 10  # Smaller for testing
  
  timeouts:
    test_execution: 30  # 30 seconds max per test
    suite_execution: 300  # 5 minutes max per suite
```

## Test Execution

### Test Runner Script

```python
# tests/run_tests.py
#!/usr/bin/env python3
import sys
import os
import argparse
import unittest
from tests.test_runner import TestRunner

def main():
    parser = argparse.ArgumentParser(description='Run automation system tests')
    parser.add_argument('--type', choices=['unit', 'integration', 'system', 'all'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--pattern', default='test_*.py', 
                       help='Pattern for test files')
    parser.add_argument('--output-format', choices=['text', 'xml'], 
                       default='text', help='Output format')
    parser.add_argument('--verbose', action='store_true', 
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Configuration
    config = {
        'output_format': args.output_format,
        'pattern': args.pattern,
        'verbosity': 2 if args.verbose else 1
    }
    
    # Initialize test runner
    test_runner = TestRunner(config)
    
    # Run tests based on type
    if args.type == 'unit':
        result = test_runner.run_test_module('tests.test_agents')
    elif args.type == 'integration':
        result = test_runner.run_test_module('tests.test_integration')
    elif args.type == 'system':
        result = test_runner.run_test_module('tests.test_system')
    else:  # all
        result = test_runner.run_all_tests('tests')
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == '__main__':
    main()
```

## Continuous Integration

### CI Configuration

```yaml
# .github/workflows/test.yml
name: Run Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run unit tests
      run: python -m tests.run_tests --type unit
    
    - name: Run integration tests
      run: python -m tests.run_tests --type integration
    
    - name: Run system tests
      run: python -m tests.run_tests --type system
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      if: always()
      with:
        name: test-results
        path: test-reports/
```

## Usage Examples

### Running Tests

```bash
# Run all tests
python -m tests.run_tests

# Run unit tests only
python -m tests.run_tests --type unit

# Run with XML output
python -m tests.run_tests --output-format xml

# Run with verbose output
python -m tests.run_tests --verbose
```

### Writing Tests

```python
# Example test for a new agent
class TestDocumentAgent(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.agent = DocumentAgent()
    
    def test_document_processing(self):
        """Test document processing functionality"""
        test_document = {
            'content': 'Test document content',
            'type': 'pdf'
        }
        
        result = self.agent.handle(test_document)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'success')
        self.assertIn('processed', result['message'])
    
    def test_document_validation(self):
        """Test document validation"""
        invalid_document = {
            'content': '',  # Empty content
            'type': 'unknown'  # Unknown type
        }
        
        result = self.agent.handle(invalid_document)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'error')
        self.assertIn('validation', result['message'])
```

## Test Coverage

### Coverage Configuration

```ini
# .coveragerc
[run]
source = src/
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

show_missing = True
precision = 2
```

## Benefits

1. **Quality Assurance**: Comprehensive testing ensures system quality
2. **Regression Prevention**: Automated tests prevent breaking changes
3. **Documentation**: Tests serve as executable documentation
4. **Confidence**: Reliable tests provide confidence in deployments
5. **Maintainability**: Well-tested code is easier to maintain
6. **Performance**: Performance tests ensure system efficiency
7. **Security**: Security tests identify vulnerabilities
8. **Collaboration**: Shared testing framework improves team collaboration
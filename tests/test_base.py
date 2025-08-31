import unittest
import tempfile
import os
import sys
import logging
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_start_time = datetime.now()
        self.temp_dir = tempfile.mkdtemp()
        self._setup_test_logging()
        
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Reset any global state
        self._reset_global_state()
    
    def _setup_test_logging(self):
        """Setup logging for tests"""
        # Disable logging during tests to avoid cluttering output
        logging.getLogger().setLevel(logging.CRITICAL)
    
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
    
    def create_test_config(self) -> dict:
        """Create test configuration"""
        return {
            'system': {
                'name': 'Test Automation System',
                'version': '1.0.0',
                'debug': True
            },
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
            },
            'pipelines': {
                'email': {'enabled': True},
                'finance': {'enabled': True},
                'scheduler': {'enabled': True},
                'document': {'enabled': True},
                'support': {'enabled': True}
            }
        }
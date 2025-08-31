import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from agents.email_agent import EmailAgent

class TestEmailAgent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agent = EmailAgent()
    
    def test_email_agent_initialization(self):
        """Test EmailAgent initialization"""
        self.assertEqual(self.agent.name, "EmailAgent")
        self.assertIsNotNone(self.agent.logger)
        self.assertIsNotNone(self.agent.context_manager)
        self.assertIsNotNone(self.agent.memory_store)
    
    def test_process_with_context_returns_string(self):
        """Test that _process_with_context method returns a string"""
        context = {
            'task': 'Test email task',
            'memories': []
        }
        result = self.agent._process_with_context('Test email task', context)
        self.assertIsInstance(result, str)
        self.assertIn("EmailAgent", result)
        self.assertIn("Test email task", result)
    
    def test_process_with_context_with_memories(self):
        """Test _process_with_context with memory context"""
        context = {
            'task': 'Test email task',
            'memories': [
                {'task': 'previous task', 'result': 'previous result'}
            ]
        }
        result = self.agent._process_with_context('Test email task', context)
        self.assertIsInstance(result, str)
        self.assertIn("EmailAgent", result)
        self.assertIn("Test email task", result)
        self.assertIn("Contexto relevante", result)

if __name__ == '__main__':
    unittest.main()
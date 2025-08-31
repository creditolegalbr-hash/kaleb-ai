import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from agents.base_agent import BaseAgent

class TestBaseAgent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agent = BaseAgent("TestAgent")
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertIsNotNone(self.agent.logger)
        self.assertIsNotNone(self.agent.context_manager)
        self.assertIsNotNone(self.agent.memory_store)
    
    def test_handle_method_raises_not_implemented(self):
        """Test that handle method raises NotImplementedError"""
        with self.assertRaises(NotImplementedError) as context:
            self.agent.handle("test task")
        
        self.assertIn("Este método deve ser implementado pelas subclasses", 
                     str(context.exception))
    
    def test_context_manager_functionality(self):
        """Test context manager functionality"""
        # Test updating context
        self.agent.context_manager.update_context("test_key", "test_value")
        context = self.agent.context_manager.get_context()
        self.assertEqual(context["test_key"], "test_value")
        
        # Test adding to history
        interaction = {"task": "test", "timestamp": "2023-01-01"}
        self.agent.context_manager.add_to_history(interaction)
        history = self.agent.context_manager.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["task"], "test")
    
    def test_memory_store_functionality(self):
        """Test memory store functionality"""
        # Test storing memory
        memory_item = {
            "agent": "TestAgent",
            "task": "test task",
            "result": "test result"
        }
        self.agent.memory_store.store(memory_item)
        
        # Test retrieving by keyword
        memories = self.agent.memory_store.retrieve_by_keyword("test")
        self.assertGreater(len(memories), 0)
        
        # Test retrieving recent memories
        recent_memories = self.agent.memory_store.retrieve_recent(5)
        self.assertGreater(len(recent_memories), 0)

if __name__ == '__main__':
    unittest.main()
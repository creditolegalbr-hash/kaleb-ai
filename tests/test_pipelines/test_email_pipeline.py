import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pipelines.email_pipeline import EmailPipeline

class TestEmailPipeline(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.pipeline = EmailPipeline()
    
    def test_email_pipeline_initialization(self):
        """Test EmailPipeline initialization"""
        self.assertEqual(self.pipeline.name, "EmailPipeline")
        self.assertIsNotNone(self.pipeline.email_agent)
        self.assertGreater(len(self.pipeline.steps), 0)
    
    def test_process_email_step(self):
        """Test process_email step"""
        data = {"task": "Send test email"}
        result = self.pipeline.process_email(data)
        self.assertIn('processed_email', result)
        self.assertIsInstance(result['processed_email'], str)
    
    def test_analyze_content_step(self):
        """Test analyze_content step"""
        # Test normal priority
        data = {"task": "Send regular email"}
        result = self.pipeline.analyze_content(data)
        self.assertEqual(result['priority'], 'normal')
        
        # Test high priority
        data = {"task": "Send urgent email ASAP"}
        result = self.pipeline.analyze_content(data)
        self.assertEqual(result['priority'], 'high')
        
        # Test low priority
        data = {"task": "Send email later tomorrow"}
        result = self.pipeline.analyze_content(data)
        self.assertEqual(result['priority'], 'low')
    
    def test_determine_action_step(self):
        """Test determine_action step"""
        # Test reply action
        data = {"task": "Reply to customer email"}
        result = self.pipeline.determine_action(data)
        self.assertEqual(result['action'], 'reply')
        
        # Test forward action
        data = {"task": "Forward email to manager"}
        result = self.pipeline.determine_action(data)
        self.assertEqual(result['action'], 'forward')
        
        # Test archive action
        data = {"task": "Archive old email file"}
        result = self.pipeline.determine_action(data)
        self.assertEqual(result['action'], 'archive')
        
        # Test classify action (default)
        data = {"task": "Process email"}
        result = self.pipeline.determine_action(data)
        self.assertEqual(result['action'], 'classify')
    
    def test_execute_action_step(self):
        """Test execute_action step"""
        # Test reply action
        data = {"task": "Send email", "action": "reply"}
        result = self.pipeline.execute_action(data)
        self.assertIn("Auto-replied", result['result'])
        
        # Test forward action
        data = {"task": "Forward email", "action": "forward"}
        result = self.pipeline.execute_action(data)
        self.assertIn("Forwarded", result['result'])
        
        # Test archive action
        data = {"task": "Archive email", "action": "archive"}
        result = self.pipeline.execute_action(data)
        self.assertIn("Archived", result['result'])
        
        # Test classify action
        data = {"task": "Classify email", "action": "classify"}
        result = self.pipeline.execute_action(data)
        self.assertIn("Classified", result['result'])
    
    def test_full_pipeline_process(self):
        """Test full pipeline process"""
        data = {"task": "Send urgent email to client"}
        result = self.pipeline.process(data)
        
        # Check that all steps were processed
        self.assertIn('processed_email', result)
        self.assertIn('priority', result)
        self.assertIn('action', result)
        self.assertIn('result', result)
        self.assertTrue(result['success'])

if __name__ == '__main__':
    unittest.main()
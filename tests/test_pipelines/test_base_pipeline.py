import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pipelines.base_pipeline import BasePipeline

class TestBasePipeline(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
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
    
    def test_process_with_error_handling(self):
        """Test pipeline error handling"""
        def step1(data):
            data['step1'] = True
            return data
        
        def step2(data):
            raise Exception("Test error")
        
        def step3(data):
            data['step3'] = True
            return data
        
        self.pipeline.add_step(step1)
        self.pipeline.add_step(step2)
        self.pipeline.add_step(step3)
        
        data = {"original": "data"}
        result = self.pipeline.process(data)
        
        # Step1 should have executed
        self.assertTrue(result['step1'])
        # Step2 should have caused an error
        self.assertIn('error', result)
        self.assertEqual(result['error'], "Test error")
        # Step3 should not have executed
        self.assertNotIn('step3', result)

if __name__ == '__main__':
    unittest.main()
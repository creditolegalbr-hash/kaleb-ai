#!/usr/bin/env python3
"""
Test runner for Intelligent Automation System
"""

import sys
import os
import unittest
import argparse

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_all_tests():
    """Run all tests in the tests directory"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

def run_tests_by_module(module_name):
    """Run tests for a specific module"""
    # Import the test module
    module = __import__(f'tests.{module_name}', fromlist=[''])
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(module)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

def run_tests_by_type(test_type):
    """Run tests for a specific type (agents, pipelines, etc.)"""
    # Discover and run tests for specific type
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), f'test_{test_type}')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

def main():
    """Main entry point for test runner"""
    parser = argparse.ArgumentParser(description='Run tests for Intelligent Automation System')
    parser.add_argument('--module', '-m', help='Run tests for specific module')
    parser.add_argument('--type', '-t', help='Run tests for specific type (agents, pipelines, etc.)')
    parser.add_argument('--all', '-a', action='store_true', help='Run all tests (default)')
    
    args = parser.parse_args()
    
    try:
        if args.module:
            # Run tests for specific module
            exit_code = run_tests_by_module(args.module)
        elif args.type:
            # Run tests for specific type
            exit_code = run_tests_by_type(args.type)
        else:
            # Run all tests
            exit_code = run_all_tests()
        
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
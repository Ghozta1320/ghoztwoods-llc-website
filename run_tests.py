import unittest
import sys
from test_osint_scanner_part1 import TestOSINTScannerPart1
from test_osint_scanner_part2 import TestOSINTScannerPart2
from test_osint_scanner_part3 import TestOSINTScannerPart3

def run_test_suite():
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases from all parts
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOSINTScannerPart1))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOSINTScannerPart2))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOSINTScannerPart3))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("Starting OSINT Scanner Test Suite...")
    print("Testing comprehensive scanning capabilities...")
    sys.exit(run_test_suite())

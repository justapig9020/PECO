import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../judger")

from judge import judge
import unittest

class Test(unittest.TestCase):
    def test_all_pass(self):
        report = judge('all_pass/judge.yaml')
        self.assertEqual(len(report), 5)
        # Traverse the value of report
        # Assert that all values are None
        for result in report.values():
            self.assertEqual(result, None, result)
    
    def test_with_fail(self):
        report = judge('with_fail/judge.yaml')
        self.assertEqual(len(report), 5)
        # Traverse the value of report
        # Assert that all values are None except the "input_5"
        for testcase, result in report.items():
            if 'input_5' in testcase:
                self.assertNotEqual(result, None, result)
            else:
                self.assertEqual(result, None, result)

if __name__ == '__main__':
    unittest.main()
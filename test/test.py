import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../judger")

from judge import judge
import unittest

class Test(unittest.TestCase):
    def test(self):
        report = judge('all_pass/judge.yaml')
        self.assertEqual(len(report), 5)
        for result in report.items():
            self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.main()
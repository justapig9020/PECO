import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../judger")

from judge import judge
import unittest

class Test(unittest.TestCase):
    def test(self):
        result = judge('all_pass/judge.yaml')
        print(result)

if __name__ == '__main__':
    unittest.main()
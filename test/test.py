import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from process import process_tasks
import unittest
import re

class Test(unittest.TestCase):
    def setUp(self):
        self.pwd = os.getcwd()

    def tearDown(self):
        os.chdir(self.pwd)

    def test_all_pass(self):
        pwd = os.getcwd()

        results = process_tasks('all_pass/judge.yaml')
        self.assertEqual(len(results), 5)
        # Traverse the value of report
        # Assert that all values are None
        for result in results.values():
            self.assertEqual(result, None, result)

        self.assertEqual(os.getcwd(), pwd)

    def test_with_fail(self):
        pwd = os.getcwd()

        results = process_tasks('with_fail/judge.yaml')
        self.assertEqual(len(results), 5)
        # Traverse the value of report
        # Assert that all values are None except the "input_5"
        for testcase, result in results.items():
            if '5' in testcase:
                self.assertNotEqual(result, None, result)
            else:
                self.assertEqual(result, None, result)

        self.assertEqual(os.getcwd(), pwd)

    def test_compile_error(self):
        from process import SetupFailed
        with self.assertRaises(SetupFailed):
            process_tasks('compile_error/judge.yaml')

    def test_missing_input(self):
        from task import FileMiss
        with self.assertRaises(FileMiss) as raised:
            process_tasks('missing_input/judge.yaml')
        expect = "task.FileMiss: File in \"input\" type with index \"1\" is missing"
        message = f'{raised.exception}'
        self.assertIsNotNone(expect, message)

    def test_missing_expect(self):
        from task import FileMiss
        with self.assertRaises(FileMiss) as raised:
            process_tasks('missing_input/judge.yaml')
        expect = "task.FileMiss: File in \"expect\" type with index \"1\" is missing"
        message = f'{raised.exception}'
        self.assertIsNotNone(expect, message)

if __name__ == '__main__':
    unittest.main()
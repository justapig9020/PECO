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
            if 'input_5' in testcase:
                self.assertNotEqual(result, None, result)
            else:
                self.assertEqual(result, None, result)

        self.assertEqual(os.getcwd(), pwd)

    def test_compile_error(self):
        from process import CompileError
        with self.assertRaises(CompileError):
            process_tasks('compile_error/judge.yaml')

    def test_missing_input(self):
        from task import InputMiss
        with self.assertRaises(InputMiss) as raised:
            process_tasks('missing_input/judge.yaml')
        expect = re.compile("Input file for .*missing_input/testcases/output_1.txt is missing")
        message = f'{raised.exception}'
        self.assertIsNotNone(expect.match(message), message)

    def test_missing_expect(self):
        from task import ExpectMiss
        with self.assertRaises(ExpectMiss) as raised:
            process_tasks('missing_expect/judge.yaml')
        expect = re.compile("Expect file for .*missing_expect/testcases/input_1.txt is missing")
        message = f'{raised.exception}'
        self.assertIsNotNone(expect.match(message), message)

if __name__ == '__main__':
    unittest.main()
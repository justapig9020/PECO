import variable
import os
import re
import itertools

class IndexedFile:
    def __init__(self, index, name):
        self.index = index
        self.name = name

def list_test_cases(config):
    path = config['root'] + '/' + variable.solve_string(config, config['test_cases']['path'])
    input_format = config['test_cases']['format']['input']
    expect_format = config['test_cases']['format']['expect']
    input_format_re = variable.solve_string(config, input_format, prefix='(', postfix=')')
    expect_format_re = variable.solve_string(config, expect_format, prefix='(', postfix=')')
    input_list = list_matched_files(path, input_format_re)
    expect_list = list_matched_files(path, expect_format_re)
    combinations = itertools.product(input_list, expect_list)
    return [(input.name, expect.name) for input, expect in combinations if input.index == expect.index]


def list_matched_files(path, format):
    # list all files in the path
    files = os.listdir(path)
    # filter the files
    format = re.compile(format)
    indexed_files = [(file, format.findall(file)) for file in files]
    return [IndexedFile(index, file) for file, index in indexed_files if index != []]
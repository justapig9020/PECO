import variable
import os
import re
import itertools

class IndexedFile:
    def __init__(self, index, name):
        self.index = index
        self.name = name

class InputMiss(Exception):
    def __init__(self, expect_file):
        super().__init__(f'Input file for {expect_file} is missing')

class ExpectMiss(Exception):
    def __init__(self, input_file):
        super().__init__(f'Expect file for {input_file} is missing')

def expect_file(input_file, expect_hash):
    if input_file.index in expect_hash:
        # FIXME: the function pop() is not efficient since it will modify the hash table
        return expect_hash.pop(input_file.index).name
    else:
        raise ExpectMiss(input_file.name)

def build_testcases(input_list, expect_list):
    testcases = [(input_list[i].name, expect_list[i].name) for i in range(len(input_list))]
    return testcases

def check_no_missing_testcases(input_list, expect_list):
    input_indices = set([f.index for f in input_list])
    expect_indices = set([f.index for f in expect_list])

    diff_indices = sorted(input_indices ^ expect_indices)

    if len(diff_indices) != 0:
        if diff_indices[0] in input_indices:
            for f in input_list:
                if f.index == diff_indices[0]:
                    raise ExpectMiss(f.name)
        elif diff_indices[0] in expect_indices:
            for f in expect_list:
                if f.index == diff_indices[0]:
                    raise InputMiss(f.name)

def list_testcases(config):
    path = config['root'] + '/' + variable.solve_string(config, config['testcases']['path'])
    input_format = config['testcases']['format']['input']
    expect_format = config['testcases']['format']['expect']
    input_format_re = variable.solve_string(config, input_format, prefix='(', postfix=')')
    expect_format_re = variable.solve_string(config, expect_format, prefix='(', postfix=')')

    files = list_files_recursively(path)
    input_list = list_matched_files(files, input_format_re)
    expect_list = list_matched_files(files, expect_format_re)
    check_no_missing_testcases(input_list, expect_list)

    # sort input_list by index
    input_list = sorted(input_list, key=lambda file: file.index)
    testcases = build_testcases(input_list, expect_list)

    file_format_re = '(' + variable.solve_string(config, input_format) + ')'
    file_name = re.compile(file_format_re)
    testcases = [(input, expect, file_name.findall(input)[0]) for input, expect in testcases]
    return testcases

def list_files_recursively(path):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            result.append(file_path)
    return result

def list_matched_files(files, format):
    # filter the files
    format = re.compile(format)
    files = [file for file in files]
    indexed_files = [(file, format.findall(file)) for file in files]
    return [IndexedFile(index[0], file) for file, index in indexed_files if index != []]
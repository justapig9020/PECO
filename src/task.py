import os
import re

import variable

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

def build_tasks(input_list, expect_list):
    expect_hash = {file.index: file for file in expect_list}

    tasks = [(input.name, expect_file(input, expect_hash)) for input in input_list]

    if len(expect_hash) != 0:
        # pick one of the expect file
        input_miss = list(expect_hash.values())[0]
        raise InputMiss(input_miss.name)

    return tasks

def list_tasks(config):
    tasks = config['tasks']
    path = config['root'] + '/' + variable.solve_string(config, tasks['path'])
    input_format = tasks['format']['input']
    expect_format = tasks['format']['expect']
    input_format_re = variable.solve_string(config, input_format, prefix='(', postfix=')')
    expect_format_re = variable.solve_string(config, expect_format, prefix='(', postfix=')')

    files = list_files_recursively(path)
    input_list = list_matched_files(files, input_format_re)
    expect_list = list_matched_files(files, expect_format_re)

    # sort input_list by index
    input_list = sorted(input_list, key=lambda file: file.index)
    tasks = build_tasks(input_list, expect_list)

    file_format_re = '(' + variable.solve_string(config, input_format) + ')'
    file_name = re.compile(file_format_re)
    tasks = [(input, expect, file_name.findall(input)[0]) for input, expect in tasks]
    return tasks

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
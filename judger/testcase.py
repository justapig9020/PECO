import variable
import os
import re
import itertools

class IndexedFile:
    def __init__(self, index, name):
        self.index = index
        self.name = name


def list_testcases(config):
    path = config['root'] + '/' + variable.solve_string(config, config['testcases']['path'])
    input_format = config['testcases']['format']['input']
    expect_format = config['testcases']['format']['expect']
    input_format_re = variable.solve_string(config, input_format, prefix='(', postfix=')')
    expect_format_re = variable.solve_string(config, expect_format, prefix='(', postfix=')')

    files = list_files_recursively(path)
    input_list = list_matched_files(files, input_format_re)
    expect_list = list_matched_files(files, expect_format_re)
    combinations = itertools.product(input_list, expect_list)

    id_format_re = '(' + variable.solve_string(config, input_format) + ')'
    id = re.compile(id_format_re)
    return [(input.name, expect.name, id.findall(input.name)[0]) for input, expect in combinations if input.index == expect.index]

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
    return [IndexedFile(index, file) for file, index in indexed_files if index != []]
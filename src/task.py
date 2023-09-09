import os
import re

import variable

class IndexedFile:
    def __init__(self, index, name):
        self.index = index
        self.name = name

    def __lt__(self, other):
        return self.index < other.index

class FileMiss(Exception):
    def __init__(self, format_type, index):
        super().__init__(f'File in "{format_type}" type with index "{index}" is missing')

def build_tasks(files_info):
    keys = list(files_info.keys())
    files = {}
    indices = []

    for key in keys:
        files[key] = [file.name for file in files_info[key]]
    if len(keys) > 0:
        indices = [file.index for file in files_info[keys[0]]]

    return (files, indices)

def check_tasks(files_info):
    keys = list(files_info.keys())
    files_mx_cnt = max([len(files_info[key]) for key in keys])

    for i in range(files_mx_cnt):
        for j in range(1, len(keys)):
            if files_info[keys[j - 1]][i].index < files_info[keys[j]][i].index:
                raise FileMiss(keys[j], files_info[keys[j - 1]][i].index)
            elif files_info[keys[j - 1]][i].index > files_info[keys[j]][i].index:
                raise FileMiss(keys[j - 1], files_info[keys[j]][i].index)

def list_tasks(config):
    tasks = config['tasks']
    tasks_path = config['root'] + '/' + variable.solve_string(config, tasks['path'])
    tasks_format = tasks['format']

    files_path = list_files_recursively(tasks_path)
    files_info = {}
    for format_type in tasks_format:
        if format_type == 'index':
            continue
        format_re = variable.solve_string(config, tasks_format[format_type], prefix='(', postfix=')')
        format_list = list_matched_files(files_path, format_re)
        files_info[format_type] = sorted(format_list)

    check_tasks(files_info)
    return build_tasks(files_info)

def list_files_recursively(path):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            result.append(file_path)
    return result

def list_matched_files(files, format):
    # Filter the files
    format = re.compile(format)
    files = [file for file in files]
    indexed_files = [(file, format.findall(file)) for file in files]
    return [IndexedFile(index[0], file) for file, index in indexed_files if index != []]
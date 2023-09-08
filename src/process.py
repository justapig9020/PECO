import yaml
import task
from execute import execute_commands
import os
from os import path
import shutil

class WorkingDirectory(object):
    def __init__(self, working_path):
        self.working_path = working_path

        # Remove all files in the working directory
        if (path.exists(working_path)):
            shutil.rmtree(working_path)

        # Create clean working directory
        os.mkdir(working_path)

    def __enter__(self):
        self.original_path = os.getcwd()
        os.chdir(self.working_path)

    def __exit__(self, type, value, traceback):
        os.chdir(self.original_path)

class SetupFailed(Exception):
    def __init__(self, log):
        super().__init__(f'{log}')

def field_check(config):
    required_fields = ['process', 'tasks']
    reserved_fields = ['root', 'input', 'expect']

    for field in required_fields:
        if field not in config:
            raise Exception(f'Field {field} is required in the config file')

    for field in reserved_fields:
        if field in config:
            raise Exception(f'Field {field} is reserved')

def run(config):
    # Setup
    if 'setup' in config:
        (log, result) = execute_commands(config, 'setup')
        if not result:
            raise SetupFailed(log)

    # List test cases
    tasks = task.list_tasks(config)

    # Process tasks
    test_result = {}
    for input, expect, id in tasks:
        config['input'] = input
        config['expect'] = expect
        (log, result) = execute_commands(config, 'process')
        if result:
            test_result[id] = None
        else:
            test_result[id] = log
    return test_result

def setup_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    field_check(config)
    config['root'] = path.join(os.getcwd(), os.path.dirname(config_file))
    return config

def process_tasks(config_file):
    config = setup_config(config_file)
    build = config['build']['path'] if 'build' in config else 'build'
    root = config['root']
    build = path.join(root, build)

    # Wrap the environment setup and teardown by a context manager
    with WorkingDirectory(build):
        results = run(config)

    return results
import task
from execute import execute_commands
from config import Config
import os
import shutil

class WorkingDirectory(object):
    def __init__(self, working_path):
        self.working_path = working_path

        # Remove all files in the working directory
        if (os.path.exists(working_path)):
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

def process_tasks(config_file):
    # Create a pre-checked configuration which can be used as a dict type
    config = Config(config_file)

    # Wrap the environment setup and teardown by a context manager
    with WorkingDirectory(config['build']['path']):
        results = run(config)

    return results
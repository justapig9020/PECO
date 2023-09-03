import yaml
import testcase
from execute import execute_commands
import os
from os import path
import shutil

class CompileError(Exception):
    def __init__(self, log):
        super().__init__(f'{log}')

def setup_env(config):
    current_env = {
        'pwd': os.getcwd(),
    }
    build = config['build']['path'] if 'build' in config else 'build'
    root = config['root']
    build = path.join(root, build)
    if (path.exists(build)):
        # Remove all files in the build directory
        shutil.rmtree(build)
    os.mkdir(build)
    os.chdir(build)
    return current_env

def resolve_env(env):
    os.chdir(env['pwd'])

def field_check(config):
    required_fields = ['judge', 'testcases']
    reserved_fields = ['root', 'input', 'expect']

    for field in required_fields:
        if field not in config:
            raise Exception(f'Field {field} is required in the config file')

    for field in reserved_fields:
        if field in config:
            raise Exception(f'Field {field} is reserved')

def run(config):
    # Compile
    if 'compile' in config:
        (log, result) = execute_commands(config, 'compile')
        if not result:
            raise CompileError(log)

    # List test cases
    test_cases = testcase.list_testcases(config)

    # Judge
    test_result = {}
    for input, expect, id in test_cases:
        config['input'] = input
        config['expect'] = expect
        (log, result) = execute_commands(config, 'judge')
        if result:
            test_result[id] = None
        else:
            test_result[id] = log
    return test_result

def setup_config(config_file):
    if path.isfile(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    else:
        raise Exception(f'Config file {config_file} is unexisted')
    field_check(config)
    config['root'] = path.join(os.getcwd(), os.path.dirname(config_file))
    return config

def judge(config_file):
    config = setup_config(config_file)
    origin_env = setup_env(config)

    results = run(config)

    resolve_env(origin_env)

    return results
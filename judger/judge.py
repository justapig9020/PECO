import yaml
import testcase
from execute import execute_commands
import os
import shutil

def setup_env(config):
    build = config['build']['path'] if 'build' in config else 'build'
    root = config['root']
    build = f'{root}/{build}'
    if (os.path.exists(build)):
        # Remove all files in the build directory
        shutil.rmtree(build)
    os.mkdir(build)
    os.chdir(build)

def resolve_env(config):
    os.chdir(config['root'])

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
            return {'Compile Error': log}

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

def setup_config(config):
    with open(config, 'r') as f:
        config = yaml.safe_load(f)
    field_check(config)
    config['root'] = os.getcwd()
    return config

def judge(config):
    config = setup_config(config)
    setup_env(config)

    result = run(config)   

    resolve_env(config)

    return result
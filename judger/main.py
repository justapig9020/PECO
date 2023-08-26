import argparse
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

if __name__ == '__main__':
    # the first argument is the path of the config file, the config file is a yaml file

    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='the path of the config file')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    required_fields = ['judge', 'testcases']
    for field in required_fields:
        if field not in config:
            raise Exception(f'Field {field} is required in the config file')

    reserved_fields = ['root', 'input', 'expect']
    for field in reserved_fields:
        if field in config:
            raise Exception(f'Field {field} is reserved')

    config['root'] = os.getcwd()

    setup_env(config)

    # Compile
    if 'compile' in config:
        (log, result) = execute_commands(config, 'compile')

    # List test cases
    test_cases = testcase.list_testcases(config)

    # Judge
    for input, expect in test_cases:
        print(input)
        print(expect)
        config['input'] = input
        config['expect'] = expect
        (log, result) = execute_commands(config, 'judge')
        print(result)
    
    resolve_env(config)
import argparse
import yaml
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

    config['root'] = os.getcwd()

    setup_env(config)
    (log, result) = execute_commands(config, 'compile')
    print(log)
    print(result)
    resolve_env(config)
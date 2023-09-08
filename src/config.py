import os
import yaml

class Config():
    def __init__(self, config_file):
        self.config_file = config_file

        if os.path.isfile(config_file):
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            raise Exception(f'Config file {config_file} is unexisted')

        self.check_required_fields()
        self.create_reserved_fields()

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config

    def check_required_fields(self):
        required_fields = ['process', 'tasks']
        for field in required_fields:
            if field not in self.config:
                raise Exception(f'Field {field} is required in the config file')

    def create_reserved_fields(self):
        reserved_fields = ['root', 'input', 'expect']
        for field in reserved_fields:
            if field in self.config:
                raise Exception(f'Field {field} is reserved')

        self.config['root'] = os.path.join(os.getcwd(), os.path.dirname(self.config_file))

        # Make build path an absolute path
        if 'build' in self.config and 'path' in self.config['build']:
            build_path = self.config['build']['path']
        else:
            self.config['build'] = {}
            build_path = 'build'
        self.config['build']['path'] = os.path.join(self.config['root'], build_path)
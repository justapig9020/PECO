import argparse
from judge import judge

if __name__ == '__main__':
    # the first argument is the path of the config file, the config file is a yaml file
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='the path of the config file')
    args = parser.parse_args()

    result = judge(args.config)
    print(result)
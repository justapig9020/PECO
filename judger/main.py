import argparse
from judge import judge
from report import report

if __name__ == '__main__':
    # the first argument is the path of the config file, the config file is a yaml file
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='the path of the config file')
    args = parser.parse_args()

    results = judge(args.config)

    print(report(results))
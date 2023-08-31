import argparse
from judge import judge
from report import report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # the argument "config", or short in "c", is the path of the config file, the config file is a yaml file
    parser.add_argument('-c', '--config', help='the path of the config file', required=True, type=str)

    # the argument "text-only", or short in "t", indicates not to colorize the output. The argument is default to False
    parser.add_argument('-t', '--text-only', help='do not colorize the output', default=False, action='store_true')

    args = parser.parse_args()

    results = judge(args.config)

    print(report(results, not args.text_only))
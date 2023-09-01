import argparse
from judge import judge
from report import report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # the argument "config", or short in "c", is the path of the config file, the config file is a yaml file
    parser.add_argument('-c', '--config', help='the path of the config file', required=True, type=str)

    # the argument "quiet", or short in "q", is a flag, if it is set, the report will not contain the log of the commands and without colors
    parser.add_argument('-q', '--quiet', help='quiet mode, do not print the log of the commands', action='store_true', default=False)

    args = parser.parse_args()

    results = judge(args.config)

    print(report(results, verbose = not args.quiet))
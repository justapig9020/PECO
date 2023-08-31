from termcolor import colored

def shader(text, color, colorize):
    if colorize:
        return colored(text, color)
    else:
        return text

def report(results, colorize=True):
    # The function returns the report as a string
    # The result is a dict, the key is the name of the test case, the value is the result of the test case
    # If the value is None, it means the test case passed
    # Otherwise, the value is a list of the log of the commands
    # Report the resuls in the following format:
    # If the test case passed:
    #  <test case name>: Passed
    # The Passed is green
    # If the test case failed:
    #  <test case name>: Failed
    #  <log of the commands>
    # The Failed is red

    report = ''
    for testcase, result in results.items():
        if result is None:
            report += f'{testcase}: {shader("Passed", "green", colorize)}\n'
        else:
            report += f'{testcase}: {shader("Failed", "red", colorize)}\n'
            for log in result:
                for command, outcome in log.items():
                    report += '-' * len(command) + '\n'
                    report += f'{command}: \n'
                    if outcome['stdout'] != b'':
                        report += f'stdout:\n'
                        report += f'{outcome["stdout"].decode()}\n'
                        report += '\n'
                    if outcome["stderr"] != b'':
                        report += f'stderr:\n'
                        report += f'{outcome["stderr"].decode()}\n'
                        report += '\n'
    return report
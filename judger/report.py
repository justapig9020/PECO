from termcolor import colored

# Colors
PASSED = "green"
FAILED = "red"
COMMAND = "cyan"
OUTCOME = "magenta"

def shader(text, color, colorize):
    if colorize:
        return colored(text, color)
    else:
        return text

def report(results, verbose=True):
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
            report += f'{testcase}: {shader("Passed", PASSED, verbose)}\n'
        else:
            report += f'{testcase}: {shader("Failed", FAILED, verbose)}\n'
            if not verbose:
                continue
            length = max([len(command) for log in result for command in log.keys()]) + 2
            for log in result:
                for command, outcome in log.items():
                    report += '-' * length + '\n'
                    report += f'{shader(command, COMMAND, verbose)}: \n'
                    if outcome['stdout'] != b'':
                        report += f'{shader("stdout:", OUTCOME, verbose)}\n'
                        report += f'{outcome["stdout"].decode()}\n'
                        report += '\n'
                    if outcome["stderr"] != b'':
                        report += f'{shader("stderr:", OUTCOME, verbose)}\n'
                        report += f'{outcome["stderr"].decode()}\n'
                        report += '\n'
            report += '=' * length + '\n\n'
    # Conclude the report with a summary (Failed / Total)
    if verbose:
        failed = len([result for result in results.values() if result is not None])
        report += f'\nRan {len(results)} test cases, {failed} failed\n'
    return report
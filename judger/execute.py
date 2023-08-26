import subprocess
import variable

def for_all_commands(result):
    return True

def without_fail(result):
    return result.returncode == 0

def default_logger(result):
    return {'stdout': result.stdout.decode(), 'stderr': result.stderr.decode()}

def execute_commands(config, field, logger = default_logger, is_success = without_fail):
    commands = config[field]['commands']
    timeout = config[field]['timeout'] if 'timeout' in config[field] else None
    log = []
    for command in commands:
        command = variable.solve_string(command, config)
        command = command.split(' ')
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        log.append(logger(result))
        if not is_success(result):
            return (log, False)
    return (log, True)
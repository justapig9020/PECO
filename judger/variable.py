import re

def with_variable(string):
    return extract_variables(string) != []

def extract_variables(string):
    var_format = "<([a-zA-Z0-9_:]*)>"
    return re.findall(var_format, string)

def solve_string(config, string, prefix = '', postfix = ''):
    vars = extract_variables(string)
    for var in vars:
        value = get_variable(config, var)
        if with_variable(value):
            value = solve_string(config, value, prefix, postfix)
        value = prefix + value + postfix
        string = solve_variable(string, var, value)
    return string

def solve_variable(string, var, value):
    return string.replace('<' + var + '>', value)

def get_variable(config, var):
    prefix = config['root'] + '/' if var.split('::')[-1] == 'path' else ''
    value = get_variable_inner(config, var)
    return prefix + value

def get_variable_inner(config, var):
    var_list = var.split('::', 1)
    if len(var_list) == 1:
        return config[var_list[0]]
    else:
        return get_variable_inner(config[var_list[0]], var_list[1])

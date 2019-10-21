# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import re

def comment():
    expr = r'#.*\n'
    return re.compile(expr)

def task_graph():
    expr = r'@TASK_GRAPH\s+(?P<identifier>\d+)\s+{\n'
    return re.compile(expr)

def task():
    expr = r'TASK\s+(?P<name>([ab-z]|[0-9])+)\s+TYPE\s+(?P<type>\d+)\s*((HOST|host)\s+(?P<host>\d+))?\n'
    return re.compile(expr)

def channel():
    expr = (r'ARC(\s+)(?P<name>([AB-Z]|[ab-z]|[0-9]|\_)+)\s+(FROM|from)\s+(?P<source>([ab-z]|[0-9])+)\s+(TO|to)\s+'
            '(?P<destination>([ab-z]|[0-9])+)\s+TYPE\s+(?P<type>\d+)\n')
    return re.compile(expr)

def commun_quant():
    expr = r'@COMMUN_QUANT\s+(?P<identifier>\d+)\s+{\n'
    return re.compile(expr)

def commun_value():
    expr = r'(?P<identifier>\d+)\s(?P<value>\d+)E(?P<exponent>\d+)\n'
    return re.compile(expr)

def std_link_value():
    expr = (r'(\s*)(?P<use_price>\d+)\s+(?P<contact_price>\d+(\.\d+)?)\s+(?P<packet_size>\d+)\s+(?P<bit_time>\d+(\.\d+)?(e|E)-\d+)'
            '\s+(?P<power>\d+(\.\d+)?((e|E)-\d+)?)\s+(?P<contacts>\d+)\n')
    return re.compile(expr)

def prim_link_value():
    expr = (r'\s*(?P<c_use_prc>\d+(\.\d+)?)\s+(?P<c_cont_prc>\d+(\.\d+)?)'
            '\s+(?P<s_use_prc>\d+(\.\d+)?)\s+(?P<s_cont_prc>\d+(\.\d+)?)'
            '\s+(?P<packet_size>\d+(\.\d+)?)\s+(?P<bit_time>\d+(\.\d+)?((e|E)(-)?\d+)?)\s+(?P<power>\d+(\.\d+)?((e|E)(-)?\d+)?)\n')
    return re.compile(expr)

def scope_limiter():
    expr = r'}\n'
    return re.compile(expr)

def new_line():
    expr = r'\n'
    return re.compile(expr)

def hw_component():
    expr = r'\s*@(?P<name>([AB-Z]|[ab-z]|[0-9]|\_)+)\s+(?P<identifier>\d+)\s+{\n'
    return re.compile(expr)

def properties():
    expr = (r'\s+(?P<price>\d+(\.\d+)?)\s+(?P<buffered>\d+)\s+(?P<preempt_power>\d+(\.\d+)?)((e|E)-\d+)?\s+(?P<commun_energ_bit>\d+)\s+(?P<io_energ_bit>\d+)\s+'
            '(?P<idle_power>\d+(\.\d+)?)\s*\n')
    return re.compile(expr)

def operation():
    expr = (r'\s*(?P<type>\d+)\s+(?P<version>\d+)\s+(?P<valid>\d+)\s+(?P<task_time>\d+(\.\d+)?((e|E)-\d+)?)\s+(?P<preempt_time>\d+E-\d+)\s+'
            '(?P<code_bits>\d+(\.\d+)?((e|E)\+\d+)?)\s+(?P<task_power>\d+(\.\d+)?)\s*\n')
    return re.compile(expr)

def hyperperiod():
    expr = r'\s*@HYPERPERIOD\s+(?P<value>\d+\.\d+)\n'
    return re.compile(expr)

def hard_deadline():
    expr = r'\s*HARD\_DEADLINE\s+(?P<identifier>([ab-z]|[0-9]|\_)+)\s+(ON|on)\s+(?P<target>([ab-z]|[0-9]|\_)+)\s+(AT|at)\s+(?P<value>\d+(\.\d+)?)\n'
    return re.compile(expr)

def soft_deadline():
    expr = r'\s*SOFT\_DEADLINE\s+(?P<identifier>([ab-z]|[0-9]|\_)+)\s+(ON|on)\s+(?P<target>([ab-z]|[0-9]|\_)+)\s+(AT|at)\s+(?P<value>\d+(\.\d+)?)\n'
    return re.compile(expr)

def period():
    expr = r'\s*PERIOD\s+\d+(\.\d+)?\n'
    return re.compile(expr)

def memory():
    expr = r'\s*@MEMORY\s+(?P<size>\d+)\s+\d+\n'
    return re.compile(expr)


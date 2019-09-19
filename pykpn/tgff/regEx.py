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
    expr = r'TASK\s+(?P<name>([ab-z]|[0-9])+)\s+TYPE\s+(?P<type>\d+)\n'
    return re.compile(expr)

def channel():
    expr = r'ARC(\s+)(?P<name>([AB-Z]|[ab-z]|[0-9]|\_)+)\s+FROM\s+(?P<source>([ab-z]|[0-9])+)\s+TO\s+(?P<destination>([ab-z]|[0-9])+)\s+TYPE\s+(?P<type>\d+)\n'
    return re.compile(expr)

def commun_quant():
    expr = r'@COMMUN_QUANT\s+(?P<identifier>\d+)\s+{\n'
    return re.compile(expr)

def commun_value():
    expr = r'(?P<identifier>\d+)\s(?P<value>\d+)E(?P<exponent>\d+)\n'
    return re.compile(expr)

def link():
    expr = r'@LINK\s+(?P<identifier>\d+)\s+{\n'
    return re.compile(expr)

def link_type():
    expr = r'(\s*)(?P<identifier>\d+)\s+(\d+((\.|\d+)*))\s+(?P<size>\d+).*\n'
    return re.compile(expr)

def scope_limiter():
    expr = r'}\n'
    return re.compile(expr)

def new_line():
    expr = r'\n'
    return re.compile(expr)

def process():
    expr = r'@PROC\s+(?P<identifier>\d+)\s+{\n'
    return re.compile(expr)

def propertys():
    expr = r'\s+(?P<price>\d+)\s+(?P<buffered>\d+)\s+(?P<preempt_power>\d+\.\d+)\s+(?P<commun_energ_bit>\d+)\s+(?P<io_energ_bit>\s+)\s+(?P<idle_power>\d+\.\d+)\s+\n'
    return re.compile(expr)

def operation():
    expr_head = r'\s+(?P<type>\d+)\s+(?P<version>\d+)\s+(?P<valid>\d+)\s+(?P<task_time>\((d+(\.\d+){0,1}(e|E)-\d+)|(\d+\.\d+)))'
    expr_tail = r'\s+(?P<preempt_time>\d+E-\d+)\s+(?P<code_bits>)\s+(?P<task_power>)\s+\n'
    return re.compile(expr_head + expr_tail)


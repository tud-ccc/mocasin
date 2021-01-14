# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import re

"""Including the regular expressions to recognize all patterns that can occur in a .tgff file. 
For patterns which encode relevant information, a useful grouping is applied for parsing.
"""


def new_line():
    expr = r"\n"
    return re.compile(expr)


def comment():
    expr = r"#(?P<comment>.*)\n"
    return re.compile(expr)


def task_graph():
    expr = r"@TASK_GRAPH\s+(?P<identifier>\d+)\s+{\n"
    return re.compile(expr)


def task():
    expr = (
        r"TASK\s+(?P<name>([ab-z]|[0-9]|\-|\_)+)"
        r"\s+TYPE\s+(?P<type>\d+)"
        r"\s*((HOST|host)\s+(?P<host>\d+))?\s*\n"
    )
    return re.compile(expr)


def channel():
    expr = (
        r"ARC(\s+)(?P<name>([AB-Z]|[ab-z]|[0-9]|\-|\_)+)"
        r"\s+(FROM|from)"
        r"\s+(?P<source>([ab-z]|[0-9]|\-|\_)+)"
        r"\s+(TO|to)\s+(?P<destination>([ab-z]|[0-9]|\-|\_)+)"
        r"\s+TYPE\s+(?P<type>\d+)\n"
    )
    return re.compile(expr)


def commun_quant():
    expr = r"@COMMUN_QUANT\s+(?P<identifier>\d+)\s+{\n"
    return re.compile(expr)


def commun_value():
    expr = r"(?P<identifier>\d+)\s+(?P<value>(\d|E|e|\.)+)\n"
    return re.compile(expr)


def std_link_value():
    expr = (
        r"(\s*)(?P<use_price>\d+)"
        r"\s+(?P<contact_price>\d+(\.\d+)?)"
        r"\s+(?P<packet_size>\d+)"
        r"\s+(?P<bit_time>\d+(\.\d+)?(e|E)-\d+)"
        r"\s+(?P<power>\d+(\.\d+)?((e|E)-\d+)?)"
        r"\s+(?P<contacts>\d+)\n"
    )
    return re.compile(expr)


def prim_link_value():
    expr = (
        r"\s*(?P<c_use_prc>\d+(\.\d+)?)"
        r"\s+(?P<c_cont_prc>\d+(\.\d+)?)"
        r"\s+(?P<s_use_prc>\d+(\.\d+)?)"
        r"\s+(?P<s_cont_prc>\d+(\.\d+)?)"
        r"\s+(?P<packet_size>\d+(\.\d+)?)"
        r"\s+(?P<bit_time>\d+(\.\d+)?((e|E)(-)?\d+)?)"
        r"\s+(?P<power>\d+(\.\d+)?((e|E)(-)?\d+)?)\n"
    )
    return re.compile(expr)


def scope_limiter():
    expr = r"\s*}\s*\n"
    return re.compile(expr)


def hw_component():
    expr = (
        r"\s*@(?P<name>([AB-Z]|[ab-z]|[0-9]|\_)+)"
        r"\s+(?P<identifier>\d+)\s+{\n"
    )
    return re.compile(expr)


def properties():
    expr = (
        r"\s+(?P<price>\d+(\.|(\.\d+))?)"
        r"\s+(?P<buffered>\d+)"
        r"(\s+(?P<max_freq>\d+(\.\d+)?((e|E)(\+|\-)\d+)?))?"
        r"(\s+(?P<width>\d+(\.\d+)?((e|E)(\+|\-)\d+)?))?"
        r"(\s+(?P<height>\d+(\.\d+)?((e|E)(\+|\-)\d+)?))?"
        r"(\s+(?P<density>\d+(\.\d+)?((e|E)(\+|\-)\d+)?))?"
        r"(\s+(?P<preempt_power>\d+(\.\d+)?((e|E)(\+|\-)\d+)?))?"
        r"\s+(?P<commun_energ_bit>\d+)"
        r"\s+(?P<io_energ_bit>\d+)"
        r"\s+(?P<idle_power>\d+(\.\d+)?)\s*\n"
    )
    return re.compile(expr)


def operation():
    expr = (
        r"\s*(?P<type>\d+)"
        r"\s+(?P<version>\d+)"
        r"\s+(?P<valid>\d+)"
        r"\s+(?P<task_time>\d+(\.\d+)?((e|E)-\d+)?)"
        r"\s+(?P<preempt_time>\d+E-\d+)"
        r"\s+(?P<code_bits>\d+(\.\d+)?((e|E)\+\d+)?)"
        r"\s+(?P<task_power>\d+(\.\d+)?)\s*\n"
    )
    return re.compile(expr)


def hyperperiod():
    expr = r"\s*@HYPERPERIOD\s+(?P<value>\d+\.\d+)\n"
    return re.compile(expr)


def hard_deadline():
    expr = (
        r"\s*HARD\_DEADLINE\s+(?P<identifier>([ab-z]|[0-9]|\_)+)\s+(ON|on)"
        r"\s+(?P<target>([ab-z]|[0-9]|\_)+)\s+(AT|at)"
        r"\s+(?P<value>\d+(\.\d+)?)\n"
    )
    return re.compile(expr)


def soft_deadline():
    expr = (
        r"\s*SOFT\_DEADLINE\s+(?P<identifier>([ab-z]|[0-9]|\_)+)\s+(ON|on)"
        r"\s+(?P<target>([ab-z]|[0-9]|\_)+)\s+(AT|at)"
        r"\s+(?P<value>\d+(\.\d+)?)\n"
    )
    return re.compile(expr)


def period():
    expr = r"\s*PERIOD\s+\d+(\.\d+)?\n"
    return re.compile(expr)


def unused_statement():
    expr = r"\s*(@([AB-Z]|\_)*)?(([0-9]|E|\.|-)*\s*)+\n"
    return re.compile(expr)


def unused_scope():
    expr = r"\s*@([AB-Z]|\_)+\s+{\s*\n"
    return re.compile(expr)

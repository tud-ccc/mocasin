# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


"""This module manages the executable tasks that are available within pykpn

To add a new task, write a function within a module within this package and add
a descriptor tuple to the :attr:`_tasks` dict. The tuple should have three
entries. The first is the name of the module that defines the task function,
the second is the name of the task function and the third is a description of
the task that is printed when running ``pykpn help``.  Each task function
should be annotated with ``@hydra.main`` and expect precisely one parameter,
the Omniconf object as created by hydra.
"""

import hydra
import logging
import sys
import textwrap

from importlib import import_module

log = logging.getLogger(__name__)


@hydra.main(config_path='conf/help.yaml')
def print_help(cfg=None):
    _print_help_impl()


_tasks = {
    'csv_plot': (
        'csv_plot',
        'csv_plot',
        "???"),
    'design_centering': (
        'design_centering',
        'dc_task',
        "generate a mapping using the design centering algorityh"),
    'enumerate_equivalent': (
        'enumerate_equivalent',
        'enumerate_equivalent',
        "ennumerate all mappings equivalent to the given mapping"),
    'generate_mapping': (
        'generate_mapping',
        'generate_mapping',
        "Generate a mapping."),
    'generate_yaml': (
        'generate_yaml',
        'generate_yaml',
        "Generates a bunch of yaml files"),
    'help': (
        None,
        None,
        "Print a help message"),
    'kpn_to_dot': (
        'to_dot',
        'kpn_to_dot',
        "Visualize a KPN application as a dot graph"),
    'mapping_to_dot': (
        'to_dot',
        'mapping_to_dot',
        "Visualize a mapping as a dot graph"),
    'platform_to_autgrp': (
        'platform_to_autgrp',
        'platform_to_autgrp',
        "Calculate the Automorphism Group of a Platform Graph"),
    'platform_to_dot': (
        'to_dot',
        'platform_to_dot',
        "Visualize a platform as a dot graph"),
    'simulate': (
        'simulate',
        'simulate',
        "Replay traces to simulate the execution of a KPN application on a "
        "given platform"),
    'solve_query' : (
        'solve_query',
        'solve_query',
        "Generates a mapping based on constraints expressed in a query language"),
    'visualize': (
        'visualize',
        'visualize',
        "Visualize a mapping in the GUI"),
    'tetris' : (
        tetris,
        "Run TETRiS scheduler")
}
"""A dictionary that maps task names to descriptors of callable functions."""


def _print_help_impl():
    print("pykpn is a framework for modeling KPN applications and their")
    print("execution on MPSoC platforms.")
    print("")
    print("Usage: pykpn TASK [PYKPN OPTIONS] [HYDRA OPTIONS]")
    print("")
    print("pykpn can perform one of several tasks. It expects the first ")
    print("argument to specify the task to be executed.")
    print("")
    print("Available pykpn tasks:")
    for kv in _tasks.items():
        desc = kv[1][2]
        desc_lines = textwrap.wrap(desc, width=41)
        task = "  %s: " % kv[0]
        print("%s%s" % ("{:<24}".format(task), desc_lines[0]))
        for line in desc_lines[1:]:
            print("%s%s" % ("{:<24}".format(''), line))
    print("")
    print("Optional arguments:")
    print(" --no-fail-on-exception If this flag is given, pykpn does not exit")
    print("                        with an error code in case of an internal")
    print("                        exception. This is useful in combination")
    print("                        with hydra mutlirun if execution should")
    print("                        continue even when one job failed.")


def execute_task(task):
    """Executes an individual task.

    :param task: name of the task to be executed
    :return:
    """

    if task is None:
        log.error("ERROR: You need to specify a task!\n")
        print_help()
        sys.exit(-1)

    if task not in _tasks:
        log.error("ERROR: Tried to run a task unknown to pykpn (%s)\n" % task)
        print_help()
        sys.exit(-1)

    if task == 'help':
        print_help()
    else:
        # load the task
        module_name = _tasks[task][0]
        function_name = _tasks[task][1]
        module = import_module(f"pykpn.tasks.{module_name}")
        function = getattr(module, function_name)
        # execute the task
        function()

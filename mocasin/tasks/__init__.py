# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


"""This module describes all entrypoints (tasks) provided by mocasin.

To add a new task, simply define a function within this module. Each function
will automatically become available as a mocasin task. Each function should
provide a docstring, as this is used for generating a help text for the command
line interface.

Note that each task function should be annotated with ``@hydra.main`` and
expect precisely one parameter, the OmegaCconf object as created by hydra. Note
that we import any necessary modules only within the functions and not
globally. This significantly speeds up the runtime of individual tasks as well
as the shell auto completion.
"""

import hydra


@hydra.main(config_path="conf", config_name="find_design_center", version_base="1.1")
def find_design_center(cfg):
    """generate a mapping using the design centering algorithm"""
    from mocasin.tasks.find_design_center import dc_task

    dc_task(cfg)


@hydra.main(config_path="conf", config_name="enumerate_equivalent", version_base="1.1")
def enumerate_equivalent(cfg):
    """ennumerate all mappings equivalent to the given mapping"""
    from mocasin.tasks.enumerate_equivalent import enumerate_equivalent

    enumerate_equivalent(cfg)


@hydra.main(config_path="conf", config_name="generate_mapping", version_base="1.1")
def generate_mapping(cfg):
    """Generate a mapping"""
    from mocasin.tasks.generate_mapping import generate_mapping

    generate_mapping(cfg)


@hydra.main(config_path="conf/", config_name="pareto_front.yaml", version_base="1.1")
def pareto_front(cfg):
    """Generate a pareto front of mappings"""
    from mocasin.tasks.pareto_front import pareto_front

    pareto_front(cfg)


@hydra.main(config_path="conf", config_name="graph_to_dot", version_base="1.1")
def graph_to_dot(cfg):
    """Visualize a dataflow application as a dot graph"""
    from mocasin.tasks.to_dot import graph_to_dot

    graph_to_dot(cfg)


@hydra.main(config_path="conf", config_name="platform_to_dot.yaml", version_base="1.1")
def platform_to_dot(cfg):
    """Visualize a platform as a dot graph"""
    from mocasin.tasks.to_dot import platform_to_dot

    platform_to_dot(cfg)


@hydra.main(config_path="conf", config_name="mapping_to_dot.yaml", version_base="1.1")
def mapping_to_dot(cfg):
    """Visualize a mapping as a dot graph"""
    from mocasin.tasks.to_dot import mapping_to_dot

    mapping_to_dot(cfg)


@hydra.main(config_path="conf", config_name="calculate_platform_embedding", version_base="1.1")
def calculate_platform_embedding(cfg):
    """Calculate a low-distortion embedding for a platform"""
    from mocasin.tasks.calculate_platform_embedding import (
        calculate_platform_embedding,
    )

    calculate_platform_embedding(cfg)


@hydra.main(config_path="conf", config_name="calculate_platform_symmetries", version_base="1.1")
def calculate_platform_symmetries(cfg):
    """Calculate the automorphism group of a platform graph"""
    from mocasin.tasks.calculate_platform_symmetries import (
        calculate_platform_symmetries,
    )

    calculate_platform_symmetries(cfg)


@hydra.main(config_path="conf", config_name="simulate", version_base="1.1")
def simulate(cfg):
    """Replay traces to simulate the execution of a dataflow application on a
    given platform
    """
    from mocasin.tasks.simulate import simulate

    simulate(cfg)


@hydra.main(config_path="conf", config_name="solve_query.yaml", version_base="1.1")
def solve_query(cfg):
    """Generates a mapping based on constraints expressed in a query language"""
    from mocasin.tasks.solve_query import solve_query

    solve_query(cfg)


@hydra.main(config_path="conf", config_name="tetris_scheduler", version_base="1.1")
def tetris_scheduler(cfg):
    """Run the Tetris scheduler for a single input state"""
    from mocasin.tasks.tetris import tetris_scheduler

    tetris_scheduler(cfg)


@hydra.main(config_path="conf", config_name="tetris_manager", version_base="1.1")
def tetris_manager(cfg):
    """Run the Tetris manager"""
    from mocasin.tasks.tetris import tetris_manager

    tetris_manager(cfg)


@hydra.main(config_path="conf", config_name="visualize", version_base="1.1")
def visualize(cfg):
    """Visualize a mapping in the GUI"""
    from mocasin.tasks.visualize import visualize

    visualize(cfg)


@hydra.main(config_path="conf", config_name="parse_multirun", version_base="1.1")
def parse_multirun(cfg):
    """Parse the directory structure after executing a multirun job"""
    from mocasin.tasks.parse_multirun import parse_multirun

    parse_multirun(cfg)

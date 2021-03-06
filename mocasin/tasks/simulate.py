# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import hydra
import logging
import timeit
import os
import csv


log = logging.getLogger(__name__)


def simulate(cfg):
    """Simulate the execution of a dataflow application mapped to a platform.

    This script expects a configuration file as the first positional argument.
    It constructs a system according to this configuration and simulates
    it. Finally, the script reports the simulated execution time.

    This task expects four hydra parameters to be available.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **graph:** the input dataflow graph. The task expects a configuration dict
          that can be instantiated to a :class:`~mocasin.common.graph.DataflowGraph`
          object.
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **mapping:** the input mapping. The task expects a configuration dict
          that can be instantiated to a :class:`~mocasin.common.mapping.Mapping`
          object.
        * **trace:** the input trace. The task expects a configuration dict
          that can be instantiated to a
          :class:`~mocasin.common.trace.TraceGenerator` object.
    """

    trace_cfg = cfg["simtrace"]
    simulation = hydra.utils.instantiate(cfg.simulation_type, cfg)

    with simulation:
        if trace_cfg is not None and trace_cfg["file"] is not None:
            simulation.system.app_trace_enabled = trace_cfg["app"]
            simulation.system.platform_trace_enabled = trace_cfg["platform"]
            load_cfg = trace_cfg["load"]
            if load_cfg is not None:
                simulation.system.load_trace_cfg = (
                    load_cfg["granularity"],
                    load_cfg["time_frame"],
                )

        log.info("Start the simulation")
        start = timeit.default_timer()
        simulation.run()
        stop = timeit.default_timer()
        log.info("Simulation done")

        result = simulation.result

        exec_time = float(result.exec_time) / 1000000000.0
        print("Total simulated time: " + str(exec_time) + " ms")
        print("Total simulation time: " + str(stop - start) + " s")
        summary = {}
        summary["Total_simulated_time_ms"] = str(exec_time)
        summary["Total_simulation_time_s"] = str(stop - start)

        if result.total_energy is not None:
            total_energy = float(result.total_energy) / 1000000000.0
            static_energy = float(result.static_energy) / 1000000000.0
            dynamic_energy = float(result.dynamic_energy) / 1000000000.0
            avg_power = total_energy / exec_time
            print(f"Total energy consumption: {total_energy:.9f} mJ")
            print(f"      ---  static energy: {static_energy:.9f} mJ")
            print(f"      --- dynamic energy: {dynamic_energy:.9f} mJ")
            print(f"Average power: {avg_power:.6f} W")

            summary["total_energy_mj"] = f"{total_energy:.9f}"
            summary["static_energy_mj"] = f"{static_energy:.9f}"
            summary["dynamic_energy_mj"] = f"{dynamic_energy:.9f}"
            summary["avg_power_W"] = f"{avg_power:.6f}"

        summary_to_file(summary)

        if trace_cfg is not None and trace_cfg["file"] is not None:
            simulation.system.write_simulation_trace(trace_cfg["file"])
        hydra.utils.call(cfg["cleanup"])


def summary_to_file(summary):
    with open("summary.csv", "x") as file:
        writer = csv.writer(
            file,
            delimiter=",",
            lineterminator="\n",
        )
        writer.writerow(summary.keys())
        writer.writerow(summary.values())


def summary_parser(dir):
    results = {}
    try:
        with open(os.path.join(dir, "summary.csv"), "r") as f:
            reader = csv.reader(f, delimiter=",")
            headers = next(reader)
            results = dict(zip(headers, next(reader)))

        return results, headers
    except FileNotFoundError:
        return {}, []

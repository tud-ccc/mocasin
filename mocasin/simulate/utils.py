# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Julian Robledo

import os
from mocasin.util.logging import getLogger

log = getLogger(__name__)


def summary_parser(dir):
    results = {}
    try:
        with open(os.path.join(dir, "summary.txt"), "r") as f:
            results["simulated_time"] = float(
                f.readline().replace("Total simulated time (ms): ", "")
            )
            results["simulation_time"] = float(
                f.readline().replace("Total simulation time (s): ", "")
            )
            total_energy = f.readline()
            if len(total_energy) > 0:
                results["total_energy"] = float(
                    total_energy.replace("Total energy consumption (mJ): ", "")
                )
                results["static_energy"] = float(
                    f.readline().replace("Static energy (mJ): ", "")
                )
                results["dynamic_energy"] = float(
                    f.readline().replace("Dynamic energy (mJ): ", "")
                )
                results["average_power"] = float(
                    f.readline().replace("Average power (W): ", "")
                )
        return results, list(results.keys())
    except FileNotFoundError:
        return {}, []

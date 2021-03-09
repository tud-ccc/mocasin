# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.tetris.job_request import JobRequestInfo

from mocasin.maps.graph import MapsDataflowGraph
from mocasin.util.mapping_table import MappingTableReader

import csv
import logging
import math
import os

log = logging.getLogger(__name__)

CPN_FILENAME = "cpn.xml"
MAPPINGS_SUFFIX = ".mappings.csv"


def read_applications(base_dir, platform):
    """Read application and mappings from base directory.

    The base directory includes the subdirectories with the name of application,
    each subdirectory consists of cpn.xml describing the application, and
    <platform>.mappings.csv describing canonical mappings.

    Args:
        base_dir (str): path to base directiry
        platform (Platform): a platform

    Returns:
        a dict {app_name: (graph, [mapping, ..])}
    """
    assert os.path.isdir(base_dir), "The folder '{}' does not exist".format(
        base_dir
    )
    log.info("Reading applications:")
    apps = {}
    for name in os.listdir(base_dir):
        app_folder = os.path.join(base_dir, name)
        if not os.path.isdir(app_folder):
            continue
        app_file = os.path.join(app_folder, CPN_FILENAME)
        graph = MapsDataflowGraph(name, app_file)
        mapping_file = os.path.join(app_folder, platform.name + MAPPINGS_SUFFIX)
        mappings_reader = MappingTableReader(platform, graph, mapping_file)
        mappings = [m[0] for m in mappings_reader.form_mappings()]
        apps.update({name: (graph, mappings)})
        log.info("   * {}".format(name))
    return apps


def read_requests(jobs_file, apps):
    """Read job requests and their state states.

    Example of csv file:
    app,arrival,deadline,start_cratio
    sr.B,0,29.94,0.00

    Args:
        jobs_file (str): a path to jobs file
        apps (dict): a dict of application and mappings created by
            read_applications
    """
    reqs = []
    with open(jobs_file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            app = apps[row["app"]][0]
            mappings = apps[row["app"]][1]
            start_cratio = float(row.get("start_cratio", 0.0))
            deadline = float(row["deadline"])
            if deadline < 0:
                deadline = math.inf
            request = JobRequestInfo(
                app,
                mappings,
                float(row["arrival"]),
                deadline=deadline,
                start_cratio=start_cratio,
            )
            reqs.append(request)
    return reqs

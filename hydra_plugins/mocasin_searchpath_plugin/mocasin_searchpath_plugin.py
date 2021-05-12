# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import os
import mocasin

from hydra.plugins.search_path_plugin import SearchPathPlugin
from omegaconf import OmegaConf


class MocasinSearchPathPlugin(SearchPathPlugin):
    """
    A hydra plugin that extends the search path that hydra uses to find
    configurations.

    The plugin adds all directories specified in environment variable
    ~MOCASIN_CONF_PATH~ to the search path. The plugin expects a ':' separated
    list of paths which it prepends to the search path.

    The plugin also provides a custom resolver ``mocasin_path`` for reading
    files from the mocasin package.
    """

    def __init__(self):
        # register a custom resolver to resolve paths to files located within
        # the mocasin package
        OmegaConf.register_resolver(
            "mocasin_path",
            lambda path="": os.path.join(
                os.path.dirname(mocasin.__file__), path
            ),
        )

    def manipulate_search_path(self, search_path):
        # prepend paths from the environment variable MOCASIN_CONF_PATH
        mocasin_conf_path = os.environ.get("MOCASIN_CONF_PATH")
        if mocasin_conf_path is not None:
            split = mocasin_conf_path.split(":")
            for path in split:
                search_path.prepend(
                    provider="mocasin-searchpath-plugin",
                    path=path,
                    anchor="main",
                )

        # also append mocasins own config to make it available for plugins that
        # provide their own entry points
        search_path.append(
            provider="mocasin",
            path="pkg://mocasin.conf",
            anchor="main",
        )

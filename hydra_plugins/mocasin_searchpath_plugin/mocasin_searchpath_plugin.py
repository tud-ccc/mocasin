# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import os

from hydra.plugins.search_path_plugin import SearchPathPlugin


class MocasinSearchPathPlugin(SearchPathPlugin):
    """
    A hydra plugin that extends the search path that hydra uses to find
    configurations.

    The plugin adds all directories specified in environment variable
    ~MOCASIN_CONF_PATH~ to the search path. The plugin expects a ':' separated
    list of paths which it prepends to the search path.
    """

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

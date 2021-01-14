# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import os

from hydra.plugins.search_path_plugin import SearchPathPlugin


class MocasinSearchPathPlugin(SearchPathPlugin):
    """
    A hydra plugin that extends the search path that hydra uses to find
    configurations.

    The plugin adds the directory 'conf/' relative to the CWD which allows
    users to define project specific configuration. In case multiple
    configuration directories are required or users want to point to other
    directories, the user can set the environment variable ~MOCASIN_CONF_PATH~.
    The plugin expects a ':' separated list of paths which it appends to the
    search path.
    """

    def manipulate_search_path(self, search_path):
        search_path.prepend(
            provider="mocasin-searchpath-plugin", path="conf/", anchor="main"
        )

        # append paths from the environment variable MOCASIN_CONF_PATH
        mocasin_conf_path = os.environ.get("MOCASIN_CONF_PATH")
        if mocasin_conf_path is not None:
            split = mocasin_conf_path.split(":")
            for path in split:
                search_path.prepend(
                    provider="mocasin-searchpath-plugin",
                    path=path,
                    anchor="main",
                )

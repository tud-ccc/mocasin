# Copyright (C) 2021 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

from hydra.plugins.search_path_plugin import SearchPathPlugin


class MocasinExampleSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path):
        search_path.append(
            provider="mocasin-example-plugin",
            path="pkg://mocasin_example_plugin.conf",
            anchor="main",
        )

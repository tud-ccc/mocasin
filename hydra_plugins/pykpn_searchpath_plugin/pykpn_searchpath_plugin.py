# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

from hydra.plugins.search_path_plugin import SearchPathPlugin


class PykpnSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path):
        search_path.append(
            provider="pykpn-searchpath-plugin", path="conf/")

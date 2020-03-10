# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
from pykpn.util import logging
from pykpn.tgff.tgffParser.parser import Parser

logger = logging.getLogger('tgff_parser_test')


@pytest.fixture
def graph_dict():
    parser = Parser()
    data = parser.parse_file('examples/tgff/e3s-0.9/auto-indust-cords.tgff')
    return data[0]


@pytest.fixture
def processor_list():
    parser = Parser()
    data = parser.parse_file('examples/tgff/e3s-0.9/auto-indust-cowls.tgff')
    return data[1]


@pytest.fixture
def link_dict():
    parser = Parser()
    data = parser.parse_file('examples/tgff/e3s-0.9/consumer-cords.tgff')
    return data[2]


@pytest.fixture
def communication_quantities():
    parser = Parser()
    data = parser.parse_file('examples/tgff/e3s-0.9/consumer-cowls.tgff')
    return data[3]

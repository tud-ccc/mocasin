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
    data = None
    try:
        data = parser.parse_file('pykpn/tgff/graphs/auto-indust-cords.tgff')
    except:
        logger.error('Error parsing: auto-indust-cords.tgff')
    return data[0]

@pytest.fixture
def processor_dict():
    parser = Parser()
    data = None
    try:
        data = parser.parse_file('pykpn/tgff/graphs/auto-indust-cowls.tgff')
    except:
        logger.error('Error parsing: auto-indust-cowls.tgff')
    return data[1]

@pytest.fixture
def link_dict():
    parser = Parser()
    data = None
    try:
        data = parser.parse_file('pykpn/tgff/graphs/consumer-cords.tgff')
    except:
        logger.error('Error parsing: consumer-cords.tgff')
    return data[2]

@pytest.fixture
def communication_quantities():
    parser = Parser()
    data = None
    try:
        data = parser.parse_file('pykpn/tgff/graphs/consumer-cowls.tgff')
    except:
        logger.error('Error parsing: consumer-cowls.tgff')
    return data[3]



# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
from termcolor import colored


COLORS = {
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'DEBUG': 'blue'
}


_indent_level = 0


def increment_logger_indent():
    global _indent_level
    _indent_level += 1


def decrement_logger_indent():
    global _indent_level
    _indent_level -= 1
    assert _indent_level >= 0


class PykpnFormatter(logging.Formatter):

    def __init__(self, msg, use_color):
        super().__init__(msg)
        self._use_color = use_color

    def format(self, record):
        # add brackets
        levelname = '[%s]' % (record.levelname)
        # fill with spaces
        levelname = '%-10s' % (levelname)
        # colorize
        if self._use_color:
            if record.levelname in COLORS:
                color = COLORS[record.levelname]
            else:
                color = 'white'
            levelname = colored(levelname, color, attrs=['bold'])
        record.levelname = levelname

        global _indent_level
        if _indent_level > 0:
            indent_string = '%s* ' % (' ' * _indent_level * 2)
            record.msg = indent_string + record.msg

        return super().format(record)


def setup_root_logger(level, filters=None, use_color=True):
    logger = logging.getLogger('pykpn')
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    if filters is not None:
        for f in filters:
            logger.addFilter(logging.Filter(f))

    formatter = PykpnFormatter('%(levelname)s %(message)s', use_color)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging as l
from termcolor import colored


COLORS = {
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'DEBUG': 'blue'
}


_indent_level = 0


def inc_indent():
    global _indent_level
    _indent_level += 1


def dec_indent():
    global _indent_level
    _indent_level -= 1
    assert _indent_level >= 0


class PykpnFormatter(l.Formatter):

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


class WhitelistFilter(l.Filter):

    def __init__(self, names):
        self._filters = [l.Filter(n) for n in names]

    def filter(self, record):
        return any(f.filter(record) for f in self._filters)


def setup(level, filters=None, use_color=True):
    logger = l.getLogger('pykpn')
    logger.setLevel(level)

    handler = l.StreamHandler()
    handler.setLevel(level)

    if filters is None:
        filters = []
    handler.addFilter(WhitelistFilter(filters))

    formatter = PykpnFormatter('%(levelname)s %(message)s', use_color)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def add_cli_args(parser):
    parser.add_argument(
        '-v',
        '--verbosity',
        action="count",
        help="increase output verbosity (e.g., -vv is more than -v)",
        dest='verbosity')

    parser.add_argument(
        '-f',
        '--filter',
        action="append",
        help="add a log filter (e.g. pykpn.common)",
        dest='filter')

    parser.add_argument(
        '--no-color',
        action="store_false",
        help="disable colored output",
        dest='color')
    parser.set_defaults(color=True)


def setup_from_args(args):
    log_level = l.WARNING
    if args.verbosity is not None:
        if args.verbosity >= 2:
            log_level = l.DEBUG
        elif args.verbosity >= 1:
            log_level = l.INFO

    setup(log_level, args.filter, args.color)


def getLogger(name):
    return l.getLogger(name)

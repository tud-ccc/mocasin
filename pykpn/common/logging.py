# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging as l
import re

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
        levelname = '%-9s' % (levelname)
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

        # ensure that multiline messages are properly indented
        record.msg = record.msg.replace('\n', '\n%s' % (
            ' ' * (10 + _indent_level * 2)))

        return super().format(record)


class WhitelistFilter(l.Filter):

    def __init__(self, names):
        self._filters = [l.Filter(n) for n in names]

    def filter(self, record):
        if record.levelno > l.DEBUG:
            return True
        else:
            return any(f.filter(record) for f in self._filters)


class BlacklistFilter(l.Filter):

    def __init__(self, names):
        self._filters = [l.Filter(n) for n in names]

    def filter(self, record):
        if record.levelno > l.DEBUG:
            return True
        else:
            return not any(f.filter(record) for f in self._filters)


class RegexFilter(l.Filter):

    def __init__(self, regex):
        self._pattern = re.compile(regex)

    def filter(self, record):
        if record.levelno > l.DEBUG:
            return True
        else:
            return bool(self._pattern.search(record.msg))


def setup(level, whitelist=None, blacklist=None, message_filer=None,
          use_color=True):
    logger = l.getLogger('')
    logger.setLevel(level)

    handler = l.StreamHandler()
    handler.setLevel(level)

    if whitelist is not None:
        handler.addFilter(WhitelistFilter(whitelist))
    if blacklist is not None:
        handler.addFilter(BlacklistFilter(blacklist))
    if message_filer is not None:
        handler.addFilter(RegexFilter(message_filer))

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
        '-s',
        '--silent',
        action="store_true",
        help='suppress all output except errors (overrides verbosity)',
        dest='silent')

    parser.add_argument(
        '-w',
        '--log-whitelist',
        nargs='+',
        help='add a log whitelist filter (e.g. pykpn.common)',
        dest='whitelist')

    parser.add_argument(
        '-b',
        '--log-blacklist',
        nargs='+',
        help='add a log blacklist filter (e.g. pykpn.common)',
        dest='blacklist')

    parser.add_argument(
        '-r',
        '--log-regex',
        type=str,
        help='Add a regex filter that matches the message',
        dest='regex')

    parser.add_argument(
        '--no-color',
        action="store_false",
        help="disable colored output",
        dest='color')
    parser.set_defaults(color=True)


def setup_from_args(args):
    if args.silent:
        log_level = l.ERROR
    elif args.verbosity is not None:
        if args.verbosity >= 2:
            log_level = l.DEBUG
        elif args.verbosity >= 1:
            log_level = l.INFO
    else:
        log_level = l.WARNING

    setup(log_level, args.whitelist, args.blacklist, args.regex, args.color)


def getLogger(name):
    return l.getLogger(name)

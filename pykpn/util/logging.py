# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


"""Utility module for improved logging functionality

This module extends the functionality provided by the :mod:`logging` package.
It provides a custom formatter (:class:`PykpnFormatter`) that produces colored
output as well as classes for filtering the log stream
(:class:`BlacklistFilter`, :class:`WhitelistFilter`, :class:`RegexFilter`). The
:func:`setup` function can be used to configure the default logger to use a
:class:`PykpnFormatter` and to optionally apply any filters.

For convenience, this module also provides the functions :func:`add_cli_args`
and :func:`setup_from_args` that allow extend a cli argument parser with
options for controlling the logging and to apply these options to the default
logger. See the code below for an example of usage.

.. code-block:: py

   import argparse
   from pykpn.util import logging

   log = logging.getLogger(__name__)

   def main():
       parser = argparse.ArgumentParser()
       logging.add_cli_args(parser)
       # add more args here ...
       args = parser.parse_args()
       logging.setup_from_args(args)

       log.info("Info Test")
       log.debug("Debug Test")
       log.warn("Warning Test")
       log.error("Error Test")

       # do something useful ...

   if __name__ == '__main__':
       main()
"""


import logging as l
import re

from termcolor import colored


COLORS = {
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'DEBUG': 'blue'
}
"""Maps logging levels to colors"""


_indent_level = 0
"""The current level of indentation"""


def inc_indent():
    """Increment the indentation level"""
    global _indent_level
    _indent_level += 1


def dec_indent():
    """Decrement the indentation level"""
    global _indent_level
    _indent_level -= 1
    assert _indent_level >= 0


class PykpnFormatter(l.Formatter):
    """A custom pykpn logging formatter

    This formatter deviates from the default implementation
    :class:`logging.Formatter` by providing a colored output. ``%(levelname)``
    in the format string is replaced by the name of the current logging level
    enclosed in brackets and printed in the color as defined in
    :data:`COLORS`. The string is further filled with spaces to ensure that the
    actual logging message always start at the same position. If the
    indentation level was increased using :func:`inc_indent`, the formatter add
    additional white spaces to increment the output.

    Attributes:
        _use_color (bool): Flag indicating whether colored output should be
            produced

    Args:
        fmt (str): Format string as expected by :class:`logging.Formatter`
        use_color(bool): Produce colored output if ``True``
    """

    def __init__(self, fmt, use_color):
        super().__init__(fmt=fmt)
        self._use_color = use_color

    def format(self, record):
        """Format a given record

        See :class:`PykpnFormatter` for details.
        """
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
    """A filter that whitelists DEBUG messages of certain loggers

    Attributes:
        _filter(list(~logging.Filter)): A list of filters generated from ``names``

    Args:
        names (list(str)): A list of names to be whitelisted
    """

    def __init__(self, names):
        self._filters = [l.Filter(n) for n in names]

    def filter(self, record):
        """Apply all whitelist filters"""
        if record.levelno > l.DEBUG:
            return True
        else:
            return any(f.filter(record) for f in self._filters)


class BlacklistFilter(l.Filter):
    """A filter that blacklists DEBUG messages of certain loggers

    Attributes:
        _filter(list(~logging.Filter)): A list of filters generated from ``names``

    Args:
        names (list(str)): A list of names to be blacklisted
    """

    def __init__(self, names):
        self._filters = [l.Filter(n) for n in names]

    def filter(self, record):
        """Apply all blacklist filters"""
        if record.levelno > l.DEBUG:
            return True
        else:
            return not any(f.filter(record) for f in self._filters)


class RegexFilter(l.Filter):
    """A filter that filters DEBUG messages according to a regular expression

    Attributes:
        _patter: compiled regex

    Args:
        regex (str): The regex to be applied for this filter
    """

    def __init__(self, regex):
        self._pattern = re.compile(regex)

    def filter(self, record):
        """Apply the regex filter"""
        if record.levelno > l.DEBUG:
            return True
        else:
            return bool(self._pattern.search(record.msg))


def setup(level, whitelist=None, blacklist=None, message_filer=None,
          use_color=True):
    """Setup the default logger

    Configures the default logger to print messages in the format
    ``"[LOGLEVEL] message"`` where the loglevel is printed in color. Optionally
    filters can be applied to to debug messages in order to only focus
    on specific modules or on messages macthing a regex.

    Args:
        level: the global log level
        whitelist (WhitelistFilter): An optional whitelist filter
        blacklist (BlacklistFilter): An optional blacklist filter
        Regexlist (RegexFilter): An optional regex filter
        use_color (bool): Produce uncolored output if set to ``False``
    """
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
    """Add logging related cli arguments to the argument parser

    Adds a set of cli arguments to the given :class:`~argparse.ArgumentParser`.
    This works well in combination with :func:`setup_from_args`.

    **Added Cli Arguments:**
      * ``-v`` or ``--verbose``: increase output verbosity (e.g., ``-vv`` is more than ``-v``)
      * ``-s`` or ``--silent``: suppress all output except errors
      * ``-w`` or ``--log-whitelist``: add a log whitelist filter (e.g. pykpn.common)
      * ``-b`` or ``--log-blacklist``: add a log blacklist filter (e.g. pykpn.common) 
      * ``-r`` or ``--log-regex``: Add a regex filter that matches the message
      * ``--no-color``: disable colored output

    Args:
        parser(~argparse.ArgumentParser): The parser to be extended by logging
            arguments
    """

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
    """Setup the default logger as configured by the cli arguments.

    This only works in combination with :func:`add_cli_args`! 

    Args:
        args: arguments as returned by :meth:`~argparse.ArgumentParser.parse_args`
    """

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
    """Return a new logger with the given name"""
    return l.getLogger(name)

# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


"""Utility module for improved logging functionality

This module extends the functionality provided by the :mod:`logging` package.
It provides a custom formatter (:class:`MocasinFormatter`) that produces colored
output. By default, the hydra configuration uses the custom formatter from this
module.
"""

import logging as l
import copy
from termcolor import colored


COLORS = {"INFO": "green", "WARNING": "yellow", "ERROR": "red", "DEBUG": "blue"}
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


class MocasinFormatter(l.Formatter):
    """A custom mocasin logging formatter

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

        See :class:`MocasinFormatter` for details.
        """
        # make sure not to modify the original record object
        record = copy.deepcopy(record)
        # add brackets
        levelname = "[%s]" % record.levelname
        # fill with spaces
        levelname = "%-9s" % levelname
        # colorize
        if self._use_color:
            if record.levelname in COLORS:
                color = COLORS[record.levelname]
            else:
                color = "red"
            levelname = colored(levelname, color, attrs=["bold"])
            record.name = colored(record.name, "cyan")
        record.levelname = levelname

        global _indent_level
        if _indent_level > 0:
            indent_string = "%s* " % (" " * _indent_level * 2)
            record.msg = indent_string + record.msg

        # ensure that multiline messages are properly indented
        record.msg = record.msg.replace(
            "\n", "\n%s" % (" " * (10 + _indent_level * 2))
        )

        return super().format(record)


def getLogger(name):
    """Return a new logger with the given name"""
    return l.getLogger(name)

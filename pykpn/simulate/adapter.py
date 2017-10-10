# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

from termcolor import colored


class SimulateLoggerAdapter(logging.LoggerAdapter):

    def __init__(self, logger, instance, env):
        super().__init__(logger, {})
        self._instance = instance
        self._env = env

    def process(self, msg, kwargs):
        instance = colored(self._instance, 'green')
        msg = '@%14d %s: %s' % (self._env.now, instance, msg)
        return msg, kwargs

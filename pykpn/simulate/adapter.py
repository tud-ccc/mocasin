# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging


class SimulateLoggerAdapter(logging.LoggerAdapter):

    def __init__(self, logger, instance, env):
        super().__init__(logger, {})
        self._instance = instance
        self._env = env

    def process(self, msg, kwargs):
        msg = '%s: @%d\n  %s' % (self._instance, self._env.now, msg)
        return msg, kwargs

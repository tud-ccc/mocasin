# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

import sys
import pandas as pd
import math
from enum import Enum

from pykpn.tetris.apptable import AppTable
from pykpn.tetris.context import Context

import logging
log = logging.getLogger(__name__)


class JobRequestStatus(Enum):
    ARRIVED = 1
    ACCEPTED = 2
    FINISHED = 3
    REFUSED = 4


class JobRequestInfo:
    def __init__(self, kpn, arrival, deadline=math.inf,
                 status=JobRequestStatus.ARRIVED, start_cratio=0.0):
        self.__app = kpn
        self.__arrival = arrival
        self.__deadline = deadline  # Absolute time
        self.__status = status
        self.__start_cratio = start_cratio
        self.__finish = None

    def app(self):
        return self.__app

    def arrival(self):
        return self.__arrival

    def deadline(self):
        return self.__deadline

    def start_cratio(self):
        return self.__start_cratio

    @property
    def status(self):
        """Returns a request status."""
        return self.__status

    @status.setter
    def status(self, status):
        """Set a new request status. This setter ensures that the new status is
        a valid transition of the old status.
        """
        if self.status == status:
            log.warning("Attempt to set the same request status")
        if self.status == JobRequestStatus.ARRIVED:
            assert status != JobRequestStatus.FINISHED
        if self.status == JobRequestStatus.ACCEPTED:
            assert status != JobRequestStatus.NEW
            assert status != JobRequestStatus.REFUSED
        if self.status == JobRequestStatus.REFUSED:
            assert status == JobRequestStatus.REFUSED
        if self.status == JobRequestStatus.FINISHED:
            assert status == JobRequestStatus.FINISHED
        self.__status = status

    @property
    def finish_time(self):
        return self.__finish

    @finish_time.setter
    def finish_time(self, finish):
        assert self.__finish is None
        self.__finish = finish

    def to_str(self):
        res = ("Job request (app: {}, arrival [cratio]: {} [{}], " +
               "deadline: {}, status: {}, finished: {})").format(
                   self.__app.name, self.__arrival, self.__start_cratio,
                   self.__deadline, self.__status, self.__finished)

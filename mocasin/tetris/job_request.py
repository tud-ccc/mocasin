# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from mocasin.common.kpn import KpnGraph

from enum import Enum
import logging
import math

log = logging.getLogger(__name__)


class JobRequestStatus(Enum):
    ARRIVED = 1
    ACCEPTED = 2
    FINISHED = 3
    REFUSED = 4


class JobRequestInfo:
    def __init__(
        self,
        app,
        mappings,
        arrival,
        deadline=math.inf,
        status=JobRequestStatus.ARRIVED,
        start_cratio=0.0,
    ):
        assert isinstance(app, KpnGraph)
        assert isinstance(mappings, list)
        assert isinstance(arrival, float)
        assert isinstance(deadline, float)
        assert isinstance(status, JobRequestStatus)
        assert isinstance(start_cratio, float)
        self.__app = app
        self.__mappings = mappings
        self.__arrival = arrival
        self.__deadline = deadline  # Absolute time
        self.__status = status
        self.__start_cratio = start_cratio
        self.__finish = None

        # Memoize functions
        self.__memo_min_exec_time = None
        self.__memo_min_energy = None

    @property
    def app(self):
        return self.__app

    @property
    def mappings(self):
        return self.__mappings

    @property
    def arrival(self):
        return self.__arrival

    @property
    def deadline(self):
        return self.__deadline

    @property
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
        res = (
            "(Job request app={} arrival[cratio]={}[{}] "
            + "deadline={} status={} finished={})"
        ).format(
            self.__app.name,
            self.__arrival,
            self.__start_cratio,
            self.__deadline,
            self.__status,
            self.__finish,
        )
        return res

    def get_min_exec_time(self):
        """Returns the minimum execution time over all mappings."""
        if self.__memo_min_exec_time is not None:
            return self.__memo_min_exec_time

        self.__memo_min_exec_time = min(
            [m.metadata.exec_time for m in self.__mappings]
        )
        return self.__memo_min_exec_time

    def get_min_energy(self):
        """Returns the minimum energy consumption over all mappings."""
        if self.__memo_min_energy is not None:
            return self.__memo_min_energy

        self.__memo_min_energy = min(
            [m.metadata.energy for m in self.__mappings]
        )
        return self.__memo_min_energy

# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from enum import Enum
import logging
import math

log = logging.getLogger(__name__)


class JobRequestStatus(Enum):
    # New request, not known by the resource manager
    NEW = 0
    # Arrived request to the resource manager
    ARRIVED = 1
    # Request is accepted by the resource manager
    ACCEPTED = 2
    # Successfully finished request
    FINISHED = 3
    # Refused request
    REFUSED = 4


class JobRequestInfo:
    # FIXME: Rewrite this class as dataclass
    def __init__(
        self,
        graph,
        mappings,
        arrival=None,
        deadline=None,
        status=JobRequestStatus.NEW,
        start_cratio=0.0,
    ):
        assert isinstance(status, JobRequestStatus)
        self.app = graph
        self.mappings = mappings
        self.arrival = arrival
        self.deadline = deadline  # Absolute time
        if not deadline:
            self.deadline = math.inf
        self._status = status
        self.start_cratio = start_cratio
        self.finish_time = None

        # Memoize functions
        self._memo_min_exec_time = None
        self._memo_min_energy = None

    @property
    def status(self):
        """Returns a request status."""
        return self._status

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
        self._status = status

    def to_str(self):
        res = (
            "(Job request app={} arrival[cratio]={}[{}] "
            + "deadline={} status={} finished={})"
        ).format(
            self.app.name,
            self.arrival,
            self.start_cratio,
            self.deadline,
            self.status,
            self.finish_time,
        )
        return res

    def get_min_exec_time(self):
        """Returns the minimum execution time over all mappings."""
        if self._memo_min_exec_time is not None:
            return self._memo_min_exec_time

        self._memo_min_exec_time = min(
            [m.metadata.exec_time for m in self.mappings]
        )
        return self._memo_min_exec_time

    def get_min_energy(self):
        """Returns the minimum energy consumption over all mappings."""
        if self._memo_min_energy is not None:
            return self._memo_min_energy

        self._memo_min_energy = min([m.metadata.energy for m in self.mappings])
        return self._memo_min_energy

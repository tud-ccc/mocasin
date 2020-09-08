# Author: Robert Khasanov

from pykpn.common.mapping import Mapping
from enum import Enum

import logging
log = logging.getLogger(__name__)

class JobStateEnum(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    PAUSED = 2
    CANCELLED = 3
    FINISHED = 4

class JobStateInfo:
    """Job state info

    Job state info is defined by a JobRequestInfo object, a mapping, a state and
    a completion ratio. The objects of this class are supplied to scheduler.

    Args:
        request_info (JobRequestInfo): A reference to job request info
        mapping (Mapping): Current mapping
        state (JobStateEnum): Current state
        cratio (float): Completion ratio
    """
    def __init__(self, request_info, mapping=None,
                 state=JobStateEnum.NOT_STARTED, cratio=0.0):
        assert isinstance(request_info, JobRequestInfo)
        assert isinstance(mapping, Mapping)
        assert isinstance(cratio, float)
        self.request = request_info
        self.mapping = mapping
        self.state = state
        # TODO: make a property
        # self.rid = rid
        self.__cratio = cratio

    @property
    def deadline(self):
        return self.request.deadline

    @property
    def cratio(self):
        return self.__cratio

    @cratio.setter
    def cratio(self, val):
        if val < self.cratio:
            log.warning("Job state is going to be degrade")
        self.__cratio = val

    @property
    def app(self):
        """Application."""
        return self.request.app()

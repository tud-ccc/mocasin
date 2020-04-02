from pykpn.tetris.tetris.context import Context
from pykpn.tetris.tetris.mapping import Mapping

import logging
log = logging.getLogger(__name__)

class Job:
    """Job state.

    Job state is defined by its request id and completion ratio. The instance of job is created for each request, and updated during the trace simulation. The instances may be copied by schedulers for internal simulation.

    Args:
        rid (int): Request id
        cratio (float): Completion ratio
    """
    def __init__(self, table, rid, cratio = 0.0):
        assert isinstance(cratio, float)
        self.__table = table
        # TODO: make a property
        self.rid = rid
        self.__cratio = cratio

    @property
    def deadline(self):
        return self.abs_deadline - self.__table.time

    @property
    def abs_deadline(self):
        return Context().req_table[self.rid].abs_deadline()

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
        return Context().req_table[self.rid].app()

class JobTable:
    """Table of jobs.

    Job table is created at the beginning of simulation. It keeps current statuses of jobs.
    Some schedulers may create their own version of job tables.

    Args:
        time (float): Current time
    """
    def __init__(self, time = 0.0):
        assert time >= 0.0
        self.__jobs = []
        self.time = time

    def init_by_req_table(self):
        assert len(self.__jobs) == 0, "There should be no task in the state table"
        for r in Context().req_table:
            self.add(r.rid(), r.start_completion_rate())

    @classmethod
    def from_mapping(cls, mapping):
        """Create an instance by mapping."""
        assert isinstance(mapping, Mapping)
        if len(mapping) == 0:
            return cls()

        new_obj = cls(time = mapping.end_time)
        for sm in mapping.last:
            finished = sm.finished
            rid = sm.rid
            fcr = sm.end_cratio
            if not finished:
                new_obj.add(rid, fcr)
        return new_obj

    def copy(self):
        """Copy the job table."""
        new_jt = JobTable(time = self.time)
        for j in self:
            new_jt.add(j.rid, j.cratio)
        return new_jt


    def add(self, rid, cratio = 0.0):
        """Add a job into the job table."""
        self.__jobs.append(Job(self, rid, cratio))

    def find_by_rid(self, rid):
        assert isinstance(rid, int)
        for t in self:
            if t.rid == rid:
                return t
        assert False
        return None

    def remove(self, rid):
        """Remove job by its rid."""
        for idx, j in enumerate(self):
            if j.rid == rid:
                del self.__jobs[idx]
                return
        assert False

    def __getitem__(self, idx):
        return self.__jobs[idx]

    def __len__(self):
        return len(self.__jobs)

    def __iter__(self):
        yield from self.__jobs


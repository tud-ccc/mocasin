import sys
import pandas as pd
import math
from enum import Enum

from pykpn.tetris.context import Context

import logging
log = logging.getLogger(__name__)

class RequestStatus(Enum):
    NEW = 1
    ACCEPTED = 2
    FINISHED = 3
    REFUSED = 4

class Request:
    def __init__(self, rid, app, arrival, deadline, start_completion_rate = 0.0, status = RequestStatus.NEW):
        self.__rid = rid
        self.__app = app
        self.__arrival = arrival
        self.__status = status
        if deadline < 0:
            self.__deadline = math.inf
        else:
            self.__deadline = deadline  # Relative to arrival time
        self.__start_completion_rate = start_completion_rate

    def rid(self):
        return self.__rid

    def app_name(self):
        return self.__app

    def app(self):
        return Context().app_table[self.app_name()]

    def arrival_time(self):
        return self.__arrival

    def deadline(self):
        return self.__deadline

    def start_completion_rate(self):
        return self.__start_completion_rate

    def abs_deadline(self):
        return self.__deadline + self.__arrival

    @property
    def status(self):
        """Returns a request status."""
        return self.__status

    @status.setter
    def status(self, status):
        """Set a new request status. This setter ensures that the new status is a valid transition of the old status"""
        if self.status == status:
            log.warning("Attempt to set the same request status")
        if self.status == RequestStatus.NEW:
            assert status != RequestStatus.FINISHED
        if self.status == RequestStatus.ACCEPTED:
            assert status != RequestStatus.NEW
            assert status != RequestStatus.REFUSED
        if self.status == RequestStatus.REFUSED:
            assert status == RequestStatus.REFUSED
        if self.status == RequestStatus.FINISHED:
            assert status == RequestStatus.Finished
        self.__status = status

    def dump(self, outf = sys.stdout, prefix = "", end='\n'):
        print(self.dump_str(prefix=prefix), file=outf, end=end)

    def dump_str(self, prefix = ""):
        res = prefix + "Request {} [{}], arrival = {}, deadline (abs) = {} ({})".format(
            self.rid(), self.app_name(), self.arrival_time(), self.deadline(), self.abs_deadline())
        return res

class ReqTable:
    def __init__(self):
        self.__reqs = []
        self.__next_rid = 0

    def add(self, app_name, arrival, deadline, completion_rate = 0.0, status = RequestStatus.NEW):
        rid = self.__next_rid
        r = Request(rid, app_name, arrival, deadline, completion_rate, status)
        self.__next_rid += 1
        self.__reqs.append(r)
        return rid

    def read_from_file(self, scenario):
        sdf = pd.read_csv(scenario, comment='#')

        assert sdf.start_time.unique() == [0]
        reqs = sdf.to_dict('records')

        for r in reqs:
            if 'start_completion_rate' in r:
                sc = r['start_completion_rate']
            else:
                sc = 0.0
            self.add(r['app'], r['start_time'], r['deadline'], sc)

    def to_list(self):
        return self.__reqs.copy()

    def __getitem__(self, key):
        for r in self.__reqs:
            if r.rid() == key:
                return r
        assert False, "No request with id '{}'. ReqTable: {}".format(key, self.dump_str())

    def __iter__(self):
        yield from self.__reqs

    def __len__(self):
        return len(self.__reqs)

    def count_accepted_and_finished(self):
        """Returns the number of accepted requests."""
        res = 0
        for r in self:
            if r.status == RequestStatus.ACCEPTED or r.status == RequestStatus.FINISHED:
                res += 1
        return res

    def dump(self, outf = sys.stdout, prefix = ""):
        print(self.dump_str(prefix=prefix, file=outf))

    def dump_str(self, prefix = ""):
        res = prefix + "Request table:\n"
        for r in self.__reqs:
            res += r.dump_str(prefix = prefix + "  ") + "\n"
        return res

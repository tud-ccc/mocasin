from unittest.mock import Mock
import pytest

from pykpn.common.kpn import KpnProcess,KpnGraph
from pykpn.common.platform import Platform,Processor,Scheduler

@pytest.fixture
def num_procs():
    return 7

@pytest.fixture
def kpn():
    k = KpnGraph('a')
    k.add_process(KpnProcess('a'))
    k.add_process(KpnProcess('b'))
    return k


@pytest.fixture
def platform(num_procs):
    p = Platform('platform')
    procs = []
    for i in range(num_procs):
        proc = Processor(('processor' + str(i)), 'proctype', Mock())
        procs.append(proc)
        p.add_processor(proc)
    policies = [Mock()]
    sched = Scheduler('name', procs, policies)
    p.add_scheduler(sched)
    return p



# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


def test_init(frequency_domain):
    assert frequency_domain.name == "fd"
    assert frequency_domain.frequency == 1500000000


def test_cycles_to_ticks(frequency_domain):
    # one cycle should be 667 ps at 1.5GHz
    assert frequency_domain.cycles_to_ticks(1) == 667
    # 15 cycles are 10 ns at 1.5GHz
    assert frequency_domain.cycles_to_ticks(15) == 10000
    # and 15,000,000,000 cycles are 10 s at 1.5 GHz
    assert frequency_domain.cycles_to_ticks(15000000000) == 10000000000000

    # switch to 20 Hz
    frequency_domain.frequency = 20
    # one cycle should be 50 ms at 20Hz
    assert frequency_domain.cycles_to_ticks(1) == 50000000000

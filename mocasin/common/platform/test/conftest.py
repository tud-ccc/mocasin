# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import pytest


from mocasin.common.platform import FrequencyDomain


@pytest.fixture
def frequency_domain():
    return FrequencyDomain(name="fd", frequency=1500000000)

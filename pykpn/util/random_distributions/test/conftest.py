import numpy as np
import pytest
from scipy.linalg import sqrtm


@pytest.fixture
def ns():
    return [50,80]

@pytest.fixture
def mu():
    return [15,35]

@pytest.fixture
def Q():
    return np.array(sqrtm(np.array([[ 3., 0.], [0., 1/3.]])))
    #Q = np.array(sqrtm(np.ndarray([[ 2., 0.], [0., 1/2.]])))
    #Q = np.array(sqrtm(np.ndarray([[ 1.66666667,  1.33333333], [ 1.33333333,  1.66666667]]))) # same as above, rotated 45^\circ

@pytest.fixture
def r():
    return 3

@pytest.fixture
def eigenv(r,Q):
    eigenv,_ = np.linalg.eig(r**2 * Q @ np.transpose(Q))
    return eigenv




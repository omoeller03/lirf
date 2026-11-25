import numpy as np

from fluorescence.ion import Ion
from fluorescence.angular_distribution import AngularDistribution


def test_beta_zero_is_isotropic():
    distribution = AngularDistribution(Ion(beta=0.0))
    values = distribution.probability_per_solid_angle(
        np.array([0.0, 0.5, 1.0, 2.0])
    )
    assert np.allclose(values, 1.0 / (4.0 * np.pi))

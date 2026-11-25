import numpy as np

from fluorescence.ion import Ion
from fluorescence.relativistic import RelativisticKinematics


def test_beta_zero_energy_is_unchanged():
    kin = RelativisticKinematics(Ion(beta=0.0))
    assert np.isclose(kin.photon_energy_lab(1234.0, 0.7), 1234.0)


def test_forward_and_backward_energy():
    beta = 0.6
    energy = 1000.0
    ion = Ion(beta=beta)
    kin = RelativisticKinematics(ion)

    assert np.isclose(
        kin.photon_energy_lab(energy, 0.0),
        ion.gamma * energy * (1.0 + beta),
    )
    assert np.isclose(
        kin.photon_energy_lab(energy, np.pi),
        ion.gamma * energy * (1.0 - beta),
    )


def test_angle_transform_forward_direction():
    kin = RelativisticKinematics(Ion(beta=0.9))
    assert np.isclose(kin.angle_lab(0.0), 0.0)

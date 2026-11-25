import numpy as np

from .ion import Ion
from .transition import Transition
from .relativistic import RelativisticKinematics


class FluorescenceSpectrum:
    """Energy-angle relation for a single ion velocity and transition."""

    def __init__(self, ion: Ion, transition: Transition) -> None:
        self.ion = ion
        self.transition = transition
        self.kinematics = RelativisticKinematics(ion)

    @property
    def forward_energy_eV(self) -> float:
        return float(self.kinematics.photon_energy_lab(
            self.transition.energy_eV, 0.0
        ))

    @property
    def backward_energy_eV(self) -> float:
        return float(self.kinematics.photon_energy_lab(
            self.transition.energy_eV, np.pi
        ))

    def energy_vs_rest_angle(self, theta_rest_rad):
        return self.kinematics.photon_energy_lab(
            self.transition.energy_eV, theta_rest_rad
        )

    def energy_vs_lab_angle(self, theta_lab_rad):
        return self.kinematics.photon_energy_lab_from_lab_angle(
            self.transition.energy_eV, theta_lab_rad
        )

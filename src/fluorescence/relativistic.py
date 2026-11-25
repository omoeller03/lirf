import numpy as np

from .ion import Ion


class RelativisticKinematics:
    """Lorentz transformations for photons emitted by a moving ion.

    Angles are measured relative to the ion velocity direction.
    """

    def __init__(self, ion: Ion) -> None:
        self.ion = ion

    def photon_energy_lab(self, energy_rest_eV, theta_rest_rad):
        """Photon energy in the lab for a rest-frame emission angle.

        E_lab = gamma * E_rest * (1 + beta*cos(theta_rest)).
        Accepts scalars or NumPy arrays.
        """
        theta = np.asarray(theta_rest_rad)
        return (
            self.ion.gamma
            * energy_rest_eV
            * (1.0 + self.ion.beta * np.cos(theta))
        )

    def angle_lab(self, theta_rest_rad):
        """Transform rest-frame photon angle to laboratory angle."""
        theta = np.asarray(theta_rest_rad)
        mu_rest = np.cos(theta)
        mu_lab = (mu_rest + self.ion.beta) / (
            1.0 + self.ion.beta * mu_rest
        )
        mu_lab = np.clip(mu_lab, -1.0, 1.0)
        return np.arccos(mu_lab)

    def angle_rest(self, theta_lab_rad):
        """Inverse transformation: lab angle to rest-frame angle."""
        theta = np.asarray(theta_lab_rad)
        mu_lab = np.cos(theta)
        mu_rest = (mu_lab - self.ion.beta) / (
            1.0 - self.ion.beta * mu_lab
        )
        mu_rest = np.clip(mu_rest, -1.0, 1.0)
        return np.arccos(mu_rest)

    def photon_energy_lab_from_lab_angle(self, energy_rest_eV, theta_lab_rad):
        """Photon energy as a function of laboratory emission angle."""
        theta = np.asarray(theta_lab_rad)
        return energy_rest_eV / (
            self.ion.gamma * (1.0 - self.ion.beta * np.cos(theta))
        )

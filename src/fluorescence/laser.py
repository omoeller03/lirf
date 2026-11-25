
from dataclasses import dataclass

import numpy as np


@dataclass
class Laser:
    """
    Laser beam in the laboratory frame.

    Parameters
    ----------
    photon_energy_eV:
        Laser photon energy in eV.
    angle_rad:
        Angle between laser propagation and ion velocity.
        0      = co-propagating
        pi     = counter-propagating
    """

    photon_energy_eV: float
    angle_rad: float = np.pi
    energy_sigma_eV: float = 0.0


    def __post_init__(self):
        if self.photon_energy_eV <= 0:
            raise ValueError("Laser photon energy must be positive.")

        if not 0 <= self.angle_rad <= np.pi:
            raise ValueError("Laser angle must be between 0 and pi.")

    def energy_in_ion_rest_frame(self, beta):
        """Calculate the Doppler-shifted laser photon energy."""

        beta = np.asarray(beta)

        if np.any(np.abs(beta) >= 1):
            raise ValueError("Beta must satisfy |beta| < 1.")

        gamma = 1.0 / np.sqrt(1.0 - beta**2)

        return (
            gamma
            * self.photon_energy_eV
            * (1.0 - beta * np.cos(self.angle_rad))
        )

    def resonant_lab_energy(self, beta, transition_energy_eV):
        """Calculate the laser photon energy required for resonance."""

        beta = np.asarray(beta)

        if np.any(np.abs(beta) >= 1):
            raise ValueError("Beta must satisfy |beta| < 1.")

        gamma = 1.0 / np.sqrt(1.0 - beta**2)

        return transition_energy_eV / (
            gamma * (1.0 - beta * np.cos(self.angle_rad))
        )


@dataclass
class Resonance:
    """
    Simple Lorentzian resonance model.

    linewidth_eV is the full width at half maximum (FWHM).
    """

    transition_energy_eV: float
    linewidth_eV: float

    def __post_init__(self):
        if self.transition_energy_eV <= 0:
            raise ValueError("Transition energy must be positive.")

        if self.linewidth_eV <= 0:
            raise ValueError("Linewidth must be positive.")

    def detuning(self, laser: Laser, beta):
        """Energy difference between laser and transition in the ion frame."""

        laser_energy = laser.energy_in_ion_rest_frame(beta)

        return laser_energy - self.transition_energy_eV

    def excitation_weight(self, laser: Laser, beta):
        """
        Relative excitation strength between 0 and 1.

        This is not yet the absolute excitation probability.
        """

        delta_e = self.detuning(laser, beta)
        half_width = self.linewidth_eV / 2.0

        return half_width**2 / (
            delta_e**2 + half_width**2
        )





    def excitation_weight_broadened(
            self,
            laser: Laser,
            beta: np.ndarray | float,
            ) -> np.ndarray:
        beta = np.asarray(beta, dtype=float)

    
        if np.any(np.abs(beta) >= 1.0):
            raise ValueError("beta must be between -1 and 1.")

        if not np.isclose(laser.angle_rad, np.pi):
            raise NotImplementedError(
                "Only counter-propagating lasers are supported."
            )

        sigma_transition = self.linewidth_eV / (
            2.0 * np.sqrt(2.0 * np.log(2.0))
        )

        doppler = np.sqrt((1.0 + beta) / (1.0 - beta))

        sigma_effective = np.sqrt(
            sigma_transition**2
            + (doppler * laser.energy_sigma_eV)**2
        )

        detuning = (
            doppler * laser.photon_energy_eV
            - self.transition_energy_eV
        )

        return (
            sigma_transition / sigma_effective
            * np.exp(
                -0.5 * (detuning / sigma_effective)**2
            )
        )

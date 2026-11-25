import numpy as np

from .ion import Ion


class AngularDistribution:
    """Relativistic angular distribution for isotropic rest-frame emission."""

    def __init__(self, ion: Ion) -> None:
        self.ion = ion

    def probability_per_solid_angle(self, theta_lab_rad):
        """Return dP/dOmega in sr^-1 in the laboratory frame.

        For isotropic emission in the ion rest frame:
        dP/dOmega = 1 / [4*pi*gamma^2*(1-beta*cos(theta))^2].
        """
        theta = np.asarray(theta_lab_rad)
        denominator = (
            4.0
            * np.pi
            * self.ion.gamma**2
            * (1.0 - self.ion.beta * np.cos(theta)) ** 2
        )
        return 1.0 / denominator

    def relative_intensity(self, theta_lab_rad):
        """Distribution normalized to its value at theta=0."""
        values = self.probability_per_solid_angle(theta_lab_rad)
        forward = self.probability_per_solid_angle(0.0)
        return values / forward

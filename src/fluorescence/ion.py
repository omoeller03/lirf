from dataclasses import dataclass


@dataclass(frozen=True)
class Ion:
    """Kinematic properties of an ion beam.

    The first version only needs beta. Element, mass and charge state can be
    added later when recoil and transition databases are implemented.
    """

    beta: float
    label: str = "ion"

    def __post_init__(self) -> None:
        if not 0.0 <= self.beta < 1.0:
            raise ValueError("beta must satisfy 0 <= beta < 1")

    @property
    def gamma(self) -> float:
        """Lorentz factor."""
        return 1.0 / (1.0 - self.beta**2) ** 0.5

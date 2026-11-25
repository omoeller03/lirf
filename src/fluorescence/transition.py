from dataclasses import dataclass


@dataclass(frozen=True)
class Transition:
    """Atomic transition energy in the ion rest frame, in eV."""

    energy_eV: float
    label: str = "transition"

    def __post_init__(self) -> None:
        if self.energy_eV <= 0.0:
            raise ValueError("transition energy must be positive")

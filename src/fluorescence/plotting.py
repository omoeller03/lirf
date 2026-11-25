from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .angular_distribution import AngularDistribution
from .spectrum import FluorescenceSpectrum


def plot_energy_vs_angle(spectrum: FluorescenceSpectrum, output: Path | None = None):
    theta = np.linspace(0.0, np.pi, 1000)
    energy = spectrum.energy_vs_lab_angle(theta)

    fig, ax = plt.subplots()
    ax.plot(np.degrees(theta), energy)
    ax.set_xlabel(r"Laboratory emission angle $\theta$ (deg)")
    ax.set_ylabel("Photon energy (eV)")
    ax.set_title("Fluorescence photon energy vs. laboratory angle")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if output:
        fig.savefig(output, dpi=160)
    return fig, ax


def plot_angular_distribution(
    distribution: AngularDistribution,
    output: Path | None = None,
):
    theta = np.linspace(0.0, np.pi, 1000)
    intensity = distribution.probability_per_solid_angle(theta)

    fig, ax = plt.subplots()
    ax.plot(np.degrees(theta), intensity)
    ax.set_xlabel(r"Laboratory emission angle $\theta$ (deg)")
    ax.set_ylabel(r"$dP/d\Omega$ (sr$^{-1}$)")
    ax.set_title("Relativistic fluorescence angular distribution")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if output:
        fig.savefig(output, dpi=160)
    return fig, ax

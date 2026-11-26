from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .angular_distribution import AngularDistribution
from .spectrum import FluorescenceSpectrum
from .laser import Laser, Resonance


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

def plot_angular_distribution_2d(distribution: AngularDistribution, output: Path | None = None):
    """
    Plot relativistic angular distribution as a polar COLZ plot

    radial coordinate: polar emission angle theta (0 ... 180 deg)
    azimuthal coordinate: azimuth angle phi (0 ... 360 deg)
    color: probability per solid angle dP/dOmega
    """
    n_theta = 20000
    n_phi = 36 # no phi dependence...

    # bin edges
    theta_edges = np.linspace(0., np.pi/1., n_theta+1)
    phi_edges = np.linspace(0.,2.*np.pi, n_phi+1)

    # bin centers
    theta_centers = 0.5 * (theta_edges[:-1] + theta_edges[1:])

    # angular distribution
    intensity = distribution.probability_per_solid_angle(theta_centers)
    values = np.repeat(intensity[:, np.newaxis], n_phi, axis=1)

    # polar mesh
    phi_grid, theta_grid = np.meshgrid(phi_edges, theta_edges)
    fig, ax = plt.subplots(figsize=(8,7), subplot_kw={"projection": "polar"})
    mesh = ax.pcolormesh(phi_grid, theta_grid, values, shading="flat", cmap="viridis")

    # polar axis configuration
    ax.set_ylim(np.radians(0.08), np.pi/1.) #0., np.pi)
    ax.set_yscale("log")
    ticks_deg = [0.1, 1., 10.,100.]
    ax.set_yticks(np.radians(ticks_deg))
    ax.set_yticklabels(f"{angle}°" for angle in ticks_deg)

    ax.set_rlabel_position(60)
    ax.tick_params(axis="y", pad=8)
    #ax.set_yticks(np.radians([30, 60, 90, 120, 150, 180]))
    #ax.set_yticklabels(["30°", "60°", "90°", "120°", "150°", "180°"])

    # forward direction at the top
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)


    ax.set_title("Relativistic fluorescence angular distribution", pad=25)

    cbar = fig.colorbar(mesh, ax=ax, pad=0.12)
    cbar.set_label(r"$dP/d\Omega$ (sr$^{-1}$)")

    fig.tight_layout()

    if output:
        fig.savefig(output,dpi=160)

    return fig, ax





def plot_excitation_vs_beta(laser: Laser, resonance: Resonance, beta_center: float, output: Path | None = None):
    """
    plot relative excitation strength as a function of ion velocity beta.

    plot range: automatically chosen around resonance
    """

    # determine local slope of detuning
    step = min(1e-7, beta_center * 0.1, (1.0 - beta_center) * 1.)

    #beta_values = np.array([beta_center - step, beta_center + step])

    #detuning_values = resonance.detuning(laser, beta_values)
    #derivative = ( detuning_values[1] - detuning_values[0]) / (2.0 * step)
    #if derivative == 0:
    #    raise ValueError("Cannot determine resonance position.")

    # estimate resonance position using a linear approx
    detuning_center = resonance.detuning(laser, beta_center)

    if not np.isclose(laser.angle_rad, np.pi):
        raise NotImplementedError("Exact resonance calculation currently supports couter-propagation lasers only.")

    ratio = resonance.transition_energy_eV / laser.photon_energy_eV
    beta_resonance = (ratio**2 - 1.) / (ratio**2 + 1.)

    #beta_resonance = beta_center - detuning_center / derivative

    if not 0. < beta_resonance < 1.:
        #raise ValueError("Resonance lies outside the physical beta range.")
        print("Resonance lies outside the physical beta range.")
        return

    step = 1e-8
    derivative = (resonance.detuning(laser, beta_resonance + step) - resonance.detuning(laser,beta_resonance - step) ) / (2.0 * step)

    beta_width = resonance.linewidth_eV / abs(derivative)

    # convert energy linewidth into an approx beta linewidth
    #beta_width = resonance.linewidth_eV / abs(derivative)

    # show five linewidths on either side of resonance
    beta_min = beta_resonance - 5. * beta_width
    beta_max = beta_resonance + 5. * beta_width

    beta = np.linspace(beta_min, beta_max, 2000)
    #excitation = resonance.excitation_weight(laser, beta)
    excitation = resonance.excitation_weight_broadened(laser, beta)

    delta_beta = (beta - beta_resonance) / 1e-6

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(delta_beta, excitation, label="Excitation strength")

    ax.axvline(0.0, color="red", linestyle="--", label=rf"Resonance: $\beta_\mathrm{{res}}={beta_resonance:.9f}$")
    ax.set_xlabel(r"Velocity deviation $\Delta\beta = \beta-\beta_\mathrm{res}$ ($10^{-6}$)")
    ax.set_ylabel("Relative excitation strength")
    ax.set_title("Laser excitation vs. ion velocity")
    ax.set_xlim(delta_beta.min(), delta_beta.max())
    ax.set_ylim(0., 1.05)
    ax.legend()

    fig.tight_layout()

    if output is not None:
        fig.savefig(output, dpi=160)

    return fig, ax


def plot_beam_excitation(
    laser: Laser,
    resonance: Resonance,
    beta_center: float,
    beta_sigma: float,
    output: Path | None = None,
):
    """
    Plot the ion beam velocity distribution and its excitation.

    The beam has a Gaussian beta distribution.
    The excitation profile is weighted by the beam distribution.
    """

    if beta_sigma <= 0.0:
        raise ValueError("beta_sigma must be positive.")

    # Beta range: +/- 5 standard deviations
    beta_min = max(0.0, beta_center - 5.0 * beta_sigma)
    beta_max = min(1.0, beta_center + 5.0 * beta_sigma)

    beta = np.linspace(beta_min, beta_max, 4000)

    # Gaussian beam velocity distribution
    beam = np.exp(
        -0.5 * ((beta - beta_center) / beta_sigma)**2
    ) / (np.sqrt(2.0 * np.pi) * beta_sigma)

    # Normalize in the physical beta interval
    beam /= np.trapezoid(beam, beta)

    # Excitation strength for each velocity
    #excitation = resonance.excitation_weight(laser, beta)
    excitation = resonance.excitation_weight_broadened(laser, beta)

    # Distribution of excited ions
    excited_beam = beam * excitation

    # Expected excited fraction
    expected_fraction = np.trapezoid(excited_beam, beta)

    # x-axis in units of beam standard deviation
    x = (beta - beta_center) / beta_sigma

    fig, ax1 = plt.subplots(figsize=(9, 5))

    # Beam distribution
    ax1.plot(
        x,
        beam,
        color="tab:blue",
        label="Ion beam distribution",
    )

    ax1.fill_between(
        x,
        excited_beam,
        color="tab:green",
        alpha=0.35,
        label="Excited ion distribution",
    )

    ax1.set_xlabel(
        r"Velocity deviation $(\beta-\beta_0)/\sigma_\beta$"
    )
    ax1.set_ylabel(r"Normalized beam density $f(\beta)$")
    ax1.set_xlim(-5.0, 5.0)
    ax1.grid(True, alpha=0.3)

    # Excitation profile on second y-axis
    ax2 = ax1.twinx()

    ax2.plot(
        x,
        excitation,
        color="tab:red",
        linestyle="--",
        label="Excitation strength",
    )

    ax2.set_ylabel("Relative excitation strength")
    ax2.set_ylim(0.0, 1.05)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper left",
    )

    ax1.set_title(
        "Laser excitation of the ion beam\n"
        + rf"Expected excited fraction: {expected_fraction:.4e}"
    )

    fig.tight_layout()

    if output is not None:
        fig.savefig(output, dpi=160)

    return fig, ax1, expected_fraction







def plot_excitation_vs_beta_broadened(
    laser: Laser,
    resonance: Resonance,
    output: Path | None = None,
):
    # Resonance beta for central laser energy
    ratio = resonance.transition_energy_eV / laser.photon_energy_eV
    beta_res = (ratio**2 - 1.0) / (ratio**2 + 1.0)

    if not 0.0 < beta_res < 1.0:
        raise ValueError("No physical resonance in beta range.")

    beta = np.linspace(
        max(0.0, beta_res - 10e-4),
        min(0.999999999, beta_res + 10e-4),
        3000,
    )

    excitation = resonance.excitation_weight_broadened(
        laser, beta
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(beta, excitation)

    ax.axvline(
        beta_res,
        color="red",
        linestyle="--",
        label=rf"Resonance $\beta={beta_res:.8f}$",
    )

    ax.set_xlabel(r"Ion velocity $\beta$")
    ax.set_ylabel("Relative excitation strength")
    ax.set_title("Excitation strength vs. ion velocity")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    if output is not None:
        fig.savefig(output, dpi=160)

    return fig, ax








def plot_excitation_vs_laser_energy(
    laser: Laser,
    resonance: Resonance,
    beta: float,
    output: Path | None = None,
):
    doppler = np.sqrt((1.0 + beta) / (1.0 - beta))

    energy_res = resonance.transition_energy_eV / doppler

    sigma_transition = resonance.linewidth_eV / (
        2.0 * np.sqrt(2.0 * np.log(2.0))
    )

    sigma_effective = np.sqrt(
        sigma_transition**2
        + (doppler * laser.energy_sigma_eV)**2
    )

    energy_width = sigma_effective / doppler

    energy = np.linspace(
        max(0.0, energy_res - 5.0 * energy_width),
        energy_res + 5.0 * energy_width,
        2000,
    )

    # Evaluate with varying central laser energy
    excitation = []

    for e in energy:
        test_laser = Laser(
            photon_energy_eV=e,
            angle_rad=laser.angle_rad,
            energy_sigma_eV=laser.energy_sigma_eV,
        )

        excitation.append(
            resonance.excitation_weight_broadened(
                test_laser, beta
            )
        )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(energy, excitation)

    ax.axvline(
        energy_res,
        color="red",
        linestyle="--",
        label=rf"Resonance: {energy_res:.6f} eV",
    )

    ax.set_xlabel("Central laser photon energy (eV)")
    ax.set_ylabel("Relative excitation strength")
    ax.set_title(
        rf"Laser excitation at $\beta={beta:.6f}$"
    )
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    if output is not None:
        fig.savefig(output, dpi=160)

    return fig, ax











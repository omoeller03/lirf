import numpy as np
import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from .ion import Ion
from .transition import Transition
from .spectrum import FluorescenceSpectrum
from .angular_distribution import AngularDistribution
from .laser import Laser, Resonance
from .plotting import (
        plot_energy_vs_angle,
        plot_angular_distribution,
        plot_angular_distribution_2d,
        plot_excitation_vs_beta,
        plot_beam_excitation,
        plot_excitation_vs_beta_broadened,
        plot_excitation_vs_laser_energy)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Relativistic fluorescence photon calculator"
    )
    parser.add_argument("--beta", type=float, required=True,
                        help="Ion velocity divided by c")
    parser.add_argument("--beta-sigma", type=float, default=1e-4,
                        help="Standard deviation of ion velocity distribution beta")
    parser.add_argument("--transition-energy", type=float, required=True,
                        help="Transition energy in the ion rest frame [eV]")
    parser.add_argument("--laser-energy", type=float, required=True,
                        help="Laser photon energy in the laboratory frame [eV]")
    parser.add_argument("--laser-energy-sigma", type=float, default=0.0,
                        help="Standard deviation of laser photon energy [eV]")
    parser.add_argument("--linewidth", type=float, default=0.1,
                        help="Transition linewidth (FWHM) in the ion rest frame [eV]")
    parser.add_argument("--label", default="ion",
                        help="Optional ion label for plot titles/output")
    parser.add_argument("--output-dir", type=Path, default=Path("results"),
                        help="Directory for plot files")
    parser.add_argument("--no-show", action="store_true",
                        help="Save plots without opening plot windows")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    ion = Ion(beta=args.beta, label=args.label)
    transition = Transition(energy_eV=args.transition_energy)
    spectrum = FluorescenceSpectrum(ion, transition)
    angular = AngularDistribution(ion)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    energy_path = args.output_dir / "energy_vs_lab_angle.png"
    angular_path = args.output_dir / "angular_distribution.png"
    angular_2d_path = args.output_dir / "angular_distribution_2d.png"
    excitation_path = args.output_dir / "excitation_vs_beta.png"
    beam_excitation_path = args.output_dir / "beam_excitation.png"
    excitation_beta_broad = args.output_dir / "excitation_vs_beta_broadened.png"
    excitation_laser_energy = args.output_dir / "excitation_vs_laser_energy.png"

    print(f"Ion: {ion.label}")
    print(f"beta: {ion.beta:.8f}")
    print(f"gamma: {ion.gamma:.8f}")
    print(f"Rest-frame transition energy: {transition.energy_eV:.6g} eV")
    print(f"Forward photon energy:  {spectrum.forward_energy_eV:.6g} eV")
    print(f"Backward photon energy: {spectrum.backward_energy_eV:.6g} eV")

    # Laser excitation
    laser = Laser(photon_energy_eV=args.laser_energy, energy_sigma_eV=args.laser_energy_sigma, angle_rad=np.pi) # angle = pi --> antikollinear
    resonance = Resonance(transition_energy_eV=transition.energy_eV, linewidth_eV=args.linewidth)

    laser_energy_rest = laser.energy_in_ion_rest_frame(ion.beta)
    detuning = resonance.detuning(laser, ion.beta)
    #excitation_weight = resonance.excitation_weight(laser, ion.beta)
    excitation_weight = resonance.excitation_weight_broadened(laser, ion.beta)

    print("\nLaser excitation:")
    print(f"Laser energy (lab):            {args.laser_energy:.6f} eV")
    print(f"Laser energy (ion frame):      {laser_energy_rest:.6f} eV")
    print(f"Detuning:                      {detuning: 6f} eV")
    print(f"Excitation weight (broadened): {excitation_weight: 6f}")




    plot_energy_vs_angle(spectrum, energy_path)
    plot_angular_distribution(angular, angular_path)
    plot_angular_distribution_2d(angular, angular_2d_path)
    plot_excitation_vs_beta(laser=laser, resonance=resonance, beta_center=ion.beta, output=excitation_path)
    _, _, expected_fraction = plot_beam_excitation(laser=laser, resonance=resonance, beta_center=ion.beta, beta_sigma=args.beta_sigma, output=beam_excitation_path)
    plot_excitation_vs_beta_broadened(laser, resonance, output=excitation_beta_broad)
    plot_excitation_vs_laser_energy(laser, resonance, ion.beta, output=excitation_laser_energy)

    print(f"Saved: {energy_path}")
    print(f"Saved: {angular_path}")
    print(f"Saved: {angular_2d_path}")
    print(f"Saved: {excitation_path}")
    print(f"Saved: {beam_excitation_path}")


    if args.no_show:
        plt.close("all")
    else:
        plt.show()


if __name__ == "__main__":
    main()

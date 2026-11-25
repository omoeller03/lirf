import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from .ion import Ion
from .transition import Transition
from .spectrum import FluorescenceSpectrum
from .angular_distribution import AngularDistribution
from .plotting import plot_energy_vs_angle, plot_angular_distribution


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Relativistic fluorescence photon calculator"
    )
    parser.add_argument("--beta", type=float, required=True,
                        help="Ion velocity divided by c")
    parser.add_argument("--transition-energy", type=float, required=True,
                        help="Transition energy in the ion rest frame [eV]")
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

    print(f"Ion: {ion.label}")
    print(f"beta: {ion.beta:.8f}")
    print(f"gamma: {ion.gamma:.8f}")
    print(f"Rest-frame transition energy: {transition.energy_eV:.6g} eV")
    print(f"Forward photon energy:  {spectrum.forward_energy_eV:.6g} eV")
    print(f"Backward photon energy: {spectrum.backward_energy_eV:.6g} eV")

    plot_energy_vs_angle(spectrum, energy_path)
    plot_angular_distribution(angular, angular_path)

    print(f"Saved: {energy_path}")
    print(f"Saved: {angular_path}")

    if args.no_show:
        plt.close("all")
    else:
        plt.show()


if __name__ == "__main__":
    main()

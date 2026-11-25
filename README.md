# Fluorescence

A small, platform-independent Python application for calculating relativistic
fluorescence-photon energies and angular distributions.

## Installation

```bash
python -m pip install -e .
```

Optional test dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Run

```bash
fluorescence --beta 0.996 --transition-energy 10000
```

Or, from the project directory:

```bash
python -m fluorescence.main --beta 0.996 --transition-energy 10000
```

The transition energy is given in eV. The beta value is v/c.

## Initial model and limitations

- The ion is represented by its speed `beta`.
- The transition energy is specified manually in the ion rest frame.
- Emission is initially assumed isotropic in the ion rest frame.
- Recoil, natural linewidth, laser excitation probability, polarization,
  magnetic-sublevel populations and detector response are not yet included.
- The laser parameters are not yet used to select resonantly excited ions.
  They will be added in the next development step.

The energy-angle relation and the angular distribution are calculated in the
laboratory frame using Lorentz transformations.

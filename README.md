# Fluorescence

A platform-independent Python application for calculating relativistic fluorescence-photon energies, angular distributions and laser excitation of fast ions.

## Features

- Relativistic calculation of fluorescence-photon energies in the laboratory frame.
- Angular distribution of emitted fluorescence photons.
- Laser excitation of ions using the relativistic Doppler shift.
- Lorentzian transition line shape with configurable linewidth.
- Gaussian laser energy distribution with configurable bandwidth.
- Excitation strength as a function of ion velocity and laser photon energy.
- Estimation of the excited fraction of an ion beam.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd lirf
```

### 2. Create a virtual environment

To create a Python virtual environment follow the description.

On Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

After activation, the virtual environment is indicated by `(.venv)` in the terminal.

To deactivate it:

```bash
deactivate
```

### 3. Install the application

With the virtual environment activated, install the project and its dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Optional development and test dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Run

The application can be started from the project directory using:

```bash
python -m fluorescence
```

For example:

```bash
python -m fluorescence \
    --beta 0.999 \
    --transition-energy 1000 \
    --laser-energy 22.366272 \
    --laser-energy-sigma 0.001 \
    --linewidth 0.1
```

### Parameters

| Parameter | Description | Unit |
|---|---|---|
| `--beta` | Ion velocity divided by the speed of light | – |
| `--transition-energy` | Transition energy in the ion rest frame | eV |
| `--laser-energy` | Central laser photon energy in the laboratory frame | eV |
| `--laser-energy-sigma` | Standard deviation of the Gaussian laser energy distribution | eV |
| `--linewidth` | Transition linewidth (FWHM) | eV |
| `--label` | Optional label for the ion | – |
| `--output-dir` | Directory for generated plots | – |
| `--no-show` | Save plots without opening plot windows | – |

Use `--help` to display all available command-line options:

```bash
python -m fluorescence --help
```

## Physical model and limitations

- The ion velocity is specified by `beta = v/c`.
- The transition energy and linewidth are defined in the ion rest frame.
- The transition is described by a Lorentzian line shape.
- The laser energy distribution is assumed to be Gaussian.
- The laser photon energy is transformed into the ion rest frame using the relativistic Doppler shift.
- Fluorescence emission is assumed to be isotropic in the ion rest frame.
- The excitation strength is a relative quantity between 0 and 1, not an absolute excitation probability.
- The estimated excited fraction depends on the assumed ion-beam velocity distribution.

Re

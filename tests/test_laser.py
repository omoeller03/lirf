
import numpy as np

from fluorescence.laser import Laser, Resonance

beta = 0.999
transition_energy = 1000.0  # eV

# Counter-propagating laser
laser = Laser(
    photon_energy_eV=22.366,
    angle_rad=np.pi,
)

resonance = Resonance(
    transition_energy_eV=transition_energy,
    linewidth_eV=0.1,
)

rest_energy = laser.energy_in_ion_rest_frame(beta)
detuning = resonance.detuning(laser, beta)
weight = resonance.excitation_weight(laser, beta)

print(f"Laser energy in ion frame: {rest_energy:.6f} eV")
print(f"Detuning:                  {detuning:.6f} eV")
print(f"Excitation weight:         {weight:.6f}")

required_energy = laser.resonant_lab_energy(
    beta,
    transition_energy,
)

print(f"Required laser energy:     {required_energy:.6f} eV")

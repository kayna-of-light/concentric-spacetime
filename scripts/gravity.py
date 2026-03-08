"""Gravitational quantum states on R⁺: linear potential + hard wall.

Reproduces the qBounce experiment (Nesvizhevsky et al. 2002): ultra-cold
neutrons bouncing above a mirror in Earth's gravity occupy discrete
quantum energy levels.  The solutions are Airy functions — eigenfunctions
of the linear potential on R⁺.

The linear potential V(z) = mgz acts on the radial coordinate R⁺.
The angular part (S²) is trivially l=0 since gravity at this scale
introduces no angular momentum structure.

Physics
-------
Schrödinger equation:  -ℏ²/(2m) ψ'' + mgz ψ = E ψ,  ψ(0) = 0

Substitution  ξ = z/z₀ + aₙ  where  z₀ = (ℏ²/(2m²g))^{1/3}
converts to the Airy equation  ψ''(ξ) = ξ ψ(ξ).

Eigenvalues:  E_n = |aₙ| × mgz₀   where aₙ are zeros of Ai(x).
"""

import numpy as np
from scipy.special import airy, ai_zeros
from scipy.integrate import quad


# ==============================================================================
# Physical constants (SI)
# ==============================================================================

HBAR = 1.054571817e-34       # ℏ  (J·s)
M_NEUTRON = 1.674927471e-27  # neutron mass (kg)
G_EARTH = 9.80665            # standard gravity (m/s²)
EV_TO_J = 1.602176634e-19    # J per eV
PEV_TO_J = EV_TO_J * 1e-12  # J per peV


# ==============================================================================
# Characteristic scales
# ==============================================================================

def characteristic_length(m=M_NEUTRON, g=G_EARTH):
    """Characteristic length z₀ = (ℏ²/(2m²g))^{1/3} in metres."""
    return (HBAR**2 / (2 * m**2 * g)) ** (1.0 / 3.0)


def energy_scale(m=M_NEUTRON, g=G_EARTH):
    """Energy scale E₀ = mgz₀ = (mg²ℏ²/2)^{1/3} in Joules."""
    return m * g * characteristic_length(m, g)


# ==============================================================================
# Eigenvalues
# ==============================================================================

def airy_zeros(n_max):
    """Return the first *n_max* zeros of Ai(x), all negative."""
    a, _ap, _ai, _aip = ai_zeros(n_max)
    return a


def energy_levels(n_max, m=M_NEUTRON, g=G_EARTH, unit="peV"):
    """Energy eigenvalues E_n = |aₙ| × E₀.

    Parameters
    ----------
    n_max : int
        Number of levels to compute.
    m, g : float
        Particle mass (kg) and gravitational acceleration (m/s²).
    unit : str
        ``'peV'`` for pico-electron-volts, ``'J'`` for Joules.

    Returns
    -------
    E : ndarray, shape (n_max,)
    """
    zeros = airy_zeros(n_max)
    E0 = energy_scale(m, g)
    E = np.abs(zeros) * E0
    if unit == "peV":
        E /= PEV_TO_J
    return E


def classical_turning_points(n_max, m=M_NEUTRON, g=G_EARTH, unit="um"):
    """Classical turning points z_n = E_n / (mg).

    Returns heights in micrometres (default) or metres.
    """
    E_J = energy_levels(n_max, m, g, unit="J")
    z = E_J / (m * g)
    if unit == "um":
        z *= 1e6
    return z


# ==============================================================================
# Wavefunctions
# ==============================================================================

def airy_wavefunction(z, n, m=M_NEUTRON, g=G_EARTH, normalize=True):
    """Evaluate ψ_n(z) = N × Ai(z/z₀ + aₙ).

    Parameters
    ----------
    z : array_like
        Height above mirror in metres.
    n : int
        Quantum number (1-indexed).
    m, g : float
        Particle mass and gravitational acceleration.
    normalize : bool
        If True, numerically normalize so ∫|ψ|²dz = 1.

    Returns
    -------
    psi : ndarray, same shape as *z*.
    """
    z = np.asarray(z, dtype=float)
    z0 = characteristic_length(m, g)
    zeros = airy_zeros(n)
    a_n = zeros[n - 1]  # n is 1-indexed

    xi = z / z0 + a_n
    ai_val, _aip, _bi, _bip = airy(xi)

    # Hard wall: ψ = 0 for z < 0
    psi = np.where(z >= 0, ai_val, 0.0)

    if normalize:
        # Integrate from 0 to well past the classical turning point
        z_max = np.abs(a_n) * z0 * 5.0

        def integrand(zz):
            val, _, _, _ = airy(zz / z0 + a_n)
            return val**2

        norm_sq, _ = quad(integrand, 0, z_max, limit=200)
        if norm_sq > 0:
            psi /= np.sqrt(norm_sq)

    return psi


# ==============================================================================
# Transition energies and frequencies
# ==============================================================================

def transition_energies(n_max, m=M_NEUTRON, g=G_EARTH, unit="peV"):
    """Upper-triangular matrix of transition energies ΔE_{i→j} = E_j - E_i."""
    E = energy_levels(n_max, m, g, unit=unit)
    n = len(E)
    dE = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dE[i, j] = E[j] - E[i]
    return dE


def transition_frequencies(n_max, m=M_NEUTRON, g=G_EARTH):
    """Transition frequencies in Hz: ν = ΔE / h."""
    dE_J = transition_energies(n_max, m, g, unit="J")
    return dE_J / (2.0 * np.pi * HBAR)


# ==============================================================================
# WKB semiclassical approximation
# ==============================================================================

def wkb_energies(n_max, m=M_NEUTRON, g=G_EARTH, unit="peV"):
    """WKB approximation: E_n^{WKB} = E₀ × [3π(n − ¼)/2]^{2/3}.

    Derived from Bohr–Sommerfeld quantization with Maslov index ¼:
        ∫₀^{z_n} √(2m(E − mgz)) dz = (n − ¼) π ℏ
    """
    E0 = energy_scale(m, g)
    n_arr = np.arange(1, n_max + 1, dtype=float)
    E = E0 * (1.5 * np.pi * (n_arr - 0.25)) ** (2.0 / 3.0)
    if unit == "peV":
        E /= PEV_TO_J
    return E


# ==============================================================================
# qBounce reference data
# Nesvizhevsky et al., Nature 415:297 (2002)
# Jenke et al., Nature Physics 7:468 (2011)
# ==============================================================================

QBOUNCE_ENERGIES_PEV = {1: 1.407, 2: 2.461, 3: 3.321}
QBOUNCE_HEIGHTS_UM = {1: 13.7, 2: 24.0, 3: 32.4}

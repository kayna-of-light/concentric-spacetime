"""Scattering cross-sections on S² × R⁺: partial wave analysis.

Partial wave decomposition is inherently an S² expansion: each angular
momentum channel l on the sphere contributes independently to the
scattering amplitude, weighted by a phase shift δ_l that encodes how
the radial wavefunction on R⁺ is modified by the potential.

Implements:
  - Hard-sphere scattering (analytical phase shifts)
  - Finite square-well scattering (numerical phase shifts, resonances)
  - Coulomb scattering (Rutherford formula from Coulomb phase shifts)
  - Optical theorem verification (unitarity on S²)
"""

import numpy as np
from scipy.special import spherical_jn, spherical_yn, gamma, eval_legendre


# ==============================================================================
# Phase shifts
# ==============================================================================

def hard_sphere_phase_shifts(k, a, l_max):
    """Phase shifts for a hard sphere of radius *a* at wavenumber *k*.

    Boundary condition ψ(a) = 0 gives:
        tan(δ_l) = j_l(ka) / y_l(ka)
    """
    x = k * a
    delta = np.zeros(l_max + 1)
    for l in range(l_max + 1):
        jl = spherical_jn(l, x)
        yl = spherical_yn(l, x)
        if abs(yl) > 1e-300:
            delta[l] = np.arctan2(jl, yl)
        else:
            delta[l] = 0.0
    return delta


def square_well_phase_shifts(k, V0, a, l_max):
    """Phase shifts for a finite square well: V = -V₀ for r < a, 0 for r > a.

    Works in units where ℏ = 1, 2m = 1, so E = k² and κ² = k² + V₀.
    """
    if k < 1e-15:
        return np.zeros(l_max + 1)
    kappa = np.sqrt(k**2 + V0)
    x_out = k * a
    x_in = kappa * a
    delta = np.zeros(l_max + 1)

    for l in range(l_max + 1):
        # Interior log-derivative
        jl_in = spherical_jn(l, x_in)
        djl_in = spherical_jn(l, x_in, derivative=True)
        if abs(jl_in) < 1e-300:
            continue
        gamma_val = kappa * djl_in / jl_in

        # Exterior functions and derivatives
        jl_out = spherical_jn(l, x_out)
        yl_out = spherical_yn(l, x_out)
        djl_out = spherical_jn(l, x_out, derivative=True)
        dyl_out = spherical_yn(l, x_out, derivative=True)

        num = k * djl_out - gamma_val * jl_out
        den = k * dyl_out - gamma_val * yl_out
        if abs(den) > 1e-300:
            delta[l] = np.arctan2(num, den)
    return delta


# ==============================================================================
# Coulomb scattering
# ==============================================================================

def coulomb_phase_shifts(eta, l_max):
    """Coulomb phase shifts σ_l = arg[Γ(l + 1 + iη)]."""
    sigma = np.zeros(l_max + 1)
    for l in range(l_max + 1):
        sigma[l] = np.angle(gamma(l + 1 + 1j * eta))
    return sigma


def rutherford_cross_section(theta, k, eta):
    """Rutherford differential cross-section dσ/dΩ = (η/(2k))² / sin⁴(θ/2).

    Parameters
    ----------
    theta : array_like
        Scattering angle in radians.
    k : float
        Wavenumber.
    eta : float
        Sommerfeld parameter η = Z₁Z₂e²m/(ℏ²k).
    """
    theta = np.asarray(theta, dtype=float)
    sin2 = np.sin(theta / 2.0) ** 2
    # Avoid division by zero at theta=0
    sin2 = np.where(sin2 < 1e-30, 1e-30, sin2)
    return (eta / (2.0 * k)) ** 2 / sin2**2


def coulomb_amplitude(theta, k, eta):
    """Exact Coulomb scattering amplitude.

    f_C(θ) = -η/(2k sin²(θ/2)) × exp(-iη ln(sin²(θ/2)) + 2iσ₀)
    """
    theta = np.asarray(theta, dtype=float)
    sin2 = np.sin(theta / 2.0) ** 2
    sin2 = np.where(sin2 < 1e-30, 1e-30, sin2)
    sigma0 = np.angle(gamma(1 + 1j * eta))
    phase = -eta * np.log(sin2) + 2.0 * sigma0
    return -eta / (2.0 * k * sin2) * np.exp(1j * phase)


# ==============================================================================
# Scattering amplitude and cross-sections
# ==============================================================================

def scattering_amplitude(theta, k, phase_shifts):
    """Partial wave scattering amplitude.

    f(θ) = (1/k) Σ_l (2l+1) e^{iδ_l} sin(δ_l) P_l(cos θ)
    """
    theta = np.asarray(theta, dtype=float)
    cos_theta = np.cos(theta)
    f = np.zeros(len(theta) if theta.ndim > 0 else 1, dtype=complex)
    if theta.ndim == 0:
        cos_theta = np.array([cos_theta])

    for l, dl in enumerate(phase_shifts):
        Pl = eval_legendre(l, cos_theta)
        f += (2 * l + 1) * np.exp(1j * dl) * np.sin(dl) * Pl

    f /= k
    if theta.ndim == 0:
        return f[0]
    return f


def differential_cross_section(theta, k, phase_shifts):
    """dσ/dΩ = |f(θ)|²."""
    f = scattering_amplitude(theta, k, phase_shifts)
    return np.abs(f) ** 2


def total_cross_section(k, phase_shifts):
    """σ_total = (4π/k²) Σ_l (2l+1) sin²(δ_l)."""
    sigma = 0.0
    for l, dl in enumerate(phase_shifts):
        sigma += (2 * l + 1) * np.sin(dl) ** 2
    return 4.0 * np.pi / k**2 * sigma


# ==============================================================================
# Optical theorem
# ==============================================================================

def verify_optical_theorem(k, phase_shifts):
    """Verify σ_total = (4π/k) Im[f(θ=0)].

    Returns (sigma_partial_wave, sigma_optical, relative_error).
    """
    sigma_pw = total_cross_section(k, phase_shifts)
    f0 = scattering_amplitude(np.array([0.0]), k, phase_shifts)[0]
    sigma_opt = 4.0 * np.pi / k * f0.imag
    if abs(sigma_pw) > 1e-30:
        rel_err = abs(sigma_opt - sigma_pw) / sigma_pw
    else:
        rel_err = 0.0
    return sigma_pw, sigma_opt, rel_err

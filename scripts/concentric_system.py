"""
The Four-Prime Concentric System on S² × R⁺

Correct formalization of the coordinate space described in:
  "The Resolution of the Finite Mind"
      — primes as irreducible dimensions of finite comprehension
  "Orbits That Lost Their Center"
      — concentric geometry on a curved manifold, not Cartesian grid

The manifold is S² × R⁺ (sphere + radial half-line), NOT T⁴ (flat torus).

The wave equation on this curved space produces:
  · Spherical harmonics Y_l^m as angular standing waves on S²
  · Radial eigenfunctions R_nl as shell structure on R⁺
  · Nesting constraints |m| ≤ l < n emerging from the geometry itself

Prime → Coordinate → Quantum Number:
  p=2 (bilateral)     → φ azimuthal [0,2π)  → m magnetic
  p=3 (vertical)      → θ polar     [0,π]   → l angular momentum
  p=5 (radial)        → r radial    [0,∞)   → n principal
  p=7 (developmental) → t time              → cumulative state evolution
"""

import numpy as np
from scipy.special import sph_harm_y, factorial


# ═══════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════

PRIMES = np.array([2, 3, 5, 7])

CORRESPONDENCE = {
    2: dict(cut='bilateral',     coord='φ (azimuthal)', range='[0, 2π)',
            quantum='m (magnetic)',      topology='circle S¹'),
    3: dict(cut='vertical',      coord='θ (polar)',     range='[0, π]',
            quantum='l (angular mom.)',  topology='bounded interval'),
    5: dict(cut='radial',        coord='r (radial)',    range='[0, ∞)',
            quantum='n (principal)',     topology='half-line R⁺'),
    7: dict(cut='developmental', coord='t (time)',      range='monotonic',
            quantum='cumulative state',  topology='developmental arc'),
}


# ═══════════════════════════════════════════════════════════
# Angular structure: Spherical Harmonics on S²
# ═══════════════════════════════════════════════════════════

def angular_wavefunction(l: int, m: int, theta, phi):
    """
    Spherical harmonic Y_l^m(θ, φ).

    θ = polar (colatitude) ∈ [0, π]   — vertical resolution (p=3)
    φ = azimuthal           ∈ [0, 2π) — bilateral orientation (p=2)

    Constraint |m| ≤ l EMERGES from solving ∇²Y = −l(l+1)Y on S².

    scipy 1.14+: sph_harm_y(l, m, θ_polar, φ_azimuthal).
    """
    return sph_harm_y(l, m, theta, phi)


def angular_eigenvalue(l: int, R: float = 1.0):
    """
    Eigenvalue of −∇² on sphere of radius R:  λ_l = l(l+1) / R².
    (2l+1)-fold degenerate in m.

    R → ∞ : λ → 0   (flat, continuous spectrum, no discrete structure)
    R → 0 : λ → ∞   (maximum curvature, maximum separation)
    """
    return l * (l + 1) / R**2


# ═══════════════════════════════════════════════════════════
# Radial structure: Shells on R⁺
# ═══════════════════════════════════════════════════════════

def _assoc_laguerre(x, k: int, alpha: int):
    """Associated Laguerre polynomial L_k^α(x) via stable recurrence."""
    x = np.asarray(x, dtype=float)
    if k == 0:
        return np.ones_like(x)
    L0 = np.ones_like(x)
    L1 = 1.0 + alpha - x
    if k == 1:
        return L1
    for j in range(2, k + 1):
        L2 = ((2 * j - 1 + alpha - x) * L1 - (j - 1 + alpha) * L0) / j
        L0, L1 = L1, L2
    return L1


def radial_wavefunction(n: int, l: int, r):
    """
    Hydrogen-like radial wavefunction R_nl(r)  (atomic units, a₀ = 1).

    n = principal quantum number (p=5, radial depth)
    l = angular momentum (constraint l < n emerges from normalizability)

    Numerically normalised: ∫₀^∞ |R_nl|² r² dr = 1.
    """
    if l >= n:
        raise ValueError(f"l={l} must be < n={n} (nesting constraint)")
    r = np.asarray(r, dtype=float)
    rho = 2.0 * r / n
    L = _assoc_laguerre(rho, n - l - 1, 2 * l + 1)
    R = np.exp(-rho / 2) * rho**l * L
    # Numerical normalisation
    if r.size > 1:
        dr = np.diff(r)
        integrand = R[:-1]**2 * r[:-1]**2
        norm_sq = np.sum(integrand * dr)
        if norm_sq > 0:
            R = R / np.sqrt(norm_sq)
    return R


def radial_probability(n: int, l: int, r):
    """Radial probability density P(r) = r² |R_nl(r)|²."""
    R = radial_wavefunction(n, l, r)
    return r**2 * R**2


# ═══════════════════════════════════════════════════════════
# Energy
# ═══════════════════════════════════════════════════════════

def energy_level(n: int):
    """E_n = −1/(2n²) atomic units.  Inner shells (small n) are lowest."""
    return -1.0 / (2 * n**2)


# ═══════════════════════════════════════════════════════════
# Nesting constraints  (EMERGE from the geometry)
# ═══════════════════════════════════════════════════════════

def valid_states(n_max: int):
    """
    All (n, l, m) satisfying  1 ≤ n ≤ n_max,  0 ≤ l < n,  |m| ≤ l.

    These ARE the nesting constraints of the four-prime system:
        p=5 (n)  constrains  p=3 (l)  constrains  p=2 (m).
    """
    out = []
    for n in range(1, n_max + 1):
        for l in range(n):
            for m in range(-l, l + 1):
                out.append((n, l, m))
    return out


def states_per_shell(n: int):
    """States at level n = n²."""
    return n * n


def cumulative_states(n_max: int):
    """Total states through level n_max = n(n+1)(2n+1)/6."""
    return n_max * (n_max + 1) * (2 * n_max + 1) // 6


# ═══════════════════════════════════════════════════════════
# Curvature
# ═══════════════════════════════════════════════════════════

def gaussian_curvature(R: float):
    """
    Gaussian curvature of S² with radius R:  K = 1/R².
    K > 0 : center exists  →  curved  →  discrete structure
    K → 0 : center forgotten  →  flat  →  proprium's geometry
    """
    return 1.0 / R**2 if R > 0 else float('inf')


def eigenvalue_gap(l: int, R: float):
    """Gap Δλ = λ_{l+1} − λ_l = 2(l+1)/R².  → 0 as R → ∞."""
    return 2 * (l + 1) / R**2


# ═══════════════════════════════════════════════════════════
# Time evolution  (p=7: the developmental arc)
# ═══════════════════════════════════════════════════════════

def phase_factors(n_max: int, t):
    """
    Time-evolution phases  e^{−i E_n t}  for shells 1 … n_max.

    Each shell oscillates at its own energy-frequency.
    The total state at time t is a superposition weighted by these phases.
    """
    t = np.asarray(t, dtype=float)
    return {n: np.exp(-1j * energy_level(n) * t)
            for n in range(1, n_max + 1)}


def wavepacket_autocorrelation(coeffs: dict, t):
    """
    |⟨Ψ(0)|Ψ(t)⟩|² for a superposition Ψ = Σ c_n |n⟩.

    Pure eigenstate  → constant 1  (no temporal structure).
    Superposition    → oscillates  (temporal complexity from spatial content).
    More shells occupied  →  richer temporal pattern.
    """
    t = np.asarray(t, dtype=float)
    n_max = max(coeffs)
    phases = phase_factors(n_max, t)
    overlap = sum(np.abs(c)**2 * phases[n] for n, c in coeffs.items())
    return np.abs(overlap)**2

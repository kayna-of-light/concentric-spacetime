"""Band structure and solid-state physics on R⁺: periodic potentials.

When atoms form a periodic lattice, the allowed electron energies split into
bands separated by gaps. The Kronig-Penney model — a periodic square-well
potential on R⁺ — captures this exactly via a transfer matrix that encodes
how wavefunctions propagate through one unit cell.

Implements:
  - Kronig-Penney dispersion relation via transfer matrix
  - Band structure extraction (allowed/forbidden energy regions)
  - Nearly-free electron perturbation theory
  - Tight-binding cosine bands
  - Effective mass from band curvature
  - Density of states from inverse group velocity
"""

import numpy as np
from scipy.optimize import brentq


# ==============================================================================
# Kronig-Penney Model
# ==============================================================================

def kronig_penney_rhs(E, V0, a, b):
    """Right-hand side of the Kronig-Penney dispersion relation.

    For a periodic potential with wells of width (a-b) and barriers of width b
    at height V0, the dispersion relation is:

        cos(Ka) = cos(α(a-b)) cos(βb) - ½(β/α + α/β) sin(α(a-b)) sin(βb)

    for E < V0 (tunnelling through barrier), or with cosh/sinh when E < V0.

    Parameters
    ----------
    E : float or array
        Electron energy (ℏ=1, 2m=1 units, so E = k²).
    V0 : float
        Barrier height.
    a : float
        Lattice constant (period).
    b : float
        Barrier width.

    Returns
    -------
    rhs : float or array
        The value that must equal cos(Ka) for allowed states.
    """
    E = np.asarray(E, dtype=float)
    w = a - b  # well width

    rhs = np.zeros_like(E)
    for i in range(len(E.flat)):
        Ei = E.flat[i]
        if Ei <= 0:
            rhs.flat[i] = 2.0  # forbidden
            continue

        alpha = np.sqrt(Ei)  # wavevector in well (V=0 region)

        if Ei < V0:
            # Tunnelling: evanescent in barrier
            beta = np.sqrt(V0 - Ei)
            rhs.flat[i] = (np.cos(alpha * w) * np.cosh(beta * b)
                           + 0.5 * (beta / alpha - alpha / beta)
                           * np.sin(alpha * w) * np.sinh(beta * b))
        elif abs(Ei - V0) < 1e-12:
            # E = V0 edge case
            rhs.flat[i] = np.cos(alpha * w) - 0.5 * alpha * b * np.sin(alpha * w)
        else:
            # Propagating in both regions
            beta = np.sqrt(Ei - V0)
            rhs.flat[i] = (np.cos(alpha * w) * np.cos(beta * b)
                           - 0.5 * (beta / alpha + alpha / beta)
                           * np.sin(alpha * w) * np.sin(beta * b))
    return rhs


def band_structure(V0, a, b, n_bands=6, n_k=200):
    """Compute band structure E(K) for the Kronig-Penney model.

    Parameters
    ----------
    V0 : float
        Barrier height.
    a : float
        Lattice constant.
    b : float
        Barrier width.
    n_bands : int
        Number of bands to find.
    n_k : int
        Number of K-points in the first Brillouin zone.

    Returns
    -------
    K_values : (n_k,) array
        Crystal momentum in [0, π/a].
    bands : list of (n_k,) arrays
        Energy for each band at each K-point.
    gaps : list of (E_bottom, E_top) tuples
        Band gaps between consecutive bands.
    """
    K_values = np.linspace(0, np.pi / a, n_k)

    # Find allowed energy ranges by scanning
    E_max = V0 + (n_bands + 2) ** 2 * np.pi ** 2 / a ** 2
    E_scan = np.linspace(1e-6, E_max, 20000)
    rhs_scan = kronig_penney_rhs(E_scan, V0, a, b)

    # Identify band edges where |rhs| crosses 1
    in_band = np.abs(rhs_scan) <= 1.0
    transitions = np.diff(in_band.astype(int))
    starts = np.where(transitions == 1)[0]
    ends = np.where(transitions == -1)[0]

    # Pair them up
    band_ranges = []
    for s in starts:
        matching_ends = ends[ends > s]
        if len(matching_ends) > 0:
            band_ranges.append((E_scan[s], E_scan[matching_ends[0] + 1]))
        if len(band_ranges) >= n_bands:
            break

    # For each K, solve for E in each band
    bands = []
    for bmin, bmax in band_ranges:
        E_band = np.zeros(n_k)
        E_fine = np.linspace(bmin, bmax, 5000)
        rhs_fine = kronig_penney_rhs(E_fine, V0, a, b)

        for j, K in enumerate(K_values):
            target = np.cos(K * a)
            diff = rhs_fine - target
            # Find zero crossings
            crossings = np.where(np.diff(np.sign(diff)))[0]
            if len(crossings) > 0:
                idx = crossings[0]
                # Linear interpolation
                E1, E2 = E_fine[idx], E_fine[idx + 1]
                d1, d2 = diff[idx], diff[idx + 1]
                if abs(d2 - d1) > 1e-30:
                    E_band[j] = E1 - d1 * (E2 - E1) / (d2 - d1)
                else:
                    E_band[j] = 0.5 * (E1 + E2)
            else:
                E_band[j] = np.nan

        bands.append(E_band)

    # Compute gaps
    gaps = []
    for i in range(len(bands) - 1):
        top_of_lower = np.nanmax(bands[i])
        bottom_of_upper = np.nanmin(bands[i + 1])
        if bottom_of_upper > top_of_lower:
            gaps.append((top_of_lower, bottom_of_upper))
        else:
            gaps.append(None)

    return K_values, bands, gaps


# ==============================================================================
# Nearly-Free Electron Model
# ==============================================================================

def nearly_free_electron(V1, a, n_k=200):
    """Nearly-free electron band structure with weak periodic potential.

    For V(x) = 2V₁ cos(2πx/a), gaps of width 2|V₁| open at zone boundaries.
    Returns the first two bands from degenerate perturbation theory.

    Parameters
    ----------
    V1 : float
        Fourier component of the periodic potential.
    a : float
        Lattice constant.
    n_k : int
        Number of K-points.

    Returns
    -------
    K_values : array
    E_lower : array
        Lower band (first Brillouin zone).
    E_upper : array
        Upper band.
    gap : float
        Band gap width (= 2|V1|).
    """
    K = np.linspace(-np.pi / a, np.pi / a, n_k)
    G = 2 * np.pi / a  # reciprocal lattice vector

    E_lower = np.zeros(n_k)
    E_upper = np.zeros(n_k)

    for i, k in enumerate(K):
        E0_k = k ** 2           # free electron at k
        E0_kG = (k - G) ** 2   # free electron at k-G
        avg = 0.5 * (E0_k + E0_kG)
        diff = 0.5 * (E0_k - E0_kG)
        coupling = np.sqrt(diff ** 2 + V1 ** 2)
        E_lower[i] = avg - coupling
        E_upper[i] = avg + coupling

    return K, E_lower, E_upper, 2 * abs(V1)


# ==============================================================================
# Tight-Binding Model
# ==============================================================================

def tight_binding(E0, t, a, n_k=200):
    """1D tight-binding band structure.

    E(k) = E₀ - 2t cos(ka)

    Parameters
    ----------
    E0 : float
        On-site energy.
    t : float
        Hopping integral.
    a : float
        Lattice constant.
    n_k : int
        Number of K-points.

    Returns
    -------
    K_values : array
    E_band : array
    bandwidth : float (= 4|t|)
    """
    K = np.linspace(-np.pi / a, np.pi / a, n_k)
    E_band = E0 - 2 * t * np.cos(K * a)
    return K, E_band, 4 * abs(t)


# ==============================================================================
# Effective Mass
# ==============================================================================

def effective_mass(K_values, E_band):
    """Compute effective mass m* = ℏ²/(d²E/dk²) at each k-point.

    In our units (ℏ=1, 2m=1), the free electron has d²E/dk² = 2,
    so m* = 1/(d²E/dk²) in these units.

    Returns
    -------
    K_interior : array
        K-points (excluding endpoints).
    m_star : array
        Effective mass at each interior point.
    """
    dK = K_values[1] - K_values[0]
    d2E = np.gradient(np.gradient(E_band, dK), dK)
    # Clip to interior (away from endpoints where gradient is unreliable)
    margin = 3
    K_int = K_values[margin:-margin]
    m_star = np.where(np.abs(d2E[margin:-margin]) > 1e-10,
                      1.0 / d2E[margin:-margin], np.inf)
    return K_int, m_star


# ==============================================================================
# Density of States
# ==============================================================================

def density_of_states(K_values, E_band, n_E=500):
    """Compute 1D density of states g(E) = (1/π)|dk/dE|.

    Parameters
    ----------
    K_values : array
        Crystal momenta (should be in [0, π/a] for positive branch).
    E_band : array
        Band energies at each K.
    n_E : int
        Number of energy points.

    Returns
    -------
    E_grid : array
        Energy grid within the band range.
    dos : array
        Density of states at each energy.
    """
    E_min, E_max = np.nanmin(E_band), np.nanmax(E_band)
    E_grid = np.linspace(E_min + 1e-6, E_max - 1e-6, n_E)

    dK = K_values[1] - K_values[0]
    dE_dk = np.gradient(E_band, dK)

    dos = np.zeros(n_E)
    for i, E in enumerate(E_grid):
        # Find k-points where E_band is close to E
        diff = E_band - E
        crossings = np.where(np.diff(np.sign(diff)))[0]
        for c in crossings:
            # Interpolate dk/dE at crossing
            v_group = abs(dE_dk[c])
            if v_group > 1e-10:
                dos[i] += 1.0 / (np.pi * v_group)

    return E_grid, dos

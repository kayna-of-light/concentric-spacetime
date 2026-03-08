"""Molecular binding on S² × R⁺: two-center integrals and H₂ calculations.

Uses STO-3G basis (Hehre, Stewart, Pople 1969) for analytical Gaussian integrals.
The angular structure of the AOs comes from S² (spherical harmonics),
while the radial part is approximated by contracted Gaussians on R⁺.
"""

import numpy as np
from scipy.special import erf
from scipy.optimize import minimize_scalar
from scipy.interpolate import UnivariateSpline
from scipy.linalg import eigh


# ==============================================================================
# STO-3G basis set for 1s orbital (zeta = 1.0)
# From Hehre, Stewart, Pople, J. Chem. Phys. 51, 2657 (1969)
# ==============================================================================

_STO3G_ALPHA_ZETA1 = np.array([0.109818, 0.405771, 2.22766])
_STO3G_COEFF = np.array([0.444635, 0.535328, 0.154329])


def _sto3g_params(zeta=1.0):
    """Return scaled STO-3G exponents and normalised contraction coefficients."""
    alphas = _STO3G_ALPHA_ZETA1 * zeta ** 2
    norms = (2 * alphas / np.pi) ** 0.75
    coeffs = _STO3G_COEFF * norms          # absorb normalisation into coefficients
    return alphas, coeffs


# ==============================================================================
# Boys function F₀(t) — the incomplete gamma function for s-type Gaussians
# ==============================================================================

def _boys_f0(t):
    """Boys function F₀(t) = erf(√t)·√π/(2√t) for t>0, 1.0 for t≈0."""
    t = np.asarray(t, dtype=float)
    result = np.ones_like(t)
    mask = t > 1e-10
    result[mask] = 0.5 * np.sqrt(np.pi / t[mask]) * erf(np.sqrt(t[mask]))
    return result if result.ndim > 0 else float(result)


# ==============================================================================
# Primitive s-type Gaussian integrals (two-center)
# ==============================================================================

def _overlap_prim(a, A, b, B):
    """Overlap ⟨g_a(A)|g_b(B)⟩ for primitive s-Gaussians."""
    gamma = a + b
    Rsq = np.sum((A - B) ** 2)
    return (np.pi / gamma) ** 1.5 * np.exp(-a * b / gamma * Rsq)


def _kinetic_prim(a, A, b, B):
    """Kinetic integral ⟨g_a(A)|−½∇²|g_b(B)⟩."""
    gamma = a + b
    Rsq = np.sum((A - B) ** 2)
    ab_g = a * b / gamma
    S = (np.pi / gamma) ** 1.5 * np.exp(-ab_g * Rsq)
    return ab_g * (3 - 2 * ab_g * Rsq) * S


def _nuclear_prim(a, A, b, B, C, Z_C=1.0):
    """Nuclear attraction ⟨g_a(A)|−Z/r_C|g_b(B)⟩."""
    gamma = a + b
    P = (a * A + b * B) / gamma
    Rsq_AB = np.sum((A - B) ** 2)
    Rsq_PC = np.sum((P - C) ** 2)
    pre = -Z_C * 2 * np.pi / gamma * np.exp(-a * b / gamma * Rsq_AB)
    return pre * _boys_f0(gamma * Rsq_PC)


def _eri_prim(a, A, b, B, c, C, d, D):
    """Electron repulsion (ab|cd) in Mulliken notation for s-Gaussians."""
    gamma1 = a + b
    gamma2 = c + d
    P = (a * A + b * B) / gamma1
    Q = (c * C + d * D) / gamma2
    Rsq_AB = np.sum((A - B) ** 2)
    Rsq_CD = np.sum((C - D) ** 2)
    Rsq_PQ = np.sum((P - Q) ** 2)
    delta = gamma1 + gamma2
    pre = (2 * np.pi ** 2.5 / (gamma1 * gamma2 * np.sqrt(delta))
           * np.exp(-a * b / gamma1 * Rsq_AB - c * d / gamma2 * Rsq_CD))
    return pre * _boys_f0(gamma1 * gamma2 / delta * Rsq_PQ)


# ==============================================================================
# Contracted STO-3G integrals
# ==============================================================================

def _contract_1e(prim_func, A, B, zeta_a=1.0, zeta_b=1.0, **kwargs):
    """Contract a one-electron primitive integral over STO-3G shells."""
    alphas_a, coeffs_a = _sto3g_params(zeta_a)
    alphas_b, coeffs_b = _sto3g_params(zeta_b)
    val = 0.0
    for i in range(3):
        for j in range(3):
            val += coeffs_a[i] * coeffs_b[j] * prim_func(
                alphas_a[i], A, alphas_b[j], B, **kwargs)
    return val


def _contract_2e(A, B, C, D, zeta_a=1.0, zeta_b=1.0, zeta_c=1.0, zeta_d=1.0):
    """Contract an ERI over STO-3G shells."""
    aa, ca = _sto3g_params(zeta_a)
    ab, cb = _sto3g_params(zeta_b)
    ac, cc = _sto3g_params(zeta_c)
    ad, cd = _sto3g_params(zeta_d)
    val = 0.0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    val += (ca[i] * cb[j] * cc[k] * cd[l]
                            * _eri_prim(aa[i], A, ab[j], B,
                                        ac[k], C, ad[l], D))
    return val


# ==============================================================================
# H₂⁺ molecular ion
# ==============================================================================

def h2plus_energy(R, zeta=1.0):
    """H₂⁺ LCAO-MO energy at internuclear distance R (a.u.).

    Returns (E_bonding, E_antibonding).
    """
    A = np.array([0.0, 0.0, -R / 2])
    B = np.array([0.0, 0.0, R / 2])

    S = _contract_1e(_overlap_prim, A, B, zeta, zeta)
    h_AA = (_contract_1e(_kinetic_prim, A, A, zeta, zeta)
            + _contract_1e(_nuclear_prim, A, A, zeta, zeta, C=A)
            + _contract_1e(_nuclear_prim, A, A, zeta, zeta, C=B))
    h_AB = (_contract_1e(_kinetic_prim, A, B, zeta, zeta)
            + _contract_1e(_nuclear_prim, A, B, zeta, zeta, C=A)
            + _contract_1e(_nuclear_prim, A, B, zeta, zeta, C=B))

    E_g = (h_AA + h_AB) / (1 + S) + 1 / R
    E_u = (h_AA - h_AB) / (1 - S) + 1 / R
    return E_g, E_u


def h2plus_energy_opt(R):
    """H₂⁺ energy with variationally optimised ζ."""
    res = minimize_scalar(lambda z: h2plus_energy(R, zeta=z)[0],
                          bounds=(0.5, 3.0), method='bounded')
    return h2plus_energy(R, zeta=res.x)[0], res.x


# ==============================================================================
# H₂ molecule — integrals in AO and MO bases
# ==============================================================================

def _h2_integrals(R, zeta=1.0):
    """Build all one- and two-electron integrals for minimal basis H₂."""
    A = np.array([0.0, 0.0, -R / 2])
    B = np.array([0.0, 0.0, R / 2])
    centers = [A, B]

    # Overlap matrix
    S = np.zeros((2, 2))
    H_core = np.zeros((2, 2))
    for p in range(2):
        for q in range(2):
            S[p, q] = _contract_1e(_overlap_prim,
                                   centers[p], centers[q], zeta, zeta)
            H_core[p, q] = (_contract_1e(_kinetic_prim,
                                         centers[p], centers[q], zeta, zeta)
                            + _contract_1e(_nuclear_prim,
                                           centers[p], centers[q], zeta, zeta,
                                           C=A)
                            + _contract_1e(_nuclear_prim,
                                           centers[p], centers[q], zeta, zeta,
                                           C=B))

    # Two-electron integrals
    eri = np.zeros((2, 2, 2, 2))
    for p in range(2):
        for q in range(2):
            for r in range(2):
                for s in range(2):
                    eri[p, q, r, s] = _contract_2e(
                        centers[p], centers[q], centers[r], centers[s],
                        zeta, zeta, zeta, zeta)

    return S, H_core, eri


def h2_energy(R, method='ci', zeta=1.0):
    """H₂ total energy at internuclear distance R (a.u.).

    Parameters
    ----------
    R : float
        Internuclear distance in bohr.
    method : {'hf', 'ci', 'hl'}
        'hf'  — Hartree-Fock (both electrons in σ_g)
        'ci'  — Configuration Interaction (σ_g² + σ_u²)
        'hl'  — Heitler-London
    zeta : float
        STO orbital exponent.

    Returns
    -------
    E : float
        Total energy including nuclear repulsion (hartree).
    """
    S_mat, H_core, eri = _h2_integrals(R, zeta)
    V_nn = 1.0 / R

    if method == 'hl':
        S_ab = S_mat[0, 1]
        H_11 = H_core[0, 0] + H_core[1, 1] + eri[0, 0, 1, 1]
        H_12 = S_ab * H_core[0, 1] + S_ab * H_core[1, 0] + eri[0, 1, 1, 0]
        E_s = (H_11 + H_12) / (1 + S_ab ** 2) + V_nn
        return E_s

    # Solve generalised eigenvalue problem for MO coefficients
    evals, C = eigh(H_core, S_mat)

    # MO integrals
    h_mo = C.T @ H_core @ C
    eri_mo = np.einsum('ip,jq,ijkl,kr,ls->pqrs', C, C, eri, C, C)

    if method == 'hf':
        return 2 * h_mo[0, 0] + eri_mo[0, 0, 0, 0] + V_nn

    # CI: diagonalise in {|σ_g²⟩, |σ_u²⟩}
    H_CI = np.array([
        [2 * h_mo[0, 0] + eri_mo[0, 0, 0, 0], eri_mo[0, 1, 0, 1]],
        [eri_mo[0, 1, 0, 1], 2 * h_mo[1, 1] + eri_mo[1, 1, 1, 1]]
    ])
    return np.linalg.eigvalsh(H_CI)[0] + V_nn


def h2_energy_opt(R, method='ci'):
    """H₂ energy with variationally optimised ζ."""
    res = minimize_scalar(lambda z: h2_energy(R, method=method, zeta=z),
                          bounds=(0.5, 3.0), method='bounded')
    return h2_energy(R, method=method, zeta=res.x), res.x


# ==============================================================================
# Potential energy surface scan and analysis
# ==============================================================================

def pes_scan(R_values, species='h2', method='ci', optimize_zeta=False):
    """Scan potential energy surface.

    Returns arrays (energies, zetas) — zetas is None when not optimising.
    """
    energies = np.empty(len(R_values))
    zetas = np.empty(len(R_values)) if optimize_zeta else None

    for i, R in enumerate(R_values):
        if species == 'h2plus':
            if optimize_zeta:
                energies[i], zetas[i] = h2plus_energy_opt(R)
            else:
                energies[i] = h2plus_energy(R, zeta=1.0)[0]
        else:
            if optimize_zeta:
                energies[i], zetas[i] = h2_energy_opt(R, method=method)
            else:
                energies[i] = h2_energy(R, method=method, zeta=1.0)
    return energies, zetas


def find_equilibrium(R_values, energies):
    """Find equilibrium distance, minimum energy, and dissociation energy.

    Returns (R_eq, E_min, D_e_eV).
    """
    spl = UnivariateSpline(R_values, energies, s=0, k=4)
    res = minimize_scalar(lambda r: float(spl(r)),
                          bounds=(R_values[1], R_values[-2]),
                          method='bounded')
    R_eq = res.x
    E_min = float(spl(R_eq))
    E_inf = energies[-1]
    D_e_eV = (E_inf - E_min) * 27.2114
    return R_eq, E_min, D_e_eV


def vibrational_frequency(R_values, energies, R_eq, mu_amu):
    """Harmonic vibrational frequency from PES curvature.

    Parameters
    ----------
    R_values, energies : arrays
    R_eq : float  — equilibrium distance (bohr)
    mu_amu : float — reduced mass (amu).  H₂: 0.50391, H₂⁺: 0.50391

    Returns
    -------
    nu_cm : float — wavenumber in cm⁻¹
    k_au  : float — force constant in Ha/bohr²
    """
    spl = UnivariateSpline(R_values, energies, s=0, k=4)
    k_au = float(spl.derivative(n=2)(R_eq))

    # Work in atomic units, then convert to cm⁻¹
    mu_au = mu_amu * 1822.888          # amu → electron masses
    omega_au = np.sqrt(abs(k_au) / mu_au)
    # 1 a.u. of angular frequency = 4.1341e16 s⁻¹
    # ν̃ = ω/(2πc) with c = 2.998e10 cm/s
    nu_cm = omega_au * 4.1341e16 / (2 * np.pi * 2.998e10)
    return nu_cm, k_au

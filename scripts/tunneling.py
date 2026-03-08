"""Quantum tunneling and alpha decay on R⁺.

Demonstrates that radioactive decay lifetimes emerge from WKB barrier
penetration on the radial half-line R⁺, with the Coulomb barrier as
the potential.

Units: MeV for energy, fm for length.
Physical constants in MeV·fm units.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Physical constants (MeV·fm units)
# ---------------------------------------------------------------------------

HBAR_C = 197.3269804  # ℏc in MeV·fm
E2 = 1.4399764       # e² in MeV·fm (Coulomb constant × e²)
AMU_MEV = 931.494     # 1 amu in MeV/c²


# ---------------------------------------------------------------------------
# Rectangular barrier (textbook exact)
# ---------------------------------------------------------------------------

def rectangular_barrier_transmission(E: float, V0: float, a: float,
                                     m: float = 1.0) -> float:
    """Exact transmission coefficient for a rectangular barrier.

    T = 1 / (1 + V0²sin²(κa)/(4E(V0-E)))  for E < V0
    where κ = sqrt(2m(V0-E))/ℏ.

    Parameters
    ----------
    E : particle energy (MeV)
    V0 : barrier height (MeV)
    a : barrier width (fm)
    m : particle mass (amu)
    """
    if abs(E - V0) < 1e-12:
        # At barrier top — limiting case: T = 1/(1 + m*V0*a²/(2ℏ²))
        ka2 = 2 * m * AMU_MEV * V0 * a**2 / HBAR_C**2
        return 1.0 / (1 + ka2 / 4)

    if E > V0:
        # Above barrier — oscillatory
        k = np.sqrt(2 * m * AMU_MEV * (E - V0)) / HBAR_C
        denom = 1 + V0**2 * np.sin(k * a)**2 / (4 * E * (E - V0))
        return 1.0 / denom

    # Below barrier — tunneling
    kappa = np.sqrt(2 * m * AMU_MEV * (V0 - E)) / HBAR_C
    sinh_val = np.sinh(kappa * a)
    denom = 1 + V0**2 * sinh_val**2 / (4 * E * (V0 - E))
    return 1.0 / denom


# ---------------------------------------------------------------------------
# Coulomb barrier for alpha decay
# ---------------------------------------------------------------------------

def coulomb_barrier(r: np.ndarray, Z_daughter: int, R_touch: float) -> np.ndarray:
    """Coulomb barrier for alpha particle (Z=2) outside nuclear radius.

    V(r) = 2 * Z_daughter * e² / r    for r > R_touch
    V(r) = -V0 (nuclear well)          for r < R_touch

    Returns potential in MeV.
    """
    V = np.where(r > R_touch,
                 2 * Z_daughter * E2 / r,
                 np.zeros_like(r))
    return V


def gamow_factor(Q_alpha: float, Z_daughter: int, A_daughter: int) -> float:
    """Compute the Gamow factor γ for alpha decay via WKB on R⁺.

    γ = ∫_R^b sqrt(2μ(V(r) - Q)/ℏ²) dr

    where R is the nuclear touch radius, b is the classical turning point,
    and μ is the reduced mass.

    Parameters
    ----------
    Q_alpha : alpha decay energy (kinetic energy of alpha) in MeV
    Z_daughter : atomic number of daughter nucleus
    A_daughter : mass number of daughter nucleus

    Returns
    -------
    gamma : the Gamow factor (dimensionless)
    """
    # Reduced mass of alpha + daughter system
    A_alpha = 4
    mu_amu = (A_alpha * A_daughter) / (A_alpha + A_daughter)  # in amu
    mu_mev = mu_amu * AMU_MEV  # MeV/c²

    # Nuclear touch radius R = r0 * (A_alpha^{1/3} + A_daughter^{1/3})
    r0 = 1.2  # fm
    R = r0 * (A_alpha**(1/3) + A_daughter**(1/3))

    # Classical turning point: V(b) = Q_alpha
    # 2 * Z_daughter * e² / b = Q_alpha
    b = 2 * Z_daughter * E2 / Q_alpha

    if b <= R:
        return 0.0  # No barrier

    # Numerical WKB integral on R⁺
    r = np.linspace(R, b, 10000)
    V = 2 * Z_daughter * E2 / r  # Coulomb barrier in MeV
    kappa = np.sqrt(2 * mu_mev * np.maximum(V - Q_alpha, 0)) / HBAR_C  # 1/fm
    gamma = np.trapezoid(kappa, r)

    return gamma


def alpha_half_life(Q_alpha: float, Z_daughter: int, A_daughter: int,
                    A_parent: int) -> float:
    """Estimate alpha decay half-life from WKB tunneling on R⁺.

    t½ = ln(2) / (ν × T)

    where ν is the assault frequency and T = e^{-2γ}.

    Parameters
    ----------
    Q_alpha : alpha decay energy in MeV
    Z_daughter : atomic number of daughter
    A_daughter : mass number of daughter
    A_parent : mass number of parent

    Returns
    -------
    half_life : in seconds
    """
    gamma = gamow_factor(Q_alpha, Z_daughter, A_daughter)
    T = np.exp(-2 * gamma)

    # Assault frequency: v / (2R)
    # v = sqrt(2Q/mu) (classical velocity inside nucleus)
    A_alpha = 4
    mu = (A_alpha * A_daughter) / (A_alpha + A_daughter)  # amu
    mu_mev = mu * AMU_MEV  # MeV/c²

    v = np.sqrt(2 * Q_alpha / mu_mev)  # in units of c
    R = 1.2 * (A_alpha**(1/3) + A_daughter**(1/3))  # fm

    # Convert to frequency: v*c / (2R)
    c_fm_per_s = 2.998e23  # c in fm/s
    nu_assault = v * c_fm_per_s / (2 * R)

    # Half-life
    if T > 0 and nu_assault > 0:
        half_life = np.log(2) / (nu_assault * T)
    else:
        half_life = np.inf

    return half_life


def geiger_nuttall_data() -> list[dict]:
    """Known alpha emitters for Geiger-Nuttall law verification.

    Returns list of dicts with: name, Z_parent, A_parent, Q_alpha (MeV),
    half_life_s (experimental, in seconds).
    """
    return [
        {"name": "²¹²Po", "Z_parent": 84, "A_parent": 212,
         "Q_alpha": 8.954, "half_life_s": 2.99e-7},
        {"name": "²¹⁴Po", "Z_parent": 84, "A_parent": 214,
         "Q_alpha": 7.833, "half_life_s": 1.643e-4},
        {"name": "²¹⁸Po", "Z_parent": 84, "A_parent": 218,
         "Q_alpha": 6.115, "half_life_s": 186.0},
        {"name": "²²⁰Rn", "Z_parent": 86, "A_parent": 220,
         "Q_alpha": 6.405, "half_life_s": 55.6},
        {"name": "²²²Rn", "Z_parent": 86, "A_parent": 222,
         "Q_alpha": 5.590, "half_life_s": 3.3053e5},
        {"name": "²²⁶Ra", "Z_parent": 88, "A_parent": 226,
         "Q_alpha": 4.871, "half_life_s": 5.049e10},
        {"name": "²³²Th", "Z_parent": 90, "A_parent": 232,
         "Q_alpha": 4.082, "half_life_s": 4.434e17},
        {"name": "²³⁵U",  "Z_parent": 92, "A_parent": 235,
         "Q_alpha": 4.679, "half_life_s": 2.221e16},
        {"name": "²³⁸U",  "Z_parent": 92, "A_parent": 238,
         "Q_alpha": 4.270, "half_life_s": 1.410e17},
        {"name": "²⁴⁴Pu", "Z_parent": 94, "A_parent": 244,
         "Q_alpha": 4.666, "half_life_s": 2.525e15},
    ]

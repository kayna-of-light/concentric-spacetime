"""Nuclear shell model on S² × R⁺.

Demonstrates that nuclear magic numbers (2, 8, 20, 28, 50, 82, 126) emerge
from the same S² angular structure as atomic shells, with a different potential
on R⁺ (Woods-Saxon instead of Coulomb) and stronger spin-orbit coupling.

Units: ℏ = 1, nucleon mass m = 1.  Energy in units of ℏω (oscillator).
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


# ---------------------------------------------------------------------------
# Potentials on R⁺
# ---------------------------------------------------------------------------

def harmonic_oscillator_levels(n_max: int = 7) -> list[dict]:
    """Harmonic oscillator shell model (no spin-orbit).

    Energy levels: E(N) = (N + 3/2)ℏω  where N = 2(n-1) + l.
    Each level has degeneracy 2(2l+1) for each (n,l) pair.

    Returns list of dicts with keys: N, n, l, j_values, energy, degeneracy, label.
    """
    levels = []
    for N in range(n_max):
        # For oscillator quantum number N, l = N, N-2, N-4, ... ≥ 0
        for l in range(N, -1, -2):
            n_radial = (N - l) // 2 + 1  # radial quantum number (1-based)
            spectroscopic = "spdfghij"[l] if l < 8 else f"l={l}"
            label = f"{n_radial}{spectroscopic}"
            deg = 2 * (2 * l + 1)  # spin degeneracy
            energy = N + 1.5
            levels.append({
                "N": N,
                "n": n_radial,
                "l": l,
                "j_values": [l + 0.5, l - 0.5] if l > 0 else [0.5],
                "energy": energy,
                "degeneracy": deg,
                "label": label,
            })
    return levels


def harmonic_oscillator_magic() -> list[int]:
    """Return harmonic oscillator magic numbers (no spin-orbit).

    Shell closures at cumulative filling: 2, 8, 20, 40, 70, 112, 168.
    """
    magic = []
    total = 0
    for N in range(7):
        # Degeneracy of oscillator shell N = (N+1)(N+2)
        deg_N = (N + 1) * (N + 2)
        total += deg_N
        magic.append(total)
    return magic


def spin_orbit_split(levels: list[dict], C_so: float = 0.1,
                     C_l2: float = 0.0) -> list[dict]:
    """Apply l² correction and spin-orbit splitting to harmonic oscillator levels.

    The full nuclear shell model uses:
        E(n,l,j) = (N + 3/2)ℏω - C_l2·l(l+1) - C_so·(l·s)

    where l·s = [j(j+1) - l(l+1) - 3/4] / 2.

    C_l2 flattens the potential (lowers high-l orbits within each N shell),
    C_so splits j = l±1/2 states.  Both are needed for nuclear magic numbers.

    Returns a flat list of (n, l, j, energy, degeneracy, label) sorted by energy.
    """
    split_levels = []
    for lev in levels:
        l = lev["l"]
        n = lev["n"]
        E0 = lev["energy"]
        spectroscopic = "spdfghij"[l] if l < 8 else f"l={l}"

        # l² correction: lowers high-l states within each shell
        E_base = E0 - C_l2 * l * (l + 1)

        if l == 0:
            j = 0.5
            deg = 2  # 2j+1 = 2 × 0.5 + 1 = 2
            E_j = E_base  # No spin-orbit for l=0
            label = f"{n}{spectroscopic}_{int(2*j)}/2"
            split_levels.append({
                "N": lev["N"], "n": n, "l": l, "j": j,
                "energy": E_j, "degeneracy": deg, "label": label,
            })
        else:
            for j in [l + 0.5, l - 0.5]:
                # Spin-orbit shift: E_so = -C_so/2 * [j(j+1) - l(l+1) - 3/4]
                shift = -C_so / 2 * (j * (j + 1) - l * (l + 1) - 0.75)
                E_j = E_base + shift
                deg = int(2 * j + 1)
                label = f"{n}{spectroscopic}_{int(2*j)}/2"
                split_levels.append({
                    "N": lev["N"], "n": n, "l": l, "j": j,
                    "energy": E_j, "degeneracy": deg, "label": label,
                })

    # Sort by energy
    split_levels.sort(key=lambda x: (x["energy"], -x["j"]))
    return split_levels


def find_shell_closures(levels: list[dict]) -> list[tuple[int, float]]:
    """Find magic numbers from level filling.

    Returns list of (cumulative_nucleons, energy_gap) at each gap that is
    significantly larger than the average spacing.
    """
    cumulative = []
    total = 0
    for lev in levels:
        total += lev["degeneracy"]
        cumulative.append({"total": total, "energy": lev["energy"], "label": lev["label"]})

    # Find gaps: energy difference to next level
    closures = []
    for i in range(len(cumulative) - 1):
        gap = cumulative[i + 1]["energy"] - cumulative[i]["energy"]
        closures.append((cumulative[i]["total"], gap))

    return closures


def identify_magic_numbers(closures: list[tuple[int, float]],
                           threshold_factor: float = 1.5) -> list[int]:
    """Identify magic numbers from shell closures.

    A magic number occurs where the gap to the next level is significantly
    larger than the median gap.
    """
    if not closures:
        return []

    gaps = [g for _, g in closures]
    median_gap = np.median(gaps)

    magic = []
    for total, gap in closures:
        if gap > median_gap * threshold_factor:
            magic.append(total)

    return magic


# ---------------------------------------------------------------------------
# Woods-Saxon potential (realistic nuclear mean field)
# ---------------------------------------------------------------------------

def woods_saxon(r: np.ndarray, V0: float = 50.0, R0: float = 1.0,
                a_diff: float = 0.67) -> np.ndarray:
    """Woods-Saxon potential: V(r) = -V0 / (1 + exp((r-R0)/a)).

    Parameters
    ----------
    r : radial coordinate
    V0 : well depth in natural units
    R0 : nuclear radius (= r0 × A^{1/3})
    a_diff : surface diffuseness
    """
    return -V0 / (1 + np.exp((r - R0) / a_diff))


def solve_woods_saxon(l: int, V0: float = 50.0, R0: float = 5.0,
                      a_diff: float = 0.67, r_max: float = 15.0,
                      n_grid: int = 2000, n_bound: int = 5) -> list[float]:
    """Find bound state energies for angular momentum l in Woods-Saxon potential.

    Solves the radial Schrödinger equation:
        u'' + [2m(E - V(r)) - l(l+1)/r²] u = 0
    on R⁺ with u(0) = 0, u(r_max) → 0.

    Returns list of bound state energies (negative values).
    """
    dr = r_max / n_grid
    r = np.linspace(dr, r_max, n_grid)
    V = woods_saxon(r, V0, R0, a_diff)

    def count_nodes(E):
        """Count nodes in the wavefunction for energy E via Numerov."""
        # Effective potential including centrifugal term
        k2 = 2.0 * (E - V) - l * (l + 1) / r**2
        # Numerov method
        u = np.zeros(n_grid)
        u[0] = r[0]**(l + 1)  # boundary condition u ~ r^{l+1}
        u[1] = r[1]**(l + 1)

        for i in range(1, n_grid - 1):
            f_prev = 1 - dr**2 / 12 * k2[i - 1]
            f_curr = 1 - dr**2 / 12 * k2[i]
            f_next = 1 - dr**2 / 12 * k2[i + 1]
            u[i + 1] = (2 * f_curr * u[i] - f_prev * u[i - 1]) / f_next

        # Count sign changes (nodes)
        nodes = 0
        for i in range(n_grid - 1):
            if u[i] * u[i + 1] < 0:
                nodes += 1
        return nodes, u[-1]

    # Search for bound states by scanning energy
    energies = []
    E_min = -V0 * 1.1
    E_max = -0.01
    n_scan = 500
    E_scan = np.linspace(E_min, E_max, n_scan)

    # Find energies where node count changes
    prev_nodes = None
    for E in E_scan:
        try:
            nodes, u_end = count_nodes(E)
            if prev_nodes is not None and nodes != prev_nodes:
                # Refine by bisection on the boundary value
                E_lo, E_hi = E_scan[max(0, np.searchsorted(E_scan, E) - 1)], E
                try:
                    def boundary_val(e):
                        _, u = count_nodes(e)
                        return u
                    E_bound = brentq(boundary_val, E_lo, E_hi, xtol=1e-8)
                    energies.append(E_bound)
                    if len(energies) >= n_bound:
                        break
                except (ValueError, RuntimeError):
                    pass
            prev_nodes = nodes
        except (OverflowError, FloatingPointError):
            continue

    return sorted(energies)


def nuclear_level_scheme(V0: float = 50.0, A: int = 208,
                         r0: float = 1.25, a_diff: float = 0.67,
                         C_so: float = 0.0, l_max: int = 7,
                         n_bound: int = 4) -> list[dict]:
    """Compute nuclear single-particle levels for a Woods-Saxon potential.

    Returns levels sorted by energy, with spin-orbit splitting if C_so > 0.
    """
    R0 = r0 * A**(1.0 / 3)

    all_levels = []
    for l in range(l_max + 1):
        energies = solve_woods_saxon(l, V0, R0, a_diff, n_bound=n_bound)
        spectroscopic = "spdfghij"[l] if l < 8 else f"l={l}"

        for i, E in enumerate(energies):
            n_radial = i + 1
            if C_so > 0 and l > 0:
                for j in [l + 0.5, l - 0.5]:
                    shift = -C_so / 2 * (j * (j + 1) - l * (l + 1) - 0.75)
                    E_j = E + shift
                    deg = int(2 * j + 1)
                    label = f"{n_radial}{spectroscopic}_{int(2*j)}/2"
                    all_levels.append({
                        "n": n_radial, "l": l, "j": j,
                        "energy": E_j, "degeneracy": deg, "label": label,
                    })
            else:
                j_vals = [l + 0.5, l - 0.5] if l > 0 else [0.5]
                total_deg = sum(int(2*j+1) for j in j_vals)
                label = f"{n_radial}{spectroscopic}"
                all_levels.append({
                    "n": n_radial, "l": l, "j": None,
                    "energy": E, "degeneracy": total_deg, "label": label,
                })

    all_levels.sort(key=lambda x: x["energy"])
    return all_levels


# ---------------------------------------------------------------------------
# Standard (textbook) nuclear magic numbers
# ---------------------------------------------------------------------------

KNOWN_MAGIC_NUMBERS = [2, 8, 20, 28, 50, 82, 126]
HO_MAGIC_NUMBERS = [2, 8, 20, 40, 70, 112, 168]

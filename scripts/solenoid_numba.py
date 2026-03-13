"""
Numba-Accelerated Solenoid Dynamics (Tier 1).

Drop-in replacement for the integration pipeline in solenoid_system.py,
using Numba JIT compilation for the ODE RHS and ProcessPoolExecutor
to bypass the Python GIL.

Performance: ~5-15x faster than scipy + ThreadPoolExecutor on multi-core CPU.

Usage:
    from solenoid_numba import integrate_all_branches_numba

    results = integrate_all_branches_numba(branches, t_eval, T_max)

    # Same dict format — compatible with accumulate_sectors / cp_pair_ratios
    sector_rms = SolenoidSystem.accumulate_sectors(results, ...)

Or via the backend parameter on SolenoidSystem:
    sys0 = SolenoidSystem()
    results = sys0.integrate_all_branches(
        branches, t_eval, T_max, backend='numba'
    )

Notes:
    - First call triggers Numba JIT compilation (~2-5s, cached to disk).
    - Uses ProcessPoolExecutor (true OS processes, no GIL contention).
    - On Windows, process spawning adds ~5-10s startup overhead.
    - Requires: numba (already in concentric env).
"""

import time
import numpy as np
import numba
from scipy.integrate import solve_ivp
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple

# Default constants (mirror solenoid_algebra.py)
_PRIMES = np.array([2, 3, 5, 7], dtype=np.float64)
_P = 210
_RHO = 1.0 / np.sqrt(_P)
_OMEGA = 2.0 * np.pi


# ── Numba-JIT'd ODE RHS ─────────────────────────────────────────────

@numba.njit(cache=True)
def _cascade_ode_numba(t, R, primes, omega, epsilon, kappa):
    """
    Cascade ODE RHS, compiled to native machine code by Numba.

    Eliminates Python interpreter overhead for the millions of
    RHS evaluations per branch integration.
    """
    n = len(primes)

    # Reconstruct theta via forward substitution
    th = np.empty(n + 1)
    th[0] = omega * t
    for k in range(n):
        th[k + 1] = (R[k] + th[k]) / primes[k]

    # Compute dR/dt
    dR = np.empty(n)
    dR[0] = epsilon * np.sin(th[0]) - kappa * R[0]
    for k in range(1, n):
        dR[k] = (
            epsilon * np.sin(th[k])
            - epsilon * np.sin(th[k - 1]) / primes[k - 1]
            + kappa * R[k - 1] / primes[k - 1]
            - kappa * R[k]
        )
    return dR


# ── Worker function (must be module-level for pickling) ──────────────

def _integrate_one(args):
    """
    Integrate a single branch. Module-level for ProcessPoolExecutor.

    Each worker process gets its own Python interpreter (no GIL sharing).
    The Numba-JIT'd ODE function is loaded from cache in each process.
    """
    branch, t_eval, T_max, primes, omega, epsilon, kappa, rtol, atol = args

    R0 = np.array([2.0 * np.pi * j for j in branch], dtype=np.float64)
    primes_arr = np.asarray(primes, dtype=np.float64)

    def ode(t, R):
        return _cascade_ode_numba(t, R, primes_arr, omega, epsilon, kappa)

    sol = solve_ivp(
        ode,
        [0.0, T_max + 1.0],
        R0,
        method="DOP853",
        t_eval=t_eval,
        rtol=rtol,
        atol=atol,
    )
    if sol.status != 0:
        raise RuntimeError(f"Branch {branch} FAILED: {sol.message}")

    return branch, sol.y.T  # (n_eval, n_levels)


# ── Main integration function ────────────────────────────────────────

def integrate_all_branches_numba(
    branches: List[Tuple[int, ...]],
    t_eval: np.ndarray,
    T_max: float,
    primes: Optional[List[int]] = None,
    omega: float = _OMEGA,
    epsilon: float = _RHO,
    kappa: float = _RHO,
    rtol: float = 1e-12,
    atol: float = 1e-14,
    max_workers: int = 8,
    verbose: bool = True,
) -> Dict[Tuple[int, ...], np.ndarray]:
    """
    Integrate all branches using Numba JIT + ProcessPoolExecutor.

    Parameters
    ----------
    branches : list of tuples
        Branch indices to integrate.
    t_eval : ndarray
        Times at which to record output.
    T_max : float
        End time.
    primes : list of int, optional
        Covering primes. Default: [2, 3, 5, 7].
    omega, epsilon, kappa : float
        ODE parameters.
    rtol, atol : float
        Integration tolerances.
    max_workers : int
        Number of parallel worker processes.
    verbose : bool
        Print timing information.

    Returns
    -------
    results : dict[tuple, ndarray]
        branch -> R_vals (n_eval, n_levels). Compatible with
        SolenoidSystem.accumulate_sectors().
    """
    if primes is None:
        primes = list([2, 3, 5, 7])
    primes_arr = np.array(primes, dtype=np.float64)

    # Pre-warm Numba JIT (compiles on first call, cached thereafter)
    _warmup_numba(primes_arr, omega, epsilon, kappa)

    # Build task list
    tasks = [
        (b, t_eval, T_max, primes_arr, omega, epsilon, kappa, rtol, atol)
        for b in branches
    ]

    t0 = time.perf_counter()
    results = {}

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_integrate_one, task): task[0] for task in tasks}
        done = 0
        for f in as_completed(futures):
            branch, R_vals = f.result()
            results[branch] = R_vals
            done += 1
            if verbose and done % 50 == 0:
                print(f"  Numba: {done}/{len(branches)} ({time.perf_counter()-t0:.1f}s)")

    elapsed = time.perf_counter() - t0
    if verbose:
        print(
            f"  Numba [{max_workers} workers]: {len(branches)} branches, "
            f"{len(t_eval)} eval pts, T={T_max} — {elapsed:.2f}s"
        )

    return results


def _warmup_numba(primes, omega, epsilon, kappa):
    """Trigger Numba JIT compilation (cached to disk after first run)."""
    R_test = np.zeros(len(primes), dtype=np.float64)
    _cascade_ode_numba(0.0, R_test, primes, omega, epsilon, kappa)

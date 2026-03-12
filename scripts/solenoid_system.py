"""
The (p1, p2, ..., pn)-Solenoid Dynamical System.

The correct topology for the four-prime concentric system.
Established in NB25/NB26: the flat torus T^4 makes primes invisible;
the solenoid makes them irreplaceable.

The solenoid is the inverse limit of covering maps:
    S^1 <--p1-- S^1 <--p2-- S^1 <--p3-- S^1 <--p4-- S^1

Each covering map wraps p_k times: p_k * theta_k = theta_{k-1} (mod 2pi).
The inverse limit has a Cantor-set fiber over each point of S^1.

Key properties:
  - Poincare section has exactly product(primes) = 210 discrete points
  - Coprimality of primes guarantees maximal structure
  - Composite alignment grid: returns at primorials (2, 6, 30, 210)
  - Perturbation (epsilon > 0) dissolves structure toward flat T^4
  - Linear restoring force (kappa > 0) drives covering residuals toward zero
  - Spectrum is sparse (covering constraints = quantization mechanism)

Two formulations:
  SolenoidSystem  — Original theta-space ODE (5D: theta_0..theta_4)
  CascadeSystem   — Reduced R-space ODE (4D: R_1..R_4, covering residuals)
                    Established in NB79-81. Equivalent to SolenoidSystem
                    within 0.002% (NB80), but 4D instead of 5D.

Frequencies:
  Level 0 (base):   omega
  Level k:          omega / P_k     where P_k = p_1 * p_2 * ... * p_k (primorial)

For primes [2, 3, 5, 7]:
  Primorials: [1, 2, 6, 30, 210]
  Frequencies: [omega, omega/2, omega/6, omega/30, omega/210]
"""

import numpy as np
from math import gcd
from scipy.integrate import solve_ivp
from typing import Dict, List, Optional, Tuple


class SolenoidSystem:
    """
    Dynamics on the (p1, p2, ..., pn)-solenoid.

    The solenoid is defined by n covering maps on (n+1) circles:
        p_k * theta_k = theta_{k-1} (mod 2pi),  k = 1, ..., n

    Exact solenoid translation:
        d(theta_0)/dt = omega
        d(theta_k)/dt = omega / P_k

    Perturbation (breaks covering constraint):
        d(theta_k)/dt = omega / P_k + epsilon * sin(theta_{k-1}) / p_k

    Restoring force (NB67+, drives residuals toward zero):
        d(theta_k)/dt = omega / P_k + epsilon * sin(theta_{k-1}) / p_k
                        - kappa * R_k / p_k
        where R_k = p_k * theta_k - theta_{k-1} (covering residual)

    Parameters
    ----------
    primes : list of int
        Covering degrees [2, 3, 5, 7].
    omega : float
        Base frequency (on theta_0).
    epsilon : float
        Perturbation strength. 0 = exact solenoid.
    kappa : float
        Linear restoring force strength. 0 = no restoring.
        Typically set equal to epsilon (= 1/sqrt(210)).
    """

    def __init__(self, primes, omega=2 * np.pi, epsilon=0.0, kappa=0.0):
        self.primes = list(primes)
        self.n = len(primes)
        self.n_angles = self.n + 1  # base circle + n covering levels
        self.omega = omega
        self.epsilon = epsilon
        self.kappa = kappa

        # Primorial products: P_k = p_1 * p_2 * ... * p_k
        self.primorials = [1]
        P = 1
        for p in self.primes:
            P *= p
            self.primorials.append(P)
        # For [2,3,5,7]: primorials = [1, 2, 6, 30, 210]

        # Exact solenoid frequencies: omega / P_k
        self.solenoid_freqs = [omega / P for P in self.primorials]

        # Periods: 2*pi / freq = 2*pi * P_k / omega
        self.periods = [2 * np.pi * P / omega for P in self.primorials]

        # Full product (total alignment period in returns)
        self.full_product = self.primorials[-1]

    def initial_condition(self, phi0=0.0, branch=None):
        """
        Generate initial condition on the solenoid manifold.

        Parameters
        ----------
        phi0 : float
            Starting angle on the base circle.
        branch : tuple of int, optional
            (j_1, ..., j_n) where 0 <= j_k < p_k.
            Selects which solenoid leaf.
            Default: (0, 0, ..., 0).
        """
        if branch is None:
            branch = tuple(0 for _ in self.primes)

        theta = np.zeros(self.n_angles)
        theta[0] = phi0

        for k in range(self.n):
            p = self.primes[k]
            j = branch[k]
            # Covering: p_k * theta_k = theta_{k-1} (mod 2pi)
            # So theta_k = (theta_{k-1} + 2pi*j) / p_k
            theta[k + 1] = (theta[k] + 2 * np.pi * j) / p

        return theta

    def ode(self, t, theta):
        """RHS of the solenoid ODE with optional restoring force."""
        dtheta = np.zeros(self.n_angles)
        dtheta[0] = self.omega

        for k in range(1, self.n_angles):
            p = self.primes[k - 1]
            dtheta[k] = self.solenoid_freqs[k]
            if self.epsilon > 0:
                dtheta[k] += self.epsilon * np.sin(theta[k - 1]) / p
            if self.kappa > 0:
                R_k = p * theta[k] - theta[k - 1]
                dtheta[k] -= self.kappa * R_k / p

        return dtheta

    def covering_residuals(self, theta):
        """
        Compute the covering constraint residuals.

        R_k = p_k * theta_k - theta_{k-1} (mod 2pi), mapped to [-pi, pi].
        Should be ~0 on exact solenoid.
        """
        residuals = np.zeros(self.n)
        for k in range(self.n):
            p = self.primes[k]
            R = (p * theta[k + 1] - theta[k]) % (2 * np.pi)
            if R > np.pi:
                R -= 2 * np.pi
            residuals[k] = R
        return residuals

    def integrate(
        self,
        t_span,
        n_points=1_000_000,
        theta0=None,
        branch=None,
        rtol=1e-10,
        atol=1e-12,
    ):
        """
        Integrate the solenoid ODE.

        Returns dict with keys 't', 'theta', 'theta_mod'.
        """
        if theta0 is None:
            theta0 = self.initial_condition(branch=branch)
        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        sol = solve_ivp(
            self.ode,
            t_span,
            theta0,
            t_eval=t_eval,
            method="RK45",
            rtol=rtol,
            atol=atol,
        )
        return {
            "t": sol.t,
            "theta": sol.y,
            "theta_mod": np.mod(sol.y, 2 * np.pi),
        }

    def poincare_section(
        self, t_span=(0, 5000), n_points=1_000_000, branch=None
    ):
        """
        Record states of all angles when theta_0 crosses 0.

        Returns array of shape (n_angles-1, n_crossings).
        """
        result = self.integrate(t_span, n_points, branch=branch)
        th0 = result["theta_mod"][0, :]

        # Crossings: theta_0 wraps from ~2pi to ~0
        crossings = np.where(np.diff(th0) < -np.pi)[0]

        # Record NON-base angles at crossing times
        sections = result["theta_mod"][1:, crossings]
        return sections

    def solenoid_eigenvalue(self, n):
        """
        Eigenvalue of mode n on the solenoid.

        On the solenoid leaf, the single free parameter is the return number n.
        At level k, the effective mode number is n / P_k.
        lambda_n = sum_{k=0}^{N} (n / P_k)^2
        """
        return sum((n / P) ** 2 for P in self.primorials)

    def spectrum(self, n_modes=50):
        """Return the first n_modes solenoid eigenvalues."""
        return [self.solenoid_eigenvalue(n) for n in range(1, n_modes + 1)]

    def alignment_structure(self, max_return=None):
        """
        Compute the alignment structure of Poincare returns.

        At return n, theta_k = 2*pi*n / P_k (mod 2pi).
        A level aligns (returns to 0) when n is a multiple of P_k.

        Returns list of (n, aligned_levels) tuples for notable returns.
        """
        if max_return is None:
            max_return = self.full_product
        results = []
        for n in range(1, max_return + 1):
            aligned = []
            for k in range(self.n):
                P = self.primorials[k + 1]
                if n % P == 0:
                    aligned.append(k + 1)
            if aligned:
                results.append((n, aligned))
        return results

    def integrate_and_section(
        self,
        t_span=(0, 5000),
        theta0=None,
        branch=None,
        n_factor=200,
        rtol=1e-12,
        atol=1e-14,
    ):
        """
        Integrate and extract Poincare sections with covering residuals.

        Returns
        -------
        sections : ndarray, shape (n_angles, n_crossings)
            Full theta state at each base-circle crossing.
        residuals : ndarray, shape (n, n_crossings)
            Covering residuals R_k at each crossing, mapped to [-pi, pi].
        n_crossings : int
            Number of crossings detected.
        """
        T = t_span[1] - t_span[0]
        n_pts = max(500_000, int(T * n_factor))
        if theta0 is None:
            theta0 = self.initial_condition(branch=branch)
        sol = solve_ivp(
            self.ode,
            t_span,
            theta0,
            t_eval=np.linspace(t_span[0], t_span[1], n_pts),
            method="RK45",
            rtol=rtol,
            atol=atol,
        )
        th0_mod = np.mod(sol.y[0], 2 * np.pi)
        crossings = np.where(np.diff(th0_mod) < -np.pi)[0]
        sections = sol.y[:, crossings]
        n_cross = sections.shape[1]
        residuals = np.zeros((self.n, n_cross))
        for k in range(self.n):
            p = self.primes[k]
            raw = p * sections[k + 1] - sections[k]
            R = np.mod(raw, 2 * np.pi)
            R[R > np.pi] -= 2 * np.pi
            residuals[k] = R
        return sections, residuals, n_cross

    def __repr__(self):
        return (
            f"SolenoidSystem(primes={self.primes}, omega={self.omega:.4f}, "
            f"epsilon={self.epsilon}, kappa={self.kappa}, "
            f"primorials={self.primorials})"
        )


class CascadeSystem:
    """
    The 4D Primorial Cascade ODE on covering residuals R_k.

    Established in NB79-81. This is the reduced formulation of the
    solenoid dynamics, operating in R-space (covering residuals) rather
    than theta-space. Equivalent to SolenoidSystem within 0.002% (NB80),
    but 4D instead of 5D — theta_0 is eliminated analytically.

    The cascade ODE:
        dR_k/dt + kappa*R_k = f_k(t; lower levels)

    where f_k encodes the nonlinear sin coupling between levels.
    Initial conditions R_k(0) = 2*pi*j_k select the solenoid branch.

    Parameters
    ----------
    primes : list of int
        Covering degrees [2, 3, 5, 7].
    omega : float
        Base frequency. Default: 2*pi.
    epsilon : float
        Coupling strength. Default: 1/sqrt(210).
    kappa : float
        Restoring force. Default: 1/sqrt(210).
    """

    def __init__(
        self,
        primes: Optional[List[int]] = None,
        omega: float = 2 * np.pi,
        epsilon: Optional[float] = None,
        kappa: Optional[float] = None,
    ):
        self.primes = list(primes) if primes is not None else [2, 3, 5, 7]
        self.n = len(self.primes)
        self.omega = omega

        # Default coupling: 1/sqrt(product of primes)
        from functools import reduce
        self.P = reduce(lambda a, b: a * b, self.primes)
        rho = 1.0 / np.sqrt(self.P)
        self.epsilon = epsilon if epsilon is not None else rho
        self.kappa = kappa if kappa is not None else rho

    def cascade_rhs(self, t: float, R: np.ndarray) -> np.ndarray:
        """
        RHS of the 4D cascade ODE.

        Reconstructs theta from R and base angle, then computes
        the coupled residual dynamics.
        """
        # Reconstruct theta from R: theta_0 = omega*t, then
        # theta_{k+1} = (R_k + theta_k) / p_k
        th = np.empty(self.n + 1)
        th[0] = self.omega * t
        for k in range(self.n):
            th[k + 1] = (R[k] + th[k]) / self.primes[k]

        dR = np.empty(self.n)
        dR[0] = self.epsilon * np.sin(th[0]) - self.kappa * R[0]
        for k in range(1, self.n):
            dR[k] = (
                self.epsilon * np.sin(th[k])
                - self.epsilon * np.sin(th[k - 1]) / self.primes[k - 1]
                + self.kappa * R[k - 1] / self.primes[k - 1]
                - self.kappa * R[k]
            )
        return dR

    def initial_condition(self, branch: Tuple[int, ...]) -> np.ndarray:
        """
        Initial R-vector for a given branch.

        R_k(0) = 2*pi*j_k where j_k is the k-th branch index.
        """
        return np.array([2 * np.pi * j for j in branch], dtype=float)

    def integrate_branch(
        self,
        branch: Tuple[int, ...],
        t_eval: np.ndarray,
        T_max: float,
        rtol: float = 1e-12,
        atol: float = 1e-14,
    ) -> np.ndarray:
        """
        Integrate a single branch of the cascade ODE.

        Parameters
        ----------
        branch : tuple of int
            (j_1, ..., j_n) branch indices.
        t_eval : ndarray
            Times at which to evaluate (typically coprime crossing times).
        T_max : float
            End time of integration.
        rtol, atol : float
            Solver tolerances.

        Returns
        -------
        R_vals : ndarray, shape (len(t_eval), n)
            Covering residuals at each evaluation time.
        """
        R0 = self.initial_condition(branch)
        sol = solve_ivp(
            self.cascade_rhs,
            [0.0, T_max + 1.0],
            R0,
            method="DOP853",
            t_eval=t_eval,
            rtol=rtol,
            atol=atol,
        )
        if sol.status != 0:
            raise RuntimeError(f"Branch {branch} FAILED: {sol.message}")
        return sol.y.T  # (n_eval, n_levels)

    def integrate_all_branches(
        self,
        branches: List[Tuple[int, ...]],
        t_eval: np.ndarray,
        T_max: float,
        max_workers: int = 8,
        rtol: float = 1e-12,
        atol: float = 1e-14,
        progress_interval: int = 50,
    ) -> Dict[Tuple[int, ...], np.ndarray]:
        """
        Integrate multiple branches in parallel.

        Parameters
        ----------
        branches : list of tuples
            Branch indices to integrate.
        t_eval : ndarray
            Evaluation times.
        T_max : float
            End time.
        max_workers : int
            Number of parallel workers.
        progress_interval : int
            Print progress every N branches.

        Returns
        -------
        results : dict
            branch tuple -> R_vals array (n_eval, n_levels)
        """
        import time
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def _integrate_one(branch):
            return branch, self.integrate_branch(branch, t_eval, T_max, rtol, atol)

        t0 = time.time()
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(_integrate_one, b): b for b in branches}
            done = 0
            for f in as_completed(futures):
                branch, R_vals = f.result()
                results[branch] = R_vals
                done += 1
                if progress_interval > 0 and done % progress_interval == 0:
                    print(f"  {done}/{len(branches)} ({time.time()-t0:.1f}s)")

        return results

    @staticmethod
    def accumulate_sectors(
        results: Dict[Tuple[int, ...], np.ndarray],
        coprime_cis: np.ndarray,
        ci_a3: np.ndarray,
        ci_a5: np.ndarray,
        ci_a7: np.ndarray,
        n_levels: int = 4,
    ) -> np.ndarray:
        """
        Accumulate wrapped R^2 into CRT sectors and compute RMS.

        Parameters
        ----------
        results : dict
            branch -> R_vals array (n_coprime, n_levels)
        coprime_cis : ndarray
            Coprime crossing indices.
        ci_a3, ci_a5, ci_a7 : ndarray
            CRT sector labels for each coprime crossing.
        n_levels : int
            Number of covering levels (default 4).

        Returns
        -------
        sector_rms : ndarray, shape (4, 2, 6, n_levels)
            RMS residual per (a5, a3, a7*, level) sector.
        """
        branches = list(results.keys())
        n_br = len(branches)

        # Stack and wrap to [-pi, pi]
        all_R = np.stack([results[b] for b in branches])  # (n_br, n_coprime, n_levels)
        all_R_w = np.mod(all_R, 2 * np.pi)
        all_R_w[all_R_w > np.pi] -= 2 * np.pi

        # Sum R^2 over branches
        R_sq_sum = (all_R_w ** 2).sum(axis=0)  # (n_coprime, n_levels)

        sector_sq = np.zeros((4, 2, 6, n_levels))
        sector_cnt = np.zeros((4, 2, 6), dtype=int)

        for idx in range(len(coprime_cis)):
            a5, a3, a7 = ci_a5[idx], ci_a3[idx], ci_a7[idx]
            sector_sq[a5, a3, a7] += R_sq_sum[idx]
            sector_cnt[a5, a3, a7] += n_br

        sector_rms = np.zeros((4, 2, 6, n_levels))
        for a5 in range(4):
            for a3 in range(2):
                for a7 in range(6):
                    cnt = sector_cnt[a5, a3, a7]
                    if cnt > 0:
                        sector_rms[a5, a3, a7] = np.sqrt(
                            sector_sq[a5, a3, a7] / cnt
                        )
        return sector_rms

    @staticmethod
    def cp_pair_ratios(
        sector_rms: np.ndarray,
        cp_pairs: Optional[Dict[str, tuple]] = None,
    ) -> Dict[str, List[float]]:
        """
        Compute CP-pair ratios from sector RMS values.

        Parameters
        ----------
        sector_rms : ndarray, shape (4, 2, 6, n_levels)
            Output of accumulate_sectors.
        cp_pairs : dict, optional
            Channel definitions. Default: QUARK=(1,4,2), LEPTON=(0,1,5).

        Returns
        -------
        ratios : dict
            channel name -> [R_1, R_2, R_3, R_4] ratio values
        """
        if cp_pairs is None:
            from solenoid_algebra import CP_PAIRS
            cp_pairs = CP_PAIRS

        n_levels = sector_rms.shape[3]
        ratios = {}
        for pname, (a3, a7_g1, a7_g2) in cp_pairs.items():
            r = []
            for lev in range(n_levels):
                v1 = sector_rms[0, a3, a7_g1, lev]
                v2 = sector_rms[0, a3, a7_g2, lev]
                r.append(v1 / v2 if v2 > 0 else 0.0)
            ratios[pname] = r
        return ratios

    def __repr__(self):
        return (
            f"CascadeSystem(primes={self.primes}, omega={self.omega:.4f}, "
            f"epsilon={self.epsilon}, kappa={self.kappa})"
        )

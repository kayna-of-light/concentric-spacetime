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

Frequencies:
  Level 0 (base):   omega
  Level k:          omega / P_k     where P_k = p_1 * p_2 * ... * p_k (primorial)

For primes [2, 3, 5, 7]:
  Primorials: [1, 2, 6, 30, 210]
  Frequencies: [omega, omega/2, omega/6, omega/30, omega/210]
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Optional


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

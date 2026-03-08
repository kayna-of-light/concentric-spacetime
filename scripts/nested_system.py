"""
Hierarchically Coupled Concentric Dynamical System.

The complete mathematical formalization of the four-prime coordinate system
as nested concentric orbits with energy-constrained dynamics.

Each outer orbit is constituted by the inner orbits it contains:
  7 contains 5 contains 3 contains 2

The energy (influx from center) determines how many orbits are active.
The coupling is one-directional upward: inner content modulates outer dynamics.
The metric weight 1/p means inner orbits carry more significance per unit of
angular change.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Optional


# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────
PRIMES = np.array([2, 3, 5, 7])
N_ORBITS = len(PRIMES)
OMEGA_BASE = 2 * np.pi * np.sqrt(PRIMES)  # incommensurate base frequencies
METRIC_WEIGHTS = (1.0 / PRIMES) / (1.0 / PRIMES).sum()  # normalized 1/p weights


class ConcentricSystem:
    """
    A hierarchically coupled dynamical system on nested concentric orbits.

    State: four angular positions θ_p ∈ [0, 2π) for p ∈ {2, 3, 5, 7}.

    Dynamics:
        dθ₂/dt = ω₂ · a₂
        dθ₃/dt = ω₃ · a₃  +  α · (1/2) · sin(θ₂)
        dθ₅/dt = ω₅ · a₅  +  α · [(1/2)·sin(θ₂) + (1/3)·sin(θ₃)]
        dθ₇/dt = ω₇ · a₇  +  α · [(1/2)·sin(θ₂) + (1/3)·sin(θ₃) + (1/5)·sin(θ₅)]

    where a_p(E) is the amplitude for orbit p given total energy E:
        - Each orbit has an activation energy threshold E_p = ω_p² / (2p)
        - Orbits activate in order: 2 → 3 → 5 → 7 as energy increases
        - Active orbits share remaining energy proportionally to 1/p

    Parameters
    ----------
    energy : float
        Total energy flowing into the system (influx from center).
        Controls how many orbits are active and at what amplitude.
    alpha : float
        Coupling strength. How strongly inner content modulates outer dynamics.
        α = 0 recovers the independent (Cartesian) model from NB01-08.
    """

    def __init__(self, energy: float = 1.0, alpha: float = 0.5):
        self.primes = PRIMES.copy()
        self.n_orbits = N_ORBITS
        self.omega = OMEGA_BASE.copy()
        self.weights = METRIC_WEIGHTS.copy()
        self.energy = energy
        self.alpha = alpha

        # Compute orbit activation thresholds and amplitudes
        self._compute_amplitudes()

    def _compute_amplitudes(self):
        """
        Compute amplitude for each orbit based on available energy.

        Activation thresholds: E_p = ω_p / (2p)
        This means inner orbits (small p, small ω) activate first.
        The threshold is proportional to the orbit's "minimum kinetic energy"
        weighted by its metric significance.

        As energy increases beyond all thresholds, amplitudes grow
        proportionally to 1/p — inner orbits carry more energy per unit.
        """
        # Activation thresholds — inner orbits first
        # E_p = ω_p / (2 * p) ensures ordering: E_2 < E_3 < E_5 < E_7
        self.thresholds = self.omega / (2 * self.primes)

        # Cumulative thresholds — energy needed to activate up to orbit k
        self.cumulative_thresholds = np.cumsum(self.thresholds)

        # Determine which orbits are active
        self.active = np.zeros(self.n_orbits, dtype=bool)
        self.amplitudes = np.zeros(self.n_orbits)

        remaining = self.energy
        for i in range(self.n_orbits):
            if remaining >= self.thresholds[i]:
                self.active[i] = True
                remaining -= self.thresholds[i]
            else:
                break

        # Distribute remaining energy to active orbits proportional to 1/p
        if self.active.any():
            active_weights = (1.0 / self.primes[self.active])
            active_weights /= active_weights.sum()
            # Amplitude = sqrt(2 * E_share * p) to convert back from KE
            energy_shares = remaining * active_weights
            for i, idx in enumerate(np.where(self.active)[0]):
                # Base amplitude of 1.0 + boost from excess energy
                self.amplitudes[idx] = 1.0 + np.sqrt(
                    2 * energy_shares[i] * self.primes[idx]
                )

    def ode(self, t: float, theta: np.ndarray) -> np.ndarray:
        """
        Right-hand side of the coupled ODE system.

        Parameters
        ----------
        t : float
            Current time.
        theta : ndarray of shape (4,)
            Angular positions [θ₂, θ₃, θ₅, θ₇].

        Returns
        -------
        dtheta : ndarray of shape (4,)
            Angular velocities [dθ₂/dt, dθ₃/dt, dθ₅/dt, dθ₇/dt].
        """
        dtheta = np.zeros(self.n_orbits)

        # Base frequencies modulated by amplitude
        for i in range(self.n_orbits):
            dtheta[i] = self.omega[i] * self.amplitudes[i]

        # Hierarchical coupling: inner → outer (one-way upward)
        if self.alpha > 0 and self.active.sum() > 1:
            # Orbit 3 (index 1) coupled to orbit 2 (index 0)
            if self.active[1]:
                dtheta[1] += self.alpha * (1.0 / 2) * np.sin(theta[0])

            # Orbit 5 (index 2) coupled to orbits 2, 3
            if self.active[2]:
                dtheta[2] += self.alpha * (
                    (1.0 / 2) * np.sin(theta[0]) +
                    (1.0 / 3) * np.sin(theta[1])
                )

            # Orbit 7 (index 3) coupled to orbits 2, 3, 5
            if self.active[3]:
                dtheta[3] += self.alpha * (
                    (1.0 / 2) * np.sin(theta[0]) +
                    (1.0 / 3) * np.sin(theta[1]) +
                    (1.0 / 5) * np.sin(theta[2])
                )

        return dtheta

    def integrate(
        self,
        t_span: tuple[float, float],
        n_points: int = 10000,
        theta0: Optional[np.ndarray] = None,
    ) -> dict:
        """
        Integrate the coupled system.

        Parameters
        ----------
        t_span : (t_start, t_end)
        n_points : number of output time points
        theta0 : initial angular positions (default: all zeros)

        Returns
        -------
        dict with keys:
            't' : time array
            'theta' : angular positions, shape (4, n_points)
            'theta_mod' : positions mod 2π
            'active' : boolean array of active orbits
        """
        if theta0 is None:
            theta0 = np.zeros(self.n_orbits)

        t_eval = np.linspace(t_span[0], t_span[1], n_points)

        sol = solve_ivp(
            self.ode,
            t_span,
            theta0,
            t_eval=t_eval,
            method='RK45',
            rtol=1e-10,
            atol=1e-12,
        )

        theta_mod = np.mod(sol.y, 2 * np.pi)

        return {
            't': sol.t,
            'theta': sol.y,
            'theta_mod': theta_mod,
            'active': self.active.copy(),
        }

    def state_distance(self, theta_a: np.ndarray, theta_b: np.ndarray) -> float:
        """
        Geodesic distance on the weighted torus between two states.

        d_s = sqrt(Σ w_p · Δθ_p²)

        where w_p = (1/p) / Σ(1/p) and Δθ_p is the minimum angular difference.
        """
        dtheta = np.abs(theta_a - theta_b)
        dtheta = np.minimum(dtheta, 2 * np.pi - dtheta)
        return np.sqrt(np.sum(self.weights * dtheta**2))

    @staticmethod
    def angular_diff(a: float, b: float) -> float:
        """Minimum angular difference on the circle."""
        d = abs(a - b) % (2 * np.pi)
        return min(d, 2 * np.pi - d)

    def info(self) -> str:
        """Summary string."""
        lines = [
            f"ConcentricSystem(E={self.energy:.3f}, α={self.alpha:.3f})",
            f"  Active orbits: {self.primes[self.active]}",
            f"  Amplitudes:    {np.round(self.amplitudes, 4)}",
            f"  Thresholds:    {np.round(self.thresholds, 4)}",
            f"  Cumulative:    {np.round(self.cumulative_thresholds, 4)}",
        ]
        return '\n'.join(lines)


# ──────────────────────────────────────────────────────────────
# Recurrence analysis
# ──────────────────────────────────────────────────────────────

def find_near_returns(
    theta_mod: np.ndarray,
    t: np.ndarray,
    orbit_idx: int,
    tolerance: float = 0.1,
) -> list[dict]:
    """
    Find times when a specific orbit returns near its initial angular position.

    Parameters
    ----------
    theta_mod : shape (4, n_points) — angular positions mod 2π
    t : time array
    orbit_idx : which orbit (0=p2, 1=p3, 2=p5, 3=p7)
    tolerance : angular tolerance in radians for "near return"

    Returns
    -------
    List of dicts with 't', 'theta_target', 'inner_state', 'inner_variance'
    """
    theta_target = theta_mod[orbit_idx, 0]  # initial position of this orbit
    returns = []

    for i in range(1, theta_mod.shape[1]):
        diff = abs(theta_mod[orbit_idx, i] - theta_target)
        diff = min(diff, 2 * np.pi - diff)
        if diff < tolerance:
            # Record the inner state at this return
            inner_state = theta_mod[:orbit_idx, i]  # all orbits inside this one
            returns.append({
                't': t[i],
                'theta_target': theta_mod[orbit_idx, i],
                'inner_state': inner_state.copy(),
            })

    # Compute variance of inner states across returns
    if returns and orbit_idx > 0:
        inner_matrix = np.array([r['inner_state'] for r in returns])
        for r in returns:
            r['inner_variance'] = np.var(inner_matrix, axis=0).sum()

    return returns


def recurrence_times(
    theta_mod: np.ndarray,
    t: np.ndarray,
    tolerance: float = 0.05,
) -> list[dict]:
    """
    Compute recurrence statistics at each nesting level.

    For each level k, find times when ALL orbits up to k simultaneously
    return near their initial positions.

    Returns list of dicts with keys: primes, first_recurrence, count.
    """
    results = []
    initial = theta_mod[:, 0]

    for level in range(1, len(PRIMES) + 1):
        # All orbits 0..level-1 must be near initial
        near_mask = np.ones(theta_mod.shape[1], dtype=bool)
        for k in range(level):
            diff = np.abs(theta_mod[k, :] - initial[k])
            diff = np.minimum(diff, 2 * np.pi - diff)
            near_mask &= (diff < tolerance)

        near_mask[0] = False  # exclude t=0 itself
        return_times = t[near_mask]

        if len(return_times) >= 1:
            first_rec = return_times[0]
        else:
            first_rec = np.inf

        results.append({
            'primes': PRIMES[:level].tolist(),
            'first_recurrence': float(first_rec),
            'count': int(near_mask.sum()),
        })

    return results


# ──────────────────────────────────────────────────────────────
# State complexity
# ──────────────────────────────────────────────────────────────

def state_complexity(theta_mod: np.ndarray, window: int = 100) -> np.ndarray:
    """
    Compute rolling state complexity at each nesting level.

    Complexity at level k = circular variance of the state on orbit k
    over a sliding window. Measures how much the state "explored" recently.

    Returns array of shape (n_windows, n_orbits).
    """
    n_orbits, n_points = theta_mod.shape
    n_windows = n_points - window + 1
    complexity = np.zeros((n_windows, n_orbits))

    for k in range(n_orbits):
        for i in range(n_windows):
            segment = theta_mod[k, i:i + window]
            # Circular variance: 1 - |mean of unit vectors|
            circ_var = 1.0 - np.abs(np.mean(np.exp(1j * segment)))
            complexity[i, k] = circ_var

    return complexity


# ──────────────────────────────────────────────────────────────
# Curvature
# ──────────────────────────────────────────────────────────────

def connection_curvature(
    theta_mod: np.ndarray,
    t: np.ndarray,
    segment_length: int = 200,
) -> list[dict]:
    """
    Measure effective fiber bundle curvature from hierarchical coupling.

    For each coupling pair (inner j → outer k), divide the trajectory into
    segments and measure the variance of the "connection form" dθ_j/dθ_k.
    A flat connection has constant ratio; curvature means the ratio varies.

    Parameters
    ----------
    theta_mod : shape (4, n_points)
    t : time array
    segment_length : samples per segment

    Returns
    -------
    List of dicts with 'pair' (str) and 'mean_curvature' (float).
    """
    n_points = theta_mod.shape[1]
    n_segments = n_points // segment_length
    results = []

    for k in range(1, N_ORBITS):
        for j in range(k):
            pair_label = f"p{PRIMES[j]}→p{PRIMES[k]}"
            curvatures = []

            for seg in range(n_segments):
                start = seg * segment_length
                end = start + segment_length
                seg_theta_j = theta_mod[j, start:end]
                seg_theta_k = theta_mod[k, start:end]

                dtheta_j = np.diff(seg_theta_j)
                dtheta_k = np.diff(seg_theta_k)

                # Avoid division by near-zero angular velocities
                mask = np.abs(dtheta_k) > 1e-8
                if mask.sum() > 10:
                    connection = dtheta_j[mask] / dtheta_k[mask]
                    # Curvature = std of connection (flat = constant ratio)
                    curvatures.append(np.std(connection))

            mean_curv = float(np.mean(curvatures)) if curvatures else 0.0
            results.append({
                'pair': pair_label,
                'mean_curvature': mean_curv,
            })

    return results

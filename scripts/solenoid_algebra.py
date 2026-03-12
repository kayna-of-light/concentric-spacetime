"""
The Discrete Algebra of the Four-Prime Solenoid.

Complement to solenoid_system.py (continuous topology).
This module encodes the multiplicative group Z*_210 and all
algebraic primitives established in NB29-NB42.

The four primes {2, 3, 5, 7} are not axes in a coordinate system.
Each prime is its own STATE-SPACE — a faculty of finite comprehension.
The nesting is STRUCTURE; the state is CUMULATIVE within that structure.
All four faculties are active simultaneously in every configuration.

Faculty mapping (from the theological framework):
    Prime 2: love/wisdom       — the bilateral cut (innermost, constant)
    Prime 3: degree            — celestial / spiritual / natural
    Prime 5: rational          — the product of the mind (five faculties)
    Prime 7: ultimates         — where interaction and embodiment happen

Key algebraic facts:
    P₄ = 2 × 3 × 5 × 7 = 210
    φ(210) = 1 × 2 × 4 × 6 = 48       (group order)
    λ(210) = lcm(1, 2, 4, 6) = 12      (group exponent)
    Z*_210 ≅ C₁ × C₂ × C₄ × C₆       (group structure by CRT)

Primorial nesting:
    P₁ = 2,  P₂ = 6,  P₃ = 30,  P₄ = 210
    Each Pₖ is the cumulative product of primes up to level k.
"""

from __future__ import annotations

import numpy as np
from math import gcd, sqrt
from functools import reduce
from typing import Dict, List, Optional, Sequence, Tuple


# ── Constants ────────────────────────────────────────────────────────

PRIMES: List[int] = [2, 3, 5, 7]
"""The four irreducible primes of the solenoid."""

P: int = 210
"""The primorial P₄ = 2·3·5·7."""

PHI: int = 48
"""Euler totient φ(210) = order of Z*_210."""

GROUP_EXPONENT: int = 12
"""Carmichael function λ(210) = lcm(1,2,4,6). All dynamics repeats after 12 steps."""

PHI_P: Dict[int, int] = {2: 1, 3: 2, 5: 4, 7: 6}
"""Per-prime Euler totients: φ(p) = p − 1."""

PRIMORIALS: List[int] = [2, 6, 30, 210]
"""Primorial sequence [P₁, P₂, P₃, P₄]. Each Pₖ = product of primes 1..k."""

PRIMORIAL_WEIGHTS: Dict[int, int] = {2: 2, 3: 6, 5: 30, 7: 210}
"""Primorial weighting for the Lagrangian. Weight of prime p = Pₖ where p is the k-th prime."""

FACULTY_LABELS: Dict[int, str] = {
    2: "love/wisdom",
    3: "degree",
    5: "rational",
    7: "ultimates",
}
"""Theological mapping of each prime to its faculty."""

PRIMITIVE_ROOTS: Dict[int, int] = {3: 2, 5: 2, 7: 3}
"""Primitive root (generator) for each Z*_p, p > 2."""


# ── Physical constants (NB67+) ───────────────────────────────────────

RHO: float = 1.0 / sqrt(P)
"""Primorial VEV ratio ρ = 1/√P₄ = 1/√210 ≈ 0.069007. The unique coupling (NB76)."""

KAPPA: float = RHO
"""Linear restoring force strength κ = ρ = 1/√210."""

EPSILON: float = RHO
"""Perturbation (inter-level coupling) strength ε = ρ = 1/√210."""

OMEGA: float = 2.0 * np.pi
"""Base frequency on the solenoid."""


# ── Algebraic mass exponents (NB70-73) ───────────────────────────────
# All derived from number theory of 210, zero free parameters.

X4: float = 48 / (2.0 * np.pi)
"""φ(210)/(2π) = 48/(2π) ≈ 7.6394. R₄ exponent for m_s/m_d."""

X3: float = 12 / (2.0 * np.pi)
"""λ(35)/(2π) = 12/(2π) ≈ 1.9099. R₃ exponent for inter-level ratios."""

X2: float = 8 / (2.0 * np.pi)
"""φ(30)/(2π) = 8/(2π) ≈ 1.2732. R₂ exponent for m_b/m_s."""

LAM7: int = 6
"""λ(7) = 6. Generation period; cascade correction exponent."""

X4_LEP: float = 49 / (2.0 * np.pi)
"""p₇²/(2π) = 49/(2π) ≈ 7.7986. Lepton R₄ exponent for m_μ/m_e."""


# ── Discrete log tables (flattened form) ─────────────────────────────

DLOG: Dict[int, Dict[int, int]] = {
    3: {1: 0, 2: 1},
    5: {1: 0, 2: 1, 4: 2, 3: 3},
    7: {1: 0, 3: 1, 2: 2, 6: 3, 4: 4, 5: 5},
}
"""Discrete log tables for CRT sector assignment: DLOG[p][x] = k where g^k ≡ x (mod p)."""


# ── Standard Model physical crossings (NB62, NB72) ──────────────────

PHYSICAL_CROSSINGS: Dict[str, Dict] = {
    'QUARK_g1':  {'ci': 11,  'a3': 1, 'a5': 0, 'a7s': 4, 'type': 'QUARK',  'gen': 'g1'},
    'LEPTON_g1': {'ci': 31,  'a3': 0, 'a5': 0, 'a7s': 1, 'type': 'LEPTON', 'gen': 'g1'},
    'LEPTON_g2': {'ci': 61,  'a3': 0, 'a5': 0, 'a7s': 5, 'type': 'LEPTON', 'gen': 'g2'},
    'QUARK_g2':  {'ci': 191, 'a3': 1, 'a5': 0, 'a7s': 2, 'type': 'QUARK',  'gen': 'g2'},
}
"""Physical CP-pair crossing indices and their CRT labels."""

CP_PAIRS: Dict[str, tuple] = {
    'QUARK':  (1, 4, 2),   # (a₃, a₇*_g1, a₇*_g2)
    'LEPTON': (0, 1, 5),
}
"""CP conjugate pair definitions: channel → (a₃, a₇*_g1, a₇*_g2)."""


# ── PDG target values (PDG 2024) ─────────────────────────────────────

SM_TARGETS: Dict[str, tuple] = {
    'm_s/m_d': (20.0, 2.5),
    'm_c/m_u': (588.0, 100.0),
    'm_b/m_s': (44.75, 4.0),
    'm_b/m_d': (895.0, 100.0),
    'm_t/m_c': (135.8, 5.0),
    'm_mu/m_e': (206.768, 0.0),
}
"""PDG 2024 mass ratio targets: name → (central_value, uncertainty)."""


# ── Covering tower hierarchy (NB49+) ─────────────────────────────────

ACTIVE_PRIMES: List[List[int]] = [[3], [3, 7], [3, 5, 7]]
"""Tower levels: progressive prime activation for generation structure."""


class SolenoidAlgebra:
    """
    The discrete algebraic structure of the four-prime solenoid.

    Encodes Z*_210 as a multiplicative group with CRT decomposition,
    order computation, orbits, characters, and all primitives needed
    for spectral and dynamical analysis.

    Parameters
    ----------
    primes : sequence of int, optional
        Override the prime set. Default: [2, 3, 5, 7].
    """

    def __init__(self, primes: Optional[Sequence[int]] = None):
        self.primes = list(primes) if primes is not None else list(PRIMES)
        self.P = reduce(lambda a, b: a * b, self.primes)
        self.phi_p = {p: p - 1 for p in self.primes}
        self.PHI = reduce(lambda a, b: a * b, self.phi_p.values())

        # Group exponent = lcm of per-prime totients
        self.group_exponent = reduce(_lcm, self.phi_p.values())

        # Primorials: cumulative products
        self.primorials = []
        acc = 1
        for p in self.primes:
            acc *= p
            self.primorials.append(acc)

        # The 48 coprime elements (group members)
        self.Z_star = sorted(
            k for k in range(1, self.P + 1) if gcd(k, self.P) == 1
        )
        assert len(self.Z_star) == self.PHI

        # Index mapping: group element → position in Z_star list
        self._idx = {k: i for i, k in enumerate(self.Z_star)}

        # Primitive roots per prime (p > 2 only; Z*_2 is trivial)
        self.primitive_roots = {}
        for p in self.primes:
            if p == 2:
                continue
            for g in range(2, p):
                if _order_mod(g, p) == p - 1:
                    self.primitive_roots[p] = g
                    break

        # Discrete log tables: dlog[p][x] = k such that g^k ≡ x (mod p)
        self.dlog: Dict[int, Dict[int, int]] = {}
        for p, g in self.primitive_roots.items():
            table = {}
            x = 1
            for k in range(p - 1):
                table[x] = k
                x = (x * g) % p
            self.dlog[p] = table

        # Per-element orders (cached on first call)
        self._orders: Optional[Dict[int, int]] = None

    # ── CRT decomposition ────────────────────────────────────────────

    def decompose(self, k: int) -> Tuple[int, ...]:
        """CRT decomposition: k → (k mod p₁, k mod p₂, …)."""
        return tuple(k % p for p in self.primes)

    def reconstruct(self, residues: Sequence[int]) -> int:
        """Inverse CRT: (r₁, r₂, …) → k mod P via Chinese Remainder Theorem."""
        result = 0
        for r, p in zip(residues, self.primes):
            # Garner's algorithm: weight = P/p, then modular inverse
            M = self.P // p
            inv = pow(M, -1, p)
            result += r * M * inv
        return result % self.P

    # ── Multiplicative group operations ──────────────────────────────

    def multiply(self, a: int, b: int) -> int:
        """Group operation: a · b mod P."""
        return (a * b) % self.P

    def inverse(self, a: int) -> int:
        """Multiplicative inverse of a in Z*_P."""
        return pow(a, -1, self.P)

    def power(self, a: int, n: int) -> int:
        """a^n mod P."""
        return pow(a, n, self.P)

    # ── Order computation ────────────────────────────────────────────

    def order(self, g: int) -> int:
        """Multiplicative order of g in Z*_P."""
        return _order_mod(g, self.P)

    def per_prime_orders(self, g: int) -> Tuple[int, ...]:
        """Orders of g in each Z*_p component."""
        d = self.decompose(g)
        result = []
        for i, p in enumerate(self.primes):
            r = d[i] % p
            if r == 0 or p == 2:
                result.append(1)
            else:
                result.append(_order_mod(r, p))
        return tuple(result)

    @property
    def orders(self) -> Dict[int, int]:
        """Dict of {element: order} for all elements of Z*_P. Cached."""
        if self._orders is None:
            self._orders = {g: self.order(g) for g in self.Z_star}
        return self._orders

    @property
    def order_spectrum(self) -> Dict[int, int]:
        """How many elements have each order: {order: count}."""
        from collections import Counter
        return dict(sorted(Counter(self.orders.values()).items()))

    @property
    def max_order_generators(self) -> List[int]:
        """Elements of maximum order (= group exponent)."""
        return [g for g in self.Z_star if self.orders[g] == self.group_exponent]

    # ── Orbit computation ────────────────────────────────────────────

    def orbit(self, g: int, start: int = 1) -> List[int]:
        """Trace the orbit of start under repeated multiplication by g."""
        result = []
        x = start
        for _ in range(self.PHI):
            result.append(x)
            x = (x * g) % self.P
            if x == start:
                break
        return result

    def orbit_decomposition(self, g: int) -> List[List[int]]:
        """Partition Z*_P into disjoint orbits under multiplication by g."""
        visited = set()
        orbits = []
        for start in self.Z_star:
            if start in visited:
                continue
            orb = self.orbit(g, start)
            visited.update(orb)
            orbits.append(orb)
        return orbits

    # ── Frequency hierarchy ──────────────────────────────────────────

    def frequency_ratios(self, g: int) -> Dict[int, float]:
        """
        Per-prime frequency of g, relative to the total period.

        For a max-order generator: f_p = group_exponent / ord_p(g).
        Inner primes cycle faster (influx: inner is fast/constant,
        outer accumulates/unfolds).
        """
        ppo = self.per_prime_orders(g)
        total = reduce(_lcm, ppo)
        return {p: total / t for p, t in zip(self.primes, ppo)}

    # ── Permutation matrix & eigenvalues ─────────────────────────────

    def permutation_matrix(self, g: int) -> np.ndarray:
        """
        Build the PHI × PHI permutation matrix for multiplication by g.

        P[i, j] = 1 iff Z_star[i] = g · Z_star[j] mod P.
        Eigenvalues are roots of unity encoding the orbit periods.
        """
        mat = np.zeros((self.PHI, self.PHI), dtype=float)
        for k in self.Z_star:
            target = (k * g) % self.P
            mat[self._idx[target], self._idx[k]] = 1.0
        return mat

    def eigenvalue_spectrum(self, g: int) -> Dict[int, int]:
        """
        Eigenvalue multiplicities for the permutation matrix of g.

        Returns {n: multiplicity} where eigenvalue = exp(2πi·n/ord(g)).
        """
        mat = self.permutation_matrix(g)
        evals = np.linalg.eigvals(mat)
        ord_g = self.order(g)
        roots = np.exp(2j * np.pi * np.arange(ord_g) / ord_g)

        mults = {}
        for n, root in enumerate(roots):
            count = int(np.sum(np.abs(evals - root) < 1e-10))
            if count > 0:
                mults[n] = count
        return mults

    # ── Character table ──────────────────────────────────────────────

    def character(
        self, char_index: Tuple[int, ...], g: int
    ) -> complex:
        """
        Evaluate character χ_{char_index} at group element g.

        For Z*_P ≅ ∏ Z*_p, the character indexed by (a₁, a₂, …) is:
            χ(g) = ∏_p  ω_p^(aₚ · dlog_p(g mod p))
        where ω_p = exp(2πi / φ(p)).

        Parameters
        ----------
        char_index : tuple of int
            (a₁, a₂, …) with 0 ≤ aₖ < φ(pₖ).
        g : int
            Group element.
        """
        d = self.decompose(g)
        phase = 0.0
        for i, p in enumerate(self.primes):
            phi = self.phi_p[p]
            a = char_index[i]
            r = d[i] % p
            if phi == 1 or r == 0:
                continue
            k = self.dlog[p].get(r, 0)
            phase += 2 * np.pi * a * k / phi
        return np.exp(1j * phase)

    def all_character_indices(self) -> List[Tuple[int, ...]]:
        """All character indices (a₁, …, aₙ) for the dual group."""
        from itertools import product as cartesian
        ranges = [range(self.phi_p[p]) for p in self.primes]
        return list(cartesian(*ranges))

    def character_table(self) -> np.ndarray:
        """
        Full character table: rows = characters, columns = group elements.

        Returns complex array of shape (PHI, PHI).
        """
        indices = self.all_character_indices()
        table = np.zeros((self.PHI, self.PHI), dtype=complex)
        for i, idx in enumerate(indices):
            for j, g in enumerate(self.Z_star):
                table[i, j] = self.character(idx, g)
        return table

    # ── Spectral functions (for physics) ─────────────────────────────

    def laplacian_energy(self, k: int) -> float:
        """
        Discrete Laplacian energy: Σ_p 2(1 − cos(2π k_p / p)).

        k is an element of Z_P (not necessarily coprime).
        This is the natural energy on the lattice Z_p₁ × … × Z_pₙ.
        """
        d = self.decompose(k)
        return sum(
            2 * (1 - np.cos(2 * np.pi * r / p))
            for r, p in zip(d, self.primes)
        )

    def squared_norm(self, k: int) -> float:
        """Squared norm on the character lattice: Σ (k_p / p)²."""
        d = self.decompose(k)
        return sum((r / p) ** 2 for r, p in zip(d, self.primes))

    # ── Lagrangian weighting ─────────────────────────────────────────

    def primorial_weight(self, p: int) -> int:
        """
        Primorial weight for prime p.

        Each orbit's weight = cumulative product of all primes it CONTAINS.
        The outermost orbit costs 105× more than the innermost.
        """
        idx = self.primes.index(p)
        return self.primorials[idx]

    def weighted_kinetic(
        self, delta: Tuple[int, ...]
    ) -> float:
        """
        Primorial-weighted kinetic term: Σ_p  P_p · |δ_p|².

        delta: per-prime displacements (as CRT tuple).
        """
        return sum(
            self.primorials[i] * (d ** 2)
            for i, d in enumerate(delta)
        )

    # ── Generating sets ──────────────────────────────────────────────

    def generates_group(self, gens: Sequence[int]) -> bool:
        """Check whether a set of elements generates all of Z*_P."""
        generated = set()
        frontier = {1}
        while frontier:
            new = set()
            for x in frontier:
                for g in gens:
                    for y in ((x * g) % self.P, (x * self.inverse(g)) % self.P):
                        if y not in generated and y not in frontier:
                            new.add(y)
                generated.add(x)
            frontier = new
        return len(generated) == self.PHI

    # ── Convenience ──────────────────────────────────────────────────

    def element_index(self, k: int) -> int:
        """Position of element k in the Z_star list (0-based)."""
        return self._idx[k]

    def is_unit(self, k: int) -> bool:
        """Whether k is coprime to P (i.e. a member of Z*_P)."""
        return gcd(k, self.P) == 1

    # ── Sector mapping (NB62+) ───────────────────────────────────────

    def sector(self, ci: int) -> Tuple[int, int, int]:
        """
        Map a crossing index to its CRT sector (a₃, a₅, a₇*).

        Uses discrete log tables. ci must be coprime to P.
        Returns (a₃, a₅, a₇*) where each value is the discrete log
        of (ci mod p) in the corresponding Z*_p.
        """
        return (
            self.dlog[3][ci % 3],
            self.dlog[5][ci % 5],
            self.dlog[7][ci % 7],
        )

    def coprime_indices(self, n: int) -> np.ndarray:
        """Return array of crossing indices in [0, n) coprime to P."""
        return np.array([ci for ci in range(n) if gcd(ci, self.P) == 1])

    def sector_labels(self, coprime_cis: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Vectorized CRT sector labels for an array of coprime crossing indices.

        Returns (a3_array, a5_array, a7_array).
        """
        a3 = np.array([self.dlog[3][ci % 3] for ci in coprime_cis])
        a5 = np.array([self.dlog[5][ci % 5] for ci in coprime_cis])
        a7 = np.array([self.dlog[7][ci % 7] for ci in coprime_cis])
        return a3, a5, a7

    def all_branches(self) -> List[Tuple[int, ...]]:
        """Generate all P branches: (j₁, j₂, ..., jₙ) with 0 ≤ jₖ < pₖ."""
        from itertools import product as cartesian
        return list(cartesian(*(range(p) for p in self.primes)))

    def mass_ratios(
        self,
        cp_ratios: Dict[str, List[float]],
    ) -> Dict[str, float]:
        """
        Compute fermion mass ratios from CP-pair ratios.

        Parameters
        ----------
        cp_ratios : dict
            {'QUARK': [R₁, R₂, R₃, R₄], 'LEPTON': [R₁, R₂, R₃, R₄]}

        Returns
        -------
        dict : mass ratio name → predicted value
        """
        R4_q = cp_ratios['QUARK'][3]
        R3_q = cp_ratios['QUARK'][2]
        R2_q = cp_ratios['QUARK'][1]
        R4_l = cp_ratios['LEPTON'][3]
        return {
            'm_s/m_d': R4_q ** X4,
            'm_c/m_u': R3_q ** X3 * R4_q ** X4,
            'm_b/m_s': R2_q ** X2,
            'm_t/m_c': R2_q ** X2 * R3_q ** X3 / R4_q ** LAM7,
            'm_mu/m_e': R4_l ** X4_LEP,
        }

    def __repr__(self) -> str:
        return (
            f"SolenoidAlgebra(primes={self.primes}, P={self.P}, "
            f"φ={self.PHI}, λ={self.group_exponent})"
        )


# ── Module-level helpers ─────────────────────────────────────────────

def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def _order_mod(a: int, n: int) -> int:
    """Multiplicative order of a mod n."""
    if gcd(a, n) != 1:
        return 0
    o, x = 1, a % n
    while pow(a, o, n) != 1:
        o += 1
    return o


# ── Default instance ─────────────────────────────────────────────────

# Pre-built instance for the canonical {2,3,5,7} solenoid.
# Import and use directly: from solenoid_algebra import SA
SA = SolenoidAlgebra()

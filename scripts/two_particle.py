"""
Two-Particle Extension of the Concentric System on S² × R⁺

Tests the entanglement thesis: curvature produces correlation,
flatness produces separability.

Two excitations on the same manifold interact through the shared
Coulomb potential.  Their coupling, and therefore their entanglement,
is a function of the manifold curvature R.

    R finite  →  entangled (states correlated through shared center)
    R → ∞     →  separable (flat limit, classical independence)

This module provides:
    · Slater radial integrals  F^k, G^k
    · Gaunt angular coefficients (via sympy Wigner 3j)
    · Two-particle antisymmetrized basis
    · Hamiltonian matrix construction
    · Entanglement entropy from reduced density matrix
"""

import numpy as np
from itertools import combinations
from functools import lru_cache
from sympy.physics.wigner import gaunt as sympy_gaunt
from scipy.integrate import quad

from concentric_system import (
    radial_wavefunction,
    energy_level,
    valid_states,
)


# ═══════════════════════════════════════════════════════════
# Single-particle basis
# ═══════════════════════════════════════════════════════════

def single_particle_states(n_max: int):
    """
    All single-particle states |n, l, m, s⟩ up to shell n_max.
    s = +1/2 (↑) or -1/2 (↓).
    Returns list of (n, l, m, s) tuples.
    """
    states = []
    for n, l, m in valid_states(n_max):
        states.append((n, l, m, +0.5))
        states.append((n, l, m, -0.5))
    return states


# ═══════════════════════════════════════════════════════════
# Radial integrals  (Slater integrals)
# ═══════════════════════════════════════════════════════════

def _radial_integrand_Rk(r, n1, l1, n2, l2, k, R_scale):
    """
    Inner piece of Slater integral: for a given r1, compute
    the integral over r2 of R_n1l1(r1)² × (r<^k / r>^{k+1}) × R_n2l2(r2)² × r2² dr2.

    We split into r2 < r1 and r2 > r1.

    R_scale rescales coordinates: r_phys = r * R_scale.
    In atomic units on S² × R⁺ with curvature radius R,
    the Bohr radius scales as a₀ → a₀ · R.
    """
    r1 = r * R_scale
    # We do this numerically via nested integration
    # For efficiency, we'll compute the full 2D integral differently
    pass


def slater_Rk(n1, l1, n2, l2, k, R_scale=1.0, r_max=None, n_grid=2000):
    """
    Slater radial integral R^k(n1 l1, n2 l2):

        R^k = ∫∫ |R_{n1,l1}(r1)|² |R_{n2,l2}(r2)|²
              × (r_<^k / r_>^{k+1}) × r1² r2²  dr1 dr2

    where r_< = min(r1,r2), r_> = max(r1,r2).

    R_scale controls the Bohr radius scaling: on a sphere of radius R,
    the effective Bohr radius is a₀·R, stretching all radial functions.

    Computed by numerical quadrature on a log-linear grid.
    """
    if r_max is None:
        r_max = max(4 * (n1**2 + n2**2), 60) * R_scale

    # Build radial grid (denser near origin where curvature matters)
    r_lin = np.linspace(0, r_max, n_grid)
    r_lin[0] = 1e-10  # avoid r=0 singularity
    dr = np.diff(r_lin)

    # Evaluate radial densities: ρ(r) = R_nl(r/R_scale)² × r² on scaled coords
    def rho(n, l):
        r_scaled = r_lin / R_scale
        R_nl = radial_wavefunction(n, l, r_scaled)
        return R_nl**2 * r_lin**2

    rho1 = rho(n1, l1)
    rho2 = rho(n2, l2)

    # Compute R^k via the Yk(r1) method:
    #   Y_k(r1) = ∫ ρ2(r2) × (r<^k / r>^{k+1}) dr2
    #           = r1^{-(k+1)} ∫_0^{r1} ρ2(r2) r2^k dr2
    #             + r1^k ∫_{r1}^{∞} ρ2(r2) r2^{-(k+1)} dr2
    # Then R^k = ∫ ρ1(r1) Y_k(r1) dr1

    rho2_rk = rho2 * r_lin**k          # ρ2(r) × r^k
    rho2_rmk1 = rho2 * r_lin**(-(k+1)) # ρ2(r) × r^{-(k+1)}

    # Cumulative integrals (trapezoidal)
    # inner_integral[i] = ∫_0^{r_i} ρ2(r) r^k dr
    inner_integral = np.zeros(n_grid)
    for i in range(1, n_grid):
        inner_integral[i] = inner_integral[i-1] + 0.5 * (rho2_rk[i-1] + rho2_rk[i]) * dr[i-1]

    # outer_integral[i] = ∫_{r_i}^{∞} ρ2(r) r^{-(k+1)} dr
    outer_integral = np.zeros(n_grid)
    for i in range(n_grid - 2, -1, -1):
        outer_integral[i] = outer_integral[i+1] + 0.5 * (rho2_rmk1[i] + rho2_rmk1[i+1]) * dr[i]

    # Y_k(r1) for each grid point
    with np.errstate(divide='ignore', invalid='ignore'):
        Yk = np.where(r_lin > 1e-15,
                       r_lin**(-(k+1)) * inner_integral + r_lin**k * outer_integral,
                       0.0)

    # R^k = ∫ ρ1(r1) × Y_k(r1) dr1
    integrand = rho1 * Yk
    result = np.sum(0.5 * (integrand[:-1] + integrand[1:]) * dr)

    return result


# ═══════════════════════════════════════════════════════════
# Angular coefficients  (Gaunt integrals via sympy)
# ═══════════════════════════════════════════════════════════

@lru_cache(maxsize=4096)
def gaunt_coefficient(l1, m1, k, q, l2, m2):
    """
    Gaunt integral: ∫ Y_{l1}^{m1*} Y_k^q Y_{l2}^{m2} dΩ.

    This encodes the angular selection rules for the Coulomb interaction.
    Returns float.
    """
    val = sympy_gaunt(l1, k, l2, m1, q, m2)
    return float(val)


def angular_coulomb_coefficient(l1, m1, l2, m2, la, ma, lb, mb):
    """
    Full angular coefficient for the Coulomb matrix element
    ⟨l1 m1, l2 m2 | 1/r12 | la ma, lb mb⟩.

    The 1/|r1-r2| expansion gives:
        Σ_k (4π/(2k+1)) Σ_q Y_k^{q*}(Ω1) Y_k^q(Ω2) × (r<^k/r>^{k+1})

    The angular part yields:
        Σ_k (4π/(2k+1)) × c_k(l1,m1,la,ma) × c_k(l2,m2,lb,mb)

    where c_k(l,m,l',m') = ∫ Y_l^{m*} Y_k^{m'-m} Y_{l'}^{m'} dΩ
    and the sum runs over k where the Gaunt integrals are nonzero.
    """
    k_max = max(l1 + la, l2 + lb)  # triangular condition limits k
    result = {}  # k -> angular coefficient (to pair with Slater R^k)

    for k in range(0, k_max + 1):
        q = ma - m1  # selection rule: (-m1) + (-q) + ma = 0
        if abs(q) > k:
            continue
        # Second Gaunt requires q = m2 - mb (total m conservation)
        if q != m2 - mb:
            continue

        # First angular: ⟨l1,m1| Y_k^{q*} |la,ma⟩
        #   = (-1)^{q+m1} × gaunt(l1, k, la; -m1, -q, ma)
        # Second angular: ⟨l2,m2| Y_k^q |lb,mb⟩
        #   = (-1)^{m2} × gaunt(l2, k, lb; -m2, q, mb)
        g1 = (-1)**(q + m1) * gaunt_coefficient(l1, -m1, k, -q, la, ma)
        g2 = (-1)**m2 * gaunt_coefficient(l2, -m2, k, q, lb, mb)

        if abs(g1) > 1e-15 and abs(g2) > 1e-15:
            factor = 4 * np.pi / (2 * k + 1)
            result[k] = factor * g1 * g2

    return result


# ═══════════════════════════════════════════════════════════
# Two-particle basis  (antisymmetrized Slater determinants)
# ═══════════════════════════════════════════════════════════

def two_particle_basis(sp_states):
    """
    Build antisymmetrized two-particle basis from single-particle states.
    Each basis function is |ij⟩_A = (|i⟩|j⟩ - |j⟩|i⟩)/√2, i < j.

    Returns list of (i, j) index pairs into sp_states.
    """
    n_sp = len(sp_states)
    return list(combinations(range(n_sp), 2))


# ═══════════════════════════════════════════════════════════
# Hamiltonian construction
# ═══════════════════════════════════════════════════════════

def coulomb_matrix_element(state_a, state_b, state_c, state_d, R_scale=1.0, n_grid=2000):
    """
    Two-electron Coulomb matrix element:
        ⟨ab|1/r12|cd⟩ = Σ_k angular_k × R^k(na la, nb lb, nc lc, nd ld)

    States are (n, l, m, s) tuples.
    Spin orthogonality: nonzero only if s_a == s_c and s_b == s_d
    (for direct) or s_a == s_d and s_b == s_c (for exchange).

    R_scale: Bohr radius scaling from manifold curvature.
    """
    na, la, ma, sa = state_a
    nb, lb, mb, sb = state_b
    nc, lc, mc, sc = state_c
    nd, ld, md, sd = state_d

    # Spin orthogonality (direct term)
    if sa != sc or sb != sd:
        return 0.0

    ang_coeffs = angular_coulomb_coefficient(la, ma, lb, mb, lc, mc, ld, md)
    if not ang_coeffs:
        return 0.0

    total = 0.0
    for k, ang_k in ang_coeffs.items():
        Rk = slater_Rk(na, la, nc, lc, k, R_scale=R_scale, n_grid=n_grid)
        # For the second pair we need the cross Slater integral
        # But actually R^k already encodes both radial functions.
        # The full integral is: R^k(a c, b d) with the Yk method generalized.
        # Let me use the proper two-pair Slater integral.
        pass

    # Recompute properly: the Coulomb integral factorizes as
    # ⟨ab|1/r12|cd⟩ = Σ_k ang_k × R^k(ac;bd)
    # where R^k(ac;bd) = ∫∫ R_a(r1)R_c(r1) × (r<^k/r>^{k+1}) × R_b(r2)R_d(r2) r1²r2² dr1 dr2

    total = 0.0
    for k, ang_k in ang_coeffs.items():
        Rk = slater_Rk_cross(na, la, nc, lc, nb, lb, nd, ld, k,
                              R_scale=R_scale, n_grid=n_grid)
        total += ang_k * Rk

    return total


def slater_Rk_cross(n1, l1, n3, l3, n2, l2, n4, l4, k,
                     R_scale=1.0, r_max=None, n_grid=2000):
    """
    Cross Slater radial integral:

        R^k(13;24) = ∫∫ R_{n1,l1}(r1) R_{n3,l3}(r1)
                        × (r_<^k / r_>^{k+1})
                        × R_{n2,l2}(r2) R_{n4,l4}(r2)
                        × r1² r2²  dr1 dr2

    Generalizes the diagonal Slater integral to off-diagonal pairs.
    """
    if r_max is None:
        r_max = max(4 * max(n1, n2, n3, n4)**2, 60) * R_scale

    r = np.linspace(0, r_max, n_grid)
    r[0] = 1e-10
    dr = np.diff(r)

    r_scaled = r / R_scale

    # Product densities
    R1 = radial_wavefunction(n1, l1, r_scaled)
    R3 = radial_wavefunction(n3, l3, r_scaled)
    rho13 = R1 * R3 * r**2  # φ_1(r) φ_3(r) r²

    R2 = radial_wavefunction(n2, l2, r_scaled)
    R4 = radial_wavefunction(n4, l4, r_scaled)
    rho24 = R2 * R4 * r**2

    # Yk method on rho24
    rho24_rk = rho24 * r**k
    rho24_rmk1 = rho24 * r**(-(k+1))

    inner_integral = np.zeros(n_grid)
    for i in range(1, n_grid):
        inner_integral[i] = inner_integral[i-1] + 0.5 * (rho24_rk[i-1] + rho24_rk[i]) * dr[i-1]

    outer_integral = np.zeros(n_grid)
    for i in range(n_grid - 2, -1, -1):
        outer_integral[i] = outer_integral[i+1] + 0.5 * (rho24_rmk1[i] + rho24_rmk1[i+1]) * dr[i]

    with np.errstate(divide='ignore', invalid='ignore'):
        Yk = np.where(r > 1e-15,
                       r**(-(k+1)) * inner_integral + r**k * outer_integral,
                       0.0)

    integrand = rho13 * Yk
    result = np.sum(0.5 * (integrand[:-1] + integrand[1:]) * dr)
    return result


def build_two_particle_hamiltonian(sp_states, R_scale=1.0, n_grid=1500):
    """
    Build the full two-particle Hamiltonian in the antisymmetrized basis.

    H = H₀ + V₁₂

    H₀ = E_{n_i} + E_{n_j}  (diagonal: sum of single-particle energies)
    V₁₂ = ⟨ij|1/r12|kl⟩_A  (antisymmetrized Coulomb matrix elements)

    where ⟨ij|V|kl⟩_A = ⟨ij|V|kl⟩ - ⟨ij|V|lk⟩  (direct - exchange).

    Returns (H, basis_pairs, sp_states).
    """
    basis = two_particle_basis(sp_states)
    N = len(basis)
    H = np.zeros((N, N))

    # Diagonal: single-particle energies (scaled by 1/R² for curvature)
    for idx, (i, j) in enumerate(basis):
        ni, li, mi, si = sp_states[i]
        nj, lj, mj, sj = sp_states[j]
        # Energy scales as 1/R_scale² on the curved manifold
        H[idx, idx] = (energy_level(ni) + energy_level(nj)) / R_scale**2

    # Off-diagonal + Coulomb corrections
    for row, (i, j) in enumerate(basis):
        for col, (k, l) in enumerate(basis):
            if col < row:
                continue  # exploit Hermiticity

            si = sp_states[i]
            sj = sp_states[j]
            sk = sp_states[k]
            sl = sp_states[l]

            # Direct: ⟨ij|V|kl⟩
            direct = coulomb_matrix_element(si, sj, sk, sl,
                                             R_scale=R_scale, n_grid=n_grid)
            # Exchange: ⟨ij|V|lk⟩
            exchange = coulomb_matrix_element(si, sj, sl, sk,
                                              R_scale=R_scale, n_grid=n_grid)

            V_antisym = direct - exchange
            # Scale Coulomb by 1/R_scale (e²/r scales as 1/R in curved coords)
            V_antisym /= R_scale

            H[row, col] += V_antisym
            if row != col:
                H[col, row] += V_antisym

    return H, basis, sp_states


# ═══════════════════════════════════════════════════════════
# Entanglement entropy
# ═══════════════════════════════════════════════════════════

def reduced_density_matrix(eigenvector, basis, n_sp):
    """
    Trace over particle 2 to get the reduced density matrix ρ₁.

    Given |Ψ⟩ = Σ_{i<j} c_{ij} |ij⟩_A in the antisymmetrized basis,
    ρ₁ = Tr₂(|Ψ⟩⟨Ψ|).

    The matrix elements are:
        ρ₁[a,b] = Σ_j c_{aj}* c_{bj}   (summing over shared particle-2 index)
    """
    rho = np.zeros((n_sp, n_sp))

    # Build coefficient matrix c[i,j] from eigenvector
    # basis contains (i,j) pairs with i < j
    c_matrix = np.zeros((n_sp, n_sp))
    for idx, (i, j) in enumerate(basis):
        c_matrix[i, j] = eigenvector[idx]
        c_matrix[j, i] = -eigenvector[idx]  # antisymmetry

    # ρ₁[a,b] = Σ_k c[a,k] c[b,k]*
    rho = c_matrix @ c_matrix.T

    return rho


def von_neumann_entropy(rho):
    """
    Von Neumann entropy: S = -Tr(ρ ln ρ).

    S = 0  → pure state (separable, no entanglement)
    S > 0  → mixed state (entangled, correlated through shared geometry)
    S = ln(d) → maximally entangled
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    # Filter out numerical noise
    eigenvalues = eigenvalues[eigenvalues > 1e-14]
    if len(eigenvalues) == 0:
        return 0.0
    return -np.sum(eigenvalues * np.log(eigenvalues))


def spatial_reduced_density_matrix(eigenvector, basis, sp_states):
    """
    Spatial (orbital-only) 1-RDM: trace over both particle-2 AND spin.

        γ^spatial[α,β] = Σ_σ  γ^spinorbital[α σ, β σ]

    where α, β are spatial orbital indices (n, l, m).
    Eigenvalues are natural orbital occupation numbers (sum to N=2).
    """
    n_sp = len(sp_states)
    # Build spin-orbital 1-RDM
    rho_sp = reduced_density_matrix(eigenvector, basis, n_sp)

    # Map spin-orbital indices → spatial orbital indices
    spatial_orbs = []
    sp_to_spatial = {}
    for i, (n, l, m, s) in enumerate(sp_states):
        key = (n, l, m)
        if key not in spatial_orbs:
            spatial_orbs.append(key)
        sp_to_spatial[i] = spatial_orbs.index(key)

    n_spatial = len(spatial_orbs)
    gamma = np.zeros((n_spatial, n_spatial))
    for a in range(n_sp):
        for b in range(n_sp):
            # Only sum if same spin (orthogonality of spin functions)
            if sp_states[a][3] == sp_states[b][3]:
                gamma[sp_to_spatial[a], sp_to_spatial[b]] += rho_sp[a, b]

    return gamma


def spatial_entanglement_entropy(eigenvector, basis, sp_states):
    """
    Orbital entanglement entropy: von Neumann entropy of the
    normalized spatial 1-RDM.

    The spatial 1-RDM has Tr = N (number of electrons).
    Normalizing by N gives a proper density matrix whose
    entropy measures spatial (orbital) correlation only,
    excluding trivial spin entanglement from antisymmetrization.
    """
    gamma = spatial_reduced_density_matrix(eigenvector, basis, sp_states)
    N = np.trace(gamma)
    if N < 1e-14:
        return 0.0
    rho_norm = gamma / N
    eigenvalues = np.linalg.eigvalsh(rho_norm)
    eigenvalues = eigenvalues[eigenvalues > 1e-14]
    if len(eigenvalues) == 0:
        return 0.0
    return -np.sum(eigenvalues * np.log(eigenvalues))


def conditional_entropy(eigenvector, basis, sp_states, trace_over='particle2'):
    """
    Compute the conditional von Neumann entropy.

    S(1|2) = S(ρ₁₂) - S(ρ₂)

    For a pure state |Ψ⟩, S(ρ₁₂) = 0, so S(1|2) = -S(ρ₂).
    And by Schmidt decomposition, S(ρ₁) = S(ρ₂).

    But for the asymmetry test, we compute the mutual information
    between SUBSETS of quantum numbers, not full particle traces.
    """
    n_sp = len(sp_states)
    rho = reduced_density_matrix(eigenvector, basis, n_sp)
    return von_neumann_entropy(rho)


# ═══════════════════════════════════════════════════════════
# Shell-resolved entanglement
# ═══════════════════════════════════════════════════════════

def shell_restricted_basis(sp_states, shell_range):
    """
    Get indices of single-particle states within specified shells.
    shell_range: tuple (n_min, n_max) inclusive.
    """
    return [i for i, (n, l, m, s) in enumerate(sp_states)
            if shell_range[0] <= n <= shell_range[1]]


def entanglement_vs_curvature(n_max=2, R_values=None, n_grid=1000):
    """
    Main test: compute entanglement entropy of the two-particle
    ground state as a function of manifold curvature radius R.

    Prediction: S(R) monotonically decreasing.
        Small R (high curvature) → large S (strong entanglement)
        Large R (flat)           → small S (approaching separability)

    Returns dict with R_values, entropies, and ground state energies.
    """
    if R_values is None:
        R_values = np.array([0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0])

    sp_states = single_particle_states(n_max)
    results = {
        'R_values': R_values,
        'entropies': [],
        'ground_energies': [],
        'n_basis': 0,
    }

    for R in R_values:
        H, basis, _ = build_two_particle_hamiltonian(
            sp_states, R_scale=R, n_grid=n_grid
        )
        results['n_basis'] = len(basis)

        eigenvalues, eigenvectors = np.linalg.eigh(H)
        ground_state = eigenvectors[:, 0]
        ground_energy = eigenvalues[0]

        rho1 = reduced_density_matrix(ground_state, basis, len(sp_states))
        S = von_neumann_entropy(rho1)

        results['entropies'].append(S)
        results['ground_energies'].append(ground_energy)

    results['entropies'] = np.array(results['entropies'])
    results['ground_energies'] = np.array(results['ground_energies'])

    return results


# ═══════════════════════════════════════════════════════════
# Z-scaling approach  (precompute once, rescale for sweep)
# ═══════════════════════════════════════════════════════════

def precompute_matrices(sp_states, n_grid=1500):
    """
    Precompute the kinetic (H₀) and Coulomb (V) matrices at Z=1.

    The hydrogen-like Z-scaling theorem gives:
        H(Z) = Z² × H₀ + Z × V

    where Z plays the role of curvature strength:
        Z = 1/R  (large Z → high curvature/strong center, Z→0 → flat)

    H₀[ij,kl] = δ_{ik}δ_{jl} × (ε_i + ε_j)     kinetic + central potential
    V[ij,kl]  = ⟨ij|1/r₁₂|kl⟩_A                  antisymmetrized Coulomb

    Both computed at Z=1 (R_scale=1).  The Slater integrals are expensive,
    so we compute them once here.

    Returns (H0, V, basis, sp_states).
    """
    basis = two_particle_basis(sp_states)
    N = len(basis)
    H0 = np.zeros((N, N))
    V = np.zeros((N, N))

    # H₀: diagonal single-particle energies at Z=1
    for idx, (i, j) in enumerate(basis):
        ni = sp_states[i][0]
        nj = sp_states[j][0]
        H0[idx, idx] = energy_level(ni) + energy_level(nj)

    # V: antisymmetrized Coulomb at Z=1 (R_scale=1)
    for row, (i, j) in enumerate(basis):
        for col, (k, l) in enumerate(basis):
            if col < row:
                continue

            si, sj, sk, sl = sp_states[i], sp_states[j], sp_states[k], sp_states[l]

            direct = coulomb_matrix_element(si, sj, sk, sl,
                                             R_scale=1.0, n_grid=n_grid)
            exchange = coulomb_matrix_element(si, sj, sl, sk,
                                              R_scale=1.0, n_grid=n_grid)
            V_elem = direct - exchange

            V[row, col] = V_elem
            if row != col:
                V[col, row] = V_elem

    return H0, V, basis


def hamiltonian_at_Z(H0, V, Z):
    """
    Form the full Hamiltonian at curvature parameter Z.

        H(Z) = Z² × H₀  +  Z × V

    Z = 1/R where R is the manifold curvature radius.
      Z large → strong center → deeply bound → large gaps
      Z small → weak center → barely bound → flat limit
      Z = 1   → standard hydrogen units
    """
    return Z**2 * H0 + Z * V


def entanglement_sweep(H0, V, basis, n_sp, Z_values):
    """
    Efficient curvature sweep: compute ground-state entanglement
    entropy S(Z) using precomputed matrices.

    The Slater integrals are computed once (in precompute_matrices);
    here we only rescale and diagonalize at each Z.

    Returns dict with Z_values, entropies, ground_energies,
    rho_eigenvalues (per Z), and ground_state_coeffs.
    """
    results = {
        'Z_values': np.asarray(Z_values, dtype=float),
        'entropies': np.zeros(len(Z_values)),
        'ground_energies': np.zeros(len(Z_values)),
        'rho_eigenvalues': [],
        'eigenvalue_spectra': [],
    }

    for idx, Z in enumerate(Z_values):
        H = hamiltonian_at_Z(H0, V, Z)
        eigenvalues, eigenvectors = np.linalg.eigh(H)

        ground_state = eigenvectors[:, 0]
        results['ground_energies'][idx] = eigenvalues[0]
        results['eigenvalue_spectra'].append(eigenvalues)

        rho1 = reduced_density_matrix(ground_state, basis, n_sp)
        rho_eigs = np.linalg.eigvalsh(rho1)
        rho_eigs = rho_eigs[rho_eigs > 1e-14]

        results['rho_eigenvalues'].append(rho_eigs)
        results['entropies'][idx] = -np.sum(rho_eigs * np.log(rho_eigs)) if len(rho_eigs) > 0 else 0.0

    return results

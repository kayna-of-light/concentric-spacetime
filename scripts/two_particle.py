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


# ═══════════════════════════════════════════════════════════
# One-body operators in Slater determinant basis
# (Zeeman, spin-orbit, Stark)
# ═══════════════════════════════════════════════════════════

def _one_body_op_slater(sp_states, basis, op_func):
    """
    Build a one-body operator O = Σ_i o(i) in the antisymmetrised
    Slater-determinant basis using Slater–Condon rules.

    op_func(a, b) returns the single-particle matrix element ⟨a|o|b⟩
    where a, b are spin-orbital indices.

    For a two-electron Slater determinant |ij⟩_A with i<j:
        ⟨ij|O|kl⟩ = δ_jl ⟨i|o|k⟩ + δ_ik ⟨j|o|l⟩
                   - δ_jk ⟨i|o|l⟩ - δ_il ⟨j|o|k⟩
    """
    N = len(basis)
    mat = np.zeros((N, N))
    for row, (i, j) in enumerate(basis):
        for col, (k, l) in enumerate(basis):
            val = 0.0
            if j == l:
                val += op_func(i, k)
            if i == k:
                val += op_func(j, l)
            if j == k:
                val -= op_func(i, l)
            if i == l:
                val -= op_func(j, k)
            mat[row, col] = val
    return mat


def zeeman_matrix(sp_states, basis, B=1.0):
    """
    Zeeman perturbation in Slater determinant basis.

    H_Z = (B/2) × (L_z + 2S_z)  [atomic units, μ_B = 1/2]

    The single-particle matrix element is diagonal:
        ⟨a|l_z + 2s_z|b⟩ = δ_{ab} × (m_a + 2s_a)
    """
    def op(a, b):
        if a != b:
            return 0.0
        _, _, m_a, s_a = sp_states[a][:4]
        return m_a + 2 * s_a

    return (B / 2) * _one_body_op_slater(sp_states, basis, op)


def total_mj_matrix(sp_states, basis):
    """
    Total M_J = M_L + M_S operator in Slater determinant basis.

    Each spin-orbital contributes m_l + m_s (diagonal).
    """
    def op(a, b):
        if a != b:
            return 0.0
        _, _, m_a, s_a = sp_states[a][:4]
        return m_a + s_a

    return _one_body_op_slater(sp_states, basis, op)


def spin_orbit_radial_integral(n, l, Z=1, R_scale=1.0, n_grid=2000):
    """
    Radial part of spin-orbit coupling:
        ξ_{nl} = (α²/2) × Z × ∫₀^∞ R_{nl}(r) × (1/r³) × R_{nl}(r) × r² dr

    For hydrogen-like atoms: ξ_{nl} = (α² Z⁴) / (2 n³ l(l+½)(l+1))  [exact]
    We use the analytic formula for efficiency and accuracy.

    Returns ξ in Hartree.
    """
    if l == 0:
        return 0.0  # L·S = 0 for s-orbitals (l=0 → no spin-orbit)
    alpha = 1 / 137.035999  # fine structure constant
    # Exact hydrogen-like result
    xi = (alpha**2 * Z**4) / (2 * n**3 * l * (l + 0.5) * (l + 1))
    return xi


def _ls_single_particle(sp_states, a, b, Z=1):
    """
    Single-particle matrix element of L·S between spin-orbitals a and b.

    L·S = L_z S_z + (L₊S₋ + L₋S₊)/2

    Only connects states with same n, l and gives non-zero when:
      - Same spatial orbital, same spin: L_z × S_z term
      - Same n,l, m differs by ±1, spin flips: L₊S₋ or L₋S₊ terms
    """
    n_a, l_a, m_a, s_a = sp_states[a][:4]
    n_b, l_b, m_b, s_b = sp_states[b][:4]

    # L·S only couples states within same n, l subshell
    if n_a != n_b or l_a != l_b:
        return 0.0

    val = 0.0

    # L_z S_z term: diagonal in m_l and m_s
    if m_a == m_b and s_a == s_b:
        val += m_a * s_a

    # L₊S₋ term: m_l increases by 1, m_s decreases by 1 (spin down)
    # ⟨l,m+1| L₊ |l,m⟩ = √(l(l+1) - m(m+1))
    # ⟨s,-½| S₋ |s,+½⟩ = 1  (for s=½)
    if m_a == m_b + 1 and s_a == s_b - 1:
        lp = np.sqrt(l_a * (l_a + 1) - m_b * (m_b + 1))
        sm = 1.0  # √(s(s+1) - ms(ms-1)) = √(3/4 - ½×(-½)) = 1
        val += 0.5 * lp * sm

    # L₋S₊ term: m_l decreases by 1, m_s increases by 1 (spin up)
    if m_a == m_b - 1 and s_a == s_b + 1:
        lm = np.sqrt(l_a * (l_a + 1) - m_b * (m_b - 1))
        sp = 1.0
        val += 0.5 * lm * sp

    return val


def spin_orbit_matrix(sp_states, basis, Z=1):
    """
    Spin-orbit coupling H_SO = Σ_i ξ(r_i) × L_i · S_i  in Slater det basis.

    For hydrogen-like systems:
        ξ_{nl} = (α² Z⁴) / (2 n³ l(l+½)(l+1))

    The matrix in CI eigenstate basis:  V_SO_CI = U^T × V_SO_slater × U
    """
    # Precompute ξ for each (n,l) subshell
    xi_cache = {}
    for st in sp_states:
        n, l = st[0], st[1]
        key = (n, l)
        if key not in xi_cache:
            xi_cache[key] = spin_orbit_radial_integral(n, l, Z=Z)

    def op(a, b):
        n_a, l_a = sp_states[a][0], sp_states[a][1]
        xi = xi_cache[(n_a, l_a)]
        if xi == 0.0:
            return 0.0
        return xi * _ls_single_particle(sp_states, a, b, Z=Z)

    return _one_body_op_slater(sp_states, basis, op)


def stark_matrix(sp_states, basis, F=1.0, R_scale=1.0, n_grid=2000):
    """
    Stark effect perturbation: H_E = F × z = F × r × cos(θ)

    This is the q=0 component of the dipole operator scaled by F.
    Reuses the dipole machinery: ⟨a|z|b⟩ = ⟨a|r cos θ|b⟩

    Returns the perturbation matrix in the Slater determinant basis.
    """
    def op(a, b):
        n_a, l_a, m_a, s_a = sp_states[a][:4]
        n_b, l_b, m_b, s_b = sp_states[b][:4]
        if s_a != s_b:
            return 0.0  # dipole doesn't flip spin
        # z = r cos θ  →  q=0 component
        ang = dipole_angular_coefficient(l_a, m_a, l_b, m_b, q=0)
        if abs(ang) < 1e-15:
            return 0.0
        rad = radial_dipole_integral(n_a, l_a, n_b, l_b,
                                      R_scale=R_scale, n_grid=n_grid)
        return np.sqrt(4 * np.pi / 3) * rad * ang

    return F * _one_body_op_slater(sp_states, basis, op)


def lande_g_factor(eigenvector, basis, sp_states, H0, V, Z,
                   B_values=None):
    """
    Compute the Landé g-factor for a CI eigenstate by measuring the
    linear Zeeman slope: dE/dB = g × M_J × μ_B.

    Uses numerical differentiation of eigenvalue vs B.
    """
    if B_values is None:
        B_values = np.array([0.0, 1e-6, 2e-6])

    H_base = hamiltonian_at_Z(H0, V, Z)

    # Find index of the target state at B=0
    evals_0, evecs_0 = np.linalg.eigh(H_base)
    overlaps = np.abs(evecs_0.T @ eigenvector)
    target_idx = np.argmax(overlaps)

    energies = []
    for B in B_values:
        H_B = H_base + zeeman_matrix(sp_states, basis, B)
        evals_B = np.linalg.eigvalsh(H_B)
        energies.append(evals_B[target_idx])

    energies = np.array(energies)
    # dE/dB via finite difference
    dEdB = (energies[-1] - energies[0]) / (B_values[-1] - B_values[0])

    # M_J for this state
    MJ_mat = total_mj_matrix(sp_states, basis)
    MJ = eigenvector @ MJ_mat @ eigenvector

    if abs(MJ) < 1e-10:
        return 0.0  # M_J = 0, can't determine g
    # dE/dB = g × M_J / 2  (atomic units, μ_B = 1/2)
    g = 2 * dEdB / MJ
    return g


# ═══════════════════════════════════════════════════════════
# Dipole matrix elements  (spectral properties)
# ═══════════════════════════════════════════════════════════

def radial_dipole_integral(n1, l1, n2, l2, R_scale=1.0, n_grid=2000):
    """
    Radial dipole integral: ∫₀^∞ R_{n1,l1}(r) × r × R_{n2,l2}(r) × r² dr.

    The extra factor of r comes from the dipole operator.
    R_scale controls the Bohr radius scaling from manifold curvature.
    """
    r_max = max(4 * max(n1, n2)**2, 60) * R_scale
    r = np.linspace(0, r_max, n_grid)
    r[0] = 1e-10
    dr = np.diff(r)

    r_scaled = r / R_scale
    R1 = radial_wavefunction(n1, l1, r_scaled)
    R2 = radial_wavefunction(n2, l2, r_scaled)

    # Integrand: R1(r) * r * R2(r) * r²  (the r² is from volume element)
    integrand = R1 * r * R2 * r**2
    result = np.sum(0.5 * (integrand[:-1] + integrand[1:]) * dr)
    return result


def dipole_angular_coefficient(l1, m1, l2, m2, q):
    """
    Angular part of the dipole matrix element for polarization q.

    ⟨l1,m1| C^1_q |l2,m2⟩  where C^1_q = √(4π/3) Y_1^q

    The bra requires complex conjugation:
        ∫ Y_{l1}^{m1*} Y_1^q Y_{l2}^{m2} dΩ
      = (-1)^{m1} × ∫ Y_{l1}^{-m1} Y_1^q Y_{l2}^{m2} dΩ
      = (-1)^{m1} × gaunt(l1, -m1, 1, q, l2, m2)

    q = 0  → z-component (ΔM = 0)
    q = ±1 → circular components (ΔM = ±1)
    """
    # Selection rule: m1 = m2 + q
    if m1 != m2 + q:
        return 0.0
    # Triangle rule: |l1 - l2| ≤ 1 ≤ l1 + l2
    if abs(l1 - l2) > 1 or l1 + l2 < 1:
        return 0.0
    # Parity rule: l1 + l2 must be odd (for dipole)
    if (l1 + l2) % 2 == 0:
        return 0.0

    # Gaunt integral with proper bra conjugation: Y_{l1}^{m1*} = (-1)^{m1} Y_{l1}^{-m1}
    g = (-1)**m1 * gaunt_coefficient(l1, -m1, 1, q, l2, m2)
    return g


def one_body_dipole_element(state_a, state_b, q, R_scale=1.0):
    """
    Single-particle dipole matrix element ⟨a| r_q |b⟩.

    r_q = r × √(4π/3) × Y_1^q  (spherical component of position operator)

    Returns the full matrix element (radial × angular).
    """
    na, la, ma, sa = state_a
    nb, lb, mb, sb = state_b

    # Spin orthogonality
    if sa != sb:
        return 0.0

    ang = dipole_angular_coefficient(la, ma, lb, mb, q)
    if abs(ang) < 1e-15:
        return 0.0

    rad = radial_dipole_integral(na, la, nb, lb, R_scale=R_scale)

    # Factor √(4π/3) for spherical dipole convention
    return np.sqrt(4 * np.pi / 3) * rad * ang


def many_body_dipole_matrix(sp_states, basis, eigenvectors, q=0, R_scale=1.0):
    """
    Dipole matrix elements between CI eigenstates.

    D[i,j] = ⟨Ψ_i| D_q |Ψ_j⟩

    where D_q = Σ_k r_q(k) is the one-body dipole operator summed over electrons.

    In second quantization over Slater determinants:
        ⟨IJ| D_q |KL⟩ = d_{IK}δ_{JL} - d_{IL}δ_{JK} + d_{JL}δ_{IK} - d_{JK}δ_{IL}

    where d_{ab} = ⟨a|r_q|b⟩ is the single-particle dipole element.
    """
    n_basis = len(basis)
    n_states = eigenvectors.shape[1]

    # Build one-body dipole matrix in spin-orbital basis
    n_sp = len(sp_states)
    d_1b = np.zeros((n_sp, n_sp))
    for a in range(n_sp):
        for b in range(n_sp):
            d_1b[a, b] = one_body_dipole_element(
                sp_states[a], sp_states[b], q, R_scale=R_scale
            )

    # Build dipole in Slater determinant basis
    D_slater = np.zeros((n_basis, n_basis))
    for row, (I, J) in enumerate(basis):
        for col, (K, L) in enumerate(basis):
            val = 0.0
            # One-body operator between antisymmetrized determinants:
            # ⟨IJ|_A  D  |KL⟩_A = d_IK δ_JL - d_IL δ_JK
            #                     + d_JL δ_IK - d_JK δ_IL
            if J == L:
                val += d_1b[I, K]
            if J == K:
                val -= d_1b[I, L]
            if I == K:
                val += d_1b[J, L]
            if I == L:
                val -= d_1b[J, K]
            D_slater[row, col] = val

    # Transform to CI eigenstate basis: D_CI = V^T × D_slater × V
    D_ci = eigenvectors.T @ D_slater @ eigenvectors
    return D_ci


def oscillator_strength(delta_E, dipole_sq):
    """
    Oscillator strength: f = (2/3) × ΔE × |⟨f|r|i⟩|²

    delta_E: energy difference in Hartree (positive)
    dipole_sq: |⟨f|r|i⟩|² summed over q = -1, 0, +1
    """
    return (2.0 / 3.0) * abs(delta_E) * dipole_sq


def transition_wavelength_nm(delta_E_hartree):
    """
    Convert energy difference in Hartree to wavelength in nm.

    λ = hc/ΔE

    1 Hartree = 27.211386 eV = 4.359744 × 10⁻¹⁸ J
    hc = 1239.8419 eV·nm

    So λ(nm) = 1239.8419 / (ΔE_Ha × 27.211386) = 45.5634 / ΔE_Ha
    """
    if abs(delta_E_hartree) < 1e-15:
        return np.inf
    return 45.563353 / abs(delta_E_hartree)


def classify_parity(eigenvector, basis, sp_states):
    """
    Determine parity of a CI eigenstate.

    Parity P = (-1)^{l1+l2} for each Slater determinant.
    For eigenstates with definite parity, all components should
    have the same parity (to numerical precision).

    Returns: +1 (even), -1 (odd), or 0 (mixed/undefined)
    """
    even_weight = 0.0
    odd_weight = 0.0
    for idx, (i, j) in enumerate(basis):
        l1 = sp_states[i][1]
        l2 = sp_states[j][1]
        p = (-1) ** (l1 + l2)
        w = eigenvector[idx] ** 2
        if p > 0:
            even_weight += w
        else:
            odd_weight += w
    if even_weight > 0.99:
        return +1
    elif odd_weight > 0.99:
        return -1
    else:
        return 0


def classify_spin(eigenvector, basis, sp_states):
    """
    Estimate total spin of a CI eigenstate.

    For two electrons, S_total = 0 (singlet) or 1 (triplet).
    Compute ⟨S²⟩ = S(S+1): singlet → 0, triplet → 2.

    S² = s₁² + s₂² + 2s₁·s₂ = 3/2 + 2s₁·s₂
    ⟨s₁·s₂⟩ depends on whether spins are aligned.
    """
    S2_expect = 0.0
    for row, (i, j) in enumerate(basis):
        si, sj = sp_states[i][3], sp_states[j][3]
        for col, (k, l) in enumerate(basis):
            sk, sl = sp_states[k][3], sp_states[l][3]
            c_row = eigenvector[row]
            c_col = eigenvector[col]
            if abs(c_row * c_col) < 1e-15:
                continue
            # S² matrix element between |ij⟩_A and |kl⟩_A
            # For two-electron system: ⟨S²⟩ = s1(s1+1) + s2(s2+1) + 2⟨s1·s2⟩
            # Direct: δ_ik δ_jl terms, Exchange: -δ_il δ_jk terms
            val = 0.0
            if i == k and j == l:
                val += 0.75 + 0.75  # s(s+1) for each electron
                # s1·s2 diagonal: s1z*s2z
                val += 2 * si * sj
            if i == l and j == k:
                val -= 0.75 + 0.75
                val -= 2 * si * sj
            # Off-diagonal s1·s2 (spin flip terms)
            # s₁₊s₂₋ + s₁₋s₂₊ : these connect |↑↓⟩ ↔ |↓↑⟩
            # For determinant |ij⟩ → |kl⟩ via spin exchange:
            ni, li, mi = sp_states[i][:3]
            nj, lj, mj = sp_states[j][:3]
            nk, lk, mk = sp_states[k][:3]
            nl, ll, ml = sp_states[l][:3]
            # Spatial parts must match for spin-flip contributions
            if (ni, li, mi) == (nk, lk, mk) and (nj, lj, mj) == (nl, ll, ml):
                if si != sk and sj != sl and si == -sk:
                    val += 2 * 0.5  # ⟨↑|s₊|↓⟩⟨↓|s₋|↑⟩ = 1/2 each, factor 2
            if (ni, li, mi) == (nl, ll, ml) and (nj, lj, mj) == (nk, lk, mk):
                if si != sl and sj != sk and si == -sl:
                    val -= 2 * 0.5
            S2_expect += c_row * c_col * val
    # S(S+1): singlet=0, triplet=2
    S = (-1 + np.sqrt(1 + 4 * S2_expect)) / 2 if S2_expect > -0.1 else 0
    return round(2 * S + 1)  # multiplicity: 1=singlet, 3=triplet


# ── Multi-electron approximate methods (Slater shielding) ──────────────

# Aufbau filling order: (n, l) sorted by (n+l, n)
FILLING_ORDER = [
    (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (3, 2), (4, 1),
    (5, 0), (4, 2), (5, 1), (6, 0), (4, 3), (5, 2), (6, 1), (7, 0),
]

MAX_OCCUPATION = {0: 2, 1: 6, 2: 10, 3: 14}

EFFECTIVE_N = {1: 1.0, 2: 2.0, 3: 3.0, 4: 3.7, 5: 4.0, 6: 4.2, 7: 4.4}

ORBITAL_LABEL = {0: 's', 1: 'p', 2: 'd', 3: 'f'}

# Slater groups in order from inner to outer
SLATER_GROUPS = [
    [(1, 0)],
    [(2, 0), (2, 1)],
    [(3, 0), (3, 1)],
    [(3, 2)],
    [(4, 0), (4, 1)],
    [(4, 2)],
    [(4, 3)],
    [(5, 0), (5, 1)],
    [(5, 2)],
    [(5, 3)],
    [(6, 0), (6, 1)],
    [(6, 2)],
    [(7, 0), (7, 1)],
]

_NL_TO_GROUP = {}
for _gi, _grp in enumerate(SLATER_GROUPS):
    for _nl in _grp:
        _NL_TO_GROUP[_nl] = _gi


def ground_state_config(Z):
    """Return ground-state electron configuration as {(n, l): count}."""
    config = {}
    remaining = Z
    for n, l in FILLING_ORDER:
        if remaining <= 0:
            break
        occupy = min(remaining, MAX_OCCUPATION[l])
        config[(n, l)] = occupy
        remaining -= occupy
    return config


def config_string(config):
    """Human-readable configuration string like '1s² 2s² 2p⁶'."""
    superscripts = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
    parts = []
    for n, l in FILLING_ORDER:
        if (n, l) in config:
            count = config[(n, l)]
            parts.append(f'{n}{ORBITAL_LABEL[l]}{str(count).translate(superscripts)}')
    return ' '.join(parts)


def slater_zeff(Z, config, target_nl):
    """Effective nuclear charge for orbital target_nl using Slater's rules.

    Parameters
    ----------
    Z : int — nuclear charge
    config : dict — {(n, l): electron_count}
    target_nl : tuple — (n, l) of the orbital
    """
    n_t, l_t = target_nl
    g_t = _NL_TO_GROUP[target_nl]
    sigma = 0.0

    for (n, l), count in config.items():
        if (n, l) not in _NL_TO_GROUP:
            continue
        g = _NL_TO_GROUP[(n, l)]

        if g > g_t:
            continue  # outer electrons don't shield

        if g == g_t:
            # Same Slater group: 0.35 (0.30 for 1s)
            n_same = count - (1 if (n, l) == target_nl else 0)
            sigma += n_same * (0.30 if g_t == 0 else 0.35)
        elif l_t <= 1:
            # Target is s/p: (n-1) shell → 0.85, deeper → 1.00
            if n == n_t - 1:
                sigma += count * 0.85
            else:
                sigma += count * 1.00
        else:
            # Target is d/f: all inner → 1.00
            sigma += count * 1.00

    return Z - sigma


def slater_orbital_energy(Z, config, target_nl):
    """One-electron orbital energy (Hartree) using Slater's rules."""
    n = target_nl[0]
    z_eff = slater_zeff(Z, config, target_nl)
    n_star = EFFECTIVE_N[n]
    return -z_eff ** 2 / (2 * n_star ** 2)


def slater_total_energy(Z, config=None):
    """Total electronic energy (Hartree) from Slater's rules."""
    if config is None:
        config = ground_state_config(Z)
    E = 0.0
    for (n, l), count in config.items():
        E += count * slater_orbital_energy(Z, config, (n, l))
    return E


def slater_ionization_energy(Z):
    """First ionization energy (Hartree) via total energy difference."""
    config_N = ground_state_config(Z)

    # Remove one electron from the outermost orbital
    config_Nm1 = dict(config_N)
    outermost = None
    for n, l in reversed(FILLING_ORDER):
        if (n, l) in config_Nm1 and config_Nm1[(n, l)] > 0:
            outermost = (n, l)
            break
    config_Nm1[outermost] -= 1
    if config_Nm1[outermost] == 0:
        del config_Nm1[outermost]

    E_N = slater_total_energy(Z, config_N)
    E_Nm1 = slater_total_energy(Z, config_Nm1)
    return E_Nm1 - E_N


def expected_radius(n, l, Z_eff):
    """Expected radius ⟨r⟩ for hydrogen-like orbital (atomic units)."""
    return (3 * n ** 2 - l * (l + 1)) / (2 * Z_eff)

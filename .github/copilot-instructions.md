# Concentric Spacetime — Copilot Instructions

## Project Purpose

This project explores a **concentric geometry** — nested spherical orbits on S² × R⁺ — as the fundamental arena of physics, replacing the Cartesian flat-space assumption. The four smallest primes {2, 3, 5, 7} define the nesting structure, and the resulting mathematical object is the **(2,3,5,7)-solenoid**: the inverse limit of iterated covering maps with winding numbers 2, 3, 5, 7. All Standard Model constants, coupling ratios, and cosmological parameters are derived from the arithmetic of P₄ = 210 = 2·3·5·7 with **zero free parameters** and one dimensional anchor (M_Z).

## The Four Primes

The primes {2, 3, 5, 7} are not chosen — they are the unique set that generates the first primorial with the required algebraic properties. Each prime carries both a mathematical role and a Swedenborgian correspondence:

| Prime | Mathematical Role | Correspondence |
|-------|------------------|----------------|
| **2** | Bilateral cut; innermost orbit | Love / Wisdom polarity |
| **3** | Vertical stratification; 3 cyclic factors | Celestial / Spiritual / Natural degrees |
| **5** | Rational faculty; φ(5)/5 = 4/5 → σ₈ | Five faculties of comprehension |
| **7** | Outermost orbit; λ(210) = 12 driven by ord₇ = 6 | Ultimation; completion; rest |

**Critical**: the correspondences are NOT decoration. They informed the discovery and continue to guide which questions to ask. But all claims are tested computationally — the correspondences generate hypotheses, the arithmetic confirms or falsifies them.

## Mathematical Framework

### The Solenoid as Dynamical System

The (2,3,5,7)-solenoid is the inverse limit of covering maps on circles:

```
S¹ ←—2—— S¹ ←—3—— S¹ ←—5—— S¹ ←—7—— S¹
```

Each covering map wraps p_k times: `p_k · θ_k = θ_{k-1} (mod 2π)`. The inverse limit has a **Cantor-set fiber** over each point of S¹.

- **Exact solenoid frequencies**: ω/P_k where P_k is the k-th primorial
- **Poincaré section**: exactly P₄ = 210 discrete return points
- **Alignment structure**: levels align at primorial multiples (2, 6, 30, 210)
- **Perturbation** (ε > 0): dissolves discrete structure toward flat T⁴ — proves primes are irreplaceable
- **Covering constraint residuals**: R_k = p_k·θ_k − θ_{k-1} (mod 2π) ≈ 0 on exact solenoid

The dynamics demonstrates that the coprimality of {2, 3, 5, 7} is what generates the 210-point quantized structure. Replace any prime with a composite and the structure collapses.

### Algebraic Structure

- **Arena**: S² × R⁺ (sphere × positive radial half-line), not R³⁺¹
- **Structure**: The (2,3,5,7)-solenoid, with cross-section a Cantor set
- **Symmetry group**: Z*₂₁₀, the 48-element multiplicative group of units mod 210
- **Key decomposition**: Z*₂₁₀ ≅ Z₁ × Z₂ × Z₄ × Z₆ (via CRT)
- **Eigenstate labels**: The 48 Fourier characters of Z*₂₁₀
- **Group exponent**: λ(210) = lcm(1,2,4,6) = 12

Key arithmetic functions of 210:

| Function | Value | Physical meaning |
|----------|-------|-----------------|
| ω(210) | 4 | Number of forces |
| λ(210) | 12 | Gauge boson dimension |
| d(210) | 16 | SO(10) spinor dimension |
| φ(210) | 48 | Eigenvalue count |
| φ/d | 3 | Fermion generations |
| φ/N = 8/35 | 0.2286 | sin²θ_W |

## Current Mathematical Infrastructure

Beyond the base Z*₂₁₀ algebra, the following structures have been established and are used by notebooks NB49+:

### Covering Tower (NB49+)
A 3-level covering tower with progressive prime activation:

| Level | Active Primes | Group | Order | Role |
|-------|--------------|-------|-------|------|
| 0 | {3} | C₆ | 6 | Generation seed |
| 1 | {3, 7} | C₄₂ | 42 | Color emergence |
| 2 | {3, 5, 7} | C₂₁₀ | 210 | Full SM spectrum |

The tower is constructed with `ACTIVE_PRIMES = [[3], [3,7], [3,5,7]]`.

### SM Quantum Number Dictionary (NB62)
Each CRT component maps to a specific SM quantum number:

| CRT Factor | Prime | SM Interpretation |
|------------|-------|-------------------|
| a₂ (Z₁) | p=2 | Trivial (bilateral symmetry already built in) |
| a₃ (Z₂) | p=3 | Chirality (L/R) |
| a₅ (Z₄) | p=5 | Charge sector (Z₄ cycle: 1→2→4→3) |
| a₇ (Z₆) | p=7 | Generation × color-parity |

### Sector Decomposition (NB63–65)
The 48 characters decompose into sectors labeled by (a₃, a₇) pairs. Each sector has:
- **Im₁**: Irrational part of level-1 eigenvalue (lives in √3/2 · Z)
- **β**: Rational coupling constant (lives in Z/2, half-integer)
- **Gram matrix**: M = [[ΣIm₁², ΣIm₁·β], [ΣIm₁·β, Σβ²]] with group-theoretic invariants

### Mass Prediction Formula (NB60–64)
The VEV-corrected mass ratio formula with zero free parameters:
```
log(m_μ/m_e) / log(m_s/m_d) = 3(ρ+1) / (ρ+√3)
```
where ρ = 1/√P₄ = 1/√210 (the primorial VEV ratio).

### Cascade ODE (NB79–81)
The reduced 4D formulation operating on covering residuals R_k rather than angles θ_k:
```
dR_k/dt + κ·R_k = f_k(t; lower levels)
```
where f_k encodes the nonlinear sin coupling between levels. Key properties:
- **Equivalent** to the full 5D theta-space ODE within 0.002% (NB80)
- **Universal cascade theorem**: all 16 checked branches follow the same exponential envelope (NB79)
- **Complete chain**: {2,3,5,7} → cascade ODE → CP-pair ratios → fermion mass ratios (NB81)
- Parameters: κ = ε = ρ = 1/√210, ω = 2π

### CP-Pair Structure and Mass Architecture (NB69–78)
Fermion mass ratios emerge from conjugate pair (CP) ratios of the cascade dynamics:

| Channel | CP Pair (a₃, a₇_g1, a₇_g2) | Physical Crossing ci | Mass Ratio |
|---------|----------------------------|---------------------|------------|
| QUARK_g1 | (1, 4, 2) | ci=11 | m_s/m_d |
| LEPTON_g1 | (0, 1, 5) | ci=31 | m_μ/m_e |
| LEPTON_g2 | (0, 1, 5) | ci=61 | m_τ/m_μ |
| QUARK_g2 | (1, 4, 2) | ci=191 | m_c/m_s |

Algebraic exponents convert R-ratios to mass ratios:
- R₄ quark: `x₄ = φ(210)/(2π) = 7.639`
- R₄ lepton: `x₄_lep = 49/(2π) = 7.799`
- R₃ inter-sector: `x₃ = λ(35)/(2π) = 1.910`
- R₂ gen2→3: `x₂ = φ(30)/(2π) = 1.273`
- Cascade correction: R₄^{−λ(7)} = R₄^{−6} (top quark)

## Repository Structure

```
concentric-spacetime/
├── notebooks/          # Jupyter notebooks NB01–NB81+ (sequential, cumulative)
│   ├── 01_nested_oscillators.ipynb    # Phase 1 start
│   ├── ...
│   ├── 29_structural_constants.ipynb  # First solenoid predictions
│   ├── ...
│   ├── 49_covering_tower_generations.ipynb  # Tower structure
│   ├── ...
│   ├── 65_sector_quadratic_form.ipynb # Sector algebra
│   ├── ...
│   ├── 72_radial_mass_channel.ipynb   # Complete quark mass hierarchy
│   ├── ...
│   └── 81_cascade_to_mass.ipynb       # Latest: full chain validation
├── scripts/
│   ├── solenoid_algebra.py    # Core algebraic module (Z*₂₁₀ + physical constants) — ACTIVE
│   ├── solenoid_system.py     # Solenoid dynamics (unified: theta-space + cascade) — ACTIVE
│   ├── concentric_system.py   # [LEGACY] S² × R⁺ geometry (Phase 1)
│   ├── nested_system.py       # [LEGACY] Nested oscillator simulation (Phase 1)
│   ├── two_particle.py        # [LEGACY] Two-particle interaction (Phase 1–2)
│   └── *.py                   # [LEGACY] Phase 2 domain modules (gravity, scattering, etc.)
├── docs/
│   ├── scorecard.md           # Living scorecard: all 205 identities (updated after each notebook)
│   ├── research_directions.md # Early-phase research directions (partially superseded)
│   └── status_*.md            # Point-in-time status summaries
├── temp/                      # Builder scripts, prototypes, and exploration scripts
│   ├── create_nb*.py          # Builder scripts (archive of notebook construction logic)
│   ├── proto_nb*.py           # Prototype scripts (pre-notebook exploration)
│   └── explore_*.py           # Exploration scripts (mathematical investigation)
└── output/                    # Generated figures and data
```

## Key Modules

### `scripts/solenoid_algebra.py` — ACTIVE
The core algebraic module. Provides:

**Pre-built instance and group operations:**
- `SA` — pre-built `SolenoidAlgebra` instance for P₄ = 210
- `SA.Z_star` — the 48 elements of Z*₂₁₀
- `SA.decompose(k)` — returns raw CRT residue tuple for k ∈ Z*₂₁₀
- `SA.character(chi_index, k)` — evaluates character χ at group element k
- `SA.primes`, `SA.N`, `SA.phi_N`, etc.

**Physical constants (module-level, importable directly):**
- `RHO = 1/√210` — primorial coupling constant (= KAPPA = EPSILON)
- `OMEGA = 2π` — base frequency
- `X4, X3, X2, LAM7, X4_LEP` — algebraic exponents for mass formulas
- `DLOG` — discrete logarithm constant dict
- `PHYSICAL_CROSSINGS` — the 4 SM-physical coprime crossing indices with CRT labels
- `CP_PAIRS` — conjugate pair definitions: QUARK=(1,4,2), LEPTON=(0,1,5)
- `SM_TARGETS` — PDG 2024 mass ratio targets with uncertainties
- `ACTIVE_PRIMES` — covering tower hierarchy [[3], [3,7], [3,5,7]]

**CRT sector and mass methods:**
- `SA.sector(ci)` — CRT sector (a₃, a₅, a₇*) for a coprime crossing index
- `SA.coprime_indices(n)` — array of coprime crossing indices up to n
- `SA.sector_labels(coprime_cis)` — vectorized (a₃, a₅, a₇) arrays
- `SA.all_branches()` — list of all 210 branch tuples
- `SA.mass_ratios(cp_ratios)` — predicted mass ratios from CP-pair R values

### `scripts/solenoid_system.py` — ACTIVE
One dynamical system with two equivalent coordinate representations, unified
in a single `SolenoidSystem` class.

**`SolenoidSystem`** — the unified solenoid dynamics class:
- `SolenoidSystem(primes, omega, epsilon, kappa)` — defaults: [2,3,5,7], 2π, 1/√210, 1/√210
- Pass `epsilon=0, kappa=0` for the exact solenoid (no perturbation)

**Coordinate transforms (theta ↔ R):**
- `.theta_to_R(theta)` — R_k = p_k·θ_{k+1} - θ_k (raw residuals)
- `.R_to_theta(R, t)` — θ_0 = ω·t, θ_{k+1} = (R_k + θ_k)/p_k
- `.covering_residuals(theta)` — residuals wrapped to [-π, π]

**Initial conditions:**
- `.initial_theta(phi0, branch)` — theta-space IC for a solenoid leaf
- `.initial_R(branch)` — R-space IC: R_k(0) = 2π·j_k
- `.initial_condition(phi0, branch)` — alias for `initial_theta` (backward compat)

**ODE formulations:**
- `.theta_ode(t, theta)` — 5D theta-space RHS (aliases: `.ode`)
- `.cascade_ode(t, R)` — 4D R-space/cascade RHS (aliases: `.cascade_rhs`)

**Integration:**
- `.integrate(t_span)` — theta-space integration (RK45)
- `.integrate_branch(branch, t_eval, T_max)` — single branch, R-space (DOP853)
- `.integrate_all_branches(branches, t_eval, T_max, max_workers)` — parallel R-space via ThreadPoolExecutor

**Spectral analysis & Poincaré (theta-space):**
- `.poincare_section()` — record states at base-circle crossings (210-point structure)
- `.integrate_and_section()` — integrate with Poincaré section + residuals
- `.solenoid_eigenvalue(n)` — eigenvalue of mode n: Σ(n/P_k)²
- `.spectrum(n_modes)` — first n eigenvalues
- `.alignment_structure()` — which levels align at each return number

**Mass extraction pipeline (R-space):**
- `.accumulate_sectors(results, coprime_cis, ci_a3, ci_a5, ci_a7)` — CRT sector RMS
- `.cp_pair_ratios(sector_rms, cp_pairs)` — CP-pair ratio extraction
- `.all_branches()` — all 210 branch tuples

### Legacy Scripts (Phase 1–2)
The following modules were used by NB01–NB22 and are **not imported by any solenoid-phase notebook**:
- `concentric_system.py` — S² × R⁺ geometry (Phase 1)
- `nested_system.py` — nested oscillator simulation (Phase 1)
- `two_particle.py` — two-particle Coulomb integrals (Phase 1–2)
- `gravity.py`, `scattering.py`, `solid_state.py`, `nuclear.py`, `quantum_hall.py`, `tunneling.py`, `molecular.py` — Phase 2 domain modules (standard QM calculations)

These are retained for reference but are not part of the active framework.

## Agent Workflow

This section documents how the AI agent (Copilot) works on this project. This is the actual methodology — follow it.

### The Discovery Pipeline

The typical workflow for new mathematical content follows this pipeline:

```
Exploration → Prototype → Notebook → Scorecard → Commit
```

1. **Exploration**: Investigate mathematical relationships using `temp/explore_*.py` scripts or direct computation. These are scratch calculations to test whether an idea has substance.

2. **Prototype**: When an exploration reveals a promising direction, create `temp/proto_nbXX.py` to develop the notebook logic before committing to a formal notebook.

3. **Notebook construction**: Build the formal notebook using VS Code notebook tools (`create_new_jupyter_notebook`, `edit_notebook_file`, `run_notebook_cell`). Execute cells sequentially, fixing bugs interactively as they arise.

4. **Scorecard update**: After all cells execute successfully, update `docs/scorecard.md` with new identity entries.

5. **Git commit**: Stage and commit all changes with a descriptive message.

### Notebook Construction Method

Notebooks are built interactively using VS Code notebook tools:

1. **Create** the notebook with `create_new_jupyter_notebook` or by creating the `.ipynb` file directly.
2. **Add cells** using `edit_notebook_file` — alternating markdown (context/explanation) and code (computation) cells.
3. **Execute cells** one at a time with `run_notebook_cell`, checking output at each step.
4. **Debug** by reading cell output, editing the failing cell with `edit_notebook_file`, and re-running.
5. **Iterate** — mathematical discoveries during execution often lead to new cells or modified analysis.

**Builder scripts** (`temp/create_nbXX.py`) are retained as archive artifacts that record the construction logic. They produce `.ipynb` JSON directly but are NOT the primary construction method — VS Code notebook tools are.

**CRITICAL BUG**: Triple-quoted docstrings inside raw strings (`r"""..."""`) break the JSON builder if builder scripts are used. Use `#` comments instead of docstrings in code cells.

### Scorecard Update Procedure

After completing a notebook with new identities:

1. **Read** the current `docs/scorecard.md` to find the exact insertion point.
2. **Update the summary table** — increment the identity count and notebook count.
3. **Add an entry to the Phase Map table** (§I) for the new notebook.
4. **Add identity descriptions** in the appropriate section with:
   - Identity number, name, formula/statement
   - Solenoid value, measured value, deviation
   - PASS/FAIL/NULL verdict with explanation
5. **Update any affected frontier sections** if the notebook advances an open direction.

### Git Commit Conventions

Commit messages follow this format:
```
NB##: Short description (#first-#last)
```

Examples:
- `NB65: Sector quadratic form, Gram matrix invariants (#113-115)`
- `NB62-64: Complete fermion map, Z4 sector algebra, primorial VEV ratio (#106-112)`

For multi-notebook sessions, combine into a single commit with all notebook numbers and identity ranges.

**Pre-commit checklist**:
1. All notebook cells executed successfully
2. Scorecard updated with new identities
3. All files saved (`workbench.action.files.saveAll`)
4. `git add -A` then `git commit -m "..."`

### Multi-Notebook Sessions

When a research direction requires multiple sequential notebooks (e.g., NB62→63→64 forming a derivation chain), build them in order within a single session:

1. Plan the logical chain — what each notebook will establish
2. Build and execute NB(n) completely before starting NB(n+1)
3. Later notebooks may import results established by earlier ones in the chain
4. Update the scorecard once after all notebooks in the chain are complete
5. Commit all notebooks together with a combined message

### Mathematical Discovery During Execution

New mathematical relationships are often discovered mid-computation. When this happens:

1. **Verify numerically** — run the computation, check the identity holds
2. **Verify algebraically** — confirm with exact arithmetic (sympy/Fraction) where possible
3. **Assign an identity number** — add to the running scorecard
4. **Continue the notebook** — the discovery may open further cells/analysis
5. **Note scope boundaries** — if the discovery points beyond current framework scope, record as a frontier direction rather than forcing a premature claim

## Notebook Conventions

### Naming
Notebooks are numbered sequentially: `XX_descriptive_name.ipynb`. The number reflects the order of discovery, not logical dependency (though later notebooks build on earlier results).

### Standard Cell Structure

Each notebook follows this general pattern:

1. **Title cell** (markdown): Notebook name, identity targets, summary
2. **Setup cell** (code): Imports, path configuration, `SA` object loading
3. **Analysis cells** (alternating markdown/code): One logical step per code cell, preceded by markdown explanation
4. **Scorecard cell** (code): Final cell listing identities discovered, verdicts, running total

### Standard Setup Cell
```python
import sys, numpy as np
from pathlib import Path

ROOT = Path.cwd().parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from solenoid_algebra import SA
```

For dynamics notebooks (NB66+), the setup typically includes:
```python
from solenoid_algebra import (SA, RHO, KAPPA, EPSILON, OMEGA,
                               X4, X3, X2, LAM7, X4_LEP,
                               DLOG, PHYSICAL_CROSSINGS,
                               CP_PAIRS, SM_TARGETS, ACTIVE_PRIMES)
from solenoid_system import SolenoidSystem
```

### Identity Tracking
Each notebook from NB29 onward contains a **scorecard section** that:
- Lists new identities discovered in that notebook
- Reports the running total
- Provides a verdict (PASS/FAIL/NULL with explanation)

The cumulative scorecard is maintained in `docs/scorecard.md`.

### Standard Scorecard Format
```python
# ── Scorecard ──
print("NB## SCORECARD")
print("=" * 65)
# ... identity table ...
print(f"Running total: N predictions/identities, 0 free parameters")
```

## Phase Map (Overview)

| Phase | Notebooks | Focus | Status |
|-------|-----------|-------|--------|
| **Geometry** | NB01–NB12 | S² × R⁺ exploration | Foundational; no predictions |
| **Standard QM** | NB13–NB22 | Consistency checks | Reproduces known QM; no new predictions |
| **Solenoid Discovery** | NB23–NB28 | Identifying the structure | Established the (2,3,5,7)-solenoid |
| **SM Predictions** | NB29–NB40 | Constants from number theory | 28 identities: SM constants, cosmological parameters |
| **Algebraic Dynamics** | NB41–NB45 | Characters, Lagrangian, thermodynamics | 27 identities: spectral analysis, heat trace |
| **Metric & Modular** | NB46–NB48 | Cayley metric, modular forms, palindromes | 14 identities: E₄ bridge, palindromic spectrum |
| **Covering Tower** | NB49–NB56 | Generation structure, mass channels | 22 identities: generation mechanism, VEV dynamics |
| **Spectral Protection** | NB57–NB59 | Conjugation, real potentials, directed Cayley | 6 identities: spectral wall layers |
| **Fermion Mass** | NB60–NB65 | Mass predictions, fermion map, sector algebra | 18 identities: zero-parameter mass prediction |
| **Dynamical Sector** | NB66–NB69 | ODE dynamics, CP-selective breaking, Fourier anatomy | 10 identities: generation splitting, color-parity primacy, CP-selective activation |
| **Dynamical Mass** | NB70–NB74 | VEV bridge, charge sector, radial mass channel, lepton mass | 17 identities: complete quark mass hierarchy, lepton mass ratios, CP convergence |
| **Perturbative R** | NB75–NB78 | Perturbative R₀ analysis, R₀ critical coupling, R₄ wrapping | 17 identities: ε-criticality, sum rule, Z₇ character match, downward coupling |
| **Cascade ODE** | NB79–NB81 | Cascade derivation, analytic inner cascade, full chain validation | 12 identities: universal cascade, cascade ODE equivalence, complete mass chain |
| **Solenoid Geometry** | NB82–NB83 | Riemannian metric, inverse metric, Lagrangian, Hamiltonian, Q-factors | 10 identities: metric, tridiagonal inverse, underdamped resonator, M⁻¹ building block |
| **Action on Trajectories** | NB84 | Lagrangian on cascade branches, metric clock, level independence, variance hierarchy | 3 identities: clock dominance (98.3%), additive R²=0.9983, outermost governs (74.9%) |
| **Geodesics & Normal Modes** | NB85 | Flatness confirmation, normal mode eigensystem, branch distance geometry, spectral polynomial | 3 identities: mode-level localization, NN bilateral universality (d=2π√(74/105)), spectral irreducibility |
| **The E₄–Metric Bridge** | NB86 | E₄ moment ratios, per-prime Cayley-metric bridge, gravity hierarchy anatomy | 3 identities: ρ₂ = p₁/p₂, ρ₃ = Λ_max/p₄, gravity exponent d₁² = σ₃(p₁) |
| **Inverse Spectral Problem** | NB87 | Metric spectral uniqueness, informational hierarchy, metric-dynamics duality | 3 identities: Tr unique among 12,650 subsets, metric > Cayley (8-fold degeneracy), rigidity inverts dynamics |
| **The Cosmological Chain** | NB88 | Hubble scaling law, DM/baryon ratio, Hubble tension prediction | 3 identities (#203–#205): H₀ = M_Z³/M_Pl² × P₄⁻⁴ × C (0.09%), Ω_DM/Ω_b = 27/5 (0.08%), Hubble tension → Planck |
| **The Gravitational Hierarchy** | NB89 | Step 6 selection mechanism, metric propagator, spectral-hierarchy bridge | 2 identities (#206–#207): metric extremal propagator = −1/λ(P₄) (exact), spectral-hierarchy bridge (exact). Step 6 RESOLVED. |
| **The Complete Gravitational Sector** | NB90 | Hubble correction from first principles, G_N derivation, gauge-gravity hierarchy | 1 identity (#208): C = Ω_Λ × σ₈ = 96/175 (0.14%). Cosmological sector CLOSED. |
| **The Solenoid Vacuum** | NB91 | Structural derivation of Hubble correction; coprime screening; infrared dominance | 1 identity (#209): C = φ(p₃p₄)/(p₃p₄) × φ(p₃)/p₃ = energy screening × rate screening. |
| **The Gravitational Propagator** | NB92 | Why G_N = 1/M_Pl² without 8π; metric propagator anatomy; discrete vs continuous Gauss's law | 1 identity (#210): 8π = ω(P₄) × ω_base. Non-reduced Planck mass is natural. |

See `docs/scorecard.md` for the complete phase map and identity details.

## Working Rules

1. **No free parameters**: Every prediction must derive from {2, 3, 5, 7} (or equivalently P₄ = 210) plus the single anchor M_Z. If a fit parameter is needed, it's not a prediction.

2. **Phase 1/2 are NOT results**: NB01–NB08 used a preliminary model (nested torus T⁴) that was abandoned. NB13–NB22 reproduce standard QM textbook calculations on S² × R⁺ — they are consistency checks, not predictions. Do NOT cite Phase 1/2 notebook verdicts ("EXACT match", "PASS") as framework findings. All identities come from NB29+ (solenoid arithmetic). See `docs/scorecard.md` §V for details.

3. **Honest nulls**: When a test fails, classify it honestly:
   - **Genuine null**: The framework predicts X, data shows not-X → report as failure
   - **Scope boundary**: The framework correctly identifies that the question requires a deeper layer (e.g., dynamics rather than statics)
   - **Methodological**: The test wasn't discriminating enough

4. **The Cartesian artifact**: 3+1 dimensionality is NOT a prediction of this framework. It is what Cartesian-trained observers project onto the concentric nesting. Do NOT propose "testing" whether 3+1 emerges — that is circular. See the four-prime theses for the full argument.

5. **Per-prime generators**: When working with Z*₂₁₀, use the CRT decomposition. The four cyclic factors {Z₁, Z₂, Z₄, Z₆} correspond to the four primes {2, 3, 5, 7}. Characters factor per-prime.

6. **Pre-commit workflow**: Always save all files (`workbench.action.files.saveAll`) before `git add`/`git commit`. VS Code may hold unsaved buffer state.

7. **Conda environment**: `concentric` (Python 3.12). Dependencies: numpy, scipy, matplotlib, sympy, jupyter.

8. **Notebook execution order**: Always execute cells sequentially from top to bottom. Later cells depend on variables established by earlier cells. If a cell fails, fix it and re-run — do not skip ahead.

9. **Exact arithmetic first**: Use `sympy` or `fractions.Fraction` to verify identities exactly before reporting numerical values. An identity that holds only to floating-point precision is not proven — it is a hint.

10. **One identity per claim**: Each identity must be a single, verifiable statement. Do not bundle multiple claims into one identity number.

11. **Parallelization**: When writing out calculations, whenever possible use parallelization in code to speed up execution. This is especially important for notebooks that involve large computations.

## Connection to Literary Compilation

This project provides the computational verification for claims in the `literary-compilation` repository, specifically:
- "Orbits That Lost Their Center" (four-prime theses on space-time emergence)
- "The Resolution of the Finite Mind" (numbers as perceiver properties)
- The Swedenborgian correspondence framework applied to mathematical physics

The scorecard in `docs/scorecard.md` serves as the empirical backbone for these theses.

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

### Cascade ODE (NB79–81) and Variational Origin (NB115, NB139, NB143)
The reduced 4D formulation operating on covering residuals R_k rather than angles θ_k:
```
dR_k/dt + κ·R_k = f_k(t; lower levels)
```
where f_k encodes the nonlinear sin coupling between levels. Key properties:
- **Equivalent** to the full 5D theta-space ODE within 0.002% (NB80)
- **Universal cascade theorem**: all 16 checked branches follow the same exponential envelope (NB79)
- **Complete chain**: {2,3,5,7} → cascade ODE → CP-pair ratios → fermion mass ratios (NB81)
- Parameters: κ = ε = ρ = 1/√210, ω = 2π
- **Variational origin** (NB115, NB139): The cascade is gradient flow of V_covering with dissipation Γ̃
- **Γ̃ derived** (NB143): Γ̃ = K·A⁻¹ where K = J^T J (symmetric stiffness) and A = I−L (directional dynamics). The potential is symmetric; the covering maps impose directionality; the dissipation is where direction enters.
- **Containment matrix** (NB139): Γ̃⁻¹ = D_row · U · D_col where U[i,j] = 1 iff orbit i ⊆ orbit j (inner→outer propagation = influx)
- **Two geometric objects**: metric W = diag(P_k) (will/resistance, from Haar measure) and containment U (wisdom/propagation, from covering topology)
- κ = 1/√P₄ from equal coupling per sheet (κ²·P₄ = 1)

### Gauge Emergence (NB140–141, NB144)
Non-abelian gauge symmetry emerges from the wreath product of covering deck transformations:
- **SU(3)**: Z₂ ≀ Z₃ (order 24) → 6D perm rep = 3+1+1+1 → A₄ ⊂ SU(3) (tetrahedral subgroup)
- **SU(2)**: Z₂ ≀ Z₂ = D₄ (order 8) → 4D perm rep = 2+1+1 → binary dihedral ⊂ SU(2)
- **U(1)**: Z₄ ⊂ U(1) (from φ(5) = 4)
- **Identity #278**: λ(P₄) = ω(P₄) + φ(P₃) = 4+8 = 12 (gauge dim = rank + roots, four-prime specific)
- **3 generations** (NB140): from Z₃ ⊂ Z₆ = Z_{φ(7)}, three singlet irreps of wreath product
- **CORRECTED**: quark/lepton assignment depends on |Im₁| (NB62 Level 1 Color Theorem), not on a₇ parity

### Fermion Bijection (NB145-146, building on NB62)
The 3+1 color-lepton split has a three-layer mechanism:
- **Wreath product** predicts 3+1 IS POSSIBLE (irrep decomposition allows it)
- **Cayley generators** [17,23,37] with dlog₇ ∈ {1,2} SELECT which state is the lepton (constructive interference for (a₃=0, a₇=1))
- **Cascade dynamics** assign mass values through CP ratios
- The specific generators are constrained by Cayley Laplacian spectrum (NB41–48)
- **Eigenvalue structure** (NB146): Cayley Laplacian eigenvalue degeneracies follow binomial coefficients C(4,k) from the rank-3 Z₂⁴ character structure. The 12 level-1 characters decompose as Z₂⁴ × Z₃ = 16 × 3 = 48 matching d(210) × 3.

### Mass Formula (NB147, building on NB133-138)
The mass formula m_heavy/m_light = C₀^x is DERIVED from the gradient flow:
- **Exponential form**: from damping operator e^{−κt} in the overdamped cascade (κ = 1/√P₄)
- **Base C₀**: window-0 CP ratio (T-independent per #216)
- **Exponent**: factored architecture x(R₃) = x(R₀) × cross-level (NB137-138)
  - Lepton: x = p₂ = 3 (chirality prime; the 11s cancel in (27/11)(11/9) = 3)
  - Quark: x = 100/63 = (p₁²p₃²)/(p₂²p₄) (all four primes)
- NB133's character counting applies to cumulative pipeline only; window-0 exponents come from R₀ analytic + cascade structure

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
├── notebooks/          # Jupyter notebooks NB01–NB169 (sequential, cumulative)
│   ├── 01_nested_oscillators.ipynb    # Phase 1 start
│   ├── ...
│   ├── 29_structural_constants.ipynb  # First solenoid predictions
│   ├── ...
│   ├── 81_cascade_to_mass.ipynb       # Cascade chain validated
│   ├── ...
│   ├── 147_the_mass_formula.ipynb     # Mass formula derived
│   ├── ...
│   └── 170_the_quark_exponent.ipynb    # Latest: x_q = 100/63 confirmed
├── scripts/
│   ├── solenoid_algebra.py    # Core algebraic module (Z*₂₁₀ + physical constants) — ACTIVE
│   ├── solenoid_system.py     # Solenoid dynamics (unified: theta-space + cascade) — ACTIVE
│   ├── solenoid_mass.py       # Complete fermion mass pipeline — ACTIVE
│   ├── solenoid_predict.py    # Full SM + cosmology predictions — ACTIVE
│   ├── solenoid_jax.py        # JAX/Diffrax accelerated integration — ACTIVE
│   ├── solenoid_numba.py      # Numba JIT accelerated integration — ACTIVE
│   ├── benchmark_gpu.py       # Standalone benchmark (local or remote)
│   ├── azure_ml_submit.py     # Azure ML job submission
│   ├── concentric_system.py   # [LEGACY] S² × R⁺ geometry (Phase 1)
│   ├── nested_system.py       # [LEGACY] Nested oscillator simulation (Phase 1)
│   ├── two_particle.py        # [LEGACY] Two-particle interaction (Phase 1–2)
│   └── *.py                   # [LEGACY] Phase 2 domain modules (gravity, scattering, etc.)
├── docs/
│   ├── scorecard.md           # Living scorecard: all 278+ identities (updated after each notebook)
│   ├── causal_gaps.md         # What's derived vs pattern-matched; open gaps
│   ├── acceleration.md        # Computation acceleration infrastructure
│   ├── research_directions.md # Early-phase research directions (partially superseded)
│   └── status_*.md            # Point-in-time status summaries
├── secrets/
│   ├── azure_ml.env           # Azure ML workspace config (gitignored)
│   └── azure_ml.env.example   # Template (committed)
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
- `SA.primes`, `SA.P`, `SA.PHI`, etc.

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

### `scripts/solenoid_jax.py` — ACTIVE
JAX/Diffrax accelerated integration backend (~200× faster than scipy).

- `integrate_all_branches_jax(branches, t_eval, T_max, ...)` — vmap'd batch integration across all 210 branches
- `warmup()` — pre-compile JIT (avoids timing compilation in benchmarks)
- `detect_device()` — returns device string ("CPU" or "GPU (Tesla V100-...)")

Uses Dopri8 (8th-order RK) with PIDController adaptive stepping. Float64 enabled automatically.

### `scripts/solenoid_numba.py` — ACTIVE
Numba JIT + ProcessPoolExecutor backend (~5–15× faster than scipy).

- `integrate_all_branches_numba(branches, t_eval, T_max, ...)` — parallel integration with JIT'd ODE RHS
- Uses `@numba.njit(cache=True)` for the cascade ODE, bypasses GIL via process pool

### `scripts/benchmark_gpu.py`
Standalone benchmark script for local or remote execution.

- `run_benchmark(T_max)` — full pipeline: detect device → warmup → integrate → sector analysis → save results
- Used by `azure_ml_submit.py` for remote jobs

### `scripts/azure_ml_submit.py`
Azure ML job submission. Loads workspace config from `secrets/azure_ml.env`.

- `submit_benchmark(ml_client, T_max, gpu, dry_run)` — submit benchmark to GPU or CPU cluster
- `submit_custom_script(ml_client, script_path, gpu, dry_run)` — submit arbitrary script
- Privacy: suppresses git metadata, uses generic experiment/display names

### Legacy Scripts (Phase 1–2)
The following modules were used by NB01–NB22 and are **not imported by any solenoid-phase notebook**:
- `concentric_system.py` — S² × R⁺ geometry (Phase 1)
- `nested_system.py` — nested oscillator simulation (Phase 1)
- `two_particle.py` — two-particle Coulomb integrals (Phase 1–2)
- `gravity.py`, `scattering.py`, `solid_state.py`, `nuclear.py`, `quantum_hall.py`, `tunneling.py`, `molecular.py` — Phase 2 domain modules (standard QM calculations)

These are retained for reference but are not part of the active framework.

## Acceleration Infrastructure

See `docs/acceleration.md` for full documentation including benchmark results and Azure ML setup.

### Backend Selection

The cascade ODE integration supports three backends via `SolenoidSystem.integrate_all_branches(..., backend=)`:

| Backend | When to Use | Speedup |
|---------|------------|--------|
| `'scipy'` | Debugging, small T (<50), compatibility | 1× (baseline) |
| `'numba'` | JAX unavailable, multi-core benefit needed | ~5–15× |
| `'jax'` | **All production work** — notebooks, parameter sweeps | ~200× |

**Always use `backend='jax'` for notebooks with T > 100.** The 200× speedup comes from JIT compilation + vmap vectorization on CPU. GPU provides no additional benefit for this workload (sequential ODE stepping).

### Azure ML Remote Execution

For very large T or batch parameter sweeps:

```bash
python scripts/azure_ml_submit.py --benchmark --T 5000        # GPU cluster
python scripts/azure_ml_submit.py --benchmark --T 5000 --cpu   # CPU cluster
python scripts/azure_ml_submit.py --script my_script.py        # Custom script
```

Requires `secrets/azure_ml.env` (see `secrets/azure_ml.env.example` for template). All workspace identifiers, compute target names, and experiment names are loaded from this file — nothing is hardcoded in scripts.

**Privacy**: The submit script suppresses git metadata discovery, uses generic naming, and disables MLflow source tracking. Delete jobs after downloading results.

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

The project has progressed through 171 notebooks. The full per-notebook Phase Map is in `docs/scorecard.md` — consult it for identity details and notebook-level descriptions. Below is the high-level arc.

| Phase | Notebooks | Focus |
|-------|-----------|-------|
| Geometry + Standard QM | NB01–NB22 | S² × R⁺ exploration, consistency checks. No predictions. Phase 1/2 are NOT results. |
| Solenoid Discovery | NB23–NB28 | Identified the (2,3,5,7)-solenoid as the fundamental structure. |
| SM Constants | NB29–NB40 | 28 identities from number theory — structural constants, coupling constants, cosmological parameters. |
| Algebraic Dynamics | NB41–NB48 | Characters, Lagrangian, Cayley metric, modular forms. 41 identities. |
| Covering Tower + Spectral | NB49–NB59 | Generation mechanism, VEV dynamics, spectral wall. 28 identities. |
| Fermion Mass (Static) | NB60–NB65 | Zero-parameter mass predictions from Z*₂₁₀ sector algebra. 18 identities. |
| Cascade Dynamics | NB66–NB81 | ODE dynamics → CP-pair ratios → fermion mass ratios. Complete chain validated. 44 identities. |
| Solenoid Geometry + Gravity | NB82–NB92 | Metric, Lagrangian, cosmology (H₀, Ω_DM/Ω_b, G_N). Cosmological sector CLOSED. 23 identities. |
| Lepton Mass + Wrapping | NB93–NB108 | Window-0 concentration, dilution, wrapping anatomy. Mass mechanism understood. 18 identities. |
| Mixing + EW Precision | NB109–NB123 | CKM (4 Wolfenstein), PMNS (5 angles), gauge couplings, α(0), m_H, gravity bridge. 42 identities. |
| Mass Architecture | NB124–NB137 | τ-μ bridge, unified mass architecture, exponent derivation, factored x(R₃). 8 identities + mechanism. |
| Gauge Emergence | NB138–NB147 | Single action, wreath product → SU(3)×SU(2)×U(1), fermion bijection, mass formula derived. Identity #278. |
| Mass Pipeline | NB148–NB162 | End-to-end pipeline: {2,3,5,7}+M_Z → 9 fermion masses. x(R0)=4/7 DERIVED. r_bs, r_tc DERIVED. 9/9 PASS. |
| CKM + Frontier | NB163–NB169 | CKM from dynamics, V_us derived (0.029%), sector-resolved pipeline. GAP-15 (bottom Yukawa) confirmed OPEN. |
| Exponent Derivation | NB170–171 | x_q = 100/63 confirmed (0.01σ). Factored: (4/7)(25/9). Base derived. Cross-level 25/9 mechanism: transient wrapping + SS amplification ≈ p₃² (NB171, 0.018%). 3 new identities (#279–281). |
| S² Reconstruction | NB172–176 | Cascade visualization (NB172). A₅ icosahedral truncation → non-circular reason for 4 primes (NB173, #282–289). A₅ ↔ Z*₂₁₀ McKay bridge (NB174, #290–294). Monodromy IS the coupling (NB175, #295–297). Cascade = S² gradient flow, all dynamics grounded (NB176, #298–302). Reconstruction Phases 0–3 RESOLVED. |
| Concentric Geometry | NB177–178 | Primorial radii r_k = P_k from covering constraint. Area ratios = Γ̃ eigenvalues. Geometric Laplacian = 2K_k. Path graph reduction. Metric radii sum. Gauge-gravity bridge r₃+r₄ = Tr(L) = 240 (unique). Consecutive quartet 5,6,7,8 (unique). Gravity in curvature language. 11 identities (#303–313). |
| Spectral Bridge | NB179 | Natural per-factor Cayley graph on Z*₂₁₀: |S| = p₃ = 5 (unique). Integer eigenvalues 0..10, palindromic (bipartite). det'(L) = 2²⁵ × 3¹⁶ × 5¹³ × 7⁸. Spectral bridge: H = det'(L)·p₄/(Λ_max^{σ₃(p₁)}·p₂^{λ(P₄)}) — EXACT. Canonical: H = p₁^λ × P₄^ω × p₄^{p₃}. 7 identities (#314–320). |
| p-Adic Bridge Derivation | NB180 | All four p-adic valuations of det'(L) determined by v₂ = p₃² = |S|². Pairwise differences = framework invariants. Bridge exponents forced by Λ_max = p₁·p₃ consistency. Fundamental identity p₃² = σ₃(p₁) + p₁^{ω(P₄)}. GAP-19 RESOLVED. 5 identities (#321–325). |
| SS Amplification Mechanism | NB181 | Frequency gradient drives SS₃/SS₀ ≈ P₃ = 30 (not p₃² = 25). Jacobian: lower-triangular, eigenvalue −κ (stable). FFT confirms ω/P_k descent. CORRECTION of NB171 SS claim. 0 new identities. |
| Bottom Yukawa | NB182 | 42 = P₄/p₃ charge-neutral sub-covering. λ(P₄) = p₁p₂(p₄−p₃) (also holds for {3,5,7,11}). m_t/m_b = 42×√(29/30) at 0.40σ. D₄ wreath product context. GAP-15 NARROWED. 2 identities (#326–327). |
| Concentric Sphere Laplacian | NB183 | GEO-1: x_lep = l(l+1)/P₁² at l=3 = 3.0 (125 ppm). x_q = (3/2)×(200/189) at l=2 = 100/63 (geometric decomposition). p₁³p₃²−p₂³p₄ = 11 = p₅. Covering singlet/triplet: p₂=3 gives 1 mode at l=2, 3 modes at l=3. S²/S¹ separation. 4 identities (#328–331), 1 NULL (#332). |
| Inter-Sphere Coupling | NB184 | GEO-1 continuation + GEO-2. l selection rule: l=2 quarks (inward non-trivial + outward singlet), l=3 leptons (both non-trivial). 200/189 honest null. Curvature-mass predictions: m_μ/m_e ≈ 35^{3/2} (0.14%), m_τ/m_μ ≈ 9^{9/7} (0.26%). C₀ atlas: C₀(lepton) = √(p₃p₄) = (K₂/K₄)^{1/4} (0.05%), C₀(quark) = 21/√10 (0.04%). 3 identities (#333–335). |
| C₀ Atlas Derivation | NB185 | C₀ mechanism identified. C₀ lives at cascade R₃ level (not R₀). R₀-level C₀(lepton) = 8.77, transforms through 3 nonlinear cascade levels to R₃ = 5.912 ≈ √35 (0.070%). NOT topological — requires κ = 1/√P₄ (κ-sensitive, resonance structure). NOT single-branch — p₄=7 branch averaging gives C₀² ≈ p₃p₄. Effective decay rate γ₃/κ ≈ λ(7)/p₄ = 6/7 (0.14%). #333, #334 status: PATTERN-MATCHED → COMP. CONFIRMED. 0 new identities. |
| S² Covering Energy | NB186 | S² geometry PRODUCES cascade dynamics that S¹ topology only DESCRIBES. Embedding theorem: S¹ cascade ≡ l=0 sector of S² covering energy gradient flow (machine precision, 0.00e+00). Per-l cascade ODE with geometric damping κ_eff(l,k) = κ(1 + l(l+1)/P_k²). Mass exponents from innermost sphere Laplacian: x_lep = l(l+1)/P₁² at l=3 = 3 (EXACT), x_q base = 3/2 at l=2 (×200/189 → 100/63 EXACT). Covering selection: p₂=3 filter on Y_l^m creates singlet at l=2 (quarks), triplet at l=3 (leptons). Mode splitting visible on nontrivial branches. Explanatory gain: S² resolves 6/6 observables vs S¹'s 2/6. #328–#331 status: PATTERN-MATCHED → DERIVED. 1 new identity (#336). |
| Per-ℓ Cascade Dynamics | NB187 | Full JAX integration of 210 branches at ℓ=0,2,3 with correct inter-level coupling ODE. ℓ=0 matches standard pipeline to 10⁻¹². Primorial screening theorem: S² geometric damping screened at R₃ — quark C₀ changes 0.058% (ℓ=0→ℓ=2), lepton 5.3% (ℓ=0→ℓ=3). 200/189 NOT absorbed by per-ℓ damping. Division of labor: S²(ℓ>0) selects modes, S¹(ℓ=0) computes masses. Inner-sphere products: 35/12 = p₃p₄/λ(P₄) at ℓ=2, 16/3 = d(P₄)/p₂ at ℓ=3. 4 identities (#337–340). |
| Radial Structure | NB188 | GEO-5: prime 5 = radial metric. Covering Jacobian J (4×5), stiffness JᵀJ, Cauchy-Binet det(JJᵀ) = Σ(P₄/Pₖ)². Path graph T₄ with golden ratio eigenvalue pairing. Hydrogen Σn²=30=P₃. Double truncation l_max=3. Primorial localization. Z₄ connection dimensional not structural. 5 identities (#341–#345). |
| Oriented Axes | NB189 | GEO-4: axis assignment 2→φ, 3→θ, 5→r, 7→arc is UNIQUE (1/24). Forced by 4 constraints: {2,3}→angular, {5,7}→non-angular, 2→φ (bilateral=full circle), 5→r (NB188). CRT–coordinate correspondence: each CRT factor Z_{φ(p)} maps to one axis. Per-axis metric. Cascade = inter-axis coupling. Angular state count 12 = λ(P₄) coincidental (NULL). 1 identity (#346). |
| Full S² Covering Action | NB190 | GD-1: complete covering energy E = T + V as 80×80 quadratic form. Azimuthal C_az (p₁=2) kills 8/16 modes. Polar C_pol (p₂=3) creates l-mixing via Chebyshev T₃. l-parity conservation: even-l {0,2} / odd-l {1,3} decouple (forced by T₃ odd symmetry). Physical mode count = ω(P₄)=4 per parity (1+3 structure). l=0 recovers S¹ cascade exactly. Three-cluster spectrum at P_k² scales. Upper cluster spread = λ(P₄)=12. C₀, 200/189 confirmed dynamical not spectral. 3 identities (#348–350). |
| L-Sector Decoupling | NB191 | GD-1 complete: Euler-Lagrange of S² action. C_pol(l'>0, 0; m) = 0 by Legendre orthogonality (analytic proof, sympy-verified). Even-parity C_pol(m=0) = [[1,8/35],[0,-1/7]] — upper triangular, framework-prime fractions. C_pol(0,2;0) = 8/35 = φ(P₄)/P₄ = sin²θ_W — Weinberg angle IS the geometric coupling of l=2 (quark) into l=0 (cascade). S¹ cascade = exact l=0 invariant subspace (nonlinear). C₀ NOT from cross-l coupling. 3 identities (#351–353). |
| Chebyshev Coupling Formulas | NB192 | Universal analytic formulas for per-prime Chebyshev coupling on S². C_T_p(0,2;0) = (p²−1)/(4p²−1) for any covering degree p (sympy-verified p=2..10). C_T_p(2,2;0) = −15p²/[(4p²−1)(4p²−9)] for any p≥1 (sympy-verified p=2..8). Three-way Weinberg chain: sin²θ_W = (p₂²−1)/(4p₂²−1) = p₁³/(p₃p₄) = φ(P₄)/P₄ via Catalan (3²−2³=1 unique). Self-coupling at p₂=3: C(2,2) = −1/p₄. Even-parity block: [[1, φ(P₄)/P₄], [0, −1/p₄]]. 200/189 classified as algebraic bridge (GD-3 ANSWERED). 5 identities (#354–358). |
| Chebyshev Coupling Algebra | NB193 | C_T_p(1,1;0) = −3/(p²−4) for odd p (sympy-proved). Bilateral spectral democracy: C_T_2(0,l) = (−1)^l/(2l+1) for all l (sympy-proved). Cross-level resonance: C₃(2,2) = C₅(1,1) = −1/p₄, forced by three arithmetic identities specific to {2,3,5,7}. Uniqueness: {2,3,5,7} is the only prime quadruple satisfying p₃=p₁+p₂, p₄=p₁+p₃ (mod 3 proof). −1/p₄ appears at three independent positions. 4 identities (#359–362). |
| Odd-Parity Block | NB194 | Complete l-parity decomposition: odd block (l=1,3) fully characterized. Bilateral Annihilation Theorem: C₂(l,l')=0 for ALL l when l' odd. p=3 odd block has complex eigenvalues (rotation), p=5,7 real (scaling). Framework constants: C₃(1,1)=−p₂/p₃, C₃(1,3)=p₁³/p₃ (unique positive off-diagonal), C₇(1,1)=−1/(p₂·p₃). Composite det numerator = p₂²·p₃³·p₄² (framework primes only). 6 identities (#363–368). |

### Current State (Post-NB194)

- **368+ structural identities**, 0 free parameters, 1 dimensional anchor (M_Z)
- **Mass pipeline**: 9/9 PASS, mean |dev| = 0.65%, 8/9 within 1σ (NB167)
- **CKM**: 9/9 within 2σ, χ²/9 = 1.92, V_us derived to 0.029%
- **Reconstruction**: Phases 0–3 RESOLVED. Cascade = S² gradient flow. All dynamics grounded.
- **S² covering energy** (NB186): S¹ cascade ≡ l=0 sector of S² gradient flow (embedding theorem). Per-l geometric damping PRODUCES mass exponents (x_lep = 3 at l=3, x_q = 100/63 at l=2). Covering selection rules PRODUCE quark/lepton split. GEO-1 RESOLVED for mass exponents and selection rules.
- **Per-ℓ cascade** (NB187): Full JAX integration at ℓ=0,2,3. Primorial screening: S² geometric damping screened at R₃ (quark 0.058%, lepton 5.3%). 200/189 NOT absorbed by per-ℓ damping — confirmed as S¹ cascade mechanism. Division of labor: S²(ℓ>0) selects modes, S¹(ℓ=0) computes masses.
- **Radial structure** (NB188): Prime 5 = radial metric. Covering Jacobian J (4×5), stiffness JᵀJ, Cauchy-Binet det(JJᵀ) = Σ(P₄/Pₖ)², golden ratio eigenvalue pairing, hydrogen Σn²=30=P₃, double truncation l_max=3, primorial localization. GEO-5 ANSWERED.
- **Oriented axes** (NB189): Axis assignment 2→φ, 3→θ, 5→r, 7→arc is UNIQUE (1/24), forced by S² coordinate structure + covering monodromy + NB188 radial confirmation. CRT–coordinate correspondence. Per-axis metric. Cascade = inter-axis interfaces. GEO-4 ANSWERED. Geometric program ALL 5 questions RESOLVED/ANSWERED.
- **Full S² covering action** (NB190): Complete covering energy as 80×80 quadratic form on 5 shells × 16 modes. l-parity conservation (even/odd decouple, forced by Chebyshev T₃ odd symmetry). Physical mode count ω(P₄)=4 per parity with 1+3 structure. l=0 recovers S¹ exactly. Three-cluster spectrum at P_k² scales. C₀ and 200/189 are dynamical, not spectral.
- **L-sector decoupling** (NB191): C_pol(l'>0, 0; m) = 0 by Legendre orthogonality (analytic proof). Even-parity C_pol(m=0) = [[1, 8/35], [0, -1/7]] — upper triangular, all framework-prime fractions. C_pol(0,2;0) = φ(P₄)/P₄ = sin²θ_W — Weinberg angle IS the geometric coupling of l=2 (quark) into l=0 (cascade). S¹ cascade = exact l=0 invariant subspace (nonlinear). C₀ NOT from cross-l coupling. GD-1: COMPLETE (NB190+NB191).
- **Chebyshev coupling formulas** (NB192): Universal analytic formulas for per-prime Chebyshev coupling on S². C_T_p(0,2;0) = (p²−1)/(4p²−1) for any covering degree p. C_T_p(2,2;0) = −15p²/[(4p²−1)(4p²−9)] for any p≥1. Three-way Weinberg chain: sin²θ_W = (p₂²−1)/(4p₂²−1) = p₁³/(p₃p₄) = φ(P₄)/P₄ via Catalan (3²−2³=1 unique). Self-coupling at p₂=3: C(2,2) = −1/p₄. Even-parity block: [[1, φ(P₄)/P₄], [0, −1/p₄]]. 200/189 classified as algebraic bridge. GD-3: ANSWERED.
- **Chebyshev coupling algebra** (NB193): C_T_p(1,1;0) = −3/(p²−4) for odd p (sympy-proved). Bilateral spectral democracy: C_T_2(0,l) = (−1)^l/(2l+1) for all l (sympy-proved). Cross-level resonance: C₃(2,2) = C₅(1,1) = −1/p₄, forced by three arithmetic identities specific to {2,3,5,7}. Uniqueness: {2,3,5,7} is the only prime quadruple satisfying p₃=p₁+p₂, p₄=p₁+p₃ (mod 3 proof). −1/p₄ appears at three independent positions.
- **Odd-parity block** (NB194): Complete l-parity decomposition. Bilateral Annihilation Theorem: C₂(l,l')=0 for ALL l when l' odd. p=3 odd block has complex eigenvalues (rotation), p=5,7 real (scaling). Framework constants: C₃(1,1)=−p₂/p₃, C₃(1,3)=p₁³/p₃ (unique positive off-diagonal), C₇(1,1)=−1/(p₂·p₃). Composite det numerator = p₂²·p₃³·p₄² (framework primes only).
- **Concentric sphere arena**: r_k = P_k, K_k = 1/P_k², Tr(L) = r₃+r₄ = 240, gravity in curvature language
- **C₀ atlas**: cascade base ratios = curvature ratios (NB184), mechanism identified — C₀ lives at R₃ level, requires κ = 1/√P₄, emerges from p₄=7 branch averaging (NB185). GEO-2: curvature hierarchies approximate but need dynamics.
- **Spectral bridge**: M_Pl/M_Z = det'(L)·p₄/(Λ_max^{σ₃(p₁)}·p₂^{λ(P₄)}) — exact (NB179). Bridge exponents derived from p-adic consistency (NB180). GAP-19 RESOLVED.
- **Causal gaps**: see `docs/causal_gaps.md` for full classification (DERIVED / PATTERN-MATCHED / OPEN)

### Open Frontier — Geometric Program (PRIMARY)

The reconstruction (NB172–178) established the S² × R⁺ arena with concentric spheres but never derived dynamics FROM it. The mass pipeline still runs on S¹ covering maps with hardcoded exponents and pattern-matched anchors. The geometric program is the primary research direction:

| Priority | Question | Status |
|----------|----------|--------|
| **GEO-1** | Laplacian spectrum on nested concentric spheres {S²(P_k)} with covering connections | RESOLVED (NB186+NB190+NB191). S¹ cascade = l=0 sector of S² gradient flow (embedding theorem + analytic proof). L-sector decoupling: C_pol(l'>0, 0; m) = 0 (Legendre orthogonality). Even-parity block upper triangular: C_pol(0,2;0) = 8/35 = sin²θ_W. GD-1 COMPLETE. |
| **GEO-2** | Do curvature ratios K_k/K_{k+1} = p_{k+1}² produce mass hierarchies without ODE integration? | NB184: APPROXIMATE. Curvature ratios set hierarchy SCALE: m_μ/m_e ≈ 35^{3/2} (0.14%), m_τ/m_μ ≈ 9^{9/7} (0.26%). Exponents are prime ratios. Dynamics still needed for exact values. |
| **GEO-3** | Covering constraint in Y_l^m basis — what do spherical harmonics give that Fourier modes on S¹ don't? | NB186: ANSWERED. S² gives l-dependent dynamics (per-l damping, selection rules, mode splitting) that S¹ cannot access. The l=0 sector IS S¹. The l>0 sectors produce mass exponents, quark/lepton discrimination, and degeneracy values. Full explanatory gain: 6/6 vs 2/6 observables. |
| **GEO-4** | Oriented axes (2→φ, 3→θ, 5→r, 7→arc) — mathematical content of axis assignment | ANSWERED (NB189). Axis assignment is UNIQUE (1/24): forced by S² coordinate structure (bilateral → full circle, stratification → half-range) + covering monodromy + NB188 radial confirmation. CRT–coordinate correspondence: each CRT factor Z_{φ(p)} maps to one axis with one quantum number. Per-axis metric: g_φ = P_k²sin²θ, g_θ = P_k², g_r = 1, g_arc = 1/P₄. Cascade residuals = inter-axis interfaces. Angular state count 12 = λ(P₄) coincidental (NULL). 1 identity (#346). |
| **GEO-5** | Radial structure — what does the radial coordinate (prime 5) contribute? | ANSWERED (NB188). Prime 5 = radial metric. Covering Jacobian J (4×5), stiffness JᵀJ, Cauchy-Binet det(JJᵀ) = Σ(P₄/Pₖ)². Path graph T₄ with golden ratio eigenvalue pairing. Hydrogen Σn²=30=P₃. Double truncation l_max=3. Primorial localization. Z₄ connection dimensional not structural. 5 identities (#341–#345). |

The current mass pipeline phenomenological inputs that the geometric program should replace:
- Hardcoded exponents: x_q = 1.587, x_l = 3.000 — NOW DERIVED from S² Laplacian (NB186). x_l_inter from cascade measurement (S¹ = l=0 sector)
- Pattern-matched anchors: m_t/M_Z = p₂²/√(πp₄)×..., m_t/m_b = 42×...
- C₀ values: now known to be curvature ratios (√35, 21/√10) and computationally confirmed from cascade dynamics (NB185), but no analytic derivation yet
- S¹ dynamics projected from S² arena (cascade ODE on covering residuals)

### Algebraic Gaps (SECONDARY — tracked, not actively pursued)

| Gap | Description | Where |
|-----|-------------|-------|
| **GAP-19** | RESOLVED (NB180). Full causal chain established. | NB178–180 |
| **GAP-15** | NARROWED (NB182). Formula structural, mechanism not derived. May follow from geometry. | NB169, NB182 |
| **GAP-20** | Mechanism IDENTIFIED (NB171). Cross-level factor may follow from curvature ratios. | NB170–171, NB181 |
| **GAP-11** | Gauge ρ-corrections — pattern-matched. | NB111 |
| **GAP-14** | CKM Wolfenstein parameters — structural. | NB109, NB168 |
| **GAP-12/13** | QED running, Higgs mass — pattern-matched. | NB113, NB120 |

## Working Rules

1. **No free parameters**: Every prediction must derive from {2, 3, 5, 7} (or equivalently P₄ = 210) plus the single anchor M_Z. If a fit parameter is needed, it's not a prediction.

2. **Phase 1/2 are NOT results**: NB01–NB08 used a preliminary model (nested torus T⁴) that was abandoned. NB13–NB22 reproduce standard QM textbook calculations on S² × R⁺ — they are consistency checks, not predictions. Do NOT cite Phase 1/2 notebook verdicts ("EXACT match", "PASS") as framework findings. All identities come from NB29+ (solenoid arithmetic). See `docs/scorecard.md` §V for details.

3. **System first, shadows second**: Numerical identities are projections — shadows the system casts onto the measurement plane. Understanding the dynamical system that produces them is the actual physics. A notebook that observes, characterizes, or explains the system is not a "null result" — it is the real work. Do NOT frame system-observation notebooks as "0 new identities (honest null)" as if the purpose was identity-hunting and we failed. The identity count tracks the shadows; understanding tracks the system.

4. **Honest nulls**: When a test generates a specific prediction and it fails, classify it honestly:
   - **Genuine null**: The framework predicts X, data shows not-X → report as failure
   - **Scope boundary**: The framework correctly identifies that the question requires a deeper layer (e.g., dynamics rather than statics)
   - **Methodological**: The test wasn't discriminating enough

5. **The Cartesian artifact**: 3+1 dimensionality is NOT a prediction of this framework. It is what Cartesian-trained observers project onto the concentric nesting. Do NOT propose "testing" whether 3+1 emerges — that is circular. See the four-prime theses for the full argument.

6. **Per-prime generators**: When working with Z*₂₁₀, use the CRT decomposition. The four cyclic factors {Z₁, Z₂, Z₄, Z₆} correspond to the four primes {2, 3, 5, 7}. Characters factor per-prime.

7. **Pre-commit workflow**: Always save all files (`workbench.action.files.saveAll`) before `git add`/`git commit`. VS Code may hold unsaved buffer state.

8. **Conda environment**: `concentric` (Python 3.12). Dependencies: numpy, scipy, matplotlib, sympy, jupyter, jax, diffrax, numba.

9. **Notebook execution order**: Always execute cells sequentially from top to bottom. Later cells depend on variables established by earlier cells. If a cell fails, fix it and re-run — do not skip ahead.

10. **Exact arithmetic first**: Use `sympy` or `fractions.Fraction` to verify identities exactly before reporting numerical values. An identity that holds only to floating-point precision is not proven — it is a hint.

11. **One identity per claim**: Each identity must be a single, verifiable statement. Do not bundle multiple claims into one identity number.

12. **Parallelization**: When writing out calculations, whenever possible use parallelization in code to speed up execution. This is especially important for notebooks that involve large computations.

## Connection to Literary Compilation

This project provides the computational verification for claims in the `literary-compilation` repository, specifically:
- "Orbits That Lost Their Center" (four-prime theses on space-time emergence)
- "The Resolution of the Finite Mind" (numbers as perceiver properties)
- The Swedenborgian correspondence framework applied to mathematical physics

The scorecard in `docs/scorecard.md` serves as the empirical backbone for these theses.

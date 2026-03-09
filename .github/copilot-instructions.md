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

## Repository Structure

```
concentric-spacetime/
├── notebooks/          # Jupyter notebooks NB01–NB45 (sequential, cumulative)
│   ├── 01_nested_oscillators.ipynb
│   ├── ...
│   └── 45_thermal_dynamics.ipynb
├── scripts/
│   ├── solenoid_algebra.py    # Core algebraic module (Z*₂₁₀ operations) — ACTIVE
│   ├── solenoid_system.py     # Solenoid dynamics utilities — ACTIVE
│   ├── concentric_system.py   # [LEGACY] S² × R⁺ geometry (Phase 1)
│   ├── nested_system.py       # [LEGACY] Nested oscillator simulation (Phase 1)
│   ├── two_particle.py        # [LEGACY] Two-particle interaction (Phase 1–2)
│   └── *.py                   # [LEGACY] Phase 2 domain modules (gravity, scattering, etc.)
├── docs/
│   ├── scorecard.md           # Living scorecard: all 55 identities
│   └── research_directions.md # Early-phase research directions (partially superseded)
├── temp/                      # Builder scripts (create_nbXX.py) and scratch
└── output/                    # Generated figures and data
```

## Key Modules

### `scripts/solenoid_algebra.py` — ACTIVE
The core algebraic module. Provides:
- `SA` — pre-built `SolenoidAlgebra` instance for P₄ = 210
- `SA.Z_star` — the 48 elements of Z*₂₁₀
- `SA.decompose(k)` — returns raw CRT residue tuple for k ∈ Z*₂₁₀
- `SA.character(chi_index, k)` — evaluates character χ at group element k
- `SA.primes`, `SA.N`, `SA.phi_N`, etc.

### `scripts/solenoid_system.py` — ACTIVE
Solenoid dynamics: Lagrangian construction, kinetic matrix, Cayley graph Laplacian, spectral analysis.

### Legacy Scripts (Phase 1–2)
The following modules were used by NB01–NB22 and are **not imported by any solenoid-phase notebook**:
- `concentric_system.py` — S² × R⁺ geometry (Phase 1)
- `nested_system.py` — nested oscillator simulation (Phase 1)
- `two_particle.py` — two-particle Coulomb integrals (Phase 1–2)
- `gravity.py`, `scattering.py`, `solid_state.py`, `nuclear.py`, `quantum_hall.py`, `tunneling.py`, `molecular.py` — Phase 2 domain modules (standard QM calculations)

These are retained for reference but are not part of the active framework.

## Notebook Conventions

### Naming
Notebooks are numbered sequentially: `XX_descriptive_name.ipynb`. The number reflects the order of discovery, not logical dependency (though later notebooks build on earlier results).

### Builder Pattern
Notebooks are generated from Python builder scripts in `temp/create_nbXX.py` that produce `.ipynb` JSON directly. This ensures reproducibility and avoids manual cell editing.

**CRITICAL BUG**: Triple-quoted docstrings inside raw strings (`r"""..."""`) break the JSON builder. Use `#` comments instead of docstrings in code cells.

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

## Working Rules

1. **No free parameters**: Every prediction must derive from {2, 3, 5, 7} (or equivalently P₄ = 210) plus the single anchor M_Z. If a fit parameter is needed, it's not a prediction.

2. **Phase 1/2 are NOT results**: NB01–NB08 used a preliminary model (nested torus T⁴) that was abandoned. NB13–NB22 reproduce standard QM textbook calculations on S² × R⁺ — they are consistency checks, not predictions. Do NOT cite Phase 1/2 notebook verdicts ("EXACT match", "PASS") as framework findings. All 55 identities come from NB29–NB45 (solenoid arithmetic). See `docs/scorecard.md` §V for details.

3. **Honest nulls**: When a test fails, classify it honestly:
   - **Genuine null**: The framework predicts X, data shows not-X → report as failure
   - **Scope boundary**: The framework correctly identifies that the question requires a deeper layer (e.g., dynamics rather than statics)
   - **Methodological**: The test wasn't discriminating enough

4. **The Cartesian artifact**: 3+1 dimensionality is NOT a prediction of this framework. It is what Cartesian-trained observers project onto the concentric nesting. Do NOT propose "testing" whether 3+1 emerges — that is circular. See the four-prime theses for the full argument.

5. **Per-prime generators**: When working with Z*₂₁₀, use the CRT decomposition. The four cyclic factors {Z₁, Z₂, Z₄, Z₆} correspond to the four primes {2, 3, 5, 7}. Characters factor per-prime.

6. **Pre-commit workflow**: Always save all files (`workbench.action.files.saveAll`) before `git add`/`git commit`. VS Code may hold unsaved buffer state.

7. **Conda environment**: `concentric` (Python 3.12). Dependencies: numpy, scipy, matplotlib, sympy, jupyter.

## Connection to Literary Compilation

This project provides the computational verification for claims in the `literary-compilation` repository, specifically:
- "Orbits That Lost Their Center" (four-prime theses on space-time emergence)
- "The Resolution of the Finite Mind" (numbers as perceiver properties)
- The Swedenborgian correspondence framework applied to mathematical physics

The scorecard in `docs/scorecard.md` serves as the empirical backbone for these theses.

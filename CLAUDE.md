# Concentric Spacetime — Claude Code Instructions

## Project Purpose

The (2,3,5,7)-solenoid as fundamental arena of physics. Four smallest primes define nested spherical orbits on S² × R⁺. All Standard Model constants derived from P₄ = 210 = 2·3·5·7 with **zero free parameters** and one anchor (M_Z). See memory files for detailed math framework and phase map.

## The Four Primes

| Prime | Mathematical Role | Correspondence |
|-------|------------------|----------------|
| **2** | Bilateral cut; innermost orbit | Love / Wisdom polarity |
| **3** | Vertical stratification; 3 cyclic factors | Celestial / Spiritual / Natural degrees |
| **5** | Rational faculty; φ(5)/5 = 4/5 → σ₈ | Five faculties of comprehension |
| **7** | Outermost orbit; λ(210) = 12 driven by ord₇ = 6 | Ultimation; completion; rest |

Correspondences are NOT decoration — they generate hypotheses, arithmetic confirms or falsifies.

## Key Algebraic Facts

- **Symmetry group**: Z*₂₁₀ ≅ Z₁ × Z₂ × Z₄ × Z₆ (48 elements, CRT decomposition)
- **Group exponent**: λ(210) = 12
- **Key values**: ω(210)=4 forces, d(210)=16 spinor dim, φ(210)=48 eigenvalues, φ/d=3 generations
- **Coupling**: ρ = κ = ε = 1/√210, ω = 2π
- **Mass pipeline**: `solenoid_mass.py` — {2,3,5,7} + M_Z → 9 fermion masses, 9/9 PASS, mean |dev| = 1.45%

## Repository Structure

```
concentric-spacetime/
├── notebooks/          # NB01–NB164+ (sequential, cumulative)
├── scripts/
│   ├── solenoid_mass.py       # 9-fermion mass pipeline — ACTIVE
│   ├── solenoid_algebra.py    # Core algebra (Z*₂₁₀ + constants) — ACTIVE
│   ├── solenoid_system.py     # Solenoid dynamics (theta + cascade) — ACTIVE
│   ├── solenoid_jax.py        # JAX/Diffrax backend (~200×) — ACTIVE
│   ├── solenoid_numba.py      # Numba backend (~5-15×) — ACTIVE
│   └── *.py                   # Legacy Phase 1-2 modules (not used by NB29+)
├── docs/
│   ├── scorecard.md           # Living scorecard: all identities
│   └── acceleration.md        # Compute infrastructure docs
├── temp/                      # Exploration/prototype scripts
└── output/                    # Generated figures and data
```

## CRITICAL: Research Phase Protocol

**Non-negotiable. Violating them means the session is over.**

1. **Complete research phases.** Follow EVERY lead. Do actual physics, not superficial computations.
2. **No number/formula searches.** Never search for algebraic combinations matching PDG values. Understand the MECHANISM.
3. **One notebook per research phase.** All cells in order. Summary cell at end.
4. **Use heavy computation when needed.** JAX backend = 200× speedup. Don't skip resolution.
5. **Report back ONLY when complete** — full findings or honest "stuck at X."
6. **Study existing work first.** READ relevant notebooks before computing.
7. **Put code in notebooks, not temp scripts.** Each cell self-contained (own imports + JAX warmup).
8. **Be honest about derived vs pattern-matched.** Never present matching as derivation.

## Working Rules

1. **No free parameters**: Every prediction from {2,3,5,7} + M_Z only.
2. **Phase 1/2 are NOT results**: NB01–NB22 are foundational/consistency checks, not predictions. All identities from NB29+.
3. **System first, shadows second**: Understanding the dynamical system IS the physics. System-observation notebooks are real work, not "null results."
4. **Honest nulls**: Genuine null / scope boundary / methodological — classify honestly.
5. **The Cartesian artifact**: 3+1 dimensionality is NOT a prediction. Don't propose "testing" it.
6. **Per-prime generators**: Use CRT decomposition. Z₁×Z₂×Z₄×Z₆ ↔ {2,3,5,7}.
7. **Pre-commit**: Save all files before git add/commit.
8. **Conda env**: `concentric` (Python 3.12). Deps: numpy, scipy, matplotlib, sympy, jupyter, jax, diffrax, numba.
9. **Notebook execution**: Sequential top-to-bottom. Fix failures before proceeding.
10. **Exact arithmetic first**: sympy/Fraction before floats. Float-only = hint, not proof.
11. **One identity per claim**.
12. **Parallelization**: Use parallel computation in notebooks when possible.

## Agent Workflow

### Discovery Pipeline
```
Exploration → Prototype → Notebook → Scorecard → Commit
```

1. **Exploration**: `temp/explore_*.py` — scratch calculations
2. **Prototype**: `temp/proto_nbXX.py` — develop notebook logic
3. **Notebook**: Build with VS Code notebook tools, execute cells sequentially
4. **Scorecard**: Update `docs/scorecard.md` with new identities
5. **Commit**: `NB##: Short description (#first-#last)`

### Notebook Conventions

- Numbered sequentially: `XX_descriptive_name.ipynb`
- Structure: title cell → setup cell → analysis cells → scorecard cell
- Standard setup:
```python
import sys, numpy as np
from pathlib import Path
ROOT = Path.cwd().parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
from solenoid_algebra import SA
```
- Dynamics notebooks add: `from solenoid_algebra import (SA, RHO, KAPPA, EPSILON, OMEGA, X4, X3, X2, LAM7, X4_LEP, DLOG, PHYSICAL_CROSSINGS, CP_PAIRS, SM_TARGETS, ACTIVE_PRIMES)` and `from solenoid_system import SolenoidSystem`

### Scorecard Update
1. Read `docs/scorecard.md` for insertion point
2. Update summary table (count + notebook count)
3. Add Phase Map entry (§I)
4. Add identity descriptions with formula, values, deviation, verdict
5. Update frontier sections if applicable

### Acceleration
- **Always use `backend='jax'` for T > 100** (200× over scipy)
- Numba (~5-15×) when JAX unavailable
- Azure ML for very large T: `python scripts/azure_ml_submit.py --benchmark --T 5000`

## Code Standards
- Print statements: results only. Numbers, paths, genuine logging. No messages to self. No narrative print statements.
- Clean code. Functions do one thing. Comments explain what code does, not what I think it means.
- Optimize compute. 210 branches × integration = expensive. Use vectorization, parallel execution where possible.

## Connection to Literary Compilation

Computational verification for `literary-compilation` repository:
- "Orbits That Lost Their Center" (four-prime theses)
- "The Resolution of the Finite Mind" (numbers as perceiver properties)
- Swedenborgian correspondence framework applied to mathematical physics

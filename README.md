# Concentric Spacetime

**Zero free parameters. One dimensional anchor ($M_Z$).**

This repository derives Standard Model constants, coupling ratios, and fermion mass hierarchies from the arithmetic of the four smallest primes $\{2, 3, 5, 7\}$ — specifically from $P_4 = 210 = 2 \cdot 3 \cdot 5 \cdot 7$ and the multiplicative group $\mathbb{Z}^*_{210}$.

The mathematical object is the **(2,3,5,7)-solenoid**: the inverse limit of iterated covering maps with winding numbers 2, 3, 5, 7. Its Poincaré section has exactly 210 discrete return points, its symmetry group has 48 elements, and its group exponent is 12.

All identities, predictions, and verdicts are documented in [docs/scorecard.md](docs/scorecard.md).

## Mathematical Framework

### The Solenoid

Four covering maps on circles with winding numbers $\{2, 3, 5, 7\}$:

$$S^1 \xleftarrow{2} S^1 \xleftarrow{3} S^1 \xleftarrow{5} S^1 \xleftarrow{7} S^1$$

The inverse limit has a Cantor-set fiber over each point. At $\varepsilon = 0$ (exact solenoid), the dynamics are quasiperiodic with frequencies $\omega / P_k$. At $\varepsilon > 0$, the structure dissolves toward flat $T^4$ — proving the primes are irreplaceable.

### Algebraic Structure

- **Arena**: $S^2 \times \mathbb{R}^+$ (sphere × positive radial half-line)
- **Symmetry group**: $\mathbb{Z}^*_{210} \cong \mathbb{Z}_1 \times \mathbb{Z}_2 \times \mathbb{Z}_4 \times \mathbb{Z}_6$ (via CRT)
- **48 Fourier characters** label the fermion eigenstates
- **CRT decomposition** maps to SM quantum numbers: chirality ($p=3$), charge sector ($p=5$), generation × color-parity ($p=7$)

### Cascade ODE

The dynamics admits two equivalent coordinate representations — one system, two views:

| Representation | Dimension | Variables | Best For |
|---|---|---|---|
| **Theta-space** | 5D | Angles $\theta_k$ on each orbit | Spectral analysis, Poincaré sections |
| **R-space (cascade)** | 4D | Covering residuals $R_k = p_k \theta_{k+1} - \theta_k$ | Mass predictions, CP-pair ratios |

The cascade ODE:

$$\frac{dR_k}{dt} + \kappa R_k = f_k(t;\text{lower levels})$$

where $f_k$ encodes nonlinear sin coupling. All parameters fixed: $\kappa = \varepsilon = 1/\sqrt{210}$, $\omega = 2\pi$.

## Phase Map

| Phase | Notebooks | Focus | Identities |
|---|---|---|---|
| Geometry | NB01–NB12 | $S^2 \times \mathbb{R}^+$ exploration | — |
| Standard QM | NB13–NB22 | Consistency checks (reproduces textbook QM) | — |
| Solenoid Discovery | NB23–NB28 | Identifying the (2,3,5,7)-solenoid | — |
| SM Predictions | NB29–NB40 | Constants from number theory | #1–#28 |
| Algebraic Dynamics | NB41–NB45 | Characters, Lagrangian, thermodynamics | #29–#55 |
| Metric & Modular | NB46–NB48 | Cayley metric, modular forms, palindromes | #56–#69 |
| Covering Tower | NB49–NB56 | Generation structure, mass channels | #70–#91 |
| Spectral Protection | NB57–NB59 | Conjugation, real potentials, directed Cayley | #92–#97 |
| Fermion Mass | NB60–NB65 | Mass predictions, fermion map, sector algebra | #98–#115 |
| Dynamical Sector | NB66–NB69 | ODE dynamics, CP-selective breaking | #116–#125 |
| Dynamical Mass | NB70–NB74 | Complete quark + lepton mass hierarchy | #126–#142 |
| Perturbative R | NB75–NB78 | Critical coupling, wrapping, sum rules | #143–#159 |
| Cascade ODE | NB79–NB81 | Cascade derivation, full chain validation | #160–#171 |

All identities are documented in [docs/scorecard.md](docs/scorecard.md).

## Repository Structure

```
concentric-spacetime/
├── notebooks/              # 81 Jupyter notebooks (NB01–NB81, sequential)
├── scripts/
│   ├── solenoid_algebra.py # Core algebraic module (Z*₂₁₀, constants, mass formulas)
│   ├── solenoid_system.py  # Unified solenoid dynamics (theta-space + cascade)
│   └── *.py                # Legacy Phase 1–2 modules (retained for reference)
├── docs/
│   └── scorecard.md        # Living scorecard: all 171 identities
├── temp/                   # Exploration scripts, prototypes, builders
├── output/                 # Generated figures and data
├── environment.yml         # Conda environment (Python 3.12)
└── README.md
```

### Key Modules

**`solenoid_algebra.py`** — The algebraic backbone:
- Pre-built `SA` instance for $P_4 = 210$
- CRT decomposition, character evaluation, sector labels
- Physical constants: $\rho = \kappa = \varepsilon = 1/\sqrt{210}$, algebraic exponents ($x_4$, $x_3$, $x_2$)
- SM targets (PDG 2024), CP-pair definitions, covering tower hierarchy

**`solenoid_system.py`** — One dynamical system, two coordinate views:
- Coordinate transforms: `theta_to_R()`, `R_to_theta()`
- Both ODE formulations: `theta_ode()`, `cascade_ode()`
- Both initial conditions: `initial_theta()`, `initial_R()`
- Integration: theta-space (`integrate()`) and R-space (`integrate_branch()`, parallel via ThreadPoolExecutor)
- Mass extraction: `accumulate_sectors()`, `cp_pair_ratios()`
- Spectral analysis: `poincare_section()`, `spectrum()`, `alignment_structure()`

## Setup

```bash
conda env create -f environment.yml
conda activate concentric
jupyter lab
```

## The Four Primes

Each prime carries both a mathematical role and a Swedenborgian correspondence:

| Prime | Mathematical Role | Correspondence |
|---|---|---|
| **2** | Bilateral cut; innermost orbit | Love / Wisdom polarity |
| **3** | Vertical stratification; 3 cyclic factors | Celestial / Spiritual / Natural degrees |
| **5** | Rational faculty; $\varphi(5)/5 = 4/5 \to \sigma_8$ | Five faculties of comprehension |
| **7** | Outermost orbit; $\text{ord}_7 = 6$ drives $\lambda(210) = 12$ | Ultimation; completion; rest |

The correspondences are not decoration — they informed the discovery. But all claims are tested computationally: the correspondences generate hypotheses, the arithmetic confirms or falsifies them.

## Companion Documents

- **Thesis**: [Orbits That Lost Their Center](docs/reports/Orbits%20That%20Lost%20Their%20Center_%20The%20Concentric%20Geometry%20of%20the%20Four-Prime%20Coordinate%20System%20and%20the%20Cartesian%20Linearization%20of%20the%20Proprium.md)
- **Arithmetic companion**: [The Resolution of the Finite Mind](docs/reports/The%20Resolution%20of%20the%20Finite%20Mind_%20Celestial%20Perception%2C%20Numerical%20Architecture%2C%20and%20the%20Limit%20of%20Spiritual%20Analysis.md)
- **Framework**: The [literary-compilation](https://github.com/kayna-of-light/literary-compilation) repository contains the full correspondential framework

## Methodology

Every prediction must derive from $\{2, 3, 5, 7\}$ plus one dimensional anchor ($M_Z$). If a fit parameter is needed, it is not a prediction.

Results are reported honestly:
- **PASS**: Prediction matches measurement within stated precision
- **FAIL**: Prediction does not match — recorded as a genuine miss
- **NULL**: Test is not discriminating enough, or the question requires a deeper layer (e.g., dynamics rather than statics)

Phase 1–2 notebooks (NB01–NB22) reproduce standard QM and are consistency checks, not predictions. All 171 identities come from NB29+ (solenoid arithmetic).

# Concentric Spacetime

Computational testing of the concentric geometry described in *Orbits That Lost Their Center: The Concentric Geometry of the Four-Prime Coordinate System and the Cartesian Linearization of the Proprium*.

## What This Repository Tests

The thesis proposes that the four foundational primes (2, 3, 5, 7) form not a Cartesian grid but a system of **nested concentric orbits** — two inside three inside five inside seven — each measured by angular position, each containing all inner orbits. Several claims in the thesis are computationally testable:

### 1. Nested Oscillator Dynamics
Four concentric oscillators with strict containment constraints (outer constituted by inner content, inner boundary-conditioned by outer). The thesis claims:
- Every outer orbit's state IS the total state of its inner orbits
- State change is distributed across all nesting levels, not concentrated on any single orbit
- No orbit returns to the same state, even though every orbit returns to the same angular position
- The outermost orbit carries cumulative complexity that makes coordinate identification fail

### 2. Recurrence and the Resolution Threshold
The Poincaré recurrence theorem applied to nested coupled systems. The thesis claims:
- Recurrence time increases combinatorially with nesting depth
- At the innermost orbit (simplest internal structure), recurrence is fast — coordinate identification succeeds
- At the outermost orbit (carrying total inner state), recurrence time exceeds any meaningful timescale
- The **resolution threshold** — where coordinate identification breaks down — is a continuous gradient, not a sharp boundary
- The $3+1$ split arises from an observer drawing a binary line across this gradient

### 3. Quantum Number–Prime Correspondence
The quantum numbers ($n$, $l$, $m$, $s$) and the prime nesting (5, 3, 2) satisfy the same containment constraints:
- $n$ sets maximum $l$; $l$ sets maximum $m$ — outer constrains inner
- Total states per shell: $2n^2$ — the factor structure mirrors prime nesting
- The angular part of the hydrogen wave function is a spherical harmonic $Y_l^m(\theta, \phi)$
- Verify the formal parallel and compute where it holds precisely vs. where it is structural analogy

### 4. Curvature, Linearization, and Spherical Harmonics
The mathematical backbone of the thesis:
- $\kappa = 1/R \to 0$ as $R \to \infty$: a straight line is a circle with infinite radius
- Sagitta $h/s \to 0$ as $R \to \infty$: the arc becomes indistinguishable from the chord
- Successive spherical harmonic degrees ($l = 0, 1, 2, \ldots$) add angular structure while preserving lower-degree structure — mapping to the prime cuts (uniform → bilateral → vertical → ...)
- Schwarzschild metric approaching Minkowski at $r \to \infty$: curvature vanishes at infinite distance from the source

### 5. Metric Signature from Nesting Topology
The most ambitious claim. The thesis argues that $(-,+,+,+)$ is not a fundamental property but the Cartesian observer's projection of a continuous complexity gradient onto a binary:
- Can a system of four nested oscillators, observed from inside, produce an apparent signature where three coordinates are "returnable" and one is not?
- Is the threshold continuous (as the thesis claims) or sharp?
- Does it shift with observer resolution capacity (as the thesis predicts for different beings)?

## Repository Structure

```
concentric-spacetime/
├── notebooks/          # Jupyter notebooks — one per testable claim
│   ├── 01_nested_oscillators.ipynb
│   ├── 02_recurrence_threshold.ipynb
│   ├── 03_quantum_prime_correspondence.ipynb
│   ├── 04_curvature_harmonics.ipynb
│   └── 05_metric_signature_emergence.ipynb
├── scripts/            # Reusable computation modules
├── output/             # Generated figures and data
├── docs/               # Notes and supplementary documents
├── temp/               # Working files
├── secrets/            # Credentials (gitignored)
├── environment.yml     # Conda environment specification
└── README.md           # This file
```

## Setup

```bash
conda env create -f environment.yml
conda activate concentric
jupyter lab
```

## Dependencies

- Python 3.12
- NumPy, SciPy, SymPy — numerical and symbolic computation
- Matplotlib, Seaborn, Plotly — visualization (including interactive 3D)
- Pandas — data handling
- Jupyter, JupyterLab — notebook environment

## Companion Documents

- **Thesis**: *Orbits That Lost Their Center* — in [literary-compilation](https://github.com/marconian/literary-compilation) `data/02_Swedenborgian_Theology/`
- **Arithmetic companion**: *The Resolution of the Finite Mind* — same directory
- **Framework**: The [literary-compilation](https://github.com/marconian/literary-compilation) repository contains the full correspondential framework

## Methodology

Each notebook follows the same structure:
1. **Claim** — what the thesis asserts
2. **Model** — the mathematical/computational setup
3. **Computation** — numerical results
4. **Verdict** — does the computation support, refine, or contradict the claim?

Results are reported honestly. If a computation contradicts a thesis claim, that is recorded as a miss. If it supports the claim, that is recorded as a hit. If the result is underdetermined, that is stated explicitly.

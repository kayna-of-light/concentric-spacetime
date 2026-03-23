# Phase 2B Findings: Monodromy Dynamics

**Date**: 2025-07-16
**Script**: `temp/phase2b_monodromy_dynamics.py`
**Question**: What replaces the cascade ODE when the arena is S² × R⁺?

## Key Findings

### 1. Tower genus preservation (Riemann-Hurwitz)
Each p-fold branched covering of S² with exactly 2(p−1) simple branch points has genus 0 by Riemann-Hurwitz:
```
2g − 2 = p(−2) + 2(p−1) = −2  ⟹  g = 0
```
The covering tower is S² ← S² ← S² ← S² ← S² (all spheres), exactly analogous to the solenoid S¹ ← S¹ ← S¹ ← S¹ ← S¹. This is a necessary structural requirement: the tower preserves the base geometry.

### 2. Monodromy generates Z₂₁₀, not Z*₂₁₀
- Monodromy around a branch point at level k shifts the fiber component by ±1 mod p_k
- Since shifts at different levels commute (act on different CRT factors), the total monodromy group is Z₂ × Z₃ × Z₅ × Z₇ = Z₂₁₀
- Z*₂₁₀ is the **symmetry group** (deck automorphisms), not the monodromy group
- Important distinction: monodromy = what the dynamics CAN DO; deck symmetry = what the dynamics RESPECTS

### 3. Balanced branching → conjugate pairs
For balanced branching (equal numbers of σ and σ⁻¹ monodromies), each level has (p−1) conjugate pairs:
- Level 0 (p=2): 1 pair — bilateral cut
- Level 1 (p=3): 2 pairs — chirality
- Level 2 (p=5): 4 pairs — charge sector
- Level 3 (p=7): 6 pairs — generation × color
- Total: 1 + 2 + 4 + 6 = 13 branch-point pairs

This is reminiscent of the CP-pair structure but the numbers don't directly match the cascade CP pairs. The (p−1) count per level DOES match the CRT factor orders minus 1.

### 4. S² covering potential is naturally higher-dimensional
- On S¹: 4 scalar residuals → 4D ODE
- On S²: 4 vector residuals (each with θ and φ components) → 8D ODE
- With axis constraints (p=2 acts on φ only, p=3 acts on θ only): reduces to 6D
- Including R⁺ (radial): up to 12D

### 5. Monodromy IS the coupling mechanism
**This is the key realization.** On S¹, coverings of circles have no branch points, so the coupling between levels had to be INVENTED (the sin perturbation in the cascade). On S², branch points exist naturally and their monodromy provides coupling without invention.

The covering potential on S² near a branch point b_j:
```
V_mono(x) ~ −log|x − b_j|  (logarithmic singularity)
```
Branch points at Platonic vertices (NB173) create a potential landscape with the symmetry of nested Platonic solids.

### 6. κ = 1/√P₄ from Haar metric
The "equal coupling per sheet" argument (NB143) carries over: each of P₄ = 210 sheets contributes equally, giving κ² · P₄ = 1. This was previously post-hoc on S¹; on S² it follows from the covering-space metric normalization.

Argument 3 (branch-point density) **fails** as a derivation of κ (1.44 ≠ 0.069).

### 7. Berry phase from monodromy
Transport around a branch point at level k produces Berry phase 2π/p_k. Total Berry phase for one circuit of all branch points:
```
Σ_k 2(p_k−1) · (2π/p_k) = 2π · Σ_k 2(p_k−1)/p_k = 2π · 593/105 ≈ 2π · 5.648
```

### 8. The S² cascade replacement
The S² dynamics should be the gradient flow of V_covering with the Haar metric W = diag(P_k):
```
d(config)/dt = −W⁻¹ · ∇V_covering
```
where V_covering includes:
- Quadratic covering residuals (same structure as S¹ cascade)
- Logarithmic branch-point potential (NEW — provides the coupling)
- Spherical metric cross-terms (NEW — from S² curvature)

## Identity Candidates

| # | Formula | Description |
|---|---------|-------------|
| A | g(all levels) = 0 | Tower genus preservation: Riemann-Hurwitz with 2(p−1) branch points on S² gives genus 0 at every level |
| B | Balanced branching: (p−1) conjugate pairs per level | Total pairs: 1+2+4+6 = 13 |
| C | Berry sum = 2π · Σ 2(p−1)/p = 2π · 593/105 | Total Berry phase from all branch-point monodromy |

## Open Questions for NB175

1. Can candidate A be promoted? It's a mathematical theorem (Riemann-Hurwitz), not a prediction — it's a REQUIREMENT for the tower to work.
2. Candidate B's total (13) doesn't match any known structural number directly. Is this significant?
3. The Berry sum 593/105 — does this simplify or match anything?
4. Can the logarithmic branch-point potential be computed explicitly for the Platonic vertex positions?
5. Does the 6D reduced system (with axis constraints) reproduce the 4D cascade behavior in projection?

## Synthesis

The cascade ODE was assembled from invented parts:
1. Linear damping → from gradient flow (OK)
2. sin coupling → **INVENTED** (S¹ has no branch points)
3. κ = 1/√210 → **SET** (equal per sheet)
4. ω = 2π → **CHOSEN**

On S², items 2 and 3 become geometric:
- Item 2: Branch-point monodromy provides natural coupling (no invention needed)
- Item 3: κ = 1/√P₄ from covering-space metric normalization

Item 4 (ω = 2π) remains conventional and may need revisiting when the Laplacian eigenvalues are computed.

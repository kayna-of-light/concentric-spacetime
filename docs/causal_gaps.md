# Causal Gaps — The "Why" Questions

> **Principle**: Every formula is a pattern until we understand the mechanism that produces it. A formula found by matching to PDG is an observation, not a derivation. This document tracks what is genuinely derived vs what is pattern-matched, and what work remains to close each gap.

**Status**: Post-NB162. The fermion mass mechanism is fully resolved (coherence across covering levels). Many coupling constants and cosmological parameters remain pattern-matched.

---

## Classification

| Status | Meaning |
|--------|---------|
| **DERIVED** | Mechanism understood. Would predict the value without knowing PDG. |
| **PATTERN-MATCHED** | Formula found by searching prime-arithmetic expressions that fit PDG. Physical interpretation given but mechanism not derived. |
| **PARTIALLY DERIVED** | Some steps have mechanisms, others are pattern-matched. |
| **IRREDUCIBLE** | Understood as a boundary condition, not derivable within the framework. |

---

## I. FULLY DERIVED (mechanism understood)

### Fermion Masses (NB148-162)
**Status**: DERIVED. 9/9 PASS, mean |dev| = 1.45%.

The mass mechanism is spatial coherence: the non-wrapping fraction across all 4 covering levels × generation spacing P₃ gives the mass exponent. The resonance condition κ = 1/√P₄ places the gen2 crossing at the wrapping boundary.

| Quantity | Formula | Mechanism |
|----------|---------|-----------|
| x(R0) = 4/7 | ∏(1-f_k) × P₃ = φ(p₃)/p₄ | Non-wrapping fraction product (NB161) |
| r_bs = 19/15 | 1 + φ(p₃)/(p₂p₃) | Isospin non-wrapping fraction (NB162) |
| r_tc = 23/14 | 1 + 1/p₁ + 1/p₄ | Chirality + generation fractions (NB162) |
| κ = 1/√P₄ | Sheet normalization | Resonance condition for rational exponents (NB159) |
| CP ratios | From cascade ODE | Spatial profile of covering misalignment |
| x_q, x_l | Cascade eigenvalues | T-independent, computable from ODE |

### Gauge Structure (NB140-144)
**Status**: DERIVED.

| Quantity | Formula | Mechanism |
|----------|---------|-----------|
| SU(3) | Z₂ ≀ Z₃ → 3+1+1+1 | Wreath product of deck transformations |
| SU(2) | Z₂ ≀ Z₂ = D₄ → 2+1+1 | Wreath product |
| U(1) | Z₄ ⊂ U(1) | φ(5) = 4 |
| 3 generations | Z₃ ⊂ Z₆ | Singlet irreps of wreath product |
| φ(P₄) = 48 states | Group theory | |Z*₂₁₀| |

### Tree-Level Gauge Couplings (NB30, NB111)
**Status**: DERIVED (tree level). The tree values come directly from Z*₂₁₀ character counting.

| Quantity | Tree Formula | Mechanism |
|----------|-------------|-----------|
| 1/α_s(tree) | φ(P₃) = 8 | Characters visible at p=3 level |
| 1/α₂(tree) | P₃ = 30 | Third primorial |
| 1/α₁(tree) | P₁P₃ = 60 | Product of primorials |

### PMNS Reactor + Solar Angles (NB110, NB129)
**Status**: DERIVED.

| Quantity | Formula | Mechanism |
|----------|---------|-----------|
| sin²θ₁₃ = 1/45 | 1/(p₂²p₃) | Cascade susceptibility (Γ̃⁻¹)₁₂ (NB276) |
| sin²θ₁₂ = 14/45 | 1/p₂ − sin²θ₁₃ | TBM sum rule from μ-τ symmetry (p₂=3) |

### Hubble Correction (NB90-91)
**Status**: DERIVED.

| Quantity | Formula | Mechanism |
|----------|---------|-----------|
| C = 96/175 | (1−1/p₃)²(1−1/p₄) | Energy screening (outer primes carry 96.5% of variance, NB84) |

### Single Action (NB139, NB143)
**Status**: DERIVED.

| Quantity | Formula | Mechanism |
|----------|---------|-----------|
| Γ̃ = K·A⁻¹ | Covering stiffness × directional dynamics | Derived from covering topology |
| κ = ε = 1/√P₄ | Sheet normalization | κ²P₄ = 1 |

---

## II. PATTERN-MATCHED GAPS (formula works, mechanism unknown)

### GAP-11: Gauge Coupling ρ Corrections [STRUCTURAL]

**What we have**: The ρ-corrections to gauge couplings from NB111:
- 1/α_s = φ(P₃) **+ p₄ρ** = 8 + 7/√210
- 1/α₂ = P₃ **− λ(p₄)ρ** = 30 − 6/√210
- 1/α₁ = P₁P₃ **− P₄ρ²** = 60 − 1 = 59

**What's missing**: WHY is the strong correction +p₄ρ (generation prime × coupling)? Why is the weak correction −λ(p₄)ρ (Carmichael of generation × coupling)? The hypercharge correction −P₄ρ² = −1 is structurally clean (P₄ρ² = 1 by definition), but the other two corrections were FOUND by matching, not derived from the cascade.

**Would resolve**: Complete gauge coupling predictions from first principles.

### GAP-12: QED Running Ratio 15/14 [STRUCTURAL]

**What we have**: 1/α(0) / 1/α(M_Z) = p₂p₃/(p₁p₄) = 15/14 (#246, NB119).

**What's missing**: WHY does the full QED running (all loops, hadronic VP, thresholds) equal the ratio of inner to outer prime products? This was found because 137.036/127.9 ≈ 15/14. The decomposition "inner primes / outer primes" is a rationalization.

**Would resolve**: 1/α(0) = 137.056 from first principles.

### GAP-13: Higgs Mass Formula [STRUCTURAL]

**What we have**: m_H/M_Z = (φ(P₄) + ρ)/(p₃p₄) = (48 + 1/√210)/35 (#260, NB120). Dev: 0.08σ.

**What's missing**: WHY does φ(P₄)/(p₃p₄) = 48/35 give the Higgs-to-Z ratio? The decomposition sin²θ_W(tree) × λ(p₄) = (8/35) × 6 is noted but not derived. Found because 48/35 × 91.19 ≈ 125.25.

**Would resolve**: Higgs mass from solenoid mechanism.

### GAP-14: CKM Wolfenstein Parameters [STRUCTURAL]

**What we have** (NB109):
- λ = p₂²/(φ(P₃)p₃) = 9/40 (0.00σ — exact match to PDG)
- A = φ(p₃)/p₃ = 4/5 (0.04σ)
- ρ̄ = 1/ω = 1/(2π) (0.02σ)
- η̄ = √p₂/p₃ = √3/5 (0.16σ)

**What's missing**: WHY do these specific prime combinations give the CKM parameters? The Cabibbo angle matching to 0.00σ strongly suggests it was fitted, not predicted. The connection ρ̄ = 1/(2π) is elegant but unexplained. WHY does the CP-violating phase involve the base frequency?

**Partial progress**: The Froggatt-Nielsen route (sin θ_C ≈ √(m_d/m_s)) connects the Cabibbo angle to the cascade mass ratio. If m_s/m_d → (40/9)² = 19.75 ≈ 20, then sin θ_C = 9/40 follows. This would DERIVE λ from the masses. But (40/9)² = 19.75, not exactly 20.

**Would resolve**: CKM matrix from solenoid dynamics.

### GAP-15: PMNS Atmospheric Angle and CP Phase [STRUCTURAL]

**What we have** (NB110):
- sin²θ₂₃ = p₃p₄/p₁^{λ(p₄)} = 35/64 (0.04σ)
- δ_CP = p₃p₄π/p₁^{p₃} = 35π/32 (0.01σ)
- Cross-relation: δ_CP/π = p₁ × sin²θ₂₃

**What's missing**: WHY does the atmospheric angle involve these specific prime combinations? The cross-relation is interesting but doesn't explain WHY these formulas.

**Would resolve**: PMNS matrix from solenoid mechanism.

### GAP-16: Neutrino Mass-Squared Ratio [STRUCTURAL]

**What we have**: Δm²₃₂/Δm²₂₁ = p₁p₄²/p₂ = 98/3 (#237, NB110). Dev: 0.10σ.

**What's missing**: WHY this combination of primes? Only p₃ (charge) is absent. Found by matching.

**Would resolve**: Neutrino mass hierarchy from solenoid.

### GAP-17: Neutrino Boost Factor [PARTIALLY DERIVED]

**What we have**: m₃ = (M_Z²/M_Pl) × p₂³p₃⁵p₄/p₁³ (#274, NB128-129).

**Derived part**: B_ν = λ(P₄) × (Γ̃⁻¹)₁₂⁻¹ × (p₃/p₁)^{p₂} — the susceptibility inverse entries ARE from the dissipation matrix (NB275). UNIQUE decomposition proven.

**Pattern-matched part**: The specific exponents in the M_Z-form (p₂³p₃⁵p₄/p₁³) combine seesaw + boost in a way that was verified against PDG, not predicted.

### GAP-18: Cosmological Parameters [STRUCTURAL]

**What we have** (NB37-39, NB88):
- Ω_Λ = φ(35)/35 = 24/35 (0.14σ)
- n_s = 1 − 1/P₃ = 29/30 (0.42σ)
- σ₈ = φ(p₃)/p₃ = 4/5 (1.83σ)
- Ω_DM/Ω_b = p₂³/p₃ = 27/5 (0.04σ)

**What's missing**: WHY does the dark energy fraction equal the totient density of p₃p₄? WHY is the spectral index 1 − 1/P₃? These are totient densities and primorial fractions that were found to match cosmological data. The Totient Density Tower (sin²θ_W, σ₈, Ω_Λ all being φ(n)/n) is a suggestive pattern but not a derived mechanism.

**Would resolve**: Cosmology from solenoid spatial structure.

### GAP-19: Gravity Hierarchy Exponents [PARTIALLY DERIVED]

**What we have**: M_Pl/M_Z = 240⁴ × 7⁹ = Tr(L)^{ω(P₄)} × p₄^{σ₃(p₁)} (#261, NB121). Dev: 0.003%.

**Derived part**: Tr(L) = 240 (Cayley Laplacian trace, spectral theorem). ω(P₄) = 4 (prime count). σ₃(p₁) = 9 (sum of cubes of divisors of 2). Multiple independent derivation chains converge on 240.

**Pattern-matched part**: WHY Tr(L)^{ω(P₄)} × p₄^{σ₃(p₁)} specifically? The scorecard admits "5/6 steps proved from first principles, 1/6 remains structural identification." Five candidate mechanisms tested, none fully deductive.

---

## III. ORIGINAL MECHANISM GAPS (from pre-NB148)

### GAP-04: Seesaw Mechanism [FRAMEWORK]
**Status**: Framework identified (NB142). The seesaw base v²/M_Pl connects to the gravity hierarchy. The boost factor has a unique susceptibility decomposition (NB275). But the MECHANISM producing the seesaw from the solenoid (why neutrino mass ∝ 1/M_Pl) is not derived.

### GAP-09: Dimensional Anchor M_Z [IRREDUCIBLE]
**Status**: Understood as irreducible. M_Z = 2π√P₄ in natural units is the filter cutoff (NB142, NB248). A dimensionless theory needs one dimension to anchor it.

---

## IV. RESOLVED GAPS

| Gap | Status | Mechanism |
|-----|--------|-----------|
| GAP-01 | RESOLVED | ρ from impedance balance + wrapping (NB130-131) |
| GAP-02 | FULLY RESOLVED | Mass = coherence across levels. Non-wrapping product × P₃ (NB161-162). Resonance at κ=1/√P₄ (NB159). |
| GAP-03 | MECHANISM | Three-layer fermion map: wreath (framework) + Cayley generators (selection) + dynamics (masses) (NB145) |
| GAP-05 | MAJOR PROGRESS | Gauge groups from wreath products (NB140-144) |
| GAP-06 | RESOLVED | 3 generations from Z₃ singlet irreps (NB140) |
| GAP-07 | RESOLVED | Cascade = gradient flow with containment dissipation (NB139) |
| GAP-08 | RESOLVED | Stratification = gauge structure (NB142) |
| GAP-10 | FULLY RESOLVED | Γ̃ = K·A⁻¹ derived from covering topology (NB143) |

---

## V. RECOMMENDED ATTACK ORDER

Based on which gaps would unlock the most understanding:

1. **GAP-14 (CKM)** — The Cabibbo angle may follow from the cascade mass ratio via Froggatt-Nielsen. If m_s/m_d from the cascade connects to sin θ_C, this DERIVES the CKM from the same dynamics that gives masses. High leverage.

2. **GAP-11 (Gauge ρ-corrections)** — The tree-level couplings are derived. Understanding the ρ-corrections would complete the gauge sector. The corrections may come from the same cascade dynamics that produces masses.

3. **GAP-13 (Higgs mass)** — At 0.08σ, this is the most precise match. If the formula (48+ρ)/35 has a mechanism, it would connect the Higgs to the eigenstate count and outer prime structure.

4. **GAP-18 (Cosmology)** — The Totient Density Tower suggests a unified mechanism. Understanding WHY φ(n)/n gives cosmological parameters would be a breakthrough.

5. **GAP-19 (Gravity exponents)** — 5/6 derived. The remaining 1/6 (why this specific combination) is the last piece.

6. **GAP-15, GAP-16 (PMNS + ν mass²)** — These may follow from the dissipation matrix, which already gives sin²θ₁₃.

7. **GAP-12 (Running ratio)** — May be the hardest; encodes all-loop QED in a single ratio.

8. **GAP-17 (ν boost)** — Partially derived; needs the full seesaw mechanism (GAP-04).

---

*Created: 2026-03-16 (post-NB129)*
*Updated: 2026-03-17 (post-NB162). Complete audit of derived vs pattern-matched. 9 new gaps (GAP-11 through GAP-19) cataloging all pattern-matched formulas.*

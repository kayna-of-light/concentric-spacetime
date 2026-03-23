# Phase 2 Findings — Algebraic Bridge: A₅ ↔ Z*₂₁₀

**Date**: Session following NB173 completion  
**Script**: `temp/phase2_algebra_exploration.py`

## Summary

Phase 2 asked: does Z*₂₁₀ emerge from S² geometry? The answer is **no** — Z*₂₁₀ brings additional fiber structure that geometry alone cannot see. But the geometry **constrains** the algebra through a P₄-specific interlock.

## Key Findings

### Finding 1: Character-Geometry Factorization (48 = 16 × 3)

Z*₂₁₀ ≅ Z₂ × Z₄ × Z₆ = Z₂ × Z₄ × (Z₂ × Z₃)

Fixing the Z₃ component (the generation subgroup from Z₃ ⊂ Z₆ = Z*₇):
- Each generation: Z₂ × Z₄ × Z₂ = 16 characters
- 16 × 3 = 48 total

**The 16 "geometric" characters per generation match d(P₄) = 16 harmonic slots from A₅ truncation.**

This is the explicit decomposition: φ(P₄) = d(P₄) × (φ(P₄)/d(P₄)) = 16 × 3.

### Finding 2: Z*₂₁₀ Cannot Act Faithfully on V₁₆

Since dim V₁₆ = 16 < 48 = |Z*₂₁₀|, at most 16 of the 48 characters can appear as eigenvalues on V₁₆. The kernel must have order ≥ 3. This is precisely the 3-fold generation redundancy.

### Finding 3: McKay Correspondence Match

The McKay correspondence for finite subgroups of SU(2):
- Binary tetrahedral 2T (order 24 = 2λ(P₄)) ↔ E₆
- **Binary octahedral 2O (order 48 = φ(P₄)) ↔ E₇**
- Binary icosahedral 2I (order 120 = 2|A₅|) ↔ E₈

The fiber character count |Z*₂₁₀| = 48 = |2O| (binary octahedral). While Z*₂₁₀ ≅ 2O as groups is false (one is abelian, the other non-abelian), the ORDER match connects the solenoid to E₇ in the McKay classification.

The E₈ root count 240 = lcm(|A₅|, |Z*₂₁₀|) = Tr(L) — already established as the gauge-gravity bridge.

### Finding 4: The McKay Prime Chain

The ratios between binary groups track the primes:
- |2O|/|2T| = 48/24 = 2 = p₁
- |2I|/|2O| = 120/48 = 5/2 = p₃/p₁
- |2I|/|2T| = 120/24 = 5 = p₃
- |A₅|/|A₄| = 60/12 = 5 = p₃

And the SO(3) quotients:
- A₄ = 2T/Z₂ (order 12 = λ(P₄))
- S₄ = 2O/Z₂ (order 24 = |Aut(Boolean lattice 2⁴)|)
- A₅ = 2I/Z₂ (order 60)

### Finding 5: The A₄ Bridge

Both A₅ (geometry) and S₄ (divisor automorphisms) contain A₄ (order 12 = λ(P₄)):
- A₄ ⊂ A₅ as point stabilizer (index 5 = p₃)
- A₄ ⊂ S₄ as alternating subgroup (index 2 = p₁)

A₄ is the "geometric-algebraic intersection group." This gives:
- Geometry (A₅) → A₄ ← Algebra (S₄ → Z*₂₁₀)

### Finding 6: S₄ on 16 Divisors

S₄ acts on the 16 divisors of 210 by permuting primes. This gives 5 orbits: {1}, {p_i}, {p_ip_j}, {p_ip_jp_k}, {210}, with sizes {1,4,6,4,1} = Pascal's row. This is the same count as A₅ orbits on V₁₆ (5 irreps), though the orbit sizes differ ({1,3,5,3,4} for A₅ vs {1,4,6,4,1} for S₄).

### Finding 7: Monodromy Diagnosis

On S², the monodromy of the p=5 covering CAN be A₅ (not just Z₅). But if the monodromy is A₅, the cover is non-Galois (no deck symmetry). The solenoid assumed cyclic (Z_p) monodromy. The S² geometry permits but does not require the richer monodromy.

## New Identity Candidates

| # | Identity | Formula | Status |
|---|----------|---------|--------|
| #A | Character-Geometry Factorization | 48 = 16 × 3 = d(P₄) × (φ(P₄)/d(P₄)) | Structural |
| #B | McKay E₇ Bridge | |2O| = φ(P₄) = 48 | Structural |
| #C | E₈ Root LCM | Roots(E₈) = lcm(|A₅|, φ(P₄)) = 240 = Tr(L) | Structural |
| #D | A₄ = Bridge Group | |A₄| = gcd(|A₅|, |Z*₂₁₀|) = 12 = λ(P₄) | Structural |
| #E | Generation Quotient | Z*₂₁₀ / Z₃ ≅ Z₂ × Z₄ × Z₂ (order 16 = d(P₄)) | Structural |

## The Full Picture

```
S² base                          Z₂₁₀ fiber
  |                                 |
O(3) symmetry                   Z*₂₁₀ symmetry
  |                                 |
A₅ truncation (order 60)       48 characters
  |                                 |
5 irreps → 16 slots            16 × 3 factorization
  |                                 |
  └──── gcd = 12 = λ(P₄) ────────┘
         (A₄ bridge)
         
  lcm = 240 = Tr(L) = c₁(E₈) = P₃ × φ(P₃)
```

## Phase 2 Conclusion

Z*₂₁₀ does NOT emerge from S² geometry alone. The relationship is:
1. S² geometry provides A₅ truncation → 16 geometric slots
2. The fiber Z₂₁₀ provides Z*₂₁₀ → 48 characters = 16 × 3
3. The bridge A₄ (order 12 = λ(P₄)) sits in both structures
4. The McKay correspondence connects everything through ADE classification:
   - φ(P₄) = |2O| ↔ E₇
   - 2|A₅| = |2I| ↔ E₈
   - 240 = lcm = roots(E₈) = Tr(L)

The two structures are COMPLEMENTARY: geometry selects the 16 slots, algebra fills them with 48 states (3 per slot = generations). Neither is derivable from the other — they are different manifestations of the same primorial P₄ = 210.

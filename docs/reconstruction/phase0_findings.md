# Phase 0 Findings — How the Four Primes Relate to S²

> **Date**: 2025-07-14. Phase 0 of the reconstruction plan.
> **Script**: `temp/phase0_spectral_exploration.py`
> **References**: NB03, NB04, NB09, `scripts/concentric_system.py`

---

## Summary

Phase 0 investigated the key mathematical question from the reconstruction plan:

> Does the spherical harmonic degeneracy sequence {1, 3, 5, 7} at l = {0, 1, 2, 3}
> provide the natural mathematical embedding of the four primes into the geometry of S²?

**Answer: Partially. The primes enter S² × R⁺ through four structurally DIFFERENT 
mechanisms, not through four levels of the same thing.**

---

## The Four Mechanisms

| Prime | Role (from reports) | Mechanism on S² × R⁺ | Quantum number | How it enters |
|-------|--------------------|-----------------------|----------------|--------------|
| **2** | Bilateral cut | Z₂ parity ⊂ O(3) | m (magnetic) | Reflection, not rotation |
| **3** | Vertical stratification | l=1 irrep (dim 3) | l (angular momentum) | SO(3) irrep dimension |
| **5** | Radial openness | Radial shells on R⁺ | n (principal) | Normalizability on R⁺ |
| **7** | Developmental arc | Time evolution | cumulative state | Parametric, not spectral |

### Why the degeneracy match {1,3,5,7} is partial

The Laplacian on S² has eigenvalues −l(l+1) with degeneracy 2l+1. For l = 0,1,2,3:
degeneracies = 1, 3, 5, 7. This matches primes {3,5,7} at l=1,2,3 but gives 1 (not 2) 
at l=0.

The reason: 2l+1 is the sequence of ALL odd numbers. The first few odd numbers happen to 
be prime (3, 5, 7) but the sequence is arithmetic (universal), not prime-selected. At l=4, 
2l+1 = 9 = 3² (not prime). The match holds for exactly l=1,2,3 and then breaks.

### Why prime 2 is different

Prime 2 is the only even prime. On S², it enters through PARITY:
- The full symmetry group of S² is O(3) = SO(3) × Z₂
- The Z₂ factor is the bilateral reflection (θ → π − θ)
- This splits every l-level into even/odd parity (the bilateral cut)
- The parity eigenvalue of Y_l^m is (−1)^l

So prime 2 enters through a fundamentally different structural feature than {3,5,7}:
- **2 → Z₂ factor** (discrete, binary)
- **3,5,7 → SO(3) irrep dimensions** (continuous group, labeled by l)

This matches the reports: 2 is the "innermost orbit" — the first, most fundamental cut.
And Z₂ IS the most fundamental group: it has only two elements.

---

## What Phase 0 Tested and Found

### Test 1: Degeneracy matching (2l+1 = primes)
- **Result**: Matches {3,5,7} at l=1,2,3. Fails at l=0 (1 ≠ 2) and l=4 (9 is composite).
- **Verdict**: PARTIAL MATCH. Explains {3,5,7} but not {2}. Breaks at l=4.

### Test 2: Region counting (NB03/NB04 result, confirmed)
- **Result**: Zonal harmonic P_l creates l+1 zones. l+1 = {1,2,3,4,5,...} which matches 
  primes {2,3} at l={1,2} but fails at l=3 (4 zones ≠ prime 5).
- **Verdict**: FAILS. Confirmed NB03/NB04.

### Test 3: Cumulative state count
- **Result**: Through l=3: total harmonics = 1+3+5+7 = 16 = 4² = d(210).
- **Verdict**: NUMERICAL COINCIDENCE. The cumulative count is always L² for L levels. 
  d(210) = 16 = 4² because there are 4 primes (ω(210) = 4), and L² for L=4 gives 16. 
  This is tautological: d(P_k) = 2^k and L² with L=k gives k². These match when 2^k = k², 
  which happens at k=4. So d(P₄) = 4² is specific to four primes, but it's a coincidence 
  of 2^k = k², not a deep geometric fact.

### Test 4: Multiplicative algebra of harmonics
- **Result**: Of 136 nonzero product pairs within l ≤ 3, only 37 (27%) stay within l ≤ 3. 
  The other 99 (73%) produce components at L > 3.
- **Verdict**: CLOSED ALGEBRA FAILS. The first 16 harmonics do NOT form a closed algebra 
  under pointwise multiplication. Z*₂₁₀ cannot emerge from harmonic products.

### Test 5: Selection rules (Wigner 3j)
- **Result**: 15 allowed (l₁,l₂,l₃) coupling triples within l ≤ 3. The parity selection 
  rule (l₁+l₂+l₃ even) eliminates many couplings.
- **Verdict**: INTERESTING STRUCTURE. The 15 allowed triples within l ≤ 3 define a specific 
  coupling graph. Phase 1 should investigate whether this graph has prime-related structure.

### Test 6: Finite subgroups of SO(3)
- **Result**: The icosahedral group A₅ (order 60 = 2²·3·5) uses exactly {2,3,5}. 
  Prime 7 appears only in cyclic Z₇ and dihedral D₇ — no exceptional subgroup uses 7.
- **Verdict**: {2,3,5} has a natural home in the icosahedron. Prime 7 must enter differently 
  (through the developmental arc / time evolution, consistent with the reports).

### Test 7: Tensor product structure (Clebsch-Gordan)
- **Result**: V₁⊗V₁ = V₀⊕V₁⊕V₂ (reaches l=2), V₁⊗V₂ = V₁⊕V₂⊕V₃ (reaches l=3), 
  V₁⊗V₃ = V₂⊕V₃⊕V₄ (ESCAPES to l=4).
- **Verdict**: Starting from V₁ (fundamental rep), two tensor products suffice to reach V₃ 
  but three products escape to l=4+. No natural truncation at l=3.

---

## What Phase 0 Did NOT Find

1. **No truncation mechanism**: S² provides no reason to stop at l=3. The sequence 2l+1 
   continues forever. We need something ELSE to select exactly 4 levels.

2. **No Z*₂₁₀ from S²**: The multiplicative structure of the unit group does not emerge 
   from harmonic products. The algebra is not closed.

3. **No way to embed all four primes uniformly**: 2 enters through parity, 3,5,7 through 
   irrep dimensions. The four primes are NOT four instances of the same thing on S².

---

## What This Means for Phase 1

### The truncation question
Why exactly 4 levels? Candidate answers:

**(a) The hydrogen-atom constraint l < n**: If the radial quantum number n is bounded 
at n_max = 4, then l ∈ {0,1,2,3}. But what bounds n at 4?

**(b) The four-dimensionality of the system**: The four primes define four coordinates 
(φ, θ, r, t). Each coordinate is qualitatively different. There is no fifth prime entering 
the system, so there is no fifth structural level.

**(c) The developmental arc as boundary**: Prime 7 (the outermost orbit) "contains all 
three." If the developmental arc is the outer boundary of the spatial structure, it defines 
the maximum complexity: three spatial primes (2,3,5) ↔ three degrees of angular/radial 
structure ↔ l_max = 3 (but this doesn't follow deductively).

**(d) The first composite odd number**: 2l+1 = 9 = 3² at l=4. The first composite odd 
number is the square of the first odd prime. Maybe the system self-truncates when 
degeneracies become composite (non-prime dimensions admit non-trivial factorizations, 
unlike prime dimensions which are irreducible as vector spaces over finite fields).

### What should Phase 1 investigate?

1. **The radial structure**: How does prime 5 enter through the RADIAL coordinate? 
   Not through harmonic degeneracy, but through the principal quantum number n. 
   If n has exactly 5 values (or 4, or φ(5) = 4), what determines this?

2. **Covering maps on S²**: The solenoid uses S¹ coverings. S² admits branched coverings 
   (Riemann surfaces). A p-fold branched covering of S² by S² has 2(p-1) branch points 
   (Riemann-Hurwitz). What structure does a (2,3,5,7) tower of branched coverings produce?

3. **The nesting as operator eigenvalues**: Instead of levels of the SAME operator 
   (Laplacian), the four primes might define four DIFFERENT operators whose eigenvalue 
   spectra interact:
   - Parity operator P: eigenvalues ±1 (prime 2)
   - Angular momentum L²: eigenvalues l(l+1) (prime 3 through dim of l=1)
   - Radial Hamiltonian H_r: eigenvalues −1/(2n²) (prime 5 through n)
   - Total evolution U(t): cumulative state (prime 7)

4. **The icosahedron**: A₅ ≅ I is the largest exceptional finite subgroup of SO(3), with 
   order 60 = 2²·3·5. The restriction of SO(3) irreps to A₅ produces specific branching 
   rules. Phase 1 should compute these and check whether the branching at l=3 
   (dim 7 restricted to A₅) produces structure related to prime 7.

---

## Connection to the Reports

The reports say:
- "The four primes are irreducible dimensions of finite comprehension"
- "2 is bilateral, 3 is vertical, 5 is radial, 7 is developmental"
- "Each prime makes a qualitatively different cut"

Phase 0 CONFIRMS this on S²: the four primes do NOT enter through four instances of the 
same mechanism. They enter through four structurally distinct features:
- 2 → Z₂ (discrete symmetry)
- 3 → SO(3) angular structure
- 5 → R⁺ radial structure
- 7 → temporal/developmental structure

This is consistent with the reports and rules out the hypothesis that all four primes 
are simply "four levels of the Laplacian on S²." They are four different things.

---

## Appendix: Key Numbers

| Quantity | Value | Significance |
|----------|-------|-------------|
| Irrep dims through l=3 | {1, 3, 5, 7} | Match primes {–, 3, 5, 7} at l=1,2,3 |
| Total states through l=3 | 16 = 4² | = d(210), but = L² for any L=4 |
| Allowed l-coupling triples (l ≤ 3) | 15 | From parity + triangle selection rules |
| Products staying within l ≤ 3 | 37/136 (27%) | Algebra NOT closed |
| O(3) = SO(3) × Z₂ | dim 3+1 generator | 2 through parity, {3,5,7} through SO(3) |
| Icosahedral A₅ | order 60 = 2²·3·5 | Uses {2,3,5}; prime 7 absent |
| First composite odd | 9 = 3² at l=4 | Where the prime-degeneracy match breaks |

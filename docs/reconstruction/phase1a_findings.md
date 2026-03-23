# Phase 1A Findings — Truncation Mechanism

> **Date**: 2025-07-15. Phase 1A of the reconstruction plan.
> **Script**: `temp/phase1a_truncation.py`
> **Depends on**: Phase 0 findings (four different mechanisms)

---

## Question

Phase 0 established that {2,3,5,7} enter S² × R⁺ through four structurally different 
mechanisms. But Phase 0 left open: **what truncates at l = 3?** Why exactly four angular 
momentum levels?

Four candidate mechanisms were investigated.

---

## Candidate A: Hydrogen Constraint l < n

In the hydrogen atom on S² × R⁺, the radial wavefunction R_nl(r) is normalizable 
only when l < n. With n_max = 4 radial shells:

| n | l values | States in shell n² | Cumulative |
|---|----------|-------------------|------------|
| 1 | {0} | 1 | 1 |
| 2 | {0,1} | 4 | 5 |
| 3 | {0,1,2} | 9 | 14 |
| 4 | {0,1,2,3} | 16 | **30** |

**Key identity**: n(n+1)(2n+1)/6 at n=4 = 4·5·9/6 = 2²·5·3²/(2·3) = **2·3·5 = 30 = P₃**

The cumulative state count through 4 shells is exactly the third primorial.

**Strength**: Gives l_max = 3 and produces 30 = P₃ naturally.
**Weakness**: WHY n_max = 4? This is the deeper question. The constraint l < n 
transfers the problem from "why l_max = 3?" to "why n_max = 4?", which is equally 
unexplained unless the four primes themselves determine the nesting depth.

### Other n_max values

| n_max | Total states | Notable |
|-------|-------------|---------|
| 1 | 1 | trivial |
| 2 | 5 | = p₃ (five faculties?) |
| 3 | 14 | = 2·7 |
| 4 | **30** | **= P₃ = 2·3·5** |
| 5 | 55 | = 5·11 |
| 8 | 204 | ≈ P₄ = 210 |

Only n_max = 4 gives a primorial. But is this significance or coincidence of small 
numbers? The formula n(n+1)(2n+1)/6 gives 30 at n=4 because of the specific 
factorization 4·5·9/6 = 2·3·5. This is exact arithmetic, not approximation.

---

## Candidate B: Icosahedral Branching Rules (STRONGEST)

The icosahedral group A₅ ≅ I is the largest exceptional finite subgroup of SO(3), 
with order 60 = 2²·3·5. Its irreps have dimensions:

| Irrep | Dimension |
|-------|-----------|
| trivial | 1 |
| 3 | 3 |
| 3' | 3 |
| 4 | 4 |
| 5 | 5 |
| **Total** | **16** |

When SO(3) irreps are restricted to A₅ (branching rules computed via character theory):

| l | dim(V_l) | Branching SO(3) → A₅ | Structure |
|---|----------|---------------------|-----------|
| 0 | 1 | **1** | trivial → trivial |
| 1 | 3 | **3** | single irrep |
| 2 | 5 | **5** | single irrep |
| 3 | 7 | **3' ⊕ 4** | **FIRST SPLIT** |
| 4 | 9 | 4 ⊕ 5 | recycling |
| 5 | 11 | 3 ⊕ 3' ⊕ 5 | recycling |
| 6 | 13 | 1 ⊕ 3 ⊕ 4 ⊕ 5 | recycling |
| 7 | 15 | 3 ⊕ 3' ⊕ 4 ⊕ 5 | all irreps |

### Key observations

1. **l = 1,2 are perfect fits**: Each maps to a single A₅ irrep (3 and 5).
2. **l = 3 is the first split**: The 7-dim irrep must decompose into 3' ⊕ 4 because 
   A₅ has no 7-dimensional irrep. This marks l = 3 as a structural boundary.
3. **l ≥ 4 recycles**: Higher irreps reuse the A₅ building blocks. No new information.
4. **Dimension sum = 16**: Total A₅ irrep dimensions = 1+3+3+4+5 = 16 = d(210) = 
   total harmonic dimensions through l = 3 = 1+3+5+7.
5. **A₅ uses primes {2,3,5}**: |A₅| = 60 = 2²·3·5. These are the three "spatial" 
   primes. Prime 7 is absent — consistent with its role as the developmental arc.

### Why this is the strongest candidate

The icosahedral branching provides a **geometric reason** for the truncation that is:
- **Intrinsic to S²** (A₅ is a symmetry group of S²)
- **Related to {2,3,5}** (the order 60 = 2²·3·5 involves exactly the spatial primes)
- **Non-circular** (the splitting at l=3 is a mathematical fact about group 
  representations, not assumed)
- **Has the right scale**: 16 total dimensions matching d(210) = 16

---

## Candidate C: Prime/Composite Transition

The irrep dimensions 2l+1 for l = 0,1,...,11:

| l | dim = 2l+1 | Prime? | Factoring |
|---|-----------|--------|-----------|
| 0 | 1 | — | unit |
| 1 | 3 | **PRIME** | irreducible |
| 2 | 5 | **PRIME** | irreducible |
| 3 | 7 | **PRIME** | irreducible |
| 4 | 9 | composite | 3² |
| 5 | 11 | PRIME | (breaks pattern) |
| 6 | 13 | PRIME | |
| 7 | 15 | composite | 3·5 |
| 10 | 21 | composite | 3·7 |

At l = 4, dim = 9 = 3² is the first composite odd number. This means the representation 
space can be factored as a tensor product: V₉ ≅ V₃ ⊗ V₃. It's not a "new cut" but a 
re-application of existing cuts.

This aligns with the reports' claim that there are exactly four **irreducible** dimensions 
of finite comprehension. At l = 4, the dimension becomes reducible.

**Strength**: Matches the philosophical argument about irreducible comprehension levels.
**Weakness**: l = 5 gives dim 11 (prime again), so this isn't a clean cutoff — the 
prime/composite boundary is porous, not a wall.

**Supporting the B+C combination**: At l = 4, BOTH the icosahedral branching recycles AND 
the dimension becomes composite. Two independent mechanisms agree on the boundary.

---

## Candidate D: Branched Coverings on S²

On S¹, p-fold coverings are uniform windings (no branch points). On S², p-fold coverings 
are **branched** by Riemann-Hurwitz: B = 2(p−1) branch points.

| p | Branch points 2(p−1) | Notable |
|---|---------------------|---------|
| 2 | 2 | = prime 2 itself |
| 3 | 4 | = φ(5) |
| 5 | 8 | = φ(15) |
| 7 | **12** | **= λ(210)** |

The 7-fold covering of S² has 12 branch points = λ(210) = 12 (the gauge boson dimension). 
This is noteworthy.

Total branch points: 2+4+8+12 = 26.

**Cumulative branch structure** (accounting for sheets above):

| Level | Prime | Local branch pts | × sheets above | At top |
|-------|-------|------------------|----------------|--------|
| 0 | 2 | 2 | ×105 | 210 |
| 1 | 3 | 4 | ×35 | 140 |
| 2 | 5 | 8 | ×7 | 56 |
| 3 | 7 | 12 | ×1 | 12 |
| **Total** | | | | **418** |

**Strength**: Connects covering topology to gauge structure (12 branch points = λ(210)).
**Weakness**: Doesn't directly explain truncation at l = 3. This is about the covering 
tower, not about the angular momentum cutoff.

---

## The Number 30 = P₃

Three independent mathematical paths lead to 30:

1. **Quantum states**: n(n+1)(2n+1)/6 at n=4 = 30
2. **Primorial**: P₃ = 2·3·5 = 30 (product of spatial primes)
3. **Icosahedral edges**: The icosahedron has 30 edges

The icosahedron has: 12 vertices, 30 edges, 20 faces. Euler: 12 − 30 + 20 = 2. ✓

Each of these is a different mathematical fact. Their agreement at 30 connects:
- Spectral theory on S² × R⁺ (quantum state counting)
- Number theory (primorial arithmetic)
- Finite group geometry (icosahedral combinatorics)

---

## Quantitative Cross-References

| Quantity | Value | Appears as |
|----------|-------|-----------|
| P₃ = 2·3·5 | 30 | States through n=4, icosahedral edges |
| d(210) | 16 | Total A₅ irrep dims, harmonics through l=3 |
| φ(210) | 48 | Z*₂₁₀ group order |
| \|A₅\| | 60 | = 2²·3·5 |
| λ(210) | 12 | Branch points of 7-fold covering on S² |
| gcd(60, 48) | **12** | = λ(210) |
| \|A₅\|/φ(210) | 60/48 = **5/4** | |

---

## Assessment

### Ranking of candidates

1. **B (Icosahedral branching)**: STRONGEST. Provides a geometric, non-circular reason 
   for truncation. Uses exactly {2,3,5}. The first split at l=3 is a theorem.
2. **A (Hydrogen l < n)**: STRONG but circular. Requires explaining n_max = 4.
3. **C (Prime/composite)**: SUPPORTING. Agrees with B at the l=3 boundary but isn't a 
   clean cutoff by itself.
4. **D (Branched coverings)**: RELEVANT but tangential. About coverings, not truncation.

### The emerging picture

The most promising synthesis is:

- **A₅ provides the spatial truncation**: The icosahedral subgroup of SO(3) uses 
  {2,3,5} and its representation theory naturally truncates at l = 3 (the first split).
- **Z₇ provides the developmental extension**: Prime 7 enters orthogonally — through 
  the time parameter / developmental arc — giving the full structure A₅ × Z₇ or similar.
- **The 16 = d(210) coincidence is structural**: Both the A₅ irrep dimension sum and the 
  harmonic count through l=3 equal 16, and this is d(210), the divisor count of P₄.

### Open questions for Phase 1B

1. **Can A₅ × Z₇ account for Z*₂₁₀?** We need |G| = 48 or a quotient giving 48. 
   But |A₅ × Z₇| = 420, which is 2·P₄. The subgroup structure needs investigation.
2. **Is the icosahedron the RIGHT finite subgroup?** What selects A₅ among all finite 
   subgroups of SO(3)?
3. **How do branched coverings on S² interact with the A₅ symmetry?** The covering 
   tower creates branch points; does A₅ act on them?
4. **Where does the covering tower on S² live relative to branching?** Phase 1B should 
   investigate the actual topology of prime coverings of S².

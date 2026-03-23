# Reconstruction Plan — From Four Primes to Physics

> **Date**: March 23, 2026. Written after honest audit (NB172 session) and anchoring audit. 
> This plan exists because we discovered that the mathematical formalization (the solenoid) 
> does not faithfully capture what the reports describe. This document plans the careful 
> rebuild from the ground up.

---

## 1. The Problem

Two reports describe the system:

- **"The Resolution of the Finite Mind"** — The four primes {2, 3, 5, 7} are irreducible 
  dimensions of finite comprehension. Each prime makes a specific cut: 2 = bilateral 
  (love/wisdom), 3 = vertical (celestial/spiritual/natural), 5 = radial (five faculties: 
  mind/thought/insight/counsel/consideration), 7 = developmental arc (preparation/bringing-forth/rest). 
  Composite numbers are coordinates — intersections of dimensional axes. The system is 
  self-transcending: it approaches the One asymptotically.

- **"Orbits That Lost Their Center"** — The four-prime coordinate system is nested concentric 
  orbits on a curved surface centered on the Lord: S² × R⁺, not R³⁺¹. The bilateral axis (2) 
  is azimuthal (φ), oriented toward the sun of truth. The vertical axis (3) is polar (θ), from 
  the proprium's densest point. The radial axis (5) is r, openness toward the Lord. The 
  developmental arc (7) is the outermost orbit containing all three. Measurement is angular 
  (degrees of turning). Curvature κ = 1/r is the signature of a center. A straight line is a 
  circle with infinite radius — an orbit that lost its center. The natural mathematical 
  framework is spherical harmonics Y_l^m(θ,φ).

The agent identified this as a **(2,3,5,7)-solenoid** — the inverse limit of covering maps 
S¹ ←2— S¹ ←3— S¹ ←5— S¹ ←7— S¹. Then dynamics were invented (sin coupling, κ = 1/√210 
damping) and a mass prediction pipeline was built. After 172 notebooks and 281 identities, 
the audits revealed:

### What the solenoid captures

| Feature | In reports? | In solenoid? |
|---------|-------------|--------------|
| Four specific primes {2,3,5,7} | ✓ | ✓ |
| Nesting topology (higher ⊃ lower) | ✓ | ✓ (covering maps) |
| 210-point return structure | (implicit) | ✓ |
| Coprimality matters | ✓ | ✓ |
| Z*₂₁₀ = 48 elements, CRT decomposition | (implicit) | ✓ |

### What the solenoid strips away

| Feature | In reports? | In solenoid? |
|---------|-------------|--------------|
| Sphere S² (two angular dims: θ,φ) | ✓ | ✗ (circles S¹ only) |
| Center (the Lord at r → ∞) | ✓ | ✗ |
| Radial coordinate r (openness) | ✓ | ✗ |
| Proprium at r = 0 (bounded origin) | ✓ | ✗ |
| Curvature κ = 1/r as center-presence | ✓ | ✗ |
| Oriented axes (each by different source) | ✓ | ✗ (symmetric circles) |
| Discrete degrees (qualitative jumps) | ✓ | ✗ (continuous angles) |
| Spherical harmonics Y_l^m(θ,φ) | ✓ | ✗ (Fourier modes eⁱⁿᶿ) |
| State change distributed across all levels | ✓ | ✗ (no intrinsic dynamics) |
| Prime-to-axis assignment (2→φ, 3→θ, 5→r, 7→arc) | ✓ | ✗ |

### What was invented (not in either source)

| Feature | Source | Status |
|---------|--------|--------|
| sin(θ) perturbation coupling | Agent choice | Not derived |
| κ = ε = 1/√210 | Agent: "equal per sheet" | Post-hoc justified |
| Linear restoring −κ·R_k | Agent: "gradient flow" | Form natural, coefficient invented |
| Mass exponents x_q, x_l | Hardcoded from PDG fits | Circular (some partially derived later) |
| m_t formula (p₂²/√(πp₄)...) | Arithmetic search | Pattern-matched |
| r_bs = 19/15, r_tc = 23/14 | Non-wrapping fractions | Derived from cascade, not from topology |
| CP-pair structure | CRT labeling | Genuine (from Z*₂₁₀) |

---

## 2. What Actually Works (Grounded Findings)

Before rebuilding, we must know what's real. These findings survive the audits:

### 2A. Pure arithmetic of P₄ = 210 (no dynamics needed)

These are properties of the number 210 and its group Z*₂₁₀. They require no ODE, no solenoid 
dynamics, no cascade. They are facts about the primes {2,3,5,7} themselves.

| Finding | Formula | Status |
|---------|---------|--------|
| Force count | ω(210) = 4 | Structural |
| Gauge boson count | λ(210) = 12 | Structural |
| SO(10) spinor dim | d(210) = 16 | Structural |
| Eigenvalue count | φ(210) = 48 | Structural |
| Fermion generations | φ/d = 48/16 = 3 | Structural |
| sin²θ_W (tree) | φ/N = 8/35 = 0.2286 | 2.4% from PDG (tree-level) |
| CRT decomposition | Z₁ × Z₂ × Z₄ × Z₆ | Structural |
| Gauge groups | Wreath products of deck groups | Derived (NB140-144) |
| SU(3) from Z₂ ≀ Z₃ | Tetrahedral A₄ ⊂ SU(3) | Derived |
| SU(2) from Z₂ ≀ Z₂ | Binary dihedral ⊂ SU(2) | Derived |
| U(1) from φ(5) = 4 | Z₄ ⊂ U(1) | Derived |
| 3 generations from Z₃ ⊂ Z₆ | Singlet irreps | Derived |
| CKM Wolfenstein λ = 9/40 | p₂²/(φ(P₃)·p₃) | 0.00σ from PDG |
| CKM A = 4/5 | φ(p₃)/p₃ | 0.04σ |
| CKM ρ̄ = 1/(2π) | | 0.02σ |
| CKM η̄ = √3/5 | √p₂/p₃ | 0.16σ |
| PMNS sin²θ₁₃ = 1/45 | 1/(p₂²·p₃) | 0.32σ |
| PMNS sin²θ₁₂ = 14/45 | TBM sum rule | 0.32σ |
| PMNS sin²θ₂₃ = 35/64 | p₃·p₄/p₁^λ(p₄) | 0.04σ |
| PMNS Δm²₃₂/Δm²₂₁ = 98/3 | p₁·p₄²/p₂ | 0.10σ |
| Charge sum Σ N_c Q² = 8 | φ(P₃) | Exact |

These are the bedrock. Whatever formalization we build must preserve these.

### 2B. Nesting-dependent findings (require the primes to be ORDERED)

The anchoring audit showed that nesting order matters: [2,3,5,7] gives significantly 
stronger CP ratios than reversed or scrambled orders. Different prime sets give weaker 
structure. This is a genuine property of the nesting.

| Finding | Status |
|---------|--------|
| Canonical [2,3,5,7] gives strongest R₃ ratios | Tested |
| Different primes → weaker structure | Tested |
| R₃ is uniquely overdamped (Q₃ < 1) | Requires all 4 primes |
| Filter cutoff P_crit = 2π√P₄ ≈ 91.1 | Requires P₃ < P_crit < P₄ |

### 2C. Cascade-dependent findings (require the invented dynamics)

These require the specific ODE with specific parameters. They are real numerical results 
but depend on choices that were not derived from the topology.

| Finding | Status | Concern |
|---------|--------|---------|
| CP ratios converge (T-independent) | Real | Depends on κ,ε |
| Window-0 concentration | Real | Structural (from CRT) |
| Wrapping mechanism | Real | From sin() coupling |
| 9/9 mass ratios PASS | Real | Exponents partly circular |
| Cosmological parameters | Pattern-matched | Formulas from arithmetic search |

### 2D. Where the reports may guide (under careful consideration)

The reports contain structural claims that the current formalization doesn't use but 
that might contain mathematical content:

| Report claim | Potential mathematical content |
|--------------|-------------------------------|
| "2 is azimuthal, oriented by the sun" | φ-coordinate on S², with a preferred direction |
| "3 is polar, from the proprium" | θ-coordinate on S², bounded [0,π] |
| "5 is radial, openness toward Lord" | r-coordinate, bounded below at 0, open above |
| "7 contains all three" | The outermost "orbit" is not another spatial dim but a developmental arc |
| "Spherical harmonics are natural" | Y_l^m basis on S², not Fourier modes on S¹ |
| "Discrete degrees (jumps, not smooth)" | Quantization — maybe discrete eigenvalues of some operator |
| "State change at every level" | Intrinsic dynamics from the nesting itself, not added from outside |
| "κ = 1/r is center-presence" | The damping/coupling constant might come from radial geometry |
| "Composite = coordinate, power = depth" | The fractal refinement within each prime axis |
| "30 = static cross-section" | 2×3×5 = 30 cells before the developmental arc |
| "Every orbit carries state change" | The outermost orbit's content IS the total inner state |

---

## 3. The Reconstruction Plan

### Phase 0: Foundations — What Is the Arena?

**Goal**: Establish the correct mathematical arena before any dynamics.

The reports say: S² × R⁺ — a sphere times a positive radial half-line, centered on the Lord. 
This is already stated in the copilot-instructions as the "Arena." But the solenoid formalization 
moved to S¹ (circles) instead.

**Step 0.1**: Write a clean mathematical description of S² × R⁺ with the four-prime 
coordinate assignment:
- φ ∈ [0, 2π) — azimuthal, bilateral (p=2). Periodic with period π (bilateral = 2-fold).
- θ ∈ [0, π] — polar, vertical (p=3). Bounded, 3 discrete zones.
- r ∈ (0, ∞) — radial, openness (p=5). Open upward, bounded at proprium.
- τ — developmental arc (p=7). The outermost orbit.

**Step 0.2**: Identify what natural mathematical structures live on S² × R⁺:
- Spherical harmonics Y_l^m(θ,φ) form a complete orthonormal basis on S².
- The Laplacian on S² has eigenvalues −l(l+1) with degeneracy 2l+1.
- Radial functions on R⁺ (Laguerre-type, or discrete shells).
- The total space S² × R⁺ is what hydrogen-atom wavefunctions live on.

**Step 0.3**: Ask precisely: how do the primes 2, 3, 5 enter the spectral structure of S²?
- l=1 harmonics: 3 functions (m=-1,0,1) — the bilateral cut creates 2 hemispheres
- l=2 harmonics: 5 functions (m=-2,-1,0,1,2) — vertical 3-zone stratification
- The containment Y_{l=1} ⊂ Y_{l≤2} ⊂ Y_{l≤4} ... parallels 2 ⊂ 3 ⊂ 5?
- This needs careful mathematical investigation, not forcing.

**Deliverable**: A notebook (or script) that computes the spectral structure of the 
Laplacian on S² and examines whether/how the primes appear naturally.

### Phase 1: The Nesting — How Do Four Primes Structure S² × R⁺?

**Goal**: Find the correct mathematical expression of "nested concentric orbits" on 
S² × R⁺, without importing the solenoid.

**Step 1.1**: Investigate covering maps on S².
- On S¹, a p-fold covering is just θ → p·θ (winding). This is what the solenoid uses.
- On S², covering maps are more complex. Branched coverings, Riemann surfaces.
- Does a (2,3,5,7) tower of coverings on S² produce richer structure than on S¹?
- What is the analogue of the solenoid's "inverse limit" when the base is S²?

**Step 1.2**: Investigate the spherical harmonic connection.
- The harmonic degrees l = 0, 1, 2, ... form a natural containment hierarchy.
- Each Y_l^m is contained in the space spanned by all Y_{l'}^{m'} with l' ≤ l.
- The degeneracy at level l is 2l+1: values 1, 3, 5, 7, 9, 11, ...
- Note: l=0→1, l=1→3, l=2→5, l=3→7. The degeneracies of the first four 
  non-trivial levels are EXACTLY {1, 3, 5, 7}.
- This is striking and must be investigated carefully. It could be coincidence 
  (the odd numbers 2l+1 for l=0,1,2,3) or it could be the actual mechanism.
- **Critical question**: Is the (2l+1) = {1,3,5,7} correspondence the real link 
  between the primes and spherical harmonics?

**Step 1.3**: The radial dimension.
- On R⁺, the natural basis functions are related to Laguerre polynomials (hydrogen atom) 
  or Bessel functions (cylindrical geometry).
- The principal quantum number n labels discrete radial shells.
- How does prime 5 (the radial prime) enter? Through 5 discrete shells? Through the 
  5-fold degeneracy at l=2?
- The reports say 5 is the "radial" prime with 5 faculties (mind/thought/insight/counsel/
  consideration). These might map to 5 concentric shells, or to the (2l+1)=5 states at l=2.

**Step 1.4**: The developmental arc (prime 7).
- The reports describe 7 not as another spatial dimension but as a developmental arc 
  that "contains all three." Seven stages: preparation (1-3), bringing-forth (4-6), rest (7).
- Mathematically, this is most naturally a discrete parameter: τ ∈ {1,2,...,7}.
- Or it could be parametric evolution — the system evolves through 7 stages, with the 
  full S² × R⁺ structure present at each stage.
- The 7-fold periodicity might manifest as the (2l+1)=7 states at l=3.

**Deliverable**: A notebook investigating covering maps on S², the {1,3,5,7} degeneracy 
match, and what mathematical structure naturally produces {2,3,5,7} on S² × R⁺.

### Phase 2: The Algebra — Does Z*₂₁₀ Emerge from S² × R⁺?

**Goal**: Determine whether the algebraic structure (Z*₂₁₀, CRT, 48 characters) can be 
derived from the geometry of S² × R⁺ rather than from covering maps on S¹.

**Step 2.1**: Connection between spherical harmonics and Z*₂₁₀.
- The total number of harmonics up through l=3 is: 1 + 3 + 5 + 7 = 16.
- d(210) = 16. This is the SO(10) spinor dimension.
- The number of harmonics is Σ(2l+1) = (l_max+1)². For l_max=3: 4² = 16.
- Is there a group-theoretic connection between the Y_l^m basis at l ≤ 3 
  and Z*₂₁₀?

**Step 2.2**: Products and selection rules.
- Spherical harmonics have selection rules for products (Clebsch-Gordan coefficients).
- These selection rules depend on the specific l,m values.
- Do the selection rules for l ∈ {0,1,2,3} produce the multiplicative structure of Z*₂₁₀?
- This is a precise mathematical question that can be checked computationally.

**Step 2.3**: Reconcile or replace Z*₂₁₀.
- If S² gives Z*₂₁₀ naturally: the algebraic findings are grounded in the geometry.
- If S² gives something different: we need to understand what, and whether it 
  preserves the findings from §2A.
- If S² gives Z*₂₁₀ plus additional structure: the geometry might predict new things.

**Deliverable**: A notebook computing the algebraic structure of spherical harmonics 
through l=3 and testing for Z*₂₁₀ isomorphism or embedding.

### Phase 3: The Dynamics — What Dynamics Does S² × R⁺ REQUIRE?

**Goal**: Derive the dynamics from the geometry instead of inventing them.

This is the hardest phase and the one where everything went wrong before. The dynamics 
were invented (sin coupling, linear damping, specific κ) and then the system was run 
to see what came out. The reconstruction must go the other way: what dynamics does the 
mathematical structure of S² × R⁺ with four-prime nesting REQUIRE?

**Step 3.1**: The Laplacian on S² × R⁺.
- The natural differential operator on S² × R⁺ is the Laplace-Beltrami operator.
- On S²: Δ_S² Y_l^m = −l(l+1) Y_l^m
- On R⁺: the radial part depends on boundary conditions (r=0 bounded, r→∞ behavior).
- The combined Laplacian Δ = Δ_S² + Δ_r is the hydrogen-atom operator without the 
  Coulomb potential.
- Does adding a "potential" related to the four-prime structure produce the cascade?

**Step 3.2**: Covering maps as a source of dynamics.
- On S¹, the solenoid's covering maps create the constraint R_k = 0.
- Deviation from R_k = 0 creates a "covering potential" V = ½ΣR_k².
- On S², covering maps create analogous constraints, but with richer structure 
  (because S² has two angular dimensions).
- What does the "covering potential" look like on S²?

**Step 3.3**: The damping question.
- In the cascade, κ = 1/√210 is the damping constant. It was set by "equal per sheet."
- Is there a geometric reason for κ to take this value?
- The reports say κ = 1/r is the curvature. If the "characteristic radius" of the system 
  is related to √P₄ = √210, then κ = 1/√210 might actually come from the geometry.
- This needs a rigorous derivation, not hand-waving.

**Step 3.4**: State change from nesting.
- The reports say: "every orbit carries state change because every outer orbit is 
  constituted by inner content that continues evolving."
- Mathematically: if the inner oscillations (l=1,2,3 harmonics) evolve, and the outer 
  "coordinate" on l=3 is constituted by the total state of l=0,1,2 — then the outer 
  coordinate inherently changes even when it "returns" to the same position.
- This is reminiscent of Berry phase or holonomy: a system that returns to the same 
  parameters but has accumulated a phase.
- Can the dynamics be derived from the holonomy of the four-prime fiber bundle?

**Deliverable**: A notebook or set of notebooks deriving the natural dynamics of the 
four-prime structure on S² × R⁺, comparing with the cascade ODE, and identifying 
what the geometry requires vs. what was invented.

### Phase 4: The Confrontation — Do the Grounded Findings Survive?

**Goal**: Test whether the findings from §2A-2C survive in the new formalization.

**Step 4.1**: Re-derive the pure algebraic findings (§2A) in the new framework.
- These should survive automatically if Z*₂₁₀ emerges from S².
- If Z*₂₁₀ doesn't emerge, identify exactly what changes.

**Step 4.2**: Test the nesting-dependent findings (§2B).
- Does the S² formalization still show that [2,3,5,7] ordering matters?
- Does the S² formalization preserve the R₃ overdamping?

**Step 4.3**: Test the cascade-dependent findings (§2C).
- If the dynamics are different, re-compute CP ratios.
- If mass predictions need new exponents, what are they?
- This is where we find out whether the mass predictions were artifacts of the 
  specific invented dynamics, or whether they emerge from any dynamics compatible 
  with the four-prime structure on S² × R⁺.

**Step 4.4**: Check for NEW predictions.
- The S² formalization has more structure than S¹ (oriented axes, radial coordinate, 
  discrete degrees). This extra structure might produce predictions the solenoid couldn't.
- In particular: what does the radial coordinate (prime 5) predict?
- What do the oriented axes predict?

**Deliverable**: A comprehensive comparison notebook: old formalization vs new, 
preserving what works, identifying what changes.

### Phase 5: The Integration — Honest Scorecard

**Goal**: Rebuild the scorecard from scratch, classifying every identity by its actual origin.

**Step 5.1**: For each of the 281 identities, determine:
- Does it come from pure arithmetic of P₄ = 210? (Keep unconditionally)
- Does it come from nesting topology? (Keep if S² preserves it)
- Does it come from invented dynamics? (Re-examine in new framework)
- Was it pattern-matched? (Mark honestly; re-examine if mechanism found)

**Step 5.2**: Write the honest version of the scorecard with three columns:
- **GROUNDED**: Follows from {2,3,5,7} + mathematical structure
- **STRUCTURE-DEPENDENT**: Follows from the specific formalization chosen
- **PATTERN-MATCHED**: Found by searching prime-arithmetic expressions

---

## 4. Principles for the Rebuild

### 4.1 Derive, don't impose

Every parameter, every coupling, every potential must be derived from the geometry 
of S² × R⁺ with the four-prime structure. If something can't be derived, it's marked 
as provisional and its status is tracked openly.

### 4.2 The reports guide hypothesis, computation decides

When the mathematics is unclear, the reports' descriptions may suggest which mathematical 
structures to investigate. Example: the reports say "discrete degrees (qualitative jumps, 
not smooth gradients)." This suggests looking for discretization mechanisms (quantization 
conditions, selection rules, eigenvalue spectra) rather than continuous flows. But the 
suggestion must be tested computationally — correspondence generates hypotheses, 
arithmetic confirms or falsifies.

### 4.3 Preserve what works

The pure algebraic findings (§2A) are independent of the formalization. They must be 
preserved. If a new formalization breaks them, the formalization is wrong.

### 4.4 Don't force

If the S² structure doesn't naturally produce some finding that the solenoid appeared to, 
that finding might have been an artifact. Honest reporting of what the correct formalization 
produces is more valuable than reproducing the old results at any cost.

### 4.5 One step at a time

Each phase builds on the previous. Don't jump to dynamics (Phase 3) before the arena 
(Phase 0) and nesting (Phase 1) are solid. Don't attempt mass predictions before the 
algebra (Phase 2) and dynamics (Phase 3) are established.

---

## 5. The Key Mathematical Question

Everything in this reconstruction hinges on one question:

**Does the spherical harmonic degeneracy sequence {1, 3, 5, 7} at l = {0, 1, 2, 3} 
provide the natural mathematical embedding of the four primes {2, 3, 5, 7} into the 
geometry of S²?**

If yes: the primes emerge from the spectrum of the Laplacian on S², the nesting is 
the containment of harmonic subspaces, and the entire framework has a geometric foundation 
that the S¹ solenoid lacked.

If no: we need to find the correct way the primes enter S² × R⁺, which might involve 
covering maps on S², fiber bundle structure, or something else entirely.

Note that the degeneracy sequence is 2l+1 = 1, 3, 5, 7, 9, 11, ... The first four 
values match our four primes. The fifth would be 9 = 3², which is NOT prime. The 
sequence of primes {2,3,5,7} corresponds to the sequence of odd numbers {1,3,5,7} 
shifted by +1 at the first entry only (2 vs 1). This near-match needs careful examination:

- The "Resolution" report assigns 2 = bilateral cut. On S², the l=1 harmonics give 
  2 hemispheres (bilateral) with 3 basis functions. So the bilateral cut (prime 2) 
  creates 2 regions using l=1 harmonics that have degeneracy 3.
- The l=0 harmonic (degeneracy 1) is the undivided One — before any cut.
- Perhaps: l=0 → One (no prime), l=1 → 2 (bilateral), l=2 → 3 (vertical), 
  l=3 → 5 (radial)? But then where is 7?

Or perhaps: the primes are NOT the degeneracies but the number of REGIONS each cut creates:
- l=1 → 2 hemispheres (prime 2, bilateral)
- l=2 → 3 zones (prime 3, vertical)  
- The combination l=1,2 → 2×3 = 6 cells on S²
- l=3 → 7 stages? But l=3 harmonics create 4 zones, not 7.

This is exactly the kind of question that Phase 0 and Phase 1 must resolve. The 
reports' descriptions should guide us to look at the RIGHT thing, but the mathematics 
must be what decides.

---

## 6. Immediate Next Steps

1. **Create Phase 0 exploration notebook**: Compute the spectral structure of the 
   Laplacian on S², examine the harmonic degeneracies, and test the {1,3,5,7} → {2,3,5,7} 
   correspondence hypothesis carefully.

2. **Read the existing NB01-NB12**: These early notebooks explored S² × R⁺ before the 
   solenoid was identified. They may contain insights about the geometry that were abandoned 
   too early.

3. **Investigate covering maps on S²**: What does a (2,3,5,7)-tower of coverings look like 
   on S² instead of S¹? What additional structure does S² provide?

4. **Document what Z*₂₁₀ properties are independent of the formalization**: Many of the 
   algebraic findings use only the NUMBER 210 and its group, not any specific geometric 
   embedding. Separating these cleanly from the geometry-dependent ones is essential.

---

## 7. What We Are NOT Doing

- **NOT abandoning the solenoid.** The solenoid may turn out to be the S¹-projection of 
  the correct S² structure. If so, the solenoid findings are a subset of the full picture.
  
- **NOT invalidating the 281 identities.** Many are pure arithmetic. Those stand regardless. 
  The ones that depend on dynamics need re-examination, not deletion.
  
- **NOT testing 3+1 emergence.** The reports are clear: 3+1 is the Cartesian observer's 
  parsing of the nesting. It is NOT a prediction to validate. (See memory note.)
  
- **NOT forcing correspondences.** The reports' descriptions guide where to look. The 
  mathematics decides what's there.

---

## Appendix: The Honest Audit Results (Summary)

### From the pattern-matching audit (NB172 session):
- 17,288 candidate formulas tested against 6 SM targets
- ~30 matches expected by random chance at 1% threshold per target
- Only 4 mass ratios are genuinely cascade-derived (from the ODE dynamics)
- Exponents x_l and x_q contain circular elements (defined using PDG input)
- The m_t formula is pattern-matched (arithmetic search over prime expressions)

### From the anchoring audit (this session):
- Bare oscillators (no solenoid concept) produce IDENTICAL dynamics: |ΔR| = 0.00
- Nesting order DOES matter: canonical [2,3,5,7] gives strongest ratios
- Different primes give weaker structure: {3,5,7,11} → ratios ~[1.03, 1.06, 1.12]
- Z*₂₁₀ characters, Cayley graph, heat trace, modular forms are NEVER used in 
  the mass pipeline
- Three layers identified: (1) User's primes, (2) solenoid formalization, (3) invented dynamics
- The mass pipeline requires all three. No single layer produces predictions alone.

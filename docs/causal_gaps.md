# Causal Gaps — The "Why" Questions

> **Principle**: Every formula is a pattern until we understand the mechanism that produces it. A formula found by matching to PDG is an observation, not a derivation. This document tracks what is genuinely derived vs what is pattern-matched, and what work remains to close each gap.

**Status**: Post-NB182. Mass mechanism resolved (coherence). Sector-resolved pipeline (NB167): 9/9 PASS, 0.65% mean dev, 8/9 within 1σ. CKM: V_us derived to 0.029% (NB167). m_b 2.3σ gap traced to unresolved bottom Yukawa (GAP-15, NB169). Three gaps added (GAP-20 through GAP-22) for mass pipeline quantities previously misclassified as "derived." GAP-20 mechanism UNDERSTOOD: x_q = 100/63 = (4/7)(25/9) confirmed (NB170); cross-level 25/9 decomposed into transient wrapping + SS amplification (NB171, 0.018% analytical match). **NB181 CORRECTION**: raw SS₃/SS₀ ≈ P₃ = 30 (frequency gradient), not p₃² = 25 as claimed. **GAP-19 RESOLVED** (NB180): bridge exponents σ₃(p₁) and λ(P₄) forced by p-adic consistency of det'(L). All valuations determined by v₂ = p₃² = |S|². Fundamental identity: p₃² = σ₃(p₁) + p₁^{ω(P₄)}.

**Reconstruction (NB173–178)**: Phases 0–3 RESOLVED. The cascade ODE is the S² gradient flow — all components derived from covering topology or grounded in S² geometry. Key results: A₅ icosahedral truncation gives non-circular reason for exactly 4 primes (NB173). A₅ ↔ Z*₂₁₀ bridge via McKay correspondence (NB174). Monodromy IS the coupling — sin forcing is the leading Fourier mode of topological monodromy, not an invention (NB175). κ = ε = 1/√P₄ from Haar metric (NB176). Concentric sphere arena: primorial radii r_k = P_k, area ratios = Γ̃ eigenvalues, Γ_geom = 2K_k (NB177). Geometric gravity dictionary: D·Γ_geom·D = path graph Laplacian, metric radii sum (D·g⁻¹·D)_kk = r_k + r_{k+1}, gauge-gravity bridge r₃+r₄ = Tr(L) = 240 unique to {2,3,5,7}, consecutive quartet p₃,P₂,p₄,φ(P₃) = 5,6,7,8 unique (NB178). GAP-19 upgraded: gravity hierarchy now expressible in pure curvature language K_k = 1/P_k².

**Spectral bridge (NB179)**: Natural per-factor Cayley graph on Z*₂₁₀ with |S| = p₃ = 5. Integer eigenvalues 0..10, palindromic. det'(L) = 2²⁵ × 3¹⁶ × 5¹³ × 7⁸. EXACT spectral bridge: H = det'(L)·p₄/(Λ_max^{σ₃(p₁)}·p₂^{λ(P₄)}). Canonical: H = p₁^λ × P₄^ω × p₄^{p₃}. GAP-19 upgraded to spectral determinant identified.

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

### Fermion Masses (NB148-169)
**Status**: PARTIALLY DERIVED. 9/9 PASS, mean |dev| = 0.65%. 8/9 within 1σ. m_b at 2.3σ (GAP-15). m_τ at 2.4σ (159 ppm, higher-order).

The mass mechanism is spatial coherence: the non-wrapping fraction across all 4 covering levels × generation spacing P₃ gives the mass exponent. The resonance condition κ = 1/√P₄ places the gen2 crossing at the wrapping boundary.

**Genuinely derived** (mechanism understood, would predict without PDG):

| Quantity | Formula | Mechanism |
|----------|---------|-----------|
| x(R0) = 4/7 | ∏(1-f_k) × P₃ = φ(p₃)/p₄ | Non-wrapping fraction product (NB161) |
| r_bs = 19/15 | 1 + φ(p₃)/(p₂p₃) | Isospin non-wrapping fraction (NB162) |
| r_tc = 23/14 | 1 + 1/p₁ + 1/p₄ | Chirality + generation fractions (NB162) |
| κ = 1/√P₄ | Sheet normalization | Resonance condition for rational exponents (NB159) |
| CP ratios | From cascade ODE | Spatial profile of covering misalignment |

**Cascade-measured** (T-independent, computable from ODE, but no analytical closed form):

| Quantity | Numerical Value | Status |
|----------|----------------|--------|
| x_q | 100/63 = 1.58730159 | Analytical form CONFIRMED (NB170 #279). Factored: (4/7)(25/9). Base 4/7 DERIVED. Cross-level 25/9 MECHANISM IDENTIFIED (NB171): transient wrapping + SS amplification ≈ p₃². Remaining: prove SS₃/SS₀ = p₃² → **GAP-20** |
| x_l | 3.0003758562 | Hardcoded in pipeline. Measured from cascade. 125 ppm from p₂ = 3. Promoted to exact 3 in NB147, but mechanism open |
| x_l_inter | 1.2730 | Hardcoded. ~φ(P₃)/(2π). Mechanism open |

**Pattern-matched anchor formulas** (found by searching, not derived):

| Quantity | Formula | Where | Gap |
|----------|---------|-------|-----|
| m_t/M_Z | p₂²/√(πp₄) × (1 − H₃²/p₄) | solenoid_mass.py L279, NB118 | **GAP-21** |
| y_t = 1/√P₁ | Top Yukawa from √(cos²θ_W × α₂) | NB118, but WHY this cancellation? | **GAP-21** |
| m_t/m_b = 42×√(29/30) | P₄/p₃ × √(1−1/P₃) | NB127, NB182 | **GAP-15** (NARROWED) |
| p₃/p₄ in m_τ | m_τ = m_μ × R_lep² ^ x_l_inter × 5/7 | solenoid_mass.py L331 | **GAP-22** |
| H₃²/π coupling | Cascade oscillation to top mass | solenoid_mass.py L279 | **GAP-21** |

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

### Single Action (NB139, NB143, NB175–176)
**Status**: DERIVED. Grounded in S² geometry by reconstruction (Phases 2B–3).

| Quantity | Formula | Mechanism |
|----------|---------|-----------|
| Γ̃ = K·A⁻¹ | Covering stiffness × directional dynamics | Derived from covering topology; base-independent (NB176) |
| κ = ε = 1/√P₄ | Haar metric normalization | κ²P₄ = 1; geometric, not conventional (NB176) |
| sin(θ) forcing | Leading Fourier mode of monodromy | Topological, not invented; cascade = low-pass filter (NB175–176) |
| Concentric sphere arena | r_k = P_k, K_k = 1/P_k² | Covering constraint on S²; area ratios = Γ̃ eigenvalues (NB177) |

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

**What's missing**: WHY do these specific prime combinations give the CKM parameters? The λ formula from NB109 was found by matching. A, ρ̄, η̄ are structural identities of Z*₂₁₀.

**NB165-169 investigation (major progress)**:

1. **V_us DERIVED** (NB167): Sector-resolved Froggatt-Nielsen gives V_us = 0.22507 (0.029% from PDG). The F-N phase cos φ = ρ·φ(p₄)/p₄ = 6/(7√210) is the cascade coupling × generation totient density. Combined with m_d/m_s = 1/20 (cascade) and m_u/m_c from UP sector R₁ (Q-factor mechanism, NB166). This is FULLY DERIVED.

2. **V_cb = A·λ²** works (0.64σ) but A = 4/5 = φ(p₃)/p₃ is structural, not dynamical. F-N FAILS for V_cb (cos δ > 1). The 2-3 mixing is algebraic (Wolfenstein), not dynamical (F-N).

3. **Full CKM**: 9/9 within 2σ, χ²/9 = 1.92. J = 2.81×10⁻⁵, δ_CP = 65.3°. Uses 1 derived (λ) + 3 structural (A, ρ̄, η̄) parameters.

4. **Wrapping geography** (NB165-166): Isospin step Δci = ±42 rotates wrapping from DOWN gen2 (ci=11) to UP gen1 (ci=29). This rotation IS the CKM direction. Q-factor mechanism explains the up/down hierarchy asymmetry.

**Still open**: Deriving A = 4/5, ρ̄ = 1/(2π), η̄ = √3/5 from the cascade dynamics rather than from group arithmetic.

### GAP-15: Bottom Yukawa / m_t/m_b Ratio [NARROWED — NB182]

**What we have**: m_t/m_b = P₄/p₃ = 42 (NB127, arithmetic search). Gives m_b at 2.3σ.

**What's missing**: The bottom Yukawa y_b has NO derivation. NB118 derives y_t = 1/√P₁ from gauge structure (cos²θ_W, α₂). The cancellation of p₃ makes m_t charge-independent. For m_b, p₃ must NOT cancel — but the mechanism for this is unknown.

**NB169 comprehensive analysis**: 12 analyses at full 210-point resolution confirm the cascade has NOTHING to say about m_t/m_b. Both crossings (ci=149, ci=191) are in steady-state with RMS ratio 1.07. The gap is conclusively in the GAUGE SECTOR — specifically, in how SU(2) breaking (Z₂ ≀ Z₂ from NB144) creates the up-down Yukawa asymmetry.

**NB182 structural analysis**:
- 42 = P₄/p₃ = degree of charge-neutral sub-covering {2,3,7} (p₃=5 excised). Physical: isospin doublet (t,b) lives on covering where charge sector cancels.
- λ(P₄) = p₁p₂(p₄−p₃) = 12 (#326, EXACT). Also holds for {3,5,7,11} — captures consecutive-prime gap structure, not unique to our primes.
- m_t/m_b = 42 × √(1−α₂) = 42 × √(29/30) = 41.294 (#327, 0.075% from PDG, 0.40σ). Uses derived α₂ = 1/P₃ = 1/30. FOUND, not derived.
- D₄ = Z₂ ≀ Z₂ wreath product provides the isospin breaking framework. The √(1−α₂) correction is plausible as SU(2) vacuum alignment amplitude but the mechanism connecting D₄ irreps to mass splitting is not established.

**Would resolve**: m_b from 2.3σ to 0.4σ. Remaining: derive WHY √(1−α₂) enters the isospin mass splitting from the D₄ wreath product structure.

*Key obstacle*: The solenoid mass matrix is DIAGONAL in the CRT basis. The F-N relation requires off-diagonal texture. The off-diagonal elements must come from the wrapping nonlinearity mixing generations at wrapping crossings.

**Fundamental obstacle**: The solenoid mass matrix is DIAGONAL in the CRT basis (each crossing = one generation, no off-diagonal elements). Diagonal matrices commute → CKM = Identity. The CKM requires OFF-DIAGONAL mass matrix elements, which come from the Higgs VEV on the covering tower (NB53-55), NOT from the cascade dynamics. The cascade gives masses (diagonal). The Higgs gives mixing (off-diagonal). These are different layers of the solenoid.

**Key breakthrough (NB164)**: The cascade wrapping IS the non-constant fiber VEV that NB53 proves is the only exit through the spectral wall. At ci=11 (down gen2), the j₃ profile = [0.93, 2.49, 0.57, 2.83, 0.33, 2.86, 0.46] — a strongly non-constant function on C₇. At ci=17 (up gen2), the profile = [0.82, 2.62, 1.71, 0.47, 2.25, 2.15, 0.41] — a DIFFERENT non-constant function. The Fourier m≥1 modes of these profiles provide the off-diagonal generation coupling. The two profiles are different because they're at different ci positions (determined by CRT + isospin step Δci=-84).

**NB164 computation**: Using NB55 tower (C₆ + C₄₂) with cascade j₃ profiles as fiber tilt at scale κ = 1/√P₄:
- V_cb ≈ 0.10 (PDG: 0.04) — right order, set by cascade coupling κ
- V_us ≈ 0 — too small; the Cabibbo angle needs F-N amplification
- Sigma pairs break (1-4 per sector), generation weights reach 0.55-0.66

**The CKM has TWO sources**:
1. **V_cb, V_ub scale** (∝ κ ≈ 0.07): Tower Sigma breaking via cascade fiber VEV
2. **V_us (Cabibbo) scale** (∝ √(m_d/m_s) ≈ 0.22): F-N mass texture

This matches the SM hierarchy: V_us ∝ λ, V_cb ∝ λ² where λ = Cabibbo parameter. The tower breaking gives the λ² scale; the mass texture gives λ.

**NB164 results**: At t_hop = √κ = P₄^{-1/4} (geometric mean of cascade and kinetic):
- V_cb = 0.040 (PDG: 0.041, 3% off) — from tower gen0↔gen2 coupling
- V_us = 0.224 from F-N (PDG: 0.225, 2.1σ) — from cascade mass ratio
- V_ub = 0.016 (PDG: 0.004, 4× off) — OPEN

The tower coupling √κ is the geometric mean of the cascade damping rate (κ) and the kinetic unit (1). V_cb emerges naturally. V_us requires F-N. V_ub is the remaining open element.

**3-level tower (C₆+C₄₂+C₂₁₀, N=258)**: V_ub drops to 0.003 (PDG: 0.004), but V_cb drops to 0.0001 (destroyed). The truncation level matters — 2-level gets V_cb right, 3-level gets V_ub closer, but not both simultaneously.

**Honest wall**: The full CKM requires the profinite tower limit (all covering levels), not a fixed truncation. Each level adds sites that dilute generation-specific effects differently. The correct CKM elements emerge from the balance of all levels. This is a well-defined computation but exceeds current session capacity.

**Would resolve**: Full CKM from profinite tower limit + F-N texture.

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

### GAP-20: Quark Mass Exponent x_q [MECHANISM UNDERSTOOD — NB170–171, NB181]

**What we have**: x_q = 100/63 = p₁²p₃²/(p₂²p₄) CONFIRMED (NB170, #279). Cascade-measured value 1.58664640 matches 100/63 = 1.58730159 to 413 ppm. Applied to PDG: m_s/m_d = C₀^{100/63} = 20.025 vs 20.0 ± 2.69 (0.01σ). T-independence: 0.0 ppm spread across T=211–2000 (#280).

**Factored decomposition** (#281): x_q = (4/7) × (25/9) = x(R₀) × (p₃/p₂)².
- x(R₀) = 4/7 = p₁²/p₄: DERIVED (NB161, +37 ppm)
- Cross-level factor (p₃/p₂)² = 25/9: MECHANISM IDENTIFIED (NB171, 0.018% analytical match)

**R₃ anomaly** (NB170): The outermost cascade level has non-vanishing far-field driven oscillation at frequency ω/P₃ = 2π/30, unlike R₀–R₂ which decay to ~0. Linearized model predicts far-field RMS within 7% of measured value.

**Cross-level mechanism** (NB171): Decomposition into transient (wrapping) and steady-state components:
- **Transient R₀ at ci=11**: Trans(R₀) ≈ π√2 · e^{−κ·11} (binary branch wrapping), verified 0.2%
- **Transient R₃ at ci=191**: Trans(R₃) ≈ π/√3 (quasi-uniform wrapping across 210 branches), verified 1.8%
- **SS amplification**: NB171 claimed SS₃/SS₀ ≈ p₃² = 25. **NB181 CORRECTION**: raw RMS ratio SS₃/SS₀ ≈ 29 ≈ P₃ = 30 (from frequency gradient, see below). The p₃² in NB171's formula refers to a quantity within the cross-level decomposition, not the raw SS₃/SS₀ ratio.
- **R₀ exact solution**: R₀(n) = (2πj₀ + α)·e^{−κn} − α, where α = εω/(ω²+κ²) ≈ 0.01098
- **β = 1/α = 2π√P₄ ≈ 91.1** (the primorial VEV ratio appears naturally)
- **Analytical formula**: cross-level = (ln β + A)/(ln β + B) where A = ln(π√2 · e^{−κ·11}), B = ln(π/(√3·p₃²))
- **Result**: analytical = 2.7773 vs 25/9 = 2.7778 (0.018% — individual ~2% errors absorbed by log structure)

**SS amplification mechanism** (NB181): The cascade SS amplification is driven by the **frequency gradient**:
- Each level k oscillates at dominant frequency ω/P_k (confirmed by FFT)
- The 1st-order transfer function gain ∝ 1/ω_k gives per-level amplification ≈ p_{k+1}
- Total SS₃/SS₀ ≈ P₃ = p₁·p₂·p₃ = 30 (measured: 29.0, deviation 3.3%)
- Cascade Jacobian at R=0: lower-triangular, all eigenvalues = −κ (stable, forced response)
- Off-diagonal coupling: J[k+1,k] ∝ 2/p_{k+1} (decreasing with primes, compensated by frequency gain)
- System is STABLE — SS amplitudes arise from forced response to base oscillation, not instability

**What remains**: The cross-level factor 25/9 in NB171's analytical formula uses a B term with p₃² in the denominator. This p₃² is NOT the raw SS ratio (≈ P₃) but a quantity within the specific coprime-crossing transient/SS decomposition. Understanding how P₃ enters the formula as p₃² in the B term requires re-examining the decomposition at ci=191. The transient components (π√2, π/√3) also need exact proofs.

**Would resolve**: Promoting all 4 quark mass ratios from "cascade-measured" to "analytically derived."

### GAP-21: Top Mass Anchor Formula [STRUCTURAL]

**What we have**: m_t/M_Z = p₂²/√(πp₄) × (1 − H₃²/p₄) (NB118, solenoid_mass.py L279).

Decomposition: y_t = 1/√P₁ = √(cos²θ_W × α₂). This is numerically clean — it uses only derived quantities (sin²θ_W, α₂). But the cancellation pattern was FOUND by searching, not predicted.

Also: H₃² ≡ harmonic oscillation amplitude of the cascade at level 3. The coupling H₃²/p₄ was found to improve the top mass match but has no mechanism.

**What's missing**: WHY does the top Yukawa equal √(cos²θ_W × α₂)? Is this a one-loop relation? And WHY does H₃² couple as H₃²/p₄?

**Would resolve**: Top mass from gauge structure without pattern matching.

### GAP-22: Tau Mass Factor p₃/p₄ [STRUCTURAL]

**What we have**: m_τ = m_μ × R_lep₂^{x_l_inter} × p₃/p₄ (solenoid_mass.py L331). The factor 5/7 was found empirically — it makes the tau prediction work (from ~7σ off to 2.4σ).

**What's missing**: WHY does the tau acquire a factor of p₃/p₄ = 5/7 that the muon doesn't? Is this a higher-order wrapping effect at the third generation? Or does it reflect the charge sector (p₃ = charge prime) interacting with the generation sector (p₄ = generation prime)?

**Would resolve**: m_τ prediction from mechanism rather than empirical correction.

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

### GAP-19: Gravity Hierarchy Exponents [RESOLVED — NB180]

**What we have**: M_Pl/M_Z = 240⁴ × 7⁹ = Tr(L)^{ω(P₄)} × p₄^{σ₃(p₁)} (#261, NB121). Dev: 0.003%.

**Derived part**: Tr(L) = 240 (Cayley Laplacian trace, spectral theorem). ω(P₄) = 4 (prime count). σ₃(p₁) = 9 (sum of cubes of divisors of 2). Multiple independent derivation chains converge on 240.

**NB177–178 geometric identification**:
- Tr(L) = 240 = r₃ + r₄ = P₃ + P₄ = 30 + 210 — the sum of the two outermost primorial radii (#311). This is UNIQUE to {2,3,5,7}: requires p₄+1 = φ(P₃), which fails for all other 4-prime sets tested.
- σ₃(p₁) = 9 = K₁/K₂ — the curvature ratio between chirality and charge spheres (#313).
- M_Pl/M_Z can be written entirely in curvature language: (K₁/K₂)^{σ₃(p₁)} × Tr(L)⁴ where all factors are Gaussian curvatures K_k = 1/P_k² (#313).
- The concentric sphere geometry (NB177) shows the curvature gradient from K₀=1 (innermost) to K₄=1/44100 (outermost) is the gravitational hierarchy.
- Consecutive quartet p₃, P₂, p₄, φ(P₃) = 5, 6, 7, 8 — four consecutive integers, unique to {2,3,5,7} (#312). This interlocking constrains the gauge-gravity bridge.

**NB179 spectral bridge** (major upgrade):
- Natural per-factor Cayley graph on Z*₂₁₀ with |S| = p₃ = 5 generators (#314).
- Integer eigenvalues 0..10 with palindromic multiplicities; bipartite Cayley graph (#315).
- Exact spectral determinant: det'(L) = 2²⁵ × 3¹⁶ × 5¹³ × 7⁸ (#316).
- **Spectral bridge formula** (#317, HEADLINE): H = det'(L) · p₄ / (Λ_max^{σ₃(p₁)} · p₂^{λ(P₄)}) — EXACT algebraic identity. Every component is a framework invariant.
- Canonical factorization: H = p₁^{λ(P₄)} × P₄^{ω(P₄)} × p₄^{p₃} = 2¹² × 210⁴ × 7⁵ (#318).
- Supporting: σ₃(p₁) = ω(P₄) + p₃ → 9 = 4 + 5 (#319); λ(P₄) + ω(P₄) = p₁^{ω(P₄)} → 16 = 16 (#320).

**NB180 p-adic derivation** (RESOLVED):
- All four p-adic valuations of det'(L) are determined by v₂ = p₃² = |S|² = 25 (#321).
- Pairwise valuation differences are all framework invariants: v₂−v₃ = σ₃(p₁) = 9, v₂−v₅ = λ(P₄) = 12, v₅−v₇ = p₃ = 5, v₃−v₇ = φ(P₃) = 8 (#322).
- The bridge exponents are **forced by p-adic consistency**: since Λ_max = p₁·p₃ = 10 contains both primes 2 and 5, the exponent a must satisfy BOTH v₂ and v₅ constraints, which forces a = σ₃(p₁). The v₃ constraint independently forces b = λ(P₄) (#323).
- Fundamental identity: p₃² = σ₃(p₁) + p₁^{ω(P₄)} = 25 = 9 + 16 (#324). Connects |S|² to bilateral arithmetic and group exponent tower.
- Complete valuation formula: det'(L) = ∏_p p^{p₃²−δ_p} with δ₂=0, δ₃=σ₃(p₁), δ₅=λ(P₄), δ₇=λ(P₄)+p₃ (#325).

**Full causal chain**: {2,3,5,7} → Z*₂₁₀ → CRT generators (|S|=p₃) → integer eigenvalues 0..2p₃ → p-adic valuations v_p = p₃²−δ_p → bridge exponents forced by consistency → H = 240⁴ × 7⁹ = M_Pl/M_Z.

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

1. **GAP-20 (x_q cross-level factor)** — Mechanism UNDERSTOOD (NB171 + NB181): cross-level = (ln β + A)/(ln β + B) reproduces 25/9 to 0.018%. **NB181 CORRECTION**: raw SS₃/SS₀ ≈ P₃ = 30 from frequency gradient (confirmed by FFT + Jacobian analysis), NOT p₃² = 25 as claimed. The p₃² enters the formula through the specific coprime-crossing decomposition, not the raw SS ratio. What remains: re-examining how P₃ appears as p₃² in the B term of NB171's formula. **HIGHEST REMAINING LEVERAGE.**

2. **GAP-21 (Top mass anchor)** — y_t = 1/√P₁ = √(cos²θ_W × α₂) may be a one-loop identity connecting the gauge sector to the Yukawa sector. If derived, the entire top mass becomes mechanism-free.

3. **GAP-15 (Bottom Yukawa / m_t/m_b)** — NARROWED (NB182). 42 = charge-neutral sub-covering degree. m_t/m_b = 42×√(29/30) at 0.40σ. Formula structural, mechanism (√(1−α₂) from D₄ irreps) interpretive. Gap remains in gauge sector.

4. **GAP-14 (CKM Wolfenstein A, ρ̄, η̄)** — V_us is derived. The remaining 3 Wolfenstein parameters are structural. The profinite tower limit is the theoretically correct approach but computationally demanding.

5. **GAP-11 (Gauge ρ-corrections)** — The tree-level couplings are derived. Understanding the ρ-corrections would complete the gauge sector.

6. **GAP-13 (Higgs mass)** — At 0.08σ, this is the most precise match. If the formula (48+ρ)/35 has a mechanism, it would connect the Higgs to the eigenstate count.

7. **GAP-22 (Tau p₃/p₄ factor)** — May resolve automatically if x_q derivation reveals the wrapping geometry for all fermions.

8. **GAP-18 (Cosmology)** — The Totient Density Tower suggests a unified mechanism. Lower priority since cosmological predictions already work.

9. **GAP-19 (Gravity exponents)** — 5/6 derived. The remaining 1/6 is the last piece.

6. **GAP-15, GAP-16 (PMNS + ν mass²)** — These may follow from the dissipation matrix, which already gives sin²θ₁₃.

7. **GAP-12 (Running ratio)** — May be the hardest; encodes all-loop QED in a single ratio.

8. **GAP-17 (ν boost)** — Partially derived; needs the full seesaw mechanism (GAP-04).

---

*Created: 2026-03-16 (post-NB129)*
*Updated: 2026-03-17 (post-NB162). Complete audit of derived vs pattern-matched. 9 new gaps (GAP-11 through GAP-19) cataloging all pattern-matched formulas.*

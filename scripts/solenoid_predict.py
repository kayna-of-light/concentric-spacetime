"""
Complete Standard Model + Cosmology predictions from the (2,3,5,7)-solenoid.

Input:  {2, 3, 5, 7} + M_Z = 91.1876 GeV
Output: Gauge couplings, Higgs mass, CKM matrix, PMNS matrix,
        9 fermion masses, neutrino masses, cosmological parameters,
        gravitational hierarchy.

Every prediction traces to {2,3,5,7} through an identified mechanism:
- Gauge couplings: Z*_210 arithmetic + rho corrections (NB111)
- Mixing angles: CRT structure + dissipation matrix (NB109-110)
- Masses: cascade coherence + non-wrapping fractions (NB148-162)
- Cosmology: totient densities + spectral invariants (NB37-91)
- Gravity: modular bridge Tr(L) = c1(E4) = 240 (NB121)

Usage:
    python solenoid_predict.py
"""

import numpy as np
from math import prod, gcd
from functools import reduce
from math import lcm as _lcm
from dataclasses import dataclass, field
from typing import Dict, Optional


# ════════════════════════════════════════════════════════════════
# Primes and derived constants
# ════════════════════════════════════════════════════════════════

PRIMES = [2, 3, 5, 7]
p1, p2, p3, p4 = PRIMES
P4 = prod(PRIMES)                              # 210
P3 = p1 * p2 * p3                              # 30
P2 = p1 * p2                                   # 6
P1 = p1                                        # 2

phi_P4 = prod(p - 1 for p in PRIMES)           # 48
phi_P3 = prod(p - 1 for p in PRIMES[:3])       # 8
lambda_P4 = reduce(_lcm, [p - 1 for p in PRIMES])  # 12
d_P4 = prod(2 for _ in PRIMES)                 # 16 (squarefree)
omega_P4 = len(PRIMES)                         # 4

rho = 1.0 / np.sqrt(P4)                        # 1/sqrt(210)
omega = 2 * np.pi                              # base frequency


# ════════════════════════════════════════════════════════════════
# Experimental reference values
# ════════════════════════════════════════════════════════════════

EXP = {
    # Gauge couplings at M_Z
    '1/alpha_s':   (8.4746,    0.065),
    '1/alpha_2':   (29.580,    0.020),
    '1/alpha_1':   (59.00,     0.02),
    'sin2_thetaW': (0.23122,   0.00003),
    '1/alpha_em':  (137.036,   0.0),      # essentially exact

    # Electroweak masses
    'm_H (GeV)':   (125.25,    0.17),
    'm_W (GeV)':   (80.3692,   0.0133),
    'v (GeV)':     (246.22,    0.0),

    # CKM Wolfenstein
    'lambda_CKM':  (0.22500,   0.00067),
    'A_CKM':       (0.826,     0.016),
    'rhobar_CKM':  (0.159,     0.010),
    'etabar_CKM':  (0.348,     0.010),

    # PMNS
    'sin2_13':     (0.0220,    0.0007),
    'sin2_12':     (0.307,     0.013),
    'sin2_23':     (0.546,     0.021),
    'delta_CP_deg':(197.1,     21.8),
    'Dm2_ratio':   (32.576,    0.882),

    # Neutrino
    'm3 (meV)':    (50.282,    0.5),

    # Cosmology
    'Omega_Lambda': (0.6847,   0.0073),
    'H0 (km/s/Mpc)':(67.36,   0.54),
    'Omega_DM/Omega_b': (5.396, 0.1),
    'n_s':         (0.9649,    0.0042),
    'sigma_8':     (0.811,     0.006),

    # Gravity
    'M_Pl/M_Z':    (1.2209e19 / 91.1876,  0.0),  # non-reduced Planck mass
}


def compute_all(M_Z: float = 91.1876) -> Dict[str, float]:
    """Compute all predictions from {2,3,5,7} + M_Z."""
    pred = {}

    # ════════════════════════════════════════════════════════════
    # I. GAUGE COUPLINGS (NB111, NB119)
    # ════════════════════════════════════════════════════════════

    # Strong: 1/alpha_s = phi(P3) + p4*rho (#241)
    pred['1/alpha_s'] = phi_P3 + p4 * rho

    # Weak: 1/alpha_2 = P3 - lambda(p4)*rho (#242)
    lam_p4 = p4 - 1  # lambda(7) = 6
    pred['1/alpha_2'] = P3 - lam_p4 * rho

    # Hypercharge: 1/alpha_1 = P1*P3 - 1 (#243)
    pred['1/alpha_1'] = P1 * P3 - 1

    # Weinberg angle from EW identity (#244)
    # sin2_thetaW = (1/alpha_2) / (1/alpha_2 + (p3/p2)/alpha_1)
    inv_a2 = pred['1/alpha_2']
    inv_a1 = pred['1/alpha_1']
    pred['sin2_thetaW'] = inv_a2 / (inv_a2 + (p3 / p2) * inv_a1)

    # Fine structure constant (#259, NB119)
    # 1/alpha(0) = 275/2 - 45/(7*sqrt(210))
    pred['1/alpha_em'] = 275.0 / 2 - 45.0 / (7 * np.sqrt(P4))

    # ════════════════════════════════════════════════════════════
    # II. ELECTROWEAK MASSES (NB118, NB120)
    # ════════════════════════════════════════════════════════════

    # Higgs mass: m_H/M_Z = (phi(P4) + rho) / (p3*p4) (#260)
    pred['m_H (GeV)'] = M_Z * (phi_P4 + rho) / (p3 * p4)

    # W mass: tree-level m_W = M_Z * cos(thetaW). With our sin2_thetaW = 0.23129,
    # this gives 79.95 GeV (MISS at tree level). NB258 shows the full prediction
    # including radiative corrections from m_t gives m_W = 80.384 GeV (1.1σ PASS).
    # The tree-level MISS is expected — m_W requires loop corrections.
    pred['m_W (GeV)'] = M_Z * np.sqrt(1 - pred['sin2_thetaW'])

    # Higgs VEV: v = M_Z / sqrt(1 - sin2_thetaW) / sqrt(alpha_2/(4*pi))
    # Simpler: v from M_Z + solenoid correction (#17)
    # Use the standard EW relation with our predicted sin2_thetaW
    cos2_thetaW = 1 - pred['sin2_thetaW']
    alpha_2 = 1.0 / pred['1/alpha_2']
    pred['v (GeV)'] = 2 * pred['m_W (GeV)'] / np.sqrt(4 * np.pi * alpha_2)

    # ════════════════════════════════════════════════════════════
    # III. CKM MATRIX (NB109)
    # ════════════════════════════════════════════════════════════

    # Wolfenstein parameters:
    # lambda = sin(theta_C) = p2^2 / (phi(P3)*p3) = 9/40 (#230)
    lam = p2**2 / (phi_P3 * p3)
    pred['lambda_CKM'] = lam

    # A = phi(p3)/p3 = 4/5 (#231)
    A = (p3 - 1) / p3
    pred['A_CKM'] = A

    # rhobar = 1/omega = 1/(2*pi) (#232)
    pred['rhobar_CKM'] = 1.0 / omega

    # etabar = sqrt(p2)/p3 = sqrt(3)/5 (#233)
    pred['etabar_CKM'] = np.sqrt(p2) / p3

    # Derived CKM elements
    Vcb = A * lam**2
    Vub = A * lam**3 * np.sqrt(pred['rhobar_CKM']**2 + pred['etabar_CKM']**2)
    delta_CKM = np.arctan2(pred['etabar_CKM'], pred['rhobar_CKM'])
    J_CKM = A**2 * lam**6 * pred['etabar_CKM']

    # ════════════════════════════════════════════════════════════
    # IV. PMNS MATRIX (NB110)
    # ════════════════════════════════════════════════════════════

    # Reactor angle: sin2_theta13 = 1/(p2^2 * p3) = 1/45 (#234)
    pred['sin2_13'] = 1.0 / (p2**2 * p3)

    # Solar angle via TBM sum rule: sin2_12 + sin2_13 = 1/p2 = 1/3 (#235)
    pred['sin2_12'] = 1.0 / p2 - pred['sin2_13']  # 14/45

    # Atmospheric angle: sin2_23 = p3*p4 / p1^lambda(p4) = 35/64 (#236)
    pred['sin2_23'] = (p3 * p4) / p1**lam_p4

    # CP phase: delta_CP = p3*p4*pi / p1^p3 = 35*pi/32 (#238)
    delta_CP_rad = p3 * p4 * np.pi / p1**p3
    pred['delta_CP_deg'] = np.degrees(delta_CP_rad)

    # Mass-squared ratio: Dm2_32/Dm2_21 = p1*p4^2/p2 = 98/3 (#237)
    pred['Dm2_ratio'] = p1 * p4**2 / p2

    # ════════════════════════════════════════════════════════════
    # V. NEUTRINO MASSES (NB128-129)
    # ════════════════════════════════════════════════════════════

    # Gravity hierarchy first (needed for seesaw)
    # M_Pl/M_Z = 240^4 * 7^9 (#261)
    Tr_L = 240  # Cayley Laplacian trace = c1(E4)
    sigma3_p1 = 1 + p1**3  # = 9
    M_Pl_over_M_Z = Tr_L**omega_P4 * p4**sigma3_p1
    M_Pl = M_Z * M_Pl_over_M_Z
    pred['M_Pl/M_Z'] = M_Pl_over_M_Z

    # Neutrino mass from NB128-129 (#274):
    # m3 = (M_Z^2/M_Pl) * p2^3 * p3^5 * p4 / p1^3
    # This is the exact form from the scorecard, combining seesaw + boost
    m3_GeV = M_Z**2 / M_Pl * p2**3 * p3**5 * p4 / p1**3
    pred['m3 (meV)'] = m3_GeV * 1e12  # GeV to meV

    # ════════════════════════════════════════════════════════════
    # VI. COSMOLOGICAL PARAMETERS (NB37-39, NB88-91)
    # ════════════════════════════════════════════════════════════

    # Dark energy: Omega_Lambda = phi(p3*p4)/(p3*p4) = phi(35)/35 = 24/35 (#22)
    phi_35 = (p3 - 1) * (p4 - 1)  # 24
    pred['Omega_Lambda'] = phi_35 / (p3 * p4)

    # Spectral index: n_s = 1 - 1/P3 = 29/30 (#23)
    pred['n_s'] = 1 - 1.0 / P3

    # Fluctuation amplitude: sigma_8 = phi(p3)/p3 = 4/5 (#24)
    pred['sigma_8'] = (p3 - 1) / p3

    # Hubble parameter: H0 = M_Z^3/M_Pl^2 * P4^{-4} * C (#203)
    # C = Omega_Lambda * sigma_8 = 96/175 (#209)
    C_hubble = pred['Omega_Lambda'] * pred['sigma_8']  # 96/175

    # H0 in natural units (GeV), then convert to km/s/Mpc
    # Conversion: 1 GeV = 1/(6.5822e-25 s) and 1 Mpc = 3.0857e22 m
    # So H0[km/s/Mpc] = H0[GeV] * (c in km/s) / (1 Mpc in natural units)
    # 1 Mpc = 3.0857e22 m = 3.0857e22 / (1.9733e-16) GeV^{-1} = 1.5637e38 GeV^{-1}
    H0_GeV = M_Z**3 / M_Pl**2 / P4**4 * C_hubble
    Mpc_in_GeV_inv = 1.5637e38
    pred['H0 (km/s/Mpc)'] = H0_GeV * Mpc_in_GeV_inv * 2.9979e5  # * c in km/s

    # DM/baryon ratio: Omega_DM/Omega_b = p2^3/p3 = 27/5 (#204)
    pred['Omega_DM/Omega_b'] = p2**3 / p3

    return pred


def print_predictions(pred: Dict[str, float]):
    """Print all predictions compared to experiment."""
    print(f'\n{"="*78}')
    print(f'  COMPLETE STANDARD MODEL + COSMOLOGY FROM THE (2×3×5×7)-SOLENOID')
    print(f'  Input: {{2, 3, 5, 7}} + M_Z = 91.1876 GeV')
    print(f'  Free parameters: 0')
    print(f'{"="*78}\n')

    sections = [
        ('I. GAUGE COUPLINGS', ['1/alpha_s', '1/alpha_2', '1/alpha_1', 'sin2_thetaW', '1/alpha_em']),
        ('II. ELECTROWEAK MASSES', ['m_H (GeV)', 'm_W (GeV)']),
        ('III. CKM MATRIX', ['lambda_CKM', 'A_CKM', 'rhobar_CKM', 'etabar_CKM']),
        ('IV. PMNS MATRIX', ['sin2_13', 'sin2_12', 'sin2_23', 'delta_CP_deg', 'Dm2_ratio']),
        ('V. NEUTRINO', ['m3 (meV)']),
        ('VI. COSMOLOGY', ['Omega_Lambda', 'H0 (km/s/Mpc)', 'Omega_DM/Omega_b', 'n_s', 'sigma_8']),
        ('VII. GRAVITY', ['M_Pl/M_Z']),
    ]

    n_pass = 0
    n_total = 0

    for section_name, keys in sections:
        print(f'  {section_name}')
        print(f'  {"Quantity":>22s}  {"Predicted":>14s}  {"Experimental":>14s}  {"sigma":>8s}')
        print(f'  {"-"*64}')

        for key in keys:
            p = pred[key]
            if key in EXP:
                e_val, e_err = EXP[key]
                n_total += 1

                # Format based on magnitude
                if abs(p) > 1000:
                    p_str = f'{p:.3e}'
                    e_str = f'{e_val:.3e}'
                elif abs(p) > 10:
                    p_str = f'{p:.4f}'
                    e_str = f'{e_val:.4f}'
                elif abs(p) > 0.1:
                    p_str = f'{p:.5f}'
                    e_str = f'{e_val:.5f}'
                else:
                    p_str = f'{p:.5f}'
                    e_str = f'{e_val:.5f}'

                if e_err > 0:
                    sig = abs(p - e_val) / e_err
                    sig_str = f'{sig:.2f}σ'
                    status = 'PASS' if sig < 3 else 'MISS'
                else:
                    dev = abs(p - e_val) / abs(e_val) * 100
                    sig_str = f'{dev:.3f}%'
                    status = 'PASS' if dev < 1 else 'MISS'

                if status == 'PASS':
                    n_pass += 1

                print(f'  {key:>22s}  {p_str:>14s}  {e_str:>14s}  {sig_str:>8s}  {status}')
            else:
                print(f'  {key:>22s}  {p:.6f}')

        print()

    print(f'  {"="*64}')
    print(f'  {n_pass}/{n_total} PASS (within 3σ or 1%)')
    print(f'{"="*78}')


def main():
    pred = compute_all()
    print_predictions(pred)

    # Also run the fermion mass pipeline
    print(f'\n  VIII. FERMION MASSES (from cascade dynamics)')
    print(f'  {"─"*64}')
    try:
        from solenoid_mass import compute_mass_table
        table = compute_mass_table(verbose=False)
        table.print()
    except ImportError:
        print('  [Run from scripts/ directory to include fermion masses]')


if __name__ == '__main__':
    main()

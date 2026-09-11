# Tables and figures quoted in the paper

## Sect. 6.1 - The floor and its behaviour

- Effective reference size n_eff = 789.1; effective margin of error ±3.49 pp
- Single-proportion floor (p = 0.5, n_s = 1,000), Eq. (5): 4.67 pp
- TV floors of the 143 single-response items: 3.4-8.4 points (median 6.3)
- Mean option floors of the 9 multiple-response items: 2.6-4.2 pp
- Tolerance of the actual panel (n_s = 1,000): ε = 33.8%
- n_s for ε = 20% at this barometer: 1793

**Table 1.** Synthetic sample size required to bring the comparison within a tolerance ε of its asymptotic floor, Eq. (7)

| Tolerance ε | n_s / n_r | n_s for n_r = 1,000 |
|---|---|---|
| 50% | 0.8× | 800 |
| 30% | 1.4× | 1,449 |
| 20% | 2.3× | 2,273 |
| 10% | 4.8× | 4,762 |
| 5% | 9.8× | 9,756 |
| 1% | 49.8× | 49,751 |

## Sect. 6.2 - Items compatible with an unbiased generator

- Within floor: 9 of 152 (5.9%); median ratio 6.23 (IQR 4.34-7.68; max 13.43)
- Benjamini-Hochberg (q = 0.05): 143 items flagged; identical to 'beyond floor': True
- Under simple random sampling (DEFF = 1): 7 within floor
- Items carried in the persona profile: 13; within floor 6; median ratio 1.64
- Other items: 139; within floor 3 (2.2%); median ratio 6.48
- Items within the floor: B7 q1 (0.14, profile), B5 q0 (0.22, profile), B7 q2 (0.22, profile), B7 q7 (0.36, profile), B1 q1 (0.44, profile), B5 q24 (0.64, profile), B5 q27 (0.93), B6 q11 (0.98), B3 q5 (0.99)

**Table 2.** Distribution of the items by ratio of observed divergence to floor

| Ratio | Items | Share |
|---|---|---|
| ≤ 1 | 9 | 5.9% |
| 1-2 | 4 | 2.6% |
| 2-5 | 39 | 25.7% |
| 5-10 | 86 | 56.6% |
| > 10 | 14 | 9.2% |

**Table 3.** Items within their sampling floor, by block

| Block | Items | Within floor | Share |
|---|---|---|---|
| B1 Situación económica | 26 | 1 | 3.8% |
| B2 Estado de bienestar y políticas públicas | 24 | 0 | 0.0% |
| B3 Los miedos de la era de la inseguridad | 7 | 1 | 14.3% |
| B4 El impacto social del turismo | 2 | 0 | 0.0% |
| B5 Situación política y calidad de la democracia | 60 | 3 | 5.0% |
| B6 Geopolítica, guerras y Donald Trump | 24 | 1 | 4.2% |
| B7 Perfil y clasificación (validación) | 9 | 3 | 33.3% |
| Total | 152 | 9 | 5.9% |

## Sect. 6.3 - Tightening paradox

**Table 4.** Items compatible with the floor as a function of synthetic sample size (observed divergence held fixed)

| n_s | Floor factor (single proportion) | Items within floor | Share |
|---|---|---|---|
| 250 | 1.52× | 10 | 6.6% |
| 500 | 1.20× | 9 | 5.9% |
| actual (837-1,000) | 1.00× | 9 | 5.9% |
| 2,000 | 0.88× | 6 | 3.9% |
| 10,000 | 0.78× | 6 | 3.9% |
| ∞ | 0.75× | 6 | 3.9% |

Note. Rows other than 'actual' rescale the floor to a common n_s with 10,000 Monte Carlo replications (seed + 1). Setting every item to exactly n_s = 1,000 gives 7 items: B6 q11 has only 837 valid synthetic responses, so its floor falls when n_s is raised to 1,000, and B3 q5 lies on the floor (ratio 0.99 in the main run, 1.00 in the rescaled run).

- Valid synthetic responses per item: 837-1000
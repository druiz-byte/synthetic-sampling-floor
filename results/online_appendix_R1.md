# Online Appendix — Revision R1 (paper 175)

Supplementary material referred to in the revised manuscript as "online appendix". Scripts: `analysis/r1_*.py`.

## A1. Items within the floor under alternative specifications (Table R1)

| Specification | Reference | Synthetic panel | Floor | Within floor | Profile / inferred |
|---|---|---|---|---|---|
| S1. Submitted | Weighted, n_eff = 789 | Unweighted | Independent | 9 (5.9%) | 6 / 3 |
| S2. Simple random sampling | Unweighted, n = 1,000 | Unweighted | Independent | 7 (4.6%) | 6 / 1 |
| S3. Weight-aligned | Weighted | Weighted with paired respondent's weight | Independent | 8 (5.3%) | 6 / 2 |
| S4. Weight-aligned, paired | Weighted | Weighted with paired respondent's weight | Paired (conditional null) | 5 (3.3%) | 5 / 0 |
| S5. Bonferroni (α/152) | Weighted, n_eff = 789 | Unweighted | Independent | 11 not rejected | 6 / 5 |

Fisher's exact test, profile vs inferred items: S1 6/13 vs 3/139, p = 8.2 × 10⁻⁶; S4 5/13 vs 0/139, p = 2.0 × 10⁻⁶.
Implied ρ for the 139 inferred items: median 0.21 (IQR 0.17–0.26); paired/independent floor factor median 0.89.
Weighted vs unweighted reference distributions (single-response items): total-variation distance median 1.7, max 7.7 points. Published toplines reconstruct with mean error 0.10 pp (weighted) vs 0.54 pp (unweighted).

## A2. Items within the floor, by block (submitted specification)

| Block | Items | Within floor | Share |
|---|---|---|---|
| B1 Economic situation | 26 | 1 | 3.8% |
| B2 Welfare and public policy | 24 | 0 | 0.0% |
| B3 Fears | 7 | 1 | 14.3% |
| B4 Social impact of tourism | 2 | 0 | 0.0% |
| B5 Politics and quality of democracy | 60 | 3 | 5.0% |
| B6 Geopolitics, wars, Trump | 24 | 1 | 4.2% |
| B7 Profile and classification | 9 | 3 | 33.3% |
| Total | 152 | 9 | 5.9% |

## A3. Items whose answer is carried in the persona profile (n = 13)

B1 q0 perceived main problems; B1 q1 rating of the regional economic situation; B5 q0 rating of the political situation; B5 q24 preferred territorial arrangement; B5 q44 ideology; B5 q52 nationalist sentiment; B7 q0 educational level; B7 q1 religion; B7 q2 birthplace; B7 q4–q6 regional-language competence (reading, writing, conversation); B7 q7 2024 regional vote.

## A4. The nine items within the floor (Table R3)

| Item | Profile | K | TV (pts) | Floor (pts) | Ratio S1 | Ratio S3 | Ratio S4 | MDE 80% (pts) |
|---|---|---|---|---|---|---|---|---|
| B7 q1 Religion | Yes | 6 | 0.9 | 6.3 | 0.14 | 0.00 | 0.00 | 7.6 |
| B5 q0 Political situation | Yes | 6 | 1.3 | 6.0 | 0.22 | 0.00 | 0.00 | 6.9 |
| B7 q2 Birthplace | Yes | 3 | 0.8 | 3.6 | 0.22 | 0.00 | 0.00 | 4.9 |
| B7 q7 Vote 2024 | Yes | 13 | 3.0 | 8.3 | 0.36 | 0.00 | 0.00 | 7.9 |
| B1 q1 Economic situation | Yes | 6 | 2.6 | 5.9 | 0.44 | 0.32 | 1.03 | 8.4 |
| B5 q24 Territorial preference | Yes | 6 | 4.0 | 6.3 | 0.64 | 0.29 | 0.85 | 6.9 |
| B5 q27 Party: housing | No | 8 | 6.4 | 6.9 | 0.93 | 0.88 | 1.05 | 7.4 |
| B6 q11 Israel ally/enemy | No | 3 | 5.0 | 5.1 | 0.98 | 0.95 | 1.07 | 10.7 |
| B3 q5 Trip cancelled | No | 2 | 4.1 | 4.2 | 0.99 | 1.08 | 1.19 | 5.7 |

MDE 80% = bias, in total-variation points and in the direction of the observed discrepancy, detected with 80% power by the S1 test (simulation, 6,000 replications per step). B3 q5 (binary): difference −4.1 pp, 90% CI [−7.5, −0.7], 95% CI [−8.1, −0.1] (unpooled Wald).

## A5. Expected passes vs synthetic sample size (Table 3 of the manuscript)

Noise-corrected bias: for each item, δ̂ = λ(q̂ − p̂) with λ² = max(0, 1 − s² Σₖ pₖ(1 − pₖ) / ‖q̂ − p̂‖²), s² = 1/n_eff + 1/n_s (actual n_s). Both samples are simulated at each n_s (multinomial for single-response items; independent normal options for multiple-response items), and the probability of passing the floor recomputed at that n_s is summed over items (4,000 replications).

| n_s | Plug-in: all | Plug-in: inferred | Noise-corrected: all | Noise-corrected: inferred |
|---|---|---|---|---|
| 250 | 8.8 | 3.0 | 9.6 | 3.6 |
| 500 | 7.4 | 1.9 | 8.4 | 2.5 |
| 1,000 | 6.5 | 1.2 | 7.8 | 2.1 |
| 2,000 | 5.9 | 0.8 | 7.4 | 1.7 |
| 10,000 | 5.3 | 0.5 | 6.9 | 1.3 |
| ∞ | 5.1 | 0.4 | 6.8 | 1.2 |

## A6. Filtered items

B1 q4 (n = 648, n_eff = 515) and B3 q6 (n = 267, n_eff = 212) were evaluated at 789 in the submitted version. Rescaled floors (factors 1.14 and 1.58) give ratios 4.1 and 6.3; both remain beyond the floor. The distribution of ratios in Table 2 of the manuscript and Fig. 2 use the corrected values (`results/items_v4.json`). Their reference and synthetic bases differ (the synthetic panel answered without the filter), which is a further caveat for these two items.

## A7. Multiplicity

BH 143, Benjamini–Yekutieli 143, Holm 143, Bonferroni 141 rejections of 152. Descriptive correlations: r = 0.68 across 1,172 option shares; r = 0.75 across the means of the 54 items on 0–10 scales.

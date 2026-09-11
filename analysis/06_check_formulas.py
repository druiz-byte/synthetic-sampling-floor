"""Step 6 - Monte Carlo check of the closed-form results of Sect. 3.

(a) Eq. (5): 95% floor of |p_r - p_s| for a single proportion.
(b) Eq. (3): expected total variation between two samples, E[TV] ≈ s/sqrt(2π) Σ sqrt(p_k(1-p_k)).
(c) P4: probability of passing the floor falls with n_s for a biased item and stays at 95% for an unbiased one.
Output: results/formula_checks.md
"""
import json, math
import numpy as np
from savio import ROOT

DE = json.loads((ROOT / "results" / "design_effect.json").read_text())
n_r = int(round(DE["n_eff"])); rng = np.random.default_rng(2026); R = 200_000
L = ["# Monte Carlo checks of Sect. 3\n"]

# (a) single proportion
for p, n_s in ((0.5, 1000), (0.3, 500), (0.1, 2000)):
    a = rng.binomial(n_r, p, R) / n_r; b = rng.binomial(n_s, p, R) / n_s
    mc = np.quantile(np.abs(a - b), 0.95) * 100
    cf = 1.96 * math.sqrt(p * (1 - p) * (1 / n_r + 1 / n_s)) * 100
    L.append(f"- Eq. (5), p = {p}, n_r = {n_r}, n_s = {n_s}: closed form {cf:.2f} pp · Monte Carlo {mc:.2f} pp")

# (b) expected TV
for pk, n_s in (([.4, .3, .2, .1], 1000), ([.2] * 5, 500), ([.5, .3, .1, .05, .03, .02], 2000)):
    pk = np.array(pk); s = math.sqrt(1 / n_r + 1 / n_s)
    cf = s / math.sqrt(2 * math.pi) * np.sqrt(pk * (1 - pk)).sum()
    A = rng.multinomial(n_r, pk, 50_000) / n_r; B = rng.multinomial(n_s, pk, 50_000) / n_s
    mc = 0.5 * np.abs(A - B).sum(1).mean()
    L.append(f"- Eq. (3), k = {len(pk)}, n_s = {n_s}: closed form {100 * cf:.2f} · Monte Carlo {100 * mc:.2f} TV points")

# (c) P4 for a single proportion with bias delta
L.append("\n| n_s | P(pass), unbiased | P(pass), bias 2 pp | P(pass), bias 4 pp |\n|---|---|---|---|")
for n_s in (250, 500, 1000, 2000, 10000):
    fl = 1.96 * math.sqrt(0.25 * (1 / n_r + 1 / n_s))
    cells = []
    for d in (0, 0.02, 0.04):
        a = rng.binomial(n_r, 0.5, R) / n_r; b = rng.binomial(n_s, 0.5 + d, R) / n_s
        cells.append(f"{np.mean(np.abs(b - a) <= fl):.3f}")
    L.append(f"| {n_s:,} | " + " | ".join(cells) + " |")
(ROOT / "results" / "formula_checks.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))

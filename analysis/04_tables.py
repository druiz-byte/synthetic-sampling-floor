"""Step 4 - Tables 1-4 and every number quoted in Sect. 6 of the paper.
Output: results/tables.md
"""
import json, math
import numpy as np
from savio import ROOT

DE = json.loads((ROOT / "results" / "design_effect.json").read_text())
rows = json.loads((ROOT / "results" / "items_deff.json").read_text(encoding="utf-8"))
srs = json.loads((ROOT / "results" / "items_srs.json").read_text(encoding="utf-8"))
r = np.array([x["ratio"] for x in rows])
L = []
P = L.append

# ---- 6.1: single-proportion floor and Table 1 (Eqs. 5 and 7)
Z, n_eff, fpc2 = 1.96, DE["n_eff"], DE["fpc"] ** 2
floor = lambda ns: 100 * Z * math.sqrt(0.25 * (1 / n_eff + 1 / ns))
P("# Tables and figures quoted in the paper\n")
P("## Sect. 6.1 - The floor and its behaviour\n")
P(f"- Effective reference size n_eff = {n_eff:.1f}; effective margin of error ±{DE['moe_effective_pp']:.2f} pp")
P(f"- Single-proportion floor (p = 0.5, n_s = 1,000), Eq. (5): {floor(1000):.2f} pp")
tv = [x["floor_95"] * 100 for x in rows if x["metric"] == "TV"]
dm = [x["floor_95"] for x in rows if x["metric"] != "TV"]
P(f"- TV floors of the {len(tv)} single-response items: {min(tv):.1f}-{max(tv):.1f} points (median {np.median(tv):.1f})")
P(f"- Mean option floors of the {len(dm)} multiple-response items: {min(dm):.1f}-{max(dm):.1f} pp")
eps_now = math.sqrt(1 + n_eff / 1000) - 1
P(f"- Tolerance of the actual panel (n_s = 1,000): ε = {100 * eps_now:.1f}%")
P(f"- n_s for ε = 20% at this barometer: {n_eff / ((1.2) ** 2 - 1):.0f}\n")
P("**Table 1.** Synthetic sample size required to bring the comparison within a tolerance ε of its asymptotic floor, Eq. (7)\n")
P("| Tolerance ε | n_s / n_r | n_s for n_r = 1,000 |\n|---|---|---|")
for e in (0.5, 0.3, 0.2, 0.1, 0.05, 0.01):
    k = 1 / ((1 + e) ** 2 - 1)
    P(f"| {e:.0%} | {k:.1f}× | {1000 * k:,.0f} |")

# ---- 6.2
P("\n## Sect. 6.2 - Items compatible with an unbiased generator\n")
P(f"- Within floor: {int((r <= 1).sum())} of {len(r)} ({(r <= 1).mean():.1%}); median ratio {np.median(r):.2f} "
  f"(IQR {np.percentile(r, 25):.2f}-{np.percentile(r, 75):.2f}; max {r.max():.2f})")
p = np.array([x["p_value"] for x in rows]); m = len(p); o = np.argsort(p)
thr = np.where(p[o] <= 0.05 * np.arange(1, m + 1) / m)[0]
nbh = int(thr.max() + 1) if len(thr) else 0
flag = np.zeros(m, bool); flag[o[:nbh]] = True
P(f"- Benjamini-Hochberg (q = 0.05): {nbh} items flagged; identical to 'beyond floor': {bool((flag == (r > 1)).all())}")
rs = np.array([x["ratio"] for x in srs])
P(f"- Under simple random sampling (DEFF = 1): {int((rs <= 1).sum())} within floor")
prof = np.array([x["in_profile"] for x in rows])
P(f"- Items carried in the persona profile: {prof.sum()}; within floor {int((r[prof] <= 1).sum())}; median ratio {np.median(r[prof]):.2f}")
P(f"- Other items: {(~prof).sum()}; within floor {int((r[~prof] <= 1).sum())} ({(r[~prof] <= 1).mean():.1%}); median ratio {np.median(r[~prof]):.2f}")
P("- Items within the floor: " + ", ".join(f"{x['block']} q{x['item']} ({x['ratio']:.2f}{', profile' if x['in_profile'] else ''})"
                                           for x in sorted(rows, key=lambda x: x["ratio"]) if x["ratio"] <= 1))
P("\n**Table 2.** Distribution of the items by ratio of observed divergence to floor\n")
P("| Ratio | Items | Share |\n|---|---|---|")
for lo, hi, lab in ((0, 1, "≤ 1"), (1, 2, "1-2"), (2, 5, "2-5"), (5, 10, "5-10"), (10, np.inf, "> 10")):
    k = int(((r <= hi) & (r > lo)).sum()) if lo else int((r <= hi).sum())
    P(f"| {lab} | {k} | {k / len(r):.1%} |")
P("\n**Table 3.** Items within their sampling floor, by block\n")
P("| Block | Items | Within floor | Share |\n|---|---|---|---|")
for b in sorted({x["block"] for x in rows}, key=lambda s: int(s[1:])):
    rb = [x for x in rows if x["block"] == b]; k = sum(x["ratio"] <= 1 for x in rb)
    P(f"| {b} {rb[0]['block_name']} | {len(rb)} | {k} | {k / len(rb):.1%} |")
P(f"| Total | {len(rows)} | {int((r <= 1).sum())} | {(r <= 1).mean():.1%} |")

# ---- 6.3
P("\n## Sect. 6.3 - Tightening paradox\n")
P("**Table 4.** Items compatible with the floor as a function of synthetic sample size (observed divergence held fixed)\n")
P("| n_s | Floor factor (single proportion) | Items within floor | Share |\n|---|---|---|---|")
for n in ("250", "500", "actual", "2000", "10000", "None"):
    if n == "actual":
        k = int((r <= 1).sum())
        P(f"| actual (837-1,000) | 1.00× | {k} | {k / len(rows):.1%} |")
        continue
    k = sum(x["p4"][n] <= 1 for x in rows)
    fac = math.sqrt(1 / n_eff + (0 if n == "None" else 1 / int(n))) / math.sqrt(1 / n_eff + 1 / 1000)
    P(f"| {'∞' if n == 'None' else f'{int(n):,}'} | {fac:.2f}× | {k} | {k / len(rows):.1%} |")
k1000 = sum(x["p4"]["1000"] <= 1 for x in rows)
P(f"\nNote. Rows other than 'actual' rescale the floor to a common n_s with 10,000 Monte Carlo replications "
  f"(seed + 1). Setting every item to exactly n_s = 1,000 gives {k1000} items: B6 q11 has only 837 valid "
  f"synthetic responses, so its floor falls when n_s is raised to 1,000, and B3 q5 lies on the floor "
  f"(ratio 0.99 in the main run, 1.00 in the rescaled run).")
ns = [x["n_synthetic"] for x in rows]
P(f"\n- Valid synthetic responses per item: {min(ns)}-{max(ns)}")
(ROOT / "results" / "tables.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))

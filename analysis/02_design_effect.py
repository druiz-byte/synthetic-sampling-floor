"""Step 2 - Design effect of the weighted reference survey (paper, Sect. 5.2).

Kish (1965) design effect of the weights: DEFF = 1 + CV^2(w).
Effective size n_eff = n * FPC^2 / DEFF, with FPC^2 = (N - n) / (N - 1).
Output: results/design_effect.json
"""
import json, math
from savio import read_sav, ROOT

N_UNIVERSE = 2_242_343          # population aged 18+ of the Basque Country (survey technical sheet)
Z = 1.96

df, _ = read_sav()
w = df["ponde"].astype(float)
n = len(w)
cv2 = float(w.var(ddof=0) / w.mean() ** 2)
deff = 1 + cv2
fpc2 = (N_UNIVERSE - n) / (N_UNIVERSE - 1)
n_eff = n * fpc2 / deff
out = dict(
    n=n, universe=N_UNIVERSE, fpc=math.sqrt(fpc2), cv2_weights=cv2, deff=deff,
    deff_used=round(deff, 4),                       # value used by the floor analysis
    n_eff=n * fpc2 / round(deff, 4),
    moe_nominal_pp=100 * Z * math.sqrt(0.25 * fpc2 / n),
    moe_effective_pp=100 * Z * math.sqrt(0.25 * fpc2 * round(deff, 4) / n),
)
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "design_effect.json").write_text(json.dumps(out, indent=1))
print(f"design effect: CV2 = {cv2:.4f} · DEFF = {deff:.4f} · n_eff = {out['n_eff']:.1f} · "
      f"MoE nominal ±{out['moe_nominal_pp']:.2f} pp, effective ±{out['moe_effective_pp']:.2f} pp")

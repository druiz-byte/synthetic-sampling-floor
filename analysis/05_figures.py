"""Step 5 - Figures 1 and 2 of the paper.
Grayscale, vector (PDF/SVG) plus 800-dpi PNG; marker shapes carry meaning.
Outputs: results/figures/fig1_floor_vs_ns.*, results/figures/fig2_items_ratio.*
"""
import json, numpy as np, matplotlib
from savio import ROOT
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, FixedLocator

plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 8, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6, "svg.fonttype": "path",
                     "pdf.fonttype": 42})
W, H = 4.72, 2.6
DE = json.loads((ROOT / "results" / "design_effect.json").read_text())
NEFF, Z, P, OBS = DE["n_eff"], 1.96, 0.5, 4.2   # OBS: illustrative observed divergence (pp)
OUT = ROOT / "results" / "figures"; OUT.mkdir(parents=True, exist_ok=True)
floor = lambda ns: 100 * Z * np.sqrt(P * (1 - P) * (1 / NEFF + 1 / ns))
asym = 100 * Z * np.sqrt(P * (1 - P) / NEFF)
nstar = 1 / ((OBS / (100 * Z)) ** 2 / (P * (1 - P)) - 1 / NEFF)
fmt = FuncFormatter(lambda v, _: f"{v:,.0f}")

def save(fig, name):
    for ext in ("pdf", "svg"):
        fig.savefig(OUT / f"{name}.{ext}", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=800, bbox_inches="tight")

# ---- Fig. 1
fig, ax = plt.subplots(figsize=(W, H))
ns = np.logspace(2, 5, 400)
ax.plot(ns, floor(ns), color="black", lw=1.6, label="Sampling floor, Eq. (5)")
ax.axhline(asym, color="0.35", lw=1.0, ls=(0, (5, 3)), label=f"Reference margin of error ({asym:.1f} pp): P2")
ax.axhline(OBS, color="black", lw=0.9, ls=(0, (1, 1.5)), label=f"Observed divergence of a biased item ({OBS} pp)")
ax.plot([1000], [floor(1000)], "s", color="black", ms=5, zorder=5)
ax.plot([nstar], [OBS], "o", mfc="white", mec="black", ms=5, mew=1, zorder=5)
ax.annotate("this study ($n_s$ = 1,000)", (1000, floor(1000)), xytext=(1450, 7.3),
            arrowprops=dict(arrowstyle="-", color="0.4", lw=0.6))
ax.annotate(f"crossing at $n_s$ ≈ {round(nstar, -1):,.0f}", (nstar, OBS), xytext=(3600, 5.8),
            arrowprops=dict(arrowstyle="-", color="0.4", lw=0.6))
ax.text(160, OBS + 0.3, "item passes", fontsize=7.5)
ax.text(14000, OBS + 0.3, "item fails (P4)", fontsize=7.5)
ax.set_xscale("log"); ax.set_xlim(100, 1e5); ax.set_ylim(0, 11)
ax.xaxis.set_major_locator(FixedLocator([100, 300, 1000, 3000, 10000, 30000, 100000]))
ax.xaxis.set_major_formatter(fmt); ax.xaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
ax.set_xlabel("Synthetic sample size $n_s$ (log scale)"); ax.set_ylabel("Floor (percentage points)")
ax.grid(axis="y", color="0.88", lw=0.5); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="upper right", fontsize=7.5, handlelength=2.6)
save(fig, "fig1_floor_vs_ns"); plt.close(fig)

# ---- Fig. 2
d = json.loads((ROOT / "results" / "items_deff.json").read_text(encoding="utf-8"))
rows = sorted(d, key=lambda r: r["ratio"])
x = np.arange(1, len(rows) + 1); y = np.array([r["ratio"] for r in rows])
prof = np.array([r["in_profile"] for r in rows])
assert prof.sum() == 13 and len(rows) == 152 and (y <= 1).sum() == 9
fig, ax = plt.subplots(figsize=(W, H))
ax.axhline(1, color="black", lw=0.9, ls=(0, (5, 3)), zorder=1)
ax.scatter(x[~prof], y[~prof], s=6, color="black", label=f"Answer not in profile (n = {(~prof).sum()})", zorder=3)
ax.scatter(x[prof], y[prof], s=26, marker="s", facecolor="white", edgecolor="black", lw=0.8,
           label=f"Answer carried in profile (n = {prof.sum()})", zorder=4)
ax.text(152, 1.08, "floor (ratio = 1)", ha="right", va="bottom", fontsize=7.5)
ax.text(16, 0.52, f"{(y <= 1).sum()} items within the floor", fontsize=7.5, va="center")
ax.set_yscale("log"); ax.set_ylim(0.1, 20); ax.set_xlim(0, 154)
ax.yaxis.set_major_locator(FixedLocator([0.1, 0.2, 0.5, 1, 2, 5, 10, 20]))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
ax.set_xlabel("Items ranked by ratio"); ax.set_ylabel("Observed divergence / floor (log scale)")
ax.grid(axis="y", color="0.88", lw=0.5); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="upper left", fontsize=7.5, handletextpad=0.3)
save(fig, "fig2_items_ratio"); plt.close(fig)
print(f"figures: crossing at n_s = {nstar:,.0f}; asymptote {asym:.2f} pp → results/figures/")

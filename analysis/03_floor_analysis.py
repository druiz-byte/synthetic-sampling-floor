"""Step 3 - Sampling floor of every item and classification within / beyond it
(paper, Sects. 5.5-5.6 and 6.2-6.3).

For each of the 152 items:
  * single-response items: total-variation (TV) divergence between the
    reference marginal (`datos_reales`) and the synthetic marginal; the floor is
    the 95th percentile of TV between two independent multinomial samples drawn
    from the reference marginal, the reference at its effective size and the
    synthetic sample at its actual size (Monte Carlo, 20,000 replications);
    two-sample Monte Carlo p-value.
  * multiple-response items: mean absolute deviation across options; each option
    is a binomial proportion and the item floor is the mean of the option
    floors; Bonferroni-adjusted option-level z-test.
The same computation is repeated for n_s in {250, 500, 2000, 10000, inf}
holding the observed divergence fixed (Table 4, P4), and under simple random
sampling (DEFF = 1).
Outputs: results/items.csv, results/items_deff.json, results/items_srs.json
"""
import json, math, os, re, glob
import numpy as np
import pandas as pd
from scipy.stats import norm
from savio import ROOT

RESP = sorted(glob.glob(str(ROOT / "data" / "synthetic" / "responses" / "encuesta_*.json")))
DE = json.loads((ROOT / "results" / "design_effect.json").read_text())
N_R, U, K = DE["n"], DE["universe"], 1.96
FPC2 = (U - N_R) / (U - 1)
REPS = int(os.environ.get("REPS", "20000"))
NS_GRID = [250, 500, 1000, 2000, 10000, None]      # None = infinitely large panel
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# items whose answer the persona carries in its profile (manipulation checks)
PROFILE = {("B1", 0), ("B1", 1), ("B5", 0), ("B5", 24), ("B5", 44), ("B5", 52),
           ("B7", 0), ("B7", 1), ("B7", 2), ("B7", 4), ("B7", 5), ("B7", 6), ("B7", 7)}


def norm_key(s):
    s = re.sub(r"[^a-z0-9áéíóúñü ]", " ", s.lower().strip())
    return re.sub(r"\s+", " ", s).strip()


NSNC = {"ns nc", "no lo sé prefiero no contestar", "no lo se prefiero no contestar",
        "ns nc no sabe no contesta", "no sabe no contesta", "no lo sé",
        "no lo se", "prefiero no contestar", "n s n c"}


def match_real(opciones, datos):
    """Reference percentages aligned with the options of the template item."""
    dn = {norm_key(k): v for k, v in datos.items()}
    out = []
    for o in opciones:
        ko = norm_key(o)
        if ko in dn:
            out.append(dn[ko]); continue
        if ko in NSNC or "no lo s" in ko or "no contestar" in ko:
            hit = next((v for k, v in dn.items() if k in NSNC or "ns nc" in k
                        or "no lo s" in k or "no contestar" in k), None)
            if hit is not None:
                out.append(hit); continue
        cand = [v for k, v in dn.items() if k.startswith(ko[:18]) or ko.startswith(k[:18])]
        if len(cand) == 1:
            out.append(cand[0]); continue
        raise ValueError(f"option not matched: {o}")
    return out


def run(deff):
    n_eff = N_R * FPC2 / deff

    def tv_null(prn, n_s, rng, reps):
        A = rng.multinomial(int(round(n_eff)), prn, size=reps) / round(n_eff)
        if n_s is None:
            return 0.5 * np.abs(A - prn).sum(1)
        B = rng.multinomial(n_s, prn, size=reps) / n_s
        return 0.5 * np.abs(A - B).sum(1)

    rows = []
    for fp in RESP:
        d = json.load(open(fp, encoding="utf-8"))
        bnum, bname = re.search(r"Bloque (\d+): (.+)", d["titulo"]).groups()
        for qi, q in enumerate(d["definition"]):
            ops = q["opciones"]; mult = q.get("multiple", 1)
            real = match_real(ops, q["datos_reales"])
            counts = np.zeros(len(ops)); n_resp = 0
            for r in d["results"]:
                v = r.get("resps", {}).get(str(qi))
                if not v:
                    continue
                idxs = [LETTERS.index(x.strip()) for x in str(v).split(",")
                        if x.strip() in LETTERS and LETTERS.index(x.strip()) < len(ops)]
                if not idxs:
                    continue
                n_resp += 1
                for i in idxs:
                    counts[i] += 1
            pr = np.array(real, float) / 100; ps = counts / n_resp; n_s = n_resp
            seed = qi * 977 + int(bnum)
            if mult and mult > 1:
                gaps = np.abs(pr - ps)

                def flo_for(nsx):
                    inv = 0 if nsx is None else 1 / nsx
                    return float(np.mean(K * np.sqrt(pr * (1 - pr) * (deff * FPC2 / N_R + inv))))
                div = float(np.mean(gaps)) * 100; flo = flo_for(n_s) * 100
                se = np.sqrt(pr * (1 - pr) * (deff * FPC2 / N_R + 1 / n_s))
                z = gaps / np.where(se > 0, se, np.inf)
                pval = float(min(1.0, np.min(2 * (1 - norm.cdf(z))) * len(z)))
                p4 = {str(n): div / (flo_for(n) * 100) for n in NS_GRID}
                metric = "DAM-multi"
            else:
                prn = pr / pr.sum(); psn = ps / ps.sum()
                div = float(0.5 * np.abs(prn - psn).sum())
                sim = tv_null(prn, n_s, np.random.default_rng(seed), REPS)
                flo = float(np.quantile(sim, 0.95))
                pval = float((np.sum(sim >= div) + 1) / (REPS + 1))
                p4 = {}
                for n in NS_GRID:
                    s2 = tv_null(prn, n, np.random.default_rng(seed + 1), 10000)
                    p4[str(n)] = div / float(np.quantile(s2, 0.95))
                metric = "TV"
            rows.append(dict(block=f"B{bnum}", block_name=bname, item=qi, question=q["texto"],
                             n_options=len(ops), metric=metric, n_synthetic=n_s,
                             divergence=div, floor_95=flo, ratio=div / flo, within_floor=div <= flo,
                             p_value=pval, in_profile=(f"B{bnum}", qi) in PROFILE, p4=p4))
    return rows


deff = DE["deff_used"]
res = {}
for tag, dv in (("deff", deff), ("srs", 1.0)):
    rows = run(dv)
    (ROOT / "results" / f"items_{tag}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    res[tag] = rows
    r = np.array([x["ratio"] for x in rows])
    print(f"[{tag}] DEFF={dv} · items={len(rows)} · within floor={int((r <= 1).sum())} · "
          f"median ratio={np.median(r):.2f} · IQR={np.percentile(r, 25):.2f}-{np.percentile(r, 75):.2f} · max={r.max():.2f}")

# flat CSV (unit: divergence in TV fraction for single-response items, pp for multiple-response items)
flat = []
for a, b in zip(res["deff"], res["srs"]):
    row = {k: v for k, v in a.items() if k != "p4"}
    for n, v in a["p4"].items():
        row[f"ratio_ns_{'inf' if n == 'None' else n}"] = v
    row.update(floor_95_srs=b["floor_95"], ratio_srs=b["ratio"], within_floor_srs=b["within_floor"], p_value_srs=b["p_value"])
    flat.append(row)
pd.DataFrame(flat).to_csv(ROOT / "results" / "items.csv", index=False, encoding="utf-8")
print("→ results/items.csv")

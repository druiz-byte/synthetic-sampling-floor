"""Step 7 - Pairing between personas and reference respondents (paper, Sects. 3.5 and 5.3).

Each persona of the synthetic panel was built from the record of one respondent
of the reference survey. This script finds, for every persona, the respondents
that match it exactly on sex, age, province, religion, birthplace and 2024
regional vote, and, for personas with a unique match, checks agreement on the
political variables carried in the profile.
Output: results/pairing_report.md
"""
import json
import numpy as np
from savio import read_sav, ROOT

df, meta = read_sav()
VL = meta.variable_value_labels
P = json.loads((ROOT / "data" / "synthetic" / "personas_v1.json").read_text(encoding="utf-8"))["poblacion"]

def lab(var):
    return df[var].map(lambda v: VL[var].get(v) if v == v else None)

KEYS = {"genero": lab("sexo"), "provincia": lab("prov"), "religion": lab("p41"),
        "nacimiento": lab("p42"), "voto_autonomicas_2024": lab("p45")}
CHECK = {"valoracion_economia_pv": lab("p2"), "valoracion_politica_pv": lab("p18"),
         "preferencia_territorial": lab("p22")}
SCALES = {"ideologia_0_10": "p36", "escala_nacionalismo_0_10": "p38"}
edad = df["edad"].values

n_match = []; uniq = []
for i, a in enumerate(P):
    m = edad == a["edad"]
    for k, ser in KEYS.items():
        m &= (ser.values == a[k])
    idx = np.where(m)[0]
    n_match.append(len(idx))
    if len(idx) == 1:
        uniq.append((a, idx[0]))
n_match = np.array(n_match)
L = ["# Persona-respondent pairing\n",
     f"- Personas: {len(P)}; respondents: {len(df)}",
     f"- Personas with at least one exact match on sex, age, province, religion, birthplace and 2024 vote: {(n_match >= 1).sum()}",
     f"- Personas with a unique match: {len(uniq)}\n",
     "Agreement among uniquely matched personas:\n", "| Profile attribute | Survey variable | Agreement |", "|---|---|---|"]
for k, ser in CHECK.items():
    ok = np.mean([ser.values[j] == a[k] for a, j in uniq])
    L.append(f"| {k} | {dict(zip(CHECK, ['p2', 'p18', 'p22']))[k]} | {ok:.1%} |")
for k, v in SCALES.items():
    pairs = [(a[k], df[v].values[j]) for a, j in uniq if a[k] is not None and df[v].values[j] <= 10]
    ok = np.mean([float(x) == float(y) for x, y in pairs])
    L.append(f"| {k} | {v} (valid answers, n = {len(pairs)}) | {ok:.1%} |")
(ROOT / "results" / "pairing_report.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))

import sys; sys.path.insert(0,'.')
from r1_common import *
P = json.load(open(ROOT/"data/synthetic/personas_v1.json",encoding="utf-8"))["poblacion"]
def lab(var): return df[var].map(lambda v: VVL[var].get(v) if v==v else None).values
K = {"genero":lab("sexo"),"provincia":lab("prov"),"religion":lab("p41"),"nacimiento":lab("p42"),"voto_autonomicas_2024":lab("p45")}
T = {"valoracion_economia_pv":lab("p2"),"valoracion_politica_pv":lab("p18"),"preferencia_territorial":lab("p22"),"habitat":lab("hab"),"lengua_encuesta":lab("lengua")}
edad = df["edad"].values
def num(x):
    try: return float(x)
    except: return np.nan
p36 = df["p36"].values; p38=df["p38"].values
mapping = {}; amb=0; none=0; used=set()
for a in P:
    m = edad==a["edad"]
    for k,s in K.items(): m &= (s==a[k])
    idx = np.where(m)[0]
    if len(idx)>1:
        sc = np.zeros(len(idx))
        for k,s in T.items(): sc += (s[idx]==a.get(k))
        sc += (p36[idx]==num(a.get("ideologia_0_10"))) + (p38[idx]==num(a.get("escala_nacionalismo_0_10")))
        best = idx[sc==sc.max()]
        if len(best)>1: amb+=1
        idx = best
    if len(idx)==0: none+=1; continue
    cand=[i for i in idx if i not in used] or list(idx)
    mapping[a["id"]] = int(cand[0]); used.add(int(cand[0]))
print("mapped",len(mapping),"ambiguous after tiebreak",amb,"none",none,"distinct respondents",len(set(mapping.values())))
json.dump(mapping, open(str(ROOT/"results"/"persona_map.json"),"w"))

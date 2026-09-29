"""Revision R1 - item-specific effective reference size for the two filtered items
(B1 q4, n = 648; B3 q6, n = 267). Rescales their floors (floors are homogeneous of
degree one in s, Eq. 4) and rewrites results/items_v4.json/csv; regenerates Fig. 2."""
import json, numpy as np, pandas as pd
from savio import ROOT
from r1_common import df, W, CW, item_Y
DE=json.loads((ROOT/"results/design_effect.json").read_text()); NEFF=DE["n_eff"]
d=json.loads((ROOT/"results/items_deff.json").read_text(encoding="utf-8"))
for e in CW:
    if e['tipo']=='multi': continue
    y=item_Y(e); o=~np.isnan(y)
    if o.sum()>=950: continue
    w=W[o]; ne=w.sum()**2/(w**2).sum()
    b=f"B{int(e['bloque'].split('_')[2])}"
    r=[x for x in d if x['block']==b and x['item']==e['qi']][0]
    ns=r['n_synthetic']; f=np.sqrt((1/ne+1/ns)/(1/NEFF+1/ns))
    r['floor_95']=float(r['floor_95']*f); r['ratio']=float(r['divergence']/r['floor_95']); r['within_floor']=bool(r['ratio']<=1)
    r['n_eff_reference']=float(ne)
    print(b,e['qi'],'n',int(o.sum()),'n_eff %.0f factor %.2f ratio %.2f'%(ne,f,r['ratio']))
(ROOT/"results/items_v4.json").write_text(json.dumps(d,ensure_ascii=False,indent=1),encoding="utf-8")
r=np.array([x['ratio'] for x in d])
print('within',(r<=1).sum(),'median %.2f IQR %.2f-%.2f max %.2f'%(np.median(r),*np.percentile(r,[25,75]),r.max()))
print('bins',[int(((r>a)&(r<=b)).sum()) for a,b in [(-1,1),(1,2),(2,5),(5,10),(10,1e9)]])
prof=np.array([x['in_profile'] for x in d]); print('median profile %.2f other %.2f'%(np.median(r[prof]),np.median(r[~prof])))

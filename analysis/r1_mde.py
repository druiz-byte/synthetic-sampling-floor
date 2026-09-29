import sys, warnings; sys.path.insert(0,'.'); warnings.filterwarnings("ignore")
from r1_common import *
DE=json.load(open(ROOT/"results/design_effect.json")); neff=int(round(DE['n_eff']))
rng=np.random.default_rng(11); R=6000
NINE=[("B7",1),("B5",0),("B7",2),("B7",7),("B1",1),("B5",24),("B5",27),("B6",11),("B3",5)]
def match_real(ops, datos):
    dn={norm(k):v for k,v in datos.items()}; return np.array([dn[mo(o,dn.keys())] for o in ops],float)/100
for b,qi in NINE:
    d=json.load(open(RESP[int(b[1])-1],encoding='utf-8')); q=d['definition'][qi]; K=len(q['opciones'])
    p=match_real(q['opciones'],q['datos_reales']); p/=p.sum()
    cnt=np.zeros(K); n=0
    for r in d['results']:
        v=r.get('resps',{}).get(str(qi))
        if v and v.strip() in LET and LET.index(v.strip())<K: cnt[LET.index(v.strip())]+=1; n+=1
    qs=cnt/n; tv=0.5*np.abs(qs-p).sum()
    A=rng.multinomial(neff,p,size=R)/neff; B=rng.multinomial(n,p,size=R)/n
    fl=np.quantile(0.5*np.abs(A-B).sum(1),.95)
    u=(qs-p)/max(0.5*np.abs(qs-p).sum(),1e-9)   # direction with TV = 1
    if tv==0: u=np.zeros(K); u[np.argmax(p)]=-1; u[np.argmin(p)]=1
    lo,hi=0,0.3
    for _ in range(25):
        mid=(lo+hi)/2; qt=np.clip(p+mid*u,0,None); qt/=qt.sum()
        A=rng.multinomial(neff,p,size=R)/neff; Bq=rng.multinomial(n,qt,size=R)/n
        pw=np.mean(0.5*np.abs(A-Bq).sum(1)>fl)
        (hi,lo)=(mid,lo) if pw>=0.8 else (hi,mid)
    extra=""
    if K==2:
        se=np.sqrt(p[0]*(1-p[0])/neff+qs[0]*(1-qs[0])/n); dd=qs[0]-p[0]
        extra=" | diff %.1f pp, 90%% CI [%.1f, %.1f], 95%% CI [%.1f, %.1f]"%(dd*100,(dd-1.645*se)*100,(dd+1.645*se)*100,(dd-1.96*se)*100,(dd+1.96*se)*100)
    print(f"{b} q{qi}: K={K} n_s={n} TV={tv*100:.1f} floor={fl*100:.1f} MDE80(TV, observed direction)={hi*100:.1f}{extra}")

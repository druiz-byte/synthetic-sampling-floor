import sys, warnings; sys.path.insert(0,'.'); warnings.filterwarnings("ignore")
from r1_common import *
_c=pd.read_csv(ROOT/"results/items.csv"); it=[dict(block=a,item=b,in_profile=c) for a,b,c in zip(_c.block,_c.item,_c.in_profile)]
DE=json.load(open(ROOT/"results/design_effect.json")); neff=int(round(DE['n_eff']))
rng=np.random.default_rng(7); R=4000; K196=1.96
GRID=[250,500,1000,2000,10000,None]
import re as _re
def match_real(ops, datos):
    dn={norm(k):v for k,v in datos.items()}; out=[]
    for o in ops:
        k=mo(o,dn.keys()); out.append(dn[k])
    return np.array(out,float)/100
res={g:{'plug':np.zeros(len(GRID)),'shr':np.zeros(len(GRID))} for g in ('all','profile','other')}
lam_list=[]
for bnum in range(1,8):
    d=json.load(open(RESP[bnum-1],encoding='utf-8'))
    for qi,q in enumerate(d['definition']):
        row=[x for x in it if x['block']==f"B{bnum}" and x['item']==qi][0]
        ops=q['opciones']; K=len(ops); mult=q.get('multiple',1)
        pr=match_real(ops,q['datos_reales'])
        cnt=np.zeros(K); n=0
        for r in d['results']:
            v=r.get('resps',{}).get(str(qi))
            if not v: continue
            idx=[LET.index(x.strip()) for x in str(v).split(',') if x.strip() in LET and LET.index(x.strip())<K]
            if not idx: continue
            n+=1; cnt[idx]+=1
        ps=cnt/n; grp='profile' if row['in_profile'] else 'other'
        if mult and mult>1:
            dl=ps-pr; v1=pr*(1-pr); s2=1/neff+1/n
            lam=np.sqrt(max(0,1-s2*v1.sum()/max((dl**2).sum(),1e-12)))
            for L,key in ((1,'plug'),(lam,'shr')):
                for gi,g in enumerate(GRID):
                    inv=0 if g is None else 1/g; sd=np.sqrt(v1*(1/neff+inv))
                    Dk=L*dl+sd*rng.standard_normal((R,K))
                    pas=np.mean(np.mean(np.abs(Dk),1)<=np.mean(K196*sd))
                    for gg in ('all',grp): res[gg][key][gi]+=pas
        else:
            p=pr/pr.sum(); qs=ps/ps.sum(); dl=qs-p
            s2=1/neff+1/n; lam=np.sqrt(max(0,1-s2*(p*(1-p)).sum()/max((dl**2).sum(),1e-12)))
            lam_list.append(lam)
            for gi,g in enumerate(GRID):
                A=rng.multinomial(neff,p,size=R)/neff
                B0=p if g is None else rng.multinomial(g,p,size=R)/g
                fl=np.quantile(0.5*np.abs(A-B0).sum(1) if g is not None else 0.5*np.abs(A-p).sum(1),.95)
                for L,key in ((1,'plug'),(lam,'shr')):
                    qt=np.clip(p+L*dl,0,None); qt/=qt.sum()
                    A2=rng.multinomial(neff,p,size=R)/neff
                    B=qt if g is None else rng.multinomial(g,qt,size=R)/g
                    pas=np.mean(0.5*np.abs(A2-B).sum(1)<=fl)
                    for gg in ('all',grp): res[gg][key][gi]+=pas
print("median shrink lambda (single items)", np.median(lam_list), "share lambda=0:", np.mean(np.array(lam_list)==0))
for g in res:
    print(g, 'plug-in', np.round(res[g]['plug'],2), 'shrunk', np.round(res[g]['shr'],2))

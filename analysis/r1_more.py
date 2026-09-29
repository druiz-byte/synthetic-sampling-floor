import sys, warnings; sys.path.insert(0,'.'); warnings.filterwarnings("ignore")
from r1_common import *
from scipy.stats import norm as N01
it = pd.read_csv(ROOT/"results/items.csv")
# ---- A. published toplines vs weighted / unweighted microdata
errs_w=[]; errs_u=[]; tv_wu=[]
for bnum in range(1,8):
    d=json.load(open(RESP[bnum-1],encoding='utf-8'))
    for e,q in zip([x for x in CW if x['bloque'].startswith(f"barometro_digital_{bnum}_")], d['definition']):
        dr={norm(k):v for k,v in q['datos_reales'].items()}
        if e['tipo']=='multi':
            Y=item_Y(e); pu=Y.mean(0)*100; pw=np.average(Y,axis=0,weights=W)*100
        else:
            y=item_Y(e); o=~np.isnan(y); K=len(e['opciones'])
            pu=np.array([(y[o]==k).mean() for k in range(K)])*100
            pw=np.array([W[o&(y==k)].sum() for k in range(K)])/W[o].sum()*100
            tv_wu.append(0.5*np.abs(pu-pw).sum())
        for j,op in enumerate(e['opciones']):
            k=mo(op,dr.keys())
            if k is not None: errs_w.append(abs(pw[j]-dr[k])); errs_u.append(abs(pu[j]-dr[k]))
print("A. mean |published - unweighted| = %.2f pp ; mean |published - weighted| = %.2f pp"%(np.mean(errs_u),np.mean(errs_w)))
print("   TV(weighted, unweighted) single items: median %.2f, max %.2f points"%(np.median(tv_wu),np.max(tv_wu)))
# ---- C. multiplicity
p=it.p_value.values; m=len(p); o=np.argsort(p); ps=p[o]
def bh(ps,c=1):
    k=np.where(ps<=np.arange(1,m+1)/m*0.05/c)[0]; return 0 if len(k)==0 else k.max()+1
cm=np.sum(1/np.arange(1,m+1))
holm=0
for i,x in enumerate(ps):
    if x<=0.05/(m-i): holm+=1
    else: break
print("C. BH %d, BY %d, Holm %d, Bonferroni %d, unadjusted %d of %d"%(bh(ps),bh(ps,cm),holm,(p<=0.05/m).sum(),(p<=0.05).sum(),m))
print("   min p-value resolution", p.min(), " items at min", (p==p.min()).sum())
# block-level: Simes/Bonferroni per block (one test per block, robust to within-block dependence)
for b,g in it.groupby('block'):
    pp=np.sort(g.p_value.values); k=len(pp)
    print("   ",b,k,"block Bonferroni min p*k=%.2g"%(pp[0]*k), "BY within block rejects", bh_ := int(max([i+1 for i in range(k) if pp[i]<=(i+1)/k*0.05/np.sum(1/np.arange(1,k+1))]+[0])))

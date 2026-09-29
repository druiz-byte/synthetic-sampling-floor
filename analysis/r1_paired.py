import sys, warnings; sys.path.insert(0,'.'); warnings.filterwarnings("ignore")
from r1_common import *
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
MAP = {int(k):v for k,v in json.load(open(str(ROOT/"results"/"persona_map.json"))).items()}
PROFILE = {("B1",0),("B1",1),("B5",0),("B5",24),("B5",44),("B5",52),("B7",0),("B7",1),("B7",2),("B7",4),("B7",5),("B7",6),("B7",7)}
# profile covariates taken from the respondent record (what the persona carries)
cat_vars = ["sexo","edad_r","prov","hab","p42","edu","cs8","cs","lengua","p44_1","p44_2","p44_3","p41","p22","p45","p2","p18"]
Xparts=[pd.get_dummies(df[v].fillna(-1).astype(int).astype(str), prefix=v) for v in cat_vars]
for v in ["p36","p38"]:
    x=df[v].where(df[v]<=10); Xparts.append(pd.DataFrame({v:x.fillna(5)/10, v+"_na":x.isna().astype(float), v+"_sq":(x.fillna(5)/10)**2}))
Xparts.append(df[[f"p1_{i}" for i in range(1,25)]].fillna(0).clip(0,1))
X = pd.concat(Xparts,axis=1).astype(float).values
N=len(df); R=2000; rng=np.random.default_rng(2026)

def crossfit(y, K):
    """out-of-fold P(Y=k|X) for all respondents; trained on respondents with observed y"""
    obs = ~np.isnan(y); pi = np.zeros((N,K)); cnt=np.zeros(N)
    kf = KFold(5, shuffle=True, random_state=1)
    for tr, te in kf.split(X):
        t = tr[obs[tr]]
        cls = np.unique(y[t]).astype(int)
        if len(cls)==1: pi[te, cls[0]] += 1; cnt[te]+=1; continue
        m = LogisticRegression(C=1.0, max_iter=2000).fit(X[t], y[t].astype(int))
        pi[np.ix_(te, cls)] += m.predict_proba(X[te]); cnt[te]+=1
    pi /= cnt[:,None]
    pi = 0.999*pi + 0.001/K           # tiny smoothing for classes unseen in a fold
    return pi/pi.sum(1,keepdims=True)

def draw(pi, reps):
    cs = np.cumsum(pi,1); u = rng.random((reps, pi.shape[0],1))
    return (u > cs[None,:,:]).sum(2).clip(max=pi.shape[1]-1)

def wdist(idx, w, K):   # idx: reps x n
    out = np.zeros((idx.shape[0],K))
    for k in range(K): out[:,k] = ((idx==k)*w).sum(1)
    return out/w.sum()

rows=[]
for bnum in range(1,8):
    items=[e for e in CW if e['bloque'].startswith(f"barometro_digital_{bnum}_")]
    for e in items:
        qi=e['qi']; ops=e['opciones']; K=len(ops); blk=f"B{bnum}"
        d, syn = synth(bnum, qi, K)
        pid = [r['id'] for r in d['results']]
        S = [(MAP[p], s) for p,s in zip(pid, syn) if s is not None]
        js = np.array([j for j,_ in S]); ws = W[js]
        if e['tipo']=='multi':
            Y = item_Y(e); ref = np.average(Y, axis=0, weights=W)
            Q = np.zeros((len(S),K))
            for i,(_,s) in enumerate(S): Q[i, s]=1
            qw = np.average(Q,axis=0,weights=ws)
            div = np.mean(np.abs(ref-qw))
            fl_p=[]; fl_i=[]
            for k in range(K):
                y=Y[:,k]
                if y.sum()<5: pik=np.full((N,2),[1-y.mean(),y.mean()])
                else: pik=crossfit(y,2)
                A = wdist(draw(pik,R),W,2)[:,1]; B = wdist(draw(pik[js],R),ws,2)[:,1]
                fl_p.append(np.quantile(np.abs(A-B),.95))
                pm = np.average(pik[:,1],weights=W)
                B0 = wdist(draw(np.tile([1-pm,pm],(len(js),1)),R),ws,2)[:,1]
                fl_i.append(np.quantile(np.abs(A-B0),.95))
            flp=float(np.mean(fl_p)); fli=float(np.mean(fl_i))
        else:
            y = item_Y(e); obs=~np.isnan(y)
            ref = np.array([W[obs&(y==k)].sum() for k in range(K)])/W[obs].sum()
            q = np.zeros(K)
            for (j,s) in S: q[s[0]] += W[j]
            q/=q.sum(); div = 0.5*np.abs(ref-q).sum()
            pi = crossfit(y,K)
            Ro = np.where(obs)[0]
            A = wdist(draw(pi[Ro],R), W[Ro], K); B = wdist(draw(pi[js],R), ws, K)
            flp = float(np.quantile(0.5*np.abs(A-B).sum(1),.95))
            pm = ref
            B0 = wdist(draw(np.tile(pm,(len(js),1)),R), ws, K)
            A0 = wdist(draw(np.tile(pm,(len(Ro),1)),R), W[Ro], K)
            fli = float(np.quantile(0.5*np.abs(A0-B0).sum(1),.95))
        rows.append(dict(block=blk,item=qi,tipo=e['tipo'],K=K,n_syn=len(S),div_w=div,floor_paired=flp,floor_indep=fli,
                         ratio_paired=div/flp, ratio_indep=div/fli, in_profile=(blk,qi) in PROFILE))
        print(blk,qi,e['tipo'],round(div,3),round(fli,3),round(flp,3),flush=True)
pd.DataFrame(rows).to_csv(str(ROOT/"results"/"r1_paired.csv"),index=False)

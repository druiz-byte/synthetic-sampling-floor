import json, re, glob, unicodedata
import numpy as np, pandas as pd
from savio import read_sav, ROOT
df, meta = read_sav()
VVL = meta.variable_value_labels
CW = json.load(open(ROOT/"data/instrument/crosswalk.json", encoding="utf-8"))
RESP = sorted(glob.glob(str(ROOT/"data/synthetic/responses/encuesta_*.json")))
LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
W = df["ponde"].values if "ponde" in df else None

def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9ñ ]', ' ', s)).strip()

def is_ns(n): return n.startswith('no lo se') or n in ('ns nc','ns','nsnc') or 'no contestar' in n or 'no sabe' in n

def mo(op, keys):
    n = norm(op)
    if n in keys: return n
    if is_ns(n):
        for k in keys:
            if is_ns(k): return k
    for k in keys:
        if k and (k in n or n in k): return k
    return None

def item_Y(e):
    """respondent-level option index (single) or indicator matrix (multi); NaN = not asked/missing"""
    ops = e['opciones']
    if e['tipo']=='multi':
        M = np.column_stack([(df[v]==c).astype(float).values if v else np.zeros(len(df)) for v,c in zip(e['vars'],e['codigos'])])
        return M
    v = e['var']; lab = VVL.get(v, {}); keys = {norm(l):code for code,l in lab.items()}
    code2opt = {}
    for j,o in enumerate(ops):
        k = mo(o, keys.keys())
        if k is not None: code2opt[keys[k]] = j
    y = df[v].map(lambda c: code2opt.get(c, np.nan) if c==c else np.nan).values
    return y

def synth(bnum, qi, nops):
    d = json.load(open(RESP[bnum-1], encoding='utf-8'))
    out = []
    for r in d['results']:
        v = r.get('resps',{}).get(str(qi))
        if not v: out.append(None); continue
        idx = [LET.index(x.strip()) for x in str(v).split(',') if x.strip() in LET and LET.index(x.strip())<nops]
        out.append(idx if idx else None)
    return d, out

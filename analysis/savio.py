"""Read the SPSS reference file.

Uses pyreadstat when it is installed. Otherwise falls back to a small
pure-Python reader (numeric variables, variable labels and value labels only),
which is all this replication package needs. Both paths return
(DataFrame, meta) where meta has `column_names_to_labels` and
`variable_value_labels`, mirroring pyreadstat.
"""
from pathlib import Path
from types import SimpleNamespace
import struct

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SAV = ROOT / "data" / "reference" / "reference_survey_summer2026.sav"


def _fix(s):
    # the file stores UTF-8 text; decode bytes read as latin-1 back to UTF-8
    try:
        return s.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def _read_pure(path):
    b = Path(path).read_bytes()
    p = 0

    def rd(fmt):
        nonlocal p
        v = struct.unpack_from(fmt, b, p)
        p += struct.calcsize(fmt)
        return v

    if b[:4] not in (b"$FL2", b"$FL3"):
        raise ValueError("not an SPSS .sav file")
    e = "<" if struct.unpack_from("<i", b, 64)[0] in (2, 3) else ">"
    p = 64
    _layout, _ncs, comp, _wix, ncases = rd(e + "5i")
    bias, = rd(e + "d")
    p += 9 + 8 + 64 + 3
    vars_, vlabels, longnames = [], {}, {}
    while True:
        rt, = rd(e + "i")
        if rt == 2:
            typ, hasl, nmis, _pr, _wr = rd(e + "5i")
            name = b[p:p + 8].decode("latin1").strip()
            p += 8
            lab = None
            if hasl:
                ln, = rd(e + "i")
                lab = b[p:p + ln].decode("latin1", "replace")
                p += (ln + 3) // 4 * 4
            p += abs(nmis) * 8
            vars_.append(dict(name=name, type=typ, label=lab))
        elif rt == 3:
            n, = rd(e + "i")
            vl = []
            for _ in range(n):
                val = struct.unpack(e + "d", b[p:p + 8])[0]
                p += 8
                ln = b[p]
                lab = b[p + 1:p + 1 + ln].decode("latin1", "replace")
                p += ((ln + 1 + 7) // 8) * 8
                vl.append((val, lab))
            rt4, = rd(e + "i")
            assert rt4 == 4
            nv, = rd(e + "i")
            for i in rd(e + f"{nv}i"):
                vlabels[i - 1] = vl
        elif rt == 6:
            n, = rd(e + "i")
            p += 80 * n
        elif rt == 7:
            sub, size, cnt = rd(e + "3i")
            data = b[p:p + size * cnt]
            p += size * cnt
            if sub == 13:
                for pair in data.decode("latin1").split("\t"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        longnames[k] = v
        elif rt == 999:
            rd(e + "i")
            break
        else:
            raise ValueError(f"unexpected record type {rt}")
    nslots = len(vars_)
    out = np.full((ncases if ncases > 0 else 200000, nslots), np.nan)
    row = col = 0

    def put(v):
        nonlocal row, col
        out[row, col] = v if vars_[col]["type"] == 0 else np.nan
        col += 1
        if col == nslots:
            col = 0
            row += 1

    if comp == 1:
        done = False
        while not done and p < len(b):
            cmds = b[p:p + 8]
            p += 8
            for c in cmds:
                if c == 0:
                    continue
                if c == 252:
                    done = True
                    break
                if c == 253:
                    v = struct.unpack_from(e + "d", b, p)[0]
                    p += 8
                elif c in (254, 255):
                    v = np.nan
                else:
                    v = c - bias
                put(v)
    else:
        while p + 8 <= len(b):
            v = struct.unpack_from(e + "d", b, p)[0]
            p += 8
            put(np.nan if v < -1e300 else v)
    out = out[:row]
    keep = [i for i, v in enumerate(vars_) if v["type"] == 0]   # numeric variables
    names = [longnames.get(vars_[i]["name"], vars_[i]["name"]) for i in keep]
    df = pd.DataFrame(out[:, keep], columns=names)
    meta = SimpleNamespace(
        column_names_to_labels={n: _fix(vars_[i]["label"] or "") for n, i in zip(names, keep)},
        variable_value_labels={n: {v: _fix(l) for v, l in vlabels[i]} for n, i in zip(names, keep) if i in vlabels},
    )
    return df, meta


def read_sav(path=SAV):
    try:
        import pyreadstat
        return pyreadstat.read_sav(str(path))
    except ImportError:
        return _read_pure(path)

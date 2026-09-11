"""Step 0 - Export the reference survey (.sav) to open formats.

Writes data/reference/reference_survey_summer2026.csv (numeric codes of every
numeric variable; empty = system missing) and data/reference/codebook.json
(variable labels and value labels), so the data can be used without SPSS.
"""
import json
from savio import read_sav, ROOT

df, meta = read_sav()
out = ROOT / "data" / "reference"
df.to_csv(out / "reference_survey_summer2026.csv", index=False, encoding="utf-8")
cb = {v: {"label": meta.column_names_to_labels.get(v, ""),
          "values": {str(int(k)) if float(k).is_integer() else str(k): l
                     for k, l in (meta.variable_value_labels.get(v) or {}).items()}}
      for v in df.columns}
(out / "codebook.json").write_text(json.dumps(cb, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"reference survey: {df.shape[0]} respondents × {df.shape[1]} numeric variables → CSV + codebook")

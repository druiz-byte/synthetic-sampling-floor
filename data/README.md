# Data

## `reference/` — reference survey

Deustobarómetro, summer 2026 wave. Population aged 18 and over of the Basque Country
(universe 2,242,343); n = 1,000; self-administered online panel; weighted by sex, age and
social class. Published margin of error ±3.08% (95%, p = q = 0.5).

| File | Content |
|---|---|
| `reference_survey_summer2026.sav` | Respondent-level microdata (SPSS). Weight variable: `ponde`. |
| `reference_survey_summer2026.csv` | Numeric variables of the `.sav`, one row per respondent (codes; empty = missing). |
| `codebook.json` | Variable labels and value labels, `{variable: {label, values: {code: label}}}`. |

The file contains no names, contact details or other direct identifiers. Variables used in
the analysis: `ponde` (weight); `sexo`, `edad`, `prov`, `p41`, `p42`, `p45` (pairing keys);
`p2`, `p18`, `p22`, `p36`, `p38` (profile checks); and the `p*` variables mapped in
`instrument/crosswalk.json`.

## `synthetic/` — synthetic panel

**`personas_v1.json`** — the 1,000 personas (`poblacion`). Each persona reproduces the
record of one respondent of the reference survey (sex, age, province, habitat, birthplace,
education, employment, social class, language, Basque-language competence, religion,
ideology, nationalist sentiment, territorial preference, 2024 regional vote, ratings of the
regional economic and political situation, main problems). A media profile and a wellbeing
profile were added by exact statistical matching (territory × sex × age band ×
Basque-language competence) with two regional government surveys, and weights were
post-stratified by territory × Basque-language competence (fields `calibracion`,
`fuente_medios`). Names are fictitious. `analysis/07_verify_pairing.py` checks the pairing
against the microdata.

**`responses/`** — responses of the panel to the seven questionnaire blocks, generated on
16 July 2026 with Claude Haiku 4.5:

| File | Block | Items |
|---|---|---|
| `encuesta_2026-07-16_120045.json` | B1 Economic situation | 26 |
| `encuesta_2026-07-16_120212.json` | B2 Welfare and public policy | 24 |
| `encuesta_2026-07-16_120317.json` | B3 Fears | 7 |
| `encuesta_2026-07-16_120413.json` | B4 Social impact of tourism | 2 |
| `encuesta_2026-07-16_120638.json` | B5 Politics and quality of democracy | 60 |
| `encuesta_2026-07-16_120811.json` | B6 Geopolitics, wars, Trump | 24 |
| `encuesta_2026-07-16_120926.json` | B7 Profile and classification | 9 |

Each file holds `definition` (the items exactly as shown to the personas, with
`opciones`, `multiple` and `datos_reales` — the reference percentages), `results` (one
entry per persona; `resps` maps the item's position in the block to the chosen option
letters, e.g. `"0": "F,Q,U"`), `modelo`, `fecha` and `plantilla` (source template). Items
with fewer than 1,000 valid answers had unparseable or empty replies (minimum 837).

## `instrument/`

| File | Content |
|---|---|
| `templates/barometro_digital_*.json` | The seven questionnaire blocks (152 items) fed to the panel; `datos_reales` holds the reference percentages used as reference marginals. |
| `crosswalk.json` | Item ↔ survey-variable mapping produced by `analysis/01_crosswalk.py`, with the reconstruction error per item. |
| `crosswalk_readable.md` | Human-readable version: template wording next to the variable label in the `.sav`. |

## Terms of use

The data are provided to allow replication of the paper and further research on synthetic
survey panels. Please cite the paper and the Deustobarómetro when using them.

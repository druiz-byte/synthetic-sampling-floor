# How Many Synthetic Respondents Are Enough? — Replication package

Data and code for the paper *How Many Synthetic Respondents Are Enough? A Sampling-Floor
Criterion for Validating LLM-Generated Survey Panels*, by David Ruiz (Deusto Business
School, University of Deusto), ICMarkTech 2026.

The reference survey is the **Deustobarómetro** (summer 2026 wave), a public-opinion
barometer of the population aged 18 and over of the Basque Country (Spain). The survey
application used to generate the synthetic panel is **Pueblo Digital**.

The package reproduces every number, table and figure of the paper from the data included
here, without API access. It also contains the unmodified code that generated the
synthetic panel's responses, so the experiment can be run again with a new panel,
generator or reference survey.

## Quick start

```bash
pip install -r requirements.txt
python run_all.py          # steps 00-07, about one minute
```

The analyses added in the revision (weighted and paired floors, filtered items,
multiplicity, minimum detectable bias, Table 3) are run separately, from `analysis/`:

```bash
cd analysis
python r1_map.py        # persona -> respondent map      -> results/persona_map.json
python r1_paired.py     # weighted and paired floors     -> results/r1_paired.csv   (several minutes)
python r1_filtered.py   # item-specific n_eff, 2 items   -> results/items_v4.json
python r1_fig2.py       # Figs. 1-2 from items_v4.json   -> results/figures/
python r1_more.py       # toplines, weighting, BH/BY/Holm/Bonferroni
python r1_mde.py        # minimum detectable bias (80% power), 9 items within the floor
python r1_p4.py         # Table 3: expected passes vs n_s (plug-in and noise-corrected bias)
```

Outputs are written to `results/`. The versions committed in `results/` are the ones
reported in the paper; a fresh run reproduces them (fixed random seeds).

## What the study does

A synthetic panel of 1,000 personas, each built from the record of one respondent of the
reference survey, answered its 152 closed items. For each item the observed divergence
between the synthetic and the reference distribution is compared with its *sampling
floor*: the largest divergence that two finite samples drawn from the same population
would produce with 95% probability. Items below the floor are statistically
indistinguishable from an unbiased generator.

## Repository map

```
data/
  reference/      Deustobarómetro, summer 2026: .sav microdata, CSV export, codebook
  synthetic/      personas_v1.json (the panel) and responses/ (7 blocks × 1,000 personas)
  instrument/     questionnaire templates, crosswalk to the survey variables
generation/       original generation code (as run on 16 July 2026) + wrapper to re-run it
analysis/         analysis pipeline: steps 00-07 and revision scripts r1_*
results/          outputs: item-level results, tables, figures, checks, online appendix
run_all.py        runs steps 00-07
```

See `data/README.md` and `generation/README.md` for details.

## From the paper to the code

| Paper | Script | Output |
|---|---|---|
| Sect. 5.4 Instrument equivalence (152/152 items, mean error 0.58 pp) | `analysis/01_crosswalk.py` | `data/instrument/crosswalk.json`, `results/crosswalk_report.md` |
| Sect. 5.2 Design effect (DEFF 1.27, effective size 789, MoE ±3.5%) | `analysis/02_design_effect.py` | `results/design_effect.json` |
| Sects. 5.5–5.6 Floors, ratios, Monte Carlo p-values | `analysis/03_floor_analysis.py` | `results/items.csv`, `results/items_deff.json`, `results/items_srs.json` |
| Sect. 5.2, filtered items at their own effective size (515 and 212) | `analysis/r1_filtered.py` | `results/items_v4.json` |
| Table 1, Sect. 6.1 | `analysis/04_tables.py` | `results/tables.md` |
| Table 2 (independent floor), Fig. 2, Sect. 6.2 | `analysis/r1_filtered.py`, `analysis/r1_fig2.py` | `results/items_v4.json`, `results/figures/` |
| Table 2 (weight-aligned, paired floor), Sect. 3.5, Eq. (9) | `analysis/r1_map.py`, `analysis/r1_paired.py` | `results/persona_map.json`, `results/r1_paired.csv` |
| Sect. 5.6 Multiplicity (BH, BY, Holm, Bonferroni); Sect. 8.2 correlations | `analysis/r1_more.py` | console; `results/online_appendix_R1.md` (A1, A7) |
| Sect. 6.2 Minimum detectable bias, 90% CI | `analysis/r1_mde.py` | `results/online_appendix_R1.md` (A4) |
| Table 3, Sect. 6.3 (P4) | `analysis/r1_p4.py` | `results/online_appendix_R1.md` (A5) |
| Fig. 1 | `analysis/r1_fig2.py` | `results/figures/fig1_floor_vs_ns.*` |
| Sect. 3, Eqs. (3), (5) and P4 checked by simulation | `analysis/06_check_formulas.py` | `results/formula_checks.md` |
| Sects. 3.5 and 5.3, persona–respondent pairing | `analysis/07_verify_pairing.py` | `results/pairing_report.md` |
| Online appendix | — | `results/online_appendix_R1.md` |

`results/tables.md` was written for the first submission; its Tables 3–4 are superseded
by the online appendix and by `results/items_v4.json` (see A6 in the appendix).

## Reproducibility notes

- Monte Carlo floors use 20,000 replications per item with item-specific seeds
  (`seed = 977·item + block`). Paired floors use 2,000 replications (seed 2026) and
  five-fold cross-fitted regularised multinomial logits; Table 3 uses 4,000
  replications per item and n_s (seed 7). `REPS=2000 python run_all.py` gives a quick but
  noisier run of steps 00-07.
- Three items lie on the floor (B5 q27, ratio 0.93; B6 q11, 0.98; B3 q5, 0.99). Their
  classification is sensitive to the random draw.
- `analysis/savio.py` reads the `.sav` file with `pyreadstat` if installed and otherwise
  with a bundled pure-Python reader (numeric variables, variable and value labels).
- Tested with Python 3.11, numpy 2.4, scipy 1.17, pandas 3.0, matplotlib 3.10,
  scikit-learn 1.x (revision scripts only).

## Re-running the generation

`generation/run_generation.py` re-runs the seven questionnaire blocks with the original
code (Claude Haiku 4.5, `claude-haiku-4-5-20251001`, API default temperature 1.0; one
request per persona and block). It needs an Anthropic API key and cost about USD 15–20.
Generation is stochastic, so a new run reproduces the design, not the exact responses.
The prompt sent to the model is shown in `generation/prompt_example.md`.

## How to cite

Ruiz, D.: How many synthetic respondents are enough? A sampling-floor criterion for
validating LLM-generated survey panels. In: Proceedings of ICMarkTech 2026 (in press).

Please also cite the Deustobarómetro when using the reference data.

## Licence

Code: MIT (see `LICENSE`). Data: see `data/README.md`.

# How Many Synthetic Respondents Are Enough? — Replication package

Data and code for the paper *How Many Synthetic Respondents Are Enough? A Sampling-Floor
Criterion for Validating LLM-Generated Survey Panels* (ICMarkTech 2026, under review).

> Author information is withheld for double-blind review. In the anonymised version of this
> repository, the names of the reference survey and of the survey application are masked.

The package reproduces every number, table and figure of the paper from the data included
here, without API access, in about one minute. It also contains the unmodified code that
generated the synthetic panel's responses, so the experiment can be run again with a new
panel, generator or reference survey.

## Quick start

```bash
pip install -r requirements.txt
python run_all.py
```

Outputs are written to `results/`. The versions committed in `results/` are the ones
reported in the paper; a fresh run reproduces them exactly (fixed random seeds).

## What the study does

A synthetic panel of 1,000 personas answered the 152 closed items of a regional
public-opinion barometer (summer 2026 wave, n = 1,000). For each item the observed
divergence between the synthetic and the reference distribution is compared with its
*sampling floor*: the largest divergence that two finite samples drawn from the same
population would produce with 95% probability. Items below the floor are statistically
indistinguishable from an unbiased generator.

## Repository map

```
data/
  reference/      reference survey: .sav microdata, CSV export, codebook
  synthetic/      personas_v1.json (the panel) and responses/ (7 blocks × 1,000 personas)
  instrument/     questionnaire templates, crosswalk to the survey variables
generation/       original generation code (as run on 16 July 2026) + wrapper to re-run it
analysis/         analysis pipeline, steps 00-07
results/          outputs: item-level results, tables, figures, checks
run_all.py        runs steps 00-07
```

See `data/README.md` and `generation/README.md` for details.

## From the paper to the code

| Paper | Script | Output |
|---|---|---|
| Sect. 5.4 Instrument equivalence (152/152 items, mean error 0.58 pp) | `analysis/01_crosswalk.py` | `data/instrument/crosswalk.json`, `results/crosswalk_report.md` |
| Sect. 5.2 Design effect (DEFF 1.27, effective size 789, MoE ±3.5%) | `analysis/02_design_effect.py` | `results/design_effect.json` |
| Sects. 5.5–5.6 Floors, ratios, Monte Carlo p-values (DEFF and SRS) | `analysis/03_floor_analysis.py` | `results/items.csv`, `results/items_deff.json`, `results/items_srs.json` |
| Sect. 6, Tables 1–4, Benjamini–Hochberg, profile vs. non-profile items | `analysis/04_tables.py` | `results/tables.md` |
| Figs. 1–2 | `analysis/05_figures.py` | `results/figures/` |
| Sect. 3, Eqs. (3), (5) and P4 checked by simulation | `analysis/06_check_formulas.py` | `results/formula_checks.md` |
| Sects. 3.5 and 5.3, persona–respondent pairing | `analysis/07_verify_pairing.py` | `results/pairing_report.md` |

## Reproducibility notes

- Monte Carlo floors use 20,000 replications per item with item-specific seeds
  (`seed = 977·item + block`); the rescaled floors of Table 4 use 10,000 replications
  (`seed + 1`). `REPS=2000 python run_all.py` gives a quick but noisier run.
- Two items lie on the floor (B3 q5, ratio 0.99; B6 q11, ratio 0.98). Their
  classification is sensitive to the random draw; see the note under Table 4 in
  `results/tables.md`.
- `analysis/savio.py` reads the `.sav` file with `pyreadstat` if installed and otherwise
  with a bundled pure-Python reader (numeric variables, variable and value labels), which
  reproduces the crosswalk check and the design effect reported in the paper.
- Tested with Python 3.11, numpy 2.4, scipy 1.17, pandas 3.0, matplotlib 3.10.

## Re-running the generation

`generation/run_generation.py` re-runs the seven questionnaire blocks with the original
code (Claude Haiku 4.5, `claude-haiku-4-5-20251001`, API default temperature 1.0; one
request per persona and block). It needs an Anthropic API key and cost about USD 15–20.
Generation is stochastic, so a new run reproduces the design, not the exact responses.
The prompt sent to the model is shown in `generation/prompt_example.md`.

## Licence

Code: MIT (see `LICENSE`). Data: see `data/README.md`.

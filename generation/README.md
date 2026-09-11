# Generation of the synthetic responses

`server.py` and `lanzar_barometro.py` are the original files of the survey application,
unmodified, as committed on 16 July 2026 at 09:59, before the run analysed in the paper
(12:00–12:09 the same day). The application also serves an interactive avatar interview;
only the survey engine is used here:

| Function (`server.py`) | Role |
|---|---|
| `build_system_prompt(a)` | Turns a persona record into the system prompt (profile + response instructions). |
| `_ask_persona(a, preguntas)` | Builds the questionnaire message for one block and calls the model; if the reply cannot be parsed, sends one follow-up turn asking for the required format. |
| `_parse_survey_response(text, preguntas)` | Extracts the option letters (`N:X` or `N:X,Y,Z`). |
| `_survey_worker(preguntas, subset)` | Runs all personas in parallel (20 threads) and saves the block to `resultados/`. |

`lanzar_barometro.py` runs the blocks in sequence and tags each output file with its
template.

## Settings of the run

- Model: `claude-haiku-4-5-20251001` (Anthropic Messages API, version `2023-06-01`)
- Temperature: not set, i.e. the API default of 1.0
- `max_tokens`: 10 per requested option, minimum 60
- One request per persona and block: the persona answers all items of the block in a
  single reply, so answers to items of the same block are not independent draws
- Personas: `data/synthetic/personas_v1.json`; templates: `data/instrument/templates/`

`prompt_example.md` shows the exact request for one persona and one block.

## Re-running

```bash
cd generation
cp .env.example .env        # set ANTHROPIC_API_KEY; the other keys are not needed
python run_generation.py --muestra 50    # test with 50 personas
python run_generation.py                 # full run: 7 blocks × 1,000 personas
```

`run_generation.py` only redirects the input paths to this repository; the generation
logic is the original one. New files are written to `generation/resultados/` with the
same structure as `data/synthetic/responses/`. To analyse them, copy them to
`data/synthetic/responses/` (replacing the originals) and run `python run_all.py`.

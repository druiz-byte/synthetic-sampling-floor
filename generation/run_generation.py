"""Re-run the synthetic panel on the seven questionnaire blocks.

Wraps the original, unmodified generation code (server.py and
lanzar_barometro.py, as committed on 2026-07-16 before the run) so that it
reads the personas and templates from this repository and writes to
generation/resultados/.

Requirements: Python 3.10+ (standard library only) and an Anthropic API key in
generation/.env (ANTHROPIC_API_KEY=...; leave GEMINI_API_KEY and GROQ_API_KEY
unset). Cost with Claude Haiku 4.5 was roughly USD 15-20 for the full run.

Usage:  python run_generation.py                 all 7 blocks x 1,000 personas
        python run_generation.py 3               block 3 only
        python run_generation.py --muestra 50    random subset of 50 personas
Generation is stochastic (API default temperature 1.0), so a new run
reproduces the design, not the exact responses; the responses analysed in the
paper are in data/synthetic/responses/.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import server                                   # noqa: E402  (loads .env and the survey engine)
server.agents = json.loads((ROOT / "data" / "synthetic" / "personas_v1.json")
                           .read_text(encoding="utf-8"))["poblacion"]
print(f"personas loaded: {len(server.agents)}")

import lanzar_barometro                         # noqa: E402
lanzar_barometro.BLOQUES = sorted((ROOT / "data" / "instrument" / "templates").glob("barometro_digital_*.json"))

if __name__ == "__main__":
    lanzar_barometro.main()

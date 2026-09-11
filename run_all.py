"""Reproduce every result of the paper from the data in this repository.

    pip install -r requirements.txt
    python run_all.py            (about one minute; no API key needed)

Set REPS=2000 for a quick check (Monte Carlo floors become noisier and
borderline items may flip).
"""
import runpy, sys
from pathlib import Path

A = Path(__file__).resolve().parent / "analysis"
sys.path.insert(0, str(A))
for step in ("00_export_reference", "01_crosswalk", "02_design_effect", "03_floor_analysis",
             "04_tables", "05_figures", "06_check_formulas", "07_verify_pairing"):
    print(f"\n=== {step} ===")
    runpy.run_path(str(A / f"{step}.py"), run_name="__main__")

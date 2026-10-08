import sys
sys.path.insert(0, ".")
from physics_sim.nuri_rocket_staging_sim import REACT_HTML
import os

with open("scratch/test.html", "w", encoding="utf-8") as f:
    f.write(REACT_HTML)

print("Saved scratch/test.html successfully, length:", len(REACT_HTML))

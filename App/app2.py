from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Data" / "cleaned" / "amac_rental_master_v2.csv"

print(f"this is : {BASE_DIR}")      # paste what this prints in your terminal
print(DATA_PATH)     # paste what this prints

df = pd.read_csv(DATA_PATH)
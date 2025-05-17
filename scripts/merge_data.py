import pandas as pd
import os

# === Percorsi ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OWID_PATH = os.path.join(BASE_DIR, 'data', 'owid_clean.csv')
SURFACE_PATH = os.path.join(BASE_DIR, 'data', 'surface_fixed.csv')
MERGED_PATH = os.path.join(BASE_DIR,  'data', 'all_countries.csv')

# Carica i dataset
owid = pd.read_csv(OWID_PATH)
surface = pd.read_csv(SURFACE_PATH)

# Merge su 'country'
df = pd.merge(owid, surface, on='country', how='inner')

# Se presente, usa 'country_code' come alias di 'iso_code'
df["iso_code"] = df["country_code"]

# Calcolo co2/km2
df["co2_per_km2"] = df["co2"] / df["surface_km2"]
df["co2_per_km2"] = df["co2_per_km2"].round(6)

# Rimuove righe con valori nulli
df = df.dropna(subset=["country", "year", "co2", "population", "surface_km2", "co2_per_km2", "iso_code"])

# Salva solo colonne utili (incluso iso_code)
df[["country", "iso_code", "year", "co2", "population", "surface_km2", "co2_per_km2"]].to_csv(MERGED_PATH, index=False)

print(f"✅ all_countries.csv salvato con {len(df)} righe")

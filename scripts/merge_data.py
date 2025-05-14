import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OWID_PATH = os.path.join(BASE_DIR, '..', 'data', 'owid_clean.csv')
SURFACE_PATH = os.path.join(BASE_DIR, '..', 'data', 'surface_fixed.csv')
MERGED_PATH = os.path.join(BASE_DIR, '..', 'data', 'all_countries.csv')

# Carica i dataset
owid = pd.read_csv(OWID_PATH)
surface = pd.read_csv(SURFACE_PATH)

# Merge su "country"
df = pd.merge(owid, surface, on='country', how='inner')

# Calcola co2_per_km2 in modo sicuro
df['co2_per_km2'] = df['co2'] / df['surface_km2']

# Rimuovi righe con dati mancanti essenziali
df = df.dropna(subset=['country', 'year', 'co2', 'population', 'surface_km2', 'co2_per_km2'])

# Salva risultato
columns_to_save = ['country', 'year', 'co2', 'population', 'surface_km2', 'co2_per_km2']
df[columns_to_save].to_csv(MERGED_PATH, index=False)

print(f"✅ File salvato: {MERGED_PATH} con {len(df)} righe valide.")
print(df[columns_to_save].head())

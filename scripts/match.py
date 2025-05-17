import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OWID_PATH = os.path.join(BASE_DIR, '..', '..', 'data', 'owid_clean.csv')
SURFACE_PATH = os.path.join(BASE_DIR,'..', '..', 'data', 'surface_fixed.csv')

# Carica i dati
owid = pd.read_csv(OWID_PATH)
surface = pd.read_csv(SURFACE_PATH)

# Estrai ISO da OWID
df_owid_iso = owid[['country', 'iso_code']].drop_duplicates()

# Usiamo solo country da surface_fixed.csv
df_surface = surface[['country']].drop_duplicates()

# Merge su country (non ISO, perché surface_fixed.csv non ha iso_code)
merged = pd.merge(df_owid_iso, df_surface, on='country', how='left')

# Separiamo chi fa match da chi no
match = merged[merged['country'].notna()]
no_match = merged[merged['country'].isna()]

# Salva CSV
match.to_csv(os.path.join(BASE_DIR, '..', 'data', 'iso_matches.csv'), index=False)
no_match.to_csv(os.path.join(BASE_DIR, '..', 'data', 'iso_no_matches.csv'), index=False)

print(f"✅ Match trovati: {len(match)}")
print(f"❌ Senza match: {len(no_match)}")
print("📄 File salvati: iso_matches.csv e iso_no_matches.csv")

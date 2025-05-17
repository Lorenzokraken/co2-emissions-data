import os
import pandas as pd

# === Percorsi ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WB_PATH = os.path.join(BASE_DIR, '..', 'data', 'csv', 'API_AG.SRF.TOTL.K2_DS2_en_csv_v2_94516.csv')
SAVE_PATH = os.path.join(BASE_DIR, '..', 'data', 'surface_fixed.csv')
OWID_PATH = os.path.join(BASE_DIR, '..', 'data', 'owid_clean.csv')

# === Carica World Bank ===
wbg = pd.read_csv(WB_PATH, skiprows=0)
wbg.columns = [col.strip() for col in wbg.columns]

# Trova anno più recente con dati validi
year_columns = [col for col in wbg.columns if col.isdigit() and 1900 <= int(col) <= 2100]

for y in sorted(year_columns, reverse=True):
    if pd.to_numeric(wbg[y], errors='coerce').notna().sum() > 0:
        latest_year = y
        break
else:
    raise ValueError("❌ Nessun anno valido con dati disponibili.")

# Filtra solo superficie
df = wbg[wbg['Indicator Name'] == 'Surface area (sq. km)']

# Escludi entità non statali
exclude_terms = ['World', 'income', 'Euro', 'OECD', 'Arab', 'IDA', 'IBRD', 'Blend', 'Union', 'region']
df = df[~df['Country Name'].str.contains('|'.join(exclude_terms), case=False, regex=True)]

# Estrai colonne rilevanti
df_surface = df[['Country Name', latest_year]].copy()
df_surface.columns = ['country', 'surface_km2']
df_surface['surface_km2'] = pd.to_numeric(df_surface['surface_km2'], errors='coerce').round(0)

# Fix manuale Canada
df_surface.loc[df_surface['country'] == 'Canada', 'surface_km2'] = 9984670

# Drop righe nulle
df_surface = df_surface.dropna()

# === Match con OWID per country_code ===
if os.path.exists(OWID_PATH):
    df_owid = pd.read_csv(OWID_PATH)
    iso_lookup = df_owid[['country', 'iso_code']].drop_duplicates()
    df_surface = df_surface.merge(iso_lookup, on='country', how='left')
    df_surface = df_surface.rename(columns={'iso_code': 'country_code'})
else:
    df_surface['country_code'] = None  # fallback

# Salva CSV finale
df_surface.to_csv(SAVE_PATH, index=False)
print(f"✅ surface_fixed.csv salvato ({len(df_surface)} paesi)")
print(df_surface.sort_values("surface_km2", ascending=False).head(10))

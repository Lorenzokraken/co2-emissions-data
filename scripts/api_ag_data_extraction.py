import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WB_PATH = os.path.join(BASE_DIR, '..', 'data', 'API_AG.SRF.TOTL.K2_DS2_en_csv_v2_94516.csv')
SAVE_PATH = os.path.join(BASE_DIR, '..', 'data', 'surface_fixed.csv')

# Carica World Bank
wbg = pd.read_csv(WB_PATH, skiprows=0)

# Pulisce i nomi delle colonne da spazi o caratteri invisibili
wbg.columns = [col.strip() for col in wbg.columns]

# Filtra le colonne che rappresentano anni veri
year_columns = [col for col in wbg.columns if col.isdigit() and 1900 <= int(col) <= 2100]

if not year_columns:
    raise ValueError("⚠️ Nessuna colonna anno valida trovata. Controlla il file CSV.")

# Trova l'ultimo anno disponibile con almeno un valore non nullo
for y in sorted(year_columns, reverse=True):
    if pd.to_numeric(wbg[y], errors='coerce').notna().sum() > 0:
        latest_year = y
        break
else:
    raise ValueError("❌ Nessun anno valido con dati disponibili.")
print(f"\n📅 Anno più recente usato: {latest_year}")

# Filtra solo indicatori di superficie pura
wbg = wbg[wbg['Indicator Name'] == 'Surface area (sq. km)']

# Debug: mostra le prime righe grezze
print("\n👁️‍🗨️ Prime righe dopo filtro 'Indicator Name':")
print(wbg[['Country Name', latest_year]].head(10))

# Estrai le colonne desiderate
df_surface = wbg[['Country Name', latest_year]].copy()
df_surface.columns = ['country', 'surface_km2']

# Debug: prima del dropna
print("\n➡️ Prima del dropna:")
print(df_surface.head(10))

# Pulisci e converti
df_surface['surface_km2'] = pd.to_numeric(df_surface['surface_km2'], errors='coerce')

# Debug: valori statistici prima del filtro finale
print("\n📊 Statistiche 'surface_km2':")
print(df_surface['surface_km2'].describe())

# Drop finale
df_surface = df_surface.dropna(subset=['surface_km2'])

# Salva CSV
df_surface.to_csv(SAVE_PATH, index=False)
print(f"\n✅ surface_fixed.csv salvato: {SAVE_PATH} con {len(df_surface)} righe valide")
print(df_surface.head())

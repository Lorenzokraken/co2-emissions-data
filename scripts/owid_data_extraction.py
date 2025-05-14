# === owid_data_extraction.py ===
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'owid-co2-data.csv')
SAVE_PATH = os.path.join(BASE_DIR, '..', 'data', 'owid_clean.csv')

# Carica e filtra OWID
df = pd.read_csv(DATA_PATH)
df = df[df['year'] >= 1850]

# Colonne minime richieste
columns = ['country', 'year', 'co2', 'population', 'iso_code']

df = df[columns]

# Rimuovi righe con dati mancanti
df = df.dropna(subset=columns)

df.to_csv(SAVE_PATH, index=False)
print(f"✅ owid_clean.csv salvato: {SAVE_PATH}")


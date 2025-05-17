import sqlite3
import pandas as pd

# Percorso al DB
DB_PATH = "../data/co2_emissions.db"

# Connessione
conn = sqlite3.connect(DB_PATH)

# Legge la tabella countries
df = pd.read_sql("SELECT * FROM countries", conn)

# Disabilita notazione scientifica
pd.set_option("display.float_format", lambda x: f"{x:,.0f}")

# Assicura numerico
df["surface_km2"] = pd.to_numeric(df["surface_km2"], errors="coerce")

# Ordina
df_sorted = df.sort_values("surface_km2", ascending=False)

# Mostra i primi 20
print(df_sorted[["name", "surface_km2"]].head(20))

conn.close()

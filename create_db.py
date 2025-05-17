# === create_db.py ===
import pandas as pd
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# === Percorsi ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MERGED_PATH = os.path.join(BASE_DIR, '..', 'data', 'all_countries.csv')
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'co2_emissions.db')

# === Carica i dati unificati ===
df = pd.read_csv(MERGED_PATH)
df = df.dropna()

# === Evita notazione scientifica nei float durante print/debug
pd.set_option("display.float_format", lambda x: f"{x:,.3f}")

# === SQLAlchemy setup ===
Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()

# === Modelli ===
class Country(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    iso_code = Column(String, unique=True)  # 👈 AGGIUNGI QUESTA RIGA
    surface_km2 = Column(Float)
    emissions = relationship("Emission", back_populates="country")

class Year(Base):
    __tablename__ = 'years'
    year_id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True)
    emissions = relationship("Emission", back_populates="year")

class Emission(Base):
    __tablename__ = 'emissions'
    emission_id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.country_id"))
    year_id = Column(Integer, ForeignKey("years.year_id"))
    co2 = Column(Float)
    co2_per_km2 = Column(Float)
    population = Column(Integer)
    country = relationship("Country", back_populates="emissions")
    year = relationship("Year", back_populates="emissions")

# === Crea il database ===
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# === Normalizza ===
df_countries = df[["country", "surface_km2", "iso_code"]].drop_duplicates().reset_index(drop=True)
df_countries["country_id"] = df_countries.index + 1

df_years = df[["year"]].drop_duplicates().reset_index(drop=True)
df_years["year_id"] = df_years.index + 1

# Elimina colonna duplicata prima del merge
df = df.drop(columns=["surface_km2"])
df = df.merge(df_countries, on="country").merge(df_years, on="year")

# === Inserisci countries e years ===
for _, row in df_countries.iterrows():
    session.add(Country(
        country_id=int(row.country_id),
        name=row.country,
        surface_km2=float(row.surface_km2),
        iso_code=row.iso_code  # 👈 AGGIUNTO
    ))


for _, row in df_years.iterrows():
    session.add(Year(
        year_id=int(row.year_id),
        year=int(row.year)
    ))

# === Inserisci emissions ===
for _, row in df.iterrows():
    try:
        surface = float(row.surface_km2)
        co2 = float(row.co2)
        co2_per_km2 = round(co2 / surface, 3) if surface > 0 else 0
        population = int(row.population)
    except Exception as e:
        print(f"❌ Errore nella riga {row}: {e}")
        continue

    session.add(Emission(
        country_id=int(row.country_id),
        year_id=int(row.year_id),
        co2=co2,
        co2_per_km2=co2_per_km2,
        population=population
    ))

session.commit()
session.close()
print(f"✅ Database creato: {DB_PATH}")

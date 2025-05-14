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

# === SQLAlchemy setup ===
Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()

class Country(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    emissions = relationship("Emission", back_populates="country")
    iso_code = Column(String, unique=True)

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
    surface_km2 = Column(Integer)
    country = relationship("Country", back_populates="emissions")
    year = relationship("Year", back_populates="emissions")



# === Crea il database ===
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# === Normalizza ===
df_countries = df[["country"]].drop_duplicates().reset_index(drop=True)
df_countries["country_id"] = df_countries.index + 1

df_years = df[["year"]].drop_duplicates().reset_index(drop=True)
df_years["year_id"] = df_years.index + 1

df = df.merge(df_countries, on="country").merge(df_years, on="year")

# === Inserisci ===
for _, row in df_countries.iterrows():
    session.add(Country(country_id=int(row.country_id), name=row.country))

for _, row in df_years.iterrows():
    session.add(Year(year_id=int(row.year_id), year=int(row.year)))

for _, row in df.iterrows():
    session.add(Emission(
        country_id=int(row.country_id),
        year_id=int(row.year_id),
        co2=float(row.co2),
        co2_per_km2=float(row.co2_per_km2),
        population=int(row.population),
        surface_km2=int(row.surface_km2)
    ))

session.commit()
session.close()
print(f"✅ Database creato: {DB_PATH}")

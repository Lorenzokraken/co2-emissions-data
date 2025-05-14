# 🌍 CO₂ Emissions – Creazione database per analisi globali
Un progetto completo per analizzare l'evoluzione delle emissioni globali di CO₂ a partire dal 1800. 
Questa repository si concentra sulla parte **ETL e database**, trasformando dati raw in un database relazionale normalizzato in SQLite, 
pronto per essere interrogato o usato in applicazioni web.

## 🧰 Tecnologie usate
Python (pandas, SQLAlchemy)
SQLite
Dati da Our World in Data e World Bank

👤 Autore
Lorenzo Iuliano
Progetto a scopo educativo/professionale

[LinkedIn](https://www.linkedin.com/in/lorenzo-iuliano-852798220/)


---

## 📦 Contenuto della repository
```
co2-emissions-data/
├── data/
│ ├── owid-co2-data.csv
│ ├── API_AG...csv
│ ├── surface_fixed.csv
│ ├── owid_clean.csv
│ ├── all_countries.csv
│ └── co2_emissions.db
├── scripts/
│ ├── owid_data_extraction.py
│ ├── api_ag_data_extraction.py
│ ├── match.py
│ ├── merge_data.py
│ └── create_db.py
├── requirements.txt
├── LICENSE
└── README.md
```
## 🧠 Obiettivo
Convertire dati grezzi in un database strutturato e interrogabile online, utile per visualizzazioni, API, machine learning o reportistica.
Prende in input dei file CSV, permette di intervenire sulle colonne selezionando quelle necessari per poi creare un file .db con SQLAlchemy

## ⚙️ Come funziona

## 1. Estrazione dati
- owid_data_extraction.py : pulisce e filtra i dati sulle emissioni CO₂ da Our World in Data
- api_ag_data_extraction.py : estrae la superficie terrestre dai dataset della World Bank

## 2. Matching & Merge
-match.py : confronta i paesi nei due dataset e produce match con codici ISO
- merge_data.py : unisce le fonti e calcola co2_per_km2

## 3. Creazione Database
- create_db.py : genera ```co2_emissions.db``` con 3 tabelle relazionate:
- 
  - countries
  - years
  - emissions

## 🧪 Come rigenerare il database
```
bash
cd scripts/
python owid_data_extraction.py
python api_ag_data_extraction.py
python match.py
python merge_data.py
python create_db.py
```
Dopo l'ultimo passaggio troverai ```data/co2_emissions.db``` creato e pronto all'uso.



USER STORY:
Come data engineer in formazione, avevo l'obiettivo di costruire un progetto end-to-end 
che partisse da dati grezzi e arrivasse a un database strutturato, interrogabile e pronto 
per essere integrato in una dashboard o applicazione web.
Ho lavorato con fonti complesse, affrontato problemi di normalizzazione e pulizia dei dati reali,
e automatizzato ogni passaggio in Python. Questo progetto rappresenta un esempio concreto del mio 
approccio pratico al ciclo completo dei dati.


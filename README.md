# 🏠 Avito Data Pipeline

> Scraping · Data Cleaning · Data Warehouse Modeling

Pipeline de données industriel complet qui transforme des annonces immobilières brutes d'Avito.ma en une architecture prête pour l'analyse décisionnelle (Power BI) et le Machine Learning.

---

## 📐 Architecture

```
Avito.ma → Extract → Staging → Clean → Data Warehouse
                                         ├── bi_schema  (Star Schema → Power BI)
                                         └── ml_schema  (OBT → Machine Learning)
```

---

## 🗂️ Structure du projet

```
avito/
├── extract/
│   └── scraper.py          # Scraping Selenium (headless Chrome)
├── clean/
│   └── cleaner.py          # Nettoyage + Feature Engineering
├── warehouse/
│   ├── database_setup.py   # Création des schémas et tables
│   └── load_to_warehouse.py# Chargement + Validation + Archivage
├── pipeline/
│   └── run_pipeline.py     # Orchestrateur (scraping → clean → warehouse)
├── staging/
│   └── archive/            # Fichiers CSV archivés après chargement
├── logs/                   # Logs horodatés de chaque exécution
├── docker-compose.yml      # PostgreSQL + pgAdmin
├── Dockerfile.pipeline     # Image Docker du pipeline
├── requirements.txt        # Dépendances Python
└── .env                    # Variables d'environnement (non versionné)
```

---

## ⚙️ Installation

### Prérequis

* Docker & Docker Compose
* Python 3.12+
* Google Chrome

### 1. Cloner le projet

```bash
git clone <repo-url>
cd avito
```

### 2. Configurer les variables d'environnement

```bash
cp .env.example .env
```

### 3. Lancer la base de données

```bash
docker-compose up -d db pgadmin
```

### 4. Installer les dépendances Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Créer la structure du Data Warehouse

```bash
python3 warehouse/database_setup.py
```

---

## 🚀 Lancer le pipeline

```bash
source venv/bin/activate
python3 pipeline/run_pipeline.py
```

Le pipeline exécute automatiquement :

1. **Scraping** — collecte des annonces depuis Avito.ma
2. **Cleaning** — nettoyage, imputation, feature engineering
3. **Warehouse** — chargement, validation, archivage du staging

En cas d'échec, chaque étape est relancée automatiquement **3 fois** avant d'arrêter le pipeline.

---

## 🗄️ Data Warehouse

### BI Schema (`bi_schema`) — Star Schema

| Table                    | Description                          |
| ------------------------ | ------------------------------------ |
| `fact_annonce`         | Table de faits (prix, price_per_m²) |
| `dim_localisation`     | Dimension ville                      |
| `dim_caracteristiques` | Dimension surface, segment           |

### ML Schema (`ml_schema`) — One Big Table

| Table                 | Description                                 |
| --------------------- | ------------------------------------------- |
| `obt_avito_dataset` | Dataset plat prêt pour le Machine Learning |

> ⚠️ Les transformations ML (scaling, encoding, SMOTE…) ne sont **pas** effectuées ici. Elles sont réalisées après extraction dans le Brief ML.

---

## 📊 Accès pgAdmin

```
URL      : http://localhost:8080
Email    : valeur de PGADMIN_EMAIL dans .env
Password : valeur de PGADMIN_PASSWORD dans .env
Host DB  : db
Port     : 5432
```

---

## 📋 Données collectées

| Champ            | Description                                 |
| ---------------- | ------------------------------------------- |
| `title`        | Titre de l'annonce                          |
| `price`        | Prix en MAD                                 |
| `city`         | Ville                                       |
| `surface_m2`   | Surface en m²                              |
| `rooms`        | Nombre de chambres                          |
| `baths`        | Nombre de salles de bain                    |
| `link`         | Lien vers l'annonce                         |
| `price_per_m2` | Prix par m² (feature engineered)           |
| `segment`      | Segment marché : Luxe / Moyen / Economique |

> 🔒 Aucune donnée personnelle n'est collectée (pas de noms, téléphones ou emails).

---

## 🛡️ Conformité RGPD

* Collecte minimale — uniquement les données nécessaires à l'analyse
* Exclusion stricte de toute information personnelle
* Logs de traçabilité à chaque étape
* Archivage horodaté des fichiers staging
* Durée de conservation limitée via rotation des archives

---

## 🔧 Technologies

| Outil          | Usage                      |
| -------------- | -------------------------- |
| Python 3.12    | Langage principal          |
| Selenium       | Scraping web               |
| Pandas         | Traitement des données    |
| PostgreSQL 15  | Base de données           |
| SQLAlchemy     | ORM / connexion DB         |
| Docker Compose | Infrastructure             |
| pgAdmin 4      | Interface base de données |

---

# AMAC Rental Intelligence Dashboard

> A full-stack data pipeline for analysing the residential rental market across Abuja Municipal Area Council (AMAC) districts — from raw web scraping to an interactive Streamlit dashboard.

---

## Overview

This project provides a comprehensive, data-driven view of the Abuja rental market. It scrapes live listings from two major Nigerian property portals, cleans and consolidates the data through a structured pipeline, and surfaces actionable market intelligence through an interactive web dashboard.

The dashboard allows users to explore rental price distributions, compare districts by tier (Budget, Mid-Range, Luxury), and analyse market composition by property category — all with dynamic, real-time filters.

---

## Project Architecture

```
AMAC-Rental-Intelligence-Dashboard/
│
├── Scraper/
│   ├── scraper.ipynb              # Nigeria Property Centre scraper
│   └── 01_ppro_scrapper.ipynb     # Property Pro NG scraper
│
├── Notebooks/
│   ├── data_cleaning_npc.ipynb    # Cleaning pipeline for NPC data
│   ├── data_cleaning_ppro.ipynb   # Cleaning pipeline for PropertyPro data
│   └── data_analysis.ipynb        # Feature engineering, EDA, and master dataset creation
│
├── Data/
│   ├── messy.csv                  # Raw, unprocessed listings (sample)
│   └── cleaned/
│       ├── amac_rental_cleaned_v1.csv
│       ├── amac_rental_cleaned_v2.csv
│       ├── amac_ppro_rental_cleaned_v1.csv
│       ├── amac_ppro_rental_cleaned_v2.csv
│       └── amac_rental_master_v2.csv   # Final dataset used by the dashboard
│
├── App/
│   └── App.py                     # Streamlit dashboard application
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Data Pipeline

The project follows a structured Extract → Transform → Load (ETL) pipeline:

### 1. Extraction (Scraper/)
Two independent scrapers collect rental listings from:
- **Nigeria Property Centre** (`nigeriapropertycentre.com`) — 234 pages scraped
- **Property Pro NG** (`propertypro.ng`) — 104 pages scraped

Both scrapers implement production-grade reliability features:
- `requests.Session` with persistent TCP connections for realistic browsing behaviour
- Rotating user-agent strings to reduce bot detection risk
- Referer header injection to simulate natural page navigation
- Exponential backoff retry logic (`Retry` with `backoff_factor=2`) for transient server errors
- Randomised sleep intervals (3–7 seconds) between requests
- Checkpoint saves every 10 pages to prevent data loss on failure
- Per-listing `try/except` blocks so one bad record never crashes the run

### 2. Transformation (Notebooks/)

**Cleaning (NPC & PropertyPro):**
- Bedroom count extracted from raw property title strings via regex
- Property types normalised into 3 canonical categories: `Duplex`, `Apartment`, `Bungalow`
- Non-residential listings (office space, hotels, commercial) filtered out
- `house` records reclassified by bedroom count: ≥4 beds → Duplex, <4 beds → Bungalow
- USD-denominated listings converted to Naira (exchange rate: ₦1,354.97/$1, as of Feb 10, 2026)
- District extracted from free-text location strings against a 24-district AMAC reference list
- Listings outside AMAC boundaries dropped

**Analysis & Feature Engineering:**
- Datasets from both sources merged with a `Source` tag for data lineage tracking
- Duplicate removal by `[Bedrooms, Price, District, Property Category, Source]`
- Outlier capping: bedroom count ≤ 6, price between ₦250,000 and ₦50,000,000
- `Price_per_Bed` derived metric created for fair cross-district comparison
- `District Tier` engineered using data-driven quantile classification (q=3) on district median prices → `Budget`, `Mid-Range`, `Luxury`

### 3. Load (App/)
The master dataset (`amac_rental_master_v2.csv`) is loaded into a Streamlit app with:
- 5 interactive sidebar filters (price range, bedrooms, district, category, tier)
- 4 KPI metrics (average rent, median rent, most expensive district, listing count)
- 6 Plotly charts: price distribution histogram, bedroom box plots, district bar chart, tier segmentation, category pie chart, and source volume chart
- Empty-state handling for aggressive filter combinations

---

## Dashboard Features

| Feature | Description |
|---|---|
| Price Range Slider | Filter listings by annual rent in Naira |
| Bedroom Filter | Multi-select for 1–6 bedroom properties |
| District Filter | Drill into any of the 24 AMAC districts |
| Property Category | Filter by Apartment, Duplex, or Bungalow |
| District Tier | Budget / Mid-Range / Luxury segmentation |
| KPI Cards | Live metrics that respond to all filters |
| Price Distribution | Histogram with marginal box plot |
| Bedroom Price Variance | Box plots per bedroom count |
| District Comparison | Horizontal bar chart sorted by average rent |
| Market Segmentation | Tier-level average rent comparison |
| Category Market Share | Donut chart of listing composition |
| Source Volume | Listing count by data source |

---

## Key Market Insights

Based on the dataset of **4,920 cleaned listings** collected in February 2026:

- **Maitama**, **Jabi** and **Asokoro** consistently rank as the most expensive districts
- **Lugbe**, **Karshi** and **Lokogoma** represent the most affordable entry points into the market
- Apartments dominate listing volume, while Duplexes command the highest median rents
- The median-to-mean gap reveals significant price skew — a small number of high-value properties pull the average up considerably
- Listings from Nigeria Property Centre and Property Pro NG show broadly consistent pricing, validating cross-source data integrity

---

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/PROD-A33A/AMAC-Rental-Intelligence-Dashboard.git
cd AMAC-Rental-Intelligence-Dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
cd App
streamlit run App.py
```



> **Note:** Raw data files are excluded from this repository (see `.gitignore`). The `Data/cleaned/` directory contains the processed master dataset required by the dashboard.

---



## Tech Stack

| Layer | Tools |
|---|---|
| Scraping | `Python`, `requests`, `BeautifulSoup4` |
| Data Processing | `pandas`, `numpy`, `re` |
| Analysis | `pandas`, `numpy`|
| Dashboard | `Streamlit`, `Plotly Express` |
| Version Control | `Git`, `GitHub` |

---

## Data Sources

- [Nigeria Property Centre](https://nigeriapropertycentre.com) — residential listings, Abuja
- [Property Pro NG](https://propertypro.ng) — residential listings, Abuja

*Data collected February 2026. Prices reflect market conditions at time of collection.*

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Abba Onoja**    
EMAIL: abbaonoja38@gmail.com  | LinkedIn: www.linkedin.com/in/abba-o-050b003a8

For any further questions or inquiries, feel free to reach out. We are happy to assist you with any queries.



# Table Aggregator

A modular data processing pipeline built with Python 3, `pandas`, `pyarrow`, and `duckdb` for cleaning, transforming, and aggregating large structured datasets.

Each processing step is implemented as a separate script with CLI arguments. Project is managed using [Poetry](https://python-poetry.org/).

---

## Installation

```bash
git clone https://github.com/kepeld/table-aggregator.git
cd table-aggregator
poetry install
````

---

## Example: Process First 10,000 Rows

```bash
# 1. Initial cleanup and export to Parquet
poetry run python scripts/01_clean.py \
 -i data/dataset.txt \
 -o data/tmp/clean.parquet -n 10000

# 2. Deduplication
poetry run python scripts/02_dedupe.py \
 -i data/tmp/clean.parquet \
 -o data/processed/dedup.parquet

# 3. Fill missing values (e.g., phone, email)
poetry run python scripts/05_fill.py \
 -i data/processed/dedup.parquet \
 -o data/processed/filled.parquet \
 --keys Прізвище "Ім'я" По_батькові \
 --cols Телефон Email

# 4. Group full record fields into lists
poetry run python scripts/06_group_lists.py \
 -i data/processed/filled.parquet \
 -o data/processed/grouped.parquet \
 --keys Прізвище "Ім'я" По_батькові \
 --cols Телефон Email Адрес Snils INN

# 5. Split into chunks with index
poetry run python scripts/03_chunking.py \
 -i data/processed/grouped.parquet \
 -o data/chunks -n 1000
```

---

## Script Overview

| Script              | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| `01_clean.py`       | Cleans raw text data, converts types, saves as Parquet     |
| `02_dedupe.py`      | Removes duplicates by full name and birth date             |
| `05_fill.py`        | Fills missing values in selected columns by group          |
| `06_group_lists.py` | Aggregates selected fields into lists per person group     |
| `03_chunking.py`    | Splits large dataset into indexed chunks of fixed size     |
| `04_aggregate.py`   | (Deprecated) Early aggregation version, kept for reference |
---
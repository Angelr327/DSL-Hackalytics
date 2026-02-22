"""
data_processing.py

Handles:
- Loading CSVs
- Cleaning
- Validation
- Merging
- UN Key Calculations
- Sorting
"""

import pandas as pd
from config import RESPONSE_PATH, METRICS_PATH


def build_master_table():
    # -----------------------------
    # Load CSV files
    # -----------------------------
    response_df = pd.read_csv(RESPONSE_PATH)
    metrics_df = pd.read_csv(METRICS_PATH)

    # -----------------------------
    # Standardize column names
    # -----------------------------
    response_df.columns = response_df.columns.str.strip().str.lower()
    metrics_df.columns = metrics_df.columns.str.strip().str.lower()

    # -----------------------------
    # Normalize ISO3
    # -----------------------------
    response_df["country_iso3"] = (
        response_df["country_iso3"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    metrics_df["country_iso3"] = (
        metrics_df["country_iso3"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # -----------------------------
    # Normalize year
    # -----------------------------
    response_df["year"] = pd.to_numeric(response_df["year"], errors="coerce")
    metrics_df["year"] = pd.to_numeric(metrics_df["year"], errors="coerce")

    # -----------------------------
    # Merge on ISO3 + year
    # -----------------------------
    df = pd.merge(
        response_df,
        metrics_df,
        on=["country_iso3", "year"],
        how="inner"
    )

    # Remove duplicates if any
    df = df.drop_duplicates(subset=["country_iso3", "year"])

    # -----------------------------
    # Ensure numeric columns
    # -----------------------------
    numeric_cols = [
        "people_in_need",
        "people_targeted",
        "requirements",
        "funding"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols)

    # Remove impossible values
    df = df[df["people_in_need"] > 0]
    df = df[df["requirements"] > 0]

    # -----------------------------
    # UN KEY METRICS
    # -----------------------------

    # Funding per person in need
    df["funding_per_pin"] = df["funding"] / df["people_in_need"]

    # % of appeal funded
    df["coverage_ratio"] = df["funding"] / df["requirements"]

    # Absolute funding gap
    df["funding_gap"] = df["requirements"] - df["funding"]

    # People targeting gap
    df["targeting_gap"] = df["people_in_need"] - df["people_targeted"]

    # % of people in need actually targeted
    df["targeting_ratio"] = df["people_targeted"] / df["people_in_need"]

    # Sort by worst coverage (lowest first)
    df = df.sort_values(by="coverage_ratio", ascending=True)

    return df


def get_top_countries(df, n=10):
    return df.sort_values(by="funding", ascending=False).head(n)


def get_country(df, iso3):
    iso3 = iso3.strip().upper()
    return df[df["country_iso3"] == iso3]
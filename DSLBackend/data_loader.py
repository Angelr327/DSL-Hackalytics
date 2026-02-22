"""
data_loader.py

Handles loading raw CSV files only.
No cleaning or calculations here.
"""

import pandas as pd
import os
from config import DATA_DIR


def load_response_plans():
    path = os.path.join(DATA_DIR, "response_plans.csv")
    return pd.read_csv(path)


def load_crisis_metrics():
    path = os.path.join(DATA_DIR, "crisis_metrics.csv")
    return pd.read_csv(path)
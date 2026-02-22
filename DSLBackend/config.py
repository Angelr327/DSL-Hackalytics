"""
config.py

Centralizes file paths for dataset loading.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESPONSE_PATH = os.path.join(BASE_DIR, "Data", "response_plans.csv")
METRICS_PATH = os.path.join(BASE_DIR, "Data", "metrics.csv")
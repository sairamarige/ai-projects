"""
config.py
=========
Central place for logging setup and business rules. Pulling these out of
the agents means a rule change (a new tax slab, a new grade boundary)
doesn't require touching agent logic at all.
"""

import logging

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)-20s | %(message)s"


def configure_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt="%H:%M:%S")


# ---------------------------------------------------------------------------
# Student rules
# ---------------------------------------------------------------------------
MARK_MIN, MARK_MAX = 0, 100
GRADE_BOUNDARIES = [   # (minimum percentage, grade) — checked highest first
    (90, "A+"),
    (75, "A"),
    (60, "B"),
    (40, "C"),
    (0, "F"),
]

# ---------------------------------------------------------------------------
# Employee rules
# ---------------------------------------------------------------------------
HRA_RATE = 0.40
TRAVEL_ALLOWANCE = 2000
TAX_SLABS = [   # (gross threshold, rate) — checked highest first
    (80000, 0.20),
    (50000, 0.12),
    (0, 0.05),
]
BONUS_RATING_PCT = {"high": 0.15, "medium": 0.08, "low": 0.03}
LOYALTY_BONUS_PER_YEAR = 500

# ---------------------------------------------------------------------------
# Shopping rules
# ---------------------------------------------------------------------------
BULK_QTY_THRESHOLD = 2
BULK_DISCOUNT_RATE = 0.10
CART_DISCOUNT_THRESHOLD = 5000
CART_DISCOUNT_RATE = 0.05
TAX_RATE = 0.18
CARD_PAYMENT_THRESHOLD = 3000

# ---------------------------------------------------------------------------
# Data sources (stand-ins for a DB/API — see data_loader.py)
# ---------------------------------------------------------------------------
DATA_DIR = "data"
STUDENTS_CSV = f"{DATA_DIR}/students.csv"
EMPLOYEES_CSV = f"{DATA_DIR}/employees.csv"
PRODUCTS_CSV = f"{DATA_DIR}/products.csv"

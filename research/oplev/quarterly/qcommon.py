"""Shared constants and date helpers for the H5/H6 quarterly study."""
from __future__ import annotations

import datetime as dt
from functools import lru_cache
from pathlib import Path

import pandas as pd
from dateutil.easter import easter

HERE = Path(__file__).resolve().parent
OPLEV = HERE.parent
CACHE = HERE / "cache"
CF = CACHE / "cf"

# Revenue tags: same order as research/oplev/build_panel.py (first total tag wins;
# goods + services summed only when no total tag is reported for the period).
REV_TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
            "RevenueFromContractWithCustomerIncludingAssessedTax"]
REV_PART_TAGS = ["SalesRevenueGoodsNet", "SalesRevenueServicesNet"]
OPINC_TAG = "OperatingIncomeLoss"
RPO_TAG = "RevenueRemainingPerformanceObligation"

# forms whose facts count as "reported" (first-reported values); triggers are originals only
PERIODIC = {"10-K", "10-Q", "10-K/A", "10-Q/A", "10-KT", "10-QT", "10-KT/A", "10-QT/A"}
TRIGGER = {"10-K", "10-Q"}

REV_MIN = 10e6
MCAP_MIN = 50e6
LARGE = 2e9
FY_STALE_DAYS = 550        # latest fiscal year must have ended within this many days
SHARES_STALE_DAYS = 400    # a share count older than this is not used
MCAP_RATIO_BAND = (0.002, 100.0)   # as build_panel.py
HIST_FLOAT_BAND = (0.2, 5.0)       # as build_panel.py

LAST_COMPLETE_MONTH = pd.Timestamp("2026-08-01")   # returns through August 2026


@lru_cache(maxsize=None)
def last_trading_day(year: int, month: int) -> pd.Timestamp:
    """Last NYSE trading day of a month: last weekday, stepping back over the two
    holidays that can fall on a month's last weekday (Good Friday, Memorial Day)."""
    d = (pd.Timestamp(year, month, 1) + pd.offsets.MonthEnd(0)).date()
    gf = easter(year) - dt.timedelta(days=2)
    while True:
        if d.weekday() >= 5:
            d -= dt.timedelta(days=1)
            continue
        memorial = d.month == 5 and d.weekday() == 0 and d.day >= 25
        if d == gf or memorial:
            d -= dt.timedelta(days=1)
            continue
        return pd.Timestamp(d)


def formation_month(filed: pd.Timestamp) -> pd.Timestamp:
    """Month (as month-start timestamp) at whose last trading day a filing enters:
    the first month-end strictly after the filing date."""
    y, m = filed.year, filed.month
    if filed < last_trading_day(y, m):
        return pd.Timestamp(y, m, 1)
    n = pd.Timestamp(y, m, 1) + pd.offsets.MonthBegin(1)
    return n

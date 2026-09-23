"""Shared helpers: load data, average a monthly series over a fiscal quarter's exact dates."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_quarters():
    Q = pd.read_csv(DATA / "calm_quarterly.csv", parse_dates=["period_start", "period_end"])
    Q["weeks"] = ((Q.period_end - Q.period_start).dt.days + 1) / 7.0
    Q["label"] = "FY" + Q.fy.astype(str).str[2:] + " Q" + Q.q.astype(str)
    return Q


def load_prices():
    return pd.read_csv(DATA / "prices_monthly.csv", parse_dates=["month"]).set_index("month")


def daily(series):
    """Monthly series (month-start index) -> daily step series (each day carries its month's value)."""
    s = series.dropna()
    idx = pd.date_range(s.index.min(), s.index.max() + pd.offsets.MonthEnd(0), freq="D")
    return s.reindex(idx, method="ffill")


def qavg(dser, start, end, lag_days=0):
    """Average of a daily series over [start, end] shifted back by lag_days. NaN if not fully covered."""
    a, b = pd.Timestamp(start) - pd.Timedelta(days=lag_days), pd.Timestamp(end) - pd.Timedelta(days=lag_days)
    if a < dser.index.min() or b > dser.index.max():
        return np.nan
    return float(dser.loc[a:b].mean())

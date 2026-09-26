"""Daily adjusted closes from Yahoo (yfinance), throttled, one cached file per ticker in cache/yahoo/px/.
Rate-limited tickers are re-queued (never cached as missing); a ticker is recorded as having no Yahoo data
only after Yahoo answers "no data / delisted" for it twice.
Priority order: event companies first (arrangement filers), then the rest of the benchmark universe.
Writes cache/prices_close.parquet (dates x yahoo tickers) and data/price_coverage.csv."""
import sys
import time
from pathlib import Path

import pandas as pd
import yfinance as yf
from yfinance.exceptions import YFRateLimitError

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

PX = sec.CACHE / "yahoo" / "px"
MISS = sec.CACHE / "yahoo" / "missing"
START, END = "2022-12-01", "2026-09-26"
BATCH = 20
EXTRA = ["SPY", "IWM"]
PART, NPART = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 1)


def done(s):
    p = PX / f"{s}.parquet"
    if p.exists():
        return "split" in pd.read_parquet(p).columns  # files from the first pass lack split data
    return (MISS / f"{s}.2").exists()


def mark_missing(s):
    n1 = MISS / f"{s}.1"
    if n1.exists():
        (MISS / f"{s}.2").write_text("no data twice")
    else:
        n1.write_text("no data once")


def canary_ok():
    """Yahoo sometimes answers a rate-limited request with an empty frame; check a ticker that surely has data."""
    try:
        h = yf.Ticker("MSFT").history(period="5d", raise_errors=True)
        return h is not None and not h.empty
    except Exception:
        return False


def one(s):
    """Returns 'ok', 'missing' or 'ratelimit'."""
    r = _one(s)
    if r == "missing?":
        if canary_ok():
            mark_missing(s)
            return "missing"
        return "ratelimit"
    return r


def _one(s):
    try:
        h = yf.Ticker(s).history(start=START, end=END, auto_adjust=True, actions=True, raise_errors=True)
    except YFRateLimitError:
        return "ratelimit"
    except Exception as e:
        msg = str(e)
        if "Rate" in msg or "Too Many" in msg or "429" in msg:
            return "ratelimit"
        return "missing?"
    if h is None or h.empty or h["Close"].notna().sum() == 0:
        return "missing?"
    h = h[h["Close"].notna()]
    out = pd.DataFrame({"close": h["Close"],
                        "split": h["Stock Splits"] if "Stock Splits" in h else 0.0})
    out.index = pd.to_datetime(out.index).tz_localize(None).normalize()
    out.to_parquet(PX / f"{s}.parquet")
    return "ok"


def run():
    PX.mkdir(parents=True, exist_ok=True)
    MISS.mkdir(parents=True, exist_ok=True)
    tk = pd.read_csv(sec.ROOT / "data" / "tickers.csv")
    arr = pd.read_csv(sec.ROOT / "data" / "arrangements.csv.gz", usecols=["cik", "is_trm", "is_adopt"], low_memory=False)
    tk["pri"] = 0
    tk.loc[tk.cik.isin(set(arr.cik[arr.is_adopt == True])), "pri"] = 1
    tk.loc[tk.cik.isin(set(arr.cik[arr.is_trm == True])), "pri"] = 2
    tk = tk.sort_values("pri", ascending=False, kind="stable")
    order = list(dict.fromkeys(EXTRA + list(tk.yahoo.dropna()) + list(tk.yahoo_alt.dropna())))
    order = [s for s in order if len(s) <= 8 and s not in ("-", "N-A", "FALSE", "TRUE", "NONE")]
    gap = 0.8
    for rnd in range(6):
        todo = [s for i_, s in enumerate(order) if not done(s) and i_ % NPART == PART]
        if not todo:
            break
        print(f"round {rnd}: {len(todo)} to do", flush=True)
        for i, s in enumerate(todo):
            res = one(s)
            while res == "ratelimit":
                gap = min(gap * 1.5, 5.0)
                print(f"  rate limited at {s}; sleeping 120s, gap {gap:.1f}s", flush=True)
                time.sleep(120)
                res = one(s)
            gap = max(0.8, gap * 0.98)
            time.sleep(gap)
            if i % 200 == 0:
                print(f"  {i}/{len(todo)} (have {len(list(PX.glob('*.parquet')))})", flush=True)
    if NPART > 1:
        return
    frames = {p.stem: pd.read_parquet(p)["close"] for p in PX.glob("*.parquet")}
    px = pd.DataFrame(frames).sort_index()
    px.to_parquet(sec.CACHE / "prices_close.parquet")
    cov = pd.DataFrame({"yahoo": order, "has_price": [s in frames for s in order],
                        "no_yahoo_data": [(MISS / f"{s}.2").exists() for s in order]})
    cov.to_csv(sec.ROOT / "data" / "price_coverage.csv", index=False)
    print("tickers", len(order), "with prices", int(cov.has_price.sum()), "no data", int(cov.no_yahoo_data.sum()))


if __name__ == "__main__":
    run()

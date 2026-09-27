"""Step 5: daily prices from Yahoo for every sponsor ticker plus SPY, IWM, XBI.

Chunks of 40 tickers, 2 s between calls. SPY rides along in every call as a sentinel: if it
comes back empty the call was rate limited and is retried after a back-off instead of the
tickers being marked "no data". Output: cache/prices_daily.pkl (long: date, ticker, adj =
split- and dividend-adjusted close, close = split-adjusted close, split = split ratio that day),
cache/price_status.csv (ok / nodata per ticker).
"""
import sys, time
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
PX = HERE / "cache" / "prices_daily.pkl"
ST = HERE / "cache" / "price_status.csv"
START = "2014-06-01"
SENTINEL = "SPY"


def chunk_download(tks):
    import yfinance as yf
    req = list(dict.fromkeys(tks + [SENTINEL]))
    try:
        df = yf.download(req, start=START, auto_adjust=False, actions=True, progress=False,
                         threads=True, group_by="column", multi_level_index=True)
    except Exception:
        return None
    if df is None or df.empty or ("Adj Close", SENTINEL) not in df.columns or df[("Adj Close", SENTINEL)].notna().sum() < 1000:
        return None
    return df


def main(tickers):
    have = pd.read_pickle(PX) if PX.exists() else pd.DataFrame()
    status = pd.read_csv(ST) if ST.exists() else pd.DataFrame(columns=["ticker", "status"])
    done = set(status.ticker)
    todo = [t for t in dict.fromkeys(tickers + ["SPY", "IWM", "XBI"]) if t not in done]
    print(len(todo), "tickers to fetch")
    frames, st = [have] if len(have) else [], []
    for i in range(0, len(todo), 40):
        part = todo[i:i + 40]
        for attempt in range(6):
            close = chunk_download(part)
            if close is not None: break
            print("  rate limited? backing off", 60 * (attempt + 1)); time.sleep(60 * (attempt + 1))
        else:
            print("  giving up on chunk", i); continue
        for t in part:
            if ("Adj Close", t) in close.columns and close[("Adj Close", t)].notna().sum() > 0:
                sub = pd.DataFrame({"adj": close[("Adj Close", t)], "close": close[("Close", t)],
                                    "split": close[("Stock Splits", t)] if ("Stock Splits", t) in close.columns else 0.0})
                sub = sub.dropna(subset=["adj"]).reset_index().rename(columns={"Date": "date"})
                sub["ticker"] = t; frames.append(sub); st.append((t, "ok"))
            else:
                st.append((t, "nodata"))
        print(f"  {min(i + 40, len(todo))}/{len(todo)}", flush=True)
        if (i // 40) % 5 == 4 or i + 40 >= len(todo):          # checkpoint every 200 tickers
            px = save(frames, status, st)
            frames, status, st = [px], pd.read_csv(ST), []
        time.sleep(2.0)
    print("saved", pd.read_pickle(PX).shape)


def save(frames, status, st):
    px = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    px["date"] = pd.to_datetime(px["date"]).dt.tz_localize(None) if getattr(px["date"].dt, "tz", None) else pd.to_datetime(px["date"])
    px = px.drop_duplicates(["date", "ticker"], keep="last").sort_values(["ticker", "date"])
    px.to_pickle(PX)
    pd.concat([status, pd.DataFrame(st, columns=["ticker", "status"])]).to_csv(ST, index=False)
    return px


if __name__ == "__main__":
    tick = pd.read_csv(sys.argv[1]).ticker.dropna().astype(str).tolist()
    main(tick)

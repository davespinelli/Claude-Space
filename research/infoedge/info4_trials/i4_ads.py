"""Step 1g: depositary-share ratio for foreign issuers (20-F / 40-F / 6-K filers) and for any
other priced sponsor whose computed market value is currently above $1B (some 10-K filers,
such as BeiGene or Zai Lab, also trade as ADSs).

Their XBRL share counts are ordinary shares, but the US price is per ADS. For each such
sponsor with a Yahoo ticker, compare Yahoo's current market value with (latest XBRL share
count x current price). If they differ by more than 1.5x, the ratio (rounded to a common
ADS ratio) is stored and later applied to every date. One Yahoo request every 2 s.
Output: cache/ads_ratio.csv (cik, ticker, yahoo_mcap, xbrl_mcap, ratio).
"""
import json, time
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
COMMON = np.array([1 / 40, 1 / 20, 1 / 10, 1 / 8, 1 / 6, 1 / 5, 1 / 4, 1 / 3, 1 / 2, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 40, 50, 100])


def main():
    import yfinance as yf
    comp = pd.read_csv(HERE / "data/sponsor_companies_priced.csv")
    big = comp.max_mcap.fillna(0) > 1e9 if "max_mcap" in comp else False
    comp = comp[(comp.foreign | big) & comp.ticker.notna()]
    sh = pd.read_csv(HERE / "cache/shares.csv", names=["cik", "filed", "end", "val", "src"])
    sh = sh[sh.src == "dei"].groupby(["cik", "filed", "end"], as_index=False).val.sum().sort_values("filed")
    outf = HERE / "cache/ads_ratio.csv"
    prev = pd.read_csv(outf) if outf.exists() else pd.DataFrame(columns=["cik"])
    out = prev.to_dict("records")
    for r in comp.itertuples():
        if r.cik in set(prev.cik): continue
        s = sh[sh.cik == r.cik]
        if s.empty: continue
        shares = float(s.val.iloc[-1])
        try:
            fi = yf.Ticker(r.ticker).fast_info
            ymc, px = fi.get("marketCap"), fi.get("lastPrice")
        except Exception:
            ymc, px = None, None
        time.sleep(2.0)
        if not ymc or not px: continue
        xm = shares * px
        q = ymc / xm
        ratio = float(COMMON[np.argmin(np.abs(np.log(COMMON) - np.log(q)))]) if (q > 1.5 or q < 1 / 1.5) else 1.0
        out.append({"cik": r.cik, "ticker": r.ticker, "yahoo_mcap": ymc, "xbrl_mcap": xm, "q": q, "ratio": ratio})
        print(r.ticker, round(q, 3), ratio, flush=True)
    pd.DataFrame(out).to_csv(outf, index=False)


if __name__ == "__main__":
    main()

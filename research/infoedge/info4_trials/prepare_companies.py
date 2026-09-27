"""Step 5b: pick one Yahoo ticker per sponsor company and flag foreign issuers.

Ticker: among the company's current SEC tickers, one on a US exchange (not OTC) if any has Yahoo
prices, otherwise the one with the most Yahoo price rows.
Foreign: the company has filed a 20-F or 40-F (EDGAR submissions).
Output: data/sponsor_companies_priced.csv; data/excluded_no_price.csv lists every kept
company with no Yahoo price (its events become "missing").
"""
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent


def main():
    comp = pd.read_csv(HERE / "data/sponsor_companies.csv")
    tk = pd.read_csv(HERE / "cache/tickers_for_prices.csv")
    px = pd.read_pickle(HERE / "cache/prices_daily.pkl")
    rows_per = px.groupby("ticker").size()
    # exchange of each ticker from the EDGAR submissions file (tickers and exchanges are aligned)
    exch = {}
    for cik in comp.cik:
        f = HERE / "cache/submissions" / f"CIK{int(cik):010d}.json"
        if f.exists():
            j = json.load(open(f))
            for t, x in zip(j.get("tickers") or [], j.get("exchanges") or []):
                exch[t] = x or ""
    best = {}
    for cik, g in tk.groupby("cik"):
        # prefer a ticker on a US exchange (Nasdaq/NYSE/CBOE) over an OTC line; then most price rows
        cand = [(exch.get(t, "") not in ("", "OTC"), rows_per.get(t, 0), t) for t in g.ticker]
        cand = [c for c in cand if c[1] > 0]
        if cand: best[cik] = max(cand)[2]
    comp["ticker"] = comp.cik.map(best)
    foreign = {}
    for cik in comp.cik:
        f = HERE / "cache/submissions" / f"CIK{int(cik):010d}.json"
        if f.exists():
            forms = set(json.load(open(f))["filings"]["recent"]["form"])
            foreign[cik] = bool(forms & {"20-F", "40-F", "20-F/A", "6-K"})
    comp["foreign"] = comp.cik.map(foreign).fillna(False)
    comp.to_csv(HERE / "data/sponsor_companies_priced.csv", index=False)
    comp[comp.ticker.isna()][["cik", "sec_name", "name_now", "tickers", "n_trials"]].to_csv(HERE / "data/excluded_no_price.csv", index=False)
    print(len(comp), "companies;", comp.ticker.notna().sum(), "with Yahoo prices;", int(comp.foreign.sum()), "foreign issuers")


if __name__ == "__main__":
    main()

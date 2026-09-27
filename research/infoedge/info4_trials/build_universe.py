"""Step 1f: choose the sponsor companies and trials whose histories are pulled.

Keeps a mapped CIK when
  - it filed a 10-K/10-Q/20-F/40-F in 2014-2026 (EDGAR form indices), and
  - a "core" (loose) or one-dictionary-word match is kept only if the SIC code is health care.
Writes data/sponsor_companies.csv and data/sponsor_map_kept.csv. The size screen (under $5B
at some point since 2015) and the trial list are made by size_screen.py once prices and
share counts are in.
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
HC_SIC = set(range(2833, 2837)) | set(range(3841, 3846)) | {3826, 3829, 3851, 5047, 5122, 8731, 8733, 8734, 8071} | set(range(8000, 8100))


def main():
    m = pd.read_csv(HERE / "data/sponsor_map.csv")
    info = pd.read_csv(HERE / "cache/sponsor_cik_info.csv")
    hist = pd.read_csv(HERE / "cache/sec_names_hist.csv")
    periodic = set(hist.cik)
    m = m.merge(info[["cik", "sic", "sic_desc", "tickers", "exchanges", "category", "name_now"]], on="cik", how="left")
    m["hc"] = m.sic.fillna(0).astype(int).isin(HC_SIC)
    m["periodic"] = m.cik.isin(periodic)
    keep = m[m.periodic & ((m.match == "exact") | m.hc)].copy()   # core and exact_word need health-care SIC
    fl = pd.read_csv(HERE / "cache/float.csv", names=["cik", "filed", "end", "val", "unit"])
    fl = fl[(fl.unit == "USD") & (fl.filed >= "2014-06-01") & (fl.val > 0)]
    keep["min_float"] = keep.cik.map(fl.groupby("cik").val.min())
    comp = keep.groupby("cik").agg(name_now=("name_now", "first"), sec_name=("sec_name", "first"),
                                   tickers=("tickers", "first"), exchanges=("exchanges", "first"),
                                   sic=("sic", "first"), hc=("hc", "first"), min_float=("min_float", "first"),
                                   n_names=("lead_sponsor", "size"), n_trials=("n_trials", "sum")).reset_index()
    comp.to_csv(HERE / "data/sponsor_companies.csv", index=False)
    keep[["lead_sponsor", "cik", "match", "sec_name", "sic", "hc", "name_first_seen"]].to_csv(HERE / "data/sponsor_map_kept.csv", index=False)
    print(len(comp), "companies kept by the mapping filters;", "health-care SIC share", round(comp.hc.mean(), 2))


if __name__ == "__main__":
    main()

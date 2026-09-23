#!/usr/bin/env python3
"""Free price data for the Cal-Maine nowcast -> data/prices_monthly.csv

Downloads (cached in cache/prices/):
  USDA ERS "Wholesale prices" workbook (Livestock and Meat Domestic Data), monthly, 2000 on:
      Eggs, Grade A large, Combined regional (USDA AMS report 2848 basis) and New York, cents/dozen.
      https://www.ers.usda.gov/media/5538/wholesale-prices.xlsx  (sheet Historical + sheet Current;
      the newest month in 'Current' is flagged by ERS as a current-month estimate)
  FRED (BLS):  WPU017107  PPI Eggs for fresh use;  WPU01710703  PPI Eggs, large;  WPU0171 PPI Chicken eggs;
               APU0000708111  CPI average retail price, Grade A large eggs, $/dozen.
  Feed:  USDA ERS "Broiler, turkey and egg feed costs" (corn No.2 yellow Chicago $/bu, soybean meal
         Decatur $/ton, monthly, 2000 - Feb 2026; ERS stopped updating it in April 2026),
         FRED IMF PMAIZMTUSDM (corn, US Gulf $/mt) and PSMEAUSDM (soybean meal $/mt) to extend it,
         Yahoo Finance ZC=F daily CBOT corn front-month (cents/bu) for the latest months.
"""
import io, json, time
from pathlib import Path
import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "cache" / "prices"
C.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (research; dspinjr@gmail.com)"}


def fetch(url, dest, refresh=False):
    dest = C / dest
    if dest.exists() and not refresh:
        return dest
    r = requests.get(url, headers=UA, timeout=90)
    r.raise_for_status()
    dest.write_bytes(r.content)
    time.sleep(0.5)
    return dest


def fred(sid):
    p = fetch(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", f"fred_{sid}.csv")
    d = pd.read_csv(p)
    d.columns = ["date", sid]
    d["date"] = pd.to_datetime(d.date)
    d[sid] = pd.to_numeric(d[sid], errors="coerce")
    return d.set_index("date")[sid]


def ers_eggs():
    p = fetch("https://www.ers.usda.gov/media/5538/wholesale-prices.xlsx?v=70883", "ers_wholesale-prices.xlsx")
    h = pd.read_excel(p, sheet_name="Historical", header=None)
    # columns 27/28 = Eggs Grade A large: Combined regional, New York (cents/doz); verified by header rows
    assert "Eggs" in str(h.iloc[0, 27]) and "Combined" in str(h.iloc[1, 27]) and "New York" in str(h.iloc[1, 28])
    d = h.iloc[4:, [0, 27, 28]].copy()
    d.columns = ["date", "ers_combined", "ers_ny"]
    d = d[pd.to_datetime(d.date, errors="coerce").notna()]
    d["date"] = pd.to_datetime(d.date)
    d = d.set_index("date").astype(float) / 100.0  # $/dozen
    d["ers_estimate"] = 0
    cur = pd.read_excel(p, sheet_name="Current", header=None)
    hdr = cur.iloc[0, 1:].tolist()
    rowc = cur.index[cur[0].astype(str).str.strip() == "Combined regional"][0]
    rown = cur.index[cur[0].astype(str).str.strip() == "New York"][0]
    for j, hname in enumerate(hdr, start=1):
        if isinstance(hname, str) and "/*" in hname:  # e.g. 'Aug-26/*' = current-month estimate
            dt = pd.to_datetime(hname.replace("/*", ""), format="%b-%y")
            d.loc[dt, ["ers_combined", "ers_ny"]] = [cur.iloc[rowc, j] / 100.0, cur.iloc[rown, j] / 100.0]
            d.loc[dt, "ers_estimate"] = 1
    return d.sort_index()


def ers_feed():
    p = fetch("https://www.ers.usda.gov/media/20291/broiler-turkey-and-egg-feed-costs.xlsx?v=75973",
              "ers_broiler-turkey-and-egg-feed-costs.xlsx")
    e = pd.read_excel(p, sheet_name="Eggs", header=None).iloc[5:, :3]
    e.columns = ["date", "sbm_ton", "corn_bu"]
    e = e[pd.to_datetime(e.date, errors="coerce").notna()]
    e["date"] = pd.to_datetime(e.date)
    return e.set_index("date").astype(float)


def yahoo_corn():
    p = C / "yf_zc.json"
    if not p.exists():
        fetch("https://query1.finance.yahoo.com/v8/finance/chart/ZC=F?range=15y&interval=1d", "yf_zc.json")
    j = json.load(open(p))["chart"]["result"][0]
    s = pd.Series(j["indicators"]["quote"][0]["close"], index=pd.to_datetime(j["timestamp"], unit="s")).dropna()
    return (s / 100.0).resample("MS").mean().rename("cbot_corn_yf")


def main():
    eg = ers_eggs()
    ppi_fresh = fred("WPU017107")
    ppi_large = fred("WPU01710703")
    ppi_eggs = fred("WPU0171")
    retail = fred("APU0000708111")
    feed = ers_feed()
    imf_corn = fred("PMAIZMTUSDM")
    imf_sbm = fred("PSMEAUSDM")
    yc = yahoo_corn()
    M = pd.concat([eg, ppi_fresh.rename("ppi_fresh"), ppi_large.rename("ppi_large"), ppi_eggs.rename("ppi_eggs"),
                   retail.rename("retail_large"), feed, imf_corn.rename("imf_corn_mt"), imf_sbm.rename("imf_sbm_mt"),
                   yc], axis=1)
    M = M[M.index >= "2012-01-01"]
    # Extend ERS corn/SBM after Feb 2026: corn from CBOT front-month (Yahoo), SBM from IMF scaled to Decatur level
    ov = M.dropna(subset=["sbm_ton", "imf_sbm_mt"])
    ov = ov[ov.index >= "2022-01-01"]
    k_sbm = (ov.sbm_ton / ov.imf_sbm_mt).median()
    ov2 = M.dropna(subset=["corn_bu", "cbot_corn_yf"])
    ov2 = ov2[ov2.index >= "2022-01-01"]
    k_corn = (ov2.corn_bu / ov2.cbot_corn_yf).median()
    M["corn"] = M.corn_bu.fillna(M.cbot_corn_yf * k_corn)
    M["sbm"] = M.sbm_ton.fillna(M.imf_sbm_mt * k_sbm)
    M["feed_note"] = np.where(M.corn_bu.notna(), "ERS", "extended: corn=CBOT(Yahoo)x%.3f, sbm=IMFx%.3f" % (k_corn, k_sbm))
    M.index.name = "month"
    M.to_csv(ROOT / "data" / "prices_monthly.csv", float_format="%.4f")
    print(M.tail(10)[["ers_combined", "ers_ny", "ers_estimate", "ppi_fresh", "ppi_large", "retail_large", "corn", "sbm"]])
    print("k_sbm", k_sbm, "k_corn", k_corn)


if __name__ == "__main__":
    main()

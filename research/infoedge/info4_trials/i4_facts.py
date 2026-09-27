"""Step 1e: XBRL company facts for candidate sponsors -> share counts and public float over time.

One request every 0.55 s (SEC cap for this test: 2 a second). Raw JSON is not kept (it is
large); the extracted series go to cache/shares.csv (cik, filed, end, shares, source) and
cache/float.csv (cik, filed, end, float_usd).
"""
import csv, json, sys, time
from pathlib import Path
import pandas as pd, requests

HERE = Path(__file__).resolve().parent
UA = "Claude Space research dspinjr@gmail.com"
DONE = HERE / "cache" / "facts_done.txt"


def main(ciks):
    s = requests.Session(); s.headers["User-Agent"] = UA
    done = set(DONE.read_text().split()) if DONE.exists() else set()
    sh = open(HERE / "cache" / "shares.csv", "a", newline=""); fl = open(HERE / "cache" / "float.csv", "a", newline="")
    wsh, wfl = csv.writer(sh), csv.writer(fl)
    dn = open(DONE, "a")
    for i, cik in enumerate(ciks):
        if str(cik) in done: continue
        for attempt in range(5):
            time.sleep(0.55)
            try:
                r = s.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json", timeout=90)
            except requests.RequestException:
                time.sleep(10); continue
            if r.status_code in (200, 404): break
            time.sleep(10 * (attempt + 1))
        if r.status_code == 200:
            facts = r.json().get("facts", {})
            dei = facts.get("dei", {}); gaap = facts.get("us-gaap", {}); ifrs = facts.get("ifrs-full", {})
            for src, block, key in [("dei", dei, "EntityCommonStockSharesOutstanding"),
                                    ("gaap_out", gaap, "CommonStockSharesOutstanding"),
                                    ("gaap_wab", gaap, "WeightedAverageNumberOfSharesOutstandingBasic"),
                                    ("ifrs_wab", ifrs, "WeightedAverageShares")]:
                for unit, obs in block.get(key, {}).get("units", {}).items():
                    for o in obs:
                        if o.get("filed") and o.get("val") is not None:
                            wsh.writerow([cik, o["filed"], o.get("end"), o["val"], src])
            for unit, obs in dei.get("EntityPublicFloat", {}).get("units", {}).items():
                for o in obs:
                    if o.get("filed") and o.get("val") is not None:
                        wfl.writerow([cik, o["filed"], o.get("end"), o["val"], unit])
        dn.write(f"{cik}\n"); dn.flush(); sh.flush(); fl.flush()
        if i % 100 == 0: print(i, len(ciks), flush=True)


if __name__ == "__main__":
    main(pd.read_csv(sys.argv[1]).cik.astype(int).tolist())

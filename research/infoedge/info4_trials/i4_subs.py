"""Step 1d: EDGAR submissions JSON for every candidate sponsor CIK (SIC code, exchange, tickers).
One request every 0.55 s (SEC cap for this test: 2 a second). Raw -> cache/submissions/."""
import json, time
from pathlib import Path
import pandas as pd, requests

HERE = Path(__file__).resolve().parent
OUT = HERE / "cache" / "submissions"; OUT.mkdir(parents=True, exist_ok=True)
UA = "Claude Space research dspinjr@gmail.com"

def fetch(s, cik):
    f = OUT / f"CIK{cik:010d}.json"
    if f.exists(): return json.loads(f.read_text())
    for attempt in range(5):
        time.sleep(0.55)
        r = s.get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", timeout=60)
        if r.status_code == 200:
            f.write_text(r.text); return r.json()
        if r.status_code == 404: return None
        time.sleep(5 * (attempt + 1))
    return None

def main():
    s = requests.Session(); s.headers["User-Agent"] = UA
    m = pd.read_csv(HERE / "data/sponsor_map.csv")
    rows = []
    for i, cik in enumerate(sorted(m.cik.unique())):
        j = fetch(s, int(cik))
        if j is None: rows.append({"cik": cik}); continue
        rows.append({"cik": cik, "sic": j.get("sic"), "sic_desc": j.get("sicDescription"),
                     "tickers": "|".join(j.get("tickers") or []), "exchanges": "|".join(x or "" for x in (j.get("exchanges") or [])),
                     "entity_type": j.get("entityType"), "category": j.get("category"),
                     "state_inc": j.get("stateOfIncorporation"), "name_now": j.get("name"),
                     "former": "|".join(f["name"] for f in j.get("formerNames") or [])})
        if i % 100 == 0: print(i, flush=True)
    pd.DataFrame(rows).to_csv(HERE / "cache" / "sponsor_cik_info.csv", index=False)

if __name__ == "__main__":
    main()

"""Step 1c: EDGAR quarterly form indices 2014Q1-2026Q3 -> historical registrant names and 8-K dates.

Downloads full-index/{year}/QTR{q}/form.gz (one request every 0.6 s, SEC cap is 2 a second
for this test). Writes:
  cache/sec_names_hist.csv  every name used by a 10-K/10-Q/20-F/40-F filer (cik, name, first, last)
  cache/edgar_8k_dates.csv  every 8-K / 8-K/A, and 6-K / 6-K/A for foreign issuers (cik, date, form)
"""
import csv, gzip, re, time
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
IDX = HERE / "cache" / "edgar_index"; IDX.mkdir(parents=True, exist_ok=True)
UA = "Claude Space research dspinjr@gmail.com"
PERIODIC = {"10-K", "10-Q", "10-K/A", "10-Q/A", "10-KT", "20-F", "40-F", "10-K405"}

def main():
    s = requests.Session(); s.headers["User-Agent"] = UA
    names, eightk = {}, set()
    for y in range(2014, 2027):
        for q in range(1, 5):
            if (y, q) > (2026, 3): break
            f = IDX / f"form_{y}Q{q}.gz"
            if not f.exists():
                for attempt in range(5):
                    time.sleep(0.6)
                    r = s.get(f"https://www.sec.gov/Archives/edgar/full-index/{y}/QTR{q}/form.gz", timeout=120)
                    if r.status_code == 200: break
                    time.sleep(5 * (attempt + 1))
                r.raise_for_status(); f.write_bytes(r.content)
            text = gzip.decompress(f.read_bytes()).decode("latin-1")
            lines = text.splitlines()
            start = next(i for i, l in enumerate(lines) if l.startswith("---")) + 1
            for l in lines[start:]:
                # "<form>  <company>  <cik>  <date>  <file>"; forms never contain double spaces
                m = re.match(r"^(\S+(?: \S+)*)\s{2,}(.*?)\s+(\d+)\s+(\d{4}-\d{2}-\d{2})\s+(\S+)\s*$", l)
                if not m: continue
                form, comp, cik, date = m.group(1), m.group(2).strip(), m.group(3), m.group(4)
                if form in PERIODIC:
                    k = (int(cik), comp)
                    a, b = names.get(k, (date, date)); names[k] = (min(a, date), max(b, date))
                elif form in ("8-K", "8-K/A", "6-K", "6-K/A"):
                    eightk.add((int(cik), date, form.split("/")[0]))
            print(y, q, len(names), len(eightk), flush=True)
    with open(HERE / "cache" / "sec_names_hist.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["cik", "name", "first", "last"])
        for (c, n), (a, b) in sorted(names.items()): w.writerow([c, n, a, b])
    with open(HERE / "cache" / "edgar_8k_dates.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["cik", "date", "form"])
        for c, d, f in sorted(eightk): w.writerow([c, d, f])

if __name__ == "__main__":
    main()

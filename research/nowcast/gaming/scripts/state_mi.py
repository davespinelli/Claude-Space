"""Michigan (Detroit commercial casinos) monthly revenue by casino -> data/state_mi.csv.gz

Source: Michigan Gaming Control Board (MGCB), "Revenues and Wagering Tax Information"
  https://www.michigan.gov/mgcb/detroit-casinos/resources/revenues-and-wagering-tax-information
  Files used (Excel; the PDFs on the same page are print versions of the same tables):
    Detroit_Casino_Revenue_1999-2017_645375_7.xlsx   sheets Combined-1999 .. Combined-2018
    Detroit_Casino_Revenue_Jan_2019_646139_7.xls      Combined-2019 (+2018)
    Detroit_casino_revenues_January_2020__681064_7.xls Combined-2020 (+2019)
    Detroit_Casino_revenue_Jan_2021_715841_7-(2).xls  Combined - 2021 (+2020)
    Detroit-casino-revenue---Jan-2022.xls              Combined - 2022 (+2021)
    Detroit-Casino---January-2023.xls                  Combined - 2023 (+2022)
    Detroit_Casino_Revenue-2024/2025/2026-XLS.xls      Combined - 2024/2025/2026 (+prior year)
  The .xls files for 2019-2025 are "write-protected" BIFF files encrypted with Excel's default
  password (VelvetSweatshop); they are decrypted in memory with msoffcrypto-tool. For each calendar
  year the sheet from the NEWEST file containing it is used (prior-year sheets carry revisions).
  Retail sports betting (RSB), iGaming, online sports and fantasy are in separate files -> NOT used.

Measure: "Total Adjusted Revenue" per casino = Michigan adjusted gross receipts (AGR) from table
  games and slots (the monthly press release, e.g. Aug 2026, reports "Table games and slots generated
  $108.86 million" = the file's All Detroit Casinos total 108,862,040.62; MGM $52.90M = file). Only
  the total is published monthly -> slots/tables blank. measure = "AGR". Dollars (not thousands).
Units (unit_level = property), names as published (the file has never renamed them):
  MI_MGM_GRAND_DETROIT  "MGM GRAND DETROIT"
  MI_MOTORCITY          "MOTORCITY CASINO"
  MI_GREEKTOWN          "GREEKTOWN CASINO" (branded Greektown Casino-Hotel -> Hollywood Casino at
                        Greektown since 2023 under PENN, owner VICI; the file keeps the old name)
  __STATE_TOTAL__ = "All Detroit Casinos / Total Adjusted Gross Receipts" (unit_id MI_STATE_TOTAL).
Month range: 2012-01 .. latest in the 2026 file (2026-08 as of 2026-09-23).
COVID: casinos closed 2020-03-16 .. 2020-08-05 -> Apr-Jul 2020 are 0 as published.
Publication dates: MGCB monthly press release "Detroit casinos report $X in <Month> revenue",
  collected from the michigan.gov news search API (/mgcb/sxa/search/results/). The index only reaches
  back to Aug 2021, so pub_date is filled for 2021-07 onward (pub_source = press_release); earlier
  months are blank (old michigan.gov press-release archive was not retrievable). Typical lag: 8-15
  days after month end (e.g. Aug 2026 -> 2026-09-11; Jul 2026 -> 2026-08-11).
Spot checks: sum of 3 casinos vs "All Detroit Casinos" every month 2012-01..latest -> see
  data/state_mi_checks.csv.gz. Run 2026-09-23: 176 months 2012-01..2026-08, max |diff| 0.0000%
  (Apr-Jul 2020 are 0 = 0). Cross-check with press release Aug 2026: table games + slots $108.86M,
  MGM $52.90M, MotorCity $33.77M, Greektown $22.19M -> identical to the file.
  Jump scan (m/m > 3x or < 1/3 outside Mar-Aug 2020): only Jan 2021 (x3.6-4.5), a real rebound from
  the second state-ordered closure 2020-11-18 .. 2020-12-23 (Nov/Dec 2020 are partial months).
  Rows: 704 = 3 casinos + state total x 176 months. Pub dates: 62 months (2021-07..2026-08),
  lag 7-27 days, median 11.5.
"""
from __future__ import annotations

import io
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "mi"
DATA = ROOT / "data"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
LISTING = ("https://www.michigan.gov/mgcb/detroit-casinos/resources/"
           "revenues-and-wagering-tax-information")
SEARCH = "https://www.michigan.gov/mgcb/sxa/search/results/"
SEARCH_PARAMS = {"s": "{F71378C3-4227-43FD-A440-6F7DAE499886}",
                 "itemid": "{031D0012-1E35-4713-8018-79111AA2F635}",
                 "v": "{B7A22BE8-17FC-44A5-83BC-F54442A57941}",
                 "p": 100, "o": "Article Date,Descending"}
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
UNIT_IDS = {"MGM GRAND DETROIT": "MI_MGM_GRAND_DETROIT", "MOTORCITY CASINO": "MI_MOTORCITY",
            "GREEKTOWN CASINO": "MI_GREEKTOWN"}
_last = [0.0]


def get(url, **kw):
    for attempt in range(4):
        w = 0.6 - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=60, **kw)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            print(f"  retry {attempt + 1} {url}: {e}", file=sys.stderr)
            time.sleep(2 ** attempt * 2)
    raise RuntimeError(url)


def fetch(url: str, dest: Path, refresh=False) -> Path:
    if dest.exists() and dest.stat().st_size > 0 and not refresh:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(get(url).content)
    return dest


def norm(s) -> str:
    return re.sub(r"\s+", " ", str(s)).strip()


def download(refresh: bool) -> list[Path]:
    html = fetch(LISTING, CACHE / "_listing_revenues.html", refresh).read_text(errors="ignore")
    out = []
    for h in sorted(set(re.findall(r'href="([^"]+)"', html))):
        h = h.replace("&amp;", "&")
        if "Detroit-Casino-Revenue" not in h or re.search(r"fantasy|internet|rsb|igaming", h, re.I):
            continue
        fn = Path(h.split("?")[0]).name
        if not re.search(r"\.(xls|xlsx)$", fn, re.I):
            continue
        out.append(fetch("https://www.michigan.gov" + h, CACHE / fn))
    return out


def read_sheets(path: Path) -> dict[str, list[list]]:
    """return {sheet_name: rows} for xls (possibly default-password encrypted) or xlsx."""
    if path.suffix.lower() == ".xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True)
        return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}
    import xlrd
    data = path.read_bytes()
    try:
        wb = xlrd.open_workbook(file_contents=data)
    except xlrd.biffh.XLRDError:
        import msoffcrypto
        buf = io.BytesIO()
        of = msoffcrypto.OfficeFile(io.BytesIO(data))
        of.load_key(password="VelvetSweatshop")
        of.decrypt(buf)
        wb = xlrd.open_workbook(file_contents=buf.getvalue())
    return {sh.name: [sh.row_values(i) for i in range(sh.nrows)] for sh in wb.sheets()}


def parse_sheet(rows: list[list]) -> tuple[int, list[dict]]:
    year = None
    for r in rows[:3]:
        for v in r:
            m = re.search(r"Calendar Year\s*(\d{4})", str(v or ""))
            if m:
                year = int(m.group(1))
    # name row and header row
    name_row = next(i for i, r in enumerate(rows) if any(norm(v or "") == "MGM GRAND DETROIT" for v in r))
    hdr = rows[name_row + 1]
    cols = {}
    for c, v in enumerate(rows[name_row]):
        nm = norm(v or "")
        if nm in UNIT_IDS or nm == "All Detroit Casinos":
            # first "Total Adjusted ..." column at or after c
            cc = next(j for j in range(c, len(hdr)) if norm(hdr[j] or "").startswith("Total Adjusted"))
            cols[nm] = cc
    out = []
    for r in rows[name_row + 2:]:
        lab = norm(r[0] or "")
        m = re.match(r"(" + "|".join(MONTHS) + r")", lab, re.I)
        if not m:
            continue
        mo = MONTHS.index(m.group(1).lower()) + 1
        vals = {nm: r[c] for nm, c in cols.items()}
        if all(v in ("", None) for v in vals.values()):
            continue  # month not yet reported
        for nm, v in vals.items():
            out.append(dict(name=nm, month=f"{year}-{mo:02d}", ggr=float(v or 0)))
    return year, out


def press_release_dates(refresh: bool) -> dict[str, str]:
    cache = CACHE / "_news_search.json"
    if cache.exists() and not refresh:
        res = json.loads(cache.read_text())
    else:
        res, e = [], 0
        while True:
            j = get(SEARCH, params={**SEARCH_PARAMS, "e": e}).json()
            res += j["Results"]
            if not j["Results"] or e + 100 >= j["Count"]:
                break
            e += 100
        cache.write_text(json.dumps(res))
    out = {}
    for x in res:
        t = re.search(r'content-title-link"[^>]*>\s*(.*?)\s*</a>', x["Html"], re.S)
        title = norm(t.group(1)) if t else ""
        url = x["Url"]
        if not re.search(r"detroit casino", title, re.I) or not re.search(r"revenue", title, re.I):
            continue
        if re.search(r"igaming|online|sports betting|fantasy|tribal", title, re.I):
            continue
        y, m, d = map(int, re.search(r"/news/(\d{4})/(\d{2})/(\d{2})/", url).groups())
        dm_y, dm_m = (y, m - 1) if m > 1 else (y - 1, 12)
        key = f"{dm_y}-{dm_m:02d}"
        pub = f"{y}-{m:02d}-{d:02d}"
        if key not in out or pub < out[key]:
            out[key] = pub
    return out


def main(refresh=False):
    files = download(refresh)
    # file order: newest primary year last
    def primary_year(p: Path) -> int:
        ys = [int(y) for y in re.findall(r"(?:19|20)\d\d", p.name)]
        return max(ys)
    by_year: dict[int, tuple[int, Path, list]] = {}
    for p in sorted(files, key=primary_year):
        for sn, rows in read_sheets(p).items():
            if not re.search(r"combined", sn, re.I):
                continue
            year, recs = parse_sheet(rows)
            if year < 2012 or not recs:
                continue
            by_year[year] = (primary_year(p), p, recs)  # later files overwrite earlier
    pubs = press_release_dates(refresh)
    rows = []
    for year, (_, p, recs) in sorted(by_year.items()):
        print(f"  {year}: {len(recs)} values from {p.name}")
        for r in recs:
            st = r["name"] == "All Detroit Casinos"
            pd_ = pubs.get(r["month"], "")
            rows.append(dict(state="MI", unit="__STATE_TOTAL__" if st else r["name"],
                             unit_id="MI_STATE_TOTAL" if st else UNIT_IDS[r["name"]],
                             unit_level="state_total" if st else "property", month=r["month"],
                             ggr=r["ggr"], slots=None, tables=None, n_casinos=None, measure="AGR",
                             pub_date=pd_, pub_source="press_release" if pd_ else "",
                             source_file=p.name))
    out = pd.DataFrame(rows).sort_values(["month", "unit_level", "unit_id"])
    assert not out.duplicated(["unit_id", "month"]).any()
    DATA.mkdir(exist_ok=True)
    out.to_csv(DATA / "state_mi.csv.gz", index=False)

    u = out[out.unit_level == "property"].groupby("month").ggr.sum()
    t = out[out.unit_level == "state_total"].set_index("month").ggr
    chk = pd.DataFrame({"sum_of_units": u, "regulator_total": t})
    chk["diff_pct"] = (chk.sum_of_units - chk.regulator_total) / chk.regulator_total.where(chk.regulator_total != 0) * 100
    chk["note"] = "3 Detroit casinos vs All Detroit Casinos (AGR, table games + slots)"
    chk.index.name = "month"
    chk.reset_index().to_csv(DATA / "state_mi_checks.csv.gz", index=False)

    jumps = []
    for uid, g in out[out.unit_level == "property"].groupby("unit_id"):
        v = g.set_index("month").ggr
        rat = v / v.shift(1)
        for m, x in rat.items():
            if pd.notna(x) and (x > 3 or x < 1 / 3) and not ("2020-03" <= m <= "2020-08"):
                jumps.append((uid, m, round(x, 2)))
    print(f"rows={len(out)} months {out.month.min()}..{out.month.max()} "
          f"max|diff%|={chk.diff_pct.abs().max():.4f} jumps={jumps}")
    print("pub dates filled:", (out.pub_date != "").sum() // 4, "months; lag days:",
          (pd.to_datetime(out[out.pub_date != ""].pub_date)
           - (pd.to_datetime(out[out.pub_date != ""].month) + pd.offsets.MonthEnd(0))).dt.days.describe()[["min", "50%", "max"]].to_dict())


if __name__ == "__main__":
    main("--refresh" in sys.argv)

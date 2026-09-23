"""Colorado: monthly casino adjusted gross proceeds (AGP) by gaming town, 2012-01 .. latest.

Run:  python3 scripts/state_co.py [--refresh]
      (--refresh re-reads the statistics page and the calendar-year detail workbook to pick up new months;
      workbooks/PDFs already in cache/co/ are never re-downloaded.)
Output: data/state_co.csv.gz, data/state_co_checks.csv.gz. Raw files: cache/co/{fy,monthly}/.

SOURCES (Colorado Division of Gaming, https://sbg.colorado.gov/industry-statistics-gaming)
  A default curl User-Agent gets HTTP 403; a browser User-Agent + Accept headers works.
  * Previous fiscal years: one workbook per FY, "TaxYY-YY.xls(x)" (FY2012-FY2024 hosted on sbg.colorado.gov;
    FY2025 is a Google Drive/Sheets link, fetched with the /export?format=xlsx URL). Rows = (town, item),
    columns JULY..JUNE; FY YYYY = Jul YYYY-1 .. Jun YYYY.
  * Current fiscal year: "Colorado Gaming Statistics, <Month YYYY>" per month, .xls (Google Drive links; one
    on sbg) and .pdf (2025-07 .. 2026-07). Columns Statewide / Black Hawk / Central City / Cripple Creek.
  * "Monthly Detail by Calendar Year" workbook (casinos, devices, AGP by town since 1991-10; Google link):
    used only as an independent cross-check.
  The Division is barred by law from releasing casino-level figures, so towns are the finest geography.

UNITS: Black Hawk, Central City, Cripple Creek (unit_level = town; unit_id CO_<TOWN>); __STATE_TOTAL__ = the
  "Statewide" column. No renames.
MEASURE: AGP (all wagers less payouts). slots = "Slots Total" block AGP; tables = Total AGP - slot AGP
  (table games incl. house-banked and player-banked poker; from 2021-05, after Amendment 77, also keno and
  "other casino games", < 0.05% of AGP). Sports betting is reported separately by the Division and is
  not in AGP (excluded). Values in dollars.
n_casinos: "# of Casinos" row (per town, per month).
n_slot_units / n_table_units (added at the end of the row, after source_file): device counts published in
  the same workbooks, split for every town-month (so the calendar-year workbook's combined "Devices" figure
  is only used as a check). n_slot_units = "Slots Total" (slot machines). n_table_units = "Total Devices" -
  "Slots Total" = "Table Games" count (all tables incl. house-banked and player-banked poker) plus, from
  2021-05 (Amendment 77), keno and "other casino games" devices (2-9 statewide), matching the tables AGP
  column. Apr-May 2020 counts are as the source shows them during the closure.
MONTHS: 2012-01 .. 2026-07 (175 months, no gaps). COVID: casinos closed 2020-03-17 .. 2020-06-14; April and
  May 2020 AGP is 0 in the source and kept as 0 (n_casinos still shows licensed casinos).
PUBLICATION DATE: PDF CreationDate of the monthly statistics PDF (pub_source = pdf_metadata), available only
  for 2025-07 onward (13 months; lag after month-end 16-26 days, median 19; the page says statistics are
  posted "on or about the 20th"). Blank for earlier months: only fiscal-year workbooks remain online.

SPOT CHECKS (data/state_co_checks.csv.gz, all 175 months):
  * Black Hawk + Central City + Cripple Creek = Statewide AGP exactly (max |diff| 2e-14%).
  * Independent cross-check against the "Monthly Detail by Calendar Year" workbook, 2012-01..2025-07:
    644 unit-months, max |AGP diff| $1; n_casinos differs in 5 unit-months (2012-06, 2018-11, 2019-04,
    +/-1 casino).
  * n_slot_units + n_table_units = "Devices" in the independent calendar-year workbook in 628 of 644
    unit-months; the 16 exceptions (2014-12, 2016-02, 2017-02, 2021-06, 2021-07, 2023-01) look like errors in
    that workbook (e.g. 2014-12 and 2021-06 it shows slots only). Source quirk kept as published: Central City
    2023-01 shows 2,100 slots and 8 casinos in the FY workbook (neighbouring months ~1,710 and 6).
  * slots + tables = AGP by construction; the published Table Games AGP differs from (AGP - slots) only
    after 2021-05, by < $31k/month statewide.
  * no month/month jump > 3x or < 1/3 outside the 2020 closure.
"""
import re
import sys
import time
import html as htmlmod
import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "co"
DATA = ROOT / "data"
SBG = "https://sbg.colorado.gov"
STATS_PAGE = SBG + "/industry-statistics-gaming"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.9"})
_last = [0.0]
REFRESH = "--refresh" in sys.argv          # re-read listing page (new months); raw data files are never re-fetched
FIRST = "2012-01"
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
TOWNS = {"black hawk": ("Black Hawk", "CO_BLACK_HAWK"),
         "central city": ("Central City", "CO_CENTRAL_CITY"),
         "cripple creek": ("Cripple Creek", "CO_CRIPPLE_CREEK")}


def fetch(url, dest, force=False):
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(5):
        wait = 0.6 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = SESSION.get(url, timeout=60, allow_redirects=True)
            if r.status_code == 200 and r.content:
                dest.write_bytes(r.content)
                return dest
            print(f"  HTTP {r.status_code} {url}", file=sys.stderr)
        except requests.RequestException as e:
            print(f"  error {e} {url}", file=sys.stderr)
        time.sleep(2 ** attempt)
    raise RuntimeError(f"failed to download {url}")


def gdrive_export(url):
    """Google Drive/Sheets share link -> direct xlsx export link."""
    m = re.search(r"/d/([A-Za-z0-9_-]{20,})", url)
    return f"https://docs.google.com/spreadsheets/d/{m.group(1)}/export?format=xlsx" if m else url


def absolute(href):
    href = htmlmod.unescape(href)
    return SBG + href if href.startswith("/") else href


def parse_listing():
    page = CACHE / "listing_industry_statistics.html"
    html = fetch(STATS_PAGE, page, force=REFRESH or not page.exists()).read_text(encoding="utf-8", errors="ignore")
    monthly, fy = {}, {}
    # monthly rows: "July 2025 | .pdf | .xls"
    for tr in re.findall(r"<tr.*?</tr>", html, flags=re.S):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, flags=re.S)
        if not cells:
            continue
        label = " ".join(htmlmod.unescape(re.sub("<[^>]+>", " ", cells[0])).split()).lower()
        m = re.fullmatch(r"([a-z]+) (20\d\d)", label)
        if not m or m.group(1) not in MONTHS:
            continue
        mo = f"{m.group(2)}-{MONTHS.index(m.group(1)) + 1:02d}"
        links = [absolute(h) for h in re.findall(r'href="([^"]+)"', tr)]
        pdf = [u for u in links if u.lower().endswith(".pdf")]
        xls = [u for u in links if not u.lower().endswith(".pdf")]
        monthly[mo] = {"pdf": pdf[0] if pdf else None, "xls": xls[0] if xls else None}
    # previous fiscal-year workbooks: text between "Previous Fiscal Years" and "Statistical Summaries"
    i = html.find("Previous Fiscal Years")
    j = html.find("Statistical Summaries", i)
    for href, inner in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html[i:j], flags=re.S):
        txt = re.sub("<[^>]+>", "", inner).strip()
        if re.fullmatch(r"20\d\d", txt):
            fy[int(txt)] = absolute(href)
    # calendar-year monthly detail workbook (casinos, devices, AGP by town since 1991)
    m = re.search(r"Monthly Detail by Calendar Year.*?href=\"([^\"]+)\"", html, flags=re.S)
    cy = absolute(m.group(1)) if m else None
    return monthly, fy, cy


def download_all():
    monthly, fy, cy = parse_listing()
    files = {"fy": {}, "monthly_xls": {}, "monthly_pdf": {}}
    for year, u in sorted(fy.items()):
        if year < 2012:
            continue
        ext = ".xls" if u.lower().endswith(".xls") else ".xlsx"
        files["fy"][year] = fetch(gdrive_export(u) if "google" in u else u, CACHE / "fy" / f"Tax_FY{year}{ext}")
    for mo, d in sorted(monthly.items()):
        if d["xls"]:
            files["monthly_xls"][mo] = fetch(gdrive_export(d["xls"]) if "google" in d["xls"] else d["xls"],
                                             CACHE / "monthly" / f"stats_{mo}.xlsx")
        if d["pdf"]:
            files["monthly_pdf"][mo] = fetch(d["pdf"], CACHE / "monthly" / f"stats_{mo}.pdf")
    if cy:
        files["cy"] = fetch(gdrive_export(cy), CACHE / "monthly_detail_by_calendar_year.xlsx",
                            force=REFRESH)
    return files


FY_MONTHS = ["JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER",
             "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE"]


def _num(x):
    try:
        v = float(x)
        return 0.0 if np.isnan(v) else v
    except (TypeError, ValueError):
        return np.nan


def parse_fy(path, fy_year):
    """Fiscal-year workbook TaxYY-YY: rows = (town, label), columns JULY..JUNE. Returns long records."""
    v = pd.read_excel(path, header=None)
    hdr = next(i for i in range(10) if "JULY" in [str(c).strip().upper() for c in v.iloc[i]])
    cols = {}
    for j, c in enumerate(v.iloc[hdr]):
        c = str(c).strip().upper()
        if c in FY_MONTHS:
            k = FY_MONTHS.index(c)
            year = fy_year - 1 if k < 6 else fy_year        # FY2013 = Jul 2012 .. Jun 2013
            cols[j] = f"{year}-{(k + 6) % 12 + 1:02d}"
    recs = {}
    cur_block = {}
    for i in range(hdr + 1, len(v)):
        town = str(v.iat[i, 0]).strip() if pd.notna(v.iat[i, 0]) else None
        label = str(v.iat[i, 1]).strip() if pd.notna(v.iat[i, 1]) else None
        if not town or not label:
            continue
        key = town.lower()
        if label in ("Slots Total", "Table Games") or label.endswith("Slots") or label.endswith("Tables"):
            cur_block[key] = label
        field = None
        if label == "AGP" and cur_block.get(key) == "Slots Total":
            field = "slots"
        elif label == "AGP" and cur_block.get(key) == "Table Games":
            field = "tables"
        elif label == "Total AGP":
            field = "ggr"
        elif label == "# of Casinos":
            field = "n_casinos"
        elif label == "Slots Total":
            field = "n_slot_devices"
        elif label == "Table Games":
            field = "n_table_devices"
        elif label == "Total Devices":
            field = "n_devices"
        if field is None:
            continue
        for j, mo in cols.items():
            recs.setdefault((key, mo), {})[field] = _num(v.iat[i, j])
    out = []
    for (key, mo), d in recs.items():
        out.append(dict(town_key=key, month=mo, source_file=f"fy/{Path(path).name}", **d))
    return out


def parse_monthly_xls(path, mo):
    v = pd.read_excel(path, header=None)
    hdr = next(i for i in range(10) if "Statewide" in [str(c).strip() for c in v.iloc[i]])
    towns = {j: str(c).strip().lower() for j, c in enumerate(v.iloc[hdr]) if pd.notna(c)}
    recs = {t: {} for t in towns.values()}
    block = None
    for i in range(hdr + 1, len(v)):
        label = str(v.iat[i, 0]).strip() if pd.notna(v.iat[i, 0]) else None
        if not label:
            continue
        if label == "Slots Total" or label == "Table Games" or label.endswith("Slots") or label.endswith("Tables"):
            block = label
        field = None
        if label == "AGP" and block == "Slots Total":
            field = "slots"
        elif label == "AGP" and block == "Table Games":
            field = "tables"
        elif label == "Total AGP":
            field = "ggr"
        elif label == "# of Casinos":
            field = "n_casinos"
        elif label == "Slots Total":
            field = "n_slot_devices"
        elif label == "Table Games":
            field = "n_table_devices"
        elif label == "Total Devices":
            field = "n_devices"
        if field is None:
            continue
        for j, t in towns.items():
            recs[t][field] = _num(v.iat[i, j])
    return [dict(town_key=t, month=mo, source_file=f"monthly/{Path(path).name}", **d) for t, d in recs.items()]


def pdf_created(path):
    import pymupdf
    raw = pymupdf.open(path).metadata.get("creationDate", "") or ""
    m = re.match(r"D:(\d{4})(\d\d)(\d\d)", raw)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def build():
    files = download_all()
    recs = []
    for fy_year, path in sorted(files["fy"].items()):
        recs += parse_fy(path, fy_year)
    have = {(r["town_key"], r["month"]) for r in recs}
    for mo, path in sorted(files["monthly_xls"].items()):
        for r in parse_monthly_xls(path, mo):
            if (r["town_key"], r["month"]) not in have:     # FY workbook (final, audited-year) wins if both
                recs.append(r)
    df = pd.DataFrame(recs)
    df = df[(df.month >= FIRST)].copy()
    # months beyond the last published one appear as all-zero columns in the current FY workbook
    tot = df[df.town_key == "statewide"].groupby("month")["ggr"].sum()
    live = tot[tot != 0].index
    covid = [m for m in tot.index if "2020-03" < m < "2020-07"]          # statewide closure Mar 17 - Jun 14 2020
    df = df[df.month.isin(set(live) | set(covid)) & (df.month <= max(live))]
    pub = {mo: pdf_created(p) for mo, p in files["monthly_pdf"].items()}
    rows = []
    for r in df.itertuples(index=False):
        if r.town_key == "statewide":
            unit, uid, lvl = "__STATE_TOTAL__", "CO___STATE_TOTAL__", "state_total"
        else:
            unit, uid = TOWNS[r.town_key]
            lvl = "town"
        rows.append(dict(state="CO", unit=unit, unit_id=uid, unit_level=lvl, month=r.month,
                         ggr=r.ggr, slots=r.slots, tables=round(r.ggr - r.slots, 2), n_casinos=r.n_casinos,
                         measure="AGP",
                         pub_date=pub.get(r.month, ""), pub_source="pdf_metadata" if pub.get(r.month) else "",
                         source_file=r.source_file, n_slot_units=r.n_slot_devices,
                         n_table_units=r.n_devices - r.n_slot_devices, _n_table_row=r.n_table_devices))
    out = pd.DataFrame(rows).sort_values(["month", "unit_level", "unit"]).reset_index(drop=True)
    return out, files


def checks(out, files):
    notes = []
    t = out[out.unit_level == "town"].groupby("month")[["ggr", "slots", "tables"]].sum()
    s = out[out.unit_level == "state_total"].set_index("month")
    ck = pd.DataFrame({"month": t.index, "sum_of_units": t.ggr.values,
                       "regulator_total": s.loc[t.index, "ggr"].values})
    ck["diff_pct"] = np.where(ck.regulator_total != 0,
                              100 * (ck.sum_of_units - ck.regulator_total) / ck.regulator_total.replace(0, np.nan), 0.0)
    ck["note"] = "towns (Black Hawk+Central City+Cripple Creek) vs Statewide Total AGP"
    x = out.n_table_units - out._n_table_row
    notes.append(f"n_table_units (Total Devices - Slots Total) minus 'Table Games' count = keno + other casino "
                 f"games devices: 0 in {int((x == 0).sum())} rows, max {int(x.max())} (first nonzero "
                 f"{out.month[x != 0].min()})")
    # tables := Total AGP - slot AGP, so it includes 'Other Casino Games' (post-Amendment 77, from 2021-05);
    # report how far that is from the published Table Games AGP line
    notes.append("tables = Total AGP - slot AGP (includes 'other casino games', tiny, since 2021-05)")
    # cross-check with the calendar-year 'Monthly Detail' workbook (independent file)
    if files.get("cy") is not None:
        m = pd.read_excel(files["cy"], header=None)
        # layout: Date | Total Casinos | Total Devices | Total AGP | Taxes | PY chg | (blank) | CC casinos | devices
        #   | AGP | taxes | chg | (blank) | BH ... | CRK ...   (header row 1 names the blocks)
        m = m[m[0].map(lambda x: isinstance(x, (dt.datetime, pd.Timestamp)))].copy()
        m["month"] = m[0].map(lambda x: x.strftime("%Y-%m"))
        hdr = pd.read_excel(files["cy"], header=None, nrows=2)
        blocks = {}
        for j, c in enumerate(hdr.iloc[0]):
            if isinstance(c, str) and c.strip():
                blocks[c.strip().lower()] = j
        # each block: Casinos | Devices | AGP | Taxes | PY chg, starting at the block-title column
        cmp = []
        for key, j0 in blocks.items():
            name = key
            agp_col, cas_col, dev_col = j0 + 2, j0, j0 + 1
            for _, r in m.iterrows():
                cmp.append((name, r["month"], _num(r[agp_col]), _num(r[cas_col]), _num(r[dev_col])))
        c = pd.DataFrame(cmp, columns=["town_key", "month", "agp_cy", "cas_cy", "dev_cy"])
        o = out.copy()
        o["town_key"] = o.unit.str.lower().replace({"__state_total__": "statewide"})
        mm = o.merge(c, on=["town_key", "month"], how="inner")
        mm = mm[mm.agp_cy != 0]                      # not-yet-filled months are 0 in that workbook
        d = (mm.ggr - mm.agp_cy).abs()
        notes.append(f"cross-check vs 'Monthly Detail by Calendar Year' workbook: {len(mm)} unit-months, "
                     f"max |AGP diff| ${d.max():,.0f}, n_casinos mismatches {(mm.n_casinos != mm.cas_cy).sum()}, "
                     f"slot+table units vs devices mismatches "
                     f"{((mm.n_slot_units + mm.n_table_units) != mm.dev_cy).sum()}")
        ck = ck.merge(mm[mm.town_key == "statewide"][["month", "agp_cy"]], on="month", how="left")
        ck["note"] = np.where(ck.agp_cy.notna(),
                              ck.note + "; CY-detail workbook statewide AGP diff $" +
                              (ck.regulator_total - ck.agp_cy).round(0).astype("Int64").astype(str),
                              ck.note)
        ck = ck.drop(columns="agp_cy")
    return ck, notes


def jumps(out):
    rows = []
    for uid, g in out[out.unit_level == "town"].groupby("unit_id"):
        g = g.sort_values("month")
        r = g.ggr / g.ggr.shift(1)
        for mo, x in zip(g.month, r):
            if pd.notna(x) and (x > 3 or x < 1 / 3) and not ("2020-03" <= mo <= "2020-07"):
                rows.append((uid, mo, x))
    return rows


if __name__ == "__main__":
    out, files = build()
    ck, notes = checks(out, files)
    DATA.mkdir(exist_ok=True)
    assert not out.duplicated(["unit_id", "month"]).any()
    cols = ["state", "unit", "unit_id", "unit_level", "month", "ggr", "slots", "tables", "n_casinos", "measure",
            "pub_date", "pub_source", "source_file", "n_slot_units", "n_table_units"]
    out[cols].to_csv(DATA / "state_co.csv.gz", index=False)
    ck.to_csv(DATA / "state_co_checks.csv.gz", index=False)
    print(out.month.min(), out.month.max(), out.month.nunique(), "months;", out.unit.nunique(), "units")
    print("max |diff_pct|", ck.diff_pct.abs().max())
    for n in notes:
        print(n)
    print("jumps:", jumps(out))

"""Mississippi: monthly casino revenue by MGC region (Central, Coastal, Northern), 2012-01 .. latest.

Run:  python3 scripts/state_ms.py [--refresh]
      (--refresh re-reads MGC listing pages and the rolling revenue sheets; monthly report PDFs are never
      re-downloaded.)
Output: data/state_ms.csv.gz, data/state_ms_checks.csv.gz, plus data/state_ms_devices.csv.gz (casino-level
  monthly slot and table counts from the Gaming Devices Reports; for imputing property sizes).
  Raw files: cache/ms/{monthly,revenue,listing}/.

SOURCES
  Mississippi Gaming Commission (www.msgamingcommission.com):
  * Monthly archive https://www.msgamingcommission.com/index.php/reports/monthly_archive/<year> ->
    monthly_details pages -> PDFs <MMYY>win.pdf (Slots Win Report, by region), <MMYY>hold.pdf (Tables Hold
    Report), <MMYY>gdrslots.pdf / <MMYY>gdrtables.pdf (Gaming Devices Reports: one row per casino),
    <MMYY>_sports_wagering.pdf (from 2018-09; 2018-08 = "Monthy_Sports_Activity_-_Regional_for_August.pdf").
  * "Monthly Casino Adjusted Gross Gaming Revenue" by region (one table per year):
    images/uploads/revenue_previous_history.pdf (2016-2025) and images/uploads/<MMYY>revenue.pdf (current year).
  Mississippi Department of Revenue (https://www.dor.ms.gov/gaming-statistics):
  * "Casino Gross Gaming Revenues" history (GamingGrossRevenues 2025 History.pdf): monthly, but only two
    groups - Gulf Coast counties vs Mississippi River counties - back to 1994.
  COUNTY DATA: checked - DOR publishes no county-level monthly gaming revenue (only Coast/River gross revenue
  and tax collections split into general fund / bond fund / local-government transfers, no counties), and
  MGC publishes regions only. So the finest geography is the 3 MGC regions (unit_level = region); Hancock
  County (Silver Slipper + Hollywood Gulf Coast) cannot be isolated.

UNITS: "Central" (Vicksburg, Natchez, Greenville = Central River), "Coastal" (Biloxi, Gulfport, Bay St Louis,
  D'Iberville), "Northern" (Tunica, Lula = Northern River), names as printed; unit_id MS_<REGION>.
  __STATE_TOTAL__ = MGC "Totals" column (2016+) or DOR total (2012-2015).

MEASURE
  2016-01 on: ggr = MGC region AGR minus that region's sports-wagering taxable revenue (measure "AGR" before
    2018-08, "AGR ex sports" after). MGC AGR includes sports: the residual AGR - slot win - table hold
    - sports shows no break at 2018-08. slots = slot win (Win/Loss, "Overall For Region"); tables = table hold
    ("Overall for Region", excludes poker). ggr - slots - tables = poker rake, other games and adjustments:
    typically 1-2% of ggr in Central, 0.5-1% Coastal, 3-6% Northern (can be negative in a month).
  2012-01 .. 2015-12: MGC's regional AGR table is not online for these years. Coastal ggr = DOR Gulf Coast
    counties AGR (measure "AGR (DOR Gulf Coast counties)"). Central and Northern are only published together
    (DOR River counties), so the River figure is split in proportion to k_r x (slot win + table hold) with
    k_r = median AGR/(win+hold) over 2016-01..2018-07 (Central 1.0133, Northern 1.0317); measure says
    "... imputed". slots/tables are the published MGC figures in all years, so slots+tables is a fully
    published, consistent series 2012-2026 if the imputed split is not wanted.
    DOR vs MGC comparability (where both exist): 2016-2022 median |diff| of totals 0.21%, 94% of months
    within 1%; from 2023 DOR drifts from MGC (median 3%), so DOR is used only for 2012-2015.
n_casinos: number of casinos listed for the region in that month's Gaming Devices Report: Slots.
COVID: casinos closed 2020-03-16 .. 2020-05-21. MGC posted a closure notice instead of April 2020 reports
  (MGC_April_Reports_2020.pdf) and AGR = 0: April 2020 rows are 0 (ggr, slots, tables, n_casinos).
MONTHS: 2012-01 .. 2026-08 (176 months, no gaps). Quirks handled: "August" with no year on the 2016
  archive page; March 2022 win report named 0322in.pdf; January 2025 files named "... - Copy".

PUBLICATION DATE: earliest PDF CreationDate among the month's MGC report PDFs (pub_source = pdf_metadata);
  would be blanked if > 60 days after month-end (re-generated files; none left after taking the earliest).
  Lag after month-end: median 17 days (2015 on: 14-19 days; 2012-2014 about 35 days).

SPOT CHECKS (data/state_ms_checks.csv.gz, all 176 months):
  * sum of 3 regions vs statewide total: exact (same table; max |diff| 2e-14%).
  * sum of regional slot win vs the win report's "Overall For State": 0.000% every month.
  * DOR total vs MGC AGR total noted per month (see above).
  * $ units (not thousands) confirmed; no month/month jump > 3x or < 1/3 outside Mar-Jun 2020.
"""
import re
import sys
import time
import datetime as dt
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "ms"
DATA = ROOT / "data"
MGC = "https://www.msgamingcommission.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"})
_last = [0.0]
REFRESH = "--refresh" in sys.argv   # re-read listing pages / rolling revenue sheets; monthly reports never re-fetched
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
FIRST_YEAR = 2012


def fetch(url, dest, force=False, min_size=1):
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size >= min_size and not force:
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
                if str(url).lower().endswith(".pdf") and r.content[:5] != b"%PDF-":
                    print(f"  not a PDF (missing file?) {url}", file=sys.stderr)
                    return None
                dest.write_bytes(r.content)
                return dest
            if r.status_code == 404:
                return None
            print(f"  HTTP {r.status_code} {url}", file=sys.stderr)
        except requests.RequestException as e:
            print(f"  error {e} {url}", file=sys.stderr)
        time.sleep(2 ** attempt)
    raise RuntimeError(f"failed to download {url}")


def month_pages(year, force=False):
    """Return {YYYY-MM: monthly_details url} from the MGC yearly archive page."""
    p = fetch(f"{MGC}/index.php/reports/monthly_archive/{year}", CACHE / "listing" / f"archive_{year}.html",
              force=force)
    html = p.read_text(encoding="utf-8", errors="ignore")
    out = {}
    for href, txt in re.findall(r'href="([^"]*monthly_details/\d+)"[^>]*>\s*([^<]+?)\s*<', html):
        t = txt.strip().lower().replace("novemeber", "november")
        m = re.match(r"([a-z]+)\s*(\d{4})?", t)
        if not m or m.group(1) not in MONTHS:
            continue
        yr = m.group(2) or str(year)                  # e.g. 'August' (no year) on the 2016 page
        out[f"{yr}-{MONTHS.index(m.group(1)) + 1:02d}"] = href
    return out


def download_all(last_year=None):
    last_year = last_year or dt.date.today().year
    files = {}
    for y in range(FIRST_YEAR, last_year + 1):
        pages = month_pages(y, force=REFRESH and y >= last_year - 1)
        for mo, href in sorted(pages.items()):
            dp = fetch(href, CACHE / "listing" / f"details_{mo}.html",
                       force=REFRESH and mo >= f"{last_year - 1}-06")
            html = dp.read_text(encoding="utf-8", errors="ignore")
            links = sorted(set(re.findall(r'href="([^"]+\.(?:pdf|xlsx?))"', html, flags=re.I)))
            files[mo] = []
            for u in links:
                if not u.lower().endswith(".pdf"):
                    continue          # PDFs only: one consistent (Reporting Services) layout for all years
                name = u.rsplit("/", 1)[-1]
                got = fetch(u, CACHE / "monthly" / name)
                if got is not None:
                    files[mo].append(got)
    # region AGR (MGC) and Coast/River gross revenue (DOR)
    fetch(f"{MGC}/images/uploads/revenue_previous_history.pdf", CACHE / "revenue" / "revenue_previous_history.pdf",
          force=REFRESH)
    mp = fetch(f"{MGC}/index.php/reports/monthly_reports", CACHE / "listing" / "monthly_reports.html", force=REFRESH)
    cur = re.findall(r'href="([^"]+/images/uploads/(\d{4})revenue\.pdf)"', mp.read_text(errors="ignore"))
    for u, mmyy in cur:
        fetch(u, CACHE / "revenue" / f"{mmyy}revenue.pdf")
    dor = "https://www.dor.ms.gov/sites/default/files/statistics/"
    fetch(dor + "GamingGrossRevenues%202025%20History.pdf", CACHE / "revenue" / "dor_GamingGrossRevenues_2025_History.pdf")
    return files


# ----------------------------------------------------------------------------------------------------------
# parsing
# ----------------------------------------------------------------------------------------------------------
REGIONS = ["Central", "Coastal", "Northern"]
MONEY = re.compile(r"^\(?-?\$?\(?-?[\d,]+(?:\.\d+)?\)?$")


def money(tok):
    t = tok.strip().replace("$", "").replace(",", "").replace("‐", "-").replace("‑", "-")
    neg = "(" in t or t.startswith("-")
    v = float(t.strip("()-"))
    return -v if neg else v


def lines_of(page):
    return [l.strip() for l in page.get_text().splitlines() if l.strip()]


def parse_overall(path, label_re, value_index):
    """win / hold / sports reports: one page per region; the row 'Overall For Region' is followed by its
    values in order. Returns {region: value} using the value_index-th value (0-based)."""
    import pymupdf
    out = {}
    for page in pymupdf.open(path):
        ls = lines_of(page)
        if not ls or ls[0] not in REGIONS:
            continue
        for i, l in enumerate(ls):
            if re.fullmatch(label_re, l, flags=re.I):
                vals = [x for x in ls[i + 1:i + 8] if MONEY.match(x) or re.fullmatch(r"-?[\d.]+%", x)]
                out[ls[0]] = money(vals[value_index])
                break
    return out


def parse_devices(path):
    """gdrslots / gdrtables: per region, one row per casino (name line, then counts; last count = Total)."""
    import pymupdf
    out = {}
    for page in pymupdf.open(path):
        ls = lines_of(page)
        if not ls or ls[0] not in REGIONS:
            continue
        region = ls[0]
        try:
            start = ls.index("Total") + 1                 # end of the column header
        except ValueError:
            continue
        casinos, name, nums = [], None, []
        for l in ls[start:]:
            if re.fullmatch(r"-?[\d,]+", l):
                nums.append(int(l.replace(",", "")))
                continue
            if name is not None and nums:
                casinos.append((name, nums[-1]))
                name, nums = None, []
            if l.startswith("Region Total"):
                break
            name = l if name is None else name + " " + l   # names wrapped over two lines
        out[region] = casinos
    return out


def parse_sports_2018_08(path):
    """First sports month uses a different (event-activity) report: 'Region Totals' taxable revenue."""
    import pymupdf
    out, region = {}, None
    for page in pymupdf.open(path):
        rows = {}
        for w in page.get_text("words"):
            rows.setdefault(round(w[1] / 4), []).append(w)
        for k in sorted(rows):
            ws = [w[4] for w in sorted(rows[k])]
            if ws[:1] == ["Region:"] and len(ws) > 1:
                region = ws[1]
            if ws[:2] == ["Region", "Totals:"] and region in REGIONS:
                vals = [x for x in ws[2:] if "$" in x]
                out[region] = money(vals[2])
    return out


def parse_agr_tables(path):
    """MGC 'Monthly casino adjusted gross gaming revenue' (one page per calendar year):
    Month, Year, Central, Coastal, Northern, Totals."""
    import pymupdf
    out = {}
    for page in pymupdf.open(path):
        ls = lines_of(page)
        for i in range(len(ls) - 5):
            m = ls[i].lower()
            if m in MONTHS and re.fullmatch(r"20\d\d", ls[i + 1]) and all(MONEY.match(x) for x in ls[i + 2:i + 6]):
                mo = f"{ls[i + 1]}-{MONTHS.index(m) + 1:02d}"
                c, co, n, t = (money(x) for x in ls[i + 2:i + 6])
                out[mo] = {"Central": c, "Coastal": co, "Northern": n, "Total": t}
    return out


def parse_dor_history(path):
    """DOR 'Casino gross gaming revenues': Gulf Coast counties vs Mississippi River counties (1992 on)."""
    import pymupdf
    out = {}
    for page in pymupdf.open(path):
        ls = [l for l in lines_of(page) if l != "$"]
        year = None
        i = 0
        while i < len(ls):
            l = ls[i].upper()
            if l in [m.upper() for m in MONTHS]:
                j = i + 1
                if re.fullmatch(r"(19|20)\d\d", ls[j]):
                    year = int(ls[j])
                    j += 1
                vals = []
                while j < len(ls) and len(vals) < 3 and MONEY.match(ls[j].replace(" ", "")):
                    vals.append(money(ls[j].replace(" ", "")))
                    j += 1
                if year and len(vals) == 3:
                    out[f"{year}-{MONTHS.index(l.lower()) + 1:02d}"] = {"GulfCoast": vals[0], "River": vals[1],
                                                                      "Total": vals[2]}
                i = j
                continue
            i += 1
    return out


def pdf_created(path):
    import pymupdf
    raw = pymupdf.open(path).metadata.get("creationDate", "") or ""
    m = re.match(r"D:(\d{4})(\d\d)(\d\d)", raw)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


# ----------------------------------------------------------------------------------------------------------
# build
# ----------------------------------------------------------------------------------------------------------
def file_month(name):
    m = re.match(r"(\d\d)(\d\d)", name)
    return f"20{m.group(2)}-{m.group(1)}" if m else None


def parse_monthly():
    recs, created = {}, {}
    for f in sorted((CACHE / "monthly").glob("*.pdf")):
        n = f.name.lower()
        mo = file_month(f.name)
        if n.startswith("monthy_sports_activity"):
            recs.setdefault("2018-08", {})["sports"] = parse_sports_2018_08(f)
            recs["2018-08"]["sports_file"] = f.name
            continue
        if n.startswith("mgc_april_reports_2020"):
            recs.setdefault("2020-04", {})["closed"] = True
            recs["2020-04"]["win_file"] = f.name
            created["2020-04"] = pdf_created(f)
            continue
        if not mo:
            continue
        c = pdf_created(f)
        if c and (mo not in created or c < created[mo]):
            created[mo] = c                                   # earliest creation date among the month's PDFs
        r = recs.setdefault(mo, {})
        if "sport" in n:
            r["sports"] = parse_overall(f, r"Overall for Region", 1)
            r["sports_file"] = f.name
        elif "gdrslots" in n:
            r["gdrslots"] = parse_devices(f)
        elif "gdrtables" in n:
            r["gdrtables"] = parse_devices(f)
        elif "hold" in n:
            r["hold"] = parse_overall(f, r"Overall for Region", 2)
            r["hold_state"] = parse_state_line(f, r"Overall for State", 2)
        elif re.search(r"win", n) or re.fullmatch(r"\d{4}in\.pdf", n):     # '0322in.pdf' is March 2022 win
            r["win"] = parse_overall(f, r"Overall For Region", 2)
            r["win_state"] = parse_state_line(f, r"Overall For State", 2)
            r["win_file"] = f.name
    return recs, created


def parse_state_line(path, label_re, value_index):
    import pymupdf
    doc = pymupdf.open(path)
    ls = lines_of(doc[len(doc) - 1])
    for i, l in enumerate(ls):
        if re.fullmatch(label_re, l, flags=re.I):
            vals = [x for x in ls[i + 1:i + 8] if MONEY.match(x) or re.fullmatch(r"-?[\d.]+%", x)]
            return money(vals[value_index])
    return None


def month_end(mo):
    y, m = map(int, mo.split("-"))
    return dt.date(y + m // 12, m % 12 + 1, 1) - dt.timedelta(days=1)


def build():
    import numpy as np
    import pandas as pd
    download_all()
    recs, created = parse_monthly()
    agr = {}
    for f in sorted((CACHE / "revenue").glob("*.pdf")):
        if not f.name.startswith("dor_"):
            for mo, v in parse_agr_tables(f).items():
                if mo not in agr or f.name != "revenue_previous_history.pdf":   # current-year sheet wins
                    agr[mo] = dict(v, file=f"revenue/{f.name}")
    dor = parse_dor_history(CACHE / "revenue" / "dor_GamingGrossRevenues_2025_History.pdf")
    last = max(m for m in recs if "win" in recs[m] or recs[m].get("closed"))
    months = [m for m in sorted(recs) if FIRST_YEAR <= int(m[:4]) and m <= last]
    # AGR / (slot win + table hold) per region, pre-sports-betting 2016-01..2018-07 (used only to split the
    # DOR 'Mississippi River counties' AGR between Central and Northern for 2012-2015)
    k = {}
    for g in REGIONS:
        rat = [agr[m][g] / (recs[m]["win"][g] + recs[m]["hold"][g]) for m in months
               if "2016-01" <= m <= "2018-07" and m in agr and "win" in recs[m]]
        k[g] = float(np.median(rat))
    rows, dev = [], []
    for mo in months:
        r = recs[mo]
        closed = r.get("closed", False)
        pub = created.get(mo, "")
        if pub and (dt.date.fromisoformat(pub) - month_end(mo)).days > 60:
            pub = ""            # file regenerated long after first release (e.g. 2016-07, 2023-01/02): unknown
        base = dict(state="MS", month=mo, pub_date=pub, pub_source="pdf_metadata" if pub else "")
        sp = r.get("sports", {})
        n_cas = {g: len(r.get("gdrslots", {}).get(g, [])) for g in REGIONS}
        if mo in agr:
            src = agr[mo]["file"]
            for g in REGIONS:
                ggr = agr[mo][g] - sp.get(g, 0.0)
                rows.append(dict(base, unit=g, unit_id=f"MS_{g.upper()}", unit_level="region", ggr=ggr,
                                 slots=0.0 if closed else r["win"][g], tables=0.0 if closed else r["hold"][g],
                                 n_casinos=n_cas[g], measure="AGR ex sports" if sp else "AGR",
                                 source_file=f"{src}; monthly/{r.get('win_file', '')}" +
                                             (f"; monthly/{r['sports_file']}" if sp else "")))
            rows.append(dict(base, unit="__STATE_TOTAL__", unit_id="MS___STATE_TOTAL__", unit_level="state_total",
                             ggr=agr[mo]["Total"] - sum(sp.values()), slots=None if closed else r["win_state"],
                             tables=None if closed else r["hold_state"], n_casinos=sum(n_cas.values()),
                             measure="AGR ex sports" if sp else "AGR", source_file=src))
        elif mo in dor:
            d = dor[mo]
            w = {g: k[g] * (r["win"][g] + r["hold"][g]) for g in ("Central", "Northern")}
            for g in REGIONS:
                if g == "Coastal":
                    ggr, meas = d["GulfCoast"], "AGR (DOR Gulf Coast counties)"
                else:
                    ggr = d["River"] * w[g] / (w["Central"] + w["Northern"])
                    meas = "AGR (DOR River counties split by win+hold share; imputed)"
                rows.append(dict(base, unit=g, unit_id=f"MS_{g.upper()}", unit_level="region", ggr=ggr,
                                 slots=r["win"][g], tables=r["hold"][g], n_casinos=n_cas[g], measure=meas,
                                 source_file=f"revenue/dor_GamingGrossRevenues_2025_History.pdf; "
                                             f"monthly/{r['win_file']}"))
            rows.append(dict(base, unit="__STATE_TOTAL__", unit_id="MS___STATE_TOTAL__", unit_level="state_total",
                             ggr=d["Total"], slots=r["win_state"], tables=r["hold_state"],
                             n_casinos=sum(n_cas.values()), measure="AGR (DOR)",
                             source_file="revenue/dor_GamingGrossRevenues_2025_History.pdf"))
        else:
            print(f"  no AGR for {mo}", file=sys.stderr)
        for g in REGIONS:
            tabs = dict(r.get("gdrtables", {}).get(g, []))
            for name, n in r.get("gdrslots", {}).get(g, []):
                dev.append(dict(state="MS", month=mo, region=g, casino=name, slot_units=n,
                                table_units=tabs.get(name)))
            for name, n in r.get("gdrtables", {}).get(g, []):
                if name not in dict(r.get("gdrslots", {}).get(g, [])):
                    dev.append(dict(state="MS", month=mo, region=g, casino=name, slot_units=None, table_units=n))
    df = pd.DataFrame(rows)
    return df, pd.DataFrame(dev), recs, agr, dor, k


def checks(df, recs, agr, dor):
    import numpy as np
    import pandas as pd
    u = df[df.unit_level == "region"].groupby("month")[["ggr", "slots", "tables"]].sum()
    st = df[df.unit_level == "state_total"].set_index("month")
    ck = pd.DataFrame({"month": u.index, "sum_of_units": u.ggr.values, "regulator_total": st.loc[u.index, "ggr"].values})
    ck["diff_pct"] = np.where(ck.regulator_total != 0,
                              100 * (ck.sum_of_units - ck.regulator_total) / ck.regulator_total.replace(0, np.nan), 0.0)
    notes = []
    for mo in ck.month:
        parts = ["sum of 3 regions vs statewide total (same source)"]
        sl = st.loc[mo, "slots"]
        if pd.notna(sl) and sl:
            parts.append(f"slot win regions vs 'Overall for State' {100 * (u.loc[mo, 'slots'] - sl) / sl:+.3f}%")
        if mo in agr and mo in dor and agr[mo]["Total"]:
            parts.append(f"DOR total vs MGC AGR total {100 * (dor[mo]['Total'] - agr[mo]['Total']) / agr[mo]['Total']:+.2f}%")
        notes.append("; ".join(parts))
    ck["note"] = notes
    return ck


def jumps(df):
    out = []
    for uid, g in df[df.unit_level == "region"].groupby("unit_id"):
        g = g.sort_values("month")
        r = g.ggr / g.ggr.shift(1)
        for mo, x in zip(g.month, r):
            if x == x and (x > 3 or x < 1 / 3) and not ("2020-03" <= mo <= "2020-06"):
                out.append((uid, mo, round(x, 2)))
    return out


if __name__ == "__main__":
    import pandas as pd
    df, dev, recs, agr, dor, k = build()
    ck = checks(df, recs, agr, dor)
    assert not df.duplicated(["unit_id", "month"]).any()
    cols = ["state", "unit", "unit_id", "unit_level", "month", "ggr", "slots", "tables", "n_casinos", "measure",
            "pub_date", "pub_source", "source_file"]
    DATA.mkdir(exist_ok=True)
    df[cols].sort_values(["month", "unit_level", "unit"]).to_csv(DATA / "state_ms.csv.gz", index=False)
    ck.to_csv(DATA / "state_ms_checks.csv.gz", index=False)
    dev.to_csv(DATA / "state_ms_devices.csv.gz", index=False)
    print(df.month.min(), df.month.max(), df.month.nunique(), "months")
    print("AGR/(win+hold) ratios used for the 2012-2015 River split:", {g: round(v, 4) for g, v in k.items()})
    print("max |diff_pct|", ck.diff_pct.abs().max())
    print("jumps:", jumps(df))

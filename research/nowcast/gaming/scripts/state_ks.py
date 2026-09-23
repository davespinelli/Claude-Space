"""Kansas state-owned (Lottery gaming facility) casinos: monthly revenue by casino
-> data/state_ks.csv.gz

Source: Kansas Racing and Gaming Commission (KRGC), Revenue Reports
  https://krgc.kansas.gov/public-info/revenue-reports/
  One PDF per month (Commission-meeting exhibit), one page per casino, figures "as reported by the
  Kansas Lottery Central Computer System" (unaudited). 2009-2025-11 PDFs are linked directly
  (wp-content/uploads/2025/10/<Month>_<Year>_Revenue_Report.pdf, file names vary); 2025-12 onward are
  WordPress posts (e.g. /august-revenue-reports/) that redirect to the PDF
  (wp-content/uploads/2026/9September/August-Revenue-Reports.pdf). The month and year are read
  from the PDF text (column header "<Month> <Month> Fiscal YTD Fiscal YTD" + year line), not from
  file names.
Measure: "Total Lottery Gaming Facility Revenue" = Electronic gaming machines + Table games + Other
  ("other sweeps, principally lost and found funds", a few $ to a few $k a month). ggr = that published
  total (measure "LGFR" = the state's adjusted gross gaming revenue base for the 22%/24% state share);
  slots = Electronic gaming machines, tables = Table games. Dollars. No sports wagering on these pages
  (Kansas sports wagering since 9/2022 is reported separately by the Kansas Lottery -> not used).
Units (unit_level = property; names as printed on each page):
  KS_BOOT_HILL        BOOT HILL CASINO & RESORT (Dodge City)
  KS_KANSAS_STAR      KANSAS STAR CASINO & RESORT (Mulvane; opened 12/2011)
  KS_HOLLYWOOD_KS     HOLLYWOOD CASINO & RESORT (Hollywood Casino at Kansas Speedway, Kansas City;
                      Jan 2012 = one-day controlled demonstration 1/30/2012, opened 2/3/2012)
  KS_KANSAS_CROSSING  KANSAS CROSSING CASINO & RESORT (Pittsburg; opened 3/2017)
State total: KRGC publishes no statewide figure, so __STATE_TOTAL__ (unit_id KS_STATE_TOTAL) is the
  SUM of the casino totals (derived, not regulator-published).
Month range: 2012-01 .. 2026-08 (latest posted 2026-09).
April 2017: the KRGC PDF (April_2017_Revenue_Report.pdf) is a scanned image with no text; its values
  are taken from the "April 2017" prior-year column of April_2018_Revenue_Report.pdf (source_file
  says so); pub_date still = CreationDate of the April 2017 PDF.
COVID: casinos closed mid-March 2020 to mid/late May 2020 -> April 2020 = 0 as published.
Publication dates: pub_date = PDF CreationDate of that month's report (pub_source = pdf_metadata);
  the reports are Commission-meeting exhibits; lag 3-58 days, median 16. (All pre-2025 PDFs were
  re-uploaded in 10/2025, but their embedded CreationDates are the originals.) Blanked: dates shared
  by >= 3 reports (Dec 2019, Jan, Feb 2020 all created 2020-04-13) and > 60 days (Apr 2020 report
  created 2021-05-26) -> 4 months without pub_date.
Checks (data/state_ks_checks.csv.gz):
  (1) "ytd-implied": for each month, sum over casinos of the published Fiscal-YTD total at month M minus
      the Fiscal-YTD total in the previous month's report (July: YTD itself) vs the sum of the monthly
      totals. Captures revisions and parse errors.
  (2) "prior-year column": the same month's total re-published one year later as the comparison
      column vs the original.
  Run 2026-09-23: (1) 174 months, max |diff| 0.0000% (2012-01 and 2017-05 not computable);
  (2) 163 months, max |diff| 0.82% (small later revisions; none > 1%).
  Page parse: 4 casinos x every month present after each opening, no gaps (script asserts);
  Other = total - EGM - tables, max $30.7k (Hollywood 2019-03). Some PDFs extract month names with
  stray spaces ("Ma y"); handled. November_2017 PDF repeats 3 pages verbatim (identical; deduped).
  Jump scan (m/m >3x or <1/3 outside Mar-Jun 2020): Hollywood 2012-02 (x480; Jan 2012 = one-day
  demonstration) and Kansas Crossing 2017-04 (x5.6; opened late March 2017). Both real.
  Rows: 818 (4 casinos + derived state total), 2012-01 .. 2026-08.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "ks"
DATA = ROOT / "data"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
LISTING = "https://krgc.kansas.gov/public-info/revenue-reports/"
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
# month names in some PDFs are extracted with stray spaces ("Ma y", "Decem ber")
MON = "|".join(r"\s?".join(m.capitalize()) for m in MONTHS)
UNITS = [(r"BOOT HILL", "KS_BOOT_HILL"), (r"KANSAS STAR", "KS_KANSAS_STAR"),
         (r"HOLLYWOOD", "KS_HOLLYWOOD_KS"), (r"KANSAS CROSSING", "KS_KANSAS_CROSSING")]
_last = [0.0]


def get(url):
    for attempt in range(4):
        w = 0.6 - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=60, allow_redirects=True)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            print(f"  retry {attempt + 1} {url}: {e}", file=sys.stderr)
            time.sleep(2 ** attempt * 2)
    raise RuntimeError(url)


def download(refresh: bool) -> list[Path]:
    CACHE.mkdir(parents=True, exist_ok=True)
    lst = CACHE / "_listing_revenue-reports.html"
    if refresh or not lst.exists():
        lst.write_bytes(get(LISTING).content)
    html = lst.read_text(errors="ignore")
    postmap = CACHE / "_posts.tsv"  # post url -> pdf file name (posts redirect to PDFs)
    posts = dict(l.split("\t") for l in postmap.read_text().splitlines()) if postmap.exists() else {}
    out = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.S):
        h, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if "/wp-content/uploads/" in h and h.lower().endswith(".pdf"):
            u = h if h.startswith("http") else "https://krgc.kansas.gov" + h
            dest = CACHE / Path(u).name
            if not dest.exists():
                dest.write_bytes(get(u).content)
            out.append(dest)
        elif ("krgc.kansas.gov/" in h and "revenue" in (h + txt).lower()
              and "uploads" not in h and "public-info" not in h):
            if h in posts and (CACHE / posts[h]).exists():
                out.append(CACHE / posts[h])
                continue
            r = get(h)
            fn = Path(r.url.split("?")[0]).name
            if not fn.lower().endswith(".pdf"):
                print("  post without pdf:", h, file=sys.stderr)
                continue
            (CACHE / fn).write_bytes(r.content)
            posts[h] = fn
            out.append(CACHE / fn)
    postmap.write_text("\n".join(f"{k}\t{v}" for k, v in posts.items()))
    return sorted(set(out))


def num(tok: str) -> float:
    t = tok.replace(",", "").replace("$", "")
    if re.fullmatch(r"[‐‑‒–—\-]+", t):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    return -float(t.strip("()")) if neg else float(t)


NUM = r"(?:\(?-?[\d,]+\.\d+\)?|\(?-?[\d,]+\)?|[‐‑‒–—\-])"


def parse_pdf(path: Path) -> list[dict]:
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        pages = [(pg.extract_text() or "") for pg in pdf.pages]
    out = []
    for t in pages:
        name = re.search(r"^\s*([A-Z][A-Z &+.\-]*(?:CASINO|RESORT)[A-Z &+.\-]*)\s*$", t, re.M)
        if not name:
            continue
        name = re.sub(r"\s+", " ", name.group(1)).strip()
        uid = next((u for pat, u in UNITS if re.search(pat, name)), None)
        if uid is None:
            continue
        hdr = re.search(rf"({MON})(?:\s+({MON}))?\s+Fiscal YTD(?:\s+Fiscal YTD)?\s*\n\s*((?:\d{{4}}\s*)+)", t)
        if not hdr:
            continue
        mo = MONTHS.index(re.sub(r"\s", "", hdr.group(1)).lower()) + 1
        years = [int(y) for y in hdr.group(3).split()]
        ncol = len(years)
        # columns: 4 -> cur, prior, ytd_cur, ytd_prior ; 2 -> cur, ytd_cur
        year = years[0]
        flat = re.sub(r"Total Lottery Gaming Facility\s*\n\s*Revenue", "Total Lottery Gaming Facility Revenue", t)
        vals = {}
        for key, pat in (("egm", r"Electronic gaming machines"), ("tables", r"Table games"),
                         ("other", r"Other(?:\s*#)?"), ("total", r"Total Lottery Gaming Facility Revenue")):
            m = re.search(rf"^{pat}\s*\**\s+((?:{NUM}\s*){{{ncol}}})\s*$", flat, re.M)
            if not m:
                m = re.search(rf"^{pat}\s*\**\s+((?:{NUM}\s+){{{ncol - 1}}}{NUM})", flat, re.M)
            if m:
                vals[key] = [num(x) for x in re.findall(NUM, m.group(1))][:ncol]
        if "total" not in vals:
            print(f"  WARN no total on page {name} {path.name}", file=sys.stderr)
            continue
        idx_ytd = 2 if ncol == 4 else 1
        rec = dict(unit=name, unit_id=uid, month=f"{year}-{mo:02d}", source_file=path.name,
                   ggr=vals["total"][0], slots=vals.get("egm", [None])[0],
                   tables=vals.get("tables", [None])[0], other=vals.get("other", [0])[0],
                   ytd=vals["total"][idx_ytd])
        if ncol == 4:
            rec["prior"] = vals["total"][1]
            rec["prior_slots"] = vals.get("egm", [None, None])[1]
            rec["prior_tables"] = vals.get("tables", [None, None])[1]
            rec["prior_month"] = f"{years[1]}-{mo:02d}"
        out.append(rec)
    return out


def pdf_created(path: Path) -> str:
    import pymupdf
    d = pymupdf.open(path).metadata.get("creationDate") or ""
    m = re.match(r"D:(\d{4})(\d{2})(\d{2})", d)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def main(refresh=False):
    files = download(refresh)
    recs, created = [], {}
    for p in files:
        rows = parse_pdf(p)
        for r in rows:
            r["pub_date"] = pdf_created(p)
        recs += rows
        if not rows and "April_2017" in p.name:
            created["2017-04"] = pdf_created(p)
    df = pd.DataFrame(recs)
    df = df[df.month >= "2011-07"]
    dup = df[df.duplicated(["unit_id", "month"], keep=False)]
    if len(dup):
        # November_2017_Revenue_Report.pdf repeats three pages verbatim -> identical duplicates
        nconf = dup.groupby(["unit_id", "month"]).ggr.nunique().max()
        print(f"duplicate unit-months: {len(dup)} rows, max distinct values per key = {nconf}")
        assert nconf == 1, "conflicting duplicate pages"
        df = df.sort_values("pub_date").drop_duplicates(["unit_id", "month"], keep="last")
    # April 2017 from April 2018's prior-year column
    fill = df[df.prior_month == "2017-04"]
    have = set(df[df.month == "2017-04"].unit_id)
    add = []
    for r in fill.itertuples():
        if r.unit_id in have:
            continue
        add.append(dict(unit=r.unit, unit_id=r.unit_id, month="2017-04",
                        source_file=f"{r.source_file} (prior-year column; April_2017_Revenue_Report.pdf is image-only)",
                        ggr=r.prior, slots=r.prior_slots, tables=r.prior_tables,
                        pub_date=created.get("2017-04", "")))
    df = pd.concat([df, pd.DataFrame(add)], ignore_index=True)

    panel = df[df.month >= "2012-01"].copy()
    panel["state"] = "KS"
    panel["unit_level"] = "property"
    panel["n_casinos"] = None
    panel["measure"] = "LGFR"
    tot = panel.groupby("month").agg(ggr=("ggr", "sum"), slots=("slots", "sum"), tables=("tables", "sum"),
                                     n_casinos=("unit_id", "nunique"), pub_date=("pub_date", "max"),
                                     source_file=("source_file", "first")).reset_index()
    tot["source_file"] = "sum of casino pages (" + tot.source_file.str.split(" ").str[0] + ")"
    tot = tot.assign(state="KS", unit="__STATE_TOTAL__", unit_id="KS_STATE_TOTAL",
                     unit_level="state_total", measure="LGFR")
    cols = ["state", "unit", "unit_id", "unit_level", "month", "ggr", "slots", "tables", "n_casinos",
            "measure", "pub_date", "pub_source", "source_file"]
    out = pd.concat([panel, tot], ignore_index=True)
    # CreationDates shared by >= 3 months (batch re-creation: 2020-04-13 for Dec 2019-Feb 2020) or
    # > 60 days after month end (Apr 2020 report created 2021-05-26) are not first-publication dates
    # -> blank. Pairs of months created the same day (e.g. Sep+Oct 2022 on 2022-11-18, a skipped
    # meeting) are kept: that is when the earlier month actually appeared.
    mp = out[out.unit_level == "property"].groupby("pub_date").month.nunique()
    shared = set(mp[mp > 2].index)
    lagd = (pd.to_datetime(out.pub_date.replace("", None)) -
            (pd.to_datetime(out.month) + pd.offsets.MonthEnd(0))).dt.days
    bad = out.pub_date.isin(shared) | (lagd > 60)
    out.loc[bad, "pub_date"] = ""
    out["pub_source"] = out.pub_date.map(lambda x: "pdf_metadata" if isinstance(x, str) and x else "")
    out = out[cols].sort_values(["month", "unit_level", "unit_id"])
    assert not out.duplicated(["unit_id", "month"]).any()
    # zero months must be 0 not missing: check completeness per unit after its first month
    months = sorted(out.month.unique())
    for uid, g in out[out.unit_level == "property"].groupby("unit_id"):
        exp = [m for m in months if m >= g.month.min()]
        miss = sorted(set(exp) - set(g.month))
        if miss:
            print("MISSING months", uid, miss)
    DATA.mkdir(exist_ok=True)
    out.to_csv(DATA / "state_ks.csv.gz", index=False)

    # checks
    chk = []
    d = df.set_index(["unit_id", "month"])
    su = panel.groupby("month").ggr.sum()
    for m in sorted(panel.month.unique()):
        y, mo = map(int, m.split("-"))
        prev = f"{y}-{mo - 1:02d}" if mo > 1 else f"{y - 1}-12"
        imp, ok = 0.0, True
        for uid in panel[panel.month == m].unit_id:
            cur = d.loc[(uid, m), "ytd"] if (uid, m) in d.index else None
            if cur is None or pd.isna(cur):
                ok = False
                break
            if mo == 7 or (uid, prev) not in d.index:
                imp += cur  # FY start, or first month of a casino
            elif pd.notna(d.loc[(uid, prev), "ytd"]):
                imp += cur - d.loc[(uid, prev), "ytd"]
            else:
                ok = False  # previous report has no YTD (April 2017 image-only PDF)
                break
        if ok:
            chk.append(dict(month=m, sum_of_units=su[m], regulator_total=imp,
                            diff_pct=(su[m] - imp) / imp * 100 if imp else None,
                            note="ytd-implied monthly total (sum of casinos' Fiscal YTD differences)"))
    pr = df.dropna(subset=["prior"]).groupby("prior_month").prior.sum()
    for m, v in pr.items():
        if m in su.index and m >= "2012-01":
            chk.append(dict(month=m, sum_of_units=su[m], regulator_total=v,
                            diff_pct=(su[m] - v) / v * 100 if v else None,
                            note="prior-year column in next year's report"))
    chk = pd.DataFrame(chk).sort_values(["note", "month"])
    chk.to_csv(DATA / "state_ks_checks.csv.gz", index=False)

    jumps = []
    for uid, g in panel.sort_values("month").groupby("unit_id"):
        v = g.set_index("month").ggr
        rat = v / v.shift(1)
        for m, x in rat.items():
            if pd.notna(x) and (x > 3 or x < 1 / 3) and not ("2020-03" <= m <= "2020-06"):
                jumps.append((uid, m, round(x, 2)))
    comp = (panel.slots.fillna(0) + panel.tables.fillna(0) - panel.ggr).abs()
    lag = (pd.to_datetime(out.pub_date.replace("", None)) -
           (pd.to_datetime(out.month) + pd.offsets.MonthEnd(0))).dt.days
    print(f"rows={len(out)} months {out.month.min()}..{out.month.max()} units={panel.unit_id.nunique()}")
    print("max |egm+tables-total| (=other):", comp.max())
    for n, g in chk.groupby("note"):
        big = g[g.diff_pct.abs() > 1]
        print(f"check {n}: n={len(g)} max|diff%|={g.diff_pct.abs().max():.4f} >1%: {big[['month', 'diff_pct']].round(3).values.tolist()}")
    print("jumps:", jumps)
    print("pub lag days:", lag.describe()[["min", "50%", "max"]].to_dict(), "missing pub:", (out.pub_date == "").sum())
    return out


if __name__ == "__main__":
    main("--refresh" in sys.argv)

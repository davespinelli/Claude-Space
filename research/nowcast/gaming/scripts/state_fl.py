"""Florida monthly slot revenue by pari-mutuel slot facility (Broward & Miami-Dade).

Sources
-------
* Florida Gaming Control Commission (FGCC), Division of Pari-Mutuel Wagering (the division
  moved from DBPR / myfloridalicense.com to FGCC in 2022), statistics page
  https://flgaming.gov/pmw/statistics/  tab "Slot Machine Gaming Revenues":
  one PDF per fiscal year (July-June), "MONTHLY SLOT ACTIVITY PER FACILITY FY yyyy/yyyy",
  https://flgaming.gov/pmw/statistics/docs/slots/SlotRevenues<yyyy>-<yyyy>[--suffix].pdf
  The current-FY file is overwritten each month (FY2026-27 holds Jul+Aug 2026 at build time).
  FY2011-12 and FY2012-13 files are "Revised 2014 June 25" versions (the only ones posted).
* No per-month archive exists, so values are the latest posted vintage of each fiscal year,
  not first-published figures.

Measure
-------
"Net Slot Revenue" per facility per month (credits in - credits out - promotional credits +
30-day unclaimed tickets + winnings withheld from excluded persons = the taxable slot
revenue). measure = "net slot revenue"; slots = ggr; tables blank (pari-mutuel card rooms /
designated-player games are excluded, as instructed). Dollars (whole dollars in the PDFs).
The Seminole Tribe's casinos (Hard Rock etc.) are tribal and NOT reported: this panel covers
only the 8 pari-mutuel "racinos"/slot facilities.
__STATE_TOTAL__ = the PDF's own "TOTAL" block.

Units (unit = facility name as printed, whitespace-normalised, footnote '*' removed; the PDFs
print the name vertically beside each block and the wording changes from year to year).
Renames linked into unit_id (8 facilities, unit_level = property):
  FL_GULFSTREAM     GULFSTREAM / GULFSTREAM PARK / GULFSTREAM PARK RACING AND CASINO
  FL_MARDI_GRAS     MARDI GRAS -> BIG EASY CASINO (Hallandale; closed after Hurricane Irma
                    Sep 2017, reopened as Big Easy May 2018: Oct 2017-Apr 2018 = 0)
  FL_POMPANO        POMPANO / THE ISLE CASINO & RACING AT POMPANO PARK / PPI, INC. D/B/A
                    POMPANO PARK (Isle -> Caesars "Harrah's Pompano Beach"; casino continues)
  FL_MAGIC_CITY     FLAGLER / FLAGLER DOG TRACK & MAGIC CITY CASINO / GRETNA RACING D/B/A MAGIC
                    CITY CASINO (license moved to Gretna Racing 28 Apr 2023, same casino)
  FL_CALDER         CALDER / CALDER CASINO & RACE COURSE / CALDER RACE COURSE
  FL_CASINO_MIAMI   MIAMI JAI ALAI -> CASINO MIAMI (slots began 23 Jan 2012)
  FL_HIALEAH        HIALEAH PARK / HIALEAH PARK CASINO / SOUTH FLORIDA RACING ASSOC ... (from
                    Aug 2013)
  FL_DANIA          DANIA JAI ALAI -> THE CASINO AT DANIA BEACH -> DANIA ENTERTAINMENT CNTR ...
                    (opened Feb 2014; closed for rebuild Nov 2014-Dec 2015 = 0; reopened Jan 2016)
Pre-opening months printed as '-' are dropped (series start at the first positive month).

Month range: 2012-01 .. latest month in the current FY file (2026-08 at build time).

Publication date
----------------
The FY files are overwritten monthly, so a month's first posting date is generally unknown
(Wayback captures of these PDFs are too sparse: 2-5 per file). pub_date is filled only for the
LAST month contained in each FY file, from the PDF's CreationDate metadata when it falls 1-60
days after that month's end (pub_source=pdf_metadata; e.g. June 2026 -> 2026-07-15,
Aug 2026 -> 2026-09-14); all other months are blank (the pre-registered fallback is
month-end + 30 days). Typical lag of the dated months ~2-3 weeks.

Quirks
------
* Layout: facility names are rotated text in the left margin; values are located by position
  (the "Net Slot Revenue" row, numbers assigned to the nearest month-column header).
* COVID closure: all facilities closed 17 Mar 2020 (Apr-May 2020 = 0); Broward reopened
  June 2020, Miami-Dade (Calder, Casino Miami, Hialeah, Magic City) only ~31 Aug 2020, hence the
  ~35x jump into Sep 2020. Other flagged jumps are the openings/closures listed above.
* Page layouts differ by year (portrait 2012-13, pages with /Rotate 90 in FY2015/FY2018, a
  1.54x-scaled page in FY2023, merged header cells in FY2024); FY2015 June also has weekly
  sub-columns (ignored; the June column is used). The parser works in display coordinates on
  word positions and assigns right-aligned numbers to month columns.

Spot checks (data/state_fl_checks.csv.gz):
* all 176 months: sum of facilities vs the PDF's TOTAL block: max |diff| 0.010% (rounding);
* 140 facility-years: sum of the parsed monthly values vs the printed Y-T-D Total column:
  max |diff| 0.018% (rounding) -> no month is mis-assigned or missing.

Run: python3 scripts/state_fl.py [--refresh]  (--refresh re-downloads the statistics page and
the current fiscal-year PDF, which is overwritten monthly; older PDFs are never re-downloaded).
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

import pandas as pd
import requests

ROOT = Path("/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming")
CACHE = ROOT / "cache" / "fl"
DATA = ROOT / "data"
CACHE.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)

PAGE = "https://flgaming.gov/pmw/statistics/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
START = "2012-01"
_last: dict[str, float] = {}
MONTHS = ["JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY",
          "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE"]


def fetch(url: str, fname: str, min_interval: float = 0.6, force: bool = False) -> Path | None:
    path = CACHE / fname
    if path.exists() and path.stat().st_size > 0 and not force:
        return path
    host = urlparse(url).netloc
    for attempt in range(5):
        wait = min_interval - (time.time() - _last.get(host, 0.0))
        if wait > 0:
            time.sleep(wait)
        _last[host] = time.time()
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=90)
        except requests.RequestException:
            time.sleep(3 * 2 ** attempt)
            continue
        if r.status_code == 200 and r.content:
            if fname.endswith(".pdf") and not r.content.startswith(b"%PDF"):
                return None
            path.write_bytes(r.content)
            return path
        if r.status_code in (403, 404, 410):
            return None
        time.sleep(3 * 2 ** attempt)
    return None


UNIT_MAP = [
    (r"GULFSTREAM", "FL_GULFSTREAM"),
    (r"MARDI|BIG EASY", "FL_MARDI_GRAS"),
    (r"POMPANO", "FL_POMPANO"),
    (r"FLAGLER|MAGIC CITY|GRETNA", "FL_MAGIC_CITY"),
    (r"CALDER", "FL_CALDER"),
    (r"JAI ALAI.*MIAMI|MIAMI JAI|CASINO MIAMI", "FL_CASINO_MIAMI"),
    (r"HIALEAH", "FL_HIALEAH"),
    (r"DANIA", "FL_DANIA"),
]


def unit_id(name: str) -> str:
    u = name.upper()
    for pat, uid in UNIT_MAP:
        if re.search(pat, u):
            return uid
    raise ValueError(f"unmapped FL facility {name!r}")


def _num(t: str) -> float | None:
    t = t.strip().replace("$", "")
    if t in ("-", "--", "–"):
        return 0.0
    m = re.fullmatch(r"\(?-?[\d,]+(\.\d+)?\)?", t)
    if not m:
        return None
    v = float(re.sub(r"[^\d.]", "", t))
    return -v if t.startswith(("(", "-")) else v


def parse_fy_pdf(path: Path, fy_end: int) -> tuple[list[dict], dict]:
    """Return rows [{name, month, value}] (name 'TOTAL' for the statewide block) and meta."""
    import pymupdf
    doc = pymupdf.open(str(path))
    out, ytd = [], []
    for page in doc:
        # all geometry in display coordinates (some years' pages carry /Rotate 90)
        M = page.rotation_matrix
        k = max(page.rect.width, page.rect.height) / 792.0  # FY2023 file is drawn at 1.54x
        # rotated (vertical) lines = facility names in the left margin
        rot = []
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(sp["text"] for sp in ln["spans"])
                dx, dy = ln["dir"]
                ddx = dx * M.a + dy * M.c  # direction in display space
                if t.strip() and abs(ddx) < 0.5:
                    r = pymupdf.Rect(ln["bbox"]) * M
                    rot.append(dict(t=t.strip(), x0=r.x0, x1=r.x1, y0=r.y0, y1=r.y1,
                                    yc=(r.y0 + r.y1) / 2))
        # horizontal words (header cells can be merged into one text line, so use words)
        words = []
        for (x0, y0, x1, y1, w, bno, lno, wno) in page.get_text("words"):
            r = pymupdf.Rect(x0, y0, x1, y1) * M
            xc, yc = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            if any(q["x0"] - 1 <= xc <= q["x1"] + 1 and q["y0"] - 1 <= yc <= q["y1"] + 1 for q in rot):
                continue
            words.append(dict(t=w, x0=r.x0, x1=r.x1, xc=xc, yc=yc, key=(bno, lno), wno=wno))
        # block anchors: the 'Y-T-D Total' column header (not 'Y-T-D Average Payout ...')
        anc = []
        tots = [w for w in words if w["t"].upper() == "TOTAL"]
        for w in sorted(words, key=lambda w: w["yc"]):
            if w["t"].upper() != "Y-T-D":
                continue
            ok = any((abs(t["yc"] - w["yc"]) < 3 * k and 0 < t["x0"] - w["x1"] < 20 * k) or
                     (abs(t["xc"] - w["xc"]) < 15 * k and 0 < t["yc"] - w["yc"] < 9 * k)
                     for t in tots)
            if ok and (not anc or w["yc"] - anc[-1] > 5 * k):
                anc.append(w["yc"])
        bottoms = [a - 20 * k for a in anc[1:]] + [page.rect.height]
        for a, bot in zip(anc, bottoms):
            top = a - 20 * k
            heads = {}
            for w in words:
                if a - 10 * k <= w["yc"] <= a + 6 * k and w["t"].upper() in MONTHS:
                    heads[w["t"].upper()] = w["xc"]
            if not heads:
                continue
            lab = None
            for w in words:
                if top <= w["yc"] < bot and w["t"].upper() == "NET":
                    nxt = [v for v in words if v["key"] == w["key"] and v["wno"] in (w["wno"] + 1,
                                                                                     w["wno"] + 2)]
                    if [v["t"].upper() for v in sorted(nxt, key=lambda v: v["wno"])] == ["SLOT", "REVENUE"]:
                        lab = dict(yc=w["yc"], x1=max(v["x1"] for v in nxt))
                        break
            if lab is None:
                continue
            # pseudo-columns whose values must be dropped: the Y-T-D total and (FY2015 June)
            # weekly sub-columns headed by dates
            pseudo = [("__YTD__" if w["t"].upper() == "Y-T-D" else None, w["xc"]) for w in words
                      if a - 10 * k <= w["yc"] <= a + 14 * k and
                      (w["t"].upper() == "Y-T-D" or re.fullmatch(r"\d{2}/\d{2}/\d{4}", w["t"]))]
            cols = list(heads.items()) + pseudo
            row = [w for w in words if abs(w["yc"] - lab["yc"]) < 3.5 * k and w["x0"] > lab["x1"] - 1
                   and _num(w["t"]) is not None]
            wide = sorted(w["x1"] - w["x0"] for w in row if len(w["t"]) >= 7)
            half = wide[len(wide) // 2] / 2 if wide else 0
            vals = {}
            for w in row:
                # numbers are right-aligned: narrow tokens ('-', '2,654') are centred as if
                # they had the row's typical width
                eff = w["xc"] if len(w["t"]) >= 7 or not half else w["x1"] - half
                mname, xc = min(cols, key=lambda kv: abs(kv[1] - eff))
                if mname is None or abs(xc - eff) > 30 * k:
                    continue
                if mname in vals:
                    raise ValueError(f"two values for {mname} in {path.name}")
                vals[mname] = _num(w["t"])
            names = sorted([r for r in rot if top <= r["yc"] < bot], key=lambda r: r["x0"])
            name = re.sub(r"\s+", " ", " ".join(r["t"] for r in names).replace("*", " ")).strip()
            if not name:
                raise ValueError(f"no facility name for block at y={a:.0f} in {path.name}")
            if "__YTD__" in vals:
                ytd.append(dict(name=name, ytd=vals.pop("__YTD__"),
                                sum_months=sum(v for m_, v in vals.items() if m_ in heads)))
            for mname in heads:
                if mname not in vals:
                    continue  # blank cell: facility not yet operating (e.g. before opening)
                mi = MONTHS.index(mname)
                yr = fy_end - 1 if mi < 6 else fy_end
                cal = (mi + 6) % 12 + 1
                out.append(dict(name=name, month=f"{yr}-{cal:02d}", value=vals[mname]))
    md = dict(doc.metadata or {})
    md["ytd"] = ytd
    return out, md


def main(refresh: bool = False) -> None:
    page = fetch(PAGE, "fgcc_statistics.html", force=refresh)
    html = page.read_text(encoding="utf-8", errors="ignore")
    files = {}
    for href in re.findall(r'href="(docs/slots/SlotRevenues[^"]+\.pdf)"', html, re.I):
        name = unquote(href.split("/")[-1])
        m = re.match(r"SlotRevenues\s*(\d{4})-(\d{4})", name, re.I)
        if not m:
            continue
        fy_end = int(m.group(2))
        if fy_end < 2012:
            continue
        files[fy_end] = (PAGE + quote(href), name.replace(" ", "_"))
    cur_fy = max(files)
    rows, totals, meta, ytd_checks = [], [], {}, []
    for fy_end in sorted(files):
        url, cname = files[fy_end]
        path = fetch(url, cname, force=refresh and fy_end == cur_fy)
        if path is None:
            print("  could not download", url)
            continue
        recs, md = parse_fy_pdf(path, fy_end)
        months_in = sorted({r["month"] for r in recs})
        cd = md.get("creationDate", "")
        m = re.match(r"D:(\d{4})(\d{2})(\d{2})", cd)
        created = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None
        meta[fy_end] = (months_in[-1] if months_in else None, created, cname)
        for y in md["ytd"]:
            ytd_checks.append(dict(month=months_in[-1], sum_of_units=y["sum_months"],
                                   regulator_total=y["ytd"],
                                   diff_pct=(y["sum_months"] - y["ytd"]) / y["ytd"] * 100
                                   if y["ytd"] else None,
                                   note=f"FY{fy_end} {y['name']}: sum of monthly values vs printed "
                                        f"Y-T-D Total ({cname})"))
        for r in recs:
            if r["month"] < START:
                continue
            if r["name"].upper().strip() == "TOTAL":
                totals.append(dict(month=r["month"], ggr=r["value"], source_file=cname))
            else:
                rows.append(dict(state="FL", unit=r["name"], unit_id=unit_id(r["name"]),
                                 unit_level="property", month=r["month"], ggr=r["value"],
                                 slots=r["value"], tables=None, n_casinos=None,
                                 measure="net slot revenue", source_file=cname))
        print(f"  FY{fy_end}: {len(recs)} values, months {months_in[:1]}..{months_in[-1:]}, "
              f"created {created}")
    pub = {}
    for fy_end, (last_m, created, cname) in meta.items():
        if last_m and created:
            me = (pd.Timestamp(last_m + "-01") + pd.offsets.MonthEnd(0)).date()
            if 1 <= (created - me).days <= 60:
                pub[last_m] = created.isoformat()
    df = pd.DataFrame(rows)
    # months before a facility's first revenue are printed as '-' in its first fiscal year:
    # drop those pre-opening zeros (closures after opening stay as 0)
    first_pos = df[df.ggr > 0].groupby("unit_id").month.min()
    df = df[df.month >= df.unit_id.map(first_pos)]
    tt = pd.DataFrame(totals)
    n = df.groupby("month").unit_id.nunique()
    tt = tt.assign(state="FL", unit="__STATE_TOTAL__", unit_id="FL__STATE_TOTAL__",
                   unit_level="state_total", slots=None, tables=None,
                   n_casinos=tt.month.map(n), measure="net slot revenue")
    df = pd.concat([df, tt], ignore_index=True)
    df["pub_date"] = df.month.map(pub).fillna("")
    df["pub_source"] = df.pub_date.map(lambda x: "pdf_metadata" if x else "")
    cols = ["state", "unit", "unit_id", "unit_level", "month", "ggr", "slots", "tables",
            "n_casinos", "measure", "pub_date", "pub_source", "source_file"]
    df = df[cols].sort_values(["month", "unit_level", "unit_id"]).reset_index(drop=True)
    dup = df[df.duplicated(["unit_id", "month"], keep=False)]
    if len(dup):
        print(dup.to_string())
        raise SystemExit("duplicate unit_id-month rows")

    prop = df[df.unit_level == "property"]
    s = prop.groupby("month").ggr.sum()
    ck = []
    for _, r in df[df.unit_level == "state_total"].iterrows():
        ck.append(dict(month=r.month, sum_of_units=s.get(r.month), regulator_total=r.ggr,
                       diff_pct=(s.get(r.month) - r.ggr) / r.ggr * 100 if r.ggr else None,
                       note=f"vs TOTAL block of {r.source_file}"))
    ck = pd.DataFrame(ck)
    yc = pd.DataFrame(ytd_checks)
    print(f"Y-T-D column checks: {len(yc)} facility-years, max |diff| "
          f"{yc.diff_pct.abs().max():.4f}%")
    ck = pd.concat([ck, yc], ignore_index=True).sort_values(["month", "note"])
    ck.to_csv(DATA / "state_fl_checks.csv.gz", index=False)
    print(f"checks: {len(ck)} rows, max |diff| {ck.diff_pct.abs().max():.4f}%")
    big = ck[ck.diff_pct.abs() > 1]
    if len(big):
        print(big.to_string())
    covid = {"2020-03", "2020-04", "2020-05", "2020-06", "2020-07"}
    for uid, g in prop.sort_values("month").groupby("unit_id"):
        g = g.set_index("month")["ggr"]
        r = g / g.shift(1)
        bad = r[((r > 3) | (r < 1 / 3)) & ~r.index.isin(covid)]
        if len(bad):
            print("  jump", uid, {k: round(v, 2) for k, v in bad.items()})
        idx = [p.strftime("%Y-%m") for p in pd.period_range(g.index.min(), g.index.max(), freq="M")]
        gaps = [m for m in idx if m not in g.index]
        if gaps:
            print("  gap months", uid, gaps)
    df.to_csv(DATA / "state_fl.csv.gz", index=False)
    print(f"wrote {len(df)} rows; months {df.month.min()}..{df.month.max()}; units "
          f"{prop.unit_id.nunique()}; pub_date for {len(pub)} months: {pub}")
    print(prop.groupby("unit_id").agg(first=("month", "min"), last=("month", "max"),
                                      n=("month", "size"),
                                      names=("unit", lambda x: sorted(set(x)))).to_string())


if __name__ == "__main__":
    main(refresh="--refresh" in sys.argv)

"""Iowa (IA) monthly casino revenue by property, 2012-01 onward.

Output: data/state_ia.csv.gz, data/state_ia_checks.csv.gz (spec: scripts/STATE_DATA_SPEC.txt).
Run:    python3 state_ia.py            (downloads what is not cached, parses, writes)
        python3 state_ia.py --no-download

SOURCES (Iowa Racing and Gaming Commission, IRGC)
  https://irgc.iowa.gov/publications-reports/gaming-revenue            (current FY: monthly PDFs)
  https://irgc.iowa.gov/publications-reports/gaming-revenue/archived-gaming-revenue  (one PDF per
     fiscal year, "Fiscal Year YYYY Gaming Revenue", /media/<id>/download)
  https://irgc.iowa.gov/general-information/newsroom  (monthly "<Month> <Year> Revenue Information"
     releases; used only for pub_date)
  Files cached in cache/ia/ as FY2012.pdf .. FY2026.pdf, month_2026-07.pdf, month_2026-08.pdf.
  Each fiscal-year PDF (Jul-Jun) holds, for every month, a revenue summary (one column per casino,
  rows = AGR, admissions, table drop/revenue, slot coin-in/revenue, taxes) plus game/denomination
  detail pages. FY months are mapped to calendar months from each page title ("-- JULY 2011").
  FY2012-FY2014 have separate "TRACK" (racino) and "RIVERBOAT" pages, some drawn rotated 90 degrees
  (coordinates are rotated back) and in FY2014 several track pages carry a wrong title
  ("TRACKS TABLE REVENUE BY GAME"), so pages are recognised by their "ADJUSTED GROSS REVENUE" row,
  not by title. Columns are located from the positions of the AGR values; casino names are the
  header text above each column (merged header spans are split into words).

MEASURE (ggr) = ADJUSTED GROSS REVENUE (table revenue + slot revenue, published), dollars.
  tables = TABLE REVENUE, slots = SLOT REVENUE (sum = AGR in every row). Sports wagering is reported
  separately by IRGC and excluded. MEASURE BREAK: from 2026-07 IRGC's AGR no longer includes
  promotional (free) play (end of the SF619 phase-out that began in FY2022); the measure column says
  "AGR (excl. promotional play)" for 2026-07+ and "AGR" before. The August 2026 release puts the
  statewide effect at -13.1% y/y, so 2026-07/08 y/y growth is NOT comparable with earlier years.
  Values are those in the latest issue of each fiscal-year file, i.e. they include the corrections
  listed on the FY "Amendments" pages (e.g. Dec-2025 table/slot split of Grand Falls and Rhythm City),
  not necessarily the first-published figures.

MONTHS 2012-01 .. 2026-08 (176, none missing). COVID: casinos closed 2020-03-17 .. 2020-05-31; IRGC
  printed 0 for 2020-04 and 2020-05 (kept); Harrah's Council Bluffs stayed closed in 2020-06 (0).

UNITS (20 property ids; renames linked in UNIT_ID)
  Isle of Capri - Marquette -> Lady Luck -> Casino Queen - Marquette -> Bally's Marquette (2026-03);
  Catfish Bend Casino -> Great River Casino Resort (Burlington, 2026-05); Mystique Casino -> Q Casino
  (Dubuque greyhound park); Horseshoe Casino and Bluffs Run Greyhound Park -> Horseshoe Casino Council
  Bluffs; Terrible's Lakeside -> Lakeside Casino (Osceola); The Isle Casino & Hotel at Waterloo ->
  Isle Casino Hotel Waterloo; Diamond Jo -> Diamond Jo - Dubuque; 'Riverside ... LLC' -> Riverside.
  NOT linked: Argosy - Sioux City (last month 2014-07) and Hard Rock Casino (Sioux City; first month
  2014-07 with $9k pre-opening, opened 2014-08). Wild Rose - Jefferson first month 2015-07.

PUBLICATION DATE
  press_release: date in the IRGC newsroom URL of "<Month> <Year> Revenue Information" (June figures:
  the fiscal-year release). The current IRGC site only carries these for 2026-01 .. 2026-08
  (lags 9-28 days, median ~16); earlier months are blank (no dated listing survives on the site; FY
  PDFs are re-issued cumulatively and HTTP Last-Modified reflects a 2023 re-upload, so not used).

CHECKS (data/state_ia_checks.csv.gz, all months)
  sum of property AGR vs the published statewide "Totals" column (2014-07+) or the sum of the
  published riverboat "TOTAL" + track "TOTALS" columns (2012-01 .. 2014-06): max |diff| 0.00%,
  176/176 months. tables + slots = AGR for every row. Aug 2026 total $131.37M matches the IRGC
  press release. Jump scan (m/m >3x or <1/3 outside Mar-Jul 2020): only Hard Rock Sioux City
  opening (2014-08). No duplicate (unit_id, month). Unknown casino names raise an error.
"""
import os, re, sys, time, glob, collections, datetime as dt
import requests
import pandas as pd
import numpy as np

ROOT = "/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming"
CACHE = os.path.join(ROOT, "cache", "ia")
DATA = os.path.join(ROOT, "data")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
BASE = "https://irgc.iowa.gov"
LISTINGS = {"current": BASE + "/publications-reports/gaming-revenue",
            "archive": BASE + "/publications-reports/gaming-revenue/archived-gaming-revenue"}
NEWSROOM = BASE + "/general-information/newsroom"
MONTHS = {m.upper(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
     "November", "December"], 1)}

# Regulator column header (upper, footnote marks removed, whitespace-normalised) -> stable unit_id.
UNIT_ID = {
    "AMERISTAR II": "IA_AMERISTAR_COUNCIL_BLUFFS",
    "ISLE OF CAPRI - MARQUETTE": "IA_MARQUETTE", "LADY LUCK CASINO MARQUETTE": "IA_MARQUETTE",
    "CASINO QUEEN - MARQUETTE": "IA_MARQUETTE", "CASINO QUEEN MARQUETTE": "IA_MARQUETTE",
    "BALLY'S MARQUETTE": "IA_MARQUETTE",
    "DIAMOND JO": "IA_DIAMOND_JO_DUBUQUE", "DIAMOND JO - DUBUQUE": "IA_DIAMOND_JO_DUBUQUE",
    "DIAMOND JO DUBUQUE": "IA_DIAMOND_JO_DUBUQUE",
    "DIAMOND JO - WORTH": "IA_DIAMOND_JO_WORTH", "DIAMOND JO WORTH": "IA_DIAMOND_JO_WORTH",
    "WILD ROSE - CLINTON": "IA_WILD_ROSE_CLINTON", "WILD ROSE CLINTON": "IA_WILD_ROSE_CLINTON",
    "WILD ROSE - EMMETSBURG": "IA_WILD_ROSE_EMMETSBURG", "WILD ROSE EMMETSBURG": "IA_WILD_ROSE_EMMETSBURG",
    "WILD ROSE - JEFFERSON": "IA_WILD_ROSE_JEFFERSON", "WILD ROSE JEFFERSON": "IA_WILD_ROSE_JEFFERSON",
    "CATFISH BEND CASINO": "IA_BURLINGTON", "CATFISH BEND CASINOS": "IA_BURLINGTON",
    "GREAT RIVER CASINO RESORT": "IA_BURLINGTON",
    "ARGOSY - SIOUX CITY": "IA_ARGOSY_SIOUX_CITY", "ARGOSY CASINO SIOUX CITY": "IA_ARGOSY_SIOUX_CITY",
    "HARD ROCK CASINO": "IA_HARD_ROCK_SIOUX_CITY", "HARD ROCK HOTEL & CASINO": "IA_HARD_ROCK_SIOUX_CITY",
    "HARD ROCK HOTEL & CASINO SIOUX CITY": "IA_HARD_ROCK_SIOUX_CITY",
    "TERRIBLE'S LAKESIDE CASINO": "IA_LAKESIDE_OSCEOLA", "LAKESIDE CASINO": "IA_LAKESIDE_OSCEOLA",
    "LAKESIDE HOTEL CASINO": "IA_LAKESIDE_OSCEOLA",
    "THE ISLE CASINO & HOTEL AT WATERLOO": "IA_ISLE_WATERLOO", "ISLE CASINO HOTEL WATERLOO": "IA_ISLE_WATERLOO",
    "ISLE CASINO HOTEL - WATERLOO": "IA_ISLE_WATERLOO",
    "RHYTHM CITY CASINO": "IA_RHYTHM_CITY_DAVENPORT", "RHYTHM CITY CASINO RESORT": "IA_RHYTHM_CITY_DAVENPORT",
    "ISLE OF CAPRI - BETTENDORF": "IA_ISLE_BETTENDORF", "ISLE CASINO HOTEL BETTENDORF": "IA_ISLE_BETTENDORF",
    "ISLE CASINO HOTEL - BETTENDORF": "IA_ISLE_BETTENDORF",
    "HARRAHS COUNCIL BLUFFS CASINO & HOTEL": "IA_HARRAHS_COUNCIL_BLUFFS",
    "HARRAH'S COUNCIL BLUFFS CASINO & HOTEL": "IA_HARRAHS_COUNCIL_BLUFFS",
    "RIVERSIDE CASINO AND GOLF RESORT LLC": "IA_RIVERSIDE", "RIVERSIDE CASINO AND GOLF RESORT": "IA_RIVERSIDE",
    "GRAND FALLS CASINO RESORT": "IA_GRAND_FALLS", "GRAND FALLS CASINO": "IA_GRAND_FALLS",
    "PRAIRIE MEADOWS RACETRACK & CASINO": "IA_PRAIRIE_MEADOWS",
    "HORSESHOE CASINO AND BLUFFS RUN GREYHOUND PARK": "IA_HORSESHOE_COUNCIL_BLUFFS",
    "HORSESHOE CASINO COUNCIL BLUFFS": "IA_HORSESHOE_COUNCIL_BLUFFS",
    "HORSESHOE COUNCIL BLUFFS": "IA_HORSESHOE_COUNCIL_BLUFFS",
    "MYSTIQUE CASINO": "IA_Q_CASINO_DUBUQUE", "Q CASINO": "IA_Q_CASINO_DUBUQUE",
    "Q CASINO + HOTEL": "IA_Q_CASINO_DUBUQUE",
    "LADY LUCK": "IA_MARQUETTE",
    "HORSESHOE CASINO/BLUFFS RUN GREYHOUND PARK": "IA_HORSESHOE_COUNCIL_BLUFFS",
    "HORSESHOE CASINO- BLUFFS RUN GREYHOUND PARK": "IA_HORSESHOE_COUNCIL_BLUFFS",
    "HORSESHOE CASINO - BLUFFS RUN GREYHOUND PARK": "IA_HORSESHOE_COUNCIL_BLUFFS",
}
TOTAL_LABELS = {"TOTAL", "TOTALS"}


def log(*a):
    print(*a, file=sys.stderr)


# ------------------------------------------------------------------ download
def _get(url, dest, min_size=500, refresh=False):
    if not refresh and os.path.exists(dest) and os.path.getsize(dest) >= min_size:
        return dest
    for k in range(5):
        try:
            r = requests.get(url, headers=UA, timeout=120)
            if r.status_code == 200 and len(r.content) >= min_size:
                open(dest, "wb").write(r.content)
                time.sleep(0.6)
                return dest
            log("status", r.status_code, url)
            if r.status_code == 404:
                return None
        except Exception as e:
            log("err", e, url)
        time.sleep(2 ** k)
    return None


def listing_links():
    """(label, media_url) pairs from the IRGC gaming revenue pages."""
    out = []
    for key in ("current", "archive"):
        h = open(os.path.join(CACHE, f"listing_{key}.html"), encoding="utf-8", errors="ignore").read()
        out += re.findall(r'aria-label="([^"]+)"\s+href="(/media/\d+/download[^"]*)"', h)
    return [(re.sub(r"\s+", " ", a).strip(), u) for a, u in out]


def file_name_for(label):
    m = re.match(r"Fiscal Year (\d{4}) Gaming Revenue", label)
    if m:
        return f"FY{m.group(1)}.pdf"
    m = re.match(r"(\w+) (\d{4}) Gaming Revenue", label)
    if m and m.group(1).upper() in MONTHS:
        return f"month_{m.group(2)}-{MONTHS[m.group(1).upper()]:02d}.pdf"
    m = re.match(r"FYTD (\d{4}) Gaming Revenue", label)
    if m:
        return f"FYTD{m.group(1)}.pdf"
    if "Amendments" in label:
        return "FY_amendments_" + re.sub(r"\W+", "_", label).strip("_") + ".pdf"
    return None


def download():
    os.makedirs(CACHE, exist_ok=True)
    for key, u in LISTINGS.items():
        _get(u, os.path.join(CACHE, f"listing_{key}.html"), min_size=1000, refresh=(key == "current"))
    for label, u in listing_links():
        fn = file_name_for(label)
        if not fn:
            continue
        m = re.match(r"FY(\d{4})\.pdf", fn)
        if m and int(m.group(1)) < 2012:
            continue
        _get(BASE + u, os.path.join(CACHE, fn), min_size=1000)  # data files: cached, never re-downloaded
    # newsroom (monthly '<Month> <Year> Revenue Information' releases give the publication date; the
    # current IRGC site only carries releases from 2026 on). Index pages are refreshed each run.
    for page in range(0, 10):
        fn = os.path.join(CACHE, f"newsroom_p{page}.html")
        url = NEWSROOM if page == 0 else NEWSROOM + f"?page={page}"
        if not _get(url, fn, min_size=1000, refresh=True):
            break
        if "/news-release/" not in open(fn, encoding="utf-8", errors="ignore").read():
            os.remove(fn)
            break


# ------------------------------------------------------------------ parsing
MONEY = re.compile(r"^\(?-?\$\s*-?[\d,]+(\.\d+)?\)?$")
JUNK = {"TEST", "TEXT36:", "IOWA RACING AND GAMING COMMISSION"}


def money(s):
    s = s.strip()
    neg = s.startswith("(") or s.startswith("-") or "-$" in s
    v = float(re.sub(r"[^\d.]", "", s))
    return -v if neg else v


def norm_name(s):
    s = re.sub(r"[¹²³⁰-⁹*]", "", s)
    s = s.replace("’", "'")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+-$", " -", s)
    return s


def page_spans(page):
    """Spans and words of a page in a normalised reading frame (text runs left->right).
    Some IRGC pages (FY2012-FY2014 riverboat pages) are drawn rotated; we rotate coordinates back."""
    d = page.get_text("dict")
    raw, dirs = [], collections.Counter()
    for b in d["blocks"]:
        for l in b.get("lines", []):
            dr = (round(l["dir"][0]), round(l["dir"][1]))
            dirs[dr] += 1
            for s in l["spans"]:
                t = s["text"].replace("\u00ad", "-").strip()
                if t:
                    raw.append((t, s["bbox"]))
    words = [(w[4].replace("\u00ad", "-"), w[:4]) for w in page.get_text("words")]
    dom = dirs.most_common(1)[0][0] if dirs else (1, 0)
    H = max((b[3] for _, b in raw), default=0) + 10
    W = max((b[2] for _, b in raw), default=0) + 10

    def tr(items):
        out = []
        for t, (x0, y0, x1, y1) in items:
            if dom == (0, -1):
                x0, y0, x1, y1 = H - y1, x0, H - y0, x1
            elif dom == (0, 1):
                x0, y0, x1, y1 = y0, W - x1, y1, W - x0
            out.append(dict(t=t, x0=x0, y0=y0, x1=x1, y1=y1, xc=(x0 + x1) / 2, yc=(y0 + y1) / 2))
        return out
    return tr(raw), tr(words)


def page_month(spans):
    for s in spans:
        m = re.search(r"--\s*([A-Z]+)\s+(\d{4})", s["t"].upper())
        if m and m.group(1) in MONTHS:
            return f"{m.group(2)}-{MONTHS[m.group(1)]:02d}"
        if re.search(r"--\s*FYTD", s["t"].upper()):
            return "FYTD"
    return None


def row_values(spans, label_span, cols, tol=3.0):
    vals = [s for s in spans if abs(s["yc"] - label_span["yc"]) < tol and s["x0"] > label_span["x1"]
            and MONEY.match(s["t"])]
    out = {}
    for v in vals:
        j = int(np.argmin([abs(v["xc"] - c) for c in cols]))
        if abs(v["xc"] - cols[j]) < 30:
            out[j] = money(v["t"])
    return out


def parse_page(spans, words):
    """Return list of dict(name, agr, tables, slots) for every column of every section on the page."""
    res = []
    agr_labels = sorted([s for s in spans if s["t"].upper() == "ADJUSTED GROSS REVENUE"], key=lambda s: s["yc"])
    for k, lab in enumerate(agr_labels):
        y_next = agr_labels[k + 1]["yc"] if k + 1 < len(agr_labels) else 1e9
        vals = sorted([s for s in spans if abs(s["yc"] - lab["yc"]) < 3 and s["x0"] > lab["x1"]
                       and MONEY.match(s["t"])], key=lambda s: s["xc"])
        cols = [v["xc"] for v in vals]
        if not cols:
            continue
        agr = {j: money(v["t"]) for j, v in enumerate(vals)}

        def find(label):
            c = [s for s in spans if s["t"].upper() == label and lab["yc"] < s["yc"] < y_next]
            return min(c, key=lambda s: s["yc"]) if c else None
        tl, sl = find("TABLE REVENUE"), find("SLOT REVENUE")
        tv = row_values(spans, tl, cols) if tl else {}
        sv = row_values(spans, sl, cols) if sl else {}
        # header: non-numeric spans just above the AGR row, over the value columns
        spacing = np.median(np.diff(cols)) if len(cols) > 1 else 80
        title_y = [t["yc"] for t in spans if "--" in t["t"]]

        def is_hdr(w):
            return (lab["yc"] - 70 < w["yc"] < lab["yc"] - 2 and w["xc"] > lab["x1"] - 5
                    and not any(abs(w["yc"] - ty) < 4 for ty in title_y)
                    and not MONEY.match(w["t"]) and w["t"].upper() not in JUNK
                    and not re.match(r"^[\d,.%$]+$", w["t"]) and (len(w["t"]) > 1 or w["t"] in "&-"))
        hdr = [h for h in spans if is_hdr(h)]
        # header cells are centred, values right-aligned: estimate the offset from single-cell header spans
        offs = []
        for h in hdr:
            if h["x1"] - h["x0"] <= spacing:
                j = int(np.argmin([abs(h["xc"] - c) for c in cols]))
                if abs(h["xc"] - cols[j]) < spacing * 0.6:
                    offs.append(h["xc"] - cols[j])
        off = float(np.median(offs)) if offs else 0.0
        ccols = [c + off for c in cols]
        pieces = []
        for h in hdr:
            if h["x1"] - h["x0"] <= spacing * 1.02:
                pieces.append(h)
            else:  # one text span covering several header cells: split into words
                pieces += [w for w in words if is_hdr(w) and h["x0"] - 1 <= w["xc"] <= h["x1"] + 1
                           and h["y0"] - 1 <= w["yc"] <= h["y1"] + 1]
        names = collections.defaultdict(list)
        for w in pieces:
            j = int(np.argmin([abs(w["xc"] - c) for c in ccols]))
            if abs(w["xc"] - ccols[j]) < spacing * 0.6:
                names[j].append(w)
        for j in range(len(cols)):
            nm = " ".join(w["t"] for w in sorted(names.get(j, []), key=lambda w: (round(w["yc"] / 3), w["x0"])))
            res.append(dict(name=norm_name(nm), agr=agr[j], tables=tv.get(j), slots=sv.get(j)))
    return res


def parse_pdf(path):
    import pymupdf
    d = pymupdf.open(path)
    out = collections.defaultdict(list)
    for p in d:
        sp, wd = page_spans(p)
        mo = page_month(sp)
        if mo is None or mo == "FYTD":
            continue
        for r in parse_page(sp, wd):
            out[mo].append(r)
    return out


def news_dates():
    """month -> press-release date from the IRGC newsroom ('<Month> <Year> Revenue Information')."""
    res = {}
    for fn in glob.glob(os.path.join(CACHE, "newsroom_p*.html")):
        h = open(fn, encoding="utf-8", errors="ignore").read()
        for d, slug in re.findall(r'href="/news-release/(\d{4}-\d{2}-\d{2})/([a-z]+-\d{4})-revenue-information"', h):
            mname, yr = slug.rsplit("-", 1)
            if mname.upper() in MONTHS:
                res[f"{yr}-{MONTHS[mname.upper()]:02d}"] = d
        # June figures are released with the fiscal-year summary release
        for d, fy in re.findall(r'href="/news-release/(\d{4}-\d{2}-\d{2})/[^"]*fiscal-year-(\d{4})"', h):
            res.setdefault(f"{fy}-06", d)
    return res


def uid_for(name):
    k = name.upper()
    if k in UNIT_ID:
        return UNIT_ID[k]
    raise KeyError(f"unmapped IA unit {name!r}")


def build():
    files = sorted(glob.glob(os.path.join(CACHE, "FY20*.pdf"))) + sorted(glob.glob(os.path.join(CACHE, "month_*.pdf")))
    by_month = {}
    for f in files:
        parsed = parse_pdf(f)
        for mo, rows in parsed.items():
            if mo < "2012-01":
                continue
            # later files (monthly files after FY files) override; FY files are cumulative re-issues
            by_month[mo] = (rows, os.path.basename(f))
    nd = news_dates()
    recs, notes = [], {}
    for mo, (rows, src) in sorted(by_month.items()):
        measure = "AGR" if mo < "2026-07" else "AGR (excl. promotional play)"
        pub = nd.get(mo, "")
        psrc = "press_release" if pub else ""
        tot_rows = [r for r in rows if r["name"].upper() in TOTAL_LABELS]
        props = [r for r in rows if r["name"].upper() not in TOTAL_LABELS]
        seen = set()
        for r in props:
            uid = uid_for(r["name"])
            if uid in seen:
                raise ValueError(f"duplicate {uid} in {mo}")
            seen.add(uid)
            recs.append(dict(state="IA", unit=r["name"], unit_id=uid, unit_level="property", month=mo,
                             ggr=r["agr"], slots=r["slots"], tables=r["tables"], n_casinos=np.nan,
                             measure=measure, pub_date=pub, pub_source=psrc, source_file=src))
        if tot_rows:
            g = sum(r["agr"] for r in tot_rows)
            t = sum(r["tables"] for r in tot_rows) if all(r["tables"] is not None for r in tot_rows) else np.nan
            s = sum(r["slots"] for r in tot_rows) if all(r["slots"] is not None for r in tot_rows) else np.nan
            recs.append(dict(state="IA", unit="__STATE_TOTAL__", unit_id="IA___STATE_TOTAL__",
                             unit_level="state_total", month=mo, ggr=g, slots=s, tables=t,
                             n_casinos=float(len(props)), measure=measure, pub_date=pub, pub_source=psrc,
                             source_file=src))
            notes[mo] = ("sum of published riverboat TOTAL + track TOTALS columns" if len(tot_rows) == 2
                         else "published statewide Totals column")
        else:
            log("no total column", mo)
    df = pd.DataFrame(recs)
    return df, notes


def checks_and_write(df, notes):
    props = df[df.unit_level == "property"]
    tot = df[df.unit_level == "state_total"].set_index("month")["ggr"]
    s = props.groupby("month")["ggr"].sum()
    ck = pd.DataFrame({"month": s.index, "sum_of_units": s.values, "regulator_total": tot.reindex(s.index).values})
    with np.errstate(divide="ignore", invalid="ignore"):
        ck["diff_pct"] = np.where(ck.regulator_total != 0, (ck.sum_of_units / ck.regulator_total - 1) * 100, 0.0)
    ck["note"] = ck.month.map(notes).fillna("")
    # components: tables + slots should equal AGR
    comp = props.dropna(subset=["tables", "slots"])
    bad = comp[(comp.tables + comp.slots - comp.ggr).abs() > 2]
    jumps = []
    for uid, g in props.sort_values("month").groupby("unit_id"):
        g = g.set_index("month")["ggr"]
        r = g / g.shift(1)
        for mo, v in r.items():
            if "2020-03" <= mo <= "2020-07":
                continue
            if pd.notna(v) and np.isfinite(v) and (v > 3 or v < 1 / 3):
                jumps.append((uid, mo, round(float(v), 3)))
    dup = df.duplicated(["unit_id", "month"]).sum()
    assert dup == 0, f"{dup} duplicate (unit_id, month)"
    cols = ["state", "unit", "unit_id", "unit_level", "month", "ggr", "slots", "tables", "n_casinos",
            "measure", "pub_date", "pub_source", "source_file"]
    os.makedirs(DATA, exist_ok=True)
    df[cols].sort_values(["month", "unit_level", "unit_id"]).to_csv(
        os.path.join(DATA, "state_ia.csv.gz"), index=False, compression="gzip")
    ck.to_csv(os.path.join(DATA, "state_ia_checks.csv.gz"), index=False, compression="gzip")
    return ck, jumps, bad


if __name__ == "__main__":
    if "--no-download" not in sys.argv:
        download()
    df, notes = build()
    ck, jumps, bad = checks_and_write(df, notes)
    print("rows", len(df), "months", df.month.nunique(), df.month.min(), df.month.max())
    print("units", df[df.unit_level == "property"].unit_id.nunique())
    print("max |diff_pct|", ck.diff_pct.abs().max())
    print("tables+slots != AGR rows:", len(bad))
    print("jumps:")
    for j in jumps:
        print("  ", j)

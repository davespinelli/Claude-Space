"""Illinois (IL) monthly casino revenue by property, 2012-01 onward.

Output: data/state_il.csv.gz, data/state_il_checks.csv.gz (spec: scripts/STATE_DATA_SPEC.txt).
Run:    python3 state_il.py            (downloads what is not cached, parses, writes)
        python3 state_il.py --no-download

SOURCES (Illinois Gaming Board, IGB)
  1) Archived monthly "Casino Report" PDFs, 2011-12 .. 2020-03, listed by the JSON behind
     https://igb.illinois.gov/casino-gambling/casino-reports.html  (ARCHIVE_JSON below), files
     https://igb.illinois.gov/content/dam/soi/en/web/igb/documents/casino/credit-reports/archive-casino-reports/YYYYMM-casino-report.pdf
  2) IGB web app https://igbapps.illinois.gov/CasinoReports_AEM.aspx (ASP.NET form; "Casino Summary",
     one month per request), 2020-07 onward: CSV export (per-casino Table Game AGR, EGD AGR, Total AGR)
     and the PDF rendering of the same report (used only for its "Totals:" row).
     Cached as cache/il/app_casino_summary_YYYY-MM.csv / .pdf. A month that is not yet published
     returns the HTML form and is skipped.
  Only riverboat/land-based casinos (incl. the Fairmount Park racino casino) are in these reports.
  Video gaming terminals and sports wagering are separate IGB reports and are excluded.

MEASURE (ggr) = AGR (adjusted gross receipts = table + EGD win), dollars.
  2012-01 .. 2013-01: the archive PDF prints AGR in $000s (format A, city names); values x1000, so
  unit precision is +-$500 for these 13 months. 2013-02 .. 2020-03: dollars (format B).
  tables / slots:
    2020-07+: Table Game AGR / EGD AGR from the CSV (sum = Total AGR exactly).
    2013-01 .. 2019-12: from the per-casino "detail" page, which each archive PDF prints for the
      PREVIOUS month (so month m's split comes from file m+1). That page's statistical AGR differs from
      the page-1 tax AGR (= ggr) by median 0.1% (max 7.3%, Harrah's Joliet 2014-01; Rivers 2016-05,
      2017-05, 2017-10 1.5-3%), so tables + slots need not equal ggr exactly in those months.
    Blank: 2012-01..2012-12 (detail pages in $000s, column-major layout, not parsed) and
      2020-01..2020-03 (the 3-page 2020 PDFs dropped the detail page).

MONTHS 2012-01 .. 2026-08 (176, none missing).
  COVID: IGB suspended casino gaming 2020-03-16 .. 2020-07-01 and published no reports for
  2020-04..2020-06; those months are written as 0 for the 10 then-open casinos
  (source_file = none_covid_closure). Second closure 2020-11-20 .. 2021-01-16: Dec 2020 AGR is only
  $1-16k per casino (as published, kept).

UNITS (17 property ids; renames linked in UNIT_ID)
  Alton / ALTON - ARGOSY / Argosy Casino Alton; East Peoria / E. PEORIA - PAR-A-DICE / Par-A-Dice;
  Rock Island / ROCK ISLAND - JUMERS / Bally's Quad Cities; Joliet - Hollywood / Hollywood Casino
  Joliet (relocated to a new land-based building in Aug 2025, same licence, same id); Metropolis /
  Harrah's Metropolis; Joliet - Harrah's / Harrah's Joliet; Aurora / Hollywood Casino Aurora;
  E St Louis / Casino Queen / DraftKings at Casino Queen; Elgin / Grand Victoria; Des Plaines /
  Rivers Casino. New licensees are printed under legal-entity names: FHR-Illinois LLC = American
  Place Waukegan (Full House; from 2023-02), Danville Development, LLC = Golden Nugget Danville
  (2023-05), Bally's Chicago Operating Company, LLC (temporary Medinah Temple casino, 2023-09),
  Walker's Bluff Casino Resort, LLC (2023-08), Wind Creek IL LLC = Wind Creek Chicago Southland
  (2024-11), Hard Rock Casino Rockford (temporary 2021-11, permanent 2024; one id), Fairmount Park
  (racino casino, 2025-04). Temporary -> permanent moves keep one id.

PUBLICATION DATE
  Archive months (2012-01 .. 2020-03): pdf_metadata = PDF CreationDate (the files were re-uploaded in
  2024, ModDate 2024-05-03, but CreationDate is original). Median lag 4 days after month end; a few
  late dates (2014-01, 2015-04, 2019-07: 34-36 days; 2020-03: 104 days) probably reflect re-issued
  PDFs. 2020-04 onward: blank. The web app generates reports on request (its "Report Date" is the
  request time) and IGB issues no monthly revenue press release, so no first-publication date is
  available (use the pre-registered month-end + 30 days fallback).

CHECKS (data/state_il_checks.csv.gz, all months)
  sum of units vs regulator total ("Totals" row of archive PDF page 1; "Totals:" row of the app PDF):
  max |diff| 0.0016% (rounding in the $000s months). Jump scan (m/m >3x or <1/3 outside Mar-Jul 2020):
  Nov 2020-Feb 2021 COVID closure/reopening (all casinos), Argosy Alton 2019-05/06 Mississippi flood
  closure and 2019-07 reopening, Golden Nugget Danville 2023-06 and Walker's Bluff 2023-09 (first full
  months after opening). No duplicate (unit_id, month). Unknown casino labels raise an error.
"""
import os, re, sys, time, glob, json, calendar, datetime as dt
import requests
import pandas as pd
import numpy as np

ROOT = "/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming"
CACHE = os.path.join(ROOT, "cache", "il")
DATA = os.path.join(ROOT, "data")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
BASE = "https://igb.illinois.gov"
ARCHIVE_JSON = (BASE + "/content/soi/igb/en/casino-gambling/casino-reports/jcr:content/responsivegrid/container/"
                "container_293684588/container/container_copy/container_1711859025/data_table_assets.datatableassets.json")
APP = "https://igbapps.illinois.gov/CasinoReports_AEM.aspx"
MEASURE = "AGR"

# regulator name (upper-cased, whitespace-normalised, curly quotes -> ') -> stable unit_id
UNIT_ID = {
    # format A (2011-12..2013-01, city names, $000s)
    "ALTON": "IL_ARGOSY_ALTON", "EAST PEORIA": "IL_PAR_A_DICE", "ROCK ISLAND": "IL_ROCK_ISLAND",
    "JOLIET - HOLLYWOOD": "IL_HOLLYWOOD_JOLIET", "METROPOLIS": "IL_HARRAHS_METROPOLIS",
    "JOLIET - HARRAH'S": "IL_HARRAHS_JOLIET", "AURORA": "IL_HOLLYWOOD_AURORA", "E ST LOUIS": "IL_CASINO_QUEEN",
    "ELGIN": "IL_GRAND_VICTORIA_ELGIN", "DES PLAINES": "IL_RIVERS_DES_PLAINES",
    # format B (2013-02..2020-03, 'CITY - NAME', dollars)
    "ALTON - ARGOSY": "IL_ARGOSY_ALTON", "E. PEORIA - PAR-A-DICE": "IL_PAR_A_DICE",
    "ROCK ISLAND - JUMERS": "IL_ROCK_ISLAND", "JOLIET - HOLLYWOOD": "IL_HOLLYWOOD_JOLIET",
    "METROPOLIS - HARRAHS": "IL_HARRAHS_METROPOLIS", "JOLIET - HARRAHS": "IL_HARRAHS_JOLIET",
    "AURORA - HOLLYWOOD": "IL_HOLLYWOOD_AURORA", "E. ST. LOUIS - CASINO QUEEN": "IL_CASINO_QUEEN",
    "ELGIN - GRAND VICTORIA": "IL_GRAND_VICTORIA_ELGIN", "DES PLAINES - RIVERS CASINO": "IL_RIVERS_DES_PLAINES",
    # IGB web app (2020-07 onward; licensee / trade names)
    "ARGOSY CASINO ALTON": "IL_ARGOSY_ALTON", "PAR-A-DICE HOTEL CASINO": "IL_PAR_A_DICE",
    "JUMER'S CASINO & HOTEL": "IL_ROCK_ISLAND", "BALLY'S QUAD CITIES CASINO & HOTEL": "IL_ROCK_ISLAND",
    "HOLLYWOOD CASINO JOLIET": "IL_HOLLYWOOD_JOLIET", "HARRAH'S METROPOLIS CASINO": "IL_HARRAHS_METROPOLIS",
    "HARRAH'S JOLIET CASINO & HOTEL": "IL_HARRAHS_JOLIET", "HOLLYWOOD CASINO AURORA": "IL_HOLLYWOOD_AURORA",
    "CASINO QUEEN": "IL_CASINO_QUEEN", "DRAFTKINGS AT CASINO QUEEN": "IL_CASINO_QUEEN",
    "GRAND VICTORIA CASINO": "IL_GRAND_VICTORIA_ELGIN", "RIVERS CASINO": "IL_RIVERS_DES_PLAINES",
    "HARD ROCK CASINO ROCKFORD": "IL_HARD_ROCK_ROCKFORD",
    "BALLY'S CHICAGO OPERATING COMPANY, LLC": "IL_BALLYS_CHICAGO",
    "DANVILLE DEVELOPMENT, LLC": "IL_GOLDEN_NUGGET_DANVILLE",
    "FHR-ILLINOIS LLC": "IL_AMERICAN_PLACE_WAUKEGAN",
    "WALKER'S BLUFF CASINO RESORT, LLC": "IL_WALKERS_BLUFF",
    "WIND CREEK IL LLC": "IL_WIND_CREEK_CHICAGO_SOUTHLAND",
    "FAIRMOUNT PARK": "IL_FAIRMOUNT_PARK",
}


def log(*a):
    print(*a, file=sys.stderr)


def norm(s):
    s = str(s).replace("’", "'").replace("‘", "'")
    s = s.replace("*", "")
    return re.sub(r"\s+", " ", s).strip()


def uid_for(name):
    k = norm(name).upper()
    if k in UNIT_ID:
        return UNIT_ID[k]
    raise KeyError(f"unmapped IL unit {name!r}")


# ------------------------------------------------------------------ download
def _get(url, dest, min_size=500):
    if os.path.exists(dest) and os.path.getsize(dest) >= min_size:
        return dest
    for k in range(5):
        try:
            r = requests.get(url, headers=UA, timeout=90)
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


def _app_fetch(session, year, month, view):
    """POST the IGB CasinoReports form for one month. view: 'ViewCSV' | 'ViewPDF'."""
    mname = calendar.month_name[month]
    for k in range(5):
        try:
            h = session.get(APP, timeout=60).text
            f = {n: v for n, v in re.findall(r'<input type="hidden" name="([^"]+)" id="[^"]+" value="([^"]*)"', h)}
            f.update({"CasinoReportTypes": "Casino Summary", "SearchStartMonth": mname, "SearchStartYear": str(year),
                      "SearchEndMonth": mname, "SearchEndYear": str(year), "ViewType": view,
                      "ButtonSearch.x": "10", "ButtonSearch.y": "10"})
            time.sleep(0.6)
            r = session.post(APP, data=f, timeout=90)
            time.sleep(0.6)
            ct = r.headers.get("content-type", "")
            if view == "ViewCSV" and "csv" in ct:
                return r.content
            if view == "ViewPDF" and "pdf" in ct:
                return r.content
            return None  # month not (yet) published -> HTML page comes back
        except Exception as e:
            log("err", e)
            time.sleep(2 ** k)
    return None


def download():
    os.makedirs(CACHE, exist_ok=True)
    lst = os.path.join(CACHE, "archive_list.json")
    _get(ARCHIVE_JSON, lst, min_size=1000)
    for r in json.load(open(lst))["data"]:
        url = r[0][1]
        m = re.search(r"/(\d{6})-casino-report\.pdf$", url)
        if m and m.group(1) >= "201112":
            _get(BASE + url, os.path.join(CACHE, os.path.basename(url)), min_size=1000)
    s = requests.Session()
    s.headers.update(UA)
    today = dt.date.today()
    y, mo = 2020, 7
    misses = 0
    while (y, mo) <= (today.year, today.month):
        for view, ext in (("ViewCSV", "csv"), ("ViewPDF", "pdf")):
            fn = os.path.join(CACHE, f"app_casino_summary_{y}-{mo:02d}.{ext}")
            if os.path.exists(fn) and os.path.getsize(fn) > 200:
                continue
            b = _app_fetch(s, y, mo, view)
            if b:
                open(fn, "wb").write(b)
            else:
                log("not published:", y, mo, view)
        mo += 1
        if mo == 13:
            y, mo = y + 1, 1


# ------------------------------------------------------------------ parsing
NUM = re.compile(r"^\(?-?\$?\s*-?[\d,]+(\.\d+)?\)?%?$")


def num(s):
    s = str(s).strip()
    neg = s.startswith("(") or s.startswith("-") or "-$" in s
    v = float(re.sub(r"[^\d.]", "", s))
    return -v if neg else v


def pdf_created(d):
    mc = re.match(r"D:(\d{4})(\d{2})(\d{2})", (d.metadata or {}).get("creationDate") or "")
    return dt.date(*map(int, mc.groups())) if mc else None


def parse_archive_page0(path):
    """Return (rows[(name, agr)], total_agr, thousands_flag, created_date)."""
    import pymupdf
    d = pymupdf.open(path)
    t = d[0].get_text()
    thousands = "(000's)" in t[:800]
    toks = [x.strip() for x in t.split("\n")]
    toks = [x for x in toks if x and x != "$"]
    groups, cur = [], None
    for x in toks:
        if NUM.match(x):
            if cur is not None:
                cur[1].append(num(x))
            continue
        nm = norm(x)
        if nm.upper() in UNIT_ID or nm.upper() == "TOTALS":
            cur = [nm, []]
            groups.append(cur)
        else:
            # header / note / chart label: stop collecting (kept only to detect unknown casino names)
            cur = ["?" + nm, []]
            groups.append(cur)
    unknown = [g for g in groups if g[0].startswith("?") and len(g[1]) == 7 and g[1][1] >= 5000]  # 2nd col = sq ft
    if unknown:
        raise KeyError(f"{path}: unknown row label(s) with 7 numbers: {[g[0] for g in unknown]}")
    groups = [g for g in groups if not g[0].startswith("?")]
    rows, total = [], None
    for i, (nm, vals) in enumerate(groups):
        if nm.upper() == "TOTALS":
            if vals:
                total = vals[0]
            continue
        if len(vals) == 14 and i + 1 < len(groups) and groups[i + 1][0].upper() == "TOTALS" and not groups[i + 1][1]:
            vals, total = vals[:7], vals[7]  # format A: totals printed before the 'Totals' label
        if len(vals) != 7:
            raise ValueError(f"{path}: {nm} has {len(vals)} numbers")
        rows.append((nm, vals[0]))
    if total is None:
        raise ValueError(f"{path}: no total")
    k = 1000.0 if thousands else 1.0
    return [(n, v * k) for n, v in rows], total * k, thousands, pdf_created(d)


def parse_archive_detail(path):
    """Per-casino detail page (dollars; 2013-02..2020-01 files) for the PREVIOUS month.
    Returns dict name -> (agr, table_agr, egd_agr), incl. 'Totals'."""
    import pymupdf
    d = pymupdf.open(path)
    for p in d:
        t = p.get_text()
        if "Table AGR" not in t or "EGD AGR" not in t or "ALTON" not in t:
            continue
        toks = [x.strip() for x in t.split("\n") if x.strip() and x.strip() != "$"]
        i0 = next(i for i, x in enumerate(toks) if "Casino Report" in x)
        i1 = next(i for i, x in enumerate(toks) if x == "Totals")
        names = []
        for x in toks[i0 + 1:i1]:
            if x.endswith("-") or " - " in x:
                names.append(x)
            elif names:
                names[-1] += " " + x
        names = [norm(n) for n in names] + ["Totals"]
        if len(names) < 6:
            continue  # statewide statistics page, not the per-casino detail page

        def row(label):
            j = toks.index(label)
            vals = []
            for x in toks[j + 1:]:
                if NUM.match(x):
                    vals.append(num(x))
                    if len(vals) == len(names):
                        break
                else:
                    break
            return vals
        agr, ta, ea = row("AGR"), row("Table AGR"), row("EGD AGR")
        if not (len(agr) == len(ta) == len(ea) == len(names)):
            return None
        return {n: (a, b, c) for n, a, b, c in zip(names, agr, ta, ea)}
    return None


def parse_app_csv(path):
    raw = open(path, "rb").read()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("cp1252")
    lines = txt.splitlines()
    hi = next(i for i, l in enumerate(lines) if l.startswith('"Casino"'))
    from io import StringIO
    df = pd.read_csv(StringIO("\n".join(lines[hi:])))
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df = df[df["Casino"].notna() & (df["Casino"].astype(str).str.strip() != "")]
    return df


def parse_app_pdf_totals(path):
    import pymupdf
    d = pymupdf.open(path)
    t = "\n".join(p.get_text() for p in d)
    i = t.find("Totals:")
    if i < 0:
        return None
    vals = [x.strip() for x in t[i + 7:].split("\n") if x.strip()]
    money = [num(v) for v in vals if v.startswith("$") or v.startswith("-$") or v.startswith("($")][:3]
    return dict(tables=money[0], slots=money[1], ggr=money[2])


# ------------------------------------------------------------------ build
def build():
    recs, notes = [], {}
    files = sorted(glob.glob(os.path.join(CACHE, "*-casino-report.pdf")))
    details = {}
    page0 = {}
    for f in files:
        ym = re.search(r"(\d{4})(\d{2})-casino-report", f)
        mo = f"{ym.group(1)}-{ym.group(2)}"
        page0[mo] = parse_archive_page0(f)
        det = parse_archive_detail(f)
        if det:
            prev = (pd.Period(mo, "M") - 1).strftime("%Y-%m")
            details[prev] = det
    for mo, (rows, total, thousands, created) in sorted(page0.items()):
        if mo < "2012-01":
            continue
        me = pd.Period(mo, "M").end_time.date()
        pub, psrc = ("", "")
        if created and 0 <= (created - me).days <= 150:
            pub, psrc = created.isoformat(), "pdf_metadata"
        det = details.get(mo)
        det_uid = {("TOTALS" if n == "Totals" else uid_for(n)): v for n, v in det.items()} if det else {}
        src = f"{mo.replace('-', '')}-casino-report.pdf"
        for nm, agr in rows:
            tb = sl = np.nan
            v = det_uid.get(uid_for(nm))
            if v is not None:
                a, ta, ea = v
                # detail page: statistical table/EGD AGR (sums to its own AGR, which can differ a little from
                # the tax AGR on page 1 = ggr); keep as published when internally consistent
                if abs(ta + ea - a) <= 2:
                    tb, sl = ta, ea
                if abs(a / agr - 1) > 0.02:
                    log(f"note: {mo} {nm}: detail-page AGR {a:,.0f} vs page-1 AGR {agr:,.0f}")
            recs.append(dict(state="IL", unit=nm, unit_id=uid_for(nm), unit_level="property", month=mo, ggr=agr,
                             slots=sl, tables=tb, n_casinos=np.nan, measure=MEASURE, pub_date=pub, pub_source=psrc,
                             source_file=src))
        tt = ts = np.nan
        if "TOTALS" in det_uid:
            tt, ts = det_uid["TOTALS"][1], det_uid["TOTALS"][2]
        recs.append(dict(state="IL", unit="__STATE_TOTAL__", unit_id="IL___STATE_TOTAL__", unit_level="state_total",
                         month=mo, ggr=total, slots=ts, tables=tt, n_casinos=float(len(rows)), measure=MEASURE,
                         pub_date=pub, pub_source=psrc, source_file=src))
        notes[mo] = ("archive PDF p.1 'Totals' (AGR in $000s; units x1000)" if thousands
                     else "archive PDF p.1 'Totals' (AGR, dollars)")
    # COVID closure: IGB suspended all casino gaming 2020-03-16 .. 2020-07-01; no reports for Apr-Jun 2020.
    last = max(page0)
    open_units = [(nm, uid_for(nm)) for nm, _ in page0["2020-03"][0]]
    for mo in ("2020-04", "2020-05", "2020-06"):
        for nm, uid in open_units:
            recs.append(dict(state="IL", unit=nm, unit_id=uid, unit_level="property", month=mo, ggr=0.0, slots=0.0,
                             tables=0.0, n_casinos=np.nan, measure=MEASURE, pub_date="", pub_source="",
                             source_file="none_covid_closure"))
        recs.append(dict(state="IL", unit="__STATE_TOTAL__", unit_id="IL___STATE_TOTAL__", unit_level="state_total",
                         month=mo, ggr=0.0, slots=0.0, tables=0.0, n_casinos=0.0, measure=MEASURE, pub_date="",
                         pub_source="", source_file="none_covid_closure"))
        notes[mo] = "casinos closed by IGB order (COVID-19); zero by construction"
    # IGB web app, 2020-07 onward
    for f in sorted(glob.glob(os.path.join(CACHE, "app_casino_summary_*.csv"))):
        mo = re.search(r"(\d{4}-\d{2})\.csv$", f).group(1)
        df = parse_app_csv(f)
        n = 0
        for _, r in df.iterrows():
            nm = norm(r["Casino"])
            recs.append(dict(state="IL", unit=nm, unit_id=uid_for(nm), unit_level="property", month=mo,
                             ggr=float(r["Total AGR"]), slots=float(r["EGD AGR"]), tables=float(r["Table Game AGR"]),
                             n_casinos=np.nan, measure=MEASURE, pub_date="", pub_source="",
                             source_file=os.path.basename(f)))
            n += 1
        pf = f[:-4] + ".pdf"
        tot = parse_app_pdf_totals(pf) if os.path.exists(pf) else None
        if tot:
            recs.append(dict(state="IL", unit="__STATE_TOTAL__", unit_id="IL___STATE_TOTAL__",
                             unit_level="state_total", month=mo, ggr=tot["ggr"], slots=tot["slots"],
                             tables=tot["tables"], n_casinos=float(n), measure=MEASURE, pub_date="", pub_source="",
                             source_file=os.path.basename(pf)))
            notes[mo] = "IGB app PDF 'Totals:' row (Total Adjusted Gross Receipts)"
    return pd.DataFrame(recs), notes


def checks_and_write(df, notes):
    props = df[df.unit_level == "property"]
    tot = df[df.unit_level == "state_total"].set_index("month")["ggr"]
    s = props.groupby("month")["ggr"].sum()
    ck = pd.DataFrame({"month": s.index, "sum_of_units": s.values, "regulator_total": tot.reindex(s.index).values})
    with np.errstate(divide="ignore", invalid="ignore"):
        ck["diff_pct"] = np.where(ck.regulator_total != 0, (ck.sum_of_units / ck.regulator_total - 1) * 100, 0.0)
    ck["note"] = ck.month.map(notes).fillna("")
    # component checks where split is present
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
        os.path.join(DATA, "state_il.csv.gz"), index=False, compression="gzip")
    ck.to_csv(os.path.join(DATA, "state_il_checks.csv.gz"), index=False, compression="gzip")
    return ck, jumps


if __name__ == "__main__":
    if "--no-download" not in sys.argv:
        download()
    df, notes = build()
    ck, jumps = checks_and_write(df, notes)
    print("rows", len(df), "months", df.month.nunique(), df.month.min(), df.month.max())
    print("units", df[df.unit_level == "property"].unit_id.nunique())
    print("max |diff_pct|", ck.diff_pct.abs().max())
    print("jumps:")
    for j in jumps:
        print("  ", j)

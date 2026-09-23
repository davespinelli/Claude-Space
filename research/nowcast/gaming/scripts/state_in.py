"""Indiana (IN) monthly casino revenue by property, 2012-01 onward.

Output: data/state_in.csv.gz, data/state_in_checks.csv.gz (spec: scripts/STATE_DATA_SPEC.txt).
Run:    python3 state_in.py            (downloads what is not cached, parses, writes)
        python3 state_in.py --no-download

SOURCES (Indiana Gaming Commission, IGC)
  Listing pages:  https://www.in.gov/igc/publications/monthly-revenue/  (current year)
                  https://www.in.gov/igc/publications/archived-monthly-revenue-reports/archived-monthly-revenue-reports-YYYY/
                  (2012-2024), .../igc-monthly-revenue-reports-2025/
  Files:          https://www.in.gov/igc/files/reports/YYYY/YYYY-MM-Revenue.pdf   (all months)
                  https://www.in.gov/igc/files/reports/YYYY/YYYY-MM-Revenue.xlsx  (2019-07 onward)
  Cached in cache/in/ under the original file names.

MEASURE (ggr)
  "Win" = Table Win + EGD/Slot Win from the WAGERING TAX table of each monthly report (page 1 /
  sheet 1), per casino/racino. This is gross gaming win BEFORE Indiana's AGR deductions. The report's
  "Taxable AGR" column subtracts qualified free-play (capped per licensee per fiscal year, so it is
  front-loaded each Jul-Jun year), "Other" items, and a 12% deduction for the two racinos; those
  artefacts make taxable AGR a poor monthly revenue series, so it is NOT used. slots = EGD/Slot Win,
  tables = Table Win (incl. poker). From 2014 the report also prints a "Win" column; it equals
  table+EGD win to the dollar except 3 unit-months (<= $4,452 differences, 2015-07 Indiana Grand,
  2021-06 Blue Chip, 2023-10 Rising Star). Sports wagering (from 2019-09) is reported in separate
  columns/sheets and is excluded. Source preference: xlsx when present (2019-07+), else PDF text.
  Racinos (Hoosier Park, Indiana Live/Indiana Grand/Horseshoe Indianapolis) had no table games
  until 2020 -> tables = 0.

MONTHS  2012-01 .. 2026-08 (176 months, none missing). COVID: all casinos closed 2020-03-16 to
  mid-June 2020; the IGC published 2020-04 and 2020-05 reports with zeros (kept as 0).

UNITS (15 property ids; unit = name as printed that month; renames linked in UNIT_ID):
  Casino Aztar -> Tropicana (Evansville) -> Tropicana Evansville -> Bally's Evansville (IN_EVANSVILLE);
  Indiana Live -> Indiana Grand -> Horseshoe Indianapolis (IN_SHELBYVILLE);
  Horseshoe SI -> Caesars Southern Indiana (IN_SOUTHERN_INDIANA); Horseshoe HD -> Horseshoe Hammond;
  Hoosier Park -> Harrah's Hoosier Park; Hollywood -> Hollywood Lawrenceburg; short -> long names for
  Ameristar, Belterra, Blue Chip, French Lick, Rising Star.
  NOT linked (different physical casinos): Majestic Star and Majestic Star II (two Gary boats, last
  month 2021-04; Majestic Star II's April 2021 win fell to $0.58M ahead of closure, a real drop) vs
  Hard Rock Casino Northern Indiana (Gary, opened 2021-05-14; printed "... A" 2021-2025 because its
  receipts were taxed as two licences until 2025-06-30); Terre Haute Casino (new licence, opened
  2024-04).

PUBLICATION DATE
  pdf_metadata: CreationDate of the monthly PDF (the posted file). Checked against the "Last updated on
  MM-DD-YYYY" line printed in each report: CreationDate is 0-6 days later in 173/174 months. One
  exception, 2025-09 (PDF re-created 2025-11-05, 30 days after its "Last updated" date 2025-10-06): that
  month uses the printed date (pub_source = report_text). Typical lag: 9 days after month end
  (range 6-12).

CHECKS (data/state_in_checks.csv.gz, all 176 months)
  sum of property win vs the report's own TOTAL row (TOTAL table win + TOTAL EGD win): max |diff|
  0.000004%. Exception handled: in 2021-05 the WAGERING TAX TOTAL row double-counts Hard Rock NI
  (241.4M vs 220.8M sum); for that month regulator_total is the TOTAL of the published "Win" column
  (220,846,734), which matches the sum (noted in the checks file). The IGC corrections notice
  (in.gov/igc/files/publications/corrections.pdf) lists no win corrections for 2012+ (it notes the
  2021-06 "Win" total-row error, which does not affect unit values). Jump scan (m/m ratio >3 or <1/3
  outside Mar-Jul 2020): only Majestic Star II 2021-04 (closure). No duplicate (unit_id, month).
"""
import os, re, sys, time, glob, datetime as dt
import requests
import pandas as pd
import numpy as np

ROOT = "/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming"
CACHE = os.path.join(ROOT, "cache", "in")
DATA = os.path.join(ROOT, "data")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
BASE = "https://www.in.gov"
LISTINGS = {y: f"{BASE}/igc/publications/archived-monthly-revenue-reports/archived-monthly-revenue-reports-{y}/"
            for y in range(2012, 2025)}
LISTINGS[2025] = f"{BASE}/igc/publications/archived-monthly-revenue-reports/igc-monthly-revenue-reports-2025/"
LISTINGS["current"] = f"{BASE}/igc/publications/monthly-revenue/"

# Hand-coded unit_id map: regulator name (upper, stripped of asterisks) -> stable id.
UNIT_ID = {
    "AMERISTAR": "IN_AMERISTAR_EAST_CHICAGO", "AMERISTAR CASINO": "IN_AMERISTAR_EAST_CHICAGO",
    "BELTERRA": "IN_BELTERRA", "BELTERRA CASINO": "IN_BELTERRA",
    "BLUE CHIP": "IN_BLUE_CHIP", "BLUE CHIP CASINO": "IN_BLUE_CHIP",
    "CASINO AZTAR": "IN_EVANSVILLE", "TROPICANA": "IN_EVANSVILLE", "TROPICANA EVANSVILLE": "IN_EVANSVILLE",
    "BALLY'S EVANSVILLE": "IN_EVANSVILLE",
    "FRENCH LICK": "IN_FRENCH_LICK", "FRENCH LICK RESORT": "IN_FRENCH_LICK",
    "HOLLYWOOD": "IN_HOLLYWOOD_LAWRENCEBURG", "HOLLYWOOD LAWRENCEBURG": "IN_HOLLYWOOD_LAWRENCEBURG",
    "HOOSIER PARK": "IN_HOOSIER_PARK", "HARRAH'S HOOSIER PARK": "IN_HOOSIER_PARK",
    "HORSESHOE HD": "IN_HORSESHOE_HAMMOND", "HORSESHOE HAMMOND": "IN_HORSESHOE_HAMMOND",
    "HORSESHOE SI": "IN_SOUTHERN_INDIANA", "HORSESHOE SOUTHERN INDIANA": "IN_SOUTHERN_INDIANA",
    "CAESARS SOUTHERN INDIANA": "IN_SOUTHERN_INDIANA",
    "INDIANA LIVE": "IN_SHELBYVILLE", "INDIANA GRAND": "IN_SHELBYVILLE", "HORSESHOE INDIANAPOLIS": "IN_SHELBYVILLE",
    "MAJESTIC STAR": "IN_MAJESTIC_STAR_I", "MAJESTIC STAR II": "IN_MAJESTIC_STAR_II",
    "HARD ROCK CASINO NORTHERN INDIANA": "IN_HARD_ROCK_NORTHERN_INDIANA",
    "HARD ROCK NORTHERN INDIANA": "IN_HARD_ROCK_NORTHERN_INDIANA",
    # 2021-2025 the Hard Rock NI row is labelled 'A' (its receipts were taxed as two licences until 2025-06-30)
    "HARD ROCK CASINO NORTHERN INDIANA A": "IN_HARD_ROCK_NORTHERN_INDIANA",
    "RISING STAR": "IN_RISING_STAR", "RISING STAR CASINO": "IN_RISING_STAR",
    "TERRE HAUTE CASINO": "IN_TERRE_HAUTE", "QUEEN OF TERRE HAUTE": "IN_TERRE_HAUTE",
    "TERRE HAUTE CASINO RESORT": "IN_TERRE_HAUTE",
}
MEASURE = "win (table+EGD, pre free-play/AGR deductions)"
TOTAL_NOTE = {}


def log(*a):
    print(*a, file=sys.stderr)


def get(url, dest, min_size=500):
    """Download url to dest unless cached. Throttled (0.6 s) with retry/backoff."""
    if os.path.exists(dest) and os.path.getsize(dest) >= min_size:
        return dest
    for k in range(5):
        try:
            r = requests.get(url, headers=UA, timeout=90)
            if r.status_code == 200 and len(r.content) >= min_size:
                with open(dest, "wb") as f:
                    f.write(r.content)
                time.sleep(0.6)
                return dest
            log("status", r.status_code, url)
            if r.status_code == 404:
                return None
        except Exception as e:  # network hiccup
            log("err", e, url)
        time.sleep(2 ** k)
    return None


def download(refresh_current=True):
    os.makedirs(CACHE, exist_ok=True)
    links = set()
    for y, u in LISTINGS.items():
        fn = os.path.join(CACHE, f"listing_{y}.html")
        if y == "current" and refresh_current and os.path.exists(fn):
            os.remove(fn)  # the current-year page changes monthly
        get(u, fn, min_size=1000)
        h = open(fn, encoding="utf-8", errors="ignore").read()
        links |= set(re.findall(r'href="([^"]*/reports/[^"]*\.(?:pdf|xlsx?))"', h, flags=re.I))
    for l in sorted(links):
        m = re.search(r"/(\d{4})-(\d{2})-Revenue\.(pdf|xlsx?)$", l, flags=re.I)
        if not m or int(m.group(1)) < 2012:
            continue
        get(BASE + l if l.startswith("/") else l, os.path.join(CACHE, os.path.basename(l)), min_size=1000)


# ---------------------------------------------------------------- parsing helpers
NUMRE = re.compile(r"^\(?-?\$?\s*-?\(?[\d,]*\.?\d*\)?$")


def to_num(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip()
    if s in ("", "$", "-", "N/A", "n/a"):
        return None
    neg = s.startswith("(") or s.startswith("-") or "-$" in s
    s2 = re.sub(r"[^\d.]", "", s)
    if s2 == "":
        return None
    v = float(s2)
    return -v if neg else v


def norm_name(s):
    s = re.sub(r"\s+", " ", str(s)).strip()
    return s.replace("*", "").strip()


def is_numtok(s):
    s = s.strip()
    return s == "" or s == "$" or bool(NUMRE.match(s)) and any(c.isdigit() for c in s) or s == "$"


def parse_wagering_rows(tokens):
    """tokens: list of strings after the header of the WAGERING TAX table.
    Returns list of (name, table_win, egd_win, n_tables, n_egd) incl. TOTAL."""
    rows, cur, vals = [], None, []

    def flush():
        if cur is None:
            return
        money = [v for v in vals if "$" in v]
        cnts = [v for v in vals if "$" not in v and any(c.isdigit() for c in v)]
        rows.append((cur, money, cnts, list(vals)))

    for t in tokens:
        t = t.strip()
        if t == "":
            continue
        if is_numtok(t):
            if cur is not None:
                vals.append(t)
        else:
            if t.startswith("*") or t.upper().startswith("YEAR TO DATE") or t.upper().startswith("YTD"):
                break
            flush()
            cur, vals = norm_name(t), []
            if cur.upper() == "TOTAL":
                pass
    flush()
    out = []
    for name, money, cnts, raw in rows:
        # money tokens: [table_win, egd_win, agr] or [egd_win, agr] (racino, no tables)
        if len(money) >= 3:
            tw, ew = to_num(money[-3]), to_num(money[-2])
        elif len(money) == 2:
            # racino without table games: '$' placeholder or a bare 0 for table win
            tw, ew = 0.0, to_num(money[-2])
        else:
            continue
        if tw is None:
            tw = 0.0
        n_eg = to_num(cnts[-1]) if cnts else None
        out.append((name, tw, ew, raw))
        if name.upper() == "TOTAL":
            break
    return out


def parse_pdf(path):
    import pymupdf
    d = pymupdf.open(path)
    text = "\n".join(p.get_text() for p in d)
    meta = d.metadata or {}
    lu = re.search(r"Last updated on\s+(\d{1,2})[-/](\d{1,2})[-/](\d{4})", text)
    last_upd = dt.date(int(lu.group(3)), int(lu.group(1)), int(lu.group(2))) if lu else None
    cd = meta.get("creationDate") or ""
    mc = re.match(r"D:(\d{4})(\d{2})(\d{2})", cd)
    created = dt.date(int(mc.group(1)), int(mc.group(2)), int(mc.group(3))) if mc else None
    m = re.search(r"WAGERING TAX\s*\n\s*No\. of Table Games", text)
    if not m:
        return None, {}, last_upd, created
    seg = text[m.end():]
    # skip header labels up to 'AGR'
    h = re.search(r"\n\s*AGR\s*\n", seg)
    seg = seg[h.end():]
    tokens = seg.split("\n")
    rows = parse_wagering_rows(tokens)
    # published 'Win' column (2014+) for cross-check
    win = {}
    mw = re.search(r"\n\s*Win\s*\n\s*Free Play\s*\n\s*Other \*?\s*\n\s*Taxable AGR\s*\n", text)
    if mw:
        toks = [t.strip() for t in text[mw.end():].split("\n") if t.strip()]
        cur = None
        for t in toks:
            if is_numtok(t):
                if cur is not None and cur not in win and "$" in t:
                    win[cur] = to_num(t)
            else:
                if t.upper().startswith("WAGERING TAX") or t.startswith("*"):
                    break
                if cur == "TOTAL":
                    break
                cur = norm_name(t).upper()
    return rows, win, last_upd, created


def parse_xlsx(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb.worksheets[0]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    out, win = [], {}
    start = None
    for i, r in enumerate(rows):
        cells = [str(x or "").strip() for x in r]
        if "WAGERING TAX" in [c.upper() for c in cells] and any("Table Win" in c for c in cells):
            start, hdr = i, cells
            break
    if start is None:
        raise ValueError("no WAGERING TAX in " + path)
    cn = [c.upper() for c in hdr].index("WAGERING TAX")
    ci_tw = hdr.index("Table Win")
    ci_ew = [j for j, x in enumerate(hdr) if x.startswith("EGD") and "Win" in x][0]
    for r in rows[start + 1:]:
        name = norm_name(r[cn] or "") if cn < len(r) else ""
        if not name:
            continue
        if name.startswith("*") or name.upper().startswith("YEAR"):
            break
        tw, ew = to_num(r[ci_tw]), to_num(r[ci_ew])
        out.append((name, tw if tw is not None else 0.0, ew, r))
        if name.upper() == "TOTAL":
            break
    # published 'Win' column of the Win / Free Play / Other / Taxable AGR table (cross-check only)
    for i, r in enumerate(rows):
        cells = [str(x or "").strip() for x in r]
        if "Taxable AGR" in cells and "Win" in cells:
            cw = cells.index("Win")
            for r2 in rows[i + 1:]:
                n = norm_name(r2[cn] or "") if cn < len(r2) else ""
                if not n:
                    continue
                if n.upper() == "WAGERING TAX":
                    break
                win[n.upper()] = to_num(r2[cw])
                if n.upper() == "TOTAL":
                    break
            break
    return out, win


def build():
    files = sorted(glob.glob(os.path.join(CACHE, "*-Revenue.*")))
    months = sorted({re.match(r"(\d{4}-\d{2})", os.path.basename(f)).group(1) for f in files})
    recs, checks, pubinfo = [], [], []
    for mo in months:
        if mo < "2012-01":
            continue
        pdf = os.path.join(CACHE, f"{mo}-Revenue.pdf")
        xl = os.path.join(CACHE, f"{mo}-Revenue.xlsx")
        last_upd = created = None
        prow, pwin = None, {}
        if os.path.exists(pdf):
            try:
                prow, pwin, last_upd, created = parse_pdf(pdf)
            except Exception as e:
                log("pdf parse fail", mo, e)
        if os.path.exists(xl):
            rows, win = parse_xlsx(xl)
            src = os.path.basename(xl)
        else:
            rows, win, src = prow, pwin, os.path.basename(pdf)
        if not rows:
            log("NO ROWS", mo)
            continue
        # pub date: PDF CreationDate (the file posted); fallback report text 'Last updated on'
        me = (pd.Period(mo, "M").end_time).date()
        pub, psrc = "", ""
        regenerated = created and last_upd and (created - last_upd).days > 10
        if created and 0 <= (created - me).days <= 120 and not regenerated:
            pub, psrc = created.isoformat(), "pdf_metadata"
        elif last_upd and 0 <= (last_upd - me).days <= 120:
            pub, psrc = last_upd.isoformat(), "report_text"
        pubinfo.append((mo, created, last_upd))
        total = None
        for name, tw, ew, raw in rows:
            if name.upper() == "TOTAL":
                total = (tw, ew)
                continue
            key = name.upper()
            uid = UNIT_ID.get(key)
            if uid is None:
                raise KeyError(f"unmapped IN unit {name!r} in {mo}")
            g = (tw or 0.0) + (ew or 0.0)
            recs.append(dict(state="IN", unit=name, unit_id=uid, unit_level="property", month=mo,
                             ggr=g, slots=ew, tables=tw, n_casinos=np.nan, measure=MEASURE,
                             pub_date=pub, pub_source=psrc, source_file=src))
            w = win.get(key)
            if w is not None and abs(w - g) > 2:
                log(f"WIN MISMATCH {mo} {name}: table+egd={g:,.0f} published Win={w:,.0f}")
        if total is None:
            raise ValueError("no TOTAL row " + mo)
        tot = total[0] + total[1]
        sum_units = sum((r[1] or 0) + (r[2] or 0) for r in rows if r[0].upper() != "TOTAL")
        wt = win.get("TOTAL")
        TOTAL_NOTE[mo] = "regulator_total = TOTAL row of WAGERING TAX table (table win + EGD win)"
        if tot and wt and abs(sum_units / tot - 1) > 0.01 and abs(sum_units / wt - 1) < 0.001:
            TOTAL_NOTE[mo] = (f"WAGERING TAX TOTAL row ({tot:,.0f}) double-counts Hard Rock NI; "
                              f"regulator_total = TOTAL of published 'Win' column instead")
            tot = wt
        recs.append(dict(state="IN", unit="__STATE_TOTAL__", unit_id="IN___STATE_TOTAL__",
                         unit_level="state_total", month=mo, ggr=tot, slots=total[1], tables=total[0],
                         n_casinos=float(sum(1 for r in rows if r[0].upper() != "TOTAL")), measure=MEASURE,
                         pub_date=pub, pub_source=psrc, source_file=src))
        if wt is not None and abs(wt - tot) > 2:
            log(f"TOTAL WIN MISMATCH {mo}: {tot:,.0f} vs {wt:,.0f}")
    df = pd.DataFrame(recs)
    return df, pubinfo


def checks_and_write(df):
    props = df[df.unit_level == "property"]
    tot = df[df.unit_level == "state_total"].set_index("month")["ggr"]
    s = props.groupby("month")["ggr"].sum()
    ck = pd.DataFrame({"month": s.index, "sum_of_units": s.values, "regulator_total": tot.reindex(s.index).values})
    ck["diff_pct"] = (ck.sum_of_units / ck.regulator_total - 1) * 100
    ck["note"] = ck.month.map(TOTAL_NOTE).fillna("")
    # jump scan
    notes = []
    for uid, g in props.sort_values("month").groupby("unit_id"):
        g = g.set_index("month")["ggr"]
        r = g / g.shift(1)
        for mo, v in r.items():
            if mo[:7] in ("2020-03", "2020-04", "2020-05", "2020-06", "2020-07"):
                continue
            if pd.notna(v) and np.isfinite(v) and (v > 3 or v < 1 / 3):
                notes.append((uid, mo, round(float(v), 3)))
    dup = df.duplicated(["unit_id", "month"]).sum()
    assert dup == 0, f"{dup} duplicate unit_id-month rows"
    os.makedirs(DATA, exist_ok=True)
    cols = ["state", "unit", "unit_id", "unit_level", "month", "ggr", "slots", "tables", "n_casinos",
            "measure", "pub_date", "pub_source", "source_file"]
    df[cols].sort_values(["month", "unit_level", "unit_id"]).to_csv(
        os.path.join(DATA, "state_in.csv.gz"), index=False, compression="gzip")
    ck.to_csv(os.path.join(DATA, "state_in_checks.csv.gz"), index=False, compression="gzip")
    return ck, notes


if __name__ == "__main__":
    if "--no-download" not in sys.argv:
        download()
    df, pubinfo = build()
    ck, notes = checks_and_write(df)
    print("rows", len(df), "months", df.month.nunique(), df.month.min(), df.month.max())
    print("units", df[df.unit_level == "property"].unit_id.nunique())
    print("max |diff_pct|", ck.diff_pct.abs().max())
    print("jumps (ratio >3 or <1/3, excl. Mar-Jul 2020):")
    for n in notes:
        print("  ", n)

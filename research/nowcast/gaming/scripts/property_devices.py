#!/usr/bin/env python3
"""Slot machines and table games per NV / CO casino, from the owners' 10-K property tables.

Nevada and Colorado publish gaming revenue by area only; these counts let us impute each
casino's share of its area.  For every (company, property) in data/ownership.csv.gz with state NV
or CO and every fiscal year 2012..2025 in which the company held it, the counts are taken from
that company's 10-K for that fiscal year.

Run:  python3 scripts/property_devices.py            (download what is missing, parse, build)
      flags --download / --parse / --build run single steps.

Steps
  1. Targets: ownership rows -> (company, state, property, fiscal_year) where the holding period
     [start, end) overlaps the fiscal year (ISLE's fiscal year ends in April, the rest in December).
  2. 10-K list per company from https://data.sec.gov/submissions (cached in cache/sec/submissions,
     shared with sec_fetch.py); the original 10-K's main document (primaryDocument) is downloaded to
     cache/tenk/<company>_<fy>_<accession>.htm.gz.  User-Agent carries dspinjr@gmail.com; <= ~7 req/s.
     Parsed tables + plain text are cached in cache/tenk/parsed/.
  3. Tables (automated): a header row naming slot machines / gaming machines / devices and table games
     fixes the two columns; each data row's name cell is matched with company-specific patterns
     (PATTERNS; CAESARS shared by CZR_OLD and ERI_CZR).  Cell values are read by column position in the
     HTML grid (colspans), falling back to cell counting.  PENN tables whose headings sit outside the
     HTML table are read by position (HEADERLESS).
  4. Prose (automated fallback, PROSE): where a 10-K describes a property in words ("... offered 1,232
     slots, 33 table games ..."), the counts after the first mention of the property are used; poker
     tables are added to table games when listed separately.  The note quotes the sentence.
  5. HAND: notes and the few values read by hand (with the filing they come from).
  6. data/property_devices.csv.gz: company, state, property, fiscal_year, slots, tables,
     source_accession, note.

Conventions
  * Numbers are as printed ("approximately" dropped).  '-' in the table-games column = 0; '-' in the
    slot column (property closed) and 'N/A' = blank.  Blank = not printed; the note says why.
  * Where a 10-K prints one row for several of our properties (AFFI/BALY "Black Hawk Casinos",
    PENN/PNK "Cactus Petes and Horseshu", FLL "Bronco Billy's / Chamonix"; COMBINED), the figure sits on
    one member's row and the others are blank with a note, so sums by company stay right.
  * MGM "Aria (CityCenter)" is the CityCenter row until FY2020 (Aria + Vdara; 50% JV); WYNN is Wynn Las
    Vegas + Encore as one resort.

"""
import gzip, json, re, sys, time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CACHE = ROOT / "cache"
TENK = CACHE / "tenk"
SUBS = CACHE / "sec" / "submissions"
UA = {"User-Agent": "ClaudeSpace research dspinjr@gmail.com", "Accept-Encoding": "gzip, deflate"}
FY0, FY1 = 2012, 2025
COMPANIES = ["PENN", "PNK", "BYD", "ERI_CZR", "CZR_OLD", "RRR", "MCRI", "CNTY", "FLL", "BALY", "MGM",
             "WYNN", "GDEN", "ISLE", "TPCA", "CHDN", "AFFI"]
# registrants whose 10-Ks are used in addition to the CIKs in ownership.csv.gz: company -> [(cik, fy_from, fy_to)]
EXTRA_CIKS = {"RRR": [(1503579, 2012, 2015)]}   # Station Casinos LLC (predecessor of Red Rock Resorts)

_last = [0.0]


def http_get(url: str) -> requests.Response:
    for attempt in range(6):
        dt = time.time() - _last[0]
        if dt < 0.15:
            time.sleep(0.15 - dt)
        try:
            r = requests.get(url, headers=UA, timeout=90)
            _last[0] = time.time()
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return None
            print("  status", r.status_code, url, file=sys.stderr)
        except Exception as e:  # network hiccup
            print("  retry", url, e, file=sys.stderr)
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed {url}")


def submissions_json(cik: int) -> list[dict]:
    """All filings of a registrant (recent + older shards), cached."""
    def load(name):
        p = SUBS / (name + ".gz")
        if p.exists():
            with gzip.open(p, "rt") as f:
                return json.load(f)
        r = http_get(f"https://data.sec.gov/submissions/{name}")
        j = r.json()
        p.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(p, "wt") as f:
            json.dump(j, f)
        return j
    j = load(f"CIK{cik:010d}.json")
    frames = [j["filings"]["recent"]] + [load(fl["name"]) for fl in j["filings"].get("files", [])]
    rows = []
    for f in frames:
        for i in range(len(f["form"])):
            rows.append(dict(cik=cik, form=f["form"][i], filed=f["filingDate"][i], accn=f["accessionNumber"][i],
                             report_date=f["reportDate"][i], doc=f["primaryDocument"][i]))
    return rows


# ----------------------------------------------------------------------------------------- targets
def targets() -> pd.DataFrame:
    o = pd.read_csv(DATA / "ownership.csv.gz")
    o = o[o.state.isin(["NV", "CO"]) & o.company.isin(COMPANIES)].copy()
    rows = []
    for r in o.itertuples():
        s = pd.Timestamp(r.start) if isinstance(r.start, str) else pd.Timestamp("1900-01-01")
        e = pd.Timestamp(r.end) if isinstance(r.end, str) else pd.Timestamp("2100-01-01")
        for fy in range(FY0, FY1 + 1):
            # ISLE's fiscal year ends in late April; everyone else December
            fe = pd.Timestamp(f"{fy}-04-30") if r.company == "ISLE" else pd.Timestamp(f"{fy}-12-31")
            fs = fe - pd.DateOffset(years=1) + pd.Timedelta(days=1)
            if s <= fe and e > fs:
                rows.append(dict(company=r.company, cik=int(r.cik), state=r.state, property=r.property,
                                 fiscal_year=fy, start=r.start, end=r.end, relation=r.relation,
                                 aliases=r.aliases if isinstance(r.aliases, str) else ""))
    t = pd.DataFrame(rows)
    # one row per company-property-year (a property can have several ownership rows in one year)
    t = (t.sort_values(["company", "property", "fiscal_year", "start"], na_position="first")
           .groupby(["company", "state", "property", "fiscal_year"], as_index=False)
           .agg(cik=("cik", "last"), start=("start", "first"), end=("end", "last"),
                relation=("relation", lambda x: "|".join(dict.fromkeys(x))), aliases=("aliases", "first")))
    return t


# ----------------------------------------------------------------------------------------- 10-K list
def tenk_list(t: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for comp, g in t.groupby("company"):
        ciks = {int(c): (FY0, FY1) for c in g.cik.unique()}
        for cik, a, b in EXTRA_CIKS.get(comp, []):
            ciks[cik] = (a, b)
        need = set(g.fiscal_year)
        for cik, (a, b) in ciks.items():
            for f in submissions_json(cik):
                if f["form"] not in ("10-K", "10-KT", "10-K405") or not f["report_date"]:
                    continue
                fy = int(f["report_date"][:4])
                if fy in need and a <= fy <= b:
                    rows.append(dict(company=comp, fiscal_year=fy, **f))
    k = pd.DataFrame(rows).sort_values(["company", "fiscal_year", "filed"])
    # the original 10-K per company-year (a second 10-K for the same year would be a re-filing)
    k = k.drop_duplicates(["company", "fiscal_year", "cik"], keep="first")
    # PNK: two registrants hold the same property; keep one 10-K per year (latest CIK wins)
    k = k.sort_values(["company", "fiscal_year", "cik"]).drop_duplicates(["company", "fiscal_year"], keep="last")
    return k.reset_index(drop=True)


def doc_path(r) -> Path:
    return TENK / f"{r.company}_{r.fiscal_year}_{r.accn}.htm.gz"


def download(k: pd.DataFrame):
    TENK.mkdir(parents=True, exist_ok=True)
    for r in k.itertuples():
        p = doc_path(r)
        if p.exists():
            continue
        url = f"https://www.sec.gov/Archives/edgar/data/{r.cik}/{r.accn.replace('-', '')}/{r.doc}"
        resp = http_get(url)
        if resp is None:
            print("  missing", url, file=sys.stderr)
            continue
        with gzip.open(p, "wb") as f:
            f.write(resp.content)
        print("  got", p.name, len(resp.content) // 1000, "kB", flush=True)


# ----------------------------------------------------------------------------------------- parsing
PARSED = TENK / "parsed"
ZW = dict.fromkeys(map(ord, "\u200b\u200e\u200f\ufeff\u2060"), None)


def clean(s: str) -> str:
    s = s.translate(ZW).replace("\xa0", " ").replace("\u2019", "'").replace("\u2018", "'")
    s = re.sub(r"[\u2010-\u2015\u2500\u2212]", "-", s)     # dashes and box-drawing line -> "-"
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s).strip()


def parse_doc(path: Path) -> dict:
    """{'tables': [[[start, span, text], ...] per row] per table], 'text': plain text}; cached."""
    out = PARSED / path.name.replace(".htm.gz", ".json.gz")
    if out.exists():
        with gzip.open(out, "rt") as f:
            return json.load(f)
    import warnings
    from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
    with gzip.open(path) as f:
        soup = BeautifulSoup(f.read(), "lxml")
    tables = []
    for tb in soup.find_all("table"):
        tt = clean(tb.get_text(" ")).lower()
        if not re.search(r"slot|machines|devices|vlt|gaming positions|gaming", tt):
            continue
        rows = []
        for tr in tb.find_all("tr"):
            col, cells = 0, []
            for td in tr.find_all(["td", "th"]):
                try:
                    span = max(1, int(str(td.get("colspan", "1")).strip() or 1))
                except ValueError:
                    span = 1
                x = clean(td.get_text(" "))
                if x and x not in ("$", ")", "%", "(", "*"):
                    cells.append([col, span, x])
                col += span
            if cells:
                rows.append(cells)
        if rows:
            tables.append(rows)
    for br in soup.find_all(["br"]):
        br.replace_with(" ")
    text = clean(soup.get_text(" "))
    d = dict(tables=tables, text=text)
    out.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out, "wt") as f:
        json.dump(d, f)
    return d


# ----------------------------------------------------------------------------------------- patterns
# Row-name patterns (regex, matched case-insensitively at the start of the property-name cell after
# clean(): curly quotes -> ', dashes -> -).  A tuple (regex, ctx) additionally requires ctx to match
# the table section heading or the row's other cells (e.g. a location column).
LV = r"Las Vegas|Nev|NV|Henderson"
PATTERNS = {
    "AFFI": {
        "Buffalo Bill's Resort & Casino": [r"Buffalo Bill"],
        "Dayton Depot Casino": [r"Dayton"],
        "Gold Ranch Casino & RV Resort": [r"Gold Ranch"],
        "Henderson Casino Bowl": [r"(Terrible's )?Henderson Casino"],
        "Primm Valley Resort & Casino": [r"Primm Valley"],
        "Rail City Casino": [r"(Terrible's )?Rail City"],
        "Sands Regency Casino Hotel": [r"(The )?Sands Regency", r"Sands\b"],
        "Searchlight Casino": [r"(Terrible's )?Searchlight"],
        "Silver Sevens Hotel & Casino": [r"Silver Sevens", r"Terrible's (Las Vegas|Hotel)"],
        "Terrible's Lakeside Casino & RV Park (Pahrump)": [(r"(Terrible's )?Lakeside", r"Pahrump")],
        "Terrible's Town Casino (Pahrump)": [r"(Terrible's )?Town Casino"],
        "Whiskey Pete's Hotel & Casino": [r"Whiskey Pete"],
    },
    "BALY": {
        "Bally's Lake Tahoe Casino Resort": [r"Bally's Lake Tahoe", r"MontBleu"],
        "Tropicana Las Vegas": [r"Tropicana Las Vegas"],
    },
    "BYD": {
        "Aliante Casino + Hotel + Spa": [r"Aliante"],
        "Cadence Crossing Casino": [r"Cadence Crossing"],
        "California Hotel and Casino": [r"(The )?California Hotel"],
        "Cannery Casino Hotel": [r"(The )?Cannery"],
        "Eastside Cannery Casino and Hotel": [r"Eastside Cannery"],
        "Eldorado Casino": [r"Eldorado Casino"],
        "Fremont Hotel & Casino": [r"Fremont Hotel"],
        "Gold Coast Hotel and Casino": [r"Gold Coast"],
        "Jokers Wild Casino": [r"Joker'?s Wild"],
        "Main Street Station Hotel and Casino": [r"Main Street Station"],
        "Sam's Town Hotel and Gambling Hall Las Vegas": [(r"Sam's Town", r"Las Vegas")],
        "Suncoast Hotel and Casino": [r"Suncoast"],
        "The Orleans Hotel and Casino": [r"(The )?Orleans Hotel"],
    },
    "CNTY": {
        "Century Casino & Hotel - Central City": [r"Century Casino (& Hotel )?(- )?Central City", r"Central City"],
        "Century Casino & Hotel - Cripple Creek": [r"Century Casino (& Hotel )?(- )?Cripple Creek", r"Cripple Creek"],
        "Nugget Casino Resort": [r"(The )?Nugget Casino Resort", r"Nugget\b"],
    },
    "FLL": {
        "Bronco Billy's Casino": [r"Bronco Billy"],
        "Chamonix Casino Hotel": [r"Chamonix"],
        "Grand Lodge Casino": [r"Grand Lodge"],
        "Stockman's Casino": [r"Stockman"],
    },
    "GDEN": {
        "Aquarius Casino Resort": [r"Aquarius"],
        "Arizona Charlie's Boulder": [r"Arizona Charlie'?s Boulder"],
        "Arizona Charlie's Decatur": [r"Arizona Charlie'?s Decatur"],
        "Colorado Belle Hotel & Casino Resort": [r"Colorado Belle"],
        "Edgewater Hotel & Casino Resort": [r"Edgewater"],
        "Gold Town Casino": [r"Gold Town"],
        "Lakeside Casino & RV Park": [r"Lakeside Casino"],
        "Pahrump Nugget": [r"Pahrump Nugget"],
        "The STRAT Hotel, Casino & Tower": [r"(The )?STRAT\b", r"Stratosphere"],
    },
    "ISLE": {
        "Isle Casino Hotel Black Hawk": [r"Isle (Casino Hotel|of Capri)( -)? ?-? ?Black Hawk", r"Isle Casino Hotel"],
        "Lady Luck Casino Black Hawk": [(r"Lady Luck", r"Black Hawk")],
    },
    "MGM": {
        "Aria (CityCenter)": [r"Aria\b", r"CityCenter"],
        "Bellagio": [r"Bellagio"],
        "Circus Circus Las Vegas": [r"Circus Circus Las Vegas", (r"Circus Circus$", r"Las Vegas")],
        "Circus Circus Reno": [r"Circus Circus Reno", (r"Circus Circus", r"Reno")],
        "Excalibur": [r"Excalibur"],
        "Gold Strike Jean": [(r"Gold Strike(?! Tunica)", r"Jean|Nevada")],
        "Luxor": [r"Luxor"],
        "MGM Grand Las Vegas": [r"MGM Grand Las Vegas"],
        "Mandalay Bay": [r"Mandalay Bay"],
        "New York-New York": [r"New York ?- ?New York"],
        "Park MGM": [r"Park MGM", r"Monte Carlo"],
        "Railroad Pass": [r"Railroad Pass"],
        "Silver Legacy Reno": [r"Silver Legacy"],
        "The Cosmopolitan of Las Vegas": [r"(The )?Cosmopolitan"],
        "The Mirage": [r"(The )?Mirage"],
    },
    "PENN": {
        "Ameristar Black Hawk": [r"Ameristar Black Hawk"],
        "Bullwhackers": [r"Bullwhackers"],
        "M Resort Spa Casino": [r"(The )?M Resort"],
        "Tropicana Las Vegas": [r"Tropicana Las Vegas"],
    },
    "PNK": {
        "Ameristar Black Hawk": [r"Ameristar Black Hawk"],
        "Boomtown Reno": [r"Boomtown Reno"],
    },
    "RRR": {
        "Barley's Casino & Brewing Company": [r"Barley"],
        "Boulder Station": [r"Boulder Station"],
        "Durango Casino & Resort": [r"Durango"],
        "Fiesta Henderson": [r"Fiesta Henderson"],
        "Fiesta Rancho": [r"Fiesta Rancho"],
        "Green Valley Ranch": [r"Green Valley Ranch"],
        "Palace Station": [r"Palace Station"],
        "Palms Casino Resort": [r"(The )?Palms"],
        "Red Rock Casino Resort & Spa": [r"Red Rock"],
        "Santa Fe Station": [r"Santa Fe Station"],
        "Sunset Station": [r"Sunset Station"],
        "Texas Station": [r"Texas Station"],
        "The Greens": [r"(The )?Greens"],
        "Wild Wild West Gambling Hall & Hotel": [r"Wild Wild West"],
        "Wildfire Boulder": [r"Wildfire Boulder"],
        "Wildfire Fremont": [r"Wildfire Fremont"],
        "Wildfire Lake Mead": [r"Wildfire Lake Mead", r"Lake Mead"],
        "Wildfire Lanes": [r"Wildfire Lanes"],
        "Wildfire Rancho": [r"Wildfire Rancho"],
        "Wildfire Sunset": [r"Wildfire Sunset"],
        "Wildfire Valley View": [r"Wildfire Valley View", r"The Lift"],
    },
    "TPCA": {
        "MontBleu Resort Casino & Spa": [r"MontBleu"],
        "River Palms Hotel & Casino": [r"River Palms"],
        "River Palms Hotel & Casino (leaseback period)": [r"River Palms"],
        "Tropicana Laughlin": [r"Tropicana Laughlin"],
    },
    "WYNN": {
        "Wynn Las Vegas (incl. Encore)": [r"Las Vegas Operations", r"Wynn Las Vegas"],
    },
}
CAESARS = {
    "Caesars Palace Las Vegas": [(r"Caesars Palace", LV)],
    "Flamingo Las Vegas": [(r"Flamingo( Las Vegas)?\b(?! Laughlin)", r"Las Vegas")],
    "Harrah's Lake Tahoe": [r"Harrah's (Lake )?Tahoe"],
    "Harrah's Las Vegas": [r"Harrah's Las Vegas"],
    "Harrah's Laughlin": [r"Harrah's Laughlin"],
    "Harrah's Reno": [r"Harrah's Reno"],
    "Paris Las Vegas": [r"Paris Las Vegas", (r"Paris\b", LV)],
    "Planet Hollywood Resort & Casino": [r"Planet Hollywood"],
    "Rio All-Suite Hotel & Casino": [(r"Rio\b", LV)],
    "The LINQ Hotel & Casino": [r"(The )?LINQ(?! Promenade)", r"(The )?Quad\b", r"Imperial Palace"],
}
PATTERNS["CZR_OLD"] = dict(CAESARS, **{
    "Bally's Las Vegas": [r"Bally's Las Vegas"],
    "Harveys Lake Tahoe": [r"Harvey'?s (Lake )?Tahoe", r"Harveys Resort"],
    "The Cromwell": [r"(The )?Cromwell", r"Bill's Gamblin"],
})
PATTERNS["ERI_CZR"] = dict(CAESARS, **{
    "Horseshoe Las Vegas": [r"Horseshoe Las Vegas", r"Bally's Las Vegas"],
    "Caesars Republic Lake Tahoe": [r"Caesars Republic (Lake )?Tahoe", r"Harvey'?s (Lake )?Tahoe"],
    "The Vanderpump Hotel": [r"(The )?Vanderpump", r"(The )?Cromwell"],
    "Horseshoe Black Hawk": [r"Horseshoe Black Hawk", r"Isle (Casino Hotel|Casino|of Capri)?( -)? ?-? ?Black Hawk",
                             r"Isle Casino Hotel"],
    "Lady Luck Casino - Black Hawk": [(r"Lady Luck", r"Black Hawk")],
    "Circus Circus Reno": [r"Circus (Circus )?Reno"],
    "Eldorado Resort Casino Reno": [r"Eldorado (Resort Casino |Hotel Casino )?Reno"],
    "MontBleu Resort Casino & Spa": [r"MontBleu"],
    "Silver Legacy Resort Casino": [r"Silver Legacy"],
    "Tamarack Junction": [r"Tamarack"],
    "Tropicana Laughlin Hotel & Casino": [r"Tropicana Laughlin"],
})
# rows that print one figure for several of our properties: (company, row regex) -> (members, row that
# carries the figure).  The other members get a blank with a note, so company sums stay right.
COMBINED = {
    ("AFFI", r"Black Hawk Casinos"): (["Golden Gates Casino", "Golden Gulch Casino", "Golden Mardi Gras Casino"],
                                      "Golden Gates Casino"),
    ("BALY", r"(Black Hawk Casinos|Bally's Black Hawk\b)"): (
        ["Bally's Black Hawk East Casino", "Bally's Black Hawk North Casino", "Bally's Black Hawk West Casino"],
        "Bally's Black Hawk East Casino"),
    ("PENN", r"Cactus Pete'?s and Horseshu"): (["Cactus Petes", "Horseshu"], "Cactus Petes"),
    ("PNK", r"Cactus Pete'?s and Horseshu"): (["Cactus Petes Resort Casino", "Horseshu Hotel & Casino"],
                                              "Cactus Petes Resort Casino"),
    ("FLL", r"(Chamonix.*Bronco|Bronco.*Chamonix)"): (["Bronco Billy's Casino", "Chamonix Casino Hotel"],
                                                     "Bronco Billy's Casino"),
}

# ----------------------------------------------------------------------------------------- tables
SLOT_H = re.compile(r"slot|machines|devices|\bEGMs?\b|gaming positions", re.I)
TABLE_H = re.compile(r"\btables?\b|table games|table and poker", re.I)
NOT_H = re.compile(r"handle|\bwin\b|hold|revenue|per unit|average|drop|participation|liabilit|expense", re.I)
FOOT = re.compile(r"^(\((\d{1,2}|[a-z]{1,2})\)\s*)+$|^\*+$")


def num(x: str):
    """Printed count -> (int or None, kind): kind 'n' number, 'dash' printed as a dash, 'na', 'text'."""
    x = x.strip()
    x = re.sub(r"(\s*\((\d{1,2}|[a-z]{1,2})\))+$", "", x).strip().rstrip("*").strip()
    x = re.sub(r"^(approx\.?|approximately|~)\s*", "", x, flags=re.I)
    if re.fullmatch(r"-+", x) or x.lower() == "none":
        return 0, "dash"
    if x.upper() in ("N/A", "NA"):
        return None, "na"
    m = re.fullmatch(r"\d{1,3}(,\d{3})+|\d+", x)
    if m:
        return int(x.replace(",", "")), "n"
    # a number split by stray markup ("49 8" = 498, CNTY FY2013/14/17/18); never a comma group + footnote
    j = x.replace(" ", "")
    if re.fullmatch(r"\d[\d ]*\d", x) and re.fullmatch(r"\d{1,3}(,\d{3})+|\d+", j) and len(j) <= 4:
        return int(j), "split"
    return None, "text"


def header_cols(row):
    texts = [c[2] for c in row]
    if any(len(x) > 90 for x in texts) or texts[0].startswith(("•", "·", "◦")):
        return None
    si = [i for i, x in enumerate(texts) if SLOT_H.search(x) and not NOT_H.search(x)]
    ti = [i for i, x in enumerate(texts) if TABLE_H.search(x) and not SLOT_H.search(x) and not NOT_H.search(x)]
    if si and ti and si[0] != ti[0]:
        return si[0], ti[0]
    return None


def pick(row, hdr, hi):
    """Value of header column hi in data row: grid overlap first, then position counting."""
    hs, hspan = hdr[hi][0], hdr[hi][1]
    grid = [c for c in row[1:] if c[0] < hs + hspan and c[0] + c[1] > hs]
    g = None
    for c in grid:
        v = num(c[2])
        if v[1] != "text" or not FOOT.match(c[2]):
            g = v + (c[2],)
            break
        g = (None, "foot", c[2])
    vals = row[1:]
    j = None
    if len(vals) == len(hdr):
        j = hi
    elif len(vals) == len(hdr) - 1:
        j = hi - 1
    elif len(vals) > len(hdr):
        j = hi + len(vals) - len(hdr)
    cnt = None
    if j is not None and 0 <= j < len(vals):
        cnt = num(vals[j][2]) + (vals[j][2],)
    return g, cnt


def match_name(name: str, ctx: str, pats) -> bool:
    for p in pats:
        rx, cx = (p, None) if isinstance(p, str) else p
        if re.match(rx, name, re.I) and (cx is None or re.search(cx, name + " | " + ctx, re.I)):
            return True
    return False


# Property tables whose column headings sit outside the HTML table (PENN FY2016-2017, FY2021 on): the
# layout is fixed (... | Gaming Square Footage | Gaming Machines | Table Games | Hotel Rooms), so the
# counts are the 3rd- and 2nd-last cells of rows whose facility-type cell says "... gaming".
HEADERLESS = {"PENN": (-3, -2, r"\| (Land|Dockside|Riverboat)[- ]*based gaming|\| Dockside gaming|\| Land ?- ?based gaming")}


def table_rows(doc: dict, company: str = ""):
    """Yield (table_no, name, section+row context, slots_cell, tables_cell) for data rows under a
    slot/table header.  *_cell = (value, kind, raw text, method)."""
    for ti, tb in enumerate(doc["tables"]):
        hdr, cols, section = None, None, ""
        for row in tb:
            hc = header_cols(row)
            if hc:
                hdr, cols = row, hc
                continue
            if hdr is None:
                if company in HEADERLESS and len(row) >= 5:
                    si, tj, rx = HEADERLESS[company]
                    ctx = " | " + " | ".join(c[2] for c in row[1:])
                    if re.search(rx, ctx, re.I) and num(row[0][2])[1] == "text":
                        yield (ti, row[0][2], ctx, num(row[si][2]) + (row[si][2], "headerless"),
                               num(row[tj][2]) + (row[tj][2], "headerless"))
                continue
            if len(row) == 1:
                if num(row[0][2])[1] == "text":
                    section = row[0][2]
                continue
            name = row[0][2]
            if num(name)[1] != "text" or len(name) > 160:
                continue
            out = []
            for hi in cols:
                g, c = pick(row, hdr, hi)
                if g is not None and g[1] != "foot":
                    out.append(g + ("grid",) + ((c,) if c and c[:2] != g[:2] else ()))
                elif c is not None:
                    out.append(c + ("count",))
                elif g is not None:
                    out.append(g + ("grid",))
                else:
                    out.append((None, "missing", "", "none"))
            ctx = section + " | " + " | ".join(c[2] for c in row[1:])
            yield ti, name, ctx, out[0], out[1]


# ----------------------------------------------------------------------------------------- prose
# Where a 10-K describes a property in words ("... offered 1,232 slots, 33 table games ..."), the counts
# are read from the text that follows a mention of the property, cut at the next mention of another
# of the company's properties (STOP).  The first mention followed by a slot count wins.
PROSE = {
    "MCRI": {"Atlantis Casino Resort Spa": [r"Atlantis Casino Resort Spa", r"The Atlantis\b"],
             "Monarch Casino Resort Spa Black Hawk": [r"Monarch Casino Resort Spa Black Hawk", r"Monarch Black Hawk",
                                                      r"(The )?Monarch Casino Black Hawk", r"Riviera Black Hawk"]},
    "CHDN": {"Saratoga Casino Black Hawk": [r"Saratoga's Colorado facility", r"Saratoga Casino Black Hawk"]},
    "WYNN": {"Wynn Las Vegas (incl. Encore)": [r"Wynn Las Vegas \| Encore features", r"Our integrated Las Vegas resort",
                                               r"Wynn Las Vegas features", r"Las Vegas Operations Wynn Las Vegas",
                                               r"Wynn Las Vegas\b"]},
    "FLL": {"Grand Lodge Casino": [r"Grand Lodge"], "Stockman's Casino": [r"Stockman's"],
            "Bronco Billy's Casino": [r"Our Cripple Creek operations", r"Bronco Billy's"]},
    "GDEN": {"Pahrump Nugget": [r"Pahrump Nugget"], "Gold Town Casino": [r"Gold Town Casino"],
             "Lakeside Casino & RV Park": [r"Lakeside Casino & RV Park"], "Aquarius Casino Resort": [r"(The )?Aquarius"],
             "The STRAT Hotel, Casino & Tower": [r"(The )?Stratosphere", r"The STRAT\b"],
             "Arizona Charlie's Decatur": [r"Arizona Charlie's Decatur"],
             "Arizona Charlie's Boulder": [r"Arizona Charlie's Boulder"],
             "Edgewater Hotel & Casino Resort": [r"(The )?Edgewater"],
             "Colorado Belle Hotel & Casino Resort": [r"(The )?Colorado Belle"]},
    "ERI_CZR": {"Eldorado Resort Casino Reno": [r"Eldorado Reno (currently )?offers"],
                "Silver Legacy Resort Casino": [r"Silver Legacy (currently )?(offers|features)"],
                "Circus Circus Reno": [r"Circus Reno (currently )?offers"]},
    "AFFI": {"Sands Regency Casino Hotel": [r"Sands Regency Casino Hotel in"],
             "Gold Ranch Casino & RV Resort": [r"Gold Ranch Casino and RV Resort in"],
             "Dayton Depot Casino": [r"Dayton Depot Casino in", r"Dayton Depot\b"]},
}
STOP = {
    "WYNN": r"Wynn Macau|Wynn Palace|Encore Boston|Encore at Wynn Macau|Macau Operations",
    "MCRI": r"Monarch Casino Resort Spa Black Hawk|Monarch (Casino )?Black Hawk|Riviera Black Hawk|Atlantis Casino Resort Spa",
    "GDEN": r"Rocky Gap|Pahrump Nugget|Gold Town|Lakeside Casino|Aquarius|Stratosphere|The Strat\b|Arizona Charlie|"
            r"Edgewater|Colorado Belle|distributed gaming|taverns",
    "FLL": r"Rising Star|Silver Slipper|American Place|Chamonix|Grand Lodge|Stockman|Bronco Billy",
    "AFFI": r"Sands Regency|Gold Ranch|Rail City|Primm|Whiskey|Buffalo Bill|Silver Sevens|Lakeside",
}
WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "no": 0})
NUMW = r"(\d{1,3}(?:,\d{3})+|\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|" \
       r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|no)"
SLOT_P = re.compile(NUMW + r"\s+(?:slots?\b|slot machines|slot and video poker machines|slot machines and VLTs|"
                    r"gaming (?:devices|machines)|electronic gaming (?:devices|machines))", re.I)
TABLE_P = re.compile(NUMW + r"\s+(?:live\s+)?(?:table games|table and poker games|gaming tables)", re.I)
POKER_P = re.compile(NUMW + r"\s+(?:live\s+)?poker tables", re.I)
FUTURE = re.compile(r"will (feature|have|include|offer)|expected to|upon completion|when complete", re.I)


def wnum(x: str) -> int:
    x = x.lower().replace(",", "")
    return int(x) if x.isdigit() else WORDS[x]


def prose_counts(text: str, anchors: list[str], stop: str | None, win: int = 900):
    """(slots, tables, snippet, future) from the first anchor mention followed by a slot count."""
    for a in anchors:
        for m in re.finditer(a, text, re.I):
            w = text[m.start(): m.start() + win]
            if stop:
                s = re.search(stop, w[len(m.group(0)) + 5:])
                if s:
                    w = w[: len(m.group(0)) + 5 + s.start()]
            sm = SLOT_P.search(w)
            if not sm:
                continue
            tm = TABLE_P.search(w, sm.start() - 150 if sm.start() > 150 else 0)
            slots = wnum(sm.group(1))
            tables = None
            if tm and abs(tm.start() - sm.start()) < 250:
                tables = wnum(tm.group(1))
                pm = POKER_P.search(w, tm.end())
                if pm and pm.start() - tm.end() < 60 and not re.search(r"includ", w[tm.end():pm.start()], re.I):
                    tables += wnum(pm.group(1))
            lo = max(0, min(sm.start(), tm.start() if tables is not None else sm.start()) - 120)
            snip = w[lo: max(sm.end(), tm.end() if tables is not None else sm.end()) + 40]
            return slots, tables, snip, bool(FUTURE.search(w[:max(sm.end(), tm.end() if tm else 0)]))
    return None


# ----------------------------------------------------------------------------------------- hand entries
# (company, property, fiscal_year) -> fields.  "slots"/"tables" override the automated value (the source is
# the 10-K of that company-year unless "accn" says otherwise); "note" is appended.  Every number here was
# read from the filing named.
HAND = {
    # FY2021 table: Stockman's table-games cell is footnote (d): "Table games operations remained closed during 2021"
    ("FLL", "Stockman's Casino", 2021): dict(tables=0, note="tables cell = footnote (d): table games closed during 2021"),
    ("MCRI", "Monarch Casino Resort Spa Black Hawk", 2014): dict(
        note="10-K adds: slot count temporarily reduced to ~620 during redesign"),
    ("MCRI", "Monarch Casino Resort Spa Black Hawk", 2020): dict(
        note="capacity after the redesign; the expanded casino opened Dec 2020"),
    ("CHDN", "Saratoga Casino Black Hawk", 2016): dict(
        note="25% equity investee; the same 10-K elsewhere says ~600 slot machines and seven table games"),
    ("FLL", "Grand Lodge Casino", 2013): dict(note="poker room's tables not counted (text gives no number)"),
    ("BYD", "Jokers Wild Casino", 2022): dict(note="as printed; out of line with FY2021 (348) and FY2023 (344)"),
}
# why a held property has no count although the company-year 10-K exists: (company, fiscal_year, property or None)
MISSING_NOTE = {
    ("BALY", 2024, None): "property table in this 10-K gives casino square footage only (no slot or table counts)",
    ("BALY", 2025, None): "property table in this 10-K gives casino square footage only (no slot or table counts)",
    ("CZR_OLD", 2015, None): "CEOC property (deconsolidated Jan 2015 - Oct 2017); 10-K property table lists only CERP/CGP properties",
    ("CZR_OLD", 2016, None): "CEOC property (deconsolidated Jan 2015 - Oct 2017); 10-K property table lists only CERP/CGP properties",
    ("RRR", 2012, "Wildfire Lake Mead"): "not in the Station Casinos LLC property table (first listed FY2014)",
    ("RRR", 2013, "Wildfire Lake Mead"): "not in the Station Casinos LLC property table (first listed FY2014)",
    ("AFFI", 2012, None): "not in this 10-K (sold Feb 2012, before the FY2012 10-K)",
    ("CHDN", 2018, None): "no counts in this 10-K (25% stake sold 2018-08-31)",
}
NO_10K = {
    ("ERI_CZR", 2012): "no 10-K: Eldorado Resorts was private before the Sept 2014 MTR Gaming merger",
    ("ERI_CZR", 2013): "no 10-K: Eldorado Resorts was private before the Sept 2014 MTR Gaming merger",
    ("AFFI", 2016): "no 10-K: Affinity Gaming taken private Jan 2017 before filing a FY2016 10-K",
    ("AFFI", 2017): "no 10-K: Affinity Gaming taken private Jan 2017",
    ("CZR_OLD", 2020): "no 10-K: merged into Eldorado (ERI_CZR) July 2020",
    ("ISLE", 2017): "no 10-K: acquired by Eldorado May 1 2017, before a FY2017 (Apr) 10-K",
    ("PNK", 2018): "no 10-K: acquired by Penn Oct 2018",
    ("TPCA", 2018): "no 10-K: acquired by Eldorado Oct 2018",
}


# ----------------------------------------------------------------------------------------- build
def describe(cell, what):
    """(value, note) for one table cell of kind n / dash / na / text / foot."""
    v, kind, raw = cell[0], cell[1], cell[2]
    if kind == "n":
        return v, ""
    if kind == "split":
        return v, f'{what} cell printed as "{raw}" (digits split by markup), read as {v}'
    if kind == "dash":
        if what == "slots":
            return None, "slots printed '-'"
        return 0, ""
    if kind == "na":
        return None, f"{what} printed 'N/A'"
    return None, f'{what} cell reads "{raw[:20]}"'


def extract_company_year(r, props: list[str]) -> dict:
    """property -> dict(slots, tables, note) for one 10-K."""
    doc = parse_doc(doc_path(r))
    pats = PATTERNS.get(r.company, {})
    comb = [(rx, v) for (c, rx), v in COMBINED.items() if c == r.company]
    hits = {}
    for ti, name, ctx, sc, tc in table_rows(doc, r.company):
        nm = clean(name)
        tgt, cm = None, None
        for rx, (members, primary) in comb:
            if re.search(rx, nm, re.I):
                tgt, cm = primary, members
        if tgt is None:
            for p in props:
                if match_name(nm, ctx, pats.get(p, [])):
                    tgt = p
                    break
        if tgt and tgt in props:
            hits.setdefault(tgt, []).append((ti, nm, sc, tc, cm))
    out = {}
    for p, h in hits.items():
        good = [x for x in h if x[2][1] == "n"] or h          # prefer a row with a numeric slot count
        ti, nm, sc, tc, cm = good[0]
        s, n1 = describe(sc, "slots")
        tb, n2 = describe(tc, "tables")
        notes = [x for x in (n1, n2) if x]
        if sc[1] == "dash" and tc[1] == "dash":        # whole row dashed: property closed, not zero tables
            tb, notes = None, ["slots and tables printed '-' (property closed)"]
        if sc[3] == "headerless":
            notes.append("table without heading row; columns by position")
        if any(len(c) > 4 for c in (sc, tc)):
            notes.append("column read from cell positions under the heading (row has a blank cell)")
        other = {(x[2][0], x[3][0]) for x in good[1:] if x[2][1] == "n"} - {(sc[0], tc[0])}
        if other:
            notes.append("another table in the 10-K prints " + ", ".join(f"{a}/{b}" for a, b in sorted(other)))
        if cm:
            notes.insert(0, f'combined row "{nm[:60]}" covers {" + ".join(cm)}')
            for m in cm:
                if m != p and m in props:
                    out[m] = dict(slots=None, tables=None,
                                  note=f'included in the combined figure on the "{p}" row ("{nm[:60]}")')
        out[p] = dict(slots=s, tables=tb, note="; ".join([f'table row "{nm[:60]}"'] + notes))
    # prose fallback
    for p in props:
        if p in out or p not in PROSE.get(r.company, {}):
            continue
        res = prose_counts(doc["text"], PROSE[r.company][p], STOP.get(r.company))
        if res:
            s, tb, snip, fut = res
            note = 'text: "...' + snip.strip()[:170] + '..."'
            if fut:
                note = "FORWARD-LOOKING " + note
            if tb is None:
                note += "; no table-game count in the text"
            out[p] = dict(slots=s, tables=tb, note=note)
    return out


def build() -> pd.DataFrame:
    t = targets()
    k = tenk_list(t)
    rows = []
    for (comp, fy), g in t.groupby(["company", "fiscal_year"]):
        kk = k[(k.company == comp) & (k.fiscal_year == fy)]
        props = g.property.tolist()
        got, accn, form = {}, "", ""
        if len(kk):
            r = kk.iloc[0]
            got = extract_company_year(r, props)
            accn = r.accn
            if int(r.cik) in [c for c, _, _ in EXTRA_CIKS.get(comp, [])]:
                form = "Station Casinos LLC 10-K (RRR predecessor); "
        for x in g.itertuples():
            d = dict(got.get(x.property, {}))
            if not len(kk):
                d = dict(slots=None, tables=None, note=NO_10K.get((comp, fy), "no 10-K found"))
            elif not d:
                sold = isinstance(x.end, str) and pd.Timestamp(x.end) <= pd.Timestamp(f"{fy}-12-31")
                why = MISSING_NOTE.get((comp, fy, x.property)) or MISSING_NOTE.get((comp, fy, None))
                d = dict(slots=None, tables=None,
                         note=why or ("not in this 10-K" + (f" (held until {x.end})" if sold else "")))
            h = HAND.get((comp, x.property, fy), {})
            for f in ("slots", "tables"):
                if f in h:
                    d[f] = h[f]
            note = form + d.get("note", "")
            if h.get("note"):
                note = note + "; " + h["note"]
            rows.append(dict(company=comp, state=x.state, property=x.property, fiscal_year=fy,
                             slots=d.get("slots"), tables=d.get("tables"),
                             source_accession=h.get("accn", accn), note=note.strip("; ")))
    df = pd.DataFrame(rows)
    for c in ("slots", "tables"):
        df[c] = df[c].astype("Int64")
    return df


if __name__ == "__main__":
    steps = [a for a in sys.argv[1:] if a in ("--download", "--parse", "--build")] or ["--download", "--parse", "--build"]
    t = targets()
    k = tenk_list(t)
    print(len(t), "company-property-years;", len(k), "10-Ks")
    if "--download" in steps:
        download(k)
    if "--parse" in steps:
        for r in k.itertuples():
            parse_doc(doc_path(r))
    if "--build" in steps:
        df = build()
        df.to_csv(DATA / "property_devices.csv.gz", index=False)
        have = df.slots.notna() | df.tables.notna()
        print(f"wrote data/property_devices.csv.gz: {len(df)} rows, {have.sum()} with a count "
              f"({have.mean():.0%}); by company:")
        print(df.assign(have=have).groupby("company").have.agg(["size", "sum"]).to_string())

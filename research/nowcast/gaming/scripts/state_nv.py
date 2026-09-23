"""Nevada: monthly casino gaming win by NGCB reporting area, 2012-01 .. latest (state_nv.py).

Run:  python3 scripts/state_nv.py [--refresh]
      (--refresh re-reads the two NGCB listing pages to pick up new months; raw PDFs are never re-downloaded.)
Output: data/state_nv.csv.gz, data/state_nv_checks.csv.gz; raw files in cache/nv/{gri,release}/.

SOURCES (Nevada Gaming Control Board, www.gaming.nv.gov)
  * Gaming Revenue Report ("GRI", ~48-page PDF per month), listing:
      https://www.gaming.nv.gov/about/gaming-revenue/information/
    One page per County/Area "All Nonrestricted Locations" (plus revenue-range pages, which are ignored).
  * Monthly press release "Monthly Win and Percentage Fee Tax Collections" (abbreviated revenue release), listing:
      https://www.gaming.nv.gov/about/abb-revenue/release/
    Used only for the publication date ("Release: <date>") and the exact statewide total gaming win (check).

UNITS: the finest non-overlapping partition of the GRI area pages (21 units): the 7 Clark County areas
  (Las Vegas Strip, Downtown Las Vegas, North Las Vegas, Laughlin, Boulder Strip, Mesquite, Balance of County),
  4 Washoe areas (Reno, Sparks, North Shore Lake Tahoe, Balance of County), Douglas County South Shore Lake Tahoe,
  Elko County Wendover + Balance of County, Carson Valley Area (Carson City + Douglas County ex South Lake Tahoe),
  Churchill, Humboldt, Lyon, Nye, White Pine counties, and "Balance of Counties". Parent pages (Clark, Washoe,
  Elko County totals) are dropped; the Statewide page becomes __STATE_TOTAL__. unit = page title exactly as
  printed (UPPER CASE through 2018-04, Title Case from 2018-05); unit_level = county for whole-county units,
  area otherwise. unit_id = NV_<title>; one rename linked: "Clark County Boulder Area" (2018-05 on) =
  "CLARK COUNTY BOULDER STRIP AREA" -> NV_CLARK_COUNTY_BOULDER_STRIP_AREA. Nonrestricted licensees only.

MEASURE ("win ex race/sports"): current-month Total Gaming Win minus Race Book and Sports Pool win (both are
  separate rows, so both are removed; sports pool includes mobile sports). Includes all slots, table/counter
  games, keno, bingo and card games (poker). slots = "Total Slot Machines" win; tables = ggr - slots (all
  non-slot games incl. poker, keno, bingo). Reported in $000 -> multiplied by 1000 (so +/- $500 rounding per
  component). Only the current-month column is used (3- and 12-month columns ignored, except below).
  Quirk: where fewer than 3 locations in an area report race book / sports pool, NGCB folds them into
  "Other" games, so a little race/sports win stays in some small areas' ggr (this is why the sum of areas
  exceeds the Statewide figure by up to 0.016%).
n_casinos: number of locations reporting slot win ("# of Loc" on the Total Slot Machines row) - a count
  that is consistent across the 2018 report redesign. (The header count "# of reporting locations" (old) /
  "Number of Reporting Licensees" (new) jumps from ~327 to ~434 in 2018-05 because of a definition change,
  so it is not used.) Blank in the 4 derived months.
n_slot_units / n_table_units (added at the end of the row, after source_file): current-month "# of Units".
  n_slot_units = units on the "Total Slot Machines" row (= sum of the denomination rows; checked, 0
  mismatches). n_table_units = sum of the units of every "Table, Counter and Card Games" row EXCEPT Race Book
  and Sports Pool, i.e. table games + card (poker) tables + keno/bingo + "other" games (checked: the games
  Total row's units = sum of rows in every page-month; pre-2016 "TOTAL GAMES" excluded the separate
  "CARD GAMES" row, which is added). Units are counted only for games reporting activity, so they drop to ~0
  in the 2020 closure. Where an area has < 3 locations with race book/sports pool these are folded into
  "Other", so their units stay in that area's n_table_units: areas sum to within 0.1-0.7% of the statewide
  table count (slots: exact). Derived months (2020-04, 2020-05, 2025-06, 2025-07): 3 x the 3-month "Avg
  Units" of the report two months later minus the two later months, floored at 0; tested on 2,900 normal
  area-months: slot units median |error| 0.08%, table units median 1.1% (areas with > 100 tables).

MONTHS: 2012-01 .. 2026-07 (175 months, no gaps).
  Four GRIs have no text layer ("Microsoft Print to PDF" images/outlines): 2020-04, 2020-05 (COVID closure,
  casinos shut 2020-03-18..06-04) and 2025-06, 2025-07. No OCR engine is installed, so these months are
  backed out of the 3-month column of the report two months later: X(m) = 3mo(m+2) - X(m+1) - X(m+2)
  (May 2020 and Jul 2025 first). measure is labelled "... (derived from 3-month column)". Validation of the
  method on 24 months whose own report exists: median |error| 0.003% for areas > $5M/month, statewide max
  0.27%, worst single area 1.9% (late-filing revisions). Derived statewide total gaming win vs the press
  release: 2025-06 +0.03%, 2025-07 -0.03%, 2020-04 -1.3% and 2020-05 +0.8% (of a ~$3.5M closure-month base).
  COVID months are therefore ~0 (small positive/negative residual win), not missing.
  2017-09: the archived GRI is a re-issue created 2018-10 (numbers revised; statewide -0.09% vs release).

PUBLICATION DATE: "Release: <date>" printed on the monthly press release (pub_source = press_release),
  all 175 months. Lag after month-end: median 29 days (24-43; 2012 releases were ~6 weeks). The GRI PDF is
  posted with the release (its own "as of" date is a few days earlier).

FORMAT NOTES: two layouts - fixed-width text with '|' column separators through 2018-04 (the current-month
  win amount is the token ending at character ~28 of the first block) and Microsoft Reporting Services from
  2018-05 (parsed from word coordinates: values right-aligned under the first "Amount" header). Pre-2016
  reports put card games in a separate "CARD GAMES" row outside "TOTAL GAMES"; later "TOTAL GAMES & TABLES"
  includes them - irrelevant here because ggr is built from Total Gaming Win.

SPOT CHECKS (data/state_nv_checks.csv.gz, all 175 months):
  * sum of the 21 areas vs Statewide page: max |diff| 0.016% in text months (0.4% in the two derived COVID
    months, tiny base). Positive diffs come from race/sports folded into "Other" in small areas.
  * Statewide total gaming win (GRI, $000) vs press-release dollars: 0.000% in 170 of 175 months; 0.095%
    (2017-09 re-issue) outside the derived months.
  * total gaming win = games + slots within $3k rounding in every page-month.
  * unit counts: the note column gives areas-minus-statewide slot and table unit differences per month.
  * units: $000 confirmed against the release's exact dollars. Month/month jumps > 3x or < 1/3 outside
    Mar-Jul 2020: one, real - South Lake Tahoe 2021-09 (x0.22; Caldor Fire evacuation, only 4 of 5 casinos
    reported).
"""
import re
import sys
import time
import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "nv"
DATA = ROOT / "data"
BASE = "https://www.gaming.nv.gov"
GRI_PAGE = BASE + "/about/gaming-revenue/information/"
REL_PAGE = BASE + "/about/abb-revenue/release/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"})
_last = [0.0]
REFRESH = "--refresh" in sys.argv   # re-read listing pages to pick up new months; raw reports are never re-fetched

MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
FIRST = "2012-01"


def fetch(url, dest, force=False):
    """Download url to dest unless cached. <= 1 request / 0.6 s, retry with backoff."""
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


def month_from_name(fn):
    """Parse report month (YYYY-MM) from NGCB file names (GRI or press release)."""
    f = Path(fn).name.lower()
    m = re.match(r"(20\d\d)([a-z]{3})-", f)                       # 2012jan-gri.pdf, 2022jan-abrrevenue.pdf
    if m:
        return f"{m.group(1)}-{MONTHS[m.group(2)]:02d}"
    m = re.match(r"arr([a-z]{3})(\d\d)\.pdf", f)                    # arrjan12.pdf
    if m:
        yy = int(m.group(2))
        return f"{1900 + yy if yy > 80 else 2000 + yy}-{MONTHS[m.group(1)]:02d}"
    m = re.match(r"mrr([a-z]{3})[a-z]*(20\d\d)\.pdf", f)            # mrrjul2026.pdf, mrrsept2025.pdf
    if m:
        return f"{m.group(2)}-{MONTHS[m.group(1)]:02d}"
    m = re.search(r"(january|february|march|april|may|june|july|august|september|october|november|december)"
                  r"-(20\d\d)", f)                                   # monthly-revenue-report---july-2026.pdf
    if m:
        return f"{m.group(2)}-{MONTHS[m.group(1)[:3]]:02d}"
    return None


def list_links(page_url, cache_name):
    html = fetch(page_url, CACHE / cache_name, force=REFRESH).read_text(encoding="utf-8", errors="ignore")
    links = sorted(set(re.findall(r'href="([^"]+\.pdf)"', html, flags=re.I)))
    out = {}
    for href in links:
        mo = month_from_name(href)
        if mo and mo >= FIRST:
            out.setdefault(mo, href)
    return out


def download_all():
    gri = list_links(GRI_PAGE, "listing_gri.html")
    rel = list_links(REL_PAGE, "listing_release.html")
    for mo, href in sorted(gri.items()):
        fetch(BASE + href if href.startswith("/") else href, CACHE / "gri" / f"gri_{mo}.pdf")
    for mo, href in sorted(rel.items()):
        fetch(BASE + href if href.startswith("/") else href, CACHE / "release" / f"release_{mo}.pdf")
    return gri, rel


# ----------------------------------------------------------------------------------------------------------
# parsing
# ----------------------------------------------------------------------------------------------------------
NUM = r"\(?-?\d[\d,]*(?:\.\d+)?\)?"


def to_num(tok):
    tok = tok.strip()
    neg = tok.startswith("(") and tok.endswith(")") or tok.startswith("-")
    v = float(tok.strip("()").replace(",", "").lstrip("-"))
    return -v if neg else v


def norm(s):
    return " ".join(s.split())


def parse_pipe_page(text):
    """Old fixed-width layout (through 2018-04): '|'-separated blocks; the first block after the label is the
    current month. Win amount tokens end at character 28 of that block (right-aligned column)."""
    lines = text.splitlines()
    head = [norm(l) for l in lines[:15] if norm(l)]
    if len(head) < 2 or head[1].upper() != "ALL NONRESTRICTED LOCATIONS":
        return None
    rec = {"area": head[0], "unit_rows": []}
    section = "games"
    for l in lines:
        if "|" not in l:
            continue
        parts = l.split("|")
        label = norm(parts[0]).upper()
        cur = parts[1] if len(parts) > 1 else ""
        m = re.search(r"REPORTING LOCATIONS\s*--\s*([\d,]+)", cur)
        if m and "n_loc" not in rec:
            rec["n_loc"] = int(m.group(1).replace(",", ""))
            continue
        if label.startswith("SLOT MACHINES"):
            section = "slots"
            continue
        def block_win(block):
            w = None
            for t in re.finditer(r"-?\d[\d,]*(?:\.\d+)?", block):
                if 25 <= t.end() <= 31 and "." not in t.group():
                    w = to_num(t.group())
            return w
        def block_units(block):                 # '# OF UNITS' column: token ending at character 14-19
            u = None
            for t in re.finditer(r"\d[\d,]*(?:\.\d+)?", block):
                if 14 <= t.end() <= 19 and "." not in t.group():
                    u = int(to_num(t.group()))
            return u
        toks = list(re.finditer(r"-?\d[\d,]*(?:\.\d+)?", cur))
        win = block_win(cur)
        win3 = block_win(parts[2]) if len(parts) > 2 else None
        u, u3 = block_units(cur), (block_units(parts[2]) if len(parts) > 2 else None)
        if section in ("games", "slots") and (u is not None or u3 is not None or win is not None):
            rec["unit_rows"].append((section, label, u, u3))      # also rows with a blank win (e.g. race book)
        if win is None and win3 is None:
            continue
        if label.startswith("TOTAL GAMING"):
            section = "footer"
        key = None
        if label.startswith("RACE BOOK"):
            key = "race"
        elif label.startswith("SPORTS POOL") and "DETAIL" not in label:
            key = "sports"
        elif label.startswith("TOTAL GAMES"):          # 'TOTAL GAMES' (excl. card games) or 'TOTAL GAMES & TABLES'
            key = "games_total"
            rec["games_incl_card"] = "&" in label
        elif label.startswith("CARD GAMES"):
            key = "card"
        elif label.startswith("TOTAL SLOT"):
            key = "slots"
            if toks and toks[0].end() <= 12:                 # '# OF LOC'S' column (locations with slot win)
                rec["n_slot_loc"] = int(to_num(toks[0].group()))
        elif label.startswith("TOTAL GAMING"):
            key = "tgw"
        if key and key not in rec:
            rec[key] = win if win is not None else 0.0
            rec[key + "_3m"] = win3 if win3 is not None else 0.0
    return rec


def parse_new_page(page):
    """Reporting Services layout (2018-05 on): use word coordinates. The current-month 'Win Amount' column is
    the first 'Amount' header; values are right-aligned to it."""
    words = page.get_text("words")
    rows = {}
    for w in words:
        rows.setdefault(round((w[1] + w[3]) / 2 / 3), []).append(w)
    rows = [sorted(v) for _, v in sorted(rows.items())]
    title = None
    for r in rows[:8]:
        t = norm(" ".join(w[4] for w in r))
        if t.endswith("All Nonrestricted Locations"):
            title = t[: -len("All Nonrestricted Locations")].rstrip(" -")
            break
        if "Revenue Range" in t:
            return None
    if not title:
        return None
    amt = [w for w in words if w[4] == "Amount"]
    if not amt:
        return None
    amt = sorted(amt, key=lambda w: w[0])
    x_win = amt[0][2]                                          # right edge of the current-month 'Amount' header
    x_win3 = amt[1][2] if len(amt) > 1 else None               # ... and of the three-month 'Amount' header
    units_hdr = sorted([w for w in words if w[4] == "Units" and w[3] < 200], key=lambda w: w[0])
    x_u = units_hdr[0][2] if units_hdr else None                # current-month '# Of Units'
    x_u3 = units_hdr[1][2] if len(units_hdr) > 1 else None      # three-month 'Avg Units'
    rec = {"area": title, "games_incl_card": True, "unit_rows": []}
    section = None
    for r in rows:
        label = norm(" ".join(w[4] for w in r if w[2] < 140))
        full = norm(" ".join(w[4] for w in r))
        if "Number of Reporting Licensees" in full and "n_loc" not in rec:
            m = re.search(r"Licensees\s*-\s*([\d,]+)", full)
            if m:
                rec["n_loc"] = int(m.group(1).replace(",", ""))
            continue
        if label.startswith("Table, Counter"):
            section = "games"
            continue
        if label.startswith("Slot Machines"):
            section = "slots"
            continue
        vals = [w for w in r if w[0] > 140 and abs(w[2] - x_win) <= 8 and re.fullmatch(NUM, w[4])]
        vals3 = [w for w in r if x_win3 and abs(w[2] - x_win3) <= 8 and re.fullmatch(NUM, w[4])]
        if not vals and not vals3:
            continue
        win = to_num(vals[0][4]) if vals else 0.0
        win3 = to_num(vals3[0][4]) if vals3 else 0.0
        if section in ("games", "slots") and not label.startswith("Total Gaming"):
            uu = [w for w in r if x_u and abs(w[2] - x_u) <= 8 and re.fullmatch(r"[\d,]+", w[4])]
            uu3 = [w for w in r if x_u3 and abs(w[2] - x_u3) <= 8 and re.fullmatch(r"[\d,]+", w[4])]
            rec["unit_rows"].append((section, label.upper(), int(to_num(uu[0][4])) if uu else None,
                                     int(to_num(uu3[0][4])) if uu3 else None))
        key = None
        if label.startswith("Race Book") and section == "games":
            key = "race"
        elif label.startswith("Sports Pool") and section == "games":
            key = "sports"
        elif label == "Card Games" and section == "games":
            key = "card"
        elif label == "Total" and section == "games":
            key = "games_total"
        elif label == "Total" and section == "slots":
            key = "slots"
            locs = [w for w in r if 140 < w[0] and w[2] < 165 and re.fullmatch(r"[\d,]+", w[4])]
            if locs:
                rec["n_slot_loc"] = int(to_num(locs[0][4]))
        elif label.startswith("Total Gaming"):
            key = "tgw"
            section = "footnotes"
        if key and key not in rec:
            rec[key] = win
            rec[key + "_3m"] = win3
    return rec


def parse_gri(path):
    import pymupdf
    doc = pymupdf.open(path)
    out = []
    for page in doc:
        text = page.get_text()
        if "|" in text[:3000]:
            rec = parse_pipe_page(text)
        else:
            rec = parse_new_page(page)
        if rec and "tgw" in rec:
            unit_counts(rec)
            out.append(rec)
    return out


def unit_counts(rec):
    """n_slot_units = slot-machine units (Total Slot Machines row, else sum of denomination rows);
    n_table_units = units of all table, counter and card-game rows except race book and sports pool
    (i.e. table games + poker tables + keno/bingo 'units' + 'other'). Same for the 3-month average columns.
    Also records whether the games 'Total' row's units equal the row sum (a parse check)."""
    rows = rec.pop("unit_rows", [])
    for suf, i in (("", 2), ("_3m", 3)):
        slot_tot = [r[i] for r in rows if r[0] == "slots" and r[1].startswith("TOTAL")]
        slot_rows = [r[i] or 0 for r in rows if r[0] == "slots" and not r[1].startswith("TOTAL")]
        game_rows = [r for r in rows if r[0] == "games" and not r[1].startswith("TOTAL")]
        rec["slot_units" + suf] = slot_tot[0] if slot_tot and slot_tot[0] is not None else sum(slot_rows)
        rec["table_units" + suf] = sum(r[i] or 0 for r in game_rows
                                       if not r[1].startswith(("RACE BOOK", "SPORTS POOL")))
        if suf == "":
            gt = [r for r in rows if r[0] == "games" and r[1].startswith("TOTAL")]
            if gt and gt[0][i] is not None:
                incl = [r[i] or 0 for r in game_rows
                        if rec.get("games_incl_card", True) or not r[1].startswith("CARD GAMES")]
                rec["units_check"] = gt[0][i] - sum(incl)
            if slot_tot and slot_tot[0] is not None:
                rec["slot_units_check"] = slot_tot[0] - sum(slot_rows)


def parse_release(path):
    """Press release: release date, report month, statewide total gaming win (dollars)."""
    import pymupdf
    t = " ".join(pymupdf.open(path)[0].get_text().split())
    rel = re.search(r"Release:\s*([A-Z][a-z]+\.?\s+\d{1,2},?\s+\d{4})", t)
    mon = re.search(r"Win Revenue Summary\s*[-–—]+\s*([A-Z][a-z]+)\s+(\d{4})", t)
    tot = re.search(r"gaming win\W{0,3}\s*of\s*\$?([\d,]+)", t)
    d = {}
    if rel:
        s = rel.group(1).replace(".", "").replace(",", "")
        for fmt in ("%B %d %Y", "%b %d %Y"):
            try:
                d["pub_date"] = dt.datetime.strptime(s, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                pass
    if mon:
        d["month"] = f"{mon.group(2)}-{MONTHS[mon.group(1)[:3].lower()]:02d}"
    if tot:
        d["tgw_release"] = float(tot.group(1).replace(",", ""))
    return d


# ----------------------------------------------------------------------------------------------------------
# build
# ----------------------------------------------------------------------------------------------------------
ALIASES = {"CLARK COUNTY BOULDER AREA": "CLARK COUNTY BOULDER STRIP AREA"}   # renamed in the 2018 report redesign
COMPONENTS = ["tgw", "race", "sports", "slots"]


def area_key(name):
    k = norm(name).upper()
    return ALIASES.get(k, k)


def uid_of(key):
    return "NV_" + re.sub(r"[^A-Z0-9]+", "_", key).strip("_")


def shift(mo, k):
    y, m = map(int, mo.split("-"))
    m += k
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    return f"{y}-{m:02d}"


def derive_month(parsed, mo, derived):
    """Month whose GRI has no text layer: back it out of the three-month column of the report two months
    later: X(m) = 3mo(m+2 report) - X(m+1) - X(m+2). X(m+1) may itself be derived (done first)."""
    rep = parsed.get(shift(mo, 2))
    if not rep:
        return None
    nxt1 = parsed.get(shift(mo, 1)) or derived.get(shift(mo, 1))
    nxt2 = parsed.get(shift(mo, 2))
    if not nxt1 or not nxt2:
        return None
    out = {}
    for k, r in rep.items():
        if k not in nxt1 or k not in nxt2:
            continue
        d = {"area": r["area"]}
        for c in COMPONENTS:
            d[c] = r.get(c + "_3m", 0.0) - nxt1[k].get(c, 0.0) - nxt2[k].get(c, 0.0)
        for c in ("slot_units", "table_units"):          # 3-month column is the AVERAGE unit count
            d[c] = max(0, 3 * r.get(c + "_3m", 0) - nxt1[k].get(c, 0) - nxt2[k].get(c, 0))
        d["derived"] = True
        out[k] = d
    return out


def build():
    download_all()
    parsed, meta = {}, {}
    for p in sorted((CACHE / "gri").glob("gri_*.pdf")):
        mo = p.stem[4:]
        recs = parse_gri(p)
        if recs:
            parsed[mo] = {area_key(r["area"]): r for r in recs}
        meta[mo] = p
    rel = {}
    for p in sorted((CACHE / "release").glob("release_*.pdf")):
        d = parse_release(p)
        d["file"] = p
        rel[p.stem[8:]] = d
        if d.get("month") and d["month"] != p.stem[8:]:
            print(f"  release file {p.name} says month {d['month']}", file=sys.stderr)
    missing = sorted(set(meta) - set(parsed))
    derived = {}
    for mo in sorted(missing, reverse=True):          # later month first (May 2020 before Apr 2020)
        d = derive_month(parsed, mo, derived)
        if d:
            derived[mo] = d
        else:
            print(f"  cannot derive {mo}", file=sys.stderr)
    allm = {**parsed, **derived}
    # leaves = areas that are not a prefix-parent of another area (STATEWIDE, CLARK COUNTY, WASHOE COUNTY, ELKO COUNTY)
    rows = []
    for mo in sorted(allm):
        recs = allm[mo]
        keys = set(recs)
        for k, r in recs.items():
            is_parent = k == "STATEWIDE" or any(o != k and o.startswith(k + " ") for o in keys)
            if is_parent and k != "STATEWIDE":
                continue
            ggr = 1000.0 * (r["tgw"] - r.get("race", 0.0) - r.get("sports", 0.0))
            slots = 1000.0 * r.get("slots", 0.0)
            if k == "STATEWIDE":
                unit, uid, lvl = "__STATE_TOTAL__", "NV___STATE_TOTAL__", "state_total"
            else:
                unit, uid = norm(r["area"]), uid_of(k)
                lvl = "county" if re.fullmatch(r"[A-Z ]+ COUNTY", k) and k.count("COUNTY") == 1 else "area"
            rl = rel.get(mo, {})
            if rl.get("pub_date"):
                pub, src = rl["pub_date"], "press_release"
            else:
                import pymupdf
                cd = pymupdf.open(meta[mo]).metadata.get("creationDate", "")
                pub, src = (f"{cd[2:6]}-{cd[6:8]}-{cd[8:10]}", "pdf_metadata") if cd else ("", "")
            src_file = f"gri/gri_{mo}.pdf" if not r.get("derived") else \
                f"gri/gri_{shift(mo, 2)}.pdf (3-month column) - gri_{shift(mo, 1)} - gri_{shift(mo, 2)}"
            rows.append(dict(state="NV", unit=unit, unit_id=uid, unit_level=lvl, month=mo, ggr=ggr, slots=slots,
                             tables=ggr - slots, n_casinos=r.get("n_slot_loc", np.nan),
                             n_slot_units=r.get("slot_units", np.nan), n_table_units=r.get("table_units", np.nan),
                             measure="win ex race/sports" if not r.get("derived") else
                             "win ex race/sports (derived from 3-month column)",
                             pub_date=pub, pub_source=src, source_file=src_file,
                             _tgw=1000.0 * r["tgw"], _games=1000.0 * (r.get("games_total", np.nan) +
                                                                      (0 if r.get("games_incl_card", True) else r.get("card", 0.0)))))
    df = pd.DataFrame(rows)
    return df, rel, parsed, derived


def validate_derivation(parsed, months):
    """Apply the 3-month back-out to months whose own report exists, to measure its error."""
    errs = []
    for mo in months:
        d = derive_month(parsed, mo, {})
        if not d:
            continue
        for k, r in d.items():
            if k in parsed[mo]:
                a = parsed[mo][k]
                ggr_a = a["tgw"] - a.get("race", 0) - a.get("sports", 0)
                ggr_d = r["tgw"] - r["race"] - r["sports"]
                errs.append((mo, k, ggr_a, ggr_d))
    return pd.DataFrame(errs, columns=["month", "area", "actual_000", "derived_000"])


def checks(df, rel):
    leaves = df[df.unit_level != "state_total"].groupby("month")[["ggr", "_tgw", "n_slot_units",
                                                                    "n_table_units"]].sum()
    st = df[df.unit_level == "state_total"].set_index("month")
    ck = pd.DataFrame({"month": leaves.index, "sum_of_units": leaves.ggr.values,
                       "regulator_total": st.loc[leaves.index, "ggr"].values})
    ck["diff_pct"] = 100 * (ck.sum_of_units - ck.regulator_total) / ck.regulator_total
    notes = []
    for mo, tgw_st in st._tgw.items():
        r = rel.get(mo, {}).get("tgw_release")
        notes.append(f"statewide total gaming win (GRI, $000 x1000) vs press release ${r:,.0f}: "
                     f"{100 * (tgw_st - r) / r:+.3f}%" if r else "no press release total")
    du = [f"; units areas-statewide: slots {int(a - b):+d}, tables {int(c - d):+d}"
          for a, b, c, d in zip(leaves.n_slot_units, st.loc[leaves.index, "n_slot_units"],
                                leaves.n_table_units, st.loc[leaves.index, "n_table_units"])]
    ck["note"] = ["sum of finest areas vs Statewide page (win ex race book & sports pool); " + n + u
                  for n, u in zip(notes[:len(ck)], du)]
    return ck


def jumps(df):
    out = []
    for uid, g in df[df.unit_level != "state_total"].groupby("unit_id"):
        g = g.sort_values("month")
        r = g.ggr / g.ggr.shift(1)
        for mo, x, v in zip(g.month, r, g.ggr):
            if pd.notna(x) and (x > 3 or x < 1 / 3) and not ("2020-03" <= mo <= "2020-07"):
                out.append((uid, mo, round(x, 2), v))
    return out


if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    df, rel, parsed, derived = build()
    ck = checks(df, rel)
    val = validate_derivation(parsed, [m for m in sorted(parsed) if m >= "2012-03"][::7])
    val["err_pct"] = 100 * (val.derived_000 - val.actual_000) / val.actual_000.abs().clip(lower=1)
    big = val[val.actual_000.abs() > 5000]
    print("derivation test (areas with >$5M): median |err| %.3f%%, max |err| %.3f%%" %
          (big.err_pct.abs().median(), big.err_pct.abs().max()))
    cols = ["state", "unit", "unit_id", "unit_level", "month", "ggr", "slots", "tables", "n_casinos", "measure",
            "pub_date", "pub_source", "source_file", "n_slot_units", "n_table_units"]
    out = df[cols]
    bad_u = [(m, k) for m, recs in parsed.items() for k, r in recs.items()
             if r.get("units_check", 0) != 0 or r.get("slot_units_check", 0) != 0]
    print("unit-count parse check (Total row units != sum of rows):", len(bad_u), bad_u[:5])
    uv = []
    for mo in [m for m in sorted(parsed) if m >= "2012-03"][::7]:
        d = derive_month(parsed, mo, {})
        for k, r in (d or {}).items():
            if k in parsed[mo]:
                uv.append((r["slot_units"] - parsed[mo][k]["slot_units"], r["table_units"] - parsed[mo][k]["table_units"]))
    uv = pd.DataFrame(uv, columns=["ds", "dt"]).abs()
    print("unit derivation test: max |slot err| %d, max |table err| %d, median %.1f / %.1f units"
          % (uv.ds.max(), uv.dt.max(), uv.ds.median(), uv.dt.median()))
    assert not out.duplicated(["unit_id", "month"]).any()
    DATA.mkdir(exist_ok=True)
    out.to_csv(DATA / "state_nv.csv.gz", index=False)
    ck.to_csv(DATA / "state_nv_checks.csv.gz", index=False)
    print(out.month.min(), out.month.max(), out.month.nunique(), "months;", out.unit_id.nunique(), "unit ids")
    print("max |diff_pct|", ck.diff_pct.abs().max())
    print("derived months:", sorted(derived))
    gm = df.dropna(subset=["_games"])
    bad = gm[(gm._tgw - gm._games - gm.slots).abs() > 3000]
    print("rows where total gaming win != games + slots (> $3k rounding):", len(bad))
    print("jumps:", jumps(df))

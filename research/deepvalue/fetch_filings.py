#!/usr/bin/env python3
"""SEC EDGAR document fetcher -> plain-text, LLM-ready files.

Usage:
    fetch_filings.py TICKER [TICKER...]

Writes, per ticker, under research/deepvalue/filings/<TICKER>/:
    10-K_<date>_item1_business.md
    10-K_<date>_item1a_risks.md
    10-K_<date>_item7_mdna.md      (or 10-K_<date>_full.md if splitting fails)
    10-Q_<date>_mdna.md
    DEF14A_<date>_summary.md
    8-K_<date>_<desc>.md           (last 6 months, main doc + EX-99 exhibits)
    form4_last12m.csv / form4_summary.md
    meta.json

Raw downloads are cached under <TICKER>/raw/ (gitignored).
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import argparse
import datetime as dt
from pathlib import Path
from xml.etree import ElementTree as ET

import warnings

import requests
from bs4 import BeautifulSoup, NavigableString

try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except ImportError:
    pass

# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------
USER_AGENT = "ClaudeSpace research dspinjr@gmail.com"
REQ_SLEEP = 0.15          # <= ~7 req/sec
BASE = Path(__file__).resolve().parent
OUT_ROOT = BASE / "filings"
MAX_MD_CHARS = 380_000    # keep every .md comfortably under 400k
FULL_FALLBACK_CHARS = 150_000
PROXY_WINDOW = 40_000

# Per-ticker request budget. None = unlimited (the single-ticker default, unchanged).
# fetch_all.py sets these so a whole-universe sweep stays inside its time budget:
# 8-Ks cost ~3 requests each (index + main doc + EX-99) and Form 4s 1-2 each, and
# a handful of names file 100+ Form 4s a year.
MAX_8K = None             # keep the N most recent 8-Ks in the 6-month window
MAX_FORM4 = None          # parse the N most recent Form 4s in the 12-month window

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"

_session = requests.Session()
_session.headers.update({
    "User-Agent": USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
})
_last_req = [0.0]


def _throttle():
    delta = time.time() - _last_req[0]
    if delta < REQ_SLEEP:
        time.sleep(REQ_SLEEP - delta)
    _last_req[0] = time.time()


def fetch(url: str, cache_dir: Path, cache_name: str | None = None,
          binary: bool = False, tries: int = 3):
    """GET with on-disk cache under cache_dir. Returns bytes, or None on failure."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    name = cache_name or re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/Archives/")[-1])
    path = cache_dir / name[-180:]
    if path.exists() and path.stat().st_size > 0:
        return path.read_bytes()
    last_err = None
    for attempt in range(tries):
        _throttle()
        try:
            r = _session.get(url, timeout=45)
            if r.status_code == 200:
                path.write_bytes(r.content)
                return r.content
            if r.status_code == 404:
                return None
            last_err = f"HTTP {r.status_code}"
        except Exception as exc:            # network hiccup
            last_err = str(exc)
        time.sleep(1.0 + attempt)
    print(f"    ! fetch failed {url}: {last_err}", file=sys.stderr)
    return None


# --------------------------------------------------------------------------
# HTML -> text
# --------------------------------------------------------------------------
BLOCK_TAGS = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6",
              "section", "article", "hr", "td_block"}


def _table_to_text(tbl) -> str:
    lines = []
    for tr in tbl.find_all("tr"):
        cells = []
        for td in tr.find_all(["td", "th"]):
            txt = td.get_text(" ", strip=True).replace("\xa0", " ")
            txt = re.sub(r"\s+", " ", txt).strip()
            cells.append(txt)
        while cells and not cells[-1]:
            cells.pop()
        cells = [c for c in cells if c not in ("", "$", ")", "(")] or cells
        row = " | ".join(c for c in cells if c)
        if row.strip(" |"):
            lines.append(row)
    return "\n".join(lines)


def html_to_text(raw: bytes) -> str:
    soup = BeautifulSoup(raw, "lxml")

    # strip scripts, styles, inline-XBRL headers and hidden blocks
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()
    for tag in soup.find_all(lambda t: t.name and (
            t.name.startswith("ix:header") or t.name in ("ix:header", "ix:hidden",
                                                         "ix:references", "ix:resources"))):
        tag.decompose()
    for tag in soup.find_all(style=True):
        st = (tag.get("style") or "").replace(" ", "").lower()
        if "display:none" in st:
            tag.decompose()

    # tables -> pipe-separated rows
    for tbl in soup.find_all("table"):
        tbl.replace_with(NavigableString("\n" + _table_to_text(tbl) + "\n"))

    # block boundaries -> newlines
    for tag in soup.find_all(list(BLOCK_TAGS)):
        try:
            tag.insert_before(NavigableString("\n"))
            tag.insert_after(NavigableString("\n"))
        except Exception:
            pass

    text = soup.get_text(" ")
    text = (text.replace("\xa0", " ").replace("’", "'").replace("‘", "'")
                .replace("“", '"').replace("”", '"'))
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def doc_to_text(raw: bytes, filename: str) -> str:
    if filename.lower().endswith((".txt",)):
        return re.sub(r"\n{3,}", "\n\n", raw.decode("utf-8", "replace"))
    return html_to_text(raw)


# --------------------------------------------------------------------------
# item / heading detection
# --------------------------------------------------------------------------
FLAGS = re.I | re.M | re.S
GAP = r"[\s\.\:\-–—\)]{0,40}"


def _pat(num: str, title: str) -> str:
    return rf"^[ \t]*(?:PART\s+[IV]+[\s\.\-]*)?ITEM{GAP}{num}{GAP}(?:{title})"


ITEM_PATS = {
    "1":  _pat("1",  r"BUSINESS"),
    "1a": _pat("1A", r"RISK\s*FACTORS"),
    "1b": _pat("1B", r"UNRESOLVED"),
    "1c": _pat("1C", r"CYBER"),
    "2":  _pat("2",  r"PROPERT"),
    "3":  _pat("3",  r"LEGAL\s*PROCEED"),
    "7":  _pat("7",  r"MANAGEMENT'?S?\s*DISCUSSION"),
    "7a": _pat("7A", r"QUANTITATIVE"),
    "8":  _pat("8",  r"FINANCIAL\s*STATEMENTS"),
}
# loose fallbacks (no title requirement)
ITEM_PATS_LOOSE = {k: rf"^[ \t]*ITEM{GAP}{n}\b"
                   for k, n in [("1", "1"), ("1a", "1A"), ("1b", "1B"), ("1c", "1C"),
                                ("2", "2"), ("3", "3"), ("7", "7"), ("7a", "7A"), ("8", "8")]}

Q_ITEM_PATS = {
    "q2": _pat("2", r"MANAGEMENT'?S?\s*DISCUSSION"),
    "q3": _pat("3", r"QUANTITATIVE"),
    "q4": _pat("4", r"CONTROLS"),
    "q1": _pat("1", r"FINANCIAL\s*STATEMENTS"),
}


def _starts(text, pat):
    return [m.start() for m in re.finditer(pat, text, FLAGS)]


def _toc_line(text, pos):
    """True if the line at pos looks like a table-of-contents entry (trailing page no.)."""
    nl = text.find("\n", pos)
    line = text[pos: nl if nl > 0 else len(text)]
    return bool(re.search(r"\|\s*[ivxlc\d]+\s*$", line, re.I))


def pick_section(text, start_pat, end_pats, min_len=800):
    """Choose the occurrence of start_pat that yields the longest section.

    Table-of-contents entries are immediately followed by the next item's TOC
    entry, so they score a tiny span and lose to the real body heading.
    """
    starts = _starts(text, start_pat)
    if not starts:
        return None
    # drop table-of-contents lines ("Item 1A. Risk Factors | 16") when we have alternatives
    non_toc = [p for p in starts if not _toc_line(text, p)]
    if non_toc:
        starts = non_toc
    ends = sorted({p for ep in end_pats for p in _starts(text, ep)})
    best = None
    for s in starts:
        # +10 only guards against a heading matching itself; TOC entries sit a few
        # dozen characters apart and must stay eligible as end markers so that a
        # TOC start scores a tiny span and loses to the real body heading.
        e = next((x for x in ends if x > s + 10), len(text))
        if best is None or (e - s) > (best[1] - best[0]):
            best = (s, e)
    if best and (best[1] - best[0]) >= min_len:
        return best
    return None


def extract_10k_items(text):
    """-> dict with keys item1/item1a/item7 (missing keys = not found)."""
    out = {}
    plans = [
        ("item1",  ["1"],  [["1a"], ["1b"], ["2"]]),
        ("item1a", ["1a"], [["1b"], ["1c"], ["2"]]),
        ("item7",  ["7"],  [["7a"], ["8"]]),
    ]
    for key, starts, endgroups in plans:
        got = None
        for pats, loose in ((ITEM_PATS, False), (ITEM_PATS_LOOSE, True)):
            spat = pats[starts[0]]
            epats = [pats[e] for grp in endgroups for e in grp if e in pats]
            got = pick_section(text, spat, epats, min_len=1200 if not loose else 2000)
            if got:
                break
        if got:
            out[key] = text[got[0]:got[1]].strip()
    return out


def extract_10q_mdna(text):
    got = pick_section(text, Q_ITEM_PATS["q2"],
                       [Q_ITEM_PATS["q3"], Q_ITEM_PATS["q4"]], min_len=1000)
    if not got:
        got = pick_section(text, rf"^[ \t]*ITEM{GAP}2\b",
                           [rf"^[ \t]*ITEM{GAP}3\b", rf"^[ \t]*ITEM{GAP}4\b"], min_len=2000)
    return text[got[0]:got[1]].strip() if got else None


# (title, patterns in priority order, prefer-numeric-dense-occurrence)
PROXY_TOPICS = [
    ("Executive Compensation - Summary Compensation Table",
     [r"^[ \t]*(?:(?:FISCAL\s+)?\d{4}\s+)?SUMMARY\s+COMPENSATION\s+TABLE[^\n]{0,40}$",
      r"^[ \t]*EXECUTIVE\s+COMPENSATION\s+TABLES?[^\n]{0,20}$",
      r"^[ \t]*EXECUTIVE\s+COMPENSATION[^\n]{0,20}$"], True),
    ("Beneficial Ownership",
     [r"^[ \t]*SECURITY\s+OWNERSHIP[^\n]{0,80}$",
      r"^[ \t]*(?:COMMON\s+STOCK\s+)?BENEFICIAL\s+OWNERSHIP[^\n]{0,60}$",
      r"^[ \t]*(?:PRINCIPAL\s+)?(?:STOCKHOLDERS?|SHAREHOLDERS?)[^\n]{0,50}$",
      r"^[ \t]*OWNERSHIP\s+OF[^\n]{0,60}$"], True),
    ("Related-Party Transactions",
     [r"^[ \t]*CERTAIN\s+RELATIONSHIPS[^\n]{0,80}$",
      r"^[ \t]*TRANSACTIONS\s+WITH\s+RELATED[^\n]{0,60}$",
      r"^[ \t]*RELATED[\s\-]*(?:PARTY|PARTIES|PERSON|PERSONS)[^\n]{0,60}$"], False),
]


def extract_proxy_sections(text):
    """-> list of (title, body). Empty list if nothing matched."""
    n = len(text)
    toc_cut = max(15_000, int(n * 0.05))
    chosen = []
    for title, pats, numeric in PROXY_TOPICS:
        cands = []
        for pat in pats:                      # first pattern that hits wins
            allc = _starts(text, pat)
            cands = [p for p in allc if p > toc_cut and not _toc_line(text, p)]
            if not cands:
                cands = [p for p in allc if not _toc_line(text, p)]
            if cands:
                break
        if not cands:
            continue
        if numeric and len(cands) > 1:
            # the real table is the occurrence followed by the most digits
            cands.sort(key=lambda p: -sum(c.isdigit() for c in text[p:p + 5000]))
        chosen.append((title, cands[0]))
    if not chosen:
        return []
    chosen.sort(key=lambda x: x[1])
    out = []
    for i, (title, s) in enumerate(chosen):
        nxt = chosen[i + 1][1] if i + 1 < len(chosen) else n
        e = min(nxt, s + PROXY_WINDOW) if nxt - s > 500 else min(n, s + PROXY_WINDOW)
        out.append((title, text[s:e].strip()))
    return out


# --------------------------------------------------------------------------
# writing
# --------------------------------------------------------------------------
def write_md(path: Path, header: str, body: str, notes=()):
    body = body or ""
    trunc = ""
    if len(body) > MAX_MD_CHARS:
        body = body[:MAX_MD_CHARS]
        trunc = f"\n\n[TRUNCATED to {MAX_MD_CHARS:,} characters]\n"
    parts = [header.rstrip(), ""]
    for nt in notes:
        parts.append(f"> NOTE: {nt}")
    if notes:
        parts.append("")
    parts.append(body)
    parts.append(trunc)
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return path.stat().st_size


# --------------------------------------------------------------------------
# EDGAR plumbing
# --------------------------------------------------------------------------
def ticker_to_cik(ticker: str, shared_raw: Path):
    raw = fetch(TICKERS_URL, shared_raw, "company_tickers.json")
    if raw is None:
        raise RuntimeError("could not fetch company_tickers.json")
    data = json.loads(raw)
    for v in data.values():
        if v["ticker"].upper() == ticker.upper():
            return int(v["cik_str"]), v["title"]
    raise KeyError(f"ticker {ticker} not found in SEC ticker map")


def get_submissions(cik: int, raw_dir: Path):
    raw = fetch(f"https://data.sec.gov/submissions/CIK{cik:010d}.json",
                raw_dir, f"submissions_{cik}.json")
    if raw is None:
        raise RuntimeError("could not fetch submissions")
    return json.loads(raw)


def recent_filings(sub):
    r = sub["filings"]["recent"]
    keys = ["form", "filingDate", "reportDate", "accessionNumber",
            "primaryDocument", "primaryDocDescription", "items"]
    n = len(r["form"])
    rows = []
    for i in range(n):
        rows.append({k: (r[k][i] if k in r and i < len(r[k]) else "") for k in keys})
    return rows


def acc_nodash(acc):
    return acc.replace("-", "")


def filing_dir_url(cik, acc):
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash(acc)}"


def doc_url(cik, acc, primary_doc):
    # Form 3/4/5 primaryDocument is an XSL-rendered path (xslF345X06/form4.xml);
    # the raw XML sits one level up.
    return f"{filing_dir_url(cik, acc)}/{primary_doc}"


def filing_documents(cik, acc, raw_dir):
    """-> list of dicts {seq, description, document, type, size} from -index.html."""
    url = f"{filing_dir_url(cik, acc)}/{acc}-index.html"
    raw = fetch(url, raw_dir, f"{acc}-index.html")
    if raw is None:
        return []
    soup = BeautifulSoup(raw, "lxml")
    docs = []
    for tbl in soup.find_all("table"):
        hdr = [th.get_text(strip=True) for th in tbl.find_all("th")]
        if "Type" not in hdr or "Document" not in hdr:
            continue
        idx = {h: i for i, h in enumerate(hdr)}
        for tr in tbl.find_all("tr")[1:]:
            tds = [td for td in tr.find_all("td")]
            if len(tds) < len(hdr):
                continue
            a = tds[idx["Document"]].find("a")
            href = a["href"] if a and a.has_attr("href") else ""
            name = href.split("/")[-1].split("?")[0]
            docs.append({
                "description": tds[idx.get("Description", 0)].get_text(" ", strip=True),
                "document": name,
                "type": tds[idx["Type"]].get_text(strip=True),
            })
    return docs


# --------------------------------------------------------------------------
# 8-K helpers
# --------------------------------------------------------------------------
ITEM_8K_SLUG = {
    "1.01": "material-agreement", "1.02": "agreement-terminated", "2.01": "acquisition",
    "2.02": "results", "2.03": "obligation", "2.05": "exit-costs", "3.01": "listing",
    "3.02": "equity-sale", "4.01": "auditor-change", "5.01": "control-change",
    "5.02": "officers-directors", "5.03": "bylaws", "5.07": "shareholder-vote",
    "7.01": "reg-fd", "8.01": "other-events", "9.01": "exhibits",
}


def slug_8k(items: str, desc: str) -> str:
    codes = [c.strip() for c in (items or "").split(",") if c.strip()]
    codes = [c for c in codes if c != "9.01"] or codes
    if codes:
        c = codes[0]
        return f"{c.replace('.', '-')}-{ITEM_8K_SLUG.get(c, 'item')}"
    s = re.sub(r"[^a-z0-9]+", "-", (desc or "8k").lower()).strip("-")
    return s[:40] or "8k"


# --------------------------------------------------------------------------
# Form 4
# --------------------------------------------------------------------------
def _t(node, *names):
    for nm in names:
        el = node.find(nm)
        if el is not None:
            v = el.find("value")
            txt = (v.text if v is not None else el.text) or ""
            if txt.strip():
                return txt.strip()
    return ""


def parse_form4(xml_bytes, filing_date, accession):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    owners = []
    for ro in root.findall("reportingOwner"):
        roid = ro.find("reportingOwnerId")
        nm = _t(roid, "rptOwnerName") if roid is not None else ""
        rel = ro.find("reportingOwnerRelationship")
        flags = []
        if rel is not None:
            if (rel.findtext("isDirector") or "").strip() in ("1", "true"):
                flags.append("Director")
            if (rel.findtext("isOfficer") or "").strip() in ("1", "true"):
                flags.append("Officer")
            if (rel.findtext("isTenPercentOwner") or "").strip() in ("1", "true"):
                flags.append("10% Owner")
            if (rel.findtext("isOther") or "").strip() in ("1", "true"):
                flags.append("Other")
            title = (rel.findtext("officerTitle") or "").strip()
            if title:
                flags.append(title)
        owners.append((nm, "; ".join(flags)))
    if not owners:
        owners = [("", "")]
    owner_name = " / ".join(o[0] for o in owners if o[0])
    owner_rel = " / ".join(o[1] for o in owners if o[1])

    rows = []
    for table, tag in (("nonDerivativeTable", "nonDerivativeTransaction"),
                       ("derivativeTable", "derivativeTransaction")):
        tb = root.find(table)
        if tb is None:
            continue
        for tx in tb.findall(tag):
            amt = tx.find("transactionAmounts")
            coding = tx.find("transactionCoding")
            post = tx.find("postTransactionAmounts")
            code = _t(coding, "transactionCode") if coding is not None else ""
            shares = _t(amt, "transactionShares") if amt is not None else ""
            price = _t(amt, "transactionPricePerShare") if amt is not None else ""
            ad = _t(amt, "transactionAcquiredDisposedCode") if amt is not None else ""
            owned = _t(post, "sharesOwnedFollowingTransaction",
                       "valueOwnedFollowingTransaction") if post is not None else ""
            rows.append({
                "filing_date": filing_date,
                "transaction_date": _t(tx, "transactionDate"),
                "owner": owner_name,
                "relationship": owner_rel,
                "security": _t(tx, "securityTitle"),
                "table": "derivative" if table.startswith("deriv") else "non-derivative",
                "code": code,
                "acquired_disposed": ad,
                "shares": shares,
                "price": price,
                "shares_owned_after": owned,
                "accession": accession,
            })
    return rows


def _f(x):
    try:
        return float(str(x).replace(",", "").replace("$", ""))
    except Exception:
        return 0.0


def form4_summary(rows):
    buys = [r for r in rows if r["code"] == "P" and r["table"] == "non-derivative"]
    sells = [r for r in rows if r["code"] == "S" and r["table"] == "non-derivative"]
    buy_val = sum(_f(r["shares"]) * _f(r["price"]) for r in buys)
    sell_val = sum(_f(r["shares"]) * _f(r["price"]) for r in sells)
    buy_sh = sum(_f(r["shares"]) for r in buys)
    sell_sh = sum(_f(r["shares"]) for r in sells)
    n_buyers = len({r["owner"] for r in buys if r["owner"]})
    largest = max(buys, key=lambda r: _f(r["shares"]) * _f(r["price"]), default=None)
    if largest:
        lg = (f"{largest['owner']} bought {_f(largest['shares']):,.0f} sh "
              f"@ ${_f(largest['price']):,.2f} (${_f(largest['shares'])*_f(largest['price']):,.0f}) "
              f"on {largest['transaction_date']}")
    else:
        lg = "none"
    l1 = (f"Net open-market activity (last 12m): buys {buy_sh:,.0f} sh / ${buy_val:,.0f} "
          f"vs sells {sell_sh:,.0f} sh / ${sell_val:,.0f} "
          f"-> net ${buy_val - sell_val:,.0f} ({'BUYING' if buy_val > sell_val else 'SELLING'}).")
    l2 = f"Distinct insiders buying (code P): {n_buyers}. Largest buy: {lg}."
    return l1, l2, buys, sells


# --------------------------------------------------------------------------
# main per-ticker routine
# --------------------------------------------------------------------------
def process(ticker: str) -> dict:
    t0 = time.time()
    ticker = ticker.upper()
    out_dir = OUT_ROOT / ticker
    raw_dir = out_dir / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    shared_raw = OUT_ROOT / "_shared" / "raw"

    cik, name = ticker_to_cik(ticker, shared_raw)
    sub = get_submissions(cik, raw_dir)
    rows = recent_filings(sub)
    today = dt.date.today()
    written, problems = [], []

    meta = {
        "ticker": ticker,
        "cik": f"{cik:010d}",
        "cik_int": cik,
        "name": sub.get("name") or name,
        "sic": sub.get("sic"),
        "sic_description": sub.get("sicDescription"),
        "fiscal_year_end": sub.get("fiscalYearEnd"),
        "exchanges": sub.get("exchanges"),
        "tickers": sub.get("tickers"),
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "filings_used": {},
        "notes": [],
    }

    def record(p):
        written.append((p.name, p.stat().st_size))

    def latest(form_names):
        """First (= most recent) filing whose form matches, honouring the order
        of form_names as a preference list: DEF 14A beats DEFA14A, 10-K beats 20-F."""
        for want in form_names:
            for r in rows:
                if r["form"] == want:
                    return r
        return None

    def load_primary(r):
        url = doc_url(cik, r["accessionNumber"], r["primaryDocument"])
        raw = fetch(url, raw_dir, f"{r['accessionNumber']}_{Path(r['primaryDocument']).name}")
        if raw is None:
            return None
        return doc_to_text(raw, r["primaryDocument"])

    # ---------------- 10-K ----------------
    k = latest(["10-K", "10-K405", "10-KSB", "20-F", "40-F"])
    if not k:
        problems.append("no 10-K/20-F in recent filings")
    else:
        d = k["filingDate"]
        meta["filings_used"]["10-K"] = {"filingDate": d, "reportDate": k["reportDate"],
                                        "accession": k["accessionNumber"],
                                        "form": k["form"], "primaryDocument": k["primaryDocument"]}
        text = load_primary(k)
        if not text:
            problems.append(f"10-K {d}: primary document could not be downloaded")
        else:
            items = extract_10k_items(text)
            want = {"item1": ("item1_business", "Item 1 - Business"),
                    "item1a": ("item1a_risks", "Item 1A - Risk Factors"),
                    "item7": ("item7_mdna", "Item 7 - MD&A")}
            found = [k2 for k2 in want if k2 in items]
            for k2, (suffix, title) in want.items():
                if k2 in items:
                    p = out_dir / f"10-K_{d}_{suffix}.md"
                    write_md(p, f"# {ticker} {k['form']} {d} - {title}\n\n"
                                f"Source: {doc_url(cik, k['accessionNumber'], k['primaryDocument'])}",
                             items[k2])
                    record(p)
            missing = [want[k2][1] for k2 in want if k2 not in items]
            if missing:
                problems.append(f"10-K {d}: heading split missed {', '.join(missing)}")
            if not found:
                p = out_dir / f"10-K_{d}_full.md"
                write_md(p, f"# {ticker} {k['form']} {d} - FULL DOCUMENT",
                         text[:FULL_FALLBACK_CHARS],
                         notes=[f"Item 1/1A/7 heading detection failed; full text truncated to "
                                f"{FULL_FALLBACK_CHARS:,} of {len(text):,} characters."])
                record(p)
                meta["notes"].append("10-K item splitting failed; wrote full-text fallback.")

    # ---------------- 10-Q ----------------
    q = latest(["10-Q"])
    if not q:
        problems.append("no 10-Q in recent filings")
    else:
        d = q["filingDate"]
        meta["filings_used"]["10-Q"] = {"filingDate": d, "reportDate": q["reportDate"],
                                        "accession": q["accessionNumber"]}
        text = load_primary(q)
        if not text:
            problems.append(f"10-Q {d}: primary document could not be downloaded")
        else:
            md = extract_10q_mdna(text)
            p = out_dir / f"10-Q_{d}_mdna.md"
            if md:
                write_md(p, f"# {ticker} 10-Q {d} - Item 2 MD&A\n\n"
                            f"Source: {doc_url(cik, q['accessionNumber'], q['primaryDocument'])}", md)
            else:
                write_md(p, f"# {ticker} 10-Q {d} - FULL DOCUMENT", text[:FULL_FALLBACK_CHARS],
                         notes=["Item 2 MD&A heading not detected; full text truncated."])
                problems.append(f"10-Q {d}: MD&A heading not detected, wrote truncated full text")
            record(p)

    # ---------------- DEF 14A ----------------
    px = latest(["DEF 14A", "DEFM14A", "DEF 14C", "DEFA14A"])
    if not px:
        problems.append("no proxy (DEF 14A) in recent filings")
    else:
        d = px["filingDate"]
        meta["filings_used"]["DEF 14A"] = {"filingDate": d, "accession": px["accessionNumber"],
                                           "form": px["form"]}
        text = load_primary(px)
        if not text:
            problems.append(f"DEF 14A {d}: primary document could not be downloaded")
        else:
            secs = extract_proxy_sections(text)
            p = out_dir / f"DEF14A_{d}_summary.md"
            hdr = (f"# {ticker} {px['form']} {d} - Compensation / Ownership / Related Parties\n\n"
                   f"Source: {doc_url(cik, px['accessionNumber'], px['primaryDocument'])}")
            if secs:
                body = "\n\n".join(f"## {t}\n\n{b}" for t, b in secs)
                write_md(p, hdr, body)
            else:
                write_md(p, hdr, text[:60_000],
                         notes=["Target headings not found; first 60,000 characters of the proxy."])
                problems.append(f"DEF 14A {d}: target headings not found, wrote first 60k chars")
            record(p)

    # ---------------- 8-K, last 6 months ----------------
    cutoff_6m = today - dt.timedelta(days=183)
    eights = [r for r in rows if r["form"] in ("8-K", "8-K/A")
              and r["filingDate"] >= cutoff_6m.isoformat()]
    n_eights_all = len(eights)
    if MAX_8K is not None and len(eights) > MAX_8K:
        eights = eights[:MAX_8K]          # `rows` is newest-first
        meta["notes"].append(
            f"8-K capped at the {MAX_8K} most recent of {n_eights_all} in the last 6 months")
    used_8k = []
    seen_names = set()
    for r in eights:
        d = r["filingDate"]
        acc = r["accessionNumber"]
        base = f"8-K_{d}_{slug_8k(r['items'], r['primaryDocDescription'])}"
        fn = base
        i = 2
        while fn in seen_names:
            fn = f"{base}-{i}"
            i += 1
        seen_names.add(fn)

        chunks = []
        text = load_primary(r)
        if text:
            chunks.append(("Main document (" + r["primaryDocument"] + ")", text))
        docs = filing_documents(cik, acc, raw_dir)
        for dd in docs:
            typ = (dd["type"] or "").upper()
            nm = dd["document"]
            if not typ.startswith("EX-99"):
                continue
            if not nm.lower().endswith((".htm", ".html", ".txt")):
                continue
            raw = fetch(f"{filing_dir_url(cik, acc)}/{nm}", raw_dir, f"{acc}_{nm}")
            if raw is None:
                continue
            chunks.append((f"{typ} - {dd['description'] or nm} ({nm})", doc_to_text(raw, nm)))
        if not chunks:
            problems.append(f"8-K {d}: no readable documents")
            continue
        body = "\n\n".join(f"## {t}\n\n{b}" for t, b in chunks)
        p = out_dir / f"{fn}.md"
        write_md(p, f"# {ticker} {r['form']} {d}  (Items: {r['items'] or 'n/a'})\n\n"
                    f"Source: {filing_dir_url(cik, acc)}/{acc}-index.html", body)
        record(p)
        used_8k.append({"filingDate": d, "accession": acc, "items": r["items"],
                        "file": p.name, "exhibits": len(chunks) - 1})
    meta["filings_used"]["8-K"] = used_8k
    if not eights:
        meta["notes"].append("no 8-K filings in the last 6 months")

    # ---------------- Form 4, last 12 months ----------------
    cutoff_12m = today - dt.timedelta(days=365)
    fours = [r for r in rows if r["form"] == "4"
             and r["filingDate"] >= cutoff_12m.isoformat()]
    n_fours_all = len(fours)
    if MAX_FORM4 is not None and len(fours) > MAX_FORM4:
        fours = fours[:MAX_FORM4]         # `rows` is newest-first
        meta["notes"].append(
            f"Form 4 capped at the {MAX_FORM4} most recent of {n_fours_all} in the last 12 months; "
            f"the buy/sell totals below cover only those")
    f4rows = []
    for r in fours:
        acc = r["accessionNumber"]
        pd = r["primaryDocument"] or "form4.xml"
        # strip the xslF345Xnn/ rendering prefix to get the raw XML
        xml_name = pd.split("/")[-1]
        raw = fetch(f"{filing_dir_url(cik, acc)}/{xml_name}", raw_dir, f"{acc}_{xml_name}")
        if raw is None:
            docs = filing_documents(cik, acc, raw_dir)
            cand = next((d["document"] for d in docs
                         if d["document"].lower().endswith(".xml")), None)
            if cand:
                raw = fetch(f"{filing_dir_url(cik, acc)}/{cand}", raw_dir, f"{acc}_{cand}")
        if raw is None:
            continue
        f4rows.extend(parse_form4(raw, r["filingDate"], acc))

    cols = ["filing_date", "transaction_date", "owner", "relationship", "security", "table",
            "code", "acquired_disposed", "shares", "price", "shares_owned_after", "accession"]
    csv_path = out_dir / "form4_last12m.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in sorted(f4rows, key=lambda x: (x["transaction_date"] or "", x["owner"])):
            w.writerow(r)
    record(csv_path)

    l1, l2, buys, sells = form4_summary(f4rows)
    codes = {}
    for r in f4rows:
        codes[r["code"]] = codes.get(r["code"], 0) + 1
    tbl = "\n".join(f"| {c or '(blank)'} | {n} |" for c, n in sorted(codes.items()))
    p = out_dir / "form4_summary.md"
    write_md(p, f"# {ticker} Form 4 insider activity - trailing 12 months",
             f"{l1}\n{l2}\n\n"
             f"Form 4 filings parsed: {len(fours)}; transaction rows: {len(f4rows)} "
             f"(open-market buys {len(buys)}, sales {len(sells)}).\n\n"
             f"| code | rows |\n|---|---|\n{tbl}\n\n"
             f"Codes: P=open-market purchase, S=open-market sale, A=grant/award, "
             f"M=option exercise, F=tax withholding, G=gift.\n\n"
             f"Detail: form4_last12m.csv\n")
    record(p)
    meta["filings_used"]["form4_count"] = len(fours)
    meta["filings_used"]["form4_available"] = n_fours_all
    meta["filings_used"]["eightk_available"] = n_eights_all
    meta["filings_used"]["form4_rows"] = len(f4rows)
    if not fours:
        meta["notes"].append("no Form 4 filings in the last 12 months")
        problems.append("no Form 4 filings in the last 12 months")

    # ---------------- meta ----------------
    meta["problems"] = problems
    meta["runtime_seconds"] = round(time.time() - t0, 1)
    mp = out_dir / "meta.json"
    mp.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    record(mp)

    return {"ticker": ticker, "written": written, "problems": problems,
            "runtime": meta["runtime_seconds"], "out_dir": out_dir}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fetch SEC EDGAR filings as LLM-ready text.")
    ap.add_argument("tickers", nargs="+", help="one or more ticker symbols")
    args = ap.parse_args(argv)
    for tk in args.tickers:
        try:
            res = process(tk)
        except Exception as exc:
            print(f"{tk}: FAILED - {exc}", file=sys.stderr)
            continue
        print(f"\n=== {res['ticker']} -> {res['out_dir']} ({res['runtime']}s) ===")
        for nm, size in sorted(res["written"]):
            print(f"  {size:>9,}  {nm}")
        for pb in res["problems"]:
            print(f"  ! {pb}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

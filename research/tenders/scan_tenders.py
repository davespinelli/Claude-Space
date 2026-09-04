#!/usr/bin/env python3
"""Idea B2 — odd-lot tender-offer scanner.

An **issuer self-tender** is filed on Schedule TO-I (Rule 13e-4); amendments are
SC TO-I/A, pre-commencement communications SC TO-C, and the pre-1999 form is
SC 13E4. Most of these offers give **odd-lot priority**: a holder of fewer than
100 shares who tenders *all* of them is bought out in full, ahead of and exempt
from the proration that hits everyone else if the offer is oversubscribed. For a
$100k account this is not a strategy, it is a small, repeatable income stream
that institutions cannot scale into. This script finds the offers and does the
arithmetic; the human does the buying.

Sources, in the order tried
---------------------------
1. **EDGAR form indexes** (the route that works, and the one used below).
   * quarterly: ``/Archives/edgar/full-index/<Y>/QTR<n>/form.idx`` — a fixed-width
     table of every filing in the quarter, sorted by form type. Its header line
     ``Last Data Received:`` says how current it is; it typically lags by a day.
   * daily: ``/Archives/edgar/daily-index/<Y>/QTR<n>/form.<YYYYMMDD>.idx`` — same
     layout, used to fill the gap between the quarterly index and today.
2. **EDGAR full-text search** (``https://efts.sec.gov/LATEST/search-index`` with
   ``forms=SC TO-I`` and an empty ``q``) — the fallback if the index files fail.
   It is used automatically when step 1 yields nothing.

Per filing
----------
``<accn>-index-headers.html`` is the canonical document manifest: it carries the
SGML ``<TYPE>``/``<FILENAME>`` pairs *and* the subject company's SIC code, in one
request. ``index.json`` supplies file sizes. The document type label for the
offer to purchase is not standardised — real examples in a single 45-day window
include ``EX-99.(A)(1)(A)``, ``EXHIBIT (A)(1)(A)``, ``EX-99-A1A`` and
``EXHIBIT 99.(A)(1)(I)`` — so types are normalised to alphanumerics and the
largest document in the "(a)(1)" exhibit family is taken as the offer to
purchase, falling back to the largest document overall.

Every extracted field is optional. When a pattern does not match, the field is
recorded as ``not found`` rather than guessed; the quoted "odd lot" sentence is
carried verbatim so the reader can judge it.

What this deliberately does *not* treat as an opportunity
--------------------------------------------------------
* **Option exchange offers** (RxSight, Aug 2026) are SC TO-I but the class of
  securities is employee options — nothing for an outside holder to tender.
* **Closed-end fund / BDC repurchase offers** are the bulk of SC TO-I by count
  (129 of 144 offers in the 45 days to 2026-09-04) and are priced *at net asset
  value*, so the premium is zero by construction. They are still parsed and still
  written to history.csv, but they are kept out of the actionable table. A fund
  that *is* exchange-listed is the exception and is carried as a
  "listed fund tender", because a premium to the traded price is real.
* **Debt and preferred tenders** (Lincoln National's depositary shares, Aug 2026)
  price per $1,000 of liquidation preference, not per common share.

Two parsing traps are handled explicitly because both produce confident wrong
answers: "par value $0.01 per share" reads as a fixed offer price unless guarded,
and every Schedule TO cover page contains the sentence "Check the following box if
the filing is a final amendment reporting the results" beside an *unchecked* box,
so the phrase alone must not be read as a completed offer. Odd-lot language is also
checked for explicit *denial* ("this tender offer will not have any special pro
ration provision for odd-lot tenders") before it is read as priority.

Run: .venv/bin/python research/tenders/scan_tenders.py [--days 45] [--no-cache]
                                                      [--budget 40]
Writes research/tenders/TENDERS.md and research/tenders/history.csv.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html as htmllib
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

def log(*a, **kw):
    kw.setdefault("flush", True)
    print(*a, **kw)


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research" / "tenders"
CACHE = ROOT / "research" / ".cache" / "tenders"
OUT_MD = HERE / "TENDERS.md"
OUT_CSV = HERE / "history.csv"

UA = "ClaudeSpace research dspinjr@gmail.com"
MAX_RPS = 7.0                       # brief caps us at 8/s; SEC's own limit is 10
WORKERS = 6
DEADLINE = [float("inf")]           # wall-clock budget so the daily job cannot hang
ARCHIVES = "https://www.sec.gov/Archives/edgar"
FTS = "https://efts.sec.gov/LATEST/search-index"
TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"

FORMS = ("SC TO-I", "SC TO-I/A", "SC 13E4", "SC 13E4/A", "SC TO-C")
SIC_FUND = {"6726"}                 # investment offices: interval funds, BDCs

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
_lock = threading.Lock()
_next = [0.0]
USE_CACHE = True

# SEC serves an HTML "temporarily unavailable" page instead of a 429 when it
# throttles; a naive parser silently reads it as an empty document.
THROTTLED = "temporarily unavailable"


def get(url, params=None, tries=5, binary=False, quiet503=False):
    """Rate-limited GET with retry and throttle-page detection."""
    for i in range(tries):
        with _lock:
            wait = _next[0] - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            _next[0] = time.monotonic() + 1.0 / MAX_RPS
        try:
            r = SESSION.get(url, params=params, timeout=90)
        except requests.RequestException:
            time.sleep(1.5 * (i + 1))
            continue
        if r.status_code == 404:
            return None
        if r.status_code != 200:
            # a daily index that has not been published yet answers 503, not 404
            if quiet503 and r.status_code == 503 and i >= 1:
                return None
            time.sleep(1.5 * (i + 1))
            continue
        if not binary and THROTTLED in r.text[:4000].lower():
            time.sleep(2.0 * (i + 1))
            continue
        return r
    return None


def cached(key, url, params=None, quiet503=False):
    """Fetch `url` once per run-set; cache the body under a hash of `key`."""
    p = CACHE / (hashlib.sha1(key.encode()).hexdigest() + ".txt")
    if USE_CACHE and p.exists():
        return p.read_text(encoding="utf-8", errors="ignore")
    r = get(url, params, quiet503=quiet503)
    if r is None:
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    p.write_text(r.text, encoding="utf-8", errors="ignore")
    return r.text


# --------------------------------------------------------------- text handling
def to_text(raw):
    """HTML/SGML -> one long normalised line of prose."""
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = htmllib.unescape(t)
    return re.sub(r"[\s   ]+", " ", t).strip()


MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
DATE_RE = re.compile(rf"(?:{MONTHS})\s+\d{{1,2}},\s*(?:19|20)\d{{2}}", re.I)
MONTH_N = {m.lower(): i + 1 for i, m in enumerate(MONTHS.split("|"))}
MONEY = r"\$\s?([\d,]+(?:\.\d{1,2})?)"


def parse_date(s):
    m = re.match(rf"({MONTHS})\s+(\d{{1,2}}),\s*((?:19|20)\d{{2}})", s.strip(), re.I)
    if not m:
        return None
    try:
        return dt.date(int(m.group(3)), MONTH_N[m.group(1).lower()], int(m.group(2)))
    except ValueError:
        return None


def money(s):
    try:
        return float(s.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def window(text, match, before=280, after=320):
    """A readable excerpt around a regex match, trimmed to word boundaries."""
    a, b = max(0, match.start() - before), min(len(text), match.end() + after)
    s = text[a:b].strip()
    if a:
        s = "…" + s.split(" ", 1)[-1]
    if b < len(text):
        s = s.rsplit(" ", 1)[0] + "…"
    return re.sub(r"\s+", " ", s)


# --------------------------------------------------------------- 1. filing list
def idx_rows(body):
    """Parse a fixed-width form.idx body into (form, company, cik, date, path)."""
    rows, started = [], False
    for line in body.splitlines():
        if not started:
            if line.startswith("---"):
                started = True
            continue
        # the columns are space-padded, not at fixed offsets that hold across
        # years, so split on runs of two or more spaces and anchor on the date
        m = re.match(r"^(\S.*?)\s{2,}(\S.*?)\s{2,}(\d+)\s+(\d{4}-\d{2}-\d{2})\s+(\S+)", line)
        if not m:
            continue
        form, name, cik, date, path = (g.strip() for g in m.groups())
        if form in FORMS:
            rows.append(dict(form=form, company=name, cik=cik, filing_date=date,
                             path=path))
    return rows


def quarters_between(start, end):
    y, q = start.year, (start.month - 1) // 3 + 1
    while (y, q) <= (end.year, (end.month - 1) // 3 + 1):
        yield y, q
        q += 1
        if q == 5:
            y, q = y + 1, 1


def from_indexes(start, end):
    """Quarterly form.idx for the covered quarters + daily files for the tail."""
    rows, last_received = [], None
    for y, q in quarters_between(start, end):
        body = cached(f"formidx-{y}-{q}", f"{ARCHIVES}/full-index/{y}/QTR{q}/form.idx")
        if body is None:
            log(f"  ! quarterly index {y}QTR{q} unavailable", file=sys.stderr)
            continue
        m = re.search(r"Last Data Received:\s*(.+)", body)
        if m:
            d = parse_date(m.group(1))
            if d and (last_received is None or d > last_received):
                last_received = d
        n = len(rows)
        rows += idx_rows(body)
        log(f"  full-index {y}QTR{q}: {len(rows) - n} tender filings")

    # fill the gap between the quarterly index and today from the daily indexes
    day = (last_received or end) + dt.timedelta(days=1)
    while day <= end:
        q = (day.month - 1) // 3 + 1
        body = cached(f"dayidx-{day}",
                      f"{ARCHIVES}/daily-index/{day.year}/QTR{q}/form.{day:%Y%m%d}.idx",
                      quiet503=True)
        if body:
            got = idx_rows(body)
            rows += got
            if got:
                log(f"  daily-index {day}: {len(got)} tender filings")
        day += dt.timedelta(days=1)

    seen, out = set(), []
    for r in rows:
        d = parse_date_iso(r["filing_date"])
        if d is None or not (start <= d <= end):
            continue
        acc = accession_from_path(r["path"])
        if acc in seen:
            continue
        seen.add(acc)
        r["accession"], r["date"] = acc, d
        out.append(r)
    return out


def parse_date_iso(s):
    try:
        return dt.date.fromisoformat(s.strip())
    except (ValueError, AttributeError):
        return None


def accession_from_path(path):
    m = re.search(r"(\d{10}-\d{2}-\d{6})", path)
    return m.group(1) if m else path


def from_fts(start, end):
    """Fallback: EDGAR full-text search, one form at a time, paged."""
    out, seen = [], set()
    for form in ("SC TO-I", "SC TO-C", "SC 13E4"):
        frm = 0
        while True:
            r = get(FTS, {"q": "", "forms": form, "startdt": str(start),
                          "enddt": str(end), "from": frm})
            if r is None:
                break
            try:
                h = r.json()["hits"]
            except (ValueError, KeyError):
                break
            for s in h["hits"]:
                src = s["_source"]
                acc = src.get("adsh", "")
                if acc in seen:
                    continue
                seen.add(acc)
                ciks = src.get("ciks") or [""]
                out.append(dict(form=src.get("form", form),
                                company=(src.get("display_names") or [""])[0],
                                cik=str(int(ciks[0])) if str(ciks[0]).isdigit() else "",
                                filing_date=src.get("file_date", ""),
                                date=parse_date_iso(src.get("file_date", "")),
                                accession=acc, path=""))
            frm += 100
            if frm >= h["total"]["value"] or not h["hits"]:
                break
    return [r for r in out if r["date"] and start <= r["date"] <= end]


# --------------------------------------------------------------- 2. per filing
def doc_manifest(cik, accession):
    """[(type, filename, size)] plus the subject company's SIC, from EDGAR."""
    nod = accession.replace("-", "")
    base = f"{ARCHIVES}/data/{int(cik)}/{nod}"
    hdr = cached(f"hdr-{accession}", f"{base}/{accession}-index-headers.html")
    if hdr is None:
        return [], "", base
    types = re.findall(r"&lt;TYPE&gt;([^\n<]+)", hdr)
    files = re.findall(r"&lt;FILENAME&gt;([^\n<]+)", hdr)
    sic = ""
    m = re.search(r"STANDARD INDUSTRIAL CLASSIFICATION:.*?\[(\d{4})\]", hdr)
    if m:
        sic = m.group(1)
    sizes = {}
    j = cached(f"idxjson-{accession}", f"{base}/index.json")
    if j:
        try:
            for it in json.loads(j)["directory"]["item"]:
                sizes[it["name"]] = int(it.get("size") or 0)
        except (ValueError, KeyError, TypeError):
            pass
    docs = [(t.strip(), f.strip(), sizes.get(f.strip(), 0))
            for t, f in zip(types, files) if f.strip().lower().endswith((".htm", ".html", ".txt"))]
    return docs, sic, base


def pick_offer_doc(docs):
    """Largest document in the exhibit (a)(1) family; else the largest document."""
    def norm(s):
        return re.sub(r"[^A-Z0-9]", "", s.upper())
    fam = [d for d in docs if re.search(r"A1(?:[A-H]|I{1,3}V?|VI{0,3}|IX|X)?$", norm(d[0]))]
    fam = fam or [d for d in docs if "A1" in norm(d[0])]
    pool = fam or [d for d in docs if not norm(d[0]).startswith(("GRAPHIC", "XML", "EXFILINGFEES"))]
    return max(pool, key=lambda d: d[2]) if pool else None


def primary_doc(docs):
    for d in docs:
        if re.match(r"SC\s?(TO|13E)", d[0], re.I):
            return d
    return docs[0] if docs else None


# --------------------------------------------------------------- 3. extraction
NOT_FOUND = "not found"


PAR_VALUE = re.compile(r"(?i)(par|stated)\s+value(?:\s+of)?\s*\$?\s*$")


def _par(t, pos):
    """True when the dollar figure at `pos` is a par value, not an offer price."""
    return bool(PAR_VALUE.search(t[max(0, pos - 40):pos]))


def extract_price(t):
    """Fixed price, or a Dutch-auction range. Returns (kind, low, high, quote)."""
    rng = [
        # "not less than $X nor greater than $Y per share" and its inversions
        re.compile(rf"(?i)not\s+(?:less|greater|more)\s+than\s+{MONEY}\s*(?:nor|and|or|to)\s*"
                   rf"(?:not\s+)?(?:greater|less|more)\s+than\s+{MONEY}"),
        re.compile(rf"(?i)price\s+range\s+of\s+{MONEY}\s*(?:to|-|–|—)\s*{MONEY}"),
        re.compile(rf"(?i)at\s+a\s+(?:purchase\s+)?price\s+(?:of\s+)?"
                   rf"{MONEY}\s*(?:to|-|–|—)\s*{MONEY}\s+per\s+(?:share|unit)"),
    ]
    for rx in rng:
        for m in rx.finditer(t):
            if _par(t, m.start(1)):
                continue
            a, b = money(m.group(1)), money(m.group(2))
            if a is not None and b is not None and a != b:
                return "Dutch auction", min(a, b), max(a, b), window(t, m)

    fixed = [
        re.compile(rf"(?i)at\s+a\s+(?:purchase\s+)?price\s+of\s+{MONEY}\s+(?:net\s+)?"
                   rf"(?:in\s+cash\s+)?per\s+(?:share|unit|ordinary\s+share)"),
        re.compile(rf"(?i)(?:purchase|tender)\s+price\s+of\s+{MONEY}\s+per\s+(?:share|unit|ordinary\s+share)"),
        re.compile(rf"(?i)(?:purchase|buy|pay|acquire)[^.]{{0,90}}?{MONEY}\s+(?:net\s+)?"
                   rf"(?:in\s+cash,?\s+)?per\s+(?:share|unit|ordinary\s+share)"),
        re.compile(rf"(?i){MONEY}\s+(?:net\s+)?(?:in\s+cash,?\s+)?per\s+(?:share|unit|ordinary\s+share)"),
    ]
    for rx in fixed:
        for m in rx.finditer(t):
            if _par(t, m.start(1)):          # "par value $0.01 per share" is not a bid
                continue
            v = money(m.group(1))
            if v:
                return "Fixed price", v, v, window(t, m)
    return NOT_FOUND, None, None, NOT_FOUND


def extract_expiration(t):
    """The date most often stated right after an 'expire' token."""
    votes, quotes = {}, {}
    for m in re.finditer(r"(?i)\bexpir(?:e|es|ed|ation|ing)\b", t):
        seg = t[m.end():m.end() + 260]
        dm = DATE_RE.search(seg)
        if not dm:
            continue
        d = parse_date(dm.group(0))
        if not d:
            continue
        # weight cover-page phrasing ("WILL EXPIRE AT 5:00 P.M. ... ON <date>")
        w = 1 + 3 * bool(re.search(r"(?i)(midnight|[\d:]{4,5}\s*[ap]\.?m|new york city time)", seg))
        votes[d] = votes.get(d, 0) + w
        quotes.setdefault(d, window(t, m, 120, 260))
    if not votes:
        return None, NOT_FOUND
    best = max(votes.items(), key=lambda kv: (kv[1], kv[0]))[0]
    return best, quotes[best]


def extract_odd_lot(t):
    """(verdict, quoted sentence). 'yes' only when priority/proration is explicit."""
    if len(t) < 2000:                       # document unreadable: say so, do not say "no"
        return "unclear", NOT_FOUND
    hits = list(re.finditer(r"(?i)odd[\s‐-―-]?lot", t))
    if not hits:
        return "no", NOT_FOUND
    # an explicit denial beats everything: some funds say so in as many words
    deny = re.compile(r"(?i)(no(t| )\s*(have\s+)?(any\s+)?special\s+pro\s?ration|"
                      r"odd[\s-]?lots?\s+(?:tenders?\s+)?(?:are|will\s+be)\s+subject\s+to\s+prorat|"
                      r"no\s+odd[\s-]?lot\s+priorit)")
    for m in hits:
        seg = window(t, m)
        if deny.search(seg):
            return "no", seg
    strong = re.compile(r"(?i)(priorit|without\s+prorat|not\s+subject\s+to\s+prorat|"
                        r"before\s+prorat|free\s+of\s+prorat|purchase\s+all\s+.{0,40}odd)")
    best = None
    for m in hits:
        seg = window(t, m)
        if strong.search(seg):
            best = seg
            break
        best = best or seg
    verdict = "yes" if best and strong.search(best) else "unclear"
    # an explicit definition of the odd-lot holder strengthens the read
    if verdict == "unclear" and re.search(r"(?i)fewer\s+than\s+100\s+(?:shares|Shares)", t):
        verdict = "unclear"
    return verdict, best or NOT_FOUND


def extract_class(t):
    m = re.search(r"(?is)(.{0,140})\(Title of (?:the )?Class of Securities\)", t)
    return re.sub(r"\s+", " ", m.group(1)).strip(" .,") if m else NOT_FOUND


def extract_conditions(t):
    out = []
    if re.search(r"(?i)minimum\s+(?:tender\s+)?condition", t):
        out.append("minimum tender condition")
    elif re.search(r"(?i)condition(?:ed|al)\s+(?:up)?on\s+.{0,60}minimum", t):
        out.append("minimum tender condition")
    if re.search(r"(?i)not\s+(?:conditioned|subject\s+to|contingent)\s+(?:up)?on\s+.{0,60}financ", t):
        out.append("no financing condition")
    elif re.search(r"(?i)financing\s+condition", t):
        out.append("financing condition")
    if re.search(r"(?i)not\s+(?:conditioned|subject\s+to)\s+(?:up)?on\s+any\s+minimum", t):
        out = [c for c in out if c != "minimum tender condition"] + ["no minimum"]
    if re.search(r"(?i)not\s+subject\s+to\s+prorat", t):
        out.append("odd lots not subject to proration")
    return "; ".join(dict.fromkeys(out)) or NOT_FOUND


FUND_CLASS = re.compile(
    r"(?i)(shares?\s+of\s+beneficial\s+interest|units?\s+of\s+beneficial\s+interest|"
    r"limited\s+liability\s+company\s+interests|limited\s+partnership\s+interests|"
    r"founders.{0,3}\s+shares|class\s+[a-z]\d?\s+(?:common\s+)?(?:shares|units)|"
    r"class\s+[a-z](?:,|\s+and)\s)")
FUND_NAME = re.compile(r"(?i)(\b(fund|bdc)\b|private\s+credit|private\s+lending|"
                       r"private\s+markets|income\s+corp|capital\s+corp|lending\s+co)")
SENIOR = re.compile(r"(?i)(depositary\s+shares?|preferred\s+stock|preference\s+shares?|"
                    r"\bdebentures?\b|senior\s+notes|subordinated\s+notes|"
                    r"convertible\s+notes|\b\d(?:\.\d+)?%\s+notes)")


def classify(sic, cls, name, form, text, ticker=""):
    """Bucket the filing. Only 'share tender' rows are actionable for an odd lot."""
    if form == "SC TO-C":
        return "pre-commencement (SC TO-C)"
    if re.search(r"(?i)option", cls or "") or re.search(
            r"(?i)offer\s+to\s+exchange\s+certain\s+options|eligible\s+options", text[:8000]):
        return "option exchange"
    if re.search(r"(?i)\bwarrant", cls or ""):
        return "warrant exchange"
    if SENIOR.search(cls or "") or SENIOR.search(text[:8000]):
        return "debt / preferred tender"
    if (sic in SIC_FUND or FUND_CLASS.search(cls or "")
            or re.search(r"(?i)(net\s+asset\s+value\s+per\s+(?:share|unit)|interval\s+fund|"
                         r"rule\s+23c-3|repurchase\s+offer\s+amount)", text)
            # a name-only match is only trusted for issuers with no listed ticker:
            # an exchange-traded operating company always has one
            or (not ticker and FUND_NAME.search(name or "")
                and not re.search(r"(?i)\breit\b", name or ""))):
        # a *listed* fund tendering for its common shares is still a real trade
        return ("listed fund tender" if ticker and not SENIOR.search(cls or "")
                else "fund/BDC repurchase (NAV)")
    return "share tender"


def amendment_signals(t):
    """Termination / extension / final-results signals from an SC TO-I/A."""
    flags = []
    # every Schedule TO carries the sentence "Check the following box if the filing
    # is a final amendment reporting the results" next to an unchecked box, so the
    # phrase alone means nothing — require a ticked box or an affirmative statement
    if (re.search(r"☒[^☐☒]{0,140}final amendment", t, re.I)
            or re.search(r"(?i)(is|constitutes)\s+the\s+final\s+amendment", t)):
        flags.append("final amendment (results)")
    if re.search(r"(?i)\b(has\s+terminated\s+the\s+offer|the\s+offer\s+(?:has\s+been|is)\s+"
                 r"terminated|hereby\s+(?:terminates|withdraws)\s+the\s+offer)\b", t):
        flags.append("terminated/withdrawn")
    ext = None
    m = re.search(rf"(?i)(?:extend(?:ed|s|ing)?|expiration date[^.]{{0,60}})[^.]{{0,160}}?({DATE_RE.pattern})", t)
    if m:
        ext = parse_date(m.group(1))
    return flags, ext


# --------------------------------------------------------------- 4. market data
def ticker_map():
    body = cached("company_tickers", TICKER_MAP)
    out = {}
    if body:
        try:
            for v in json.loads(body).values():
                out.setdefault(int(v["cik_str"]), v["ticker"].upper())
        except (ValueError, KeyError, TypeError):
            pass
    return out


def quote(tickers):
    """{ticker: last price}. yfinance is optional; missing prices become None."""
    px = {}
    if not tickers:
        return px
    try:
        import yfinance as yf
    except ImportError:
        log("  ! yfinance not installed; prices omitted", file=sys.stderr)
        return px
    try:
        data = yf.download(list(tickers), period="5d", progress=False,
                           auto_adjust=False, threads=True)
        close = data["Close"] if "Close" in data else data
        for t in tickers:
            try:
                s = close[t] if hasattr(close, "columns") and t in close.columns else close
                s = s.dropna()
                if len(s):
                    px[t] = float(s.iloc[-1])
            except (KeyError, IndexError, TypeError, ValueError):
                pass
    except Exception as e:                                   # noqa: BLE001
        log(f"  ! yfinance bulk download failed: {e}", file=sys.stderr)
    return px


# --------------------------------------------------------------- 5. the pipeline
def process(filing, tmap):
    cik = filing["cik"]
    docs, sic, base = doc_manifest(cik, filing["accession"])
    row = dict(filing)
    row.update(sic=sic, url=f"{base}/{filing['accession']}-index.htm",
               ticker=tmap.get(int(cik), ""), doc="", offer_type=NOT_FOUND,
               price_low=None, price_high=None, price_quote=NOT_FOUND,
               expires=None, expires_quote=NOT_FOUND, odd_lot="unclear",
               odd_lot_quote=NOT_FOUND, conditions=NOT_FOUND, security=NOT_FOUND,
               kind="share tender", flags="")
    if not docs:
        row["flags"] = "manifest unavailable"
        return row

    if time.monotonic() > DEADLINE[0]:
        row["flags"] = "skipped: time budget exhausted"
        row["odd_lot"] = "unclear"
        return row

    prim = primary_doc(docs)
    ptext = ""
    if prim:
        raw = cached(f"doc-{filing['accession']}-{prim[1]}", f"{base}/{prim[1]}")
        ptext = to_text(raw) if raw else ""
    row["security"] = extract_class(ptext) if ptext else NOT_FOUND

    offer = pick_offer_doc(docs)
    otext = ""
    if offer and (not prim or offer[1] != prim[1]):
        raw = cached(f"doc-{filing['accession']}-{offer[1]}", f"{base}/{offer[1]}")
        otext = to_text(raw) if raw else ""
        row["doc"] = offer[1]
    else:
        otext, row["doc"] = ptext, prim[1] if prim else ""

    full = otext if len(otext) > len(ptext) else ptext
    row["kind"] = classify(sic, row["security"], filing["company"], filing["form"],
                           ptext + " " + full, row["ticker"])

    row["offer_type"], row["price_low"], row["price_high"], row["price_quote"] = extract_price(full)
    exp, row["expires_quote"] = extract_expiration(full)
    row["expires"] = exp
    row["odd_lot"], row["odd_lot_quote"] = extract_odd_lot(full)
    row["conditions"] = extract_conditions(full)

    if filing["form"].endswith("/A") or filing["form"] == "SC TO-C":
        flags, ext = amendment_signals(ptext or full)
        row["flags"] = "; ".join(flags)
        if ext:
            row["expires"] = ext
    return row


def group_key(row):
    """One offer = one CIK; amendments fold into the original filing."""
    return str(int(row["cik"]))


def consolidate(rows):
    """Fold SC TO-I/A onto the SC TO-I they amend; newest terms win."""
    groups = {}
    for r in rows:
        groups.setdefault(group_key(r), []).append(r)
    out = []
    for _, g in groups.items():
        g.sort(key=lambda r: (r["date"], r["form"].endswith("/A")))
        originals = [r for r in g if not r["form"].endswith("/A") and r["form"] != "SC TO-C"]
        base = max(originals, key=lambda r: r["date"]) if originals else g[-1]
        base = dict(base)
        amends = [r for r in g if r is not base and r["date"] >= base["date"]]
        base["n_amendments"] = sum(1 for r in g if r["form"].endswith("/A"))
        base["last_filing"] = max(r["date"] for r in g)
        fl = [f for r in amends for f in (r["flags"] or "").split("; ") if f]
        for r in amends:                       # a later amendment can move the date
            if r["expires"] and base["expires"] and r["expires"] > base["expires"]:
                base["expires"] = r["expires"]
                fl.append("expiration extended by amendment")
        base["flags"] = "; ".join(dict.fromkeys(list(filter(None, [base["flags"]])) + fl))
        out.append(base)
    return out


# --------------------------------------------------------------- 6. the outputs
def fmt_money(v):
    return "n/a" if v is None else (f"${v:,.4f}" if v < 0.5 else f"${v:,.2f}")


def fmt_pct(v):
    return "n/a" if v is None else f"{v:+.1%}"


def build(rows, today):
    for r in rows:
        px = r.get("price")
        lo, hi = r.get("price_low"), r.get("price_high")
        r["prem_low"] = (lo / px - 1) if (px and lo) else None
        r["prem_high"] = (hi / px - 1) if (px and hi) else None
        r["profit_low"] = (lo - px) * 99 if (px and lo) else None
        r["profit_high"] = (hi - px) * 99 if (px and hi) else None
        r["dte"] = (r["expires"] - today).days if r["expires"] else None
        warn = []
        # a premium this far from the market almost always means the parser locked
        # onto the wrong dollar figure (a liquidation preference, a fee, a par value)
        r["suspect"] = bool(r["prem_high"] is not None and abs(r["prem_high"]) > 0.60)
        if r["suspect"]:
            warn.append("price parse suspect — verify against the filing")
        elif r["prem_high"] is not None and r["prem_high"] < 0:
            warn.append("market above offer")
        if r["price_low"] is None and r["kind"] in ("share tender", "listed fund tender"):
            warn.append("offer price not parsed")
        if not r["ticker"] and r["kind"] in ("share tender", "listed fund tender"):
            warn.append("no listed ticker (non-traded?)")
        if r["dte"] is not None and r["dte"] < 0:
            warn.append("expired")
        if r["flags"]:
            warn.append(r["flags"])
        r["warnings"] = "; ".join(dict.fromkeys(w for w in warn if w))
    return rows


def md_table(rows, today):
    head = ("| Ticker | Company | Type | Offer price / range | Current | Premium lo/hi "
            "| 99-sh profit lo/hi | Expires | Days | Odd-lot | Flags | Filing |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    if not rows:
        return head + "| — | _no live offers matched in this window_ | | | | | | | | | | |\n"
    out = [head]
    for r in rows:
        pr = (fmt_money(r["price_low"]) if r["price_low"] == r["price_high"]
              else f"{fmt_money(r['price_low'])}–{fmt_money(r['price_high'])}")
        if r["price_low"] is None:
            pr = NOT_FOUND
        prof = ("n/a" if r["profit_low"] is None else
                (f"${r['profit_low']:,.0f}" if r["profit_low"] == r["profit_high"]
                 else f"${r['profit_low']:,.0f}/${r['profit_high']:,.0f}"))
        prem = ("n/a" if r["prem_low"] is None else
                (fmt_pct(r["prem_low"]) if r["prem_low"] == r["prem_high"]
                 else f"{fmt_pct(r['prem_low'])}/{fmt_pct(r['prem_high'])}"))
        out.append("| {t} | {c} | {k} | {p} | {px} | {prem} | {prof} | {e} | {d} | {o} | {w} | [{f}]({u}) |\n".format(
            t=r["ticker"] or "—", c=r["company"][:38], k=r["offer_type"],
            p=pr, px=fmt_money(r.get("price")), prem=prem, prof=prof,
            e=r["expires"] or NOT_FOUND, d="—" if r["dte"] is None else r["dte"],
            o=r["odd_lot"], w=r["warnings"] or "—", f=r["form"], u=r["url"]))
    return "".join(out)


EXPLAINER = """## How odd-lot tenders work, and the risks

An issuer self-tender (Schedule TO-I under Rule 13e-4) is a company offering to buy
back its own shares from holders, usually at a premium to the market, either at a
**fixed price** or through a **Dutch auction** in which holders name a price inside a
stated range and the company pays the single lowest price that fills its target. Most
of these offers grant **odd-lot priority**: a holder of **fewer than 100 shares** who
tenders *all* of them is bought in full and is exempt from the proration that hits
everyone else when the offer is oversubscribed. That is why 99 shares, not 100, is the
position size in the table above — at 100 shares the priority is lost entirely.

The risks are real and the arithmetic above ignores most of them:

* **The offer can be amended, extended, or withdrawn.** Terms change by amendment
  (SC TO-I/A) and offers are routinely conditioned on financing, on a minimum number
  of shares being tendered, or on no material adverse change. If the offer dies you
  are left holding the stock at whatever it is worth then, which is usually below the
  price you paid on the announcement.
* **Odd-lot priority is not universal.** It has to be in the offer document. The
  table quotes the actual sentence so it can be checked; "unclear" means the phrase
  appears without explicit priority or proration-exemption language, and "not found"
  means the parser could not locate the field at all. Read the offer to purchase.
* **Fewer than 100 shares, and all of them.** Priority applies only to holders who own
  fewer than 100 shares in total and tender every one. Owning 150 shares and tendering
  99 does not qualify. Holding across two brokers is a grey area — brokers certify the
  odd-lot status.
* **Dutch auctions can clear below the top of the range**, so the high-end profit
  column is a ceiling, not an expectation. Tendering at the low end (or "at the
  purchase price determined") maximises the chance of being bought.
* **Settlement and tax.** Cash typically arrives days to weeks after expiration, and
  brokers often charge a fee to tender. The proceeds are a normal sale for tax
  purposes: short-term capital gain at ordinary rates, and a repurchase can in some
  cases be treated as a dividend. Commissions and the bid-ask spread on a 99-share
  buy in an illiquid small cap can consume a meaningful share of the premium.
* **Capacity.** Each event is worth a few hundred dollars at most. That is the whole
  point — it is a structural edge precisely because it is too small for institutions.

This file is generated automatically from EDGAR filings and market data. It is
information, not investment advice, and no one has verified the extraction by hand.
Every number here should be checked against the offer to purchase before acting.
"""


def write_md(rows, today, stats):
    live = [r for r in rows
            if r["kind"] in ("share tender", "listed fund tender")
            and (r["ticker"] or r["price_low"] is not None)
            and not (r["dte"] is not None and r["dte"] < 0)]
    live.sort(key=lambda r: (r["expires"] or dt.date(2099, 1, 1), r["ticker"]))
    other = [r for r in rows if r not in live]
    other.sort(key=lambda r: (r["expires"] or dt.date(2099, 1, 1), r["company"]))

    body = [f"# Tender offers with odd-lot priority\n",
            f"\n_Generated {today} · EDGAR form indexes, last {stats['days']} days · "
            f"{stats['n_filings']} tender filings → {stats['n_offers']} distinct offers, "
            f"of which {stats['n_common']} are common-stock self-tenders · "
            f"{stats['n_odd']} carry odd-lot priority ({stats['n_odd_common']} in common stock)._\n\n",
            "## Live share tenders\n\n", md_table(live, today),
            "\n### Odd-lot language, quoted\n\n"]
    for r in live:
        if r["odd_lot_quote"] != NOT_FOUND:
            body.append(f"* **{r['ticker'] or r['company'][:30]}** — _{r['odd_lot_quote']}_\n")
    if not any(r["odd_lot_quote"] != NOT_FOUND for r in live):
        body.append("* _No odd-lot language located in the live offers._\n")

    body.append("\n## Everything else seen in the window\n\n")
    body.append("Option/warrant exchanges, closed-end fund and BDC repurchases at net "
                "asset value (no premium by construction), expired offers, and filings "
                "the parser could not read.\n\n")
    body.append("| Ticker | Company | Kind | Offer | Expires | Odd-lot | Notes | Filing |\n"
                "|---|---|---|---|---|---|---|---|\n")
    for r in other:
        pr = (NOT_FOUND if r["price_low"] is None else
              (fmt_money(r["price_low"]) if r["price_low"] == r["price_high"]
               else f"{fmt_money(r['price_low'])}–{fmt_money(r['price_high'])}"))
        body.append(f"| {r['ticker'] or '—'} | {r['company'][:38]} | {r['kind']} | {pr} | "
                    f"{r['expires'] or NOT_FOUND} | {r['odd_lot']} | "
                    f"{r['warnings'] or '—'} | [{r['form']}]({r['url']}) |\n")

    body.append("\n" + EXPLAINER)
    OUT_MD.write_text("".join(body), encoding="utf-8")


CSV_COLS = ["scan_date", "cik", "ticker", "company", "form", "filing_date", "accession",
            "kind", "security", "offer_type", "price_low", "price_high", "expires",
            "days_to_expiry", "current_price", "premium_low", "premium_high",
            "profit_99_low", "profit_99_high", "odd_lot", "conditions", "sic",
            "n_amendments", "last_filing", "flags", "warnings", "suspect", "odd_lot_quote",
            "price_quote", "expires_quote", "url"]


def write_csv(rows, today):
    prior, seen = [], set()
    if OUT_CSV.exists():
        with OUT_CSV.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                prior.append(r)
    keys = {(r.get("accession"), r.get("scan_date")) for r in prior}
    new = []
    for r in rows:
        rec = dict(
            scan_date=str(today), cik=r["cik"], ticker=r["ticker"], company=r["company"],
            form=r["form"], filing_date=str(r["date"]), accession=r["accession"],
            kind=r["kind"], security=r["security"], offer_type=r["offer_type"],
            price_low=r["price_low"], price_high=r["price_high"],
            expires=r["expires"] or "", days_to_expiry=r["dte"],
            current_price=r.get("price"), premium_low=r["prem_low"],
            premium_high=r["prem_high"], profit_99_low=r["profit_low"],
            profit_99_high=r["profit_high"], odd_lot=r["odd_lot"],
            conditions=r["conditions"], sic=r["sic"],
            n_amendments=r.get("n_amendments", 0), last_filing=r.get("last_filing", ""),
            flags=r["flags"], warnings=r["warnings"], suspect=int(bool(r.get("suspect"))),
            odd_lot_quote=r["odd_lot_quote"][:600], price_quote=r["price_quote"][:400],
            expires_quote=r["expires_quote"][:400], url=r["url"])
        if (rec["accession"], rec["scan_date"]) in keys or (rec["accession"], rec["scan_date"]) in seen:
            continue
        seen.add((rec["accession"], rec["scan_date"]))
        new.append(rec)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        for r in prior + new:
            w.writerow({k: r.get(k, "") for k in CSV_COLS})
    return len(new)


# --------------------------------------------------------------- main
def main():
    global USE_CACHE
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=45)
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--budget", type=float, default=40,
                    help="minutes of document fetching before the rest are skipped")
    a = ap.parse_args()
    USE_CACHE = not a.no_cache
    DEADLINE[0] = time.monotonic() + a.budget * 60

    today = dt.date.today()
    start = today - dt.timedelta(days=a.days)
    HERE.mkdir(parents=True, exist_ok=True)

    log(f"Tender scan {start} .. {today}")
    filings = from_indexes(start, today)
    route = "EDGAR form indexes (full-index + daily-index)"
    if not filings:
        log("  index route empty — falling back to EDGAR full-text search")
        filings = from_fts(start, today)
        route = "EDGAR full-text search (efts.sec.gov)"
    log(f"  route: {route}; {len(filings)} filings "
          f"({sum(1 for f in filings if f['form'] == 'SC TO-I')} SC TO-I)")

    log("  fetching CIK->ticker map")
    tmap = ticker_map()
    log(f"  ticker map: {len(tmap)} CIKs")
    rows = []
    with ThreadPoolExecutor(WORKERS) as ex:
        for i, r in enumerate(ex.map(lambda f: process(f, tmap), filings), 1):
            rows.append(r)
            if i % 10 == 0 or i == len(filings):
                log(f"  parsed {i}/{len(filings)}")

    offers = consolidate(rows)
    px = quote({r["ticker"] for r in offers if r["ticker"]
                and r["kind"] in ("share tender", "listed fund tender")})
    for r in offers:
        r["price"] = px.get(r["ticker"])

    offers = build(offers, today)
    n_common = sum(1 for r in offers
                   if r["kind"] in ("share tender", "listed fund tender"))
    stats = dict(days=a.days, n_filings=len(filings), n_offers=len(offers),
                 n_common=n_common,
                 n_odd=sum(1 for r in offers if r["odd_lot"] == "yes"),
                 n_odd_common=sum(1 for r in offers if r["odd_lot"] == "yes"
                                  and r["kind"] in ("share tender", "listed fund tender")))
    write_md(offers, today, stats)
    n_new = write_csv(offers, today)

    print(f"\nSC TO-I filings: {sum(1 for f in filings if f['form'] == 'SC TO-I')}")
    print(f"distinct offers: {len(offers)}   odd-lot priority: {stats['n_odd']}")
    print(f"wrote {OUT_MD.relative_to(ROOT)} and {n_new} new rows to {OUT_CSV.relative_to(ROOT)}")

    live = [r for r in offers
            if r["kind"] in ("share tender", "listed fund tender") and r["profit_high"]
            and not r["suspect"] and (r["dte"] is None or r["dte"] >= 0)]
    live.sort(key=lambda r: -r["profit_high"])
    for r in live[:5]:
        log(f"  {r['ticker'] or r['company'][:24]:8s} "
              f"{fmt_money(r['price_low'])}-{fmt_money(r['price_high'])} "
              f"vs {fmt_money(r.get('price'))} "
              f"prem {fmt_pct(r['prem_high'])} 99sh ${r['profit_high']:,.0f} "
              f"exp {r['expires']} odd-lot {r['odd_lot']}")


if __name__ == "__main__":
    main()

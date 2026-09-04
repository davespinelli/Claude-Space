#!/usr/bin/env python3
"""Fetch an earnings call transcript (or the closest legally-available substitute)
for a US-listed ticker and write it to research/deepvalue/filings/<TICKER>/.

Source chain (see TRANSCRIPT_SOURCES.md for the full research write-up):

  1. earningscall  -- v2.api.earningscall.biz. Works with NO key using the public
                      "demo" key, but the demo key only covers AAPL and MSFT.
                      Set EARNINGSCALL_API_KEY for the full 5,000+ company universe.
                      Yields a FULL transcript.
  2. alphavantage  -- EARNINGS_CALL_TRANSCRIPT. Needs a free key (25 req/day),
                      obtainable in under a minute at alphavantage.co/support/#api-key.
                      Set ALPHAVANTAGE_API_KEY. Yields a FULL transcript.
  3. sec           -- EDGAR 8-K Item 2.02 EX-99 exhibits. No key, no rate-limit
                      problems, works for essentially every US filer. Yields
                      PREPARED REMARKS when the company files them (rare for small
                      caps) and otherwise the EARNINGS PRESS RELEASE.

Deliberately NOT implemented: fool.com, seekingalpha.com and finance.yahoo.com
scraping. Their terms of use prohibit automated access (see TRANSCRIPT_SOURCES.md).

Usage:
    fetch_transcript.py TICKER [--quarter 2026Q2] [--source auto|earningscall|alphavantage|sec]
                               [--list-sources] [--force]

Exit codes: 0 = wrote a file, 1 = nothing available, 2 = bad usage/ticker.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
try:
    from dotenv import load_dotenv; load_dotenv(__import__('pathlib').Path(__file__).resolve().parents[2] / '.env')
except Exception:
    pass
import re
import sys
import time
from pathlib import Path

import warnings

import requests
from bs4 import BeautifulSoup

try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent
OUT_ROOT = ROOT / "filings"
CACHE = ROOT / ".cache"

# EDGAR requires a descriptive UA with contact info. Overridable via SEC_USER_AGENT.
SEC_UA = os.environ.get("SEC_USER_AGENT", "ClaudeSpace research dspinjr@gmail.com")

FULL_TRANSCRIPT = "full_transcript"
PREPARED_REMARKS = "prepared_remarks"
PRESS_RELEASE = "press_release"
PRESENTATION = "investor_presentation"

CONTENT_LABEL = {
    FULL_TRANSCRIPT: "FULL TRANSCRIPT (prepared remarks + Q&A)",
    PREPARED_REMARKS: "PREPARED REMARKS ONLY (no Q&A)",
    PRESS_RELEASE: "EARNINGS PRESS RELEASE ONLY (not a transcript)",
    PRESENTATION: "INVESTOR PRESENTATION ONLY (not a transcript)",
}


class Result:
    def __init__(self, text, content_type, source, source_url, event_date,
                 fiscal_label="", notes="", period_code="", period_source=""):
        self.text = text
        self.content_type = content_type
        self.source = source
        self.source_url = source_url
        self.event_date = event_date          # "YYYY-MM-DD"
        self.fiscal_label = fiscal_label      # e.g. "FY2026 Q2"
        self.notes = notes
        self.period_code = period_code        # e.g. "2026Q1" / "2025FY" -> filename
        self.period_source = period_source    # how the period was determined

    def resolve_period(self):
        """Fill period_code/fiscal_label from the document text when the API did
        not supply them. Returns (period_code, fiscal_label, period_source)."""
        if self.period_code:
            return self.period_code, self.fiscal_label, self.period_source or "API response"
        code, label = parse_period(self.text)
        if code:
            self.period_code, self.period_source = code, "parsed from the document text"
            if not self.fiscal_label:
                self.fiscal_label = label
        else:
            self.period_source = "not stated in the document; file dated by the filing date"
        return self.period_code, self.fiscal_label, self.period_source


# ------------------------------------------------------- fiscal-period parsing

ORD_Q = {"first": 1, "second": 2, "third": 3, "fourth": 4}
MONTH_NUM = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"])}
SPAN_LABEL = {"three": "Q", "six": "H1 through Q", "nine": "9M through Q",
              "twelve": "FY through Q"}


def parse_period(text: str) -> tuple[str, str]:
    """Best-effort fiscal period of the call/release -> ("2026Q1", "Q1 2026").

    Returns ("", "") when the document does not state a period. Only the first
    ~8k characters are considered: that is the headline / dateline region, where
    the period is always named, and it avoids matching year-over-year comparison
    tables deeper in the release.
    """
    head = re.sub(r"\s+", " ", (text or "")[:8000])
    pats = [
        # "fourth quarter and full year 2025", "first quarter of fiscal 2026"
        (r"\b(first|second|third|fourth)\s+quarter\b[^.]{0,60}?\b(?:of\s+)?"
         r"(?:the\s+)?(?:fiscal\s+)?(?:year\s+)?(?:ended\s+[A-Za-z]+\s+\d{1,2},?\s+)?"
         r"(20\d{2})\b", "ord_year"),
        # "fiscal 2026 first quarter"
        (r"\b(?:fiscal\s+)?(?:year\s+)?(20\d{2})\s+(first|second|third|fourth)\s+quarter\b",
         "year_ord"),
        # "Q2 2026", "Q2 FY2026", "second-quarter 2026"
        (r"\bQ([1-4])\s*(?:FY|fiscal)?\s*(20\d{2})\b", "q_year"),
        (r"\b(?:FY|fiscal)?\s*(20\d{2})\s*[-\s]?Q([1-4])\b", "year_q"),
    ]
    for pat, kind in pats:
        m = re.search(pat, head, re.I)
        if not m:
            continue
        if kind == "ord_year":
            q, y = ORD_Q[m.group(1).lower()], m.group(2)
        elif kind == "year_ord":
            q, y = ORD_Q[m.group(2).lower()], m.group(1)
        elif kind == "q_year":
            q, y = int(m.group(1)), m.group(2)
        else:
            q, y = int(m.group(2)), m.group(1)
        return f"{y}Q{q}", f"Q{q} {y}"
    # "three / six / nine months ended June 30, 2026"
    m = re.search(r"\b(three|six|nine|twelve)\s+months\s+ended\s+"
                  r"([A-Za-z]+)\s+\d{1,2},?\s+(20\d{2})", head, re.I)
    if m:
        mon = MONTH_NUM.get(m.group(2).lower())
        if mon:
            q, y = (mon - 1) // 3 + 1, m.group(3)
            span = SPAN_LABEL[m.group(1).lower()]
            return f"{y}Q{q}", f"{span}{q} {y} ({m.group(1).lower()} months ended)"
    # "full year 2025", "fiscal year ended December 31, 2025"
    m = re.search(r"\b(?:full[- ]year|fiscal\s+year|year)\s+(?:ended|ending)\s+"
                  r"[A-Za-z]+\s+\d{1,2},?\s+(20\d{2})", head, re.I)
    if not m:
        m = re.search(r"\bfull[- ]year\s+(?:results\s+)?(?:for\s+)?(20\d{2})\b", head, re.I)
    if m:
        return f"{m.group(1)}FY", f"FY{m.group(1)}"
    return "", ""


def log(msg):
    print(msg, file=sys.stderr)


def session(ua):
    s = requests.Session()
    s.headers.update({"User-Agent": ua})
    return s


# ---------------------------------------------------------------- SEC helpers

_sec = None


def sec_session():
    global _sec
    if _sec is None:
        _sec = session(SEC_UA)
    return _sec


# EDGAR throttles hard; scanning several 6-K indexes in a row trips a 503
# unless the requests are paced and transient failures are retried.
SEC_RPS = 5.0
_sec_last = [0.0]


def sec_get(url, timeout=30, tries=3):
    """Throttled EDGAR GET with retry on 429/503. Raises on final failure."""
    last = None
    for attempt in range(tries):
        gap = 1.0 / SEC_RPS if SEC_RPS > 0 else 0.0
        delta = time.monotonic() - _sec_last[0]
        if delta < gap:
            time.sleep(gap - delta)
        _sec_last[0] = time.monotonic()
        try:
            r = sec_session().get(url, timeout=timeout)
            if r.status_code in (429, 503):
                last = requests.HTTPError(f"{r.status_code} from EDGAR", response=r)
                time.sleep(1.0 + 2 * attempt)
                continue
            r.raise_for_status()
            return r
        except Exception as e:                      # noqa: BLE001
            last = e
            time.sleep(1.0 + 2 * attempt)
    raise last


def ticker_to_cik(ticker):
    """Map ticker -> zero-padded CIK using SEC's own mapping file (cached 24h)."""
    CACHE.mkdir(exist_ok=True)
    f = CACHE / "company_tickers.json"
    fresh = f.exists() and (time.time() - f.stat().st_mtime) < 86400
    if not fresh:
        try:
            r = sec_session().get(
                "https://www.sec.gov/files/company_tickers.json", timeout=30)
            r.raise_for_status()
            f.write_text(r.text)
        except Exception as e:
            if not f.exists():
                raise
            log(f"  ! could not refresh SEC ticker map ({e}); using cached copy")
    data = json.loads(f.read_text())
    m = {v["ticker"].upper(): str(v["cik_str"]).zfill(10) for v in data.values()}
    return m.get(ticker.upper())


def html_to_text(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = "\n".join(line.strip() for line in text.splitlines()).strip()
    # EDGAR prepends a small document header (type / seq / filename) to the
    # served exhibit. Drop everything up to the first "Exhibit 99.x" marker.
    m = re.search(r"^\s*Exhibit\s+99[.\d]*\s*$", text[:2000], re.I | re.M)
    if m:
        text = text[m.end():].lstrip()
    return text


# Deliberately narrow. Phrases like "Management Commentary" are standard
# earnings-PRESS-RELEASE section headings and must NOT match here.
REMARKS_RE = re.compile(
    r"prepared\s+remarks|conference\s+call\s+script|earnings\s+call\s+script"
    r"|call\s+transcript|earnings\s+call\s+remarks", re.I)
# Markers that only appear in an actual spoken-call document.
OPERATOR_RE = re.compile(
    r"\bOperator\s*[:\u2014-]|Thank you,? operator|operator instructions"
    r"|turn the call (?:back )?over to|ladies and gentlemen, (?:thank you|welcome)",
    re.I)
QA_RE = re.compile(r"question[- ]and[- ]answer|\bQ\s*&\s*A\s+session", re.I)
DECK_RE = re.compile(r"presentation|slide|supplement|deck|infographic", re.I)


def classify_exhibit(desc, filename, text):
    """Decide what an EX-99 exhibit actually is, using its label then its content.

    Erring toward PRESS_RELEASE is intentional: over-claiming that a press
    release is a transcript is the worst failure mode for this pipeline.
    """
    label = f"{desc} {filename}"
    if REMARKS_RE.search(label):
        # Even a labelled "prepared remarks" exhibit is a full transcript if it
        # carries a Q&A section.
        return FULL_TRANSCRIPT if QA_RE.search(text) else PREPARED_REMARKS
    has_operator = bool(OPERATOR_RE.search(text))
    if has_operator and QA_RE.search(text):
        return FULL_TRANSCRIPT
    if has_operator or REMARKS_RE.search(text[:4000]):
        return PREPARED_REMARKS
    if DECK_RE.search(label):
        return PRESENTATION
    # Slide decks converted to HTML are short and full of fragments; press
    # releases read as prose with a dateline and a "Non-GAAP"/"About" section.
    if re.search(r"safe harbor|forward-looking statements", text[:3000], re.I) \
            and len(text) < 20000 and text.count(".") < 120:
        return PRESENTATION
    return PRESS_RELEASE


RANK = {FULL_TRANSCRIPT: 0, PREPARED_REMARKS: 1, PRESS_RELEASE: 2, PRESENTATION: 3}

# How many recent 6-Ks to look through for an earnings release. FPIs file 6-Ks
# for everything (charters, AGMs, press releases), so the earnings one is rarely
# the newest; a handful covers a quarter's worth of filings.
SIX_K_SCAN = 8

EARNINGS_DOC_RE = re.compile(
    r"(?:financial|operating|interim|quarterly|annual|half[- ]year|full[- ]year)\s+"
    r"(?:and\s+operating\s+)?results"
    r"|results\s+for\s+(?:the|its|fiscal)"
    r"|(?:reports?|announces?)\s+(?:its\s+)?(?:\w+[- ]){0,4}results"
    r"|earnings\s+(?:release|results|call|report)"
    r"|unaudited\s+(?:interim\s+)?(?:condensed\s+)?(?:consolidated\s+)?financial", re.I)
NOT_EARNINGS_DOC_RE = re.compile(
    r"results\s+of\s+(?:its\s+|the\s+)?(?:\d{4}\s+)?(?:annual|extraordinary|special)"
    r"(?:\s+general)?\s+meeting|voting\s+results"
    r"|results\s+of\s+(?:its\s+|the\s+)?(?:tender|exchange)\s+offer", re.I)
EARNINGS_CONFIRM_DOC_RE = re.compile(
    r"\bnet\s+(?:income|loss|revenues?)\b|\badjusted\s+ebitda\b|\bearnings\s+per\s+share\b"
    r"|\bper\s+(?:common\s+)?share\b|\bgross\s+(?:profit|margin)\b"
    r"|\boperating\s+income\b|\btotal\s+revenues?\b", re.I)


def is_earnings_document(desc, url, text):
    """Does this 6-K exhibit read as an earnings release rather than a charter
    announcement, AGM notice or shelf-registration housekeeping?"""
    head = f"{desc} {url.rsplit('/', 1)[-1]} " + re.sub(r"\s+", " ", (text or "")[:4000])
    if NOT_EARNINGS_DOC_RE.search(head):
        return False
    if not EARNINGS_DOC_RE.search(head):
        return False
    return bool(EARNINGS_CONFIRM_DOC_RE.search((text or "")[:20000]))


# 8-Ks carry the release in EX-99. Foreign private issuers use EX-1/EX-2, and
# often put the release straight into the 6-K document itself.
EX_8K_TYPE = re.compile(r"^EX-99(?:\.\d+)?$", re.I)
EX_6K_TYPE = re.compile(r"^(?:EX-(?:99|1|2)(?:\.\d+)?|6-K(?:/A)?)$", re.I)


def sec_exhibit_rows(cik, accession, six_k=False):
    """Return [(type, description, url)] for the readable docs in a filing.

    8-K: EX-99* only. 6-K: EX-99/EX-1/EX-2 plus the 6-K body, because FPIs
    routinely file the earnings release as the primary document.
    """
    want = EX_6K_TYPE if six_k else EX_8K_TYPE
    acc_nodash = accession.replace("-", "")
    url = (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
           f"{acc_nodash}/{accession}-index.htm")
    r = sec_get(url)
    soup = BeautifulSoup(r.text, "lxml")
    rows = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 4:
            continue
        doc_type = tds[3].get_text(strip=True)
        if not want.match(doc_type):
            continue
        a = tds[2].find("a")
        if not a or not a.get("href"):
            continue
        href = a["href"]
        # iXBRL viewer links wrap the real document
        href = href.replace("/ix?doc=", "")
        if not href.lower().split("?")[0].endswith((".htm", ".html", ".txt")):
            continue
        rows.append((doc_type, tds[1].get_text(strip=True),
                     "https://www.sec.gov" + href))
    return url, rows


def fetch_sec(ticker, want_quarter=None):
    cik = ticker_to_cik(ticker)
    if not cik:
        log(f"  - SEC: no CIK found for {ticker} in SEC's ticker mapping")
        return None
    sub = sec_get(f"https://data.sec.gov/submissions/CIK{cik}.json").json()
    recent = sub["filings"]["recent"]
    company = sub.get("name", ticker)

    eights, sixes = [], []
    for i, form in enumerate(recent["form"]):
        if form == "8-K" and "2.02" in (recent["items"][i] or ""):
            eights.append((recent["filingDate"][i], recent["accessionNumber"][i]))
        elif form.startswith("6-K"):
            sixes.append((recent["filingDate"][i], recent["accessionNumber"][i]))

    if eights:
        # unchanged behaviour for domestic filers: newest 8-K with Item 2.02
        candidates, form_label, scan = eights[:1], "8-K Item 2.02", 1
    elif sixes:
        # Foreign private issuers file 6-K instead of 8-K and 6-Ks carry no item
        # codes, so scan the recent ones for the newest earnings exhibit.
        candidates, form_label, scan = sixes[:SIX_K_SCAN], "6-K", SIX_K_SCAN
        log(f"  - SEC: {ticker} files 6-K (foreign private issuer); scanning the "
            f"{len(candidates)} most recent for an earnings release")
    else:
        log(f"  - SEC: no 8-K with Item 2.02 and no 6-K filings for {ticker}")
        return None

    best_overall = None
    for filing_date, accession in candidates[:scan]:
        try:
            index_url, rows = sec_exhibit_rows(cik, accession, six_k=(form_label == "6-K"))
        except Exception as e:                      # noqa: BLE001
            log(f"  ! SEC: could not read the {filing_date} filing index: {e}")
            continue
        if not rows:
            if form_label == "8-K Item 2.02":
                log(f"  - SEC: 8-K {filing_date} has no EX-99 exhibits")
            continue
        best = None
        for doc_type, desc, url in rows:
            try:
                body = sec_get(url)
            except Exception as e:                  # noqa: BLE001
                log(f"  ! SEC: could not fetch {url}: {e}")
                continue
            text = html_to_text(body.text)
            if len(text) < 200:
                continue
            ctype = classify_exhibit(desc, url.rsplit("/", 1)[-1], text)
            cand = (RANK[ctype], -len(text), ctype, doc_type, desc, url, text)
            if best is None or cand[:2] < best[:2]:
                best = cand
        if best is None:
            continue
        _, _, ctype, doc_type, desc, url, text = best
        if form_label == "6-K" and not is_earnings_document(desc, url, text):
            continue                      # charter announcement, AGM notice, ...
        notes = (f"Selected {doc_type} from the {form_label.split()[0]} filed "
                 f"{filing_date}. Filing index: {index_url}")
        if form_label == "6-K":
            notes += ("\n> NOTE: this is a foreign private issuer; it reports on Form 6-K "
                      "rather than 8-K, and this exhibit is the most recent 6-K that reads "
                      "as an earnings release.")
        if ctype in (PRESS_RELEASE, PRESENTATION):
            notes += ("\n> NOTE: this company did not file prepared remarks or a "
                      "call transcript as an exhibit. This is the closest "
                      "SEC-sourced substitute, not the call itself.")
        res = Result(text, ctype,
                     f"SEC EDGAR {form_label}, {doc_type} ({company})",
                     url, filing_date, notes=notes)
        if ctype in (FULL_TRANSCRIPT, PREPARED_REMARKS):
            return res                    # cannot do better
        if best_overall is None:
            best_overall = res
    if best_overall is None and form_label == "6-K":
        log(f"  - SEC: none of the {len(candidates)} most recent 6-Ks for {ticker} "
            f"contained an earnings release")
    return best_overall


# ------------------------------------------------------------------ API keys

# A key that was never filled in is worse than no key at all: it turns a clean
# "SKIPPED, no key" into a 401/403 that reads like the source being down. An
# empty value, a leftover placeholder, or anything too short to be a real key is
# therefore treated as UNSET.
KEY_PLACEHOLDERS = ("paste", "your_key", "your-key", "yourkey", "xxxxxxxx")
KEY_MIN_LEN = 8


def clean_key(raw):
    """Return a usable API key, or None if the value is effectively unset."""
    k = (raw or "").strip().strip("\"'")
    if len(k) < KEY_MIN_LEN:
        return None
    low = k.lower()
    if any(m in low for m in KEY_PLACEHOLDERS):
        return None
    return k


def _key_looks_set_but_isnt(raw):
    """True when the env var is non-empty but is a placeholder / too short."""
    return bool((raw or "").strip()) and clean_key(raw) is None


# --------------------------------------------------------------- earningscall

EC_BASE = "https://v2.api.earningscall.biz"
EC_EXCHANGES = ["NASDAQ", "NYSE", "AMEX", "OTC"]

# The public "demo" key covers AAPL and MSFT only. Without this latch a batch run
# pays four HTTP round trips per ticker to relearn that for every name in the
# universe, so the demo path is attempted at most once per process.
_ec_demo_spent = [False]
_ec_key_warned = [False]


def ec_key():
    return clean_key(os.environ.get("EARNINGSCALL_API_KEY"))


def fetch_earningscall(ticker, want_quarter=None):
    key = ec_key()
    if key is None:
        raw = os.environ.get("EARNINGSCALL_API_KEY")
        if _key_looks_set_but_isnt(raw) and not _ec_key_warned[0]:
            _ec_key_warned[0] = True
            log("  - earningscall: EARNINGSCALL_API_KEY is a placeholder or too short "
                "-> treated as UNSET, falling back to the public demo key")
        key = "demo"
    if key == "demo" and _ec_demo_spent[0]:
        log("  - earningscall: SKIPPED, demo key covers AAPL/MSFT only and was already "
            "tried once this process (set EARNINGSCALL_API_KEY for full coverage)")
        return None
    s = session("ClaudeSpace research")
    for exchange in EC_EXCHANGES:
        try:
            r = s.get(f"{EC_BASE}/events",
                      params={"apikey": key, "exchange": exchange,
                              "symbol": ticker.upper()}, timeout=25)
        except Exception as e:
            log(f"  ! earningscall: {e}")
            return None
        if r.status_code == 403:
            continue  # not covered by this plan
        if r.status_code != 200:
            continue
        events = r.json().get("events") or []
        events = [e for e in events if e.get("is_published")]
        if not events:
            continue
        if want_quarter:
            yr, q = int(want_quarter[:4]), int(want_quarter[-1])
            events = [e for e in events if e["year"] == yr and e["quarter"] == q]
            if not events:
                log(f"  - earningscall: no published event for {want_quarter}")
                return None
        ev = events[0]
        t = s.get(f"{EC_BASE}/transcript",
                  params={"apikey": key, "exchange": exchange,
                          "symbol": ticker.upper(), "year": ev["year"],
                          "quarter": ev["quarter"], "level": 1}, timeout=30)
        if t.status_code != 200:
            continue
        text = (t.json() or {}).get("text") or ""
        if len(text) < 500:
            continue
        date = (ev.get("conference_date") or "")[:10]
        return Result(text, FULL_TRANSCRIPT,
                      f"EarningsCall API ({exchange}:{ticker.upper()})",
                      f"{EC_BASE}/transcript?exchange={exchange}"
                      f"&symbol={ticker.upper()}&year={ev['year']}&quarter={ev['quarter']}",
                      date, f"FY{ev['year']} Q{ev['quarter']}",
                      period_code=f"{ev['year']}Q{ev['quarter']}",
                      period_source="EarningsCall event year/quarter",
                      notes=("Retrieved with the public 'demo' key (AAPL and MSFT only). "
                             "Set EARNINGSCALL_API_KEY for full coverage."
                             if key == "demo" else ""))
    if key == "demo":
        _ec_demo_spent[0] = True          # do not re-probe the demo key per ticker
        log(f"  - earningscall: {ticker.upper()} not in the free demo universe "
            f"(demo key covers AAPL and MSFT only); skipping this source for the "
            f"rest of the run")
    else:
        log(f"  - earningscall: {ticker.upper()} not available on this API key")
    return None


# --------------------------------------------------------------- alphavantage

def candidate_quarters(n=6):
    """Recent calendar quarters, newest first, as 'YYYYQn'."""
    today = dt.date.today()
    y, q = today.year, (today.month - 1) // 3 + 1
    out = []
    for _ in range(n):
        out.append(f"{y}Q{q}")
        q -= 1
        if q == 0:
            q, y = 4, y - 1
    return out


_av_key_warned = [False]


def av_key():
    raw = os.environ.get("ALPHAVANTAGE_API_KEY") or os.environ.get("ALPHA_VANTAGE_API_KEY")
    k = clean_key(raw)
    if k is None and _key_looks_set_but_isnt(raw) and not _av_key_warned[0]:
        _av_key_warned[0] = True
        log("  - alphavantage: ALPHAVANTAGE_API_KEY is a placeholder or too short "
            "-> treated as UNSET")
    return k


# Alpha Vantage's free tier is 25 requests/day and roughly 5/minute; this script
# walks up to 6 quarters per ticker, so pace the calls rather than burst them.
AV_RPS = 0.8
_av_last = [0.0]


def _av_throttle():
    """Space Alpha Vantage requests at most AV_RPS per second (process-wide)."""
    if AV_RPS <= 0:
        return
    gap = 1.0 / AV_RPS
    delta = time.monotonic() - _av_last[0]
    if delta < gap:
        time.sleep(gap - delta)
    _av_last[0] = time.monotonic()


def fetch_alphavantage(ticker, want_quarter=None):
    key = av_key()
    if not key:
        log("  - alphavantage: SKIPPED, no API key set (export ALPHAVANTAGE_API_KEY; "
            "free key, no card, at https://www.alphavantage.co/support/#api-key)")
        return None
    s = session("ClaudeSpace research")
    quarters = [want_quarter] if want_quarter else candidate_quarters()
    for quarter in quarters:
        try:
            _av_throttle()
            r = s.get("https://www.alphavantage.co/query",
                      params={"function": "EARNINGS_CALL_TRANSCRIPT",
                              "symbol": ticker.upper(), "quarter": quarter,
                              "apikey": key}, timeout=30)
            data = r.json()
        except Exception as e:
            log(f"  ! alphavantage: {e}")
            return None
        if "Information" in data or "Note" in data:
            log(f"  - alphavantage: {data.get('Information') or data.get('Note')}")
            return None
        turns = data.get("transcript") or []
        if not turns:
            continue
        lines = []
        for t in turns:
            who = t.get("speaker", "").strip()
            title = t.get("title", "").strip()
            head = f"**{who}**" + (f" — *{title}*" if title else "")
            lines.append(f"{head}\n\n{t.get('content','').strip()}")
        text = "\n\n".join(lines)
        return Result(text, FULL_TRANSCRIPT,
                      f"Alpha Vantage EARNINGS_CALL_TRANSCRIPT ({ticker.upper()})",
                      "https://www.alphavantage.co/documentation/#transcript",
                      "", quarter,
                      notes="Speaker-tagged turns as returned by Alpha Vantage.",
                      period_code=quarter,
                      period_source="Alpha Vantage `quarter` field for this call")
    log(f"  - alphavantage: no transcript for {ticker.upper()} in "
        f"{quarters[0]}..{quarters[-1]}")
    return None


# ------------------------------------------------------------------ orchestration

SOURCES = {
    "earningscall": fetch_earningscall,
    "alphavantage": fetch_alphavantage,
    "sec": fetch_sec,
}
DEFAULT_ORDER = ["earningscall", "alphavantage", "sec"]


def write_output(ticker, res, force=False):
    """Write transcript_<period>_<date>.md.

    The file is named after the fiscal period the CALL ITSELF covers, not after
    the day we happened to fetch it: an Alpha Vantage response for a stale
    quarter used to land as transcript_<today>.md and read as current. The
    period comes from the API response when it gives one, otherwise from the
    document's own header text, and the date component falls back to the
    8-K/6-K filing date (or, failing that, the retrieval date).
    """
    dated = bool(res.event_date)
    date = res.event_date or dt.date.today().isoformat()
    period, label, how = res.resolve_period()
    outdir = OUT_ROOT / ticker.upper()
    outdir.mkdir(parents=True, exist_ok=True)
    stem = f"transcript_{period}_{date}" if period else f"transcript_{date}"
    path = outdir / f"{stem}.md"
    if path.exists() and not force:
        log(f"  = {path} already exists (use --force to overwrite)")
        return path
    title_period = label or period or "period not stated"
    header = [
        f"# {ticker.upper()} earnings call material — {title_period}",
        "",
        f"- **call_period:** **{period or 'UNKNOWN'}**"
        + (f" ({label})" if label and label != period else "")
        + f" — {how}",
        f"- **content_type:** `{res.content_type}` — {CONTENT_LABEL[res.content_type]}",
        f"- **source:** {res.source}",
        f"- **source_url:** {res.source_url}",
        f"- **event_date:** {date}"
        + ("" if dated else "  (NOT a real event date: the source gave none, so this is the "
                            "retrieval date — judge recency by call_period above)"),
    ]
    if res.fiscal_label:
        header.append(f"- **fiscal_period:** {res.fiscal_label}")
    header += [
        f"- **retrieved_utc:** {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}",
        f"- **retrieved_by:** research/deepvalue/fetch_transcript.py",
    ]
    if res.notes:
        header += ["", "> " + res.notes.replace("\n", "\n> ")]
    header += ["", "---", "", ""]
    path.write_text("\n".join(header) + res.text + "\n")
    return path


def main(argv=None):
    global AV_RPS
    p = argparse.ArgumentParser(
        description="Fetch an earnings call transcript or closest substitute.")
    p.add_argument("ticker", nargs="?", help="US ticker, e.g. CULP")
    p.add_argument("--quarter", help="Target quarter, e.g. 2026Q2 (default: most recent)")
    p.add_argument("--source", default="auto",
                   choices=["auto"] + list(SOURCES),
                   help="Force a single source (default: try all in order)")
    p.add_argument("--force", action="store_true", help="Overwrite an existing file")
    p.add_argument("--av-rps", type=float, default=AV_RPS, metavar="RPS",
                   help=f"Alpha Vantage request rate, requests/second "
                        f"(default {AV_RPS}; 0 disables throttling)")
    p.add_argument("--list-sources", action="store_true",
                   help="Show source chain and key status, then exit")
    args = p.parse_args(argv)

    if args.list_sources:
        print("Source chain (in order):")
        for name in DEFAULT_ORDER:
            if name == "earningscall":
                status = ("key set" if ec_key()
                          else "NO usable key -> demo mode, tried once per run (AAPL/MSFT only)")
            elif name == "alphavantage":
                status = (f"key set (throttled to {AV_RPS} req/s)" if av_key()
                          else "NO key -> skipped entirely (free key: 20 seconds)")
            else:
                status = "no key needed (always available)"
            print(f"  {name:<14} {status}")
        return 0

    if not args.ticker:
        p.error("TICKER is required (or use --list-sources)")
    if args.quarter and not re.fullmatch(r"\d{4}Q[1-4]", args.quarter):
        p.error("--quarter must look like 2026Q2")

    ticker = args.ticker.upper()
    AV_RPS = max(0.0, args.av_rps)
    order = DEFAULT_ORDER if args.source == "auto" else [args.source]
    if "alphavantage" in order and not av_key():
        if args.source == "alphavantage":
            sys.stderr.write(
                "ERROR: --source alphavantage needs ALPHAVANTAGE_API_KEY. Get a free key "
                "(no card) at https://www.alphavantage.co/support/#api-key.\n")
            return 2
        # Do not burn an attempt on a source that cannot possibly answer.
        order = [n for n in order if n != "alphavantage"]
        log("  - alphavantage: SKIPPED, no ALPHAVANTAGE_API_KEY set "
            "(free key at https://www.alphavantage.co/support/#api-key)")
    log(f"Fetching earnings call material for {ticker} ...")
    for name in order:
        log(f"  > trying {name}")
        try:
            res = SOURCES[name](ticker, args.quarter)
        except Exception as e:
            log(f"  ! {name} failed: {type(e).__name__}: {e}")
            continue
        if res:
            path = write_output(ticker, res, force=args.force)
            log(f"  OK {name}: {CONTENT_LABEL[res.content_type]}")
            print(path)
            return 0

    sys.stderr.write(
        f"\nERROR: no earnings call material available for {ticker}.\n"
        f"Tried: {', '.join(order)}.\n"
        f"Next steps:\n"
        f"  * Confirm {ticker} is a US SEC filer with a recent 8-K Item 2.02\n"
        f"    (check https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={ticker}).\n"
        f"  * Get a free Alpha Vantage key (25 req/day, no card) at\n"
        f"    https://www.alphavantage.co/support/#api-key and\n"
        f"    export ALPHAVANTAGE_API_KEY=... for full transcripts.\n"
        f"  * See research/deepvalue/TRANSCRIPT_SOURCES.md for paid options.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())

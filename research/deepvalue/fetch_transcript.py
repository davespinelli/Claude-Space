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

import requests
from bs4 import BeautifulSoup

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
                 fiscal_label="", notes=""):
        self.text = text
        self.content_type = content_type
        self.source = source
        self.source_url = source_url
        self.event_date = event_date          # "YYYY-MM-DD"
        self.fiscal_label = fiscal_label      # e.g. "FY2026 Q2"
        self.notes = notes


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


def sec_exhibit_rows(cik, accession):
    """Return [(type, description, url)] for EX-99* docs in a filing."""
    acc_nodash = accession.replace("-", "")
    url = (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
           f"{acc_nodash}/{accession}-index.htm")
    r = sec_session().get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    rows = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 4:
            continue
        doc_type = tds[3].get_text(strip=True)
        if not doc_type.startswith("EX-99"):
            continue
        a = tds[2].find("a")
        if not a or not a.get("href"):
            continue
        href = a["href"]
        # iXBRL viewer links wrap the real document
        href = href.replace("/ix?doc=", "")
        rows.append((doc_type, tds[1].get_text(strip=True),
                     "https://www.sec.gov" + href))
    return url, rows


def fetch_sec(ticker, want_quarter=None):
    cik = ticker_to_cik(ticker)
    if not cik:
        log(f"  - SEC: no CIK found for {ticker} in SEC's ticker mapping")
        return None
    s = sec_session()
    r = s.get(f"https://data.sec.gov/submissions/CIK{cik}.json", timeout=30)
    r.raise_for_status()
    sub = r.json()
    recent = sub["filings"]["recent"]
    company = sub.get("name", ticker)

    candidates = []
    for i, form in enumerate(recent["form"]):
        if form != "8-K":
            continue
        if "2.02" not in (recent["items"][i] or ""):
            continue
        candidates.append((recent["filingDate"][i], recent["accessionNumber"][i]))
    if not candidates:
        log(f"  - SEC: no 8-K with Item 2.02 (Results of Operations) for {ticker}")
        return None

    for filing_date, accession in candidates[:1]:
        index_url, rows = sec_exhibit_rows(cik, accession)
        if not rows:
            log(f"  - SEC: 8-K {filing_date} has no EX-99 exhibits")
            continue
        best = None
        for doc_type, desc, url in rows:
            try:
                body = s.get(url, timeout=30)
                body.raise_for_status()
            except Exception as e:
                log(f"  ! SEC: could not fetch {url}: {e}")
                continue
            text = html_to_text(body.text)
            if len(text) < 200:
                continue
            ctype = classify_exhibit(desc, url.rsplit("/", 1)[-1], text)
            cand = (RANK[ctype], -len(text), ctype, doc_type, desc, url, text)
            if best is None or cand[:2] < best[:2]:
                best = cand
            time.sleep(0.15)
        if best is None:
            continue
        _, _, ctype, doc_type, desc, url, text = best
        notes = (f"Selected {doc_type} from the 8-K filed {filing_date}. "
                 f"Filing index: {index_url}")
        if ctype in (PRESS_RELEASE, PRESENTATION):
            notes += ("\n> NOTE: this company did not file prepared remarks or a "
                      "call transcript as an exhibit. This is the closest "
                      "SEC-sourced substitute, not the call itself.")
        return Result(text, ctype, f"SEC EDGAR 8-K Item 2.02, {doc_type} ({company})",
                      url, filing_date, notes=notes)
    return None


# --------------------------------------------------------------- earningscall

EC_BASE = "https://v2.api.earningscall.biz"
EC_EXCHANGES = ["NASDAQ", "NYSE", "AMEX", "OTC"]


def fetch_earningscall(ticker, want_quarter=None):
    key = os.environ.get("EARNINGSCALL_API_KEY", "demo")
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
                      notes=("Retrieved with the public 'demo' key (AAPL and MSFT only). "
                             "Set EARNINGSCALL_API_KEY for full coverage."
                             if key == "demo" else ""))
    if key == "demo":
        log(f"  - earningscall: {ticker.upper()} not in the free demo universe "
            f"(demo key covers AAPL and MSFT only)")
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


def fetch_alphavantage(ticker, want_quarter=None):
    key = os.environ.get("ALPHAVANTAGE_API_KEY") or os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not key:
        log("  - alphavantage: skipped (set ALPHAVANTAGE_API_KEY; free key at "
            "https://www.alphavantage.co/support/#api-key)")
        return None
    s = session("ClaudeSpace research")
    quarters = [want_quarter] if want_quarter else candidate_quarters()
    for quarter in quarters:
        try:
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
                      notes="Speaker-tagged turns as returned by Alpha Vantage.")
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
    date = res.event_date or dt.date.today().isoformat()
    outdir = OUT_ROOT / ticker.upper()
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / f"transcript_{date}.md"
    if path.exists() and not force:
        log(f"  = {path} already exists (use --force to overwrite)")
        return path
    header = [
        f"# {ticker.upper()} earnings call material — {date}",
        "",
        f"- **content_type:** `{res.content_type}` — {CONTENT_LABEL[res.content_type]}",
        f"- **source:** {res.source}",
        f"- **source_url:** {res.source_url}",
        f"- **event_date:** {date}",
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
    p = argparse.ArgumentParser(
        description="Fetch an earnings call transcript or closest substitute.")
    p.add_argument("ticker", nargs="?", help="US ticker, e.g. CULP")
    p.add_argument("--quarter", help="Target quarter, e.g. 2026Q2 (default: most recent)")
    p.add_argument("--source", default="auto",
                   choices=["auto"] + list(SOURCES),
                   help="Force a single source (default: try all in order)")
    p.add_argument("--force", action="store_true", help="Overwrite an existing file")
    p.add_argument("--list-sources", action="store_true",
                   help="Show source chain and key status, then exit")
    args = p.parse_args(argv)

    if args.list_sources:
        print("Source chain (in order):")
        for name in DEFAULT_ORDER:
            if name == "earningscall":
                k = os.environ.get("EARNINGSCALL_API_KEY")
                status = "key set" if k else "NO key -> demo mode (AAPL/MSFT only)"
            elif name == "alphavantage":
                k = os.environ.get("ALPHAVANTAGE_API_KEY") or \
                    os.environ.get("ALPHA_VANTAGE_API_KEY")
                status = "key set" if k else "NO key -> skipped (free key: 20 seconds)"
            else:
                status = "no key needed (always available)"
            print(f"  {name:<14} {status}")
        return 0

    if not args.ticker:
        p.error("TICKER is required (or use --list-sources)")
    if args.quarter and not re.fullmatch(r"\d{4}Q[1-4]", args.quarter):
        p.error("--quarter must look like 2026Q2")

    ticker = args.ticker.upper()
    order = DEFAULT_ORDER if args.source == "auto" else [args.source]
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

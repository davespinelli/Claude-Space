#!/usr/bin/env python3
"""Build a compact triage pack for one or more tickers.

Usage:
    python research/deepvalue/triage_pack.py TICKER [TICKER ...]

Writes research/deepvalue/triage/packs/TICKER.md, a 25k-40k character context
assembled from the screen row, meta.json, form 4 summary, the latest earnings
press release, the annual-report MD&A and business section, and the transcript
file.

Foreign private issuers file a 20-F (Item 4 = Business, Item 5 = MD&A,
Item 3.D = Risk Factors) and a 6-K instead of a 10-K and an 8-K. The pack reads
meta.json's `form_type` and pulls the right sections, labelling them by the form
they actually came from. A 20-F Item 7 is Major Shareholders, NOT MD&A, and is
never treated as such.

Every source is optional. A missing document is reported inline and in the
"Document availability" section rather than raising, so a pack is always
written as long as the ticker is known to the screen or to filings/.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILINGS = HERE / "filings"
PACKS = HERE / "triage" / "packs"
CANDIDATES = HERE / "candidates.csv"
UNIVERSE = HERE / "universe_under2b.csv"

# character budgets per section
BUDGET_EX99 = 12_000
BUDGET_MDNA = 10_000
BUDGET_ITEM1 = 6_000
BUDGET_TRANSCRIPT = 3_000
BUDGET_FORM4 = 2_500
HEADLINE_MONTHS = 6

# ---------------------------------------------------------------- formatting


def _isnan(v) -> bool:
    return isinstance(v, float) and math.isnan(v)


def money(v, dp: int = 1) -> str:
    if v is None or v == "" or _isnan(v):
        return "n/a"
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    sign = "-" if v < 0 else ""
    a = abs(v)
    if a >= 1e9:
        return f"{sign}${a/1e9:,.{dp}f}B"
    if a >= 1e6:
        return f"{sign}${a/1e6:,.{dp}f}M"
    if a >= 1e3:
        return f"{sign}${a/1e3:,.0f}k"
    return f"{sign}${a:,.2f}"


def pct(v, dp: int = 1) -> str:
    if v is None or v == "" or _isnan(v):
        return "n/a"
    try:
        return f"{float(v)*100:,.{dp}f}%"
    except (TypeError, ValueError):
        return str(v)


def mult(v, dp: int = 1) -> str:
    if v is None or v == "" or _isnan(v):
        return "n/a"
    try:
        return f"{float(v):,.{dp}f}x"
    except (TypeError, ValueError):
        return str(v)


def num(v, dp: int = 2) -> str:
    if v is None or v == "" or _isnan(v):
        return "n/a"
    try:
        return f"{float(v):,.{dp}f}"
    except (TypeError, ValueError):
        return str(v)


def ints(v) -> str:
    if v is None or v == "" or _isnan(v):
        return "n/a"
    try:
        return f"{float(v):,.0f}"
    except (TypeError, ValueError):
        return str(v)


def clip(text: str, limit: int) -> tuple[str, bool]:
    """Trim to limit chars on a paragraph/sentence boundary."""
    text = re.sub(r"\n{3,}", "\n\n", (text or "").strip())
    if len(text) <= limit:
        return text, False
    cut = text[:limit]
    for sep in ("\n\n", "\n", ". "):
        i = cut.rfind(sep)
        if i > limit * 0.6:
            cut = cut[: i + (1 if sep == ". " else 0)]
            break
    return cut.rstrip() + f"\n\n_[...truncated at ~{limit:,} chars of this document]_", True


# ---------------------------------------------------------------- doc parsing

TOC_ROW = re.compile(
    r"^\s*(?:item\s+\d+[a-c]?\.?\s*)?[A-Za-z][A-Za-z0-9'’,&()./\- ]{2,80}?[.\s|·—–]*\s\d{1,3}\s*$",
    re.I,
)
NOISE = re.compile(
    r"^\s*(table of contents|index|part\s+[ivx]+|page\s*\d*|\d{1,3}|-+|_+)\s*$", re.I
)


def strip_fetch_header(text: str) -> str:
    """Drop the '# TICKER 10-K ... / Source: url' preamble our fetcher writes."""
    lines = text.split("\n")
    out = []
    for i, ln in enumerate(lines):
        if i < 8 and (ln.startswith("# ") or ln.startswith("Source: ") or ln.startswith("> ")):
            continue
        out.append(ln)
    return "\n".join(out).strip()


def strip_toc(text: str) -> str:
    """Remove a leading table-of-contents block if the filing carried one."""
    lines = text.split("\n")
    window = min(len(lines), 200)
    run_start = run_end = None
    i = 0
    while i < window:
        if TOC_ROW.match(lines[i] or ""):
            j = i
            hits = 0
            while j < window:
                ln = (lines[j] or "").strip()
                if not ln or NOISE.match(ln):
                    j += 1
                    continue
                if TOC_ROW.match(ln) and len(ln) < 120:
                    hits += 1
                    j += 1
                    continue
                break
            if hits >= 5:
                run_start, run_end = i, j
                break
            i = j + 1
        else:
            i += 1
    if run_start is not None:
        lines = lines[run_end:]
    # drop stray page-artifact lines anywhere
    lines = [ln for ln in lines if not NOISE.match(ln or "") or ln.strip() == ""]
    return "\n".join(lines).strip()


OVERVIEW_ANCHORS = (
    "business overview",
    "company overview",
    "executive overview",
    "executive summary",
    "overview of our business",
    "overview",
    "current business update",
    "our business",
    "introduction",
)
RESULTS_ANCHORS = (
    "results of operations",
    "consolidated results of operations",
    "results of operation",
    "comparison of",
)


def find_heading(text: str, anchors: tuple[str, ...], start: int = 0) -> int:
    """Char offset of the first standalone heading line matching an anchor."""
    best = -1
    pos = 0
    for line in text.split("\n"):
        line_start = pos
        pos += len(line) + 1
        if line_start < start:
            continue
        s = line.strip().strip("*#").strip().rstrip(":.").strip()
        if not s or len(s) > 80:
            continue
        low = s.lower()
        for a in anchors:
            if low == a or low.startswith(a + " ") or low.startswith(a + ","):
                return line_start
            if a in low and len(low) <= len(a) + 24 and low.startswith(("the ", a[:4])):
                if best < 0:
                    best = line_start
    return best


def extract_mdna(text: str, budget: int = BUDGET_MDNA) -> tuple[str, str]:
    """Return (excerpt, how) for the Overview / Results of Operations portion."""
    body = strip_toc(strip_fetch_header(text))
    ov = find_heading(body, OVERVIEW_ANCHORS)
    res = find_heading(body, RESULTS_ANCHORS, start=max(ov, 0) + 1)
    if ov < 0 and res < 0:
        out, _ = clip(body, budget)
        return out, "no Overview/Results heading found; took the start of Item 7"
    if ov < 0:
        out, _ = clip(body[res:], budget)
        return out, "started at 'Results of Operations'"
    if res < 0 or res - ov <= budget:
        out, _ = clip(body[ov:], budget)
        how = "started at the Overview heading"
        if 0 <= res <= ov + budget:
            how += "; window reaches 'Results of Operations'"
        return out, how
    # Overview and Results are far apart: split the budget across both.
    a, _ = clip(body[ov:], int(budget * 0.6))
    b, _ = clip(body[res:], budget - int(budget * 0.6))
    return (
        a + "\n\n... [gap in Item 7 skipped] ...\n\n" + b,
        "split excerpt: Overview block + Results of Operations block",
    )


def newest(pattern: str, d: Path) -> Path | None:
    hits = sorted(glob.glob(str(d / pattern)))
    if not hits:
        return None
    dated = []
    for h in hits:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(h))
        dated.append((m.group(1) if m else "0000-00-00", h))
    dated.sort()
    return Path(dated[-1][1])


def read(p: Path | None) -> str:
    if not p or not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


# 8-Ks carry the release in EX-99; foreign private issuers use EX-1/EX-2 on a
# 6-K, or put the release straight into the 6-K body with no exhibit at all.
EXHIBIT_HEAD = re.compile(r"\s*EX-?(?:99|1|2)\b", re.I)


def extract_ex99(text: str, filename: str = "") -> str:
    """Concatenate the exhibit sections of an 8-K / 6-K markdown file.

    For a 6-K with no separate exhibit the main document IS the release, so it
    is used rather than reporting the filing as having no press release.
    """
    parts = re.split(r"^## ", text, flags=re.M)
    keep = []
    for part in parts:
        head = part.split("\n", 1)[0]
        if EXHIBIT_HEAD.match(head):
            keep.append("## " + part.strip())
    if keep:
        return "\n\n".join(keep)
    if filename.startswith("6-K"):
        for part in parts:
            head = part.split("\n", 1)[0]
            if re.match(r"\s*main document", head, re.I) and len(part) > 800:
                return "## " + part.strip()
    return ""


ITEM_HEAD = re.compile(r"^\s*item\s+(\d+\.\d+)\s*[.|:\-]?\s*(.*)$", re.I)
WATCH_ITEMS = {"1.01", "1.02", "5.02"}
ITEM_LABEL = {
    "1.01": "entry into a material definitive agreement",
    "1.02": "termination of a material definitive agreement",
    "5.02": "officer / director change or comp arrangement",
}
# do not end a "sentence" on these
ABBREV = re.compile(
    r"(?:\b(?:inc|corp|co|ltd|llc|l\.l\.c|plc|no|nos|mr|mrs|ms|dr|jr|sr|st|approx|est|"
    r"u\.s|u\.k|e\.g|i\.e|vs|etc|fig|al)\.|\b[A-Z]\.)\s*$",
    re.I,
)


def first_sentence(body: str, min_len: int = 90, max_len: int = 260) -> str:
    """First sentence, joining across common abbreviations and short fragments."""
    body = re.sub(r"\s+", " ", body or "").strip()
    if not body:
        return ""
    pieces = re.split(r"(?<=[.!?])\s+", body)
    out = ""
    for piece in pieces:
        out = (out + " " + piece).strip() if out else piece
        if len(out) >= min_len and not ABBREV.search(out):
            break
        if len(out) >= max_len:
            break
    if len(out) > max_len:
        cut = out[:max_len]
        i = cut.rfind(" ")
        out = (cut[:i] if i > max_len * 0.6 else cut).rstrip(" ,;") + "..."
    return out


def item_headline(path: Path, want: set[str]) -> list[str]:
    """One-line summaries of the watched 8-K items inside a filing."""
    text = read(path)
    if not text:
        return []
    lines = text.split("\n")
    out = []
    seen = set()
    for i, ln in enumerate(lines):
        m = ITEM_HEAD.match(ln)
        if not m or m.group(1) not in want or m.group(1) in seen:
            continue
        code = m.group(1)
        seen.add(code)
        title = re.sub(r"\s+", " ", m.group(2)).strip(" .|")
        # SEC item captions are long boilerplate; prefer our short label
        label = ITEM_LABEL.get(code, title.lower())
        if title and len(title) <= 70:
            label = title
        body = ""
        for nxt in lines[i + 1 : i + 14]:
            s = nxt.strip()
            if len(s) > 60 and not ITEM_HEAD.match(s):
                body = s
                break
        sent = first_sentence(body)
        out.append(f"Item {code} ({label}): {sent}".rstrip(": ").strip())
    return out


# ---------------------------------------------------------------- data inputs


def load_screen_row(ticker: str) -> tuple[dict, str]:
    src = CANDIDATES if CANDIDATES.exists() else None
    if src is None:
        return {}, "candidates.csv not found"
    try:
        import pandas as pd
    except ImportError:
        return {}, "pandas not available"
    df = pd.read_csv(src)
    hit = df[df.get("ticker", "").astype(str).str.upper() == ticker]
    if hit.empty and UNIVERSE.exists():
        u = pd.read_csv(UNIVERSE)
        uh = u[u.get("ticker", "").astype(str).str.upper() == ticker]
        if not uh.empty:
            return uh.iloc[0].to_dict(), "universe_under2b.csv (not a screen candidate)"
    if hit.empty:
        return {}, f"{src.name} has no row for {ticker}"
    return hit.iloc[0].to_dict(), src.name


def price_range(ticker: str) -> tuple[str, str]:
    """1y price range from yfinance. Silently skipped when unavailable."""
    if os.environ.get("TRIAGE_NO_PRICE"):
        return "", "skipped (TRIAGE_NO_PRICE set)"
    try:
        import logging
        import warnings

        warnings.filterwarnings("ignore")
        logging.getLogger("yfinance").setLevel(logging.CRITICAL)
        import yfinance as yf

        h = yf.Ticker(ticker).history(period="1y", auto_adjust=False)
        if h is None or h.empty or "Close" not in h:
            return "", "no yfinance data"
        close = h["Close"].dropna()
        if close.empty:
            return "", "no yfinance closes"
        last, hi, lo = float(close.iloc[-1]), float(close.max()), float(close.min())
        off_hi = (last / hi - 1) if hi else float("nan")
        up_lo = (last / lo - 1) if lo else float("nan")
        asof = close.index[-1].strftime("%Y-%m-%d")
        return (
            f"Last {num(last)} (as of {asof}) · 52w range {num(lo)} - {num(hi)} · "
            f"{pct(off_hi)} vs 52w high · {pct(up_lo)} above 52w low",
            "yfinance",
        )
    except Exception as exc:  # network, rate limit, delisted, missing package
        return "", f"yfinance unavailable ({type(exc).__name__})"


# ---------------------------------------------------------------- pack render

SCREEN_GROUPS = [
    (
        "Valuation",
        [
            ("price", num), ("mktcap", money), ("ev", money), ("ev_ebit", mult),
            ("fcf", money), ("fcf_yield", pct),
        ],
    ),
    (
        "Quality and balance sheet",
        [
            ("roic", pct), ("net_debt", money), ("net_debt_ebit", mult),
            ("cash", money), ("ltd", money), ("equity", money), ("ltd_tag", str),
        ],
    ),
    (
        "Growth and operations",
        [
            ("revenue", money), ("revenue_prior", money), ("rev_growth", pct),
            ("rev_growth_note", str),
            ("ebit", money), ("net_income", money), ("cfo", money), ("capex", money),
        ],
    ),
    (
        "Capital allocation",
        [("share_chg", pct), ("share_chg_src", str), ("shares", ints), ("shares_py", ints)],
    ),
    (
        "Price behaviour and liquidity",
        [("mom_12_1", pct), ("r6m", pct), ("off_52w_high", pct), ("adv20", money)],
    ),
    (
        "Screen ranks (0-1, higher is better)",
        [
            ("r_fcf_yield", num), ("r_ev_ebit", num), ("r_roic", num),
            ("r_rev_growth", num), ("r_buyback", num), ("score", num),
        ],
    ),
    (
        "Data provenance and flags",
        [
            ("revenue_period", str), ("ebit_period", str), ("equity_period", str),
            ("shares_period", str), ("shares_py_period", str),
            ("capex_missing", str), ("ltd_missing", str),
        ],
    ),
]


def render_screen(row: dict, source: str) -> str:
    if not row:
        return f"_No screen row: {source}._\n"
    used = set()
    out = [f"_Source: {source}_\n"]
    ident = [
        f"- **Name:** {row.get('name', 'n/a')}",
        f"- **CIK:** {ints(row.get('cik'))} · **SIC:** {row.get('sic', 'n/a')} "
        f"({row.get('sic_desc', 'n/a')}) · **Exchange:** {row.get('exchange', 'n/a')}",
    ]
    used.update({"name", "cik", "sic", "sic_desc", "exchange", "ticker"})
    out.append("\n".join(ident) + "\n")
    for title, fields in SCREEN_GROUPS:
        lines = []
        for key, fmt in fields:
            if key not in row:
                continue
            used.add(key)
            v = row.get(key)
            lines.append(f"| {key} | {'n/a' if _isnan(v) else fmt(v)} |")
        if lines:
            out.append(f"**{title}**\n\n| metric | value |\n|---|---|\n" + "\n".join(lines) + "\n")
    extra = [k for k in row if k not in used and k != "why"]
    if extra:
        rows = "\n".join(f"| {k} | {row[k]} |" for k in extra)
        out.append(f"**Other screen columns**\n\n| metric | value |\n|---|---|\n{rows}\n")
    if row.get("why"):
        out.append(f"**Screen rationale:** {row['why']}\n")
    return "\n".join(out)


def share_trend(row: dict) -> str:
    """Share-count trend, using screen.py's own share_chg (which may come from a
    fallback tag) rather than recomputing it from two possibly-mixed columns."""
    sh, py = row.get("shares"), row.get("shares_py")
    chg = row.get("share_chg")
    src = str(row.get("share_chg_src") or "").strip()
    have_chg = not (chg in (None, "") or _isnan(chg))
    if not have_chg:
        return ("_No usable share count for the prior year (dei cover-page count absent and "
                "no fallback tag available); share trend not computed._")
    chg = float(chg)
    direction = "buyback / shrinking count" if chg < -0.005 else (
        "dilution / growing count" if chg > 0.005 else "roughly flat"
    )
    lines = []
    if not (sh in (None, "") or py in (None, "") or _isnan(sh) or _isnan(py)):
        lines.append(
            f"- Shares outstanding: **{ints(sh)}** ({row.get('shares_period', 'n/a')}) "
            f"vs **{ints(py)}** prior year ({row.get('shares_py_period', 'n/a')})"
        )
    lines.append(f"- Change: **{pct(chg)}** — {direction}")
    if src:
        lines.append(f"- Source concept: `{src}`")
    note = str(row.get("rev_growth_note") or "").strip()
    if note and note.lower() not in ("nan", "none"):
        lines.append(f"- **Flag:** {note}")
    return "\n".join(lines)


# --------------------------------------------------------------- FPI support

# role -> (10-K glob + label, 20-F glob + label)
ANNUAL_SECTIONS = {
    "mdna": {
        "10-K": ("10-K_*_item7_mdna.md", "10-K Item 7 MD&A"),
        "20-F": ("20-F_*_item5_operating_review.md",
                 "20-F Item 5 - Operating and Financial Review and Prospects (MD&A)"),
    },
    "business": {
        "10-K": ("10-K_*_item1_business.md", "10-K Item 1 - Business"),
        "20-F": ("20-F_*_item4_business.md", "20-F Item 4 - Information on the Company"),
    },
    "risks": {
        "10-K": ("10-K_*_item1a_risks.md", "10-K Item 1A - Risk Factors"),
        "20-F": ("20-F_*_item3d_risks.md", "20-F Item 3.D - Risk Factors"),
    },
}


def annual_form(meta: dict, d: Path) -> str:
    """Which annual report this issuer files: '20-F' (foreign private issuer) or '10-K'."""
    ft = str(meta.get("form_type") or "").upper()
    if ft.startswith("20-F"):
        return "20-F"
    if ft.startswith("10-K"):
        return "10-K"
    # meta.json predates the form_type field: fall back to what is on disk
    if list(d.glob("20-F_*.md")) and not list(d.glob("10-K_*.md")):
        return "20-F"
    return "10-K"


def section_doc(d: Path, form: str, role: str) -> tuple[Path | None, str]:
    pat, label = ANNUAL_SECTIONS[role][form]
    return newest(pat, d), label


PERIOD_RE = re.compile(r"(\d{4})(Q[1-4]|FY)")


def period_key(code: str) -> tuple[int, int]:
    """Sortable key for a '2026Q2' / '2025FY' period code. ('' -> lowest)."""
    m = PERIOD_RE.fullmatch(code or "")
    if not m:
        return (0, 0)
    q = 5 if m.group(2) == "FY" else int(m.group(2)[1])
    return (int(m.group(1)), q)


CT_RANK = {"full_transcript": 0, "prepared_remarks": 1,
           "press_release": 2, "investor_presentation": 3}


def transcript_candidates(d: Path) -> list[dict]:
    """Every transcript_*.md with its declared call period, date and content type."""
    out = []
    for fp in sorted(d.glob("transcript_*.md")):
        raw = read(fp)
        m = re.search(r"call_period:\*\*\s*\**([0-9]{4}(?:Q[1-4]|FY))\**", raw)
        code = m.group(1) if m else ""
        if not code:
            m = re.search(r"transcript_([0-9]{4}(?:Q[1-4]|FY))_", fp.name)
            code = m.group(1) if m else ""
        m = re.search(r"content_type:\*\*\s*`?([a-z_]+)`?", raw)
        ctype = m.group(1) if m else ""
        m = re.search(r"event_date:\*\*\s*(\d{4}-\d{2}-\d{2})", raw)
        date = m.group(1) if m else ""
        if not date:
            m = re.search(r"(\d{4}-\d{2}-\d{2})", fp.name)
            date = m.group(1) if m else ""
        out.append({"path": fp, "period": code, "date": date, "ctype": ctype, "raw": raw})
    # A real transcript is management's own voice and is worth more than another
    # copy of the press release already excerpted in section 7 - even one quarter
    # behind, which section 10 then flags. Among equals, newest call period wins.
    out.sort(key=lambda c: (-CT_RANK.get(c["ctype"], 9), period_key(c["period"]), c["date"]),
             reverse=True)
    return out


def release_period(path: Path | None) -> str:
    """Fiscal period of an 8-K/6-K earnings release, via fetch_transcript's parser."""
    if not path:
        return ""
    try:
        import fetch_transcript as _ft            # sibling module, same directory
    except Exception:                             # noqa: BLE001
        return ""
    try:
        return _ft.parse_period(strip_fetch_header(read(path)))[0]
    except Exception:                             # noqa: BLE001
        return ""


def build_pack(ticker: str) -> tuple[str, dict]:
    ticker = ticker.upper()
    d = FILINGS / ticker
    missing: list[str] = []
    found: list[str] = []
    now = datetime.now(timezone.utc)

    row, row_src = load_screen_row(ticker)
    name = str(row.get("name") or ticker)

    meta = {}
    meta_p = d / "meta.json"
    if meta_p.exists():
        try:
            meta = json.loads(read(meta_p))
            found.append("meta.json")
        except json.JSONDecodeError:
            missing.append("meta.json (unparseable)")
    else:
        missing.append("meta.json")
    if not name or name == ticker:
        name = str(meta.get("name") or ticker)

    parts: list[str] = []
    parts.append(f"# Triage pack — {ticker} · {name}")
    parts.append(
        f"_Generated {now.strftime('%Y-%m-%d %H:%M UTC')} by research/deepvalue/triage_pack.py. "
        "Excerpts only: every section is truncated. Do not infer anything the text does not say._"
    )

    # --- 1. identity -------------------------------------------------------
    form = annual_form(meta, d)
    fye = meta.get("fiscal_year_end") or ""
    fye_fmt = f"{fye[:2]}-{fye[2:]}" if len(fye) == 4 else (fye or "n/a")
    exch = ", ".join(meta.get("exchanges") or []) or str(row.get("exchange") or "n/a")
    parts.append(
        "## 1. Company identity\n\n"
        f"- **Ticker:** {ticker} · **Name:** {name}\n"
        f"- **CIK:** {meta.get('cik') or ints(row.get('cik'))}\n"
        f"- **SIC:** {meta.get('sic') or row.get('sic', 'n/a')} — "
        f"{meta.get('sic_description') or row.get('sic_desc', 'n/a')}\n"
        f"- **Fiscal year end (MM-DD):** {fye_fmt}\n"
        f"- **Exchange:** {exch}\n"
        + (f"- **Annual report form:** {form} — FOREIGN PRIVATE ISSUER. It files a 20-F "
           f"(Item 4 = business, Item 5 = MD&A, Item 3.D = risk factors) and 6-Ks instead "
           f"of a 10-K, 10-Q, 8-K and proxy. There is no quarterly 10-Q and no DEF 14A.\n"
           if form == "20-F" else "")
        + f"- **Filings fetched:** {meta_p.parent if meta else 'none'}"
    )
    if meta.get("problems"):
        parts.append(
            "**Fetcher warnings for this ticker:** "
            + "; ".join(str(p) for p in meta["problems"])
        )

    # --- 2. screen row -----------------------------------------------------
    parts.append("## 2. Screen row (all metrics)\n\n" + render_screen(row, row_src))

    # --- 3. share count + price -------------------------------------------
    parts.append("## 3. Share count trend\n\n" + share_trend(row))
    pr, pr_note = price_range(ticker)
    if pr:
        parts.append("## 4. Price range (1 year)\n\n- " + pr + "\n\n_Source: yfinance, live._")
    else:
        parts.append(f"## 4. Price range (1 year)\n\n_Not included: {pr_note}._")

    # --- 5. recent 8-K item headlines -------------------------------------
    cutoff = (now - timedelta(days=HEADLINE_MONTHS * 31)).strftime("%Y-%m-%d")
    headlines: list[str] = []
    eight_ks: list[tuple[str, Path, str]] = []
    for entry in (meta.get("filings_used", {}).get("8-K") or []):
        fp = d / str(entry.get("file") or "")
        eight_ks.append((str(entry.get("filingDate") or ""), fp, str(entry.get("items") or "")))
    if not eight_ks:
        for fp in sorted(glob.glob(str(d / "8-K_*.md"))):
            m = re.search(r"8-K_(\d{4}-\d{2}-\d{2})_(.+)\.md$", os.path.basename(fp))
            if m:
                eight_ks.append((m.group(1), Path(fp), m.group(2).replace("-", ".")))
    for date, fp, items in sorted(eight_ks, reverse=True):
        if date < cutoff or not fp.exists():
            continue
        want = {i for i in WATCH_ITEMS if i in items.replace("-", ".")} or WATCH_ITEMS
        for h in item_headline(fp, want):
            headlines.append(f"- **{date}** — {h}")
    six_ks = sorted(glob.glob(str(d / "6-K_*.md")), reverse=True)
    sec5 = "## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)\n\n"
    if headlines:
        sec5 += "\n".join(headlines)
    elif eight_ks:
        sec5 += (
            "_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director "
            f"change) 8-K filed since {cutoff} among the {len(eight_ks)} 8-Ks fetched._"
        )
    elif six_ks:
        # FPIs file 6-Ks, which carry no item codes at all
        titles = []
        for fp in six_ks[:12]:
            m = re.search(r"6-K_(\d{4}-\d{2}-\d{2})_(.+)\.md$", os.path.basename(fp))
            if m:
                titles.append(f"- **{m.group(1)}** — {m.group(2).replace('-', ' ')}")
        sec5 = ("## 5. Material 6-K events, last 6 months\n\n"
                "_This is a foreign private issuer: it files 6-Ks, which carry no 8-K item "
                "codes, so these are the filings by headline rather than by item._\n\n"
                + "\n".join(titles))
    else:
        sec5 += "_No 8-K filings fetched for this ticker._"
        missing.append("8-K filings")
    parts.append(sec5)

    # --- 6. form 4 ---------------------------------------------------------
    f4 = d / "form4_summary.md"
    if f4.exists():
        found.append("form4_summary.md")
        body, _ = clip(strip_fetch_header(read(f4)), BUDGET_FORM4)
        parts.append("## 6. Insider activity (Form 4, trailing 12 months)\n\n" + body)
    else:
        missing.append("form4_summary.md")
        parts.append(
            "## 6. Insider activity (Form 4, trailing 12 months)\n\n"
            "_Not available: form4_summary.md was not fetched. Treat insider activity as unknown, "
            "not as absent._"
        )

    # --- 7. earnings press release ----------------------------------------
    er = newest("8-K_*_2-02-results.md", d) or newest("6-K_*_results.md", d)
    ex99 = extract_ex99(read(er), er.name) if er else ""
    if not ex99:
        cands = sorted(glob.glob(str(d / "8-K_*.md")), reverse=True) + \
                sorted(glob.glob(str(d / "6-K_*.md")), reverse=True)
        for cand in cands:
            got = extract_ex99(read(Path(cand)), os.path.basename(cand))
            if got:
                er, ex99 = Path(cand), got
                break
    ex99_excerpt = ""
    er_date = ""
    if er:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", er.name)
        er_date = m.group(1) if m else ""
    if ex99:
        found.append(er.name)
        ex99_excerpt, _ = clip(ex99, BUDGET_EX99)
        src_form = "6-K" if er.name.startswith("6-K") else "8-K"
        parts.append(
            f"## 7. Latest earnings press release ({src_form} exhibit from {er.name})\n\n"
            + ("_This issuer reports on Form 6-K rather than 8-K._\n\n" if src_form == "6-K" else "")
            + ex99_excerpt
        )
    else:
        missing.append(("6-K" if form == "20-F" else "8-K") + " earnings press release exhibit")
        parts.append(
            f"## 7. Latest earnings press release\n\n"
            f"_Not available: no {'6-K' if form == '20-F' else '8-K'} with a readable release "
            "exhibit was fetched. Current-quarter results are unknown from this pack._"
        )

    # --- 8. MD&A -----------------------------------------------------------
    m7, mdna_label = section_doc(d, form, "mdna")
    if m7:
        found.append(m7.name)
        excerpt, how = extract_mdna(read(m7))
        parts.append(
            f"## 8. {mdna_label} — Overview / Results of Operations ({m7.name})\n\n"
            f"_Extraction: {how}._\n\n" + excerpt
        )
    else:
        q7 = newest("10-Q_*_mdna.md", d)
        if q7:
            found.append(q7.name + " (10-Q MD&A used in place of the 10-K)")
            excerpt, how = extract_mdna(read(q7))
            parts.append(
                f"## 8. MD&A — no 10-K Item 7 fetched, using 10-Q MD&A ({q7.name})\n\n"
                f"_Extraction: {how}._\n\n" + excerpt
            )
            missing.append("10-K Item 7 MD&A (substituted 10-Q MD&A)")
        else:
            missing.append(f"{mdna_label} (management commentary)")
            parts.append(
                f"## 8. {mdna_label}\n\n_Not available: no {mdna_label} "
                + ("" if form == "20-F" else "and no 10-Q MD&A ")
                + "was fetched. No management commentary in this pack._"
            )

    # --- 9. business -------------------------------------------------------
    m1, biz_label = section_doc(d, form, "business")
    if m1:
        found.append(m1.name)
        body, _ = clip(strip_toc(strip_fetch_header(read(m1))), BUDGET_ITEM1)
        parts.append(f"## 9. {biz_label} ({m1.name})\n\n" + body)
    else:
        missing.append(f"{biz_label} (business description)")
        parts.append(
            f"## 9. {biz_label}\n\n_Not available: the fetcher did not split out this section "
            "for this filing. Describe the business from the MD&A overview above instead, and say "
            "so in the note._"
        )

    # --- 10. transcript ----------------------------------------------------
    cands = transcript_candidates(d)
    tr = cands[0]["path"] if cands else None
    sec10 = "## 10. Earnings call material\n\n"
    if tr:
        chosen = cands[0]
        found.append(tr.name)
        raw = chosen["raw"]
        ctype = chosen["ctype"]
        src_url = ""
        m = re.search(r"source_url:\*\*\s*(\S+)", raw)
        if m:
            src_url = m.group(1)
        if "transcript" in ctype and "press" not in ctype:
            label = "REAL CALL TRANSCRIPT / PREPARED REMARKS — management's own words"
        elif ctype:
            label = (
                "EARNINGS PRESS RELEASE ONLY, not the call — no Q&A, no unscripted management "
                "commentary. Do not attribute call quotes to this."
            )
        else:
            label = "UNLABELLED — content type not stated in the file; treat provenance as unknown"
        body = raw.split("\n---\n", 1)[-1] if "\n---\n" in raw else raw
        body = strip_fetch_header(body)
        head_a = re.sub(r"\W+", " ", body[:400]).strip().lower()
        head_b = re.sub(r"\W+", " ", ex99_excerpt[-4000:]).strip().lower()
        dup = bool(head_a) and (head_a[:200] in head_b or head_a[:200] in re.sub(
            r"\W+", " ", ex99_excerpt[:4000]).strip().lower())
        tr_period = chosen["period"]
        rel_period = release_period(er)
        real_date = "NOT a real event date" not in raw[:1500]
        sec10 += (
            f"- **CALL PERIOD: {tr_period or 'UNKNOWN'}**"
            + (f" (call dated {chosen['date']})" if chosen["date"] and real_date
               else f" (no event date from the source; file dated {chosen['date']} when "
                    f"retrieved — judge recency by the call period)" if chosen["date"] else "")
            + "\n"
        )
        # Is this call older than the results already excerpted in section 7?
        stale = ""
        if er:
            if tr_period and rel_period and period_key(tr_period) < period_key(rel_period):
                stale = (f"STALE: this call covers {tr_period}, but the latest earnings "
                         f"release in this pack (section 7, {er.name}) covers {rel_period}. "
                         f"Everything said below predates those results — do not read it as "
                         f"commentary on the current quarter.")
            elif not tr_period and er_date and chosen["date"] and chosen["date"] < er_date:
                stale = (f"STALE: this file is dated {chosen['date']}, before the latest "
                         f"earnings release in this pack (section 7, {er.name}, {er_date}), "
                         f"and states no fiscal period. Treat it as out of date.")
            elif not tr_period:
                stale = ("Call period could not be determined from the file; judge its "
                         "recency from the source, not from the file name.")
        if stale:
            sec10 += f"- **Recency:** {stale}\n"
            missing.append(f"current-period call material ({stale.split(':')[0]})")
        elif tr_period:
            sec10 += ("- **Recency:** same fiscal period as the latest earnings release in "
                      "this pack.\n" if rel_period and period_key(tr_period) == period_key(rel_period)
                      else "- **Recency:** no earnings release to compare against.\n"
                      if not rel_period else
                      "- **Recency:** newer than the earnings release in section 7.\n")
        others = [c for c in cands[1:] if c["period"] or c["ctype"]]
        if others:
            sec10 += ("- **Other transcript files present (not shown):** "
                      + ", ".join(f"{c['path'].name} [{c['period'] or 'no period'}, "
                                  f"{c['ctype'] or 'unlabelled'}]" for c in others[:4])
                      + "\n")
        sec10 += f"- **File:** {tr.name}\n- **Type:** {label}\n"
        if src_url:
            sec10 += f"- **Source:** {src_url}\n"
        if dup and ex99_excerpt:
            sec10 += (
                "\n_Body not repeated: this file is the same press release already excerpted in "
                "section 7._"
            )
        else:
            excerpt, _ = clip(body, BUDGET_TRANSCRIPT)
            sec10 += "\n" + excerpt
    else:
        missing.append("transcript / prepared remarks")
        sec10 += (
            "_Not available: no transcript or prepared-remarks file was fetched. There is no "
            "management voice in this pack beyond the press release and MD&A._"
        )
    parts.append(sec10)

    # --- 11. availability --------------------------------------------------
    avail = "## 11. Document availability\n\n"
    # Say explicitly which document filled each role, so a 20-F Item 7 can never
    # be mistaken for MD&A and a missing role is never reported as present.
    roles = []
    for role, human in (("business", "Business description"),
                        ("mdna", "MD&A / management commentary"),
                        ("risks", "Risk factors")):
        doc, lbl = section_doc(d, form, role)
        roles.append(f"| {human} | {lbl} | {doc.name if doc else '**MISSING**'} |")
    avail += (f"**Annual report form:** {form}"
              + (" (foreign private issuer)" if form == "20-F" else "")
              + "\n\n| role | source item | file |\n|---|---|---|\n"
              + "\n".join(roles) + "\n\n")
    avail += "**Present:** " + (", ".join(found) if found else "none") + "\n\n"
    avail += "**Missing:** " + (", ".join(missing) if missing else "none") + "\n\n"
    avail += (
        "_Anything not listed as present is absent from this pack. Score conservatively and say "
        "what you could not check rather than guessing._"
    )
    parts.append(avail)

    text = "\n\n".join(parts).strip() + "\n"
    stats = {
        "ticker": ticker,
        "chars": len(text),
        "est_tokens": round(len(text) / 4),
        "missing": missing,
        "found": found,
        "has_screen_row": bool(row),
    }
    return text, stats


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Build compact triage packs.")
    ap.add_argument("tickers", nargs="+", help="one or more tickers")
    ap.add_argument("--out-dir", default=str(PACKS), help="output directory")
    ap.add_argument("--no-price", action="store_true", help="skip the yfinance lookup")
    args = ap.parse_args(argv)
    if args.no_price:
        os.environ["TRIAGE_NO_PRICE"] = "1"
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rc = 0
    for t in args.tickers:
        t = t.strip().upper()
        if not t:
            continue
        text, stats = build_pack(t)
        if not stats["found"] and not stats["has_screen_row"]:
            print(f"{t}: no screen row and no fetched documents; nothing to pack", file=sys.stderr)
            rc = 1
            continue
        p = out_dir / f"{t}.md"
        p.write_text(text, encoding="utf-8")
        miss = f" · missing: {', '.join(stats['missing'])}" if stats["missing"] else ""
        print(f"{t}: {stats['chars']:,} chars (~{stats['est_tokens']:,} tokens) -> {p}{miss}")
        if stats["chars"] < 8_000:
            print(
                f"  warning: {t} pack is thin ({stats['chars']:,} chars). Run "
                f"fetch_filings.py {t} (and fetch_transcript.py {t}) before triaging it.",
                file=sys.stderr,
            )
            rc = max(rc, 2)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

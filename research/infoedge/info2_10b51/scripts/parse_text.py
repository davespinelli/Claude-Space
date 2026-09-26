"""Text parser for Item 408(a) terminations in 10-Q/10-K documents that carry no ecd XBRL tags.
Validated first on tagged filings whose answer is known (PREREG D3).

Outputs: data/text_events_raw.csv.gz (all parsed statements; validation rows come from validate_text.py)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import lxml.html
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec
from build_events import (DATE, RX_BOILER, RX_COMPLETED, RX_EARLY, RX_EXPIRED_WEAK, RX_MODIFY, RX_BUY, RX_SALE,
                          norm_name, parse_date, sched_end_from_text, title_class)

BLOCK = {"p", "div", "tr", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section"}
RX_ZONE = re.compile(r"10b5\s*[-–‑]\s*1|trading\s+arrangement", re.I)
NOT_PERSON = re.compile(r"\b(?:agreement|plan|combination|program|board|company|registration|transaction|amendment|"
                        r"certification|merger|rights?|statement|arrangement|trust|fund|partners?|holdings?|inc|corp|llc|"
                        r"l\.?p|sponsor|notes?|credit|facility|lease|offering|rule|section|item|act|exchange|securities|"
                        r"shares?|stock|option|units?|warrants?|committee|policy|date|period|quarter|year|aggregate|number|"
                        r"total|name|title|type|action|adoption|termination|duration)\b", re.I)
RX_PLANWORD = re.compile(r"10b5|trading\s+(?:plan|arrangement)|(?:sales|selling|stock|share|trading)\s+plan|pre-?arranged"
                         r"|written\s+plan|the\s+plan\b", re.I)
RX_OTHER = re.compile(r"other\s+information", re.I)
RX_NEG = re.compile(r"\b(?:no|none\s+of|neither|nor|not\s+any)\b[^.]{0,80}\b(?:directors?|officers?|persons?)\b"
                    r"|\bdid\s+not\b|\bhas\s+not\b|\bhave\s+not\b|\bno\s+(?:such\s+)?(?:rule\s+)?10b5|\bnot\s+applicable\b"
                    r"|\bthere\s+were\s+no\b", re.I)
NAME = r"(?:(?:Mr|Mrs|Ms|Dr)\.?\s+)?[A-Z][A-Za-z'’\-]+(?:\s+(?:[A-Z]\.|[A-Z][A-Za-z'’\-]+|de|van|von|da|del|la)){1,4}(?:,?\s+(?:Jr|Sr|II|III|IV)\.?)?"
TITLE_LEAD = r"(?:the\s+Company.s\s+|our\s+|its\s+|a\s+|an\s+|the\s+|then\s+|who\s+(?:serves|served|is|was)\s+as\s+(?:our\s+|a\s+|an\s+|the\s+)?|member\s+of\s+our\s+)?"
RX_A = re.compile(rf"(?P<name>{NAME}),\s+{TITLE_LEAD}(?P<title>[^,;:]{{3,160}}?(?:,\s*[^,;:]{{3,80}}?){{0,3}}),?\s+"
                  rf"(?:(?:has|had|have)\s+)?(?:(?:entered\s+into|adopted)\s+and\s+(?:subsequently\s+)?)?terminat")
RX_B = re.compile(rf"(?:our|the\s+Company.s|its)\s+(?P<title>[^,;:]{{3,120}}?),\s+(?P<name>{NAME}),\s+"
                  rf"(?:(?:has|had)\s+)?terminat")
RX_TERM_ON = re.compile(rf"terminat\w*\s+(?:[^.]{{0,80}}?\s)?on\s+({DATE})|({DATE})\s*,\s*[^.]{{0,200}}?\bterminat", re.I)
RX_DATE = re.compile(DATE, re.I)
TITLE_WORDS = re.compile(r"officer|director|chair|president|counsel|secretary|treasurer|controller|vice|chief|"
                         r"founder|head|board|executive|ceo|cfo|coo|cto", re.I)


def html_lines(b: bytes) -> list[str]:
    try:
        doc = lxml.html.fromstring(b)
    except Exception:
        return []
    for bad in doc.xpath("//script|//style|//*[local-name()='header']|//*[local-name()='hidden']"):
        bad.getparent().remove(bad)
    out, buf = [], []

    def flush():
        s = re.sub(r"\s+", " ", "".join(buf)).strip()
        if s:
            out.append(s)
        buf.clear()

    for ev, el in lxml.etree.iterwalk(doc, events=("start", "end")):
        tag = el.tag if isinstance(el.tag, str) else ""
        tag = tag.split("}")[-1].lower()
        if ev == "start":
            if tag in BLOCK:
                if tag == "tr":
                    flush()
                elif tag not in ("td", "th"):
                    flush()
            if el.text:
                buf.append(el.text)
        else:
            if tag in ("td", "th"):
                buf.append(" | ")
            if tag in BLOCK:
                flush()
            if el.tail:
                buf.append(el.tail)
    flush()
    return [re.sub(r"(?:\s*\|\s*)+", " | ", ln).strip(" |") for ln in out]


def zone(lines: list[str]) -> list[int]:
    """Indices of lines in the Item 408 passage(s): lines near a 10b5-1 / trading-arrangement mention that
    follows an "Other Information" heading (Item 5 / Item 9B). Falls back to all mentions."""
    oth = [i for i, l in enumerate(lines) if RX_OTHER.search(l) and len(l) < 200]
    hits = [i for i, l in enumerate(lines) if RX_ZONE.search(l)]
    if oth:
        after = [h for h in hits if any(o <= h <= o + 150 for o in oth)]
        hits = after or hits
    keep = set()
    for h in hits:
        keep.update(range(max(0, h - 2), min(len(lines), h + 40)))
    return sorted(keep)


def sentences(line: str) -> list[str]:
    return [s for s in re.split(r"(?<=[a-z0-9\)])\.\s+(?=[A-Z(])", line) if s.strip()]


def extract(lines: list[str]) -> list[dict]:
    idx = zone(lines)
    txt_lines = [lines[i] for i in idx]
    zone_text = " ".join(txt_lines)
    out = []
    adopt_sents = []
    for l in txt_lines:
        for s in ([l] if " | " in l else sentences(l)):
            s2 = RX_BOILER.sub(" ", s)
            if (re.search(r"\badopt(?:ed|ion)\b|\bentered\s+into\b|\|\s*adopt", s2, re.I)
                    and not re.search(r"terminat|previously\s+adopted|(?:was|were|been|had)\s+adopted|adopted\s+(?:on|in|as\s+of)\s", s2, re.I)):
                adopt_sents.append(s2)
    for li, l in enumerate(txt_lines):
        is_row = " | " in l
        units = [l] if is_row else sentences(l)
        for u in units:
            u2 = RX_BOILER.sub(" ", u)
            if not re.search(r"terminat", u2, re.I):
                continue
            if RX_NEG.search(u2) and not re.search(r"except", u2, re.I):
                continue
            name = title = None
            if is_row:
                cells = [c.strip() for c in l.split(" | ") if c.strip()]
                if not any(re.search(r"^terminat|terminat(?:ed|ion)$", c, re.I) for c in cells) and \
                        not re.search(r"\|\s*terminat", l, re.I):
                    continue
                look = cells + [c.strip() for k in (1, 2) if li - k >= 0 and " | " in txt_lines[li - k]
                                for c in txt_lines[li - k].split(" | ") if c.strip()]
                for c in look:
                    m = re.match(rf"^({NAME})(?:\s*\(\d+\))?(?:,\s*(.+))?$", c)
                    if m and not TITLE_WORDS.search(m.group(1)) and not re.search(r"terminat|adopt|rule|plan", m.group(1), re.I):
                        name = m.group(1)
                        title = m.group(2) or ""
                        break
                if title is not None and not title:
                    title = " ".join(c for c in cells if TITLE_WORDS.search(c))[:200]
                ctx = l + " " + (txt_lines[li + 1] if li + 1 < len(txt_lines) else "")
            else:
                if not RX_PLANWORD.search(u2):
                    continue  # a "termination" of something other than a trading plan (employment terms etc.)
                m = RX_A.search(u2) or RX_B.search(u2)
                if m:
                    name, title = m.group("name"), m.group("title")
                else:
                    m = re.match(rf"^\s*({NAME})(?:,\s*[A-Z][\w.]*\.?){{0,3}},\s*(?P<title>[^\u2013\u2014:]{{3,140}}?)\s*[-\u2013\u2014:]\s", l)
                    if m and TITLE_WORDS.search(m.group("title")):
                        name, title = m.group(1), m.group("title")
                ctx = u2
            if name is None or NOT_PERSON.search(name):
                continue
            last = norm_name(name).split()
            if not last:
                continue
            last = last[-1]
            # person context: every zone sentence that mentions the last name
            pctx = " ".join(s for s in sentences(zone_text) if re.search(rf"\b{re.escape(last)}\b", s, re.I))
            pctx = RX_BOILER.sub(" ", pctx) or ctx
            dm = RX_TERM_ON.search(ctx)
            td = parse_date((dm.group(1) or dm.group(2))) if dm else pd.NaT
            if pd.isna(td):
                ds = [parse_date(x) for x in RX_DATE.findall(ctx)]
                ds = [d for d in ds if pd.notna(d)]
                td = ds[0] if ds else pd.NaT
            tc = title_class(title or "")
            adopt_same = any(re.search(rf"\b{re.escape(last)}\b", a_, re.I) for a_ in adopt_sents)
            out.append({"name": name, "last": last, "title": title, "term_date": td, "ctx": pctx[:3000],
                        "adopt_same_filing": adopt_same, **tc})
    # one per person
    seen, res = set(), []
    for r in out:
        if r["last"] in seen:
            continue
        seen.add(r["last"])
        res.append(r)
    return res


def classify(r) -> tuple[str, str]:
    c = r["ctx"] or ""
    td = r["term_date"]
    if r["adopt_same_filing"]:
        return "replacement", "same person adopted a plan in the same filing"
    if RX_MODIFY.search(c):
        return "replacement", "text: modified / replaced"
    if RX_COMPLETED.search(c):
        return "expired", "text: completed / ended by its terms"
    se = sched_end_from_text(c)
    if pd.notna(td) and pd.notna(se) and se > td + pd.Timedelta(days=3):
        return "early", "text: scheduled end after termination"
    if RX_EXPIRED_WEAK.search(c) and not RX_EARLY.search(c):
        return "expired", "text: expired"
    return "early", "default (no expiry / replacement cue)"


def parse_doc(url: str) -> list[dict]:
    b = sec.get(url, "docs", ".htm", offline=True, ok404=True)
    if not b:
        return None
    recs = extract(html_lines(b))
    for r in recs:
        r["trm_class"], r["trm_reason"] = classify(r)
        r["purchase_only"] = bool(RX_BUY.search(r["ctx"])) and not bool(RX_SALE.search(r["ctx"]))
    return recs


def run(groups=("valid_pos", "valid_neg", "untagged", "not_in_fsn")):
    dl = pd.read_csv(sec.CACHE / "doc_list.csv")
    dl = dl[dl.group.isin(groups)]
    rows, status = [], []
    for r in dl.itertuples():
        recs = parse_doc(r.url)
        status.append({"adsh": r.adsh, "group": r.group, "fetched": recs is not None,
                       "n_trm": len(recs or [])})
        for x in recs or []:
            rows.append({"adsh": r.adsh, "group": r.group, "file_date": r.file_date, "ciks": r.ciks, **x})
    return pd.DataFrame(rows), pd.DataFrame(status)


if __name__ == "__main__":
    ev, st = run()
    ev.to_csv(sec.ROOT / "data" / "text_events_raw.csv.gz", index=False)
    st.to_csv(sec.CACHE / "text_parse_status.csv", index=False)
    print(st.groupby("group").agg(n=("adsh", "size"), fetched=("fetched", "sum"), with_trm=("n_trm", lambda s: (s > 0).sum())))

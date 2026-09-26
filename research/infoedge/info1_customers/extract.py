"""
INFO-1 link extraction: (customer, % of revenue) from one 10-K document's text.

A mention counts only when all of these hold (fixed before any return was computed):
  1. the sentence (or table row) names a customer from aliases.py;
  2. the name is in a customer role:
       before it: "sales to", "revenue(s) from", "sales of our products to", "sold to",
                  "our largest customer," ...;  or
       after it:  "(Inc., its affiliates, parenthetical) accounted for / represented /
                  comprised / was our largest customer" ...;
     names joined by commas/"and" share the role of the chain;
  3. a percentage in the same sentence is a share of sales/revenue ("25% of our net
     sales", "25%, 22% and 20% of net sales"), not of receivables, purchases, a segment
     or a division, and is not preceded by "less than / below / under";
  4. the percentage for the most recent year is >= 10% (first in the list, or the last
     when the years run oldest-first).
Table rows: a row whose first cell is a customer name, under a nearby header about
sales/revenue share (not receivables), first number 10-100 in the row.
"""
from __future__ import annotations

import re

from aliases import C as CUSTOMERS
from aliases import _spell_re
from textutil import sentences

# --------------------------------------------------------------------------- alias search
_ALL = []
for c in CUSTOMERS:
    for s in set(c["spell"]):
        _ALL.append((len(s), s, c["id"]))
_ALL.sort(key=lambda x: -x[0])
BIG = re.compile(r"(?<![A-Za-z0-9&])(?:" + "|".join(_spell_re(s) for _, s, _ in _ALL) + r")(?![A-Za-z0-9])")
_ENTRY = [(re.compile(r"(?:" + _spell_re(s) + r")\Z"), cid) for _, s, cid in _ALL]
_BYID = {c["id"]: c for c in CUSTOMERS}
_NA = {c["id"]: re.compile(c["not_after"]) for c in CUSTOMERS if c["not_after"]}
_NB = {c["id"]: re.compile(c["not_before"]) for c in CUSTOMERS if c["not_before"]}


def which(span: str) -> str | None:
    for rx, cid in _ENTRY:
        if rx.match(span):
            return cid
    return None


# --------------------------------------------------------------------------- patterns
PCT = re.compile(r"(\d{1,3}(?:\.\d+)?)\s?(?:%|percent\b|per cent\b)")
REVW = re.compile(r"(?i)\b(?:sales|revenues?|shipments|billings)\b")
_SUF1 = (r",?\s*(?:Incorporated|Inc|Corporation|Corp|Companies|Company|Co\.,?\s*Inc|Co|L\.L\.C|LLC|Limited|Ltd|"
         r"L\.P|LP|p\.l\.c|plc|N\.V|S\.A|AG|SE|Stores|Holdings|Group|U\.S\.A|USA|U\.S|US|North America|"
         r"Americas|America|International|Worldwide|Global|Enterprises)\.?(?![A-Za-z])")
_PAR1 = r"\s*\([^)]{0,100}\)"
# any run of legal-form suffixes and parentheticals: "Shell Trading (US) Company", "Apple Inc. ("Apple")"
SUFFIX = r"(?:" + _SUF1 + r"|" + _PAR1 + r")*"
PAREN = r"(?:" + _PAR1 + r")?"
# extra capitalised words that belong to the customer's legal name ("Costco Wholesale Corporation",
# "Chevron Products Company", "Lowe's Home Centers, LLC")
NAME_TAIL = r"(?:\s+(?!(?:In|During|For|And|Or|The|Our|Its|Which|Who|Accounted|Represented)\b)[A-Z][A-Za-z0-9&.'\-]*){0,4}"
AFFIL = (r"(?:\s*,?\s*(?:and|together with|including|along with|plus)\s+(?:its|their|certain of its|various of its)\s+"
         r"(?:\w+\s+)?(?:affiliates|subsidiaries|affiliated (?:companies|entities)|related (?:parties|entities)|"
         r"divisions|stores|banners|affiliate|subsidiary)\s*,?)?")
POST_VERB = re.compile(
    r"^" + SUFFIX + PAREN + r"\.?" + AFFIL + PAREN +
    r"\s*,?\s*(?:(?:which|who)\s+(?:is|was|has been|were)\s+(?:our|the Company's|its)\s+(?:\w+\s+){0,2}customers?\s*,?\s*)?"
    r"(?:(?:our|the Company's|its)\s+(?:\w+\s+){0,2}customers?\s*,?\s*)?"
    r"(?:(?:which|who|that)\s+)?(?:together\s+|collectively\s+|combined\s+|individually\s+|each\s+)?"
    r"(?:accounted|accounts|account|represented|represents|represent|comprised|comprises|comprise|constituted|"
    r"constitutes|contributed|contributes|made up|makes up|amounted|amounts|totaled|totalled|generated|"
    r"was responsible|were responsible|is responsible|accounting|representing|comprising)\b", re.I)
POST_ISCUST = re.compile(
    r"^" + SUFFIX + PAREN + AFFIL +
    r"\s*,?\s*(?:is|was|has been|remains|remained|became|continues to be|continued to be|were|are)\s+"
    r"(?:our|the Company's|its|the)\s+(?:\w+\s+){0,2}(?:customer|customers|purchaser|distributor|account)\b", re.I)
PRE_ROLE = re.compile(
    r"(?:(?:sales|revenues?|shipments|billings|business|orders|net sales|product sales|sold|sell|selling|sells|"
    r"revenue derived|revenues derived|revenue generated|revenues generated|revenue earned|revenues earned|"
    r"income|receipts)\s+(?:(?:were|was|is|are|made|primarily|principally|directly|indirectly|of|our|its|the|"
    r"recognized|received|by|us|we|"
    r"products?|services?|goods|merchandise|in|fiscal|\d{4}|attributable|attributed|derived|generated|"
    r"under|contracts?|agreements?|through|with)\s+){0,4}(?:to|from|with)"
    r"|(?:largest|major|significant|principal|biggest|primary|key|single largest|largest single|"
    r"second largest|third largest|one|two|three|four|five|same)\s+(?:\w+\s+)?customers?\s*,?\s*(?:was|were|is|are|being|namely|:|,|-)?"
    r"|customers?\s+(?:was|were|is|are|namely|being)"
    r"|(?:purchaser|purchasers)\s+(?:was|were|is|are)?)"
    r"\s*,?\s*(?:the\s+)?$", re.I)
SUPPLIER_PRE = re.compile(r"(?i)(?:products?|services?|merchandise|equipment|brands?|lines?|purchases?|purchased|"
                          r"sourced|supplied|manufactured|licensed|distributed|made|produced|franchised|provided)\s+"
                          r"(?:and\s+\w+\s+)?(?:\w+\s+){0,2}(?:from|of|by)\s*(?:the\s+)?$")
VENDOR_PRE = re.compile(r"(?i)(?:\b(?:vendor|vendors|supplier|suppliers|licensor|licensors)\b[^.;]{0,40}$|"
                        r"(?:sub-?contractors?|contract manufacturers?|manufacturers?|suppliers?|distributors?|resellers?|"
                        r"providers?|vendors?|partners?)\s+(?:to|for|of)\s+(?:the\s+)?$)")
GROUP_PRE = re.compile(r"(?i)(?:customers?\s*,?\s*(?:including|include|includes|included|such as|like)\s*$|"
                       r"(?:including|such as|like)\s*$)")
SEP = re.compile(r"^" + NAME_TAIL + SUFFIX + PAREN + AFFIL + PAREN + r"\s*(?:,|;|and|or|&|/|,\s*and|,\s*or)?\s*(?:the\s+)?$")
NEG_BEFORE = re.compile(r"(?i)(?:less than|under|below|fewer than|no more than|not more than|lower than|up to)\s*(?:approximately\s*)?$")
_OF = (r"(?:,|;|and|or|\s)*(?:respectively)?(?:,|\s)*"
       r"(?:(?:in|for|during)\s+(?:fiscal\s+)?(?:years?\s+)?(?:\d{4}|each of)(?:\s*,?\s*(?:and\s+)?\d{4})*\s*,?\s*)?"
       r"(?:respectively,?\s*)?of\s+(?:the\s+)?(?:(?P<poss>[A-Za-z][\w&.\-]*(?:\s+[A-Za-z][\w&.\-]*){0,2})'s\s+)?"
       r"(?:(?:the|our|its|their|total|consolidated|net|gross|"
       r"worldwide|annual|operating|overall|aggregate|product|products|fiscal|\d{4})\s+){0,5}")
REV_AFTER = re.compile(r"^" + r"(?:\s*(?:,|and|or)\s*(?:(?:approximately|about|roughly|nearly|over|more than|less than|under|below|in excess of)\s*)?\d{1,3}(?:\.\d+)?\s?(?:%|percent)\s*)*\s*" + _OF +
                       r"(?:net\s+)?(?:sales|revenues?|net revenues?|product sales|shipments|product revenues?|"
                       r"billings|net product sales|gross product sales|operating revenues?|product shipments|"
                       r"total revenues?|net sales revenues?|contract revenues?|oil and (?:natural )?gas (?:sales|revenues?)|"
                       r"oil,? (?:natural gas|NGL)[\w ,]{0,30}(?:sales|revenues?)|(?:crude )?oil (?:sales|revenues?)|"
                       r"(?:natural )?gas (?:sales|revenues?)|production revenues?)\b", re.I)
BAD_QUAL = re.compile(r"(?i)segment|division|business unit|receivable|purchases|inventor|cost of|backlog|"
                      r"unit sales|units sold|volume|market share")
YEAR = re.compile(r"\b(19[89]\d|20[0-4]\d)\b")
SEG_BEFORE = re.compile(r"(?i)\b(?:segment|segments|division|divisions|business unit|subsidiary|subsidiaries)\b(?!\s+(?:and|or)\b)")


_GENERIC_OWNER = {"company", "corporation", "partnership", "registrant", "group", "trust", "bank", "fund", "firm",
                  "entity", "issuer", "our company", "the company", "holding", "holdings", "combined company"}
FILER_WORDS: set = set()     # words of the filer's name, set by extract() for the possessive check


def rev_share(s: str, pos: int) -> bool:
    """Is the percentage ending at s[pos] a share of the filer's total sales/revenue?"""
    tail = s[pos:pos + 170]
    m = REV_AFTER.match(tail)
    if not m:
        return False
    if BAD_QUAL.search(tail[:m.end()]):
        return False
    owner = m.group("poss")
    if owner:
        o = owner.lower().strip()
        words = {w for w in re.findall(r"[a-z0-9&]+", o) if len(w) >= 3} - {"the", "and", "inc", "corp"}
        if o not in _GENERIC_OWNER and not (words and words <= FILER_WORDS) and not (words & FILER_WORDS and len(words) == 1):
            return False    # "of Fresh Dairy Direct's net sales": a segment's or someone else's sales
    # "20% of our sales of hospitality systems": a product line, not total sales
    if re.match(r"^\s+of\s+(?!(?:the\s+)?(?:Company|Corporation|Registrant|Partnership|Group)\b)(?:our\s+|the\s+|its\s+)?[a-z]",
                tail[m.end():m.end() + 40]):
        return False
    return True


def pct_list_after(s: str, start: int) -> list[tuple[float, int, int, bool]]:
    """Percentages after `start`: (value, start, end, is_revenue_share)."""
    out = []
    for m in PCT.finditer(s, start):
        neg = bool(NEG_BEFORE.search(s[max(0, m.start() - 25):m.start()]))
        # "less than 10%" stays in the list (positions matter) with value 0: below the threshold
        out.append((0.0 if neg else float(m.group(1)), m.start(), m.end(), rev_share(s, m.end())))
    return out


_QUAL = r"(?:(?:approximately|about|roughly|nearly|over|more than|less than|under|below|fewer than|in excess of)\s*)?"
_LSEP = re.compile(r"\s*(?:,|;|and|or|,\s*and|,\s*or)?\s*" + _QUAL)


def _list_run(pcts, s):
    """The first run of percentages ('25%, 23% and 20%') that carries a revenue-share qualifier."""
    for i, p in enumerate(pcts):
        if p[3]:
            j = i
            while j > 0 and _LSEP.fullmatch(s[pcts[j - 1][2]:pcts[j][1]]):
                j -= 1
            k = i
            while k + 1 < len(pcts) and _LSEP.fullmatch(s[pcts[k][2]:pcts[k + 1][1]]):
                k += 1
            return pcts[j:k + 1]
    return []


def _pick_recent(run, s, a, b):
    """Most recent year's value from a list run: first, or last when years run oldest-first."""
    vals = [p[0] for p in run]
    if len(vals) >= 2:
        yrs = [int(y) for y in YEAR.findall(s)]
        if len(yrs) >= 2 and len(yrs) >= len(vals) and yrs[0] < yrs[-1]:
            return vals[-1], vals
    return vals[0], vals


_STOPFIRST = {"In", "During", "For", "The", "Our", "Sales", "Net", "Revenue", "Revenues", "As", "At", "Of", "By",
              "With", "From", "To", "Fiscal", "Approximately", "Customers", "Customer", "Each", "Both", "Two", "Three",
              "Four", "Five", "Its", "We", "These", "This", "Such", "No", "One", "Also", "Additionally", "However",
              "Further", "Furthermore", "Company", "Total", "Products", "Product", "Subsidiaries", "Affiliates",
              "Including", "Includes", "Include", "Namely", "Other", "All", "Certain", "Their", "Consolidated"}
_TOKEN = r"[A-Z][A-Za-z0-9&.'\-]*"
NAME_ITEM = r"(?:" + _TOKEN + r")(?:\s+(?:" + _TOKEN + r"|&|of|de|du|la|\d+[A-Za-z]*))*" + SUFFIX + PAREN
LIST_SEP = r"\s*(?:,\s*and|,\s*&|,\s*or|,|and|&|or)\s*"
_FWD_ITEM = re.compile(LIST_SEP + r"(?!(?:our|its|the|which|who|each|respectively|collectively|together|both)\b)("
                       + NAME_ITEM + r")" + AFFIL)
_BWD_ITEM = re.compile(r"(?:^|(?<=[\s,(;:]))(" + NAME_ITEM + r")" + AFFIL + LIST_SEP + r"$")
_LEAD = re.compile(r"^" + NAME_TAIL + SUFFIX + PAREN + AFFIL + PAREN)


def _first_ok(name: str) -> bool:
    return name.split()[0].strip(",.") not in _STOPFIRST


def sentence_mentions(s: str) -> list[dict]:
    if len(s) > 2500 or not PCT.search(s) or not REVW.search(s):
        return []
    ms = []
    for m in BIG.finditer(s):
        cid = which(m.group(0))
        if cid is None:
            continue
        if cid in _NA and _NA[cid].search(s[m.end():m.end() + 40]):
            continue
        if cid in _NB and _NB[cid].search(s[max(0, m.start() - 20):m.start()]):
            continue
        if ms and m.start() - ms[-1][1] <= 100:
            gap = s[ms[-1][1]:m.start()]
            if gap.count("(") > gap.count(")"):
                continue  # inside a parenthetical after a name: 'Apple Inc. ("Apple")'
        ms.append((m.start(), m.end(), cid, m.group(0)))
    if not ms:
        return []
    # chains of alias names joined only by separators
    chains, cur = [], [ms[0]]
    for prev, nxt in zip(ms, ms[1:]):
        if SEP.match(s[prev[1]:nxt[0]]):
            cur.append(nxt)
        else:
            chains.append(cur)
            cur = [nxt]
    chains.append(cur)
    out = []
    for ci, ch in enumerate(chains):
        a, b = ch[0][0], ch[-1][1]
        # extend the list over non-alias company names on either side
        nb, pa = 0, a
        while True:
            m = _BWD_ITEM.search(s[max(0, pa - 150):pa])
            if not m or not _first_ok(m.group(1)):
                break
            nb += 1
            pa = max(0, pa - 150) + m.start()
        na, pb = 0, b + _LEAD.match(s[b:]).end()
        while True:
            m = _FWD_ITEM.match(s, pb)
            if not m or not _first_ok(m.group(1)) or BIG.match(m.group(1)):
                break
            na += 1
            pb = m.end()
        pre = s[max(0, pa - 120):pa]
        post = s[pb:pb + 200]
        role = None
        if SUPPLIER_PRE.search(pre[-80:]) or VENDOR_PRE.search(pre[-60:]):
            continue   # "sales of products and services from IBM", "our largest vendor, Motorola",
                       # "Foxconn, a sub-contractor for Cisco": not the filer's customer
        if PRE_ROLE.search(pre):
            role = "pre"
        elif POST_VERB.match(post) or POST_ISCUST.match(post):
            role = "post"
        if role is None:
            continue
        if SEG_BEFORE.search(s[:pa]):
            continue   # "In our Innerwear segment, Walmart accounted for 38% of net sales": a segment share
        group = bool(GROUP_PRE.search(pre[-60:]))
        n_items = nb + len(ch) + na
        nxt_a = chains[ci + 1][0][0] if ci + 1 < len(chains) else len(s)
        assigned = {}          # chain index -> (value, run values)
        after = pct_list_after(s[:nxt_a], pb)
        run = _list_run(after, s)
        if run:
            vals = [p[0] for p in run]
            if n_items == 1:
                assigned[0] = _pick_recent(run, s, pb, nxt_a)
            elif len(vals) >= n_items and ("respectively" in s[pb:] or len(vals) == n_items):
                for k in range(len(ch)):
                    assigned[k] = (vals[nb + k], vals)
            # a single share for several names ("A and B together accounted for 35%") is not a link
        if not assigned and n_items == 1 and role == "post" and after:
            # elliptical: "..., and Ford accounted for 12%." (qualifier stated earlier in the sentence)
            mv = POST_VERB.match(post) or POST_ISCUST.match(post)
            p0 = after[0]
            gap = s[pb + mv.end():p0[1]]
            if len(gap) <= 45 and not re.search(r"(?i)increase|decrease|grew|growth|declin|change|rose|fell", gap) \
                    and any(q[3] for q in pct_list_after(s, 0)):
                assigned[0] = (p0[0], [p0[0]])
        if not assigned and n_items == 1 and role == "pre" and re.search(
                r"(?i)(?:were|was|are|is|came|come|derived|made|attributable|attributed|generated|earned)\s+"
                r"(?:\w+\s+){0,3}(?:to|from|with)\s*,?\s*(?:the\s+)?$", pre):
            # "25% of our net sales were to Walmart"
            before = pct_list_after(s[:pa], max(0, pa - 250))
            runb = _list_run(before, s)
            if runb:
                assigned[0] = _pick_recent(runb, s, max(0, pa - 250), pa)
        if group and n_items > 1 and not assigned:
            continue
        seen = set()
        for k, x in enumerate(ch):
            if k in assigned and x[2] not in seen:
                seen.add(x[2])
                v, vals = assigned[k]
                yrs = [int(y) for y in YEAR.findall(s)]
                out.append(dict(cid=x[2], alias=x[3], pct=v, pcts=";".join(f"{q:g}" for q in vals),
                                role=role, combined=False, chain=ci, list_items=n_items,
                                years=";".join(str(y) for y in sorted(set(yrs))), snippet=s[:700]))
    return out


# --------------------------------------------------------------------------- tables
ROW_NUM = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d+)?)(?![\d.,]*\d{3})")
HDR_REV = re.compile(r"(?i)(?:sales|revenues?)")
HDR_REC = re.compile(r"(?i)receivable")
HDR_PCT = re.compile(r"(?i)%|percent")


def table_mentions(lines: list[str], i: int) -> list[dict]:
    row = lines[i]
    cells = [c.strip() for c in row.split("|")]
    cells = [c for c in cells if c]
    if len(cells) < 2:
        return []
    first = cells[0]
    m = BIG.match(first)
    if not m:
        return []
    cid = which(m.group(0))
    if cid is None:
        return []
    rest_first = first[m.end():]
    if not re.fullmatch(NAME_TAIL + SUFFIX + PAREN + AFFIL + r"\s*[:\-]?\s*(?:\(\d\))?\s*", rest_first):
        return []
    # nearest header line above that mentions sales/revenue or receivables
    kind = None
    for j in range(i - 1, max(-1, i - 15), -1):
        L = lines[j]
        rec, rev = HDR_REC.search(L), HDR_REV.search(L)
        if rec and not rev:
            kind = "rec"
            break
        if rev and not rec:
            kind = "rev" if (HDR_PCT.search(L) or HDR_PCT.search(" ".join(lines[max(0, j - 3):i + 1]))) else None
            break
        if rev and rec:
            kind = None
            break
    if kind != "rev":
        return []
    if re.search(r"(?i)segment|division|tenant|rent", " ".join(lines[max(0, i - 8):i])):
        return []    # segment-level or rent tables: not a share of the filer's total revenue
    nums = []
    for c in cells[1:]:
        c2 = c.replace("%", "").strip()
        if re.fullmatch(r"\(?\d{1,3}(?:\.\d+)?\)?", c2):
            nums.append(float(c2.strip("()")))
        elif re.fullmatch(r"[*\-—–]|n/?a|N/?A|\*+|—", c2):
            nums.append(None)
        elif c2 in ("", "$"):
            continue
        else:
            return []  # a row with dollar amounts or text is not a share row
    vals = [v for v in nums if v is not None]
    if not vals or nums[0] is None:
        return []
    if any(v > 100 for v in vals):
        return []
    hdr = " ".join(lines[max(0, i - 8):i])
    yrs = [int(y) for y in YEAR.findall(hdr)]
    return [dict(cid=cid, alias=m.group(0), pct=nums[0], pcts=";".join(f"{q:g}" for q in vals), role="table",
                 combined=False, chain=-1, list_items=1, years=";".join(str(y) for y in sorted(set(yrs))),
                 snippet=(" / ".join(lines[max(0, i - 4):i + 1]))[:700])]


def extract(text: str, filer_name: str | None = None) -> list[dict]:
    global FILER_WORDS
    FILER_WORDS = {w for w in re.findall(r"[a-z0-9&]+", (filer_name or "").lower().split("(cik")[0].split("  (")[0])
                   if len(w) >= 3} - {"inc", "corp", "the", "and", "company", "corporation", "ltd", "llc", "co"}
    out = []
    for off, s in sentences(text):
        parts = [s]
        if s.count("|") >= 2:   # table row: only long narrative cells are read as sentences
            parts = [c.strip() for c in s.split("|") if len(c.strip()) >= 80]
        for part in parts:
            for r in sentence_mentions(part):
                r["offset"] = off
                out.append(r)
    lines = text.split("\n")
    for i, L in enumerate(lines):
        if L.count("|") >= 2 and BIG.search(L[:80]):
            for r in table_mentions(lines, i):
                r["offset"] = -1
                out.append(r)
    return out

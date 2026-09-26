"""HTML/text cleaning and sentence splitting for 10-K documents."""
from __future__ import annotations

import html
import re

_IS_HTML = re.compile(r"(?i)<(?:html|body|p|div|table|font|br)\b")
_DROP = re.compile(r"(?is)<(script|style|ix:header|xbrl|head)\b.*?</\1\s*>")
_TR_END = re.compile(r"(?i)</tr\s*>")
_CELL_END = re.compile(r"(?i)</t[dh]\s*>")
_BLOCK = re.compile(r"(?i)<(?:/p|/div|br\s*/?|/li|/h[1-6]|/table|p\b[^>]*|div\b[^>]*)\s*>")
_TAG = re.compile(r"(?s)<[^>]+>")
_WS = re.compile(r"[ \t\r\f\v    ​]+")
_NL = re.compile(r"\n\s*\n+")


def html_to_text(raw: str) -> str:
    """Strip tags. Table cells become ' | ', rows and blocks become newlines."""
    if not raw:
        return ""
    s = raw
    if _IS_HTML.search(s[:20000]):
        # raw line breaks inside HTML are just source formatting
        s = s.replace("\r", " ").replace("\n", " ")
    else:
        # plain-text filing: a blank line ends a paragraph, a single newline is a wrap
        s = s.replace("\r", "")
        s = re.sub(r"\n[ \t]*\n+", "\u2029", s)
        s = s.replace("\n", " ").replace("\u2029", "\n\n")
        s = html.unescape(s)
    s = _DROP.sub(" ", s)
    s = _CELL_END.sub(" | ", s)
    s = _TR_END.sub("\n", s)
    s = _BLOCK.sub("\n", s)
    s = _TAG.sub(" ", s)
    s = html.unescape(s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    s = _WS.sub(" ", s)
    s = re.sub(r"(\d) \.(\d)", r"\1.\2", s)          # "26 .5 %" -> "26.5 %"
    s = re.sub(r"(\d\.) (\d)", r"\1\2", s)           # "26. 5%"  -> "26.5%"
    s = re.sub(r" *\n *", "\n", s)
    s = _NL.sub("\n\n", s)
    return s


# Sentence splitter tolerant of corporate abbreviations ("Inc.", "Corp.", "Co.", "U.S.").
_ABBR = r"(?:Inc|Corp|Co|Ltd|L\.P|LLC|Mr|Ms|Dr|No|Nos|U\.S|U\.K|St|Jr|Sr|vs|approx|Fig|Nov|Dec|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|S\.A|N\.V|B\.V|A\.G|Bros|Mfg|Intl|Assn|e\.g|i\.e|etc)"


def sentences(text: str) -> list[tuple[int, str]]:
    """(start offset, sentence) pairs. Splits on . ! ? followed by space + capital/quote/digit,
    or on newlines, but not after common abbreviations or single capital initials."""
    out = []
    for m in re.finditer(r"[^\n]+", text):
        para, base = m.group(0), m.start()
        start = 0
        for mm in re.finditer(r"[.!?;](?=\s+[\"'(]?[A-Z0-9])", para):
            end = mm.end()
            prev = para[max(0, mm.start() - 12):mm.start() + 1]
            if re.search(r"(?:\b" + _ABBR + r"|\b[A-Z])\.$", prev):
                continue
            if mm.group(0) == ";":
                continue
            seg = para[start:end].strip()
            if seg:
                out.append((base + start, seg))
            start = end
        seg = para[start:].strip()
        if seg:
            out.append((base + start, seg))
    return out

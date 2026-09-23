"""Tiny helper: SEC HTML -> plain text with table rows kept on one line (cells joined by ' | ')."""
import re
from bs4 import BeautifulSoup


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style"]):
        t.decompose()
    for tr in soup.find_all("tr"):
        cells = []
        for td in tr.find_all(["td", "th"]):
            s = re.sub(r"\s+", " ", td.get_text(" ", strip=True)).strip()
            if s and s not in ("$",):
                cells.append(s)
        tr.replace_with(soup.new_string("\n" + " | ".join(cells) + "\n"))
    txt = soup.get_text("\n")
    txt = txt.replace("\xa0", " ")
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt)
    return txt

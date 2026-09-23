#!/usr/bin/env python
"""
Precision check: random sample of documents that matched the exact phrase
"operating leverage", fetch the matched file from EDGAR Archives, strip HTML,
extract +/-300 characters around the phrase, and (once hand labels exist in
precision_labels.csv) render precision_sample.md with the proportions.

    .venv/bin/python research/oplev/commentary/precision_check.py            # sample + snippets
    .venv/bin/python research/oplev/commentary/precision_check.py --sample validation --n 30
         # second sample, drawn from the recommended clean event definition (clean_events.csv.gz)
    .venv/bin/python research/oplev/commentary/precision_check.py --sample tenk --n 20
         # third sample, 10-K hits only, to size the risk-factor / boilerplate problem

section_guess (most recent 'Item N' heading before the match) is a crude heuristic kept in
the CSV only; it is fooled by cross-references such as 'see Item 1A' and was wrong on 2 of the
first 20 random files, so the markdown does not show it. Labels come from reading the text.

Sampling unit = one matched FILE (accession + file name). Draw order is fixed by
the seed; files that cannot be used (PDF/image, fetch error, phrase not found in the
stripped text) are skipped and logged, and the next file in the draw is taken.
"""
from __future__ import annotations

import argparse
import html
import re
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
DOCS = HERE / "cache" / "docs"
UA = "ClaudeSpace research dspinjr@gmail.com"
PAT = re.compile(r"operating[\s\-]+leverage", re.I)
WIN = 300
SEED = 20260923


def fetch(url: str, dest: Path) -> bytes | None:
    if dest.exists() and dest.stat().st_size > 0:
        return dest.read_bytes()
    for attempt in range(6):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=90)
        except requests.RequestException:
            time.sleep(2 ** attempt)
            continue
        time.sleep(0.2)  # <= 5 req/s to sec.gov
        if r.status_code == 200:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            return r.content
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(2 ** attempt)
            continue
        return None
    return None


def to_text(raw: bytes, fname: str) -> str:
    s = raw.decode("utf-8", errors="replace")
    if fname.lower().endswith((".htm", ".html", ".xml")) or "<html" in s[:5000].lower():
        soup = BeautifulSoup(s, "lxml")
        for t in soup(["script", "style"]):
            t.decompose()
        s = soup.get_text(" ")
    s = html.unescape(s).replace("\xa0", " ")
    return re.sub(r"\s+", " ", s)


SECTION = re.compile(r"\bitem\s*(1a|1b|1|2|3|4|5|6|7a|7|8|9a|9)\b[\s\.\:\-–—]*([a-z’' ,&]{0,60})", re.I)


def section_guess(text: str, pos: int, root_form: str) -> str:
    """Most recent 'Item N' heading before the match (10-K/10-Q only). Heuristic."""
    if "8-K" in root_form:
        return ""
    last = None
    for m in SECTION.finditer(text, 0, pos):
        last = m
    if not last:
        return "?"
    tag = last.group(1).upper()
    title = last.group(2).strip().lower()
    if tag == "1A" or "risk factor" in title:
        return "Item 1A risk factors"
    if tag in ("7", "2") and ("management" in title or "discussion" in title):
        return "MD&A"
    return f"Item {tag} {title[:30]}".strip()


def snippets(text: str, k: int = 3):
    out, last_end = [], -1
    for m in PAT.finditer(text):
        if m.start() < last_end:
            continue
        a, b = max(0, m.start() - WIN), min(len(text), m.end() + WIN)
        out.append((m.start(), text[a:b]))
        last_end = b
        if len(out) >= k:
            break
    return out, len(PAT.findall(text))


def draw_pool(kind: str) -> pd.DataFrame:
    m = pd.read_csv(HERE / "mentions.csv.gz", dtype={"sic": "string", "items": "string"}, low_memory=False)
    if kind == "random":
        pool = m[m.phrase_key == "operating_leverage"]
    elif kind == "tenk":
        pool = m[(m.phrase_key == "operating_leverage") & (m.query_form == "10-K")]
    else:  # validation sample of the recommended clean event
        ev = pd.read_csv(HERE / "clean_events.csv.gz")
        ev = ev.assign(file_name=ev.file_names.str.split(";")).explode("file_name")
        pool = m[m.phrase_key == "operating_leverage"].merge(ev[["cik", "adsh", "file_name"]].drop_duplicates(),
                                                              on=["cik", "adsh", "file_name"])
    pool = pool.sort_values(["adsh", "file_name", "cik"]).drop_duplicates(["adsh", "file_name"])
    seed = {"random": SEED, "validation": SEED + 1, "tenk": SEED + 2}[kind]
    return pool.sample(frac=1.0, random_state=seed).reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", choices=["random", "validation", "tenk"], default="random")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--redraw", action="store_true",
                    help="draw a new sample even if precision_sample<tag>.csv exists (labels would no longer match)")
    args = ap.parse_args()
    tag = {"random": "", "validation": "_validation", "tenk": "_10k"}[args.sample]
    out_csv = HERE / f"precision_sample{tag}.csv"
    lab_path = HERE / f"precision_labels{tag}.csv"
    if out_csv.exists() and not args.redraw:
        # The hand labels refer to this exact sample, so re-render instead of redrawing.
        s = pd.read_csv(out_csv)
        sk = pd.read_csv(HERE / f"precision_skipped{tag}.csv")
        print(f"reusing {out_csv.name} ({len(s)} files); pass --redraw for a new draw")
        if lab_path.exists():
            render(s, pd.read_csv(lab_path), list(sk.itertuples(index=False, name=None)), tag)
        evaluate_all()
        return
    pool = draw_pool(args.sample)
    rows, skipped = [], []
    for _, r in pool.iterrows():
        if len(rows) >= args.n:
            break
        fn = r.file_name
        if fn.lower().endswith((".pdf", ".jpg", ".gif", ".png", ".xlsx", ".xls")):
            skipped.append((r.adsh, fn, "binary file type"))
            continue
        raw = fetch(r.url, DOCS / f"{r.adsh}_{fn}")
        if raw is None:
            skipped.append((r.adsh, fn, "fetch failed"))
            continue
        text = to_text(raw, fn)
        sn, n_occ = snippets(text)
        if not sn:
            skipped.append((r.adsh, fn, "phrase not found in stripped text"))
            continue
        pos0 = sn[0][0]
        rows.append(dict(
            sample_id=len(rows) + 1, cik=r.cik, display_name=r.display_name, sic=r.sic,
            is_financial=r.is_financial, file_date=r.file_date, form=r.form, doc_role=r.doc_role,
            is_earnings_8k=r.is_earnings_8k, adsh=r.adsh, file_name=fn, url=r.url, n_occurrences=n_occ,
            section_guess=section_guess(text, pos0, r.root_form),
            fls_nearby=bool(re.search(r"forward[\s\-]looking", text[max(0, pos0 - 1500): pos0 + 300], re.I)),
            snippet_1=sn[0][1], snippet_2=sn[1][1] if len(sn) > 1 else "", snippet_3=sn[2][1] if len(sn) > 2 else "",
        ))
    s = pd.DataFrame(rows)
    s.to_csv(HERE / f"precision_sample{tag}.csv", index=False)
    pd.DataFrame(skipped, columns=["adsh", "file_name", "reason"]).to_csv(HERE / f"precision_skipped{tag}.csv", index=False)
    print(f"sample{tag}: {len(s)} usable files, {len(skipped)} skipped")

    if lab_path.exists():
        render(s, pd.read_csv(lab_path), skipped, tag)
        evaluate_all()


LABELS = {
    "a": "(a) management describing its own operating leverage as positive / improving",
    "b": "(b) negative operating leverage / deleveraging",
    "c": "(c) risk-factor, forward-looking-statement or other boilerplate",
    "d": "(d) bank / financial-company usage (efficiency-ratio sense)",
    "e": "(e) other (definitions, generic discussion, third-party, etc.)",
}


def render(s: pd.DataFrame, lab: pd.DataFrame, skipped, tag: str):
    s = s.merge(lab, on="sample_id", how="left")
    n = len(s)
    counts = s.label.value_counts().reindex(list(LABELS)).fillna(0).astype(int)
    title = "Precision check" + {"": "", "_validation": " - validation sample of the recommended clean event",
                                 "_10k": " - 10-K-only sample (risk-factor check)"}[tag]
    md = [f"# {title}", ""]
    if tag == "_validation":
        md += ["Fresh random draw (seed 20260924) from the FIRST-PASS clean-event definition (non-financial filers, "
               "original 8-K / 10-Q / 10-K, phrase \"operating leverage\", no \"negative operating leverage\" / "
               "\"operating deleverage\" in the same filing). Two of the 30 turned out to be negatives phrased as "
               "\"reduced operating leverage\", which is why the final definition also drops filings that match the "
               "supplementary negative phrases and SPAC-named filers. See the scoring table at the bottom of "
               "precision_sample.md for how the final definition does on these files.", ""]
    elif tag == "_10k":
        md += ["Random draw (seed 20260925) of 10-K files matching \"operating leverage\" (all filers), to check how "
               "often the phrase sits in Item 1A risk factors or other boilerplate. Same labelling rules; the note "
               "says where in the 10-K the phrase sits.", ""]
    else:
        md += ["Random sample (seed 20260923) of files matching the exact phrase \"operating leverage\" in 8-K, 10-Q "
               "and 10-K filings, 2010-01-01 to 2026-09-23. Unit = one matched file. Each file was fetched from "
               "EDGAR, HTML stripped, and the text around the phrase read by hand. The label describes the file: "
               "if any shown occurrence is management describing the company's own operating leverage, the file "
               "gets (a)/(b); (c) only if every shown occurrence is boilerplate; (d) whenever the filer is a bank or "
               "other financial firm using the term in the revenue-growth-minus-expense-growth sense. Sub-labels "
               "split (a) into *realized* (the period's margins improved because of operating leverage), "
               "*forward* (expected or targeted operating leverage) and *model-claim* (a static claim that the business model has high operating leverage, typical of investor decks).", ""]
    md += ["| label | n | share |", "|---|---:|---:|"]
    for k, v in counts.items():
        md.append(f"| {LABELS[k]} | {v} | {v / n:.0%} |")
    md.append(f"| total | {n} | |")
    sub = s[s.label == "a"].sublabel.value_counts()
    if len(sub):
        md += ["", "Within (a): " + ", ".join(f"{k} {v} ({v / n:.0%} of sample)" for k, v in sub.items()) + "."]
    md += ["", f"Files skipped in the draw (unusable, replaced by the next draw): {len(skipped)}"]
    for a, f, why in skipped:
        md.append(f"- {a} {f}: {why}")
    md += ["", "Cross-tab by filer type and document type:", ""]
    s["filer"] = s.is_financial.map({True: "financial (SIC 6000-6999)", False: "non-financial"}).fillna("SIC missing")
    s["doc"] = s.apply(lambda r: "8-K earnings release (Item 2.02 EX-99)" if (r.doc_role == "ex99" and r.is_earnings_8k)
                         else ("8-K other" if "8-K" in r.form else f"{r.form} {r.doc_role}"), axis=1)
    ct = pd.crosstab([s["filer"], s["doc"]], s["label"]).reindex(columns=list(LABELS), fill_value=0)
    md.append("| filer | document | " + " | ".join(ct.columns) + " |")
    md.append("|---|---|" + "---:|" * len(ct.columns))
    for (f, w), row in ct.iterrows():
        md.append(f"| {f} | {w} | " + " | ".join(str(int(x)) for x in row) + " |")
    md += ["", "---", ""]
    for _, r in s.iterrows():
        sl = f" / {r.sublabel}" if isinstance(r.get("sublabel"), str) else ""
        md.append(f"### {r.sample_id}. {r.display_name} - {r.form} {r.file_date} - `{r.file_name}` -> **({r.label}){sl}**")
        meta = f"SIC {r.sic}; doc_role={r.doc_role}; earnings 8-K={r.is_earnings_8k}; occurrences in file={r.n_occurrences}"
        md += [meta + f"; [link]({r.url})", ""]
        if isinstance(r.get("note"), str) and r.note:
            md += [f"*Why:* {r.note}", ""]
        for c in ["snippet_1", "snippet_2", "snippet_3"]:
            if isinstance(r[c], str) and r[c]:
                t = PAT.sub(lambda m: f"**{m.group(0)}**", r[c].replace("|", "/"))
                md += [f"> ...{t}...", ""]
    (HERE / f"precision_sample{tag}.md").write_text("\n".join(md))
    print(counts.to_string())
    print(f"wrote precision_sample{tag}.md")


def evaluate_all():
    """Score the final event definitions against every hand-labelled file (all three samples)."""
    ev = pd.read_csv(HERE / "clean_events.csv.gz")
    neg = pd.read_csv(HERE / "clean_negative_events.csv.gz")
    clean = set(zip(ev.cik, ev.adsh))
    kick = set(zip(ev[ev.kicking_in].cik, ev[ev.kicking_in].adsh))
    negs = set(zip(neg.cik, neg.adsh))
    frames = []
    for tag, name in [("", "random"), ("_10k", "10-K only"), ("_validation", "first-pass clean")]:
        sp, lp = HERE / f"precision_sample{tag}.csv", HERE / f"precision_labels{tag}.csv"
        if sp.exists() and lp.exists():
            frames.append(pd.read_csv(sp).merge(pd.read_csv(lp), on="sample_id").assign(sample=name))
    if not frames:
        return
    a = pd.concat(frames, ignore_index=True)
    key = list(zip(a.cik, a.adsh))
    a["in_clean"] = [k in clean for k in key]
    a["in_kicking_in"] = [k in kick for k in key]
    a["in_clean_negative"] = [k in negs for k in key]
    a["channel"] = a.form.str.replace("/A", "", regex=False)
    a["lab"] = a.label + a.sublabel.where(a.label.eq("a"), "").radd("/").where(a.label.eq("a"), "")
    a[["sample", "sample_id", "cik", "adsh", "form", "channel", "label", "sublabel", "in_clean", "in_kicking_in",
       "in_clean_negative"]].to_csv(HERE / "precision_eval.csv", index=False)
    cats = ["a/realized", "a/forward", "a/model-claim", "b", "c", "d", "e"]
    rows = []
    for nm, mask in [("all labelled files", a.index == a.index),
                     ("random sample only (unconditional)", a["sample"].eq("random")),
                     ("in final clean_events", a.in_clean),
                     ("  of which 8-K", a.in_clean & a.channel.eq("8-K")),
                     ("  of which 10-Q", a.in_clean & a.channel.eq("10-Q")),
                     ("  of which 10-K", a.in_clean & a.channel.eq("10-K")),
                     ("in final kicking_in subset", a.in_kicking_in),
                     ("in clean_negative_events", a.in_clean_negative),
                     ("excluded from both", ~a.in_clean & ~a.in_clean_negative)]:
        sub = a[mask]
        vc = sub.lab.value_counts()
        r = {"subset": nm, "n": len(sub)}
        r.update({c: int(vc.get(c, 0)) for c in cats})
        r["share (a)"] = f"{sub.label.eq('a').mean():.0%}" if len(sub) else ""
        r["share a/realized"] = f"{sub.lab.eq('a/realized').mean():.0%}" if len(sub) else ""
        rows.append(r)
    t = pd.DataFrame(rows)
    lines = ["## How the final event definitions score on all hand-labelled files", "",
             f"{len(a)} labelled files: 40 random (all filers, all forms), 20 random 10-K hits, 30 random draws "
             "from the first-pass clean definition. Membership is by (CIK, accession) in the FINAL "
             "`clean_events.csv.gz` / `clean_negative_events.csv.gz`. The three samples come from different pools "
             "(the 10-K draw over-weights 10-Ks), and each row has only a few dozen files, so treat the shares as "
             "rough (a 90% share on 30 files has a 95% interval of roughly 74-98%). Unit = file; a filing-level "
             "event can carry a different tone in another exhibit of the same filing.", "",
             "| " + " | ".join(t.columns) + " |", "|---|" + "---:|" * (len(t.columns) - 1)]
    for _, r in t.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.values) + " |")
    block = "\n".join(lines) + "\n"
    p = HERE / "precision_sample.md"
    if p.exists():
        txt = p.read_text()
        marker = "## How the final event definitions score"
        if marker in txt:
            head, rest = txt.split(marker, 1)
            tail = rest[rest.find("\n---\n"):] if "\n---\n" in rest else ""
            txt = head + block + tail
        else:
            txt = txt.replace("\n---\n", "\n" + block + "\n---\n", 1)
        p.write_text(txt)
    print(t.to_string(index=False))


if __name__ == "__main__":
    main()

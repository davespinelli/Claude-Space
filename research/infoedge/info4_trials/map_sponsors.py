"""Step 1b: map ClinicalTrials.gov lead-sponsor names to SEC registrants.

Pass 1: exact match on the normalised name (legal suffixes and punctuation removed).
Pass 2: match on the "core" name (normalised name with generic industry words removed),
        only when the core is at least 5 characters, points to exactly one SEC company, and
        is either two or more words or a single word that is not an ordinary English word
        (/usr/share/dict/words); a one-word core whose two names carry different industry
        words ("Nobilis Therapeutics" vs "Nobilis Health") is rejected. build_universe.py also
        requires a health-care SIC code for these looser matches.
Exact matches whose normalised name is a single dictionary word ("Beam") are labelled
exact_word and, like core matches, need a health-care SIC code in build_universe.py.
SEC names come from data/sec_cache/company_tickers.json (current registrants with tickers)
plus, for companies that have since delisted, cache/sec_names_hist.csv (built by
build_sec_names.py from EDGAR xbrl.idx quarterly indices, 10-K/10-Q filers only).
Output: data/sponsor_map.csv (one row per sponsor name that mapped).
"""
import csv, json, re
from collections import defaultdict
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

SUFFIX = {"inc", "incorporated", "corp", "corporation", "co", "company", "ltd", "limited", "llc",
          "plc", "sa", "ag", "nv", "se", "as", "gmbh", "lp", "llp", "the", "bv", "ab", "asa",
          "oyj", "spa", "sarl", "kk", "pty", "ulc", "de", "us", "usa", "holdings", "holding"}
GENERIC = {"pharmaceuticals", "pharmaceutical", "pharma", "therapeutics", "therapeutic",
           "biosciences", "bioscience", "biotherapeutics", "biopharma", "biopharmaceuticals",
           "biopharmaceutical", "biologics", "biotech", "biotechnology", "bio", "biomedical",
           "medical", "medicine", "medicines", "sciences", "science", "laboratories", "labs",
           "research", "and", "development", "international", "global", "group", "technologies",
           "technology", "health", "healthcare", "oncology", "diagnostics", "devices", "systems",
           "life", "clinical", "operations", "americas", "north", "america", "affairs", "rd"}

def norm(name):
    s = name.lower()
    s = re.sub(r"/\s*[a-z]{2,5}\b\s*/?", " ", s)   # SEC state/ADR tags like /DE/, / MA, /ADR
    s = s.replace("&", " and ").replace("+", " and ")
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    toks = s.split()
    while toks and toks[-1] in SUFFIX: toks.pop()
    while toks and toks[0] == "the": toks.pop(0)
    # drop interior legal words too (e.g. "Inc." before a division name), but not a leading
    # one ("INC Research Holdings" must not become "research")
    toks = toks[:1] + [t for t in toks[1:] if t not in {"inc", "llc", "ltd", "corp", "plc", "incorporated"}]
    return " ".join(toks)

try:
    WORDS = {w.strip().lower() for w in open("/usr/share/dict/words")}
except OSError:
    WORDS = set()


def core_ok(c):
    toks = c.split()
    return len(c.replace(" ", "")) >= 5 and (len(toks) >= 2 or toks[0] not in WORDS)


def generic_words(n):
    return {t for t in n.split() if t in GENERIC and t not in {"and", "the"}}


def core(n):
    return " ".join(t for t in n.split() if t not in GENERIC)

def load_sec():
    rows = []
    for v in json.load(open(ROOT / "data/sec_cache/company_tickers.json")).values():
        rows.append({"cik": int(v["cik_str"]), "sec_name": v["title"], "ticker": v["ticker"], "src": "current"})
    hist = HERE / "cache" / "sec_names_hist.csv"
    if hist.exists():
        for r in csv.DictReader(open(hist)):
            rows.append({"cik": int(r["cik"]), "sec_name": r["name"], "ticker": "", "src": "hist",
                         "first": r["first"]})
    return pd.DataFrame(rows)

def main():
    sec = load_sec()
    sec["n"] = sec.sec_name.map(norm); sec["c"] = sec.n.map(core)
    by_n = defaultdict(set); by_c = defaultdict(set); gen_c = defaultdict(set)
    for r in sec.itertuples():
        if r.n: by_n[r.n].add(r.cik)
        if len(r.c.replace(" ", "")) >= 5:
            by_c[r.c].add(r.cik); gen_c[(r.c, r.cik)] |= generic_words(r.n)
    names = sec.groupby("cik").agg(sec_name=("sec_name", "first"),
                                   ticker=("ticker", lambda x: next((t for t in x if t), ""))).to_dict("index")
    tr = pd.read_csv(HERE / "data/trials_current.csv", dtype=str).fillna("")
    out = []
    for sp, cnt in tr.lead_sponsor.value_counts().items():
        n = norm(sp); c = core(n); how, ciks = "", set()
        single_word = len(n.split()) == 1 and n in WORDS      # e.g. "Beam" -> Beam Inc (spirits)
        if n in by_n and len(by_n[n]) == 1:
            how, ciks = ("exact_word" if single_word else "exact"), by_n[n]
        elif c and core_ok(c) and c in by_c and len(by_c[c]) == 1:
            cik0 = next(iter(by_c[c])); gs, gc = generic_words(n), gen_c[(c, cik0)]
            # one-word core with different industry words on both sides ("Nobilis Therapeutics"
            # vs "Nobilis Health") is treated as a different company
            if not (len(c.split()) == 1 and gs and gc and not (gs & gc)):
                how, ciks = "core", by_c[c]
        if ciks:
            cik = next(iter(ciks))
            # first date this company filed a periodic report under a name matching the sponsor
            # (same normalised name, or same distinctive core, e.g. Sangamo BioSciences ->
            # Sangamo Therapeutics)
            same = (sec.cik == cik) & ((sec.n == n) | ((sec.c == c) & bool(c) & core_ok(c) if c else False))
            fs = sec[same]["first"].dropna()
            out.append({"lead_sponsor": sp, "n_trials": cnt, "cik": cik, "sec_name": names[cik]["sec_name"],
                        "ticker": names[cik]["ticker"], "match": how, "norm": n,
                        "name_first_seen": fs.min() if len(fs) else ""})
    df = pd.DataFrame(out)
    df.to_csv(HERE / "data/sponsor_map.csv", index=False)
    print(len(df), "sponsor names mapped;", df.cik.nunique(), "companies;", df.n_trials.sum(), "trials")
    print(df.match.value_counts())

if __name__ == "__main__":
    main()

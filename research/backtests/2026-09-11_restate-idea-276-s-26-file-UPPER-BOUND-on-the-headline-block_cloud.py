#!/usr/bin/env python3
"""IDEA 523 - restate idea 276's 26-file UPPER BOUND on the HEADLINE BLOCK.

Idea 276 published two bounds on how much of the record is exposed to the breadth/cap
collinearity: **136 cross-cap files** and, of those, **26** that additionally use a panel-
property word, with **14** naming `breadth`.  Idea 286 then showed the tightest of those
columns counts the WORD, not the CLAIM: 2 of the 14 are ledgers, 218 of 246 occurrences live
in those two, and only 1 of the 12 real headline files puts `breadth` in its own headline as
a panel property.

Two specific defects follow, and this run fixes both and reports what each bound becomes.

  (a) ROLE.  `breadth60`, `breadth gate`, `disp8`, `evol60` name an INSTRUMENT - a gate the
      book switches on - not a property OF A PANEL.  Idea 276's `PROP_TOK` has no lookahead
      and counts them all.  Every count here is published twice: RAW (idea 276's rule,
      unchanged) and ROLE-FILTERED (instrument spellings removed).
  (b) SITE.  A word anywhere in a 60 KB file is not that file's claim.  Every count is also
      published on a BLOCK - the part of the file that carries the headline - and with the
      property word required within a WINDOW of a panel token.

P1 = window width  {80, 200, 400, whole-block}  characters between panel token and property
P2 = block rule    {WHOLE FILE, FIRST 20 LINES, FIRST 40 LINES, TITLE+VERDICT}
4 x 4 = 16 points x {RAW, ROLE-FILTERED} x {both corpora} - every one reported.

The regexes, the corpus rule and the counting are IMPORTED from idea 276's own module, never
re-typed, so the RAW column is idea 276's statistic by construction and any move is the
restatement's, not a transcription's.

Idea 682 (this session) showed the record's corpus grows under every census, so both corpora
are run and reported side by side: idea 276's OWN corpus, restored from its publishing commit
78ab84b via git, and TODAY's.  The reproduction gate is that idea 276's rule on idea 276's
corpus returns idea 276's published numbers.

Rule 8 is run on the book axis (IS 2009-2016 chooses, OOS 2017-2026 read once) and both
PROTOCOL KEEP paths are evaluated, against the live baseline and SPY.

SURVIVORSHIP: the book block uses U56 (current constituents); the census is prose and carries
no market exposure.  Deterministic, standalone.  Writes only its own artefacts.  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.
"""
import importlib.util
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest, metrics                                     # noqa: E402

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
I276 = OUT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py"
I276_SHA = os.environ.get("I523_SHA", "78ab84b6f8b74b0013e47f687902dfad93223c60")

# idea 276's published census, quoted here ONLY as the gate's target
PUBLISHED = dict(files=292, small=140, large=266, cross=136, cmp=126, prop=26, breadth=14)

WINDOWS = [80, 200, 400, 10 ** 9]          # P1, chars; 1e9 == "anywhere in the block"
BLOCKS = ["WHOLE FILE", "FIRST 20 LINES", "FIRST 40 LINES", "TITLE+VERDICT"]   # P2

# ---- (a) the ROLE filter -----------------------------------------------------------------
# An instrument spelling: the property word carrying a parameter, or explicitly called a gate
# / overlay / instrument / arm / leg.  These are things a BOOK switches on, not descriptions
# of a PANEL, and idea 276's PROP_TOK counts them as panel properties.
INSTRUMENT = re.compile(
    r"\b(?:breadth|disp|dispersion|corr|evol|vol|ddctl)\s?\d+\b"
    r"|\b(?:breadth|dispersion|disp|corr|evol)[- ](?:gate|gated|overlay|instrument|arm|leg|"
    r"filter|screen|rule|signal|trigger|clause)\b"
    r"|\b(?:gate|overlay|instrument|arm|leg|filter|screen)\s+(?:on\s+)?"
    r"(?:breadth|dispersion|disp|corr|evol)\b", re.I)

IS_END, OOS_START, COST_BPS, FREQ = "2016-12-31", "2017-01-01", 10, "W"

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def git(*a):
    return subprocess.run(["git", *a], cwd=str(REPO), capture_output=True,
                          text=True, errors="replace").stdout


# =========================================================================================
# the two corpora
# =========================================================================================
def corpus_at(sha):
    """Idea 276's OWN corpus rule (research/backtests/*.md + LEADERBOARD + CHANGELOG),
    evaluated against the tree at `sha` - read from git, not from disk."""
    names = [l for l in git("ls-tree", "-r", "--name-only", sha).split("\n") if l]
    md = sorted(n for n in names
                if n.startswith("research/backtests/") and n.endswith(".md")
                and "/" not in n[len("research/backtests/"):])
    extra = [n for n in ("research/LEADERBOARD.md", "research/CHANGELOG.md") if n in names]
    out = {}
    for n in md + extra:
        out[Path(n).name] = git("show", f"{sha}:{n}")
    return out


def corpus_today():
    files = sorted((OUT).glob("*.md")) + [REPO / "research" / "LEADERBOARD.md",
                                          REPO / "research" / "CHANGELOG.md"]
    out = {}
    for f in files:
        if f.name == f"{STEM}.result.md":
            continue
        try:
            out[f.name] = f.read_text(errors="ignore")
        except Exception:
            pass
    return out


# =========================================================================================
# the counting
# =========================================================================================
def block_of(text, rule):
    if rule == "WHOLE FILE":
        return text
    if rule == "FIRST 20 LINES":
        return "\n".join(text.splitlines()[:20])
    if rule == "FIRST 40 LINES":
        return "\n".join(text.splitlines()[:40])
    if rule == "TITLE+VERDICT":
        lines = text.splitlines()
        keep = lines[:3]
        for i, l in enumerate(lines):
            if re.search(r"(?i)^\s*[#*\s]*verdict\b|\*\*verdict", l):
                keep += lines[i:i + 6]
        return "\n".join(keep) if len(keep) > 3 else "\n".join(lines[:3])
    raise ValueError(rule)


def strip_instruments(text):
    """Blank out instrument spellings so the property regex cannot see them.  Replaced with
    spaces, not deleted, so every character offset - and therefore every WINDOW distance -
    is preserved exactly."""
    return INSTRUMENT.sub(lambda m: " " * len(m.group(0)), text)


def near(text, tok_re, prop_re, w):
    """True if a property match lies within w characters of a panel-token match."""
    if w >= 10 ** 9:
        return bool(tok_re.search(text)) and bool(prop_re.search(text))
    ts = [m.start() for m in tok_re.finditer(text)]
    if not ts:
        return False
    ts = np.array(ts)
    for m in prop_re.finditer(text):
        if np.min(np.abs(ts - m.start())) <= w:
            return True
    return False


def score(corpus, m276, block_rule, window, role_filter):
    S, L, PR, C = m276.SMALL_TOK, m276.LARGE_TOK, m276.PROP_TOK, m276.CMP_TOK
    BR = re.compile(r"\bbreadth\b", re.I)
    PANEL = re.compile(f"(?:{S.pattern})|(?:{L.pattern})", re.I)
    rows = []
    for name, text in corpus.items():
        b = block_of(text, block_rule)
        bb = strip_instruments(b) if role_filter else b
        s, l = bool(S.search(b)), bool(L.search(b))
        rows.append(dict(file=name, small=s, large=l, cross=s and l,
                         cmp=bool(C.search(b)),
                         prop=near(bb, PANEL, PR, window),
                         breadth=near(bb, PANEL, BR, window)))
    D = pd.DataFrame(rows)
    cross = D[D.cross]
    cmpf = cross[cross.cmp]
    return dict(files=len(D), small=int(D.small.sum()), large=int(D.large.sum()),
                cross=int(D.cross.sum()), cmp=int(cmpf.shape[0]),
                prop=int(cmpf.prop.sum()), breadth=int(cmpf.breadth.sum())), D


# =========================================================================================
def book_block():
    px = load_universe()
    spy = px["SPY"].pct_change().fillna(0.0)
    start = px.index[260]
    series = {"RULES v2 (live)": backtest(px, rules_v2_weights(px), cost_bps=COST_BPS,
                                          freq=FREQ)["returns"].loc[start:],
              "RULES v1 (previous)": backtest(px, rules_v1_weights(px), cost_bps=COST_BPS,
                                              freq=FREQ)["returns"].loc[start:],
              "SPY": spy.loc[start:]}
    rows = []
    for nm, r in series.items():
        h = len(r) // 2
        m, i, o = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
        rows.append(dict(book=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                         IS_Sharpe=i["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"],
                         OOS_MaxDD=o["MaxDD"]))
    B = pd.DataFrame(rows).set_index("book")
    s, b = B.loc["SPY"], B.loc["RULES v2 (live)"]
    kp = []
    for nm, r in B.iterrows():
        kp.append(dict(book=nm,
                       pass4a=int(r.H1 > b.H1 and r.H2 > b.H2 and r.MaxDD >= b.MaxDD),
                       pass4b=int(r.H1 > s.H1 and r.H2 > s.H2
                                  and r.OOS_Sharpe > s.OOS_Sharpe
                                  and r.MaxDD >= 0.60 * s.MaxDD
                                  and r.CAGR >= 0.70 * s.CAGR),
                       bar_s_DD=0.60 * s.MaxDD, bar_s_CAGR=0.70 * s.CAGR,
                       bar_s_OOS=s.OOS_Sharpe))
    return B.reset_index(), pd.DataFrame(kp)


def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 523 (cloud, 2026-09-11) - RESTATE IDEA 276's 26-FILE UPPER BOUND ON THE HEADLINE")
    P("BLOCK, WITH INSTRUMENT SPELLINGS OF THE PROPERTY WORDS EXCLUDED")
    P("=" * 104)

    m276 = load_mod(I276, "i276")
    P(f"[G1] idea 276's regexes imported verbatim from {I276.name}:")
    for nm in ("SMALL_TOK", "LARGE_TOK", "PROP_TOK", "CMP_TOK"):
        P(f"       {nm:<10} {getattr(m276, nm).pattern[:96]}")

    P("")
    c276_all = corpus_at(I276_SHA)
    own = [k for k in c276_all if k.startswith("2026-09-06_is-breadth-a-small-cap-dummy")]
    c276 = {k: v for k, v in c276_all.items() if k not in own}
    got_all, _ = score(c276_all, m276, "WHOLE FILE", 10 ** 9, False)
    P(f"[G2a] idea 276's OWN rule on the tree at its OWN commit, SELF INCLUDED: {got_all}")
    P(f"[G2a] that is +1 on EVERY column, and the extra file is idea 276's own output "
      f"({own}).  A census that globs `research/backtests/*.md` counts ITSELF once it is "
      f"committed - so a published census number and the same number re-derived from the "
      f"record afterwards can never agree unless the census self-excludes.  Reported, not "
      f"corrected silently.")
    got, D276 = score(c276, m276, "WHOLE FILE", 10 ** 9, False)
    P(f"[G2] idea 276's OWN rule on idea 276's OWN corpus, SELF EXCLUDED (tree "
      f"{I276_SHA[:9]}, read from git): {got}")
    P(f"       published:                                                                "
      f"{PUBLISHED}")
    hits = {k: (got[k] == PUBLISHED[k]) for k in PUBLISHED}
    P(f"[G2] match: {hits}")
    if all(hits.values()):
        P("[G2] REPRODUCTION GATE PASS - every published census number is re-derived exactly, "
          "so any move below is the RESTATEMENT's, not a transcription's.")
    else:
        P("[G2] REPRODUCTION GATE **PARTIAL** - the columns that do not match are reported "
          "as-is and every restatement below is quoted against THIS RUN's RAW column, never "
          "against the published one.")

    ctoday = corpus_today()
    P(f"[G3] TODAY's corpus under the same rule: {len(ctoday)} files vs {len(c276)} at "
      f"{I276_SHA[:9]} - the record grew by {len(ctoday) - len(c276)} "
      f"({(len(ctoday)/max(1,len(c276)) - 1):.0%}); both are scored, never merged.")
    raw_today, _ = score(ctoday, m276, "WHOLE FILE", 10 ** 9, False)
    P(f"[G3] idea 276's rule on TODAY's corpus: {raw_today}")

    # ---- the grid --------------------------------------------------------------------------
    P("")
    P("=" * 104)
    P("THE GRID - P1 window x P2 block rule x {RAW, ROLE-FILTERED} x {both corpora}")
    P("=" * 104)
    rows, detail = [], {}
    for corpus_name, corpus in (("idea276 (292 files)", c276), ("TODAY", ctoday)):
        for block in BLOCKS:
            for w in WINDOWS:
                for rf in (False, True):
                    g, D = score(corpus, m276, block, w, rf)
                    g.update(corpus=corpus_name, block=block,
                             window=("block" if w >= 10 ** 9 else w),
                             role_filter="ROLE-FILTERED" if rf else "RAW")
                    rows.append(g)
                    detail[(corpus_name, block, w, rf)] = D
    G = pd.DataFrame(rows)[["corpus", "block", "window", "role_filter", "files", "cross",
                            "cmp", "prop", "breadth"]]
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    for cn in G.corpus.unique():
        P("")
        P(f"--- corpus: {cn} ---")
        P(G[G.corpus == cn].pivot_table(index=["block", "window"], columns="role_filter",
                                        values=["cross", "cmp", "prop", "breadth"],
                                        aggfunc="first").to_string())

    # the file-level detail for the headline cell
    key = ("idea276 (292 files)", "TITLE+VERDICT", 200, True)
    detail[key].to_csv(OUT / f"{STEM}.census.csv", index=False)
    detail[("idea276 (292 files)", "WHOLE FILE", 10 ** 9, False)].to_csv(
        OUT / f"{STEM}.census_raw.csv", index=False)

    # ---- what the two bounds become ----------------------------------------------------------
    P("")
    P("-" * 104)
    P("WHAT EACH PUBLISHED BOUND BECOMES")
    P("-" * 104)
    base = G[(G.corpus == "idea276 (292 files)") & (G.block == "WHOLE FILE")
             & (G.window == "block") & (G.role_filter == "RAW")].iloc[0]
    P(f"  idea 276 published: cross-cap {PUBLISHED['cross']}, comparison "
      f"{PUBLISHED['cmp']}, panel-property {PUBLISHED['prop']} (UPPER BOUND), "
      f"breadth {PUBLISHED['breadth']} (tight lower bound).")
    P(f"  this run, same rule:  cross-cap {base.cross}, comparison {base['cmp']}, "
      f"panel-property {base['prop']}, breadth {base.breadth}.")
    for block in BLOCKS:
        sub = G[(G.corpus == "idea276 (292 files)") & (G.block == block)]
        for rf in ("RAW", "ROLE-FILTERED"):
            s2 = sub[sub.role_filter == rf]
            P(f"    {block:<16} {rf:<14} cross {list(s2.cross)}  prop "
              f"{list(s2['prop'])}  breadth {list(s2.breadth)}   (windows "
              f"{list(s2.window)})")
    tight = G[(G.corpus == "idea276 (292 files)") & (G.block == "TITLE+VERDICT")
              & (G.window == 200) & (G.role_filter == "ROLE-FILTERED")].iloc[0]
    P("")
    P(f"  >>> TIGHTEST defensible cell (headline block, property within 200 chars of a panel "
      f"token, instrument spellings removed): cross-cap {tight.cross}, "
      f"panel-property **{tight['prop']}**, breadth **{tight.breadth}** "
      f"- against the published {PUBLISHED['prop']} and {PUBLISHED['breadth']}.")
    P(f"  >>> LOOSEST cell (idea 276's own rule): panel-property {base['prop']}, "
      f"breadth {base.breadth}.")
    P(f"  >>> the two bounds therefore span "
      f"{tight['prop']}..{base['prop']} (property) and {tight.breadth}..{base.breadth} "
      f"(breadth) on idea 276's own corpus.")

    # how much of the move is ROLE and how much is SITE, separated
    P("")
    P("  DECOMPOSITION - which of the two defects does the work:")
    for block in BLOCKS:
        r = G[(G.corpus == "idea276 (292 files)") & (G.block == block)
              & (G.window == "block")]
        raw = int(r[r.role_filter == "RAW"]["prop"].iloc[0])
        flt = int(r[r.role_filter == "ROLE-FILTERED"]["prop"].iloc[0])
        P(f"    block={block:<16} ROLE alone REMOVES {raw - flt:2d} files ({raw} -> {flt});"
          f"  SITE alone moves {int(base['prop'])} -> {raw} "
          f"({raw - int(base['prop']):+3d})")

    # ---- rule 8 / KEEP paths -------------------------------------------------------------
    P("")
    P("=" * 104)
    P("RULE 8 (PROTOCOL 8) AND BOTH KEEP PATHS - the book axis")
    P("=" * 104)
    B, KP = book_block()
    B.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    P(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P(KP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"  4a passes {int(KP.pass4a.sum())} of {len(KP)};  "
      f"4b passes {int(KP.pass4b.sum())} of {len(KP)}.")

    P("")
    P("=" * 104)
    P(f"HEADLINE: idea 276's UPPER BOUND of {PUBLISHED['prop']} files becomes "
      f"**{tight['prop']}** and its tight lower bound of {PUBLISHED['breadth']} becomes "
      f"**{tight.breadth}** once the property word must sit in the headline block, within "
      f"200 chars of a panel token, and must not be an instrument spelling.")
    wi = G[(G.corpus == "idea276 (292 files)") & (G.block == "WHOLE FILE")].cross.nunique()
    P(f"          The cross-cap count is WINDOW-invariant ({base.cross} at all four windows, "
      f"{wi} distinct value) but NOT site-invariant: "
      f"{list(G[(G.corpus=='idea276 (292 files)') & (G.window=='block') & (G.role_filter=='RAW')].sort_values('cross', ascending=False).cross)} "
      f"across WHOLE FILE / FIRST 40 / FIRST 20 / TITLE+VERDICT.  So the WINDOW does nothing "
      f"to the 136 and most of the work to the 26: the two bounds are not the same kind of "
      f"number and PROTOCOL should not quote them side by side.")
    rf_cost = int(base['prop']) - int(G[(G.corpus == "idea276 (292 files)")
                                        & (G.block == "WHOLE FILE") & (G.window == "block")
                                        & (G.role_filter == "ROLE-FILTERED")]['prop'].iloc[0])
    P(f"          Of the {int(base['prop']) - int(tight['prop'])}-file fall, the ROLE defect "
      f"the queue named accounts for {rf_cost} and the SITE defect for the other "
      f"{int(base['prop']) - int(tight['prop']) - rf_cost}.")
    P("=" * 104)
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

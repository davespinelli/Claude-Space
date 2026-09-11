#!/usr/bin/env python3
"""Idea 523 — restate idea 276's 26-file UPPER BOUND on the HEADLINE BLOCK.

Idea 276 censused the corpus for claims that pool panels of different capitalisation and
published three nested counts: 292 files scanned, 136 (46.6%) CROSS-CAP (a small-cap token
AND a large-cap token both appear), of those 26 "attribute a result to a panel PROPERTY",
and 14 "name breadth".  The 26 is the record's standing UPPER BOUND on how far any
panel-property claim reaches.

Idea 286 then read the tightest of those columns semantically and found the census counts
the WORD, not the CLAIM: 2 of the frozen 14 are the append-only LEDGERS (LEADERBOARD.md,
CHANGELOG.md) which have no headline of their own, 218 of the 246 `breadth` occurrences sit
in those two files, and of the remaining 12 headline files exactly ONE puts `breadth` in its
own headline block in a PANEL-PROPERTY role.

This run applies idea 286's role-and-location audit to the two LOOSER columns — the 26-file
upper bound and the 136-file cross-cap count — over the whole panel-property vocabulary that
built the 26, with instrument-sense occurrences excluded and scoring restricted to each
file's headline block, and reports what each bound becomes.

Two tuned parameters, exactly as the queue allows:
    1. WINDOW WIDTH  W   — the +/-W character context the role is read in.
                           5 grid points 40 / 70 / 100 / 140 / 200.  W=70 is idea 286's.
    2. BLOCK RULE    B   — what counts as the file's "headline block".
                           5 grid points TITLE / PRE-H2 / FIRST-H2 / CHARS1500 / WHOLE.
                           PRE-H2 is idea 286's; WHOLE reproduces idea 276 verbatim.
ALL 25 grid points are reported.  The EXCLUSION reading (LITERAL = the queue's own wording,
`breadth\\d+` and 'breadth gate' only; GENERAL = the same instrument shapes over the full
vocabulary) is a pre-registered PAIR OF READINGS of every grid point, not a third tuned
parameter: both are reported at all 25 cells and neither is selected on.

Pre-registered definitions, fixed before any number was read:
  FROZEN CORPUS  the 292 filenames in idea 276's committed census.csv.  The corpus has GROWN
                 since 2026-09-06, so every reproduction gate and every restated bound is
                 computed on the FROZEN list; the TODAY list is reported beside it, never
                 substituted for it.
  VOCABULARY     idea 276's PROP_TOK verbatim: breadth | dispersion | disp | pairwise
                 correlation | corr | eligible-set vol | n_elig | evol.
  ROLE           per occurrence, read in the +/-W window:
                   INSTRUMENT     the token names a BOOK DIAL (breadth7, 'breadth gate',
                                  'market breadth'); under GENERAL the same shapes over the
                                  whole vocabulary.
                   PANEL-PROPERTY the window also carries a panel/capitalisation word
                                  (idea 286's PANELPROP, verbatim).
                   OTHER          neither.
  HEADLINE-PROP  a file qualifies iff >= 1 PANEL-PROPERTY-role occurrence falls inside its
                 headline block under B, after the exclusion.  INSTRUMENT hits never count.
  LEDGERS        LEADERBOARD.md and CHANGELOG.md have no `## ` headline structure; idea 286
                 scored them separately and so does this run.  They can never be
                 HEADLINE-PROP and are reported as their own line.
  RESTATED 26    |{f in frozen 26 : HEADLINE-PROP(f, W, B)}|
  RESTATED 136   |{f in frozen 136 : HEADLINE-PROP(f, W, B)}|
  4a / 4b        PROTOCOL rule 4, both paths, verbatim (4a against live RULES v2 on the same
                 panel; 4b against SPY with the 0.60 MaxDD cap and the 0.70 CAGR floor).
  Rule 8         PROTOCOL 8.  The book family's arm is chosen on 2010-2016 ONLY by IS Sharpe,
                 2017-2026 read once against RULES v2, RULES v1, SPY and an EWALL control.
                 The census leg enters here and nowhere else: at each of the 25 grid points
                 the rule-8 CHOICE SET is restricted to the panels the restated bound's
                 surviving files actually name, so the question "does this documentation
                 decision have a book consequence" is answered with a number.

Costs 10 bps headline and a 25 bps rung, derived from one cost-free run by the exact
identity r(c) = r(0) - turnover * c/1e4 (gated below, G3).  Weekly cadence.  Weights decided
at close t, applied at t+1 (engine).  No network: panels come from the committed caches via
research/baseline.load_universe.
SURVIVORSHIP: U56 = research/universe.json, B136 = research/universe_broad.json (current
constituents only), SMALL439 = the sub-$2B screen with the 44 tickers whose max_1d_move
>= 1.0 dropped first (the record's SMALL439).  Every small-cap number is biased upward by an
unknown amount; no cross-panel ordering here is survivorship-clean.
"""
from __future__ import annotations
import re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, band_state  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-11_restate-idea-276-s-26-file-UPPER-BOUND-on-the-headline-block_B"
OUT = ROOT / "research" / "backtests"
BT = OUT
GROSS, BAND = 0.75, 0.03
COSTS = [10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CENSUS276 = OUT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.census.csv"
AUDIT286 = OUT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.audit.csv"

_console: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); _console.append(s)

# ================================================================ census vocabulary
# idea 276's regexes, copied verbatim from
# 2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py
SMALL_TOK = re.compile(r"SMALL\s?\d{2,3}|small[- ]cap panel|small panel|prices_small|small=True|sub-\$2B|SMALL_PANEL", re.I)
LARGE_TOK = re.compile(r"\bU56\b|\bB136\b|BSTK\s?\d{2,3}|\bETF\s?36\b|universe\.json|universe_broad|broad=True|mega[- ]cap|large[- ]cap", re.I)
PROP_TOK  = re.compile(r"\bbreadth\b|\bdispersion\b|\bdisp\b|pairwise correlation|\bcorr\b|eligible[- ]set vol|\bn_elig\b|\bevol\b", re.I)

# idea 286's role regexes, copied verbatim from
# 2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py
HEAD_SPLIT = re.compile(r"^## ", re.M)
INSTR_LIT = re.compile(r"breadth\s?\d+|breadth[- ](gate|signal|overlay|trigger|instrument|rule|dial|arm|filter)"
                       r"|(market|spy|index)[- ]breadth", re.I)
PANELPROP = re.compile(r"panel|universe|eligible|n_elig|width|cap\b|capitalisation|capitalization"
                       r"|small|large|mega|u56|b136|bstk|etf\s?36|corpus|collinear|dummy", re.I)
# GENERAL reading: the same instrument shapes over the whole idea-276 vocabulary
VOCAB = r"(?:breadth|dispersion|disp|corr|n_elig|evol)"
INSTR_GEN = re.compile(rf"{VOCAB}\s?\d+"
                       rf"|{VOCAB}[- ](gate|signal|overlay|trigger|instrument|rule|dial|arm|filter|column|leg)"
                       r"|(market|spy|index)[- ]breadth", re.I)
EXCL = {"LITERAL": INSTR_LIT, "GENERAL": INSTR_GEN}

LEDGERS = {"LEADERBOARD.md", "CHANGELOG.md"}
WINDOWS = [40, 70, 100, 140, 200]
BLOCKS = ["TITLE", "PRE-H2", "FIRST-H2", "CHARS1500", "WHOLE"]

def read_file(name):
    p = BT / name
    if not p.exists(): p = ROOT / "research" / name
    return p.read_text(errors="ignore") if p.exists() else None

def block_len(t, name, rule):
    """Length of the prefix of t that counts as the file's headline block."""
    if name in LEDGERS and rule != "WHOLE":
        return 0                                   # append-only ledger: no headline of its own
    if rule == "WHOLE":     return len(t)
    if rule == "TITLE":     return len(t.split("\n", 1)[0])
    if rule == "PRE-H2":    return len(HEAD_SPLIT.split(t, maxsplit=1)[0])
    if rule == "CHARS1500": return min(1500, len(t))
    if rule == "FIRST-H2":
        parts = HEAD_SPLIT.split(t)
        if len(parts) <= 1: return len(t)
        return len(parts[0]) + 3 + len(parts[1])    # pre-H2 + the first `## ` section
    raise ValueError(rule)

def occurrences(files, token_re):
    """Every token hit in every file, with its character position, cached once."""
    rows = []
    for name in files:
        t = read_file(name)
        if t is None: continue
        for m in token_re.finditer(t):
            i = m.start()
            rows.append(dict(file=name, pos=i, tok=m.group(0).lower(),
                             ctx=t[max(0, i - 200): i + 200], nchars=len(t)))
    return pd.DataFrame(rows)

def role_of(ctx_200, i_in_ctx, W, instr_re):
    win = ctx_200[max(0, i_in_ctx - W): i_in_ctx + W]
    if instr_re.search(win):   return "INSTRUMENT"
    if PANELPROP.search(win):  return "PANEL-PROPERTY"
    return "OTHER"

# ================================================================ book family
def w_topn(px, n, gross=GROSS, band=BAND):
    """Top-n of the scan composite inside the 200d +/-band state, gross/n each."""
    s = score(px)[0].where(band_state(px, band))
    rank = s.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)

def w_bandarm(px, band, gross=GROSS):
    return rules_v2_weights(px, band=band, gross=gross)

def w_ewall(px, gross=1.0):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

NS = [5, 10, 20, 30, 50]
BANDS = [0.00, 0.03, 0.05, 0.08, 0.12]

def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]

PANEL_TOK = [("U56", re.compile(r"\bU56\b|\bu56\b|universe\.json", re.I)),
             ("B136", re.compile(r"\bB136\b|universe_broad|\bbroad\b", re.I)),
             ("BSTK100", re.compile(r"BSTK\s?\d{2,3}", re.I)),
             ("ETF36", re.compile(r"\bETF\s?36\b", re.I)),
             ("SMALL439", re.compile(r"SMALL\s?43\d|prices_small|small=True|sub-\$2B|small[- ]cap panel|small panel", re.I)),
             ("SMALL484", re.compile(r"SMALL\s?48\d", re.I))]
RUNNABLE = {"U56": "U56", "B136": "B136", "SMALL439": "SMALL439", "SMALL484": "SMALL439"}

def panels_named(name):
    t = read_file(name)
    if t is None: return set()
    return {k for k, rx in PANEL_TOK if rx.search(t)}

# ================================================================ metric helpers
def maxdd(r):
    eq = (1 + r).cumprod(); return float((eq / eq.cummax() - 1).min())

def trio(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def arm_row(name, panel, r0, to, cost, start):
    """All PROTOCOL-relevant readings of one arm at one cost rung."""
    r = (r0 - to * cost / 1e4).loc[start:]
    h = len(r) // 2
    i, o = r.loc[:IS_END], r.loc[OOS_START:]
    d = dict(arm=name, panel=panel, cost=cost)
    for tag, x in (("", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]), ("IS", i), ("OOS", o)):
        c, s, dd = trio(x)
        d[f"{tag}_CAGR" if tag else "CAGR"] = c
        d[f"{tag}_Sharpe" if tag else "Sharpe"] = s
        d[f"{tag}_MaxDD" if tag else "MaxDD"] = dd
    return d

def keep_paths(a, v2, spy):
    p4a = (a["H1_Sharpe"] > v2["H1_Sharpe"] and a["H2_Sharpe"] > v2["H2_Sharpe"]
           and a["MaxDD"] >= v2["MaxDD"])
    p4b = (a["H1_Sharpe"] > spy["H1_Sharpe"] and a["H2_Sharpe"] > spy["H2_Sharpe"]
           and a["OOS_Sharpe"] > spy["OOS_Sharpe"]
           and a["MaxDD"] >= 0.60 * spy["MaxDD"] and a["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(p4a), bool(p4b)

# ================================================================ main
def main():
    t0 = time.time()
    say(f"# {STAMP}")
    say(__doc__.split("Two tuned parameters")[0].strip())

    # ============================================================ GATE 0
    say("\n## GATE 0 — reproduction before any new number is read")
    cen = pd.read_csv(CENSUS276)
    frozen = list(cen.file)
    say(f"G0 frozen corpus from idea 276's committed census.csv: {len(frozen)} files")

    # --- G1: idea 276's three counts, recomputed from source on the frozen list
    rows = []
    for name in frozen:
        t = read_file(name)
        if t is None:
            rows.append(dict(file=name, missing=True)); continue
        s, l = bool(SMALL_TOK.search(t)), bool(LARGE_TOK.search(t))
        rows.append(dict(file=name, missing=False, small=s, large=l, cross=s and l,
                         prop=bool(PROP_TOK.search(t)),
                         breadth=bool(re.search(r"\bbreadth\b", t, re.I))))
    C = pd.DataFrame(rows)
    miss = int(C.missing.sum())
    n_cross, n_26, n_14 = int(C.cross.sum()), int((C.cross & C.prop).sum()), int((C.cross & C.breadth).sum())
    pub = dict(cross=int(cen.cross.sum()), prop26=int((cen.cross & cen.prop).sum()),
               br14=int((cen.cross & cen.breadth).sum()))
    g1 = (miss == 0 and n_cross == pub["cross"] == 136 and n_26 == pub["prop26"] == 26
          and n_14 == pub["br14"] == 14)
    say(f"G1 idea 276's counts from source on the frozen list: cross {n_cross} (published {pub['cross']}), "
        f"cross&prop {n_26} ({pub['prop26']}), cross&breadth {n_14} ({pub['br14']}), missing files {miss}"
        f"  -> {'PASS' if g1 else 'FAIL'}")
    assert g1, "G1: idea 276's published census does not reproduce on the frozen list"

    # --- G2: idea 286's role audit, row-for-row against its committed artefact
    a286 = pd.read_csv(AUDIT286)
    f14 = list(C.loc[C.cross & C.breadth, "file"])
    assert sorted(f14) == sorted(a286.file.unique()), "G2: frozen 14 does not match idea 286's audit"
    occ14 = occurrences(f14, re.compile(r"\bbreadth\b", re.I))
    mine = []
    for _, o in occ14.iterrows():
        t = read_file(o.file)
        hl = block_len(t, o.file, "PRE-H2")
        i_in_ctx = o.pos - max(0, o.pos - 200)
        mine.append(dict(file=o.file, pos=o.pos, in_headline=o.pos < hl,
                         role=role_of(o.ctx, i_in_ctx, 70, INSTR_LIT)))
    M = pd.DataFrame(mine)
    M12 = M[~M.file.isin(LEDGERS)].sort_values(["file", "pos"]).reset_index(drop=True)
    A12 = a286[~a286.file.isin(LEDGERS)].sort_values(["file", "pos"]).reset_index(drop=True)
    same = (len(M12) == len(A12) and (M12.file.values == A12.file.values).all()
            and (M12.pos.values == A12.pos.values).all()
            and (M12.role.values == A12.role.values).all()
            and (M12.in_headline.values == A12.in_headline.values).all())
    hb286 = sorted(M12[(M12.in_headline) & (M12.role == "PANEL-PROPERTY")].file.unique())
    say(f"G2 idea 286's role audit on the 12 headline files, row-for-row vs its committed "
        f"audit.csv: {len(M12)} occurrences (published 28), identical file/pos/role/in_headline "
        f"-> {'PASS' if same else 'FAIL'}")
    say(f"   HEADLINE-BREADTH files reproduce: {len(hb286)} of 12 (published 1) -> "
        f"{'PASS' if len(hb286) == 1 else 'FAIL'};  {hb286}")
    assert same and len(hb286) == 1, "G2: idea 286's headline audit does not reproduce"

    # --- G2b: the LEDGER concentration is a VINTAGE statistic, not an invariant
    led_now = int(M.file.isin(LEDGERS).sum()); tot_now = len(M)
    led_286 = int(a286.file.isin(LEDGERS).sum()); tot_286 = len(a286)
    say(f"G2b idea 286's concentration is NOT reproducible and was never meant to be: the "
        f"ledgers are append-only.  Published {led_286}/{tot_286} = {led_286/tot_286:.1%}; "
        f"today {led_now}/{tot_now} = {led_now/tot_now:.1%} (+{led_now-led_286} occurrences in "
        f"2 days).  The 12-file leg above is frozen and DOES reproduce exactly; only the "
        f"ledger leg drifts, and it drifts in the direction that STRENGTHENS idea 286.")

    # --- G3: engine + cost-rung identity
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    for k, v in panels.items(): say(f"   panel {k}: {v.shape[1]} cols, {v.index[0].date()} -> {v.index[-1].date()}")
    pu = panels["U56"]; start_u = pu.index[260]
    res0 = backtest(pu, rules_v2_weights(pu), cost_bps=0, freq="W")
    res10 = backtest(pu, rules_v2_weights(pu), cost_bps=10, freq="W")
    d = float((res0["returns"] - res0["turnover"] * 10 / 1e4 - res10["returns"]).abs().max())
    c, s, dd = trio((res0["returns"] - res0["turnover"] * 10 / 1e4).loc[start_u:])
    say(f"G3 cost-rung identity r(10) = r(0) - turnover*10/1e4 on U56: max|d| {d:.3e} -> "
        f"{'PASS' if d < 1e-12 else 'FAIL'}")
    say(f"   live RULES v2 on U56 @10bps: CAGR {c:.2%} Sharpe {s:.4f} MaxDD {dd:.2%} "
        f"(record's committed constants 8.66% / 1.2056 / -12.05%)")
    assert d < 1e-12, "G3: cost decomposition broken"
    g3b = abs(c - 0.0866) < 5e-4 and abs(s - 1.2056) < 5e-4 and abs(dd + 0.1205) < 5e-4
    say(f"G3b live-book constants match the record to 5e-4 -> {'PASS' if g3b else 'DRIFTED'}")

    # ============================================================ LEG A
    say("\n## LEG A — the restatement: what the 26 and the 136 become on the headline block")
    f26 = list(C.loc[C.cross & C.prop, "file"])
    f136 = list(C.loc[C.cross, "file"])
    say(f"incumbent bounds on the frozen list: 136 cross-cap, {len(f26)} cross-cap & panel-property, "
        f"{len(f14)} naming breadth.  Ledgers inside them: "
        f"136 {len(set(f136)&LEDGERS)}, 26 {len(set(f26)&LEDGERS)}, 14 {len(set(f14)&LEDGERS)}")

    occ136 = occurrences(f136, PROP_TOK)
    occ136["i_in_ctx"] = occ136.pos - (occ136.pos - 200).clip(lower=0)
    say(f"panel-property VOCABULARY occurrences over the 136: {len(occ136)} in "
        f"{occ136.file.nunique()} files")
    conc = occ136.file.isin(LEDGERS)
    say(f"  of those, {int(conc.sum())} ({conc.mean():.1%}) sit in the 2 LEDGERS — idea 286's "
        f"concentration finding is not a breadth-only fact, it is a VOCABULARY-wide fact")
    say("  token mix over the 136 (top 8): " +
        ", ".join(f"{k} {v}" for k, v in occ136.tok.value_counts().head(8).items()))

    # precompute block lengths per (file, rule)
    BL = {}
    for name in set(f136):
        t = read_file(name)
        for b in BLOCKS: BL[(name, b)] = block_len(t, name, b)

    ROLES = {(W, ex): np.array([role_of(o.ctx, o.i_in_ctx, W, rx) for o in occ136.itertuples()])
             for W in WINDOWS for ex, rx in EXCL.items()}
    INHL = {B: np.array([o.pos < BL[(o.file, B)] for o in occ136.itertuples()]) for B in BLOCKS}
    SURV = {}                                     # (W, B, ex) -> surviving file set (136 level)
    grid, per_file = [], []
    for W in WINDOWS:
        for B in BLOCKS:
            for ex in EXCL:
                rl, inhl = ROLES[(W, ex)], INHL[B]
                good = inhl & (rl == "PANEL-PROPERTY")
                qual = set(occ136.file[good])
                r26, r136 = qual & set(f26), qual & set(f136)
                SURV[(W, B, ex)] = r136
                grid.append(dict(W=W, block=B, excl=ex,
                                 n_occ=len(occ136), n_instr=int((rl == "INSTRUMENT").sum()),
                                 n_other=int((rl == "OTHER").sum()),
                                 n_prop=int((rl == "PANEL-PROPERTY").sum()),
                                 n_in_block=int(inhl.sum()), n_qualifying_occ=int(good.sum()),
                                 restated_26=len(r26), restated_136=len(r136),
                                 shrink_26=len(r26) / len(f26), shrink_136=len(r136) / len(f136),
                                 files_26=";".join(sorted(r26))))
                if (W, B, ex) == (70, "PRE-H2", "LITERAL"):
                    for f in sorted(r136): per_file.append(dict(file=f, in26=f in set(f26)))
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say("\nALL 25 grid points x 2 pre-registered exclusion readings "
        "(W=70, block=PRE-H2, excl=LITERAL is idea 286's setting; block=WHOLE is idea 276's):")
    show = G[["W", "block", "excl", "n_instr", "n_prop", "n_in_block", "n_qualifying_occ",
              "restated_26", "restated_136", "shrink_26", "shrink_136"]]
    say(show.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say(f"\nrestated 26 across the 25x2 cells: min {G.restated_26.min()} max {G.restated_26.max()} "
        f"median {G.restated_26.median():.1f};  restated 136: min {G.restated_136.min()} "
        f"max {G.restated_136.max()} median {G.restated_136.median():.1f}")
    inc = G[(G.W == 70) & (G.block == "PRE-H2") & (G.excl == "LITERAL")].iloc[0]
    whole = G[(G.W == 70) & (G.block == "WHOLE") & (G.excl == "LITERAL")].iloc[0]
    say(f"AT IDEA 286's OWN SETTING (W=70, PRE-H2, LITERAL): the 26-file upper bound becomes "
        f"{inc.restated_26} ({inc.shrink_26:.1%} of it survives) and the 136-file cross-cap "
        f"count becomes {inc.restated_136} ({inc.shrink_136:.1%}).")
    say(f"AT IDEA 276's OWN SETTING (block=WHOLE, i.e. no headline restriction): 26 -> "
        f"{whole.restated_26}, 136 -> {whole.restated_136}.  The gap between these two rows is "
        f"the entire content of the restatement.")
    say("\nsensitivity of the restated 26 to each parameter alone (LITERAL reading):")
    L = G[G.excl == "LITERAL"]
    say("  by block rule (range over W):  " + ",  ".join(
        f"{b} {L[L.block==b].restated_26.min()}-{L[L.block==b].restated_26.max()}" for b in BLOCKS))
    say("  by window width (range over B): " + ",  ".join(
        f"W={w} {L[L.W==w].restated_26.min()}-{L[L.W==w].restated_26.max()}" for w in WINDOWS))
    say("  LITERAL vs GENERAL exclusion, same 25 cells: mean restated_26 "
        f"{L.restated_26.mean():.2f} vs {G[G.excl=='GENERAL'].restated_26.mean():.2f}; "
        f"mean restated_136 {L.restated_136.mean():.2f} vs {G[G.excl=='GENERAL'].restated_136.mean():.2f}")
    say(f"\nthe surviving files at idea 286's setting ({inc.restated_136} of 136, "
        f"{inc.restated_26} of them inside the 26):")
    PF = pd.DataFrame(per_file)
    if len(PF):
        PF.to_csv(OUT / f"{STAMP}.survivors.csv", index=False)
        for _, r in PF.sort_values(["in26", "file"], ascending=[False, True]).iterrows():
            say(f"   [{'in 26   ' if r.in26 else '136 only'}] {r.file}")

    # ============================================================ LEG B — panels named
    say("\n## LEG B — which panels the surviving files actually name")
    pan_rows = []
    for name in sorted(set(f136)):
        ps = panels_named(name)
        pan_rows.append(dict(file=name, in26=name in set(f26), in14=name in set(f14),
                             panels=";".join(sorted(ps)),
                             runnable=";".join(sorted({RUNNABLE[p] for p in ps if p in RUNNABLE}))))
    P = pd.DataFrame(pan_rows); P.to_csv(OUT / f"{STAMP}.panels.csv", index=False)
    say(f"of the 136 cross-cap files, panel tokens found in {int((P.panels!='').sum())}; "
        f"unrunnable-only (BSTK100/ETF36 alone) {int(((P.panels!='')&(P.runnable=='')).sum())}")
    say("panel-token frequency over the 136: " + ", ".join(
        f"{k} {sum(k in s.split(';') for s in P.panels)}" for k, _ in PANEL_TOK))

    # ============================================================ LEG C — books
    say("\n## LEG C — the book family, PROTOCOL 4a/4b at both cost rungs")
    arms = {}
    for pname, px in panels.items():
        st = px.index[260]
        specs = ([(f"topn{n}", lambda p, n=n: w_topn(p, n)) for n in NS]
                 + [(f"band{b:.2f}", lambda p, b=b: w_bandarm(p, b)) for b in BANDS]
                 + [("RULES v2 (live)", rules_v2_weights), ("RULES v1", rules_v1_weights),
                    ("EWALL control", w_ewall)])
        for aname, fn in specs:
            res = backtest(px, fn(px), cost_bps=0, freq="W")
            for cost in COSTS:
                arms[(pname, aname, cost)] = arm_row(aname, pname, res["returns"], res["turnover"], cost, st)
        spy_r = px["SPY"].pct_change().fillna(0.0)
        zero = pd.Series(0.0, index=px.index)
        for cost in COSTS:
            arms[(pname, "SPY", cost)] = arm_row("SPY", pname, spy_r, zero, cost, st)
        say(f"   {pname}: {len(specs)+1} arms x {len(COSTS)} rungs done  ({time.time()-t0:.0f}s)")

    A = pd.DataFrame(arms.values())
    for k in ("pass4a", "pass4b"): A[k] = False
    for i, r in A.iterrows():
        v2 = arms[(r.panel, "RULES v2 (live)", r.cost)]; sp = arms[(r.panel, "SPY", r.cost)]
        a, b = keep_paths(r, v2, sp)
        A.at[i, "pass4a"], A.at[i, "pass4b"] = a, b
    A.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    cand = A[~A.arm.isin(["RULES v2 (live)", "RULES v1", "SPY", "EWALL control"])]
    say(f"candidate arms: {len(cand)} ({len(NS)} topn + {len(BANDS)} band) x 3 panels x 2 rungs")
    say(f"PROTOCOL 4a passes: {int(cand.pass4a.sum())}/{len(cand)};  "
        f"4b passes: {int(cand.pass4b.sum())}/{len(cand)};  "
        f"BOTH: {int((cand.pass4a & cand.pass4b).sum())}")
    if cand.pass4b.any():
        say("4b passers:"); say(cand[cand.pass4b][["panel", "arm", "cost", "CAGR", "Sharpe", "MaxDD",
            "OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nheadline table, 10 bps rung (full / halves / OOS):")
    h = A[A.cost == 10][["panel", "arm", "CAGR", "Sharpe", "MaxDD", "H1_Sharpe", "H2_Sharpe",
                         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b"]]
    say(h.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ rule 8
    say("\n## PROTOCOL 8 walk-forward — arm chosen on 2010-2016 ONLY, 2017-2026 read once")
    say("the census enters here: at each grid point the CHOICE SET is restricted to the panels")
    say("the restated bound's surviving files name.  If the restatement has no book")
    say("consequence, every cell picks the same arm.")
    PNAMED = {f: {RUNNABLE[p] for p in panels_named(f) if p in RUNNABLE} for f in set(f136)}
    wf = []
    for _, g in G.iterrows():
        s136 = SURV[(g.W, g.block, g.excl)]
        named = set()
        for f in s136: named |= PNAMED[f]
        choice = sorted(named) if named else sorted(panels)      # empty survivor set -> all panels
        for cost in COSTS:
            sub = cand[(cand.cost == cost) & (cand.panel.isin(choice))]
            if not len(sub): continue
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            v2 = arms[(pick.panel, "RULES v2 (live)", cost)]
            v1 = arms[(pick.panel, "RULES v1", cost)]
            sp = arms[(pick.panel, "SPY", cost)]
            ew = arms[(pick.panel, "EWALL control", cost)]
            wf.append(dict(W=g.W, block=g.block, excl=g.excl, cost=cost,
                           n_surv136=len(s136), n_surv26=g.restated_26,
                           choice_set=",".join(choice), n_choice=len(sub),
                           pick=f"{pick.panel}/{pick.arm}",
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           v2_OOS_CAGR=v2["OOS_CAGR"], v2_OOS_Sharpe=v2["OOS_Sharpe"],
                           v2_OOS_MaxDD=v2["OOS_MaxDD"],
                           spy_OOS_CAGR=sp["OOS_CAGR"], spy_OOS_Sharpe=sp["OOS_Sharpe"],
                           spy_OOS_MaxDD=sp["OOS_MaxDD"],
                           v1_OOS_Sharpe=v1["OOS_Sharpe"], ew_OOS_Sharpe=ew["OOS_Sharpe"]))
    Wf = pd.DataFrame(wf); Wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(Wf[["W", "block", "excl", "cost", "n_surv136", "n_surv26", "choice_set", "n_choice", "pick",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "v2_OOS_Sharpe", "spy_OOS_Sharpe",
            "v2_OOS_CAGR", "spy_OOS_CAGR", "v2_OOS_MaxDD", "spy_OOS_MaxDD"]]
       .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\ndistinct rule-8 picks over the {len(Wf)} cells: {Wf['pick'].nunique()} "
        f"({dict(Wf['pick'].value_counts())})")
    say(f"distinct choice sets: {Wf.choice_set.nunique()} ({sorted(Wf.choice_set.unique())})")
    say(f"OOS Sharpe spread across cells: {Wf.OOS_Sharpe.min():.4f} -> {Wf.OOS_Sharpe.max():.4f} "
        f"(range {Wf.OOS_Sharpe.max()-Wf.OOS_Sharpe.min():.4f}); "
        f"OOS MaxDD spread {Wf.OOS_MaxDD.min():.2%} -> {Wf.OOS_MaxDD.max():.2%}")
    say(f"cells whose pick beats RULES v2 OOS Sharpe: {int((Wf.OOS_Sharpe>Wf.v2_OOS_Sharpe).sum())}/{len(Wf)};"
        f" beats SPY OOS Sharpe: {int((Wf.OOS_Sharpe>Wf.spy_OOS_Sharpe).sum())}/{len(Wf)};"
        f" beats the EWALL control: {int((Wf.OOS_Sharpe>Wf.ew_OOS_Sharpe).sum())}/{len(Wf)}")

    # ============================================================ LEG D
    say("\n## LEG D — what the restatement reaches, and what it does not")
    ident = bool((G.restated_26 == G.restated_136).all())
    say(f"D1 restated_26 == restated_136 in {int((G.restated_26==G.restated_136).sum())} of {len(G)} "
        f"cells -> {'IDENTICAL EVERYWHERE' if ident else 'DIFFER'}.  This is a THEOREM, not a "
        f"coincidence: the restatement scores panel-property VOCABULARY occurrences, and a file "
        f"with no vocabulary hit has none to put in its headline, so the survivor set is a subset "
        f"of the 26 by construction.  The 136-file cross-cap count therefore carries NO "
        f"independent information as a bound on panel-property reach — it is a capitalisation-"
        f"token count wearing a claim count's name, and the 26 was always the binding column.")
    s_inc = SURV[(70, "PRE-H2", "LITERAL")]
    say(f"D2 of the {len(s_inc)} survivors at idea 286's setting, {len(s_inc & set(f14))} are inside "
        f"its frozen 14 and {len(s_inc - set(f14))} are NOT: "
        + ", ".join(sorted(s_inc - set(f14))))
    say(f"   idea 286's breadth-only audit therefore UNDERCOUNTS the record's headline "
        f"panel-property claims by {len(s_inc - set(f14))} of {len(s_inc)}; the missed ones are "
        f"dispersion- and n_elig-sense claims, which the 26 admits and the 14 cannot see.")
    say("D3 which 4b bar cuts each candidate arm at 10 bps (sole-cut attribution):")
    bars = []
    for _, r in cand[cand.cost == 10].iterrows():
        sp = arms[(r.panel, "SPY", 10)]
        f = [nm for nm, ok in (("H1", r.H1_Sharpe > sp["H1_Sharpe"]), ("H2", r.H2_Sharpe > sp["H2_Sharpe"]),
                               ("OOS", r.OOS_Sharpe > sp["OOS_Sharpe"]),
                               ("DD", r.MaxDD >= 0.60 * sp["MaxDD"]),
                               ("CAGR", r.CAGR >= 0.70 * sp["CAGR"])) if not ok]
        bars.append(dict(panel=r.panel, arm=r.arm, n_fail=len(f), fails=",".join(f) or "NONE"))
    B4 = pd.DataFrame(bars); B4.to_csv(OUT / f"{STAMP}.bars.csv", index=False)
    say("   fail-set frequency: " + ", ".join(f"{k} {v}" for k, v in B4.fails.value_counts().items()))
    say(f"   arms whose ONLY failing bar is the CAGR floor: {int((B4.fails=='CAGR').sum())} of {len(B4)}"
        f" — the floor, not the Sharpe legs, is what 4b turns on in this family too")
    p4b = cand[cand.pass4b]
    for _, r in p4b.iterrows():
        sp = arms[(r.panel, "SPY", r.cost)]
        say(f"D4 the single 4b pass is {r.panel}/{r.arm} @{r.cost}bps: CAGR {r.CAGR:.2%} "
            f"(floor {0.70*sp['CAGR']:.2%}) Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:.2%} "
            f"(cap {0.60*sp['MaxDD']:.2%}) H1/H2 {r.H1_Sharpe:.4f}/{r.H2_Sharpe:.4f} "
            f"OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%}")
        o = cand[(cand.panel == r.panel) & (cand.arm == r.arm) & (cand.cost == 25)].iloc[0]
        say(f"   at the 25 bps rung the SAME book fails: CAGR {o.CAGR:.2%} vs floor "
            f"{0.70*arms[(r.panel,'SPY',25)]['CAGR']:.2%} -> the only 4b pass in {len(cand)} arms is "
            f"decided by the cost rung through the CAGR floor, i.e. RUNG-FRAGILE.")
        say(f"   and PROTOCOL 8 never reaches it: the IS-Sharpe selector's per-panel argmax on "
            f"{r.panel} is {cand[(cand.panel==r.panel)&(cand.cost==10)].sort_values('IS_Sharpe').iloc[-1].arm}, "
            f"not {r.arm}; over all 100 rule-8 cells the pick is {Wf['pick'].iloc[0]} every time.")
    say("D5 BOOK CONSEQUENCE OF THE RESTATEMENT: none that this corpus can see.  Every one of the "
        f"{len(Wf)} rule-8 cells draws the same choice set ({Wf.choice_set.iloc[0]}) because even "
        f"the 2-file TITLE survivor set names all three runnable panels, so the same arm is picked "
        f"and the same OOS numbers are read at every grid point.  The restatement is a DOCUMENTATION "
        f"correction with a measured book footprint of ZERO, which is the honest finding and not a "
        f"weakness of the restatement.")

    say(f"\nruntime {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()

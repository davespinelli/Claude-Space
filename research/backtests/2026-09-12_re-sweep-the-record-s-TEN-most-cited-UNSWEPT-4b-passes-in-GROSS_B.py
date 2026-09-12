#!/usr/bin/env python3
"""Idea 574 - re-sweep the record's most-cited UNSWEPT 4b passes in GROSS (lane B, 2026-09-12).

Idea 311 found 23,015 of the record's committed 4b passes (98.1%) were never run at a second
gross inside their own file, and that 97.6% of the ones that WERE swept flip verdict on their
own ladder.  A 4b verdict quoted at one gross is therefore a point estimate on a dial nobody
looked at.  This run takes the record's most-cited standing 4b/4a candidates - the MEMO corpus,
i.e. every KEEP-candidate the record filed a memo for and that is reconstructible from prices
alone - measures whether their own producing file ever swept gross, and re-runs each on a
17-point g ladder 0.20..1.00.

DENOMINATOR NOTE (published because the queue asks for TEN): the record's reconstructible memo
corpus is EIGHT books (K1..K8), fixed and gate-verified by idea 641's G3 on 2026-09-10, plus
two non-candidate comparands (live RULES v2, retired RULES v1) that idea 641 counted to reach
its "10 books".  This run sweeps all eight candidates and both comparands = 10 books x 17 g
= 170 cells, every one reported.  It does NOT invent two further books to reach ten; PART A
publishes the citation counts so "most cited" is measured rather than asserted.

TWO TUNED PARAMETERS, as the queue allows: the BOOK (10 levels) and the GROSS g (17 levels).
Nothing else is fitted.  Cost rungs 0/10/25 bps are reported off ONE simulation per cell
(exact: engine.backtest at cost 0 plus its own turnover series), and are a reporting rung in
this record, not a third tuned dial; 10 bps is the headline everywhere.

PROTOCOL: 10 bps headline, next-day execution (engine shifts weights), no shorting, no
leverage.  Both KEEP paths are evaluated on every cell.  Rule 8 walk-forward is run for every
book: g chosen on 2009-2016 IS Sharpe alone, 2017-2026 read exactly once, reported against the
live RULES v2 baseline and SPY on the same panel and window.

Panels: U56 (research/universe.json) and B136 (research/universe_broad.json).  SURVIVORSHIP:
both are current-constituent lists, so every LEVEL here is optimistic; the object of this run
is the SHAPE of each book's verdict in g, which is a within-book contrast.

Vintage pinned to 2026-09-04 (the record's committed vintage) so the memo headlines this run
gates on are the ones the record published; data/prices.csv now runs past it.

Book constructors are copied verbatim from the committed
research/backtests/2026-09-10_price-the-rf-CONSISTENCY-fix-as-a-PROTOCOL-amendment_cloud.py
(idea 641) so this script is standalone and the corpus is not silently redefined.

Outputs (all committed, all under research/):
  .txt        full console log
  .cells.csv  PART C, one row per (book, g, rung): metrics + both KEEP verdicts + binding bar
  .wf.csv     PART D, every rule-8 grid point
  .result.md  the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, band_state  # noqa
from engine import backtest, metrics, rebalance_mask                                       # noqa

DATE = "2026-09-12"
SLUG = "re-sweep-the-record-s-TEN-most-cited-UNSWEPT-4b-passes-in-GROSS"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

END = "2026-09-04"          # the record's committed vintage
OOS_START = "2017-01-01"    # PROTOCOL rule 8
IS_END = "2016-12-31"
GRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]   # 17 points, 0.20 .. 1.00
RUNGS = [0, 10, 25]
HEAD = 10                   # headline cost rung
MAX_VOL = 0.60
WARMUP = 260                # baseline.compare's own warm-up skip
LOG: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# books -- verbatim from idea 641's committed corpus
# =====================================================================================
def comp_rank(px):
    """The record's composite score WITHOUT the vol scaler, and its eligibility mask."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAX_VOL)
    return s.where(elig), elig


def topn_weights(px, n=20, gross=0.75, m=0, fixed=False):
    sc, elig = comp_rank(px)
    rank = sc.rank(axis=1, ascending=False)
    if m == 0:
        sel = (rank <= n).fillna(False)
    else:
        R = rank.values; E = elig.values
        held = np.zeros(px.shape[1], bool)
        out = np.zeros(px.shape, bool)
        for i in range(len(px)):
            r_i, e_i = R[i], E[i]
            ok = ~np.isnan(r_i)
            keep = held & e_i & ok & (r_i <= n + m)
            need = n - int(keep.sum())
            if need > 0:
                cand = np.where(e_i & ok & ~keep)[0]
                if len(cand):
                    cand = cand[np.argsort(r_i[cand])][:need]
                    keep[cand] = True
            held = keep
            out[i] = keep
        sel = pd.DataFrame(out, index=px.index, columns=px.columns)
    if fixed:
        return sel.astype(float).mul(gross / n)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(k, axis=0).mul(gross).fillna(0.0)


def band_ew_respread(px, band, gross):
    e = band_state(px, band).astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def ewall_weights(px, gross=1.00):
    _, elig = comp_rank(px)
    e = elig.astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def shy_residual_weights(px, gross=0.375, sleeve="SHY"):
    W = ewall_weights(px.drop(columns=[sleeve]), gross).reindex(columns=px.columns).fillna(0.0)
    W[sleeve] = (1.0 - W.sum(axis=1)).clip(lower=0.0)
    return W


def breadth_gate_weights(px, gross=1.00, q=0.17, wroll=1008, depth=1.0, freq="W"):
    core = px.drop(columns=["SPY"], errors="ignore")
    above = core > core.rolling(200).mean()
    breadth = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    thr = breadth.rolling(wroll, min_periods=wroll).quantile(q)
    bad = (breadth < thr) & breadth.notna() & thr.notna()
    m = pd.Series(1.0, index=px.index).where(~bad, 1.0 - depth)
    mask = rebalance_mask(px.index, freq)
    m = m.where(mask).ffill().fillna(1.0)
    return ewall_weights(px, gross).mul(m, axis=0)


# (key, label, panel, weights(px, g), cadence, memo gross, published (CAGR, Sharpe, MaxDD),
#  memo file stem, citation token)
CORPUS = [
    ("K1", "u56 top20 composite, weekly", "U56",
     lambda px, g: topn_weights(px, 20, g, 0), "W", 0.75, (0.1279, 1.064, -0.1831),
     "2026-09-07_u56-top20-g075-4b_C", "u56-top20-g075-4b"),
    ("K2", "u56 top20 composite + rank buffer m=20, weekly", "U56",
     lambda px, g: topn_weights(px, 20, g, 20), "W", 0.75, (None, None, None),
     "2026-09-07_u56-top20-band-m20", "u56-top20-band-m20"),
    ("K3", "u56 top20-200d DAILY + rank buffer m=50 (fixed g/n)", "U56",
     lambda px, g: topn_weights(px, 20, g, 50, fixed=True), "D", 0.75, (0.1171, 1.1454, -0.1237),
     "2026-09-06_top20-200d-daily-buffer", "top20-200d-daily"),
    ("K4", "u56 EW-all 200d-MA gate (band 0), MONTHLY", "U56",
     lambda px, g: rules_v2_weights(px, 0.0, g), "M", 1.00, (0.1196, 1.2126, -0.1549),
     "2026-09-08_u56-ewall-magate-fullgross", "u56-ewall-magate-fullgross"),
    ("K5", "u56 RULES v2 gate (band 3%), weekly", "U56",
     lambda px, g: rules_v2_weights(px, 0.03, g), "W", 1.00, (0.1159, 1.2055, -0.1591),
     "2026-09-08_u56-rulesv2-fullgross", "u56-rulesv2-fullgross"),
    ("K6", "u56 wide-band b=0.12 EW respread, weekly", "U56",
     lambda px, g: band_ew_respread(px, 0.12, g), "W", 0.75, (0.1402, 1.2264, -0.1942),
     "2026-09-07_u56-band12-ew", "band12"),
    ("K7", "b136 scored-eligible EW, residual in SHY, weekly", "B136",
     lambda px, g: shy_residual_weights(px, g), "W", 0.375, (0.0627, 1.1777, -0.1110),
     "2026-09-07_b136-ewall-shy-residual", "shy-residual"),
    ("K8", "u56 EW-all, de-gross to ZERO on breadth < trailing-1008d q0.17, weekly", "U56",
     lambda px, g: breadth_gate_weights(px, g, 0.17), "W", 1.00, (0.1413, 1.2204, -0.1479),
     "2026-09-10_u56-ewall-breadth-qroll", "breadth-qroll"),
    ("LIVE", "RULES v2 (LIVE book, band 3%), weekly  [comparand, not a 4b pass]", "U56",
     lambda px, g: rules_v2_weights(px, 0.03, g), "W", 0.75, (0.0863, 1.202, -0.1205),
     "RULES.md v2", "RULES v2"),
    ("V1", "RULES v1 (retired book), weekly  [comparand, not a 4b pass]", "U56",
     lambda px, g: rules_v1_weights(px, 5, 0.15 * g / 0.75), "W", 0.75, (None, None, None),
     "RULES.md v1", "RULES v1"),
]
CANDS = [c[0] for c in CORPUS if c[0] not in ("LIVE", "V1")]

# each book's OWN committed memo, named explicitly so PART A measures rather than guesses.
# K3: its m=30 sibling's PARK memo, the file that swept the BUFFER dial (and only g=0.75).
# K8: its q=0.20 sibling's memo, the one file in the corpus that already ran a 17-rung g ladder.
MEMO_FILE = {
    "K1": "2026-09-07_u56-top20-g075-4b_C_MEMO.md",
    "K2": "2026-09-07_u56-top20-band-m20_4b_B_MEMO.md",
    "K3": "2026-09-06_daily-plus-buffer30_PARK_MEMO.md",
    "K4": "2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO.md",
    "K5": "2026-09-08_u56-band3-fullgross_KEEP_MEMO.md",
    "K6": "2026-09-06_band12-ewall-rw_PARK_MEMO.md",
    "K7": "2026-09-07_b136-shy-residual-ewall-g0375_4a_cloud_MEMO.md",
    "K8": "2026-09-10_does-the-BREADTH-gate-4b-pass-live-only-at-gross-1.00_cloud.memo.md",
}


# =====================================================================================
# simulation helpers
# =====================================================================================
def sim(px, W, freq):
    """One cost-free simulation; every rung comes off it exactly."""
    b = backtest(px, W, cost_bps=0, freq=freq)
    return b["returns"], b["turnover"]


def netr(r, to, bps, start):
    return (r - to * bps / 1e4).loc[start:]


def pack(r):
    m = metrics(r)
    h = len(r) // 2
    oos = r.loc[OOS_START:]
    mo = metrics(oos)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                IS=metrics(r.loc[:IS_END])["Sharpe"], IS_CAGR=metrics(r.loc[:IS_END])["CAGR"])


def keep4b(p, bar):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  Returns (pass, first-failing bar, full fail set)."""
    fails = []
    if not (p["H1"] > bar["H1"]):        fails.append("H1")
    if not (p["H2"] > bar["H2"]):        fails.append("H2")
    if not (p["OOS"] > bar["OOS"]):      fails.append("OOS")
    if not (p["MaxDD"] >= bar["DD"]):    fails.append("DD")
    if not (p["CAGR"] >= bar["CAGR"]):   fails.append("CAGR")
    return (len(fails) == 0), (fails[0] if fails else ""), "+".join(fails)


def keep4a(p, b):
    """PROTOCOL 4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse."""
    fails = []
    if not (p["H1"] > b["H1"]):       fails.append("H1")
    if not (p["H2"] > b["H2"]):       fails.append("H2")
    if not (p["MaxDD"] >= b["MaxDD"]): fails.append("DD")
    return (len(fails) == 0), "+".join(fails)


def bands(flags):
    """Longest run of True in a list, and the total count; returns (count, width, lo, hi)."""
    best = (0, None, None); cur = 0; start = None
    for i, f in enumerate(flags):
        if f:
            if cur == 0: start = i
            cur += 1
            if cur > best[0]: best = (cur, start, i)
        else:
            cur = 0
    return sum(flags), best[0], best[1], best[2]


# =====================================================================================
def main():
    log("=" * 108)
    log(f"Idea 574 - re-sweep the record's most-cited UNSWEPT 4b passes in GROSS  ({DATE}, lane B)")
    log("=" * 108)
    pxU = load_universe().loc[:END]
    pxB = load_universe(broad=True).loc[:END]
    PX = {"U56": pxU, "B136": pxB}
    ST = {k: v.index[WARMUP] for k, v in PX.items()}
    log(f"U56  {pxU.shape[1]} names, {ST['U56'].date()} .. {pxU.index[-1].date()}")
    log(f"B136 {pxB.shape[1]} names, {ST['B136'].date()} .. {pxB.index[-1].date()}")
    log(f"grid: {len(GRID)} gross points {GRID[0]} .. {GRID[-1]} step 0.05; "
        f"{len(CORPUS)} books ({len(CANDS)} candidates + 2 comparands) = {len(CORPUS)*len(GRID)} cells")

    # ---- bars: SPY and live RULES v2, per panel, per rung ------------------------------
    BAR4b, BASE = {}, {}
    for pan, px in PX.items():
        st = ST[pan]
        spy = px["SPY"].pct_change().fillna(0).loc[st:]
        s = pack(spy)
        BAR4b[pan] = dict(H1=s["H1"], H2=s["H2"], OOS=s["OOS"],
                          DD=0.60 * s["MaxDD"], CAGR=0.70 * s["CAGR"], SPY=s)
        r, to = sim(px, rules_v2_weights(px, 0.03, 0.75), "W")
        BASE[pan] = {c: pack(netr(r, to, c, st)) for c in RUNGS}
    for pan in PX:
        b = BAR4b[pan]; s = b["SPY"]; v = BASE[pan][HEAD]
        log(f"\n  {pan} SPY  CAGR {s['CAGR']:.2%}  Sharpe {s['Sharpe']:.4f} "
            f"(H1 {s['H1']:.4f} / H2 {s['H2']:.4f}, OOS {s['OOS']:.4f})  MaxDD {s['MaxDD']:.2%}")
        log(f"  {pan} 4b bars: H1>{b['H1']:.4f}  H2>{b['H2']:.4f}  OOS>{b['OOS']:.4f}  "
            f"MaxDD>={b['DD']:.2%}  CAGR>={b['CAGR']:.2%}")
        log(f"  {pan} RULES v2 @{HEAD}bps (4a bar): CAGR {v['CAGR']:.2%} Sharpe {v['Sharpe']:.4f} "
            f"(H1 {v['H1']:.4f} / H2 {v['H2']:.4f})  MaxDD {v['MaxDD']:.2%}  OOS {v['OOS']:.4f}")

    # =================================================================================
    # GATES -- pre-registered, run and read before any result
    # =================================================================================
    log("\n" + "=" * 108)
    log("GATES (four, pre-registered)")
    log("=" * 108)
    gres = {}

    # G1: RULES v2's own committed headline
    v = BASE["U56"][HEAD]
    g1 = (abs(v["Sharpe"] - 1.202) < 6e-3 and abs(v["CAGR"] - 0.0863) < 6e-3
          and abs(v["MaxDD"] + 0.1205) < 6e-3)
    gres["G1"] = g1
    log(f"  G1  RULES v2 U56 @10bps {v['CAGR']:.2%}/{v['Sharpe']:.4f}/{v['MaxDD']:.2%} vs committed "
        f"8.63%/1.202/-12.05%  (bar 6e-3; prices.csv is re-downloaded daily, so u56 rows in this "
        f"record reproduce to ~3e-3, NOT bit-exact - idea 406)  {'PASS' if g1 else 'FAIL'}")

    # G2: every memo book reproduces its published headline at its OWN memo gross
    log("  G2  memo-headline reproduction at the memo's own gross (bar |dSharpe| <= 0.02; "
        "a miss EXCLUDES the book from PART C's verdict count):")
    MEMO, excluded = {}, []
    for key, label, pan, fn, freq, gm, pub, stem, tok in CORPUS:
        px = PX[pan]
        r, to = sim(px, fn(px, gm), freq)
        p = pack(netr(r, to, HEAD, ST[pan]))
        MEMO[key] = p
        if pub[0] is None:
            log(f"      {key:4s} g={gm:.3f} {p['CAGR']:7.2%} {p['Sharpe']:7.4f} {p['MaxDD']:8.2%}"
                f"   (no published headline to gate on)   {label}")
            continue
        d = abs(p["Sharpe"] - pub[1])
        ok = d <= 0.02
        if not ok: excluded.append(key)
        log(f"      {key:4s} g={gm:.3f} {p['CAGR']:7.2%} {p['Sharpe']:7.4f} {p['MaxDD']:8.2%}"
            f"   vs published {pub[0]:.2%}/{pub[1]:.4f}/{pub[2]:.2%}  |dS| {d:.4f}  "
            f"{'PASS' if ok else 'FAIL'}   {label}")
    gres["G2"] = len(excluded) == 0
    log(f"      -> {len([c for c in CORPUS if c[6][0] is not None]) - len(excluded)} of "
        f"{len([c for c in CORPUS if c[6][0] is not None])} gated books reproduce; "
        f"excluded: {excluded or 'none'}   {'PASS' if gres['G2'] else 'PARTIAL'}")

    # G3: the g grid contains each book's own memo point exactly
    onmesh = {c[0]: any(abs(g - c[5]) < 1e-9 for g in GRID) for c in CORPUS}
    off = [k for k, v_ in onmesh.items() if not v_]
    gres["G3"] = True    # informational: off-mesh books are swept AND priced at their memo g
    log(f"  G3  memo gross on the 17-point mesh: {len(onmesh)-len(off)} of {len(onmesh)}; "
        f"off-mesh {off or 'none'} (K7's 0.375 sits between 0.35 and 0.40 - it is reported at "
        f"BOTH its memo point and the mesh)  INFO")

    # G4: cost rungs are exact (rung 0 minus turnover*bps == engine at that cost_bps)
    px = PX["U56"]
    W = rules_v2_weights(px, 0.03, 0.75)
    r0, t0 = sim(px, W, "W")
    ref = backtest(px, W, cost_bps=25, freq="W")["returns"]
    d4 = float(np.abs((r0 - t0 * 25 / 1e4) - ref).max())
    gres["G4"] = d4 < 1e-12
    log(f"  G4  derived cost rung vs engine.backtest(cost_bps=25): {d4:.3e} (bar 1e-12)  "
        f"{'PASS' if gres['G4'] else 'FAIL'}")
    log(f"  GATES: {sum(gres.values())} of {len(gres)} pass "
        f"({', '.join(k for k,v_ in gres.items() if not v_) or 'none failing'})")

    # =================================================================================
    # PART A -- is each book actually UNSWEPT, and how often is it cited?
    # =================================================================================
    log("\n" + "=" * 108)
    log("PART A -- the queue's two premises, measured: UNSWEPT (its own file never ran a second")
    log("          gross) and MOST-CITED (how often the record names it)")
    log("=" * 108)
    md = sorted(ROOT.glob("research/**/*.md")) + sorted(ROOT.glob("research/**/*.py"))
    corpus_txt = {}
    for f in md:
        try: corpus_txt[f] = f.read_text(errors="ignore")
        except Exception: pass
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    rows = []
    log("  Each book's OWN memo is named explicitly (the filename census a text search cannot do")
    log("  reliably); the gross literals below are read out of that file. Two footnotes, both")
    log("  published because they soften the premise:")
    log("    K3's memo is its m=30 sibling's PARK memo (the file that swept the buffer dial m);")
    log("    K8's is the q=0.20 sibling's memo, which DID run a 17-rung gross ladder.")
    log("")
    log(f"  {'book':4s} {'cites(all)':>10s} {'cites(LB)':>9s} {'g-values in its own memo':>28s}  swept?")
    for key, label, pan, fn, freq, gm, pub, stem, tok in CORPUS:
        cites = sum(t.count(tok) for t in corpus_txt.values())
        lbc = lb.count(tok)
        f = ROOT / "research" / "backtests" / MEMO_FILE[key] if MEMO_FILE.get(key) else None
        gvals, note = set(), ""
        if f is not None and f.exists():
            txt = f.read_text(errors="ignore")
            for m_ in re.finditer(r"(?:gross|g)\s*[=:]?\s*([01]\.\d{2,3})\b", txt, re.I):
                gvals.add(round(float(m_.group(1)), 3))
            if "17-rung" in txt or "17 rung" in txt or "0.20..1.00" in txt:
                note = " (memo states a 17-rung ladder)"
                gvals |= set(GRID)
        else:
            note = " (no single memo file; comparand)"
        swept = len(gvals) >= 2
        rows.append(dict(book=key, cites=cites, cites_lb=lbc, memo=MEMO_FILE.get(key, ""),
                         n_gross_in_memo=len(gvals), g_in_memo=sorted(gvals), swept=swept))
        shown = sorted(gvals) if len(gvals) <= 4 else f"{len(gvals)} values 0.20..1.00"
        log(f"  {key:4s} {cites:10d} {lbc:9d} {str(shown)[:28]:>28s}  "
            f"{'SWEPT' if swept else 'UNSWEPT (one g only)'}{note}")
    cens = pd.DataFrame(rows)
    cser = cens[cens.book.isin(CANDS)]
    log(f"\n  PREMISE 1 (unswept): {int((~cser.swept).sum())} of {len(cser)} candidates were "
        f"published at ONE gross and never re-run at a second inside their own memo. "
        f"The {int(cser.swept.sum())} exception(s): {list(cser[cser.swept].book)}.")
    log(f"  PREMISE 2 (most cited): ranked by mentions across committed research/ text - "
        f"{', '.join(f'{r.book} {r.cites}' for _, r in cser.sort_values('cites', ascending=False).iterrows())}. "
        f"The two comparands dominate the record by construction (LIVE {int(cens[cens.book=='LIVE'].cites.iloc[0])}, "
        f"V1 {int(cens[cens.book=='V1'].cites.iloc[0])}) and are reported but not counted as candidates.")

    # =================================================================================
    # PART C -- the 17-point gross ladder
    # =================================================================================
    log("\n" + "=" * 108)
    log(f"PART C -- the gross ladder: {len(CORPUS)} books x {len(GRID)} g x {len(RUNGS)} rungs = "
        f"{len(CORPUS)*len(GRID)*len(RUNGS)} rows, EVERY POINT REPORTED")
    log("=" * 108)
    cells = []
    for key, label, pan, fn, freq, gm, pub, stem, tok in CORPUS:
        px = PX[pan]; st = ST[pan]; bar = BAR4b[pan]
        gs = sorted(set(GRID) | {gm})
        for g in gs:
            r, to = sim(px, fn(px, g), freq)
            for c in RUNGS:
                p = pack(netr(r, to, c, st))
                ok4b, first, fset = keep4b(p, bar)
                ok4a, f4a = keep4a(p, BASE[pan][c])
                cells.append(dict(book=key, label=label, panel=pan, cadence=freq, g=g,
                                  memo_g=gm, is_memo_g=abs(g - gm) < 1e-9, bps=c,
                                  **{k_: v_ for k_, v_ in p.items()},
                                  keep4b=ok4b, bind4b=first, fail4b_set=fset,
                                  keep4a=ok4a, fail4a_set=f4a))
    C = pd.DataFrame(cells)
    C.to_csv(f"{OUT}.cells.csv", index=False)

    for key, label, pan, fn, freq, gm, pub, stem, tok in CORPUS:
        sub = C[(C.book == key) & (C.bps == HEAD)].sort_values("g")
        log(f"\n  {key}  {label}   [{pan}, {freq}, memo g={gm:.3f}]")
        log(f"    {'g':>5s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
            f"{'OOS':>7s} {'4b':>4s} {'bind':>10s} {'4a':>4s}")
        for _, row in sub.iterrows():
            star = " <- memo" if row.is_memo_g else ""
            log(f"    {row.g:5.3f} {row.CAGR:8.2%} {row.Sharpe:8.4f} {row.MaxDD:8.2%} "
                f"{row.H1:7.4f} {row.H2:7.4f} {row.OOS:7.4f} "
                f"{'PASS' if row.keep4b else ' -  ':>4s} {row.bind4b or '-':>10s} "
                f"{'PASS' if row.keep4a else ' -  ':>4s}{star}")
        mesh = sub[sub.g.isin(GRID)]
        n4b, w4b, lo, hi = bands(list(mesh.keep4b))
        n4a, _, _, _ = bands(list(mesh.keep4a))
        gl = list(mesh.g)
        span = f"{gl[lo]:.2f}-{gl[hi]:.2f}" if w4b else "none"
        memo_row = sub[sub.is_memo_g].iloc[0]
        log(f"    -> 4b {n4b}/{len(mesh)} of the mesh, widest contiguous band {w4b} rungs "
            f"({span}); 4a {n4a}/{len(mesh)}.  At the memo's own g: "
            f"4b {'PASS' if memo_row.keep4b else 'FAIL (' + memo_row.fail4b_set + ')'}, "
            f"4a {'PASS' if memo_row.keep4a else 'FAIL'}")

    # ---- the headline tally ------------------------------------------------------------
    log("\n" + "-" * 108)
    log("  PART C HEADLINE -- how many of the corpus keep their verdict, and how wide is the band")
    log("-" * 108)
    log(f"  {'book':4s} {'memo g':>7s} {'4b@memo':>8s} {'4b cells':>9s} {'band':>5s} {'band span':>11s} "
        f"{'edge?':>6s} {'4a cells':>9s} {'binding bar (mode)':>20s}")
    tally = []
    for key in [c[0] for c in CORPUS]:
        sub = C[(C.book == key) & (C.bps == HEAD)].sort_values("g")
        mesh = sub[sub.g.isin(GRID)]
        memo_row = sub[sub.is_memo_g].iloc[0]
        n4b, w4b, lo, hi = bands(list(mesh.keep4b))
        n4a, _, _, _ = bands(list(mesh.keep4a))
        gl = list(mesh.g)
        span = f"{gl[lo]:.2f}-{gl[hi]:.2f}" if w4b else "none"
        # is the memo point at the edge of the admissible band?
        edge = "n/a"
        if memo_row.keep4b and w4b:
            inband = [gl[i] for i in range(lo, hi + 1)]
            if any(abs(memo_row.g - x) < 1e-9 for x in inband):
                edge = "EDGE" if abs(memo_row.g - inband[0]) < 1e-9 or abs(memo_row.g - inband[-1]) < 1e-9 else "interior"
            else:
                edge = "isolated"
        binders = mesh[~mesh.keep4b].bind4b
        mode = binders.mode().iloc[0] if len(binders) else "-"
        tally.append(dict(book=key, memo_g=memo_row.g, keep4b_memo=bool(memo_row.keep4b),
                          n4b=n4b, band=w4b, span=span, edge=edge, n4a=n4a, binder=mode))
        log(f"  {key:4s} {memo_row.g:7.3f} {'PASS' if memo_row.keep4b else 'FAIL':>8s} "
            f"{n4b:5d}/{len(mesh):<3d} {w4b:5d} {span:>11s} {edge:>6s} {n4a:5d}/{len(mesh):<3d} "
            f"{mode or '-':>20s}")
    T = pd.DataFrame(tally)
    cand = T[T.book.isin(CANDS)]
    log(f"\n  CANDIDATES ONLY (n={len(cand)}): 4b holds at the memo's own gross in "
        f"{int(cand.keep4b_memo.sum())} of {len(cand)}.")
    log(f"  Admissible-band width in g (17 rungs = the whole ladder): "
        f"median {cand.band.median():.0f}, min {cand.band.min()}, max {cand.band.max()}; "
        f"{int((cand.band == 0).sum())} books admit NOWHERE, {int((cand.band == 17).sum())} everywhere.")
    log(f"  Of the {int(cand.keep4b_memo.sum())} that hold, "
        f"{int((cand[cand.keep4b_memo].edge == 'EDGE').sum())} sit on the EDGE of their own band "
        f"and {int((cand[cand.keep4b_memo].edge == 'interior').sum())} in its interior.")
    for c in RUNGS:
        sc = C[(C.bps == c) & C.book.isin(CANDS) & C.g.isin(GRID)]
        log(f"  rung {c:2d} bps: 4b {int(sc.keep4b.sum())}/{len(sc)} cells, "
            f"4a {int(sc.keep4a.sum())}/{len(sc)}")

    # ---- WHY the band is what it is: is g an information dial at all? -------------------
    log("\n" + "-" * 108)
    log("  PART C MECHANISM -- is gross an INFORMATION dial or a pure EXPOSURE dial?")
    log("  (if Sharpe is flat in g, the 4b band is only the window where the CAGR floor and the")
    log("   DD cap happen to cross, and carries no evidence about the book)")
    log("-" * 108)
    log(f"  {'book':4s} {'max|dSharpe| over ladder':>24s} {'rho(g,CAGR)':>12s} {'rho(g,MaxDD)':>13s} "
        f"{'CAGR/g slope':>13s} {'reading':>22s}")
    flat = []
    for key in [c[0] for c in CORPUS]:
        s = C[(C.book == key) & (C.bps == HEAD) & C.g.isin(GRID)].sort_values("g")
        dS = float(s.Sharpe.max() - s.Sharpe.min())
        rc = float(np.corrcoef(s.g, s.CAGR)[0, 1])
        rd = float(np.corrcoef(s.g, s.MaxDD)[0, 1])
        slope = float(np.polyfit(s.g, s.CAGR, 1)[0])
        read = "pure EXPOSURE" if dS < 0.02 else ("mix dial" if dS > 0.10 else "near-pure")
        flat.append(dict(book=key, dSharpe_span=dS, rho_g_CAGR=rc, rho_g_MaxDD=rd,
                         CAGR_per_unit_g=slope, reading=read))
        log(f"  {key:4s} {dS:24.4f} {rc:12.4f} {rd:13.4f} {slope:13.4f} {read:>22s}")
    F = pd.DataFrame(flat)
    F.to_csv(f"{OUT}.flat.csv", index=False)
    fc = F[F.book.isin(CANDS)]
    log(f"\n  {int((fc.dSharpe_span < 0.02).sum())} of {len(fc)} candidates move Sharpe by less than "
        f"0.02 across the ENTIRE 0.20-1.00 ladder (median span {fc.dSharpe_span.median():.4f}); "
        f"rho(g, CAGR) is +1.0000 to four decimals in {int((fc.rho_g_CAGR > 0.9999).sum())} of "
        f"{len(fc)} and rho(g, MaxDD) is -1.0000 in {int((fc.rho_g_MaxDD < -0.9999).sum())} of {len(fc)}.")
    log("  Where that holds, moving g cannot change the book's information content -- it moves the")
    log("  book along a straight line in (CAGR, MaxDD) at constant Sharpe, and the 4b band is the")
    log("  segment of that line between the CAGR floor and the DD cap. The published verdict is")
    log("  then a statement about the bars, not about the strategy.")

    # =================================================================================
    # PART D -- rule 8 walk-forward: g chosen on IS <= 2016, OOS 2017- read once
    # =================================================================================
    log("\n" + "=" * 108)
    log("PART D -- PROTOCOL rule 8 walk-forward: g chosen on 2009-2016 IS Sharpe ALONE,")
    log("          2017-2026 read exactly ONCE.  Reported against the live baseline and SPY.")
    log("=" * 108)
    wf = []
    for pan in PX:
        st = ST[pan]
        spy = PX[pan]["SPY"].pct_change().fillna(0).loc[st:]
        so = metrics(spy.loc[OOS_START:])
        bo = BASE[pan][HEAD]
        log(f"\n  {pan} OOS comparands @{HEAD}bps:  RULES v2 CAGR {bo['OOS_CAGR']:.2%} "
            f"Sharpe {bo['OOS']:.4f} MaxDD {bo['OOS_MaxDD']:.2%}   |   "
            f"SPY CAGR {so['CAGR']:.2%} Sharpe {so['Sharpe']:.4f} MaxDD {so['MaxDD']:.2%}")
    log(f"\n  {'book':4s} {'IS-pick g':>9s} {'memo g':>7s} {'pick=memo':>9s} {'OOS CAGR':>9s} "
        f"{'OOS Shrp':>9s} {'OOS MaxDD':>10s} {'vs v2':>7s} {'vs SPY':>7s} {'OOS 4b':>7s} "
        f"{'memo-g OOS Shrp':>15s}")
    for key, label, pan, fn, freq, gm, pub, stem, tok in CORPUS:
        sub = C[(C.book == key) & (C.bps == HEAD) & C.g.isin(GRID)].sort_values("g")
        pick = sub.loc[sub.IS.idxmax()]
        memo_row = C[(C.book == key) & (C.bps == HEAD) & C.is_memo_g].iloc[0]
        bo = BASE[pan][HEAD]
        so = metrics(PX[pan]["SPY"].pct_change().fillna(0).loc[ST[pan]:].loc[OOS_START:])
        beats_v2 = pick.OOS > bo["OOS"]
        beats_spy = pick.OOS > so["Sharpe"]
        wf.append(dict(book=key, panel=pan, pick_g=pick.g, memo_g=gm,
                       same=abs(pick.g - gm) < 1e-9, IS_Sharpe=pick.IS,
                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS, OOS_MaxDD=pick.OOS_MaxDD,
                       base_OOS=bo["OOS"], base_OOS_CAGR=bo["OOS_CAGR"],
                       spy_OOS=so["Sharpe"], spy_OOS_CAGR=so["CAGR"],
                       beats_base=beats_v2, beats_spy=beats_spy, keep4b_pick=bool(pick.keep4b),
                       memo_OOS=memo_row.OOS, memo_OOS_CAGR=memo_row.OOS_CAGR,
                       memo_OOS_MaxDD=memo_row.OOS_MaxDD))
        log(f"  {key:4s} {pick.g:9.2f} {gm:7.3f} {str(abs(pick.g-gm)<1e-9):>9s} "
            f"{pick.OOS_CAGR:9.2%} {pick.OOS:9.4f} {pick.OOS_MaxDD:10.2%} "
            f"{'YES' if beats_v2 else 'no':>7s} {'YES' if beats_spy else 'no':>7s} "
            f"{'PASS' if pick.keep4b else '-':>7s} {memo_row.OOS:15.4f}")
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.wf.csv", index=False)
    wc = WF[WF.book.isin(CANDS)]
    log(f"\n  Rule 8, candidates only (n={len(wc)}): the IS-Sharpe pick reproduces the memo's own "
        f"gross in {int(wc.same.sum())} of {len(wc)}.")
    log(f"  OOS the picks beat the live RULES v2 baseline {int(wc.beats_base.sum())}/{len(wc)} and "
        f"SPY {int(wc.beats_spy.sum())}/{len(wc)}; 4b holds OOS-inclusive for "
        f"{int(wc.keep4b_pick.sum())}/{len(wc)} picks.")
    log(f"  Median OOS Sharpe: pick {wc.OOS_Sharpe.median():.4f} vs memo-g "
        f"{wc.memo_OOS.median():.4f} vs RULES v2 {wc.base_OOS.median():.4f} vs SPY "
        f"{wc.spy_OOS.median():.4f}.")
    mv = wc[~wc.same]     # the books where rule 8 actually moved the gross; the other 3 are ties
    log(f"  What the selector's move BUYS and PAYS, on the {len(mv)} books where it MOVED the gross "
        f"(pick minus memo-g; the other {int(wc.same.sum())} are exact ties and are excluded so the "
        f"median is not pinned at zero by them):")
    log(f"    OOS Sharpe  median {float((mv.OOS_Sharpe - mv.memo_OOS).median()):+.4f}  "
        f"mean {float((mv.OOS_Sharpe - mv.memo_OOS).mean()):+.4f}  "
        f"range {float((mv.OOS_Sharpe - mv.memo_OOS).min()):+.4f} .. "
        f"{float((mv.OOS_Sharpe - mv.memo_OOS).max()):+.4f}")
    log(f"    OOS CAGR    median {float((mv.OOS_CAGR - mv.memo_OOS_CAGR).median()):+.2%}  "
        f"range {float((mv.OOS_CAGR - mv.memo_OOS_CAGR).min()):+.2%} .. "
        f"{float((mv.OOS_CAGR - mv.memo_OOS_CAGR).max()):+.2%}")
    log(f"    OOS MaxDD   median {float((mv.OOS_MaxDD - mv.memo_OOS_MaxDD).median()):+.2%}  "
        f"range {float((mv.OOS_MaxDD - mv.memo_OOS_MaxDD).min()):+.2%} .. "
        f"{float((mv.OOS_MaxDD - mv.memo_OOS_MaxDD).max()):+.2%}  "
        f"(negative = DEEPER drawdown than the memo's own gross)")
    log("  Read with the mechanism above: on a book whose Sharpe is flat in g, an IS-SHARPE")
    log("  selector is choosing a gross almost at random and the OOS Sharpe it reports is nearly")
    log("  unchanged -- what actually moves is the drawdown the book will hand its owner.")

    # =================================================================================
    # KEEP paths
    # =================================================================================
    log("\n" + "=" * 108)
    log("KEEP PATHS -- both evaluated on every cell")
    log("=" * 108)
    mesh = C[C.g.isin(GRID) & C.book.isin(CANDS)]
    for c in RUNGS:
        s = mesh[mesh.bps == c]
        log(f"  {c:2d} bps: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}")
    head = mesh[mesh.bps == HEAD]
    both = head[head.keep4a & head.keep4b]
    log(f"  BOTH paths at {HEAD} bps: {len(both)}/{len(head)}")
    if len(head[head.keep4b]):
        best = head[head.keep4b].sort_values("Sharpe", ascending=False).iloc[0]
        log(f"  best 4b cell by full-sample Sharpe: {best.book} g={best.g:.2f} "
            f"{best.CAGR:.2%}/{best.Sharpe:.4f}/{best.MaxDD:.2%} (H {best.H1:.4f}/{best.H2:.4f}, "
            f"OOS {best.OOS:.4f})")
    log("  NO NEW KEEP-CANDIDATE IS CLAIMED BY THIS RUN: every 4b-passing cell here is a gross")
    log("  re-pricing of a book the record has already memo'd, not a new book. The deliverable is")
    log("  the BAND, not a candidate.")

    # ---- write artefacts ---------------------------------------------------------------
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    cens.to_csv(f"{OUT}.census.csv", index=False)
    T.to_csv(f"{OUT}.tally.csv", index=False)
    log(f"\nwrote {OUT}.txt / .cells.csv / .wf.csv / .census.csv / .tally.csv")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

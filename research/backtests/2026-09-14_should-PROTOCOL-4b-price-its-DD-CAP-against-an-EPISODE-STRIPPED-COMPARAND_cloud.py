#!/usr/bin/env python3
"""Idea 861 (cloud lane, 2026-09-14) — should PROTOCOL 4b price its DD CAP against an
EPISODE-STRIPPED COMPARAND?

QUESTION (QUEUE idea 861, verbatim)
    idea 814 found the CORR-HI candidate clears the 4b drawdown cap by 5.12pp with SPY's 2020 in
    the denominator and FAILS by 0.41pp without it, while its OWN MaxDD is -15.11% either way.
    The cap is a ratio against a comparand whose denominator is one 33-day episode.  Census the
    record's committed 4b DD-leg margins, re-measure each with the 2020 and the 2022 episode
    removed from BOTH sides, and price a PROTOCOL clause requiring the leg to clear at every
    single-episode strip.  Max 2 params (book set, episode set).

WHAT IS NEW AGAINST 851 (the same lane, yesterday).  851 asked "how many candidates survive
    their own bar when ONE episode is deleted", one episode at a time, and answered: the BAR
    moves (SPY -33.72% -> -24.50%), the BOOKS do not.  It stopped there.  861 asks the
    engineering question that follows and that nothing on the record has priced:

      (A) THE MARGIN CENSUS.  Not "does it pass" but BY HOW MUCH.  Every committed 4b DD leg on
          the record, with its margin (book MaxDD - cap) in pp, on the unstripped leg.  A leg
          that clears by 5 pp and a leg that clears by 0.1 pp are the same PASS today.

      (B) THE CONJUNCTIVE CLAUSE, stated and then priced as a rule:
             4b-DD-STRIP: the DD leg must clear at EVERY single-episode strip in a declared
             episode set, with the cap re-priced on the same stripped leg.
          The clause's statistic is MINMARGIN = min over strips of (MaxDD_ex - cap_ex).  It is
          a conjunction, so it can only ever REMOVE passes; the whole question is what it
          removes and whether what it removes deserved to go.

      (C) THE CLAUSE'S OWN FALSE-REJECTION RATE.  A conjunction over k strips rejects things by
          arithmetic alone.  Two calibrations are run before the clause is believed:
             PLACEBO episode set   strips of the same calendar shape containing no crash.  A
                                   clause that kills books here is measuring day-count, not
                                   drawdown control.
             SHUFFLE strips        20 random blocks of the headline episode's length, drawn
                                   from a fixed seed.  The clause's kill count on real episodes
                                   must sit outside the shuffle distribution or it is noise.

      (D) RULE 8 WITH THE CLAUSE AS A SELECTOR.  The capital question: if the clause is applied
          IN SAMPLE (2009-2016) as a screen on the candidate pool, is the book it picks BETTER
          out of sample (2017-2026) than the book the unscreened chooser picks?  A protocol
          clause that costs OOS Sharpe is a worse clause than no clause, however tidy it reads.
          Both choosers, both panels, every episode set, all reported.

TUNED PARAMETERS: exactly TWO, the two the queue names.
    (1) BOOK SET in {SHELF, GRID}.
            SHELF  every committed 4b KEEP-candidate memo under research/backtests/ that this
                   run rebuilds from its own RULES wording and gates against its published
                   headline (idea 851's shelf, restated verbatim so the two runs are
                   comparable).  A memo that does not reproduce is NAMED and EXCLUDED.
            GRID   a mechanical band x gross x QROLL ladder that was never memo-selected.
    (2) EPISODE SET in {QUEUE2, REAL5, PLACEBO3}.
            QUEUE2    {COVID_TIGHT, BEAR2022}      <- HEADLINE, the queue's own two, declared
                                                      here before any number is read
            REAL5     QUEUE2 + {COVID_WIDE, COVID_DD, DD_2015}
            PLACEBO3  {PLACEBO_2017, PLACEBO_2013, PLACEBO_2019}   (calibration only)

DELETION CONVENTION: SPLICE, from idea 851 — the episode's trading days are removed from every
    series (book, RULES v2 baseline, SPY) before any moment is taken, so Sharpe, CAGR and MaxDD
    are all read on the same shortened calendar, and the cap is re-priced as 60% of SPY's MaxDD
    ON THAT SAME LEG.  "From BOTH sides", as the queue puts it.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_MARGIN   the committed 4b DD-leg margins are NOT concentrated at the bar: the median
               unstripped margin over passing rows exceeds 2.00 pp.
    H_CLAUSE   the QUEUE2 clause removes at least one third of the unstripped 4b passes on the
               SHELF (if it removes nothing it is not worth a PROTOCOL line; if it removes
               everything it is a day-count artefact, which PLACEBO3 then has to confirm).
    H_PLACEBO  the PLACEBO3 clause removes strictly fewer passes than the QUEUE2 clause, i.e.
               the clause is reading drawdown episodes rather than sample length.
    H_SHUFFLE  the QUEUE2 kill count sits at or beyond the 90th percentile of the 20-draw
               shuffle-strip null.
    H_R8       the clause-screened rule-8 pick does NOT beat the unscreened pick on OOS Sharpe
               (i.e. the clause is a REPORTING requirement, not an alpha filter).  Declared in
               this direction deliberately: the honest prior is that a drawdown-robustness
               screen buys nothing on a 10-year OOS window.

GATES (printed before any new number; all must pass)
    G1  the empty splice is the identity (max|d| == 0.0).
    G2  every SHELF book reproduces its committed memo headline inside a stated tolerance
        (Sharpe 0.030, MaxDD 1.5 pp).  Books outside are named and dropped.
    G3  SPY reproduces the record's committed 4b comparand 15.16% / 0.8861 / -33.72%.
    G4  851 REPLICATION: this run's SPY MaxDD under COVID_TIGHT equals 851's committed
        -24.50% and its re-priced cap equals -14.70%, to 0.05 pp.  If the two runs disagree the
        census below is not comparable with the record and nothing is read.
    G5  the clause is a conjunction: MINMARGIN <= every single-strip margin, for every row.

PROTOCOL: 10 bps per unit turnover (25 also reported), weights decided at close t applied at
    t+1, no shorting, no leverage.  Both KEEP paths evaluated on every row.  Rule 8: the dial is
    chosen on 2009-2016 alone and the OOS window 2017-2026 is read once per (chooser, panel,
    episode set).

SURVIVORSHIP, up front: U56 and B136 are CURRENT-constituent lists, so every CAGR and drawdown
    LEVEL is optimistic; the strip-to-strip DIFFERENCE is the durable part.  Nothing here is a
    capital claim and nothing is promoted.

Outputs (committed under research/backtests/):
    .console.txt      full log
    .margins.csv      every book x episode-strip x rung: MaxDD, cap, margin, 4a/4b verdicts
    .clause.csv       every book x episode SET x rung: MINMARGIN, binding strip, clause verdict
    .shuffle.csv      the 20-draw shuffle-strip null
    .walkforward.csv  rule-8, screened vs unscreened chooser, per (panel, episode set)

Run: python research/backtests/2026-09-14_should-PROTOCOL-4b-price-its-DD-CAP-against-an-EPISODE-STRIPPED-COMPARAND_cloud.py
Deterministic (seed 861); no network (reads the committed price caches only).
"""
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, rules_v1_weights  # noqa: E402
from engine import rebalance_mask  # noqa: E402

DATE = "2026-09-14"
SLUG = "should-PROTOCOL-4b-price-its-DD-CAP-against-an-EPISODE-STRIPPED-COMPARAND"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FREQ, LAG, WARMUP, MAX_VOL = "W", 1, 260, 0.60
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED = 861
N_SHUFFLE = 20

# the record's COMMITTED full-sample bars, quoted in every 4b memo
FIXED_CAP = -0.2023
FIXED_FLOOR = 0.70 * 0.151631

# ---- tuned dial 1: the book set ---------------------------------------------------------
SETS = ["SHELF", "GRID"]

# ---- tuned dial 2: the episode set ------------------------------------------------------
EPISODES = {
    "COVID_TIGHT": ("2020-02-19", "2020-04-07"),
    "COVID_DD": None,                          # resolved from SPY itself
    "COVID_WIDE": ("2020-02-01", "2020-06-30"),
    "DD_2015": ("2015-08-10", "2015-09-29"),
    "BEAR2022": ("2022-01-03", "2022-10-12"),
    "PLACEBO_2017": ("2017-02-19", "2017-04-07"),
    "PLACEBO_2013": ("2013-02-19", "2013-04-07"),
    "PLACEBO_2019": ("2019-02-19", "2019-04-07"),
}
EP_SETS = {
    "QUEUE2": ["COVID_TIGHT", "BEAR2022"],                                      # <- HEADLINE
    "REAL5": ["COVID_TIGHT", "BEAR2022", "COVID_WIDE", "COVID_DD", "DD_2015"],
    "PLACEBO3": ["PLACEBO_2017", "PLACEBO_2013", "PLACEBO_2019"],
}
EPSET_HEAD = "QUEUE2"

REPRO_TOL_SHARPE, REPRO_TOL_DD = 0.030, 0.015
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (the record's)
def fast_run(prices, weights, mask, lag=LAG):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def pack(r):
    c, s, d = fmet(r)
    h = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]))


def verdicts(s, base, spy, cap, floor):
    """PROTOCOL rule 4, both paths; cap/floor passed in so the comparand convention is the
    only difference between two otherwise identical readings."""
    p4a = (s["H1"] > base["H1"]) and (s["H2"] > base["H2"]) and (s["MaxDD"] >= base["MaxDD"])
    legs = dict(H1=s["H1"] > spy["H1"], H2=s["H2"] > spy["H2"],
                DDCAP=s["MaxDD"] >= cap, CAGRFLOOR=s["CAGR"] >= floor)
    fails = "+".join(k for k, v in legs.items() if not v) or "-"
    return bool(p4a), all(legs.values()), fails


# ------------------------------------------------------------------ panels and books
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def gate_mult(br, thr, depth, idx):
    below = (br < thr)
    m = pd.Series(1.0, index=idx).where(~below, 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def shelf_books(U, B):
    """Idea 851's shelf, restated verbatim so the two runs are directly comparable: every
    committed 4b KEEP-candidate memo this lane can rebuild FROM ITS OWN RULES WORDING."""
    out = {}
    out["u56-v2band-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.03, 1.00), memo=(0.1155, 1.2067, -0.1570),
        src="2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md")
    out["u56-band008-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.08, 1.00), memo=(0.1137, 1.1439, -0.1905),
        src="2026-09-11_u56-band008-gross100_4b_cloud_MEMO.md")

    s, above, vol20 = score(U, vol_scale=False)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    out["u56-top20-band-m20"] = dict(
        panel="U56", freq="W", W=(rank <= 20).astype(float) * 0.75 / 20,
        memo=(0.1287, 1.112, -0.1722), src="2026-09-07_u56-top20-band-m20_4b_B_MEMO.md")

    ab = (U > U.rolling(200).mean()).astype(float)
    n = ab.sum(axis=1).replace(0, np.nan)
    out["u56-marsrespread-gross075"] = dict(
        panel="U56", freq="W", W=ab.div(n, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1155, 1.0914, None), src="2026-09-11_u56-marsrespread-gross075_4b_C_MEMO.md")

    rel = U / U.rolling(200).mean() - 1
    sel = (rel.rank(axis=1, ascending=False, pct=True) <= 0.50) & rel.notna()
    k = sel.astype(float).sum(axis=1).replace(0, np.nan)
    out["u56-quantile50-respread-M"] = dict(
        panel="U56", freq="M", W=sel.astype(float).div(k, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1547, 1.2359, -0.1980), src="2026-09-11_u56-quantile50-respread-M_4b_B_MEMO.md")

    r6 = B / B.shift(126) - 1
    out["b136-r620-gross065-W"] = dict(
        panel="B136", freq="W", W=(r6.rank(axis=1, ascending=False) <= 20).astype(float) * 0.65 / 20,
        memo=(0.1499, 1.1264, -0.1943), src="2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md")

    for nm, px, q, dep, memo, src in (
            ("b136-qroll-q012-w1008-d050-g100", B, 0.12, 0.50, (0.1430, 1.1121, -0.1731),
             "2026-09-12_b136-qroll-q012-w1008-depth050-gross100_4b_cloud_MEMO.md"),
            ("u56-k8-qroll-q017-w1008-d100-g100", U, 0.17, 1.00, (0.1416, 1.2226, -0.1479),
             "2026-09-14_u56-k8-qroll-q017-w1008-depth100-gross100_LIVELEG_4b_cloud_MEMO.md")):
        elig = eligible_mask(px).astype(float)
        nn = elig.sum(axis=1).replace(0, np.nan)
        base = elig.div(nn, axis=0).fillna(0.0)
        br = breadth(px)
        thr = br.rolling(1008, min_periods=1008).quantile(q)
        out[nm] = dict(panel=("B136" if px is B else "U56"), freq="W",
                       W=base.mul(gate_mult(br, thr, dep, px.index), axis=0),
                       memo=memo, src=src)
    return out


def grid_books(U, B):
    """A mechanical ladder that was never memo-selected (851's grid, restated)."""
    out = {}
    for pname, px in (("U56", U), ("B136", B)):
        for band, g in product((0.03, 0.08), (0.50, 0.75, 1.00)):
            out[f"{pname}-band{band:.2f}-g{g:.2f}"] = dict(
                panel=pname, freq="W", W=rules_v2_weights(px, band, g), memo=None, src="GRID")
        elig = eligible_mask(px).astype(float)
        nn = elig.sum(axis=1).replace(0, np.nan)
        base = elig.div(nn, axis=0).fillna(0.0)
        br = breadth(px)
        for q, w, dep in product((0.12, 0.17), (252, 504, 1008), (0.50, 1.00)):
            thr = br.rolling(w, min_periods=w).quantile(q)
            out[f"{pname}-qroll-q{q:.2f}-w{w}-d{dep:.2f}"] = dict(
                panel=pname, freq="W", W=base.mul(gate_mult(br, thr, dep, px.index), axis=0),
                memo=None, src="GRID")
    return out


def main():
    t0 = time.time()
    P(f"# Idea 861 — should PROTOCOL 4b price its DD CAP against an EPISODE-STRIPPED "
      f"COMPARAND? ({DATE}, cloud lane)")
    P(f"# 2 tuned dials: BOOK SET {SETS} x EPISODE SET {list(EP_SETS)}; ALL grid points reported.")
    P(f"# HEADLINE episode set = {EPSET_HEAD} (the queue's own 2020 + 2022), declared before "
      f"any number is read.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent lists; every LEVEL is optimistic.")

    U = load_universe().dropna(how="all").ffill()
    B = load_universe(broad=True).dropna(how="all").ffill()
    PX = {"U56": U, "B136": B}
    idx = U.index
    assert B.index.equals(idx), "panels must share a calendar for a common splice"
    start = idx[WARMUP]
    eidx = idx[idx >= start]
    P(f"\n   U56 {U.shape}, B136 {B.shape}; scored from {start.date()} ({len(eidx)} days) "
      f"to {eidx[-1].date()}")

    # ---- episodes, COVID_DD resolved from the data --------------------------------------
    EPD = dict(EPISODES)
    s = U["SPY"].loc["2019-06-01":]
    pk = s.loc[:"2020-02-19"].idxmax()
    lvl = float(s.loc[pk])
    rec = s.loc[pk:][s.loc[pk:] >= lvl]
    EPD["COVID_DD"] = (str(pk.date()), str((rec.index[1] if len(rec) > 1 else s.index[-1]).date()))
    P("   episodes (COVID_DD resolved from SPY itself):")
    for kk, vv in EPD.items():
        n = int(((eidx >= pd.Timestamp(vv[0])) & (eidx <= pd.Timestamp(vv[1]))).sum())
        P(f"      {kk:<13} {vv}  {n} scored days")
    P("   episode SETS:")
    for kk, vv in EP_SETS.items():
        P(f"      {kk:<9} {vv}")

    def keep_mask(ep):
        if ep is None:
            return np.ones(len(eidx), bool)
        a, b = EPD[ep]
        return ~((eidx >= pd.Timestamp(a)) & (eidx <= pd.Timestamp(b)))

    oos_mask = np.asarray(eidx >= pd.Timestamp(OOS_START))
    is_mask = ~oos_mask

    # ---- returns ---------------------------------------------------------------------------
    books = {}
    for setname, maker in (("SHELF", shelf_books), ("GRID", grid_books)):
        for nm, b in maker(U, B).items():
            px = PX[b["panel"]]
            r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
            b["net"] = {c: (r - t * c / 1e4).loc[start:].values for c in RUNGS}
            b["set"] = setname
            books[nm] = b
    spy = U["SPY"].pct_change().fillna(0.0).loc[start:].values
    v2 = {p: {c: (lambda rt: (rt[0] - rt[1] * c / 1e4).loc[start:].values)(
        fast_run(PX[p], rules_v2_weights(PX[p]), rebalance_mask(PX[p].index, FREQ)))
        for c in RUNGS} for p in PX}
    v1 = {p: {c: (lambda rt: (rt[0] - rt[1] * c / 1e4).loc[start:].values)(
        fast_run(PX[p], rules_v1_weights(PX[p]), rebalance_mask(PX[p].index, FREQ)))
        for c in RUNGS} for p in PX}

    # ----------------------------------------------------------------- GATES
    P("\n### GATES (printed before any new number)")
    ok = True
    nm0 = "u56-v2band-gross100"
    a = pack(books[nm0]["net"][RUNG_HEAD])
    b_ = pack(books[nm0]["net"][RUNG_HEAD][keep_mask(None)])
    g1 = max(abs(a[k] - b_[k]) for k in a)
    P(f"   G1 empty splice == unspliced on {nm0}: max|d| {g1:.3e} {'PASS' if g1 == 0.0 else 'FAIL'}")
    ok &= g1 == 0.0

    for nm, b in books.items():
        if b["set"] != "SHELF":
            continue
        m = pack(b["net"][RUNG_HEAD])
        mm = b["memo"]
        dS = abs(m["Sharpe"] - mm[1])
        dD = abs(m["MaxDD"] - mm[2]) if mm[2] is not None else 0.0
        b["repro"] = (dS <= REPRO_TOL_SHARPE) and (dD <= REPRO_TOL_DD)
        P(f"   G2 {nm:<34} {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}  vs memo "
          f"{mm[0]:.2%} / {mm[1]:.4f} / "
          f"{('%.2f%%' % (100 * mm[2])) if mm[2] is not None else '   n/a'}  "
          f"dSharpe {dS:.4f} dMaxDD {dD:.4f}  {'REPRODUCES' if b['repro'] else 'EXCLUDED'}")
    n_rep = sum(1 for b in books.values() if b["set"] == "SHELF" and b["repro"])
    n_sh_all = sum(1 for b in books.values() if b["set"] == "SHELF")
    P(f"   G2 {n_rep} of {n_sh_all} committed 4b memos reproduce inside tolerance "
      f"(Sharpe {REPRO_TOL_SHARPE}, MaxDD {REPRO_TOL_DD:.1%}).")
    P("   G2 NOT REBUILT AT ALL (named, outside the shelf, as in 851): "
      "2026-09-12_b136-corr-hi-q017-w252-d050-D-g100 — neither natural reading of its memo's "
      "tail convention reproduces its headline; excluded and reported as unreproduced. NOTE: "
      "this is idea 814's own book, the one the queue's question is ABOUT, so its 5.12pp -> "
      "-0.41pp margin is quoted from 814's committed file, not re-derived here.")
    ok &= n_rep >= 6

    sm = pack(spy)
    g3 = max(abs(sm["CAGR"] - 0.1516), abs(sm["Sharpe"] - 0.8861), abs(sm["MaxDD"] + 0.3372))
    P(f"   G3 SPY full {sm['CAGR']:.4%} / {sm['Sharpe']:.4f} / {sm['MaxDD']:.4%} vs committed "
      f"15.16% / 0.8861 / -33.72%: max|d| {g3:.2e} {'PASS' if g3 < 1e-3 else 'FAIL'}")
    ok &= g3 < 1e-3

    spy_ct = pack(spy[keep_mask("COVID_TIGHT")])
    g4a, g4b = abs(spy_ct["MaxDD"] + 0.2450), abs(0.60 * spy_ct["MaxDD"] + 0.1470)
    P(f"   G4 851 REPLICATION: SPY MaxDD ex-COVID_TIGHT {spy_ct['MaxDD']:.4%} vs 851's "
      f"-24.50% (|d| {g4a:.4f}); re-priced cap {0.60 * spy_ct['MaxDD']:.4%} vs -14.70% "
      f"(|d| {g4b:.4f}): {'PASS' if max(g4a, g4b) < 5e-4 else 'FAIL'}")
    ok &= max(g4a, g4b) < 5e-4
    P(f"   GATES so far: {'ALL PASS' if ok else 'FAILURE — nothing below is read'}")
    assert ok

    # ----------------------------------------------------------------- PART A: margin census
    P("\n### PART A — THE MARGIN CENSUS: every book x strip, cap RE-PRICED on the same leg")
    P("   (margin = book MaxDD - cap, in pp; positive = clears.  The record publishes PASS/FAIL "
      "only, so these margins are new.)")
    rows = []
    strips = [None] + list(EPISODES)
    for nm, b in books.items():
        if b["set"] == "SHELF" and not b.get("repro", False):
            continue
        for ep, rung in product(strips, RUNGS):
            km = keep_mask(ep)
            sbk = pack(b["net"][rung][km])
            base = pack(v2[b["panel"]][rung][km])
            sp = pack(spy[km])
            cap, flo = 0.60 * sp["MaxDD"], 0.70 * sp["CAGR"]
            p4a, p4b, fails = verdicts(sbk, base, sp, cap, flo)
            _, p4b_fix, _ = verdicts(sbk, base, sp, FIXED_CAP, FIXED_FLOOR)
            rows.append(dict(book=nm, set=b["set"], panel=b["panel"],
                             strip=("NONE" if ep is None else ep), rung=rung,
                             days=int(km.sum()), CAGR=sbk["CAGR"], Sharpe=sbk["Sharpe"],
                             MaxDD=sbk["MaxDD"], H1=sbk["H1"], H2=sbk["H2"],
                             cap=cap, floor=flo, dd_margin=sbk["MaxDD"] - cap,
                             cagr_margin=sbk["CAGR"] - flo, SPY_MaxDD=sp["MaxDD"],
                             SPY_CAGR=sp["CAGR"], pass4a=p4a, pass4b=p4b,
                             pass4b_fixedbar=p4b_fix, fail4b=fails))
    MG = pd.DataFrame(rows)
    MG.to_csv(f"{OUT}.margins.csv", index=False)
    P(f"   {len(MG)} rows ({MG.book.nunique()} books x {len(strips)} strips x {len(RUNGS)} rungs) "
      f"written to .margins.csv")

    hd = MG[(MG.rung == RUNG_HEAD) & (MG.strip == "NONE")]
    for st in SETS:
        t = hd[hd.set == st].sort_values("dd_margin")
        npass = int(t.pass4b.sum())
        P(f"\n   {st} — UNSTRIPPED 4b, 10 bps: {npass} of {len(t)} books pass; DD-leg margins "
          f"(book MaxDD - cap {FIXED_CAP:.2%}) for the PASSING rows:")
        for r in t[t.pass4b].sort_values("dd_margin").itertuples():
            P(f"      {r.book:<34} MaxDD {r.MaxDD:>8.2%}  cap {r.cap:>8.2%}  "
              f"margin {100 * r.dd_margin:>+7.2f} pp")
        if npass:
            mm = t[t.pass4b].dd_margin
            P(f"      -> median {100 * mm.median():+.2f} pp, min {100 * mm.min():+.2f} pp, "
              f"max {100 * mm.max():+.2f} pp; {int((mm < 0.01).sum())} of {npass} clear by "
              f"under 1.00 pp")
    shp = hd[(hd.set == "SHELF") & hd.pass4b].dd_margin
    P(f"\n   H_MARGIN (median SHELF passing DD margin > 2.00 pp): "
      f"{'PASS' if shp.median() > 0.02 else 'FAIL'} ({100 * shp.median():+.2f} pp)")

    # ----------------------------------------------------------------- PART B: the clause
    P("\n### PART B — THE CLAUSE.  4b-DD-STRIP: the DD leg must clear at EVERY single-episode "
      "strip in the set, cap re-priced on each stripped leg.  Statistic = MINMARGIN.")
    crows = []
    for nm in MG.book.unique():
        for esn, rung in product(EP_SETS, RUNGS):
            sub = MG[(MG.book == nm) & (MG.rung == rung)]
            base_row = sub[sub.strip == "NONE"].iloc[0]
            eps = EP_SETS[esn]
            m = sub[sub.strip.isin(eps)]
            minm = float(m.dd_margin.min())
            bind = m.loc[m.dd_margin.idxmin()].strip
            # the clause is a CONJUNCTION laid on top of the unstripped 4b verdict
            clause_ok = bool(base_row.pass4b) and (minm >= 0)
            crows.append(dict(book=nm, set=base_row.set, panel=base_row.panel, epset=esn,
                              rung=rung, base_pass4b=bool(base_row.pass4b),
                              base_margin=float(base_row.dd_margin), minmargin=minm,
                              binding_strip=bind, clause_pass=clause_ok,
                              killed_by_clause=bool(base_row.pass4b) and not clause_ok,
                              all_legs_pass4b_everystrip=bool(base_row.pass4b) and
                              bool(m.pass4b.all())))
    CL = pd.DataFrame(crows)
    CL.to_csv(f"{OUT}.clause.csv", index=False)

    # G5 — the clause really is a conjunction: MINMARGIN is <= every single-strip margin.
    g5bad = 0
    for r in CL.itertuples():
        sub = MG[(MG.book == r.book) & (MG.rung == r.rung) & MG.strip.isin(EP_SETS[r.epset])]
        if r.minmargin > sub.dd_margin.min() + 1e-12:
            g5bad += 1
    P(f"   G5 the clause is a conjunction (MINMARGIN <= every single-strip margin) on "
      f"{len(CL) - g5bad} of {len(CL)} rows: {'PASS' if g5bad == 0 else 'FAIL'}")
    assert g5bad == 0

    for st, rung in product(SETS, RUNGS):
        t = CL[(CL.set == st) & (CL.rung == rung)]
        nbase = int(t[t.epset == EPSET_HEAD].base_pass4b.sum())
        P(f"\n   {st} @ {rung:.0f} bps — {nbase} unstripped 4b passes; the clause keeps:")
        for esn in EP_SETS:
            u = t[t.epset == esn]
            P(f"      {esn:<9} keeps {int(u.clause_pass.sum()):>2} of {nbase}  "
              f"(kills {int(u.killed_by_clause.sum())});  FULL-4b-at-every-strip (all four legs, "
              f"not just DD) keeps {int(u.all_legs_pass4b_everystrip.sum()):>2}")

    hdc = CL[(CL.set == "SHELF") & (CL.rung == RUNG_HEAD)]
    nb = int(hdc[hdc.epset == EPSET_HEAD].base_pass4b.sum())
    kq = int(hdc[hdc.epset == EPSET_HEAD].killed_by_clause.sum())
    kp = int(hdc[hdc.epset == "PLACEBO3"].killed_by_clause.sum())
    P(f"\n   SHELF book by book @ {RUNG_HEAD:.0f} bps, {EPSET_HEAD}:")
    P(f"      {'book':<34}{'base 4b':>9}{'base mgn':>10}{'MINMARGIN':>11}{'binds at':>14}"
      f"{'clause':>9}")
    for r in hdc[hdc.epset == EPSET_HEAD].sort_values("minmargin").itertuples():
        P(f"      {r.book:<34}{('PASS' if r.base_pass4b else 'fail'):>9}"
          f"{100 * r.base_margin:>+9.2f} {100 * r.minmargin:>+10.2f}{r.binding_strip:>14}"
          f"{('KEEP' if r.clause_pass else 'DROP'):>9}")
    P(f"\n   H_CLAUSE (QUEUE2 removes >= 1/3 of the SHELF's unstripped 4b passes): "
      f"{'PASS' if nb and kq >= nb / 3 else 'FAIL'} ({kq} of {nb})")
    P(f"   H_PLACEBO (PLACEBO3 removes strictly fewer than QUEUE2): "
      f"{'PASS' if kp < kq else 'FAIL'} (placebo {kp} vs real {kq})")

    # ----------------------------------------------------------------- PART B2: shuffle null
    P("\n### PART B2 — THE CLAUSE'S OWN NULL: 20 random strips of COVID_TIGHT's length "
      f"(seed {SEED}), same conjunctive clause, SHELF @ {RUNG_HEAD:.0f} bps")
    rng = np.random.default_rng(SEED)
    L = int((~keep_mask("COVID_TIGHT")).sum())
    _eq = np.cumprod(1.0 + spy)
    _dd = _eq / np.maximum.accumulate(_eq) - 1.0
    dd_t = int(np.argmin(_dd))
    dd_p = int(np.argmax(_eq[:dd_t + 1]))
    P(f"   SPY's binding MaxDD episode runs {eidx[dd_p].date()} -> {eidx[dd_t].date()} "
      f"({_dd[dd_t]:.2%}).  The cap can only move if a strip INTERSECTS it, so the null below "
      f"is expected to be inert except on draws that do; that expectation is itself the result.")
    shelf_books_ok = [nm for nm, b in books.items()
                      if b["set"] == "SHELF" and b.get("repro", False)]
    srows = []
    for d in range(N_SHUFFLE):
        i0 = int(rng.integers(0, len(eidx) - L))
        km = np.ones(len(eidx), bool)
        km[i0:i0 + L] = False
        sp = pack(spy[km])
        cap = 0.60 * sp["MaxDD"]
        kills = 0
        for nm in shelf_books_ok:
            basep = bool(MG[(MG.book == nm) & (MG.strip == "NONE") &
                            (MG.rung == RUNG_HEAD)].pass4b.iloc[0])
            if not basep:
                continue
            mdd = pack(books[nm]["net"][RUNG_HEAD][km])["MaxDD"]
            kills += int((mdd - cap) < 0)
        srows.append(dict(draw=d, start=str(eidx[i0].date()), end=str(eidx[i0 + L - 1].date()),
                          SPY_MaxDD=sp["MaxDD"], cap=cap, kills=kills,
                          hits_spy_dd=bool(i0 < dd_t and i0 + L > dd_p)))
    SHF = pd.DataFrame(srows)
    SHF.to_csv(f"{OUT}.shuffle.csv", index=False)
    P(SHF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    q90 = float(np.quantile(SHF.kills, 0.90))
    # the real single-strip kill counts, for the same statistic
    real_kills = {}
    for ep in ["COVID_TIGHT", "BEAR2022"]:
        u = MG[(MG.set == "SHELF") & (MG.rung == RUNG_HEAD) & (MG.strip == ep)]
        base_pass = MG[(MG.set == "SHELF") & (MG.rung == RUNG_HEAD) &
                       (MG.strip == "NONE")].set_index("book").pass4b
        real_kills[ep] = int(sum((not (r.dd_margin >= 0)) and base_pass[r.book]
                                 for r in u.itertuples()))
    P(f"   shuffle kills: mean {SHF.kills.mean():.2f}, median {SHF.kills.median():.1f}, "
      f"p90 {q90:.1f}, max {SHF.kills.max()}; {int(SHF.hits_spy_dd.sum())} of {N_SHUFFLE} draws "
      f"intersect SPY's binding MaxDD episode, and SPY's MaxDD is unchanged at "
      f"{SHF.SPY_MaxDD.min():.2%}..{SHF.SPY_MaxDD.max():.2%} on every draw")
    P(f"   real single-strip kills: COVID_TIGHT {real_kills['COVID_TIGHT']}, "
      f"BEAR2022 {real_kills['BEAR2022']}")
    P(f"   H_SHUFFLE (COVID_TIGHT kill count >= shuffle p90): "
      f"{'PASS' if real_kills['COVID_TIGHT'] >= q90 else 'FAIL'} "
      f"({real_kills['COVID_TIGHT']} vs p90 {q90:.1f})")

    # ----------------------------------------------------------------- PART C: rule 8
    P("\n### PART C — RULE 8 WITH THE CLAUSE AS A SELECTOR.  Dial chosen on 2009-2016 ALONE; "
      "OOS 2017-2026 read ONCE per (panel, episode set, chooser).")
    P("   UNSCREENED: argmax IS Sharpe over the GRID pool.")
    P("   SCREENED  : argmax IS Sharpe over the GRID pool RESTRICTED to books whose DD leg "
      "clears at every strip of the set, with everything (pool, strips, cap) computed on the "
      "IS window only.  A book that never qualifies in sample cannot be picked.")
    wrows = []
    for pname, esn in product(PX, EP_SETS):
        pool = [(nm, b) for nm, b in books.items()
                if b["set"] == "GRID" and b["panel"] == pname]

        def is_sh(b):
            return fsharpe(b["net"][RUNG_HEAD][is_mask])

        def is_qualifies(b):
            for ep in EP_SETS[esn]:
                km = keep_mask(ep) & is_mask
                if km.sum() < 250:
                    continue
                sp_is = pack(spy[km])
                if pack(b["net"][RUNG_HEAD][km])["MaxDD"] < 0.60 * sp_is["MaxDD"]:
                    return False
            return True

        elig_pool = [(nm, b) for nm, b in pool if is_qualifies(b)]
        for chooser, cand in (("UNSCREENED", pool), ("SCREENED", elig_pool)):
            if not cand:
                wrows.append(dict(panel=pname, epset=esn, chooser=chooser, pick="NONE-ELIGIBLE",
                                  pool_n=len(pool), elig_n=0))
                continue
            best = max(cand, key=lambda kv: is_sh(kv[1]))
            sel = oos_mask
            sbk = pack(best[1]["net"][RUNG_HEAD][sel])
            base = pack(v2[pname][RUNG_HEAD][sel])
            old = pack(v1[pname][RUNG_HEAD][sel])
            sp = pack(spy[sel])
            p4a, p4b, fails = verdicts(sbk, base, sp, 0.60 * sp["MaxDD"], 0.70 * sp["CAGR"])
            _, p4b_fix, fails_fix = verdicts(sbk, base, sp, FIXED_CAP, FIXED_FLOOR)
            # does the OOS pick itself satisfy the clause OUT of sample?
            oos_min = min((pack(best[1]["net"][RUNG_HEAD][keep_mask(ep) & oos_mask])["MaxDD"]
                           - 0.60 * pack(spy[keep_mask(ep) & oos_mask])["MaxDD"])
                          for ep in EP_SETS[esn])
            wrows.append(dict(panel=pname, epset=esn, chooser=chooser, pick=best[0],
                              pool_n=len(pool), elig_n=len(elig_pool),
                              IS_Sharpe=is_sh(best[1]), OOS_CAGR=sbk["CAGR"],
                              OOS_Sharpe=sbk["Sharpe"], OOS_MaxDD=sbk["MaxDD"],
                              OOS_H1=sbk["H1"], OOS_H2=sbk["H2"],
                              V2_OOS_CAGR=base["CAGR"], V2_OOS_Sharpe=base["Sharpe"],
                              V2_OOS_MaxDD=base["MaxDD"], V1_OOS_Sharpe=old["Sharpe"],
                              SPY_OOS_CAGR=sp["CAGR"], SPY_OOS_Sharpe=sp["Sharpe"],
                              SPY_OOS_MaxDD=sp["MaxDD"], pass4a=p4a, pass4b=p4b, fail4b=fails,
                              pass4b_fixedbar=p4b_fix, OOS_clause_minmargin=oos_min,
                              OOS_clause_pass=bool(p4b and oos_min >= 0)))
    WF = pd.DataFrame(wrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    for r in WF.itertuples():
        P(f"   {r.panel:<5} {r.epset:<9} {r.chooser:<11} pool {r.pool_n:>2}/elig {r.elig_n:>2}  "
          f"pick {r.pick:<28} IS {r.IS_Sharpe:.4f}  OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / "
          f"{r.OOS_MaxDD:.2%} | v2 {r.V2_OOS_CAGR:.2%}/{r.V2_OOS_Sharpe:.4f}/{r.V2_OOS_MaxDD:.2%}"
          f" | SPY {r.SPY_OOS_CAGR:.2%}/{r.SPY_OOS_Sharpe:.4f}/{r.SPY_OOS_MaxDD:.2%} | "
          f"4b {'PASS' if r.pass4b else 'FAIL ' + r.fail4b}  4a {'PASS' if r.pass4a else 'FAIL'}"
          f"  | OOS clause minmargin {100 * r.OOS_clause_minmargin:+.2f} pp "
          f"{'KEEP' if r.OOS_clause_pass else 'DROP'}")
    deltas = []
    for pname, esn in product(PX, EP_SETS):
        u = WF[(WF.panel == pname) & (WF.epset == esn)].set_index("chooser")
        if "SCREENED" in u.index and "UNSCREENED" in u.index:
            deltas.append(float(u.loc["SCREENED"].OOS_Sharpe - u.loc["UNSCREENED"].OOS_Sharpe))
    nbetter = sum(1 for d in deltas if d > 0)
    P(f"\n   SCREENED minus UNSCREENED OOS Sharpe over {len(deltas)} (panel, episode set) "
      f"cells: {', '.join(f'{d:+.4f}' for d in deltas)}; median {np.median(deltas):+.4f}, "
      f"better in {nbetter} of {len(deltas)}")
    P(f"   H_R8 (the clause does NOT buy OOS Sharpe): "
      f"{'PASS' if nbetter <= len(deltas) / 2 else 'FAIL'} "
      f"({nbetter} of {len(deltas)} cells improved)")

    P(f"\n### done in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

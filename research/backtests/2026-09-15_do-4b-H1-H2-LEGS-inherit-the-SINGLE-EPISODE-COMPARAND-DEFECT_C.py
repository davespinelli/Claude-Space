#!/usr/bin/env python3
"""Idea 865 (lane C, 2026-09-15) — do 4b's H1/H2 LEGS inherit the SAME SINGLE-EPISODE
COMPARAND DEFECT as its DD CAP?

QUESTION (QUEUE idea 865, verbatim)
    ideas 814/861 priced 4b's drawdown cap against an episode-stripped comparand and found it
    is a statement about SPY's 2020.  Idea 863 hit the identical defect through a DIFFERENT leg:
    its rule-8 pick fails 4b on the 2022-free corpus purely on H2, because deleting 2022 removes
    the drawdown from SPY's second half and raises the bar the arm exists to clear.  Census the
    record's committed 4b passes for how many of their H1/H2 margins survive removing one
    episode from BOTH sides, and propose the PROTOCOL line.  Max 2 params (episode set, pass set)

WHAT IS NEW AGAINST 861 (the same machinery, the OTHER leg).  861 censused the DD leg's
    margins and priced the clause "the DD leg must clear at every single-episode strip".  It
    found the clause is a ONE-EPISODE clause: COVID_TIGHT bound 16 of 16 kills and BEAR2022
    killed nothing, because SPY's binding MaxDD is a single 33-day window and a strip that
    misses it cannot move the cap.  865 asks the same question of the TWO LEGS THAT ARE NOT A
    RATIO AGAINST A SINGLE EPISODE:

      (A) THE HALF-MARGIN CENSUS.  4b's H1 and H2 legs are `book half Sharpe > SPY half Sharpe`.
          The record publishes the book's H1/H2 (every LEADERBOARD row has the column) and the
          comparand's, but never the MARGIN, and never the margin under a strip.  Part A is
          every committed 4b pass's H1 and H2 margin in Sharpe units, unstripped and at every
          single-episode strip, with the comparand re-read on the SAME shortened calendar.

      (B) THE CLAUSE.  4b-HALF-STRIP: BOTH half legs must clear at EVERY single-episode strip
          in a declared set, SPY's halves re-read on each stripped leg.  Statistic HALFMIN =
          min over (strip x {H1, H2}) of the margin.  A conjunction, so it can only remove.

      (B1) THE DECOMPOSITION THAT ANSWERS THE QUESTION AS ASKED.  "Inherit the COMPARAND defect"
          is a claim about WHICH SIDE MOVES.  Every strip's margin change decomposes exactly:
             d margin = d(book half Sharpe) - d(SPY half Sharpe) = dBOOK - dCOMP
          Part B1 attributes every kill to its side.  If dCOMP carries it, the half legs have
          the same disease as the DD cap in a different organ.  If dBOOK carries it, they do
          not, and the queue's reading of 863 is a coincidence of one arm.

      (B2) THE BOUNDARY CHANNEL, which the DD leg does not have.  The record splits halves BY
          COUNT (`h = len(r) // 2`, baseline._row).  Deleting days MOVES THE MIDPOINT, so a
          strip changes which days are in which half even where it changes no return.  Control:
          the DATE convention, halves split at the unstripped midpoint DATE and the strip
          applied afterwards, so the boundary is frozen.  Reported at every cell.  A defect that
          vanishes under DATE is a convention artefact, not a comparand defect.

      (B3) CALIBRATION.  PLACEBO3 (crash-free strips of the same calendar shape) and a 20-draw
          shuffle-strip null at COVID_TIGHT's length, seed 865.  The half legs move on EVERY
          strip (both sides do), so unlike 861's DD null this one is NOT inert by construction,
          and its dispersion is the bar the real episodes have to clear.

      (C) RULE 8 WITH THE CLAUSE AS A SELECTOR.  Dial chosen on 2009-2016 alone, OOS 2017-2026
          read once per (panel, episode set, chooser).  If the clause costs OOS Sharpe it is a
          reporting requirement, not an alpha filter, and the PROTOCOL line must say so.

TUNED PARAMETERS: exactly TWO, the two the queue names.
    (1) PASS SET in {SHELF, GRID}  — 861's book sets, restated verbatim so the two runs are
            directly comparable leg against leg.
            SHELF  every committed 4b KEEP-candidate memo this lane rebuilds from its own RULES
                   wording and gates against its published headline.  Non-reproducers are NAMED
                   and EXCLUDED.
            GRID   a mechanical band x gross x QROLL ladder that was never memo-selected.
    (2) EPISODE SET in {QUEUE2, REAL5, PLACEBO3}
            QUEUE2    {COVID_TIGHT, BEAR2022}   <- HEADLINE, the queue's own two
            REAL5     QUEUE2 + {COVID_WIDE, COVID_DD, DD_2015}
            PLACEBO3  {PLACEBO_2017, PLACEBO_2013, PLACEBO_2019}   (calibration only)
    The half convention (COUNT / DATE) is a reported CONTROL at every cell, not a third dial:
    COUNT is the record's own and is the headline everywhere.

DELETION CONVENTION: SPLICE, from ideas 851/861 — the episode's trading days are removed from
    every series (book, RULES v2 baseline, SPY) before any moment is taken, "from BOTH sides".

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_MARGIN    the committed 4b passes' half legs are not perched on the bar: the median
                unstripped SHELF HALFMIN (the weaker of H1, H2) exceeds 0.20 Sharpe units.
    H_INHERIT   the QUEUE2 half-clause removes at least one third of the SHELF's unstripped 4b
                passes, i.e. the half legs DO inherit a strip sensitivity of the same order the
                DD leg showed (861: 3 of 8).
    H_COMPARAND among the kills, the comparand side carries the move: median |dCOMP| > median
                |dBOOK|.  This is the queue's own reading of 863 and the reason the idea exists.
    H_BEAR      BEAR2022 binds the half legs materially more than it bound the DD leg, where it
                killed EXACTLY ZERO of 16.  Declared as: BEAR2022's own single-strip half-kill
                count on the SHELF is >= 1.
    H_BOUNDARY  the DATE convention (frozen midpoint) gives a STRICTLY LOWER QUEUE2 kill count
                than COUNT, i.e. part of the effect is the midpoint moving, not the episode.
    H_R8        the clause does NOT buy OOS Sharpe (a robustness screen bought with in-sample
                information is not expected to pay out of sample).

GATES (printed before any new number; all must pass)
    G1  the empty splice is the identity (max|d| == 0.0) on a named book.
    G2  every SHELF book reproduces its committed memo headline inside tolerance (Sharpe 0.030,
        MaxDD 1.5 pp).  Books outside are named and dropped.
    G3  SPY reproduces the record's committed 4b comparand 15.16% / 0.8861 / -33.72%.
    G4  861 CROSS-RUN REPLICATION: SPY MaxDD ex-COVID_TIGHT == -24.50% and the re-priced cap
        == -14.70% to 0.05 pp, so this run's census is comparable with 861's DD census.
    G5  HALVES PARTITION: for every (book, strip, convention) the two halves are disjoint,
        exhaustive, and the COUNT-convention H1/H2 equal baseline's own `len(r)//2` reading; and
        on the UNSTRIPPED leg the two conventions coincide exactly.
    G6  the clause is a conjunction: HALFMIN <= every single (strip, half) margin, every row.

PROTOCOL: 10 bps per unit turnover (25 also reported), weights decided at close t applied at
    t+1, no shorting, no leverage.  Both KEEP paths evaluated on every row.  Rule 8 run in full.

SURVIVORSHIP, up front: U56 and B136 are CURRENT-constituent lists, so every CAGR and drawdown
    LEVEL is optimistic; the strip-to-strip DIFFERENCE is the durable part.  Nothing here is a
    capital claim and nothing is promoted.

Outputs (committed under research/backtests/):
    .console.txt      full log
    .margins.csv      every book x strip x rung x convention: H1/H2/DD margins and 4a/4b verdicts
    .clause.csv       every book x episode SET x rung x convention: HALFMIN, binding cell, verdict
    .decomp.csv       every book x strip x half: d margin = dBOOK - dCOMP, with attribution
    .shuffle.csv      the 20-draw shuffle-strip null
    .walkforward.csv  rule 8, screened vs unscreened chooser, per (panel, episode set)

Run: python research/backtests/2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py
Deterministic (seed 865); no network (reads the committed price caches only).
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

DATE = "2026-09-15"
SLUG = "do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

FREQ, LAG, WARMUP, MAX_VOL = "W", 1, 260, 0.60
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED = 865
N_SHUFFLE = 20

FIXED_CAP = -0.2023                 # the record's committed full-sample 4b cap
FIXED_FLOOR = 0.70 * 0.151631       # and CAGR floor

SETS = ["SHELF", "GRID"]
CONVS = ["COUNT", "DATE"]
CONV_HEAD = "COUNT"                 # the record's own (baseline._row)

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


def pack(r, h1=None, h2=None):
    """Full-sample moments plus the two half Sharpes.  h1/h2 are boolean selectors INTO r; when
    absent the record's own COUNT convention (`len(r)//2`) is used."""
    c, s, d = fmet(r)
    if h1 is None:
        k = len(r) // 2
        s1, s2 = fsharpe(r[:k]), fsharpe(r[k:])
    else:
        s1, s2 = fsharpe(r[h1]), fsharpe(r[h2])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=s1, H2=s2)


def verdicts(s, base, spy, cap, floor):
    """PROTOCOL rule 4, both paths."""
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
    """861's shelf, restated verbatim so the DD census and this half census are comparable."""
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
    """861's mechanical ladder, restated."""
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
    P(f"# Idea 865 — do 4b's H1/H2 LEGS inherit the SAME SINGLE-EPISODE COMPARAND DEFECT as its "
      f"DD CAP? ({DATE}, lane C)")
    P(f"# 2 tuned dials: PASS SET {SETS} x EPISODE SET {list(EP_SETS)}; ALL grid points reported.")
    P(f"# half convention {CONVS} is a reported CONTROL at every cell; headline = {CONV_HEAD} "
      f"(the record's own, baseline._row `h = len(r)//2`).")
    P(f"# HEADLINE episode set = {EPSET_HEAD} (the queue's own 2020 + 2022), declared first.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent lists; every LEVEL is optimistic.")

    U = load_universe().dropna(how="all").ffill()
    B = load_universe(broad=True).dropna(how="all").ffill()
    # The broad cache is refreshed weekly (PROTOCOL rule 9) and today runs one session behind the
    # U56 cache.  A common splice needs ONE calendar, so both panels are truncated to their
    # intersection and the truncation is stated.  861 ran on a day when the two already agreed.
    if not U.index.equals(B.index):
        common = U.index.intersection(B.index)
        P(f"\n   CALENDAR: U56 ends {U.index[-1].date()}, B136 ends {B.index[-1].date()} "
          f"(weekly broad cache); both truncated to the common {len(common)} days ending "
          f"{common[-1].date()} — {len(U.index.difference(common))} U56 day(s) dropped.")
        U, B = U.loc[common], B.loc[common]
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

    # ---- THE TWO HALF CONVENTIONS -------------------------------------------------------
    # COUNT: halves of the SURVIVING days (the record's; the midpoint MOVES when days go).
    # DATE : halves split at the UNSTRIPPED midpoint DATE, strip applied afterwards (frozen).
    MID_DATE = eidx[len(eidx) // 2]
    P(f"\n   half conventions: COUNT = len(r)//2 of the surviving days (record's);  "
      f"DATE = frozen at the unstripped midpoint {MID_DATE.date()}")

    def halves(km, conv):
        """Boolean selectors into the SURVIVING return vector r = full[km]."""
        m = int(km.sum())
        if conv == "COUNT":
            k = m // 2
            a = np.zeros(m, bool)
            a[:k] = True
            return a, ~a
        d = np.asarray(eidx[km] < MID_DATE)
        return d, ~d

    HV = {(ep, c): halves(keep_mask(ep), c) for ep in [None] + list(EPISODES) for c in CONVS}

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
    P("   G2 NOT REBUILT AT ALL (named, outside the shelf, as in 851/861): "
      "2026-09-12_b136-corr-hi-q017-w252-d050-D-g100 — neither natural reading of its memo's "
      "tail convention reproduces its headline; excluded and reported as unreproduced.")
    ok &= n_rep >= 6

    sm = pack(spy)
    g3 = max(abs(sm["CAGR"] - 0.1516), abs(sm["Sharpe"] - 0.8861), abs(sm["MaxDD"] + 0.3372))
    P(f"   G3 SPY full {sm['CAGR']:.4%} / {sm['Sharpe']:.4f} / {sm['MaxDD']:.4%} vs committed "
      f"15.16% / 0.8861 / -33.72%: max|d| {g3:.2e} {'PASS' if g3 < 1e-3 else 'FAIL'}")
    P(f"   G3b SPY half Sharpes (the 4b comparand this run is about): H1 {sm['H1']:.4f}  "
      f"H2 {sm['H2']:.4f}")
    ok &= g3 < 1e-3

    spy_ct = pack(spy[keep_mask("COVID_TIGHT")])
    g4a, g4b = abs(spy_ct["MaxDD"] + 0.2450), abs(0.60 * spy_ct["MaxDD"] + 0.1470)
    P(f"   G4 861 REPLICATION: SPY MaxDD ex-COVID_TIGHT {spy_ct['MaxDD']:.4%} vs 861's "
      f"-24.50% (|d| {g4a:.4f}); re-priced cap {0.60 * spy_ct['MaxDD']:.4%} vs -14.70% "
      f"(|d| {g4b:.4f}): {'PASS' if max(g4a, g4b) < 5e-4 else 'FAIL'}")
    ok &= max(g4a, g4b) < 5e-4

    # G5 halves partition + convention identity on the unstripped leg
    g5bad = 0
    for ep in [None] + list(EPISODES):
        km = keep_mask(ep)
        for c in CONVS:
            h1, h2 = HV[(ep, c)]
            if not (h1.sum() + h2.sum() == int(km.sum()) and not (h1 & h2).any()):
                g5bad += 1
    rr = books[nm0]["net"][RUNG_HEAD]
    pc = pack(rr, *HV[(None, "COUNT")])
    pd_ = pack(rr, *HV[(None, "DATE")])
    pn = pack(rr)
    g5c = max(abs(pc["H1"] - pn["H1"]), abs(pc["H2"] - pn["H2"]))
    g5d = max(abs(pc["H1"] - pd_["H1"]), abs(pc["H2"] - pd_["H2"]))
    P(f"   G5 halves disjoint+exhaustive at all {2 * (1 + len(EPISODES))} (strip, convention) "
      f"cells: {g5bad} bad; COUNT == baseline's own len(r)//2 reading: {g5c:.3e}; "
      f"COUNT == DATE on the UNSTRIPPED leg: {g5d:.3e}  "
      f"{'PASS' if g5bad == 0 and g5c == 0.0 and g5d == 0.0 else 'FAIL'}")
    ok &= (g5bad == 0 and g5c == 0.0 and g5d == 0.0)
    P(f"   GATES so far: {'ALL PASS' if ok else 'FAILURE — nothing below is read'}")
    assert ok

    # ----------------------------------------------------------------- PART A: half margins
    P("\n### PART A — THE HALF-MARGIN CENSUS: every book x strip x convention, SPY's halves "
      "RE-READ on the same shortened calendar")
    P("   (margin = book half Sharpe - SPY half Sharpe, in Sharpe units; positive = clears.  "
      "The record publishes the two half Sharpes but never the margin, and never under a strip.)")
    rows = []
    strips = [None] + list(EPISODES)
    for nm, b in books.items():
        if b["set"] == "SHELF" and not b.get("repro", False):
            continue
        for ep, rung, conv in product(strips, RUNGS, CONVS):
            km = keep_mask(ep)
            h1, h2 = HV[(ep, conv)]
            sbk = pack(b["net"][rung][km], h1, h2)
            base = pack(v2[b["panel"]][rung][km], h1, h2)
            sp = pack(spy[km], h1, h2)
            cap, flo = 0.60 * sp["MaxDD"], 0.70 * sp["CAGR"]
            p4a, p4b, fails = verdicts(sbk, base, sp, cap, flo)
            _, p4b_fix, _ = verdicts(sbk, base, sp, FIXED_CAP, FIXED_FLOOR)
            m1, m2 = sbk["H1"] - sp["H1"], sbk["H2"] - sp["H2"]
            rows.append(dict(book=nm, set=b["set"], panel=b["panel"],
                             strip=("NONE" if ep is None else ep), rung=rung, conv=conv,
                             days=int(km.sum()), CAGR=sbk["CAGR"], Sharpe=sbk["Sharpe"],
                             MaxDD=sbk["MaxDD"], H1=sbk["H1"], H2=sbk["H2"],
                             SPY_H1=sp["H1"], SPY_H2=sp["H2"],
                             h1_margin=m1, h2_margin=m2, half_min=min(m1, m2),
                             dd_margin=sbk["MaxDD"] - cap, cagr_margin=sbk["CAGR"] - flo,
                             cap=cap, floor=flo, SPY_MaxDD=sp["MaxDD"], SPY_CAGR=sp["CAGR"],
                             pass4a=p4a, pass4b=p4b, pass4b_fixedbar=p4b_fix, fail4b=fails))
    MG = pd.DataFrame(rows)
    MG.to_csv(f"{OUT}.margins.csv", index=False)
    P(f"   {len(MG)} rows ({MG.book.nunique()} books x {len(strips)} strips x {len(RUNGS)} rungs "
      f"x {len(CONVS)} conventions) written to .margins.csv")

    hd = MG[(MG.rung == RUNG_HEAD) & (MG.strip == "NONE") & (MG.conv == CONV_HEAD)]
    for st in SETS:
        t = hd[hd.set == st]
        npass = int(t.pass4b.sum())
        P(f"\n   {st} — UNSTRIPPED 4b, 10 bps, {CONV_HEAD} halves: {npass} of {len(t)} books "
          f"pass; the HALF-leg margins of the PASSING rows (vs SPY H1 {sm['H1']:.4f} / "
          f"H2 {sm['H2']:.4f}):")
        for r in t[t.pass4b].sort_values("half_min").itertuples():
            P(f"      {r.book:<34} H1 {r.H1:>6.3f} ({r.h1_margin:>+6.3f})   "
              f"H2 {r.H2:>6.3f} ({r.h2_margin:>+6.3f})   HALFMIN {r.half_min:>+6.3f}  "
              f"[DD margin {100 * r.dd_margin:>+6.2f} pp]")
        if npass:
            mm = t[t.pass4b].half_min
            P(f"      -> median HALFMIN {mm.median():+.4f}, min {mm.min():+.4f}, "
              f"max {mm.max():+.4f}; {int((mm < 0.10).sum())} of {npass} clear by under 0.10")
    shp = hd[(hd.set == "SHELF") & hd.pass4b].half_min
    P(f"\n   H_MARGIN (median SHELF passing HALFMIN > 0.20): "
      f"{'PASS' if shp.median() > 0.20 else 'FAIL'} ({shp.median():+.4f})")
    P(f"   [861's companion number, the DD leg, on the same rows: median "
      f"{100 * hd[(hd.set == 'SHELF') & hd.pass4b].dd_margin.median():+.2f} pp]")

    # ----------------------------------------------------------------- PART B: the clause
    P("\n### PART B — THE CLAUSE.  4b-HALF-STRIP: BOTH half legs must clear at EVERY "
      "single-episode strip in the set, SPY's halves re-read on each stripped leg.  "
      "Statistic = HALFMIN over (strip x {H1,H2}).")
    crows = []
    for nm in MG.book.unique():
        for esn, rung, conv in product(EP_SETS, RUNGS, CONVS):
            sub = MG[(MG.book == nm) & (MG.rung == rung) & (MG.conv == conv)]
            base_row = sub[sub.strip == "NONE"].iloc[0]
            eps = EP_SETS[esn]
            m = sub[sub.strip.isin(eps)]
            cells = [(r.strip, "H1", r.h1_margin) for r in m.itertuples()] + \
                    [(r.strip, "H2", r.h2_margin) for r in m.itertuples()]
            bstrip, bhalf, minm = min(cells, key=lambda x: x[2])
            clause_ok = bool(base_row.pass4b) and (minm >= 0)
            crows.append(dict(book=nm, set=base_row.set, panel=base_row.panel, epset=esn,
                              rung=rung, conv=conv, base_pass4b=bool(base_row.pass4b),
                              base_halfmin=float(base_row.half_min), halfmin=minm,
                              binding_strip=bstrip, binding_half=bhalf, clause_pass=clause_ok,
                              killed_by_clause=bool(base_row.pass4b) and not clause_ok,
                              # 861's DD clause on the identical rows, for the leg comparison
                              dd_minmargin=float(m.dd_margin.min()),
                              killed_by_dd_clause=bool(base_row.pass4b) and
                              (float(m.dd_margin.min()) < 0),
                              all_legs_pass4b_everystrip=bool(base_row.pass4b) and
                              bool(m.pass4b.all())))
    CL = pd.DataFrame(crows)
    CL.to_csv(f"{OUT}.clause.csv", index=False)

    g6bad = 0
    for r in CL.itertuples():
        sub = MG[(MG.book == r.book) & (MG.rung == r.rung) & (MG.conv == r.conv) &
                 MG.strip.isin(EP_SETS[r.epset])]
        if r.halfmin > min(sub.h1_margin.min(), sub.h2_margin.min()) + 1e-12:
            g6bad += 1
    P(f"   G6 the clause is a conjunction (HALFMIN <= every (strip, half) margin) on "
      f"{len(CL) - g6bad} of {len(CL)} rows: {'PASS' if g6bad == 0 else 'FAIL'}")
    assert g6bad == 0

    for st, rung, conv in product(SETS, RUNGS, CONVS):
        t = CL[(CL.set == st) & (CL.rung == rung) & (CL.conv == conv)]
        nbase = int(t[t.epset == EPSET_HEAD].base_pass4b.sum())
        P(f"\n   {st} @ {rung:.0f} bps, {conv} halves — {nbase} unstripped 4b passes; the "
          f"HALF clause keeps:")
        for esn in EP_SETS:
            u = t[t.epset == esn]
            P(f"      {esn:<9} keeps {int(u.clause_pass.sum()):>2} of {nbase}  "
              f"(kills {int(u.killed_by_clause.sum())});  the DD clause (861's, same rows) kills "
              f"{int(u.killed_by_dd_clause.sum())};  FULL-4b-at-every-strip keeps "
              f"{int(u.all_legs_pass4b_everystrip.sum()):>2}")

    hdc = CL[(CL.set == "SHELF") & (CL.rung == RUNG_HEAD) & (CL.conv == CONV_HEAD)]
    nb = int(hdc[hdc.epset == EPSET_HEAD].base_pass4b.sum())
    kq = int(hdc[hdc.epset == EPSET_HEAD].killed_by_clause.sum())
    kp = int(hdc[hdc.epset == "PLACEBO3"].killed_by_clause.sum())
    kdd = int(hdc[hdc.epset == EPSET_HEAD].killed_by_dd_clause.sum())
    P(f"\n   SHELF book by book @ {RUNG_HEAD:.0f} bps, {EPSET_HEAD}, {CONV_HEAD} halves:")
    P(f"      {'book':<34}{'base 4b':>9}{'base HM':>9}{'HALFMIN':>9}{'binds at':>22}"
      f"{'clause':>8}{'DD clause':>11}")
    for r in hdc[hdc.epset == EPSET_HEAD].sort_values("halfmin").itertuples():
        P(f"      {r.book:<34}{('PASS' if r.base_pass4b else 'fail'):>9}"
          f"{r.base_halfmin:>+9.3f}{r.halfmin:>+9.3f}"
          f"{(r.binding_strip + '/' + r.binding_half):>22}"
          f"{('KEEP' if r.clause_pass else 'DROP'):>8}"
          f"{('DROP' if r.killed_by_dd_clause else 'keep'):>11}")
    # EROSION: the clause's verdict is binary, but the margin it eats is the reportable number.
    P(f"\n   EROSION of the half margin under {EPSET_HEAD} (the number the record never "
      f"publishes), {CONV_HEAD} halves:")
    for st, rung in product(SETS, RUNGS):
        u = CL[(CL.set == st) & (CL.rung == rung) & (CL.epset == EPSET_HEAD) &
               (CL.conv == CONV_HEAD) & CL.base_pass4b]
        if not len(u):
            continue
        b0, b1 = u.base_halfmin.median(), u.halfmin.median()
        P(f"      {st:<6} @ {rung:>2.0f} bps  median HALFMIN {b0:+.4f} -> {b1:+.4f} "
          f"({100 * (b0 - b1) / b0:.1f}% of the margin eaten); min {u.base_halfmin.min():+.4f} "
          f"-> {u.halfmin.min():+.4f}; rows landing under +0.10: "
          f"{int((u.base_halfmin < 0.10).sum())} -> {int((u.halfmin < 0.10).sum())} of {len(u)}")
    P(f"\n   H_INHERIT (QUEUE2 half clause removes >= 1/3 of the SHELF's unstripped 4b passes): "
      f"{'PASS' if nb and kq >= nb / 3 else 'FAIL'} ({kq} of {nb}; 861's DD clause removed "
      f"{kdd} of the same {nb})")
    P(f"   BINDING STRIP (which episode sets HALFMIN), SHELF @ {RUNG_HEAD:.0f} bps, "
      f"{EPSET_HEAD}: " + ", ".join(
        f"{k} {v}" for k, v in
        hdc[hdc.epset == EPSET_HEAD].binding_strip.value_counts().items()) +
      "  — against 861's DD leg, where BEAR2022 bound 0 of 16 kills.")
    P(f"   H_PLACEBO-style control (PLACEBO3 removes strictly fewer than QUEUE2): "
      f"{'PASS' if kp < kq else 'FAIL'} (placebo {kp} vs real {kq})")

    # ---------------------------------------------- PART B1: which side moves (THE question)
    P("\n### PART B1 — THE DECOMPOSITION.  d margin = d(book half Sharpe) - d(SPY half Sharpe) "
      "= dBOOK - dCOMP, exactly.  'Inherits the COMPARAND defect' is a claim about which term "
      "carries it.")
    drows = []
    for nm in MG.book.unique():
        for ep, rung, conv, half in product(list(EPISODES), RUNGS, CONVS, ["H1", "H2"]):
            sub = MG[(MG.book == nm) & (MG.rung == rung) & (MG.conv == conv)]
            b0 = sub[sub.strip == "NONE"].iloc[0]
            b1 = sub[sub.strip == ep].iloc[0]
            bk = float(getattr(b1, half) - getattr(b0, half))
            cp = float(getattr(b1, f"SPY_{half}") - getattr(b0, f"SPY_{half}"))
            mg0 = float(getattr(b0, f"{half.lower()}_margin"))
            mg1 = float(getattr(b1, f"{half.lower()}_margin"))
            tot = abs(bk) + abs(cp)
            drows.append(dict(book=nm, set=b0.set, panel=b0.panel, strip=ep, rung=rung,
                              conv=conv, half=half, margin0=mg0, margin1=mg1,
                              d_margin=mg1 - mg0, dBOOK=bk, dCOMP=cp,
                              comparand_share=(abs(cp) / tot if tot > 0 else np.nan),
                              side=("COMPARAND" if abs(cp) > abs(bk) else "BOOK"),
                              flips_leg=bool(mg0 >= 0 and mg1 < 0),
                              base_pass4b=bool(b0.pass4b)))
    DC = pd.DataFrame(drows)
    DC.to_csv(f"{OUT}.decomp.csv", index=False)
    P(f"   {len(DC)} (book, strip, rung, convention, half) decompositions written to .decomp.csv "
      f"(identity d_margin == dBOOK - dCOMP holds by construction; residual "
      f"{np.abs(DC.d_margin - (DC.dBOOK - DC.dCOMP)).max():.3e})")

    hdd = DC[(DC.rung == RUNG_HEAD) & (DC.conv == CONV_HEAD) & (DC.set == "SHELF") &
             DC.base_pass4b & DC.strip.isin(EP_SETS[EPSET_HEAD])]
    P(f"\n   SHELF, {EPSET_HEAD}, {CONV_HEAD}, 10 bps — mean |dBOOK| vs mean |dCOMP| by "
      f"(strip, half):")
    P(f"      {'strip':<13}{'half':>5}{'mean dBOOK':>12}{'mean dCOMP':>12}"
      f"{'comp share':>12}{'legs flipped':>14}")
    for (ep, half), g in hdd.groupby(["strip", "half"]):
        P(f"      {ep:<13}{half:>5}{g.dBOOK.mean():>+12.4f}{g.dCOMP.mean():>+12.4f}"
          f"{g.comparand_share.mean():>12.3f}{int(g.flips_leg.sum()):>8} of {len(g)}")
    kills = hdd[hdd.flips_leg]
    if len(kills):
        P(f"\n   the {len(kills)} leg flips (margin >= 0 unstripped, < 0 stripped):")
        for r in kills.sort_values("d_margin").itertuples():
            P(f"      {r.book:<34}{r.strip:<13}{r.half:>3}  margin {r.margin0:>+6.3f} -> "
              f"{r.margin1:>+6.3f}   dBOOK {r.dBOOK:>+7.4f}  dCOMP {r.dCOMP:>+7.4f}  "
              f"-> {r.side}")
        mb, mc = kills.dBOOK.abs().median(), kills.dCOMP.abs().median()
        P(f"   H_COMPARAND (median |dCOMP| > median |dBOOK| among the flips): "
          f"{'PASS' if mc > mb else 'FAIL'} (|dCOMP| {mc:.4f} vs |dBOOK| {mb:.4f}; "
          f"{int((kills.side == 'COMPARAND').sum())} of {len(kills)} flips are COMPARAND-side)")
    else:
        P("   NO leg flips on the SHELF at the headline cell — H_COMPARAND is VACUOUS there; "
          "the pooled reading below is what carries the answer.")
    pooled = DC[(DC.rung == RUNG_HEAD) & (DC.conv == CONV_HEAD) & DC.base_pass4b &
                DC.strip.isin(EP_SETS[EPSET_HEAD])]
    pk_ = pooled[pooled.flips_leg]
    P(f"   POOLED over SHELF+GRID at the headline cell: {len(pk_)} flips of {len(pooled)} "
      f"(book, strip, half) cells; COMPARAND-side "
      f"{int((pk_.side == 'COMPARAND').sum())}, BOOK-side {int((pk_.side == 'BOOK').sum())}; "
      f"median comparand share over ALL cells {pooled.comparand_share.median():.3f}")
    # THE HEDGE: the comparand moves, but so does the book.  d margin = dBOOK - dCOMP, so the
    # offset ratio dBOOK/dCOMP is exactly how much of the comparand shift the book absorbs.
    # A ratio near 1 means the leg is immune BECAUSE both sides are long the same episode --
    # the structural difference from the DD cap, where the book's own MaxDD need not be in it.
    P(f"\n   THE HEDGE — how much of the comparand's move the book absorbs "
      f"(offset = mean dBOOK / mean dCOMP; 1.00 = margin untouched, 0.00 = margin takes the "
      f"full comparand shift).  SHELF+GRID, {CONV_HEAD}, {RUNG_HEAD:.0f} bps, 4b passes only:")
    allp = DC[(DC.rung == RUNG_HEAD) & (DC.conv == CONV_HEAD) & DC.base_pass4b]
    P(f"      {'strip':<13}{'half':>5}{'mean dCOMP':>12}{'mean dBOOK':>12}{'offset':>9}"
      f"{'mean d margin':>15}")
    for (ep, half), g in allp.groupby(["strip", "half"]):
        off = g.dBOOK.mean() / g.dCOMP.mean() if abs(g.dCOMP.mean()) > 1e-12 else np.nan
        P(f"      {ep:<13}{half:>5}{g.dCOMP.mean():>+12.4f}{g.dBOOK.mean():>+12.4f}"
          f"{off:>9.2f}{g.d_margin.mean():>+15.4f}")
    q2 = allp[allp.strip.isin(EP_SETS[EPSET_HEAD]) & (allp.half == "H2")]
    P(f"      -> on H2, the leg the queue's 863 case failed on: comparand moves "
      f"{q2.dCOMP.mean():+.4f}, book moves {q2.dBOOK.mean():+.4f}, "
      f"offset {q2.dBOOK.mean() / q2.dCOMP.mean():.2f}, net margin "
      f"{q2.d_margin.mean():+.4f} — the defect IS in the comparand and it is LARGE; it does not "
      f"reach the verdict because the book is long the same episode.")
    P(f"\n   SPY's own halves under each strip ({CONV_HEAD}, the bar the books must clear):")
    for ep in [None] + list(EPISODES):
        km = keep_mask(ep)
        sp = pack(spy[km], *HV[(ep, CONV_HEAD)])
        b0 = pack(spy)
        P(f"      {('NONE' if ep is None else ep):<13} SPY H1 {sp['H1']:>6.4f} "
          f"({sp['H1'] - b0['H1']:>+7.4f})   H2 {sp['H2']:>6.4f} "
          f"({sp['H2'] - b0['H2']:>+7.4f})   MaxDD {sp['MaxDD']:>7.2%}")

    # ---------------------------------------------- PART B2: the boundary channel
    P("\n### PART B2 — THE BOUNDARY CHANNEL (the leg the DD cap does not have).  COUNT moves "
      "the midpoint when days are deleted; DATE freezes it.")
    for st, esn in product(SETS, EP_SETS):
        u = CL[(CL.set == st) & (CL.rung == RUNG_HEAD) & (CL.epset == esn)]
        kc = int(u[u.conv == "COUNT"].killed_by_clause.sum())
        kd = int(u[u.conv == "DATE"].killed_by_clause.sum())
        nbc = int(u[u.conv == "COUNT"].base_pass4b.sum())
        P(f"   {st:<6} {esn:<9} kills COUNT {kc:>2} / DATE {kd:>2}  (of {nbc} unstripped passes)")
    uq = CL[(CL.set == "SHELF") & (CL.rung == RUNG_HEAD) & (CL.epset == EPSET_HEAD)]
    kc = int(uq[uq.conv == "COUNT"].killed_by_clause.sum())
    kd = int(uq[uq.conv == "DATE"].killed_by_clause.sum())
    P(f"   H_BOUNDARY (DATE kills strictly fewer than COUNT on SHELF/{EPSET_HEAD}): "
      f"{'PASS' if kd < kc else 'FAIL'} (COUNT {kc} vs DATE {kd})")
    dshift = {}
    for ep in list(EPISODES):
        km = keep_mask(ep)
        h1, _ = HV[(ep, "COUNT")]
        dshift[ep] = (eidx[km][int(h1.sum()) - 1], int(h1.sum()) - int(HV[(ep, 'DATE')][0].sum()))
    P("   midpoint under COUNT after each strip (unstripped "
      f"{MID_DATE.date()}), and the day-count shift vs DATE:")
    for ep, (d, sh) in dshift.items():
        P(f"      {ep:<13} {str(d.date()):<12} {sh:>+5} days moved across the boundary")

    # ---------------------------------------------- PART B3: the shuffle null
    P(f"\n### PART B3 — THE CLAUSE'S OWN NULL: {N_SHUFFLE} random strips of COVID_TIGHT's "
      f"length (seed {SEED}), same conjunctive HALF clause, SHELF @ {RUNG_HEAD:.0f} bps, "
      f"{CONV_HEAD} halves.  Unlike 861's DD null this one is NOT inert: both half Sharpes move "
      "on every strip.")
    rng = np.random.default_rng(SEED)
    L = int((~keep_mask("COVID_TIGHT")).sum())
    shelf_ok = [nm for nm, b in books.items() if b["set"] == "SHELF" and b.get("repro", False)]
    base_pass = MG[(MG.set == "SHELF") & (MG.rung == RUNG_HEAD) & (MG.conv == CONV_HEAD) &
                   (MG.strip == "NONE")].set_index("book").pass4b
    srows = []
    for d in range(N_SHUFFLE):
        i0 = int(rng.integers(0, len(eidx) - L))
        km = np.ones(len(eidx), bool)
        km[i0:i0 + L] = False
        k = int(km.sum()) // 2
        h1 = np.zeros(int(km.sum()), bool)
        h1[:k] = True
        sp = pack(spy[km], h1, ~h1)
        kills = 0
        for nm in shelf_ok:
            if not bool(base_pass[nm]):
                continue
            q = pack(books[nm]["net"][RUNG_HEAD][km], h1, ~h1)
            kills += int(min(q["H1"] - sp["H1"], q["H2"] - sp["H2"]) < 0)
        srows.append(dict(draw=d, start=str(eidx[i0].date()), end=str(eidx[i0 + L - 1].date()),
                          SPY_H1=sp["H1"], SPY_H2=sp["H2"], SPY_MaxDD=sp["MaxDD"], kills=kills))
    SHF = pd.DataFrame(srows)
    SHF.to_csv(f"{OUT}.shuffle.csv", index=False)
    P(SHF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    q90 = float(np.quantile(SHF.kills, 0.90))
    real_kills = {}
    for ep in EPISODES:
        u = MG[(MG.set == "SHELF") & (MG.rung == RUNG_HEAD) & (MG.conv == CONV_HEAD) &
               (MG.strip == ep)]
        real_kills[ep] = int(sum(bool(base_pass[r.book]) and (min(r.h1_margin, r.h2_margin) < 0)
                                 for r in u.itertuples()))
    P(f"   shuffle kills: mean {SHF.kills.mean():.2f}, median {SHF.kills.median():.1f}, "
      f"p90 {q90:.1f}, max {SHF.kills.max()}; SPY's spliced halves range "
      f"H1 {SHF.SPY_H1.min():.4f}..{SHF.SPY_H1.max():.4f}, "
      f"H2 {SHF.SPY_H2.min():.4f}..{SHF.SPY_H2.max():.4f}")
    P("   real single-strip half-kills on the SHELF: " +
      ", ".join(f"{k} {v}" for k, v in real_kills.items()))
    P(f"   H_BEAR (BEAR2022's own half-kill count >= 1, against its DD-leg count of 0 in 861): "
      f"{'PASS' if real_kills['BEAR2022'] >= 1 else 'FAIL'} ({real_kills['BEAR2022']})")
    P(f"   shuffle calibration: QUEUE2's worst single strip kills "
      f"{max(real_kills['COVID_TIGHT'], real_kills['BEAR2022'])} vs null p90 {q90:.1f} "
      f"-> {'OUTSIDE' if max(real_kills['COVID_TIGHT'], real_kills['BEAR2022']) > q90 else 'INSIDE'} "
      f"the null")

    # ----------------------------------------------------------------- PART C: rule 8
    P("\n### PART C — RULE 8 WITH THE HALF CLAUSE AS A SELECTOR.  Dial chosen on 2009-2016 "
      "ALONE; OOS 2017-2026 read ONCE per (panel, episode set, chooser).")
    P("   UNSCREENED: argmax IS Sharpe over the GRID pool.")
    P("   SCREENED  : argmax IS Sharpe over the GRID pool RESTRICTED to books whose BOTH half "
      "legs clear at every strip of the set, with pool, strips, halves and comparand all "
      "computed on the IS window only.")
    is_eidx = eidx[is_mask]
    IS_MID = is_eidx[len(is_eidx) // 2]

    def is_halves(km_is):
        k = int(km_is.sum()) // 2
        a = np.zeros(int(km_is.sum()), bool)
        a[:k] = True
        return a, ~a

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
                kk = km[is_mask]                       # selector inside the IS vector
                h1, h2 = is_halves(kk)
                sp_is = pack(spy[km], h1, h2)
                q = pack(b["net"][RUNG_HEAD][km], h1, h2)
                if min(q["H1"] - sp_is["H1"], q["H2"] - sp_is["H2"]) < 0:
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
            _, p4b_fix, _ = verdicts(sbk, base, sp, FIXED_CAP, FIXED_FLOOR)
            # does the OOS pick satisfy the HALF clause OUT of sample?
            oos_min = np.inf
            for ep in EP_SETS[esn]:
                km = keep_mask(ep) & oos_mask
                kk = km[oos_mask]
                k2 = int(kk.sum()) // 2
                a = np.zeros(int(kk.sum()), bool)
                a[:k2] = True
                spx = pack(spy[km], a, ~a)
                qx = pack(best[1]["net"][RUNG_HEAD][km], a, ~a)
                oos_min = min(oos_min, qx["H1"] - spx["H1"], qx["H2"] - spx["H2"])
            wrows.append(dict(panel=pname, epset=esn, chooser=chooser, pick=best[0],
                              pool_n=len(pool), elig_n=len(elig_pool),
                              IS_Sharpe=is_sh(best[1]), OOS_CAGR=sbk["CAGR"],
                              OOS_Sharpe=sbk["Sharpe"], OOS_MaxDD=sbk["MaxDD"],
                              OOS_H1=sbk["H1"], OOS_H2=sbk["H2"],
                              V2_OOS_CAGR=base["CAGR"], V2_OOS_Sharpe=base["Sharpe"],
                              V2_OOS_MaxDD=base["MaxDD"], V1_OOS_Sharpe=old["Sharpe"],
                              SPY_OOS_CAGR=sp["CAGR"], SPY_OOS_Sharpe=sp["Sharpe"],
                              SPY_OOS_MaxDD=sp["MaxDD"], pass4a=p4a, pass4b=p4b, fail4b=fails,
                              pass4b_fixedbar=p4b_fix, OOS_clause_halfmin=float(oos_min),
                              OOS_clause_pass=bool(p4b and oos_min >= 0)))
    WF = pd.DataFrame(wrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    for r in WF.itertuples():
        P(f"   {r.panel:<5} {r.epset:<9} {r.chooser:<11} pool {r.pool_n:>2}/elig {r.elig_n:>2}  "
          f"pick {r.pick:<28} IS {r.IS_Sharpe:.4f}  OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / "
          f"{r.OOS_MaxDD:.2%} (H1 {r.OOS_H1:.3f}/H2 {r.OOS_H2:.3f}) | v2 "
          f"{r.V2_OOS_CAGR:.2%}/{r.V2_OOS_Sharpe:.4f}/{r.V2_OOS_MaxDD:.2%} | SPY "
          f"{r.SPY_OOS_CAGR:.2%}/{r.SPY_OOS_Sharpe:.4f}/{r.SPY_OOS_MaxDD:.2%} | "
          f"4b {'PASS' if r.pass4b else 'FAIL ' + r.fail4b}  4a {'PASS' if r.pass4a else 'FAIL'}"
          f" | OOS half-clause {r.OOS_clause_halfmin:+.4f} "
          f"{'KEEP' if r.OOS_clause_pass else 'DROP'}")
    deltas = []
    for pname, esn in product(PX, EP_SETS):
        u = WF[(WF.panel == pname) & (WF.epset == esn)].set_index("chooser")
        if "SCREENED" in u.index and "UNSCREENED" in u.index and \
                u.loc["SCREENED"].pick != "NONE-ELIGIBLE":
            deltas.append(float(u.loc["SCREENED"].OOS_Sharpe - u.loc["UNSCREENED"].OOS_Sharpe))
    nbetter = sum(1 for d in deltas if d > 0)
    P(f"\n   SCREENED minus UNSCREENED OOS Sharpe over {len(deltas)} (panel, episode set) "
      f"cells: {', '.join(f'{d:+.4f}' for d in deltas)}; median "
      f"{(np.median(deltas) if deltas else float('nan')):+.4f}, better in {nbetter} of "
      f"{len(deltas)}")
    P(f"   H_R8 (the clause does NOT buy OOS Sharpe): "
      f"{'PASS' if nbetter <= len(deltas) / 2 else 'FAIL'} "
      f"({nbetter} of {len(deltas)} cells improved)")

    P(f"\n### done in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

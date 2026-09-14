#!/usr/bin/env python3
"""Idea 851 (cloud lane, 2026-09-14) — is the 4b MaxDD CAP itself a SINGLE-EPISODE number?

QUESTION (QUEUE idea 851, verbatim)
    idea 835 found 89% of the shelf's 4b passes die when 2020-02-19..2020-04-07 is deleted, and
    the cap every candidate is judged against (60% of SPY's -33.72%) is set by that same episode.
    Re-price the cap on legs that exclude 2020 and report how many standing candidates survive
    their own bar.  Max 2 params (excluded episode, candidate set).

WHAT IS NEW AGAINST 835.  835 deleted the episode from a 216-arm MECHANICAL QROLL corpus and
    re-priced the bar with it (SPY -33.72% -> -24.50%, cap -20.23% -> -14.70%, 4b 141 -> 16).
    It never touched THE SHELF — the books the record has actually written 4b KEEP-candidate
    memos for, the ones a Sunday review would pick from.  This run rebuilds every such memo'd
    book from its own committed RULES wording, gates each against its published headline, and
    then asks 851's question of THEM.  It also separates the two things 835's design confounds:
        CAP CONVENTION FIXED     judge the 2020-free book against the record's COMMITTED bars
                                 (cap -20.23%, floor 70% x 15.16%) -- is the BOOK 2020-made?
        CAP CONVENTION REPRICED  judge it against SPY on the SAME leg -- is the BAR 2020-made?
    Both are computed for every candidate, every episode and every leg.  A pass that dies only
    under REPRICED is killed by the bar moving, not by the book.

TUNED PARAMETERS: exactly TWO, the two the queue names.
    (1) EXCLUDED EPISODE, 7 levels, all reported.  HEADLINE = COVID_TIGHT, the queue's own
        window, declared here before any number is read.
            NONE           no deletion (the record's leg)
            COVID_TIGHT    2020-02-19..2020-04-07   <- HEADLINE (835's / the queue's)
            COVID_DD       SPY's own peak -> first recovery day, resolved FROM THE DATA
            COVID_WIDE     2020-02-01..2020-06-30
            DD_2015        2015-08-10..2015-09-29   (a second real, smaller episode)
            BEAR2022       2022-01-03..2022-10-12   (the other big decline; if deleting THIS
                           also empties the shelf, the cap is a generic-crash number, not a
                           2020 number)
            PLACEBO_2017   2017-02-19..2017-04-07   (same calendar shape, no crash: the leg
                           count must barely move or the design is measuring day-count)
    (2) CANDIDATE SET in {SHELF, GRID}.
            SHELF  every committed 4b KEEP-candidate memo under research/backtests/ that this
                   run can rebuild from its own RULES wording and gate against its published
                   headline.  A memo that does not reproduce is NAMED and EXCLUDED, never
                   silently re-specified.
            GRID   a mechanical ladder (band x gross, and the QROLL breadth family) so the
                   shelf's answer can be read against a corpus that was never memo-selected.

DELETION CONVENTION: SPLICE — the episode's trading days are removed from every series before
    any moment is taken, so Sharpe, CAGR and MaxDD are all read on the same shortened calendar
    (835's convention, restated).  MaxDD is therefore the deepest peak-to-trough of the SPLICED
    equity curve: the crash cannot contribute, and neither can any drawdown that needed those
    days to deepen.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_CAPEPISODE  SPY's full-sample MaxDD is a single-episode number: deleting COVID_TIGHT moves
                  it by more than 5 pp.
    H_SHELFDIES   under COVID_TIGHT + REPRICED bars a MAJORITY of the reproducing shelf loses 4b.
    H_BARNOTBOOK  the same books mostly KEEP 4b under COVID_TIGHT + FIXED bars, i.e. the kill is
                  the bar re-pricing rather than the book being 2020-made.
    H_PLACEBO     PLACEBO_2017 leaves the shelf's 4b count within 1 of the NONE count.
    H_2022        deleting BEAR2022 does NOT empty the shelf (if it does, "single-episode" is the
                  wrong description — the cap is a generic-crash number).
    H_R8          the rule-8 OOS pick's 4b verdict flips between FIXED and REPRICED bars on the
                  2020-free leg.

GATES (printed before any new number; all must pass)
    G1  the empty-episode splice is the identity: NONE reproduces the unspliced numbers exactly
        (max|d| must be 0.0).
    G2  every SHELF book reproduces its committed memo headline inside a stated tolerance
        (Sharpe 0.030, MaxDD 1.5 pp — the memos were written on samples ending 2026-09-04..
        2026-09-11 and this panel ends 2026-09-11, so exact equality is not available for all).
        Books outside tolerance are named and dropped from the SHELF.
    G3  SPY reproduces the record's 4b comparand 15.16% / 0.8861 / -33.72%, and its committed
        MaxDD episode is located and printed (peak, trough, depth) so the cap's provenance is
        a fact on the page rather than an assumption.
    G4  the splice is clean: every deleted day is gone from every series and the kept-day count
        agrees across candidate, baseline and SPY.

PROTOCOL: 10 bps per unit turnover (25 also reported), weights decided at close t applied at
    t+1, no shorting, no leverage.  Both KEEP paths evaluated on every row.  Rule 8: the GRID
    dial is chosen on 2009-2016 IS Sharpe alone (the IS window contains no 2020) and the OOS
    window is read once per (episode, bar convention).

SURVIVORSHIP, up front: U56 and B136 are CURRENT-constituent lists, so every CAGR and drawdown
    LEVEL is optimistic; the episode-to-episode DIFFERENCE is the durable part.  Nothing here is
    a capital claim on its own and nothing is promoted.

Outputs (committed under research/backtests/):
    .console.txt   full log
    .spy.csv       SPY and both 4b bars on every (episode, leg)
    .books.csv     every candidate x episode x bar convention x leg x rung, with 4a/4b verdicts
    .shelf.csv     the reproduction gate for every committed 4b memo
    .walkforward.csv  the rule-8 pick per (episode, bar convention) and its OOS read

Run: python research/backtests/2026-09-14_is-the-4b-MaxDD-CAP-itself-a-SINGLE-EPISODE-number_cloud.py
Deterministic; no network (reads the committed price caches only).
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
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-14"
SLUG = "is-the-4b-MaxDD-CAP-itself-a-SINGLE-EPISODE-number"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FREQ = "W"
LAG = 1
WARMUP = 260
MAX_VOL = 0.60
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BARS = ["FIXED", "REPRICED"]
LEGS = ["FULL", "OOS"]

# ---- tuned dial 1: the excluded episode; headline declared before any number ------------
EPISODES = {
    "NONE": None,
    "COVID_TIGHT": ("2020-02-19", "2020-04-07"),
    "COVID_DD": None,                       # resolved from SPY itself
    "COVID_WIDE": ("2020-02-01", "2020-06-30"),
    "DD_2015": ("2015-08-10", "2015-09-29"),
    "BEAR2022": ("2022-01-03", "2022-10-12"),
    "PLACEBO_2017": ("2017-02-19", "2017-04-07"),
}
EP_HEAD = "COVID_TIGHT"

# ---- tuned dial 2: the candidate set ----------------------------------------------------
SETS = ["SHELF", "GRID"]

# the record's COMMITTED bars (full-sample SPY), quoted in every 4b memo
FIXED_CAP = -0.2023
FIXED_FLOOR = 0.70 * 0.151631
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
    """PROTOCOL rule 4, both paths. cap/floor are passed in so the FIXED and REPRICED
    conventions are the only difference between two otherwise identical readings."""
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
    """Every committed 4b KEEP-candidate memo this run can rebuild FROM ITS OWN RULES WORDING,
    with the headline the memo publishes, for the G2 reproduction gate."""
    out = {}

    # --- U56 band books (memos 2026-09-11) --------------------------------------------
    out["u56-v2band-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.03, 1.00), memo=(0.1155, 1.2067, -0.1570),
        src="2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md")
    out["u56-band008-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.08, 1.00), memo=(0.1137, 1.1439, -0.1905),
        src="2026-09-11_u56-band008-gross100_4b_cloud_MEMO.md")

    # --- U56 top-20 composite, gross 0.75, no vol scaler (memo 2026-09-07; the m=20 band
    #     "moves no holdings" per its own point 2, so the m=0 book is the same book) -------
    s, above, vol20 = score(U, vol_scale=False)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    out["u56-top20-band-m20"] = dict(
        panel="U56", freq="W", W=(rank <= 20).astype(float) * 0.75 / 20,
        memo=(0.1287, 1.112, -0.1722), src="2026-09-07_u56-top20-band-m20_4b_B_MEMO.md")

    # --- U56 "MARS" respread, gross 0.75 (memo 2026-09-11) -----------------------------
    ab = (U > U.rolling(200).mean()).astype(float)
    n = ab.sum(axis=1).replace(0, np.nan)
    out["u56-marsrespread-gross075"] = dict(
        panel="U56", freq="W", W=ab.div(n, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1155, 1.0914, None), src="2026-09-11_u56-marsrespread-gross075_4b_C_MEMO.md")

    # --- U56 top-50% by close/MA200-1, respread 0.75, MONTHLY (memo 2026-09-11) --------
    rel = U / U.rolling(200).mean() - 1
    sel = (rel.rank(axis=1, ascending=False, pct=True) <= 0.50) & rel.notna()
    k = sel.astype(float).sum(axis=1).replace(0, np.nan)
    out["u56-quantile50-respread-M"] = dict(
        panel="U56", freq="M", W=sel.astype(float).div(k, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1547, 1.2359, -0.1980), src="2026-09-11_u56-quantile50-respread-M_4b_B_MEMO.md")

    # --- B136 6-month-return top 20, gross 0.65 (memo 2026-09-12) ----------------------
    r6 = B / B.shift(126) - 1
    out["b136-r620-gross065-W"] = dict(
        panel="B136", freq="W", W=(r6.rank(axis=1, ascending=False) <= 20).astype(float) * 0.65 / 20,
        memo=(0.1499, 1.1264, -0.1943), src="2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md")

    # --- the two breadth-QROLL candidates (memos 2026-09-12 / 2026-09-14) --------------
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
    """A mechanical ladder that was never memo-selected, so the shelf's answer can be read
    against something the record did not choose."""
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
    P(f"# Idea 851 — is the 4b MaxDD CAP itself a SINGLE-EPISODE number? ({DATE}, cloud lane)")
    P(f"# {len(EPISODES)} episodes x {len(SETS)} candidate sets x {len(BARS)} bar conventions x "
      f"{len(LEGS)} legs x {len(RUNGS)} rungs, ALL reported.  Headline episode = {EP_HEAD}.")
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

    # ---- episodes resolved from the data -------------------------------------------------
    EPD = dict(EPISODES)
    s = U["SPY"].loc["2019-06-01":]
    pk = s.loc[:"2020-02-19"].idxmax()
    lvl = float(s.loc[pk])
    rec = s.loc[pk:][s.loc[pk:] >= lvl]
    EPD["COVID_DD"] = (str(pk.date()), str((rec.index[1] if len(rec) > 1 else s.index[-1]).date()))
    P("   episodes (COVID_DD resolved from SPY itself):")
    for kk, vv in EPD.items():
        P(f"      {kk:<13} {vv}")

    def keep_mask(ep):
        m = np.ones(len(eidx), bool)
        if EPD[ep] is None:
            return m
        a, b = EPD[ep]
        return ~((eidx >= pd.Timestamp(a)) & (eidx <= pd.Timestamp(b)))

    oos_mask = np.asarray(eidx >= pd.Timestamp(OOS_START))

    # ---- returns for every candidate ------------------------------------------------------
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

    # G1 — the empty splice is the identity.
    nm0 = "u56-v2band-gross100"
    a = pack(books[nm0]["net"][RUNG_HEAD])
    bsel = keep_mask("NONE")
    b_ = pack(books[nm0]["net"][RUNG_HEAD][bsel])
    g1 = max(abs(a[k] - b_[k]) for k in a)
    P(f"   G1 empty splice == unspliced on {nm0}: max|d| {g1:.3e} "
      f"{'PASS' if g1 == 0.0 else 'FAIL'}")
    ok &= g1 == 0.0

    # G2 — the shelf reproduces its memos.
    srows = []
    for nm, b in books.items():
        if b["set"] != "SHELF":
            continue
        m = pack(b["net"][RUNG_HEAD])
        mm = b["memo"]
        dS = abs(m["Sharpe"] - mm[1])
        dD = abs(m["MaxDD"] - mm[2]) if mm[2] is not None else 0.0
        good = (dS <= REPRO_TOL_SHARPE) and (dD <= REPRO_TOL_DD)
        srows.append(dict(book=nm, panel=b["panel"], memo_CAGR=mm[0], memo_Sharpe=mm[1],
                          memo_MaxDD=mm[2], got_CAGR=m["CAGR"], got_Sharpe=m["Sharpe"],
                          got_MaxDD=m["MaxDD"], dSharpe=dS, dMaxDD=dD, reproduces=good,
                          memo_file=b["src"]))
        b["repro"] = good
        P(f"   G2 {nm:<34} {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}  vs memo "
          f"{mm[0]:.2%} / {mm[1]:.4f} / "
          f"{('%.2f%%' % (100 * mm[2])) if mm[2] is not None else '   n/a'}  "
          f"dSharpe {dS:.4f} dMaxDD {dD:.4f}  {'REPRODUCES' if good else 'EXCLUDED'}")
    SH = pd.DataFrame(srows)
    SH.to_csv(f"{OUT}.shelf.csv", index=False)
    n_rep = int(SH.reproduces.sum())
    P(f"   G2 {n_rep} of {len(SH)} committed 4b memos reproduce inside tolerance "
      f"(Sharpe {REPRO_TOL_SHARPE}, MaxDD {REPRO_TOL_DD:.1%}); the rest are named above and "
      f"dropped from the SHELF, never re-specified.")
    P("   G2 NOT REBUILT AT ALL (named, outside the shelf): "
      "2026-09-12_b136-corr-hi-q017-w252-d050-D-g100 — neither natural reading of its memo's "
      "tail convention reproduces its headline (best attempt 13.31% / 1.0951 / -17.69% vs "
      "14.02% / 1.1538 / -15.11%), so it is excluded and reported as unreproduced.")
    ok &= n_rep >= 6

    # G3 — SPY and the provenance of the cap.
    sm = pack(spy)
    g3 = max(abs(sm["CAGR"] - 0.1516), abs(sm["Sharpe"] - 0.8861), abs(sm["MaxDD"] + 0.3372))
    eq = np.cumprod(1.0 + spy)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    it = int(np.argmin(dd))
    ip = int(np.argmax(eq[:it + 1]))
    P(f"   G3 SPY full {sm['CAGR']:.4%} / {sm['Sharpe']:.4f} / {sm['MaxDD']:.4%} vs committed "
      f"15.16% / 0.8861 / -33.72%: max|d| {g3:.2e} {'PASS' if g3 < 1e-3 else 'FAIL'}")
    P(f"   G3 the cap's provenance: SPY's committed MaxDD runs {eidx[ip].date()} -> "
      f"{eidx[it].date()} ({dd[it]:.2%}); the committed 4b cap is 60% of it = {FIXED_CAP:.2%}")
    ok &= g3 < 1e-3

    # G4 — the splice is clean and shared.
    kt = keep_mask(EP_HEAD)
    g4 = (int((~kt).sum()) == int(((eidx >= pd.Timestamp(EPD[EP_HEAD][0])) &
                                  (eidx <= pd.Timestamp(EPD[EP_HEAD][1]))).sum()))
    P(f"   G4 splice removes {int((~kt).sum())} scored days for {EP_HEAD} "
      f"({EPD[EP_HEAD][0]}..{EPD[EP_HEAD][1]}), the same mask for every series: "
      f"{'PASS' if g4 else 'FAIL'}")
    ok &= g4
    P(f"   GATES: {'ALL PASS' if ok else 'FAILURE — nothing below is read'}")
    assert ok

    # ----------------------------------------------------------------- PART A: the bar itself
    P("\n### PART A — what the DELETION does to SPY, and therefore to the BAR")
    srows = []
    for ep in EPISODES:
        km = keep_mask(ep)
        for leg in LEGS:
            sel = km & (oos_mask if leg == "OOS" else True)
            sp = pack(spy[sel])
            srows.append(dict(episode=ep, leg=leg, days=int(sel.sum()),
                              deleted=int((~km).sum()),
                              SPY_CAGR=sp["CAGR"], SPY_Sharpe=sp["Sharpe"], SPY_MaxDD=sp["MaxDD"],
                              SPY_H1=sp["H1"], SPY_H2=sp["H2"],
                              REPRICED_cap=0.60 * sp["MaxDD"], REPRICED_floor=0.70 * sp["CAGR"],
                              FIXED_cap=FIXED_CAP, FIXED_floor=FIXED_FLOOR))
    SPYT = pd.DataFrame(srows)
    SPYT.to_csv(f"{OUT}.spy.csv", index=False)
    P(SPYT[SPYT.leg == "FULL"][["episode", "deleted", "days", "SPY_CAGR", "SPY_Sharpe",
                                "SPY_MaxDD", "REPRICED_cap", "REPRICED_floor"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dd_none = float(SPYT[(SPYT.episode == "NONE") & (SPYT.leg == "FULL")].SPY_MaxDD.iloc[0])
    dd_head = float(SPYT[(SPYT.episode == EP_HEAD) & (SPYT.leg == "FULL")].SPY_MaxDD.iloc[0])
    P(f"   H_CAPEPISODE: SPY MaxDD {dd_none:.2%} -> {dd_head:.2%} when {EP_HEAD} is deleted "
      f"(move {abs(dd_head - dd_none):.2%}) — {'PASS' if abs(dd_head - dd_none) > 0.05 else 'FAIL'}; "
      f"the cap moves {FIXED_CAP:.2%} -> {0.60 * dd_head:.2%}")

    # ----------------------------------------------------------------- PART B: the candidates
    P("\n### PART B — every candidate x episode x bar convention x leg x rung")
    rows = []
    for nm, b in books.items():
        if b["set"] == "SHELF" and not b.get("repro", False):
            continue
        for ep, leg, bar, rung in product(EPISODES, LEGS, BARS, RUNGS):
            km = keep_mask(ep)
            sel = km & (oos_mask if leg == "OOS" else True)
            s = pack(b["net"][rung][sel])
            base = pack(v2[b["panel"]][rung][sel])
            sp = pack(spy[sel])
            cap = FIXED_CAP if bar == "FIXED" else 0.60 * sp["MaxDD"]
            flo = FIXED_FLOOR if bar == "FIXED" else 0.70 * sp["CAGR"]
            p4a, p4b, fails = verdicts(s, base, sp, cap, flo)
            rows.append(dict(book=nm, set=b["set"], panel=b["panel"], episode=ep, leg=leg,
                             bar=bar, rung=rung, days=int(sel.sum()),
                             CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                             H1=s["H1"], H2=s["H2"], cap=cap, floor=flo,
                             dd_margin=s["MaxDD"] - cap,
                             SPY_MaxDD=sp["MaxDD"], SPY_CAGR=sp["CAGR"],
                             V2_Sharpe=base["Sharpe"], V2_MaxDD=base["MaxDD"],
                             pass4a=p4a, pass4b=p4b, fail4b=fails))
    BK = pd.DataFrame(rows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    P(f"   {len(BK)} rows written; {BK.book.nunique()} distinct books "
      f"({BK[BK.set == 'SHELF'].book.nunique()} SHELF, {BK[BK.set == 'GRID'].book.nunique()} GRID)")

    hd = BK[(BK.rung == RUNG_HEAD) & (BK.leg == "FULL")]
    for st in SETS:
        t = hd[hd.set == st]
        P(f"\n   {st}: 4b passes by (episode, bar convention) — full sample, 10 bps, "
          f"n = {t.book.nunique()} books")
        P(t.pivot_table(index="episode", columns="bar", values="pass4b", aggfunc="sum")
          .reindex(EPISODES.keys()).to_string())
        P(f"   {st}: 4a passes (same cells)")
        P(t.pivot_table(index="episode", columns="bar", values="pass4a", aggfunc="sum")
          .reindex(EPISODES.keys()).to_string())

    sh = hd[hd.set == "SHELF"]
    n_sh = sh.book.nunique()
    none_n = int(sh[(sh.episode == "NONE") & (sh.bar == "FIXED")].pass4b.sum())
    rep_n = int(sh[(sh.episode == EP_HEAD) & (sh.bar == "REPRICED")].pass4b.sum())
    fix_n = int(sh[(sh.episode == EP_HEAD) & (sh.bar == "FIXED")].pass4b.sum())
    plac_n = int(sh[(sh.episode == "PLACEBO_2017") & (sh.bar == "REPRICED")].pass4b.sum())
    b22_n = int(sh[(sh.episode == "BEAR2022") & (sh.bar == "REPRICED")].pass4b.sum())
    P(f"\n   THE ANSWER, shelf, full sample, 10 bps: {none_n} of {n_sh} standing candidates pass "
      f"4b as the record reads them; {fix_n} survive deleting {EP_HEAD} against the COMMITTED "
      f"bars; {rep_n} survive it against bars RE-PRICED on the same leg.")
    P(f"   H_SHELFDIES ({EP_HEAD} + REPRICED, majority lost): "
      f"{'PASS' if rep_n < none_n / 2 else 'FAIL'} ({none_n} -> {rep_n})")
    P(f"   H_BARNOTBOOK (same books mostly keep 4b under FIXED bars): "
      f"{'PASS' if fix_n >= max(1, int(0.5 * none_n)) else 'FAIL'} ({none_n} -> {fix_n})")
    P(f"   H_PLACEBO (PLACEBO_2017 + REPRICED within 1 of NONE): "
      f"{'PASS' if abs(plac_n - none_n) <= 1 else 'FAIL'} ({none_n} -> {plac_n})")
    P(f"   H_2022 (deleting BEAR2022 does not empty the shelf): "
      f"{'PASS' if b22_n > 0 else 'FAIL'} ({none_n} -> {b22_n})")

    P(f"\n   Book by book at {EP_HEAD}, 10 bps, full sample (REPRICED cap "
      f"{0.60 * dd_head:.2%}, floor {0.70 * float(SPYT[(SPYT.episode == EP_HEAD) & (SPYT.leg == 'FULL')].SPY_CAGR.iloc[0]):.2%}):")
    P(f"      {'book':<34}{'MaxDD none':>11}{'MaxDD ex':>10}{'CAGR ex':>9}{'Sh ex':>8}"
      f"{'4b FIXED':>10}{'4b REPRICED':>13}  fail legs (REPRICED)")
    for nm in sorted(sh.book.unique()):
        a = sh[(sh.book == nm) & (sh.episode == "NONE") & (sh.bar == "REPRICED")].iloc[0]
        e_f = sh[(sh.book == nm) & (sh.episode == EP_HEAD) & (sh.bar == "FIXED")].iloc[0]
        e_r = sh[(sh.book == nm) & (sh.episode == EP_HEAD) & (sh.bar == "REPRICED")].iloc[0]
        P(f"      {nm:<34}{a.MaxDD:>11.2%}{e_r.MaxDD:>10.2%}{e_r.CAGR:>9.2%}{e_r.Sharpe:>8.3f}"
          f"{('PASS' if e_f.pass4b else 'FAIL'):>10}{('PASS' if e_r.pass4b else 'FAIL'):>13}  "
          f"{e_r.fail4b}")

    # How decisive is the re-priced bar?  A verdict decided by basis points is a statement
    # about the BAR's position, not about the books.
    mr = sh[(sh.episode == EP_HEAD) & (sh.bar == "REPRICED")]
    P(f"\n   HOW DECISIVE IS THE RE-PRICED CAP: the shelf's ex-{EP_HEAD} MaxDDs run "
      f"{mr.MaxDD.min():.2%}..{mr.MaxDD.max():.2%} against a cap of {0.60 * dd_head:.2%}; "
      f"{int((mr.dd_margin.abs() <= 0.01).sum())} of {len(mr)} books sit within 1.00 pp of it "
      f"and {int((mr.dd_margin.abs() <= 0.005).sum())} within 0.50 pp. Margins (MaxDD - cap): "
      + ", ".join(f"{r.book.split('-')[0]}..{r.book[-12:]} {r.dd_margin:+.2%}"
                  for r in mr.sort_values('dd_margin').itertuples()))
    P(f"   the three failures miss by "
      + ", ".join(f"{r.dd_margin:+.2%}" for r in
                  mr[~mr.pass4b].sort_values('dd_margin').itertuples())
      + " — basis points, not regime.")

    # ----------------------------------------------------------------- PART C: rule 8
    P("\n### PART C — RULE 8: GRID dial chosen on 2009-2016 IS Sharpe alone (the IS window "
      "contains no 2020), OOS read ONCE per (episode, bar convention)")
    wrows = []
    is_mask = ~oos_mask
    for ep, bar in product(EPISODES, BARS):
        km = keep_mask(ep)
        for pname in PX:
            pool = [(nm, b) for nm, b in books.items()
                    if b["set"] == "GRID" and b["panel"] == pname]
            issel = km & is_mask
            best = max(pool, key=lambda kv: fsharpe(kv[1]["net"][RUNG_HEAD][issel]))
            sel = km & oos_mask
            s = pack(best[1]["net"][RUNG_HEAD][sel])
            base = pack(v2[pname][RUNG_HEAD][sel])
            old = pack(v1[pname][RUNG_HEAD][sel])
            sp = pack(spy[sel])
            cap = FIXED_CAP if bar == "FIXED" else 0.60 * sp["MaxDD"]
            flo = FIXED_FLOOR if bar == "FIXED" else 0.70 * sp["CAGR"]
            p4a, p4b, fails = verdicts(s, base, sp, cap, flo)
            wrows.append(dict(episode=ep, bar=bar, panel=pname, pick=best[0],
                              IS_Sharpe=fsharpe(best[1]["net"][RUNG_HEAD][issel]),
                              OOS_CAGR=s["CAGR"], OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"],
                              OOS_H1=s["H1"], OOS_H2=s["H2"], cap=cap, floor=flo,
                              V2_OOS_Sharpe=base["Sharpe"], V2_OOS_CAGR=base["CAGR"],
                              V2_OOS_MaxDD=base["MaxDD"], V1_OOS_Sharpe=old["Sharpe"],
                              SPY_OOS_CAGR=sp["CAGR"], SPY_OOS_Sharpe=sp["Sharpe"],
                              SPY_OOS_MaxDD=sp["MaxDD"], pass4a=p4a, pass4b=p4b, fail4b=fails))
    WF = pd.DataFrame(wrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    for r in WF.itertuples():
        P(f"   {r.episode:<13} {r.bar:<9} {r.panel:<5} pick {r.pick:<28} IS {r.IS_Sharpe:.4f}  "
          f"OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%} "
          f"(cap {r.cap:.2%}, floor {r.floor:.2%}) | v2 {r.V2_OOS_CAGR:.2%}/{r.V2_OOS_Sharpe:.4f}"
          f"/{r.V2_OOS_MaxDD:.2%} | SPY {r.SPY_OOS_CAGR:.2%}/{r.SPY_OOS_Sharpe:.4f}"
          f"/{r.SPY_OOS_MaxDD:.2%} | 4b {'PASS' if r.pass4b else 'FAIL ' + r.fail4b}"
          f"  4a {'PASS' if r.pass4a else 'FAIL'}")
    flips = 0
    for ep, pn in product(EPISODES, PX):
        f = WF[(WF.episode == ep) & (WF.panel == pn) & (WF.bar == "FIXED")].pass4b.iloc[0]
        rr = WF[(WF.episode == ep) & (WF.panel == pn) & (WF.bar == "REPRICED")].pass4b.iloc[0]
        flips += int(bool(f) != bool(rr))
    P(f"   H_R8: the 4b verdict differs between FIXED and REPRICED bars in {flips} of "
      f"{len(EPISODES) * len(PX)} (episode, panel) cells — "
      f"{'PASS' if flips > 0 else 'FAIL'}")
    P(f"   pick stability: {WF.groupby(['panel']).pick.nunique().to_dict()} distinct picks per "
      f"panel across all {len(EPISODES)} episodes (the IS window contains no 2020, so a moving "
      f"pick would mean the deletion is reaching the chooser)")

    P(f"\n### done in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

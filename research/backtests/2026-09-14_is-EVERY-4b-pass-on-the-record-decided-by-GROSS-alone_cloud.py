#!/usr/bin/env python3
"""Idea 657 (cloud lane, 2026-09-14) — is EVERY 4b pass on the record decided by GROSS alone?

QUESTION (QUEUE idea 657, verbatim)
    idea 653's fresh 4-panel grid found 13 of 48 cells carry a 4b pass at 10 bps, **0 pass at all
    three grosses**, and max |Sharpe(g=1.00) - Sharpe(g=0.50)| over those cells is only 0.0052 —
    the ladder moves the CAGR floor and DD cap, never the risk-adjusted number.  Re-run the
    record's committed 4b passers on a denser gross ladder and report the share whose pass is a
    pure exposure fact, and whether PROTOCOL 4b needs a matched-gross leg.
    Max 2 params (gross grid, panel).

THE MECHANISM UNDER TEST.  De-grossing to cash is a near-affine operation on a book's daily
    returns: r_g ~ g * r_1 (plus a small cost and rebalance-drift term).  Sharpe is invariant to
    an affine scale, so the 4b Sharpe legs (H1 > SPY, H2 > SPY) barely move down the ladder,
    while CAGR falls roughly linearly (breaching the 70%-of-SPY floor from below) and MaxDD
    shrinks roughly linearly (clearing the 60%-of-SPY cap from above).  If that is the whole
    story then a 4b pass is a statement about EXPOSURE, and two books with identical selection
    but different gross get opposite verdicts.  This run measures it instead of asserting it.

WHAT IS NEW AGAINST 653.  653 had 3 grosses on a mechanical grid.  This run has (a) 17 grosses,
    (b) the record's OWN committed 4b passers rather than a fresh grid, (c) a MATCHED-GROSS TWIN
    for every book at every rung — the same panel, same cadence, every priced name equal-weighted
    to the SAME realised mean gross, no selection and no gate — so "does the selection do
    anything the exposure does not" is answered book by book and rung by rung, and (d) the small-
    cap panel as a third, genuinely different, panel.

TUNED PARAMETERS: exactly TWO, the two the queue names.
    (1) GROSS GRID: de-gross SCALE FACTOR k in {0.20, 0.25, ..., 1.00} — 17 rungs, ALL reported.
        Every weight is multiplied by k and the remainder held in CASH, so the realised mean
        gross at rung k is k x (the book's native mean gross), printed per book.  k = 1.00 is
        the book as committed.  HEADLINE RUNG = k 1.00 for the pass census, the whole ladder
        for the window.

        A FAILED FIRST PARAMETERISATION, recorded rather than deleted.  The ladder was first
        written as a TARGET MEAN GROSS g* in {0.20..1.00}, scaling each book by g*/native and
        clipping the daily total at 1.00 to respect PROTOCOL rule 2.  It failed its own gates:
        the clipped-day share at g* = 1.00 ran 12.7%..100.0% (the band books hold cash on gated
        days, so matching their MEAN gross to 1.00 pins their daily gross at the 1.00 ceiling on
        most days and stops being a scale at all), and G5 affinity fell to 0.9865.  You cannot
        up-gross these books without leverage, so the only clip-free ladder is a DE-GROSS ladder.
        That is the parameterisation used below; the failed one is reported here and nowhere
        else, because no number was read off it.
    (2) PANEL in {U56, B136, SMALL483}.
            U56       research/universe.json (ETF + mega-cap), the live book's panel
            B136      universe_broad.json, 136 large caps
            SMALL483  the sub-$2B panel, tickers with max_1d_move >= 1.0 DROPPED FIRST per
                      data/small_meta.csv.  SURVIVORSHIP is severe here (current constituents
                      of a screen) and is restated at every use.

BOOKS
    SHELF     the 8 committed 4b KEEP-candidate memos this lane rebuilds and gates (idea 851's
              shelf, restated verbatim; each on its own native panel).
    PORTABLE  4 book FORMS run on ALL THREE panels, so the panel dial has something to move:
              band003, band008 (RULES v2 band at two widths), qroll-q012-w1008-d050 (the breadth
              gate), r6top20 (6-month-return top 20).  12 book x panel cells.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_FLAT     Sharpe is flat in gross: max |Sharpe(g*) - Sharpe(1.00)| over the 17 rungs is
               under 0.10 for a MAJORITY of books.
    H_WINDOW   no book passes 4b at ALL 17 rungs, i.e. every committed 4b pass has a gross
               WINDOW rather than being a property of the selection.  (653 found 0 of 13 passing
               at all three of its grosses; this is the same claim at 17.)
    H_LEGS     the leg that fails at the bottom of the ladder is CAGRFLOOR and the leg that fails
               at the top is DDCAP, for a majority of books with a non-empty window.
    H_TWIN     a MAJORITY of the record's committed 4b passers do NOT beat their matched-gross
               twin on full-sample Sharpe at their own native gross.  Declared in this direction
               deliberately: if selection were doing the work the honest prior would be the
               opposite, and 653's 0.0052 says it is not.
    H_R8       adding a matched-gross leg to the rule-8 chooser (pick the best book that BEATS
               its twin, instead of the best book) does not cost OOS Sharpe.

GATES (printed before any new number; all must pass)
    G1  scale identity: k = 1.00 reproduces the unscaled book exactly (max|d| < 1e-12).
    G2  the 8 SHELF books reproduce their committed memo headlines (Sharpe 0.030, MaxDD 1.5 pp).
    G3  SPY reproduces the record's committed 4b comparand 15.16% / 0.8861 / -33.72% on U56's
        calendar, and each panel's own SPY comparand is printed (the small panel starts 2010, so
        its bars are NOT the record's and are re-priced on its own calendar).
    G4  no leverage and no clipping anywhere: max daily total weight <= 1.0 + 1e-9 at every
        rung, and ZERO clipped days (the de-gross ladder cannot clip by construction; the gate
        is what the first parameterisation failed).
    G5  affinity check: the correlation between a book's k=0.20 and k=1.00 daily returns is
        > 0.995 (if de-grossing were NOT near-affine the whole mechanism claim is wrong).

PROTOCOL: 10 bps per unit turnover (25 also reported), weights decided at close t applied at t+1,
    no shorting, no leverage.  Both KEEP paths on every row.  Rule 8: chosen on the first half
    (2009/2010-2016) alone, OOS (2017-2026) read once per (panel, chooser).

Outputs (committed under research/backtests/):
    .console.txt      full log
    .ladder.csv       every book x panel x rung x cost: metrics, twin, 4a/4b verdicts, fail legs
    .windows.csv      per book: the gross window, its width, the leg that closes each end
    .walkforward.csv  rule-8, plain vs matched-gross chooser, per panel

Run: python research/backtests/2026-09-14_is-EVERY-4b-pass-on-the-record-decided-by-GROSS-alone_cloud.py
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
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import rebalance_mask  # noqa: E402

DATE = "2026-09-14"
SLUG = "is-EVERY-4b-pass-on-the-record-decided-by-GROSS-alone"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FREQ, LAG, WARMUP, MAX_VOL = "W", 1, 260, 0.60
RUNGS_BPS = [10.0, 25.0]
BPS_HEAD = 10.0
OOS_START = "2017-01-01"

# ---- tuned dial 1: the de-gross scale ladder ---------------------------------------------
GROSS = [round(0.20 + 0.05 * i, 2) for i in range(17)]     # scale factor k, 0.20 .. 1.00
G_HEAD = 1.00

# ---- tuned dial 2: the panel -------------------------------------------------------------
PANELS = ["U56", "B136", "SMALL483"]

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


def verdicts(s, base, spy):
    p4a = (s["H1"] > base["H1"]) and (s["H2"] > base["H2"]) and (s["MaxDD"] >= base["MaxDD"])
    legs = dict(H1=s["H1"] > spy["H1"], H2=s["H2"] > spy["H2"],
                DDCAP=s["MaxDD"] >= 0.60 * spy["MaxDD"],
                CAGRFLOOR=s["CAGR"] >= 0.70 * spy["CAGR"])
    fails = "+".join(k for k, v in legs.items() if not v) or "-"
    return bool(p4a), all(legs.values()), fails


# ------------------------------------------------------------------ book forms
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def gate_mult(br, thr, depth, idx):
    m = pd.Series(1.0, index=idx).where(~(br < thr), 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def form_band(px, band):
    return rules_v2_weights(px, band, 1.00)


def form_qroll(px, q=0.12, w=1008, dep=0.50):
    elig = eligible_mask(px).astype(float)
    nn = elig.sum(axis=1).replace(0, np.nan)
    base = elig.div(nn, axis=0).fillna(0.0)
    br = breadth(px)
    thr = br.rolling(w, min_periods=w).quantile(q)
    return base.mul(gate_mult(br, thr, dep, px.index), axis=0)


def form_r6top20(px):
    r6 = px / px.shift(126) - 1
    return (r6.rank(axis=1, ascending=False) <= 20).astype(float) / 20.0


def twin_weights(px):
    """The MATCHED-GROSS TWIN: every priced name equal-weight, weekly, no selection, no gate.
    Scaled to the candidate's realised mean gross by the ladder, so the only difference between
    a book and its twin is WHICH names, never HOW MUCH."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def scale_to(W, k, start):
    """De-gross: multiply every weight by k, remainder to CASH.  Realised mean gross at rung k
    is k x the book's native mean gross.  k <= 1 and the native daily total is <= 1, so there is
    never leverage and never a clip.  Returns (scaled W, clipped-day share, native mean gross)."""
    native = float(W.loc[start:].sum(axis=1).mean())
    S = W * k
    over = S.sum(axis=1) > 1.0 + 1e-12
    return S, float(over.loc[start:].mean()), native


def main():
    t0 = time.time()
    P(f"# Idea 657 — is EVERY 4b pass on the record decided by GROSS alone? ({DATE}, cloud lane)")
    P(f"# 2 tuned dials: GROSS GRID {GROSS[0]}..{GROSS[-1]} in 0.05 ({len(GROSS)} rungs) x PANEL "
      f"{PANELS}.  ALL grid points reported.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent lists and SMALL483 is a current-"
      "constituent SCREEN (worse). Every LEVEL below is optimistic; the ACROSS-RUNG difference "
      "is the durable part.")

    # ---- panels ---------------------------------------------------------------------------
    U = load_universe().dropna(how="all").ffill()
    B = load_universe(broad=True).dropna(how="all").ffill()
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    Sm = load_universe(small=True).dropna(how="all").ffill()
    drop = [c for c in Sm.columns if c in bad]
    Sm = Sm.drop(columns=drop)
    P(f"\n   SMALL483: dropped {len(drop)} of {len(meta)} meta tickers with max_1d_move >= 1.0 "
      f"(present in the panel: {len(drop)}); panel now {Sm.shape[1] - 1} names + SPY")
    PX = {"U56": U, "B136": B, "SMALL483": Sm}
    STARTS = {}
    for p_, px in PX.items():
        STARTS[p_] = px.index[WARMUP]
        P(f"   {p_:<9} {px.shape}  scored {STARTS[p_].date()} .. {px.index[-1].date()} "
          f"({int((px.index >= STARTS[p_]).sum())} days)")

    # ---- books ----------------------------------------------------------------------------
    BOOKS = {}   # name -> dict(panel, freq, W, memo, src, family)

    # SHELF: idea 851's shelf, restated verbatim.
    s, above, vol20 = score(U, vol_scale=False)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    ab = (U > U.rolling(200).mean()).astype(float)
    nab = ab.sum(axis=1).replace(0, np.nan)
    rel = U / U.rolling(200).mean() - 1
    sel = (rel.rank(axis=1, ascending=False, pct=True) <= 0.50) & rel.notna()
    kq = sel.astype(float).sum(axis=1).replace(0, np.nan)
    r6B = B / B.shift(126) - 1
    SHELF = {
        "u56-v2band-gross100": ("U56", "W", rules_v2_weights(U, 0.03, 1.00), (0.1155, 1.2067, -0.1570)),
        "u56-band008-gross100": ("U56", "W", rules_v2_weights(U, 0.08, 1.00), (0.1137, 1.1439, -0.1905)),
        "u56-top20-band-m20": ("U56", "W", (rank <= 20).astype(float) * 0.75 / 20, (0.1287, 1.112, -0.1722)),
        "u56-marsrespread-gross075": ("U56", "W", ab.div(nab, axis=0).mul(0.75).fillna(0.0), (0.1155, 1.0914, None)),
        "u56-quantile50-respread-M": ("U56", "M", sel.astype(float).div(kq, axis=0).mul(0.75).fillna(0.0), (0.1547, 1.2359, -0.1980)),
        "b136-r620-gross065-W": ("B136", "W", (r6B.rank(axis=1, ascending=False) <= 20).astype(float) * 0.65 / 20, (0.1499, 1.1264, -0.1943)),
        "b136-qroll-q012-w1008-d050-g100": ("B136", "W", form_qroll(B), (0.1430, 1.1121, -0.1731)),
        "u56-k8-qroll-q017-w1008-d100-g100": ("U56", "W", form_qroll(U, 0.17, 1008, 1.00), (0.1416, 1.2226, -0.1479)),
    }
    for nm, (p_, f_, W, memo) in SHELF.items():
        BOOKS[nm] = dict(panel=p_, freq=f_, W=W, memo=memo, family="SHELF")

    # PORTABLE: 4 forms x 3 panels, so the PANEL dial has something to move.
    FORMS = {"band003": lambda px: form_band(px, 0.03),
             "band008": lambda px: form_band(px, 0.08),
             "qroll-q012-w1008-d050": form_qroll,
             "r6top20": form_r6top20}
    for p_, (fn, fmk) in product(PANELS, FORMS.items()):
        BOOKS[f"{p_}:{fn}"] = dict(panel=p_, freq="W", W=fmk(PX[p_]), memo=None,
                                   family="PORTABLE")

    P(f"\n   {len(BOOKS)} books: {sum(1 for b in BOOKS.values() if b['family'] == 'SHELF')} SHELF "
      f"(the record's committed 4b memos) + "
      f"{sum(1 for b in BOOKS.values() if b['family'] == 'PORTABLE')} PORTABLE "
      f"({len(FORMS)} forms x {len(PANELS)} panels)")

    # ---- benchmarks per panel --------------------------------------------------------------
    SPYR, V2R, TWINW = {}, {}, {}
    for p_, px in PX.items():
        st = STARTS[p_]
        SPYR[p_] = px["SPY"].pct_change().fillna(0.0).loc[st:].values
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, FREQ))
        V2R[p_] = {c: (r - t * c / 1e4).loc[st:].values for c in RUNGS_BPS}
        TWINW[p_] = twin_weights(px)

    # ----------------------------------------------------------------- GATES
    P("\n### GATES (printed before any new number)")
    ok = True

    # G1 scale identity at native gross
    nm0 = "u56-v2band-gross100"
    b0 = BOOKS[nm0]
    st0 = STARTS[b0["panel"]]
    W0 = b0["W"]
    nat0 = float(W0.loc[st0:].sum(axis=1).mean())
    S0, _, _ = scale_to(W0, 1.00, st0)
    g1 = float(np.abs(S0.values - W0.values).max())
    P(f"   G1 scale identity at k=1.00 on {nm0} (native mean gross {nat0:.4f}): max|d| "
      f"{g1:.3e} {'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    # precompute every (book, rung) run
    P("   ... running the ladder")
    RUNS, CLIP, NATIVE = {}, {}, {}
    for nm, b in BOOKS.items():
        px, st = PX[b["panel"]], STARTS[b["panel"]]
        mask = rebalance_mask(px.index, b["freq"])
        NATIVE[nm] = float(b["W"].loc[st:].sum(axis=1).mean())
        for g in GROSS:
            S, cl, _ = scale_to(b["W"], g, st)
            r, t = fast_run(px, S, mask)
            RUNS[(nm, g)] = {c: (r - t * c / 1e4).loc[st:].values for c in RUNGS_BPS}
            CLIP[(nm, g)] = cl
    # The twin is matched to the BOOK's realised mean gross at that rung, so it is keyed by
    # (book, rung), not just (panel, rung): equal-weight-all-names has native gross 1.0, so the
    # matching factor is exactly k x native_book.  Runs are cached by (panel, factor).
    TWIN, _tcache = {}, {}
    for nm, b in BOOKS.items():
        p_ = b["panel"]
        px, st = PX[p_], STARTS[p_]
        for g in GROSS:
            f = round(g * NATIVE[nm], 6)
            if (p_, f) not in _tcache:
                S, _, _ = scale_to(TWINW[p_], f, st)
                r, t = fast_run(px, S, rebalance_mask(px.index, FREQ))
                _tcache[(p_, f)] = {c: (r - t * c / 1e4).loc[st:].values for c in RUNGS_BPS}
            TWIN[(nm, g)] = _tcache[(p_, f)]

    # G2 shelf reproduction, at each book's own native gross rung (nearest 0.05)
    for nm in SHELF:
        b = BOOKS[nm]
        m = pack(RUNS[(nm, 1.00)][BPS_HEAD])
        mm = b["memo"]
        dS = abs(m["Sharpe"] - mm[1])
        dD = abs(m["MaxDD"] - mm[2]) if mm[2] is not None else 0.0
        b["repro"] = (dS <= REPRO_TOL_SHARPE) and (dD <= REPRO_TOL_DD)
        P(f"   G2 {nm:<34} native gross {NATIVE[nm]:.4f}  {m['CAGR']:.2%} / {m['Sharpe']:.4f} / "
          f"{m['MaxDD']:.2%}  vs memo {mm[0]:.2%} / {mm[1]:.4f}  dSharpe {dS:.4f} dMaxDD "
          f"{dD:.4f}  {'REPRODUCES' if b['repro'] else 'EXCLUDED'}")
    n_rep = sum(1 for nm in SHELF if BOOKS[nm]["repro"])
    P(f"   G2 {n_rep} of {len(SHELF)} committed 4b memos reproduce inside tolerance")
    ok &= n_rep >= 6

    # G3 SPY comparands per panel
    for p_ in PANELS:
        sp = pack(SPYR[p_])
        P(f"   G3 {p_:<9} SPY {sp['CAGR']:.4%} / {sp['Sharpe']:.4f} / {sp['MaxDD']:.4%}  "
          f"-> 4b floor {0.70 * sp['CAGR']:.2%}, cap {0.60 * sp['MaxDD']:.2%}")
    spU = pack(SPYR["U56"])
    g3 = max(abs(spU["CAGR"] - 0.1516), abs(spU["Sharpe"] - 0.8861), abs(spU["MaxDD"] + 0.3372))
    P(f"   G3 U56's SPY == the record's committed comparand: max|d| {g3:.2e} "
      f"{'PASS' if g3 < 1e-3 else 'FAIL'}.  SMALL483 starts 2010 so its bars are re-priced on "
      f"its own calendar and are NOT the record's.")
    ok &= g3 < 1e-3

    # G4 no leverage
    worst = 0.0
    for nm, b in BOOKS.items():
        st = STARTS[b["panel"]]
        for g in GROSS:
            S, _, _ = scale_to(b["W"], g, st)
            worst = max(worst, float(S.loc[st:].sum(axis=1).max()))
    nclip = max(CLIP.values())
    P(f"   G4 no leverage, no clipping: max daily total weight over every book x rung = "
      f"{worst:.6f}, max clipped-day share = {nclip:.3%} "
      f"{'PASS' if worst <= 1.0 + 1e-9 and nclip == 0.0 else 'FAIL'}")
    ok &= worst <= 1.0 + 1e-9 and nclip == 0.0

    # G5 affinity
    cors = [float(np.corrcoef(RUNS[(nm, 0.20)][BPS_HEAD], RUNS[(nm, 1.00)][BPS_HEAD])[0, 1])
            for nm in BOOKS]
    P(f"   G5 de-grossing is near-affine: corr(r at k=0.20, r at k=1.00) over {len(cors)} "
      f"books runs {min(cors):.6f}..{max(cors):.6f} "
      f"{'PASS' if min(cors) > 0.995 else 'FAIL'}")
    ok &= min(cors) > 0.995
    P(f"   GATES: {'ALL PASS' if ok else 'FAILURE — nothing below is read'}")
    assert ok

    # ----------------------------------------------------------------- PART A: the ladder
    P("\n### PART A — THE LADDER: every book x rung x cost, with its MATCHED-GROSS TWIN")
    rows = []
    for nm, b in BOOKS.items():
        if b["family"] == "SHELF" and not b["repro"]:
            continue
        p_ = b["panel"]
        sp = pack(SPYR[p_])
        for g, c in product(GROSS, RUNGS_BPS):
            s_ = pack(RUNS[(nm, g)][c])
            tw = pack(TWIN[(nm, g)][c])
            base = pack(V2R[p_][c])
            p4a, p4b, fails = verdicts(s_, base, sp)
            _, t4b, _ = verdicts(tw, base, sp)
            rows.append(dict(book=nm, family=b["family"], panel=p_, gross=g, bps=c,
                             native_gross=NATIVE[nm], realised_gross=g * NATIVE[nm],
                             clipped=CLIP[(nm, g)],
                             CAGR=s_["CAGR"], Sharpe=s_["Sharpe"], MaxDD=s_["MaxDD"],
                             H1=s_["H1"], H2=s_["H2"],
                             twin_CAGR=tw["CAGR"], twin_Sharpe=tw["Sharpe"],
                             twin_MaxDD=tw["MaxDD"], twin_pass4b=t4b,
                             dSharpe_vs_twin=s_["Sharpe"] - tw["Sharpe"],
                             SPY_CAGR=sp["CAGR"], SPY_MaxDD=sp["MaxDD"],
                             cap=0.60 * sp["MaxDD"], floor=0.70 * sp["CAGR"],
                             pass4a=p4a, pass4b=p4b, fail4b=fails))
    LD = pd.DataFrame(rows)
    LD.to_csv(f"{OUT}.ladder.csv", index=False)
    P(f"   {len(LD)} rows ({LD.book.nunique()} books x {len(GROSS)} rungs x {len(RUNGS_BPS)} "
      f"costs) written to .ladder.csv")

    hd = LD[LD.bps == BPS_HEAD]
    P(f"\n   Sharpe FLATNESS in gross (10 bps): max |Sharpe(g*) - Sharpe(1.00)| over the "
      f"{len(GROSS)} rungs")
    flat = {}
    for nm in hd.book.unique():
        t = hd[hd.book == nm].set_index("gross")
        flat[nm] = float((t.Sharpe - t.Sharpe.loc[G_HEAD]).abs().max())
    FL = pd.Series(flat).sort_values()
    P(f"      median {FL.median():.4f}, min {FL.min():.4f}, max {FL.max():.4f}; "
      f"{int((FL < 0.10).sum())} of {len(FL)} books under 0.10")
    P("      largest 5: " + ", ".join(f"{k} {v:.4f}" for k, v in FL.tail(5).items()))
    P(f"   H_FLAT (majority under 0.10): "
      f"{'PASS' if (FL < 0.10).sum() > len(FL) / 2 else 'FAIL'} "
      f"({int((FL < 0.10).sum())} of {len(FL)})")
    P(f"   for contrast, CAGR moves {hd.groupby('book').CAGR.apply(lambda s: s.max() - s.min()).median():.2%} "
      f"and MaxDD {hd.groupby('book').MaxDD.apply(lambda s: s.max() - s.min()).median():.2%} "
      f"(medians of the within-book range) over the same rungs.")

    # ----------------------------------------------------------------- PART B: the windows
    P("\n### PART B — THE GROSS WINDOW: at which rungs does each book pass 4b, and which leg "
      "closes each end?")
    wrows = []
    for nm in hd.book.unique():
        for c in RUNGS_BPS:
            t = LD[(LD.book == nm) & (LD.bps == c)].sort_values("gross")
            gp = t[t.pass4b].gross.tolist()
            lo_leg = hi_leg = "-"
            if gp:
                below = t[t.gross < min(gp)]
                above_ = t[t.gross > max(gp)]
                lo_leg = below.iloc[-1].fail4b if len(below) else "OPEN(bottom)"
                hi_leg = above_.iloc[0].fail4b if len(above_) else "OPEN(top)"
            wrows.append(dict(book=nm, family=t.iloc[0].family, panel=t.iloc[0].panel, bps=c,
                              native_gross=NATIVE[nm], n_pass=len(gp),
                              g_lo=(min(gp) if gp else np.nan),
                              g_hi=(max(gp) if gp else np.nan),
                              width=((max(gp) - min(gp)) if gp else np.nan),
                              contiguous=(len(gp) == 0 or
                                          len(gp) == 1 + int(round((max(gp) - min(gp)) / 0.05))),
                              closes_below=lo_leg, closes_above=hi_leg,
                              passes_all_rungs=(len(gp) == len(GROSS)),
                              native_pass4b=bool(t[np.isclose(t.gross, 1.00)].pass4b.iloc[0])))
    WD = pd.DataFrame(wrows)
    WD.to_csv(f"{OUT}.windows.csv", index=False)
    h = WD[WD.bps == BPS_HEAD].sort_values(["family", "panel", "book"])
    P(f"      {'book':<38}{'panel':<10}{'native':>7}{'#pass':>6}{'window':>14}{'contig':>8}"
      f"  closes below / above")
    for r in h.itertuples():
        win = "-" if r.n_pass == 0 else f"{r.g_lo:.2f}..{r.g_hi:.2f}"
        P(f"      {r.book:<38}{r.panel:<10}{r.native_gross:>7.2f}{r.n_pass:>6}{win:>14}"
          f"{str(r.contiguous):>8}  {r.closes_below} / {r.closes_above}")
    nall = int(h.passes_all_rungs.sum())
    P(f"\n   H_WINDOW (no book passes 4b at ALL {len(GROSS)} rungs): "
      f"{'PASS' if nall == 0 else 'FAIL'} ({nall} of {len(h)} do)")
    hw = h[h.n_pass > 0]
    lo_cagr = int(hw.closes_below.str.contains("CAGRFLOOR").sum())
    hi_dd = int(hw.closes_above.str.contains("DDCAP").sum())
    P(f"   H_LEGS (bottom closed by CAGRFLOOR, top by DDCAP, for a majority with a window): "
      f"{'PASS' if lo_cagr > len(hw) / 2 and hi_dd > len(hw) / 2 else 'FAIL'} "
      f"(bottom CAGRFLOOR {lo_cagr} of {len(hw)}, top DDCAP {hi_dd} of {len(hw)}; "
      f"{int((hw.closes_above == 'OPEN(top)').sum())} windows run to the top of the ladder)")
    P(f"   window widths (10 bps, books with a window): median {hw.width.median():.2f} of a "
      f"0.80-wide ladder; {int((hw.width <= 0.20).sum())} of {len(hw)} are 0.20 or narrower")

    # ----------------------------------------------------------------- PART C: the twin
    P("\n### PART C — THE MATCHED-GROSS TWIN: does the SELECTION beat the EXPOSURE?")
    P("   (twin = same panel, same weekly cadence, every priced name equal-weight, scaled to the "
      "SAME mean gross.  Only the choice of names differs.)")
    nat = []
    for nm in hd.book.unique():
        r = hd[(hd.book == nm) & np.isclose(hd.gross, 1.00)].iloc[0]
        nat.append(dict(book=nm, family=r.family, panel=r.panel, gross=r.realised_gross,
                        Sharpe=r.Sharpe, twin=r.twin_Sharpe, d=r.dSharpe_vs_twin,
                        pass4b=r.pass4b, twin_pass4b=r.twin_pass4b))
    NT = pd.DataFrame(nat)
    P(f"      {'book':<38}{'panel':<10}{'g*':>5}{'Sharpe':>9}{'twin':>9}{'delta':>9}"
      f"{'4b':>6}{'twin 4b':>9}")
    for r in NT.sort_values("d").itertuples():
        P(f"      {r.book:<38}{r.panel:<10}{r.gross:>5.2f}{r.Sharpe:>9.4f}{r.twin:>9.4f}"
          f"{r.d:>+9.4f}{('PASS' if r.pass4b else 'fail'):>6}"
          f"{('PASS' if r.twin_pass4b else 'fail'):>9}")
    sh = NT[NT.family == "SHELF"]
    nbeat = int((sh.d > 0).sum())
    P(f"\n   SHELF (the record's committed 4b passers): {nbeat} of {len(sh)} beat their matched-"
      f"gross twin on full-sample Sharpe at their own native gross; median delta "
      f"{sh.d.median():+.4f}")
    P(f"   H_TWIN (a MAJORITY do NOT beat the twin): "
      f"{'PASS' if nbeat <= len(sh) / 2 else 'FAIL'} ({len(sh) - nbeat} of {len(sh)} do not)")
    both = hd[hd.pass4b]
    P(f"   across the whole ladder at 10 bps: {int(both.twin_pass4b.sum())} of {len(both)} 4b-"
      f"passing rows have a twin that ALSO passes 4b at the same gross "
      f"({100 * both.twin_pass4b.mean():.1f}%) — a pass the exposure alone would have earned.")

    # ----------------------------------------------------------------- PART D: rule 8
    P("\n### PART D — RULE 8: book x gross chosen on the FIRST HALF alone, OOS read ONCE per "
      "(panel, chooser).  PLAIN = argmax IS Sharpe.  MATCHED = argmax IS Sharpe among books "
      "that BEAT their matched-gross twin IN SAMPLE.")
    wf = []
    for p_ in PANELS:
        px, st = PX[p_], STARTS[p_]
        eidx = px.index[px.index >= st]
        oos = np.asarray(eidx >= pd.Timestamp(OOS_START))
        ism = ~oos
        pool = [(nm, g) for nm, b in BOOKS.items() for g in GROSS
                if b["panel"] == p_ and not (b["family"] == "SHELF" and not b["repro"])]
        def issh(nm, g):
            return fsharpe(RUNS[(nm, g)][BPS_HEAD][ism])
        matched = [(nm, g) for nm, g in pool
                   if issh(nm, g) > fsharpe(TWIN[(nm, g)][BPS_HEAD][ism])]
        for chooser, cand in (("PLAIN", pool), ("MATCHED", matched)):
            if not cand:
                wf.append(dict(panel=p_, chooser=chooser, pick="NONE-ELIGIBLE",
                               pool_n=len(pool), elig_n=0, pass4a=False, pass4b=False,
                               fail4b="EMPTY-POOL"))
                continue
            nm, g = max(cand, key=lambda kv: issh(*kv))
            s_ = pack(RUNS[(nm, g)][BPS_HEAD][oos])
            tw = pack(TWIN[(nm, g)][BPS_HEAD][oos])
            base = pack(V2R[p_][BPS_HEAD][oos])
            sp = pack(SPYR[p_][oos])
            p4a, p4b, fails = verdicts(s_, base, sp)
            fl = pack(RUNS[(nm, g)][BPS_HEAD])
            wf.append(dict(panel=p_, chooser=chooser, pick=f"{nm}@g{g:.2f}", pool_n=len(pool),
                           elig_n=len(cand), IS_Sharpe=issh(nm, g),
                           FULL_CAGR=fl["CAGR"], FULL_Sharpe=fl["Sharpe"], FULL_MaxDD=fl["MaxDD"],
                           FULL_H1=fl["H1"], FULL_H2=fl["H2"],
                           OOS_CAGR=s_["CAGR"], OOS_Sharpe=s_["Sharpe"], OOS_MaxDD=s_["MaxDD"],
                           OOS_twin_Sharpe=tw["Sharpe"], OOS_dvs_twin=s_["Sharpe"] - tw["Sharpe"],
                           V2_OOS_CAGR=base["CAGR"], V2_OOS_Sharpe=base["Sharpe"],
                           V2_OOS_MaxDD=base["MaxDD"], SPY_OOS_CAGR=sp["CAGR"],
                           SPY_OOS_Sharpe=sp["Sharpe"], SPY_OOS_MaxDD=sp["MaxDD"],
                           pass4a=p4a, pass4b=p4b, fail4b=fails))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    for r in WF.itertuples():
        if r.pick == "NONE-ELIGIBLE":
            P(f"   {r.panel:<9} {r.chooser:<8} pool {r.pool_n:>3}/elig {r.elig_n:>3}  "
              f"NO BOOK IN THE POOL BEATS ITS MATCHED-GROSS TWIN IN SAMPLE — the chooser has "
              f"nothing to pick, which is itself the result for this panel.")
            continue
        P(f"   {r.panel:<9} {r.chooser:<8} pool {r.pool_n:>3}/elig {r.elig_n:>3}  "
          f"pick {r.pick:<42} IS {r.IS_Sharpe:.4f}  full {r.FULL_CAGR:.2%}/{r.FULL_Sharpe:.4f}/"
          f"{r.FULL_MaxDD:.2%} (H1 {r.FULL_H1:.3f}/H2 {r.FULL_H2:.3f})  OOS {r.OOS_CAGR:.2%}/"
          f"{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%} | twin OOS {r.OOS_twin_Sharpe:.4f} "
          f"(d {r.OOS_dvs_twin:+.4f}) | v2 {r.V2_OOS_CAGR:.2%}/{r.V2_OOS_Sharpe:.4f}/"
          f"{r.V2_OOS_MaxDD:.2%} | SPY {r.SPY_OOS_CAGR:.2%}/{r.SPY_OOS_Sharpe:.4f}/"
          f"{r.SPY_OOS_MaxDD:.2%} | 4b {'PASS' if r.pass4b else 'FAIL ' + r.fail4b}  "
          f"4a {'PASS' if r.pass4a else 'FAIL'}")
    d, empty = [], []
    for p_ in PANELS:
        u = WF[WF.panel == p_].set_index("chooser")
        if u.loc["MATCHED"].pick == "NONE-ELIGIBLE":
            empty.append(p_)
            continue
        d.append(float(u.loc["MATCHED"].OOS_Sharpe - u.loc["PLAIN"].OOS_Sharpe))
    P(f"\n   MATCHED minus PLAIN OOS Sharpe over the {len(d)} panels where the matched pool is "
      f"non-empty: {', '.join(f'{x:+.4f}' for x in d)}; median {np.median(d):+.4f}"
      + (f".  EMPTY on {empty}: no book beats its twin in sample there, so the leg is not a "
         f"tie-break but a VETO." if empty else ""))
    P(f"   H_R8 (the matched-gross leg does not cost OOS Sharpe where it can be applied): "
      f"{'PASS' if np.median(d) >= -1e-9 else 'FAIL'}"
      + (f" — but it VETOES the whole pool on {len(empty)} of {len(PANELS)} panels ({empty}), "
         f"which is a cost the Sharpe delta does not show." if empty else ""))
    ok_rows = WF[WF.pick != "NONE-ELIGIBLE"]
    nbeat_oos = int((ok_rows.OOS_dvs_twin > 0).sum())
    P(f"   every rule-8 pick vs its OWN twin out of sample: {nbeat_oos} of {len(ok_rows)} beat "
      f"it; deltas " + ", ".join(f"{r.panel}/{r.chooser} {r.OOS_dvs_twin:+.4f}"
                                 for r in ok_rows.itertuples()))

    P(f"\n### done in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

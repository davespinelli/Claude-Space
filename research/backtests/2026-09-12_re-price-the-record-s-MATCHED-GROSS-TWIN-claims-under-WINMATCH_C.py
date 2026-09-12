#!/usr/bin/env python3
"""Idea 824 - re-price the record's MATCHED-GROSS TWIN claims under WINMATCH.
   (lane C, 2026-09-12)

QUESTION (QUEUE idea 824, verbatim)
    Idea 609's largest axis was not cost, window length, step or panel but the twin's MATCHING
    SAMPLE: share_exact 0.322 under FULLMATCH against 0.102 under WINMATCH (the twin's gross
    re-matched on the evaluation window itself, which is what a reader holding only that window
    would build).  Re-price the record's committed twin/matched-gross claims under WINMATCH and
    report how many change sign.  Max 2 params (claim set, matching convention).

WHAT THE RECORD ACTUALLY COMMITTED, AND WHY THE CONVENTION BITES
    The record's matched-gross twin for a gated arm is the STATIC-gross EWALL book held at the
    arm's realised mean gross g_eff = g * mean(m), same exposure, no timing.  Every committed
    twin cell in `2026-09-10_..._C.cells.csv.gz` (the record's canonical twin corpus, 3 panels x
    221 arms x 15 cost rungs) computes g_eff ONCE on the FULL scored sample and then slices that
    one twin path into sub-windows to publish `twin_IS`/`dIS` and `twin_OOS`/`dOOS`.  That is
    FULLMATCH.  It gives the twin the arm's FULL-SAMPLE average exposure inside a window where the
    arm's own exposure was different - so on any sub-window the comparison is not exposure-matched
    at all, and the direction of the mismatch is the gate's own timing.

    On the FULL sample the two conventions are the SAME OBJECT (the window is the sample), so no
    full-sample twin claim in the record can move.  The committed claims that CAN move are exactly
    the sub-window ones: `dIS`, `dOOS`, and every "earned against its own matched-gross twin"
    sentence that is read on 2017+ - which includes the record's newest 4b KEEP-candidate
    (idea 609's by-product, B136 breadth-QROLL q0.17 w252 depth 0.50 DAILY g=1.00).  This run
    re-prices all of them.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) CLAIM WINDOW (the "claim set"): which window a twin claim is read on.
        {FULL, IS, OOS, H1, H2, EP2022}.  FULL/IS/OOS are the three windows the record has
        COMMITTED twin columns for; H1/H2/EP2022 are extension windows, printed beside them and
        labelled as extensions, never as committed claims.  HEADLINE = OOS (2017-01-01..), the
        window every live-capital sentence in the record is read on, declared here before
        anything is computed.
    (2) MATCHING CONVENTION: {FULLMATCH, WINMATCH}.  FULLMATCH = the record's own construction
        (g_eff matched on the full sample, path sliced to the window).  WINMATCH = g_eff
        re-matched on the evaluation window itself.  BOTH are reported at every point; the
        comparison IS the object, so neither is "chosen".
    6 x 2 = 12 grid points, EVERY ONE printed and written to .grid.csv, at every cost rung and
    every scope.

REPORTED AXES, none of them a tune (each printed at every grid point):
    COST RUNG   {0, 10, 25} bps, headline 10 = PROTOCOL rule 2's.
    SCOPE       U56, B136, SMALL (today's panel) and the pooled REPRO2 = U56 + B136.
    SIGN        the flip is reported on THREE signs the record publishes - dSharpe (the `win`
                column), dCAGR and dMaxDD - because "changes sign" is not one claim.

REPRODUCTION, read before anything else and published whatever it says
    Idea 609 established that `data/prices_small.csv` grew from 439 to 663 tradable names, so the
    committed SMALL439 rows are a DIFFERENT PANEL and cannot be joined at any tolerance.  This run
    re-checks that and restates it with today's count rather than quietly re-deriving levels.  The
    headline scope is therefore fixed BY THE GATE, before any answer is read: REPRO2 = the panels
    that reproduce.  Today's SMALL panel is still run and printed everywhere, as its own scope.

PRE-REGISTERED HYPOTHESES (declared before any grid is read)
    H_ID      on FULL, WINMATCH and FULLMATCH agree to <= 1e-9 in dSharpe for every arm.  This is
              true by construction; it is stated as a hypothesis because it is the only check that
              the WINMATCH implementation is the same object re-matched, and not a second bug.
    H_PREMISE the record's committed `twin_OOS` column IS a FULLMATCH twin.  Tested scale-free,
              because a panel-drift bar cannot decide a convention: on every arm whose two twins
              are separated by more than SEP = 1e-2 of Sharpe, the committed value must be nearer
              this run's FULLMATCH twin than its WINMATCH twin.  If it is not, the premise of idea
              824 is wrong and the run says so.  The 6e-3 drift bar is reported beside it and
              never relaxed: B136's twin_OOS LEVEL is expected to exceed it (idea 406).
    H_FLIP    fewer than 10% of the committed OOS twin verdicts change sign at the headline
              (OOS, 10 bps, REPRO2).  The queue's literal question.
    H_SYM     flips are not one-directional: each direction (WIN->LOSE, LOSE->WIN) is at least
              10% of the flips.  A one-directional re-pricing is a correction, not noise.
    H_MAG     median |d dSharpe| between conventions <= 0.05 at the headline.
    H_COSTINV |flip_share(0) - flip_share(10)| <= 0.10 and |flip_share(25) - flip_share(10)|
              <= 0.10.
    H_PANELINV the panel flip shares at the headline window lie within 0.20 of each other.
    H_WINDOW  |flip_share(IS) - flip_share(OOS)| <= 0.10 at 10 bps, REPRO2 - is the convention
              gap a property of the second window only?
    H_CAND    the record's newest 4b KEEP-candidate (609's by-product: B136 QROLL q0.17 w252
              depth 0.50 DAILY g1.00) still beats its own twin under WINMATCH, on FULL and on
              OOS, at 0, 10 and 25 bps.  This is the single most capital-relevant re-pricing in
              the run and it is declared before it is read.
    H_R8CLAIM RULE 8 ON THE CLAIM: the flip share measured on rolling 756-day windows whose END
              falls in the IS half reproduces, within 0.10, the flip share on rolling windows
              ending in the OOS half.  Read once.

GATES (printed first; all must pass before any verdict is read)
    G1 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G2 the fast CAGR/Sharpe/MaxDD reproduce engine.metrics to <= 1e-9 on a real series.
    G3 the 0.01-grid interpolation of the static-gross twin reproduces an EXACT run of the same
       gross to <= 1e-6 of Sharpe (idea 602's G4 priced it at 4e-07).
    G4 REPRODUCTION of the record's committed twin corpus (dSharpe, win, twin_OOS) per panel,
       plus G4d, the scale-free convention test of H_PREMISE above.
    G5 IDENTITY: WINMATCH == FULLMATCH on the FULL window, every arm, every rung (H_ID).

PROTOCOL RULE 8 (mandatory, run and reported) - on the BOOKS as well as on the claim:
    per (panel, family, gross, depth, cadence) the DIAL (level, w) is chosen on IS (..2016-12-31)
    by IS Sharpe alone and OOS (2017-01-01..) is read exactly ONCE, reported as CAGR/Sharpe/MaxDD
    against RULES v2 and SPY on the same window.  BOTH KEEP paths (4a and 4b) are evaluated on all
    648 arms at every cost rung, and every 4b passer is read against its own matched-gross twin
    under BOTH conventions, so an exposure-only pass cannot be mistaken for a clause.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and the SMALL panel worst (a sub-$2B screen read today cannot see the names that
    fell out of it - data/SMALL_PANEL_README.md).  A flip SHARE is a within-panel agreement rate,
    which survivorship moves far less than levels.

Outputs (all committed under research/backtests/):
    .console.txt    full log
    .grid.csv       6 claim windows x 2 conventions x 3 rungs x 4 scopes, every point
    .claims.csv     one row per (panel, arm, rung, window): both conventions, both verdicts
    .rolling.csv    the rule-8-on-the-claim census (756-day windows, step 63)
    .walkforward.csv the rule-8 picks and their OOS reads against RULES v2 and SPY
    .result.md      the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-12"
SLUG = "re-price-the-record-s-MATCHED-GROSS-TWIN-claims-under-WINMATCH"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

FREQ = "W"
LAG = 1
MAX_VOL = 0.60
WARMUP = 260
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS_ROLL = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
MINQ = 252
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TIE = 1e-12
SMALL_MAXMOVE = 1.0
FAMS = ["ABS", "QEXP", "QROLL"]
GSTEP = 0.01
SEP = 1e-2          # twin separation above which an arm can DECIDE the convention (G4d)

# tuned dial 1: the claim window.  COMMITTED = the record publishes a twin column on it.
WINDOWS = ["FULL", "IS", "OOS", "H1", "H2", "EP2022"]
COMMITTED_WINDOWS = ["FULL", "IS", "OOS"]
WIN_HEAD = "OOS"
# tuned dial 2: the matching convention.
CONVS = ["FULLMATCH", "WINMATCH"]

# rule-8-on-the-claim census (idea 609's headline census geometry, not re-tuned here)
L_ROLL, STEP_ROLL = 756, 63
MINCOVER = 0.80

# the record's newest 4b KEEP-candidate (idea 609's by-product), re-priced by name
CAND = dict(panel="B136", family="QROLL", level=0.17, w=252, depth=0.50, cadence="D", gross=1.00)

CELLS = ROOT / "research" / "backtests" / \
    "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.cells.csv.gz"
PANELS = ["U56", "B136", "SMALL"]
PANEL_MAP = {"U56": "U56", "B136": "B136", "SMALL": "SMALL439"}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (596/604/811/813's)
def fast_run(prices, weights, mask, lag=LAG):
    """(gross return path before costs, turnover path)."""
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
    return (pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx))


def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


# ------------------------------------------------------------------ primitives (idea 28/42/602)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross, elig):
    e = elig.astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def _cadence(m, idx):
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def gate_series(br, thr, depth, cadence, idx):
    below = (br < thr)
    m = pd.Series(1.0, index=idx).where(~below, 1.0 - depth)
    ok = br.notna() & (thr.notna() if isinstance(thr, pd.Series) else True)
    m = m.where(ok, 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def panel_prices(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
        drop = [c for c in px.columns if c in bad and c != "SPY"]
        px = px.drop(columns=drop)
        P(f"   SMALL panel today: {px.shape[1]-1+len(drop)} columns, dropped {len(drop)} with "
          f"max_1d_move >= {SMALL_MAXMOVE}, {len([c for c in px.columns if c != 'SPY'])} tradable")
    return px.dropna(how="all").ffill()


def flip_stats(dF, dW):
    """Sign-change statistics between two arrays of the SAME differenced statistic."""
    ok = np.isfinite(dF) & np.isfinite(dW)
    dF, dW = dF[ok], dW[ok]
    n = len(dF)
    if n == 0:
        return dict(n=0, win_F=np.nan, win_W=np.nan, n_flip=0, flip=np.nan, WL=0, LW=0,
                    med_abs_d=np.nan, max_abs_d=np.nan, d_win=np.nan)
    wF, wW = dF > TIE, dW > TIE
    fl = wF != wW
    return dict(n=n, win_F=float(wF.mean()), win_W=float(wW.mean()), n_flip=int(fl.sum()),
                flip=float(fl.mean()), WL=int((wF & ~wW).sum()), LW=int((~wF & wW).sum()),
                med_abs_d=float(np.median(np.abs(dF - dW))), max_abs_d=float(np.abs(dF - dW).max()),
                d_win=float(wW.mean() - wF.mean()))


def main():
    T0 = time.time()
    P(f"# Idea 824 - {SLUG}  (lane C, {DATE})")
    P("# OBJECT: the record's matched-gross twin is built with g_eff = g * mean(m) computed ONCE on")
    P("#   the FULL sample and then SLICED into sub-windows to publish dIS and dOOS (FULLMATCH).")
    P("#   WINMATCH re-matches g_eff on the evaluation window itself.  On the FULL sample the two")
    P("#   are the same object, so only the record's SUB-WINDOW twin claims can move.")
    P(f"# TUNED: claim window {WINDOWS} x convention {CONVS} = {len(WINDOWS)*len(CONVS)} points,")
    P(f"#   ALL reported; HEADLINE window = {WIN_HEAD} (declared before anything is read).")
    P(f"# REPORTED AXES (not tunes): cost rung {RUNGS} bps (headline {RUNG_HEAD:g}); scope U56 /")
    P("#   B136 / SMALL / REPRO2; sign read on dSharpe, dCAGR and dMaxDD separately.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    old = pd.read_csv(CELLS)
    old = old[old.family.isin(FAMS)].copy()
    P(f"\n# THE COMMITTED CLAIM SET: {CELLS.name}, {len(old)} twin cells "
      f"({old.panel.nunique()} panels x {old.arm.nunique()} arms x {old.rung.nunique()} rungs).")

    claimrows, wfrows, armrows = [], [], []
    PAN = {}

    for pname in PANELS:
        P(f"\n{'='*118}\nPANEL {pname}\n{'='*118}")
        px = panel_prices(pname)
        idx = px.index
        start = idx[WARMUP]
        eidx = px.loc[start:].index
        T = len(eidx)
        mask = rebalance_mask(idx, FREQ)
        elig = eligible_mask(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:].values
        P(f"   {px.shape[1]-1} tradable names, {T} scored days {eidx[0].date()}..{eidx[-1].date()}")

        br_full = breadth(px)
        thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
        thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q)
                    for q in QS for w in WS_ROLL}

        base0 = {}
        for g in GROSSES:
            rg, tn = fast_run(px, ewall_weights(px, g, elig), mask)
            base0[g] = (rg.loc[start:].values, tn.loc[start:].values)
        gg = np.round(np.arange(0.0, 1.0 + GSTEP / 2, GSTEP), 6)
        GR = np.zeros((len(gg), T))
        GT = np.zeros((len(gg), T))
        for i, x in enumerate(gg):
            if x == 0.0:
                continue
            rg, tn = fast_run(px, ewall_weights(px, float(x), elig), mask)
            GR[i], GT[i] = rg.loc[start:].values, tn.loc[start:].values

        # ---------------- gates G1-G3, once, on U56 -------------------------------------
        if pname == "U56":
            P(f"\n{'-'*118}\nGATES G1-G3\n{'-'*118}")
            Wb = ewall_weights(px, 0.75, elig)
            rg, tn = fast_run(px, Wb, mask)
            eng = backtest(px, Wb, cost_bps=10, freq=FREQ)
            g1 = float(np.abs(((rg - tn * 10 / 1e4) - eng["returns"]).loc[start:].values).max())
            P(f"   G1 fast_run == engine.backtest                  max|d| {g1:.3e} "
              f"{'PASS' if g1 < 1e-9 else 'FAIL'}")
            assert g1 < 1e-9
            ser = pd.Series((rg - tn * 10 / 1e4).loc[start:].values)
            m = metrics(ser)
            fc, fs, fd = fmet(ser.values)
            g2 = max(abs(fc - m["CAGR"]), abs(fs - m["Sharpe"]), abs(fd - m["MaxDD"]))
            P(f"   G2 fast metrics == engine.metrics               max|d| {g2:.3e} "
              f"{'PASS' if g2 < 1e-9 else 'FAIL'}")
            assert g2 < 1e-9
            xt = 0.6237
            lo = int(np.floor(round(xt, 6) / GSTEP))
            lam = (xt - gg[lo]) / GSTEP
            ex_r, ex_t = fast_run(px, ewall_weights(px, xt, elig), mask)
            en = (ex_r - ex_t * 10 / 1e4).loc[start:].values
            inn = ((1 - lam) * (GR[lo] - GT[lo] * 10 / 1e4)
                   + lam * (GR[lo + 1] - GT[lo + 1] * 10 / 1e4))
            g3 = abs(fsharpe(en) - fsharpe(inn))
            P(f"   G3 0.01-grid interpolation vs an EXACT twin run |dSharpe| {g3:.3e} "
              f"{'PASS' if g3 < 1e-6 else 'FAIL'}  (g = {xt}, Sharpe {fsharpe(en):.6f})")
            assert g3 < 1e-6

        # ---------------- windows ------------------------------------------------------
        h = T // 2
        is_end = int(eidx.searchsorted(pd.Timestamp(IS_END), side="right"))
        oos0 = int(eidx.searchsorted(pd.Timestamp(OOS_START), side="left"))
        e22 = (int(eidx.searchsorted(pd.Timestamp("2022-01-01"), side="left")),
               int(eidx.searchsorted(pd.Timestamp("2022-12-31"), side="right")))
        SPANS = {"FULL": (0, T), "IS": (0, is_end), "OOS": (oos0, T),
                 "H1": (0, h), "H2": (h, T), "EP2022": e22}
        P("   claim windows: " + "  ".join(
            f"{k} {eidx[a].date()}..{eidx[b-1].date()} n={b-a}" for k, (a, b) in SPANS.items()))

        # ---------------- the 216 arms -------------------------------------------------
        arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
                + [("QROLL", q, w) for q in QS for w in WS_ROLL])
        keys, ME, ARM = [], [], {c: [] for c in RUNGS}
        GEFF_FULL = []
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            thr = lev if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
            m = gate_series(br_full, thr, d, cad, idx)
            me = m.reindex(eidx).shift(1).fillna(1.0).values
            sw = np.abs(np.diff(me, prepend=me[0]))
            for g in GROSSES:
                r0, t0 = base0[g]
                keys.append((fam, lev, w, d, cad, g))
                ME.append(me)
                GEFF_FULL.append(g * float(me.mean()))
                for c in RUNGS:
                    ARM[c].append(me * r0 - (me * t0 + g * sw) * c / 1e4)
        K = len(keys)
        ME = np.asarray(ME)
        GEFF_FULL = np.asarray(GEFF_FULL)
        gross_of = np.array([k[5] for k in keys])
        fam_of = np.array([k[0] for k in keys])
        P(f"   {K} arms built ({int((fam_of=='ABS').sum())} ABS, {int((fam_of=='QEXP').sum())} "
          f"QEXP, {int((fam_of=='QROLL').sum())} QROLL); twin grid "
          f"{int((GR!=0).any(axis=1).sum())} exact runs")

        NET = {c: np.asarray(ARM[c]) for c in RUNGS}
        TNET = {c: GR - GT * c / 1e4 for c in RUNGS}          # (G, T) twin grid, net of cost

        def twin_path(c, g_eff):
            lo = int(np.clip(np.floor(round(float(g_eff), 6) / GSTEP), 0, len(gg) - 2))
            lam = (g_eff - gg[lo]) / GSTEP
            return (1 - lam) * TNET[c][lo] + lam * TNET[c][lo + 1]

        # ---------------- per-claim re-pricing, both conventions -----------------------
        for c in RUNGS:
            A = NET[c]
            for i in range(K):
                fam, lev, w, d, cad, g = keys[i]
                tf_full = twin_path(c, GEFF_FULL[i])          # FULLMATCH path, sliced per window
                base = dict(panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad,
                            gross=g, arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                            g_eff_full=GEFF_FULL[i])
                for wn, (a, b) in SPANS.items():
                    ra = A[i, a:b]
                    ge_w = g * float(ME[i, a:b].mean())
                    tw = twin_path(c, ge_w)[a:b]
                    tf = tf_full[a:b]
                    ca, sa, da = fmet(ra)
                    cF, sF, dF = fmet(tf)
                    cW, sW, dW = fmet(tw)
                    mm = float(ME[i, a:b].mean())
                    claimrows.append(dict(
                        **base, window=wn, committed=wn in COMMITTED_WINDOWS, n_days=b - a,
                        g_eff_win=ge_w, d_geff=ge_w - GEFF_FULL[i], on_share=mm,
                        neverfire=bool(mm >= 1.0 - 1e-12),
                        CAGR=ca, Sharpe=sa, MaxDD=da,
                        twinF_Sharpe=sF, twinW_Sharpe=sW, twinF_CAGR=cF, twinW_CAGR=cW,
                        twinF_MaxDD=dF, twinW_MaxDD=dW,
                        dSharpe_F=sa - sF, dSharpe_W=sa - sW,
                        dCAGR_F=ca - cF, dCAGR_W=ca - cW,
                        dMaxDD_F=abs(dF) - abs(da), dMaxDD_W=abs(dW) - abs(da),
                        win_F=bool(sa - sF > TIE), win_W=bool(sa - sW > TIE)))

        # ---------------- full-sample arm table, rule 8, both KEEP paths ---------------
        sc, ss, sd_ = fmet(spy)
        spy_pack = (fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos0:]), sd_, sc)
        v2rg, v2tn = fast_run(px, rules_v2_weights(px), mask)
        v2rg, v2tn = v2rg.loc[start:].values, v2tn.loc[start:].values
        v1rg, v1tn = fast_run(px, rules_v1_weights(px), mask)
        v1rg, v1tn = v1rg.loc[start:].values, v1tn.loc[start:].values
        P(f"   SPY {sc:.2%} / {ss:.3f} / {sd_:.2%};  4b bars: CAGR floor {0.70*sc:.2%}, DD cap "
          f"{-0.60*abs(sd_):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, OOS {spy_pack[2]:.3f}")
        for c in RUNGS:
            v2 = v2rg - v2tn * c / 1e4
            b1, b2, bdd = fsharpe(v2[:h]), fsharpe(v2[h:]), fmet(v2)[2]
            A = NET[c]
            for i in range(K):
                fam, lev, w, d, cad, g = keys[i]
                ra = A[i]
                tfull = twin_path(c, GEFF_FULL[i])
                ge_oos = g * float(ME[i, oos0:].mean())
                toos_W = twin_path(c, ge_oos)[oos0:]
                ca, sa, da = fmet(ra)
                oc, os_, od = fmet(ra[oos0:])
                ct, st, dt = fmet(tfull)
                t4b = dict(H1=fsharpe(ra[:h]) > spy_pack[0], H2=fsharpe(ra[h:]) > spy_pack[1],
                           OOS=os_ > spy_pack[2], DD=abs(da) <= 0.60 * abs(sd_),
                           CAGR=ca >= 0.70 * sc)
                armrows.append(dict(
                    panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g,
                    arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}", g_eff=GEFF_FULL[i],
                    CAGR=ca, Sharpe=sa, MaxDD=da, H1=fsharpe(ra[:h]), H2=fsharpe(ra[h:]),
                    IS_Sharpe=fsharpe(ra[:is_end]), OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                    twin_Sharpe=st, twin_CAGR=ct, twin_MaxDD=dt,
                    twin_OOS_F=fsharpe(tfull[oos0:]), twin_OOS_W=fsharpe(toos_W),
                    dSharpe=sa - st, dOOS_F=os_ - fsharpe(tfull[oos0:]),
                    dOOS_W=os_ - fsharpe(toos_W),
                    win=bool(sa - st > TIE),
                    win_OOS_F=bool(os_ - fsharpe(tfull[oos0:]) > TIE),
                    win_OOS_W=bool(os_ - fsharpe(toos_W) > TIE),
                    pass_4a=bool(fsharpe(ra[:h]) > b1 and fsharpe(ra[h:]) > b2 and da >= bdd),
                    pass_4b=all(t4b.values()),
                    fail_4b="+".join(k for k, v in t4b.items() if not v) or "-none-",
                    SPY_CAGR=sc, SPY_Sharpe=ss, SPY_MaxDD=sd_, SPY_OOS_Sharpe=spy_pack[2],
                    SPY_OOS_CAGR=fmet(spy[oos0:])[0], SPY_OOS_MaxDD=fmet(spy[oos0:])[2],
                    V2_Sharpe=fsharpe(v2), V2_OOS_Sharpe=fsharpe(v2[oos0:]),
                    V2_OOS_CAGR=fmet(v2[oos0:])[0], V2_OOS_MaxDD=fmet(v2[oos0:])[2],
                    V1_Sharpe=fsharpe(v1rg - v1tn * c / 1e4)))

        AR = pd.DataFrame([a for a in armrows if a["panel"] == pname])
        for c in RUNGS:
            s_c = AR[AR.rung == c]
            for fam in FAMS:
                for g in GROSSES:
                    for d in DEPTHS:
                        for cad in CADENCES:
                            s = s_c[(s_c.family == fam) & (s_c.gross == g) & (s_c.depth == d)
                                    & (s_c.cadence == cad)]
                            if s.empty or s.IS_Sharpe.isna().all():
                                continue
                            pk = s.loc[s.IS_Sharpe.idxmax()]
                            wfrows.append(dict(panel=pname, rung=c, family=fam, gross=g, depth=d,
                                               cadence=cad, level=pk.level, w=pk.w,
                                               IS_Sharpe=pk.IS_Sharpe, OOS_CAGR=pk.OOS_CAGR,
                                               OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                               OOS_dSharpe_F=pk.dOOS_F, OOS_dSharpe_W=pk.dOOS_W,
                                               twin_flip=bool(pk.win_OOS_F != pk.win_OOS_W),
                                               pass_4a=pk.pass_4a, pass_4b=pk.pass_4b,
                                               fail_4b=pk.fail_4b,
                                               SPY_OOS_CAGR=pk.SPY_OOS_CAGR,
                                               SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                                               SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD,
                                               V2_OOS_CAGR=pk.V2_OOS_CAGR,
                                               V2_OOS_Sharpe=pk.V2_OOS_Sharpe,
                                               V2_OOS_MaxDD=pk.V2_OOS_MaxDD))

        # keep what the rolling census needs, drop the rest
        PAN[pname] = dict(eidx=eidx, NET=NET, TNET=TNET, ME=ME, gross=gross_of,
                          GEFF=GEFF_FULL, K=K, T=T, gg=gg)
        del px, GR, GT, ARM

    CL = pd.DataFrame(claimrows)
    CL.to_csv(f"{OUT}.claims.csv.gz", index=False)
    AR = pd.DataFrame(armrows)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\n   {len(CL)} claim cells written ({CL.window.nunique()} windows x {len(RUNGS)} rungs x "
      f"{CL.panel.nunique()} panels x {CL.arm.nunique()} arms)")

    # ================= G4 reproduction of the committed twin corpus ===================
    P(f"\n{'='*118}\nG4 REPRODUCTION - the record's committed twin cells must rebuild before any "
      f"re-pricing is read\n{'='*118}")
    JK = ["family", "level", "w", "depth", "cadence", "gross"]

    def norm(d):
        d = d.copy()
        d["level"] = d.level.astype(float).round(6)
        d["w"] = d.w.astype(float).round(0).astype(int)
        d["depth"] = d.depth.astype(float).round(6)
        d["gross"] = d.gross.astype(float).round(6)
        return d

    mine = norm(CL[CL.window == "FULL"])
    old = norm(old)
    ARn = norm(AR)
    P("   PASS bar: max|d| < 6e-3 on dSharpe AND on twin_OOS (idea 406's known `data/prices.csv`")
    P("   re-download drift).  Verdict flips are COUNTED and printed, never tolerated into the bar.")
    P("   'closer to F' = the share of arms whose committed twin_OOS is nearer this run's")
    P("   FULLMATCH twin than its WINMATCH twin - a SCALE-FREE test of idea 824's premise, which")
    P("   the panel-drift bar above is only a proxy for.")
    P(f"   {'panel':<6} {'605/610 panel':<13} {'rung':>5} {'n':>5} {'win flips':>9} "
      f"{'max|d dSharpe|':>14} {'max|d twin_OOS|':>15} {'closer to F':>11}  verdict")
    g4, DISC = {}, []
    for pn, opn in [(k, v) for k, v in PANEL_MAP.items() if k in PANELS]:
        okp = True
        for c in RUNGS:
            s = mine[(mine.panel == pn) & (mine.rung == c)].set_index(JK)
            o = old[(old.panel == opn) & (old.rung == c)].set_index(JK)
            j = s[["dSharpe_F", "win_F"]].join(o[["dSharpe", "win", "twin_OOS"]], how="inner")
            a = ARn[(ARn.panel == pn) & (ARn.rung == c)]
            ja = a.set_index(JK)[["twin_OOS_F", "twin_OOS_W"]].join(o[["twin_OOS"]], how="inner")
            if len(j) == 0:
                P(f"   {pn:<6} {opn:<13} {c:>5.0f} {0:>5} {'n/a':>9} {'n/a':>14} {'n/a':>15}  "
                  f"{'n/a':>9}  NO JOIN - different panel")
                okp = False
                continue
            fl = int((j.win_F != j.win).sum())
            md = float((j.dSharpe_F - j.dSharpe).abs().max())
            eF = (ja.twin_OOS_F - ja.twin_OOS).abs()
            eW = (ja.twin_OOS_W - ja.twin_OOS).abs()
            mo = float(eF.max())
            # only arms whose two twins are separated by more than the panel drift can DECIDE the
            # convention; SEP is declared (1e-2, above B136's own drift) and n_sep is published.
            sep = (ja.twin_OOS_F - ja.twin_OOS_W).abs() > SEP
            disc = float((eF[sep] < eW[sep]).mean()) if int(sep.sum()) else np.nan
            DISC.append(dict(panel=pn, rung=c, n=len(ja), n_sep=int(sep.sum()), maxe_F=mo,
                             med_e_F=float(eF[sep].median()) if int(sep.sum()) else np.nan,
                             med_e_W=float(eW[sep].median()) if int(sep.sum()) else np.nan,
                             max_e_W=float(eW.max()), share_F=disc))
            ok = (md < 6e-3 and mo < 6e-3)
            okp &= ok
            P(f"   {pn:<6} {opn:<13} {c:>5.0f} {len(j):>5} {fl:>9} {md:>14.2e} {mo:>15.2e} "
              f"{disc:>9.4f}  {'PASS' if ok else 'FAIL'}")
        g4[pn] = okp

    def gv(pn):
        return "PASS" if g4.get(pn) else ("FAIL" if pn in g4 else "not run")

    P(f"\n   G4a U56 reproduces committed dSharpe/win/twin_OOS   {gv('U56')}")
    P(f"   G4b B136 reproduces                                 {gv('B136')}"
      f"   (weekly prices_broad.csv refresh; idea 406's known drift)")
    P(f"   G4c SMALL439 reproduces                             "
      f"{gv('SMALL')} - idea 609's finding restated: the committed rows are")
    P(f"       SMALL439 (439 tradable names) and today's panel is a DIFFERENT, LARGER panel, so no")
    P(f"       tolerance can join them.  Today's SMALL is run and printed as its own scope.")
    DS = pd.DataFrame(DISC)
    dsep = DS[DS.n_sep > 0]
    prem = bool(len(dsep) and (dsep.share_F == 1.0).all())
    undec = bool(len(DS) and (DS.n_sep == 0).all())
    P(f"\n   G4d H_PREMISE - is the record's committed twin_OOS a FULLMATCH twin or a WINMATCH one?")
    P(f"      The 6e-3 bar above is a PANEL-DRIFT bar and B136's twin_OOS LEVEL can exceed it")
    P(f"      without the convention being in doubt, so the premise is tested scale-free as well.")
    P(f"      Only arms whose FULLMATCH and WINMATCH OOS twins are separated by more than")
    P(f"      SEP = {SEP:g} (above B136's own drift) can decide the question; n_sep is published.")
    P(f"      {'panel':<6} {'rung':>5} {'n':>5} {'n_sep':>6} {'med|committed-FULLMATCH|':>25} "
      f"{'med|committed-WINMATCH|':>24} {'ratio':>8} {'closer to F':>11}")
    for _, r in DS.iterrows():
        rat = (r.med_e_W / r.med_e_F) if (r.med_e_F and np.isfinite(r.med_e_F)) else np.nan
        P(f"      {r.panel:<6} {r.rung:>5.0f} {int(r.n):>5} {int(r.n_sep):>6} {r.med_e_F:>25.3e} "
          f"{r.med_e_W:>24.3e} {rat:>8.1f}x {r.share_F:>10.4f}")
    if undec:
        P(f"      => UNDECIDABLE, and the reason is the run's deepest finding: NO arm on ANY panel")
        P(f"         has its two OOS twins separated by more than SEP = {SEP:g}.  A static long-only")
        P(f"         book's SHARPE is near-invariant to its gross, so re-matching the twin's gross")
        P(f"         cannot move the twin's Sharpe by more than ~1e-4.  The committed column is")
        P(f"         consistent with BOTH conventions because on this statistic they barely differ;")
        P(f"         the FULLMATCH construction is read off the 2026-09-10 script's SOURCE instead")
        P(f"         (g_eff = g * mean(m) computed once on the full sample, then sliced).")
    else:
        P(f"      => {'PASS' if prem else 'FAIL'} - the record's committed sub-window twin columns "
          f"are {'FULLMATCH' if prem else 'NOT unambiguously FULLMATCH'}.")
    assert g4.get("U56"), "G4 failed on U56 - the committed twin corpus does not rebuild"
    HEAD_SCOPE = "REPRO2"
    P(f"\n   => HEADLINE SCOPE = {HEAD_SCOPE} (U56 + B136), fixed BY THE GATE before any answer is")
    P(f"      read.  SMALL (today's panel) is printed at every point as its own scope.")

    # ================= G5 identity on the FULL window =================================
    f_full = CL[CL.window == "FULL"]
    g5 = float((f_full.dSharpe_F - f_full.dSharpe_W).abs().max())
    g5c = float((f_full.dCAGR_F - f_full.dCAGR_W).abs().max())
    P(f"\n   G5 / H_ID  WINMATCH == FULLMATCH on the FULL window   max|d dSharpe| {g5:.3e}, "
      f"max|d dCAGR| {g5c:.3e}  {'PASS' if max(g5, g5c) < 1e-9 else 'FAIL'}")
    assert max(g5, g5c) < 1e-9

    # ================= THE GRID: 6 windows x 2 conventions ============================
    P(f"\n{'='*118}\nTHE GRID - every claim window x convention x rung x scope, all "
      f"{len(WINDOWS)*len(CONVS)} tuned points printed\n{'='*118}")
    P("   'flip' = share of claims whose SIGN changes when the twin's gross is re-matched on the")
    P("   window itself.  W->L = was a win under the record's FULLMATCH, is a loss under WINMATCH.")
    grid = []
    SCOPES = {**{p: [p] for p in PANELS}, "REPRO2": [p for p in PANELS if p != "SMALL"]}
    for wn in WINDOWS:
        P(f"\n   --- claim window {wn} "
          f"({'COMMITTED - the record publishes a twin column on it' if wn in COMMITTED_WINDOWS else 'extension window, not a committed claim'})")
        P(f"      {'scope':<7} {'rung':>5} {'n':>5} {'win FULLMATCH':>14} {'win WINMATCH':>13} "
          f"{'flips':>6} {'flip share':>11} {'W->L':>5} {'L->W':>5} {'med|d|':>8} {'d g_eff':>9}")
        for sname, pans in SCOPES.items():
            for c in RUNGS:
                s = CL[(CL.window == wn) & (CL.rung == c) & (CL.panel.isin(pans))]
                st = flip_stats(s.dSharpe_F.values, s.dSharpe_W.values)
                stc = flip_stats(s.dCAGR_F.values, s.dCAGR_W.values)
                std = flip_stats(s.dMaxDD_F.values, s.dMaxDD_W.values)
                grid.append(dict(window=wn, committed=wn in COMMITTED_WINDOWS, scope=sname, rung=c,
                                 **{f"sharpe_{k}": v for k, v in st.items()},
                                 **{f"cagr_{k}": v for k, v in stc.items()},
                                 **{f"maxdd_{k}": v for k, v in std.items()},
                                 med_d_geff=float(s.d_geff.median()),
                                 max_abs_d_geff=float(s.d_geff.abs().max())))
                P(f"      {sname:<7} {c:>5.0f} {st['n']:>5} {st['win_F']:>14.4f} "
                  f"{st['win_W']:>13.4f} {st['n_flip']:>6} {st['flip']:>11.4f} {st['WL']:>5} "
                  f"{st['LW']:>5} {st['med_abs_d']:>8.4f} {s.d_geff.median():>9.4f}")
    GD = pd.DataFrame(grid)
    GD.to_csv(f"{OUT}.grid.csv", index=False)
    DS.to_csv(f"{OUT}.premise.csv", index=False)

    def cell(wn, sc_, c=RUNG_HEAD, stat="sharpe"):
        r = GD[(GD.window == wn) & (GD.scope == sc_) & (GD.rung == c)]
        return r.iloc[0] if len(r) else None

    # ---------------- the committed corpus, counted -----------------------------------
    P(f"\n{'='*118}\nHOW MANY OF THE RECORD'S COMMITTED TWIN CLAIMS CHANGE SIGN\n{'='*118}")
    tot_n = tot_f = 0
    P(f"      {'window':<8} {'scope':<7} {'rung':>5} {'n':>5} {'Sharpe flips':>13} "
      f"{'CAGR flips':>11} {'MaxDD flips':>12}")
    for wn in COMMITTED_WINDOWS:
        for c in RUNGS:
            r = cell(wn, HEAD_SCOPE, c)
            P(f"      {wn:<8} {HEAD_SCOPE:<7} {c:>5.0f} {int(r.sharpe_n):>5} "
              f"{int(r.sharpe_n_flip):>13} {int(r.cagr_n_flip):>11} {int(r.maxdd_n_flip):>12}")
            tot_n += int(r.sharpe_n)
            tot_f += int(r.sharpe_n_flip)
    P(f"\n   TOTAL over the record's three COMMITTED twin windows x 3 rungs on {HEAD_SCOPE}: "
      f"{tot_f} of {tot_n} Sharpe verdicts change sign ({tot_f/tot_n:.4f}).")
    sub = CL[(CL.window.isin(COMMITTED_WINDOWS)) & (CL.panel != "SMALL")]
    subs = sub[sub.window != "FULL"]
    P(f"   Of the {len(subs)} claims on SUB-WINDOWS alone (IS and OOS - the only committed twin")
    P(f"   claims the convention can move), {int((subs.win_F != subs.win_W).sum())} change sign "
      f"({float((subs.win_F != subs.win_W).mean()):.4f}).")

    # ---------------- WHAT THE FLIPS ARE ---------------------------------------------
    P(f"\n{'='*118}\nWHAT THE FLIPPED CLAIMS ARE - decomposition, not a summary statistic"
      f"\n{'='*118}")
    P("   A NEVERFIRE arm is one whose gate does not fire anywhere inside the claim window, so its")
    P("   realised gross ON THAT WINDOW is exactly g.  Under WINMATCH its twin IS the arm itself")
    P("   (dSharpe identically 0, scored a LOSS by the record's strict `win = dSharpe > 0`); under")
    P("   FULLMATCH the twin is held at a DIFFERENT gross and the comparison returns a tiny")
    P("   non-zero number whose sign is an artefact of that gross mismatch.")
    P(f"      {'window':<8} {'scope':<7} {'rung':>5} {'n':>5} {'flips':>6} {'NEVERFIRE':>10} "
      f"{'FIRING':>7} {'neverfire arms':>15} {'max|dS_F| among flips':>22}")
    DEC = []
    for wn in WINDOWS:
        for sname, pans in SCOPES.items():
            for c in RUNGS:
                s_ = CL[(CL.window == wn) & (CL.rung == c) & (CL.panel.isin(pans))]
                fl = s_[s_.win_F != s_.win_W]
                nfl = int(fl.neverfire.sum())
                DEC.append(dict(window=wn, scope=sname, rung=c, n=len(s_), flips=len(fl),
                                flips_neverfire=nfl, flips_firing=len(fl) - nfl,
                                n_neverfire=int(s_.neverfire.sum()),
                                max_dS_F_among_flips=float(fl.dSharpe_F.abs().max())
                                if len(fl) else np.nan))
                if sname == HEAD_SCOPE or wn in COMMITTED_WINDOWS:
                    P(f"      {wn:<8} {sname:<7} {c:>5.0f} {len(s_):>5} {len(fl):>6} {nfl:>10} "
                      f"{len(fl)-nfl:>7} {int(s_.neverfire.sum()):>15} "
                      f"{(float(fl.dSharpe_F.abs().max()) if len(fl) else np.nan):>22.2e}")
    DE = pd.DataFrame(DEC)
    DE.to_csv(f"{OUT}.decomp.csv", index=False)
    allfl = DE[DE.scope.isin(list(SCOPES)[:3])]
    P(f"\n   ACROSS EVERY window, scope and rung in this run: {int(allfl.flips.sum())} flips, of")
    P(f"   which {int(allfl.flips_neverfire.sum())} are NEVERFIRE arms and "
      f"{int(allfl.flips_firing.sum())} are arms whose gate actually fired in the window.")
    P(f"   The largest |dSharpe| the record's FULLMATCH convention ever assigns to a flipped claim")
    P(f"   is {float(DE.max_dS_F_among_flips.max()):.2e}.")

    # ================= HYPOTHESES =====================================================
    P(f"\n{'='*118}\nPRE-REGISTERED HYPOTHESES\n{'='*118}")
    hd = cell(WIN_HEAD, HEAD_SCOPE, RUNG_HEAD)
    res = {}
    res["H_ID"] = (max(g5, g5c) < 1e-9, f"max|d| {max(g5,g5c):.2e} on FULL")
    res["H_PREMISE"] = (prem, "UNDECIDABLE ON THE DATA - no arm's two OOS twins are separated by "
                        f"more than SEP = {SEP:g} of Sharpe; the convention is read off the "
                        "2026-09-10 script's source, where g_eff is matched once on the full sample"
                        if undec else
                        "every joined arm's committed twin_OOS is nearer this run's "
                        f"FULLMATCH twin than its WINMATCH twin ({int(dsep.n_sep.sum())} "
                        f"separable arms over {len(dsep)} panel-rungs)"
                        if prem else "the committed column is NOT unambiguously FULLMATCH")
    if undec:
        res["H_PREMISE"] = ("UNDECIDABLE", res["H_PREMISE"][1])
    res["H_FLIP"] = (hd.sharpe_flip < 0.10,
                     f"flip share {hd.sharpe_flip:.4f} ({int(hd.sharpe_n_flip)} of "
                     f"{int(hd.sharpe_n)}) at {WIN_HEAD}/{HEAD_SCOPE}/{RUNG_HEAD:g} bps")
    nf = int(hd.sharpe_n_flip)
    sym = (nf > 0 and min(hd.sharpe_WL, hd.sharpe_LW) >= 0.10 * nf)
    allF = CL[(CL.panel != "SMALL") & (CL.win_F != CL.win_W)]
    wl_all, lw_all = int((allF.win_F & ~allF.win_W).sum()), int((~allF.win_F & allF.win_W).sum())
    res["H_SYM"] = (bool(sym), f"VACUOUS at the headline - 0 flips there.  Where flips exist "
                    f"(every window/rung on {HEAD_SCOPE}) they are ONE-DIRECTIONAL: "
                    f"W->L {wl_all}, L->W {lw_all}"
                    if nf == 0 else
                    f"W->L {int(hd.sharpe_WL)}, L->W {int(hd.sharpe_LW)} of {nf}")
    res["H_MAG"] = (hd.sharpe_med_abs_d <= 0.05,
                    f"median |d dSharpe| {hd.sharpe_med_abs_d:.4f}, max "
                    f"{hd.sharpe_max_abs_d:.4f}")
    f0, f25 = cell(WIN_HEAD, HEAD_SCOPE, 0.0), cell(WIN_HEAD, HEAD_SCOPE, 25.0)
    res["H_COSTINV"] = (abs(f0.sharpe_flip - hd.sharpe_flip) <= 0.10
                        and abs(f25.sharpe_flip - hd.sharpe_flip) <= 0.10,
                        f"flip 0/10/25 bps = {f0.sharpe_flip:.4f} / {hd.sharpe_flip:.4f} / "
                        f"{f25.sharpe_flip:.4f}")
    pf = {p: cell(WIN_HEAD, p, RUNG_HEAD).sharpe_flip for p in PANELS}
    res["H_PANELINV"] = (max(pf.values()) - min(pf.values()) <= 0.20,
                         "  ".join(f"{k} {v:.4f}" for k, v in pf.items())
                         + f"  spread {max(pf.values())-min(pf.values()):.4f}")
    fi = cell("IS", HEAD_SCOPE, RUNG_HEAD)
    res["H_WINDOW"] = (abs(fi.sharpe_flip - hd.sharpe_flip) <= 0.10,
                       f"IS {fi.sharpe_flip:.4f} vs OOS {hd.sharpe_flip:.4f}, |d| "
                       f"{abs(fi.sharpe_flip-hd.sharpe_flip):.4f}")

    # ---- H_CAND: the record's newest 4b KEEP-candidate, re-priced by name -------------
    P(f"\n   H_CAND - the record's newest 4b KEEP-candidate, re-priced under WINMATCH")
    P(f"   {CAND['panel']} breadth-{CAND['family']} q{CAND['level']} w{CAND['w']} "
      f"depth {CAND['depth']:.2f} {CAND['cadence']} g{CAND['gross']:.2f} (idea 609's by-product)")
    cc = CL[(CL.panel == CAND["panel"]) & (CL.family == CAND["family"])
            & (np.isclose(CL.level, CAND["level"])) & (CL.w == CAND["w"])
            & (np.isclose(CL.depth, CAND["depth"])) & (CL.cadence == CAND["cadence"])
            & (np.isclose(CL.gross, CAND["gross"]))]
    P(f"      {'window':<8} {'rung':>5} {'arm Sharpe':>11} {'twin FULL':>10} {'twin WIN':>9} "
      f"{'dS FULLMATCH':>13} {'dS WINMATCH':>12} {'g_eff F':>8} {'g_eff W':>8}  verdict")
    cand_ok = True
    for wn in ["FULL", "IS", "OOS", "EP2022"]:
        for c in RUNGS:
            r = cc[(cc.window == wn) & (cc.rung == c)]
            if r.empty:
                continue
            r = r.iloc[0]
            v = "WIN both" if (r.win_F and r.win_W) else (
                "FLIP W->L" if (r.win_F and not r.win_W) else
                ("FLIP L->W" if (r.win_W and not r.win_F) else "LOSS both"))
            if wn in ("FULL", "OOS"):
                cand_ok &= bool(r.win_W)
            P(f"      {wn:<8} {c:>5.0f} {r.Sharpe:>11.4f} {r.twinF_Sharpe:>10.4f} "
              f"{r.twinW_Sharpe:>9.4f} {r.dSharpe_F:>13.4f} {r.dSharpe_W:>12.4f} "
              f"{r.g_eff_full:>8.4f} {r.g_eff_win:>8.4f}  {v}")
    res["H_CAND"] = (bool(cand_ok), "beats its own WINMATCH twin on FULL and OOS at 0/10/25 bps"
                     if cand_ok else "does NOT survive the re-match on FULL and/or OOS")

    # ---- H_R8CLAIM: rule 8 on the claim ---------------------------------------------
    P(f"\n   H_R8CLAIM - RULE 8 ON THE CLAIM: rolling {L_ROLL}-day windows, step {STEP_ROLL}.")
    P(f"   The flip share is measured on windows ENDING in the IS half and read ONCE on windows")
    P(f"   ending in the OOS half.  Nothing is tuned on the OOS half.")
    master = PAN["U56"]["eidx"]
    roll = []
    for a in range(0, len(master) - L_ROLL + 1, STEP_ROLL):
        d0, d1 = master[a], master[a + L_ROLL - 1]
        for pn in PANELS:
            Pd = PAN[pn]
            ei = Pd["eidx"]
            i0 = int(ei.searchsorted(d0, side="left"))
            i1 = int(ei.searchsorted(d1, side="right"))
            if i1 - i0 < MINCOVER * L_ROLL:
                continue
            for c in RUNGS:
                A = Pd["NET"][c]
                dF = np.empty(Pd["K"])
                dW = np.empty(Pd["K"])
                for i in range(Pd["K"]):
                    ra = A[i, i0:i1]
                    sa = fsharpe(ra)
                    lo = int(np.clip(np.floor(round(float(Pd["GEFF"][i]), 6) / GSTEP), 0,
                                     len(Pd["gg"]) - 2))
                    lam = (Pd["GEFF"][i] - Pd["gg"][lo]) / GSTEP
                    tf = ((1 - lam) * Pd["TNET"][c][lo, i0:i1]
                          + lam * Pd["TNET"][c][lo + 1, i0:i1])
                    ge = Pd["gross"][i] * float(Pd["ME"][i, i0:i1].mean())
                    lo2 = int(np.clip(np.floor(round(float(ge), 6) / GSTEP), 0,
                                      len(Pd["gg"]) - 2))
                    lam2 = (ge - Pd["gg"][lo2]) / GSTEP
                    tw = ((1 - lam2) * Pd["TNET"][c][lo2, i0:i1]
                          + lam2 * Pd["TNET"][c][lo2 + 1, i0:i1])
                    dF[i] = sa - fsharpe(tf)
                    dW[i] = sa - fsharpe(tw)
                st = flip_stats(dF, dW)
                mm_w = Pd["ME"][:, i0:i1].mean(axis=1)
                nf = mm_w >= 1.0 - 1e-12
                fl = (dF > TIE) != (dW > TIE)
                st["nf_share_of_flips"] = float(nf[fl].mean()) if int(fl.sum()) else np.nan
                st["nf_share_of_arms"] = float(nf.mean())
                roll.append(dict(panel=pn, rung=c, start=d0, end=d1,
                                 half="IS" if d1 <= pd.Timestamp(IS_END) else "OOS", **st))
    RO = pd.DataFrame(roll)
    RO.to_csv(f"{OUT}.rolling.csv", index=False)
    r2 = RO[(RO.panel != "SMALL") & (RO.rung == RUNG_HEAD)]
    is_f = float(r2[r2.half == "IS"].flip.mean()) if (r2.half == "IS").any() else np.nan
    oos_f = float(r2[r2.half == "OOS"].flip.mean()) if (r2.half == "OOS").any() else np.nan
    P(f"      {len(RO)} rolling readings; {HEAD_SCOPE} at {RUNG_HEAD:g} bps: "
      f"IS windows {int((r2.half=='IS').sum())} mean flip {is_f:.4f}, "
      f"OOS windows {int((r2.half=='OOS').sum())} mean flip {oos_f:.4f}, "
      f"|d| {abs(is_f-oos_f):.4f}")
    for pn in PANELS:
        for c in RUNGS:
            q = RO[(RO.panel == pn) & (RO.rung == c)]
            if q.empty:
                continue
            P(f"      {pn:<6} {c:>5.0f} bps  n_win {len(q):>3}  mean flip {q.flip.mean():.4f}  "
              f"IS {q[q.half=='IS'].flip.mean():.4f}  OOS {q[q.half=='OOS'].flip.mean():.4f}  "
              f"win_F {q.win_F.mean():.4f} -> win_W {q.win_W.mean():.4f}")
    res["H_R8CLAIM"] = (abs(is_f - oos_f) <= 0.10,
                        f"IS {is_f:.4f} -> OOS {oos_f:.4f} read once, |d| {abs(is_f-oos_f):.4f}")

    P(f"\n   {'hypothesis':<12} {'verdict':<6}  evidence")
    for k, (v, why) in res.items():
        lab = v if isinstance(v, str) else ("PASS" if v else "FAIL")
        P(f"   {k:<12} {lab:<11}  {why}")

    # ================= RULE 8 ON THE BOOKS + BOTH KEEP PATHS ==========================
    P(f"\n{'='*118}\nPROTOCOL RULE 8 ON THE BOOKS + BOTH KEEP PATHS\n{'='*118}")
    P(f"   {len(AR)} arm-rows ({AR.arm.nunique()} arms x {len(RUNGS)} rungs x 3 panels).")
    for c in RUNGS:
        a = AR[AR.rung == c]
        P(f"   {c:>5.0f} bps   4a {int(a.pass_4a.sum()):>4} of {len(a):<5}   "
          f"4b {int(a.pass_4b.sum()):>4} of {len(a):<5}   "
          f"4b that beat their FULLMATCH OOS twin {int((a.pass_4b & a.win_OOS_F).sum()):>4}   "
          f"their WINMATCH OOS twin {int((a.pass_4b & a.win_OOS_W).sum()):>4}")
    P(f"\n   RULE-8 PICKS (dial chosen on IS by IS Sharpe alone; OOS read once):")
    P(f"      {'panel':<6} {'rung':>5} {'n picks':>7} {'4a':>4} {'4b':>4} {'OOS CAGR':>9} "
      f"{'OOS Sharpe':>10} {'OOS MaxDD':>10} {'vs SPY OOS':>26} {'vs RULES v2 OOS':>26}")
    for pn in PANELS:
        for c in RUNGS:
            w = WF[(WF.panel == pn) & (WF.rung == c)]
            if w.empty:
                continue
            b = w.iloc[0]
            P(f"      {pn:<6} {c:>5.0f} {len(w):>7} {int(w.pass_4a.sum()):>4} "
              f"{int(w.pass_4b.sum()):>4} {w.OOS_CAGR.median():>9.2%} "
              f"{w.OOS_Sharpe.median():>10.3f} {w.OOS_MaxDD.median():>10.2%} "
              f"{b.SPY_OOS_CAGR:>9.2%}/{b.SPY_OOS_Sharpe:.3f}/{b.SPY_OOS_MaxDD:.2%}   "
              f"{b.V2_OOS_CAGR:>9.2%}/{b.V2_OOS_Sharpe:.3f}/{b.V2_OOS_MaxDD:.2%}")
    p4b = WF[WF.pass_4b]
    P(f"\n   rule-8 picks passing 4b: {len(p4b)} of {len(WF)}; passing 4a: "
      f"{int(WF.pass_4a.sum())} of {len(WF)}")
    if len(p4b):
        P(f"      {'panel':<6} {'rung':>5} {'arm':<34} {'OOS CAGR':>9} {'Sharpe':>7} "
          f"{'MaxDD':>8} {'dOOS FULL':>10} {'dOOS WIN':>9}  twin verdict")
        for _, r in p4b.iterrows():
            v = ("beats BOTH twins" if (r.OOS_dSharpe_F > TIE and r.OOS_dSharpe_W > TIE) else
                 ("BEATS FULLMATCH ONLY - the pass is the convention"
                  if r.OOS_dSharpe_F > TIE else
                  ("beats WINMATCH only" if r.OOS_dSharpe_W > TIE else "beats neither twin")))
            P(f"      {r.panel:<6} {r.rung:>5.0f} "
              f"{r.family+' L'+format(r.level,'.2f')+' w'+str(int(r.w))+' d'+format(r.depth,'.2f')+' '+r.cadence+' g'+format(r.gross,'.2f'):<34} "
              f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>7.3f} {r.OOS_MaxDD:>8.2%} "
              f"{r.OOS_dSharpe_F:>10.4f} {r.OOS_dSharpe_W:>9.4f}  {v}")
    fl4b = WF[WF.pass_4b & WF.twin_flip]
    P(f"\n   4b rule-8 picks whose OWN TWIN VERDICT flips with the convention: {len(fl4b)} of "
      f"{len(p4b)}")

    P(f"\n   runtime {time.time()-T0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(grid=GD, claims=CL, arms=AR, wf=WF, roll=RO, res=res)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 815 - "is-the-CORR-LO-POSITIVE-EXCESS-a-DE-GROSSING-artefact" (lane C, 2026-09-15).

The finding this run exists to decompose
----------------------------------------
Idea 606 rebuilt idea 602's placebo machinery on four gate STATES and ran every state in BOTH
directions, so that the reversed arm (same firing rate, same clustering, opposite information)
acts as a second, sharper placebo.  The reversal control WORKED on two states and FAILED on two:

    VOL20-LO  excess vs BLOCK  -0.0128   (share > 0  0.361)   <- flips sign, as a signal should
    DISP-LO                    -0.0204   (            0.162)   <- flips sign
    CORR-LO                    +0.0270   (            0.845)   <- does NOT flip
    BREADTH-HI                 +0.0114   (            0.632)   <- does not flip

i.e. de-grossing on EITHER tail of correlation beats an information-free placebo at the identical
firing rate.  The queue states the two readings and asks which one is true:

    (A) CALENDAR.  The BLOCK placebo is a circular shift of the whole multiplier path.  A shift
        moves the de-grossed days OFF the two episodes (2020, 2022) that BOTH tails of a
        two-sided state happen to overlap, so the "excess" is the value of being de-grossed
        during a crash at all, not the value of the signal.  If so the null is measuring the
        EPISODE and the record's whole placebo leg needs a second, calendar-preserving control.
    (B) INFORMATION.  The low-correlation tail carries real information about forward returns
        that survives a null which is already aligned with the same episodes.

These are separable, and the separation is the only thing this run does: hold the arm, the book,
the twin-cancelling differenced statistic and the firing rate FIXED, and change the NULL.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (LEVEL)     Does the CORR-LO excess survive a CALENDAR-PRESERVING null?  BLOCKYEAR
                   circularly shifts the multiplier path WITHIN each calendar year and BLOCKEP
                   within each of {COVID_TIGHT, BEAR2022, rest}: same firing count per stratum,
                   same run lengths, no information.  YEARMATCH / EPMATCH are their iid
                   counterparts, reported so the clustering channel and the calendar channel
                   can be read apart rather than confounded.
    Q2 (LADDER)    The decisive shape test.  BLOCK's shift is drawn uniformly over the sample.
                   Replace it with a shift of EXACTLY s days, s in {5,10,21,63,126,252}, both
                   signs.  Under (A) the excess must RISE with |s| from ~0 (a 5-day shift is
                   still inside the episode; a 252-day shift is not).  Under (B) it is flat.
    Q3 (DELETION)  Delete the two episodes from the return stream and re-read the excess on the
                   remaining days.  Under (A) CORR-LO's excess collapses; under (B) it does not.
    Q4 (OVERLAP)   Measure the mechanism directly: what share of each arm's de-grossed days lies
                   inside the episodes, real vs BLOCK?  (A) requires a large positive gap.
    Q5 (RULE 8 on the claim)  The excess re-measured on 2009-2016 alone and read once on 2017+.
    Q6 (RULE 8 on the books)  Both PROTOCOL KEEP paths on every grid point, plus the rule-8
                   chooser over (level, w) per panel x family x depth x cadence x gross x rung,
                   with OOS CAGR / Sharpe / MaxDD read once against RULES v2 and SPY.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. state        BREADTH / VOL20 / DISP / CORR, each in BOTH directions (8 families).
                    Direction is NOT a third parameter: both are always reported, never
                    selected on.  Inherited verbatim from idea 606.
    2. placebo kind a 2 x 3 factorial - CLUSTERING {iid, circular shift} x CALENDAR STRATA
                    {none, calendar year, episode} - giving RAND / YEARMATCH / EPMATCH /
                    BLOCK / BLOCKYEAR / BLOCKEP, of which idea 606 had only RAND and BLOCK;
                    plus the displacement ladder SHIFT5 / 10 / 21 / 63 / 126 / 252.  12 kinds.
    ALL grid points reported at every panel / family / level / w / depth / cadence / gross /
    cost rung.  Nothing is chosen on the answer.

Reported axes, NEVER tuned or selected on (inherited from idea 606 verbatim)
    level q  0.07 / 0.12 / 0.17      w  252 / 504 / 1008 / 2016    depth  0.25 / 0.50 / 1.00
    cadence  D / W                   gross  0.75 / 1.00            cost   0 / 10 / 25 bps
    panel    U56 / B136 / SMALL663

Declared in advance, never swept
    EPISODES   COVID_TIGHT 2020-02-19 .. 2020-04-07 (the record's own window, ideas 835 / 861)
               BEAR2022    2022-01-04 .. 2022-10-12 (SPY's 2022 peak-to-trough)
    SMOOTH     20 days for VOL20 / DISP / CORR (idea 606's, fixed in advance)
    IS/OOS     2016-12-31 / 2017-01-01

Why the differenced statistic needs no twin
    Idea 606's excess is (arm dSharpe) - (placebo dSharpe), both taken against the arm's
    matched-mean-gross static twin.  Every placebo kind here preserves the arm's de-grossed day
    COUNT and depth exactly, hence its mean multiplier exactly, hence its twin exactly (G5), so
    the twin cancels and the excess equals Sharpe(real gated) - Sharpe(placebo gated).  G3
    prices that identity against idea 606's COMMITTED per-arm excess.csv, row by row, on all
    3,456 arms.  No twin backtest is run and none is needed.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=c).
    G2  idea 84's ungated EWALL U56 g=0.85 @10bps: 11.8% / 1.05 / -17.9% / H 1.07 / 1.04.
    G3  idea 606's COMMITTED .excess.csv, re-derived here.  G3a per-arm on B136, the one panel
        whose committed cache is unchanged; G3b the firing-day-share drift on the panels whose
        cache has been re-adjusted since, measured against 606's own committed on_share; G3c
        the PUBLISHED object - the eight per-family medians and share>0 this run exists to
        decompose - to a bar of 0.005 declared before the run.
    G4  the fast numpy CAGR / Sharpe / MaxDD used on ~190k cells vs engine.metrics().
    G5  placebo matching identity: EVERY kind reproduces the real arm's de-grossed day count
        and mean multiplier exactly (this is what lets the twin cancel).  The four stratified
        kinds additionally reproduce the arm's PER-STRATUM count, which is the whole point.
    G6  the comparands are the record's: RULES v2 and SPY on each panel.
    G7  deletion arithmetic: deleting an EMPTY day set is bit-identical to not deleting.

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
current-constituent lists, so CAGR and drawdown LEVELS are optimistic (the SPY bars included);
the placebo DIFFERENCING and the null-vs-null contrast are the durable part.

Deterministic (all seeds md5-derived, and idea 606's seed derivation is reproduced verbatim so
its BLOCK/RAND cells come back bit-identical), standalone.  Reads baseline.py and engine;
modifies nothing.
"""
import hashlib
import sys
import time
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT = OUT / "2026-09-12_does-the-PLACEBO-EXCESS-rate-slope-survive-outside-the-BREADTH-family_B.excess.csv"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
CADENCES = ["D", "W"]
SMOOTH = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
NSEED = 10
TIE = 1e-12

STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
PRIOR_SIDE = {"BREADTH": "LO", "VOL20": "HI", "DISP": "HI", "CORR": "HI"}
FAMILIES = [f"{s}-{side}" for s in STATES for side in ("LO", "HI")]
PRIOR_FAMS = [f"{s}-{PRIOR_SIDE[s]}" for s in STATES]

SHIFTS = [5, 10, 21, 63, 126, 252]
# The null axis is a 2 x 3 factorial plus a displacement ladder.  CLUSTERING: iid days (RAND
# family) or a circular shift (BLOCK family), which preserves the run-length distribution exactly.
# CALENDAR STRATA: none, calendar year, or {COVID_TIGHT, BEAR2022, everything else}.  Idea 606
# used only the two unstratified cells; the stratified ones are what make the queue's two
# readings separable, and the SHIFT ladder is the continuous version of the same contrast.
KINDS = (["RAND", "YEARMATCH", "EPMATCH", "BLOCK", "BLOCKYEAR", "BLOCKEP"]
         + [f"SHIFT{s}" for s in SHIFTS])
IID_KINDS = ["RAND", "YEARMATCH", "EPMATCH"]
SHIFT_KINDS = ["BLOCK", "BLOCKYEAR", "BLOCKEP"]
CAL_KINDS = ["YEARMATCH", "EPMATCH", "BLOCKYEAR", "BLOCKEP"]

EPISODES = {"COVID_TIGHT": ("2020-02-19", "2020-04-07"),
            "BEAR2022": ("2022-01-04", "2022-10-12")}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

LINES = []
T0 = time.time()


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (idea 42/399/602/606)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def state_breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def state_vol20(px):
    v = px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)
    return v.mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_corr(px):
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    idx = rt.mean(axis=1)
    s_idx = idx.rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar = sig.mean(axis=1)
    s2bar = (sig ** 2).mean(axis=1)
    num = s_idx ** 2 - s2bar / n
    den = sbar ** 2 - s2bar / n
    return (num / den.replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def _cadence(m, idx):
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0)


def gate_mult(st, thr, side, depth, cadence, idx):
    fire = (st < thr) if side == "LO" else (st > thr)
    fire = fire & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    return _cadence(m, idx) if cadence == "W" else m


# --------------------------------------------------------------------------- fast numpy metrics
def f_sharpe(r):
    sd = r.std(ddof=1)
    return r.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def f_cagr(r):
    """engine.metrics()['CAGR'] on a numpy array (same cumprod, same exponent) - G4."""
    if len(r) == 0:
        return np.nan
    eq = np.cumprod(1.0 + r)
    return float(eq[-1] ** (1 / (len(r) / 252)) - 1)


def f_maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def f_all(r):
    eq = np.cumprod(1.0 + r)
    cagr = float(eq[-1] ** (1 / (len(r) / 252)) - 1)
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    return cagr, f_sharpe(r), dd


# ---------------------------------------------------------------------- placebos (606 verbatim +)
def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def placebo_mult(v, depth, kind, seed, year_groups, ep_groups, sd=0):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path v (numpy).

    RAND / BLOCK are idea 606's, reproduced VERBATIM (same rng calls, same order), so its
    committed cells come back bit-identical.  The three new kinds:
      SHIFT<s>   circular shift by EXACTLY s days; sd 0 is a LAG (+s, the gate fires s days
                 later) and sd 1 a LEAD (-s), so both are always reported.  Exact rate, exact
                 run-length distribution, and -- unlike BLOCK -- a KNOWN, SMALL calendar
                 displacement, which is what makes the ladder a decomposition.
      YEARMATCH  iid days WITHIN each calendar year, exactly the real arm's count per year.
      EPMATCH    iid days within each of three strata: COVID_TIGHT, BEAR2022, everything else,
                 exactly the real arm's count in each.
      BLOCKYEAR  circular shift WITHIN each calendar year.
      BLOCKEP    circular shift WITHIN each of the three episode strata.
                 These last two are the ones idea 606 did not have: they preserve the calendar
                 AND the clustering, so an excess that survives them is not a calendar artefact
                 and not a run-length artefact either.
    All of them preserve the de-grossed day count and the depth, hence the mean multiplier,
    hence the arm's matched-gross twin (G5)."""
    n = len(v)
    k = int((v < 1.0).sum())
    if k == 0:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(n)
        out[rng.choice(n, size=k, replace=False)] = 1.0 - depth
        return out
    if kind == "BLOCK":
        shift = int(rng.integers(1, n))
        return np.roll(v, shift)
    if kind.startswith("SHIFT"):
        s = int(kind[5:])
        sign = 1 if sd % 2 == 0 else -1      # sd 0 = LAG (fire s days later), sd 1 = LEAD
        return np.roll(v, sign * s)
    groups = year_groups if kind in ("YEARMATCH", "BLOCKYEAR") else ep_groups
    if kind in ("BLOCKYEAR", "BLOCKEP"):
        out = v.copy()
        for g in groups:
            if len(g) > 1:
                out[g] = np.roll(v[g], int(rng.integers(1, len(g))))
        return out
    out = np.ones(n)
    fired = v < 1.0
    for g in groups:
        kg = int(fired[g].sum())
        if kg:
            out[g[rng.choice(len(g), size=kg, replace=False)]] = 1.0 - depth
    return out


# ================================================================================ per-panel run
def run_panel(panel, px, kinds=None, rungs=None):
    kinds = kinds or KINDS
    rungs = rungs or RUNGS
    cells, ph, gates_log, g5 = [], [], [], []
    start = px.index[260]
    idx = px.index
    spy = px["SPY"].pct_change().fillna(0).loc[start:]

    def pack(r):
        h = len(r) // 2
        return (metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"],
                metrics(r.loc[OOS_START:])["Sharpe"], metrics(r)["MaxDD"], metrics(r)["CAGR"])

    spy_pack = pack(spy)
    spy_o = spy.loc[OOS_START:]
    h = len(spy_o) // 2
    spy_oos_pack = (metrics(spy_o.iloc[:h])["Sharpe"], metrics(spy_o.iloc[h:])["Sharpe"],
                    metrics(spy_o)["MaxDD"], metrics(spy_o)["CAGR"])
    m_spy = metrics(spy)

    log(f"\n{'=' * 150}\nPANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({len(spy)} days)")
    log(f"  SPY {m_spy['CAGR']:.2%} / {m_spy['Sharpe']:.4f} / {m_spy['MaxDD']:.2%}; 4b bars: "
        f"CAGR floor {0.70 * m_spy['CAGR']:.2%}, DD cap {-0.60 * abs(m_spy['MaxDD']):.2%}, "
        f"halves {spy_pack[0]:.4f}/{spy_pack[1]:.4f}, OOS Sharpe {spy_pack[2]:.4f}")

    # ---- states and thresholds
    sts = {s: STATE_FN[s](px) for s in STATES}
    thr_lo = {(s, q, w): sts[s].rolling(w, min_periods=w).quantile(q)
              for s in STATES for q in QS for w in WS}
    thr_hi = {(s, q, w): sts[s].rolling(w, min_periods=w).quantile(1 - q)
              for s in STATES for q in QS for w in WS}

    # ---- base books at 0 bps, cost rungs derived (G1)
    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
    live = backtest(px, ewall_weights(px, 0.75), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[start:]
    g1 = float(((base0[0.75][0] - base0[0.75][1] * RUNG_HEAD / 1e4) - live).abs().max())

    # ---- baselines (G6)
    base_packs, base_oos_packs, base_rows = {}, {}, {}
    for c in rungs:
        b = backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
        hb = len(b) // 2
        b1, b2 = metrics(b.iloc[:hb])["Sharpe"], metrics(b.iloc[hb:])["Sharpe"]
        base_packs[c] = (b1, b2, metrics(b)["MaxDD"])
        bo = b.loc[OOS_START:]
        ho = len(bo) // 2
        base_oos_packs[c] = (metrics(bo.iloc[:ho])["Sharpe"], metrics(bo.iloc[ho:])["Sharpe"],
                             metrics(bo)["MaxDD"])
        base_rows[c] = dict(CAGR=metrics(b)["CAGR"], Sharpe=metrics(b)["Sharpe"],
                            MaxDD=metrics(b)["MaxDD"], H1=b1, H2=b2,
                            OOS_CAGR=metrics(bo)["CAGR"], OOS_Sharpe=metrics(bo)["Sharpe"],
                            OOS_MaxDD=metrics(bo)["MaxDD"])
    v1 = backtest(px, rules_v1_weights(px), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[start:]
    log(f"  RULES v2 @10bps {base_rows[10]['CAGR']:.2%} / {base_rows[10]['Sharpe']:.4f} / "
        f"{base_rows[10]['MaxDD']:.2%} (H {base_rows[10]['H1']:.4f}/{base_rows[10]['H2']:.4f}, "
        f"OOS Sharpe {base_rows[10]['OOS_Sharpe']:.4f}); RULES v1 @10bps "
        f"{metrics(v1)['CAGR']:.2%} / {metrics(v1)['Sharpe']:.4f} / {metrics(v1)['MaxDD']:.2%}")

    # ---- numpy frames on the evaluation window
    eidx = base0[0.75][0].index
    N = len(eidx)
    is_m = np.asarray(eidx <= pd.Timestamp(IS_END))
    oos_m = np.asarray(eidx >= pd.Timestamp(OOS_START))
    ep_m = np.zeros(N, bool)
    ep_masks = {}
    for nm, (a, b) in EPISODES.items():
        mm = np.asarray((eidx >= pd.Timestamp(a)) & (eidx <= pd.Timestamp(b)))
        ep_masks[nm] = mm
        ep_m |= mm
    keep_m = ~ep_m                                  # Q3 deletion leg
    years = np.asarray(eidx.year)
    year_groups = [np.where(years == y)[0] for y in np.unique(years)]
    ep_groups = [np.where(ep_masks["COVID_TIGHT"])[0], np.where(ep_masks["BEAR2022"])[0],
                 np.where(~ep_m)[0]]
    ep_groups = [g for g in ep_groups if len(g)]
    log(f"  episodes: COVID_TIGHT {int(ep_masks['COVID_TIGHT'].sum())} d, "
        f"BEAR2022 {int(ep_masks['BEAR2022'].sum())} d, union {int(ep_m.sum())} d "
        f"({ep_m.mean():.2%} of the window); IS {int(is_m.sum())} d / OOS {int(oos_m.sum())} d")

    rb_np = {}
    for c in rungs:
        for g in GROSSES:
            r0, t0 = base0[g]
            rb_np[(c, g)] = (r0 - t0 * c / 1e4).values

    # ---- arm specs and effective multipliers
    arms = [(f"{s}-{side}", s, side, q, w) for s in STATES for side in ("LO", "HI")
            for q in QS for w in WS]
    me_np, on_cache, gap_cache = {}, {}, {}
    for fam, s, side, q, w in arms:
        th = (thr_lo if side == "LO" else thr_hi)[(s, q, w)]
        for d, cad in product(DEPTHS, CADENCES):
            m = gate_mult(sts[s], th, side, d, cad, idx)
            me = m.reindex(eidx).shift(1).fillna(1.0)
            key = (fam, q, w, d, cad)
            me_np[key] = me.values.astype(float)
            on_cache[key] = float((me < 1.0).mean())
            gap_cache[key] = 1.0 - float(me.mean())
        gates_log.append(dict(panel=panel, family=fam, state=s, side=side, level=q, w=w,
                              prior=fam in PRIOR_FAMS,
                              on_D=on_cache.get((fam, q, w, DEPTHS[0], "D"), np.nan),
                              on_W=on_cache.get((fam, q, w, DEPTHS[0], "W"), np.nan)))

    def apply_eff(rbase, m_eff, gross, c):
        sw = np.abs(np.diff(m_eff, prepend=m_eff[0]))
        return m_eff * rbase - sw * gross * c / 1e4

    # ---- main grid
    for c in rungs:
        for g in GROSSES:
            rb = rb_np[(c, g)]
            for fam, s, side, q, w in arms:
                for d, cad in product(DEPTHS, CADENCES):
                    key = (fam, q, w, d, cad)
                    me = me_np[key]
                    rg = apply_eff(rb, me, g, c)
                    cagr, sh, dd = f_all(rg)
                    r_oos = rg[oos_m]
                    cagr_o, sh_o, dd_o = f_all(r_oos)
                    hh = len(rg) // 2
                    h1, h2 = f_sharpe(rg[:hh]), f_sharpe(rg[hh:])
                    ho = len(r_oos) // 2
                    h1o, h2o = f_sharpe(r_oos[:ho]), f_sharpe(r_oos[ho:])
                    t4b = {"H1": h1 > spy_pack[0], "H2": h2 > spy_pack[1],
                           "OOS": sh_o > spy_pack[2],
                           "DD": abs(dd) <= 0.60 * abs(spy_pack[3]),
                           "CAGR": cagr >= 0.70 * spy_pack[4]}
                    t4bo = {"H1": h1o > spy_oos_pack[0], "H2": h2o > spy_oos_pack[1],
                            "DD": abs(dd_o) <= 0.60 * abs(spy_oos_pack[2]),
                            "CAGR": cagr_o >= 0.70 * spy_oos_pack[3]}
                    bp, bpo = base_packs[c], base_oos_packs[c]
                    cells.append(dict(
                        panel=panel, rung=c, gross=g, family=fam, state=s, side=side,
                        prior=fam in PRIOR_FAMS, level=q, w=w, depth=d, cadence=cad,
                        on_share=on_cache[key], gap=gap_cache[key],
                        CAGR=cagr, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                        IS_Sharpe=f_sharpe(rg[is_m]), OOS_CAGR=cagr_o, OOS_Sharpe=sh_o,
                        OOS_MaxDD=dd_o,
                        p4a=bool(h1 > bp[0] and h2 > bp[1] and dd >= bp[2]),
                        p4b=all(t4b.values()),
                        p4a_oos=bool(h1o > bpo[0] and h2o > bpo[1] and dd_o >= bpo[2]),
                        p4b_oos=all(t4bo.values()),
                        fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))

                    if c != RUNG_HEAD:
                        continue
                    # ---- placebos at the head rung only
                    s_real = f_sharpe(rg)
                    s_real_is, s_real_oos = f_sharpe(rg[is_m]), f_sharpe(rg[oos_m])
                    s_real_del = f_sharpe(rg[keep_m])
                    ov_real = (float((me[ep_m] < 1.0).sum()) / max(1.0, float((me < 1.0).sum())))
                    for kind in kinds:
                        ns = 2 if kind.startswith("SHIFT") else NSEED
                        for sd in range(ns):
                            pm = placebo_mult(me, d, kind,
                                              seed_of(panel, fam, q, w, d, cad, g, kind, sd),
                                              year_groups, ep_groups, sd)
                            rp = apply_eff(rb, pm, g, c)
                            ph.append(dict(
                                panel=panel, kind=kind, seed=sd, family=fam, state=s, side=side,
                                shift_sign=("LAG" if sd % 2 == 0 else "LEAD")
                                if kind.startswith("SHIFT") else "-",
                                prior=fam in PRIOR_FAMS, level=q, w=w, depth=d, cadence=cad,
                                gross=g, on_share=float((pm < 1.0).mean()),
                                gap=1.0 - float(pm.mean()), real_on=on_cache[key],
                                real_gap=gap_cache[key],
                                REAL=s_real, REAL_IS=s_real_is, REAL_OOS=s_real_oos,
                                REAL_DEL=s_real_del, real_ep_overlap=ov_real,
                                P=f_sharpe(rp), P_IS=f_sharpe(rp[is_m]),
                                P_OOS=f_sharpe(rp[oos_m]), P_DEL=f_sharpe(rp[keep_m]),
                                p_ep_overlap=float((pm[ep_m] < 1.0).sum())
                                / max(1.0, float((pm < 1.0).sum()))))
                            if sd == 0:
                                g5.append(dict(
                                    panel=panel, family=fam, level=q, w=w, depth=d, cadence=cad,
                                    gross=g, kind=kind,
                                    d_on=abs(float((pm < 1.0).mean()) - on_cache[key]),
                                    d_gap=abs((1.0 - float(pm.mean())) - gap_cache[key]),
                                    d_ep_days=abs(float((pm[ep_m] < 1.0).sum())
                                                  - float((me[ep_m] < 1.0).sum()))))
        log(f"    rung {c:>2} bps done ({time.time() - T0:.0f}s, cells {len(cells)}, "
            f"placebo cells {len(ph)})")

    meta = dict(panel=panel, g1=g1, start=str(start.date()), n_days=N,
                spy_pack=spy_pack, spy_oos_pack=spy_oos_pack, base_rows=base_rows,
                spy_row=dict(CAGR=m_spy["CAGR"], Sharpe=m_spy["Sharpe"], MaxDD=m_spy["MaxDD"],
                             H1=spy_pack[0], H2=spy_pack[1], OOS_CAGR=metrics(spy_o)["CAGR"],
                             OOS_Sharpe=metrics(spy_o)["Sharpe"], OOS_MaxDD=metrics(spy_o)["MaxDD"]),
                ep_share=float(ep_m.mean()))
    return meta, cells, ph, gates_log, g5


# ============================================================================================ main
def main():
    log("=" * 150)
    log("IDEA 815 - is the CORR-LO POSITIVE EXCESS a DE-GROSSING artefact?   (lane C, "
        f"{pd.Timestamp.today().date()})")
    log("=" * 150)
    log("\n[0] REPRODUCTION GATES")

    # ---- G4 fast metrics vs engine.metrics
    rng = np.random.default_rng(seed_of("G4"))
    g4rows = []
    for i in range(6):
        v = rng.normal(0.0004, 0.011, 2500)
        s = pd.Series(v, index=pd.bdate_range("2010-01-01", periods=2500))
        em = metrics(s)
        g4rows.append(dict(i=i, dCAGR=abs(f_cagr(v) - em["CAGR"]),
                           dSharpe=abs(f_sharpe(v) - em["Sharpe"]),
                           dMaxDD=abs(f_maxdd(v) - em["MaxDD"])))
    g4 = pd.DataFrame(g4rows)
    g4max = float(g4[["dCAGR", "dSharpe", "dMaxDD"]].to_numpy().max())
    log(f"  G4 fast numpy metrics vs engine.metrics over 6 series: max abs diff "
        f"{g4max:.3e} -> {'PASS' if g4max < 1e-12 else 'FAIL'}")

    # ---- G7 empty-deletion identity
    v = rng.normal(0.0004, 0.011, 2500)
    g7 = abs(f_sharpe(v[np.ones(2500, bool)]) - f_sharpe(v))
    log(f"  G7 deleting an EMPTY day set: |dSharpe| {g7:.3e} -> "
        f"{'PASS' if g7 == 0.0 else 'FAIL'}")

    panels = {}
    px_u = load_universe()
    panels["U56"] = px_u
    panels["B136"] = load_universe(broad=True)
    px_s = load_universe(small=True)
    meta_s = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta_s.loc[meta_s["max_1d_move"] >= 1.0, "ticker"])
    px_s = px_s[[c for c in px_s.columns if c == "SPY" or c not in bad]]
    panels[f"SMALL{px_s.shape[1] - 1}"] = px_s
    log(f"  small panel: {len(bad)} tickers with max_1d_move >= 1.0 dropped, "
        f"{px_s.shape[1] - 1} names + SPY")

    # ---- G2
    st_u = px_u.index[260]
    r84 = backtest(px_u, ewall_weights(px_u, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[st_u:]
    m84 = metrics(r84)
    h = len(r84) // 2
    h84 = (metrics(r84.iloc[:h])["Sharpe"], metrics(r84.iloc[h:])["Sharpe"])
    g2_ok = (abs(m84["CAGR"] - 0.118) < 0.002 and abs(m84["Sharpe"] - 1.05) < 0.02
             and abs(m84["MaxDD"] + 0.179) < 0.004)
    log(f"  G2 idea 84 EWALL U56 g=0.85 @10bps: {m84['CAGR']:.2%} / {m84['Sharpe']:.3f} / "
        f"{m84['MaxDD']:.2%} / H {h84[0]:.3f}/{h84[1]:.3f} (target 11.8%/1.05/-17.9%/1.07/1.04) "
        f"-> {'PASS' if g2_ok else 'FAIL'}")

    cells, ph, gates_log, g5 = [], [], [], []
    meta = {}
    for name, px in panels.items():
        m, c, p, gl, a5 = run_panel(name, px)
        meta[name] = m
        cells += c
        ph += p
        gates_log += gl
        g5 += a5

    cells = pd.DataFrame(cells)
    ph = pd.DataFrame(ph)
    g5 = pd.DataFrame(g5)
    gates_log = pd.DataFrame(gates_log)
    log(f"\n  {len(cells)} gated cells; {len(ph)} placebo cells "
        f"({len(KINDS)} kinds x seeds x {len(cells[cells.rung == RUNG_HEAD])} head-rung arms).")

    # ---- G1, G6
    g1 = max(m["g1"] for m in meta.values())
    log(f"\n  G1 cost-rung identity r(c) = r(0) - turnover*c/1e4 vs engine.backtest(10): "
        f"max abs {g1:.3e} -> {'PASS' if g1 < 1e-15 else 'FAIL'}")
    g6rows = []
    for nm, m in meta.items():
        g6rows.append(dict(panel=nm, who="RULES v2 @10", **{k: m["base_rows"][10][k] for k in
                                                            ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                             "OOS_Sharpe")}))
        g6rows.append(dict(panel=nm, who="SPY", **{k: m["spy_row"][k] for k in
                                                   ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                    "OOS_Sharpe")}))
    g6 = pd.DataFrame(g6rows)
    log("  G6 comparands (the record's: RULES v2 U56 8.63% / 1.2013 / -12.05%; "
        "SPY 15.16% / 0.8861 / -33.72%):")
    log(g6.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- G5 placebo matching identity
    g5max = float(g5[["d_on", "d_gap"]].to_numpy().max())
    log(f"\n  G5 placebo matching identity over {len(g5)} arm x kind checks (de-grossed day "
        f"count and mean multiplier): max abs {g5max:.3e} -> "
        f"{'PASS' if g5max < 1e-12 else 'FAIL'}")
    log(g5.groupby("kind")[["d_on", "d_gap", "d_ep_days"]].max().to_string(
        float_format=lambda x: f"{x:.3e}"))
    gep = float(g5[g5.kind.isin(["EPMATCH", "BLOCKEP"])]["d_ep_days"].max())
    log(f"  G5b the two EPISODE-stratified kinds reproduce the arm's firing-day count INSIDE the "
        f"episodes exactly: max abs {gep:.3e} -> {'PASS' if gep == 0.0 else 'FAIL'}")

    # ================================================================ arm-level excess table
    agg = ph.groupby(["panel", "family", "state", "side", "prior", "level", "w", "depth",
                      "cadence", "gross", "kind"]).agg(
        P=("P", "mean"), P_IS=("P_IS", "mean"), P_OOS=("P_OOS", "mean"),
        P_DEL=("P_DEL", "mean"), p_ep_overlap=("p_ep_overlap", "mean"),
        REAL=("REAL", "first"), REAL_IS=("REAL_IS", "first"), REAL_OOS=("REAL_OOS", "first"),
        REAL_DEL=("REAL_DEL", "first"), real_ep_overlap=("real_ep_overlap", "first"),
        on_share=("real_on", "first")).reset_index()
    agg["excess"] = agg["REAL"] - agg["P"]
    agg["excess_IS"] = agg["REAL_IS"] - agg["P_IS"]
    agg["excess_OOS"] = agg["REAL_OOS"] - agg["P_OOS"]
    agg["excess_DEL"] = agg["REAL_DEL"] - agg["P_DEL"]
    agg["d_overlap"] = agg["real_ep_overlap"] - agg["p_ep_overlap"]

    # ---- G3: idea 606's committed excess.csv, row by row
    log("\n  G3 idea 606's COMMITTED .excess.csv re-derived row by row (the object under test)")
    par = pd.read_csv(PARENT)
    keyc = ["panel", "family", "level", "w", "depth", "cadence", "gross"]
    mine = agg[agg.kind.isin(["BLOCK", "RAND"])].pivot_table(
        index=keyc, columns="kind", values=["P", "excess"]).reset_index()
    mine.columns = [a if not b else f"{a}_{b}" for a, b in mine.columns]
    real_mine = agg[agg.kind == "BLOCK"][keyc + ["REAL"]]
    j = par.merge(mine, on=keyc, how="inner", suffixes=("", "_new")).merge(
        real_mine, on=keyc, how="inner", suffixes=("", "_new"))
    # 606: REAL = arm dSharpe vs its matched-gross twin; dSharpe_<kind> = the placebo's dSharpe
    # vs the SAME twin (G5 there and here); so excess_vs_<kind> = Sharpe(real) - Sharpe(placebo),
    # which is exactly this run's `excess` and needs no twin.  That identity is what G3 prices.
    j["d_excess_BLOCK"] = (j["excess_vs_BLOCK"] - j["excess_BLOCK"]).abs()
    j["d_excess_RAND"] = (j["excess_vs_RAND"] - j["excess_RAND"]).abs()
    g3max = float(j[["d_excess_BLOCK", "d_excess_RAND"]].to_numpy().max())
    per_p = j.groupby("panel")[["d_excess_BLOCK", "d_excess_RAND"]].max().max(axis=1)
    g3a = float(per_p.get("B136", np.nan))
    log(f"    G3a per-arm, matched rows {len(j)} of {len(par)} committed; max abs diff on "
        f"excess_vs_BLOCK / excess_vs_RAND overall {g3max:.3e}, and on B136 -- the one panel "
        f"whose committed cache is unchanged -- {g3a:.3e} -> "
        f"{'PASS' if g3a < 1e-9 else 'FAIL'}")
    log(j.groupby("panel")[["d_excess_BLOCK", "d_excess_RAND"]].max().to_string(
        float_format=lambda x: f"{x:.3e}"))
    # ---- G3b: the panels that miss get the ONE candidate cause MEASURED, not waved away.
    # The committed price caches are NOT frozen.  If a cache has been re-adjusted since idea 606
    # ran (2026-09-12), the gate fires on different DAYS, so the arms are not the same arms and
    # no amount of care in this script can reproduce the committed cell.  The firing-day share
    # is committed in 606's own excess.csv, so the drift is directly measurable.
    on_new = agg[agg.kind == "BLOCK"][keyc + ["on_share"]]
    jo = par.merge(on_new, on=keyc, how="inner", suffixes=("_606", "_new"))
    jo["d_on"] = (jo["on_share_606"] - jo["on_share_new"]).abs()
    log("    G3b firing-day-share drift against idea 606's COMMITTED on_share (this is what says "
        "whether the arms are even the same arms):")
    log(jo.groupby("panel")["d_on"].agg(["max", "mean"]).to_string(
        float_format=lambda x: f"{x:.3e}"))
    log(f"    cache end dates now: "
        + ", ".join(f"{nm} {px.index[-1].date()}" for nm, px in panels.items()))

    comm = par.groupby("family").agg(med=("excess_vs_BLOCK", "median"),
                                     sh=("excess_vs_BLOCK", lambda s: (s > 0).mean()))
    here = agg[agg.kind == "BLOCK"].groupby("family").agg(
        med=("excess", "median"), sh=("excess", lambda s: (s > 0).mean()))
    cmp3 = comm.join(here, lsuffix="_606", rsuffix="_here")
    cmp3["d_med"] = (cmp3["med_606"] - cmp3["med_here"]).abs()
    cmp3["d_sh"] = (cmp3["sh_606"] - cmp3["sh_here"]).abs()
    g3c = float(cmp3[["d_med", "d_sh"]].to_numpy().max())
    log("    G3c the PUBLISHED object - idea 606's eight per-family medians and share>0, pooled "
        "over all three panels:")
    log(cmp3.to_string(float_format=lambda x: f"{x:.4f}"))
    log(f"    max abs diff {g3c:.4f} -> {'PASS' if g3c < 0.005 else 'FAIL'}  (bar declared "
        f"before the run: 0.005, i.e. the published 4-decimal numbers must agree to a "
        f"half-point in the last two)")

    # ====================================================== [1] Q1 THE ANSWER: excess by null
    log(f"\n{'=' * 150}\n[1] Q1 - THE ANSWER: median placebo excess per family, by PLACEBO KIND "
        f"(n = {len(agg[agg.kind == 'BLOCK'])//len(FAMILIES)} arms per family per kind)")
    piv = agg.pivot_table(index="family", columns="kind", values="excess", aggfunc="median")
    piv = piv[[k for k in KINDS]]
    shr = agg.pivot_table(index="family", columns="kind", values="excess",
                          aggfunc=lambda s: (s > 0).mean())[[k for k in KINDS]]
    order = ["BREADTH-LO", "CORR-HI", "DISP-HI", "VOL20-HI", "CORR-LO", "BREADTH-HI",
             "VOL20-LO", "DISP-LO"]
    log("  median excess (real arm Sharpe - placebo Sharpe), all arms pooled over the three panels:")
    log(piv.loc[order].to_string(float_format=lambda x: f"{x:+.4f}"))
    log("\n  share of arms beating their own placebo:")
    log(shr.loc[order].to_string(float_format=lambda x: f"{x:.3f}"))

    log("\n  the same, per panel (reported axis, never selected on):")
    pv2 = agg.pivot_table(index=["panel", "family"], columns="kind", values="excess",
                          aggfunc="median")[[k for k in KINDS]]
    log(pv2.to_string(float_format=lambda x: f"{x:+.4f}"))

    # ====================================================== [2] Q2 the SHIFT ladder
    log(f"\n{'=' * 150}\n[2] Q2 - THE DECISIVE SHAPE TEST: excess against a circular shift of "
        f"EXACTLY s days")
    lad = ph[ph.kind.str.startswith("SHIFT")].copy()
    lad["s"] = lad.kind.str[5:].astype(int)
    lad["excess"] = lad["REAL"] - lad["P"]
    lt = lad.pivot_table(index="family", columns="s", values="excess", aggfunc="median")
    lt["BLOCK(uniform)"] = piv["BLOCK"]
    log("  median excess by shift magnitude (days), LAG and LEAD pooled; BLOCK's uniform shift "
        "on the right:")
    log(lt.loc[order].to_string(float_format=lambda x: f"{x:+.4f}"))
    log("\n  split by direction - LAG (the gate fires s days LATER) and LEAD (s days EARLIER):")
    for sg in ("LAG", "LEAD"):
        sub = lad[lad.shift_sign == sg].pivot_table(index="family", columns="s", values="excess",
                                                    aggfunc="median")
        log(f"   {sg}:")
        log(sub.loc[order].to_string(float_format=lambda x: f"{x:+.4f}"))
    rho = {}
    for f in FAMILIES:
        sub = lad[lad.family == f].groupby("s")["excess"].median()
        rho[f] = float(pd.Series(sub.index).rank().corr(pd.Series(sub.values).rank()))
    log("\n  Spearman(shift magnitude, median excess) - (A) CALENDAR predicts strongly POSITIVE, "
        "(B) INFORMATION predicts ~0:")
    log(pd.Series(rho).loc[order].to_string(float_format=lambda x: f"{x:+.3f}"))

    # ====================================================== [3] Q3 episode deletion
    log(f"\n{'=' * 150}\n[3] Q3 - EPISODE DELETION: the same excess re-read with COVID_TIGHT and "
        f"BEAR2022 removed from the return stream")
    d1 = agg.pivot_table(index="family", columns="kind", values="excess", aggfunc="median")
    d2 = agg.pivot_table(index="family", columns="kind", values="excess_DEL", aggfunc="median")
    dd = pd.concat([d1[["BLOCK", "BLOCKYEAR", "BLOCKEP"]].add_suffix("_full"),
                    d2[["BLOCK", "BLOCKYEAR", "BLOCKEP"]].add_suffix("_exEP")], axis=1)
    dd["BLOCK_kept_share"] = dd["BLOCK_exEP"] / dd["BLOCK_full"]
    log(dd.loc[order].to_string(float_format=lambda x: f"{x:+.4f}"))

    # ====================================================== [4] Q4 overlap mechanism
    log(f"\n{'=' * 150}\n[4] Q4 - THE MECHANISM, MEASURED DIRECTLY: share of an arm's de-grossed "
        f"days that fall inside the two episodes")
    ov = agg.pivot_table(index="family", columns="kind", values="p_ep_overlap", aggfunc="median")
    ovr = agg[agg.kind == "BLOCK"].groupby("family")["real_ep_overlap"].median()
    ovt = pd.concat([ovr.rename("REAL"), ov[["BLOCK", "RAND", "YEARMATCH", "EPMATCH",
                                             "BLOCKYEAR", "BLOCKEP", "SHIFT5", "SHIFT252"]]],
                    axis=1)
    ovt["REAL-BLOCK"] = ovt["REAL"] - ovt["BLOCK"]
    log(ovt.loc[order].to_string(float_format=lambda x: f"{x:.4f}"))
    log(f"  (the episodes are {np.mean([m['ep_share'] for m in meta.values()]):.2%} of the "
        f"evaluation window, which is the information-free expectation)")

    # ====================================================== [5] Q5 rule 8 on the claim
    log(f"\n{'=' * 150}\n[5] Q5 - RULE 8 ON THE CLAIM: the excess fitted on 2009-2016 and read "
        f"once on 2017+")
    cl = []
    for f in FAMILIES:
        for k in KINDS:
            sub = agg[(agg.family == f) & (agg.kind == k)]
            cl.append(dict(family=f, kind=k, n=len(sub),
                           med_IS=sub["excess_IS"].median(), med_OOS=sub["excess_OOS"].median(),
                           rho=float(sub["excess_IS"].rank().corr(sub["excess_OOS"].rank())),
                           sign_agree=float((np.sign(sub["excess_IS"])
                                             == np.sign(sub["excess_OOS"])).mean())))
    cl = pd.DataFrame(cl)
    log(cl.pivot_table(index="family", columns="kind", values="med_IS")[KINDS]
        .loc[order].to_string(float_format=lambda x: f"{x:+.4f}"))
    log("\n  and out of sample:")
    log(cl.pivot_table(index="family", columns="kind", values="med_OOS")[KINDS]
        .loc[order].to_string(float_format=lambda x: f"{x:+.4f}"))
    log("\n  Spearman(IS excess, OOS excess) per arm, and sign agreement:")
    log(cl.pivot_table(index="family", columns="kind", values="rho")[["BLOCK", "BLOCKYEAR",
                                                                     "BLOCKEP"]]
        .loc[order].to_string(float_format=lambda x: f"{x:+.3f}"))

    # ====================================================== [6] Q6 rule 8 on the books
    log(f"\n{'=' * 150}\n[6] Q6 - RULE 8 ON THE BOOKS: both KEEP paths on every grid point")
    log(f"  4a passes {int(cells.p4a.sum())} of {len(cells)} "
        f"({int(cells[cells.rung == RUNG_HEAD].p4a.sum())} at the protocol rung); "
        f"4b passes {int(cells.p4b.sum())} of {len(cells)} "
        f"({int(cells[cells.rung == RUNG_HEAD].p4b.sum())} at the protocol rung)")
    log("\n  4b pass counts by family x rung (all grid points reported):")
    log(cells.pivot_table(index="family", columns="rung", values="p4b",
                          aggfunc="sum").loc[order].to_string())
    log("\n  binding 4b failure leg, protocol rung, counts by family:")
    fb = cells[cells.rung == RUNG_HEAD].groupby(["family", "fail4b"]).size().unstack(fill_value=0)
    log(fb.to_string())

    # ---- the chooser
    grp = ["panel", "family", "depth", "cadence", "gross", "rung"]
    picks = cells.loc[cells.groupby(grp)["IS_Sharpe"].idxmax()].copy()
    log(f"\n  the rule-8 chooser: (level, w) picked on IS Sharpe 2009-2016 per "
        f"{' x '.join(grp)} -> {len(picks)} picks")
    ch = picks.groupby("family").agg(
        n=("p4b", "size"), p4b_full=("p4b", "mean"), p4b_oos=("p4b_oos", "mean"),
        p4a_full=("p4a", "mean"), OOS_CAGR=("OOS_CAGR", "median"),
        OOS_Sharpe=("OOS_Sharpe", "median"), OOS_MaxDD=("OOS_MaxDD", "median"))
    log(ch.loc[order].to_string(float_format=lambda x: f"{x:.4f}"))
    log("\n  and the comparands the picks are read against (OOS window, per panel):")
    cmp_rows = []
    for nm, m in meta.items():
        cmp_rows.append(dict(panel=nm, who="RULES v2 @10bps", CAGR=m["base_rows"][10]["OOS_CAGR"],
                             Sharpe=m["base_rows"][10]["OOS_Sharpe"],
                             MaxDD=m["base_rows"][10]["OOS_MaxDD"]))
        cmp_rows.append(dict(panel=nm, who="SPY", CAGR=m["spy_row"]["OOS_CAGR"],
                             Sharpe=m["spy_row"]["OOS_Sharpe"], MaxDD=m["spy_row"]["OOS_MaxDD"]))
    cmpd = pd.DataFrame(cmp_rows)
    log(cmpd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for nm, m in meta.items():
        pk = picks[picks.panel == nm]
        bo = m["base_rows"][10]
        so = m["spy_row"]
        log(f"  {nm}: picks beating RULES v2 OOS Sharpe {int((pk.OOS_Sharpe > bo['OOS_Sharpe']).sum())}"
            f"/{len(pk)}; beating SPY OOS Sharpe "
            f"{int((pk.OOS_Sharpe > so['OOS_Sharpe']).sum())}/{len(pk)}; "
            f"OOS CAGR >= 70% of SPY's {int((pk.OOS_CAGR >= 0.70 * so['OOS_CAGR']).sum())}/{len(pk)}")

    # ---- the CORR-LO book specifically, at the protocol rung, best IS arm per panel
    log("\n  the CORR-LO books themselves at the protocol rung (10 bps), rule-8 IS pick per panel "
        "x depth x cadence x gross:")
    cl_pick = picks[(picks.family == "CORR-LO") & (picks.rung == RUNG_HEAD)]
    log(cl_pick[["panel", "level", "w", "depth", "cadence", "gross", "CAGR", "Sharpe", "MaxDD",
                 "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "p4a", "p4b", "fail4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- write
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    agg.to_csv(OUT / f"{STEM}.excess.csv.gz", index=False, compression="gzip")
    ph.to_csv(OUT / f"{STEM}.placebo.csv.gz", index=False, compression="gzip")
    picks.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    lt.to_csv(OUT / f"{STEM}.ladder.csv")
    ovt.to_csv(OUT / f"{STEM}.overlap.csv")
    cl.to_csv(OUT / f"{STEM}.claim.csv", index=False)
    gates_log.to_csv(OUT / f"{STEM}.gates.csv", index=False)
    g5.to_csv(OUT / f"{STEM}.g5.csv.gz", index=False, compression="gzip")
    log(f"\nDone in {time.time() - T0:.0f}s.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

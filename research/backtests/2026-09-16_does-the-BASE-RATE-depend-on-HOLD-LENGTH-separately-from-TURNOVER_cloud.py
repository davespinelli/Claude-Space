#!/usr/bin/env python3
"""Idea 936 (cloud lane, 2026-09-16) — does the BASE RATE depend on HOLD LENGTH separately from
TURNOVER?

QUESTION (QUEUE idea 936, verbatim)
    idea 926 (lane B run) found the W/M zero-crossing gap shrinks from 5.12x in COST to 2.31x in
    realised DRAG but does not close (H_DRAG FAIL at a 2.0x bar), so turnover explains about half
    of the cadence effect.  Split the cadence axis into REBALANCE FREQUENCY and per-name HOLDING
    PERIOD (a weekly grid with a minimum-hold constraint turns one into the other) and measure
    which one carries the null's upper tail.  Max 2 params (rebalance grid, min hold).

THE CONSTRUCTION THAT SPLITS THE AXIS.  A cadence dial confounds two things: how OFTEN the book
    may trade (REBALANCE FREQUENCY f) and how LONG a name stays once bought (HOLDING PERIOD).
    A minimum-hold constraint separates them: at each rebalance date, every name held for fewer
    than H trading days is RETAINED (it may not be sold), and only the remaining slots are filled
    from that date's ranking.  H = 0 is the record's ordinary book.  A daily grid with H = 63 is a
    book that may react every day but turns over at a quarterly rate; a quarterly grid with H = 0
    is a book that reacts four times a year and replaces everything when it does.  The two have
    nearly the same turnover and opposite reaction speeds, which is exactly the contrast 926's
    drag-matching could not make.

THE TWO DIALS (rule 4, no more than two tuned parameters)
    1. REBALANCE GRID  f in {D, W, M, Q}
    2. MIN HOLD        H in {0, 5, 21, 63, 126} trading days
    All 20 points reported for books AND for the gross-matched null.  Gross 0.75 and 10 bps are
    PROTOCOL/968 conventions held fixed, not dials; a 0 bps re-pricing is printed as a diagnostic
    on the comparand (968's C2 precedent), never as a third dial.

THE ARITHMETIC, DECLARED BEFORE ANY NUMBER.
    Raising H cuts realised turnover at fixed f, so if the cadence effect is ENTIRELY a turnover
    rebate (931/943's reading) then the null's upper tail should be a function of realised drag
    alone: two cells with the same drag should have the same tail whatever their f.  If instead
    reaction speed matters in its own right, cells at the same drag but different f will separate
    — and the sign is not obvious in advance.  Holding a loser through a selloff (large H) raises
    |MaxDD|, which is the leg 968 and 1059 both found to be cost-invariant; so the prediction that
    can actually be refuted is: H moves L_DD and f moves nothing once drag is charged.

RULE 8.  The (f, H) point is chosen on 2009-2016 alone (IS Sharpe, and an IS 4b-leg count) and
    2017-2026 is read once, against SPY and against the live RULES v2 book at the same rung.
    Both KEEP paths reported at every one of the 20 grid points.

SURVIVORSHIP.  U56 and B136 are current-constituent panels.  The bias is common to books and to
    the null and flatters both the CAGR floor and the DD cap against SPY, which is a real index.
"""
from __future__ import annotations

import hashlib
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-the-BASE-RATE-depend-on-HOLD-LENGTH-separately-from-TURNOVER"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
BAND = 0.03
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS = 0.75

# ---- the two tuned dials ----------------------------------------------------------------------
FREQS = ["D", "W", "M", "Q"]
HOLDS = [0, 5, 21, 63, 126]

PANELS = ["U56", "B136"]
MECHS = ["CAND20", "R3_84", "MOMONLY"]
LEGSETS = {"CAND20": [(21, 252), (0, 126), (0, 63)],
           "R3_84": [(21, 252), (0, 126), (0, 84)],
           "MOMONLY": [(21, 252)]}
LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
NSEED = 20

# committed cross-run anchors
CAND20_W_1059 = (0.12738, 1.0603, -0.18310)      # idea 1059 census, U56/CAND20/W/0.75/10bps
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
NULL_TURN_1059 = {"D": 239.0, "W": 49.8, "M": 11.5, "Q": 3.9}   # U56 null turn/yr at H=0
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


def nrun(rets, wt, mk):
    """GROSS returns and turnover; cost applied outside (gated at G1 against engine.backtest)."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
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
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lag(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def lagmask(m):
    out = np.zeros_like(m)
    out[LAG:] = m[:-LAG]
    return out


def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_score(px, mech):
    """Selection SCORE (higher = better) and the eligibility mask — 961/968/1059's construction,
    verbatim, with the ranking exposed so a min-hold constraint can fill only the free slots."""
    comp = legs_composite(px, LEGSETS[mech])
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))      # no vol scaler (KEEP 4b convention)
    elig = (above & (vol20 < MAXVOL)).values
    return sc.values, elig


def minhold_weights(rank_key, elig, priced, reb, H, T, N):
    """Gross-1.0 target weights under a MIN-HOLD constraint.

    rank_key[t, j]  : ordering key at day t, LOWER = picked first (NaN = never pickable)
    elig[t, j]      : eligibility gate at day t (the book's own screen; ignored for retained names)
    priced[t, j]    : the name has a price that day
    reb             : rebalance day indices
    H               : minimum hold in trading days; a name entered at t0 may not be sold before
                      t0 + H.  H = 0 reproduces the record's ordinary book exactly.
    Weights are a step function: set at each rebalance date, constant until the next one.
    """
    W = np.zeros((T, N))
    cur = np.full(N, -1, dtype=np.int64)          # entry day per column, -1 = not held
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]        # an unpriced name cannot be held
        else:
            young = held
        keep = set(young.tolist())
        need = NTOP - len(keep)
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf                      # already held
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        else:
            take = []
        new_cur = np.full(N, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = 1.0 / len(sel)
    return W


def blocks(r, warm, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    o = r[oos]
    oc, os_, od = fmet(o)
    ii = r[warm & ~oos]
    ic, is_, idd = fmet(ii)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"L_OOS_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_OOS_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "L_OOS_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def eta2(y, g):
    """Fraction of variance in y explained by the grouping g (one-way, unadjusted)."""
    y = np.asarray(y, float)
    tot = ((y - y.mean()) ** 2).sum()
    if tot == 0:
        return np.nan
    bet = 0.0
    for lev in pd.unique(pd.Series(g)):
        m = np.asarray(pd.Series(g) == lev)
        bet += m.sum() * (y[m].mean() - y.mean()) ** 2
    return float(bet / tot)


def main():
    t0 = time.time()
    P(f"# Idea 936 (cloud lane, {DATE}) — does the BASE RATE depend on HOLD LENGTH separately "
      f"from TURNOVER?")
    P(f"# 2 tuned dials: REBALANCE GRID {FREQS} x MIN HOLD {HOLDS} trading days = "
      f"{len(FREQS)*len(HOLDS)} points, ALL reported, none selected.")
    P(f"# Fixed (NOT dials): gross {GROSS}, cost {COST:.0f} bps (PROTOCOL rule 2), NTOP {NTOP}, "
      f"max_vol {MAXVOL}, {len(MECHS)} top-N mechanisms x {len(PANELS)} panels, canonical "
      f"calendar period-end rebalance dates.  A 0 bps re-pricing is a DIAGNOSTIC (968's C2).")
    P("# MIN HOLD: at each rebalance date a name held fewer than H trading days is RETAINED and")
    P("#   only the free slots are refilled from that date's ranking.  H=0 is the ordinary book")
    P("#   (gated at G3).  (D, H=63) reacts daily but turns over quarterly; (Q, H=0) reacts four")
    P("#   times a year and replaces everything — same drag, opposite reaction speed.")
    P("# DECLARED BEFORE ANY NUMBER: if the cadence effect is ENTIRELY a turnover rebate, the")
    P("#   null's upper tail is a function of realised DRAG alone and two cells at matched drag")
    P("#   must agree whatever their f.  The refutable prediction is that H moves L_DD (holding a")
    P("#   loser through a selloff) while f moves nothing once drag is charged.")
    P(f"# NSEED = {NSEED} gross-matched null books per (panel, f, H), drawn from ONE per-day")
    P("#   permutation stream per (panel, seed) so the null is PAIRED across both dials.")
    P("# SURVIVORSHIP: current-constituent panels; the bias is common to books and null.")
    P("")

    PXD = {"U56": load_universe(), "B136": load_universe(broad=True)}
    PAN = {}
    for p, px in PXD.items():
        idx = px.index
        rets = px.pct_change().fillna(0.0).values
        ar = np.arange(len(idx))
        warm = ar >= WARMUP
        oos = np.asarray(idx > pd.Timestamp(IS_END))
        spyr = px["SPY"].pct_change().fillna(0.0).values
        PAN[p] = dict(px=px, idx=idx, rets=rets, warm=warm, oos=oos & warm, T=len(idx),
                      N=px.shape[1], priced=px.notna().values, yrs=warm.sum() / 252.0,
                      spy=blocks(spyr, warm, oos & warm),
                      reb={f: np.flatnonzero(rebalance_mask(idx, f).values) for f in FREQS},
                      mask={f: rebalance_mask(idx, f).values for f in FREQS})
        P(f"  {p}: {px.shape[1]} cols x {len(idx)} days, {idx[0].date()} -> {idx[-1].date()}; "
          f"SPY full {PAN[p]['spy']['CAGR']:.2%} / {PAN[p]['spy']['Sharpe']:.4f} / "
          f"{PAN[p]['spy']['MaxDD']:.2%}; rebalance counts "
          + ", ".join(f"{f} {len(PAN[p]['reb'][f]):,}" for f in FREQS))

    SCORE = {}
    for p, m in product(PANELS, MECHS):
        sc, el = mech_score(PXD[p], m)
        with np.errstate(invalid="ignore"):
            key = -np.nan_to_num(sc, nan=-np.inf)      # LOWER key = better score
        key[np.isnan(sc)] = np.inf
        SCORE[(p, m)] = (key, el)

    # one per-day permutation stream per (panel, seed): pairs the null across BOTH dials
    PERM = {}
    for p, s in product(PANELS, range(NSEED)):
        T, N = PAN[p]["T"], PAN[p]["N"]
        rng = np.random.default_rng(mdseed("PERM936", p, s, T, N))
        PERM[(p, s)] = rng.random((T, N)).astype(np.float32)   # uniform key; lower = first

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES")
    P("=" * 100)
    gates = {}

    px = PXD["U56"]
    w1 = GROSS * minhold_weights(*SCORE[("U56", "CAND20")], PAN["U56"]["priced"],
                                 PAN["U56"]["reb"]["W"], 0, PAN["U56"]["T"], PAN["U56"]["N"])
    gr, tt = nrun(PAN["U56"]["rets"], lag(w1), lagmask(PAN["U56"]["mask"]["W"]))
    mine = gr - tt * COST / 1e4
    eng = backtest(px, pd.DataFrame(w1, index=px.index, columns=px.columns),
                   cost_bps=COST, freq="W")
    d1r = float(np.abs(mine[WARMUP:] - eng["returns"].values[WARMUP:]).max())
    gates["G1"] = (d1r < 1e-12, f"OUTSIDE-cost runner == engine.backtest at {COST:.0f} bps on the "
                                f"min-hold book: max|dret| {d1r:.2e}")

    trip = fmet(mine[PAN["U56"]["warm"]])
    d3 = max(abs(trip[i] - CAND20_W_1059[i]) for i in range(3))
    gates["G3"] = (d3 < 5e-3, f"CROSS-RUN H=0 reproduces idea 1059's committed U56/CAND20/W/"
                              f"{GROSS}/{COST:.0f}bps book: {trip[0]:.4%} / {trip[1]:.4f} / "
                              f"{trip[2]:.2%} vs 12.738% / 1.0603 / -18.31% (max|d| {d3:.2e})")

    sp = PAN["U56"]["spy"]
    d4 = max(abs(sp["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sp["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sp["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G4"] = (d4 < 5e-4, f"CROSS-RUN SPY OOS at {IS_END}: {sp['OOS_CAGR']:.4f} / "
                              f"{sp['OOS_Sharpe']:.4f} / {sp['OOS_MaxDD']:.4f} vs committed "
                              f"{SPY_OOS_COMMITTED} (max|d| {d4:.2e})")

    # G5: the constraint BINDS — realised holding period rises with H, and no name is ever sold
    # before H days.  Measured on the weights themselves, not inferred.
    meanhold = {}
    for H in HOLDS:
        Wc = minhold_weights(*SCORE[("U56", "CAND20")], PAN["U56"]["priced"],
                             PAN["U56"]["reb"]["W"], H, PAN["U56"]["T"], PAN["U56"]["N"])
        occ = Wc > 0
        spans = []
        for j in range(occ.shape[1]):
            col = occ[:, j]
            if not col.any():
                continue
            d = np.diff(np.concatenate([[0], col.view(np.int8), [0]]))
            st, en = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
            spans.extend((en - st).tolist())
        spans = np.array(spans)
        meanhold[H] = float(spans.mean()) if len(spans) else np.nan
    mono = all(meanhold[HOLDS[i]] <= meanhold[HOLDS[i + 1]] + 1e-9 for i in range(len(HOLDS) - 1))
    gates["G5"] = (mono, "the MIN-HOLD constraint binds: mean realised holding span (trading days,"
                         " U56/CAND20/W) rises monotonically with H — "
                         + ", ".join(f"H={H} {meanhold[H]:.1f}d" for H in HOLDS))

    # G6: the null is gross-matched and its H=0 turnover reproduces 1059's committed null
    nturn, d6 = {}, 0.0
    for f in FREQS:
        el = np.ones_like(PAN["U56"]["priced"])
        Wn = minhold_weights(PERM[("U56", 0)], el, PAN["U56"]["priced"],
                             PAN["U56"]["reb"][f], 0, PAN["U56"]["T"], PAN["U56"]["N"])
        _, t = nrun(PAN["U56"]["rets"], lag(GROSS * Wn), lagmask(PAN["U56"]["mask"][f]))
        nturn[f] = float(t[PAN["U56"]["warm"]].sum() / PAN["U56"]["yrs"])
        d6 = max(d6, abs(nturn[f] - NULL_TURN_1059[f]) / NULL_TURN_1059[f])
    gates["G6"] = (d6 < 0.15, "CROSS-RUN the H=0 null's realised turnover reproduces idea 1059's "
                              "committed U56 null (within 15%): "
                              + ", ".join(f"{f} {nturn[f]:.1f} vs {NULL_TURN_1059[f]:.1f}/yr"
                                          for f in FREQS) + f"  max rel|d| {d6:.3f}")

    g7 = float(np.abs(np.where(w1.sum(axis=1) > 0, w1.sum(axis=1), GROSS) - GROSS).max())
    gates["G7"] = (g7 < 1e-12, f"gross-matched everywhere the book is invested: "
                               f"max|sum(w) - {GROSS}| = {g7:.2e}")

    # ================================================================== (A) the grid
    rows = []
    for p, m, f, H in product(PANELS, MECHS, FREQS, HOLDS):
        pan = PAN[p]
        W = GROSS * minhold_weights(*SCORE[(p, m)], pan["priced"], pan["reb"][f], H,
                                    pan["T"], pan["N"])
        gr, t = nrun(pan["rets"], lag(W), lagmask(pan["mask"][f]))
        ty = float(t[pan["warm"]].sum() / pan["yrs"])
        for c in (COST, 0.0):
            r = gr - t * c / 1e4
            b = blocks(r, pan["warm"], pan["oos"])
            lg = legs_4b(b, pan["spy"])
            rows.append(dict(kind="BOOK", panel=p, mech=m, freq=f, hold=H, seed=-1, cost=c,
                             turn_yr=ty, drag_bp=ty * c, **b, **lg, pass4b=all(lg.values()),
                             nfail=sum(1 for v in lg.values() if not v)))
    for p, f, H, s in product(PANELS, FREQS, HOLDS, range(NSEED)):
        pan = PAN[p]
        el = np.ones_like(pan["priced"])
        W = GROSS * minhold_weights(PERM[(p, s)], el, pan["priced"], pan["reb"][f], H,
                                    pan["T"], pan["N"])
        gr, t = nrun(pan["rets"], lag(W), lagmask(pan["mask"][f]))
        ty = float(t[pan["warm"]].sum() / pan["yrs"])
        for c in (COST, 0.0):
            r = gr - t * c / 1e4
            b = blocks(r, pan["warm"], pan["oos"])
            lg = legs_4b(b, pan["spy"])
            rows.append(dict(kind="NULL", panel=p, mech="NULL", freq=f, hold=H, seed=s, cost=c,
                             turn_yr=ty, drag_bp=ty * c, **b, **lg, pass4b=all(lg.values()),
                             nfail=sum(1 for v in lg.values() if not v)))
    G = pd.DataFrame(rows)

    for k in sorted(gates, key=lambda s: int(s[1:])):
        ok, msg = gates[k]
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"GATES: {sum(1 for v in gates.values() if v[0])} of {len(gates)} pass.")
    P("")
    P("=" * 100)
    P("(A) THE GRID — 4 rebalance frequencies x 5 min-holds x (books, null) x 2 panels")
    P("=" * 100)
    dump(G, "grid")
    P(f"  {int((G.kind=='BOOK').sum()):,} book rows + {int((G.kind=='NULL').sum()):,} null rows "
      f"(each book/null priced at {COST:.0f} and 0 bps).")
    P("")

    # ================================================================== (B) turnover surface
    P("=" * 100)
    P("(B) DOES H BUY THE SAME TURNOVER AS f?  realised turns/yr (the axis-splitting check)")
    P("=" * 100)
    for kind in ["BOOK", "NULL"]:
        s = G[(G.kind == kind) & (G.cost == COST) & (G.panel == "U56")]
        piv = s.pivot_table(index="freq", columns="hold", values="turn_yr").loc[FREQS]
        P(f"  {kind} U56 turnover/yr (rows = rebalance grid, cols = min hold):")
        for line in piv.to_string(float_format=lambda x: f"{x:8.2f}").split("\n"):
            P("    " + line)
    P("")

    # ================================================================== (C) the null's upper tail
    P("=" * 100)
    P("(C) THE NULL'S UPPER TAIL — base rate and p90 Sharpe by (f, H)")
    P("=" * 100)
    tail = []
    for p, f, H, c in product(PANELS, FREQS, HOLDS, [COST, 0.0]):
        s = G[(G.kind == "NULL") & (G.panel == p) & (G.freq == f) & (G.hold == H) & (G.cost == c)]
        tail.append(dict(panel=p, freq=f, hold=H, cost=c, n=len(s),
                         base4b=float(s.pass4b.mean()),
                         p90_Sharpe=float(np.percentile(s.Sharpe, 90)),
                         med_Sharpe=float(s.Sharpe.median()),
                         p90_OOS_Sharpe=float(np.percentile(s.OOS_Sharpe, 90)),
                         med_MaxDD=float(s.MaxDD.median()),
                         med_CAGR=float(s.CAGR.median()),
                         turn_yr=float(s.turn_yr.mean()), drag_bp=float(s.drag_bp.mean()),
                         **{lg: float((~s[lg]).mean()) for lg in LEGS}))
    TL = pd.DataFrame(tail)
    dump(TL, "nulltail")
    for c in [COST, 0.0]:
        P(f"  NULL p90 Sharpe, U56, {c:.0f} bps (rows = f, cols = H):")
        piv = TL[(TL.panel == "U56") & (TL.cost == c)].pivot_table(
            index="freq", columns="hold", values="p90_Sharpe").loc[FREQS]
        for line in piv.to_string(float_format=lambda x: f"{x:7.3f}").split("\n"):
            P("    " + line)
    P(f"  NULL 4b base rate, U56, {COST:.0f} bps (rows = f, cols = H):")
    piv = TL[(TL.panel == "U56") & (TL.cost == COST)].pivot_table(
        index="freq", columns="hold", values="base4b").loc[FREQS]
    for line in piv.to_string(float_format=lambda x: f"{x:7.3f}").split("\n"):
        P("    " + line)
    P(f"  NULL L_DD failure share, U56, {COST:.0f} bps (rows = f, cols = H):")
    piv = TL[(TL.panel == "U56") & (TL.cost == COST)].pivot_table(
        index="freq", columns="hold", values="L_DD").loc[FREQS]
    for line in piv.to_string(float_format=lambda x: f"{x:7.3f}").split("\n"):
        P("    " + line)
    P("")

    # ================================================================== (D) matched drag
    P("=" * 100)
    P("(D) THE DECISIVE TEST — cells at MATCHED DRAG but different f")
    P("=" * 100)
    P("    A pair is MATCHED when the two cells' realised turnover is within 20% of each other.")
    P("    If the cadence effect is entirely a turnover rebate, matched pairs must agree.")
    pairs = []
    for p, c in product(PANELS, [COST, 0.0]):
        t = TL[(TL.panel == p) & (TL.cost == c)]
        recs = t.to_dict("records")
        for i in range(len(recs)):
            for j in range(i + 1, len(recs)):
                a, b = recs[i], recs[j]
                if a["freq"] == b["freq"]:
                    continue
                lo, hi = sorted([a["turn_yr"], b["turn_yr"]])
                if lo <= 0 or hi / lo > 1.20:
                    continue
                pairs.append(dict(panel=p, cost=c, f1=a["freq"], h1=a["hold"], f2=b["freq"],
                                  h2=b["hold"], turn1=a["turn_yr"], turn2=b["turn_yr"],
                                  turn_ratio=hi / lo,
                                  d_p90=a["p90_Sharpe"] - b["p90_Sharpe"],
                                  d_base=a["base4b"] - b["base4b"],
                                  d_medDD=a["med_MaxDD"] - b["med_MaxDD"],
                                  d_LDD=a["L_DD"] - b["L_DD"]))
    PRS = pd.DataFrame(pairs)
    dump(PRS, "matchedpairs")
    if len(PRS):
        mm = PRS[PRS.cost == COST]
        P(f"    {len(mm)} matched pairs at {COST:.0f} bps (turnover within 20%).  "
          f"|d p90 Sharpe| median {mm.d_p90.abs().median():.4f}, max {mm.d_p90.abs().max():.4f}; "
          f"|d base rate| median {mm.d_base.abs().median():.4f}, max {mm.d_base.abs().max():.4f}")
        for line in mm.sort_values("d_p90", key=abs, ascending=False).head(10).to_string(
                index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
            P("      " + line)
    P("")

    # variance decomposition on the 20 null cells
    P("    VARIANCE DECOMPOSITION of the null's p90 Sharpe over the 20 (f, H) cells, U56:")
    dec = []
    for p, c in product(PANELS, [COST, 0.0]):
        t = TL[(TL.panel == p) & (TL.cost == c)]
        lt = pd.qcut(np.log(t.turn_yr.clip(lower=1e-9)), 4, labels=False, duplicates="drop")
        dec.append(dict(panel=p, cost=c,
                        eta2_freq=eta2(t.p90_Sharpe.values, t.freq.values),
                        eta2_hold=eta2(t.p90_Sharpe.values, t.hold.values),
                        eta2_logturn_q4=eta2(t.p90_Sharpe.values, lt.values),
                        eta2_freq_base=eta2(t.base4b.values, t.freq.values),
                        eta2_hold_base=eta2(t.base4b.values, t.hold.values),
                        eta2_logturn_base=eta2(t.base4b.values, lt.values)))
    DEC = pd.DataFrame(dec)
    dump(DEC, "decomposition")
    for line in DEC.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("      " + line)
    P("")

    # ================================================================== (E) the books
    P("=" * 100)
    P("(E) THE BOOKS — 4b pass and the two KEEP paths at every (f, H)")
    P("=" * 100)
    bk = G[(G.kind == "BOOK") & (G.cost == COST)]
    for p in PANELS:
        P(f"  {p} 4b pass count over {len(MECHS)} mechanisms (rows = f, cols = H):")
        piv = bk[bk.panel == p].pivot_table(index="freq", columns="hold", values="pass4b",
                                            aggfunc="sum").loc[FREQS]
        for line in piv.to_string().split("\n"):
            P("    " + line)
        P(f"  {p} book Sharpe, mean over mechanisms (rows = f, cols = H):")
        piv = bk[bk.panel == p].pivot_table(index="freq", columns="hold",
                                            values="Sharpe").loc[FREQS]
        for line in piv.to_string(float_format=lambda x: f"{x:7.4f}").split("\n"):
            P("    " + line)
        P(f"  {p} book MaxDD, mean over mechanisms (rows = f, cols = H):")
        piv = bk[bk.panel == p].pivot_table(index="freq", columns="hold",
                                            values="MaxDD").loc[FREQS]
        for line in piv.to_string(float_format=lambda x: f"{x:7.4f}").split("\n"):
            P("    " + line)
    P("")

    # the 4a comparand: live RULES v2 at the same rung
    V2 = {}
    for p in PANELS:
        pxp = PXD[p]
        w = rules_v2_weights(pxp, BAND, GROSS).values
        gr, t = nrun(PAN[p]["rets"], lag(w), lagmask(PAN[p]["mask"]["W"]))
        V2[p] = blocks(gr - t * COST / 1e4, PAN[p]["warm"], PAN[p]["oos"])
        P(f"  RULES v2 (live) {p} @ {COST:.0f} bps: full {V2[p]['CAGR']:.2%} / "
          f"{V2[p]['Sharpe']:.4f} / {V2[p]['MaxDD']:.2%}, halves {V2[p]['H1']:.3f}/"
          f"{V2[p]['H2']:.3f}, OOS {V2[p]['OOS_CAGR']:.2%} / {V2[p]['OOS_Sharpe']:.4f} / "
          f"{V2[p]['OOS_MaxDD']:.2%}")
    kp = []
    for p, m, f, H in product(PANELS, MECHS, FREQS, HOLDS):
        r = bk[(bk.panel == p) & (bk.mech == m) & (bk.freq == f) & (bk.hold == H)].iloc[0]
        v2 = V2[p]
        kp.append(dict(panel=p, mech=m, freq=f, hold=H, CAGR=r.CAGR, Sharpe=r.Sharpe,
                       MaxDD=r.MaxDD, H1=r.H1, H2=r.H2, turn_yr=r.turn_yr,
                       OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                       pass4b=bool(r.pass4b),
                       pass4a=bool(r.H1 > v2["H1"] and r.H2 > v2["H2"]
                                   and r.MaxDD >= v2["MaxDD"])))
    KP = pd.DataFrame(kp)
    dump(KP, "keeppaths")
    P(f"  KEEP paths over all {len(KP)} (panel, mech, f, H) books at {COST:.0f} bps: "
      f"4b {int(KP.pass4b.sum())}, 4a {int(KP.pass4a.sum())}, "
      f"BOTH {int((KP.pass4b & KP.pass4a).sum())}")
    if int(KP.pass4a.sum()):
        for line in KP[KP.pass4a].to_string(index=False,
                                            float_format=lambda x: f"{x:.4f}").split("\n"):
            P("    " + line)
    P("")

    # ================================================================== (F) rule 8
    P("=" * 100)
    P("(F) RULE 8 WALK-FORWARD — the (f, H) point chosen on 2009-2016 ALONE, OOS read once")
    P("=" * 100)
    wf = []
    for p, m in product(PANELS, MECHS):
        s = bk[(bk.panel == p) & (bk.mech == m)]
        pan, v2 = PAN[p], V2[p]
        pick_s = s.loc[s.IS_Sharpe.idxmax()]
        legcnt = s.apply(lambda r: int(r.IS_Sharpe > pan["spy"]["IS_Sharpe"])
                         + int(abs(r.IS_MaxDD) <= DD_CAP * abs(pan["spy"]["IS_MaxDD"]))
                         + int(r.IS_CAGR >= CAGR_FLOOR * pan["spy"]["IS_CAGR"]), axis=1)
        pick_l = s.loc[(legcnt * 100 + s.IS_Sharpe).idxmax()]
        oos_best = s.loc[s.OOS_Sharpe.idxmax()]
        for ch, r in [("C_ISSHARPE", pick_s), ("C_ISLEGS", pick_l), ("C_DEFAULT_W0",
                      s[(s.freq == "W") & (s.hold == 0)].iloc[0])]:
            ol = legs_4b_oos(r, pan["spy"])
            wf.append(dict(panel=p, mech=m, chooser=ch, pick=f"{r.freq}/H{r.hold}",
                           oos_best=f"{oos_best.freq}/H{oos_best.hold}",
                           hit=bool(r.freq == oos_best.freq and r.hold == oos_best.hold),
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           spy_OOS_CAGR=pan["spy"]["OOS_CAGR"],
                           spy_OOS_Sharpe=pan["spy"]["OOS_Sharpe"],
                           spy_OOS_MaxDD=pan["spy"]["OOS_MaxDD"],
                           v2_OOS_CAGR=v2["OOS_CAGR"], v2_OOS_Sharpe=v2["OOS_Sharpe"],
                           v2_OOS_MaxDD=v2["OOS_MaxDD"],
                           CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                           turn_yr=r.turn_yr, **ol, pass4b=bool(r.pass4b),
                           pass4b_oos=all(ol.values()),
                           pass4a=bool(r.H1 > v2["H1"] and r.H2 > v2["H2"]
                                       and r.MaxDD >= v2["MaxDD"])))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    for line in WF[["panel", "mech", "chooser", "pick", "oos_best", "hit", "OOS_CAGR",
                    "OOS_Sharpe", "OOS_MaxDD", "v2_OOS_Sharpe", "spy_OOS_Sharpe", "pass4b",
                    "pass4b_oos", "pass4a"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)
    P("")

    # ================================================================== hypotheses
    H_ = {}
    u = TL[(TL.panel == "U56") & (TL.cost == COST)]
    base_h0 = u[u.hold == 0].set_index("freq").p90_Sharpe
    span_f = float(base_h0.max() - base_h0.min())
    w_row = u[u.freq == "W"].set_index("hold").p90_Sharpe
    span_h = float(w_row.max() - w_row.min())
    H_["H_HOLD"] = (span_h >= 0.5 * span_f,
                    f"at fixed f=W, walking H 0->126 moves the null's p90 Sharpe by at least half "
                    f"of what walking f D->Q at H=0 does: |dH| {span_h:.4f} vs |df| {span_f:.4f} "
                    f"(ratio {span_h/max(span_f,1e-9):.2f})")

    mm = PRS[(PRS.cost == COST) & (PRS.panel == "U56")] if len(PRS) else PRS
    H_["H_FREQ"] = (len(mm) > 0 and float(mm.d_p90.abs().median()) <= 0.10,
                    f"at MATCHED drag (turnover within 20%), cells with different f agree on the "
                    f"null's p90 Sharpe to within 0.10 (median): "
                    + (f"{len(mm)} pairs, median |d| {mm.d_p90.abs().median():.4f}, "
                       f"max {mm.d_p90.abs().max():.4f}" if len(mm) else "NO matched pairs exist"))

    d = DEC[(DEC.panel == "U56") & (DEC.cost == COST)].iloc[0]
    H_["H_TAIL"] = (d.eta2_logturn_q4 >= max(d.eta2_freq, d.eta2_hold),
                    f"the null's upper tail is ordered by realised DRAG rather than by either dial "
                    f"alone (U56, {COST:.0f} bps): eta2 log-turnover {d.eta2_logturn_q4:.4f} vs "
                    f"freq {d.eta2_freq:.4f} vs hold {d.eta2_hold:.4f}")

    z = TL[(TL.panel == "U56") & (TL.cost == 0.0)]
    zf = z[z.hold == 0].set_index("freq").L_DD
    zh = z[z.freq == "W"].set_index("hold").L_DD
    H_["H_LDD"] = (float(zh.max() - zh.min()) >= 0.20,
                   f"MIN HOLD moves the null's L_DD failure share by >=0.20 at ZERO cost (the "
                   f"refutable half of the declared arithmetic — holding a loser through a "
                   f"selloff is not a cost effect): W row over H {list(np.round(zh.values,3))} "
                   f"(span {zh.max()-zh.min():.3f}); f row at H=0 {list(np.round(zf.values,3))}")

    ws = WF[WF.chooser == "C_ISSHARPE"]
    dflt = WF[WF.chooser == "C_DEFAULT_W0"]
    H_["H_RULE8"] = (float(ws.OOS_Sharpe.mean()) > float(dflt.OOS_Sharpe.mean()),
                     f"the IS-chosen (f, H) beats the DEFAULT W/H=0 book out of sample: mean OOS "
                     f"Sharpe {ws.OOS_Sharpe.mean():.4f} vs {dflt.OOS_Sharpe.mean():.4f} "
                     f"(hit rate on the OOS-best cell {ws.hit.mean():.3f}; OOS 4b "
                     f"{ws.pass4b_oos.mean():.3f} vs {dflt.pass4b_oos.mean():.3f})")

    H_["H_BOOK"] = (bool((KP.pass4b & KP.pass4a).sum() > 0),
                    f"some (f, H) book clears BOTH KEEP paths at {COST:.0f} bps: 4b "
                    f"{int(KP.pass4b.sum())} of {len(KP)}, 4a {int(KP.pass4a.sum())}, BOTH "
                    f"{int((KP.pass4b & KP.pass4a).sum())}")

    P("=" * 100)
    P("HYPOTHESES")
    P("=" * 100)
    for k, (ok, msg) in H_.items():
        P(f"  {k:10s} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"HYPOTHESES: {sum(1 for v in H_.values() if v[0])} of {len(H_)} pass.")
    pd.DataFrame([dict(hypothesis=k, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                  for k, v in H_.items()]).to_csv(f"{OUT}.hypotheses.csv", index=False)
    pd.DataFrame([dict(gate=k, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                  for k, v in gates.items()]).to_csv(f"{OUT}.gates.csv", index=False)
    P("")
    P(f"Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

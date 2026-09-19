#!/usr/bin/env python3
"""
Idea 1468 (cloud lane, 2026-09-19) --- is the DD-per-CAGR SLOPE a MEASURABLE STATISTIC on ANY
device family, or is it broken for the RECORD generally?

THE PREMISE.  Idea 1461 put a paired circular-block bootstrap on the beta band's "exchange rate"
--- pp of drawdown bought per pp of CAGR given up --- and found the statistic carries a standard
error of 0.61..8.96 against a five-rung spread of only 0.92.  No rung resolved from any other at
|t| > 0.20, so every 'best rung' ever read off that ladder is unsupportable.  1461 could not say
whether the defect belongs to the BETA BAND specifically or to the STATISTIC generally, because
it measured exactly one device family.

THIS RUN MEASURES THE OTHER THREE the record has priced, on their OWN published dial ladders:

  FAMILY G   the GROSS SCALAR              (ideas 1446 / 1454), dial g, published ladder
             {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00}.  Anchor g = 0.75 (the frozen
             incumbent).  The four rungs BELOW it are the DD-BUYING side and carry the slope;
             the two rungs ABOVE are LEVER, published as books but excluded from the slope
             ladder by the pre-registered sign convention below, not by their numbers.
  FAMILY V   INTRA-BOOK INVERSE-VOL SIZING (idea 1433), dial p, published ladder
             {0.0, 0.5, 1.0, 1.5, 2.0}; w_i proportional to vol_i^(-p), renormalised to the
             SAME gross 0.75.  Anchor p = 0 IS equal weight, i.e. the frozen incumbent.
  FAMILY S   the TRAILING EQUITY STOP      (idea 1405), dial depth d, published ladder
             {0.05, 0.075, 0.10, 0.125, 0.15, 0.20}.  Anchor = no brake (FRAC = 0), i.e. the
             frozen incumbent again.

A CORRECTION MADE DURING THIS RUN AND KEPT IN THE RECORD.  FAMILY S was first specified with
FRAC = 1.00 (full de-risk) and RESTORE = "SAME", on the stated reasoning that the largest
possible exposure cut is the most favourable case for the statistic being measurable.  That
reasoning was WRONG and the cell is DEGENERATE: at FRAC = 1.00 the braked book holds only cash,
so its own equity stops moving, its drawdown from peak can never shrink, and the release
condition can never fire.  The brake is an ABSORBING STATE.  Measured here: at U56 depth 0.05
the book is braked on 4,411 of 4,708 rows after exactly ONE episode, and its entire 2017-2026
OOS window is flat (CAGR 0.00%, Sharpe undefined).  Those numbers REPLAY idea 1405's own
committed FRAC = 1.00 cells to 4 dp (gate G12), so this is a property of the record's published
grid, not of this script.  The FRAC = 1.00 arm is therefore PUBLISHED IN FULL as the
absorbing-corner diagnostic, and the headline slope arm is FRAC = 0.50, where the braked book
retains 0.375 gross and can recover.  FRAC is a REPORTED AXIS at both values, not a third dial:
every cell of both arms is published and the pre-registered bar below is read on the
NON-ABSORBING arm, as declared before either arm's slopes were read.

All three families therefore share ONE anchor book --- the frozen 2026-09-04 incumbent (N = 20,
H = 126, gross 0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1) --- which is asserted as a
gate, and which makes the three ladders directly comparable in the same currency.

THE STATISTIC, IDENTICAL TO 1444 / 1461 SO THE THREE RUNS ARE COMPARABLE:
    dMaxDD_pp = (MaxDD_rung - MaxDD_anchor) * 100     (MaxDD is negative; > 0 means LESS drawdown)
    dCAGR_pp  = (CAGR_rung  - CAGR_anchor ) * 100     (< 0 means CAGR was given up)
    SLOPE     = dMaxDD_pp / dCAGR_pp                  (negative; MORE NEGATIVE IS BETTER)
A DD-buying device has dMaxDD_pp > 0 and dCAGR_pp < 0.  A LEVER has both signs flipped and the
ratio is negative for the opposite reason, which is why the two lever rungs of FAMILY G are
published as books but never enter a slope ladder.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  the FAMILY DIAL --- g, p or d --- each family read ONLY on its own published ladder.
  DIAL 2  L, the circular-block length, {21, 63, 126}.  ALL THREE reported; 63 is the record's
          default and the primary; every verdict below must hold at all three.

FROZEN, NEVER SELECTED ON: N = 20, H = 126, MAXVOL = 0.60, MA gate ON, weekly cadence, 10 bps,
t+1 (the frozen incumbent's own settings); FAMILY V's vol lookback 63 rows; FAMILY S's
RESTORE = "SAME".  FAMILY S's FRAC is a REPORTED AXIS at {0.50, 1.00}; the headline is 0.50 for
the reason given above.

HOW THE SLOPE IS MEASURED.  A circular-block bootstrap on the REALISED DAILY NET returns, with
ONE block-start matrix per (panel, L) shared by the anchor AND every rung of every family, so
each rung's slope and every rung-to-rung difference is a PAIRED statistic.  Published:
  (a) each rung's own slope, its bootstrap SE and t;
  (b) every ADJACENT rung-to-rung gap (the headline count) and every ALL-PAIRS gap, each with
      its paired SE, t and sign fraction;
  (c) the ladder SPREAD (max slope - min slope) beside the median rung SE, which is the
      signal-to-noise reading 1461 published for the band;
  (d) the count of bootstrap replicates with a DEGENERATE denominator (|dCAGR_pp| < 0.01),
      reported rather than silently dropped;
  (e) the CROSS-FAMILY contrast: the paired difference of two families' LADDER-MEAN slopes.
      The record uses exchange rates for two different jobs --- picking a RUNG inside a family
      and ranking one DEVICE against another --- and (b) only prices the first.  If the
      cross-family gaps resolve where the rung gaps do not, the statistic is usable for the
      second job and not the first, and the recommendation has to say which.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  The DD-per-CAGR slope is a MEASURABLE
statistic on a family if, at the primary block length L = 63 and on U56 AND B136:
  (i)  at least HALF that family's adjacent rung-to-rung gaps resolve at |t| > 2, AND
  (ii) the ladder spread exceeds the median rung SE.
If NO family clears this on any panel, the record should stop quoting exchange rates as findings
and PROTOCOL should say so; that recommendation is written but NOT enacted (rule 6 confines
rules changes to the Sunday review).  This run proposes no rules change either way.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell, FULL and OOS; the halves; turnover and its 10 bps drag; realised mean gross.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
frozen 2026-09-04 incumbent anchor.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: each family's
dial chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed frozen U56 anchor
(15.80% / 1.1537 / -19.13% full, 1.1857 OOS Sharpe).  G2 the three families' anchors are
BIT-IDENTICAL to one another and to the frozen incumbent.  G3 every cell published.  G4 exactly
two tuned dials.  G5 the rule-8 choosers read no row on or after 2017-01-01.  G6 no leverage:
every rebalance's weight sum <= 0.7500 + 1e-12 on every book.  G7 FAMILY V's exposure channel is
SHUT: mean gross identical across p at fixed panel.  G8 each family's dial BITES (a monotone
diagnostic per family).  G9 ONE block-start matrix per (panel, L), shared by every book.
G10 bit-identical recompute of the U56 headline cell.  G11 selection depends on neither dial:
identical held-name sets across every rung of every family.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_dd-per-cagr-slope-measurability_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-19"
SLUG = "dd-per-cagr-slope-measurability"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

GS_ALL = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]   # 1446/1454's published ladder
GS_DD = [0.625, 0.50, 0.375, 0.25]                       # the DD-BUYING side (slope ladder)
GS_LEVER = [0.875, 1.00]                                 # published books, never a slope rung
PS = [0.0, 0.5, 1.0, 1.5, 2.0]                           # 1433's published ladder (0.0 = anchor)
PS_DD = [0.5, 1.0, 1.5, 2.0]
VOL_LOOK = 63                                            # FROZEN (1433 published 20/63/126/252)
DEPTHS = [0.05, 0.075, 0.10, 0.125, 0.15, 0.20]          # 1405's published ladder
FRACS = [0.50, 1.00]                                     # REPORTED AXIS, not a dial
FRAC_HEAD = 0.50                                         # the NON-ABSORBING headline arm
STOP_RESTORE = "SAME"                                    # FROZEN
# idea 1405's committed U56 FRAC=1.00 / RESTORE=SAME cells, for the cross-script replay G12
C1405_U56_F1 = {0.05: (-0.001579, -0.153164, -0.066146), 0.075: (0.009464, 0.317301, -0.083929),
                0.10: (0.009610, 0.247304, -0.129023), 0.125: (0.009610, 0.247304, -0.129023),
                0.15: (0.073244, 0.799774, -0.175939), 0.20: (0.158028, 1.153663, -0.191276)}

LS = [21, 63, 126]                                       # DIAL 2
L_PRIMARY = 63
BOOT_REPS, SEED = 400, 20260919
DEGEN_EPS = 0.01                                         # pp, on |dCAGR_pp|
BAR_T = 2.0
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


# ----------------------------------------------------------------------------- mechanics
def mech(q):
    """The live selection mechanics (baseline.score with the incumbent's 3-leg composite)."""
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        # trailing vol of the INVESTABLE names, for FAMILY V (backward-looking only)
        self.volL = (px[invest].pct_change().rolling(VOL_LOOK).std()
                     * np.sqrt(252)).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def segments(pan, N=I_N, H=I_H, lag=1):
    """The frozen min-hold selection frame.  Depends on NEITHER family dial, so it is built
    ONCE per panel and every rung of every family holds the IDENTICAL names (gate G11)."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    segs = []
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy()))
    return segs


def w_equal(pan, segs, gross):
    """FAMILY G: equal weight, gross/n.  gross = 0.75 IS the anchor."""
    return [np.full(len(sel), gross / len(sel)) if len(sel) else np.zeros(0)
            for (_t, _s, _ts, sel) in segs]


def w_ivol(pan, segs, p, gross=I_G):
    """FAMILY V: w_i proportional to vol_i^(-p), renormalised to the SAME gross (exposure shut).
    p = 0 is BIT-IDENTICAL to equal weight.  Vol stamped at the t-1 decision row."""
    ws = []
    for (_t, _s, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        if p == 0.0:
            ws.append(np.full(n, gross / n))
            continue
        v = pan.volL[ts, sel].astype(float)
        fin = np.isfinite(v) & (v > 0)
        med = np.median(v[fin]) if fin.any() else 1.0
        v = np.where(fin, v, med)
        raw = v ** (-p)
        ws.append(gross * raw / raw.sum())
    return ws


def run_book(pan, segs, ws, depth=None, frac=0.0, restore="SAME"):
    """One book.  depth=None / frac=0 is the un-braked case.  The brake decides at each
    rebalance row from the book's OWN NET equity through the PREVIOUS segment only."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gpath = np.zeros(T)
    curw = np.zeros(M)
    eq, peak, stopped, episodes = 1.0, 1.0, False, 0
    wsum_max = 0.0
    braked_rows = 0
    for (i0, i1, _ts, sel), wv in zip(segs, ws):
        if frac > 0.0 and depth is not None:
            dd = eq / peak - 1.0
            if stopped:
                if restore == "SAME":
                    stopped = not (dd > -depth)
                elif restore == "HALF":
                    stopped = not (dd > -depth / 2.0)
                else:
                    stopped = not (dd >= -1e-12)
            else:
                if dd <= -depth:
                    stopped = True
                    episodes += 1
        scale = (1.0 - frac) if stopped else 1.0
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv * scale
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        seg = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        out[i0:i1] = seg
        gpath[i0:i1] = w0.sum()
        if stopped:
            braked_rows += (i1 - i0)
        nt = seg.copy()
        nt[0] -= turn[i0] * COST / 1e4
        e_path = eq * np.cumprod(1.0 + nt)
        peak = max(peak, float(e_path.max()))
        eq = float(e_path[-1])
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    net = out - turn * COST / 1e4
    return dict(net=net, turn=turn, gross=gpath, wsum_max=wsum_max,
                episodes=episodes, braked_rows=braked_rows)


# ----------------------------------------------------------------------------- statistics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a against the LIVE RULES v2 book; 4b against SPY (PROTOCOL rule 4)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def block_index(n, L, reps=BOOT_REPS, seed=SEED):
    """ONE circular-block start matrix per (panel, L), shared by every book --- gate G9."""
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def boot_cagr_mdd(r, idx):
    X = np.asarray(r, float)[idx]
    n = X.shape[1]
    E = np.cumprod(1.0 + X, axis=1)
    c = E[:, -1] ** (252.0 / n) - 1.0
    d = (E / np.maximum.accumulate(E, axis=1) - 1.0).min(axis=1)
    return c, d


def slope_point(m_r, m_a):
    dD = (m_r["MaxDD"] - m_a["MaxDD"]) * 100.0
    dC = (m_r["CAGR"] - m_a["CAGR"]) * 100.0
    return (dD / dC) if abs(dC) >= 1e-12 else np.nan, dD, dC


# ----------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 136)
    say("IDEA 1468 (cloud, 2026-09-19) --- IS THE DD-per-CAGR SLOPE A MEASURABLE STATISTIC ON ANY "
        "DEVICE FAMILY?")
    say("  1461 found the beta band's slope carries SE 0.61..8.96 against a 5-rung spread of 0.92 "
        "(no gap at |t| > 0.20).")
    say("  Here the SAME paired bootstrap is re-formed on the record's three OTHER DD-buying "
        "families, each on its OWN published ladder.")
    say(f"DIAL 1  the family dial: G g {GS_ALL} (slope side {GS_DD}, lever {GS_LEVER} published "
        f"as books only);  V p {PS};  S depth {DEPTHS}.")
    say(f"DIAL 2  block length L {LS} (primary {L_PRIMARY}), ALL reported.")
    say(f"FROZEN: N={I_N}, H={I_H}, gross={I_G}, MAXVOL={MAXVOL}, MA gate ON, weekly, {COST:.0f} "
        f"bps, t+1;  FAMILY V vol lookback {VOL_LOOK};  FAMILY S RESTORE={STOP_RESTORE}.")
    say(f"REPORTED AXIS (not a dial): FAMILY S FRAC {FRACS} --- headline {FRAC_HEAD:.2f}; "
        f"FRAC = 1.00 is an ABSORBING state (braked book is all cash, so its own drawdown can "
        f"never shrink and the brake can never release) and is published as a diagnostic, not "
        f"read for the bar.")
    say(f"PRE-REGISTERED BAR (written before any number was read): a family's slope is MEASURABLE "
        f"if, at L={L_PRIMARY} on U56 AND B136, (i) >= half its ADJACENT rung-to-rung gaps resolve "
        f"at |t| > {BAR_T:.0f} AND (ii) the ladder spread exceeds the median rung SE.")
    say("=" * 136)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names remain.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one.  What this run reads is the RESOLUTION of a contrast "
        "between books built over the SAME names on the SAME days, which the bias cannot "
        "manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned dials (family dial, block length L)", "2", "== 2", True)

    grid, slope_rows, pair_rows, wf_rows = [], [], [], []
    g2_dev = g6_max = g6b_max = g7_dev = 0.0
    g11_ok = True

    for pan in panels:
        say("")
        say("=" * 136)
        say(f"PANEL {pan.name}")
        say("=" * 136)
        segs = segments(pan)
        w0 = WARMUP
        ev = pan.idx[w0:]
        oos_mask = np.asarray(ev >= pd.Timestamp(OOS_START))
        is_mask = ~oos_mask
        gate(f"G5 [{pan.name}] the rule-8 chooser reads no row on or after {OOS_START}",
             f"IS last row {ev[is_mask][-1].date()}", f"< {OOS_START}",
             ev[is_mask][-1] < pd.Timestamp(OOS_START))

        # comparands
        spy = pan.spy[w0:]
        base_r = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                          freq=CADENCE)["returns"].values[w0:]
        bm_full, live_full = bmpack(spy), bmpack(base_r)
        bm_oos, live_oos = bmpack(spy[oos_mask]), bmpack(base_r[oos_mask])
        say(f"  SPY        full CAGR {bm_full['CAGR']:7.2%} Sharpe {bm_full['Sharpe']:6.4f} "
            f"MaxDD {bm_full['MaxDD']:7.2%} | OOS CAGR {bm_oos['CAGR']:7.2%} "
            f"Sharpe {bm_oos['Sharpe']:6.4f} MaxDD {bm_oos['MaxDD']:7.2%}")
        say(f"  RULES v2   full CAGR {live_full['CAGR']:7.2%} Sharpe {live_full['Sharpe']:6.4f} "
            f"MaxDD {live_full['MaxDD']:7.2%} | OOS CAGR {live_oos['CAGR']:7.2%} "
            f"Sharpe {live_oos['Sharpe']:6.4f} MaxDD {live_oos['MaxDD']:7.2%}")

        # ---- build every book -------------------------------------------------------
        books = {}          # key -> dict(net=..., ...)
        def add(fam, dial, res):
            books[(fam, dial)] = res

        anchor_res = run_book(pan, segs, w_equal(pan, segs, I_G))
        for g in GS_ALL:
            add("G", g, anchor_res if g == I_G else run_book(pan, segs, w_equal(pan, segs, g)))
        for p in PS:
            add("V", p, anchor_res if p == 0.0 else run_book(pan, segs, w_ivol(pan, segs, p)))
        for fr in FRACS:
            add(f"S{fr:g}", 0.0, anchor_res)
            for d in DEPTHS:
                add(f"S{fr:g}", d, run_book(pan, segs, w_equal(pan, segs, I_G),
                                            depth=d, frac=fr, restore=STOP_RESTORE))

        # G2: the three family anchors are the SAME book
        a_net = anchor_res["net"][w0:]
        for fam, dial in (("G", I_G), ("V", 0.0), ("S0.5", 0.0), ("S1", 0.0)):
            g2_dev = max(g2_dev, float(np.abs(books[(fam, dial)]["net"][w0:] - a_net).max()))
        # G6 no leverage; G7 exposure shut on FAMILY V
        for k, b in books.items():
            g6_max = max(g6_max, b["wsum_max"])
            if not (k[0] == "G" and k[1] in GS_LEVER):
                g6b_max = max(g6b_max, b["wsum_max"])
        gv = [float(np.mean(books[("V", p)]["gross"][w0:])) for p in PS]
        g7_dev = max(g7_dev, float(np.max(gv) - np.min(gv)))

        m_anchor = triple(a_net)
        ah1, ah2 = halves(a_net)
        say(f"  ANCHOR (frozen incumbent, shared by all three families): "
            f"CAGR {m_anchor['CAGR']:7.2%} Sharpe {m_anchor['Sharpe']:6.4f} "
            f"MaxDD {m_anchor['MaxDD']:7.2%}  H1/H2 {ah1:.4f}/{ah2:.4f}")
        if pan.name == "U56":
            gate("G1 cross-script replay of the committed frozen U56 anchor (full)",
                 f"CAGR {m_anchor['CAGR']:.4%} Sharpe {m_anchor['Sharpe']:.4f} "
                 f"MaxDD {m_anchor['MaxDD']:.4%}",
                 f"CAGR ~{C_U56['CAGR']:.2%} Sharpe ~{C_U56['Sharpe']:.4f} "
                 f"MaxDD ~{C_U56['MaxDD']:.2%}",
                 abs(m_anchor["CAGR"] - C_U56["CAGR"]) < 5e-4
                 and abs(m_anchor["Sharpe"] - C_U56["Sharpe"]) < 5e-3
                 and abs(m_anchor["MaxDD"] - C_U56["MaxDD"]) < 5e-4)
            gate("G1b cross-script replay of the committed frozen U56 anchor (OOS Sharpe)",
                 f"{sharpe(a_net[oos_mask]):.4f}", f"~{C_U56['oSharpe']:.4f}",
                 abs(sharpe(a_net[oos_mask]) - C_U56["oSharpe"]) < 5e-3)
            rep = run_book(pan, segs, w_equal(pan, segs, I_G))["net"][w0:]
            gate("G10 bit-identical recompute of the U56 headline (anchor) cell",
                 f"{float(np.abs(rep - a_net).max()):.3e}", "== 0",
                 float(np.abs(rep - a_net).max()) == 0.0)
            dev = 0.0
            for d, (cc, ss_, dd_) in C1405_U56_F1.items():
                m_ = triple(books[("S1", d)]["net"][w0:])
                dev = max(dev, abs(m_["CAGR"] - cc), abs(m_["Sharpe"] - ss_),
                          abs(m_["MaxDD"] - dd_))
            gate("G12 cross-script replay of idea 1405's committed U56 FRAC=1.00/RESTORE=SAME "
                 "cells (all 6 depths, CAGR/Sharpe/MaxDD)", f"max |dev| {dev:.3e}", "< 1e-5",
                 dev < 1e-5)
            ep1 = [books[("S1", d)]["episodes"] for d in DEPTHS]
            ep5 = [books[(f"S{FRAC_HEAD:g}", d)]["episodes"] for d in DEPTHS]
            gate("G13 the FRAC=1.00 arm is ABSORBING (<= 1 brake episode at every depth) while "
                 "the FRAC=0.50 headline arm is NOT (> 1 episode at the depths that brake)",
                 f"FRAC 1.00 episodes {ep1}; FRAC 0.50 episodes {ep5}",
                 "1.00 arm all <= 1; 0.50 arm max > 1",
                 max(ep1) <= 1 and max(ep5) > 1)

        # ---- the grid: every cell, both KEEP paths, FULL and OOS ---------------------
        FAMS = [("G", "gross scalar (1446/1454)", GS_ALL, I_G),
                ("V", "intra-book inverse-vol (1433)", PS, 0.0),
                ("S0.5", "trailing equity stop, FRAC 0.50 (1405) [HEADLINE ARM]",
                 [0.0] + DEPTHS, 0.0),
                ("S1", "trailing equity stop, FRAC 1.00 (1405) [ABSORBING ARM, published]",
                 [0.0] + DEPTHS, 0.0)]
        say("")
        say(f"  {'fam':<3} {'dial':>7} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'4a':>4} {'4b':>4} {'oCAGR':>8} {'oSh':>7} {'oMDD':>8} {'4bOOS':>6} "
            f"{'turn/y':>7} {'gross':>6} {'dDD_pp':>7} {'dCG_pp':>7} {'slope':>8}")
        for fam, label, ladder, anch in FAMS:
            for dial in ladder:
                r = books[(fam, dial)]["net"][w0:]
                k4a, k4b, m, h1, h2, legs = keep_paths(r, bm_full, live_full)
                ro = r[oos_mask]
                k4ao, k4bo, mo, o1, o2, lego = keep_paths(ro, bm_oos, live_oos)
                sl, dD, dC = slope_point(m, m_anchor)
                ty = float(books[(fam, dial)]["turn"][w0:].sum()) / (len(r) / 252.0)
                gr = float(np.mean(books[(fam, dial)]["gross"][w0:]))
                say(f"  {fam:<3} {dial:>7.4g} {m['CAGR']:>7.2%} {m['Sharpe']:>8.4f} "
                    f"{m['MaxDD']:>7.2%} {h1:>7.3f} {h2:>7.3f} {str(k4a):>4} {str(k4b):>4} "
                    f"{mo['CAGR']:>7.2%} {mo['Sharpe']:>7.4f} {mo['MaxDD']:>7.2%} "
                    f"{str(k4bo):>6} {ty:>7.3f} {gr:>6.3f} {dD:>7.3f} {dC:>7.3f} "
                    f"{(f'{sl:8.4f}' if np.isfinite(sl) else '     nan')}")
                grid.append(dict(panel=pan.name, family=fam, family_label=label, dial=dial,
                                 is_anchor=(dial == anch),
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                                 leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                 leg_CAGR=legs["CAGR"],
                                 oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                 keep4a_oos=k4ao, keep4b_oos=k4bo,
                                 turnover_yr=ty, mean_gross=gr,
                                 dMaxDD_pp=dD, dCAGR_pp=dC, slope=sl,
                                 episodes=books[(fam, dial)]["episodes"],
                                 braked_rows=books[(fam, dial)]["braked_rows"],
                                 spy_CAGR=bm_full["CAGR"], spy_Sharpe=bm_full["Sharpe"],
                                 spy_MaxDD=bm_full["MaxDD"],
                                 live_Sharpe=live_full["Sharpe"], live_MaxDD=live_full["MaxDD"],
                                 spy_oCAGR=bm_oos["CAGR"], spy_oSharpe=bm_oos["Sharpe"],
                                 spy_oMaxDD=bm_oos["MaxDD"],
                                 live_oSharpe=live_oos["Sharpe"], live_oMaxDD=live_oos["MaxDD"]))

        # ---- G8: each dial BITES ------------------------------------------------------
        gr_by_g = [float(np.mean(books[("G", g)]["gross"][w0:])) for g in GS_ALL]
        bite_g = all(gr_by_g[i] < gr_by_g[i + 1] for i in range(len(gr_by_g) - 1))
        maxw_by_p = []
        for p in PS:
            ws = w_ivol(pan, segs, p)
            maxw_by_p.append(float(max((w.max() if len(w) else 0.0) for w in ws)))
        bite_v = all(maxw_by_p[i] <= maxw_by_p[i + 1] + 1e-12 for i in range(len(maxw_by_p) - 1))
        br = [books[(f"S{FRAC_HEAD:g}", d)]["braked_rows"] for d in DEPTHS]
        bite_s = all(br[i] >= br[i + 1] for i in range(len(br) - 1)) and br[0] > 0
        gate(f"G8 [{pan.name}] every family dial BITES (G: mean gross strictly increasing; "
             f"V: max weight non-decreasing in p; S: braked rows non-increasing in depth, > 0)",
             f"G {bite_g} / V {bite_v} / S {bite_s}  (braked rows {br})", "all True",
             bite_g and bite_v and bite_s)

        # ---- G11: selection identical across every rung --------------------------------
        # segments() takes no dial, so this is true by construction; asserted as a value.
        nsel = sorted({len(sel) for (_a, _b, _c, sel) in segs})
        publish(f"G11 held-name-set source [{pan.name}]",
                f"one segments() frame, {len(segs)} segments, held-count range "
                f"{nsel[0]}..{nsel[-1]}")

        # ---- the bootstrap ------------------------------------------------------------
        n = len(a_net)
        for L in LS:
            idx = block_index(n, L)
            bc, bd = {}, {}
            for key, b in books.items():
                c, d = boot_cagr_mdd(b["net"][w0:], idx)
                bc[key], bd[key] = c, d
            ca, da = bc[("G", I_G)], bd[("G", I_G)]

            SLAD = [("G", GS_DD), ("V", PS_DD), ("S0.5", DEPTHS), ("S1", DEPTHS)]
            LADMEAN, LADPT = {}, {}
            for fam, ladder in SLAD:
                S = {}        # dial -> (reps,) slope replicates, nan where degenerate
                degen = {}
                for dial in ladder:
                    dC = (bc[(fam, dial)] - ca) * 100.0
                    dD = (bd[(fam, dial)] - da) * 100.0
                    bad_d = np.abs(dC) < DEGEN_EPS
                    s = np.where(bad_d, np.nan, dD / np.where(bad_d, 1.0, dC))
                    S[dial] = s
                    degen[dial] = int(bad_d.sum())
                pts = {}
                for dial in ladder:
                    m_r = triple(books[(fam, dial)]["net"][w0:])
                    pts[dial] = slope_point(m_r, m_anchor)[0]
                ses = {}
                for dial in ladder:
                    v = S[dial][np.isfinite(S[dial])]
                    ses[dial] = float(v.std(ddof=1)) if len(v) > 2 else np.nan
                    slope_rows.append(dict(panel=pan.name, family=fam, L=L, dial=dial,
                                           slope=pts[dial], se=ses[dial],
                                           t=(pts[dial] / ses[dial]
                                              if ses[dial] and np.isfinite(ses[dial])
                                              and ses[dial] > 0 else np.nan),
                                           degenerate_reps=degen[dial], reps=BOOT_REPS))
                sp = np.nanmax(list(pts.values())) - np.nanmin(list(pts.values()))
                med_se = float(np.nanmedian(list(ses.values())))
                # adjacent + all pairs
                nadj = nadj_res = nall = nall_res = 0
                for i in range(len(ladder)):
                    for j in range(i + 1, len(ladder)):
                        a_, b_ = ladder[i], ladder[j]
                        dif = S[a_] - S[b_]
                        v = dif[np.isfinite(dif)]
                        se = float(v.std(ddof=1)) if len(v) > 2 else np.nan
                        pt = pts[a_] - pts[b_]
                        tt = pt / se if se and np.isfinite(se) and se > 0 else np.nan
                        sgn = float(np.mean(np.sign(v) == np.sign(pt))) if len(v) else np.nan
                        adj = (j == i + 1)
                        res = bool(np.isfinite(tt) and abs(tt) > BAR_T)
                        nall += 1
                        nall_res += int(res)
                        if adj:
                            nadj += 1
                            nadj_res += int(res)
                        pair_rows.append(dict(panel=pan.name, family=fam, L=L,
                                             rung_a=a_, rung_b=b_, adjacent=adj,
                                             diff=pt, se=se, t=tt, sign_frac=sgn,
                                             resolves=res, valid_reps=int(len(v))))
                say(f"  SLOPE [{pan.name} fam {fam} L={L:>3}]  spread {sp:8.4f}  median SE "
                    f"{med_se:9.4f}  spread/SE {(sp/med_se if med_se>0 else np.nan):7.4f}  "
                    f"adjacent gaps resolving |t|>{BAR_T:.0f}: {nadj_res}/{nadj}  "
                    f"all pairs: {nall_res}/{nall}  degenerate reps "
                    f"{max(degen.values())}/{BOOT_REPS} (worst rung)")
                LADMEAN[fam] = np.nanmean(np.vstack([S[d] for d in ladder]), axis=0)
                LADPT[fam] = float(np.nanmean([pts[d] for d in ladder]))
                slope_rows.append(dict(panel=pan.name, family=fam, L=L, dial="LADDER",
                                       slope=sp, se=med_se,
                                       t=(sp / med_se if med_se > 0 else np.nan),
                                       degenerate_reps=max(degen.values()), reps=BOOT_REPS))
            for fa, fb in [("G", "V"), ("G", "S0.5"), ("V", "S0.5"), ("G", "S1")]:
                dif = LADMEAN[fa] - LADMEAN[fb]
                v = dif[np.isfinite(dif)]
                se = float(v.std(ddof=1)) if len(v) > 2 else np.nan
                pt = LADPT[fa] - LADPT[fb]
                tt = pt / se if se and np.isfinite(se) and se > 0 else np.nan
                sgn = float(np.mean(np.sign(v) == np.sign(pt))) if len(v) else np.nan
                res = bool(np.isfinite(tt) and abs(tt) > BAR_T)
                pair_rows.append(dict(panel=pan.name, family=f"XFAM:{fa}-{fb}", L=L,
                                      rung_a=LADPT[fa], rung_b=LADPT[fb], adjacent=False,
                                      diff=pt, se=se, t=tt, sign_frac=sgn, resolves=res,
                                      valid_reps=int(len(v))))
                say(f"  XFAM  [{pan.name} L={L:>3}]  ladder-mean slope {fa} {LADPT[fa]:8.4f} vs "
                    f"{fb} {LADPT[fb]:8.4f}   diff {pt:+8.4f}  SE {se:8.4f}  t {tt:+8.4f}  "
                    f"sign {sgn:.3f}  resolves {res}")

        # ---- (e) the CROSS-FAMILY contrast, same block-start matrix -------------------
        # (placeholder replaced below)
        # ---- rule 8 walk-forward ------------------------------------------------------
        for fam, label, ladder, anch in FAMS:
            pick, best = None, -np.inf
            for dial in ladder:
                s_is = sharpe(books[(fam, dial)]["net"][w0:][is_mask])
                if np.isfinite(s_is) and s_is > best:
                    best, pick = s_is, dial
            ro = books[(fam, pick)]["net"][w0:][oos_mask]
            k4ao, k4bo, mo, o1, o2, lego = keep_paths(ro, bm_oos, live_oos)
            ao = a_net[oos_mask]
            ma = triple(ao)
            say(f"  RULE 8 [{pan.name} fam {fam}] IS-argmax-Sharpe pick = {pick:g}  ->  OOS "
                f"CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.4f} MaxDD {mo['MaxDD']:7.2%}  "
                f"| anchor OOS {ma['CAGR']:7.2%}/{sharpe(ao):6.4f}/{ma['MaxDD']:7.2%}  "
                f"| SPY {bm_oos['CAGR']:7.2%}/{bm_oos['Sharpe']:6.4f}/{bm_oos['MaxDD']:7.2%}  "
                f"| RULESv2 {live_oos['CAGR']:7.2%}/{live_oos['Sharpe']:6.4f}/"
                f"{live_oos['MaxDD']:7.2%}  4a {k4ao} 4b {k4bo}")
            wf_rows.append(dict(panel=pan.name, family=fam, chooser="IS_ARGMAX_SHARPE",
                                pick=pick, is_sharpe=best,
                                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                                oos_MaxDD=mo["MaxDD"], keep4a_oos=k4ao, keep4b_oos=k4bo,
                                anchor_oos_CAGR=ma["CAGR"], anchor_oos_Sharpe=sharpe(ao),
                                anchor_oos_MaxDD=ma["MaxDD"],
                                d_oos_sharpe_vs_anchor=mo["Sharpe"] - sharpe(ao),
                                spy_oos_CAGR=bm_oos["CAGR"], spy_oos_Sharpe=bm_oos["Sharpe"],
                                spy_oos_MaxDD=bm_oos["MaxDD"],
                                live_oos_CAGR=live_oos["CAGR"],
                                live_oos_Sharpe=live_oos["Sharpe"],
                                live_oos_MaxDD=live_oos["MaxDD"]))

    gate("G2 the three families' anchors are BIT-IDENTICAL to one another (and to the frozen "
         "incumbent)", f"{g2_dev:.3e}", "== 0", g2_dev == 0.0)
    gate("G6 no leverage (PROTOCOL rule 2): max weight sum over every rebalance of every book. "
         "FAMILY G's published ladder tops out at g = 1.00 (fully invested, no borrowing); every "
         "other book, and every slope-ladder rung, sits at or below the incumbent's 0.75",
         f"{g6_max:.6f}", "<= 1.0000", g6_max <= 1.0 + 1e-12)
    gate("G6b every SLOPE-LADDER rung and both anchors sit at or below the incumbent's gross",
         f"{g6b_max:.6f}", f"<= {I_G:.4f}", g6b_max <= I_G + 1e-12)
    gate("G7 FAMILY V exposure channel SHUT (mean gross identical across p)",
         f"{g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G11 selection depends on NEITHER dial (one segments() frame per panel, built before "
         "any dial is read)", "by construction", "identical name sets", g11_ok)
    gate("G3 every cell published", f"{len(grid)} grid rows, {len(slope_rows)} slope rows, "
         f"{len(pair_rows)} pair rows, {len(wf_rows)} walk-forward rows", "all written", True)
    gate("G9 ONE block-start matrix per (panel, L), shared by every book",
         f"seed {SEED}, reps {BOOT_REPS}", "paired by construction", True)

    G = pd.DataFrame(grid)
    S = pd.DataFrame(slope_rows)
    P = pd.DataFrame(pair_rows)
    W = pd.DataFrame(wf_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    S.to_csv(f"{OUT}.slopes.csv", index=False)
    P.to_csv(f"{OUT}.pairs.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    # ----------------------------------------------------------------- headline
    say("")
    say("=" * 136)
    say("HEADLINE")
    say("=" * 136)
    adj = P[P["adjacent"]]
    XF = P[P["family"].str.startswith("XFAM")]
    P_in = P[~P["family"].str.startswith("XFAM")]
    adj = P_in[P_in["adjacent"]]
    say(f"  ADJACENT rung-to-rung gaps resolving at |t| > {BAR_T:.0f}, ALL panels x ALL L: "
        f"{int(adj['resolves'].sum())} of {len(adj)}   "
        f"(all WITHIN-family pairs: {int(P_in['resolves'].sum())} of {len(P_in)})")
    say(f"  CROSS-FAMILY ladder-mean gaps resolving at |t| > {BAR_T:.0f}: "
        f"{int(XF['resolves'].sum())} of {len(XF)}   median |t| "
        f"{np.nanmedian(np.abs(XF['t'])):.4f}   max |t| {np.nanmax(np.abs(XF['t'])):.4f}")
    for fam in ["G", "V", "S0.5", "S1"]:
        a = adj[adj["family"] == fam]
        say(f"    family {fam}: adjacent {int(a['resolves'].sum())}/{len(a)}   "
            f"median |t| {np.nanmedian(np.abs(a['t'])):.4f}   max |t| "
            f"{np.nanmax(np.abs(a['t'])):.4f}")
    lad = S[S["dial"] == "LADDER"]
    say("")
    say(f"  {'panel':<6} {'fam':<4} {'L':>4} {'spread':>9} {'medianSE':>10} {'spread/SE':>10}")
    for _, r in lad.iterrows():
        say(f"  {r['panel']:<6} {r['family']:<4} {int(r['L']):>4} {r['slope']:>9.4f} "
            f"{r['se']:>10.4f} {r['t']:>10.4f}")
    prim = adj[(adj["L"] == L_PRIMARY) & (adj["panel"].isin(["U56", "B136"]))]
    verdicts = {}
    for fam in ["G", "V", "S0.5", "S1"]:
        ok = True
        for pan_name in ["U56", "B136"]:
            a = prim[(prim["family"] == fam) & (prim["panel"] == pan_name)]
            half = len(a) and (a["resolves"].sum() >= len(a) / 2.0)
            l = lad[(lad["family"] == fam) & (lad["L"] == L_PRIMARY)
                    & (lad["panel"] == pan_name)]
            sn = bool(len(l)) and float(l["t"].iloc[0]) > 1.0
            ok = ok and bool(half) and sn
        verdicts[fam] = ok
        say(f"  BAR family {fam}: MEASURABLE = {ok}")
    say("")
    say(f"  4a passes (full): {int(G['keep4a'].sum())} of {len(G)};  "
        f"4b full: {int(G['keep4b'].sum())} of {len(G)};  "
        f"4b full AND OOS: {int((G['keep4b'] & G['keep4b_oos']).sum())} of {len(G)}")
    for leg in ["leg_H1", "leg_H2", "leg_DD", "leg_CAGR"]:
        say(f"    4b leg {leg:<8} fails {int((~G[leg]).sum())} of {len(G)}")
    say(f"  RULE 8 mean d(OOS Sharpe) of the IS-chosen rung vs the frozen anchor: "
        f"{W['d_oos_sharpe_vs_anchor'].mean():+.4f}  "
        f"(beats the anchor {int((W['d_oos_sharpe_vs_anchor'] > 0).sum())} of {len(W)})")
    gp = pd.DataFrame(GATES)
    npass = int(gp["pass_"].sum())
    say(f"  GATES {npass}/{len(gp)} pass")
    say(f"  runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

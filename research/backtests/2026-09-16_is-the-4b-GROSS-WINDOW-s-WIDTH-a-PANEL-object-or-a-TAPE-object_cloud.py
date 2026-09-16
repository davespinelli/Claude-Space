#!/usr/bin/env python3
"""Idea 1152 (cloud lane, 2026-09-16)
   is-the-4b-GROSS-WINDOW-s-WIDTH-a-PANEL-object-or-a-TAPE-object

QUEUE PREMISE.  Idea 1150 walked gross on a 33-rung ladder (0.200..1.000 step 0.025) at
eight cost rungs and found 4b's pass set at 10 bps is a CONTIGUOUS WINDOW between two
opposed exposure legs rather than a peak: U56 0.525..0.775 (11 rungs), B136 0.500..0.725
(10 rungs).  So "4b passes" on that ladder is a statement about a BAND, and the band's
WIDTH is the natural statistic.  THE ASK: measure the width on the SMALL panel and on
SUB-TAPES, and say whether width is a PANEL property or a TAPE-LENGTH one.

TUNED DIALS (2, PROTOCOL rule 4 — the queue names both):
    DIAL 1  PANEL           {U56, B136, SMALL}
    DIAL 2  SUB-TAPE FRAC   f in {1, 2, 3, 4, 6} — the warm tape cut into f equal
                            contiguous stretches; every stretch is measured and published.
The GROSS LADDER is NOT a dial: it is the object being measured, and all 33 rungs are
published at every cell (.grid.csv).  COST is frozen at the PROTOCOL's 10 bps.  The TAPE
VARIANT {T_OWN, T_MATCHED} is a CONTROL, not a dial: T_MATCHED restricts EVERY panel to
the SMALL panel's own trading days so the three panels are matched in length row for row.
It is computed at every cell and never selected on.  PARTITION {ALIGNED, OFFSET} is a
control too (1157's construction), reported for the headline fraction ladder.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1150's construction: CAND20 legs
[(21,252),(0,126),(0,63)], cap INF, max_vol 0.60, min hold 126, N=20, W cadence, LAG 1,
warm-up 260, IS end 2016-12-31, zero-cash convention, 10 bps.  Gross is the ladder; panel
and sub-tape fraction are the two dials; nothing else moves.

THE WIDTH RULE, DECLARED BEFORE ANY NUMBER.  On a stretch, the 4b legs that are defined
WITHIN that stretch are the four CORE legs — L_H1, L_H2 (the stretch's own halves vs SPY
over the same days), L_DD (|dd| <= 0.60|SPY dd|), L_CAGR (CAGR >= 0.70*SPY CAGR).  The
fifth leg L_OOS needs the tape-wide 2016-12-31 split and exists only at f=1; the full
five-leg 4b is therefore reported AT f=1 ONLY and is what gate G6 reproduces against
1150's committed grid.  WIDTH = number of gross rungs of 33 whose CORE legs all pass.
SPAN = hi - lo in rungs; CONTIGUOUS iff WIDTH == SPAN + 1.  A stretch on which SPY's own
CAGR is <= 0 has a FLOOR THAT REWARDS LOSING (0.70 * a negative number); such stretches
are flagged `spy_down` and every headline is published both pooled and excluding them.

THE VERDICT RULE, DECLARED BEFORE ANY NUMBER.  Width is a PANEL object if the BETWEEN-PANEL
spread of width at MATCHED length exceeds the WITHIN-PANEL spread of width across the
equal-length stretches of one panel; a TAPE object if the reverse.  Both are medians over
the fraction ladder, on T_MATCHED, count-matched (1155's defect: a range grows with the
number of points it is taken over, so both terms use the same mean-absolute-pairwise-
difference statistic 1157 called MATCHED, never a max-minus-min).

Standalone, deterministic, offline.  Writes only research/backtests/<this stem>.* files.
SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are CURRENT-constituent lists and the SMALL
pool is the current output of a sub-$2B screen — every panel is survivorship-biased upward,
and the SMALL panel most of all.  Names with max_1d_move >= 1.0 in data/small_meta.csv are
dropped before anything is computed.
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-4b-GROSS-WINDOW-s-WIDTH-a-PANEL-object-or-a-TAPE-object"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_G = [round(0.20 + 0.025 * i, 3) for i in range(33)]   # 1150's ladder, verbatim
PANELS = ["U56", "B136", "SMALL"]
TAPES = ["T_OWN", "T_MATCHED"]
FRACS = [1, 2, 3, 4, 6]
HEAD_TAPE = "T_MATCHED"                                   # the length-matched reading
PARTITIONS = ["ALIGNED", "OFFSET"]
OFFSET_FRACS = (0.0, 1.0 / 3.0, 2.0 / 3.0)
CORE = ["L_H1", "L_H2", "L_DD", "L_CAGR"]
FIVE = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]

NSEED = 20                                                # gross-matched random-book null
SEED = 11521152
NPAIR = 200

# committed cross-run anchors, quoted and gated, never re-derived from memory
PRIOR1150 = BT / ("2026-09-16_is-the-CAGR-FLOOR-a-DE-GROSSING-DETECTOR-rather-than-a-"
                  "COST-LEG_C.grid.csv")
A936_WH126 = (0.155787, 1.139701, -0.191276)              # U56 W/H126/N=20, 10 bps
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
W1150 = {"U56": (0.525, 0.775, 11), "B136": (0.500, 0.725, 10)}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- 1082/1098/1150's fast runner, verbatim
def nrun(rets, wt, mk):
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


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1150's selection loop, verbatim.  Holdings do NOT depend on gross — it is a pure
    multiplier on the row — which is why the ladder costs one build per cell, not 33."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows_idx(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, ins=None, oos=None):
    c, s, d = fmet(r)
    h = len(r) // 2
    out = dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]))
    if ins is not None:
        ic, is_, idd = fmet(r[ins])
        oc, os_, od = fmet(r[oos])
        out.update(IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                   OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)
    return out


def legs_core(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def parts_at(n, f, partition):
    """1157's partition scheme, verbatim: index slices of the warm tape at fraction 1/f."""
    L = n // f
    if L < 3:
        return []
    if f == 1 or partition == "ALIGNED":
        return [(k * L, (k + 1) * L) for k in range(f)]
    out = []
    for o in OFFSET_FRACS:
        s = int(round(o * L))
        k = 0
        while s + (k + 1) * L <= n:
            out.append((s + k * L, s + (k + 1) * L))
            k += 1
    return out


def matched_spread(v, rng):
    """1157's MATCHED statistic: mean |difference| over random PAIRS.  Count-matched by
    construction, so it does not inflate with the number of points (1155's defect)."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    if len(v) == 2:
        return float(abs(v[0] - v[1]))
    i = rng.integers(0, len(v), size=(NPAIR, 2))
    i = i[i[:, 0] != i[:, 1]]
    return float(np.abs(v[i[:, 0]] - v[i[:, 1]]).mean())


def spearman(x, y):
    """Rank correlation without scipy (the sandbox has none): pearson of the ranks."""
    x = pd.Series(np.asarray(x, float)).rank()
    y = pd.Series(np.asarray(y, float)).rank()
    if x.std(ddof=1) == 0 or y.std(ddof=1) == 0:
        return np.nan
    return float(x.corr(y))


def window_of(passes):
    """passes: bool array over LAD_G.  -> width, lo, hi, span, contiguous, n_gaps."""
    idx = np.flatnonzero(passes)
    if len(idx) == 0:
        return dict(width=0, lo=np.nan, hi=np.nan, span=np.nan, contiguous=True, n_gaps=0)
    lo, hi = int(idx[0]), int(idx[-1])
    span = hi - lo
    gaps = int(np.sum(np.diff(idx) > 1))
    return dict(width=int(len(idx)), lo=LAD_G[lo], hi=LAD_G[hi], span=span + 1,
                contiguous=bool(len(idx) == span + 1), n_gaps=gaps)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


def main():
    t0 = time.time()
    P(f"# Idea 1152 (cloud lane, {DATE}) — is the 4b GROSS WINDOW's WIDTH a PANEL object or a")
    P("#   TAPE object?  1150 found the 4b pass set on the 33-rung gross ladder is a CONTIGUOUS")
    P("#   WINDOW (U56 0.525..0.775 = 11 rungs; B136 0.500..0.725 = 10) rather than a peak.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): PANEL {PANELS} x SUB-TAPE FRACTION {FRACS}.")
    P(f"#   The {len(LAD_G)}-rung GROSS ladder {LAD_G[0]}..{LAD_G[-1]} step 0.025 is the OBJECT, not a dial:")
    P("#   every rung is published at every cell.  COST frozen at the PROTOCOL's 10 bps.")
    P(f"#   CONTROLS, never selected on: TAPE {TAPES} (T_MATCHED restricts EVERY panel to the")
    P(f"#   SMALL panel's own trading days) and PARTITION {PARTITIONS}.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, min hold {HOLD0}, N {N0},")
    P(f"#   cadence {FREQ0}, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, zero cash, {NSEED} null seeds.")
    P("#")
    P("# THE WIDTH RULE, DECLARED BEFORE ANY NUMBER: on a stretch only the FOUR CORE legs are")
    P("#   defined (L_H1, L_H2 on the stretch's own halves vs SPY over the same days; L_DD")
    P("#   |dd| <= 0.60|SPY dd|; L_CAGR CAGR >= 0.70*SPY CAGR).  L_OOS needs the tape-wide")
    P("#   2016-12-31 split and exists at f=1 only, where the FULL five-leg 4b is also reported")
    P("#   and gated against 1150's committed grid (G6).  WIDTH = passing rungs of 33;")
    P("#   CONTIGUOUS iff WIDTH == hi-lo+1.  Stretches with SPY CAGR <= 0 have a floor that")
    P("#   REWARDS LOSING and are flagged `spy_down`; every headline is published both ways.")
    P("# THE VERDICT RULE, DECLARED BEFORE ANY NUMBER: PANEL object iff the BETWEEN-PANEL")
    P("#   matched spread of width at MATCHED length exceeds the WITHIN-PANEL matched spread")
    P("#   across equal-length stretches; TAPE object iff the reverse.  Both use 1157's")
    P("#   count-matched pairwise statistic, never a max-minus-min (1155's defect).")
    P("# SURVIVORSHIP (rule 9): all three panels are current-constituent lists; SMALL most of all.")
    P("")

    gaterows = []

    def gate(name, what, value, ok):
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}: {value:.4e}")

    # ------------------------------------------------------------------------- panels
    P("## PANELS — loaded and STAMPED before any result number")
    small, ndrop, nmeta = load_small()
    raw = {"U56": load_universe().dropna(how="all").ffill(),
           "B136": load_universe(broad=True).dropna(how="all").ffill(),
           "SMALL": small}
    SMALL_DAYS = raw["SMALL"].index

    def prep(px):
        idx = px.index
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows_idx(idx)
        sc, elig = mech(px)
        return dict(px=px, idx=idx, K=len(px.columns), T=len(idx), rets=rets, priced=priced,
                    warm=warm, ins=ins, oos=oos, sc=sc, elig=elig,
                    spy_i=list(px.columns).index("SPY"))

    cells = {}
    for tape in TAPES:
        for panel in PANELS:
            px = raw[panel]
            if tape == "T_MATCHED":
                px = px.loc[px.index.intersection(SMALL_DAYS)]
            d = prep(px)
            if panel == "SMALL":
                d["elig"] = d["elig"].copy()
                d["elig"][:, d["spy_i"]] = False        # SPY is the benchmark, not a holding
            cells[(tape, panel)] = d
            P(f"  {tape:<10s} {panel:<6s} {d['K']:4d} cols, {d['T']:,} rows "
              f"{d['idx'][0].date()} -> {d['idx'][-1].date()}  warm {d['warm'].sum():,}  "
              f"IS {d['ins'].sum():,}  OOS {d['oos'].sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {cells[('T_OWN','SMALL')]['K'] - 1} names + SPY as "
      f"benchmark; tape {SMALL_DAYS[0].date()} -> {SMALL_DAYS[-1].date()}.")
    P("")

    # ---------------------------------------------------------------- the ladder runner
    def ladder(tape, panel, rank_key=None):
        """Net daily returns of the CAND20 book at every gross rung.  One build, 33 rows."""
        d = cells[(tape, panel)]
        mk = rebalance_mask(d["idx"], FREQ0).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        key = -d["sc"] if rank_key is None else rank_key
        W1 = build(key, d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], 1.0)
        out = {}
        for g in LAD_G:
            W = W1 * g
            Wl = np.zeros_like(W)
            Wl[LAG:] = W[:-LAG]
            gr, tn = nrun(d["rets"], Wl, mkl)
            out[g] = gr - tn * COST / 1e4
        return out

    def rand_key(tape, panel, seed):
        """Gross-matched RANDOM-BOOK null: same N, H, cadence, gross and eligibility, but the
        rank is a fresh uniform draw at every row.  Holdings only, nothing else changes."""
        d = cells[(tape, panel)]
        return np.random.default_rng(seed).random((d["T"], d["K"]))

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = cells[("T_OWN", "U56")]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    lad_u56 = ladder("T_OWN", "U56")
    rfast = lad_u56[GROSS0]
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20, g=0.75)", v, v < 1e-12)
    m = blocks_m(rfast[d["warm"]], d["ins"][d["warm"]], d["oos"][d["warm"]])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple", v, v < 5e-5)
    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy[d["warm"]], d["ins"][d["warm"]], d["oos"][d["warm"]])
    v = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple (U56 own tape)", v, v < 5e-4)
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    v = abs(blocks_m(lb_r[d["warm"]])["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)
    v = float(np.abs(ladder("T_OWN", "SMALL")[GROSS0] - ladder("T_OWN", "SMALL")[GROSS0]).max())
    gate("G5", "determinism of the SMALL pipeline", v, v == 0.0)

    prior = pd.read_csv(PRIOR1150)
    P("     1150's COMMITTED 10 bps window, quoted VERBATIM FROM ITS OWN CSV (never re-derived "
      "from memory):")
    pr_win = {}
    for p in ("U56", "B136"):
        s = prior[(prior.panel == p) & (prior.cost_bps == 10.0)].sort_values("gross")
        w = s[s.pass_4b_full]
        pr_win[p] = (float(w.gross.min()), float(w.gross.max()), int(len(w)))
        P(f"       {p:<5s} {pr_win[p][0]:.3f} .. {pr_win[p][1]:.3f}  ({pr_win[p][2]} rungs of {len(s)})")
    okq = all(abs(pr_win[p][0] - W1150[p][0]) < 1e-9 and abs(pr_win[p][1] - W1150[p][1]) < 1e-9
              and pr_win[p][2] == W1150[p][2] for p in W1150)
    gate("G6a", "1150's committed grid is present and carries the quoted window",
         0.0 if okq else 1.0, okq)

    # ------------------- G6: the FIVE-leg window at f=1 reproduces 1150's, panel by panel
    P("")
    P("## ARM 0 — VERBATIM REPRODUCTION of 1150's five-leg 4b window at f=1 (T_OWN, 10 bps)")
    five_rows = []
    lads = {}
    for tape in TAPES:
        for panel in PANELS:
            lads[(tape, panel)] = lad_u56 if (tape, panel) == ("T_OWN", "U56") \
                else ladder(tape, panel)
            P(f"  built ladder {tape}/{panel}  ({time.time()-t0:.0f}s)")
    repro = {}
    for tape in TAPES:
        for panel in PANELS:
            dd_ = cells[(tape, panel)]
            warm, ins, oos = dd_["warm"], dd_["ins"][dd_["warm"]], dd_["oos"][dd_["warm"]]
            sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values[warm], ins, oos)
            lbw = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                           freq="W")["returns"].values[warm]
            lbm = blocks_m(lbw, ins, oos)
            pass5, pass4, pass4a = [], [], []
            for g in LAD_G:
                r = lads[(tape, panel)][g][warm]
                b = blocks_m(r, ins, oos)
                lg = legs_core(b, sb)
                lg["L_OOS"] = bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"])
                la = legs_4a(b, lbm)
                pass5.append(all(lg[k] for k in FIVE))
                pass4.append(all(lg[k] for k in CORE))
                pass4a.append(all(la.values()))
                five_rows.append(dict(tape=tape, panel=panel, gross=g,
                                      CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"],
                                      H1=b["H1"], H2=b["H2"], OOS_Sharpe=b["OOS_Sharpe"],
                                      OOS_CAGR=b["OOS_CAGR"], OOS_MaxDD=b["OOS_MaxDD"],
                                      **{k: lg[k] for k in FIVE}, **la,
                                      pass_4b_five=pass5[-1], pass_4b_core=pass4[-1],
                                      pass_4a=pass4a[-1]))
            repro[(tape, panel)] = dict(five=window_of(np.array(pass5)),
                                        core=window_of(np.array(pass4)),
                                        n4a=int(np.sum(pass4a)))
            w5, w4 = repro[(tape, panel)]["five"], repro[(tape, panel)]["core"]
            P(f"  {tape:<10s} {panel:<6s} FIVE-leg width {w5['width']:2d} "
              f"[{w5['lo']} .. {w5['hi']}] contig {w5['contiguous']}   |   "
              f"CORE width {w4['width']:2d} [{w4['lo']} .. {w4['hi']}] contig {w4['contiguous']}"
              f"   |   4a {repro[(tape, panel)]['n4a']} of {len(LAD_G)}")
    FT = pd.DataFrame(five_rows)
    dump(FT, "fulltape")
    P("  WHY a window is the width it is — per-leg FAILURE COUNT over the 33 rungs "
      "(a rung passes only if every leg does):")
    for tape in TAPES:
        for panel in PANELS:
            s = FT[(FT.tape == tape) & (FT.panel == panel)]
            P(f"    {tape:<10s} {panel:<6s} " + "  ".join(
                f"{k} fails {int((~s[k]).sum()):2d}" for k in FIVE))
    dec_ok, dec_v = True, 0.0
    for tape in TAPES:
        for panel in PANELS:
            s = FT[(FT.tape == tape) & (FT.panel == panel)].sort_values("gross")
            nsh = int((~s["L_H1"] | ~s["L_H2"] | ~s["L_OOS"]).sum())
            ndd, ncg = int((~s["L_DD"]).sum()), int((~s["L_CAGR"]).sum())
            w = int(s.pass_4b_five.sum())
            if nsh == 0:
                dec_v = max(dec_v, abs(w - (len(LAD_G) - ndd - ncg)))
                dec_ok &= (w == len(LAD_G) - ndd - ncg)
    gate("G8", "where NO Sharpe leg binds, WIDTH is exactly 33 - |L_DD fails| - |L_CAGR fails|, "
         "i.e. the window is the arithmetic gap between the two opposed EXPOSURE legs",
         dec_v, dec_ok)
    P("     Gross moves CAGR and drawdown and is very nearly Sharpe-neutral, so on a panel")
    P("     where a Sharpe leg fails, NO rung of the ladder can rescue it: the window is not")
    P("     narrow there, it is STRUCTURALLY EMPTY.  That is the whole of the SMALL reading.")
    v = max(abs(repro[("T_OWN", p)]["five"]["lo"] - W1150[p][0]) +
            abs(repro[("T_OWN", p)]["five"]["hi"] - W1150[p][1]) +
            abs(repro[("T_OWN", p)]["five"]["width"] - W1150[p][2]) for p in W1150)
    gate("G6", "CROSS-RUN 1150's five-leg window reproduced rung for rung (U56 and B136)",
         v, v == 0.0)
    ok7 = all(repro[(t, p)]["core"]["width"] >= repro[(t, p)]["five"]["width"]
              for t in TAPES for p in PANELS)
    gate("G7", "the CORE window contains the FIVE-leg window at every f=1 cell (dropping a "
         "leg cannot shrink a pass set)", 0.0 if ok7 else 1.0, ok7)

    # --------------------------------------------------------- ARM 1: the sub-tape grid
    P("")
    P("## ARM 1 — the WIDTH grid: panel x tape x fraction x stretch x 33 gross rungs")
    grid, wins = [], []
    for tape in TAPES:
        for panel in PANELS:
            dd_ = cells[(tape, panel)]
            warm = dd_["warm"]
            spyw = dd_["px"]["SPY"].pct_change().fillna(0.0).values[warm]
            lbw = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                           freq="W")["returns"].values[warm]
            rw = {g: lads[(tape, panel)][g][warm] for g in LAD_G}
            n = int(warm.sum())
            for partition in PARTITIONS:
                for f in FRACS:
                    for si, (a, b_) in enumerate(parts_at(n, f, partition)):
                        sp = spyw[a:b_]
                        sb = blocks_m(sp)
                        lbm = blocks_m(lbw[a:b_])
                        spy_down = bool(sb["CAGR"] <= 0)
                        pas, pas4a = [], []
                        for g in LAD_G:
                            bm = blocks_m(rw[g][a:b_])
                            lg = legs_core(bm, sb)
                            la = legs_4a(bm, lbm)
                            pas.append(all(lg[k] for k in CORE))
                            pas4a.append(all(la.values()))
                            grid.append(dict(tape=tape, panel=panel, partition=partition,
                                             frac=f, stretch=si, n_days=b_ - a, gross=g,
                                             spy_down=spy_down, CAGR=bm["CAGR"],
                                             Sharpe=bm["Sharpe"], MaxDD=bm["MaxDD"],
                                             spy_CAGR=sb["CAGR"], spy_Sharpe=sb["Sharpe"],
                                             spy_MaxDD=sb["MaxDD"], **lg, **la,
                                             pass_4b_core=pas[-1], pass_4a=pas4a[-1]))
                        w = window_of(np.array(pas))
                        wins.append(dict(tape=tape, panel=panel, partition=partition, frac=f,
                                         stretch=si, n_days=b_ - a, spy_down=spy_down,
                                         n_4a=int(np.sum(pas4a)), **w))
    G = pd.DataFrame(grid)
    Wd = pd.DataFrame(wins)
    dump(G, "grid")
    dump(Wd, "windows")

    P("")
    P("  WIDTH by panel x fraction (T_MATCHED, ALIGNED, median over stretches; "
      "'(-dn)' = excluding spy_down stretches):")
    P(f"    {'panel':<6s} " + " ".join(f"{'f=' + str(f):>12s}" for f in FRACS))
    for panel in PANELS:
        cellsr = []
        for f in FRACS:
            s = Wd[(Wd.tape == HEAD_TAPE) & (Wd.panel == panel) & (Wd.partition == "ALIGNED")
                  & (Wd.frac == f)]
            sd = s[~s.spy_down]
            cellsr.append(f"{s.width.median():5.1f}({sd.width.median() if len(sd) else float('nan'):4.1f})")
        P(f"    {panel:<6s} " + " ".join(f"{c:>12s}" for c in cellsr))
    P("  Same on T_OWN (each panel over its own, unequal tape):")
    for panel in PANELS:
        cellsr = []
        for f in FRACS:
            s = Wd[(Wd.tape == "T_OWN") & (Wd.panel == panel) & (Wd.partition == "ALIGNED")
                  & (Wd.frac == f)]
            sd = s[~s.spy_down]
            cellsr.append(f"{s.width.median():5.1f}({sd.width.median() if len(sd) else float('nan'):4.1f})")
        P(f"    {panel:<6s} " + " ".join(f"{c:>12s}" for c in cellsr))
    ncontig = int((~Wd.contiguous).sum())
    P(f"  CONTIGUITY: {len(Wd) - ncontig} of {len(Wd)} stretch-windows are contiguous "
      f"({(len(Wd)-ncontig)/len(Wd):.4f}); {ncontig} carry a gap.")
    nz = int((Wd.width == 0).sum())
    P(f"  EMPTY: {nz} of {len(Wd)} stretch-windows are EMPTY (no gross rung of 33 passes 4b-core).")

    # ------------------------------------------------- ARM 2: the PANEL vs TAPE verdict
    P("")
    P("## ARM 2 — the VERDICT: between-panel spread vs within-panel spread, count-matched")
    rng = np.random.default_rng(seed_of("verdict"))
    vrows = []
    for tape in TAPES:
        for partition in PARTITIONS:
            for excl in (False, True):
                bet, wit = [], []
                for f in FRACS:
                    s = Wd[(Wd.tape == tape) & (Wd.partition == partition) & (Wd.frac == f)]
                    if excl:
                        s = s[~s.spy_down]
                    if not len(s):
                        continue
                    med = [s[s.panel == p].width.median() for p in PANELS
                           if len(s[s.panel == p])]
                    b = matched_spread(med, rng)
                    if np.isfinite(b):
                        bet.append(b)
                    if f > 1:
                        for p in PANELS:
                            v = s[s.panel == p].width.values
                            w = matched_spread(v, rng)
                            if np.isfinite(w):
                                wit.append(w)
                B = float(np.nanmedian(bet)) if bet else np.nan
                Wi = float(np.nanmedian(wit)) if wit else np.nan
                vrows.append(dict(tape=tape, partition=partition, excl_spy_down=excl,
                                  between_panel=B, within_panel=Wi,
                                  ratio=(B / Wi if Wi else np.nan),
                                  verdict=("PANEL" if B > Wi else "TAPE")))
                P(f"  {tape:<10s} {partition:<8s} excl_spy_down={str(excl):<5s} "
                  f"BETWEEN-PANEL {B:6.3f}  WITHIN-PANEL {Wi:6.3f}  ratio {B/Wi if Wi else float('nan'):6.3f}"
                  f"  -> {'PANEL' if B > Wi else 'TAPE'}")
    V = pd.DataFrame(vrows)
    dump(V, "verdict")
    head_v = V[(V.tape == HEAD_TAPE) & (V.partition == "ALIGNED") & (~V.excl_spy_down)].iloc[0]
    P(f"  HEADLINE ({HEAD_TAPE}/ALIGNED/pooled): between {head_v.between_panel:.3f} vs within "
      f"{head_v.within_panel:.3f} -> {head_v.verdict}")
    P(f"  UNANIMITY across the {len(V)} (tape, partition, spy_down) readings: "
      + ", ".join(f"{k} {int(v)}" for k, v in V.verdict.value_counts().items()))
    ndeg = int((V.between_panel == 0).sum())
    P(f"  DEGENERACY, stated rather than buried: {ndeg} of {len(V)} readings have a")
    P("  BETWEEN-PANEL spread of exactly 0 — not because the panels agree on a width, but")
    P("  because every panel's median width is CENSORED AT 0 (the window is empty on all")
    P("  three).  A 'TAPE' verdict reached that way is a floor artefact, not evidence.")

    # ----------------------------------------- ARM 3: does width fall with tape LENGTH?
    P("")
    P("## ARM 3 — width vs tape LENGTH (the mechanical hypothesis: a shorter tape resolves")
    P("##   fewer rungs, so the window narrows or empties as f grows)")
    lrows = []
    for tape in TAPES:
        for panel in PANELS:
            s = Wd[(Wd.tape == tape) & (Wd.panel == panel) & (Wd.partition == "ALIGNED")]
            x = np.log(s.n_days.values.astype(float))
            y = s.width.values.astype(float)
            b = np.polyfit(x, y, 1)[0] if len(set(x)) > 1 else np.nan
            rho = spearman(x, y)
            lrows.append(dict(tape=tape, panel=panel, n=len(s), slope_width_per_log_days=b,
                              spearman=rho, width_f1=float(s[s.frac == 1].width.iloc[0]),
                              width_f6_med=float(s[s.frac == 6].width.median())))
            P(f"  {tape:<10s} {panel:<6s} n {len(s):3d}  d(width)/d(log days) {b:+7.3f}  "
              f"spearman {rho:+.4f}  width f=1 {s[s.frac==1].width.iloc[0]:2.0f} -> "
              f"f=6 median {s[s.frac==6].width.median():4.1f}")
    dump(pd.DataFrame(lrows), "length")

    # ------------------------------------- ARM 4: the gross-matched RANDOM-BOOK null
    P("")
    P(f"## ARM 4 — the gross-matched RANDOM-BOOK null ({NSEED} seeds): is a WIDTH of this size")
    P("##   evidence of anything, or does a random 20-name book of the same gross get one too?")
    nrows = []
    for panel in PANELS:
        for seed_i in range(NSEED):
            sd = seed_of("null", HEAD_TAPE, panel, seed_i)
            lad = ladder(HEAD_TAPE, panel, rank_key=rand_key(HEAD_TAPE, panel, sd))
            dd_ = cells[(HEAD_TAPE, panel)]
            warm, ins, oos = dd_["warm"], dd_["ins"][dd_["warm"]], dd_["oos"][dd_["warm"]]
            sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values[warm], ins, oos)
            pas, pas5 = [], []
            for g in LAD_G:
                bm = blocks_m(lad[g][warm], ins, oos)
                lg = legs_core(bm, sb)
                lg["L_OOS"] = bool(bm["OOS_Sharpe"] > sb["OOS_Sharpe"])
                pas.append(all(lg[k] for k in CORE))
                pas5.append(all(lg[k] for k in FIVE))
            w, w5 = window_of(np.array(pas)), window_of(np.array(pas5))
            nrows.append(dict(panel=panel, seed=seed_i, width_core=w["width"],
                              lo=w["lo"], hi=w["hi"], contiguous=w["contiguous"],
                              width_five=w5["width"]))
        P(f"  built {NSEED} null ladders for {panel}  ({time.time()-t0:.0f}s)")
    Nn = pd.DataFrame(nrows)
    dump(Nn, "nulls")
    for panel in PANELS:
        s = Nn[Nn.panel == panel]
        book = repro[(HEAD_TAPE, panel)]
        pct_c = float((s.width_core <= book["core"]["width"]).mean())
        pct_5 = float((s.width_five <= book["five"]["width"]).mean())
        strict = float((s.width_core < book["core"]["width"]).mean())
        P(f"  {panel:<6s} BOOK core width {book['core']['width']:2d} / five {book['five']['width']:2d}"
          f"   NULL core median {s.width_core.median():4.1f} "
          f"[{s.width_core.min()}, {s.width_core.max()}] , five median {s.width_five.median():4.1f}"
          f"   -> book percentile core {pct_c:.3f} (STRICTLY below {strict:.3f}) / five {pct_5:.3f}"
          f"   (null contiguous {s.contiguous.mean():.3f})")
    P("  TIE WARNING, stated rather than buried: the <= percentile is 1.000 by construction")
    P("  wherever the book's own width is 0, because every null draw ties it.  The STRICTLY-")
    P("  below column is the honest one: it is the share of nulls the book actually beats.")

    # ------------------------------------------------------- ARM 5: rule 8 walk-forward
    P("")
    P("## ARM 5 — PROTOCOL rule 8 WALK-FORWARD.  Parameters chosen on the FIRST HALF only")
    P("##   (<= 2016-12-31), evaluated on the untouched SECOND HALF.  For THIS idea the")
    P("##   walk-forward object is the WINDOW itself: is the IS window the OOS window?")
    wfrows = []
    for tape in TAPES:
        for panel in PANELS:
            dd_ = cells[(tape, panel)]
            warm = dd_["warm"]
            ins, oos = dd_["ins"][warm], dd_["oos"][warm]
            spyw = dd_["px"]["SPY"].pct_change().fillna(0.0).values[warm]
            lbw = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                           freq="W")["returns"].values[warm]
            sb_i, sb_o = blocks_m(spyw[ins]), blocks_m(spyw[oos])
            lb_o = blocks_m(lbw[oos])
            pi, po, isS = [], [], []
            for g in LAD_G:
                r = lads[(tape, panel)][g][warm]
                bi, bo = blocks_m(r[ins]), blocks_m(r[oos])
                pi.append(all(legs_core(bi, sb_i)[k] for k in CORE))
                po.append(all(legs_core(bo, sb_o)[k] for k in CORE))
                isS.append(bi["Sharpe"])
            wi, wo = window_of(np.array(pi)), window_of(np.array(po))
            inter = int(np.sum(np.array(pi) & np.array(po)))
            uni = int(np.sum(np.array(pi) | np.array(po)))
            # the three honest IS-only choosers of 1150/1157
            picks = {"C_ISSHARPE": int(np.argmax(isS)),
                     "C_ISWINMID": (int(round((np.flatnonzero(pi).mean()))) if wi["width"] else -1),
                     "C_ANCHOR": LAD_G.index(GROSS0)}
            for cname, gi in picks.items():
                if gi < 0:
                    wfrows.append(dict(tape=tape, panel=panel, chooser=cname, pick=np.nan,
                                       pick_in_OOS_window=False, OOS_CAGR=np.nan,
                                       OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                       spy_OOS_CAGR=sb_o["CAGR"], spy_OOS_Sharpe=sb_o["Sharpe"],
                                       spy_OOS_MaxDD=sb_o["MaxDD"], live_OOS_Sharpe=lb_o["Sharpe"],
                                       live_OOS_MaxDD=lb_o["MaxDD"], pass_4b_core_OOS=False))
                    continue
                g = LAD_G[gi]
                bo = blocks_m(lads[(tape, panel)][g][warm][oos])
                wfrows.append(dict(
                    tape=tape, panel=panel, chooser=cname, pick=g,
                    pick_in_OOS_window=bool(po[gi]),
                    OOS_CAGR=bo["CAGR"], OOS_Sharpe=bo["Sharpe"], OOS_MaxDD=bo["MaxDD"],
                    spy_OOS_CAGR=sb_o["CAGR"], spy_OOS_Sharpe=sb_o["Sharpe"],
                    spy_OOS_MaxDD=sb_o["MaxDD"], live_OOS_Sharpe=lb_o["Sharpe"],
                    live_OOS_MaxDD=lb_o["MaxDD"],
                    pass_4b_core_OOS=bool(po[gi])))
            P(f"  {tape:<10s} {panel:<6s} IS window width {wi['width']:2d} [{wi['lo']}..{wi['hi']}]"
              f"   OOS window width {wo['width']:2d} [{wo['lo']}..{wo['hi']}]"
              f"   Jaccard {inter/uni if uni else float('nan'):.3f}"
              f"   picks: " + ", ".join(
                  f"{k}={LAD_G[v] if v >= 0 else 'none'}{'*' if v >= 0 and po[v] else ''}"
                  for k, v in picks.items()))
    WF = pd.DataFrame(wfrows)
    dump(WF, "walkforward")
    P("  ('*' = the IS-chosen rung is inside the OOS window.)")
    P("  OOS triples of the IS-Sharpe pick vs SPY and vs the live book:")
    for r in WF[WF.chooser == "C_ISSHARPE"].itertuples():
        P(f"    {r.tape:<10s} {r.panel:<6s} pick g={r.pick}  OOS CAGR {r.OOS_CAGR:7.2%} / "
          f"Sharpe {r.OOS_Sharpe:6.3f} / MaxDD {r.OOS_MaxDD:7.2%}   "
          f"SPY {r.spy_OOS_CAGR:7.2%} / {r.spy_OOS_Sharpe:6.3f} / {r.spy_OOS_MaxDD:7.2%}   "
          f"LIVE {r.live_OOS_Sharpe:6.3f} / {r.live_OOS_MaxDD:7.2%}")

    # --------------------------------------------------------------------- hypotheses
    P("")
    P("## HYPOTHESES — declared in the docstring, scored here")
    n_cont = float(Wd.contiguous.mean())
    len_slopes = [r["slope_width_per_log_days"] for r in lrows]
    h = []
    h.append(("H_REPRO", "1150's five-leg window reproduces rung for rung on U56 and B136",
              all(g["gate"] != "G6" or g["pass_"] for g in gaterows)))
    h.append(("H_CONTIG", "the pass set is a contiguous WINDOW at >= 90% of stretch cells",
              n_cont >= 0.90))
    h.append(("H_PANEL", "width is a PANEL object (between-panel spread > within-panel)",
              bool(head_v.verdict == "PANEL")))
    h.append(("H_TAPE", "width is a TAPE-LENGTH object (width rises with log tape length on a "
              "majority of panel-tape cells)", bool(np.nanmedian(len_slopes) > 0)))
    h.append(("H_NULL", "the book's width is not reachable by a gross-matched random book "
              "(book STRICTLY above >= 0.90 of null draws on a majority of panels)",
              bool(np.mean([float((Nn[Nn.panel == p].width_core <
                                   repro[(HEAD_TAPE, p)]["core"]["width"]).mean()) >= 0.90
                            for p in PANELS]) > 0.5)))
    h.append(("H_WF", "the IS window's midpoint rung is inside the OOS window on a majority "
              "of panel-tape cells",
              bool(WF[WF.chooser == "C_ISWINMID"].pick_in_OOS_window.mean() > 0.5)))
    for k, w, ok in h:
        P(f"  [{'YES' if ok else 'NO ':<3s}] {k:<9s} {w}")
    dump(pd.DataFrame([dict(hypothesis=k, statement=w, holds=bool(ok)) for k, w, ok in h]),
         "hypotheses")

    # ------------------------------------------------------------------ the KEEP paths
    P("")
    P("## BOTH KEEP PATHS (PROTOCOL rule 4), over every cell this run produced")
    n4a_full = sum(repro[(t, p)]["n4a"] for t in TAPES for p in PANELS)
    P(f"  4a (beat the live book) full tape: {n4a_full} of {len(TAPES)*len(PANELS)*len(LAD_G)} "
      f"(gross, tape, panel) cells; on sub-tapes {int(G.pass_4a.sum())} of {len(G)} rows.")
    P(f"  4b full-tape FIVE-leg: " + ", ".join(
        f"{t}/{p} {repro[(t,p)]['five']['width']}" for t in TAPES for p in PANELS)
      + f" of {len(LAD_G)} rungs each.")
    P(f"  4b CORE on sub-tapes: {int(G.pass_4b_core.sum())} of {len(G)} rows.")
    P("  NOTHING IS PROPOSED: every 4b pass here is a rung of the incumbent CAND20 book, the")
    P("  object 1150 already published; this run measures the WIDTH of that pass set, it does")
    P("  not offer a new rule.  RULES.md / scan.py / bot.py / baseline.py untouched (rule 6).")

    dump(pd.DataFrame(gaterows), "gates")
    P("")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

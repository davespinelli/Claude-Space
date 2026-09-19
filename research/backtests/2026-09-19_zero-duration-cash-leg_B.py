#!/usr/bin/env python3
"""Idea 1602 (lane B, 2026-09-19): DOES THE SHY RESIDUAL CLAUSE SURVIVE A ZERO-DURATION CASH LEG?

THE DEFECT.  RULES v2 clause 2 gates a name OUT below the 200d -3% band and parks its weight in
CASH at 0.00%/yr.  Ideas 1358 / 1498 / 1555 / 1547 all fix that by crediting the idle NAV with
SHY, and idea 1498's cell (LIVE frame, U56, G = 0.75, F = 1.00 -> 9.12% / 1.2675 / -11.48%) is
the FIRST device in the record to clear path 4a at all.  But SHY is NOT cash.  It is a 1-3y
Treasury ETF marked to market: it lost 3.88% in calendar 2022, it carries a -5.71% own drawdown,
and idea 1555's own preamble flagged the gap in one line ("there is NO zero-duration cash
instrument in the committed cache").  Idea 1547 then found the 4a pass FAILS inside ERA_HIKE on
the first half alone, monotonically in F — i.e. exactly where duration was paid.

So the committed 4a pass is a SUM of two different things that the record has never separated:
  (i)  CARRY      -- idle NAV earning a positive rate instead of 0.00%/yr, and
  (ii) DURATION   -- a marked-to-market bond sleeve with its own vol, its own drawdown and its
                     own 2022 loss, which is NOT what a broker sweep does.
A real book's idle NAV earns (i) with NONE of (ii).  If the pass is carry, a ZERO-DURATION
accrual at the same realised rate reproduces it (or beats it, having no 2022 loss) and the
clause should be restated in accrual terms.  If the pass needs the bond, it is a DIVERSIFICATION
claim about holding duration against equity, not a cash-convention claim, and it must be
re-titled -- and then re-argued, because a book that must hold duration to pass 4a is exposed to
a rate shock the record has never priced.

THE CONSTRUCTION.  Replace the sleeve asset with a SYNTHETIC ZERO-DURATION ACCRUAL: a daily
return of exactly (1 + a)^(1/252) - 1, constant, no mark-to-market, no drawdown, no vol.  Run it
against the SHY arm on the SAME names, the SAME days, the SAME frame and the SAME F ladder.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  F {0.00, 0.25, 0.50, 0.75, 1.00}  DIAL 1 -- fraction of the gated-out (idle) NAV routed to the
      sleeve.  F = 0.00 IS the live 0%-cash convention and is a cell of EVERY arm, so the "change
      nothing" null is priced on the same tape as every candidate (gate G1).
  A {0, 1, 2, 3, 4, 5} %/yr        DIAL 2 -- the accrual rate.  A = 0 must reproduce F = 0 and
      the live book exactly (gate G8).

  AND A STANDING CAVEAT, PRE-REGISTERED: A IS NOT A DIAL A MANAGER OWNS.  The accrual rate on a
  sweep is set by the money market, not chosen by the book.  It is swept here to map the verdict
  ONTO the rate environment and to solve the break-even a*, and the PRIMARY rule-8 chooser is
  therefore run over F ALONE at each A.  The joint (F, A) chooser is ALSO reported, labelled as
  the illegitimate one, because the record keeps re-finding that a free dial is worth less than
  its default.

COMPARANDS (derived from the data, no free parameter, reported at every F):
  SHY      the committed incumbent sleeve of ideas 1358 / 1498 / 1555 / 1547.
  MATCH1   FLAT accrual at a = SHY's OWN realised CAGR on that panel's tape.  Same carry, zero
           duration.  SHY minus MATCH1 IS THE DURATION CONTRIBUTION, and it is this run's
           headline statistic.
  MATCH2   two-piece accrual at SHY's OWN realised CAGR in each era (ZIRP / HIKE), zero duration.
           Matches the carry era by era, so it cannot be confounded by the 2022 regime break.

SHAPES (reported at every value, NOT dials): FLAT (constant a over the whole tape) and STEP
(0.00%/yr before 2022-03-16, a after).  2022-03-16 is the FOMC's first hike of the 2022-23 cycle
-- a CALENDAR fact, fixed before any return was read, and the same break idea 1547 used.  STEP is
the ERA-HONEST shape: a sweep paid ~0 in the ZIRP years and ~5% after, so FLAT at 5% is a
counterfactual and STEP at 5% is roughly what a book run today would actually earn.

FRAMES / PANELS (reported at every value, NOT dials):
  LIVE  = the live RULES v2 shape (`baseline.rules_v2_weights`, 200d +/-3% hysteresis band, equal
          weight inside, de-gross to cash), weekly, G = 0.75 -- the frame idea 1498's pass is on.
  INC   = the frozen 2026-09-04 incumbent (composite momentum, N = 20, H = 126, 200d gate,
          vol20 < 0.60), weekly, G = 0.75.
  PANELS U56 / B136 / SMALL.

GROSS IS FROZEN at G = 0.75 on both frames (the live value and the 2026-09-04 anchor value).
Idea 1498 already swept it; sweeping it again would be a third parameter.

450 cells, EVERY ONE PUBLISHED in the .grid.csv, plus a 41-point break-even curve per
(panel, frame) in the .astar.csv.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) MATCH1 >= SHY on Sharpe AND MaxDD at F = 1.00 on most panel-frames -> the credit is PURE
      CARRY, duration is a NET COST, and clause 6 should be written as an accrual, not an ETF.
  (b) SHY > MATCH1 on Sharpe or MaxDD -> the sleeve is buying DIVERSIFICATION and the clause is
      mis-titled; it is a bond-allocation rule and must be re-argued as one.
  (c) The 4a pass survives only at accrual rates ABOVE what a sweep actually pays -> the pass is
      not reachable by a real cash leg at all, and the committed 4a result is an ARTEFACT OF THE
      INSTRUMENT.  The break-even a* is the number that decides this and it is solved, not
      asserted.
  (d) The rule-8 chooser over F alone loses OOS -> the axis is a KILL as a dial whatever its
      ex-post best cell does.
All four are reported.  Nothing is tuned until it works.

GATES.  G0 sample >= 10y (rule 1).  G1 F = 0 invariance: every arm bit-identical to the live
0%-cash book at F = 0 on every (panel, frame).  G2 cross-script replay of `baseline.compare`'s
RULES v2 row.  G3 cross-script replay of idea 1498's TWO committed U56 SHY cells.  G4 no
leverage.  G5 exactly two tuned parameters.  G6 no chooser reads a row on or after 2017-01-01.
G7 all cells published.  G8a A = 0 invariance on the FREE-SWEEP book (FLAT and STEP at a = 0 ==
the live book at any F, to float precision), with G8b publishing the charged-cost residual as
the sleeve's own turnover cost.
G9 PUBLISHED, not asserted: SHY's own standalone profile, full and by era, on every panel; the
realised mean idle share; and the exact free-sweep (zero sleeve cost) reconstruction.  G10 the
era-honest first half is BIT-IDENTICAL to the live book — the structural result of H5.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps on BOTH legs, no leverage, no shorting); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward, 2017-2026 read
exactly once); rule 9 (survivorship stated).  RULES.md, scan.py, bot.py and baseline.py are NOT
modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_zero-duration-cash-leg_B.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "zero-duration-cash-leg"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H = 20, 126                                  # the frozen 2026-09-04 incumbent
G_FROZEN, CAD, COST, BAND = 0.75, "W", 10.0, 0.03
GRID_F = [0.00, 0.25, 0.50, 0.75, 1.00]
GRID_A = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]       # accrual rate, /yr
SHAPES = ["FLAT", "STEP"]
FRAMES = ["LIVE", "INC"]
HIKE = "2022-03-16"                                 # FOMC first hike of the 2022-23 cycle
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
ASTAR_GRID = [round(0.0025 * k, 4) for k in range(41)]      # 0.00% .. 10.00% by 0.25 pp
# idea 1498's committed U56 SHY cells at G = 0.75, F = 1.00 (CHANGELOG 2026-09-19)
REPLAY_1498 = {"LIVE": dict(CAGR=0.0912, Sharpe=1.2675, MaxDD=-0.1148),
               "INC": dict(CAGR=0.1616, Sharpe=1.1787, MaxDD=-0.1888)}

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
    say(f"    PUBLISHED  {name}: {value}")


def daily(a):
    """Annual accrual a -> the exact constant daily rate that compounds to a over 252 days."""
    return (1.0 + a) ** (1.0 / 252.0) - 1.0


# ---------------------------------------------------------------- selection frames (frozen)
def mech(q):
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
    def __init__(self, name, px, invest, ref):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        # SHY comes from the SAME reference tape on every panel, so the duration contrast is not
        # confounded by which panel prices the sleeve.
        self.shy = np.nan_to_num(ref["SHY"].reindex(px.index).ffill().pct_change().values, nan=0.0)
        self.i_hike = int(np.searchsorted(px.index.values, np.datetime64(HIKE)))
        self.i_oos = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)

    def accrual(self, a, shape="FLAT"):
        """Zero-duration sleeve: a constant daily accrual, never marked to market."""
        s = np.full(len(self.idx), daily(a))
        if shape == "STEP":
            s[: self.i_hike] = 0.0
        return s

    def accrual2(self, a_zirp, a_hike):
        s = np.full(len(self.idx), daily(a_zirp))
        s[self.i_hike:] = daily(a_hike)
        return s


def frame_inc(pan, reb, N, H, lag=1):
    """Frozen min-hold momentum selection at GROSS = 1.0 (the 2026-09-04 incumbent)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
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
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def frame_live(pan, band=BAND):
    """The live RULES v2 band shape at GROSS = 1.0, shifted so row t carries the close-t-1
    decision -- exactly engine.backtest's `weights.shift(1)` convention."""
    return rules_v2_weights(pan.px, band=band, gross=1.0).reindex(pan.idx).fillna(0.0).shift(1).fillna(0.0).values


def run_cell(pan, frame, reb, sleeve_ret, f, g=G_FROZEN, cost=COST):
    """The frozen frame at constant gross g, routing fraction f of the IDLE NAV into a sleeve
    whose daily return series is `sleeve_ret`.  The sleeve drifts with the book between
    rebalances and pays `cost` bps on its own turnover, exactly as a held ETF does; f = 0
    reduces to the record's 0%-cash convention for ANY sleeve.  Identical arithmetic to idea
    1555's run_cell (gate G3 replays its committed cells), with sleeve turnover split out so the
    free-sweep variant can be reconstructed exactly rather than re-run.
    """
    rets = pan.rets
    cr = sleeve_ret
    T, M = rets.shape
    turn_r = np.zeros(T)
    turn_s = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    csle = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0 + f * (1.0 - s0))
        turn_r[i0] = float(np.abs(w0 - curw).sum())
        turn_s[i0] = f * abs(s0 - float(curw.sum()))
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])            # risky value at START of each day
        seg = cr[i0:i1]
        cash_growth = np.concatenate(([1.0], np.cumprod(1.0 + f * seg)[:-1]))
        Ccash = (1.0 - s0) * cash_growth                          # residual value at START of day
        V = A.sum(axis=1) + Ccash
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1) + (Ccash / V) * (f * seg)
        gsum[i0:i1] = A.sum(axis=1) / V
        csle[i0:i1] = f * Ccash / V
        Ae = w0 * (C[i1 - 1] / base)
        ce = (1.0 - s0) * float(np.prod(1.0 + f * seg))
        curw = Ae / (Ae.sum() + ce)
    turn = turn_r + turn_s
    return out - turn * cost / 1e4, turn, turn_s, wsum_max, gsum, csle


# ---------------------------------------------------------------- metrics
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
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def arm_label(shape, a):
    return f"{shape}@{a*100:.2f}%"


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1602 (lane B, 2026-09-19) — DOES THE SHY RESIDUAL CLAUSE SURVIVE A ZERO-DURATION CASH LEG?")
    say(f"DIALS: F {GRID_F}  x  A {[f'{a:.0%}' for a in GRID_A]} /yr.  Everything else is frozen or reported.")
    say(f"SHAPES (reported, not dials): FLAT (constant a) and STEP (0 before {HIKE}, a after).")
    say(f"COMPARANDS (derived, no free parameter): SHY (the committed sleeve), MATCH1 (flat accrual at "
        f"SHY's OWN realised CAGR), MATCH2 (two-piece accrual at SHY's OWN era CAGRs).")
    say(f"GROSS FROZEN at G = {G_FROZEN}.  Weekly, {COST:.0f} bps on BOTH legs, t+1.  F = 0.00 is the null.")
    say("PRE-REGISTERED CAVEAT: A is NOT a dial a manager owns — a sweep rate is set by the money market. "
        "The PRIMARY rule-8 chooser runs over F ALONE at each A; the joint (F, A) chooser is reported and "
        "labelled illegitimate.")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"], ref),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"], ref),
              Panel("SMALL", pxS, inv, ref)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} "
        f"(of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B "
        "screen carried back to 2010.  Every absolute level below — every CAGR, every 4a/4b pass — is an "
        "UPPER BOUND.  What survives that bias is the CONTRAST between SHY and its zero-duration twin on "
        "the same names, the same days and the same frame: both arms inherit the identical bias.")
    say("  ACCRUAL REALISM (stated, not glossed): the synthetic sleeve is a pure carry instrument — no "
        "mark-to-market, no vol, no drawdown, no credit risk.  That is the OPTIMISTIC end of a real broker "
        "sweep (which pays below the policy rate and is not risk-free either).  It is exactly the right "
        "control here because the question is what the DURATION in SHY is worth, and an idealised cash leg "
        "is the conservative comparand for that: if SHY cannot beat it, SHY certainly cannot beat a real one.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # ---- G9a: SHY's own profile, full and by era, on every panel's own window
    say("\n  G9a SHY's OWN standalone profile (before any book credits it), per panel window:")
    SHY_A = {}
    for p in panels:
        s = p.shy
        full, zirp, hike = triple(s[WARMUP:]), triple(s[WARMUP:p.i_hike]), triple(s[p.i_hike:])
        oos = triple(s[p.i_oos:])
        SHY_A[p.name] = dict(full=full["CAGR"], zirp=zirp["CAGR"], hike=hike["CAGR"])
        publish(f"G9a SHY on {p.name} window",
                f"FULL {full['CAGR']:.4%}/{full['Sharpe']:.3f}/{full['MaxDD']:.2%}  "
                f"ZIRP {zirp['CAGR']:.4%}  HIKE {hike['CAGR']:.4%}  OOS {oos['CAGR']:.4%}/{oos['MaxDD']:.2%}")

    # ---------------------------------------------------------------- the grid
    grid, wsum_global = [], 0.0
    RET, TS, ISPK, BARS, FRAMEW, REB = {}, {}, {}, {}, {}, {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = pan.i_oos
        spy = bmpack(pan.spy[WARMUP:]); spyO = bmpack(pan.spy[i_oos:]); spyI = bmpack(pan.spy[WARMUP:i_oos])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq=CAD)["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        BARS[pan.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, i_oos=i_oos, lr=lr)
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}  |  "
            f"OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @{COST:.0f}bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  (the 4a bar)")

        reb = pan.reb_rows(CAD); REB[pan.name] = reb
        frames = {"LIVE": frame_live(pan), "INC": frame_inc(pan, reb, I_N, I_H)}
        FRAMEW[pan.name] = frames

        arms = [(arm_label(sh, a), pan.accrual(a, sh), sh, a) for sh in SHAPES for a in GRID_A]
        arms.append(("SHY", pan.shy, "SHY", np.nan))
        arms.append(("MATCH1", pan.accrual(SHY_A[pan.name]["full"], "FLAT"), "MATCH", SHY_A[pan.name]["full"]))
        arms.append(("MATCH2", pan.accrual2(SHY_A[pan.name]["zirp"], SHY_A[pan.name]["hike"]), "MATCH", np.nan))

        for fr in FRAMES:
            fm = frames[fr]
            for (lab, sret, sh, a) in arms:
                for f in GRID_F:
                    r, tu, ts, ws, gs, cs = run_cell(pan, fm, reb, sret, f)
                    wsum_global = max(wsum_global, ws)
                    RET[(pan.name, fr, lab, f)] = r
                    TS[(pan.name, fr, lab, f)] = ts
                    rfree = r + ts * COST / 1e4          # exact free-sweep reconstruction
                    k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                    ISPK[(pan.name, fr, lab, f)] = dict(Sharpe=sharpe(r[WARMUP:i_oos]),
                                                        CAGR=cagr(r[WARMUP:i_oos]),
                                                        MaxDD=mdd(r[WARMUP:i_oos]))
                    yrs = (T - WARMUP) / 252.0
                    grid.append(dict(panel=pan.name, frame=fr, arm=lab, shape=sh, A=a, F=f,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                     oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                     zCAGR=cagr(r[WARMUP:pan.i_hike]), hCAGR=cagr(r[pan.i_hike:]),
                                     zSharpe=sharpe(r[WARMUP:pan.i_hike]), hSharpe=sharpe(r[pan.i_hike:]),
                                     isCAGR=ISPK[(pan.name, fr, lab, f)]["CAGR"],
                                     isSharpe=ISPK[(pan.name, fr, lab, f)]["Sharpe"],
                                     isMaxDD=ISPK[(pan.name, fr, lab, f)]["MaxDD"],
                                     freeCAGR=cagr(rfree[WARMUP:]), freeSharpe=sharpe(rfree[WARMUP:]),
                                     mean_gross=float(np.mean(gs[WARMUP:])),
                                     mean_sleeve=float(np.mean(cs[WARMUP:])),
                                     turnover_yr=float(tu[WARMUP:].sum() / yrs),
                                     sleeve_turnover_yr=float(ts[WARMUP:].sum() / yrs),
                                     keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                     leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                     leg_CAGR=legs["CAGR"], oleg_H1=legsO["H1"], oleg_H2=legsO["H2"],
                                     oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"]))
        say(f"    [{pan.name}] {len(arms)*len(GRID_F)*len(FRAMES)} cells done ({time.time()-t0:.0f}s elapsed)")

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ================================================================ GATES
    say("\n" + "=" * 118)
    say("GATES")
    say("=" * 118)

    arm_names = sorted(G.arm.unique())
    worst = 0.0
    for pan in panels:
        for fr in FRAMES:
            base = RET[(pan.name, fr, "SHY", 0.00)]
            for lab in arm_names:
                worst = max(worst, float(np.abs(RET[(pan.name, fr, lab, 0.00)] - base).max()))
    gate(f"G1 arm invariance at F=0 ({len(arm_names)} arms x 6 panel-frames, max |diff|)",
         f"{worst:.3e}", "== 0.0", worst == 0.0)

    d2 = 0.0
    for pan in panels:
        mine = RET[(pan.name, "LIVE", "SHY", 0.00)]
        d2 = max(d2, float(np.abs(mine[WARMUP:] - BARS[pan.name]["lr"][WARMUP:]).max()))
    gate("G2 LIVE/F=0 == baseline.rules_v2_weights book (max |diff|, 3 panels)",
         f"{d2:.3e}", "<= 1e-12", d2 <= 1e-12)

    ok3, det3 = True, []
    for fr in FRAMES:
        m = triple(RET[("U56", fr, "SHY", 1.00)][WARMUP:])
        want = REPLAY_1498[fr]
        dd = dict(CAGR=abs(m["CAGR"] - want["CAGR"]), Sharpe=abs(m["Sharpe"] - want["Sharpe"]),
                  MaxDD=abs(m["MaxDD"] - want["MaxDD"]))
        ok3 &= dd["CAGR"] <= 1e-3 and dd["Sharpe"] <= 2e-3 and dd["MaxDD"] <= 1e-3
        det3.append(f"{fr} got {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} vs committed "
                    f"{want['CAGR']:.2%}/{want['Sharpe']:.4f}/{want['MaxDD']:.2%}")
    gate("G3 replay of idea 1498's U56 SHY F=1.00 cells (LIVE and INC)", " | ".join(det3),
         "|dCAGR|<=1e-3, |dSharpe|<=2e-3, |dMaxDD|<=1e-3", ok3)

    gate("G4 no leverage (max risky+sleeve over all cells)", f"{wsum_global:.12f}",
         "<= 1.0", wsum_global <= 1.0 + 1e-12)
    gate("G5 exactly two tuned parameters", "F, A (G=0.75, band=0.03, N=20, H=126, hike date all frozen)",
         "== 2", True)

    w8, w8c, drag = 0.0, 0.0, []
    for pan in panels:
        for fr in FRAMES:
            base = RET[(pan.name, fr, "SHY", 0.00)]
            for sh in SHAPES:
                for f in GRID_F:
                    k = (pan.name, fr, arm_label(sh, 0.0), f)
                    w8 = max(w8, float(np.abs(RET[k] + TS[k] * COST / 1e4 - base).max()))
                    w8c = max(w8c, float(np.abs(RET[k] - base).max()))
                    if f == 1.00 and sh == "FLAT":
                        drag.append(cagr(base[WARMUP:]) - cagr(RET[k][WARMUP:]))
    gate("G8a A=0 invariance on the FREE-SWEEP book (FLAT/STEP at a=0, every F, == the live 0% book)",
         f"{w8:.3e}", "<= 1e-15 (float precision; the claim is exact in real arithmetic)", w8 <= 1e-15)
    publish("G8b the A=0 residual IS the sleeve's own turnover cost, not an arithmetic error",
            f"max |daily diff| with the cost charged {w8c:.3e}; CAGR drag at F=1.00 "
            f"{np.mean(drag)*100:.4f} pp/yr mean over 6 panel-frames "
            f"(a REAL ETF sleeve pays it; a broker sweep does NOT, which is why the free-sweep "
            f"column is carried through the whole grid)")

    gate("G7 all cells published", f"{len(G)} rows in {Path(OUT).name}.grid.csv",
         f"== {len(arm_names)*len(GRID_F)*len(FRAMES)*len(panels)}",
         len(G) == len(arm_names) * len(GRID_F) * len(FRAMES) * len(panels))

    publish("G9b realised mean IDLE share (1 - mean gross) at F=0, LIVE frame",
            ", ".join(f"{r.panel} {1-r.mean_gross:.4f}"
                      for r in G[(G.arm == "SHY") & (G.F == 0.0) & (G.frame == "LIVE")].itertuples()))
    publish("G9c sleeve turnover cost at F=1.00 (SHY, LIVE) — the free-sweep gap",
            ", ".join(f"{r.panel} {r.sleeve_turnover_yr*COST/1e4*100:.3f} pp/yr "
                      f"(CAGR {r.CAGR:.2%} -> {r.freeCAGR:.2%})"
                      for r in G[(G.arm == "SHY") & (G.F == 1.0) & (G.frame == "LIVE")].itertuples()))

    # ================================================================ H1 — THE DURATION DECOMPOSITION
    say("\n" + "=" * 118)
    say("H1 — THE DURATION DECOMPOSITION: SHY vs MATCH1 (same realised carry, ZERO duration), F = 1.00")
    say("=" * 118)
    say(f"{'panel':6} {'frame':5} {'arm':8} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'oCAGR':>8} {'oSharpe':>8} {'oMaxDD':>8} {'4a':>5} {'4b':>5} {'4aO':>5}")
    H1ROWS = []
    for pan in panels:
        for fr in FRAMES:
            for lab in ["SHY", "MATCH1", "MATCH2"]:
                r = G[(G.panel == pan.name) & (G.frame == fr) & (G.arm == lab) & (G.F == 1.00)].iloc[0]
                say(f"{pan.name:6} {fr:5} {lab:8} {r.CAGR:8.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} "
                    f"{r.H1:7.3f} {r.H2:7.3f} {r.oCAGR:8.2%} {r.oSharpe:8.4f} {r.oMaxDD:8.2%} "
                    f"{str(r.keep4a):>5} {str(r.keep4b):>5} {str(r.keep4a_oos):>5}")
            s = G[(G.panel == pan.name) & (G.frame == fr) & (G.arm == "SHY") & (G.F == 1.00)].iloc[0]
            for lab in ["MATCH1", "MATCH2"]:
                m1 = G[(G.panel == pan.name) & (G.frame == fr) & (G.arm == lab) & (G.F == 1.00)].iloc[0]
                H1ROWS.append(dict(panel=pan.name, frame=fr, twin=lab,
                                   dCAGR=s.CAGR - m1.CAGR, dSharpe=s.Sharpe - m1.Sharpe,
                                   dMaxDD=s.MaxDD - m1.MaxDD, doSharpe=s.oSharpe - m1.oSharpe,
                                   doMaxDD=s.oMaxDD - m1.oMaxDD, dhSharpe=s.hSharpe - m1.hSharpe,
                                   shy4a=bool(s.keep4a), twin4a=bool(m1.keep4a)))
            say("")
    H1D = pd.DataFrame(H1ROWS)
    H1D.to_csv(f"{OUT}.duration.csv", index=False)
    say("SHY MINUS its ZERO-DURATION twin (positive = duration HELPS), 6 panel-frames per twin:")
    for lab in ["MATCH1", "MATCH2"]:
        d = H1D[H1D.twin == lab]
        say(f"  vs {lab}: dCAGR {d.dCAGR.mean()*100:+.4f} pp (wins {int((d.dCAGR>0).sum())}/6)   "
            f"dSharpe {d.dSharpe.mean():+.4f} (wins {int((d.dSharpe>0).sum())}/6)   "
            f"dMaxDD {d.dMaxDD.mean()*100:+.3f} pp (wins {int((d.dMaxDD>0).sum())}/6)   "
            f"dOOS-Sharpe {d.doSharpe.mean():+.4f} (wins {int((d.doSharpe>0).sum())}/6)   "
            f"dHIKE-Sharpe {d.dhSharpe.mean():+.4f} (wins {int((d.dhSharpe>0).sum())}/6)")
    say(f"  4a: SHY passes {int(H1D[H1D.twin=='MATCH1'].shy4a.sum())}/6, MATCH1 twin passes "
        f"{int(H1D[H1D.twin=='MATCH1'].twin4a.sum())}/6, MATCH2 twin passes "
        f"{int(H1D[H1D.twin=='MATCH2'].twin4a.sum())}/6.")

    # ================================================================ H2 — THE FULL GRID
    say("\n" + "=" * 118)
    say("H2 — THE ACCRUAL GRID (every cell; A is the environment, F the dial), F = 1.00 shown")
    say("=" * 118)
    for sh in SHAPES:
        say(f"  SHAPE {sh}")
        say(f"  {'panel':6} {'frame':5} {'A':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'oSharpe':>8} {'4a':>5} {'4b':>5} {'4aO':>5} {'4bO':>5}")
        for pan in panels:
            for fr in FRAMES:
                for a in GRID_A:
                    r = G[(G.panel == pan.name) & (G.frame == fr) & (G.arm == arm_label(sh, a))
                          & (G.F == 1.00)].iloc[0]
                    say(f"  {pan.name:6} {fr:5} {a:6.1%} {r.CAGR:8.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} "
                        f"{r.H1:7.3f} {r.H2:7.3f} {r.oSharpe:8.4f} {str(r.keep4a):>5} {str(r.keep4b):>5} "
                        f"{str(r.keep4a_oos):>5} {str(r.keep4b_oos):>5}")
                say("")
    say("PASS COUNTS over all 30 (panel, frame, F) cells per arm:")
    for lab in arm_names:
        d = G[G.arm == lab]
        say(f"  {lab:12} 4a {int(d.keep4a.sum()):2}/30 full, {int((d.keep4a & d.keep4a_oos).sum()):2}/30 "
            f"full+OOS   |   4b {int(d.keep4b.sum()):2}/30 full, "
            f"{int((d.keep4b & d.keep4b_oos).sum()):2}/30 full+OOS")

    # ================================================================ H3 — BREAK-EVEN ACCRUAL a*
    say("\n" + "=" * 118)
    say("H3 — THE BREAK-EVEN ACCRUAL a*: what rate must a ZERO-DURATION sweep pay to clear 4a / 4b?")
    say("      (F = 1.00, BOTH shapes, 41 rungs 0.00%..10.00% by 0.25 pp, EVERY rung published)")
    say("=" * 118)
    astar_rows = []
    for pan in panels:
        b = BARS[pan.name]
        for fr in FRAMES:
            fm = FRAMEW[pan.name][fr]
            for sh in SHAPES:
                for a in ASTAR_GRID:
                    r, tu, ts, ws, gs, cs = run_cell(pan, fm, REB[pan.name], pan.accrual(a, sh), 1.00)
                    rf = r + ts * COST / 1e4                      # the FREE-SWEEP book, exact
                    k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], b["spy"], b["live"])
                    k4aO, k4bO, mo, _, _, _ = keep_paths(r[b["i_oos"]:], b["spyO"], b["liveO"])
                    f4a, f4b, fm_, fh1, fh2, _ = keep_paths(rf[WARMUP:], b["spy"], b["live"])
                    astar_rows.append(dict(panel=pan.name, frame=fr, shape=sh, A=a, CAGR=m["CAGR"],
                                           Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                           oSharpe=mo["Sharpe"], oCAGR=mo["CAGR"], oMaxDD=mo["MaxDD"],
                                           keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                           free_H1=fh1, free_H2=fh2, free_keep4a=f4a, free_keep4b=f4b))
            say(f"    [{pan.name}/{fr}] a* curve done ({time.time()-t0:.0f}s elapsed)")
    AS = pd.DataFrame(astar_rows)
    AS.to_csv(f"{OUT}.astar.csv", index=False)
    say(f"{'panel':6} {'frame':5} {'shape':5} {'a*(4a)':>10} {'a*(4a+OOS)':>12} {'a*(4b)':>10} "
        f"{'a*(4a,free)':>12} {'mono':>6} {'SHY carry':>10}")
    ASTAR = {}
    for pan in panels:
      for sh in SHAPES:
        for fr in FRAMES:
            d = AS[(AS.panel == pan.name) & (AS.frame == fr) & (AS["shape"] == sh)].sort_values("A")
            def first(col):
                w = d[d[col]]
                return float(w.A.iloc[0]) if len(w) else np.nan
            # monotone = once the path passes it never fails again on a higher rung
            mono = True
            for col in ["keep4a", "keep4b"]:
                v = list(d[col])
                if True in v:
                    mono &= all(v[v.index(True):])
            a4a, a4b, a4af = first("keep4a"), first("keep4b"), first("free_keep4a")
            w = d[d.keep4a & d.keep4a_oos]
            a4ao = float(w.A.iloc[0]) if len(w) else np.nan
            ASTAR[(pan.name, fr, sh)] = dict(a4a=a4a, a4ao=a4ao, a4b=a4b, a4af=a4af, mono=mono)
            f4 = lambda x: "never<=10%" if np.isnan(x) else f"{x:.2%}"
            say(f"{pan.name:6} {fr:5} {sh:5} {f4(a4a):>10} {f4(a4ao):>12} {f4(a4b):>10} "
                f"{f4(a4af):>12} {str(mono):>6} {SHY_A[pan.name]['full']:10.2%}")
    say("READ: a* is the LOWEST zero-duration accrual at which the clause clears the path.  Compare it to "
        "what a sweep actually paid — SHY's own realised CAGR is in the last column, and a real broker "
        "sweep pays LESS than that.  The a*(4a,free) column charges the sleeve NO transaction cost, so a "
        "FLAT a* that falls there was partly a cost artefact and a STEP a* that stays empty there is not.")

    # ---------------- H5: why the STEP column is empty, proved rather than scanned
    say("\n" + "=" * 118)
    say("H5 — THE STRUCTURAL RESULT: path 4a CANNOT certify an era-honest cash leg on this tape.")
    say("=" * 118)
    say("  4a's first leg is a STRICT inequality, H1_Sharpe > the live book's H1_Sharpe.  The record's own")
    say("  tape splits at ~2017, so the WHOLE first half sits in ZIRP.  An era-honest sweep pays 0 there, so")
    say("  the book's first half is BIT-IDENTICAL to the live book (free sweep) or strictly worse by the")
    say("  sleeve's turnover cost (held ETF).  Equal is not greater.  4a therefore fails at EVERY rate and")
    say("  EVERY F — not because the credit is small but because 4a has no window in which to see it.")
    say("  VERIFIED, not asserted (STEP@5.00%, F = 1.00, free sweep, vs the live book's own first half):")
    okh, dworst = True, 0.0
    for pan in panels:
        b = BARS[pan.name]
        fm = FRAMEW[pan.name]["LIVE"]
        r, tu, ts, ws, gs, cs = run_cell(pan, fm, REB[pan.name], pan.accrual(0.05, "STEP"), 1.00)
        rf = (r + ts * COST / 1e4)[WARMUP:]
        lv = b["lr"][WARMUP:]
        h = len(rf) // 2
        dmax = float(np.abs(rf[:h] - lv[:h]).max())
        dworst = max(dworst, dmax)
        say(f"    {pan.name:6} max |daily diff| over the first half = {dmax:.3e}   "
            f"H1 {sharpe(rf[:h]):.4f} vs live {sharpe(lv[:h]):.4f}   strictly greater? "
            f"{sharpe(rf[:h]) > sharpe(lv[:h])}")
    gate("G10 era-honest first half reproduces the live book to float precision (free sweep, 3 panels)",
         f"{dworst:.3e}", "<= 1e-15", dworst <= 1e-15)
    STP = AS[AS["shape"] == "STEP"]
    n_step_4a = int(STP.keep4a.sum() + STP.free_keep4a.sum())
    say(f"  EMPIRICAL CONFIRMATION: over the STEP a* scan — {len(STP)} (rung, panel-frame) cells, "
        f"both cost conventions — 4a passes {n_step_4a} times out of {2*len(STP)}.")

    # ================================================================ H4 — RULE 8 WALK-FORWARD
    say("\n" + "=" * 118)
    say("H4 — RULE 8 WALK-FORWARD.  Parameters chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE.")
    say("=" * 118)
    gate("G6 no chooser reads a row on/after 2017-01-01",
         f"IS slice is [WARMUP:{OOS_START}) by construction; IS end rows per panel: "
         + ", ".join(f"{p.name} {p.idx[p.i_oos-1].date()}" for p in panels),
         f"last IS date < {OOS_START}",
         all(p.idx[p.i_oos - 1] < pd.Timestamp(OOS_START) for p in panels))

    wf = []
    for pan in panels:
        b = BARS[pan.name]
        for fr in FRAMES:
            null = (arm_label("FLAT", 0.0), 0.00)
            nullO = triple(RET[(pan.name, fr, null[0], null[1])][b["i_oos"]:])
            # ---- PRIMARY: F chosen by IS Sharpe, A held at each environment value (legitimate)
            for sh in SHAPES:
                for a in GRID_A:
                    lab = arm_label(sh, a)
                    cells = [(lab, f) for f in GRID_F]
                    pick = max(cells, key=lambda c: (ISPK[(pan.name, fr, c[0], c[1])]["Sharpe"], -c[1]))
                    o = triple(RET[(pan.name, fr, pick[0], pick[1])][b["i_oos"]:])
                    wf.append(dict(panel=pan.name, frame=fr, chooser=f"C_F|A({sh},{a:.0%})",
                                   legit=True, pick=f"{pick[0]} F={pick[1]:.2f}",
                                   oCAGR=o["CAGR"], oSharpe=o["Sharpe"], oMaxDD=o["MaxDD"],
                                   d_oSharpe=o["Sharpe"] - nullO["Sharpe"],
                                   d_oCAGR=o["CAGR"] - nullO["CAGR"],
                                   beat_null=o["Sharpe"] > nullO["Sharpe"],
                                   beat_liveO=o["Sharpe"] > b["liveO"]["Sharpe"],
                                   beat_spyO=o["Sharpe"] > b["spyO"]["Sharpe"]))
            # ---- REPORTED, ILLEGITIMATE: joint (F, A) inside a shape
            for sh in SHAPES:
                cells = [(arm_label(sh, a), f) for a in GRID_A for f in GRID_F]
                for cname, key in [("C_JOINT_SHARPE", lambda c: ISPK[(pan.name, fr, c[0], c[1])]["Sharpe"]),
                                   ("C_JOINT_CAGR", None)]:
                    if key is None:
                        bar = DD_CAP * b["spyI"]["MaxDD"]
                        ok = [c for c in cells if ISPK[(pan.name, fr, c[0], c[1])]["MaxDD"] >= bar]
                        pick = max(ok, key=lambda c: ISPK[(pan.name, fr, c[0], c[1])]["CAGR"]) if ok else null
                    else:
                        pick = max(cells, key=key)
                    o = triple(RET[(pan.name, fr, pick[0], pick[1])][b["i_oos"]:])
                    wf.append(dict(panel=pan.name, frame=fr, chooser=f"{cname}({sh})", legit=False,
                                   pick=f"{pick[0]} F={pick[1]:.2f}",
                                   oCAGR=o["CAGR"], oSharpe=o["Sharpe"], oMaxDD=o["MaxDD"],
                                   d_oSharpe=o["Sharpe"] - nullO["Sharpe"],
                                   d_oCAGR=o["CAGR"] - nullO["CAGR"],
                                   beat_null=o["Sharpe"] > nullO["Sharpe"],
                                   beat_liveO=o["Sharpe"] > b["liveO"]["Sharpe"],
                                   beat_spyO=o["Sharpe"] > b["spyO"]["Sharpe"]))
            # ---- the SHY arm's own chooser over F (what the committed clause would have done)
            cells = [("SHY", f) for f in GRID_F]
            pick = max(cells, key=lambda c: (ISPK[(pan.name, fr, c[0], c[1])]["Sharpe"], -c[1]))
            o = triple(RET[(pan.name, fr, pick[0], pick[1])][b["i_oos"]:])
            wf.append(dict(panel=pan.name, frame=fr, chooser="C_F|SHY", legit=True,
                           pick=f"{pick[0]} F={pick[1]:.2f}",
                           oCAGR=o["CAGR"], oSharpe=o["Sharpe"], oMaxDD=o["MaxDD"],
                           d_oSharpe=o["Sharpe"] - nullO["Sharpe"], d_oCAGR=o["CAGR"] - nullO["CAGR"],
                           beat_null=o["Sharpe"] > nullO["Sharpe"],
                           beat_liveO=o["Sharpe"] > b["liveO"]["Sharpe"],
                           beat_spyO=o["Sharpe"] > b["spyO"]["Sharpe"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("OOS BARS (read once): " + ", ".join(
        f"{p.name} live {BARS[p.name]['liveO']['Sharpe']:.4f}/{BARS[p.name]['liveO']['CAGR']:.2%}, "
        f"SPY {BARS[p.name]['spyO']['Sharpe']:.4f}/{BARS[p.name]['spyO']['CAGR']:.2%}" for p in panels))
    for legit, tag in [(True, "LEGITIMATE (F chosen, A = environment)"),
                       (False, "ILLEGITIMATE (A treated as a dial), reported for contrast")]:
        d = WF[WF.legit == legit]
        say(f"\n  {tag}: {len(d)} picks")
        say(f"    mean d_oSharpe vs changing nothing {d.d_oSharpe.mean():+.4f}  "
            f"(beats null {int(d.beat_null.sum())}/{len(d)})")
        say(f"    mean d_oCAGR   vs changing nothing {d.d_oCAGR.mean()*100:+.4f} pp")
        say(f"    beats LIVE RULES v2 OOS Sharpe {int(d.beat_liveO.sum())}/{len(d)}   "
            f"beats SPY OOS Sharpe {int(d.beat_spyO.sum())}/{len(d)}")
        say(f"    picks F=1.00 in {int(d['pick'].str.endswith('F=1.00').sum())}/{len(d)}, "
            f"F=0.00 (changes nothing) in {int(d['pick'].str.endswith('F=0.00').sum())}/{len(d)}")
    say("\n  PER PANEL-FRAME, the SHY arm's own F chooser (what the committed clause would ship):")
    for r in WF[WF.chooser == "C_F|SHY"].itertuples():
        say(f"    {r.panel:6} {r.frame:5} picks {r.pick:16} OOS {r.oCAGR:7.2%} / {r.oSharpe:.4f} / "
            f"{r.oMaxDD:7.2%}   vs null {r.d_oSharpe:+.4f} Sharpe   beats live OOS {r.beat_liveO}")
    say("\n  THE SAME CHOOSER ON THE ZERO-DURATION TWIN at the era-honest STEP shape, a = 5%:")
    for pan in panels:
        for fr in FRAMES:
            d = WF[(WF.panel == pan.name) & (WF.frame == fr) & (WF.chooser == "C_F|A(STEP,5%)")]
            if len(d):
                r = d.iloc[0]
                say(f"    {pan.name:6} {fr:5} picks {r['pick']:16} OOS {r.oCAGR:7.2%} / {r.oSharpe:.4f} / "
                    f"{r.oMaxDD:7.2%}   vs null {r.d_oSharpe:+.4f} Sharpe   beats live OOS {r.beat_liveO}")

    # ================================================================ VERDICT
    say("\n" + "=" * 118)
    say("VERDICT")
    say("=" * 118)
    d1 = H1D[H1D.twin == "MATCH1"]
    dur_helps_sharpe = int((d1.dSharpe > 0).sum())
    dur_helps_dd = int((d1.dMaxDD > 0).sum())
    say(f"  Duration (SHY minus its matched zero-duration twin): helps Sharpe on {dur_helps_sharpe}/6 "
        f"panel-frames, helps MaxDD on {dur_helps_dd}/6, mean dSharpe {d1.dSharpe.mean():+.4f}, "
        f"mean dMaxDD {d1.dMaxDD.mean()*100:+.3f} pp, mean dCAGR {d1.dCAGR.mean()*100:+.4f} pp.")
    for sh in SHAPES:
        live_a = {k: v for k, v in ASTAR.items() if k[1] == "LIVE" and k[2] == sh}
        say(f"  Break-even accrual a* for 4a, LIVE frame, {sh} shape: " + ", ".join(
            f"{k[0]} {'never<=10%' if np.isnan(v['a4a']) else format(v['a4a'], '.2%')}"
            for k, v in live_a.items()))
    dl = WF[WF.legit]
    say(f"  Rule 8, legitimate choosers: mean d_oSharpe {dl.d_oSharpe.mean():+.4f} vs changing nothing, "
        f"beats the null {int(dl.beat_null.sum())}/{len(dl)}, beats live OOS {int(dl.beat_liveO.sum())}/{len(dl)}.")
    npass = int(GATES and sum(1 for g in GATES if g["target"] != "published, not asserted" and g["pass_"]))
    ntot = sum(1 for g in GATES if g["target"] != "published, not asserted")
    say(f"  GATES {npass}/{ntot}.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nWrote {Path(OUT).name}.grid.csv / .astar.csv / .duration.csv / .walkforward.csv / .gates.csv / .log.txt")
    say(f"Total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()

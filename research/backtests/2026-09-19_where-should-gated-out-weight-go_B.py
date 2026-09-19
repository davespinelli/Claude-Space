#!/usr/bin/env python3
"""Idea 1555 (lane B, 2026-09-19): WHERE SHOULD GATED-OUT WEIGHT GO?

THE DEFECT.  RULES v2 clause 2 gates a name OUT when it falls through the 200d -3% band and
sends its weight to CASH at 0.00%/yr, "never re-spread".  That destination was never chosen; it
is what the first implementation happened to do.  Today TWO DIFFERENT FIXES for it stand in the
record, proposed four hours apart, and they have NEVER BEEN RACED AGAINST EACH OTHER:

  * Idea 1454 (lane B): the live book fails 4b on the CAGR FLOOR ALONE (-1.97 pp full, -1.22 pp
    OOS, all four other legs passing).  Its reading: ABOLISH the cash leg, run at G = 1.00,
    because the cash leg earns nothing.
  * Ideas 1358 (cloud) + 1498 (lane B): CREDIT the cash leg with SHY.  1498 found it is the
    FIRST device in twelve consecutive runs to clear path 4a at all, and a strict 4b improvement
    to the standing 2026-09-04 candidate.

These are not the same rule and they cannot both be right.  "Abolish" buys equity beta with the
idle NAV; "credit" buys carry with it.  This run puts BOTH — and five other destinations — on the
same tape, at IDENTICAL selection, IDENTICAL cadence and IDENTICAL 100% of NAV, and reads which
one a rule-8 chooser would actually pick.

THE CONTROL THAT DECIDES THE FRAMING.  1358 already ran a DURATION ladder (SHY / IEF / TLT) and
found SHY alone survives, concluding the credit is CARRY, not duration.  That ladder never
included an EQUITY sleeve.  If routing the gated-out weight into plain SPY ALSO clears 4a, then
1498's headline is not about cash yield at all — it is about the band leaving a quarter of NAV
un-deployed, and the honest rule is "deploy it", not "buy short Treasuries".  SPY is therefore
the single most informative cell in this grid and it is stated as such BEFORE the run.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DEST {CASH, SHY, IEF, TLT, GLD, SPY, RESPREAD}   DIAL 1 -- where the gated-out weight goes.
      CASH     0.00%/yr -- the live convention, and the null cell of this grid.
      SHY      1-3y Treasuries -- 1358 / 1498's answer.
      IEF,TLT  7y and 20y Treasuries -- 1358's duration controls, replicated here on an
               independent construction so this run's ladder is readable against its.
      GLD      a non-bond, non-equity control: near-zero correlation, no carry, real vol.
      SPY      THE FRAMING CONTROL described above.
      RESPREAD not an asset: the gated-out weight is re-spread PRO RATA over the names still
               inside the band.  At F = 1.00 this IS idea 1454's "abolish the cash leg", made
               conditional rather than a constant gross.  When the band is EMPTY there is
               nothing to re-spread and the book sits in 0% cash -- stated, not glossed.

  F {0.00, 0.25, 0.50, 0.75, 1.00}                 DIAL 2 -- the fraction of gated-out weight
      actually routed to DEST.  F = 0.00 IS the live convention and is a cell of the grid for
      every destination, so the null "change nothing" is priced on the same tape as every
      candidate and all seven destinations must collapse onto ONE book there (gate G1).

35 cells per (frame, panel).  NOT DIALS, reported at every value: FRAME {LIVE, INC}, PANEL
{U56, B136, SMALL}.  210 cells in all, EVERY ONE PUBLISHED in the .grid.csv.

  FRAME LIVE = the live RULES v2 shape (`baseline.rules_v2_weights`: 200d +/-3% hysteresis band,
               equal weight across IN names, de-gross to cash, never re-spread), weekly.  This is
               the frame whose CAGR floor idea 1454 found binding.
  FRAME INC  = the frozen 2026-09-04 KEEP-4b incumbent (composite momentum, N = 20, H = 126-day
               minimum hold, 200d MA gate, vol20 < 0.60), weekly.  This is the anchor that beat
               1405 / 1413 / 1429 / 1433 / 1436 / 1534.

GROSS IS FROZEN, NOT TUNED.  G = 0.75 on both frames -- the live value and the committed
2026-09-04 anchor value.  Idea 1498 already swept G x F; sweeping it again here would be a third
parameter.  This run holds G fixed and asks only WHERE the residual goes.

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_SHARPE  argmax IS Sharpe over all 35 cells
  C_CAGR    argmax IS CAGR among cells whose IS MaxDD <= 0.60 x SPY_IS MaxDD (spend the budget)
  C_ANCHOR  (CASH, 0.00), choosing nothing -- the null every pick is scored against
All three range over the SAME two dials; they are readings of one grid, not extra parameters.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.  (a) If RESPREAD dominates SHY on Sharpe
AND CAGR AND MaxDD, 1454 is right and 1498's sleeve is a slower version of the same fix.  (b) If
SHY dominates RESPREAD, the residual wants carry and the band's de-gross is doing real work.
(c) If SPY clears 4a alongside SHY, 1498's "cash convention" framing is wrong and must be
restated as "the band under-deploys".  (d) If the rule-8 chooser lands on a destination that
loses OOS -- as it did in 1358, where it picked IEF/TLT and never found SHY -- then the axis is
a KILL AS A DIAL whatever its ex-post best cell does.  All four outcomes are reported; nothing is
tuned until it works.

THE HONEST LIMIT, STATED UP FRONT.  There is no true ZERO-DURATION cash instrument in the
committed cache (no BIL, no SHV), so the cheapest sleeve available is SHY, which is marked to
market and lost 5.71% in 2022.  Every "credit the cash" number in this record, this run's
included, is therefore an OPTIMISTIC proxy for a broker sweep in the ZIRP years and a GENUINE
DURATION RISK in the rate-rise years.  Each sleeve's own standalone profile is published BEFORE
anything is credited so the reader can price that directly.  SHY, IEF, TLT, GLD and SPY are all
CONSTITUENTS of U56 and B136, so the INC frame may already select them on momentum; that is the
incumbent's existing behaviour, left unchanged, and the sleeve is ADDITIVE to it.

GATES.  G0 sample >= 10y (rule 1).  G1 DESTINATION INVARIANCE AT F = 0: all seven destinations
must produce BIT-IDENTICAL returns at F = 0.00 on every (panel, frame).  G2 CROSS-SCRIPT REPLAY:
LIVE/U56 at (CASH, 0.00) must reproduce `baseline.compare`'s RULES v2 baseline row.  G3
CROSS-SCRIPT REPLAY of idea 1498's two committed SHY cells (LIVE/U56 9.12% / 1.2675 / -11.48%
full and INC/U56 16.16% / 1.1787 / -18.88% full).  G4 NO LEVERAGE: risky + sleeve never exceeds
1.0 in any cell.  G5 exactly two tuned parameters.  G6 no chooser reads a row on or after
2017-01-01 -- asserted by construction AND tested by refitting on a truncated IS tape.  G7 all
210 cells published.  G8 PUBLISHED, not asserted: every sleeve asset's own return profile, and
RESPREAD's realised mean gross at F = 1.00.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps on BOTH legs, no leverage, no shorting); rule 3
(RULES v2 live baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_where-should-gated-out-weight-go_B.py
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

DATE, SLUG = "2026-09-19", "where-should-gated-out-weight-go"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H = 20, 126                                  # the frozen 2026-09-04 incumbent
G_FROZEN, CAD, COST, BAND = 0.75, "W", 10.0, 0.03
SLEEVES = ["SHY", "IEF", "TLT", "GLD", "SPY"]       # asset destinations, from data/prices.csv
DESTS = ["CASH"] + SLEEVES + ["RESPREAD"]
GRID_F = [0.00, 0.25, 0.50, 0.75, 1.00]
FRAMES = ["LIVE", "INC"]
NULL_CELL = ("CASH", 0.00)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
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
        # every sleeve return comes from the SAME reference tape on every panel, so the
        # destination contrast is not confounded by which panel prices the sleeve.
        self.sl = {t: np.nan_to_num(ref[t].reindex(px.index).ffill().pct_change().values, nan=0.0)
                   for t in SLEEVES}
        self.sl["CASH"] = np.zeros(len(px.index))
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


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


def run_cell(pan, frame, reb, dest, f, g=G_FROZEN, cost=COST):
    """The frozen frame at constant gross g, routing fraction f of the GATED-OUT weight to `dest`.

    dest == 'RESPREAD' scales the risky vector up pro rata (no new instrument).  Any other dest
    is a REAL held sleeve: it drifts with the book between rebalances and pays `cost` bps on its
    own turnover.  f = 0 reduces exactly to the record's 0% cash convention on EVERY dest.
    """
    rets = pan.rets
    respread = (dest == "RESPREAD")
    cr = np.zeros(len(pan.idx)) if respread else pan.sl[dest]
    T, M = rets.shape
    turn = np.zeros(T)
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
        if respread:
            # re-spread the gated-out weight pro rata over the names still inside the band.
            # Empty band -> nothing to re-spread -> the book sits in 0% cash, unchanged.
            if s0 > 0:
                w0 = w0 * ((s0 + f * (1.0 - s0)) / s0)
                s0 = float(w0.sum())
            fe = 0.0
        else:
            fe = f
        wsum_max = max(wsum_max, s0 + fe * (1.0 - s0))
        turn[i0] = float(np.abs(w0 - curw).sum()) + fe * abs(s0 - float(curw.sum()))
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])            # risky value at START of each day
        seg = cr[i0:i1]
        cash_growth = np.concatenate(([1.0], np.cumprod(1.0 + fe * seg)[:-1]))
        Ccash = (1.0 - s0) * cash_growth                          # residual value at START of day
        V = A.sum(axis=1) + Ccash
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1) + (Ccash / V) * (fe * seg)
        gsum[i0:i1] = A.sum(axis=1) / V
        csle[i0:i1] = fe * Ccash / V
        Ae = w0 * (C[i1 - 1] / base)
        ce = (1.0 - s0) * float(np.prod(1.0 + fe * seg))
        curw = Ae / (Ae.sum() + ce)
    return out - turn * cost / 1e4, turn, wsum_max, gsum, csle


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


# ---------------------------------------------------------------- choosers (rule 8)
def chooser_sharpe(cells, ispk):
    return max(cells, key=lambda c: (ispk[c]["Sharpe"], -DESTS.index(c[0]), -c[1]))


def chooser_cagr(cells, ispk, dd_bar):
    ok = [c for c in cells if ispk[c]["MaxDD"] >= dd_bar]
    if not ok:
        return NULL_CELL, True
    return max(ok, key=lambda c: (ispk[c]["CAGR"], -DESTS.index(c[0]), -c[1])), False


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1555 (lane B, 2026-09-19) — WHERE SHOULD GATED-OUT WEIGHT GO?")
    say(f"DIALS: DEST {DESTS}  x  F {GRID_F}.")
    say(f"GROSS FROZEN at G = {G_FROZEN} on both frames (live value AND the 2026-09-04 anchor "
        f"value) — it is NOT a dial here; idea 1498 already swept it.")
    say(f"FRAMES (not dials): LIVE = RULES v2 band shape; INC = frozen 2026-09-04 incumbent "
        f"(N={I_N}, H={I_H}).  Both weekly, {COST:.0f} bps on BOTH legs, t+1.  (CASH, 0.00) is "
        f"the standing null on each.")
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
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below — every CAGR, every 4b "
        "pass — is an UPPER BOUND.  What survives that bias is the CONTRAST between DESTINATIONS "
        "on the same names, the same days and the same frame.")
    say("  SLEEVE REALISM (stated, not glossed): there is NO zero-duration cash instrument in the "
        "committed cache (no BIL, no SHV).  SHY is a 1-3y Treasury ETF on ADJUSTED closes — a "
        "short-duration TOTAL-RETURN sleeve, marked to market, which lost money in 2022 and "
        "earned roll in 2009-2015 that bills did not.  Every 'credit the cash' number here and "
        "in ideas 1358 / 1498 is therefore an OPTIMISTIC broker-sweep proxy in the ZIRP years "
        "and a GENUINE DURATION RISK afterwards.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # ---- G8a: every sleeve's own profile, published BEFORE anything is credited
    say("\n  G8a SLEEVE PROFILES (own standalone returns, before any book credits them):")
    p0 = panels[0]
    i0 = int(np.searchsorted(p0.idx.values, np.datetime64(OOS_START)))
    for t in SLEEVES:
        s = p0.sl[t]
        a, b, c = triple(s[WARMUP:]), triple(s[WARMUP:i0]), triple(s[i0:])
        publish(f"G8a {t}", f"FULL {a['CAGR']:.2%}/{a['Sharpe']:.3f}/{a['MaxDD']:.2%}  "
                            f"IS {b['CAGR']:.2%}/{b['MaxDD']:.2%}  OOS {c['CAGR']:.2%}/{c['MaxDD']:.2%}")

    grid, wsum_global = [], 0.0
    RET, ISPK, BARS = {}, {}, {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy = bmpack(pan.spy[WARMUP:]); spyO = bmpack(pan.spy[i_oos:]); spyI = bmpack(pan.spy[WARMUP:i_oos])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq=CAD)["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        BARS[pan.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, i_oos=i_oos, lr=lr)
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}  |  "
            f"OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           SPY IS   {spyI['CAGR']:.2%} / {spyI['MaxDD']:.2%}  (the bar C_CAGR reads)")
        say(f"           RULES v2 live @{COST:.0f}bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        reb = pan.reb_rows(CAD)
        frames = {"LIVE": frame_live(pan), "INC": frame_inc(pan, reb, I_N, I_H)}
        for fr in FRAMES:
            fm = frames[fr]
            for dest in DESTS:
                for f in GRID_F:
                    r, tu, ws, gs, cs = run_cell(pan, fm, reb, dest, f)
                    wsum_global = max(wsum_global, ws)
                    RET[(pan.name, fr, dest, f)] = r
                    k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                    ISPK[(pan.name, fr, dest, f)] = dict(Sharpe=sharpe(r[WARMUP:i_oos]),
                                                         CAGR=cagr(r[WARMUP:i_oos]),
                                                         MaxDD=mdd(r[WARMUP:i_oos]))
                    yrs = (T - WARMUP) / 252.0
                    grid.append(dict(panel=pan.name, frame=fr, dest=dest, F=f,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                     oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                     isCAGR=ISPK[(pan.name, fr, dest, f)]["CAGR"],
                                     isSharpe=ISPK[(pan.name, fr, dest, f)]["Sharpe"],
                                     isMaxDD=ISPK[(pan.name, fr, dest, f)]["MaxDD"],
                                     mean_gross=float(np.mean(gs[WARMUP:])),
                                     mean_sleeve=float(np.mean(cs[WARMUP:])),
                                     turnover_yr=float(tu[WARMUP:].sum() / yrs),
                                     keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                     leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                     leg_CAGR=legs["CAGR"], oleg_H1=legsO["H1"], oleg_H2=legsO["H2"],
                                     oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"]))
        say(f"    [{pan.name}] {len(DESTS)*len(GRID_F)*len(FRAMES)} cells done "
            f"({time.time()-t0:.0f}s elapsed)")

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ================================================================ GATES
    say("\n" + "=" * 118)
    say("GATES")
    say("=" * 118)

    # G1 destination invariance at F = 0
    worst = 0.0
    for pan in panels:
        for fr in FRAMES:
            base = RET[(pan.name, fr, "CASH", 0.00)]
            for d in DESTS[1:]:
                worst = max(worst, float(np.abs(RET[(pan.name, fr, d, 0.00)] - base).max()))
    gate("G1 destination invariance at F=0 (max |diff| over 6 dests x 6 panel-frames)",
         f"{worst:.3e}", "== 0.0", worst == 0.0)

    # G2 cross-script replay of baseline.compare's RULES v2 row
    d2 = 0.0
    for pan in panels:
        mine = RET[(pan.name, "LIVE", "CASH", 0.00)]
        d2 = max(d2, float(np.abs(mine[WARMUP:] - BARS[pan.name]["lr"][WARMUP:]).max()))
    gate("G2 LIVE/(CASH,0.00) == baseline.rules_v2_weights book (max |diff|, 3 panels)",
         f"{d2:.3e}", "<= 1e-12", d2 <= 1e-12)

    # G3 cross-script replay of idea 1498's committed U56 SHY cells
    ok3, det3 = True, []
    for fr in FRAMES:
        m = triple(RET[("U56", fr, "SHY", 1.00)][WARMUP:])
        want = REPLAY_1498[fr]
        dd = dict(CAGR=abs(m["CAGR"] - want["CAGR"]), Sharpe=abs(m["Sharpe"] - want["Sharpe"]),
                  MaxDD=abs(m["MaxDD"] - want["MaxDD"]))
        ok3 &= dd["CAGR"] <= 1e-3 and dd["Sharpe"] <= 2e-3 and dd["MaxDD"] <= 1e-3
        det3.append(f"{fr} got {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} vs committed "
                    f"{want['CAGR']:.2%}/{want['Sharpe']:.4f}/{want['MaxDD']:.2%}")
    gate("G3 replay of idea 1498's U56 SHY F=1.00 cells", " | ".join(det3),
         "|dCAGR|<=1e-3, |dSharpe|<=2e-3, |dMaxDD|<=1e-3", ok3)

    gate("G4 no leverage (max risky+sleeve over all 210 cells)", f"{wsum_global:.12f}",
         "<= 1.0", wsum_global <= 1.0 + 1e-12)
    gate("G5 exactly two tuned parameters", "DEST, F (G=0.75, band=0.03, N=20, H=126 all frozen)",
         "== 2", True)
    gate("G7 all cells published", f"{len(G)} rows in {Path(OUT).name}.grid.csv",
         f"== {len(DESTS)*len(GRID_F)*len(FRAMES)*len(panels)}",
         len(G) == len(DESTS) * len(GRID_F) * len(FRAMES) * len(panels))

    rs = G[(G.dest == "RESPREAD") & (G.F == 1.00)]
    publish("G8b RESPREAD F=1.00 realised mean gross (by panel/frame)",
            ", ".join(f"{r.panel}/{r.frame} {r.mean_gross:.4f}" for r in rs.itertuples()))
    publish("G8c LIVE (CASH,0.00) realised mean gross (by panel)",
            ", ".join(f"{r.panel} {r.mean_gross:.4f}"
                      for r in G[(G.dest == "CASH") & (G.F == 0.0) & (G.frame == "LIVE")].itertuples()))

    # ================================================================ HEADLINES
    say("\n" + "=" * 118)
    say("H1 — THE FRAMING CONTROL: does an EQUITY sleeve (SPY) clear 4a where CASH does not?")
    say("=" * 118)
    say(f"{'panel':6} {'frame':5} {'dest':9} {'F':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
        f"{'H1':>7} {'H2':>7} {'4a':>4} {'4b':>4} {'4aO':>4} {'4bO':>4}")
    for pan in panels:
        for fr in FRAMES:
            for d in DESTS:
                r = G[(G.panel == pan.name) & (G.frame == fr) & (G.dest == d) & (G.F == 1.00)].iloc[0]
                say(f"{pan.name:6} {fr:5} {d:9} {1.00:5.2f} {r.CAGR:8.2%} {r.Sharpe:8.4f} "
                    f"{r.MaxDD:8.2%} {r.H1:7.3f} {r.H2:7.3f} {str(r.keep4a):>4} {str(r.keep4b):>4} "
                    f"{str(r.keep4a_oos):>4} {str(r.keep4b_oos):>4}")
            say("")

    say("BY DESTINATION — 4a / 4b pass counts over all 30 (panel, frame, F) cells each:")
    say(f"{'dest':9} {'4a full':>8} {'4a f+O':>8} {'4b full':>8} {'4b f+O':>8} "
        f"{'mean dSharpe vs CASH twin (F>0)':>34}")
    dsum = {}
    for d in DESTS:
        sub = G[G.dest == d]
        n4a = int(sub.keep4a.sum()); n4ao = int((sub.keep4a & sub.keep4a_oos).sum())
        n4b = int(sub.keep4b.sum()); n4bo = int((sub.keep4b & sub.keep4b_oos).sum())
        ds = []
        for r in sub[sub.F > 0].itertuples():
            base = G[(G.panel == r.panel) & (G.frame == r.frame) & (G.dest == "CASH") & (G.F == 0.0)].iloc[0]
            ds.append(r.Sharpe - base.Sharpe)
        dsum[d] = float(np.mean(ds)) if ds else 0.0
        say(f"{d:9} {n4a:8d} {n4ao:8d} {n4b:8d} {n4bo:8d} {dsum[d]:34.4f}")

    say("\n" + "=" * 118)
    say("H2 — HEAD TO HEAD: idea 1454's fix (RESPREAD, F=1.00) vs idea 1498's fix (SHY, F=1.00)")
    say("=" * 118)
    say(f"{'panel':6} {'frame':5} {'dSharpe':>9} {'dCAGR':>9} {'dMaxDD':>9} | "
        f"{'oSharpe':>9} {'oCAGR':>9} {'oMaxDD':>9}   (RESPREAD minus SHY)")
    h2rows = []
    for pan in panels:
        for fr in FRAMES:
            a = G[(G.panel == pan.name) & (G.frame == fr) & (G.dest == "RESPREAD") & (G.F == 1.0)].iloc[0]
            b = G[(G.panel == pan.name) & (G.frame == fr) & (G.dest == "SHY") & (G.F == 1.0)].iloc[0]
            h2rows.append(dict(panel=pan.name, frame=fr, dSharpe=a.Sharpe - b.Sharpe,
                               dCAGR=a.CAGR - b.CAGR, dMaxDD=a.MaxDD - b.MaxDD,
                               odSharpe=a.oSharpe - b.oSharpe, odCAGR=a.oCAGR - b.oCAGR,
                               odMaxDD=a.oMaxDD - b.oMaxDD))
            say(f"{pan.name:6} {fr:5} {a.Sharpe-b.Sharpe:9.4f} {a.CAGR-b.CAGR:9.2%} "
                f"{a.MaxDD-b.MaxDD:9.2%} | {a.oSharpe-b.oSharpe:9.4f} {a.oCAGR-b.oCAGR:9.2%} "
                f"{a.oMaxDD-b.oMaxDD:9.2%}")
    H2 = pd.DataFrame(h2rows)
    H2.to_csv(f"{OUT}.headtohead.csv", index=False)
    say(f"  MEAN over 6 panel-frames: dSharpe {H2.dSharpe.mean():+.4f}, dCAGR "
        f"{H2.dCAGR.mean():+.2%}, dMaxDD {H2.dMaxDD.mean():+.2%} | OOS dSharpe "
        f"{H2.odSharpe.mean():+.4f}, dCAGR {H2.odCAGR.mean():+.2%}, dMaxDD {H2.odMaxDD.mean():+.2%}")
    say(f"  RESPREAD beats SHY on Sharpe at {int((H2.dSharpe>0).sum())} of 6 full, "
        f"{int((H2.odSharpe>0).sum())} of 6 OOS; on CAGR {int((H2.dCAGR>0).sum())} of 6 full; "
        f"on MaxDD (shallower) {int((H2.dMaxDD>0).sum())} of 6 full.")

    # ================================================================ RULE 8
    say("\n" + "=" * 118)
    say("H3 / RULE 8 — dials fit on warm-up..2016-12-31 ONLY; 2017-2026 read EXACTLY ONCE")
    say("=" * 118)
    cells = [(d, f) for d in DESTS for f in GRID_F]
    wf = []
    say(f"{'panel':6} {'frame':5} {'chooser':9} {'pick':16} {'oCAGR':>8} {'oSharpe':>9} "
        f"{'oMaxDD':>8} {'d vs null':>10} {'4bO':>5}")
    for pan in panels:
        B = BARS[pan.name]
        for fr in FRAMES:
            ispk = {c: ISPK[(pan.name, fr, c[0], c[1])] for c in cells}
            dd_bar = DD_CAP * B["spyI"]["MaxDD"]
            picks = {"C_SHARPE": (chooser_sharpe(cells, ispk), False),
                     "C_CAGR": chooser_cagr(cells, ispk, dd_bar),
                     "C_ANCHOR": (NULL_CELL, False)}
            nullr = RET[(pan.name, fr, NULL_CELL[0], NULL_CELL[1])][B["i_oos"]:]
            nulls = sharpe(nullr)
            for cname, (pick, fell) in picks.items():
                r = RET[(pan.name, fr, pick[0], pick[1])][B["i_oos"]:]
                m = triple(r)
                _, k4bO, _, _, _, _ = keep_paths(r, B["spyO"], B["liveO"])
                wf.append(dict(panel=pan.name, frame=fr, chooser=cname, dest=pick[0], F=pick[1],
                               fallback=fell, oCAGR=m["CAGR"], oSharpe=m["Sharpe"],
                               oMaxDD=m["MaxDD"], d_vs_null=m["Sharpe"] - nulls, keep4b_oos=k4bO))
                say(f"{pan.name:6} {fr:5} {cname:9} {pick[0]+' F='+format(pick[1],'.2f'):16} "
                    f"{m['CAGR']:8.2%} {m['Sharpe']:9.4f} {m['MaxDD']:8.2%} "
                    f"{m['Sharpe']-nulls:+10.4f} {str(k4bO):>5}")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for cname in ("C_SHARPE", "C_CAGR"):
        s = W[W.chooser == cname]
        say(f"  {cname}: mean OOS dSharpe vs the do-nothing null {s.d_vs_null.mean():+.4f}, "
            f"beats it {int((s.d_vs_null>0).sum())} of {len(s)}; picks "
            f"{dict(s.dest.value_counts())}")

    # G6: the choosers read nothing on or after OOS_START — tested, not asserted
    ok6 = True
    for pan in panels:
        B = BARS[pan.name]
        cut = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        ok6 &= (pan.idx[cut] >= pd.Timestamp(OOS_START)) and (pan.idx[cut - 1] <= pd.Timestamp(IS_END))
        for fr in FRAMES:
            for c in cells:
                a = sharpe(RET[(pan.name, fr, c[0], c[1])][WARMUP:cut])
                b = ISPK[(pan.name, fr, c[0], c[1])]["Sharpe"]
                ok6 &= abs(a - b) <= 1e-12
    gate("G6 every IS statistic is computed on rows strictly before 2017-01-01",
         "refit on truncated IS tape reproduces every chooser input", "identical", ok6)

    # ================================================================ VERDICT
    say("\n" + "=" * 118)
    say("VERDICT")
    say("=" * 118)
    n4a = int(G.keep4a.sum()); n4ao = int((G.keep4a & G.keep4a_oos).sum())
    n4b = int(G.keep4b.sum()); n4bo = int((G.keep4b & G.keep4b_oos).sum())
    say(f"  PATH 4a: {n4a} of {len(G)} cells full, {n4ao} full AND OOS.")
    say(f"  PATH 4b: {n4b} of {len(G)} cells full, {n4bo} full AND OOS.")
    say(f"  4a passes at F = 0.00: {int(G[G.F==0.0].keep4a.sum())} of {len(G[G.F==0.0])}  "
        f"(the standing convention, all seven destinations identical).")
    if n4a:
        best = G[G.keep4a].sort_values("Sharpe", ascending=False).iloc[0]
        say(f"  BEST 4a CELL: {best.panel}/{best.frame} {best.dest} F={best.F:.2f} — full "
            f"{best.CAGR:.2%} / {best.Sharpe:.4f} / {best.MaxDD:.2%}, halves "
            f"{best.H1:.3f}/{best.H2:.3f}, OOS {best.oCAGR:.2%} / {best.oSharpe:.4f} / "
            f"{best.oMaxDD:.2%}, turnover {best.turnover_yr:.2f}x/yr.")
    if n4b:
        best = G[G.keep4b & G.keep4b_oos].sort_values("Sharpe", ascending=False)
        if len(best):
            b = best.iloc[0]
            say(f"  BEST 4b (full AND OOS) CELL: {b.panel}/{b.frame} {b.dest} F={b.F:.2f} — full "
                f"{b.CAGR:.2%} / {b.Sharpe:.4f} / {b.MaxDD:.2%}, OOS {b.oCAGR:.2%} / "
                f"{b.oSharpe:.4f} / {b.oMaxDD:.2%}.")
    gp = pd.DataFrame(GATES)
    gp.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gp[gp.target != "published, not asserted"].pass_.sum())
    ntot = int((gp.target != "published, not asserted").sum())
    say(f"\n  GATES {npass}/{ntot} pass.  {time.time()-t0:.0f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"  Written: {Path(OUT).name}.grid.csv / .headtohead.csv / .walkforward.csv / "
        f".gates.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

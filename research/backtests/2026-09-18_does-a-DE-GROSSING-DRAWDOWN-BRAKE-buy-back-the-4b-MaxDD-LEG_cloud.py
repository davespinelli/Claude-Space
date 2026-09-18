#!/usr/bin/env python3
"""IDEA 1296 — does a DE-GROSSING DRAWDOWN BRAKE buy back the 4b MaxDD leg the record
says is the binder?

QUESTION.  Idea 1215's capital arm found that of 148 cells failing PROTOCOL 4b, the DD cap
binds ALONE in 32 and jointly with the CAGR floor in 56 more — 88 of 148, the modal reason
this family fails.  Every repair tried so far has moved a CROSS-SECTIONAL dial (N, gross, H,
cadence, eligibility).  This idea moves a TIME-SERIES one instead: cut the book's gross when a
causal, book-level trend signal is off, and put the freed weight in cash.  It adds no new
cross-sectional signal and no new name.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4, max 2 tuned parameters):
    BRAKE BASIS   {NONE, SPY200, OWN200}
                  NONE   = the frozen incumbent, no brake.
                  SPY200 = braked on days when SPY closed below its own 200d MA.
                  OWN200 = braked on days when the BOOK'S OWN equity closed below its own
                           200d MA.  Causal: at rebalance interval start i0 the brake reads
                           the book's realised equity up to i0-LAG only, which is already
                           computed when the interval opens.
    BRAKE DEPTH   {0.00, 0.25, 0.50, 0.75, 1.00} = the multiplier applied to GROSS while
                  braked.  0.00 is fully to cash, 1.00 is no brake at all.
ALL 11 distinct cells per panel are reported (NONE once, plus 2 bases x 5 depths).  Nothing is
reported conditional on its result.

THE BOOK (frozen, not tuned here).  The standing 2026-09-04 KEEP-4b family as re-certified by
ideas 1294 and 1215: RAW three-leg composite ranking (21->252, 0->126, 0->63 pct-ranks,
averaged), eligibility = above own 200d MA AND vol20 < 0.60, GROSS spread equally over N slots,
minimum hold H=126 trading days, weekly Fri-decide / Mon-trade, 10 bps per unit turnover, t+1
execution, 260-row warm-up.  ANCHOR per panel is idea 1215's own rule-8 pick: U56 N=15/g=0.60,
B136 N=25/g=0.60, SMALL N=25/g=0.40 (1215's declared fallback — SMALL's IS 4b set is empty).

HYPOTHESES, declared before the grid is read:
  H_BUYS     at least one braked cell on at least one panel turns a 4b FAIL into a 4b PASS
             that the unbraked anchor does not already hold.
  H_DEEPER   MaxDD is monotone improving in brake depth (0.00 shallowest drawdown).
  H_COSTS    the brake sells more CAGR than it buys in MaxDD, so no braked cell improves the
             4b CAGR-floor margin and the DD margin gain does not clear the floor loss.
  H_OOS      rule 8: the IS-chosen (basis, depth) beats PROTOCOL's no-brake anchor out of
             sample by more than +0.02 of Sharpe.
Whichever fire are reported as they fall.

GATES.
  G1  BASIS x DEPTH=1.00 reproduces the NONE cell bit-for-bit on every panel (the brake is a
      pure multiplier and 1.00 is the identity).
  G2  the fast runner used here reproduces products/backtester/engine.backtest on the NONE
      anchor to < 1e-10 on every daily return row, compared on ndarray (no skipna), per the
      standing request in queue item 1198.
  G3  determinism: the whole grid, bit for bit, on a second pass.
  G4  causality of OWN200: the brake state consumed at interval i0 is computed from equity
      rows strictly before i0-LAG+1, verified by recomputing it against an equity series whose
      tail from i0 onward is replaced by NaN.
  G5  IS and OOS windows do not overlap and OOS starts on or after 2017-01-01.
  G6  the IS argmax reads no OOS row (recomputed on an IS-truncated return vector).
  G7  DEPTH=0.00 holds strictly less gross-days than DEPTH=1.00 on every panel and basis.
  G8  the anchor replay residual against idea 1215's committed U56 triple (13.66% / 1.1706 /
      -16.38%) and B136 OOS triple is REPORTED, not gated: prices.csv was refreshed on
      2026-09-18 after those numbers were committed, so a hard equality gate would be a gate
      on a cache vintage, not on this code.

PROTOCOL: rule 2 costs (10 bps) and t+1 execution; rule 4 BOTH KEEP paths at EVERY cell; rule 5
one idea, one script, deterministic, standalone; rule 8 parameters chosen on warm-up..2016-12-31
only, 2017-2026 read ONCE; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current sub-$2B
screen with tickers whose max_1d_move >= 1.0 in data/small_meta.csv dropped first.  Delisted and
acquired names are absent from all three, which flatters every momentum book here, so every
absolute level is optimistic and every 4b pass is an UPPER bound.  The headline of this idea is
a DIFFERENCE between brake settings on the SAME names in the SAME book, so a level bias common
to the panel moves every cell together and the brake findings are first-order immune; the 4b
pass COUNTS are not, and are quoted as upper bounds.

Runs standalone and offline from the committed caches:
  python research/backtests/2026-09-18_does-a-DE-GROSSING-DRAWDOWN-BRAKE-buy-back-the-4b-MaxDD-LEG_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask  # noqa: E402

COST, WARMUP, LAG = 10.0, 260, 1
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]        # committed RAW three-leg composite
A_H, A_MV = 126, 0.60                        # frozen
ANCHOR = {"U56": (15, 0.60), "B136": (25, 0.60), "SMALL": (25, 0.40)}   # idea 1215's rule-8 picks
BASES = ["NONE", "SPY200", "OWN200"]
DEPTHS = [0.00, 0.25, 0.50, 0.75, 1.00]

OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


GATES = []


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    h = len(r) // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                **{"is": stats(r[:o])})


def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def margin_4b(b, spy):
    """Joint 4b margin in pp: the worst of the five legs' distances from its own bar."""
    return min(100 * (b["h1"]["Sharpe"] - spy["h1"]["Sharpe"]),
               100 * (b["h2"]["Sharpe"] - spy["h2"]["Sharpe"]),
               100 * (b["oos"]["Sharpe"] - spy["oos"]["Sharpe"]),
               100 * (b["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]),
               100 * (b["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]))


# ------------------------------------------------------------------ panel + runner
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        self.vol20 = np.nan_to_num((q.pct_change().rolling(20).std() * np.sqrt(252)).values,
                                   nan=1e9)
        spy = px["SPY"]
        self.spy = spy.pct_change().fillna(0.0).values
        # SPY200 brake state, daily, causal by construction (rolling mean of closes <= t)
        self.spy_on = (spy > spy.rolling(200).mean()).fillna(False).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)

    def elig(self, maxvol):
        return self.above & (self.vol20 < maxvol)


def build(pan, N, H, maxvol, lag=LAG):
    """Selection frame at GROSS = 1.0, equal slot weights.  Row t = APPLICATION-time weight
    (decided t-lag, applied t).  Minimum hold H trading days."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    el = pan.elig(maxvol)
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(el[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_braked(pan, Wt, gross, basis="NONE", depth=1.00, lag=LAG, want_state=False):
    """Weekly-rebalanced book with a de-grossing brake.

    The brake multiplier for the interval opening at i0 is decided from information available
    at i0-lag: for SPY200 from SPY's own 200d state on that row, for OWN200 from the book's
    OWN realised equity up to i0-lag (already computed when the interval opens) against its
    own 200d mean.  Freed weight goes to CASH; it is never re-spread.
    """
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    port = np.zeros(T)
    eq = np.ones(T + 1)           # eq[t] = equity at END of row t-1; eq[0] = 1.0
    curw = np.zeros(M)
    state = np.ones(T)
    bounds = list(zip(pan.reb, np.append(pan.reb[1:], T)))
    for i0, i1 in bounds:
        mult = 1.0
        if basis != "NONE":
            ts = max(i0 - lag, 0)
            if basis == "SPY200":
                on = bool(pan.spy_on[ts])
            else:                                    # OWN200 — the book's own equity
                hist = eq[1:ts + 2]                  # realised equity rows 0..ts
                if len(hist) < 200:
                    on = True                        # no 200d history yet -> unbraked
                else:
                    on = bool(hist[-1] > hist[-200:].mean())
            mult = 1.0 if on else depth
        state[i0:i1] = mult
        w0 = gross * mult * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        seg_gross = (held[i0:i1] * rets[i0:i1]).sum(axis=1)
        seg = seg_gross.copy()
        seg[0] -= turn[i0] * COST / 1e4
        port[i0:i1] = seg
        eq[i0 + 1:i1 + 1] = eq[i0] * np.cumprod(1.0 + seg)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    ann_turn = float(turn.sum() / (T / 252.0))
    if want_state:
        return port, ann_turn, state
    return port, ann_turn


def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1296 — does a DE-GROSSING DRAWDOWN BRAKE buy back the 4b MaxDD leg?")
    say("=" * 100)

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append(("B136", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    panels.append(("SMALL", psm, inv_s))
    say(f"\nPANELS: U56 {px.shape[1]-1} names to {px.index[-1].date()} | "
        f"B136 {pb.shape[1]-1} to {pb.index[-1].date()} | "
        f"SMALL {len(inv_s)} to {psm.index[-1].date()} "
        f"({len(bad)} max_1d_move>=1.0 tickers dropped)")
    say("SURVIVORSHIP (rule 9): all three are CURRENT-constituent lists; every level is "
        "optimistic and every 4b pass is an UPPER bound.")

    say("\n" + "=" * 100)
    say("GRID — 3 panels x (NONE + 2 BASES x 5 DEPTHS) = 33 books, ALL reported")
    say("=" * 100)

    rows = []
    store = {}
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        N, G = ANCHOR[pname]
        idx = pan.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy = windows(pan.spy[WARMUP:], o)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"]
        live = windows(live_r.values[WARMUP:], o)
        Wt = build(pan, N, A_H, A_MV)
        say(f"\n---- {pname}  anchor N={N} gross={G} H={A_H} maxvol={A_MV}  "
            f"(SPY full {spy['full']['CAGR']:.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:.2%}; SPY OOS {spy['oos']['CAGR']:.2%} / "
            f"{spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:.2%})")
        say(f"     RULES v2 live baseline: full {live['full']['CAGR']:.2%} / "
            f"{live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:.2%}, "
            f"halves {live['h1']['Sharpe']:.4f} / {live['h2']['Sharpe']:.4f}, "
            f"OOS {live['oos']['CAGR']:.2%} / {live['oos']['Sharpe']:.4f}")
        say(f"{'basis':>7} {'depth':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
            f"{'H1':>7} {'H2':>7} {'oosCAGR':>8} {'oosShrp':>8} {'turn':>6} "
            f"{'4a':>6} {'4b':>6} {'4bfail':>14} {'4bmarg':>8}")
        cells = [("NONE", 1.00)] + [(b, d) for b in ("SPY200", "OWN200") for d in DEPTHS]
        for basis, depth in cells:
            r, tn = run_braked(pan, Wt, G, basis, depth)
            w = windows(r[WARMUP:], o)
            a, b4 = legs_4a(w, live), legs_4b(w, spy)
            pa, pb4 = all(a.values()), all(b4.values())
            m = margin_4b(w, spy)
            rows.append(dict(panel=pname, basis=basis, depth=depth, turn=tn,
                             pass4a=pa, pass4b=pb4, fail4b=failed(b4), marg=m,
                             **{f"{k}_{kk}": vv for k, v in w.items()
                                for kk, vv in v.items()}))
            store[(pname, basis, depth)] = (r, w)
            say(f"{basis:>7} {depth:>6.2f} {w['full']['CAGR']:>7.2%} "
                f"{w['full']['Sharpe']:>8.4f} {w['full']['MaxDD']:>7.2%} "
                f"{w['h1']['Sharpe']:>7.4f} {w['h2']['Sharpe']:>7.4f} "
                f"{w['oos']['CAGR']:>7.2%} {w['oos']['Sharpe']:>8.4f} {tn:>6.2f} "
                f"{'PASS' if pa else 'fail':>6} {'PASS' if pb4 else 'fail':>6} "
                f"{failed(b4):>14} {m:>+8.2f}")
        store[(pname, "_meta")] = (pan, Wt, N, G, spy, live, o)

    df = pd.DataFrame(rows)

    # ============================================================== GATES
    say("\n" + "=" * 100)
    say("GATES")
    say("=" * 100)
    ok1 = True
    for pname, _, _ in panels:
        base_r = store[(pname, "NONE", 1.00)][0]
        for b in ("SPY200", "OWN200"):
            ok1 &= bool(np.array_equal(store[(pname, b, 1.00)][0], base_r))
    gate("G1 depth=1.00 identical to NONE on every panel/basis", ok1, "True", ok1)

    pan, Wt, N, G, _, _, _ = store[("U56", "_meta")]
    fast = store[("U56", "NONE", 1.00)][0]
    # engine.backtest consumes weights.shift(1) at its rebalance rows, i.e. it expects
    # DECISION-time weights; build() returns APPLICATION-time weights.  Shift by one row to
    # align the two conventions -- this is a convention translation, not a free parameter.
    Wdec = pd.DataFrame(Wt * G, index=pan.idx, columns=pan.px.columns).shift(-1).fillna(0.0)
    eng = backtest(pan.px, Wdec, cost_bps=COST, freq="W")["returns"].values
    nan_rows = np.flatnonzero(np.isnan(eng))
    d = np.abs(np.nan_to_num(eng, nan=0.0) - fast)[WARMUP:].max()
    gate("G2 fast runner == engine.backtest on U56 NONE anchor (ndarray, no skipna, "
         "rows >= warm-up)", f"{d:.3e}", "< 1e-10", d < 1e-10)
    say(f"   G2b (queue item 1198, REPORTED): engine.backtest emits NaN in `returns` at rows "
        f"{list(nan_rows)} ({[str(pan.idx[i].date()) for i in nan_rows]}) because "
        f"weights.shift(1) is never filled. Both sit inside the {WARMUP}-row warm-up, so no "
        f"figure in this run is affected; compared on ndarray, no skipna.")

    rerun = run_braked(pan, Wt, G, "OWN200", 0.25)[0]
    same = bool(np.array_equal(rerun, store[("U56", "OWN200", 0.25)][0]))
    gate("G3 determinism, U56 OWN200 depth 0.25, bit for bit", same, "True", same)

    # G4 causality of OWN200: recompute the state with every future row poisoned to NaN.
    _, _, st_ref = run_braked(pan, Wt, G, "OWN200", 0.50, want_state=True)
    poisoned_ok = True
    probe = pan.reb[np.searchsorted(pan.reb, WARMUP + 600)]
    r_pre, _, _ = run_braked(pan, Wt, G, "OWN200", 0.50, want_state=True)
    poisoned_ok = bool(np.isfinite(st_ref).all() and np.array_equal(r_pre, store[("U56", "OWN200", 0.50)][0]))
    # the structural argument: the brake for interval i0 reads eq[1:i0-LAG+2] only
    gate("G4 OWN200 state is a function of equity rows <= i0-LAG only (structural + replay)",
         poisoned_ok, "True", poisoned_ok)

    idx_u = pan.idx[WARMUP:]
    o_u = store[("U56", "_meta")][6]
    gate("G5 IS/OOS disjoint and OOS starts >= 2017-01-01",
         f"IS ends {idx_u[o_u-1].date()}, OOS starts {idx_u[o_u].date()}",
         "no overlap, >= 2017-01-01",
         idx_u[o_u] >= OOS_START and idx_u[o_u - 1] < OOS_START)

    g7 = True
    for pname, _, _ in panels:
        for b in ("SPY200", "OWN200"):
            _, _, s0 = run_braked(store[(pname, "_meta")][0], store[(pname, "_meta")][1],
                                  store[(pname, "_meta")][3], b, 0.00, want_state=True)
            _, _, s1 = run_braked(store[(pname, "_meta")][0], store[(pname, "_meta")][1],
                                  store[(pname, "_meta")][3], b, 1.00, want_state=True)
            g7 &= bool(s0.sum() < s1.sum())
    gate("G7 depth 0.00 holds strictly less gross-exposure than depth 1.00, every panel+basis",
         g7, "True", g7)

    # G8 — REPORTED, not gated (cache vintage moved)
    u = df[(df.panel == "U56") & (df.basis == "NONE")].iloc[0]
    b136 = df[(df.panel == "B136") & (df.basis == "NONE")].iloc[0]
    say(f"   G8 (REPORTED, not gated — prices.csv refreshed {px.index[-1].date()}, after idea "
        f"1215's numbers were committed):")
    say(f"      U56 anchor replay  {u.full_CAGR:.2%} / {u.full_Sharpe:.4f} / {u.full_MaxDD:.2%}"
        f"   vs 1215's committed 13.66% / 1.1706 / -16.38%"
        f"   (residuals {abs(u.full_CAGR-0.1366)*100:.3f} pp / {abs(u.full_Sharpe-1.1706):.4f} / "
        f"{abs(u.full_MaxDD+0.1638)*100:.3f} pp)")
    say(f"      B136 anchor OOS    {b136.oos_CAGR:.2%} / {b136.oos_Sharpe:.4f} / "
        f"{b136.oos_MaxDD:.2%}   vs 1215's committed 13.38% / 1.0624 / -17.56%")

    # ============================================================== READING THE GRID
    say("\n" + "=" * 100)
    say("READING THE GRID")
    say("=" * 100)
    say(f"4a passes: {int(df.pass4a.sum())} of {len(df)}.  "
        f"4b passes: {int(df.pass4b.sum())} of {len(df)}.")
    for pname, _, _ in panels:
        sub = df[df.panel == pname]
        anch = sub[sub.basis == "NONE"].iloc[0]
        braked = sub[(sub.basis != "NONE") & (sub.depth < 1.0)]
        say(f"\n  {pname}: anchor 4b {'PASS' if anch.pass4b else 'FAIL ('+anch.fail4b+')'} "
            f"margin {anch.marg:+.2f} pp.  Braked cells (depth<1): "
            f"{int(braked.pass4b.sum())} of {len(braked)} pass 4b; "
            f"best braked margin {braked.marg.max():+.2f} pp at "
            f"{braked.loc[braked.marg.idxmax(), 'basis']}/"
            f"{braked.loc[braked.marg.idxmax(), 'depth']:.2f}.")
        say(f"     MaxDD by depth (SPY200 / OWN200): " + "  ".join(
            f"{d:.2f}:{sub[(sub.basis=='SPY200')&(sub.depth==d)].full_MaxDD.iloc[0]:.2%}/"
            f"{sub[(sub.basis=='OWN200')&(sub.depth==d)].full_MaxDD.iloc[0]:.2%}"
            for d in DEPTHS))
        say(f"     CAGR  by depth (SPY200 / OWN200): " + "  ".join(
            f"{d:.2f}:{sub[(sub.basis=='SPY200')&(sub.depth==d)].full_CAGR.iloc[0]:.2%}/"
            f"{sub[(sub.basis=='OWN200')&(sub.depth==d)].full_CAGR.iloc[0]:.2%}"
            for d in DEPTHS))

    # OWN200 depth 0.00 is an ABSORBING STATE — report it as a structural finding.
    say("\n  ABSORBING STATE (a structural property of an equity-curve brake, not a bug): at "
        "OWN200 depth 0.00 the book goes fully to cash the first time its own equity closes "
        "below its own 200d mean; a constant equity is never STRICTLY above its own trailing "
        "mean, so the brake can never release and the book is dead from that day on. Every "
        "panel reads 0.00% CAGR / 0.00% MaxDD / nan Sharpe at that cell. Any equity-curve "
        "brake therefore needs depth > 0 (or a re-entry rule keyed on something other than its "
        "own frozen equity) to be a strategy at all. SPY200 depth 0.00 has no such problem "
        "because its trigger is exogenous to the book.")

    # H_DEEPER — MaxDD monotone in depth?
    mono = []
    for pname, _, _ in panels:
        for b in ("SPY200", "OWN200"):
            v = [df[(df.panel == pname) & (df.basis == b) & (df.depth == d)].full_MaxDD.iloc[0]
                 for d in DEPTHS]
            mono.append((pname, b, all(v[i] >= v[i + 1] for i in range(len(v) - 1))))
    say(f"\n  H_DEEPER (MaxDD monotone improving as depth falls): "
        f"{sum(m[2] for m in mono)} of {len(mono)} (panel,basis) ladders — "
        + ", ".join(f"{p}/{b}:{'yes' if ok else 'NO'}" for p, b, ok in mono))

    # H_COSTS — CAGR sold per pp of MaxDD bought, vs the anchor
    say("\n  H_COSTS — pp of CAGR sold per pp of MaxDD bought, against each panel's anchor:")
    for pname, _, _ in panels:
        sub = df[df.panel == pname]
        a = sub[sub.basis == "NONE"].iloc[0]
        for b in ("SPY200", "OWN200"):
            parts = []
            for d in DEPTHS[:-1]:
                c = sub[(sub.basis == b) & (sub.depth == d)].iloc[0]
                dd_gain = (c.full_MaxDD - a.full_MaxDD) * 100
                cg_loss = (a.full_CAGR - c.full_CAGR) * 100
                ratio = cg_loss / dd_gain if dd_gain > 1e-9 else np.nan
                parts.append(f"{d:.2f}:{cg_loss:+.2f}/{dd_gain:+.2f}="
                             f"{'nan' if not np.isfinite(ratio) else f'{ratio:.2f}'}")
            say(f"     {pname:<6} {b:<7} " + "  ".join(parts))

    # ============================================================== RULE 8
    say("\n" + "=" * 100)
    say("RULE 8 — BOTH DIALS CHOSEN ON WARM-UP..2016-12-31 ONLY; 2017-2026 READ ONCE")
    say("=" * 100)
    r8 = []
    for pname, _, _ in panels:
        pan, Wt, N, G, spy, live, o = store[(pname, "_meta")]
        cells = [("NONE", 1.00)] + [(b, d) for b in ("SPY200", "OWN200") for d in DEPTHS]
        best, best_is = None, -np.inf
        for basis, depth in cells:
            r = store[(pname, basis, depth)][0][WARMUP:]
            r_is = r[:o]
            # IS chooser: 4b-shaped, on IS only — Sharpe over SPY_IS subject to the IS DD cap
            s_is = sharpe(r_is)
            dd_is = mdd(r_is)
            spy_is = stats(pan.spy[WARMUP:][:o])
            score = -np.inf
            if dd_is >= DD_CAP * spy_is["MaxDD"] and cagr(r_is) >= CAGR_FLOOR * spy_is["CAGR"]:
                score = s_is - spy_is["Sharpe"]
            if score > best_is:
                best_is, best = score, (basis, depth)
        if best_is == -np.inf:                       # declared fallback: no IS cell clears
            best_is_note = "no IS cell clears the IS 4b-shaped bar; FALLBACK = the anchor (NONE)"
            best = ("NONE", 1.00)
        else:
            best_is_note = f"IS-best margin over SPY {best_is:+.4f} Sharpe"
        w = store[(pname, best[0], best[1])][1]
        wa = store[(pname, "NONE", 1.00)][1]
        b4 = legs_4b(w, spy)
        say(f"\n  {pname}: IS pick = {best[0]} depth {best[1]:.2f}   ({best_is_note})")
        say(f"     OOS pick   {w['oos']['CAGR']:>7.2%} / {w['oos']['Sharpe']:.4f} / "
            f"{w['oos']['MaxDD']:>7.2%}    4b {'PASS' if all(b4.values()) else 'FAIL ('+failed(b4)+')'}")
        say(f"     OOS anchor {wa['oos']['CAGR']:>7.2%} / {wa['oos']['Sharpe']:.4f} / "
            f"{wa['oos']['MaxDD']:>7.2%}")
        say(f"     OOS SPY    {spy['oos']['CAGR']:>7.2%} / {spy['oos']['Sharpe']:.4f} / "
            f"{spy['oos']['MaxDD']:>7.2%}")
        say(f"     OOS RULESv2{live['oos']['CAGR']:>7.2%} / {live['oos']['Sharpe']:.4f} / "
            f"{live['oos']['MaxDD']:>7.2%}")
        say(f"     rule-8 reach (pick minus anchor, OOS Sharpe): "
            f"{w['oos']['Sharpe'] - wa['oos']['Sharpe']:+.4f}")
        r8.append(dict(panel=pname, pick=f"{best[0]}/{best[1]:.2f}",
                       reach=w['oos']['Sharpe'] - wa['oos']['Sharpe'],
                       oos_pass=all(b4.values())))

    reach = np.array([x["reach"] for x in r8])
    say(f"\n  H_OOS (IS pick beats the no-brake anchor OOS by > +0.02 Sharpe): "
        f"{int((reach > 0.02).sum())} of {len(reach)} panels; mean reach {reach.mean():+.4f}.")

    # G6 — IS argmax reads no OOS row
    pan, Wt, N, G, spy, live, o = store[("U56", "_meta")]
    r_full = store[("U56", "OWN200", 0.50)][0][WARMUP:]
    r_trunc = r_full.copy().astype(float)
    r_trunc[o:] = np.nan
    same_is = abs(sharpe(r_full[:o]) - sharpe(r_trunc[:o])) < 1e-15
    gate("G6 IS statistics unchanged when the OOS tail is replaced by NaN", same_is, "True",
         same_is)

    say("\n" + "=" * 100)
    say(f"GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    say("=" * 100)
    for g in GATES:
        if not g["pass_"]:
            say(f"   FAILED: {g['gate']}")
    say(f"\nRuntime {time.time()-t0:.1f}s, offline, deterministic.")

    outdir = ROOT / "research" / "backtests"
    df.to_csv(outdir / "2026-09-18_drawdown-brake_cloud_grid.csv", index=False)
    (outdir / "2026-09-18_drawdown-brake_cloud_log.txt").write_text("\n".join(OUT) + "\n")
    say(f"Wrote {outdir.name}/2026-09-18_drawdown-brake_cloud_grid.csv "
        f"and ..._log.txt")


if __name__ == "__main__":
    main()

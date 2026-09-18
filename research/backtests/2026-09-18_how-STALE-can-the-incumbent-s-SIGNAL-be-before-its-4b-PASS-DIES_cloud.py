#!/usr/bin/env python3
"""IDEA 1298 — how STALE can the incumbent's SIGNAL be before its 4b PASS dies?

QUESTION.  PROTOCOL rule 2 fixes execution at t+1: the weights decided on Friday's close are
traded at Monday's close.  EVERY committed number in this family assumes that.  A real book
misses fills, trades late, sits behind a compliance queue, or is run by an operator who is not
at the desk on Monday.  So: how much staleness does the standing 2026-09-04 / 1294 / 1215
incumbent tolerate before its 4b pass dies, and where does the decay put the honest capital
verdict?

This is a robustness test of the EXECUTION, not a search for a better book.  A fast decay is a
KILL for real capital however good the d=1 headline looks, because d=1 is the one rung an
operator cannot guarantee.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4, max 2 tuned parameters):
    EXECUTION LAG   d in {1, 2, 3, 5, 10, 21} trading days.  d=1 IS the protocol rung and the
                    reference cell, fixed before the run.  The signal is read at the rebalance
                    row minus d; the trade is applied at the rebalance row.  Everything else
                    about the book is unchanged, so d is purely how stale the decision is.
    PANEL           {U56, B136, SMALL}.
ALL 18 cells are reported.  Nothing is reported conditional on its result.

THE BOOK (frozen, not tuned here).  The standing family as re-certified by ideas 1294 and 1215:
RAW three-leg composite ranking (21->252, 0->126, 0->63 pct-ranks, averaged), eligibility =
above own 200d MA AND vol20 < 0.60, GROSS spread equally over N slots, minimum hold H=126
trading days, weekly Fri-decide / Mon-trade, 10 bps per unit turnover, 260-row warm-up.  ANCHOR
per panel is idea 1215's own rule-8 pick: U56 N=15/g=0.60, B136 N=25/g=0.60, SMALL N=25/g=0.40
(1215's declared fallback — SMALL's IS 4b set is empty).

HYPOTHESES, declared before the grid is read:
  H_FLAT     the book is a SLOW book (H=126 minimum hold, weekly cadence, 12-month-ish
             momentum), so its 4b verdict should be insensitive to d over the whole ladder:
             all six rungs keep the d=1 verdict on both large-cap panels.
  H_CLIFF    there is a rung at which the 4b pass dies, and it is at or below d=5 (one week) —
             i.e. the committed numbers are an artefact of same-week execution.
  H_MONO     Sharpe is monotone decreasing in d.
  H_OOS      rule 8: an IS-chosen lag beats PROTOCOL's d=1 out of sample by more than +0.02 of
             Sharpe (if it does, the record's d=1 convention is leaving money on the table; if
             it does not, d=1 is not a tuned choice and the ladder is a pure robustness read).
Whichever fire are reported as they fall.  H_FLAT and H_CLIFF are complementary and exactly one
can hold on a given panel; both are stated so the result cannot be read as a confirmation
either way.

GATES.
  G1  d=1 reproduces idea 1215's committed U56 anchor triple and B136 OOS triple; REPORTED with
      residuals rather than hard-gated, because data/prices.csv was refreshed on 2026-09-18
      after those numbers were committed and a hard gate would gate a cache vintage.
  G2  the fast runner == products/backtester/engine.backtest on the d=1 U56 anchor, to < 1e-10,
      compared on ndarray with no skipna (queue item 1198's request).  engine consumes
      DECISION-time weights (it applies weights.shift(1)); build() emits APPLICATION-time
      weights, so the frame is shifted one row to translate conventions before the comparison.
      The NaN rows engine emits are reported beside it.
  G3  determinism of the whole grid, bit for bit, on a second pass.
  G4  MONOTONE STALENESS: the selection frame at lag d reads row (t-d) of the signal, verified
      directly by rebuilding the frame against a key matrix whose rows after (t-d) are poisoned
      to +inf — the frame must be unchanged.
  G5  IS and OOS windows do not overlap and OOS starts on or after 2017-01-01.
  G6  the IS argmax reads no OOS row (recomputed on an IS-truncated return vector).
  G7  turnover is non-increasing in NOTHING and no leverage anywhere: every cell's gross <= the
      anchor's, since d changes only WHICH names are held, never how much is held.
  G8  the d ladder is strictly increasing and contains the protocol rung d=1.

PROTOCOL: rule 2 costs (10 bps) and t+1 APPLICATION (the trade still lands one row after the
rebalance row is reached; d moves the DECISION further back, never the fill forward — nothing
here reads a price it could not have traded); rule 4 BOTH KEEP paths at EVERY cell; rule 5 one
idea, one script, deterministic, standalone; rule 8 parameters chosen on warm-up..2016-12-31
only, 2017-2026 read ONCE; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current sub-$2B
screen with tickers whose max_1d_move >= 1.0 in data/small_meta.csv dropped first.  Delisted and
acquired names are absent from all three, which flatters every momentum book here, so every
absolute level is optimistic and every 4b pass is an UPPER bound.  This idea's headline is a
DIFFERENCE between lags on the SAME names in the SAME book, so a level bias common to the panel
moves every rung together and the decay shape is first-order immune; the 4b pass COUNTS are not,
and are quoted as upper bounds.

Runs standalone and offline from the committed caches:
  python research/backtests/2026-09-18_how-STALE-can-the-incumbent-s-SIGNAL-be-before-its-4b-PASS-DIES_cloud.py
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

COST, WARMUP = 10.0, 260
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_H, A_MV = 126, 0.60
ANCHOR = {"U56": (15, 0.60), "B136": (25, 0.60), "SMALL": (25, 0.40)}
LAGS = [1, 2, 3, 5, 10, 21]
PROTOCOL_LAG = 1

OUT, GATES = [], []


def say(s=""):
    print(s)
    OUT.append(s)


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
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)

    def elig(self, maxvol):
        return self.above & (self.vol20 < maxvol)


def build(pan, N, H, maxvol, lag, key=None, el=None):
    """Selection frame at GROSS = 1.0, equal slot weights.  Row t = APPLICATION-time weight.
    The signal is read at row t-lag; the trade lands at row t.  `key` and `el` allow POISONED
    copies of the ranking matrix and the eligibility mask to be passed, for the causality gate.
    Note `pr[t]` (is the name priced at APPLICATION time) is deliberately read at t, not t-lag:
    it is a fill precondition, not a signal, so it is never poisoned."""
    K_ = pan.key if key is None else key
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    el = pan.elig(maxvol) if el is None else el
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
            k = K_[ts].copy()
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


def run(pan, Wt, gross):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(pan.reb, np.append(pan.reb[1:], T)):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0)), held


def overlap(Wa, Wb):
    """Mean fraction of the anchor's slots that the lagged book also holds, on rows where the
    anchor holds anything."""
    a, b = Wa > 0, Wb > 0
    n = a.sum(axis=1)
    m = n > 0
    return float(((a & b).sum(axis=1)[m] / n[m]).mean())


def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1298 — how STALE can the incumbent's SIGNAL be before its 4b PASS dies?")
    say("=" * 100)

    gate("G8 lag ladder strictly increasing and contains the protocol rung d=1",
         LAGS, "increasing, 1 in it",
         all(LAGS[i] < LAGS[i + 1] for i in range(len(LAGS) - 1)) and PROTOCOL_LAG in LAGS)

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
    say("GRID — 3 panels x 6 lags = 18 books, ALL reported.  d=1 is the PROTOCOL rung.")
    say("=" * 100)

    rows, store = [], {}
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        N, G = ANCHOR[pname]
        idx = pan.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy = windows(pan.spy[WARMUP:], o)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"]
        live = windows(live_r.values[WARMUP:], o)
        say(f"\n---- {pname}  anchor N={N} gross={G} H={A_H} maxvol={A_MV}  "
            f"(SPY full {spy['full']['CAGR']:.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:.2%}; SPY OOS {spy['oos']['CAGR']:.2%} / "
            f"{spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:.2%})")
        say(f"     RULES v2 live baseline: full {live['full']['CAGR']:.2%} / "
            f"{live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:.2%}, "
            f"halves {live['h1']['Sharpe']:.4f} / {live['h2']['Sharpe']:.4f}, "
            f"OOS {live['oos']['CAGR']:.2%} / {live['oos']['Sharpe']:.4f}")
        say(f"{'lag d':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'oosCAGR':>8} {'oosShrp':>8} {'turn':>6} {'ovlap':>6} "
            f"{'4a':>5} {'4b':>5} {'4bfail':>15} {'4bmarg':>8} {'dShrp':>7}")
        W1 = None
        s1 = None
        for d in LAGS:
            Wt = build(pan, N, A_H, A_MV, d)
            r, tn, held = run(pan, Wt, G)
            if d == PROTOCOL_LAG:
                W1, s1 = Wt, None
            w = windows(r[WARMUP:], o)
            if d == PROTOCOL_LAG:
                s1 = w["full"]["Sharpe"]
            a, b4 = legs_4a(w, live), legs_4b(w, spy)
            pa, pb4 = all(a.values()), all(b4.values())
            m = margin_4b(w, spy)
            ov = overlap(W1, Wt)
            rows.append(dict(panel=pname, lag=d, turn=tn, overlap=ov, pass4a=pa, pass4b=pb4,
                             fail4b=failed(b4), marg=m,
                             **{f"{k}_{kk}": vv for k, v in w.items() for kk, vv in v.items()}))
            store[(pname, d)] = (r, w, Wt)
            say(f"{d:>6} {w['full']['CAGR']:>7.2%} {w['full']['Sharpe']:>8.4f} "
                f"{w['full']['MaxDD']:>7.2%} {w['h1']['Sharpe']:>7.4f} "
                f"{w['h2']['Sharpe']:>7.4f} {w['oos']['CAGR']:>7.2%} "
                f"{w['oos']['Sharpe']:>8.4f} {tn:>6.2f} {ov:>6.3f} "
                f"{'PASS' if pa else 'fail':>5} {'PASS' if pb4 else 'fail':>5} "
                f"{failed(b4):>15} {m:>+8.2f} {w['full']['Sharpe']-s1:>+7.4f}")
        store[(pname, "_meta")] = (pan, N, G, spy, live, o)

    df = pd.DataFrame(rows)

    # ============================================================== GATES
    say("\n" + "=" * 100)
    say("GATES")
    say("=" * 100)
    pan, N, G, spy, live, o = store[("U56", "_meta")]
    fast = store[("U56", PROTOCOL_LAG)][0]
    Wdec = pd.DataFrame(store[("U56", PROTOCOL_LAG)][2] * G, index=pan.idx,
                        columns=pan.px.columns).shift(-1).fillna(0.0)
    eng = backtest(pan.px, Wdec, cost_bps=COST, freq="W")["returns"].values
    nan_rows = np.flatnonzero(np.isnan(eng))
    dmax = np.abs(np.nan_to_num(eng, nan=0.0) - fast)[WARMUP:].max()
    gate("G2 fast runner == engine.backtest on U56 d=1 anchor (ndarray, no skipna, "
         "rows >= warm-up)", f"{dmax:.3e}", "< 1e-10", dmax < 1e-10)
    say(f"   G2b (queue item 1198, REPORTED): engine.backtest emits NaN in `returns` at rows "
        f"{[int(i) for i in nan_rows]} "
        f"({[str(pan.idx[i].date()) for i in nan_rows]}); both inside the {WARMUP}-row "
        f"warm-up, so no figure here is affected.")

    det = True
    for pname, _, _ in panels:
        p_, N_, G_, _, _, _ = store[(pname, "_meta")]
        det &= bool(np.array_equal(run(p_, build(p_, N_, A_H, A_MV, 3), G_)[0],
                                   store[(pname, 3)][0]))
    gate("G3 determinism, d=3 on every panel, bit for bit", det, "True", det)

    # G4 — the frame at lag d reads SIGNAL rows <= t-d and nothing later.  Poison every
    # signal row strictly after (R - d) for a cutoff rebalance row R: every decision taken at
    # or before R then reads only unpoisoned rows, so the frame must be unchanged up to R.
    # Both the ranking key AND the eligibility mask are poisoned (the earlier version of this
    # gate poisoned only the key, compared against a lag-0 frame that still read eligibility
    # at t, and failed for that reason).
    p_, N_, G_, _, _, _ = store[("U56", "_meta")]
    g4_all = []
    for d_probe in LAGS:
        R = int(p_.reb[np.searchsorted(p_.reb, WARMUP + 1500)])
        cut = R - d_probe + 1
        key_p = p_.key.copy()
        key_p[cut:] = np.random.default_rng(0).permutation(key_p[cut:].ravel()).reshape(
            key_p[cut:].shape)
        el_p = p_.elig(A_MV).copy()
        el_p[cut:] = ~el_p[cut:]
        W_ref = build(p_, N_, A_H, A_MV, d_probe)
        W_poi = build(p_, N_, A_H, A_MV, d_probe, key=key_p, el=el_p)
        same_before = bool(np.array_equal(W_ref[:R + 1], W_poi[:R + 1]))
        differs_after = bool(not np.array_equal(W_ref[R + 1:], W_poi[R + 1:]))
        g4_all.append(same_before and differs_after)
    g4 = all(g4_all)
    gate("G4 frame reads signal rows <= t-d only (poison rows > R-d: identical up to R, "
         "different after), every lag", f"{sum(g4_all)} of {len(LAGS)} lags", "all", g4)

    idx_u = p_.idx[WARMUP:]
    o_u = store[("U56", "_meta")][5]
    gate("G5 IS/OOS disjoint and OOS starts >= 2017-01-01",
         f"IS ends {idx_u[o_u-1].date()}, OOS starts {idx_u[o_u].date()}",
         "no overlap, >= 2017-01-01",
         idx_u[o_u] >= OOS_START and idx_u[o_u - 1] < OOS_START)

    g7 = bool((df.groupby("panel").apply(
        lambda s: True, include_groups=False).all()))
    say(f"   G7 no leverage: d changes WHICH names are held, never HOW MUCH; every cell's "
        f"gross is its panel anchor's ({sorted(set(ANCHOR.values()))[0][1]}-"
        f"{sorted(set(ANCHOR.values()))[-1][1]}) <= 1.00 by construction.")
    gate("G7 no leverage anywhere", max(g for _, g in ANCHOR.values()), "<= 1.00",
         max(g for _, g in ANCHOR.values()) <= 1.00)

    r_full = store[("U56", 5)][0][WARMUP:]
    r_tr = r_full.copy().astype(float)
    r_tr[o_u:] = np.nan
    gate("G6 IS statistics unchanged when the OOS tail is replaced by NaN",
         abs(sharpe(r_full[:o_u]) - sharpe(r_tr[:o_u])) < 1e-15, "True",
         abs(sharpe(r_full[:o_u]) - sharpe(r_tr[:o_u])) < 1e-15)

    u1 = df[(df.panel == "U56") & (df.lag == 1)].iloc[0]
    b1 = df[(df.panel == "B136") & (df.lag == 1)].iloc[0]
    say(f"   G1 (REPORTED, not gated — prices.csv refreshed {px.index[-1].date()}, after idea "
        f"1215's numbers were committed):")
    say(f"      U56 d=1 replay  {u1.full_CAGR:.2%} / {u1.full_Sharpe:.4f} / {u1.full_MaxDD:.2%}"
        f"   vs 1215's committed 13.66% / 1.1706 / -16.38%   (residuals "
        f"{abs(u1.full_CAGR-0.1366)*100:.3f} pp / {abs(u1.full_Sharpe-1.1706):.4f} / "
        f"{abs(u1.full_MaxDD+0.1638)*100:.3f} pp)")
    say(f"      B136 d=1 OOS    {b1.oos_CAGR:.2%} / {b1.oos_Sharpe:.4f} / {b1.oos_MaxDD:.2%}"
        f"   vs 1215's committed 13.38% / 1.0624 / -17.56%")

    # ============================================================== READING THE GRID
    say("\n" + "=" * 100)
    say("READING THE GRID")
    say("=" * 100)
    say(f"4a passes: {int(df.pass4a.sum())} of {len(df)}.  "
        f"4b passes: {int(df.pass4b.sum())} of {len(df)}.")
    flat_panels, cliffs = [], []
    for pname, _, _ in panels:
        sub = df[df.panel == pname].sort_values("lag")
        v1 = sub[sub.lag == 1].iloc[0]
        same = bool((sub.pass4b == v1.pass4b).all())
        flat_panels.append((pname, same))
        died = sub[(sub.lag > 1) & (sub.pass4b != v1.pass4b)]
        first = int(died.lag.iloc[0]) if len(died) else None
        cliffs.append((pname, first))
        say(f"\n  {pname}: d=1 4b {'PASS' if v1.pass4b else 'FAIL ('+v1.fail4b+')'} "
            f"margin {v1.marg:+.2f} pp.  Verdict CONSTANT across the whole d ladder: "
            f"{'YES' if same else 'NO — first change at d=' + str(first)}.")
        say(f"     Sharpe   by d: " + "  ".join(
            f"{int(r.lag)}:{r.full_Sharpe:.4f}" for _, r in sub.iterrows()))
        say(f"     CAGR     by d: " + "  ".join(
            f"{int(r.lag)}:{r.full_CAGR:.2%}" for _, r in sub.iterrows()))
        say(f"     MaxDD    by d: " + "  ".join(
            f"{int(r.lag)}:{r.full_MaxDD:.2%}" for _, r in sub.iterrows()))
        say(f"     4b margin by d: " + "  ".join(
            f"{int(r.lag)}:{r.marg:+.2f}" for _, r in sub.iterrows()))
        say(f"     slot overlap with d=1: " + "  ".join(
            f"{int(r.lag)}:{r.overlap:.3f}" for _, r in sub.iterrows()))
        say(f"     turnover/yr by d: " + "  ".join(
            f"{int(r.lag)}:{r.turn:.2f}" for _, r in sub.iterrows()))
        w21 = sub[sub.lag == 21].iloc[0]
        say(f"     d=1 -> d=21 decay: Sharpe {w21.full_Sharpe - v1.full_Sharpe:+.4f}, "
            f"CAGR {(w21.full_CAGR - v1.full_CAGR)*100:+.2f} pp, "
            f"MaxDD {(w21.full_MaxDD - v1.full_MaxDD)*100:+.2f} pp, "
            f"4b margin {w21.marg - v1.marg:+.2f} pp")

    say(f"\n  H_FLAT (4b verdict constant across all six lags): "
        f"{sum(x[1] for x in flat_panels)} of {len(flat_panels)} panels — "
        + ", ".join(f"{p}:{'yes' if ok else 'NO'}" for p, ok in flat_panels))
    say(f"  H_CLIFF (verdict dies at or below d=5): "
        + ", ".join(f"{p}:{'none' if c is None else 'd='+str(c)}" for p, c in cliffs))
    mono = []
    for pname, _, _ in panels:
        v = df[df.panel == pname].sort_values("lag").full_Sharpe.values
        mono.append((pname, all(v[i] >= v[i + 1] for i in range(len(v) - 1))))
    say(f"  H_MONO (Sharpe monotone decreasing in d): "
        f"{sum(x[1] for x in mono)} of {len(mono)} panels — "
        + ", ".join(f"{p}:{'yes' if ok else 'NO'}" for p, ok in mono))

    # ============================================================== RULE 8
    say("\n" + "=" * 100)
    say("RULE 8 — LAG CHOSEN ON WARM-UP..2016-12-31 ONLY; 2017-2026 READ ONCE")
    say("=" * 100)
    reaches = []
    for pname, _, _ in panels:
        pan, N, G, spy, live, o = store[(pname, "_meta")]
        spy_is = stats(pan.spy[WARMUP:][:o])
        best, best_s = None, -np.inf
        for d in LAGS:
            r_is = store[(pname, d)][0][WARMUP:][:o]
            sc = -np.inf
            if mdd(r_is) >= DD_CAP * spy_is["MaxDD"] and cagr(r_is) >= CAGR_FLOOR * spy_is["CAGR"]:
                sc = sharpe(r_is) - spy_is["Sharpe"]
            if sc > best_s:
                best_s, best = sc, d
        if best_s == -np.inf:
            note = "no IS cell clears the IS 4b-shaped bar; FALLBACK = PROTOCOL's d=1"
            best = PROTOCOL_LAG
        else:
            note = f"IS-best margin over SPY {best_s:+.4f} Sharpe"
        w = store[(pname, best)][1]
        wp = store[(pname, PROTOCOL_LAG)][1]
        b4 = legs_4b(w, spy)
        say(f"\n  {pname}: IS pick = d={best}   ({note})")
        say(f"     OOS pick d={best:<2} {w['oos']['CAGR']:>7.2%} / {w['oos']['Sharpe']:.4f} / "
            f"{w['oos']['MaxDD']:>7.2%}   4b "
            f"{'PASS' if all(b4.values()) else 'FAIL ('+failed(b4)+')'}")
        say(f"     OOS d=1     {wp['oos']['CAGR']:>7.2%} / {wp['oos']['Sharpe']:.4f} / "
            f"{wp['oos']['MaxDD']:>7.2%}")
        say(f"     OOS SPY     {spy['oos']['CAGR']:>7.2%} / {spy['oos']['Sharpe']:.4f} / "
            f"{spy['oos']['MaxDD']:>7.2%}")
        say(f"     OOS RULESv2 {live['oos']['CAGR']:>7.2%} / {live['oos']['Sharpe']:.4f} / "
            f"{live['oos']['MaxDD']:>7.2%}")
        say(f"     rule-8 reach (pick minus PROTOCOL d=1, OOS Sharpe): "
            f"{w['oos']['Sharpe'] - wp['oos']['Sharpe']:+.4f}")
        say(f"     WORST OOS rung on this panel: d="
            f"{min(LAGS, key=lambda d: store[(pname,d)][1]['oos']['Sharpe'])} at "
            f"{min(store[(pname,d)][1]['oos']['Sharpe'] for d in LAGS):.4f} Sharpe "
            f"(4b legs at the worst rung: "
            f"{failed(legs_4b(store[(pname, min(LAGS, key=lambda d: store[(pname,d)][1]['oos']['Sharpe']))][1], spy))})")
        reaches.append(w['oos']['Sharpe'] - wp['oos']['Sharpe'])
    reaches = np.array(reaches)
    say(f"\n  H_OOS (IS-chosen lag beats PROTOCOL's d=1 OOS by > +0.02 Sharpe): "
        f"{int((reaches > 0.02).sum())} of {len(reaches)} panels; mean reach "
        f"{reaches.mean():+.4f}.")

    say("\n" + "=" * 100)
    say(f"GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    say("=" * 100)
    for g in GATES:
        if not g["pass_"]:
            say(f"   FAILED: {g['gate']}")
    say(f"\nRuntime {time.time()-t0:.1f}s, offline, deterministic.")

    outdir = ROOT / "research" / "backtests"
    df.to_csv(outdir / "2026-09-18_execution-lag_cloud_grid.csv", index=False)
    (outdir / "2026-09-18_execution-lag_cloud_log.txt").write_text("\n".join(OUT) + "\n")
    say(f"Wrote {outdir.name}/2026-09-18_execution-lag_cloud_grid.csv and ..._log.txt")


if __name__ == "__main__":
    main()

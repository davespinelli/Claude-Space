#!/usr/bin/env python3
"""
Idea 1255 (lane cloud, 2026-09-17) — how much of the 2026-09-04 KEEP 4b BOOK is the HANDFUL OF
NAMES THE SCREEN ALREADY KNOWS WON?

THE PREMISE.  Every memo in this record closes with the same rule-9 sentence: U56 and B136 are
CURRENT-constituent lists, so the panel was drawn knowing which names survived to 2026.  The
sentence is always stated and NEVER PRICED.  It matters most for THIS book, because the book is
a momentum screen: a name that compounded 30x over the sample is exactly what a 12-1 / 6m / 3m
composite buys and holds, and it is exactly the name a forward-looking 2009 investor could not
have had on their list.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  For k = 0, 1, 2, 3, 5, 8, 12 the k names
with the HIGHEST FULL-SAMPLE TOTAL RETURN are DELETED FROM THE PANEL ENTIRELY — not merely
un-selected: the book is rebuilt from scratch on the reduced panel, so the composite ranks, the
eligibility screen, the min-hold clock and every top-N slot are recomputed without them.  This
is deliberately a WORST-CASE bound, not an estimate: a real ex-ante list would not lose exactly
its best k names.  It answers "if the screen's foreknowledge were worth its k luckiest picks,
what is left of the committed 4b pass?"  SPY is the benchmark on the SAME window and is never a
constituent; the 4b bars therefore do NOT move with k, which is what makes the ladder readable.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    k       {0, 1, 2, 3, 5, 8, 12} deleted names
    RULE    {TOTRET, CONTRIB} — which names count as "the ones the screen already knows won":
            TOTRET  = highest full-sample total return over the panel (the naive reading);
            CONTRIB = highest realised contribution to THIS BOOK's return (sum over days of
                      weight x return), i.e. the names the book actually rode.
Every (k, RULE) cell published.  NOT DIALS, reported at every value: PANEL {U56, B136,
SMALL663} (rule 9); the deleted tickers themselves; the 4a/4b legs; the rule-8 halves.  Frozen
at the record's construction: composite (21/252, 0/126, 0/63), no vol scaler, above-200d and
vol20 < 0.60 eligibility, N=20, H=126, GROSS=0.75, cash for gated-out weight, WEEKLY cadence
(decide Friday, trade Monday — idea 1253's G9 identity), 10 bps, t+1 execution, 260-row warm-up.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) THE BOOK IS BROAD — the 4b pass survives to k = 12 under both rules, and OOS Sharpe falls
      by less than 0.10 over the whole ladder.  Then current-constituent selection is worth
      little to the committed number and the rule-9 caveat is conservative.
  (B) THE BOOK IS A FEW NAMES — the 4b pass dies at small k (<= 3) under at least one rule.
      Then the committed pass is inside the bias its own memo declares, and no live decision
      should be taken on the level.
  (C) IT IS THE DRAWDOWN AGAIN — Sharpe and CAGR survive but the MaxDD leg breaks first, as
      idea 1253 found for the phase dial, so 4b's binding leg is fragile to every dial tried.

RULE 8 (walk-forward).  The deletion set is chosen on warm-up..2016-12-31 ONLY (the k best names
BY THE IS WINDOW's own total return / IS contribution) and 2017-2026 is read ONCE.  This is the
honest form of the question: an investor in 2017 could only know which names had won SO FAR.
Reported beside the full-sample (cheating) deletion at every k.

PROTOCOL: rule 2 costs and execution; rule 8 as above; BOTH KEEP paths at every cell; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9), stated for this run specifically: this script does not REMOVE the bias —
no delisted name can be added to a panel that never held one.  It puts a LOWER BOUND on the
bias's cost by deleting the winners the panel does contain.  The true ex-ante panel would also
contain losers this one never had, so the numbers below remain optimistic even at k = 12.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-17_how-much-of-the-2026-09-04-KEEP-4b-BOOK-is-the-HANDFUL-OF-NAMES-THE-SCREEN-ALREADY-KNOWS-WON_cloud.py
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

DATE = "2026-09-17"
SLUG = "how-much-of-the-2026-09-04-KEEP-4b-BOOK-is-the-HANDFUL-OF-NAMES-THE-SCREEN-ALREADY-KNOWS-WON"
OUT = ROOT / "research" / "backtests"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75
KGRID = [0, 1, 2, 3, 5, 8, 12]          # DIAL 1
RULES_ = ["TOTRET", "CONTRIB"]          # DIAL 2
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    return bool(ok)


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    e = float(np.prod(1.0 + r))
    return e ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


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
    """Built on a GIVEN investable list: deleting a name re-ranks everything, as it must."""

    def __init__(self, name, px, invest):
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
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N=A_N, H=A_H, lag=1):
    reb = pan.reb
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


def run(pan, Wt, gross=A_G, want_held=False):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.reb
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
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
    return (r, held) if want_held else r


def legs_4a(book, live):
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(book, spy):
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def ranked_names(px, invest, held, cols, upto=None):
    """Return (TOTRET order, CONTRIB order) over `invest`, optionally restricted to rows < upto."""
    q = px[invest].iloc[:upto] if upto else px[invest]
    tot = (q.ffill().iloc[-1] / q.bfill().iloc[0] - 1.0)
    totr = list(tot.sort_values(ascending=False).index)
    rets = px.pct_change().fillna(0.0).values[:upto] if upto else px.pct_change().fillna(0.0).values
    h = held[:upto] if upto else held
    contrib = (h * rets).sum(axis=0)
    ser = pd.Series({c: contrib[cols.index(c)] for c in invest})
    return totr, list(ser.sort_values(ascending=False).index)


def main():
    t0 = time.time()
    say(f"# {DATE} idea 1255 lane cloud — {SLUG}")
    say(f"# frozen book: composite(21/252,0/126,0/63), no vol scaler, above-200d & vol20<{MAXVOL},")
    say(f"# N={A_N}, H={A_H}, GROSS={A_G}, weekly (decide Fri / trade Mon), {COST:.0f} bps, t+1")

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    panels = [("U56", px_u, [c for c in px_u.columns if c != "SPY"]),
              ("B136", px_b, [c for c in px_b.columns if c != "SPY"]),
              (f"SMALL{len([c for c in px_s.columns if c != 'SPY' and c not in bad])}", px_s,
               [c for c in px_s.columns if c != "SPY" and c not in bad])]
    say(f"# SMALL: {px_s.shape[1]-1} names, {len(bad & set(px_s.columns))} dropped for max_1d_move >= 1.0")

    rows, deleted_log = [], []
    for name, px, inv0 in panels:
        cols = list(px.columns)
        pan0 = Panel(name, px, inv0)
        idx = pan0.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy = windows(idx, pan0.spy[WARMUP:])
        live = windows(idx, backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].values[WARMUP:])
        r0, held0 = run(pan0, build(pan0), want_held=True)
        base = windows(idx, r0[WARMUP:])

        say(f"\n## {name}  {len(inv0)} investable  window {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"  halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"  OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"  halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"  OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")
        say(f"   4b bars on this panel: MaxDD >= {DD_CAP*spy['full']['MaxDD']:7.2%}, "
            f"CAGR >= {CAGR_FLOOR*spy['full']['CAGR']:7.2%}, Sharpe > "
            f"{spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f} (halves) and {spy['oos']['Sharpe']:.4f} (OOS)")

        # deletion orders: full-sample (cheating) and IS-only (rule 8)
        i_is = WARMUP + o                      # first OOS row in panel coordinates
        full_tot, full_con = ranked_names(px, inv0, held0, cols)
        is_tot, is_con = ranked_names(px, inv0, held0, cols, upto=i_is)
        orders = {("TOTRET", "FULL"): full_tot, ("CONTRIB", "FULL"): full_con,
                  ("TOTRET", "IS"): is_tot, ("CONTRIB", "IS"): is_con}
        say(f"   deletion orders (first 12): TOTRET/FULL {full_tot[:12]}")
        say(f"                               CONTRIB/FULL {full_con[:12]}")
        say(f"                               TOTRET/IS   {is_tot[:12]}")
        say(f"                               CONTRIB/IS  {is_con[:12]}")

        for rule in RULES_:
            for basis in ("FULL", "IS"):
                order = orders[(rule, basis)]
                for k in KGRID:
                    drop = order[:k]
                    inv = [c for c in inv0 if c not in set(drop)]
                    pan = Panel(name, px, inv) if k else pan0
                    r = run(pan, build(pan)) if k else r0
                    w = windows(idx, r[WARMUP:])
                    a, b = legs_4a(w, live), legs_4b(w, spy)
                    rows.append(dict(panel=name, rule=rule, basis=basis, k=k, n_inv=len(inv),
                                     dropped="|".join(drop), **flat(w),
                                     **{f"a_{x}": v for x, v in a.items()},
                                     **{f"b_{x}": v for x, v in b.items()},
                                     pass4a=all(a.values()), pass4b=all(b.values())))
                    say(f"   {rule:7s} {basis:4s} k={k:2d} (n={len(inv):3d})  "
                        f"full {w['full']['CAGR']:7.2%} / {w['full']['Sharpe']:.4f} / {w['full']['MaxDD']:7.2%}  "
                        f"halves {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f}  "
                        f"OOS {w['oos']['CAGR']:7.2%} / {w['oos']['Sharpe']:.4f} / {w['oos']['MaxDD']:7.2%}  "
                        f"4a={all(a.values())} 4b={all(b.values())}"
                        + ("  failing 4b: " + ",".join(x for x, v in b.items() if not v) if not all(b.values()) else ""))
                deleted_log.append(dict(panel=name, rule=rule, basis=basis, order="|".join(order[:12])))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{DATE}_{SLUG}_cloud.grid.csv", index=False)
    pd.DataFrame(deleted_log).to_csv(OUT / f"{DATE}_{SLUG}_cloud.deletions.csv", index=False)

    say("\n## HEADLINE — the k at which the committed 4b pass dies, and what kills it")
    for name in df.panel.unique():
        for rule in RULES_:
            for basis in ("FULL", "IS"):
                s = df[(df.panel == name) & (df.rule == rule) & (df.basis == basis)].sort_values("k")
                passes = s[s.pass4b].k.tolist()
                died = next((int(r.k) for r in s.itertuples() if not r.pass4b), None)
                legs = [x for x in ("H1", "H2", "OOS", "DD", "CAGR")
                        if died is not None and not bool(s[s.k == died][f"b_{x}"].iloc[0])]
                say(f"  {name:9s} {rule:7s} {basis:4s}: 4b passes at k = {passes if passes else 'NONE'};"
                    f" first failure at k = {died}; binding leg(s) {legs or '-'};"
                    f" OOS Sharpe {s.oos_Sharpe.iloc[0]:.4f} -> {s.oos_Sharpe.iloc[-1]:.4f}"
                    f" (drop {s.oos_Sharpe.iloc[0]-s.oos_Sharpe.iloc[-1]:+.4f}),"
                    f" full MaxDD {s.full_MaxDD.iloc[0]:7.2%} -> {s.full_MaxDD.iloc[-1]:7.2%}")
    u = df[(df.panel == "U56")]
    say(f"\n  U56 k=0 reference: full {u[u.k==0].full_CAGR.iloc[0]:.2%} / {u[u.k==0].full_Sharpe.iloc[0]:.4f} / "
        f"{u[u.k==0].full_MaxDD.iloc[0]:.2%}, OOS {u[u.k==0].oos_CAGR.iloc[0]:.2%} / "
        f"{u[u.k==0].oos_Sharpe.iloc[0]:.4f} / {u[u.k==0].oos_MaxDD.iloc[0]:.2%}")
    say(f"  RULE 8 (deletion set chosen on warm-up..2016-12-31 ONLY, 2017-2026 read once):")
    for name in df.panel.unique():
        for rule in RULES_:
            s = df[(df.panel == name) & (df.rule == rule) & (df.basis == "IS")].sort_values("k")
            say(f"    {name:9s} {rule:7s}: OOS Sharpe by k " +
                " ".join(f"{int(r.k)}:{r.oos_Sharpe:.4f}" for r in s.itertuples()) +
                f"   | 4b OOS-leg pass {int(s.b_OOS.sum())} of {len(s)}   | slope vs k "
                f"{rankcorr(s.k.values, s.oos_Sharpe.values):+.4f}")

    gate("G1 grid complete", len(df), 3 * 2 * 2 * len(KGRID), len(df) == 3 * 2 * 2 * len(KGRID))
    k0 = df[df.k == 0]
    gate("G2 all k=0 cells identical per panel (max Sharpe dev)",
         f"{k0.groupby('panel').full_Sharpe.apply(lambda s: s.max()-s.min()).max():.3e}", "0.0",
         float(k0.groupby("panel").full_Sharpe.apply(lambda s: s.max() - s.min()).max()) == 0.0)
    u0 = float(df[(df.panel == "U56") & (df.k == 0)].full_Sharpe.iloc[0])
    gate("G3 U56 k=0 reproduces the committed anchor Sharpe", f"{u0:.4f}", "1.1480", abs(u0 - 1.1480) < 5e-4)
    d0 = float(df[(df.panel == "U56") & (df.k == 0)].full_MaxDD.iloc[0])
    gate("G4 U56 k=0 reproduces the committed anchor MaxDD", f"{d0:.4f}", "-0.1913", abs(d0 + 0.1913) < 5e-4)
    gate("G5 deletions actually shrink the panel", int(df[df.k == 12].n_inv.min()),
         "= n0 - 12", bool((df[df.k == 12].n_inv + 12 == df[df.k == 12].panel.map(
             df[df.k == 0].set_index("panel").n_inv.to_dict())).all()))
    gate("G6 SPY never a constituent", 0, 0, not any("SPY" in str(x).split("|") for x in df.dropped))
    gate("G7 costs = 10 bps", COST, 10.0, COST == 10.0)
    gate("G8 OOS split date", str(OOS_START.date()), "2017-01-01", True)
    gate("G9 4b bars do not move with k (SPY is not in the panel)", "by construction", "yes", True)
    g = pd.DataFrame(GATES)
    say("\n## GATES")
    say(g.to_string(index=False))
    say(f"\n{int(g.pass_.sum())} of {len(g)} gates pass; {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()

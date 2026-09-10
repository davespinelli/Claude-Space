#!/usr/bin/env python3
"""Idea 396 - "the-stop-family-never-beats-its-own-exposure" (cloud, 2026-09-10).

The finding this run exists to settle
-------------------------------------
Idea 135 (`2026-09-07_is-a-class-member-just-its-own-ladder-point_B2`) reports per-kind
survival against a matched-mean-gross control of `gate` 18.0% (58 of 323), `dd` 7.9%,
`bud` 3.5% and **`stop` 0.0% - 0 of 59** (and 0 of 12 in the parallel cloud run): no trailing
stop arm anywhere in the record beats simply HOLDING LESS of the same book at the same mean
gross.  The queue's objection is that the record has only ever run the stop at TWO levels -
15% and 25% - so a 0-of-59 could be a statement about those two numbers rather than about the
instrument.

This run sweeps the stop across its own range, from a stop so tight it fires almost daily to
one so loose it barely fires at all, and re-runs the matched-gross control at every point.  If
the dSharpe-vs-control curve is negative at EVERY level on EVERY book and EVERY panel, the
0-of-59 is a property of the INSTRUMENT and idea 74's "the stop is the dearest menu entry"
stands as a general result.  If a level exists where the stop wins, the record's stop KILL was
a level artefact and has to be re-read.

A trailing stop is the record's fastest de-grossing instrument: it spends time in cash, so the
honest comparand - inherited from ideas 66/94/135 verbatim - is the SAME book de-grossed to the
stop arm's own realised mean invested fraction.  Anything the stop buys that de-grossing also
buys is not the stop's.

New this run, carried over from idea 604 (same day): the stop arm also gets a BLOCK PLACEBO
column - the arm's own invested-fraction path circularly shifted, so the placebo holds the
same amount of cash on the same number of days with the same run-length distribution and NO
information about when to hold it.  Idea 602 showed the record's twin leg is uncentred without
one.  Here it answers a sharper question: if the stop loses to its de-grossed control, does it
at least beat a no-information cash path of the same shape?

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (LEVEL vs INSTRUMENT)  Over an 11-point stop ladder from 3% to 50%, is there ANY
                              (panel, book, stop, cooldown, cost) cell where the stop beats its
                              own matched-mean-gross control on Sharpe?  Reported as the full
                              curve, not a count.
    Q2 (SHAPE)                Is dSharpe monotone in the stop level, and where does the curve
                              peak?  If the record's 15%/25% happen to sit at the curve's
                              minimum the KILL was measured at the worst two points.
    Q3 (WHAT IT BUYS)         At matched gross, what does the stop actually pay and receive?
                              dCAGR, dMaxDD and dCalmar beside dSharpe at every point.
    Q4 (PLACEBO)              Does the stop beat a BLOCK placebo holding the same cash on the
                              same day-count with the same clustering and no information?
    Q5 (KEEP + RULE 8)        Both PROTOCOL KEEP paths on every arm (4a vs cost-matched
                              RULES v2, 4b vs SPY), and the rule-8 walk-forward: choose
                              (stop, cooldown) on 2009-2016 by IS Sharpe, read the pick once on
                              2017+ against the un-stopped book, RULES v2 and SPY.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. stop level S     0.03 0.05 0.075 0.10 0.125 0.15 0.20 0.25 0.30 0.40 0.50
                        (the record's own two, 0.15 and 0.25, are points 6 and 8)
    2. cooldown C       0 or 21 trading days before a stopped name may be re-bought
    ALL grid points reported at every panel / book / cost rung.  Nothing else is tuned.

Reported axes, NEVER tuned or selected on
    panel  U56 / B136 / SMALL(sub-$2B, 439 names)
    book   v1 (RULES v1 top-5) / TOP20 (the 2026-09-04 KEEP 4b candidate: top-20 equal weight,
           no vol scaler) / EWALL (eligible equal weight at gross 0.75)
    cost   0 / 10 / 25 bps          cadence  weekly (FREQ='W')

Reproduction gates (section [0], printed before any new number is read)
    G1  run_stop(stop=None) reproduces engine.backtest EXACTLY on every panel x book
        (max|dreturn| and max|dturnover| must be 0).
    G2  idea 84's ungated EWALL U56 g=0.85 @10bps landmark: 11.8% / 1.05 / -17.9% / H 1.07/1.04.
    G3  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=c).
    G4  de-grossed control interpolation on the 0.01 lambda cache vs a true backtest at the
        exact lambda, 6 off-grid values.
    G5  BLOCK placebo matching identity: the placebo's mean invested fraction and its
        de-grossed-day count reproduce the stop arm's EXACTLY, so it shares the arm's control.

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: all three panels are CURRENT-CONSTITUENT lists, so CAGR and drawdown LEVELS are
optimistic.  The stop-vs-control CONTRAST is the durable part.  The small panel drops every
ticker with max_1d_move >= 1.0 in data/small_meta.csv before anything is computed (44 names)
and starts 2010-01-04, so its halves are not U56/B136's calendar halves.

`run_stop` is idea 9's simulator (2026-09-04_trailing-stop_cloud.py) reproduced verbatim so
this file is standalone; G1 asserts the reproduction.  Deterministic.  Modifies nothing.
"""
import hashlib
import sys
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

FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
NPOS = 20
STOPS = [0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]  # tuned param 1
RECORD_STOPS = [0.15, 0.25]          # the only two the record has ever run
COOLDOWNS = [0, 21]                  # tuned param 2
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12
LSTEP = 0.01
NSEED = 10

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# =====================================================================================
# books
# =====================================================================================
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def w_ewall(px):
    e = eligible_mask(px).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


def w_top20(px):
    """The 2026-09-04 KEEP 4b candidate: top-20 equal weight, NO vol scaler."""
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


BOOKS = {"v1": rules_v1_weights, "TOP20": w_top20, "EWALL": w_ewall}


# =====================================================================================
# simulator (idea 9, 2026-09-04_trailing-stop_cloud.py, verbatim)
# =====================================================================================
def run_stop(prices, weights, stop=None, cooldown=0, freq=FREQ):
    """engine.backtest + a per-name trailing stop, at zero cost (costs applied later).

    stop=None reproduces engine.backtest exactly (G1).  The stop is evaluated at close t on
    the running high since the position opened and executed at close t+1; stopped capital goes
    to cash and the name is blocked for `cooldown` trading days.
    """
    rets = prices.pct_change().fillna(0.0).values
    pxv = prices.values
    n = pxv.shape[1]
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values

    cur = np.zeros(n)
    peak = np.full(n, np.nan)
    blocked_until = np.zeros(n, dtype=int)
    pending = np.zeros(n, dtype=bool)
    port = np.zeros(len(prices))
    turn = np.zeros(len(prices))
    invested = np.zeros(len(prices))
    n_stops = 0

    for i in range(len(prices)):
        if pending.any():
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        if mask[i] or i == 0:
            new = w_target[i].copy()
            if stop is not None and cooldown > 0:
                new = np.where(blocked_until > i, 0.0, new)
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held = cur.copy()
        invested[i] = held.sum()
        port[i] = float(np.nansum(held * rets[i]))
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
        if stop is not None:
            alive = cur > 1e-9
            p = pxv[i]
            peak = np.where(alive, np.fmax(np.where(np.isnan(peak), -np.inf, peak), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak * (1 - stop))
            if hit.any():
                pending |= hit
                n_stops += int(hit.sum())
                blocked_until = np.where(hit, i + 1 + cooldown, blocked_until)

    idx = prices.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(invested, index=idx), n_stops)


# =====================================================================================
# helpers
# =====================================================================================
def sharpe(r):
    v = r.std()
    return (r.mean() * 252) / (v * np.sqrt(252)) if v else np.nan


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def tests_4b(r, spy_pack):
    s1, s2, s_oos, s_dd, s_cagr = spy_pack
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > s_oos,
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def verdict_4a(r, base_pack):
    b1, b2, bdd = base_pack
    h1, h2 = half_sharpes(r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= bdd)


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


class DeGrossed:
    """The SAME book scaled to lambda of its weights, cached on a LSTEP lambda grid and
    interpolated to an exact lambda.  G4 prices the interpolation error."""

    def __init__(self, px, w, start):
        self.px, self.w, self.start, self.cache, self.n_bt = px, w, start, {}, 0

    def _exact(self, lam):
        lam = round(lam, 6)
        if lam not in self.cache:
            res = backtest(self.px, self.w * lam, cost_bps=0, freq=FREQ)
            self.cache[lam] = (res["returns"].loc[self.start:], res["turnover"].loc[self.start:])
            self.n_bt += 1
        return self.cache[lam]

    def at(self, lam, cost_bps):
        lam = float(np.clip(lam, 0.0, 1.0))
        lo = round(np.floor(round(lam, 6) / LSTEP) * LSTEP, 6)
        f = (round(lam, 6) - lo) / LSTEP
        if f <= 1e-9:
            r0, t0 = self._exact(lo)
        else:
            rl, tl = self._exact(lo)
            rh, th = self._exact(round(lo + LSTEP, 6))
            r0, t0 = (1 - f) * rl + f * rh, (1 - f) * tl + f * th
        return r0 - t0 * cost_bps / 1e4


def block_shift(path, seed):
    """Circular shift: exact mean, exact run-length distribution, zero information."""
    rng = np.random.default_rng(seed)
    return pd.Series(np.roll(path.values, int(rng.integers(1, len(path)))), index=path.index)


# =====================================================================================
# per panel
# =====================================================================================
def run_panel(panel, px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    s1, s2 = half_sharpes(spy)
    spy_pack = (s1, s2, metrics(spy.loc[OOS_START:])["Sharpe"], ms["MaxDD"], ms["CAGR"])

    log(f"\n{'='*185}")
    log(f"PANEL {panel}: {px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"eval from {start.date()} ({len(px.loc[start:])} days)")
    log(f"  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}; 4b bars: CAGR floor "
        f"{0.70*ms['CAGR']:.2%}, DD cap {-0.60*abs(ms['MaxDD']):.2%}, halves {s1:.3f}/{s2:.3f}, "
        f"OOS {spy_pack[2]:.3f}")

    v2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    v2r0, v2t = v2["returns"].loc[start:], v2["turnover"].loc[start:]
    base_packs = {}
    for c in RUNGS:
        rv = v2r0 - v2t * c / 1e4
        h1, h2 = half_sharpes(rv)
        base_packs[c] = (h1, h2, metrics(rv)["MaxDD"])
    mv = metrics(v2r0 - v2t * RUNG_HEAD / 1e4)
    log(f"  RULES v2 @10bps {mv['CAGR']:.2%} / {mv['Sharpe']:.3f} / {mv['MaxDD']:.2%}")

    rows, praw = [], []
    for bk, wf in BOOKS.items():
        w = wf(px)
        dg = DeGrossed(px, w, start)
        r0_ns, t0_ns, inv_ns, _ = run_stop(px, w, stop=None)
        r0_ns, t0_ns, inv_ns = r0_ns.loc[start:], t0_ns.loc[start:], inv_ns.loc[start:]
        # G1 on this panel x book
        eb = backtest(px, w, cost_bps=0, freq=FREQ)
        g1r = float(abs(r0_ns - eb["returns"].loc[start:]).max())
        g1t = float(abs(t0_ns - eb["turnover"].loc[start:]).max())
        m_ns = metrics(r0_ns - t0_ns * RUNG_HEAD / 1e4)
        log(f"\n  book {bk}: G1 stop=None vs engine.backtest  max|dret| {g1r:.3e}  "
            f"max|dturn| {g1t:.3e}  [{'PASS' if max(g1r,g1t)<1e-15 else 'FAIL'}]")
        log(f"    un-stopped @10bps {m_ns['CAGR']:.2%} / {m_ns['Sharpe']:.3f} / "
            f"{m_ns['MaxDD']:.2%}; mean invested {inv_ns.mean():.4f}")

        for S in STOPS:
            for C in COOLDOWNS:
                r0, t0, inv, ns = run_stop(px, w, stop=S, cooldown=C)
                r0, t0, inv = r0.loc[start:], t0.loc[start:], inv.loc[start:]
                lam = inv.mean() / inv_ns.mean() if inv_ns.mean() > 0 else 0.0
                # placebo: the arm's own invested path, circularly shifted, applied to the
                # un-stopped book as a multiplier (same mean, same run lengths, no information)
                mult = (inv / inv_ns.replace(0, np.nan)).fillna(1.0).clip(0, 1)
                pmults = [block_shift(mult, seed_of(panel, bk, S, C, s)) for s in range(NSEED)]
                for c in RUNGS:
                    r = r0 - t0 * c / 1e4
                    ctl = dg.at(lam, c)
                    mr, mc = metrics(r), metrics(ctl)
                    h1, h2 = half_sharpes(r)
                    t4b = tests_4b(r, spy_pack)
                    row = dict(panel=panel, book=bk, stop=S, cool=C, cost=c,
                               n_stops=ns, stops_per_yr=ns / metrics(r)["Years"],
                               mean_inv=float(inv.mean()), lam=lam,
                               turn_yr=float(t0.sum() / metrics(r)["Years"]),
                               CAGR=mr["CAGR"], Sharpe=mr["Sharpe"], MaxDD=mr["MaxDD"],
                               Calmar=mr["Calmar"], H1=h1, H2=h2,
                               OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                               OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                               OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                               ctl_CAGR=mc["CAGR"], ctl_Sharpe=mc["Sharpe"],
                               ctl_MaxDD=mc["MaxDD"], ctl_Calmar=mc["Calmar"],
                               dSharpe=mr["Sharpe"] - mc["Sharpe"],
                               dCAGR=mr["CAGR"] - mc["CAGR"],
                               dMaxDD=mr["MaxDD"] - mc["MaxDD"],
                               dCalmar=mr["Calmar"] - mc["Calmar"],
                               dOOS=metrics(r.loc[OOS_START:])["Sharpe"] - metrics(ctl.loc[OOS_START:])["Sharpe"],
                               win=bool(mr["Sharpe"] - mc["Sharpe"] > TIE),
                               p4a=verdict_4a(r, base_packs[c]), p4b=all(t4b.values()),
                               fail4b=",".join(k for k, v in t4b.items() if not v) or "-")
                    row["dSharpe_IS"] = sharpe(r.loc[:IS_END]) - sharpe(ctl.loc[:IS_END])
                    row["IS_Sharpe"] = sharpe(r.loc[:IS_END])
                    rows.append(row)
                    for s, pm in enumerate(pmults):
                        rp = pm * (r0_ns - t0_ns * c / 1e4) - pm.diff().abs().fillna(0) * GROSS * c / 1e4
                        praw.append(dict(panel=panel, book=bk, stop=S, cool=C, cost=c, seed=s,
                                         p_mean_mult=float(pm.mean()),
                                         dSharpe=sharpe(rp) - sharpe(ctl),
                                         win=bool(sharpe(rp) - sharpe(ctl) > TIE)))
    return pd.DataFrame(rows), pd.DataFrame(praw)


# =====================================================================================
def main():
    log(f"# {STEM}")
    log("# idea 396 - the stop family never beats its own exposure: is that the LEVEL or the "
        "INSTRUMENT?")
    log(f"# tuned params: (1) stop level {STOPS}  (2) cooldown {COOLDOWNS}. "
        f"All other axes reported, never selected on.")
    log(f"# the record has only ever run the stop at {RECORD_STOPS} (idea 135: stop 0.0%, 0 of 59)")

    # ------------------------------------------------------------------ [0] gates
    log("\n" + "=" * 185)
    log("[0] REPRODUCTION GATES")
    log("=" * 185)
    px_u = load_universe()
    start_u = px_u.index[260]
    w85 = w_ewall(px_u) / GROSS * 0.85
    b0 = backtest(px_u, w85, cost_bps=0, freq=FREQ)
    b10 = backtest(px_u, w85, cost_bps=10, freq=FREQ)
    g3 = float(abs((b0["returns"] - b0["turnover"] * 10 / 1e4) - b10["returns"]).max())
    log(f"  G3 derived-rung identity: max|diff| {g3:.3e}  [{'PASS' if g3 < 1e-12 else 'FAIL'}]")
    rr = b10["returns"].loc[start_u:]
    m84 = metrics(rr)
    h1, h2 = half_sharpes(rr)
    log(f"  G2 idea 84 EWALL U56 g=0.85 @10bps: {m84['CAGR']:.1%} / {m84['Sharpe']:.2f} / "
        f"{m84['MaxDD']:.1%} / H {h1:.2f}/{h2:.2f}   (committed 11.8% / 1.05 / -17.9% / 1.07/1.04)")
    dg = DeGrossed(px_u, w_ewall(px_u), start_u)
    errs = []
    for lam in (0.6234, 0.7117, 0.7788, 0.8351, 0.9042, 0.4567):
        true = backtest(px_u, w_ewall(px_u) * lam, cost_bps=10, freq=FREQ)["returns"].loc[start_u:]
        errs.append(abs(sharpe(dg.at(lam, 10)) - sharpe(true)))
    log(f"  G4 de-gross interpolation over 6 off-grid lambda: max|dSharpe| {max(errs):.3e}, "
        f"mean {np.mean(errs):.3e}")

    # ------------------------------------------------------------------ panels
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pxs, ndrop = small_panel()
    panels["SMALL"] = pxs
    log(f"\n  small panel: dropped {ndrop} tickers with max_1d_move >= 1.0 -> {pxs.shape[1]-1} names")

    As, Ps = [], []
    for name, px in panels.items():
        a, p = run_panel(name, px)
        As.append(a)
        Ps.append(p)
    A = pd.concat(As, ignore_index=True)
    P = pd.concat(Ps, ignore_index=True)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    P.to_csv(OUT / f"{STEM}.placebo.csv", index=False)

    j = P.merge(A[["panel", "book", "stop", "cool", "cost", "lam"]],
                on=["panel", "book", "stop", "cool", "cost"])
    log(f"\n  G5 placebo matching identity: max|mean multiplier - lambda| "
        f"{abs(j.p_mean_mult - j.lam).max():.3e}")

    # ------------------------------------------------------------------ Q1
    log("\n" + "=" * 185)
    log("[1] Q1 - is there ANY cell where the stop beats its own matched-mean-gross control?")
    log("=" * 185)
    log(f"  arms {len(A)} = 3 panels x 3 books x {len(STOPS)} stops x {len(COOLDOWNS)} cooldowns "
        f"x {len(RUNGS)} rungs")
    log(f"  WINS (dSharpe > 0): {int(A.win.sum())} of {len(A)} = {A.win.mean():.1%}")
    log("  by cost rung: " + ", ".join(f"{c} bps {int(A[A.cost==c].win.sum())}/{int((A.cost==c).sum())}"
                                       for c in RUNGS))
    log("  by panel:     " + ", ".join(f"{p} {int(A[A.panel==p].win.sum())}/{int((A.panel==p).sum())}"
                                       for p in A.panel.unique()))
    log("  by book:      " + ", ".join(f"{b} {int(A[A.book==b].win.sum())}/{int((A.book==b).sum())}"
                                       for b in A.book.unique()))
    log("  by stop level:")
    for S in STOPS:
        sub = A[A.stop == S]
        tag = "  <- record's own level" if S in RECORD_STOPS else ""
        log(f"    S={S:<6} wins {int(sub.win.sum()):>3}/{len(sub):<3}  median dSharpe "
            f"{sub.dSharpe.median():+.4f}  median dOOS {sub.dOOS.median():+.4f}  "
            f"median lambda {sub.lam.median():.3f}  stops/yr {sub.stops_per_yr.median():.0f}{tag}")
    if A.win.any():
        log("\n  the winning cells:")
        cols = ["panel", "book", "stop", "cool", "cost", "lam", "Sharpe", "ctl_Sharpe",
                "dSharpe", "dOOS", "dCAGR", "dMaxDD", "p4a", "p4b"]
        log(A[A.win][cols].round(4).to_string(index=False))
    else:
        log("\n  NO winning cell anywhere on the ladder.")

    # ------------------------------------------------------------------ Q2
    log("\n" + "=" * 185)
    log("[2] Q2 - the SHAPE of the curve: median dSharpe vs stop level, per panel x book "
        f"(cost {RUNG_HEAD} bps, cooldown pooled)")
    log("=" * 185)
    piv = A[A.cost == RUNG_HEAD].pivot_table(index="stop", columns=["panel", "book"],
                                             values="dSharpe", aggfunc="median")
    log(piv.round(4).to_string())
    log("\n  argmax of the curve per panel x book (the best stop level there is), 10 bps:")
    best = (A[A.cost == RUNG_HEAD].groupby(["panel", "book", "stop"])["dSharpe"].median()
            .reset_index().sort_values("dSharpe", ascending=False)
            .groupby(["panel", "book"]).head(1).sort_values(["panel", "book"]))
    log(best.round(4).to_string(index=False))
    rec = A[(A.cost == RUNG_HEAD) & (A.stop.isin(RECORD_STOPS))].groupby(["panel", "book"])["dSharpe"].median()
    allm = A[A.cost == RUNG_HEAD].groupby(["panel", "book"])["dSharpe"].median()
    cmp_ = pd.DataFrame({"record_15_25": rec, "whole_ladder": allm})
    cmp_["record_worse_than_ladder"] = cmp_.record_15_25 < cmp_.whole_ladder
    log("\n  were 15%/25% the WORST two points?  median dSharpe there vs over the whole ladder:")
    log(cmp_.round(4).to_string())
    log(f"    the record's two levels are BELOW the ladder median in "
        f"{int(cmp_.record_worse_than_ladder.sum())} of {len(cmp_)} panel x book cells")

    # ------------------------------------------------------------------ Q3
    log("\n" + "=" * 185)
    log("[3] Q3 - at matched gross, what does the stop PAY and what does it BUY? "
        f"(median over cells, {RUNG_HEAD} bps)")
    log("=" * 185)
    q3 = (A[A.cost == RUNG_HEAD].groupby("stop")[["dCAGR", "dMaxDD", "dCalmar", "dSharpe",
                                                  "turn_yr", "lam"]].median())
    log(q3.round(4).to_string())
    log("\n  same, split by panel:")
    log(A[A.cost == RUNG_HEAD].pivot_table(index="stop", columns="panel",
                                           values=["dCAGR", "dMaxDD"], aggfunc="median").round(4).to_string())

    # ------------------------------------------------------------------ Q4
    log("\n" + "=" * 185)
    log("[4] Q4 - the BLOCK placebo: does the stop beat a no-information cash path of the "
        "same shape?")
    log("=" * 185)
    for c in RUNGS:
        rw = A[A.cost == c]["win"].mean()
        pw = P[P.cost == c]["win"].mean()
        log(f"    cost {c:>2} bps: REAL win {rw:.3f}   BLOCK placebo win {pw:.3f}   "
            f"diff {rw - pw:+.3f}   median dSharpe REAL {A[A.cost==c].dSharpe.median():+.4f} "
            f"vs BLOCK {P[P.cost==c].dSharpe.median():+.4f}")
    log("\n  per panel x book (10 bps): REAL win rate, BLOCK win rate, difference")
    kk = ["panel", "book"]
    rw = A[A.cost == RUNG_HEAD].groupby(kk)["win"].mean()
    pw = P[P.cost == RUNG_HEAD].groupby(kk)["win"].mean()
    T = pd.DataFrame({"REAL": rw, "BLOCK": pw})
    T["diff"] = T.REAL - T.BLOCK
    log(T.round(3).to_string())
    log(f"    REAL beats BLOCK in {int((T['diff'] > 0).sum())} of {len(T)} cells; "
        f"REVERSED (placebo better) in {int((T['diff'] < 0).sum())}")

    # ------------------------------------------------------------------ Q5 KEEP
    log("\n" + "=" * 185)
    log("[5] Q5a - PROTOCOL KEEP paths on every arm")
    log("=" * 185)
    log(f"  4a (vs cost-matched RULES v2): {int(A.p4a.sum())} of {len(A)}; at 10 bps "
        f"{int(A[A.cost==RUNG_HEAD].p4a.sum())} of {int((A.cost==RUNG_HEAD).sum())}")
    log(f"  4b (vs SPY):                   {int(A.p4b.sum())} of {len(A)}; at 10 bps "
        f"{int(A[A.cost==RUNG_HEAD].p4b.sum())} of {int((A.cost==RUNG_HEAD).sum())}")
    log("  4a by rung: " + ", ".join(f"{c} bps {int(A[A.cost==c].p4a.sum())}" for c in RUNGS))
    log("  4b by rung: " + ", ".join(f"{c} bps {int(A[A.cost==c].p4b.sum())}" for c in RUNGS))
    log("  binding 4b bar at 10 bps:")
    log(A[A.cost == RUNG_HEAD]["fail4b"].value_counts().head(10).to_string())
    both = A[A.p4a & A.p4b]
    log(f"\n  arms passing BOTH paths: {len(both)}")
    if len(A[A.p4b]):
        cols = ["panel", "book", "stop", "cool", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "dSharpe", "win", "p4a"]
        log("  the 4b passers:")
        log(A[A.p4b][cols].round(4).to_string(index=False))

    # ------------------------------------------------------------------ rule 8
    log("\n" + "=" * 185)
    log("[6] Q5b - RULE 8 WALK-FORWARD: choose (stop, cooldown) on 2009-2016 by IS Sharpe, "
        "read once on 2017+")
    log("=" * 185)
    wf_rows = []
    for panel, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
        v2r = (v2["returns"] - v2["turnover"] * RUNG_HEAD / 1e4).loc[start:]
        for bk, wfun in BOOKS.items():
            sub = A[(A.panel == panel) & (A.book == bk) & (A.cost == RUNG_HEAD)]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            w = wfun(px)
            r0, t0, inv, _ = run_stop(px, w, stop=float(pick["stop"]), cooldown=int(pick["cool"]))
            r = (r0 - t0 * RUNG_HEAD / 1e4).loc[start:]
            r0n, t0n, invn, _ = run_stop(px, w, stop=None)
            rn = (r0n - t0n * RUNG_HEAD / 1e4).loc[start:]
            dgb = DeGrossed(px, w, start)
            ctl = dgb.at(float(pick["lam"]), RUNG_HEAD)
            mo = metrics(r.loc[OOS_START:])
            mn = metrics(rn.loc[OOS_START:])
            mc = metrics(ctl.loc[OOS_START:])
            mv = metrics(v2r.loc[OOS_START:])
            msp = metrics(spy.loc[OOS_START:])
            log(f"\n    {panel} / {bk}: IS pick stop={pick['stop']} cool={int(pick['cool'])} "
                f"(IS Sharpe {pick['IS_Sharpe']:.3f}, IS dSharpe vs control {pick['dSharpe_IS']:+.4f})")
            log(f"      OOS 2017+  stop arm      {mo['CAGR']:>7.2%} / {mo['Sharpe']:.3f} / {mo['MaxDD']:>7.2%}")
            log(f"                 matched-gross {mc['CAGR']:>7.2%} / {mc['Sharpe']:.3f} / {mc['MaxDD']:>7.2%}")
            log(f"                 un-stopped    {mn['CAGR']:>7.2%} / {mn['Sharpe']:.3f} / {mn['MaxDD']:>7.2%}")
            log(f"                 RULES v2      {mv['CAGR']:>7.2%} / {mv['Sharpe']:.3f} / {mv['MaxDD']:>7.2%}")
            log(f"                 SPY           {msp['CAGR']:>7.2%} / {msp['Sharpe']:.3f} / {msp['MaxDD']:>7.2%}")
            wf_rows.append(dict(panel=panel, book=bk, stop=float(pick["stop"]), cool=int(pick["cool"]),
                                IS_Sharpe=float(pick["IS_Sharpe"]), IS_dSharpe=float(pick["dSharpe_IS"]),
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                ctl_OOS_Sharpe=mc["Sharpe"], nostop_OOS_Sharpe=mn["Sharpe"],
                                v2_OOS_CAGR=mv["CAGR"], v2_OOS_Sharpe=mv["Sharpe"], v2_OOS_MaxDD=mv["MaxDD"],
                                spy_OOS_CAGR=msp["CAGR"], spy_OOS_Sharpe=msp["Sharpe"], spy_OOS_MaxDD=msp["MaxDD"],
                                beats_ctl=bool(mo["Sharpe"] > mc["Sharpe"]),
                                beats_nostop=bool(mo["Sharpe"] > mn["Sharpe"]),
                                beats_v2=bool(mo["Sharpe"] > mv["Sharpe"]),
                                beats_spy=bool(mo["Sharpe"] > msp["Sharpe"])))
    W = pd.DataFrame(wf_rows)
    W.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    log(f"\n    OOS: picks beating their matched-gross control {int(W.beats_ctl.sum())}/{len(W)}, "
        f"the un-stopped book {int(W.beats_nostop.sum())}/{len(W)}, RULES v2 "
        f"{int(W.beats_v2.sum())}/{len(W)}, SPY {int(W.beats_spy.sum())}/{len(W)}")
    log(f"    IS->OOS sign of dSharpe vs control: IS positive in {int((W.IS_dSharpe>0).sum())}/{len(W)}, "
        f"OOS positive in {int(W.beats_ctl.sum())}/{len(W)}")

    (OUT / f"{STEM}.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.txt / .arms.csv / .placebo.csv / .wf.csv")


if __name__ == "__main__":
    main()

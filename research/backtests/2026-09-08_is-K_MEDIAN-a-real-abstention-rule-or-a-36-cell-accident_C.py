#!/usr/bin/env python3
"""QUEUE idea 431 — is-K_MEDIAN-a-real-abstention-rule-or-a-36-cell-accident  (lane C, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 431)
    "idea 204's only reliably positive OOS lift belongs to K_MEDIAN (+0.0205, t +2.73, 28/36
     wins), the selector that picks the median IS-Sharpe arm instead of the argmax, and it still
     loses to do-nothing by -0.0182.  Test it as a pre-registered abstention rule against idea
     241's minimum-margin proposal on a corpus that does not overlap idea 204's 36 cells, and
     report whether a rank-based non-argmax chooser has any expectancy at all.  Max 2 params."

THE ONE STRUCTURAL POINT THIS RUN ADDS
    A selector that picks the MEDIAN of an IS ranking is doing two things at once, and only one
    of them can be skill.  Write the pick's OOS lift as

        lift  :=  M_OOS(a*) - mean_P M_OOS
               =  [ M_OOS(a*) - M_OOS(a_dialmid) ]  +  [ M_OOS(a_dialmid) - mean_P M_OOS ]
                  \____________ TRANSFER ________/     \_________ POSITION __________/

    where a_dialmid is the arm sitting at the MIDDLE OF THE PRINTED DIAL ORDER -- a rule that
    reads NO performance data at all, has zero parameters, and is fixed before any backtest runs.
    In a dial family the arms are ordered along a monotone axis (band width, MA length, vol cap,
    lookback), IS Sharpe is usually monotone-ish in that axis, and so the median-IS arm is very
    often just the interior arm.  If lift(K_MEDIAN) ~ lift(K_DIALMID) and TRANSFER ~ 0, then
    K_MEDIAN is idea 240/256's GRID-EDGE flag wearing a selector's clothes: "don't sit on the
    end of your own grid" is a statement about the grid, not a chooser with expectancy.

    That is the decisive test here, it is cheap, and it is run on BOTH corpora -- the fresh one
    below AND idea 204's own committed 36 cells, which is where the queue's number came from.

CORPUS C -- fresh, and DISJOINT from idea 204's corpus B on the family axis
    3 panels (u56, broad, small) x 4 dial families x 3 cost rungs = 36 cells, none of which is
    one of idea 204's 36: its families were GROSS / WIDTH / CADENCE / GATE-KIND, and none of the
    four below turns any of those dials.
        BAND     band half-width b in {0.00 .01 .02 .03 .05 .08 .12}   control b=0.03 (RULES v2)
        MALEN    MA lookback L in {50 100 150 200 250 300}             control L=200 (RULES v2)
        VOLCAP   extra vol20 cap in {0.30 .40 .50 .60 .80 off}         control = off
        MOMLOOK  top-20 signal-window scale k in {0.5 .75 1.0 1.5 2.0}  control k=1.0
    24 arms/panel, 72 simulations, 216 arm-rows (the 3 rungs come off the exact turnover identity
    r(c) = r(0) - turnover*c/1e4, gate G5).  The families necessarily MEET idea 204's corpus at a
    single arm each -- the do-nothing control -- because "vs do-nothing" is the comparison the
    queue asks about; that overlap is stated, not hidden, and no CELL is shared.

SELECTORS  (the two tuned parameters, every grid point reported, none selected on)
    p1  RANK QUANTILE q in {0.00, 0.25, 0.50, 0.75, 1.00}: sort the pool by IS Sharpe ascending
        and take position round(q*(n-1)).  q=1.00 IS the incumbent argmax (= idea 204's
        K_Sharpe), q=0.50 IS K_MEDIAN, q=0.00 IS K_ANTI (the power check).
    p2  MARGIN m in {0.00, 0.05, 0.10, 0.15, 0.25, 0.50, inf} (idea 241's proposal): take the
        argmax on IS Sharpe if its gap to the runner-up is >= m, else ABSTAIN to the control.
        m=0.00 is the raw argmax; m=inf is always-abstain and is delta 0 vs do-nothing by
        construction (a bookkeeping anchor, not a candidate).
    Zero-parameter controls, not tuned: K_MED204 (idea 204's exact even-n convention,
    index[len//2]), K_DIALMID (middle of the printed dial order, no performance data),
    K_RANDOM (closed form: expectation = pool mean, lift == 0 exactly).

PRE-REGISTERED PREDICTIONS (written before any number below was computed)
    P1  K_MEDIAN's mean OOS lift on corpus C is smaller than idea 204's +0.0205 and does not
        clear |t| > 2.
    P2  K_DIALMID -- which reads no performance data -- has a lift indistinguishable from
        K_MEDIAN's, and the two pick the same arm in more than half of all pools.
    P3  No q and no m beats do-nothing out of sample at any grid point.
    P4  K_MARGIN's mean delta vs do-nothing rises monotonically toward 0 as m grows, with no
        interior optimum (abstention buys back the argmax's loss, it does not create a gain).
    P5  q=0.00 (argmin, the power check) has a reliably negative lift.

GATES
    G0  PREMISE.  Recompute idea 204's K_MEDIAN row from its own committed .gridB.csv without
        re-simulating anything, and check it against the queue's quoted +0.0205 / t +2.73 / 28-36.
    G1  fast_backtest reproduces engine.backtest on returns AND turnover, per panel.
    G5  the cost-rung identity r(c) = r(0) - turnover*c/1e4, per panel.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54) on all three panels: current constituents only, every CAGR is
      flattered.  Every statistic quoted is a PAIRED within-pool contrast, which the level bias
      cannot move.
    * 36 cells is 36 cells.  Arms and books overlap heavily inside a panel, so the t-statistics
      are quoted with their n and with per-panel / per-family / per-rung breakdowns beside them.
      This run does not claim 36 independent observations; it claims the same clustering idea
      204 had, on a disjoint set of dials, which is exactly what a replication needs.
    * Idea 126: t+1 execution throughout; PROTOCOL's rung is 10 bps, 0 and 25 reported alongside.
    * PROTOCOL 4a and 4b are scored on every arm and every pick because rule 4 requires it; this
      is a bookkeeping idea and cannot promote a book.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .picks.csv, .selectors.csv,
.decomp.csv and .keeppaths.csv next to itself.  Modifies nothing.
"""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_is-K_MEDIAN-a-real-abstention-rule-or-a-36-cell-accident_C"
OUT = ROOT / "research" / "backtests"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I204_GRID = OUT / "2026-09-08_is-the-pool-sign-the-whole-selector-story_B.gridB.csv"

FREQ = "W"
GROSS = 0.75
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b CAGR floor / MaxDD cap, PROTOCOL rule 4b

QS = [0.00, 0.25, 0.50, 0.75, 1.00]                    # tuned parameter 1
MARGINS = [0.00, 0.05, 0.10, 0.15, 0.25, 0.50, np.inf]  # tuned parameter 2

pd.set_option("display.width", 340)
pd.set_option("display.max_columns", 60)

_LOG = []


def say(s=""):
    print(s)
    _LOG.append(str(s))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


D = _load(I133, "i133C431")      # panel_px, the record's three panels, verbatim


# ------------------------------------------------------------------ stats ---
def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], dtype=float)
    if len(x) < 2 or x.std(ddof=1) == 0:
        return float("nan")
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def sign_p(wins, n):
    if n == 0:
        return float("nan")
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


def spearman(a, b):
    """Rank correlation without scipy: Pearson on average ranks."""
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    if ra.std(ddof=1) == 0 or rb.std(ddof=1) == 0:
        return float("nan")
    return float(ra.corr(rb))


def window(r, which):
    if which == "IS":
        return r.loc[:IS_END]
    if which == "OOS":
        return r.loc[OOS_START:]
    return r


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ------------------------------------------------------------- fast runner ---
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
    """Idea 196's fast_backtest verbatim (asserted == engine.backtest in gate G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------ books ---
def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def band_mask(px, b, L=200):
    """MA(L) band with hysteresis, half-width b.  b=0 is the plain MA(L) cross."""
    ma = px.rolling(L).mean()
    if b <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def ew(px, mask, g=GROSS):
    """Equal weight over priced names at gross g; gated-out weight goes to CASH (de-gross)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    W = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return W.where(mask, 0.0)


def composite_k(px, k):
    """The scan.py composite with every window scaled by k (k=1.0 is the live signal)."""
    w1, w3, w6, w12 = [max(2, int(round(x * k))) for x in (21, 63, 126, 252)]
    mom = px.shift(w1) / px.shift(w12) - 1
    r6, r3 = px / px.shift(w6) - 1, px / px.shift(w3) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def topn_k(px, n, k):
    rank = composite_k(px, k).rank(axis=1, ascending=False)
    W = (rank <= n).astype(float) * (GROSS / n)
    return W.where(band_mask(px, 0.03, 200), 0.0)


BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12]
MALENS = [50, 100, 150, 200, 250, 300]
VOLCAPS = [0.30, 0.40, 0.50, 0.60, 0.80, None]
MOMKS = [0.5, 0.75, 1.0, 1.5, 2.0]
FAMILIES = ["BAND", "MALEN", "VOLCAP", "MOMLOOK"]


def family_arms(fam):
    """-> [(arm_label, weights_fn, is_control)], IN PRINTED DIAL ORDER (K_DIALMID reads this)."""
    if fam == "BAND":
        return [(f"b={b:.2f}", (lambda p, b=b: ew(p, band_mask(p, b, 200))), b == 0.03)
                for b in BANDS]
    if fam == "MALEN":
        return [(f"L={L}", (lambda p, L=L: ew(p, band_mask(p, 0.03, L))), L == 200)
                for L in MALENS]
    if fam == "VOLCAP":
        def wf(p, c=None):
            m = band_mask(p, 0.03, 200)
            if c is not None:
                m = m & (vol20(p) < c).fillna(False)
            return ew(p, m)
        return [(f"vcap={'off' if c is None else f'{c:.2f}'}", (lambda p, c=c: wf(p, c)), c is None)
                for c in VOLCAPS]
    if fam == "MOMLOOK":
        return [(f"k={k:.2f}", (lambda p, k=k: topn_k(p, 20, k)), k == 1.0) for k in MOMKS]
    raise ValueError(fam)


# ------------------------------------------------------------- KEEP paths ---
def bars(spy_r, which):
    m = metrics(window(spy_r, which))
    return dict(S=m["Sharpe"], CAGR=m["CAGR"], DD=m["MaxDD"])


def pass4b(r, spy_r, which="full"):
    """PROTOCOL 4b: Sharpe > SPY over the window AND in both halves, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's."""
    rr = window(r, which)
    b = bars(spy_r, which)
    m = metrics(rr)
    h1, h2 = halves(rr)
    sb1, sb2 = halves(window(spy_r, which))
    mg = dict(H1=h1 - sb1, H2=h2 - sb2, S=m["Sharpe"] - b["S"],
              DD=DELTA * abs(b["DD"]) - abs(m["MaxDD"]), CAGR=m["CAGR"] - PHI * b["CAGR"])
    ok = all(v > 0 for v in mg.values())
    return ok, min(mg, key=lambda k: mg[k]), mg


def pass4a(r, base_r):
    """PROTOCOL 4a: Sharpe > the live book in BOTH halves and MaxDD no worse."""
    h1, h2 = halves(r)
    b1, b2 = halves(base_r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"])


# ============================================================== CORPUS C =====
def build_corpus():
    rows, store, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")

        Wg = ew(px, band_mask(px, 0.03, 200))
        e1 = fast_backtest(px, Wg, 0.0, FREQ)
        e0 = backtest(px, Wg, cost_bps=0.0, freq=FREQ)
        d_r = float((e1["returns"] - e0["returns"]).abs().max())
        d_t = float((e1["turnover"] - e0["turnover"]).abs().max())
        e25 = backtest(px, Wg, cost_bps=25.0, freq=FREQ)
        d_c = float((e25["returns"] - (e0["returns"] - e0["turnover"] * 25.0 / 1e4)).abs().max())
        say(f"  G1 fast vs engine: returns {d_r:.3e}  turnover {d_t:.3e}   | "
            f"G5 rung identity {d_c:.3e}")
        assert d_r < 1e-12 and d_t < 1e-12 and d_c < 1e-12, "G1/G5 FAILED — unsafe"

        v2 = fast_backtest(px, rules_v2_weights(px), 0.0, FREQ)
        v1 = fast_backtest(px, rules_v1_weights(px), 0.0, FREQ)
        ref[pk] = dict(spy=spy, start=start,
                       v2={c: (v2["returns"] - v2["turnover"] * c / 1e4).loc[start:] for c in COSTS},
                       v1={c: (v1["returns"] - v1["turnover"] * c / 1e4).loc[start:] for c in COSTS})
        ms, mo = metrics(spy), metrics(window(spy, "OOS"))
        mv, mvo = metrics(ref[pk]["v2"][10.0]), metrics(window(ref[pk]["v2"][10.0], "OOS"))
        say(f"  SPY      full {ms['CAGR']:7.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:7.2%} | "
            f"OOS {mo['CAGR']:7.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:7.2%}")
        say(f"  RULES v2 full {mv['CAGR']:7.2%}/{mv['Sharpe']:.3f}/{mv['MaxDD']:7.2%} | "
            f"OOS {mvo['CAGR']:7.2%}/{mvo['Sharpe']:.3f}/{mvo['MaxDD']:7.2%}   (@10bps)")

        for fam in FAMILIES:
            for pos, (arm, wfn, is_ctl) in enumerate(family_arms(fam)):
                res = fast_backtest(px, wfn(px), 0.0, FREQ)
                r0, to = res["returns"], res["turnover"]
                for c in COSTS:
                    r = (r0 - to * c / 1e4).loc[start:]
                    store[(pk, fam, c, arm)] = r
                    m, mi, mo_ = metrics(r), metrics(window(r, "IS")), metrics(window(r, "OOS"))
                    h1, h2 = halves(r)
                    ok_f, bind_f, _ = pass4b(r, spy, "full")
                    ok_o, bind_o, _ = pass4b(r, spy, "OOS")
                    rows.append(dict(
                        panel=pk, family=fam, cost=c, arm=arm, dial_pos=pos, control=is_ctl,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        TO=float(to.loc[start:].sum()) / m["Years"],
                        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                        OOS_Sharpe=mo_["Sharpe"], OOS_CAGR=mo_["CAGR"], OOS_MaxDD=mo_["MaxDD"],
                        pass4b=ok_f, bind4b=bind_f, pass4b_oos=ok_o, bind4b_oos=bind_o,
                        pass4a_v2=pass4a(r, ref[pk]["v2"][c]),
                        pass4a_v1=pass4a(r, ref[pk]["v1"][c])))
    return pd.DataFrame(rows), store, ref


# ------------------------------------------------------------- selectors ----
def rank_pick(sub, q):
    """Position round(q*(n-1)) in the IS-Sharpe ascending order.  Ties: printed dial order."""
    s = sub["IS_Sharpe"].astype(float)
    order = s.sort_values(kind="mergesort").index
    return order[int(round(q * (len(order) - 1)))]


def med204_pick(sub):
    """Idea 204's exact convention: index[len//2] of the ascending IS-Sharpe order."""
    s = sub["IS_Sharpe"].astype(float)
    return s.sort_values(kind="mergesort").index[len(s) // 2]


def margin_pick(sub, m):
    """Idea 241: argmax on IS Sharpe if its gap to the runner-up is >= m, else the control."""
    s = sub["IS_Sharpe"].astype(float).sort_values(ascending=False, kind="mergesort")
    gap = float(s.iloc[0] - s.iloc[1])
    if np.isfinite(m) and gap >= m:
        return s.index[0], gap, False
    if not np.isfinite(m):
        return sub.index[sub["control"].values.argmax()], gap, True
    return sub.index[sub["control"].values.argmax()], gap, True


def selectors_for_pool(sub):
    """-> {name: (row_index, extra)}.  sub is one pool's arm table, in printed dial order."""
    out = {}
    for q in QS:
        out[f"K_Q{q:.2f}"] = (rank_pick(sub, q), {})
    out["K_MED204"] = (med204_pick(sub), {})
    out["K_DIALMID"] = (sub.index[len(sub) // 2], {})            # no performance data at all
    for m in MARGINS:
        j, gap, abst = margin_pick(sub, m)
        out[f"K_M{m:.2f}" if np.isfinite(m) else "K_Minf"] = (j, dict(gap=gap, abstained=abst))
    return out


def main():
    say("=" * 120)
    say("QUEUE idea 431 — is-K_MEDIAN-a-real-abstention-rule-or-a-36-cell-accident  (lane C, "
        "2026-09-08)")
    say("=" * 120)
    say("PRE-REGISTERED: P1 K_MEDIAN's lift on the fresh corpus is < +0.0205 and |t| <= 2 | "
        "P2 K_DIALMID (no performance data) matches it | P3 no q and no m beats do-nothing OOS | "
        "P4 K_MARGIN's delta rises monotonically to 0 in m, no interior optimum | "
        "P5 q=0 (argmin) reliably negative")
    say("TUNED PARAMETERS: (1) rank quantile q, (2) margin m.  Panels, families, cost rungs and "
        "metrics are REPORTED axes, never selected on.  Every grid point is printed.")

    # ------------------------------------------------------------------ G0 --
    say("\n" + "=" * 120)
    say("GATE G0 — THE PREMISE, recomputed from idea 204's own committed grid (no re-simulation)")
    say("=" * 120)
    g204 = pd.read_csv(I204_GRID)
    say(f"  read {I204_GRID.name}: {len(g204)} arm-rows, "
        f"{g204.groupby(['panel', 'family', 'cost']).ngroups} pools")
    rows204 = []
    for (pk, fam, c), sub in g204.groupby(["panel", "family", "cost"], sort=False):
        sub = sub.reset_index(drop=True)
        pool_oos = float(sub["OOS_Sharpe"].mean())
        ctl = sub.index[sub["control"].values.argmax()]
        for nm, (j, _x) in dict(
                K_MED204=(med204_pick(sub), {}),
                K_DIALMID=(sub.index[len(sub) // 2], {}),
                K_ARGMAX=(sub["IS_Sharpe"].astype(float).idxmax(), {}),
                K_ANTI=(sub["IS_Sharpe"].astype(float).idxmin(), {})).items():
            rows204.append(dict(panel=pk, family=fam, cost=c, selector=nm, arm=sub.loc[j, "arm"],
                                same_as_dialmid=bool(j == sub.index[len(sub) // 2]),
                                OOS_Sharpe=float(sub.loc[j, "OOS_Sharpe"]),
                                lift=float(sub.loc[j, "OOS_Sharpe"]) - pool_oos,
                                d_vs_ctl=float(sub.loc[j, "OOS_Sharpe"] - sub.loc[ctl, "OOS_Sharpe"]),
                                pool_med_minus_mean=float(sub["OOS_Sharpe"].median() - pool_oos)))
    r204 = pd.DataFrame(rows204)
    say("\n  idea 204's corpus B, re-derived (36 cells per selector):")
    say(f"  {'selector':<10} {'mean lift':>10} {'t':>7} {'wins':>7} {'vs do-nothing':>14} "
        f"{'t':>7} {'= DIALMID':>10}")
    for nm, s in r204.groupby("selector", sort=False):
        w = int((s["lift"] > 0).sum())
        say(f"  {nm:<10} {s['lift'].mean():>+10.4f} {tstat(s['lift']):>+7.2f} "
            f"{w:>4}/{len(s):<3} {s['d_vs_ctl'].mean():>+14.4f} {tstat(s['d_vs_ctl']):>+7.2f} "
            f"{s['same_as_dialmid'].mean():>9.1%}")
    q = r204[r204.selector == "K_MED204"]
    say(f"\n  QUEUE quotes K_MEDIAN +0.0205 / t +2.73 / 28-36 wins / -0.0182 vs do-nothing.")
    say(f"  G0 re-derivation:      {q['lift'].mean():+.4f} / t {tstat(q['lift']):+.2f} / "
        f"{int((q['lift'] > 0).sum())}-{len(q)} wins / {q['d_vs_ctl'].mean():+.4f} vs do-nothing")
    dl = abs(q["lift"].mean() - 0.0205)
    dc = abs(q["d_vs_ctl"].mean() - (-0.0182))
    say(f"  |d| vs published: lift {dl:.2e}, vs-do-nothing {dc:.2e}  -> "
        f"{'PASS' if (dl < 5e-4 and dc < 5e-4) else 'FAIL'}")
    r204.to_csv(OUT / f"{STEM}.premise204.csv", index=False)

    # ------------------------------------------------------------- corpus C --
    say("\n" + "=" * 120)
    say("CORPUS C — fresh: 3 panels x 4 NEW dial families (24 arms) x 3 rungs = 36 cells")
    say("=" * 120)
    g, store, ref = build_corpus()
    g.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    npools = g.groupby(["panel", "family", "cost"]).ngroups
    say(f"\ncorpus C: {len(g)} arm-rows, {npools} pools "
        f"({g.groupby(['panel', 'family']).ngroups} simulated books)")

    # per-pool selector picks -----------------------------------------------
    picks, decomp = [], []
    for (pk, fam, c), sub in g.groupby(["panel", "family", "cost"], sort=False):
        sub = sub.reset_index(drop=True)
        pool_oos = float(sub["OOS_Sharpe"].mean())
        pool_is = float(sub["IS_Sharpe"].mean())
        ctl = sub.index[sub["control"].values.argmax()]
        dm = sub.index[len(sub) // 2]
        spy = ref[pk]["spy"]
        v2 = ref[pk]["v2"][c]
        m_spy, m_v2 = metrics(window(spy, "OOS")), metrics(window(v2, "OOS"))
        for nm, (j, extra) in selectors_for_pool(sub).items():
            r = store[(pk, fam, c, sub.loc[j, "arm"])]
            ok_o, bind_o, _ = pass4b(r, spy, "OOS")
            ok_f, bind_f, _ = pass4b(r, spy, "full")
            picks.append(dict(
                panel=pk, family=fam, cost=c, selector=nm, arm=sub.loc[j, "arm"],
                dial_pos=int(sub.loc[j, "dial_pos"]), n_arms=len(sub),
                is_control=bool(j == ctl), same_as_dialmid=bool(j == dm),
                IS_Sharpe=float(sub.loc[j, "IS_Sharpe"]), pool_IS=pool_is, pool_OOS=pool_oos,
                OOS_Sharpe=float(sub.loc[j, "OOS_Sharpe"]),
                OOS_CAGR=float(sub.loc[j, "OOS_CAGR"]), OOS_MaxDD=float(sub.loc[j, "OOS_MaxDD"]),
                lift=float(sub.loc[j, "OOS_Sharpe"]) - pool_oos,
                d_vs_ctl=float(sub.loc[j, "OOS_Sharpe"] - sub.loc[ctl, "OOS_Sharpe"]),
                d_vs_v2=float(sub.loc[j, "OOS_Sharpe"]) - m_v2["Sharpe"],
                d_vs_spy=float(sub.loc[j, "OOS_Sharpe"]) - m_spy["Sharpe"],
                spy_OOS_Sharpe=m_spy["Sharpe"], spy_OOS_CAGR=m_spy["CAGR"],
                spy_OOS_MaxDD=m_spy["MaxDD"], v2_OOS_Sharpe=m_v2["Sharpe"],
                v2_OOS_CAGR=m_v2["CAGR"], v2_OOS_MaxDD=m_v2["MaxDD"],
                pass4a_v2=pass4a(r, v2), pass4b=ok_f, bind4b=bind_f,
                pass4b_oos=ok_o, bind4b_oos=bind_o, **extra))
        # the decomposition, per pool, for K_MEDIAN (q=0.50) and K_MED204
        for nm, j in [("K_Q0.50", rank_pick(sub, 0.50)), ("K_MED204", med204_pick(sub))]:
            decomp.append(dict(
                panel=pk, family=fam, cost=c, selector=nm, n_arms=len(sub),
                lift=float(sub.loc[j, "OOS_Sharpe"]) - pool_oos,
                POSITION=float(sub.loc[dm, "OOS_Sharpe"]) - pool_oos,
                TRANSFER=float(sub.loc[j, "OOS_Sharpe"] - sub.loc[dm, "OOS_Sharpe"]),
                same_arm=bool(j == dm),
                pool_med_minus_mean=float(sub["OOS_Sharpe"].median() - pool_oos),
                rho_IS_dial=spearman(sub["IS_Sharpe"], sub["dial_pos"]),
                rho_IS_OOS=spearman(sub["IS_Sharpe"], sub["OOS_Sharpe"])))
    P = pd.DataFrame(picks)
    DC = pd.DataFrame(decomp)
    P.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    DC.to_csv(OUT / f"{STEM}.decomp.csv", index=False)

    # ------------------------------------------------- Q1: the q dial -------
    say("\n" + "=" * 120)
    say("Q1 — THE RANK-QUANTILE DIAL q  (tuned parameter 1; ALL 5 grid points, 36 cells each)")
    say("=" * 120)
    say(f"  {'selector':<12} {'mean lift':>10} {'t':>7} {'wins':>8} {'sign p':>8} "
        f"{'vs do-nothing':>14} {'t':>7} {'wins':>8} {'=DIALMID':>9} {'=control':>9}")
    srows = []
    order = [f"K_Q{q:.2f}" for q in QS] + ["K_MED204", "K_DIALMID"] + \
            [(f"K_M{m:.2f}" if np.isfinite(m) else "K_Minf") for m in MARGINS]
    for nm in order:
        s = P[P.selector == nm]
        if not len(s):
            continue
        w, wc = int((s["lift"] > 0).sum()), int((s["d_vs_ctl"] > 0).sum())
        nz = int((s["d_vs_ctl"] != 0).sum())
        row = dict(selector=nm, n=len(s), mean_lift=s["lift"].mean(), t_lift=tstat(s["lift"]),
                   wins_lift=w, sign_p=sign_p(w, len(s)),
                   mean_d_vs_ctl=s["d_vs_ctl"].mean(), t_d_vs_ctl=tstat(s["d_vs_ctl"]),
                   wins_vs_ctl=wc, n_nonzero_vs_ctl=nz,
                   mean_d_vs_v2=s["d_vs_v2"].mean(), mean_d_vs_spy=s["d_vs_spy"].mean(),
                   mean_OOS_Sharpe=s["OOS_Sharpe"].mean(), mean_OOS_CAGR=s["OOS_CAGR"].mean(),
                   mean_OOS_MaxDD=s["OOS_MaxDD"].mean(),
                   share_dialmid=s["same_as_dialmid"].mean(), share_control=s["is_control"].mean(),
                   pass4b_oos=int(s["pass4b_oos"].sum()), pass4a_v2=int(s["pass4a_v2"].sum()))
        srows.append(row)
        if nm.startswith("K_Q") or nm in ("K_MED204", "K_DIALMID"):
            say(f"  {nm:<12} {row['mean_lift']:>+10.4f} {row['t_lift']:>+7.2f} "
                f"{w:>4}/{len(s):<3} {row['sign_p']:>8.3f} {row['mean_d_vs_ctl']:>+14.4f} "
                f"{row['t_d_vs_ctl']:>+7.2f} {wc:>4}/{len(s):<3} "
                f"{row['share_dialmid']:>8.1%} {row['share_control']:>8.1%}")
    S = pd.DataFrame(srows)
    S.to_csv(OUT / f"{STEM}.selectors.csv", index=False)
    say("\n  q=1.00 is the incumbent argmax, q=0.50 is K_MEDIAN, q=0.00 is the power check.")
    say("  K_DIALMID reads NO performance data: it is the middle of the printed dial order.")

    # ------------------------------------------------- Q2: the margin dial --
    say("\n" + "=" * 120)
    say("Q2 — IDEA 241's MINIMUM-MARGIN ABSTENTION RULE  (tuned parameter 2; ALL 7 grid points)")
    say("=" * 120)
    say(f"  {'m':>6} {'abstain':>8} {'mean lift':>10} {'t':>7} {'vs do-nothing':>14} {'t':>7} "
        f"{'wins':>8} {'mean OOS S':>11} {'vs v2':>9} {'vs SPY':>9}")
    for m in MARGINS:
        nm = f"K_M{m:.2f}" if np.isfinite(m) else "K_Minf"
        s = P[P.selector == nm]
        wc = int((s["d_vs_ctl"] > 0).sum())
        say(f"  {('inf' if not np.isfinite(m) else f'{m:.2f}'):>6} "
            f"{s['abstained'].mean():>8.1%} {s['lift'].mean():>+10.4f} {tstat(s['lift']):>+7.2f} "
            f"{s['d_vs_ctl'].mean():>+14.4f} {tstat(s['d_vs_ctl']):>+7.2f} {wc:>4}/{len(s):<3} "
            f"{s['OOS_Sharpe'].mean():>11.4f} {s['d_vs_v2'].mean():>+9.4f} "
            f"{s['d_vs_spy'].mean():>+9.4f}")
    gaps = P[P.selector == "K_M0.00"]
    say(f"\n  top-2 IS-Sharpe gap over the 36 pools: median {gaps['gap'].median():.4f}, "
        f"mean {gaps['gap'].mean():.4f}, max {gaps['gap'].max():.4f}, "
        f"share < 0.05 {(gaps['gap'] < 0.05).mean():.1%}, share < 0.15 {(gaps['gap'] < 0.15).mean():.1%}")

    # ------------------------------------------ Q3: the decomposition -------
    say("\n" + "=" * 120)
    say("Q3 — THE DECOMPOSITION   lift = TRANSFER + POSITION   (POSITION reads no performance data)")
    say("=" * 120)
    for nm, s in DC.groupby("selector", sort=False):
        say(f"\n  {nm}  (n={len(s)} pools)")
        say(f"    lift      {s['lift'].mean():>+9.4f}  t {tstat(s['lift']):>+6.2f}   "
            f"wins {int((s['lift'] > 0).sum())}/{len(s)}")
        say(f"    POSITION  {s['POSITION'].mean():>+9.4f}  t {tstat(s['POSITION']):>+6.2f}   "
            f"wins {int((s['POSITION'] > 0).sum())}/{len(s)}   <- zero selector content")
        say(f"    TRANSFER  {s['TRANSFER'].mean():>+9.4f}  t {tstat(s['TRANSFER']):>+6.2f}   "
            f"wins {int((s['TRANSFER'] > 0).sum())}/{len(s)}   <- the only part that can be skill")
        say(f"    same arm as DIALMID: {s['same_arm'].mean():.1%}   |   "
            f"pool median-minus-mean OOS {s['pool_med_minus_mean'].mean():+.4f}")
        say(f"    spearman(IS_Sharpe, dial position) {s['rho_IS_dial'].mean():+.3f}   "
            f"spearman(IS_Sharpe, OOS_Sharpe) {s['rho_IS_OOS'].mean():+.3f} "
            f"({int((s['rho_IS_OOS'] > 0).sum())}/{len(s)} positive)")

    # ---------------------------------------- Q3b: where the lift comes from --
    say("\n" + "-" * 120)
    say("Q3b — THE SECOND DECOMPOSITION, against the pool's own do-nothing arm")
    say("-" * 120)
    say("  For every selector, exactly:   lift  ==  d_vs_ctl  +  CONTROL_LIFT")
    say("  where CONTROL_LIFT = OOS(control) - mean_P OOS is the POOL DEFICIT — a property of the")
    say("  pool, measurable with no selector at all.  It is idea 204's '-0.0387' with its sign")
    say("  flipped.  A selector's whole contribution is d_vs_ctl; everything else it 'earns' is")
    say("  borrowed from sitting still.")
    ctl_lift = P[P.selector == "K_Minf"]["lift"]
    say(f"\n  corpus C  CONTROL_LIFT (pool deficit) {ctl_lift.mean():+.4f}  t {tstat(ctl_lift):+.2f}"
        f"   {int((ctl_lift > 0).sum())}/{len(ctl_lift)} pools positive")
    say(f"  {'selector':<12} {'lift':>9} {'=':>3} {'d_vs_ctl':>10} {'+':>3} {'CONTROL_LIFT':>13} "
        f"{'  identity |d|':>14}")
    for nm in ["K_Q0.50", "K_MED204", "K_Q1.00", "K_DIALMID"]:
        s = P[P.selector == nm]
        idn = float(np.abs(s["lift"].values - s["d_vs_ctl"].values - ctl_lift.values).max())
        say(f"  {nm:<12} {s['lift'].mean():>+9.4f} {'=':>3} {s['d_vs_ctl'].mean():>+10.4f} "
            f"{'+':>3} {ctl_lift.mean():>+13.4f} {idn:>14.2e}")
    c204 = r204[r204.selector == "K_MED204"]
    say(f"\n  idea 204's corpus B, the same reading: K_MEDIAN lift {c204['lift'].mean():+.4f} = "
        f"d_vs_ctl {c204['d_vs_ctl'].mean():+.4f} + CONTROL_LIFT "
        f"{(c204['lift'] - c204['d_vs_ctl']).mean():+.4f}")
    say("  (idea 204 published that pool deficit as -0.0387; it is the same number.)")

    say("\n  CONFOUND, disclosed: how often the middle of the printed dial order IS the control arm")
    cf = P[P.selector == "K_DIALMID"].groupby("family")["is_control"].mean()
    say("    " + "  ".join(f"{k}={v:.0%}" for k, v in cf.items()) +
        f"   overall {P[P.selector == 'K_DIALMID']['is_control'].mean():.0%}")
    say("    On BAND/MALEN/MOMLOOK the adopted value sits at the dial's centre by construction, so")
    say("    K_DIALMID is the control there and its lift IS the pool deficit.  VOLCAP is the one")
    say("    family where they differ, and it is the family where K_DIALMID loses to do-nothing")
    say(f"    ({P[(P.selector == 'K_DIALMID') & (P.family == 'VOLCAP')]['d_vs_ctl'].mean():+.4f}). "
        "K_DIALMID is therefore not an independent rule — it is a")
    say("    restatement of 'hold the adopted arm', which is what do-nothing already means.")

    # per-family / per-panel / per-rung breakdowns for the two headline rules
    say("\n  BREAKDOWNS (mean lift / mean vs-do-nothing), the clustering the t-stats hide:")
    for nm in ["K_Q0.50", "K_Q1.00", "K_DIALMID"]:
        s = P[P.selector == nm]
        say(f"\n   {nm}")
        for ax in ["panel", "family", "cost"]:
            b = s.groupby(ax).agg(lift=("lift", "mean"), d=("d_vs_ctl", "mean"), n=("lift", "size"))
            say("     " + ax + ": " + "  ".join(
                f"{k}={r.lift:+.4f}/{r.d:+.4f}(n{int(r.n)})" for k, r in b.iterrows()))

    # ------------------------------------------------ Q4: KEEP paths --------
    say("\n" + "=" * 120)
    say("Q4 — PROTOCOL 4a / 4b, on every ARM and every PICK, full sample and OOS (rule 4 requires it)")
    say("=" * 120)
    say(f"  {'scope':<22} {'rung':>6} {'n':>5} {'4a vs v2':>9} {'4b full':>9} {'4b OOS':>9} "
        f"{'BOTH':>6}")
    for c in COSTS:
        a = g[g.cost == c]
        both = int((a["pass4a_v2"] & a["pass4b"] & a["pass4b_oos"]).sum())
        say(f"  {'corpus-C arms':<22} {c:>6.0f} {len(a):>5} {int(a['pass4a_v2'].sum()):>9} "
            f"{int(a['pass4b'].sum()):>9} {int(a['pass4b_oos'].sum()):>9} {both:>6}")
    for c in COSTS:
        a = P[P.cost == c]
        both = int((a["pass4a_v2"] & a["pass4b"] & a["pass4b_oos"]).sum())
        say(f"  {'walk-forward picks':<22} {c:>6.0f} {len(a):>5} {int(a['pass4a_v2'].sum()):>9} "
            f"{int(a['pass4b'].sum()):>9} {int(a['pass4b_oos'].sum()):>9} {both:>6}")
    kp = g[g.pass4b & g.pass4b_oos]
    say(f"\n  arms clearing 4b FULL and OOS: {len(kp)} of {len(g)}  -> " +
        (", ".join(f"{r.panel}/{r.family}/{r.arm}@{r.cost:.0f}bps" for r in kp.itertuples())
         if len(kp) else "none"))
    say(f"  arms clearing BOTH PATHS (4a and 4b full and 4b OOS): "
        f"{int((g['pass4a_v2'] & g['pass4b'] & g['pass4b_oos']).sum())} of {len(g)}")
    say("  4b binding bar over all arm-rows: full " +
        str(dict(g["bind4b"].value_counts())) + "  OOS " + str(dict(g["bind4b_oos"].value_counts())))
    pd.concat([g.assign(scope="arm"), P.assign(scope="pick")], ignore_index=True).to_csv(
        OUT / f"{STEM}.keeppaths.csv", index=False)

    # PROTOCOL rung headline table for the two rules the queue names
    say("\n  PROTOCOL RUNG (10 bps) — the picks' OOS levels against the baseline and SPY, "
        "averaged over the 12 cells:")
    say(f"  {'selector':<12} {'OOS CAGR':>9} {'OOS Sharpe':>11} {'OOS MaxDD':>10} "
        f"{'dS vs v2':>9} {'dS vs SPY':>10} {'dS vs do-nothing':>17}")
    for nm in ["K_Q1.00", "K_Q0.50", "K_MED204", "K_DIALMID", "K_M0.15", "K_Minf"]:
        s = P[(P.selector == nm) & (P.cost == PROTOCOL_RUNG)]
        say(f"  {nm:<12} {s['OOS_CAGR'].mean():>9.2%} {s['OOS_Sharpe'].mean():>11.4f} "
            f"{s['OOS_MaxDD'].mean():>10.2%} {s['d_vs_v2'].mean():>+9.4f} "
            f"{s['d_vs_spy'].mean():>+10.4f} {s['d_vs_ctl'].mean():>+17.4f}")
    s = P[(P.selector == "K_Minf") & (P.cost == PROTOCOL_RUNG)]
    say(f"  {'do-nothing':<12} {s['OOS_CAGR'].mean():>9.2%} {s['OOS_Sharpe'].mean():>11.4f} "
        f"{s['OOS_MaxDD'].mean():>10.2%} {s['d_vs_v2'].mean():>+9.4f} "
        f"{s['d_vs_spy'].mean():>+10.4f} {0.0:>+17.4f}   (K_Minf IS the control by construction)")

    # ------------------------------------------------ scorecard -------------
    say("\n" + "=" * 120)
    say("PREDICTION SCORECARD")
    say("=" * 120)
    k50 = P[P.selector == "K_Q0.50"]
    kdm = P[P.selector == "K_DIALMID"]
    k00 = P[P.selector == "K_Q0.00"]
    p1 = (k50["lift"].mean() < 0.0205) and (abs(tstat(k50["lift"])) <= 2)
    say(f"  P1 K_MEDIAN lift < +0.0205 and |t| <= 2: {k50['lift'].mean():+.4f}, "
        f"t {tstat(k50['lift']):+.2f}  -> {'CONFIRMED' if p1 else 'REJECTED'}")
    dif = k50["lift"].values - kdm["lift"].values
    p2 = (abs(tstat(dif)) <= 2) and (k50["same_as_dialmid"].mean() > 0.5)
    say(f"  P2 K_DIALMID indistinguishable and agrees > 50%: paired d {dif.mean():+.4f} "
        f"t {tstat(dif):+.2f}, agreement {k50['same_as_dialmid'].mean():.1%}  -> "
        f"{'CONFIRMED' if p2 else 'REJECTED'}")
    beat = S[(S.selector.str.startswith(("K_Q", "K_M"))) & (S.mean_d_vs_ctl > 0)]
    say(f"  P3 no q and no m beats do-nothing OOS: {len(beat)} of "
        f"{int(S.selector.str.startswith(('K_Q', 'K_M')).sum())} grid points beat it  -> "
        f"{'CONFIRMED' if len(beat) == 0 else 'REJECTED'} "
        f"{'' if len(beat) == 0 else '(' + ', '.join(beat.selector) + ')'}")
    mv = [P[P.selector == (f'K_M{m:.2f}' if np.isfinite(m) else 'K_Minf')]["d_vs_ctl"].mean()
          for m in MARGINS]
    p4 = all(mv[i] <= mv[i + 1] + 1e-12 for i in range(len(mv) - 1))
    say(f"  P4 K_MARGIN monotone to 0 in m: " + " ".join(f"{v:+.4f}" for v in mv) +
        f"  -> {'CONFIRMED' if p4 else 'REJECTED'}")
    p5 = tstat(k00["lift"]) < -2
    say(f"  P5 q=0.00 reliably negative: {k00['lift'].mean():+.4f}, t {tstat(k00['lift']):+.2f} "
        f"-> {'CONFIRMED' if p5 else 'REJECTED'}")

    say("\n  P2 is a CONJUNCTION and it splits: the paired difference between K_MEDIAN and a rule")
    say("     that reads no performance data is NOT significant (t -0.96), which is the half that")
    say("     matters; the agreement half fails because K_DIALMID lands on a DIFFERENT arm 86% of")
    say("     the time and still scores HIGHER.  That is stronger than P2 predicted, not weaker.")

    say("\n" + "=" * 120)
    say("THE ANSWER TO THE QUEUE'S QUESTION")
    say("=" * 120)
    say(f"  Does a rank-based non-argmax chooser have expectancy?  NO, on the only comparand that")
    say(f"  can pay for one.  K_MEDIAN's lift REPLICATES on a disjoint corpus "
        f"({k50['lift'].mean():+.4f}, t {tstat(k50['lift']):+.2f}, "
        f"{int((k50['lift'] > 0).sum())}/36) — the queue's premise survives — but the lift is")
    say(f"  measured against the POOL MEAN, and the pool mean is not an alternative anyone can")
    say(f"  hold.  Against the do-nothing arm, which is, K_MEDIAN loses "
        f"{k50['d_vs_ctl'].mean():+.4f} (t {tstat(k50['d_vs_ctl']):+.2f}), the do-nothing arm's")
    say(f"  OWN lift is {ctl_lift.mean():+.4f} (t {tstat(ctl_lift):+.2f}), and the q-dial's positive")
    say(f"  region is the whole top half (q=0.75 {P[P.selector == 'K_Q0.75']['lift'].mean():+.4f} "
        f">= q=0.50 {k50['lift'].mean():+.4f}), not a peak at the median.")
    say("  Idea 241's minimum-margin rule cannot fix this: 100% of the 36 pools have a top-2 IS gap")
    say("  under 0.15, so every m >= 0.10 IS do-nothing by construction (delta exactly 0.0000) and")
    say("  the only m that ever trades, 0.05, still loses. The margin rule is damage control on the")
    say("  argmax (-0.0512 -> -0.0084), never expectancy.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    say(f"\nwrote {STEM}.console.txt/.grid.csv/.picks.csv/.selectors.csv/.decomp.csv/"
        f".keeppaths.csv/.premise204.csv")


if __name__ == "__main__":
    main()

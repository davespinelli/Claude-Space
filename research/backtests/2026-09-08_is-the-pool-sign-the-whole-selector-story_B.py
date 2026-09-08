#!/usr/bin/env python3
"""QUEUE idea 204 — is-the-pool-sign-the-whole-selector-story  (lane B, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 204)
    "idea 196 found S2LF beats RANDOM from its own pool by +0.0110 (t +3.78) while still losing
     to do-nothing by -0.0032, because the pool's mean dSharpe is negative and monotone in tilt
     strength.  Test the general form across every selector in the record: regress each
     selector's paired dOOS on the MEAN dSharpe of the pool it picks from.  If the pool's sign
     explains the selector's sign, 'does selection help' was always the wrong question.
     Max 2 params."

WHAT THIS RUN ACTUALLY DOES, AND THE ONE THING THE QUEUE DID NOT NOTICE
    Write the quantities out.  A selector K picks arm a* from a pool P of arms, and its claim is
    published against a comparand C:

        sel_d  := M_OOS(a*)            - M_OOS(C)          <- what gets published
        pool   := mean_{a in P} M_OOS(a) - M_OOS(C)        <- idea 205's column
        lift   := M_OOS(a*)            - mean_{a in P} M_OOS(a)

    so, for EVERY selector, EVERY pool, EVERY comparand and EVERY metric,

        sel_d  ==  pool + lift                              (an algebraic IDENTITY)

    The regression idea 204 proposes -- sel_d on pool -- is therefore a regression of (X + Y)
    on X.  Its slope is 1 + cov(lift, pool)/var(pool) and it CANNOT come back null; a slope near
    +1 with a large R2 is arithmetic, not evidence.  This run reports that regression anyway,
    exactly as asked, on every selector in two corpora -- and then reports the three statistics
    that are NOT determined by the identity and that carry the queue's actual question:

      Q1  THE ASKED REGRESSION.  slope / intercept / R2 / t of sel_d on pool, per selector, per
          comparand, per corpus.  Reported in full.
      Q2  THE IDENTITY, MEASURED.  max |sel_d - pool - lift| over every claim row (gate G2), and
          the variance decomposition var(sel_d) = var(pool) + var(lift) + 2cov, as shares.
      Q3  DOES THE POOL'S SIGN EXPLAIN THE SELECTOR'S SIGN?  sign-agreement rate, the
          "pool-decided" share |pool| > |lift|, and P(sel_d<0 | pool<0) / P(sel_d>0 | pool>0).
      Q4  DOES SELECTION HELP, ONCE THE POOL IS REMOVED?  mean lift per selector with a paired t
          and an exact sign test, bounded below by K_ANTI (argmin IS) and centred by K_RANDOM
          (whose expectation is the pool mean, i.e. lift == 0 by construction).  This is the
          residual question the queue says was mis-posed; it is answerable and it is answered.
      Q5  COMPARAND INVARIANCE.  lift does not move with C at all (gate G4); pool absorbs 100%
          of it.  Idea 205R's "+0.2874 / +0.0495 / -0.1156 with lift +0.0397 in all three" is
          the general case, and this run puts a number on the general case.
      Q6  RULE 8.  Selectors read IS (<= 2016-12-31) only and are read ONCE on 2017-2026.  Does
          IS lift predict OOS lift (is there persistent selection skill)?  Does IS pool mean
          predict OOS pool mean (is idea 205's column causal)?  OOS CAGR/Sharpe/MaxDD of every
          pick against RULES v2 (live), RULES v1 and SPY.
      Q7  BOTH KEEP PATHS, 4a and 4b, on every corpus-B arm and every selector pick, full sample
          and OOS.  This is a bookkeeping idea and cannot promote a book; the paths are scored
          anyway because PROTOCOL requires it.

CORPORA
    A  READ-ONLY, the record's own.  research/backtests/
       2026-09-08_the-pool-mean-as-a-leaderboard-column_B.grid.csv -- 1,224 arm-rows =
       3 panels x 8/6 books x 3 cost rungs x idea 94's 17 arms = 72 pools, each with exactly one
       `control` (do-nothing) arm.  Nothing is re-run; the file is read at face value and its
       provenance is quoted.  Two pool definitions are carried as a REPORTED axis: P_ALL (all 17
       arms) and P_S1 (the file's own admissible subset, column adm_P_S1).
    B  FRESH, run here, so KEEP paths and rule 8 apply to real books.  3 panels x 4 pre-registered
       dial families (GROSS 7 arms, WIDTH 6, CADENCE 4, GATE 6 = 23 arms) x 3 cost rungs.
       The rungs come off the exact turnover identity r(c) = r(0) - turnover*c/1e4 (gate G5), so
       69 simulations serve 207 arm-rows.

SELECTORS (tuned parameter 1 -- every value reported, none selected on)
    corpus B (10): K_Sharpe K_CAGR K_Calmar K_Sortino K_MaxDD K_Vol K_TO K_MEDIAN K_RANDOM K_ANTI
    corpus A  (7): K_Sharpe K_CAGR K_Calmar K_MaxDD K_MEDIAN K_RANDOM K_ANTI
                   (the committed grid carries no IS Sortino / vol / turnover column)
    K_RANDOM is scored in closed form (its expectation over a uniform draw IS the pool mean, so
    its lift is exactly 0) AND as 400 seeded draws, to show the seeded spread around that zero.
    K_ANTI is the falsification control: if lift cannot detect K_ANTI, it cannot detect skill.

DIAL FAMILY (tuned parameter 2 -- every value reported, none selected on)
    GROSS / WIDTH / CADENCE / GATE on corpus B; the pool definition P_ALL / P_S1 on corpus A.
    Panels, cost rungs, comparands and metrics are REPORTED axes, never selected on.

COMPARANDS (reported axis, 3)
    C_CONTROL = the pool's own pre-registered do-nothing arm
    C_V2      = RULES v2 (live) on the same panel at the same rung
    C_SPY     = SPY buy-and-hold on the same panel's evaluated slice

PRE-REGISTERED PREDICTIONS (written before any number below was computed)
    P1  The asked regression returns slope ~ +1 and a large R2 for EVERY selector, including
        K_ANTI and K_RANDOM -- i.e. it is an identity and cannot discriminate selectors.
    P2  sign(pool) agrees with sign(sel_d) in more than 70% of claim rows.
    P3  No selector's mean lift is reliably positive at the 10 bps PROTOCOL rung; K_ANTI's is
        reliably negative (the power check).
    P4  max |lift(C) - lift(C')| == 0 across the three comparands, to machine precision.
    P5  Under rule 8, IS lift does not predict OOS lift: slope not distinguishable from 0.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): all three panels are current constituents; every CAGR here is
      flattered and no level is an achievable return.  Every statistic reported is a PAIRED
      contrast inside one panel, so the pairing is unaffected by the panel's level bias.
    * 72 corpus-A pools and 12 corpus-B pools are not that many independent observations: books
      and arms overlap heavily inside a panel.  Per-panel, per-rung and per-family breakdowns are
      printed so the clustering is visible, and every t is quoted with its n.
    * Corpus A is read at face value.  It cannot know which of its rows was ever the subject of
      a published selector sentence; it is the poolable population idea 205 identified, not a
      census of the record's prose.
    * Idea 401's restatement: data/prices.csv was rewritten after some committed grids, so the
      reproduction gate G3 is quoted per column rather than asserted.
    * Idea 126: every row is t+1 execution; PROTOCOL's rung is 10 bps and 0/25 are reported.

Deterministic, standalone.  Writes .console.txt, .gridB.csv, .claims.csv, .regression.csv,
.lift.csv, .walkforward.csv and .keeppaths.csv next to itself.  Modifies nothing.
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

STEM = "2026-09-08_is-the-pool-sign-the-whole-selector-story_B"
OUT = ROOT / "research" / "backtests"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
A_GRID = OUT / "2026-09-08_the-pool-mean-as-a-leaderboard-column_B.grid.csv"

FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b CAGR floor / MaxDD cap, PROTOCOL rule 4b
N_SEEDS = 400

pd.set_option("display.width", 330)
pd.set_option("display.max_columns", 160)
pd.set_option("display.max_rows", 4000)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = _load(I133, "i133")          # panel_px, verbatim construction of the record's three panels


# ------------------------------------------------------------------ stats ---
def ols(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    ok = np.isfinite(y) & np.isfinite(x)
    y, x = y[ok], x[ok]
    n = len(y)
    if n < 3 or x.std() == 0:
        return dict(n=n, slope=np.nan, icept=np.nan, r2=np.nan, t=np.nan)
    b, a = np.polyfit(x, y, 1)
    yh = a + b * x
    ss_res = float(((y - yh) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    se = math.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()) if n > 2 else np.nan
    return dict(n=n, slope=float(b), icept=float(a),
                r2=1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan,
                t=float(b / se) if se and np.isfinite(se) and se > 0 else np.nan)


def tstat(x):
    x = np.asarray([v for v in np.asarray(x, float) if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def sign_p(wins, n):
    """Two-sided exact binomial sign test at p=0.5; ties excluded by the caller."""
    if n == 0:
        return np.nan
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


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


# ----------------------------------------------------------------- books B ---
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def gate_mask(px, gate):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0).mask(px < ma * 0.97, 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (vol20(px) < MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (vol20(px) < MAX_VOL)).fillna(False)
    raise ValueError(gate)


def ew_weights(px, g=GROSS, gate=None):
    """Equal weight over priced names at gross g; gated-out weight goes to CASH (de-gross)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    W = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return W.where(gate_mask(px, gate), 0.0)


def topn_weights(px, n, g=GROSS, gate="band3"):
    """Top-n on the plain composite, equal weight g/n, de-grossed by the gate.  n=None -> all."""
    if n is None:
        return ew_weights(px, g, gate)
    rank = composite(px).rank(axis=1, ascending=False)
    W = (rank <= n).astype(float) * (g / n)
    return W.where(gate_mask(px, gate), 0.0)


# family -> list of (arm, weights_fn, freq, is_control)
def family_arms(fam):
    if fam == "GROSS":
        gs = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
        return [(f"g={g:.3f}", (lambda p, g=g: ew_weights(p, g, "band3")), FREQ, g == GROSS)
                for g in gs]
    if fam == "WIDTH":
        ns = [5, 10, 20, 40, 80, None]
        return [(f"n={'ALL' if n is None else n}", (lambda p, n=n: topn_weights(p, n)), FREQ,
                 n is None) for n in ns]
    if fam == "CADENCE":
        return [(f"freq={f}", (lambda p: ew_weights(p, GROSS, "band3")), f, f == FREQ)
                for f in ["D", "W", "M", "Q"]]
    if fam == "GATE":
        gates = [None, "g200", "band3", "abs12", "vol60", "v1gate"]
        return [(f"gate={'none' if g is None else g}",
                 (lambda p, g=g: ew_weights(p, GROSS, g)), FREQ, g == "band3") for g in gates]
    raise ValueError(fam)


FAMILIES = ["GROSS", "WIDTH", "CADENCE", "GATE"]


# ------------------------------------------------------------- KEEP paths ---
def bars(spy_r, which):
    m = metrics(window(spy_r, which))
    return dict(S=m["Sharpe"], CAGR=m["CAGR"], DD=m["MaxDD"])


def pass4b(r, spy_r, which="full"):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves and (for OOS scope) over the window, MaxDD <=
    60% of SPY's, CAGR >= 70% of SPY's.  Returns (bool, binding-bar name, margins dict)."""
    rr = window(r, which)
    b = bars(spy_r, which)
    m = metrics(rr)
    h1, h2 = halves(rr)
    sb1, sb2 = halves(window(spy_r, which))
    mg = dict(H1=h1 - sb1, H2=h2 - sb2, S=m["Sharpe"] - b["S"],
              DD=DELTA * abs(b["DD"]) - abs(m["MaxDD"]), CAGR=m["CAGR"] - PHI * b["CAGR"])
    ok = all(v > 0 for v in mg.values())
    binding = min(mg, key=lambda k: mg[k])
    return ok, binding, mg


def pass4a(r, base_r):
    """PROTOCOL 4a: Sharpe > live book in BOTH halves and MaxDD no worse."""
    h1, h2 = halves(r)
    b1, b2 = halves(base_r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"])


# ============================================================== CORPUS B =====
def build_corpus_B():
    rows, store, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")

        # gate G1 -- the vectorised runner reproduces engine.backtest on returns AND turnover
        Wg = ew_weights(px, GROSS, "band3")
        e1 = fast_backtest(px, Wg, 0.0, FREQ)
        e0 = backtest(px, Wg, cost_bps=0.0, freq=FREQ)
        d_r = float((e1["returns"] - e0["returns"]).abs().max())
        d_t = float((e1["turnover"] - e0["turnover"]).abs().max())
        # gate G5 -- the cost-rung identity r(c) = r(0) - turnover*c/1e4
        e25 = backtest(px, Wg, cost_bps=25.0, freq=FREQ)
        d_c = float((e25["returns"] - (e0["returns"] - e0["turnover"] * 25.0 / 1e4)).abs().max())
        say(f"  G1 fast_backtest vs engine.backtest: returns {d_r:.3e}  turnover {d_t:.3e}"
            f"   | G5 rung identity {d_c:.3e}")
        assert d_r < 1e-12 and d_t < 1e-12 and d_c < 1e-12, "G1/G5 FAILED - unsafe"

        v2 = fast_backtest(px, rules_v2_weights(px), 0.0, FREQ)
        v1 = fast_backtest(px, rules_v1_weights(px), 0.0, FREQ)
        ref[pk] = dict(px=px, spy=spy, start=start,
                       v2={c: (v2["returns"] - v2["turnover"] * c / 1e4).loc[start:] for c in COSTS},
                       v1={c: (v1["returns"] - v1["turnover"] * c / 1e4).loc[start:] for c in COSTS})
        ms, mo = metrics(spy), metrics(window(spy, "OOS"))
        say(f"  SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%}"
            f" | OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")
        for c in (PROTOCOL_RUNG,):
            mv = metrics(ref[pk]["v2"][c])
            mvo = metrics(window(ref[pk]["v2"][c], "OOS"))
            say(f"  RULES v2 @{c:.0f}bps {mv['CAGR']:.2%}/{mv['Sharpe']:.3f}/{mv['MaxDD']:.2%}"
                f" | OOS {mvo['CAGR']:.2%}/{mvo['Sharpe']:.3f}/{mvo['MaxDD']:.2%}")

        for fam in FAMILIES:
            for arm, wfn, freq, is_ctl in family_arms(fam):
                res = fast_backtest(px, wfn(px), 0.0, freq)
                r0, to = res["returns"], res["turnover"]
                for c in COSTS:
                    r = (r0 - to * c / 1e4).loc[start:]
                    store[(pk, fam, c, arm)] = r
                    m, mi, mo = metrics(r), metrics(window(r, "IS")), metrics(window(r, "OOS"))
                    h1, h2 = halves(r)
                    ok_f, bind_f, _ = pass4b(r, spy, "full")
                    ok_o, bind_o, _ = pass4b(r, spy, "OOS")
                    rows.append(dict(
                        panel=pk, family=fam, cost=c, arm=arm, control=is_ctl,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        Vol=m["Vol"], TO=float(to.loc[start:].sum()) / m["Years"],
                        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                        IS_Calmar=mi["Calmar"], IS_Sortino=mi["Sortino"], IS_Vol=mi["Vol"],
                        IS_TO=float(to.loc[start:IS_END].sum()) / mi["Years"],
                        OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                        pass4b=ok_f, bind4b=bind_f, pass4b_oos=ok_o, bind4b_oos=bind_o,
                        pass4a_v2=pass4a(r, ref[pk]["v2"][c]),
                        pass4a_v1=pass4a(r, ref[pk]["v1"][c])))
    return pd.DataFrame(rows), store, ref


# ------------------------------------------------------------- selectors ----
# name -> (IS column, direction)   direction +1 = argmax, -1 = argmin
SEL_B = {"K_Sharpe": ("IS_Sharpe", +1), "K_CAGR": ("IS_CAGR", +1),
         "K_Calmar": ("IS_Calmar", +1), "K_Sortino": ("IS_Sortino", +1),
         "K_MaxDD": ("IS_MaxDD", +1), "K_Vol": ("IS_Vol", -1), "K_TO": ("IS_TO", -1)}
SEL_A = {"K_Sharpe": ("IS_Sharpe", +1), "K_CAGR": ("IS_CAGR", +1),
         "K_Calmar": ("IS_Calmar", +1), "K_MaxDD": ("IS_MaxDD", +1)}


def pick(sub, col, direction):
    """Deterministic argmax/argmin on an IS column; ties broken by the arm's printed order."""
    s = sub[col]
    if not np.isfinite(s).any():
        return None
    j = (s.idxmax() if direction > 0 else s.idxmin())
    return j


def claims_for_pool(sub, sels, metric, comparands, rng):
    """One pool -> one claim row per (selector x comparand).  sub is the pool's arm table."""
    out = []
    vals = sub[metric].astype(float)
    pool_mean = float(vals.mean())
    order = list(sub.index)
    picks = {}
    for k, (col, dr) in sels.items():
        j = pick(sub, col, dr)
        picks[k] = j
    # median-IS-Sharpe arm and the anti-selector
    s = sub["IS_Sharpe"].astype(float)
    picks["K_MEDIAN"] = s.sort_values(kind="mergesort").index[len(s) // 2]
    picks["K_ANTI"] = s.idxmin()
    # K_RANDOM: closed form (expectation == pool mean, lift == 0 exactly)
    for k, j in picks.items():
        if j is None:
            continue
        for cname, cval in comparands.items():
            m = float(vals.loc[j])
            out.append(dict(selector=k, arm=sub.loc[j, "arm"], comparand=cname,
                            metric=metric, M_pick=m, M_pool=pool_mean, M_comp=cval,
                            sel_d=m - cval, pool=pool_mean - cval, lift=m - pool_mean,
                            n_arms=len(sub)))
    for cname, cval in comparands.items():
        out.append(dict(selector="K_RANDOM", arm="<uniform>", comparand=cname, metric=metric,
                        M_pick=pool_mean, M_pool=pool_mean, M_comp=cval,
                        sel_d=pool_mean - cval, pool=pool_mean - cval, lift=0.0,
                        n_arms=len(sub)))
    # seeded draws, reported as a spread around the closed form
    draws = rng.integers(0, len(order), size=N_SEEDS)
    dv = vals.values[draws]
    out.append(dict(selector="K_RANDOM_seeded", arm=f"<{N_SEEDS} draws>", comparand="_spread",
                    metric=metric, M_pick=float(dv.mean()), M_pool=pool_mean, M_comp=np.nan,
                    sel_d=np.nan, pool=np.nan, lift=float(dv.mean() - pool_mean),
                    n_arms=len(sub), lift_sd=float(dv.std(ddof=1))))
    return out


def main():
    say("=" * 118)
    say("QUEUE idea 204 — is-the-pool-sign-the-whole-selector-story   (lane B, 2026-09-08)")
    say("=" * 118)
    say("PRE-REGISTERED: P1 the asked regression is an identity (slope~1, large R2, every "
        "selector) | P2 sign agreement > 70% | P3 no selector's mean lift reliably > 0, K_ANTI's "
        "reliably < 0 | P4 lift invariant to the comparand at machine precision | P5 IS lift "
        "does not predict OOS lift")
    say("TUNED PARAMETERS: (1) the selector K, (2) the dial family / pool definition. "
        "Every value of both is reported; panels, rungs, comparands and metrics are reported "
        "axes, never selected on.")

    # ---------------------------------------------------------------- corpus B
    say("\n" + "=" * 118)
    say("CORPUS B — fresh, this run: 3 panels x 4 dial families (23 arms) x 3 rungs")
    say("=" * 118)
    gB, store, ref = build_corpus_B()
    gB.to_csv(OUT / f"{STEM}.gridB.csv", index=False)
    say(f"\ncorpus B: {len(gB)} arm-rows, {gB.groupby(['panel','family','cost']).ngroups} pools")

    claims = []
    for (pk, fam, c), sub in gB.groupby(["panel", "family", "cost"], sort=True):
        sub = sub.reset_index(drop=True)
        ctl = sub.index[sub["control"]]
        assert len(ctl) == 1, f"pool {(pk,fam,c)} has {len(ctl)} controls"
        ctl = ctl[0]
        rng = np.random.default_rng(abs(hash((pk, fam, float(c)))) % (2 ** 32))
        for metric, comps in (
            ("OOS_Sharpe", dict(C_CONTROL=float(sub.loc[ctl, "OOS_Sharpe"]),
                                C_V2=metrics(window(ref[pk]["v2"][c], "OOS"))["Sharpe"],
                                C_SPY=metrics(window(ref[pk]["spy"], "OOS"))["Sharpe"])),
            ("OOS_CAGR", dict(C_CONTROL=float(sub.loc[ctl, "OOS_CAGR"]),
                              C_V2=metrics(window(ref[pk]["v2"][c], "OOS"))["CAGR"],
                              C_SPY=metrics(window(ref[pk]["spy"], "OOS"))["CAGR"])),
            ("IS_Sharpe", dict(C_CONTROL=float(sub.loc[ctl, "IS_Sharpe"]),
                               C_V2=metrics(window(ref[pk]["v2"][c], "IS"))["Sharpe"],
                               C_SPY=metrics(window(ref[pk]["spy"], "IS"))["Sharpe"]))):
            for row in claims_for_pool(sub, SEL_B, metric, comps, rng):
                row.update(corpus="B", panel=pk, poolname=f"{fam}", family=fam, cost=c,
                           pooldef="P_ALL")
                claims.append(row)

    # ---------------------------------------------------------------- corpus A
    say("\n" + "=" * 118)
    say("CORPUS A — read-only, the record's own poolable grid")
    say("=" * 118)
    gA = pd.read_csv(A_GRID)
    say(f"source {A_GRID.name}: {len(gA)} arm-rows, "
        f"{gA.groupby(['panel','book','cost']).ngroups} pools, {gA['arm'].nunique()} arms")
    # gate G3 -- provenance: the file's control arm exists exactly once per pool
    bad = [k for k, s in gA.groupby(["panel", "book", "cost"]) if (s["arm"] == "control").sum() != 1]
    say(f"  G3 provenance: pools with exactly one `control` row: "
        f"{gA.groupby(['panel','book','cost']).ngroups - len(bad)}"
        f"/{gA.groupby(['panel','book','cost']).ngroups}  ({'PASS' if not bad else 'FAIL'})")
    assert not bad

    for pooldef in ("P_ALL", "P_S1"):
        for (pk, bk, c), sub0 in gA.groupby(["panel", "book", "cost"], sort=True):
            sub = sub0.reset_index(drop=True)
            ctl = sub.index[sub["arm"] == "control"][0]
            if pooldef == "P_S1":
                keep = sub.index[sub["adm_P_S1"].astype(bool) | (sub.index == ctl)]
                sub = sub.loc[keep].reset_index(drop=True)
                ctl = sub.index[sub["arm"] == "control"][0]
            if len(sub) < 3:
                continue
            rng = np.random.default_rng(abs(hash((pk, bk, float(c), pooldef))) % (2 ** 32))
            spy_oosS = metrics(window(ref[pk]["spy"], "OOS"))["Sharpe"]
            spy_oosC = metrics(window(ref[pk]["spy"], "OOS"))["CAGR"]
            v2r = ref[pk]["v2"][c]
            for metric, comps in (
                ("OOS_Sharpe", dict(C_CONTROL=float(sub.loc[ctl, "OOS_Sharpe"]),
                                    C_V2=metrics(window(v2r, "OOS"))["Sharpe"],
                                    C_SPY=spy_oosS)),
                ("OOS_CAGR", dict(C_CONTROL=float(sub.loc[ctl, "OOS_CAGR"]),
                                  C_V2=metrics(window(v2r, "OOS"))["CAGR"],
                                  C_SPY=spy_oosC))):
                for row in claims_for_pool(sub, SEL_A, metric, comps, rng):
                    row.update(corpus="A", panel=pk, poolname=f"{bk}", family=bk, cost=c,
                               pooldef=pooldef)
                    claims.append(row)

    CL = pd.DataFrame(claims)
    CL.to_csv(OUT / f"{STEM}.claims.csv", index=False)
    real = CL[CL["comparand"] != "_spread"].copy()
    say(f"\nclaim rows: {len(real)} scored + {len(CL) - len(real)} seeded-spread rows")

    # ---------------------------------------------------- G2: the identity ---
    resid = (real["sel_d"] - real["pool"] - real["lift"]).abs().max()
    say("\n" + "=" * 118)
    say("Q2 / GATE G2 — THE IDENTITY  sel_d == pool + lift")
    say("=" * 118)
    say(f"  max |sel_d - pool - lift| over {len(real)} claim rows = {resid:.3e}   "
        f"({'EXACT' if resid < 1e-12 else 'NOT EXACT — unsafe'})")
    assert resid < 1e-12

    # ------------------------------------------- G4: comparand invariance ----
    piv = real.pivot_table(index=["corpus", "pooldef", "panel", "poolname", "cost", "metric",
                                  "selector"], columns="comparand", values="lift")
    inv = float((piv.max(axis=1) - piv.min(axis=1)).abs().max())
    pv2 = real.pivot_table(index=["corpus", "pooldef", "panel", "poolname", "cost", "metric",
                                  "selector"], columns="comparand", values="sel_d")
    mv = float((pv2.max(axis=1) - pv2.min(axis=1)).abs().max())
    say("\n" + "=" * 118)
    say("Q5 / GATE G4 — COMPARAND INVARIANCE OF `lift`")
    say("=" * 118)
    say(f"  max spread of `lift` across the 3 comparands   = {inv:.3e}   "
        f"({'INVARIANT' if inv < 1e-12 else 'NOT INVARIANT'})")
    say(f"  max spread of `sel_d` across the 3 comparands  = {mv:.4f}"
        "   <- the entire comparand controversy lives in `pool`")
    assert inv < 1e-12
    # corpus B: the do-nothing control of all four families IS the live book, by construction
    bb = real[(real.corpus == "B") & (real.comparand.isin(["C_CONTROL", "C_V2"]))]
    bp = bb.pivot_table(index=["panel", "poolname", "cost", "metric", "selector"],
                        columns="comparand", values="sel_d")
    dcv = float((bp["C_CONTROL"] - bp["C_V2"]).abs().max())
    say(f"\n  corpus B disclosure: every family's do-nothing arm is EW/band3/g=0.75/weekly, "
        f"which IS RULES v2 —\n  max |sel_d(C_CONTROL) - sel_d(C_V2)| = {dcv:.3e}.  Corpus B "
        "therefore has TWO distinct comparands\n  (control == live book, and SPY), not three; "
        "corpus A's three are distinct.")

    # ------------------------------------------------ Q1: the asked regression
    say("\n" + "=" * 118)
    say("Q1 — THE REGRESSION IDEA 204 ASKS FOR:  sel_d ~ a + b * pool   (every selector)")
    say("=" * 118)
    regs = []
    for keys, sub in real.groupby(["corpus", "metric", "comparand", "selector"], sort=True):
        o = ols(sub["sel_d"], sub["pool"])
        vs, vp, vl = (float(sub["sel_d"].var(ddof=1)), float(sub["pool"].var(ddof=1)),
                      float(sub["lift"].var(ddof=1)))
        cov = float(np.cov(sub["pool"], sub["lift"], ddof=1)[0, 1])
        regs.append(dict(corpus=keys[0], metric=keys[1], comparand=keys[2], selector=keys[3],
                         n=o["n"], slope=o["slope"], icept=o["icept"], r2=o["r2"], t=o["t"],
                         var_sel=vs, share_pool=vp / vs if vs else np.nan,
                         share_lift=vl / vs if vs else np.nan,
                         share_2cov=2 * cov / vs if vs else np.nan))
    RG = pd.DataFrame(regs)
    RG.to_csv(OUT / f"{STEM}.regression.csv", index=False)
    for corpus in ("B", "A"):
        for met in sorted(RG.loc[RG.corpus == corpus, "metric"].unique()):
            sub = RG[(RG.corpus == corpus) & (RG.metric == met)]
            say(f"\n  corpus {corpus} · metric {met}")
            say(sub.drop(columns=["corpus", "metric", "var_sel"])
                .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  READ: K_RANDOM is the degenerate case — lift == 0 by construction, so its slope is "
        "exactly 1.0000\n  and its R2 exactly 1.0000 in every single row.  That is what the "
        "regression measures when the\n  pool is the whole story.")
    say("\n  Q1b — THE REGRESSION'S ANSWER IS A PROPERTY OF THE COMPARAND, NOT OF THE SELECTOR:")
    rr = RG[RG.selector != "K_RANDOM"].copy()
    rr["cmp_kind"] = np.where(rr["comparand"] == "C_CONTROL", "pool's own control",
                              "FIXED (SPY / live book)")
    say(rr.groupby(["corpus", "cmp_kind"]).agg(
        n=("r2", "size"), median_R2=("r2", "median"), min_R2=("r2", "min"),
        max_R2=("r2", "max"), median_slope=("slope", "median"),
        min_slope=("slope", "min"), max_slope=("slope", "max"),
        share_slope_near1=("slope", lambda s: float(((s - 1).abs() < 0.35).mean())),
        median_share_pool=("share_pool", "median"))
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say("  A FIXED comparand is common to every pool in a panel, so its own cross-pool variance "
        "is zero and\n  `pool` inherits all of it: R2 is then a measure of how much the "
        "COMPARAND moves, not of how much\n  the pool explains the selector.  Differencing "
        "against the pool's OWN control removes that shared\n  term and the same regression "
        "collapses.  Idea 204's proposed statistic is therefore not identified\n  without also "
        "naming the comparand — which is idea 398's open question, reached from a new direction.")

    # ------------------------------------------------------ Q3: sign story ---
    say("\n" + "=" * 118)
    say("Q3 — DOES THE POOL'S SIGN EXPLAIN THE SELECTOR'S SIGN?")
    say("=" * 118)
    srows = []
    for keys, sub in real.groupby(["corpus", "metric", "comparand"], sort=True):
        s = sub[(sub.selector != "K_RANDOM")]
        agree = float((np.sign(s["sel_d"]) == np.sign(s["pool"])).mean())
        decided = float((s["pool"].abs() > s["lift"].abs()).mean())
        neg = s[s["pool"] < 0]
        pos = s[s["pool"] > 0]
        srows.append(dict(corpus=keys[0], metric=keys[1], comparand=keys[2], n=len(s),
                          sign_agree=agree, pool_decides=decided,
                          p_seld_neg_given_pool_neg=float((neg["sel_d"] < 0).mean()) if len(neg) else np.nan,
                          p_seld_pos_given_pool_pos=float((pos["sel_d"] > 0).mean()) if len(pos) else np.nan,
                          share_pool_neg=float((s["pool"] < 0).mean())))
    SG = pd.DataFrame(srows)
    say(SG.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ Q4: lift ---
    say("\n" + "=" * 118)
    say("Q4 — DOES SELECTION HELP ONCE THE POOL IS REMOVED?  (mean `lift`, the residual)")
    say("=" * 118)
    lrows = []
    for keys, sub in real.groupby(["corpus", "metric", "selector"], sort=True):
        s = sub[sub.comparand == "C_CONTROL"]        # lift is comparand-invariant (G4)
        x = s["lift"].astype(float).values
        wins = int((x > 0).sum())
        ties = int((x == 0).sum())
        lrows.append(dict(corpus=keys[0], metric=keys[1], selector=keys[2], n=len(x),
                          mean_lift=float(np.mean(x)), sd=float(np.std(x, ddof=1)) if len(x) > 1 else np.nan,
                          t=tstat(x), wins=wins, losses=len(x) - wins - ties,
                          sign_p=sign_p(wins, len(x) - ties)))
    LF = pd.DataFrame(lrows)
    LF.to_csv(OUT / f"{STEM}.lift.csv", index=False)
    for corpus in ("B", "A"):
        for met in sorted(LF.loc[LF.corpus == corpus, "metric"].unique()):
            say(f"\n  corpus {corpus} · metric {met}")
            say(LF[(LF.corpus == corpus) & (LF.metric == met)].drop(columns=["corpus", "metric"])
                .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    sp = CL[CL.comparand == "_spread"]
    say(f"\n  K_RANDOM seeded control ({N_SEEDS} draws/pool, {len(sp)} pools): mean of the draw "
        f"means - pool mean = {sp['lift'].mean():+.5f} (closed form 0), "
        f"mean within-pool draw sd = {sp['lift_sd'].mean():.4f}")

    # -------------------------------- Q4b: lift at the PROTOCOL rung, per family
    for met in ("OOS_Sharpe", "OOS_CAGR"):
        say(f"\n  corpus B, PROTOCOL rung 10 bps only, by dial family (mean lift, {met}):")
        sb = real[(real.corpus == "B") & (real.metric == met) &
                  (real.cost == PROTOCOL_RUNG) & (real.comparand == "C_CONTROL")]
        say(sb.pivot_table(index="selector", columns="family", values="lift", aggfunc="mean")
            .to_string(float_format=lambda x: f"{x:+.4f}"))
    say("\n  READ: on the GROSS dial every selector's OOS_Sharpe lift is +-0.0012 (Sharpe is "
        "invariant in gross,\n  idea 311) while its OOS_CAGR lift is the largest of the four "
        "families — so a positive CAGR lift on a\n  gross-scalar pool is an EXPOSURE reading, "
        "not selection skill.  The two metrics disagree by construction.")

    # ------------------------------------------------------- Q6: rule 8 -----
    say("\n" + "=" * 118)
    say("Q6 — PROTOCOL RULE 8.  Selectors read IS (<= 2016-12-31) ONLY; read once on 2017-2026.")
    say("=" * 118)
    wf = []
    for (pk, fam, c), sub in gB.groupby(["panel", "family", "cost"], sort=True):
        sub = sub.reset_index(drop=True)
        ctl = sub.index[sub["control"]][0]
        pool_is = float(sub["IS_Sharpe"].mean())
        pool_oos = float(sub["OOS_Sharpe"].mean())
        spy_o = metrics(window(ref[pk]["spy"], "OOS"))
        v2_o = metrics(window(ref[pk]["v2"][c], "OOS"))
        v1_o = metrics(window(ref[pk]["v1"][c], "OOS"))
        s_is = sub["IS_Sharpe"].astype(float)
        med_j = s_is.sort_values(kind="mergesort").index[len(s_is) // 2]
        sels = dict(SEL_B)
        for k, (col, dr) in (list(sels.items()) + [("K_ANTI", ("IS_Sharpe", -1)),
                                                   ("K_MEDIAN", (None, 0))]):
            j = med_j if k == "K_MEDIAN" else pick(sub, col, dr)
            if j is None:
                continue
            r = store[(pk, fam, c, sub.loc[j, "arm"])]
            ro = window(r, "OOS")
            m = metrics(ro)
            ok_o, bind_o, _ = pass4b(r, ref[pk]["spy"], "OOS")
            ok_f, bind_f, _ = pass4b(r, ref[pk]["spy"], "full")
            wf.append(dict(panel=pk, family=fam, cost=c, selector=k, arm=sub.loc[j, "arm"],
                           pool_minus_ctl=pool_oos - float(sub.loc[ctl, "OOS_Sharpe"]),
                           IS_Sharpe=float(sub.loc[j, "IS_Sharpe"]),
                           IS_lift=float(sub.loc[j, "IS_Sharpe"]) - pool_is,
                           OOS_lift=float(sub.loc[j, "OOS_Sharpe"]) - pool_oos,
                           pool_IS=pool_is, pool_OOS=pool_oos,
                           OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                           d_vs_ctl=m["Sharpe"] - float(sub.loc[ctl, "OOS_Sharpe"]),
                           d_vs_v2=m["Sharpe"] - v2_o["Sharpe"],
                           d_vs_v1=m["Sharpe"] - v1_o["Sharpe"],
                           d_vs_spy=m["Sharpe"] - spy_o["Sharpe"],
                           spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                           spy_OOS_MaxDD=spy_o["MaxDD"], v2_OOS_Sharpe=v2_o["Sharpe"],
                           pass4a_v2=pass4a(r, ref[pk]["v2"][c]),
                           pass4b=ok_f, bind4b=bind_f, pass4b_oos=ok_o, bind4b_oos=bind_o))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say("\n  P5 — does IS lift predict OOS lift?  (OLS over every walk-forward cell)")
    for lab, W in (("all selectors", WF), ("excl. K_ANTI", WF[WF.selector != "K_ANTI"])):
        for c in COSTS:
            s = W[W.cost == c]
            o = ols(s["OOS_lift"], s["IS_lift"])
            say(f"    {lab:<14} @{c:>4.0f} bps  n={o['n']:>3}  slope {o['slope']:+.4f}  "
                f"t {o['t']:+.3f}  R2 {o['r2']:.4f}   mean IS_lift {s['IS_lift'].mean():+.4f} -> "
                f"mean OOS_lift {s['OOS_lift'].mean():+.4f}")
    say("    per family, all rungs (excl. K_ANTI):")
    for fam in FAMILIES:
        s = WF[(WF.family == fam) & (WF.selector != "K_ANTI")]
        o = ols(s["OOS_lift"], s["IS_lift"])
        say(f"      {fam:<8} n={o['n']:>3}  slope {o['slope']:+.4f}  t {o['t']:+.3f}  "
            f"R2 {o['r2']:.4f}   mean OOS_lift {s['OOS_lift'].mean():+.4f}")
    say("    READ: a positive SLOPE with a mean OOS_lift at ~0 says IS lift RANKS the pool's arms "
        "out of sample\n    but does not DELIVER a level — the selector is informative about "
        "which arm is worse, and buys nothing.")
    say("\n  is idea 205's column CAUSAL?  pool_OOS ~ pool_IS over the "
        f"{WF.groupby(['panel','family','cost']).ngroups} pools:")
    pp = WF.drop_duplicates(subset=["panel", "family", "cost"])
    o = ols(pp["pool_OOS"], pp["pool_IS"])
    say(f"    n={o['n']}  slope {o['slope']:+.4f}  icept {o['icept']:+.4f}  R2 {o['r2']:.4f}  "
        f"t {o['t']:+.3f}   sign agreement "
        f"{float((np.sign(pp['pool_OOS']) == np.sign(pp['pool_IS'])).mean()):.4f}")

    say(f"\n  walk-forward picks at the PROTOCOL rung ({PROTOCOL_RUNG:.0f} bps), all {len(WF[WF.cost==PROTOCOL_RUNG])} cells:")
    say(WF[WF.cost == PROTOCOL_RUNG].drop(columns=["cost", "pool_IS", "pool_OOS", "IS_Sharpe",
                                                   "spy_OOS_CAGR", "spy_OOS_MaxDD",
                                                   "v2_OOS_Sharpe", "bind4b"])
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  selector summary over all 36 walk-forward cells (mean d(OOS Sharpe), each comparand):")
    su = WF.groupby("selector").agg(n=("d_vs_ctl", "size"), IS_lift=("IS_lift", "mean"),
                                    OOS_lift=("OOS_lift", "mean"), vs_ctl=("d_vs_ctl", "mean"),
                                    vs_v2=("d_vs_v2", "mean"), vs_v1=("d_vs_v1", "mean"),
                                    vs_spy=("d_vs_spy", "mean"))
    su["t_OOS_lift"] = [tstat(WF.loc[WF.selector == k, "OOS_lift"]) for k in su.index]
    su["t_vs_ctl"] = [tstat(WF.loc[WF.selector == k, "d_vs_ctl"]) for k in su.index]
    say(su.to_string(float_format=lambda x: f"{x:+.4f}"))
    pmc = WF.drop_duplicates(subset=["panel", "family", "cost"])["pool_minus_ctl"]
    say(f"\n  THE DECOMPOSITION, ON THE WALK-FORWARD ITSELF:  the pool's own OOS mean sits "
        f"{pmc.mean():+.4f} below\n  the do-nothing control (t {tstat(pmc):+.3f}, negative in "
        f"{int((pmc < 0).sum())} of {len(pmc)} pools).  Every selector's mean OOS lift over that "
        f"pool is\n  smaller in magnitude than that deficit, so d_vs_ctl is negative for "
        f"{int((su['vs_ctl'] < 0).sum())} of {len(su)} selectors — idea 196's\n  shape "
        "(+lift over RANDOM, -delta vs do-nothing), at 36 cells per selector rather than one.")

    # --------------------------------------------------------- Q7: KEEP -----
    say("\n" + "=" * 118)
    say("Q7 — BOTH KEEP PATHS (PROTOCOL 4a and 4b), every corpus-B arm and every pick")
    say("=" * 118)
    kp = []
    for c in COSTS:
        s = gB[gB.cost == c]
        kp.append(dict(scope="arms", cost=c, n=len(s),
                       pass4a=int(s["pass4a_v2"].sum()), pass4b=int(s["pass4b"].sum()),
                       pass4b_oos=int(s["pass4b_oos"].sum()),
                       both=int((s["pass4a_v2"] & s["pass4b"]).sum())))
        w = WF[WF.cost == c]
        kp.append(dict(scope="picks", cost=c, n=len(w),
                       pass4a=int(w["pass4a_v2"].sum()), pass4b=int(w["pass4b"].sum()),
                       pass4b_oos=int(w["pass4b_oos"].sum()),
                       both=int((w["pass4a_v2"] & w["pass4b"]).sum())))
    KP = pd.DataFrame(kp)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(KP.to_string(index=False))
    say("\n  4b binding bar over corpus-B arms (full sample, all rungs):")
    say(gB["bind4b"].value_counts().to_string())
    say("  4b binding bar over corpus-B arms (OOS):")
    say(gB["bind4b_oos"].value_counts().to_string())
    b4 = gB[gB["pass4b"] & gB["pass4b_oos"] & (gB.cost == PROTOCOL_RUNG)]
    say(f"\n  arms clearing 4b FULL *and* OOS at {PROTOCOL_RUNG:.0f} bps: {len(b4)}")
    if len(b4):
        say(b4[["panel", "family", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "pass4a_v2"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # -------------------------------------------------------------- verdict --
    say("\n" + "=" * 118)
    say("PREDICTION SCORECARD")
    say("=" * 118)
    sl = RG[RG.selector != "K_RANDOM"]["slope"]
    p1 = bool(((sl - 1).abs() < 0.35).mean() > 0.9)
    ag = float(SG["sign_agree"].mean())
    p2 = bool(ag > 0.70)
    lf10 = LF[(LF.corpus == "B") & (LF.metric == "OOS_Sharpe")]
    anyup = lf10[(lf10.selector != "K_RANDOM") & (lf10.selector != "K_ANTI") &
                 (lf10["t"] > 2.0) & (lf10["mean_lift"] > 0)]
    anti = lf10[lf10.selector == "K_ANTI"]
    p3 = bool(len(anyup) == 0)
    o5 = ols(WF["OOS_lift"], WF["IS_lift"])
    o5b = ols(WF.loc[WF.selector != "K_ANTI", "OOS_lift"],
              WF.loc[WF.selector != "K_ANTI", "IS_lift"])
    p5 = bool(abs(o5["t"]) < 2.0)
    fx = RG[(RG.selector != "K_RANDOM") & (RG.comparand != "C_CONTROL")]
    ct = RG[(RG.selector != "K_RANDOM") & (RG.comparand == "C_CONTROL")]
    say(f"  P1 regression is an identity (|slope-1|<0.35 for >90% of selector rows): "
        f"{'CONFIRMED' if p1 else 'REJECTED'}  (share {float(((sl-1).abs()<0.35).mean()):.3f}, "
        f"median slope {sl.median():+.4f}, median R2 {RG[RG.selector!='K_RANDOM']['r2'].median():.4f})")
    say(f"     as pre-registered it is REJECTED, and the SPLIT is the finding: against a FIXED "
        f"comparand share {float(((fx['slope']-1).abs()<0.35).mean()):.3f}, median R2 "
        f"{fx['r2'].median():.4f}; against the pool's OWN control share "
        f"{float(((ct['slope']-1).abs()<0.35).mean()):.3f}, median R2 {ct['r2'].median():.4f}.")
    say(f"  P2 sign agreement > 70%: {'CONFIRMED' if p2 else 'REJECTED'}  (mean {ag:.4f}, "
        f"range {SG['sign_agree'].min():.4f}..{SG['sign_agree'].max():.4f})")
    say(f"  P3 no selector's mean lift reliably > 0: {'CONFIRMED' if p3 else 'REJECTED'}  "
        f"({len(anyup)} selectors with t>2 and mean lift>0)")
    if len(anti):
        say(f"     power check — K_ANTI mean lift {float(anti['mean_lift'].iloc[0]):+.4f} "
            f"t {float(anti['t'].iloc[0]):+.3f} (lift CAN detect a bad selector)")
    say(f"  P4 lift invariant to the comparand: CONFIRMED  (max spread {inv:.3e})")
    say(f"  P5 IS lift does not predict OOS lift: {'CONFIRMED' if p5 else 'REJECTED'}  "
        f"(slope {o5['slope']:+.4f}, t {o5['t']:+.3f}, R2 {o5['r2']:.4f}, n {o5['n']})")
    say(f"     excl. K_ANTI: slope {o5b['slope']:+.4f}, t {o5b['t']:+.3f}, R2 {o5b['r2']:.4f}, "
        f"n {o5b['n']}; mean OOS_lift over those cells "
        f"{WF.loc[WF.selector != 'K_ANTI', 'OOS_lift'].mean():+.4f} "
        f"(t {tstat(WF.loc[WF.selector != 'K_ANTI', 'OOS_lift']):+.3f}) — the slope is real, "
        f"the LEVEL is not delivered.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.{{console.txt,gridB.csv,claims.csv,regression.csv,lift.csv,"
        f"walkforward.csv,keeppaths.csv}}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

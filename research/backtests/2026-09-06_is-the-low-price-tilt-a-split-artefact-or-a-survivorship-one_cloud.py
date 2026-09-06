#!/usr/bin/env python3
"""QUEUE idea 185 - is-the-low-price-tilt-a-split-artefact-or-a-survivorship-one (cloud, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 185)
    "idea 181's selector picked PRICE/NEG in 6 of 6 rule-8 cells and beat do-nothing by +0.4086
     OOS Sharpe, the first selector in this project to beat the control, but share price level is
     split-history on u56/broad and on the small panel a low-price tilt points at exactly the
     cohort a current-constituent panel over-represents (small@10bps m=1.0: 20.59% OOS at Sharpe
     1.19).  Separate the two: re-run PRICE/NEG with price replaced by (a) a split-adjusted price
     rank frozen at panel entry, (b) a dollar-volume rank, (c) a market-cap proxy, and report
     which survives.  It fails 4b on broad (DD) and small (H1) already, so expect PARK or KILL.
     Max 2 params."

WHAT THIS RUN OWES THE RECORD, AND WHAT IT DOES NOT
    Idea 193 (committed 2026-09-05) already ran legs (a) and (b) and settled a THIRD horn the
    queue text did not anticipate: on auto-adjusted closes `px[T]/px[t]` IS the cumulative total
    return t->T, so a cross-sectional price-LEVEL rank is terminal price MINUS REALISED FUTURE
    TOTAL RETURN.  That result subsumes idea 185's SPLIT horn analytically - a split-adjusted
    level and a dividend-adjusted level are the same object, and the "split history" the queue
    worried about is one term of an adjustment factor that is only known at T.  Legs (a) FROZEN
    and (b) DVOL are therefore REPRODUCED here as controls, not re-discovered.
    Leg (c), a market-cap proxy, needs a shares-outstanding series.  None is cached in data/ and
    this sandbox has no internet, so leg (c) is NOT RUNNABLE here - exactly as idea 193 found and
    idea 195 queued.  It is declared, not silently dropped.

    What idea 185 asks that idea 193 did NOT answer is the SURVIVORSHIP horn: the small panel is
    a current-constituent list, so a name that once fell 80% and is still in the panel is
    over-represented by construction, and "tilt toward low price" points straight at that cohort.
    This run tests that horn two ways, and adds the leak-free analogue of the tilt:
      Q1  REPRODUCE   idea 181's published PRICE/MOM/R3 cells, and legs (a) and (b).
      Q2  LEAK-FREE   does the CAUSAL analogue of "tilt toward beaten-down names" - trailing
                      252d drawdown, knowable at t - reproduce PRICE/NEG's dSharpe?  If it does,
                      the tilt is a real beaten-down effect; if it does not, the published effect
                      is the adjustment leak and nothing else.
      Q3  SURVIVORSHIP  split the small panel into terciles by each NAME'S OWN full-sample max
                      drawdown (an oracle-conditioned cohort, declared as such, not a book) and
                      re-run PRICE/NEG inside each.  If the edge is survivorship it must live in
                      the deep-drawdown cohort and vanish in the shallow one.
      Q4  LEAK IC     Spearman between each key's rank at t and the realised forward total return
                      t->T, the direct measurement of how much of each key is future information.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4
    1. KEY          - the axis under test.  ALL keys reported, none preferred.
    2. TILT STRENGTH m in {0.20, 0.50, 1.00} - all three reported at every key and direction.
    Panel, direction and cost rung are REPORTED AXES inherited from the parent, not tuned.

THE BOOK - idea 181's, unchanged, so the arms are comparable to the published ones
    top N=20 by (composite + dir * m * key) among names above the 200d MA with vol20 < 0.60,
    equal weight at GROSS 0.75, weekly, t+1 execution, costs 10 and 25 bps.
    Panels: broad (136 large caps) and small (the sub-$2B panel with every ticker whose
    data/small_meta.csv max_1d_move >= 1.0 dropped first, per standing instruction).

KEYS
    published anchors   PRICE MOM R3 VOL R6      (reproduction of idea 181's grid)
    queue leg (a)       FROZEN   split-adjusted price rank frozen at panel entry
    queue leg (b)       DVOL     20d mean dollar volume rank            (small panel only)
    queue leg (c)       MCAP     NOT RUNNABLE - no shares-outstanding series offline
    leak-free analogues DDTR     trailing 252d drawdown px/rolling-max - 1  (the causal "low
                                 price" / beaten-down tilt; NEG = tilt toward beaten-down)
                        REBASED  px / first observed price (causal level proxy, idea 193's)
                        VOLSH    20d mean share volume rank             (small panel only)
    oracle diagnostics  PXTERM   terminal price level        } idea 193's decomposition, carried
                        FWDRET   realised forward return     } so the leak is priced, not assumed
    null band           NULL00..19, idea 181's own 20 matched draws at the parent's per-panel
                        seed, so the published bands reproduce.  Report-only: idea 192 killed
                        the clause as a KEEP gate.

WALK-FORWARD (PROTOCOL rule 8, required)
    Per (panel, cost) cell the arm is chosen on <= 2016-12-31 by IS Sharpe alone, three selectors:
      S0  do nothing (the composite control)          the standing eight-run champion
      S1  best IS Sharpe over ALL keys                what the record's selector does
      S2  best IS Sharpe over LEAK-FREE keys only     the only implementable version
    2017-01-01.. read once.  OOS CAGR/Sharpe/MaxDD reported against RULES v1 and SPY.

BOTH KEEP PATHS (PROTOCOL rule 4) evaluated on every arm in the run, 4a and 4b exactly.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  Reproduction of idea 181's published PRICE/MOM/R3/VOL/R6 cells to < 1e-9.
    P2  PRICE/NEG's dSharpe is large and positive on both panels (it is the published finding).
    P3  DDTR/NEG - the leak-free analogue - carries LESS THAN HALF of PRICE/NEG's dSharpe.  If
        the tilt were a real beaten-down effect the causal version would carry most of it.
    P4  FROZEN does not replicate on the small panel (idea 193 found 0/12) and DVOL does (6/12),
        and DVOL's replication tracks its leak IC, not its liquidity content.
    P5  |Spearman(key, forward return)| orders PRICE > DVOL > FROZEN > DDTR ~ 0, and mean
        dSharpe orders the same way.  The tilt is priced by its leak, not by its economics.
    P6  SURVIVORSHIP: PRICE/NEG's dSharpe is LARGER in the deep-drawdown tercile than in the
        shallow one - the cohort a current-constituent panel over-represents.
    P7  No 4b pass among the leak-free arms.  Verdict PARK or KILL, per the queue's own
        expectation.

CAVEATS carried, not buried
    * SURVIVORSHIP is the subject here, not a footnote: both panels are CURRENT-CONSTITUENT
      lists (data/SMALL_PANEL_README.md, idea 54).  Q3's cohorts are formed on FULL-SAMPLE
      drawdown, i.e. they are oracle-conditioned by construction - they are a diagnostic of the
      panel, never a book, and no level in Q3 is an attainable return.
    * Q4's forward-return IC uses the terminal date, which is look-ahead by construction.  That
      is the point of the measurement; it is labelled, and no arm is selected on it.
    * SPY is a benchmark column on the small panel, never a constituent; it carries no volume, so
      DVOL/VOLSH give it a neutral 0.5 rank (idea 193's convention, kept for comparability).
    * Idea 38: data/prices*.csv are calendar-day indexed after 2014-09-17.  It hits every arm and
      the control identically.
    * Leg (c) is not runnable offline.  It is reported as NOT RUN, with the reason.

Deterministic, standalone.  Writes .console.txt, .arms.csv, .cohorts.csv, .keyic.csv,
.walkforward.csv, .reproduction.csv.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_is-the-low-price-tilt-a-split-artefact-or-a-survivorship-one_cloud"
OUT = ROOT / "research" / "backtests"
PARENT = "2026-09-05_does-a-null-column-change-any-published-verdict_cloud"

# ---- inherited verbatim from ideas 181/193 so the published cells and null bands reproduce
SEED, B_NULL = 181, 20
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
COSTS = [10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
PANEL_IX = {"u56": 0, "broad": 1, "small": 2}
PHI, DELTA = 0.70, 0.60

ANCHORS = ["VOL", "MOM", "R6", "R3", "PRICE"]        # idea 181's published real keys, its order
LEAKFREE = ["MOM", "R3", "R6", "VOL", "DDTR", "REBASED"]
ORACLE = ["PXTERM", "FWDRET"]
PRICELEVEL = ["PRICE", "FROZEN"]

_console = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


def rankpct(df):
    return df.rank(axis=1, pct=True)


def spearman(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 5:
        return np.nan
    ra, rb = pd.Series(a[m]).rank().values, pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ------------------------------------------------------------------ vectorised engine equivalent
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
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
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ------------------------------------------------------------------------------ panels and keys
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"  small panel: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(keep) - 1} names + SPY benchmark remain  (SURVIVORSHIP: current constituents only)")
    return px[keep]


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


def first_valid_row(px):
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def last_valid_row(px):
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(lv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def build_keys(px, panel, rng):
    entry, term = first_valid_row(px), last_valid_row(px)
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    keys = {
        "VOL":     rankpct(vol20),                                  # published (idea 181)
        "MOM":     rankpct(px.shift(21) / px.shift(252) - 1),       # published
        "R6":      rankpct(px / px.shift(126) - 1),                 # published
        "R3":      rankpct(px / px.shift(63) - 1),                  # published
        "PRICE":   rankpct(px),                                     # published - THE arm on trial
        "FROZEN":  rankpct(entry),                                  # queue leg (a)
        "DDTR":    rankpct(px / px.rolling(252).max() - 1.0),       # leak-free "beaten down"
        "REBASED": rankpct(px / entry),                             # causal level proxy
        "PXTERM":  rankpct(term),                                   # oracle diagnostic
        "FWDRET":  rankpct(term / px - 1.0),                        # oracle diagnostic
    }
    if panel == "small":
        vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
        for nm, raw in (("DVOL", px * vol), ("VOLSH", vol)):       # queue leg (b), and its
            k = rankpct(raw.rolling(20).mean())                    # price-free companion
            if "SPY" in k.columns:
                k["SPY"] = 0.5
            keys[nm] = k
    sd = float(np.nanmedian(px.pct_change().std().values))
    for j in range(B_NULL):
        steps = rng.normal(0.0, sd, size=px.shape)
        walk = pd.DataFrame(np.cumsum(steps, axis=0), index=px.index, columns=px.columns) + 10.0
        keys[f"NULL{j:02d}"] = rankpct(walk / walk.shift(126) - 1)
    return keys


# --------------------------------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def full_row(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_LO))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = \
            m["CAGR"], m["Sharpe"], m["MaxDD"]
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]
                and row["CAGR_F"] >= PHI * spy["CAGR_F"])


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


# ============================================================================================ run
def main():
    t0 = time.time()
    say("=" * 112)
    say(f"IDEA 185  is-the-low-price-tilt-a-split-artefact-or-a-survivorship-one  (cloud, "
        f"{pd.Timestamp.today().date()})")
    say("=" * 112)
    say("Idea 193 settled the SPLIT horn analytically (an adjusted price LEVEL is terminal price")
    say("minus realised future total return) and ran legs (a) FROZEN and (b) DVOL.  Leg (c) MCAP")
    say("needs a shares-outstanding series: none is cached and the sandbox has no internet, so it")
    say("is NOT RUN here and stays queued as idea 195.  What this run adds is the SURVIVORSHIP")
    say("horn and the leak-free analogue of the tilt.")
    say("Two tuned params: KEY (all reported) x TILT STRENGTH m in %s (all reported)." % MS)
    say("")

    panels = {"broad": load_universe(broad=True), "small": small_panel()}
    arms, repro, ics, cohorts = [], [], [], []

    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0, freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    say(f"R0  RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / {mu['MaxDD']:.5%}"
        f"   (published 6.45305% / 0.66418 / -13.82780%)")
    repro.append(dict(check="R0_rules_v1_u56", value=mu["Sharpe"], target=0.66418,
                      err=abs(mu["Sharpe"] - 0.66418)))
    say("")

    for pn, px in panels.items():
        start = px.index[260]
        keys = build_keys(px, pn, np.random.default_rng(SEED + 1000 * (1 + PANEL_IX[pn])))
        comp = composite(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        elig = (px > px.rolling(200).mean()) & (vol20 < MAXVOL)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        srow = full_row(spy)
        say(f"panel {pn}: {px.shape[1]} cols, sample {start.date()}..{px.index[-1].date()}, "
            f"SPY {srow['CAGR_F']:.2%}/{srow['Sharpe_F']:.3f}/{srow['MaxDD_F']:.2%} "
            f"(H1 {srow['Sharpe_H1']:.3f} / H2 {srow['Sharpe_H2']:.3f} / OOS {srow['Sharpe_OOS']:.3f})")

        def run(sc, prices=px, el=elig, st=start):
            rk = sc.where(el).rank(axis=1, ascending=False)
            w = (rk <= N).astype(float) * (GROSS / N)
            g, t = fast_backtest(prices, w)
            return g.loc[st:], t.loc[st:]

        # --- reproduction controls
        c0, ct = run(comp)
        eng = backtest(px, (comp.where(elig).rank(axis=1, ascending=False) <= N).astype(float)
                       * (GROSS / N), cost_bps=0.0, freq=FREQ)["returns"].loc[start:]
        e2 = float((eng - c0).abs().max())
        say(f"  R1  fast_backtest == engine.backtest on the control book : max abs err {e2:.3e}")
        repro.append(dict(check=f"R1_engine_{pn}", value=e2, target=0.0, err=e2))
        trm = px.iloc[-1] / px
        cum = (1 + px.pct_change().fillna(0.0)).cumprod()
        ident = float(np.nanmax(np.abs((trm - cum.iloc[-1] / cum).values)))
        say(f"  R2  idea 193's adjusted-price identity px[T]/px[t] == TR(t->T): max err {ident:.3e}")
        repro.append(dict(check=f"R2_identity_{pn}", value=ident, target=0.0, err=ident))

        base = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        b0, bt = base["returns"].loc[start:], base["turnover"].loc[start:]
        base_rows = {c: full_row(b0 - bt * c / 1e4) for c in COSTS}
        ctrl_rows = {c: full_row(c0 - ct * c / 1e4) for c in COSTS}
        for c in COSTS:
            r = dict(panel=pn, key="CONTROL", klass="control", dir="-", m=0.0, cost=c,
                     turnover_yr=float(ct.sum() / (len(ct) / 252)),
                     dSharpe_F=0.0, dSharpe_IS=0.0, dSharpe_OOS=0.0)
            r.update(ctrl_rows[c])
            r["pass4a"] = pass4a(r, base_rows[c])
            r["pass4b"] = pass4b(r, srow)
            arms.append(r)

        # --- Q4: how much of each key is future information?
        fwd = (px.iloc[-1] / px - 1.0)
        for kn, kv in keys.items():
            if kn.startswith("NULL"):
                continue
            rows = kv.index[(len(kv) // 4)::252]        # a date grid, not a chosen date
            vals = [spearman(kv.loc[d].values, fwd.loc[d].values) for d in rows]
            ics.append(dict(panel=pn, key=kn, mean_IC_fwd=float(np.nanmean(vals)),
                            n_dates=int(np.isfinite(vals).sum())))

        # --- the grid
        for kn, kv in keys.items():
            klass = ("nullkey" if kn.startswith("NULL") else
                     "oracle" if kn in ORACLE else
                     "pricelevel" if kn in PRICELEVEL else
                     "leakfree" if kn in LEAKFREE else "levelproduct")
            for dn, dv in DIRS.items():
                for m in MS:
                    r0, trn = run(comp + dv * m * kv)
                    for c in COSTS:
                        rr = dict(panel=pn, key=kn, klass=klass, published=kn in ANCHORS,
                                  dir=dn, m=m, cost=c,
                                  turnover_yr=float(trn.sum() / (len(trn) / 252)))
                        rr.update(full_row(r0 - trn * c / 1e4))
                        for tag in ("F", "IS", "OOS"):
                            rr[f"dSharpe_{tag}"] = rr[f"Sharpe_{tag}"] - ctrl_rows[c][f"Sharpe_{tag}"]
                        rr["pass4a"] = pass4a(rr, base_rows[c])
                        rr["pass4b"] = pass4b(rr, srow)
                        arms.append(rr)
        say(f"  ... {pn} grid done ({time.time()-t0:.0f}s)")

        # --- Q3: the survivorship cohorts (small panel only; it is the panel the queue names)
        if pn == "small":
            names = [c for c in px.columns if c != "SPY"]
            eq = px[names]
            dd = (eq / eq.cummax() - 1.0).min()
            q = dd.quantile([1 / 3, 2 / 3])
            groups = {"deepDD": [c for c in names if dd[c] <= q.iloc[0]],
                      "midDD": [c for c in names if q.iloc[0] < dd[c] <= q.iloc[1]],
                      "shallowDD": [c for c in names if dd[c] > q.iloc[1]]}
            say("")
            say("  Q3 SURVIVORSHIP COHORTS (terciles of each NAME'S full-sample max drawdown).")
            say("     ORACLE-CONDITIONED BY CONSTRUCTION: the cohort uses the whole sample, so")
            say("     these are a diagnostic of the panel, never a book.  No level is attainable.")
            for gn, cols in groups.items():
                sub = px[cols + ["SPY"]]
                sel = elig[cols + ["SPY"]]
                cs = comp[cols + ["SPY"]]
                g0, gt = run(cs, sub, sel, start)
                gctrl = {c: full_row(g0 - gt * c / 1e4) for c in COSTS}
                say(f"     {gn:10s} {len(cols):3d} names, mean full-sample MaxDD "
                    f"{dd[cols].mean():7.2%}, control Sharpe {gctrl[10.0]['Sharpe_F']:.4f}")
                for kn in ["PRICE", "DDTR", "DVOL", "FROZEN"]:
                    if kn not in keys:
                        continue
                    kv = keys[kn][cols + ["SPY"]]
                    for m in MS:
                        r0, trn = run(cs - m * kv, sub, sel, start)
                        for c in COSTS:
                            rw = full_row(r0 - trn * c / 1e4)
                            cohorts.append(dict(cohort=gn, n_names=len(cols),
                                                mean_maxdd=float(dd[cols].mean()), key=kn,
                                                dir="NEG", m=m, cost=c,
                                                Sharpe_F=rw["Sharpe_F"],
                                                dSharpe_F=rw["Sharpe_F"] - gctrl[c]["Sharpe_F"],
                                                dSharpe_OOS=rw["Sharpe_OOS"] - gctrl[c]["Sharpe_OOS"],
                                                CAGR_F=rw["CAGR_F"], MaxDD_F=rw["MaxDD_F"]))
        say("")

    A = pd.DataFrame(arms)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    IC = pd.DataFrame(ics)
    IC.to_csv(OUT / f"{STEM}.keyic.csv", index=False)
    CO = pd.DataFrame(cohorts)
    CO.to_csv(OUT / f"{STEM}.cohorts.csv", index=False)
    say(f"{len(A)} arm rows, {len(CO)} cohort rows  ({time.time()-t0:.0f}s)")
    say("")

    # ---------------------------------------------------------------- Q1: reproduction of idea 181
    say("=" * 112)
    say("Q1  REPRODUCTION of idea 181's published grid (broad + small, its 5 real keys + 20 nulls)")
    old = pd.read_csv(OUT / f"{PARENT}.grid.csv")
    old = old[old.panel.isin(["broad", "small"])]
    mine = A[["panel", "key", "dir", "m", "cost", "Sharpe_F", "dSharpe_F", "Sharpe_OOS"]]
    mg = old.merge(mine, on=["panel", "key", "dir", "m", "cost"], suffixes=("_o", "_n"))
    d1 = float((mg.Sharpe_F_o - mg.Sharpe_F_n).abs().max())
    d2 = float((mg.dSharpe_F_o - mg.dSharpe_F_n).abs().max())
    say(f"  matched {len(mg)} of the parent's {len(old)} broad+small rows; "
        f"max |dSharpe_F| {d1:.3e}, max |ddSharpe_F| {d2:.3e} -> "
        f"{'PASS' if (d1 < 1e-9 and d2 < 1e-9) else 'FAIL'}")
    repro.append(dict(check="Q1_parent_grid", value=max(d1, d2), target=0.0, err=max(d1, d2)))
    pd.DataFrame(repro).to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    if not (d1 < 1e-9 and d2 < 1e-9):
        say("  *** the published cells do not reproduce; the substitutions are not comparable.")
    say("")

    # ---------------------------------------------------------------- Q2: the substitution table
    say("=" * 112)
    say("Q2  THE SUBSTITUTION TABLE - mean dSharpe_F over the 3 tilt strengths, both directions,")
    say("    both cost rungs.  ALL grid points are in .arms.csv; nothing here is picked.")
    say("")
    real = A[~A.key.str.startswith("NULL") & (A.key != "CONTROL")]
    nul = A[A.key.str.startswith("NULL")]
    for pn in panels:
        say(f"  panel {pn}")
        say(f"  {'key':9s} {'class':13s} " + " ".join(f"{('m'+str(m)+'/'+d):>13s}"
                                                      for d in ["NEG", "POS"] for m in MS)
            + f" {'mean NEG':>10s} {'null q95 |d|':>13s}")
        band = float(np.nanquantile(nul[nul.panel == pn]["dSharpe_F"].abs().values, 0.95)) \
            if len(nul[nul.panel == pn]) else np.nan
        for kn in [k for k in real[real.panel == pn].key.unique()]:
            g = real[(real.panel == pn) & (real.key == kn)]
            cells = []
            for d in ["NEG", "POS"]:
                for m in MS:
                    v = g[(g["dir"] == d) & (g.m == m)]["dSharpe_F"].mean()
                    cells.append(f"{v:+13.4f}")
            mneg = g[g["dir"] == "NEG"]["dSharpe_F"].mean()
            say(f"  {kn:9s} {g.klass.iloc[0]:13s} " + " ".join(cells)
                + f" {mneg:+10.4f} {band:13.4f}")
        say("")
    say("  LEG (c) MCAP: NOT RUN.  A market-cap proxy needs shares outstanding; no such series is")
    say("  cached in data/ and this sandbox has no internet.  Unchanged from idea 193; idea 195.")
    say("")

    # ---------------------------------------------------------------- Q4: the leak IC
    say("=" * 112)
    say("Q4  HOW MUCH OF EACH KEY IS FUTURE INFORMATION")
    say("    mean Spearman(key rank at t, realised forward total return t->T) on an annual date")
    say("    grid, against the key's own mean NEG-direction dSharpe.  A key that scores near 0")
    say("    on the IC and near 0 on dSharpe is telling the same story twice.")
    say("")
    say(f"  {'panel':6s} {'key':9s} {'class':13s} {'mean IC vs fwd ret':>19s} {'mean dSharpe NEG':>17s} "
        f"{'mean dSharpe POS':>17s}")
    for _, r in IC.sort_values(["panel", "mean_IC_fwd"]).iterrows():
        g = real[(real.panel == r.panel) & (real.key == r.key)]
        say(f"  {r.panel:6s} {r.key:9s} {g.klass.iloc[0]:13s} {r.mean_IC_fwd:19.4f} "
            f"{g[g['dir']=='NEG'].dSharpe_F.mean():17.4f} {g[g['dir']=='POS'].dSharpe_F.mean():17.4f}")
    say("")
    for pn in panels:
        s = IC[IC.panel == pn].merge(
            real[real["dir"] == "NEG"].groupby(["panel", "key"])["dSharpe_F"].mean().reset_index(),
            on=["panel", "key"])
        say(f"  Spearman(|IC vs forward return|, mean NEG dSharpe) on {pn}: "
            f"{spearman(-s.mean_IC_fwd.values, s.dSharpe_F.values):+.3f}  (n={len(s)} keys)")
    say("")

    # ---------------------------------------------------------------- Q3: cohorts
    say("=" * 112)
    say("Q3  THE SURVIVORSHIP HORN - PRICE/NEG and its substitutes inside drawdown-cohort panels")
    say("    (small panel; cohorts are oracle-conditioned, see the caveat - diagnostic, not a book)")
    say("")
    if len(CO):
        say(f"  {'key':8s} {'m':>5s} {'cost':>5s} " + " ".join(f"{c:>22s}" for c in
                                                               ["deepDD", "midDD", "shallowDD"])
            + f" {'deep-minus-shallow':>19s}")
        for kn in CO.key.unique():
            for m in MS:
                for c in COSTS:
                    g = CO[(CO.key == kn) & (CO.m == m) & (CO.cost == c)].set_index("cohort")
                    cells, vals = [], {}
                    for ch in ["deepDD", "midDD", "shallowDD"]:
                        if ch in g.index:
                            vals[ch] = g.loc[ch, "dSharpe_F"]
                            cells.append(f"{g.loc[ch,'Sharpe_F']:8.4f} (d{vals[ch]:+7.4f})")
                        else:
                            cells.append(f"{'-':>22s}")
                    dm = (vals.get("deepDD", np.nan) - vals.get("shallowDD", np.nan))
                    say(f"  {kn:8s} {m:5.2f} {c:5.0f} " + " ".join(f"{x:>22s}" for x in cells)
                        + f" {dm:+19.4f}")
        say("")
        say("  cohort composition:")
        for ch, g in CO.groupby("cohort"):
            say(f"   {ch:10s} {int(g.n_names.iloc[0]):3d} names, mean full-sample MaxDD "
                f"{g.mean_maxdd.iloc[0]:7.2%}")
        say("")
        for kn in CO.key.unique():
            g = CO[CO.key == kn]
            piv = g.pivot_table(index=["m", "cost"], columns="cohort", values="dSharpe_F")
            if "deepDD" in piv and "shallowDD" in piv:
                d = (piv["deepDD"] - piv["shallowDD"]).dropna()
                say(f"   {kn:8s} deep-minus-shallow dSharpe over {len(d)} (m,cost) cells: "
                    f"mean {d.mean():+.4f}, {int((d>0).sum())}/{len(d)} positive")
    say("")

    # ---------------------------------------------------------------- rule 8
    say("=" * 112)
    say("PROTOCOL RULE 8 WALK-FORWARD - arm chosen on <= 2016-12-31 by IS Sharpe, OOS read once")
    say("")
    wf = []
    say(f"  {'panel':6s} {'cost':>5s} {'selector':10s} {'pick':22s} {'OOS CAGR':>9s} "
        f"{'OOS Sharpe':>11s} {'OOS MaxDD':>10s} {'vs S0':>8s} {'4b':>4s}")
    for pn in panels:
        px = panels[pn]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        srow = full_row(spy)
        bs = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        for c in COSTS:
            brow = full_row(bs["returns"].loc[start:] - bs["turnover"].loc[start:] * c / 1e4)
            cell = A[(A.panel == pn) & (A.cost == c)]
            s0 = cell[cell.key == "CONTROL"].iloc[0]
            pools = {
                "S0-nothing": cell[cell.key == "CONTROL"],
                "S1-any key": cell[(cell.key != "CONTROL") & (~cell.key.str.startswith("NULL"))],
                "S2-leakfree": cell[cell.klass == "leakfree"],
            }
            for sn, pool in pools.items():
                if not len(pool):
                    continue
                pick = pool.loc[pool["Sharpe_IS"].idxmax()]
                lbl = f"{pick.key}/{pick['dir']}/m{pick.m:.2f}"
                say(f"  {pn:6s} {c:5.0f} {sn:10s} {lbl:22s} {pick.CAGR_OOS:9.2%} "
                    f"{pick.Sharpe_OOS:11.4f} {pick.MaxDD_OOS:10.2%} "
                    f"{pick.Sharpe_OOS - s0.Sharpe_OOS:+8.4f} {str(bool(pick.pass4b)):>4s}")
                wf.append(dict(panel=pn, cost=c, selector=sn, pick=lbl, key=pick.key,
                               OOS_CAGR=pick.CAGR_OOS, OOS_Sharpe=pick.Sharpe_OOS,
                               OOS_MaxDD=pick.MaxDD_OOS,
                               d_vs_S0=float(pick.Sharpe_OOS - s0.Sharpe_OOS),
                               pass4a=bool(pick.pass4a), pass4b=bool(pick.pass4b),
                               spy_OOS_Sharpe=srow["Sharpe_OOS"], spy_OOS_CAGR=srow["CAGR_OOS"],
                               spy_OOS_MaxDD=srow["MaxDD_OOS"], v1_OOS_Sharpe=brow["Sharpe_OOS"],
                               v1_OOS_CAGR=brow["CAGR_OOS"], v1_OOS_MaxDD=brow["MaxDD_OOS"]))
            say(f"  {pn:6s} {c:5.0f} {'reference':10s} {'SPY':22s} {srow['CAGR_OOS']:9.2%} "
                f"{srow['Sharpe_OOS']:11.4f} {srow['MaxDD_OOS']:10.2%}")
            say(f"  {pn:6s} {c:5.0f} {'reference':10s} {'RULES v1':22s} {brow['CAGR_OOS']:9.2%} "
                f"{brow['Sharpe_OOS']:11.4f} {brow['MaxDD_OOS']:10.2%}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("")
    for sn, g in WF.groupby("selector"):
        say(f"  {sn:12s} mean OOS Sharpe {g.OOS_Sharpe.mean():.4f}  mean d vs S0 "
            f"{g.d_vs_S0.mean():+.4f} (t {tstat(g.d_vs_S0.values):+.2f})  4b {int(g.pass4b.sum())}/{len(g)}")
    say("")

    # ---------------------------------------------------------------- KEEP paths
    say("=" * 112)
    say("BOTH KEEP PATHS over every arm in the run (PROTOCOL rule 4a and 4b, exactly)")
    say(f"  {'class':13s} {'arms':>5s} {'4a':>4s} {'4b':>4s}")
    for kl, g in A.groupby("klass"):
        say(f"  {kl:13s} {len(g):5d} {int(g.pass4a.sum()):4d} {int(g.pass4b.sum()):4d}")
    lf = A[A.klass == "leakfree"]
    say(f"  -> leak-free arms passing 4b: {int(lf.pass4b.sum())} of {len(lf)}")
    p4 = A[A.pass4b & (A.key != "CONTROL")]
    if len(p4):
        say("  4b passes (all classes, so the leaky ones are visible and labelled):")
        for _, r in p4.sort_values("Sharpe_OOS", ascending=False).head(15).iterrows():
            say(f"   {r.panel:6s} {r.key:8s}/{r['dir']:3s} m{r.m:.2f} @{r.cost:.0f}bps "
                f"[{r.klass}] CAGR {r.CAGR_F:6.2%} Sharpe {r.Sharpe_F:.4f} MaxDD {r.MaxDD_F:7.2%} "
                f"halves {r.Sharpe_H1:.3f}/{r.Sharpe_H2:.3f} OOS {r.Sharpe_OOS:.4f}")
    else:
        say("  4b passes among the tilted arms: NONE.")
    say("")

    # ---------------------------------------------------------------- predictions
    say("=" * 112)
    say("PRE-REGISTERED PREDICTIONS - scored")

    def mean_d(pn, k, d="NEG"):
        g = real[(real.panel == pn) & (real.key == k) & (real["dir"] == d)]
        return float(g.dSharpe_F.mean()) if len(g) else np.nan

    p1 = (d1 < 1e-9 and d2 < 1e-9)
    pr_s, pr_b = mean_d("small", "PRICE"), mean_d("broad", "PRICE")
    dd_s, dd_b = mean_d("small", "DDTR"), mean_d("broad", "DDTR")
    p2 = pr_s > 0 and pr_b > 0
    p3 = (abs(dd_s) < 0.5 * abs(pr_s)) and (abs(dd_b) < 0.5 * abs(pr_b))
    say(f"  P1 reproduction of idea 181 to <1e-9                       -> {'HIT' if p1 else 'MISS'}")
    say(f"  P2 PRICE/NEG large and positive on both panels  small {pr_s:+.4f} broad {pr_b:+.4f} "
        f"-> {'HIT' if p2 else 'MISS'}")
    say(f"  P3 DDTR/NEG carries < half of PRICE/NEG   small {dd_s:+.4f} broad {dd_b:+.4f} "
        f"-> {'HIT' if p3 else 'MISS'}")
    say(f"  P4 FROZEN {mean_d('small','FROZEN'):+.4f} (small) / {mean_d('broad','FROZEN'):+.4f} "
        f"(broad);  DVOL {mean_d('small','DVOL'):+.4f} (small)")
    ic_ord = IC[IC.panel == "small"].set_index("key")["mean_IC_fwd"]
    say(f"  P5 leak ordering on small: " + ", ".join(
        f"{k} {ic_ord.get(k, np.nan):+.3f}" for k in ["PRICE", "DVOL", "FROZEN", "DDTR"]))
    if len(CO):
        g = CO[CO.key == "PRICE"].pivot_table(index=["m", "cost"], columns="cohort", values="dSharpe_F")
        dms = (g["deepDD"] - g["shallowDD"]).dropna() if "deepDD" in g and "shallowDD" in g else pd.Series(dtype=float)
        say(f"  P6 PRICE/NEG deeper in the deep-DD cohort   mean deep-minus-shallow "
            f"{dms.mean():+.4f} ({int((dms>0).sum())}/{len(dms)} cells) -> "
            f"{'HIT' if len(dms) and dms.mean() > 0 else 'MISS'}")
    say(f"  P7 no 4b pass among leak-free arms   {int(lf.pass4b.sum())} passes -> "
        f"{'HIT' if int(lf.pass4b.sum()) == 0 else 'MISS'}")
    say("")
    say(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()

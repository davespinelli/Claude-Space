#!/usr/bin/env python3
"""Idea 332: is the H2-for-DD exchange rate of the CADENCE dial a record-wide constant?

Idea 329's monthly-vs-weekly move on B136 (top-20, m=20, 10 bps) buys +0.189 of 4b H2 margin
for -0.059 of 4b DD margin -- a ratio of -3.2 H2 per unit DD.  If that exchange rate were a
constant of the cadence dial, ONE weekly cell would tell you, without running anything, whether
slowing the book down can ever clear 4b: 4b's H2 bar and DD cap trade against each other, so a
weekly cell whose H2 deficit costs more DD than it has margin for is unreachable by cadence.

DEFINITIONS (fixed before any number was read; both are 4b margins, not raw metrics):
    H2 margin  = Sharpe(H2) - Sharpe(SPY, H2)                       [4b bar: > 0]
    DD margin  = 0.60*|MaxDD(SPY)| - |MaxDD(book)|                   [4b bar: > 0]
    R          = d(H2 margin) / d(DD margin) over a cadence pair holding EVERYTHING else fixed.
SPY is constant inside a panel, so R = dH2 / -d|MaxDD| and needs no benchmark alignment across
files.  R < 0 means slowing down buys H2 and pays drawdown (idea 329's direction).

THE TEST, pre-registered:

  [A] FRESH CORPUS, one instrument, three reported axes.  Book: top-n eligible by the RULES v1
      composite with the vol scaler OFF, RULES v1 eligibility (above the 200d MA, vol20 < 0.60),
      NORM weights w_i = g/k_t, next-day execution, 10 bps.  cadence in {W, 2W, M, Q} x
      n in {10, 20, 40} x gross in {0.50, 0.75, 1.00} on 3 panels = 108 books, every one printed
      and written to <slug>.grid.csv.  Two tuned parameters (n, cadence); gross and panel are
      REPORTED axes -- they are exactly the axes the queue asks the ratio's spread over.

  [B] ARCHIVAL CENSUS.  Every committed grid CSV in research/backtests that carries a cadence
      column plus H2 and MaxDD: group on every other key column, form all cadence pairs inside
      each group, and price R.  Idea 329's own file is in the census and is the arithmetic gate.

  [C] IS THE CONSTANT USABLE?  The queue's actual deliverable.  From a WEEKLY cell alone, cadence
      can close the H2 bar without breaking the DD cap iff  DDmargin_W - |H2deficit_W / R| > 0.
      Scored with a LEAVE-ONE-PANEL-OUT R (the panel being predicted never contributes to its own
      R) against the observed monthly cell.  A constant that cannot call the monthly outcome is
      not a screening rule, whatever its spread.

  [D] RULE 8 walk-forward: (n, cadence) chosen on 2008-2016 by IS Sharpe at 10 bps with gross
      pinned at 0.75, 2017-2026 read once, against the weekly n=20 anchor, the OOS-best cell
      (regret), RULES v2 (live) and SPY.  Both KEEP paths evaluated on every grid point.

REPRODUCTION GATES (section [0], asserted before any new number is read):
  * fast_backtest == engine.backtest to 1e-12 on returns AND turnover;
  * the derived cost rung r(c) = r(0) - turnover*c/1e4 == engine.backtest(cost_bps=c) to 1e-12;
  * idea 329's COMMITTED B136 n=20 m=20 W and M rows re-derive its published +0.189 / -0.059 /
    -3.2 from the definitions above;
  * idea 329's COMMITTED B136 top-20 m=0 cells reproduce from this script's own book (the same
    construction at m=0): WEEKLY 12.99%/0.943/-20.05%, H2 0.803 and MONTHLY 16.61%/1.109/
    -26.10%, H2 0.958.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book; the LEVELS are optimistic, the cadence DIFFERENCES much less so, but a
ratio of two differences inherits both.  The small panel is the worst offender and the tickers
with max_1d_move >= 1.0 in data/small_meta.csv are dropped before anything is run.
(2) SMALL484 starts 2010-01-04, so its halves and its IS window are not the same calendar as
U56/B136.  (3) 2W decimates the weekly mask (every 2nd week-end), phase-anchored to the panel's
first complete week; a different phase is a different, unreported choice.  (4) The census in [B]
pools files with different books, costs and conventions; it prices the SPREAD of R, which is the
question, not a pooled estimate of R.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os
import re
import sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"     # re-read [A] from the committed grid CSV

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_price-the-H2-for-DD-exchange-rate-as-a-record-wide-constant_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL = 0.60
CADENCES = ["W", "2W", "M", "Q"]
NS = [10, 20, 40]
GROSSES = [0.50, 0.75, 1.00]
COST = 10.0
ANCHOR_N, ANCHOR_CAD, ANCHOR_G = 20, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
PAIRS = [("W", "2W"), ("2W", "M"), ("M", "Q"), ("W", "M")]     # fast -> slow


# ---------------------------------------------------------------- cadence
def reb_mask(idx, cadence):
    """Last trading day of each rebalance period.  W/M/Q are engine.rebalance_mask verbatim so
    the W and M cells reproduce idea 329 exactly.  2W decimates the weekly mask."""
    if cadence in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, cadence)
    w = rebalance_mask(idx, "W")
    pos = np.where(w.values)[0][1::2]
    s = pd.Series(False, index=idx)
    s.iloc[pos] = True
    return s


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the book
def rank_frame(px, drop_spy=False):
    """Composite rank among eligible names (v1 composite, vol scaler OFF; v1 eligibility).
    On U56/B136 SPY is a genuine constituent (idea 44's convention, needed for the gate); on the
    small panel it is joined only as a benchmark and is removed from eligibility."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def weights_top_n(rk, n, gross):
    s = (rk <= n).astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- fast backtester
def fast_backtest(px, w, cadence="W"):
    """Vectorised-loop clone of engine.backtest at ZERO cost; cost rungs are derived
    arithmetically as r(c) = r(0) - turnover*c/1e4 (identity asserted in [0])."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = reb_mask(px.index, cadence).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - 0.0
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    """PROTOCOL 4a: Sharpe > the LIVE book in BOTH halves and MaxDD no worse."""
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


# ---------------------------------------------------------------- [0] gates
def gates(panels):
    print("\n[0] REPRODUCTION GATES")
    px = panels["U56"]
    rk, _ = rank_frame(px)
    w = weights_top_n(rk, 20, 0.75)
    r0, t0 = fast_backtest(px, w, "W")
    eng0 = backtest(px, w, cost_bps=0.0, freq="W")
    d_ret = float(np.abs(r0 - eng0["returns"]).max())
    d_turn = float(np.abs(t0 - eng0["turnover"]).max())
    eng10 = backtest(px, w, cost_bps=10.0, freq="W")
    d_rung = float(np.abs((r0 - t0 * 10 / 1e4) - eng10["returns"]).max())
    print(f"    fast_backtest vs engine.backtest : returns {d_ret:.3e}  turnover {d_turn:.3e}")
    print(f"    derived rung r(10) vs engine(10) : {d_rung:.3e}")
    assert d_ret < 1e-12 and d_turn < 1e-12 and d_rung < 1e-12

    g = pd.read_csv(OUT / "2026-09-07_does-the-BAND-rescue-the-B136-H2-bar_C.grid.csv")
    sel = g[(g.panel == "B136") & (g.n == 20) & (g.m == 20)].set_index("cadence")
    dH2 = sel.loc["M", "H2_10"] - sel.loc["W", "H2_10"]
    dDD = -(abs(sel.loc["M", "MaxDD_10"]) - abs(sel.loc["W", "MaxDD_10"]))
    print(f"    idea 329 B136 n=20 m=20 W->M: dH2 {dH2:+.4f} (pub +0.189)  "
          f"dDDmargin {dDD:+.4f} (pub -0.059)  R {dH2/dDD:+.3f} (pub -3.2)")
    assert abs(dH2 - 0.189) < 5e-4 and abs(dDD + 0.059) < 5e-4 and abs(dH2 / dDD + 3.2) < 0.02

    b = panels["B136"]
    rkb, _ = rank_frame(b)
    wb = weights_top_n(rkb, 20, 0.75)
    start = b.index[WARMUP]
    for cad, pub in (("W", (0.1299, 0.943, -0.2005, 0.803)), ("M", (0.1661, 1.109, -0.2610, 0.958))):
        rr, tt = fast_backtest(b, wb, cad)
        r = (rr - tt * COST / 1e4).loc[start:]
        m = metrics(r); _, h2 = hs(r)
        print(f"    idea 329 B136 top20 m=0 {cad}: CAGR {m['CAGR']:.2%} (pub {pub[0]:.2%})  "
              f"Sharpe {m['Sharpe']:.3f} (pub {pub[1]:.3f})  MaxDD {m['MaxDD']:.2%} "
              f"(pub {pub[2]:.2%})  H2 {h2:.3f} (pub {pub[3]:.3f})")
        assert abs(m["CAGR"] - pub[0]) < 2e-3 and abs(m["Sharpe"] - pub[1]) < 5e-3
        assert abs(m["MaxDD"] - pub[2]) < 2e-3 and abs(h2 - pub[3]) < 5e-3
    print("    ALL GATES PASS")


# ---------------------------------------------------------------- [A] fresh corpus
def build_grid(panels):
    rows = []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname.startswith("SMALL")))
        br, bt = fast_backtest(px, rules_v2_weights(px), "W")
        base = (br - bt * COST / 1e4).loc[start:]
        bm = metrics(base); b1, b2 = hs(base); bo = metrics(base.loc[OOS_START:])
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}, "
              f"eligible/day mean {elig.sum(axis=1).loc[start:].mean():.1f}")
        print(f"    SPY  CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%} "
              f"MaxDD {so['MaxDD']:.2%} | 4b DD cap {0.6*abs(ms['MaxDD']):.4f} "
              f"CAGR floor {0.7*ms['CAGR']:.2%}")
        print(f"    RULES v2 (live, W, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f}")
        for n in NS:
            for g in GROSSES:
                w = weights_top_n(rk, n, g)
                for cad in CADENCES:
                    rr, tt = fast_backtest(px, w, cad)
                    r = (rr - tt * COST / 1e4).loc[start:]
                    m = metrics(r); h1, h2 = hs(r)
                    ro = r.loc[OOS_START:]; mo = metrics(ro)
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    ok4a, d4a, f4a = bars_4a(r, base)
                    rows.append(dict(
                        panel=pname, n=n, gross=g, cadence=cad, cost_bps=COST,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                        H1=h1, H2=h2,
                        IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        turn_yr=tt.loc[start:].sum() / (len(r) / 252),
                        H2_margin=d4b["H2"], DD_margin=d4b["DD"], H1_margin=d4b["H1"],
                        OOS_margin=d4b["OOS"], CAGR_margin=d4b["CAGR"],
                        pass4b=ok4b, fail4b=",".join(f4b), pass4a=ok4a, fail4a=",".join(f4a),
                        spy_H1=s1, spy_H2=s2, spy_MaxDD=ms["MaxDD"], spy_CAGR=ms["CAGR"],
                        spy_OOS_Sharpe=so["Sharpe"], spy_OOS_CAGR=so["CAGR"],
                        spy_OOS_MaxDD=so["MaxDD"],
                        base_Sharpe=bm["Sharpe"], base_H1=b1, base_H2=b2, base_MaxDD=bm["MaxDD"],
                        base_OOS_Sharpe=bo["Sharpe"], base_OOS_CAGR=bo["CAGR"],
                        base_OOS_MaxDD=bo["MaxDD"]))
    return pd.DataFrame(rows)


def price_pairs(grid):
    """R for every adjacent cadence pair, holding panel/n/gross fixed."""
    rows = []
    for (p, n, g), sub in grid.groupby(["panel", "n", "gross"]):
        s = sub.set_index("cadence")
        for fast, slow in PAIRS:
            if fast not in s.index or slow not in s.index:
                continue
            dH2 = s.loc[slow, "H2_margin"] - s.loc[fast, "H2_margin"]
            dDD = s.loc[slow, "DD_margin"] - s.loc[fast, "DD_margin"]
            rows.append(dict(panel=p, n=n, gross=g, pair=f"{fast}->{slow}",
                             dH2=dH2, dDD=dDD,
                             R=dH2 / dDD if abs(dDD) > 1e-9 else np.nan,
                             R_x_gross=(dH2 / dDD) * g if abs(dDD) > 1e-9 else np.nan,
                             dturn=s.loc[slow, "turn_yr"] - s.loc[fast, "turn_yr"],
                             fast_H2m=s.loc[fast, "H2_margin"], fast_DDm=s.loc[fast, "DD_margin"],
                             slow_H2m=s.loc[slow, "H2_margin"], slow_DDm=s.loc[slow, "DD_margin"],
                             fast_4b=s.loc[fast, "pass4b"], slow_4b=s.loc[slow, "pass4b"]))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- [B] archival census
CAD_NAMES = {"cadence", "freq", "rebal", "exit_cadence", "pick_cadence", "gate_eval"}
METRIC_RE = re.compile(
    r"(CAGR|Sharpe|MaxDD|Calmar|Sortino|^DD|_DD|Vol$|^vol|^Turn|turn|^TO$|^T$|T_|H1|H2|OOS|"
    r"^IS$|IS_|pass|fail|keep|^v4|^p4|^m4|spy|base_|live_|breakeven|reproduces|published|"
    r"pub_|got_|margin|^d[A-Z]|regret|best|anchor|prereg|nogate|static_|gate_|grid|"
    r"flips|on_share|mean_mult|names|reb_per_yr|frac|ctl_|Gross$|^Total|WinRate|f_star|"
    r"gridmean|oosbest|^S[0-9]|dturn|Years)")


def census():
    """Price R on every committed grid CSV carrying a cadence column + H2 + MaxDD."""
    rows, files = [], 0
    for f in sorted(OUT.glob("*.csv")):
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        if d.empty:
            continue
        cad = next((c for c in d.columns if c in CAD_NAMES), None)
        if cad is None:
            continue
        h2 = next((c for c in ("H2", "H2_10", "Sharpe_H2") if c in d.columns), None)
        dd = next((c for c in ("MaxDD", "MaxDD_10") if c in d.columns), None)
        if h2 is None or dd is None:
            continue
        if d[cad].nunique() < 2:
            continue
        keys = [c for c in d.columns if c != cad and not METRIC_RE.search(c)]
        keys = [c for c in keys if d[c].notna().all()]
        # A key must actually GROUP.  Some files carry a REALISED quantity under a dial's name
        # (idea 329's `gross` is the measured mean gross, distinct on all 45 rows); grouping on
        # it fragments every group into singletons and silently drops the whole file.
        keys = [c for c in keys if d[c].nunique() <= max(2, len(d) // 3)]
        used = 0
        for _, sub in (d.groupby(keys, dropna=False) if keys else [((), d)]):
            sub = sub.dropna(subset=[h2, dd])
            if sub[cad].nunique() < 2:
                continue
            # Dropping a key column would merge non-comparable rows; a duplicated cadence inside
            # a group is exactly that signature, so the group is skipped rather than guessed at.
            if sub[cad].value_counts().max() > 1:
                continue
            s = sub.set_index(cad)
            cads = list(s.index)
            for i in range(len(cads)):
                for j in range(len(cads)):
                    if i >= j:
                        continue
                    a, b = cads[i], cads[j]
                    dH2 = s.loc[b, h2] - s.loc[a, h2]
                    dDD = -(abs(s.loc[b, dd]) - abs(s.loc[a, dd]))
                    if abs(dDD) < 5e-3:            # below this the ratio is noise/noise
                        continue
                    rows.append(dict(file=f.name, pair=f"{a}->{b}", dH2=dH2, dDD=dDD,
                                     R=dH2 / dDD,
                                     keys=",".join(keys),
                                     key=";".join(f"{k}={s.loc[b, k]}" for k in keys if k in s.columns)))
                    used += 1
        if used:
            files += 1
    out = pd.DataFrame(rows)
    print(f"    census: {files} committed grid CSVs carry a cadence dial with H2 and MaxDD; "
          f"{len(out)} cadence pairs priced (|dDDmargin| >= 0.005)")
    return out


# ---------------------------------------------------------------- [C] usability
def quadrants(df):
    """The SIGN structure behind R.  An 'exchange rate' presupposes a trade-off: slowing down
    must buy H2 and pay DD (dH2 > 0, dDDmargin < 0 -- idea 329's quadrant).  R is a ratio of two
    differences and explodes when its denominator is near zero, so the sign census is the
    scale-free reading and the R spread is reported both raw and with a denominator guard."""
    q = pd.Series(np.select(
        [(df.dH2 > 0) & (df.dDD < 0), (df.dH2 > 0) & (df.dDD > 0),
         (df.dH2 < 0) & (df.dDD < 0), (df.dH2 < 0) & (df.dDD > 0)],
        ["TRADE-OFF (buy H2, pay DD)", "FREE LUNCH (buy both)",
         "STRICTLY WORSE (lose both)", "REVERSE (lose H2, buy DD)"], default="degenerate"),
        index=df.index)
    return q


def usability(pairs):
    """Can ONE weekly cell + a constant R call the monthly 4b outcome?

    Prediction, from the WEEKLY cell alone: cadence can close the H2 bar without breaking the
    DD cap iff   DDmargin_W - |H2deficit_W / R| > 0,  where H2deficit_W = max(0, -H2margin_W).
    R is LEAVE-ONE-PANEL-OUT (median R of the W->M pairs on the other two panels), so no panel
    ever contributes to the constant used to predict it.

    Two CONTROLS decide whether R is doing any work at all:
      FREE  -- R = infinity, i.e. the DD cost of closing H2 is assumed zero: predict on
               DDmargin_W > 0 alone, no exchange rate anywhere in the rule;
      R329  -- the single number the queue proposes to generalise, -3.217, held fixed.
    If FREE scores as well as the leave-one-out constant, the constant is decoration."""
    wm = pairs[pairs.pair == "W->M"].copy()
    preds = []
    for _, r in wm.iterrows():
        others = wm[(wm.panel != r.panel) & wm.R.notna() & np.isfinite(wm.R)]
        Rloo = float(others.R.median()) if len(others) else np.nan
        deficit = max(0.0, -r.fast_H2m)
        cost = abs(deficit / Rloo) if Rloo and not np.isnan(Rloo) and Rloo != 0 else np.nan
        pred = bool(r.fast_DDm - cost > 0)
        pred_free = bool(r.fast_DDm > 0)
        pred_329 = bool(r.fast_DDm - abs(deficit / -3.217) > 0)
        # the observed monthly cell: did BOTH bars in fact hold?
        actual = bool(r.slow_H2m > 0 and r.slow_DDm > 0)
        preds.append(dict(panel=r.panel, n=r.n, gross=r.gross, R_loo=Rloo,
                          W_H2margin=r.fast_H2m, W_DDmargin=r.fast_DDm,
                          predicted_DD_cost=cost, predicted_M_ok=pred,
                          pred_FREE=pred_free, pred_R329=pred_329,
                          M_H2margin=r.slow_H2m, M_DDmargin=r.slow_DDm, actual_M_ok=actual,
                          correct=(pred == actual), correct_FREE=(pred_free == actual),
                          correct_R329=(pred_329 == actual)))
    return pd.DataFrame(preds)


# ---------------------------------------------------------------- [D] rule 8
def walkforward(grid, panels):
    rows = []
    for pname, px in panels.items():
        sub = grid[(grid.panel == pname) & (grid.gross == ANCHOR_G)]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        anchor = sub[(sub.n == ANCHOR_N) & (sub.cadence == ANCHOR_CAD)].iloc[0]
        best = sub.loc[sub.OOS_Sharpe.idxmax()]
        rows.append(dict(
            panel=pname, pick_n=int(pick.n), pick_cadence=pick.cadence, gross=ANCHOR_G,
            IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
            OOS_MaxDD=pick.OOS_MaxDD,
            anchor_n=ANCHOR_N, anchor_cadence=ANCHOR_CAD, anchor_OOS_Sharpe=anchor.OOS_Sharpe,
            anchor_OOS_CAGR=anchor.OOS_CAGR, anchor_OOS_MaxDD=anchor.OOS_MaxDD,
            best_OOS_Sharpe=best.OOS_Sharpe, best_n=int(best.n), best_cadence=best.cadence,
            regret=best.OOS_Sharpe - pick.OOS_Sharpe,
            grid_mean_OOS=sub.OOS_Sharpe.mean(),
            base_OOS_Sharpe=pick.base_OOS_Sharpe, base_OOS_CAGR=pick.base_OOS_CAGR,
            base_OOS_MaxDD=pick.base_OOS_MaxDD,
            spy_OOS_Sharpe=pick.spy_OOS_Sharpe, spy_OOS_CAGR=pick.spy_OOS_CAGR,
            spy_OOS_MaxDD=pick.spy_OOS_MaxDD,
            full_pass4b=bool(pick.pass4b), full_fail4b=pick.fail4b,
            full_pass4a=bool(pick.pass4a), full_fail4a=pick.fail4a))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print("Book: top-n eligible by the v1 composite (vol scaler OFF), NORM weights g/k_t, "
          "next-day execution, 10 bps.")
    print(f"Tuned: n in {NS} x cadence in {CADENCES}.  Reported axes: gross {GROSSES}, panel.")
    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL484": small_panel()}

    gates(panels)

    print("\n[A] FRESH CORPUS (108 books, every point printed)")
    gcsv = OUT / f"{SLUG}.grid.csv"
    if RESUME and gcsv.exists():
        print("    RESUME=1: re-reading the committed grid CSV")
        grid = pd.read_csv(gcsv)
    else:
        grid = build_grid(panels)
        grid.to_csv(gcsv, index=False)
    cols = ["panel", "n", "gross", "cadence", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "turn_yr", "H2_margin", "DD_margin", "pass4b", "fail4b", "pass4a"]
    print(grid[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n    4b passes: {int(grid.pass4b.sum())}/{len(grid)}   "
          f"4a passes: {int(grid.pass4a.sum())}/{len(grid)}")

    print("\n[A2] THE EXCHANGE RATE R = d(H2 margin)/d(DD margin), every cadence pair")
    pairs = price_pairs(grid)
    pairs.to_csv(OUT / f"{SLUG}.pairs.csv", index=False)
    print(pairs.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    fin = pairs[pairs.R.notna() & np.isfinite(pairs.R)]

    print("\n    SIGN CENSUS -- is the move even a trade-off?  (an exchange rate presupposes one)")
    q = quadrants(fin)
    vc = q.value_counts()
    for k, v in vc.items():
        print(f"      {k:<28} {v:3d}/{len(fin)} = {v/len(fin):6.1%}")
    print("    by pair type:")
    print(pd.crosstab(fin.pair, q).to_string())
    print("    by panel:")
    print(pd.crosstab(fin.panel, q).to_string())

    guard = fin[fin.dDD.abs() >= 0.01]
    print(f"\n    DENOMINATOR GUARD |dDDmargin| >= 0.01 keeps {len(guard)}/{len(fin)} pairs: "
          f"median R {guard.R.median():+.3f}  IQR [{guard.R.quantile(.25):+.3f}, "
          f"{guard.R.quantile(.75):+.3f}]  min {guard.R.min():+.3f}  max {guard.R.max():+.3f}  "
          f"spread {guard.R.max()-guard.R.min():.3f}")

    print(f"\n    ALL pairs: n={len(fin)}  median R {fin.R.median():+.3f}  "
          f"IQR [{fin.R.quantile(.25):+.3f}, {fin.R.quantile(.75):+.3f}]  "
          f"min {fin.R.min():+.3f}  max {fin.R.max():+.3f}  sign-negative "
          f"{int((fin.R < 0).sum())}/{len(fin)}")
    for ax in ("panel", "n", "gross", "pair"):
        g = fin.groupby(ax).R.agg(["count", "median", "min", "max"])
        g["spread"] = g["max"] - g["min"]
        print(f"\n    R by {ax}:\n" + g.to_string(float_format=lambda x: f"{x:.3f}"))
    gg = fin.groupby("gross").R_x_gross.agg(["count", "median", "min", "max"])
    gg["spread"] = gg["max"] - gg["min"]
    print("\n    R x gross (the gross-normalised candidate invariant) by gross:\n" +
          gg.to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"    R x gross overall: median {fin.R_x_gross.median():+.3f}  "
          f"IQR [{fin.R_x_gross.quantile(.25):+.3f}, {fin.R_x_gross.quantile(.75):+.3f}]  "
          f"spread {fin.R_x_gross.max()-fin.R_x_gross.min():.3f}")
    wm = fin[fin.pair == "W->M"]
    print(f"    idea 329's own pair type (W->M): n={len(wm)} median {wm.R.median():+.3f} "
          f"range [{wm.R.min():+.3f}, {wm.R.max():+.3f}]  (idea 329 read -3.217)")

    print("\n[B] ARCHIVAL CENSUS over the committed record")
    cen = census()
    if len(cen):
        cen.to_csv(OUT / f"{SLUG}.census.csv", index=False)
        c = cen[np.isfinite(cen.R)]
        cq = quadrants(c)
        print("    SIGN CENSUS over the archive:")
        for k, v in cq.value_counts().items():
            print(f"      {k:<28} {v:5d}/{len(c)} = {v/len(c):6.1%}")
        cg = c[c.dDD.abs() >= 0.01]
        print(f"    denominator guard |dDDmargin| >= 0.01 keeps {len(cg)}/{len(c)}: median R "
              f"{cg.R.median():+.3f}  IQR [{cg.R.quantile(.25):+.3f}, {cg.R.quantile(.75):+.3f}]  "
              f"min {cg.R.min():+.3f}  max {cg.R.max():+.3f}")
        print(f"    R: median {c.R.median():+.3f}  IQR [{c.R.quantile(.25):+.3f}, "
              f"{c.R.quantile(.75):+.3f}]  10-90 pct [{c.R.quantile(.10):+.3f}, "
              f"{c.R.quantile(.90):+.3f}]  min {c.R.min():+.3f}  max {c.R.max():+.3f}")
        print(f"    sign: negative {int((c.R<0).sum())}/{len(c)} = {(c.R<0).mean():.1%} "
              f"(a constant would be 100% one sign)")
        print(f"    within +/-20% of idea 329's -3.217: "
              f"{int(((c.R>-3.86)&(c.R<-2.57)).sum())}/{len(c)} = "
              f"{((c.R>-3.86)&(c.R<-2.57)).mean():.1%}")
        top = cen.groupby("file").R.agg(["count", "median", "min", "max"]).sort_values("count",
                                                                                       ascending=False)
        print("\n    per-file R (all files):\n" + top.to_string(float_format=lambda x: f"{x:.3f}"))
        own = cen[cen.file.str.contains("does-the-BAND-rescue-the-B136-H2-bar")]
        print(f"\n    self-check, idea 329's own file: {len(own)} pairs, "
              f"R range [{own.R.min():+.3f}, {own.R.max():+.3f}]")

    print("\n[C] IS THE CONSTANT USABLE? (leave-one-panel-out R, W cell -> M outcome)")
    us = usability(pairs)
    us.to_csv(OUT / f"{SLUG}.usability.csv", index=False)
    print(us.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    acc = us.correct.mean()
    base_rate = max(us.actual_M_ok.mean(), 1 - us.actual_M_ok.mean())
    print(f"\n    leave-one-panel-out R : accuracy {acc:.1%} ({int(us.correct.sum())}/{len(us)})")
    print(f"    CONTROL  R = infinity : accuracy {us.correct_FREE.mean():.1%} "
          f"({int(us.correct_FREE.sum())}/{len(us)})   [no exchange rate in the rule at all]")
    print(f"    CONTROL  R = -3.217   : accuracy {us.correct_R329.mean():.1%} "
          f"({int(us.correct_R329.sum())}/{len(us)})   [idea 329's number held fixed]")
    print(f"    majority-class baseline {base_rate:.1%}  ->  edge of the fitted R "
          f"{acc-base_rate:+.1%}, of the R-free control {us.correct_FREE.mean()-base_rate:+.1%}")
    tp = int(((us.predicted_M_ok) & (us.actual_M_ok)).sum())
    fp = int(((us.predicted_M_ok) & (~us.actual_M_ok)).sum())
    fn = int(((~us.predicted_M_ok) & (us.actual_M_ok)).sum())
    tn = int(((~us.predicted_M_ok) & (~us.actual_M_ok)).sum())
    print(f"    confusion  TP {tp}  FP {fp}  FN {fn}  TN {tn}")

    print("\n[D] RULE 8 WALK-FORWARD (choose n x cadence on <=2016 at gross 0.75, read 2017+ once)")
    wf = walkforward(grid, panels)
    wf.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n[VERDICT INPUTS]")
    print(f"    fresh-corpus R spread: {fin.R.min():+.3f} .. {fin.R.max():+.3f} "
          f"({fin.R.max()-fin.R.min():.3f} wide, median {fin.R.median():+.3f})")
    if len(cen):
        print(f"    archival R spread:     {c.R.min():+.3f} .. {c.R.max():+.3f} "
              f"({c.R.max()-c.R.min():.3f} wide, median {c.R.median():+.3f})")
    print(f"    trade-off quadrant share (fresh): "
          f"{(q == 'TRADE-OFF (buy H2, pay DD)').mean():.1%}")
    print(f"    usability: fitted-R {acc:.1%} vs R-free control {us.correct_FREE.mean():.1%} "
          f"vs majority class {base_rate:.1%}")
    print(f"    4b passes in the fresh corpus: {int(grid.pass4b.sum())}/{len(grid)}; "
          f"4a passes: {int(grid.pass4a.sum())}/{len(grid)}")


if __name__ == "__main__":
    main()

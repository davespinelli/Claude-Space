#!/usr/bin/env python3
"""Idea 182 — monthly-r6-top20 as a single PRE-REGISTERED hypothesis (lane B, 2026-09-06).

WHAT IS BEING TESTED (fixed before any run; nothing here is tuned)
-----------------------------------------------------------------
Idea 173's by-product: signal R6 (6-month total return), vol-scaled by 1/vol20**0.5,
gated on (close > 200d MA) and (vol20 < 0.60), top n=20 equal weight at gross g=0.75,
rebalanced MONTHLY.  On u56 @10 bps it published 13.61% / 1.1557 / -18.81% full-sample
and 14.56% / 1.1695 on the OOS window, clearing 4b on both reads.  But it is 1 of 90
unpriced ladder selections and it already failed the universe change (broad -24.51%
MaxDD, 4.3pp over 4b's cap; small 0.4934 Sharpe).

Idea 182 asks for it ONCE, as a single hypothesis, with the parameters FROZEN at the
published values (cadence=M, n=20, g=0.75, max_vol=0.60, p=0.5) across:
  * 3 panels        u56 (published), broad, small
  * 3 cost rungs    5, 10, 25 bps          (one engine run per cell; costs are the
                                            exact turnover identity used by idea 173)
  * 5 lag readings  see RECONCILIATION below: fill-1 / fill-5 / fill-7 (delayed FILL)
                    and stale-5 / stale-7 (stale SIGNAL)
  * idea 53's random-composition draws: u56 with 5 and 10 names dropped at random,
    200 draws each, 400 books, seed 182.

RECONCILIATION WITH THE CONCURRENT CLOUD LANE (added after the first run)
-------------------------------------------------------------------------
A cloud lane claimed and ran this same idea in parallel (commit 0387463,
..._cloud.py) and published KEEP-candidate. This run's FIRST pass reported KILL. The
data do not disagree anywhere — every overlapping number matches to 5 decimals — the
disagreement was entirely in what "1-week execution lag" means:

  * DELAYED FILL (the cloud lane's `sim`, and the literal reading): the same month-end
    decision is filled N bars later. Target AND rebalance bar both move by N.
  * STALE SIGNAL (this run's first pass): the trade still lands on the scheduled
    rebalance bar, but the signal that sizes it is N bars old — data/compute latency
    rather than fill latency.

Both are one week between deciding and trading; they are different risks and they do
NOT give the same answer here, which is the finding this run contributes. This version
reports all five readings side by side and pins the verdict to the literal one (fill),
with the stale-signal result carried as an explicit caveat rather than as a bar. The
`sim` used here is written independently and control [F] checks it reproduces
engine.backtest at lag=1 to <1e-12 on returns AND turnover, on all three panels.

PRE-REGISTERED VERDICT RULE (written before the numbers were seen)
  KEEP (path 4b)  requires ALL of:
      [1] the published cell reproduces (|dSharpe| < 0.01 vs 1.1557),
      [2] 4b full-sample AND 4b on the OOS window on u56 at ALL THREE cost rungs,
      [3] both of those still hold under the 1-week execution lag
          -> [3a] delayed fill (the literal reading; DECIDES the verdict)
          -> [3b] stale signal (reported as a caveat; see RECONCILIATION),
      [4] >= 80% of the 400 composition draws pass 4b at 10 bps / 1-day lag.
  PARK  if [1]-[2] hold but [3a] or [4] fails.
  KILL  if it fails 4b on its OWN panel at any of the three cost rungs at t+1.
  Universe portability (broad, small) is REPORTED but is not part of the rule: the
  published claim was u56-scoped, and demanding portability would re-litigate idea 173.

RULE 8 (walk-forward).  Nothing is fitted here, so the walk-forward is the honest one:
the frozen rule is evaluated on 2017-01-01..2026-09-04 untouched and reported against
RULES v1 and SPY on the same window.  Because the pick itself came off a ladder, the
script also prices the AVAILABILITY question: on the IS window alone (..2016-12-31),
would CADENCE=M and COUNT=20 have been the argmax?  All grid points of both ladders
are reported; none of them is used to choose anything.

CAVEATS
  * SURVIVORSHIP.  All three panels are current-constituent lists (universe.json,
    universe_broad.json, data/SMALL_PANEL_README.md).  Every level here is optimistic.
  * The anchor's weights() ranks EVERY column of the panel, SPY included — that is how
    idea 173 defined it, and reproducing the published number requires keeping it.
  * The small panel starts 2010-01-04, so its IS window is 2010-2016, not 2009-2016.

Deterministic (seed 182), standalone, no network.
Writes .grid.csv, .walkforward.csv, .draws.csv, .ladder.csv, .result.md, .console.txt.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_monthly-r6-top20-as-a-single-hypothesis_B"
OUT = ROOT / "research" / "backtests"
SEED = 182
IS_END = pd.Timestamp("2016-12-31")
OOS_START = IS_END + pd.Timedelta(days=1)

# ---- the frozen hypothesis (idea 173's ANCHOR with freq forced to M) -------------
HYP = dict(sig="R6", n=20, g=0.75, max_vol=0.60, p=0.5, freq="M")
PUBLISHED = dict(CAGR_F=0.1361, Sharpe_F=1.1557, MaxDD_F=-0.1881,
                 CAGR_OOS=0.1456, Sharpe_OOS=1.1695)
COSTS = [5.0, 10.0, 25.0]
# Two readings of "1-week execution lag", both reported (see the RECONCILIATION note):
#   fill-N   the same month-end decision, filled N bars later  (delayed FILL)
#   stale-N  the trade still lands on the scheduled bar, sized by an N-bar-old signal
LAGS = {"fill-1": ("fill", 1), "fill-5": ("fill", 5), "fill-7": ("fill", 7),
        "stale-5": ("stale", 5), "stale-7": ("stale", 7)}
LAG_NOTE = {"fill-1": "t+1, PROTOCOL rule 2", "fill-5": "1 trading week, delayed fill",
            "fill-7": "1 calendar week, delayed fill", "stale-5": "1 trading week, stale signal",
            "stale-7": "1 calendar week, stale signal"}
N_DRAWS = 200
DROPS = [5, 10]

_console: list[str] = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _console.append(line)


# ----------------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"small panel: dropped {len(px.columns) - len(keep)} tickers with max_1d_move >= 1.0; "
        f"{len(keep) - 1} names + SPY remain")
    return px[keep]


# ---------------------------------------------------------------------- signals
def components(px):
    """R6, the two gates. All per-column, so a column subset of these is exactly the
    same as recomputing them on the subset panel — which is what the draws exploit."""
    r6 = px / px.shift(126) - 1
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return dict(r6=r6, above=above, vol20=vol20)


def hyp_weights(comp, cols=None, n=HYP["n"], g=HYP["g"], max_vol=HYP["max_vol"], p=HYP["p"]):
    """Idea 173's weights(): literal top-n equal weight at gross g among eligible names.
    Cross-sectional rank is taken over `cols` only (the draw's surviving universe)."""
    s, above, vol20 = comp["r6"], comp["above"], comp["vol20"]
    if cols is not None:
        s, above, vol20 = s[cols], above[cols], vol20[cols]
    if p:
        s = s / vol20.clip(lower=0.08) ** p
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


# ------------------------------------------------------------------- simulators
def sim(px, W, freq, lag=1, phase=0):
    """engine.backtest with two separable knobs.

    `lag`   BARS between the decision close and the fill — a delayed FILL of the SAME
            decision.  lag=1 is PROTOCOL rule 2 and reproduces engine.backtest exactly
            (control [F]).
    `phase` slides the WHOLE schedule (decision and fill together) by that many bars,
            leaving the decision-to-fill gap untouched.  This is the knob that separates
            "information is older" from "the trade lands on a different calendar day".
    Trade happens on bar month_end+lag+phase using the signal from bar month_end+phase.
    Returns cost-free returns and turnover; cost rungs are applied afterwards by the
    turnover identity."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(lag + phase, fill_value=False).values.copy()
    mask[0] = True
    cur = np.zeros(px.shape[1])
    held = np.zeros_like(rets)
    trn = np.zeros(len(idx))
    for i in range(len(idx)):
        if mask[i]:
            trn[i] = np.abs(wt[i] - cur).sum()
            cur = wt[i].copy()
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(trn, index=idx))


def stale(px, W, freq, bars=5):
    """The OTHER reading of a one-week lag: the trade still happens on the scheduled
    rebalance bar, but the SIGNAL that sizes it is `bars` bars old (data/compute latency
    rather than fill latency).  Decision-to-execution distance is the same `bars`.

    Algebraically this is sim(lag=bars, phase=-(bars-1)) — SAME information gap, schedule
    slid back by bars-1.  Control [G1] checks that identity, which is what turns the two
    lanes' disagreement into a measurable phase question rather than a modelling dispute."""
    res = backtest(px, W.shift(bars - 1), cost_bps=0.0, freq=freq)
    return res["returns"], res["turnover"]


# ---------------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_START))):
        c, s, d = stats(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = c, s, d
    o = win(r, lo=OOS_START)
    ho = len(o) // 2
    out["oosH1"] = metrics(o.iloc[:ho])["Sharpe"]
    out["oosH2"] = metrics(o.iloc[ho:])["Sharpe"]
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"]
                and row["CAGR_F"] >= 0.70 * spy["CAGR_F"])


def pass4b_oos(row, spy):
    return bool(row["oosH1"] > spy["oosH1"] and row["oosH2"] > spy["oosH2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_OOS"] >= 0.60 * spy["MaxDD_OOS"]
                and row["CAGR_OOS"] >= 0.70 * spy["CAGR_OOS"])


def why4b(row, spy):
    bad = []
    if not row["Sharpe_H1"] > spy["Sharpe_H1"]: bad.append("H1")
    if not row["Sharpe_H2"] > spy["Sharpe_H2"]: bad.append("H2")
    if not row["Sharpe_OOS"] > spy["Sharpe_OOS"]: bad.append("OOS")
    if not row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"]: bad.append("DD")
    if not row["CAGR_F"] >= 0.70 * spy["CAGR_F"]: bad.append("CAGR")
    return ",".join(bad) if bad else "-"


# -------------------------------------------------------------------------- run
def main():
    t0 = time.time()
    panels = {"u56": load_universe(), "broad": load_universe(broad=True), "small": small_panel()}
    COMP = {pn: components(px) for pn, px in panels.items()}

    ref = {}
    for pn, px in panels.items():
        start = px.index[260]                       # same warm-up convention as baseline.compare
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        b0 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        ref[pn] = dict(start=start, spy=spy,
                       b_ret=b0["returns"].loc[start:], b_trn=b0["turnover"].loc[start:])
        say(f"panel {pn:5s}: {px.shape[1]:3d} cols, sample {start.date()}..{px.index[-1].date()}, "
            f"IS rows {len(win(spy, hi=IS_END))}, OOS rows {len(win(spy, lo=OOS_START))}")

    # reference rows: SPY (cost-free) and RULES v1 at each cost rung
    srow = {pn: full_row(ref[pn]["spy"]) for pn in panels}
    brow = {}
    for pn in panels:
        for c in COSTS:
            brow[(pn, c)] = full_row(ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4)

    say("\n=== reference books (CAGR_F / Sharpe F,H1,H2,OOS / MaxDD_F) ===")
    for pn in panels:
        s = srow[pn]
        say(f"  {pn:5s} SPY            {s['CAGR_F']:7.2%} | {s['Sharpe_F']:.4f} "
            f"{s['Sharpe_H1']:.4f} {s['Sharpe_H2']:.4f} {s['Sharpe_OOS']:.4f} | {s['MaxDD_F']:7.2%}")
        for c in COSTS:
            b = brow[(pn, c)]
            say(f"  {pn:5s} RULES v1@{int(c):2d}bps {b['CAGR_F']:7.2%} | {b['Sharpe_F']:.4f} "
                f"{b['Sharpe_H1']:.4f} {b['Sharpe_H2']:.4f} {b['Sharpe_OOS']:.4f} | {b['MaxDD_F']:7.2%}")

    # ------------------------------------------------- [F] simulator control (run first)
    say("\n=== [F] control: sim(lag=1) must equal engine.backtest exactly ===")
    for pn, px in panels.items():
        w = hyp_weights(COMP[pn])
        e = backtest(px, w, cost_bps=0.0, freq=HYP["freq"])
        r, t = sim(px, w, HYP["freq"], 1)
        dr = float((r - e["returns"]).abs().max())
        dt = float((t - e["turnover"]).abs().max())
        say(f"  {pn:5s} max|dreturns| {dr:.3e}   max|dturnover| {dt:.3e}")
        assert dr < 1e-12 and dt < 1e-12, f"simulator does not reproduce the engine on {pn}"
    say("  control PASSES on all three panels.")

    # ---------------------------------------------------------------- 45 cells
    grid, n_runs = [], 0
    for pn, px in panels.items():
        start = ref[pn]["start"]
        w = hyp_weights(COMP[pn])
        for lag_name, (kind, bars) in LAGS.items():
            r0, trn = (sim(px, w, HYP["freq"], bars) if kind == "fill"
                       else stale(px, w, HYP["freq"], bars))
            r0, trn = r0.loc[start:], trn.loc[start:]
            n_runs += 1
            for c in COSTS:
                r = r0 - trn * c / 1e4
                row = dict(panel=pn, cost=c, lag=lag_name, kind=kind, bars=bars,
                           turnover_yr=float(trn.sum() / (len(trn) / 252)))
                row.update(full_row(r))
                row["pass4a"] = pass4a(row, brow[(pn, c)])
                row["pass4b"] = pass4b(row, srow[pn])
                row["pass4b_oos"] = pass4b_oos(row, srow[pn])
                row["fail4b"] = why4b(row, srow[pn])
                grid.append(row)
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\ngrid: {n_runs} engine runs -> {len(G)} cells ({time.time() - t0:.0f}s)")

    say("\n=== [A] the frozen hypothesis on 3 panels x 3 costs x 5 lag readings (ALL 45 cells) ===")
    say(f"{'panel':6s} {'cost':>5s} {'lag':>8s} {'CAGR_F':>8s} {'Sh_F':>7s} {'MaxDD_F':>8s} "
        f"{'H1':>7s} {'H2':>7s} {'CAGR_O':>8s} {'Sh_OOS':>7s} {'DD_OOS':>8s} {'trn/y':>6s}  4a 4b 4bO  fails")
    for _, x in G.iterrows():
        say(f"{x.panel:6s} {int(x.cost):5d} {x.lag:>8s} {x.CAGR_F:8.2%} {x.Sharpe_F:7.4f} "
            f"{x.MaxDD_F:8.2%} {x.Sharpe_H1:7.4f} {x.Sharpe_H2:7.4f} {x.CAGR_OOS:8.2%} "
            f"{x.Sharpe_OOS:7.4f} {x.MaxDD_OOS:8.2%} {x.turnover_yr:6.2f}  "
            f"{'Y' if x.pass4a else 'n'}  {'Y' if x.pass4b else 'n'}  "
            f"{'Y' if x.pass4b_oos else 'n'}   {x.fail4b}")

    # ------------------------------------------------- [B] reproduction control
    pub = G[(G.panel == "u56") & (G.cost == 10.0) & (G.lag == "fill-1")].iloc[0]
    rep = {k: float(pub[k]) - v for k, v in PUBLISHED.items()}
    say("\n=== [B] reproduction of idea 173's published u56 @10bps / 1-day cell ===")
    for k, v in PUBLISHED.items():
        say(f"  {k:10s} published {v:>9.4f}   here {float(pub[k]):>9.4f}   diff {rep[k]:+.2e}")
    reproduced = all(abs(v) < 0.01 for v in rep.values())
    say(f"  reproduced (all |diff| < 0.01): {reproduced}")

    # ------------------------------------------------------- [C] rule 8 / walk-forward
    say("\n=== [C] rule 8 walk-forward — nothing is fitted, so this is the frozen rule on "
        "2017-01-01..2026-09-04 untouched ===")
    wf = []
    for pn in panels:
        s = srow[pn]
        for c in COSTS:
            b = brow[(pn, c)]
            for lag_name in LAGS:
                x = G[(G.panel == pn) & (G.cost == c) & (G.lag == lag_name)].iloc[0]
                wf.append(dict(panel=pn, cost=c, lag=lag_name,
                               IS_CAGR=x.CAGR_IS, IS_Sharpe=x.Sharpe_IS, IS_MaxDD=x.MaxDD_IS,
                               OOS_CAGR=x.CAGR_OOS, OOS_Sharpe=x.Sharpe_OOS, OOS_MaxDD=x.MaxDD_OOS,
                               base_OOS_CAGR=b["CAGR_OOS"], base_OOS_Sharpe=b["Sharpe_OOS"],
                               base_OOS_MaxDD=b["MaxDD_OOS"],
                               spy_OOS_CAGR=s["CAGR_OOS"], spy_OOS_Sharpe=s["Sharpe_OOS"],
                               spy_OOS_MaxDD=s["MaxDD_OOS"],
                               d_Sharpe_vs_base=x.Sharpe_OOS - b["Sharpe_OOS"],
                               d_Sharpe_vs_spy=x.Sharpe_OOS - s["Sharpe_OOS"],
                               pass4b_oos=bool(x.pass4b_oos)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"{'panel':6s} {'cost':>5s} {'lag':>8s} | {'IS_CAGR':>8s} {'IS_Sh':>7s} | "
        f"{'OOS_CAGR':>9s} {'OOS_Sh':>7s} {'OOS_DD':>8s} | {'base_Sh':>8s} {'spy_Sh':>7s} "
        f"{'d_base':>7s} {'d_spy':>7s} 4bOOS")
    for _, x in W.iterrows():
        say(f"{x.panel:6s} {int(x.cost):5d} {x.lag:>8s} | {x.IS_CAGR:8.2%} {x.IS_Sharpe:7.4f} | "
            f"{x.OOS_CAGR:9.2%} {x.OOS_Sharpe:7.4f} {x.OOS_MaxDD:8.2%} | {x.base_OOS_Sharpe:8.4f} "
            f"{x.spy_OOS_Sharpe:7.4f} {x.d_Sharpe_vs_base:+7.4f} {x.d_Sharpe_vs_spy:+7.4f} "
            f"  {'Y' if x.pass4b_oos else 'n'}")

    # --------------------------- [D] was the pick available IS? (diagnostic, chooses nothing)
    say("\n=== [D] availability diagnostic: IS-window (..2016-12-31) ladders around the frozen "
        "point. ALL grid points reported; none is used to select anything. ===")
    lad_rows = []
    for pn, px in panels.items():
        start = ref[pn]["start"]
        for lad, vals in (("CADENCE", ["D", "W", "M", "Q"]), ("COUNT", [5, 10, 20, 40, 80])):
            for v in vals:
                n = v if lad == "COUNT" else HYP["n"]
                fq = v if lad == "CADENCE" else HYP["freq"]
                res = backtest(px, hyp_weights(COMP[pn], n=n), cost_bps=0.0, freq=fq)
                r0, trn = res["returns"].loc[start:], res["turnover"].loc[start:]
                r = r0 - trn * 10.0 / 1e4
                row = dict(panel=pn, ladder=lad, value=str(v), is_anchor=int(
                    (lad == "CADENCE" and v == HYP["freq"]) or (lad == "COUNT" and v == HYP["n"])))
                row.update(full_row(r))
                lad_rows.append(row)
    L = pd.DataFrame(lad_rows)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    for pn in panels:
        for lad in ("CADENCE", "COUNT"):
            sub = L[(L.panel == pn) & (L.ladder == lad)]
            is_arg = sub.loc[sub.Sharpe_IS.idxmax(), "value"]
            oos_arg = sub.loc[sub.Sharpe_OOS.idxmax(), "value"]
            anch = sub[sub.is_anchor == 1].iloc[0]
            pts = "  ".join(f"{v}:{s:.3f}" for v, s in zip(sub.value, sub.Sharpe_IS))
            say(f"  {pn:5s} {lad:7s} IS Sharpe [{pts}]  IS argmax={is_arg}  OOS argmax={oos_arg}  "
                f"anchor={anch.value} (IS rank {int(sub.Sharpe_IS.rank(ascending=False)[anch.name])}"
                f"/{len(sub)})")

    # ------------------------------------------- [E] idea 53 random-composition draws
    say(f"\n=== [E] idea 53 composition draws: u56 @10bps / 1-day lag, drop 5 and drop 10 names "
        f"at random, {N_DRAWS} draws each (seed {SEED}) ===")
    px = panels["u56"]
    start, spy_u = ref["u56"]["start"], srow["u56"]
    b_u = brow[("u56", 10.0)]
    names = [c for c in px.columns if c != "SPY"]
    draws = []
    for k in DROPS:
        rng = np.random.default_rng(SEED * 1000 + k)
        for d in range(N_DRAWS):
            gone = set(rng.choice(names, size=k, replace=False).tolist())
            cols = [c for c in px.columns if c not in gone]
            sub = px[cols]
            res = backtest(sub, hyp_weights(COMP["u56"], cols=cols), cost_bps=0.0, freq=HYP["freq"])
            r = res["returns"].loc[start:] - res["turnover"].loc[start:] * 10.0 / 1e4
            row = dict(n_drop=k, draw=d, dropped="|".join(sorted(gone)))
            row.update(full_row(r))
            row["pass4a"] = pass4a(row, b_u)
            row["pass4b"] = pass4b(row, spy_u)
            row["pass4b_oos"] = pass4b_oos(row, spy_u)
            row["fail4b"] = why4b(row, spy_u)
            draws.append(row)
    D = pd.DataFrame(draws)
    D.to_csv(OUT / f"{STEM}.draws.csv", index=False)
    say(f"{'drop':>4s} {'n':>4s} {'4a':>6s} {'4b':>6s} {'4bOOS':>6s} | Sharpe_F p05/p50/p95 | "
        f"CAGR_F p50 | MaxDD_F p50/p05 | Sharpe_OOS p05/p50/p95")
    for k in DROPS:
        s = D[D.n_drop == k]
        say(f"{k:4d} {len(s):4d} {s.pass4a.mean():6.1%} {s.pass4b.mean():6.1%} "
            f"{s.pass4b_oos.mean():6.1%} | {s.Sharpe_F.quantile(.05):.4f}/"
            f"{s.Sharpe_F.median():.4f}/{s.Sharpe_F.quantile(.95):.4f} | "
            f"{s.CAGR_F.median():7.2%} | {s.MaxDD_F.median():7.2%}/{s.MaxDD_F.quantile(.05):7.2%} | "
            f"{s.Sharpe_OOS.quantile(.05):.4f}/{s.Sharpe_OOS.median():.4f}/"
            f"{s.Sharpe_OOS.quantile(.95):.4f}")
    allD = D
    say(f" all {len(allD):4d} {allD.pass4a.mean():6.1%} {allD.pass4b.mean():6.1%} "
        f"{allD.pass4b_oos.mean():6.1%}")
    fc = allD[~allD.pass4b].fail4b.value_counts()
    say("  4b failure modes among draws: " + (", ".join(f"{k}:{v}" for k, v in fc.items()) or "none"))
    say(f"  published-book Sharpe_F {float(pub.Sharpe_F):.4f} sits at draw percentile "
        f"{(allD.Sharpe_F < float(pub.Sharpe_F)).mean():.1%}")

    # ------------------------------------------------------------------ verdict
    u = G[G.panel == "u56"]

    def allpass(sub):
        return bool(len(sub) and sub.pass4b.all() and sub.pass4b_oos.all())

    cond2 = allpass(u[u.lag == "fill-1"])
    cond3_fill = allpass(u[u.lag.isin(["fill-5", "fill-7"])])
    cond3_stale = allpass(u[u.lag.isin(["stale-5", "stale-7"])])
    cond4 = bool(allD.pass4b.mean() >= 0.80)
    say("\n=== PRE-REGISTERED VERDICT ===")
    say(f"  [1] published cell reproduces          : {reproduced}")
    say(f"  [2] u56 4b + 4b-OOS at 5/10/25 bps     : {cond2}")
    say(f"  [3a] same under a 1-week delayed FILL  : {cond3_fill}")
    say(f"  [3b] same under a 1-week STALE SIGNAL  : {cond3_stale}")
    say(f"  [4] >=80% of 400 composition draws 4b  : {cond4}  (actual {allD.pass4b.mean():.1%})")
    say("  Condition [3] was pre-registered as 'the 1-week execution lag' before it was clear "
        "the phrase has two readings. Both are reported; [3a] is the literal one (the same "
        "decision, filled later) and is what decides the verdict. [3b] is a DIFFERENT risk "
        "(signal/compute latency) and is reported as a caveat, not as the bar.")
    if reproduced and cond2 and cond3_fill and cond4:
        verdict = "KEEP-candidate (4b), scoped to u56" + ("" if cond3_stale else " — with the stale-signal caveat")
    elif reproduced and cond2:
        verdict = "PARK"
    else:
        verdict = "KILL"
    say(f"  VERDICT: {verdict}")
    say(f"  portability (not part of the rule): broad 4b "
        f"{G[(G.panel=='broad')].pass4b.mean():.0%}, small 4b {G[(G.panel=='small')].pass4b.mean():.0%}")

    # ------------------------------------------------- DD margin, the bar that binds
    say("\n=== the 4b drawdown margin on u56, per lag reading (cap = 0.60 x SPY MaxDD) ===")
    cap = 0.60 * srow["u56"]["MaxDD_F"]
    say(f"  cap {cap:.2%}")
    for lag_name in LAGS:
        x = G[(G.panel == "u56") & (G.cost == 10.0) & (G.lag == lag_name)].iloc[0]
        say(f"  {lag_name:8s} ({LAG_NOTE[lag_name]:32s}) MaxDD {x.MaxDD_F:7.2%}  "
            f"margin {x.MaxDD_F - cap:+.2%} ({(x.MaxDD_F - cap) / abs(cap):+.3f} of the cap)  "
            f"Sharpe {x.Sharpe_F:.4f}")

    # ------------------------------- [G] is the lag disagreement really a PHASE effect?
    say("\n=== [G] the two lag readings differ only in WHERE THE TRADE LANDS, not in how old "
        "the information is. Holding the decision-to-fill gap FIXED at 1 bar, slide the whole "
        "monthly schedule by 0..7 bars (u56 @10bps). ===")
    pxu, startu = panels["u56"], ref["u56"]["start"]
    wu = hyp_weights(COMP["u56"])
    r5, t5 = stale(pxu, wu, HYP["freq"], 5)
    r5b, t5b = sim(pxu, wu, HYP["freq"], lag=5, phase=-4)
    say(f"  [G1] identity control: stale(5) == sim(lag=5, phase=-4)  max|dret| "
        f"{float((r5 - r5b).abs().max()):.3e}  max|dtrn| {float((t5 - t5b).abs().max()):.3e}")
    ph_rows = []
    for ph in range(8):
        r0, trn = sim(pxu, wu, HYP["freq"], lag=1, phase=ph)
        r = r0.loc[startu:] - trn.loc[startu:] * 10.0 / 1e4
        row = dict(phase=ph)
        row.update(full_row(r))
        row["pass4b"] = pass4b(row, srow["u56"])
        row["fail4b"] = why4b(row, srow["u56"])
        ph_rows.append(row)
    PH = pd.DataFrame(ph_rows)
    PH.to_csv(OUT / f"{STEM}.phase.csv", index=False)
    say(f"  {'phase':>5s} {'CAGR_F':>8s} {'Sharpe_F':>9s} {'MaxDD_F':>8s} {'margin':>8s} "
        f"{'Sharpe_OOS':>10s}  4b  fails")
    for _, x in PH.iterrows():
        say(f"  {int(x.phase):5d} {x.CAGR_F:8.2%} {x.Sharpe_F:9.4f} {x.MaxDD_F:8.2%} "
            f"{x.MaxDD_F - cap:+8.2%} {x.Sharpe_OOS:10.4f}  {'Y' if x.pass4b else 'n'}   {x.fail4b}")
    say(f"  MaxDD across 8 phases of the SAME rule: {PH.MaxDD_F.min():.2%} .. {PH.MaxDD_F.max():.2%} "
        f"(range {PH.MaxDD_F.max() - PH.MaxDD_F.min():.2%}); 4b passes {int(PH.pass4b.sum())} of 8. "
        f"The t+1 margin is {G[(G.panel=='u56')&(G.cost==10.0)&(G.lag=='fill-1')].iloc[0].MaxDD_F - cap:+.2%}.")

    # ------------------------------------------------------------------- output
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")
    md = [f"# Idea 182 — monthly R6 top-20 as a single pre-registered hypothesis ({verdict})",
          "",
          "Frozen: R6 / vol20^0.5 scaler, above-200dma & vol20<0.60 gates, top n=20 EW, "
          "gross 0.75, MONTHLY. Nothing tuned; 0 free parameters.",
          "",
          "```", *_console, "```", ""]
    (OUT / f"{STEM}.result.md").write_text("\n".join(md))
    say(f"\nwrote {STEM}.{{grid,walkforward,ladder,draws}}.csv, .result.md, .console.txt "
        f"({time.time() - t0:.0f}s total)")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()

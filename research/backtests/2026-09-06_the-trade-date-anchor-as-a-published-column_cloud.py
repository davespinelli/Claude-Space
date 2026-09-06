#!/usr/bin/env python3
"""QUEUE idea 223 - the-trade-date-anchor-as-a-published-column   (cloud, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 223)
    "idea 182B found the identical monthly book spans 2.51pp of full-sample MaxDD over 8 of its
     ~21 possible month anchors at a FIXED decision-to-fill gap, enough to flip a 4b verdict,
     while the record treats a monthly rebalance as phase-free.  Price all ~21 anchors for the
     standing candidate on u56 AND broad, and report how many published monthly drawdown claims
     in LEADERBOARD.md have a margin narrower than their own anchor band.  Max 2 params."

WHAT AN "ANCHOR" IS HERE
    engine.rebalance_mask(freq="M") fires on the LAST trading bar of each calendar month, and
    engine.backtest fills one bar later (PROTOCOL rule 2).  An ANCHOR slides that whole schedule
    - decision bar AND fill bar together - by `phase` bars, leaving the decision-to-fill gap at
    exactly 1 bar.  phase=0 is the published month-end anchor; phase=p trades p bars later in the
    month.  A monthly rule on this panel has ~21 such anchors before the schedule wraps onto the
    next month's, so phases 0..20 enumerate the choice.  This is 182B's `sim(lag, phase)` knob,
    unmodified: control [B] reproduces its committed phase.csv exactly.

    An anchor is NOT a signal, a cadence or a lag.  Nothing about the book changes across the 21
    cells; only the calendar day the identical decision lands on.  Any spread across them is
    schedule noise that the record has never priced.

THE STANDING CANDIDATE (fixed, nothing tuned)
    signal   R6 = px/px.shift(126) - 1, divided by vol20.clip(0.08) ** 0.5
    gate     px > 200d MA  AND  vol20 < 0.60
    book     top 20 by signal among eligible, equal weight, gross 0.75 (cash otherwise)
    cadence  MONTHLY
    This is the config committed by idea 182/182B (13.61% / 1.1557 / -18.81% on u56 @10bps).

PARAMETERS (PROTOCOL rule 4, max 2)
    1. ANCHOR phase in 0..20        <- the object of the study
    2. rule-8 arm (how an anchor is chosen: CONST-0 / IS-PICK / ORACLE / MEAN)
    PANEL (u56, broad) and COST (10, 25 bps) are AUDIT AXES: every cell is reported, nothing is
    chosen for reporting.

DELIVERABLES
    D1  the 21-anchor band per (panel, cost): MaxDD / Sharpe / CAGR spread of the IDENTICAL rule,
        and the 4b and 4a pass count out of 21.
    D2  the LEADERBOARD back-fill: every published row whose cadence is monthly, its 4b drawdown
        margin, and how many of those margins are narrower than the anchor band measured in D1.
    D3  PROTOCOL rule 8 walk-forward on the anchor choice: phase chosen on <= 2016-12-31 only,
        read once on 2017-01-01.. , against RULES v1 and SPY over the same OOS window.
    Both KEEP paths (4a and 4b) are evaluated on every cell.

CAVEATS carried, not buried
    * SURVIVORSHIP.  universe.json and universe_broad.json are CURRENT-CONSTITUENT lists; no level
      here is an attainable return.  The anchor SPREAD is a within-panel differencing statistic and
      is far less exposed to that bias than the levels are.
    * The D2 margin needs a 4b drawdown cap, i.e. SPY's MaxDD over the row's own evaluation window,
      which LEADERBOARD.md does not record.  This script uses SPY's MaxDD over ITS OWN post-warm-up
      full sample as the cap for every row, and says so; rows evaluated on a different window carry
      a cap error that is NOT quantified here.  The count is therefore an estimate of exposure, not
      a re-adjudication of any row.
    * The cadence classifier over free-text leaderboard names is reported in TWO strictnesses
      (STRICT and WIDE) with its exact regexes printed, because "monthly" is not a committed column.
      That is the point of the idea.

Deterministic, standalone, no network.  Writes .console.txt, .anchors.csv, .claims.csv,
.walkforward.csv.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_the-trade-date-anchor-as-a-published-column_cloud"
PARENT = "2026-09-06_monthly-r6-top20-as-a-single-hypothesis_B"
OUT = ROOT / "research" / "backtests"

IS_END = pd.Timestamp("2016-12-31")
OOS_START = IS_END + pd.Timedelta(days=1)
PHI, DELTA = 0.70, 0.60

CFG = dict(sig="R6", n=20, g=0.75, max_vol=0.60, p=0.5, freq="M")
PHASES = list(range(21))
COSTS = [10.0, 25.0]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 200)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def flush():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


# ---------------------------------------------------------------- book (182B, verbatim)
_C = {}


def raw_signal(px):
    k = (id(px), "R6")
    if k not in _C:
        _C[k] = px / px.shift(126) - 1
    return _C[k]


def gates(px):
    k = (id(px), "g")
    if k not in _C:
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        _C[k] = (above, vol20)
    return _C[k]


def book_weights(px):
    s = raw_signal(px)
    above, vol20 = gates(px)
    s = s / vol20.clip(lower=0.08) ** CFG["p"]
    elig = s.where(above & (vol20 < CFG["max_vol"]))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= CFG["n"]).astype(float) * (CFG["g"] / CFG["n"])


# ---------------------------------------------------------------- simulator (182B sim, verbatim)
def sim(px, W, freq, lag=1, phase=0):
    """Decision bar and fill bar slide together by `phase`; the decision-to-fill gap stays `lag`."""
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


# ---------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def full_row(r):
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:len(r) // 2]), ("H2", r.iloc[len(r) // 2:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_START))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = m["CAGR"], m["Sharpe"], m["MaxDD"]
    return out


def fail4a(row, base):
    f = []
    if not row["Sharpe_H1"] > base["Sharpe_H1"]: f.append("H1")
    if not row["Sharpe_H2"] > base["Sharpe_H2"]: f.append("H2")
    if not row["MaxDD_F"] >= base["MaxDD_F"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail4b(row, spy):
    f = []
    if not row["Sharpe_H1"] > spy["Sharpe_H1"]: f.append("H1")
    if not row["Sharpe_H2"] > spy["Sharpe_H2"]: f.append("H2")
    if not row["Sharpe_OOS"] > spy["Sharpe_OOS"]: f.append("OOS")
    if not row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]: f.append("DD")
    if not row["CAGR_F"] >= PHI * spy["CAGR_F"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def dd_margin_pp(maxdd, spy_maxdd):
    """4b drawdown margin in PERCENTAGE POINTS: cap - |MaxDD|.  Positive = passes with room."""
    return (DELTA * abs(spy_maxdd) - abs(maxdd)) * 100.0


# ---------------------------------------------------------------- controls
def check_a(px):
    P("  [A] sim(lag=1, phase=0) == engine.backtest, and cost linearity via the turnover identity:")
    W = book_weights(px)
    e0 = backtest(px, W, cost_bps=0.0, freq=CFG["freq"])
    r0, t0 = sim(px, W, CFG["freq"], 1, 0)
    d1 = float((e0["returns"] - r0).abs().max())
    d2 = float((e0["turnover"] - t0).abs().max())
    e10 = backtest(px, W, cost_bps=10.0, freq=CFG["freq"])["returns"]
    d3 = float((e10 - (r0 - t0 * 10.0 / 1e4)).abs().max())
    ok = d1 < 1e-12 and d2 < 1e-10 and d3 < 1e-12
    P(f"      max|dret|={d1:.3e}  max|dturn|={d2:.3e}  cost-linearity max|d|={d3:.3e}"
      f"   -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_b(cells):
    """THE decisive control: reproduce 182B's committed phase.csv (u56 @10bps, phases 0..7)."""
    P(f"  [B] anchor sweep vs {PARENT}.phase.csv  (THE decisive control)")
    src = OUT / f"{PARENT}.phase.csv"
    if not src.exists():
        P(f"      MISSING {src.name} -> control cannot run; the run STOPS.")
        return False
    ref = pd.read_csv(src)
    mine = cells[(cells.panel == "u56") & (cells.cost == 10.0)].set_index("phase")
    cols = ["CAGR_F", "Sharpe_F", "MaxDD_F", "CAGR_H1", "Sharpe_H1", "CAGR_H2", "Sharpe_H2",
            "CAGR_IS", "Sharpe_IS", "CAGR_OOS", "Sharpe_OOS", "MaxDD_OOS"]
    worst, ok = 0.0, True
    for _, rr in ref.iterrows():
        ph = int(rr["phase"])
        if ph not in mine.index:
            P(f"      phase {ph} absent from this sweep -> FAIL")
            ok = False
            continue
        for c in cols:
            if c in ref.columns:
                worst = max(worst, abs(float(rr[c]) - float(mine.loc[ph, c])))
    ok &= worst < 1e-9
    P(f"      {len(ref)} reference phases x {len(cols)} columns: max|d| = {worst:.3e}"
      f"   -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- D1: the anchor sweep
def anchor_sweep(panels):
    rows = []
    for pn, px in panels.items():
        W = book_weights(px)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base_r = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        keep = {}
        for ph in PHASES:
            r0, t0 = sim(px, W, CFG["freq"], 1, ph)
            keep[ph] = (r0, t0)
            for cb in COSTS:
                r = (r0 - t0 * cb / 1e4).loc[start:]
                d = full_row(r)
                d.update(panel=pn, phase=ph, cost=cb,
                         turnover_yr=float(t0.loc[start:].sum()) / (len(r) / 252))
                b = (base_r["returns"] - base_r["turnover"] * cb / 1e4).loc[start:]
                d["fail4a"] = fail4a(d, full_row(b))
                d["fail4b"] = fail4b(d, full_row(spy))
                d["pass4a"] = d["fail4a"] == "-"
                d["pass4b"] = d["fail4b"] == "-"
                d["dd_margin_pp"] = dd_margin_pp(d["MaxDD_F"], metrics(spy)["MaxDD"])
                rows.append(d)
        # anchor-agnostic by-product: 1/21 of capital on each of the 21 anchor schedules.
        # No choice is made, so this adds no tuned parameter; it is reported, not selected.
        r0m = pd.concat([v[0] for v in keep.values()], axis=1).mean(axis=1)
        t0m = pd.concat([v[1] for v in keep.values()], axis=1).mean(axis=1)
        for cb in COSTS:
            r = (r0m - t0m * cb / 1e4).loc[start:]
            d = full_row(r)
            d.update(panel=pn, phase=-1, cost=cb,
                     turnover_yr=float(t0m.loc[start:].sum()) / (len(r) / 252))
            b = (base_r["returns"] - base_r["turnover"] * cb / 1e4).loc[start:]
            d["fail4a"] = fail4a(d, full_row(b))
            d["fail4b"] = fail4b(d, full_row(spy))
            d["pass4a"] = d["fail4a"] == "-"
            d["pass4b"] = d["fail4b"] == "-"
            d["dd_margin_pp"] = dd_margin_pp(d["MaxDD_F"], metrics(spy)["MaxDD"])
            rows.append(d)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- D2: the leaderboard back-fill
STRICT = re.compile(r"monthly|freq\s*=\s*M\b|cad(?:ence)?\s*[=:]?\s*M\b|\bM-cadence\b", re.I)
BARE_M = re.compile(r"(?<![\w-])M(?![\w-])")          # a lone capital M used as a cadence token


def is_monthly(s, wide):
    """WIDE is a strict superset of STRICT: STRICT's named forms, plus a bare capital M."""
    return bool(STRICT.search(s)) or (wide and bool(BARE_M.search(s)))


def parse_leaderboard():
    rows = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n"):
        if not ln.startswith("| 20"):
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) < 8:
            continue
        try:
            dd = float(c[4].replace("%", "")) / 100.0
        except ValueError:
            continue
        rows.append(dict(date=c[0], idea=c[1], MaxDD=dd, verdict=c[7], script=c[-1]))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- D3: rule-8 walk-forward
def walkforward(panels, cells):
    rows = []
    for pn, px in panels.items():
        W = book_weights(px)
        start = px.index[260]
        spy_all = px["SPY"].pct_change().fillna(0).loc[start:]
        base_raw = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        sims = {ph: sim(px, W, CFG["freq"], 1, ph) for ph in PHASES}
        for cb in COSTS:
            nets = {ph: (r0 - t0 * cb / 1e4).loc[start:] for ph, (r0, t0) in sims.items()}
            is_sh = {ph: metrics(win(r, hi=IS_END))["Sharpe"] for ph, r in nets.items()}
            oos_sh = {ph: metrics(win(r, lo=OOS_START))["Sharpe"] for ph, r in nets.items()}
            arms = {
                "CONST-0 (published)": nets[0],
                "IS-PICK": nets[max(is_sh, key=is_sh.get)],
                "MEAN-21 (anchor-agnostic)": pd.concat(nets.values(), axis=1).mean(axis=1),
                "ORACLE (upper bound)": nets[max(oos_sh, key=oos_sh.get)],
            }
            arms["RULES v1 baseline"] = (base_raw["returns"] - base_raw["turnover"] * cb / 1e4).loc[start:]
            arms["SPY"] = spy_all
            for nm, r in arms.items():
                o = win(r, lo=OOS_START)
                m = metrics(o)
                rows.append(dict(panel=pn, cost=cb, arm=nm,
                                 IS_Sharpe=metrics(win(r, hi=IS_END))["Sharpe"],
                                 OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                                 chosen=(max(is_sh, key=is_sh.get) if nm == "IS-PICK" else
                                         (max(oos_sh, key=oos_sh.get) if nm.startswith("ORACLE") else
                                          (0 if nm.startswith("CONST") else -1)))))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    P(f"=== idea 223  the-trade-date-anchor-as-a-published-column   ({STEM}) ===")
    P("Standing candidate:", CFG, "| anchors: phases 0..20 | costs:", COSTS,
      "| decision-to-fill gap FIXED at 1 bar (PROTOCOL rule 2)")
    P("")
    panels = {"u56": load_universe(), "broad": load_universe(broad=True)}
    for pn, px in panels.items():
        bpm = px.groupby([px.index.year, px.index.month]).size()
        P(f"  panel {pn}: {px.shape[1]-1} names + SPY, {px.index[0].date()}..{px.index[-1].date()}, "
          f"{px.shape[0]} bars, {bpm.mean():.2f} bars/month (min {bpm.min()}, max {bpm.max()})"
          f"   -> 21 phases enumerates the anchor choice")
    P("  SURVIVORSHIP: both panels are current-constituent lists; levels are not attainable returns.")
    P("")

    P("CONTROLS")
    ok_a = all(check_a(px) for px in panels.values())
    P("")

    P("D1  THE 21-ANCHOR BAND  (identical rule, only the trade date moves)")
    cells = anchor_sweep(panels)
    cells.to_csv(OUT / f"{STEM}.anchors.csv", index=False)
    ok_b = check_b(cells)
    P("")
    if not (ok_a and ok_b):
        P("!! a control FAILED - no conclusion is drawn from the numbers below.")

    band = {}
    for (pn, cb), gall in cells.groupby(["panel", "cost"]):
        g = gall[gall.phase >= 0]
        mean_row = gall[gall.phase == -1].iloc[0]
        P(f"  --- {pn} @ {cb:.0f} bps  ({len(g)} anchors) ---")
        P(f"  {'phase':>5s} {'CAGR_F':>8s} {'Sharpe_F':>9s} {'MaxDD_F':>8s} {'DDmargin':>9s} "
          f"{'Sharpe_OOS':>10s} {'turn/yr':>8s}  4b  4a  fails4b")
        for _, x in g.sort_values("phase").iterrows():
            P(f"  {int(x.phase):5d} {x.CAGR_F:8.2%} {x.Sharpe_F:9.4f} {x.MaxDD_F:8.2%} "
              f"{x.dd_margin_pp:+8.2f}pp {x.Sharpe_OOS:10.4f} {x.turnover_yr:8.2f}  "
              f"{'Y' if x.pass4b else 'n':2s}  {'Y' if x.pass4a else 'n':2s}  {x.fail4b}")
        b = dict(MaxDD=(g.MaxDD_F.max() - g.MaxDD_F.min()) * 100,
                 Sharpe=g.Sharpe_F.max() - g.Sharpe_F.min(),
                 CAGR=(g.CAGR_F.max() - g.CAGR_F.min()) * 100,
                 OOS=g.Sharpe_OOS.max() - g.Sharpe_OOS.min())
        band[(pn, cb)] = b
        P(f"  BAND over 21 anchors: MaxDD {g.MaxDD_F.min():.2%}..{g.MaxDD_F.max():.2%} "
          f"(range {b['MaxDD']:.2f}pp) | Sharpe {g.Sharpe_F.min():.4f}..{g.Sharpe_F.max():.4f} "
          f"(range {b['Sharpe']:.4f}) | CAGR range {b['CAGR']:.2f}pp | OOS Sharpe range {b['OOS']:.4f}")
        P(f"  4b passes {int(g.pass4b.sum())}/21   4a passes {int(g.pass4a.sum())}/21   "
          f"published anchor (phase 0) 4b={'PASS' if bool(g[g.phase==0].pass4b.iloc[0]) else 'FAIL'}")
        P(f"  MEAN-21 anchor-agnostic book (1/21 on each schedule, nothing chosen): "
          f"{mean_row.CAGR_F:.2%} {mean_row.Sharpe_F:.4f} {mean_row.MaxDD_F:.2%} "
          f"OOS {mean_row.Sharpe_OOS:.4f} trn {mean_row.turnover_yr:.2f}x  "
          f"4b={'PASS' if mean_row.pass4b else 'FAIL ('+mean_row.fail4b+')'}  "
          f"4a={'PASS' if mean_row.pass4a else 'FAIL ('+mean_row.fail4a+')'}")
        P("")

    P("D2  LEADERBOARD BACK-FILL: how many published monthly drawdown claims are narrower than")
    P("    their own anchor band?")
    lb = parse_leaderboard()
    P(f"  {len(lb)} leaderboard rows carry a parseable MaxDD.")
    P(f"  STRICT cadence regex: {STRICT.pattern}   (case-insensitive)")
    P(f"  WIDE = STRICT or a lone capital M: {BARE_M.pattern}")
    lb["monthly_strict"] = lb.idea.map(lambda s: is_monthly(s, False))
    lb["monthly_wide"] = lb.idea.map(lambda s: is_monthly(s, True))
    P(f"  monthly rows: STRICT {int(lb.monthly_strict.sum())}, WIDE {int(lb.monthly_wide.sum())}")

    spy_dd = metrics(panels["u56"]["SPY"].pct_change().fillna(0).loc[panels["u56"].index[260]:])["MaxDD"]
    cap = DELTA * abs(spy_dd)
    P(f"  4b drawdown cap used for EVERY row: 0.60 x |SPY MaxDD| = 0.60 x {abs(spy_dd):.2%} = "
      f"{cap:.2%}   (SPY over this script's own post-warm-up sample; see the window caveat)")
    lb["dd_margin_pp"] = lb.MaxDD.map(lambda d: dd_margin_pp(d, spy_dd))
    lb.to_csv(OUT / f"{STEM}.claims.csv", index=False)

    for tag, mask in (("STRICT", lb.monthly_strict), ("WIDE", lb.monthly_wide)):
        sub = lb[mask]
        P("")
        P(f"  -- {tag} monthly set: {len(sub)} rows --")
        for (pn, cb), b in band.items():
            B = b["MaxDD"]
            inside = sub[sub.dd_margin_pp.abs() < B]
            passing_narrow = sub[(sub.dd_margin_pp > 0) & (sub.dd_margin_pp < B)]
            P(f"     vs the {pn}@{cb:.0f}bps anchor band of {B:.2f}pp: "
              f"{len(inside)}/{len(sub)} ({len(inside)/max(len(sub),1):.1%}) of monthly rows sit "
              f"within +/-{B:.2f}pp of the 4b drawdown cap - i.e. their published DD verdict is "
              f"inside the phase noise of their own schedule;")
            P(f"        of those, {len(passing_narrow)} PASS the cap by less than the band "
              f"(a pass that a different trade date could remove).")
        ex = sub[sub.dd_margin_pp.abs() < max(b['MaxDD'] for b in band.values())]
        if len(ex):
            P(f"     narrowest 12 of {len(ex)} exposed rows:")
            for _, x in ex.reindex(ex.dd_margin_pp.abs().sort_values().index).head(12).iterrows():
                P(f"        {x.date}  {x.dd_margin_pp:+6.2f}pp  MaxDD {x.MaxDD:7.2%}  "
                  f"{x.verdict:16s} {x.idea[:78]}")
    P("")

    P("D3  PROTOCOL rule 8 WALK-FORWARD on the anchor choice")
    P("    parameters (the phase) chosen on <= 2016-12-31 only; 2017-01-01.. read once.")
    wf = walkforward(panels, cells)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    for (pn, cb), g in wf.groupby(["panel", "cost"]):
        P(f"  --- {pn} @ {cb:.0f} bps ---")
        P(f"  {'arm':>28s} {'chosen':>7s} {'IS Sharpe':>10s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
        for _, x in g.iterrows():
            ch = "-" if x.chosen < 0 else f"ph{int(x.chosen)}"
            P(f"  {x.arm:>28s} {ch:>7s} {x.IS_Sharpe:10.4f} {x.OOS_CAGR:9.2%} "
              f"{x.OOS_Sharpe:11.4f} {x.OOS_MaxDD:10.2%}")
        sp = g[g.arm == "SPY"].iloc[0]
        c0 = g[g.arm.str.startswith("CONST")].iloc[0]
        ip = g[g.arm == "IS-PICK"].iloc[0]
        P(f"  IS-PICK vs published anchor: dOOS Sharpe {ip.OOS_Sharpe - c0.OOS_Sharpe:+.4f}; "
          f"vs SPY {ip.OOS_Sharpe - sp.OOS_Sharpe:+.4f}")
        P("")

    P("=== end ===")
    flush()


if __name__ == "__main__":
    main()

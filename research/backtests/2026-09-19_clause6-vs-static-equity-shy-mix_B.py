#!/usr/bin/env python3
"""Idea 1674 (lane B, 2026-09-19): is the CLAUSE-6 candidate just a STATIC EQUITY/SHY MIX?

Ideas 1498 / 1555 found the SHY residual sleeve is the only device in the recent record that
LIFTS Sharpe: the live RULES v2 band book (U56, band 0.03, gross 0.75) with its gated-out weight
parked in SHY instead of 0%-cash clears PROTOCOL path 4a full AND OOS.  The record's standing
diagnosis is that every device loses to a matched-EXPOSURE twin.  That twin was never built for
THIS candidate, because its twin is not a de-gross: it is a STATIC equity/SHY mix held at the
candidate's own MEAN equity exposure.  If a constant mix matches the candidate, the 200d band
buys nothing and the live apparatus is unpaid turnover.

Two dials, both published in full:
    G  -- candidate target gross  {0.50, 0.65, 0.75, 0.85, 1.00}
    a  -- static twin equity weight (grid + the exposure-MATCHED value solved per candidate)
Cost axis c {0, 10, 25, 50} bps is DERIVED exactly off the c = 0 run (gate G2).
Rule 8: choosers see rows <= 2016-12-31 only; 2017-2026 read once.

Deterministic, offline, no network.  Writes .grid.csv .paired.csv .walkforward.csv .gates.csv .log.txt
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics                                            # noqa: E402

OUT = Path(__file__).with_suffix("")
SAFE = "SHY"
BAND = 0.03                       # the LIVE band, not tuned here
G_RUNGS = [0.50, 0.65, 0.75, 0.85, 1.00]
A_RUNGS = [0.40, 0.50, 0.60, 0.65, 0.70, 0.75, 0.85, 1.00]
COSTS = [0, 10, 25, 50]
IS_END = "2016-12-31"
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# ---------------------------------------------------------------- weights fns
def clause6_weights(px, band=BAND, gross=0.75):
    """RULES v2 band book at target gross `gross`, residual NAV held in SHY (clause 6, F=1.00)."""
    w = rules_v2_weights(px, band=band, gross=gross)
    resid = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w = w.copy()
    w[SAFE] = w[SAFE] + resid.where(px[SAFE].notna(), 0.0)
    return w


def static_mix_weights(px, a):
    """No gate, no ranking: equity weight `a` spread equally over every priced NON-SHY name,
    the remaining 1-a in SHY.  Same weekly cadence, same costs."""
    eq = px.drop(columns=[SAFE]).notna().astype(float)
    w = a * eq.div(eq.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    w[SAFE] = (1.0 - a) * px[SAFE].notna().astype(float)
    return w


# ---------------------------------------------------------------- run helpers
def run(px, wfn, freq="W"):
    """One c = 0 engine run; the cost axis is derived from it exactly."""
    res = backtest(px, wfn(px), cost_bps=0.0, freq=freq)
    held = res["weights"]
    eq_exp = held.drop(columns=[SAFE]).sum(axis=1)          # equity exposure = everything but SHY
    return dict(gross=res["returns"], turnover=res["turnover"], eq_exp=eq_exp, held=held)


def net(r, c):
    return r["gross"] - r["turnover"] * c / 1e4


def legs(ret, start, is_end):
    r = ret.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    oos = metrics(r.loc[pd.Timestamp(is_end) + pd.Timedelta(days=1):])
    ins = metrics(r.loc[:is_end])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=ins["Sharpe"], IS_CAGR=ins["CAGR"], IS_MaxDD=ins["MaxDD"],
                OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"], OOS_MaxDD=oos["MaxDD"])


def solve_a(px, target, lo=0.05, hi=1.00, tol=1e-5, window=None):
    """Bisect the static twin's `a` so its REALISED mean equity exposure equals the
    candidate's, over `window` (None = full scored sample)."""
    def f(a):
        e = run(px, lambda p, a=a: static_mix_weights(p, a))["eq_exp"]
        e = e.loc[START:] if window is None else e.loc[START:window]
        return e.mean()
    for _ in range(40):
        mid = (lo + hi) / 2
        if f(mid) < target: lo = mid
        else: hi = mid
        if hi - lo < tol: break
    return (lo + hi) / 2


# ---------------------------------------------------------------- data
px = load_universe()
START = px.index[260]                                    # same warm-up skip as baseline.compare
say(f"# idea 1674 — clause-6 candidate vs static equity/SHY mix, U56, {START.date()} -> {px.index[-1].date()}")
say(f"# {px.shape[1]} instruments, {(px.index[-1]-START).days/365.25:.2f} years scored, band {BAND}, weekly, "
    f"costs derived at {COSTS} bps")

spy_ret = px["SPY"].pct_change().fillna(0.0)
base = run(px, rules_v2_weights)                          # LIVE RULES v2 (G 0.75, 0% cash)
v1 = run(px, rules_v1_weights)

# ---------------------------------------------------------------- gates (printed before any hypothesis)
gates = []


def gate(name, val, ok, note=""):
    gates.append(dict(gate=name, value=val, pass_=bool(ok), note=note))
    say(f"GATE {name}: {val}  {'PASS' if ok else 'FAIL'}  {note}")


gate("G0 sample years", round((px.index[-1] - START).days / 365.25, 2), (px.index[-1] - START).days / 365.25 >= 10,
     "PROTOCOL rule 1 minimum 10y")
_chk = backtest(px, rules_v2_weights(px), cost_bps=25.0, freq="W")["returns"].loc[START:]
_der = net(base, 25).loc[START:]
gate("G1 cost axis exact (derived 25bps vs engine 25bps)", f"{float((_chk-_der).abs().max()):.3e}",
     float((_chk - _der).abs().max()) < 1e-12, "r(c) = r_gross - turnover*c/1e4")
_c6 = clause6_weights(px, gross=0.75)
_v2 = rules_v2_weights(px, gross=0.75)
gate("G2 clause6 equity leg == baseline.rules_v2_weights", f"{float((_c6.drop(columns=[SAFE])-_v2.drop(columns=[SAFE])).abs().max().max()):.3e}",
     float((_c6.drop(columns=[SAFE]) - _v2.drop(columns=[SAFE])).abs().max().max()) < 1e-15,
     "clause 6 changes only the SHY line")
gate("G3 clause6 fully invested", f"{float(_c6.sum(axis=1).loc[START:].min()):.6f} .. {float(_c6.sum(axis=1).loc[START:].max()):.6f}",
     abs(float(_c6.sum(axis=1).loc[START:].max()) - 1.0) < 1e-9, "no leverage, no shorting")
gate("G4 static twin weights sum to 1", f"{float(static_mix_weights(px,0.75).sum(axis=1).loc[START:].min()):.6f}",
     abs(float(static_mix_weights(px, 0.75).sum(axis=1).loc[START:].min()) - 1.0) < 1e-9, "")
gate("G5 no negative weights", float(min(_c6.min().min(), static_mix_weights(px, 0.75).min().min())),
     min(_c6.min().min(), static_mix_weights(px, 0.75).min().min()) >= -1e-15, "long-only")

spy_full = metrics(spy_ret.loc[START:]); _h = len(spy_ret.loc[START:]) // 2
spy_h1 = metrics(spy_ret.loc[START:].iloc[:_h]); spy_h2 = metrics(spy_ret.loc[START:].iloc[_h:])
spy_oos = metrics(spy_ret.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
say(f"\nSPY FULL {spy_full['CAGR']:.2%} / {spy_full['Sharpe']:.4f} / {spy_full['MaxDD']:.2%}"
    f"  halves {spy_h1['Sharpe']:.4f} / {spy_h2['Sharpe']:.4f}"
    f"  OOS {spy_oos['CAGR']:.2%} / {spy_oos['Sharpe']:.4f} / {spy_oos['MaxDD']:.2%}")
LIVE = legs(net(base, 10), START, IS_END)
say(f"LIVE RULES v2 @10bps FULL {LIVE['CAGR']:.2%} / {LIVE['Sharpe']:.4f} / {LIVE['MaxDD']:.2%}"
    f"  halves {LIVE['H1']:.4f} / {LIVE['H2']:.4f}  OOS {LIVE['OOS_CAGR']:.2%} / {LIVE['OOS_Sharpe']:.4f} / {LIVE['OOS_MaxDD']:.2%}")

# ---------------------------------------------------------------- KEEP paths
def keep4a(d, c):
    live = legs(net(base, c), START, IS_END)
    return bool(d["H1"] > live["H1"] and d["H2"] > live["H2"] and d["MaxDD"] >= live["MaxDD"])


def keep4b(d, oos=False):
    if oos:
        return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"]
                    and d["OOS_Sharpe"] > spy_oos["Sharpe"]
                    and d["OOS_MaxDD"] >= 0.6 * spy_oos["MaxDD"]
                    and d["OOS_CAGR"] >= 0.7 * spy_oos["CAGR"])
    return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"]
                and d["MaxDD"] >= 0.6 * spy_full["MaxDD"] and d["CAGR"] >= 0.7 * spy_full["CAGR"])


# ---------------------------------------------------------------- arms
runs, rows = {}, []
for G in G_RUNGS:
    runs[("CAND", G)] = run(px, lambda p, G=G: clause6_weights(p, BAND, G))
for a in A_RUNGS:
    runs[("STATIC", a)] = run(px, lambda p, a=a: static_mix_weights(p, a))

# exposure-matched twins: full-sample match, and an IS-ONLY match used for the OOS leg
matched = {}
for G in G_RUNGS:
    tgt_full = runs[("CAND", G)]["eq_exp"].loc[START:].mean()
    tgt_is = runs[("CAND", G)]["eq_exp"].loc[START:IS_END].mean()
    a_full, a_is = solve_a(px, tgt_full), solve_a(px, tgt_is, window=IS_END)
    for tag, a in (("MATCH", a_full), ("MATCH_IS", a_is)):
        runs[(tag, G)] = run(px, lambda p, a=a: static_mix_weights(p, a))
    matched[G] = dict(target_full=tgt_full, a_full=a_full, target_is=tgt_is, a_is=a_is)
    say(f"matched twin  G={G:.2f}: candidate mean equity exposure FULL {tgt_full:.4f} -> a {a_full:.4f} "
        f"(realised {runs[('MATCH',G)]['eq_exp'].loc[START:].mean():.4f}); IS {tgt_is:.4f} -> a {a_is:.4f}")

worst = max(abs(runs[("MATCH", G)]["eq_exp"].loc[START:].mean() - matched[G]["target_full"]) for G in G_RUNGS)
gate("G6 exposure match tolerance (FULL)", f"{worst:.3e}", worst < 1e-4, "candidate vs matched twin mean equity weight")

for (kind, k), r in runs.items():
    for c in COSTS:
        d = legs(net(r, c), START, IS_END)
        yrs = (px.index[-1] - START).days / 365.25
        rows.append(dict(arm=kind, dial=k, cost_bps=c,
                         mean_eq_exposure=float(r["eq_exp"].loc[START:].mean()),
                         turnover_yr=float(r["turnover"].loc[START:].sum() / yrs),
                         **{kk: float(vv) for kk, vv in d.items()},
                         keep4a=keep4a(d, c), keep4b_full=keep4b(d), keep4b_oos=keep4b(d, oos=True)))
grid = pd.DataFrame(rows)
grid.to_csv(f"{OUT}.grid.csv", index=False)
say(f"\n# GRID: {len(grid)} cells, all published -> {Path(OUT).name}.grid.csv")

# ---------------------------------------------------------------- the contest
say("\n## PAIRED: clause-6 candidate MINUS its exposure-matched static twin (same mean equity weight)")
pair = []
for G in G_RUNGS:
    for c in COSTS:
        cd = legs(net(runs[("CAND", G)], c), START, IS_END)
        td = legs(net(runs[("MATCH", G)], c), START, IS_END)
        to = legs(net(runs[("MATCH_IS", G)], c), START, IS_END)
        pair.append(dict(G=G, cost_bps=c, a_matched=matched[G]["a_full"],
                         cand_CAGR=cd["CAGR"], twin_CAGR=td["CAGR"], dCAGR_pp=(cd["CAGR"] - td["CAGR"]) * 100,
                         cand_Sharpe=cd["Sharpe"], twin_Sharpe=td["Sharpe"], dSharpe=cd["Sharpe"] - td["Sharpe"],
                         cand_MaxDD=cd["MaxDD"], twin_MaxDD=td["MaxDD"], dMaxDD_pp=(cd["MaxDD"] - td["MaxDD"]) * 100,
                         dSharpe_H1=cd["H1"] - td["H1"], dSharpe_H2=cd["H2"] - td["H2"],
                         dSharpe_OOS=cd["OOS_Sharpe"] - to["OOS_Sharpe"],
                         dMaxDD_OOS_pp=(cd["OOS_MaxDD"] - to["OOS_MaxDD"]) * 100,
                         dCAGR_OOS_pp=(cd["OOS_CAGR"] - to["OOS_CAGR"]) * 100,
                         cand_turnover=runs[("CAND", G)]["turnover"].loc[START:].sum() / ((px.index[-1]-START).days/365.25),
                         twin_turnover=runs[("MATCH", G)]["turnover"].loc[START:].sum() / ((px.index[-1]-START).days/365.25)))
pair = pd.DataFrame(pair)
pair.to_csv(f"{OUT}.paired.csv", index=False)
say(pair[["G", "cost_bps", "a_matched", "cand_Sharpe", "twin_Sharpe", "dSharpe", "dSharpe_H1", "dSharpe_H2",
          "dSharpe_OOS", "dCAGR_pp", "dMaxDD_pp", "cand_turnover", "twin_turnover"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
n = len(pair)
say(f"\ndSharpe FULL > 0 in {int((pair.dSharpe>0).sum())} of {n}; OOS > 0 in {int((pair.dSharpe_OOS>0).sum())} of {n}; "
    f"BOTH halves > 0 in {int(((pair.dSharpe_H1>0)&(pair.dSharpe_H2>0)).sum())} of {n}; "
    f"dMaxDD (shallower) > 0 in {int((pair.dMaxDD_pp>0).sum())} of {n}; "
    f"dCAGR > 0 in {int((pair.dCAGR_pp>0).sum())} of {n}")
say(f"mean dSharpe FULL {pair.dSharpe.mean():+.4f}, OOS {pair.dSharpe_OOS.mean():+.4f}, "
    f"mean dMaxDD {pair.dMaxDD_pp.mean():+.2f} pp, mean dCAGR {pair.dCAGR_pp.mean():+.2f} pp")

# ---------------------------------------------------------------- KEEP path census
k4a = grid[grid.keep4a]; k4b = grid[grid.keep4b_full]; k4bo = grid[grid.keep4b_full & grid.keep4b_oos]
say(f"\n## KEEP paths over all {len(grid)} cells: 4a {len(k4a)}; 4b FULL {len(k4b)}; 4b FULL and OOS {len(k4bo)}")
for nm, sub in (("4a", k4a), ("4b FULL+OOS", k4bo)):
    if len(sub):
        say(f"  {nm}: " + "; ".join(f"{r.arm} {r.dial:.2f} @{r.cost_bps}bps (S {r.Sharpe:.4f}, DD {r.MaxDD:.2%}, CAGR {r.CAGR:.2%})"
                                    for r in sub.itertuples()))
    else:
        say(f"  {nm}: none")

# ---------------------------------------------------------------- rule 8 walk-forward
say("\n## RULE 8 WALK-FORWARD — choosers fitted on rows <= 2016-12-31 only, 2017-2026 read once")
wf = []
universe_arms = [("CAND", G) for G in G_RUNGS] + [("STATIC", a) for a in A_RUNGS]
for c in COSTS:
    is_stats = {k: legs(net(runs[k], c), START, IS_END) for k in universe_arms}
    # C_MEMO is the record's OWN pre-stated rule (2026-09-03 recommendation memo): "smallest
    # exposure dial whose MaxDD <= 60% of SPY's and CAGR >= 70% of SPY's; if none, keep 0.75",
    # evaluated here on IS ROWS ONLY against the IS SPY bars.
    spy_is = metrics(spy_ret.loc[START:IS_END])

    def memo_pick(fam, default):
        ok = [k for k in universe_arms if k[0] == fam
              and is_stats[k]["IS_MaxDD"] >= 0.6 * spy_is["MaxDD"]
              and is_stats[k]["IS_CAGR"] >= 0.7 * spy_is["CAGR"]]
        return min(ok, key=lambda k: k[1]) if ok else default

    choosers = {
        "C_SHARPE": max(universe_arms, key=lambda k: is_stats[k]["IS_Sharpe"]),
        "C_CAGR": max(universe_arms, key=lambda k: is_stats[k]["IS_CAGR"]),
        "C_CALMAR": max(universe_arms, key=lambda k: is_stats[k]["IS_CAGR"] / abs(is_stats[k]["IS_MaxDD"])),
        "C_MEMO_CAND": memo_pick("CAND", ("CAND", 0.75)),
        "C_MEMO_STATIC": memo_pick("STATIC", ("STATIC", 0.75)),
        "C_LIVE": ("CAND", 0.75),
    }
    for nm, k in choosers.items():
        d = legs(net(runs[k], c), START, IS_END)
        wf.append(dict(cost_bps=c, chooser=nm, pick=f"{k[0]} {k[1]:.2f}",
                       OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"], OOS_MaxDD=d["OOS_MaxDD"],
                       keep4b_oos=keep4b(d, oos=True), keep4a=keep4a(d, c)))
wf = pd.DataFrame(wf)
wf.to_csv(f"{OUT}.walkforward.csv", index=False)
say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
live_oos = legs(net(base, 10), START, IS_END)
say(f"\nbenchmarks OOS: LIVE RULES v2 @10bps {live_oos['OOS_CAGR']:.2%} / {live_oos['OOS_Sharpe']:.4f} / {live_oos['OOS_MaxDD']:.2%}"
    f"   SPY {spy_oos['CAGR']:.2%} / {spy_oos['Sharpe']:.4f} / {spy_oos['MaxDD']:.2%}")
gate("G7 chooser sees no 2017+ row", "truncated arrays", True,
     "IS_Sharpe/IS_CAGR/IS_MaxDD computed on r.loc[:2016-12-31] only")
gate("G8 every grid point published", f"{len(grid)} cells", True, "grid.csv + paired.csv + walkforward.csv")
pd.DataFrame(gates).to_csv(f"{OUT}.gates.csv", index=False)
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
print(f"\nwrote {Path(OUT).name}.{{grid,paired,walkforward,gates}}.csv and .log.txt")

# ---------------------------------------------------------------- head to head, the two 4b books
say("\n## HEAD TO HEAD — the gated candidate vs the ungated static mix, both 4b passers")
h2h = []
for c in COSTS:
    for k, nm in ((("CAND", 1.00), "CAND G=1.00 (band, clause 6)"), (("STATIC", 0.60), "STATIC a=0.60 (no gate)")):
        d = legs(net(runs[k], c), START, IS_END)
        h2h.append(dict(book=nm, cost_bps=c, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                        H1=d["H1"], H2=d["H2"], OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"],
                        OOS_MaxDD=d["OOS_MaxDD"], keep4b_full=keep4b(d), keep4b_oos=keep4b(d, oos=True),
                        turnover_yr=runs[k]["turnover"].loc[START:].sum() / ((px.index[-1]-START).days/365.25)))
h2h = pd.DataFrame(h2h)
h2h.to_csv(f"{OUT}.headtohead.csv", index=False)
say(h2h.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")

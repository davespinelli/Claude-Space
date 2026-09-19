#!/usr/bin/env python3
"""Idea 1670 (lane cloud, 2026-09-19): does the 1674 STATIC-TWIN verdict hold on B136 and SMALL?

Idea 1674 (lane B, U56) killed the hypothesis that the clause-6 band book is just a static
equity/SHY mix: at MATCHED mean equity exposure the candidate was SHALLOWER in 20 of 20 and
higher OOS Sharpe in 20 of 20, paid for in CAGR (20 of 20 lower) and 2.79x/yr turnover, with
the Sharpe edge reversing at 50 bps.  The construction is one line and portable.  This run
re-prices the SAME contest on the record's other two committed panels and reports whether the
verdict is a U56 fact or a panel-independent one.

Two dials, both published in full (idea 1670's own statement: panel, mix rung):
    panel  {U56 (replication control), B136, SMALL}
    a      static twin equity weight (8 published rungs + the exposure-MATCHED value per G)
Candidate gross G {0.50, 0.65, 0.75, 0.85, 1.00}; cost axis {0, 10, 25, 50} bps derived
EXACTLY off the c = 0 run.  Rule 8: choosers see rows <= 2016-12-31 only; 2017-2026 read once.

SMALL carries no SHY column, so the defensive leg is joined from data/prices.csv exactly as
load_universe joins SPY -- a benchmark sleeve, not a panel constituent (gated, G9).
SURVIVORSHIP (rule 9): U56/B136/SMALL are CURRENT-CONSTITUENT lists; absolute levels are
UPPER BOUNDS.  The candidate-minus-twin contrast is same-names/same-days/same-exposure.

Deterministic, offline, no network.  Writes .grid.csv .paired.csv .walkforward.csv .headtohead.csv .gates.csv .log.txt
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state                  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics                                              # noqa: E402

OUT = Path(__file__).with_suffix("")
SAFE = "SHY"
BAND = 0.03
G_RUNGS = [0.50, 0.65, 0.75, 0.85, 1.00]
A_RUNGS = [0.40, 0.50, 0.60, 0.65, 0.70, 0.75, 0.85, 1.00]
COSTS = [0, 10, 25, 50]
IS_END = "2016-12-31"
LOG, gates = [], []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


def gate(name, val, ok, note=""):
    gates.append(dict(gate=name, value=val, pass_=bool(ok), note=note))
    say(f"GATE {name}: {val}  {'PASS' if ok else 'FAIL'}  {note}")


# ---------------------------------------------------------------- panels
def build_panels():
    P = {}
    u = load_universe()
    P["U56"] = (u, [c for c in u.columns if c not in (SAFE,)])
    b = load_universe(broad=True)
    P["B136"] = (b, [c for c in b.columns if c not in (SAFE,)])
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SAFE]
    shy = shy.reindex(sm.index, method="ffill").rename(SAFE)
    keep = [c for c in sm.columns if c not in bad and c != "SPY"]
    sm2 = pd.concat([sm[keep + ["SPY"]], shy], axis=1)
    P["SMALL"] = (sm2, keep)
    return P, len(bad)


# ---------------------------------------------------------------- weights fns (verbatim from 1674)
def clause6_weights(px, tradable, band=BAND, gross=0.75):
    """Band book over `tradable` at target gross, residual NAV parked in SHY (clause 6, F=1.00)."""
    e = px[tradable].notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(band_state(px[tradable], band), 0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    resid = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SAFE] = w[SAFE] + resid.where(px[SAFE].notna(), 0.0)
    return w


def static_mix_weights(px, tradable, a):
    """No gate, no ranking: equity weight `a` spread equally over every priced tradable name,
    the remaining 1-a in SHY.  Same weekly cadence, same costs."""
    e = px[tradable].notna().astype(float)
    w = a * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    w[SAFE] = (1.0 - a) * px[SAFE].notna().astype(float)
    return w


def run(px, wfn, tradable, freq="W"):
    res = backtest(px, wfn(px), cost_bps=0.0, freq=freq)
    held = res["weights"]
    return dict(gross=res["returns"], turnover=res["turnover"],
                eq_exp=held[tradable].sum(axis=1), held=held)


def net(r, c):
    return r["gross"] - r["turnover"] * c / 1e4


def legs(ret, start):
    r = ret.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins, oos = metrics(r.loc[:IS_END]), metrics(r.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=ins["Sharpe"], IS_CAGR=ins["CAGR"], IS_MaxDD=ins["MaxDD"],
                OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"], OOS_MaxDD=oos["MaxDD"])


PANELS, n_bad = build_panels()
say("# idea 1670 — does the 1674 static-twin verdict hold on B136 and SMALL?")
for k, (px, tr) in PANELS.items():
    say(f"#   {k}: {px.shape[1]} cols, {len(tr)} tradable equities, {px.index[0].date()} -> {px.index[-1].date()}")
say(f"#   SMALL screen: {n_bad} tickers with max_1d_move >= 1.0 dropped from data/small_meta.csv; "
    f"SHY joined from data/prices.csv as a benchmark sleeve, SPY excluded from the tradable set")
gate("G9 SHY present on every panel", ", ".join(f"{k}:{SAFE in px.columns}" for k, (px, _) in PANELS.items()),
     all(SAFE in px.columns for px, _ in PANELS.values()), "defensive leg available on all three panels")
gate("G10 SHY never tradable equity", ", ".join(f"{k}:{SAFE not in tr}" for k, (_, tr) in PANELS.items()),
     all(SAFE not in tr for _, tr in PANELS.values()), "clause 3 reserves SHY")

rows, pair, h2h, wf = [], [], [], []
for pname, (px, trad) in PANELS.items():
    START = px.index[260]
    yrs = (px.index[-1] - START).days / 365.25
    spy = px["SPY"].pct_change().fillna(0.0)
    spy_f = metrics(spy.loc[START:]); _h = len(spy.loc[START:]) // 2
    spy_h1 = metrics(spy.loc[START:].iloc[:_h]); spy_h2 = metrics(spy.loc[START:].iloc[_h:])
    spy_o = metrics(spy.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    spy_is = metrics(spy.loc[START:IS_END])
    base = run(px, rules_v2_weights, trad)
    say(f"\n## PANEL {pname}  {START.date()} -> {px.index[-1].date()}  ({yrs:.2f} y), "
        f"{len(trad)} tradable equities")
    say(f"   SPY FULL {spy_f['CAGR']:.2%} / {spy_f['Sharpe']:.4f} / {spy_f['MaxDD']:.2%}  halves "
        f"{spy_h1['Sharpe']:.4f} / {spy_h2['Sharpe']:.4f}  OOS {spy_o['CAGR']:.2%} / {spy_o['Sharpe']:.4f} / {spy_o['MaxDD']:.2%}")
    LB = legs(net(base, 10), START)
    say(f"   RULES v2 baseline @10bps FULL {LB['CAGR']:.2%} / {LB['Sharpe']:.4f} / {LB['MaxDD']:.2%}  halves "
        f"{LB['H1']:.4f} / {LB['H2']:.4f}  OOS {LB['OOS_CAGR']:.2%} / {LB['OOS_Sharpe']:.4f} / {LB['OOS_MaxDD']:.2%}")

    def keep4a(d, c):
        L = legs(net(base, c), START)
        return bool(d["H1"] > L["H1"] and d["H2"] > L["H2"] and d["MaxDD"] >= L["MaxDD"])

    def keep4b(d, oos=False):
        if oos:
            return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"] and d["OOS_Sharpe"] > spy_o["Sharpe"]
                        and d["OOS_MaxDD"] >= 0.6 * spy_o["MaxDD"] and d["OOS_CAGR"] >= 0.7 * spy_o["CAGR"])
        return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"]
                    and d["MaxDD"] >= 0.6 * spy_f["MaxDD"] and d["CAGR"] >= 0.7 * spy_f["CAGR"])

    # ---- exposure curve for the static mix, inverted to solve the matched twin
    LADDER = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.00]
    ew = {a: run(px, lambda p, a=a: static_mix_weights(p, trad, a), trad) for a in LADDER}
    cx_full = [float(ew[a]["eq_exp"].loc[START:].mean()) for a in LADDER]
    cx_is = [float(ew[a]["eq_exp"].loc[START:IS_END].mean()) for a in LADDER]
    gate(f"G6 {pname} static exposure curve monotone",
         f"{bool(np.all(np.diff(cx_full)>0))}/{bool(np.all(np.diff(cx_is)>0))}",
         bool(np.all(np.diff(cx_full) > 0) and np.all(np.diff(cx_is) > 0)), "unique matched twin")

    arms = {}
    for G in G_RUNGS:
        arms[("CAND", G)] = run(px, lambda p, G=G: clause6_weights(p, trad, BAND, G), trad)
    for a in A_RUNGS:
        arms[("STATIC", a)] = ew[a] if a in ew else run(px, lambda p, a=a: static_mix_weights(p, trad, a), trad)

    matched, merr = {}, []
    for G in G_RUNGS:
        tf = float(arms[("CAND", G)]["eq_exp"].loc[START:].mean())
        ti = float(arms[("CAND", G)]["eq_exp"].loc[START:IS_END].mean())
        af, ai = float(np.interp(tf, cx_full, LADDER)), float(np.interp(ti, cx_is, LADDER))
        arms[("MATCH", G)] = run(px, lambda p, a=af: static_mix_weights(p, trad, a), trad)
        arms[("MATCH_IS", G)] = run(px, lambda p, a=ai: static_mix_weights(p, trad, a), trad)
        matched[G] = dict(target_full=tf, a_full=af, target_is=ti, a_is=ai)
        merr.append(abs(float(arms[("MATCH", G)]["eq_exp"].loc[START:].mean()) - tf))
        say(f"   matched twin G={G:.2f}: candidate mean equity exposure FULL {tf:.4f} -> a {af:.4f} "
            f"(realised {arms[('MATCH',G)]['eq_exp'].loc[START:].mean():.4f}); IS {ti:.4f} -> a {ai:.4f}")
    gate(f"G7 {pname} exposure match tolerance", f"{max(merr):.3e}", max(merr) < 5e-3, "")
    _c6 = clause6_weights(px, trad, BAND, 0.75)
    gate(f"G8 {pname} fully invested, long only",
         f"sum {float(_c6.sum(axis=1).loc[START:].max()):.6f}, min w {float(_c6.min().min()):.2e}",
         abs(float(_c6.sum(axis=1).loc[START:].max()) - 1.0) < 1e-9 and _c6.min().min() >= -1e-15, "")

    for (kind, k), r in arms.items():
        for c in COSTS:
            d = legs(net(r, c), START)
            rows.append(dict(panel=pname, arm=kind, dial=k, cost_bps=c,
                             mean_eq_exposure=float(r["eq_exp"].loc[START:].mean()),
                             turnover_yr=float(r["turnover"].loc[START:].sum() / yrs),
                             **{kk: float(vv) for kk, vv in d.items()},
                             keep4a=keep4a(d, c), keep4b_full=keep4b(d), keep4b_oos=keep4b(d, oos=True)))

    for G in G_RUNGS:
        for c in COSTS:
            cd = legs(net(arms[("CAND", G)], c), START)
            td = legs(net(arms[("MATCH", G)], c), START)
            to = legs(net(arms[("MATCH_IS", G)], c), START)
            pair.append(dict(panel=pname, G=G, cost_bps=c, a_matched=matched[G]["a_full"],
                             cand_CAGR=cd["CAGR"], twin_CAGR=td["CAGR"], dCAGR_pp=(cd["CAGR"] - td["CAGR"]) * 100,
                             cand_Sharpe=cd["Sharpe"], twin_Sharpe=td["Sharpe"], dSharpe=cd["Sharpe"] - td["Sharpe"],
                             cand_MaxDD=cd["MaxDD"], twin_MaxDD=td["MaxDD"], dMaxDD_pp=(cd["MaxDD"] - td["MaxDD"]) * 100,
                             dSharpe_H1=cd["H1"] - td["H1"], dSharpe_H2=cd["H2"] - td["H2"],
                             dSharpe_OOS=cd["OOS_Sharpe"] - to["OOS_Sharpe"],
                             dMaxDD_OOS_pp=(cd["OOS_MaxDD"] - to["OOS_MaxDD"]) * 100,
                             dCAGR_OOS_pp=(cd["OOS_CAGR"] - to["OOS_CAGR"]) * 100,
                             cand_turnover=float(arms[("CAND", G)]["turnover"].loc[START:].sum() / yrs),
                             twin_turnover=float(arms[("MATCH", G)]["turnover"].loc[START:].sum() / yrs)))

    # head to head: 1674's two 4b books, re-priced on this panel
    for c in COSTS:
        for k, nm in ((("CAND", 1.00), "CAND G=1.00 (band, clause 6)"), (("STATIC", 0.60), "STATIC a=0.60 (no gate)")):
            d = legs(net(arms[k], c), START)
            h2h.append(dict(panel=pname, book=nm, cost_bps=c, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                            H1=d["H1"], H2=d["H2"], OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"],
                            OOS_MaxDD=d["OOS_MaxDD"], keep4b_full=keep4b(d), keep4b_oos=keep4b(d, oos=True),
                            turnover_yr=float(arms[k]["turnover"].loc[START:].sum() / yrs)))

    # rule 8 — 1674's own six choosers, re-fitted per panel on IS rows only
    ua = [("CAND", G) for G in G_RUNGS] + [("STATIC", a) for a in A_RUNGS]
    for c in COSTS:
        isd = {k: legs(net(arms[k], c), START) for k in ua}

        def memo_pick(fam, default):
            ok = [k for k in ua if k[0] == fam and isd[k]["IS_MaxDD"] >= 0.6 * spy_is["MaxDD"]
                  and isd[k]["IS_CAGR"] >= 0.7 * spy_is["CAGR"]]
            return min(ok, key=lambda k: k[1]) if ok else default

        choosers = {"C_SHARPE": max(ua, key=lambda k: isd[k]["IS_Sharpe"]),
                    "C_CAGR": max(ua, key=lambda k: isd[k]["IS_CAGR"]),
                    "C_CALMAR": max(ua, key=lambda k: isd[k]["IS_CAGR"] / abs(isd[k]["IS_MaxDD"])),
                    "C_MEMO_CAND": memo_pick("CAND", ("CAND", 0.75)),
                    "C_MEMO_STATIC": memo_pick("STATIC", ("STATIC", 0.75)),
                    "C_LIVE": ("CAND", 0.75)}
        for nm, k in choosers.items():
            d = legs(net(arms[k], c), START)
            wf.append(dict(panel=pname, cost_bps=c, chooser=nm, pick=f"{k[0]} {k[1]:.2f}",
                           OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"], OOS_MaxDD=d["OOS_MaxDD"],
                           SPY_OOS_CAGR=spy_o["CAGR"], SPY_OOS_Sharpe=spy_o["Sharpe"], SPY_OOS_MaxDD=spy_o["MaxDD"],
                           keep4b_oos=keep4b(d, oos=True), keep4a=keep4a(d, c)))

grid = pd.DataFrame(rows); grid.to_csv(f"{OUT}.grid.csv", index=False)
pair = pd.DataFrame(pair); pair.to_csv(f"{OUT}.paired.csv", index=False)
h2h = pd.DataFrame(h2h); h2h.to_csv(f"{OUT}.headtohead.csv", index=False)
wf = pd.DataFrame(wf); wf.to_csv(f"{OUT}.walkforward.csv", index=False)
gate("G11 every grid point published", f"{len(grid)} grid, {len(pair)} paired, {len(h2h)} h2h, {len(wf)} wf", True, "")
gate("G12 tuned dials", "2 (panel, mix rung a)", True, "idea 1670's own statement; G ladder is 1674's, not re-tuned")

say(f"\n# GRID: {len(grid)} cells published -> {Path(OUT).name}.grid.csv")
say("\n## PAIRED — clause-6 candidate MINUS its exposure-matched static twin, by panel")
say(pair[["panel", "G", "cost_bps", "a_matched", "cand_Sharpe", "twin_Sharpe", "dSharpe", "dSharpe_H1",
          "dSharpe_H2", "dSharpe_OOS", "dCAGR_pp", "dMaxDD_pp", "cand_turnover", "twin_turnover"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

say("\n## THE 1674 VERDICT, PANEL BY PANEL (1674 on U56: dMaxDD shallower 20/20 mean +4.10 pp; "
    "dSharpe_OOS > 0 20/20 mean +0.1085; dCAGR < 0 20/20 mean -1.07 pp)")
for pname, sub in pair.groupby("panel"):
    n = len(sub)
    say(f"  {pname}: dMaxDD shallower {int((sub.dMaxDD_pp>0).sum())}/{n} (mean {sub.dMaxDD_pp.mean():+.2f} pp); "
        f"dSharpe_OOS > 0 {int((sub.dSharpe_OOS>0).sum())}/{n} (mean {sub.dSharpe_OOS.mean():+.4f}); "
        f"dSharpe FULL > 0 {int((sub.dSharpe>0).sum())}/{n} (mean {sub.dSharpe.mean():+.4f}); "
        f"BOTH halves > 0 {int(((sub.dSharpe_H1>0)&(sub.dSharpe_H2>0)).sum())}/{n}; "
        f"dCAGR > 0 {int((sub.dCAGR_pp>0).sum())}/{n} (mean {sub.dCAGR_pp.mean():+.2f} pp); "
        f"turnover {sub.cand_turnover.mean():.2f}x vs {sub.twin_turnover.mean():.2f}x")
say("\n  cost-rung detail (mean dSharpe FULL by panel x cost):")
say(pair.pivot_table(index="panel", columns="cost_bps", values="dSharpe", aggfunc="mean")
    .to_string(float_format=lambda x: f"{x:+.4f}"))
say("  mean dSharpe OOS by panel x cost:")
say(pair.pivot_table(index="panel", columns="cost_bps", values="dSharpe_OOS", aggfunc="mean")
    .to_string(float_format=lambda x: f"{x:+.4f}"))
say("  mean dMaxDD (pp, + = candidate shallower) by panel x cost:")
say(pair.pivot_table(index="panel", columns="cost_bps", values="dMaxDD_pp", aggfunc="mean")
    .to_string(float_format=lambda x: f"{x:+.2f}"))

k4a = grid[grid.keep4a]; k4bo = grid[grid.keep4b_full & grid.keep4b_oos]
say(f"\n## KEEP paths over all {len(grid)} cells: 4a {len(k4a)}; 4b FULL {int(grid.keep4b_full.sum())}; "
    f"4b FULL and OOS {len(k4bo)}")
for nm, sub in (("4a", k4a), ("4b FULL+OOS", k4bo)):
    say(f"  {nm}: " + ("; ".join(f"{r.panel}/{r.arm} {r.dial:.2f} @{r.cost_bps}bps "
                                 f"(S {r.Sharpe:.4f}, DD {r.MaxDD:.2%}, CAGR {r.CAGR:.2%})"
                                 for r in sub.itertuples()) if len(sub) else "none"))

say("\n## HEAD TO HEAD — 1674's two books re-priced on each panel")
say(h2h.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

say("\n## RULE 8 WALK-FORWARD — choosers fitted on rows <= 2016-12-31 only, 2017-2026 read once")
say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("\nOOS 4b pass rate by panel x chooser:")
say(wf.pivot_table(index="chooser", columns="panel", values="keep4b_oos", aggfunc="sum").to_string())
gate("G13 chooser sees no 2017+ row", "truncated arrays", True, "IS_* on r.loc[:2016-12-31] only")
_px = PANELS["U56"][0]
_chk = backtest(_px, rules_v2_weights(_px), cost_bps=25.0, freq="W")["returns"]
_der = net(run(_px, rules_v2_weights, PANELS["U56"][1]), 25)
gate("G14 cost axis exact (derived 25bps vs engine 25bps)", f"{float((_chk-_der).abs().max()):.3e}",
     float((_chk - _der).abs().max()) < 1e-12, "r(c) = r_gross - turnover*c/1e4")
pd.DataFrame(gates).to_csv(f"{OUT}.gates.csv", index=False)
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
print(f"\nwrote {Path(OUT).name}.{{grid,paired,headtohead,walkforward,gates}}.csv and .log.txt")

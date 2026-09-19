#!/usr/bin/env python3
"""Idea 1454 (lane B, 2026-09-19): does the 2026-09-03 RECOMMENDATION memo's OWN G-choosing
rule survive PROTOCOL rule 8?

WHY THIS IDEA.  Five consecutive runs on 2026-09-19 (1405 trailing equity stop, 1413 breadth
throttle, 1433 intra-book inverse-vol, 1429 beta-keyed floor-and-cap, 1436 its beta-matched
twin) each found a DRAWDOWN-BUYING DEVICE that is beaten, at matched exposure, by a plain
DE-GROSS of the same anchor.  The record's repeated WINNER is therefore the constant gross
scalar G itself -- and G has never been scored as a candidate in its own right, nor has the
rule that SET the live G=0.75 ever been licensed out of sample.  That rule is written down,
pre-registered, in research/backtests/2026-09-03_RECOMMENDATION.md:

    "gross G (G chosen ONLY from idea 28's three reported values by the pre-stated rule
     'smallest G whose MaxDD <= 60% of SPY's and CAGR >= 70% of SPY's'; if none, keep 75%)"

This run fits that rule, and its budget-side mirror, on 2009-2016 ALONE and reads 2017-2026
exactly once.

THE GRID.  G in {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00} x cadence in {W, M}
= 14 cells per panel, 42 in all, EVERY ONE REPORTED.  Two tuned parameters exactly (G, cadence).
The book at every cell is the LIVE RULES v2 shape (`baseline.rules_v2_weights`, band 0.03,
de-gross to cash, never re-spread) with its gross replaced by G; G=0.75 & W IS the live book.
No leverage: the ladder stops at G=1.00 (PROTOCOL rule 2).

CHOOSERS, all fit on IS (2009-2016) only, then read once on OOS (2017-2026):
  C_MEMO   smallest G with IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR;
           if no G qualifies, keep 0.75 (the memo's own stated fallback).
  C_BUDGET largest  G with IS MaxDD <= 0.60 x SPY_IS MaxDD  (spend the whole risk budget).
  C_ANCHOR G = 0.75, the frozen live value (the null: choosing nothing).
Each is run per-cadence and jointly over (G, cadence) with IS Sharpe as the tiebreak.

Costs 10 bps per unit turnover, weights decided at t and applied at t+1 (engine), per PROTOCOL.
Outputs: .grid.csv (every cell), .choosers.csv, .gates.csv, .console.txt.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

sys.path.insert(0, "research")
from baseline import load_universe, rules_v2_weights, compare, ROOT  # noqa
from engine import backtest, metrics  # noqa

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-19_memo-G-chooser-under-rule-8_B"
COST = 10
GRID_G = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
CADENCES = ["W", "M"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
ALT_SPLITS = {"2015": "2015-01-01", "2019": "2019-01-01"}   # reported robustness of the rule-8 split itself
RET = {}

def win(r, a=None, b=None):
    s = r.loc[a:b] if (a or b) else r
    return s

def stats(r):
    if len(r) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])

def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def keep_4a(cell, base):
    """Sharpe > live rules in BOTH halves AND MaxDD no worse than live rules."""
    return bool(cell["H1"] > base["H1"] and cell["H2"] > base["H2"] and cell["MaxDD"] >= base["MaxDD"])

def keep_4b(cell, spy, window="FULL"):
    """Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    if window == "FULL":
        legs = dict(
            H1=cell["H1"] > spy["H1"], H2=cell["H2"] > spy["H2"], OOS=cell["oos_Sharpe"] > spy["oos_Sharpe"],
            DD=cell["MaxDD"] >= 0.60 * spy["MaxDD"], CAGR=cell["CAGR"] >= 0.70 * spy["CAGR"])
    else:  # OOS-only reading of the same five legs, halves taken inside the OOS window
        legs = dict(
            H1=cell["oos_H1"] > spy["oos_H1"], H2=cell["oos_H2"] > spy["oos_H2"],
            OOS=cell["oos_Sharpe"] > spy["oos_Sharpe"],
            DD=cell["oos_MaxDD"] >= 0.60 * spy["oos_MaxDD"], CAGR=cell["oos_CAGR"] >= 0.70 * spy["oos_CAGR"])
    return bool(all(legs.values())), legs

def panel_rows(pname, px, log):
    start = px.index[260]                                   # skip warm-up, as baseline.compare does
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    ref = {}
    for nm, r in (("SPY", spy_r),
                  ("RULESv2", backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[start:])):
        d = stats(r); d["H1"], d["H2"] = halves(r)
        o = win(r, OOS_START); i = win(r, None, IS_END)
        d.update({f"oos_{k}": v for k, v in stats(o).items()})
        d["oos_H1"], d["oos_H2"] = halves(o)
        d.update({f"is_{k}": v for k, v in stats(i).items()})
        for lbl, cut in ALT_SPLITS.items():
            d.update({f"alt{lbl}_{k}": v for k, v in stats(win(r, cut)).items()})
        ref[nm] = d
    spy, base = ref["SPY"], ref["RULESv2"]
    log(f"\n=== PANEL {pname}  ({px.shape[1]} cols, {start.date()} -> {px.index[-1].date()}) ===")
    log(f"  SPY      full CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.3f} MaxDD {spy['MaxDD']:.2%} "
        f"| halves {spy['H1']:.3f}/{spy['H2']:.3f} | IS MaxDD {spy['is_MaxDD']:.2%} CAGR {spy['is_CAGR']:.2%} "
        f"| OOS CAGR {spy['oos_CAGR']:.2%} Sharpe {spy['oos_Sharpe']:.3f} MaxDD {spy['oos_MaxDD']:.2%}")
    log(f"  RULES v2 full CAGR {base['CAGR']:.2%} Sharpe {base['Sharpe']:.3f} MaxDD {base['MaxDD']:.2%} "
        f"| halves {base['H1']:.3f}/{base['H2']:.3f} | OOS CAGR {base['oos_CAGR']:.2%} "
        f"Sharpe {base['oos_Sharpe']:.3f} MaxDD {base['oos_MaxDD']:.2%}")
    log(f"  4b caps on this panel: DD cap {0.60*spy['MaxDD']:.2%} (IS {0.60*spy['is_MaxDD']:.2%}, "
        f"OOS {0.60*spy['oos_MaxDD']:.2%}) | CAGR floor {0.70*spy['CAGR']:.2%} "
        f"(IS {0.70*spy['is_CAGR']:.2%}, OOS {0.70*spy['oos_CAGR']:.2%})")

    rows = []
    for freq in CADENCES:
        for g in GRID_G:
            res = backtest(px, rules_v2_weights(px, gross=g), cost_bps=COST, freq=freq)
            r = res["returns"].loc[start:]
            c = dict(panel=pname, cadence=freq, G=g)
            c.update(stats(r)); c["H1"], c["H2"] = halves(r)
            o, i = win(r, OOS_START), win(r, None, IS_END)
            c.update({f"oos_{k}": v for k, v in stats(o).items()})
            c["oos_H1"], c["oos_H2"] = halves(o)
            c.update({f"is_{k}": v for k, v in stats(i).items()})
            c["turnover_yr"] = res["turnover"].loc[start:].sum() / (len(r) / 252)
            for lbl, cut in ALT_SPLITS.items():          # reported robustness, NOT a tuned dial
                oo = win(r, cut); st = stats(oo)
                c[f"alt{lbl}_CAGR"], c[f"alt{lbl}_Sharpe"], c[f"alt{lbl}_MaxDD"] = st["CAGR"], st["Sharpe"], st["MaxDD"]
                ii = win(r, None, pd.Timestamp(cut) - pd.Timedelta(days=1))
                sti = stats(ii)
                c[f"alt{lbl}_is_CAGR"], c[f"alt{lbl}_is_MaxDD"], c[f"alt{lbl}_is_Sharpe"] = sti["CAGR"], sti["MaxDD"], sti["Sharpe"]
            RET[(c["panel"], freq, g)] = r
            c["pass4a"] = keep_4a(c, base)
            c["pass4b_full"], legs_f = keep_4b(c, spy, "FULL")
            c["pass4b_oos"], legs_o = keep_4b(c, spy, "OOS")
            c["legs_full"] = "".join(k for k, v in legs_f.items() if not v) or "-"
            c["legs_oos"] = "".join(k for k, v in legs_o.items() if not v) or "-"
            rows.append(c)
    df = pd.DataFrame(rows)
    log("\n  --- ALL 14 GRID POINTS (full sample | halves | OOS) ---")
    log("  cad     G |  CAGR  Sharpe   MaxDD |    H1     H2 | oosCAGR oosShrp oosMaxDD | trn/yr | 4a 4bF 4bO | binding(full/oos)")
    for _, c in df.iterrows():
        log(f"  {c.cadence:>3} {c.G:5.3f} | {c.CAGR:6.2%} {c.Sharpe:6.3f} {c.MaxDD:7.2%} | "
            f"{c.H1:5.3f} {c.H2:6.3f} | {c.oos_CAGR:7.2%} {c.oos_Sharpe:7.3f} {c.oos_MaxDD:8.2%} | "
            f"{c.turnover_yr:6.2f} | {str(c.pass4a)[0]:>2} {str(c.pass4b_full)[0]:>3} {str(c.pass4b_oos)[0]:>3} | "
            f"{c.legs_full}/{c.legs_oos}")
    return df, spy, base, start

def choosers(df, spy, pname, log):
    """Every chooser is fit on IS (2009-2016) ONLY; OOS is read once."""
    dd_cap_is = 0.60 * spy["is_MaxDD"]
    cagr_floor_is = 0.70 * spy["is_CAGR"]
    out = []
    scopes = [("cad=" + f, df[df.cadence == f]) for f in CADENCES] + [("joint", df)]
    for scope, sub in scopes:
        elig_dd = sub[sub.is_MaxDD >= dd_cap_is]                      # MaxDD is negative: >= is "shallower"
        elig_both = elig_dd[elig_dd.is_CAGR >= cagr_floor_is]
        picks, fb = {}, {}
        if len(elig_both):
            picks["C_MEMO"] = elig_both.sort_values(["G", "is_Sharpe"], ascending=[True, False]).iloc[0]
            fb["C_MEMO"] = False
        else:
            picks["C_MEMO"] = sub[(sub.G == 0.75) & (sub.cadence == ("W" if scope == "joint" else scope[-1]))].iloc[0]
            fb["C_MEMO"] = True                       # the memo's own stated fallback: "if none, keep 75%"
        picks["C_BUDGET"] = (elig_dd.sort_values(["G", "is_Sharpe"], ascending=[False, False]).iloc[0]
                             if len(elig_dd) else
                             sub.sort_values("is_MaxDD", ascending=False).iloc[0])
        picks["C_ANCHOR"] = sub[(sub.G == 0.75) & (sub.cadence == ("W" if scope == "joint" else scope[-1]))].iloc[0]
        fb["C_BUDGET"] = fb["C_ANCHOR"] = False
        for cname, p in picks.items():
            out.append(dict(panel=pname, scope=scope, chooser=cname, pick_G=p.G, pick_cadence=p.cadence,
                            used_fallback=fb[cname], is_rungs_clearing_dd_cap=len(elig_dd), is_rungs=len(sub),
                            is_rungs_clearing_both=len(elig_both),
                            is_MaxDD=p.is_MaxDD, is_CAGR=p.is_CAGR, is_Sharpe=p.is_Sharpe,
                            oos_CAGR=p.oos_CAGR, oos_Sharpe=p.oos_Sharpe, oos_MaxDD=p.oos_MaxDD,
                            oos_dd_cap=0.60 * spy["oos_MaxDD"], oos_cagr_floor=0.70 * spy["oos_CAGR"],
                            oos_dd_cap_held=bool(p.oos_MaxDD >= 0.60 * spy["oos_MaxDD"]),
                            oos_cagr_floor_held=bool(p.oos_CAGR >= 0.70 * spy["oos_CAGR"]),
                            oos_beats_spy_sharpe=bool(p.oos_Sharpe > spy["oos_Sharpe"]),
                            pass4b_full=bool(p.pass4b_full), pass4b_oos=bool(p.pass4b_oos),
                            pass4a=bool(p.pass4a)))
            eligible = len(elig_dd)
            log(f"  [{scope:>6}] {cname:<9} picks G={p.G:5.3f} {p.cadence}{' [MEMO FALLBACK: no rung cleared BOTH IS legs, memo says keep 0.75]' if fb[cname] else ''}  "
                f"(IS MaxDD {p.is_MaxDD:.2%} vs cap {dd_cap_is:.2%}, IS CAGR {p.is_CAGR:.2%} vs floor {cagr_floor_is:.2%}; "
                f"{eligible} of {len(sub)} rungs clear the IS DD cap)"
                f"  ->  OOS CAGR {p.oos_CAGR:.2%} Sharpe {p.oos_Sharpe:.3f} MaxDD {p.oos_MaxDD:.2%}"
                f"  [OOS cap {0.60*spy['oos_MaxDD']:.2%} held={p.oos_MaxDD >= 0.60*spy['oos_MaxDD']}]")
    return pd.DataFrame(out)

def gates(df, spy, base, pname, log):
    g = []
    for freq in CADENCES:
        sub = df[df.cadence == freq].sort_values("G")
        mono = bool((sub.MaxDD.diff().dropna() <= 1e-12).all())      # deeper (more negative) as G rises
        g.append(dict(panel=pname, gate="G1_maxdd_monotone_in_G", cadence=freq, value=mono,
                      detail=f"MaxDD {sub.MaxDD.min():.2%}..{sub.MaxDD.max():.2%}"))
        ratio = (sub.turnover_yr / sub.G)
        g.append(dict(panel=pname, gate="G2_turnover_per_unit_gross_constant", cadence=freq,
                      value=bool(ratio.std() / ratio.mean() < 0.02),
                      detail=f"trn/G {ratio.min():.3f}..{ratio.max():.3f} (cv {ratio.std()/ratio.mean():.2e})"))
    anchor = df[(df.G == 0.75) & (df.cadence == "W")].iloc[0]
    g.append(dict(panel=pname, gate="G3_anchor_reproduces_live_RULESv2", cadence="W",
                  value=bool(abs(anchor.Sharpe - base["Sharpe"]) < 1e-9 and abs(anchor.MaxDD - base["MaxDD"]) < 1e-9),
                  detail=f"cell {anchor.Sharpe:.6f}/{anchor.MaxDD:.6f} vs baseline {base['Sharpe']:.6f}/{base['MaxDD']:.6f}"))
    g.append(dict(panel=pname, gate="G4_spy_dd_cap_moves_IS_to_OOS", cadence="-", value=True,
                  detail=f"SPY MaxDD IS {spy['is_MaxDD']:.2%} -> OOS {spy['oos_MaxDD']:.2%}; "
                         f"cap {0.60*spy['is_MaxDD']:.2%} -> {0.60*spy['oos_MaxDD']:.2%} "
                         f"({0.60*(spy['is_MaxDD']-spy['oos_MaxDD'])*100:+.2f} pp)"))
    gd = pd.DataFrame(g)
    log("\n  --- GATES ---")
    for _, r in gd.iterrows():
        log(f"  {r.gate:<38} [{r.cadence}] {str(r.value):<5} {r.detail}")
    return gd

def main():
    lines = []
    def log(s=""):
        print(s); lines.append(s)

    log(__doc__)
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True)),
              ("SMALL485", load_universe(small=True))]
    grid, ch, ga = [], [], []
    global SPYREF; SPYREF = {}
    for pname, px in panels:
        df, spy, base, start = panel_rows(pname, px, log)
        SPYREF[pname] = spy
        log("\n  --- CHOOSERS (fit on IS 2009-2016 only, OOS read once) ---")
        ch.append(choosers(df, spy, pname, log))
        ga.append(gates(df, spy, base, pname, log))
        grid.append(df)
    G = pd.concat(grid, ignore_index=True); C = pd.concat(ch, ignore_index=True); GA = pd.concat(ga, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.choosers.csv", index=False)
    GA.to_csv(OUT / f"{STEM}.gates.csv", index=False)

    log("\n=== SUMMARY ===")
    log(f"  grid cells: {len(G)}  |  4a passes: {int(G.pass4a.sum())}  |  "
        f"4b FULL passes: {int(G.pass4b_full.sum())}  |  4b OOS passes: {int(G.pass4b_oos.sum())}")
    for pname in G.panel.unique():
        s = G[G.panel == pname]
        log(f"  {pname:<9} 4a {int(s.pass4a.sum())}/{len(s)}  4bFULL {int(s.pass4b_full.sum())}/{len(s)}  "
            f"4bOOS {int(s.pass4b_oos.sum())}/{len(s)}")
    log("\n  CHOOSER LICENSING (does an IS-fit G keep the OOS DD cap?):")
    for _, r in C.iterrows():
        log(f"  {r.panel:<9} {r.scope:>6} {r.chooser:<9} G={r.pick_G:5.3f}{r.pick_cadence} "
            f"oosMaxDD {r.oos_MaxDD:7.2%} vs cap {r.oos_dd_cap:7.2%} -> {'HELD' if r.oos_dd_cap_held else 'BREACHED'}"
            f" | oosCAGR {r.oos_CAGR:6.2%} vs floor {r.oos_cagr_floor:6.2%} -> "
            f"{'ok' if r.oos_cagr_floor_held else 'FAIL'} | 4bFULL {r.pass4b_full} 4bOOS {r.pass4b_oos}")

    # headline cell through the protocol's own comparator, for the leaderboard row
    hp = C[(C.panel == "U56") & (C.scope == "joint") & (C.chooser == "C_BUDGET")].iloc[0]
    global HEAD_G, HEAD_CAD; HEAD_G, HEAD_CAD = float(hp.pick_G), str(hp.pick_cadence)
    log("\n=== RULE-8 SPLIT ROBUSTNESS (the licensable G band at three splits, U56/B136/SMALL485) ===")
    log("  A cell is 'licensable' at a split if it clears all five 4b legs on the post-split window.")
    for pname in G.panel.unique():
        for lbl, oc, dc in (("2017", "oos_CAGR", "oos_MaxDD"), ("2015", "alt2015_CAGR", "alt2015_MaxDD"),
                            ("2019", "alt2019_CAGR", "alt2019_MaxDD")):
            sub = G[G.panel == pname]
            sp = SPYREF[pname]
            spc = sp[f"{'oos' if lbl == '2017' else 'alt' + lbl}_CAGR"]
            spd = sp[f"{'oos' if lbl == '2017' else 'alt' + lbl}_MaxDD"]
            ok = sub[(sub[oc] >= 0.70 * spc) & (sub[dc] >= 0.60 * spd)]
            gs = sorted(set(ok.G))
            log(f"  {pname:<9} split {lbl}: SPY post-split CAGR {spc:6.2%} MaxDD {spd:7.2%} -> "
                f"floor {0.70*spc:6.2%} cap {0.60*spd:7.2%} | G clearing DD+CAGR: "
                f"{gs if gs else 'NONE'}  ({len(ok)} of {len(sub)} cells)")

    log("\n=== STRESS YEARS: headline cell vs live RULES v2 vs SPY (U56) ===")
    px0 = panels[0][1]; s0 = px0.index[260]
    spy0 = px0["SPY"].pct_change().fillna(0).loc[s0:]
    live0 = backtest(px0, rules_v2_weights(px0), cost_bps=COST, freq="W")["returns"].loc[s0:]
    head = RET[("U56", HEAD_CAD, HEAD_G)]
    yr = pd.DataFrame({"headline": head, "RULESv2": live0, "SPY": spy0}).groupby(head.index.year).apply(
        lambda x: (1 + x).prod() - 1)
    for y, row in yr.iterrows():
        log(f"  {y}  headline {row.headline:+7.2%}   RULESv2 {row.RULESv2:+7.2%}   SPY {row.SPY:+7.2%}")

    log("\n=== COST-RUNG LADDER on the RECOMMENDED cell, U56 (RULES.md clause 7 claims 5/10/25/50 bps) ===")
    log("  CAVEAT (idea 1063): the ladder is ONE-SIDED — SPY buy-and-hold pays no turnover cost at any")
    log("  rung, so the 4b floor/cap it sets never move while the candidate's CAGR falls.")
    px0 = panels[0][1]; s0 = px0.index[260]
    spy0 = px0["SPY"].pct_change().fillna(0).loc[s0:]
    sp0 = stats(spy0); sp0["H1"], sp0["H2"] = halves(spy0)
    o0 = win(spy0, OOS_START); sp0.update({f"oos_{k}": v for k, v in stats(o0).items()})
    sp0["oos_H1"], sp0["oos_H2"] = halves(o0)
    crows = []
    for bps in (0, 5, 10, 25, 50):
        for g in (0.75, 1.00):
            r = backtest(px0, rules_v2_weights(px0, gross=g), cost_bps=bps, freq="W")["returns"].loc[s0:]
            c = dict(panel="U56", cadence="W", G=g, cost_bps=bps)
            c.update(stats(r)); c["H1"], c["H2"] = halves(r)
            oo = win(r, OOS_START); c.update({f"oos_{k}": v for k, v in stats(oo).items()})
            c["oos_H1"], c["oos_H2"] = halves(oo)
            c["pass4b_full"], lf = keep_4b(c, sp0, "FULL"); c["pass4b_oos"], lo = keep_4b(c, sp0, "OOS")
            c["binding_full"] = "".join(k for k, v in lf.items() if not v) or "-"
            c["binding_oos"] = "".join(k for k, v in lo.items() if not v) or "-"
            crows.append(c)
            log(f"  {bps:>2} bps  G={g:.2f} | CAGR {c['CAGR']:6.2%} (floor {0.70*sp0['CAGR']:.2%}) "
                f"MaxDD {c['MaxDD']:7.2%} (cap {0.60*sp0['MaxDD']:.2%}) Sharpe {c['Sharpe']:.3f} | "
                f"OOS CAGR {c['oos_CAGR']:6.2%} (floor {0.70*sp0['oos_CAGR']:.2%}) | "
                f"4bFULL {str(c['pass4b_full']):<5} 4bOOS {str(c['pass4b_oos']):<5} binding {c['binding_full']}/{c['binding_oos']}")
    pd.DataFrame(crows).to_csv(OUT / f"{STEM}.costladder.csv", index=False)

    log("\n=== baseline.compare() on the two U56 chooser picks ===")
    log("  The RECOMMENDED cell keeps the LIVE cadence (W, PROTOCOL's default and the frozen live value)")
    log("  and changes ONE number, the gross. The joint chooser's M pick is reported, not recommended:")
    log("  preferring W is not a post-hoc choice, it is declining to change a second dial.")
    rows_out = []
    for lbl, (gg, ff) in (("RECOMMENDED (live cadence)", (float(C[(C.panel=="U56")&(C.scope=="cad=W")&(C.chooser=="C_BUDGET")].iloc[0].pick_G), "W")),
                          ("joint chooser pick", (HEAD_G, HEAD_CAD))):
        log(f"\n  -- {lbl}: G={gg:.3f} cadence {ff}")
        res = compare(f"1454 gross {gg:.2f} {ff} (U56, RULES v2 shape)",
                      lambda p, _g=gg: rules_v2_weights(p, gross=_g), px0, freq=ff, cost_bps=COST)
        lines.append(str(res["table"].to_string(float_format=lambda x: f"{x:.3f}")))
        lines.append(res["row"]); rows_out.append(res["row"])
    (OUT / f"{STEM}.console.txt").write_text("\n".join(lines))

if __name__ == "__main__":
    main()

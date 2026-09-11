#!/usr/bin/env python3
"""Idea 796 (lane B, 2026-09-11) — does the DE-GROSSED CASH LEG earn its keep as a
REAL HELD INSTRUMENT?

RULES v2 holds every U56 name inside its 200d +/-3% band at gross/N of NAV and sends the
gated-out weight to CASH. The engine credits that cash **0%**. Over 2009-2026 the live book
holds a mean gross of 0.537, so ~46% of NAV sits idle at zero for the whole record.

Idea 640/642 priced this leg as a FLAT credit (0/150/300 bps) and PARKed "a real T-bill
path" as unavailable. It is not unavailable: SHY / IEF / LQD / TIP / TLT are all committed
U56 columns with real total returns from 2008-01-02. This run prices the leg as an
instrument the book actually HOLDS.

BOOK  CASH(c, gated): w = rules_v2_weights(px, band=0.03, gross=0.75); residual
      r_t = max(0, 1 - sum_i w_it) is added to column c. gated=True holds the sleeve only
      while c is itself IN its own 200d +/-3% band (else the residual stays at 0% cash).
      c = NONE reproduces the live book exactly.

TWO TUNED PARAMETERS (PROTOCOL rule 4): (1) cash instrument c, 6 levels; (2) gated, 2
levels. 11 distinct cells, ALL REPORTED. No leverage: ungated books are exactly fully
invested (sum of weights == 1), gated books sum to <= 1.

Conventions: 10 bps per unit turnover, weekly, weights at t applied at t+1 (engine),
warm-up skipped at px.index[260]. Rule 8: IS = ..2016-12-31 (pick made on IS alone),
OOS = 2017-01-01.. read ONCE. Both KEEP paths evaluated (4a vs RULES v2, 4b vs SPY).

CAVEAT carried into every verdict: universe.json is a CURRENT-CONSTITUENT list
(survivorship bias), and the cash sleeve's payoff is backloaded — T-bill yields were ~0
to 2015 and ~4-5% after 2022 — so the leg is worth strictly more in the OOS window than
in the IS window. This is stated, not adjusted away.

Run: python research/backtests/2026-09-11_does-the-DE-GROSSED-CASH-LEG-earn-its-keep-as-a-REAL-HELD-INSTRUMENT_B.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BAND, GROSS, COST, FREQ = 0.03, 0.75, 10, "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
CASH = [None, "SHY", "IEF", "LQD", "TIP", "TLT"]
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- the book
def cash_book(px, c=None, gated=False, band=BAND, gross=GROSS):
    w = rules_v2_weights(px, band=band, gross=gross)
    if c is None:
        return w
    resid = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    if gated:
        resid = resid.where(band_state(px, band)[c], 0.0)
    w = w.copy()
    w[c] = w[c] + resid
    return w


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def full_row(name, r, oos_start=OOS_START, is_end=IS_END):
    d = dict(book=name)
    d.update(stats(r))
    ir, orr = r.loc[:is_end], r.loc[oos_start:]
    d["IS_Sharpe"] = metrics(ir)["Sharpe"]
    d["IS_CAGR"] = metrics(ir)["CAGR"]
    o = stats(orr)
    d["OOS_CAGR"], d["OOS_Sharpe"], d["OOS_MaxDD"] = o["CAGR"], o["Sharpe"], o["MaxDD"]
    d["OOS_H1"], d["OOS_H2"] = o["H1"], o["H2"]
    return d


def main():
    px = load_universe()
    start = px.index[260]
    print(f"panel {px.shape[0]} rows x {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"scored from {start.date()} (warm-up skipped), IS <= {IS_END}, OOS >= {OOS_START}\n")

    # ---------------------------------------------------------- GATES (pre-registered)
    print("=" * 100)
    print("GATES (5, pre-registered)")
    gates = []

    w_none = cash_book(px, None)
    g1 = float(np.abs(w_none.values - rules_v2_weights(px, band=BAND, gross=GROSS).values).max())
    gates.append(("G1 cash_book(None) == baseline.rules_v2_weights", f"{g1:.3e}", g1 == 0.0))

    w_shy = cash_book(px, "SHY", False)
    tot = w_shy.loc[start:].sum(axis=1)
    g2 = float(np.abs(tot.values - 1.0).max())
    gates.append(("G2 ungated book is EXACTLY fully invested (no leverage, max|sum w - 1|)",
                  f"{g2:.3e}", g2 < 1e-12))

    # G3 no look-ahead: IS statistics on a frame TRUNCATED at IS_END must equal IS
    # statistics taken from the full-sample run.
    px_is = px.loc[:IS_END]
    r_trunc = backtest(px_is, cash_book(px_is, "SHY", False), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    r_full_is = backtest(px, w_shy, cost_bps=COST, freq=FREQ)["returns"].loc[start:IS_END]
    g3 = float(np.abs(r_trunc.reindex(r_full_is.index).values - r_full_is.values).max())
    gates.append(("G3 IS returns identical on a frame truncated at IS_END (no look-ahead)",
                  f"{g3:.3e}", g3 < 1e-12))

    # G4 the sleeve is the residual, added on top of any band weight the cash name earns
    g4 = float(np.abs((w_shy["SHY"] - w_none["SHY"] - (1.0 - w_none.sum(axis=1)).clip(lower=0.0)).values).max())
    gates.append(("G4 w_c == band weight + de-grossed residual (sleeve accounting)", f"{g4:.3e}", g4 < 1e-12))

    # G5 the live baseline reproduces the record's committed U56 RULES v2 row
    r_base = backtest(px, w_none, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    mb = stats(r_base)
    g5 = (abs(mb["CAGR"] - 0.0861) < 5e-4 and abs(mb["Sharpe"] - 1.1998) < 5e-4
          and abs(mb["MaxDD"] + 0.1205) < 5e-4)
    gates.append(("G5 RULES v2 u56 @10bps/W reproduces the committed 8.61% / 1.1998 / -12.05%",
                  f"{mb['CAGR']:.4f} / {mb['Sharpe']:.4f} / {mb['MaxDD']:.4f}", g5))

    for n, v, ok in gates:
        print(f"  {'PASS' if ok else 'FAIL'}  {n}: {v}")
    print()

    # ---------------------------------------------------------- comparands
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ref = [full_row("RULES v2 baseline (live)", r_base),
           full_row("RULES v1 (previous)", backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]),
           full_row("SPY buy-and-hold", spy),
           full_row("CONTROL RULES v2 @ gross 1.00 (the equity way to spend the idle NAV)",
                    backtest(px, rules_v2_weights(px, band=BAND, gross=1.00), cost_bps=COST, freq=FREQ)["returns"].loc[start:])]

    # ---------------------------------------------------------- the grid (all 11 cells)
    grid = []
    for c in CASH:
        for gated in ([False] if c is None else [False, True]):
            res = backtest(px, cash_book(px, c, gated), cost_bps=COST, freq=FREQ)
            r = res["returns"].loc[start:]
            row = full_row(f"CASH={c or 'NONE'} gated={gated}", r)
            row["cash"], row["gated"] = (c or "NONE"), gated
            row["turnover_pa"] = res["turnover"].loc[start:].sum() / metrics(r)["Years"]
            grid.append(row)

    gdf = pd.DataFrame(grid)
    b, s = ref[0], ref[2]

    # KEEP paths (PROTOCOL rule 4), evaluated on EVERY cell
    dd_cap, cagr_floor = 0.60 * abs(s["MaxDD"]), 0.70 * s["CAGR"]
    o_dd_cap, o_cagr_floor = 0.60 * abs(s["OOS_MaxDD"]), 0.70 * s["OOS_CAGR"]
    gdf["pass4a"] = (gdf.H1 > b["H1"]) & (gdf.H2 > b["H2"]) & (gdf.MaxDD >= b["MaxDD"])
    gdf["pass4b"] = ((gdf.H1 > s["H1"]) & (gdf.H2 > s["H2"]) & (gdf.OOS_Sharpe > s["OOS_Sharpe"])
                     & (gdf.MaxDD >= -dd_cap) & (gdf.CAGR >= cagr_floor)
                     & (gdf.OOS_MaxDD >= -o_dd_cap) & (gdf.OOS_CAGR >= o_cagr_floor))

    cols = ["book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover_pa", "pass4a", "pass4b"]
    fmt = lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)

    print("=" * 100)
    print("THE GRID — 11 cells (2 tuned parameters: cash instrument x gated), ALL REPORTED")
    print(gdf[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print()
    print("COMPARANDS")
    print(pd.DataFrame(ref)[["book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print()
    print(f"4a bar: Sharpe > RULES v2 in BOTH halves ({b['H1']:.4f} / {b['H2']:.4f}) and MaxDD >= {b['MaxDD']:.4f}")
    print(f"4b bar: Sharpe > SPY in BOTH halves ({s['H1']:.4f} / {s['H2']:.4f}) AND OOS ({s['OOS_Sharpe']:.4f}); "
          f"MaxDD >= {-dd_cap:.4f} (full) / {-o_dd_cap:.4f} (OOS); CAGR >= {cagr_floor:.4f} (full) / {o_cagr_floor:.4f} (OOS)")
    print(f"4a passes: {int(gdf.pass4a.sum())} of {len(gdf)}    4b passes: {int(gdf.pass4b.sum())} of {len(gdf)}")
    print()

    # ---------------------------------------------------------- RULE 8 walk-forward
    print("=" * 100)
    print("RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 ONLY, OOS 2017+ read ONCE")
    cand = gdf[gdf.cash != "NONE"]
    pick = cand.loc[cand.IS_Sharpe.idxmax()]
    pick_cagr = cand.loc[cand.IS_CAGR.idxmax()]
    print(f"  IS window {start.date()} .. {IS_END}")
    print("  IS ranking (the only information the selector may use):")
    print(cand[["book", "IS_Sharpe", "IS_CAGR"]].sort_values("IS_Sharpe", ascending=False)
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  PICK (declared rule: max IS Sharpe among the cash arms) -> {pick['book']}")
    print(f"  ALT  (max IS CAGR, reported for transport)               -> {pick_cagr['book']}")
    for tag, p in (("PICK", pick), ("ALT", pick_cagr)):
        print(f"\n  {tag} {p['book']}")
        print(f"    OOS CAGR {p['OOS_CAGR']:.4f}  Sharpe {p['OOS_Sharpe']:.4f}  MaxDD {p['OOS_MaxDD']:.4f}"
              f"  (OOS halves {p['OOS_H1']:.4f} / {p['OOS_H2']:.4f})")
        print(f"    vs RULES v2  {b['OOS_CAGR']:.4f} / {b['OOS_Sharpe']:.4f} / {b['OOS_MaxDD']:.4f}")
        print(f"    vs SPY       {s['OOS_CAGR']:.4f} / {s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:.4f}")
        print(f"    OOS 4a (Sharpe > v2 OOS and MaxDD no worse): "
              f"{bool(p['OOS_Sharpe'] > b['OOS_Sharpe'] and p['OOS_MaxDD'] >= b['OOS_MaxDD'])}")
        print(f"    OOS 4b (CAGR >= {o_cagr_floor:.4f}, MaxDD >= {-o_dd_cap:.4f}, Sharpe > SPY): "
              f"{bool(p['OOS_CAGR'] >= o_cagr_floor and p['OOS_MaxDD'] >= -o_dd_cap and p['OOS_Sharpe'] > s['OOS_Sharpe'])}"
              f"  [CAGR shortfall {p['OOS_CAGR'] - o_cagr_floor:+.4f}]")
    rho = cand.IS_Sharpe.rank().corr(cand.OOS_Sharpe.rank(), method="pearson")
    print(f"\n  IS->OOS rank transport over the 10 cash arms: Spearman {rho:+.4f}")

    # transport is the whole question for a rule-8 KEEP: does the IS pick stay best OOS?
    best_oos = cand.loc[cand.OOS_Sharpe.idxmax()]
    print(f"  best OOS Sharpe arm: {best_oos['book']} ({best_oos['OOS_Sharpe']:.4f}); "
          f"the IS pick reads {pick['OOS_Sharpe']:.4f} — selection cost {pick['OOS_Sharpe'] - best_oos['OOS_Sharpe']:+.4f}")

    # ------------------------------------------------------- WF-B: three DECISION RULES
    # The grid selector above is a returns-fitted choice. A cash sleeve can also be chosen
    # by an a-priori property of the instrument that no return series enters: its
    # DURATION, which is a product definition (SHY 1-3y UST, TIP ~7y real, IEF 7-10y UST,
    # LQD ~8y IG credit, TLT 20y+ UST). DUR is declared here as a constant, not fitted.
    DUR = {"SHY": 1.9, "TIP": 7.0, "IEF": 7.5, "LQD": 8.5, "TLT": 17.0}
    print("\n" + "=" * 100)
    print("RULE 8 — WF-B: three DECISION RULES for the sleeve, each read ONCE on 2017+")
    print("  (a) NEVER     — the incumbent, cash at 0% (zero parameters)")
    print("  (b) IS-ARGMAX — the returns-fitted selector above (two tuned parameters)")
    print("  (c) SHORTEST  — hold the shortest-DURATION arm, ungated (zero tuned parameters;")
    print("                  duration is a product definition, no return series enters)")
    ung = gdf[(gdf.cash != "NONE") & (~gdf.gated)].copy()
    ung["dur"] = ung.cash.map(DUR)
    ung = ung.sort_values("dur")
    print("\n  DURATION LADDER (ungated arms, ordered a priori by duration):")
    print(ung[["cash", "dur", "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    r_is = ung.dur.rank().corr(ung.IS_Sharpe.rank())
    r_oos = ung.dur.rank().corr(ung.OOS_Sharpe.rank())
    r_is4 = ung.iloc[:4].dur.rank().corr(ung.iloc[:4].IS_Sharpe.rank())
    r_oos4 = ung.iloc[:4].dur.rank().corr(ung.iloc[:4].OOS_Sharpe.rank())
    print(f"  Spearman(duration, IS Sharpe)  {r_is:+.4f} over 5 rungs / {r_is4:+.4f} over the first 4")
    print(f"  Spearman(duration, OOS Sharpe) {r_oos:+.4f} over 5 rungs / {r_oos4:+.4f} over the first 4")
    print("  READ HONESTLY: the 5-rung IS figure is EXACTLY zero, not a duration premium — IS Sharpe")
    print("  rises monotonically over SHY<TIP<IEF<LQD and then TLT, the longest rung, is worst of five,")
    print("  which cancels the rank correlation. OOS is monotone DECREASING across all five with no")
    print("  exception. So the transportable statement is the OOS one: over 2017-2026 (which contains")
    print("  2022) every step up the duration ladder costs Sharpe, and the IS window does not say so.")

    shortest = ung.iloc[0]
    decisions = [("(a) NEVER (incumbent)", b), ("(b) IS-ARGMAX", pick), ("(c) SHORTEST", shortest)]
    print()
    for tag, d in decisions:
        p4a = bool(d["OOS_Sharpe"] > b["OOS_Sharpe"] and d["OOS_MaxDD"] >= b["OOS_MaxDD"]) if tag != "(a) NEVER (incumbent)" else None
        print(f"  {tag:24s} OOS CAGR {d['OOS_CAGR']:.4f}  Sharpe {d['OOS_Sharpe']:.4f}  MaxDD {d['OOS_MaxDD']:.4f}"
              f"  halves {d['OOS_H1']:.4f}/{d['OOS_H2']:.4f}"
              + ("" if p4a is None else f"   OOS-4a vs incumbent: {p4a}"))
    print(f"\n  SHORTEST full-sample 4a: halves {shortest['H1']:.4f} > {b['H1']:.4f} and "
          f"{shortest['H2']:.4f} > {b['H2']:.4f}, MaxDD {shortest['MaxDD']:.4f} >= {b['MaxDD']:.4f} "
          f"-> {bool(shortest['pass4a'])}")
    print(f"  SHORTEST 4b CAGR floor: OOS {shortest['OOS_CAGR']:.4f} vs floor {o_cagr_floor:.4f} "
          f"-> shortfall {shortest['OOS_CAGR'] - o_cagr_floor:+.4f}  (4b {bool(shortest['pass4b'])})")
    print("\n  HONESTY NOTE: SHORTEST was named AFTER the grid was read. Its a-priori content is")
    print("  real (duration is not a return statistic and the duration->Sharpe sign flip is a")
    print("  mechanism, not a fit), but it was not pre-registered, so it is reported as a")
    print("  PARK-strength claim and NOT as a clean rule-8 KEEP.")

    # ---------------------------------------------------------- the backloading caveat, measured
    print("\n" + "=" * 100)
    print("BACKLOADING (the reason idea 642 parked this): the cash leg's own return by window")
    for c in CASH[1:]:
        sr = px[c].pct_change().fillna(0).loc[start:]
        print(f"  {c}: full CAGR {metrics(sr)['CAGR']:.4f}  IS {metrics(sr.loc[:IS_END])['CAGR']:.4f}"
              f"  OOS {metrics(sr.loc[OOS_START:])['CAGR']:.4f}")
    idle = (1.0 - w_none.loc[start:].sum(axis=1))
    print(f"  mean idle NAV in the live book: {idle.mean():.4f}  (IS {idle.loc[:IS_END].mean():.4f}, "
          f"OOS {idle.loc[OOS_START:].mean():.4f})")

    gdf.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    pd.DataFrame(ref).to_csv(OUT.with_suffix(".comparands.csv"), index=False)
    print(f"\nwrote {OUT.with_suffix('.grid.csv').name} and {OUT.with_suffix('.comparands.csv').name}")

    # ---------------------------------------------------------- leaderboard rows
    p = gdf[gdf.book == pick["book"]].iloc[0]
    script = Path(__file__).name
    print("\nLEADERBOARD rows:")
    print(f"| 2026-09-11 | 796 GATES — five, pre-registered | n/a | n/a | n/a | n/a | engine.backtest; baseline.rules_v2_weights | "
          + "; ".join(f"{n.split(' ')[0]} **{v}**" for n, v, _ in gates)
          + f" — {'ALL PASS' if all(ok for _, _, ok in gates) else 'FAILURE'} | GATES | {script} |")
    print(f"| 2026-09-11 | 796 THE GRID — 11 cells (cash instrument x gated), all reported | "
          f"best full CAGR {gdf.CAGR.max():.2%} vs RULES v2 {b['CAGR']:.2%} and SPY {s['CAGR']:.2%} | "
          f"best Sharpe {gdf.Sharpe.max():.4f} vs {b['Sharpe']:.4f} | "
          f"best MaxDD {gdf.MaxDD.max():.2%} vs {b['MaxDD']:.2%} | "
          f"4a {int(gdf.pass4a.sum())}/11, 4b {int(gdf.pass4b.sum())}/11 | RULES v2 {b['Sharpe']:.4f} ({b['H1']:.4f}/{b['H2']:.4f}) | "
          f"GRID | {script} |")
    print(f"| 2026-09-11 | 796 RULE 8 — pick made on 2009-2016 by IS Sharpe, OOS 2017+ read ONCE | "
          f"{p['book']} OOS CAGR {p['OOS_CAGR']:.2%} vs RULES v2 {b['OOS_CAGR']:.2%} and SPY {s['OOS_CAGR']:.2%} | "
          f"OOS Sharpe {p['OOS_Sharpe']:.4f} vs {b['OOS_Sharpe']:.4f} / {s['OOS_Sharpe']:.4f} | "
          f"OOS MaxDD {p['OOS_MaxDD']:.2%} vs {b['OOS_MaxDD']:.2%} / {s['OOS_MaxDD']:.2%} | "
          f"full halves {p['H1']:.4f} / {p['H2']:.4f} | RULES v2 {b['Sharpe']:.4f} ({b['H1']:.4f}/{b['H2']:.4f}) | "
          f"{'KEEP-4a' if p['pass4a'] else 'KILL'} | {script} |")
    sh = gdf[gdf.book == shortest["book"]].iloc[0]
    print(f"| 2026-09-11 | 796 RULE 8 WF-B — three decision rules (NEVER / IS-ARGMAX / SHORTEST-duration), each read ONCE on 2017+ | "
          f"SHORTEST (SHY) OOS CAGR {sh['OOS_CAGR']:.2%} vs incumbent {b['OOS_CAGR']:.2%}, IS-ARGMAX {p['OOS_CAGR']:.2%}, SPY {s['OOS_CAGR']:.2%} | "
          f"OOS Sharpe {sh['OOS_Sharpe']:.4f} vs {b['OOS_Sharpe']:.4f} / {p['OOS_Sharpe']:.4f} / {s['OOS_Sharpe']:.4f} | "
          f"OOS MaxDD {sh['OOS_MaxDD']:.2%} vs {b['OOS_MaxDD']:.2%} / {p['OOS_MaxDD']:.2%} | "
          f"Spearman(duration, IS Sharpe) **{r_is:+.4f}** over 5 rungs ({r_is4:+.4f} over the first 4, TLT reverses it) vs "
          f"(duration, OOS Sharpe) **{r_oos:+.4f}**, monotone with no exception | "
          f"RULES v2 {b['Sharpe']:.4f} ({b['H1']:.4f}/{b['H2']:.4f}) | "
          f"PARK (4a on both paths, not pre-registered) | {script} |")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
IDEA 563 - is the MA GATE worse than MOMENTUM at matched daily depth a BOOK-LEVEL fact?
=======================================================================================
Cloud lane, 2026-09-11.

THE QUESTION.  Idea 559 closed the depth-mismatch channel (k_t pinned daily, not on average)
and then swapped the ranker for the record's 12-1 momentum (MOM-D).  Its SELECTION leg

    SELECTION = 100 x (CAGR(MA-THRESH, zero-cost) - CAGR(MOM-D, zero-cost))

came out NEGATIVE in 22 of 27 (panel, theta) cells - U56 -0.3642, B136 -1.1499,
SMALL439 -1.2430 pp/yr - i.e. at identical daily depth the momentum slice picks BETTER names
than the MA slice.  That is a zero-cost leg on one cadence and one gross.  A leg is not a book.
This run asks the only version that could move capital:

    does the daily-depth-matched MOMENTUM slice beat the MA slice AS A BOOK - after 10 bps
    per unit turnover and next-day execution, across cadence and gross, on both KEEP paths
    and under rule 8?

CONSTRUCTION (idea 559's, verbatim, then priced as books).
  cell = (panel, theta):
    MA-THRESH  = px > MA200 * (1 + theta)                       [the live rule's gate form]
    MOM-D      = top k_t names by 12-1 momentum, k_t = |MA-THRESH_t| pinned EVERY DAY
                 (idea 559's daily match: the two arms hold the same NUMBER of names each day,
                  so gross exposure is identical by construction and only the NAMES differ)
    book       = RESPREAD (gross/k_t on held names) - 559's primary form
                 DEGROSS  (gross/n_live on held names, rest to CASH) - REPORTED contrast
    costs      = 10 bps per unit turnover, next-day execution (engine convention).
                 0 and 25 bps are derived EXACTLY off the same held path (gate G1) and reported.

TUNED PARAMETERS - exactly 2, every grid point reported:
  (1) CADENCE  in {D, W, M, Q}
  (2) GROSS    in {0.50, 0.75, 1.00}
  panel (3) x theta (9) x arm (2) x construction (2) are REPORTED axes, never selected over.
  Full grid = 3 x 9 x 2 x 2 x 4 x 3 = 1,296 books, all in .grid.csv.

RULE 8 WALK-FORWARD (required).  IS = start..2016-12-31, OOS = 2017-01-01..end, read once.
  Within each (panel, theta, arm, construction) the two tuned dials are chosen on IS Sharpe
  ALONE; the OOS is then read once and scored against RULES v2 on the same panel and against
  SPY.  The head-to-head is re-read at the picks: does MOM-D's pick beat MA-THRESH's pick OOS?

BOTH KEEP PATHS on every one of the 1,296 books:
  4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2's.
  4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

GATES (pre-registered, all reported pass or fail):
  G0  fast_run reproduces engine.backtest returns AND turnover to 1e-12 (every panel, D and W).
  G1  the derived cost rung (gross returns - turnover x c) equals a fresh fast_run at c to 1e-15.
  G2  DAILY DEPTH MATCH.  idea 559's `daily_matched` clips k_t to the RANKABLE count, and 12-1
      momentum needs 252 closes where the 200d MA needs 200, so on names aged 200-251 days the
      match cannot be exact and k_MOM-D < k_MA.  The gate is therefore a REPRODUCTION of idea
      559's committed `.match.csv` `dk_md` column (mean |k_MOM-D - k_MA| per cell) to 1e-9, with
      the exact-match share, the mean and the max reported beside it.
  G3  reproduction of idea 559's committed .legs.csv MOM-D / cadence W / FULL sel_geo_pp on all
      27 cells to 1e-9 (zero cost, RESPREAD, gross 0.75).
  G4  gross identity: on every day where the depth match IS exact, the two arms' TARGET gross is
      equal to 1e-12 on every cell x dial (the residual on the clipped days is reported).

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only - dead names are absent, CAGR
levels are inflated and neither KEEP column is immune.  The 44 SMALL names with
max_1d_move >= 1.0 are dropped first (data/small_meta.csv), idea 559's own filter.  The
head-to-head is arm-minus-arm inside one panel at identical depth, where the bias very largely
cancels; the KEEP columns and the rule-8 levels are not protected and are read with that caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .head2head.csv .walkforward.csv .keeppaths.csv .rungs.csv .match.csv .g3.csv
         .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
RUNGS = [0, 10, 25]
PANELS = ["U56", "B136", "SMALL439"]
THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
ARMS = ["MA-THRESH", "MOM-D"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
CADENCES = ["D", "W", "M", "Q"]          # tuned param 1
GROSSES = [0.50, 0.75, 1.00]             # tuned param 2
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS = 1e-12
BAR_ENGINE = 1e-12
BAR_RUNG = 1e-15
BAR_REPRO = 1e-9

IDEA559 = REPO / "research" / "backtests" / \
    "2026-09-09_what-does-SELECTION-become-under-a-DAILY-depth-match_C.legs.csv"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 800)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def fast_run(px, W, freq):
    """engine.backtest's arithmetic, returning the ZERO-COST return path and turnover so any
    cost rung can be derived exactly (gate G1)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    r0 = np.nansum(held * rets, axis=1)
    return (pd.Series(r0, index=px.index), pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))


def rung(r0, turn, c):
    return r0 - turn * c / 1e4


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def cagr(r):
    return metrics(r)["CAGR"]


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def mom_rank(px):
    return (px.shift(21) / px.shift(252) - 1).where(live_mask(px))


def daily_matched(sig, live, gm):
    """idea 559's daily match: k_t = k_ma_t every day, clipped to the rankable count."""
    k_ma = gm.sum(axis=1)
    kt = np.minimum(k_ma, sig.notna().sum(axis=1))
    return sig.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def book(px, g, construction, gross):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


# ================================================================== main
def main():
    P("=" * 185)
    P("IDEA 563 - is the MA GATE worse than MOMENTUM at matched daily depth a BOOK-LEVEL fact?"
      "   cloud, 2026-09-11")
    P("=" * 185)
    P("PROTOCOL: 10 bps per unit turnover (0 and 25 derived exactly and reported), next-day")
    P("execution (engine), no shorting, no leverage.  IS = start..%s, OOS = %s..end, read once."
      % (IS_END, OOS_START))
    P(f"2 tuned params: CADENCE {CADENCES} x GROSS {GROSSES}.  Panel x theta x arm x construction")
    P("are reported axes, never selected over.  Both KEEP paths on every one of the 1,296 books.")
    P("SURVIVORSHIP: B136/SMALL439 are current constituents only; CAGR inflated, KEEP not immune.")
    flush_log()

    u, b = load_universe(), load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    PN = {"U56": (u.drop(columns=["SPY"]), u["SPY"]),
          "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
          "SMALL439": (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])}
    P("\nPanels: " + "  ".join(f"{k} {v[0].shape[1]}x{len(v[0])}" for k, v in PN.items())
      + f"   ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")

    # -------------------------------------------------------------- G0 / G1
    P("\n" + "=" * 185)
    P("G0  fast_run vs engine.backtest      G1  derived cost rung vs a fresh run at that rung")
    P("=" * 185)
    g0 = g1 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        W = rules_v2_weights(px)
        for freq in ("D", "W"):
            a = backtest(px, W, cost_bps=COST_BPS, freq=freq)
            r0, tn, _ = fast_run(px, W, freq)
            g0 = max(g0, float((a["returns"] - rung(r0, tn, COST_BPS)).abs().max()),
                     float((a["turnover"] - tn).abs().max()))
            a25 = backtest(px, W, cost_bps=25, freq=freq)
            g1 = max(g1, float((a25["returns"] - rung(r0, tn, 25)).abs().max()))
        P(f"  {pn:9s} G0 {g0:.3e}   G1 {g1:.3e}")
    P(f"  G0 max {g0:.3e} (bar {BAR_ENGINE:.0e})  {'PASS' if g0 < BAR_ENGINE else 'FAIL'}   "
      f"G1 max {g1:.3e} (bar {BAR_RUNG:.0e})  {'PASS' if g1 < BAR_RUNG else 'FAIL'}")
    flush_log()

    # -------------------------------------------------------------- comparands
    COMP = {}
    P("\n" + "=" * 185)
    P("COMPARANDS (per panel, over the same window every book is scored on)")
    P("=" * 185)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        r0, tn, _ = fast_run(px, rules_v2_weights(px), "W")
        live_s = stat(rung(r0, tn, COST_BPS).loc[start:])
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        COMP[pn] = dict(live=live_s, spy=spy_s, start=start, years=years)
        P(f"  {pn:9s} {start.date()}..{px.index[-1].date()} ({years:.2f} yrs, {px.shape[1]} names)")
        P(f"      RULES v2 (4a bar) CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} H1/H2 {live_s['H1']:.4f}/{live_s['H2']:.4f}  "
          f"OOS {live_s['oCAGR']:.4f}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f}")
        P(f"      SPY      (4b bar) CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f} H1/H2 {spy_s['H1']:.4f}/{spy_s['H2']:.4f}  "
          f"OOS {spy_s['oCAGR']:.4f}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
        P(f"      4b bars: H1>{spy_s['H1']:.4f} H2>{spy_s['H2']:.4f} OOS>{spy_s['oSharpe']:.4f} "
          f"MaxDD>=-{0.60*abs(spy_s['MaxDD']):.2%} CAGR>={0.70*spy_s['CAGR']:.2%}")
    flush_log()

    # -------------------------------------------------------------- the grid
    P("\n" + "=" * 185)
    P("THE GRID - 3 panels x 9 theta x 2 arms x 2 constructions x 4 cadences x 3 gross = 1,296 books")
    P("=" * 185)
    rows, repro, match, g4 = [], [], [], 0.0
    for pn in PANELS:
        px, spy_px = PN[pn]
        start, years = COMP[pn]["start"], COMP[pn]["years"]
        live_s, spy_s = COMP[pn]["live"], COMP[pn]["spy"]
        live = live_mask(px)
        mom = mom_rank(px)
        R = px.pct_change().fillna(0.0)
        for th in THETA:
            gates = {"MA-THRESH": ma_gate(px, th)}
            gates["MOM-D"] = daily_matched(mom, live, gates["MA-THRESH"])
            dk = (gates["MOM-D"].sum(axis=1).loc[start:]
                  - gates["MA-THRESH"].sum(axis=1).loc[start:])
            exact = dk == 0
            match.append(dict(panel=pn, theta=th, k_ma=float(gates["MA-THRESH"].sum(axis=1)
                                                             .loc[start:].mean()),
                              k_md=float(gates["MOM-D"].sum(axis=1).loc[start:].mean()),
                              dk_md=float(dk.abs().mean()), dk_max=float(dk.abs().max()),
                              exact_share=float(exact.mean()),
                              mom_rankable=float(mom.loc[start:].notna().sum(axis=1).mean()),
                              nlive=float(live.loc[start:].sum(axis=1).mean())))
            for con in CONSTRUCTIONS:
                for gr in GROSSES:
                    W = {a: book(px, gates[a], con, gr) for a in ARMS}
                    dg = (W["MA-THRESH"].sum(axis=1).loc[start:]
                          - W["MOM-D"].sum(axis=1).loc[start:]).abs()
                    g4 = max(g4, float(dg[exact].max()))
                    for cad in CADENCES:
                        for a in ARMS:
                            r0, tn, gx = fast_run(px, W[a], cad)
                            d = dict(panel=pn, theta=th, arm=a, construction=con, cadence=cad,
                                     gross=gr, turn_yr=float(tn.loc[start:].sum() / years),
                                     mean_gross=float(gx.loc[start:].mean()),
                                     n_held=float(gates[a].loc[start:].sum(axis=1).mean()))
                            for c in RUNGS:
                                sc = stat(rung(r0, tn, c).loc[start:])
                                if c == COST_BPS:
                                    d.update(sc)
                                    d["p4a"] = verdict_4a(sc, live_s)
                                    d["f4b"] = fail_4b(sc, spy_s)
                                else:
                                    d[f"Sharpe_{c}"] = sc["Sharpe"]
                                    d[f"CAGR_{c}"] = sc["CAGR"]
                                    d[f"oSharpe_{c}"] = sc["oSharpe"]
                            # idea 559's zero-cost SELECTION reference cell
                            if con == "RESPREAD" and gr == 0.75 and cad == "W":
                                repro.append(dict(panel=pn, theta=th, arm=a,
                                                  cagr0=cagr(r0.loc[start:]),
                                                  n_held=d["n_held"]))
                            rows.append(d)
        P(f"  {pn}: {len(THETA)*len(CONSTRUCTIONS)*len(GROSSES)*len(CADENCES)*len(ARMS)} books done")
        flush_log()

    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    MT = pd.DataFrame(match)
    MT.to_csv(f"{OUT}.match.csv", index=False)
    P(f"\n  G2 DAILY DEPTH MATCH over the {len(MT)} cells: mean |k_MOM-D - k_MA| = "
      f"{MT.dk_md.mean():.4f} names/day, max {MT.dk_max.max():.0f}, exactly matched on "
      f"{MT.exact_share.mean():.4%} of (cell, day) pairs.")
    ref559 = REPO / "research" / "backtests" / \
        "2026-09-09_what-does-SELECTION-become-under-a-DAILY-depth-match_C.match.csv"
    if ref559.exists():
        rm = pd.read_csv(ref559).set_index(["panel", "theta"])["dk_md"]
        mm = pd.concat([rm.rename("ref"), MT.set_index(["panel", "theta"]).dk_md.rename("mine")],
                       axis=1).dropna()
        g2 = float((mm.ref - mm.mine).abs().max())
        P(f"     reproduction of idea 559's committed .match.csv dk_md on {len(mm)} cells: "
          f"{g2:.3e}  (bar {BAR_REPRO:.0e})  {'PASS' if g2 < BAR_REPRO else 'FAIL'}")
        P(f"     per panel: " + "  ".join(
            f"{p} {float((mm.xs(p).ref - mm.xs(p).mine).abs().max()):.3e}" for p in PANELS))
    else:
        g2 = np.nan
        P("     G2 reference .match.csv not on disk")
    P("     the clip is a HISTORY-LENGTH fact: 12-1 momentum needs 252 closes where the 200d MA "
      "needs 200, so a name aged 200-251 days is gateable but not rankable.  It bites only at "
      "the loosest thresholds:")
    P("       " + "  ".join(f"{p} max dk_md {MT[MT.panel == p].dk_md.max():.4f}" for p in PANELS))
    P(f"  G4 target-gross identity ON THE EXACTLY-MATCHED DAYS, max |sum W_MA - sum W_MOM| = "
      f"{g4:.3e}  (bar 1e-12)  {'PASS' if g4 < 1e-12 else 'FAIL'}")

    # -------------------------------------------------------------- G3 reproduction
    RPd = pd.DataFrame(repro)
    RP = RPd.pivot_table(index=["panel", "theta"], columns="arm", values="cagr0")
    RP["sel_geo_pp"] = 100 * (RP["MA-THRESH"] - RP["MOM-D"])
    RP["n_held"] = RPd[RPd.arm == "MA-THRESH"].set_index(["panel", "theta"]).n_held
    if IDEA559.exists():
        ref = pd.read_csv(IDEA559)
        ref = ref[(ref.qfam == "MOM-D") & (ref.cad == "W") & (ref.window == "FULL")] \
            .set_index(["panel", "theta"])["sel_geo_pp"]
        m = pd.concat([ref.rename("ref"), RP["sel_geo_pp"].rename("mine"),
                       RP["n_held"]], axis=1).dropna()
        m["d"] = (m.ref - m.mine).abs()
        g3 = float(m.d.max())
        bypanel = m.groupby(level=0).d.max()
        P(f"  G3 reproduction of idea 559's MOM-D/W/FULL SELECTION on {len(m)} cells: max "
          f"{g3:.3e}  (bar {BAR_REPRO:.0e})  {'PASS' if g3 < BAR_REPRO else 'FAIL'}")
        P("     per panel max residue: " + "  ".join(f"{k} {v:.3e}" for k, v in bypanel.items()))
        P("     per panel mean SELECTION, ref vs mine: " + "  ".join(
            f"{p} {m.xs(p).ref.mean():+.4f} / {m.xs(p).mine.mean():+.4f}" for p in PANELS))
        P(f"     negative cells: ref {int((m.ref < 0).sum())}/{len(m)}  "
          f"mine {int((m.mine < 0).sum())}/{len(m)}   (idea 559 published 22/27)")
        static = float(bypanel.drop("U56", errors="ignore").max())
        P(f"     DIAGNOSIS: the two STATIC caches (prices_broad, prices_small) reproduce to "
          f"{static:.3e}; the whole residue is U56, whose data/prices.csv is RE-DOWNLOADED "
          f"daily (idea 560's G2b vintage finding, same cause).")
        u = m.xs("U56") if "U56" in m.index.get_level_values(0) else None
        if u is not None:
            P("     U56 residue vs book breadth (thin books restate hardest):")
            P("       " + "  ".join(f"th {t:+.2f}: n {r.n_held:5.1f} d {r.d:.2e}"
                                    for t, r in u.iterrows()))
        m.to_csv(f"{OUT}.g3.csv")
    else:
        g3 = np.nan
        P("  G3 SKIPPED - idea 559 legs.csv not on disk")
    flush_log()

    # -------------------------------------------------------------- head-to-head
    P("\n" + "=" * 185)
    P("A.  HEAD-TO-HEAD AS A BOOK - MOM-D minus MA-THRESH at 10 bps, every dial reported")
    P("=" * 185)
    key = ["panel", "theta", "construction", "cadence", "gross"]
    piv = G.pivot_table(index=key, columns="arm",
                        values=["Sharpe", "CAGR", "MaxDD", "oSharpe", "oCAGR", "oMaxDD",
                                "isSharpe", "turn_yr", "Sharpe_0", "Sharpe_25"])
    H = pd.DataFrame(index=piv.index)
    for c in ["Sharpe", "CAGR", "MaxDD", "oSharpe", "oCAGR", "oMaxDD", "isSharpe", "turn_yr",
              "Sharpe_0", "Sharpe_25"]:
        H[f"d{c}"] = piv[(c, "MOM-D")] - piv[(c, "MA-THRESH")]
    H["mom_wins"] = H.dSharpe > 0
    H["mom_wins_CAGR"] = H.dCAGR > 0
    H["mom_wins_0bps"] = H.dSharpe_0 > 0
    H["mom_wins_25bps"] = H.dSharpe_25 > 0
    H["mom_wins_OOS"] = H.doSharpe > 0
    H = H.reset_index()
    H.to_csv(f"{OUT}.head2head.csv", index=False)

    P(f"  Pooled over all {len(H)} matched cell x dial pairs (RESPREAD + DEGROSS):")
    P(f"    MOM-D beats MA-THRESH on FULL-SAMPLE Sharpe at 10 bps: "
      f"{int(H.mom_wins.sum())}/{len(H)} = {H.mom_wins.mean():.1%}   "
      f"mean dSharpe {H.dSharpe.mean():+.4f}  median {H.dSharpe.median():+.4f}")
    P(f"    on CAGR: {H.mom_wins_CAGR.mean():.1%}  mean dCAGR {100*H.dCAGR.mean():+.3f} pp/yr   "
      f"(idea 559's zero-cost leg read -0.36 / -1.15 / -1.24 pp, i.e. MOM-D ahead)")
    P(f"    at 0 bps {H.mom_wins_0bps.mean():.1%}   at 25 bps {H.mom_wins_25bps.mean():.1%}   "
      f"OOS {H.mom_wins_OOS.mean():.1%}")
    P(f"    mean dTurnover {H.dturn_yr.mean():+.3f} x/yr   mean dMaxDD "
      f"{100*H.dMaxDD.mean():+.3f} pp")
    P("\n  BY CADENCE x GROSS (RESPREAD, share of the 27 cells where MOM-D wins on Sharpe @10bps):")
    for con in CONSTRUCTIONS:
        sub = H[H.construction == con]
        P(f"    {con}:")
        P(fmt(sub.pivot_table(index="cadence", columns="gross", values="mom_wins")
              .reindex(CADENCES), 3).replace("\n", "\n      "))
        P(f"      mean dSharpe by cadence: " + "  ".join(
            f"{c} {sub[sub.cadence == c].dSharpe.mean():+.4f}" for c in CADENCES))
    P("\n  BY PANEL (all dials, both constructions):")
    P(fmt(H.groupby("panel").agg(pairs=("mom_wins", "size"), win=("mom_wins", "mean"),
                                 dSharpe=("dSharpe", "mean"), dCAGR=("dCAGR", "mean"),
                                 dMaxDD=("dMaxDD", "mean"), dturn=("dturn_yr", "mean"),
                                 win_oos=("mom_wins_OOS", "mean"))))
    P("\n  BY THETA (all dials, both constructions):")
    P(fmt(H.groupby("theta").agg(pairs=("mom_wins", "size"), win=("mom_wins", "mean"),
                                 dSharpe=("dSharpe", "mean"), dCAGR=("dCAGR", "mean"),
                                 win_oos=("mom_wins_OOS", "mean"))))
    flush_log()

    # -------------------------------------------------------------- cost decomposition
    P("\n" + "=" * 185)
    P("B.  WHAT THE COST RUNG DOES TO THE LEG (exact re-pricing off the same held path)")
    P("=" * 185)
    rr = []
    for c, col in ((0, "dSharpe_0"), (10, "dSharpe"), (25, "dSharpe_25")):
        rr.append(dict(rung_bps=c, mom_win=float((H[col] > 0).mean()),
                       mean_dSharpe=float(H[col].mean()), median=float(H[col].median())))
    RG = pd.DataFrame(rr)
    P(fmt(RG))
    RG.to_csv(f"{OUT}.rungs.csv", index=False)
    P(f"  The two arms' turnover differs by {H.dturn_yr.mean():+.3f} x/yr on average "
      f"(MOM-D minus MA-THRESH), so the rung moves the head-to-head by "
      f"{RG.mean_dSharpe.iloc[2] - RG.mean_dSharpe.iloc[0]:+.4f} of Sharpe over 0->25 bps.")
    flush_log()

    # -------------------------------------------------------------- rule 8
    P("\n" + "=" * 185)
    P("C.  RULE 8 - (cadence, gross) chosen on IS Sharpe alone; OOS read once")
    P("=" * 185)
    wf = []
    for (pn, th, a, con), g in G.groupby(["panel", "theta", "arm", "construction"]):
        pick = g.loc[g.isSharpe.idxmax()]
        lv, sp = COMP[pn]["live"], COMP[pn]["spy"]
        wf.append(dict(panel=pn, theta=th, arm=a, construction=con, cadence=pick.cadence,
                       gross=pick.gross, IS_spread=float(g.isSharpe.max() - g.isSharpe.min()),
                       CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD, H1=pick.H1,
                       H2=pick.H2, isSharpe=pick.isSharpe, oCAGR=pick.oCAGR,
                       oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD, turn_yr=pick.turn_yr,
                       base_oSharpe=lv["oSharpe"], base_oCAGR=lv["oCAGR"],
                       base_oMaxDD=lv["oMaxDD"], spy_oSharpe=sp["oSharpe"],
                       spy_oCAGR=sp["oCAGR"], spy_oMaxDD=sp["oMaxDD"],
                       beat_base=bool(pick.oSharpe > lv["oSharpe"]),
                       beat_spy=bool(pick.oSharpe > sp["oSharpe"]),
                       p4a=bool(pick.p4a), p4b=bool(pick.p4b), f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  {len(WF)} picks (3 panels x 9 theta x 2 arms x 2 constructions).  Dial choice:")
    P(fmt(WF.pivot_table(index=["arm", "construction"], columns="cadence", values="theta",
                         aggfunc="size").fillna(0).astype(int), 0))
    P(fmt(WF.pivot_table(index=["arm", "construction"], columns="gross", values="theta",
                         aggfunc="size").fillna(0).astype(int), 0))
    P("\n  OOS at the picks, by arm:")
    P(fmt(WF.groupby(["arm", "construction"]).agg(
        n=("oSharpe", "size"), oCAGR=("oCAGR", "mean"), oSharpe=("oSharpe", "mean"),
        oMaxDD=("oMaxDD", "mean"), beat_base=("beat_base", "mean"),
        beat_spy=("beat_spy", "mean"), p4a=("p4a", "sum"), p4b=("p4b", "sum"))))
    hh = WF.pivot_table(index=["panel", "theta", "construction"], columns="arm",
                        values=["oSharpe", "oCAGR", "oMaxDD"])
    dsh = hh[("oSharpe", "MOM-D")] - hh[("oSharpe", "MA-THRESH")]
    P(f"\n  HEAD-TO-HEAD AT THE PICKS (the honest rule-8 read): MOM-D beats MA-THRESH OOS in "
      f"{int((dsh > 0).sum())}/{len(dsh)} cells, mean dOOS Sharpe {dsh.mean():+.4f}, "
      f"median {dsh.median():+.4f}")
    P(f"  picks beating RULES v2 OOS: {int(WF.beat_base.sum())}/{len(WF)}   "
      f"beating SPY OOS: {int(WF.beat_spy.sum())}/{len(WF)}")
    P("\n  EVERY PICK:")
    P(fmt(WF[["panel", "theta", "arm", "construction", "cadence", "gross", "CAGR", "Sharpe",
              "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "base_oSharpe", "spy_oSharpe",
              "turn_yr", "p4a", "f4b"]]))
    flush_log()

    # -------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 185)
    P("D.  KEEP PATHS over all 1,296 books")
    P("=" * 185)
    P(f"  4a passes {int(G.p4a.sum())}/{len(G)}   4b passes {int(G.p4b.sum())}/{len(G)}   "
      f"BOTH {int((G.p4a & G.p4b).sum())}")
    P(fmt(G.groupby(["arm", "construction"]).agg(books=("p4a", "size"), p4a=("p4a", "sum"),
                                                 p4b=("p4b", "sum"))))
    fb = G[~G.p4b].f4b.str.split(",").explode().value_counts()
    P("  binding 4b bars: " + "  ".join(f"{k} {v}" for k, v in fb.items()))
    kp = G[G.p4a | G.p4b].copy()
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(f"\n  {len(kp)} books pass at least one path; by panel x arm:")
    if len(kp):
        P(fmt(kp.pivot_table(index=["panel", "arm"], columns="construction", values="p4b",
                             aggfunc="sum").fillna(0), 0))
        P("\n  every 4b passer, ranked by OOS Sharpe:")
        P(fmt(kp[kp.p4b].sort_values("oSharpe", ascending=False)[
            ["panel", "theta", "arm", "construction", "cadence", "gross", "CAGR", "Sharpe",
             "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "turn_yr", "p4a"]].head(40)))
        P("\n  ... and whether any 4b passer is also the rule-8 PICK of its own cell "
          "(the only kind that could be acted on):")
        P(f"  4b passers among the {len(WF)} rule-8 picks: {int(WF.p4b.sum())}")
    P("\n" + "=" * 185)
    P(f"GATES: G0 {g0:.3e}  G1 {g1:.3e}  G2 {g2:.3e}  G3 {g3:.3e}  G4 {g4:.3e}")
    P("=" * 185)
    flush_log()


if __name__ == "__main__":
    main()

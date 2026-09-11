#!/usr/bin/env python3
"""QUEUE idea 733 — is the EWALL-g1.00 vs RULES-v2 OOS-Sharpe TIE real, or a COST-RUNG artefact?

Idea 727 reported that its two best rule-8 picks LOSE to the live book's OOS Sharpe by
0.0007 (U56, 1.2827 vs 1.2834) and 0.0011 (B136, 1.1195 vs 1.1206) — gaps of 7e-4 and 1.1e-3
on a statistic whose own sampling noise is ~0.1.  A dead heat at one cost rung is one point,
not a finding.  This run prices the de-grossing equal-weight book against RULES v2 on a FINE
cost x gross ladder and asks whether the tie is a property of the two books or of the 10 bps
rung the record happens to quote.

TUNED PARAMETERS (2, both reported in full — every grid point is published):
    1. gross  g in {0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00, 1.10, 1.25}   (9 rungs; 0.75 live)
    2. cost   c in {0, 5, 10, 15, 20, 25, 35, 50} bps                        (8 rungs; 10 is PROTOCOL)

REPORTED AXES (inherited from the record, never tuned):
    panel in {U56 = load_universe(), B136 = load_universe(broad=True)}
    gate  in {EW_BAND = RULES v2's 200d +/-3% hysteresis band,
              EW_ELIG = RULES v1's un-ranked eligibility (above 200d AND vol20 < 0.60)}
    cadence W, execution t+1 (engine), 260-day warm-up skip, IS/OOS boundary 2016-12-31.

WHICH BOOK IS "EWALL"?  The record uses the label for both gates, so this run carries both and
lets GATE 0b decide which one idea 727 actually ran: whichever reading reproduces the published
OOS-Sharpe pair on BOTH panels is the one the claim is about.  Both are DE-GROSSING equal-weight
books in the record's sense: every priced name carries g/N_priced of NAV when its own gate is ON
and 0.0 when it is OFF, so gated-out weight goes to CASH and is never re-spread.  EW_BAND at
g=0.75 IS the live book (baseline.rules_v2_weights).  SPY is a BENCHMARK COLUMN ONLY on both
panels and is dropped from every weight frame (idea 737's noSPY convention; stated explicitly
because idea 740 is open on exactly this).

PROTOCOL 2 ("no leverage unless the idea says so"): the idea does not say so, so only g <= 1.00
is ADMISSIBLE.  g in {1.10, 1.25} is carried as a reported ladder extension and is excluded from
every KEEP tally and every rule-8 pick; the inadmissible tallies are printed beside them.

GATES
    0a. EW_BAND g0.75 reproduces baseline.rules_v2_weights exactly on each panel.
    0b. reproduce idea 727's published U56 / B136 OOS-Sharpe pair at 10 bps, both gates.
    1.  cost linearity: the engine's cost enters only as -turnover*c/1e4 on a cost-independent
        holdings path, so r(c) = r(0) - turnover*c/1e4 exactly.  Checked against direct engine
        runs before any of the ladder is derived that way.

RULE 8 (walk-forward, required).  Gross is chosen on the IS half (<= 2016-12-31) ONLY, at the
PROTOCOL 10 bps rung, by two selectors, and the pick is then evaluated on 2017-2026 untouched:
    S1 = max IS Sharpe (the record's usual selector);
    S2 = the 2026-09-03 memo's PRE-STATED rule, "smallest G whose MaxDD <= 60% of SPY's and
         CAGR >= 70% of SPY's", read on the IS window alone.
OOS CAGR/Sharpe/MaxDD are reported against RULES v2 (baseline, same cost rung) and SPY.

KEEP paths 4a and 4b are evaluated for every cell, on the full sample and on the OOS window,
against the RULES v2 comparand run on the IDEA'S OWN PANEL at the SAME cost rung.

Outputs: <stem>.grid.csv  <stem>.walkforward.csv  <stem>.gates.csv  <stem>.console.txt
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state, rules_v2_weights      # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

STEM = str(Path(__file__))[:-3]          # the slug contains '.', so with_suffix() is unusable
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

FREQ = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
GS = [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00, 1.10, 1.25]     # tuned param 1
COSTS = [0, 5, 10, 15, 20, 25, 35, 50]                          # tuned param 2
PROTO_COST = 10
GMAX_ADMISSIBLE = 1.00                                          # PROTOCOL 2: no leverage
WARMUP = 260
GATES = ("EW_BAND", "EW_ELIG")

# idea 727's published pair (EWALL g1.00, RULES v2 g0.75) OOS Sharpe at 10 bps — GATE 0b
PUB = {"U56": (1.2827, 1.2834), "B136": (1.1195, 1.1206)}
PUB_TOL = 5e-4


# ------------------------------------------------------------------ panels
def panels():
    px = load_universe().dropna(how="all").ffill()
    pxb = load_universe(broad=True)
    return {"U56": (px, [c for c in px.columns if c != "SPY"]),
            "B136": (pxb, [c for c in pxb.columns if c != "SPY"])}


# ------------------------------------------------------------------ books
def elig_mask(px, cols):
    """RULES v1 eligibility, un-ranked: above the 200d mean AND vol20 < 0.60."""
    sub = px[cols]
    above = sub > sub.rolling(200).mean()
    vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)
    return above & (vol20 < 0.60)


def degross_weights(px, cols, gate, g):
    """g/N_priced on every name whose gate is ON, 0 otherwise -> gated-out weight is CASH."""
    priced = px[cols].notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    w = (g * priced.astype(float)).div(n, axis=0).fillna(0.0)
    w = w.where(gate.reindex_like(w).fillna(False), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def book_fn(gate, cols, g):
    if gate == "EW_ELIG":
        return lambda px: degross_weights(px, cols, elig_mask(px, cols), g)
    if gate == "EW_BAND":
        return lambda px: degross_weights(px, cols, band_state(px[cols], 0.03), g)
    raise ValueError(gate)


# ------------------------------------------------------------------ scoring
def seg(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(x); return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def full_row(tag, r):
    h = len(r) // 2
    o = r.loc[OOS_START:]; ho = len(o) // 2
    i = r.loc[:IS_END];    hi = len(i) // 2
    d, do, di = seg(r), seg(r, OOS_START), seg(r, None, IS_END)
    return dict(tag=tag, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS_CAGR=do["CAGR"], OOS_Sharpe=do["Sharpe"], OOS_MaxDD=do["MaxDD"],
                OOS_H1=metrics(o.iloc[:ho])["Sharpe"], OOS_H2=metrics(o.iloc[ho:])["Sharpe"],
                IS_CAGR=di["CAGR"], IS_Sharpe=di["Sharpe"], IS_MaxDD=di["MaxDD"],
                IS_H1=metrics(i.iloc[:hi])["Sharpe"], IS_H2=metrics(i.iloc[hi:])["Sharpe"])


def keep_rec(row, spy, v2):
    """PROTOCOL 4a / 4b as the record computes them (full-sample halves + the OOS Sharpe leg)."""
    a = (row["H1"] > v2["H1"] and row["H2"] > v2["H2"] and row["MaxDD"] >= v2["MaxDD"])
    b = (row["H1"] > spy["H1"] and row["H2"] > spy["H2"]
         and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def keep_win(row, spy, v2, pre):
    S, C, D, H1, H2 = pre + "Sharpe", pre + "CAGR", pre + "MaxDD", pre + "H1", pre + "H2"
    a = (row[H1] > v2[H1] and row[H2] > v2[H2] and row[D] >= v2[D])
    b = (row[H1] > spy[H1] and row[H2] > spy[H2] and row[S] > spy[S]
         and row[D] >= 0.60 * spy[D] and row[C] >= 0.70 * spy[C])
    return bool(a), bool(b)


# ------------------------------------------------------------------ run
def main():
    gates, grid, wf = [], [], []
    for pname, (px, cols) in panels().items():
        st = px.index[WARMUP]
        P(f"\n=== panel {pname}: {len(cols)} tradables + SPY benchmark, "
          f"{px.index[0].date()}..{px.index[-1].date()} ({len(px)} rows), scored from {st.date()}")
        spy = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        P(f"    SPY   full Sharpe {spy['Sharpe']:.4f} CAGR {spy['CAGR']:.4%} MaxDD {spy['MaxDD']:.4%}"
          f" | IS Sharpe {spy['IS_Sharpe']:.4f} CAGR {spy['IS_CAGR']:.4%} MaxDD {spy['IS_MaxDD']:.4%}"
          f" | OOS Sharpe {spy['OOS_Sharpe']:.4f} CAGR {spy['OOS_CAGR']:.4%} MaxDD {spy['OOS_MaxDD']:.4%}")
        P(f"    4b bars: CAGR >= {0.70*spy['CAGR']:.4%} (full) / {0.70*spy['OOS_CAGR']:.4%} (OOS);"
          f"  MaxDD >= {0.60*spy['MaxDD']:.4%} (full) / {0.60*spy['OOS_MaxDD']:.4%} (OOS)")

        # cost-free engine runs, one per (gate, gross); every cost rung is derived from these
        base = {}
        for gt in GATES:
            for g in GS:
                res = backtest(px, book_fn(gt, cols, g)(px), cost_bps=0.0, freq=FREQ)
                base[(gt, g)] = (res["returns"].loc[st:], res["turnover"].loc[st:])

        # GATE 1 — cost linearity against direct engine runs
        for gt, g, c in (("EW_BAND", 0.75, 10), ("EW_BAND", 1.00, 50), ("EW_ELIG", 1.00, 10)):
            r0, to = base[(gt, g)]
            direct = backtest(px, book_fn(gt, cols, g)(px), cost_bps=c, freq=FREQ)["returns"].loc[st:]
            gap = float((direct - (r0 - to * c / 1e4)).abs().max())
            gates.append(dict(panel=pname, gate="G1_cost_linearity", cell=f"{gt} g{g:.2f} {c}bps",
                              value=gap, bar=1e-12, passed=gap < 1e-12))
            P(f"    GATE1 cost-linearity {gt} g{g:.2f} {c}bps  max|gap| {gap:.3e}  "
              f"{'PASS' if gap < 1e-12 else 'FAIL'}")

        # GATE 0a — EW_BAND g0.75 vs the live helper, and WHERE the two differ.
        # baseline.rules_v2_weights counts SPY in its N_priced denominator (g/(N+1) per name);
        # dropping the SPY column afterwards therefore leaves a book with slightly LESS gross
        # deployed than g/N per name.  This is exactly the open idea-740 convention.  Both
        # readings are measured so the gap has a named cause rather than a pass/fail verdict.
        r0, to = base[("EW_BAND", 0.75)]
        helper = backtest(px, rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
                          .reindex(columns=px.columns).fillna(0.0),
                          cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[st:]
        gap_noSPY = float((helper - (r0 - to * PROTO_COST / 1e4)).abs().max())
        # the same book with SPY INSIDE the denominator (the helper's own convention)
        priced_all = px.notna()
        n_all = priced_all.sum(axis=1).replace(0, np.nan)
        w = (0.75 * priced_all[cols].astype(float)).div(n_all, axis=0).fillna(0.0)
        w = w.where(band_state(px[cols], 0.03).reindex_like(w).fillna(False), 0.0)
        alt = backtest(px, w.reindex(columns=px.columns).fillna(0.0),
                       cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[st:]
        gap_withSPY = float((helper - alt).abs().max())
        for cell, v in (("N_excl_SPY (this run)", gap_noSPY), ("N_incl_SPY (helper's own)", gap_withSPY)):
            gates.append(dict(panel=pname, gate="G0a_SPY_denominator_convention", cell=cell,
                              value=v, bar=1e-12, passed=v < 1e-12))
        P(f"    GATE0a vs baseline.rules_v2_weights (SPY column dropped): "
          f"N excl SPY max|gap| {gap_noSPY:.3e} ({'match' if gap_noSPY < 1e-12 else 'DIFFERS'})"
          f"   N incl SPY max|gap| {gap_withSPY:.3e} "
          f"({'match' if gap_withSPY < 1e-12 else 'DIFFERS'})"
          f"  -> the helper's denominator is the idea-740 convention")

        # the ladder
        for c in COSTS:
            rows = {}
            for gt in GATES:
                for g in GS:
                    r0, to = base[(gt, g)]
                    rows[(gt, g)] = full_row(f"{gt}_g{g:.2f}", r0 - to * c / 1e4)
            v2 = rows[("EW_BAND", 0.75)]                     # the live book, same cost rung
            for (gt, g), row in rows.items():
                a_f, b_f = keep_rec(row, spy, v2)
                a_o, b_o = keep_win(row, spy, v2, "OOS_")
                _, to = base[(gt, g)]
                grid.append(dict(panel=pname, gate=gt, gross=g, cost_bps=c,
                                 admissible=g <= GMAX_ADMISSIBLE,
                                 turn_yr=float(to.sum() / (len(to) / 252)),
                                 **{k: v for k, v in row.items() if k != "tag"},
                                 d_OOS_Sharpe_vs_v2=row["OOS_Sharpe"] - v2["OOS_Sharpe"],
                                 d_full_Sharpe_vs_v2=row["Sharpe"] - v2["Sharpe"],
                                 d_OOS_Sharpe_vs_SPY=row["OOS_Sharpe"] - spy["OOS_Sharpe"],
                                 keep4a_full=a_f, keep4b_full=b_f, keep4a_oos=a_o, keep4b_oos=b_o,
                                 spy_Sharpe=spy["Sharpe"], spy_CAGR=spy["CAGR"], spy_MaxDD=spy["MaxDD"],
                                 spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                                 spy_OOS_MaxDD=spy["OOS_MaxDD"]))

            # GATE 0b — which gate reading reproduces idea 727's published pair?
            if c == PROTO_COST:
                pe, pv = PUB[pname]
                for gt in GATES:
                    e = rows[(gt, 1.00)]
                    d = e["OOS_Sharpe"] - pe
                    gates.append(dict(panel=pname, gate="G0b_idea727_g100_OOS_Sharpe", cell=gt,
                                      value=d, bar=PUB_TOL, passed=abs(d) < PUB_TOL))
                    P(f"    GATE0b {gt} g1.00 OOS Sharpe {e['OOS_Sharpe']:.4f} vs published "
                      f"{pe:.4f}  d {d:+.4f}  {'MATCH' if abs(d) < PUB_TOL else 'no'}")
                d = v2["OOS_Sharpe"] - pv
                gates.append(dict(panel=pname, gate="G0b_idea727_RULESv2_OOS_Sharpe", cell="EW_BAND g0.75",
                                  value=d, bar=PUB_TOL, passed=abs(d) < PUB_TOL))
                P(f"    GATE0b RULES v2 (EW_BAND g0.75) OOS Sharpe {v2['OOS_Sharpe']:.4f} vs published "
                  f"{pv:.4f}  d {d:+.4f}  {'MATCH' if abs(d) < PUB_TOL else 'no'}")

        # rule 8 — gross chosen on IS only, among ADMISSIBLE rungs, two selectors
        cand_all = [r for r in grid if r["panel"] == pname and r["cost_bps"] == PROTO_COST]
        v2o = next(r for r in cand_all if r["gate"] == "EW_BAND" and r["gross"] == 0.75)
        for gt in GATES:
            adm = [r for r in cand_all if r["gate"] == gt and r["admissible"]]
            allr = [r for r in cand_all if r["gate"] == gt]
            s2 = [r for r in adm if r["IS_MaxDD"] >= 0.60 * spy["IS_MaxDD"]
                  and r["IS_CAGR"] >= 0.70 * spy["IS_CAGR"]]
            picks = {"S1_maxISSharpe_admissible": max(adm, key=lambda r: r["IS_Sharpe"]),
                     "S2_memo_smallestG_clearing_IS_4b_bars": (min(s2, key=lambda r: r["gross"])
                                                               if s2 else None),
                     "S1_maxISSharpe_unrestricted": max(allr, key=lambda r: r["IS_Sharpe"])}
            for sel, pick in picks.items():
                if pick is None:
                    wf.append(dict(panel=pname, gate=gt, selector=sel, picked_gross=np.nan,
                                   note="no admissible gross clears the IS 4b bars"))
                    P(f"    RULE8 {gt} {sel}: EMPTY — no admissible gross clears the IS 4b bars")
                    continue
                wf.append(dict(panel=pname, gate=gt, selector=sel, picked_gross=pick["gross"],
                               admissible=pick["admissible"],
                               IS_Sharpe=pick["IS_Sharpe"], IS_CAGR=pick["IS_CAGR"],
                               IS_MaxDD=pick["IS_MaxDD"],
                               OOS_Sharpe=pick["OOS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                               OOS_MaxDD=pick["OOS_MaxDD"],
                               v2_OOS_Sharpe=v2o["OOS_Sharpe"], v2_OOS_CAGR=v2o["OOS_CAGR"],
                               v2_OOS_MaxDD=v2o["OOS_MaxDD"],
                               spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                               spy_OOS_MaxDD=spy["OOS_MaxDD"],
                               d_OOS_Sharpe_vs_v2=pick["d_OOS_Sharpe_vs_v2"],
                               keep4a_oos=pick["keep4a_oos"], keep4b_oos=pick["keep4b_oos"],
                               keep4a_full=pick["keep4a_full"], keep4b_full=pick["keep4b_full"],
                               note=""))

    G = pd.DataFrame(grid); W = pd.DataFrame(wf); GT = pd.DataFrame(gates)
    G.to_csv(STEM + ".grid.csv", index=False)
    W.to_csv(STEM + ".walkforward.csv", index=False)
    GT.to_csv(STEM + ".gates.csv", index=False)

    # ---------------------------------------------------------------- report
    P("\n=== EVERY GRID POINT — OOS Sharpe levels (rows = gross, cols = cost bps)")
    for pname in G.panel.unique():
        for gt in GATES:
            s = G[(G.panel == pname) & (G.gate == gt)]
            P(f"\n[{pname} {gt}] OOS Sharpe")
            P(s.pivot(index="gross", columns="cost_bps", values="OOS_Sharpe")
              .to_string(float_format=lambda x: f"{x:.4f}"))
            P(f"[{pname} {gt}] d(OOS Sharpe) vs RULES v2 (EW_BAND g0.75, same cost rung)")
            P(s.pivot(index="gross", columns="cost_bps", values="d_OOS_Sharpe_vs_v2")
              .to_string(float_format=lambda x: f"{x:+.4f}"))
            P(f"[{pname} {gt}] full-sample CAGR")
            P(s.pivot(index="gross", columns="cost_bps", values="CAGR")
              .to_string(float_format=lambda x: f"{x:.4%}"))
            P(f"[{pname} {gt}] full-sample MaxDD")
            P(s.pivot(index="gross", columns="cost_bps", values="MaxDD")
              .to_string(float_format=lambda x: f"{x:.4%}"))

    P("\n=== THE TIE — g1.00 vs RULES v2 g0.75 at every cost rung, both gate readings")
    for gt in GATES:
        t = G[(G.gate == gt) & (G.gross == 1.00)]
        P(f"\n[{gt} g1.00]")
        P(t[["panel", "cost_bps", "OOS_Sharpe", "d_OOS_Sharpe_vs_v2", "Sharpe",
             "d_full_Sharpe_vs_v2", "OOS_CAGR", "OOS_MaxDD", "turn_yr"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        for pname in G.panel.unique():
            x = t[t.panel == pname]
            sgn = "/".join("+" if v > 0 else ("-" if v < 0 else "0") for v in x.d_OOS_Sharpe_vs_v2)
            P(f"  [{pname}] sign over {len(x)} cost rungs: {sgn}   "
              f"range [{x.d_OOS_Sharpe_vs_v2.min():+.4f}, {x.d_OOS_Sharpe_vs_v2.max():+.4f}]   "
              f"|d| max {x.d_OOS_Sharpe_vs_v2.abs().max():.4f}   "
              f"turnover {x.turn_yr.iloc[0]:.2f}/yr vs v2 "
              f"{G[(G.panel==pname)&(G.gate=='EW_BAND')&(G.gross==0.75)].turn_yr.iloc[0]:.2f}/yr")

    P("\n=== GROSS-INVARIANCE OF SHARPE on the de-grossing book (cost rung 10 bps)")
    for pname in G.panel.unique():
        for gt in GATES:
            s = G[(G.panel == pname) & (G.gate == gt) & (G.cost_bps == PROTO_COST)
                  & G.admissible].sort_values("gross")
            P(f"  [{pname} {gt}] gross {s.gross.min():.2f}->{s.gross.max():.2f}: "
              f"full Sharpe {s.Sharpe.iloc[0]:.4f}->{s.Sharpe.iloc[-1]:.4f} "
              f"(spread {s.Sharpe.max()-s.Sharpe.min():.4f}), "
              f"OOS Sharpe {s.OOS_Sharpe.iloc[0]:.4f}->{s.OOS_Sharpe.iloc[-1]:.4f} "
              f"(spread {s.OOS_Sharpe.max()-s.OOS_Sharpe.min():.4f}), "
              f"CAGR {s.CAGR.iloc[0]:.2%}->{s.CAGR.iloc[-1]:.2%}, "
              f"MaxDD {s.MaxDD.iloc[0]:.2%}->{s.MaxDD.iloc[-1]:.2%}")

    P("\n=== RULE 8 WALK-FORWARD (gross chosen on IS <= 2016 only; OOS 2017-2026 untouched)")
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n=== KEEP PATHS")
    A = G[G.admissible]
    P(f"admissible cells (g <= {GMAX_ADMISSIBLE:.2f}): {len(A)} of {len(G)}")
    P(f"  4a full {int(A.keep4a_full.sum())}   4b full {int(A.keep4b_full.sum())}   "
      f"4a OOS {int(A.keep4a_oos.sum())}   4b OOS {int(A.keep4b_oos.sum())}")
    I = G[~G.admissible]
    P(f"  [inadmissible, PROTOCOL 2 leverage, reported only] 4a full {int(I.keep4a_full.sum())}   "
      f"4b full {int(I.keep4b_full.sum())}   4a OOS {int(I.keep4a_oos.sum())}   "
      f"4b OOS {int(I.keep4b_oos.sum())}")
    for pname in G.panel.unique():
        for gt in GATES:
            s = A[(A.panel == pname) & (A.gate == gt)]
            P(f"  [{pname} {gt}] 4a full {int(s.keep4a_full.sum())}/{len(s)}   "
              f"4b full {int(s.keep4b_full.sum())}/{len(s)}   "
              f"4a OOS {int(s.keep4a_oos.sum())}/{len(s)}   4b OOS {int(s.keep4b_oos.sum())}/{len(s)}")
    k = A[A.keep4b_full]
    P(f"\n  admissible 4b-full passers ({len(k)}):")
    if len(k):
        P(k[["panel", "gate", "gross", "cost_bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "spy_CAGR", "spy_MaxDD", "turn_yr"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    kp = k[k.cost_bps == PROTO_COST]
    P(f"\n  admissible 4b-full passers AT THE PROTOCOL 10 bps RUNG ({len(kp)}):")
    if len(kp):
        P(kp[["panel", "gate", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "turn_yr"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P("  highest cost rung at which each of those cells still clears 4b-full:")
        for _, r in kp.iterrows():
            same = k[(k.panel == r.panel) & (k.gate == r.gate) & (k.gross == r.gross)]
            P(f"    {r.panel} {r.gate} g{r.gross:.2f}: {int(same.cost_bps.max())} bps")

    Path(STEM + ".console.txt").write_text("\n".join(LOG) + "\n")
    return G, W, GT


if __name__ == "__main__":
    main()

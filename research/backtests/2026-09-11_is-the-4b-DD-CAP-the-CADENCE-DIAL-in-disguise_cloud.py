#!/usr/bin/env python3
"""QUEUE idea 541 — is the 4b DD CAP the CADENCE DIAL in disguise?

Idea 299 reported that idea 298's PARK candidate clears the 0.60x-SPY drawdown cap by 0.40 pp
at MONTHLY cadence and misses it by 0.70 pp at WEEKLY, i.e. 1.13 pp of MaxDD on one book comes
from the rebalance schedule alone.  If that generalises, the 4b drawdown leg is partly a
bookkeeping artefact of a dial nobody pre-registers.  This run sweeps cadence D/W/M/Q against
the cap across the books that carry the record's committed 4b passes and asks, cell by cell,
whether each 4b verdict is CADENCE-DECIDED or SIGNAL-DECIDED.

WHICH BOOKS ARE "THE RECORD'S COMMITTED 4b PASSERS"?  Idea 733 (2026-09-11, this lane)
established that the record's 4b passes are the de-grossing band book at high gross — the live
RULES v2 clause with gross as the only dial that moves the binding bar.  So the sweep runs that
family.  Idea 298's own QUANTILE-family book is NOT rebuilt here: idea 299 re-affirmed it as
PARK with 0 of 27 books clearing 4b at weekly cadence, so its cadence sensitivity cannot be
read off a 4b pass it does not have.  That anchor is therefore quoted, not reproduced, and this
run answers the general question on the books that do pass.

TUNED PARAMETERS (2, both reported in full — every grid point is published):
    1. cadence in {D, W, M, Q}                                   (4 rungs; W is live)
    2. gross   g in {0.50, 0.75, 0.90, 1.00}                      (4 rungs; 0.75 is live)
Deviation from the QUEUE entry's suggested "(cadence, panel)": panel is carried as a REPORTED
AXIS over all three panels instead of a tuned one, and gross takes the second tuned slot,
because idea 733 showed gross is the only dial that moves 4b's binding bar — a cadence sweep at
a single gross would have nothing to flip.

REPORTED AXES (never tuned): panel in {U56, B136, SMALL439}; book in {BAND, ALLIN};
cost in {10, 25, 50} bps (10 is PROTOCOL); execution t+1; 260-day warm-up skip;
IS/OOS boundary 2016-12-31.

BOOKS.  BAND = the live signal: every priced name carries g/N_priced of NAV while it is inside
its own 200d +/-3% hysteresis band and 0.0 outside it, so gated-out weight becomes CASH and is
never re-spread (de-grossing).  ALLIN = the SIGNAL-FREE control: the same envelope with the gate
always ON, i.e. g/N_priced on every priced name, every day.  The pair is what makes "signal-
decided" measurable: ALLIN carries the cadence and the gross but none of the timing.

PRE-STATED DEFINITIONS (fixed before the grid was cut):
    CADENCE-DECIDED      a (panel, book, gross, cost) cell whose 4b verdict is NOT constant
                         across the four cadences.
    DD-CADENCE-DECIDED   ... and whose DD-cap leg alone is not constant across the four.
    SIGNAL-DECIDED       a (panel, cadence, gross, cost) cell whose 4b verdict differs between
                         BAND and ALLIN.
    DD_SPREAD            max MaxDD - min MaxDD over the four cadences, in pp — the quantity
                         idea 299 measured as 1.13 pp on one book.

SMALL439: data/prices_small.csv is 483 sub-$2B names since 2010; the 44 tickers with
max_1d_move >= 1.0 in data/small_meta.csv are dropped FIRST, leaving 439.  SURVIVORSHIP: the
panel is current constituents of the screen only (data/SMALL_PANEL_README.md), so every
small-cap number here is biased upward and is reported, never promoted.

GATES
    1. cost linearity: r(c) = r(0) - turnover*c/1e4 exactly, checked against direct engine runs.
    2. the live book reproduces: BAND g0.75 at weekly cadence on U56 must restate idea 733's
       committed row (CAGR 8.63%, Sharpe 1.2069, MaxDD -11.90%, OOS Sharpe 1.2834) at 10 bps.
    3. ALLIN is really signal-free: its realised gross must equal g on every day every name is
       priced, and its turnover must be strictly below BAND's at the same cadence.

RULE 8 (walk-forward, required): (cadence, gross) chosen on the IS window <= 2016-12-31 ONLY,
at 10 bps, by max IS Sharpe and by the 2026-09-03 memo's pre-stated 4b-bar rule; evaluated on
2017-2026 untouched, OOS CAGR/Sharpe/MaxDD against RULES v2 (the live book, weekly, same panel
and cost rung) and SPY.

Outputs: <stem>.grid.csv <stem>.cadence.csv <stem>.walkforward.csv <stem>.gates.csv <stem>.console.txt
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state                        # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

STEM = str(Path(__file__))[:-3]
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

CADENCES = ["D", "W", "M", "Q"]                         # tuned param 1
GS = [0.50, 0.75, 0.90, 1.00]                           # tuned param 2
COSTS = [10, 25, 50]                                    # reported axis
PROTO_COST = 10
LIVE_CADENCE, LIVE_GROSS = "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
BOOKS = ("BAND", "ALLIN")

# idea 733's committed live-book row on U56 at 10 bps, weekly — GATE 2
ANCHOR = dict(CAGR=0.086347, Sharpe=1.206912, MaxDD=-0.118966, OOS_Sharpe=1.283437)
ANCHOR_TOL = 5e-6
IDEA299_DD_SPREAD_PP = 1.13                             # the claim under test, one book


# ------------------------------------------------------------------ panels
def panels():
    out = {}
    px = load_universe().dropna(how="all").ffill()
    out["U56"] = (px, [c for c in px.columns if c != "SPY"])
    pxb = load_universe(broad=True)
    out["B136"] = (pxb, [c for c in pxb.columns if c != "SPY"])
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"    SMALL: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len(bad)} with max_1d_move >= 1.0 -> {len(cols)} kept")
    out[f"SMALL{len(cols)}"] = (pxs[cols + ["SPY"]].dropna(how="all").ffill(), cols)
    return out


# ------------------------------------------------------------------ books
def weights(px, cols, book, g):
    priced = px[cols].notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    w = (g * priced.astype(float)).div(n, axis=0).fillna(0.0)
    if book == "BAND":
        w = w.where(band_state(px[cols], 0.03).reindex_like(w).fillna(False), 0.0)
    elif book != "ALLIN":
        raise ValueError(book)
    return w.reindex(columns=px.columns).fillna(0.0)


# ------------------------------------------------------------------ scoring
def seg(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(x); return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def full_row(r):
    h = len(r) // 2
    o = r.loc[OOS_START:]; ho = len(o) // 2
    i = r.loc[:IS_END];    hi = len(i) // 2
    d, do, di = seg(r), seg(r, OOS_START), seg(r, None, IS_END)
    return dict(CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS_CAGR=do["CAGR"], OOS_Sharpe=do["Sharpe"], OOS_MaxDD=do["MaxDD"],
                OOS_H1=metrics(o.iloc[:ho])["Sharpe"], OOS_H2=metrics(o.iloc[ho:])["Sharpe"],
                IS_CAGR=di["CAGR"], IS_Sharpe=di["Sharpe"], IS_MaxDD=di["MaxDD"])


def legs4b(row, spy):
    """The three 4b legs, separately, so the DD cap can be read on its own."""
    return dict(leg_halves=bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"]),
                leg_oos=bool(row["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                leg_dd=bool(row["MaxDD"] >= 0.60 * spy["MaxDD"]),
                leg_cagr=bool(row["CAGR"] >= 0.70 * spy["CAGR"]))


# ------------------------------------------------------------------ run
def main():
    grid, gates, wf = [], [], []
    P("=== panels")
    PS = panels()

    for pname, (px, cols) in PS.items():
        st = px.index[WARMUP]
        P(f"\n=== panel {pname}: {len(cols)} tradables + SPY benchmark, "
          f"{px.index[0].date()}..{px.index[-1].date()} ({len(px)} rows), scored from {st.date()}")
        spy = full_row(px["SPY"].pct_change().fillna(0).loc[st:])
        P(f"    SPY  full Sharpe {spy['Sharpe']:.4f} CAGR {spy['CAGR']:.4%} MaxDD {spy['MaxDD']:.4%}"
          f" | OOS Sharpe {spy['OOS_Sharpe']:.4f} CAGR {spy['OOS_CAGR']:.4%} MaxDD {spy['OOS_MaxDD']:.4%}")
        P(f"    4b bars: DD cap {0.60*spy['MaxDD']:.4%}, CAGR floor {0.70*spy['CAGR']:.4%}")

        for book in BOOKS:
            for g in GS:
                w = weights(px, cols, book, g)
                if book == "ALLIN" and g == LIVE_GROSS:          # GATE 3: signal-free envelope
                    dep = w[cols].sum(axis=1).loc[st:]
                    gates.append(dict(panel=pname, gate="G3_ALLIN_gross_is_flat", cell=f"g{g:.2f}",
                                      value=float((dep - g).abs().max()), bar=1e-12,
                                      passed=float((dep - g).abs().max()) < 1e-12))
                for cad in CADENCES:
                    res = backtest(px, w, cost_bps=0.0, freq=cad)
                    r0, to = res["returns"].loc[st:], res["turnover"].loc[st:]
                    for c in COSTS:
                        row = full_row(r0 - to * c / 1e4)
                        lg = legs4b(row, spy)
                        grid.append(dict(panel=pname, book=book, cadence=cad, gross=g, cost_bps=c,
                                         turn_yr=float(to.sum() / (len(to) / 252)), **row, **lg,
                                         keep4b=all(lg.values()),
                                         spy_Sharpe=spy["Sharpe"], spy_CAGR=spy["CAGR"],
                                         spy_MaxDD=spy["MaxDD"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                                         spy_OOS_CAGR=spy["OOS_CAGR"],
                                         dd_cap=0.60 * spy["MaxDD"],
                                         dd_margin_pp=100 * (row["MaxDD"] - 0.60 * spy["MaxDD"])))
                    # GATE 1: cost linearity on one probe per (book, gross) at weekly
                    if cad == LIVE_CADENCE and g == LIVE_GROSS:
                        direct = backtest(px, w, cost_bps=PROTO_COST, freq=cad)["returns"].loc[st:]
                        gap = float((direct - (r0 - to * PROTO_COST / 1e4)).abs().max())
                        gates.append(dict(panel=pname, gate="G1_cost_linearity",
                                          cell=f"{book} g{g:.2f} W {PROTO_COST}bps",
                                          value=gap, bar=1e-12, passed=gap < 1e-12))

    G = pd.DataFrame(grid)

    # GATE 2 — the live book restates idea 733's committed row
    a = G[(G.panel == "U56") & (G.book == "BAND") & (G.cadence == LIVE_CADENCE)
          & (G.gross == LIVE_GROSS) & (G.cost_bps == PROTO_COST)].iloc[0]
    for k, v in ANCHOR.items():
        d = float(a[k]) - v
        gates.append(dict(panel="U56", gate="G2_idea733_live_row", cell=k, value=d,
                          bar=ANCHOR_TOL, passed=abs(d) < ANCHOR_TOL))
    GT = pd.DataFrame(gates)
    P("\n=== GATES")
    for _, r in GT.iterrows():
        P(f"    {r.gate:32s} {r.panel:10s} {str(r.cell):22s} value {r.value:+.3e}  "
          f"{'PASS' if r.passed else 'FAIL'}")
    # GATE 3b: ALLIN turnover must be below BAND's at the same cadence/gross
    t = G.groupby(["panel", "book", "cadence", "gross"]).turn_yr.first().unstack("book")
    bad = int((t.ALLIN >= t.BAND).sum())
    P(f"    G3b ALLIN turnover < BAND turnover: violations {bad} of {len(t)}  "
      f"{'PASS' if bad == 0 else 'FAIL'}")
    gates.append(dict(panel="all", gate="G3b_ALLIN_turnover_below_BAND", cell="count",
                      value=bad, bar=0, passed=bad == 0))
    GT = pd.DataFrame(gates)

    # ---------------------------------------------------------------- cadence effect on MaxDD
    P("\n=== DD_SPREAD: max-min MaxDD over the four cadences, in pp (the idea-299 statistic)")
    recs = []
    for (pn, bk, g, c), s in G.groupby(["panel", "book", "gross", "cost_bps"]):
        s = s.set_index("cadence")
        dd = s.MaxDD * 100
        recs.append(dict(panel=pn, book=bk, gross=g, cost_bps=c,
                         dd_D=dd.get("D"), dd_W=dd.get("W"), dd_M=dd.get("M"), dd_Q=dd.get("Q"),
                         dd_spread_pp=float(dd.max() - dd.min()),
                         dd_cap_pp=float(s.dd_cap.iloc[0] * 100),
                         best_cadence=str(dd.idxmax()), worst_cadence=str(dd.idxmin()),
                         keep4b_D=bool(s.keep4b.get("D")), keep4b_W=bool(s.keep4b.get("W")),
                         keep4b_M=bool(s.keep4b.get("M")), keep4b_Q=bool(s.keep4b.get("Q")),
                         leg_dd_D=bool(s.leg_dd.get("D")), leg_dd_W=bool(s.leg_dd.get("W")),
                         leg_dd_M=bool(s.leg_dd.get("M")), leg_dd_Q=bool(s.leg_dd.get("Q")),
                         n_pass=int(s.keep4b.sum()), n_dd_pass=int(s.leg_dd.sum())))
    C = pd.DataFrame(recs)
    C["cadence_decided"] = ~C.n_pass.isin([0, 4])
    C["dd_cadence_decided"] = ~C.n_dd_pass.isin([0, 4])
    C.to_csv(STEM + ".cadence.csv", index=False)
    G.to_csv(STEM + ".grid.csv", index=False)

    P(C[["panel", "book", "gross", "cost_bps", "dd_D", "dd_W", "dd_M", "dd_Q",
         "dd_spread_pp", "dd_cap_pp", "n_pass", "n_dd_pass"]]
      .to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    P(f"\n  DD_SPREAD over all {len(C)} (panel, book, gross, cost) cells: "
      f"median {C.dd_spread_pp.median():.2f} pp, mean {C.dd_spread_pp.mean():.2f} pp, "
      f"min {C.dd_spread_pp.min():.2f}, max {C.dd_spread_pp.max():.2f} pp")
    P(f"  idea 299's one-book claim was {IDEA299_DD_SPREAD_PP:.2f} pp; "
      f"{int((C.dd_spread_pp >= IDEA299_DD_SPREAD_PP).sum())} of {len(C)} cells "
      f"({100*(C.dd_spread_pp >= IDEA299_DD_SPREAD_PP).mean():.1f}%) reach it")
    P("  by panel / book:")
    P(C.groupby(["panel", "book"]).dd_spread_pp.agg(["median", "min", "max"])
      .to_string(float_format=lambda x: f"{x:.2f}"))
    P("  which cadence gives the SHALLOWEST drawdown (count of cells):")
    P(C.best_cadence.value_counts().to_string())

    # ---------------------------------------------------------------- the verdict census
    P("\n=== CADENCE-DECIDED vs SIGNAL-DECIDED")
    P(f"  4b passes over all {len(G)} cells: {int(G.keep4b.sum())}")
    P(f"  (panel, book, gross, cost) cells with ANY 4b pass: "
      f"{int((C.n_pass > 0).sum())} of {len(C)};  all four cadences pass: {int((C.n_pass == 4).sum())}")
    P(f"  **CADENCE-DECIDED (verdict not constant across D/W/M/Q): "
      f"{int(C.cadence_decided.sum())} of {int((C.n_pass > 0).sum())} cells with any pass**")
    P(f"  **DD-CADENCE-DECIDED (the DD leg alone flips across cadence): "
      f"{int(C.dd_cadence_decided.sum())} of {len(C)} cells**")
    if C.cadence_decided.any():
        P(C[C.cadence_decided][["panel", "book", "gross", "cost_bps", "keep4b_D", "keep4b_W",
                                "keep4b_M", "keep4b_Q", "leg_dd_D", "leg_dd_W", "leg_dd_M",
                                "leg_dd_Q", "dd_spread_pp"]]
          .to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    # which leg does the failing actually sit on?
    P("\n  among the 4b FAILURES, which legs fail (a cell can fail several):")
    F = G[~G.keep4b]
    P(f"    halves {int((~F.leg_halves).sum())}   OOS Sharpe {int((~F.leg_oos).sum())}   "
      f"DD cap {int((~F.leg_dd).sum())}   CAGR floor {int((~F.leg_cagr).sum())}   of {len(F)} failures")
    P("    SOLE failing leg (the bar that actually binds):")
    for leg in ("leg_halves", "leg_oos", "leg_dd", "leg_cagr"):
        others = [x for x in ("leg_halves", "leg_oos", "leg_dd", "leg_cagr") if x != leg]
        sole = F[~F[leg] & F[others].all(axis=1)]
        P(f"      {leg:11s} {len(sole):4d}")

    P("\n  SIGNAL-DECIDED (BAND vs ALLIN at the same cadence/gross/cost/panel):")
    piv = G.pivot_table(index=["panel", "cadence", "gross", "cost_bps"], columns="book",
                        values="keep4b", aggfunc="first")
    sd = piv[piv.BAND != piv.ALLIN]
    P(f"    {len(sd)} of {len(piv)} (panel, cadence, gross, cost) cells flip on the SIGNAL; "
      f"BAND passes where ALLIN fails in {int((piv.BAND & ~piv.ALLIN).sum())}, "
      f"the reverse in {int((~piv.BAND & piv.ALLIN).sum())}")
    P("    MaxDD gap BAND - ALLIN (pp), by panel and cadence (positive = the gate is shallower):")
    gg = G.pivot_table(index=["panel", "cadence"], columns="book", values="MaxDD", aggfunc="mean")
    gg["gate_pp"] = 100 * (gg.BAND - gg.ALLIN)
    P(gg.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n=== THE DIRECT COMPARISON the idea asks for: cadence effect vs signal effect, in pp of MaxDD")
    for pn in G.panel.unique():
        cad_eff = C[(C.panel == pn) & (C.book == "BAND")].dd_spread_pp.median()
        s = G[(G.panel == pn) & (G.cadence == LIVE_CADENCE)]
        sig_eff = 100 * (s[s.book == "BAND"].MaxDD.mean() - s[s.book == "ALLIN"].MaxDD.mean())
        P(f"  [{pn}] median cadence spread on the signal book **{cad_eff:.2f} pp**   vs   "
          f"signal effect at the live weekly cadence **{sig_eff:+.2f} pp**   "
          f"ratio {abs(sig_eff)/cad_eff if cad_eff else float('nan'):.1f}x")

    # ---------------------------------------------------------------- rule 8
    P("\n=== RULE 8 WALK-FORWARD ((cadence, gross) chosen on IS <= 2016 only; OOS untouched)")
    for pn in G.panel.unique():
        spy_row = dict(OOS_Sharpe=G[G.panel == pn].spy_OOS_Sharpe.iloc[0],
                       OOS_CAGR=G[G.panel == pn].spy_OOS_CAGR.iloc[0],
                       MaxDD=G[G.panel == pn].spy_MaxDD.iloc[0],
                       CAGR=G[G.panel == pn].spy_CAGR.iloc[0])
        live = G[(G.panel == pn) & (G.book == "BAND") & (G.cadence == LIVE_CADENCE)
                 & (G.gross == LIVE_GROSS) & (G.cost_bps == PROTO_COST)].iloc[0]
        for book in BOOKS:
            cand = G[(G.panel == pn) & (G.book == book) & (G.cost_bps == PROTO_COST)]
            s1 = cand.loc[cand.IS_Sharpe.idxmax()]
            ok = cand[(cand.IS_MaxDD >= 0.60 * live.spy_MaxDD)
                      & (cand.IS_CAGR >= 0.70 * live.spy_CAGR)]
            s2 = ok.sort_values(["gross", "cadence"]).iloc[0] if len(ok) else None
            for sel, pick in (("S1_maxISSharpe", s1), ("S2_memo_bars", s2)):
                if pick is None:
                    wf.append(dict(panel=pn, book=book, selector=sel,
                                   note="no (cadence, gross) clears the IS 4b bars"))
                    P(f"  [{pn} {book}] {sel}: EMPTY — no (cadence, gross) clears the IS 4b bars")
                    continue
                wf.append(dict(panel=pn, book=book, selector=sel, cadence=pick.cadence,
                               gross=pick.gross, IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR,
                               IS_MaxDD=pick.IS_MaxDD, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_CAGR=pick.OOS_CAGR, OOS_MaxDD=pick.OOS_MaxDD,
                               keep4b_full=bool(pick.keep4b),
                               live_OOS_Sharpe=live.OOS_Sharpe, live_OOS_CAGR=live.OOS_CAGR,
                               live_OOS_MaxDD=live.OOS_MaxDD,
                               spy_OOS_Sharpe=spy_row["OOS_Sharpe"],
                               spy_OOS_CAGR=spy_row["OOS_CAGR"], note=""))
                P(f"  [{pn} {book}] {sel}: pick cadence={pick.cadence} g={pick.gross:.2f} "
                  f"(IS Sharpe {pick.IS_Sharpe:.4f}) -> OOS Sharpe {pick.OOS_Sharpe:.4f} "
                  f"CAGR {pick.OOS_CAGR:.4%} MaxDD {pick.OOS_MaxDD:.4%} | live OOS "
                  f"{live.OOS_Sharpe:.4f}/{live.OOS_CAGR:.4%}/{live.OOS_MaxDD:.4%} | SPY OOS "
                  f"{spy_row['OOS_Sharpe']:.4f}/{spy_row['OOS_CAGR']:.4%} | 4b full "
                  f"{'PASS' if pick.keep4b else 'FAIL'}")
    W = pd.DataFrame(wf)
    W.to_csv(STEM + ".walkforward.csv", index=False)
    GT.to_csv(STEM + ".gates.csv", index=False)

    P("\n=== 4b PASSERS (all cells)")
    k = G[G.keep4b]
    if len(k):
        P(k[["panel", "book", "cadence", "gross", "cost_bps", "CAGR", "Sharpe", "MaxDD",
             "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "dd_margin_pp", "turn_yr"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("  none")

    Path(STEM + ".console.txt").write_text("\n".join(LOG) + "\n")
    return G, C, W, GT


if __name__ == "__main__":
    main()

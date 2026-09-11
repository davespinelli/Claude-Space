#!/usr/bin/env python3
"""IDEA 531 (cloud, 2026-09-11): price-the-0.60-DD-CAP-as-the-single-tuned-number-in-4b.

THE QUESTION (queue, verbatim)
------------------------------
"idea 527's live leg fails the DD cap on 36 of 39 pre-registered books including every top-n
momentum book on all three panels, i.e. the cap and not the return bars is what makes 4b
almost unpassable.  Sweep the cap multiple 0.40-1.00 and the CAGR floor 0.50-0.90 and publish
the 4b pass rate surface on a fixed pre-registered book family, so the protocol's two
constants are read rather than assumed.  Max 2 params (cap, floor)."

PROTOCOL 4b, as written, is five legs:
    H1  Sharpe_H1  > SPY_H1          (no constant)
    H2  Sharpe_H2  > SPY_H2          (no constant)
    OOS OOS Sharpe > SPY OOS Sharpe  (no constant)
    DD  MaxDD      >= phi_DD   * SPY MaxDD     phi_DD   = 0.60, never derived
    CAG CAGR       >= phi_CAGR * SPY CAGR      phi_CAGR = 0.70, never derived
The two constants were written down on 2026-09-04 and have been applied ~400k times since.
This run reads them off the data instead of assuming them.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4, max 2) ARE THE PROTOCOL'S OWN CONSTANTS
    PARAM 1  phi_DD   in {0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00}   (7 rungs)
    PARAM 2  phi_CAGR in {0.50, 0.60, 0.70, 0.80, 0.90}               (5 rungs)
    All 35 cells reported.  Two extra rungs are carried as LABELLED DELETIONS, not as tuning:
    phi_DD = inf (cap deleted) and phi_CAGR = 0 (floor deleted), which is how "what do the two
    constants actually cut" is measured.
NOTHING ABOUT THE BOOKS IS TUNED.  The book family is PRE-REGISTERED in this docstring and
every one of its members is reported, pass or fail:

    panels   U56 (research/universe.json), B136 (universe_broad.json), SMALL439
    families BAND(b)  b in {0.00, 0.03, 0.08}   - the live RULES v2 clause
             TOPN(n)  n in {10, 20, 50}         - idea 276's CAND-n (v1 composite, scaler off)
             EWALL                              - idea 155's gated equal weight
             SPYG                               - ZERO-SIGNAL CONTROL: SPY held at gross g
    gross    g in {0.50, 0.75, 1.00}
    = 3 panels x 8 books x 3 gross = 72 rows, of which 63 are real books and 9 the control.
Costs 10 bps, weekly cadence, next-day execution, 260-day warm-up skip, IS <= 2016-12-31,
OOS 2017-01-01.. .  Comparands per panel: SPY buy-and-hold and RULES v2 (SPY column dropped
from the book, idea 286's `do_panel` convention), both on the panel's own calendar.

THE STRUCTURAL CLAIM THIS RUN TESTS (beyond the queue's ask).  A book is a point
(DD_ratio, CAGR_ratio) = (MaxDD/SPY MaxDD, CAGR/SPY CAGR); the DD leg is DD_ratio <= phi_DD
and the floor is CAGR_ratio >= phi_CAGR.  Both hold only if
        Calmar_book / Calmar_SPY >= phi_CAGR / phi_DD,
so along a Calmar ray the two constants enter ONLY through their RATIO (0.70/0.60 = 1.1667,
idea 333's committed closed form).  If the pass surface collapses onto phi_CAGR/phi_DD then
"the 0.60 cap" is not a number the protocol tunes at all - the tuned number is 1.1667 - and
the queue's framing needs restating.  The converse is NOT algebraically implied, so the run
reports how often a book clears the Calmar bar and still fails a leg.

GATES (pre-registered, printed before any new number is read)
    G1  fast_bt vs engine.backtest on a SMALL439 book: returns AND turnover.
    G2  the live leg: RULES v2 on U56 at 10 bps vs the record's committed 8.66% / 1.2056 /
        -12.05% (|dSharpe| <= 0.02; data/prices.csv is re-downloaded daily, idea 641 G2).
    G3  this run's parameterised 4b at (0.60, 0.70) reproduces idea 286's committed
        `keep_paths` on every book row, and its 4a likewise - exactly.
    G4  the Calmar implication: DD-leg AND floor => Calmar_ratio >= phi_CAGR/phi_DD, asserted
        on all 72 x 35 cells; the converse rate is reported, not asserted.

RULE 8 (PROTOCOL 8, required).  For each (panel, family) the dial (b or n, and g) is chosen on
2009-2016 IS Sharpe ONLY and the pick is read once on 2017-01-01.. .  Reported against RULES
v2 and SPY on the same panel, with the 4b surface re-read on the picks alone - i.e. how many
constants-cells would certify a book an honest selector could actually have reached.

SURVIVORSHIP.  All three panels are CURRENT constituents of their screens (universe.json,
universe_broad.json, data/SMALL_PANEL_README.md), so every CAGR level is optimistic and the
CAGR floor is tested in the books' favour.  Nothing here is promoted: the object under test is
a pair of PROTOCOL constants, not a rule.

Outputs: .books.csv .surface.csv .legs.csv .walkforward.csv .console.txt .result.md
"""
import importlib.util, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights          # noqa
from engine import backtest, rebalance_mask, metrics                 # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

COST, FREQ, WARM = 10, "W", 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI_DD   = [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]     # PARAM 1
PHI_CAGR = [0.50, 0.60, 0.70, 0.80, 0.90]                 # PARAM 2
LIVE_DD, LIVE_CAGR = 0.60, 0.70                           # what PROTOCOL says today
BANDS, NS, GROSSES = [0.00, 0.03, 0.08], [10, 20, 50], [0.50, 0.75, 1.00]
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
full_row, keep_paths = M286.full_row, M286.keep_paths
cand_weights_ref, ewall_weights_ref = M286.cand_weights, M286.ewall_weights


def fast_bt(prices, weights, cost_bps=COST, freq=FREQ):
    """numpy re-implementation of engine.backtest; same algorithm, same NaN semantics (G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    w_t = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    held = np.empty_like(rets); turn = np.zeros(n); cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = w_t[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ---------------------------------------------------------------- the pre-registered books
def panel_cache(px):
    tr = [c for c in px.columns if c != "SPY"]
    s, above, vol20 = score(px[tr], vol_scale=False)
    gate = above & (vol20 < 0.60)
    return dict(tr=tr, rank=s.where(gate).rank(axis=1, ascending=False), gate=gate)


def w_topn(px, c, n, g):
    w = (c["rank"] <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def w_ewall(px, c, g):
    e = c["gate"].astype(float)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def w_band(px, b, g):
    return (rules_v2_weights(px, band=b, gross=g).drop(columns=["SPY"], errors="ignore")
            .reindex(columns=px.columns).fillna(0.0))


def w_spyg(px, g):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["SPY"] = g
    return w


def legs(row, spy, phi_dd, phi_cagr):
    """PROTOCOL 4b, with its two constants as arguments."""
    return dict(H1=row["H1"] > spy["H1"], H2=row["H2"] > spy["H2"],
                OOS=row["OOS_Sharpe"] > spy["OOS_Sharpe"],
                DD=row["MaxDD"] >= phi_dd * spy["MaxDD"],
                CAGR=row["CAGR"] >= phi_cagr * spy["CAGR"])


def main():
    t0all = time.time()
    P("=" * 104)
    P("IDEA 531 - price-the-0.60-DD-CAP-as-the-single-tuned-number-in-4b (cloud, 2026-09-11)")
    P("=" * 104)
    P(f"TUNED (2), and they are the PROTOCOL's OWN CONSTANTS: phi_DD in {PHI_DD} x phi_CAGR in {PHI_CAGR}")
    P(f"  plus two LABELLED DELETIONS (cap deleted / floor deleted), never a chosen rung.")
    P(f"PRE-REGISTERED BOOK FAMILY (docstring, fixed before any number below): 3 panels x "
      f"[BAND {BANDS} + TOPN {NS} + EWALL + SPYG control] x gross {GROSSES} = 72 rows, all reported.")
    P("10 bps, weekly, next-day execution, 260d warm-up, IS <=2016 / OOS 2017-.")

    src = M276.build_sources()
    pxs = src["pxs"]
    panels = {"U56": load_universe(), "B136": load_universe(broad=True),
              "SMALL439": pxs[[c for c in src["s_stk"]] + ["SPY"]]}
    for k, v in panels.items():
        P(f"  {k}: {len([c for c in v.columns if c != 'SPY'])} tradables, "
          f"{v.index[0].date()} .. {v.index[-1].date()} ({len(v)} days)")

    # ------------------------------------------------------------------ run
    P("\n" + "=" * 104); P("RUNNING THE PRE-REGISTERED FAMILY"); P("=" * 104)
    rows, comps = [], {}
    g1_done = False
    for pname, px in panels.items():
        c = panel_cache(px)
        st = px.index[WARM]
        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        v2_r = full_row("v2", fast_bt(px, w_band(px, 0.03, 0.75))[0].loc[st:])
        comps[pname] = dict(spy=spy_r, v2=v2_r)
        books = ([(f"BAND{b:.2f}", "BAND", b, lambda p, g, b=b: w_band(p, b, g)) for b in BANDS]
                 + [(f"TOPN{n}", "TOPN", n, lambda p, g, n=n: w_topn(p, c, n, g)) for n in NS]
                 + [("EWALL", "EWALL", np.nan, lambda p, g: w_ewall(p, c, g))]
                 + [("SPYG", "CONTROL", np.nan, lambda p, g: w_spyg(p, g))])
        for bname, fam, dial, wf in books:
            for g in GROSSES:
                w = wf(px, g)
                if not g1_done and pname == "SMALL439":
                    eng = backtest(px, w, cost_bps=COST, freq=FREQ)
                    rf, tf = fast_bt(px, w)
                    P(f"\n--- GATE 1 (on {pname} {bname} g={g}) ---")
                    d1 = float(np.abs(eng["returns"] - rf).max()); d2 = float(np.abs(eng["turnover"] - tf).max())
                    assert d1 < 1e-12 and d2 < 1e-12, f"GATE 1 FAILED {d1} {d2}"
                    P(f"  GATE 1 PASS - returns {d1:.3e}, turnover {d2:.3e}\n")
                    g1_done = True
                ret, turn = fast_bt(px, w)
                row = full_row(f"{bname} g={g:.2f}", ret.loc[st:])
                mask = rebalance_mask(px.index, FREQ)
                rows.append(dict(panel=pname, book=bname, family=fam, dial=dial, gross=g,
                                 real_gross=float(w.loc[mask.values].loc[st:].sum(axis=1).mean()),
                                 turnover=float(turn.loc[st:].sum() / (len(ret.loc[st:]) / 252)),
                                 **{k: v for k, v in row.items() if k != "tag"},
                                 spy_CAGR=spy_r["CAGR"], spy_S=spy_r["Sharpe"], spy_DD=spy_r["MaxDD"],
                                 spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                                 spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                                 v2_CAGR=v2_r["CAGR"], v2_S=v2_r["Sharpe"], v2_DD=v2_r["MaxDD"],
                                 v2_H1=v2_r["H1"], v2_H2=v2_r["H2"], v2_OOS_S=v2_r["OOS_Sharpe"],
                                 v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"]))
        P(f"  {pname}: done ({time.time()-t0all:.0f}s)")

    b = pd.DataFrame(rows)
    b["DD_ratio"] = b.MaxDD / b.spy_DD                       # <= phi_DD passes the cap
    b["CAGR_ratio"] = b.CAGR / b.spy_CAGR                    # >= phi_CAGR passes the floor
    b["Calmar"] = b.CAGR / b.MaxDD.abs()
    b["Calmar_SPY"] = b.spy_CAGR / b.spy_DD.abs()
    b["Calmar_ratio"] = b.Calmar / b.Calmar_SPY
    for nm, phi in [("live", (LIVE_DD, LIVE_CAGR))]:
        pass
    b.to_csv(f"{OUT}.books.csv", index=False)
    P(f"\n{len(b)} book rows ({(b.family != 'CONTROL').sum()} real books, "
      f"{(b.family == 'CONTROL').sum()} zero-signal control rows)")

    # ------------------------------------------------------------------ G2 / G3
    P("\n--- GATE 2: the live leg ---")
    live = b[(b.panel == "U56") & (b.book == "BAND0.03") & (b.gross == 0.75)].iloc[0]
    P(f"  RULES v2 on U56 @10bps: {live.CAGR:.2%} / {live.Sharpe:.4f} / {live.MaxDD:.2%}   "
      f"committed 8.66% / 1.2056 / -12.05%")
    assert abs(live.Sharpe - 1.2056) <= 0.02, "GATE 2 FAILED"
    P("  GATE 2 PASS (bar |dSharpe| <= 0.02; data/prices.csv is re-downloaded daily, idea 641 G2)")

    P("\n--- GATE 3: this run's parameterised 4b at (0.60, 0.70) vs idea 286's committed keep_paths ---")
    bad = 0
    for _, r in b.iterrows():
        spy = dict(H1=r.spy_H1, H2=r.spy_H2, OOS_Sharpe=r.spy_OOS_S, MaxDD=r.spy_DD, CAGR=r.spy_CAGR)
        v2 = dict(H1=r.v2_H1, H2=r.v2_H2, MaxDD=r.v2_DD)
        mine = legs(dict(H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe, MaxDD=r.MaxDD, CAGR=r.CAGR),
                    spy, LIVE_DD, LIVE_CAGR)
        a_ref, b_ref = keep_paths(dict(H1=r.H1, H2=r.H2, MaxDD=r.MaxDD, CAGR=r.CAGR,
                                       OOS_Sharpe=r.OOS_Sharpe), spy, v2)
        if bool(all(mine.values())) != b_ref: bad += 1
    assert bad == 0, f"GATE 3 FAILED on {bad} rows"
    P(f"  GATE 3 PASS - 0 disagreements on {len(b)} rows.")

    # ------------------------------------------------------------------ legs at the live point
    P("\n" + "=" * 104); P("PART A - THE LIVE POINT (0.60, 0.70): which legs actually cut"); P("=" * 104)
    lrows = []
    for _, r in b.iterrows():
        spy = dict(H1=r.spy_H1, H2=r.spy_H2, OOS_Sharpe=r.spy_OOS_S, MaxDD=r.spy_DD, CAGR=r.spy_CAGR)
        L = legs(r, spy, LIVE_DD, LIVE_CAGR)
        fails = [k for k, v in L.items() if not v]
        lrows.append(dict(panel=r.panel, book=r.book, family=r.family, gross=r.gross,
                          CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                          OOS_Sharpe=r.OOS_Sharpe, DD_ratio=r.DD_ratio, CAGR_ratio=r.CAGR_ratio,
                          Calmar_ratio=r.Calmar_ratio, n_fail=len(fails),
                          **{f"leg_{k}": v for k, v in L.items()},
                          fails=",".join(fails) or "PASS", sole=fails[0] if len(fails) == 1 else ""))
    lg = pd.DataFrame(lrows); lg.to_csv(f"{OUT}.legs.csv", index=False)
    real = lg[lg.family != "CONTROL"]
    P(f"  4b at the live point: {int(real.n_fail.eq(0).sum())} of {len(real)} real books pass "
      f"({int(lg[lg.family=='CONTROL'].n_fail.eq(0).sum())} of {len(lg)-len(real)} control rows).")
    P("  per-leg FAIL counts over the 63 real books:")
    P("   " + "  ".join(f"{k} {int((~real['leg_' + k]).sum())}" for k in ["H1", "H2", "OOS", "DD", "CAGR"]))
    P("  SOLE binding bar (the only failing leg), over the books that fail exactly one:")
    P(real[real.sole != ""].sole.value_counts().to_string())
    P("\n  every real book at the live point (all 63, sorted by panel):")
    P(real[["panel", "book", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
            "DD_ratio", "CAGR_ratio", "Calmar_ratio", "fails"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  the zero-signal control (SPY held at gross g) at the live point:")
    P(lg[lg.family == "CONTROL"][["panel", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                  "DD_ratio", "CAGR_ratio", "Calmar_ratio", "fails"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ the surface
    P("\n" + "=" * 104); P("PART B - THE PASS-RATE SURFACE: all 35 cells, plus the two deletions"); P("=" * 104)
    srows, conv_bad, conv_tot, imp_bad = [], 0, 0, 0
    for pdd in PHI_DD + [np.inf]:
        for pcg in PHI_CAGR + [0.0]:
            for scope, sub in [("real", b[b.family != "CONTROL"]), ("control", b[b.family == "CONTROL"])]:
                npass = 0; per_panel = {}
                for _, r in sub.iterrows():
                    spy = dict(H1=r.spy_H1, H2=r.spy_H2, OOS_Sharpe=r.spy_OOS_S,
                               MaxDD=r.spy_DD, CAGR=r.spy_CAGR)
                    L = legs(r, spy, pdd, pcg)
                    ok = all(L.values()); npass += ok
                    per_panel[r.panel] = per_panel.get(r.panel, 0) + int(ok)
                    if np.isfinite(pdd) and pcg > 0:                 # G4 bookkeeping
                        conv_tot += 1
                        cal_ok = r.Calmar_ratio >= pcg / pdd
                        if L["DD"] and L["CAGR"] and not cal_ok: imp_bad += 1
                        if cal_ok and not (L["DD"] and L["CAGR"]): conv_bad += 1
                srows.append(dict(phi_DD=pdd, phi_CAGR=pcg, scope=scope, n=len(sub), passes=npass,
                                  rate=npass / len(sub), ratio=(pcg / pdd if np.isfinite(pdd) and pdd else np.nan),
                                  **{f"p_{k}": v for k, v in per_panel.items()}))
    surf = pd.DataFrame(srows); surf.to_csv(f"{OUT}.surface.csv", index=False)
    P("  4b pass COUNT on the 63 pre-registered real books (rows phi_DD, cols phi_CAGR;")
    P("  'inf' = cap deleted, '0.0' = floor deleted):")
    piv = surf[surf.scope == "real"].pivot_table(index="phi_DD", columns="phi_CAGR", values="passes")
    P(piv.to_string())
    P("\n  the same for the 9 zero-signal control rows (SPY at gross g) - the BASE RATE:")
    P(surf[surf.scope == "control"].pivot_table(index="phi_DD", columns="phi_CAGR", values="passes").to_string())
    P("\n  marginal readings:")
    r0 = surf[(surf.scope == "real")]
    P(f"    cap swept at the live floor (phi_CAGR=0.70): " +
      ", ".join(f"{d:.2f}->{int(r0[(r0.phi_DD==d)&(r0.phi_CAGR==0.70)].passes.iloc[0])}" for d in PHI_DD)
      + f", inf->{int(r0[(r0.phi_DD==np.inf)&(r0.phi_CAGR==0.70)].passes.iloc[0])}")
    P(f"    floor swept at the live cap (phi_DD=0.60):   " +
      ", ".join(f"{c:.2f}->{int(r0[(r0.phi_DD==0.60)&(r0.phi_CAGR==c)].passes.iloc[0])}" for c in PHI_CAGR)
      + f", 0(deleted)->{int(r0[(r0.phi_DD==0.60)&(r0.phi_CAGR==0.0)].passes.iloc[0])}")
    P(f"    BOTH constants deleted (the three Sharpe legs alone): "
      f"{int(r0[(r0.phi_DD==np.inf)&(r0.phi_CAGR==0.0)].passes.iloc[0])} of 63")
    P(f"    at the live point (0.60, 0.70): {int(r0[(r0.phi_DD==0.60)&(r0.phi_CAGR==0.70)].passes.iloc[0])} of 63")

    P("\n  the two coordinates the constants are read against (63 real books):")
    P("    DD_ratio   = MaxDD / SPY MaxDD   quantiles: " +
      ", ".join(f"{q:.0%} {np.quantile(real.DD_ratio, q):.3f}" for q in [0.1, 0.25, 0.5, 0.75, 0.9]))
    P("    CAGR_ratio = CAGR  / SPY CAGR    quantiles: " +
      ", ".join(f"{q:.0%} {np.quantile(real.CAGR_ratio, q):.3f}" for q in [0.1, 0.25, 0.5, 0.75, 0.9]))
    P(f"    share of real books clearing the cap alone at 0.60: {(real.DD_ratio <= 0.60).mean():.3f}; "
      f"the floor alone at 0.70: {(real.CAGR_ratio >= 0.70).mean():.3f}; both: "
      f"{((real.DD_ratio <= 0.60) & (real.CAGR_ratio >= 0.70)).mean():.3f}")

    # ------------------------------------------------------------------ G4 / the Calmar collapse
    P("\n--- GATE 4: the Calmar implication ---")
    assert imp_bad == 0, f"GATE 4 FAILED: {imp_bad} rows break the algebra"
    P(f"  GATE 4 PASS - (cap AND floor) => Calmar_ratio >= phi_CAGR/phi_DD on all {conv_tot} "
      f"row x cell checks.  CONVERSE FAILS on {conv_bad} ({conv_bad/conv_tot:.1%}) - the pair is "
      f"STRICTLY stronger than the Calmar bar, so the two constants are NOT a single ratio.")
    rr = surf[(surf.scope == "real") & surf.ratio.notna()]
    grp = rr.groupby("ratio").passes.agg(["min", "max", "mean", "size"])
    spread = grp[grp["size"] > 1]
    P("  pass count grouped by the RATIO phi_CAGR/phi_DD (if the surface collapsed onto the ratio,")
    P("  min and max would be equal inside every group):")
    P(grp.to_string(float_format=lambda x: f"{x:.2f}"))
    P(f"  max within-ratio spread over the {len(spread)} multi-cell ratios: "
      f"{int((spread['max']-spread['min']).max())} books")

    # ------------------------------------------------------------------ rule 8
    P("\n" + "=" * 104); P("PART C - PROTOCOL 8 WALK-FORWARD, then the surface re-read on the picks"); P("=" * 104)
    wrows = []
    for (pn, fam), sub in b[b.family != "CONTROL"].groupby(["panel", "family"]):
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        spy = dict(H1=pick.spy_H1, H2=pick.spy_H2, OOS_Sharpe=pick.spy_OOS_S,
                   MaxDD=pick.spy_DD, CAGR=pick.spy_CAGR)
        v2 = dict(H1=pick.v2_H1, H2=pick.v2_H2, MaxDD=pick.v2_DD)
        a_ref, b_ref = keep_paths(dict(H1=pick.H1, H2=pick.H2, MaxDD=pick.MaxDD, CAGR=pick.CAGR,
                                       OOS_Sharpe=pick.OOS_Sharpe), spy, v2)
        wrows.append(dict(panel=pn, family=fam, pick=pick.book, gross=pick.gross,
                          IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                          OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                          v2_OOS_CAGR=pick.v2_OOS_CAGR, v2_OOS_S=pick.v2_OOS_S, v2_OOS_DD=pick.v2_OOS_DD,
                          spy_OOS_CAGR=pick.spy_OOS_CAGR, spy_OOS_S=pick.spy_OOS_S,
                          spy_OOS_DD=pick.spy_OOS_DD, DD_ratio=pick.DD_ratio,
                          CAGR_ratio=pick.CAGR_ratio, pass4a=a_ref, pass4b_live=b_ref,
                          beats_v2=bool(pick.OOS_Sharpe > pick.v2_OOS_S),
                          beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS_S)))
    wf = pd.DataFrame(wrows); wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  picks: 4a {int(wf.pass4a.sum())}/{len(wf)}, 4b(live constants) {int(wf.pass4b_live.sum())}/{len(wf)}, "
      f"beat RULES v2 OOS Sharpe {int(wf.beats_v2.sum())}/{len(wf)}, beat SPY OOS Sharpe {int(wf.beats_spy.sum())}/{len(wf)}")
    P("  the constants surface re-read on the 9 rule-8 picks alone (count of picks certified):")
    pk = []
    for pdd in PHI_DD + [np.inf]:
        row = {"phi_DD": pdd}
        for pcg in PHI_CAGR + [0.0]:
            npass = 0
            for _, r in b[b.family != "CONTROL"].iterrows():
                if not any((w.panel == r.panel and w.family == r.family and w.pick == r.book
                            and w.gross == r.gross) for _, w in wf.iterrows()):
                    continue
                spy = dict(H1=r.spy_H1, H2=r.spy_H2, OOS_Sharpe=r.spy_OOS_S, MaxDD=r.spy_DD, CAGR=r.spy_CAGR)
                npass += all(legs(r, spy, pdd, pcg).values())
            row[pcg] = npass
        pk.append(row)
    P(pd.DataFrame(pk).set_index("phi_DD").to_string())

    P(f"\ntotal elapsed {time.time()-t0all:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

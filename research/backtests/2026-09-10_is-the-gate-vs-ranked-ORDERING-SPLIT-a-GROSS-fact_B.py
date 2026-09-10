#!/usr/bin/env python3
"""Idea 462 — IS THE GATE-vs-RANKED ORDERING SPLIT A *GROSS* FACT?

Idea 460 restated 44 published panel orderings as an EXCESS over each panel's own EW_ALL
control and found the survival rate splits by BOOK FAMILY: de-grossed GATE books survive
16/16, RANKED books 6/28.  But the two families do not sit at the same exposure — the gate
books run 0.53-0.57 of realised gross (gated weight goes to CASH, never re-spread) while the
ranked books run 0.72-0.75.  "Family" and "exposure" are therefore confounded, exactly as
idea 244 warned.  This run breaks the confound by re-running the SAME restatement with the
families matched on gross, in both directions.

Pre-registration (fixed before any number was read):

  * The restatement is idea 460's, unchanged.  For metric M in {Sharpe, CAGR}, book B,
    panel P, rung c:
        RAW(B,P)    = M(B on P)
        EXCESS(B,P) = M(B on P) - M(EW_ALL on P)      [same panel, rung, window, VARIANT]
    A full ORDERING (the ranking of the three panels for one book/rung/metric) SURVIVES iff
    the RAW and EXCESS permutations are identical; a pairwise comparison FLIPS iff
    sign(RAW_i - RAW_j) != sign(EXCESS_i - EXCESS_j).

  * TWO tuned parameters and no more: FAMILY (gate / ranked) and GROSS (the three exposure
    variants below).  Cost rung (10, 25 bps) and metric are REPORTED at every level, never
    chosen.  Every grid point is printed.

  * The three GROSS variants.  Matching exposure admits two distinct implementations and the
    record has never separated them; both are run, plus the unmatched control:
      NATIVE    — idea 460 exactly.  Gate books de-grossed (gated weight -> cash), ranked
                  books at nominal gross 0.75, EW_ALL at 0.75.  This is the REPRODUCTION arm
                  and gate G4 asserts it returns idea 460's published counts.
      RESPREAD  — match the families UP.  Each gate book re-spreads its nominal 0.75 across
                  its ADMITTED names only (g/n_adm), so its nominal gross is 0.75 on every
                  day with >=1 admitted name; ranked books and EW_ALL are unchanged.  This
                  is leverage-free and it CHANGES THE BOOK (concentration into survivors).
      SCALARLO  — match the families DOWN.  Each ranked book and EW_ALL is multiplied by a
                  single constant k <= 1, so its realised gross equals the panel's native
                  gate-family realised gross; gate books are unchanged.  k is fitted on the
                  IS window (<= 2016-12-31) ONLY and applied to the whole sample, so no OOS
                  information enters it; both the fitted k and the ACHIEVED full-sample
                  realised gross are published.  This is a pure EXPOSURE move: the remainder
                  sits in cash at 0%, no leverage.
    Note stated in advance, because it is the analytical crux: with cash at 0% a scalar
    rescale is nearly Sharpe-NEUTRAL (it scales the return stream), so SCALARLO can only
    move a Sharpe ordering through the cost term and compounding drift.  The run MEASURES
    that residual instead of assuming it (see the SHARPE-INVARIANCE block).

  * Books (11 + control), unchanged from idea 460 so the arms are comparable:
      GATE   (4): RULESV2 (= BAND3 de-grossed 0.75, the live book), MA200dg, BAND6dg, ABSdg
      RANKED (7): TOP5V1, TOP10, TOP20, TOP40, TOP20V, TOP20B3, LOWVOL20
      control  : EWALL (hold every priced name at 0.75/N, no gate, no ranking)
    Panels (3): U56, B136, SMALL439 (sub-$2B less the 44 with max_1d_move >= 1.0).
    Grid = 12 books x 3 variants x 3 panels x 2 rungs = 216 points, ALL reported.

  * COMMON WINDOW.  Every number in PART B is on the intersection of the three panels'
    post-260-day-warm-up trading days, as in idea 460.

  * BOTH KEEP paths on every point.  4a is judged against the LIVE book — native RULES v2 on
    the same panel, window and rung — in every variant, because that is what the book must
    beat to replace it; 4b against SPY (data/prices.csv).  The counterfactual 4b' ("and
    beats its own variant's EW_ALL on Sharpe") is reported beside it.

  * RULE 8 (PROTOCOL 8): inside each variant the book is chosen on IS <= 2016-12-31 ONLY,
    under two selectors (IS raw Sharpe; IS excess over that variant's EW_ALL), and
    2017-01-01.. is read ONCE.  OOS CAGR/Sharpe/MaxDD reported against native RULES v2 and
    SPY on the same OOS window.  The IS->OOS stability of the panel orderings is reported
    per variant.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent lists, so their
LEVELS are biased upward and unequally so; that is why only the within-panel book-minus-
EW_ALL contrast is load-bearing here.  U56 is a fixed ETF/mega-cap list and is least biased.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .grid.csv, .orderings.csv, .walkforward.csv, .gross.csv,
.console.txt.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-10_is-the-gate-vs-ranked-ORDERING-SPLIT-a-GROSS-fact_B"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
GROSS = 0.75
RUNGS = [10, 25]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

GATE = ["RULESV2", "MA200dg", "BAND6dg", "ABSdg"]
RANKED = ["TOP5V1", "TOP10", "TOP20", "TOP40", "TOP20V", "TOP20B3", "LOWVOL20"]
BOOKS = ["EWALL"] + GATE + RANKED
PANELS = ["U56", "B136", "SMALL439"]
VARIANTS = ["NATIVE", "RESPREAD", "SCALARLO"]
FAMILY = {**{b: "GATE" for b in GATE}, **{b: "RANKED" for b in RANKED}, "EWALL": "CONTROL"}

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


# ---------------------------------------------------------------- engine twin (idea 460)
def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost, also returning drifted gross."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "gross": pd.Series(gross, index=px.index)}


def net(res, bps):
    return res["returns0"] - res["turnover"] * bps / 1e4


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------- books (idea 460 forms)
def dg_weights(px, gate, g=GROSS, cols=None):
    """De-grossed: g/N on every admitted priced name, gated weight -> CASH, never re-spread."""
    p = px if cols is None else px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(gate.reindex_like(ew).fillna(False), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def rs_weights(px, gate, g=GROSS, cols=None):
    """RE-SPREAD twin of dg_weights: g/n_admitted on the admitted names, so nominal gross is
    g on every day with >=1 admitted name and 0 (all cash) otherwise.  Leverage-free."""
    p = px if cols is None else px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    adm = e.where(gate.reindex_like(e).fillna(False), 0.0)
    w = g * adm.div(adm.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def topn_weights(px, n, cols, vol_scale=False, gate=None, g=GROSS):
    """Rank by the project's composite score; hold the top n at g/n; gated names dropped."""
    p = px[cols]
    s, above, vol20 = score(p, vol_scale=vol_scale)
    elig = s.where(above)
    if gate is not None:
        elig = elig.where(gate.reindex_like(elig).fillna(False))
    rank = elig.rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def lowvol_weights(px, n, cols, g=GROSS):
    p = px[cols]
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
    rank = vol20.rank(axis=1, ascending=True)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def build_books(px, cols, respread_gates=False):
    """The 12 pre-registered book forms on one panel.  SPY is a benchmark, never held.
    respread_gates=True swaps the four GATE books' de-grossing for re-spreading."""
    p = px[cols]
    ma = p.rolling(200).mean()
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
    NONE = pd.DataFrame(True, index=p.index, columns=p.columns)
    gw = rs_weights if respread_gates else dg_weights
    B = {}
    B["EWALL"] = dg_weights(px, NONE, cols=cols)          # no gate: dg == rs identically
    B["RULESV2"] = gw(px, band_state(p, 0.03), cols=cols)
    B["MA200dg"] = gw(px, (p > ma).fillna(False), cols=cols)
    B["BAND6dg"] = gw(px, band_state(p, 0.06), cols=cols)
    B["ABSdg"] = gw(px, (p > p.shift(252)).fillna(False), cols=cols)
    v1 = topn_weights(px, 5, cols, vol_scale=True)
    ok = (vol20 < 0.60).fillna(False).reindex(columns=px.columns).fillna(False)
    B["TOP5V1"] = (v1.where(ok, 0.0)) * (0.15 * 5 / GROSS)   # v1 is 5 x 15% = 75% gross
    B["TOP10"] = topn_weights(px, 10, cols)
    B["TOP20"] = topn_weights(px, 20, cols)
    B["TOP40"] = topn_weights(px, 40, cols)
    B["TOP20V"] = topn_weights(px, 20, cols, vol_scale=True)
    B["TOP20B3"] = topn_weights(px, 20, cols, gate=band_state(p, 0.03))
    B["LOWVOL20"] = lowvol_weights(px, 20, cols)
    return B


def panels():
    out = {}
    u = load_universe(); out["U56"] = (u, [c for c in u.columns])
    b = load_universe(broad=True); out["B136"] = (b, [c for c in b.columns])
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    out["SMALL439"] = (sm, [c for c in sm.columns if c != "SPY"])   # SPY benchmark only
    return out


def orderings(G, variant, spy_unused=None):
    """idea 460's restatement, applied inside one variant.  Returns a DataFrame of the 22
    (11 books x 2 rungs x 2 metrics = 44) ordering rows for that variant."""
    rows = []
    sub = G[G.variant == variant]
    for b in BOOKS:
        if b == "EWALL":
            continue
        for bps in RUNGS:
            for met in ("Sharpe", "CAGR"):
                raw = {k: float(sub[(sub.panel == k) & (sub.book == b) & (sub.bps == bps)][met].iloc[0])
                       for k in PANELS}
                exc = {k: raw[k] - float(sub[(sub.panel == k) & (sub.book == "EWALL") &
                                             (sub.bps == bps)][met].iloc[0]) for k in PANELS}
                ordr = ">".join(sorted(PANELS, key=lambda k: -raw[k]))
                orde = ">".join(sorted(PANELS, key=lambda k: -exc[k]))
                flips = 0; pairs = []
                for i in range(3):
                    for j in range(i + 1, 3):
                        a, c = PANELS[i], PANELS[j]
                        f = np.sign(raw[a] - raw[c]) != np.sign(exc[a] - exc[c])
                        flips += int(f); pairs.append(f"{a}|{c}:{'FLIP' if f else 'same'}")
                rows.append(dict(variant=variant, family=FAMILY[b], book=b, bps=bps, metric=met,
                                 raw_order=ordr, excess_order=orde,
                                 order_survives=(ordr == orde), pair_flips=flips,
                                 pairs=" ".join(pairs),
                                 **{f"raw_{k}": raw[k] for k in PANELS},
                                 **{f"exc_{k}": exc[k] for k in PANELS}))
    return pd.DataFrame(rows)


def main():
    PX = panels()

    # ---------------- GATES (G1-G3 are idea 460's, re-asserted on this file's own code)
    say("=== GATES ===")
    upx, ucols = PX["U56"]
    st = upx.index[260]
    w2 = rules_v2_weights(upx)
    e_res = engine_backtest(upx, w2, cost_bps=10, freq=FREQ)
    f_res = fast_backtest(upx, w2)
    g1r = float(np.abs((net(f_res, 10) - e_res["returns"]).loc[st:].values).max())
    g1t = float(np.abs((f_res["turnover"] - e_res["turnover"]).loc[st:].values).max())
    say(f"G1 fast_backtest vs engine.backtest (from {st.date()})   max|d returns| = {g1r:.3e}"
        f"   max|d turnover| = {g1t:.3e}")
    assert g1r < 1e-12 and g1t < 1e-12, "G1 FAILED"
    B3 = band_state(upx[ucols], 0.03)
    g2 = float(np.abs(dg_weights(upx, B3, cols=ucols).values - w2.values).max())
    say(f"G2 dg_weights(BAND3,0.75) vs baseline.rules_v2_weights   max|diff| = {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"
    NONEu = pd.DataFrame(True, index=upx.index, columns=ucols)
    g3a = dg_weights(upx, NONEu, cols=ucols); g3b = rs_weights(upx, NONEu, cols=ucols)
    g3 = float(np.abs(g3a.sum(axis=1).iloc[260:] - GROSS).max())
    g3d = float(np.abs(g3a.values - g3b.values).max())
    say(f"G3 EW_ALL nominal gross is exactly {GROSS} post-warm-up (max dev {g3:.3e}) and the"
        f" de-grossed and re-spread constructions agree on it exactly (max|diff| {g3d:.3e})")
    assert g3 < 1e-12 and g3d < 1e-12, "G3 FAILED"
    rsw = rs_weights(upx, B3, cols=ucols)
    nadm = B3.sum(axis=1)
    g3r = float(np.abs(rsw.sum(axis=1)[nadm > 0] - GROSS).max())
    say(f"G3b RESPREAD gate book's nominal gross is {GROSS} on every day with an admitted"
        f" name (max dev {g3r:.3e}); {int((nadm == 0).sum())} all-cash days on U56/BAND3")
    assert g3r < 1e-12, "G3b FAILED"

    # ---------------- common window
    idx = None
    for k in PANELS:
        px, cols = PX[k]
        own = px.index[260:]
        idx = own if idx is None else idx.intersection(own)
    is_idx = idx[idx <= IS_END]; oos_idx = idx[idx >= OOS_START]
    say(f"\ncommon window {idx[0].date()} -> {idx[-1].date()}  ({len(idx)} trading days, "
        f"{len(idx)/252:.1f} years);  IS {len(is_idx)} d, OOS {len(oos_idx)} d")

    # ---------------- simulate: NATIVE and RESPREAD book sets, then the SCALARLO rescale
    RET = {}       # (variant, panel, book, rung) -> net return series on the common window
    GR = {}        # (variant, panel, book) -> mean realised gross (full common window)
    GRIS = {}      # ... on the IS window only
    KFIT = {}      # (panel, book) -> the SCALARLO multiplier
    say("\n=== SIMULATION ===")
    for k in PANELS:
        px, cols = PX[k]
        BN = build_books(px, cols, respread_gates=False)
        BR = build_books(px, cols, respread_gates=True)
        res_n, res_r = {}, {}
        for b in BOOKS:
            res_n[b] = fast_backtest(px, BN[b])
            for bps in RUNGS:
                RET[("NATIVE", k, b, bps)] = net(res_n[b], bps).reindex(idx)
            GR[("NATIVE", k, b)] = float(res_n[b]["gross"].reindex(idx).mean())
            GRIS[("NATIVE", k, b)] = float(res_n[b]["gross"].reindex(is_idx).mean())
            # RESPREAD: only the four gate books change; everything else is the native object
            if b in GATE:
                res_r[b] = fast_backtest(px, BR[b])
                for bps in RUNGS:
                    RET[("RESPREAD", k, b, bps)] = net(res_r[b], bps).reindex(idx)
                GR[("RESPREAD", k, b)] = float(res_r[b]["gross"].reindex(idx).mean())
                GRIS[("RESPREAD", k, b)] = float(res_r[b]["gross"].reindex(is_idx).mean())
            else:
                for bps in RUNGS:
                    RET[("RESPREAD", k, b, bps)] = RET[("NATIVE", k, b, bps)]
                GR[("RESPREAD", k, b)] = GR[("NATIVE", k, b)]
                GRIS[("RESPREAD", k, b)] = GRIS[("NATIVE", k, b)]

        # SCALARLO target = the panel's NATIVE gate-family mean realised gross, IS window only
        target = float(np.mean([GRIS[("NATIVE", k, b)] for b in GATE]))
        say(f"  {k}: SCALARLO target realised gross = {target:.4f} (IS mean of the 4 native"
            f" gate books; ranked books natively {np.mean([GRIS[('NATIVE', k, b)] for b in RANKED]):.4f})")
        for b in BOOKS:
            if b in GATE:                      # gate books already sit at the target family
                for bps in RUNGS:
                    RET[("SCALARLO", k, b, bps)] = RET[("NATIVE", k, b, bps)]
                GR[("SCALARLO", k, b)] = GR[("NATIVE", k, b)]
                GRIS[("SCALARLO", k, b)] = GRIS[("NATIVE", k, b)]
                KFIT[(k, b)] = 1.0
                continue
            kf = target / GRIS[("NATIVE", k, b)]
            kf = min(kf, 1.0)                  # never lever; assert below that it never binds
            KFIT[(k, b)] = kf
            W = (BN[b] * kf)
            r = fast_backtest(px, W)
            for bps in RUNGS:
                RET[("SCALARLO", k, b, bps)] = net(r, bps).reindex(idx)
            GR[("SCALARLO", k, b)] = float(r["gross"].reindex(idx).mean())
            GRIS[("SCALARLO", k, b)] = float(r["gross"].reindex(is_idx).mean())
        assert all(KFIT[(k, b)] < 1.0 for b in RANKED + ["EWALL"]), "SCALARLO cap bound — check"

    SPY = PX["U56"][0]["SPY"].pct_change().fillna(0.0).reindex(idx)   # single 4b benchmark
    sm_spy = mstats(SPY)
    say(f"SPY on the common window: CAGR {sm_spy['CAGR']:.2%}  Sharpe {sm_spy['Sharpe']:.4f}  "
        f"MaxDD {sm_spy['MaxDD']:.2%}  halves {sm_spy['H1']:.3f}/{sm_spy['H2']:.3f}")

    # ---------------- exposure table: did the matching work?
    say("\n=== PART A: REALISED GROSS BY FAMILY AND VARIANT (the confound, measured) ===")
    grows = []
    for v in VARIANTS:
        for k in PANELS:
            for b in BOOKS:
                grows.append(dict(variant=v, panel=k, book=b, family=FAMILY[b],
                                  k_multiplier=(KFIT[(k, b)] if v == "SCALARLO" else 1.0),
                                  gross_IS=GRIS[(v, k, b)], gross_full=GR[(v, k, b)]))
    GRDF = pd.DataFrame(grows)
    GRDF.to_csv(OUT / f"{STAMP}.gross.csv", index=False)
    piv = GRDF[GRDF.family != "CONTROL"].pivot_table(index=["variant", "panel"],
                                                     columns="family", values="gross_full")
    piv["gap"] = piv["RANKED"] - piv["GATE"]
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    say("(NATIVE reproduces idea 460's confound: the gate family runs ~0.55 of realised gross"
        " against the ranked family's ~0.74.  RESPREAD closes it from below, SCALARLO from"
        " above.  EW_ALL, the excess control, moves with the ranked family in SCALARLO and"
        " stays at 0.75 in the other two variants — its own row is in the .gross.csv.)")

    # ---------------- PART B: the full grid, both KEEP paths
    say("\n=== PART B: 12 books x 3 variants x 3 panels x 2 rungs = 216 points ===")
    rows = []
    for v in VARIANTS:
        for k in PANELS:
            for b in BOOKS:
                for bps in RUNGS:
                    m = mstats(RET[(v, k, b, bps)])
                    mc = mstats(RET[(v, k, "EWALL", bps)])
                    mv2 = mstats(RET[("NATIVE", k, "RULESV2", bps)])   # the LIVE book
                    p4a = (m["H1"] > mv2["H1"] and m["H2"] > mv2["H2"] and m["MaxDD"] >= mv2["MaxDD"])
                    p4b = (m["H1"] > sm_spy["H1"] and m["H2"] > sm_spy["H2"]
                           and m["MaxDD"] >= 0.60 * sm_spy["MaxDD"]
                           and m["CAGR"] >= 0.70 * sm_spy["CAGR"])
                    rows.append(dict(variant=v, panel=k, book=b, family=FAMILY[b], bps=bps,
                                     **{kk: m[kk] for kk in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")},
                                     gross=GR[(v, k, b)],
                                     dSharpe_vs_EWALL=m["Sharpe"] - mc["Sharpe"],
                                     dCAGR_vs_EWALL=m["CAGR"] - mc["CAGR"],
                                     pass4a=p4a, pass4b=p4b,
                                     pass4b_plus_beats_EWALL=bool(p4b and m["Sharpe"] > mc["Sharpe"])))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n4a passes {int(G.pass4a.sum())}/{len(G)}   4b passes {int(G.pass4b.sum())}/{len(G)}"
        f"   4b AND beats own EW_ALL {int(G.pass4b_plus_beats_EWALL.sum())}/{len(G)}")
    for v in VARIANTS:
        s = G[G.variant == v]
        say(f"  {v:9s} 4a {int(s.pass4a.sum())}/{len(s)}   4b {int(s.pass4b.sum())}/{len(s)}"
            f"   4b' {int(s.pass4b_plus_beats_EWALL.sum())}/{len(s)}")

    # ---------------- SHARPE-INVARIANCE of the scalar match (the analytical crux, measured)
    say("\n=== SHARPE-INVARIANCE OF A SCALAR GROSS MATCH (measured, not assumed) ===")
    inv = []
    for k in PANELS:
        for b in RANKED + ["EWALL"]:
            for bps in RUNGS:
                a = mstats(RET[("NATIVE", k, b, bps)]); c = mstats(RET[("SCALARLO", k, b, bps)])
                inv.append(dict(panel=k, book=b, bps=bps, k=KFIT[(k, b)],
                                dSharpe=c["Sharpe"] - a["Sharpe"], dCAGR=c["CAGR"] - a["CAGR"],
                                dMaxDD=c["MaxDD"] - a["MaxDD"]))
    INV = pd.DataFrame(inv)
    say(f"scaling {len(INV)} ranked/control arms down to the gate family's gross"
        f" (k {INV.k.min():.3f}-{INV.k.max():.3f}):")
    say(f"  max |d Sharpe| = {INV.dSharpe.abs().max():.4f}   mean {INV.dSharpe.mean():+.4f}")
    say(f"  max |d CAGR|   = {INV.dCAGR.abs().max():.4f}   mean {INV.dCAGR.mean():+.4f}")
    say(f"  max |d MaxDD|  = {INV.dMaxDD.abs().max():.4f}   mean {INV.dMaxDD.mean():+.4f}")
    say("  A scalar exposure match moves CAGR and MaxDD by construction and moves Sharpe only"
        " through the cost term (turnover scales with k) and compounding drift.  Any ordering"
        " change SCALARLO produces under Sharpe is therefore a second-order cost effect, and"
        " that is the honest ceiling on 'the split is a gross fact' read through Sharpe.")

    # ---------------- ORDERINGS by variant and family
    say("\n=== PART C: ORDERINGS — raw vs excess-over-EW_ALL, by VARIANT x FAMILY ===")
    O = pd.concat([orderings(G, v) for v in VARIANTS], ignore_index=True)
    O.to_csv(OUT / f"{STAMP}.orderings.csv", index=False)
    say(O[["variant", "family", "book", "bps", "metric", "raw_order", "excess_order",
           "order_survives", "pair_flips"]].to_string(index=False))

    # G4: the NATIVE arm must reproduce idea 460's published counts exactly
    nat = O[O.variant == "NATIVE"]
    n_gate = int(nat[nat.family == "GATE"].order_survives.sum()); n_gate_t = int((nat.family == "GATE").sum())
    n_rank = int(nat[nat.family == "RANKED"].order_survives.sum()); n_rank_t = int((nat.family == "RANKED").sum())
    say(f"\nG4 REPRODUCTION of idea 460 on the NATIVE arm:"
        f"  gate {n_gate}/{n_gate_t} (published 16/16),"
        f"  ranked {n_rank}/{n_rank_t} (published 6/28),"
        f"  all {int(nat.order_survives.sum())}/{len(nat)} (published 22/44),"
        f"  pairwise flips {int(nat.pair_flips.sum())}/{3*len(nat)} (published 34/132)")
    assert (n_gate, n_gate_t) == (16, 16) and (n_rank, n_rank_t) == (6, 28), "G4 FAILED"
    assert int(nat.order_survives.sum()) == 22 and int(nat.pair_flips.sum()) == 34, "G4 FAILED"
    say("G4 PASSED — the restatement machinery is idea 460's, number for number.")

    say("\nFULL-ORDERING SURVIVAL (the headline table):")
    hdr = f"  {'variant':10s} {'GATE':>12s} {'RANKED':>12s} {'gap (pp)':>10s}"
    say(hdr)
    head = []
    for v in VARIANTS:
        s = O[O.variant == v]
        g = s[s.family == "GATE"]; r = s[s.family == "RANKED"]
        gs, rs = g.order_survives.mean(), r.order_survives.mean()
        head.append(dict(variant=v, gate_surv=int(g.order_survives.sum()), gate_n=len(g),
                         ranked_surv=int(r.order_survives.sum()), ranked_n=len(r),
                         gate_rate=gs, ranked_rate=rs, gap_pp=100 * (gs - rs)))
        say(f"  {v:10s} {int(g.order_survives.sum()):4d}/{len(g):<3d} {gs:5.1%}"
            f" {int(r.order_survives.sum()):4d}/{len(r):<3d} {rs:5.1%} {100*(gs-rs):9.1f}")
    HEAD = pd.DataFrame(head)
    say("\nPAIRWISE FLIP RATE (the count most published headlines quote):")
    for v in VARIANTS:
        s = O[O.variant == v]
        g = s[s.family == "GATE"]; r = s[s.family == "RANKED"]
        say(f"  {v:10s} gate {int(g.pair_flips.sum()):3d}/{3*len(g):<3d} ({g.pair_flips.sum()/(3*len(g)):5.1%})"
            f"   ranked {int(r.pair_flips.sum()):3d}/{3*len(r):<3d} ({r.pair_flips.sum()/(3*len(r)):5.1%})")
    say("\nby metric and rung (every grid point, no aggregation hiding a leg):")
    for v in VARIANTS:
        for met in ("Sharpe", "CAGR"):
            for bps in RUNGS:
                s = O[(O.variant == v) & (O.metric == met) & (O.bps == bps)]
                g = s[s.family == "GATE"]; r = s[s.family == "RANKED"]
                say(f"  {v:10s} {met:6s} {bps:2d}bps   gate {int(g.order_survives.sum())}/{len(g)}"
                    f"   ranked {int(r.order_survives.sum())}/{len(r)}")

    # the decisive contrasts
    gh = HEAD.set_index("variant")
    say("\nDECISIVE CONTRASTS")
    say(f"  gate family, NATIVE -> RESPREAD (matched UP):  "
        f"{gh.loc['NATIVE','gate_surv']}/{gh.loc['NATIVE','gate_n']} -> "
        f"{gh.loc['RESPREAD','gate_surv']}/{gh.loc['RESPREAD','gate_n']}")
    say(f"  ranked family, NATIVE -> SCALARLO (matched DOWN): "
        f"{gh.loc['NATIVE','ranked_surv']}/{gh.loc['NATIVE','ranked_n']} -> "
        f"{gh.loc['SCALARLO','ranked_surv']}/{gh.loc['SCALARLO','ranked_n']}")
    say(f"  family gap, NATIVE {gh.loc['NATIVE','gap_pp']:.1f} pp -> RESPREAD "
        f"{gh.loc['RESPREAD','gap_pp']:.1f} pp -> SCALARLO {gh.loc['SCALARLO','gap_pp']:.1f} pp")

    # ---------------- RULE 8 walk-forward, inside every variant
    say("\n=== PART D: RULE 8 WALK-FORWARD (book chosen on IS <= 2016-12-31, OOS read once) ===")
    mspy_o = mstats(SPY.reindex(oos_idx))
    say(f"SPY OOS: CAGR {mspy_o['CAGR']:.2%}  Sharpe {mspy_o['Sharpe']:.4f}  MaxDD {mspy_o['MaxDD']:.2%}")
    wrows = []
    for v in VARIANTS:
        for k in PANELS:
            for bps in RUNGS:
                cand = [b for b in BOOKS if b != "EWALL"]
                is_raw = {b: metrics(RET[(v, k, b, bps)].reindex(is_idx))["Sharpe"] for b in cand}
                is_ew = metrics(RET[(v, k, "EWALL", bps)].reindex(is_idx))["Sharpe"]
                is_exc = {b: is_raw[b] - is_ew for b in cand}
                for sel, d in (("IS_raw_Sharpe", is_raw), ("IS_excess_over_EWALL", is_exc)):
                    pick = max(d, key=d.get)
                    mo = mstats(RET[(v, k, pick, bps)].reindex(oos_idx))
                    mew = mstats(RET[(v, k, "EWALL", bps)].reindex(oos_idx))
                    mv2 = mstats(RET[("NATIVE", k, "RULESV2", bps)].reindex(oos_idx))
                    wrows.append(dict(variant=v, panel=k, bps=bps, selector=sel, pick=pick,
                                      pick_family=FAMILY[pick], IS_score=d[pick],
                                      OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                      OOS_EWALL_Sharpe=mew["Sharpe"],
                                      OOS_RULESV2_Sharpe=mv2["Sharpe"], OOS_RULESV2_CAGR=mv2["CAGR"],
                                      OOS_RULESV2_MaxDD=mv2["MaxDD"],
                                      OOS_SPY_Sharpe=mspy_o["Sharpe"], OOS_SPY_CAGR=mspy_o["CAGR"],
                                      OOS_SPY_MaxDD=mspy_o["MaxDD"],
                                      beats_EWALL_OOS=mo["Sharpe"] > mew["Sharpe"],
                                      beats_SPY_OOS=mo["Sharpe"] > mspy_o["Sharpe"],
                                      beats_RULESV2_OOS=mo["Sharpe"] > mv2["Sharpe"],
                                      OOS_4b=(mo["Sharpe"] > mspy_o["Sharpe"]
                                              and mo["MaxDD"] >= 0.60 * mspy_o["MaxDD"]
                                              and mo["CAGR"] >= 0.70 * mspy_o["CAGR"])))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\npicks beating their own EW_ALL out of sample: {int(W.beats_EWALL_OOS.sum())}/{len(W)}")
    say(f"picks beating SPY out of sample:              {int(W.beats_SPY_OOS.sum())}/{len(W)}")
    say(f"picks beating live RULES v2 out of sample:    {int(W.beats_RULESV2_OOS.sum())}/{len(W)}")
    say(f"picks clearing 4b out of sample:              {int(W.OOS_4b.sum())}/{len(W)}")
    say("picks by family: " + ", ".join(f"{v}: " +
        "/".join(f"{f} {int((W[(W.variant==v)].pick_family==f).sum())}" for f in ("GATE", "RANKED"))
        for v in VARIANTS))
    dis = sum(1 for v in VARIANTS for k in PANELS for bps in RUNGS
              if W[(W.variant == v) & (W.panel == k) & (W.bps == bps)].pick.nunique() > 1)
    say(f"IS selector disagreement (raw vs excess pick differently): {dis}/{len(VARIANTS)*len(PANELS)*len(RUNGS)} cells")

    # does the restatement change the CHOICE inside a variant? (idea 460 found 0/6)
    say("\ndoes the EXCESS restatement change the rule-8 PICK inside a variant?")
    for v in VARIANTS:
        s = W[W.variant == v]
        n = sum(1 for k in PANELS for bps in RUNGS
                if s[(s.panel == k) & (s.bps == bps)].pick.nunique() > 1)
        say(f"  {v:10s} {n}/6 cells disagree")

    # IS -> OOS ordering stability per variant (raw and excess)
    say("\nIS panel ordering vs OOS panel ordering (Sharpe, 10 bps), per variant:")
    for v in VARIANTS:
        hold_raw = hold_exc = tot = 0
        for b in BOOKS:
            if b == "EWALL":
                continue
            ir = {k: metrics(RET[(v, k, b, 10)].reindex(is_idx))["Sharpe"] for k in PANELS}
            orr = {k: metrics(RET[(v, k, b, 10)].reindex(oos_idx))["Sharpe"] for k in PANELS}
            ie = {k: ir[k] - metrics(RET[(v, k, "EWALL", 10)].reindex(is_idx))["Sharpe"] for k in PANELS}
            oe = {k: orr[k] - metrics(RET[(v, k, "EWALL", 10)].reindex(oos_idx))["Sharpe"] for k in PANELS}
            f = lambda d: ">".join(sorted(PANELS, key=lambda k: -d[k]))
            hold_raw += (f(ir) == f(orr)); hold_exc += (f(ie) == f(oe)); tot += 1
        say(f"  {v:10s} raw {hold_raw}/{tot} stable, excess {hold_exc}/{tot} stable")

    # ---------------- PART E: every 4b passer read once out of sample (no cherry-picking)
    say("\n=== PART E: EVERY 4b-CLEARING POINT, READ ONCE OUT OF SAMPLE (2017-01-01..) ===")
    krows = []
    for _, rr in G[G.pass4b].iterrows():
        mo = mstats(RET[(rr.variant, rr.panel, rr.book, rr.bps)].reindex(oos_idx))
        me = mstats(RET[(rr.variant, rr.panel, "EWALL", rr.bps)].reindex(oos_idx))
        mv = mstats(RET[("NATIVE", rr.panel, "RULESV2", rr.bps)].reindex(oos_idx))
        krows.append(dict(variant=rr.variant, panel=rr.panel, book=rr.book, family=rr.family,
                          bps=rr.bps, full_CAGR=rr.CAGR, full_Sharpe=rr.Sharpe, full_MaxDD=rr.MaxDD,
                          H1=rr.H1, H2=rr.H2,
                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          OOS_EWALL_Sharpe=me["Sharpe"], OOS_RULESV2_Sharpe=mv["Sharpe"],
                          OOS_beats_SPY=mo["Sharpe"] > mspy_o["Sharpe"],
                          OOS_beats_EWALL=mo["Sharpe"] > me["Sharpe"],
                          OOS_4b=(mo["Sharpe"] > mspy_o["Sharpe"]
                                  and mo["MaxDD"] >= 0.60 * mspy_o["MaxDD"]
                                  and mo["CAGR"] >= 0.70 * mspy_o["CAGR"])))
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STAMP}.keep.csv", index=False)
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n4b passers holding 4b out of sample: {int(K.OOS_4b.sum())}/{len(K)};"
        f" beating their own EW_ALL OOS: {int(K.OOS_beats_EWALL.sum())}/{len(K)};"
        f" beating SPY OOS: {int(K.OOS_beats_SPY.sum())}/{len(K)}")
    both = K[K.OOS_4b & K.OOS_beats_EWALL]
    say(f"4b passers that ALSO hold 4b OOS AND beat their own EW_ALL OOS: {len(both)}")
    if len(both):
        say(both.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- PART F: the paired DE-GROSS vs RE-SPREAD contrast (24 pairs)
    say("\n=== PART F: DE-GROSS vs RE-SPREAD, PAIRED (4 gate books x 3 panels x 2 rungs) ===")
    frows = []
    for k in PANELS:
        for b in GATE:
            for bps in RUNGS:
                a = RET[("NATIVE", k, b, bps)]; c = RET[("RESPREAD", k, b, bps)]
                ma, mc = mstats(a), mstats(c)
                mao, mco = mstats(a.reindex(oos_idx)), mstats(c.reindex(oos_idx))
                frows.append(dict(panel=k, book=b, bps=bps,
                                  dg_Sharpe=ma["Sharpe"], rs_Sharpe=mc["Sharpe"],
                                  dSharpe=mc["Sharpe"] - ma["Sharpe"],
                                  dg_CAGR=ma["CAGR"], rs_CAGR=mc["CAGR"],
                                  dCAGR=mc["CAGR"] - ma["CAGR"],
                                  dg_MaxDD=ma["MaxDD"], rs_MaxDD=mc["MaxDD"],
                                  dMaxDD=mc["MaxDD"] - ma["MaxDD"],
                                  OOS_dSharpe=mco["Sharpe"] - mao["Sharpe"],
                                  OOS_dCAGR=mco["CAGR"] - mao["CAGR"],
                                  OOS_dMaxDD=mco["MaxDD"] - mao["MaxDD"]))
    F = pd.DataFrame(frows)
    F.to_csv(OUT / f"{STAMP}.respread.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nre-spreading a gate book, over {len(F)} paired points:")
    say(f"  full sample: dSharpe mean {F.dSharpe.mean():+.4f} (wins {int((F.dSharpe>0).sum())}/{len(F)}),"
        f" dCAGR mean {F.dCAGR.mean():+.2%}, dMaxDD mean {F.dMaxDD.mean():+.2%}"
        f" (worse on {int((F.dMaxDD<0).sum())}/{len(F)})")
    say(f"  out of sample: dSharpe mean {F.OOS_dSharpe.mean():+.4f} (wins {int((F.OOS_dSharpe>0).sum())}/{len(F)}),"
        f" dCAGR mean {F.OOS_dCAGR.mean():+.2%}, dMaxDD mean {F.OOS_dMaxDD.mean():+.2%}"
        f" (worse on {int((F.OOS_dMaxDD<0).sum())}/{len(F)})")
    say("  Re-spreading is what a 'matched-gross gate book' IS; it buys CAGR and pays it in"
        " drawdown, which is why it moves the CAGR orderings and leaves the Sharpe orderings"
        " where they were.")

    # ---------------- verdict arithmetic
    say("\n=== VERDICT ARITHMETIC ===")
    gate_moved = gh.loc["NATIVE", "gate_surv"] - gh.loc["RESPREAD", "gate_surv"]
    rank_moved = gh.loc["SCALARLO", "ranked_surv"] - gh.loc["NATIVE", "ranked_surv"]
    say(f"  matching the gate family UP costs it {gate_moved} of its {gh.loc['NATIVE','gate_n']} surviving orderings")
    say(f"  matching the ranked family DOWN buys it {rank_moved} of {gh.loc['NATIVE','ranked_n']}")
    say(f"  the family gap closes by "
        f"{gh.loc['NATIVE','gap_pp'] - min(gh.loc['RESPREAD','gap_pp'], gh.loc['SCALARLO','gap_pp']):.1f} pp"
        f" at best across the two matched variants (NATIVE gap {gh.loc['NATIVE','gap_pp']:.1f} pp)")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    print(f"\nwrote {STAMP}.grid.csv .orderings.csv .walkforward.csv .gross.csv .console.txt")


if __name__ == "__main__":
    main()

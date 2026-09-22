#!/usr/bin/env python3
"""Idea 2246 (2026-09-22, lane cloud, run 11) -- DOES THE BOTH-PATHS CELL'S 8.18x/yr TURNOVER
DECOMPOSE INTO AN EQUITY LEG AND A SLEEVE LEG?

WHY THIS RUN EXISTS
    The 2026-09-20 Sunday review disqualified the record's ONLY book clearing PROTOCOL path 4a
    (against the live RULES v2 book) AND path 4b at the same time -- idea 142's by-product
    `u56 / S3-50 + band3-rw @10 bps` (11.27% / 1.2632 / -11.63%, halves 1.282/1.247, OOS 1.288)
    -- on TURNOVER alone: 8.18x/yr on u56 and 10.88x/yr on broad against the live book's 1.77x.
    Two devices have since been priced against that number and both KILLED (2254 rank
    hysteresis, 2250 slow rank refresh), each reporting a turnover FLOOR it could not get under.
    Before a third device is priced, the record should know WHICH OF THE THREE MOVING PARTS
    actually pays the 8.18x:
        (1) the top-20 composite rank churn (the equity leg),
        (2) the TLT/GLD/UUP momentum-vote x risk-parity sleeve's weekly re-solve,
        (3) the rescale-to-gross-0.75 that RE-COUPLES them (a move in either leg's raw gross
            re-prices every weight in the OTHER leg).
    This run measures those three shares at matched weights and publishes them at every cost rung.

THE BOOK (frozen, bit-for-bit the committed cell -- idea 133's `S3-50` under idea 94's `band3`
gate in the `rw` convention, weekly, t+1)
        raw equity leg : R = (1-f) * ranked(px, 20, band3, rw)          f = 0.50, n = 20
        raw sleeve leg : S = f * sleeve_weights(px, [TLT,GLD,UUP]) masked by band3
        rescale        : k = GROSS / (R+S).sum(axis=1),  w = k*R + k*S,  GROSS = 0.75
    NOTHING is tuned.  n, f, band, gross, cadence and the sleeve asset list are all FROZEN at the
    committed values; cost rung and panel are REPORTED axes, never selected on.  Tuned-parameter
    count for PROTOCOL rule 4: ZERO.

THE DECOMPOSITION (exactly additive, by construction)
    The simulator carries the drifted book PER LEG: cur_A and cur_B drift under the SAME daily
    returns and the SAME cash-inclusive normaliser the engine uses, so cur_A + cur_B == cur to
    machine precision at every date.  At a rebalance the traded vector is
        d_j = (A_j - cur_A_j) + (B_j - cur_B_j)
    and the realised turnover is sum_j |d_j|.  Each column's |d_j| is split pro rata by
    |A_j - cur_A_j| and |B_j - cur_B_j|, so EQ share + SL share == total EXACTLY (gate G4).
    Published beside it: the GROSS (uncancelled) leg turnovers sum_j|dA_j| and sum_j|dB_j|,
    whose sum exceeds the total by the amount the two legs NET against each other on the columns
    they share (TLT/GLD/UUP are selectable by the equity ranker on both panels).
    The RESCALE leg is not a column-wise object, so it is measured as a COUNTERFACTUAL: a
    DECOUPLED twin that pins each leg at its own fixed gross (0.375 each) instead of rescaling
    the blend, i.e. the same two signals with the re-coupling removed.  Its turnover gap against
    the incumbent IS the rescale's contribution.

COMPARANDS (each a real book, each published)
    INCUMBENT  the committed S3-50 + band3-rw cell
    EQONLY     the equity leg alone at full gross 0.75 (ranked 20, band3, rw)
    SLONLY     the sleeve alone at full gross 0.75 (band3-masked, rescaled)
    DECOUPLED  the incumbent with the rescale re-coupling removed (legs pinned at 0.375 each)

THE GRID (every point published, pass or fail)
    PANEL {u56, broad} x COST {5, 10, 25, 50} bps x BOOK {INCUMBENT, EQONLY, SLONLY, DECOUPLED}
    = 32 published rows, each with CAGR / Sharpe / MaxDD / H1 / H2 / OOS / turnover / 4a / 4b.

GATES (printed before any hypothesis is read)
    G1  the leg construction reproduces `i133.book_weights(px,'S3-50','band3','rw')`, max|dw| = 0.
    G2  the per-leg simulator reproduces `engine.backtest` returns AND turnover to < 1e-12.
    G3  the (u56, 10 bps, INCUMBENT) cell reproduces the Sunday review's re-run of idea 142 to
        < 5e-3 on CAGR / Sharpe / MaxDD / H1 / H2 / OOS Sharpe.
    G4  the leg attribution is exactly additive: |TO_EQ + TO_SL - TO_total| < 1e-10 at every cell.
    G5  all 32 cells published.

RULE 8 (PROTOCOL rule 8 -- walk-forward, 2017-2026 read ONCE)
    With zero tuned parameters the only legal IS-only choice left is WHICH BOOK, so the chooser is
    argmax IN-SAMPLE Sharpe over the four comparands on 2009-2016 alone, per panel per cost rung;
    the 2017-2026 leg is then reported untouched against the live RULES v2 book's OOS and SPY's OOS.

CAVEATS carried
    Survivorship (PROTOCOL rule 9 / idea 54): u56 and broad are CURRENT constituents, so every
    CAGR level is optimistic and both 4b bars are easier than on a point-in-time panel.  The
    turnover SHARES are same-tape / same-names contrasts and are first-order immune; the pass
    counts are not.  Costs are flat per unit turnover with no spread, impact or borrow.  One
    cadence (W), one execution delay (t+1), one blend (0.50), one band (3%), one gross (0.75).
    The decomposition is an ACCOUNTING of the incumbent's own trading, not a device: it cannot by
    itself lower turnover and this run proposes no rules change.
    Deterministic, standalone.  Writes .log.txt / .grid.csv / .decomp.csv / .walkforward.csv
    next to itself.  Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-22_both-paths-turnover-leg-decomposition_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"

COSTS = [5.0, 10.0, 25.0, 50.0]
PANELS = ["u56", "broad"]
BOOKS = ["INCUMBENT", "EQONLY", "SLONLY", "DECOUPLED"]
GATE, CONV, BLEND, NTOP = "band3", "rw", 0.50, 20
PHI0, DELTA0 = 0.70, 0.60          # PROTOCOL 4b: CAGR floor and MaxDD cap multipliers
LIVE_TO = 1.77                     # the live RULES v2 book's annual turnover (Sunday review)

REF142 = dict(CAGR=0.11264347733520674, Sharpe=1.2631836842789088, MaxDD=-0.11630008422595184,
              H1=1.2821692801839668, H2=1.2472607800728146, OOS_Sharpe=1.288118742321921)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
D = _load(I133, "i133")
FREQ, GROSS, OOS_START, IS_END = H.FREQ, H.GROSS, H.OOS_START, H.IS_END
S3 = D.S3

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------- the two raw legs ----
def raw_legs(px):
    """R and S: the incumbent's two RAW (pre-rescale) legs, exactly as idea 133 blends them."""
    gm = H.gate_mask(px, GATE)
    R = (1 - BLEND) * D.ranked(px, NTOP, GATE, CONV)
    S = BLEND * D.sleeve_weights(px, S3).where(gm, 0.0)
    return R.fillna(0.0), S.fillna(0.0)


def scaled_legs(px, book):
    """The two leg weight matrices A, B with A+B == the book's target weights."""
    R, S = raw_legs(px)
    if book == "EQONLY":
        A = R.mul((GROSS / R.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)
        return A, A * 0.0
    if book == "SLONLY":
        B = S.mul((GROSS / S.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)
        return B * 0.0, B
    if book == "DECOUPLED":                       # each leg pinned at its own fixed gross
        gA = GROSS * (1 - BLEND)
        gB = GROSS * BLEND
        A = R.mul((gA / R.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)
        B = S.mul((gB / S.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)
        return A, B
    tot = (R + S).sum(axis=1).replace(0, np.nan)  # INCUMBENT: one common rescale
    k = (GROSS / tot).fillna(0.0)
    return R.mul(k, axis=0).fillna(0.0), S.mul(k, axis=0).fillna(0.0)


# ------------------------------------------------- engine.backtest, carried per leg ----
def run_legged(px, A, B, cost_bps, freq=FREQ):
    """`engine.backtest` on weights A+B, with the drifted book carried SEPARATELY per leg so
    every traded unit can be attributed.  cur_A + cur_B == engine's cur at every date."""
    rets = px.pct_change().fillna(0.0)
    wA = A.reindex(px.index).fillna(0.0).shift(1)
    wB = B.reindex(px.index).fillna(0.0).shift(1)
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False)
    n = px.shape[1]
    held = np.zeros((len(px.index), n))
    cA = np.zeros(n); cB = np.zeros(n)
    to = np.zeros(len(px.index)); toA = np.zeros(len(px.index)); toB = np.zeros(len(px.index))
    gA = np.zeros(len(px.index)); gB = np.zeros(len(px.index))
    rv = rets.values; aV = wA.values; bV = wB.values; mV = mask.values
    for i in range(len(px.index)):
        if mV[i] or i == 0:
            dA = aV[i] - cA
            dB = bV[i] - cB
            d = dA + dB
            ad = np.abs(d); aA = np.abs(dA); aB = np.abs(dB)
            den = aA + aB
            shA = np.divide(aA, den, out=np.zeros_like(aA), where=den > 0)
            to[i] = ad.sum(); toA[i] = (ad * shA).sum(); toB[i] = (ad * (1 - shA)).sum()
            gA[i] = aA.sum(); gB[i] = aB.sum()
            cA = aV[i].copy(); cB = bV[i].copy()
        cur = cA + cB
        held[i] = cur
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            f = (1 + rv[i]) / tot
            cA = cA * f; cB = cB * f
    idx = px.index
    port = pd.Series((held * rv).sum(axis=1), index=idx) - pd.Series(to, index=idx) * cost_bps / 1e4
    return dict(returns=port,
                turnover=pd.Series(to, index=idx),
                to_eq=pd.Series(toA, index=idx), to_sl=pd.Series(toB, index=idx),
                gross_eq=pd.Series(gA, index=idx), gross_sl=pd.Series(gB, index=idx))


# ------------------------------------------------------------------------ scoring ----
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def score(r, spy, base):
    m = metrics(r); h1, h2 = halves(r)
    ms, mb = metrics(spy), metrics(base)
    s1, s2 = halves(spy); b1, b2 = halves(base)
    ro, so, bo = r.loc[OOS_START:], spy.loc[OOS_START:], base.loc[OOS_START:]
    mo, mso, mbo = metrics(ro), metrics(so), metrics(bo)
    p4a = (h1 > b1) and (h2 > b2) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = (h1 > s1) and (h2 > s2) and (mo["Sharpe"] > mso["Sharpe"]) \
        and (m["MaxDD"] >= DELTA0 * ms["MaxDD"]) and (m["CAGR"] >= PHI0 * ms["CAGR"])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                pass4a=p4a, pass4b=p4b,
                SPY_S=ms["Sharpe"], SPY_CAGR=ms["CAGR"], SPY_DD=ms["MaxDD"],
                SPY_OOS_S=mso["Sharpe"], SPY_OOS_CAGR=mso["CAGR"],
                BASE_S=mb["Sharpe"], BASE_CAGR=mb["CAGR"], BASE_DD=mb["MaxDD"],
                BASE_OOS_S=mbo["Sharpe"], BASE_OOS_CAGR=mbo["CAGR"],
                SPY_H1=s1, SPY_H2=s2, BASE_H1=b1, BASE_H2=b2)


def main():
    grid, decomp, wf = [], [], []
    for panel in PANELS:
        px, _ = D.panel_px(panel)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]

        # ---- G1: the leg construction IS the committed book
        A, B = scaled_legs(px, "INCUMBENT")
        ref = D.book_weights(px, "S3-50", GATE, CONV)
        g1 = float((A + B - ref).abs().to_numpy().max())
        say(f"[G1] {panel}: max|A+B - i133.book_weights(S3-50,band3,rw)| = {g1:.3e}")
        assert g1 < 1e-12, g1

        # ---- G2: the per-leg simulator IS engine.backtest
        eng = backtest(px, ref, cost_bps=10.0, freq=FREQ)
        mine = run_legged(px, A, B, 10.0)
        g2r = float((eng["returns"] - mine["returns"]).abs().max())
        g2t = float((eng["turnover"] - mine["turnover"]).abs().max())
        say(f"[G2] {panel}: max|dret| = {g2r:.3e}   max|dturnover| = {g2t:.3e}")
        assert g2r < 1e-12 and g2t < 1e-12

        legs = {b: scaled_legs(px, b) for b in BOOKS}
        for cost in COSTS:
            base = backtest(px, rules_v2_weights(px), cost_bps=cost, freq=FREQ)["returns"].loc[start:]
            base_to = backtest(px, rules_v2_weights(px), cost_bps=cost, freq=FREQ)["turnover"].loc[start:]
            yrs = len(base) / 252
            for book in BOOKS:
                a, b = legs[book]
                res = run_legged(px, a, b, cost)
                r = res["returns"].loc[start:]
                to = res["turnover"].loc[start:].sum() / yrs
                toe = res["to_eq"].loc[start:].sum() / yrs
                tos = res["to_sl"].loc[start:].sum() / yrs
                ge = res["gross_eq"].loc[start:].sum() / yrs
                gs = res["gross_sl"].loc[start:].sum() / yrs
                add = abs(toe + tos - to)
                assert add < 1e-10, (panel, cost, book, add)          # G4
                sc = score(r, spy, base)
                grid.append(dict(panel=panel, cost_bps=cost, book=book, TO=to,
                                 TO_eq=toe, TO_sl=tos, sh_eq=toe / to if to else np.nan,
                                 sh_sl=tos / to if to else np.nan,
                                 TO_eq_gross=ge, TO_sl_gross=gs,
                                 netting=(ge + gs - to),
                                 drag_eq_pp=toe * cost / 1e4 * 100,
                                 drag_sl_pp=tos * cost / 1e4 * 100,
                                 drag_pp=to * cost / 1e4 * 100,
                                 base_TO=base_to.sum() / yrs, additivity=add, **sc))
        say(f"[G4] {panel}: leg attribution additive at all {len(COSTS)*len(BOOKS)} cells "
            f"(max |TO_eq+TO_sl-TO| = {max(g['additivity'] for g in grid if g['panel']==panel):.2e})")

        # ---- the decomposition table, one row per cost rung (INCUMBENT vs DECOUPLED)
        for cost in COSTS:
            inc = next(g for g in grid if g["panel"] == panel and g["cost_bps"] == cost and g["book"] == "INCUMBENT")
            dec = next(g for g in grid if g["panel"] == panel and g["cost_bps"] == cost and g["book"] == "DECOUPLED")
            eq = next(g for g in grid if g["panel"] == panel and g["cost_bps"] == cost and g["book"] == "EQONLY")
            sl = next(g for g in grid if g["panel"] == panel and g["cost_bps"] == cost and g["book"] == "SLONLY")
            decomp.append(dict(panel=panel, cost_bps=cost, TO_total=inc["TO"],
                               TO_eq=inc["TO_eq"], TO_sl=inc["TO_sl"],
                               share_eq=inc["sh_eq"], share_sl=inc["sh_sl"],
                               TO_decoupled=dec["TO"], rescale_cost=inc["TO"] - dec["TO"],
                               share_rescale=(inc["TO"] - dec["TO"]) / inc["TO"],
                               TO_eqonly_standalone=eq["TO"], TO_slonly_standalone=sl["TO"],
                               netting=inc["netting"],
                               drag_eq_pp=inc["drag_eq_pp"], drag_sl_pp=inc["drag_sl_pp"],
                               drag_total_pp=inc["drag_pp"],
                               live_book_TO=inc["base_TO"], mult_vs_live=inc["TO"] / inc["base_TO"]))

        # ---- RULE 8: IS-only chooser over the four books, OOS read once
        for cost in COSTS:
            cells = [g for g in grid if g["panel"] == panel and g["cost_bps"] == cost]
            pick = max(cells, key=lambda g: g["IS_Sharpe"])
            wf.append(dict(panel=panel, cost_bps=cost, pick=pick["book"],
                           IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                           OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                           BASE_OOS_S=pick["BASE_OOS_S"], SPY_OOS_S=pick["SPY_OOS_S"],
                           BASE_OOS_CAGR=pick["BASE_OOS_CAGR"], SPY_OOS_CAGR=pick["SPY_OOS_CAGR"],
                           pass4a=pick["pass4a"], pass4b=pick["pass4b"], TO=pick["TO"]))

    G = pd.DataFrame(grid); DEC = pd.DataFrame(decomp); WF = pd.DataFrame(wf)

    # ---- G3
    ref_cell = G[(G.panel == "u56") & (G.cost_bps == 10.0) & (G.book == "INCUMBENT")].iloc[0]
    g3 = {k: abs(ref_cell[k] - v) for k, v in REF142.items()}
    say(f"[G3] u56/10bps/INCUMBENT vs the Sunday review's idea-142 re-run: "
        + "  ".join(f"{k} d={v:.2e}" for k, v in g3.items()))
    assert max(g3.values()) < 5e-3, g3
    say(f"[G5] {len(G)} of {len(PANELS)*len(COSTS)*len(BOOKS)} cells published.\n")

    say("=" * 118)
    say("THE DECOMPOSITION (incumbent S3-50 + band3-rw, annual turnover x/yr; shares are exact, "
        "rescale is the decoupled counterfactual)")
    say("=" * 118)
    say(DEC.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("=" * 118)
    say("ALL 32 CELLS")
    say("=" * 118)
    cols = ["panel", "cost_bps", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO", "TO_eq", "TO_sl", "sh_eq", "sh_sl",
            "drag_pp", "pass4a", "pass4b"]
    say(G[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("BENCHMARKS (same sample, per panel per cost rung)")
    say(G[["panel", "cost_bps", "BASE_CAGR", "BASE_S", "BASE_DD", "BASE_H1", "BASE_H2",
           "BASE_OOS_CAGR", "BASE_OOS_S", "SPY_CAGR", "SPY_S", "SPY_DD", "SPY_H1", "SPY_H2",
           "SPY_OOS_CAGR", "SPY_OOS_S", "base_TO"]].drop_duplicates()
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("=" * 118)
    say("RULE 8 WALK-FORWARD (book chosen by IS Sharpe on 2009-2016 only; 2017-2026 read once)")
    say("=" * 118)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")

    # ---- hypotheses
    say("=" * 118)
    say("HYPOTHESES")
    say("=" * 118)
    for panel in PANELS:
        d = DEC[DEC.panel == panel].iloc[0]
        say(f"H1  {panel}: the equity leg pays {d.share_eq:.1%} of the {d.TO_total:.2f}x/yr and the "
            f"sleeve leg {d.share_sl:.1%}  (eq {d.TO_eq:.2f}x, sleeve {d.TO_sl:.2f}x).")
        say(f"H2  {panel}: removing the rescale re-coupling moves turnover {d.TO_total:.2f}x -> "
            f"{d.TO_decoupled:.2f}x, i.e. the re-coupling is {d.share_rescale:+.1%} of the total.")
        say(f"H3  {panel}: standalone legs at full gross 0.75 run eq {d.TO_eqonly_standalone:.2f}x and "
            f"sleeve {d.TO_slonly_standalone:.2f}x; the blend's netting saves {d.netting:.2f}x/yr.")
        say(f"H4  {panel}: the book is {d.mult_vs_live:.2f}x the live RULES v2 book's own "
            f"{d.live_book_TO:.2f}x/yr on this panel.")
    say("")
    for _, r in DEC.iterrows():
        say(f"H5  {r.panel} @ {r.cost_bps:.0f} bps: cost drag {r.drag_total_pp:.2f} pp/yr = "
            f"{r.drag_eq_pp:.2f} equity + {r.drag_sl_pp:.2f} sleeve.")
    say("")
    n4a = int(G.pass4a.sum()); n4b = int(G.pass4b.sum()); nboth = int((G.pass4a & G.pass4b).sum())
    say(f"H6  KEEP paths over all {len(G)} cells: 4a passes {n4a}, 4b passes {n4b}, BOTH {nboth}.")
    if nboth:
        say(G[G.pass4a & G.pass4b][["panel", "cost_bps", "book", "CAGR", "Sharpe", "MaxDD",
                                    "H1", "H2", "OOS_Sharpe", "TO"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"H7  rule 8: the IS-only chooser picks "
        f"{dict(WF.pick.value_counts())} across the {len(WF)} panel x cost cells; "
        f"{int(WF.pass4b.sum())} of {len(WF)} picked cells clear 4b, {int(WF.pass4a.sum())} clear 4a.")

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    DEC.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.log.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

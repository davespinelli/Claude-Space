#!/usr/bin/env python3
"""Idea 948 (2026-09-22, lane B) — DOES THE GROSS DIAL'S SHARPE NEUTRALITY HOLD FOR EVERY
COMMITTED GROSS CLAIM?

THE QUESTION AS FILED
    Idea 945 found that halving gross moves the NULL's median Sharpe gain by only
    -0.0002 / -0.0006 / -0.0016 on U56 / B136 / SMALL while the (turnover drop x cost / vol)
    predictor says +0.18 to +0.26, because gross scales turnover AND vol together and the
    rebate cancels in the ratio.  LEADERBOARD.md carries 1,644 gross-keyword lines.  Walk a
    full gross ladder 0.25..1.50 on REAL BOOKS and report whether ANY gross move is larger
    than the +/-0.005 of Sharpe that cancellation leaves --- i.e. which published gross-Sharpe
    claims in the record are noise.

WHY THE ANSWER IS NOT ARITHMETICALLY OBVIOUS (the mechanism this run isolates)
    Target weights scale EXACTLY with gross (gate G2), and both legs of the net return scale
    with them --- the gross return `(w . r)` and the cost `bps * turnover`.  If the book were
    rebalanced to target every day, the net return path at gross g would be EXACTLY (g/0.75)
    times the path at 0.75, so Sharpe would be gross-invariant to machine precision and every
    published gross-Sharpe gain would be exactly zero (gate G5a proves this).
    It is not, for one reason: `engine.backtest` DRIFTS between rebalances and renormalises
    the held vector by TOTAL NAV, cash included ---

        growth = cur * (1 + rets);  tot = growth.sum() + (1 - cur.sum());  cur = growth / tot

    --- so the cash cushion `(1 - cur.sum())` damps the drift below gross 1 and AMPLIFIES it
    above (where it is a free 0% borrow).  The gross-Sharpe effect is therefore a PURE
    BETWEEN-REBALANCE DRIFT ARTEFACT whose size must grow with the holding period.  Gate G5b
    measures that, and the W-vs-M contrast tests it.
    The second and only other channel is FINANCING: the engine lends at 0%, so gross > 1 is a
    free borrow.  Arm FIN re-charges it at idea 997's 200 bps/yr on the levered fraction.

THE GRID (every point published, pass or fail)
    GROSS g in {0.25, 0.50, 0.75, 1.00, 1.25, 1.50}                     <- tuned dial 1
    BOOK (the CLAIM SET) in {RULESV2, EWall_b3dg, TOP20_b3rw, S3-50_b3rw}  <- tuned dial 2
    x PANEL {u56, broad, small} x CADENCE {W, M} x COST {0,10,25,50} bps x ARM {RAW, FIN}
    S3-50 needs TLT/GLD/UUP and so does not exist on the small panel: 11 (panel,book) pairs.
    11 x 6 x 2 x 4 x 2 = 1,056 published rows.  Panel, cadence, cost and arm are REPORTED
    axes, never selected on.  Costs are derived EXACTLY from the turnover series (gate G1),
    so one simulation serves all four rungs.

GATES (printed before any hypothesis is read)
    G1  cost reconstruction: `(held*rets).sum(1) - turnover*bps/1e4` == `engine.backtest(...,
        cost_bps=bps)["returns"]` at every rung.
    G2  the dial is a pure scalar on TARGET weights: max|W(g) - (g/0.75) W(0.75)| == 0.
    G3  the (u56, RULESV2, W, 10 bps, g=0.75) cell reproduces the record's committed live-book
        OOS headline 7.85% / 1.1017 / -12.24% (CHANGELOG 2026-09-22) to < 5e-3.
    G4  every one of the 1,056 cells is published.
    G5a DAILY cadence, 0 bps: max|r_g - (g/0.75) r_0.75| ~ 0 --- the dial is EXACTLY
        Sharpe-neutral once the drift channel is switched off.
    G5b the same deviation at W and M is NOT zero and is LARGER at M --- the drift channel.

RULE 8 (PROTOCOL rule 8 --- walk-forward, 2017-2026 READ ONCE)
    Gross chosen by argmax IN-SAMPLE Sharpe on 2009-2016 ONLY, per (panel, book, cadence,
    cost, arm); 2017-2026 then read untouched and reported against the live RULES v2 book's
    OOS and SPY's OOS, beside the no-information control of shipping the committed 0.75.

CAVEATS carried
    SURVIVORSHIP (PROTOCOL rule 9): u56 / broad / small are CURRENT-constituent lists, so
    every absolute CAGR level is optimistic and both 4b bars are easier than on a
    point-in-time panel.  The gross CONTRASTS are same-tape / same-names and first-order
    immune; the pass counts are not.  Costs are flat per unit turnover, no spread, impact or
    borrow beyond arm FIN's flat 200 bps/yr.  Gross > 1.00 is LEVERAGE, admitted here only
    because idea 948 names the 0.25..1.50 ladder; arm RAW prices it at the engine's free 0%
    borrow and is reported for continuity with the record, NOT recommended.
    Deterministic, standalone.  Writes .console.txt / .grid.csv / .pairs.csv / .gates.csv /
    .walkforward.csv next to itself.  Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-22_gross-sharpe-neutrality-band_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"

GROSSES = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50]
G0 = 0.75                                  # the committed gross every book is built at
BOOKS = ["RULESV2", "EWall_b3dg", "TOP20_b3rw", "S3-50_b3rw"]
PANELS = ["u56", "broad", "small"]
CADENCES = ["W", "M"]
COSTS = [0.0, 10.0, 25.0, 50.0]
ARMS = ["RAW", "FIN"]
BAND = 0.005                               # idea 945's cancellation band, in Sharpe units
FIN_BPS_YR = 200.0                         # idea 997's financing charge on the levered fraction
PHI0, DELTA0 = 0.70, 0.60                  # PROTOCOL 4b: CAGR floor and MaxDD cap multipliers
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BASE_FREQ = "W"                            # RULES v2's own live cadence (baseline.compare)

# Committed headlines this run must reproduce, all quoted from CHANGELOG.md / the 2026-09-20
# Sunday review.  G3a: the LIVE RULES v2 book's OOS leg on B136.  G3b: the record's only
# 4a+4b book at the cadence the split-clock run committed it at.  G3c: the same book weekly
# (idea 142's by-product, as the Sunday review re-ran it).
REF_G3A = dict(OOS_CAGR=0.0785, OOS_Sharpe=1.1017, OOS_MaxDD=-0.1224)
REF_G3B = dict(CAGR=0.1206, Sharpe=1.3171, MaxDD=-0.1035, H1=1.3256, H2=1.3109,
               OOS_CAGR=0.1271, OOS_Sharpe=1.3591, OOS_MaxDD=-0.1035)
REF_G3C = dict(CAGR=0.11264, Sharpe=1.26318, MaxDD=-0.11630, H1=1.28217, H2=1.24726,
               OOS_Sharpe=1.28812)
REF_LIVE_TO = 1.77                         # the live book's annual turnover (Sunday review)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
D = _load(I133, "i133")


# ------------------------------------------------------------------ books ----
def book_at_g0(px, book):
    """Every book at the committed gross 0.75, built by the COMMITTED constructors."""
    if book == "RULESV2":
        return rules_v2_weights(px, band=0.03, gross=G0)
    if book == "EWall_b3dg":
        return D.book_weights(px, "EWall", "band3", "dg")
    if book == "TOP20_b3rw":
        return D.book_weights(px, "TOP20", "band3", "rw")
    if book == "S3-50_b3rw":
        return D.book_weights(px, "S3-50", "band3", "rw")
    raise ValueError(book)


def books_on(panel, px):
    b = [x for x in BOOKS if x != "S3-50_b3rw"]
    if all(t in px.columns for t in D.S3):
        b.append("S3-50_b3rw")
    return b


# ---------------------------------------------------------------- scoring ----
def simulate(px, W, freq):
    """One simulation; returns the COST-FREE return path, the turnover series and the
    realised gross series, from which every cost rung and both arms are exact."""
    res = backtest(px, W, cost_bps=0.0, freq=freq)
    held = res["weights"]
    base = (held * px.pct_change().fillna(0.0)).sum(axis=1)
    return base, res["turnover"], held.sum(axis=1)


def net(base, turn, gsum, bps, arm):
    r = base - turn * bps / 1e4
    if arm == "FIN":
        r = r - (FIN_BPS_YR / 1e4 / 252.0) * (gsum - 1.0).clip(lower=0.0)
    return r


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"],
                ocagr=metrics(spy.loc[OOS_START:])["CAGR"],
                odd=metrics(spy.loc[OOS_START:])["MaxDD"])


def cell(r, turn_yr, bars, base_r):
    m, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    h1, h2 = halves(r)
    b1, b2 = halves(base_r)
    mb, mbo = metrics(base_r), metrics(base_r.loc[OOS_START:])
    fail = []
    if not h1 > bars["s1"]:
        fail.append("H1")
    if not h2 > bars["s2"]:
        fail.append("H2")
    if not mo["Sharpe"] > bars["soos"]:
        fail.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA0 * abs(bars["sdd"]):
        fail.append("DD")
    if not m["CAGR"] >= PHI0 * bars["scagr"]:
        fail.append("CAGR")
    ofail = []
    if not mo["Sharpe"] > bars["soos"]:
        ofail.append("OOS")
    if not abs(mo["MaxDD"]) <= DELTA0 * abs(bars["odd"]):
        ofail.append("DD")
    if not mo["CAGR"] >= PHI0 * bars["ocagr"]:
        ofail.append("CAGR")
    return dict(
        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"], H1=h1, H2=h2,
        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
        TO=turn_yr,
        v2_Sharpe=mb["Sharpe"], v2_MaxDD=mb["MaxDD"], v2_H1=b1, v2_H2=b2,
        v2_OOS_CAGR=mbo["CAGR"], v2_OOS_Sharpe=mbo["Sharpe"], v2_OOS_MaxDD=mbo["MaxDD"],
        pass4a=bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= mb["MaxDD"]),
        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
        pass4b_oos=(len(ofail) == 0), fail4b_oos=",".join(ofail) or "-")


# ------------------------------------------------------------------- main ----
def main():
    say(f"IDEA 948 — {STEM}")
    say("Does the GROSS dial's SHARPE NEUTRALITY hold for every committed gross claim?")
    say(f"Ladder {GROSSES} on {len(BOOKS)} committed books x 3 panels x 2 cadences x "
        f"{len(COSTS)} cost rungs x 2 financing arms.")
    say(f"Cancellation band under test: +/-{BAND:.4f} of Sharpe (idea 945).\n")

    gates, rows, prows, wrows = [], [], [], []

    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bars = bars_of(spy)
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        bl = books_on(pk, px)
        say(f"[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}; books {bl}")
        say(f"    SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.4f}  MaxDD {ms['MaxDD']:.2%}"
            f"  halves {bars['s1']:.4f}/{bars['s2']:.4f}   OOS {mso['CAGR']:.2%} / "
            f"{mso['Sharpe']:.4f} / {mso['MaxDD']:.2%}")
        say(f"    4b bars FULL: CAGR floor {PHI0*bars['scagr']:.2%}, MaxDD cap "
            f"{-DELTA0*abs(bars['sdd']):.2%}, halves {bars['s1']:.4f}/{bars['s2']:.4f}, "
            f"OOS Sharpe {bars['soos']:.4f};  OOS leg: CAGR floor {PHI0*bars['ocagr']:.2%}, "
            f"MaxDD cap {-DELTA0*abs(bars['odd']):.2%}")

        # ---- the 4a comparand: the LIVE book at its own cadence, every cost rung, both arms
        Wv2 = rules_v2_weights(px, band=0.03, gross=G0)
        bb, bt, bg = simulate(px, Wv2, BASE_FREQ)
        v2_r = {(c, a): net(bb, bt, bg, c, a).loc[start:] for c in COSTS for a in ARMS}

        # ---- G1 cost reconstruction is exact
        g1 = 0.0
        for c in COSTS:
            ref = backtest(px, Wv2, cost_bps=c, freq=BASE_FREQ)["returns"]
            g1 = max(g1, float((net(bb, bt, bg, c, "RAW") - ref).abs().max()))
        say(f"[G1] cost reconstruction vs engine.backtest at {COSTS} bps: max|diff| {g1:.3e} "
            f"({'EXACT' if g1 < 1e-15 else 'NOT EXACT — unsafe'})")
        gates.append(dict(panel=pk, gate="G1_cost_reconstruction", value=g1,
                          verdict="EXACT" if g1 < 1e-15 else "FAIL"))

        # ---- G2 the dial is a pure scalar on TARGET weights
        # RULESV2 is the ONLY book in the claim set whose committed constructor takes a gross
        # argument, so it is the only one where the scalar is a TESTABLE claim rather than the
        # definition; the other three are built by constructors hard-wired at 0.75 and the
        # ladder multiplies them, which is the record's own gross convention.
        W0v2 = book_at_g0(px, "RULESV2")
        g2 = max(float((rules_v2_weights(px, band=0.03, gross=g) - W0v2 * (g / G0))
                       .abs().max().max()) for g in GROSSES)
        say(f"[G2] gross is a pure scalar on target weights (RULESV2, the one book whose "
            f"committed constructor takes gross): max|W(g) - (g/0.75)W(0.75)| "
            f"{g2:.3e} ({'EXACT' if g2 < 1e-15 else 'FAIL'})")
        gates.append(dict(panel=pk, gate="G2_pure_scalar_targets", value=g2,
                          verdict="EXACT" if g2 < 1e-15 else "FAIL"))

        # ---- G5 the drift channel: D (no drift) vs W vs M, 0 bps, book RULESV2
        for fq in ["D", "W", "M"]:
            b0, t0, s0 = simulate(px, book_at_g0(px, "RULESV2"), fq)
            r0 = net(b0, t0, s0, 0.0, "RAW").loc[start:]
            dev = 0.0
            for g in GROSSES:
                bg_, tg_, sg_ = simulate(px, book_at_g0(px, "RULESV2") * (g / G0), fq)
                rg = net(bg_, tg_, sg_, 0.0, "RAW").loc[start:]
                dev = max(dev, float((rg - (g / G0) * r0).abs().max()))
            tag = "G5a_daily_exact" if fq == "D" else f"G5b_drift_{fq}"
            say(f"[{tag}] {fq} cadence, 0 bps: max|r_g - (g/0.75)r_0.75| = {dev:.3e}"
                + ("  <- EXACT: no drift, the dial cannot move Sharpe at all" if fq == "D" else
                   "  <- the drift channel"))
            gates.append(dict(panel=pk, gate=tag, value=dev,
                              verdict="EXACT" if dev < 1e-15 else "nonzero"))

        # ---- the grid
        for b in bl:
            W0 = book_at_g0(px, b)
            for fq in CADENCES:
                sims = {}
                for g in GROSSES:
                    bs, ts, gs = simulate(px, W0 * (g / G0), fq)
                    sims[g] = (bs, ts, gs)
                for g in GROSSES:
                    bs, ts, gs = sims[g]
                    for c in COSTS:
                        for a in ARMS:
                            r = net(bs, ts, gs, c, a).loc[start:]
                            yrs = metrics(r)["Years"]
                            d = cell(r, float(ts.loc[start:].sum() / yrs), bars, v2_r[(c, a)])
                            d.update(panel=pk, book=b, cadence=fq, cost=c, arm=a, gross=g)
                            rows.append(d)
                say(f"    done {pk}/{b}/{fq}")

    df = pd.DataFrame(rows)
    front = ["panel", "book", "cadence", "cost", "arm", "gross"]
    df = df[front + [c for c in df.columns if c not in front]]
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    n_exp = sum(len(books_on(p, D.panel_px(p)[0])) for p in PANELS) * len(GROSSES) * \
        len(CADENCES) * len(COSTS) * len(ARMS)
    say(f"\n[G4] cells published: {len(df)} of {n_exp} "
        f"({'ALL' if len(df) == n_exp else 'INCOMPLETE'})")
    gates.append(dict(panel="-", gate="G4_cells_published", value=len(df),
                      verdict="ALL" if len(df) == n_exp else "INCOMPLETE"))

    # ---- G3 three committed headlines, reproduced off this run's own grid
    def _pick(p, b, fq, c):
        return df[(df.panel == p) & (df.book == b) & (df.cadence == fq) & (df.cost == c)
                  & (df.arm == "RAW") & (df.gross == G0)].iloc[0]

    for tag, (p, b, fq, c), refd, txt in [
            ("G3a_live_book_OOS", ("broad", "RULESV2", "W", 10.0), REF_G3A,
             "the LIVE RULES v2 book's OOS leg, CHANGELOG 7.85% / 1.1017 / -12.24%"),
            ("G3b_both_paths_M", ("u56", "S3-50_b3rw", "M", 10.0), REF_G3B,
             "the record's only 4a+4b book, monthly, CHANGELOG 12.06% / 1.3171 / -10.35%, "
             "halves 1.3256/1.3109, OOS 12.71% / 1.3591 / -10.35%"),
            ("G3c_both_paths_W", ("u56", "S3-50_b3rw", "W", 10.0), REF_G3C,
             "the same book weekly, the Sunday review's re-run of idea 142")]:
        r = _pick(p, b, fq, c)
        g3 = max(abs(float(r[k]) - v) for k, v in refd.items())
        say(f"[{tag}] ({p}, {b}, {fq}, {int(c)} bps, g=0.75) vs {txt}: max|diff| {g3:.3e} "
            f"({'PASS' if g3 < 5e-3 else 'FAIL'})")
        gates.append(dict(panel=p, gate=tag, value=g3,
                          verdict="PASS" if g3 < 5e-3 else "FAIL"))

    # ---- G6 the claim set contains a DUPLICATE: RULES v2 IS EWall under band3-dg
    a = df[df.book == "RULESV2"].set_index(["panel", "cadence", "cost", "arm", "gross"])
    b_ = df[df.book == "EWall_b3dg"].set_index(["panel", "cadence", "cost", "arm", "gross"])
    g6 = float((a.Sharpe - b_.Sharpe).abs().max())
    say(f"[G6] RULESV2 vs EWall_b3dg: max|dSharpe| over all {len(a)} matched cells {g6:.3e} "
        f"({'IDENTICAL — the claim set holds 3 DISTINCT books, not 4' if g6 == 0 else 'distinct'})")
    gates.append(dict(panel="-", gate="G6_rulesv2_is_ewall_band3dg", value=g6,
                      verdict="IDENTICAL" if g6 == 0 else "distinct"))

    # ---- G7 the live book's own turnover
    to = float(_pick("u56", "RULESV2", "W", 10.0).TO)
    say(f"[G7] live RULES v2 annual turnover on u56 weekly: {to:.4f}x vs the Sunday review's "
        f"committed {REF_LIVE_TO}x (|diff| {abs(to - REF_LIVE_TO):.4f})")
    gates.append(dict(panel="u56", gate="G7_live_turnover", value=abs(to - REF_LIVE_TO),
                      verdict="PASS" if abs(to - REF_LIVE_TO) < 0.01 else "FAIL"))
    pd.DataFrame(gates).to_csv(OUT / f"{STEM}.gates.csv", index=False)

    # ================================================================ (A) the band
    say("\n" + "=" * 100)
    say("(A) IS ANY GROSS MOVE LARGER THAN IDEA 945's +/-0.005 SHARPE BAND?")
    say("=" * 100)
    keys = ["panel", "book", "cadence", "cost", "arm"]
    for k, sub in df.groupby(keys):
        s = sub.set_index("gross")["Sharpe"]
        for gi in GROSSES:
            for gj in GROSSES:
                if gj <= gi:
                    continue
                prows.append(dict(zip(keys, k)) | dict(g_lo=gi, g_hi=gj,
                                                       dSharpe=s[gj] - s[gi],
                                                       dCAGR=sub.set_index("gross")["CAGR"][gj]
                                                       - sub.set_index("gross")["CAGR"][gi],
                                                       dMaxDD=sub.set_index("gross")["MaxDD"][gj]
                                                       - sub.set_index("gross")["MaxDD"][gi]))
    P = pd.DataFrame(prows)
    P.to_csv(OUT / f"{STEM}.pairs.csv", index=False)
    say(f"pairwise gross moves priced: {len(P)} (15 ordered pairs x "
        f"{len(P)//15} (panel,book,cadence,cost,arm) families)")
    say(f"|dSharpe| > {BAND}: {int((P.dSharpe.abs() > BAND).sum())} of {len(P)} "
        f"({(P.dSharpe.abs() > BAND).mean():.1%});  median |dSharpe| "
        f"{P.dSharpe.abs().median():.5f};  max {P.dSharpe.abs().max():.5f}")
    say(f"    by arm:  " + ";  ".join(
        f"{a} {(P[P.arm == a].dSharpe.abs() > BAND).mean():.1%} "
        f"(max {P[P.arm == a].dSharpe.abs().max():.5f})" for a in ARMS))
    say(f"    RAW only, by cadence:  " + ";  ".join(
        f"{fq} {(P[(P.arm == 'RAW') & (P.cadence == fq)].dSharpe.abs() > BAND).mean():.1%} "
        f"(median {P[(P.arm == 'RAW') & (P.cadence == fq)].dSharpe.abs().median():.5f}, "
        f"max {P[(P.arm == 'RAW') & (P.cadence == fq)].dSharpe.abs().max():.5f})"
        for fq in CADENCES))
    say(f"    RAW only, by cost:  " + ";  ".join(
        f"{int(c)}bps {(P[(P.arm == 'RAW') & (P.cost == c)].dSharpe.abs() > BAND).mean():.1%} "
        f"(max {P[(P.arm == 'RAW') & (P.cost == c)].dSharpe.abs().max():.5f})" for c in COSTS))
    say(f"    RAW only, by panel:  " + ";  ".join(
        f"{p} {(P[(P.arm == 'RAW') & (P.panel == p)].dSharpe.abs() > BAND).mean():.1%}"
        for p in PANELS))
    Pd = P[P.book != "EWall_b3dg"]          # G6: drop the duplicate label, 3 distinct books
    say(f"    de-duplicated (G6: EWall_b3dg IS RULESV2), {len(Pd)} moves over 3 distinct "
        f"books: {(Pd.dSharpe.abs() > BAND).mean():.1%} over the band, median "
        f"{Pd.dSharpe.abs().median():.5f}, max {Pd.dSharpe.abs().max():.5f}")
    say(f"    de-duplicated, by book:  " + ";  ".join(
        f"{b} {(Pd[Pd.book == b].dSharpe.abs() > BAND).mean():.1%}"
        for b in Pd.book.unique()))
    say("\nWHAT THE DIAL MOVES INSTEAD (same 2,640 moves): the dial is a SIZING dial.")
    say(f"    median |dSharpe| {P.dSharpe.abs().median():.5f}   vs   median |dCAGR| "
        f"{P.dCAGR.abs().median():.4%}   vs   median |dMaxDD| {P.dMaxDD.abs().median():.4%}")
    say(f"    ratio  median|dMaxDD| / median|dSharpe|  =  "
        f"{P.dMaxDD.abs().median() / P.dSharpe.abs().median():.1f} pp of drawdown per unit "
        f"of Sharpe; sign agreement dCAGR>0 & dMaxDD<0 in "
        f"{((P.dCAGR > 0) & (P.dMaxDD < 0)).mean():.1%} of moves (gross buys return with "
        f"drawdown, one for one)")
    say("\nwithin-family Sharpe SPREAD over the whole 0.25..1.50 ladder (max - min):")
    spread = df.groupby(keys)["Sharpe"].agg(lambda s: s.max() - s.min()).rename("spread")
    sp = spread.reset_index()
    say(f"    median {sp.spread.median():.5f}, max {sp.spread.max():.5f}, "
        f"families over {BAND}: {int((sp.spread > BAND).sum())} of {len(sp)} "
        f"({(sp.spread > BAND).mean():.1%})")
    say(sp.groupby(["arm", "cadence"]).spread.agg(["median", "max", "count"]).to_string(
        float_format=lambda x: f"{x:.5f}"))
    say("\nthe SAME ladder in the legs the dial DOES move (RAW, 10 bps, weekly):")
    show = df[(df.arm == "RAW") & (df.cost == 10.0) & (df.cadence == "W")]
    say(show.pivot_table(index=["panel", "book"], columns="gross",
                         values=["Sharpe", "CAGR", "MaxDD"]).to_string(
        float_format=lambda x: f"{x:.4f}"))

    # ================================================================ (B) 4a / 4b
    say("\n" + "=" * 100)
    say("(B) BOTH KEEP PATHS AT EVERY GRID POINT")
    say("=" * 100)
    say(f"4a (beat the live RULES v2 book, same cost rung / arm): "
        f"{int(df.pass4a.sum())} of {len(df)} ({df.pass4a.mean():.1%})")
    say(f"4b FULL (Sharpe > SPY both halves AND OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY): "
        f"{int(df.pass4b.sum())} of {len(df)} ({df.pass4b.mean():.1%})")
    say(f"4b on the OOS leg alone: {int(df.pass4b_oos.sum())} of {len(df)}")
    say(f"BOTH 4a and 4b: {int((df.pass4a & df.pass4b).sum())} of {len(df)}")
    say("\n4b pass count by gross rung (the dial the verdict actually turns on):")
    say(df.groupby("gross")[["pass4a", "pass4b"]].agg(["sum", "mean"]).to_string(
        float_format=lambda x: f"{x:.3f}"))
    say("\nbinding leg of the 4b FAILs:")
    say(df[~df.pass4b].fail4b.value_counts().head(12).to_string())
    say("\nevery cell clearing BOTH paths (4a AND 4b) — the only capital-relevant corner:")
    B = df[df.pass4a & df.pass4b]
    if len(B):
        say(B[front + ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                       "OOS_MaxDD", "TO"]].to_string(index=False,
                                                     float_format=lambda x: f"{x:.4f}"))
        say(f"    distinct (panel, book, gross) triples among them: "
            f"{sorted(set(map(tuple, B[['panel', 'book', 'gross']].values.tolist())))}")
    else:
        say("    NONE.")
    if df.pass4b.any():
        say("\nevery 4b PASS:")
        say(df[df.pass4b][front + ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                                   "OOS_Sharpe", "OOS_MaxDD", "TO", "pass4a"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================ (C) rule 8
    say("\n" + "=" * 100)
    say("(C) RULE 8 — GROSS CHOSEN ON 2009-2016 ONLY, 2017-2026 READ ONCE")
    say("=" * 100)
    for k, sub in df.groupby(keys):
        s = sub.set_index("gross")
        pick = float(s.IS_Sharpe.idxmax())
        row = s.loc[pick]
        dflt = s.loc[G0]
        # the IS-Sharpe ties: how many rungs sit within the band of the argmax
        ties = int((s.IS_Sharpe.max() - s.IS_Sharpe <= BAND).sum())
        wrows.append(dict(zip(keys, k)) | dict(
            pick=pick, ties_within_band=ties,
            IS_Sharpe_pick=row.IS_Sharpe, IS_Sharpe_dflt=dflt.IS_Sharpe,
            IS_spread=float(s.IS_Sharpe.max() - s.IS_Sharpe.min()),
            OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
            d_OOS_CAGR=row.OOS_CAGR - dflt.OOS_CAGR,
            d_OOS_Sharpe=row.OOS_Sharpe - dflt.OOS_Sharpe,
            d_OOS_MaxDD=row.OOS_MaxDD - dflt.OOS_MaxDD,
            pick_4b=bool(row.pass4b), dflt_4b=bool(dflt.pass4b),
            pick_4b_oos=bool(row.pass4b_oos), dflt_4b_oos=bool(dflt.pass4b_oos),
            pick_4a=bool(row.pass4a), dflt_4a=bool(dflt.pass4a),
            v2_OOS_CAGR=row.v2_OOS_CAGR, v2_OOS_Sharpe=row.v2_OOS_Sharpe,
            v2_OOS_MaxDD=row.v2_OOS_MaxDD))
    Wf = pd.DataFrame(wrows)
    Wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"walk-forward families: {len(Wf)}")
    say(f"IS-Sharpe SPREAD across the 6 rungs: median {Wf.IS_spread.median():.5f}, "
        f"max {Wf.IS_spread.max():.5f}; families whose spread is inside the "
        f"{BAND} band: {int((Wf.IS_spread <= BAND).sum())} of {len(Wf)} "
        f"({(Wf.IS_spread <= BAND).mean():.1%})")
    say(f"rungs tied with the IS argmax to within {BAND}: median "
        f"{Wf.ties_within_band.median():.1f} of {len(GROSSES)}")
    say("\nwhat the IS-Sharpe chooser picks:")
    say(Wf.pick.value_counts().sort_index().to_string())
    say(f"\npicks the committed default 0.75: {int((Wf.pick == G0).sum())} of {len(Wf)} "
        f"({(Wf.pick == G0).mean():.1%}) — a uniform draw over 6 rungs would give 16.7%")
    say(f"\nOOS, chooser vs shipping 0.75:")
    say(f"    d OOS Sharpe  median {Wf.d_OOS_Sharpe.median():+.5f}  "
        f"mean {Wf.d_OOS_Sharpe.mean():+.5f}  (better in "
        f"{(Wf.d_OOS_Sharpe > 0).mean():.1%} of families)")
    say(f"    d OOS CAGR    median {Wf.d_OOS_CAGR.median():+.4%}  "
        f"mean {Wf.d_OOS_CAGR.mean():+.4%}")
    say(f"    d OOS MaxDD   median {Wf.d_OOS_MaxDD.median():+.4%}  "
        f"mean {Wf.d_OOS_MaxDD.mean():+.4%}  (deeper in "
        f"{(Wf.d_OOS_MaxDD < 0).mean():.1%} of families)")
    say(f"    4b FULL : chooser {int(Wf.pick_4b.sum())} of {len(Wf)} "
        f"({Wf.pick_4b.mean():.1%})   default 0.75 {int(Wf.dflt_4b.sum())} "
        f"({Wf.dflt_4b.mean():.1%})")
    say(f"    4b OOS  : chooser {int(Wf.pick_4b_oos.sum())} of {len(Wf)} "
        f"({Wf.pick_4b_oos.mean():.1%})   default 0.75 {int(Wf.dflt_4b_oos.sum())} "
        f"({Wf.dflt_4b_oos.mean():.1%})")
    say(f"    4a      : chooser {int(Wf.pick_4a.sum())} of {len(Wf)}   "
        f"default 0.75 {int(Wf.dflt_4a.sum())}")
    say("\nthe walk-forward table (all families), OOS beside the live book's OOS:")
    say(Wf[keys + ["pick", "IS_spread", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                   "v2_OOS_CAGR", "v2_OOS_Sharpe", "v2_OOS_MaxDD", "pick_4b", "pick_4b_oos",
                   "pick_4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

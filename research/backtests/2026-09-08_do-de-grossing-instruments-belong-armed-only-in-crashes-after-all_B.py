#!/usr/bin/env python3
"""QUEUE idea 249 — do-de-grossing-instruments-belong-armed-only-in-crashes-after-all
(lane B, 2026-09-08)

QUESTION (pre-registered, verbatim from QUEUE.md idea 249)
    "idea 246 found the sign idea 75 reported for stops runs the OTHER way for pure exposure
    cuts: `gross50` and `ddctl8` have always-on delta +12.6 and +5.8 pp/yr ON crash days
    against -9.2 and -4.6 OFF them, i.e. the crash regime is the one regime they pay in.
    That is idea 6's breadth sleeve and idea 40's premise, and both were killed on the FULL
    period number.  Re-price both at matched realised gross with the switching cost
    (switch_mult 5.9-11.6x) charged explicitly, and report whether either is cheap enough to
    survive once LEAK is not divided out.  Max 2 params."

WHAT IS BEING TESTED, AND WHY THE COMPARAND IS THE WHOLE POINT
    An arm that de-grosses ONLY in crashes holds ~0.62-0.69 mean gross where its always-on
    sibling holds ~0.37.  Compared against the ungated 0.75-gross control it therefore looks
    good for a reason that has nothing to do with timing: it holds less of a book whose
    drawdown it is being judged on, and more of it than the always-on arm whose CAGR floor it
    is being judged against.  Idea 244 established that a matched-mean-gross control is
    NECESSARY for any dial that moves realised gross.  So the decisive comparand here is a
    CONSTANT de-gross of the same base book to the SAME realised mean gross:

        MATCHED(a)  ==  base book scaled by a constant mu, mu solved so that
                        mean realised gross == mean realised gross of arm `a`

    and the reportable statistic is arm minus MATCHED, not arm minus control.

    Idea 246's `L` divided the conditional arm's loss by the armed fraction f (0.171 for
    spy200), which multiplies its off-regime residue by (1-f)/f = 4.9-10.6x and made LEAK 52%
    of the answer.  Nothing here is divided by f.  Every number below is a RAW annualised
    difference on the whole sample, with the switching cost charged inside the simulator, and
    the same books are re-run at 0 bps so the cost bill is separable rather than assumed.

H1 (the queue's question)  For family in {gross, ddctl}: does the spy200-armed conditional arm
        beat its OWN MATCHED-GROSS static control on annualised return and on Sharpe, at 10
        bps, over the full sample?  Falsified if the median difference is <= 0 or the sign
        count is a coin flip.
H2 (the naive comparand)   The same difference measured against the UNMATCHED do-nothing
        control, reported beside H1 so the size of the gross confound is visible.
H3 (the cost bill)         The 0-bps rung.  If H1 fails at 10 bps but passes at 0 bps, the arm
        is a switching-cost casualty and switch_mult is the reason; if it fails at both, the
        crash-day edge is not there once LEAK is not divided out.
H4 (KEEP paths)            PROTOCOL rule 4a/4b evaluated on EVERY row, including the matched
        controls, so a pass that the matched control already has is not credited to the arm.
RULE 8                     In each (panel, book, cost) cell the (FAMILY, STRENGTH) pair is
        chosen on 2009-2016 IS Sharpe alone from a menu that includes the do-nothing control
        AND all 8 matched static controls, and read ONCE on 2017-2026.  Regret is reported
        against do-nothing and against the best matched static.

GRID — exactly TWO tuned parameters (FAMILY, STRENGTH).  Every grid point printed and written
    to the .grid.csv.
      panels    u56 (56 names), broad (136), small (439 sub-$2B after idea 130's bad-split
                drop; SPY held as benchmark only)                       [reported, not tuned]
      books     V1u, TOP20, EWall — idea 94's three ungated base books  [reported, not tuned]
      FAMILY    gross  (idea 66's parameter-free lever; gross x spy200 IS the classic 200d
                        market-timing overlay and idea 6's sleeve shape)
                ddctl  (idea 22/40's book-drawdown control, k=0.5 fixed at its published value)
      STRENGTH  gross: m in {0.00, 0.25, 0.50, 0.75}   (m=0.50 is idea 246's `gross50`)
                ddctl: D in {0.04, 0.08, 0.12, 0.16}   (D=0.08 is idea 246's `ddctl8`)
      regime    spy200 (SPY < its own 200d MA) — the queue's crash regime, PRIMARY.
                breadth20 (panel breadth <= expanding 20th pct, 3y min) reported as a
                never-selected robustness arm; it is never used for any verdict.
      always    the unconditional sibling of every arm, f = 1
      matched   one constant-gross static control per conditional arm, gross-matched at that
                arm's own realised mean gross in that same cell and cost rung
      costs     0, 10 (the PROTOCOL rung) and 25 bps, every arm re-run at each — never derived
                from a turnover identity, because the ddctl state machine reads NET equity and
                so its BOOK is cost-dependent.

ARMING MECHANICS: idea 94's harness and idea 246's `run_cond`, imported and not re-implemented.
    Arming gates the instrument's ACTION, never its STATE, so `always` is a strict special case
    of every conditional arm.  The regime is read at close t-1 and applied at t; breadth20 uses
    an EXPANDING quantile with a 3y minimum, so there is no full-sample threshold anywhere.

SURVIVORSHIP: all three panels are current-constituent lists (idea 54), so every absolute CAGR
    is optimistic.  H1-H3 are paired differences inside one cell on the same days and are far
    less exposed; the KEEP-path and rule-8 LEVELS are fully exposed and are upper bounds.

Deterministic, standalone.  Imports research/baseline.py, idea 94's harness and idea 246's
simulator; modifies nothing outside research/backtests/.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_do-de-grossing-instruments-belong-armed-only-in-crashes-after-all_B"
OUT = ROOT / "research" / "backtests"

_spec = importlib.util.spec_from_file_location(
    "i246", OUT / "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
H = M.H                                                   # idea 94's harness, via idea 246

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PROTO_COST = 10.0
COSTS = [0.0, 10.0, 25.0]
PANELS = ["u56", "broad", "small"]
BOOKS = ["V1u", "TOP20", "EWall"]
REGIMES = ["spy200", "breadth20"]                          # spy200 primary, breadth20 reported
GROSS_M = [0.00, 0.25, 0.50, 0.75]
DDCTL_D = [0.04, 0.08, 0.12, 0.16]
K_DD = 0.5                                                 # idea 40's published value, fixed
MATCH_TOL = 1e-4                                           # mean-gross match tolerance
MATCH_ITERS = 12

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def arms_spec():
    """The 8 (FAMILY, STRENGTH) grid points.  Two tuned dimensions, nothing else."""
    out = []
    for m in GROSS_M:
        out.append(dict(arm=f"gross{int(round(m*100)):02d}", fam="gross", strength=m,
                        kw=dict(m=m)))
    for d in DDCTL_D:
        out.append(dict(arm=f"ddctl{int(round(d*100)):02d}", fam="ddctl", strength=d,
                        kw=dict(D=d, k=K_DD)))
    return out


ARMS = arms_spec()


def solve_matched(px, W_base, target_gross, bps):
    """Constant multiplier mu on the base book whose realised MEAN gross equals target_gross.

    g(mu) is very close to linear in mu (the 0.75-gross book never trips run_cond's s>1
    renormaliser), so a linear seed plus secant refinement converges in 2-3 runs; the loop
    below still runs to tolerance and the achieved gap is reported for every match."""
    g1 = float(M.run_cond(px, W_base, m=1.0, bps=bps)["gross"].mean())
    mu = target_gross / g1
    res = M.run_cond(px, W_base, m=mu, bps=bps)
    g = float(res["gross"].mean())
    lo_mu, lo_g = 0.0, 0.0
    it = 0
    while abs(g - target_gross) > MATCH_TOL and it < MATCH_ITERS:
        it += 1
        denom = (g - lo_g)
        mu_new = mu + (target_gross - g) * (mu - lo_mu) / denom if abs(denom) > 1e-12 else mu
        mu_new = float(np.clip(mu_new, 0.0, 4.0))
        lo_mu, lo_g = mu, g
        mu = mu_new
        res = M.run_cond(px, W_base, m=mu, bps=bps)
        g = float(res["gross"].mean())
    return mu, res, abs(g - target_gross)


def stats(r, to, gross, start, v1, bars):
    p4a, p4b, h1, h2, mm, mo = M.keep_paths(r.loc[start:], v1, bars)
    return dict(ann=M.ann(r.loc[start:]), CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                IS_Sharpe=metrics(r.loc[start:IS_END])["Sharpe"],
                turnover=float(to.loc[start:].mean() * 252),
                mean_gross=float(gross.loc[start:].mean()),
                pass4a=p4a, pass4b=p4b)


def main():
    grid, mech, wf, matchlog, live = [], [], [], [], []
    checked = False

    for pname in PANELS:
        px, names = M.panel(pname)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bars = M.bars_of(spy)
        ms = metrics(spy)
        v1w = rules_v1_weights(px[names]).reindex(columns=px.columns).fillna(0.0)
        v1 = {c: backtest(px, v1w, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        v2w = rules_v2_weights(px[names]).reindex(columns=px.columns).fillna(0.0)
        v2 = {c: backtest(px, v2w, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        for c in COSTS:
            for lab, rr in (("RULES v1", v1[c]), ("RULES v2 (LIVE)", v2[c])):
                mm, mo = metrics(rr), metrics(rr.loc[OOS_START:])
                hh1, hh2 = M.halves(rr)
                live.append(dict(panel=pname, cost=c, book=lab, CAGR=mm["CAGR"],
                                 Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=hh1, H2=hh2,
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"]))

        say("\n" + "=" * 200)
        say(f"PANEL {pname}: {len(names)} tradable names, {px.index[0].date()} -> "
            f"{px.index[-1].date()} | eval from {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
        say(f"  SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f} | "
            f"4b bars: DD cap {0.60*abs(bars['sdd']):.2%}, CAGR floor {0.70*bars['scagr']:.2%}")

        arms_mask = {r: M.regime(px, names, r) for r in REGIMES}
        fr = {}
        for r in REGIMES:
            v = arms_mask[r].loc[start:]
            fr[r] = float(v.mean())
            say(f"  regime {r:10s} armed {v.mean():.3f} ({int(v.sum())} days) | "
                f"IS {v.loc[:IS_END].mean():.3f} OOS {v.loc[OOS_START:].mean():.3f}")

        sub = px[names]
        for book in BOOKS:
            W_base = H.targets(sub, book).reindex(columns=px.columns).fillna(0.0)

            if not checked:                                # CHECK (a): exact reproduction
                for c in COSTS:
                    a = M.run_cond(px, W_base, bps=c)["r"]
                    b = backtest(px, W_base, cost_bps=c, freq=FREQ)["returns"]
                    d = float(np.abs(a - b).max())
                    say(f"  CHECK(a) run_cond(no instrument) == engine.backtest @{c:g}bps: "
                        f"max|diff| = {d:.3e}")
                    assert d < 1e-12, d
                checked = True

            for c in COSTS:
                ctl = M.run_cond(px, W_base, bps=c)
                sctl = stats(ctl["r"], ctl["to"], ctl["gross"], start, v1[c], bars)
                grid.append(dict(panel=pname, book=book, cost=c, arm="CONTROL", fam="none",
                                 strength=np.nan, regime="none", armed_frac=1.0,
                                 match_gap=0.0, mu=1.0, **sctl))

                for a in ARMS:
                    alw = M.run_cond(px, W_base, bps=c, **a["kw"])
                    salw = stats(alw["r"], alw["to"], alw["gross"], start, v1[c], bars)
                    grid.append(dict(panel=pname, book=book, cost=c, arm=a["arm"],
                                     fam=a["fam"], strength=a["strength"], regime="always",
                                     armed_frac=1.0, match_gap=0.0, mu=np.nan, **salw))

                    for rg in REGIMES:
                        con = M.run_cond(px, W_base, armed=arms_mask[rg], bps=c, **a["kw"])
                        scon = stats(con["r"], con["to"], con["gross"], start, v1[c], bars)
                        grid.append(dict(panel=pname, book=book, cost=c, arm=a["arm"],
                                         fam=a["fam"], strength=a["strength"], regime=rg,
                                         armed_frac=fr[rg], match_gap=0.0, mu=np.nan, **scon))

                        mu, mres, gap = solve_matched(px, W_base, scon["mean_gross"], c)
                        smat = stats(mres["r"], mres["to"], mres["gross"], start, v1[c], bars)
                        grid.append(dict(panel=pname, book=book, cost=c,
                                         arm=f"MATCHED[{a['arm']}/{rg}]", fam=a["fam"],
                                         strength=a["strength"], regime=f"matched-{rg}",
                                         armed_frac=fr[rg], match_gap=gap, mu=mu, **smat))
                        matchlog.append(dict(panel=pname, book=book, cost=c, arm=a["arm"],
                                             regime=rg, target=scon["mean_gross"],
                                             achieved=smat["mean_gross"], mu=mu, gap=gap))

                        # switching cost, charged explicitly and never divided by f
                        sm = ((scon["turnover"] / salw["turnover"] / fr[rg])
                              if salw["turnover"] > 0 else np.nan)
                        mech.append(dict(
                            panel=pname, book=book, cost=c, arm=a["arm"], fam=a["fam"],
                            strength=a["strength"], regime=rg, armed_frac=fr[rg],
                            d_ann_vs_matched=scon["ann"] - smat["ann"],
                            d_cagr_vs_matched=(scon["CAGR"] - smat["CAGR"]) * 100.0,
                            d_shp_vs_matched=scon["Sharpe"] - smat["Sharpe"],
                            d_dd_vs_matched=scon["MaxDD"] - smat["MaxDD"],
                            d_ann_vs_control=scon["ann"] - sctl["ann"],
                            d_shp_vs_control=scon["Sharpe"] - sctl["Sharpe"],
                            d_ann_vs_always=scon["ann"] - salw["ann"],
                            gross_cond=scon["mean_gross"], gross_always=salw["mean_gross"],
                            gross_ctl=sctl["mean_gross"], match_gap=gap,
                            to_cond=scon["turnover"], to_always=salw["turnover"],
                            to_matched=smat["turnover"], switch_mult=sm,
                            cost_bill_pp=(scon["turnover"] - smat["turnover"]) * c / 1e4 * 100.0,
                            oos_shp_cond=scon["OOS_Sharpe"], oos_shp_matched=smat["OOS_Sharpe"],
                            p4b_cond=scon["pass4b"], p4b_matched=smat["pass4b"],
                            p4a_cond=scon["pass4a"], p4a_matched=smat["pass4a"]))

    G = pd.DataFrame(grid)
    Mx = pd.DataFrame(mech)
    ML = pd.DataFrame(matchlog)
    LV = pd.DataFrame(live).drop_duplicates()
    LV.to_csv(OUT / f"{STEM}.livebase.csv", index=False)
    say("\n" + "=" * 200)
    say("LIVE-BASELINE CONTEXT — idea 246's imported `keep_paths` judges 4a against RULES v1 "
        "(the pre-2026-09-06 convention).  RULES v2 has been live since 2026-09-06 and is "
        "printed here so no 4a count in this file is read as a claim against the live book:")
    say(LV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    Mx.to_csv(OUT / f"{STEM}.mech.csv", index=False)
    ML.to_csv(OUT / f"{STEM}.match.csv", index=False)

    say("\n" + "=" * 200)
    say(f"GRID: {len(G)} runs written to {STEM}.grid.csv "
        f"({G.arm.nunique()} arm labels x {len(PANELS)} panels x {len(BOOKS)} books x "
        f"{len(COSTS)} cost rungs)")
    say(f"GROSS MATCH QUALITY: max |achieved - target| mean gross over all "
        f"{len(ML)} matched controls = {ML.gap.max():.2e} (tolerance {MATCH_TOL:g}); "
        f"mu range {ML.mu.min():.4f} - {ML.mu.max():.4f}")

    say("\n----- FULL GRID (every point) -----")
    cols = ["panel", "book", "cost", "arm", "regime", "armed_frac", "mean_gross", "turnover",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "pass4a", "pass4b"]
    say(G[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ H1 / H2 / H3
    say("\n" + "=" * 200)
    say("H1 — CONDITIONAL ARM minus its OWN MATCHED-GROSS STATIC CONTROL (raw, never divided "
        "by the armed fraction; switching cost charged inside the simulator)")
    for rg in REGIMES:
        for c in COSTS:
            sub = Mx[(Mx.regime == rg) & (Mx.cost == c)]
            for fam in ["gross", "ddctl"]:
                s = sub[sub.fam == fam]
                pa, kn, n = M.signtest(s.d_ann_vs_matched.values)
                ps, ksn, ns = M.signtest(s.d_shp_vs_matched.values)
                tag = "PRIMARY" if rg == "spy200" else "robust "
                say(f"  [{tag}] {rg:10s} @{c:5.1f}bps {fam:6s} n={len(s):3d} | "
                    f"d_ann median {s.d_ann_vs_matched.median():+7.3f} pp/yr "
                    f"({(s.d_ann_vs_matched > 0).sum():2d}/{len(s)} positive, sign p {pa:.4f}) | "
                    f"d_Sharpe median {s.d_shp_vs_matched.median():+7.4f} "
                    f"({(s.d_shp_vs_matched > 0).sum():2d}/{len(s)} positive, sign p {ps:.4f}) | "
                    f"d_CAGR median {s.d_cagr_vs_matched.median():+7.3f} pp/yr "
                    f"({(s.d_cagr_vs_matched > 0).sum():2d}/{len(s)} positive) | "
                    f"d_MaxDD median {s.d_dd_vs_matched.median():+7.4f}")

    say("\nH2 — THE SAME ARMS AGAINST THE UNMATCHED DO-NOTHING CONTROL (the naive comparand)")
    for rg in REGIMES:
        for c in COSTS:
            sub = Mx[(Mx.regime == rg) & (Mx.cost == c)]
            for fam in ["gross", "ddctl"]:
                s = sub[sub.fam == fam]
                say(f"  {rg:10s} @{c:5.1f}bps {fam:6s} n={len(s):3d} | "
                    f"vs CONTROL   d_ann median {s.d_ann_vs_control.median():+7.3f} "
                    f"({(s.d_ann_vs_control > 0).sum():2d}/{len(s)} pos), "
                    f"d_Sharpe median {s.d_shp_vs_control.median():+7.4f} "
                    f"({(s.d_shp_vs_control > 0).sum():2d}/{len(s)} pos) | "
                    f"mean gross cond {s.gross_cond.mean():.4f} vs ctl {s.gross_ctl.mean():.4f} "
                    f"vs always {s.gross_always.mean():.4f}")

    say("\nH3 — THE COST BILL, CHARGED EXPLICITLY (switch_mult = (TO_cond/TO_always)/f, "
        "never used to normalise any return)")
    for rg in REGIMES:
        for fam in ["gross", "ddctl"]:
            s = Mx[(Mx.regime == rg) & (Mx.fam == fam) & (Mx.cost == PROTO_COST)]
            s0 = Mx[(Mx.regime == rg) & (Mx.fam == fam) & (Mx.cost == 0.0)]
            say(f"  {rg:10s} {fam:6s} | switch_mult median {s.switch_mult.median():6.3f} "
                f"(min {s.switch_mult.min():.3f} max {s.switch_mult.max():.3f}, "
                f">1 in {(s.switch_mult > 1).sum()}/{len(s)}) | "
                f"turnover cond {s.to_cond.median():5.2f}x vs matched {s.to_matched.median():5.2f}x "
                f"vs always {s.to_always.median():5.2f}x | "
                f"explicit cost bill vs matched {s.cost_bill_pp.median():+6.3f} pp/yr | "
                f"d_ann vs matched @0bps {s0.d_ann_vs_matched.median():+7.3f} -> "
                f"@10bps {s.d_ann_vs_matched.median():+7.3f}")

    say("\nBY (FAMILY, STRENGTH), spy200 @10bps — every grid point, medians over 9 panel x book "
        "cells")
    rows = []
    for a in ARMS:
        s = Mx[(Mx.regime == "spy200") & (Mx.arm == a["arm"]) & (Mx.cost == PROTO_COST)]
        rows.append(dict(arm=a["arm"], fam=a["fam"], strength=a["strength"], n=len(s),
                         d_ann_vs_matched=s.d_ann_vs_matched.median(),
                         pos=int((s.d_ann_vs_matched > 0).sum()),
                         d_shp_vs_matched=s.d_shp_vs_matched.median(),
                         pos_shp=int((s.d_shp_vs_matched > 0).sum()),
                         d_ann_vs_control=s.d_ann_vs_control.median(),
                         d_ann_vs_always=s.d_ann_vs_always.median(),
                         switch_mult=s.switch_mult.median(),
                         gross_cond=s.gross_cond.median(),
                         p4b_cond=int(s.p4b_cond.sum()), p4b_matched=int(s.p4b_matched.sum())))
    T = pd.DataFrame(rows)
    say(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    T.to_csv(OUT / f"{STEM}.bystrength.csv", index=False)

    # ------------------------------------------------------------------ H4 KEEP paths
    say("\n" + "=" * 200)
    say("H4 — KEEP PATHS (PROTOCOL rule 4), every one of the "
        f"{len(G)} rows evaluated")
    for lab, sel in [("CONTROL", G.regime == "none"),
                     ("ALWAYS-ON", G.regime == "always"),
                     ("COND spy200", G.regime == "spy200"),
                     ("COND breadth20", G.regime == "breadth20"),
                     ("MATCHED (spy200 gross)", G.regime == "matched-spy200"),
                     ("MATCHED (breadth20 gross)", G.regime == "matched-breadth20")]:
        s = G[sel]
        say(f"  {lab:26s} n={len(s):4d} | 4a {int(s.pass4a.sum()):4d} | 4b {int(s.pass4b.sum()):4d}")

    # the only pass that would be NEW: conditional passes 4b where its matched twin does not
    m = Mx[(Mx.regime == "spy200")]
    new4b = m[(m.p4b_cond) & (~m.p4b_matched)]
    new4a = m[(m.p4a_cond) & (~m.p4a_matched)]
    say(f"\n  spy200 arms passing 4b where their OWN matched-gross control does NOT: "
        f"{len(new4b)}/{len(m)}   (4a: {len(new4a)}/{len(m)})")
    if len(new4b):
        say(new4b[["panel", "book", "cost", "arm", "gross_cond", "d_ann_vs_matched",
                   "d_shp_vs_matched", "oos_shp_cond", "oos_shp_matched"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    best = G[(G.regime == "spy200") & (G.pass4b) & (G.cost == PROTO_COST)]
    if len(best):
        say("\n  spy200 4b passers @10bps (levels are survivorship-inflated upper bounds):")
        say(best.sort_values("Sharpe", ascending=False)
            [["panel", "book", "arm", "mean_gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "OOS_Sharpe", "turnover"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ rule 8
    say("\n" + "=" * 200)
    say("RULE 8 — (FAMILY, STRENGTH) chosen on 2009-2016 IS Sharpe alone; menu = 8 spy200 arms "
        "+ do-nothing control + 8 matched static controls; 2017-2026 read ONCE")
    for pname in PANELS:
        for book in BOOKS:
            for c in COSTS:
                cell = G[(G.panel == pname) & (G.book == book) & (G.cost == c)]
                ctl = cell[cell.regime == "none"].iloc[0]
                menu = cell[cell.regime.isin(["spy200", "matched-spy200", "none"])]
                pick = menu.loc[menu.IS_Sharpe.idxmax()]
                cond_only = cell[cell.regime == "spy200"]
                best_oos = cond_only.loc[cond_only.OOS_Sharpe.idxmax()]
                bestmat = cell[cell.regime == "matched-spy200"]
                bm = bestmat.loc[bestmat.OOS_Sharpe.idxmax()]
                rho = M.spearman(menu.IS_Sharpe.values, menu.OOS_Sharpe.values)
                wf.append(dict(panel=pname, book=book, cost=c, pick=pick.arm,
                               pick_regime=pick.regime, pick_OOS_Sharpe=pick.OOS_Sharpe,
                               pick_OOS_CAGR=pick.OOS_CAGR, pick_OOS_MaxDD=pick.OOS_MaxDD,
                               ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                               regret_vs_control=pick.OOS_Sharpe - ctl.OOS_Sharpe,
                               regret_vs_best_matched=pick.OOS_Sharpe - bm.OOS_Sharpe,
                               best_cond_OOS=best_oos.OOS_Sharpe, best_cond_arm=best_oos.arm,
                               spearman_IS_OOS=rho))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  chooser picks a CONDITIONAL spy200 arm in "
        f"{int((W.pick_regime == 'spy200').sum())}/{len(W)} cells, a MATCHED static in "
        f"{int((W.pick_regime == 'matched-spy200').sum())}, do-nothing in "
        f"{int((W.pick_regime == 'none').sum())}")
    say(f"  OOS regret vs do-nothing:    mean {W.regret_vs_control.mean():+.4f}  "
        f"median {W.regret_vs_control.median():+.4f}  wins "
        f"{int((W.regret_vs_control > 0).sum())}/{len(W)}")
    say(f"  OOS regret vs best matched:  mean {W.regret_vs_best_matched.mean():+.4f}  "
        f"median {W.regret_vs_best_matched.median():+.4f}  wins "
        f"{int((W.regret_vs_best_matched > 0).sum())}/{len(W)}")
    say(f"  median Spearman(IS Sharpe, OOS Sharpe) across the menu: "
        f"{W.spearman_IS_OOS.median():.4f}")
    say(f"  IS pick == OOS oracle among the conditional arms in "
        f"{int((W.pick == W.best_cond_arm).sum())}/{len(W)} cells")
    for c in COSTS:
        w = W[W.cost == c]
        say(f"    @{c:5.1f}bps: pick OOS Sharpe median {w.pick_OOS_Sharpe.median():.4f} vs "
            f"do-nothing {w.ctl_OOS_Sharpe.median():.4f}; pick OOS CAGR median "
            f"{w.pick_OOS_CAGR.median():.2%} vs {w.ctl_OOS_CAGR.median():.2%}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.grid.csv / .mech.csv / .match.csv / .bystrength.csv / "
        f".walkforward.csv / .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

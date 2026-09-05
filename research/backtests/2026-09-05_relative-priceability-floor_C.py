#!/usr/bin/env python3
"""QUEUE idea 123 — relative-priceability-floor (lane C, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 119 showed idea 94's absolute floor (dMaxDD > 0.10 pp) publishes 11 negative prices in
a cell where every arm moves under 10% of the book's own -34% drawdown.  Re-tabulate every
price the project has published under a RELATIVE floor (dMaxDD >= 10% of the control's
|MaxDD|), mark the rows that stop being priceable, and re-run idea 97's tier statement on
what is left.  Bears on idea 117."

What is on trial.  Not a book and not an instrument — a PUBLICATION RULE.  Every price this
project has quoted is

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)     pp CAGR per pp MaxDD

and idea 94 publishes it whenever the denominator exceeds an ABSOLUTE 0.10 pp.  That floor is
scale-free in the wrong direction: 0.10 pp is 0.3% of a 34-pp small-cap drawdown and 0.6% of
a 16-pp large-cap one, so the same bar admits a ratio-of-noise on one panel and a real
measurement on another.  The proposal is a RELATIVE floor, dMaxDD >= phi * |MaxDD_ctl|, whose
headline phi = 0.10 is idea 119's own pre-registered materiality bar, adopted here unchanged
so this run cannot pick its own threshold.

Harness.  This run does NOT re-implement idea 94 or idea 97.  It imports idea 94's module
directly (targets / run / price / ladder_slope / arm_specs / GATES / window / spearman) and
rebuilds idea 97's three panels under idea 97's own conventions, then asserts that the
regenerated price list equals idea 97's COMMITTED pricelist.csv row-for-row before any new
number is computed.  Only the floor layer, the removal census and the selectors are new.

Panels (3, all reported) — idea 97's, unchanged
    u56    research/universe.json         (56 names)
    broad  research/universe_broad.json   (136 names)
    small  data/prices_small.csv.gz       (439 names: SPY held out as benchmark, the 44 names
           with max_1d_move >= 1.0 in data/small_meta.csv dropped).  Trading-day indexed,
           eval from 2011-01-13, so its IS window is 2011-2016.
Books (idea 94's, ungated, 75% gross): V1u, TOP20, EWall.  Costs 10 and 25 bps.
3 x 3 x 2 = 18 cells, 16 priced arms + a 19-point static-gross ladder each, 3 windows
(full / IS 2009-2016 / OOS 2017-2026) => 864 price rows.

The two floors
    ABS(0.10 pp)     idea 94's published convention: publish iff dMaxDD > 0.10 pp.
    REL(phi)         publish iff dMaxDD >= phi * |MaxDD_ctl| IN THAT WINDOW (and > 0).
                     Per-window denominators, because idea 122 showed the IS window's own
                     depth (SPY -22.1%) is what makes IS denominators unmeasurable.

Tuned parameters (PROTOCOL rule 4): TWO.
    (1) phi, the relative floor.  Grid {0.00, 0.02, 0.05, 0.10, 0.20}, ALL five reported
        everywhere; 0.10 is the headline and is inherited from idea 119, not chosen here.
    (2) the instrument family in the walk-forward selector (idea 97's single tuned parameter,
        inherited).
Everything else — arms, books, costs, windows, gross, the 1.0 pp IS-eligibility depth in
idea 94's selector, the "unpriceable tier ranks last" convention — is inherited and reported.

Pre-registered predictions (written before any number was read)
    R1  The relative floor at phi=0.10 removes at least 80% of the NEGATIVE published prices
        (idea 119 found 0 of 11 material on small/V1u; the claim here is that this
        generalises to the whole published list).
    R2  The rows the relative floor removes are LESS stable than the rows it keeps: lower
        IS->OOS price-sign agreement and larger |rate_OOS - rate_IS|.  This is the only
        argument for the floor that is not aesthetic.
    R3  Idea 97's tier statement changes under the floor: at least one of the 54 published
        clause rows flips, and the small-panel C1 inversion (the ordering reversal) is
        affected, because the small panel is where the denominators are shallowest relative
        to the book's own drawdown.
    R4  Restricting idea 94's walk-forward selector to relative-admissible arms does NOT cost
        OOS Sharpe (if it does, the floor is REPORT-ONLY, exactly as idea 122's sign test).
    R5  No arm here is a new 4b pass (measurement run; 4a/4b computed and reported anyway).

Execution realism (PROTOCOL rule 2): idea 94's simulator — weights decided at close t applied
at t+1, weekly, long-only, no leverage, costs charged inside the loop.

SURVIVORSHIP: all three panels are current-constituent lists; the small panel's bias is the
worst and falls on beaten-down names.  Every number here is a within-cell delta on matched
days, and the object under test is a publication rule rather than a return, but the
small-panel rows should still be read as a lower bound on any gate's cost.

Calendar-day index (open idea 38) is unfixed for u56/broad and affects control and arm
equally inside every cell; the small panel is trading-day indexed.

Deterministic, standalone.  Imports research/baseline.py and idea 94's module; modifies
nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_relative-priceability-floor_C"
BT = ROOT / "research" / "backtests"
I94 = BT / "2026-09-04_drawdown-insurance-price-list_B.py"
I97_PRICELIST = BT / "2026-09-05_price-list-tier-bar_B.pricelist.csv"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS, BOOKS, LADDER, PCOST = H.COSTS, H.BOOKS, H.LADDER, H.PCOST
PANELS = ["u56", "broad", "small"]
WINDOWS = ["full", "IS", "OOS"]
PHIS = [0.00, 0.02, 0.05, 0.10, 0.20]
PHI0 = 0.10                      # headline, inherited from idea 119
ABS_FLOOR = 0.10                 # idea 94's published absolute floor, pp
BIG = 1e9                        # an unpriceable tier ranks last (idea 97's convention)

TIER = {}
for g in H.GATES:
    for conv in ("dg", "rw"):
        TIER[f"{g}-{conv}"] = "T1_gate"
TIER["ddctl-8/.5/recover"] = "T3_ddctl"
TIER["ddctl-8/.5/high"] = "T3_ddctl"
TIER["stop15"] = "T4_stop"
TIER["stop25"] = "T4_stop"
TIER["ebud-0.10"] = "X_ebud"
TIER["ebud-0.20"] = "X_ebud"
ALL_TIERS = ["T1_gate", "T2_lever", "T3_ddctl", "T4_stop"]
CLAIMS = [("C1", "T1_gate", "T2_lever"), ("C2", "T2_lever", "T3_ddctl"),
          ("C3", "T3_ddctl", "T4_stop")]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
FMT = lambda x: f"{x:.3f}"                                              # noqa: E731


# ---------------------------------------------------------------- panels (idea 97's)
def panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)})"
    raise ValueError(name)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def margins(r, bars):
    h1, h2 = halves(r)
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def raw_price(rc, ra):
    """Idea 94's price WITHOUT the floor: the raw numerator, denominator and ratio."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd != 0 else np.nan), abs(mc["MaxDD"]) * 100.0, \
        ma["Sharpe"] - mc["Sharpe"]


def admissible(dd, ctl_dd, phi):
    """Relative floor: buy at least phi of the control's OWN drawdown, in this window."""
    return bool(dd > 0 and dd >= phi * ctl_dd)


# ---------------------------------------------------------------- verification
def verify(px_u56):
    print("=" * 200)
    print("VERIFICATION — idea 94's harness, then idea 97's committed price list")
    print("=" * 200)
    worst = 0.0
    start = px_u56.index[260]
    for b in BOOKS:
        W = H.targets(px_u56, b)
        a = H.run(px_u56, W, bps=PCOST)["r"].loc[start:]
        e = backtest(px_u56, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"  engine-equivalence (control vs engine.backtest @10bps, u56): max|diff| = "
          f"{worst:.3e}  ({'EXACT' if worst < 1e-12 else 'NOT EXACT — UNSAFE'})")
    r = H.run(px_u56, H.targets(px_u56, "EWall", "vol60", "dg"), bps=10.0)["r"].loc[start:]
    m = metrics(r)
    print(f"  published EWall+vol60-dg u56 @10bps: CAGR {m['CAGR']:.1%} (pub 11.6%)  "
          f"Sharpe {m['Sharpe']:.3f} (pub 1.133)  MaxDD {m['MaxDD']:.1%} (pub -16.9%)")
    return worst < 1e-12 and abs(m["Sharpe"] - 1.133) < 5e-3


def verify_pricelist(P):
    """Every regenerated full-window row must equal idea 97's COMMITTED file."""
    pub = pd.read_csv(I97_PRICELIST)
    key = ["panel", "book", "cost", "arm"]
    mine = P[P.window == "full"].copy()
    j = pub.merge(mine, on=key, suffixes=("_pub", "_new"))
    d1 = float((j.dCAGR_pub - j.dCAGR_new).abs().max())
    d2 = float((j.dMaxDD_pub - j.dMaxDD_new).abs().max())
    pubr, newr = j["rate"].values, j["rate_abs"].values
    both = np.isfinite(pubr) & np.isfinite(newr)
    d3 = float(np.max(np.abs(pubr[both] - newr[both]))) if both.any() else 0.0
    nanok = int((np.isfinite(pubr) == np.isfinite(newr)).sum())
    print(f"  idea 97 pricelist.csv: matched {len(j)} of {len(pub)} published rows; "
          f"max|d dCAGR| {d1:.2e}  max|d dMaxDD| {d2:.2e}  max|d rate| {d3:.2e}  "
          f"NaN-pattern agreement {nanok}/{len(j)}")
    ok = len(j) == len(pub) and d1 < 1e-9 and d2 < 1e-9 and d3 < 1e-9 and nanok == len(j)
    print(f"  -> {'REPRODUCED idea 97 EXACTLY' if ok else 'MISMATCH — do not trust what follows'}")
    return ok


# ---------------------------------------------------------------- the grid
def build():
    rows, prices, cellinfo = [], [], []
    for pn in PANELS:
        px, spy_full, label = panel(pn)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bars = bars_of(spy)
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c,
                              freq=FREQ)["returns"].loc[start:] for c in COSTS}
        mv1 = metrics(v1_net[PCOST])
        mv1o = metrics(v1_net[PCOST].loc[OOS_START:])
        print("\n" + "=" * 200)
        print(f"PANEL {pn} — {label}: {px.shape[1]} holdable names, eval from {start.date()} "
              f"-> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
        print(f"  SPY       CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  "
              f"MaxDD {ms['MaxDD']:.2%}  | OOS CAGR {mso['CAGR']:.2%}  Sharpe {mso['Sharpe']:.3f}"
              f"  MaxDD {mso['MaxDD']:.2%}")
        print(f"  RULES v1  CAGR {mv1['CAGR']:.2%}  Sharpe {mv1['Sharpe']:.3f}  "
              f"MaxDD {mv1['MaxDD']:.2%}  | OOS CAGR {mv1o['CAGR']:.2%}  "
              f"Sharpe {mv1o['Sharpe']:.3f}  MaxDD {mv1o['MaxDD']:.2%}")
        print(f"  4b bars: Sharpe > {bars['s1']:.3f}/{bars['s2']:.3f}/{bars['soos']:.3f}, "
              f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")

        rets, ladders = {}, {}
        for b in BOOKS:
            for c in COSTS:
                lad = []
                for m_ in LADDER:
                    r = H.run(px, H.targets(px, b), m=m_, bps=c)["r"].loc[start:]
                    mm = metrics(r)
                    lad.append(dict(m=m_, CAGR=mm["CAGR"], MaxDD=mm["MaxDD"],
                                    IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                    IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                                    OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                    OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"]))
                ladders[(b, c)] = pd.DataFrame(lad)
            for name, kind, kwargs, (g, conv) in H.arm_specs():
                W = H.targets(px, b, g, conv)
                for c in COSTS:
                    res = H.run(px, W, bps=c, **kwargs)
                    r = res["r"].loc[start:]
                    rets[(b, name, c)] = r
                    mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
                    mg = margins(r, bars)
                    rows.append(dict(
                        panel=pn, book=b, arm=name, tier=TIER.get(name, "-"), kind=kind, cost=c,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        TO=res["to"].loc[start:].sum() / mm["Years"],
                        gross=res["gross"].loc[start:].mean(),
                        p4b=all(v > 0 for v in mg.values()),
                        f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-",
                        p4a=H.pass4a(r, v1_net[c])))

        for b in BOOKS:
            for c in COSTS:
                L = ladders[(b, c)]
                slope = {w: H.ladder_slope(L, f"{p}MaxDD", f"{p}CAGR")
                         for w, p in (("full", ""), ("IS", "IS_"), ("OOS", "OOS_"))}
                rc = rets[(b, "control", c)]
                for name, kind, _, _ in H.arm_specs():
                    if name == "control":
                        continue
                    ra = rets[(b, name, c)]
                    for w in WINDOWS:
                        dc, dd, rate, ctl_dd, dsh = raw_price(H.window(rc, w), H.window(ra, w))
                        prices.append(dict(
                            panel=pn, book=b, cost=c, arm=name, tier=TIER.get(name, "-"),
                            kind=kind, window=w, dCAGR=dc, dMaxDD=dd, rate_raw=rate,
                            ctl_MaxDD=ctl_dd, dd_pct_ctl=100.0 * dd / ctl_dd,
                            dSharpe=dsh, lever=slope[w],
                            pub_abs=bool(dd > ABS_FLOOR),
                            rate_abs=(rate if dd > ABS_FLOOR else np.nan),
                            **{f"adm_{int(100*phi):02d}": admissible(dd, ctl_dd, phi)
                               for phi in PHIS}))
        cellinfo.append(dict(panel=pn, spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"],
                             spy_MaxDD=ms["MaxDD"], spy_OOS_CAGR=mso["CAGR"],
                             spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_MaxDD=mso["MaxDD"],
                             v1_OOS_CAGR=mv1o["CAGR"], v1_OOS_Sharpe=mv1o["Sharpe"],
                             v1_OOS_MaxDD=mv1o["MaxDD"]))
        globals().setdefault("_RETS", {})[pn] = rets
    return pd.DataFrame(rows), pd.DataFrame(prices), pd.DataFrame(cellinfo)


# ---------------------------------------------------------------- floor tabulation
def floor_table(P):
    print("\n" + "=" * 200)
    print("1. THE RE-TABULATION — every price the project publishes, under both floors")
    print("   ABS = idea 94's published rule (dMaxDD > 0.10 pp).  REL(phi) = dMaxDD >= phi * "
          "|MaxDD_ctl| in that window.  ALL five phi reported.")
    print("=" * 200)
    out = []
    for w in WINDOWS:
        for phi in PHIS:
            col = f"adm_{int(100*phi):02d}"
            for pn in PANELS + ["ALL"]:
                s = P[P.window == w] if pn == "ALL" else P[(P.window == w) & (P.panel == pn)]
                pub = s[s.pub_abs]
                kept = pub[pub[col]]
                lost = pub[~pub[col]]
                neg = pub[pub.rate_abs < 0]
                negl = neg[~neg[col]]
                out.append(dict(window=w, phi=phi, panel=pn, published_abs=len(pub),
                                total_rows=len(s), kept=len(kept), removed=len(lost),
                                pct_removed=100.0 * len(lost) / max(len(pub), 1),
                                negatives=len(neg), negatives_removed=len(negl),
                                med_dd_kept=kept.dMaxDD.median(),
                                med_dd_removed=lost.dMaxDD.median(),
                                med_pctctl_removed=lost.dd_pct_ctl.median()))
    F = pd.DataFrame(out)
    print(F.to_string(index=False, float_format=FMT))

    col = f"adm_{int(100*PHI0):02d}"
    pub = P[P.pub_abs]

    def census(keys):
        rec = []
        for k, d in pub.groupby(keys):
            rec.append(dict(zip(keys if isinstance(keys, list) else [keys],
                                k if isinstance(k, tuple) else (k,)),
                            published=len(d), kept=int(d[col].sum()),
                            removed=int((~d[col]).sum()),
                            pct_removed=100.0 * float((~d[col]).mean()),
                            negatives=int((d.rate_abs < 0).sum()),
                            neg_removed=int(((d.rate_abs < 0) & (~d[col])).sum())))
        return pd.DataFrame(rec)

    print("\n  --- headline phi = 0.10, by book (the address idea 122 found) ---")
    print(census(["book"]).to_string(index=False, float_format=FMT))
    print("\n  --- headline phi = 0.10, by panel x window ---")
    print(census(["panel", "window"]).to_string(index=False, float_format=FMT))
    print("\n  --- headline phi = 0.10, by tier ---")
    print(census(["tier"]).to_string(index=False, float_format=FMT))

    print("\n  --- R1: the negative prices (every published row with rate < 0) ---")
    neg = pub[pub.rate_abs < 0].sort_values("rate_abs")
    print(neg[["panel", "book", "cost", "arm", "window", "dCAGR", "dMaxDD", "ctl_MaxDD",
               "dd_pct_ctl", "rate_abs", "dSharpe"] + [f"adm_{int(100*p):02d}" for p in PHIS]]
          .to_string(index=False, float_format=FMT))
    n_neg, n_neg_removed = len(neg), int((~neg[col]).sum())
    print(f"\n  R1: negative published prices {n_neg}; removed by REL(0.10) {n_neg_removed} "
          f"({100.0*n_neg_removed/max(n_neg,1):.1f}%)  -> "
          f"{'CONFIRMED' if n_neg_removed >= 0.8 * n_neg else 'REFUTED'} (bar was 80%)")
    return F, n_neg, n_neg_removed


# ---------------------------------------------------------------- R2: do removals matter?
def stability_of_removed(P):
    print("\n" + "=" * 200)
    print("2. R2 — ARE THE REMOVED ROWS THE UNSTABLE ONES?  (the only non-aesthetic argument)")
    print("   For every (panel, book, cost, arm) whose FULL-window price is published under "
          "ABS, compare IS and OOS prices.")
    print("=" * 200)
    col = f"adm_{int(100*PHI0):02d}"
    piv = P.pivot_table(index=["panel", "book", "cost", "arm"], columns="window",
                        values=["rate_raw", "dMaxDD", "dd_pct_ctl", "rate_abs", col],
                        aggfunc="first")
    rec = []
    for k, r in piv.iterrows():
        if not np.isfinite(r[("rate_abs", "full")]):
            continue
        ri, ro = r[("rate_raw", "IS")], r[("rate_raw", "OOS")]
        rec.append(dict(panel=k[0], book=k[1], cost=k[2], arm=k[3],
                        kept=bool(r[(col, "full")]), rate=r[("rate_abs", "full")],
                        dd_pct_ctl=r[("dd_pct_ctl", "full")],
                        IS_rate=ri, OOS_rate=ro,
                        sign_agree=(np.sign(ri) == np.sign(ro))
                        if (np.isfinite(ri) and np.isfinite(ro)) else np.nan,
                        abs_gap=abs(ro - ri) if (np.isfinite(ri) and np.isfinite(ro)) else np.nan,
                        IS_dd_pos=r[("dMaxDD", "IS")] > 0, OOS_dd_pos=r[("dMaxDD", "OOS")] > 0))
    S = pd.DataFrame(rec)
    for lab, d in (("KEPT by REL(0.10)", S[S.kept]), ("REMOVED by REL(0.10)", S[~S.kept])):
        sa = d.sign_agree.dropna().astype(float)
        print(f"  {lab:22s} n={len(d):3d}  IS->OOS sign agreement "
              f"{100.0*sa.mean() if len(sa) else float('nan'):5.1f}% (n={len(sa)})  "
              f"median |rate_OOS - rate_IS| {d.abs_gap.median():7.3f}  "
              f"IS dMaxDD>0 {100.0*d.IS_dd_pos.mean():5.1f}%  "
              f"OOS dMaxDD>0 {100.0*d.OOS_dd_pos.mean():5.1f}%  "
              f"median |rate| {d.rate.abs().median():6.3f}")
    kept, rem = S[S.kept], S[~S.kept]
    ka = float(kept.sign_agree.dropna().astype(float).mean())
    ra_ = float(rem.sign_agree.dropna().astype(float).mean())
    kg, rg = kept.abs_gap.median(), rem.abs_gap.median()
    ok = (ka > ra_) and (kg < rg)
    print(f"\n  R2: kept rows are more stable on BOTH measures "
          f"(sign {ka:.3f} vs {ra_:.3f}; gap {kg:.3f} vs {rg:.3f}): "
          f"{'CONFIRMED' if ok else 'NOT CONFIRMED — see both numbers'}")
    print("\n  Spearman of |rate| against denominator size (a price that is a ratio of noise "
          "should be LARGE when the denominator is small):")
    for pn in PANELS:
        d = S[S.panel == pn]
        print(f"    {pn:6s} rho(|rate|, dMaxDD as % of ctl) = "
              f"{H.spearman(d.rate.abs().values, d.dd_pct_ctl.values):+.3f}  (n={len(d)})")
    print(f"    ALL    rho = {H.spearman(S.rate.abs().values, S.dd_pct_ctl.values):+.3f} "
          f"(n={len(S)})")
    return S


# ---------------------------------------------------------------- 3. tier statement
def tiers(P, use_rel):
    """Idea 97's tier layer, with the admissibility rule swapped."""
    col = f"adm_{int(100*PHI0):02d}"
    out = []
    for (pn, b, c, w), g in P.groupby(["panel", "book", "cost", "window"]):
        d = dict(panel=pn, book=b, cost=c, window=w,
                 floor=("REL(0.10)" if use_rel else "ABS(0.10pp)"))
        d["T2_lever"] = float(g.lever.iloc[0])
        for t in ("T1_gate", "T3_ddctl", "T4_stop", "X_ebud"):
            v = g[g.tier == t]
            ok = v[col] if use_rel else v.pub_abs
            fin = v.rate_raw[ok.values & np.isfinite(v.rate_raw.values)]
            d[t] = float(fin.median()) if len(fin) else np.nan
            d[f"n_{t}"] = int(len(fin))
        for cid, a, bb in CLAIMS:
            pa = d[a] if np.isfinite(d[a]) else BIG
            pb = d[bb] if np.isfinite(d[bb]) else BIG
            d[cid] = bool(pa < pb) if (pa != BIG or pb != BIG) else np.nan
        ranks = {t: (d[t] if np.isfinite(d[t]) else BIG) for t in ALL_TIERS}
        d["order"] = ">".join(sorted(ranks, key=lambda t: (ranks[t], ALL_TIERS.index(t))))
        d["exact"] = d["order"] == ">".join(ALL_TIERS)
        out.append(d)
    return pd.DataFrame(out)


def tier_report(Ta, Tr):
    print("\n" + "=" * 200)
    print("3. IDEA 97'S TIER STATEMENT, RE-RUN ON WHAT SURVIVES THE RELATIVE FLOOR")
    print("   C1 gate < lever | C2 lever < DD rule | C3 DD rule < stop.  Unpriceable tier "
          "ranks LAST (idea 97's convention).")
    print("=" * 200)
    both = pd.concat([Ta, Tr])
    print(both[["floor", "panel", "book", "cost", "window", "T1_gate", "T2_lever", "T3_ddctl",
                "T4_stop", "n_T1_gate", "n_T3_ddctl", "n_T4_stop", "C1", "C2", "C3", "exact",
                "order"]].sort_values(["panel", "book", "cost", "window", "floor"])
          .to_string(index=False, float_format=FMT))
    print("\n  --- clause counts, ABS vs REL(0.10) ---")
    for w in WINDOWS:
        print(f"  window {w}")
        for pn in PANELS + ["ALL"]:
            line = f"    {pn:6s} "
            for lab, T in (("ABS", Ta), ("REL", Tr)):
                s = T[T.window == w] if pn == "ALL" else T[(T.window == w) & (T.panel == pn)]
                bits = " ".join(f"{cid} {int(s[cid].sum())}/{int(s[cid].notna().sum())}"
                                for cid, _, _ in CLAIMS)
                line += f"| {lab}: {bits} exact {int(s.exact.sum())}/{len(s)} "
            print(line)
    a_all = pd.concat([Ta[c] for c, _, _ in CLAIMS]).sum()
    r_all = pd.concat([Tr[c] for c, _, _ in CLAIMS]).sum()
    n = len(Ta) * 3
    print(f"\n  all 54 rows x 3 clauses: ABS {int(a_all)}/{n} true, REL(0.10) {int(r_all)}/{n}")
    key = ["panel", "book", "cost", "window"]
    m = Ta.merge(Tr, on=key, suffixes=("_abs", "_rel"))
    flips = 0
    print("\n  --- rows whose clause truth or tier ORDER changes under the floor ---")
    for _, r in m.iterrows():
        ch = [cid for cid, _, _ in CLAIMS
              if (r[f"{cid}_abs"] is not r[f"{cid}_rel"]) and
              not (pd.isna(r[f"{cid}_abs"]) and pd.isna(r[f"{cid}_rel"]))]
        if ch or r.order_abs != r.order_rel:
            flips += len(ch)
            print(f"    {r.panel:6s} {r.book:6s} @{r.cost:.0f}bps {r.window:4s}  "
                  f"clauses changed: {ch or '-':}  order {r.order_abs} -> {r.order_rel}")
    print(f"\n  R3: clause-truth flips = {flips}; "
          f"{'CONFIRMED' if flips >= 1 else 'REFUTED'} (bar was >= 1)")
    print("\n  --- median tier prices by panel (full window), ABS vs REL(0.10) ---")
    for lab, T in (("ABS", Ta), ("REL", Tr)):
        f = T[T.window == "full"]
        for pn in PANELS:
            s = f[f.panel == pn]
            print(f"    {lab} {pn:6s} T1 {s.T1_gate.median():7.3f}  T2 {s.T2_lever.median():7.3f}"
                  f"  T3 {s.T3_ddctl.median():7.3f}  T4 {s.T4_stop.median():7.3f}   "
                  f"arms priced: T1 {int(s.n_T1_gate.sum()):2d} T3 {int(s.n_T3_ddctl.sum()):2d} "
                  f"T4 {int(s.n_T4_stop.sum()):2d}")
    return flips


# ---------------------------------------------------------------- 4. walk-forward
def walk_forward(P, G, C):
    print("\n" + "=" * 200)
    print("4. RULE 8 WALK-FORWARD — the floor as a SELECTOR.  Eligibility computed on "
          "2009/2011-2016 only; 2017-2026 untouched.")
    print("   S1      = idea 94's selector: among arms with IS dMaxDD >= 1.0 pp and finite IS "
          "rate, argmin IS rate.")
    print("   Srel(p) = same argmin, eligibility replaced by the IS RELATIVE floor "
          "(IS dMaxDD >= p * |IS MaxDD_ctl|).")
    print("=" * 200)
    IS = P[P.window == "IS"].set_index(["panel", "book", "cost", "arm"])
    OO = P[P.window == "OOS"].set_index(["panel", "book", "cost", "arm"])
    gi = G.set_index(["panel", "book", "arm", "cost"])
    rows = []
    for pn in PANELS:
        for b in BOOKS:
            for c in COSTS:
                cell = IS.loc[(pn, b, c)]
                oos = OO.loc[(pn, b, c)]
                schemes = [("S1", cell[(cell.dMaxDD >= 1.0) & np.isfinite(cell.rate_raw)])]
                for phi in PHIS:
                    col = f"adm_{int(100*phi):02d}"
                    schemes.append((f"Srel{phi:.2f}", cell[cell[col] &
                                                           np.isfinite(cell.rate_raw)]))
                for nm, elig in schemes:
                    if not len(elig):
                        rows.append(dict(panel=pn, book=b, cost=c, scheme=nm, pick="(none)",
                                         n_elig=0))
                        continue
                    pick = elig.rate_raw.idxmin()
                    o = oos.loc[pick]
                    g = gi.loc[(pn, b, pick, c)]
                    ctl = gi.loc[(pn, b, "control", c)]
                    cand = oos[np.isfinite(oos.rate_raw) & (oos.dMaxDD > 0)]
                    best = cand.rate_raw.min() if len(cand) else np.nan
                    rows.append(dict(
                        panel=pn, book=b, cost=c, scheme=nm, pick=pick, n_elig=len(elig),
                        IS_rate=float(elig.rate_raw.min()),
                        IS_dMaxDD=float(elig.loc[pick].dMaxDD),
                        IS_dd_pct=float(elig.loc[pick].dd_pct_ctl),
                        OOS_rate=float(o.rate_raw), OOS_dMaxDD=float(o.dMaxDD),
                        regret=float(o.rate_raw - best) if np.isfinite(best) else np.nan,
                        OOS_CAGR=float(g.OOS_CAGR), OOS_Sharpe=float(g.OOS_Sharpe),
                        OOS_MaxDD=float(g.OOS_MaxDD),
                        ctl_OOS_CAGR=float(ctl.OOS_CAGR), ctl_OOS_Sharpe=float(ctl.OOS_Sharpe),
                        ctl_OOS_MaxDD=float(ctl.OOS_MaxDD),
                        p4a=bool(g.p4a), p4b=bool(g.p4b)))
    W = pd.DataFrame(rows)
    print(W.to_string(index=False, float_format=FMT))
    print("\n  --- selector summary (mean over the 18 cells) ---")
    base = W[W.scheme == "S1"].set_index(["panel", "book", "cost"])
    print(f"  {'scheme':10s} {'picks':>6s} {'chg vs S1':>10s} {'mean regret':>12s} "
          f"{'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} {'4a':>3s} {'4b':>3s}")
    summ = []
    for nm in ["S1"] + [f"Srel{p:.2f}" for p in PHIS]:
        s = W[W.scheme == nm]
        have = s[s.pick != "(none)"]
        chg = sum(1 for _, r in have.iterrows()
                  if base.loc[(r.panel, r.book, r.cost)].pick != r.pick)
        print(f"  {nm:10s} {len(have):6d} {chg:10d} {have.regret.mean():12.3f} "
              f"{have.OOS_CAGR.mean():9.3f} {have.OOS_Sharpe.mean():11.3f} "
              f"{have.OOS_MaxDD.mean():10.3f} {int(have.p4a.sum()):3d} {int(have.p4b.sum()):3d}")
        summ.append(dict(scheme=nm, picks=len(have), changed=chg,
                         mean_regret=have.regret.mean(), OOS_CAGR=have.OOS_CAGR.mean(),
                         OOS_Sharpe=have.OOS_Sharpe.mean(), OOS_MaxDD=have.OOS_MaxDD.mean()))
    ctl = W[W.scheme == "S1"]
    print(f"  {'control':10s} {len(ctl):6d} {'-':>10s} {'-':>12s} "
          f"{ctl.ctl_OOS_CAGR.mean():9.3f} {ctl.ctl_OOS_Sharpe.mean():11.3f} "
          f"{ctl.ctl_OOS_MaxDD.mean():10.3f}")
    for _, r in C.iterrows():
        print(f"  reference {r.panel:6s}: SPY OOS CAGR {r.spy_OOS_CAGR:.3f} Sharpe "
              f"{r.spy_OOS_Sharpe:.3f} MaxDD {r.spy_OOS_MaxDD:.3f} | RULES v1 OOS CAGR "
              f"{r.v1_OOS_CAGR:.3f} Sharpe {r.v1_OOS_Sharpe:.3f} MaxDD {r.v1_OOS_MaxDD:.3f}")
    s1 = W[(W.scheme == "S1") & (W.pick != "(none)")]
    sr = W[(W.scheme == f"Srel{PHI0:.2f}") & (W.pick != "(none)")]
    print(f"\n  R4: Srel(0.10) OOS Sharpe {sr.OOS_Sharpe.mean():.3f} vs S1 "
          f"{s1.OOS_Sharpe.mean():.3f} -> "
          f"{'CONFIRMED (no cost)' if sr.OOS_Sharpe.mean() >= s1.OOS_Sharpe.mean() - 1e-9 else 'REFUTED — the floor costs OOS Sharpe as a selector'}")
    return W, pd.DataFrame(summ)


# ---------------------------------------------------------------- main
def main():
    px_u56 = load_universe()
    ok_h = verify(px_u56)
    # RPF_REUSE=1 re-reads this run's OWN cached grid instead of recomputing it.  Debug
    # convenience only; the committed console was produced with it unset (full recompute).
    import os
    cg, cp, cc = (BT / f"{STEM}.grid.csv", BT / f"{STEM}.pricelist.csv",
                  BT / f"{STEM}.cells.csv")
    if os.environ.get("RPF_REUSE") == "1" and cg.exists() and cp.exists() and cc.exists():
        G, P, C = pd.read_csv(cg), pd.read_csv(cp), pd.read_csv(cc)
        print("  [RPF_REUSE=1] loaded cached grid — verification below still runs")
    else:
        G, P, C = build()
        G.to_csv(cg, index=False)
        P.to_csv(cp, index=False)
        C.to_csv(cc, index=False)
    ok_p = verify_pricelist(P)

    print("\n" + "=" * 200)
    print(f"FULL GRID — {len(G)} arm-points (3 panels x 3 books x 17 arms x 2 costs), ALL "
          f"reported.  4a/4b per PROTOCOL rule 4.")
    print("=" * 200)
    print(G[["panel", "book", "arm", "tier", "cost", "CAGR", "Sharpe", "MaxDD", "OOS_CAGR",
             "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "p4a", "p4b", "f4b"]]
          .to_string(index=False, float_format=FMT))

    F, n_neg, n_neg_rm = floor_table(P)
    S = stability_of_removed(P)
    Ta, Tr = tiers(P, use_rel=False), tiers(P, use_rel=True)
    flips = tier_report(Ta, Tr)
    W, summ = walk_forward(P, G, C)

    print("\n" + "=" * 200)
    print("PRE-REGISTERED PREDICTIONS")
    print("=" * 200)
    print(f"  R1 relative floor removes >=80% of negative published prices: "
          f"{n_neg_rm}/{n_neg} = {100.0*n_neg_rm/max(n_neg,1):.1f}% -> "
          f"{'CONFIRMED' if n_neg_rm >= 0.8*n_neg else 'REFUTED'}")
    kept, rem = S[S.kept], S[~S.kept]
    ka = float(kept.sign_agree.dropna().astype(float).mean())
    ra_ = float(rem.sign_agree.dropna().astype(float).mean())
    kg, rg = kept.abs_gap.median(), rem.abs_gap.median()
    print(f"  R2 removed rows less stable (sign {ra_:.3f} vs kept {ka:.3f}; gap {rg:.3f} vs "
          f"{kg:.3f}): {'CONFIRMED' if (ka > ra_ and kg < rg) else 'NOT CONFIRMED'}")
    print(f"  R3 tier statement changes: {flips} clause flips -> "
          f"{'CONFIRMED' if flips >= 1 else 'REFUTED'}")
    s1 = W[(W.scheme == "S1") & (W.pick != "(none)")]
    sr = W[(W.scheme == f"Srel{PHI0:.2f}") & (W.pick != "(none)")]
    print(f"  R4 floor is free as a selector: OOS Sharpe {sr.OOS_Sharpe.mean():.3f} vs "
          f"{s1.OOS_Sharpe.mean():.3f} -> "
          f"{'CONFIRMED' if sr.OOS_Sharpe.mean() >= s1.OOS_Sharpe.mean() - 1e-9 else 'REFUTED'}")
    n4b = int(G.p4b.sum())
    print(f"  R5 no new 4b pass: {n4b} arm-points pass 4b "
          f"({sorted(set(G[G.p4b].arm)) if n4b else 'none'}) -> "
          f"{'CONFIRMED' if n4b == 0 else 'see the list'}")
    print(f"  4a passes @10bps by panel: " + "; ".join(
        f"{pn}: {sorted(set(G[(G.cost==PCOST) & G.p4a & (G.panel==pn)].arm)) or 'none'}"
        for pn in PANELS))
    print(f"\n  harness verification: idea 94 {'OK' if ok_h else 'MISMATCH'}; "
          f"idea 97 pricelist {'OK' if ok_p else 'MISMATCH'}")

    P.to_csv(BT / f"{STEM}.pricelist.csv", index=False)
    F.to_csv(BT / f"{STEM}.floors.csv", index=False)
    S.to_csv(BT / f"{STEM}.stability.csv", index=False)
    pd.concat([Ta, Tr]).to_csv(BT / f"{STEM}.tiers.csv", index=False)
    W.to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    G.to_csv(BT / f"{STEM}.grid.csv", index=False)
    print(f"\nWrote {STEM}.{{grid,pricelist,floors,stability,tiers,walkforward}}.csv")


if __name__ == "__main__":
    main()

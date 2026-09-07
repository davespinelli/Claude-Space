#!/usr/bin/env python3
"""QUEUE idea 129 — is-the-sign-test-worth-anything-on-the-small-panel (cloud, 2026-09-07).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 122 showed the screen has ZERO out-of-sample discriminating power on u56/broad (OOS
denominator positive in 138/138 rows, admissible and rejected alike).  Idea 119's small panel
is where the sign actually moves, so run the identical IS-only screen there and ask the one
question that matters: does an IS-admissible small-panel denominator stay positive OOS more
often than a rejected one?  If not, the clause is cosmetic everywhere and PROTOCOL should say
so."

What is being tested.  Every drawdown "price" the project publishes has the form

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)     pp CAGR per pp MaxDD

Idea 122 proposed a REPORT-ONLY PROTOCOL clause: quote the ratio only if the denominator's
sign survives three nuisance perturbations (D1 cost rungs, D2 windows, D3 name-subsample
draws).  On the large-cap lists the clause could not be evaluated as a *predictor*, because
the OOS denominator was positive in 138 of 138 published rows -- there was nothing for the
screen to discriminate.  This run moves the identical screen to the panel where idea 119
showed the sign genuinely moves, and reads the one number that decides whether the clause is
a screen or a decoration:

    P(dMaxDD_OOS > 0 | IS-admissible)  -  P(dMaxDD_OOS > 0 | IS-rejected)

The screen is computed on 2009/2010-2016 DATA ONLY (IS cost axis on IS returns, IS-window
bootstrap draws).  The OOS window is never consulted by the screen.  D2 has no IS-only form
and is therefore not part of the predictor, exactly as in idea 122.

Tuned parameters (PROTOCOL rule 4).  TWO, both of the TEST and neither of any trading rule,
and both inherited unchanged from idea 122 so this run cannot pick its own bar:
    q    drop fraction in {0.05, 0.10, 0.20}
    tau  sign-agreement threshold in {0.80, 0.90, 0.95, 1.00}
All 12 grid points reported.  (q, tau) = (0.10, 0.90) is the pre-registered headline.
Books, arms, cost rungs, the IS/OOS split, NDRAW and the seed are idea 122's verbatim.

PANEL.  data/prices_small.csv.gz, the 439 names left after dropping the 44 tickers with
max_1d_move >= 1.0 in data/small_meta.csv (the convention of every small-panel run in this
record), SPY joined only as the benchmark and excluded from the book by construction of the
draw (it is one column of 440; the draws are uniform over columns, idea 119's convention,
and the books rank on the composite so SPY can be held -- stated, not hidden).

Pre-registered predictions (written before any number below was read)
    P1  The small panel is NOT degenerate: the OOS base rate P(dMaxDD_OOS > 0) is below 95%,
        unlike u56/broad's 100%.  If P1 fails the idea cannot be answered on this panel
        either and the correct report is "no panel in the record can evaluate the clause".
    P2  The screen is COSMETIC: the discrimination above is under +10 pp at the headline
        (q, tau), i.e. an IS-admissible denominator is not meaningfully more likely to stay
        positive OOS than a rejected one.
    P3  4a and 4b pass counts on the small panel are ~0, as in every prior small-panel run.
    P4  The IS-only screen changes few of idea 122's selector picks and its OOS Sharpe is
        within noise of the unscreened selector's.

Execution realism (PROTOCOL rule 2): inherited from idea 94's simulator -- weekly decision at
close t applied at t+1, long-only, no leverage, costs charged inside the loop so both state
machines see NET equity.  10 bps is the PROTOCOL point; 0/5/25 are the D1 nuisance rungs.

SURVIVORSHIP: data/prices_small.csv.gz is a CURRENT-CONSTITUENT screen of sub-$2B names (see
data/SMALL_PANEL_README.md).  Every absolute level below is optimistic, and a small-cap
current-constituent list is the most flattered panel in this record.  This run reports sign
stability and within-cell differences, which are far less exposed than levels -- but a
survivorship-free small panel could still move which rows pass.

Deterministic (seeded), standalone.  Imports idea 122's script (which imports idea 94's) and
research/baseline.py; modifies nothing.

    python research/backtests/2026-09-07_is-the-sign-test-worth-anything-on-the-small-panel_cloud.py
"""
import importlib.util
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest, metrics                                     # noqa: E402

BT = ROOT / "research" / "backtests"
_s122 = importlib.util.spec_from_file_location(
    "i122", BT / "2026-09-05_price-denominator-sign-test_C.py")
M = importlib.util.module_from_spec(_s122)
_s122.loader.exec_module(M)
H = M.H                                            # idea 94's harness, through idea 122

STEM = Path(__file__).stem
OUT = BT / STEM
PCOST = M.PCOST
COST_RUNGS, PUB_COSTS = M.COST_RUNGS, M.PUB_COSTS
IS_END, OOS_START = M.IS_END, M.OOS_START
BOOKS, ARMS = M.BOOKS, M.ARMS
NDRAW, DROP_FRACS, TAUS, SEED = M.NDRAW, M.DROP_FRACS, M.TAUS, M.SEED
Q_STAR, TAU_STAR, FLOOR = M.Q_STAR, M.TAU_STAR, M.FLOOR
UNAME = "prices_small(439)"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
fmt = M.fmt


def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def fisher_p(a, b, c, d):
    """Two-sided Fisher exact p for [[a,b],[c,d]] (small tables, exact, no scipy)."""
    n = a + b + c + d
    r1, r2, c1 = a + b, c + d, a + c
    def pr(x):
        return (math.comb(r1, x) * math.comb(r2, c1 - x) / math.comb(n, c1))
    lo, hi = max(0, c1 - r2), min(r1, c1)
    p0 = pr(a)
    return float(sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 * (1 + 1e-12)))


# ---------------------------------------------------------------- grid on this panel
def build_grid(px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    S = M.signals(px)

    worst_t = 0.0
    for b in BOOKS:
        for g in [None] + H.GATES:
            for conv in (("dg",) if g is None else ("dg", "rw")):
                a = M.targets_c(px, b, S, g, conv).fillna(0.0)
                e = H.targets(px, b, g, conv).fillna(0.0)
                worst_t = max(worst_t, float((a - e).abs().to_numpy().max()))
    print(f"    G1 cached targets vs idea 94 targets(): max|diff| {worst_t:.3e} "
          f"({'EXACT' if worst_t < 1e-15 else 'NOT EXACT — unsafe'})")
    assert worst_t < 1e-15

    W20 = M.targets_c(px, "TOP20", S)
    d_eng = float(np.abs(H.run(px, W20, bps=PCOST)["r"].loc[start:] -
                         backtest(px, W20, cost_bps=PCOST, freq=H.FREQ)["returns"].loc[start:]).max())
    print(f"    G2 H.run (all instruments off) vs engine.backtest @10 bps: max|diff| {d_eng:.3e}")
    assert d_eng < 1e-12

    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}
    v2_net = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}

    rets = {}
    t0 = time.time()
    for b in BOOKS:
        for name, kind, kwargs, (g, conv) in H.arm_specs():
            W = M.targets_c(px, b, S, g, conv)
            for c in COST_RUNGS:
                rets[(b, name, c)] = H.run(px, W, bps=c, **kwargs)["r"].loc[start:]
    print(f"    main grid: {len(rets)} runs in {time.time()-t0:.0f}s")

    rows = []
    for b in BOOKS:
        for c in PUB_COSTS:
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in ARMS:
                ra = rets[(b, name, c)]
                dc, dd, rate = M.dpair(rc, ra)
                rec = dict(uni=UNAME, book=b, cost=c, arm=name, kind=kind,
                           dCAGR=dc, dMaxDD=dd, rate=rate, published=bool(np.isfinite(rate)))
                for cc in COST_RUNGS:
                    _, dd_c, _ = M.dpair(rets[(b, "control", cc)], rets[(b, name, cc)])
                    rec[f"dMaxDD@{cc:.0f}"] = dd_c
                    _, dd_ci, _ = M.dpair(M.win(rets[(b, "control", cc)], "IS"),
                                          M.win(rets[(b, name, cc)], "IS"))
                    rec[f"dMaxDD_IS@{cc:.0f}"] = dd_ci
                for w in ("IS", "OOS"):
                    dcw, ddw, rw_ = M.dpair(M.win(rc, w), M.win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dcw, ddw, rw_
                ma_, mc_ = metrics(ra), metrics(rc)
                mg = H.margins(ra, bars)
                rec.update(CAGR=ma_["CAGR"], Sharpe=ma_["Sharpe"], MaxDD=ma_["MaxDD"],
                           ctl_MaxDD=mc_["MaxDD"], ctl_CAGR=mc_["CAGR"],
                           p4a_v1=H.pass4a(ra, v1_net[c]), p4a=H.pass4a(ra, v2_net[c]),
                           p4b=all(v > 0 for v in mg.values()),
                           f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-")
                rows.append(rec)
    G = pd.DataFrame(rows)
    G["D1_pass"] = np.all([G[f"dMaxDD@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    G["D2_pass"] = (G.dMaxDD_IS > 0) & (G.dMaxDD_OOS > 0)
    G["D1_pass_IS_only"] = np.all([G[f"dMaxDD_IS@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    return px, start, S, spy, bars, v1_net, v2_net, rets, G


_PX, _START = None, None


def _init(px, start):
    global _PX, _START
    _PX, _START = px, start


def _draw_job(job):
    """One bootstrap draw.  Pure function of (q, draw index, kept columns) and the panel, so
    the parallel schedule cannot change a number; the draws themselves are pre-generated from
    idea 122's single seeded rng in the same order as its serial loop."""
    q, d, keep = job
    sub, start = _PX.iloc[:, keep], _START
    Ss = M.signals(sub)
    rows = []
    for b in BOOKS:
        rc = H.run(sub, M.targets_c(sub, b, Ss), bps=PCOST)["r"].loc[start:]
        for name, kind, kwargs, (g, conv) in ARMS:
            ra = H.run(sub, M.targets_c(sub, b, Ss, g, conv), bps=PCOST, **kwargs)["r"].loc[start:]
            rec = dict(uni=UNAME, q=q, draw=d, book=b, arm=name)
            for w in ("full", "IS", "OOS"):
                dc, dd, rt = M.dpair(M.win(rc, w), M.win(ra, w))
                rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dc, dd, rt
            rows.append(rec)
    return rows


def bootstrap(px, start, nproc=4):
    """Idea 122's D3, verbatim: NDRAW seeded name-subsample draws per q, signals recomputed on
    each sub-panel so the book is genuinely re-formed.  The draw sets come off ONE
    np.random.default_rng(SEED) in idea 122's order; only their evaluation is parallel."""
    import multiprocessing as mp
    rng = np.random.default_rng(SEED)
    ncol = px.shape[1]
    jobs = []
    for q in DROP_FRACS:
        k = int(round(ncol * (1 - q)))
        for d in range(NDRAW):
            jobs.append((q, d, sorted(rng.choice(ncol, size=k, replace=False))))
    out, t0, done = [], time.time(), 0
    with mp.Pool(nproc, initializer=_init, initargs=(px, start)) as pool:
        for rows in pool.imap_unordered(_draw_job, jobs, chunksize=1):
            out.extend(rows); done += 1
            if done % 10 == 0:
                print(f"    {done}/{len(jobs)} draws ({time.time()-t0:.0f}s)", flush=True)
    return pd.DataFrame(out).sort_values(["q", "draw", "book", "arm"]).reset_index(drop=True)


# ---------------------------------------------------------------- walk-forward
def walk_forward(G, D3, rets, v1_net, v2_net, spy):
    out = []
    for (b, c), cell in G.groupby(["book", "cost"]):
        ctl_o = metrics(rets[(b, "control", c)].loc[OOS_START:])
        v1_o, v2_o = metrics(v1_net[c].loc[OOS_START:]), metrics(v2_net[c].loc[OOS_START:])
        spy_o = metrics(spy.loc[OOS_START:])
        base = cell[(cell.dMaxDD_IS >= 1.0) & np.isfinite(cell.rate_IS)]
        for q in DROP_FRACS:
            for tau in TAUS:
                d3 = D3[(D3.q == q) & (D3.book == b)].set_index("arm").frac_pos_IS
                for sel, sub in (("S1", base),
                                 ("S2", base[base.arm.map(lambda a: d3.get(a, 0.0) >= tau)
                                             & base.D1_pass_IS_only])):
                    if sel == "S1" and (q, tau) != (DROP_FRACS[0], TAUS[0]):
                        continue
                    rec = dict(book=b, cost=c, q=q, tau=tau, selector=sel,
                               ctl_OOS_CAGR=ctl_o["CAGR"], ctl_OOS_Sharpe=ctl_o["Sharpe"],
                               ctl_OOS_MaxDD=ctl_o["MaxDD"],
                               v1_OOS_Sharpe=v1_o["Sharpe"], v2_OOS_Sharpe=v2_o["Sharpe"],
                               v2_OOS_CAGR=v2_o["CAGR"], v2_OOS_MaxDD=v2_o["MaxDD"],
                               spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                               spy_OOS_MaxDD=spy_o["MaxDD"], n_eligible=len(sub))
                    if sub.empty:
                        rec.update(pick="NOTHING ADMISSIBLE", IS_rate=np.nan, OOS_rate=np.nan,
                                   OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                   OOS_dMaxDD_pos=np.nan, p4a=False, p4b=False)
                    else:
                        pk = sub.sort_values("rate_IS").iloc[0]
                        mo = metrics(rets[(b, pk.arm, c)].loc[OOS_START:])
                        rec.update(pick=pk.arm, IS_rate=pk.rate_IS, OOS_rate=pk.rate_OOS,
                                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                   OOS_MaxDD=mo["MaxDD"], OOS_dMaxDD_pos=bool(pk.dMaxDD_OOS > 0),
                                   p4a=bool(pk.p4a), p4b=bool(pk.p4b))
                    out.append(rec)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    print(__doc__.split("Deterministic")[0])
    print("=" * 200)
    print(f"PRE-REGISTERED (idea 122's settings, unchanged): D1 costs {COST_RUNGS} bps | "
          f"D2 windows IS/OOS | D3 {NDRAW} draws x q in {DROP_FRACS} (seed {SEED}), "
          f"tau in {TAUS}; headline (q,tau) = ({Q_STAR}, {TAU_STAR})")
    print("=" * 200)

    # ---------------------------------------------------------- [0] the premise, re-read
    print("\n[0] PREMISE GATE — idea 122's committed .signtest.csv, re-read before anything new")
    P = pd.read_csv(BT / "2026-09-05_price-denominator-sign-test_C.signtest.csv")
    pub122 = P[P.published]
    print(f"    rows {len(P)}, published rates {len(pub122)}, admissible "
          f"{int(pub122.ADMISSIBLE.sum())} ({pub122.ADMISSIBLE.mean():.1%})")
    print(f"    OOS denominator positive on u56/broad: "
          f"{int((pub122.dMaxDD_OOS > 0).sum())}/{len(pub122)} "
          f"({(pub122.dMaxDD_OOS > 0).mean():.1%})  <- the degeneracy this run is testing against")
    assert len(pub122) == 138 and int(pub122.ADMISSIBLE.sum()) == 90
    assert int((pub122.dMaxDD_OOS > 0).sum()) == 138
    d3_122 = P.D1_pass_IS_only & (P.D3_frac_IS >= TAU_STAR)
    for lab, sel in (("IS-admissible", d3_122), ("IS-rejected", ~d3_122)):
        s = P[sel & P.published]
        print(f"      u56/broad {lab:>14}: n {len(s):>3}  P(dMaxDD_OOS>0) "
              f"{(s.dMaxDD_OOS > 0).mean():.4f}")

    gcsv, bcsv = f"{OUT}.signtest.csv", f"{OUT}.bootstrap.csv"
    if RESUME and Path(gcsv).exists() and Path(bcsv).exists():
        G, B = pd.read_csv(gcsv), pd.read_csv(bcsv)
        px = small_panel(); start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        S = M.signals(px)
        v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
                  for c in PUB_COSTS}
        v2_net = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
                  for c in PUB_COSTS}
        rets = {}
        for b in BOOKS:
            for name, kind, kwargs, (g, conv) in H.arm_specs():
                W = M.targets_c(px, b, S, g, conv)
                for c in COST_RUNGS:
                    rets[(b, name, c)] = H.run(px, W, bps=c, **kwargs)["r"].loc[start:]
        analyse(G, B, rets, v1_net, v2_net, spy, px, start)
        return

    print(f"\n[1] PANEL {UNAME}")
    px = small_panel()
    px, start, S, spy, bars, v1_net, v2_net, rets, G = build_grid(px)
    ms = metrics(spy)
    print(f"    {px.shape[1]-1} names + SPY, {px.index[0].date()} -> {px.index[-1].date()} | "
          f"eval from {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"    SPY {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
          f"{bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f}")
    mv2 = metrics(v2_net[10.0]); mv1 = metrics(v1_net[10.0])
    print(f"    RULES v2 (live) on this panel @10 bps {mv2['CAGR']:.2%}/{mv2['Sharpe']:.3f}/"
          f"{mv2['MaxDD']:.2%} | RULES v1 {mv1['CAGR']:.2%}/{mv1['Sharpe']:.3f}/{mv1['MaxDD']:.2%}")

    print(f"\n[2] D3 BOOTSTRAP — {len(DROP_FRACS)} x {NDRAW} draws x {len(BOOKS)} books x "
          f"{len(ARMS)} arms (+control) on a {px.shape[1]}-column panel", flush=True)
    B = bootstrap(px, start)
    G.to_csv(gcsv, index=False); B.to_csv(bcsv, index=False)
    analyse(G, B, rets, v1_net, v2_net, spy, px, start)


def analyse(G, B, rets, v1_net, v2_net, spy, px, start):
    D3 = M.d3_table(B)
    d3s = D3[D3.q == Q_STAR].set_index(["book", "arm"])
    G["D3_frac_full"] = [d3s.frac_pos_full.get((b, a), np.nan) for b, a in zip(G.book, G.arm)]
    G["D3_frac_IS"] = [d3s.frac_pos_IS.get((b, a), np.nan) for b, a in zip(G.book, G.arm)]
    G["D3_frac_OOS"] = [d3s.frac_pos_OOS.get((b, a), np.nan) for b, a in zip(G.book, G.arm)]
    G["D3_pass"] = G.D3_frac_full >= TAU_STAR
    G["ADMISSIBLE"] = G.D1_pass & G.D2_pass & G.D3_pass
    pub = G[G.published].copy()

    print("\n" + "=" * 200)
    print(f"[3] THE SMALL-PANEL PRICE LIST UNDER THE IDENTICAL SIGN TEST — {len(G)} rows, "
          f"{len(pub)} carry a published rate (dMaxDD > {FLOOR} pp).")
    print(fmt(G[["book", "cost", "arm", "dCAGR", "dMaxDD", "rate", "published",
                 "dMaxDD@0", "dMaxDD@10", "dMaxDD@25", "D1_pass", "dMaxDD_IS", "dMaxDD_OOS",
                 "D2_pass", "D3_frac_full", "D3_pass", "ADMISSIBLE", "p4a", "p4b"]]))
    surv = pd.DataFrame([dict(axis=nm, n_pub=len(pub), n_pass=int(pub[col].sum()),
                              frac=float(pub[col].mean()) if len(pub) else np.nan)
                         for nm, col in (("D1 cost {0,5,10,25} bps", "D1_pass"),
                                         ("D2 window IS and OOS", "D2_pass"),
                                         (f"D3 panel q={Q_STAR} tau={TAU_STAR}", "D3_pass"),
                                         ("ALL THREE (admissible)", "ADMISSIBLE"))])
    print("\n--- SURVIVAL of the published rates ---")
    print(fmt(surv))
    print("\n--- how often is the denominator positive at all, on this panel? ---")
    for w, col in (("full", "dMaxDD"), ("IS", "dMaxDD_IS"), ("OOS", "dMaxDD_OOS")):
        print(f"      all {len(G)} rows, {w:>4}: positive {int((G[col] > 0).sum()):>3}/{len(G)} "
              f"({(G[col] > 0).mean():.1%})   | published rows: "
              f"{int((pub[col] > 0).sum()):>3}/{len(pub)} ({(pub[col] > 0).mean():.1%})")

    # ---------------------------------------------------------- [4] THE QUESTION
    print("\n" + "=" * 200)
    print("[4] THE ONE QUESTION — does an IS-admissible small-panel denominator stay positive")
    print("    OUT OF SAMPLE more often than a rejected one?  Screen = D1 on IS returns (all")
    print("    four rungs) AND D3 on IS-window draws.  The OOS window is never consulted.")
    ver = []
    for q in DROP_FRACS:
        dd_is = D3[D3.q == q].set_index(["book", "arm"]).frac_pos_IS
        f_is = np.array([dd_is.get((b, a), np.nan) for b, a in zip(G.book, G.arm)])
        for tau in TAUS:
            scr = (G.D1_pass_IS_only & (f_is >= tau)).values
            row = dict(q=q, tau=tau)
            for lab, sel in (("adm", scr), ("rej", ~scr)):
                s = G[sel & G.published.values]
                row[f"n_{lab}"] = len(s)
                row[f"pos_{lab}"] = float((s.dMaxDD_OOS > 0).mean()) if len(s) else np.nan
                row[f"priceable_{lab}"] = float(np.isfinite(s.rate_OOS).mean()) if len(s) else np.nan
                row[f"medrate_{lab}"] = float(s.rate_OOS.median()) if len(s) else np.nan
            a = int((G[scr & G.published.values].dMaxDD_OOS > 0).sum())
            b_ = int((G[scr & G.published.values].dMaxDD_OOS <= 0).sum())
            c_ = int((G[~scr & G.published.values].dMaxDD_OOS > 0).sum())
            d_ = int((G[~scr & G.published.values].dMaxDD_OOS <= 0).sum())
            row["discrimination_pp"] = 100.0 * (row["pos_adm"] - row["pos_rej"]) \
                if (row["n_adm"] and row["n_rej"]) else np.nan
            row["fisher_p"] = fisher_p(a, b_, c_, d_) if (a + b_) and (c_ + d_) else np.nan
            row.update(a=a, b=b_, c=c_, d=d_)
            ver.append(row)
    V = pd.DataFrame(ver)
    print(fmt(V[["q", "tau", "n_adm", "pos_adm", "n_rej", "pos_rej", "discrimination_pp",
                 "fisher_p", "priceable_adm", "priceable_rej", "medrate_adm", "medrate_rej"]]))
    hv = V[(V.q == Q_STAR) & (V.tau == TAU_STAR)].iloc[0]
    print(f"\n    HEADLINE (q={Q_STAR}, tau={TAU_STAR}): P(OOS sign positive | IS-admissible) "
          f"{hv.pos_adm:.4f} (n {int(hv.n_adm)}) vs | IS-rejected {hv.pos_rej:.4f} "
          f"(n {int(hv.n_rej)})  ->  discrimination {hv.discrimination_pp:+.1f} pp, "
          f"Fisher p {hv.fisher_p:.3f}")
    fin = V.dropna(subset=["discrimination_pp"])
    print(f"    across all {len(fin)} of 12 evaluable grid points: discrimination mean "
          f"{fin.discrimination_pp.mean():+.1f} pp, min {fin.discrimination_pp.min():+.1f}, "
          f"max {fin.discrimination_pp.max():+.1f}, positive {int((fin.discrimination_pp>0).sum())}"
          f"/{len(fin)}, any with Fisher p < 0.05: {int((fin.fisher_p < 0.05).sum())}")
    V.to_csv(f"{OUT}.discrim.csv", index=False)

    # ---------------------------------------------------------- [4b] the answerable version
    print("\n" + "=" * 200)
    print("[4b] THE SAME TEST ON ALL 96 ROWS, not just the 63 that carry a published rate.")
    print("     The published subset is selected on a FULL-SAMPLE denominator, so it may be")
    print("     pre-conditioned; the unrestricted population is the one the screen could still")
    print("     discriminate in.  Not a KEEP path, a diagnostic.")
    ver2 = []
    for q in DROP_FRACS:
        dd_is = D3[D3.q == q].set_index(["book", "arm"]).frac_pos_IS
        f_is = np.array([dd_is.get((b, a), np.nan) for b, a in zip(G.book, G.arm)])
        for tau in TAUS:
            scr = (G.D1_pass_IS_only & (f_is >= tau)).values
            a = int((G[scr].dMaxDD_OOS > 0).sum()); b_ = int((G[scr].dMaxDD_OOS <= 0).sum())
            c_ = int((G[~scr].dMaxDD_OOS > 0).sum()); d_ = int((G[~scr].dMaxDD_OOS <= 0).sum())
            pa = a / (a + b_) if a + b_ else np.nan
            pr_ = c_ / (c_ + d_) if c_ + d_ else np.nan
            ver2.append(dict(q=q, tau=tau, n_adm=a + b_, pos_adm=pa, n_rej=c_ + d_, pos_rej=pr_,
                             discrimination_pp=100 * (pa - pr_),
                             fisher_p=fisher_p(a, b_, c_, d_) if (a + b_) and (c_ + d_) else np.nan))
    V2 = pd.DataFrame(ver2)
    print(fmt(V2))
    h2 = V2[(V2.q == Q_STAR) & (V2.tau == TAU_STAR)].iloc[0]
    print(f"     HEADLINE on all rows: {h2.pos_adm:.4f} (n {int(h2.n_adm)}) vs {h2.pos_rej:.4f} "
          f"(n {int(h2.n_rej)}) -> {h2.discrimination_pp:+.1f} pp, Fisher p {h2.fisher_p:.4f}; "
          f"across 12 points mean {V2.discrimination_pp.mean():+.1f} pp, "
          f"p<0.05 in {int((V2.fisher_p < 0.05).sum())}/12")
    V2.to_csv(f"{OUT}.discrim_allrows.csv", index=False)

    # ---------------------------------------------------------- [4c] why it cannot discriminate
    print("\n[4c] MECHANISM — why the published subset is degenerate on BOTH panel families.")
    print("     If the full-sample MaxDD of both legs is attained inside the OOS window, the")
    print("     PUBLISHED denominator IS the OOS denominator, and a screen fitted on the IS")
    print("     window is predicting a number it partly cannot see.")
    def trough(r):
        eq = (1 + r).cumprod()
        return (eq / eq.cummax() - 1).idxmin()
    tr = []
    for b in BOOKS:
        for name, kind, _, _ in [("control", "ctl", None, None)] + [(a[0], a[1], None, None) for a in ARMS]:
            r = rets[(b, name, 10.0)]
            t = trough(r)
            tr.append(dict(book=b, arm=name, trough=str(t.date()), in_OOS=bool(t >= pd.Timestamp(OOS_START))))
    TR = pd.DataFrame(tr)
    print(f"     full-sample MaxDD trough falls in the OOS window for "
          f"{int(TR.in_OOS.sum())}/{len(TR)} book-arm legs @10 bps "
          f"(controls: {int(TR[TR.arm=='control'].in_OOS.sum())}/{len(TR[TR.arm=='control'])})")
    print("     trough dates by book: " + " | ".join(
        f"{b}: " + ", ".join(sorted(set(TR[TR.book == b].trough))) for b in BOOKS))
    print(f"     corr(dMaxDD_full, dMaxDD_OOS) = {G.dMaxDD.corr(G.dMaxDD_OOS):+.4f}   "
          f"corr(dMaxDD_full, dMaxDD_IS) = {G.dMaxDD.corr(G.dMaxDD_IS):+.4f}")
    print(f"     sign(full) == sign(OOS) in {int((np.sign(G.dMaxDD)==np.sign(G.dMaxDD_OOS)).sum())}"
          f"/{len(G)} rows; sign(full) == sign(IS) in "
          f"{int((np.sign(G.dMaxDD)==np.sign(G.dMaxDD_IS)).sum())}/{len(G)}")
    unp = G[~G.published]
    print(f"     the {len(unp)} rows the absolute floor (dMaxDD_full > {FLOOR} pp) already "
          f"excludes: OOS-positive {int((unp.dMaxDD_OOS > 0).sum())}/{len(unp)}, i.e. the FLOOR, "
          f"not the sign test, is what removes the negative-OOS rows.")
    TR.to_csv(f"{OUT}.troughs.csv", index=False)

    # ---------------------------------------------------------- [5] the (q,tau) grid
    print("\n" + "=" * 200)
    print("[5] ALL 12 GRID POINTS — admissibility counts (full-sample screen, idea 122's table C)")
    gp = []
    for q in DROP_FRACS:
        dd = D3[D3.q == q].set_index(["book", "arm"]).frac_pos_full
        f = np.array([dd.get((b, a), np.nan) for b, a in zip(G.book, G.arm)])
        for tau in TAUS:
            ok = (G.D1_pass & G.D2_pass & (f >= tau)).values
            gp.append(dict(q=q, tau=tau, n_rows=len(G), admissible_rows=int(ok.sum()),
                           n_published=int(G.published.sum()),
                           admissible_published=int((ok & G.published.values).sum()),
                           frac_published=float((ok & G.published.values).sum() /
                                                max(int(G.published.sum()), 1))))
    GP = pd.DataFrame(gp)
    print(fmt(GP))
    GP.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------- [6] rule 8 walk-forward
    print("\n" + "=" * 200)
    print("[6] RULE 8 WALK-FORWARD — screen computed on IS only; 2017-2026 untouched.")
    Wf = walk_forward(G, D3, rets, v1_net, v2_net, spy)
    print(fmt(Wf[["book", "cost", "selector", "q", "tau", "n_eligible", "pick", "IS_rate",
                  "OOS_rate", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "ctl_OOS_Sharpe",
                  "v2_OOS_Sharpe", "spy_OOS_Sharpe", "p4a", "p4b"]]))
    s1 = Wf[Wf.selector == "S1"]
    print(f"\n    S1 (idea 94's selector, no screen): {len(s1)} cells, mean OOS Sharpe "
          f"{s1.OOS_Sharpe.mean():.4f}, picks {sorted(set(s1.pick))}")
    ch = []
    for q in DROP_FRACS:
        for tau in TAUS:
            s2 = Wf[(Wf.selector == "S2") & (Wf.q == q) & (Wf.tau == tau)]
            nn = int((s2.pick == "NOTHING ADMISSIBLE").sum())
            mg = s1.set_index(["book", "cost"]).pick
            diff = sum(1 for _, r in s2.iterrows() if r.pick != mg.get((r.book, r.cost)))
            ch.append(dict(q=q, tau=tau, changed=diff, n_cells=len(s2), nothing=nn,
                           mean_OOS_Sharpe=s2.OOS_Sharpe.mean()))
            print(f"    S2 q={q:.2f} tau={tau:.2f}: mean OOS Sharpe {s2.OOS_Sharpe.mean():.4f} "
                  f"over {len(s2)-nn} cells with a pick, {nn} NOTHING ADMISSIBLE, "
                  f"changes {diff}/{len(s2)} of S1's picks, picks "
                  f"{sorted(set(s2[s2.pick != 'NOTHING ADMISSIBLE'].pick))}")
    CH = pd.DataFrame(ch)
    Wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    CH.to_csv(f"{OUT}.selector.csv", index=False)

    # ---------------------------------------------------------- [7] KEEP paths
    print("\n" + "=" * 200)
    print("[7] PROTOCOL rule 4, BOTH KEEP PATHS — every arm-point @10/25 bps on this panel")
    k = G[G.cost.isin(PUB_COSTS)]
    print(f"    4a (vs RULES v2, live): {int(k.p4a.sum())} of {len(k)}   "
          f"4a (vs RULES v1, continuity): {int(k.p4a_v1.sum())} of {len(k)}   "
          f"4b: {int(k.p4b.sum())} of {len(k)}")
    fails = k[~k.p4b].f4b.str.split(",").explode()
    print(f"    binding 4b bars: " + "  ".join(f"{a} {b}" for a, b in fails.value_counts().items()))
    if k.p4b.any():
        print(fmt(k[k.p4b][["book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "ADMISSIBLE", "rate"]]))

    # ---------------------------------------------------------- [8] scorecard
    print("\n" + "=" * 200)
    print("[8] PREDICTION SCORECARD")
    base_oos = float((G[G.published].dMaxDD_OOS > 0).mean())
    print(f"  P1 small panel NOT degenerate (OOS base rate < 95%): {base_oos:.1%} "
          f"({'CONFIRMED' if base_oos < 0.95 else 'REFUTED'})  [u56/broad was 100.0%]")
    print(f"  P2 screen is cosmetic (headline discrimination < +10 pp): "
          f"{hv.discrimination_pp:+.1f} pp "
          f"({'CONFIRMED' if hv.discrimination_pp < 10 else 'REFUTED'})")
    print(f"  P3 4a/4b ~ 0 on the small panel: 4a {int(k.p4a.sum())}/{len(k)}, "
          f"4b {int(k.p4b.sum())}/{len(k)} "
          f"({'CONFIRMED' if (k.p4a.sum() + k.p4b.sum()) == 0 else 'REFUTED'})")
    hd = CH[(CH.q == Q_STAR) & (CH.tau == TAU_STAR)].iloc[0]
    print(f"  P4 screen changes few picks and OOS Sharpe is within noise: changed "
          f"{int(hd.changed)}/{int(hd.n_cells)}, S2 {hd.mean_OOS_Sharpe:.4f} vs S1 "
          f"{s1.OOS_Sharpe.mean():.4f} (d {hd.mean_OOS_Sharpe - s1.OOS_Sharpe.mean():+.4f})")
    G.to_csv(f"{OUT}.signtest.csv", index=False)
    D3.to_csv(f"{OUT}.d3.csv", index=False)
    print(f"\n    wrote {Path(OUT).name}.signtest.csv / .bootstrap.csv / .d3.csv / "
          f".discrim.csv / .grid.csv / .walkforward.csv / .selector.csv")


if __name__ == "__main__":
    main()

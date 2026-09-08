#!/usr/bin/env python3
"""Idea 461 — does-the-width-convergence-hold-past-n=40 (lane C, 2026-09-08).

PRE-REGISTERED QUESTION (QUEUE 461): idea 239 (lane B) found that a ranked book's EXCESS
over its own un-ranked EW_ALL control is a WIDTH function — mean OOS excess -0.289 / -0.220
/ -0.161 / -0.131 at n = 5 / 10 / 20 / 40 — monotone in n and still NEGATIVE at the grid
edge.  Push n past 40 and report (i) the n, if any, at which the excess reaches ZERO, and
(ii) WHAT IS LEFT OF THE BOOK THERE.

TWO TUNED PARAMETERS ONLY:
    p1 = n, the ranked book's width        {5, 10, 20, 40, 60, 90, 120, 180}
    p2 = GROSS CONVENTION                  {FIXED, NORM}
Everything else is FIXED and pre-registered before any number was read.  Panels are a
pre-registered LIST (B136 and SMALL439, which QUEUE 461 names, plus U56 so the published
n=5..40 ladder can be reproduced on all three of idea 239's named panels), not a dial.

WHY THE SECOND DIAL IS A DIAL AND NOT A CHOICE (this is the whole methodological point).
The record's ranked book is built FIXED: every selected name gets GROSS/n, so when fewer
than n names are eligible the shortfall sits in CASH and the REALISED gross falls as n
rises.  On a 136-name panel, n=180 cannot hold 180 names, so a FIXED book at n=180 is a
DE-GROSSED book, not a wide one.  QUEUE 240 / the 2026-09-08 cloud run
("how-many-published-count-dials-are-gross-dials") showed this channel is real, undisclosed
in 62 of 127 committed count-sweep files, and worth up to 38% of a published width premium.
Reading "excess reaches zero at large n" off a FIXED ladder alone would therefore be
uninterpretable: the excess could go to zero because the book stopped ranking (the claim) or
because the book stopped investing (an artefact).  So BOTH conventions are run and ALL grid
points are reported:
    FIXED : w_i = GROSS / n           for each selected name  (the record's construction)
    NORM  : w_i = GROSS / n_held(t)   for each selected name  (realised gross pinned at
            GROSS whenever >= 1 name is eligible — QUEUE 461's "at pinned gross")
REALISED GROSS is published beside every single arm, per the cloud run's proposal.

DEFINITIONS (identical to idea 239 lane B so the ladders are comparable)
    EW_ALL   : every name PRICED that day at GROSS/N_priced.  No gate, no ranking.  This is
               the control; its realised gross is GROSS by construction, so it is the same
               book under both conventions and is run once.
    RANKED(n): the record's composite (12-1 + 6m + 3m rank-average, NO vol scaling), gated
               by the plain 200d MA and vol20 < 0.60, top n by composite.
    EXCESS   := Sharpe(RANKED(n)) - Sharpe(EW_ALL) on the SAME panel, rung and cadence.
    "reaches zero" := EXCESS >= 0 (the queue's bar).
    TRIVIAL  := the point at which RANKED(n) IS the control by construction.  Because the
               ranked book is GATED and the control is not, the two never coincide exactly;
               what converges is the ranked book's holding onto the gated subset.  So the
               run also publishes OVERLAP := sum_i min(w_ranked_i, w_ctrl_i) / GROSS, the
               fraction of the control's book the ranked book actually holds, so that
               "convergence" is MEASURED rather than asserted.

FIXED: gross G = 0.75 on every arm; cadence weekly; gate = plain 200d MA (no hysteresis);
vol cap 0.60; de-gross convention `dg` (gated-out weight to CASH at 0, never re-spread);
cost rungs {0, 10, 25} bps derived EXACTLY from one 0-bps run per arm
(net(c) = gross - turn*c/1e4); 10 bps is the verdict rung (PROTOCOL 2); next-day execution
(weights decided at close t, applied t+1).

SURVIVORSHIP: SMALL439 is the current constituents of the sub-$2B screen
(data/SMALL_PANEL_README.md); B136 is the current constituents of universe_broad.json
(PROTOCOL 9).  Every panel-level reading here is RELATIVE, never achievable.

PARTS
 A  THE LADDER: 3 panels x 8 widths x 2 conventions x 3 rungs, every point reported, with
    realised gross, mean names held, mean names ELIGIBLE, turnover and OVERLAP beside each.
 B  THE ANSWER: the smallest n at which excess >= 0, per (panel, convention, rung, window),
    and what the book looks like there.
 C  RULE 8 WALK-FORWARD (PROTOCOL 8): n chosen on 2009-2016 IS Sharpe ONLY, per (panel,
    convention, rung); 2017-2026 read once, against the do-nothing EW_ALL control, RULES v2
    and SPY.
 D  BOTH KEEP PATHS (4a vs RULES v2 on the same panel; 4b vs SPY incl. the OOS clause) on
    EVERY grid point.

Outputs (all committed):
    .grid.csv         Part A: every (panel, n, conv, rung) point
    .zero.csv         Part B: the smallest-n-with-nonnegative-excess table
    .walkforward.csv  Part C
    .console.txt      full stdout
"""
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics                                          # noqa: E402

OUT = Path(__file__).with_suffix("")

RUNGS = [0, 10, 25]
VERDICT_RUNG = 10
NS = [5, 10, 20, 40, 60, 90, 120, 180]      # p1 — published grid {5,10,20,40} + QUEUE 461's
CONVS = ["FIXED", "NORM"]                   # p2
GROSS = 0.75
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"


# ------------------------------------------------------------------ machinery (idea 239's)
def week_mask(idx):
    per = idx.to_period("W")
    s = pd.Series(per, index=idx)
    return (s != s.shift(-1)).values


def simulate(px, W, mask):
    """Weights decided at t, applied at t+1; drift between rebalances (== engine.backtest)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    cur = np.zeros(px.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(len(px))
    for i in range(len(px)):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))


def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    f = []
    if not s["H1"] > b["H1"]: f.append("H1")
    if not s["H2"] > b["H2"]: f.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: f.append("DD")
    return ",".join(f)


def bars_4b(s, spy, oos_s, oos_spy):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not oos_s > oos_spy: f.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGR")
    return ",".join(f)


# ------------------------------------------------------------------ the two book forms
def ew_weights(px):
    """EW_ALL: every priced name at GROSS/N_priced."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_weights(comp, above, vol20, n, conv):
    """Top-n by composite among gated + vol-capped names.

    FIXED : GROSS/n per selected name (record construction; realised gross falls when
            fewer than n names are eligible).
    NORM  : GROSS/n_held per selected name (realised gross pinned at GROSS).
    """
    elig = comp.where(above & (vol20 < MAX_VOL))
    sel = (elig.rank(axis=1, ascending=False) <= n).astype(float)
    if conv == "FIXED":
        return sel * (GROSS / n)
    k = sel.sum(axis=1).replace(0, np.nan)
    return GROSS * sel.div(k, axis=0).fillna(0.0)


def overlap(Wr, Wc, rb):
    """sum_i min(w_ranked, w_ctrl) / GROSS, averaged over REBALANCE days only (the days the
    weights are actually the book).  1.0 == the ranked book holds the whole control book."""
    A = Wr.values[rb]
    B = Wc.values[rb]
    ov = np.minimum(A, B).sum(axis=1) / GROSS
    return float(np.nanmean(ov[np.isfinite(ov)]))


# ------------------------------------------------------------------ panels
def build_panels():
    u56 = load_universe()
    b136 = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv", index_col=0)
    sm = load_universe(small=True)
    keep = [c for c in sm.columns if c == "SPY" or meta.max_1d_move.get(c, 0) < 1.0]
    return [("U56", u56), ("B136", b136), ("SMALL439", sm[keep])]


def run():
    t0 = time.time()
    grid, wf, ident = [], [], []
    for pname, px in build_panels():
        n_names = px.shape[1] - 1                      # SPY is a benchmark, not a constituent
        s_ns, above, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above.astype(float))
        mask = week_mask(px.index)
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r)
        spy_oos = metrics(spy_r.loc[OOS_START:])

        v2g, v2t, _ = simulate(px, rules_v2_weights(px), mask)
        v1g, v1t, _ = simulate(px, rules_v1_weights(px), mask)
        base = {c: stats(net(v2g, v2t, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(v2g, v2t, c).loc[OOS_START:]) for c in RUNGS}

        # GATE: the fast path must reproduce engine.backtest exactly on every panel
        eng = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        ident.append(dict(panel=pname,
                          max_abs_diff=float(np.abs(eng - net(v1g, v1t, 10).loc[start:]).max())))

        # how many names are ELIGIBLE on a typical day — the ceiling the FIXED book runs into
        elig_ct = (above & (vol20 < MAX_VOL)).loc[start:].sum(axis=1)
        mean_elig = float(elig_ct.mean())

        # ---- control (same book under both conventions, run once)
        Wc = ew_weights(px)
        cg, ct_, ch = simulate(px, Wc, mask)
        cg, ct_, ch = cg.loc[start:], ct_.loc[start:], ch.loc[start:]

        # rebalance-day mask restricted to the post-warm-up sample (aligned to px.index[260:])
        rb = mask[260:]
        Wc_s = Wc.iloc[260:]
        arms = {}
        for conv in CONVS:
            for n in NS:
                Wn = ranked_weights(comp, above, vol20, n, conv)
                g, t, h = simulate(px, Wn, mask)
                Wn_s = Wn.iloc[260:]
                held_ct = float((Wn_s > 0).sum(axis=1).values[rb].mean())
                arms[(conv, n)] = (g.loc[start:], t.loc[start:], h.loc[start:], held_ct,
                                   overlap(Wn_s, Wc_s, rb))

        def read(g, t, c):
            r = net(g, t, c)
            return (r, stats(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:]))

        for c in RUNGS:
            rc, stc, isc, ooc = read(cg, ct_, c)
            grid.append(dict(panel=pname, n_names=n_names, arm="CTRL", conv="-", n=np.nan,
                             bps=c, real_gross=float(ch.mean()), mean_held=float(n_names),
                             mean_elig=mean_elig, overlap=1.0,
                             turn_yr=float(ct_.sum() / (len(cg) / 252)), **stc,
                             IS_Sharpe=isc["Sharpe"], OOS_Sharpe=ooc["Sharpe"],
                             OOS_CAGR=ooc["CAGR"], OOS_MaxDD=ooc["MaxDD"],
                             ctrl_Sharpe=stc["Sharpe"], ctrl_OOS_Sharpe=ooc["Sharpe"],
                             excess=0.0, excess_H1=0.0, excess_H2=0.0, excess_OOS=0.0,
                             fail4a=bars_4a(stc, base[c]),
                             fail4b=bars_4b(stc, spy_s, ooc["Sharpe"], spy_oos["Sharpe"])))
            for conv in CONVS:
                for n in NS:
                    g, t, h, held_ct, ov = arms[(conv, n)]
                    r, st, iss, oo = read(g, t, c)
                    grid.append(dict(panel=pname, n_names=n_names, arm="RANKED", conv=conv, n=n,
                                     bps=c, real_gross=float(h.mean()), mean_held=held_ct,
                                     mean_elig=mean_elig, overlap=ov,
                                     turn_yr=float(t.sum() / (len(g) / 252)), **st,
                                     IS_Sharpe=iss["Sharpe"], OOS_Sharpe=oo["Sharpe"],
                                     OOS_CAGR=oo["CAGR"], OOS_MaxDD=oo["MaxDD"],
                                     ctrl_Sharpe=stc["Sharpe"], ctrl_OOS_Sharpe=ooc["Sharpe"],
                                     excess=st["Sharpe"] - stc["Sharpe"],
                                     excess_H1=st["H1"] - stc["H1"],
                                     excess_H2=st["H2"] - stc["H2"],
                                     excess_OOS=oo["Sharpe"] - ooc["Sharpe"],
                                     fail4a=bars_4a(st, base[c]),
                                     fail4b=bars_4b(st, spy_s, oo["Sharpe"], spy_oos["Sharpe"])))

            # ---- Part C: rule 8. n chosen on 2009-2016 IS Sharpe only, per convention.
            for conv in CONVS:
                iss_by_n = {}
                for n in NS:
                    g, t, h, _, _ = arms[(conv, n)]
                    iss_by_n[n] = metrics(net(g, t, c).loc[:IS_END])["Sharpe"]
                pick = max(iss_by_n, key=iss_by_n.get)
                g, t, h, held_ct, ov = arms[(conv, pick)]
                r, st, iss, oo = read(g, t, c)
                wf.append(dict(panel=pname, conv=conv, bps=c, pick_n=pick,
                               IS_Sharpe=iss_by_n[pick],
                               IS_ctrl=isc["Sharpe"],
                               OOS_Sharpe=oo["Sharpe"], OOS_CAGR=oo["CAGR"],
                               OOS_MaxDD=oo["MaxDD"], real_gross=float(h.mean()), overlap=ov,
                               OOS_ctrl_Sharpe=ooc["Sharpe"], OOS_ctrl_CAGR=ooc["CAGR"],
                               OOS_ctrl_MaxDD=ooc["MaxDD"],
                               OOS_v2_Sharpe=base_oos[c]["Sharpe"],
                               OOS_v2_CAGR=base_oos[c]["CAGR"], OOS_v2_MaxDD=base_oos[c]["MaxDD"],
                               OOS_SPY_Sharpe=spy_oos["Sharpe"], OOS_SPY_CAGR=spy_oos["CAGR"],
                               OOS_SPY_MaxDD=spy_oos["MaxDD"],
                               beats_ctrl=oo["Sharpe"] > ooc["Sharpe"],
                               beats_v2=oo["Sharpe"] > base_oos[c]["Sharpe"],
                               beats_spy=oo["Sharpe"] > spy_oos["Sharpe"],
                               fail4a=bars_4a(st, base[c]),
                               fail4b=bars_4b(st, spy_s, oo["Sharpe"], spy_oos["Sharpe"])))
        print(f"  {pname}: {n_names} names, mean eligible/day {mean_elig:.1f}, "
              f"ctrl@10bps Sharpe {grid[-1]['ctrl_Sharpe']:.4f}  [{time.time()-t0:.0f}s]")

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf)
    I = pd.DataFrame(ident)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    print("\n=== GATE: fast path vs engine.backtest (RULES v1, 10 bps) ===")
    print(I.to_string(index=False, float_format=lambda x: f"{x:.2e}"))

    # ---------------------------------------------------------------- Part A: the ladder
    print("\n=== PART A — THE WIDTH LADDER, verdict rung 10 bps, all points ===")
    for pname in G.panel.unique():
        sub = G[(G.panel == pname) & (G.bps == VERDICT_RUNG)]
        print(f"\n-- {pname} (n_names={int(sub.n_names.iloc[0])}, "
              f"mean eligible/day {sub.mean_elig.iloc[0]:.1f}) --")
        cols = ["arm", "conv", "n", "real_gross", "mean_held", "overlap", "turn_yr",
                "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                "excess", "excess_H1", "excess_H2", "excess_OOS", "fail4a", "fail4b"]
        print(sub[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== PART A2 — the published ladder reproduced, mean OOS excess by n ===")
    print("(idea 239 lane B published -0.289 / -0.220 / -0.161 / -0.131 at n=5/10/20/40 over")
    print(" 23 panels vs EW_ALL @10bps; here: 3 named panels, both conventions)")
    lad = (G[(G.arm == "RANKED") & (G.bps == VERDICT_RUNG)]
           .groupby(["conv", "n"])[["excess", "excess_OOS", "real_gross", "overlap"]].mean())
    print(lad.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- Part B: the answer
    print("\n=== PART B — THE ANSWER: smallest n with EXCESS >= 0 ===")
    zrows = []
    R = G[G.arm == "RANKED"]
    for (pname, conv, c), sub in R.groupby(["panel", "conv", "bps"]):
        sub = sub.sort_values("n")
        for win, col in [("FULL", "excess"), ("H1", "excess_H1"), ("H2", "excess_H2"),
                         ("OOS", "excess_OOS")]:
            ok = sub[sub[col] >= 0]
            hit = int(ok.n.iloc[0]) if len(ok) else -1
            row = dict(panel=pname, conv=conv, bps=c, window=win,
                       zero_at_n=hit, n_grid_max=max(NS),
                       excess_at_nmax=float(sub[col].iloc[-1]),
                       monotone=bool((sub[col].diff().dropna() >= -1e-12).all()))
            if hit > 0:
                h = sub[sub.n == hit].iloc[0]
                row.update(real_gross=float(h.real_gross), mean_held=float(h.mean_held),
                           overlap=float(h.overlap), turn_yr=float(h.turn_yr),
                           CAGR=float(h.CAGR), Sharpe=float(h.Sharpe), MaxDD=float(h.MaxDD))
            zrows.append(row)
    Z = pd.DataFrame(zrows)
    Z.to_csv(f"{OUT}.zero.csv", index=False)
    print(Z.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n-- verdict rung only (10 bps) --")
    print(Z[Z.bps == VERDICT_RUNG].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    nz = Z[Z.bps == VERDICT_RUNG]
    print(f"\nreaches zero in {int((nz.zero_at_n > 0).sum())} of {len(nz)} "
          f"(panel x conv x window) cells at 10 bps; "
          f"FIXED {int((nz[nz.conv=='FIXED'].zero_at_n > 0).sum())}/{len(nz[nz.conv=='FIXED'])}, "
          f"NORM {int((nz[nz.conv=='NORM'].zero_at_n > 0).sum())}/{len(nz[nz.conv=='NORM'])}")

    # ---------------------------------------------------------------- Part C: rule 8
    print("\n=== PART C — RULE 8 WALK-FORWARD (n chosen on 2009-2016 IS Sharpe only) ===")
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nchooser beats its own do-nothing control OOS: {int(W.beats_ctrl.sum())}/{len(W)}; "
          f"beats RULES v2 OOS: {int(W.beats_v2.sum())}/{len(W)}; "
          f"beats SPY OOS: {int(W.beats_spy.sum())}/{len(W)}")

    # ---------------------------------------------------------------- Part D: KEEP paths
    print("\n=== PART D — BOTH KEEP PATHS over all grid points ===")
    tot = len(G)
    p4a = G[G.fail4a == ""]
    p4b = G[G.fail4b == ""]
    print(f"4a: {len(p4a)}/{tot}   4b: {len(p4b)}/{tot}")
    for lbl, P in [("4a", p4a), ("4b", p4b)]:
        if len(P):
            print(f"\n-- {lbl} passers --")
            print(P[["panel", "arm", "conv", "n", "bps", "real_gross", "overlap", "CAGR",
                     "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "excess"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n4b by rung: " + ", ".join(
        f"{c}bps {len(p4b[p4b.bps==c])}/{len(G[G.bps==c])}" for c in RUNGS))
    wf4b = W[W.fail4b == ""]
    print(f"rule-8-SELECTABLE 4b passers: {len(wf4b)}/{len(W)}")
    print(f"\n[{time.time()-t0:.0f}s]")
    return G, W, Z


if __name__ == "__main__":
    run()

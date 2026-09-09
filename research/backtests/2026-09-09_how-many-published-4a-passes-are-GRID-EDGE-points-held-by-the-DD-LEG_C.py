#!/usr/bin/env python3
"""Idea 500 — how many published 4a passes are GRID-EDGE points held by the DD LEG?

Idea 270R's only 4a passer (SMALL439, band=0.05) clears PROTOCOL 4a not because it is the
best arm on its own sweep but because the two arms ABOVE it (band 0.08, 0.12) have HIGHER
Sharpe in both halves and breach the MaxDD leg, on a Sharpe curve monotone out to the
widest value the grid tested.  If that shape is common, a 4a pass is partly a statement
about where the author stopped sweeping, not about the arm.

This run censuses the record's reconstructible 4a passes for exactly that shape, on the
two parameters the queue allows: DIAL x PANEL (cost rung reported as a second reading of
the same books, not a third tuned parameter).

Pre-registered definitions, fixed before any number was read:
  4a          (PROTOCOL 4a, against the LIVE RULES v2 book at the arm's own cost rung):
              H1 Sharpe > base H1 AND H2 Sharpe > base H2 AND full MaxDD >= base MaxDD.
  dominator   another arm on the SAME sweep with strictly higher Sharpe in BOTH halves.
  DD_HELD     the passer has >= 1 dominator and EVERY dominator fails 4a on the MaxDD leg
              ALONE (its Sharpe legs both clear).  i.e. the passer wins only because the
              better arms are disqualified by drawdown.
  EDGE        the sweep's Sharpe-leg argmax (binding half = min(H1,H2)) sits at a grid
              ENDPOINT and the passer is not that endpoint.
  MONOTONE    min(H1,H2) moves monotonically from the passer to that endpoint.
  GRID_EDGE_DD_HELD = DD_HELD and EDGE and MONOTONE  (idea 270R's shape).
  OPEN vs STRUCTURAL endpoint: an endpoint is STRUCTURAL when the instrument cannot be
              widened (gross 1.00 = no leverage, PROTOCOL 2; volcap 9.99 / quantile 1.00 =
              no filter; cadence D and Q = the engine's fastest and slowest schedules).
              Only an OPEN endpoint can be an artefact of where the sweep stopped, so
              every OPEN-edge sweep is RE-RUN with the grid EXTENDED past it.

Rule 8 (PROTOCOL 8) is run separately from the halves: dial value chosen on 2009-2016
only, 2017-2026 read once, against RULES v2, RULES v1, SPY and the EWALL do-nothing
control on the same OOS window.  Both KEEP paths (4a and 4b) evaluated for every arm.

Costs 10 bps headline and 25 bps rung; weekly cadence except on the cadence dial; weights
at t applied at t+1 (engine).  No network.  ALL grid points are written to .arms.csv.
SURVIVORSHIP: B136 is current constituents of universe_broad.json; SMALL439 is the sub-$2B
screen with the 44 tickers whose max_1d_move >= 1.0 dropped first.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_how-many-published-4a-passes-are-GRID-EDGE-points-held-by-the-DD-LEG_C"
OUT = ROOT / "research" / "backtests"
GROSS, BAND = 0.75, 0.03
COSTS = [10, 25]
OOS_START = "2017-01-01"          # PROTOCOL 8: params on 2009-2016, 2017-2026 untouched

_console: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ---------------------------------------------------------------- book forms (lifted verbatim from idea 270R)
def _ew(px, mask, gross):
    e = mask.astype(float).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def w_topn(px, n, gross=GROSS):
    s, above, _ = score(px)
    r = s.where(above).rank(axis=1, ascending=False)
    return _ew(px, r <= n, gross)

def w_band(px, band, gross=GROSS):   return rules_v2_weights(px, band=band, gross=gross)
def w_gross(px, gross, band=BAND):   return rules_v2_weights(px, band=band, gross=gross)

def w_volcap(px, cap, gross=GROSS):
    _, above, vol20 = score(px)
    return _ew(px, above & (vol20 < cap), gross)

def w_quantile(px, x, gross=GROSS):
    s, above, _ = score(px)
    r = s.where(above).rank(axis=1, ascending=False, pct=True)
    return _ew(px, r <= x, gross)

def w_ewall(px, gross=GROSS):        return _ew(px, px.notna(), gross)

# published grid  |  extension past each OPEN endpoint  |  which endpoints are STRUCTURAL
DIALS = {
    "n":        dict(fn=w_topn,     pub=[5, 10, 20, 30, 50],                 ext=[3, 75, 100, 150],
                     freq="W", struct=set()),
    "band":     dict(fn=w_band,     pub=[0.00, 0.01, 0.03, 0.05, 0.08, 0.12], ext=[0.16, 0.20, 0.25, 0.35],
                     freq="W", struct={0.00}),
    "gross":    dict(fn=w_gross,    pub=[0.25, 0.50, 0.75, 1.00],            ext=[0.10],
                     freq="W", struct={1.00}),
    "volcap":   dict(fn=w_volcap,   pub=[0.30, 0.45, 0.60, 0.90, 9.99],      ext=[0.20, 0.25],
                     freq="W", struct={9.99}),
    "quantile": dict(fn=w_quantile, pub=[0.10, 0.25, 0.50, 0.75, 1.00],      ext=[0.02, 0.05],
                     freq="W", struct={1.00}),
    "cadence":  dict(fn=None,       pub=["D", "W", "M", "Q"],                ext=[],
                     freq=None, struct={"D", "Q"}),
}

def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]

# ---------------------------------------------------------------- metric helpers
def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]

def trio(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]

def split_r8(r):
    """PROTOCOL 8 split: params on 2009-2016, 2017-2026 untouched."""
    m = r.index < pd.Timestamp(OOS_START)
    return r[m], r[~m]

def stats(r):
    """Every number a leg can need, from one return series."""
    h1, h2 = halves(r)
    c, s, d = trio(r); c1, s1, d1 = trio(h1); c2, s2, d2 = trio(h2)
    return dict(FULL_CAGR=c, FULL_Sharpe=s, FULL_MaxDD=d, H1_Sharpe=s1, H2_Sharpe=s2,
                H1_CAGR=c1, H2_CAGR=c2, H1_MaxDD=d1, H2_MaxDD=d2)

def costed(gross_ret, turnover, bps):
    """Exact equivalent of engine.backtest(..., cost_bps=bps); gated against it below."""
    return gross_ret - turnover * bps / 1e4

def run_book(px, w, freq, start):
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return res["returns"].loc[start:], res["turnover"].loc[start:]

# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say(f"# {STAMP}\n")
    say("Pre-registered: 4a vs LIVE RULES v2 at the arm's own rung; DD_HELD = every "
        "Sharpe-dominator fails on the MaxDD leg alone; EDGE = Sharpe argmax at a grid "
        "endpoint the passer does not occupy; OPEN endpoints are re-swept EXTENDED.\n")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    # ---------- reproduction gates, before any new number is read
    pxu = panels["U56"]; start_u = pxu.index[260]
    g, tv = run_book(pxu, rules_v2_weights(pxu), "W", start_u)
    live = stats(costed(g, tv, 10))
    say("## Reproduction gates")
    say(f"RULES v2 on U56 @10bps: CAGR {live['FULL_CAGR']:.2%} Sharpe {live['FULL_Sharpe']:.4f} "
        f"MaxDD {live['FULL_MaxDD']:.2%} halves {live['H1_Sharpe']:.4f}/{live['H2_Sharpe']:.4f}"
        "   (published 8.66% / 1.2056 / -12.05% / 1.2259 / 1.1908)")
    direct = backtest(pxu, rules_v2_weights(pxu), cost_bps=10.0, freq="W")["returns"].loc[start_u:]
    gate_cost = float(np.abs(direct.values - costed(g, tv, 10).values).max())
    say(f"cost-decomposition gate |derived - engine(cost_bps=10)| max = {gate_cost:.3e}")
    assert gate_cost < 1e-12, "cost decomposition is not exact"

    pxs = panels["SMALL439"]; start_s = pxs.index[260]
    gs, ts = run_book(pxs, w_band(pxs, 0.05), "W", start_s)
    p270 = stats(costed(gs, ts, 10))
    say(f"idea 270R SMALL439 band=0.05 @10bps: CAGR {p270['FULL_CAGR']:.2%} "
        f"Sharpe {p270['FULL_Sharpe']:.4f} MaxDD {p270['FULL_MaxDD']:.2%} "
        f"halves {p270['H1_Sharpe']:.4f}/{p270['H2_Sharpe']:.4f}"
        "   (published 4.18% / 0.6183 / -14.6% / 0.6385 / 0.6031)\n")

    # ---------- the grid
    arm_rows, wf_rows = [], []
    for pname, px in panels.items():
        start = px.index[260]
        nnames = px.shape[1] - 1
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        say(f"## Panel {pname}: {nnames} names + SPY, {px.index[0].date()}..{px.index[-1].date()}")

        bg, bt = run_book(px, rules_v2_weights(px), "W", start)
        v1g, v1t = run_book(px, rules_v1_weights(px), "W", start)
        cg, ct = run_book(px, w_ewall(px), "W", start)

        for dname, D in DIALS.items():
            for v in list(D["pub"]) + list(D["ext"]):
                if dname == "n" and v > nnames:      # cannot rank more names than the panel has
                    continue
                if dname == "cadence":
                    w, freq = rules_v2_weights(px, band=BAND, gross=GROSS), v
                else:
                    w, freq = D["fn"](px, v), D["freq"]
                gr, tu = run_book(px, w, freq, start)
                for cost in COSTS:
                    r = costed(gr, tu, cost)
                    row = dict(panel=pname, dial=dname, arm=v, cost=cost,
                               published=int(v in D["pub"]),
                               structural_end=int(v in D["struct"]),
                               turnover_yr=float(tu.sum() / (len(tu) / 252)))
                    row.update(stats(r))
                    is_r, oos_r = split_r8(r)
                    ic, isx, idd = trio(is_r); oc, osx, odd = trio(oos_r)
                    row.update(R8_IS_CAGR=ic, R8_IS_Sharpe=isx, R8_IS_MaxDD=idd,
                               R8_OOS_CAGR=oc, R8_OOS_Sharpe=osx, R8_OOS_MaxDD=odd)
                    arm_rows.append(row)

        # comparands, per cost rung, on both the halves split and the rule-8 split
        for cost in COSTS:
            for nm, (gg, tt) in {"RULES v2 (live)": (bg, bt), "RULES v1": (v1g, v1t),
                                 "EWALL control": (cg, ct)}.items():
                r = costed(gg, tt, cost)
                row = dict(panel=pname, dial="_comparand", arm=nm, cost=cost, published=0,
                           structural_end=0, turnover_yr=float(tt.sum() / (len(tt) / 252)))
                row.update(stats(r))
                is_r, oos_r = split_r8(r)
                ic, isx, idd = trio(is_r); oc, osx, odd = trio(oos_r)
                row.update(R8_IS_CAGR=ic, R8_IS_Sharpe=isx, R8_IS_MaxDD=idd,
                           R8_OOS_CAGR=oc, R8_OOS_Sharpe=osx, R8_OOS_MaxDD=odd)
                arm_rows.append(row)
            row = dict(panel=pname, dial="_comparand", arm="SPY", cost=cost, published=0,
                       structural_end=0, turnover_yr=0.0)
            row.update(stats(spy_r))
            is_r, oos_r = split_r8(spy_r)
            ic, isx, idd = trio(is_r); oc, osx, odd = trio(oos_r)
            row.update(R8_IS_CAGR=ic, R8_IS_Sharpe=isx, R8_IS_MaxDD=idd,
                       R8_OOS_CAGR=oc, R8_OOS_Sharpe=osx, R8_OOS_MaxDD=odd)
            arm_rows.append(row)

    A = pd.DataFrame(arm_rows)

    # ---------- KEEP paths for every arm
    def cmp_of(panel, cost, who):
        m = A[(A.panel == panel) & (A.dial == "_comparand") & (A.arm == who) & (A.cost == cost)]
        return m.iloc[0]

    p4a, p4b = [], []
    for _, a in A.iterrows():
        if a.dial == "_comparand":
            p4a.append(np.nan); p4b.append(np.nan); continue
        b = cmp_of(a.panel, a.cost, "RULES v2 (live)"); s = cmp_of(a.panel, a.cost, "SPY")
        p4a.append(int(a.H1_Sharpe > b.H1_Sharpe and a.H2_Sharpe > b.H2_Sharpe
                       and a.FULL_MaxDD >= b.FULL_MaxDD))
        p4b.append(int(a.H1_Sharpe > s.H1_Sharpe and a.H2_Sharpe > s.H2_Sharpe
                       and a.R8_OOS_Sharpe > s.R8_OOS_Sharpe
                       and a.FULL_MaxDD >= 0.6 * s.FULL_MaxDD
                       and a.FULL_CAGR >= 0.7 * s.FULL_CAGR))
    A["pass4a"], A["pass4b"] = p4a, p4b
    A.to_csv(OUT / f"{STAMP}.arms.csv", index=False)

    # ---------- the census: classify every 4a pass on the PUBLISHED grid
    def classify(sub, i, b):
        """sub = one sweep (published arms only), ordered along the dial; i = passer index."""
        a = sub.iloc[i]
        dom = sub[(sub.H1_Sharpe > a.H1_Sharpe) & (sub.H2_Sharpe > a.H2_Sharpe)]
        if len(dom) == 0:
            dd_held, why = 0, "no Sharpe-dominator (arm is on the Sharpe frontier)"
        else:
            dd_only = ((dom.H1_Sharpe > b.H1_Sharpe) & (dom.H2_Sharpe > b.H2_Sharpe)
                       & (dom.FULL_MaxDD < b.FULL_MaxDD))
            dd_held = int(bool(dd_only.all()))
            why = (f"{len(dom)} dominator(s), {int(dd_only.sum())} fail on the DD leg alone")
        bind = sub[["H1_Sharpe", "H2_Sharpe"]].min(axis=1).values
        k = int(np.argmax(bind))
        edge = int(k in (0, len(sub) - 1) and k != i)
        lo, hi = (i, k) if k > i else (k, i)
        seg = bind[lo:hi + 1]
        mono = int(len(seg) < 2 or bool(np.all(np.diff(seg) >= 0) or np.all(np.diff(seg) <= 0)))
        endpoint_arm = sub.arm.iloc[k] if edge else None
        struct = int(bool(sub.structural_end.iloc[k])) if edge else 0
        return dd_held, edge, mono, why, endpoint_arm, struct, len(dom)

    cen = []
    for (pname, dname, cost), sub_all in A[A.dial != "_comparand"].groupby(["panel", "dial", "cost"], sort=False):
        pub = sub_all[sub_all.published == 1].reset_index(drop=True)
        b = cmp_of(pname, cost, "RULES v2 (live)")
        for i in range(len(pub)):
            if not pub.pass4a.iloc[i]:
                continue
            dd_held, edge, mono, why, ep, struct, ndom = classify(pub, i, b)
            cen.append(dict(panel=pname, dial=dname, cost=cost, arm=pub.arm.iloc[i],
                            n_dominators=ndom, DD_HELD=dd_held, EDGE=edge, MONOTONE=mono,
                            GRID_EDGE_DD_HELD=int(dd_held and edge and mono),
                            sharpe_argmax_arm=ep, argmax_endpoint_structural=struct,
                            H1=pub.H1_Sharpe.iloc[i], H2=pub.H2_Sharpe.iloc[i],
                            MaxDD=pub.FULL_MaxDD.iloc[i], CAGR=pub.FULL_CAGR.iloc[i],
                            base_H1=b.H1_Sharpe, base_H2=b.H2_Sharpe, base_MaxDD=b.FULL_MaxDD,
                            note=why))
    C = pd.DataFrame(cen)
    C.to_csv(OUT / f"{STAMP}.census.csv", index=False)

    say("## (1) CENSUS of 4a passes on the PUBLISHED grids "
        f"({int((A[A.dial!='_comparand'].published==1).sum())} published arm-rows, "
        f"{len(A[A.dial!='_comparand'])} arm-rows in all)")
    if len(C) == 0:
        say("no 4a passes on the published grids")
    else:
        say(f"4a passes: {len(C)}   DD_HELD {int(C.DD_HELD.sum())}   EDGE {int(C.EDGE.sum())}   "
            f"MONOTONE {int(C.MONOTONE.sum())}   GRID_EDGE_DD_HELD {int(C.GRID_EDGE_DD_HELD.sum())}")
        say(f"of the EDGE passes, {int(C[C.EDGE==1].argmax_endpoint_structural.sum())} have a "
            "STRUCTURAL endpoint (cannot be widened) and the rest an OPEN one")
        say(C[["panel", "dial", "cost", "arm", "n_dominators", "DD_HELD", "EDGE", "MONOTONE",
               "GRID_EDGE_DD_HELD", "sharpe_argmax_arm", "argmax_endpoint_structural",
               "H1", "H2", "MaxDD"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say("\nby dial: " + C.groupby("dial").GRID_EDGE_DD_HELD.agg(["size", "sum"]).to_string())
        say("by panel: " + C.groupby("panel").GRID_EDGE_DD_HELD.agg(["size", "sum"]).to_string())
    say("")

    # ---------- (1b) how much work does the DD leg do across the WHOLE corpus?
    ar0 = A[A.dial != "_comparand"].copy()
    bH1 = ar0.apply(lambda a: cmp_of(a.panel, a.cost, "RULES v2 (live)").H1_Sharpe, axis=1)
    bH2 = ar0.apply(lambda a: cmp_of(a.panel, a.cost, "RULES v2 (live)").H2_Sharpe, axis=1)
    bDD = ar0.apply(lambda a: cmp_of(a.panel, a.cost, "RULES v2 (live)").FULL_MaxDD, axis=1)
    ar0["sharpe_ok"] = (ar0.H1_Sharpe > bH1) & (ar0.H2_Sharpe > bH2)
    ar0["dd_ok"] = ar0.FULL_MaxDD >= bDD
    ar0.to_csv(OUT / f"{STAMP}.legs.csv", index=False)
    for lab, sub in (("published", ar0[ar0.published == 1]), ("all incl. extensions", ar0)):
        n = len(sub); so = int(sub.sharpe_ok.sum()); cut = int((sub.sharpe_ok & ~sub.dd_ok).sum())
        say(f"(1b) DD-leg workload [{lab}]: {n} arm-rows, both Sharpe legs clear the live book in "
            f"{so} ({so/n:.1%}); of those the MaxDD leg CUTS {cut} ({cut/max(so,1):.1%}) and admits "
            f"{so-cut}. DD-only failures are {cut/n:.1%} of the corpus.")
    say("")
    say("(1c) the dominators behind each 4a pass (the arms the DD leg disqualifies):")
    for _, c in C.iterrows():
        sub = ar0[(ar0.panel == c.panel) & (ar0.dial == c.dial) & (ar0.cost == c.cost)
                  & (ar0.published == 1)]
        dom = sub[(sub.H1_Sharpe > c.H1) & (sub.H2_Sharpe > c.H2)]
        say(f"  {c.panel}/{c.dial}@{c.cost}bps passer arm={c.arm}: H1 {c.H1:.4f} H2 {c.H2:.4f} "
            f"MaxDD {c.MaxDD:.2%} (base {c.base_H1:.4f}/{c.base_H2:.4f}/{c.base_MaxDD:.2%})")
        for _, d in dom.iterrows():
            say(f"     dominator arm={d.arm}: H1 {d.H1_Sharpe:.4f} H2 {d.H2_Sharpe:.4f} "
                f"MaxDD {d.FULL_MaxDD:.2%}  sharpe_ok={bool(d.sharpe_ok)} dd_ok={bool(d.dd_ok)}")
        ext = ar0[(ar0.panel == c.panel) & (ar0.dial == c.dial) & (ar0.cost == c.cost)]
        ext = ext.sort_values("arm", key=lambda s: s.astype(float))
        say("     full EXTENDED sweep (arm, H1, H2, MaxDD, 4a): "
            + "; ".join(f"{r.arm:g} {r.H1_Sharpe:.4f}/{r.H2_Sharpe:.4f}/{r.FULL_MaxDD:.1%}/{int(r.pass4a)}"
                        for _, r in ext.iterrows()))
    say("")

    # ---------- (2) the extension test: does the pass survive a wider grid?
    ext_rows = []
    for (pname, dname, cost), sub_all in A[A.dial != "_comparand"].groupby(["panel", "dial", "cost"], sort=False):
        if len(sub_all[sub_all.published == 0]) == 0:
            continue
        b = cmp_of(pname, cost, "RULES v2 (live)")
        pub = sub_all[sub_all.published == 1].reset_index(drop=True)
        full = sub_all.sort_values("arm", key=lambda s: s.astype(float)).reset_index(drop=True)
        for i in range(len(pub)):
            if not pub.pass4a.iloc[i]:
                continue
            j = int(np.where(full.arm.values == pub.arm.iloc[i])[0][0])
            _, e0, m0, _, _, _, nd0 = classify(pub, i, b)
            _, e1, m1, _, _, _, nd1 = classify(full, j, b)
            dh1 = classify(full, j, b)[0]
            ext_rows.append(dict(panel=pname, dial=dname, cost=cost, arm=pub.arm.iloc[i],
                                 n_pub=len(pub), n_ext=len(full),
                                 pass4a_pub=1, pass4a_ext=int(full.pass4a.iloc[j]),
                                 dom_pub=nd0, dom_ext=nd1, EDGE_pub=e0, EDGE_ext=e1,
                                 DD_HELD_ext=dh1,
                                 new_4a_in_ext=int(full[(full.published == 0)].pass4a.sum())))
    E = pd.DataFrame(ext_rows)
    E.to_csv(OUT / f"{STAMP}.extension.csv", index=False)
    say("## (2) EXTENSION test — the same sweeps re-run past every OPEN endpoint")
    if len(E) == 0:
        say("no extendable sweep carried a 4a pass")
    else:
        say(E.to_string(index=False))
        say(f"\n4a passes that survive the wider grid: {int(E.pass4a_ext.sum())} / {len(E)}; "
            f"Sharpe-dominators added by the extension: {int((E.dom_ext - E.dom_pub).sum())} "
            f"(median {float((E.dom_ext - E.dom_pub).median()):+.1f} per passer)")
    ne = A[(A.dial != "_comparand") & (A.published == 0)]
    say(f"extension arms: {len(ne)} rows, 4a {int(ne.pass4a.sum())}, 4b {int(ne.pass4b.sum())}\n")

    # ---------- (3) rule 8
    say("## (3) RULE 8 walk-forward — dial chosen on 2009-2016 by IS Sharpe, 2017-2026 read once")
    for cost in COSTS:
        for pname in panels:
            base = cmp_of(pname, cost, "RULES v2 (live)"); spy = cmp_of(pname, cost, "SPY")
            v1 = cmp_of(pname, cost, "RULES v1"); ew = cmp_of(pname, cost, "EWALL control")
            for dname in DIALS:
                for scope, sel in (("pub", A[(A.panel == pname) & (A.dial == dname) & (A.cost == cost) & (A.published == 1)]),
                                   ("ext", A[(A.panel == pname) & (A.dial == dname) & (A.cost == cost)])):
                    if len(sel) == 0:
                        continue
                    sel = sel.reset_index(drop=True)
                    k = int(sel.R8_IS_Sharpe.values.argmax())
                    # the 4a chooser: among arms whose 4a legs clear IN-SAMPLE ONLY, best IS Sharpe
                    is4a = sel[(sel.R8_IS_Sharpe > base.R8_IS_Sharpe) & (sel.R8_IS_MaxDD >= base.R8_IS_MaxDD)]
                    k4 = int(is4a.R8_IS_Sharpe.values.argmax()) if len(is4a) else -1
                    wf_rows.append(dict(panel=pname, cost=cost, dial=dname, scope=scope, n_arms=len(sel),
                                        pick=sel.arm.iloc[k], OOS_Sharpe=sel.R8_OOS_Sharpe.iloc[k],
                                        OOS_CAGR=sel.R8_OOS_CAGR.iloc[k], OOS_MaxDD=sel.R8_OOS_MaxDD.iloc[k],
                                        n_is4a=len(is4a),
                                        pick4a=(is4a.arm.iloc[k4] if k4 >= 0 else None),
                                        OOS_Sharpe_4a=(is4a.R8_OOS_Sharpe.iloc[k4] if k4 >= 0 else np.nan),
                                        OOS_CAGR_4a=(is4a.R8_OOS_CAGR.iloc[k4] if k4 >= 0 else np.nan),
                                        OOS_MaxDD_4a=(is4a.R8_OOS_MaxDD.iloc[k4] if k4 >= 0 else np.nan),
                                        base_OOS_Sharpe=base.R8_OOS_Sharpe, base_OOS_CAGR=base.R8_OOS_CAGR,
                                        base_OOS_MaxDD=base.R8_OOS_MaxDD,
                                        spy_OOS_Sharpe=spy.R8_OOS_Sharpe, spy_OOS_CAGR=spy.R8_OOS_CAGR,
                                        spy_OOS_MaxDD=spy.R8_OOS_MaxDD,
                                        v1_OOS_Sharpe=v1.R8_OOS_Sharpe, ew_OOS_Sharpe=ew.R8_OOS_Sharpe))
    W = pd.DataFrame(wf_rows)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    for scope in ("pub", "ext"):
        w = W[W.scope == scope]
        say(f"[{scope}] {len(w)} cells | IS-Sharpe chooser OOS Sharpe mean {w.OOS_Sharpe.mean():.4f} "
            f"CAGR {w.OOS_CAGR.mean():.2%} MaxDD {w.OOS_MaxDD.mean():.2%}  ||  "
            f"RULES v2 {w.base_OOS_Sharpe.mean():.4f}/{w.base_OOS_CAGR.mean():.2%}/{w.base_OOS_MaxDD.mean():.2%}  "
            f"SPY {w.spy_OOS_Sharpe.mean():.4f}/{w.spy_OOS_CAGR.mean():.2%}/{w.spy_OOS_MaxDD.mean():.2%}  "
            f"EWALL {w.ew_OOS_Sharpe.mean():.4f}  v1 {w.v1_OOS_Sharpe.mean():.4f}")
        say(f"      chooser beats RULES v2 OOS in {int((w.OOS_Sharpe > w.base_OOS_Sharpe).sum())}/{len(w)} cells, "
            f"beats SPY in {int((w.OOS_Sharpe > w.spy_OOS_Sharpe).sum())}/{len(w)}")
        w4 = w[w.pick4a.notna()]
        if len(w4):
            say(f"      IS-4a chooser ({len(w4)} cells with an IS-4a arm): OOS Sharpe "
                f"{w4.OOS_Sharpe_4a.mean():.4f} CAGR {w4.OOS_CAGR_4a.mean():.2%} "
                f"MaxDD {w4.OOS_MaxDD_4a.mean():.2%}; beats RULES v2 OOS in "
                f"{int((w4.OOS_Sharpe_4a > w4.base_OOS_Sharpe).sum())}/{len(w4)}")
    say("")
    say("full walk-forward table (published grids):")
    say(W[W.scope == "pub"][["panel", "cost", "dial", "n_arms", "pick", "OOS_Sharpe", "OOS_CAGR",
                             "OOS_MaxDD", "pick4a", "OOS_Sharpe_4a", "base_OOS_Sharpe",
                             "spy_OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")

    # how the chooser's pick moves when the grid widens
    piv = W.pivot_table(index=["panel", "cost", "dial"], columns="scope", values="OOS_Sharpe")
    moved = W.pivot_table(index=["panel", "cost", "dial"], columns="scope", values="pick", aggfunc="first")
    both = moved.dropna()
    nmove = int((both["pub"].astype(str) != both["ext"].astype(str)).sum())
    say(f"## (4) does the WIDER grid change the rule-8 pick? {nmove} of {len(both)} extendable cells "
        f"move; mean OOS Sharpe {piv['pub'].mean():.4f} (pub) -> {piv['ext'].mean():.4f} (ext)\n")

    # ---------- KEEP tallies
    ar = A[A.dial != "_comparand"]
    say("## (5) both KEEP paths, all arm-rows")
    say(f"published grids: 4a {int(ar[ar.published==1].pass4a.sum())}/{int((ar.published==1).sum())}, "
        f"4b {int(ar[ar.published==1].pass4b.sum())}/{int((ar.published==1).sum())}")
    say(f"with extensions: 4a {int(ar.pass4a.sum())}/{len(ar)}, 4b {int(ar.pass4b.sum())}/{len(ar)}")
    b4 = ar[ar.pass4b == 1]
    if len(b4):
        say("4b passers:")
        say(b4[["panel", "dial", "arm", "cost", "published", "FULL_CAGR", "FULL_Sharpe",
                "FULL_MaxDD", "H1_Sharpe", "H2_Sharpe", "R8_OOS_Sharpe", "R8_OOS_CAGR",
                "turnover_yr"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nelapsed {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()

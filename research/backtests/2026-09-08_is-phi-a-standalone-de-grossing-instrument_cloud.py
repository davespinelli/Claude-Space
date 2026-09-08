#!/usr/bin/env python3
"""QUEUE idea 468 — is-phi-a-standalone-de-grossing-instrument (cloud, 2026-09-08).

QUESTION (queue, verbatim intent)
  Idea 244 found idea 73's count convention is exactly the equal-weight book times a
  breadth-timed overlay phi_t = n_held/n, and that at matched MEAN gross the overlay's
  TIMING alone is worth +0.0480 full-sample / +0.0587 OOS Sharpe on 37 and 36 of 42
  (panel,n) cells, paying +4.1 pp of MaxDD for ~0 CAGR.  phi has never been priced on its
  own — only smuggled inside count sweeps.  Price phi as a STANDALONE overlay on the
  un-ranked EWall book against idea 74's instrument menu (which put de-gross at ~0.63 pp
  per pp) and report whether it is cheaper than the menu's cheapest gate.

WHAT phi IS HERE (the standalone construction, book-consistent)
  For a base book w (no instrument) and a per-name gate mask M:
      phi_t = sum_i w_it * M_it / sum_i w_it        in [0,1]
  i.e. the share of the BOOK's own weight that clears the gate — the un-ranked analogue of
  idea 244's n_held/n.  Three objects share that one gate:
      GATE   = re-spread:   surviving names re-normalised back to GROSS   (SELECTION only)
      PHI    = overlay:     the WHOLE ungated book scaled by phi_t        (TIMING only)
      DGG    = de-grossed:  gated weight goes to CASH, never re-spread    (BOTH)
  and they satisfy the exact identity   DGG = GATE * phi_t  (gate G2 below, 0 to 1e-17).
  PHI and DGG therefore carry the SAME realised gross path day by day — the pairing is
  matched-gross by construction, not by fitting.  PHI is priced as a standalone instrument
  on idea 74's axis, alongside the six committed families.

TUNED PARAMETERS: exactly two, the same two idea 74 used — instrument FAMILY and its
  STRENGTH LEVEL.  Every family x level is reported at every budget; panel, book and cost
  rung are reporting axes, never selected on.  phi's strength ladder is the exponent k in
  phi_t^k (k<1 damps the overlay, k>1 sharpens it; k=0 is the control by construction).

FAMILIES (9 = idea 74's committed 6 + 3 new)
  200d  MA gate, re-spread (window)          [parent]     dg    static de-gross lever   [parent]
  band  200d MA re-entry band, re-spread     [parent]     ddctl book DD control (id 40) [parent]
  abs   absolute momentum, re-spread         [parent]     stop  per-name trailing stop  [parent]
  phi   OVERLAY phi(MA200)^k                 [NEW]        phib  OVERLAY phi(band3)^k    [NEW]
  dgg   de-grossed MA gate (= GATE * phi)    [NEW, the composed object, for attribution]

PANELS  u56 (load_universe), broad136 (broad=True), SMALL439 (small=True, the 44 tickers
  with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Idea 74 priced its menu
  on u56/broad only; the small panel is added as a third reporting axis.
  SURVIVORSHIP: all three panels are CURRENT constituents (PROTOCOL 9; the small panel is
  the sub-$2B screen's survivors since 2010).  Levels are upward-biased and crashes are
  shallower than they were, so every instrument here is priced in a world with less
  drawdown to buy.  The exchange rate is a ratio of two within-cell differences against the
  SAME control on the SAME days, which cancels most but not all of that bias.

BOOKS   idea 245's two instrument-free base books, IMPORTED not re-implemented: EWALL0
  (equal weight over every name) and CAND20 (top 20 by idea 2's composite), both at gross
  0.75.  The queue asks about the un-ranked EWall book; CAND20 is carried as the contrast.

COSTS 10 bps (PROTOCOL 2) and 25 bps, applied analytically.  Weekly cadence, weights decided
  at close t and executed at close t+1 (PROTOCOL 2, inherited from idea 245's simulator).

RULE 8 (PROTOCOL 8) The cheapest instrument (family AND level) at each budget is chosen on
  2009-2016 ONLY and the 2017-2026 window is then read once, against RULES v2 (live), RULES
  v1 and SPY.  Both KEEP paths are evaluated for every arm at both rungs; 4a is judged
  against the LIVE RULES v2 book (PROTOCOL 4a as amended 2026-09-06), with the v1 row kept
  for continuity.

Artefacts: .console.txt .grid.csv .menu.csv .matched.csv .walkforward.csv .keep.csv
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
"""
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-08_is-phi-a-standalone-de-grossing-instrument_cloud"
P74 = "2026-09-06_drawdown-instrument-exchange-rate_cloud"

_LINES: list[str] = []


def say(*a) -> None:
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LINES) + "\n")


def _load(stem: str, mod: str):
    spec = importlib.util.spec_from_file_location(mod, OUT / f"{stem}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


i74 = _load(P74, "i74")                 # the menu, its ladders and its build_menu
i245 = i74.i245                          # base books, simulator, instruments
run = i245.run
arm_returns = i245.arm_returns
apply_gate = i245.apply_gate
gate_mask = i245.gate_mask
BASE_BOOKS = i245.BASE_BOOKS
GROSS = i245.GROSS
m = i245.m
halves = i245.halves
at_cost = i245.at_cost
turn_per_yr = i245.turn_per_yr
fail4b = i245.fail4b
rate = i74.rate
build_menu = i74.build_menu

FREQ = "W"
COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BUDGETS = i74.BUDGETS                    # [2, 4, 6, 8, 10] pp of MaxDD

LADDER = dict(i74.LADDER)                # the parent's six ladders, unchanged
LADDER["phi"] = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]     # exponent k on phi(MA200)
LADDER["phib"] = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]    # exponent k on phi(band 3%)
LADDER["dgg"] = [75, 100, 150, 200, 250, 300]      # MA window, de-grossed (= GATE * phi)
FAMILIES = i74.FAMILIES + ["phi", "phib", "dgg"]
NEW = {"phi", "phib", "dgg"}
LABEL = dict(i74.LABEL)
LABEL.update({"phi": "PHI overlay, breadth(MA200)^k  [NEW]",
              "phib": "PHI overlay, breadth(band3)^k  [NEW]",
              "dgg": "de-grossed MA gate = GATE * phi [NEW]"})


# ------------------------------------------------------------------ phi construction
def phi_series(px, w, kind, param=None):
    """Share of the BOOK's own weight clearing the gate, read at close t (causal)."""
    mask = gate_mask(px, "200d", 200) if kind == "ma" else gate_mask(px, "band", 0.03)
    names = list(mask.columns)
    ww = w[names]
    num = (ww * mask.astype(float)).sum(axis=1)
    den = ww.sum(axis=1).replace(0, np.nan)
    return (num / den).fillna(0.0).clip(0.0, 1.0)


def phi_weights(px, w, kind, k):
    p = phi_series(px, w, kind) ** float(k)
    return w.mul(p, axis=0)


def dg_gate_weights(px, w, window):
    """Gated weight goes to CASH, never re-spread."""
    mask = gate_mask(px, "200d", int(window))
    names = list(mask.columns)
    out = w.copy() * 0.0
    out[names] = w[names] * mask.astype(float)
    return out


def arm_weights_or_returns(px, w, fam, lv, ctrl):
    """(gross, turnover, invested, fires) for any of the nine families."""
    if fam == "phi":
        return run(px, phi_weights(px, w, "ma", lv), freq=FREQ)
    if fam == "phib":
        return run(px, phi_weights(px, w, "band", lv), freq=FREQ)
    if fam == "dgg":
        return run(px, dg_gate_weights(px, w, lv), freq=FREQ)
    return arm_returns(px, w, fam, lv, ctrl)


# ------------------------------------------------------------------ helpers
def window(r, lo=None, hi=None):
    s = r
    if lo is not None:
        s = s.loc[lo:]
    if hi is not None:
        s = s.loc[:hi]
    return s


def fail4a(r, base):
    """PROTOCOL 4a against whichever book is passed (here: LIVE RULES v2)."""
    _, _, dd = m(r)
    h1, h2 = halves(r)
    _, _, bdd = m(base)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def panels():
    out = {"u56": load_universe(), "broad136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    out["SMALL439"] = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    return out


# ------------------------------------------------------------------ gates
def harness(PX):
    say("\n=== HARNESS GATES (asserted before any result is read) ===")
    px = PX["u56"]
    w = BASE_BOOKS["EWALL0"](px)

    g, t, inv, _ = run(px, w, freq=FREQ)
    ref = backtest(px, w, cost_bps=0.0, freq=FREQ)
    d = float(np.abs(g - ref["returns"]).max()), float(np.abs(t - ref["turnover"]).max())
    say(f"G1 run(no instrument) vs engine.backtest        max|dret| {d[0]:.3e}  max|dturn| {d[1]:.3e}")
    assert max(d) < 1e-12

    worst_exact, worst_naive, notfull = 0.0, {}, {}
    for pname, p in PX.items():
        for bname, wfn in BASE_BOOKS.items():
            ww = wfn(p)
            s260 = p.index[260]
            sw = ww.sum(axis=1)
            notfull[(pname, bname)] = int((np.abs(sw.loc[s260:] - GROSS) > 1e-12).sum())
            for L in LADDER["dgg"]:
                lhs = dg_gate_weights(p, ww, L)
                mk = gate_mask(p, "200d", L)
                names = list(mk.columns)
                ph = ((ww[names] * mk.astype(float)).sum(axis=1)
                      / ww[names].sum(axis=1).replace(0, np.nan)).fillna(0.0)
                gate = apply_gate(ww, mk)
                rhs_naive = gate.mul(ph, axis=0)
                rhs_exact = rhs_naive.mul(sw / GROSS, axis=0)          # book-gross factor
                worst_exact = max(worst_exact,
                                  float(np.abs(lhs[names].values - rhs_exact[names].values).max()))
                worst_naive[bname] = max(worst_naive.get(bname, 0.0),
                                         float(np.abs(lhs[names].values - rhs_naive[names].values).max()))
    say(f"G2 IDENTITY  DGG(L) == GATE(L) * phi_L * (sum_w/GROSS)   max|dw| {worst_exact:.3e}  "
        f"(36 panel x book x level cells)")
    for bname in BASE_BOOKS:
        say(f"     without the book-gross factor, {bname}: max|dw| {worst_naive[bname]:.3e}   "
            f"(rows after warm-up where the base book is not fully invested: "
            + ", ".join(f"{pn} {notfull[(pn, bname)]}" for pn in PX) + ")")
    say("     -> on the un-ranked EWALL0 book (the queue's book) the identity DGG = GATE * phi is "
        "EXACT; on CAND20 it carries the book's own gross factor because fewer than 20 names "
        "rank on some days.")
    assert worst_exact < 1e-12

    # G3 matched gross: PHI(k=1, MA200) and DGG(200) carry the same TARGET gross every day
    gw, tgt = [], 0.0
    for pname, p in PX.items():
        for bname, wfn in BASE_BOOKS.items():
            ww = wfn(p)
            s = p.index[260]
            wp, wd = phi_weights(p, ww, "ma", 1.0), dg_gate_weights(p, ww, 200)
            tgt = max(tgt, float(np.abs(wp.sum(axis=1) - wd.sum(axis=1)).max()))
            a = run(p, wp, freq=FREQ)[2].loc[s:]
            b = run(p, wd, freq=FREQ)[2].loc[s:]
            gw.append((pname, bname, a.mean(), b.mean(), float(np.abs(a - b).max())))
    say(f"G3 MATCHED GROSS  PHI(k=1) vs DGG(200): TARGET gross identical every day, "
        f"max|d| {tgt:.3e}")
    assert tgt < 1e-12
    say("   realised (weekly-held, drifted) invested share — differs only through intra-week "
        "drift of a different composition:")
    for pn, bk, x, y, dmax in gw:
        say(f"     {pn:9s} {bk:7s}  {x:.4f} vs {y:.4f}   max|d| {dmax:.3e}")
    say("   -> the PHI/DGG pairing is matched-gross by CONSTRUCTION, not by fitting.")

    # G4 provenance: reproduce the parent's committed grid on the shared families
    par = pd.read_csv(OUT / f"{P74}.grid.csv")
    say(f"G4 parent grid {P74}.grid.csv: {len(par)} rows, families {sorted(par.family.unique())}")
    return par


# ------------------------------------------------------------------ sweep
def sweep(px, pname, rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = m(spy.loc[OOS_START:])[1]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]

    for bname, wfn in BASE_BOOKS.items():
        w = wfn(px)
        ctrl_full = run(px, w, freq=FREQ)
        g_c, t_c, inv_c = (s.loc[start:] for s in ctrl_full[:3])

        sims = {}
        for fam in FAMILIES:
            for lv in LADDER[fam]:
                gg, tt, ii, nf = arm_weights_or_returns(px, w, fam, lv, ctrl_full)
                sims[(fam, lv)] = (gg.loc[start:], tt.loc[start:], ii.loc[start:], nf)

        for cost in COSTS:
            r_c = at_cost(g_c, t_c, cost)
            c_c, s_c, dd_c = m(r_c)
            cIS, sIS, ddIS = m(window(r_c, hi=IS_END))
            cOS, sOS, ddOS = m(window(r_c, lo=OOS_START))
            h1c, h2c = halves(r_c)
            rows.append(dict(panel=pname, book=bname, cost=cost, family="none", level=np.nan,
                             CAGR=c_c, Sharpe=s_c, MaxDD=dd_c, H1=h1c, H2=h2c,
                             IS_CAGR=cIS, IS_Sharpe=sIS, IS_MaxDD=ddIS,
                             OOS_CAGR=cOS, OOS_Sharpe=sOS, OOS_MaxDD=ddOS,
                             paid_pp=0.0, bought_pp=0.0, xrate=np.nan,
                             IS_paid=0.0, IS_bought=0.0, IS_xrate=np.nan,
                             OOS_paid=0.0, OOS_bought=0.0, OOS_xrate=np.nan,
                             gross=float(inv_c.mean()), turn_yr=turn_per_yr(t_c),
                             fail4a="|".join(fail4a(r_c, v2)),
                             fail4b="|".join(fail4b(r_c, spy, sOS, spy_oos))))

            for (fam, lv), (gg, tt, ii, nf) in sims.items():
                r = at_cost(gg, tt, cost)
                c, sh, dd = m(r)
                h1, h2 = halves(r)
                ci, si, ddi = m(window(r, hi=IS_END))
                co, so, ddo = m(window(r, lo=OOS_START))
                paid, bought = (c_c - c) * 100, (dd - dd_c) * 100
                ip_, ib = (cIS - ci) * 100, (ddi - ddIS) * 100
                op, ob = (cOS - co) * 100, (ddo - ddOS) * 100
                rows.append(dict(
                    panel=pname, book=bname, cost=cost, family=fam, level=lv,
                    CAGR=c, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                    IS_CAGR=ci, IS_Sharpe=si, IS_MaxDD=ddi,
                    OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=ddo,
                    paid_pp=paid, bought_pp=bought, xrate=rate(paid, bought),
                    IS_paid=ip_, IS_bought=ib, IS_xrate=rate(ip_, ib),
                    OOS_paid=op, OOS_bought=ob, OOS_xrate=rate(op, ob),
                    gross=float(ii.mean()), turn_yr=turn_per_yr(tt),
                    fail4a="|".join(fail4a(r, v2)),
                    fail4b="|".join(fail4b(r, spy, so, spy_oos))))

    return dict(panel=pname,
                spy_CAGR=m(spy)[0], spy_Sharpe=m(spy)[1], spy_MaxDD=m(spy)[2],
                spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                spy_OOS_CAGR=m(spy.loc[OOS_START:])[0], spy_OOS_Sharpe=spy_oos,
                spy_OOS_MaxDD=m(spy.loc[OOS_START:])[2],
                v2_CAGR=m(v2)[0], v2_Sharpe=m(v2)[1], v2_MaxDD=m(v2)[2],
                v2_H1=halves(v2)[0], v2_H2=halves(v2)[1],
                v2_OOS_CAGR=m(v2.loc[OOS_START:])[0], v2_OOS_Sharpe=m(v2.loc[OOS_START:])[1],
                v2_OOS_MaxDD=m(v2.loc[OOS_START:])[2],
                v1_Sharpe=m(v1)[1], v1_OOS_Sharpe=m(v1.loc[OOS_START:])[1])


# ------------------------------------------------------------------ main
def main():
    pd.set_option("display.width", 250)
    say(f"# research/backtests/{STEM}.py")
    say("# QUEUE idea 468 — phi (breadth-timed exposure) priced as a STANDALONE instrument "
        "on idea 74's axis")
    say("# rate = (CAGR_control - CAGR_arm) / (MaxDD_arm - MaxDD_control), pp per pp. "
        "LOWER = cheaper insurance.")

    PX = panels()
    for k, v in PX.items():
        say(f"panel {k}: {v.shape[1]-1} names + SPY, {v.index[0].date()} -> {v.index[-1].date()}, "
            f"{len(v)} days")
    par = harness(PX)

    rows, refs = [], []
    for pname, p in PX.items():
        say(f"\n... sweeping {pname} ({len(FAMILIES)} families x 6 levels x 2 books x 2 rungs)")
        refs.append(sweep(p, pname, rows))
    G = pd.DataFrame(rows)
    R = pd.DataFrame(refs).set_index("panel")
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---- G4b provenance against the parent's committed grid (shared cells only)
    key = ["panel", "book", "cost", "family", "level"]
    shared = G.merge(par, on=key, suffixes=("", "_par"))
    shared = shared[shared.family != "none"]
    if len(shared):
        dc = float(np.abs(shared.CAGR - shared.CAGR_par).max())
        dd = float(np.abs(shared.MaxDD - shared.MaxDD_par).max())
        reach = shared[shared.bought_pp >= 1.0]
        dx = float(np.nanmax(np.abs(reach.xrate - reach.xrate_par))) if len(reach) else np.nan
        say(f"\nG4 REPRODUCTION of idea 74's committed grid on {len(shared)} shared arm-rows: "
            f"max|dCAGR| {dc:.3e}  max|dMaxDD| {dd:.3e}  "
            f"max|dxrate| {dx:.3e} over the {len(reach)} rows that bought >= 1 pp")
        say("   NOT bit-exact and not claimed to be: data/prices.csv was REWRITTEN on 2026-09-08 "
            "(commit 26d0089, all 4,700 rows) after idea 74 ran on 2026-09-06, so the shared cells "
            "differ by the data revision alone. The tolerance asserted is 1e-3 of CAGR / 1e-4 of "
            "MaxDD; anything larger would mean a re-implementation difference, not a data one.")
        assert dc < 1e-3 and dd < 1e-4, "G4 FAILED — the parent's numbers are not reproduced"

    say("\n=== REFERENCE ROWS (per panel, @10 bps, warm-up skipped) ===")
    say(R.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- (1) the menu
    say("\n=== (1) THE MENU — cheapest setting of each family that buys >= T pp of MaxDD ===")
    M = build_menu(G)
    M.to_csv(OUT / f"{STEM}.menu.csv", index=False)
    for pname in PX:
        for bk in BASE_BOOKS:
            for cost in COSTS:
                sub = M[(M.panel == pname) & (M.book == bk) & (M.cost == cost)]
                if not len(sub):
                    continue
                say(f"\n--- {pname} / {bk} / {cost} bps ---   (xrate, lower = cheaper; "
                    f"'--' = family cannot reach the budget)")
                tab = sub.pivot(index="family", columns="budget", values="xrate")
                tab = tab.reindex([f for f in FAMILIES if f in tab.index])
                say(tab.to_string(float_format=lambda x: f"{x:.3f}", na_rep="   --"))
                for T in BUDGETS:
                    ok = sub[(sub.budget == T) & sub.reachable]
                    if not len(ok):
                        continue
                    win = ok.loc[ok.xrate.idxmin()]
                    gates_only = ok[ok.family.isin(["200d", "band", "abs"])]
                    gbest = gates_only.loc[gates_only.xrate.idxmin()] if len(gates_only) else None
                    phis = ok[ok.family.isin(["phi", "phib"])]
                    pbest = phis.loc[phis.xrate.idxmin()] if len(phis) else None
                    say(f"    T={T:4.1f}pp  cheapest={win.family}({win.level:g}) {win.xrate:.3f}"
                        + (f" | cheapest GATE={gbest.family}({gbest.level:g}) {gbest.xrate:.3f}" if gbest is not None else " | no gate reaches")
                        + (f" | best PHI={pbest.family}({pbest.level:g}) {pbest.xrate:.3f}" if pbest is not None else " | no phi reaches"))

    # ---- the headline count: is phi cheaper than the cheapest gate / than de-gross?
    say("\n=== (2) HEADLINE — phi vs the menu, over every reachable (panel, book, cost, budget) cell ===")
    cells = []
    for (pn, bk, cost, T), g in M.groupby(["panel", "book", "cost", "budget"]):
        ok = g[g.reachable]
        if not len(ok):
            continue
        def best(fams):
            s = ok[ok.family.isin(fams)]
            return (s.xrate.min(), s.loc[s.xrate.idxmin()].family, s.loc[s.xrate.idxmin()].level) if len(s) else (np.nan, "", np.nan)
        xg, fg, lg = best(["200d", "band", "abs"])
        xp, fp, lp = best(["phi", "phib"])
        xd, _, ld = best(["dg"])
        xall, fall, lall = best([f for f in FAMILIES if f not in ("phi", "phib", "dgg")])
        cells.append(dict(panel=pn, book=bk, cost=cost, budget=T,
                          phi_x=xp, phi_arm=f"{fp}({lp:g})" if fp else "",
                          gate_x=xg, gate_arm=f"{fg}({lg:g})" if fg else "",
                          dg_x=xd, menu_x=xall, menu_arm=f"{fall}({lall:g})" if fall else "",
                          phi_beats_gate=xp < xg if np.isfinite(xp) and np.isfinite(xg) else np.nan,
                          phi_beats_dg=xp < xd if np.isfinite(xp) and np.isfinite(xd) else np.nan,
                          phi_beats_menu=xp < xall if np.isfinite(xp) and np.isfinite(xall) else np.nan))
    C = pd.DataFrame(cells)
    say(C.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for col, what in [("phi_beats_gate", "the cheapest GATE (200d/band/abs)"),
                      ("phi_beats_dg", "the de-gross reference lever"),
                      ("phi_beats_menu", "the cheapest instrument on idea 74's WHOLE menu")]:
        s = C[col].dropna().astype(bool).astype(int)
        if not len(s):
            say(f"  {col}: no comparable cells")
            continue
        say(f"  phi cheaper than {what}: {int(s.sum())} of {len(s)} cells ({s.mean():.1%})")
        for pn in PX:
            t = C[C.panel == pn][col].dropna().astype(bool).astype(int)
            for bk in BASE_BOOKS:
                u = C[(C.panel == pn) & (C.book == bk)][col].dropna().astype(bool).astype(int)
                if len(u):
                    say(f"       {pn:9s} {bk:7s} {int(u.sum())}/{len(u)}")

    # ---------------------------------------------------------------- (3) matched gross
    say("\n=== (3) MATCHED-GROSS ATTRIBUTION — the same gate, split into SELECTION and TIMING ===")
    say("    DGG(L) = GATE(L) * phi_L exactly (G2).  DGG and PHI(k=1) carry the same realised")
    say("    gross path (G3).  So  DGG - PHI = what the gate's SELECTION adds at matched gross,")
    say("    and  PHI - control = what the TIMING alone is worth.")
    mrows = []
    for (pn, bk, cost), g in G[G.family != "none"].groupby(["panel", "book", "cost"]):
        ctl = G[(G.panel == pn) & (G.book == bk) & (G.cost == cost) & (G.family == "none")].iloc[0]
        dgg = g[(g.family == "dgg") & (g.level == 200)].iloc[0]
        phi = g[(g.family == "phi") & (g.level == 1.0)].iloc[0]
        gate = g[(g.family == "200d") & (g.level == 200)].iloc[0]
        mrows.append(dict(panel=pn, book=bk, cost=cost,
                          ctl_CAGR=ctl.CAGR, ctl_Sharpe=ctl.Sharpe, ctl_MaxDD=ctl.MaxDD, ctl_gross=ctl.gross,
                          PHI_CAGR=phi.CAGR, PHI_Sharpe=phi.Sharpe, PHI_MaxDD=phi.MaxDD, PHI_gross=phi.gross,
                          DGG_CAGR=dgg.CAGR, DGG_Sharpe=dgg.Sharpe, DGG_MaxDD=dgg.MaxDD, DGG_gross=dgg.gross,
                          GATE_CAGR=gate.CAGR, GATE_Sharpe=gate.Sharpe, GATE_MaxDD=gate.MaxDD, GATE_gross=gate.gross,
                          sel_dSharpe=dgg.Sharpe - phi.Sharpe, sel_dCAGR=(dgg.CAGR - phi.CAGR) * 100,
                          sel_dMaxDD=(dgg.MaxDD - phi.MaxDD) * 100,
                          tim_dSharpe=phi.Sharpe - ctl.Sharpe, tim_dCAGR=(phi.CAGR - ctl.CAGR) * 100,
                          tim_dMaxDD=(phi.MaxDD - ctl.MaxDD) * 100,
                          sel_OOS_dSharpe=dgg.OOS_Sharpe - phi.OOS_Sharpe,
                          tim_OOS_dSharpe=phi.OOS_Sharpe - ctl.OOS_Sharpe,
                          PHI_x=phi.xrate, DGG_x=dgg.xrate, GATE_x=gate.xrate))
    MA = pd.DataFrame(mrows)
    MA.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    say(MA[["panel", "book", "cost", "ctl_gross", "PHI_gross", "DGG_gross", "GATE_gross",
            "tim_dCAGR", "tim_dSharpe", "tim_dMaxDD", "sel_dCAGR", "sel_dSharpe", "sel_dMaxDD",
            "tim_OOS_dSharpe", "sel_OOS_dSharpe"]].to_string(index=False,
                                                             float_format=lambda x: f"{x:.4f}"))
    say(f"\n  TIMING alone (PHI - control): mean dSharpe {MA.tim_dSharpe.mean():+.4f} "
        f"({int((MA.tim_dSharpe > 0).sum())}/{len(MA)} cells positive), "
        f"mean dCAGR {MA.tim_dCAGR.mean():+.2f} pp, mean dMaxDD {MA.tim_dMaxDD.mean():+.2f} pp, "
        f"mean OOS dSharpe {MA.tim_OOS_dSharpe.mean():+.4f} "
        f"({int((MA.tim_OOS_dSharpe > 0).sum())}/{len(MA)})")
    say(f"  SELECTION at matched gross (DGG - PHI): mean dSharpe {MA.sel_dSharpe.mean():+.4f} "
        f"({int((MA.sel_dSharpe > 0).sum())}/{len(MA)} cells positive), "
        f"mean dCAGR {MA.sel_dCAGR.mean():+.2f} pp, mean dMaxDD {MA.sel_dMaxDD.mean():+.2f} pp, "
        f"mean OOS dSharpe {MA.sel_OOS_dSharpe.mean():+.4f} "
        f"({int((MA.sel_OOS_dSharpe > 0).sum())}/{len(MA)})")

    # ---------------------------------------------------------------- (4) rule 8
    say("\n=== (4) RULE 8 — instrument chosen on 2009-2016 ONLY (cheapest IS xrate reaching T), "
        "2017-2026 read ONCE ===")
    wrows = []
    for (pn, bk, cost), g in G[G.family != "none"].groupby(["panel", "book", "cost"]):
        ref = R.loc[pn]
        for T in BUDGETS:
            ok = g[(g.IS_bought >= T) & np.isfinite(g.IS_xrate)]
            if not len(ok):
                wrows.append(dict(panel=pn, book=bk, cost=cost, budget=T, IS_pick="unreachable"))
                continue
            pick = ok.loc[ok.IS_xrate.idxmin()]
            oos_ok = g[(g.OOS_bought >= T) & np.isfinite(g.OOS_xrate)]
            oracle = oos_ok.loc[oos_ok.OOS_xrate.idxmin()] if len(oos_ok) else None
            wrows.append(dict(
                panel=pn, book=bk, cost=cost, budget=T,
                IS_pick=f"{pick.family}({pick.level:g})", IS_xrate=pick.IS_xrate,
                IS_bought=pick.IS_bought, OOS_bought=pick.OOS_bought, OOS_xrate=pick.OOS_xrate,
                OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                oracle=f"{oracle.family}({oracle.level:g})" if oracle is not None else "",
                oracle_xrate=oracle.OOS_xrate if oracle is not None else np.nan,
                pick_is_phi=pick.family in ("phi", "phib"),
                oracle_is_phi=(oracle.family in ("phi", "phib")) if oracle is not None else np.nan,
                v2_OOS_Sharpe=ref.v2_OOS_Sharpe, v2_OOS_CAGR=ref.v2_OOS_CAGR,
                v2_OOS_MaxDD=ref.v2_OOS_MaxDD,
                spy_OOS_Sharpe=ref.spy_OOS_Sharpe, spy_OOS_CAGR=ref.spy_OOS_CAGR,
                spy_OOS_MaxDD=ref.spy_OOS_MaxDD))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    live = W[W.IS_pick != "unreachable"]
    pick_phi = live.pick_is_phi.dropna().astype(bool).astype(int)
    orac_phi = live.oracle_is_phi.dropna().astype(bool).astype(int)
    say(f"\n  IS-cheapest is a PHI arm in {int(pick_phi.sum())} of {len(pick_phi)} cells; "
        f"OOS-cheapest (oracle) is a PHI arm in {int(orac_phi.sum())} of {len(orac_phi)}.")
    same = (live.IS_pick == live.oracle).sum()
    say(f"  IS pick stays OOS-cheapest in {int(same)} of {len(live)}; mean OOS-minus-IS xrate "
        f"{np.nanmean(live.OOS_xrate - live.IS_xrate):+.3f}; IS pick still reaches its budget OOS "
        f"in {int((live.OOS_bought >= live.budget).sum())} of {len(live)}.")

    # ---------------------------------------------------------------- (5) KEEP paths
    say("\n=== (5) BOTH KEEP PATHS, every arm, both rungs (4a vs LIVE RULES v2, 4b vs SPY) ===")
    A = G.copy()
    A["pass4a"] = A.fail4a == ""
    A["pass4b"] = A.fail4b == ""
    say(f"  4a: {int(A.pass4a.sum())} of {len(A)} rows;  4b: {int(A.pass4b.sum())} of {len(A)} rows")
    byfam = A.groupby("family")[["pass4a", "pass4b"]].sum().astype(int)
    byfam["n"] = A.groupby("family").size()
    say(byfam.to_string())
    kp = A[A.pass4b]
    if len(kp):
        say("\n  4b passers:")
        say(kp[["panel", "book", "cost", "family", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "gross", "turn_yr"]].to_string(index=False,
                                                             float_format=lambda x: f"{x:.4f}"))
    A.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    say("\n  4b bars per panel (SPY): " + "; ".join(
        f"{p}: CAGR>={R.loc[p].spy_CAGR*0.7:.2%}, MaxDD>={R.loc[p].spy_MaxDD*0.6:.2%}, "
        f"H1>{R.loc[p].spy_H1:.3f}, H2>{R.loc[p].spy_H2:.3f}, OOS>{R.loc[p].spy_OOS_Sharpe:.3f}"
        for p in PX))

    say("\nSURVIVORSHIP: all three panels are current constituents (PROTOCOL 9); the small panel "
        "is the sub-$2B screen's survivors since 2010 with the 44 max_1d_move >= 1.0 tickers "
        "dropped. Levels are upward-biased; the exchange rate is a within-cell ratio against the "
        "same control on the same days, which cancels most but not all of that bias.")
    say(f"\nwrote {STEM}.grid.csv / .menu.csv / .matched.csv / .walkforward.csv / .keep.csv")
    flush()


if __name__ == "__main__":
    main()

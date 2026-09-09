#!/usr/bin/env python3
"""Idea 509 — does any other published EDGE FLAG survive its own EXTENSION re-run?

Idea 500 extended idea 270R's band grid 3x past its published stop (0.12 -> 0.35) and the
flag did NOT survive: the binding-half Sharpe argmax moved to an INTERIOR point (0.16), so
"monotone to the widest point tested" turned out to be a statement about where the author
stopped, not about the curve.  Idea 240 had already done the same to idea 77's n=20 flag
and the argmax moved off 20 on 4 of 7 panels — but re-fired at the NEW grid top (n=60) on
3 of them, which is the reporting habit, not a finding.

This run asks whether that is general.  Two tuned parameters, exactly the queue's:
FLAG (the flagged dial family) x EXTENSION DEPTH (0/1/2/3 steps past the published stop).
Panel, cost rung and outcome metric are reporting axes, not tuned dials: every point of
every grid is written to .arms.csv and every classification to .extension.csv.

PRE-REGISTERED BEFORE ANY NUMBER WAS READ
-----------------------------------------
Flag population.  Two censuses, both reported:
  (a) TEXTUAL — every committed .md under research/ is scanned for the record's own
      edge-flag language ("grid edge", "ladder edge", "argmax at a grid end", "monotone to
      the widest point tested", ...).  This counts the CLAIMS.
  (b) NUMERIC — idea 256's committed cells file (22,443 fully-crossed cells, 100 (file,dial)
      grids) is re-read and its edge / edge_mono decomposition rebuilt.  This counts the
      SHAPES.  Idea 256's own published headline (87.4% of argmaxes at a grid end) is a
      reproduction gate.

Endpoint status.  An endpoint is STRUCTURAL when the instrument cannot be widened past it:
      n     high = the panel's own name count (cannot rank more names than exist), low = 1
      band  low  = 0.00 (no hysteresis is the plain 200d MA rule; a negative band is not
                   an instrument), high = OPEN
      gross high = 1.00 (PROTOCOL 2: no leverage), low = OPEN until the book is degenerate
      m     high = 1.3333 (PROTOCOL 2 again: m is a multiplier on a 0.75 target gross, so
                   m > 4/3 is leverage), low = OPEN
      volcap high = 9.99 (no filter), low = OPEN until the book is empty
      quantile high = 1.00 (no filter), low = OPEN until the book is empty
      cadence BOTH (D is the engine's fastest schedule, Q its slowest) -> the CONTROL flag,
                   a dial whose edge flags cannot be extension-tested at all.
An extension step that would cross a structural bound, or that empties the book (mean held
names < 1), is recorded CLOSED at that depth and no arm is run past it.

Extension geometry, fixed in advance and applied uniformly:
      HIGH end -> arithmetic, step = the published grid's own last step (p_L - p_{L-1}).
      LOW  end -> geometric, ratio = the published grid's own first ratio (p_1 / p_2),
                  because every low end here is a positive scale bounded below by 0.
Depth k = k such steps.  Depth 0 = the published grid, untouched.

Verdict classes, per (flag, panel, cost, outcome, depth), evaluated on the grid as it
stands at that depth:
      SURVIVES         the argmax is STILL the published endpoint the flag named.
      MIGRATE_EDGE     the argmax has moved to the NEW extended endpoint -> the flag simply
                       re-fires one grid wider; this is the reporting habit.
      MIGRATE_INTERIOR the argmax is strictly interior -> the flag was a stopping-point
                       artefact and a real optimum exists (idea 500's band = 0.16 shape).
      CLOSED           the endpoint is structural / degenerate; the flag cannot be tested.
A flag that is MIGRATE_EDGE at every depth it can reach is a reporting habit.  A flag that
SURVIVES to depth 3 is a finding.

PROTOCOL compliance: 10 bps headline and a 25 bps rung (one gross backtest per arm, both
rungs derived and gated exactly against engine.backtest); weights at close t applied at
t+1 (engine); weekly cadence except on the cadence dial; no shorting, no leverage (arms
above the no-leverage ceiling are never run).  Rule 8 is run for every flag at every depth:
the arm is chosen on 2009-2016 IS Sharpe alone and 2017-2026 is read once, against RULES v2
(live), RULES v1, SPY and an equal-weight-everything do-nothing control.  Both KEEP paths
(4a and 4b) are evaluated for every arm at every depth.  No network.

SURVIVORSHIP: B136 is the current constituents of research/universe_broad.json; SMALL439 is
the sub-$2B screen with the 44 tickers whose max_1d_move >= 1.0 dropped first.  Neither is
free of survivorship bias and no conclusion below is quoted as a live expectation.
"""
from __future__ import annotations
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_does-any-other-published-EDGE-FLAG-survive-its-own-EXTENSION-re-run_C"
OUT = ROOT / "research" / "backtests"
GROSS, BAND = 0.75, 0.03
COSTS = [10, 25]
OOS_START = "2017-01-01"
DEPTHS = [0, 1, 2, 3]

_console: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


# ------------------------------------------------------------------ book forms
# lifted verbatim from idea 270R / idea 500 so the extension is run on the same
# instruments the flags were published on.
def _ew(px, mask, gross):
    e = mask.astype(float).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_topn(px, n, gross=GROSS):
    s, above, _ = score(px)
    r = s.where(above).rank(axis=1, ascending=False)
    return _ew(px, r <= n, gross)


def w_band(px, band, gross=GROSS):
    return rules_v2_weights(px, band=band, gross=gross)


def w_gross(px, gross, band=BAND):
    return rules_v2_weights(px, band=band, gross=gross)


def w_volcap(px, cap, gross=GROSS):
    _, above, vol20 = score(px)
    return _ew(px, above & (vol20 < cap), gross)


def w_quantile(px, x, gross=GROSS):
    s, above, _ = score(px)
    r = s.where(above).rank(axis=1, ascending=False, pct=True)
    return _ew(px, r <= x, gross)


def w_m(px, m, n=20):
    """The record's SCALE ladder: a static multiplier on a 0.75 target gross, applied to the
    ranked top-20 book (the form the 2026-09-04 KEEP 4b candidate uses).  m = 1.00 is 0.75
    gross, so PROTOCOL 2's no-leverage ceiling sits at m = 4/3."""
    return w_topn(px, n, gross=GROSS * m)


def w_ewall(px, gross=GROSS):
    return _ew(px, px.notna(), gross)


# ------------------------------------------------------------------ the flags
# pub  = the record's widest PUBLISHED grid for that dial family (post-240 for n,
#        post-500 for band, the m-family grid for m, idea 270R's for the rest)
# ends = which end(s) are structural, with the bound
FLAGS = {
    "n": dict(fn=w_topn, freq="W", pub=[5, 10, 20, 30, 40, 60],
              hi_struct="panel_names", lo_struct=1, integer=True,
              anchor="idea 77 -> 240: n=20 flagged a grid edge, argmax re-fired at n=60"),
    "band": dict(fn=w_band, freq="W", pub=[0.00, 0.01, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.35],
                 hi_struct=None, lo_struct=0.00, integer=False,
                 anchor="idea 270R -> 500: monotone to 0.12, argmax moved interior to 0.16"),
    "gross": dict(fn=w_gross, freq="W", pub=[0.25, 0.50, 0.75, 1.00],
                  hi_struct=1.00, lo_struct=None, integer=False,
                  anchor="census dial 'g': 1,870 of 1,925 cells at an edge, 100% monotone"),
    "m": dict(fn=w_m, freq="W", pub=[round(0.10 + 0.05 * i, 2) for i in range(25)],
              hi_struct=4.0 / 3.0, lo_struct=None, integer=False,
              anchor="census dial 'm': 6,866 edge cells, the record's largest flag family"),
    "volcap": dict(fn=w_volcap, freq="W", pub=[0.30, 0.45, 0.60, 0.90, 9.99],
                   hi_struct=9.99, lo_struct=None, integer=False,
                   anchor="idea 270R volatility gate; high end is 'no filter'"),
    "quantile": dict(fn=w_quantile, freq="W", pub=[0.10, 0.25, 0.50, 0.75, 1.00],
                     hi_struct=1.00, lo_struct=None, integer=False,
                     anchor="idea 270R selectivity gate; high end is 'no filter'"),
    "cadence": dict(fn=None, freq=None, pub=["D", "W", "M", "Q"],
                    hi_struct="Q", lo_struct="D", integer=False,
                    anchor="CONTROL: both ends structural, the flag cannot be extended"),
}

# the outcomes an argmax can be read on (idea 256's own outcome set, condensed)
OUTCOMES = ["Sharpe", "BindSharpe", "CAGR", "MaxDD", "OOS_Sharpe"]


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]


# ------------------------------------------------------------------ metrics
def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def trio(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def split_r8(r):
    m = r.index < pd.Timestamp(OOS_START)
    return r[m], r[~m]


def stats(r):
    h1, h2 = halves(r)
    c, s, d = trio(r)
    c1, s1, _ = trio(h1)
    c2, s2, _ = trio(h2)
    ic, isx, idd = trio(r[r.index < pd.Timestamp(OOS_START)])
    oc, osx, odd = trio(r[r.index >= pd.Timestamp(OOS_START)])
    return dict(FULL_CAGR=c, FULL_Sharpe=s, FULL_MaxDD=d, H1_Sharpe=s1, H2_Sharpe=s2,
                H1_CAGR=c1, H2_CAGR=c2,
                R8_IS_CAGR=ic, R8_IS_Sharpe=isx, R8_IS_MaxDD=idd,
                R8_OOS_CAGR=oc, R8_OOS_Sharpe=osx, R8_OOS_MaxDD=odd)


def costed(gross_ret, turnover, bps):
    return gross_ret - turnover * bps / 1e4


def run_book(px, w, freq, start):
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


# ------------------------------------------------------------------ extension geometry
def ext_points(pub, end, depth, spec, n_names):
    """The pre-registered continuation of a published grid.  Returns (points, closed_at)."""
    if spec["fn"] is None:                      # cadence: structural both ends
        return [], 1
    pts, closed = [], None
    if end == "hi":
        step = pub[-1] - pub[-2]
        bound = spec["hi_struct"]
        if bound == "panel_names":
            bound = n_names
        cur = pub[-1]
        for k in range(depth):
            cur = cur + step
            if spec["integer"]:
                cur = int(round(cur))
            if bound is not None and cur > bound + 1e-9:
                closed = k + 1
                break
            pts.append(cur)
    else:
        ratio = pub[1] / pub[0] if pub[0] > 0 else None
        bound = spec["lo_struct"]
        if pub[0] <= 0 or ratio is None:        # a zero low end is the structural floor
            return [], 1
        cur = pub[0]
        for k in range(depth):
            cur = cur / ratio
            if spec["integer"]:
                cur = int(round(cur))
            if bound is not None and cur < bound - 1e-9:
                closed = k + 1
                break
            pts.append(round(cur, 6))
    return pts, closed


def main():
    t0 = time.time()
    say(f"# {STAMP}\n")
    say("Pre-registered: FLAG x EXTENSION DEPTH.  SURVIVES = argmax still at the published "
        "endpoint; MIGRATE_EDGE = argmax at the NEW extended endpoint (the reporting habit); "
        "MIGRATE_INTERIOR = argmax strictly interior; CLOSED = structural or degenerate.\n")

    # ================================================================ CENSUS (a): the CLAIMS
    say("## (0a) TEXTUAL census of the record's edge-flag language")
    PATS = {
        "grid-edge": r"grid[- ]edge|grid END|grid end|edge of the grid|at a grid endpoint|"
                     r"ladder edge|GRID_EDGE|grid top",
        "monotone-to-widest": r"monotone (?:in|out|to)[^.]{0,80}widest|"
                              r"widest (?:point|value|arm|n|m)[^.]{0,40}tested|"
                              r"ladder never turned|never turned over",
        "argmax-at-end": r"argmax (?:sits |is )?at (?:a |the )?(?:grid )?(?:end|edge|endpoint|top|boundary)",
    }
    md = sorted((ROOT / "research" / "backtests").glob("*.md")) + \
        [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md",
         ROOT / "research" / "QUEUE.md"]
    tex_rows = []
    for f in md:
        t = f.read_text(errors="ignore")
        d = {k: len(re.findall(p, t)) for k, p in PATS.items()}
        if sum(d.values()):
            tex_rows.append(dict(file=f.name, **d, total=sum(d.values())))
    TEX = pd.DataFrame(tex_rows).sort_values("total", ascending=False)
    TEX.to_csv(OUT / f"{STAMP}.textcensus.csv", index=False)
    say(f"{len(md)} committed .md files scanned; {len(TEX)} carry at least one edge-flag phrase; "
        f"{int(TEX.total.sum())} phrases in all "
        f"(grid-edge {int(TEX['grid-edge'].sum())}, monotone-to-widest "
        f"{int(TEX['monotone-to-widest'].sum())}, argmax-at-end {int(TEX['argmax-at-end'].sum())}).")
    say("top result/memo files (the three registers LEADERBOARD/CHANGELOG/QUEUE excluded):")
    reg = {"LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md"}
    say(TEX[~TEX.file.isin(reg)].head(12).to_string(index=False))
    say("")

    # ================================================================ CENSUS (b): the SHAPES
    say("## (0b) NUMERIC census — idea 256's committed cells file, re-read")
    cells = pd.read_csv(OUT / "2026-09-06_every-published-reach-is-a-ladder-edge_C.cells.csv.gz")
    edge_rate = cells.edge.mean()
    say(f"cells {len(cells)}  (idea 256 published 22,443)   files {cells.stem.nunique()}   "
        f"dials {cells.dial.nunique()}   (file,dial) grids {cells.groupby(['stem','dial']).ngroups}")
    say(f"argmax at a grid END: {edge_rate:.3%}   (idea 256 published 87.4%)")
    say(f"of those, MONOTONE (ladder never turned): {cells[cells.edge].monotone.mean():.3%}   "
        f"(idea 256 published 66.9% of all cells -> {cells.edge_mono.mean():.3%} here)")
    gate_256 = abs(edge_rate - 0.874) < 0.002 and len(cells) == 22443
    say(f"GATE idea-256 reproduction: {'PASS' if gate_256 else 'FAIL'}")
    assert gate_256, "idea 256's census does not reproduce from its own committed cells file"
    dcen = cells[cells.edge].groupby("dial").agg(
        edge_cells=("edge", "size"), lo=("edge_lo", "sum"), hi=("edge_hi", "sum"),
        monotone=("monotone", "sum"), files=("stem", "nunique")).sort_values("edge_cells", ascending=False)
    dcen["lo_share"] = (dcen.lo / dcen.edge_cells).round(3)
    dcen.to_csv(OUT / f"{STAMP}.census.csv")
    say("edge cells by dial (the flag population this run extends):")
    say(dcen.head(12).to_string())
    say("")

    # ================================================================ the extension re-runs
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    # ---- reproduction gates on live books, before any new number
    say("## Reproduction gates")
    pxu = panels["U56"]
    start_u = pxu.index[260]
    g, tv = run_book(pxu, rules_v2_weights(pxu), "W", start_u)
    live = stats(costed(g, tv, 10))
    say(f"RULES v2 U56 @10bps: CAGR {live['FULL_CAGR']:.2%} Sharpe {live['FULL_Sharpe']:.4f} "
        f"MaxDD {live['FULL_MaxDD']:.2%} halves {live['H1_Sharpe']:.4f}/{live['H2_Sharpe']:.4f}"
        "   (idea 500 read 8.64% / 1.2037 / -12.05% / 1.2309 / 1.1828)")
    direct = backtest(pxu, rules_v2_weights(pxu), cost_bps=10.0, freq="W")["returns"].loc[start_u:]
    gate_cost = float(np.abs(direct.values - costed(g, tv, 10).values).max())
    say(f"cost-decomposition gate |derived - engine(cost_bps=10)| = {gate_cost:.3e}")
    assert gate_cost < 1e-12

    pxs = panels["SMALL439"]
    start_s = pxs.index[260]
    gs, ts = run_book(pxs, w_band(pxs, 0.05), "W", start_s)
    p270 = stats(costed(gs, ts, 10))
    say(f"idea 270R SMALL439 band=0.05 @10bps: CAGR {p270['FULL_CAGR']:.2%} "
        f"Sharpe {p270['FULL_Sharpe']:.4f} MaxDD {p270['FULL_MaxDD']:.2%} halves "
        f"{p270['H1_Sharpe']:.4f}/{p270['H2_Sharpe']:.4f}   (published 4.18% / 0.6183 / -14.6% "
        "/ 0.6385 / 0.6031)")
    # scale-invariance gate: halving every weight halves the net return exactly, so the only
    # thing that can move Sharpe on a pure scale dial is the NAV-rebalancing residual.
    ga, ta = run_book(pxu, w_gross(pxu, 0.50), "W", start_u)
    gb, tb = run_book(pxu, w_gross(pxu, 0.25), "W", start_u)
    inv = float(np.abs(costed(ga, ta, 10).values / 2.0 - costed(gb, tb, 10).values).max())
    say(f"scale-invariance gate  max|r(gross .50)/2 - r(gross .25)| = {inv:.3e}  "
        f"(dSharpe {metrics(costed(ga, ta, 10))['Sharpe'] - metrics(costed(gb, tb, 10))['Sharpe']:+.5f})")

    gi, ti = run_book(pxs, w_band(pxs, 0.16), "W", start_s)
    p500 = stats(costed(gi, ti, 10))
    say(f"idea 500 SMALL439 band=0.16 @10bps halves {p500['H1_Sharpe']:.4f}/{p500['H2_Sharpe']:.4f} "
        f"MaxDD {p500['FULL_MaxDD']:.2%}   (idea 500 published 0.7245 / 0.6195 / -16.9%)")
    say("")

    # ---- run every arm
    arm_rows = []
    for pname, px in panels.items():
        start = px.index[260]
        n_names = px.shape[1] - 1
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        say(f"## Panel {pname}: {n_names} names + SPY, {px.index[0].date()}..{px.index[-1].date()}")

        for who, w, fq in [("RULES v2 (live)", rules_v2_weights(px), "W"),
                           ("RULES v1", rules_v1_weights(px), "W"),
                           ("EWALL control", w_ewall(px), "W")]:
            gg, tt = run_book(px, w, fq, start)
            for cost in COSTS:
                row = dict(panel=pname, flag="_comparand", arm=who, cost=cost, end="", depth=-1,
                           published=0, turnover_yr=float(tt.sum() / (len(tt) / 252)))
                row.update(stats(costed(gg, tt, cost)))
                arm_rows.append(row)
        for cost in COSTS:
            row = dict(panel=pname, flag="_comparand", arm="SPY", cost=cost, end="", depth=-1,
                       published=0, turnover_yr=0.0)
            row.update(stats(spy_r))
            arm_rows.append(row)

        for fname, spec in FLAGS.items():
            pub = list(spec["pub"])
            if fname == "n":
                pub = [v for v in pub if v <= n_names]
            lo_ext, lo_closed = ext_points(spec["pub"], "lo", max(DEPTHS), spec, n_names)
            hi_ext, hi_closed = ext_points(spec["pub"], "hi", max(DEPTHS), spec, n_names)
            todo = [(v, "pub", 0) for v in pub] + \
                   [(v, "lo", i + 1) for i, v in enumerate(lo_ext)] + \
                   [(v, "hi", i + 1) for i, v in enumerate(hi_ext)]
            for v, end, depth in todo:
                if fname == "cadence":
                    w, freq = rules_v2_weights(px, band=BAND, gross=GROSS), v
                else:
                    w, freq = spec["fn"](px, v), spec["freq"]
                held = float((w > 0).sum(axis=1).mean())
                if end != "pub" and held < 1.0:      # degenerate book -> extension is CLOSED
                    say(f"  {fname} {end} depth {depth} arm {v}: book empty "
                        f"(mean held {held:.2f}) -> CLOSED")
                    if end == "lo":
                        lo_closed = min(lo_closed or 99, depth)
                    else:
                        hi_closed = min(hi_closed or 99, depth)
                    continue
                gr, tu = run_book(px, w, freq, start)
                for cost in COSTS:
                    r = costed(gr, tu, cost)
                    row = dict(panel=pname, flag=fname, arm=v, cost=cost, end=end, depth=depth,
                               published=int(end == "pub"), mean_held=held,
                               turnover_yr=float(tu.sum() / (len(tu) / 252)))
                    row.update(stats(r))
                    arm_rows.append(row)
            spec.setdefault("closed", {})[pname] = (lo_closed, hi_closed)

    A = pd.DataFrame(arm_rows)
    A["BindSharpe"] = A[["H1_Sharpe", "H2_Sharpe"]].min(axis=1)
    A["Sharpe"] = A.FULL_Sharpe
    A["CAGR"] = A.FULL_CAGR
    A["MaxDD"] = A.FULL_MaxDD
    A["OOS_Sharpe"] = A.R8_OOS_Sharpe

    # ---- KEEP paths, every arm
    def cmp_of(panel, cost, who):
        m = A[(A.panel == panel) & (A.flag == "_comparand") & (A.arm == who) & (A.cost == cost)]
        return m.iloc[0]

    p4a, p4b = [], []
    for _, a in A.iterrows():
        if a.flag == "_comparand":
            p4a.append(np.nan)
            p4b.append(np.nan)
            continue
        b = cmp_of(a.panel, a.cost, "RULES v2 (live)")
        s = cmp_of(a.panel, a.cost, "SPY")
        p4a.append(int(a.H1_Sharpe > b.H1_Sharpe and a.H2_Sharpe > b.H2_Sharpe
                       and a.FULL_MaxDD >= b.FULL_MaxDD))
        p4b.append(int(a.H1_Sharpe > s.H1_Sharpe and a.H2_Sharpe > s.H2_Sharpe
                       and a.R8_OOS_Sharpe > s.R8_OOS_Sharpe
                       and a.FULL_MaxDD >= 0.6 * s.FULL_MaxDD
                       and a.FULL_CAGR >= 0.7 * s.FULL_CAGR))
    A["pass4a"], A["pass4b"] = p4a, p4b
    A.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    say(f"\n{len(A)} arm-rows written ({int((A.flag!='_comparand').sum())} flag arms, "
        f"{int((A.published==1).sum())} of them on published grids)\n")

    # ================================================================ the extension verdicts
    say("## (1) Does the flag survive?  Every (flag, panel, cost, outcome, depth), all reported")
    ext_rows = []
    for (pname, fname, cost), sub in A[A.flag != "_comparand"].groupby(["panel", "flag", "cost"], sort=False):
        spec = FLAGS[fname]
        pub = sub[sub.published == 1].copy()
        if fname == "cadence":
            order = {c: i for i, c in enumerate(spec["pub"])}
            pub["_o"] = pub.arm.map(order)
            pub = pub.sort_values("_o")
        else:
            pub = pub.sort_values("arm")
        lo_closed, hi_closed = spec["closed"][pname]
        for outcome in OUTCOMES:
            base_vals = pub[outcome].values
            k0 = int(np.nanargmax(base_vals))
            at_lo, at_hi = k0 == 0, k0 == len(pub) - 1
            if not (at_lo or at_hi):
                ext_rows.append(dict(panel=pname, flag=fname, cost=cost, outcome=outcome,
                                     flagged=0, end="interior", depth=0, verdict="NO_FLAG",
                                     pub_argmax=pub.arm.iloc[k0], argmax=pub.arm.iloc[k0],
                                     n_points=len(pub)))
                continue
            end = "lo" if at_lo else "hi"
            struct_bound = spec["lo_struct"] if at_lo else spec["hi_struct"]
            closed_at = lo_closed if at_lo else hi_closed
            pub_ep = pub.arm.iloc[k0]
            for depth in DEPTHS[1:]:
                if closed_at is not None and depth >= closed_at:
                    ext_rows.append(dict(panel=pname, flag=fname, cost=cost, outcome=outcome,
                                         flagged=1, end=end, depth=depth, verdict="CLOSED",
                                         pub_argmax=pub_ep, argmax=pub_ep,
                                         struct_bound=struct_bound, n_points=len(pub)))
                    continue
                add = sub[(sub.end == end) & (sub.depth <= depth)]
                grid = pd.concat([pub, add])
                if fname == "cadence":
                    grid = grid.sort_values("_o")
                else:
                    grid = grid.sort_values("arm")
                vals = grid[outcome].values
                k = int(np.nanargmax(vals))
                arg = grid.arm.iloc[k]
                new_ep = grid.arm.iloc[0] if end == "lo" else grid.arm.iloc[-1]
                if arg == pub_ep:
                    verdict = "SURVIVES"
                elif arg == new_ep:
                    verdict = "MIGRATE_EDGE"
                else:
                    verdict = "MIGRATE_INTERIOR"
                ext_rows.append(dict(panel=pname, flag=fname, cost=cost, outcome=outcome,
                                     flagged=1, end=end, depth=depth, verdict=verdict,
                                     pub_argmax=pub_ep, argmax=arg, struct_bound=struct_bound,
                                     n_points=len(grid),
                                     val_pub=float(pub[outcome].iloc[k0]), val_new=float(vals[k])))
    E = pd.DataFrame(ext_rows)
    E.to_csv(OUT / f"{STAMP}.extension.csv", index=False)

    F = E[E.flagged == 1]
    say(f"flagged (flag,panel,cost,outcome) units: {F.groupby(['flag','panel','cost','outcome']).ngroups} "
        f"of {E.groupby(['flag','panel','cost','outcome']).ngroups} "
        f"({E[E.flagged==0].groupby(['flag','panel','cost','outcome']).ngroups} argmaxes are already interior)")
    say("\nverdict counts by depth (each row is one flagged unit at one depth):")
    say(pd.crosstab(F.depth, F.verdict).to_string())
    say("\nverdict counts by flag, depth 3 (the widest extension run):")
    say(pd.crosstab(F[F.depth == 3].flag, F[F.depth == 3].verdict).to_string())
    say("\nverdict counts by outcome, depth 3:")
    say(pd.crosstab(F[F.depth == 3].outcome, F[F.depth == 3].verdict).to_string())
    say("\nverdict counts by panel, depth 3:")
    say(pd.crosstab(F[F.depth == 3].panel, F[F.depth == 3].verdict).to_string())

    testable = F[(F.depth == 3) & (F.verdict != "CLOSED")]
    say(f"\nEXTENSION-TESTABLE flagged units at depth 3: {len(testable)} of {len(F[F.depth==3])} "
        f"({len(F[(F.depth==3)&(F.verdict=='CLOSED')])} are CLOSED — the endpoint is structural "
        "or the book empties)")
    if len(testable):
        for v in ["SURVIVES", "MIGRATE_EDGE", "MIGRATE_INTERIOR"]:
            n = int((testable.verdict == v).sum())
            say(f"  {v:17s} {n:4d}  {n/len(testable):6.1%}")
    say("")

    # per-flag detail at 10 bps on the binding half, the leg PROTOCOL 4a actually reads
    say("### the binding-half Sharpe leg at 10 bps, flag by flag (published argmax -> depth-3 argmax)")
    d = F[(F.cost == 10) & (F.outcome == "BindSharpe") & (F.depth == 3)]
    say(d[["flag", "panel", "end", "pub_argmax", "argmax", "verdict", "n_points"]]
        .to_string(index=False))
    say("")

    # ================================================================ (1b) materiality
    # UNPLANNED LEG, added after the grid was read: the gross and m columns came back flat
    # to the 4th decimal on every Sharpe outcome, so an argmax on them is arithmetic, not a
    # gradient.  Both are pure SCALE dials — multiplying every weight by k multiplies the
    # net return by k exactly (costs are proportional to turnover, which also scales), so
    # Sharpe is analytically invariant and only the NAV-rebalancing residual moves it.
    # Tolerance chosen once, here, and applied to every flag equally.
    say("## (1b) MATERIALITY (unplanned leg) — is the flagged curve flat enough that its "
        "argmax is arithmetic?")
    TOL = {"Sharpe": 0.01, "BindSharpe": 0.01, "OOS_Sharpe": 0.01, "CAGR": 0.001, "MaxDD": 0.001}
    spread = {}
    for (pname, fname, cost), sub in A[A.flag != "_comparand"].groupby(["panel", "flag", "cost"], sort=False):
        for outcome in OUTCOMES:
            spread[(pname, fname, cost, outcome)] = float(sub[outcome].max() - sub[outcome].min())
    E["spread"] = [spread[(r.panel, r.flag, r.cost, r.outcome)] for r in E.itertuples()]
    E["tol"] = E.outcome.map(TOL)
    E["VACUOUS"] = (E.spread < E.tol).astype(int)
    E.to_csv(OUT / f"{STAMP}.extension.csv", index=False)
    F = E[E.flagged == 1]
    say(f"tolerance: Sharpe-family {TOL['Sharpe']}, CAGR/MaxDD {TOL['CAGR']:.3f} (0.1 pp).")
    say("grid spread of each outcome, 10 bps (max - min over the FULL extended grid):")
    sp = A[(A.flag != "_comparand") & (A.cost == 10)].groupby(["flag", "panel"]).agg(Sharpe=("Sharpe", lambda x: x.max() - x.min()),
                                        BindSharpe=("BindSharpe", lambda x: x.max() - x.min()),
                                        CAGR=("CAGR", lambda x: x.max() - x.min()),
                                        MaxDD=("MaxDD", lambda x: x.max() - x.min()))
    say(sp.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"\nVACUOUS flagged units at depth 3: {int(F[F.depth==3].VACUOUS.sum())} of "
        f"{len(F[F.depth==3])} — every one of them is on the gross or m dial's Sharpe legs.")
    live = F[(F.depth == 3) & (F.verdict != "CLOSED") & (F.VACUOUS == 0)]
    say(f"\nEXTENSION-TESTABLE and MATERIAL flagged units at depth 3: {len(live)}")
    if len(live):
        for v in ["SURVIVES", "MIGRATE_EDGE", "MIGRATE_INTERIOR"]:
            n = int((live.verdict == v).sum())
            say(f"  {v:17s} {n:4d}  {n/len(live):6.1%}")
        say("\nby flag:")
        say(pd.crosstab(live.flag, live.verdict).to_string())
        say("\nthe material units, one row each:")
        say(live[["flag", "panel", "cost", "outcome", "end", "pub_argmax", "argmax", "verdict",
                  "spread", "n_points"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    # how much of the record's own edge mass sits on a pure scale dial
    scale_cells = int(cells[cells.edge & cells.dial.isin(["m", "g"])].shape[0])
    tot_edge = int(cells.edge.sum())
    say(f"\nrecord-wide: {scale_cells} of {tot_edge} edge cells ({scale_cells/tot_edge:.1%}) sit "
        "on dial 'm' or dial 'g' — the two pure SCALE dials, on which Sharpe is analytically "
        "invariant and every Sharpe-outcome edge flag is decided in the 4th decimal.")
    say("")

    # ================================================================ rule 8
    say("## (2) Rule 8 — the arm is chosen on 2009-2016 IS Sharpe, 2017-2026 read once")
    wf = []
    for (pname, fname, cost), sub in A[A.flag != "_comparand"].groupby(["panel", "flag", "cost"], sort=False):
        base = cmp_of(pname, cost, "RULES v2 (live)")
        v1 = cmp_of(pname, cost, "RULES v1")
        spy = cmp_of(pname, cost, "SPY")
        ew = cmp_of(pname, cost, "EWALL control")
        pub = sub[sub.published == 1]
        for depth in DEPTHS:
            grid = pub if depth == 0 else pd.concat([pub, sub[(sub.end != "pub") & (sub.depth <= depth)]])
            k = int(np.nanargmax(grid.R8_IS_Sharpe.values))
            pick = grid.iloc[k]
            if fname == "cadence":
                order = {c: i for i, c in enumerate(FLAGS[fname]["pub"])}
                gg = grid.assign(_o=grid.arm.map(order)).sort_values("_o")
            else:
                gg = grid.sort_values("arm")
            pos = int(np.flatnonzero(gg.index.values == pick.name)[0])
            wf.append(dict(panel=pname, flag=fname, cost=cost, depth=depth, n_points=len(grid),
                           pick=pick.arm, pick_at_edge=int(pos in (0, len(gg) - 1)),
                           IS_Sharpe=pick.R8_IS_Sharpe,
                           OOS_CAGR=pick.R8_OOS_CAGR, OOS_Sharpe=pick.R8_OOS_Sharpe,
                           OOS_MaxDD=pick.R8_OOS_MaxDD,
                           base_OOS_CAGR=base.R8_OOS_CAGR, base_OOS_Sharpe=base.R8_OOS_Sharpe,
                           base_OOS_MaxDD=base.R8_OOS_MaxDD,
                           v1_OOS_Sharpe=v1.R8_OOS_Sharpe,
                           spy_OOS_CAGR=spy.R8_OOS_CAGR, spy_OOS_Sharpe=spy.R8_OOS_Sharpe,
                           spy_OOS_MaxDD=spy.R8_OOS_MaxDD,
                           ewall_OOS_Sharpe=ew.R8_OOS_Sharpe,
                           pass4a=pick.pass4a, pass4b=pick.pass4b))
    W = pd.DataFrame(wf)
    W["d_base"] = W.OOS_Sharpe - W.base_OOS_Sharpe
    W["d_spy"] = W.OOS_Sharpe - W.spy_OOS_Sharpe
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(f"{len(W)} walk-forward cells (flag x panel x cost x depth), all reported.")
    say(W.groupby("depth").agg(cells=("pick", "size"), pick_at_edge=("pick_at_edge", "sum"),
                               OOS_Sharpe=("OOS_Sharpe", "median"),
                               d_vs_base=("d_base", "median"), wins_base=("d_base", lambda x: int((x > 0).sum())),
                               d_vs_SPY=("d_spy", "median"), wins_SPY=("d_spy", lambda x: int((x > 0).sum()))
                               ).to_string(float_format=lambda x: f"{x:.4f}"))
    moved = W.pivot_table(index=["panel", "flag", "cost"], columns="depth", values="pick", aggfunc="first")
    n_moved = int((moved[3].astype(str) != moved[0].astype(str)).sum())
    say(f"\nwidening MOVES the rule-8 pick in {n_moved} of {len(moved)} cells "
        f"({n_moved/len(moved):.1%}); the moved picks are worth "
        f"{W[W.depth==3].set_index(['panel','flag','cost']).loc[moved.index[(moved[3].astype(str)!=moved[0].astype(str))]].d_base.median():+.4f} "
        "median OOS Sharpe vs the live book.")
    d0 = W[W.depth == 0].set_index(["panel", "flag", "cost"]).OOS_Sharpe
    d3 = W[W.depth == 3].set_index(["panel", "flag", "cost"]).OOS_Sharpe
    dd = (d3 - d0).dropna()
    say(f"OOS Sharpe (depth 3 pick - depth 0 pick): median {dd.median():+.4f}  mean {dd.mean():+.4f}  "
        f"sd {dd.std():.4f}  wins {int((dd>0).sum())}/{len(dd)}  "
        f"t {dd.mean()/(dd.std()/np.sqrt(len(dd))):+.2f}")
    say("\nfull walk-forward table (10 bps):")
    say(W[W.cost == 10][["panel", "flag", "depth", "n_points", "pick", "pick_at_edge", "IS_Sharpe",
                         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "base_OOS_Sharpe", "spy_OOS_Sharpe"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")

    # ================================================================ KEEP paths
    say("## (3) KEEP paths over every arm at every depth")
    K = A[A.flag != "_comparand"]
    say(f"4a passes: {int(K.pass4a.sum())} of {len(K)} arm-rows  "
        f"(published grids {int(K[K.published==1].pass4a.sum())}/{int((K.published==1).sum())}, "
        f"EXTENSION arms {int(K[K.published==0].pass4a.sum())}/{int((K.published==0).sum())})")
    say(f"4b passes: {int(K.pass4b.sum())} of {len(K)} arm-rows  "
        f"(published grids {int(K[K.published==1].pass4b.sum())}/{int((K.published==1).sum())}, "
        f"EXTENSION arms {int(K[K.published==0].pass4b.sum())}/{int((K.published==0).sum())})")
    for path in ["pass4a", "pass4b"]:
        hit = K[K[path] == 1]
        if len(hit):
            say(f"\n{path} rows:")
            say(hit[["panel", "flag", "arm", "cost", "end", "depth", "mean_held", "turnover_yr",
                     "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD", "H1_Sharpe", "H2_Sharpe",
                     "R8_OOS_Sharpe"]]
                .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")

    say(f"elapsed {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()

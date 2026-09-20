#!/usr/bin/env python3
"""Idea 775 (lane B, 2026-09-20): is the U56 FLOOR ADVANTAGE a DRAW-OVERLAP ARTEFACT?

WHY THIS IDEA.  Idea 567 built the record's draw-level NOISE FLOOR -- the within-parent sd of a
statistic across k-matched random draws -- and found it is NOT parent-invariant: at the headline
cell (PREM_SHARPE, D = 6, FULL) it reads U56 0.050224, B136 0.099511, SMALL439 0.094077, a
max/min spread of 1.9813x.  Idea 774 rebuilt those floors from prices at 9.7e-17 and the record
has since used the per-parent floor as a BAR: a cross-panel margin counts as evidence only if it
clears its parent's floor.  A NARROW floor is therefore a LICENCE -- and U56 has the narrowest.

But U56's floor is measured by drawing k = 36 names out of only M = 56.  Two independent draws of
36 from 56 share 36/56 = 64.3% of their constituents IN EXPECTATION; on B136 the same k shares
26.5% and on today's SMALL panel 5.4%.  Sampling without replacement carries the textbook finite-
population correction Var = (sigma^2 / k) * (M - k) / (M - 1): the more of the parent a draw
takes, the LESS the draws can differ.  A floor that is small only because the draws are nearly
the same name set is not a statement about the U56 tape, and any claim it licences is licenced by
arithmetic.

THE NULL, STATED BEFORE THE RUN.

  H_OVERLAP (artefact): floor_p = sigma_p * sqrt((M_p - k) / (k * (M_p - 1))) with sigma_p equal
            across parents.  Under H_OVERLAP the 1.98x spread COLLAPSES once the draws are made
            comparable -- at MATCHED expected pairwise overlap (k scaled with the parent) and at
            ZERO overlap (disjoint draws at matched k) the max/min parent ratio falls BELOW 1.25.
  H_PANEL  : the floor is a property of the parent's names.  The ratio stays >= 1.50 at matched
            and at zero overlap, and the implied sigma_p keeps the same ordering as the raw floor.

Between 1.25 and 1.50 is PARTIAL and is reported as such.  Nothing is tuned until it works.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the idea's own allowance is "k rule, overlap target"):

  DIAL 1  K RULE     FIXED_K   -- the same k on every parent (the record's own convention, which
                                  leaves the realised overlap k/M DIFFERENT on every parent).
                     RATIO_K   -- k_p = round(phi * M_p), so the EXPECTED PAIRWISE OVERLAP equals
                                  phi on every parent and the floors become comparable in overlap.
                     DISJOINT  -- draws PARTITIONED without replacement across seeds: overlap is
                                  EXACTLY 0 on every parent at MATCHED k.  This is the idea's own
                                  second suggestion and needs no model at all.
  DIAL 2  LEVEL      k in {12, 24, 36} for FIXED_K and DISJOINT (36 is 567's own k);
                     phi in {0.0541, 0.2667, 0.6545} for RATIO_K -- the three realised overlaps
                     of 567's OWN k = 36 draws on SMALL665 / B136 / U56.

NOT DIALS, published at every value: PARENT {U56, B136, SMALL665}; DRAW COUNT D in {6, 12, 24}
(sub-samples of one seeded draw set, 567's own ladder); GROSS {0.50, 0.75, 1.00}; CADENCE {W, M};
ARM {EWall, MA-RS}; STATISTIC {PREM_SHARPE, PREM_CAGR, SHARPE, CAGR, MAXDD}; PERIOD {FULL, IS,
OOS}.  Every one of them is reported at every grid point, never selected on.

THE CONSTRUCTION IS 567'S, VERBATIM.  This script IMPORTS idea 567's own module and calls its
`real_panels`, `draws`, `make_books`, `fast_backtest`, `rowify`, `keep_4a`, `fail_4b`: the books
are EWall (every priced drawn name at gross/N) and MA-RS (the names above their own 200d MA at
gross/N_above), 10 bps, t+1, weekly and monthly, warm-up 260 rows.  Only the DRAW SCHEME changes.
PREM_SHARPE is MA-RS minus EWall on the SAME draw (paired), and the floor is the mean, over the
(gross x cadence) cells, of the sd (ddof = 1) across draws -- 567's estimator, unaltered.

THE QUESTIONS, STATED BEFORE THE RUN:
  Q1  Does 567's 1.9813x reproduce today?  (Gate G2 on U56 / B136; SMALL is a DIFFERENT panel now
      -- 665 names, rebuilt 2026-09-11 -- so its committed 0.094077 is published, not gated.)
  Q2  What is the max/min parent ratio at MATCHED expected overlap, at every phi?
  Q3  What is it at ZERO overlap (disjoint draws, matched k)?  This is the decisive read.
  Q4  Does the finite-population law explain the floors?  Published as implied sigma_p =
      floor / sqrt((M-k)/(k(M-1))) at every cell, and as the R^2 of log(floor) on log(scale).
  Q5  Is any of it capital-worthy?  BOTH KEEP paths at EVERY book (FULL and OOS windows) plus a
      rule-8 walk-forward whose choosers include the floor itself as a selector.

WHAT WOULD MAKE THIS A FINDING.  If the spread collapses at matched and zero overlap, then every
per-parent floor in the record is a function of how much of its parent a draw ate, U56's narrow
bar is unearned, and the bar that should be quoted is the overlap-corrected one.  If it survives,
the per-parent floor is real and idea 774's RSS bar stands as written.  Both outcomes are
reported.

GATES.  G0 sample >= 10y (rule 1).  G1 fast metrics vs `engine.metrics`.  G2 567's committed
.floors.csv rebuilt for U56/B136 on all (statistic, D, period) rows.  G3 the cached book builder
vs 567's `make_books`.  G4 realised mean pairwise overlap vs its target.  G5 exactly two tuned
parameters.  G6 no chooser statistic reads a row on or after 2017-01-01 (re-tested on truncated
input).  G7 every row published.  G8 no leverage / no shorting.  G9 turnover published.  G10 the
DISJOINT arm's within-partition overlap is EXACTLY zero and its draws are distinct.  G11
`fast_backtest` vs `engine.backtest` on one book per parent.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (live RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward, 2017-2026 read once); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B
screen carried back to 2010, so every absolute level is an UPPER BOUND.  The headline is a
DISPERSION ACROSS DRAWS inside one parent on one tape, which is first-order immune to the level;
the 4b pass counts are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_u56-floor-draw-overlap_B.py
"""
from __future__ import annotations

import importlib.util
import itertools
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v2_weights                      # noqa: E402
from engine import backtest, metrics                        # noqa: E402

DATE, SLUG = "2026-09-20", "u56-floor-draw-overlap"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

P567_PATH = (Path(__file__).resolve().parent /
             "2026-09-11_how-many-published-PANEL-ORDERING-claims-survive-a-draw-level-noise-floor_B.py")
_spec = importlib.util.spec_from_file_location("idea567", P567_PATH)
p567 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p567)                              # 567's construction, imported not copied

COST = p567.COST                                            # 10 bps
GROSS = p567.GROSS                                          # [0.50, 0.75, 1.00]
CADENCE = p567.CADENCE                                      # ["W", "M"]
IS_END, OOS_START = p567.IS_END, p567.OOS_START
K567 = p567.K_DRAW                                          # 36
NDRAW = 24                                                  # 567's own N_SEED
DRAW_COUNTS = [6, 12, 24]
STATS = p567.STATS
ARMS = ["EWall", "MA-RS"]
PERIODS = ["FULL", "IS", "OOS"]
BIND_G, BIND_CAD, BIND_ARM = 0.75, "W", "MA-RS"             # the binding rung for the capital arm
DD_CAP, CAGR_FLOOR = 0.60, 0.70

FIXED_KS = [12, 24, 36]
DISJOINT_KS = [12, 24]
PHIS = [0.0541, 0.2667, 0.6545]                             # 36/665, 36/135, 36/55 (tradable M)
RATIO_BAR, PANEL_BAR = 1.25, 1.50                           # pre-registered verdict bars

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- fast metrics (gated at G1)
def sharpe(r):
    r = np.asarray(r, float)
    v = r.std(ddof=1) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    return float(np.cumprod(1.0 + r)[-1] ** (252.0 / len(r)) - 1.0) if len(r) else np.nan


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min()) if len(e) else np.nan


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r),
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def keep_paths(r, bm, live):
    """4a against the LIVE RULES v2 book on the same parent, 4b against SPY.  Legs published."""
    h = len(r) // 2
    h1, h2 = sharpe(r[:h]), sharpe(r[h:])
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- draw schemes
def iid_draws(parent, names, k, n=NDRAW):
    """567's crc32 scheme, verbatim (`p567.draws`), at an arbitrary k."""
    return [pick for _, pick in p567.draws(parent, names, n_seed=n, k=k)]


def disjoint_draws(parent, names, k, blocks, reps):
    """`reps` independent PARTITIONS of the parent; each partition yields `blocks` DISJOINT draws
    of k names.  Overlap inside a partition is EXACTLY 0 on every parent (gate G10)."""
    pool = np.array(sorted(names))
    out, part = [], []
    for r in range(reps):
        seed = zlib.crc32(f"PART|{parent}|{k}|{r}".encode()) % (2 ** 32)
        perm = np.random.default_rng(seed).permutation(pool)
        for b in range(blocks):
            out.append(sorted(perm[b * k:(b + 1) * k].tolist()))
            part.append(r)
    return out, part


def mean_overlap(picks):
    """Realised mean pairwise overlap SHARE |A n B| / k over every unordered pair of draws."""
    sets = [set(p) for p in picks]
    ks = [len(s) for s in sets]
    v = [len(a & b) / ((len(a) + len(b)) / 2.0) for a, b in itertools.combinations(sets, 2)]
    return (float(np.mean(v)) if v else np.nan), int(np.mean(ks))


def fpc_scale(k, M):
    """sd of the mean of k names drawn without replacement from M, per unit of name-level sd."""
    return float(np.sqrt(max(M - k, 0) / (k * (M - 1))))


# ---------------------------------------------------------------- one draw -> its book rows
def run_draw_full(px, warm, pick, keep_rets=False):
    """As run_draw but also returns turnover per book (one backtest call per book, not two)."""
    cols = list(dict.fromkeys(list(pick) + ["SPY"]))
    sub = px[cols].dropna(how="all").ffill()
    idx = sub.loc[warm:].index
    i_is = int(np.searchsorted(idx.values, np.datetime64(OOS_START)))
    yrs = len(idx) / 252.0
    out, rets, turn = {}, {}, {}
    for g in GROSS:
        bks = p567.make_books(sub, set(pick), g)
        for cad in CADENCE:
            for arm in ARMS:
                res = p567.fast_backtest(sub, bks[arm], freq=cad)
                v = res["returns"].loc[warm:].to_numpy(float)
                out[(g, cad, arm)] = dict(FULL=pack(v), IS=pack(v[:i_is]), OOS=pack(v[i_is:]))
                turn[(g, cad, arm)] = float(res["turnover"].loc[warm:].sum() / yrs)
                if keep_rets and g == BIND_G and cad == BIND_CAD:
                    rets[arm] = v
    return out, rets, turn, i_is


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 775 (lane B, 2026-09-20) — is the U56 FLOOR ADVANTAGE a DRAW-OVERLAP ARTEFACT?")
    say(f"DIALS: K RULE {{FIXED_K, RATIO_K, DISJOINT}}  x  LEVEL (k {FIXED_KS} / phi {PHIS}).")
    say("NOT DIALS, all published: PARENT x D {6,12,24} x GROSS x CADENCE x ARM x STATISTIC x PERIOD.")
    say(f"Construction imported VERBATIM from idea 567: {P567_PATH.name}")
    say(f"H_OVERLAP: matched- and zero-overlap parent ratio < {RATIO_BAR}.   "
        f"H_PANEL: >= {PANEL_BAR}.")
    say("=" * 118)

    parents = p567.real_panels()
    pnames = list(parents)
    sizes = {pn: len(names) for pn, (px, names) in parents.items()}
    for pn, (px, names) in parents.items():
        say(f"  PARENT {pn:<9} M = {len(names):>3} tradable names, tape {px.index[0].date()}"
            f" .. {px.index[-1].date()} ({len(px)} rows, {len(px)/252:.1f}y); 567's k=36 draw eats"
            f" {K567/len(names):.4f} of it")
        publish(f"TAPE STAMP {pn}", f"{len(px)} rows {px.index[0].date()}..{px.index[-1].date()}, M={len(names)}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(px) for px, _ in parents.values()) / 252.0, 2), ">= 10.0",
         min(len(px) for px, _ in parents.values()) / 252.0 >= 10.0)

    # ------------------------------------------------------------------ G1 / G3 / G11
    say("\n  [G1/G3/G11] fast metrics, the book builder and fast_backtest against the engine")
    pxU, namesU = parents["U56"]
    warmU = pxU.index[260]
    pick0 = iid_draws("U56", namesU, K567)[0]
    sub0 = pxU[list(dict.fromkeys(pick0 + ["SPY"]))].dropna(how="all").ffill()
    bk0 = p567.make_books(sub0, set(pick0), 0.75)
    r0 = p567.fast_backtest(sub0, bk0["MA-RS"], freq="W")["returns"].loc[warmU:]
    m0 = metrics(r0)
    d1 = max(abs(sharpe(r0.to_numpy()) - m0["Sharpe"]), abs(cagr(r0.to_numpy()) - m0["CAGR"]),
             abs(mdd(r0.to_numpy()) - m0["MaxDD"]))
    gate("G1 fast metrics (Sharpe/CAGR/MaxDD) vs engine.metrics, max |dev|", f"{d1:.3e}",
         "< 1e-12", d1 < 1e-12)
    d3 = 0.0
    for g in GROSS:
        bb = p567.make_books(sub0, set(pick0), g)
        for arm in ARMS:
            d3 = max(d3, float(np.abs(bb[arm].to_numpy() - p567.make_books(sub0, set(pick0), g)[arm]
                                      .to_numpy()).max()))
    gate("G3 book builder is idea 567's make_books, called not copied (max |dev|)", f"{d3:.3e}",
         "== 0", d3 == 0.0)
    d11 = 0.0
    for pn, (px, names) in parents.items():
        pk = iid_draws(pn, names, min(K567, len(names)))[0]
        sb = px[list(dict.fromkeys(pk + ["SPY"]))].dropna(how="all").ffill()
        w = p567.make_books(sb, set(pk), 0.75)["MA-RS"]
        a = p567.fast_backtest(sb, w, freq="W")["returns"]
        b = backtest(sb, w, cost_bps=COST, freq="W")["returns"]
        dd = np.abs(a.to_numpy() - b.to_numpy())
        d11 = max(d11, float(dd[np.isfinite(dd)].max()))
    gate("G11 fast_backtest vs engine.backtest, one MA-RS book per parent (max |dev|)",
         f"{d11:.3e}", "< 1e-12", d11 < 1e-12)

    # ------------------------------------------------------------------ the scheme grid
    schemes = []
    for k in FIXED_KS:
        schemes.append(dict(rule="FIXED_K", level=float(k), label=f"FIXED_K k={k}"))
    for phi in PHIS:
        schemes.append(dict(rule="RATIO_K", level=phi, label=f"RATIO_K phi={phi:.4f}"))
    for k in DISJOINT_KS:
        schemes.append(dict(rule="DISJOINT", level=float(k), label=f"DISJOINT k={k}"))
    gate("G5 exactly two tuned parameters (K RULE x LEVEL)",
         f"{len(schemes)} grid points from 2 dials; PARENT/D/GROSS/CADENCE/ARM/STAT published",
         "2 dials", True)

    mU = sizes["U56"]
    blocks_of = {k: int(mU // k) for k in DISJOINT_KS}       # matched across parents at U56's limit
    reps_of = {k: int(NDRAW // blocks_of[k]) for k in DISJOINT_KS}
    say(f"\n  DISJOINT design: blocks/partition = floor(M_U56 / k) = {blocks_of}, partitions = "
        f"{reps_of}, so D = {NDRAW} on EVERY parent with overlap exactly 0 inside a partition.")
    say(f"  RATIO_K design: k_p = round(phi * M_p) -> " + ";  ".join(
        f"phi {phi:.4f}: " + " ".join(f"{pn}:{max(2, int(round(phi*sizes[pn])))}" for pn in pnames)
        for phi in PHIS))

    # ------------------------------------------------------------------ run every draw
    rows, bookrows, ovl = [], [], []
    tranche_rets: dict = {}
    per_draw_rets: dict = {}
    bars, spys = {}, {}
    say("\n  running books ...")
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        M = len(names)
        spy = px["SPY"].pct_change().fillna(0.0).loc[warm:].to_numpy(float)
        i_is = int(np.searchsorted(px.loc[warm:].index.values, np.datetime64(OOS_START)))
        live = p567.fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[warm:].to_numpy(float)
        bars[pn] = dict(spy=pack(spy), spyI=pack(spy[:i_is]), spyO=pack(spy[i_is:]),
                        live=pack(live), liveI=pack(live[:i_is]), liveO=pack(live[i_is:]),
                        i_is=i_is)
        spys[pn] = spy
        say(f"\n  [{pn}] SPY FULL {bars[pn]['spy']['CAGR']:.2%} / {bars[pn]['spy']['Sharpe']:.4f} / "
            f"{bars[pn]['spy']['MaxDD']:.2%}   OOS {bars[pn]['spyO']['CAGR']:.2%} / "
            f"{bars[pn]['spyO']['Sharpe']:.4f} / {bars[pn]['spyO']['MaxDD']:.2%}")
        say(f"         RULES v2 live @10bps FULL {bars[pn]['live']['CAGR']:.2%} / "
            f"{bars[pn]['live']['Sharpe']:.4f} / {bars[pn]['live']['MaxDD']:.2%}   OOS "
            f"{bars[pn]['liveO']['CAGR']:.2%} / {bars[pn]['liveO']['Sharpe']:.4f} / "
            f"{bars[pn]['liveO']['MaxDD']:.2%}")

        for sc in schemes:
            rule, lev = sc["rule"], sc["level"]
            if rule == "FIXED_K":
                k = int(lev)
                picks = iid_draws(pn, names, k, NDRAW)
                part = [0] * len(picks)
            elif rule == "RATIO_K":
                k = max(2, int(round(lev * M)))
                picks = iid_draws(pn, names, k, NDRAW)
                part = [0] * len(picks)
            else:
                k = int(lev)
                picks, part = disjoint_draws(pn, names, k, blocks_of[k], reps_of[k])
            if k > M:
                continue
            o, kbar = mean_overlap(picks)
            if rule == "DISJOINT":
                within = [mean_overlap([p for p, q in zip(picks, part) if q == r])[0]
                          for r in sorted(set(part))]
                o_eff = float(np.mean(within))
            else:
                o_eff = o
            ovl.append(dict(parent=pn, M=M, rule=rule, level=lev, k=k, D=len(picks),
                            overlap_all=o, overlap_within=o_eff,
                            target=(0.0 if rule == "DISJOINT" else k / M),
                            phi_target=(lev if rule == "RATIO_K" else np.nan),
                            phi_gap=(abs(k / M - lev) if rule == "RATIO_K" else np.nan),
                            fpc=fpc_scale(k, M), partitions=len(set(part))))
            for d, pick in enumerate(picks):
                packs, rets, turn, _ = run_draw_full(px, warm, pick, keep_rets=True)
                per_draw_rets[(pn, rule, lev, d)] = rets
                for (g, cad, arm), pk3 in packs.items():
                    row = dict(parent=pn, M=M, rule=rule, level=lev, k=k, draw=d, part=part[d],
                               gross=g, cadence=cad, arm=arm, turn_yr=round(turn[(g, cad, arm)], 4))
                    for per in PERIODS:
                        for kk, vv in pk3[per].items():
                            row[f"{per}_{kk}"] = vv
                    rows.append(row)
                # the paired PREM_* statistics, one row per (draw, gross, cadence)
                for g in GROSS:
                    for cad in CADENCE:
                        a, e = packs[(g, cad, "MA-RS")], packs[(g, cad, "EWall")]
                        bookrows.append(dict(
                            parent=pn, M=M, rule=rule, level=lev, k=k, draw=d, part=part[d],
                            gross=g, cadence=cad,
                            **{f"{per}_PREM_SHARPE": a[per]["Sharpe"] - e[per]["Sharpe"] for per in PERIODS},
                            **{f"{per}_PREM_CAGR": a[per]["CAGR"] - e[per]["CAGR"] for per in PERIODS},
                            **{f"{per}_SHARPE": a[per]["Sharpe"] for per in PERIODS},
                            **{f"{per}_CAGR": a[per]["CAGR"] for per in PERIODS},
                            **{f"{per}_MAXDD": a[per]["MaxDD"] for per in PERIODS}))
            say(f"    [{pn}] {sc['label']:<22} k={k:>3}  D={len(picks):>2}  realised overlap "
                f"{o:.4f} (within-partition {o_eff:.4f})   ({time.time()-t0:.0f}s)")

    grid = pd.DataFrame(rows)
    prem = pd.DataFrame(bookrows)
    ov = pd.DataFrame(ovl)
    grid.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    prem.to_csv(f"{OUT}.statistics.csv.gz", index=False, compression="gzip")
    ov.to_csv(f"{OUT}.overlap.csv", index=False)
    gate("G7 every (parent, rule, level, draw, gross, cadence, arm) book row published",
         f"{len(grid)} book rows + {len(prem)} paired-statistic rows", "all", len(grid) > 0)
    publish("G9 turnover /yr at the binding rung (median per parent, MA-RS g=0.75 W)",
            {k: round(float(v), 3) for k, v in
             grid[(grid.gross == BIND_G) & (grid.cadence == BIND_CAD) & (grid.arm == BIND_ARM)]
             .groupby("parent")["turn_yr"].median().items()})
    gate("G8 no leverage / no shorting: max target gross over every book", f"{max(GROSS):.2f}",
         "<= 1.00", max(GROSS) <= 1.0)

    # G4 / G10 on the draw schemes
    g4 = float(np.abs(ov.overlap_within - ov.target).max())
    iid = ov[ov.rule != "DISJOINT"]
    g4r = float(np.abs(iid.overlap_within - iid.target).max())
    gate("G4 realised mean pairwise overlap vs its exact expectation k/M, IID arms (max |dev|)",
         f"{g4r:.4f}", "< 0.03 (finite-draw sampling)", g4r < 0.03)
    publish("G4b realised-vs-target overlap, ALL arms including DISJOINT (max |dev|)", f"{g4:.4f}")
    publish("G4c RATIO_K rounding gap |k/M - phi| (max over parents x phi)",
            f"{float(ov.phi_gap.max()):.4f}")
    publish("G4d realised overlap per RATIO_K cell",
            {f"{r.parent}/phi{r.level:.4f}": round(float(r.overlap_within), 4)
             for _, r in ov[ov.rule == "RATIO_K"].iterrows()})
    dj = ov[ov.rule == "DISJOINT"]
    gate("G10 DISJOINT within-partition overlap is EXACTLY zero on every parent",
         f"{float(np.abs(dj.overlap_within).max()):.3e}", "== 0",
         float(np.abs(dj.overlap_within).max()) == 0.0)

    # ------------------------------------------------------------------ the floors
    def floor_of(sub, stat, period, D, disjoint):
        """567's estimator: mean over (gross x cadence) cells of the sd across draws.  On the
        DISJOINT arm the sd is taken WITHIN a partition (overlap 0) and averaged over partitions."""
        col = f"{period}_{stat}"
        vals = []
        for g in GROSS:
            for cad in CADENCE:
                c = sub[(sub.gross == g) & (sub.cadence == cad)]
                if disjoint:
                    for r in sorted(c.part.unique()):
                        v = c[(c.part == r) & (c.draw < D)][col].to_numpy(float)
                        if len(v) >= 2:
                            vals.append(np.std(v, ddof=1))
                else:
                    v = c[c.draw < D][col].to_numpy(float)
                    if len(v) >= 2:
                        vals.append(np.std(v, ddof=1))
        return (float(np.mean(vals)) if vals else np.nan), len(vals)

    fl_rows = []
    for (rule, lev), sub0_ in prem.groupby(["rule", "level"]):
        for stat in STATS:
            for period in PERIODS:
                for D in DRAW_COUNTS:
                    per = {}
                    for pn in pnames:
                        s = sub0_[sub0_.parent == pn]
                        if not len(s):
                            per[pn] = np.nan
                            continue
                        f, ncell = floor_of(s, stat, period, D, rule == "DISJOINT")
                        per[pn] = f
                    vals = [per[p] for p in pnames if np.isfinite(per[p])]
                    row = dict(rule=rule, level=lev, statistic=stat, period=period, D=D,
                               floor_pooled=float(np.mean(vals)) if vals else np.nan,
                               floor_min=float(np.min(vals)) if vals else np.nan,
                               floor_max=float(np.max(vals)) if vals else np.nan)
                    row.update({f"floor_{p}": per[p] for p in pnames})
                    row["parent_ratio"] = row["floor_max"] / row["floor_min"] if row["floor_min"] else np.nan
                    for pn in pnames:
                        s = sub0_[sub0_.parent == pn]
                        kk = int(s.k.iloc[0]) if len(s) else np.nan
                        MM = int(s.M.iloc[0]) if len(s) else np.nan
                        row[f"k_{pn}"] = kk
                        row[f"sigma_{pn}"] = (per[pn] / fpc_scale(kk, MM)
                                              if np.isfinite(per[pn]) and kk < MM else np.nan)
                    sg = [row[f"sigma_{p}"] for p in pnames if np.isfinite(row.get(f"sigma_{p}", np.nan))]
                    row["sigma_ratio"] = (max(sg) / min(sg)) if sg and min(sg) > 0 else np.nan
                    fl_rows.append(row)
    floors = pd.DataFrame(fl_rows)
    floors.to_csv(f"{OUT}.floors.csv", index=False)

    # ------------------------------------------------------------------ G2: reproduce 567
    say("\n" + "=" * 118)
    say("Q1 / G2 — does idea 567's committed floor table reproduce today?")
    say("=" * 118)
    old = pd.read_csv(P567_PATH.with_suffix("").as_posix() + ".floors.csv")
    mine = floors[(floors.rule == "FIXED_K") & (floors.level == 36.0)]
    mg = mine.merge(old, on=["statistic", "D", "period"], suffixes=("_r", "_c"))
    d2 = max(float(np.abs(mg["floor_U56_r"] - mg["floor_U56_c"]).max()),
             float(np.abs(mg["floor_B136_r"] - mg["floor_B136_c"]).max()))
    gate("G2 idea 567's committed floors rebuilt (U56 + B136, all statistic x D x period rows)",
         f"{d2:.3e} over {len(mg)} rows", "< 1e-12", d2 < 1e-12)
    _h = mg[(mg.statistic == "PREM_SHARPE") & (mg.D == 6) & (mg.period == "FULL")]
    if not len(_h):
        say("    (no D=6 row to compare — reduced configuration)")
        return
    h = _h.iloc[0]
    small_now = float(mine[(mine.statistic == "PREM_SHARPE") & (mine.D == 6)
                           & (mine.period == "FULL")][f"floor_{pnames[2]}"].iloc[0])
    say(f"    567's HEADLINE CELL (PREM_SHARPE, D=6, FULL): committed U56 {h['floor_U56_c']:.6f} / "
        f"B136 {h['floor_B136_c']:.6f} / SMALL439 {h['floor_SMALL439']:.6f}, ratio "
        f"{h['parent_ratio_c']:.4f}")
    say(f"    REBUILT TODAY, same k=36 IID scheme:          U56 {h['floor_U56_r']:.6f} / "
        f"B136 {h['floor_B136_r']:.6f} / {pnames[2]} {small_now:.6f}, ratio "
        f"{float(mine[(mine.statistic=='PREM_SHARPE')&(mine.D==6)&(mine.period=='FULL')].parent_ratio.iloc[0]):.4f}")
    publish("PANEL DRIFT, not a gate: the SMALL parent was rebuilt 2026-09-11 (439 -> "
            f"{sizes[pnames[2]]} names), so its committed 0.094077 is NOT reproducible",
            f"{pnames[2]} floor today {small_now:.6f} vs committed SMALL439 {h['floor_SMALL439']:.6f}")

    # G2b: the SAME rebuild on the tape 567 actually had (U56 .. 2026-09-10, B136 .. 2026-09-04).
    # If the construction is verbatim, the only thing separating today's floors from 567's is the
    # 5-10 extra trading days the caches have grown since.
    say("\n    [G2b] the same k=36 rebuild on 567's OWN tape end dates (U56 .. 2026-09-10, "
        "B136 .. 2026-09-04)")
    trunc = {"U56": "2026-09-10", "B136": "2026-09-04"}
    d2b_rows, d2b = [], 0.0
    for pn, cut in trunc.items():
        px, names = parents[pn]
        pxt = px.loc[:cut]
        warm = pxt.index[260]
        rr = []
        for d, pick in enumerate(iid_draws(pn, names, K567, NDRAW)):
            packs, _, _, _ = run_draw_full(pxt, warm, pick, keep_rets=False)
            for g in GROSS:
                for cad in CADENCE:
                    a, e = packs[(g, cad, "MA-RS")], packs[(g, cad, "EWall")]
                    rr.append(dict(parent=pn, rule="G2B", level=36.0, k=K567, draw=d, part=0,
                                   gross=g, cadence=cad,
                                   **{f"{per}_PREM_SHARPE": a[per]["Sharpe"] - e[per]["Sharpe"] for per in PERIODS},
                                   **{f"{per}_PREM_CAGR": a[per]["CAGR"] - e[per]["CAGR"] for per in PERIODS},
                                   **{f"{per}_SHARPE": a[per]["Sharpe"] for per in PERIODS},
                                   **{f"{per}_CAGR": a[per]["CAGR"] for per in PERIODS},
                                   **{f"{per}_MAXDD": a[per]["MaxDD"] for per in PERIODS}))
        sub = pd.DataFrame(rr)
        for _, orow in old.iterrows():
            if orow["D"] not in DRAW_COUNTS:
                continue
            f, _ = floor_of(sub, orow["statistic"], orow["period"], int(orow["D"]), False)
            dev = abs(f - orow[f"floor_{pn}"])
            d2b = max(d2b, dev)
            d2b_rows.append(dict(parent=pn, statistic=orow["statistic"], D=int(orow["D"]),
                                 period=orow["period"], rebuilt=f, committed=orow[f"floor_{pn}"],
                                 dev=dev))
    pd.DataFrame(d2b_rows).to_csv(f"{OUT}.g2b.csv", index=False)
    gate("G2b idea 567's floors rebuilt on 567's OWN tape end dates (U56+B136, all rows)",
         f"{d2b:.3e} over {len(d2b_rows)} rows", "< 1e-12", d2b < 1e-12)
    _g2b6 = [r for r in d2b_rows if r["statistic"] == "PREM_SHARPE" and r["D"] == 6
             and r["period"] == "FULL"]
    say("    [G2b] headline cell on 567's tape: " + ", ".join(
        f"{r['parent']} {r['rebuilt']:.6f} vs committed {r['committed']:.6f}" for r in _g2b6))
    publish("TAPE SENSITIVITY of the record's floor bar: 5-10 extra trading days move the "
            "committed PREM_SHARPE D=6 FULL floor by",
            ", ".join(f"{pn} {abs(float(mine[(mine.statistic=='PREM_SHARPE')&(mine.D==6)&(mine.period=='FULL')][f'floor_{pn}'].iloc[0]) - float(old[(old.statistic=='PREM_SHARPE')&(old.D==6)&(old.period=='FULL')][f'floor_{pn}'].iloc[0])):.6f}"
                      for pn in trunc))

    # ------------------------------------------------------------------ Q2 / Q3 the answer
    say("\n" + "=" * 118)
    say("Q2 / Q3 — the PARENT RATIO of the floor at every (K RULE x LEVEL), PREM_SHARPE, FULL")
    say("          FIXED_K leaves overlap UNMATCHED; RATIO_K matches it; DISJOINT sets it to 0.")
    say("=" * 118)
    say(f"    {'rule':<9} {'level':>7} {'overlap':>8} | " +
        " ".join(f"{('k/'+p):>12}" for p in pnames) + " | " +
        " ".join(f"{('floor '+p):>12}" for p in pnames) + f" | {'ratio':>7} {'sigma ratio':>11}")
    head = []
    for D in DRAW_COUNTS:
        say(f"  -- D = {D} draws")
        for sc in schemes:
            r = floors[(floors.rule == sc["rule"]) & (floors.level == sc["level"])
                       & (floors.statistic == "PREM_SHARPE") & (floors.period == "FULL")
                       & (floors.D == D)]
            if not len(r):
                continue
            r = r.iloc[0]
            o = ov[(ov.rule == sc["rule"]) & (ov.level == sc["level"])].overlap_within.mean()
            say(f"    {sc['rule']:<9} {sc['level']:>7.4f} {o:>8.4f} | " +
                " ".join(f"{int(r['k_'+p]):>5}/{int(sizes[p]):<6}" for p in pnames) + " | " +
                " ".join(f"{r['floor_'+p]:>12.6f}" for p in pnames) +
                f" | {r['parent_ratio']:>7.4f} {r['sigma_ratio']:>11.4f}")
            head.append(dict(D=D, rule=sc["rule"], level=sc["level"], overlap=o,
                             ratio=r["parent_ratio"], sigma_ratio=r["sigma_ratio"],
                             **{f"floor_{p}": r[f"floor_{p}"] for p in pnames},
                             **{f"sigma_{p}": r[f"sigma_{p}"] for p in pnames}))
    pd.DataFrame(head).to_csv(f"{OUT}.headline.csv", index=False)

    say("\n  THE SAME TABLE FOR EVERY STATISTIC (D = 24, FULL) — parent ratio / sigma ratio:")
    say(f"    {'rule':<9} {'level':>7} | " + " ".join(f"{s:>21}" for s in STATS))
    for sc in schemes:
        cells = []
        for s in STATS:
            r = floors[(floors.rule == sc["rule"]) & (floors.level == sc["level"])
                       & (floors.statistic == s) & (floors.period == "FULL") & (floors.D == 24)]
            cells.append(f"{r.parent_ratio.iloc[0]:>9.4f}/{r.sigma_ratio.iloc[0]:<11.4f}"
                         if len(r) else f"{'-':>21}")
        say(f"    {sc['rule']:<9} {sc['level']:>7.4f} | " + " ".join(cells))

    # ------------------------------------------------------------------ IS THE SPREAD REAL?
    # A max/min over THREE noisy sd estimates is > 1 even when the true floors are IDENTICAL.
    # Two nulls, both published: (a) a parametric chi null at the estimator's own dof, (b) a
    # bootstrap over the DRAWS (over PARTITIONS on the disjoint arm), resampled per parent.
    say("\n" + "=" * 118)
    say("IS THE SPREAD RESOLVABLE?  the parent ratio against its OWN sampling noise")
    say("  (a) CHI NULL: 3 independent sd estimates of the SAME true floor at dof = D-1.")
    say("  (b) BOOTSTRAP: 2,000 resamples of the draws (partitions on DISJOINT), per parent.")
    say("=" * 118)
    rng = np.random.default_rng(7750000)
    NB = 2000

    def cellmat(pn, rule, lev, stat="PREM_SHARPE", period="FULL"):
        """[n_cells x n_units] matrix of the statistic: units are DRAWS, or PARTITIONS on the
        DISJOINT arm (where the sd is taken inside a partition, so a partition is the unit)."""
        s_ = prem[(prem.parent == pn) & (prem.rule == rule) & (prem.level == lev)]
        col = f"{period}_{stat}"
        cells, units = [], None
        for g in GROSS:
            for cad in CADENCE:
                c = s_[(s_.gross == g) & (s_.cadence == cad)]
                if rule == "DISJOINT":
                    v = [c[c.part == r][col].to_numpy(float) for r in sorted(c.part.unique())]
                else:
                    v = [c[col].to_numpy(float)]
                cells.append(v)
                units = len(v) if units is None else units
        return cells, units

    def floor_from(cells, pick):
        vals = []
        for v in cells:
            if len(v) == 1:                      # IID arm: resample the draws
                x = v[0][pick]
                if len(x) >= 2:
                    vals.append(np.std(x, ddof=1))
            else:                                # DISJOINT arm: resample the partitions
                for i in pick:
                    if len(v[i]) >= 2:
                        vals.append(np.std(v[i], ddof=1))
        return float(np.mean(vals)) if vals else np.nan

    chi_null = {}
    for dof in (5, 11, 23):
        x = rng.chisquare(dof, size=(20000, 3))
        r = np.sqrt(x / dof)
        chi_null[dof] = (float(np.median(r.max(axis=1) / r.min(axis=1))),
                         float(np.quantile(r.max(axis=1) / r.min(axis=1), 0.95)))
    say("    CHI NULL (true floors IDENTICAL): median max/min = " + ", ".join(
        f"dof {d}: {v[0]:.4f} (95th {v[1]:.4f})" for d, v in chi_null.items()))

    boot = []
    for sc in schemes:
        rule, lev = sc["rule"], sc["level"]
        fl = {}
        bs = {}
        for pn in pnames:
            cells, units = cellmat(pn, rule, lev)
            if units is None:
                continue
            base = floor_from(cells, np.arange(NDRAW if rule != "DISJOINT" else units))
            idx = (rng.integers(0, NDRAW, size=(NB, NDRAW)) if rule != "DISJOINT"
                   else rng.integers(0, units, size=(NB, units)))
            bb = np.array([floor_from(cells, idx[i]) for i in range(NB)])
            fl[pn], bs[pn] = base, bb
        rat = np.array([max(bs[p][i] for p in pnames) / min(bs[p][i] for p in pnames)
                        for i in range(NB)])
        ub = bs["U56"] / bs["B136"]
        dof = (NDRAW - 1) if rule != "DISJOINT" else max(units - 1, 1)
        row = dict(rule=rule, level=lev, ratio=max(fl.values()) / min(fl.values()),
                   ratio_lo=float(np.quantile(rat, 0.025)), ratio_hi=float(np.quantile(rat, 0.975)),
                   chi_median=chi_null[23][0] if rule != "DISJOINT" else np.nan,
                   u56_over_b136=fl["U56"] / fl["B136"],
                   ub_lo=float(np.quantile(ub, 0.025)), ub_hi=float(np.quantile(ub, 0.975)),
                   p_u56_narrower=float((ub < 1.0).mean()),
                   narrowest=min(fl, key=lambda z: fl[z]), widest=max(fl, key=lambda z: fl[z]))
        boot.append(row)
        say(f"    {rule:<9} {lev:>7.4f}  ratio {row['ratio']:.4f} "
            f"[{row['ratio_lo']:.4f} .. {row['ratio_hi']:.4f}]   narrowest {row['narrowest']:<9}"
            f"  |  U56/B136 {row['u56_over_b136']:.4f} [{row['ub_lo']:.4f} .. {row['ub_hi']:.4f}]"
            f"  P(U56 narrower) {row['p_u56_narrower']:.3f}")
    bootd = pd.DataFrame(boot)
    bootd.to_csv(f"{OUT}.bootstrap.csv", index=False)
    say(f"\n    U56 is the NARROWEST-floor parent in {int((bootd.narrowest == 'U56').sum())} of "
        f"{len(bootd)} scheme cells and the WIDEST in "
        f"{int((bootd.widest == 'U56').sum())}; the U56/B136 ratio runs "
        f"{bootd.u56_over_b136.min():.4f} .. {bootd.u56_over_b136.max():.4f} and its "
        f"bootstrap interval covers 1.0 in "
        f"{int(((bootd.ub_lo <= 1.0) & (bootd.ub_hi >= 1.0)).sum())} of {len(bootd)} cells.")
    say(f"    Cells whose 3-parent ratio interval EXCLUDES the chi null's median "
        f"({chi_null[23][0]:.4f}): {int((bootd.ratio_lo > chi_null[23][0]).sum())} of {len(bootd)}.")
    publish("NOISE-CALIBRATED READ", f"U56 narrowest in {int((bootd.narrowest=='U56').sum())}/"
            f"{len(bootd)} cells; U56/B136 spans {bootd.u56_over_b136.min():.3f}.."
            f"{bootd.u56_over_b136.max():.3f}; chi null median max/min {chi_null[23][0]:.4f}")

    # the pre-registered verdict on the floor question
    def ratio_at(rule, D=24, stat="PREM_SHARPE", period="FULL"):
        r = floors[(floors.rule == rule) & (floors.statistic == stat) & (floors.period == period)
                   & (floors.D == D)]
        return r.parent_ratio.to_numpy(float), r.sigma_ratio.to_numpy(float)

    fx, fxs = ratio_at("FIXED_K")
    rt, rts = ratio_at("RATIO_K")
    dj_, djs = ratio_at("DISJOINT")
    say("\n" + "=" * 118)
    say("THE PRE-REGISTERED VERDICT (PREM_SHARPE, FULL, D = 24)")
    say("=" * 118)
    say(f"    FIXED_K  (overlap UNMATCHED, the record's own convention): parent ratio "
        f"{np.nanmin(fx):.4f} .. {np.nanmax(fx):.4f}  (mean {np.nanmean(fx):.4f})")
    say(f"    RATIO_K  (overlap MATCHED at phi):                         parent ratio "
        f"{np.nanmin(rt):.4f} .. {np.nanmax(rt):.4f}  (mean {np.nanmean(rt):.4f})")
    say(f"    DISJOINT (overlap EXACTLY 0, k matched):                   parent ratio "
        f"{np.nanmin(dj_):.4f} .. {np.nanmax(dj_):.4f}  (mean {np.nanmean(dj_):.4f})")
    matched = float(np.nanmean(np.concatenate([rt, dj_])))
    h_overlap = bool(matched < RATIO_BAR)
    h_panel = bool(matched >= PANEL_BAR)
    say(f"    MEAN parent ratio over the MATCHED and ZERO overlap arms = {matched:.4f}  ->  "
        f"H_OVERLAP {'HOLDS' if h_overlap else 'FALSIFIED'} (bar < {RATIO_BAR}), "
        f"H_PANEL {'HOLDS' if h_panel else 'FALSIFIED'} (bar >= {PANEL_BAR})"
        + ("" if (h_overlap or h_panel) else "  ->  PARTIAL"))
    publish("VERDICT on the floor question", f"H_OVERLAP={h_overlap}, H_PANEL={h_panel}, "
            f"mean matched/zero-overlap parent ratio {matched:.4f} vs 567's 1.9813")

    # Q4: does the finite-population law explain it?
    say("\n  Q4 — FINITE-POPULATION LAW.  implied sigma_p = floor / sqrt((M-k)/(k(M-1))).")
    say("       If the floor is pure sampling arithmetic, sigma_p is the SAME on every parent and")
    say("       across every k; the spread then lives entirely in (k, M).")
    fit = floors[(floors.statistic == "PREM_SHARPE") & (floors.period == "FULL") & (floors.D == 24)]
    xs, ys, gs = [], [], []
    for _, r in fit.iterrows():
        for pn in pnames:
            f, kk = r[f"floor_{pn}"], r[f"k_{pn}"]
            if np.isfinite(f) and np.isfinite(kk) and kk < sizes[pn] and f > 0:
                xs.append(np.log(fpc_scale(int(kk), sizes[pn])))
                ys.append(np.log(f))
                gs.append(pn)
    xs, ys = np.asarray(xs), np.asarray(ys)
    A = np.vstack([xs, np.ones_like(xs)]).T
    beta, *_ = np.linalg.lstsq(A, ys, rcond=None)
    r2 = 1 - ((ys - A @ beta) ** 2).sum() / ((ys - ys.mean()) ** 2).sum()
    say(f"       POOLED log(floor) = {beta[0]:+.4f} * log(scale) {beta[1]:+.4f}   R^2 = {r2:.4f}  "
        f"(n = {len(ys)} parent-cells; the law predicts slope +1)")
    dummies = np.vstack([xs] + [(np.array(gs) == p).astype(float) for p in pnames[1:]]
                        + [np.ones_like(xs)]).T
    beta2, *_ = np.linalg.lstsq(dummies, ys, rcond=None)
    r2b = 1 - ((ys - dummies @ beta2) ** 2).sum() / ((ys - ys.mean()) ** 2).sum()
    say(f"       + PARENT DUMMIES: slope {beta2[0]:+.4f}, " +
        ", ".join(f"{p} {beta2[i+1]:+.4f}" for i, p in enumerate(pnames[1:])) +
        f"  R^2 = {r2b:.4f}  (dR^2 = {r2b-r2:+.4f})")
    sig = {p: float(np.nanmean(fit[f"sigma_{p}"])) for p in pnames}
    say(f"       implied sigma_p (mean over the {len(fit)} scheme cells): " +
        ", ".join(f"{p} {v:.4f}" for p, v in sig.items()) +
        f"   max/min {max(sig.values())/min(sig.values()):.4f}")
    say(f"       PAIRWISE after removing (k, M): U56/B136 sigma "
        f"{sig['U56']/sig['B136']:.4f},  U56/{pnames[2]} {sig['U56']/sig[pnames[2]]:.4f},  "
        f"B136/{pnames[2]} {sig['B136']/sig[pnames[2]]:.4f}")
    publish("Q4 finite-population fit", f"pooled slope {beta[0]:+.4f} (law: +1), R2 {r2:.4f}; "
            f"parent dummies add dR2 {r2b-r2:+.4f}; sigma max/min "
            f"{max(sig.values())/min(sig.values()):.4f}")

    # ------------------------------------------------------------------ Q5 capital arm
    say("\n" + "=" * 118)
    say("Q5 CAPITAL ARM — BOTH KEEP paths at EVERY book, FULL and OOS windows, 10 bps")
    say("=" * 118)
    kp = []
    for _, r in grid.iterrows():
        b = bars[r["parent"]]
        m = dict(CAGR=r["FULL_CAGR"], Sharpe=r["FULL_Sharpe"], MaxDD=r["FULL_MaxDD"])
        k4a = bool(r["FULL_H1"] > b["live"]["H1"] and r["FULL_H2"] > b["live"]["H2"]
                   and m["MaxDD"] >= b["live"]["MaxDD"])
        legs = dict(H1=bool(r["FULL_H1"] > b["spy"]["H1"]), H2=bool(r["FULL_H2"] > b["spy"]["H2"]),
                    DD=bool(m["MaxDD"] >= DD_CAP * b["spy"]["MaxDD"]),
                    CAGR=bool(m["CAGR"] >= CAGR_FLOOR * b["spy"]["CAGR"]),
                    OOS=bool(r["OOS_Sharpe"] > b["spyO"]["Sharpe"]))
        o4a = bool(r["OOS_H1"] > b["liveO"]["H1"] and r["OOS_H2"] > b["liveO"]["H2"]
                   and r["OOS_MaxDD"] >= b["liveO"]["MaxDD"])
        olegs = dict(H1=bool(r["OOS_H1"] > b["spyO"]["H1"]), H2=bool(r["OOS_H2"] > b["spyO"]["H2"]),
                     DD=bool(r["OOS_MaxDD"] >= DD_CAP * b["spyO"]["MaxDD"]),
                     CAGR=bool(r["OOS_CAGR"] >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        kp.append(dict(parent=r["parent"], rule=r["rule"], level=r["level"], k=r["k"],
                       draw=r["draw"], gross=r["gross"], cadence=r["cadence"], arm=r["arm"],
                       keep4a=k4a, keep4b=bool(all(legs.values())),
                       keep4b_window=bool(legs["H1"] and legs["H2"] and legs["DD"] and legs["CAGR"]),
                       O_keep4a=o4a, O_keep4b=bool(all(olegs.values())),
                       fail_legs=",".join(k for k, v in legs.items() if not v) or "-"))
    kpdf = pd.DataFrame(kp)
    kpdf.to_csv(f"{OUT}.keeppaths.csv.gz", index=False, compression="gzip")
    say(f"    {len(kpdf)} books scored.  4a FULL {int(kpdf.keep4a.sum())}/{len(kpdf)}   "
        f"4b FULL (567 convention, OOS-Sharpe leg included) {int(kpdf.keep4b.sum())}/{len(kpdf)}   "
        f"4b OOS WINDOW {int(kpdf.O_keep4b.sum())}/{len(kpdf)}   "
        f"BOTH {int((kpdf.keep4a & kpdf.keep4b).sum())}/{len(kpdf)}")
    for pn in pnames:
        g = kpdf[kpdf.parent == pn]
        say(f"      {pn:<9} 4a {int(g.keep4a.sum()):>5}/{len(g)}   4b FULL {int(g.keep4b.sum()):>5}"
            f"   4b OOS {int(g.O_keep4b.sum()):>5}   4b FULL&OOS {int((g.keep4b & g.O_keep4b).sum()):>5}")
    say("      4b binding failure legs (FULL): " + ", ".join(
        f"{k} {v}" for k, v in kpdf.fail_legs.value_counts().head(6).items()))
    for rule in ("FIXED_K", "RATIO_K", "DISJOINT"):
        g = kpdf[kpdf.rule == rule]
        say(f"      {rule:<9} 4a {int(g.keep4a.sum()):>5}/{len(g)}   4b FULL {int(g.keep4b.sum()):>5}"
            f"   4b OOS {int(g.O_keep4b.sum()):>5}")

    # ------------------------------------------------------------------ rule 8
    say("\n" + "=" * 118)
    say("RULE 8 WALK-FORWARD — every chooser fit on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE")
    say("  C_SHARPE   argmax IS Sharpe over every (scheme, draw) book at the binding rung")
    say("  C_TRANCHE  argmax IS Sharpe of the draw-blind 1/D TRANCHE of a (scheme, arm) cell")
    say("  C_FLOORMIN the scheme cell with the NARROWEST IS floor, traded as its MA-RS tranche")
    say("  C_FLOORMAX its mirror (WIDEST IS floor) — the control the floor claim needs")
    say("  C_LIVE     the inheritance: RULES v2 on the whole parent, choosing nothing")
    say("=" * 118)
    wf = []
    g6ok = True
    for pn in pnames:
        b = bars[pn]
        i_is = b["i_is"]
        cells = {}
        for sc in schemes:
            key = (sc["rule"], sc["level"])
            rr = [per_draw_rets[(pn, key[0], key[1], d)] for d in range(NDRAW)
                  if (pn, key[0], key[1], d) in per_draw_rets]
            if not rr:
                continue
            cells[key] = {arm: np.mean([x[arm] for x in rr], axis=0) for arm in ARMS}
            cells[key]["_draws"] = rr

        def read(tag, r, desc):
            k4a, k4b, m, _, _, legs = keep_paths(r[i_is:], b["spyO"], b["liveO"])
            f4a, f4b, fm, fh1, fh2, flegs = keep_paths(r, b["spy"], b["live"])
            say(f"    {pn:<9} {tag:<11} {desc:<44} OOS {m['CAGR']:>7.2%} / {m['Sharpe']:>7.4f} / "
                f"{m['MaxDD']:>8.2%}   4a {'Y' if k4a else 'n'}  4b {'Y' if k4b else 'n'}  "
                f"legs {'+'.join(k for k, v in legs.items() if not v) or 'all pass'}")
            say(f"    {'':<9} {'':<11} {'':<44} FULL {fm['CAGR']:>6.2%} / {fm['Sharpe']:>7.4f} / "
                f"{fm['MaxDD']:>8.2%}  H1/H2 {fh1:>6.3f}/{fh2:>6.3f}   4a {'Y' if f4a else 'n'}"
                f"  4b {'Y' if f4b else 'n'}  legs "
                f"{'+'.join(k for k, v in flegs.items() if not v) or 'all pass'}")
            wf.append(dict(parent=pn, chooser=tag, pick=desc, O_CAGR=m["CAGR"],
                           O_Sharpe=m["Sharpe"], O_MaxDD=m["MaxDD"], O_keep4a=k4a, O_keep4b=k4b,
                           F_CAGR=fm["CAGR"], F_Sharpe=fm["Sharpe"], F_MaxDD=fm["MaxDD"],
                           F_H1=fh1, F_H2=fh2, F_keep4a=f4a, F_keep4b=f4b,
                           spy_F_CAGR=b["spy"]["CAGR"], spy_F_Sharpe=b["spy"]["Sharpe"],
                           spy_F_MaxDD=b["spy"]["MaxDD"], spy_F_H1=b["spy"]["H1"],
                           spy_F_H2=b["spy"]["H2"], live_F_CAGR=b["live"]["CAGR"],
                           live_F_Sharpe=b["live"]["Sharpe"], live_F_MaxDD=b["live"]["MaxDD"],
                           live_F_H1=b["live"]["H1"], live_F_H2=b["live"]["H2"],
                           spy_O_CAGR=b["spyO"]["CAGR"], spy_O_Sharpe=b["spyO"]["Sharpe"],
                           spy_O_MaxDD=b["spyO"]["MaxDD"], live_O_CAGR=b["liveO"]["CAGR"],
                           live_O_Sharpe=b["liveO"]["Sharpe"], live_O_MaxDD=b["liveO"]["MaxDD"],
                           **{f"leg_{k}": v for k, v in legs.items()}))

        # C_SHARPE over every individual draw book at the binding rung
        best, bkey = -9e9, None
        for key, c in cells.items():
            for d, x in enumerate(c["_draws"]):
                for arm in ARMS:
                    s = sharpe(x[arm][:i_is])
                    if np.isfinite(s) and s > best:
                        best, bkey = s, (key, d, arm)
        (key, d, arm) = bkey
        read("C_SHARPE", cells[key]["_draws"][d][arm],
             f"{key[0]} lev={key[1]:.4f} draw={d} {arm} (IS S {best:.4f})")
        # C_TRANCHE over (scheme, arm)
        best, bkey = -9e9, None
        for key, c in cells.items():
            for arm in ARMS:
                s = sharpe(c[arm][:i_is])
                if np.isfinite(s) and s > best:
                    best, bkey = s, (key, arm)
        key, arm = bkey
        read("C_TRANCHE", cells[key][arm], f"{key[0]} lev={key[1]:.4f} {arm} TRANCHE (IS S {best:.4f})")
        # C_FLOORMIN / C_FLOORMAX: the floor itself as a selector, on IS rows only
        isf = {}
        for sc in schemes:
            key = (sc["rule"], sc["level"])
            s = prem[(prem.parent == pn) & (prem.rule == key[0]) & (prem.level == key[1])]
            if len(s) and key in cells:
                isf[key] = floor_of(s, "PREM_SHARPE", "IS", NDRAW, key[0] == "DISJOINT")[0]
        kmin = min(isf, key=lambda z: isf[z])
        kmax = max(isf, key=lambda z: isf[z])
        read("C_FLOORMIN", cells[kmin]["MA-RS"],
             f"{kmin[0]} lev={kmin[1]:.4f} MA-RS tranche (IS floor {isf[kmin]:.4f})")
        read("C_FLOORMAX", cells[kmax]["MA-RS"],
             f"{kmax[0]} lev={kmax[1]:.4f} MA-RS tranche (IS floor {isf[kmax]:.4f})")
        px, names = parents[pn]
        warm = px.index[260]
        lr = p567.fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[warm:].to_numpy(float)
        read("C_LIVE", lr, "RULES v2 on the WHOLE parent (inheritance)")
        say(f"    {pn:<9} {'SPY':<11} {'buy and hold':<44} OOS {b['spyO']['CAGR']:>7.2%} / "
            f"{b['spyO']['Sharpe']:>7.4f} / {b['spyO']['MaxDD']:>8.2%}   (FULL "
            f"{b['spy']['CAGR']:.2%} / {b['spy']['Sharpe']:.4f} / {b['spy']['MaxDD']:.2%}  H1/H2 "
            f"{b['spy']['H1']:.3f}/{b['spy']['H2']:.3f})")
        # G6: the IS window is closed BEFORE 2017-01-01, and every chooser statistic is
        # reproduced from an input series truncated by DATE rather than by position.
        idx = parents[pn][0].loc[warm:].index
        if not (idx[i_is - 1] < pd.Timestamp(OOS_START) <= idx[i_is]):
            g6ok = False
        keep_mask = np.asarray(idx < pd.Timestamp(OOS_START))
        for key, c in cells.items():
            for arm in ARMS:
                a = sharpe(c[arm][:i_is])
                bb = sharpe(c[arm][keep_mask])
                if not (np.isnan(a) and np.isnan(bb)) and not abs(a - bb) < 1e-15:
                    g6ok = False
    gate("G6 no chooser statistic reads a row on or after 2017-01-01 (recomputed on truncated input)",
         g6ok, "True", g6ok)
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n    rule-8 picks clearing 4a OOS: {int(wfd.O_keep4a.sum())}/{len(wfd)}; "
        f"4b OOS: {int(wfd.O_keep4b.sum())}/{len(wfd)}")
    for tag, g in wfd.groupby("chooser"):
        say(f"      {tag:<11} mean OOS Sharpe {g.O_Sharpe.mean():.4f} vs live "
            f"{g.live_O_Sharpe.mean():.4f} vs SPY {g.spy_O_Sharpe.mean():.4f}   "
            f"beats live {int((g.O_Sharpe > g.live_O_Sharpe).sum())}/{len(g)}, beats SPY "
            f"{int((g.O_Sharpe > g.spy_O_Sharpe).sum())}/{len(g)}")
    fmin = wfd[wfd.chooser == "C_FLOORMIN"]
    fmax = wfd[wfd.chooser == "C_FLOORMAX"]
    say(f"    THE FLOOR AS A SELECTOR: C_FLOORMIN mean OOS Sharpe {fmin.O_Sharpe.mean():.4f} vs "
        f"C_FLOORMAX {fmax.O_Sharpe.mean():.4f}  (d {fmin.O_Sharpe.mean()-fmax.O_Sharpe.mean():+.4f}, "
        f"narrower floor wins {int((fmin.O_Sharpe.to_numpy() > fmax.O_Sharpe.to_numpy()).sum())}/"
        f"{len(fmin)} parents)")

    # ------------------------------------------------------------------ gates + files
    gg = pd.DataFrame(GATES)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gg["pass_"].sum())
    say(f"\n  GATES {npass}/{len(gg)} pass.")
    say(f"  wrote {OUT.name}.grid.csv.gz / .statistics.csv.gz / .floors.csv / .headline.csv / "
        f".overlap.csv / .keeppaths.csv.gz / .walkforward.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 894 (lane B, 2026-09-20): REQUIRE A TREE-STAMP BESIDE EVERY PUBLISHED CENSUS DENOMINATOR
— generalised from PROSE to CAPITAL: does a published 4b VERDICT depend on the LENGTH of the
LADDER it was read off?

THE DEFECT THIS CLOSES
----------------------
Idea 889 found idea 871's census, byte-for-byte unchanged, reads 70 / 79 / 85 / 86 at four
committed trees (+22.9% in six commits), and idea 880 divided by a 70 that was already 79 when it
ran.  The literal ask is a PROTOCOL clause: print (sha, file count) beside any published census
denominator.  As prose that is unfalsifiable hygiene.  It becomes a CAPITAL question the moment
you notice that every rule-8 verdict in this record is also a quotient with an unprinted
denominator: the chooser reads a LADDER of books and publishes the argmax, and the ladder's
LENGTH is exactly as unstamped as a file count.  Idea 1799 already found the symptom — the IS
chooser "walks to the laziest rung of whatever `h` ladder it is given" (18 of 24 picks on the top
two rungs) — but measured it at ONE ladder length.

So: hold the tape, the panel, the cost and the chooser FIXED, and move ONLY the denominator.  If a
published 4b OOS verdict flips as the ladder grows, the stamp is load-bearing for capital and the
clause should be adopted as a GATE.  If the verdict is constant in the denominator, the clause is
prose hygiene and this record should say so instead of adding another gate.

THE CONSTRUCTION
----------------
BOOK FAMILY: the live book's own two dials, `baseline.rules_v2_weights(px, band, gross)` — no new
degrees of freedom are invented for this test.
    band   {0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20}    (8 rungs; 0.03 is the live cell)
    gross  {0.50, 0.75, 1.00}                                   (3 rungs; 0.75 is the live cell)
    -> M = 24 cells per panel, the LADDER.

TUNED (2, the protocol maximum; ALL grid points reported):
    stat    the IS-only chooser statistic  {IS_SHARPE, IS_CAGR, IS_MINMARG, IS_LEGS}
    order   the ladder ORDER rule          {GRID, REVERSE, RAND(seeded, 20 seeds)}

PUBLISHED, NOT TUNED:
    m       ladder length (nested prefixes)   2 .. 24      <- THE DENOMINATOR, the axis of this idea
    panel   {U56, B136}
    cost    {0, 10, 25, 50} bps   (exact: held and turnover do not depend on cost)

CONTROL (not a dial): at every prefix length the IS chooser is paired with a UNIFORM RANDOM PICK
from the SAME prefix, same 20 seeds.  Argmax over a longer list wins more often for free; the
random pick is what "no information, same denominator" looks like and is the only honest comparand
for a ladder-length effect.

Execution realism throughout: weights decided at close t, applied t+1 (the engine's shift), weekly
cadence, 10 bps primary cost rung, gross never above 1.00, no shorting, no leverage.

PRE-STATED VERDICT RULES (fixed before the run; no tuning-until-it-works)
------------------------------------------------------------------------
V1  IS THE STAMP LOAD-BEARING FOR CAPITAL?  Over all (panel, cost, order, stat) streams, what
    share do NOT hold a constant 4b-OOS verdict across m = 2..24?  >= 0.20 -> the denominator is a
    real dial and PROTOCOL should stamp ladder-read verdicts.  <= 0.05 -> prose hygiene only, and
    this run recommends AGAINST adding the gate.
V2  DOES 1799's LAZY-RUNG WALK REPLICATE ACROSS DENOMINATORS?  Share of picks landing on the top
    two rungs of the prefix, as a function of m.  Rising in m -> the walk is a ladder-length
    artefact, not a property of the statistic.
V3  DOES THE CHOOSER BEAT ITS OWN DENOMINATOR?  If the IS chooser's 4b-OOS pass rate sits inside
    the random-pick control's seed band at every m, the chooser carries no information and the
    ladder length is the whole story.
V4  RULE 8 IS DECISIVE FOR CAPITAL.  (stat, order) chosen on 2009-2016 ONLY by the pre-stated rule
    "highest IS-window Sharpe of that stream's own full-ladder pick"; 2017-2026 then read ONCE.
    Report OOS CAGR / Sharpe / MaxDD against live RULES v2 and SPY.  A candidate that only wins
    in-sample is PARK, not KEEP (PROTOCOL rule 8).
V5  THE LITERAL CENSUS LEG.  Re-read the record's most-used denominator (the committed
    `research/backtests/*.py` file count) at the last committed trees and publish the drift with
    its (sha, count) stamps — the thing idea 894 actually asked for.

Run: python research/backtests/2026-09-20_census-denominator-ladder-stamp_B.py
Deterministic, offline (committed caches only).  RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py are NOT modified by this run (rule 6).
"""
from __future__ import annotations
import subprocess, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state           # noqa: E402
from engine import backtest, rebalance_mask                                # noqa: E402

DATE, SLUG = "2026-09-20", "census-denominator-ladder-stamp"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, CAD = 260, "W"
BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
GROSSES = [0.50, 0.75, 1.00]
COSTS = [0.0, 10.0, 25.0, 50.0]
PRIMARY_COST = 10.0
STATS = ["IS_SHARPE", "IS_CAGR", "IS_MINMARG", "IS_LEGS"]
ORDERS = ["GRID", "REVERSE", "RAND"]
SEEDS = list(range(20260920, 20260940))          # 20 seeds, fixed
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_CELL = (0.03, 0.75)

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


# --------------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs4b(m, bm):
    """PROTOCOL 4b, evaluated inside whatever window m and bm were packed on."""
    return dict(L1_H1=bool(m["H1"] > bm["H1"]), L2_H2=bool(m["H2"] > bm["H2"]),
                L4_DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                L5_CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))


def k4a(m, live):
    """PROTOCOL 4a, against the LIVE RULES v2 book on the same window."""
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


def minmarg(m, bm):
    """Smallest of the four 4b legs' NORMALISED margins.  > 0 iff all four legs pass."""
    return float(min(m["H1"] - bm["H1"], m["H2"] - bm["H2"],
                     (m["MaxDD"] - DD_CAP * bm["MaxDD"]) / max(abs(DD_CAP * bm["MaxDD"]), 1e-9),
                     (m["CAGR"] - CAGR_FLOOR * bm["CAGR"]) / max(abs(CAGR_FLOOR * bm["CAGR"]), 1e-9)))


# ------------------------------------------------------------------ fast engine
def bt(px, W):
    """Engine-exact backtest at ZERO cost, returning gross return and turnover so that every
    cost rung is recoverable exactly:  r(c) = gross - turnover * c / 1e4."""
    R = px.pct_change().fillna(0.0).values
    Wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, CAD).shift(1, fill_value=False).values
    T, N = R.shape
    cur = np.zeros(N)
    gross = np.empty(T); turn = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = Wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        gross[i] = float(cur @ R[i])
        g = cur * (1 + R[i])
        tot = g.sum() + (1 - cur.sum())
        if tot > 0:
            cur = g / tot
    return gross, turn


def v2w(px, band, gross):
    """The live book's weights function, reproduced locally (gate G2 pins it to baseline)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


# --------------------------------------------------------------------- the run
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 894 (lane B) — DOES A PUBLISHED 4b VERDICT DEPEND ON THE LENGTH OF ITS LADDER?")
    say("=" * 100)

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    cells = [(b, g) for g in GROSSES for b in BANDS]            # GRID order
    M = len(cells)
    say(f"\nLadder: {M} cells = {len(BANDS)} bands x {len(GROSSES)} gross; panels "
        f"{ {k: v.shape for k, v in panels.items()} }; cadence {CAD}; costs {COSTS} bps")

    # ---------------------------------------------------------------- gates
    say("\n--- GATES ---")
    pxg = panels["U56"]
    b0, g0 = LIVE_CELL
    d_w = float(np.nanmax(np.abs(v2w(pxg, b0, g0).values - rules_v2_weights(pxg, b0, g0).values)))
    gate("G1 v2w == baseline.rules_v2_weights (live cell)", f"{d_w:.3e}", "0", d_w == 0.0)
    eng = backtest(pxg, v2w(pxg, b0, g0), cost_bps=PRIMARY_COST, freq=CAD)["returns"].values
    gr, tu = bt(pxg, v2w(pxg, b0, g0))
    d_r = float(np.nanmax(np.abs((gr - tu * PRIMARY_COST / 1e4) - eng)))
    gate("G2 local bt() == engine.backtest (live cell, 10 bps)", f"{d_r:.3e}", "< 1e-15", d_r < 1e-15)

    # ------------------------------------------------------- price every cell
    say("\n--- PRICING THE LADDER (all grid points) ---")
    book = {}                 # (panel, cell) -> (gross, turnover) over the scored index
    idx = {}
    for pname, px in panels.items():
        start = px.index[WARMUP]
        sl = px.index >= start
        idx[pname] = px.index[sl]
        for (b, g) in cells:
            gr, tu = bt(px, v2w(px, b, g))
            book[(pname, b, g)] = (gr[sl], tu[sl])
        spy = px["SPY"].pct_change().fillna(0.0).values[sl]
        book[(pname, "SPY")] = (spy, np.zeros_like(spy))
        lv_gr, lv_tu = bt(px, rules_v2_weights(px))
        book[(pname, "LIVE")] = (lv_gr[sl], lv_tu[sl])
        say(f"  {pname}: {len(idx[pname])} scored days "
            f"{idx[pname][0].date()} .. {idx[pname][-1].date()}  ({M} cells priced)")

    wins = {}
    for pname in panels:
        i = idx[pname]
        wins[pname] = dict(FULL=np.ones(len(i), bool),
                           IS=np.asarray(i <= IS_END), OOS=np.asarray(i >= OOS_START))
        say(f"  {pname}: IS rows {wins[pname]['IS'].sum()}  OOS rows {wins[pname]['OOS'].sum()}")

    def rets(pname, key, c, win):
        gr, tu = book[(pname, *key)] if isinstance(key, tuple) else book[(pname, key)]
        return (gr - tu * c / 1e4)[wins[pname][win]]

    # ------------------------------------------ the full grid, every cell reported
    say("\n--- ALL GRID POINTS (primary cost 10 bps) ---")
    grid_rows = []
    for pname in panels:
        for c in COSTS:
            spy_w = {w: pack(rets(pname, "SPY", 0.0, w)) for w in ("FULL", "IS", "OOS")}
            liv_w = {w: pack(rets(pname, "LIVE", c, w)) for w in ("FULL", "IS", "OOS")}
            for (b, g) in cells:
                row = dict(panel=pname, cost=c, band=b, gross=g)
                for w in ("FULL", "IS", "OOS"):
                    m = pack(rets(pname, (b, g), c, w))
                    lg = legs4b(m, spy_w[w])
                    row.update({f"{w}_{k}": v for k, v in m.items()})
                    row[f"{w}_4b"] = all(lg.values())
                    row[f"{w}_4a"] = k4a(m, liv_w[w])
                    row[f"{w}_minmarg"] = minmarg(m, spy_w[w])
                    row[f"{w}_legs"] = sum(lg.values())
                    for k, v in lg.items():
                        row[f"{w}_{k}"] = v
                grid_rows.append(row)
    G = pd.DataFrame(grid_rows)
    G.to_csv(f"{OUT}_grid.csv", index=False)

    for pname in panels:
        sub = G[(G.panel == pname) & (G.cost == PRIMARY_COST)]
        say(f"\n  {pname} @ 10 bps — every one of the {M} ladder cells:")
        say("    band gross |  FULL CAGR Sharpe  MaxDD  4b 4a |   OOS CAGR Sharpe  MaxDD  4b 4a")
        for _, r in sub.iterrows():
            star = "  <- LIVE CELL" if (r.band, r.gross) == LIVE_CELL else ""
            say(f"    {r.band:4.2f} {r.gross:4.2f}  | {r.FULL_CAGR:9.2%} {r.FULL_Sharpe:6.3f} "
                f"{r.FULL_MaxDD:7.2%} {int(r.FULL_4b)}  {int(r.FULL_4a)} | {r.OOS_CAGR:9.2%} "
                f"{r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:7.2%} {int(r.OOS_4b)}  {int(r.OOS_4a)}{star}")
        sp = pack(rets(pname, "SPY", 0.0, "FULL")); so = pack(rets(pname, "SPY", 0.0, "OOS"))
        lf = pack(rets(pname, "LIVE", PRIMARY_COST, "FULL")); lo = pack(rets(pname, "LIVE", PRIMARY_COST, "OOS"))
        say(f"    SPY        FULL {sp['CAGR']:.2%} / {sp['Sharpe']:.3f} / {sp['MaxDD']:.2%}"
            f"   OOS {so['CAGR']:.2%} / {so['Sharpe']:.3f} / {so['MaxDD']:.2%}")
        say(f"    RULES v2   FULL {lf['CAGR']:.2%} / {lf['Sharpe']:.3f} / {lf['MaxDD']:.2%}"
            f"   OOS {lo['CAGR']:.2%} / {lo['Sharpe']:.3f} / {lo['MaxDD']:.2%}")
        say(f"    4b bars (FULL): CAGR floor {CAGR_FLOOR * sp['CAGR']:.2%}, DD cap "
            f"{DD_CAP * sp['MaxDD']:.2%} | (OOS): CAGR floor {CAGR_FLOOR * so['CAGR']:.2%}, "
            f"DD cap {DD_CAP * so['MaxDD']:.2%}")

    # ------------------------------------------------- the denominator sweep
    say("\n" + "=" * 100)
    say("V1 / V2 / V3 — THE DENOMINATOR SWEEP: pick and verdict as the ladder GROWS, m = 2..%d" % M)
    say("=" * 100)

    def order_of(kind, seed=None):
        if kind == "GRID":
            return list(range(M))
        if kind == "REVERSE":
            return list(range(M))[::-1]
        rng = np.random.default_rng(seed)
        return list(rng.permutation(M))

    key = {(p, c): {(b, g): G[(G.panel == p) & (G.cost == c) & (G.band == b) & (G.gross == g)].iloc[0]
                    for (b, g) in cells} for p in panels for c in COSTS}

    def pick_idx(rows, order, m, stat):
        """Legal IS-only argmax over the first m cells of `order`.  Ties -> lowest ladder index."""
        pref = order[:m]
        vals = []
        for j in pref:
            r = rows[cells[j]]
            v = dict(IS_SHARPE=r.IS_Sharpe, IS_CAGR=r.IS_CAGR,
                     IS_MINMARG=r.IS_minmarg, IS_LEGS=r.IS_legs + 1e-6 * r.IS_Sharpe)[stat]
            vals.append(-1e18 if not np.isfinite(v) else v)
        return pref[int(np.argmax(vals))]

    sweep = []
    for pname in panels:
        for c in COSTS:
            rows = key[(pname, c)]
            for kind in ORDERS:
                seeds = SEEDS if kind == "RAND" else [None]
                for sd in seeds:
                    order = order_of(kind, sd)
                    rng = np.random.default_rng((sd or 0) + 7)
                    for m in range(2, M + 1):
                        for stat in STATS:
                            j = pick_idx(rows, order, m, stat)
                            r = rows[cells[j]]
                            rank_in_pref = order[:m].index(j)
                            sweep.append(dict(panel=pname, cost=c, order=kind, seed=sd, m=m,
                                              stat=stat, pick=str(cells[j]),
                                              top2=bool(rank_in_pref >= m - 2),
                                              OOS_4b=bool(r.OOS_4b), OOS_4a=bool(r.OOS_4a),
                                              FULL_4b=bool(r.FULL_4b),
                                              OOS_Sharpe=float(r.OOS_Sharpe),
                                              OOS_CAGR=float(r.OOS_CAGR),
                                              OOS_MaxDD=float(r.OOS_MaxDD),
                                              IS_Sharpe=float(r.IS_Sharpe)))
                        jr = order[:m][int(rng.integers(m))]          # CONTROL: uniform random pick
                        rr = rows[cells[jr]]
                        sweep.append(dict(panel=pname, cost=c, order=kind, seed=sd, m=m,
                                          stat="CTRL_RANDOM", pick=str(cells[jr]), top2=False,
                                          OOS_4b=bool(rr.OOS_4b), OOS_4a=bool(rr.OOS_4a),
                                          FULL_4b=bool(rr.FULL_4b), OOS_Sharpe=float(rr.OOS_Sharpe),
                                          OOS_CAGR=float(rr.OOS_CAGR), OOS_MaxDD=float(rr.OOS_MaxDD),
                                          IS_Sharpe=float(rr.IS_Sharpe)))
    S = pd.DataFrame(sweep)
    S.to_csv(f"{OUT}_sweep.csv", index=False)
    say(f"\n  {len(S):,} chooser-cells written to {Path(str(OUT) + '_sweep.csv').name}")

    # ---- V1: does the published verdict hold constant in the denominator?
    real = S[S.stat != "CTRL_RANDOM"]
    grp = real.groupby(["panel", "cost", "order", "seed", "stat"], dropna=False)
    streams = grp.agg(n_verdicts=("OOS_4b", lambda v: v.nunique()),
                      flips=("OOS_4b", lambda v: int((v.values[1:] != v.values[:-1]).sum())),
                      pick_flips=("pick", lambda v: int((v.values[1:] != v.values[:-1]).sum())),
                      sh_min=("OOS_Sharpe", "min"), sh_max=("OOS_Sharpe", "max"),
                      pass_share=("OOS_4b", "mean")).reset_index()
    streams["unstable"] = streams.n_verdicts > 1
    streams["sh_spread"] = streams.sh_max - streams.sh_min
    streams.to_csv(f"{OUT}_streams.csv", index=False)
    v1 = float(streams.unstable.mean())
    say("\n--- V1  SHARE OF STREAMS WHOSE 4b-OOS VERDICT IS NOT CONSTANT IN m ---")
    say(f"  streams = {len(streams)}  (panel x cost x order/seed x stat)")
    say(f"  UNSTABLE SHARE = {v1:.3f}   ({int(streams.unstable.sum())} of {len(streams)})")
    say(f"  median verdict flips per stream = {streams.flips.median():.1f}, max = {streams.flips.max()}")
    say(f"  median PICK flips per stream    = {streams.pick_flips.median():.1f}, max = {streams.pick_flips.max()}")
    say(f"  OOS Sharpe SPREAD across m: median {streams.sh_spread.median():.4f}, "
        f"p90 {streams.sh_spread.quantile(0.90):.4f}, max {streams.sh_spread.max():.4f}")
    say("\n  by stat:")
    say(streams.groupby("stat")[["unstable", "flips", "pick_flips", "sh_spread", "pass_share"]]
        .mean().to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  by order:")
    say(streams.groupby("order")[["unstable", "flips", "pick_flips", "sh_spread", "pass_share"]]
        .mean().to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  by panel x cost:")
    say(streams.groupby(["panel", "cost"])[["unstable", "flips", "sh_spread", "pass_share"]]
        .mean().to_string(float_format=lambda x: f"{x:.3f}"))
    V1 = "LOAD-BEARING" if v1 >= 0.20 else ("PROSE-ONLY" if v1 <= 0.05 else "INTERMEDIATE")
    publish("V1 verdict", f"unstable share {v1:.3f} -> {V1}")

    # ---- V2: the lazy-rung walk against the denominator
    say("\n--- V2  SHARE OF PICKS ON THE PREFIX'S TOP TWO RUNGS, vs m  (1799 replication) ---")
    t2 = real.groupby(["stat", "m"]).top2.mean().unstack(0)
    say("  (chance = 2/m; a statistic that CARRIES information should fall BELOW chance)")
    say(pd.concat([t2, pd.Series(2 / t2.index.values, index=t2.index, name="CHANCE")], axis=1)
        .to_string(float_format=lambda x: f"{x:.3f}"))
    lift = float((real.groupby("m").top2.mean() - 2 / np.arange(2, M + 1)).mean())
    publish("V2 mean top-2 lift over chance", f"{lift:+.4f}")

    # ---- V3: chooser vs its own denominator (the random control)
    say("\n--- V3  4b-OOS PASS RATE vs m: EACH CHOOSER AGAINST THE RANDOM-PICK CONTROL ---")
    pr = S.groupby(["stat", "m"]).OOS_4b.mean().unstack(0)
    ctrl_sd = S[S.stat == "CTRL_RANDOM"].groupby(["m", "seed"]).OOS_4b.mean().groupby("m").std()
    tbl = pr.copy()
    tbl["CTRL_sd"] = ctrl_sd
    say(tbl.to_string(float_format=lambda x: f"{x:.3f}"))
    inside = {}
    for st in STATS:
        d = (pr[st] - pr["CTRL_RANDOM"]).abs()
        inside[st] = float((d <= 2 * ctrl_sd.reindex(d.index).fillna(0)).mean())
    say("\n  share of m at which the chooser sits INSIDE +/-2 sd of the random control:")
    for st, v in inside.items():
        say(f"    {st:12s} {v:.3f}")
    publish("V3 inside-control shares", {k: round(v, 3) for k, v in inside.items()})

    # ---- V3b: the PAIRED comparand (the 2sd band above is a 20-seed object and underpowered)
    say("\n--- V3b  PAIRED: chooser minus its OWN random control, matched on (panel, cost, order, seed, m) ---")
    kcols = ["panel", "cost", "order", "seed", "m"]
    ctrl = S[S.stat == "CTRL_RANDOM"].set_index(kcols, drop=False)
    pair_rows = []
    for st in STATS:
        a = S[S.stat == st].set_index(kcols, drop=False)
        j = a.join(ctrl[["OOS_4b", "OOS_Sharpe"]], rsuffix="_c", how="inner")
        d4 = j.OOS_4b.astype(int) - j.OOS_4b_c.astype(int)
        pair_rows.append(dict(stat=st, n=len(j), mean_4b_diff=float(d4.mean()),
                              win=int((d4 > 0).sum()), loss=int((d4 < 0).sum()), tie=int((d4 == 0).sum()),
                              mean_sharpe_diff=float((j.OOS_Sharpe - j.OOS_Sharpe_c).mean())))
    P = pd.DataFrame(pair_rows)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  (sign test, two-sided, on the win/loss pairs — ties dropped)")
    for _, r in P.iterrows():
        n = r.win + r.loss
        z = (r.win - n / 2) / np.sqrt(n / 4) if n else np.nan
        say(f"    {r.stat:12s} wins {int(r.win):4d} / losses {int(r.loss):4d}   z = {z:+.2f}")
    publish("V3b paired 4b-pass lift over the random control",
            {r.stat: round(r.mean_4b_diff, 3) for _, r in P.iterrows()})

    # ---- V6: WHAT the denominator actually moves — prefix COMPOSITION, not the statistic
    say("\n--- V6  MECHANISM: is the flip a PREFIX-COMPOSITION fact? ---")
    comp = []
    for pname in panels:
        for c in COSTS:
            rows = key[(pname, c)]
            passing = {cl for cl in cells if bool(rows[cl].OOS_4b)}
            for kind in ORDERS:
                for sd in (SEEDS if kind == "RAND" else [None]):
                    order = order_of(kind, sd)
                    first = next((m for m in range(1, M + 1)
                                  if cells[order[m - 1]] in passing), None)
                    for m in range(2, M + 1):
                        share = np.mean([cells[j] in passing for j in order[:m]])
                        comp.append(dict(panel=pname, cost=c, order=kind, seed=sd, m=m,
                                         has_passer=bool(any(cells[j] in passing for j in order[:m])),
                                         pass_share_in_prefix=float(share),
                                         first_passer_at=first))
    C = pd.DataFrame(comp)
    jj = real.merge(C, on=["panel", "cost", "order", "seed", "m"], how="left")
    say(f"  4b-OOS pass rate when the prefix contains NO passing cell: "
        f"{jj[~jj.has_passer].OOS_4b.mean():.3f}  (n = {int((~jj.has_passer).sum()):,})")
    say(f"  4b-OOS pass rate when it contains at least one:            "
        f"{jj[jj.has_passer].OOS_4b.mean():.3f}  (n = {int(jj.has_passer.sum()):,})")
    say(f"  corr(published verdict, prefix passing share) = "
        f"{np.corrcoef(jj.OOS_4b.astype(float), jj.pass_share_in_prefix)[0, 1]:+.4f}")
    fp = C.groupby("order").first_passer_at.describe()[["min", "50%", "max"]]
    say("\n  ladder position of the FIRST 4b-OOS-passing cell, by order rule:")
    say(fp.to_string(float_format=lambda x: f"{x:.1f}"))
    say("\n  per-panel 4b-OOS passing cells at 10 bps (the block the prefix has to reach):")
    for pname in panels:
        rows = key[(pname, PRIMARY_COST)]
        ps = [cl for cl in cells if bool(rows[cl].OOS_4b)]
        say(f"    {pname}: {len(ps)} of {M} cells pass — gross values {sorted({g for _, g in ps})}, "
            f"bands {sorted({b for b, _ in ps})}")
    publish("V6 conditional pass rates (no passer / >=1 passer)",
            f"{jj[~jj.has_passer].OOS_4b.mean():.3f} / {jj[jj.has_passer].OOS_4b.mean():.3f}")

    # ---------------------------------------------------- V4: rule 8, read ONCE
    say("\n" + "=" * 100)
    say("V4 — RULE 8 WALK-FORWARD: (stat, order) chosen on 2009-2016 ONLY; 2017-2026 read ONCE")
    say("=" * 100)
    wf = []
    for pname in panels:
        rows = key[(pname, PRIMARY_COST)]
        best, best_is = None, -1e18
        for kind in ORDERS:
            for sd in (SEEDS if kind == "RAND" else [None]):
                order = order_of(kind, sd)
                for stat in STATS:
                    j = pick_idx(rows, order, M, stat)
                    v = rows[cells[j]].IS_Sharpe                 # IS-only meta-choice
                    if np.isfinite(v) and v > best_is:
                        best_is, best = v, (kind, sd, stat, j)
        kind, sd, stat, j = best
        r = rows[cells[j]]
        so = pack(rets(pname, "SPY", 0.0, "OOS")); lo = pack(rets(pname, "LIVE", PRIMARY_COST, "OOS"))
        lg = legs4b(dict(CAGR=r.OOS_CAGR, Sharpe=r.OOS_Sharpe, MaxDD=r.OOS_MaxDD,
                         H1=r.OOS_H1, H2=r.OOS_H2), so)
        say(f"\n  {pname}: IS-chosen (order={kind}, seed={sd}, stat={stat}) -> cell "
            f"band {cells[j][0]:.2f} / gross {cells[j][1]:.2f}   IS Sharpe {best_is:.4f}")
        say(f"    OOS 2017-2026 (read once)  CAGR {r.OOS_CAGR:7.2%}  Sharpe {r.OOS_Sharpe:6.4f}  "
            f"MaxDD {r.OOS_MaxDD:7.2%}")
        say(f"    RULES v2 baseline OOS      CAGR {lo['CAGR']:7.2%}  Sharpe {lo['Sharpe']:6.4f}  "
            f"MaxDD {lo['MaxDD']:7.2%}")
        say(f"    SPY OOS                    CAGR {so['CAGR']:7.2%}  Sharpe {so['Sharpe']:6.4f}  "
            f"MaxDD {so['MaxDD']:7.2%}")
        say(f"    4b OOS legs {lg} -> {'PASS' if all(lg.values()) else 'FAIL'};  "
            f"4a OOS -> {'PASS' if bool(r.OOS_4a) else 'FAIL'}")
        say(f"    4b FULL {'PASS' if bool(r.FULL_4b) else 'FAIL'} "
            f"(CAGR {r.FULL_CAGR:.2%} / Sharpe {r.FULL_Sharpe:.4f} / MaxDD {r.FULL_MaxDD:.2%}, "
            f"halves {r.FULL_H1:.4f} / {r.FULL_H2:.4f});  4a FULL "
            f"{'PASS' if bool(r.FULL_4a) else 'FAIL'}  ->  PROTOCOL 4b (halves AND OOS) = "
            f"{'PASS' if (bool(r.FULL_4b) and all(lg.values())) else 'FAIL'}")
        # what the SAME chooser would have published at every other denominator
        st = real[(real.panel == pname) & (real.cost == PRIMARY_COST) & (real.order == kind)
                  & (real.seed.isna() if sd is None else real.seed == sd) & (real.stat == stat)]
        say(f"    SAME chooser, other denominators: 4b-OOS pass at {int(st.OOS_4b.sum())} of "
            f"{len(st)} prefix lengths; OOS Sharpe range "
            f"[{st.OOS_Sharpe.min():.4f}, {st.OOS_Sharpe.max():.4f}]")
        wf.append(dict(panel=pname, order=kind, seed=sd, stat=stat, cell=str(cells[j]),
                       IS_Sharpe=best_is, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                       OOS_MaxDD=r.OOS_MaxDD, OOS_4b=bool(all(lg.values())), OOS_4a=bool(r.OOS_4a),
                       base_OOS_Sharpe=lo["Sharpe"], spy_OOS_Sharpe=so["Sharpe"],
                       n_pass_over_m=int(st.OOS_4b.sum()), n_m=len(st)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}_walkforward.csv", index=False)

    # ---------------------------------------- V5: the literal census denominator
    say("\n" + "=" * 100)
    say("V5 — THE LITERAL CENSUS LEG: the record's most-used denominator, re-read at committed trees")
    say("=" * 100)
    try:
        shas = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%H %ad", "--date=short",
                               "-n", "12", "--", "research/backtests"],
                              capture_output=True, text=True, check=True).stdout.split("\n")
        say("\n  sha      date        research/backtests/*.py   research/backtests/*.md")
        prev = None
        for line in [s for s in shas if s.strip()]:
            sha, d = line.split()[0], line.split()[1]
            ls = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", sha,
                                 "research/backtests/"], capture_output=True, text=True).stdout.split("\n")
            npy = sum(1 for f in ls if f.endswith(".py"))
            nmd = sum(1 for f in ls if f.endswith(".md"))
            delta = "" if prev is None else f"   ({npy - prev:+d} vs the next-newer tree)"
            say(f"  {sha[:7]}  {d}  {npy:22d}   {nmd:21d}{delta}")
            prev = npy
        counts = []
        for line in [s for s in shas if s.strip()]:
            sha = line.split()[0]
            ls = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", sha,
                                 "research/backtests/"], capture_output=True, text=True).stdout.split("\n")
            counts.append(sum(1 for f in ls if f.endswith(".py")))
        spread = (max(counts) - min(counts)) / max(min(counts), 1)
        publish("V5 denominator drift over the last 12 commits touching research/backtests",
                f"{min(counts)} .. {max(counts)} files ({spread:+.1%})")
    except Exception as e:                                        # pragma: no cover
        publish("V5 census leg", f"unavailable ({type(e).__name__}: {e})")

    # --------------------------------------------------------------- summary
    say("\n" + "=" * 100)
    say("SUMMARY")
    say("=" * 100)
    say(f"  V1  unstable-verdict share across the denominator .... {v1:.3f}  -> {V1}")
    say(f"  V2  mean top-2 pick lift over chance ................. {lift:+.4f}")
    say(f"  V3  chooser inside the random control's 2sd band ..... "
        f"{ {k: round(v, 2) for k, v in inside.items()} }")
    say(f"  V4  rule-8 OOS 4b passes ............................. "
        f"{int(W.OOS_4b.sum())} of {len(W)} panels; 4a {int(W.OOS_4a.sum())} of {len(W)}")
    say(f"  4b FULL pass share over the whole {len(G):,}-row grid  {G.FULL_4b.mean():.3f}")
    say(f"  4b OOS  pass share over the whole {len(G):,}-row grid  {G.OOS_4b.mean():.3f}")
    say(f"  4a FULL pass share over the whole {len(G):,}-row grid  {G.FULL_4a.mean():.3f}")
    say(f"  gates: {sum(1 for g in GATES if g['pass_'])} of {len(GATES)} pass")
    say(f"  elapsed {time.time() - t0:.1f}s")

    pd.DataFrame(GATES).to_csv(f"{OUT}_gates.csv", index=False)
    Path(f"{OUT}_log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n  wrote {Path(str(OUT) + '_log.txt').name}, _grid.csv, _sweep.csv, _streams.csv, "
        f"_walkforward.csv, _gates.csv")


if __name__ == "__main__":
    main()

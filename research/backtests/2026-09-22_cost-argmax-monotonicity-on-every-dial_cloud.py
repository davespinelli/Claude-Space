#!/usr/bin/env python3
"""Idea 1621 (lane cloud, 2026-09-22) — DOES THE "SLOWER-ONLY" DIRECTION OF COST INVERSION
HOLD ON THE OTHER DIALS?

WHERE THIS COMES FROM.  Idea 1586 (2026-09-19) found that 9 of 9 CADENCE argmax inversions
between the 10 bps and the 25 bps rung move SLOWER (D->W, W->M, M->Q) and not one moves faster.
That is not a statement about cadence.  It is a MONOTONICITY claim about the COST AXIS: raise
the price of turnover and the best rung of any turnover-bearing dial should slide toward the
slow end, never back.  The record owns several other turnover-bearing dials and has published a
"best rung" for each of them at ONE cost rung (PROTOCOL's 10 bps).  If the argmax WANDERS
non-monotonically in cost on a dial, then that dial's committed best rung is a sampling artefact
of the rung it was priced at.

THE QUESTION.  Compute each dial's argmax over a DENSE cost ladder (0..50 bps, 1 bps steps) and
report (a) whether every adjacent-rung argmax MOVE is toward the slow end, (b) whether the whole
argmax path is monotone non-decreasing in slowness, (c) the 10 -> 25 bps contrast that 1586
actually measured, and (d) the Sharpe MARGIN the argmax is held by, so a "wander" that sits
inside the grid's own resolution is not read as a wander.

WHAT IS PRICED.  Four turnover-bearing dials, each a 1-D ladder of REAL BOOKS built from
scratch on the committed caches (no prose is harvested).  The pre-registered SLOWNESS INDEX of
each ladder is its listed order, ascending = slower (more turnover-removing):
    TOPN     top-N by composite momentum among gated names, gross 0.75.
             N in {5, 10, 20, 30, 40, ALL}.  Larger N = slower (a boundary swap moves
             2*gross/N of NAV, so NAV churn falls as N rises; ALL removes the ranking).
    MINHOLD  TOP20 momentum book with a minimum holding period: a name that entered at
             rebalance date d cannot be sold before H trading days have passed unless it
             leaves the gate.  H in {1, 5, 10, 21, 42, 63, 126}.  Larger H = slower.
    HYST     TOP20 momentum book with RANK HYSTERESIS: enter at rank <= 20, leave only when
             rank > 20 + h.  h in {0, 5, 10, 20, 40, 80}.  Larger h = slower.
    BAND     200d-MA band with hysteresis (baseline.band_state), equal weight over in-band
             names at gross 0.75.  c in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16}.
             Wider band = fewer state transitions = slower.
  = 26 cells per (panel x cadence).  Panels U56 / B136 / SMALL; cadences W / M; fills t+1.
  156 book runs in all, each priced ONCE at cost 0 and then reconstructed EXACTLY at all 51
  cost rungs from its own turnover series (the engine's net return is affine in the cost rung:
  r(c) = r0 - turnover * c / 1e4; gate G_COST checks the reconstruction against a direct
  engine run at 25 bps).

TWO SLOWNESS INDICES, BOTH DECLARED BEFORE THE RUN.  "Slower" has to be defined before the
argmax can be said to move toward it.  The listed rung order above is an ASSUMPTION about which
rung churns less, and on at least one ladder (TOPN) it is not guaranteed: dropping the ranking
entirely ("ALL") can churn MORE than a wide top-N because the gate itself flickers.  So every
directional gate below is evaluated TWICE:
    SLOW_PRE   the listed rung order (the record's implicit reading of each dial).
    SLOW_TURN  the EMPIRICAL order of the same rungs by their own realised cost-0 annual
               turnover, highest turnover = fastest.  This is what "slower" actually means.
Both are published per rung.  A directional law that holds on SLOW_PRE but not on SLOW_TURN is
a statement about the record's labelling, not about the cost axis.

DEGENERATE RUNGS.  A ladder can saturate: on a 56-name panel, HYST h >= 36 makes the exit rank
N+h > 56, which no name can reach, so every rung above it is the SAME BOOK.  Every rung whose
cost-0 daily return series is bit-identical to a lower rung on the same instance is flagged
DEGENERATE and counted, and argmax ties are broken toward the FASTER rung — the conservative
direction for a "slower-only" claim.

THE TWO TUNED DIALS (and no more).
  DIAL 1 — DIAL SET: the four ladders above.
  DIAL 2 — COST LADDER: 0..50 bps in 1 bps steps.
REPORTED, NOT TUNED: panel, cadence, gross (0.75 everywhere), the momentum gate (the record's
standard `above 200d MA & vol20 < 0.60`), and N = 20 inside MINHOLD / HYST.  EVERY grid point
is published (`*.grid.csv`, 7,956 rows) and so is every argmax path (`*.argmax.csv`).

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after).
  V1  DIRECTION (a = SLOW_PRE, b = SLOW_TURN).  Over all (dial, panel, cadence) instances,
      EVERY adjacent-cost argmax move is toward the SLOW end (share of slower moves = 1.000).
      Triggered -> 1586's slower-only law is a property of the cost axis, not of cadence.
  V2  MONOTONE (a, b).  The argmax path is monotone non-decreasing in slowness on >= 90% of
      instances.
  V3  1586 REPLICATION (a, b).  Among instances whose argmax MOVES between 10 and 25 bps, every
      move is toward the slow end.
  V4  CAPITAL.  At least one argmax cell clears 4b (FULL and OOS) at the PROTOCOL 10 bps rung.
  V5  RESOLUTION.  The median Sharpe margin holding an argmax (best minus runner-up at the same
      cost) exceeds 0.02, i.e. the argmax is resolvable at all.

PROTOCOL: rule 2 (10 bps is the protocol rung, t+1 fills, no shorting, no leverage — gross
capped at 0.75); rule 3 (live RULES v2 AND SPY, per panel); rule 4 (both KEEP paths at every
argmax cell, <= 2 tuned dials); rule 5 (one idea, deterministic, standalone); rule 8
(the dial rung is chosen on 2009-2016 only and 2017-2026 is read ONCE); rule 9 (survivorship
stated).  RULES.md / scan.py / bot.py / baseline.py NOT modified.

SURVIVORSHIP (rule 9).  All three panels are CURRENT-CONSTITUENT lists: U56 = research/
universe.json, B136 = research/universe_broad.json, SMALL = data/prices_small.csv.gz (the
sub-$2B screen, 719 names as cached today, of which 54 with max_1d_move >= 1.0 are DROPPED
per data/small_meta.csv, leaving 665 investable names + SPY as a benchmark column only).
Every CAGR and MaxDD LEVEL below is therefore optimistic and both 4b bars are easier than on a
point-in-time panel.  The object this run measures is the LOCATION OF AN ARGMAX ALONG A COST
AXIS on one and the same tape, which is first-order immune to the bias; the 4b pass COUNTS are
not.

Run:  python research/backtests/2026-09-22_cost-argmax-monotonicity-on-every-dial_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state, score      # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask               # noqa: E402

DATE, SLUG = "2026-09-22", "cost-argmax-monotonicity-on-every-dial"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

PANELS = ["U56", "B136", "SMALL"]
CADENCES = ["W", "M"]
COSTS = list(range(0, 51))                 # DIAL 2 — dense cost ladder, 1 bps steps
PROTOCOL_COST = 10
GROSS = 0.75
BASE_N = 20
MAX_VOL = 0.60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# DIAL 1 — the dial set.  Listed order IS the pre-registered slowness index (ascending = slower).
LADDERS = {
    "TOPN":    [5, 10, 20, 30, 40, "ALL"],
    "MINHOLD": [1, 5, 10, 21, 42, 63, 126],
    "HYST":    [0, 5, 10, 20, 40, 80],
    "BAND":    [0.00, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16],
}

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# --------------------------------------------------------------------------- metrics helpers
def mets(r):
    r = r.dropna()
    if len(r) < 60:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


# --------------------------------------------------------------------------------- panels
def panel(name):
    """Returns (px_all, investable_cols).  SPY is a constituent of U56/B136 (it is in
    research/universe.json) but a BENCHMARK ONLY on the small panel, per baseline.load_universe."""
    if name == "U56":
        px = load_universe()
        inv = list(px.columns)
    elif name == "B136":
        px = load_universe(broad=True)
        inv = list(px.columns)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])          # mandatory scrub
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        px = px[[c for c in px.columns if c in inv or c == "SPY"]]
    px = px.dropna(how="all").ffill()
    return px, [c for c in inv if c in px.columns]


def signals(px, inv):
    comp, above, vol20 = score(px[inv], vol_scale=False)   # ranks over INVESTABLE names only
    gate_ = above & (vol20 < MAX_VOL) & px[inv].notna()
    return comp, gate_


# --------------------------------------------------------------------- weight constructors
def eq_weights(elig, gross):
    n = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(n, axis=0).fillna(0.0) * gross


def topk_weights(sig, elig, k, gross):
    if k == "ALL":
        return eq_weights(elig, gross)
    rank = sig.where(elig).rank(axis=1, ascending=False, method="first")
    return (rank <= k).astype(float) * (gross / k)


def _stateful(sig, elig, idx, freq, n, rule, param):
    """Rebalance-date loop for the two path-dependent dials.  The decision on rebalance date d
    reads ranks computed from closes up to and including d; the engine then fills at d+1."""
    mask = rebalance_mask(idx, freq).values
    rank = sig.where(elig).rank(axis=1, ascending=False, method="first")
    cols = list(sig.columns)
    ci = {c: i for i, c in enumerate(cols)}
    R = rank.values
    E = elig.values
    W = np.zeros((len(idx), len(cols)))
    held: dict[int, int] = {}                       # column index -> entry bar
    cur = np.zeros(len(cols))
    for i in range(len(idx)):
        if mask[i]:
            r = R[i]
            e = E[i]
            # 1. forced exits: a name that is no longer gated/priced always leaves.
            held = {j: t for j, t in held.items() if e[j] and np.isfinite(r[j])}
            if rule == "MINHOLD":
                # 2. locked names (age < H) stay; unlocked names stay only if still in top-N.
                keep = {j: t for j, t in held.items()
                        if (i - t) < param or r[j] <= n}
            else:                                   # HYST
                keep = {j: t for j, t in held.items() if r[j] <= n + param}
            if len(keep) > n:                       # trim worst-ranked first (deterministic)
                order = sorted(keep, key=lambda j: (r[j], cols[j]))
                keep = {j: keep[j] for j in order[:n]}
            if len(keep) < n:
                cands = [j for j in range(len(cols))
                         if e[j] and np.isfinite(r[j]) and j not in keep]
                cands.sort(key=lambda j: (r[j], cols[j]))
                for j in cands[:n - len(keep)]:
                    keep[j] = i
            held = keep
            cur = np.zeros(len(cols))
            if held:
                cur[list(held)] = GROSS / n
        W[i] = cur
    return pd.DataFrame(W, index=idx, columns=cols)


def build(dial, rung, px, inv, comp, gate_, freq):
    if dial == "TOPN":
        return topk_weights(comp, gate_, rung, GROSS)
    if dial == "BAND":
        return eq_weights(band_state(px[inv], rung) & px[inv].notna(), GROSS)
    return _stateful(comp, gate_, px.index, freq, BASE_N, dial, rung)


# ------------------------------------------------------------------------------------- run
def main():
    log(f"# Idea 1621 (lane cloud, {DATE}) — does the SLOWER-ONLY direction of COST INVERSION "
        f"hold on the OTHER DIALS?")
    log(f"# TUNED DIALS (2): DIAL SET {list(LADDERS)}; COST LADDER {COSTS[0]}..{COSTS[-1]} bps "
        f"step 1 ({len(COSTS)} rungs).")
    log(f"# reported, not tuned: PANEL {PANELS} x CADENCE {CADENCES}; gross {GROSS}; N={BASE_N} "
        f"inside MINHOLD/HYST; gate = above 200d MA & vol20 < {MAX_VOL}.")
    log(f"# COMPARAND (committed, idea 1586, NOT recomputed here): 9 of 9 CADENCE argmax "
        f"inversions between 10 and 25 bps move SLOWER, 0 move faster.")
    log(f"# slowness index = listed rung order, ascending = slower: "
        + "; ".join(f"{k} {v}" for k, v in LADDERS.items()))

    rows, argrows, cost_err = [], [], 0.0
    _r0cache: dict = {}
    for pname in PANELS:
        px, inv = panel(pname)
        comp, gate_ = signals(px, inv)
        st = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        S = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]))
        S["h1"], S["h2"] = halves(spy)
        S["ish1"], S["ish2"] = halves(spy.loc[:IS_END])
        log(f"\n## PANEL {pname}: {len(inv)} investable names, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, scored from {st.date()}  |  SPY FULL "
            f"{S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:.2%}, "
            f"OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:.2%}")

        for freq in CADENCES:
            # live RULES v2 comparand on THIS panel and THIS cadence, at every cost rung
            bres = engine_backtest(px, rules_v2_weights(px), cost_bps=0, freq=freq)
            b0, bt0 = bres["returns"].loc[st:], bres["turnover"].loc[st:]
            LV = {}
            for c in COSTS:
                br = b0 - bt0 * c / 1e4
                m = mets(br)
                lh1, lh2 = halves(br)
                LV[c] = dict(full=m, oos=mets(br.loc[OOS_START:]), h1=lh1, h2=lh2)
            log(f"\n### {pname} / {freq}  RULES v2 baseline @10bps: "
                f"{LV[10]['full']['CAGR']:.2%} / {LV[10]['full']['Sharpe']:.4f} / "
                f"{LV[10]['full']['MaxDD']:.2%}   (H1 {LV[10]['h1']:.3f} / H2 {LV[10]['h2']:.3f})")

            for dial, ladder in LADDERS.items():
                for si, rung in enumerate(ladder):
                    w = build(dial, rung, px, inv, comp, gate_, freq)
                    res = engine_backtest(px, w.reindex(columns=px.columns).fillna(0.0),
                                          cost_bps=0, freq=freq)
                    r0, t0 = res["returns"].loc[st:], res["turnover"].loc[st:]
                    if dial == "TOPN" and rung == ladder[0] and freq == "W":
                        chk = engine_backtest(px, w.reindex(columns=px.columns).fillna(0.0),
                                              cost_bps=25, freq=freq)["returns"].loc[st:]
                        cost_err = max(cost_err, float((chk - (r0 - t0 * 25 / 1e4)).abs().max()))
                    turn_yr = float(t0.sum() / (len(t0) / 252.0))
                    key = (pname, freq, dial)
                    prev = _r0cache.setdefault(key, [])
                    degen = any(float((r0 - q).abs().max()) < 1e-15 for q in prev)
                    prev.append(r0)
                    for c in COSTS:
                        r = r0 - t0 * c / 1e4
                        mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                        h1, h2 = halves(r)
                        ih1, ih2 = halves(r.loc[:IS_END])
                        lv = LV[c]
                        k4bf = (h1 > S["h1"] and h2 > S["h2"]
                                and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                                and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
                        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                        k4a = (h1 > lv["h1"] and h2 > lv["h2"]
                               and mf["MaxDD"] >= lv["full"]["MaxDD"])
                        rows.append(dict(
                            panel=pname, cadence=freq, dial=dial, rung=str(rung),
                            slow_pre=si, degenerate=degen, cost=c, turn_yr=turn_yr,
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                            H1=h1, H2=h2, is_Sharpe=mi["Sharpe"], is_H1=ih1, is_H2=ih2,
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a))
                log(f"    {pname}/{freq}/{dial}: {len(ladder)} rungs priced, turnover/yr "
                    + " ".join(f"{str(r_)}={g:.1f}x" for r_, g in
                               [(l, [x for x in rows if x['panel'] == pname and
                                     x['cadence'] == freq and x['dial'] == dial and
                                     x['rung'] == str(l) and x['cost'] == 0][0]['turn_yr'])
                                for l in ladder]))

    grid = pd.DataFrame(rows)
    # SLOW_TURN: empirical slowness index = rank by own cost-0 annual turnover, fastest = 0.
    grid["slow_turn"] = (grid.groupby(["panel", "cadence", "dial", "cost"])["turn_yr"]
                         .rank(ascending=False, method="first").astype(int) - 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    log(f"\n# GRID: {len(grid)} rows -> {Path(str(OUT)+'.grid.csv').name}")
    gate("G_COST  exact cost reconstruction vs a direct 25 bps engine run",
         f"max |err| = {cost_err:.3e}", "< 1e-12", cost_err < 1e-12)

    # ----------------------------------------------------------------- argmax paths
    for (pn, fq, dl), sub in grid.groupby(["panel", "cadence", "dial"]):
        lad = LADDERS[dl]
        for c in COSTS:
            s = sub[sub.cost == c].sort_values("slow_pre")     # ties -> FASTER rung (conservative)
            best = s.loc[s.Sharpe.idxmax()]
            runner = s.Sharpe.sort_values(ascending=False).iloc[1]
            argrows.append(dict(panel=pn, cadence=fq, dial=dl, cost=c,
                                arg_slow=int(best.slow_pre), arg_turn=int(best.slow_turn),
                                arg_rung=best.rung,
                                Sharpe=best.Sharpe, margin=float(best.Sharpe - runner),
                                n_rungs=len(lad)))
    arg = pd.DataFrame(argrows)
    arg.to_csv(f"{OUT}.argmax.csv", index=False)

    log("\n## ARGMAX PATHS OVER THE DENSE COST LADDER (Sharpe argmax; rung shown at each "
        "switch point)")
    inst_rows = []
    for (pn, fq, dl), s in arg.groupby(["panel", "cadence", "dial"]):
        s = s.sort_values("cost")
        d = np.diff(s.arg_slow.values)
        moves = d[d != 0]
        slower = int((moves > 0).sum())
        faster = int((moves < 0).sum())
        monotone = bool((d >= 0).all())
        dt = np.diff(s.arg_turn.values)
        mt = dt[dt != 0]
        slower_t = int((mt > 0).sum())
        faster_t = int((mt < 0).sum())
        monotone_t = bool((dt >= 0).all())
        a10 = int(s[s.cost == 10].arg_slow.iloc[0])
        a25 = int(s[s.cost == 25].arg_slow.iloc[0])
        t10 = int(s[s.cost == 10].arg_turn.iloc[0])
        t25 = int(s[s.cost == 25].arg_turn.iloc[0])
        ndeg = int(grid[(grid.panel == pn) & (grid.cadence == fq) & (grid.dial == dl)
                        & (grid.cost == 0)].degenerate.sum())
        segs, prev = [], None
        for _, r in s.iterrows():
            if r.arg_rung != prev:
                segs.append(f"{int(r.cost)}bps:{r.arg_rung}")
                prev = r.arg_rung
        inst_rows.append(dict(panel=pn, cadence=fq, dial=dl, n_moves=len(moves),
                              slower=slower, faster=faster, monotone=monotone,
                              n_moves_t=len(mt), slower_t=slower_t, faster_t=faster_t,
                              monotone_t=monotone_t, d_10_25_t=t25 - t10, n_degenerate=ndeg,
                              arg0=s[s.cost == 0].arg_rung.iloc[0],
                              arg10=s[s.cost == 10].arg_rung.iloc[0],
                              arg25=s[s.cost == 25].arg_rung.iloc[0],
                              arg50=s[s.cost == 50].arg_rung.iloc[0],
                              d_10_25=a25 - a10,
                              med_margin=float(s.margin.median()),
                              path="|".join(segs)))
        log(f"  {pn:5s} {fq} {dl:8s} PRE moves={len(moves):2d} slower={slower} faster={faster} "
            f"mono={str(monotone):5s} | TURN moves={len(mt):2d} slower={slower_t} "
            f"faster={faster_t} mono={str(monotone_t):5s} | degen={ndeg} "
            f"med-margin={s.margin.median():.4f}  path: " + " -> ".join(segs))
    inst = pd.DataFrame(inst_rows)
    inst.to_csv(f"{OUT}.instances.csv", index=False)

    tot_moves = int(inst.n_moves.sum())
    tot_slow = int(inst.slower.sum())
    tot_fast = int(inst.faster.sum())
    share = tot_slow / tot_moves if tot_moves else np.nan
    log(f"\n## V1 DIRECTION: {tot_moves} adjacent-cost argmax moves over {len(inst)} instances "
        f"-> SLOWER {tot_slow}, FASTER {tot_fast}, share slower = "
        + (f"{share:.4f}" if tot_moves else "n/a"))
    gate("V1a DIRECTION (SLOW_PRE)  every adjacent-cost argmax move is toward the SLOW end",
         f"{tot_slow}/{tot_moves} slower, {tot_fast} faster", "share = 1.000",
         tot_moves > 0 and tot_fast == 0)
    tm_t, ts_t, tf_t = int(inst.n_moves_t.sum()), int(inst.slower_t.sum()), int(inst.faster_t.sum())
    log(f"## V1b DIRECTION (SLOW_TURN): {tm_t} moves -> SLOWER {ts_t}, FASTER {tf_t}, share "
        + (f"{ts_t/tm_t:.4f}" if tm_t else "n/a"))
    gate("V1b DIRECTION (SLOW_TURN)  same, on the empirical turnover ordering",
         f"{ts_t}/{tm_t} slower, {tf_t} faster", "share = 1.000", tm_t > 0 and tf_t == 0)
    nm = int(inst.monotone.sum())
    gate("V2a MONOTONE (SLOW_PRE)  argmax path monotone non-decreasing in slowness",
         f"{nm}/{len(inst)} = {nm/len(inst):.3f}", ">= 0.90", nm / len(inst) >= 0.90)
    nmt = int(inst.monotone_t.sum())
    gate("V2b MONOTONE (SLOW_TURN)  same, on the empirical turnover ordering",
         f"{nmt}/{len(inst)} = {nmt/len(inst):.3f}", ">= 0.90", nmt / len(inst) >= 0.90)
    mv = inst[inst.d_10_25 != 0]
    gate("V3a 1586 REPLICATION (SLOW_PRE)  10 -> 25 bps moves all SLOWER",
         f"{len(mv)} of {len(inst)} instances move; slower {int((mv.d_10_25>0).sum())}, "
         f"faster {int((mv.d_10_25<0).sum())}", "0 faster", int((mv.d_10_25 < 0).sum()) == 0)
    mvt = inst[inst.d_10_25_t != 0]
    gate("V3b 1586 REPLICATION (SLOW_TURN)  10 -> 25 bps moves all SLOWER",
         f"{len(mvt)} of {len(inst)} instances move; slower {int((mvt.d_10_25_t>0).sum())}, "
         f"faster {int((mvt.d_10_25_t<0).sum())}", "0 faster",
         int((mvt.d_10_25_t < 0).sum()) == 0)
    log(f"## DEGENERATE RUNGS (book bit-identical to a lower rung on the same ladder): "
        f"{int(inst.n_degenerate.sum())} of {len(grid[grid.cost==0])} rungs; instances affected "
        f"{int((inst.n_degenerate>0).sum())} of {len(inst)}")
    gate("V5 RESOLUTION  median Sharpe margin holding an argmax",
         f"{inst.med_margin.median():.4f}", "> 0.02", inst.med_margin.median() > 0.02)

    # -------------------------------------------------- V4 / KEEP paths at the argmax cells
    at10 = arg[arg.cost == PROTOCOL_COST].merge(
        grid[grid.cost == PROTOCOL_COST],
        left_on=["panel", "cadence", "dial", "arg_rung"],
        right_on=["panel", "cadence", "dial", "rung"], suffixes=("", "_g"))
    log("\n## BOTH KEEP PATHS AT EVERY ARGMAX CELL @ PROTOCOL 10 bps "
        f"({len(at10)} cells)")
    for _, r in at10.iterrows():
        log(f"  {r.panel:5s} {r.cadence} {r.dial:8s} rung={r.arg_rung:>4s}  "
            f"FULL {r.CAGR:6.2%} / {r.Sharpe:6.4f} / {r.MaxDD:7.2%}  "
            f"OOS {r.oos_CAGR:6.2%} / {r.oos_Sharpe:6.4f} / {r.oos_MaxDD:7.2%}  "
            f"4b_FULL={str(r.keep4b_full):5s} 4b_OOS={str(r.keep4b_oos):5s} "
            f"4a={str(r.keep4a):5s}")
    n4b = int((at10.keep4b_full & at10.keep4b_oos).sum())
    gate("V4 CAPITAL  an argmax cell clears 4b FULL and OOS at 10 bps",
         f"4b FULL+OOS {n4b}/{len(at10)}; 4b FULL {int(at10.keep4b_full.sum())}; "
         f"4a FULL {int(at10.keep4a.sum())}", ">= 1", n4b >= 1)

    # ---------------------------------------------------------------- rule 8 walk-forward
    log("\n## RULE 8 WALK-FORWARD — rung chosen on 2009-2016 IS Sharpe @10 bps, 2017-2026 "
        "read ONCE")
    wf = []
    g10 = grid[grid.cost == PROTOCOL_COST]
    for (pn, fq, dl), s in g10.groupby(["panel", "cadence", "dial"]):
        s = s.sort_values("slow_pre")
        pick = s.loc[s.is_Sharpe.idxmax()]
        full_arg = s.loc[s.Sharpe.idxmax()]
        wf.append(dict(panel=pn, cadence=fq, dial=dl, is_pick=pick.rung,
                       full_argmax=full_arg.rung, same=bool(pick.rung == full_arg.rung),
                       oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                       oos_MaxDD=pick.oos_MaxDD, keep4b_oos=bool(pick.keep4b_oos),
                       keep4b=bool(pick.keep4b), keep4a=bool(pick.keep4a),
                       oos_rank=int((s.oos_Sharpe > pick.oos_Sharpe).sum()) + 1,
                       n_rungs=len(s)))
        log(f"  {pn:5s} {fq} {dl:8s} IS pick={str(pick.rung):>4s} (FULL argmax "
            f"{str(full_arg.rung):>4s}) -> OOS {pick.oos_CAGR:6.2%} / {pick.oos_Sharpe:6.4f} / "
            f"{pick.oos_MaxDD:7.2%}  rank {int((s.oos_Sharpe > pick.oos_Sharpe).sum())+1} of "
            f"{len(s)}  4b_OOS={str(bool(pick.keep4b_oos)):5s}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    log(f"\n  IS pick == FULL argmax on {int(wfd.same.sum())} of {len(wfd)} instances; "
        f"mean OOS rank {wfd.oos_rank.mean():.2f} of {wfd.n_rungs.mean():.1f}; "
        f"4b OOS {int(wfd.keep4b_oos.sum())}/{len(wfd)}; "
        f"4b FULL+OOS {int(wfd.keep4b.sum())}/{len(wfd)}; 4a FULL {int(wfd.keep4a.sum())}/{len(wfd)}")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    log(f"\n# wrote {Path(str(OUT)+'.grid.csv').name}, .argmax.csv, .instances.csv, "
        f".walkforward.csv, .gates.csv, .log.txt")


if __name__ == "__main__":
    main()

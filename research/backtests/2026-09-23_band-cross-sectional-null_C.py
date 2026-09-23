#!/usr/bin/env python3
"""idea 2539 (lane C, run 69, 2026-09-23) — IS THE 200d BAND's CROSS-SECTIONAL PICK WORTH
ANYTHING, PRICED AGAINST A BREADTH-MATCHED RANDOM NULL AND AN ANTI-BAND COMPLEMENT?

THE QUESTION.  The standing 4b KEEP-candidate holds every name inside the 200d +/- 3% band at
`min(g/n_t, cap)` of NAV and sweeps the idle remainder to SHY.  Idea 2506 proved that is an
EXPOSURE SCHEDULE (`G_t = min(g, cap x n_t)`) as much as a stock picker, and idea 2532 found
the candidate behind an all-names blend AT ITS OWN GROSS PATH on CAGR in 128 of 128 rows.
That IMPLIES the in-band SUBSET is a NEGATIVE cross-sectional pick, but the record has never
priced the implication against a null that holds the band's OWN BREADTH fixed: every placebo
in the record is turnover-matched (2499), ticket-matched (2512) or gross-matched (1723, 2532),
never COUNT-matched.  Idea 2520 (pushed hours before this run) closes with the same ask in
terms: "an exposure-matched re-run of it is the obvious next idea."

THE NULL THIS RUN BUILDS.  On every rebalance date the band admits n_t of the N_t priced names
at a per-name weight of per_t = min(g/n_t, cap).  RAND_s draws n_t names UNIFORMLY AT RANDOM
from the same priced set and holds them at the IDENTICAL per_t.  Count, per-name weight, risk
gross, cadence, sweep, tape and days are therefore identical BY CONSTRUCTION and the ONLY
thing that differs is WHICH names.  16 md5-seeded draws give a seed distribution, so the
band's cross-sectional value is reported with its own resolution floor instead of as a point.

RAND_STICKY is the TURNOVER-MATCHED twin of RAND: it keeps last week's random names and trades
only the count difference, so the pair brackets the cost axis from both sides (plain RAND
re-draws the whole book weekly and would otherwise be priced as a cost artefact).

ANTI_ALL holds every OUT-of-band priced name at the band's own gross m_t (the complement, no
seed).  ANTI_s is its count-matched twin: min(n_t, o_t) names drawn at random from the
out-of-band set at the same gross.  ALL holds every priced name at m_t (idea 2532's BLEND_RB
rebuilt here so the two runs can be tied together).

DIAL 1 -- gross g in {0.75 (live), 1.00}.
DIAL 2 -- cap c in {0.020 (the committed CAP2 clause), INF (idea 2300's uncapped CAND, where
          m_t = g is CONSTANT and the exposure schedule is switched off entirely)}.
Exactly two tuned parameters (G12).

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, weekly
cadence, band 0.03, t+1 execution, the SHY sweep, and the seed count K = 16.

BOTH KEEP PATHS on every book-row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no
worse) and 4b under SPY *and* under EWBH(panel) -- idea 2516's proposed wording, where the two
disagree the EWBH verdict is the one quoted.
RULE 8: (arm, gross) fitted on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers,
2017-2026 then read ONCE, and OOS CAGR / Sharpe / MaxDD reported against the live baseline and
against SPY.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_band-cross-sectional-null_C.py
"""
from __future__ import annotations

import hashlib, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest, rebalance_mask                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "band-cross-sectional-null", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
GROSSES = [0.75, 1.00]
CAPS = {"0.020": 0.020, "INF": np.inf}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
K_SEEDS = 16
BASE_GROSS = 0.75                       # the LIVE book's gross, for the 4a comparand
ARMS_FIXED = ["BAND", "ANTI_ALL", "ALL"]
ARMS_SEEDED = ["RAND", "RAND_STICKY", "ANTI"]
BENCHES = ["SPY", "EWBH"]

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
    say(f"    PUB   {name}: {value}")


def seed_of(*parts):
    return int(hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()[:8], 16)


# ---------------------------------------------------------------- metrics
def cagr(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    return float(eq.iloc[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float((r.mean() * 252) / v) if v else np.nan


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


# ---------------------------------------------------------------- the arms
def cell_shapes(px, invest, gross, cap):
    """Everything the arms share: the priced mask, the band mask, the breadth n_t, the
    per-name weight per_t = min(g/n_t, cap) and the risk gross m_t = per_t x n_t."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    n = inb.sum(axis=1)
    per = pd.Series(np.where(n > 0, gross / n.replace(0, np.nan), 0.0), index=q.index).fillna(0.0)
    per = per.clip(upper=cap) if np.isfinite(cap) else per
    m = per * n
    return pr, inb, n, per, m


def frame_from_rows(px, invest, rows):
    """rows: {position -> (column positions, per-name weight)} on rebalance days only.
    Non-rebalance rows inherit the previous target (the engine only reads mask days; the
    forward fill makes the frame convention-independent).  Idle NAV is swept to SWEEP.
    Returns the post-sweep frame AND the PRE-SWEEP row sum, which is the arm's RISK GROSS
    (the sweep sleeve must not be netted out of it -- SWEEP is also an investable name)."""
    C = len(px.columns)
    col_of = {c: i for i, c in enumerate(px.columns)}
    inv_pos = np.array([col_of[c] for c in invest])
    W = np.full((len(px.index), C), np.nan)
    for i, (sel, w) in rows.items():
        W[i, :] = 0.0
        if len(sel):
            W[i, inv_pos[sel]] = w
    pre = pd.DataFrame(W, index=px.index, columns=px.columns).ffill().fillna(0.0)
    risk = pre.sum(axis=1)
    out = pre.copy()
    idle = (1.0 - risk).clip(lower=0.0)
    out[SWEEP] = out[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return out, risk


def build_arm(px, invest, gross, cap, arm, seed=None):
    """Every arm holds a SUBSET of the priced names at a weight chosen so the RISK GROSS equals
    the band's own m_t on the same day.  BAND/RAND additionally hold the same COUNT n_t at the
    same per-name weight per_t."""
    pr, inb, n, per, m = cell_shapes(px, invest, gross, cap)
    reb = rebalance_mask(px.index, CADENCE)
    prv, inbv = pr.values, inb.values
    nv, perv, mv = n.values, per.values, m.values
    rng = np.random.default_rng(seed) if seed is not None else None
    rows, counts = {}, np.zeros(len(px.index))
    prev = np.array([], int)
    empty = 0
    idx = np.flatnonzero(reb.values | (np.arange(len(px.index)) == 0))
    for i in idx:
        priced = np.flatnonzero(prv[i])
        band = np.flatnonzero(inbv[i])
        k = int(nv[i])
        if arm == "BAND":
            sel, w = band, perv[i]
        elif arm == "ALL":
            sel = priced
            w = mv[i] / len(priced) if len(priced) else 0.0
        elif arm == "ANTI_ALL":
            sel = np.setdiff1d(priced, band, assume_unique=False)
            w = mv[i] / len(sel) if len(sel) else 0.0
        elif arm == "RAND":
            sel = rng.choice(priced, size=min(k, len(priced)), replace=False) if k else np.array([], int)
            w = perv[i]
        elif arm == "RAND_STICKY":
            # the TURNOVER-MATCHED null: keep last week's random names, trade only the count
            # difference.  Plain RAND re-draws the whole book weekly and would be priced as a
            # cost artefact at any non-zero rung; this arm brackets that axis from below.
            keep = np.intersect1d(prev, priced)
            kk = min(k, len(priced))
            if len(keep) > kk:
                keep = rng.choice(keep, size=kk, replace=False) if kk else np.array([], int)
            elif len(keep) < kk:
                pool = np.setdiff1d(priced, keep)
                keep = np.concatenate([keep, rng.choice(pool, size=min(kk - len(keep), len(pool)), replace=False)])
            sel = np.sort(keep.astype(int))
            prev = sel
            w = perv[i]
        elif arm == "ANTI":
            out_of = np.setdiff1d(priced, band, assume_unique=False)
            kk = min(k, len(out_of))
            sel = rng.choice(out_of, size=kk, replace=False) if kk else np.array([], int)
            w = mv[i] / kk if kk else 0.0
        else:
            raise ValueError(arm)
        sel = np.asarray(sel, int)
        if len(sel) == 0 and nv[i] > 0:
            empty += 1                       # complement exhausted: the arm cannot carry m_t
        rows[i] = (sel, float(w))
        counts[i] = len(sel)
    frame, risk = frame_from_rows(px, invest, rows)
    return frame, counts, idx, risk, empty


def run_zero(px, w):
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return res["returns"], res["turnover"], res["weights"]


def priced_r(r0, turn, bps):
    return r0 - turn * bps / 1e4


# ---------------------------------------------------------------- benchmarks
def ewbh(px, cols, start):
    """Equal-weight buy-and-hold of the panel's own names, bought on the last warm-up close and
    never traded again (idea 2516's comparand, same convention as 4b's SPY leg)."""
    pos = px.index.get_loc(start)
    q = px[cols].iloc[pos - 1:]
    live = q.iloc[0].notna()
    q = q.loc[:, live]
    val = (q / q.iloc[0]).mean(axis=1)
    return val.pct_change().dropna(), int(live.sum())


# ---------------------------------------------------------------- KEEP paths
def legs_4b(r, b):
    r1, r2 = halves(r); b1, b2 = halves(b)
    ro, bo = r.loc[OOS_START:], b.loc[OOS_START:]
    mm = dict(L_H1=sharpe(r1) - sharpe(b1), L_H2=sharpe(r2) - sharpe(b2),
              L_OOS=sharpe(ro) - sharpe(bo), L_DD=maxdd(r) - DD_CAP * maxdd(b),
              L_CAGR=cagr(r) - CAGR_FLOOR * cagr(b))
    ok = {k: bool(v > 0) for k, v in mm.items()}
    first = next((k for k in ("L_CAGR", "L_DD", "L_H1", "L_H2", "L_OOS") if not ok[k]), "")
    return dict(pass4b=all(ok.values()), first_fail=first,
                **{k: ok[k] for k in mm}, **{f"m_{k}": float(v) for k, v in mm.items()})


def pass_4a(r, base):
    r1, r2 = halves(r); b1, b2 = halves(base)
    return bool(sharpe(r1) > sharpe(b1) and sharpe(r2) > sharpe(b2) and maxdd(r) >= maxdd(base))


def row_of(r, turn, win, yrs):
    ro = r.loc[OOS_START:]
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(halves(r)[0]), H2=sharpe(halves(r)[1]),
                OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                IS_MaxDD=maxdd(r.loc[:IS_END]),
                turnover_yr=float(turn.loc[win].sum() / yrs))


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=== idea 2539 (lane C, run 69) — is the 200d band's CROSS-SECTIONAL pick worth anything "
        "against a BREADTH-MATCHED RANDOM null and an ANTI-BAND complement? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 gross {GROSSES}   DIAL 2 cap {list(CAPS)}   K = {K_SEEDS} md5 seeds")
    say(f"    REPORTED not selected: panels U56/B136, rungs {RUNGS}, cadence {CADENCE}, band {BAND}, K")
    gate("G12 exactly two tuned parameters", "gross, cap", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        win = px.index[WARMUP:]
        panels[nm] = (px, invest, win)
        yrs = (px.index[-1] - win[0]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} cols, {len(px)} rows, scored from {win[0].date()}",
             ">= 10y", yrs >= 10)
        gate(f"G1 sweep {SWEEP} priced on every scored row ({nm})",
             f"{int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    # ------------------------------------------------ benchmarks + 4a comparand per panel
    B, BASE = {}, {}
    for pname, (px, invest, win) in panels.items():
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        e, nbuy = ewbh(px, invest, win[0])
        B[pname] = dict(SPY=spy, EWBH=e.loc[win])
        r0, tu, _ = run_zero(px, rules_v2_weights(px[invest], band=BAND, gross=BASE_GROSS)
                             .reindex(columns=px.columns).fillna(0.0))
        BASE[pname] = (r0, tu)
        for bn in BENCHES:
            s = B[pname][bn]
            say(f"    BENCH {pname:5s} {bn:5s} CAGR {cagr(s):7.2%}  Sharpe {sharpe(s):7.4f}  MaxDD {maxdd(s):7.2%}"
                f"  H1/H2 {sharpe(halves(s)[0]):.4f}/{sharpe(halves(s)[1]):.4f}"
                f"  OOS {cagr(s.loc[OOS_START:]):7.2%}/{sharpe(s.loc[OOS_START:]):.4f}/{maxdd(s.loc[OOS_START:]):7.2%}")
        publish(f"G2 EWBH cohort ({pname})", f"{nbuy} of {len(invest)} names bought {win[0].date()}")

    # ------------------------------------------------ the grid
    rows, gross_chk, count_chk = [], [], []
    for pname, (px, invest, win) in panels.items():
        yrs = len(win) / 252
        base_r = priced_r(*BASE[pname], HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} cols)   live RULES v2 g{BASE_GROSS} @10bps "
            f"{cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for gross in GROSSES:
            for cname, cap in CAPS.items():
                _, _, nser, _, mser = cell_shapes(px, invest, gross, cap)
                plan = [(a, None) for a in ARMS_FIXED] + \
                       [(a, s) for a in ARMS_SEEDED for s in range(K_SEEDS)]
                for arm, s in plan:
                    sd = None if s is None else seed_of(pname, gross, cname, arm, s)
                    w, counts, idx, risk, empty = build_arm(px, invest, gross, cap, arm, sd)
                    r0, tu, _held = run_zero(px, w)
                    # exposure / count audits on the DECIDED frame, at SCORED rebalance dates only
                    sidx = idx[idx >= WARMUP]
                    dec_risk = risk.iloc[sidx]
                    want = mser.iloc[sidx]
                    live_sel = counts[sidx] > 0
                    dev = float((dec_risk[live_sel] - want[live_sel]).abs().max()) if live_sel.any() else 0.0
                    gross_chk.append(dict(panel=pname, gross=gross, cap=cname, arm=arm, seed=s,
                                          mean_dec_risk=float(dec_risk.mean()), mean_m=float(want.mean()),
                                          empty_dates=int(empty), max_abs_dev=dev))
                    if arm in ("BAND", "RAND", "RAND_STICKY"):
                        count_chk.append(float(np.abs(counts[sidx] - nser.values[sidx]).max()))
                    base_r0, base_tu = BASE[pname]
                    for bps in RUNGS:
                        r = priced_r(r0, tu, bps).loc[win]
                        br = priced_r(base_r0, base_tu, bps).loc[win]
                        d = dict(panel=pname, gross=gross, cap=cname, arm=arm, seed=s, bps=bps,
                                 **row_of(r, tu, win, yrs),
                                 mean_risk_gross=float(dec_risk.mean()),
                                 mean_names=float(counts[sidx].mean()),
                                 pass4a=pass_4a(r, br))
                        for bn in BENCHES:
                            for k, v in legs_4b(r, B[pname][bn]).items():
                                d[f"{bn}:{k}"] = v
                        rows.append(d)
                say(f"    [{pname} g{gross} cap {cname}] {len(plan)} arms priced  "
                    f"(mean breadth {nser.iloc[sidx].mean():.1f} of {len(invest)}, "
                    f"mean risk gross {mser.iloc[sidx].mean():.4f})   t={time.time()-t0:.0f}s")
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    pd.DataFrame(gross_chk).to_csv(f"{OUT}.exposure.csv", index=False)
    say(f"\n[grid] {len(G)} book-rows "
        f"({len(panels)} panels x {len(GROSSES)} gross x {len(CAPS)} caps x "
        f"{len(ARMS_FIXED)+len(ARMS_SEEDED)*K_SEEDS} arms x {len(RUNGS)} rungs)")

    # ------------------------------------------------ construction gates
    c = G[(G.panel == "U56") & (G.arm == "BAND") & (G.gross == 0.75) & (G.cap == "0.020") & (G.bps == 10.0)].iloc[0]
    d3 = max(abs(c.CAGR - 0.1162), abs(c.Sharpe - 1.2687), abs(c.MaxDD + 0.1481))
    gate("G3 BAND reproduces the committed CAP2 U56 g0.75 @10bps headline (11.62% / 1.2687 / -14.81%)",
         f"{c.CAGR:.2%} / {c.Sharpe:.4f} / {c.MaxDD:.2%}, max|d| {d3:.2e}", "< 5e-4", d3 < 5e-4)
    gate("G4 the committed candidate still passes 4b under SPY", f"{bool(c['SPY:pass4b'])}", "True",
         bool(c["SPY:pass4b"]))
    EX = pd.DataFrame(gross_chk)
    gate("G5 EVERY arm carries the band's OWN risk gross on every scored rebalance date",
         f"max|dev| {EX.max_abs_dev.max():.3e} over {len(EX)} arms", "< 1e-9", EX.max_abs_dev.max() < 1e-9)
    publish("G5b dates on which an arm's selection set was EMPTY while the band held names "
            "(complement exhausted; the arm sits in the sweep and is NOT gross-matched there)",
            f"{int(EX.empty_dates.sum())} over {len(EX)} arms; worst single arm {int(EX.empty_dates.max())}")
    gate("G6 RAND and RAND_STICKY hold EXACTLY the band's breadth n_t on every scored rebalance date",
         f"max|dcount| {max(count_chk):.0f}", "0", max(count_chk) == 0)
    # determinism
    w1 = build_arm(*panels["U56"][:2], 0.75, 0.020, "RAND", seed_of("U56", 0.75, "0.020", "RAND", 0))[0]
    w2 = build_arm(*panels["U56"][:2], 0.75, 0.020, "RAND", seed_of("U56", 0.75, "0.020", "RAND", 0))[0]
    gate("G7 seeded draws are deterministic", f"max|dw| {float((w1-w2).abs().max().max()):.3e}", "0.0",
         float((w1 - w2).abs().max().max()) == 0.0)
    # no-lookahead: truncating the tape must not change any decision before the cut
    px_u, inv_u, win_u = panels["U56"]
    cut = px_u.index[len(px_u) // 2]
    wf = build_arm(px_u, inv_u, 0.75, 0.020, "BAND")[0]
    wt = build_arm(px_u.loc[:cut], inv_u, 0.75, 0.020, "BAND")[0]
    dl = float((wf.loc[:cut] - wt).abs().max().max())
    gate("G8 no look-ahead (tape truncated at the midpoint)", f"max|dw| {dl:.3e}", "0.0", dl == 0.0)
    # idea 2506's identity on the BAND arm
    wb, _, idxb, _, _ = build_arm(px_u, inv_u, 0.75, 0.020, "BAND")
    hb = wb.drop(columns=[SWEEP]).iloc[idxb[idxb >= WARMUP]]
    spread = float((hb.where(hb > 0).max(axis=1) - hb.where(hb > 0).min(axis=1)).max())
    gate("G9 idea 2506's identity: every held BAND name carries the SAME weight",
         f"max(max-min) {spread:.3e}", "< 1e-15", spread < 1e-15)
    inf_g = G[G.cap == "INF"].groupby("gross").mean_risk_gross.agg(["min", "max"])
    abs_g = G[G.cap == "0.020"].groupby(["panel", "gross"]).mean_risk_gross.mean()
    publish("G10 cap=INF switches the exposure schedule off (mean risk gross by gross, min/max over arms)",
            ", ".join(f"g{g}: {r['min']:.4f}..{r['max']:.4f}" for g, r in inf_g.iterrows()))
    publish("G10b cap=0.020 mean risk gross (the exposure schedule, idea 2506)",
            ", ".join(f"{k}: {v:.4f}" for k, v in abs_g.items()))
    publish("G11 seed count", f"K = {K_SEEDS} md5-seeded draws per (panel, gross, cap) for each of {ARMS_SEEDED}")
    tv = G[G.bps == HEADLINE_RUNG].groupby(["panel", "arm"]).turnover_yr.median()
    publish("G11b median turnover by arm (x NAV/yr) -- the null's OWN cost handicap, stated not hidden",
            "; ".join(f"{p}/{a} {v:.2f}" for (p, a), v in tv.items()))
    publish("G11c the draw pool", "every arm draws from the SAME priced set as the band, which under the "
            "committed convention includes the SPY and SHY columns; the SHY sweep is applied identically to all arms")

    # ------------------------------------------------ THE ANSWER: band vs its own null
    say("\n=== Q1 — IS THE BAND's PICK BETTER THAN CHANCE AT ITS OWN BREADTH? "
        "(BAND minus the RAND null, identical count / per-name weight / gross) ===")
    cmp_rows = []
    for (pname, gross, cname, bps), g in G.groupby(["panel", "gross", "cap", "bps"]):
        band = g[g.arm == "BAND"].iloc[0]
        rnd = g[g.arm == "RAND"]
        stk = g[g.arm == "RAND_STICKY"]
        anti = g[g.arm == "ANTI"]
        antA = g[g.arm == "ANTI_ALL"].iloc[0]
        alll = g[g.arm == "ALL"].iloc[0]
        for lab, v in (("Sharpe", "Sharpe"), ("CAGR", "CAGR"), ("MaxDD", "MaxDD"),
                       ("OOS_Sharpe", "OOS_Sharpe"), ("turnover_yr", "turnover_yr")):
            sd = float(rnd[v].std(ddof=1)); sds = float(stk[v].std(ddof=1))
            cmp_rows.append(dict(panel=pname, gross=gross, cap=cname, bps=bps, stat=lab,
                                 band=float(band[v]), rand_med=float(rnd[v].median()),
                                 rand_sd=sd, stick_med=float(stk[v].median()), stick_sd=sds,
                                 anti_med=float(anti[v].median()),
                                 anti_all=float(antA[v]), all_=float(alll[v]),
                                 d_band_rand=float(band[v]) - float(rnd[v].median()),
                                 d_band_stick=float(band[v]) - float(stk[v].median()),
                                 z=(float(band[v]) - float(rnd[v].mean())) / sd if sd > 0 else np.nan,
                                 z_stick=(float(band[v]) - float(stk[v].mean())) / sds if sds > 0 else np.nan,
                                 pctile=float((rnd[v] < float(band[v])).mean()),
                                 pctile_stick=float((stk[v] < float(band[v])).mean()),
                                 d_band_all=float(band[v]) - float(alll[v])))
    CMP = pd.DataFrame(cmp_rows)
    CMP.to_csv(f"{OUT}.null_contrast.csv", index=False)
    ncells = len(panels) * len(GROSSES) * len(CAPS) * len(RUNGS)
    for stat in ("Sharpe", "CAGR", "MaxDD", "OOS_Sharpe", "turnover_yr"):
        q = CMP[CMP.stat == stat]
        say(f"\n  -- {stat} --   ({ncells} cells = {len(panels)} panels x {len(GROSSES)} gross "
            f"x {len(CAPS)} caps x {len(RUNGS)} rungs)")
        for pname in ("U56", "B136"):
            s = q[q.panel == pname]
            say(f"    {pname:5s} vs RAND (weekly re-draw)  ahead in {int((s.d_band_rand > 0).sum()):2d}/{len(s)}"
                f" | median d {s.d_band_rand.median():+.4f} | median z {s.z.median():+7.2f}"
                f" | seed sd {s.rand_sd.median():.4f} | pctile {s.pctile.median():.2f}")
            say(f"          vs RAND_STICKY (turnover-matched) ahead in {int((s.d_band_stick > 0).sum()):2d}/{len(s)}"
                f" | median d {s.d_band_stick.median():+.4f} | median z {s.z_stick.median():+7.2f}"
                f" | seed sd {s.stick_sd.median():.4f} | pctile {s.pctile_stick.median():.2f}")
            say(f"          vs ANTI_ALL {(s.band - s.anti_all).median():+.4f} (ahead {int((s.band > s.anti_all).sum()):2d}/{len(s)})"
                f" | vs ANTI(count-matched) {(s.band - s.anti_med).median():+.4f} (ahead {int((s.band > s.anti_med).sum()):2d}/{len(s)})"
                f" | vs ALL {s.d_band_all.median():+.4f} (ahead {int((s.d_band_all > 0).sum()):2d}/{len(s)})")

    say("\n  headline cell (U56, g0.75, cap 0.020, 10 bps):")
    h = CMP[(CMP.panel == "U56") & (CMP.gross == 0.75) & (CMP.cap == "0.020") & (CMP.bps == 10.0)]
    for _, r in h.iterrows():
        say(f"    {r.stat:11s} BAND {r.band:+.4f} | RAND {r.rand_med:+.4f} (sd {r.rand_sd:.4f}, z {r.z:+.2f}, "
            f"pctile {r.pctile:.2f}) | RAND_STICKY {r.stick_med:+.4f} (sd {r.stick_sd:.4f}, z {r.z_stick:+.2f}) "
            f"| ANTI_ALL {r.anti_all:+.4f} | ANTI {r.anti_med:+.4f} | ALL {r.all_:+.4f}")

    # ------------------------------------------------ KEEP paths
    say("\n=== BOTH KEEP PATHS over all book-rows ===")
    for arm in ARMS_FIXED + ARMS_SEEDED:
        q = G[G.arm == arm]
        say(f"    {arm:9s} n={len(q):4d}   4a {int(q.pass4a.sum()):4d}"
            f"   4b|SPY {int(q['SPY:pass4b'].sum()):4d}   4b|EWBH {int(q['EWBH:pass4b'].sum()):4d}")
    say("    first-binding leg under EWBH (all rows): " +
        ", ".join(f"{k} {v}" for k, v in G[~G['EWBH:pass4b']].groupby('EWBH:first_fail').size().sort_values(ascending=False).items()))
    say("    first-binding leg under SPY  (all rows): " +
        ", ".join(f"{k} {v}" for k, v in G[~G['SPY:pass4b']].groupby('SPY:first_fail').size().sort_values(ascending=False).items()))
    for arm in ARMS_FIXED:
        q = G[(G.arm == arm) & (G.bps == HEADLINE_RUNG)]
        for pname in ("U56", "B136"):
            s = q[q.panel == pname]
            say(f"    @10bps {arm:9s} {pname:5s}  CAGR {s.CAGR.median():7.2%}  Sharpe {s.Sharpe.median():7.4f}"
                f"  MaxDD {s.MaxDD.median():7.2%}  turnover {s.turnover_yr.median():5.2f}x/yr"
                f"  4b|SPY {int(s['SPY:pass4b'].sum())}/{len(s)}  4b|EWBH {int(s['EWBH:pass4b'].sum())}/{len(s)}")

    # ------------------------------------------------ RULE 8
    say("\n=== RULE 8 — (arm, gross) fitted on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE ===")
    CHOOSERS = {"C_ISSHARPE": lambda d: d.IS_Sharpe,
                "C_ISCALMAR": lambda d: d.IS_CAGR / d.IS_MaxDD.abs().replace(0, np.nan)}
    picks = []
    pool = G[G.arm.isin(ARMS_FIXED)]
    for (pname, cname, bps), g in pool.groupby(["panel", "cap", "bps"]):
        base_r0, base_tu = BASE[pname]
        win = panels[pname][2]
        br = priced_r(base_r0, base_tu, bps).loc[win]
        spy_o = B[pname]["SPY"].loc[OOS_START:]
        ewb_o = B[pname]["EWBH"].loc[OOS_START:]
        for chn, fn in CHOOSERS.items():
            w = g.loc[fn(g).idxmax()]
            picks.append(dict(panel=pname, cap=cname, bps=bps, chooser=chn, arm=w.arm, gross=w.gross,
                              OOS_CAGR=w.OOS_CAGR, OOS_Sharpe=w.OOS_Sharpe, OOS_MaxDD=w.OOS_MaxDD,
                              base_OOS_CAGR=cagr(br.loc[OOS_START:]), base_OOS_Sharpe=sharpe(br.loc[OOS_START:]),
                              base_OOS_MaxDD=maxdd(br.loc[OOS_START:]),
                              spy_OOS_CAGR=cagr(spy_o), spy_OOS_Sharpe=sharpe(spy_o), spy_OOS_MaxDD=maxdd(spy_o),
                              ewbh_OOS_Sharpe=sharpe(ewb_o), ewbh_OOS_CAGR=cagr(ewb_o),
                              beat_base=bool(w.OOS_Sharpe > sharpe(br.loc[OOS_START:])),
                              beat_spy=bool(w.OOS_Sharpe > sharpe(spy_o)),
                              beat_ewbh=bool(w.OOS_Sharpe > sharpe(ewb_o)),
                              full4b_SPY=bool(w["SPY:pass4b"]), full4b_EWBH=bool(w["EWBH:pass4b"])))
    P = pd.DataFrame(picks)
    P.to_csv(f"{OUT}.rule8.csv", index=False)
    say(f"    {len(P)} picks (2 choosers x 2 panels x 2 caps x 4 rungs) over arms {ARMS_FIXED} x gross {GROSSES}")
    say("    arm chosen IN SAMPLE: " + ", ".join(f"{k} {v}" for k, v in P.arm.value_counts().items()) +
        "   | gross: " + ", ".join(f"{k} {v}" for k, v in P.gross.value_counts().items()))
    say(f"    OOS Sharpe beats SPY in {int(P.beat_spy.sum())} of {len(P)}; beats the LIVE baseline in "
        f"{int(P.beat_base.sum())} of {len(P)}; beats EWBH(panel) in {int(P.beat_ewbh.sum())} of {len(P)}")
    say(f"    full-sample 4b carried by the pick: SPY {int(P.full4b_SPY.sum())} of {len(P)}, "
        f"EWBH {int(P.full4b_EWBH.sum())} of {len(P)}")
    for pname in ("U56", "B136"):
        s = P[P.panel == pname]
        say(f"    {pname:5s} OOS mean  pick {s.OOS_CAGR.mean():7.2%} / {s.OOS_Sharpe.mean():.4f} / {s.OOS_MaxDD.mean():7.2%}"
            f"  || baseline {s.base_OOS_CAGR.mean():7.2%} / {s.base_OOS_Sharpe.mean():.4f} / {s.base_OOS_MaxDD.mean():7.2%}"
            f"  || SPY {s.spy_OOS_CAGR.mean():7.2%} / {s.spy_OOS_Sharpe.mean():.4f} / {s.spy_OOS_MaxDD.mean():7.2%}"
            f"  || EWBH {s.ewbh_OOS_CAGR.mean():7.2%} / {s.ewbh_OOS_Sharpe.mean():.4f}")

    # a PRE-REGISTERED, zero-fitted arm for contrast: the committed BAND at g0.75
    for pname in ("U56", "B136"):
        pr0 = G[(G.panel == pname) & (G.arm == "BAND") & (G.gross == 0.75) & (G.cap == "0.020") & (G.bps == HEADLINE_RUNG)].iloc[0]
        say(f"    C_PREREG {pname:5s} (BAND g0.75 cap 0.020 @10bps, zero-fitted): "
            f"OOS {pr0.OOS_CAGR:.2%} / {pr0.OOS_Sharpe:.4f} / {pr0.OOS_MaxDD:.2%}")

    # ------------------------------------------------ leaderboard rows
    lb = []
    for pname in ("U56", "B136"):
        for arm in ARMS_FIXED:
            r = G[(G.panel == pname) & (G.arm == arm) & (G.gross == 0.75) & (G.cap == "0.020") & (G.bps == HEADLINE_RUNG)].iloc[0]
            v = "KEEP-4b" if r["EWBH:pass4b"] else ("KILL" if not r["SPY:pass4b"] else "KILL (SPY-only 4b, fails EWBH)")
            lb.append(f"| {DATE} | 2539 {arm} {pname} g0.75 cap0.020 @10bps | {r.CAGR:.1%} | {r.Sharpe:.2f} | "
                      f"{r.MaxDD:.1%} | {r.H1:.2f} / {r.H2:.2f} | OOS {r.OOS_CAGR:.1%}/{r.OOS_Sharpe:.2f}/{r.OOS_MaxDD:.1%} | "
                      f"{v} | {Path(__file__).name} |")
        for nullarm in ("RAND", "RAND_STICKY"):
            rq = G[(G.panel == pname) & (G.arm == nullarm) & (G.gross == 0.75) & (G.cap == "0.020") & (G.bps == HEADLINE_RUNG)]
            lb.append(f"| {DATE} | 2539 {nullarm}-null median {pname} g0.75 cap0.020 @10bps (K={K_SEEDS}) | "
                      f"{rq.CAGR.median():.1%} | {rq.Sharpe.median():.2f} | {rq.MaxDD.median():.1%} | "
                      f"{rq.H1.median():.2f} / {rq.H2.median():.2f} | "
                      f"OOS {rq.OOS_CAGR.median():.1%}/{rq.OOS_Sharpe.median():.2f}/{rq.OOS_MaxDD.median():.1%} | NULL | "
                      f"{Path(__file__).name} |")
    Path(f"{OUT}.leaderboard.txt").write_text("\n".join(lb) + "\n")
    say("\nLEADERBOARD rows:\n" + "\n".join(lb))

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    ng = int((~gdf.pass_).sum())
    say(f"\n[gates] {int(gdf.pass_.sum())} of {len(gdf)} pass ({ng} fail)   elapsed {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ng == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

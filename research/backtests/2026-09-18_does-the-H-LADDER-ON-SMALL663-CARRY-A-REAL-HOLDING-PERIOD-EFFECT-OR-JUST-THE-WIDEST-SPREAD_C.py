#!/usr/bin/env python3
"""Idea 1274 (lane C, 2026-09-18): does the H LADDER on SMALL663 carry a REAL HOLDING-PERIOD
EFFECT, or is it just the WIDEST-SPREAD ladder?

QUESTION (the queue's, verbatim in substance).  Idea 1260's entire observed-side win is 2
distinct book choices, BOTH the H ladder on SMALL663 — H 126->252 worth +0.2143 of OOS Sharpe
and H 63->21 worth +0.1520.  The H ladder is also the widest-spread ladder on that panel, so a
margin/spread bar may simply be picking the ladder whose rungs differ most.  Dial H finely and
report whether the OOS gain is MONOTONE in H (a real holding-period effect) or a SPREAD artefact.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; both named by the queue):
    H      {21, 42, 63, 126, 189, 252, 378} MIN-HOLD days — the queue's own 7-rung ladder, which
           strictly CONTAINS 1260's committed {21, 63, 126, 252} (gate G5), so 1260's reading is
           a sub-ladder of this one and the two are directly comparable.
    PANEL  {U56, B136, SMALL663} — the queue names the panel as dial 2 and rule 9 requires all
           three anyway.
  7 x 3 = 21 cells, doubled by the ANCHOR control below to 42, EVERY ONE PUBLISHED in .grid.csv.

NOT DIALS, reported at every value: ANCHOR {A = N20/H126/g0.75/W (1101's, the standing
2026-09-04 book), B = N12/H63/g0.55/M} — 1260's own two, carried because its two headline steps
live one on each; the three IS-only choosers {CH_ISSHARPE, CH_ISCAGR, CH_ISDD}; both KEEP paths
leg by leg at every cell; full / halves / IS / OOS everywhere.

THE CONTROL SET THAT MAKES "WIDEST SPREAD" TESTABLE (a control, not a dial): 1260's other three
ladders N {5,8,10,12,15,20,25,30,40}, GROSS {0.30..0.75}, CADENCE {D,W,M,Q} at their committed
rungs, on both anchors and all three panels.  Without them "the H ladder is the widest" is not a
falsifiable sentence.  These books are built but their rungs are never chosen over — they enter
only the spread census.

FROZEN, NOT DIALS: 1101/1252's construction inherited whole — CAND composite of the 12-1 / 6m /
3m percentile ranks; eligibility = above own 200d MA AND 20d vol < 0.60; cap INF; equal weight
gross/len(selected), gated weight to CASH; 10 bps per unit turnover; next-day execution (LAG 1);
260-row warm-up; IS = warm-up..2016-12-31, OOS = 2017-01-01 onward READ ONCE; moving-block
bootstrap L = 63, 1000 draws, block index SHARED across the rungs of a ladder so the cross-rung
correlation that makes this dial hard to resolve is preserved rather than destroyed.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER
  SHAPE        the sign of each of the 6 adjacent OOS-Sharpe steps; MONOTONE iff all 6 agree;
               the argmax rung and whether it is INTERIOR; the same on IS Sharpe.
  RESOLUTION   each step's PAIRED block-bootstrap SE (same draws both rungs); DECISIVE at 2 SE.
  INTERPOLATION  1260's two headline jumps have a NEW rung inside them on this ladder (189 inside
               126->252, 42 inside 63->21).  A real holding-period effect interpolates: the new
               rung sits between its neighbours and the two half-steps carry the same sign as the
               whole.  A two-point coincidence does not.  This is the discriminating test.
  SPREAD       for every (panel, anchor, ladder): rung spread of IS Sharpe, the IS MARGIN
               (best - second), 1260's two observed-side scores S_OBS_MARGIN = margin / |anchor
               IS stat| and S_OBS_RATIO = margin / spread, and the REALISED OOS gain d of the
               ladder's IS argmax over its anchor rung.  Then rank corr(spread, score) and rank
               corr(spread, d): the bar is measuring spread iff the first is large and the
               second is not.
  CAPITAL      4a against live RULES v2 and 4b against SPY at every cell, leg by leg.
  RULE 8       each chooser picks H on the IS window ALONE over the 7 rungs; OOS read ONCE; the
               pick is scored against the ANCHOR rung (the do-nothing bar), the ladder mean, the
               best and worst rung, and SPY.  Run on the FINE 7-rung ladder AND on 1260's
               committed 4-rung sub-ladder, so the cost of REFINING the ladder is itself priced.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) REAL HOLDING-PERIOD EFFECT — on SMALL663 the OOS curve is MONOTONE at both anchors AND
      both of 1260's jumps INTERPOLATE AND the rule-8 pick beats the anchor there.
  (B) SPREAD ARTEFACT — the fine curve is non-monotone and ~no step clears 2 SE, the jumps do not
      interpolate, AND rank corr(spread, observed score) is large while rank corr(spread,
      realised d) is not.  Then the bar is a spread detector and 1260's fire set is its output.
  (C) REAL ELSEWHERE, NOT ON SMALL663 — monotone and resolved on the large-cap panels while
      SMALL663 is not.  Then H is a dial, but not the one 1260 fired on.
  (D) NEITHER — non-monotone AND spread fails to predict the observed score too.  Then 1260's two
      fires are a coincidence of two cells and "widest spread" is not the mechanism either.
  Whichever fires, the rule-8 pick-minus-anchor OOS delta is reported FIRST, because that is the
  only number that touches capital.

GATES.  G1 fast runner == engine.backtest on the U56 anchor-A book.  G2 CROSS-RUN that book's
(CAGR, Sharpe, MaxDD) == 1101/936/1082's committed (0.155787, 1.139701, -0.191276).  G3 CROSS-RUN
SPY OOS triple (0.1521, 0.8713, -0.3372).  G4 live RULES v2 MaxDD == -12.05%.  G5 the fine ladder
CONTAINS 1260's {21,63,126,252}.  G6 REPLAY 1260's two headline H steps on SMALL663 (+0.2143 at
A 126->252, +0.1520 at B 63->21).  G7 MECHANICAL: annual turnover is non-increasing in H at every
(panel, anchor) — a longer minimum hold cannot trade more.  G8 determinism: the anchor book
recomputes bit for bit.  G9 bootstrap determinism under a fixed seed.  G10 SMALL663 carries 663
investable columns.  G11 SPY is excluded from SMALL eligibility.  Every gate published, pass or
fail; a FAIL is a finding, not a reason to tolerance.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point, 2 dials; rule 5
one idea, one script, deterministic, standalone; rule 8 as above; rule 9 stated below.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before anything is
computed — the house 663-name construction idea 1272 adjudicated).  Every absolute level is
optimistic and every 4b pass is an UPPER bound.  The headline is a CONTRAST between rungs of one
ladder on one tape, first-order immune to a level bias that moves all rungs together; the 4a/4b
legs are not.

Runs standalone and offline (committed price caches only).
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-the-H-LADDER-ON-SMALL663-CARRY-A-REAL-HOLDING-PERIOD-EFFECT-OR-JUST-THE-WIDEST-SPREAD"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_C"

# ---- frozen construction (NOT dials) --------------------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BLOCK, NDRAW, SEED0 = 63, 1000, 12741274
SE_MULT = 2.0
COMMIT_TAPE_END = "2026-09-15"

# ---- the two dials ---------------------------------------------------------------------------
LAD_H_FINE = [21, 42, 63, 126, 189, 252, 378]      # dial 1, the queue's own ladder
LAD_H_1260 = [21, 63, 126, 252]                    # 1260's committed sub-ladder (gate G5)
PANELS = ["U56", "B136", "SMALL"]                  # dial 2

# ---- controls (reported at every value, never chosen over) -----------------------------------
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

# ---- the spread control set (1260's other three ladders, committed rungs) ---------------------
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
CTRL_LADDERS = {"N": LAD_N, "GROSS": LAD_G, "CADENCE": LAD_C}

# ---- committed cross-run constants (quoted and gated, never re-derived) ----------------------
C1101_TRIPLE = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
C1260_STEP_A = 0.2143     # SMALL663 anchor A, OOS Sharpe(H=252) - OOS Sharpe(H=126)
C1260_STEP_B = 0.1520     # SMALL663 anchor B, OOS Sharpe(H=21)  - OOS Sharpe(H=63)

_LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


def dump(df, suffix):
    p = Path(f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    say(f"   wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows_of(r, i_oos):
    h = len(r) // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                is_=stats(r[:i_oos]), oos=stats(r[i_oos:]))


def flat(w):
    return {f"{k}_{m}": v for k, d in w.items() for m, v in d.items()}


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return float("nan")
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


# ------------------------------------------------------------------ book machinery (1082's)
def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(A_H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                A_H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                A_DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(L_H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                L_H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                L_OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                L_DD=abs(bk["full"]["MaxDD"]) <= DD_CAP * abs(spy["full"]["MaxDD"]),
                L_CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def legs_4b_oos(bk, spy):
    return dict(O_S=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                O_DD=abs(bk["oos"]["MaxDD"]) <= DD_CAP * abs(spy["oos"]["MaxDD"]),
                O_CAGR=bk["oos"]["CAGR"] >= CAGR_FLOOR * spy["oos"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def stat_of(chooser, w):
    return {"CH_ISSHARPE": w["is_"]["Sharpe"], "CH_ISCAGR": w["is_"]["CAGR"],
            "CH_ISDD": w["is_"]["MaxDD"]}[chooser]


# ------------------------------------------------------------------ bootstrap
def boot_draws(R, seed):
    """Moving-block bootstrap, block index SHARED across the rows of R (the rungs)."""
    n, T = R.shape
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / BLOCK))
    starts = rng.integers(0, max(T - BLOCK + 1, 1), size=(NDRAW, nb))
    off = np.arange(BLOCK)
    out = np.empty((NDRAW, n))
    for d in range(NDRAW):
        idx = (starts[d][:, None] + off[None, :]).ravel()[:T]
        idx = np.minimum(idx, T - 1)
        X = R[:, idx]
        mu, sd = X.mean(axis=1), X.std(axis=1, ddof=0)
        out[d] = np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)
    return out


# ------------------------------------------------------------------ panel loading
def load_panel(panel):
    if panel == "SMALL":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
        keep = [c for c in px.columns if c == "SPY" or c not in bad]
        px = px[keep]
    else:
        px = load_universe(broad=(panel == "B136"))
    return px.dropna(how="all").ffill()


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1274 lane C — {SLUG}")
    say(f"# DIAL 1 H (MIN-HOLD days) = {LAD_H_FINE}   DIAL 2 PANEL = {PANELS}")
    say(f"# 1260's committed H ladder {LAD_H_1260} is a strict sub-ladder of dial 1 (gate G5)")
    say(f"# controls (not dials): ANCHOR {list(ANCHORS)}, choosers {CHOOSERS}, "
        f"spread ladders {list(CTRL_LADDERS)}")
    say(f"# frozen: CAND legs {LEGS}, elig above-200d & vol20<{MAXVOL}, cap INF, "
        f"{COST:.0f} bps, t+{LAG}, warm-up {WARMUP}, IS end {IS_END.date()}, OOS read once")
    say(f"# bootstrap L={BLOCK}, {NDRAW} draws, shared block index across rungs; DECISIVE at {SE_MULT:.0f} SE")
    say("# PRE-DECLARED: (A) real holding-period effect / (B) spread artefact / "
        "(C) real elsewhere not on SMALL663 / (D) neither")
    gate("G5 the fine 7-rung ladder CONTAINS 1260's {21,63,126,252}", LAD_H_1260,
         "all in " + str(LAD_H_FINE), all(h in LAD_H_FINE for h in LAD_H_1260))

    gridrows, steprows, spreadrows, r8rows, shaperows, ctrlrows = [], [], [], [], [], []

    for pi, panel in enumerate(PANELS):
        px = load_panel(panel)
        idx = px.index
        T, K = len(idx), len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        i_oos = int(idx.searchsorted(pd.Timestamp("2017-01-01")))
        pname = {"U56": "U56", "B136": f"B{K-1}", "SMALL": f"SMALL{K-1}"}[panel]
        yrs = (len(idx) - WARMUP) / 252.0
        spy_r = px["SPY"].pct_change().fillna(0.0).values
        live_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        sw = windows_of(spy_r[WARMUP:], i_oos - WARMUP)
        lw = windows_of(live_r[WARMUP:], i_oos - WARMUP)
        say(f"\n## {pname}  n_days={T}  n_cols={K}  {idx[0].date()}..{idx[-1].date()}  OOS row {i_oos}")
        say(f"   SPY     full {sw['full']['CAGR']:7.2%} / {sw['full']['Sharpe']:.4f} / {sw['full']['MaxDD']:7.2%}"
            f"   OOS {sw['oos']['CAGR']:7.2%} / {sw['oos']['Sharpe']:.4f} / {sw['oos']['MaxDD']:7.2%}")
        say(f"   4b caps: DD {DD_CAP*sw['full']['MaxDD']:.4%}, CAGR floor {CAGR_FLOOR*sw['full']['CAGR']:.4%}")
        say(f"   RULESv2 full {lw['full']['CAGR']:7.2%} / {lw['full']['Sharpe']:.4f} / {lw['full']['MaxDD']:7.2%}"
            f"   OOS {lw['oos']['CAGR']:7.2%} / {lw['oos']['Sharpe']:.4f} / {lw['oos']['MaxDD']:7.2%}")
        if panel == "SMALL":
            gate("G10 SMALL663 carries 663 investable columns", K - 1, "== 663", (K - 1) == 663)
            gate("G11 SPY excluded from SMALL eligibility", int(elig[:, spy_i].sum()), "== 0",
                 int(elig[:, spy_i].sum()) == 0)

        masks, rebs = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(idx, f).values
            rebs[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            masks[f] = m

        cache: dict[tuple, tuple] = {}

        def book(N, H, gross, freq):
            key = (N, H, gross, freq)
            if key not in cache:
                Wm = build(rank_key, elig, priced, rebs[freq], N, H, T, K, gross)
                gr, tn = nrun(rets, lagmat(Wm), masks[freq])
                cache[key] = (gr - tn * COST / 1e4, tn)
            return cache[key]

        def rung_book(anchor, lad, rung):
            a = dict(ANCHORS[anchor])
            a[lad] = rung
            return book(a["N"], a["H"], a["GROSS"], a["CADENCE"])

        # ---------------- gates on U56 only
        if pi == 0:
            a = ANCHORS["A"]
            Wm = build(rank_key, elig, priced, rebs[a["CADENCE"]], a["N"], a["H"], T, K, a["GROSS"])
            eng = backtest(px, pd.DataFrame(Wm, index=idx, columns=px.columns),
                           cost_bps=COST, freq=a["CADENCE"])["returns"].values
            r, _ = book(a["N"], a["H"], a["GROSS"], a["CADENCE"])
            d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - r[WARMUP:])))
            gate("G1 fast runner == engine.backtest (U56 anchor A)", f"{d1:.3e}", "< 1e-12", d1 < 1e-12)
            itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
            wl = windows_of(r[WARMUP:], i_oos - WARMUP)
            wt = windows_of(r[WARMUP:itr], i_oos - WARMUP)
            say(f"   U56 anchor A on the LIVE tape (ungated): {wl['full']['CAGR']:.6f}/"
                f"{wl['full']['Sharpe']:.6f}/{wl['full']['MaxDD']:.6f}")
            d2 = max(abs((wt["full"]["CAGR"], wt["full"]["Sharpe"], wt["full"]["MaxDD"])[i] - C1101_TRIPLE[i])
                     for i in range(3))
            gate(f"G2 CROSS-RUN U56 anchor A triple == 1101/936/1082's (tape to {COMMIT_TAPE_END})",
                 f"{wt['full']['CAGR']:.6f}/{wt['full']['Sharpe']:.6f}/{wt['full']['MaxDD']:.6f} "
                 f"maxdiff {d2:.2e}", f"{C1101_TRIPLE} < 5e-3", d2 < 5e-3)
            swt = windows_of(spy_r[WARMUP:itr], i_oos - WARMUP)
            d3 = max(abs((swt["oos"]["CAGR"], swt["oos"]["Sharpe"], swt["oos"]["MaxDD"])[i] - SPY_OOS_COMMITTED[i])
                     for i in range(3))
            gate(f"G3 CROSS-RUN SPY OOS triple (tape to {COMMIT_TAPE_END}; live tape "
                 f"{sw['oos']['CAGR']:.4f}/{sw['oos']['Sharpe']:.4f}/{sw['oos']['MaxDD']:.4f})",
                 f"{swt['oos']['CAGR']:.4f}/{swt['oos']['Sharpe']:.4f}/{swt['oos']['MaxDD']:.4f} "
                 f"maxdiff {d3:.2e}", f"{SPY_OOS_COMMITTED} < 5e-3", d3 < 5e-3)
            gate("G4 live RULES v2 MaxDD == committed -12.05%", f"{lw['full']['MaxDD']:.4f}",
                 f"{LIVE_MAXDD_COMMITTED} < 5e-4", abs(lw["full"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)

        # ---------------- the 42-cell grid: H x panel x anchor
        for anc in ANCHORS:
            for H in LAD_H_FINE:
                r, tn = rung_book(anc, "H", H)
                w = windows_of(r[WARMUP:], i_oos - WARMUP)
                a4, b4, o4 = legs_4a(w, lw), legs_4b(w, sw), legs_4b_oos(w, sw)
                gridrows.append(dict(panel=pname, anchor=anc, H=H,
                                     in_1260_ladder=int(H in LAD_H_1260),
                                     is_anchor_rung=int(H == ANCHORS[anc]["H"]),
                                     turn_yr=float(tn[WARMUP:].sum() / yrs), **flat(w),
                                     keep4a=all(a4.values()), keep4b=all(b4.values()),
                                     keep4b_oos=all(o4.values()),
                                     fail4a=failed(a4), fail4b=failed(b4), fail4b_oos=failed(o4),
                                     **a4, **b4, **o4))

        # ---------------- shape / resolution / interpolation / rule 8, per anchor
        for anc in ANCHORS:
            R = np.array([rung_book(anc, "H", H)[0][WARMUP:] for H in LAD_H_FINE])
            Wl = [windows_of(R[j], i_oos - WARMUP) for j in range(len(LAD_H_FINE))]
            S_oos = np.array([w["oos"]["Sharpe"] for w in Wl])
            S_is = np.array([w["is_"]["Sharpe"] for w in Wl])
            S_full = np.array([w["full"]["Sharpe"] for w in Wl])
            tn_yr = np.array([float(rung_book(anc, "H", H)[1][WARMUP:].sum() / yrs) for H in LAD_H_FINE])
            seed = zlib.crc32(f"{pname}|{anc}".encode()) ^ SEED0
            Rb = R[:, (i_oos - WARMUP):]                 # bootstrap the OOS window (the claim's window)
            B = boot_draws(Rb, seed)
            if pi == 0 and anc == "A":
                B2 = boot_draws(Rb, seed)
                gate("G9 bootstrap determinism (same seed, same draws)",
                     f"{float(np.abs(B - B2).max()):.3e}", "== 0.0", float(np.abs(B - B2).max()) == 0.0)
            signs, ndec = [], 0
            for j in range(len(LAD_H_FINE) - 1):
                step = S_oos[j + 1] - S_oos[j]
                se = float(np.nanstd(B[:, j + 1] - B[:, j], ddof=1))
                dec = bool(abs(step) >= SE_MULT * se) if se > 0 else False
                ndec += int(dec)
                signs.append(np.sign(step))
                steprows.append(dict(panel=pname, anchor=anc, H_lo=LAD_H_FINE[j], H_hi=LAD_H_FINE[j + 1],
                                     S_oos_lo=S_oos[j], S_oos_hi=S_oos[j + 1], step_oos=step,
                                     paired_SE=se, step_over_SE=(step / se if se > 0 else np.nan),
                                     decisive=dec, step_is=S_is[j + 1] - S_is[j],
                                     new_rung=int(LAD_H_FINE[j + 1] not in LAD_H_1260
                                                  or LAD_H_FINE[j] not in LAD_H_1260)))
            nz = np.array(signs)[np.array(signs) != 0]
            mono = bool(len(set(nz)) <= 1)
            jmax = int(np.nanargmax(S_oos))
            interior = bool(0 < jmax < len(LAD_H_FINE) - 1)
            order = np.argsort(S_oos)[::-1]
            gap_se = float(np.nanstd(B[:, order[0]] - B[:, order[1]], ddof=1))
            top_gap = float(S_oos[order[0]] - S_oos[order[1]])

            # INTERPOLATION of 1260's two headline jumps
            def interp(h_lo, h_mid, h_hi):
                a_, m_, b_ = (LAD_H_FINE.index(x) for x in (h_lo, h_mid, h_hi))
                lo, hi = min(S_oos[a_], S_oos[b_]), max(S_oos[a_], S_oos[b_])
                whole = S_oos[b_] - S_oos[a_]
                s1, s2 = S_oos[m_] - S_oos[a_], S_oos[b_] - S_oos[m_]
                return dict(between=bool(lo <= S_oos[m_] <= hi),
                            whole=float(whole), half1=float(s1), half2=float(s2),
                            same_sign=bool(np.sign(s1) == np.sign(whole) and np.sign(s2) == np.sign(whole)),
                            frac_mid=float(s1 / whole) if whole != 0 else np.nan)
                
            ia = interp(126, 189, 252)
            ib = interp(63, 42, 21)
            shaperows.append(dict(panel=pname, anchor=anc, monotone_oos=mono, n_decisive_steps=ndec,
                                  n_steps=len(LAD_H_FINE) - 1,
                                  argmax_H_oos=LAD_H_FINE[jmax], argmax_interior=interior,
                                  top_gap=top_gap, top_gap_SE=gap_se,
                                  top_gap_over_SE=(top_gap / gap_se if gap_se > 0 else np.nan),
                                  top_decisive=bool(top_gap >= SE_MULT * gap_se),
                                  argmax_H_is=LAD_H_FINE[int(np.nanargmax(S_is))],
                                  spread_oos=float(np.nanmax(S_oos) - np.nanmin(S_oos)),
                                  spread_is=float(np.nanmax(S_is) - np.nanmin(S_is)),
                                  spread_oos_1260=float(
                                      np.nanmax([S_oos[LAD_H_FINE.index(h)] for h in LAD_H_1260])
                                      - np.nanmin([S_oos[LAD_H_FINE.index(h)] for h in LAD_H_1260])),
                                  interp126_252_between=ia["between"], interp126_252_whole=ia["whole"],
                                  interp126_252_half1=ia["half1"], interp126_252_half2=ia["half2"],
                                  interp126_252_same_sign=ia["same_sign"],
                                  interp63_21_between=ib["between"], interp63_21_whole=ib["whole"],
                                  interp63_21_half1=ib["half1"], interp63_21_half2=ib["half2"],
                                  interp63_21_same_sign=ib["same_sign"],
                                  S_oos_by_H={h: round(float(S_oos[j]), 4) for j, h in enumerate(LAD_H_FINE)},
                                  S_is_by_H={h: round(float(S_is[j]), 4) for j, h in enumerate(LAD_H_FINE)}))
            say(f"\n   {pname} anchor {anc} (N={ANCHORS[anc]['N']} g={ANCHORS[anc]['GROSS']} "
                f"{ANCHORS[anc]['CADENCE']}, anchor rung H={ANCHORS[anc]['H']}):")
            say(f"      OOS Sharpe by H  " + "  ".join(f"{h}:{S_oos[j]:+.4f}" for j, h in enumerate(LAD_H_FINE)))
            say(f"      IS  Sharpe by H  " + "  ".join(f"{h}:{S_is[j]:+.4f}" for j, h in enumerate(LAD_H_FINE)))
            say(f"      full Sharpe by H " + "  ".join(f"{h}:{S_full[j]:+.4f}" for j, h in enumerate(LAD_H_FINE)))
            say(f"      turnover/yr      " + "  ".join(f"{h}:{tn_yr[j]:.2f}" for j, h in enumerate(LAD_H_FINE)))
            say(f"      monotone(OOS)={mono}  decisive steps {ndec}/6  argmax H={LAD_H_FINE[jmax]} "
                f"(interior={interior}, top gap {top_gap:+.4f} = "
                f"{top_gap/gap_se if gap_se>0 else float('nan'):.2f} paired SE)")
            say(f"      INTERPOLATION 126->189->252: whole {ia['whole']:+.4f} = "
                f"{ia['half1']:+.4f} then {ia['half2']:+.4f}; mid between = {ia['between']}, "
                f"both halves same sign = {ia['same_sign']}")
            say(f"      INTERPOLATION  63-> 42-> 21: whole {ib['whole']:+.4f} = "
                f"{ib['half1']:+.4f} then {ib['half2']:+.4f}; mid between = {ib['between']}, "
                f"both halves same sign = {ib['same_sign']}")

            # ---- G6: replay 1260's two headline steps on SMALL663
            if panel == "SMALL":
                if anc == "A":
                    v = float(S_oos[LAD_H_FINE.index(252)] - S_oos[LAD_H_FINE.index(126)])
                    gate("G6a REPLAY 1260 SMALL663 anchor A OOS step H 126->252",
                         f"{v:+.4f}", f"{C1260_STEP_A:+.4f} +- 5e-3", abs(v - C1260_STEP_A) < 5e-3)
                else:
                    v = float(S_oos[LAD_H_FINE.index(21)] - S_oos[LAD_H_FINE.index(63)])
                    gate("G6b REPLAY 1260 SMALL663 anchor B OOS step H  63-> 21",
                         f"{v:+.4f}", f"{C1260_STEP_B:+.4f} +- 5e-3", abs(v - C1260_STEP_B) < 5e-3)

            # ---- rule 8 on the FINE ladder and on 1260's committed SUB-ladder
            for ladname, rungs in (("H_FINE7", LAD_H_FINE), ("H_1260_4", LAD_H_1260)):
                jj = [LAD_H_FINE.index(h) for h in rungs]
                oo = S_oos[jj]
                ii = S_is[jj]
                rc = rankcorr(ii, oo)
                ai = rungs.index(ANCHORS[anc]["H"])
                for ch in CHOOSERS:
                    vals = np.array([stat_of(ch, Wl[j]) for j in jj])
                    jsel = int(np.nanargmax(vals))
                    pw = Wl[jj[jsel]]
                    b4, a4, o4 = legs_4b(pw, sw), legs_4a(pw, lw), legs_4b_oos(pw, sw)
                    aw = Wl[jj[ai]]
                    ab4 = legs_4b(aw, sw)
                    r8rows.append(dict(panel=pname, anchor=anc, ladder=ladname, chooser=ch,
                                       pick_H=rungs[jsel], anchor_H=ANCHORS[anc]["H"],
                                       reach_anchor=int(jsel == ai),
                                       pick_OOS_S=float(oo[jsel]), anchor_OOS_S=float(oo[ai]),
                                       delta_vs_anchor=float(oo[jsel] - oo[ai]),
                                       ladder_mean_OOS_S=float(np.nanmean(oo)),
                                       best_OOS_S=float(np.nanmax(oo)), worst_OOS_S=float(np.nanmin(oo)),
                                       regret_vs_best=float(np.nanmax(oo) - oo[jsel]),
                                       spy_OOS_S=sw["oos"]["Sharpe"],
                                       pick_OOS_CAGR=pw["oos"]["CAGR"], pick_OOS_DD=pw["oos"]["MaxDD"],
                                       anchor_OOS_CAGR=aw["oos"]["CAGR"], anchor_OOS_DD=aw["oos"]["MaxDD"],
                                       spy_OOS_CAGR=sw["oos"]["CAGR"], spy_OOS_DD=sw["oos"]["MaxDD"],
                                       rank_IS_OOS=rc,
                                       pick_keep4b=all(b4.values()), pick_fail4b=failed(b4),
                                       pick_keep4a=all(a4.values()), pick_fail4a=failed(a4),
                                       pick_keep4b_oos=all(o4.values()),
                                       anchor_keep4b=all(ab4.values())))
                    say(f"      rule8 [{ladname:9s}] {ch:11s} picks H={rungs[jsel]:3d} "
                        f"(anchor {ANCHORS[anc]['H']})  OOS S {oo[jsel]:.4f} vs anchor {oo[ai]:.4f}  "
                        f"delta {oo[jsel]-oo[ai]:+.4f}  SPY {sw['oos']['Sharpe']:.4f}  "
                        f"4b {'PASS' if all(b4.values()) else 'FAIL ' + failed(b4)}")
                say(f"      [{ladname}] IS/OOS Sharpe rank correlation over {len(rungs)} rungs: {rc:+.4f}")

        # ---------------- the SPREAD census: all four ladders, both anchors
        for anc in ANCHORS:
            lads = {"H_FINE7": LAD_H_FINE, "H_1260_4": LAD_H_1260, **CTRL_LADDERS}
            for ladname, rungs in lads.items():
                axis = "H" if ladname.startswith("H_") else ladname
                Wr = []
                for rg in rungs:
                    r, _ = rung_book(anc, axis, rg)
                    Wr.append(windows_of(r[WARMUP:], i_oos - WARMUP))
                s_is = np.array([w["is_"]["Sharpe"] for w in Wr])
                s_oos = np.array([w["oos"]["Sharpe"] for w in Wr])
                spread = float(np.nanmax(s_is) - np.nanmin(s_is))
                srt = np.sort(s_is)[::-1]
                margin = float(srt[0] - srt[1])
                anchor_rung = ANCHORS[anc][axis]
                ai = rungs.index(anchor_rung)
                anchor_is = float(s_is[ai])
                jsel = int(np.nanargmax(s_is))
                d = float(s_oos[jsel] - s_oos[ai])
                spreadrows.append(dict(panel=pname, anchor=anc, ladder=ladname, n_rungs=len(rungs),
                                       spread_IS=spread, margin_IS=margin,
                                       S_OBS_MARGIN=(margin / abs(anchor_is) if anchor_is else np.nan),
                                       S_OBS_RATIO=(margin / spread if spread > 0 else np.nan),
                                       anchor_IS_S=anchor_is, pick_rung=str(rungs[jsel]),
                                       anchor_rung=str(anchor_rung), reach=int(jsel == ai),
                                       pick_OOS_S=float(s_oos[jsel]), anchor_OOS_S=float(s_oos[ai]),
                                       realised_d=d, spread_OOS=float(np.nanmax(s_oos) - np.nanmin(s_oos))))
            sub = pd.DataFrame([r for r in spreadrows if r["panel"] == pname and r["anchor"] == anc])
            wid = sub.sort_values("spread_IS", ascending=False)
            say(f"\n   {pname} anchor {anc} SPREAD CENSUS (IS Sharpe spread, widest first):")
            for _, rw in wid.iterrows():
                say(f"      {rw.ladder:9s} n={int(rw.n_rungs):2d}  spread {rw.spread_IS:.4f}  "
                    f"margin {rw.margin_IS:.4f}  S_OBS_MARGIN {rw.S_OBS_MARGIN:.4f}  "
                    f"S_OBS_RATIO {rw.S_OBS_RATIO:.4f}  pick {rw.pick_rung:>5s} vs anchor "
                    f"{rw.anchor_rung:>5s}  realised d {rw.realised_d:+.4f}")
            ctrlrows.append(dict(panel=pname, anchor=anc,
                                 widest_ladder=str(wid.iloc[0].ladder),
                                 widest_spread=float(wid.iloc[0].spread_IS),
                                 H_fine_rank=int(1 + list(wid.ladder).index("H_FINE7")),
                                 H_1260_rank=int(1 + list(wid.ladder).index("H_1260_4"))))

        # ---- G7 turnover monotone in H
        for anc in ANCHORS:
            tn_yr = np.array([float(rung_book(anc, "H", H)[1][WARMUP:].sum() / yrs) for H in LAD_H_FINE])
            dd = np.diff(tn_yr)
            gate(f"G7 turnover non-increasing in H ({pname} anchor {anc})",
                 f"max positive step {float(dd.max()):+.4f}/yr", "<= 1e-9", bool(dd.max() <= 1e-9))

        if pi == 0:
            a = ANCHORS["A"]
            r_a, _ = book(a["N"], a["H"], a["GROSS"], a["CADENCE"])
            cache.clear()
            r_b, _ = book(a["N"], a["H"], a["GROSS"], a["CADENCE"])
            gate("G8 determinism (anchor book recomputes bit for bit)",
                 f"{float(np.abs(r_a - r_b).max()):.3e}", "== 0.0", float(np.abs(r_a - r_b).max()) == 0.0)

    g = pd.DataFrame(gridrows)
    sh = pd.DataFrame(shaperows)
    st = pd.DataFrame(steprows)
    sp = pd.DataFrame(spreadrows)
    r8 = pd.DataFrame(r8rows)
    ct = pd.DataFrame(ctrlrows)
    dump(g, "grid")
    dump(sh, "shape")
    dump(st, "steps")
    dump(sp, "spread")
    dump(r8, "walkforward")
    dump(ct, "widest")
    dump(pd.DataFrame(GATES), "gates")

    say("\n" + "=" * 100)
    say("## ANSWER")

    # ---- capital first (the only number that touches money)
    fine = r8[r8.ladder == "H_FINE7"]
    coarse = r8[r8.ladder == "H_1260_4"]
    say(f"   RULE 8, FINE 7-rung ladder: pick-minus-anchor OOS Sharpe mean {fine.delta_vs_anchor.mean():+.4f}, "
        f"positive at {int((fine.delta_vs_anchor > 0).sum())}/{len(fine)}, "
        f"reach (pick == anchor rung) {int(fine.reach_anchor.sum())}/{len(fine)}, "
        f"mean regret vs the ladder's best {fine.regret_vs_best.mean():+.4f}")
    say(f"   RULE 8, 1260's 4-rung ladder: mean {coarse.delta_vs_anchor.mean():+.4f}, "
        f"positive at {int((coarse.delta_vs_anchor > 0).sum())}/{len(coarse)}, "
        f"reach {int(coarse.reach_anchor.sum())}/{len(coarse)}, "
        f"mean regret {coarse.regret_vs_best.mean():+.4f}")
    say(f"   REFINING THE LADDER is worth {fine.delta_vs_anchor.mean() - coarse.delta_vs_anchor.mean():+.4f} "
        f"of mean OOS Sharpe against 1260's own rungs")
    sm = fine[fine.panel.str.startswith("SMALL")]
    say(f"   on SMALL663 alone (the panel 1260 fired on): mean delta {sm.delta_vs_anchor.mean():+.4f}, "
        f"positive at {int((sm.delta_vs_anchor > 0).sum())}/{len(sm)}")
    say(f"   4b PASS: pick {int(fine.pick_keep4b.sum())}/{len(fine)} vs anchor "
        f"{int(fine.anchor_keep4b.sum())}/{len(fine)}; 4a pick {int(fine.pick_keep4a.sum())}/{len(fine)}")

    # ---- shape
    say(f"\n   SHAPE: {len(sh)} (panel, anchor) families.  monotone in OOS Sharpe "
        f"{int(sh.monotone_oos.sum())}/{len(sh)}; interior OOS argmax {int(sh.argmax_interior.sum())}/{len(sh)}; "
        f"top gap decisive at {SE_MULT:.0f} SE {int(sh.top_decisive.sum())}/{len(sh)}")
    say(f"   STEPS: {len(st)} adjacent steps, decisive at {SE_MULT:.0f} SE {int(st.decisive.sum())}/{len(st)} "
        f"({st.decisive.mean():.4f}); median |step|/SE {float(st.step_over_SE.abs().median()):.4f}")
    say(f"   INTERPOLATION of 1260's two jumps across all {len(sh)} families: "
        f"126->189->252 mid between at {int(sh.interp126_252_between.sum())}/{len(sh)} "
        f"(both halves same sign {int(sh.interp126_252_same_sign.sum())}/{len(sh)}); "
        f"63->42->21 mid between at {int(sh.interp63_21_between.sum())}/{len(sh)} "
        f"(same sign {int(sh.interp63_21_same_sign.sum())}/{len(sh)})")
    for _, rw in sh.iterrows():
        say(f"      {rw.panel:9s} {rw.anchor}: monotone={rw.monotone_oos}  decisive {int(rw.n_decisive_steps)}/6  "
            f"OOS argmax H={int(rw.argmax_H_oos)}  IS argmax H={int(rw.argmax_H_is)}  "
            f"spread OOS {rw.spread_oos:.4f} (1260's 4 rungs {rw.spread_oos_1260:.4f})")

    # ---- spread vs score vs realised gain
    say(f"\n   SPREAD CENSUS: {len(sp)} (panel, anchor, ladder) cells.")
    say(f"      widest ladder by (panel, anchor): " +
        "; ".join(f"{r.panel}/{r.anchor} -> {r.widest_ladder} (H_FINE7 rank {r.H_fine_rank}, "
                  f"H_1260_4 rank {r.H_1260_rank})" for _, r in ct.iterrows()))
    ctrl_only = sp[sp.ladder != "H_1260_4"]      # one H ladder per cell, no double counting
    rho_sm = rankcorr(ctrl_only.spread_IS, ctrl_only.S_OBS_MARGIN)
    rho_sr = rankcorr(ctrl_only.spread_IS, ctrl_only.S_OBS_RATIO)
    rho_sd = rankcorr(ctrl_only.spread_IS, ctrl_only.realised_d)
    rho_md = rankcorr(ctrl_only.S_OBS_MARGIN, ctrl_only.realised_d)
    rho_rd = rankcorr(ctrl_only.S_OBS_RATIO, ctrl_only.realised_d)
    say(f"      rank corr(IS spread, S_OBS_MARGIN) {rho_sm:+.4f}   "
        f"rank corr(IS spread, S_OBS_RATIO) {rho_sr:+.4f}")
    say(f"      rank corr(IS spread, REALISED d) {rho_sd:+.4f}   "
        f"rank corr(S_OBS_MARGIN, REALISED d) {rho_md:+.4f}   "
        f"rank corr(S_OBS_RATIO, REALISED d) {rho_rd:+.4f}")
    say(f"      mean realised d by ladder: " +
        "; ".join(f"{k} {v:+.4f}" for k, v in ctrl_only.groupby('ladder').realised_d.mean().items()))
    say(f"      mean IS spread by ladder:  " +
        "; ".join(f"{k} {v:.4f}" for k, v in ctrl_only.groupby('ladder').spread_IS.mean().items()))

    # ---- verdict machinery, applied to the pre-declared outcomes
    smsh = sh[sh.panel.str.startswith("SMALL")]
    a_real = bool(smsh.monotone_oos.all()
                  and smsh.interp126_252_same_sign.all() and smsh.interp63_21_same_sign.all()
                  and sm.delta_vs_anchor.mean() > 0)
    lgsh = sh[~sh.panel.str.startswith("SMALL")]
    c_real_elsewhere = bool(lgsh.monotone_oos.all() and not smsh.monotone_oos.all())
    b_spread = bool((not smsh.monotone_oos.all())
                    and st.decisive.sum() <= 0.10 * len(st)
                    and abs(rho_sm) >= 0.5 and abs(rho_sd) < 0.5)
    d_neither = bool((not smsh.monotone_oos.all()) and abs(rho_sm) < 0.5)
    fired = ("A REAL HOLDING-PERIOD EFFECT" if a_real else
             "C REAL ELSEWHERE, NOT ON SMALL663" if c_real_elsewhere else
             "B SPREAD ARTEFACT" if b_spread else
             "D NEITHER" if d_neither else "NONE OF THE FOUR AS DECLARED — read the numbers above")
    say(f"\n   PRE-DECLARED OUTCOME FIRED: ({fired})")
    say(f"      A={a_real}  B={b_spread}  C={c_real_elsewhere}  D={d_neither}")
    say(f"   4b PASS at {int(g.keep4b.sum())}/{len(g)} grid cells (OOS-only 4b "
        f"{int(g.keep4b_oos.sum())}/{len(g)}); 4a PASS at {int(g.keep4a.sum())}/{len(g)}")
    if len(g):
        bl = pd.Series([x for r in g.fail4b for x in (r.split(",") if r != "-" else [])])
        say(f"      binding 4b leg counts: {bl.value_counts().to_dict()}")
    say(f"   gates: {sum(x['pass_'] for x in GATES)}/{len(GATES)} PASS "
        f"({', '.join(x['gate'].split()[0] for x in GATES if not x['pass_']) or 'none failed'})")
    say(f"   [t={time.time()-t0:.0f}s]")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

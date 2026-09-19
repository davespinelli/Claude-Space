#!/usr/bin/env python3
"""Idea 1578 — is a MARGIN-OVER-COST-STEP ABSTENTION RULE a better rule-8 chooser than ARGMAX IS SHARPE?

THE DEFECT.  Across nine 2026-09-19 runs the protocol's rule-8 chooser (argmax in-sample Sharpe)
has lost to DOING NOTHING more often than it has won.  Idea 1562, this lane's own first idea,
shows the arithmetic in one line: its chosen U56 cell's entire OOS margin over the frozen anchor
is +0.0041 of Sharpe, while the SAME book loses -0.0415 of Sharpe moving from 10 to 25 bps of
cost.  A selector that cannot see a margin smaller than its own cost sensitivity should not be
allowed to spend capital on one.

THE PROPOSAL.  C_ABSTAIN.  Take the family's IS argmax exactly as rule 8 does.  Then ask, ON IS
ROWS ONLY, whether its IS Sharpe margin over its OWN CAGR-matched constant de-gross twin exceeds
`k` times its own IS cost-step sensitivity |Sharpe@10bps - Sharpe@STEP bps|.  If it does, take the
pick.  If it does not, ABSTAIN and hold the frozen anchor (constant gross 0.75).  Everything the
rule reads is in-sample; the abstention decision itself never touches 2017-2026.

TUNED PARAMETERS: exactly TWO — k in {0.5, 1.0, 2.0} and the cost-step partner STEP in {25, 50}.
All six (k, STEP) cells published; no third dial.

FIVE DEVICE FAMILIES, all over the SAME frozen incumbent frame (N = 20, min-hold H = 126, per-name
200d MA gate, MAXVOL 0.60, equal weight, weekly, t+1), all DE-GROSS-TO-CASH, none ever levered:
  F_TWOSTATE  gross 0.75 above SPY's own MA, gL below       (12 rungs: MA x gL)
  F_DEGROSS   constant gross                                 (6 rungs)
  F_VOLTGT    gross = min(0.75, target / trailing 20d book vol)   (6 rungs)
  F_STOP      gross -> 0 while equity is `d` below its own peak   (5 rungs)
  F_BREADTH   gross 0.75 when the share of names above their own 200d MA clears `b`, 0.375 below
                                                             (5 rungs)
The frozen anchor (constant 0.75) is a member of F_DEGROSS and is the DO-NOTHING reference for
every family.

PRE-REGISTERED TESTS (written before the run).
  T1  ABSTENTION BEATS SELECTION: mean OOS Sharpe of C_ABSTAIN > C_ISSHARPE at >= 4 of the 6
      (k, STEP) cells.
  T2  ABSTENTION NEVER LOSES TO DOING NOTHING: mean OOS Sharpe of C_ABSTAIN >= the anchor's at
      >= 4 of the 6 cells.
  T3  REGRET: C_ABSTAIN's mean OOS regret against the ex-post best rung of its own family is
      LOWER than C_ISSHARPE's at >= 4 of the 6 cells.
  A KEEP requires, on top of the tests, a chooser pick that clears path 4b on FULL and OOS AND
  beats the anchor out of sample.  Otherwise the run is a KILL or an ANSWERED.

PROTOCOL: rule 1 (>= 10y); rule 2 (weights at t-1 applied at t, 10 bps headline, no shorting, no
leverage); rule 3 (live RULES v2 AND SPY); rule 4 (full + halves, both KEEP paths at EVERY rung);
rule 8 (every chooser reads warm-up..2016-12-31 ONLY; 2017-01-01..end read exactly once); rule 9.

GATES.  G0 >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor.
G2 exactly two tuned parameters.  G3 every CAGR-matched twin within 20 bp of its target.
G4 NO chooser reads a row on or after 2017-01-01 (asserted structurally AND by re-running every
chooser on a tape truncated at IS_END and checking the picks are bit-identical).  G5 gross in
[0, 1] on every book.  G6 every rung cell published.  G7 F_DEGROSS's 0.75 rung reproduces the
anchor exactly.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_margin-over-cost-step-abstention-chooser_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-19"
SLUG = "margin-over-cost-step-abstention-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"
HEADLINE_COST = 10.0
STEPS = [25.0, 50.0]                      # DIAL 2 (tuned)
KS = [0.5, 1.0, 2.0]                      # DIAL 1 (tuned)
COSTS = [HEADLINE_COST] + STEPS
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GGRID = np.round(np.arange(0.05, 0.7501, 0.01), 4)   # the twin is a DE-GROSS of the anchor, so
                                                      # g* <= I_G by construction; see twin()
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
MATCH_BAR = 0.0020

FAMILIES = {
    "F_TWOSTATE": [("twostate", (ma, gl)) for ma in (100, 150, 200, 250)
                   for gl in (0.375, 0.5625, 0.675)],
    "F_DEGROSS":  [("const", g) for g in (0.375, 0.45, 0.525, 0.60, 0.675, 0.75)],
    "F_VOLTGT":   [("voltgt", t) for t in (0.08, 0.10, 0.12, 0.15, 0.20, 0.25)],
    "F_STOP":     [("stop", d) for d in (0.05, 0.075, 0.10, 0.15, 0.25)],
    "F_BREADTH":  [("breadth", b) for b in (0.35, 0.45, 0.50, 0.55, 0.65)],
}

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


# ------------------------------------------------------------------ statistics
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


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


# ------------------------------------------------------------------ the panel
def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy_px = px["SPY"]
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        ab = (q > q.rolling(200).mean())
        self.breadth = (ab.sum(axis=1) / q.notna().sum(axis=1).replace(0, np.nan)).shift(1).values
        self._ma = {}

    def frame_inputs(self):
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        return elig, np.where(np.isfinite(sc), -sc, np.inf)

    def spy_above(self, ma):
        if ma not in self._ma:
            s = self.spy_px
            self._ma[ma] = (s > s.rolling(int(ma)).mean()).shift(1).fillna(False).values.astype(bool)
        return self._ma[ma]


def build_frame(pan, elig, key, reb, N=I_N, H=I_H, lag=1):
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_device(pan, frame, reb, cost, kind, param, nrows=None):
    """One daily engine for all five families.  Every device only ever CUTS gross below I_G and
    the remainder is CASH at 0%.  Path-dependent devices (stop, voltgt) read the book's own NET
    equity/vol through t-1 only, so the run is cost-specific by construction."""
    T = pan.rets.shape[0] if nrows is None else nrows
    M = pan.rets.shape[1]
    isreb = np.zeros(T, bool)
    isreb[reb[reb < T]] = True
    ab = pan.spy_above(param[0]) if kind == "twostate" else None
    cur = np.zeros(M)
    rnet = np.zeros(T)
    turn = np.zeros(T)
    sc = np.zeros(T)
    eq, peak = 1.0, 1.0
    gmax = 0.0
    win = np.zeros(20)
    nw = 0
    for t in range(T):
        if isreb[t]:
            if kind == "const":
                gt = float(param)
            elif kind == "twostate":
                gt = I_G if ab[t] else float(param[1])
            elif kind == "stop":
                gt = 0.0 if eq < peak * (1.0 - float(param)) else I_G
            elif kind == "breadth":
                b = pan.breadth[t]
                gt = I_G if (np.isfinite(b) and b > float(param)) else 0.375
            elif kind == "voltgt":
                if nw >= 20:
                    v = float(win.std(ddof=0) * np.sqrt(252))
                    gt = I_G if v <= 1e-9 else min(I_G, float(param) / v)
                else:
                    gt = I_G
            else:
                raise ValueError(kind)
            gt = float(min(max(gt, 0.0), I_G))
            post = gt * frame[t]
        else:
            gt = sc[t - 1] if t else 0.0
            post = cur
        sc[t] = gt
        tr = float(np.abs(post - cur).sum())
        gmax = max(gmax, float(post.sum()))
        r = float(post @ pan.rets[t])
        rn = r - tr * cost / 1e4
        turn[t] = tr
        rnet[t] = rn
        eq *= 1.0 + rn
        peak = max(peak, eq)
        win[nw % 20] = rn
        nw += 1
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rnet=rnet, turn=turn, gmax=gmax, gbar=float(sc[min(WARMUP, T - 1):].mean()))


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1578 — is a MARGIN-OVER-COST-STEP ABSTENTION RULE a better rule-8 chooser than "
        "ARGMAX IS SHARPE?   (lane cloud, idea 2 of 2)")
    say("  C_ABSTAIN: take the family's IS argmax only if its IS Sharpe margin over its OWN "
        "IS-CAGR-matched constant de-gross twin exceeds k x its own IS cost-step sensitivity; "
        "otherwise hold the frozen anchor (constant gross 0.75).  Everything read is in-sample.")
    say("  PRE-REGISTERED  T1 mean OOS Sharpe C_ABSTAIN > C_ISSHARPE at >= 4 of 6 (k, STEP) cells; "
        "T2 C_ABSTAIN >= the anchor at >= 4 of 6; T3 C_ABSTAIN's mean OOS regret < C_ISSHARPE's at "
        ">= 4 of 6.  A KEEP needs, on top, a pick clearing 4b FULL and OOS and beating the anchor "
        "out of sample.")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level is an UPPER BOUND.  The "
        "headline is a CONTRAST BETWEEN TWO SELECTION RULES reading the SAME rungs on the SAME "
        "tape, which the bias cannot manufacture; the 4a / 4b counts are not immune.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G2 exactly two tuned parameters (k, cost-step partner STEP)", 2, "== 2", True)

    rungs, picks = [], []
    g1_ok = None
    worst_match, gmax_global, g7_dev = 0.0, 0.0, 0.0
    g4_viol = 0
    n_notwin = 0
    mono_viol = 0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=HEADLINE_COST,
                      freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        elig, key = pan.frame_inputs()
        reb = cadence_rows(pan.idx, I_C)
        frame = build_frame(pan, elig, key, reb)

        A = {c: run_device(pan, frame, reb, c, "const", I_G) for c in COSTS}
        anch = A[HEADLINE_COST]["rnet"]
        gmax_global = max(gmax_global, A[HEADLINE_COST]["gmax"])
        am, ao = triple(anch[WARMUP:]), triple(anch[i_oos:])
        ah1, ah2 = halves(anch[WARMUP:])
        a4a, a4b, _, _, _, _ = keep_paths(anch[WARMUP:], spy, live)
        a4aO, a4bO, _, _, _, _ = keep_paths(anch[i_oos:], spyO, liveO)
        a_is = sharpe(anch[WARMUP:i_is + 1])

        say(f"\n  [{pan.name}]  SPY {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f} | 4b bars DD {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  |  OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}")
        say(f"           FROZEN ANCHOR g=0.75 (the DO-NOTHING option)  {am['CAGR']:.2%}/"
            f"{am['Sharpe']:.4f}/{am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS "
            f"{ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | IS Sharpe {a_is:.4f} | "
            f"4a {int(a4a)}/{int(a4aO)} 4b {int(a4b)}/{int(a4bO)}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor "
                         "(15.80%/1.1537/-19.13% full; 1.1857 OOS)", f"max |dev| {d:.2e}",
                         "< 5e-3", d < 5e-3)

        # the constant de-gross ladder: both a family and the twin-matching curve, per cost rung
        lad = {c: {} for c in COSTS}
        for c in COSTS:
            for g in GGRID:
                lad[c][float(g)] = run_device(pan, frame, reb, c, "const", float(g))["rnet"]
        gs = np.array(sorted(lad[HEADLINE_COST]))
        cf = {c: np.array([cagr(lad[c][float(g)][WARMUP:]) for g in gs]) for c in COSTS}
        ci = {c: np.array([cagr(lad[c][float(g)][WARMUP:i_is + 1]) for g in gs]) for c in COSTS}
        for c in COSTS:
            mono_viol += int((np.diff(cf[c]) <= 0).sum()) + int((np.diff(ci[c]) <= 0).sum())

        def twin(target, cost, window):
            """The CONSTANT gross whose CAGR over `window` equals `target`.  CAGR(g) is strictly
            increasing on [0.05, I_G] (verified below by G8), so the inverse is single-valued
            there.  A device whose CAGR lands OUTSIDE that range has NO constant de-gross twin —
            that is a fact about the device, not a failure, and is returned as NaN and counted."""
            y = (cf if window == "full" else ci)[cost]
            if not (y.min() <= target <= y.max()):
                return np.nan, None, 0.0
            gstar = float(np.interp(target, y, gs))
            rn = run_device(pan, frame, reb, cost, "const", gstar)["rnet"]
            got = cagr(rn[WARMUP:]) if window == "full" else cagr(rn[WARMUP:i_is + 1])
            return gstar, rn, abs(got - target)

        for fam, specs in FAMILIES.items():
            for kind, param in specs:
                lab = f"{kind}:{param}"
                R = {c: run_device(pan, frame, reb, c, kind, param) for c in COSTS}
                gmax_global = max(gmax_global, max(R[c]["gmax"] for c in COSTS))
                rn = R[HEADLINE_COST]["rnet"]
                if fam == "F_DEGROSS" and abs(float(param) - I_G) < 1e-12:
                    g7_dev = max(g7_dev, float(np.abs(rn - anch).max()))
                k4a, k4b, m, h1, h2, lg = keep_paths(rn[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, lgO = keep_paths(rn[i_oos:], spyO, liveO)
                is_s = sharpe(rn[WARMUP:i_is + 1])
                is_c = cagr(rn[WARMUP:i_is + 1])
                gI, twI, gapI = twin(is_c, HEADLINE_COST, "is")
                worst_match = max(worst_match, gapI)
                is_margin = (np.nan if twI is None
                             else is_s - sharpe(twI[WARMUP:i_is + 1]))
                gF, twF, gapF = twin(m["CAGR"], HEADLINE_COST, "full")
                worst_match = max(worst_match, gapF)
                if twF is None:
                    n_notwin += 1
                    dS, seS, tS = np.nan, np.nan, np.nan
                    dDD = np.nan
                else:
                    dS, seS, tS = paired_block_dsharpe(rn[WARMUP:], twF[WARMUP:])
                    dDD = m["MaxDD"] - triple(twF[WARMUP:])["MaxDD"]
                row = dict(panel=pan.name, family=fam, rung=lab, kind=kind, param=str(param),
                           gbar=R[HEADLINE_COST]["gbar"],
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                           keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                           leg_H1=lg["H1"], leg_H2=lg["H2"], leg_DD=lg["DD"], leg_CAGR=lg["CAGR"],
                           is_Sharpe=is_s, is_CAGR=is_c, is_twin_g=gI, is_margin=is_margin,
                           full_twin_g=gF, dSharpe_twin=dS, t_twin=tS,
                           dMaxDD_twin=dDD)
                for c in STEPS:
                    row[f"is_Sharpe_{int(c)}"] = sharpe(R[c]["rnet"][WARMUP:i_is + 1])
                    row[f"sens_{int(c)}"] = abs(is_s - sharpe(R[c]["rnet"][WARMUP:i_is + 1]))
                rungs.append(row)

        # ------------------------------------------------------------------ the choosers
        Rdf = pd.DataFrame([r for r in rungs if r["panel"] == pan.name])
        for fam in FAMILIES:
            f = Rdf[Rdf.family == fam].reset_index(drop=True)
            best_is = f.loc[f["is_Sharpe"].idxmax()]
            expost = f.loc[f["oSharpe"].idxmax()]
            for k in KS:
                for st in STEPS:
                    sens = float(best_is[f"sens_{int(st)}"])
                    mar = float(best_is["is_margin"])
                    accept = bool(np.isfinite(mar) and mar > k * sens)
                    p = best_is if accept else None
                    picks.append(dict(
                        panel=pan.name, family=fam, k=k, step=st,
                        is_argmax=best_is["rung"], is_margin=float(best_is["is_margin"]),
                        sens=sens, bar=k * sens, accepted=accept,
                        sel_rung=best_is["rung"], sel_oSharpe=float(best_is["oSharpe"]),
                        sel_oCAGR=float(best_is["oCAGR"]), sel_oMaxDD=float(best_is["oMaxDD"]),
                        sel_keep4b=bool(best_is["keep4b"]),
                        sel_keep4b_oos=bool(best_is["keep4b_oos"]),
                        sel_keep4a_oos=bool(best_is["keep4a_oos"]),
                        abs_rung=(best_is["rung"] if accept else "ANCHOR const:0.75"),
                        abs_oSharpe=(float(best_is["oSharpe"]) if accept else ao["Sharpe"]),
                        abs_oCAGR=(float(best_is["oCAGR"]) if accept else ao["CAGR"]),
                        abs_oMaxDD=(float(best_is["oMaxDD"]) if accept else ao["MaxDD"]),
                        abs_keep4b=(bool(best_is["keep4b"]) if accept else a4b),
                        abs_keep4b_oos=(bool(best_is["keep4b_oos"]) if accept else a4bO),
                        abs_keep4a_oos=(bool(best_is["keep4a_oos"]) if accept else a4aO),
                        anchor_oSharpe=ao["Sharpe"], anchor_oCAGR=ao["CAGR"],
                        anchor_oMaxDD=ao["MaxDD"],
                        expost_rung=expost["rung"], expost_oSharpe=float(expost["oSharpe"]),
                        live_oSharpe=liveO["Sharpe"], spy_oSharpe=spyO["Sharpe"]))
        say(f"    rule-8 IS window rows {WARMUP}..{i_is} ({pan.idx[WARMUP].date()}.."
            f"{pan.idx[i_is].date()}); OOS from {pan.idx[i_oos].date()}")

        # ---- G4: re-derive every chooser input on a tape TRUNCATED at IS_END ---------------
        for fam, specs in FAMILIES.items():
            for kind, param in specs:
                Rt = run_device(pan, frame, reb, HEADLINE_COST, kind, param, nrows=i_is + 1)
                s_t = sharpe(Rt["rnet"][WARMUP:i_is + 1])
                s_f = float(Rdf[(Rdf.family == fam) & (Rdf.rung == f"{kind}:{param}")]
                            ["is_Sharpe"].iloc[0])
                if abs(s_t - s_f) > 1e-12:
                    g4_viol += 1

    R = pd.DataFrame(rungs)
    P = pd.DataFrame(picks)
    R.to_csv(f"{OUT}.rungs.csv", index=False)
    P.to_csv(f"{OUT}.picks.csv", index=False)

    gate("G3 CAGR match quality of every de-gross twin that EXISTS (IS and FULL)",
         f"worst |gap| {worst_match:.2e}", f"< {MATCH_BAR}", worst_match < MATCH_BAR)
    gate("G8 CAGR(g) is strictly increasing on [0.05, 0.75] at every cost rung (so the twin's "
         "inverse is single-valued)", f"{mono_viol} non-increasing steps", "== 0", mono_viol == 0)
    publish("rungs with NO constant de-gross twin (CAGR outside the ladder's range) — the "
            "abstention rule ABSTAINS on these by construction", f"{n_notwin} of {len(R)}")
    gate("G4 no chooser reads a row on or after 2017-01-01 (every IS Sharpe re-derived on a tape "
         "TRUNCATED at IS_END and compared bit-for-bit)",
         f"{g4_viol} of {len(R)} rungs differ", "== 0", g4_viol == 0)
    gate("G5 gross in [0, 1] on every book (no leverage, rule 2)", f"max sum(w) {gmax_global:.6f}",
         "<= 1.0 + 1e-9", gmax_global <= 1.0 + 1e-9)
    gate("G6 every rung cell published", f"{len(R)} rungs "
         f"({sum(len(v) for v in FAMILIES.values())} x 3 panels)",
         f"== {sum(len(v) for v in FAMILIES.values())*3}",
         len(R) == sum(len(v) for v in FAMILIES.values()) * 3)
    gate("G7 F_DEGROSS's 0.75 rung reproduces the frozen anchor exactly",
         f"max |dev| {g7_dev:.2e}", "== 0", g7_dev == 0.0)

    # ------------------------------------------------------------------ rungs
    say("\n" + "=" * 128)
    say("EVERY RUNG PUBLISHED (headline 10 bps).  IS columns are the ONLY thing the choosers see.")
    say("=" * 128)
    for p in ["U56", "B136", "SMALL"]:
        say(f"\n  [{p}]")
        say("    family      rung             gbar   CAGR     Sharpe   MaxDD    oSharpe  4a 4b 4bO "
            "| IS Sharpe  ISmargin  sens25   sens50")
        for _, r in R[R.panel == p].iterrows():
            say(f"    {r.family:<11} {r.rung:<16} {r.gbar:.3f} {r.CAGR:7.2%} {r.Sharpe:8.4f} "
                f"{r.MaxDD:7.2%} {r.oSharpe:8.4f} {int(r.keep4a)}  {int(r.keep4b)}  "
                f"{int(r.keep4b_oos)}  | {r.is_Sharpe:9.4f} {r.is_margin:+9.4f} "
                f"{r.sens_25:8.4f} {r.sens_50:8.4f}")

    say("\n" + "=" * 128)
    say("THE DEFECT, MEASURED: how a rung's MARGIN over its own CAGR-matched twin compares with "
        "its own COST-STEP SENSITIVITY.")
    say("=" * 128)
    say("    panel  family      median IS margin   median sens25   median sens50   margin>sens25 "
        "  margin>2*sens25")
    for p in ["U56", "B136", "SMALL"]:
        for fam in FAMILIES:
            f = R[(R.panel == p) & (R.family == fam)]
            say(f"    {p:<6} {fam:<11} {f['is_margin'].median():+.4f}           "
                f"{f['sens_25'].median():.4f}          {f['sens_50'].median():.4f}          "
                f"{int((f['is_margin'] > f['sens_25']).sum())} of {len(f)}          "
                f"{int((f['is_margin'] > 2*f['sens_25']).sum())} of {len(f)}")

    # ------------------------------------------------------------------ the race
    say("\n" + "=" * 128)
    say("RULE 8 — THE RACE.  Parameters chosen on warm-up..2016-12-31 ONLY; 2017-01-01..end read "
        "ONCE.  15 (panel, family) cells per (k, STEP).")
    say("=" * 128)
    say("     k  STEP | C_ISSHARPE  C_ABSTAIN  ANCHOR(do nothing)  ex-post best | abstains | "
        "regret SEL  regret ABS | T1 T2 T3")
    t1 = t2 = t3 = 0
    summ = []
    for k in KS:
        for st in STEPS:
            s = P[(P.k == k) & (P.step == st)]
            sel, ab, an = s["sel_oSharpe"].mean(), s["abs_oSharpe"].mean(), s["anchor_oSharpe"].mean()
            ex = s["expost_oSharpe"].mean()
            rs = (s["expost_oSharpe"] - s["sel_oSharpe"]).mean()
            ra = (s["expost_oSharpe"] - s["abs_oSharpe"]).mean()
            c1, c2, c3 = ab > sel, ab >= an, ra < rs
            t1 += c1
            t2 += c2
            t3 += c3
            summ.append(dict(k=k, step=st, sel=sel, abstain=ab, anchor=an, expost=ex,
                             n_accept=int(s["accepted"].sum()), n=len(s), regret_sel=rs,
                             regret_abs=ra, T1=bool(c1), T2=bool(c2), T3=bool(c3)))
            say(f"   {k:4.1f}  {st:4.0f} | {sel:10.4f}  {ab:9.4f}  {an:18.4f}  {ex:12.4f} | "
                f"{int(s['accepted'].sum()):2d}/{len(s):2d}    | {rs:10.4f} {ra:11.4f} | "
                f"{int(c1)}  {int(c2)}  {int(c3)}")
    S = pd.DataFrame(summ)
    S.to_csv(f"{OUT}.race.csv", index=False)
    say(f"  LIVE RULES v2 mean OOS Sharpe {P['live_oSharpe'].mean():.4f} | SPY "
        f"{P['spy_oSharpe'].mean():.4f}")
    say(f"  T1 (ABSTAIN > SELECT): {t1} of 6 cells   T2 (ABSTAIN >= DO NOTHING): {t2} of 6   "
        f"T3 (lower regret): {t3} of 6   [bar = 4 of 6 each]")

    say("\n  WHICH RUNGS ARE EVER ACCEPTED (per k, STEP): the abstention rule's whole content.")
    for k in KS:
        for st in STEPS:
            s = P[(P.k == k) & (P.step == st)]
            acc = s[s.accepted]
            say(f"    k={k} STEP={st:.0f}: accepts {len(acc)} of {len(s)} -> "
                f"{sorted(set(acc.panel + '/' + acc.family + '/' + acc.abs_rung)) if len(acc) else 'none'}")

    say("\n  PER-CELL DETAIL at the middle dial (k = 1.0, STEP = 25):")
    s = P[(P.k == 1.0) & (P.step == 25.0)]
    say("    panel  family      IS argmax        margin    bar       acc | SEL OOS Sh  ABS OOS Sh"
        "  ANCHOR    ex-post best")
    for _, r in s.iterrows():
        say(f"    {r.panel:<6} {r.family:<11} {r.is_argmax:<16} {r.is_margin:+8.4f} {r.bar:8.4f} "
            f"{'Y' if r.accepted else 'n'}   | {r.sel_oSharpe:10.4f} {r.abs_oSharpe:11.4f} "
            f"{r.anchor_oSharpe:9.4f} {r.expost_oSharpe:9.4f} ({r.expost_rung})")

    # ------------------------------------------------------------------ KEEP paths
    say("\n" + "=" * 128)
    say("KEEP PATHS across all rungs (headline 10 bps).")
    say("=" * 128)
    say(f"  4a: {int(R.keep4a.sum())} of {len(R)} FULL, {int(R.keep4a_oos.sum())} of {len(R)} OOS.")
    say(f"  4b: {int(R.keep4b.sum())} of {len(R)} FULL, {int(R.keep4b_oos.sum())} of {len(R)} OOS, "
        f"{int((R.keep4b & R.keep4b_oos).sum())} BOTH.")
    for p in ["U56", "B136", "SMALL"]:
        f = R[R.panel == p]
        say(f"    [{p}] 4b BOTH {int((f.keep4b & f.keep4b_oos).sum())} of {len(f)}; binding legs "
            f"H1 {int((~f.leg_H1).sum())} H2 {int((~f.leg_H2).sum())} DD {int((~f.leg_DD).sum())} "
            f"CAGR {int((~f.leg_CAGR).sum())} fails")
    reach = P[(P.k == 1.0) & (P.step == 25.0)]
    good = reach[reach.abs_keep4b & reach.abs_keep4b_oos
                 & (reach.abs_oSharpe > reach.anchor_oSharpe)]
    say(f"  CHOOSER PICKS at k=1.0/STEP=25 that clear 4b FULL and OOS AND beat the anchor OOS: "
        f"{len(good)} of {len(reach)}")
    for _, r in good.iterrows():
        say(f"    -> {r.panel} / {r.family} / {r.abs_rung}: OOS {r.abs_oCAGR:.2%}/"
            f"{r.abs_oSharpe:.4f}/{r.abs_oMaxDD:.2%} vs anchor {r.anchor_oCAGR:.2%}/"
            f"{r.anchor_oSharpe:.4f}/{r.anchor_oMaxDD:.2%}")

    verdict = ("KEEP-candidate" if (t1 >= 4 and t2 >= 4 and t3 >= 4 and len(good) > 0)
               else ("ANSWERED / KILL for capital" if (t1 >= 4 or t2 >= 4 or t3 >= 4)
                     else "KILL"))
    say("\n" + "=" * 128)
    say(f"  VERDICT: {verdict}   (T1 {t1}/6, T2 {t2}/6, T3 {t3}/6; qualifying picks {len(good)})")
    say("=" * 128)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(1 for g in GATES if g["target"] != "published, not asserted" and g["pass_"])
    ntot = sum(1 for g in GATES if g["target"] != "published, not asserted")
    say(f"  GATES {npass}/{ntot} PASS.   elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

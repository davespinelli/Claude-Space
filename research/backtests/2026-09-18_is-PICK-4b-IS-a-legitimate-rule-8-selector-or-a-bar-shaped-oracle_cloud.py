#!/usr/bin/env python3
"""
Idea 712 (lane cloud, 2026-09-18) — is PICK-4b-IS a LEGITIMATE rule-8 selector, or a BAR-SHAPED
ORACLE that manufactures its edge out of the shape of PROTOCOL 4b itself?

THE PREMISE.  Idea 702's only selector to reach a 4b row picks among the cells that ALREADY clear
4b on the in-sample window — it uses the bar's own shape as its objective — and its zero-signal
twin reached the 4b recommendation 3 of 6 times.  Every KEEP-4b in this record was found by some
in-sample chooser, so whether that family of chooser reads SIGNAL or reads the BAR decides what a
committed 4b pass is worth.  A selector that does as well on a corpus with NO signal in it is not
a selector.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE CORPUS (the comparison set, FROZEN, not a dial).  N {5,10,15,20,25,30} x GROSS
      {0.45,0.55,0.65,0.75,0.85} = 30 real books per panel, 90 in all, EVERY ONE PUBLISHED with
      both KEEP paths (rule 4).  Construction otherwise frozen at the certified book: H = 126-row
      min hold, weekly decision on the last trading row of the week (Fri) applied at t+1,
      3-leg composite (21/252, 0/126, 0/63) equal-ranked, above-200d and vol20 < 0.60, equal
      weights, cash at 0%, 10 bps (PROTOCOL rule 2), 260-row warm-up.
  (2) THE ANCHOR.  (U56, N=20, g=0.65) must reproduce the certified candidate 13.66% / 1.1526 /
      -16.73%, OOS 14.95% / 1.1833 (idea 1290).  A CHECK, not a result.
  (3) THE SELECTORS (dial 1), ALL read on the IS window (warm-up .. 2016-12-31) ONLY:
        PICK-4b-IS  pick among cells clearing the IS 4b ANALOGUE declared in (4); tie-break
                    highest IS Sharpe, then LOWER gross, then LOWER N.  If NO cell clears, fall
                    back to argmax IS Sharpe (declared fallback, not chosen on a result).
        PICK-SHARPE argmax IS Sharpe.
        PICK-CALMAR argmax IS CAGR / |IS MaxDD|.
        PICK-J      argmax IS min(DD-cap margin, CAGR-floor margin) — idea 1290's chooser.
        ANCHOR      the frozen certified cell (N=20, g=0.65); chooses nothing.
        CORPUS-MEAN the mean over all 30 cells = what a uniform draw from the corpus gets, i.e.
                    DOING NOTHING.  Every edge below is measured against THIS.
  (4) THE IS 4b ANALOGUE, declared exactly.  On the IS window, with IS1/IS2 its two halves:
      Sharpe(IS1) > SPY(IS1); Sharpe(IS2) > SPY(IS2); Sharpe(IS) > SPY(IS) [stands in for 4b's
      OOS-Sharpe leg, which does not exist in sample — declared, not chosen]; MaxDD(IS) >=
      0.60*MaxDD_SPY(IS); CAGR(IS) >= 0.70*CAGR_SPY(IS).
  (5) THE MATCHED ZERO-SIGNAL CONTROL (dial 2 = the control seed, 30 seeds).  For each seed the
      WHOLE corpus is rebuilt with the composite rank replaced by a uniform random key redrawn at
      every decision row.  N, gross, H, cadence, the above-200d / vol20 eligibility mask, costs
      and dates are IDENTICAL; only the ordering information is destroyed.  Turnover is reported
      for both so the match can be checked rather than asserted.
  (6) THE STATISTIC.  EDGE(selector) := OOS Sharpe of the selected cell - OOS Sharpe of the
      CORPUS MEAN, on the same panel and dates.  EDGE_real on the real corpus; EDGE_ctrl on each
      of the 30 control corpora.  A selector that reads signal has EDGE_real >> EDGE_ctrl.  Also
      reported: 4b-REC, the share of corpora where the selector's pick clears FULL-sample 4b.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) LEGITIMATE — PICK-4b-IS's EDGE_real exceeds its own control mean by more than 2 control
        SD on a MAJORITY of panels, and its control edge is not itself materially positive.
    (B) BAR-SHAPED ORACLE — its control EDGE is materially positive and of comparable size to
        EDGE_real, i.e. a corpus with no signal in it reproduces the selector's edge.
    (C) NO EDGE EITHER WAY — EDGE_real <= 0 on a majority of panels; the selector does not beat
        doing nothing, on real data or on the control.
  A KEEP-4b candidate is claimed only if some selector's rule-8 pick clears 4b on the full sample
  AND beats SPY's OOS Sharpe AND is not reproduced by the control; otherwise KILL or PARK.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4): SELECTOR (6 values) x CONTROL SEED (30).  N, gross
and panel are the CORPUS, published in full, not tuned: no number below is read off a choice among
them made after the fact.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
current constituent list of a sub-$2B screen, with tickers whose max_1d_move >= 1.0 in
data/small_meta.csv dropped before anything is built.  Delisted, acquired and bankrupt names are
absent from all three, which flatters every momentum book here and the drawdown leg specifically.
It also flatters the CONTROL, which draws from the same surviving names — so the control is a
conservative comparand for the selector, not a lenient one.

PROTOCOL: rule 2 execution and 10 bps costs; rule 4 both KEEP paths at every corpus cell; rule 8
walk-forward with 2017-2026 read ONCE; rule 9 survivorship stated.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_is-PICK-4b-IS-a-legitimate-rule-8-selector-or-a-bar-shaped-oracle_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest  # noqa: E402

OUT = Path(str(Path(__file__))[:-3])
WARMUP, MAXVOL, COST = 260, 0.60, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
A_H, A_PHASE, A_DELAY = 126, 4, 1
NS = [5, 10, 15, 20, 25, 30]
GROSSES = [0.45, 0.55, 0.65, 0.75, 0.85]
ANCHOR_N, ANCHOR_G = 20, 0.65
NSEED = 30
OOS_START = pd.Timestamp("2017-01-01")
SELECTORS = ["PICK-4b-IS", "PICK-SHARPE", "PICK-CALMAR", "PICK-J", "ANCHOR", "CORPUS-MEAN"]
PANEL_OFFSET = {"U56": 0, "B136": 1, "SMALL": 2}   # deterministic seeding (rule 5)

_LOG: list[str] = []


def say(s=""):
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------ mechanics
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def decision_rows(idx, w):
    pos = np.arange(len(idx))
    ok = idx.weekday <= w
    s = pd.Series(pos[ok], index=idx.to_period("W")[ok])
    return np.sort(s.groupby(level=0).max().values)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        self.dec = decision_rows(px.index, A_PHASE)


def build(pan, N, rng=None):
    """Min-hold top-N frame at UNIT gross.  rng=None -> the real composite rank.  rng given ->
    the MATCHED ZERO-SIGNAL control: a uniform random key redrawn at every decision row, same
    eligibility mask, same N, same H, same cadence."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = pan.dec + A_DELAY
    keep = app < T
    dec, app = pan.dec[keep], app[keep]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        ks = set(int(c) for c in young)
        need = N - len(ks)
        take = []
        if need > 0:
            k = (rng.random(K) if rng is not None else pan.rank_key[ts].copy())
            k = np.asarray(k, dtype=float)
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]):
                    break
                take.append(int(c))
        new = np.full(K, -1, dtype=np.int64)
        for c in ks:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = app[i + 1] if i + 1 < len(app) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, app


def nrun(pan, Wt, app):
    rets, Cp = pan.rets, pan.Cp
    T, M = rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    app = np.asarray(app, dtype=np.int64)
    ends = np.append(app[1:], T)
    for i0, i1 in zip(app, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        curw = held[i1 - 1]
    return (held * rets).sum(axis=1), turn


# ------------------------------------------------------------------ metrics
def mt(r):
    r = np.asarray(r, dtype=float)
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1.0),
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd)


def windows(idx):
    n = len(idx)
    h = n // 2
    h1 = np.zeros(n, bool); h1[:h] = True
    h2 = np.zeros(n, bool); h2[h:] = True
    oos = np.asarray(idx >= OOS_START)
    is_ = ~oos
    ii = np.flatnonzero(is_)
    half = ii[len(ii) // 2]
    is1 = is_.copy(); is1[half:] = False
    is2 = is_.copy(); is2[:half] = False
    return dict(FULL=np.ones(n, bool), H1=h1, H2=h2, IS=is_, OOS=oos, IS1=is1, IS2=is2)


def cell_stats(r, spy, live, W):
    """Everything a selector may look at (IS only) and everything the verdict needs (FULL/OOS)."""
    R, S, L = mt(r), mt(spy), mt(live)
    o = {}
    for wn in ("FULL", "H1", "H2", "IS", "OOS", "IS1", "IS2"):
        m = W[wn]
        a, b = mt(r[m]), mt(spy[m])
        o[f"CAGR_{wn}"], o[f"Sharpe_{wn}"], o[f"MaxDD_{wn}"] = a["CAGR"], a["Sharpe"], a["MaxDD"]
        o[f"spySharpe_{wn}"] = b["Sharpe"]
    r1, r2 = mt(r[W["H1"]]), mt(r[W["H2"]])
    s1, s2 = mt(spy[W["H1"]]), mt(spy[W["H2"]])
    l1, l2 = mt(live[W["H1"]]), mt(live[W["H2"]])
    Ro, So = mt(r[W["OOS"]]), mt(spy[W["OOS"]])
    o["pass4a"] = bool(r1["Sharpe"] > l1["Sharpe"] and r2["Sharpe"] > l2["Sharpe"]
                       and R["MaxDD"] >= L["MaxDD"])
    o["pass4b"] = bool(r1["Sharpe"] > s1["Sharpe"] and r2["Sharpe"] > s2["Sharpe"]
                       and Ro["Sharpe"] > So["Sharpe"] and R["MaxDD"] >= 0.60 * S["MaxDD"]
                       and R["CAGR"] >= 0.70 * S["CAGR"])
    # IS-only quantities the selectors are allowed to read
    Sis, S1, S2 = mt(spy[W["IS"]]), mt(spy[W["IS1"]]), mt(spy[W["IS2"]])
    Ris, R1, R2 = mt(r[W["IS"]]), mt(r[W["IS1"]]), mt(r[W["IS2"]])
    o["is4b"] = bool(R1["Sharpe"] > S1["Sharpe"] and R2["Sharpe"] > S2["Sharpe"]
                     and Ris["Sharpe"] > Sis["Sharpe"]
                     and Ris["MaxDD"] >= 0.60 * Sis["MaxDD"]
                     and Ris["CAGR"] >= 0.70 * Sis["CAGR"])
    o["is_calmar"] = Ris["CAGR"] / abs(Ris["MaxDD"]) if Ris["MaxDD"] < 0 else np.nan
    o["is_J"] = min(100.0 * (Ris["MaxDD"] - 0.60 * Sis["MaxDD"]),
                    100.0 * (Ris["CAGR"] - 0.70 * Sis["CAGR"]))
    return o


def choose(df, sel):
    """Return the chosen row index (or None for CORPUS-MEAN).  IS-only information."""
    if sel == "CORPUS-MEAN":
        return None
    if sel == "ANCHOR":
        m = df[(df.N == ANCHOR_N) & (df.gross == ANCHOR_G)]
        return int(m.index[0]) if len(m) else None
    if sel == "PICK-4b-IS":
        ok = df[df.is4b]
        if len(ok) == 0:                       # declared fallback
            return int(df["Sharpe_IS"].idxmax())
        ok = ok.sort_values(["Sharpe_IS", "gross", "N"], ascending=[False, True, True])
        return int(ok.index[0])
    key = dict({"PICK-SHARPE": "Sharpe_IS", "PICK-CALMAR": "is_calmar", "PICK-J": "is_J"})[sel]
    return int(df[key].idxmax())


def make_panels():
    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxS.columns if c != "SPY" and c in bad])
    return ([Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
             Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
             Panel("SMALL", pxS, inv)], n_drop)


def corpus(pan, spy, live, W, rng=None):
    rows = []
    for N in NS:
        W1, app = build(pan, N, rng=rng)
        for g in GROSSES:
            gr, tu = nrun(pan, W1 * g, app)
            r = (gr - tu * COST / 1e4)[WARMUP:]
            o = cell_stats(r, spy, live, W)
            o.update(N=N, gross=g,
                     turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
            rows.append(o)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 712 (lane cloud, 2026-09-18) — is PICK-4b-IS a LEGITIMATE rule-8 selector, or a")
    say("BAR-SHAPED ORACLE that manufactures its edge out of the shape of PROTOCOL 4b itself?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): SELECTOR {SELECTORS} x CONTROL SEED (0..{NSEED - 1}).")
    say(f"  CORPUS (frozen, published in full): N {NS} x GROSS {GROSSES} = "
        f"{len(NS) * len(GROSSES)} cells per panel, {len(NS) * len(GROSSES) * 3} in all.")
    say(f"  FROZEN: H={A_H}, weekly (Fri decision), t+1, {COST:.0f} bps, above-200d & vol20<0.60,")
    say("          equal weights, 260-row warm-up, cash at 0%.  IS = warm-up..2016; OOS read ONCE.")
    say("  EDGE := OOS Sharpe(pick) - OOS Sharpe(CORPUS MEAN).  Control = same corpus with the")
    say("  composite rank replaced by a uniform random key redrawn every decision row.")
    say("  OUTCOMES: (A) LEGITIMATE  (B) BAR-SHAPED ORACLE  (C) NO EDGE EITHER WAY.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY = benchmark only.")
    say("")

    # ---------------------------------------------------------- benchmarks + real corpus
    B, REAL = {}, {}
    say("=" * 100)
    say("ARM A — BENCHMARKS (post-warm-up, 10 bps)")
    say("=" * 100)
    say("")
    say(f"  {'panel':6} {'series':22} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'IS Sh':>8} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8}")
    for pan in panels:
        spy = pan.spy[WARMUP:]
        live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                        freq="W")["returns"].values[WARMUP:]
        idx = pan.idx[WARMUP:]
        W = windows(idx)
        B[pan.name] = dict(spy=spy, live=live, idx=idx, W=W)
        for tag, s in (("SPY (buy & hold)", spy), ("RULES v2 (live book)", live)):
            m, mo = mt(s), mt(s[W["OOS"]])
            say(f"  {pan.name:6} {tag:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(s[W['IS']])['Sharpe']:8.4f} {mo['CAGR']:9.2%} {mo['Sharpe']:8.4f} "
                f"{mo['MaxDD']:8.2%}")
    say("")
    for pan in panels:
        REAL[pan.name] = corpus(pan, B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["W"])
        REAL[pan.name]["panel"] = pan.name

    # ---------------------------------------------------------- anchor
    say("=" * 100)
    say("ARM B — THE ANCHOR CHECK: (U56, N=20, g=0.65, 10 bps, Fri, t+1) against the certified")
    say("candidate 13.66% / 1.1526 / -16.73%, OOS 14.95% / 1.1833 (idea 1290)")
    say("=" * 100)
    say("")
    a = REAL["U56"]
    a = a[(a.N == ANCHOR_N) & (a.gross == ANCHOR_G)].iloc[0]
    tgt = [("CAGR", a.CAGR_FULL, 0.1366), ("Sharpe", a.Sharpe_FULL, 1.1526),
           ("MaxDD", a.MaxDD_FULL, -0.1673), ("OOS_CAGR", a.CAGR_OOS, 0.1495),
           ("OOS_Sharpe", a.Sharpe_OOS, 1.1833)]
    say(f"  {'stat':10} {'this run':>12} {'committed':>12} {'diff':>12}")
    ok = True
    for k, v, w in tgt:
        say(f"  {k:10} {v:12.4f} {w:12.4f} {v - w:12.2e}")
        ok &= abs(v - w) < 5e-4
    say("")
    say(f"  ANCHOR REPRODUCES: {'YES' if ok else 'NO'} (all five within 5e-4).")
    if not ok:
        say("  *** The anchor does NOT reproduce; no verdict below may be taken on these numbers.")
    say("")

    # ---------------------------------------------------------- the corpus
    say("=" * 100)
    say("ARM C — THE REAL CORPUS, all 90 cells, both KEEP paths (rule 4)")
    say("=" * 100)
    say("")
    for pan in panels:
        df = REAL[pan.name]
        say(f"  --- {pan.name} " + "-" * 82)
        say(f"  {'N':>3} {'gross':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'turn/yr':>8} "
            f"{'IS Sh':>8} {'is4b':>5} {'is_J':>7} {'OOS CAGR':>9} {'OOS Sh':>8} {'4a':>3} {'4b':>3}")
        for _, x in df.sort_values(["N", "gross"]).iterrows():
            mk = " <-anchor" if (x.N == ANCHOR_N and x.gross == ANCHOR_G) else ""
            say(f"  {x.N:3.0f} {x.gross:6.2f} {x.CAGR_FULL:8.2%} {x.Sharpe_FULL:8.4f} "
                f"{x.MaxDD_FULL:8.2%} {x.turnover_yr:8.2f} {x.Sharpe_IS:8.4f} "
                f"{'Y' if x.is4b else '.':>5} {x.is_J:7.2f} {x.CAGR_OOS:9.2%} {x.Sharpe_OOS:8.4f} "
                f"{'Y' if x.pass4a else '.':>3} {'Y' if x.pass4b else '.':>3}{mk}")
        say(f"  {pan.name}: 4b {int(df.pass4b.sum())}/{len(df)}, 4a {int(df.pass4a.sum())}/{len(df)}, "
            f"IS-4b analogue clears {int(df.is4b.sum())}/{len(df)}.")
        say("")

    # ---------------------------------------------------------- control corpora
    say("=" * 100)
    say(f"ARM D — THE MATCHED ZERO-SIGNAL CONTROL: {NSEED} seeds x {len(NS) * len(GROSSES)} cells")
    say("x 3 panels.  Same N, gross, H, cadence, eligibility mask, costs and dates; the composite")
    say("rank is replaced by a uniform random key redrawn at every decision row.")
    say("=" * 100)
    say("")
    CTRL = {}
    for pan in panels:
        seeds = []
        for s in range(NSEED):
            # deterministic per (panel, seed): no hash(), which is salted per process
            rng = np.random.default_rng(1_000_000 + 7919 * s + 101 * PANEL_OFFSET[pan.name])
            d = corpus(pan, B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["W"], rng=rng)
            d["seed"] = s
            d["panel"] = pan.name
            seeds.append(d)
        CTRL[pan.name] = pd.concat(seeds, ignore_index=True)
        say(f"  {pan.name} control built ({time.time() - t0:.0f}s elapsed).")
    say("")
    say("  MATCH CHECK (the control must look like the book on everything but signal):")
    say(f"  {'panel':6} {'turn/yr real':>13} {'turn/yr ctrl':>13} {'ratio':>7} "
        f"{'mean OOS Sh real':>17} {'mean OOS Sh ctrl':>17}")
    for pan in panels:
        R, C = REAL[pan.name], CTRL[pan.name]
        say(f"  {pan.name:6} {R.turnover_yr.mean():13.2f} {C.turnover_yr.mean():13.2f} "
            f"{C.turnover_yr.mean() / R.turnover_yr.mean():7.3f} {R.Sharpe_OOS.mean():17.4f} "
            f"{C.Sharpe_OOS.mean():17.4f}")
    say("")
    say("  Read: a turnover ratio near 1 means the control pays what the book pays; the OOS Sharpe")
    say("  gap between the two corpora is the SIGNAL in the composite, measured corpus-wide.")
    say("")

    # ---------------------------------------------------------- selectors
    say("=" * 100)
    say("ARM E — RULE 8: every selector reads the IS window ONLY; 2017-2026 read ONCE.")
    say("=" * 100)
    say("")
    PICKS, EDGES = [], []
    for pan in panels:
        W = B[pan.name]["W"]
        bs = mt(B[pan.name]["spy"][W["OOS"]])
        bl = mt(B[pan.name]["live"][W["OOS"]])
        R = REAL[pan.name].reset_index(drop=True)
        base_real = float(R.Sharpe_OOS.mean())
        for sel in SELECTORS:
            i = choose(R, sel)
            if i is None:
                rec = dict(panel=pan.name, selector=sel, corpus="REAL", seed=-1, N=np.nan,
                           gross=np.nan, OOS_Sharpe=base_real,
                           OOS_CAGR=float(R.CAGR_OOS.mean()), OOS_MaxDD=float(R.MaxDD_OOS.mean()),
                           pass4b=float(R.pass4b.mean()), pass4a=float(R.pass4a.mean()),
                           beats_SPY=bool(base_real > bs["Sharpe"]), edge=0.0)
            else:
                x = R.loc[i]
                rec = dict(panel=pan.name, selector=sel, corpus="REAL", seed=-1, N=int(x.N),
                           gross=float(x.gross), OOS_Sharpe=float(x.Sharpe_OOS),
                           OOS_CAGR=float(x.CAGR_OOS), OOS_MaxDD=float(x.MaxDD_OOS),
                           pass4b=float(x.pass4b), pass4a=float(x.pass4a),
                           beats_SPY=bool(x.Sharpe_OOS > bs["Sharpe"]),
                           edge=float(x.Sharpe_OOS - base_real))
            rec.update(spy_OOS_Sharpe=bs["Sharpe"], spy_OOS_CAGR=bs["CAGR"],
                       spy_OOS_MaxDD=bs["MaxDD"], live_OOS_Sharpe=bl["Sharpe"],
                       live_OOS_CAGR=bl["CAGR"], live_OOS_MaxDD=bl["MaxDD"])
            PICKS.append(rec)
        C = CTRL[pan.name]
        for s in range(NSEED):
            D = C[C.seed == s].reset_index(drop=True)
            base_c = float(D.Sharpe_OOS.mean())
            for sel in SELECTORS:
                i = choose(D, sel)
                if i is None:
                    PICKS.append(dict(panel=pan.name, selector=sel, corpus="CTRL", seed=s,
                                      N=np.nan, gross=np.nan, OOS_Sharpe=base_c,
                                      OOS_CAGR=float(D.CAGR_OOS.mean()),
                                      OOS_MaxDD=float(D.MaxDD_OOS.mean()),
                                      pass4b=float(D.pass4b.mean()), pass4a=float(D.pass4a.mean()),
                                      beats_SPY=bool(base_c > bs["Sharpe"]), edge=0.0,
                                      spy_OOS_Sharpe=bs["Sharpe"], spy_OOS_CAGR=bs["CAGR"],
                                      spy_OOS_MaxDD=bs["MaxDD"], live_OOS_Sharpe=bl["Sharpe"],
                                      live_OOS_CAGR=bl["CAGR"], live_OOS_MaxDD=bl["MaxDD"]))
                    continue
                x = D.loc[i]
                PICKS.append(dict(panel=pan.name, selector=sel, corpus="CTRL", seed=s,
                                  N=int(x.N), gross=float(x.gross),
                                  OOS_Sharpe=float(x.Sharpe_OOS), OOS_CAGR=float(x.CAGR_OOS),
                                  OOS_MaxDD=float(x.MaxDD_OOS), pass4b=float(x.pass4b),
                                  pass4a=float(x.pass4a),
                                  beats_SPY=bool(x.Sharpe_OOS > bs["Sharpe"]),
                                  edge=float(x.Sharpe_OOS - base_c),
                                  spy_OOS_Sharpe=bs["Sharpe"], spy_OOS_CAGR=bs["CAGR"],
                                  spy_OOS_MaxDD=bs["MaxDD"], live_OOS_Sharpe=bl["Sharpe"],
                                  live_OOS_CAGR=bl["CAGR"], live_OOS_MaxDD=bl["MaxDD"]))
    P = pd.DataFrame(PICKS)

    say("  THE REAL CORPUS — what each selector actually bought, OOS read once:")
    say(f"  {'panel':6} {'selector':12} {'N':>4} {'gross':>6} {'OOS CAGR':>9} {'OOS Sh':>8} "
        f"{'OOS DD':>8} {'EDGE':>8} {'>SPY?':>6} {'4b full':>8}")
    for pan in panels:
        for sel in SELECTORS:
            x = P[(P.panel == pan.name) & (P.corpus == "REAL") & (P.selector == sel)].iloc[0]
            nn = "mean" if not np.isfinite(x.N) else f"{x.N:.0f}"
            gg = "  -  " if not np.isfinite(x.gross) else f"{x.gross:5.2f}"
            p4 = ("PASS" if x.pass4b >= 1 else ("FAIL" if x.pass4b <= 0 else f"{x.pass4b:.2f}"))
            say(f"  {pan.name:6} {sel:12} {nn:>4} {gg:>6} {x.OOS_CAGR:9.2%} {x.OOS_Sharpe:8.4f} "
                f"{x.OOS_MaxDD:8.2%} {x.edge:+8.4f} {'YES' if x.beats_SPY else 'no':>6} {p4:>8}")
        say("")

    say(f"  THE CONTROL — the SAME selectors on {NSEED} signal-free corpora per panel.")
    say(f"  {'panel':6} {'selector':12} {'EDGE real':>10} {'EDGE ctrl mean':>15} {'ctrl SD':>9} "
        f"{'z':>7} {'ctrl pct':>9} {'4b-REC real':>12} {'4b-REC ctrl':>12}")
    for pan in panels:
        for sel in SELECTORS:
            er = float(P[(P.panel == pan.name) & (P.corpus == "REAL") & (P.selector == sel)].edge.iloc[0])
            cc = P[(P.panel == pan.name) & (P.corpus == "CTRL") & (P.selector == sel)]
            m, sd = float(cc.edge.mean()), float(cc.edge.std(ddof=1))
            z = (er - m) / sd if sd > 0 else np.nan
            pct = float((cc.edge <= er).mean())
            r4 = float(P[(P.panel == pan.name) & (P.corpus == "REAL") & (P.selector == sel)].pass4b.iloc[0])
            c4 = float(cc.pass4b.mean())
            EDGES.append(dict(panel=pan.name, selector=sel, edge_real=er, edge_ctrl_mean=m,
                              edge_ctrl_sd=sd, z=z, ctrl_pct=pct, rec4b_real=r4, rec4b_ctrl=c4))
            say(f"  {pan.name:6} {sel:12} {er:+10.4f} {m:+15.4f} {sd:9.4f} "
                f"{(f'{z:+7.2f}' if np.isfinite(z) else '      -')} {pct:9.3f} "
                f"{r4:12.3f} {c4:12.3f}")
        say("")
    E = pd.DataFrame(EDGES)
    say("  Read: EDGE is OOS Sharpe minus the corpus mean's, so 0 = doing nothing.  'ctrl pct' is")
    say("  the share of signal-free corpora whose edge is NO LARGER than the real one.  4b-REC is")
    say("  the share of corpora where the selector's pick clears FULL-sample 4b.")
    say("")

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM F — THE ANSWER")
    say("=" * 100)
    say("")
    k = E[E.selector == "PICK-4b-IS"]
    n_beats = int(((k.z > 2) & (k.edge_real > 0)).sum())
    ctrl_pos = int((k.edge_ctrl_mean > 0.01).sum())
    if k.edge_real.le(0).sum() >= 2:
        outcome = ("(C) NO EDGE EITHER WAY — PICK-4b-IS fails to beat the corpus mean on a "
                   "majority of panels, on real data")
    elif n_beats >= 2 and ctrl_pos == 0:
        outcome = ("(A) LEGITIMATE — PICK-4b-IS's real edge exceeds its own control mean by more "
                   "than 2 control SD on a majority of panels, and its control edge is not "
                   "materially positive")
    else:
        outcome = ("(B) BAR-SHAPED ORACLE — a signal-free corpus reproduces PICK-4b-IS's edge; "
                   "the selector reads the shape of the bar, not the tape")
    say(f"  OUTCOME: {outcome}.")
    say("")
    for _, x in k.iterrows():
        say(f"    {x.panel:6} EDGE real {x.edge_real:+.4f} vs control {x.edge_ctrl_mean:+.4f} "
            f"+/- {x.edge_ctrl_sd:.4f} (z {x.z:+.2f}, pct {x.ctrl_pct:.3f}); "
            f"4b-REC {x.rec4b_real:.2f} real vs {x.rec4b_ctrl:.2f} control")
    say("")
    say("  THE OTHER SELECTORS, same test (mean over panels):")
    say(f"  {'selector':12} {'EDGE real':>10} {'EDGE ctrl':>10} {'mean z':>8} {'4b-REC real':>12} "
        f"{'4b-REC ctrl':>12}")
    for sel in SELECTORS:
        s = E[E.selector == sel]
        say(f"  {sel:12} {s.edge_real.mean():+10.4f} {s.edge_ctrl_mean.mean():+10.4f} "
            f"{s.z.mean():+8.2f} {s.rec4b_real.mean():12.3f} {s.rec4b_ctrl.mean():12.3f}")
    say("")
    cand = P[(P.corpus == "REAL") & (P.selector != "CORPUS-MEAN") & (P.pass4b >= 1) & P.beats_SPY]
    if len(cand):
        say("  Cells a selector reached that clear FULL-sample 4b and beat SPY OOS: " + ", ".join(
            f"{r.panel}/{r.selector} N={r.N:.0f} g={r.gross:.2f} (OOS {r.OOS_CAGR:.2%} / "
            f"{r.OOS_Sharpe:.4f})" for _, r in cand.iterrows()))
        say("  Whether any of these is a KEEP depends on the control column above, not on this row.")
    else:
        say("  NO selector's rule-8 pick clears full-sample 4b and beats SPY out-of-sample.")
    say("")
    say(f"  4b across the whole REAL corpus: {int(sum(REAL[p.name].pass4b.sum() for p in panels))} "
        f"of {sum(len(REAL[p.name]) for p in panels)}; 4a: "
        f"{int(sum(REAL[p.name].pass4a.sum() for p in panels))} of "
        f"{sum(len(REAL[p.name]) for p in panels)}.")
    say("")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT constituents; delisted and")
    say("  bankrupt names are absent, which flatters the drawdown leg specifically.  The control")
    say("  draws from the SAME surviving names, so it is a conservative comparand, not a lenient")
    say("  one.  Every number is a within-grid difference on fixed panels and identical dates.")
    say("")
    say(f"  ({time.time() - t0:.1f}s)")

    pd.concat([REAL[p.name] for p in panels], ignore_index=True).to_csv(
        Path(str(OUT) + ".corpus.csv"), index=False)
    pd.concat([CTRL[p.name] for p in panels], ignore_index=True).to_csv(
        Path(str(OUT) + ".control.csv"), index=False)
    P.to_csv(Path(str(OUT) + ".picks.csv"), index=False)
    E.to_csv(Path(str(OUT) + ".edges.csv"), index=False)
    Path(str(OUT) + ".log.txt").write_text("\n".join(_LOG) + "\n")
    print(f"\nwrote {Path(OUT).name}.corpus.csv / .control.csv / .picks.csv / .edges.csv / .log.txt")


if __name__ == "__main__":
    main()

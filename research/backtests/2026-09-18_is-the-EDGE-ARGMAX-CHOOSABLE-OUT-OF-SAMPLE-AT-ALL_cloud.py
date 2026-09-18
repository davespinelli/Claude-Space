#!/usr/bin/env python3
"""Idea 1084 (lane cloud, 2026-09-18): is the EDGE ARGMAX CHOOSABLE OUT OF SAMPLE AT ALL?

QUESTION.  Idea 1082 found the full-sample EDGE argmax (n=12 on one panel, n=10 on the other)
is NOT what any IS-only chooser picks — C_ISEDGE picked n=5 on both panels, so its H_ISEDGE
failed — which means a 3.9-8.1 SE effect in the record is unreachable by an honest procedure.
The queue asks for the direct measurement: the IS-vs-OOS rank correlation of EDGE across the
9 rungs, and whether the edge ladder carries ANY out-of-sample selection information.

WHAT "EDGE" MEANS HERE — the record's convention, unchanged from 1071/1082/1086/1093/1172 and
quoted so the six runs read together:
    EDGE(n, H) = book CAGR  -  MEDIAN over 40 seeds of the DD-MATCHED null's CAGR,
    where the null is the SAME machinery (N slots, min hold H, equal weight gross/len(sel),
    weight of unfilled slots to CASH) driven by UNIFORM RANDOM ranks with NO eligibility gate,
    REBUILT at gross lam * 0.75 with lam in [1e-4, 1.0] bisected (34 steps) so the null's
    |MaxDD| equals the book's OVER THE SAME ROWS.  A draw already drier than the book at
    lam = 1 enters unmatched (lam := 1), which INFLATES EDGE; that clip is the record's and is
    kept so the numbers are comparable, and the count of clipped draws is published per cell.
    EDGE IS NOT A KEEP PATH and nothing here proposes it as one.

THE CRITICAL POINT OF THIS RUN: EDGE is computed SEPARATELY INSIDE EACH WINDOW.  EDGE_IS uses
the book's IS MaxDD as the matching target and the null's IS CAGR; EDGE_OOS uses the OOS ones.
No number crosses the split.  1082's EDGE_IS_pp matched on the IS window only, so the IS side
here is that statistic; the OOS side is new.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    N      [5, 8, 10, 12, 15, 20, 25, 30, 40] — 1082's OWN 9 rungs, unchanged.
    SPLIT  {2014-12-31, 2016-12-31, 2018-12-31} — the WINDOW SPLIT.  2016-12-31 is rule 8's
           own split and the headline; the other two exist so the answer cannot be one split's
           accident.  The three IS windows are strictly nested (gate G8).
  9 x 3 = 27 (N, SPLIT) cells per (panel, H), 108 in the main grid, EVERY ONE PUBLISHED.

NOT DIALS, reported at every value: PANEL {U56, B136} (1082's two); H {63, 126} in the main
grid and H=21 additionally for the cross-run gate G4; CHOOSER {C_ISEDGE (1082's), C_ISSHARPE,
C_ISCAGR}; both KEEP paths leg by leg at every rung book; full / halves / IS / OOS everywhere.

FROZEN, NOT DIALS: CAND20 composite of the 12-1 / 6m / 3m percentile ranks; eligibility =
above own 200d MA AND 20d vol < 0.60; cap INF; gross 0.75; WEEKLY cadence; 10 bps per unit
turnover; next-day execution (LAG 1); 260-row warm-up; NSEED = 40 and the seed recipe
md5(panel|N|INF|seed) — 1082's recipe verbatim, which deliberately carries no H term, so
1093's committed EDGE figures are reproducible cell for cell (gate G4).

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) NO INFORMATION — |rho(EDGE_IS, EDGE_OOS)| < 0.3 at a majority of (panel, H, split) cells
      AND C_ISEDGE's pick-minus-anchor OOS EDGE is inside 2 seed SE.  Then every committed
      EDGE argmax in the record describes one window and is not a rule, and 1082's H_ISEDGE
      failure is the general case rather than a quirk of its split.
  (B) POSITIVE — rho >= +0.3 at a majority AND the pick beats the anchor's OOS EDGE past 2 SE.
      Then the ladder carries selection information and the record may quote its argmax.
  (C) ANTI-INFORMATION — rho <= -0.3 at a majority.  Then picking the IS EDGE argmax is worse
      than doing nothing, which is a stronger result than (A) and is reported as such.
  (D) SPLIT-DEPENDENT — the SIGN of rho flips across the split dial at a majority of (panel, H)
      families.  Then rho is not a property of the ladder at all and no single number should be
      published for it.
  The capital line is reported FIRST in every case: the pick's OOS Sharpe and OOS CAGR/MaxDD
  against the ANCHOR N=20 over the same rows, against SPY, and both KEEP paths.

RULE 8 (walk-forward, required).  Every chooser sees the IS window ALONE; each OOS window is
read ONCE per split.  Published per (panel, H, split, chooser): the pick, whether it reaches
the anchor N=20, the pick's OOS Sharpe/CAGR/MaxDD, the anchor's over the same rows, the ladder
mean/best/worst, SPY's, the pick's OOS EDGE and the OOS EDGE argmax it failed to find, and the
IS/OOS rank correlation of BOTH EDGE and Sharpe over the 9 rungs.

GATES.  G1 the fast runner reproduces engine.backtest on the U56 anchor book (N=20, H=126, W,
gross 0.75).  G1b gross_rescaler f(1.0) reproduces that same net return path.  G2 CROSS-RUN:
the anchor's (CAGR, Sharpe, MaxDD) reproduces 936/1082/1174's committed triple (0.155787,
1.139701, -0.191276).  G3 CROSS-RUN SPY OOS triple (0.1521, 0.8713, -0.3372).  G2/G3 are read
on the tape TRUNCATED to 2026-09-15, where the tape ended when those numbers were committed;
live-tape readings print beside them, ungated.  G4 CROSS-RUN 1093's committed FULL-SAMPLE EDGE
at n in {5, 8, 10} x H in {21, 63, 126} on both panels — 18 cells, the premise of this whole
family.  G5 the live RULES v2 MaxDD == the committed -12.05%.  G6 |MaxDD| of the rebuilt null
is monotone in lam, so the bisection is well posed.  G7 the null draw is deterministic in its
seed recipe.  G8 the three splits are strictly nested and every OOS window holds >= 1000 rows.
G9 determinism: the anchor book recomputes bit for bit.  G4 is read on the tape truncated to
2026-09-15 for the same reason G2/G3 are; the live-tape reading of the same 9 cells prints
beside it as G4b, ungated, because U56's cache has since grown by two rows and those two rows
move a committed EDGE figure by up to 0.098 pp.  Every gate is published, pass or fail.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point, 2 dials;
rule 5 one idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship
stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists, so every absolute level is
optimistic and every 4b pass is an UPPER bound.  EDGE is a book-minus-null CONTRAST on the
same panel and the same dates, so the level bias cancels to first order in the headline; the
4a/4b legs and every absolute CAGR do not.  Note the direction that does not cancel: the null
draws from the same survivor list, so both sides are flattered and the MATCHED comparison is
the honest part while the DD-matching target itself is a flattered drawdown.

G4 FAILED ON U56 AND IS PUBLISHED AS A FAILURE, WITH ITS CAUSE MEASURED.  B136 reproduces
1093's nine committed EDGE figures to 4.587e-07 pp, so the machinery in this file IS 1093's.
U56's nine reproduce only to 5.540e-02 pp on the truncated tape (9.801e-02 on the live one),
because data/prices.csv has been REWRITTEN since 1093 ran: comparing today's cache with the
copy committed at 0d82185 (2026-09-17) gives one added row (2026-09-17) AND revised history on
shared cells — max relative change 5.1e-05 on AVGO, 2.7e-05 on AAPL, 2.4e-05 on NVDA (9.2e-04
on the excluded crypto columns), while data/prices_broad.csv has not moved.  A 1e-05 shift in
a close moves the DD-matching bisection, which moves lam, which moves the null's CAGR, so a
committed EDGE figure on the daily-refreshed panel is only reproducible to ~0.06 pp — about
1% of its own value.  That is a fact about the record's reproducibility, not about this run,
and it is why G4 is reported FAIL rather than re-tuned to pass.

Runs standalone and offline (committed price caches only).
"""
from __future__ import annotations

import hashlib
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

DATE = "2026-09-18"
SLUG = "is-the-EDGE-ARGMAX-CHOOSABLE-OUT-OF-SAMPLE-AT-ALL"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

# ---- frozen construction (NOT dials) --------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"
NSEED = 40
BISECT = 34
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COMMIT_TAPE_END = "2026-09-15"
RHO_BAR = 0.30

# ---- the two dials ---------------------------------------------------------------------------
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]                 # 1082's 9 rungs
SPLITS = ["2014-12-31", "2016-12-31", "2018-12-31"]     # rule 8's own split is the middle one
HEADLINE_SPLIT = "2016-12-31"

HS_MAIN = [63, 126]
HS_GATE = [21]
ANCHOR_N = 20
PANELS = ["U56", "B136"]
CHOOSERS = ["C_ISEDGE", "C_ISSHARPE", "C_ISCAGR"]

# ---- committed cross-run constants ----------------------------------------------------------
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1093_EDGE = {                                   # 1093's committed null.csv, full-sample EDGE_pp
    ("B136", 21): {5: 8.074181, 8: 4.841524, 10: 5.543762},
    ("B136", 63): {5: 11.268996, 8: 8.822182, 10: 7.662768},
    ("B136", 126): {5: 5.717069, 8: 5.244527, 10: 8.323841},
    ("U56", 21): {5: 5.930208, 8: 6.162706, 10: 7.319234},
    ("U56", 63): {5: 6.598641, 8: 8.029465, 10: 6.776615},
    ("U56", 126): {5: 5.954659, 8: 5.295494, 10: 6.163594},
}

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


def mdseed(*parts):
    """1082's recipe verbatim — deliberately carries NO H term."""
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ------------------------------------------------------------------ metrics (1082/1172's)
def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    c = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return c, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


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
    nsel = []
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
        nsel.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W, np.array(nsel)


def build_null(rank_key, priced, reb, N, H, T, K, gross):
    """Same machinery, random ranks, NO eligibility gate (the record's convention)."""
    elig = np.ones((T, K), dtype=bool)
    return build(rank_key, elig, priced, reb, N, H, T, K, gross)


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


def gross_rescaler(rets, wt, mk):
    """f(lam) -> NET returns of the book REBUILT at gross lam * (this book's gross).
    1082's kernel, unmodified; f(1.0) is gated against nrun() exactly (G1b)."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0
    Sp[0] = 0.0
    Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4

    def f(lam):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        return out

    return f


def lam_rebuilt(f, sl, target_dd, hi=1.0):
    """Largest lam <= hi whose REBUILT |MaxDD| over rows `sl` does not exceed the book's.
    Returns None when the draw is already drier than the book at lam = hi (the clip binds)."""
    if abs(maxdd(f(hi)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, hi
    for _ in range(BISECT):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


# ------------------------------------------------------------------ KEEP paths
def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def blocks(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1084 lane cloud — {SLUG}")
    say(f"# DIAL 1 N = {NS} (1082's 9 rungs)   DIAL 2 SPLIT = {SPLITS} (rule 8's own is {HEADLINE_SPLIT})")
    say(f"# NOT dials, all reported: PANEL {PANELS}; H {HS_MAIN} (+{HS_GATE} for gate G4); CHOOSER {CHOOSERS}")
    say(f"# EDGE = book CAGR - median over {NSEED} seeds of the DD-MATCHED (rebuilt, lam<=1, "
        f"{BISECT}-step bisection) null CAGR, computed SEPARATELY INSIDE EACH WINDOW")
    say(f"# frozen: CAND20 legs {LEGS}, elig above-200d & vol20<{MAXVOL}, cap {CAPNAME}, gross {GROSS0}, "
        f"cadence {FREQ}, {COST:.0f} bps, t+{LAG}, warm-up {WARMUP}, seed recipe md5(panel|N|{CAPNAME}|seed)")
    say("# PRE-DECLARED: (A) no information / (B) positive / (C) anti-information / (D) split-dependent; "
        f"|rho| bar {RHO_BAR}")

    gridrows, nullrows, r8rows, rhorows, seedrows = [], [], [], [], []

    for pi, panel in enumerate(PANELS):
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        T, K = len(idx), len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        reb = np.flatnonzero(mk)
        warm = np.zeros(T, dtype=bool)
        warm[WARMUP:] = True
        itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
        warm15 = warm & (np.arange(T) < itr)      # the tape as it stood when 1093 committed G4
        spy_r = px["SPY"].pct_change().fillna(0.0).values
        live_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        say(f"\n## {panel}  n_days={T}  n_cols={K}  {idx[0].date()}..{idx[-1].date()}")

        # window masks per split
        WIN = {}
        for sp in SPLITS:
            oos = np.asarray(idx > pd.Timestamp(sp)) & warm
            ins = warm & ~oos
            WIN[sp] = (ins, oos)
            say(f"   split {sp}: IS rows {int(ins.sum())}  OOS rows {int(oos.sum())}")
        if pi == 0:
            nested = all(set(np.flatnonzero(WIN[SPLITS[i]][0])) <= set(np.flatnonzero(WIN[SPLITS[i + 1]][0]))
                         for i in range(len(SPLITS) - 1))
            gate("G8 the three splits are strictly nested and every OOS window has >= 1000 rows",
                 f"nested={nested}, min OOS rows {min(int(WIN[s][1].sum()) for s in SPLITS)}",
                 "True and >= 1000",
                 nested and min(int(WIN[s][1].sum()) for s in SPLITS) >= 1000)

        SB = {sp: blocks(spy_r, warm, *WIN[sp]) for sp in SPLITS}
        LB = {sp: blocks(live_r, warm, *WIN[sp]) for sp in SPLITS}
        hs = SB[HEADLINE_SPLIT]
        say(f"   SPY     full {hs['CAGR']:7.2%} / {hs['Sharpe']:.4f} / {hs['MaxDD']:7.2%}"
            f"   OOS({HEADLINE_SPLIT}) {hs['OOS_CAGR']:7.2%} / {hs['OOS_Sharpe']:.4f} / {hs['OOS_MaxDD']:7.2%}")
        hl = LB[HEADLINE_SPLIT]
        say(f"   RULESv2 full {hl['CAGR']:7.2%} / {hl['Sharpe']:.4f} / {hl['MaxDD']:7.2%}")

        if pi == 0:
            Wa, _ = build(rank_key, elig, priced, reb, ANCHOR_N, 126, T, K, GROSS0)
            g, tn = nrun(rets, lagmat(Wa), mkl)
            ra = g - tn * COST / 1e4
            eng = backtest(px, pd.DataFrame(Wa, index=idx, columns=px.columns),
                           cost_bps=COST, freq=FREQ)["returns"].values
            d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - ra[WARMUP:])))
            gate("G1 fast runner == engine.backtest (U56 N=20 H=126)", f"{d1:.3e}", "< 1e-12", d1 < 1e-12)
            fa = gross_rescaler(rets, lagmat(Wa), mkl)
            d1b = float(np.abs(fa(1.0) - ra).max())
            gate("G1b gross_rescaler f(1.0) == the fast runner's net path", f"{d1b:.3e}", "< 1e-14", d1b < 1e-14)
            mfull = fmet(ra[WARMUP:])
            mtr = fmet(ra[WARMUP:itr])
            say(f"   U56 anchor on the LIVE tape (ungated): {mfull[0]:.6f}/{mfull[1]:.6f}/{mfull[2]:.6f}")
            d2 = max(abs(mtr[i] - A936_WH126[i]) for i in range(3))
            gate(f"G2 CROSS-RUN U56 N=20 H=126 triple == committed (tape to {COMMIT_TAPE_END})",
                 f"{mtr[0]:.6f}/{mtr[1]:.6f}/{mtr[2]:.6f} maxdiff {d2:.2e}", f"{A936_WH126} < 5e-3", d2 < 5e-3)
            wt_ = np.zeros(T, dtype=bool)
            wt_[WARMUP:itr] = True
            oos_tr = np.asarray(idx > pd.Timestamp(HEADLINE_SPLIT)) & wt_
            sbt = fmet(spy_r[oos_tr])
            d3 = max(abs(sbt[i] - SPY_OOS_COMMITTED[i]) for i in range(3))
            gate(f"G3 CROSS-RUN SPY OOS triple (tape to {COMMIT_TAPE_END}; live tape "
                 f"{hs['OOS_CAGR']:.4f}/{hs['OOS_Sharpe']:.4f}/{hs['OOS_MaxDD']:.4f})",
                 f"{sbt[0]:.4f}/{sbt[1]:.4f}/{sbt[2]:.4f} maxdiff {d3:.2e}",
                 f"{SPY_OOS_COMMITTED} < 5e-4", d3 < 5e-4)
            gate("G5 live RULES v2 MaxDD == committed -12.05%", f"{hl['MaxDD']:.4f}",
                 f"{LIVE_MAXDD_COMMITTED} < 5e-4", abs(hl["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)
            rngc = np.random.default_rng(mdseed(panel, ANCHOR_N, CAPNAME, 0))
            Wn0, _ = build_null(rngc.random((T, K)), priced, reb, ANCHOR_N, 126, T, K, GROSS0)
            fn0 = gross_rescaler(rets, lagmat(Wn0), mkl)
            dds = [abs(maxdd(fn0(l)[warm])) for l in np.linspace(0.05, 1.0, 25)]
            viol = float(max(0.0, max(dds[i] - dds[i + 1] for i in range(len(dds) - 1))))
            gate("G6 |MaxDD| of the rebuilt null is monotone in lam over [0.05, 1.0] "
                 "(the bisection is well posed)", f"{viol:.3e}", "< 1e-12", viol < 1e-12)
            rngd = np.random.default_rng(mdseed(panel, ANCHOR_N, CAPNAME, 0))
            Wn0b, _ = build_null(rngd.random((T, K)), priced, reb, ANCHOR_N, 126, T, K, GROSS0)
            gate("G7 the null draw is deterministic in its seed recipe",
                 f"{float(np.abs(Wn0 - Wn0b).max()):.3e}", "== 0.0", float(np.abs(Wn0 - Wn0b).max()) == 0.0)
            Wa2, _ = build(rank_key, elig, priced, reb, ANCHOR_N, 126, T, K, GROSS0)
            g2, tn2 = nrun(rets, lagmat(Wa2), mkl)
            gate("G9 determinism (anchor book recomputes bit for bit)",
                 f"{float(np.abs((g2 - tn2 * COST / 1e4) - ra).max()):.3e}", "== 0.0",
                 float(np.abs((g2 - tn2 * COST / 1e4) - ra).max()) == 0.0)

        # --------------------------------------------------------- the grid
        EDGE = {}          # (H, N, key) -> edge pp,   key in {"FULL"} | splits x {"IS","OOS"}
        ESE = {}           # matching seed SE
        BOOK = {}          # (H, N) -> blocks at the headline split + return path
        for H in HS_MAIN + HS_GATE:
            for N in NS:
                W, nsel = build(rank_key, elig, priced, reb, N, H, T, K, GROSS0)
                g, tn = nrun(rets, lagmat(W), mkl)
                r = g - tn * COST / 1e4
                b = blocks(r, warm, *WIN[HEADLINE_SPLIT])
                BOOK[(H, N)] = (r, b)
                turn = float(tn[warm].sum() / (warm.sum() / 252.0))
                if H in HS_MAIN:
                    l4b, l4a = legs_4b(b, SB[HEADLINE_SPLIT]), legs_4a(b, LB[HEADLINE_SPLIT])
                    gridrows.append(dict(panel=panel, H=H, N=N, mean_nsel=float(nsel.mean()),
                                         turn_yr=turn, **b, **l4b, **l4a,
                                         pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                                         fail4b=failed(l4b), fail4a=failed(l4a)))
                # ---- the null, 40 seeds, DD-matched inside each window
                targets = {"FULL": (warm, b["MaxDD"]),
                           "FULL15": (warm15, maxdd(r[warm15]))}
                if H in HS_MAIN:
                    for sp in SPLITS:
                        ins, oos = WIN[sp]
                        targets[f"{sp}|IS"] = (ins, maxdd(r[ins]))
                        targets[f"{sp}|OOS"] = (oos, maxdd(r[oos]))
                acc = {k: [] for k in targets}
                clip = {k: 0 for k in targets}
                for s in range(NSEED):
                    rk = np.random.default_rng(mdseed(panel, N, CAPNAME, s)).random((T, K))
                    Wn, _ = build_null(rk, priced, reb, N, H, T, K, GROSS0)
                    fn = gross_rescaler(rets, lagmat(Wn), mkl)
                    base = fn(1.0)
                    for kk, (sl, tgt) in targets.items():
                        lr = lam_rebuilt(fn, sl, tgt, hi=1.0)
                        if lr is None:
                            acc[kk].append(fmet(base[sl])[0])
                            clip[kk] += 1
                        else:
                            acc[kk].append(fmet(fn(lr)[sl])[0])
                    seedrows.append(dict(panel=panel, H=H, N=N, seed=s,
                                         **{f"nullCAGR_{k.replace('|','_')}": acc[k][-1] for k in targets}))
                for kk in targets:
                    a = np.array(acc[kk], float)
                    bookc = fmet(r[targets[kk][0]])[0]
                    e = 100.0 * (bookc - float(np.median(a)))
                    se = 100.0 * 1.2533 * float(a.std(ddof=1)) / np.sqrt(NSEED)
                    EDGE[(H, N, kk)] = e
                    ESE[(H, N, kk)] = se
                    nullrows.append(dict(panel=panel, H=H, N=N, window=kk, seeds=NSEED,
                                         book_CAGR=bookc, book_MaxDD=targets[kk][1],
                                         null_CAGR_med=float(np.median(a)), EDGE_pp=e, EDGE_se_pp=se,
                                         null_CAGR_sd=float(a.std(ddof=1)),
                                         book_pct_of_null=float((a < bookc).mean()),
                                         n_clipped_at_lam1=clip[kk]))
            say(f"   {panel} H={H}: books+nulls done  [t={time.time()-t0:.0f}s]")

        # ---- G4: 1093's committed full-sample EDGE at the shared rungs
        if True:
            d4 = d4l = 0.0
            ncmp = 0
            for (p_, H_), vals in A1093_EDGE.items():
                if p_ != panel:
                    continue
                for n_, v_ in vals.items():
                    d4 = max(d4, abs(EDGE[(H_, n_, "FULL15")] - v_))
                    d4l = max(d4l, abs(EDGE[(H_, n_, "FULL")] - v_))
                    ncmp += 1
            gate(f"G4 CROSS-RUN 1093's committed full-sample EDGE, {panel}, n in {{5,8,10}} x "
                 f"H in {{21,63,126}} ({ncmp} cells — the premise itself; tape truncated to "
                 f"{COMMIT_TAPE_END}, where 1093's figures were committed)", f"maxdiff {d4:.3e}",
                 "< 5e-3", d4 < 5e-3 and ncmp == 9)
            say(f"   G4b UNGATED, the same 9 cells on the LIVE tape: maxdiff {d4l:.3e} pp. "
                f"{panel}'s cache ends {idx[-1].date()}; where it has grown since "
                f"{COMMIT_TAPE_END} the committed EDGE figures no longer reproduce, which is a "
                f"property of the tape, not of the machinery.")

        # ---- the answer: IS/OOS rank correlation and the rule-8 picks
        for H in HS_MAIN:
            for sp in SPLITS:
                e_is = np.array([EDGE[(H, N, f"{sp}|IS")] for N in NS])
                e_oos = np.array([EDGE[(H, N, f"{sp}|OOS")] for N in NS])
                se_is = np.array([ESE[(H, N, f"{sp}|IS")] for N in NS])
                se_oos = np.array([ESE[(H, N, f"{sp}|OOS")] for N in NS])
                bl = [blocks(BOOK[(H, N)][0], warm, *WIN[sp]) for N in NS]
                s_is = np.array([b["IS_Sharpe"] for b in bl])
                s_oos = np.array([b["OOS_Sharpe"] for b in bl])
                rho_e = rankcorr(e_is, e_oos)
                rho_s = rankcorr(s_is, s_oos)
                ai = NS.index(ANCHOR_N)
                jf = int(np.nanargmax([EDGE[(H, N, "FULL")] for N in NS]))
                rhorows.append(dict(panel=panel, H=H, split=sp, rho_EDGE=rho_e, rho_Sharpe=rho_s,
                                    argmax_EDGE_IS=NS[int(np.nanargmax(e_is))],
                                    argmax_EDGE_OOS=NS[int(np.nanargmax(e_oos))],
                                    argmax_EDGE_FULL=NS[jf],
                                    argmax_Sharpe_IS=NS[int(np.nanargmax(s_is))],
                                    argmax_Sharpe_OOS=NS[int(np.nanargmax(s_oos))],
                                    EDGE_IS_spread=float(np.nanmax(e_is) - np.nanmin(e_is)),
                                    EDGE_OOS_spread=float(np.nanmax(e_oos) - np.nanmin(e_oos)),
                                    mean_EDGE_se_IS=float(se_is.mean()),
                                    mean_EDGE_se_OOS=float(se_oos.mean())))
                say(f"\n   {panel} H={H} split {sp}:  rho(EDGE_IS, EDGE_OOS) = {rho_e:+.4f}   "
                    f"rho(Sharpe) = {rho_s:+.4f}")
                say(f"      EDGE_IS  " + "  ".join(f"{N}:{e_is[j]:+.2f}" for j, N in enumerate(NS)))
                say(f"      EDGE_OOS " + "  ".join(f"{N}:{e_oos[j]:+.2f}" for j, N in enumerate(NS)))
                say(f"      argmax EDGE IS={NS[int(np.nanargmax(e_is))]} OOS={NS[int(np.nanargmax(e_oos))]} "
                    f"FULL={NS[jf]}; mean seed SE IS {se_is.mean():.3f} OOS {se_oos.mean():.3f} pp")
                for ch in CHOOSERS:
                    v = {"C_ISEDGE": e_is, "C_ISSHARPE": s_is,
                         "C_ISCAGR": np.array([b["IS_CAGR"] for b in bl])}[ch]
                    j = int(np.nanargmax(v))
                    pb, ab = bl[j], bl[ai]
                    l4b, l4a = legs_4b(pb, SB[sp]), legs_4a(pb, LB[sp])
                    pair_se = float(np.hypot(se_oos[j], se_oos[ai]))
                    r8rows.append(dict(panel=panel, H=H, split=sp, chooser=ch, pick_N=NS[j],
                                       reach_anchor=int(NS[j] == ANCHOR_N),
                                       reach_OOS_EDGE_argmax=int(j == int(np.nanargmax(e_oos))),
                                       pick_OOS_S=pb["OOS_Sharpe"], anchor_OOS_S=ab["OOS_Sharpe"],
                                       delta_OOS_S=pb["OOS_Sharpe"] - ab["OOS_Sharpe"],
                                       ladder_mean_OOS_S=float(np.nanmean(s_oos)),
                                       best_OOS_S=float(np.nanmax(s_oos)), worst_OOS_S=float(np.nanmin(s_oos)),
                                       spy_OOS_S=SB[sp]["OOS_Sharpe"],
                                       pick_OOS_EDGE=e_oos[j], anchor_OOS_EDGE=e_oos[ai],
                                       best_OOS_EDGE=float(np.nanmax(e_oos)),
                                       delta_OOS_EDGE=e_oos[j] - e_oos[ai], pair_EDGE_se=pair_se,
                                       delta_EDGE_over_2se=(e_oos[j] - e_oos[ai]) / (2 * pair_se)
                                       if pair_se > 0 else np.nan,
                                       pick_OOS_CAGR=pb["OOS_CAGR"], pick_OOS_DD=pb["OOS_MaxDD"],
                                       anchor_OOS_CAGR=ab["OOS_CAGR"], anchor_OOS_DD=ab["OOS_MaxDD"],
                                       spy_OOS_CAGR=SB[sp]["OOS_CAGR"], spy_OOS_DD=SB[sp]["OOS_MaxDD"],
                                       rho_EDGE=rho_e, pass4b=all(l4b.values()), fail4b=failed(l4b),
                                       pass4a=all(l4a.values()), fail4a=failed(l4a)))
                    say(f"      rule8 {ch:11s} picks N={NS[j]:2d} (anchor {ANCHOR_N})  OOS S {pb['OOS_Sharpe']:.4f} "
                        f"vs anchor {ab['OOS_Sharpe']:.4f} (d {pb['OOS_Sharpe']-ab['OOS_Sharpe']:+.4f}, SPY "
                        f"{SB[sp]['OOS_Sharpe']:.4f})  OOS EDGE {e_oos[j]:+.2f} vs anchor {e_oos[ai]:+.2f} "
                        f"(d {e_oos[j]-e_oos[ai]:+.2f} = {(e_oos[j]-e_oos[ai])/(2*pair_se) if pair_se>0 else float('nan'):+.2f} x 2SE)"
                        f"  4b {'PASS' if all(l4b.values()) else 'FAIL ' + failed(l4b)}")

    g = pd.DataFrame(gridrows)
    nl = pd.DataFrame(nullrows)
    rh = pd.DataFrame(rhorows)
    r8 = pd.DataFrame(r8rows)
    dump(g, "grid")
    dump(nl, "null")
    dump(rh, "rho")
    dump(r8, "walkforward")
    dump(pd.DataFrame(seedrows), "seeds")
    dump(pd.DataFrame(GATES), "gates")

    say("\n" + "=" * 100)
    say("## ANSWER")
    say(f"   rho(EDGE_IS, EDGE_OOS) over {len(rh)} (panel, H, split) cells: mean {rh.rho_EDGE.mean():+.4f}, "
        f"median {rh.rho_EDGE.median():+.4f}, min {rh.rho_EDGE.min():+.4f}, max {rh.rho_EDGE.max():+.4f}")
    say(f"   |rho| >= {RHO_BAR} at {int((rh.rho_EDGE.abs() >= RHO_BAR).sum())}/{len(rh)} cells; "
        f"rho > 0 at {int((rh.rho_EDGE > 0).sum())}/{len(rh)}")
    say(f"   rho(Sharpe_IS, Sharpe_OOS) for comparison: mean {rh.rho_Sharpe.mean():+.4f}, "
        f"positive at {int((rh.rho_Sharpe > 0).sum())}/{len(rh)}")
    sf = rh.groupby(["panel", "H"]).rho_EDGE.apply(lambda x: len(set(np.sign(x))) > 1)
    say(f"   SIGN of rho flips across the split dial at {int(sf.sum())}/{len(sf)} (panel, H) families")
    say(f"   IS EDGE argmax == OOS EDGE argmax at "
        f"{int((rh.argmax_EDGE_IS == rh.argmax_EDGE_OOS).sum())}/{len(rh)} cells; "
        f"IS argmax rungs {sorted(set(rh.argmax_EDGE_IS))}, OOS argmax rungs {sorted(set(rh.argmax_EDGE_OOS))}")
    e8 = r8[r8.chooser == "C_ISEDGE"]
    say(f"   C_ISEDGE: pick-minus-anchor OOS EDGE mean {e8.delta_OOS_EDGE.mean():+.4f} pp, "
        f"positive at {int((e8.delta_OOS_EDGE > 0).sum())}/{len(e8)}, "
        f"past 2 paired seed SE at {int((e8.delta_EDGE_over_2se.abs() >= 1).sum())}/{len(e8)}")
    say(f"   C_ISEDGE: pick-minus-anchor OOS SHARPE mean {e8.delta_OOS_S.mean():+.4f}, "
        f"positive at {int((e8.delta_OOS_S > 0).sum())}/{len(e8)}; reaches the OOS EDGE argmax at "
        f"{int(e8.reach_OOS_EDGE_argmax.sum())}/{len(e8)}, the anchor at {int(e8.reach_anchor.sum())}/{len(e8)}")
    say(f"   ALL choosers: pick-minus-anchor OOS Sharpe mean {r8.delta_OOS_S.mean():+.4f}, "
        f"positive at {int((r8.delta_OOS_S > 0).sum())}/{len(r8)}")
    say(f"   4b PASS at {int(g.pass4b.sum())}/{len(g)} rung books; 4a PASS at {int(g.pass4a.sum())}/{len(g)}; "
        f"picks 4b PASS at {int(r8.pass4b.sum())}/{len(r8)}")
    say(f"   gates: {sum(x['pass_'] for x in GATES)}/{len(GATES)} PASS")
    say(f"   [t={time.time()-t0:.0f}s]")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 1166 (lane C, 2026-09-17) — does the TENT survive when the DRAWDOWN LEG is replaced
by a NON-EXPOSURE one?

(Claimed as queue idea 1163, RENUMBERED 1164 on claim because 1163 was already taken in the
queue's Done section by the cloud lane's is-the-RECORD-REPRODUCIBLE-AT-ALL idea, then 1166 on push
because lane B's concurrent push filed new open ideas 1164 and 1165 first.  Defect 932 again.)

Idea 1154 found that C_IS4B — the argmax over a dial of min(M_S, M_DD, M_CAGR), the three
IS-only 4b leg margins — is the ONE chooser that reaches the gross dial's INTERIOR (0.625 on
U56, 0.575 on B136) while all four single-statistic choosers land on an endpoint, and gave the
mechanism: on gross, M_DD runs +0.7127 -> -0.3903 while M_CAGR runs -0.6485 -> +0.7738, i.e.
two EXPOSURE legs (1150's word: quantities that scale with gross) are monotone in OPPOSITE
directions, so their MIN is a TENT and a tent's argmax is interior.  A ratio was not enough
(C_ISMAR stayed monotone, still picked 1.00).

THE QUEUE'S QUESTION, TAKEN LITERALLY: swap L_DD for a leg that is NOT an exposure object and
report whether the tent, and the interior pick, survive.  If the mechanism reading is right,
the tent is a property of the PAIR's homogeneity degrees and not of drawdown, so:
  - swapping in another DEGREE-1 (exposure) leg keeps the tent;
  - swapping in a DEGREE-0 (scale-free) leg collapses the min to a monotone ramp, and the
    interior pick dies, because only one exposure leg is left to slope.
That prediction is stated as H_TENTLIVES / H_TENTDIES BEFORE any number is read, and the
homogeneity degree of every leg statistic is MEASURED here rather than asserted (G12 measures
the same slopes on an exactly-scaled synthetic book so the machinery is validated first).

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  LEG   {L_DD (control, 1154's), L_VOLTGT, L_TUW, L_ULCER}     (4 swapped legs)
  DIAL  {D_GROSS, D_N, D_HOLD, D_CADENCE, D_MAXVOL}            (5 ladders, 66 rungs per panel)
= 20 (leg, dial) cells per panel, 40 in all, EVERY ONE PUBLISHED.  The RUNG inside a dial is
NOT a third parameter: it is the object the chooser selects, and every rung of every dial on
both panels is published in `.grid.csv` whatever any chooser did with it.  PANEL {U56, B136}
is NOT a dial — both are reported everywhere and nothing is selected on the pair.  The two
Sharpe/CAGR legs of the min are NEVER swapped; only the third leg moves, which is what makes
the four choosers comparable.

THE CAP MULTIPLIER IS NOT A THIRD PARAMETER, AND THE REASON IS ALGEBRA: a cap-form margin
(mult*spy - book)/(mult*spy) = 1 - book/(mult*spy) is a POSITIVE AFFINE transform of -book, so
each leg's own monotonicity, direction and rank correlation over any ladder are EXACTLY
invariant to the multiplier (G11 verifies).  The multiplier can only move the LEVEL of one leg
relative to the others, i.e. where the legs cross, so it is published as a sensitivity annex
(.mult.csv, 4 multipliers x every cell) with the verdict read at the PRE-DECLARED primary:
0.60 for L_DD (4b's own constant, so the control reproduces 1154 exactly) and 1.00 for
L_VOLTGT and L_TUW ("no more volatile / no longer underwater than SPY").  L_ULCER is a
beat-SPY leg like 4b's Sharpe legs and has no multiplier at all.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1150/1154's construction so the numbers
cross-read: CAND20 legs [(21,252),(0,126),(0,63)], cap INF, max_vol 0.60, min hold 126, N=20,
gross 0.75, cadence W, cost 10 bps (PROTOCOL rule 2 — a book cannot choose its cost rate),
LAG 1, warm-up 260, IS end 2016-12-31, zero cash, block L=63, 500 draws, crc32 seeds.

PRICE VINTAGE, PINNED AND DECLARED.  `data/prices.csv` is NOT append-only (idea 1159's defect,
censused by 1163-cloud on 2026-09-17: 9.1-12.4% of shared cells restated every night back to
2008-01-02, 6 of the record's 10 committed cross-run anchors no longer reproducing).  Every
tape here is truncated at PIN = 2026-09-15 for cross-readability with 1150/1154 and G2/G3 are
run BOTH ways, so the vintage is PUBLISHED, not absorbed.  A reproduction gate that fails is
reported as a FAIL with its deviation, never re-toleranced into a pass.

Writes: .gates.csv .grid.csv .shapes.csv .degree.csv .picks.csv .mult.csv .hypotheses.csv
        .walkforward.csv .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / scan.py / bot.py /
baseline.py.
"""
import sys, time, zlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-the-TENT-survive-when-the-DRAWDOWN-LEG-is-replaced-by-a-NON-EXPOSURE-one"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

PIN = "2026-09-15"
LAG, WARMUP, MAXVOL0 = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0 = 0.75, "W", 126, 20, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136"]

L_HEAD, BDRAWS, SEED_BASE, Q_HEAD = 63, 500, 11641164, 0.90

# ----------------------------------------------------------------- THE DIALS (param 2 of 2)
LAD = {
    "D_GROSS":   [round(0.20 + 0.025 * i, 3) for i in range(33)],   # 1150/1154's ladder, verbatim
    "D_N":       [3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50],
    "D_HOLD":    [5, 10, 21, 42, 63, 90, 126, 189, 252],
    "D_CADENCE": ["D", "W", "2W", "M", "2M", "Q"],
    "D_MAXVOL":  [0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 2.00],
}
DIALS = list(LAD)
DIAL_KW = {"D_GROSS": "gross", "D_N": "N", "D_HOLD": "H", "D_CADENCE": "freq", "D_MAXVOL": "maxvol"}

# -------------------------------------------------------------- THE SWAPPED LEG (param 1 of 2)
# Every chooser is min(M_S, M_<LEG>, M_CAGR) over the dial, IS-WINDOW ONLY, argmax.  M_S and
# M_CAGR are 1154's verbatim and never move; only the third leg is swapped.
#   form "cap"  -> M = (mult * spy - book) / (mult * spy)     (lower book is better)
#   form "beat" -> M = (book - spy) / |spy|                   (higher book is better)
SWAP = {
    "L_DD":     dict(form="cap",  stat="ADD",   mult=0.60, degree="EXPOSURE (declared degree 1)"),
    "L_VOLTGT": dict(form="cap",  stat="VOL",   mult=1.00, degree="EXPOSURE (declared degree 1)"),
    "L_TUW":    dict(form="cap",  stat="TUW",   mult=1.00, degree="NON-EXPOSURE (declared degree 0)"),
    "L_ULCER":  dict(form="beat", stat="UPI",   mult=None, degree="NON-EXPOSURE (declared degree 0)"),
}
SWAPS = list(SWAP)
MULTS = [0.60, 0.80, 1.00, 1.25]        # sensitivity annex only; primary per leg above

# the four single-statistic choosers 1150/1154 published, kept ONLY to re-verify their picks (G8)
SINGLE = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD", "C_ISMAR"]

# ------------------------------------------------------------------ committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)      # U56 W/H126/N=20, 10 bps
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1150_PICKS = {("C_ISSHARPE", "U56"): 1.000, ("C_ISSHARPE", "B136"): 1.000,
               ("C_ISCAGR", "U56"): 1.000, ("C_ISCAGR", "B136"): 1.000,
               ("C_ISDD", "U56"): 0.200, ("C_ISDD", "B136"): 0.200,
               ("C_ISMAR", "U56"): 1.000, ("C_ISMAR", "B136"): 1.000}
A1154_IS4B_PICKS = {"U56": 0.625, "B136": 0.575}                       # the TENT's own pick
A1154_U56_ENDS = dict(M_S=(0.2353, 0.2377), M_DD=(0.7127, -0.3903),    # gross 0.20 -> 1.00
                      M_CAGR=(-0.6485, 0.7738))

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- 1082/1098/1150/1154's fast runner, verbatim
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


# ---------------------------------------------------------------- THE SIX STATISTICS, DECLARED
def stats6(r):
    """CAGR, Sharpe, MaxDD (signed), |ulcer index|, time-under-water share, ann. vol.

    ULCER INDEX  = sqrt(mean(dd_t^2)) over the window, dd_t = eq_t / running_max - 1.
    UPI          = CAGR / ulcer  (an Ulcer RATIO: a degree-1 numerator over a degree-1
                   denominator, so scale-free by construction — that is the point).
    TUW          = share of days strictly below the running maximum.  Scale-free: multiplying
                   every return by g > 0 leaves the sign of log eq_t - max log eq_s unchanged
                   to first order, so the underwater PATTERN barely moves (G12 measures it).
    """
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1.0
    vol = r.std(ddof=1) * np.sqrt(252.0)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    ulc = float(np.sqrt(np.mean(dd ** 2)))
    return dict(CAGR=cagr, Sharpe=((r.mean() * 252.0) / vol if vol else np.nan),
                MaxDD=float(dd.min()), ADD=float(abs(dd.min())), ULC=ulc,
                UPI=(cagr / ulc if ulc > 0 else np.nan),
                TUW=float((dd < 0).mean()), VOL=float(vol))


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def allm(r, warm, ins, oos):
    """1154's blocks_m plus the three new statistics on each window."""
    rr = r[warm]
    f, i, o = stats6(rr), stats6(r[ins]), stats6(r[oos])
    h = len(rr) // 2
    m = dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
             H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]))
    for k, v in i.items():
        m["IS_" + k] = v
    for k, v in o.items():
        m["OOS_" + k] = v
    for k in ("ULC", "UPI", "TUW", "VOL", "ADD"):
        m[k] = f[k]
    return m


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, above.values, vol20.values


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


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def cadence_mask(idx, spec):
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


# ------------------------------------------------------------------- 4b / 4a, 1154's verbatim
def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# ----------------------------------------------------- THE IS-ONLY MARGINS (the swapped leg)
def m_s(b, sb):
    return (b["IS_Sharpe"] - sb["IS_Sharpe"]) / abs(sb["IS_Sharpe"])


def m_cagr(b, sb):
    flo = CAGR_FLOOR * sb["IS_CAGR"]
    return (b["IS_CAGR"] - flo) / abs(flo)


def m_swap(leg, b, sb, mult=None):
    sp = SWAP[leg]
    st = sp["stat"]
    if sp["form"] == "cap":
        cap = (sp["mult"] if mult is None else mult) * sb["IS_" + st]
        return (cap - b["IS_" + st]) / cap
    return (b["IS_" + st] - sb["IS_" + st]) / abs(sb["IS_" + st])


def min_stat(leg, b, sb, mult=None):
    return min(m_s(b, sb), m_swap(leg, b, sb, mult), m_cagr(b, sb))


def binding_of(leg, b, sb, mult=None):
    v = {"M_S": m_s(b, sb), "M_SWAP": m_swap(leg, b, sb, mult), "M_CAGR": m_cagr(b, sb)}
    return min(v, key=v.get)


def stat_single(ch, m):
    if ch == "C_ISSHARPE":
        return m["IS_Sharpe"]
    if ch == "C_ISCAGR":
        return m["IS_CAGR"]
    if ch == "C_ISDD":
        return -abs(m["IS_MaxDD"])
    if ch == "C_ISMAR":
        return m["IS_CAGR"] / abs(m["IS_MaxDD"]) if m["IS_MaxDD"] else np.nan
    raise KeyError(ch)


# ---------------------------------------------------------------- SHAPE, DECLARED BEFORE ANY NUMBER
def mono_of(v):
    d = np.diff(np.asarray(v, float))
    d = d[np.isfinite(d)]
    if len(d) == 0:
        return dict(mono=False, direction="none", mono_score=np.nan, rho=np.nan)
    up, dn = bool((d >= 0).all()), bool((d <= 0).all())
    x = np.arange(len(v), dtype=float)
    ok = np.isfinite(np.asarray(v, float))
    rho = np.nan
    if ok.sum() > 2:
        a = pd.Series(np.asarray(v, float)[ok]).rank().values
        bb = pd.Series(x[ok]).rank().values
        rho = float(np.corrcoef(a, bb)[0, 1])
    return dict(mono=bool(up or dn),
                direction=("up" if up and not dn else "down" if dn and not up else
                           "flat" if up and dn else "none"),
                mono_score=max(float((d > 0).mean()), float((d < 0).mean())), rho=rho)


def degree_slope(rungs, vals):
    """OLS slope of log|val| on log(rung) — the homogeneity degree of a statistic in gross."""
    x = np.log(np.asarray(rungs, float))
    y = np.asarray(vals, float)
    ok = np.isfinite(y) & (np.abs(y) > 0) & np.isfinite(x)
    if ok.sum() < 3:
        return np.nan
    return float(np.polyfit(x[ok], np.log(np.abs(y[ok])), 1)[0])


def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L)


def boot_all(R, idx, chunk=40):
    """Per block-bootstrap draw (PAIRED index): CAGR, Sharpe, |MaxDD|, ulcer, TUW, vol."""
    nd, TL = idx.shape
    out = np.empty((nd, 6))
    for a in range(0, nd, chunk):
        b = min(a + chunk, nd)
        X = R[idx[a:b]]
        eq = np.cumprod(1.0 + X, axis=1)
        pk = np.maximum.accumulate(eq, axis=1)
        dd = eq / pk - 1.0
        vol = X.std(axis=1, ddof=1) * np.sqrt(252.0)
        out[a:b, 0] = eq[:, -1] ** (252.0 / TL) - 1.0
        out[a:b, 1] = (X.mean(axis=1) * 252.0) / vol
        out[a:b, 2] = np.abs(dd.min(axis=1))
        out[a:b, 3] = np.sqrt((dd ** 2).mean(axis=1))
        out[a:b, 4] = (dd < 0).mean(axis=1)
        out[a:b, 5] = vol
    return out


def boot_min_vec(leg, bs, sb):
    """The chooser's min statistic on a bootstrap draw matrix (same formulae, same constants)."""
    cagr, sh, add, ulc, tuw, vol = (bs[:, i] for i in range(6))
    flo = CAGR_FLOOR * sb["IS_CAGR"]
    ms = (sh - sb["IS_Sharpe"]) / abs(sb["IS_Sharpe"])
    mc = (cagr - flo) / abs(flo)
    sp = SWAP[leg]
    if sp["form"] == "cap":
        book = {"ADD": add, "VOL": vol, "TUW": tuw}[sp["stat"]]
        cap = sp["mult"] * sb["IS_" + sp["stat"]]
        msw = (cap - book) / cap
    else:
        upi = cagr / np.maximum(ulc, 1e-12)
        msw = (upi - sb["IS_UPI"]) / abs(sb["IS_UPI"])
    return np.minimum.reduce([ms, msw, mc])


def main():
    t0 = time.time()
    P(f"# Idea 1166 (lane C, {DATE}) — does the TENT survive when the DRAWDOWN LEG is replaced")
    P("#   by a NON-EXPOSURE one?   (claimed as queue 1163; renumbered 1164 then 1166, defect 932)")
    P("#")
    P("# 1154: C_IS4B = argmax over a dial of min(M_S, M_DD, M_CAGR) is the ONE chooser that")
    P("#   reaches the gross INTERIOR (0.625 U56 / 0.575 B136), and its mechanism is that M_DD")
    P("#   and M_CAGR are monotone in OPPOSITE directions in gross — two EXPOSURE legs — so the")
    P("#   MIN is a TENT.  This run swaps the third leg and keeps M_S and M_CAGR fixed.")
    P("#")
    P(f"# TUNED PARAMETERS (2, PROTOCOL rule 4, the two the queue names): LEG {SWAPS}")
    P(f"#   x DIAL {DIALS} = {len(SWAPS) * len(DIALS)} cells per panel, "
      f"{len(SWAPS) * len(DIALS) * len(PANELS)} in all, EVERY ONE PUBLISHED.")
    P("#   The RUNG is NOT a third parameter: it is the object the chooser selects, and all")
    P(f"#   {sum(len(v) for v in LAD.values())} rungs per panel are published in .grid.csv regardless.")
    P("#   PANEL {U56, B136} is NOT a dial (both reported everywhere, nothing selected on the pair).")
    P("#")
    P("# THE LEGS, WITH THEIR PRE-DECLARED HOMOGENEITY DEGREE (measured later, not assumed):")
    for lg in SWAPS:
        sp = SWAP[lg]
        P(f"#   {lg:<9s} form {sp['form']:<4s} stat {sp['stat']:<4s} "
          f"primary mult {str(sp['mult']):<5s} {sp['degree']}")
    P("# THE CAP MULTIPLIER IS NOT A THIRD PARAMETER: (mult*spy - book)/(mult*spy) is a POSITIVE")
    P("#   AFFINE transform of -book, so each leg's monotonicity/direction/rho over any ladder is")
    P("#   EXACTLY multiplier-invariant (G11).  It can only move where the legs CROSS, so all")
    P(f"#   {len(MULTS)} multipliers {MULTS} are published in .mult.csv and the VERDICT is read at the")
    P("#   pre-declared primary (0.60 for L_DD = 4b's own constant, 1.00 for L_VOLTGT / L_TUW).")
    P("#")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL0}, min hold {HOLD0}, N {N0},")
    P(f"#   gross {GROSS0}, cadence {FREQ0}, cost {COST0} bps (rule 2), LAG {LAG}, warm-up {WARMUP},")
    P(f"#   IS end {IS_END}, zero cash, block L={L_HEAD}, {BDRAWS} draws, crc32 seeds, q={Q_HEAD}.")
    P(f"# PRICE VINTAGE PINNED at {PIN} (idea 1159/1163's restatement defect); G2/G3 BOTH ways.")
    P("#")
    P("# LADDERS, canonical order declared here and never re-chosen:")
    for k in DIALS:
        P(f"#   {k:<10s} {len(LAD[k]):2d} rungs  {LAD[k]}")
    P("#")
    P("# SHAPE TAXONOMY, DECLARED BEFORE ANY NUMBER (the three ways a min can look):")
    P("#   TENT  — the BINDING (arg-min) leg CHANGES across the ladder AND the min sequence is")
    P("#           NON-MONOTONE AND the argmax is INTERIOR.  This is 1154's object.")
    P("#   RAMP  — the min sequence is MONOTONE; its argmax is then an endpoint BY IDENTITY (G9).")
    P("#   FLAT  — the min's whole-ladder spread is under ONE paired block-bootstrap SD, i.e. the")
    P("#           argmax is a noise pick whatever its position.  Reported alongside, because a")
    P("#           degenerate leg can produce an interior pick WITHOUT a tent and must not be")
    P("#           allowed to read as one.")
    P("#   DEGREE(stat) — OLS slope of log|stat| on log(gross) over D_GROSS.  An EXPOSURE object")
    P("#           has slope ~1, a scale-free one ~0.  G12 measures the same slopes on an EXACTLY")
    P("#           SCALED synthetic book so the machinery is validated before it is believed.")
    P("#")
    P("# HYPOTHESES, DECLARED BEFORE ANY NUMBER:")
    P("#   H_DEGREE     the declared degrees are the MEASURED ones on D_GROSS, both panels:")
    P("#                slope >= 0.5 for |MaxDD|, VOL, ULC, CAGR and |slope| <= 0.25 for Sharpe,")
    P("#                UPI, TUW.  If this fails the whole exposure/non-exposure split is wrong")
    P("#                and nothing below can be read.")
    P("#   H_TENTLIVES  swapping in the OTHER exposure leg (L_VOLTGT) KEEPS the tent: on D_GROSS,")
    P("#                non-monotone AND interior pick AND binding leg changes, on BOTH panels.")
    P("#   H_TENTDIES   swapping in a NON-exposure leg (L_TUW, L_ULCER) KILLS it: on D_GROSS the")
    P("#                min becomes MONOTONE and the pick lands on an ENDPOINT, on BOTH panels.")
    P("#   H_PAIRONLY   over all 40 cells, TENT shape occurs ONLY where the swapped leg is an")
    P("#                exposure object, i.e. no L_TUW / L_ULCER cell on ANY dial is a TENT.")
    P("#                (Stronger than H_TENTDIES: it is about the pair, not about gross.)")
    P("#   H_PICKPAY    the interior picks that survive still clear 4b FULL and OOS at least as")
    P("#                often as their ladder's own base rate — i.e. the tent was buying")
    P("#                something and not just sitting in the middle.")
    P("#   H_NOPAY4a    4a is 0 of every cell and every pick, as at 1150's 528, 1154's 132 and")
    P("#                1161's 66.  A single 4a pass would be the headline instead.")
    P("#   H_PEAKRESOLVED  *** POST-HOC, ADDED AFTER THE FIRST RUN AND LABELLED AS SUCH ***.  The")
    P("#                pre-declared FLAT test compares the min's WHOLE-LADDER spread with one paired")
    P("#                SD, and the first run showed that test is too weak: where the swapped leg is")
    P("#                near-constant the min is a RAMP-then-PLATEAU whose spread is carried entirely")
    P("#                by the ramp, so a peak sitting on a dead-flat plateau still reads 7 SD.  The")
    P("#                sharper object is the peak's height over EACH endpoint separately:")
    P("#                need_lo = v[pick]-v[0], need_hi = v[pick]-v[R-1], each against the PAIRED")
    P("#                block-bootstrap SD of that very difference.  A RESOLVED tent needs BOTH over")
    P("#                one SD.  Bar: resolved only where the swapped leg is an EXPOSURE object.")
    P("#                The pre-registered verdicts above are published UNCHANGED regardless.")
    P("# DECISION RULE, declared before any number: the queue's question is ANSWERED 'NO, THE TENT")
    P("#   IS AN EXPOSURE-PAIR OBJECT AND DIES WITH THE SECOND EXPOSURE LEG' iff H_DEGREE holds")
    P("#   AND H_TENTLIVES holds AND H_TENTDIES holds.  It is ANSWERED 'YES, THE TENT SURVIVES AND")
    P("#   1154's MECHANISM READING IS WRONG' if a NON-exposure leg still gives a non-monotone min")
    P("#   with an interior pick that is not FLAT.  A mixed reading is published as mixed.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  {name:<4s} {what:<64s} {value:.2e}   {'PASS' if ok else 'FAIL'}")

    P("## PANELS — loaded, PINNED and stamped before any result number")
    panels, raw_unpinned = {}, {}
    for panel in PANELS:
        pxu = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        raw_unpinned[panel] = pxu
        px = pxu.loc[:PIN]
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, above, vol20 = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20)
        P(f"  {panel:<5s} {len(px.columns):4d} names, PINNED {len(idx):,} rows "
          f"{idx[0].date()} -> {idx[-1].date()} (unpinned ends {pxu.index[-1].date()}), "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")
    P("")

    def run_cell(panel, gross=GROSS0, N=N0, H=HOLD0, freq=FREQ0, maxvol=MAXVOL0, d=None):
        d = d or panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        el = d["above"] & (d["vol20"] < maxvol)
        W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        return nrun(d["rets"], Wl, mkl)

    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["above"] & (d["vol20"] < MAXVOL0), d["priced"], np.flatnonzero(mk),
              N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST0, freq=FREQ0)["returns"].values
    gr, tn = run_cell("U56")
    rfast = gr - tn * COST0 / 1e4
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest", g1, g1 < 1e-12)

    m = allm(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", f"committed U56 W/H126/N=20 triple, PINNED at {PIN}", g2, g2 < 5e-5)
    P(f"       ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%}) vs committed "
      f"({A936_WH126[0]:.4%} / {A936_WH126[1]:.4f} / {A936_WH126[2]:.4%})")

    pxu = raw_unpinned["U56"]
    scu, abu, vlu = mech(pxu)
    wu, iu, ou = windows(pxu.index)
    du = dict(idx=pxu.index, K=len(pxu.columns), T=len(pxu.index),
              rets=pxu.pct_change().fillna(0.0).values, priced=pxu.notna().values,
              sc=scu, above=abu, vol20=vlu, warm=wu, ins=iu, oos=ou)
    gru, tnu = run_cell("U56", d=du)
    mu = allm(gru - tnu * COST0 / 1e4, wu, iu, ou)
    g2u = max(abs(mu["CAGR"] - A936_WH126[0]), abs(mu["Sharpe"] - A936_WH126[1]),
              abs(mu["MaxDD"] - A936_WH126[2]))
    P(f"       THE VINTAGE, PUBLISHED NOT ABSORBED: the same gate UNPINNED reads {g2u:.2e} "
      f"({g2u / max(g2, 1e-18):.1f}x the pinned reading).")
    gaterows.append(dict(gate="G2u", what="same gate on the UNPINNED file (reported, not gated)",
                         value=float(g2u), pass_=bool(g2u < 5e-5)))

    spy_m, live_m = {}, {}
    for panel in PANELS:
        dp = panels[panel]
        spy_m[panel] = allm(dp["px"]["SPY"].pct_change().fillna(0.0).values,
                            dp["warm"], dp["ins"], dp["oos"])
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST0, freq="W")["returns"].values
        live_m[panel] = allm(lr, dp["warm"], dp["ins"], dp["oos"])
    g3 = max(abs(spy_m["U56"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["U56"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", f"SPY OOS triple, PINNED at {PIN}", g3, g3 < 5e-4)

    g12r, t12r = run_cell("U56", N=12)
    m12 = allm(g12r - t12r * COST0 / 1e4, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gate("G4", "CROSS-RUN 1098/1102's committed U56 n=12 triple", g4, g4 < 5e-4)

    g5 = abs(live_m["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G5", "live RULES v2 MaxDD == committed -12.05%", g5, g5 < 5e-4)

    g12b, _ = run_cell("U56", N=12)
    g6 = float(np.abs(g12r - g12b).max())
    gate("G6", "determinism (same cell twice)", g6, g6 == 0.0)

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int)
                        - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gate("G7", "cadence_mask == engine.rebalance_mask (D/W/M/Q)", float(g7), g7 == 0)

    # ---------------------------------------------------------------- THE GRID (every rung)
    P("")
    P("## THE GRID — every rung of every dial on both panels, published whatever a chooser did")
    rows, streams = [], {}
    for panel in PANELS:
        dp = panels[panel]
        sb, lbm = spy_m[panel], live_m[panel]
        for dial in DIALS:
            for j, rung in enumerate(LAD[dial]):
                kw = dict(gross=GROSS0, N=N0, H=HOLD0, freq=FREQ0, maxvol=MAXVOL0)
                kw[DIAL_KW[dial]] = rung
                g, t = run_cell(panel, **kw)
                r = g - t * COST0 / 1e4
                mm = allm(r, dp["warm"], dp["ins"], dp["oos"])
                streams[(panel, dial, j)] = r
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm)
                row = dict(panel=panel, dial=dial, rung_i=j, rung=str(rung), n_rungs=len(LAD[dial]),
                           turn_per_yr=float(t[dp["warm"]].sum() / (dp["warm"].sum() / 252.0)),
                           **{k: float(v) for k, v in mm.items()},
                           M_S=float(m_s(mm, sb)), M_CAGR=float(m_cagr(mm, sb)),
                           **{k: bool(v) for k, v in l4b.items()},
                           **{k: bool(v) for k, v in l4bo.items()},
                           **{k: bool(v) for k, v in l4a.items()},
                           pass_4b=bool(all(l4b.values())), pass_4b_oos=bool(all(l4bo.values())),
                           pass_4a=bool(all(l4a.values())))
                for lg in SWAPS:
                    row[f"M_{lg}"] = float(m_swap(lg, mm, sb))
                    row[f"S_{lg}"] = float(min_stat(lg, mm, sb))
                    row[f"B_{lg}"] = binding_of(lg, mm, sb)
                for ch in SINGLE:
                    row[f"S_{ch}"] = float(stat_single(ch, mm))
                rows.append(row)
        P(f"  {panel}: {sum(len(LAD[x]) for x in DIALS)} rungs run  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(rows)
    dump(grid, "grid")

    # G8 — CROSS-RUN: 1150's four single-statistic picks AND 1154's C_IS4B tent pick
    g8bad = 0
    for (ch, panel), want in A1150_PICKS.items():
        sub = grid[(grid.panel == panel) & (grid.dial == "D_GROSS")].sort_values("rung_i")
        got = float(sub.iloc[int(np.nanargmax(sub[f"S_{ch}"].values))]["rung"])
        if abs(got - want) > 1e-9:
            g8bad += 1
            P(f"       G8 mismatch: {ch} on {panel} picks {got} not 1150's {want}")
    for panel, want in A1154_IS4B_PICKS.items():
        sub = grid[(grid.panel == panel) & (grid.dial == "D_GROSS")].sort_values("rung_i")
        got = float(sub.iloc[int(np.nanargmax(sub["S_L_DD"].values))]["rung"])
        P(f"       CONTROL: min(M_S, M_DD, M_CAGR) on {panel} D_GROSS picks {got} "
          f"(1154 committed {want})")
        if abs(got - want) > 1e-9:
            g8bad += 1
    gate("G8", "CROSS-RUN 1150's 8 single picks + 1154's 2 tent picks", float(g8bad), g8bad == 0)

    # G8b — 1154's committed U56 margin endpoints (the mechanism itself, not a pick)
    su = grid[(grid.panel == "U56") & (grid.dial == "D_GROSS")].sort_values("rung_i")
    ends = dict(M_S=(float(su.M_S.values[0]), float(su.M_S.values[-1])),
                M_DD=(float(su.M_L_DD.values[0]), float(su.M_L_DD.values[-1])),
                M_CAGR=(float(su.M_CAGR.values[0]), float(su.M_CAGR.values[-1])))
    g8b = max(max(abs(ends[k][i] - A1154_U56_ENDS[k][i]) for i in (0, 1)) for k in ends)
    gate("G8b", "CROSS-RUN 1154's committed U56 margin endpoints (gross 0.20 -> 1.00)", g8b, g8b < 5e-3)
    for k in ends:
        P(f"       {k:<7s} {ends[k][0]:+.4f} -> {ends[k][1]:+.4f}   "
          f"(1154: {A1154_U56_ENDS[k][0]:+.4f} -> {A1154_U56_ENDS[k][1]:+.4f})")

    # G9 — THE ALGEBRA, on synthetics, so the run cannot be read as having discovered it
    rng = np.random.default_rng(seed_of("identity"))
    bad_ramp = bad_uni = n_int = n_draw = 0
    for _ in range(20000):
        R = int(rng.integers(5, 34))
        a = np.sort(rng.normal(size=R))                      # increasing
        b = -np.sort(rng.normal(size=R))                     # decreasing
        flat = np.full(R, 10.0)
        if int(np.argmax(np.minimum(a, flat))) not in (0, R - 1):
            bad_ramp += 1                                    # min(mono, flat) is mono => endpoint
        mn = np.minimum(a - a.mean(), b - b.mean())           # two OPPOSED monotone legs
        dd_ = np.diff(mn)
        pos = np.flatnonzero(dd_ > 0)
        neg = np.flatnonzero(dd_ < 0)
        if len(pos) and len(neg) and pos.max() > neg.min():
            bad_uni += 1                                     # not "up then down" => not unimodal
        n_draw += 1
        n_int += int(int(np.argmax(mn)) not in (0, R - 1))
    gate("G9", "ALGEBRA: min(mono, flat) is mono -> endpoint, 20,000 synthetic", float(bad_ramp), bad_ramp == 0)
    gate("G9b", "ALGEBRA: min of two OPPOSED monos is UNIMODAL (up then down)", float(bad_uni), bad_uni == 0)
    P(f"       and its argmax is INTERIOR in {n_int:,} of {n_draw:,} synthetic draws "
      f"({n_int / n_draw:.1%}).")
    if n_int < n_draw:
        P("       The remainder are pairs whose crossing falls in the FIRST or LAST interval, which")
        P("       is exactly the degenerate case 1161 found on its shortest rolling windows.")

    # G10 — the ladders nest the record's committed rungs
    nest = (all(abs(x - y) < 1e-9 for x, y in
                zip([r for r in LAD["D_GROSS"] if abs(r * 20 - round(r * 20)) < 1e-9],
                    [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75,
                     0.80, 0.85, 0.90, 0.95, 1.00]))
            and N0 in LAD["D_N"] and 12 in LAD["D_N"] and HOLD0 in LAD["D_HOLD"]
            and FREQ0 in LAD["D_CADENCE"] and "M" in LAD["D_CADENCE"] and MAXVOL0 in LAD["D_MAXVOL"])
    gate("G10", "ladders NEST the record's committed rungs", float(nest), nest)

    # G11 — the multiplier is an AFFINE reparametrisation: per-leg rho is EXACTLY invariant
    worst = 0.0
    for panel in PANELS:
        dp = panels[panel]
        sb = spy_m[panel]
        sub = grid[(grid.panel == panel) & (grid.dial == "D_GROSS")].sort_values("rung_i")
        for lg in [x for x in SWAPS if SWAP[x]["form"] == "cap"]:
            base = mono_of(sub[f"M_{lg}"].values)
            for mult in MULTS:
                v = [m_swap(lg, dict(("IS_" + k, sub.iloc[i]["IS_" + k]) for k in
                                     ("ADD", "VOL", "TUW", "UPI", "Sharpe", "CAGR")), sb, mult)
                     for i in range(len(sub))]
                mo = mono_of(v)
                worst = max(worst, abs((mo["rho"] or 0) - (base["rho"] or 0)),
                            float(mo["mono"] != base["mono"]))
    gate("G11", "cap multiplier is AFFINE: per-leg rho/mono invariant over 4 multipliers",
         worst, worst < 1e-12)

    # G12 — THE DEGREE MACHINERY, validated on an EXACTLY SCALED book before it is believed
    base_r = streams[("U56", "D_GROSS", len(LAD["D_GROSS"]) - 1)][panels["U56"]["ins"]]
    scales = np.array(LAD["D_GROSS"]) / LAD["D_GROSS"][-1]
    syn = {k: [] for k in ("ADD", "VOL", "ULC", "CAGR", "Sharpe", "UPI", "TUW")}
    for sc_ in scales:
        s6 = stats6(base_r * sc_)
        for k in syn:
            syn[k].append(s6[k])
    synslope = {k: degree_slope(LAD["D_GROSS"], syn[k]) for k in syn}
    want1 = ("ADD", "VOL", "ULC", "CAGR")
    want0 = ("Sharpe", "UPI", "TUW")
    g12 = max(max(abs(synslope[k] - 1.0) for k in want1), max(abs(synslope[k]) for k in want0))
    gate("G12", "DEGREE machinery on an EXACTLY SCALED book: deg-1 ~1, deg-0 ~0 (tol 0.15)", g12, g12 < 0.15)
    P("       synthetic slopes: " + "  ".join(f"{k} {synslope[k]:+.3f}" for k in syn))
    P(f"  GATES {sum(gates.values())} of {len(gates)} PASS")

    # ------------------------------------------------------- THE MEASURED DEGREES (mechanism)
    P("")
    P("## THE MEASURED HOMOGENEITY DEGREES ON D_GROSS — is each leg an EXPOSURE object?")
    degrows = []
    STATS = [("IS_ADD", "|MaxDD|", 1), ("IS_VOL", "vol", 1), ("IS_ULC", "ulcer", 1),
             ("IS_CAGR", "CAGR", 1), ("IS_Sharpe", "Sharpe", 0), ("IS_UPI", "UPI", 0),
             ("IS_TUW", "TUW", 0)]
    for panel in PANELS:
        sub = grid[(grid.panel == panel) & (grid.dial == "D_GROSS")].sort_values("rung_i")
        for col, nm, want in STATS:
            sl = degree_slope([float(x) for x in sub.rung], sub[col].values)
            ok = (sl >= 0.5) if want == 1 else (abs(sl) <= 0.25)
            degrows.append(dict(panel=panel, stat=nm, column=col, declared_degree=want,
                                measured_slope=sl, matches_declared=bool(ok),
                                lo=float(sub[col].values[0]), hi=float(sub[col].values[-1])))
            P(f"  {panel:<5s} {nm:<8s} declared degree {want}  measured slope {sl:+.4f}  "
              f"{'OK' if ok else 'MISMATCH':<8s} ({sub[col].values[0]:.4g} -> {sub[col].values[-1]:.4g})")
    deg = pd.DataFrame(degrows)
    dump(deg, "degree")
    h_degree = bool(deg.matches_declared.all())
    P(f"  -> H_DEGREE {'HOLDS' if h_degree else 'FAILS'}: {int(deg.matches_declared.sum())} "
      f"of {len(deg)} (panel, stat) slopes match their declared degree.")

    # ------------------------------------------------- SHAPES, PICKS, RULE 8 (40 cells)
    P("")
    P(f"## SHAPES AND PICKS — {len(SWAPS)} legs x {len(DIALS)} dials x {len(PANELS)} panels = "
      f"{len(SWAPS) * len(DIALS) * len(PANELS)} cells, every one published")
    shaperows, pickrows, wfrows, multrows = [], [], [], []
    for panel in PANELS:
        dp = panels[panel]
        sb, lbm = spy_m[panel], live_m[panel]
        rngb = np.random.default_rng(seed_of("boot", panel))
        bidx = block_index(rngb, int(dp["ins"].sum()), L_HEAD, BDRAWS)
        bcache = {}

        def bs_of(dial_, j_):
            if (dial_, j_) not in bcache:
                bcache[(dial_, j_)] = boot_all(streams[(panel, dial_, j_)][dp["ins"]], bidx)
            return bcache[(dial_, j_)]
        for dial in DIALS:
            sub = grid[(grid.panel == panel) & (grid.dial == dial)].sort_values("rung_i").reset_index(drop=True)
            R = len(sub)
            for lg in SWAPS:
                v = sub[f"S_{lg}"].values.astype(float)
                mo = mono_of(v)
                k = int(np.nanargmax(v))
                endpoint = k in (0, R - 1)
                bind = list(sub[f"B_{lg}"].values)
                n_bind = len(set(bind))
                spread = float(np.nanmax(v) - np.nanmin(v))
                # paired block-bootstrap SD of (argmax arm - argmin arm) in the chooser's units
                kmin = int(np.nanargmin(v))
                sd = np.nan
                dk = boot_min_vec(lg, bs_of(dial, k), sb)
                if kmin != k:
                    db = boot_min_vec(lg, bs_of(dial, kmin), sb)
                    sd = float(np.nanstd(dk - db, ddof=1))
                flat = bool(np.isfinite(sd) and spread < sd)
                tent = bool((not mo["mono"]) and (not endpoint) and n_bind > 1)
                # ---- POST-HOC: the peak's height over EACH endpoint, in paired SDs
                need = {}
                for tag, j_ in (("lo", 0), ("hi", R - 1)):
                    nd_ = float(v[k] - v[j_])
                    sd_ = 0.0 if j_ == k else float(np.nanstd(
                        dk - boot_min_vec(lg, bs_of(dial, j_), sb), ddof=1))
                    need[tag] = (nd_, sd_, bool(j_ != k and np.isfinite(sd_) and sd_ > 0 and nd_ > sd_))
                tent_resolved = bool(tent and need["lo"][2] and need["hi"][2])
                # ---- the plateau: where the SWAPPED leg binds, and how far it tilts there
                pl = [i for i in range(R) if bind[i] == "M_SWAP"]
                swv = sub[f"M_{lg}"].values.astype(float)
                tilt = float(swv[pl[-1]] - swv[pl[0]]) if len(pl) > 1 else np.nan
                ramp = float(v[k] - v[0])
                shp = "TENT" if tent else ("RAMP" if mo["mono"] else
                                           ("FLAT" if flat else "OTHER-NONMONO"))
                pr = sub.iloc[k]
                shaperows.append(dict(panel=panel, dial=dial, leg=lg, n_rungs=R,
                                      shape_class=shp, tent=tent, mono=mo["mono"],
                                      direction=mo["direction"], mono_score=mo["mono_score"],
                                      rho=mo["rho"], pick=str(pr.rung), pick_i=k,
                                      endpoint=endpoint, n_binding_legs=n_bind,
                                      binding_at_pick=str(pr[f"B_{lg}"]),
                                      binding_first=bind[0], binding_last=bind[-1],
                                      spread=spread, paired_SD=sd,
                                      spread_over_SD=(spread / sd if sd else np.nan), flat=flat,
                                      need_lo=need["lo"][0], SD_lo=need["lo"][1],
                                      lo_over_SD=(need["lo"][0] / need["lo"][1] if need["lo"][1] else np.nan),
                                      need_hi=need["hi"][0], SD_hi=need["hi"][1],
                                      hi_over_SD=(need["hi"][0] / need["hi"][1] if need["hi"][1] else np.nan),
                                      resolved_lo=need["lo"][2], resolved_hi=need["hi"][2],
                                      tent_resolved=tent_resolved, plateau_rungs=len(pl),
                                      plateau_tilt=tilt, ramp_rise=ramp))
                pickrows.append(dict(panel=panel, dial=dial, leg=lg, shape_class=shp,
                                     pick=str(pr.rung), pick_i=k, endpoint=endpoint,
                                     IS_Sharpe=pr.IS_Sharpe, IS_CAGR=pr.IS_CAGR, IS_MaxDD=pr.IS_MaxDD,
                                     CAGR=pr.CAGR, Sharpe=pr.Sharpe, MaxDD=pr.MaxDD, H1=pr.H1, H2=pr.H2,
                                     OOS_CAGR=pr.OOS_CAGR, OOS_Sharpe=pr.OOS_Sharpe,
                                     OOS_MaxDD=pr.OOS_MaxDD, turn_per_yr=pr.turn_per_yr,
                                     pass_4b=bool(pr.pass_4b), pass_4b_oos=bool(pr.pass_4b_oos),
                                     pass_4a=bool(pr.pass_4a),
                                     ladder_4b=int(sub.pass_4b.sum()),
                                     ladder_4b_both=int((sub.pass_4b & sub.pass_4b_oos).sum()),
                                     ladder_4a=int(sub.pass_4a.sum()), n_rungs=R))
                wfrows.append(dict(panel=panel, dial=dial, leg=lg, arm=f"PICK {pr.rung}",
                                   chosen_on=f"IS 2009-01..{IS_END} only", shape_class=shp,
                                   OOS_CAGR=pr.OOS_CAGR, OOS_Sharpe=pr.OOS_Sharpe,
                                   OOS_MaxDD=pr.OOS_MaxDD, full_CAGR=pr.CAGR, full_Sharpe=pr.Sharpe,
                                   full_MaxDD=pr.MaxDD, H1=pr.H1, H2=pr.H2,
                                   pass_4b=bool(pr.pass_4b), pass_4b_oos=bool(pr.pass_4b_oos),
                                   pass_4a=bool(pr.pass_4a)))
                # ---- the multiplier annex (published, verdict read at the primary only)
                if SWAP[lg]["form"] == "cap":
                    for mult in MULTS:
                        vv = np.array([min(m_s(sub.iloc[i], sb),
                                           m_swap(lg, sub.iloc[i], sb, mult),
                                           m_cagr(sub.iloc[i], sb)) for i in range(R)], float)
                        mo2 = mono_of(vv)
                        k2 = int(np.nanargmax(vv))
                        multrows.append(dict(panel=panel, dial=dial, leg=lg, mult=mult,
                                             primary=bool(abs(mult - SWAP[lg]["mult"]) < 1e-12),
                                             mono=mo2["mono"], direction=mo2["direction"],
                                             pick=str(sub.rung[k2]), pick_i=k2,
                                             endpoint=bool(k2 in (0, R - 1)),
                                             tent=bool((not mo2["mono"]) and k2 not in (0, R - 1))))
        P(f"  {panel}: {len(SWAPS) * len(DIALS)} cells scored  ({time.time() - t0:.0f}s)")

    shapes = pd.DataFrame(shaperows)
    picks = pd.DataFrame(pickrows)
    dump(shapes, "shapes")
    dump(picks, "picks")
    dump(pd.DataFrame(multrows), "mult")

    # ------------------------------------------------------------------------- THE ANSWER
    P("")
    P("## THE ANSWER")
    P("  D_GROSS, the queue's own cell — the min's shape leg by leg, both panels:")
    for panel in PANELS:
        for lg in SWAPS:
            r = shapes[(shapes.panel == panel) & (shapes.dial == "D_GROSS") & (shapes.leg == lg)].iloc[0]
            P(f"    {panel:<5s} {lg:<9s} {SWAP[lg]['degree'][:13]:<13s} shape {r['shape_class']:<13s} "
              f"mono {str(r.mono):<5s} dir {r.direction:<5s} rho {r.rho:+.3f}  pick {r['pick']:<6s} "
              f"{'ENDPOINT' if r.endpoint else 'INTERIOR':<8s} binding {r.binding_first}->{r.binding_last} "
              f"({r.n_binding_legs})  spread {r.spread:.4g} = {r.spread_over_SD:.2f} SD")
    gg = shapes[shapes.dial == "D_GROSS"]
    h_tentlives = bool(all(gg[(gg.panel == p) & (gg.leg == "L_VOLTGT")].tent.iloc[0] for p in PANELS))
    h_tentdies = bool(all(gg[(gg.panel == p) & (gg.leg == lg)].mono.iloc[0]
                          and gg[(gg.panel == p) & (gg.leg == lg)].endpoint.iloc[0]
                          for p in PANELS for lg in ("L_TUW", "L_ULCER")))
    P(f"  -> H_TENTLIVES {'HOLDS' if h_tentlives else 'FAILS'} (L_VOLTGT, the OTHER exposure leg, "
      f"is a TENT on both panels: {[bool(gg[(gg.panel == p) & (gg.leg == 'L_VOLTGT')].tent.iloc[0]) for p in PANELS]})")
    P(f"  -> H_TENTDIES  {'HOLDS' if h_tentdies else 'FAILS'} (L_TUW and L_ULCER monotone AND "
      f"endpoint on both panels)")
    nonexp_tents = shapes[(shapes.leg.isin(["L_TUW", "L_ULCER"])) & shapes.tent]
    h_paironly = bool(len(nonexp_tents) == 0)
    P(f"  -> H_PAIRONLY  {'HOLDS' if h_paironly else 'FAILS'}: TENT shape at "
      f"{int(shapes.tent.sum())} of {len(shapes)} cells overall, of which "
      f"{int(shapes[shapes.leg.isin(['L_DD', 'L_VOLTGT'])].tent.sum())} carry an EXPOSURE leg and "
      f"{len(nonexp_tents)} a NON-exposure one.")
    P("")
    P("  SHAPE BY LEG (all five dials, both panels):")
    for lg in SWAPS:
        s = shapes[shapes.leg == lg]
        P(f"    {lg:<9s} TENT {int(s.tent.sum())}/{len(s)}  RAMP {int((s.shape_class == 'RAMP').sum())}  "
          f"FLAT {int((s.shape_class == 'FLAT').sum())}  OTHER {int((s.shape_class == 'OTHER-NONMONO').sum())}  "
          f"interior picks {int((~s.endpoint).sum())}/{len(s)}")
    P("  SHAPE BY DIAL:")
    for dial in DIALS:
        s = shapes[shapes.dial == dial]
        P(f"    {dial:<10s} TENT {int(s.tent.sum())}/{len(s)}  interior picks "
          f"{int((~s.endpoint).sum())}/{len(s)}  median binding-leg count {s.n_binding_legs.median():.1f}")
    if len(nonexp_tents):
        P("  EVERY NON-EXPOSURE TENT, named (these are what would REFUTE 1154's mechanism):")
        for _, r in nonexp_tents.iterrows():
            P(f"    {r.panel:<5s} {r.dial:<10s} {r.leg:<9s} pick {r['pick']} "
              f"spread {r.spread:.4g} = {r.spread_over_SD:.2f} SD  flat {r.flat}")
    P("")
    P("  THE MULTIPLIER ANNEX (not a tuned parameter; verdict read at the primary row only):")
    mu_df = pd.DataFrame(multrows)
    for lg in [x for x in SWAPS if SWAP[x]["form"] == "cap"]:
        s = mu_df[(mu_df.leg == lg) & (mu_df.dial == "D_GROSS")]
        for panel in PANELS:
            ss = s[s.panel == panel]
            P(f"    {panel:<5s} {lg:<9s} picks over mult {MULTS}: "
              f"{list(ss.sort_values('mult')['pick'])}  tent {list(ss.sort_values('mult').tent)}")

    # ------------------------------------- POST-HOC: IS THE PEAK RESOLVABLE AT ALL?
    P("")
    P("## *** POST-HOC (added after the first run, labelled, pre-registered verdicts unchanged) ***")
    P("## IS THE PEAK RESOLVABLE? — the peak's height over EACH endpoint in paired bootstrap SDs")
    P("   The first run made the pre-declared FLAT test look useless: it compares the min's")
    P("   WHOLE-LADDER spread with one SD, and where the swapped leg is near-constant the min is a")
    P("   RAMP-then-PLATEAU whose spread is ALL ramp, so a peak on a dead-flat plateau reads 7 SD.")
    P("   need_lo = v[pick]-v[0] (the ramp side), need_hi = v[pick]-v[R-1] (the plateau side).")
    for panel in PANELS:
        for lg in SWAPS:
            r = shapes[(shapes.panel == panel) & (shapes.dial == "D_GROSS") & (shapes.leg == lg)].iloc[0]
            P(f"    {panel:<5s} {lg:<9s} pick {r['pick']:<6s} need_lo {r.need_lo:+.4f} = "
              f"{r.lo_over_SD:+6.2f} SD {'RESOLVED' if r.resolved_lo else 'unresolved':<10s} | "
              f"need_hi {r.need_hi:+.4f} = {r.hi_over_SD:+6.2f} SD "
              f"{'RESOLVED' if r.resolved_hi else 'unresolved':<10s} | plateau {int(r.plateau_rungs):2d} rungs "
              f"tilt {r.plateau_tilt:+.4f} vs ramp {r.ramp_rise:+.4f}  -> TENT RESOLVED {r.tent_resolved}")
    ggs = shapes[shapes.dial == "D_GROSS"]
    exp_ok = all(bool(ggs[(ggs.panel == p) & (ggs.leg == lg)].tent_resolved.iloc[0])
                 for p in PANELS for lg in ("L_DD", "L_VOLTGT"))
    non_ok = all(not bool(ggs[(ggs.panel == p) & (ggs.leg == lg)].tent_resolved.iloc[0])
                 for p in PANELS for lg in ("L_TUW", "L_ULCER"))
    h_peak = bool(exp_ok and non_ok)
    P(f"  -> H_PEAKRESOLVED (POST-HOC) {'HOLDS' if h_peak else 'FAILS'}: on D_GROSS the peak is")
    P(f"     resolved against BOTH endpoints at {int(ggs.tent_resolved.sum())} of {len(ggs)} cells; "
      f"EXPOSURE legs {sum(bool(ggs[(ggs.panel == p) & (ggs.leg == lg)].tent_resolved.iloc[0]) for p in PANELS for lg in ('L_DD', 'L_VOLTGT'))}"
      f"/4, NON-exposure legs "
      f"{sum(bool(ggs[(ggs.panel == p) & (ggs.leg == lg)].tent_resolved.iloc[0]) for p in PANELS for lg in ('L_TUW', 'L_ULCER'))}/4.")
    P(f"  ACROSS ALL {len(shapes)} CELLS: TENT {int(shapes.tent.sum())}, of which RESOLVED "
      f"{int(shapes.tent_resolved.sum())}; by leg " +
      "  ".join(f"{lg} {int(shapes[shapes.leg == lg].tent_resolved.sum())}/{int(shapes[shapes.leg == lg].tent.sum())}"
               for lg in SWAPS))
    P("  THE SIGN OF A DEGREE-0 LEG'S TILT IS NOISE, WHICH IS THE WHOLE POINT:")
    for lg in ("L_TUW", "L_ULCER"):
        for panel in PANELS:
            sub2 = grid[(grid.panel == panel) & (grid.dial == "D_GROSS")].sort_values("rung_i")
            vv = sub2[f"M_{lg}"].values.astype(float)
            P(f"    {panel:<5s} {lg:<9s} margin {vv[0]:+.4f} -> {vv[-1]:+.4f} "
              f"(range {vv[-1] - vv[0]:+.4f}), measured degree slope "
              f"{float(deg[(deg.panel == panel) & (deg.stat == ('TUW' if lg == 'L_TUW' else 'UPI'))].measured_slope.iloc[0]):+.4f}")

    # --------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("")
    P("## RULE 8 (walk-forward) AND BOTH KEEP PATHS")
    P("   Every chooser here is IS-ONLY by construction, so each of the 40 picks IS a rule-8")
    P(f"   decision: read on 2009-01..{IS_END}, scored on {IS_END}..{PIN} untouched.")
    for panel in PANELS:
        sb, lb = spy_m[panel], live_m[panel]
        P(f"   {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   {panel} RULES v2  full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%} "
          f"(halves {lb['H1']:.4f}/{lb['H2']:.4f}), OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        for nm, mm in (("SPY", sb), ("RULESv2", lb)):
            wfrows.append(dict(panel=panel, dial="(benchmark)", leg=nm, arm=nm, chosen_on="n/a",
                               shape_class="n/a", OOS_CAGR=mm["OOS_CAGR"], OOS_Sharpe=mm["OOS_Sharpe"],
                               OOS_MaxDD=mm["OOS_MaxDD"], full_CAGR=mm["CAGR"],
                               full_Sharpe=mm["Sharpe"], full_MaxDD=mm["MaxDD"],
                               H1=mm["H1"], H2=mm["H2"], pass_4b=False, pass_4b_oos=False,
                               pass_4a=False))
    base_rate = float((grid.pass_4b & grid.pass_4b_oos).mean())
    pick_rate = float((picks.pass_4b & picks.pass_4b_oos).mean())
    P(f"   LADDER BASE RATES over all {len(grid)} published cells: 4b full "
      f"{int(grid.pass_4b.sum())}, 4b OOS {int(grid.pass_4b_oos.sum())}, both "
      f"{int((grid.pass_4b & grid.pass_4b_oos).sum())} ({base_rate:.1%}), 4a {int(grid.pass_4a.sum())}")
    P(f"   THE 40 PICKS: 4b full {int(picks.pass_4b.sum())}, 4b OOS {int(picks.pass_4b_oos.sum())}, "
      f"both {int((picks.pass_4b & picks.pass_4b_oos).sum())} ({pick_rate:.1%}), "
      f"4a {int(picks.pass_4a.sum())}")
    P("   PICK PASS RATE BY LEG (4b full+OOS):")
    for lg in SWAPS:
        s = picks[picks.leg == lg]
        P(f"     {lg:<9s} {int((s.pass_4b & s.pass_4b_oos).sum())}/{len(s)}   "
          f"(interior picks {int((~s.endpoint).sum())}/{len(s)})")
    inter = picks[~picks.endpoint]
    endp = picks[picks.endpoint]
    h_pickpay = bool(len(inter) and (inter.pass_4b & inter.pass_4b_oos).mean() >= base_rate)
    P(f"   INTERIOR picks {int((inter.pass_4b & inter.pass_4b_oos).sum())}/{len(inter)} "
      f"vs ENDPOINT picks {int((endp.pass_4b & endp.pass_4b_oos).sum())}/{len(endp)} "
      f"vs ladder base rate {base_rate:.1%}  -> H_PICKPAY "
      f"{'HOLDS' if h_pickpay else 'FAILS'}")
    h_nopay4a = bool(grid.pass_4a.sum() == 0 and picks.pass_4a.sum() == 0)
    P(f"   4a is {int(grid.pass_4a.sum())} of {len(grid)} cells and {int(picks.pass_4a.sum())} "
      f"of {len(picks)} picks  -> H_NOPAY4a {'HOLDS' if h_nopay4a else 'FAILS'}")
    ok = picks[picks.pass_4b & picks.pass_4b_oos]
    if len(ok):
        P("   EVERY PICK THAT CLEARS 4b FULL AND OOS (the capital-relevant rows):")
        for _, r in ok.sort_values("OOS_Sharpe", ascending=False).iterrows():
            sbp = spy_m[r.panel]
            P(f"     {r.panel:<5s} {r.dial:<10s} {r.leg:<9s} {r['shape_class']:<13s} pick {r['pick']:<6s} "
              f"full {r.CAGR:.2%} / {r.Sharpe:.4f} / {r.MaxDD:.2%} (halves {r.H1:.4f}/{r.H2:.4f}), "
              f"OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%}, "
              f"{r.turn_per_yr:.2f}x/yr  [SPY OOS {sbp['OOS_CAGR']:.2%} / {sbp['OOS_Sharpe']:.4f} "
              f"/ {sbp['OOS_MaxDD']:.2%}]")
    else:
        P("   NO pick clears 4b full AND OOS.")
    bestg = grid[grid.pass_4b & grid.pass_4b_oos]
    if len(bestg):
        bb = bestg.iloc[int(np.nanargmax(bestg.OOS_Sharpe.values))]
        P(f"   BEST LADDER cell (not a pick) passing 4b full+OOS: {bb.panel} {bb.dial} rung "
          f"{bb.rung} — full {bb.CAGR:.2%} / {bb.Sharpe:.4f} / {bb.MaxDD:.2%}, OOS "
          f"{bb.OOS_CAGR:.2%} / {bb.OOS_Sharpe:.4f} / {bb.OOS_MaxDD:.2%}")
    dump(pd.DataFrame(wfrows), "walkforward")

    hyp = pd.DataFrame([
        dict(hypothesis="H_DEGREE", bar="declared degrees == measured slopes (deg1 >= 0.5, deg0 <= 0.25)",
             value=f"{int(deg.matches_declared.sum())}/{len(deg)}",
             verdict="HOLDS" if h_degree else "FAILS"),
        dict(hypothesis="H_TENTLIVES", bar="L_VOLTGT (exposure) is a TENT on D_GROSS, both panels",
             value=str([bool(gg[(gg.panel == p) & (gg.leg == 'L_VOLTGT')].tent.iloc[0]) for p in PANELS]),
             verdict="HOLDS" if h_tentlives else "FAILS"),
        dict(hypothesis="H_TENTDIES", bar="L_TUW and L_ULCER monotone AND endpoint on D_GROSS, both panels",
             value=str([[bool(gg[(gg.panel == p) & (gg.leg == lg)].mono.iloc[0]),
                         bool(gg[(gg.panel == p) & (gg.leg == lg)].endpoint.iloc[0])]
                        for p in PANELS for lg in ("L_TUW", "L_ULCER")]),
             verdict="HOLDS" if h_tentdies else "FAILS"),
        dict(hypothesis="H_PAIRONLY", bar="no NON-exposure leg is a TENT on ANY dial",
             value=f"{len(nonexp_tents)} non-exposure tents of {int(shapes.tent.sum())} total",
             verdict="HOLDS" if h_paironly else "FAILS"),
        dict(hypothesis="H_PICKPAY", bar="interior picks clear 4b full+OOS at >= the ladder base rate",
             value=f"{float((inter.pass_4b & inter.pass_4b_oos).mean()) if len(inter) else float('nan'):.3f} "
                   f"vs {base_rate:.3f}", verdict="HOLDS" if h_pickpay else "FAILS"),
        dict(hypothesis="H_PEAKRESOLVED (POST-HOC)",
             bar="on D_GROSS the peak beats BOTH endpoints by >1 paired SD only for EXPOSURE legs",
             value=f"exposure {sum(bool(ggs[(ggs.panel == p) & (ggs.leg == lg)].tent_resolved.iloc[0]) for p in PANELS for lg in ('L_DD', 'L_VOLTGT'))}/4, "
                   f"non-exposure {sum(bool(ggs[(ggs.panel == p) & (ggs.leg == lg)].tent_resolved.iloc[0]) for p in PANELS for lg in ('L_TUW', 'L_ULCER'))}/4",
             verdict="HOLDS" if h_peak else "FAILS"),
        dict(hypothesis="H_NOPAY4a", bar="4a is 0 of every cell and every pick",
             value=f"{int(grid.pass_4a.sum())}/{len(grid)} cells, {int(picks.pass_4a.sum())}/{len(picks)} picks",
             verdict="HOLDS" if h_nopay4a else "FAILS"),
    ])
    dump(hyp, "hypotheses")
    dump(pd.DataFrame(gaterows), "gates")
    P("")
    P("## HYPOTHESES")
    P(hyp.to_string(index=False))
    P("")
    answer = ("NO — THE TENT IS AN EXPOSURE-PAIR OBJECT AND DIES WITH THE SECOND EXPOSURE LEG"
              if (h_degree and h_tentlives and h_tentdies) else
              "YES IN SHAPE, NO IN SUBSTANCE — the decision rule's three conditions are "
              f"H_DEGREE {h_degree}, H_TENTLIVES {h_tentlives}, H_TENTDIES {h_tentdies}; the "
              f"POST-HOC peak test reads H_PEAKRESOLVED {h_peak}")
    P(f"## DECISION RULE SAYS: {answer}")
    P("")
    P(f"# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

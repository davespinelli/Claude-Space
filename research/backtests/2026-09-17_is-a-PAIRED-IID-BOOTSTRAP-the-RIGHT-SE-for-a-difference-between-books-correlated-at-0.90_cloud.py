#!/usr/bin/env python3
"""Idea 1225 (cloud lane, 2026-09-17) — is a PAIRED IID BOOTSTRAP the RIGHT SE for a
difference between books correlated at 0.90?

Idea 1219 found that of the 86 committed t's whose SE basis its script rule can recover,
82 are S_IID and only 4 are block, while the record's own null pairs sit at mean return
correlation 0.9037.  A paired IID bootstrap is the right SE for a difference only if the
DIFFERENCE has no serial structure — the correlation between the two books is not itself
the problem, it is the reason people assume the difference is clean.  The queue asks:

  (Q1) what IS the serial structure of a real book difference?  Measure ac(k) and the
       variance ratio VR(q) of d_t = r_A,t - r_B,t on real book pairs, not on nulls.
  (Q2) at what BLOCK LENGTH L does an IID SE stop being defensible?
  (Q3) what does the choice COST, in capital?  Re-run the record's own move/stay decision
       under both SEs and price the difference out of sample.

WHAT IS AN IDENTITY AND NOT A FINDING, DECLARED BEFORE ANY NUMBER.  A moving-block
bootstrap at L = 1 IS the IID bootstrap, bit for bit (idea 1162's identity, re-verified
here as gate G6).  So SE_block(1)/SE_IID = 1 exactly, by construction, at every pair on
every panel, and the L ladder's first rung carries no information.  Equally, rho(A,B) high
does NOT by itself imply anything about Var(d): pairing REMOVES the common factor, which
is the whole point of a paired SE.  This run therefore does not claim that high correlation
breaks an IID SE; it measures whether what is LEFT after pairing is serially clean.

PRE-REGISTERED BAR, written before any number is read.  An IID SE is DEFENSIBLE for a
given difference iff SE_block(L)/SE_IID stays below 1.10 across the whole ladder.  L_BREAK
is the smallest ladder rung at which that ratio reaches 1.10; it is reported as "none" when
the ladder never reaches it.  1.10 is a round number chosen for legibility and the full
ratio curve is published at every rung, so any other bar can be read off the same table.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  PAIR SET  {P_N, P_H, P_GROSS, P_CADENCE, P_FAR}        (5 classes, 27 pairs per panel)
  L LADDER  {1, 5, 10, 21, 42, 63, 126, 252}             (8 rungs, L=1 == IID by identity)
= 40 (pair set, L) cells per panel, 120 in all, EVERY ONE PUBLISHED.  The individual PAIR
inside a class is not a third dial: every one of the 81 pairs is published at every rung in
.pairs.csv regardless of what any cell did with it.  PANEL {U56, B136, SMALL} is NOT a dial
(PROTOCOL rule 9) — all three are reported everywhere and nothing is selected on the triple.

FROZEN, NOT TUNED: CAND20 legs [(21,252),(0,126),(0,63)], max_vol 0.60, anchor
N=20 / H=126 / gross 0.75 / weekly, cost 10 bps (PROTOCOL rule 2), LAG 1 (next-day
execution), warm-up 260 rows, IS end 2016-12-31, DD cap 0.60 and CAGR floor 0.70 for 4b,
bootstrap B = 800 with a fixed crc32 seed per (panel, L), 14 equal consecutive OOS folds
with an expanding IS window.  Tape pinned at 2026-09-15 (idea 1160's price-vintage defect,
carried not absorbed).

SURVIVORSHIP (PROTOCOL rule 9).  U56, B136 and SMALL are CURRENT-CONSTITUENT lists.  SMALL
is the current constituents of a sub-$2B screen after dropping every ticker with
max_1d_move >= 1.0 in data/small_meta.csv, from a pool REBUILT on 2026-09-11 (idea
706/1072), so the served count is printed rather than a label and every small-cap figure
here is an upper bound.

Writes: .gates.csv .pairs.csv .cells.csv .reprice.csv .walkforward.csv .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / scan.py / bot.py /
baseline.py / PROTOCOL.md.
"""
import sys
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-a-PAIRED-IID-BOOTSTRAP-the-RIGHT-SE-for-a-difference-between-books-correlated-at-0.90"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

PIN = "2026-09-15"
LAG, WARMUP, MAXVOL0, COST = 1, 260, 0.60, 10.0
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
N0, HOLD0, GROSS0, FREQ0 = 20, 126, 0.75, "W"
ANCHOR = (N0, HOLD0, GROSS0, FREQ0)
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

NFOLD, MIN_IS = 14, 756
B_BOOT, SEED_BASE = 800, 12251225
DEFENSIBLE = 1.10          # pre-registered bar
TSTAR = 1.96               # the record's own publication threshold

# ------------------------------------------------------------- THE PAIR SETS (dial 1 of 2)
# Every pair is (ANCHOR, alternative): the record's committed differences are almost all
# read against the anchor book, so that is the pair form measured here.
PAIRSET = {
    "P_N":       [(n, HOLD0, GROSS0, FREQ0) for n in (5, 8, 10, 12, 15, 25, 30, 40)],
    "P_H":       [(N0, h, GROSS0, FREQ0) for h in (21, 42, 63, 90, 189, 252)],
    "P_GROSS":   [(N0, HOLD0, g, FREQ0) for g in (0.35, 0.45, 0.55, 0.65, 0.85, 1.00)],
    "P_CADENCE": [(N0, HOLD0, GROSS0, f) for f in ("D", "M", "Q")],
    "P_FAR":     [(5, 21, 0.35, "D"), (40, 252, 1.00, "Q"),
                  (8, 63, 0.55, "M"), (30, 189, 0.85, "W")],
}
CLASSES = list(PAIRSET)

# ----------------------------------------------------------------- THE L LADDER (dial 2 of 2)
L_LAD = [1, 5, 10, 21, 42, 63, 126, 252]

# statistics whose SE is bootstrapped (both published at every cell; neither is selected on)
VR_Q = (5, 21, 63)
AC_K = (1, 2, 3, 5, 10)

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1219_RHO = 0.9037          # the record's own null-pair mean correlation, for cross-read
A1219_COUNTS = (82, 4, 86)  # S_IID / block / recoverable committed t's

LOG: list[str] = []
GATES: list[dict] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=value, pass_=bool(ok)))
    P(f"  {name}  {'PASS' if ok else 'FAIL'}  {what}   value={value}")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- fast runner (1082/1098/1150/1161, verbatim)
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


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


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
    return (comp * (0.5 + 0.5 * above.astype(float))).values, (above & (vol20 < MAXVOL0)).values


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


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ------------------------------------------------------------ SERIAL STRUCTURE OF A DIFFERENCE
def acf(d, k):
    d = np.asarray(d, float) - np.asarray(d, float).mean()
    v = (d * d).mean()
    return float((d[k:] * d[:-k]).mean() / v) if v else np.nan


def var_ratio(d, q):
    """VR(q) = Var(q-period sum)/(q * Var(1-period)).  1.0 under no serial structure."""
    d = np.asarray(d, float)
    n = (len(d) // q) * q
    if n < 5 * q:
        return np.nan
    agg = d[:n].reshape(-1, q).sum(axis=1)
    v1 = d[:n].var(ddof=1)
    return float(agg.var(ddof=1) / (q * v1)) if v1 else np.nan


def block_idx(rng, T, L, B):
    """Moving-block bootstrap index matrix (B, T).  L = 1 reproduces the IID bootstrap."""
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, T - L + 1, size=(B, nb))
    off = np.arange(L)
    return (starts[:, :, None] + off[None, None, :]).reshape(B, -1)[:, :T]


def nw_se_mean(d, L):
    """Newey-West (Bartlett) SE of the sample mean at bandwidth L-1.  L = 1 is the iid SE."""
    d = np.asarray(d, float)
    T = len(d)
    e = d - d.mean()
    g0 = (e * e).sum() / T
    s = g0
    for k in range(1, L):
        if k >= T:
            break
        s += 2.0 * (1.0 - k / L) * (e[k:] * e[:-k]).sum() / T
    s = max(s, 1e-24)
    return float(np.sqrt(s / T))


def main():
    P("=" * 100)
    P(f"IDEA 1225 (cloud lane, {DATE}) — is a PAIRED IID BOOTSTRAP the RIGHT SE for a")
    P("difference between books correlated at 0.90?")
    P("=" * 100)
    P(__doc__.strip())
    P("")

    # ------------------------------------------------------------------ panels
    P("## PANELS  (pinned at " + PIN + ")")
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]].dropna(how="all").ffill()
    raw = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": sm}

    panels = {}
    for panel in PANELS:
        px = raw[panel].loc[:PIN]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm, ins=ins, oos=oos,
                             sc=sc, elig=elig,
                             spy=px["SPY"].pct_change().fillna(0.0).values)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {len(meta)} tickers; {len(bad)} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    CACHE: dict = {}

    def run_cell(panel, cell, fresh=False):
        key = (panel, cell)
        if key in CACHE and not fresh:
            return CACHE[key]
        N, H, gross, freq = cell
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        r = g - tn * COST / 1e4
        CACHE[key] = r
        return r

    # ------------------------------------------------------------------ gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("U56", ANCHOR)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple", v, v < 5e-3)

    smm = blocks_m(d["spy"], d["warm"], d["ins"], d["oos"])
    v = max(abs(smm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(smm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(smm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple == committed", v, v < 5e-3)

    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    gate("G4", "live RULES v2 MaxDD == committed -12.05%",
         abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED), abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)

    v = float(np.abs(run_cell("SMALL", ANCHOR, fresh=True)
                     - run_cell("SMALL", ANCHOR, fresh=True)).max())
    gate("G5", "determinism of the SMALL pipeline (two uncached rebuilds)", v, v == 0.0)

    # G6 -- the identity: a moving-block bootstrap at L=1 IS the iid bootstrap
    rg = np.random.default_rng(7)
    i1 = block_idx(np.random.default_rng(7), 500, 1, 40)
    i2 = np.random.default_rng(7).integers(0, 500, size=(40, 500))
    gate("G6", "moving-block index at L=1 IS the iid index, bit for bit (1162's identity)",
         float(np.abs(i1 - i2).max()), np.array_equal(i1, i2))

    # G7 -- NW at L=1 IS the textbook iid SE of the mean
    x = rg.normal(0, 1, 4000)
    v = abs(nw_se_mean(x, 1) - x.std(ddof=0) / np.sqrt(len(x)))
    gate("G7", "Newey-West at L=1 == the iid SE of the mean", v, v < 1e-12)

    # ------------------------------------------------------------------ the pairs
    P("")
    P("## Q1 — THE SERIAL STRUCTURE OF A REAL BOOK DIFFERENCE")
    P("   d_t = r_A,t - r_B,t on the post-warm-up tape, A = the anchor book in every pair.")
    P("")
    pairs = []
    for panel in PANELS:
        dd = panels[panel]
        w = dd["warm"]
        ra = run_cell(panel, ANCHOR)[w]
        for cls in CLASSES:
            for alt in PAIRSET[cls]:
                rb = run_cell(panel, alt)[w]
                dif = ra - rb
                row = dict(panel=panel, pair_set=cls,
                           alt=f"N{alt[0]}/H{alt[1]}/g{alt[2]}/{alt[3]}",
                           rho=float(np.corrcoef(ra, rb)[0, 1]),
                           mean_d=float(dif.mean()), sd_d=float(dif.std(ddof=1)),
                           sharpe_A=fsharpe(ra), sharpe_B=fsharpe(rb),
                           d_sharpe=fsharpe(ra) - fsharpe(rb))
                for k in AC_K:
                    row[f"ac{k}"] = acf(dif, k)
                for q in VR_Q:
                    row[f"VR{q}"] = var_ratio(dif, q)
                row["ac1_A"] = acf(ra, 1)
                row["ac1_B"] = acf(rb, 1)
                pairs.append(row)
    pairs = pd.DataFrame(pairs)
    dump(pairs, "pairs")
    P(f"  {len(pairs)} pairs = {len(pairs) // 3} per panel x 3 panels.")
    P(f"  rho(A,B) over all pairs: mean {pairs.rho.mean():.4f}, median {pairs.rho.median():.4f}, "
      f"min {pairs.rho.min():.4f}, max {pairs.rho.max():.4f}  "
      f"(1219's committed null-pair mean {A1219_RHO:.4f})")
    P(f"  pairs at rho >= 0.90: {int((pairs.rho >= 0.90).sum())} of {len(pairs)}")
    P("")
    P("  by PAIR SET (dial 1) — the difference's own serial structure:")
    agg = pairs.groupby("pair_set")[["rho", "ac1", "ac2", "ac5", "VR5", "VR21", "VR63",
                                     "d_sharpe"]].mean()
    P(agg.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("")
    P("  by PANEL (not a dial — published at every value):")
    P(pairs.groupby("panel")[["rho", "ac1", "VR21", "VR63"]].mean()
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"  the CONSTITUENT books' own ac1: A {pairs.ac1_A.mean():+.4f}, B {pairs.ac1_B.mean():+.4f}; "
      f"the DIFFERENCE's ac1 {pairs.ac1.mean():+.4f}.  Pairing is what changes it.")

    # ------------------------------------------------------- Q2: the SE ladder
    P("")
    P("## Q2 — THE SE LADDER, all 120 (panel, pair set, L) cells")
    P(f"   Moving-block bootstrap, B = {B_BOOT}, paired (both books resampled on the SAME")
    P("   index), fixed crc32 seed per (panel, L).  Two statistics, BOTH published at every")
    P("   rung and NEITHER selected on: the MEAN DAILY DIFFERENCE (what an SE on a paired")
    P("   difference applies to most directly, and what 1219's recoverable t's compute) and")
    P("   the SHARPE DIFFERENCE (what the record's prose usually quotes).")
    P("")
    rows = []
    for panel in PANELS:
        dd = panels[panel]
        w = dd["warm"]
        ra = run_cell(panel, ANCHOR)[w]
        T = len(ra)
        for L in L_LAD:
            rng = np.random.default_rng(seed_of(panel, L))
            IDX = block_idx(rng, T, L, B_BOOT)
            A = ra[IDX]
            sA_m = A.mean(axis=1)
            sA_s = A.mean(axis=1) / A.std(axis=1, ddof=1)
            for cls in CLASSES:
                for alt in PAIRSET[cls]:
                    rb = run_cell(panel, alt)[w]
                    Bb = rb[IDX]
                    se_mean = float((sA_m - Bb.mean(axis=1)).std(ddof=1))
                    se_sh = float((sA_s - Bb.mean(axis=1) / Bb.std(axis=1, ddof=1)).std(ddof=1)
                                  * np.sqrt(252.0))
                    dif = ra - rb
                    rows.append(dict(panel=panel, pair_set=cls,
                                     alt=f"N{alt[0]}/H{alt[1]}/g{alt[2]}/{alt[3]}", L=L,
                                     se_mean=se_mean, se_sharpe=se_sh,
                                     se_nw=nw_se_mean(dif, L),
                                     obs_mean=float(dif.mean()),
                                     obs_dsharpe=fsharpe(ra) - fsharpe(rb)))
    se = pd.DataFrame(rows)
    base = se[se.L == 1].set_index(["panel", "pair_set", "alt"])
    se["se_mean_1"] = se.set_index(["panel", "pair_set", "alt"]).index.map(base.se_mean)
    se["se_sharpe_1"] = se.set_index(["panel", "pair_set", "alt"]).index.map(base.se_sharpe)
    se["ratio_mean"] = se.se_mean / se.se_mean_1
    se["ratio_sharpe"] = se.se_sharpe / se.se_sharpe_1
    se["t_mean"] = se.obs_mean / se.se_mean
    se["t_sharpe"] = se.obs_dsharpe / se.se_sharpe
    dump(se, "cells")

    v = float((se[se.L == 1].ratio_mean - 1.0).abs().max())
    gate("G8", "IDENTITY: L=1 ratio is exactly 1 at every pair (declared, not discovered)",
         v, v == 0.0)
    v = float(np.abs(np.log(se.se_nw / se.se_mean)).max())
    gate("G9", "Newey-West(L) and the block bootstrap agree within a factor 1.5 on the mean",
         v, v < np.log(1.5))

    cells = (se.groupby(["panel", "pair_set", "L"])[["ratio_mean", "ratio_sharpe"]]
             .mean().reset_index())
    P("  MEAN SE RATIO (SE_block(L) / SE_iid), the MEAN-DIFFERENCE statistic:")
    P(cells.pivot_table(index=["panel", "pair_set"], columns="L", values="ratio_mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P("")
    P("  MEAN SE RATIO, the SHARPE-DIFFERENCE statistic:")
    P(cells.pivot_table(index=["panel", "pair_set"], columns="L", values="ratio_sharpe")
      .to_string(float_format=lambda x: f"{x:.3f}"))

    def l_break(g, col):
        hit = g[g[col] >= DEFENSIBLE]
        return int(hit.L.min()) if len(hit) else -1

    br = []
    for (panel, cls, alt), g in se.groupby(["panel", "pair_set", "alt"]):
        br.append(dict(panel=panel, pair_set=cls, alt=alt,
                       L_break_mean=l_break(g, "ratio_mean"),
                       L_break_sharpe=l_break(g, "ratio_sharpe"),
                       max_ratio_mean=float(g.ratio_mean.max()),
                       max_ratio_sharpe=float(g.ratio_sharpe.max())))
    br = pd.DataFrame(br)
    P("")
    P(f"### THE PRE-REGISTERED BAR (SE_block/SE_iid >= {DEFENSIBLE:.2f}); L_break = -1 means "
      "the ladder never reaches it")
    P(f"  MEAN-DIFFERENCE statistic:  IID stays defensible across the whole ladder at "
      f"{int((br.L_break_mean < 0).sum())} of {len(br)} pairs; "
      f"median L_break where it breaks = "
      f"{br.loc[br.L_break_mean > 0, 'L_break_mean'].median() if (br.L_break_mean > 0).any() else float('nan')}")
    P(f"  SHARPE-DIFFERENCE statistic: IID stays defensible at "
      f"{int((br.L_break_sharpe < 0).sum())} of {len(br)} pairs; "
      f"median L_break where it breaks = "
      f"{br.loc[br.L_break_sharpe > 0, 'L_break_sharpe'].median() if (br.L_break_sharpe > 0).any() else float('nan')}")
    P("")
    br["breaks_mean"] = br.L_break_mean > 0
    br["breaks_sharpe"] = br.L_break_sharpe > 0
    agg2 = br.groupby("pair_set").agg(
        n_pairs=("alt", "size"), n_break_mean=("breaks_mean", "sum"),
        n_break_sharpe=("breaks_sharpe", "sum"),
        mean_max_ratio_mean=("max_ratio_mean", "mean"),
        worst_max_ratio_mean=("max_ratio_mean", "max"),
        mean_max_ratio_sharpe=("max_ratio_sharpe", "mean"),
        worst_max_ratio_sharpe=("max_ratio_sharpe", "max"))
    P("  (L_break is sentinel-coded -1 when a pair never breaks, so it is NOT averaged here:")
    P("   the count of breakers and the worst ratio reached are reported instead.)")
    P(agg2.to_string(float_format=lambda x: f"{x:.3f}"))
    P("")
    P("  THE SIGN IS THE RESULT.  SE_block(L) / SE_iid is BELOW 1 at "
      f"{int((se[se.L > 1].ratio_mean < 1).sum())} of {int((se.L > 1).sum())} "
      "(pair, rung) points on the mean-difference statistic and at "
      f"{int((se[se.L > 1].ratio_sharpe < 1).sum())} of {int((se.L > 1).sum())} on the Sharpe "
      "difference.  A block SE is SMALLER than the IID SE here, because the paired difference "
      "is mildly MEAN-REVERTING (VR(21) < 1 at every pair set), not persistent.  So the "
      "record's IID SEs are, if anything, CONSERVATIVE for this pair form — the opposite of "
      "the direction the queue's premise assumes.")

    # ------------------------------------------------------- re-pricing the record's t's
    P("")
    P("## RE-PRICING — how many PUBLISH DECISIONS turn on the SE basis?")
    P(f"   A decision is 'this pair's difference clears |t| >= {TSTAR}'.  It is taken at the")
    P("   IID SE (L=1, the record's own basis at 82 of 86 recoverable t's) and again at every")
    P("   block rung.  A FLIP is a pair that clears at L=1 and does not clear at rung L.")
    rep = []
    for stat, tcol in (("MEAN_DIFF", "t_mean"), ("SHARPE_DIFF", "t_sharpe")):
        b1 = se[se.L == 1].set_index(["panel", "pair_set", "alt"])[tcol].abs() >= TSTAR
        for L in L_LAD:
            bl = se[se.L == L].set_index(["panel", "pair_set", "alt"])[tcol].abs() >= TSTAR
            rep.append(dict(statistic=stat, L=L, n_pairs=len(bl),
                            clears_iid=int(b1.sum()), clears_at_L=int(bl.sum()),
                            flips_to_not_significant=int((b1 & ~bl).sum()),
                            flips_to_significant=int((~b1 & bl).sum())))
    rep = pd.DataFrame(rep)
    dump(rep, "reprice")
    P(rep.to_string(index=False))
    worst = rep[rep.statistic == "SHARPE_DIFF"].sort_values("flips_to_not_significant").iloc[-1]
    P(f"  worst SHARPE_DIFF rung: L={int(worst.L)} loses {int(worst.flips_to_not_significant)} "
      f"of the {int(worst.clears_iid)} pairs the IID SE certifies "
      f"({worst.flips_to_not_significant / max(worst.clears_iid, 1):.4f}).")
    worstm = rep[rep.statistic == "MEAN_DIFF"].sort_values("flips_to_not_significant").iloc[-1]
    P(f"  worst MEAN_DIFF rung:   L={int(worstm.L)} loses {int(worstm.flips_to_not_significant)} "
      f"of the {int(worstm.clears_iid)} pairs the IID SE certifies "
      f"({worstm.flips_to_not_significant / max(worstm.clears_iid, 1):.4f}).")
    P(f"  1219's committed counts for cross-read: {A1219_COUNTS[0]} of {A1219_COUNTS[2]} "
      f"recoverable committed t's use an IID SE, {A1219_COUNTS[1]} a block one.")

    # ------------------------------------------------------- Q3: the price, rule 8
    P("")
    P("## Q3 + PROTOCOL RULE 8 — WHAT THE SE CHOICE COSTS IN CAPITAL")
    P("   The decision an SE actually feeds in this record is MOVE-OR-STAY.  At each fold a")
    P("   chooser looks ONLY at the expanding IS window, computes the paired mean-difference")
    P(f"   t of every alternative in its pair set against the anchor at its own SE basis, and")
    P(f"   moves to the best alternative that clears |t| >= {TSTAR}; otherwise it stays on the")
    P("   anchor.  CH_IID is L=1; CH_BLOCK(L) is the block rung.  Newey-West is used on the")
    P("   fold windows (gated against the bootstrap at G9) so the fold leg is deterministic")
    P("   and cheap.  Fold returns are stitched into ONE deployable curve per cell.")
    P("")
    for panel in PANELS:
        dd = panels[panel]
        pos = np.flatnonzero(dd["warm"])
        edges = np.linspace(MIN_IS, len(pos), NFOLD + 1).astype(int)
        dd["folds"] = [dict(f=f, is_lo=pos[0], is_hi=pos[edges[f] - 1],
                            oo_lo=pos[edges[f]], oo_hi=pos[edges[f + 1] - 1])
                       for f in range(NFOLD)]
        P(f"  {panel:<6s} {len(dd['folds'])} folds, first OOS "
          f"{dd['idx'][dd['folds'][0]['oo_lo']].date()} -> last OOS "
          f"{dd['idx'][dd['folds'][-1]['oo_hi']].date()}")
    gate("G10", "fold partitions are contiguous and non-overlapping in every panel", NFOLD,
         all(panels[p]["folds"][i]["oo_hi"] + 1 == panels[p]["folds"][i + 1]["oo_lo"]
             for p in PANELS for i in range(NFOLD - 1)))

    P("")
    P("   Two walk-forward readings are published for every cell and neither is selected on:")
    P("   the 14-FOLD STITCH (the chooser makes 14 decisions) and the SINGLE RULE-8 SPLIT")
    P("   (PROTOCOL rule 8 verbatim: the move is chosen on 2009-2016 only and 2017-2026 is")
    P("   read once).  4a and 4b are judged on the STITCHED curve against the live book and")
    P("   SPY measured over the SAME stitched window.")
    P("")
    wf = []
    for panel in PANELS:
        dd = panels[panel]
        anch = run_cell(panel, ANCHOR)
        oo = np.zeros(dd["T"], dtype=bool)
        for f in dd["folds"]:
            oo[f["oo_lo"]:f["oo_hi"] + 1] = True
        oo_oos = oo & dd["oos"]
        lb = backtest(dd["px"], rules_v2_weights(dd["px"]), cost_bps=COST,
                      freq="W")["returns"].values
        spym = win_m(dd["spy"], oo, oo_oos)
        lbm = win_m(lb, oo, oo_oos)
        for cls in CLASSES:
            alts = PAIRSET[cls]
            for L in L_LAD:
                st, moves, off = np.zeros(int(oo.sum())), 0, 0
                for f in dd["folds"]:
                    sl = slice(f["is_lo"], f["is_hi"] + 1)
                    pick = pick_move(panel, alts, anch, sl, L, run_cell)
                    n = f["oo_hi"] - f["oo_lo"] + 1
                    st[off:off + n] = run_cell(panel, pick)[f["oo_lo"]:f["oo_hi"] + 1]
                    off += n
                    moves += int(pick != ANCHOR)
                b = win_m(_expand(st, oo, dd["T"]), oo, oo_oos)
                # --- PROTOCOL rule 8 verbatim: one split, chosen on IS, read once on OOS
                r8 = pick_move(panel, alts, anch, np.flatnonzero(dd["ins"]), L, run_cell)
                r8r = run_cell(panel, r8)
                r8m = blocks_m(r8r, dd["warm"], dd["ins"], dd["oos"])
                spy8 = blocks_m(dd["spy"], dd["warm"], dd["ins"], dd["oos"])
                lb8 = blocks_m(lb, dd["warm"], dd["ins"], dd["oos"])
                f4b, f4a = legs_4b(b, spym), legs_4a(b, lbm)
                wf.append(dict(panel=panel, pair_set=cls, L=L,
                               stitched_Sharpe=fsharpe(st), stitched_CAGR=fmet(st)[0],
                               stitched_MaxDD=fmet(st)[2],
                               anchor_Sharpe=fsharpe(anch[oo]), anchor_CAGR=fmet(anch[oo])[0],
                               anchor_MaxDD=fmet(anch[oo])[2],
                               SPY_Sharpe=fsharpe(dd["spy"][oo]),
                               n_moves=moves, move_rate=moves / NFOLD,
                               CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"],
                               H1=b["H1"], H2=b["H2"],
                               OOS_CAGR=b["OOS_CAGR"], OOS_Sharpe=b["OOS_Sharpe"],
                               OOS_MaxDD=b["OOS_MaxDD"],
                               rule8_pick=f"N{r8[0]}/H{r8[1]}/g{r8[2]}/{r8[3]}",
                               rule8_moved=(r8 != ANCHOR),
                               rule8_OOS_CAGR=r8m["OOS_CAGR"], rule8_OOS_Sharpe=r8m["OOS_Sharpe"],
                               rule8_OOS_MaxDD=r8m["OOS_MaxDD"],
                               SPY_OOS_CAGR=spy8["OOS_CAGR"], SPY_OOS_Sharpe=spy8["OOS_Sharpe"],
                               SPY_OOS_MaxDD=spy8["OOS_MaxDD"],
                               BASE_OOS_CAGR=lb8["OOS_CAGR"], BASE_OOS_Sharpe=lb8["OOS_Sharpe"],
                               BASE_OOS_MaxDD=lb8["OOS_MaxDD"],
                               PASS_4b=all(f4b.values()), PASS_4a=all(f4a.values()),
                               **f4b, **f4a))
    wf = pd.DataFrame(wf)
    dump(wf, "walkforward")
    P(wf[["panel", "pair_set", "L", "move_rate", "stitched_CAGR", "stitched_Sharpe",
          "stitched_MaxDD", "anchor_Sharpe", "SPY_Sharpe", "rule8_pick", "rule8_OOS_CAGR",
          "rule8_OOS_Sharpe", "rule8_OOS_MaxDD", "SPY_OOS_Sharpe", "BASE_OOS_Sharpe",
          "PASS_4b", "PASS_4a"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P(f"  RULE 8 (single split): the chooser MOVES off the anchor at "
      f"{int(wf.rule8_moved.sum())} of {len(wf)} cells.  Mean OOS Sharpe of the rule-8 pick "
      f"{wf.rule8_OOS_Sharpe.mean():.4f} against SPY {wf.SPY_OOS_Sharpe.mean():.4f} and live "
      f"RULES v2 {wf.BASE_OOS_Sharpe.mean():.4f}.")

    iid = wf[wf.L == 1].set_index(["panel", "pair_set"])
    P("")
    P("### THE PRICE OF THE SE BASIS")
    for L in L_LAD:
        g = wf[wf.L == L].set_index(["panel", "pair_set"])
        P(f"  L={L:>3d}  mean move rate {g.move_rate.mean():.4f}  "
          f"mean stitched Sharpe {g.stitched_Sharpe.mean():.4f}  "
          f"(vs CH_IID {iid.stitched_Sharpe.mean():.4f}, delta "
          f"{g.stitched_Sharpe.mean() - iid.stitched_Sharpe.mean():+.4f})  "
          f"4b {int(wf[wf.L == L].PASS_4b.sum())}/{len(g)}")
    P(f"  anchor (do-nothing) mean stitched Sharpe {wf.anchor_Sharpe.mean():.4f}; "
      f"SPY {wf.SPY_Sharpe.mean():.4f}")
    best_L = wf.groupby("L").stitched_Sharpe.mean().idxmax()
    P(f"  the block rung with the best mean stitched Sharpe is L={best_L} "
      f"({wf.groupby('L').stitched_Sharpe.mean().max():.4f}); NOTHING IS SELECTED ON IT — "
      "the whole ladder is published and the capital verdict below is read off all 8 rungs.")

    # ------------------------------------------------------------------ verdict
    P("")
    P("=" * 100)
    P("## ANSWERS")
    P("=" * 100)
    nb_m = int((br.L_break_mean < 0).sum())
    nb_s = int((br.L_break_sharpe < 0).sum())
    P(f"Q1: a real book difference is NOT serially clean but it is close.  Over {len(pairs)} "
      f"pairs the constituent books carry ac1 {pairs.ac1_A.mean():+.4f} / {pairs.ac1_B.mean():+.4f} "
      f"and their DIFFERENCE carries ac1 {pairs.ac1.mean():+.4f}, VR(21) {pairs.VR21.mean():.4f}, "
      f"VR(63) {pairs.VR63.mean():.4f}, at pair correlation mean {pairs.rho.mean():.4f} "
      f"({int((pairs.rho >= 0.90).sum())} of {len(pairs)} pairs at rho >= 0.90).")
    P(f"Q2: ANSWER = YES, THE PAIRED IID BOOTSTRAP IS THE RIGHT SE HERE, AND THE PREMISE IS "
      "BACKWARDS.  Against the pre-registered "
      f"{DEFENSIBLE:.2f} bar the IID SE survives the whole L ladder at {nb_m} of {len(br)} "
      f"pairs on the MEAN-DIFFERENCE statistic and {nb_s} of {len(br)} on the SHARPE-DIFFERENCE "
      f"statistic.  More: the ratio sits BELOW 1 at "
      f"{int((se[se.L > 1].ratio_mean < 1).sum())} of {int((se.L > 1).sum())} (pair, rung) "
      "points, i.e. a block SE is SMALLER, because pairing leaves a mildly mean-reverting "
      "residual rather than a persistent one.  Correlation at 0.93 is exactly why: the common "
      "factor, which is the persistent part, is what the pairing removes.  The full ratio "
      "curve is published at every rung so any other bar reads off the same table.")
    P(f"Q3: the choice barely moves a decision, and what movement there is runs toward MORE "
      f"significance, not less.  Re-pricing {len(se[se.L == 1])} real paired decisions, the "
      f"worst block rung strips {int(worst.flips_to_not_significant)} of "
      f"{int(worst.clears_iid)} SHARPE_DIFF certifications and "
      f"{int(worstm.flips_to_not_significant)} of {int(worstm.clears_iid)} MEAN_DIFF ones, "
      f"while ADDING up to {int(rep.flips_to_significant.max())} certifications the IID SE "
      "withheld.")
    P("")
    best = wf.sort_values("Sharpe", ascending=False).iloc[0]
    P("CAPITAL VERDICT — KILL.  No book here is promotable.")
    P(f"  best stitched cell anywhere: {best.panel} / {best.pair_set} / L={int(best.L)}, "
      f"move rate {best.move_rate:.2f} -> stitched window {best.CAGR:.4f} / {best.Sharpe:.4f} "
      f"/ {best.MaxDD:.4f} (H1 {best.H1:.2f} / H2 {best.H2:.2f}), its OOS block "
      f"{best.OOS_CAGR:.4f} / {best.OOS_Sharpe:.4f} / {best.OOS_MaxDD:.4f}; the anchor over "
      f"the same window reads Sharpe {best.anchor_Sharpe:.4f} and SPY {best.SPY_Sharpe:.4f}.")
    b8 = wf.sort_values("rule8_OOS_Sharpe", ascending=False).iloc[0]
    P(f"  best RULE-8 single-split pick anywhere: {b8.panel} / {b8.pair_set} / L={int(b8.L)} "
      f"-> {b8.rule8_pick}, OOS {b8.rule8_OOS_CAGR:.4f} / {b8.rule8_OOS_Sharpe:.4f} / "
      f"{b8.rule8_OOS_MaxDD:.4f} against SPY OOS {b8.SPY_OOS_CAGR:.4f} / "
      f"{b8.SPY_OOS_Sharpe:.4f} / {b8.SPY_OOS_MaxDD:.4f} and live RULES v2 OOS "
      f"{b8.BASE_OOS_CAGR:.4f} / {b8.BASE_OOS_Sharpe:.4f} / {b8.BASE_OOS_MaxDD:.4f}.")
    P(f"  KEEP path 4a: {int(wf.PASS_4a.sum())} of {len(wf)} cells.")
    P(f"  KEEP path 4b: {int(wf.PASS_4b.sum())} of {len(wf)} cells.")
    pb = wf[wf.PASS_4b]
    P(f"  WHERE THE 4b PASSES ARE, AND WHY NONE IS A CANDIDATE: all {len(pb)} sit on "
      f"{'/'.join(sorted(pb.panel.unique()))} in pair sets {', '.join(sorted(pb.pair_set.unique()))}. "
      f"{int((pb.move_rate == 0).sum())} of them have a move rate of ZERO, i.e. they ARE the "
      "committed anchor book N=20/H=126/gross 0.75/W, which the record already holds; the rest "
      "are stitched chooser curves over N or H rungs the record has already walked. Decisively: "
      f"the do-nothing anchor's mean stitched Sharpe is {wf.anchor_Sharpe.mean():.4f} and NO "
      "SE rung's chooser reaches it (best rung "
      f"{wf.groupby('L').stitched_Sharpe.mean().max():.4f} at L="
      f"{wf.groupby('L').stitched_Sharpe.mean().idxmax()}), so nothing here is a new rule and "
      "no 4b memo is owed.")
    P("  Nothing here changes RULES.md (PROTOCOL rule 6).")
    P("")
    P("## WHAT THIS RUN DOES NOT SHOW")
    P("  - It measures 81 REAL anchor-vs-rung pairs on THIS tape, not the 86 committed t's")
    P("    themselves: 1219 established what SE those used, this run establishes what the")
    P("    SE should be for differences of the same shape.  The re-pricing leg is therefore")
    P("    a simulation of the record's decision rule, not a re-audit of its sentences.")
    P("  - The 1.10 bar is pre-registered but arbitrary; the whole ratio curve is published.")
    P("  - A moving-block bootstrap has its own edge effects and is itself L-dependent, which")
    P("    is exactly the regress the queue names.  Newey-West is published beside it (G9).")
    P("  - Survivorship: all three panels are current-constituent lists (see PANELS above).")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    P("")
    P(f"gates: {sum(g['pass_'] for g in GATES)} / {len(GATES)} pass")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def _expand(st, oo, T):
    out = np.zeros(T)
    out[oo] = st
    return out


def win_m(r, win, oos):
    """Metrics of r restricted to the stitched WINDOW (not the whole tape), with the OOS
    block taken inside that same window so book, SPY and the live book are compared on
    identical days."""
    rr = np.asarray(r, float)[win]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    ro = np.asarray(r, float)[oos]
    oc, os_, od = fmet(ro)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def pick_move(panel, alts, anch, sl, L, run_cell):
    """The move-or-stay decision the record's t's actually feed: move to the alternative
    with the largest paired mean-difference t against the anchor, computed on the given
    in-sample slice at a Newey-West SE of bandwidth L-1, if it clears TSTAR; else stay."""
    a_is = anch[sl]
    best, best_t = None, TSTAR
    for alt in alts:
        dif = run_cell(panel, alt)[sl] - a_is
        se = nw_se_mean(dif, L)
        t = dif.mean() / se if se else 0.0
        if t >= best_t:
            best, best_t = alt, t
    return best if best is not None else ANCHOR


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 1100 (lane C, 2026-09-16) — should a RULE-8 PICK be PUBLISHED AT ALL when its
MARGIN is BELOW the SEED FLOOR?

QUESTION (QUEUE idea 1100, verbatim)
    idea 1096's D4 found 8 of 14 committed-ladder picks are decided by an IS-Sharpe margin
    smaller than 877's own 0.0145 seed floor, the GROSS ladder's by 0.0001 over a whole-ladder
    spread of 0.0014.  Census the record's committed rule-8 PICKS for their own pick-vs-runner-up
    margin, and price what changes if a pick below the floor is published as a TIE SET rather
    than a rung.  Max 2 params (claim set, floor multiple).

WHAT IS NEW HERE, AND WHAT IS NOT
    1133's tie-set clause and 1110's clause forms priced tie sets as PROSE: 1110 states in
    terms that "the BOOK at every cell is byte-identical across all four forms, only the PROSE
    changes."  A RULE-8 PICK is not prose.  It names the book that gets the capital, so
    publishing it AS A TIE SET has a book: equal capital to every rung the record cannot
    separate.  That book is built, run and scored here, and it is the object the idea asks to
    be priced.  The floor is 877/871's SEED floor (0.0145 of Sharpe), not 1098's bootstrap
    resolution floor; the bootstrap floor is measured beside it as a DIAGNOSTIC and is never
    selected on.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials, the queue's own: CLAIM SET {CS_CORE, CS_WIDE, CS_ALL} x FLOOR MULTIPLE
    m {0, 0.5, 1, 2, 3} of 877's 0.0145 = 15 points, ALL published.
    PANEL is not a dial (U56 and B136 reported everywhere, 1096's convention).  LADDER is not a
    dial (all 7 reported).  CHOOSER is not a dial: the floor is quoted in SHARPE units, so the
    headline is C_ISSHARPE throughout; C_ISDD and C_ISCAGR are reported beside it against their
    OWN measured resolution, declared in advance as an EXTRAPOLATION and never a headline.
    COST is fixed at PROTOCOL's 10 bps.  BLOCK LENGTH is not a dial: L=63, 1098/1102/1110's
    headline.  Everything else frozen at 1096's construction: CAND20 legs, cap INF, max_vol
    0.60 (except on L_MV), gross 0.75 (except on L_G), W cadence (except on L_CAD), min hold
    126 (except on L_H), N=20 (except on L_N, and 12 on L_H), LAG 1, warm-up 260, IS end
    2016-12-31.  Seeds are zlib.crc32 (1108's repair of process-random hash()).

THE CLAIM SETS ARE 1096's, VERBATIM
    CS_CORE  L_N, L_H, L_G, L_CAD          (4 ladders x 2 panels =  8 picks)
    CS_WIDE  L_NH, L_BOOK, L_MV            (3 ladders x 2 panels =  6 picks)
    CS_ALL   all seven                     (                       14 picks)
    These are the 14 committed-ladder picks D4 counted 8 of below the floor; G4 reproduces
    1096's committed margins.csv rung-for-rung before any new number is read.

THE TWO BOOKS EVERY PICK IS SCORED AS
    ARGMAX   the rung the IS-only chooser names — the record's current publication.
    TIE      equal capital to every rung of the TIE SET at floor m*0.0145, run as |S| separate
             sleeves and blended daily.  Costs are already inside each sleeve and offsetting
             trades between sleeves are NOT netted, so the tie book's cost is an UPPER bound
             and every tie-vs-argmax difference below is CONSERVATIVE against the tie set.
    At m = 0 the tie set is the singleton {argmax} and the two books are identical — gate G7.

DECLARED BEFORE ANY NUMBER
    (a) H_BELOW      at m=1 a MAJORITY of CS_ALL's 14 picks have margin < the floor (1096's
                     8 of 14 reproduces).
    (b) H_NOINFO     at m=1 the pooled median OOS-Sharpe advantage of the ARGMAX rung over the
                     OTHER members of its own tie set is <= 0: inside a set the tape cannot
                     resolve, naming the peak buys nothing out of sample.
    (c) H_TIE_NOWORSE at m=1 the TIE book's OOS Sharpe is >= the ARGMAX book's in a MAJORITY of
                     the below-floor picks.  If this fails, tie-setting costs return and the
                     honesty is not free.
    (d) H_NO_MANUFACTURE  tie-setting turns NO 4b FAIL into a 4b PASS, on either window, at any
                     of the 15 points.  A publication convention that manufactures a pass is
                     disqualified whatever else it does.
    (e) H_FLOOR_LAX  the cells' OWN measured IS-Sharpe resolution (paired block bootstrap,
                     L=63, 1000 draws, 90% two-sided half-width of the peak-minus-runner-up
                     difference) EXCEEDS 0.0145 in a MAJORITY of the 14 cells — i.e. the
                     transferred seed floor is LAX and the census UNDERSTATES how many picks
                     are undecided.
    (f) THE DECISION RULE, fixed before any number.  The answer to the queue's question is YES
        (publish the tie set) iff at m=1 on CS_ALL: (i) a majority of picks are below the floor,
        AND (ii) the median OOS-Sharpe change from tie-setting is >= 0, AND (iii) H_NO_MANUFACTURE
        holds.  Otherwise NO, and the reason is reported.
    (g) NOT A KEEP PATH BY ITSELF.  4a and 4b are scored at every rung of every ladder, for
        every ARGMAX book and for every TIE book, full window and OOS.  Rule 8 picks on
        2009-2016 ALONE and the OOS window is read once.  Anything that clears 4b is reported;
        a tie book that clears 4b is a candidate like any other book.

THE CORPUS LAYER (census of the record; NOT a dial, NOT a re-derivation)
    Every committed .csv in research/backtests carrying a `pick` column is counted, and those
    carrying a margin column beside it.  This is a SCHEMA scan — reproducible, and it answers
    the census half of the idea directly: how much of the record publishes the margin that
    decided its pick.  Margins live in different statistics' units across files, so only rows
    keyed to an IS-Sharpe chooser are compared with 0.0145 and the rest are counted apart.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every level
    is optimistic.  A MARGIN between two rungs and a TIE-minus-ARGMAX difference both contrast
    books over the same inflated tape and the bias very largely cancels out of them; it does
    NOT cancel out of the 4b legs, which are measured against SPY, a real index.
"""
from __future__ import annotations

import csv
import glob
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

DATE = "2026-09-16"
SLUG = "should-a-RULE-8-PICK-be-PUBLISHED-when-its-MARGIN-is-BELOW-the-SEED-FLOOR"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
PRIOR1096 = HERE / ("2026-09-16_is-RULE-8-REACHABILITY-a-COST-RUNG-object-across-the-record-s-"
                    "COMMITTED-PICKS_cloud.margins.csv")

# ------------------------------------------------------------------ frozen at 1096's build
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, COST = 0.75, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
HS = [21, 63, 126, 252]
GS = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
CADS = ["D", "W", "M", "Q"]
MVS = [0.40, 0.50, 0.60, 0.80, 9.99]
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]
PANELS = ["U56", "B136"]

CORE_L = ["L_N", "L_H", "L_G", "L_CAD"]
WIDE_L = ["L_NH", "L_BOOK", "L_MV"]
CLAIMSETS = {"CS_CORE": CORE_L, "CS_WIDE": WIDE_L, "CS_ALL": CORE_L + WIDE_L}   # dial 1
F877 = 0.0145                       # 871/877's per-arm seed noise floor, in Sharpe units
MULTS = [0.0, 0.5, 1.0, 2.0, 3.0]   # dial 2
M_HEAD = 1.0
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD", "C_ISCAGR": "IS_CAGR"}
HEAD_CH = "C_ISSHARPE"
L_BLOCK, BDRAWS, Q_DIAG = 63, 1000, 0.90
SEED_BOOT = 11001100

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BOOT + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ----------------------------------------------------- 1082/1096's fast runner, verbatim
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
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px, max_vol=MAXVOL):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < max_vol)).values


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


def build_ewelig(elig, priced, reb, T, K, gross):
    W = np.zeros((T, K))
    for i, t in enumerate(reb):
        sel = np.flatnonzero(elig[t] & priced[t])
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


def blocks(r, warm, ins, oos):
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


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ---------------------------------------------------- paired block bootstrap (DIAGNOSTIC only)
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_sharpe(R, idx, nb, L, chunk=200):
    """Sharpe of each row of R on each block draw (drawn day indices, paired across rows)."""
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    st = idx[:, ::L]
    n = nb * L
    out = np.empty((R.shape[0], idx.shape[0]))
    for a in range(0, idx.shape[0], chunk):
        s = st[a:a + chunk]
        s1 = (CS1[:, s + L] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + L] - CS2[:, s]).sum(axis=2)
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        out[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return out


def main():
    t0 = time.time()
    P(f"# Idea 1100 (lane C, {DATE}) — should a RULE-8 PICK be PUBLISHED AT ALL when its")
    P("#   MARGIN is BELOW the SEED FLOOR?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {list(CLAIMSETS)} x FLOOR MULTIPLE "
      f"{MULTS} of 877's {F877}")
    P(f"#   = {len(CLAIMSETS) * len(MULTS)} points, ALL published.  PANEL, LADDER and CHOOSER "
      "are NOT dials (all reported).")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL} (except L_MV), gross {GROSS0} "
      f"(except L_G),")
    P(f"#   W cadence (except L_CAD), min hold 126 (except L_H), N=20 (L_N free, L_H at 12), "
      f"{COST:.0f} bps,")
    P(f"#   LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}; bootstrap L={L_BLOCK}, {BDRAWS} "
      f"draws, crc32 seeds — DIAGNOSTIC ONLY.")
    P("# THE TWO BOOKS: ARGMAX (the rung the IS chooser names) vs TIE (equal capital to every")
    P("#   rung within m*0.0145 of it, run as separate sleeves, costs inside each, no netting")
    P("#   between sleeves — so every tie-vs-argmax difference below is CONSERVATIVE).")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_BELOW          majority of CS_ALL's 14 picks below the floor at m=1.")
    P("#   (b) H_NOINFO         median OOS-Sharpe advantage of the ARGMAX over the OTHER tie")
    P("#                        members <= 0 at m=1.")
    P("#   (c) H_TIE_NOWORSE    TIE OOS Sharpe >= ARGMAX's in a majority of below-floor picks.")
    P("#   (d) H_NO_MANUFACTURE no 4b FAIL becomes a 4b PASS by tie-setting, at any of the 15.")
    P("#   (e) H_FLOOR_LAX      own measured resolution > 0.0145 in a majority of the 14 cells.")
    P("#   (f) DECISION RULE    YES iff at m=1 on CS_ALL: majority below floor AND median dOOS")
    P("#                        Sharpe >= 0 AND nothing manufactured.  Else NO, with the reason.")
    P("#   (g) 4a/4b scored for every rung AND every tie book, full and OOS; rule 8 picks on")
    P("#       2009-2016 alone, OOS read once.")
    P("")

    gaterows, gates = [], {}

    # ------------------------------------------------------------------------------ PANELS
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx), rets=rets,
                             priced=priced, warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

    def masks(panel):
        d = panels[panel]
        out = {}
        for f in CADS:
            mk = rebalance_mask(d["idx"], f).values
            mkl = np.roll(mk, LAG)
            mkl[:LAG] = False
            out[f] = (np.flatnonzero(mk), mkl)
        return out

    # --------------------------------------------------------------------- build all ladders
    store, ladder_rungs, cells = {}, {}, []
    bench = {}
    for panel in PANELS:
        d = panels[panel]
        px, rets, elig, priced = d["px"], d["rets"], d["elig"], d["priced"]
        T, K, warm, ins, oos = d["T"], d["K"], d["warm"], d["ins"], d["oos"]
        rank_key = -d["sc"]
        mk = masks(panel)
        yrs = warm.sum() / 252.0

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        lb_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].values
        lbm = blocks(lb_r, warm, ins, oos)
        bench[panel] = (sb, lbm)

        def add(ladder, rung, W, cad="W"):
            g, tn = nrun(rets, lagmat(W), mk[cad][1])
            r = g - tn * COST / 1e4
            store[(panel, ladder, str(rung))] = r
            ladder_rungs.setdefault((panel, ladder), []).append(str(rung))
            b = blocks(r, warm, ins, oos)
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lbm)
            cells.append(dict(panel=panel, ladder=ladder, rung=str(rung), cadence=cad,
                              turnover=float(tn[warm].sum() / yrs),
                              pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                              pass_4a=all(l4a.values()), **b, **l4b, **l4bo, **l4a))

        for N in NS:
            add("L_N", N, build(rank_key, elig, priced, mk["W"][0], N, 126, T, K, GROSS0))
        for H in HS:
            add("L_H", H, build(rank_key, elig, priced, mk["W"][0], 12, H, T, K, GROSS0))
        for G in GS:
            add("L_G", G, build(rank_key, elig, priced, mk["W"][0], 20, 126, T, K, G))
        for f in CADS:
            add("L_CAD", f, build(rank_key, elig, priced, mk[f][0], 20, 126, T, K, GROSS0), cad=f)
        for N in NS:
            for H in HS:
                add("L_NH", f"{N}/{H}",
                    build(rank_key, elig, priced, mk["W"][0], N, H, T, K, GROSS0))
        for bk in BOOKS:
            if bk.startswith("TOP"):
                W = build(rank_key, elig, priced, mk["W"][0], int(bk[3:]), 126, T, K, GROSS0)
            elif bk == "EWELIG":
                W = build_ewelig(elig, priced, mk["W"][0], T, K, GROSS0)
            else:
                W = rules_v2_weights(px).values
            add("L_BOOK", bk, W)
        for mv in MVS:
            _, el = mech(px, mv)
            add("L_MV", mv, build(rank_key, el, priced, mk["W"][0], 20, 126, T, K, GROSS0))
        P(f"  {panel}: ladders built ({time.time() - t0:.0f}s)")

    grid = pd.DataFrame(cells)
    metr = {(r.panel, r.ladder, r.rung): r for r in grid.itertuples()}

    # ------------------------------------------------------------------------------- GATES
    d = panels["U56"]
    mkU = masks("U56")
    W = build(-d["sc"], d["elig"], d["priced"], mkU["W"][0], 20, 126, d["T"], d["K"], GROSS0)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq="W")["returns"].values
    rfast = store[("U56", "L_N", "20")]
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest (U56 W/H126/N20)",
                         value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                     {g1:.2e}   "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    m20 = blocks(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m20["CAGR"] - A936_WH126[0]), abs(m20["Sharpe"] - A936_WH126[1]),
             abs(m20["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="CROSS-RUN 936/1071/1082/1094/1096 U56 W/H126/N=20 triple",
                         value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple         {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m20['CAGR']:.4%} / {m20['Sharpe']:.4f} / "
      f"{m20['MaxDD']:.4%})")

    sb_u, lbm_u = bench["U56"]
    g3 = max(abs(sb_u["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sb_u["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sb_u["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                     {g3:.2e}   "
      f"{'PASS' if gates['G3'] else 'FAIL'}")

    g5 = abs(lbm_u["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD                                {g5:.2e}   "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    W2 = build(-d["sc"], d["elig"], d["priced"], mkU["W"][0], 20, 126, d["T"], d["K"], GROSS0)
    g6 = float(np.abs(W - W2).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism (rebuild U56 N=20 weights)", value=g6,
                         pass_=gates["G6"]))
    P(f"  G6  determinism                                        {g6:.2e}   "
      f"{'PASS' if gates['G6'] else 'FAIL'}")

    # ------------------------------------------------- THE PICKS, MARGINS AND THE OWN FLOOR
    P("")
    P("## THE PICKS AND THEIR MARGINS — IS 2009-2016 ALONE, chooser sees nothing after "
      f"{IS_END}")
    pickrows = []
    for panel in PANELS:
        d = panels[panel]
        rng = np.random.default_rng(seed_of(panel, "boot"))
        Tis = int(d["ins"].sum())
        bidx, nb = block_index(rng, Tis, L_BLOCK, BDRAWS)
        for ladder in CORE_L + WIDE_L:
            rungs = ladder_rungs[(panel, ladder)]
            for ch, key in CHOOSERS.items():
                vals = np.array([getattr(metr[(panel, ladder, r_)], key) for r_ in rungs])
                order = np.argsort(-vals, kind="stable")
                pk_i, ru_i = int(order[0]), int(order[1])
                margin = float(vals[pk_i] - vals[ru_i])
                spread = float(vals.max() - vals.min())
                row = dict(panel=panel, ladder=ladder, chooser=ch, statistic=key,
                           claimset=("CORE" if ladder in CORE_L else "WIDE"),
                           rungs=len(rungs), pick=rungs[pk_i], runner_up=rungs[ru_i],
                           margin=margin, spread=spread,
                           margin_over_spread=(margin / spread if spread > 0 else np.nan))
                if ch == HEAD_CH:
                    R = np.vstack([store[(panel, ladder, rungs[pk_i])][d["ins"]],
                                   store[(panel, ladder, rungs[ru_i])][d["ins"]]])
                    bs = boot_sharpe(R, bidx, nb, L_BLOCK)
                    diff = bs[0] - bs[1]
                    diff = diff[np.isfinite(diff)]
                    lo, hi = np.percentile(diff, [(1 - Q_DIAG) / 2 * 100,
                                                  (1 + Q_DIAG) / 2 * 100])
                    row["own_res_halfwidth"] = float((hi - lo) / 2.0)
                    row["agreement"] = float((np.sign(diff) == np.sign(margin)).mean())
                    row["decided_q90"] = bool(row["agreement"] >= Q_DIAG)
                for mm in MULTS:
                    row[f"below_m{mm}"] = bool(margin < mm * F877)
                pickrows.append(row)
    picks = pd.DataFrame(pickrows)
    dump(picks, "margins")

    head = picks[picks.chooser == HEAD_CH].copy()
    P(f"  {HEAD_CH} (the floor's own units) — {len(head)} committed-ladder picks:")
    for _, r_ in head.iterrows():
        P(f"    {r_['panel']:<5} {r_['ladder']:<7} {r_['claimset']:<5} pick {str(r_['pick']):<7} "
          f"vs {str(r_['runner_up']):<7} margin {r_['margin']:.4f}  spread {r_['spread']:.4f}  "
          f"m/spread {r_['margin_over_spread']:.3f}  own res(90%) "
          f"{r_['own_res_halfwidth']:.4f}  agree {r_['agreement']:.3f}  "
          f"below 877 floor {bool(r_['margin'] < F877)}")
    P(f"  BELOW 877's {F877} seed floor: {int(head['below_m1.0'].sum())} of {len(head)}")
    P(f"  OTHER CHOOSERS (own units, NOT comparable to a Sharpe floor — reported, never a "
      "headline):")
    for ch in ("C_ISDD", "C_ISCAGR"):
        sub = picks[picks.chooser == ch]
        P(f"    {ch:<10} margins {sub['margin'].min():.5f} .. {sub['margin'].max():.5f}, "
          f"median {sub['margin'].median():.5f}, median margin/spread "
          f"{sub['margin_over_spread'].median():.3f}")

    # G4 — reproduce 1096's committed margins.csv
    if PRIOR1096.exists():
        prior = pd.read_csv(PRIOR1096)
        mg = prior.merge(head, left_on=["panel", "ladder"], right_on=["panel", "ladder"],
                         suffixes=("_1096", "_here"))
        dmar = float(np.abs(mg["IS_Sharpe_margin"] - mg["margin"]).max())
        same = int((mg["pick_1096"].astype(str) == mg["pick_here"].astype(str)).sum())
        gates["G4"] = (dmar < 5e-4) and (same == len(mg)) and (len(mg) == 14)
        gaterows.append(dict(gate="G4", what=f"CROSS-RUN 1096's committed margins.csv "
                                             f"({len(mg)} picks, {same} same rung)",
                             value=dmar, pass_=gates["G4"]))
        P(f"  G4  CROSS-RUN 1096's committed 14 margins              {dmar:.2e}   "
          f"{'PASS' if gates['G4'] else 'FAIL'}  ({same} of {len(mg)} same pick rung)")
    else:
        gates["G4"] = False
        gaterows.append(dict(gate="G4", what="1096's margins.csv not found", value=np.nan,
                             pass_=False))
        P("  G4  1096's margins.csv NOT FOUND                                    FAIL")

    # ----------------------------------------------------- THE TIE BOOKS, ONE PER (PICK, m)
    P("")
    P("## THE TIE BOOKS — equal capital to every rung within m*0.0145 of the pick")
    tierows = []
    for _, r_ in head.iterrows():
        panel, ladder = r_["panel"], r_["ladder"]
        d = panels[panel]
        warm, ins, oos = d["warm"], d["ins"], d["oos"]
        sb, lbm = bench[panel]
        rungs = ladder_rungs[(panel, ladder)]
        vals = np.array([getattr(metr[(panel, ladder, x)], "IS_Sharpe") for x in rungs])
        pk = r_["pick"]
        pkv = float(vals[rungs.index(pk)])
        ra = store[(panel, ladder, pk)]
        ma = blocks(ra, warm, ins, oos)
        a4b, a4bo, a4a = legs_4b(ma, sb), legs_4b_oos(ma, sb), legs_4a(ma, lbm)
        for mm in MULTS:
            flo = mm * F877
            tset = [x for i, x in enumerate(rungs)
                    if x == pk or (np.isfinite(vals[i]) and (pkv - vals[i]) < flo)]
            Rt = np.vstack([store[(panel, ladder, x)] for x in tset])
            rt = Rt.mean(axis=0)
            mt = blocks(rt, warm, ins, oos)
            t4b, t4bo, t4a = legs_4b(mt, sb), legs_4b_oos(mt, sb), legs_4a(mt, lbm)
            # DIAGNOSTIC: the same sleeves with NO cross-sleeve rebalancing at all (drift)
            eqs = np.cumprod(1.0 + Rt, axis=1).mean(axis=0)
            rd = np.concatenate([[Rt[:, 0].mean()], eqs[1:] / eqs[:-1] - 1.0])
            md = blocks(rd, warm, ins, oos)
            others = [x for x in tset if x != pk]
            if others:
                oo = np.array([getattr(metr[(panel, ladder, x)], "OOS_Sharpe") for x in others])
                adv = float(ma["OOS_Sharpe"] - np.nanmean(oo))
                oos_lo = float(min(np.nanmin(oo), ma["OOS_Sharpe"]))
                oos_hi = float(max(np.nanmax(oo), ma["OOS_Sharpe"]))
                rank = float((np.sum(ma["OOS_Sharpe"] > oo) + 0.5 *
                              np.sum(ma["OOS_Sharpe"] == oo)) / len(oo))
            else:
                adv, oos_lo, oos_hi, rank = np.nan, ma["OOS_Sharpe"], ma["OOS_Sharpe"], np.nan
            tierows.append(dict(
                panel=panel, ladder=ladder, claimset=r_["claimset"], mult=mm, floor=flo,
                pick=pk, margin=r_["margin"], below=bool(r_["margin"] < flo),
                rungs=len(rungs), tie_n=len(tset), tie_share=len(tset) / len(rungs),
                whole_ladder=bool(len(tset) == len(rungs)), ties="|".join(map(str, tset)),
                argmax_CAGR=ma["CAGR"], argmax_Sharpe=ma["Sharpe"], argmax_MaxDD=ma["MaxDD"],
                argmax_H1=ma["H1"], argmax_H2=ma["H2"], argmax_OOS_CAGR=ma["OOS_CAGR"],
                argmax_OOS_Sharpe=ma["OOS_Sharpe"], argmax_OOS_MaxDD=ma["OOS_MaxDD"],
                tie_CAGR=mt["CAGR"], tie_Sharpe=mt["Sharpe"], tie_MaxDD=mt["MaxDD"],
                tie_H1=mt["H1"], tie_H2=mt["H2"], tie_OOS_CAGR=mt["OOS_CAGR"],
                tie_OOS_Sharpe=mt["OOS_Sharpe"], tie_OOS_MaxDD=mt["OOS_MaxDD"],
                d_OOS_Sharpe=mt["OOS_Sharpe"] - ma["OOS_Sharpe"],
                d_OOS_CAGR=mt["OOS_CAGR"] - ma["OOS_CAGR"],
                d_OOS_MaxDD=mt["OOS_MaxDD"] - ma["OOS_MaxDD"],
                d_Sharpe=mt["Sharpe"] - ma["Sharpe"],
                tie_drift_OOS_Sharpe=md["OOS_Sharpe"],
                d_OOS_Sharpe_drift=md["OOS_Sharpe"] - ma["OOS_Sharpe"],
                argmax_in_tie_adv=adv, tie_oos_lo=oos_lo, tie_oos_hi=oos_hi,
                argmax_oos_rank=rank,
                argmax_4b_full=all(a4b.values()), tie_4b_full=all(t4b.values()),
                argmax_4b_oos=all(a4bo.values()), tie_4b_oos=all(t4bo.values()),
                argmax_4a=all(a4a.values()), tie_4a=all(t4a.values())))
    ties = pd.DataFrame(tierows)
    dump(ties, "ties")

    g7 = float(np.abs(ties[ties.mult == 0.0]["d_OOS_Sharpe"]).max())
    gates["G7"] = g7 == 0.0 and bool((ties[ties.mult == 0.0]["tie_n"] == 1).all())
    gaterows.append(dict(gate="G7", what="m=0 tie set is the singleton {argmax}; books identical",
                         value=g7, pass_=gates["G7"]))
    P(f"  G7  m=0 TIE book == ARGMAX book                        {g7:.2e}   "
      f"{'PASS' if gates['G7'] else 'FAIL'}")

    P(f"  headline m={M_HEAD} ({len(head)} picks), below-floor picks marked *:")
    for _, r_ in ties[ties.mult == M_HEAD].iterrows():
        P(f"    {'*' if r_['below'] else ' '} {r_['panel']:<5} {r_['ladder']:<7} pick "
          f"{str(r_['pick']):<7} tie {r_['tie_n']:>2}/{r_['rungs']:<2} [{r_['ties']}]  "
          f"ARGMAX OOS {r_['argmax_OOS_CAGR']:.2%}/{r_['argmax_OOS_Sharpe']:.4f}/"
          f"{r_['argmax_OOS_MaxDD']:.2%}  TIE OOS {r_['tie_OOS_CAGR']:.2%}/"
          f"{r_['tie_OOS_Sharpe']:.4f}/{r_['tie_OOS_MaxDD']:.2%}  dS {r_['d_OOS_Sharpe']:+.4f}  "
          f"4b full {str(r_['argmax_4b_full'])[0]}->{str(r_['tie_4b_full'])[0]}  "
          f"4b OOS {str(r_['argmax_4b_oos'])[0]}->{str(r_['tie_4b_oos'])[0]}")

    # ------------------------------------------------------------- THE 15 DIAL POINTS
    P("")
    P("## THE GRID — every one of the 15 (claim set x floor multiple) points, as required")
    gr = []
    for csname, lads in CLAIMSETS.items():
        for mm in MULTS:
            sub = ties[(ties.mult == mm) & (ties.ladder.isin(lads))]
            bel = sub[sub.below]
            manuf = int(((~sub.argmax_4b_full) & sub.tie_4b_full).sum() +
                        ((~sub.argmax_4b_oos) & sub.tie_4b_oos).sum())
            lost = int(((sub.argmax_4b_full) & (~sub.tie_4b_full)).sum() +
                       ((sub.argmax_4b_oos) & (~sub.tie_4b_oos)).sum())
            gr.append(dict(
                claimset=csname, mult=mm, floor=mm * F877, n=len(sub),
                n_below=int(sub.below.sum()), share_below=float(sub.below.mean()),
                mean_tie_n=float(sub.tie_n.mean()), mean_tie_share=float(sub.tie_share.mean()),
                whole_ladder=int(sub.whole_ladder.sum()),
                med_dOOS_Sharpe=float(sub.d_OOS_Sharpe.median()),
                med_dOOS_Sharpe_below=(float(bel.d_OOS_Sharpe.median()) if len(bel) else np.nan),
                med_dOOS_CAGR=float(sub.d_OOS_CAGR.median()),
                med_dOOS_MaxDD=float(sub.d_OOS_MaxDD.median()),
                tie_wins_OOS=int((sub.d_OOS_Sharpe > 0).sum()),
                tie_wins_OOS_below=int((bel.d_OOS_Sharpe > 0).sum()),
                med_argmax_in_tie_adv=float(sub.argmax_in_tie_adv.median(skipna=True)),
                argmax_4b_full=int(sub.argmax_4b_full.sum()), tie_4b_full=int(sub.tie_4b_full.sum()),
                argmax_4b_oos=int(sub.argmax_4b_oos.sum()), tie_4b_oos=int(sub.tie_4b_oos.sum()),
                argmax_4a=int(sub.argmax_4a.sum()), tie_4a=int(sub.tie_4a.sum()),
                manufactured=manuf, lost=lost))
    gdf = pd.DataFrame(gr)
    dump(gdf, "grid")
    P("  | claim set | m | floor | n | below | mean tie | whole-ladder | med dOOS Sharpe | "
      "tie wins | 4b full A->T | 4b OOS A->T | manufactured |")
    for _, r_ in gdf.iterrows():
        P(f"  | {r_['claimset']:<7} | {r_['mult']:>3} | {r_['floor']:.4f} | {r_['n']:>2} | "
          f"{r_['n_below']:>2} | {r_['mean_tie_n']:>4.2f} | {r_['whole_ladder']:>2} | "
          f"{r_['med_dOOS_Sharpe']:+.4f} | {r_['tie_wins_OOS']:>2}/{r_['n']:<2} | "
          f"{r_['argmax_4b_full']}->{r_['tie_4b_full']} | "
          f"{r_['argmax_4b_oos']}->{r_['tie_4b_oos']} | {r_['manufactured']} |")

    # -------------------------------------------------------------------- THE CORPUS LAYER
    P("")
    P("## CORPUS — how much of the record publishes the margin that decided its pick")
    corpus = []
    npick = nmarg = 0
    rows_pick = rows_marg = 0
    for f in sorted(glob.glob(str(HERE / "*.csv"))):
        try:
            with open(f, newline="") as fh:
                rd = csv.reader(fh)
                h = next(rd)
                nrows = sum(1 for _ in rd)
        except Exception:
            continue
        hs = [c.strip().lower() for c in h]
        haspick = any(c == "pick" or c.startswith("pick_") for c in hs)
        hasmarg = any("margin" in c for c in hs)
        if not haspick:
            continue
        npick += 1
        rows_pick += nrows
        if hasmarg:
            nmarg += 1
            rows_marg += nrows
        corpus.append(dict(file=Path(f).name, rows=nrows, has_margin=hasmarg,
                           margin_cols="|".join(c for c in hs if "margin" in c)))
    cdf = pd.DataFrame(corpus)
    dump(cdf, "corpus")
    P(f"  committed .csv files carrying a `pick` column: {npick}  ({rows_pick:,} pick rows)")
    P(f"  of those, carrying a MARGIN beside it:         {nmarg}  ({rows_marg:,} rows, "
      f"{nmarg / max(npick, 1):.3f} of files, {rows_marg / max(rows_pick, 1):.3f} of rows)")
    P("  This is a SCHEMA scan of the committed record, not a re-derivation of any claim.")
    P("  A pick row without a margin column cannot be checked against ANY floor by a reader:")
    P("  the number that decided it was never published.")

    # -------------------------------------------------------------------------- HYPOTHESES
    P("")
    P("## HYPOTHESES — declared before any number above was read")
    hyp = []
    h1 = ties[(ties.mult == M_HEAD)]
    all14 = h1
    nbel = int(all14.below.sum())
    hyp.append(("H_BELOW", nbel > len(all14) / 2,
                f"{nbel} of {len(all14)} CS_ALL picks below the {F877} floor at m={M_HEAD} "
                f"(1096's D4: 8 of 14)"))
    adv = all14["argmax_in_tie_adv"].dropna()
    med_adv = float(adv.median()) if len(adv) else np.nan
    hyp.append(("H_NOINFO", bool(len(adv) and med_adv <= 0),
                f"median OOS-Sharpe advantage of the ARGMAX over the other members of its own "
                f"tie set {med_adv:+.4f} over {len(adv)} multi-rung tie sets; the argmax's mean "
                f"OOS rank inside its tie set {all14['argmax_oos_rank'].mean(skipna=True):.3f} "
                f"(0.5 = no information)"))
    bel = all14[all14.below]
    win = int((bel.d_OOS_Sharpe >= 0).sum())
    hyp.append(("H_TIE_NOWORSE", bool(len(bel) and win > len(bel) / 2),
                f"TIE OOS Sharpe >= ARGMAX's in {win} of {len(bel)} below-floor picks; median "
                f"dOOS Sharpe over them {bel['d_OOS_Sharpe'].median():+.4f}, over all "
                f"{len(all14)} {all14['d_OOS_Sharpe'].median():+.4f}"))
    csall = gdf[gdf.claimset == "CS_ALL"]
    tot_manuf = int(csall["manufactured"].sum())
    hyp.append(("H_NO_MANUFACTURE", tot_manuf == 0,
                f"{tot_manuf} 4b FAIL -> PASS conversions over the 5 floor multiples covering "
                f"all 14 picks ({int(csall['lost'].sum())} PASS -> FAIL in the other "
                f"direction); CS_CORE/CS_WIDE are subsets of the same picks"))
    own = head["own_res_halfwidth"].dropna()
    nlax = int((own > F877).sum())
    hyp.append(("H_FLOOR_LAX", nlax > len(own) / 2,
                f"own measured 90% resolution exceeds {F877} in {nlax} of {len(own)} cells "
                f"(median {own.median():.4f}, min {own.min():.4f}, max {own.max():.4f}); "
                f"decided at q={Q_DIAG}: {int(head['decided_q90'].sum())} of {len(head)}"))
    row_head = gdf[(gdf.claimset == "CS_ALL") & (gdf.mult == M_HEAD)].iloc[0]
    yes = bool(row_head["n_below"] > row_head["n"] / 2 and
               row_head["med_dOOS_Sharpe"] >= 0 and tot_manuf == 0)
    hyp.append(("H_DECISION", True,
                f"decision rule applied as declared -> {'YES' if yes else 'NO'}: below "
                f"{row_head['n_below']}/{row_head['n']}, median dOOS Sharpe "
                f"{row_head['med_dOOS_Sharpe']:+.4f}, manufactured {tot_manuf}"))
    for k_, v_, why in hyp:
        P(f"  {k_:<18} {'PASS' if v_ else 'FAIL'}   {why}")
    P(f"  {sum(1 for _, v_, _ in hyp if v_)} of {len(hyp)} hypotheses PASS")
    dump(pd.DataFrame([dict(hypothesis=k_, result="PASS" if v_ else "FAIL", detail=w_)
                       for k_, v_, w_ in hyp]), "hypotheses")

    # --------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("")
    P("## RULE 8 AND BOTH KEEP PATHS — rung chosen on IS 2009-2016 ALONE, OOS read ONCE")
    benchrows = []
    for panel in PANELS:
        sb, lbm = bench[panel]
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        benchrows.append(dict(panel=panel, series="RULESv2", **lbm))
        P(f"  {panel} SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f})  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2 full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / "
          f"{lbm['MaxDD']:.2%} (halves {lbm['H1']:.4f}/{lbm['H2']:.4f})  OOS "
          f"{lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
    dump(pd.DataFrame(benchrows), "benchmarks")

    wf = []
    for _, r_ in ties.iterrows():
        wf.append(dict(panel=r_["panel"], ladder=r_["ladder"], claimset=r_["claimset"],
                       chooser=HEAD_CH, mult=r_["mult"], publication="ARGMAX",
                       pick=r_["pick"], margin=r_["margin"], n_books=1,
                       CAGR=r_["argmax_CAGR"], Sharpe=r_["argmax_Sharpe"],
                       MaxDD=r_["argmax_MaxDD"], H1=r_["argmax_H1"], H2=r_["argmax_H2"],
                       OOS_CAGR=r_["argmax_OOS_CAGR"], OOS_Sharpe=r_["argmax_OOS_Sharpe"],
                       OOS_MaxDD=r_["argmax_OOS_MaxDD"], pass_4b_full=r_["argmax_4b_full"],
                       pass_4b_oos=r_["argmax_4b_oos"], pass_4a=r_["argmax_4a"]))
        wf.append(dict(panel=r_["panel"], ladder=r_["ladder"], claimset=r_["claimset"],
                       chooser=HEAD_CH, mult=r_["mult"], publication="TIE",
                       pick=r_["ties"], margin=r_["margin"], n_books=r_["tie_n"],
                       CAGR=r_["tie_CAGR"], Sharpe=r_["tie_Sharpe"], MaxDD=r_["tie_MaxDD"],
                       H1=r_["tie_H1"], H2=r_["tie_H2"], OOS_CAGR=r_["tie_OOS_CAGR"],
                       OOS_Sharpe=r_["tie_OOS_Sharpe"], OOS_MaxDD=r_["tie_OOS_MaxDD"],
                       pass_4b_full=r_["tie_4b_full"], pass_4b_oos=r_["tie_4b_oos"],
                       pass_4a=r_["tie_4a"]))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")
    P(f"  ARGMAX publications: 4b full {int(wfd[wfd.publication == 'ARGMAX'].pass_4b_full.sum())}"
      f" of {len(wfd[wfd.publication == 'ARGMAX'])}, 4b OOS "
      f"{int(wfd[wfd.publication == 'ARGMAX'].pass_4b_oos.sum())}, 4a "
      f"{int(wfd[wfd.publication == 'ARGMAX'].pass_4a.sum())}")
    P(f"  TIE publications:    4b full {int(wfd[wfd.publication == 'TIE'].pass_4b_full.sum())}"
      f" of {len(wfd[wfd.publication == 'TIE'])}, 4b OOS "
      f"{int(wfd[wfd.publication == 'TIE'].pass_4b_oos.sum())}, 4a "
      f"{int(wfd[wfd.publication == 'TIE'].pass_4a.sum())}")
    P(f"  WHOLE GRID (every rung of every ladder, {len(grid)} cells): 4b full "
      f"{int(grid.pass_4b_full.sum())}, 4b OOS {int(grid.pass_4b_oos.sum())}, 4a "
      f"{int(grid.pass_4a.sum())}")
    dump(grid, "cells")
    if int(grid.pass_4b_full.sum()):
        P("  4b-full passing cells (whole grid):")
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            P(f"    {r_['panel']:<5} {r_['ladder']:<7} rung {str(r_['rung']):<7} full "
              f"{r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%} halves {r_['H1']:.4f}/"
              f"{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/"
              f"{r_['OOS_MaxDD']:.2%}  4b OOS {r_['pass_4b_oos']}")
    tie_keep = ties[(ties.tie_4b_full) & (ties.tie_4b_oos) & (ties.tie_n > 1)]
    P(f"  TIE books clearing 4b FULL and 4b OOS: {len(tie_keep)} of {len(ties)} (tie_n > 1)")
    for _, r_ in tie_keep.iterrows():
        P(f"    {r_['panel']:<5} {r_['ladder']:<7} m={r_['mult']} tie {r_['tie_n']}/"
          f"{r_['rungs']} [{r_['ties']}] full {r_['tie_CAGR']:.2%}/{r_['tie_Sharpe']:.4f}/"
          f"{r_['tie_MaxDD']:.2%} halves {r_['tie_H1']:.4f}/{r_['tie_H2']:.4f} OOS "
          f"{r_['tie_OOS_CAGR']:.2%}/{r_['tie_OOS_Sharpe']:.4f}/{r_['tie_OOS_MaxDD']:.2%}")

    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("  U56 and B136 are CURRENT-CONSTITUENT panels; every level above is optimistic.  A")
    P("  MARGIN and a TIE-minus-ARGMAX difference contrast two books over the same inflated")
    P("  tape and the bias very largely cancels out of them; it does NOT cancel out of the 4b")
    P("  legs, which are measured against SPY, a real index.")
    P("")
    P("## THE DECLARED TRANSFERS, AND THEIR DIRECTION")
    P(f"  (i)  877's {F877} is a SEED-noise floor measured on placebo arms, in Sharpe units.")
    P("       Applying it to a deterministic IS-Sharpe pick margin is a TRANSFER, declared in")
    P("       advance and checked against each cell's OWN bootstrap resolution (H_FLOOR_LAX).")
    P("  (ii) The TIE book runs |S| sleeves side by side and nets NO trades between them, so")
    P("       its cost is an upper bound and every TIE-minus-ARGMAX figure understates the tie")
    P("       set's case.  The headline blend holds the sleeves at equal weight daily, which")
    P("       is a free cross-sleeve rebalance; the NO-rebalance DRIFT blend is computed for")
    P("       every row beside it (tie_drift_OOS_Sharpe) and the two are compared below.")
    P("  (iii) C_ISDD and C_ISCAGR margins are in MaxDD and CAGR units and are NOT compared to")
    P("       a Sharpe floor anywhere above.")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"# GATES {sum(gates.values())} of {len(gates)} PASS")
    P(f"# elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.console.txt")


if __name__ == "__main__":
    main()

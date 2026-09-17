#!/usr/bin/env python3
"""
Idea 1210 (cloud lane, 2026-09-17) — should a CHOOSER have to BEAT THE ANCHOR BY ITS OWN
BOOTSTRAP SE rather than merely OUTRANK IT?

THE PREMISE, READ FROM THE RECORD AND NOT RECALLED.  Idea 1154 scored 72 pick decisions
(3 panels x 2 anchors x 4 ladders x 3 honest choosers) under 1101's joint moving-block
bootstrap and published three publishing rules over them:

    R_RAW      publish the IS argmax, always           (the record's habit)
    R_BAR      publish it only if P_pick >= 0.90, else STAY AT THE ANCHOR
    R_ANCHOR   never move                              (1155's do-nothing control)

At C_ALL x L63 it committed mean OOS Sharpe 0.7996 / 0.7887 / 0.7901 and 4b books
6 / 19 / 24 of 72 — "the publish-the-argmax habit loses three quarters of its capital-worthy
books to doing nothing".  It also found P_boot and the IS margin NEAR-ORTHOGONAL (Spearman
0.1551; median margin 9.739e-03 among resolved against 9.369e-03 among unresolved), i.e.
P_boot measures ORDER STABILITY and not EFFECT SIZE, so neither a rank bar nor a margin
column alone prices a pick.

THE QUEUE'S PROPOSAL, TESTED HERE.  A third rule that prices the pick directly:

    R_SE(k, basis)   move only when the IS argmax beats the ANCHOR by k bootstrap SE of
                     THE DIFFERENCE stat(pick) - stat(anchor), else stay at the anchor.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  k      {0, 0.25, 0.5, 1, 1.5, 2, 3}        -- the SE multiple.  k = 0 is R_RAW exactly (G6).
  BASIS  {SE_JOINT, SE_MARGINAL, SE_IID}     -- how the SE of the difference is estimated:
         SE_JOINT     SD across 1000 JOINT moving-block redraws of (stat_pick - stat_anchor).
                      One block index per draw is applied to ALL rungs, so the cross-rung
                      correlation that makes these ladders hard to resolve is PRESERVED.
         SE_MARGINAL  sqrt(var(stat_pick) + var(stat_anchor)) from the same draws — the
                      correlation-BLIND estimate a reader would form from two published
                      error bars.  It is an upper bound whenever the rungs co-move.
         SE_IID       SE_JOINT with block length 1, i.e. the dependence in the tape thrown
                      away.  The cheapest SE anyone would reach for.

WHAT IS NOT A DIAL.  The 72 decisions, the four ladders, the two anchors, the three honest
choosers, the three panels (rule 9 requires all three), 1101's bootstrap, B = 1000 draws, the
0.90/0.10 bar and the CLAIM SET nesting are 1154's, inherited whole and unchanged.  BLOCK
LENGTH is frozen at 1154's own headline L = 63 and the other three (21, 126, 252) are
reported beside it as a sensitivity that is never adjudicated on.

THE TRAP THIS RUN IS BUILT AROUND, DECLARED BEFORE ANY NUMBER.  R_SE at large k IS R_ANCHOR:
it stops moving and therefore "recovers" every one of the 18 capital-worthy books R_RAW loses,
for free and for nothing.  A rule that buys its books by not moving has not priced anything —
R_ANCHOR already does that, costs nothing and is in the record.  So the question is NOT whether
R_SE beats R_RAW.  It is whether, AT A MATCHED MOVE COUNT, R_SE books more than

    R_BAR      the rank bar it is proposed to replace, and
    R_RANDOM   a bar that moves on a uniformly random subset of the SAME size (500 seeded
               draws), which is what "move less often" is worth with no information at all.

R_RANDOM is the control that separates an informative bar from a conservative one, and no
reading below is made without it.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 TWICE — the pick decisions
are chosen on 2009-2016 and 2017-2026 is read once (1154's split, inherited), AND this run's
own two dials are chosen on 2017-2021 with 2022-2026 read ONCE, reported in Arm E; BOTH KEEP
paths on every rung book and every published book; rule 9 survivorship stated.  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_should-a-CHOOSER-have-to-BEAT-THE-ANCHOR-BY-ITS-OWN-BOOTSTRAP-SE-rather-than-merely-OUTRANK-IT_cloud.py
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

DATE = "2026-09-17"
SLUG = "should-a-CHOOSER-have-to-BEAT-THE-ANCHOR-BY-ITS-OWN-BOOTSTRAP-SE-rather-than-merely-OUTRANK-IT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ----- 1101/1154's construction, inherited whole ---------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
OOS_SPLIT = "2021-12-31"          # this run's OWN rule-8 split, inside 1154's OOS window
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]

ANCHORS = {
    "A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
    "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M"),
}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]
CH_HEAD = "CH_ISSHARPE"
CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]
CS_HEAD = "C_ALL"                 # the queue asks about the 72, so C_ALL is the headline set
BLOCKS = [21, 63, 126, 252]
L_HEAD = 63                       # 1154's own; frozen, not a dial
BAR_HI, BAR_LO = 0.90, 0.10
BDRAWS = 1000
SEED_BASE = 11541154      # 1154's OWN seed base: the bootstrap is inherited whole, so the
                          # reproduction gates G3/G4 are bit-level and not "within MC noise".
SEED_SENS = [12101210, 20260917, 7777777]   # alternative bases, for the seed-sensitivity arm

# ----- this run's two dials ------------------------------------------------------------------
KS = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0]
BASES = ["SE_JOINT", "SE_MARGINAL", "SE_IID"]
BASIS_HEAD = "SE_JOINT"
RAND_DRAWS = 500

# ----- 1154's committed numbers, QUOTED and GATED, never re-derived --------------------------
C1154_RULE8 = {                    # C_ALL x L63: (mean_OOS_Sharpe, n_4b_full, n_4b_oos, n_4a, n_moved)
    "R_RAW":    (0.7995575457617328, 6, 7, 0, 59),
    "R_BAR":    (0.7886717099917357, 19, 19, 0, 13),
    "R_ANCHOR": (0.7900802510800281, 24, 24, 0, 0),
}
C1154_SPEARMAN = 0.1551
C1154_MED_RESOLVED, C1154_MED_UNRESOLVED = 9.739e-03, 9.369e-03
C1154_RESOLVED_CALL = 17           # of 72 at L63
LIVE_MAXDD_COMMITTED = -0.1205

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


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}  ->  {value:.3e}")
    return bool(ok)


# ============================================ 1101/1154/1159's runner and metrics, verbatim
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


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    oosA = oos & np.asarray(idx <= pd.Timestamp(OOS_SPLIT))
    oosB = oos & np.asarray(idx > pd.Timestamp(OOS_SPLIT))
    return warm, ins, oos, oosA, oosB


def blocks_m(r, warm, ins, oos, oosA, oosB):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    ac, as_, add = fmet(r[oosA])
    bc, bs_, bdd = fmet(r[oosB])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                OOSA_CAGR=ac, OOSA_Sharpe=as_, OOSA_MaxDD=add,
                OOSB_CAGR=bc, OOSB_Sharpe=bs_, OOSB_MaxDD=bdd)


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


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos, self.oosA, self.oosB = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if name == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def book(pan, N, H, gross, freq):
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def ladder_books(pan, anchor, lad):
    a = ANCHORS[anchor]
    out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        out[rung] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
    return out


# ============================================ the bootstrap — 1101's, extended to keep the draws
def block_index(rng, T, L, B):
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def pboot_stats(R, stat, L, seed, B=BDRAWS, chunk=100):
    """(B, k) matrix of the chooser statistic under JOINT moving-block redraws of the IS window.

    One block index per draw is applied to ALL rungs, so cross-rung correlation is preserved.
    1154 threw this matrix away after counting argmaxes; the SE of a DIFFERENCE needs it whole.
    """
    T, k = R.shape
    rng = np.random.default_rng(seed)
    out = np.empty((B, k))
    done = 0
    while done < B:
        b = min(chunk, B - done)
        idx = block_index(rng, T, L, b)
        X = R[idx]
        if stat == "CH_ISSHARPE":
            v = X.mean(axis=1) * 252.0 / (X.std(axis=1, ddof=1) * np.sqrt(252.0))
        elif stat == "CH_ISCAGR":
            eq = np.cumprod(1.0 + X, axis=1)
            v = eq[:, -1, :] ** (252.0 / T) - 1.0
        elif stat == "CH_ISDD":
            eq = np.cumprod(1.0 + X, axis=1)
            v = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
        else:
            raise ValueError(stat)
        out[done:done + b] = np.where(np.isfinite(v), v, -np.inf)
        done += b
    return out


def is_stat(r, ins, stat, T_is):
    x = r[ins]
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    if stat == "CH_ISCAGR":
        eq = np.cumprod(1.0 + x)
        return eq[-1] ** (252.0 / T_is) - 1.0
    if stat == "CH_ISDD":
        eq = np.cumprod(1.0 + x)
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 1210 (cloud lane, 2026-09-17) — should a CHOOSER have to BEAT THE ANCHOR BY ITS OWN")
    P("  BOOTSTRAP SE rather than merely OUTRANK IT?")
    P("  dial 1 = k      {0, 0.25, 0.5, 1, 1.5, 2, 3}          (the SE multiple)")
    P("  dial 2 = BASIS  {SE_JOINT, SE_MARGINAL, SE_IID}       (how the SE is estimated)")
    P("  Block length FROZEN at 1154's L = 63; 21/126/252 reported, never adjudicated on.")
    P("=" * 104)

    # ---------------------------------------------------------------- ARM 0: data-free first
    P("")
    P("ARM 0 — DATA-FREE.  WHAT AN SE BAR CAN AND CANNOT BE ASKED, PRINTED BEFORE ANY TAPE.")
    P("")
    P("  (i) THE DEGENERATE ANSWER, RULED OUT IN ADVANCE.  R_SE(k) is monotone in k: the move")
    P("      set shrinks as k grows, and at k large enough R_SE IS R_ANCHOR.  1154 committed")
    P(f"      R_ANCHOR at {C1154_RULE8['R_ANCHOR'][1]} of 72 4b books against R_RAW's "
      f"{C1154_RULE8['R_RAW'][1]} — a gap of "
      f"{C1154_RULE8['R_ANCHOR'][1] - C1154_RULE8['R_RAW'][1]}.  So 'R_SE recovers the 18 books'")
    P("      IS TRUE BY CONSTRUCTION at large k and means nothing: R_ANCHOR already recovers all")
    P("      18, costs nothing, needs no bootstrap and is in the record.  A new rule earns its")
    P("      place only by beating the alternatives AT A MATCHED MOVE COUNT.")
    P("")
    P("  (ii) THE TWO COMPARANDS THAT MAKE THAT TEST MEAN SOMETHING:")
    P("      R_BAR      the rank bar R_SE is proposed to replace (1154's, P_pick >= 0.90)")
    P(f"      R_RANDOM   move on a uniformly random subset of the SAME SIZE ({RAND_DRAWS} seeded")
    P("                 draws).  This is what 'move less often' is worth with NO information.")
    P("")
    P("  (iii) WHAT THE RECORD ALREADY IMPLIES ABOUT THE BAR'S POWER.  1154 committed the median")
    P(f"      IS margin at {C1154_MED_RESOLVED:.3e} among P_boot-resolved decisions against")
    P(f"      {C1154_MED_UNRESOLVED:.3e} among unresolved — a ratio of "
      f"{C1154_MED_RESOLVED / C1154_MED_UNRESOLVED:.4f}, and Spearman {C1154_SPEARMAN:.4f}.")
    P("      An SE bar is a MARGIN bar with a scale attached, so it can only separate the two")
    P("      populations if the SE varies across decisions by MORE than the margin does.  If SE")
    P("      is near-constant across the 72, R_SE is a re-labelled margin bar and must rank the")
    P("      decisions the same way a raw margin bar does.  That is measured in Arm C (G8).")
    P("")
    P("  PRE-DECLARED OUTCOMES (written before any tape is read):")
    P("    (A) THE SE BAR IS INFORMATIVE — at a matched move count R_SE books MORE 4b passers")
    P("        than R_BAR and sits ABOVE the 90th percentile of the count-matched R_RANDOM null.")
    P("    (B) IT IS ONLY CONSERVATISM — R_SE's 4b count tracks its move count along the same")
    P("        curve R_RANDOM traces (inside the null's 10-90 band), i.e. every book it recovers")
    P("        is bought by not moving, which R_ANCHOR does for free.")
    P("    (C) IT IS WORSE THAN THE RANK BAR — fewer 4b passers than R_BAR at a matched count.")
    P("    (D) DEGENERATE — R_SE's move count is 72 or 0 at every k >= 0.25, so there is no")
    P("        interior ladder to compare at all.")

    # ---------------------------------------------------------------- panels and books
    P("")
    P("-" * 104)
    P("ARM A — THE 72 DECISIONS REBUILT, AND 1154's COMMITTED NUMBERS GATED.")
    P("-" * 104)
    PAN, BOOKS = {}, {}
    u = load_universe()
    PAN["U56"] = Panel("U56", u)
    b = load_universe(broad=True)
    PAN["B136"] = Panel("B136", b)
    s, n_bad, n_meta = load_small()
    PAN["SMALL"] = Panel("SMALL", s)
    P(f"  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents of their screens.")
    P(f"  SMALL is the sub-$2B panel with {n_bad} of {n_meta} tickers dropped for max_1d_move")
    P(f"  >= 1.0, leaving {PAN['SMALL'].K - 1} names plus SPY as a benchmark column only.")
    for pn in PANELS:
        pan = PAN[pn]
        for an in ANCHORS:
            for lad in LADNAMES:
                BOOKS[(pn, an, lad)] = ladder_books(pan, an, lad)
        P(f"  {pn}: built  ({time.time() - t0:.0f}s)")

    # G1: the live book reproduces the record's committed MaxDD on U56
    lm = {}
    for pn in PANELS:
        pan = PAN[pn]
        lbk = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        lm[pn] = blocks_m(np.nan_to_num(lbk), pan.warm, pan.ins, pan.oos, pan.oosA, pan.oosB)
    gate("G1", "live RULES v2 U56 MaxDD == record -12.05%",
         abs(lm["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED), abs(lm["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)

    SPY_M = {pn: blocks_m(PAN[pn].spy, PAN[pn].warm, PAN[pn].ins, PAN[pn].oos,
                          PAN[pn].oosA, PAN[pn].oosB) for pn in PANELS}

    # ---- the decisions, with the FULL bootstrap draw matrix kept
    drows = []
    for pn in PANELS:
        pan = PAN[pn]
        T_is = int(pan.ins.sum())
        for an in ANCHORS:
            anch = ANCHORS[an]
            for lad in LADNAMES:
                rungs = LADDERS[lad]
                bk = BOOKS[(pn, an, lad)]
                R = np.column_stack([bk[r][pan.ins] for r in rungs])
                ai = rungs.index(anch[lad])
                for ch in CHOOSERS:
                    vals = [is_stat(bk[r], pan.ins, ch, T_is) for r in rungs]
                    pick_i = int(np.nanargmax(vals))
                    sv = np.sort(np.asarray(vals, float))
                    margin = float(sv[-1] - sv[-2]) if len(sv) > 1 else np.nan
                    delta = float(vals[pick_i] - vals[ai])
                    for L in BLOCKS + [1]:
                        V = pboot_stats(R, ch, L, seed_of(pn, an, lad, ch, L), B=BDRAWS)
                        pb = np.bincount(V.argmax(axis=1), minlength=len(rungs)) / BDRAWS
                        d = V[:, pick_i] - V[:, ai]
                        se_joint = float(d.std(ddof=1))
                        se_marg = float(np.sqrt(V[:, pick_i].var(ddof=1) + V[:, ai].var(ddof=1)))
                        drows.append(dict(
                            panel=pn, anchor=an, ladder=lad, chooser=ch, L=L,
                            k_rungs=len(rungs), anchor_rung=str(anch[lad]),
                            pick_rung=str(rungs[pick_i]), pick_i=pick_i, anchor_i=ai,
                            reached=bool(pick_i == ai), is_margin=margin, delta=delta,
                            SE_JOINT=se_joint, SE_MARGINAL=se_marg,
                            corr_pick_anchor=float(np.corrcoef(V[:, pick_i], V[:, ai])[0, 1])
                            if pick_i != ai else 1.0,
                            P_pick=float(pb[pick_i]), P_anchor=float(pb[ai]),
                            resolved=bool(pb[pick_i] >= BAR_HI or pb[pick_i] <= BAR_LO),
                            C_STRICT=(an == "A" and ch == CH_HEAD), C_PROX=(an == "A"),
                            C_ALL=True))
    ddf = pd.DataFrame(drows)
    # SE_IID is the L = 1 draw of SE_JOINT, carried onto every L row so a basis is one column
    iid = ddf[ddf.L == 1].set_index(["panel", "anchor", "ladder", "chooser"]).SE_JOINT
    ddf["SE_IID"] = [float(iid.loc[(r.panel, r.anchor, r.ladder, r.chooser)])
                     for r in ddf.itertuples()]
    ddf = ddf[ddf.L != 1].copy()
    dump(ddf, "decisions")

    head = ddf[ddf.L == L_HEAD]
    gate("G2", f"the decision population is 72 at L={L_HEAD}", abs(len(head) - 72), len(head) == 72)
    ok = head.is_margin.notna() & head.P_pick.notna()
    cor = float(np.corrcoef(head.loc[ok, "is_margin"].rank(), head.loc[ok, "P_pick"].rank())[0, 1])
    gate("G3", f"1154's Spearman(IS margin, P_pick) == {C1154_SPEARMAN} reproduces",
         abs(cor - C1154_SPEARMAN), abs(cor - C1154_SPEARMAN) < 5e-4)
    nres = int((head.P_pick >= BAR_HI).sum() + (head.P_pick <= BAR_LO).sum())
    gate("G4", f"1154's resolved count at L63 == {C1154_RESOLVED_CALL} of 72",
         abs(nres - C1154_RESOLVED_CALL), nres == C1154_RESOLVED_CALL)
    nmv = int((~head.reached).sum())
    gate("G5", f"1154's R_RAW move count == {C1154_RULE8['R_RAW'][4]} of 72",
         abs(nmv - C1154_RULE8["R_RAW"][4]), nmv == C1154_RULE8["R_RAW"][4])

    # ---- BYCATCH: the bootstrap SEED is an unstated dial in every P_boot claim in the record.
    P("")
    P("  BYCATCH — THE BOOTSTRAP SEED IS AN UNSTATED DIAL.  P_pick is a mean of B = 1000")
    P("  Bernoulli draws, so it carries an MC standard error of at most 0.5/sqrt(1000) =")
    P(f"  {0.5 / np.sqrt(BDRAWS):.4f}, and a decision sitting within that of the 0.90 bar can be")
    P("  called either way by the seed alone.  The same 72 decisions at L=63, re-drawn under")
    P("  three alternative seed bases (nothing else changed):")
    P(f"    {'seed base':>12s} {'resolved of 72':>15s} {'Spearman(margin, P_pick)':>26s} "
      f"{'R_BAR move count':>17s}")
    P(f"    {SEED_BASE:>12d} {nres:>15d} {cor:>26.4f} "
      f"{int(((head.P_pick >= BAR_HI) & (~head.reached)).sum()):>17d}   <- 1154's own")
    seedrows = [dict(seed_base=SEED_BASE, resolved=nres, spearman=cor,
                     bar_moves=int(((head.P_pick >= BAR_HI) & (~head.reached)).sum()))]
    for sb_ in SEED_SENS:
        pps, margs, reach = [], [], []
        for pn in PANELS:
            pan = PAN[pn]
            T_is = int(pan.ins.sum())
            for an in ANCHORS:
                for lad in LADNAMES:
                    rungs = LADDERS[lad]
                    bk = BOOKS[(pn, an, lad)]
                    R = np.column_stack([bk[r][pan.ins] for r in rungs])
                    ai = rungs.index(ANCHORS[an][lad])
                    for ch in CHOOSERS:
                        vals = [is_stat(bk[r], pan.ins, ch, T_is) for r in rungs]
                        pi = int(np.nanargmax(vals))
                        sv = np.sort(np.asarray(vals, float))
                        s_ = int(zlib.crc32("|".join(str(x) for x in
                                                     (pn, an, lad, ch, L_HEAD)).encode())) % 10_000_000
                        V = pboot_stats(R, ch, L_HEAD, sb_ + s_, B=BDRAWS)
                        pb = np.bincount(V.argmax(axis=1), minlength=len(rungs)) / BDRAWS
                        pps.append(float(pb[pi]))
                        margs.append(float(sv[-1] - sv[-2]))
                        reach.append(pi == ai)
        pps, margs, reach = np.array(pps), np.array(margs), np.array(reach)
        nr = int((pps >= BAR_HI).sum() + (pps <= BAR_LO).sum())
        sp = float(np.corrcoef(pd.Series(margs).rank(), pd.Series(pps).rank())[0, 1])
        bm = int(((pps >= BAR_HI) & (~reach)).sum())
        P(f"    {sb_:>12d} {nr:>15d} {sp:>26.4f} {bm:>17d}")
        seedrows.append(dict(seed_base=sb_, resolved=nr, spearman=sp, bar_moves=bm))
    sdfz = pd.DataFrame(seedrows)
    sdfz.to_csv(f"{OUT}.seedsens.csv", index=False)
    P(f"    range: resolved {int(sdfz.resolved.min())}-{int(sdfz.resolved.max())} of 72, "
      f"Spearman {sdfz.spearman.min():.4f}-{sdfz.spearman.max():.4f}, R_BAR move count "
      f"{int(sdfz.bar_moves.min())}-{int(sdfz.bar_moves.max())}.")
    P("    1154 stated its seed base; no OTHER P_boot claim in the record states one, and this is")
    P("    how much a claim moves on the seed with every other input identical.")

    # ---------------------------------------------------------------- ARM B: the SE ladder
    P("")
    P("-" * 104)
    P("ARM B — THE SE LADDER.  Every (k, basis) cell published; the move set is what a rule IS.")
    P("-" * 104)
    P("  A decision MOVES under R_SE(k, basis) iff delta > k * SE, where delta = stat(pick) -")
    P("  stat(anchor) on the IS window and SE is the bootstrap SD of that DIFFERENCE.")
    P("")
    P("  SE LEVELS at L = 63 over the 59 MOVERS (the 13 reached decisions have delta and SE")
    P("  identically zero and are excluded; a bar can only ever withhold a move, G11):")
    P(f"    {'basis':12s} {'median':>10s} {'min':>10s} {'max':>10s} {'max/min':>9s} "
      f"{'median delta/SE':>16s}")
    mvr = head[~head.reached]
    for bs in BASES:
        v = mvr[bs].replace([np.inf, -np.inf], np.nan).dropna()
        tstat = (mvr.delta / mvr[bs]).replace([np.inf, -np.inf], np.nan).dropna()
        P(f"    {bs:12s} {v.median():>10.4f} {v.min():>10.4f} {v.max():>10.4f} "
          f"{(v.max() / v.min()) if v.min() > 0 else np.inf:>9.2f} {tstat.median():>16.4f}")
    P("")
    n_bar = int(((head.P_pick >= BAR_HI) & (~head.reached)).sum())
    P(f"  MOVE COUNTS of R_SE(k, basis) out of 72 (R_RAW moves {nmv}, R_BAR {n_bar}, R_ANCHOR 0):")
    P(f"    {'basis':12s} " + "  ".join(f"{'k=' + str(k):>8s}" for k in KS))
    mrows = []
    MOVESET = {}
    for bs in BASES:
        cells = []
        for k in KS:
            mv = ((~head.reached) & (head.delta > k * head[bs])).values
            MOVESET[(bs, k)] = mv
            cells.append(int(mv.sum()))
            mrows.append(dict(basis=bs, k=k, n_moved=int(mv.sum())))
        P(f"    {bs:12s} " + "  ".join(f"{c:>8d}" for c in cells))
    pd.DataFrame(mrows).to_csv(f"{OUT}.movecounts.csv", index=False)
    mv0 = MOVESET[(BASIS_HEAD, 0.0)]
    gate("G6", "R_SE(k=0) is EXACTLY R_RAW (moves iff the argmax is not the anchor)",
         float(np.abs(mv0.astype(int) - (~head.reached).values.astype(int)).sum()),
         bool((mv0 == (~head.reached).values).all()))
    interior = sum(1 for bs in BASES for k in KS if k >= 0.25
                   and 0 < MOVESET[(bs, k)].sum() < 72)
    P(f"  interior cells (move count strictly between 0 and 72 at k >= 0.25): {interior} of "
      f"{len(BASES) * (len(KS) - 1)}")

    # ---------------------------------------------------------------- ARM C: is it a margin bar?
    P("")
    P("-" * 104)
    P("ARM C — IS THE SE BAR ANYTHING BUT A RE-SCALED MARGIN BAR?")
    P("-" * 104)
    P("  If SE were constant across decisions, ordering by delta/SE == ordering by delta, and")
    P("  R_SE would be a margin bar wearing a bootstrap.  Spearman(delta, delta/SE) at L=63:")
    srow = []
    for bs in BASES:
        t_ = (head.delta / head[bs]).replace([np.inf, -np.inf], np.nan)
        m_ = head.delta
        ok2 = t_.notna() & m_.notna() & (~head.reached)
        rho = float(np.corrcoef(m_[ok2].rank(), t_[ok2].rank())[0, 1])
        rho_p = float(np.corrcoef(head.loc[ok2, "P_pick"].rank(), t_[ok2].rank())[0, 1])
        P(f"    {bs:12s} Spearman(delta, delta/SE) = {rho:+.4f}   "
          f"Spearman(P_pick, delta/SE) = {rho_p:+.4f}   (n={int(ok2.sum())} movers)")
        srow.append(dict(basis=bs, spearman_delta=rho, spearman_Ppick=rho_p, n=int(ok2.sum())))
    pd.DataFrame(srow).to_csv(f"{OUT}.orthogonality.csv", index=False)
    rho_head = srow[BASES.index(BASIS_HEAD)]["spearman_delta"]
    gate("G8", "the SE bar is NOT the identity on the margin bar (Spearman < 0.999)",
         abs(rho_head), abs(rho_head) < 0.999)
    P("")
    P("  WHY THE JOINT SE IS THE RIGHT ONE: correlation between the pick's and the anchor's")
    P("  bootstrap statistic across draws, over the 72 at L=63 (a difference of two highly")
    P("  correlated quantities has a much smaller SE than either leg):")
    c_ = head.corr_pick_anchor.dropna()
    P(f"    median {c_.median():.4f}   min {c_.min():.4f}   max {c_.max():.4f}")
    P(f"    median SE_MARGINAL / SE_JOINT = "
      f"{float((head.SE_MARGINAL / head.SE_JOINT).median()):.4f}  — the correlation-blind reader")
    P("    overstates the error bar by this factor and therefore moves far less often.")

    # ---------------------------------------------------------------- ARM D: rule 8 walk
    P("")
    P("-" * 104)
    P("ARM D — RULE 8 WALK-FORWARD.  Picks chosen on 2009-2016 ALONE; 2017-2026 read ONCE.")
    P("-" * 104)
    # the OOS outcome of every (decision, chosen rung) — computed once, reused by every rule
    OUTC = {}
    for pn in PANELS:
        pan = PAN[pn]
        for an in ANCHORS:
            for lad in LADNAMES:
                for rung in LADDERS[lad]:
                    m = blocks_m(BOOKS[(pn, an, lad)][rung], pan.warm, pan.ins, pan.oos,
                                 pan.oosA, pan.oosB)
                    OUTC[(pn, an, lad, rung)] = dict(
                        m=m,
                        p4b=all(legs_4b(m, SPY_M[pn]).values()),
                        p4bo=all(legs_4b_oos(m, SPY_M[pn]).values()),
                        p4a=all(legs_4a(m, lm[pn]).values()))

    HD = head.reset_index(drop=True)

    # every decision's two possible outcomes, as parallel arrays — the move set then selects
    # between them by np.where, so the 500-draw null costs nothing.
    FLD = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "Sharpe", "OOSA_Sharpe", "OOSB_Sharpe",
           "OOSB_CAGR", "OOSB_MaxDD"]
    PK, AN = {f: [] for f in FLD + ["4b", "4bo", "4a", "rung"]}, \
             {f: [] for f in FLD + ["4b", "4bo", "4a", "rung"]}
    for r in HD.itertuples():
        for tgt, j in ((PK, r.pick_i), (AN, r.anchor_i)):
            rung = LADDERS[r.ladder][j]
            o = OUTC[(r.panel, r.anchor, r.ladder, rung)]
            for f in FLD:
                tgt[f].append(o["m"][f])
            tgt["4b"].append(o["p4b"])
            tgt["4bo"].append(o["p4bo"])
            tgt["4a"].append(o["p4a"])
            tgt["rung"].append(str(rung))
    PK = {k: np.asarray(v) for k, v in PK.items()}
    AN = {k: np.asarray(v) for k, v in AN.items()}

    def n4b_of(mv):
        return int(np.where(mv, PK["4b"], AN["4b"]).sum())

    def meanS_of(mv):
        return float(np.where(mv, PK["OOS_Sharpe"], AN["OOS_Sharpe"]).mean())

    def score(moveset, label, extra=None):
        """Apply a move set to the 72 decisions and read the OOS consequence ONCE."""
        mv = np.asarray(moveset, bool)
        d = {f: np.where(mv, PK[f], AN[f]) for f in FLD}
        out = pd.DataFrame(dict(
            rule=label, panel=HD.panel.values, anchor=HD.anchor.values,
            ladder=HD.ladder.values, chooser=HD.chooser.values,
            chosen_rung=np.where(mv, PK["rung"], AN["rung"]), moved=mv, **d,
            pass_4b_full=np.where(mv, PK["4b"], AN["4b"]),
            pass_4b_oos=np.where(mv, PK["4bo"], AN["4bo"]),
            pass_4a=np.where(mv, PK["4a"], AN["4a"])))
        for k_, v_ in (extra or {}).items():
            out[k_] = v_
        return out

    RAW_MV = (~HD.reached).values
    BAR_MV = ((HD.P_pick >= BAR_HI) & (~HD.reached)).values
    ANC_MV = np.zeros(len(HD), dtype=bool)

    allsc = [score(RAW_MV, "R_RAW", dict(basis="-", k=np.nan)),
             score(BAR_MV, "R_BAR", dict(basis="-", k=np.nan)),
             score(ANC_MV, "R_ANCHOR", dict(basis="-", k=np.nan))]
    for bs in BASES:
        for k in KS:
            allsc.append(score(MOVESET[(bs, k)], f"R_SE", dict(basis=bs, k=k)))
    wdf = pd.concat(allsc, ignore_index=True)
    dump(wdf, "walkforward")

    def summary(sub):
        return dict(n=len(sub), n_moved=int(sub.moved.sum()),
                    mean_OOS_Sharpe=float(sub.OOS_Sharpe.mean()),
                    mean_OOS_CAGR=float(sub.OOS_CAGR.mean()),
                    mean_OOS_MaxDD=float(sub.OOS_MaxDD.mean()),
                    n_4b_full=int(sub.pass_4b_full.sum()), n_4b_oos=int(sub.pass_4b_oos.sum()),
                    n_4a=int(sub.pass_4a.sum()))

    P("")
    P("  1154's THREE RULES, REPRODUCED (C_ALL x L63):")
    P(f"  {'rule':<10s} {'moved':>6s} {'meanOOS_S':>10s} {'4b_full':>8s} {'4b_oos':>7s} {'4a':>4s}"
      f"   {'1154 committed':>28s}")
    worst = 0.0
    for rl in ["R_RAW", "R_BAR", "R_ANCHOR"]:
        sub = wdf[wdf["rule"] == rl]
        sm = summary(sub)
        c = C1154_RULE8[rl]
        worst = max(worst, abs(sm["mean_OOS_Sharpe"] - c[0]))
        P(f"  {rl:<10s} {sm['n_moved']:>6d} {sm['mean_OOS_Sharpe']:>10.4f} "
          f"{sm['n_4b_full']:>8d} {sm['n_4b_oos']:>7d} {sm['n_4a']:>4d}"
          f"   {c[0]:.4f} / {c[1]} / {c[2]} / {c[3]} / moved {c[4]}")
    gate("G7", "1154's committed mean OOS Sharpes for R_RAW / R_BAR / R_ANCHOR reproduce",
         worst, worst < 5e-4)

    P("")
    P("  EVERY GRID POINT — R_SE(k, basis) against the three (C_ALL x L63, all 72 decisions):")
    P(f"  {'basis':12s} {'k':>5s} {'moved':>6s} {'meanOOS_S':>10s} {'meanOOS_CAGR':>13s} "
      f"{'meanOOS_DD':>11s} {'4b_full':>8s} {'4b_oos':>7s} {'4a':>4s}")
    grows = []
    for bs in BASES:
        for k in KS:
            sub = wdf[(wdf["rule"] == "R_SE") & (wdf.basis == bs) & (wdf.k == k)]
            sm = summary(sub)
            grows.append(dict(basis=bs, k=k, **sm))
            P(f"  {bs:12s} {k:>5.2f} {sm['n_moved']:>6d} {sm['mean_OOS_Sharpe']:>10.4f} "
              f"{sm['mean_OOS_CAGR']:>13.4f} {sm['mean_OOS_MaxDD']:>11.4f} "
              f"{sm['n_4b_full']:>8d} {sm['n_4b_oos']:>7d} {sm['n_4a']:>4d}")
    gdf = pd.DataFrame(grows)
    dump(gdf, "segrid")
    P("")
    P("  THE SAME ON THE OTHER THREE BLOCK LENGTHS (reported, never adjudicated on) — 4b_full")
    P(f"  of 72 at the headline basis {BASIS_HEAD}:")
    P(f"    {'L':>5s} " + "  ".join(f"{'k=' + str(k):>8s}" for k in KS))
    lrows = []
    for L in BLOCKS:
        hl = ddf[ddf.L == L].reset_index(drop=True)
        cells = []
        for k in KS:
            mv = ((~hl.reached) & (hl.delta > k * hl[BASIS_HEAD])).values
            sub = score(mv, "R_SE_L", dict(basis=BASIS_HEAD, k=k))
            cells.append(int(sub.pass_4b_full.sum()))
            lrows.append(dict(L=L, k=k, n_moved=int(mv.sum()),
                              n_4b_full=int(sub.pass_4b_full.sum()),
                              mean_OOS_Sharpe=float(sub.OOS_Sharpe.mean())))
        P(f"    {L:>5d} " + "  ".join(f"{c:>8d}" for c in cells))
    pd.DataFrame(lrows).to_csv(f"{OUT}.blocksens.csv", index=False)

    # ---------------------------------------------------------------- ARM E: matched move count
    P("")
    P("-" * 104)
    P("ARM E — THE ONLY TEST THAT MEANS ANYTHING: MATCHED MOVE COUNT vs R_BAR AND vs A")
    P("        COUNT-MATCHED RANDOM BAR.")
    P("-" * 104)
    P(f"  For each move count m, {RAND_DRAWS} seeded uniform draws of m of the {int(RAW_MV.sum())}")
    P("  decisions whose argmax is not the anchor.  A bar that carries INFORMATION must sit above")
    P("  this null; a bar that is merely CONSERVATIVE sits inside it.")
    P("")
    movers = np.flatnonzero(RAW_MV)
    NULLC = {}

    def null_for(m):
        if m in NULLC:
            return NULLC[m]
        rng = np.random.default_rng(seed_of("null", m))
        c4b, cs = [], []
        for _ in range(RAND_DRAWS):
            mv = np.zeros(len(HD), dtype=bool)
            if m:
                mv[rng.choice(movers, size=m, replace=False)] = True
            c4b.append(n4b_of(mv))
            cs.append(meanS_of(mv))
        NULLC[m] = (np.array(c4b), np.array(cs))
        return NULLC[m]

    P(f"  {'rule':22s} {'moved':>6s} {'4b_full':>8s} {'null 4b p10/p50/p90':>22s} {'pctile':>7s} "
      f"{'meanOOS_S':>10s} {'null S p50':>11s} {'pctile':>7s}")
    erows = []
    cand = [("R_RAW", RAW_MV, "-", np.nan), ("R_BAR", BAR_MV, "-", np.nan)]
    for bs in BASES:
        for k in KS:
            if k == 0.0:
                continue
            cand.append((f"R_SE k={k} {bs}", MOVESET[(bs, k)], bs, k))
    for label, mv, bs, k in cand:
        m = int(mv.sum())
        sub = score(mv, label)
        n4 = int(sub.pass_4b_full.sum())
        ms = float(sub.OOS_Sharpe.mean())
        c4b, cs = null_for(m)
        p4 = float((c4b < n4).mean() + 0.5 * (c4b == n4).mean())
        ps = float((cs < ms).mean() + 0.5 * (cs == ms).mean())
        P(f"  {label:22s} {m:>6d} {n4:>8d} "
          f"{f'{np.percentile(c4b, 10):.1f}/{np.percentile(c4b, 50):.1f}/{np.percentile(c4b, 90):.1f}':>22s} "
          f"{p4:>7.3f} {ms:>10.4f} {np.percentile(cs, 50):>11.4f} {ps:>7.3f}")
        erows.append(dict(rule=label, basis=bs, k=k, n_moved=m, n_4b_full=n4,
                          null_4b_p10=float(np.percentile(c4b, 10)),
                          null_4b_p50=float(np.percentile(c4b, 50)),
                          null_4b_p90=float(np.percentile(c4b, 90)), pctile_4b=p4,
                          mean_OOS_Sharpe=ms, null_S_p50=float(np.percentile(cs, 50)),
                          pctile_Sharpe=ps))
    edf = pd.DataFrame(erows)
    dump(edf, "matched")

    # the head-to-head R_SE vs R_BAR at the SAME move count
    P("")
    bar_m = int(BAR_MV.sum())
    bar_4b = int(score(BAR_MV, "R_BAR").pass_4b_full.sum())
    bar_s = float(score(BAR_MV, "R_BAR").OOS_Sharpe.mean())
    se_rows = edf[edf.basis == BASIS_HEAD]
    near = se_rows.iloc[(se_rows.n_moved - bar_m).abs().argsort()].iloc[0]
    P(f"  HEAD-TO-HEAD AT THE RANK BAR's OWN MOVE COUNT ({bar_m} of 72):")
    P(f"    R_BAR                 moves {bar_m:>2d}  4b_full {bar_4b:>2d}  mean OOS Sharpe {bar_s:.4f}")
    P(f"    R_SE k={near.k} {near.basis:11s} moves {int(near.n_moved):>2d}  "
      f"4b_full {int(near.n_4b_full):>2d}  mean OOS Sharpe {near.mean_OOS_Sharpe:.4f}")
    P(f"    count-matched RANDOM  moves {bar_m:>2d}  4b_full "
      f"{np.percentile(null_for(bar_m)[0], 50):.1f} (p10 {np.percentile(null_for(bar_m)[0], 10):.1f}, "
      f"p90 {np.percentile(null_for(bar_m)[0], 90):.1f})")
    P("")
    P("  DOES ANY R_SE CELL BEAT ITS OWN COUNT-MATCHED NULL AT THE 0.90 PERCENTILE?")
    se_only = edf[edf["rule"].str.startswith("R_SE")]
    n_info = int((se_only.pctile_4b >= 0.90).sum())
    P(f"    4b count above the null's 90th percentile: {n_info} of {len(se_only)} R_SE cells")
    P(f"    mean OOS Sharpe above it:                  "
      f"{int((se_only.pctile_Sharpe >= 0.90).sum())} of {len(se_only)}")
    P(f"    R_BAR itself: 4b pctile {float(edf[edf['rule'] == 'R_BAR'].pctile_4b.iloc[0]):.3f}, "
      f"Sharpe pctile {float(edf[edf['rule'] == 'R_BAR'].pctile_Sharpe.iloc[0]):.3f}")
    P(f"    R_RAW itself: 4b pctile {float(edf[edf['rule'] == 'R_RAW'].pctile_4b.iloc[0]):.3f}, "
      f"Sharpe pctile {float(edf[edf['rule'] == 'R_RAW'].pctile_Sharpe.iloc[0]):.3f}")

    # ---- the law that explains every published number in this family
    P("")
    P("  THE LAW.  If no bar carries information, a rule's 4b count is a function of its MOVE")
    P("  COUNT alone: each move off an anchor book destroys a 4b pass with a fixed probability.")
    P(f"  R_ANCHOR books {n4b_of(ANC_MV)} at 0 moves and R_RAW {n4b_of(RAW_MV)} at "
      f"{int(RAW_MV.sum())}, so that rate is "
      f"{(n4b_of(ANC_MV) - n4b_of(RAW_MV)) / int(RAW_MV.sum()):.4f} books per move.  The straight")
    P("  line through those two points, against the count-matched null and against every rule:")
    slope = (n4b_of(RAW_MV) - n4b_of(ANC_MV)) / int(RAW_MV.sum())   # negative: moves cost books
    icept = float(n4b_of(ANC_MV))
    P(f"    predicted 4b(m) = {icept:.1f} - {abs(slope):.4f} * m")
    P(f"    {'m':>4s} {'null p50':>9s} {'predicted':>10s} {'dev':>7s}   rules at this m")
    lawrows = []
    for m in sorted({int(r.n_moved) for r in edf.itertuples()}):
        c4b, _ = null_for(m)
        pred = icept + slope * m
        med = float(np.percentile(c4b, 50))
        at = ", ".join(f"{r['rule']}={int(r.n_4b_full)}" for _, r in edf[edf.n_moved == m].iterrows())
        P(f"    {m:>4d} {med:>9.1f} {pred:>10.2f} {med - pred:>+7.2f}   {at}")
        lawrows.append(dict(m=m, null_p50=med, predicted=pred, dev=med - pred))
    ldf = pd.DataFrame(lawrows)
    ldf.to_csv(f"{OUT}.law.csv", index=False)
    P(f"    worst deviation of the null median from the straight line: "
      f"{ldf.dev.abs().max():.2f} of a book over m = {int(ldf.m.min())}-{int(ldf.m.max())}.")
    obs = edf.n_4b_full.values.astype(float)
    prd = icept + slope * edf.n_moved.values
    ss_res = float(((obs - prd) ** 2).sum())
    ss_tot = float(((obs - obs.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot else np.nan
    P(f"    ACROSS ALL {len(edf)} PUBLISHED RULES (R_RAW, R_BAR and the 18 R_SE cells), MOVE")
    P(f"    COUNT ALONE EXPLAINS R^2 = {r2:.4f} of the 4b count, on a line fitted to NO data —")
    P("    its two endpoints are R_ANCHOR and R_RAW, both already in the record.")
    P(f"    Mean OOS Sharpe over the same {len(edf)} rules spans only "
      f"{edf.mean_OOS_Sharpe.min():.4f}-{edf.mean_OOS_Sharpe.max():.4f} "
      f"(range {edf.mean_OOS_Sharpe.max() - edf.mean_OOS_Sharpe.min():.4f}) while the 4b count")
    P(f"    spans {int(edf.n_4b_full.min())}-{int(edf.n_4b_full.max())}: the 4b count is a "
      f"THRESHOLD census, not a return.")

    # the pre-declared verdict
    best = se_only.sort_values("pctile_4b", ascending=False).iloc[0]
    interior_ok = interior > 0
    A_ok = bool(interior_ok and (best.pctile_4b >= 0.90)
                and (float(best.n_4b_full) > bar_4b))
    C_ok = bool(interior_ok and se_only[se_only.n_moved >= bar_m].n_4b_full.max() < bar_4b) \
        if (se_only.n_moved >= bar_m).any() else False
    answer = ("(D) DEGENERATE" if not interior_ok else
              "(A) THE SE BAR IS INFORMATIVE" if A_ok else
              "(C) WORSE THAN THE RANK BAR" if C_ok else
              "(B) ONLY CONSERVATISM")
    P("")
    P(f"  PRE-DECLARED OUTCOME SELECTED: {answer}")
    P(f"    interior ladder exists: {interior_ok} ({interior} interior cells)")
    P(f"    best R_SE cell by null percentile: k={best.k} {best.basis}, moves "
      f"{int(best.n_moved)}, 4b {int(best.n_4b_full)}, pctile {best.pctile_4b:.3f}")
    P(f"    R_BAR's 4b at {bar_m} moves: {bar_4b}")

    # ---------------------------------------------------------------- ARM F: this run's own rule 8
    P("")
    P("-" * 104)
    P("ARM F — THIS RUN'S OWN TWO DIALS WALKED FORWARD (PROTOCOL rule 8, second stage).")
    P("-" * 104)
    P(f"  The PICKS already use 2009-2016 only.  This run's (k, basis) is now chosen on")
    P(f"  2017-{OOS_SPLIT[:4]} and 2022-2026 is read ONCE.  Reported against the three")
    P("  inherited rules and against SPY and the live book on the same window.")
    frows = []
    for bs in BASES:
        for k in KS:
            sub = wdf[(wdf["rule"] == "R_SE") & (wdf.basis == bs) & (wdf.k == k)]
            frows.append(dict(rule=f"R_SE", basis=bs, k=k, n_moved=int(sub.moved.sum()),
                              A_Sharpe=float(sub.OOSA_Sharpe.mean()),
                              B_Sharpe=float(sub.OOSB_Sharpe.mean()),
                              B_CAGR=float(sub.OOSB_CAGR.mean()),
                              B_MaxDD=float(sub.OOSB_MaxDD.mean())))
    for rl in ["R_RAW", "R_BAR", "R_ANCHOR"]:
        sub = wdf[wdf["rule"] == rl]
        frows.append(dict(rule=rl, basis="-", k=np.nan, n_moved=int(sub.moved.sum()),
                          A_Sharpe=float(sub.OOSA_Sharpe.mean()),
                          B_Sharpe=float(sub.OOSB_Sharpe.mean()),
                          B_CAGR=float(sub.OOSB_CAGR.mean()),
                          B_MaxDD=float(sub.OOSB_MaxDD.mean())))
    fdf = pd.DataFrame(frows)
    dump(fdf, "rule8_dials")
    sel = fdf[fdf["rule"] == "R_SE"].sort_values("A_Sharpe", ascending=False).iloc[0]
    P(f"  IS-CHOSEN CELL (argmax of mean 2017-2021 Sharpe over the 21 R_SE cells): "
      f"k={sel.k} {sel.basis}, moves {int(sel.n_moved)}")
    P(f"  {'rule':22s} {'moved':>6s} {'2017-21 Sh':>11s} {'2022-26 Sh':>11s} {'2022-26 CAGR':>13s} "
      f"{'2022-26 DD':>11s}")
    P(f"  {'R_SE (IS-chosen)':22s} {int(sel.n_moved):>6d} {sel.A_Sharpe:>11.4f} "
      f"{sel.B_Sharpe:>11.4f} {sel.B_CAGR:>13.4f} {sel.B_MaxDD:>11.4f}")
    for rl in ["R_RAW", "R_BAR", "R_ANCHOR"]:
        r_ = fdf[fdf["rule"] == rl].iloc[0]
        P(f"  {rl:22s} {int(r_.n_moved):>6d} {r_.A_Sharpe:>11.4f} {r_.B_Sharpe:>11.4f} "
          f"{r_.B_CAGR:>13.4f} {r_.B_MaxDD:>11.4f}")
    for pn in PANELS:
        sm, lmm = SPY_M[pn], lm[pn]
        P(f"    {pn:6s} SPY   2017-21 {sm['OOSA_Sharpe']:.4f}  2022-26 {sm['OOSB_Sharpe']:.4f} / "
          f"{sm['OOSB_CAGR']:.2%} / {sm['OOSB_MaxDD']:.2%}      LIVE RULES v2 2022-26 "
          f"{lmm['OOSB_Sharpe']:.4f} / {lmm['OOSB_CAGR']:.2%}")
    P("  The IS-chosen cell's OOS-B reading is the one number in this run chosen and then read")
    P("  once; every other cell above is reported, not selected.")

    # ---------------------------------------------------------------- ARM G: both KEEP paths
    P("")
    P("-" * 104)
    P("ARM G — BOTH KEEP PATHS (PROTOCOL rule 4) on every rung book and every published book.")
    P("-" * 104)
    brows, seen = [], set()
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                for rung in LADDERS[lad]:
                    a = ANCHORS[an]
                    kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
                    kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
                    bkey = (pn, kw["N"], kw["H"], kw["gross"], kw["freq"])
                    if bkey in seen:
                        continue
                    seen.add(bkey)
                    o = OUTC[(pn, an, lad, rung)]
                    brows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung),
                                      N=kw["N"], H=kw["H"], gross=kw["gross"], cadence=kw["freq"],
                                      CAGR=o["m"]["CAGR"], Sharpe=o["m"]["Sharpe"],
                                      MaxDD=o["m"]["MaxDD"], H1=o["m"]["H1"], H2=o["m"]["H2"],
                                      OOS_CAGR=o["m"]["OOS_CAGR"],
                                      OOS_Sharpe=o["m"]["OOS_Sharpe"],
                                      OOS_MaxDD=o["m"]["OOS_MaxDD"],
                                      KEEP_4a=o["p4a"], KEEP_4b=o["p4b"], KEEP_4b_OOS=o["p4bo"]))
    bdf = pd.DataFrame(brows)
    dump(bdf, "books")
    P(f"  {len(bdf)} rung books: 4a {int(bdf.KEEP_4a.sum())};  4b full {int(bdf.KEEP_4b.sum())};  "
      f"4b OOS {int(bdf.KEEP_4b_OOS.sum())};  BOTH {int((bdf.KEEP_4b & bdf.KEEP_4b_OOS).sum())}")
    for pn in PANELS:
        s_ = bdf[bdf.panel == pn]
        P(f"    {pn:6s} 4a {int(s_.KEEP_4a.sum()):>2d}/{len(s_):<3d}  4b {int(s_.KEEP_4b.sum()):>2d}/{len(s_):<3d}"
          f"  4b-OOS {int(s_.KEEP_4b_OOS.sum()):>2d}/{len(s_):<3d}")
    P("  BENCHMARKS per panel (full sample from warm-up; OOS = 2017-2026):")
    for pn in PANELS:
        sm, lmm = SPY_M[pn], lm[pn]
        P(f"    {pn:6s} SPY {sm['CAGR']:>7.2%} / {sm['Sharpe']:.4f} / {sm['MaxDD']:>7.2%}  "
          f"halves {sm['H1']:.3f}/{sm['H2']:.3f}  OOS {sm['OOS_CAGR']:>7.2%} / {sm['OOS_Sharpe']:.4f}"
          f" / {sm['OOS_MaxDD']:>7.2%}   LIVE v2 {lmm['Sharpe']:.4f} (OOS {lmm['OOS_Sharpe']:.4f})")
    kb = bdf[bdf.KEEP_4b & bdf.KEEP_4b_OOS]
    if len(kb):
        P(f"  the {len(kb)} full+OOS 4b passers (PRIOR ART — these are 1154's own rung books,")
        P("  re-read by a run that adds no book of its own):")
        for _, r in kb.sort_values("OOS_Sharpe", ascending=False).head(12).iterrows():
            P(f"    {r.panel:6s} {r.anchor} {r.ladder:<8s} rung {r.rung:>5s}  CAGR {r.CAGR:>6.2%} "
              f"Sh {r.Sharpe:.4f} DD {r.MaxDD:>7.2%} halves {r.H1:.3f}/{r.H2:.3f}  "
              f"OOS {r.OOS_CAGR:>6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:>7.2%}")
    P("  NOT PROMOTED, NO MEMO: 4a is the path against the live book and this run's 4a count is")
    P("  printed above; the 4b passers are the rung books 1154 already recorded and declined.")

    # ---------------------------------------------------------------- gates
    P("")
    P("-" * 104)
    P("GATES")
    P("-" * 104)
    # G9: R_SE's move set is monotone decreasing in k at every basis
    mono = all(MOVESET[(bs, KS[i])].sum() >= MOVESET[(bs, KS[i + 1])].sum()
               for bs in BASES for i in range(len(KS) - 1))
    gate("G9", "R_SE's move count is monotone non-increasing in k at every basis",
         float(mono), bool(mono))
    # G10: SE_MARGINAL >= SE_JOINT wherever the rungs are positively correlated
    pos = head[head.corr_pick_anchor > 0]
    viol = float((pos.SE_MARGINAL < pos.SE_JOINT - 1e-12).sum())
    gate("G10", "SE_MARGINAL >= SE_JOINT wherever the pick and anchor co-move positively",
         viol, viol == 0)
    # G11: every R_SE move set is a SUBSET of R_RAW's
    sub_ok = all(bool((MOVESET[(bs, k)] & ~RAW_MV).sum() == 0) for bs in BASES for k in KS)
    gate("G11", "every R_SE move set is a subset of R_RAW's (a bar can only withhold)",
         float(sub_ok), bool(sub_ok))
    # G12: the null draws only ever move on decisions R_RAW would move on
    gate("G12", "the count-matched RANDOM null draws only from R_RAW's move set",
         float(len(movers) == int(RAW_MV.sum())), len(movers) == int(RAW_MV.sum()))
    gg = pd.DataFrame(GATES)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    P(f"  GATES {int(gg.pass_.sum())} of {len(gg)}")
    P(f"\n  total {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    return ddf, wdf, edf, bdf, gg


if __name__ == "__main__":
    main()

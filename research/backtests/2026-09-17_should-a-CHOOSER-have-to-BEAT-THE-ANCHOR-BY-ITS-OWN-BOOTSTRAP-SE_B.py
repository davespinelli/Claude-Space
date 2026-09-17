#!/usr/bin/env python3
"""
Idea 1210 (lane B, 2026-09-17) — should a CHOOSER have to BEAT THE ANCHOR BY ITS OWN
BOOTSTRAP SE rather than merely OUTRANK IT?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1154 (lane B, 2026-09-17,
`2026-09-17_does-any-committed-REACH-or-CHOOSER-claim-survive-its-OWN-P_boot-BAR_B.py`)
scored 72 published pick decisions (3 panels x 2 anchors x 4 ladders x 3 choosers) two ways
and found the two readings NEARLY ORTHOGONAL: Spearman(IS margin, P_boot) = 0.1551, median
IS margin 9.739e-03 among the RESOLVED decisions against 9.369e-03 among the unresolved.
A rank bar (P_boot) certifies ORDER STABILITY; a margin column reports EFFECT SIZE; neither
prices a pick on its own.  1154's rule-8 arm then read R_RAW 0.7996 / R_BAR 0.7887 /
R_ANCHOR 0.7901 mean OOS Sharpe with 4b-full counts 6 / 19 / 24 of 72, and the queue read
the 24 - 6 = 18 as "capital-worthy books the record's habit loses".

THE QUEUE'S QUESTION, VERBATIM: test a THIRD rule — move only when the argmax beats the
anchor by k bootstrap SE of the difference — against R_RAW, R_BAR and R_ANCHOR on the SAME
72 decisions, and report whether it recovers any of those 18.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  k          {0, 0.25, 0.5, 1.0, 1.5, 2.0}      SE multiple the argmax must clear
  SE BASIS   {SE_BLOCK, SE_IID, SE_FOLD}        how the SE of the difference is built

  = 18 dial cells, EVERY ONE PUBLISHED.  The HEADLINE rung is k = 1.0 x SE_BLOCK, declared
  here before any number: 1.0 because the queue's sentence says "by its own bootstrap SE",
  and SE_BLOCK because L = 63 moving-block is 1101's own resampler, inherited whole.

    SE_BLOCK  sd over 1000 JOINT moving-block (L=63) redraws of the IS window -- the same
              draws, the same seeds, the same chunking as 1154's P_boot, so P_pick and SE
              come off ONE pass and R_BAR reproduces 1154 to the bit (gate G8).
    SE_IID    sd over 1000 JOINT iid (L=1) redraws -- the naive basis, which ignores the
              serial dependence and must therefore read SMALLER (it moves MORE often).
    SE_FOLD   sd of the per-fold difference over the NON-OVERLAPPING IS calendar years,
              divided by sqrt(n_folds) -- the only basis carrying between-year regime
              variation, which a single-tape resample cannot see.

WHAT IS NOT A DIAL.  Everything else is 1101/1154's, inherited whole and NOT re-tuned:
PANEL {U56, B136, SMALL} (rule 9 requires all three), ANCHOR {A, B}, the four CORE LADDERS
{N, H, GROSS, CADENCE}, the three honest CHOOSERS, CAND20 legs, max_vol 0.60, min hold 126,
10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, 1000 draws, crc32 seeds.  The three
comparand rules R_RAW / R_BAR / R_ANCHOR are 1154's, verbatim.

DECLARED BEFORE THE TAPE IS READ (Arm 0 proves both as identities):
  R_SE(k=0)   == R_RAW      because d >= 0 at every decision by the definition of argmax
  R_SE(k=inf) == R_ANCHOR   because no finite margin clears an infinite bar
so R_SE is a ONE-PARAMETER INTERPOLATION between the two controls 1154 already published.
That has a hard consequence which is stated now and tested in Arm C: if the family's OOS
profile is MONOTONE in k, the rule carries NO information beyond a dimmer switch between
"always move" and "never move", and its best cell is an ENDPOINT, i.e. one of the two
controls.  Only a NON-MONOTONE profile -- an interior k beating BOTH endpoints -- would
make the SE bar a rule rather than a re-labelling.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward in Arm C
(every pick chosen on 2009-2016 alone, 2017-2026 read ONCE, after) and BOTH KEEP paths on
all 144 distinct rung books in Arm E; rule 9 survivorship stated.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_should-a-CHOOSER-have-to-BEAT-THE-ANCHOR-BY-ITS-OWN-BOOTSTRAP-SE_B.py
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
SLUG = "should-a-CHOOSER-have-to-BEAT-THE-ANCHOR-BY-ITS-OWN-BOOTSTRAP-SE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ----- 1101/1154's construction, inherited whole --------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
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

BAR_HI = 0.90                  # 1154/1101's P_boot bar, for R_BAR
BDRAWS = 1000
L_BLOCK = 63                   # 1101's own block length
SEED_BASE = 11541154           # 1154's, so the BLOCK draws are the SAME draws

# ----- THE TWO DIALS -------------------------------------------------------------------------
KS = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0]
BASES = ["SE_BLOCK", "SE_IID", "SE_FOLD"]
K_HEAD, BASIS_HEAD = 1.0, "SE_BLOCK"
K_INF = 1e9                    # the identity end of the family

RULES_PUB = ["R_RAW", "R_BAR", "R_ANCHOR"]

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived ----------------
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
A1154_MEANOOS = {"R_RAW": 0.799558, "R_BAR": 0.788672, "R_ANCHOR": 0.790080}
A1154_4BFULL = {"R_RAW": 6, "R_BAR": 19, "R_ANCHOR": 24}
A1154_SPEARMAN = 0.1551

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


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}  ->  {value:.3e}")
    return bool(ok)


# =================================================================================================
# 1101/1154/1159's runner and metrics, verbatim
# =================================================================================================
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
    return warm, ins, oos


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


# =================================================================================================
# PANEL / BOOK CONSTRUCTION — 1101's rung books
# =================================================================================================
class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
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
        self.is_years = np.asarray(px.index.year)[self.ins]


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


# =================================================================================================
# THE BOOTSTRAP — 1101's joint redraw.  ONE pass returns BOTH P_boot and the SE of the
# pick-minus-anchor difference, so the BLOCK basis is the SAME draws 1154 scored.
# =================================================================================================
def block_index(rng, T, L, B):
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def _stat_matrix(X, stat, T):
    """X is (b, T, k) resampled IS returns -> (b, k) chooser values, higher = better."""
    if stat == "CH_ISSHARPE":
        return X.mean(axis=1) * 252.0 / (X.std(axis=1, ddof=1) * np.sqrt(252.0))
    if stat == "CH_ISCAGR":
        eq = np.cumprod(1.0 + X, axis=1)
        return eq[:, -1, :] ** (252.0 / T) - 1.0
    if stat == "CH_ISDD":
        eq = np.cumprod(1.0 + X, axis=1)
        return (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
    raise ValueError(stat)


def pboot(R, stat, L, seed, pick_i, anch_i, B=BDRAWS, chunk=100):
    """Joint moving-block redraw of the IS window.  Returns (P_boot vector, sd of the
    pick-minus-anchor difference, mean of that difference).  L = 1 is the iid basis.

    One block index per draw is applied to ALL rungs, so the cross-rung correlation that
    makes these ladders hard to resolve is PRESERVED — which is exactly what makes the SE
    of the DIFFERENCE much smaller than the SE of either rung on its own.
    """
    T, k = R.shape
    rng = np.random.default_rng(seed)
    cnt = np.zeros(k)
    diffs = np.empty(B)
    done = 0
    while done < B:
        b = min(chunk, B - done)
        idx = block_index(rng, T, L, b)
        v = _stat_matrix(R[idx], stat, T)
        v = np.where(np.isfinite(v), v, -np.inf)
        cnt += np.bincount(v.argmax(axis=1), minlength=k)
        d = v[:, pick_i] - v[:, anch_i]
        diffs[done:done + b] = np.where(np.isfinite(d), d, np.nan)
        done += b
    return cnt / B, float(np.nanstd(diffs, ddof=1)), float(np.nanmean(diffs))


def is_stat_on(x, stat):
    """The chooser's statistic on an arbitrary slice of daily returns, higher = better."""
    x = np.asarray(x, float)
    if len(x) < 5:
        return np.nan
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    eq = np.cumprod(1.0 + x)
    if stat == "CH_ISCAGR":
        return eq[-1] ** (252.0 / len(x)) - 1.0
    if stat == "CH_ISDD":
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


def se_fold(r_pick, r_anch, years):
    """SE of the difference over NON-OVERLAPPING IS calendar-year folds.  The only basis
    that carries between-year regime variation; a single-tape resample cannot see it."""
    ds = []
    for y in np.unique(years):
        m = years == y
        d = is_stat_on(r_pick[m], se_fold.stat) - is_stat_on(r_anch[m], se_fold.stat)
        if np.isfinite(d):
            ds.append(d)
    if len(ds) < 2:
        return np.nan, len(ds)
    return float(np.std(ds, ddof=1) / np.sqrt(len(ds))), len(ds)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1210 (lane B, {DATE}) — should a CHOOSER have to BEAT THE ANCHOR BY ITS OWN")
    P("BOOTSTRAP SE rather than merely OUTRANK IT?")
    P("=" * 100)
    P(f"  dial 1 = k         {KS}            (headline {K_HEAD})")
    P(f"  dial 2 = SE BASIS  {BASES}   (headline {BASIS_HEAD})")
    P("  NOT dials: panel (3), anchor (2), ladder (4), chooser (3) — 1154's SAME 72 decisions,")
    P("             published at every one of the 18 dial cells.  Comparands R_RAW / R_BAR /")
    P("             R_ANCHOR are 1154's, verbatim; BLOCK seeds are 1154's, so R_BAR is its row.")
    P("")

    # ---------------------------------------------------------------- ARM 0: data-free first
    P("-" * 100)
    P("ARM 0 — DATA-FREE.  What IS the R_SE family, before any tape is read?")
    P("-" * 100)
    P("  R_SE(k) moves iff  d >= k * SE(d),  d = stat(argmax) - stat(anchor) on the IS window.")
    P("  Two ENDPOINT IDENTITIES, true by construction and gated below (G5, G6):")
    P("    k = 0    -> d >= 0 holds at EVERY decision (d is an argmax minus a member of the")
    P("                same ladder), so R_SE(0) moves whenever R_RAW moves: R_SE(0) == R_RAW.")
    P("    k = inf  -> no finite d clears it, so R_SE(inf) == R_ANCHOR, 1155's do-nothing.")
    P("  THEREFORE R_SE IS A ONE-PARAMETER INTERPOLATION BETWEEN TWO CONTROLS 1154 ALREADY")
    P("  PUBLISHED, and its move-rate is NON-INCREASING in k at every basis (G11).  The")
    P("  consequence, stated before the result: if the OOS profile is MONOTONE in k, the best")
    P("  cell is an ENDPOINT and the SE bar is a DIMMER SWITCH, not a rule.  Only an INTERIOR")
    P("  k beating BOTH endpoints would make it a rule.  That is the falsifier this run runs.")
    P("")
    P("  What the bar DEMANDS, per basis, before any tape (the ordering is an identity too):")
    P("    SE_IID   ignores serial dependence -> smallest SE -> moves MOST at a given k")
    P("    SE_BLOCK L=63 keeps it                                (1101's own resampler)")
    P("    SE_FOLD  8 IS calendar years, between-year variance -> expected LARGEST, moves LEAST")
    P("  Reported, not assumed: the realised ordering is in the decisions table and Arm B.")
    frows = []
    for lad in LADNAMES:
        k = len(LADDERS[lad])
        frows.append(dict(ladder=lad, k_rungs=k,
                          uniform_null=1.0 / k,
                          n_decisions_per_panel_anchor=len(CHOOSERS),
                          max_movable=k - 1))
    fdf = pd.DataFrame(frows)
    P("")
    P(fdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(fdf, "datafree")
    P("")
    P("  AND A COUNTING FACT THE QUEUE'S '18 BOOKS' DEPENDS ON, checked in Arm D: 72 DECISIONS")
    P("  are not 72 BOOKS.  R_ANCHOR selects the anchor rung at all 12 (ladder, chooser)")
    P(f"  decisions of a given (panel, anchor), so its 72 selections are at most "
      f"{len(PANELS) * len(ANCHORS)} DISTINCT books.")
    P("")

    # ---------------------------------------------------------------- panels
    P("-" * 100)
    P("PANELS (rule 9: all three current-constituent lists; every LEVEL is optimistic).")
    P("-" * 100)
    u = load_universe()
    b = load_universe(broad=True)
    s, n_bad, n_meta = load_small()
    PAN = {}
    for nm, px in (("U56", u), ("B136", b), ("SMALL", s)):
        PAN[nm] = Panel(nm, px)
        neli = px.shape[1] - (1 if nm == "SMALL" else 0)
        P(f"  {nm:<6s} {px.shape[0]:,} rows x {px.shape[1]} cols, {neli} eligible   "
          f"{px.index[0].date()} -> {px.index[-1].date()}  "
          f"warm {PAN[nm].warm.sum():,}  IS {PAN[nm].ins.sum():,}  OOS {PAN[nm].oos.sum():,}  "
          f"IS folds {len(np.unique(PAN[nm].is_years))}")
    P(f"  SMALL exclusion: {n_bad} of {n_meta} names dropped on max_1d_move >= 1.0 (documented).")
    P("")

    # ---------------------------------------------------------------- gates before results
    P("-" * 100)
    P("GATES — printed BEFORE any result number.")
    P("-" * 100)
    pu = PAN["U56"]
    a = ANCHORS["A"]
    r_anchor = book(pu, a["N"], a["H"], a["GROSS"], a["CADENCE"])
    W = build(-pu.sc, pu.elig, pu.priced, pu.reb["W"], a["N"], a["H"], pu.T, pu.K, a["GROSS"])
    eng = backtest(pu.px, pd.DataFrame(W, index=pu.idx, columns=pu.px.columns),
                   cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.abs(eng[pu.warm] - r_anchor[pu.warm]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", g1, g1 < 1e-12)

    mA = blocks_m(r_anchor, pu.warm, pu.ins, pu.oos)
    g2 = max(abs(mA["CAGR"] - A1101_TRIPLE[0]), abs(mA["Sharpe"] - A1101_TRIPLE[1]),
             abs(mA["MaxDD"] - A1101_TRIPLE[2]))
    gate("G2", "CROSS-RUN 1101's committed U56 anchor-A triple", g2, g2 < 5e-3)

    lb = backtest(pu.px, rules_v2_weights(pu.px), cost_bps=COST, freq="W")["returns"]
    _, _, ldd = fmet(lb.values[pu.warm])
    g3 = abs(ldd - LIVE_MAXDD_COMMITTED)
    gate("G3", "live RULES v2 U56 MaxDD == committed -12.05%", g3, g3 < 5e-4)

    spy_m = blocks_m(pu.spy, pu.warm, pu.ins, pu.oos)
    g4 = max(abs(spy_m["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(spy_m["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G4", "SPY OOS triple == committed (1161's bar 5e-3)", g4, g4 < 5e-3)

    # G7: the SE machinery's KNOWN ANSWER.  A DEGENERATE pair -- the pick book IS the anchor
    # book -- must give d == 0 and SE(d) == 0 EXACTLY on every basis, because the joint index
    # applies the same resample to both columns.  If any basis leaked an independent draw this
    # would be positive, and every t-statistic downstream would be silently finite.
    T_is = int(pu.ins.sum())
    Rdeg = np.column_stack([r_anchor[pu.ins], r_anchor[pu.ins]])
    _, sdb, mdb = pboot(Rdeg, CH_HEAD, L_BLOCK, seed_of("G7"), 0, 1, B=200)
    _, sdi, mdi = pboot(Rdeg, CH_HEAD, 1, seed_of("G7i"), 0, 1, B=200)
    se_fold.stat = CH_HEAD
    sdf_, _ = se_fold(r_anchor[pu.ins], r_anchor[pu.ins], pu.is_years)
    g7 = float(max(abs(sdb), abs(mdb), abs(sdi), abs(mdi), abs(np.nan_to_num(sdf_))))
    gate("G7", "degenerate pair (pick book == anchor book): d and SE(d) == 0 on ALL 3 bases",
         g7, g7 == 0.0)

    rng8 = np.random.default_rng(seed_of("G8det"))
    R8 = np.column_stack([r_anchor[pu.ins][block_index(rng8, T_is, 63, 1)[0]] for _ in range(5)])
    d1 = pboot(R8, CH_HEAD, 63, 424242, 0, 1, B=200)
    d2 = pboot(R8, CH_HEAD, 63, 424242, 0, 1, B=200)
    g8d = float(max(np.abs(d1[0] - d2[0]).max(), abs(d1[1] - d2[1]), abs(d1[2] - d2[2])))
    gate("G8d", "bootstrap determinism at fixed seed (P_boot AND SE)", g8d, g8d == 0.0)
    P("")

    # ---------------------------------------------------------------- build the rung books
    P("-" * 100)
    P("BUILDING 1101's RUNG BOOKS (3 panels x 2 anchors x 4 ladders, anchor rung shared).")
    P("-" * 100)
    BOOKS = {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                BOOKS[(pn, an, lad)] = ladder_books(PAN[pn], an, lad)
        P(f"  {pn}: built  ({time.time() - t0:.0f}s)")
    P("")

    # ---------------------------------------------------------------- ARM A: the 72 decisions
    P("-" * 100)
    P("ARM A — THE SAME 72 DECISIONS, now carrying d, SE(d) on THREE bases, and t = d/SE.")
    P("-" * 100)
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
                    vals = np.array([is_stat_on(bk[r][pan.ins], ch) for r in rungs], float)
                    pick_i = int(np.nanargmax(vals))
                    d_obs = float(vals[pick_i] - vals[ai])
                    sv = np.sort(vals[np.isfinite(vals)])
                    margin = float(sv[-1] - sv[-2]) if len(sv) > 1 else np.nan
                    # BLOCK basis uses 1154's EXACT seed, so P_pick is 1154's number
                    pb, se_b, _ = pboot(R, ch, L_BLOCK, seed_of(pn, an, lad, ch, L_BLOCK),
                                        pick_i, ai)
                    _, se_i, _ = pboot(R, ch, 1, seed_of(pn, an, lad, ch, "IID"), pick_i, ai)
                    se_fold.stat = ch
                    se_f, nf = se_fold(bk[rungs[pick_i]][pan.ins], bk[rungs[ai]][pan.ins],
                                       pan.is_years)
                    row = dict(panel=pn, anchor=an, ladder=lad, chooser=ch,
                               k_rungs=len(rungs), anchor_rung=str(anch[lad]),
                               pick_rung=str(rungs[pick_i]), reached=bool(pick_i == ai),
                               d_obs=d_obs, is_margin=margin,
                               P_pick=float(pb[pick_i]), P_anchor=float(pb[ai]),
                               SE_BLOCK=se_b, SE_IID=se_i, SE_FOLD=se_f, n_folds=nf)
                    for bs in BASES:
                        se = row[bs]
                        row["t_" + bs] = (d_obs / se) if (se and np.isfinite(se) and se > 0) else (
                            0.0 if d_obs == 0.0 else np.inf)
                    drows.append(row)
        P(f"  {pn}: 24 decisions scored  ({time.time() - t0:.0f}s)")
    ddf = pd.DataFrame(drows)
    dump(ddf, "decisions")

    g5 = float((ddf.d_obs < -1e-15).sum())
    gate("G9", "d = stat(argmax) - stat(anchor) >= 0 at all 72 decisions", g5, g5 == 0)
    ordv = float(((ddf.SE_IID <= ddf.SE_BLOCK + 1e-12) | (ddf.d_obs == 0)).mean())
    P(f"  SE ordering realised: SE_IID <= SE_BLOCK at {ordv:.4f} of decisions "
      f"(data-free expectation: iid understates).")
    P("")
    P("  SE LEVELS BY BASIS (over the 59 decisions where the argmax is NOT the anchor):")
    mv = ddf[~ddf.reached]
    for bs in BASES:
        P(f"    {bs:<9s} median {mv[bs].median():.6f}   mean {mv[bs].mean():.6f}   "
          f"min {mv[bs].min():.6f}   max {mv[bs].max():.6f}")
    P(f"    d_obs     median {mv.d_obs.median():.6f}   mean {mv.d_obs.mean():.6f}   "
      f"min {mv.d_obs.min():.6f}   max {mv.d_obs.max():.6f}")
    P("")
    P("  t = d/SE, the quantity the queue's rule actually thresholds:")
    for bs in BASES:
        c = mv["t_" + bs].replace([np.inf, -np.inf], np.nan)
        P(f"    t_{bs:<9s} median {c.median():.4f}   mean {c.mean():.4f}   "
          f"max {c.max():.4f}   share >= 1: {(c >= 1).mean():.4f}   >= 2: {(c >= 2).mean():.4f}")
    P("")
    P(f"  HEADLINE CELL (C_STRICT = anchor A x {CH_HEAD}, 1101/1154's basis), 12 decisions:")
    hd = ddf[(ddf.anchor == "A") & (ddf.chooser == CH_HEAD)]
    P(hd[["panel", "ladder", "anchor_rung", "pick_rung", "reached", "d_obs", "P_pick",
          "SE_BLOCK", "SE_IID", "SE_FOLD", "t_SE_BLOCK", "t_SE_FOLD"]]
      .to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    P("")

    # is the SE bar a re-labelling of the margin, or of P_boot?
    ok = ddf.is_margin.notna()
    sp_mp = float(np.corrcoef(ddf.loc[ok, "is_margin"].rank(), ddf.loc[ok, "P_pick"].rank())[0, 1])
    P(f"  Spearman(IS margin, P_pick) = {sp_mp:.4f}   (1154 committed {A1154_SPEARMAN:.4f})")
    for bs in BASES:
        t = ddf["t_" + bs].replace([np.inf, -np.inf], np.nan)
        o = t.notna() & ddf.is_margin.notna()
        r1 = float(np.corrcoef(t[o].rank(), ddf.loc[o, "is_margin"].rank())[0, 1])
        r2 = float(np.corrcoef(t[o].rank(), ddf.loc[o, "P_pick"].rank())[0, 1])
        P(f"  Spearman(t_{bs}, margin) = {r1:+.4f}   Spearman(t_{bs}, P_pick) = {r2:+.4f}")
    P("  -> a THIRD reading is only worth having if it is not a re-labelling of either; the")
    P("     correlations above are the honest answer to that and are published whichever way")
    P("     they fall.")
    P("")

    # ---------------------------------------------------------------- ARM B: the 18-cell grid
    P("-" * 100)
    P("ARM B — THE MOVE DECISION AT ALL 18 DIAL CELLS (nothing selected on).")
    P("-" * 100)

    def moves_for(rule, basis=None, k=None):
        """Boolean move decision per decision row, for any rule."""
        if rule == "R_RAW":
            return np.ones(len(ddf), bool)
        if rule == "R_ANCHOR":
            return np.zeros(len(ddf), bool)
        if rule == "R_BAR":
            return (ddf.P_pick.values >= BAR_HI)
        se = ddf[basis].values
        d = ddf.d_obs.values
        thr = k * se
        thr = np.where(np.isfinite(thr), thr, np.inf)
        return d >= thr

    mrows = []
    for bs in BASES:
        for k in KS:
            mv_ = moves_for("R_SE", bs, k)
            eff = mv_ & (~ddf.reached.values)          # a "move" onto the anchor is a no-op
            mrows.append(dict(basis=bs, k=k, n=len(ddf), n_move=int(mv_.sum()),
                              n_effective_move=int(eff.sum()),
                              move_rate=float(mv_.mean())))
    mdf = pd.DataFrame(mrows)
    P(mdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(mdf, "movegrid")
    bad = 0
    for bs in BASES:
        v = mdf[mdf.basis == bs].sort_values("k").n_move.values
        bad += int((np.diff(v) > 0).sum())
    gate("G11", "R_SE move count NON-INCREASING in k at every basis", float(bad), bad == 0)
    P("")

    # ---------------------------------------------------------------- ARM C: rule 8
    P("-" * 100)
    P("ARM C — RULE 8 WALK-FORWARD.  Every pick chosen on 2009-2016 ALONE; 2017-2026 read ONCE.")
    P("-" * 100)
    P("    R_RAW      publish the IS argmax, always            (the record's habit)")
    P("    R_BAR      publish it only if P_pick >= 0.90        (1154's rank bar)")
    P("    R_ANCHOR   never move                               (1155's do-nothing control)")
    P("    R_SE(k,b)  publish it only if d >= k * SE_b(d)      (THIS RUN'S third rule)")

    # per-panel comparands, printed as protocol rule 3 requires
    SB, LBM = {}, {}
    for pn in PANELS:
        pan = PAN[pn]
        SB[pn] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lbk = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        LBM[pn] = blocks_m(np.nan_to_num(lbk), pan.warm, pan.ins, pan.oos)
    P("")
    P("  COMPARANDS (protocol rule 3), full sample and OOS:")
    P(f"  {'panel':<7s} {'who':<22s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} "
      f"{'OOS_CAGR':>9s} {'OOS_Sh':>8s} {'OOS_DD':>8s}")
    crows = []
    for pn in PANELS:
        for who, m in (("SPY buy-and-hold", SB[pn]), ("RULES v2 baseline (live)", LBM[pn])):
            crows.append(dict(panel=pn, who=who, **{q: m[q] for q in
                              ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}))
            P(f"  {pn:<7s} {who:<22s} {m['CAGR']:>8.4f} {m['Sharpe']:>8.4f} {m['MaxDD']:>8.4f} "
              f"{m['OOS_CAGR']:>9.4f} {m['OOS_Sharpe']:>8.4f} {m['OOS_MaxDD']:>8.4f}")
    dump(pd.DataFrame(crows), "comparands")

    # metrics of every candidate book, cached once
    MET = {}
    for i, row in ddf.iterrows():
        pan = PAN[row.panel]
        bk = BOOKS[(row.panel, row.anchor, row.ladder)]
        for rung in LADDERS[row.ladder]:
            key = (row.panel, row.anchor, row.ladder, str(rung))
            if key not in MET:
                MET[key] = blocks_m(bk[rung], pan.warm, pan.ins, pan.oos)

    def bookkey(row, moved):
        rung = row.pick_rung if moved else row.anchor_rung
        return (row.panel, row.anchor, row.ladder, rung)

    def book_ident(row, moved):
        """The DISTINCT BOOK a selection lands on: (panel, N, H, GROSS, CADENCE)."""
        anch = ANCHORS[row.anchor]
        kw = dict(N=anch["N"], H=anch["H"], GROSS=anch["GROSS"], CADENCE=anch["CADENCE"])
        if moved:
            rung = row.pick_rung
            kw[row.ladder] = float(rung) if row.ladder == "GROSS" else (
                rung if row.ladder == "CADENCE" else int(rung))
        return (row.panel, kw["N"], kw["H"], kw["GROSS"], kw["CADENCE"])

    ALLRULES = [("R_RAW", None, None), ("R_BAR", None, None), ("R_ANCHOR", None, None)]
    ALLRULES += [("R_SE", bs, k) for bs in BASES for k in KS]

    wrows = []
    for rule, bs, k in ALLRULES:
        mv_ = moves_for(rule, bs, k)
        label = rule if rule != "R_SE" else f"R_SE[{bs},k={k}]"
        for i, (_, row) in enumerate(ddf.iterrows()):
            moved = bool(mv_[i])
            m = MET[bookkey(row, moved)]
            f4b = legs_4b(m, SB[row.panel])
            o4b = legs_4b_oos(m, SB[row.panel])
            f4a = legs_4a(m, LBM[row.panel])
            wrows.append(dict(
                rule=label, family=rule, basis=bs if bs else "", k=k if k is not None else np.nan,
                panel=row.panel, anchor=row.anchor, ladder=row.ladder, chooser=row.chooser,
                chosen_rung=(row.pick_rung if moved else row.anchor_rung),
                moved=bool(moved and not row.reached),
                book_id="|".join(str(x) for x in book_ident(row, moved)),
                d_obs=row.d_obs, P_pick=row.P_pick,
                OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                pass_4b_full=all(f4b.values()), pass_4b_oos=all(o4b.values()),
                pass_4a=all(f4a.values()), **f4b, **o4b, **f4a))
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")

    # --- the identity gates on the family endpoints ---
    raw_sel = wdf[wdf.rule == "R_RAW"].chosen_rung.values
    anc_sel = wdf[wdf.rule == "R_ANCHOR"].chosen_rung.values
    e0 = 0
    for bs in BASES:
        e0 += int((wdf[wdf.rule == f"R_SE[{bs},k=0.0]"].chosen_rung.values != raw_sel).sum())
    gate("G5", "R_SE(k=0) selections == R_RAW selections at all 72 x 3 bases", float(e0), e0 == 0)
    einf = 0
    for bs in BASES:
        mvinf = moves_for("R_SE", bs, K_INF)
        sel = np.array([(r.pick_rung if mvinf[i] else r.anchor_rung)
                        for i, (_, r) in enumerate(ddf.iterrows())])
        einf += int((sel != anc_sel).sum())
    gate("G6", f"R_SE(k={K_INF:.0e}) selections == R_ANCHOR at all 72 x 3 bases",
         float(einf), einf == 0)

    # --- cross-run gate on 1154's three committed rows ---
    g8 = 0.0
    for r in RULES_PUB:
        sub = wdf[wdf.rule == r]
        g8 = max(g8, abs(float(sub.OOS_Sharpe.mean()) - A1154_MEANOOS[r]),
                 abs(float(sub.pass_4b_full.sum()) - A1154_4BFULL[r]) / 100.0)
    gate("G8", "CROSS-RUN 1154's R_RAW/R_BAR/R_ANCHOR mean OOS Sharpe AND 4b-full counts",
         g8, g8 < 5e-4)

    P("")
    P("  EVERY RULE, EVERY DIAL CELL — 21 published rows, nothing selected on:")
    P(f"  {'rule':<22s} {'n':>3s} {'moved':>6s} {'mOOS_S':>8s} {'mOOS_CAGR':>10s} {'mOOS_DD':>9s} "
      f"{'mSharpe':>8s} {'4b_full':>8s} {'4b_oos':>7s} {'4a':>3s} {'books':>6s} {'4b_books':>9s}")
    srows = []
    for rule, bs, k in ALLRULES:
        label = rule if rule != "R_SE" else f"R_SE[{bs},k={k}]"
        sub = wdf[wdf.rule == label]
        nb = sub.book_id.nunique()
        nb4 = sub.loc[sub.pass_4b_full, "book_id"].nunique()
        row = dict(rule=label, family=rule, basis=bs if bs else "", k=k if k is not None else np.nan,
                   n=len(sub), n_moved=int(sub.moved.sum()),
                   mean_OOS_Sharpe=sub.OOS_Sharpe.mean(), mean_OOS_CAGR=sub.OOS_CAGR.mean(),
                   mean_OOS_MaxDD=sub.OOS_MaxDD.mean(), mean_Sharpe=sub.Sharpe.mean(),
                   mean_CAGR=sub.CAGR.mean(), mean_MaxDD=sub.MaxDD.mean(),
                   n_4b_full=int(sub.pass_4b_full.sum()), n_4b_oos=int(sub.pass_4b_oos.sum()),
                   n_4a=int(sub.pass_4a.sum()),
                   n_distinct_books=nb, n_distinct_4b_books=nb4)
        srows.append(row)
        P(f"  {label:<22s} {len(sub):>3d} {int(sub.moved.sum()):>6d} {sub.OOS_Sharpe.mean():>8.4f} "
          f"{sub.OOS_CAGR.mean():>10.4f} {sub.OOS_MaxDD.mean():>9.4f} {sub.Sharpe.mean():>8.4f} "
          f"{int(sub.pass_4b_full.sum()):>8d} {int(sub.pass_4b_oos.sum()):>7d} "
          f"{int(sub.pass_4a.sum()):>3d} {nb:>6d} {nb4:>9d}")
    sdf = pd.DataFrame(srows)
    dump(sdf, "rule8")

    # --- monotonicity of the OOS profile in k: the falsifier declared in Arm 0 ---
    P("")
    P("  IS THE OOS PROFILE MONOTONE IN k?  (Arm 0's falsifier: an INTERIOR k must beat BOTH")
    P("  endpoints for the SE bar to be a rule rather than a dimmer switch.)")
    P(f"  {'basis':<9s} {'k=0(=R_RAW)':>12s} {'0.25':>8s} {'0.5':>8s} {'1.0':>8s} {'1.5':>8s} "
      f"{'2.0':>8s} {'inf(=R_ANCHOR)':>15s} {'interior>both?':>15s}")
    anc_oos = float(wdf[wdf.rule == "R_ANCHOR"].OOS_Sharpe.mean())
    raw_oos = float(wdf[wdf.rule == "R_RAW"].OOS_Sharpe.mean())
    nonmono = []
    for bs in BASES:
        vs = [float(sdf[(sdf.basis == bs) & (sdf.k == k)].mean_OOS_Sharpe.iloc[0]) for k in KS]
        interior = max(vs[1:])                       # k > 0, finite
        beats = bool(interior > max(raw_oos, anc_oos) + 1e-12)
        nonmono.append(beats)
        P(f"  {bs:<9s} {vs[0]:>12.4f} {vs[1]:>8.4f} {vs[2]:>8.4f} {vs[3]:>8.4f} {vs[4]:>8.4f} "
          f"{vs[5]:>8.4f} {anc_oos:>15.4f} {str(beats):>15s}")
    P(f"  R_RAW endpoint {raw_oos:.4f};  R_ANCHOR endpoint {anc_oos:.4f}.")

    # --- paired comparison against the do-nothing control, SE clustered on (panel, anchor) ---
    P("")
    P("  PAIRED vs R_ANCHOR over the SAME 72 decisions, SE clustered on (panel, anchor) —")
    P(f"  {len(PANELS) * len(ANCHORS)} clusters, which is the honest count and is SMALL; the t's below are")
    P("  reported with that stated, not dressed up.")
    base_oos = wdf[wdf.rule == "R_ANCHOR"].set_index(
        ["panel", "anchor", "ladder", "chooser"]).OOS_Sharpe
    prows = []
    P(f"  {'rule':<22s} {'d_meanOOS_S':>12s} {'clSE':>8s} {'t':>7s} {'n_clusters':>11s} "
      f"{'win_cells':>10s}")
    for rule, bs, k in ALLRULES:
        label = rule if rule != "R_SE" else f"R_SE[{bs},k={k}]"
        sub = wdf[wdf.rule == label].set_index(["panel", "anchor", "ladder", "chooser"])
        dvec = (sub.OOS_Sharpe - base_oos).dropna()
        gl = dvec.groupby(level=[0, 1]).mean()
        cl = len(gl)
        se = float(gl.std(ddof=1) / np.sqrt(cl)) if cl > 1 else np.nan
        mu = float(dvec.mean())
        t = mu / se if se and se > 0 else (0.0 if mu == 0 else np.inf)
        prows.append(dict(rule=label, family=rule, basis=bs if bs else "",
                          k=k if k is not None else np.nan,
                          d_mean_OOS_Sharpe=mu, clustered_SE=se, t=t, n_clusters=cl,
                          n_cells_better=int((dvec > 0).sum()),
                          n_cells_worse=int((dvec < 0).sum())))
        P(f"  {label:<22s} {mu:>12.4f} {se:>8.4f} {t:>7.2f} {cl:>11d} "
          f"{int((dvec > 0).sum()):>4d}/{int((dvec < 0).sum()):<5d}")
    pdf = pd.DataFrame(prows)
    dump(pdf, "paired")
    best = pdf[pdf.family == "R_SE"].nlargest(1, "d_mean_OOS_Sharpe").iloc[0]
    P(f"  BEST R_SE cell over the whole 18-cell grid: {best.rule}  "
      f"delta {best.d_mean_OOS_Sharpe:+.4f} vs do-nothing, clustered SE {best.clustered_SE:.4f}, "
      f"t {best.t:+.2f}.")
    P("  And that BEST cell is a MAXIMUM OVER 18 CELLS, so even its own t is optimistic; it is")
    P("  published as the ceiling of what the rule could be worth, not as a measurement.")
    P("")

    # ---------------------------------------------------------------- ARM D: the 18 books
    P("-" * 100)
    P("ARM D — THE QUEUE'S QUESTION, ANSWERED IN BOOKS RATHER THAN IN DECISION ROWS.")
    P("-" * 100)
    P("  The queue asks whether R_SE 'recovers any of the 18 capital-worthy books the record's")
    P("  habit loses', reading 1154's 4b-full counts 6 (R_RAW) vs 24 (R_ANCHOR).  Those are")
    P("  counts of DECISION ROWS.  Here is what they are in DISTINCT BOOKS:")
    arows = []
    for rule, bs, k in ALLRULES:
        label = rule if rule != "R_SE" else f"R_SE[{bs},k={k}]"
        sub = wdf[wdf.rule == label]
        ps = sub[sub.pass_4b_full]
        arows.append(dict(rule=label, family=rule, basis=bs if bs else "",
                          k=k if k is not None else np.nan,
                          rows_4b_full=len(ps), distinct_books_4b_full=ps.book_id.nunique(),
                          distinct_books_selected=sub.book_id.nunique(),
                          books=";".join(sorted(ps.book_id.unique()))))
    adf = pd.DataFrame(arows)
    P(adf[["rule", "rows_4b_full", "distinct_books_4b_full", "distinct_books_selected"]]
      .to_string(index=False))
    dump(adf, "bookaudit")

    anc_books = set(wdf[(wdf.rule == "R_ANCHOR") & wdf.pass_4b_full].book_id.unique())
    raw_books = set(wdf[(wdf.rule == "R_RAW") & wdf.pass_4b_full].book_id.unique())
    P("")
    P(f"  R_ANCHOR's {A1154_4BFULL['R_ANCHOR']} 4b-full ROWS are {len(anc_books)} DISTINCT BOOK(S):")
    for bkid in sorted(anc_books):
        P(f"    {bkid}")
    P(f"  R_RAW's {A1154_4BFULL['R_RAW']} 4b-full ROWS are {len(raw_books)} DISTINCT BOOK(S):")
    for bkid in sorted(raw_books):
        P(f"    {bkid}")
    lost = anc_books - raw_books
    P(f"  So the '18 lost books' is {len(lost)} book(s): {sorted(lost) if lost else 'none'}.")
    gate("G12", f"R_ANCHOR's 72 selections are exactly {len(PANELS) * len(ANCHORS)} distinct books",
         float(wdf[wdf.rule == "R_ANCHOR"].book_id.nunique()),
         wdf[wdf.rule == "R_ANCHOR"].book_id.nunique() == len(PANELS) * len(ANCHORS))

    # which rules recover the lost book(s), and by what mechanism
    P("")
    P("  DOES ANY R_SE CELL RECOVER THEM, AND HOW?  A rule 'recovers' a lost book only by NOT")
    P("  MOVING off it, so the question is really: at what k does the rule stop moving there?")
    rrows = []
    for rule, bs, k in ALLRULES:
        label = rule if rule != "R_SE" else f"R_SE[{bs},k={k}]"
        sub = wdf[wdf.rule == label]
        got = set(sub[sub.pass_4b_full].book_id.unique())
        rrows.append(dict(rule=label, family=rule, basis=bs if bs else "",
                          k=k if k is not None else np.nan,
                          n_lost_recovered=len(lost & got), n_lost=len(lost),
                          recovered_by_staying=len(lost & got),
                          new_4b_books_not_in_either=len(got - anc_books - raw_books)))
        P(f"    {label:<22s} recovers {len(lost & got)}/{len(lost)} of the lost book(s); "
          f"NEW 4b books neither control found: {len(got - anc_books - raw_books)}")
    dump(pd.DataFrame(rrows), "recovery")
    P("")

    # ---------------------------------------------------------------- ARM E: both KEEP paths
    P("-" * 100)
    P("ARM E — BOTH KEEP PATHS on ALL distinct rung books (protocol rule 4; nothing selected on).")
    P("-" * 100)
    brows = []
    for pn in PANELS:
        pan = PAN[pn]
        seen = set()
        for an in ANCHORS:
            anch = ANCHORS[an]
            for lad in LADNAMES:
                for rung in LADDERS[lad]:
                    kw = dict(N=anch["N"], H=anch["H"], GROSS=anch["GROSS"], CADENCE=anch["CADENCE"])
                    kw[lad] = rung
                    key = (pn, kw["N"], kw["H"], kw["GROSS"], kw["CADENCE"])
                    if key in seen:
                        continue
                    seen.add(key)
                    m = blocks_m(BOOKS[(pn, an, lad)][rung], pan.warm, pan.ins, pan.oos)
                    f4b, o4b, f4a = legs_4b(m, SB[pn]), legs_4b_oos(m, SB[pn]), legs_4a(m, LBM[pn])
                    brows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung),
                                      N=kw["N"], H=kw["H"], GROSS=kw["GROSS"], CADENCE=kw["CADENCE"],
                                      **{q: m[q] for q in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                                      pass_4b_full=all(f4b.values()), pass_4b_oos=all(o4b.values()),
                                      pass_4a=all(f4a.values()), **f4b, **o4b, **f4a))
    bdf = pd.DataFrame(brows)
    dump(bdf, "books")
    P(f"  {len(bdf)} distinct rung books.")
    P(f"  4a {int(bdf.pass_4a.sum())} of {len(bdf)};  4b full {int(bdf.pass_4b_full.sum())};  "
      f"4b OOS {int(bdf.pass_4b_oos.sum())};  BOTH "
      f"{int((bdf.pass_4b_full & bdf.pass_4b_oos).sum())}")
    for pn in PANELS:
        sub = bdf[bdf.panel == pn]
        P(f"    {pn:<6s} n={len(sub):<3d}  4a {int(sub.pass_4a.sum()):>2d}  "
          f"4b full {int(sub.pass_4b_full.sum()):>2d}  4b OOS {int(sub.pass_4b_oos.sum()):>2d}  "
          f"leg rates: H1 {sub.L_H1.mean():.3f} H2 {sub.L_H2.mean():.3f} OOS {sub.L_OOS.mean():.3f} "
          f"DD {sub.L_DD.mean():.3f} CAGR {sub.L_CAGR.mean():.3f}")
    pas = bdf[bdf.pass_4b_full & bdf.pass_4b_oos]
    if len(pas):
        P("")
        P("  BOOKS CLEARING 4b ON BOTH READINGS (full sample AND OOS):")
        P(pas[["panel", "N", "H", "GROSS", "CADENCE", "CAGR", "Sharpe", "MaxDD",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    hl = sdf[(sdf.basis == BASIS_HEAD) & (sdf.k == K_HEAD)].iloc[0]
    hp = pdf[(pdf.basis == BASIS_HEAD) & (pdf.k == K_HEAD)].iloc[0]
    P(f"  HEADLINE R_SE[{BASIS_HEAD}, k={K_HEAD}]: moves {int(hl.n_moved)} of 72 decisions, "
      f"mean OOS Sharpe {hl.mean_OOS_Sharpe:.4f} / CAGR {hl.mean_OOS_CAGR:.4f} / "
      f"MaxDD {hl.mean_OOS_MaxDD:.4f};")
    P(f"  4b-full {int(hl.n_4b_full)} rows = {int(hl.n_distinct_4b_books)} distinct books; "
      f"4a {int(hl.n_4a)}.")
    P(f"  vs R_RAW {raw_oos:.4f} / R_BAR "
      f"{float(sdf[sdf.rule == 'R_BAR'].mean_OOS_Sharpe.iloc[0]):.4f} / "
      f"R_ANCHOR {anc_oos:.4f} mean OOS Sharpe.")
    P(f"  Paired vs do-nothing: {hp.d_mean_OOS_Sharpe:+.4f}, clustered SE {hp.clustered_SE:.4f}, "
      f"t {hp.t:+.2f} on {int(hp.n_clusters)} clusters.")
    P(f"  INTERIOR k BEATS BOTH ENDPOINTS at {sum(nonmono)} of {len(BASES)} bases "
      f"({dict(zip(BASES, nonmono))}).")
    P(f"  THE '18 BOOKS': R_ANCHOR's {A1154_4BFULL['R_ANCHOR']} 4b rows are {len(anc_books)} "
      f"distinct book(s), R_RAW's {A1154_4BFULL['R_RAW']} are {len(raw_books)}; the gap is "
      f"{len(lost)} book(s), not 18.")
    P(f"  KEEP: 4a {int(bdf.pass_4a.sum())} of {len(bdf)}; 4b full {int(bdf.pass_4b_full.sum())}; "
      f"4b OOS {int(bdf.pass_4b_oos.sum())}; BOTH {int((bdf.pass_4b_full & bdf.pass_4b_oos).sum())}.")
    P("")
    P("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current")
    P("  output of a sub-$2B screen less the documented max_1d_move >= 1.0 exclusion.  Every")
    P("  LEVEL is optimistic and every 4a/4b count is an UPPER bound.  The RULE COMPARISON is a")
    P("  DIFFERENCE between selections on the SAME panel and is far less exposed; the levels are")
    P("  published beside it anyway.")
    P("")
    P("  DECLARED APPROXIMATIONS, and their direction:")
    P("   (1) SE_BLOCK and SE_IID resample ONE tape, so they price sampling error around THIS")
    P("       regime and not regime uncertainty.  Both therefore UNDERSTATE SE(d), which makes")
    P("       R_SE MOVE MORE OFTEN than it should — the direction that FAVOURS the record's")
    P("       habit.  SE_FOLD is the corrective basis and is published beside them.")
    P("   (2) The 72 decisions are NOT 72 independent draws: they share panels, anchors and")
    P("       books.  Every clustered SE here uses the 6 (panel, anchor) clusters, and 6 is a")
    P("       small number of clusters; a t near 2 on 6 clusters is NOT a 95% statement.")
    P("   (3) The best R_SE cell is a MAXIMUM OVER 18, reported as a ceiling, never as a pick.")

    gdf2 = pd.DataFrame(GATES)
    dump(gdf2, "gates")
    P(f"  GATES {int(gdf2.pass_.sum())} of {len(gdf2)}")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    P(f"\n  total {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 1248 (lane C, 2026-09-17) — is the DETECTION CURVE'S LONG-END CONCENTRATION a
BLOCK-FRACTION (L/T) LAW?

THE PREMISE, READ FROM THE RECORD.  Idea 1208 (lane B) established that the block length L is
the record's largest unstated resampling dial: on one fixed object — 72 pick decisions
(3 panels x 2 anchors x 4 ladders x 3 choosers) — the resolution rate runs 0.1528 -> 1.0000
monotonically over L = 1 .. T.  Idea 1243 (lane cloud) then priced a "state a ladder" schema
clause on the SAME object and found the ladder's whole buy sits at the LONG end: per-rung
contribution against the record's frozen point L = 63 runs

    L      = 42  126   21    5   10  252    2    1  504  1008    T
    c(L)   =  0    1    2    3    3    4    5    6    7    15    55      (of 72 decisions)

monotone at the long end, ragged at the short end, and 0.9016 of the 12-rung detection carried
by L = T alone.  1243 read that as "the clause's value is monotone in how close its widest rung
sits to the degenerate one" — i.e. it CONJECTURED a law in the BLOCK FRACTION f = L / T and did
not test it, because it only ever ran one T.

WHAT THIS RUN TESTS.  Whether the detection curve is a function of the block FRACTION f = L / T
alone, by re-running the identical construction on IS windows of DIFFERENT LENGTHS.  If the law
is fractional, then the same f reached by different absolute L must give the same resolution
rate, and the same absolute L at different T must NOT.  This is a falsifiable, one-shot test:
the fractions are matched BY CONSTRUCTION (a fraction-keyed rung set), so no interpolation and
no curve fitting is needed to compare cells.

WHY IT MATTERS BEYOND BOOKKEEPING.  Every resampling verdict in the record is quoted at an
absolute L (almost always 63, inherited from 1101 without argument) on whatever window the run
happened to have.  If resolution is a fraction law, an absolute L is the WRONG unit: the same
L = 63 means a 0.036 block on the full IS window and a 0.250 block on a one-year window, so two
runs quoting the same L are not quoting the same test, and the record's L = 63 verdicts are not
comparable across windows.  If it is NOT a fraction law, the record's absolute-L habit is
defensible and 1243's conjecture is refuted.

PRE-DECLARED OUTCOMES (fixed before any number is read; the verdict is READ OFF, not chosen).
  (F) FRACTION LAW — at matched f, the max spread of the resolution rate across window lengths
      is <= 0.10 in EVERY panel, AND that matched-f spread is strictly smaller than the spread
      at matched absolute L.  One L/T law predicts all three panels.
  (P) FRACTION PLUS PANEL — matched-f spread across windows <= 0.10 WITHIN each panel, but the
      spread ACROSS panels at matched f exceeds 0.10.  f is the right unit; the panel is a
      separate term and a single curve does not predict all three.
  (N) NO SINGLE LAW — matched-f spread across windows exceeds 0.10 inside at least one panel.
      Resolution is neither an absolute-L nor an f law on this object.
  The 0.10 bar is declared here and is NOT moved (rule 7).  G4 measures seed noise on the same
  object so the bar can be read against it; if seed noise alone exceeded 0.10 the test would be
  void and that is reported, not repaired.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  WINDOW LENGTH  {W252, W504, W1008, WFULL} — the IS window is the LAST W rows of the panel's
                 warm-up..2016-12-31 block (rule 8's IS end is never crossed).  WFULL is the
                 record's own window, so 1208/1243's published ladder must replay in that cell.
  PANEL          {U56, B136, SMALL} — the queue's second dial; also rule 9's survivorship axis.
  All 12 (window x panel) cells are published.

NOT DIALS, REPORTED AT EVERY VALUE: the RUNG KEYING is the measurement axis, not a tuned
parameter, and both keyings are published in full —
  ABS   the record's own 12 rungs [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008, T], clipped to
        rungs <= W (a block longer than the window IS the identity redraw and is reported as
        such, not silently clamped);
  FRAC  fraction-keyed rungs f in [0.0006, 0.002, 0.005, 0.01, 0.02, 0.04, 0.08, 0.15, 0.30,
        0.60, 1.00] -> L = clip(round(f * W), 1, W).  Identical f in every cell by construction.
Also not dials: ANCHOR {A, B}; the four ladders N / H / GROSS / CADENCE; the three choosers
CH_ISSHARPE / CH_ISCAGR / CH_ISDD; the resolution bar q = 0.90 (1208's, always published);
B = 1000 draws (1208's); the 4a and 4b legs.

FROZEN AT THE RECORD'S CONSTRUCTION: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, 10 bps (rule 2), decide-at-t / apply-at-t+1, warm-up 260 rows,
IS end 2016-12-31 (rule 8), the two anchors A and B, the four ladders' rungs.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every pick made on ITS OWN IS
window only and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every
rung book and on every rule-8 row; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only).
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
SLUG = "is-the-DETECTION-CURVE-s-LONG-END-CONCENTRATION-a-BLOCK-FRACTION-LAW"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

# ------------------------------------------------------------------ 1101/1208/1243 construction
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
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

# ------------------------------------------------------------------ the two dials
WINDOWS = ["W252", "W504", "W1008", "WFULL"]      # dial 1
WLEN = {"W252": 252, "W504": 504, "W1008": 1008, "WFULL": None}   # None = the panel's full IS
# measurement axis (published in full, not tuned)
RUNGS_ABS = [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008, "T"]
FRACS = [0.0006, 0.002, 0.005, 0.01, 0.02, 0.04, 0.08, 0.15, 0.30, 0.60, 1.00]
BAR_HI = 0.90
BDRAWS = 1000
SEED_BASE = 12481248
L_HEAD = 63                                        # the record's frozen absolute point
SPREAD_BAR = 0.10                                  # pre-declared, never moved

# ------------------------------------------------------------------ the record's own numbers
A1208_RATES = {1: 0.1528, 2: 0.1667, 5: 0.1667, 10: 0.1806, 21: 0.1944, 42: 0.2222,
               63: 0.2222, 126: 0.2361, 252: 0.2778, 504: 0.3194, 1008: 0.4722, "T": 1.0000}
A1243_CONTRIB = {42: 0, 126: 1, 21: 2, 5: 3, 10: 3, 252: 4, 2: 5, 1: 6, 504: 7, 1008: 15,
                 "T": 55}
A1208_NDEC = 72
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<70s} {value:.4e}")
    return bool(ok)


# ================================================================== the record's runner
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
        # dial 1: the IS window is the LAST W rows of the panel's warm-up..IS_END block
        pos = np.flatnonzero(self.ins)
        self.T_is = len(pos)
        self.win = {}
        for w in WINDOWS:
            n = self.T_is if WLEN[w] is None else min(WLEN[w], self.T_is)
            m = np.zeros(len(px.index), dtype=bool)
            m[pos[-n:]] = True
            self.win[w] = m


def book(pan, N, H, gross, freq):
    """Decide at the rebalance close t, apply at t+1 (rule 2), 10 bps on turnover."""
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def ladder_books(pan, anchor, lad, cache):
    a = ANCHORS[anchor]
    out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        key = (pan.name, kw["N"], kw["H"], kw["gross"], kw["freq"])
        if key not in cache:
            cache[key] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
        out[rung] = cache[key]
    return out


# ================================================================== the block bootstrap
def block_index(rng, T, L, B):
    """(B, T) moving-block index; blocks with replacement, no wrap (1101's construction)."""
    L = int(min(max(L, 1), T))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def pboot_argmax(R, stat, L, seed, B=BDRAWS, chunk=250):
    """P(each rung is the argmax of `stat`) under JOINT moving-block redraws of the IS window.
    One block index per draw is applied to ALL rungs, so cross-rung correlation survives."""
    T, k = R.shape
    rng = np.random.default_rng(seed)
    cnt = np.zeros(k)
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
        v = np.where(np.isfinite(v), v, -np.inf)
        cnt += np.bincount(v.argmax(axis=1), minlength=k)
        done += b
    return cnt / B


def spearman(a, b):
    """Rank correlation without scipy: Pearson on ranks (ties averaged)."""
    ra = pd.Series(np.asarray(a, float)).rank().values
    rb = pd.Series(np.asarray(b, float)).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def is_stat_win(r, m, stat):
    x = np.asarray(r)[m]
    T_is = len(x)
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    if stat == "CH_ISCAGR":
        eq = np.cumprod(1.0 + x)
        return eq[-1] ** (252.0 / T_is) - 1.0
    if stat == "CH_ISDD":
        eq = np.cumprod(1.0 + x)
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


# ================================================================== 4a / 4b legs
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


# ================================================================== the run
def rung_sets(W):
    """The two keyings for a window of length W. Returns list of (keying, label, L, f)."""
    out = []
    for r in RUNGS_ABS:
        Lv = W if r == "T" else int(r)
        if r != "T" and Lv > W:
            out.append(("ABS", str(r), W, 1.0, True))       # a block longer than the window
        else:
            out.append(("ABS", str(r), Lv, Lv / W, False))
    for f in FRACS:
        Lv = int(min(max(round(f * W), 1), W))
        out.append(("FRAC", f"f{f:g}", Lv, Lv / W, False))
    return out


def main():
    t0 = time.time()
    P("=" * 110)
    P(f"IDEA 1248 (lane C, {DATE}) — is the DETECTION CURVE'S LONG-END CONCENTRATION a")
    P("BLOCK-FRACTION (L/T) LAW?")
    P("=" * 110)
    P("  dial 1 = WINDOW LENGTH  {W252, W504, W1008, WFULL}  (IS window = last W rows before "
      "2016-12-31)")
    P("  dial 2 = PANEL          {U56, B136, SMALL}")
    P("  NOT dials, published in full: RUNG KEYING {ABS = the record's 12 rungs, FRAC = 11")
    P("             fraction-keyed rungs}; 2 anchors x 4 ladders x 3 choosers = 24 decisions per")
    P(f"             (panel, window) = 288 decision-windows; q = {BAR_HI}; B = {BDRAWS}.")
    P(f"  PRE-DECLARED, BAR = {SPREAD_BAR:.2f}, NOT MOVED: (F) FRACTION LAW — matched-f spread")
    P("             across windows <= 0.10 in every panel AND smaller than the matched-absolute-L")
    P("             spread.  (P) FRACTION PLUS PANEL — holds within panels, fails across them.")
    P("             (N) NO SINGLE LAW — fails within at least one panel.")
    P("")

    # ------------------------------------------------------------ ARM A: panels and the object
    P("=" * 110)
    P("ARM A — THE OBJECT: 1208/1243's DECISIONS, REBUILT, AT FOUR IS WINDOW LENGTHS")
    P("=" * 110)
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pxs = load_universe(small=True)
    mv = pxs.pct_change().abs().max()
    drop = [c for c in pxs.columns if c != "SPY" and not (mv[c] < 1.0)]
    px["SMALL"] = pxs.drop(columns=drop)
    pans = {n: Panel(n, px[n]) for n in PANELS}
    P("")
    P(f"  PANELS: U56 {len(px['U56'].columns)-1} names; B136 {len(px['B136'].columns)-1}; "
      f"SMALL {len(px['SMALL'].columns)-1} investable ({len(drop)} dropped for "
      "max_1d_move >= 1.0); SPY is a benchmark column, never investable.")
    P("")
    P("  window lengths actually used (trading days of the IS block, ending 2016-12-31):")
    for pn in PANELS:
        pan = pans[pn]
        P(f"    {pn:6s} full IS = {pan.T_is:5d} rows   " +
          "   ".join(f"{w} = {int(pan.win[w].sum()):5d}" for w in WINDOWS))

    cache, BOOKS = {}, {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                BOOKS[(pn, an, lad)] = ladder_books(pans[pn], an, lad, cache)
    P(f"  {len(cache)} distinct rung books built across "
      f"{len(PANELS)*len(ANCHORS)*len(LADNAMES)} (panel, anchor, ladder) families.")

    a = ANCHORS["A"]
    r0 = cache[("U56", a["N"], a["H"], a["GROSS"], a["CADENCE"])]
    c0, s0, d0 = fmet(r0[pans["U56"].warm])
    dev = max(abs(c0 - A1101_TRIPLE[0]), abs(s0 - A1101_TRIPLE[1]), abs(d0 - A1101_TRIPLE[2]))
    gate("G1", "1101's committed U56 anchor triple replays (CAGR/Sharpe/MaxDD)", dev, dev < 2e-3)
    lb = backtest(px["U56"], rules_v2_weights(px["U56"]), cost_bps=COST,
                  freq="W")["returns"].values
    lmdd = fmet(lb[WARMUP:])[2]
    gate("G2", "live RULES v2 U56 MaxDD == committed -12.05%", abs(lmdd - LIVE_MAXDD_COMMITTED),
         abs(lmdd - LIVE_MAXDD_COMMITTED) < 5e-4)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    gate("G3", "decision count per window == 1208's 72", float(len(DEC)), len(DEC) == A1208_NDEC)

    # ------------------------------------------------------------ ARM B: the resolution table
    P("")
    P("=" * 110)
    P("ARM B — THE RESOLUTION TABLE: EVERY DECISION, EVERY WINDOW, BOTH KEYINGS")
    P("=" * 110)
    P("")
    P(f"  RESOLVED at rung L  <=>  P_boot(observed IS argmax) >= {BAR_HI} under a JOINT moving-")
    P(f"  block redraw of THAT WINDOW, B = {BDRAWS}, one block index per draw applied to every")
    P("  rung of the decision's ladder (1101/1208's construction, unchanged).  The IS argmax is")
    P("  recomputed on each window, so a shorter window may pick a different rung — that is part")
    P("  of what is being measured and is published.")
    cachef = Path(f"{OUT}.resolution.csv")
    if cachef.exists():
        LDF = pd.read_csv(cachef)
        LDF["rung"] = LDF["rung"].astype(str)
        P("")
        P(f"  RESOLUTION TABLE LOADED FROM {cachef.name} — the seeded output of this same")
        P("  script (deterministic: every draw is keyed by seed_of(panel, anchor, ladder,")
        P("  chooser, window, L)).  Delete that file to force a full recompute.")
        rows = None
    else:
        rows = []
    for wn in (WINDOWS if rows is not None else []):
        for (pn, an, lad, ch) in DEC:
            pan = pans[pn]
            m = pan.win[wn]
            Wl = int(m.sum())
            rungs = LADDERS[lad]
            R = np.column_stack([np.asarray(BOOKS[(pn, an, lad)][r])[m] for r in rungs])
            vals = [is_stat_win(BOOKS[(pn, an, lad)][r], m, ch) for r in rungs]
            obs = int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))
            pbc = {}
            for (key, lab, Lv, f, clamped) in rung_sets(Wl):
                if Lv not in pbc:
                    pbc[Lv] = pboot_argmax(R, ch, Lv, seed_of(pn, an, lad, ch, wn, Lv))
                pb = pbc[Lv]
                rows.append(dict(window=wn, W=Wl, panel=pn, anchor=an, ladder=lad, chooser=ch,
                                 keying=key, rung=lab, L=Lv, f=f, clamped=clamped,
                                 obs_rung=str(rungs[obs]), P_pick=float(pb[obs]),
                                 RESOLVED=bool(pb[obs] >= BAR_HI)))
        P(f"    {wn} done ({time.time()-t0:.0f}s)")
    if rows is not None:
        LDF = pd.DataFrame(rows)
        LDF.to_csv(f"{OUT}.resolution.csv", index=False)

    # --- G4: 1208/1243's own ladder must replay in the WFULL cell, ABS keying, pooled 72
    P("")
    P("  REPLAY OF THE RECORD'S PUBLISHED LADDER (WFULL, ABS keying, pooled over all 72):")
    P("    L        this run   1208's published   dev")
    devs = []
    wf = LDF[(LDF.window == "WFULL") & (LDF.keying == "ABS")]
    for L in RUNGS_ABS:
        z = wf[wf.rung == str(L)]
        rate = float(z.RESOLVED.mean())
        d = abs(rate - A1208_RATES[L])
        devs.append(d)
        P(f"    {str(L):6s}   {rate:8.4f}   {A1208_RATES[L]:16.4f}   {d:+.4f}")
    gate("G4", "1208's 12-rung resolution ladder replays in the WFULL cell (max dev)",
         max(devs), max(devs) <= 0.06)

    # --- G5: seed noise on the same object (so the 0.10 bar can be read against it)
    P("")
    P("  SEED NOISE ON THE SAME OBJECT (one cell, U56 x WFULL, FRAC keying, a second seed base):")
    sdev = []
    pan = pans["U56"]
    m = pan.win["WFULL"]
    Wl = int(m.sum())
    fr = [rs for rs in rung_sets(Wl) if rs[0] == "FRAC"]
    for (_, lab, Lv, f, _) in fr:
        res2 = []
        for (pn, an, lad, ch) in [d for d in DEC if d[0] == "U56"]:
            rungs = LADDERS[lad]
            R = np.column_stack([np.asarray(BOOKS[(pn, an, lad)][r])[m] for r in rungs])
            vals = [is_stat_win(BOOKS[(pn, an, lad)][r], m, ch) for r in rungs]
            obs = int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))
            pb = pboot_argmax(R, ch, Lv, seed_of("alt", pn, an, lad, ch, "WFULL", Lv))
            res2.append(bool(pb[obs] >= BAR_HI))
        r1 = float(LDF[(LDF.window == "WFULL") & (LDF.panel == "U56") &
                       (LDF.rung == lab)].RESOLVED.mean())
        sdev.append(abs(float(np.mean(res2)) - r1))
        P(f"    {lab:8s} L={Lv:5d}  seed A {r1:.4f}   seed B {np.mean(res2):.4f}   "
          f"dev {sdev[-1]:+.4f}")
    seed_noise = float(max(sdev))
    gate("G5", f"seed noise is below the pre-declared {SPREAD_BAR:.2f} spread bar (max dev)",
         seed_noise, seed_noise < SPREAD_BAR)

    # ------------------------------------------------------------ ARM C: the collapse test
    P("")
    P("=" * 110)
    P("ARM C — THE TEST: DOES RESOLUTION COLLAPSE ONTO A SINGLE FUNCTION OF f = L / T?")
    P("=" * 110)
    F = LDF[LDF.keying == "FRAC"]
    P("")
    P("  (C1) MATCHED f — the fraction-keyed rung set, identical in every cell by construction.")
    P("       rate = share of that cell's 24 decisions RESOLVED at the bar.")
    P("")
    P("       f          " + "   ".join(f"{pn}: " + " ".join(f"{w[1:]:>5s}" for w in WINDOWS)
                                        for pn in PANELS))
    crows = []
    for f in FRACS:
        lab = f"f{f:g}"
        line = f"       {f:<9g} "
        for pn in PANELS:
            vals = []
            for wn in WINDOWS:
                z = F[(F.panel == pn) & (F.window == wn) & (F.rung == lab)]
                vals.append(float(z.RESOLVED.mean()))
                crows.append(dict(f=f, panel=pn, window=wn, rate=vals[-1],
                                  L=int(z.L.iloc[0]), W=int(z.W.iloc[0])))
            line += "      " + " ".join(f"{v:.3f}" for v in vals)
        P(line)
    CR = pd.DataFrame(crows)
    CR.to_csv(f"{OUT}.collapse_f.csv", index=False)
    P("")
    P("       THE ABSOLUTE L EACH MATCHED f RESOLVES TO (U56 rows; the other panels differ only")
    P("       by their own trading-day counts).  Where two fractions map to the same L the low")
    P("       end is FLOORED at L = 1 and those rungs are NOT independent tests — stated, not")
    P("       hidden:")
    P("       f          " + "".join(f"{w:>10s}" for w in WINDOWS))
    for f in FRACS:
        z = CR[(CR.f == f) & (CR.panel == "U56")].set_index("window")
        P(f"       {f:<9g} " + "".join(f"{int(z.loc[w].L):10d}" for w in WINDOWS))

    P("")
    P("       SPREAD AT MATCHED f (max - min over the four window lengths), per panel:")
    P("       f          " + "".join(f"{pn:>10s}" for pn in PANELS) + "     pooled-over-panels")
    sp_f_panel = {pn: [] for pn in PANELS}
    sp_f_all = []
    for f in FRACS:
        line = f"       {f:<9g} "
        for pn in PANELS:
            v = CR[(CR.f == f) & (CR.panel == pn)].rate
            s = float(v.max() - v.min())
            sp_f_panel[pn].append(s)
            line += f"{s:10.4f}"
        v2 = CR[CR.f == f].rate
        sp_f_all.append(float(v2.max() - v2.min()))
        P(line + f"{sp_f_all[-1]:20.4f}")
    max_sp_f_within = max(max(v) for v in sp_f_panel.values())
    max_sp_f_all = max(sp_f_all)
    P("")
    P(f"       MAX matched-f spread ACROSS WINDOWS within a panel : {max_sp_f_within:.4f}")
    P(f"       MAX matched-f spread ACROSS ALL 12 CELLS           : {max_sp_f_all:.4f}")

    # cross-panel spread at matched f and matched window
    P("")
    P("  (C2) THE PANEL TERM — spread at matched f ACROSS PANELS, window by window.")
    P("       f          " + "".join(f"{w:>10s}" for w in WINDOWS))
    sp_panel = []
    for f in FRACS:
        line = f"       {f:<9g} "
        for wn in WINDOWS:
            v = CR[(CR.f == f) & (CR.window == wn)].rate
            s = float(v.max() - v.min())
            sp_panel.append(s)
            line += f"{s:10.4f}"
        P(line)
    max_sp_panel = max(sp_panel)
    P("")
    P(f"       MAX cross-PANEL spread at matched f and matched window: {max_sp_panel:.4f}")

    # matched absolute L (the record's habit) — the competing hypothesis
    P("")
    P("  (C3) MATCHED ABSOLUTE L — the record's own habit, the competing hypothesis.  Rungs")
    P("       reported only where the absolute L exists in every window (L <= 252); a rung longer")
    P("       than the window is the IDENTITY redraw and is flagged, never silently clamped.")
    A = LDF[LDF.keying == "ABS"]
    common_abs = [r for r in RUNGS_ABS if r != "T" and int(r) <= min(
        int(A[A.window == w].W.min()) for w in WINDOWS)]
    P("")
    P("       L          " + "   ".join(f"{pn}: " + " ".join(f"{w[1:]:>5s}" for w in WINDOWS)
                                        for pn in PANELS))
    arows = []
    for L in common_abs:
        line = f"       {str(L):<9s} "
        for pn in PANELS:
            vals = []
            for wn in WINDOWS:
                z = A[(A.panel == pn) & (A.window == wn) & (A.rung == str(L))]
                vals.append(float(z.RESOLVED.mean()))
                arows.append(dict(L=L, panel=pn, window=wn, rate=vals[-1],
                                  f=float(z.f.iloc[0])))
            line += "      " + " ".join(f"{v:.3f}" for v in vals)
        P(line)
    AR = pd.DataFrame(arows)
    AR.to_csv(f"{OUT}.collapse_absL.csv", index=False)
    P("")
    P("       SPREAD AT MATCHED ABSOLUTE L (max - min over windows), per panel:")
    P("       L          " + "".join(f"{pn:>10s}" for pn in PANELS) + "     pooled-over-panels")
    sp_L_panel = {pn: [] for pn in PANELS}
    sp_L_all = []
    for L in common_abs:
        line = f"       {str(L):<9s} "
        for pn in PANELS:
            v = AR[(AR.L == L) & (AR.panel == pn)].rate
            s = float(v.max() - v.min())
            sp_L_panel[pn].append(s)
            line += f"{s:10.4f}"
        v2 = AR[AR.L == L].rate
        sp_L_all.append(float(v2.max() - v2.min()))
        P(line + f"{sp_L_all[-1]:20.4f}")
    max_sp_L_within = max(max(v) for v in sp_L_panel.values())
    mean_sp_f_within = float(np.mean([s for v in sp_f_panel.values() for s in v]))
    mean_sp_L_within = float(np.mean([s for v in sp_L_panel.values() for s in v]))
    P("")
    P(f"       MAX matched-ABSOLUTE-L spread across windows within a panel: {max_sp_L_within:.4f}")
    P(f"       MEAN matched-f spread {mean_sp_f_within:.4f}  vs  MEAN matched-absolute-L spread "
      f"{mean_sp_L_within:.4f}")
    gate("G6", "matched-f spread is TIGHTER than matched-absolute-L spread (mean, within panel)",
         mean_sp_L_within - mean_sp_f_within, mean_sp_f_within < mean_sp_L_within)
    ident = LDF[(LDF.keying == "FRAC") & (LDF.rung == "f1")]
    gate("G7", "the identity rung f = 1 resolves EVERY decision in all 12 cells (rate)",
         float(ident.RESOLVED.mean()), float(ident.RESOLVED.mean()) == 1.0)
    # monotonicity of rate in f, per cell
    mono = []
    for pn in PANELS:
        for wn in WINDOWS:
            z = CR[(CR.panel == pn) & (CR.window == wn)].sort_values("f")
            mono.append(spearman(z.rate.values, np.arange(len(z))))
    gate("G8", "resolution is monotone in f in every cell (min Spearman over 12 cells)",
         float(np.nanmin(mono)), float(np.nanmin(mono)) >= 0.90)

    # ------------------------------------------------------------ ARM D: the contribution curve
    P("")
    P("=" * 110)
    P("ARM D — 1243's PER-RUNG CONTRIBUTION, RE-READ IN f")
    P("=" * 110)
    P("")
    P("  c(rung) = decisions whose RESOLVED verdict DIFFERS from the reference point's, of 24 per")
    P("  cell.  Two references are published: the record's ABSOLUTE L = 63, and the")
    P("  FRACTION-matched point f63 = 63 / (WFULL length), i.e. the rung the record would have")
    P("  used had it keyed on f instead of L.")
    piv = {}
    for (wn, pn) in [(w, p) for w in WINDOWS for p in PANELS]:
        z = LDF[(LDF.window == wn) & (LDF.panel == pn)]
        piv[(wn, pn)] = z.pivot_table(index=["anchor", "ladder", "chooser"], columns="rung",
                                      values="RESOLVED", aggfunc="first")
    f63 = {pn: 63.0 / pans[pn].T_is for pn in PANELS}
    P(f"  f63 (63 / full IS length) = " + ", ".join(f"{pn} {f63[pn]:.4f}" for pn in PANELS))
    drows = []
    for pn in PANELS:
        # the nearest FRAC rung to f63, fixed per panel, used as the fraction-matched reference
        fref = min(FRACS, key=lambda f: abs(np.log(f) - np.log(f63[pn])))
        for wn in WINDOWS:
            pv = piv[(wn, pn)]
            for ref_kind, refcol in (("ABS63", "63"), (f"FRACf{fref:g}", f"f{fref:g}")):
                if refcol not in pv.columns:
                    continue
                for rung in pv.columns:
                    if rung == refcol:
                        continue
                    n = int((pv[rung] != pv[refcol]).sum())
                    zz = LDF[(LDF.window == wn) & (LDF.panel == pn) & (LDF.rung == rung)]
                    drows.append(dict(panel=pn, window=wn, ref=ref_kind, rung=rung,
                                      keying=zz.keying.iloc[0], L=int(zz.L.iloc[0]),
                                      f=float(zz.f.iloc[0]), c=n, share=n / len(pv)))
    DC = pd.DataFrame(drows)
    DC.to_csv(f"{OUT}.contribution.csv", index=False)
    P("")
    P("  (D1) 1243's TABLE, REPLAYED (WFULL, ABS keying, reference ABS L = 63, pooled 72):")
    P("       rung      c (of 72)   1243's c   dev")
    cdev = []
    for L in RUNGS_ABS:
        if str(L) == "63":
            continue
        z = DC[(DC.window == "WFULL") & (DC.ref == "ABS63") & (DC.rung == str(L))]
        n = int(z.c.sum())
        d = abs(n - A1243_CONTRIB[L])
        cdev.append(d)
        P(f"       {str(L):8s}  {n:9d}   {A1243_CONTRIB[L]:8d}   {n - A1243_CONTRIB[L]:+4d}")
    gate("G9", "1243's per-rung contribution table replays in the WFULL cell (max |dev| of 72)",
         float(max(cdev)), max(cdev) <= 5)
    P("")
    P("  (D2) THE SAME CONTRIBUTION, KEYED ON f, FRACTION-MATCHED REFERENCE, ALL 12 CELLS")
    P("       (share of the cell's 24 decisions):")
    P("       f          " + "   ".join(f"{pn}: " + " ".join(f"{w[1:]:>5s}" for w in WINDOWS)
                                        for pn in PANELS))
    sp_c = []
    for f in FRACS:
        lab = f"f{f:g}"
        line = f"       {f:<9g} "
        for pn in PANELS:
            vals = []
            for wn in WINDOWS:
                z = DC[(DC.panel == pn) & (DC.window == wn) & (DC.rung == lab) &
                       (DC.ref.str.startswith("FRAC"))]
                vals.append(float(z.share.iloc[0]) if len(z) else np.nan)
            if np.all(np.isfinite(vals)):
                sp_c.append((f, pn, float(np.nanmax(vals) - np.nanmin(vals))))
            line += "      " + " ".join(("  nan" if not np.isfinite(v) else f"{v:.3f}")
                                        for v in vals)
        P(line)
    max_sp_c = max(s for _, _, s in sp_c) if sp_c else np.nan
    P("")
    P(f"       MAX contribution spread across windows at matched f, within a panel: "
      f"{max_sp_c:.4f}")

    # ------------------------------------------------------------ ARM E: rule 8 + KEEP paths
    P("")
    P("=" * 110)
    P("ARM E — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    P("=" * 110)
    P("")
    P("  (E1) every rung book, full sample and 2017-2026, 4a vs live RULES v2 and 4b vs SPY.")
    BM = {}
    for pn in PANELS:
        pan = pans[pn]
        BM[(pn, "SPY")] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lbv = backtest(px[pn], rules_v2_weights(px[pn]), cost_bps=COST,
                       freq="W")["returns"].values
        BM[(pn, "LIVE")] = blocks_m(lbv, pan.warm, pan.ins, pan.oos)
    brows = []
    for (pn, an, lad) in sorted({(a_, b_, c_) for (a_, b_, c_, _) in DEC}):
        pan = pans[pn]
        for rung, r in BOOKS[(pn, an, lad)].items():
            m = blocks_m(np.asarray(r), pan.warm, pan.ins, pan.oos)
            brows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung), **m,
                              KEEP_4a=all(legs_4a(m, BM[(pn, "LIVE")]).values()),
                              KEEP_4b=all(legs_4b(m, BM[(pn, "SPY")]).values()),
                              KEEP_4b_OOS=all(legs_4b_oos(m, BM[(pn, "SPY")]).values())))
    BK = pd.DataFrame(brows).drop_duplicates(subset=["panel", "anchor", "ladder", "rung"])
    BK.to_csv(f"{OUT}.books.csv", index=False)
    P(f"       {len(BK)} rung-book rows.  4a {int(BK.KEEP_4a.sum())}; 4b full "
      f"{int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; BOTH "
      f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")
    for pn in PANELS:
        s, l = BM[(pn, "SPY")], BM[(pn, "LIVE")]
        P(f"       {pn:6s} SPY  full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:8.2%}"
          f"   OOS {s['OOS_CAGR']:7.2%} / {s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:8.2%}")
        P(f"       {pn:6s} LIVE full {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:8.2%}"
          f"   OOS {l['OOS_CAGR']:7.2%} / {l['OOS_Sharpe']:.4f} / {l['OOS_MaxDD']:8.2%}")
    both = BK[BK.KEEP_4b & BK.KEEP_4b_OOS].sort_values("OOS_Sharpe", ascending=False)
    if len(both):
        b0 = both.iloc[0]
        P(f"       best 4b-BOTH book: {b0.panel} anchor {b0.anchor} ladder {b0.ladder} rung "
          f"{b0.rung}  full {b0.CAGR:7.2%} / {b0.Sharpe:.4f} / {b0.MaxDD:8.2%}   "
          f"OOS {b0.OOS_CAGR:7.2%} / {b0.OOS_Sharpe:.4f} / {b0.OOS_MaxDD:8.2%}")

    P("")
    P("  (E2) THE DIAL ON TRIAL.  Every pick is its decision's IS argmax computed on ITS OWN")
    P("       window ONLY; 2017-2026 is read once.  Three filters are compared at each window")
    P("       length: act on ALL 24 picks per panel; act only where the decision is RESOLVED at")
    P("       the record's ABSOLUTE L = 63; act only where it is RESOLVED at the FRACTION-matched")
    P("       rung.  If the fraction law has CAPITAL content, the f-keyed filter must beat the")
    P("       absolute-L one out of sample.")
    pickm = {}
    for wn in WINDOWS:
        for (pn, an, lad, ch) in DEC:
            pan = pans[pn]
            m = pan.win[wn]
            rungs = LADDERS[lad]
            vals = [is_stat_win(BOOKS[(pn, an, lad)][r], m, ch) for r in rungs]
            obs = rungs[int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))]
            mm = blocks_m(np.asarray(BOOKS[(pn, an, lad)][obs]), pan.warm, pan.ins, pan.oos)
            pickm[(wn, pn, an, lad, ch)] = (obs, mm)

    def resolved_at(wn, key, rung_label):
        z = LDF[(LDF.window == wn) & (LDF.panel == key[0]) & (LDF.anchor == key[1]) &
                (LDF.ladder == key[2]) & (LDF.chooser == key[3]) & (LDF.rung == rung_label)]
        return bool(z.RESOLVED.iloc[0]) if len(z) else False

    wrows = []
    for wn in WINDOWS:
        for pn in PANELS:
            fref = min(FRACS, key=lambda f: abs(np.log(f) - np.log(f63[pn])))
            keys = [d for d in DEC if d[0] == pn]
            for filt in ["ALL", "RES_ABS63", f"RES_FRACf{fref:g}"]:
                if filt == "ALL":
                    sel = keys
                elif filt == "RES_ABS63":
                    sel = [k for k in keys if resolved_at(wn, k, "63")]
                else:
                    sel = [k for k in keys if resolved_at(wn, k, f"f{fref:g}")]
                ms = [pickm[(wn,) + k][1] for k in sel]
                wrows.append(dict(
                    window=wn, panel=pn, filt=filt, n=len(ms),
                    OOS_Sharpe=float(np.mean([m["OOS_Sharpe"] for m in ms])) if ms else np.nan,
                    OOS_CAGR=float(np.mean([m["OOS_CAGR"] for m in ms])) if ms else np.nan,
                    OOS_MaxDD=float(np.mean([m["OOS_MaxDD"] for m in ms])) if ms else np.nan,
                    KEEP_4a=int(sum(all(legs_4a(m, BM[(pn, "LIVE")]).values()) for m in ms)),
                    KEEP_4b=int(sum(all(legs_4b(m, BM[(pn, "SPY")]).values()) for m in ms)),
                    KEEP_4b_OOS=int(sum(all(legs_4b_oos(m, BM[(pn, "SPY")]).values())
                                        for m in ms))))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    P("       window  panel   filter            picks   mean OOS Sharpe   mean OOS CAGR   "
      "mean OOS MaxDD   4a / 4b / 4b_OOS")
    for _, r in W8.iterrows():
        P(f"       {r.window:7s} {r.panel:6s}  {r.filt:16s}  {r.n:5d}   "
          f"{r.OOS_Sharpe:15.4f}   {r.OOS_CAGR:13.2%}   {r.OOS_MaxDD:14.2%}   "
          f"{int(r.KEEP_4a)} / {int(r.KEEP_4b)} / {int(r.KEEP_4b_OOS)}")
    P("")
    P("       POOLED OVER PANELS (equal weight on the 72 decisions):")
    P("       window  filter kind         picks   mean OOS Sharpe   vs SPY OOS (mean of panels)")
    spy_oos = float(np.mean([BM[(pn, "SPY")]["OOS_Sharpe"] for pn in PANELS]))
    pooled = []
    for wn in WINDOWS:
        for kind in ["ALL", "ABS63", "FRAC"]:
            z = W8[(W8.window == wn) & (W8.filt.str.startswith(
                {"ALL": "ALL", "ABS63": "RES_ABS63", "FRAC": "RES_FRAC"}[kind]))]
            n = int(z.n.sum())
            if n == 0:
                P(f"       {wn:7s} {kind:18s}  {n:5d}   {'nan':>15s}")
                pooled.append(dict(window=wn, kind=kind, n=0, OOS_Sharpe=np.nan))
                continue
            s = float((z.OOS_Sharpe * z.n).sum() / n)
            pooled.append(dict(window=wn, kind=kind, n=n, OOS_Sharpe=s))
            P(f"       {wn:7s} {kind:18s}  {n:5d}   {s:15.4f}   {s - spy_oos:+.4f}")
    PL = pd.DataFrame(pooled)
    PL.to_csv(f"{OUT}.pooled.csv", index=False)
    d_fa = [float(PL[(PL.window == w) & (PL.kind == "FRAC")].OOS_Sharpe.iloc[0] -
                  PL[(PL.window == w) & (PL.kind == "ABS63")].OOS_Sharpe.iloc[0])
            for w in WINDOWS]
    P("")
    P("       f-KEYED FILTER MINUS ABSOLUTE-L FILTER, mean OOS Sharpe, by window: " +
      "  ".join(f"{w} {d:+.4f}" for w, d in zip(WINDOWS, d_fa)))
    best_gain = float(np.nanmax(d_fa))

    # ------------------------------------------------------------ verdict
    P("")
    P("=" * 110)
    P("VERDICT")
    P("=" * 110)
    if max_sp_f_within > SPREAD_BAR:
        outcome = "(N) NO SINGLE LAW"
    elif max_sp_panel > SPREAD_BAR:
        outcome = "(P) FRACTION PLUS PANEL"
    else:
        outcome = "(F) FRACTION LAW"
    P("")
    P(f"    PRE-DECLARED OUTCOME FIRES: {outcome}")
    P(f"      matched-f spread across windows, worst within a panel : {max_sp_f_within:.4f}")
    P(f"      matched-f spread across all 12 cells                  : {max_sp_f_all:.4f}")
    P(f"      cross-PANEL spread at matched f and window            : {max_sp_panel:.4f}")
    P(f"      matched-ABSOLUTE-L spread, worst within a panel       : {max_sp_L_within:.4f}")
    P(f"      MEAN spreads: f {mean_sp_f_within:.4f} vs absolute L {mean_sp_L_within:.4f}")
    P(f"      seed noise on the same object                         : {seed_noise:.4f}")
    P(f"      pre-declared bar, not moved                           : {SPREAD_BAR:.4f}")
    P("")
    P(f"    CAPITAL.  The f-keyed resolution filter moves mean OOS Sharpe by "
      f"{best_gain:+.4f} at best")
    P("      against the record's absolute-L filter.  4a "
      f"{int(BK.KEEP_4a.sum())} of {len(BK)} rung books; 4b BOTH "
      f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())} books.")
    P("")
    P("    SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the")
    P("    current constituents of a sub-$2B screen with max_1d_move >= 1.0 names dropped.")
    P("    Every LEVEL is optimistic and a resample null cannot correct it.  The headline is a")
    P("    RATIO of one construction against itself (the same decisions at different window")
    P("    lengths and block fractions) so it largely cancels; the 4b legs do NOT cancel and")
    P("    those passes are upper bounds.")

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    P("")
    P(f"    GATES: {int(GD.pass_.sum())} of {len(GD)} pass.")
    P("")
    P(f"    runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()

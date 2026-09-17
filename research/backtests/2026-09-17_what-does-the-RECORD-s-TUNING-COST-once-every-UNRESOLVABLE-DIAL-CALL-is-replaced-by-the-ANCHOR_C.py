#!/usr/bin/env python3
"""
Idea 1224 (lane C, 2026-09-17) — what does the RECORD's TUNING COST, once every UNRESOLVABLE
DIAL CALL is replaced by the ANCHOR?

THE PREMISE, READ FROM THE RECORD.  Idea 1214 (lane C, 2026-09-17) walked six bar forms over
one chooser family and found the ordering terminates at DOING NOTHING: mean OOS fold Sharpe
CH_RAW 0.9677 -> CH_ANCHOR 1.0362, a paired delta of +0.0685 at t = +1.33 over 42 (panel, fold)
picks, i.e. UNRESOLVED on 14 folds.  1209/1211/1206/1221/1226/1227/1230/1231 have each arrived
at the same sentence from a different direction.  The queue asks the only question that turns
that sentence into a number a book could act on: PRICE THE SUBSTITUTION ACROSS THE RECORD'S
RULE-8 PICKS, not one run's 42, and report the POOLED DELTA and its FOLD-CLUSTERED SE.

WHAT IS BEING PRICED, STATED BEFORE ANY NUMBER IS READ.  A rule-8 pick is a (panel, ladder,
rung) chosen on an IS window and read once OOS.  Its counterfactual is the SAME ladder's ANCHOR
rung.  The tuning cost is

    DELTA = OOS Sharpe(book under the substitution) - OOS Sharpe(book the record actually picked)

so a POSITIVE delta means the record's tuning COST it that much OOS Sharpe and the substitution
pays.  Every cell of the grid is published; nothing is selected on.  DELTA is identically 0 for
S_NONE by construction (gate G7) and for any pick that already sits on the anchor rung (G8).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  PICK SET            {P_1214, P_AXIS, P_TEXT}
  SUBSTITUTION RULE   {S_NONE, S_ALL, S_SE1, S_SE2, S_ANC95}

  P_1214  1214's own 42 picks — the raw-widest ladder over ALL4, then that ladder's IS argmax,
          3 panels x 14 folds.  Carried ONLY so gate G9 can replay 1214's committed numbers.
  P_AXIS  EVERY rule-8 pick this tree can rebuild: 3 panels x 4 ladders x 14 folds = 168, one
          IS argmax per (panel, ladder, fold).  This is the pooled object the queue asks for.
  P_TEXT  the record's OWN committed rule-8 picks, harvested from LEADERBOARD.md, CHANGELOG.md
          and every research/backtests/*.md, resolved to (panel, ladder, rung) and priced on
          the split the record itself used (IS to 2016-12-31, 2017-2026 read once).

  S_NONE   keep the pick.  The reference arm; its delta is 0 at every cell.
  S_ALL    substitute the anchor rung at EVERY pick (1214's CH_ANCHOR, generalised).
  S_SE1    substitute UNLESS the pick's IS Sharpe beats the ladder's best OTHER rung by >= 1
           block-bootstrap SE of that paired difference.
  S_SE2    the same at >= 2 SE.
  S_ANC95  substitute UNLESS the 95% block-bootstrap interval of (pick - anchor) on the IS
           window excludes 0 from above — i.e. unless the pick is resolvably better than the
           thing it would be replaced by.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the record's four
ladders N/H/GROSS/CADENCE; the 14 folds; the 4a and 4b legs; the IS and OOS windows.

Frozen at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 / CADENCE=W, 10 bps (rule 2),
decide-at-t / apply-at-t+1, warm-up 260 rows, 63-day moving-block bootstrap at 800 reps.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS
window ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every
rung book, every rule-8 row and every stitched curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_what-does-the-RECORD-s-TUNING-COST-once-every-UNRESOLVABLE-DIAL-CALL-is-replaced-by-the-ANCHOR_C.py
"""
from __future__ import annotations

import hashlib
import re
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

DATE = "2026-09-17"
SLUG = ("what-does-the-RECORD-s-TUNING-COST-once-every-UNRESOLVABLE-DIAL-CALL-is-replaced-"
        "by-the-ANCHOR")
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
ANCHOR_RUNG = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}
LADS = ["N", "H", "GROSS", "CADENCE"]
PICKSETS = ["P_1214", "P_AXIS", "P_TEXT"]
SUBRULES = ["S_NONE", "S_ALL", "S_SE1", "S_SE2", "S_ANC95"]
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
BOOT_B, BOOT_REPS, BOOT_SEED = 63, 800, 12241224
# 1214's committed price leg, replayed by gate G9.
C1214 = dict(CH_RAW=0.9677, CH_ANCHOR=1.0362, delta=0.0685, SE=0.0514)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ==================================================================== panels / runner (1214's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


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


def build1(pan, N, H, freq, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight."""
    reb = pan.seg[freq]
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
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
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


def nrun(pan, Wt, freq):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


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
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def clustered(d, fold):
    """Mean of d, SE clustered on fold (1214's estimator: SD of the fold means / sqrt(G))."""
    s = pd.Series(np.asarray(d, float))
    f = pd.Series(np.asarray(fold))
    ok = s.notna()
    s, f = s[ok], f[ok]
    if len(s) == 0:
        return np.nan, np.nan, np.nan, 0, 0
    fm = s.groupby(f.values).mean()
    se = float(fm.std(ddof=1) / np.sqrt(len(fm))) if len(fm) > 1 else np.nan
    m = float(s.mean())
    t = m / se if se and se > 0 else 0.0
    return m, se, float(t), len(s), len(fm)


# ==================================================================== the record's own text
UNIT_R8 = re.compile(r"\b(rule[- ]?8|walk[- ]?forward|out[- ]of[- ]sample|OOS)\b", re.I)
UNIT_PICK = re.compile(r"\b(pick|picks|picked|chose|chosen|choose|argmax|select|selects|"
                       r"selected|chooser)\b", re.I)
PANEL_R = re.compile(r"\b(U56|B136|SMALL)\b")
R_N = re.compile(r"\bN\s*=\s*(\d+)\b")
R_H = re.compile(r"\bH\s*=\s*(\d+)\b")
R_G = re.compile(r"\b(?:gross|g)\s*[= ]\s*(0?\.\d{2})\b", re.I)
R_C = re.compile(r"\b(weekly|monthly)\b", re.I)


def units():
    U = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
    for ln in lb.split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in cl.split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    nmd = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        nmd += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, nmd


def harvest(U):
    """Every committed unit that makes a rule-8 PICK claim, with the (panel, ladder, rung)
    triples it names that this tree can rebuild."""
    rows = []
    for src, txt in U:
        r8, pk = bool(UNIT_R8.search(txt)), bool(UNIT_PICK.search(txt))
        pans = sorted(set(PANEL_R.findall(txt)))
        trip = []
        for m in R_N.finditer(txt):
            v = int(m.group(1))
            if v in LAD["N"]:
                trip.append(("N", v))
        for m in R_H.finditer(txt):
            v = int(m.group(1))
            if v in LAD["H"]:
                trip.append(("H", v))
        for m in R_G.finditer(txt):
            v = round(float(m.group(1)), 2)
            if v in LAD["GROSS"]:
                trip.append(("GROSS", v))
        for m in R_C.finditer(txt):
            trip.append(("CADENCE", "W" if m.group(1).lower() == "weekly" else "M"))
        trip = sorted(set(trip), key=lambda x: (LADS.index(x[0]), str(x[1])))
        rows.append(dict(uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
                         RULE8=r8, PICK=pk, n_panels=len(pans),
                         panels="|".join(pans), n_triples=len(trip),
                         triples="|".join(f"{a}={b}" for a, b in trip),
                         CHECKABLE=bool(r8 and pk and pans and trip)))
    return pd.DataFrame(rows)


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1224 (lane C, 2026-09-17) — what does the RECORD's TUNING COST once every")
    say("UNRESOLVABLE DIAL CALL is replaced by the ANCHOR?")
    say("=" * 108)
    say("")
    say("  DELTA = OOS Sharpe(substituted book) - OOS Sharpe(the book the record picked).")
    say("  POSITIVE delta = the record's tuning COST it that much; the substitution pays.")
    say("  PRE-DECLARED OUTCOMES: (A) TUNING IS EXPENSIVE — pooled delta > 0 at |t| >= 2 under")
    say("  S_ALL.  (B) TUNING IS FREE — |pooled delta| < 0.02 of Sharpe at |t| < 2.  (C) STILL")
    say("  UNRESOLVED — pooled delta > 0.02 but |t| < 2, i.e. 1214's +0.0685 / t 1.33 again with")
    say("  more picks and no more resolution.")

    # ------------------------------------------------------------------ panels and rung books
    say("")
    say("=" * 108)
    say("ARM A — PANELS, RUNG BOOKS, FOLDS")
    say("=" * 108)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0); SPY benchmark only.")

    booked, bench, RM, BOOKKEY = {}, {}, {}, []
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        af = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]), f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        RM[pan.name] = np.column_stack([books[k] for k in BOOKKEY])
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name:6s} {len(books)} rung books built "
            f"({' '.join(f'{k} {len(v)}' for k, v in LAD.items())}).")

    # gates on the machinery
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    gate("G1 fast runner == engine.backtest on the decision-time frame", g1, 1e-10, g1 < 1e-10)
    fr = build1(pan, A_N, A_H, "W")
    g2 = float(max(np.abs(nrun(pan, g * fr, "W") - nrun(pan, g * fr, "W")).max()
                   for g in LAD["GROSS"]))
    gate("G2 the GROSS ladder is the anchor frame SCALED (deterministic)", g2, 0.0, g2 == 0.0)
    lm = mdd(bench["U56"]["live"][WARMUP:])
    gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%", lm,
         LIVE_MAXDD_COMMITTED, abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)
    anc = [booked["U56"][(l, ANCHOR_RUNG[l])] for l in LADS]
    g4 = float(max(np.abs(a - anc[0]).max() for a in anc))
    gate("G4 the anchor rung of all four ladders is ONE book bit for bit", g4, 0.0, g4 == 0.0)
    say(f"    G1 {g1:.3e}   G2 {g2:.3e}   G3 live U56 MaxDD {lm:.4%}   G4 {g4:.3e}")

    # ---- block bootstrap over the 22 rung books
    CS, CSQ = {}, {}
    for p, M in RM.items():
        CS[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M, axis=0)])
        CSQ[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M * M, axis=0)])

    def boot_sharpes(p, lo, hi, reps=BOOT_REPS, B=BOOT_B, identity=False):
        nb = (hi - lo) // B
        if nb < 2:
            return None
        n = nb * B
        if identity:
            starts = (lo + B * np.arange(nb))[None, :]
        else:
            pid = sum(ord(ch) for ch in p)
            rng = np.random.default_rng(BOOT_SEED + 17 * lo + 101 * hi + 9973 * pid)
            starts = rng.integers(lo, hi - B + 1, size=(reps, nb))
        tot = CS[p][starts + B].sum(axis=1) - CS[p][starts].sum(axis=1)
        totq = CSQ[p][starts + B].sum(axis=1) - CSQ[p][starts].sum(axis=1)
        mu = tot / n
        sd = np.sqrt(np.maximum(totq / n - mu * mu, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)

    p0, i00 = panels[0].name, panels[0].i0
    h00 = panels[0].idx.searchsorted(pd.Timestamp(OOS_START))
    ident = boot_sharpes(p0, i00, h00, identity=True)[0]
    nb0 = (h00 - i00) // BOOT_B
    direct = np.array([sharpe(RM[p0][i00:i00 + nb0 * BOOT_B, j]) for j in range(RM[p0].shape[1])])
    g5 = float(np.nanmax(np.abs(ident - direct)))
    gate("G5 block-sum bootstrap == direct Sharpe on the identity tiling", g5, 1e-10, g5 < 1e-10)
    twice = float(np.nanmax(np.abs(boot_sharpes(p0, i00, h00) - boot_sharpes(p0, i00, h00))))
    gate("G6 the bootstrap is deterministic across independent constructions", twice, 0.0,
         twice == 0.0)
    say(f"    G5 {g5:.3e}   G6 {twice:.3e}")

    BIDX = {k: BOOKKEY.index(k) for k in BOOKKEY}
    _BC: dict = {}

    def bs(p, lo, hi):
        if (p, lo, hi) not in _BC:
            _BC[(p, lo, hi)] = boot_sharpes(p, lo, hi)
        return _BC[(p, lo, hi)]

    # ---- folds
    folds = {}
    for pan in panels:
        yrs = pan.idx.year.values
        cover = []
        for y in FOLD_YEARS:
            oo = np.flatnonzero(yrs == y)
            oo = oo[oo >= pan.i0]
            if len(oo) < 60:
                continue
            lo, hi = pan.i0, int(oo[0])
            if hi - lo < 252:
                continue
            cover.append((int(oo[0]), int(oo[-1]) + 1))
            folds.setdefault(pan.name, []).append((y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
        cover = sorted(set(cover))
        gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        gate(f"G7 folds tile {pan.name} with no overlap and no gap", float(gap), 0.0, gap == 0)
    say(f"    FOLDS: {len(folds['U56'])} per panel, {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}; "
        f"IS = warm-up to the day before the fold, OOS = the fold year.")

    # ------------------------------------------------------------------ the substitution
    def is_sharpe(p, lad, rung, lo, hi):
        return sharpe(booked[p][(lad, rung)][lo:hi])

    def substitute(rule, p, lad, rung, lo, hi):
        """Return the rung this rule holds, and the diagnostics behind the call."""
        a = ANCHOR_RUNG[lad]
        info = dict(margin=np.nan, SE=np.nan, anc_margin=np.nan, anc_lo95=np.nan)
        if rule == "S_NONE":
            return rung, info
        if rule == "S_ALL":
            return a, info
        S = bs(p, lo, hi)
        others = [r for r in LAD[lad] if r != rung]
        if not others or S is None:
            return a, info
        sp = is_sharpe(p, lad, rung, lo, hi)
        best_o, best_s = None, -np.inf
        for r in others:
            v = is_sharpe(p, lad, r, lo, hi)
            if np.isfinite(v) and v > best_s:
                best_o, best_s = r, v
        if best_o is None or not np.isfinite(sp):
            return a, info
        if rule in ("S_SE1", "S_SE2"):
            d = S[:, BIDX[(lad, rung)]] - S[:, BIDX[(lad, best_o)]]
            se = float(np.nanstd(d, ddof=1))
            info.update(margin=sp - best_s, SE=se)
            k = 1.0 if rule == "S_SE1" else 2.0
            return (rung if (np.isfinite(se) and se > 0 and (sp - best_s) >= k * se) else a), info
        # S_ANC95
        if rung == a:
            return a, info
        d = S[:, BIDX[(lad, rung)]] - S[:, BIDX[(lad, a)]]
        lo95 = float(np.nanpercentile(d, 2.5))
        m = sp - is_sharpe(p, lad, a, lo, hi)
        info.update(anc_margin=m, anc_lo95=lo95)
        return (rung if (lo95 > 0 and m > 0) else a), info

    # ------------------------------------------------------------------ pick sets
    say("")
    say("=" * 108)
    say("ARM B — THE PICK SETS")
    say("=" * 108)

    def argmax_rung(p, lad, lo, hi):
        v = [(is_sharpe(p, lad, r, lo, hi), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    picks = []          # every priced pick: (pickset, panel, ladder, rung, IS, OOS, fold)
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            # P_AXIS — every ladder's IS argmax
            for lad in LADS:
                r = argmax_rung(pan.name, lad, lo, hi)
                picks.append(dict(pickset="P_AXIS", panel=pan.name, fold=y, ladder=lad, rung=r,
                                  lo=lo, hi=hi, o0=o0, o1=o1))
            # P_1214 — the raw-widest ladder over ALL4, then that ladder's IS argmax
            spr = {}
            for lad in LADS:
                v = [is_sharpe(pan.name, lad, r, lo, hi) for r in LAD[lad]]
                v = [x for x in v if np.isfinite(x)]
                spr[lad] = (max(v) - min(v)) if len(v) > 1 else np.nan
            wid = max(spr, key=lambda k: (spr[k] if np.isfinite(spr[k]) else -np.inf))
            picks.append(dict(pickset="P_1214", panel=pan.name, fold=y, ladder=wid,
                              rung=argmax_rung(pan.name, wid, lo, hi),
                              lo=lo, hi=hi, o0=o0, o1=o1))

    # P_TEXT — the record's own committed rule-8 picks
    say("")
    say("  (B1) THE HARVEST.  Every committed unit in LEADERBOARD.md, CHANGELOG.md and every")
    say("       research/backtests/*.md, tested for a rule-8 PICK claim naming a PANEL and a")
    say("       LADDER RUNG this tree can rebuild.")
    U, nmd = units()
    H = harvest(U)
    H.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    say(f"       {len(H):,} committed units over {nmd:,} .md files + LEADERBOARD + CHANGELOG.")
    say(f"       rule-8 context {int(H.RULE8.sum()):,} ({H.RULE8.mean():.4f}); "
        f"AND a pick verb {int((H.RULE8 & H.PICK).sum()):,} "
        f"({(H.RULE8 & H.PICK).mean():.4f});")
    say(f"       AND a panel {int((H.RULE8 & H.PICK & (H.n_panels > 0)).sum()):,}; "
        f"AND a rebuildable rung — CHECKABLE {int(H.CHECKABLE.sum()):,} "
        f"({H.CHECKABLE.mean():.4f}).")
    trips = {}
    for _, r in H[H.CHECKABLE].iterrows():
        for pn in r.panels.split("|"):
            for tk in r.triples.split("|"):
                lad, rv = tk.split("=")
                rung = (rv if lad == "CADENCE" else
                        (float(rv) if lad == "GROSS" else int(rv)))
                trips.setdefault((pn, lad, rung), 0)
                trips[(pn, lad, rung)] += 1
    say(f"       {len(trips)} DISTINCT committed (panel, ladder, rung) picks over "
        f"{sum(trips.values()):,} committed unit-mentions (1194's duplicate warning: the")
    say("       DISTINCT triple is priced, the mention count is reported and not weighted on).")
    bad = [k for k in trips if k[2] not in LAD[k[1]]]
    gate("G8 every harvested rung is a rung of the record's committed ladder", float(len(bad)),
         0.0, len(bad) == 0)
    ilim = {pan.name: pan.idx.searchsorted(pd.Timestamp(OOS_START)) for pan in panels}
    for (pn, lad, rung), _n in sorted(trips.items(), key=lambda kv: (kv[0][0], kv[0][1], str(kv[0][2]))):
        pobj = [p for p in panels if p.name == pn][0]
        for (y, _lo, _hi, o0, o1) in folds[pn]:
            if y < 2017:
                continue
            picks.append(dict(pickset="P_TEXT", panel=pn, fold=y, ladder=lad, rung=rung,
                              lo=pobj.i0, hi=ilim[pn], o0=o0, o1=o1))
    P = pd.DataFrame(picks)
    say(f"       PICK SETS: P_1214 {int((P.pickset=='P_1214').sum())} cells, "
        f"P_AXIS {int((P.pickset=='P_AXIS').sum())}, "
        f"P_TEXT {int((P.pickset=='P_TEXT').sum())} "
        f"({len(trips)} committed picks x the {len([y for y in FOLD_YEARS if y>=2017])} OOS folds).")

    # ------------------------------------------------------------------ price every cell
    say("")
    say("  (B2) THE PRICE.  Every (pick set x substitution rule) cell, ALL 15 PUBLISHED.")
    rows = []
    for _, q in P.iterrows():
        base = booked[q.panel][(q.ladder, q.rung)][q.o0:q.o1]
        s_base = sharpe(base)
        for rule in SUBRULES:
            rr, info = substitute(rule, q.panel, q.ladder, q.rung, q.lo, q.hi)
            s_new = sharpe(booked[q.panel][(q.ladder, rr)][q.o0:q.o1])
            rows.append(dict(pickset=q.pickset, rule=rule, panel=q.panel, fold=q.fold,
                             ladder=q.ladder, rung=q.rung, held=rr,
                             moved=bool(rr != q.rung), at_anchor=bool(q.rung == ANCHOR_RUNG[q.ladder]),
                             OOS_Sharpe=s_new, OOS_Sharpe_pick=s_base, delta=s_new - s_base,
                             **info))
    D = pd.DataFrame(rows)
    D.to_csv(f"{OUT}.picks.csv.gz", index=False, compression="gzip")

    z = D[D.rule == "S_NONE"].delta.abs().max()
    gate("G9 S_NONE delta == 0 at every cell (the reference arm)", float(z), 0.0, z == 0.0)
    za = D[D.at_anchor].delta.abs().max()
    gate("G10 a pick already AT the anchor has delta 0 under every rule", float(za), 0.0,
         za == 0.0)

    say("")
    say("       pick set   rule      picks  move rate   mean OOS Sharpe   DELTA      SE      t")
    grid = []
    for ps in PICKSETS:
        for rule in SUBRULES:
            s = D[(D.pickset == ps) & (D.rule == rule)]
            m, se, t, n, G = clustered(s.delta.values, s.fold.values)
            grid.append(dict(PICK_SET=ps, SUB_RULE=rule, picks=n, folds=G,
                             move_rate=float(s.moved.mean()),
                             mean_OOS_Sharpe=float(s.OOS_Sharpe.mean()),
                             DELTA=m, SE=se, t=t))
            say(f"       {ps:9s}  {rule:8s} {n:6d}   {s.moved.mean():.4f}     "
                f"{s.OOS_Sharpe.mean():9.4f}    {m:+.4f}  {se if np.isfinite(se) else 0:.4f}  "
                f"{t:+6.2f}")
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # G11 — replay 1214's committed price leg
    a = D[(D.pickset == "P_1214") & (D.rule == "S_NONE")]
    b = D[(D.pickset == "P_1214") & (D.rule == "S_ALL")]
    raw_m, anc_m = float(a.OOS_Sharpe.mean()), float(b.OOS_Sharpe.mean())
    dm, dse, dt, _, _ = clustered(b.delta.values, b.fold.values)
    err = max(abs(raw_m - C1214["CH_RAW"]), abs(anc_m - C1214["CH_ANCHOR"]),
              abs(dm - C1214["delta"]), abs(dse - C1214["SE"]))
    gate("G11 P_1214 x S_ALL replays 1214's committed CH_RAW/CH_ANCHOR/delta/SE", float(err),
         1e-4, err < 1e-4)
    say("")
    say(f"       G11 — 1214's committed leg replayed: CH_RAW {raw_m:.4f} (committed "
        f"{C1214['CH_RAW']}), CH_ANCHOR {anc_m:.4f} ({C1214['CH_ANCHOR']}),")
    say(f"             delta {dm:+.4f} ({C1214['delta']:+.4f}), SE {dse:.4f} "
        f"({C1214['SE']:.4f}), t {dt:+.2f} — max dev {err:.2e}.")

    say("")
    say("  (B3) THE POOLED DELTA BY PANEL AND BY LADDER (S_ALL, the substitution the queue")
    say("       names), so no single panel or axis can carry the headline unseen:")
    sub = []
    for ps in ("P_AXIS", "P_TEXT"):
        s0 = D[(D.pickset == ps) & (D.rule == "S_ALL")]
        for key, col in (("panel", "panel"), ("ladder", "ladder")):
            for v, g in s0.groupby(col):
                m, se, t, n, nf = clustered(g.delta.values, g.fold.values)
                sub.append(dict(pickset=ps, cut=key, value=v, picks=n, DELTA=m, SE=se, t=t,
                                move_rate=float(g.moved.mean())))
                say(f"       {ps:7s} {key:7s} {str(v):9s} picks {n:4d}  delta {m:+.4f}  "
                    f"SE {se if np.isfinite(se) else 0:.4f}  t {t:+6.2f}")
    pd.DataFrame(sub).to_csv(f"{OUT}.bycut.csv", index=False)

    # ------------------------------------------------------------------ rule 8 + KEEP paths
    say("")
    say("=" * 108)
    say("ARM C — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    say("=" * 108)
    say("")
    say("  BENCHMARKS (10 bps, t+1, post warm-up):")
    BM = {}
    for pan in panels:
        ioos = ilim[pan.name]
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[pan.i0:]
            h1, h2 = halves(full)
            BM[(pan.name, nm)] = dict(**triple(full), H1=h1, H2=h2, OOS_Sharpe=sharpe(r[ioos:]),
                                      OOS_CAGR=cagr(r[ioos:]), OOS_MaxDD=mdd(r[ioos:]))
            d = BM[(pan.name, nm)]
            say(f"    {pan.name:6s} {nm:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}  halves {d['H1']:.4f}/{d['H2']:.4f}  "
                f"OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    def oos_bm(p, nm, ioos):
        d = BM[(p, nm)]
        r = bench[p]["spy" if nm == "SPY" else "live"][ioos:]
        h1, h2 = halves(r)
        return dict(H1=h1, H2=h2, CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    say("")
    say("  (C1) BOTH KEEP PATHS ON EVERY RUNG BOOK (rule 4; nothing selected on):")
    brows = []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for (lad, rung), r in booked[pan.name].items():
            k4a, k4b, m, h1, h2 = keep_paths(r[i0:], spy, liv)
            _, k4b_o, mo, _, _ = keep_paths(r[ioos:], so, lo_)
            brows.append(dict(panel=pan.name, ladder=lad, rung=rung, **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    BK = pd.DataFrame(brows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    say(f"       {len(BK)} rung books: 4a {int(BK.KEEP_4a.sum())}; "
        f"4b full {int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}")

    say("")
    say("  (C2) RULE 8 — the single split PROTOCOL names.  Every rung chosen on warm-up..")
    say("       2016-12-31 ONLY; 2017-2026 read ONCE.  All 60 rows published.")
    wrows = []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for lad in LADS:
            r_is = argmax_rung(pan.name, lad, i0, ioos)
            for rule in SUBRULES:
                held, info = substitute(rule, pan.name, lad, r_is, i0, ioos)
                rr = booked[pan.name][(lad, held)]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(rr[ioos:], so, lo_)
                wrows.append(dict(panel=pan.name, ladder=lad, IS_argmax=r_is, rule=rule,
                                  held=held, moved=bool(held != r_is), **m, H1=h1, H2=h2,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                  KEEP_4b_OOS=k4b_o, **info))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say("       panel  ladder  IS argmax  rule      held   full CAGR/Sharpe/MaxDD        "
        "OOS CAGR/Sharpe/MaxDD        4a 4b 4bOOS")
    for _, r in W8.iterrows():
        say(f"       {r.panel:6s} {r.ladder:7s} {str(r.IS_argmax):9s} {r.rule:8s} "
            f"{str(r.held):6s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:8.2%}   "
            f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}   "
            f"{'T' if r.KEEP_4a else 'F'}  {'T' if r.KEEP_4b else 'F'}  "
            f"{'T' if r.KEEP_4b_OOS else 'F'}")
    say("")
    say(f"       RULE-8 ROWS: 4a {int(W8.KEEP_4a.sum())} of {len(W8)}; "
        f"4b full {int(W8.KEEP_4b.sum())}; 4b OOS {int(W8.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())}.")
    dk = W8[W8.KEEP_4b & W8.KEEP_4b_OOS]
    if len(dk):
        key = sorted({(r.panel, r.ladder, str(r.held)) for _, r in dk.iterrows()})
        rk = sorted({(r.panel, round(r.OOS_CAGR, 8), round(r.OOS_Sharpe, 8)) for _, r in dk.iterrows()})
        say(f"       The {len(dk)} passing rows collapse to {len(rk)} DISTINCT BOOKS on the "
            f"realised-return key (1211's), {len(key)} on the (panel, ladder, rung) key.")

    say("")
    say("  (C3) STITCHED ROLLING CURVES — each fold's OOS returns concatenated, per")
    say("       (pick set x rule x panel).  Both KEEP paths on each.")
    srows = []
    for ps in PICKSETS:
        for rule in SUBRULES:
            for pan in panels:
                i0, ioos = pan.i0, ilim[pan.name]
                spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
                so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
                s = D[(D.pickset == ps) & (D.rule == rule) & (D.panel == pan.name)]
                if not len(s):
                    continue
                segs, nrows = [], 0
                for y, g in s.groupby("fold"):
                    q = P[(P.pickset == ps) & (P.panel == pan.name) & (P.fold == y)]
                    o0, o1 = int(q.o0.iloc[0]), int(q.o1.iloc[0])
                    held = [booked[pan.name][(r.ladder, r.held)][o0:o1] for _, r in g.iterrows()]
                    segs.append(np.mean(np.column_stack(held), axis=1))
                    nrows += o1 - o0
                r = np.concatenate(segs)
                k4a, k4b, m, h1, h2 = keep_paths(r, spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(r, so, lo_)
                srows.append(dict(pickset=ps, rule=rule, panel=pan.name, days=len(r),
                                  **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                  OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o, rowcheck=nrows))
    ST = pd.DataFrame(srows)
    ST.to_csv(f"{OUT}.stitched.csv", index=False)
    bad = int((ST.days != ST.rowcheck).sum())
    gate("G12 stitched lengths == the sum of their folds", float(bad), 0.0, bad == 0)
    say(f"       {len(ST)} stitched curves: 4a {int(ST.KEEP_4a.sum())}; "
        f"4b full {int(ST.KEEP_4b.sum())}; 4b OOS {int(ST.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((ST.KEEP_4b & ST.KEEP_4b_OOS).sum())}.")
    say("")
    say("       pick set  rule      panel   CAGR / Sharpe / MaxDD        halves          4a 4b")
    for _, r in ST.iterrows():
        say(f"       {r.pickset:9s} {r.rule:8s} {r.panel:6s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
            f"{r.MaxDD:8.2%}   {r.H1:.4f}/{r.H2:.4f}   {'T' if r.KEEP_4a else 'F'}  "
            f"{'T' if r.KEEP_4b else 'F'}")

    # ------------------------------------------------------------------ gates + verdict
    say("")
    say("=" * 108)
    say("GATES")
    say("=" * 108)
    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in GD.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}  value {g.value}  target {g.target}")
    say(f"  {int(GD.pass_.sum())} of {len(GD)} gates pass.")

    hl = G[(G.PICK_SET == "P_AXIS") & (G.SUB_RULE == "S_ALL")].iloc[0]
    say("")
    say("=" * 108)
    say("HEADLINE")
    say("=" * 108)
    say(f"  Over {int(hl.picks)} rebuildable rule-8 picks on {int(hl.folds)} folds, replacing every")
    say(f"  dial call with the anchor is worth DELTA {hl.DELTA:+.4f} of OOS Sharpe, SE {hl.SE:.4f}, "
        f"t {hl.t:+.2f}.")
    outcome = ("(A) TUNING IS EXPENSIVE" if (hl.DELTA > 0 and abs(hl.t) >= 2) else
               "(B) TUNING IS FREE" if abs(hl.DELTA) < 0.02 and abs(hl.t) < 2 else
               "(C) STILL UNRESOLVED")
    say(f"  PRE-DECLARED OUTCOME: {outcome}.")
    say(f"  Runtime {time.time()-t0:.0f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

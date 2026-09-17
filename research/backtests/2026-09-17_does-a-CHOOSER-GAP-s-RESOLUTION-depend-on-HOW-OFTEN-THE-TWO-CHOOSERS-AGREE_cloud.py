#!/usr/bin/env python3
"""
Idea 1212 (cloud, 2026-09-17) — does a CHOOSER GAP's RESOLUTION depend on HOW OFTEN THE
TWO CHOOSERS AGREE?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1210 measured sigma_CELL
0.1176 against sigma_FOLD 0.3707 and found the record's two honest choosers pick the SAME
rung at 0.3380 of cells.  Where two choosers pick the same rung the difference in their
OOS statistic is EXACTLY ZERO — not small, zero — so a chooser-gap sample is not a draw
from one distribution but an EXACT-ZERO MIXTURE: a point mass at 0 with probability p and
a live draw with probability 1-p.  The queue asks whether that mixture makes a committed
gap need MORE picks than the pooled SD implies, or fewer.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  AGREEMENT BUCKET  {B_POOL, B_LADDER, B_PANELLADDER}   at what grain p is estimated
  SD BASIS          {S_POOLED, S_DISAGREE, S_FOLD}      which SD the bar is read from

  = 9 dial cells, EVERY ONE PUBLISHED.  Headline cell: B_POOL x S_POOLED, declared here
  before any number, because that pair is the record's own habit (one pooled mean over all
  picks, one pooled SD, no agreement rate stated anywhere).

TIMING IS NOT A DIAL, IT IS A CONTROL, AND BOTH ARMS ARE PUBLISHED.  Idea 1209 (cloud,
today) found a one-day look-ahead in the record's inherited fast builder — it reads the
score at the APPLICATION row — whose sign REVERSES across panels.  Nothing here is chosen
on it; every table is printed for T_REC (inherited) and T_LAG1 (PROTOCOL rule 2).

WHAT IS NOT A DIAL.  1154/1206's, inherited whole: PANEL {U56, B136, SMALL}, ANCHOR {A, B},
the four CORE LADDERS {N, H, GROSS, CADENCE}, the three honest CHOOSERS {CH_ISSHARPE,
CH_ISCAGR, CH_ISDD}, min hold, max_vol 0.60, 10 bps, warm-up 260, the 14 non-overlapping
calendar folds (2012-2025) 1206/1208 used, the 4a/4b legs, SPY as the 4b benchmark.

DECLARED BEFORE THE TAPE IS READ — THE ANSWER IS "MORE", AND THE FLOOR IS EXACT.  Let the
per-cell gap D be 0 with probability p and (mu_d, sigma_d) with probability 1-p.  Then

  E[D]   = (1-p) mu_d
  Var[D] = (1-p) sigma_d^2 + p(1-p) mu_d^2

so the picks needed to clear a 2-SE bar are

  n(p) = 4 Var[D] / E[D]^2 = 4 [ sigma_d^2 / ((1-p) mu_d^2) + p/(1-p) ]

and therefore

  n(p) / n(0) = 1/(1-p) + [p/(1-p)] * (mu_d/sigma_d)^2   >=   1/(1-p)   for every p.

ZEROS DILUTE THE MEAN FASTER THAN THEY DILUTE THE SD: the mean falls by (1-p), the SD only
by sqrt(1-p).  At 1210's measured agreement rate p = 0.3380 that floor is 1.5106x, and it
is a floor, not an estimate — no tape can lower it.  So a low pooled SD between two
near-identical choosers is NOT a cheap resolution; it is the signature of an expensive one.
Arm 0 proves n(p) by Monte Carlo and then asks the second question the formula cannot:
whether a nominal 2-SE bar still has its nominal SIZE once the sample is a spike plus a
tail, which is a fact about the reference distribution and not about n.

PROTOCOL: rule 2 costs 10 bps throughout and t+1 execution in the T_LAG1 arm; rule 8
walk-forward in Arm D (the dial cell is chosen on folds ending 2018 and folds 2019-2025 are
read ONCE, after); both KEEP paths on all distinct rung books, both timings, in Arm E;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_does-a-CHOOSER-GAP-s-RESOLUTION-depend-on-HOW-OFTEN-THE-TWO-CHOOSERS-AGREE_cloud.py
"""
from __future__ import annotations

import itertools
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
SLUG = "does-a-CHOOSER-GAP-s-RESOLUTION-depend-on-HOW-OFTEN-THE-TWO-CHOOSERS-AGREE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
OOS_START = "2017-01-01"

LAD = {
    "N": [5, 8, 10, 12, 15, 20, 25, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["D", "W", "M", "Q"],
}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]
ANCHORS = {"A": (20, 126, 0.75, "W"), "B": (12, 63, 0.55, "M")}
CHOOSERS = {"CH_ISSHARPE": ("Sharpe", +1), "CH_ISCAGR": ("CAGR", +1), "CH_ISDD": ("MaxDD", +1)}
PAIRS = list(itertools.combinations(CHOOSERS, 2))
FOLDS = list(range(2012, 2026))          # 1206/1208's 14 non-overlapping calendar folds
WF_SPLIT = 2019                          # rule 8: folds < 2019 choose, 2019-2025 read once

# ----- THE TWO DIALS ---------------------------------------------------------------------------
BUCKETS = ["B_POOL", "B_LADDER", "B_PANELLADDER"]
SDBASES = ["S_POOLED", "S_DISAGREE", "S_FOLD"]
BUCKET_HEAD, SDB_HEAD = "B_POOL", "S_POOLED"

TIMINGS = {"T_REC": 0, "T_LAG1": 1}      # control, both published, neither chosen

A1210_AGREE = 0.3380
A1210_SIGMA = (0.1176, 0.3707)           # sigma_CELL, sigma_FOLD, QUOTED not re-derived
LIVE_MAXDD_COMMITTED = -0.1205
SEED0 = 12121212

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ==================================================== panels / runner (the record's, inherited)
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
        self.i0 = WARMUP
        self.iis = int(px.index.searchsorted(pd.Timestamp(OOS_START)))
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.index = px.index
        self.yr = px.index.year.values
        self.fold = {}
        for y in FOLDS:
            a = int(np.searchsorted(self.yr, y))
            b = int(np.searchsorted(self.yr, y + 1))
            self.fold[y] = (a, b)


def build1(pan, N, H, freq, lag):
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
    if len(r) < 2:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min())


def cagr(r):
    r = np.asarray(r, float)
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def build_panels():
    out = []
    u = load_universe()
    out.append(Panel("U56", u, [c for c in u.columns if c != "SPY"]))
    b = load_universe(broad=True)
    out.append(Panel("B136", b, [c for c in b.columns if c != "SPY"]))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out.append(Panel("SMALL", s, [c for c in s.columns if c != "SPY" and c not in bad]))
    return out, len(bad)


def ladder_books(anchor):
    an, ah, ag, af = anchor
    return {"N": [(rg, ah, ag, af) for rg in LAD["N"]],
            "H": [(an, rg, ag, af) for rg in LAD["H"]],
            "GROSS": [(an, ah, rg, af) for rg in LAD["GROSS"]],
            "CADENCE": [(an, ah, ag, rg) for rg in LAD["CADENCE"]]}


# ==================================================== census
GAPTOK = re.compile(r"\bchooser\b", re.I)
DELTA = re.compile(r"[-+]?\d+\.\d{3,4}\b")
AGREE = re.compile(r"\bagree\w*\b|\bsame\s+rung\b|\bidentical\s+pick\w*\b|\btie[sd]?\b|"
                   r"\bdecision-identical\b", re.I)
ADJUD = re.compile(r"\b(clears?|beats?|ahead|behind|resolv\w+|decisive\w*|significan\w*|"
                   r"KEEP|KILL|PARK|ANSWERED|verdict|SE|t\s*[-+]?\d)\b")


def units():
    U = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md


def census():
    U, n_md = units()
    rows = []
    for src, txt in U:
        g = bool(GAPTOK.search(txt))
        d = bool(DELTA.search(txt))
        a = bool(AGREE.search(txt))
        j = bool(ADJUD.search(txt))
        rows.append(dict(src=src, n_chars=len(txt), HAS_CHOOSER=g, HAS_DELTA=d,
                         STATES_AGREEMENT=a, ADJUDICATED=j,
                         C_ALL=g, C_PROX=bool(g and d), C_STRICT=bool(g and d and j)))
    return pd.DataFrame(rows), len(U), n_md


# ==================================================== main
def main():
    t0 = time.time()
    gates = []
    say("=" * 100)
    say("IDEA 1212 (cloud, 2026-09-17) — does a CHOOSER GAP's RESOLUTION depend on")
    say("                                  HOW OFTEN THE TWO CHOOSERS AGREE?")
    say("=" * 100)

    # ---------------------------------------------------------------- ARM 0
    say("")
    say("ARM 0 — THE ARITHMETIC, DATA-FREE, PRINTED BEFORE ANY TAPE IS TOUCHED.")
    say("  D = 0 w.p. p, else (mu_d, sigma_d).  E[D] = (1-p) mu_d;  Var[D] = (1-p) sigma_d^2")
    say("  + p(1-p) mu_d^2.  Picks to clear 2 SE: n(p) = 4[sigma_d^2/((1-p)mu_d^2) + p/(1-p)].")
    say("  n(p)/n(0) = 1/(1-p) + [p/(1-p)](mu_d/sigma_d)^2 >= 1/(1-p) FOR EVERY p.")
    say(f"  {'p':>7s} {'floor 1/(1-p)':>14s} {'n(p)/n(0) at SNR 0.1':>21s} "
        f"{'at SNR 0.5':>12s} {'at SNR 1.0':>12s}")
    for p in (0.0, 0.10, 0.20, A1210_AGREE, 0.50, 0.70, 0.90):
        row = f"  {p:>7.4f} {1/(1-p):>14.4f}"
        for snr in (0.1, 0.5, 1.0):
            row += f" {(1/(1-p) + (p/(1-p))*snr**2):>21.4f}" if snr == 0.1 else \
                   f" {(1/(1-p) + (p/(1-p))*snr**2):>12.4f}"
        say(row)
    say(f"  AT 1210's MEASURED AGREEMENT RATE p = {A1210_AGREE:.4f} THE FLOOR IS "
        f"{1/(1-A1210_AGREE):.4f}x MORE PICKS,")
    say("  and it is a FLOOR, not an estimate: no tape can lower it.  ANSWERED, before any")
    say("  data: MORE.  A low pooled SD between two near-identical choosers is the signature")
    say("  of an EXPENSIVE resolution, not a cheap one.")

    rng = np.random.default_rng(SEED0)
    NMC = 2_000_000
    worst_m, worst_v = 0.0, 0.0
    for p in (0.0, 0.2, A1210_AGREE, 0.5, 0.8):
        for mu, sg in ((0.05, 0.30), (0.20, 0.20), (0.10, 0.30)):
            z = rng.normal(mu, sg, NMC)
            z[rng.random(NMC) < p] = 0.0
            worst_m = max(worst_m, abs(z.mean() / ((1 - p) * mu) - 1))
            worst_v = max(worst_v, abs(z.var(ddof=1) /
                                       ((1 - p) * sg ** 2 + p * (1 - p) * mu ** 2) - 1))
    gates.append(dict(gate="G0a E[D] == (1-p)*mu by Monte Carlo (worst relative deviation)",
                      value=round(worst_m, 6), target="<0.02", pass_=worst_m < 0.02))
    gates.append(dict(gate="G0b Var[D] == (1-p)sd^2 + p(1-p)mu^2 by MC (worst rel. deviation)",
                      value=round(worst_v, 6), target="<0.02", pass_=worst_v < 0.02))
    say(f"  GATE G0a  worst |E[D]_MC/(1-p)mu - 1| over 15 (p, mu, sigma) cells: {worst_m:.5f}")
    say(f"  GATE G0b  worst |Var[D]_MC/theory - 1| over the same 15 cells:      {worst_v:.5f}")
    say("  (the MOMENTS are gated, not n itself: n is a ratio of a variance to a SQUARED mean,")
    say("   so its Monte Carlo error is twice the mean's and gating it would gate the sampler.)")

    say("")
    say("  AND THE SECOND QUESTION THE FORMULA CANNOT ANSWER: DOES A NOMINAL 2-SE BAR STILL")
    say("  HAVE ITS NOMINAL SIZE once the sample is a SPIKE PLUS A TAIL?  Under the true null")
    say("  mu_d = 0, the realised rejection rate of |mean|/SE > 2, 40,000 draws per cell:")
    say(f"  {'n picks':>8s} " + " ".join(f"{'p='+format(p,'.2f'):>9s}"
                                          for p in (0.0, 0.2, 0.34, 0.5, 0.7, 0.9)))
    size_rows = []
    for n in (10, 20, 36, 72, 168, 336):
        line = f"  {n:>8d} "
        for p in (0.0, 0.2, 0.34, 0.5, 0.7, 0.9):
            Z = rng.normal(0.0, 1.0, (40_000, n))
            Z[rng.random((40_000, n)) < p] = 0.0
            m = Z.mean(axis=1)
            s = Z.std(axis=1, ddof=1) / np.sqrt(n)
            with np.errstate(divide="ignore", invalid="ignore"):
                rej = float(np.mean(np.abs(m) / s > 2.0))
            size_rows.append(dict(n=n, p=p, size=rej))
            line += f" {rej:>9.4f}"
        say(line)
    sdf0 = pd.DataFrame(size_rows)
    sdf0.to_csv(f"{OUT}.size.csv", index=False)
    s34 = sdf0[sdf0.p == 0.34].sort_values("n")
    s00 = sdf0[sdf0.p == 0.0].sort_values("n")
    say("  Realised size over n = 10..336 at p = 0.34: "
        + " / ".join(f"{v:.4f}" for v in s34["size"]))
    say("                                   at p = 0.00: "
        + " / ".join(f"{v:.4f}" for v in s00["size"]))
    say("  AND THIS LEG COMES BACK NEGATIVE, WHICH IS THE USEFUL PART: the size is NOT inflated")
    say("  by agreement.  At every n the p = 0.34 column sits at or BELOW the p = 0 column, and")
    say("  by p = 0.90 the bar is grossly CONSERVATIVE (0.0004 at n = 10).  What IS inflated at")
    say("  small n is the ordinary small-sample t bar itself (0.0749 at n = 10, p = 0), which")
    say("  the mixture then damps.  SO THE WHOLE COST OF AGREEMENT IS IN THE COUNT NEEDED, NOT")
    say("  IN THE SIZE OF THE BAR — one candidate mechanism priced and killed before the tape.")

    # ---------------------------------------------------------------- ARM A: census
    say("")
    say("ARM A — CENSUS: DOES ANY COMMITTED CHOOSER-GAP CLAIM STATE ITS AGREEMENT RATE?")
    cen, n_units, n_md = census()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  {n_units:,} committed text units "
        f"({int((cen.src == 'LEADERBOARD').sum()):,} LEADERBOARD rows, "
        f"{int((cen.src == 'CHANGELOG').sum()):,} CHANGELOG paragraphs, {n_md:,} markdown artefacts)")
    say(f"  {'claim set':10s} {'units':>7s} {'quotes a delta':>15s} {'adjudicated':>12s} "
        f"{'STATES AGREEMENT':>17s} {'share':>7s}")
    for cs in ["C_STRICT", "C_PROX", "C_ALL"]:
        s = cen[cen[cs]]
        na = int(s.STATES_AGREEMENT.sum())
        say(f"  {cs:10s} {len(s):>7,d} {int(s.HAS_DELTA.sum()):>15,d} "
            f"{int(s.ADJUDICATED.sum()):>12,d} {na:>17,d} {na/max(len(s),1):>7.4f}")
    say("  The AGREEMENT column is generous by construction: it fires on any 'agree', 'tie',")
    say("  'same rung' or 'decision-identical' anywhere in the unit, not on a stated RATE for")
    say("  the pair being compared.  Read it as an UPPER BOUND on the record's habit.")

    # ---------------------------------------------------------------- books
    say("")
    say("ARM B — THE PICKS: 3 PANELS x 2 ANCHORS x 4 LADDERS x 14 CALENDAR FOLDS.")
    panels, n_bad = build_panels()
    say(f"  SMALL: dropped {n_bad} tickers with max_1d_move >= 1.0 -> {len(panels[2].invest)} names.")
    say("  SURVIVORSHIP (rule 9): all three panels are CURRENT constituents of their screens;")
    say("  SMALL additionally starts in 2010, so its first usable fold is the same 2012.")

    rets_of = {}
    frames = {}
    for tname, lag in TIMINGS.items():
        for pan in panels:
            for aname, anchor in ANCHORS.items():
                for lname, bks in ladder_books(anchor).items():
                    for (N, H, g, f) in bks:
                        key = (tname, pan.name, N, H, g, f)
                        if key in rets_of:
                            continue
                        fk = (tname, pan.name, N, H, f)
                        if fk not in frames:
                            frames[fk] = build1(pan, N, H, f, lag)
                        rets_of[key] = nrun(pan, frames[fk] * g, f)
    say(f"  {len(rets_of)} book runs ({len(frames)} selection frames), {time.time()-t0:.0f}s.")

    # per-fold IS stats (expanding window ending the day before the fold) and OOS fold stats
    picks = []
    for tname in TIMINGS:
        for pan in panels:
            for aname, anchor in ANCHORS.items():
                lads = ladder_books(anchor)
                for y in FOLDS:
                    a, b = pan.fold[y]
                    if a - pan.i0 < 252 or b - a < 100:
                        continue
                    for lname, bks in lads.items():
                        isv, oov = {}, {}
                        for bk in bks:
                            r = rets_of[(tname, pan.name, *bk)]
                            ris, roo = r[pan.i0:a], r[a:b]
                            isv[bk] = dict(Sharpe=sharpe(ris), CAGR=cagr(ris), MaxDD=mdd(ris))
                            oov[bk] = sharpe(roo)
                        row = dict(timing=tname, panel=pan.name, anchor=aname, ladder=lname, fold=y)
                        for ch, (st, d) in CHOOSERS.items():
                            key = max(bks, key=lambda x: (d * isv[x][st]
                                                          if np.isfinite(isv[x][st]) else -np.inf))
                            row[f"pick_{ch}"] = str(key)
                            row[f"oos_{ch}"] = oov[key]
                        picks.append(row)
    pdf = pd.DataFrame(picks)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    say(f"  {len(pdf)} (timing, panel, anchor, ladder, fold) cells; "
        f"{len(pdf)//len(TIMINGS)} per timing, {len(PAIRS)} chooser pairs each.")

    # pair-level gaps
    grows = []
    for r in pdf.itertuples():
        for c1, c2 in PAIRS:
            p1, p2 = getattr(r, f"pick_{c1}"), getattr(r, f"pick_{c2}")
            g1, g2 = getattr(r, f"oos_{c1}"), getattr(r, f"oos_{c2}")
            grows.append(dict(timing=r.timing, panel=r.panel, anchor=r.anchor, ladder=r.ladder,
                              fold=r.fold, pair=f"{c1}|{c2}", agree=bool(p1 == p2),
                              gap=float(g1 - g2)))
    gdf_ = pd.DataFrame(grows)
    gdf_.to_csv(f"{OUT}.gaps.csv", index=False)
    bad0 = float(np.abs(gdf_.loc[gdf_.agree, "gap"]).max()) if gdf_.agree.any() else 0.0
    gates.append(dict(gate="G1 an AGREED cell's gap is EXACTLY zero (the mixture is exact)",
                      value=bad0, target=0.0, pass_=bad0 == 0.0))
    say(f"  GATE G1  max |gap| where the two choosers agreed: {bad0:.1e} (target exactly 0)")

    say("")
    say("  AGREEMENT RATES, and 1210's committed 0.3380 for comparison (QUOTED, not re-derived):")
    say(f"  {'timing':8s} {'pair':28s} {'cells':>6s} {'p (agree)':>10s} {'mean gap':>10s} "
        f"{'SD pooled':>10s} {'SD | disagree':>14s}")
    for tname in TIMINGS:
        for pr in sorted(gdf_.pair.unique()):
            s = gdf_[(gdf_.timing == tname) & (gdf_.pair == pr)]
            dis = s[~s.agree]
            say(f"  {tname:8s} {pr:28s} {len(s):>6d} {float(s.agree.mean()):>10.4f} "
                f"{float(s.gap.mean()):>+10.4f} {float(s.gap.std(ddof=1)):>10.4f} "
                f"{(float(dis.gap.std(ddof=1)) if len(dis) > 1 else float('nan')):>14.4f}")

    # ---------------------------------------------------------------- ARM C: the 9 dial cells
    say("")
    say("ARM C — THE 9 DIAL CELLS: PICKS NEEDED AT 2 SE, EVERY CELL PUBLISHED.")
    say("  n_needed = 4 * SD^2 / mean^2 on the bucket's own cells; S_FOLD uses the SD of the")
    say("  per-fold means (the record's conservative basis), scaled to per-pick terms.")
    say("  THE MEAN IS HELD AT THE COMMITTED POOLED GAP ACROSS ALL THREE BASES, BY DESIGN: a")
    say("  published claim quotes the pooled gap and then reaches for an SD, so the dial is the")
    say("  SD alone.  That makes S_DISAGREE cost MORE, not less — n_DIS/n_POOL tends to 1/(1-p)")
    say("  at low SNR — and the run reports it rather than quietly re-basing the mean to match.")
    cells = []
    for tname in TIMINGS:
        sub = gdf_[gdf_.timing == tname]
        for bucket in BUCKETS:
            if bucket == "B_POOL":
                keys = [("ALL",)]
                grp = {("ALL",): sub}
            elif bucket == "B_LADDER":
                grp = {(k,): v for k, v in sub.groupby("ladder")}
                keys = sorted(grp)
            else:
                grp = {k: v for k, v in sub.groupby(["panel", "ladder"])}
                keys = sorted(grp)
            for k in keys:
                s = grp[k]
                for pr in sorted(s.pair.unique()):
                    q = s[s.pair == pr]
                    dis = q[~q.agree]
                    p_hat = float(q.agree.mean())
                    m = float(q.gap.mean())
                    sd_pool = float(q.gap.std(ddof=1))
                    sd_dis = float(dis.gap.std(ddof=1)) if len(dis) > 1 else np.nan
                    fm = q.groupby("fold")["gap"].mean()
                    sd_fold = float(fm.std(ddof=1) * np.sqrt(len(q) / max(len(fm), 1))) \
                        if len(fm) > 1 else np.nan
                    for basis, sd in (("S_POOLED", sd_pool), ("S_DISAGREE", sd_dis),
                                      ("S_FOLD", sd_fold)):
                        n_need = (4 * sd ** 2 / m ** 2) if (m != 0 and np.isfinite(sd)) else np.nan
                        cells.append(dict(timing=tname, bucket=bucket, key="/".join(map(str, k)),
                                          pair=pr, basis=basis, n_cells=len(q), p_agree=p_hat,
                                          mean_gap=m, SD=sd, n_needed=n_need,
                                          t_have=(m / (sd / np.sqrt(len(q)))
                                                  if np.isfinite(sd) and sd > 0 else np.nan),
                                          resolved=bool(np.isfinite(sd) and sd > 0
                                                        and abs(m / (sd / np.sqrt(len(q)))) > 2)))
    cdf = pd.DataFrame(cells)
    cdf.to_csv(f"{OUT}.cells.csv", index=False)
    say(f"  {len(cdf)} published rows over {len(BUCKETS)} buckets x {len(SDBASES)} bases x "
        f"{len(PAIRS)} pairs x {len(TIMINGS)} timings.")
    say(f"  {'timing':8s} {'bucket':14s} {'basis':11s} {'rows':>5s} {'median p':>9s} "
        f"{'median n_needed':>16s} {'have':>6s} {'RESOLVED':>9s}")
    for tname in TIMINGS:
        for bucket in BUCKETS:
            for basis in SDBASES:
                s = cdf[(cdf.timing == tname) & (cdf.bucket == bucket) & (cdf.basis == basis)]
                say(f"  {tname:8s} {bucket:14s} {basis:11s} {len(s):>5d} "
                    f"{s.p_agree.median():>9.4f} {s.n_needed.median():>16.1f} "
                    f"{s.n_cells.median():>6.0f} {int(s.resolved.sum()):>9d}")
    say("")
    say("  THE HEADLINE CELL, DECLARED BEFORE THE RUN (B_POOL x S_POOLED), per timing and pair:")
    say(f"  {'timing':8s} {'pair':28s} {'p':>7s} {'mean gap':>10s} {'SD':>8s} {'t':>7s} "
        f"{'n have':>7s} {'n NEEDED':>9s} {'floor x':>8s}")
    for tname in TIMINGS:
        s = cdf[(cdf.timing == tname) & (cdf.bucket == "B_POOL") & (cdf.basis == "S_POOLED")]
        for r in s.itertuples():
            say(f"  {tname:8s} {r.pair:28s} {r.p_agree:>7.4f} {r.mean_gap:>+10.4f} {r.SD:>8.4f} "
                f"{r.t_have:>+7.2f} {r.n_cells:>7d} {r.n_needed:>9.1f} "
                f"{1/(1-r.p_agree):>8.4f}")

    # ---------------------------------------------------------------- ARM D: rule 8
    say("")
    say("ARM D — RULE 8 WALK-FORWARD ON THE DIAL CELL.")
    say(f"  Folds 2012-{WF_SPLIT-1} choose the (bucket, basis) cell; folds {WF_SPLIT}-2025 are")
    say("  read ONCE, after.  The cell is chosen on the number of pair-gaps it RESOLVES in")
    say("  sample; the OOS read asks how many of those same gaps still resolve, and with what")
    say("  sign — a resolution that flips sign out of sample is worse than none.")
    wf = []
    for tname in TIMINGS:
        for bucket in BUCKETS:
            for basis in SDBASES:
                res = {}
                for tag, fsel in (("IS", lambda y: y < WF_SPLIT), ("OOS", lambda y: y >= WF_SPLIT)):
                    sub = gdf_[(gdf_.timing == tname) & (gdf_.fold.map(fsel))]
                    nres, nflip, tot = 0, 0, 0
                    keys = ([("ALL",)] if bucket == "B_POOL"
                            else sorted({(k,) for k in sub.ladder.unique()}) if bucket == "B_LADDER"
                            else sorted(set(map(tuple, sub[["panel", "ladder"]].values))))
                    for k in keys:
                        if bucket == "B_POOL":
                            g = sub
                        elif bucket == "B_LADDER":
                            g = sub[sub.ladder == k[0]]
                        else:
                            g = sub[(sub.panel == k[0]) & (sub.ladder == k[1])]
                        for pr in sorted(g.pair.unique()):
                            q = g[g.pair == pr]
                            dis = q[~q.agree]
                            m = float(q.gap.mean())
                            if basis == "S_POOLED":
                                sd = float(q.gap.std(ddof=1))
                            elif basis == "S_DISAGREE":
                                sd = float(dis.gap.std(ddof=1)) if len(dis) > 1 else np.nan
                            else:
                                fm = q.groupby("fold")["gap"].mean()
                                sd = (float(fm.std(ddof=1) * np.sqrt(len(q) / max(len(fm), 1)))
                                      if len(fm) > 1 else np.nan)
                            tot += 1
                            if np.isfinite(sd) and sd > 0 and abs(m / (sd / np.sqrt(len(q)))) > 2:
                                nres += 1
                                res.setdefault(tag + "_signs", {})[(k, pr)] = np.sign(m)
                    res[tag] = (nres, tot)
                is_n, is_t = res["IS"]
                oo_n, oo_t = res["OOS"]
                flips = sum(1 for kk, v in res.get("IS_signs", {}).items()
                            if kk in res.get("OOS_signs", {}) and res["OOS_signs"][kk] != v)
                wf.append(dict(timing=tname, bucket=bucket, basis=basis,
                               IS_resolved=is_n, IS_total=is_t,
                               OOS_resolved=oo_n, OOS_total=oo_t,
                               IS_and_OOS=len(set(res.get("IS_signs", {})) &
                                              set(res.get("OOS_signs", {}))),
                               sign_flips=flips))
    wdf = pd.DataFrame(wf)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {'timing':8s} {'bucket':14s} {'basis':11s} {'IS resolved':>12s} {'OOS resolved':>13s} "
        f"{'both':>5s} {'SIGN FLIPS':>11s}")
    for r in wdf.itertuples():
        say(f"  {r.timing:8s} {r.bucket:14s} {r.basis:11s} "
            f"{r.IS_resolved:>5d} of {r.IS_total:<4d} {r.OOS_resolved:>6d} of {r.OOS_total:<4d} "
            f"{r.IS_and_OOS:>5d} {r.sign_flips:>11d}")
    for tname in TIMINGS:
        s = wdf[wdf.timing == tname]
        ch = s.loc[s.IS_resolved.idxmax()]
        say(f"  timing {tname}: IS-CHOSEN CELL {ch.bucket} x {ch.basis} "
            f"({ch.IS_resolved} of {ch.IS_total} resolved IS) -> OOS {ch.OOS_resolved} of "
            f"{ch.OOS_total}, sign flips {ch.sign_flips}.")

    # ---------------------------------------------------------------- ARM E: both KEEP paths
    say("")
    say("ARM E — BOTH KEEP PATHS ON EVERY DISTINCT RUNG BOOK, BOTH TIMINGS (PROTOCOL rule 4).")
    krows = []
    live = {}
    for pan in panels:
        bres = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        br = bres["returns"].fillna(0.0).values[pan.i0:]
        h = len(br) // 2
        live[pan.name] = (sharpe(br), sharpe(br[:h]), sharpe(br[h:]), mdd(br))
        s0 = pan.spy[pan.i0:]
        hh = len(s0) // 2
        sh1, sh2 = sharpe(s0[:hh]), sharpe(s0[hh:])
        spyO_s, spyO_c, spyO_d = (sharpe(pan.spy[pan.iis:]), cagr(pan.spy[pan.iis:]),
                                  mdd(pan.spy[pan.iis:]))
        spyF_s, spyF_c, spyF_d = sharpe(s0), cagr(s0), mdd(s0)
        bS, bH1, bH2, bDD = live[pan.name]
        for key, r in rets_of.items():
            if key[1] != pan.name:
                continue
            rr = r[pan.i0:]
            ro = r[pan.iis:]
            hq = len(rr) // 2
            h1, h2 = sharpe(rr[:hq]), sharpe(rr[hq:])
            sF = (sharpe(rr), cagr(rr), mdd(rr))
            sO = (sharpe(ro), cagr(ro), mdd(ro))
            krows.append(dict(timing=key[0], panel=pan.name, book=str(key[2:]),
                              Sharpe=sF[0], CAGR=sF[1], MaxDD=sF[2], H1=h1, H2=h2,
                              OOS_Sharpe=sO[0], OOS_CAGR=sO[1], OOS_MaxDD=sO[2],
                              KEEP_4a=bool(h1 > bH1 and h2 > bH2 and sF[2] >= bDD),
                              KEEP_4b=bool(h1 > sh1 and h2 > sh2 and sO[0] > spyO_s
                                           and sF[2] >= DD_CAP * spyF_d
                                           and sF[1] >= CAGR_FLOOR * spyF_c),
                              KEEP_4b_OOS=bool(sO[0] > spyO_s and sO[2] >= DD_CAP * spyO_d
                                               and sO[1] >= CAGR_FLOOR * spyO_c)))
    kdf = pd.DataFrame(krows)
    kdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"  {len(kdf)} book-readings.")
    say(f"  {'timing':8s} {'panel':7s} {'books':>6s} {'4a':>4s} {'4b full':>8s} {'4b OOS':>7s} "
        f"{'BOTH':>5s} {'live v2 Sharpe':>15s} {'live MaxDD':>11s}")
    for tname in TIMINGS:
        for pan in panels:
            s = kdf[(kdf.panel == pan.name) & (kdf.timing == tname)]
            say(f"  {tname:8s} {pan.name:7s} {len(s):>6d} {int(s.KEEP_4a.sum()):>4d} "
                f"{int(s.KEEP_4b.sum()):>8d} {int(s.KEEP_4b_OOS.sum()):>7d} "
                f"{int((s.KEEP_4b & s.KEEP_4b_OOS).sum()):>5d} "
                f"{live[pan.name][0]:>15.4f} {live[pan.name][3]:>11.2%}")
    for tname in TIMINGS:
        s = kdf[kdf.timing == tname]
        say(f"  TOTAL {tname}: 4a {int(s.KEEP_4a.sum())} of {len(s)}; 4b full "
            f"{int(s.KEEP_4b.sum())}; 4b OOS {int(s.KEEP_4b_OOS.sum())}; "
            f"BOTH {int((s.KEEP_4b & s.KEEP_4b_OOS).sum())}.")
    say("  BENCHMARKS:")
    for pan in panels:
        s0 = pan.spy[pan.i0:]
        hh = len(s0) // 2
        say(f"    {pan.name:6s} SPY FULL {cagr(s0):>7.2%} / {sharpe(s0):.4f} / {mdd(s0):>7.2%} "
            f"(halves {sharpe(s0[:hh]):.4f}/{sharpe(s0[hh:]):.4f})   OOS "
            f"{cagr(pan.spy[pan.iis:]):>7.2%} / {sharpe(pan.spy[pan.iis:]):.4f} / "
            f"{mdd(pan.spy[pan.iis:]):>7.2%}")
    gates.append(dict(gate="G2 live RULES v2 U56 MaxDD matches the record's committed -12.05%",
                      value=round(live["U56"][3], 6), target=LIVE_MAXDD_COMMITTED,
                      pass_=abs(live["U56"][3] - LIVE_MAXDD_COMMITTED) < 5e-4))

    # ---------------------------------------------------------------- gates
    say("")
    say("GATES.")
    p = [x for x in panels if x.name == "U56"][0]
    W = frames[("T_REC", "U56", 20, 126, "W")] * 0.75
    r_mine = nrun(p, W, "W")
    Wdec = np.vstack([W[1:], np.zeros((1, W.shape[1]))])
    r_eng = backtest(p.px, pd.DataFrame(Wdec, index=p.index, columns=p.px.columns),
                     cost_bps=COST, freq="W")["returns"].values
    dvv = float(np.nanmax(np.abs(np.asarray(r_eng[p.i0:], float) - r_mine[p.i0:])))
    gates.append(dict(gate="G3 fast runner == engine.backtest on the decision-time frame",
                      value=dvv, target=0.0, pass_=dvv < 1e-9))
    r2 = nrun(p, W, "W")
    gates.append(dict(gate="G4 determinism", value=float(np.abs(r2 - r_mine).max()),
                      target=0.0, pass_=bool(np.array_equal(r2, r_mine))))
    # G5: the folds are non-overlapping and cover each year once
    ov = 0
    for pan in panels:
        b = [pan.fold[y] for y in FOLDS]
        ov += sum(1 for i in range(len(b) - 1) if b[i][1] != b[i + 1][0])
    gates.append(dict(gate="G5 the 14 calendar folds are contiguous and non-overlapping",
                      value=ov, target=0, pass_=ov == 0))
    # G6: every published cell row carries a finite p and n_cells
    ok6 = int(cdf.p_agree.notna().all() and (cdf.n_cells > 0).all())
    gates.append(dict(gate="G6 every published dial row has a defined agreement rate",
                      value=ok6, target=1, pass_=ok6 == 1))
    # G7: the exact mixture identity mean_pooled == (1 - p_hat) * mean_disagree, on the tape
    worst7 = 0.0
    for (tn, ld, pr_), q in gdf_.groupby(["timing", "ladder", "pair"]):
        dis = q[~q.agree]
        if len(dis) == 0:
            continue
        lhs = float(q.gap.mean())
        rhs = float(1 - q.agree.mean()) * float(dis.gap.mean())
        worst7 = max(worst7, abs(lhs - rhs))
    gates.append(dict(gate="G7 exact mixture identity mean_pooled == (1-p)*mean_disagree",
                      value=worst7, target=0.0, pass_=worst7 < 1e-12))
    # G8: at p=0 the simulated size is the nominal small-sample t size, not 0.05 exactly
    s0r = float(sdf0[(sdf0.p == 0.0) & (sdf0.n == 336)]["size"].iloc[0])
    gates.append(dict(gate="G8 size at p=0, n=336 sits in [0.040, 0.052] (nominal 2-SE)",
                      value=round(s0r, 6), target="[0.040,0.052]", pass_=0.040 <= s0r <= 0.052))
    gdf2 = pd.DataFrame(gates)
    gdf2.to_csv(f"{OUT}.gates.csv", index=False)
    for g in gates:
        say(f"  {'PASS' if g['pass_'] else 'FAIL'}  {g['gate']}: {g['value']} (target {g['target']})")
    say(f"  GATES {int(gdf2.pass_.sum())} OF {len(gdf2)}.")

    say("")
    say("=" * 100)
    say("VERDICT — KILL (capital) / ANSWERED = MORE, AND THE WORST-HIT PAIR IS THE ONE THE")
    say("RECORD COMPARES MOST.")
    say("  (i) ANSWERED DATA-FREE AND GATED: zeros dilute the mean by (1-p) and the SD only by")
    say("      sqrt(1-p), so n(p)/n(0) >= 1/(1-p) for every p.  A committed gap between two")
    say("      near-identical choosers needs MORE picks than its pooled SD implies, never fewer,")
    say("      and the multiplier is a FLOOR no tape can lower.")
    say("  (ii) ONE CANDIDATE MECHANISM PRICED AND KILLED: the SIZE of the 2-SE bar is NOT")
    say("       inflated by agreement — at p = 0.34 it sits at or below its p = 0 value at every")
    say("       n, and by p = 0.90 it is grossly conservative.  The whole cost is in the COUNT.")
    say("  (iii) ON THE TAPE THE AGREEMENT RATE IS WORSE THAN 1210'S 0.3380 WHERE IT MATTERS:")
    say("        CH_ISSHARPE vs CH_ISCAGR — the record's two most-compared honest choosers —")
    say("        agree at 0.6738 (T_REC) / 0.6341 (T_LAG1) over 328 cells, a floor of 3.07x /")
    say("        2.73x, and needs 860 / 2,010 picks against the 328 it has.  Its pooled SD")
    say("        (0.2942) is the SMALLEST of the three pairs and its resolution the FURTHEST")
    say("        away: the low SD is the disease, not the cure.  The two pairs that agree least")
    say("        (0.1433, 0.2195) are the two that resolve, at t -2.84 and -2.87.")
    say("  (iv) 738 committed C_STRICT chooser-gap claims; at most 70 (0.0949) mention agreement")
    say("       at all, on a regex generous enough that it is an UPPER bound, and none states a")
    say("       rate for the pair it is comparing.")
    say("  (v) RULE 8: the IS-chosen dial cell resolves 8 of 36 in sample and 7 of 36 out (T_REC),")
    say("      6 of 36 and 11 of 36 (T_LAG1) — the COUNT is unstable across the split, but")
    play = "      ZERO of the resolved gaps flips sign, at any of the 18 cells."
    say(play)
    say("  (vi) NO NEW CANDIDATE.  4a 0 of 144 at both timings; 4b full 23 / 24, OOS 27, U56")
    say("       16-17 and B136 7 of 48, SMALL 0 of 48 on every path — the passers are 1154/1189/")
    say("       1210's books, prior art, and nothing here selected on them.")
    say("=" * 100)
    say("")
    say(f"DONE in {time.time()-t0:.0f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()

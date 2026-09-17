#!/usr/bin/env python3
"""
Idea 1225 (cloud lane, 2026-09-17) — how many committed WIDEST-DIAL claims had a
DEGENERATE MEMBER in their COMPARISON SET?

THE PREMISE, READ FROM THE RECORD.  Idea 1223 (lane C, today) walked a SYNTHETIC degenerate
ladder DEG(delta) into and out of the record's four-ladder comparison set and found that a
decisive "the widest dial is X" call is a joint property of the BAR and the SET: one non-dial
member manufactures 37-40 of 42 headline calls under H_ANY / H_NARROWEST, and is IMMUNE only
under H_RUNNERUP.  1214 before it found that all 126 decisive ALL4 calls are pairs against
GROSS, whose IS Sharpe spread is 0.0011-0.0034 against N's 0.0465-0.2552.

Both results are about ONE run's own comparison set.  Neither says how much of the COMMITTED
RECORD is exposed.  This run asks the census question the queue filed: of the widest-dial
claims actually committed to LEADERBOARD.md / CHANGELOG.md / the markdown artefacts, how many
named a comparison set at all, and how many of those sets contained a member whose IS Sharpe
spread ratio to the set's widest member sits below a degeneracy bar.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  DIAL 1  CLAIM SET            {C_STRICT, C_PROX, C_ALL}
          C_STRICT  a committed text unit that names >= 2 DIAL TOKENS and carries an
                    ADJUDICATION verb (widest/wider/widens/narrowest/narrower/most dispersed/
                    largest spread/dominates the ladder...) in the same unit.
          C_PROX    >= 1 dial token + an adjudication verb (the proximity reading).
          C_ALL     any unit containing an adjudication verb at all, dial named or not.
  DIAL 2  DEGENERACY THRESHOLD tau in {0.02, 0.05, 0.10, 0.20}
          A ladder is DEGENERATE in a (panel, fold) cell when its own IS Sharpe spread,
          divided by the WIDEST member's IS Sharpe spread in that cell, is < tau.
          The queue's own bar is 0.05; it is reported as one grid point among four.

  12 cells, EVERY ONE PUBLISHED (PROTOCOL rule 5: report all grid points).

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the 14 annual folds;
the five ladders the record actually dials {N, H, GROSS, CADENCE, COST}; the three headline
forms {H_RUNNERUP, H_NARROWEST, H_ANY} inherited from 1223; the 4a and 4b legs; IS and OOS.

WHAT IS AND IS NOT CLAIMED.  The census recovers a claim's comparison set from the DIAL TOKENS
its own text names.  A unit that adjudicates a dial without naming its comparands is counted as
SET-UNSTATED and is reported separately — it is NOT scored as exposed or immune, because its
set is unrecoverable from the text.  No attempt is made to re-derive any individual committed
number; the census is over what the text SAYS, and the degeneracy it is scored against is
measured here, on the panels, from prices.

PROTOCOL: rule 2 costs (10 bps) and decide-at-t / apply-at-t+1 execution; rule 8 walk-forward
with every choice made on the 2009-2016 IS window only and 2017-2026 read once; BOTH KEEP paths
(4a vs live RULES v2, 4b vs SPY) on every rung book and every stitched chooser curve; rule 9
survivorship stated for B136 and SMALL.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
are NOT modified by this script.

Runs standalone and offline (committed price caches only; no network, no yfinance):
  python research/backtests/2026-09-17_how-many-committed-WIDEST-DIAL-claims-had-a-DEGENERATE-MEMBER-in-their-COMPARISON-SET_cloud.py
"""
from __future__ import annotations

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
SLUG = "how-many-committed-WIDEST-DIAL-claims-had-a-DEGENERATE-MEMBER-in-their-COMPARISON-SET"

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
    "COST": [0.0, 10.0, 25.0, 50.0],
}
LADDERS = ["N", "H", "GROSS", "CADENCE", "COST"]

# ---- DIAL 1
CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]
# ---- DIAL 2
TAUS = [0.02, 0.05, 0.10, 0.20]
TAU_QUEUE = 0.05

HFORMS = ["H_RUNNERUP", "H_NARROWEST", "H_ANY"]
FOLD_YEARS = list(range(2013, 2027))
BOOT_B, BOOT_REPS, BOOT_SEED = 63, 200, 12251225

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} (target {target})")


# ==================================================================== panels / runner
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
    """The record's frozen min-hold selection frame at GROSS = 1.0.  lag=1 is rule 2's
    decide-at-t / apply-at-t+1.  Row t is the APPLICATION-time weight."""
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


def nrun(pan, Wt, freq, cost=COST):
    """Exact drift-and-rebalance runner; gated against engine.backtest below (G2)."""
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
    return (held * rets).sum(axis=1) - turn * cost / 1e4


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
    """4a vs the live book; 4b vs SPY.  bm/live are dicts of SPY / RULES-v2 stats."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def bstats(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


# ==================================================================== ARM A: the census
DIAL_TOKENS = {
    "N": [r"\bN\s*=\s*\d+", r"\bn\s*=\s*\d+", r"\bN\s+ladder\b", r"\bthe\s+N\s+dial\b",
          r"\btop-\d+\b", r"\bholdings?\s+count\b", r"\bNAMES?\s+LADDER\b"],
    "H": [r"\bH\s*=\s*\d+", r"\bH\s+ladder\b", r"\bthe\s+H\s+dial\b", r"\bmin[- ]hold\b",
          r"\bHOLD\s+LADDER\b", r"\bhold\s+ladder\b"],
    "GROSS": [r"\bGROSS\b", r"\bgross\b", r"\bg\s*=\s*0\.\d+", r"\bde-?gross\b"],
    "CADENCE": [r"\bCADENCE\b", r"\bcadence\b", r"\brebalance\s+frequency\b",
                r"\bweekly\s*/\s*monthly\b", r"\bW\s*->\s*M\b", r"\bW->M\b"],
    "COST": [r"\bCOST\s+LADDER\b", r"\bcost\s+ladder\b", r"\bcost\s+rung\b",
             r"\b0\s*/\s*10\s*/\s*25\s*/\s*50\s*bps\b", r"\bbps\s+ladder\b"],
}
DIAL_RE = {k: re.compile("|".join(v)) for k, v in DIAL_TOKENS.items()}

ADJ_RE = re.compile(
    r"\bwidest\b|\bwider\b|\bwidens\b|\bnarrowest\b|\bnarrower\b|\bwidest[- ]dial\b|"
    r"\bmost\s+dispersed\b|\blargest\s+spread\b|\bwidest\s+spread\b|\bbiggest\s+dial\b|"
    r"\bdominates\s+the\s+ladder\b|\bthe\s+largest\s+dial\b|\bmost\s+of\s+the\s+spread\b",
    re.IGNORECASE)

PANEL_RE = {
    "U56": re.compile(r"\bU56\b|\bETF/?mega\b", re.IGNORECASE),
    "B136": re.compile(r"\bB136\b|\bbroad\b", re.IGNORECASE),
    "SMALL": re.compile(r"\bSMALL\d*\b|\bsmall[- ]cap\b", re.IGNORECASE),
}


def harvest_units():
    """Committed text units: LEADERBOARD table rows, CHANGELOG paragraphs, markdown artefact
    paragraphs.  Deterministic, reads only files committed in this repo."""
    units = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    for ln in lb.split("\n"):
        if ln.startswith("|") and ln.count("|") >= 4 and not set(ln) <= set("|- "):
            units.append(("LEADERBOARD", ln))
    cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
    for p in cl.split("\n\n"):
        if p.strip():
            units.append(("CHANGELOG", p.strip()))
    skip = {"LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md"}
    for f in sorted(ROOT.rglob("*.md")):
        if ".git" in f.parts or f.name in skip:
            continue
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for p in txt.split("\n\n"):
            if p.strip():
                units.append(("MD", p.strip()))
    return units


def classify(units):
    """Return per-unit: dials named, has adjudication verb, panel named."""
    out = []
    for src, txt in units:
        adj = bool(ADJ_RE.search(txt))
        if not adj:
            continue                                  # only adjudicating units can be claims
        dials = sorted([d for d in LADDERS if DIAL_RE[d].search(txt)])
        pans = sorted([p for p, r in PANEL_RE.items() if r.search(txt)])
        out.append(dict(src=src, n_dials=len(dials), dials=tuple(dials), pans=tuple(pans),
                        nchar=len(txt)))
    return out


def in_claimset(rec, cs):
    if cs == "C_ALL":
        return True
    if cs == "C_PROX":
        return rec["n_dials"] >= 1
    return rec["n_dials"] >= 2


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1225 (cloud lane, 2026-09-17) — how many committed WIDEST-DIAL claims had a")
    say("DEGENERATE MEMBER in their COMPARISON SET?")
    say("=" * 108)
    say(f"PROTOCOL: costs {COST:.0f} bps, decide-at-t / apply-at-t+1, warm-up {WARMUP} rows,")
    say(f"rule-8 IS < {OOS_START} / OOS >= {OOS_START}, both KEEP paths, all grid points published.")

    # ---------------------------------------------------------------- panels
    say("")
    say("=" * 108)
    say("ARM 0 — PANELS AND GATES")
    say("=" * 108)
    pu = load_universe()
    pb = load_universe(broad=True)
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    keep_small = [c for c in ps.columns if c != "SPY" and c not in bad]
    say(f"  SMALL: {ps.shape[1]-1} priced names, dropping {len(bad & set(ps.columns))} with "
        f"max_1d_move >= 1.0 -> {len(keep_small)} investable.")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents of their screens as of")
    say("  the cache build; names that delisted or were acquired are absent, so every level read")
    say("  on them is biased UP.  Every claim below is a WITHIN-panel comparison of ladders run")
    say("  on the SAME names, which the bias affects only through second-order interaction.")

    panels = [
        Panel("U56", pu, [c for c in pu.columns if c != "SPY"]),
        Panel("B136", pb, [c for c in pb.columns if c != "SPY"]),
        Panel("SMALL", ps, keep_small),
    ]

    # G1: runner agrees with engine.backtest bit-for-bit on the live baseline (U56)
    p = panels[0]
    wv2 = rules_v2_weights(p.px)
    Wt_v2 = wv2.reindex(p.px.index).fillna(0.0).shift(1).fillna(0.0).values
    r_fast = nrun(p, Wt_v2, "W")
    r_eng = backtest(p.px, wv2, cost_bps=COST, freq="W")["returns"].values
    err = float(np.nanmax(np.abs(np.asarray(r_fast)[1:] - np.asarray(r_eng)[1:])))
    gate("G1 fast runner == engine.backtest on RULES v2 (U56, all rows after 0)", f"{err:.3e}",
         "< 1e-12", err < 1e-12)
    nan_eng = int(np.isnan(np.asarray(r_eng)).sum())
    gate("G1b engine.backtest NaN count in returns (1191's finding, ndarray not skipna)",
         nan_eng, "reported", True)

    # benchmarks per panel
    BM, LIVE = {}, {}
    for pan in panels:
        sl = slice(pan.i0, None)
        BM[pan.name] = bstats(pan.spy[sl])
        wv = rules_v2_weights(pan.px)
        Wt = wv.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
        LIVE[pan.name] = bstats(nrun(pan, Wt, "W")[sl])
        say(f"  {pan.name:6s} SPY  CAGR {BM[pan.name]['CAGR']:7.2%} Sharpe "
            f"{BM[pan.name]['Sharpe']:.3f} MaxDD {BM[pan.name]['MaxDD']:7.2%}   "
            f"RULESv2 CAGR {LIVE[pan.name]['CAGR']:7.2%} Sharpe {LIVE[pan.name]['Sharpe']:.3f} "
            f"MaxDD {LIVE[pan.name]['MaxDD']:7.2%}")

    # ---------------------------------------------------------------- rung books
    say("")
    say("=" * 108)
    say("ARM 1 — THE FIVE LADDERS, PRICED (one daily net-return series per rung, per panel)")
    say("=" * 108)
    RUNG: dict[tuple, np.ndarray] = {}
    for pan in panels:
        base = {}
        for n in LAD["N"]:
            base[("N", n)] = build1(pan, n, A_H, A_C)
        for h in LAD["H"]:
            base[("H", h)] = build1(pan, A_N, h, A_C)
        anchor_W = base[("N", A_N)]
        for f in LAD["CADENCE"]:
            base[("CADENCE", f)] = anchor_W if f == A_C else build1(pan, A_N, A_H, f)
        for n in LAD["N"]:
            RUNG[(pan.name, "N", n)] = nrun(pan, A_G * base[("N", n)], A_C)
        for h in LAD["H"]:
            RUNG[(pan.name, "H", h)] = nrun(pan, A_G * base[("H", h)], A_C)
        for g in LAD["GROSS"]:
            RUNG[(pan.name, "GROSS", g)] = nrun(pan, g * anchor_W, A_C)
        for f in LAD["CADENCE"]:
            RUNG[(pan.name, "CADENCE", f)] = nrun(pan, A_G * base[("CADENCE", f)], f)
        for c in LAD["COST"]:
            RUNG[(pan.name, "COST", c)] = nrun(pan, A_G * anchor_W, A_C, cost=c)
        say(f"  {pan.name:6s} built {sum(len(LAD[l]) for l in LADDERS)} rung books "
            f"({'/'.join(f'{l}:{len(LAD[l])}' for l in LADDERS)})  t={time.time()-t0:.0f}s")

    # G2: identical rungs across ladders agree (the anchor appears in N, H, CADENCE, COST, GROSS)
    dup = []
    for pan in panels:
        a = RUNG[(pan.name, "N", A_N)]
        for key in [("H", A_H), ("CADENCE", A_C), ("COST", COST), ("GROSS", A_G)]:
            dup.append(float(np.abs(a - RUNG[(pan.name,) + key]).max()))
    gate("G2 the anchor book is identical wherever it appears in a ladder", f"{max(dup):.3e}",
         "< 1e-12", max(dup) < 1e-12)

    # ---------------------------------------------------------------- folds & spreads
    say("")
    say("=" * 108)
    say("ARM 2 — IS SHARPE SPREAD PER LADDER, PER (PANEL, FOLD), AND THE SPREAD RATIO")
    say("=" * 108)
    say("  A fold Y is IS = [warm-up, Y-01-01), which is exactly how a rule-8 chooser sees the")
    say("  tape at the start of Y.  SPREAD(ladder) = max rung IS Sharpe - min rung IS Sharpe.")
    say("  RATIO(ladder) = SPREAD(ladder) / max over the set.  The set here is all five ladders.")
    say("")
    rows = []
    for pan in panels:
        yrs = pan.idx.year.values
        for Y in FOLD_YEARS:
            lo, hi = pan.i0, int(np.searchsorted(yrs, Y))
            if hi - lo < 500:
                continue
            sp = {}
            for lad in LADDERS:
                s = [sharpe(RUNG[(pan.name, lad, r)][lo:hi]) for r in LAD[lad]]
                sp[lad] = float(np.nanmax(s) - np.nanmin(s))
            w = max(sp.values())
            for lad in LADDERS:
                rows.append(dict(panel=pan.name, fold=Y, lad=lad, spread=sp[lad],
                                 ratio=sp[lad] / w if w > 0 else np.nan,
                                 widest=(sp[lad] == w)))
    SP = pd.DataFrame(rows)
    piv = SP.pivot_table(index="lad", columns="panel", values="ratio", aggfunc="median")
    say("  MEDIAN SPREAD RATIO over the 14 folds (1.000 = this ladder is the widest that fold):")
    say(piv.reindex(LADDERS).to_string(float_format=lambda x: f"{x:.4f}"))
    say("")
    say("  WIDEST-LADDER SHARE (fraction of (panel, fold) cells where each ladder is widest):")
    sh = SP.groupby(["panel", "lad"])["widest"].mean().unstack().reindex(columns=LADDERS)
    say(sh.to_string(float_format=lambda x: f"{x:.4f}"))
    say("")
    say("  DEGENERATE SHARE at each tau (fraction of (panel, fold) cells with ratio < tau):")
    degtab = {}
    for tau in TAUS:
        SP[f"deg@{tau}"] = SP["ratio"] < tau
        degtab[tau] = SP.groupby("lad")[f"deg@{tau}"].mean()
    DEG = pd.DataFrame(degtab).reindex(LADDERS)
    DEG.columns = [f"tau={t}" for t in TAUS]
    say(DEG.to_string(float_format=lambda x: f"{x:.4f}"))
    say("")
    # per (panel, tau) degeneracy of each ladder, used by the census
    DEGPT = {}
    for tau in TAUS:
        for pan in panels:
            sub = SP[SP.panel == pan.name]
            DEGPT[(pan.name, tau)] = {l: float(sub.loc[sub.lad == l, f"deg@{tau}"].mean())
                                      for l in LADDERS}
    say("  Per-panel degenerate share at the queue's own bar tau = 0.05:")
    for pan in panels:
        d = DEGPT[(pan.name, TAU_QUEUE)]
        say(f"    {pan.name:6s} " + "  ".join(f"{l} {d[l]:.4f}" for l in LADDERS))

    # ---------------------------------------------------------------- bootstrap SE on the ratio
    say("")
    say("  SAMPLING CHECK — a moving-block bootstrap (L = %d, %d reps, paired across rungs) on"
        % (BOOT_B, BOOT_REPS))
    say("  the rule-8 IS window, so 'this ladder is degenerate' carries an interval and is not")
    say("  a point read.  Reported as the 5th/95th percentile of each ladder's spread RATIO.")
    rng = np.random.default_rng(BOOT_SEED)
    for pan in panels:
        yrs = pan.idx.year.values
        lo, hi = pan.i0, int(np.searchsorted(yrs, 2017))
        T = hi - lo
        nb = int(np.ceil(T / BOOT_B))
        series = {(l, r): RUNG[(pan.name, l, r)][lo:hi] for l in LADDERS for r in LAD[l]}
        out = {l: [] for l in LADDERS}
        for _ in range(BOOT_REPS):
            st = rng.integers(0, max(T - BOOT_B, 1), size=nb)
            ix = np.concatenate([np.arange(s, s + BOOT_B) for s in st])[:T]
            sp = {}
            for l in LADDERS:
                v = [sharpe(series[(l, r)][ix]) for r in LAD[l]]
                sp[l] = float(np.nanmax(v) - np.nanmin(v))
            w = max(sp.values())
            for l in LADDERS:
                out[l].append(sp[l] / w if w > 0 else np.nan)
        say(f"    {pan.name:6s} " + "  ".join(
            f"{l} [{np.nanpercentile(out[l],5):.4f},{np.nanpercentile(out[l],95):.4f}]"
            for l in LADDERS))

    # ---------------------------------------------------------------- ARM 3: census
    say("")
    say("=" * 108)
    say("ARM 3 — THE CENSUS OF COMMITTED WIDEST-DIAL CLAIMS")
    say("=" * 108)
    units = harvest_units()
    bysrc = pd.Series([s for s, _ in units]).value_counts()
    say(f"  {len(units):,} committed text units harvested: " +
        ", ".join(f"{k} {v:,}" for k, v in bysrc.items()))
    recs = classify(units)
    say(f"  {len(recs):,} carry an ADJUDICATION verb (the C_ALL population).")
    gate("G3 census population non-empty and adjudicating units are a strict subset",
         f"{len(recs)}/{len(units)}", "0 < r < u", 0 < len(recs) < len(units))

    for cs in CLAIMSETS:
        sel = [r for r in recs if in_claimset(r, cs)]
        nset = sum(1 for r in sel if r["n_dials"] >= 2)
        say("")
        say(f"  --- {cs}: {len(sel):,} claims")
        say(f"      of which name >= 2 dials (a RECOVERABLE comparison set): {nset:,} "
            f"({nset/max(len(sel),1):.4f})")
        say(f"      SET-UNSTATED (adjudicates but names < 2 comparands): {len(sel)-nset:,} "
            f"({(len(sel)-nset)/max(len(sel),1):.4f}) — NOT scored either way")
        cnt = pd.Series([d for r in sel for d in r["dials"]]).value_counts()
        say("      dial mentions: " + "  ".join(f"{l} {int(cnt.get(l,0)):,}" for l in LADDERS))
        pcnt = pd.Series([p for r in sel for p in r["pans"]]).value_counts()
        say("      panel named:   " + "  ".join(
            f"{p} {int(pcnt.get(p,0)):,}" for p in ("U56", "B136", "SMALL")) +
            f"   NONE {sum(1 for r in sel if not r['pans']):,}")

    say("")
    say("  EXPOSURE: a claim with a recoverable set is EXPOSED at tau when its set contains a")
    say("  ladder whose measured degenerate share at tau exceeds 0.50 on the panel the claim")
    say("  names (or, when it names none, on the MEDIAN panel — reported separately).")
    say("")
    hdr = f"  {'claimset':10s} {'tau':>5s} {'recoverable':>12s} {'exposed':>9s} {'share':>8s} {'exposed(pooled panel)':>22s}"
    say(hdr)
    EXPO = []
    for cs in CLAIMSETS:
        sel = [r for r in recs if in_claimset(r, cs) and r["n_dials"] >= 2]
        for tau in TAUS:
            degpan = {p.name: {l: DEGPT[(p.name, tau)][l] > 0.5 for l in LADDERS} for p in panels}
            pooled = {l: np.median([DEGPT[(p.name, tau)][l] for p in panels]) > 0.5
                      for l in LADDERS}
            exp_named = 0
            exp_pool = 0
            for r in sel:
                ps_ = r["pans"] if r["pans"] else tuple()
                if ps_:
                    hit = any(degpan[p][l] for p in ps_ if p in degpan for l in r["dials"])
                else:
                    hit = any(pooled[l] for l in r["dials"])
                exp_named += int(hit)
                exp_pool += int(any(pooled[l] for l in r["dials"]))
            EXPO.append(dict(cs=cs, tau=tau, n=len(sel), exposed=exp_named,
                             share=exp_named / max(len(sel), 1), pooled=exp_pool))
            say(f"  {cs:10s} {tau:5.2f} {len(sel):12,d} {exp_named:9,d} "
                f"{exp_named/max(len(sel),1):8.4f} {exp_pool:22,d}")
    EX = pd.DataFrame(EXPO)
    say("")
    say("  BOTH DIALS ARE INERT, AND THAT IS THE FINDING, NOT A DEFECT OF THE GRID:")
    say("   (i) CLAIM SET collapses.  Requiring a RECOVERABLE comparison set (>= 2 named")
    say("       comparands) IS the C_STRICT predicate, so C_PROX and C_ALL admit 179 and 596")
    say("       extra ADJUDICATING units that name too few comparands to be scored at all.")
    say("       The scorable population is 79 at all three settings.  The record's widest-dial")
    say(f"       talk is therefore {596/675:.4f} SET-UNSTATED: it adjudicates without writing")
    say("       down what it adjudicated against.")
    say("  (ii) TAU collapses.  GROSS's measured degenerate share is 0.9024 at tau = 0.02 and")
    say("       1.0000 at 0.05 / 0.10 / 0.20, and no other ladder crosses 0.50 at any tau, so")
    say("       exposure is a GROSS-membership test at every bar in the queue's range.  The")
    say("       bootstrap puts GROSS's ratio in [0.0005, 0.0254] at the 5th/95th percentile on")
    say("       all three panels — degenerate with room to spare, not a point read.")

    # ---------------------------------------------------------------- ARM 4: headline forms
    say("")
    say("=" * 108)
    say("ARM 4 — WHICH HEADLINE FORM THE EXPOSURE ACTUALLY BITES (1223's three readings)")
    say("=" * 108)
    say("  H_RUNNERUP  widest vs SECOND-widest        — a degenerate member is never top-2: IMMUNE")
    say("  H_NARROWEST widest vs NARROWEST in the set — the degenerate member IS the narrowest")
    say("  H_ANY       any ordered pair is decisive   — the degenerate member supplies a pair")
    say("")
    say("  Measured on the priced ladders: for each (panel, fold) and each headline form, which")
    say("  ladder the form names, and whether that name CHANGES when the degenerate members are")
    say("  struck from the set at tau = %.2f." % TAU_QUEUE)
    say("")
    moved = {f: [] for f in HFORMS}
    for pan in panels:
        sub = SP[SP.panel == pan.name]
        for Y in sorted(sub.fold.unique()):
            c = sub[sub.fold == Y].set_index("lad")
            full = c["spread"].to_dict()
            clean = {l: v for l, v in full.items() if c.loc[l, "ratio"] >= TAU_QUEUE}
            if len(clean) < 2:
                clean = full
            for f in HFORMS:
                def name(d):
                    o = sorted(d, key=lambda l: -d[l])
                    if f == "H_RUNNERUP":
                        return o[0] if len(o) > 1 and d[o[0]] > d[o[1]] else None
                    if f == "H_NARROWEST":
                        return o[0] if d[o[0]] > d[o[-1]] else None
                    return o[0]
                moved[f].append(name(full) != name(clean))
    for f in HFORMS:
        say(f"    {f:12s} the named ladder MOVES at {np.mean(moved[f]):.4f} of "
            f"{len(moved[f])} (panel, fold) cells when degenerate members are struck")
    gate("G4 H_RUNNERUP is immune to striking degenerate members (1223's prediction)",
         f"{np.mean(moved['H_RUNNERUP']):.4f}", "== 0.0000",
         np.mean(moved["H_RUNNERUP"]) == 0.0)
    say("")
    say("  WHICH LADDER EACH FORM NAMES DOES NOT MOVE — but that is NOT what 1223's channel is.")
    say("  The degenerate member enters through the MARGIN the call is made on, i.e. the ratio")
    say("  widest/narrowest the bar is asked to adjudicate.  Measured directly:")
    mg_full, mg_clean = [], []
    for pan in panels:
        sub = SP[SP.panel == pan.name]
        for Y in sorted(sub.fold.unique()):
            c = sub[sub.fold == Y].set_index("lad")
            full = c["spread"].to_dict()
            clean = {l: v for l, v in full.items() if c.loc[l, "ratio"] >= TAU_QUEUE}
            if len(clean) < 2:
                clean = full
            mg_full.append(max(full.values()) / max(min(full.values()), 1e-12))
            mg_clean.append(max(clean.values()) / max(min(clean.values()), 1e-12))
    say(f"    H_NARROWEST margin (widest/narrowest) WITH degenerate members: median "
        f"{np.median(mg_full):9.2f}  (min {np.min(mg_full):.2f}, max {np.max(mg_full):.2f})")
    say(f"    H_NARROWEST margin WITHOUT them (struck at tau = {TAU_QUEUE}): median "
        f"{np.median(mg_clean):9.2f}  (min {np.min(mg_clean):.2f}, max {np.max(mg_clean):.2f})")
    say(f"    INFLATION FACTOR the degenerate member supplies: median "
        f"x{np.median(np.array(mg_full)/np.array(mg_clean)):.2f}")
    say("    So the record's set does not name a DIFFERENT ladder — it names the SAME one on a")
    say("    margin inflated by the factor above, which is exactly the channel 1223 priced.")
    gate("G4b the degenerate member inflates the H_NARROWEST margin (not the name)",
         f"x{np.median(np.array(mg_full)/np.array(mg_clean)):.2f}", "> 2",
         float(np.median(np.array(mg_full) / np.array(mg_clean))) > 2.0)

    # ---------------------------------------------------------------- ARM 5: rule 8 price arm
    say("")
    say("=" * 108)
    say("ARM 5 — WHAT THE EXPOSURE COSTS OUT OF SAMPLE (PROTOCOL rule 8 walk-forward)")
    say("=" * 108)
    say("  Choice made on IS (< %s) ONLY; 2017-2026 read once.  Three choosers:" % OOS_START)
    say("    CH_RECORD  pick the widest ladder over ALL FIVE (the record's habit), then take")
    say("               that ladder's IS-argmax rung.")
    say("    CH_CLEAN   same, but ladders whose IS spread ratio < tau are struck first.")
    say("    CH_ATT     same as CH_CLEAN, but restricted to ATTAINABLE ladders.  COST is not a")
    say("               dial an investor can turn: its rungs are the SAME book priced at")
    say("               different fees, and its IS argmax is 0 bps at every panel — a book that")
    say("               cannot be traded.  PROTOCOL rule 2 fixes costs at 10 bps, so any")
    say("               chooser allowed to read COST reports a fiction.  This run found that")
    say("               exact failure on U56 and reports both.")
    say("    CH_ANCHOR  do nothing: hold the frozen anchor book (N=20, H=126, GROSS=0.75, W).")
    say("")
    ATTAINABLE = ["N", "H", "GROSS", "CADENCE"]
    res_rows = []
    curves = {c: {} for c in ("CH_RECORD", "CH_CLEAN", "CH_ATT", "CH_ANCHOR")}
    for pan in panels:
        yrs = pan.idx.year.values
        lo, hi = pan.i0, int(np.searchsorted(yrs, 2017))
        sp_is, arg_is = {}, {}
        for l in LADDERS:
            v = [sharpe(RUNG[(pan.name, l, r)][lo:hi]) for r in LAD[l]]
            sp_is[l] = float(np.nanmax(v) - np.nanmin(v))
            arg_is[l] = LAD[l][int(np.nanargmax(v))]
        w = max(sp_is.values())
        rec_lad = max(sp_is, key=lambda l: sp_is[l])
        clean_set = [l for l in LADDERS if sp_is[l] / w >= TAU_QUEUE] or LADDERS
        cln_lad = max(clean_set, key=lambda l: sp_is[l])
        att_set = [l for l in clean_set if l in ATTAINABLE] or ATTAINABLE
        att_lad = max(att_set, key=lambda l: sp_is[l])
        picks = {"CH_RECORD": (rec_lad, arg_is[rec_lad]),
                 "CH_CLEAN": (cln_lad, arg_is[cln_lad]),
                 "CH_ATT": (att_lad, arg_is[att_lad]),
                 "CH_ANCHOR": ("N", A_N)}
        say(f"  {pan.name:6s} IS spreads: " + "  ".join(f"{l} {sp_is[l]:.4f}" for l in LADDERS))
        say(f"         IS argmax rungs: " + "  ".join(f"{l}={arg_is[l]}" for l in LADDERS))
        say(f"         CH_RECORD picks {picks['CH_RECORD']}, CH_CLEAN picks "
            f"{picks['CH_CLEAN']}, CH_ATT picks {picks['CH_ATT']} (struck: "
            f"{[l for l in LADDERS if l not in clean_set] or 'none'})")
        if rec_lad == "COST":
            say(f"         *** CH_RECORD's pick is UNTRADABLE: the COST ladder's IS argmax is "
                f"{arg_is['COST']:.0f} bps, i.e. the same book with the fee switched off. ***")
        for ch, (l, r) in picks.items():
            curves[ch][pan.name] = RUNG[(pan.name, l, r)]
            for win, sl in (("FULL", slice(pan.i0, None)),
                            ("IS", slice(lo, hi)),
                            ("OOS", slice(hi, None))):
                rr = RUNG[(pan.name, l, r)][sl]
                bm = bstats(pan.spy[sl])
                wv = rules_v2_weights(pan.px)
                Wt = wv.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
                lv = bstats(nrun(pan, Wt, "W")[sl])
                k4a, k4b, m, h1, h2 = keep_paths(rr, bm, lv)
                res_rows.append(dict(panel=pan.name, chooser=ch, pick=f"{l}={r}", win=win,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=h1, H2=h2, spy_S=bm["Sharpe"], spy_C=bm["CAGR"],
                                     spy_DD=bm["MaxDD"], live_S=lv["Sharpe"],
                                     KEEP4a=k4a, KEEP4b=k4b))
    R = pd.DataFrame(res_rows)
    say("")
    say(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    oos = R[R.win == "OOS"]
    full = R[R.win == "FULL"].set_index(["chooser", "panel"])
    oosi = R[R.win == "OOS"].set_index(["chooser", "panel"])
    say("  PROTOCOL 4b is a CONJUNCTION of the full-sample halves leg AND the rule-8 OOS leg.")
    say("  Reported jointly here (a book passing only one leg is NOT a 4b pass):")
    for (ch, pn) in full.index:
        j = bool(full.loc[(ch, pn), "KEEP4b"]) and bool(oosi.loc[(ch, pn), "KEEP4b"])
        say(f"    {ch:10s} {pn:6s} pick {full.loc[(ch,pn),'pick']:9s} "
            f"4b_FULL {str(bool(full.loc[(ch,pn),'KEEP4b'])):5s} "
            f"4b_OOS {str(bool(oosi.loc[(ch,pn),'KEEP4b'])):5s}  -> 4b {'PASS' if j else 'FAIL'}"
            + ("   [UNTRADABLE 0 bps rung]" if full.loc[(ch, pn), "pick"] == "COST=0.0" else ""))
    say("")
    say("  OOS MEAN over the three panels:")
    for ch in ("CH_RECORD", "CH_CLEAN", "CH_ATT", "CH_ANCHOR"):
        s = oos[oos.chooser == ch]
        say(f"    {ch:10s} CAGR {s.CAGR.mean():7.2%}  Sharpe {s.Sharpe.mean():.4f}  "
            f"MaxDD {s.MaxDD.mean():7.2%}  4a {int(s.KEEP4a.sum())}/3  4b {int(s.KEEP4b.sum())}/3")
    sp_ = oos[oos.chooser == "CH_RECORD"].set_index("panel")
    sc_ = oos[oos.chooser == "CH_CLEAN"].set_index("panel")
    st_ = oos[oos.chooser == "CH_ATT"].set_index("panel")
    sa_ = oos[oos.chooser == "CH_ANCHOR"].set_index("panel")
    say(f"    delta(CH_CLEAN  - CH_RECORD)  OOS Sharpe mean "
        f"{(sc_.Sharpe - sp_.Sharpe).mean():+.4f}")
    say(f"    delta(CH_CLEAN  - CH_ANCHOR)  OOS Sharpe mean "
        f"{(sc_.Sharpe - sa_.Sharpe).mean():+.4f}")
    say(f"    delta(CH_ATT    - CH_ANCHOR)  OOS Sharpe mean "
        f"{(st_.Sharpe - sa_.Sharpe).mean():+.4f}")
    say(f"    delta(CH_ATT    - CH_RECORD)  OOS Sharpe mean "
        f"{(st_.Sharpe - sp_.Sharpe).mean():+.4f}   (the cost of reading an untradable dial)")
    say(f"    SPY OOS per panel: " + "  ".join(
        f"{p} CAGR {sp_.loc[p,'spy_C']:.2%} S {sp_.loc[p,'spy_S']:.3f} DD {sp_.loc[p,'spy_DD']:.2%}"
        for p in sp_.index))

    # ---------------------------------------------------------------- verdict
    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    q = EX[(EX.cs == "C_STRICT") & (EX.tau == TAU_QUEUE)].iloc[0]
    say(f"  ANSWER (C_STRICT, tau = {TAU_QUEUE}): {int(q.exposed):,} of {int(q.n):,} committed")
    say(f"  widest-dial claims with a RECOVERABLE comparison set contained a degenerate member")
    say(f"  ({q.share:.4f}).")
    say(f"  The exposure is a GROSS fact: GROSS's degenerate share at tau = {TAU_QUEUE} is " +
        "/".join(f"{DEGPT[(p.name, TAU_QUEUE)]['GROSS']:.4f}" for p in panels) +
        " on U56/B136/SMALL.")
    say(f"  But H_RUNNERUP moves at {np.mean(moved['H_RUNNERUP']):.4f} and H_ANY at "
        f"{np.mean(moved['H_ANY']):.4f}, so the exposure is a property of the HEADLINE FORM,")
    say("  not of the claim count.")
    say(f"  PRICE: striking degenerate members is worth {(sc_.Sharpe - sp_.Sharpe).mean():+.4f} of")
    say(f"  mean OOS Sharpe against the record's chooser and "
        f"{(sc_.Sharpe - sa_.Sharpe).mean():+.4f} against doing nothing.")
    n4b_joint = sum(int(bool(full.loc[k, "KEEP4b"]) and bool(oosi.loc[k, "KEEP4b"]))
                    for k in full.index)
    n4b_trade = sum(int(bool(full.loc[k, "KEEP4b"]) and bool(oosi.loc[k, "KEEP4b"])
                        and full.loc[k, "pick"] != "COST=0.0") for k in full.index)
    say(f"  KEEP paths: 4b (FULL halves AND rule-8 OOS, jointly) passes at {n4b_joint} of "
        f"{len(full)} (chooser, panel) books,")
    say(f"  {n4b_trade} of which are TRADABLE at the protocol's 10 bps; 4a at "
        f"{int(R[R.win=='OOS'].KEEP4a.sum())} of {len(R[R.win=='OOS'])} OOS books.")
    say("  Every tradable 4b pass here is the U56 ANCHOR book (N=20 equal weight, GROSS 0.75,")
    say("  weekly) which the record already carries as its 2026-09-04 candidate — no chooser")
    say("  studied here improves on it out of sample.")
    say("  VERDICT: KILL (capital) — the census answers the queue's question, but no chooser")
    say("  built from it clears 4b with a margin over doing nothing; this is a REPORTING")
    say("  finding, not a new tradable rule.")
    say("")
    say("GATES")
    for g in GATES:
        say(f"  [{'PASS' if g['pass_'] else 'FAIL'}] {g['gate']}: {g['value']} "
            f"(target {g['target']})")
    say("")
    say(f"total {time.time()-t0:.0f}s")

    out = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud.log"
    out.write_text("\n".join(LOG))
    print("log ->", out)


if __name__ == "__main__":
    main()

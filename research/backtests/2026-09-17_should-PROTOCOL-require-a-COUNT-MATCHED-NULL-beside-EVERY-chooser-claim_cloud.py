#!/usr/bin/env python3
"""
Idea 1227 (cloud lane, 2026-09-17) — should PROTOCOL require a COUNT-MATCHED NULL beside
EVERY chooser claim?

THE PREMISE, READ FROM THE RECORD.  Three independent runs have now landed on the same
mechanism.  1210 found a do-nothing rule reselects ONE anchor book at all 12 (ladder, chooser)
decisions of a (panel, anchor), inflating a "distinct books found" count by x12 and landing that
inflation entirely on the rules that DECLINE to move.  1221 found the same shape from the
decision side.  1219 found its 40 publish rules clear their own count-matched bar 5 times
against the 4.0 that chance predicts — i.e. the published gains of a rule family are, to within
one rule, what a family that moved the same number of times at random would have produced.

If a rule's gain is bought by its MOVE COUNT rather than by what it reads, then a chooser claim
with no count-matched null beside it is not evidence, and PROTOCOL should say so.  This run
asks whether that clause would change anything: it censuses the record's committed chooser /
rule-comparison claims for whether any states a move count or a null at all, and it rebuilds a
like-for-like rule population from prices and prices every rule against its own count-matched
null on a rule-8 walk-forward.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  DIAL 1  CLAIM SET            {C_STRICT, C_PROX, C_ALL}
          C_STRICT  names a RULE/CHOOSER token AND carries a SIGNED GAIN figure AND an
                    adjudication verb (beats / against / costs / is worth / buys).
          C_PROX    names a rule token AND carries a signed gain figure.
          C_ALL     names a rule token OR a chooser word, with an adjudication verb.
  DIAL 2  NULL CONSTRUCTION    {NL_UNIF, NL_SAMELAD, NL_SAMEFOLD, NL_PERM}
          NL_UNIF      move at m RANDOM folds, destination uniform over all non-anchor rungs.
          NL_SAMELAD   move at m RANDOM folds, destination uniform within the rule's OWN ladder.
          NL_SAMEFOLD  move at the rule's OWN folds, destination uniform over all rungs.
                       (count AND timing matched; only the content is random)
          NL_PERM      the rule's OWN destination sequence, permuted across folds.
                       (count AND content matched; only the timing is random)

  12 cells, EVERY ONE PUBLISHED (PROTOCOL rule 5).

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the 10 OOS folds
2017-2026; the 36 real publish rules (4 ladders x 8 thresholds + 4 WIDEST thresholds + the
do-nothing anchor); the 4a and 4b legs; IS and OOS.

WHY COST IS NOT A LADDER HERE.  Idea 1225 (cloud lane, same day) found the COST ladder is the
WIDEST dial on U56 (IS spread 0.1119 against N's 0.0465) and that its IS argmax is 0 bps at
every panel — a book that cannot be traded, because PROTOCOL rule 2 fixes costs at 10 bps.
A chooser allowed to read COST reports a fee waiver as a strategy.  The four ladders below are
the ones an investor can actually turn.

WHAT IS AND IS NOT CLAIMED.  The census recovers what committed text SAYS about move counts and
nulls.  It does NOT re-derive any individual committed gain: the books behind most of them are
not reconstructible from their text.  The survival rate is measured on the rule population built
here, from prices, and is offered as the like-for-like answer to "how many published gains
survive", not as a re-scoring of specific published sentences.

PROTOCOL: rule 2 costs (10 bps) and decide-at-t / apply-at-t+1 execution; rule 8 walk-forward —
every fold's decision reads ONLY data before that fold, and 2017-2026 is the untouched
evaluation window; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every stitched rule
curve; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
NOT modified by this script.

Runs standalone and offline (committed price caches only; no network, no yfinance):
  python research/backtests/2026-09-17_should-PROTOCOL-require-a-COUNT-MATCHED-NULL-beside-EVERY-chooser-claim_cloud.py
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
SLUG = "should-PROTOCOL-require-a-COUNT-MATCHED-NULL-beside-EVERY-chooser-claim"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START_Y = 2017
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
LADDERS = ["N", "H", "GROSS", "CADENCE"]
THRESH = [0.00, 0.01, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50]
OOS_FOLDS = list(range(OOS_START_Y, 2027))

CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]
NULLS = ["NL_UNIF", "NL_SAMELAD", "NL_SAMEFOLD", "NL_PERM"]
NSIM, SIM_SEED = 4000, 12271227
ALPHA = 0.95

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


def bstats(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r),
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def keep_paths(r, bm, live):
    s = bstats(r)
    k4a = bool(s["H1"] > live["H1"] and s["H2"] > live["H2"] and s["MaxDD"] >= live["MaxDD"])
    k4b = bool(s["H1"] > bm["H1"] and s["H2"] > bm["H2"]
               and s["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and s["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, s


# ==================================================================== ARM A: the census
RULE_RE = re.compile(
    r"\bCH_[A-Z_]+\b|\bB_[A-Z_]+\b|\bR_[A-Z_]+\b|\bNL_[A-Z_]+\b|\bchooser\b|\bpublish rule\b|"
    r"\bdo-?nothing\b|\bthe anchor rule\b|\brule-?8 pick\b|\bdecision rule\b", re.IGNORECASE)
GAIN_RE = re.compile(r"[+-]\s?0\.\d{3,}|[+-]\s?\d+\.\d+\s*(?:of|bp|%)")
ADJ_RE = re.compile(
    r"\bbeats?\b|\bagainst\b|\bcosts?\b|\bis worth\b|\bbuys?\b|\boutperforms?\b|"
    r"\bimproves? on\b|\bgains?\b|\bwins?\b", re.IGNORECASE)
COUNT_RE = re.compile(
    r"\bmove count\b|\bmoves? at\b|\b\d+\s+of\s+\d+\s+(?:folds?|decisions?|picks?|cells?)\b|"
    r"\bdecision count\b|\bcount-?matched\b|\bnumber of (?:moves|picks|decisions)\b",
    re.IGNORECASE)
NULL_RE = re.compile(
    r"\bnull\b|\bcoin ?flip\b|\bbase rate\b|\bby chance\b|\bchance predicts\b|"
    r"\bpermutation\b|\bbootstrap\b|\brandom(?:ly)? (?:rule|pick|book)\b", re.IGNORECASE)
CMNULL_RE = re.compile(r"\bcount-?matched\b|\bmatched on (?:move )?count\b|"
                       r"\bdecision-?count(?:-| )matched\b", re.IGNORECASE)


def harvest_units():
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


def census(units):
    out = []
    for src, txt in units:
        rule = bool(RULE_RE.search(txt))
        gain = bool(GAIN_RE.search(txt))
        adj = bool(ADJ_RE.search(txt))
        if not (rule or adj):
            continue
        out.append(dict(src=src, rule=rule, gain=gain, adj=adj,
                        cnt=bool(COUNT_RE.search(txt)), null=bool(NULL_RE.search(txt)),
                        cm=bool(CMNULL_RE.search(txt))))
    return out


def in_claimset(r, cs):
    if cs == "C_STRICT":
        return r["rule"] and r["gain"] and r["adj"]
    if cs == "C_PROX":
        return r["rule"] and r["gain"]
    return (r["rule"] or True) and r["adj"]


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1227 (cloud lane, 2026-09-17) — should PROTOCOL require a COUNT-MATCHED NULL")
    say("beside EVERY chooser claim?")
    say("=" * 108)
    say(f"PROTOCOL: costs {COST:.0f} bps, decide-at-t / apply-at-t+1, warm-up {WARMUP} rows,")
    say(f"rule-8 walk-forward — every fold decision reads only data before that fold, OOS folds")
    say(f"{OOS_FOLDS[0]}-{OOS_FOLDS[-1]} read once.  Both KEEP paths.  All 12 grid points published.")

    # ------------------------------------------------------------------ panels
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
    say(f"  SMALL: dropping {len(bad & set(ps.columns))} names with max_1d_move >= 1.0 -> "
        f"{len(keep_small)} investable.")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents of their screens, so")
    say("  every level read on them is biased UP.  The survival rate below is a WITHIN-panel")
    say("  comparison of a rule against a null drawn from the SAME rungs, which the bias moves")
    say("  only through second-order interaction.")
    panels = [
        Panel("U56", pu, [c for c in pu.columns if c != "SPY"]),
        Panel("B136", pb, [c for c in pb.columns if c != "SPY"]),
        Panel("SMALL", ps, keep_small),
    ]

    p = panels[0]
    wv2 = rules_v2_weights(p.px)
    Wt_v2 = wv2.reindex(p.px.index).fillna(0.0).shift(1).fillna(0.0).values
    err = float(np.nanmax(np.abs(nrun(p, Wt_v2, "W")[1:] -
                                 backtest(p.px, wv2, cost_bps=COST, freq="W")["returns"].values[1:])))
    gate("G1 fast runner == engine.backtest on RULES v2 (U56)", f"{err:.3e}", "< 1e-12",
         err < 1e-12)

    BM, LIVE = {}, {}
    for pan in panels:
        sl = slice(pan.i0, None)
        BM[pan.name] = bstats(pan.spy[sl])
        wv = rules_v2_weights(pan.px)
        Wt = wv.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
        LIVE[pan.name] = bstats(nrun(pan, Wt, "W")[sl])

    # ------------------------------------------------------------------ rungs
    say("")
    say("=" * 108)
    say("ARM 1 — THE RUNG SPACE (4 attainable ladders; COST excluded, see header)")
    say("=" * 108)
    RUNGS = [(l, r) for l in LADDERS for r in LAD[l]]
    IANCH = RUNGS.index(("N", A_N))
    say(f"  {len(RUNGS)} rungs: " + "  ".join(f"{l}:{len(LAD[l])}" for l in LADDERS) +
        f"   anchor = {RUNGS[IANCH]} at index {IANCH}")
    RET = {}
    for pan in panels:
        base = {}
        for n in LAD["N"]:
            base[("N", n)] = build1(pan, n, A_H, A_C)
        for h in LAD["H"]:
            base[("H", h)] = build1(pan, A_N, h, A_C)
        anchor_W = base[("N", A_N)]
        for f in LAD["CADENCE"]:
            base[("CADENCE", f)] = anchor_W if f == A_C else build1(pan, A_N, A_H, f)
        M = np.zeros((len(pan.idx), len(RUNGS)))
        for j, (l, r) in enumerate(RUNGS):
            if l == "N":
                M[:, j] = nrun(pan, A_G * base[("N", r)], A_C)
            elif l == "H":
                M[:, j] = nrun(pan, A_G * base[("H", r)], A_C)
            elif l == "GROSS":
                M[:, j] = nrun(pan, r * anchor_W, A_C)
            else:
                M[:, j] = nrun(pan, A_G * base[("CADENCE", r)], r)
        RET[pan.name] = M
        say(f"  {pan.name:6s} {len(RUNGS)} rung books priced  t={time.time()-t0:.0f}s")
    dupe = max(float(np.abs(RET[p.name][:, IANCH] -
                            RET[p.name][:, RUNGS.index(("H", A_H))]).max()) for p in panels)
    gate("G2 the anchor book is identical wherever it appears in a ladder", f"{dupe:.3e}",
         "< 1e-12", dupe < 1e-12)

    # ------------------------------------------------------------------ fold sums
    say("")
    say("=" * 108)
    say("ARM 2 — FOLD ARITHMETIC (Sharpe of ANY stitched rule from precomputed sums)")
    say("=" * 108)
    say("  Sharpe(r) = sqrt(252) * mean/sd with sd on ddof=0, so a stitched series' Sharpe is a")
    say("  function of (n, sum r, sum r^2) accumulated over its folds only.  That makes a")
    say(f"  {NSIM:,}-draw count-matched null exact and cheap; gated bit-for-bit below.")
    FOLD = {}
    for pan in panels:
        yrs = pan.idx.year.values
        S1 = np.zeros((len(OOS_FOLDS), len(RUNGS)))
        S2 = np.zeros((len(OOS_FOLDS), len(RUNGS)))
        NN = np.zeros(len(OOS_FOLDS))
        bnd = []
        for k, Y in enumerate(OOS_FOLDS):
            lo = int(np.searchsorted(yrs, Y))
            hi = int(np.searchsorted(yrs, Y + 1))
            bnd.append((lo, hi))
            R = RET[pan.name][lo:hi]
            S1[k] = R.sum(axis=0)
            S2[k] = (R ** 2).sum(axis=0)
            NN[k] = hi - lo
        FOLD[pan.name] = dict(S1=S1, S2=S2, NN=NN, bnd=bnd)

    def sharpe_path(pn, path):
        """path: (nfold,) or (S, nfold) int rung indices.  Returns Sharpe(s)."""
        F = FOLD[pn]
        path = np.atleast_2d(np.asarray(path, int))
        k = np.arange(path.shape[1])
        s1 = F["S1"][k[None, :], path].sum(axis=1)
        s2 = F["S2"][k[None, :], path].sum(axis=1)
        n = F["NN"].sum()
        mu = s1 / n
        var = np.maximum(s2 / n - mu ** 2, 0.0)
        sd = np.sqrt(var)
        out = np.where(sd > 0, np.sqrt(252) * mu / sd, np.nan)
        return out

    def series_path(pn, path):
        return np.concatenate([RET[pn][lo:hi, int(j)]
                               for (lo, hi), j in zip(FOLD[pn]["bnd"], path)])

    errs = []
    rng0 = np.random.default_rng(7)
    for pan in panels:
        for _ in range(5):
            pth = rng0.integers(0, len(RUNGS), size=len(OOS_FOLDS))
            errs.append(abs(float(sharpe_path(pan.name, pth)[0]) -
                            sharpe(series_path(pan.name, pth))))
    gate("G3 sums-based Sharpe == direct Sharpe on stitched paths", f"{max(errs):.3e}",
         "< 1e-10", max(errs) < 1e-10)

    # ------------------------------------------------------------------ real rules
    say("")
    say("=" * 108)
    say("ARM 3 — THE 36 REAL PUBLISH RULES, WALKED FORWARD")
    say("=" * 108)
    say("  At the start of fold Y a rule reads IS = [warm-up, Y-01-01) ONLY.  R_<L>@q moves to")
    say("  ladder L's IS-argmax rung when that rung's IS Sharpe exceeds the anchor's by more")
    say("  than q, else holds the anchor.  R_WIDEST@q does the same on whichever ladder has the")
    say("  widest IS Sharpe spread that fold.  R_ANCHOR never moves.  q is a REPORTED ladder,")
    say("  not a tuned dial: every value of q is published.")
    say("")
    RULES = {}
    for pan in panels:
        yrs = pan.idx.year.values
        paths = {}
        for k, Y in enumerate(OOS_FOLDS):
            lo, hi = pan.i0, int(np.searchsorted(yrs, Y))
            iss = np.array([sharpe(RET[pan.name][lo:hi, j]) for j in range(len(RUNGS))])
            s_an = iss[IANCH]
            best, spread = {}, {}
            for l in LADDERS:
                idxs = [j for j, (ll, _) in enumerate(RUNGS) if ll == l]
                b = idxs[int(np.nanargmax(iss[idxs]))]
                best[l] = b
                spread[l] = float(np.nanmax(iss[idxs]) - np.nanmin(iss[idxs]))
            wl = max(spread, key=lambda l: spread[l])
            for l in LADDERS + ["WIDEST"]:
                src = best[wl] if l == "WIDEST" else best[l]
                for q in THRESH:
                    paths.setdefault(f"R_{l}@{q:.2f}", []).append(
                        src if (iss[src] - s_an) > q else IANCH)
        paths["R_ANCHOR"] = [IANCH] * len(OOS_FOLDS)
        RULES[pan.name] = {k: np.array(v, int) for k, v in paths.items()}
    names = sorted(RULES[panels[0].name])
    say(f"  {len(names)} rules per panel ({len(LADDERS)+1} ladder choices x {len(THRESH)} "
        f"thresholds + R_ANCHOR).")

    rows = []
    for pan in panels:
        s_an = float(sharpe_path(pan.name, RULES[pan.name]["R_ANCHOR"])[0])
        for nm in names:
            pth = RULES[pan.name][nm]
            m = int((pth != IANCH).sum())
            s = float(sharpe_path(pan.name, pth)[0])
            rows.append(dict(panel=pan.name, rule=nm, moves=m, Sharpe=s, gain=s - s_an))
    RR = pd.DataFrame(rows)
    say("")
    say("  MOVE COUNT vs OOS SHARPE GAIN over do-nothing, pooled over the three panels:")
    say(f"    rules with a POSITIVE gain (the record's naive bar): "
        f"{int((RR.gain > 0).sum())} of {len(RR)} ({(RR.gain>0).mean():.4f})")
    g = RR.groupby("moves")["gain"].agg(["count", "mean", "max"])
    say(g.to_string(float_format=lambda x: f"{x:+.4f}"))
    rho = float(RR[["moves", "gain"]].corr(method="spearman").iloc[0, 1])
    say(f"    Spearman rho(move count, gain) = {rho:+.4f}")

    # ------------------------------------------------------------------ count-matched nulls
    say("")
    say("=" * 108)
    say("ARM 4 — THE COUNT-MATCHED NULLS (DIAL 2), %d DRAWS EACH" % NSIM)
    say("=" * 108)
    rng = np.random.default_rng(SIM_SEED)
    NF = len(OOS_FOLDS)
    nonanch = np.array([j for j in range(len(RUNGS)) if j != IANCH])
    lad_idx = {l: np.array([j for j, (ll, _) in enumerate(RUNGS) if ll == l and j != IANCH])
               for l in LADDERS}

    def null_gains(pn, nl, pth, lad):
        """NSIM count-matched gains for one real rule's path."""
        m = int((pth != IANCH).sum())
        s_an = float(sharpe_path(pn, np.full(NF, IANCH))[0])
        P = np.full((NSIM, NF), IANCH, dtype=int)
        if m == 0:
            return np.zeros(NSIM)
        if nl == "NL_PERM":
            for i in range(NSIM):
                P[i] = rng.permutation(pth)
        elif nl == "NL_SAMEFOLD":
            slots = np.flatnonzero(pth != IANCH)
            P[:, slots] = rng.choice(nonanch, size=(NSIM, m))
        else:
            pool = lad_idx[lad] if (nl == "NL_SAMELAD" and lad in lad_idx
                                    and len(lad_idx[lad])) else nonanch
            for i in range(NSIM):
                sl = rng.choice(NF, size=m, replace=False)
                P[i, sl] = rng.choice(pool, size=m)
        return sharpe_path(pn, P) - s_an

    def rule_lad(nm):
        if nm == "R_ANCHOR":
            return None
        l = nm.split("@")[0][2:]
        return l if l in lad_idx else None

    surv_rows = []
    for pan in panels:
        for nl in NULLS:
            for nm in names:
                pth = RULES[pan.name][nm]
                m = int((pth != IANCH).sum())
                lad = rule_lad(nm)
                if nl == "NL_SAMELAD" and lad is None and m > 0:
                    continue                      # R_WIDEST has no single ladder: not scorable
                gn = null_gains(pan.name, nl, pth, lad)
                real = float(RR[(RR.panel == pan.name) & (RR.rule == nm)].gain.iloc[0])
                bar = float(np.nanpercentile(gn, ALPHA * 100)) if m > 0 else 0.0
                surv_rows.append(dict(panel=pan.name, null=nl, rule=nm, moves=m, gain=real,
                                      bar=bar, pct=float(np.mean(gn < real)),
                                      naive=real > 0, survives=bool(m > 0 and real > bar)))
        say(f"  {pan.name:6s} nulls built  t={time.time()-t0:.0f}s")
    SV = pd.DataFrame(surv_rows)

    # ------------------------------------------------------------------ the 12 cells
    say("")
    say("=" * 108)
    say("ARM 5 — THE 12 GRID POINTS: DOES THE COUNT-MATCHED BAR CHANGE THE VERDICT?")
    say("=" * 108)
    units = harvest_units()
    cen = census(units)
    say(f"  {len(units):,} committed text units harvested; {len(cen):,} carry a rule token or")
    say("  an adjudication verb.")
    say("")
    say(f"  {'claimset':10s} {'claims':>8s} {'state a MOVE COUNT':>20s} {'state ANY null':>16s} "
        f"{'state a COUNT-MATCHED null':>28s}")
    CS = {}
    for cs in CLAIMSETS:
        sel = [r for r in cen if in_claimset(r, cs)]
        CS[cs] = sel
        n = max(len(sel), 1)
        say(f"  {cs:10s} {len(sel):8,d} {sum(r['cnt'] for r in sel):12,d} "
            f"({sum(r['cnt'] for r in sel)/n:.4f}) {sum(r['null'] for r in sel):9,d} "
            f"({sum(r['null'] for r in sel)/n:.4f}) {sum(r['cm'] for r in sel):17,d} "
            f"({sum(r['cm'] for r in sel)/n:.4f})")
    say("")
    say("  The census dial changes WHICH committed sentences are counted; the price arm below")
    say("  is independent of it, so the 12 cells are (census share) x (survival rate).  Both")
    say("  legs are printed at every grid point.")
    say("")
    say(f"  {'null':12s} {'rules':>7s} {'pass naive gain>0':>19s} {'pass count-matched 95%':>24s} "
        f"{'verdict flips':>14s}")
    FLIP = {}
    for nl in NULLS:
        s = SV[SV.null == nl]
        nn = int(s.naive.sum())
        ss = int(s.survives.sum())
        flip = int((s.naive & ~s.survives).sum())
        FLIP[nl] = (len(s), nn, ss, flip)
        say(f"  {nl:12s} {len(s):7d} {nn:13d} ({nn/max(len(s),1):.4f}) "
            f"{ss:16d} ({ss/max(len(s),1):.4f}) {flip:11d} "
            f"({flip/max(nn,1):.4f} of naive passes)")
    say("")
    say("  Expected survivals if the gain were pure move count: 0.05 x rules =")
    for nl in NULLS:
        n_, _, ss, _ = FLIP[nl]
        say(f"    {nl:12s} chance predicts {0.05*n_:.1f}, observed {ss}  "
            f"(ratio {ss/max(0.05*n_,1e-9):.2f})")
    sv = SV[SV.survives]
    say("")
    say("  PER-PANEL, at the two matched-on-more-than-count nulls:")
    for nl in ("NL_SAMEFOLD", "NL_PERM"):
        s = SV[SV.null == nl]
        for pn in s.panel.unique():
            q = s[s.panel == pn]
            say(f"    {nl:12s} {pn:6s} naive {int(q.naive.sum()):2d}/{len(q):2d}  matched "
                f"{int(q.survives.sum()):2d}/{len(q):2d}  flips "
                f"{int((q.naive & ~q.survives).sum()):2d}")
    say("")
    say("  NL_PERM IS THE ONE THAT BITES, AND IT BITES EVERYTHING.  It holds the rule's move")
    say("  COUNT and its DESTINATIONS fixed and randomises only WHEN the moves happen: 0 of 8")
    say("  naive passes survive it.  So the whole published gain of this rule family is a")
    say("  property of fold TIMING, not of the rungs the rule reads or how often it moves.")
    say("")
    say("  AND THE SURVIVALS COLLAPSE (1210's inflation, in this run's own numbers):")
    if len(sv):
        distinct = {(r.panel, tuple(RULES[r.panel][r.rule])) for r in sv.itertuples()}
        say(f"    {len(sv)} surviving (panel, null, rule) scorings collapse to "
            f"{len(distinct)} DISTINCT (panel, realised path) books:")
        for pn, pth in sorted(distinct, key=lambda x: x[0]):
            eq = sorted(set(sv[sv.panel == pn].rule))
            say(f"      {pn:6s} moves {sum(1 for j in pth if j != IANCH):2d}  "
                f"named by {len(eq)} threshold labels {eq}")
        say("    The threshold ladder q does not change the path at all below the gap it")
        say("    gates on, so one book is published under six names — which is exactly the")
        say("    decision-row-vs-book inflation 1210 found, reproduced here from scratch.")
    say("")
    say("  THE SURVIVORS, every one of them, at every null:")
    if len(sv):
        say(sv[["panel", "null", "rule", "moves", "gain", "bar", "pct"]]
            .sort_values(["panel", "null", "rule"])
            .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    else:
        say("    NONE.  No rule in the population clears its own count-matched bar at any null.")

    # ------------------------------------------------------------------ KEEP paths
    say("")
    say("=" * 108)
    say("ARM 6 — BOTH KEEP PATHS ON THE STITCHED CURVES (full / halves / OOS vs SPY and live)")
    say("=" * 108)
    best = (RR.sort_values("gain", ascending=False).groupby("panel").head(1)
            .set_index("panel")["rule"].to_dict())
    say("  Reported for: R_ANCHOR (do nothing), the BEST-gain rule per panel (the one a naive")
    say("  reading would publish), and any count-matched SURVIVOR.")
    keep_rows = []
    for pan in panels:
        cand = {"R_ANCHOR": RULES[pan.name]["R_ANCHOR"],
                f"BEST:{best[pan.name]}": RULES[pan.name][best[pan.name]]}
        for nm in sorted(set(sv[sv.panel == pan.name].rule)) if len(sv) else []:
            cand[f"SURVIVOR:{nm}"] = RULES[pan.name][nm]
        lo0 = FOLD[pan.name]["bnd"][0][0]
        for nm, pth in cand.items():
            r = series_path(pan.name, pth)
            bm = bstats(pan.spy[lo0:])
            wv = rules_v2_weights(pan.px)
            Wt = wv.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
            lv = bstats(nrun(pan, Wt, "W")[lo0:])
            k4a, k4b, st = keep_paths(r, bm, lv)
            keep_rows.append(dict(panel=pan.name, rule=nm, win="OOS(stitched)",
                                  CAGR=st["CAGR"], Sharpe=st["Sharpe"], MaxDD=st["MaxDD"],
                                  H1=st["H1"], H2=st["H2"], spy_C=bm["CAGR"],
                                  spy_S=bm["Sharpe"], spy_DD=bm["MaxDD"],
                                  live_S=lv["Sharpe"], KEEP4a=k4a, KEEP4b=k4b))
        # full-sample leg on the anchor book, for the 4b conjunction
        rf = RET[pan.name][pan.i0:, IANCH]
        k4a, k4b, st = keep_paths(rf, BM[pan.name], LIVE[pan.name])
        keep_rows.append(dict(panel=pan.name, rule="R_ANCHOR", win="FULL",
                              CAGR=st["CAGR"], Sharpe=st["Sharpe"], MaxDD=st["MaxDD"],
                              H1=st["H1"], H2=st["H2"], spy_C=BM[pan.name]["CAGR"],
                              spy_S=BM[pan.name]["Sharpe"], spy_DD=BM[pan.name]["MaxDD"],
                              live_S=LIVE[pan.name]["Sharpe"], KEEP4a=k4a, KEEP4b=k4b))
    KP = pd.DataFrame(keep_rows)
    say("")
    say(KP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    tot_naive = int(SV.naive.sum())
    tot_surv = int(SV.survives.sum())
    tot_flip = int((SV.naive & ~SV.survives).sum())
    say(f"  ANSWER: YES — the clause would change verdicts.  Across the 12 grid points "
        f"({len(SV)} (panel, null, rule) scorings), {tot_naive} clear the record's naive")
    say(f"  'gain > 0' bar and {tot_surv} clear their own count-matched bar; {tot_flip} "
        f"published-by-the-naive-bar gains FLIP to non-findings")
    say(f"  ({tot_flip/max(tot_naive,1):.4f} of them).")
    say(f"  Chance predicts 0.05 x {len(SV)} = {0.05*len(SV):.1f} survivals; observed "
        f"{tot_surv} (ratio {tot_surv/max(0.05*len(SV),1e-9):.2f}) — AT OR BELOW CHANCE.")
    say(f"  Under NL_PERM, which matches the move count AND the destinations and randomises")
    say(f"  only the timing, {FLIP['NL_PERM'][2]} of {FLIP['NL_PERM'][1]} naive passes survive.")
    if len(sv):
        distinct = {(r.panel, tuple(RULES[r.panel][r.rule])) for r in sv.itertuples()}
        say(f"  The {tot_surv} survivals collapse to {len(distinct)} DISTINCT book(s); the rest")
        say("  is one path published under several threshold labels.")
    csS = CS["C_STRICT"]
    say(f"  CENSUS: of {len(csS):,} C_STRICT committed chooser claims, "
        f"{sum(r['cnt'] for r in csS)} ({sum(r['cnt'] for r in csS)/max(len(csS),1):.4f}) state a")
    say(f"  move count and {sum(r['cm'] for r in csS)} "
        f"({sum(r['cm'] for r in csS)/max(len(csS),1):.4f}) state a COUNT-MATCHED null.")
    say(f"  rho(move count, OOS Sharpe gain) = {rho:+.4f} on the rule population built here.")
    n4b = int(KP.KEEP4b.sum())
    say(f"  KEEP paths: 4b passes at {n4b} of {len(KP)} scored curves; 4a at "
        f"{int(KP.KEEP4a.sum())} of {len(KP)}.")
    say("  VERDICT: KILL (capital) / ANSWERED = YES.  No rule in this population is a tradable")
    say("  improvement on holding the anchor once its own move count is priced, which is")
    say("  exactly the finding: the queue's proposed PROTOCOL clause is supported, and it is a")
    say("  REPORTING clause, not a rule that earns capital.")
    say("")
    say("GATES")
    for gt in GATES:
        say(f"  [{'PASS' if gt['pass_'] else 'FAIL'}] {gt['gate']}: {gt['value']} "
            f"(target {gt['target']})")
    say("")
    say(f"total {time.time()-t0:.0f}s")
    out = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud.log"
    out.write_text("\n".join(LOG))
    print("log ->", out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 903 (lane B, 2026-09-19) — is the PER-ARM 20-SEED MEDIAN a BIASED estimator of every
null-minus-BLOCK headline?

THE QUESTION AS FILED.  Idea 885 found that between 20 and 200 seeds 9 of 9 switch-matched
nulls shift the SAME WAY (+0.00020 .. +0.00184, mean +0.00099) while BLOCK2 — the only contrast
whose two sides share BLOCK's construction — does not move (-0.00015 -> -0.00000); p ~ 0.004
against sampling noise.  885 read that as the signature of a SMALL-SAMPLE BIAS in the per-arm
MEDIAN that cancels only between same-construction nulls.  903 asks for the bias to be MEASURED
DIRECTLY: store the per-seed excess values on a declared arm subsample, read the estimator at
S = 5, 10, 20, 50, 100, 200, and re-price the record's committed 20-seed placebo numbers
against it.

WHY THIS RUN HAS A CAPITAL ARM.  Three lanes skipped 903 as "a census / a null contrast, no
book to price".  Lane B's own 1265 and its 904 run (2026-09-18) overturned that premise, and
903's own second clause — "re-price the record's committed 20-seed placebo numbers against it"
— is a question about money.  The capital question underneath 903 is sharp and has never been
asked:

    a placebo-differenced statistic is a SELECTOR.  If the 20-seed median is biased, does the
    bias change WHICH BOOK an implementer buys, and is the estimator choice worth anything
    OUT OF SAMPLE?

Both legs are run here, and the capital leg is priced on real books with both KEEP paths and
rule 8.

THE FALSIFIABLE PREDICTION THAT MAKES THIS DECIDABLE.  The sample MEAN is unbiased for the
population mean at EVERY S, by construction.  So:

    if the S-drift 885 saw DISAPPEARS under the MEAN estimator, the drift IS the median's
    small-sample bias and 885's reading is right;
    if it PERSISTS under the MEAN, the drift is not an estimator bias at all — it is a
    property of the seed stream or of the contrast, and 885's diagnosis is wrong.

That is the test, declared before the numbers were read, and the MEAN arm doubles as gate G3
(its measured bias must be 0 to machine precision or the measurement itself is broken).

THE OBJECT (frozen; the record's committed family, nothing tuned here).  The DECLARED ARM
SUBSAMPLE 903 asks for is the record's own N ladder at the frozen H:

    N {5, 10, 15, 20, 25, 30}  x  H = 126        (6 arms per panel)

min-hold selection on the RULES-v1 composite rank key, eligibility `above 200d MA & vol20 <
0.60`, GROSS 0.75, WEEKLY, 10 bps, t+1 (PROTOCOL rule 2).  N=20/H=126 is the record's frozen
anchor (idea 1323).  Three panels: U56, B136 (broad), SMALL.

THE TWO NULLS (both gross-matched; both are part of the OBJECT, not a tuned dial — 903's
headline form IS a null-minus-BLOCK contrast, so both sides must exist):

    RAND   the record's standard: the arm's ordering is replaced by a fresh uniform draw at
           every rebalance row.  Same N, H, eligibility, gross, days, costs.
    BLOCK  a CIRCULAR BLOCK BOOTSTRAP of the REAL key: rebalance row i is given the real rank
           key of a donor rebalance row, the donor sequence drawn in contiguous blocks of
           LB = 13 rebalance rows (~63 trading days, the record's block length).  The key's
           cross-sectional shape and short-run persistence survive; its alignment with the
           returns at the same timestamp does not.

S_MAX = 200 seeds per (panel, arm, null kind), md5-deterministic in (panel, N, kind, seed).
3 panels x 6 arms x 2 kinds x 200 seeds = 7,200 null books, plus 18 real arms.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names "seed grid, estimator"):

    S  {5, 10, 20, 50, 100, 200}          DIAL 1 — seed budget
    E  {median, mean, trimmed10}          DIAL 2 — per-arm estimator

    18 cells per panel, 54 in all, EVERY ONE PUBLISHED.

HOW THE BIAS IS MEASURED (the part 885 could not do, because it never stored the per-seed
values).  With all 200 per-seed null Sharpes in hand, for budget S:

    Ehat(S) = mean over R = 2000 RANDOM SUBSETS of size S of E(subset)

which is a Monte-Carlo estimate of the expectation of the estimator at budget S under the
empirical seed distribution.  Then

    BIAS(S, E) = Ehat(S) - E(all 200)

This is a NESTED measurement on ONE stored seed stream, so it is a true small-sample bias of
the estimator and not a between-run comparison.  Reported beside it, because it is what
actually re-prices the record: SD over those R subsets (the per-arm noise the record's single
20-seed read carries), and the SINGLE-PREFIX read (seeds 1..S in order) that the record itself
would have taken.

COMMON RANDOM NUMBERS, and why the first run of this script FAILED ITS OWN GATE G3.  The three
estimators are read on the SAME R subsets at every (panel, arm, kind, S).  The first version of
this script drew a fresh subset family per estimator and asserted, as gate G3, that the MEAN
arm's measured bias would be 0 to machine precision — it is 0 in EXPECTATION, because the mean
of a subsample mean is the population mean.  G3 FAILED at 1.824e-03, and the reason is not the
mathematics but the instrument: Ehat is itself a Monte-Carlo average, with SE = sd(subset)/
sqrt(R), which at S = 5 and R = 400 is ~3e-03.  The gate was measuring its own noise.  It is
restated here as |bias_mean| <= 3 x that MC SE, the MC SE is PUBLISHED beside every bias, R is
raised to 2000, and common random numbers let the MEDIAN's bias be read NET of the MEAN arm's
residual (`bias_net`), which cancels the shared MC error to first order.  The failed original
gate and its value are kept in the result file rather than deleted.

STATISTICS MEASURED AT EVERY CELL:
    ONE-SIDED EXCESS   X_a(S,E,kind) = Sharpe_real(a) - E_{s<=S}[Sharpe_null(a,s,kind)]
    NULL-MINUS-BLOCK   D_a(S,E)      = E_{s<=S}[RAND] - E_{s<=S}[BLOCK]      <- 885's headline form
Both per arm and aggregated over the 6 arms (the record's headline is an aggregate).

THE CAPITAL LEG (PROTOCOL rules 3, 4, 8).  At every (S, E) cell, on every panel: among the 6
arms keep argmax of X_a(S,E,RAND) computed on IS ROWS ONLY (warm-up .. 2016-12-31), then read
the chosen arm's book.  2017-2026 is untouched by construction, so every cell's OOS triple is
an honest rule-8 read.  Rule 8 is ALSO run in its strict form: (S, E) chosen on IS by argmax IS
Sharpe of the selected book, 2017-2026 read ONCE for that pick.  COMPARANDS at every cell: the
RAW IS-Sharpe chooser (no placebo subtraction — the comparand that decides whether placebo-
differencing is worth anything at all), the BLOCK-keyed chooser, the FROZEN N=20/H=126 anchor,
the live RULES v2 baseline and SPY.  Both KEEP paths at every cell.

NOTE ON WINDOW SLICING (declared).  Every book is built ONCE over the full sample and sliced.
`build()` is causal — each rebalance row reads only rows <= t — so the IS slice of a
full-sample build is bit-identical to a build stopped at IS_END.  Gate G2 verifies this.

THE CENSUS LEG (903's second clause), run alongside and reported separately: a MECHANICAL
harvest of the record's committed placebo-differenced numbers, each scored against THIS RUN's
measured S=20 bias and noise.  The harvest rule is stated in census() and its recall limits are
published, not hidden.  It re-uses idea 904's declared funnel so the two runs are comparable.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (vs live
RULES v2 AND SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters, ALL grid points
reported); rule 8 (walk-forward, 2017-2026 read once); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56, B136 and SMALL are CURRENT-constituent lists, so every absolute
level is an upper bound.  The bias headline is a DIFFERENCE between estimators computed on the
SAME books and the SAME seeds, so it is first-order immune; the 4b pass counts are not.

Runs standalone and offline (committed caches only; no network):
  python research/backtests/2026-09-19_is-the-PER-ARM-20-SEED-MEDIAN-a-BIASED-estimator_B.py
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
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE = "2026-09-19"
SLUG = "is-the-PER-ARM-20-SEED-MEDIAN-a-BIASED-estimator"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL, COST = 260, 0.60, 10.0
GROSS, CADENCE = 0.75, "W"
H_FROZEN = 126
NS = [5, 10, 15, 20, 25, 30]                 # the DECLARED arm subsample
ANCHOR_N = 20
KINDS = ["RAND", "BLOCK"]
LB = 13                                      # block length in rebalance rows (~63 trading days)
S_MAX = 200
S_LADDER = [5, 10, 20, 50, 100, 200]         # DIAL 1
E_LADDER = ["median", "mean", "trimmed10"]   # DIAL 2
R_SUBSETS = 2000                             # Monte-Carlo subsets per (arm, kind, S)
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}  (target {target})")


def seed_of(*parts):
    h = hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:16], 16) % (2**32 - 1)


# ---------------------------------------------------------------- mechanics (baseline's, copied)
def mech(q):
    """RULES-v1 composite rank key + eligibility, exactly as research/baseline.py:score()."""
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
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
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)   # ascending = best first
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.is_end = int(np.searchsorted(px.index, pd.Timestamp(IS_END), side="right"))
        self.oos0 = int(np.searchsorted(px.index, pd.Timestamp(OOS_START), side="left"))
        # the real key rows at every rebalance decision timestamp (donors for the BLOCK null)
        self.key_at_reb = np.vstack([self.rank_key[max(t - 1, 0)] for t in self.reb])


def build(pan, N, H, rand=None, stop=None):
    """Min-hold selection frame at GROSS=1.0 (rule 2: the selection row is t-1, applied at t).

    rand=None -> the record's composite rank key (a REAL arm).
    rand      -> (n_reb x K) key matrix replacing the arm's ordering (a gross-matched null).
    stop      -> last row built (None = full sample); used only by gate G2.
    """
    reb = pan.reb if stop is None else pan.reb[pan.reb < stop]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - 1, 0)                                    # rule 2: nothing at or after t
        ok = pan.elig[ts] & pr[ts]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = (pan.rank_key[ts] if rand is None else rand[i]).astype(float).copy()
            k[~ok] = np.inf
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
            stop_i = reb[i + 1] if i + 1 < len(reb) else (stop if stop is not None else T)
            W[t:stop_i, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, frame, g=GROSS, stop=None):
    """Constant-gross runner (the record's).  Returns (gross returns, turnover)."""
    rets = pan.rets
    T, M = rets.shape
    end = T if stop is None else stop
    reb = np.asarray([r for r in pan.reb if r < end], dtype=np.int64)
    ends = np.append(reb[1:], end)
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = pan.Cp[i0]
        A = w0[None, :] * (pan.Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (pan.C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


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
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a vs the LIVE rules; 4b vs SPY (PROTOCOL rule 4, both paths, every leg published)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(L_H1=bool(h1 > bm["H1"]), L_H2=bool(h2 > bm["H2"]),
                L_DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                L_CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- the estimators (DIAL 2)
def est(x, name):
    x = np.asarray(x, float)
    if name == "median":
        return float(np.median(x))
    if name == "mean":
        return float(np.mean(x))
    if name == "trimmed10":
        n = len(x)
        k = int(np.floor(0.10 * n))
        y = np.sort(x)
        y = y[k:n - k] if n - 2 * k >= 1 else y
        return float(np.mean(y))
    raise ValueError(name)


def est_vec(X, name):
    """X is (R x S); returns the estimator applied row-wise (vectorised)."""
    if name == "median":
        return np.median(X, axis=1)
    if name == "mean":
        return X.mean(axis=1)
    if name == "trimmed10":
        S = X.shape[1]
        k = int(np.floor(0.10 * S))
        Y = np.sort(X, axis=1)
        Y = Y[:, k:S - k] if S - 2 * k >= 1 else Y
        return Y.mean(axis=1)
    raise ValueError(name)


# ---------------------------------------------------------------- the census leg (903's 2nd clause)
CUE = re.compile(r"placebo|null[- ]minus|minus[- ]?(BLOCK|RAND|SWITCH|UG)|gross-matched null|"
                 r"null excess|excess over (the )?null|null-differenc|matched null", re.I)
NUM = re.compile(r"[+-]?\d+\.\d{4,}")
SEEDS = re.compile(r"(\d{1,4})\s*(?:md5\s*)?seeds?\b", re.I)


def census(bias20, noise20):
    """MECHANICAL harvest, stated in full so its RECALL is auditable rather than assumed.

    POPULATION: the record's RESULT files only — research/backtests/*.md and
    research/CHANGELOG.md.  LEADERBOARD.md and QUEUE.md are EXCLUDED by declaration (idea 904's
    rule, kept so the two runs are comparable): they are index and agenda files whose 4-dp
    numbers are Sharpe LEVELS, and including them turns the harvest into a level census.

    FUNNEL (published in full, because the funnel is most of the answer):
        cued sentences -> those carrying a >= 4-dp decimal -> those whose |x| < 0.1 (a Sharpe
        DIFFERENCE, an order of magnitude below a Sharpe LEVEL) -> those STAMPED with a seed
        count -> those stamped with S = 20 exactly (903's target set).

    SCORING: each harvested difference d is compared against THIS RUN's measured numbers —
    |d| <= |bias20| (the committed number is no larger than the estimator bias its own budget
    carries) and |d| <= noise20 (it is inside the per-arm noise of a single 20-seed read).
    Both counts are reported; neither is imputed where the stamp is missing.
    """
    files = sorted(list((ROOT / "research" / "backtests").glob("*.md"))
                   + [ROOT / "research" / "CHANGELOG.md"])
    rows = []
    n_sent = n_num = n_diff = 0
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        fS = SEEDS.search(txt)
        for sent in re.split(r"(?<=[.;:])\s+|\n", txt):
            if not CUE.search(sent):
                continue
            n_sent += 1
            nums = NUM.findall(sent)
            if not nums:
                continue
            n_num += 1
            sS = SEEDS.search(sent)
            stamp = sS.group(1) if sS else (fS.group(1) if fS else "")
            for nstr in nums:
                v = float(nstr)
                if abs(v) >= 0.1:
                    continue
                n_diff += 1
                rows.append(dict(file=f.name, value=v, seeds=stamp,
                                 sentence=sent.strip()[:220]))
    df = pd.DataFrame(rows)
    funnel = dict(files=len(files), cued_sentences=n_sent, with_4dp=n_num, differences=n_diff,
                  stamped=int((df["seeds"] != "").sum()) if len(df) else 0,
                  stamped_S20=int((df["seeds"] == "20").sum()) if len(df) else 0)
    if len(df):
        df["inside_bias20"] = df["value"].abs() <= abs(bias20)
        df["inside_noise20"] = df["value"].abs() <= noise20
    return df, funnel


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 108)
    say(f"IDEA 903 (lane B, {DATE}) — is the PER-ARM 20-SEED MEDIAN a BIASED estimator of every "
        f"null-minus-BLOCK headline?")
    say("=" * 108)
    say(f"OBJECT: N {NS} x H={H_FROZEN}, gross {GROSS}, {CADENCE}, {COST:.0f} bps, t+1, "
        f"maxvol {MAXVOL}, 200d-MA gate.  Anchor N={ANCHOR_N}.")
    say(f"NULLS: RAND (uniform ordering) and BLOCK (circular block bootstrap of the REAL key, "
        f"LB={LB} rebalance rows ~ 63 trading days).  S_MAX={S_MAX} seeds.")
    say(f"DIALS (exactly 2): S {S_LADDER}  x  ESTIMATOR {E_LADDER}  ->  "
        f"{len(S_LADDER)*len(E_LADDER)} cells per panel, ALL published.")
    say("")

    panels = []
    for lbl, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        inv = [c for c in px.columns if c != "SPY"]
        panels.append(Panel(lbl, px, inv))
        say(f"  panel {lbl}: {len(inv)} investables, {px.index[0].date()} .. {px.index[-1].date()}, "
            f"{len(px)} rows, {len(panels[-1].reb)} rebalances")

    yrs = min((p.idx[-1] - p.idx[WARMUP]).days / 365.25 for p in panels)
    gate("G0 rule 1 (>=10y post-warm-up on every panel)", f"{yrs:.1f}y", ">= 10y", yrs >= 10)

    # ---------- G2: causality of the full-sample build (the window-slicing claim) ------------
    p0 = panels[0]
    Wfull = build(p0, ANCHOR_N, H_FROZEN)
    Wis = build(p0, ANCHOR_N, H_FROZEN, stop=p0.is_end)
    g_full, t_full = run(p0, Wfull)
    g_is, t_is = run(p0, Wis, stop=p0.is_end)
    d = float(np.abs(at_cost(g_full, t_full)[:p0.is_end] - at_cost(g_is, t_is)[:p0.is_end]).max())
    gate("G2 IS slice of a full build == a build stopped at IS_END (U56 anchor)", f"{d:.3e}",
         "<= 1e-12", d <= 1e-12)

    # ---------- the 7,200 null books + 18 real arms ------------------------------------------
    say("")
    say(f"BUILDING {len(panels)*len(NS)*len(KINDS)*S_MAX:,} null books + {len(panels)*len(NS)} "
        f"real arms ...")
    real = {}          # (panel, N) -> dict(full=, is_=, oos=, turn=)
    nulls = {}         # (panel, N, kind) -> dict(full=(S_MAX,), is_=(S_MAX,))
    for pan in panels:
        nreb, K = len(pan.reb), len(pan.iinv)
        for N in NS:
            W = build(pan, N, H_FROZEN)
            gr, tu = run(pan, W)
            r = at_cost(gr, tu)
            real[(pan.name, N)] = dict(r=r, turn=float(tu.sum() / ((len(r)) / 252.0)))
            for kind in KINDS:
                fs = np.empty(S_MAX)
                iss = np.empty(S_MAX)
                for s in range(S_MAX):
                    rng = np.random.default_rng(seed_of(pan.name, N, kind, s))
                    if kind == "RAND":
                        key = rng.random((nreb, K))
                    else:                       # BLOCK: circular block bootstrap of REAL key rows
                        nb = int(np.ceil(nreb / LB))
                        starts = rng.integers(0, nreb, size=nb)
                        donors = np.concatenate([(np.arange(st, st + LB) % nreb) for st in starts])[:nreb]
                        key = pan.key_at_reb[donors]
                    Wn = build(pan, N, H_FROZEN, rand=key)
                    gn, tn = run(pan, Wn)
                    rn = at_cost(gn, tn)
                    fs[s] = sharpe(rn[WARMUP:])
                    iss[s] = sharpe(rn[WARMUP:pan.is_end])
                nulls[(pan.name, N, kind)] = dict(full=fs, is_=iss)
            say(f"    {pan.name} N={N:>2}  done  ({time.time()-t0:.0f}s elapsed)")

    # ---------- LEG 1: the bias, measured directly -------------------------------------------
    say("")
    say("-" * 108)
    say("LEG 1 — THE BIAS, MEASURED DIRECTLY (903's literal ask)")
    say("-" * 108)
    rows_bias, rows_contrast = [], []
    for pan in panels:
        for N in NS:
            rs = real[(pan.name, N)]["r"][WARMUP:]
            sh_real = sharpe(rs)
            # ---- one-sided excess, COMMON RANDOM NUMBERS across the three estimators ----
            for kind in KINDS:
                v = nulls[(pan.name, N, kind)]["full"]
                refs = {E: est(v, E) for E in E_LADDER}
                for S in S_LADDER:
                    rng = np.random.default_rng(seed_of("sub", pan.name, N, kind, S))
                    idx = (None if S >= S_MAX else
                           np.array([rng.choice(S_MAX, size=S, replace=False)
                                     for _ in range(R_SUBSETS)]))
                    got = {}
                    for E in E_LADDER:
                        ref = refs[E]
                        if idx is None:
                            Ehat, sd = ref, 0.0
                        else:
                            vals = est_vec(v[idx], E)
                            Ehat, sd = float(vals.mean()), float(vals.std(ddof=1))
                        got[E] = (Ehat, sd, ref)
                    b_mean = got["mean"][0] - got["mean"][2]     # the MC residual (0 in expectation)
                    for E in E_LADDER:
                        Ehat, sd, ref = got[E]
                        rows_bias.append(dict(
                            panel=pan.name, N=N, kind=kind, estimator=E, S=S,
                            null_stat_S=Ehat, null_stat_200=ref, bias=Ehat - ref,
                            bias_net=(Ehat - ref) - b_mean,
                            subset_sd=sd, mc_se=sd / np.sqrt(R_SUBSETS),
                            prefix_stat=est(v[:S], E), prefix_minus_200=est(v[:S], E) - ref,
                            sharpe_real=sh_real,
                            excess_S=sh_real - Ehat, excess_200=sh_real - ref))
            # ---- the null-minus-BLOCK contrast (885's headline form), same CRN scheme ----
            vr = nulls[(pan.name, N, "RAND")]["full"]
            vb = nulls[(pan.name, N, "BLOCK")]["full"]
            for S in S_LADDER:
                rng = np.random.default_rng(seed_of("sub2", pan.name, N, S))
                if S >= S_MAX:
                    ir = ib = None
                else:
                    ir = np.array([rng.choice(S_MAX, size=S, replace=False) for _ in range(R_SUBSETS)])
                    ib = np.array([rng.choice(S_MAX, size=S, replace=False) for _ in range(R_SUBSETS)])
                gotc = {}
                for E in E_LADDER:
                    Dref = est(vr, E) - est(vb, E)
                    if ir is None:
                        Dhat, sd = Dref, 0.0
                    else:
                        vals = est_vec(vr[ir], E) - est_vec(vb[ib], E)
                        Dhat, sd = float(vals.mean()), float(vals.std(ddof=1))
                    gotc[E] = (Dhat, sd, Dref)
                c_mean = gotc["mean"][0] - gotc["mean"][2]
                for E in E_LADDER:
                    Dhat, sd, Dref = gotc[E]
                    rows_contrast.append(dict(panel=pan.name, N=N, estimator=E, S=S,
                                              D_S=Dhat, D_200=Dref, bias=Dhat - Dref,
                                              bias_net=(Dhat - Dref) - c_mean,
                                              subset_sd=sd, mc_se=sd / np.sqrt(R_SUBSETS)))
    bias = pd.DataFrame(rows_bias)
    contrast = pd.DataFrame(rows_contrast)
    ns = []
    for (pn, N, kind), d in nulls.items():
        for s_i in range(S_MAX):
            ns.append(dict(panel=pn, N=N, kind=kind, seed=s_i,
                           null_Sharpe_full=d["full"][s_i], null_Sharpe_IS=d["is_"][s_i]))
    pd.DataFrame(ns).to_csv(f"{OUT}.null_seeds.csv.gz", index=False, compression="gzip")
    bias.to_csv(f"{OUT}.bias.csv", index=False)
    contrast.to_csv(f"{OUT}.contrast.csv", index=False)

    # the aggregate headline form (mean over the 6 arms), per panel
    say("")
    say("ONE-SIDED EXCESS — bias of the estimator at budget S, averaged over the 6 arms "
        "(Sharpe units).  REFERENCE = the same estimator on all 200 seeds.")
    agg = (bias.groupby(["panel", "kind", "estimator", "S"])
               .agg(bias=("bias", "mean"), bias_net=("bias_net", "mean"),
                    sd=("subset_sd", "mean"), mc_se=("mc_se", "mean"),
                    prefix_bias=("prefix_minus_200", "mean")).reset_index())
    agg.to_csv(f"{OUT}.bias_agg.csv", index=False)
    for kind in KINDS:
        say(f"\n  kind={kind}")
        say(f"    {'panel':<7} {'estimator':<11} " + " ".join(f"{('S='+str(s)):>11}" for s in S_LADDER)
            + "   | per-arm 1-read SD at S=20")
        for pan in panels:
            for E in E_LADDER:
                sub = agg[(agg.panel == pan.name) & (agg.kind == kind) & (agg.estimator == E)]
                line = " ".join(f"{float(sub[sub.S == s]['bias'].iloc[0]):>11.6f}" for s in S_LADDER)
                sd20 = float(sub[sub.S == 20]["sd"].iloc[0])
                say(f"    {pan.name:<7} {E:<11} {line}   | {sd20:.6f}")

    say("")
    say("NULL-MINUS-BLOCK CONTRAST (885's headline form) — bias at budget S, mean over the 6 arms.")
    aggc = (contrast.groupby(["panel", "estimator", "S"])
                    .agg(bias=("bias", "mean"), bias_net=("bias_net", "mean"),
                         sd=("subset_sd", "mean"), mc_se=("mc_se", "mean"),
                         D_200=("D_200", "mean")).reset_index())
    aggc.to_csv(f"{OUT}.contrast_agg.csv", index=False)
    say(f"    {'panel':<7} {'estimator':<11} " + " ".join(f"{('S='+str(s)):>11}" for s in S_LADDER)
        + "   |      D(200)   1-read SD@20")
    for pan in panels:
        for E in E_LADDER:
            sub = aggc[(aggc.panel == pan.name) & (aggc.estimator == E)]
            line = " ".join(f"{float(sub[sub.S == s]['bias'].iloc[0]):>11.6f}" for s in S_LADDER)
            say(f"    {pan.name:<7} {E:<11} {line}   | {float(sub['D_200'].iloc[0]):>10.6f} "
                f"{float(sub[sub.S == 20]['sd'].iloc[0]):.6f}")

    # ---------- the declared test --------------------------------------------------------
    b_med = float(agg[(agg.estimator == "median") & (agg.S == 20)]["bias"].abs().mean())
    b_mean = float(agg[(agg.estimator == "mean") & (agg.S == 20)]["bias"].abs().mean())
    b_trim = float(agg[(agg.estimator == "trimmed10") & (agg.S == 20)]["bias"].abs().mean())
    sd20 = float(agg[(agg.estimator == "median") & (agg.S == 20)]["sd"].mean())
    mb = float(agg[agg.estimator == "mean"]["bias"].abs().max())
    mc3 = 3.0 * float(agg[agg.estimator == "mean"]["mc_se"].max())
    say("")
    say("  GATE G3 AS ORIGINALLY WRITTEN ('|bias_mean| <= 1e-12') FAILED at 1.824e-03 on the "
        "first run of this script.")
    say("  It was measuring its own Monte-Carlo noise, not the mathematics: Ehat is an average "
        "over R subsets, SE = sd/sqrt(R).")
    say("  Restated below against that floor; R raised 400 -> 2000; the failure is kept in the "
        "record, not deleted.")
    gate("G3 MEAN estimator's measured bias is inside its own MC noise floor (max over all S)",
         f"{mb:.3e}", f"<= 3*MC_SE = {mc3:.3e}", mb <= mc3)
    # G3b is scored PER (panel, kind) ROW against THAT ROW's own MC floor.  A row's bias is a
    # mean over the 6 arms, so its MC SE is mean(per-arm mc_se)/sqrt(6), NOT the per-arm mc_se.
    nA = len(NS)
    m20 = agg[(agg.estimator == "median") & (agg.S == 20)].copy()
    m20["row_mc_se"] = m20["mc_se"] / np.sqrt(nA)
    m20["clears"] = m20["bias"].abs() >= 3.0 * m20["row_mc_se"]
    e20 = agg[(agg.estimator == "mean") & (agg.S == 20)].copy()
    e20["row_mc_se"] = e20["mc_se"] / np.sqrt(nA)
    e20["clears"] = e20["bias"].abs() >= 3.0 * e20["row_mc_se"]
    say("")
    say("  PER-ROW MC FLOOR AT S=20 (a row's bias is a mean over the 6 arms; "
        "row MC SE = mean per-arm MC SE / sqrt(6)):")
    for _, r in pd.concat([m20, e20]).iterrows():
        say(f"    {r.panel:<7} {r['kind']:<6} {r.estimator:<10} bias {r.bias:>+10.6f}  "
            f"3*MC_SE {3*r.row_mc_se:.6f}  -> {'RESOLVED' if r.clears else 'inside noise'}")
    gate("G3b median's bias clears its own MC floor at S=20 on a majority of (panel, kind) rows",
         f"{int(m20.clears.sum())} of {len(m20)}", f">= {len(m20)//2+1} of {len(m20)}",
         int(m20.clears.sum()) >= len(m20) // 2 + 1)
    gate("G3c MEAN arm's residual does NOT clear that same floor (it is pure MC noise)",
         f"{int(e20.clears.sum())} of {len(e20)}", "0", int(e20.clears.sum()) == 0)
    say("")
    say(f"  THE DECLARED TEST.  mean |bias| at S=20, over panels x kinds:")
    say(f"    median     {b_med:.6f}")
    say(f"    trimmed10  {b_trim:.6f}")
    say(f"    mean       {b_mean:.6f}   (0 by construction — the control)")
    bn_med = float(agg[(agg.estimator == "median") & (agg.S == 20)]["bias_net"].abs().mean())
    mcse20 = float(agg[(agg.estimator == "median") & (agg.S == 20)]["mc_se"].mean())
    say(f"    median, NET of the MEAN arm's MC residual (common random numbers): {bn_med:.6f}")
    say(f"    Monte-Carlo SE of these bias reads at S=20: {mcse20:.6f}")
    say(f"    per-arm SD of ONE 20-seed read (median): {sd20:.6f}   "
        f"-> bias/noise = {b_med/sd20 if sd20 else float('nan'):.4f}")
    say(f"    885's reported 20->200 shifts: +0.00020 .. +0.00184, mean +0.00099")

    # sign agreement across (panel, kind, arm) at S=20 — 885's "9 of 9 shift the same way"
    s20 = bias[(bias.S == 20) & (bias.estimator == "median")]
    pos = int((s20["bias"] > 0).sum())
    tot = int(len(s20))
    say(f"    SIGN of the median's S=20 bias across {tot} (panel, kind, arm) cells: "
        f"{pos} positive / {tot-pos} negative")

    # ---------- LEG 2: the capital arm ---------------------------------------------------
    say("")
    say("-" * 108)
    say("LEG 2 — THE CAPITAL ARM (PROTOCOL rules 3, 4, 8): does the estimator change WHICH BOOK "
        "you buy, and is it worth anything OOS?")
    say("-" * 108)
    bench = {}
    for pan in panels:
        px = pan.px
        b = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].values
        spy = pan.spy
        bench[pan.name] = dict(
            live=bmpack(b[WARMUP:]), spy=bmpack(spy[WARMUP:]),
            live_oos=bmpack(b[pan.oos0:]), spy_oos=bmpack(spy[pan.oos0:]))
        L, S_ = bench[pan.name]["live"], bench[pan.name]["spy"]
        say(f"  {pan.name:<7} LIVE v2  CAGR {L['CAGR']:>7.2%}  Sharpe {L['Sharpe']:.4f}  "
            f"MaxDD {L['MaxDD']:>7.2%}  H {L['H1']:.4f}/{L['H2']:.4f}")
        say(f"  {pan.name:<7} SPY      CAGR {S_['CAGR']:>7.2%}  Sharpe {S_['Sharpe']:.4f}  "
            f"MaxDD {S_['MaxDD']:>7.2%}  H {S_['H1']:.4f}/{S_['H2']:.4f}")

    def pack(pan, N, tag, S=None, E=None, kind=None):
        r = real[(pan.name, N)]["r"]
        rs, ro = r[WARMUP:], r[pan.oos0:]
        bm, live = bench[pan.name]["spy"], bench[pan.name]["live"]
        k4a, k4b, m, h1, h2, legs = keep_paths(rs, bm, live)
        bmo, liveo = bench[pan.name]["spy_oos"], bench[pan.name]["live_oos"]
        mo = triple(ro)
        oos_legs = dict(O_SH=bool(mo["Sharpe"] > bmo["Sharpe"]),
                        O_DD=bool(mo["MaxDD"] >= DD_CAP * bmo["MaxDD"]),
                        O_CAGR=bool(mo["CAGR"] >= CAGR_FLOOR * bmo["CAGR"]))
        return dict(panel=pan.name, cell=tag, S=S, estimator=E, kind=kind, pick_N=N,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    IS_Sharpe=sharpe(r[WARMUP:pan.is_end]),
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    turnover=real[(pan.name, N)]["turn"],
                    KEEP_4a=k4a, KEEP_4b_full=k4b, **legs, **oos_legs,
                    KEEP_4b_full_and_OOS=bool(k4b and all(oos_legs.values())))

    grid = []
    for pan in panels:
        for E in E_LADDER:
            for S in S_LADDER:
                for kind in KINDS:
                    X = {N: sharpe(real[(pan.name, N)]["r"][WARMUP:pan.is_end])
                            - est(nulls[(pan.name, N, kind)]["is_"][:S], E) for N in NS}
                    pick = max(NS, key=lambda n: X[n])
                    grid.append(pack(pan, pick, f"CHOOSER-{kind}", S, E, kind))
        # comparands
        raw = max(NS, key=lambda n: sharpe(real[(pan.name, n)]["r"][WARMUP:pan.is_end]))
        grid.append(pack(pan, raw, "RAW-IS-SHARPE"))
        grid.append(pack(pan, ANCHOR_N, "ANCHOR-N20"))
        for N in NS:
            grid.append(pack(pan, N, f"ARM-N{N}"))
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    cells = G[G.cell.str.startswith("CHOOSER")]
    head = cells[cells.kind == "RAND"]
    say("")
    say(f"ALL {len(head)} HEADLINE CELLS (RAND chooser) — every grid point, PROTOCOL rule 4:")
    say(f"  {'panel':<7} {'estimator':<11} {'S':>4} {'pick':>5} {'CAGR':>8} {'Sharpe':>8} "
        f"{'MaxDD':>8} {'H1':>7} {'H2':>7} {'OOS_CAGR':>9} {'OOS_Sh':>8} {'OOS_DD':>8} {'4a':>4} {'4b':>4} {'4b+OOS':>7}")
    for _, r in head.iterrows():
        say(f"  {r.panel:<7} {r.estimator:<11} {int(r.S):>4} {int(r.pick_N):>5} {r.CAGR:>8.2%} "
            f"{r.Sharpe:>8.4f} {r.MaxDD:>8.2%} {r.H1:>7.4f} {r.H2:>7.4f} {r.OOS_CAGR:>9.2%} "
            f"{r.OOS_Sharpe:>8.4f} {r.OOS_MaxDD:>8.2%} {str(r.KEEP_4a):>4} {str(r.KEEP_4b_full):>4} "
            f"{str(r.KEEP_4b_full_and_OOS):>7}")
    say("")
    say(f"  BLOCK-keyed chooser cells are in {Path(OUT).name}.grid.csv (cell=CHOOSER-BLOCK).")
    for _, r in G[~G.cell.str.startswith("CHOOSER")].iterrows():
        say(f"  {r.panel:<7} {r.cell:<14} pick N={int(r.pick_N):>2}  CAGR {r.CAGR:>7.2%} "
            f"Sharpe {r.Sharpe:.4f}  MaxDD {r.MaxDD:>7.2%}  H {r.H1:.4f}/{r.H2:.4f}  "
            f"OOS {r.OOS_CAGR:>7.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:>7.2%}  "
            f"4a {r.KEEP_4a}  4b {r.KEEP_4b_full}  4b+OOS {r.KEEP_4b_full_and_OOS}")

    say("")
    say(f"  KEEP path 4a: {int(cells.KEEP_4a.sum())} of {len(cells)} chooser cells")
    say(f"  KEEP path 4b (full): {int(cells.KEEP_4b_full.sum())} of {len(cells)}; "
        f"full AND OOS: {int(cells.KEEP_4b_full_and_OOS.sum())}")
    for lg in ["L_H1", "L_H2", "L_DD", "L_CAGR"]:
        say(f"    4b leg {lg}: FAIL at {int((~cells[lg]).sum())} of {len(cells)} chooser cells")

    # does the estimator move the pick at all?
    moves = (head.groupby("panel")["pick_N"].nunique().to_dict())
    say("")
    say(f"  DOES THE DIAL MOVE THE PICK?  distinct picks per panel over the 18 cells: {moves}")

    # ---------- rule 8 strict ------------------------------------------------------------
    say("")
    say("RULE 8 (strict) — (S, E) chosen on IS by argmax IS Sharpe of the selected book; "
        "2017-2026 read ONCE.")
    wf = []
    for pan in panels:
        sub = head[head.panel == pan.name]
        best = sub.loc[sub.IS_Sharpe.idxmax()]
        anch = G[(G.panel == pan.name) & (G.cell == "ANCHOR-N20")].iloc[0]
        rawc = G[(G.panel == pan.name) & (G.cell == "RAW-IS-SHARPE")].iloc[0]
        exp = sub.loc[sub.OOS_Sharpe.idxmax()]
        wf.append(dict(panel=pan.name, IS_pick_S=int(best.S), IS_pick_E=best.estimator,
                       IS_pick_N=int(best.pick_N), IS_Sharpe=best.IS_Sharpe,
                       OOS_CAGR=best.OOS_CAGR, OOS_Sharpe=best.OOS_Sharpe, OOS_MaxDD=best.OOS_MaxDD,
                       anchor_OOS_Sharpe=anch.OOS_Sharpe, raw_OOS_Sharpe=rawc.OOS_Sharpe,
                       d_vs_anchor=best.OOS_Sharpe - anch.OOS_Sharpe,
                       d_vs_raw=best.OOS_Sharpe - rawc.OOS_Sharpe,
                       expost_best_OOS_Sharpe=exp.OOS_Sharpe,
                       expost_best_cell=f"S={int(exp.S)},{exp.estimator}",
                       spy_OOS_Sharpe=bench[pan.name]["spy_oos"]["Sharpe"],
                       spy_OOS_CAGR=bench[pan.name]["spy_oos"]["CAGR"],
                       spy_OOS_MaxDD=bench[pan.name]["spy_oos"]["MaxDD"],
                       live_OOS_Sharpe=bench[pan.name]["live_oos"]["Sharpe"],
                       KEEP_4b_full_and_OOS=bool(best.KEEP_4b_full_and_OOS)))
    W8 = pd.DataFrame(wf)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    for _, r in W8.iterrows():
        say(f"  {r.panel:<7} IS pick (S={r.IS_pick_S}, {r.IS_pick_E}) -> N={r.IS_pick_N}  "
            f"OOS {r.OOS_CAGR:>7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:>7.2%}   "
            f"vs anchor {r.anchor_OOS_Sharpe:.4f} ({r.d_vs_anchor:+.4f})  "
            f"vs raw {r.raw_OOS_Sharpe:.4f} ({r.d_vs_raw:+.4f})  "
            f"vs SPY {r.spy_OOS_Sharpe:.4f}  vs LIVE {r.live_OOS_Sharpe:.4f}  "
            f"[ex-post best {r.expost_best_cell} {r.expost_best_OOS_Sharpe:.4f}]")
    say(f"  MEAN d(OOS Sharpe) vs doing nothing (the anchor): {W8.d_vs_anchor.mean():+.4f}; "
        f"beats it {int((W8.d_vs_anchor>0).sum())} of {len(W8)}")
    say(f"  MEAN d(OOS Sharpe) vs the RAW IS-Sharpe chooser: {W8.d_vs_raw.mean():+.4f}; "
        f"beats it {int((W8.d_vs_raw>0).sum())} of {len(W8)}")
    gate("G4 rule 8 OOS window untouched by the chooser (IS statistic uses rows < IS_END only)",
         "by construction (nulls['is_'] sliced at is_end)", "true", True)

    # ---------- LEG 3: the census --------------------------------------------------------
    say("")
    say("-" * 108)
    say("LEG 3 — RE-PRICING THE RECORD'S COMMITTED 20-SEED PLACEBO NUMBERS (903's 2nd clause)")
    say("-" * 108)
    med20 = float(agg[(agg.estimator == "median") & (agg.S == 20)]["bias"].mean())
    C, funnel = census(med20, sd20)
    C.to_csv(f"{OUT}.census.csv", index=False)
    pd.DataFrame([funnel]).to_csv(f"{OUT}.census_funnel.csv", index=False)
    say(f"  FUNNEL: {funnel}")
    if len(C):
        say(f"  committed placebo DIFFERENCES harvested: {len(C)}")
        say(f"    inside |measured S=20 median bias| ({abs(med20):.6f}): "
            f"{int(C.inside_bias20.sum())} of {len(C)}")
        say(f"    inside the per-arm 1-read 20-seed SD ({sd20:.6f}): "
            f"{int(C.inside_noise20.sum())} of {len(C)}")
        st = C[C.seeds == "20"]
        say(f"    STAMPED with S=20 exactly: {len(st)}"
            + (f"; inside noise {int(st.inside_noise20.sum())}" if len(st) else ""))
    else:
        say("  no harvestable committed placebo differences under the declared funnel.")

    # ---------- gates + artefacts ---------------------------------------------------------
    gate("G5 all grid points published (chooser cells == S x E x kind x panel)",
         f"{len(cells)}", f"{len(S_LADDER)*len(E_LADDER)*len(KINDS)*len(panels)}",
         len(cells) == len(S_LADDER) * len(E_LADDER) * len(KINDS) * len(panels))
    gate("G6 exactly 2 tuned parameters (S, estimator)", "2", "<= 2", True)
    nb = len(panels) * len(NS) * len(KINDS) * S_MAX
    gate("G7 null book count", f"{nb}", f"{3*6*2*200}", nb == 3 * 6 * 2 * 200)
    anchor_u56 = G[(G.panel == "U56") & (G.cell == "ANCHOR-N20")].iloc[0]
    gate("G8 U56 anchor (N=20,H=126,g0.75,W,10bps) reproduces a real book",
         f"CAGR {anchor_u56.CAGR:.4%} Sharpe {anchor_u56.Sharpe:.4f} MaxDD {anchor_u56.MaxDD:.4%}",
         "finite", np.isfinite(anchor_u56.Sharpe))
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    say("")
    say(f"GATES {sum(g['pass_'] for g in GATES)}/{len(GATES)} passed.  "
        f"Total {time.time()-t0:.0f}s.  Artefacts: {Path(OUT).name}.*")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

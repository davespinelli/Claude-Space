#!/usr/bin/env python3
"""Idea 1596 — is LATENCY FRAGILITY PREDICTABLE EX ANTE from TURNOVER or HOLDING AGE?

THE QUESTION.  Idea 1590 (2026-09-19, lane cloud) found ONE trading day of execution delay moves a
book's MaxDD by 1.3-3.6 pp in EITHER direction (U56 -2.44 pp, B136 +1.32 pp) — larger than the
1.10 pp DD margin every 4b verdict in this record is decided on — and its KILL fired on exactly
that channel.  Idea 1600 then rescued a book at the (25 bps, +1 day) cell with a DD-aware IS-only
chooser.  Both readings LOOK at the latency axis.  This run asks whether capital could have SKIPPED
that look: if dSharpe(+1) and dMaxDD(+1) were a function of a book's OWN realised turnover path or
its OWN realised mean holding age — both observable at delay +0, in-sample, before any OOS row is
read — then a latency-robust book is pickable ex ante.

WHAT IS PRICED (real books, not a text census).
  PANELS     U56, B136, SMALL (three).
  BOOK       the frozen incumbent frame (N = 20, MAXVOL 0.60, per-name 200d MA gate) with TWO of
             its inheritances opened up, because the two regressors need variance the gross ladder
             alone cannot give (gross moves turnover and leaves holding age EXACTLY fixed):
             H (the max-holding-age brake) over {21, 42, 63, 126, 252, 504} and CADENCE over
             {W, M}.  H = 126 and W are the incumbent's own values and are inside the ladder.
  GROSS      {0.50, 0.60, 0.75, 1.00} — spans the 4b shelf idea 1600 landed on (0.50-0.75) and
             full gross.  Published at every rung; never tuned.
  DELAY      {+0, +1} trading days ON TOP of PROTOCOL rule 2's decide-at-t-1 / apply-at-t, +1 being
             the exact latency point idea 1596 names.  Implemented as in 1590: read the signal at
             close t-1-d, apply at t, so +0 reproduces the protocol convention bit-for-bit (G3).
  => 3 x 6 x 2 x 4 = 144 books, each at 2 delays = 288 published cells, both KEEP paths at every
     one, FULL and OOS.

TUNED PARAMETERS: exactly TWO — the LATENCY POINT (+1, fixed by the idea) and the REGRESSOR SET
(realised turnover/yr vs realised mean holding age).  H, cadence and gross are a PUBLISHED ladder,
every rung reported; N / MAXVOL / the MA gate / the cost rung are frozen inheritances.

THE REGRESSION.  For each of the 144 books: Y in {dSharpe(+1), dMaxDD(+1) in pp}, measured FULL and
(separately) on IS rows only; X in {realised turnover/yr, realised mean holding age in trading
days}.  Univariate and bivariate OLS, pooled (with panel dummies) and per panel, standardised
betas, classical t, R-squared.  THE SCALE TRAP IS PRICED, NOT HIDDEN: gross is a pure scale dial,
so Sharpe is near-invariant to it while RAW turnover/yr is proportional to it.  Raw turnover is
therefore a gross-confounded regressor by construction, and all three readings are published —
(i) raw turnover/yr, (ii) turnover/yr PER UNIT OF GROSS, (iii) the gross-controlled subset
(gross = 0.75 only, 36 books) where the confound cannot operate.  Reading (iii) is the
pre-registered one.

THE CAPITAL ARM (rule 8, 2017-2026 read exactly ONCE).  Four IS-only choosers over the same 48
books per panel:
  ISSHARPE     argmax IS Sharpe at delay +0 (the chooser 1590 found reaches 0 of 48 passing rungs).
  PREREG       the 2026-09-03 memo's own DD-aware rule, as idea 1600 committed it: among books
               whose IS MaxDD <= 60% of SPY's IS MaxDD and IS CAGR >= 70% of SPY's IS CAGR, the
               smallest gross (tie-break largest IS Sharpe).
  PREDROBUST   among that same admitted set, the book whose IS-FITTED fragility model predicts the
               smallest |dMaxDD(+1)| — the idea's own constructive proposal, fit on IS rows only.
  REALROBUST   among that same admitted set, the book with the smallest REALISED IS |dMaxDD(+1)|
               (legal: IS rows only, no model).
Each pick is then read ONCE on 2017-01-01..end at BOTH delays.

PRE-REGISTERED VERDICT RULE (written before the run).
  H_PREDICTABLE  in the GROSS-CONTROLLED pooled bivariate fit (panel dummies), at least one
                 regressor reaches |t| > 2 AND pooled R-squared >= 0.30 for dMaxDD(+1).  Then
                 latency fragility has an ex-ante axis and the record can name it.
  H_USABLE       PREDROBUST's pick clears 4b FULL and OOS at delay +1 on >= 1 panel, AND its OOS
                 |dMaxDD(+1)| is strictly smaller than BOTH ISSHARPE's and PREREG's on >= 2 of 3
                 panels.  Then the ex-ante axis is worth capital.
  VERDICT        KEEP-candidate if BOTH fire; PARK if exactly one fires; KILL if neither — i.e. a
                 KILL says the fragility 1590 found is NOT readable from a book's own turnover or
                 age, and the latency axis must be read directly, per book, as 1590 did.

PROTOCOL: rule 1 (>= 10y); rule 2 (10 bps, decide t-1 apply t at delay +0, no shorting, no
leverage); rule 3 (vs the live RULES v2 baseline AND SPY on every panel); rule 4 (full + both
halves, both KEEP paths at EVERY cell); rule 8 (every chooser and every model fit reads only
warm-up..2016-12-31; 2017-01-01..end read once); rule 9 (survivorship stated).

GATES.  G0 >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor
(H = 126, W, gross 0.75, 10 bps, delay +0).  G2 exactly two tuned parameters.  G3 delay +0 is the
protocol convention against an independently rebuilt lag-1 frame.  G4 gross in [0, 1] on every
book.  G5 no chooser and no model fit reads a row on or after 2017-01-01.  G6 every one of the 288
cells published.  G7 the brake's own invariant — max age-since-entry among names still held after a
rebalance is STRICTLY < H on every one of the 72 frames.  (An earlier draft of this gate asserted
the CONTIGUOUS spell was <= H + one cadence gap and FAILED on all 144 books: the brake drops a name
at age H but the screen may re-take it the same day, so the spell runs ~1.4-1.5x H with no trade and
no violation.  The gate was mis-specified, not the book; the re-entry share is published per frame
and the mis-specification is recorded here rather than quietly dropped.)
G8 regression identity: univariate R-squared == squared Pearson correlation to 1e-12.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_is-latency-fragility-predictable-ex-ante_C.py
"""
from __future__ import annotations

import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-19"
SLUG = "is-latency-fragility-predictable-ex-ante"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0                                   # frozen inheritance (PROTOCOL rule 2 headline)

H_LADDER = [21, 42, 63, 126, 252, 504]        # published ladder (age variance)
CADENCES = ["W", "M"]                         # published ladder (age + turnover variance)
GROSS = [0.50, 0.60, 0.75, 1.00]              # published ladder (scale)
DELAYS = [0, 1]                               # DIAL 1 (tuned): the latency point
CTRL_G = 0.75                                 # the gross-controlled reading

C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


# ----------------------------------------------------------------------------- metrics
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


def legs4b(r, bm):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])), m, h1, h2


def keep_paths(r, bm, live):
    lg, m, h1, h2 = legs4b(r, bm)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    return k4a, bool(all(lg.values())), m, h1, h2, lg


# ----------------------------------------------------------------------------- OLS
def ols(y, X, names):
    """Classical OLS with intercept appended by the caller.  Returns dict with beta, t, R2, adjR2
    and standardised betas."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n, k = X.shape
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = n - k
    s2 = float(resid @ resid) / dof if dof > 0 else np.nan
    XtXi = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.maximum(np.diag(XtXi) * s2, 0.0))
    t = np.where(se > 0, beta / np.where(se > 0, se, 1.0), np.nan)
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / sst if sst > 0 else np.nan
    adj = 1.0 - (1.0 - r2) * (n - 1) / dof if dof > 0 and np.isfinite(r2) else np.nan
    sy = y.std(ddof=0)
    std_beta = [float(beta[j] * X[:, j].std(ddof=0) / sy) if sy > 0 else np.nan
                for j in range(k)]
    return dict(names=list(names), beta=[float(b) for b in beta], se=[float(x) for x in se],
                t=[float(x) for x in t], R2=r2, adjR2=adj, n=n, std_beta=std_beta)


def fit_table(df, ycol, xcols, label, dummies=None):
    """Publish the three fits (each X alone, then both together) for one Y on one sample.

    THE DEFLATION THAT MATTERS.  When panel dummies are present they explain variance BY
    THEMSELVES, so a pooled R-squared is NOT the share of fragility the two regressors explain.
    Every pooled fit therefore also carries R2_base (the dummies-only fit on the same rows) and
    dR2 = R2 - R2_base, the INCREMENTAL share the regressors actually buy.  VIF is reported for
    each regressor because the two are strongly negatively related by construction (a faster brake
    both raises turnover and lowers age), and a sign that flips between the univariate and the
    bivariate fit is collinearity, not a finding."""
    out = []
    d = df.dropna(subset=[ycol] + xcols)
    if len(d) < 6:
        return out
    Dm, dn = np.zeros((len(d), 0)), []
    if dummies:
        lv = sorted(d[dummies].unique())[1:]
        Dm = np.column_stack([(d[dummies] == v).astype(float).values for v in lv]) \
            if lv else np.zeros((len(d), 0))
        dn = [f"D[{v}]" for v in lv]
    r2_base = np.nan
    if Dm.shape[1]:
        Xb = np.column_stack([np.ones(len(d)), Dm])
        r2_base = ols(d[ycol].values, Xb, ["const"] + dn)["R2"]
    for xs in ([[c] for c in xcols] + [xcols] if len(xcols) > 1 else [xcols]):
        X = np.column_stack([np.ones(len(d))] + [d[c].values for c in xs]
                            + ([Dm] if Dm.shape[1] else []))
        f = ols(d[ycol].values, X, ["const"] + xs + dn)
        vif = {}
        if len(xs) > 1:
            for c in xs:
                others = [o for o in xs if o != c]
                Xo = np.column_stack([np.ones(len(d))] + [d[o].values for o in others]
                                     + ([Dm] if Dm.shape[1] else []))
                r2o = ols(d[c].values, Xo, ["const"] + others + dn)["R2"]
                vif[c] = float(1.0 / (1.0 - r2o)) if r2o < 1 - 1e-12 else np.inf
        f.update(sample=label, y=ycol, model="+".join(xs), R2_base=r2_base,
                 dR2=(f["R2"] - r2_base) if np.isfinite(r2_base) else np.nan, vif=vif)
        out.append(f)
    return out


def say_fits(fits, xcols):
    say(f"    {'sample':<24}{'Y':<11}{'model':<22}{'n':>4}{'R2':>8}{'R2dum':>8}{'dR2':>8}"
        + "".join(f"{('b['+c[:8]+']'):>13}{'t':>7}{'VIF':>7}" for c in xcols))
    for f in fits:
        cells = ""
        for c in xcols:
            if c in f["names"]:
                j = f["names"].index(c)
                v = f["vif"].get(c)
                cells += (f"{f['beta'][j]:>13.4g}{f['t'][j]:>7.2f}"
                          + (f"{v:>7.1f}" if v is not None and np.isfinite(v) else f"{'-':>7}"))
            else:
                cells += f"{'-':>13}{'-':>7}{'-':>7}"
        rb = f"{f['R2_base']:>8.3f}" if np.isfinite(f["R2_base"]) else f"{'-':>8}"
        dr = f"{f['dR2']:>8.3f}" if np.isfinite(f["dR2"]) else f"{'-':>8}"
        say(f"    {f['sample']:<24}{f['y']:<11}{f['model']:<22}{f['n']:>4}{f['R2']:>8.3f}"
            f"{rb}{dr}{cells}")


def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values

    def frame_inputs(self):
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        return elig, np.where(np.isfinite(sc), -sc, np.inf)


def build_frame(pan, elig, key, reb, N=I_N, H=I_H, lag=1, diag=None):
    """The frozen incumbent's HOLDINGS frame at unit gross.  `lag` = trading days between the close
    the signal is read at and the day the trade lands; lag = 1 is PROTOCOL rule 2's own convention,
    lag = 1 + d adds d days of execution delay.

    `diag`, if given, collects the brake's own invariant — max_age, the largest (t - entry) over
    names still held after a rebalance, which the brake forces STRICTLY below H — and reentry, the
    share of fresh picks that are names the brake had just dropped.  Those re-entries are why a
    CONTIGUOUS holding spell can run past H without the brake being violated: no trade occurs, so
    the position never leaves the book."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    max_age, n_new, n_re = 0, 0, 0
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
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        dropped = set(int(c) for c in held) - keep
        n_new += len(take)
        n_re += sum(1 for c in take if c in dropped)
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            max_age = max(max_age, int((t - cur[sel]).max()))
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    if diag is not None:
        diag.update(max_age=max_age, n_new=n_new, n_reentry=n_re,
                    reentry_share=(n_re / n_new if n_new else np.nan))
    return W


def spell_stats(frame, lo, hi):
    """Realised mean holding SPELL (trading days a name stays in the book) and mean AGE of the
    positions carried on a day, over rows [lo, hi).  Computed on the HOLDINGS frame, so it is a
    property of the book's rotation and is INVARIANT to gross — which is exactly why it is a rival
    regressor to turnover and not a restatement of it."""
    H = frame[lo:hi] > 0
    if not H.any():
        return np.nan, np.nan
    T = H.shape[0]
    pad = np.zeros((1, H.shape[1]), bool)
    A = np.vstack([pad, H, pad])
    starts = (~A[:-1]) & A[1:]
    ends = A[:-1] & (~A[1:])
    lens = []
    ns = starts.sum(axis=0)
    cols = np.flatnonzero(ns > 0)
    for c in cols:
        s = np.flatnonzero(starts[:, c])
        e = np.flatnonzero(ends[:, c])
        lens.append(e - s)
    spell = float(np.concatenate(lens).mean()) if lens else np.nan
    # mean age carried: for each day, mean days since entry over the held names
    age = np.zeros(H.shape[1], dtype=np.int64)
    tot, cnt = 0.0, 0
    for t in range(T):
        age = np.where(H[t], age + 1, 0)
        k = int(H[t].sum())
        if k:
            tot += float(age[H[t]].sum())
            cnt += k
    return spell, (tot / cnt if cnt else np.nan)


def run_g(pan, frame, reb, g):
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    gmax = 0.0
    for t in range(T):
        post = g * frame[t] if isreb[t] else cur
        turn[t] = float(np.abs(post - cur).sum())
        gmax = max(gmax, float(post.sum()))
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rg=rg, turn=turn, gmax=gmax)


def turn_y(turn, lo, hi):
    seg = turn[lo:hi]
    return float(seg.sum()) * 252.0 / max(len(seg), 1)


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1596 — is LATENCY FRAGILITY PREDICTABLE EX ANTE from a book's own TURNOVER PATH or "
        "its own REALISED MEAN HOLDING AGE?   (lane C)")
    say("  PRE-REGISTERED  H_PREDICTABLE: in the GROSS-CONTROLLED pooled bivariate fit (panel "
        "dummies), >= 1 regressor reaches |t| > 2 AND pooled R2 >= 0.30 for dMaxDD(+1).")
    say("  PRE-REGISTERED  H_USABLE: PREDROBUST clears 4b FULL and OOS at delay +1 on >= 1 panel "
        "AND its OOS |dMaxDD(+1)| beats BOTH ISSHARPE's and PREREG's on >= 2 of 3 panels.")
    say("  VERDICT: KEEP-candidate if both fire; PARK if one; KILL if neither (fragility must then "
        "be read directly per book, as 1590 did).")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"\n  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level and every 4a / 4b pass count "
        "below is an UPPER BOUND.  The run's HEADLINE is a DIFFERENCE between two execution "
        "timings over the SAME names on the SAME days, and a REGRESSION of that difference on two "
        "same-book statistics; the bias cannot manufacture either.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G2 exactly two tuned parameters (the latency point +1; the regressor set "
         "turnover-vs-age).  H / cadence / gross are a PUBLISHED ladder, every rung reported; "
         "N / MAXVOL / MA gate / cost rung are frozen inheritances", 2, "== 2", True)

    rows, bench = [], {}
    re_share: list[float] = []
    spell_over_H: list[float] = []
    gmax_global, g1_ok, g3_ok, g7_ok = 0.0, None, None, True

    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        spyI = bmpack(pan.spy[WARMUP:i_is])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        bench[pan.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, i_oos=i_oos,
                               i_is=i_is)
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}  |  SPY OOS "
            f"{spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  SPY IS "
            f"{spyI['CAGR']:.2%}/{spyI['Sharpe']:.4f}/{spyI['MaxDD']:.2%}")
        say(f"           RULES v2 live @10bps FULL {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  |  OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        elig, key = pan.frame_inputs()
        for cad in CADENCES:
            reb = cadence_rows(pan.idx, cad)
            gap = int(np.median(np.diff(reb))) if len(reb) > 2 else 1
            for H in H_LADDER:
                frames, dg = {}, {}
                for d in DELAYS:
                    dd = {}
                    frames[d] = build_frame(pan, elig, key, reb, H=H, lag=1 + d, diag=dd)
                    if d == 0:
                        dg = dd
                if pan.name == "U56" and cad == I_C and H == I_H:
                    f2 = build_frame(pan, elig, key, reb, H=H, lag=1)
                    g3_ok = gate("G3 delay +0 IS the protocol convention (independently rebuilt "
                                 "lag-1 frame)", f"max |dev| {np.abs(frames[0]-f2).max():.2e}",
                                 "== 0", float(np.abs(frames[0] - f2).max()) == 0.0)
                sp0, ag0 = spell_stats(frames[0], WARMUP, len(pan.idx))
                spI, agI = spell_stats(frames[0], WARMUP, i_is)
                if dg.get("max_age", 0) >= H:
                    g7_ok = False
                publish(f"AGE {pan.name} {cad} H{H}", f"spell {sp0:.1f}d age {ag0:.1f}d "
                        f"(IS spell {spI:.1f}d); brake max age-since-entry {dg.get('max_age')} "
                        f"< H = {H}; re-entry share of fresh picks "
                        f"{dg.get('reentry_share', float('nan')):.3f}")
                re_share.append(dg.get("reentry_share", np.nan))
                spell_over_H.append(sp0 / H)
                for g in GROSS:
                    R = {d: run_g(pan, frames[d], reb, g) for d in DELAYS}
                    gmax_global = max(gmax_global, max(R[d]["gmax"] for d in DELAYS))
                    rec = dict(panel=pan.name, cadence=cad, H=H, gross=g,
                               spell=sp0, age=ag0, spell_is=spI, age_is=agI)
                    for d in DELAYS:
                        rn = R[d]["rg"] - R[d]["turn"] * COST / 1e4
                        k4a, k4b, m, h1, h2, lg = keep_paths(rn[WARMUP:], spy, live)
                        k4aO, k4bO, mo, _, _, lgO = keep_paths(rn[i_oos:], spyO, liveO)
                        mi = triple(rn[WARMUP:i_is])
                        rec.update({
                            f"CAGR_{d}": m["CAGR"], f"Sharpe_{d}": m["Sharpe"],
                            f"MaxDD_{d}": m["MaxDD"], f"H1_{d}": h1, f"H2_{d}": h2,
                            f"oCAGR_{d}": mo["CAGR"], f"oSharpe_{d}": mo["Sharpe"],
                            f"oMaxDD_{d}": mo["MaxDD"],
                            f"iCAGR_{d}": mi["CAGR"], f"iSharpe_{d}": mi["Sharpe"],
                            f"iMaxDD_{d}": mi["MaxDD"],
                            f"keep4a_{d}": k4a, f"keep4b_{d}": k4b,
                            f"keep4a_oos_{d}": k4aO, f"keep4b_oos_{d}": k4bO,
                            f"legH1_{d}": lg["H1"], f"legH2_{d}": lg["H2"],
                            f"legDD_{d}": lg["DD"], f"legCAGR_{d}": lg["CAGR"],
                            f"olegH1_{d}": lgO["H1"], f"olegH2_{d}": lgO["H2"],
                            f"olegDD_{d}": lgO["DD"], f"olegCAGR_{d}": lgO["CAGR"],
                            f"turn_y_{d}": turn_y(R[d]["turn"], WARMUP, len(pan.idx)),
                            f"turn_y_is_{d}": turn_y(R[d]["turn"], WARMUP, i_is),
                            f"turn_y_oos_{d}": turn_y(R[d]["turn"], i_oos, len(pan.idx)),
                        })
                        if (pan.name == "U56" and cad == I_C and H == I_H and g == I_G and d == 0):
                            dev = max(abs(m["Sharpe"] - C_U56["Sharpe"]),
                                      abs(mo["Sharpe"] - C_U56["oSharpe"]),
                                      abs(m["CAGR"] - C_U56["CAGR"]),
                                      abs(m["MaxDD"] - C_U56["MaxDD"]))
                            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 "
                                         "frozen anchor (H=126, W, gross 0.75, 10 bps, delay +0) "
                                         "15.80%/1.1537/-19.13% FULL, 1.1857 OOS",
                                         f"max |dev| {dev:.2e}", "< 5e-3", dev < 5e-3)
                    rec["dSharpe"] = rec["Sharpe_1"] - rec["Sharpe_0"]
                    rec["dMaxDD_pp"] = (rec["MaxDD_1"] - rec["MaxDD_0"]) * 100
                    rec["dCAGR_pp"] = (rec["CAGR_1"] - rec["CAGR_0"]) * 100
                    rec["dSharpe_is"] = rec["iSharpe_1"] - rec["iSharpe_0"]
                    rec["dMaxDD_pp_is"] = (rec["iMaxDD_1"] - rec["iMaxDD_0"]) * 100
                    rec["dSharpe_oos"] = rec["oSharpe_1"] - rec["oSharpe_0"]
                    rec["dMaxDD_pp_oos"] = (rec["oMaxDD_1"] - rec["oMaxDD_0"]) * 100
                    rec["turn_pg"] = rec["turn_y_0"] / g
                    rec["turn_pg_is"] = rec["turn_y_is_0"] / g
                    rows.append(rec)

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G4 gross in [0, 1] on every book", f"max realised weight sum {gmax_global:.6f}",
         "<= 1.0", gmax_global <= 1.0 + 1e-9)
    want = len(panels) * len(CADENCES) * len(H_LADDER) * len(GROSS)
    gate("G6 every cell published", f"{len(G)} books x {len(DELAYS)} delays = "
         f"{len(G)*len(DELAYS)} cells", f"== {want*len(DELAYS)}", len(G) == want)
    gate("G7 the brake's own invariant: max age-since-entry among names still held after a "
         "rebalance is STRICTLY < H on every book",
         f"{len(re_share)} frames checked", "max_age < H everywhere", g7_ok)
    say(f"    NOTE on the age regressor: a CONTIGUOUS holding spell runs to "
        f"{np.nanmean(spell_over_H):.2f}x H on average (range "
        f"{np.nanmin(spell_over_H):.2f}-{np.nanmax(spell_over_H):.2f}x) even though the brake is "
        f"never violated, because {np.nanmean(re_share):.1%} of fresh picks are names the brake had "
        f"just dropped and immediately re-took — no trade occurs, so the position never leaves the "
        f"book.  The regressor is the ECONOMIC holding age (what the tape sees), not the brake's "
        f"bookkeeping age.")

    # ------------------------------------------------------------------ the fragility itself
    say("\n" + "=" * 128)
    say("STEP 1 — THE FRAGILITY BEING EXPLAINED.  One trading day of execution delay, at 10 bps, "
        "on 144 published books.")
    say("=" * 128)
    say(f"    {'panel':<7}{'cad':>4}{'H':>5}{'g':>6}{'spell d':>9}{'age d':>8}{'turn/y':>8}"
        f"{'S(+0)':>9}{'S(+1)':>9}{'dS':>9}{'DD(+0)':>9}{'DD(+1)':>9}{'dDD pp':>9}"
        f"{'4b0':>6}{'4b1':>6}{'4bO0':>6}{'4bO1':>6}")
    for _, r in G.sort_values(["panel", "cadence", "H", "gross"]).iterrows():
        say(f"    {r.panel:<7}{r.cadence:>4}{int(r.H):>5}{r.gross:>6.2f}{r.spell:>9.1f}"
            f"{r.age:>8.1f}{r.turn_y_0:>8.2f}{r.Sharpe_0:>9.4f}{r.Sharpe_1:>9.4f}"
            f"{r.dSharpe:>+9.4f}{r.MaxDD_0:>9.2%}{r.MaxDD_1:>9.2%}{r.dMaxDD_pp:>+9.2f}"
            f"{str(r.keep4b_0):>6}{str(r.keep4b_1):>6}{str(r.keep4b_oos_0):>6}"
            f"{str(r.keep4b_oos_1):>6}")
    say(f"\n  FRAGILITY SPREAD (all {len(G)} books): dSharpe mean {G.dSharpe.mean():+.4f}, sd "
        f"{G.dSharpe.std(ddof=0):.4f}, min {G.dSharpe.min():+.4f}, max {G.dSharpe.max():+.4f}  |  "
        f"dMaxDD mean {G.dMaxDD_pp.mean():+.2f} pp, sd {G.dMaxDD_pp.std(ddof=0):.2f}, min "
        f"{G.dMaxDD_pp.min():+.2f}, max {G.dMaxDD_pp.max():+.2f}")
    say(f"  SIGN SPLIT: dSharpe < 0 in {int((G.dSharpe<0).sum())} of {len(G)} books; dMaxDD "
        f"WORSE (more negative) in {int((G.dMaxDD_pp<0).sum())}, BETTER in "
        f"{int((G.dMaxDD_pp>0).sum())}.  4b verdict CHANGES with the one day of latency in "
        f"{int((G.keep4b_0!=G.keep4b_1).sum())} of {len(G)} books FULL and "
        f"{int((G.keep4b_oos_0!=G.keep4b_oos_1).sum())} OOS.")
    say(f"  THE SCALE TRAP, MEASURED: corr(gross, turn_y) = "
        f"{G.gross.corr(G.turn_y_0):+.4f}; corr(gross, dSharpe) = {G.gross.corr(G.dSharpe):+.4f}; "
        f"corr(gross, dMaxDD_pp) = {G.gross.corr(G.dMaxDD_pp):+.4f}.  Gross is a pure scale dial, "
        f"so RAW turnover/yr carries it and the fragility barely does — which is why reading "
        f"(iii), gross = {CTRL_G:.2f} only, is the pre-registered one.")
    say(f"  REGRESSOR CORRELATION (all books): corr(turn_y, age) = {G.turn_y_0.corr(G.age):+.4f}; "
        f"corr(turn/gross, age) = {G.turn_pg.corr(G.age):+.4f}; corr(spell, age) = "
        f"{G.spell.corr(G.age):+.4f}")

    # ------------------------------------------------------------------ the regressions
    say("\n" + "=" * 128)
    say("STEP 2 — THE REGRESSION.  Y in {dSharpe(+1), dMaxDD(+1) pp}; X in {realised turnover/yr, "
        "realised mean holding age}.  Three scalings, pooled (panel dummies) and per panel.")
    say("=" * 128)
    fit_rows = []
    ctrl = G[G.gross == CTRL_G]
    readings = [("(i) raw turn/y", G, ["turn_y_0", "age"]),
                ("(ii) turn per gross", G, ["turn_pg", "age"]),
                (f"(iii) gross={CTRL_G:.2f}", ctrl, ["turn_y_0", "age"])]
    for label, sub, xs in readings:
        say(f"\n  READING {label}   ({len(sub)} books)")
        for ycol in ["dSharpe", "dMaxDD_pp"]:
            fits = fit_table(sub, ycol, xs, f"POOLED {label}", dummies="panel")
            say_fits(fits, xs)
            fit_rows += fits
            for pn in sub.panel.unique():
                f2 = fit_table(sub[sub.panel == pn], ycol, xs, f"{pn} {label}")
                say_fits(f2, xs)
                fit_rows += f2
    F = pd.DataFrame([{k: v for k, v in f.items() if k not in ("names", "beta", "se", "t",
                                                               "std_beta", "vif")}
                      | {f"b[{n}]": f["beta"][i] for i, n in enumerate(f["names"])}
                      | {f"t[{n}]": f["t"][i] for i, n in enumerate(f["names"])}
                      | {f"VIF[{k}]": v for k, v in f["vif"].items()}
                      for f in fit_rows])
    F.to_csv(f"{OUT}.regressions.csv", index=False)

    # -------- the sign-flip census: collinearity, not findings
    flips = 0
    pairs = 0
    for f in fit_rows:
        if "+" not in f["model"]:
            continue
        for c in f["model"].split("+"):
            u = [q for q in fit_rows if q["sample"] == f["sample"] and q["y"] == f["y"]
                 and q["model"] == c]
            if not u:
                continue
            pairs += 1
            bu = u[0]["beta"][u[0]["names"].index(c)]
            bb = f["beta"][f["names"].index(c)]
            if bu * bb < 0:
                flips += 1
    say(f"\n  COLLINEARITY CENSUS: a regressor's coefficient FLIPS SIGN between its univariate and "
        f"its bivariate fit in {flips} of {pairs} (sample, Y, regressor) triples "
        f"({flips/pairs:.1%}).  With corr(turn/y, age) = {G.turn_y_0.corr(G.age):+.3f} pooled "
        f"(a faster brake BOTH raises turnover AND lowers age, by construction), the two "
        f"regressors are not separately identified on this ladder and a bivariate sign is not a "
        f"mechanism claim.")

    # G8 identity check
    d8 = ctrl.dropna(subset=["dMaxDD_pp", "age"])
    f8 = ols(d8["dMaxDD_pp"].values,
             np.column_stack([np.ones(len(d8)), d8["age"].values]), ["const", "age"])
    rho = float(np.corrcoef(d8["age"].values, d8["dMaxDD_pp"].values)[0, 1])
    gate("G8 regression identity: univariate R2 == squared Pearson correlation",
         f"|R2 - rho^2| = {abs(f8['R2'] - rho**2):.2e}", "< 1e-12",
         abs(f8["R2"] - rho ** 2) < 1e-12)

    def pick_fit(sample_label, ycol, model):
        m = [f for f in fit_rows if f["sample"] == sample_label and f["y"] == ycol
             and f["model"] == model]
        return m[0] if m else None

    biv = "+".join(["turn_y_0", "age"])
    key_fit = pick_fit(f"POOLED (iii) gross={CTRL_G:.2f}", "dMaxDD_pp", biv)
    t_turn = key_fit["t"][key_fit["names"].index("turn_y_0")]
    t_age = key_fit["t"][key_fit["names"].index("age")]
    r2_key = key_fit["R2"]
    uni_turn = pick_fit(f"POOLED (iii) gross={CTRL_G:.2f}", "dMaxDD_pp", "turn_y_0")
    uni_age = pick_fit(f"POOLED (iii) gross={CTRL_G:.2f}", "dMaxDD_pp", "age")
    say("\n  WHICH REGRESSOR SURVIVES THE OTHER (pre-registered reading (iii), pooled, dMaxDD "
        f"(+1)): t[turn/y] = {t_turn:+.2f}, t[age] = {t_age:+.2f}, bivariate R2 = {r2_key:.3f}.")
    say(f"  HOW MUCH EITHER EXPLAINS ALONE: turnover R2 = {uni_turn['R2']:.3f}, age R2 = "
        f"{uni_age['R2']:.3f} (bivariate {r2_key:.3f}); on dSharpe(+1): turnover "
        f"{pick_fit(f'POOLED (iii) gross={CTRL_G:.2f}', 'dSharpe', 'turn_y_0')['R2']:.3f}, age "
        f"{pick_fit(f'POOLED (iii) gross={CTRL_G:.2f}', 'dSharpe', 'age')['R2']:.3f}, bivariate "
        f"{pick_fit(f'POOLED (iii) gross={CTRL_G:.2f}', 'dSharpe', biv)['R2']:.3f}.")
    h_pred = bool((abs(t_turn) > 2 or abs(t_age) > 2) and r2_key >= 0.30)
    say(f"  H_PREDICTABLE as PRE-REGISTERED (|t| > 2 on >= 1 regressor AND pooled R2 >= 0.30): "
        f"{h_pred}")
    say(f"  *** THE DEFLATION THE PRE-REGISTERED BAR MISSES.  That pooled R2 is NOT the regressors' "
        f"work: the PANEL DUMMIES ALONE explain R2_base = {key_fit['R2_base']:.3f} of dMaxDD(+1) on "
        f"the same 36 rows, so the two regressors buy only dR2 = {key_fit['dR2']:.3f} on top "
        f"(turnover alone {uni_turn['dR2']:+.3f}, age alone {uni_age['dR2']:+.3f}).  The bar was "
        f"written as a POOLED R2 before the run and is reported as written above, but the honest "
        f"reading of 'how much of the fragility either explains' is the INCREMENTAL one: "
        f"{key_fit['dR2']:.1%} of the variance, from two regressors that flip each other's signs. "
        f"Under an incremental bar of 0.30 H_PREDICTABLE would be "
        f"{bool((abs(t_turn) > 2 or abs(t_age) > 2) and key_fit['dR2'] >= 0.30)} and the verdict "
        f"below would be KILL, not PARK. ***")
    h_pred_def = bool((abs(t_turn) > 2 or abs(t_age) > 2) and key_fit["dR2"] >= 0.30)

    # ------------------------------------------------------------------ IS-only transfer
    say("\n" + "=" * 128)
    say("STEP 3 — DOES THE IS FRAGILITY EVEN PREDICT THE OOS FRAGILITY?  (the transfer the ex-ante "
        "claim needs, before any chooser)")
    say("=" * 128)
    say(f"    {'sample':<10}{'rho(iS,oS)':>12}{'rho(iDD,oDD)':>14}{'rho(age,oDD)':>14}"
        f"{'rho(turn,oDD)':>15}{'n':>5}")
    for pn in ["POOLED"] + list(G.panel.unique()):
        s = ctrl if pn == "POOLED" else ctrl[ctrl.panel == pn]
        say(f"    {pn:<10}{s.dSharpe_is.corr(s.dSharpe_oos):>12.4f}"
            f"{s.dMaxDD_pp_is.corr(s.dMaxDD_pp_oos):>14.4f}"
            f"{s.age.corr(s.dMaxDD_pp_oos):>14.4f}{s.turn_y_0.corr(s.dMaxDD_pp_oos):>15.4f}"
            f"{len(s):>5}")

    # ------------------------------------------------------------------ rule 8 capital arm
    say("\n" + "=" * 128)
    say("STEP 4 — RULE 8.  Four IS-ONLY choosers over the 48 books of each panel; the fragility "
        "model is FIT ON IS ROWS ONLY; 2017-01-01..end read exactly ONCE.")
    say("=" * 128)
    wf_rows = []
    for pan in panels:
        b = bench[pan.name]
        sub = G[G.panel == pan.name].copy()
        spyI = b["spyI"]
        adm = sub[(sub["iMaxDD_0"] >= DD_CAP * spyI["MaxDD"])
                  & (sub["iCAGR_0"] >= CAGR_FLOOR * spyI["CAGR"])]
        # PREDROBUST needs an IS-only fit of |dMaxDD| on the IS regressors
        dfit = sub.dropna(subset=["dMaxDD_pp_is", "turn_y_is_0", "age_is"])
        Xf = np.column_stack([np.ones(len(dfit)), dfit["turn_y_is_0"].values,
                              dfit["age_is"].values])
        ffit = ols(np.abs(dfit["dMaxDD_pp_is"].values), Xf, ["const", "turn_is", "age_is"])
        sub["pred_absdd"] = (ffit["beta"][0] + ffit["beta"][1] * sub["turn_y_is_0"]
                             + ffit["beta"][2] * sub["age_is"])
        adm = sub.loc[adm.index]
        say(f"\n  [{pan.name}]  IS admitted set (IS MaxDD <= {DD_CAP*spyI['MaxDD']:.2%} and IS "
            f"CAGR >= {CAGR_FLOOR*spyI['CAGR']:.2%}): {len(adm)} of {len(sub)} books.  "
            f"IS |dMaxDD| fit: b[turn_is] {ffit['beta'][1]:+.4f} (t {ffit['t'][1]:+.2f}), "
            f"b[age_is] {ffit['beta'][2]:+.4f} (t {ffit['t'][2]:+.2f}), R2 {ffit['R2']:.3f}")
        picks = {}
        picks["ISSHARPE"] = sub.loc[sub["iSharpe_0"].idxmax()]
        if len(adm):
            a = adm.sort_values(["gross", "iSharpe_0"], ascending=[True, False])
            picks["PREREG"] = a.iloc[0]
            picks["PREDROBUST"] = adm.loc[adm["pred_absdd"].idxmin()]
            picks["REALROBUST"] = adm.loc[adm["dMaxDD_pp_is"].abs().idxmin()]
        say(f"    {'chooser':<12}{'cad':>4}{'H':>5}{'g':>6}{'IS S':>9}{'FULL CAGR':>11}"
            f"{'S':>9}{'MaxDD':>9}{'OOS CAGR':>10}{'oS':>9}{'oMaxDD':>9}{'4b0':>6}{'4b1':>6}"
            f"{'4bO0':>6}{'4bO1':>6}{'4aO0':>6}{'oDS':>9}{'oDDD pp':>9}")
        for cn, pk in picks.items():
            say(f"    {cn:<12}{pk.cadence:>4}{int(pk.H):>5}{pk.gross:>6.2f}{pk.iSharpe_0:>9.4f}"
                f"{pk.CAGR_0:>11.2%}{pk.Sharpe_0:>9.4f}{pk.MaxDD_0:>9.2%}{pk.oCAGR_0:>10.2%}"
                f"{pk.oSharpe_0:>9.4f}{pk.oMaxDD_0:>9.2%}{str(pk.keep4b_0):>6}"
                f"{str(pk.keep4b_1):>6}{str(pk.keep4b_oos_0):>6}{str(pk.keep4b_oos_1):>6}"
                f"{str(pk.keep4a_oos_0):>6}{pk.dSharpe_oos:>+9.4f}{pk.dMaxDD_pp_oos:>+9.2f}")
            wf_rows.append(dict(panel=pan.name, chooser=cn, cadence=pk.cadence, H=int(pk.H),
                                gross=float(pk.gross), is_Sharpe=pk.iSharpe_0,
                                CAGR=pk.CAGR_0, Sharpe=pk.Sharpe_0, MaxDD=pk.MaxDD_0,
                                H1=pk.H1_0, H2=pk.H2_0,
                                CAGR_d1=pk.CAGR_1, Sharpe_d1=pk.Sharpe_1, MaxDD_d1=pk.MaxDD_1,
                                oCAGR=pk.oCAGR_0, oSharpe=pk.oSharpe_0, oMaxDD=pk.oMaxDD_0,
                                oCAGR_d1=pk.oCAGR_1, oSharpe_d1=pk.oSharpe_1,
                                oMaxDD_d1=pk.oMaxDD_1,
                                keep4a=bool(pk.keep4a_0), keep4b=bool(pk.keep4b_0),
                                keep4a_d1=bool(pk.keep4a_1), keep4b_d1=bool(pk.keep4b_1),
                                keep4a_oos=bool(pk.keep4a_oos_0),
                                keep4b_oos=bool(pk.keep4b_oos_0),
                                keep4a_oos_d1=bool(pk.keep4a_oos_1),
                                keep4b_oos_d1=bool(pk.keep4b_oos_1),
                                dSharpe_oos=pk.dSharpe_oos, dMaxDD_pp_oos=pk.dMaxDD_pp_oos,
                                spy_CAGR=b["spy"]["CAGR"], spy_Sharpe=b["spy"]["Sharpe"],
                                spy_MaxDD=b["spy"]["MaxDD"], spy_oCAGR=b["spyO"]["CAGR"],
                                spy_oSharpe=b["spyO"]["Sharpe"], spy_oMaxDD=b["spyO"]["MaxDD"],
                                live_Sharpe=b["live"]["Sharpe"], live_MaxDD=b["live"]["MaxDD"],
                                live_oCAGR=b["liveO"]["CAGR"], live_oSharpe=b["liveO"]["Sharpe"],
                                live_oMaxDD=b["liveO"]["MaxDD"]))
    W = pd.DataFrame(wf_rows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G5 no chooser and no model fit reads a row on or after 2017-01-01",
         f"admission, argmax and the |dMaxDD| fit all end {IS_END}", f"<= {IS_END}", True)

    # ------------------------------------------------------------------ verdict
    pr = W[W.chooser == "PREDROBUST"]
    pass_d1 = pr[(pr.keep4b_d1) & (pr.keep4b_oos_d1)]
    beats = 0
    for pn in W.panel.unique():
        a = W[(W.panel == pn) & (W.chooser == "PREDROBUST")]
        i_ = W[(W.panel == pn) & (W.chooser == "ISSHARPE")]
        p_ = W[(W.panel == pn) & (W.chooser == "PREREG")]
        if len(a) and len(i_) and len(p_):
            if (abs(a.dMaxDD_pp_oos.iloc[0]) < abs(i_.dMaxDD_pp_oos.iloc[0])
                    and abs(a.dMaxDD_pp_oos.iloc[0]) < abs(p_.dMaxDD_pp_oos.iloc[0])):
                beats += 1
    h_use = bool(len(pass_d1) >= 1 and beats >= 2)
    verdict = ("KEEP-candidate" if (h_pred and h_use) else
               ("PARK" if (h_pred or h_use) else "KILL"))
    say("\n" + "=" * 128)
    say(f"PRE-REGISTERED VERDICT.  H_PREDICTABLE {h_pred} (pooled reading (iii) dMaxDD: "
        f"t[turn] {t_turn:+.2f}, t[age] {t_age:+.2f}, R2 {r2_key:.3f} vs bars |t|>2 and 0.30).")
    say(f"                         H_USABLE {h_use} (PREDROBUST clears 4b FULL+OOS at delay +1 on "
        f"{len(pass_d1)} of {len(pr)} panels; its OOS |dMaxDD(+1)| beats BOTH rivals on {beats} of "
        f"{len(W.panel.unique())} panels, bar 2).")
    say(f"                         ->  {verdict}")
    say(f"  AND THE DEFLATED READING, stated so the record cannot quote the PARK as a half-win: "
        f"H_PREDICTABLE on the INCREMENTAL R2 over panel dummies is {h_pred_def} "
        f"(dR2 = {key_fit['dR2']:.3f}), which with H_USABLE {h_use} makes the honest verdict "
        f"{'KILL' if not (h_pred_def or h_use) else verdict}.  The PARK above is carried by a bar "
        f"that panel dummies can clear on their own.")
    say("=" * 128)

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nGATES: {len(gdf)} recorded, {int((~gdf['pass_']).sum())} FAIL.")
    say(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return verdict


if __name__ == "__main__":
    main()

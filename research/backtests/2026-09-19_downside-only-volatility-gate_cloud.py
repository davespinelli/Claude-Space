#!/usr/bin/env python3
"""
Idea 1511 (lane cloud, 2026-09-19) — does a DOWNSIDE-ONLY VOLATILITY GATE beat the incumbent's
TWO-SIDED vol20?

THE PREMISE.  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly
Fri-decide / Mon-trade, 10 bps, t+1) screens eligibility on `vol20 < 0.60`, a TWO-SIDED realised
volatility: it throws out a name whose last 20 days were violently UP exactly as hard as one whose
last 20 days were violently DOWN.  On a long-only momentum book that is a strange thing to want.
The record's standing finding is that MAXIMUM DRAWDOWN is the binding 4b leg on every family (the
U56 anchor passes at -19.13% against a -20.23% cap, a margin of 1.10 pp), so if punishing upside
dispersion is costing anything it should show up THERE.  This run replaces the gate statistic with
a DOWNSIDE semi-deviation AT A MATCHED PASS RATE and reads the drawdown leg.

THE FOUR GATE STATISTICS (the treatment axis — enumerated, not tuned, and reported at every value).
All annualised over a window w of daily returns r with mean mu, all computed on the REAL tape and
read by the frame at t-1:

  VOL    std(r) * sqrt(252)                            THE INCUMBENT'S OWN STATISTIC (control)
  SEMI0  sqrt(mean(min(r, 0)^2)) * sqrt(252)           the literal downside semi-deviation
  SEMIM  sqrt(mean(min(r - mu, 0)^2)) * sqrt(252)      semi-deviation BELOW THE MEAN
  UPM    sqrt(mean(max(r - mu, 0)^2)) * sqrt(252)      semi-deviation ABOVE THE MEAN — THE PLACEBO

SEMIM and UPM are an EXACT decomposition of the incumbent's own statistic: SEMIM^2 + UPM^2 =
VOL^2 * (w-1)/w pointwise (gate G10, asserted to 1e-12).  The (w-1)/w factor is not a fudge: VOL is
pandas' rolling std, which uses ddof = 1, and the incumbent's live screen uses exactly that, so VOL
keeps it (it is why gate G2 is bit-identical) while the two semi-deviations are population second
moments about the same mean.  That makes UPM the sharpest possible control: if screening
on UPSIDE dispersion helps as much as screening on downside, the word "downside" in this idea is
doing no work and the finding is about screening on ANY dispersion.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DIAL 1  WINDOW w        {10, 20, 40, 60}        how many days the gate statistic reads.
  DIAL 2  TARGET PASS RATE q  {0.70, 0.80, 0.90, p*, 1.00}

          where p* is the incumbent's OWN realised pass rate, measured as the share of
          priced name-days on the IN-SAMPLE window (warm-up .. 2016-12-31) with vol20 < 0.60,
          and q = 1.00 is the NO-GATE rung (the screen removed entirely).  A ladder relative to
          p* was tried first and abandoned when p* turned out to sit near the top of its range
          (see finding (0)): offsets above p* collapse onto 1.00.  The fixed ladder brackets p*
          from below, which is the only direction in which a dispersion screen can do work.
          MATCHING THE PASS RATE IS THE WHOLE POINT: four statistics on four different scales
          cannot be compared at a common numeric threshold, so each cell's threshold is the
          q-quantile of ITS OWN statistic over the SAME in-sample priced cells.  The threshold is
          therefore fitted on IS rows ONLY and applied unchanged to 2017-2026 (gate G5).
          By construction the VOL / w = 20 / q = p* cell recovers a threshold of exactly 0.60 and
          IS the frozen incumbent (gate G2).

4 statistics x 4 windows x 5 pass rates = 80 cells per panel, 240 in all on U56 / B136 / SMALL,
EVERY ONE PUBLISHED in .grid.csv.

PRE-REGISTERED BARS (written before any number was read).  The downside gate is MATERIAL iff, at
the MATCHED pass rate q = p*:
  (B1) mean dMaxDD of SEMI0 against the VOL control at the same window is >= +1.0 pp (less negative
       = shallower drawdown) on U56 AND on B136;
  (B2) at least one matched-pass-rate cell reaches |t| > 2 against its VOL control on dMaxDD or
       dSharpe (paired circular-block bootstrap, 400 reps x 63-row blocks, seed 20260919, identical
       block starts); and
  (B3) the rule-8-selected downside cell beats the frozen incumbent on OOS Sharpe.
All three are needed for a KEEP-candidate.  Anything less is KILL or PARK, and the UPM placebo
matching the downside statistic's result is a KILL on its own terms.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: BOTH dials AND
every threshold fitted on warm-up..2016-12-31, 2017-2026 read ONCE); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed 2026-09-04 U56 anchor
(15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 the VOL / w=20 / q=p* cell
recovers threshold 0.60 and is BIT-IDENTICAL to the frozen incumbent.  G3 all 240 cells published.
G4 exactly two tuned parameters.  G5 no threshold and no chooser reads a row on or after
2017-01-01.  G6 no leverage.  G7 every gate statistic is NON-ANTICIPATING (truncated-tape replay is
bit-identical).  G8 the pass rate really is matched (realised IS pass share within 1 pp of q at
every cell).  G9 deterministic recompute of one cell per panel.  G10 SEMIM^2 + UPM^2 == VOL^2 * (w-1)/w
pointwise.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_downside-only-volatility-gate_cloud.py
"""
from __future__ import annotations

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

DATE = "2026-09-19"
SLUG = "downside-only-volatility-gate"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75
COST, CADENCE = 10.0, "W"
STATS = ["VOL", "SEMI0", "SEMIM", "UPM"]
WINS = [10, 20, 40, 60]                          # DIAL 1
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
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


# ---------------------------------------------------------------------------------------------
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
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def _boot_idx(n, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def paired_block(a, b):
    """Paired circular-block bootstrap SE for BOTH dSharpe and dMaxDD, identical block starts."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    idx = _boot_idx(n)
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    def dd(X):
        e = np.cumprod(1 + X, axis=1)
        return (e / np.maximum.accumulate(e, axis=1) - 1).min(axis=1)

    ds, dd_ = sh(A) - sh(B), dd(A) - dd(B)
    o_s, o_d = float(sharpe(a) - sharpe(b)), float(mdd(a) - mdd(b))
    se_s, se_d = float(np.nanstd(ds, ddof=1)), float(np.nanstd(dd_, ddof=1))
    return (o_s, se_s, (o_s / se_s if se_s > 0 else np.nan),
            o_d, se_d, (o_d / se_d if se_d > 0 else np.nan))


# ---------------------------------------------------------------------------------------------
def _semi_about_mean(R: np.ndarray, MU: np.ndarray, w: int, side: str):
    """(1/w) * sum_{j<w} f(r_{t-j} - mu_t)^2 where mu_t is the ONE window mean, f = min(.,0) or
    max(.,0).  Rolling a per-day deviation would use a DIFFERENT mean for each day in the window
    and would not decompose (gate G10); this does."""
    T, K = R.shape
    acc = np.zeros((T, K))
    for j in range(w):
        x = np.full((T, K), np.nan)
        x[j:] = R[:T - j] - MU[j:]
        d = np.minimum(x, 0.0) if side == "dn" else np.maximum(x, 0.0)
        acc += d * d
    return acc / w


def gate_stat(q: pd.DataFrame, kind: str, w: int):
    """The four annualised dispersion statistics.  All read days <= t only."""
    r = q.pct_change()
    s = np.sqrt(252.0)
    if kind == "VOL":
        return (r.rolling(w).std() * s).values          # ddof = 1: the INCUMBENT'S own statistic
    if kind == "SEMI0":
        d = r.clip(upper=0.0)
        return (np.sqrt((d ** 2).rolling(w).mean()) * s).values
    if kind in ("SEMIM", "UPM"):
        R = r.values
        MU = r.rolling(w).mean().values
        side = "dn" if kind == "SEMIM" else "up"
        return np.sqrt(_semi_about_mean(R, MU, w, side)) * s
    raise ValueError(kind)


def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


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
        self.above = (q > q.rolling(200).mean()).values
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc = self.comp * (0.5 + 0.5 * self.above.astype(float))
        self.key = np.where(np.isfinite(sc), -sc, np.inf)


def build_frame(pan, elig, N=I_N, H=I_H, lag=1, nrows=None):
    T = pan.rets.shape[0] if nrows is None else nrows
    M = pan.rets.shape[1]
    K = len(pan.iinv)
    W = np.zeros((T, M))
    holds = []
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb[pan.reb < T]
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
            k = pan.key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
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
        holds.append(frozenset(int(x) for x in sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, holds


def run_book(pan, frame, C, Cp, g, nrows=None):
    rets = pan.rets
    T = rets.shape[0] if nrows is None else nrows
    M = rets.shape[1]
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb[pan.reb < T]
    ends = np.append(reb[1:], T)
    wsum_max = 0.0
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, wsum_max


def jaccard_vs(holds, base_holds, first_i):
    j, n = [], 0
    for i, (h, b) in enumerate(zip(holds, base_holds)):
        if i < first_i:
            continue
        n += 1
        u = len(h | b)
        j.append(len(h & b) / u if u else 1.0)
    return float(np.mean(j)) if n else np.nan


# ---------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1511 (lane cloud, 2026-09-19) — does a DOWNSIDE-ONLY VOLATILITY GATE beat the "
        "incumbent's TWO-SIDED vol20?")
    say("4 gate statistics {VOL control, SEMI0, SEMIM, UPM placebo} x DIAL 1 window {10,20,40,60} "
        "x DIAL 2 target pass rate (5 rungs around the incumbent's own p*).")
    say("Thresholds are the q-quantile of each statistic over IN-SAMPLE priced cells ONLY, applied "
        "unchanged to 2017-2026.")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "The contrast this run reads is between FOUR GATE STATISTICS over the SAME names on the "
        "SAME days at a MATCHED PASS RATE, which the bias cannot manufacture — though note it runs "
        "AGAINST a downside screen: a survivor's drawdown was, by selection, one it recovered "
        "from.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned parameters (window w, target pass rate q)", 2, "== 2", True)

    grid, wf_rows, decomp = [], [], 0.0
    wsum_global, g2_dev, g2_thr, g7_dev, g9_dev = 0.0, None, None, 0.0, 0.0
    g8_worst, pstars = 0.0, {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        first_reb = int(np.searchsorted(pan.reb, WARMUP))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
        pr = pan.priced[:, pan.iinv]
        ISW = slice(WARMUP, i_is)                       # the ONLY rows a threshold may read

        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        # ---- the four statistics and the incumbent's OWN pass rate p* -----------------------
        S = {(k, w): gate_stat(pan.q, k, w) for k in STATS for w in WINS}
        v20 = S[("VOL", 20)]
        m_is = np.zeros(pan.priced[:, pan.iinv].shape, bool)
        m_is[ISW] = True
        m_is &= pr & np.isfinite(v20)
        pstar = float((v20[m_is] < MAXVOL).mean())
        pstars[pan.name] = pstar
        QS = sorted({0.70, 0.80, 0.90, round(pstar, 6), 1.00})
        assert len(QS) == 5, f"DIAL 2 rungs collapsed on {pan.name}: {QS}"
        QMATCH = round(pstar, 6)
        say(f"           INCUMBENT'S OWN PASS RATE p* (IS priced name-days with vol20 < 0.60) = "
            f"{pstar:.4f};  DIAL 2 rungs {['%.4f' % x for x in QS]}")
        publish(f"p* {pan.name}", f"{pstar:.6f}")

        # G10: SEMIM^2 + UPM^2 == VOL^2 pointwise
        for w in WINS:
            # VOL is pandas' rolling std, which uses ddof = 1 (this is what the INCUMBENT uses,
            # so VOL must keep it -- gate G2 is bit-identical only because of that).  The two
            # semi-deviations are population (ddof = 0) second moments about the same mean, so the
            # exact identity carries a (w-1)/w factor.  Asserting it with the factor is the honest
            # form; asserting it without would be asserting that pandas' default is 0.
            a = S[("SEMIM", w)] ** 2 + S[("UPM", w)] ** 2
            b = S[("VOL", w)] ** 2 * (w - 1.0) / w
            f = np.isfinite(a) & np.isfinite(b)
            decomp = max(decomp, float(np.max(np.abs(a[f] - b[f]))) if f.any() else 0.0)

        # ---- the frozen incumbent -----------------------------------------------------------
        elig0 = pan.above & (np.nan_to_num(v20, nan=1e9) < MAXVOL)
        frame0, holds0 = build_frame(pan, elig0)
        g0, t0_, ws = run_book(pan, frame0, C, Cp, I_G)
        wsum_global = max(wsum_global, ws)
        anchor = g0 - t0_ * COST / 1e4
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        say(f"           FROZEN INCUMBENT CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} MaxDD "
            f"{am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                 f"max |dev| {d:.2e} (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/{am['MaxDD']:.4f}; "
                 f"OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- the 80-cell grid -----------------------------------------------------------------
        for k in STATS:
            for w in WINS:
                X = S[(k, w)]
                mis = np.zeros(X.shape, bool)
                mis[ISW] = True
                mis &= pr & np.isfinite(X)
                pool = X[mis]
                for q in QS:
                    thr = float(np.quantile(pool, q)) if q < 1.0 else np.inf
                    realised = float((pool < thr).mean()) if np.isfinite(thr) else 1.0
                    g8_worst = max(g8_worst, abs(realised - q))
                    elig = pan.above & (np.nan_to_num(X, nan=1e9) < thr)
                    frame, holds = build_frame(pan, elig)
                    gg, tu, ws = run_book(pan, frame, C, Cp, I_G)
                    wsum_global = max(wsum_global, ws)
                    rr = gg - tu * COST / 1e4
                    if k == "VOL" and w == 20 and q == QMATCH:
                        g2_dev = float(np.max(np.abs(rr - anchor)))
                        g2_thr = thr
                    jac = jaccard_vs(holds, holds0, first_reb)
                    k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
                    ds, se_s, t_s, dd_, se_d, t_d = paired_block(rr[WARMUP:], anchor[WARMUP:])
                    dsO, _, t_sO, ddO, _, t_dO = paired_block(rr[i_oos:], anchor[i_oos:])
                    ty = float(np.sum(tu[WARMUP:]) * 252.0 / (T - WARMUP))
                    grid.append(dict(
                        panel=pan.name, stat=k, win=w, q=q, threshold=thr,
                        realised_pass=realised, matched=bool(q == QMATCH),
                        jaccard=jac,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        turnover_yr=ty, cost_bp_yr=ty * COST,
                        dCAGR_pp=(m["CAGR"] - am["CAGR"]) * 100.0,
                        dSharpe=ds, dSharpe_se=se_s, dSharpe_t=t_s,
                        dMaxDD_pp=dd_ * 100.0, dMaxDD_se_pp=se_d * 100.0, dMaxDD_t=t_d,
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        odSharpe=dsO, odSharpe_t=t_sO, odMaxDD_pp=ddO * 100.0, odMaxDD_t=t_dO,
                        odCAGR_pp=(mo["CAGR"] - ao["CAGR"]) * 100.0,
                        keep4a=k4a, keep4b=k4b, keep4a_OOS=k4aO, keep4b_OOS=k4bO,
                        leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                        leg_CAGR=legs["CAGR"], legO_H1=legsO["H1"], legO_H2=legsO["H2"],
                        legO_DD=legsO["DD"], legO_CAGR=legsO["CAGR"],
                        is_Sharpe=sharpe(rr[WARMUP:i_is]),
                        anchor_MaxDD=am["MaxDD"], anchor_Sharpe=am["Sharpe"],
                        anchor_oSharpe=ao["Sharpe"], anchor_oMaxDD=ao["MaxDD"],
                        spy_MaxDD=spy["MaxDD"], name=f"{k}/w{w}/q{q:.4f}"))
            say(f"    [{pan.name}] {k} done ({len(grid)} cells, {time.time()-t0:.0f}s)")

        # ---- G7 causality: truncated-tape replay of every statistic --------------------------
        qt = pan.q.iloc[:i_oos]
        for k in STATS:
            a = gate_stat(pan.q, k, 20)[:i_oos]
            b = gate_stat(qt, k, 20)
            f = np.isfinite(a) & np.isfinite(b)
            g7_dev = max(g7_dev, float(np.max(np.abs(a[f] - b[f]))) if f.any() else 0.0)

        # ---- G9 deterministic recompute -------------------------------------------------------
        kk, ww, qq = "SEMI0", 40, QMATCH
        X = S[(kk, ww)]
        mis = np.zeros(X.shape, bool)
        mis[ISW] = True
        mis &= pr & np.isfinite(X)
        thr = float(np.quantile(X[mis], qq))
        f2, _ = build_frame(pan, pan.above & (np.nan_to_num(X, nan=1e9) < thr))
        gg2, tu2, _ = run_book(pan, f2, C, Cp, I_G)
        ref = [x for x in grid if x["panel"] == pan.name and x["stat"] == kk
               and x["win"] == ww and abs(x["q"] - qq) < 1e-12][0]
        g9_dev = max(g9_dev, abs(sharpe((gg2 - tu2 * COST / 1e4)[WARMUP:]) - ref["Sharpe"]))

        # ---- rule 8: BOTH dials fitted on IS only ----------------------------------------------
        cand = [x for x in grid if x["panel"] == pan.name]
        pools = [("ARGMAX-IS (all 80 cells)", cand),
                 ("ARGMAX-IS (downside statistics only: SEMI0 / SEMIM)",
                  [x for x in cand if x["stat"] in ("SEMI0", "SEMIM")]),
                 ("ARGMAX-IS (VOL control only)", [x for x in cand if x["stat"] == "VOL"]),
                 ("ARGMAX-IS (UPM placebo only)", [x for x in cand if x["stat"] == "UPM"]),
                 ("DO NOTHING (frozen incumbent)",
                  [x for x in cand if x["stat"] == "VOL" and x["win"] == 20 and x["matched"]])]
        for tag, pool in pools:
            pick = max(pool, key=lambda x: (-1e9 if not np.isfinite(x["is_Sharpe"])
                                            else x["is_Sharpe"]))
            wf_rows.append(dict(
                panel=pan.name, chooser=tag, cell=pick["name"], stat=pick["stat"],
                win=pick["win"], q=pick["q"], threshold=pick["threshold"],
                IS_Sharpe=pick["is_Sharpe"], OOS_CAGR=pick["oCAGR"], OOS_Sharpe=pick["oSharpe"],
                OOS_MaxDD=pick["oMaxDD"],
                anchor_OOS_CAGR=ao["CAGR"], anchor_OOS_Sharpe=ao["Sharpe"],
                anchor_OOS_MaxDD=ao["MaxDD"],
                spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                spy_OOS_MaxDD=spyO["MaxDD"], live_OOS_CAGR=liveO["CAGR"],
                live_OOS_Sharpe=liveO["Sharpe"], live_OOS_MaxDD=liveO["MaxDD"],
                odSharpe=pick["odSharpe"], odSharpe_t=pick["odSharpe_t"],
                odMaxDD_pp=pick["odMaxDD_pp"], odMaxDD_t=pick["odMaxDD_t"],
                keep4a_OOS=pick["keep4a_OOS"], keep4b_OOS=pick["keep4b_OOS"]))

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    gate("G3 all 240 cells published (3 panels x 4 statistics x 4 windows x 5 pass rates)",
         len(G), "== 240", len(G) == 240)
    gate("G2 the VOL / w=20 / q=p* cell recovers threshold 0.60 and is BIT-IDENTICAL to the frozen "
         "incumbent", f"threshold {g2_thr:.6f}, max |dret| {g2_dev:.3e}",
         "|thr - 0.60| < 5e-3 and |dret| < 1e-12",
         (g2_thr is not None and abs(g2_thr - MAXVOL) < 5e-3 and g2_dev < 1e-12))
    gate("G6 no leverage: max realised weight sum", f"{wsum_global:.6f}", "<= 1.0 + 1e-9",
         wsum_global <= 1.0 + 1e-9)
    gate("G7 every gate statistic is NON-ANTICIPATING (truncated-tape replay, all 4 statistics)",
         f"max |dstat| {g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G8 the pass rate really is matched (worst |realised IS pass share - q| over 240 cells)",
         f"{g8_worst:.5f}", "< 0.01", g8_worst < 0.01)
    gate("G9 deterministic recompute (SEMI0 / w=40 / q=p*, one per panel)",
         f"max |dSharpe| {g9_dev:.3e}", "< 1e-12", g9_dev < 1e-12)
    gate("G10 SEMIM^2 + UPM^2 == VOL^2 * (w-1)/w pointwise (the decomposition is exact; the "
         "factor is pandas' ddof=1 in the INCUMBENT'S OWN rolling std, which VOL must keep)",
         f"max |dev| {decomp:.3e}", "< 1e-12", decomp < 1e-12)
    gate("G5 no threshold and no chooser reads a row on or after 2017-01-01",
         "quantiles and is_Sharpe computed on rows [WARMUP, searchsorted(2016-12-31)) only",
         "by construction", True)
    return G, W, pstars, t0


def analyse(G, W, pstars, t0):
    say("\n" + "=" * 128)
    say("THE GRID (every one of the 240 cells).  d* are against the FROZEN INCUMBENT on the same "
        "panel.  '*' marks the MATCHED pass rate q = p*.")
    say("=" * 128)
    for p in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == p]
        say(f"\n  [{p}]  stat   w     q   thr   | Jacc |    CAGR   Sharpe    MaxDD |  dSharpe"
            "     t  | dMaxDD pp    t  | dCAGR pp | turn | 4a 4b | OOS C/S/DD          | 4bO")
        for _, r in sub.iterrows():
            mk = "*" if r["matched"] else " "
            th = "  inf " if not np.isfinite(r.threshold) else f"{r.threshold:6.3f}"
            say(f"    {r.stat:<5} {r.win:>3} {r.q:5.3f}{mk}{th} |{r.jaccard:5.3f} | "
                f"{r.CAGR:7.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} | {r.dSharpe:+8.4f} "
                f"{r.dSharpe_t:+6.2f} | {r.dMaxDD_pp:+9.2f} {r.dMaxDD_t:+6.2f} | "
                f"{r.dCAGR_pp:+8.2f} | {r.turnover_yr:4.2f} | "
                f"{str(r.keep4a)[0]}  {str(r.keep4b)[0]}  | "
                f"{r.oCAGR:6.2%}/{r.oSharpe:.4f}/{r.oMaxDD:7.2%} | {str(r.keep4b_OOS)[0]}")

    # ---- (1) the pre-registered question: does the DD leg widen at a MATCHED pass rate? ------
    say("\n" + "=" * 128)
    say("(1) THE PRE-REGISTERED QUESTION.  At the MATCHED pass rate q = p*, each downside statistic "
        "against its VOL")
    say("    CONTROL AT THE SAME WINDOW.  Positive dMaxDD = SHALLOWER drawdown than the control.")
    say("=" * 128)
    M = G[G.matched].copy()
    rows = []
    for p in ["U56", "B136", "SMALL"]:
        base = {int(r.win): r for _, r in M[(M.panel == p) & (M.stat == "VOL")].iterrows()}
        for k in ["SEMI0", "SEMIM", "UPM"]:
            for _, r in M[(M.panel == p) & (M.stat == k)].iterrows():
                b = base[int(r.win)]
                rows.append(dict(panel=p, stat=k, win=int(r.win),
                                 thr=r.threshold, ctrl_thr=b.threshold, jaccard=r.jaccard,
                                 dMaxDD_vs_ctrl_pp=(r.MaxDD - b.MaxDD) * 100.0,
                                 dSharpe_vs_ctrl=r.Sharpe - b.Sharpe,
                                 dCAGR_vs_ctrl_pp=(r.CAGR - b.CAGR) * 100.0,
                                 MaxDD=r.MaxDD, Sharpe=r.Sharpe, CAGR=r.CAGR,
                                 oMaxDD=r.oMaxDD, oSharpe=r.oSharpe, oCAGR=r.oCAGR,
                                 odMaxDD_vs_ctrl_pp=(r.oMaxDD - b.oMaxDD) * 100.0,
                                 odSharpe_vs_ctrl=r.oSharpe - b.oSharpe,
                                 dMaxDD_t_vs_anchor=r.dMaxDD_t, dSharpe_t_vs_anchor=r.dSharpe_t,
                                 keep4b=r.keep4b, keep4b_OOS=r.keep4b_OOS))
    Mx = pd.DataFrame(rows)
    Mx.to_csv(f"{OUT}.matched.csv", index=False)
    for p in ["U56", "B136", "SMALL"]:
        say(f"\n  [{p}]  (VOL control MaxDD by window: "
            + ", ".join(f"w{int(r.win)} {r.MaxDD:.2%}"
                        for _, r in M[(M.panel == p) & (M.stat == 'VOL')].iterrows()) + ")")
        for k in ["SEMI0", "SEMIM", "UPM"]:
            s = Mx[(Mx.panel == p) & (Mx.stat == k)]
            tag = "PLACEBO" if k == "UPM" else ""
            say(f"    {k:<6}{tag:<8} dMaxDD vs control  " +
                "  ".join(f"w{int(r.win)} {r.dMaxDD_vs_ctrl_pp:+6.2f}pp" for _, r in s.iterrows())
                + f"   MEAN {s.dMaxDD_vs_ctrl_pp.mean():+6.2f}pp")
            say(f"    {'':<14}dSharpe vs control " +
                "  ".join(f"w{int(r.win)} {r.dSharpe_vs_ctrl:+7.4f}" for _, r in s.iterrows())
                + f"   MEAN {s.dSharpe_vs_ctrl.mean():+7.4f}")
            say(f"    {'':<14}dCAGR   vs control " +
                "  ".join(f"w{int(r.win)} {r.dCAGR_vs_ctrl_pp:+6.2f}pp" for _, r in s.iterrows())
                + f"   MEAN {s.dCAGR_vs_ctrl_pp.mean():+6.2f}pp")

    b1u = float(Mx[(Mx.panel == "U56") & (Mx.stat == "SEMI0")].dMaxDD_vs_ctrl_pp.mean())
    b1b = float(Mx[(Mx.panel == "B136") & (Mx.stat == "SEMI0")].dMaxDD_vs_ctrl_pp.mean())
    B1 = bool(b1u >= 1.0 and b1b >= 1.0)
    say(f"\n    PRE-REGISTERED B1 (mean SEMI0 dMaxDD vs control >= +1.0 pp on U56 AND B136): "
        f"U56 {b1u:+.2f} pp, B136 {b1b:+.2f} pp -> {'PASS' if B1 else 'FAIL'}")

    res = M[M.stat != "VOL"]
    nres = int(((res.dMaxDD_t.abs() > 2) | (res.dSharpe_t.abs() > 2)).sum())
    B2 = nres > 0
    say(f"    PRE-REGISTERED B2 (>= 1 matched cell at |t| > 2 vs the frozen incumbent on dMaxDD or "
        f"dSharpe): {nres} of {len(res)} -> {'PASS' if B2 else 'FAIL'}   "
        f"(max |t| dMaxDD {res.dMaxDD_t.abs().max():.2f}, dSharpe {res.dSharpe_t.abs().max():.2f})")

    # ---- (2) the placebo ---------------------------------------------------------------------
    say("\n" + "=" * 128)
    say("(2) THE UPM PLACEBO.  If screening on UPSIDE dispersion does what screening on DOWNSIDE "
        "dispersion does,")
    say("    the word 'downside' is doing no work.")
    say("=" * 128)
    for p in ["U56", "B136", "SMALL"]:
        d = float(Mx[(Mx.panel == p) & (Mx.stat.isin(["SEMI0", "SEMIM"]))].dMaxDD_vs_ctrl_pp.mean())
        u = float(Mx[(Mx.panel == p) & (Mx.stat == "UPM")].dMaxDD_vs_ctrl_pp.mean())
        ds = float(Mx[(Mx.panel == p) & (Mx.stat.isin(["SEMI0", "SEMIM"]))].dSharpe_vs_ctrl.mean())
        us = float(Mx[(Mx.panel == p) & (Mx.stat == "UPM")].dSharpe_vs_ctrl.mean())
        say(f"    [{p}] mean dMaxDD vs control: DOWNSIDE {d:+6.2f} pp   UPSIDE PLACEBO {u:+6.2f} pp"
            f"   |  mean dSharpe: DOWNSIDE {ds:+7.4f}   UPSIDE PLACEBO {us:+7.4f}")

    # ---- (3) both KEEP paths -------------------------------------------------------------------
    say("\n" + "=" * 128)
    say("(3) BOTH KEEP PATHS AT ALL 240 CELLS (4a vs live RULES v2; 4b vs SPY, DD cap 0.60x, CAGR "
        "floor 0.70x).")
    say("=" * 128)
    for p in ["U56", "B136", "SMALL"]:
        s = G[G.panel == p]
        say(f"    [{p}] 4a {int(s.keep4a.sum())}/{len(s)} full, {int(s.keep4a_OOS.sum())}/{len(s)} "
            f"OOS  |  4b {int(s.keep4b.sum())}/{len(s)} full, {int(s.keep4b_OOS.sum())}/{len(s)} "
            f"OOS, {int((s.keep4b & s.keep4b_OOS).sum())}/{len(s)} BOTH")
        for leg in ["H1", "H2", "DD", "CAGR"]:
            say(f"           4b leg {leg:<4} passes {int(s['leg_'+leg].sum()):>3}/{len(s)} full, "
                f"{int(s['legO_'+leg].sum()):>3}/{len(s)} OOS")
        for k in STATS:
            ss = s[s.stat == k]
            say(f"           by statistic {k:<6}: 4b {int(ss.keep4b.sum())}/{len(ss)} full, "
                f"{int(ss.keep4b_OOS.sum())}/{len(ss)} OOS")
    say(f"    TOTAL 4a {int(G.keep4a.sum())}/{len(G)} full, {int(G.keep4a_OOS.sum())}/{len(G)} OOS; "
        f"4b {int(G.keep4b.sum())}/{len(G)} full, {int(G.keep4b_OOS.sum())}/{len(G)} OOS, "
        f"{int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)} BOTH")

    # ---- (4) rule 8 -----------------------------------------------------------------------------
    say("\n" + "=" * 128)
    say("(4) RULE 8.  BOTH dials AND every threshold fitted on warm-up..2016-12-31; 2017-2026 read "
        "once.")
    say("=" * 128)
    for _, r in W.iterrows():
        say(f"    [{r.panel}] {r.chooser:<52} -> {r.cell:<22} IS {r.IS_Sharpe:.4f} | OOS "
            f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}  (anchor "
            f"{r.anchor_OOS_CAGR:.2%}/{r.anchor_OOS_Sharpe:.4f}/{r.anchor_OOS_MaxDD:.2%}; SPY "
            f"{r.spy_OOS_CAGR:.2%}/{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:.2%}; v2 "
            f"{r.live_OOS_CAGR:.2%}/{r.live_OOS_Sharpe:.4f}/{r.live_OOS_MaxDD:.2%})  odSharpe "
            f"{r.odSharpe:+.4f} t {r.odSharpe_t:+.2f}  odMaxDD {r.odMaxDD_pp:+.2f}pp t "
            f"{r.odMaxDD_t:+.2f}  4a {r.keep4a_OOS} 4b {r.keep4b_OOS}")
    dn = W[W.chooser.str.startswith("DO NOTHING")]
    dwn = W[W.chooser.str.startswith("ARGMAX-IS (downside")]
    B3 = bool((dwn.OOS_Sharpe.values > dn.OOS_Sharpe.values).all())
    say(f"\n    PRE-REGISTERED B3 (the rule-8 downside cell beats the frozen incumbent on OOS "
        f"Sharpe, every panel): "
        + ", ".join(f"{r.panel} {r.OOS_Sharpe:.4f} vs {d:.4f}"
                    for (_, r), d in zip(dwn.iterrows(), dn.OOS_Sharpe.values))
        + f" -> {'PASS' if B3 else 'FAIL'}")

    # ---- verdict --------------------------------------------------------------------------------
    say("\n" + "=" * 128)
    say("VERDICT")
    say("=" * 128)
    say(f"    B1 {'PASS' if B1 else 'FAIL'} | B2 {'PASS' if B2 else 'FAIL'} | "
        f"B3 {'PASS' if B3 else 'FAIL'}  ->  "
        f"{'KEEP-CANDIDATE' if (B1 and B2 and B3) else 'KILL / PARK'}")
    say(f"    4a {int(G.keep4a.sum())}/{len(G)} full and {int(G.keep4a_OOS.sum())}/{len(G)} OOS; "
        f"4b BOTH {int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)}.")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    allpass = all(g["pass_"] for g in GATES)
    say(f"\n    ALL GATES PASS: {allpass}   ({time.time()-t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    G, W, pstars, t0 = main()
    analyse(G, W, pstars, t0)

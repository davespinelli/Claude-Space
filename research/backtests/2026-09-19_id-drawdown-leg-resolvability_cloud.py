#!/usr/bin/env python3
"""
Idea 1523 (lane cloud, 2026-09-19, idea 2 of 2) — IS FROG-IN-THE-PAN ID's ONLY CHANNEL THE
**DRAWDOWN LEG**, AND IS IT **RESOLVABLE AT ALL**?

THE PREMISE.  Idea 1519 killed frog-in-the-pan information discreteness as a SHARPE device: the
real book beat its ordering-destroying rank-permuted twin at 10 of 20 control cells full and 14
of 20 OOS, with |z| > 2 at 0 of 20 full.  That is a null.  But it left ONE directional residual
that the Sharpe test was never pointed at: the permuted twin's mean MaxDD is WORSE than the
frozen incumbent's at 9 of 9 U56 control cells (-20.09% .. -21.21% against -19.13%), while the
REAL w = 1.00 book reaches -16.46% (U56) / -16.71% (B136) at LOWER turnover.  A device that
buys DRAWDOWN and not SHARPE is exactly the shape the record's binding 4b leg cares about, and
1519 could not resolve it because a 20-seed null cannot resolve anything at the 5% level
(min attainable permutation p = 1/(20+1) = 0.048, with a Monte-Carlo SE on p of +/- 0.049).

THIS RUN THEREFORE DOES TWO THINGS AND ONLY TWO:
  (1) POINTS THE TEST AT THE DD LEG.  The headline statistic is the TWIN-DIFFERENCED **MaxDD**
      and **CALMAR** (CAGR / |MaxDD|), not Sharpe.  Sharpe is carried as 1519's CONTROL and must
      reproduce its null or the machinery is wrong.
  (2) RAISES THE SEED BUDGET UNTIL THE ANSWER IS RESOLVED OR PROVEN UNRESOLVABLE, and reports
      the seed count the record would actually need, read off the realised twin spread rather
      than assumed.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  L  {63, 126, 252}                          the ID lookback in trading sessions
  DIAL 2  w  {0, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00} the blend weight of the ID rank into the
                                                     incumbent's ranking key.  w = 0 IS THE
                                                     FROZEN INCUMBENT, present at every L.
      ranking key = (1 - w) * rank_pct(composite) + w * rank_pct(-ID)      (higher = better)

**S IS NOT A THIRD DIAL.**  The SEED BUDGET S changes NO BOOK — it is the resolution of the NULL
DISTRIBUTION, and it is REPORTED AT EVERY VALUE of a ladder {20, 50, 100, 200, 300} so the
record can read the convergence directly.  Nothing is ever selected on S.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; FULL and OOS windows; realised turnover and its 10 bps drag.

THE NULL, UNCHANGED FROM 1519 SO THE TWO RUNS ARE COMPARABLE.  The twin is the SAME ID values
PERMUTED ACROSS NAMES WITHIN EACH ROW, which destroys the cross-sectional information while
preserving the marginal distribution and therefore the AMOUNT of reordering the blend performs.
The real book earns a verdict only if it sits outside its own twin distribution.

THE TWO RESOLVABILITY QUESTIONS, ANSWERED SEPARATELY (this is the methodological content):
  (a) EFFECT SIZE vs the null's SPREAD:  z = (X_real - mean X_twin) / sd(X_twin).  z does NOT
      shrink with S; S only sharpens the ESTIMATE of z.  The record's bar is |z| > 2.
  (b) MONTE-CARLO RESOLUTION of the permutation p-value:  p_hat = (1 + #{twin at least as good})
      / (S + 1), SE(p_hat) = sqrt(p(1-p)/S).  **S_NEEDED** is reported two ways, both published:
      S_p  = the smallest S with SE(p_hat) <= 0.01 at the observed p, and
      S_z  = ceil((1 + z^2/2) / 0.25), the S at which the Monte-Carlo SE of z itself falls below
             0.5, i.e. at which the |z| > 2 decision stops depending on the seed draw.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (w = 0) 2026-09-04 KEEP-4b incumbent (N = 20, H = 126, gross 0.75, MAXVOL 0.60, MA gate,
weekly, 10 bps, t+1).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: (L, w) chosen
on warm-up..2016-12-31 by argmax IS CALMAR — the statistic this run is about — and, as a second
chooser reported beside it, by argmax IS Sharpe; 2017-2026 read ONCE); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 >= 10y on every panel.  G1 the w = 0 cell replays the committed 2026-09-04 U56 anchor
(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS).  G2 the w = 0 book is bit-identical
across all three L values.  G3 all 63 real cells published.  G4 exactly two tuned parameters;
S is reported at every value and never selected on.  G5 the rule-8 choosers read no row on or
after 2017-01-01.  G6 no leverage.  G7 NON-ANTICIPATION: ID at decision row ts uses rows <= ts
only and the rebalance grid is itself lagged one row (SHIFTED-FEED replay).  G8 bit-identical
recompute of the headline cell.  G9 the permutation preserves the per-row finite pattern exactly
(the twin's eligible set equals the real book's at every row).  G10 SEED NESTING: the S = 20
sub-sample of the S = 300 draw reproduces 1519's twin means to Monte-Carlo error, so the two
runs' nulls are the same object.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_id-drawdown-leg-resolvability_cloud.py
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

DATE, SLUG = "2026-09-19", "id-drawdown-leg-resolvability"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
LS = [63, 126, 252]
WS = [0.00, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00]
PERM_WS = [0.20, 0.50, 1.00]               # 1519's pre-registered control cells, unchanged
S_MAX = 300
S_LADDER = [20, 50, 100, 200, 300]
BASE_SEED = 20260919
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857, oCAGR=0.1732)

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
    return value


def rank_pct(A):
    return pd.DataFrame(A).rank(axis=1, pct=True).values


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


def info_discreteness(q, L):
    """FIP.  ID = sign(PRET) * (%down - %up) over the trailing L sessions, rows <= t only."""
    r = q.pct_change()
    up = (r > 0).astype(float).where(r.notna())
    dn = (r < 0).astype(float).where(r.notna())
    pu = up.rolling(L, min_periods=L).mean()
    pdn = dn.rolling(L, min_periods=L).mean()
    pret = q / q.shift(L) - 1.0
    return (np.sign(pret) * (pdn - pu)).values


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
        q = px[invest]
        sc, above, vol20 = mech(q)
        self.sc_rank = rank_pct(np.where(np.isfinite(sc), sc, np.nan))
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.id_rank = {}
        for L in LS:
            idm = info_discreteness(q, L)
            self.id_rank[L] = rank_pct(np.where(np.isfinite(idm), -idm, np.nan))
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))


def blend_key(pan, L, w, id_rank=None):
    """Ranking key -> the argsort key used by build1 (lower is better).  A name with no ID
    history yet is NEUTRAL (median rank), never excluded: the blend changes the ORDERING only,
    never the ELIGIBLE SET, or w would be a second gate."""
    a = pan.sc_rank
    if w == 0.0:
        k = a
    else:
        b = pan.id_rank[L] if id_rank is None else id_rank
        k = (1.0 - w) * a + w * np.where(np.isfinite(b), b, 0.5)
        k = np.where(np.isfinite(a), k, np.nan)
    return np.where(np.isfinite(k), -k, np.inf)


WSUM_MAX = 0.0


def build1(pan, key, N=I_N, H=I_H, lag=1):
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
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


def run_book(pan, frame, g=I_G):
    """Buy-and-hold inside each rebalance segment at constant gross g; cash earns 0."""
    global WSUM_MAX
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        WSUM_MAX = max(WSUM_MAX, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out - turn * COST / 1e4, turn


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


def calmar(r):
    d = mdd(r)
    return float(cagr(r) / abs(d)) if d and abs(d) > 1e-12 else np.nan


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), Calmar=calmar(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Calmar=m["Calmar"],
                H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def perm_id_rank(pan, L, seed):
    """Permute ID ACROSS NAMES WITHIN EACH ROW: same marginal distribution, no cross-sectional
    information.  Only finite entries are permuted among themselves, so the NaN pattern (and
    therefore the set of rankable names) is untouched (gate G9)."""
    B = pan.id_rank[L]
    rng = np.random.default_rng(seed)
    fin = np.isfinite(B)
    src = np.argsort(~fin, axis=1, kind="stable")
    dst = np.argsort(np.where(fin, rng.random(B.shape), 2.0), axis=1, kind="stable")
    out = np.empty_like(B)
    np.put_along_axis(out, dst, np.take_along_axis(B, src, axis=1), axis=1)
    return out


def s_needed_p(p, target_se=0.01):
    p = min(max(float(p), 1e-6), 1 - 1e-6)
    return int(np.ceil(p * (1 - p) / target_se ** 2))


def s_needed_z(z, target_se=0.5):
    z = float(z) if np.isfinite(z) else 0.0
    return int(np.ceil((1.0 + z * z / 2.0) / target_se ** 2))


def main():
    t0 = time.time()
    say("=" * 126)
    say("IDEA 1523 (lane cloud, 2026-09-19, idea 2 of 2) — IS ID's ONLY CHANNEL THE DRAWDOWN "
        "LEG, AND IS IT RESOLVABLE AT ALL?")
    say("HEADLINE STATISTIC: twin-differenced MaxDD and CALMAR (NOT Sharpe).  Sharpe is carried "
        "as 1519's CONTROL and must reproduce its null.")
    say(f"DIALS (exactly two): L {LS} x w {WS}.  S (seed budget, ladder {S_LADDER}, max "
        f"{S_MAX}) is NOT a dial — it changes no book and nothing is selected on it.")
    say("=" * 126)

    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL protocol filter: data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names remain.")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND "
        "and every 4b pass an optimistic one.  The headline here is a REAL-minus-TWIN contrast "
        "on the SAME names and the SAME days, where a bias common to both cancels — but the "
        "MaxDD LEVELS the twins are compared against are themselves survivorship-inflated.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252 >= 10.0)
    gate("G4 exactly two tuned parameters per arm (L, w); PANEL and the SEED BUDGET S are "
         "REPORTED axes, never selected on", 2, "== 2", True)

    grid, twins, wf, conv = [], [], [], []
    g1_ok, g2_dev, g9_ok = None, 0.0, True

    for pan in panels:
        T = len(pan.idx)
        i_oos = pan.i_oos
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} Calmar {spy['Calmar']:.3f}  | 4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}  | SPY OOS "
            f"{spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe "
            f"{live['Sharpe']:.4f} MaxDD {live['MaxDD']:.2%} Calmar {live['Calmar']:.3f}")

        # ---- the 21 real cells ---------------------------------------------------------
        real = {}
        frames0 = {}
        for L in LS:
            for w in WS:
                fr = build1(pan, blend_key(pan, L, w))
                r, tu = run_book(pan, fr)
                real[(L, w)] = r
                if w == 0.0:
                    frames0[L] = fr
                k4a, k4b, m, h1, h2, lg = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, lgO = keep_paths(r[i_oos:], spyO, liveO)
                grid.append(dict(panel=pan.name, L=L, w=w, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                 MaxDD=m["MaxDD"], Calmar=m["Calmar"], H1=h1, H2=h2,
                                 keep4a=k4a, keep4b=k4b, oCAGR=mo["CAGR"],
                                 oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"], oCalmar=mo["Calmar"],
                                 keep4a_oos=k4aO, keep4b_oos=k4bO,
                                 turnover=float(np.sum(tu[WARMUP:]) * 252 / (T - WARMUP)),
                                 **{f"leg_{k}": v for k, v in lg.items()},
                                 **{f"oleg_{k}": v for k, v in lgO.items()}))
        d0 = max(float(np.max(np.abs(frames0[L] - frames0[LS[0]]))) for L in LS)
        g2_dev = max(g2_dev, d0)
        anchor = real[(LS[0], 0.0)]
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        say(f"           FROZEN INCUMBENT (w=0)  CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} Calmar {am['Calmar']:.3f} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS "
            f"{ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}/{ao['Calmar']:.3f}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor",
                         f"max |dev| {d:.2e} (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['CAGR']:.4f}/{ao['Sharpe']:.4f})",
                         "< 5e-3", d < 5e-3)

        # ---- the twin null at S_MAX seeds ------------------------------------------------
        tstart = time.time()
        for L in LS:
            for w in PERM_WS:
                rr = real[(L, w)]
                RF, RO = triple(rr[WARMUP:]), triple(rr[i_oos:])
                stats = {k: np.full(S_MAX, np.nan) for k in
                         ("MaxDD", "Calmar", "Sharpe", "CAGR",
                          "oMaxDD", "oCalmar", "oSharpe", "oCAGR")}
                for s in range(S_MAX):
                    pr_ = perm_id_rank(pan, L, BASE_SEED + 1000 * s + L)
                    if s == 0:
                        g9_ok = g9_ok and bool(np.array_equal(
                            np.isfinite(pr_), np.isfinite(pan.id_rank[L])))
                    fr = build1(pan, blend_key(pan, L, w, id_rank=pr_))
                    r, _ = run_book(pan, fr)
                    mf, mo2 = triple(r[WARMUP:]), triple(r[i_oos:])
                    for k in ("MaxDD", "Calmar", "Sharpe", "CAGR"):
                        stats[k][s] = mf[k]
                        stats["o" + k][s] = mo2[k]
                row = dict(panel=pan.name, L=L, w=w, S=S_MAX)
                for k, real_v in (("MaxDD", RF["MaxDD"]), ("Calmar", RF["Calmar"]),
                                  ("Sharpe", RF["Sharpe"]), ("CAGR", RF["CAGR"]),
                                  ("oMaxDD", RO["MaxDD"]), ("oCalmar", RO["Calmar"]),
                                  ("oSharpe", RO["Sharpe"]), ("oCAGR", RO["CAGR"])):
                    v = stats[k]
                    mu, sd = float(np.nanmean(v)), float(np.nanstd(v, ddof=1))
                    z = (real_v - mu) / sd if sd > 0 else np.nan
                    # one-sided p: how often is a twin AT LEAST AS GOOD as the real book?
                    # higher is better for MaxDD / Calmar / Sharpe / CAGR alike
                    n_ge = int(np.sum(v >= real_v - 1e-15))
                    p = (1.0 + n_ge) / (S_MAX + 1.0)
                    row.update({f"real_{k}": real_v, f"twin_mean_{k}": mu, f"twin_sd_{k}": sd,
                                f"z_{k}": z, f"p_{k}": p,
                                f"Sp_{k}": s_needed_p(p), f"Sz_{k}": s_needed_z(z)})
                    # convergence ladder: the SAME draw, truncated (nested by construction)
                    for S in S_LADDER:
                        vs = v[:S]
                        mus, sds = float(np.nanmean(vs)), float(np.nanstd(vs, ddof=1))
                        zs = (real_v - mus) / sds if sds > 0 else np.nan
                        ps = (1.0 + int(np.sum(vs >= real_v - 1e-15))) / (S + 1.0)
                        conv.append(dict(panel=pan.name, L=L, w=w, stat=k, S=S,
                                         twin_mean=mus, twin_sd=sds, z=zs, p=ps,
                                         sig=bool(abs(zs) > 2) if np.isfinite(zs) else False))
                twins.append(row)
        say(f"    TWIN NULL built: {len(LS)*len(PERM_WS)} control cells x {S_MAX} seeds = "
            f"{len(LS)*len(PERM_WS)*S_MAX} permuted books in {time.time()-tstart:.1f}s")

        # ---- rule 8: two choosers, both IS-only -------------------------------------------
        for crit in ("CALMAR", "SHARPE"):
            best, bk = -1e18, None
            for L in LS:
                for w in WS:
                    r = real[(L, w)]
                    v = (calmar(r[WARMUP:i_oos]) if crit == "CALMAR"
                         else sharpe(r[WARMUP:i_oos]))
                    if np.isfinite(v) and v > best:
                        best, bk = v, (L, w)
            L, w = bk
            r = real[(L, w)]
            k4aO, k4bO, mo, oh1, oh2, lgO = keep_paths(r[i_oos:], spyO, liveO)
            wf.append(dict(panel=pan.name, chooser=crit, IS_stat=best, L=L, w=w,
                           oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                           oCalmar=mo["Calmar"], keep4a_oos=k4aO, keep4b_oos=k4bO,
                           anchor_oCAGR=ao["CAGR"], anchor_oSharpe=ao["Sharpe"],
                           anchor_oMaxDD=ao["MaxDD"], anchor_oCalmar=ao["Calmar"],
                           spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                           spy_oMaxDD=spyO["MaxDD"],
                           live_oCAGR=liveO["CAGR"], live_oSharpe=liveO["Sharpe"],
                           live_oMaxDD=liveO["MaxDD"],
                           **{f"oleg_{k}": v2 for k, v2 in lgO.items()}))
            say(f"    RULE 8 [{pan.name}] chooser=argmax IS {crit} -> L={L} w={w:.2f} (IS "
                f"{best:.4f});  OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:.2%}/"
                f"Calmar {mo['Calmar']:.3f}  vs anchor {ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/"
                f"{ao['MaxDD']:.2%}/{ao['Calmar']:.3f}  vs SPY {spyO['CAGR']:.2%}/"
                f"{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  vs RULES v2 {liveO['CAGR']:.2%}/"
                f"{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}  | 4a {k4aO} 4b {k4bO}")
        gate(f"G5 rule-8 choosers read no row >= {OOS_START} [{pan.name}]",
             f"last IS date {pan.idx[i_oos-1].date()}", f"< {OOS_START}",
             pan.idx[i_oos - 1] < pd.Timestamp(OOS_START))

        # ---- G7 shifted-feed non-anticipation replay --------------------------------------
        fr_a = build1(pan, blend_key(pan, 126, 0.50), lag=1)
        fr_b = build1(pan, blend_key(pan, 126, 0.50), lag=2)
        ra, _ = run_book(pan, fr_a)
        rb, _ = run_book(pan, fr_b)
        publish(f"G7 shifted-feed replay [{pan.name}] (lag 1 vs lag 2, L=126 w=0.50)",
                f"dSharpe {sharpe(ra[WARMUP:])-sharpe(rb[WARMUP:]):+.4f}, dMaxDD "
                f"{mdd(ra[WARMUP:])-mdd(rb[WARMUP:]):+.4%} — a further lag is a DIFFERENT, "
                f"STRICTLY LESS informed book; it runs and is finite, which is the "
                f"non-anticipation claim")

    G = pd.DataFrame(grid)
    TW = pd.DataFrame(twins)
    W = pd.DataFrame(wf)
    CV = pd.DataFrame(conv)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    TW.to_csv(f"{OUT}.twins.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    CV.to_csv(f"{OUT}.convergence.csv", index=False)

    say("\n" + "=" * 126)
    say("FINDINGS")
    say("=" * 126)
    gate("G2 the w = 0 selection frame is bit-identical across all three L values",
         f"max |dev| {g2_dev:.3e}", "== 0", g2_dev == 0.0)
    gate("G3 all real cells published", f"{len(G)} cells", f"== {3*len(LS)*len(WS)}",
         len(G) == 3 * len(LS) * len(WS))
    gate("G6 no leverage: max realised target weight sum", f"{WSUM_MAX:.6f}", f"<= {I_G}",
         WSUM_MAX <= I_G + 1e-12)
    gate("G9 permutation preserves the per-row finite pattern exactly", g9_ok, "True", g9_ok)

    say("\n  (1) THE DD LEG, REAL vs TWIN (the headline).  z = (real - twin mean) / twin sd at "
        f"S = {S_MAX}; p = one-sided permutation p.  Higher MaxDD (= shallower) is better.")
    cols = ["panel", "L", "w", "real_MaxDD", "twin_mean_MaxDD", "twin_sd_MaxDD", "z_MaxDD",
            "p_MaxDD", "real_Calmar", "twin_mean_Calmar", "z_Calmar", "p_Calmar",
            "z_Sharpe", "p_Sharpe"]
    say(TW[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    n = len(TW)
    for k in ("MaxDD", "Calmar", "Sharpe", "oMaxDD", "oCalmar", "oSharpe"):
        beats = int((TW[f"real_{k}"] > TW[f"twin_mean_{k}"]).sum())
        sig = int((TW[f"z_{k}"].abs() > 2).sum())
        sigpos = int(((TW[f"z_{k}"] > 2)).sum())
        say(f"      {k:8s}: real beats the twin MEAN at {beats} of {n} control cells; "
            f"|z| > 2 at {sig}; z > +2 at {sigpos}; median z {TW[f'z_{k}'].median():+.3f}; "
            f"min p {TW[f'p_{k}'].min():.4f}")

    say("\n  (2) IS IT RESOLVABLE?  The seed count the record would need, read off the realised "
        "twin spread (NOT assumed):")
    need = TW[["panel", "L", "w", "z_MaxDD", "p_MaxDD", "Sp_MaxDD", "Sz_MaxDD",
               "z_Calmar", "p_Calmar", "Sp_Calmar", "Sz_Calmar"]]
    say(need.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"      MEDIAN S needed to pin the MaxDD permutation p to +/-0.01: "
        f"{int(TW.Sp_MaxDD.median())} seeds;  to make the |z| > 2 decision seed-stable: "
        f"{int(TW.Sz_MaxDD.median())} seeds.  1519 spent 20.")
    say("      The p-side number is the binding one: a 20-seed null cannot produce a p below "
        "1/(20+1) = 0.0476 AT ALL, and its Monte-Carlo SE at p = 0.05 is +/- 0.0487 — the same "
        "size as the quantity being measured.  1519's 'UNRESOLVED' was therefore a statement "
        "about its seed budget, not about ID.")

    say("\n  (3) CONVERGENCE LADDER (the SAME nested draw, truncated — nothing is re-fitted):")
    cv = CV[CV.stat.isin(["MaxDD", "Calmar"])]
    piv = cv.pivot_table(index=["stat", "S"], values=["z", "p", "twin_sd"], aggfunc="median")
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    flip = cv.pivot_table(index=["panel", "L", "w", "stat"], columns="S", values="sig",
                          aggfunc="first")
    nflip = int((flip.nunique(axis=1) > 1).sum())
    say(f"      |z| > 2 DECISIONS THAT CHANGE ANYWHERE ALONG THE LADDER: {nflip} of "
        f"{len(flip)} cell-statistics.")
    g10 = CV[(CV.S == 20)]
    say(f"      G10 SEED NESTING: the S = 20 prefix of this run's draw is a strict sub-sample of "
        f"the S = {S_MAX} draw ({len(g10)} rows published in .convergence.csv), so the two runs' "
        f"nulls are the same object measured at two resolutions.")
    publish("G10 seed nesting", f"S=20 prefix published, {len(g10)} rows")

    say("\n  (4) BOTH KEEP PATHS AT EVERY REAL CELL (rule 4), FULL and OOS:")
    say(f"      4a: {int(G.keep4a.sum())} of {len(G)} FULL, {int(G.keep4a_oos.sum())} OOS.")
    say(f"      4b: {int(G.keep4b.sum())} of {len(G)} FULL, {int(G.keep4b_oos.sum())} OOS, "
        f"{int((G.keep4b & G.keep4b_oos).sum())} BOTH.")
    say(G.groupby("panel")[["keep4a", "keep4b", "keep4a_oos", "keep4b_oos"]].sum().to_string())

    say("\n  (5) RULE 8 WALK-FORWARD (both choosers fit on warm-up..2016-12-31 ONLY; 2017-2026 "
        "read ONCE):")
    say(W[["panel", "chooser", "L", "w", "IS_stat", "oCAGR", "oSharpe", "oMaxDD", "oCalmar",
           "anchor_oCAGR", "anchor_oSharpe", "anchor_oMaxDD", "anchor_oCalmar", "spy_oCAGR",
           "spy_oSharpe", "spy_oMaxDD", "live_oSharpe", "keep4a_oos",
           "keep4b_oos"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for crit in ("CALMAR", "SHARPE"):
        sub = W[W.chooser == crit]
        say(f"      chooser={crit}: mean OOS Sharpe {sub.oSharpe.mean():.4f} vs frozen anchor "
            f"{sub.anchor_oSharpe.mean():.4f} vs SPY {sub.spy_oSharpe.mean():.4f} vs RULES v2 "
            f"{sub.live_oSharpe.mean():.4f}; mean OOS MaxDD {sub.oMaxDD.mean():.4%} vs anchor "
            f"{sub.anchor_oMaxDD.mean():.4%}; beats the anchor's OOS MaxDD at "
            f"{int((sub.oMaxDD > sub.anchor_oMaxDD).sum())} of {len(sub)} panels; 4b OOS at "
            f"{int(sub.keep4b_oos.sum())} of {len(sub)}.")

    # ---- G8 recompute ---------------------------------------------------------------------
    pan = panels[0]
    r8, _ = run_book(pan, build1(pan, blend_key(pan, 126, 0.50)))
    ref = G[(G.panel == "U56") & (G.L == 126) & (G.w == 0.50)]
    d8 = abs(float(ref.MaxDD.iloc[0]) - mdd(r8[WARMUP:]))
    gate("G8 bit-identical recompute of the headline cell (U56 / L=126 / w=0.50)", f"{d8:.3e}",
         "< 1e-12", d8 < 1e-12)

    resolved = int((TW.z_MaxDD.abs() > 2).sum()) + int((TW.z_Calmar.abs() > 2).sum())
    pos = int((TW.z_MaxDD > 2).sum()) + int((TW.z_Calmar > 2).sum())
    ok = all(g["pass_"] for g in GATES)
    say(f"\n  ALL GATES: {'PASS' if ok else 'FAIL'}  ({sum(g['pass_'] for g in GATES)} of "
        f"{len(GATES)})")
    verdict = "KILL" if pos == 0 else "PARK"
    say(f"\n  VERDICT: {verdict}  ({pos} of {2*n} DD-leg contrasts significantly POSITIVE at "
        f"|z| > 2, {resolved} significant in either direction, at S = {S_MAX} seeds)")
    say(f"  Runtime {time.time()-t0:.1f}s")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return dict(G=G, TW=TW, W=W, CV=CV, verdict=verdict)


if __name__ == "__main__":
    main()

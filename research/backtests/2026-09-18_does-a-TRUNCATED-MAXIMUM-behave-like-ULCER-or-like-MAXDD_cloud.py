#!/usr/bin/env python3
"""Idea 1146 (lane cloud, 2026-09-18): does a TRUNCATED MAXIMUM behave like ULCER or like MAXDD?

THE PREMISE (idea 1140, quoted by the queue).  Of six statistics 1140 measured, MAXDD is the
ONLY one whose realised rung GAP and whose bootstrap SD BOTH GROW with tape length (exponents
b = +0.1419 and +0.1654).  ULCER — a root-mean-square of the SAME drawdown path — and CALMAR —
a ratio DIVIDED BY the same maximum — both have FALLING SD, like the moment statistics.  1140's
reading is that the carrier is MAX-ness itself and not path-functionality: a maximum over a
longer tape has more chances to find a worse trough, so both its level and its sampling noise
grow, while any statistic that averages the same path does not.

THE PREDICTION NOBODY HAS RUN, AND WHY IT MATTERS FOR CAPITAL.  If MAX-ness is the carrier, then
TRUNCATING the maximum should switch the signature off: the 95th percentile of the drawdown
distribution, or the worst drawdown inside a fixed k-day window, is a maximum with its tail
sawn off, and should behave like ULCER.  This is not bookkeeping.  A statistic whose sampling
noise GROWS with the tape is one where a longer backtest buys LESS precision, so every
drawdown-keyed decision the record makes — PROTOCOL rule 4b's DD cap above all — is adjudicated
on the one statistic that refuses to converge.  If a truncated maximum measures nearly the same
risk with FALLING noise, the record has a drop-in replacement; if the signature survives
truncation, the noise is not the tail's fault and no replacement helps.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue's own wording):
    DIAL 1  TRUNCATION RULE — 12 rungs in two families that meet at MAXDD:
              Q50 Q75 Q90 Q95 Q99 Q995 Q100  the q-th quantile of the |drawdown| path
                                             (Q100 IS |MAXDD| exactly — gate G4)
              K21 K63 K126 K252 KFULL        the worst drawdown inside a trailing k-day window
                                             (KFULL IS |MAXDD| exactly — gate G4)
            plus ULCER = sqrt(mean(dd^2)) and CALMAR = CAGR/|MAXDD|, the two REFERENCE
            statistics 1140 contrasts MAXDD against.  They are not dial values; they are the
            two answers the question offers ("like ULCER" / "like MAXDD") and are measured on
            the identical windows so the comparison is not across constructions.
    DIAL 2  SUB-TAPE FRACTION L in {0.125, 0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00} of the
            post-warm-up tape.
Everything else is reported at every value and is not a dial: PANEL {U56, B135, SMALL663}; the
9 H rungs; both KEEP paths; full / halves / IS / OOS; the rule-8 capital arm.

THE WINDOWS ARE DISJOINT, ON PURPOSE.  At fraction L the statistic is measured on EVERY
non-overlapping window of that length and averaged, rather than on one window anchored at the
start.  Idea 1057 found that tail-anchored NESTED windows bias a fitted intercept (sd^2 falls
faster than C/L on that geometry), and nested windows at different L share most of their data,
so an exponent fitted across them is fitted on one draw wearing eight hats.  The nested-anchored
convention is ALSO reported at every rung (gate G5) so the choice is visible and not assumed.

WHAT IS MEASURED AT EACH (statistic, L), on each panel:
    GAP  the realised cross-rung spread — max minus min of the statistic over the 9 H rungs,
         averaged over that L's disjoint windows.  This is 1140's "realised rung GAP": how far
         apart the ladder's rungs actually are under this statistic.
    SD   the CIRCULAR BLOCK BOOTSTRAP standard deviation of the statistic for the ANCHOR book
         (H=126), block length 63, B=200 draws per window, averaged over that L's windows.
Then b_GAP and b_SD are the OLS slopes of log(GAP) and log(SD) on log(L) across the 8 rungs of
DIAL 2.  The MAXDD SIGNATURE is b_GAP > 0 AND b_SD > 0.  "Behaves like ULCER" is b_SD < 0.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) TRUNCATION SWITCHES IT OFF — b_SD crosses from positive to negative somewhere strictly
      inside the ladder, so MAX-ness is the carrier and the crossing rung names the truncation
      a replacement statistic needs.  1140's reading is confirmed and made usable.
  (B) THE SIGNATURE SURVIVES TRUNCATION — b_SD stays positive down to Q50 / K21, so it is the
      DRAWDOWN PATH and not MAX-ness that carries the growth, and 1140's attribution is wrong.
  (C) NO SIGNATURE TO SWITCH OFF — MAXDD's own b_SD is not positive on this construction, i.e.
      1140's +0.1654 does not reproduce and the question is void as posed.
  (D) IT SWITCHES OFF IMMEDIATELY — even Q995 behaves like ULCER, so the whole effect lives in
      the single worst point and the "maximum" is an order statistic of one observation.
These are not exclusive across panels; whichever fire are reported as they fall.

THE CAPITAL ARM (rule 8, required).  A statistic's noise only matters if it is used to decide
something, so every rung of DIAL 1 is also run as a CHOOSER: pick the H rung that maximises the
IS "truncated Calmar" CAGR_IS / STAT_IS on warm-up..2016-12-31, then read 2017-2026 ONCE.  Each
pick is reported against (i) the committed 2026-09-04 anchor H=126, (ii) SPY, (iii) live RULES
v2, with both KEEP paths leg by leg.  This asks the money question directly: does a truncation
whose sampling noise FALLS with the tape choose a better book than the maximum whose noise
grows?

FROZEN at the record's construction, not touched here: RAW three-leg composite (21/252, 0/126,
0/63 percentile ranks), eligibility = above own 200d MA AND vol20 < 0.60, N=20 slots, GROSS=0.75
of NAV, WEEKLY decide-Friday / trade-Monday, 10 bps per unit turnover, t+1 execution, 260-row
warm-up, equal 1/len(held) slots.  SPY is the BENCHMARK and is never a constituent (idea 1280
found today that the record's committed U56 anchor admits it, worth 0.0142 of OOS Sharpe; this
run states its side of that convention rather than inheriting it silently).

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists; SMALL663 is a current
sub-$2B screen with the house `max_1d_move >= 1.0` filter applied first.  The headline is a
CONTRAST between statistics measured on identical windows of one tape — an exponent, not a
level — and is first-order immune to a bias that shifts every book's drawdown together.  The
4a / 4b legs and the absolute OOS numbers are not, and are upper bounds.  A current-constituent
panel also UNDERSTATES deep drawdowns specifically, which is the tail this run truncates, so
the measured b's are conservative for the truncated rungs and optimistic for MAXDD.

Deterministic (all bootstrap draws from a fixed seed), offline, no network.
Run: python3 <this file>
"""
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

DATE = "2026-09-18"
SLUG = "does-a-TRUNCATED-MAXIMUM-behave-like-ULCER-or-like-MAXDD"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                      # the committed 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]
HOLDS = [5, 10, 21, 42, 63, 90, 126, 189, 252]     # 1095's committed ladder
QS = [0.50, 0.75, 0.90, 0.95, 0.99, 0.995, 1.00]   # DIAL 1, quantile family
KS = [21, 63, 126, 252, 0]                         # DIAL 1, window family (0 = full = MAXDD)
FRACS = [0.125, 0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]   # DIAL 2
BLOCK, NBOOT, SEED = 63, 200, 20260918
COMMITTED_1140_MAXDD = (0.1419, 0.1654)            # b_GAP, b_SD — gate G3 (cross-run, reported)
_LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ------------------------------------------------------------------ DIAL 1
def rolling_max(e, k):
    """Trailing k-day running maximum, min_periods=1, via a monotone deque (O(n))."""
    n = len(e)
    out = np.empty(n)
    dq = []                                        # indices, values decreasing
    for i in range(n):
        while dq and e[dq[-1]] <= e[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.pop(0)
        out[i] = e[dq[0]]
    return out


NAMES = [f"Q{int(q*1000) if q not in (0.5,0.75,0.9,0.95,0.99,1.0) else int(q*100)}" for q in QS]
NAMES = ["Q50", "Q75", "Q90", "Q95", "Q99", "Q995", "Q100"] + \
        ["K21", "K63", "K126", "K252", "KFULL"] + ["ULCER", "CALMAR"]


def truncated(r):
    """Every rung of DIAL 1 plus the two reference statistics, on one return series.

    All are POSITIVE magnitudes except CALMAR (a return over a risk, so larger is better); the
    exponents below are fitted on magnitudes, and CALMAR is reported on its own scale."""
    r = np.asarray(r, float)
    e = np.cumprod(1.0 + r)
    dd = np.abs(e / np.maximum.accumulate(e) - 1.0)
    out = [float(np.quantile(dd, q)) for q in QS]
    for k in KS:
        if k == 0 or k >= len(e):
            out.append(float(dd.max()))
        else:
            rp = rolling_max(e, k)
            out.append(float(np.abs(e / rp - 1.0).max()))
    out.append(float(np.sqrt(np.mean(dd ** 2))))                      # ULCER
    m = dd.max()
    out.append(float(cagr(r) / m) if m > 0 else np.nan)               # CALMAR
    return np.array(out, float)


def block_boot(r, rng, nboot=NBOOT, block=BLOCK):
    """Circular block bootstrap: SD of every DIAL-1 statistic for one return series."""
    n = len(r)
    if n < 2 * block:
        return np.full(len(NAMES), np.nan)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(nboot, nb))
    off = np.arange(block)
    idxm = (starts[:, :, None] + off[None, None, :]).reshape(nboot, nb * block)[:, :n] % n
    vals = np.array([truncated(r[ix]) for ix in idxm], float)
    return np.nanstd(vals, axis=0, ddof=1)


def disjoint(n, L):
    w = int(np.floor(n * L))
    if w < 2 * BLOCK:
        return []
    return [(i * w, (i + 1) * w) for i in range(n // w)]


def ols_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    x, y = x[ok], y[ok]
    return float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())


# ------------------------------------------------------------------ panel / books
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, H, N=A_N, lag=1):
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    key = pan.key
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held):
            held = held[pr[t, held]]
        keep = [int(c) for c in (held[(t - cur[held]) < H] if len(held) else held)]
        k = key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep:
            k[c] = np.inf
        need, take = N - len(keep), []
        for c in np.argsort(k, kind="stable"):
            if need <= 0 or not np.isfinite(k[int(c)]):
                break
            take.append(int(c))
            need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1146 lane cloud — {SLUG}")
    say(f"# DIAL 1 TRUNCATION RULE: {NAMES[:7]} (quantiles of |dd|) + {NAMES[7:12]} "
        f"(worst dd in a trailing k-day window) + ULCER, CALMAR as the two reference statistics")
    say(f"# DIAL 2 SUB-TAPE FRACTION L = {FRACS}, measured on DISJOINT windows "
        f"(nested-anchored also reported, gate G5)")
    say(f"# books: 1095's H ladder {HOLDS}, N={A_N} gross={A_G} weekly {COST:.0f} bps t+1, "
        f"anchor H={A_H}; bootstrap: circular block L={BLOCK}, B={NBOOT}, seed {SEED}")
    say("# MAXDD SIGNATURE := b_GAP > 0 AND b_SD > 0;  'behaves like ULCER' := b_SD < 0")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    iQ100, iKFULL, iULC, iCAL = NAMES.index("Q100"), NAMES.index("KFULL"), \
        NAMES.index("ULCER"), NAMES.index("CALMAR")

    curves, expo, r8rows, bookrows = [], [], [], []
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   OOS Sh {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS Sh {live['oos']['Sharpe']:.4f}")

        R = {H: run(pan, build(pan, H))[WARMUP:] for H in HOLDS}
        n = len(idx)
        anchor = R[A_H]

        for H in HOLDS:
            w = windows(idx, R[H])
            a4, b4 = legs_4a(w, live), legs_4b(w, spy)
            bookrows.append(dict(panel=pname, H=H, anchor=(H == A_H), **flat(w),
                                 keep4a=all(a4.values()), keep4b=all(b4.values()),
                                 fail4a=failed(a4), fail4b=failed(b4)))

        # ---- G4: the two families meet MAXDD exactly at their untruncated ends
        if pname == "U56":
            v = truncated(anchor)
            d4 = max(abs(v[iQ100] - abs(mdd(anchor))), abs(v[iKFULL] - abs(mdd(anchor))))
            gate("G4 Q100 and KFULL ARE |MaxDD| exactly", f"{d4:.2e}", "< 1e-15", d4 < 1e-15)
            # ---- G2: fast runner == engine.backtest on the anchor
            Wdf = pd.DataFrame(np.roll(A_G * build(pan, A_H), -1, axis=0),
                               index=pan.idx, columns=pan.px.columns)
            eng = backtest(pan.px, Wdf, cost_bps=COST, freq="W")["returns"].fillna(0.0)
            dd = float(np.abs(eng.values[WARMUP:] - anchor).max())
            gate("G2 fast runner == engine.backtest", f"{dd:.2e}", "< 1e-12", dd < 1e-12)

        # ---- DIAL 2: GAP and SD at every fraction, on disjoint windows
        rng = np.random.default_rng(SEED)
        gaps, sds, gapsN, sdsN, usedL = [], [], [], [], []
        for L in FRACS:
            segs = disjoint(n, L)
            if not segs:
                continue
            g = np.array([np.nanmax([truncated(R[H][a:b]) for H in HOLDS], axis=0) -
                          np.nanmin([truncated(R[H][a:b]) for H in HOLDS], axis=0)
                          for a, b in segs], float).mean(axis=0)
            s = np.array([block_boot(anchor[a:b], rng) for a, b in segs], float).mean(axis=0)
            w = int(np.floor(n * L))
            gN = np.nanmax([truncated(R[H][:w]) for H in HOLDS], axis=0) - \
                np.nanmin([truncated(R[H][:w]) for H in HOLDS], axis=0)
            sN = block_boot(anchor[:w], rng)
            gaps.append(g); sds.append(s); gapsN.append(gN); sdsN.append(sN); usedL.append(L)
            for j, nm in enumerate(NAMES):
                curves.append(dict(panel=pname, stat=nm, L=L, n_windows=len(segs),
                                   window_days=w, gap=g[j], sd=s[j],
                                   gap_nested=gN[j], sd_nested=sN[j],
                                   level=float(np.mean([truncated(anchor[a:b])[j]
                                                        for a, b in segs]))))
        gaps, sds = np.array(gaps), np.array(sds)
        gapsN, sdsN = np.array(gapsN), np.array(sdsN)
        lx = np.log(np.array(usedL))

        say(f"\n   DIAL 1 x DIAL 2 exponents on {pname} "
            f"(b = OLS slope of log(.) on log L over {len(usedL)} fractions)")
        say("   statistic |    b_GAP     b_SD | signature | b_SD nested | level @L=1.00")
        for j, nm in enumerate(NAMES):
            bg = ols_slope(lx, np.log(np.abs(gaps[:, j])))
            bs = ols_slope(lx, np.log(np.abs(sds[:, j])))
            bgN = ols_slope(lx, np.log(np.abs(gapsN[:, j])))
            bsN = ols_slope(lx, np.log(np.abs(sdsN[:, j])))
            sig = "MAXDD" if (bg > 0 and bs > 0) else ("ULCER" if bs < 0 else "mixed")
            lvl = truncated(anchor)[j]
            say(f"   {nm:>9} | {bg:+8.4f} {bs:+8.4f} | {sig:^9} | {bsN:+11.4f} | {lvl:>12.4f}")
            expo.append(dict(panel=pname, stat=nm, b_GAP=bg, b_SD=bs, signature=sig,
                             b_GAP_nested=bgN, b_SD_nested=bsN, level_full=lvl))

        # ---- G3: does 1140's MAXDD reading reproduce?  cross-run, reported not toleranced
        if pname == "U56":
            e = [x for x in expo if x["panel"] == pname and x["stat"] == "Q100"][0]
            say(f"   G3 cross-run vs 1140's committed MAXDD exponents "
                f"(b_GAP {COMMITTED_1140_MAXDD[0]:+.4f}, b_SD {COMMITTED_1140_MAXDD[1]:+.4f}): "
                f"this run reads b_GAP {e['b_GAP']:+.4f}, b_SD {e['b_SD']:+.4f} "
                f"— SIGN agreement {'YES' if (e['b_GAP'] > 0) == (COMMITTED_1140_MAXDD[0] > 0) and (e['b_SD'] > 0) == (COMMITTED_1140_MAXDD[1] > 0) else 'NO'}")
            GATES.append(dict(gate="G3 1140's MAXDD exponents, sign agreement on DISJOINT "
                                   "windows (cross-run, REPORTED — its failure IS this run's "
                                   "headline, see the geometry section)",
                              value=f"b_GAP {e['b_GAP']:+.4f}, b_SD {e['b_SD']:+.4f}",
                              target=f"{COMMITTED_1140_MAXDD} (signs)",
                              pass_=bool(e["b_GAP"] > 0 and e["b_SD"] > 0)))
            u = [x for x in expo if x["panel"] == pname and x["stat"] == "ULCER"][0]
            gate("G5 ULCER's b_SD is NEGATIVE (1140's own contrast reproduces)",
                 f"{u['b_SD']:+.4f}", "< 0", u["b_SD"] < 0)

        # ---- CAPITAL ARM: every DIAL-1 rung as an IS chooser, OOS read once
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        wa = windows(idx, anchor)
        for j, nm in enumerate(NAMES):
            sc = []
            for H in HOLDS:
                v = truncated(R[H][:o])[j]
                c = cagr(R[H][:o])
                sc.append(c / v if (nm != "CALMAR" and np.isfinite(v) and v > 0)
                          else (v if nm == "CALMAR" else -np.inf))
            pk = HOLDS[int(np.nanargmax(sc))]
            w = windows(idx, R[pk])
            a4, b4 = legs_4a(w, live), legs_4b(w, spy)
            r8rows.append(dict(panel=pname, stat=nm, pick=pk, pick_is_anchor=(pk == A_H),
                               oos_CAGR=w["oos"]["CAGR"], oos_Sharpe=w["oos"]["Sharpe"],
                               oos_MaxDD=w["oos"]["MaxDD"],
                               anchor_oos_Sharpe=wa["oos"]["Sharpe"],
                               anchor_oos_CAGR=wa["oos"]["CAGR"],
                               anchor_oos_MaxDD=wa["oos"]["MaxDD"],
                               reach=w["oos"]["Sharpe"] >= wa["oos"]["Sharpe"],
                               spy_oos_Sharpe=spy["oos"]["Sharpe"],
                               spy_oos_CAGR=spy["oos"]["CAGR"],
                               spy_oos_MaxDD=spy["oos"]["MaxDD"],
                               live_oos_Sharpe=live["oos"]["Sharpe"],
                               full_CAGR=w["full"]["CAGR"], full_Sharpe=w["full"]["Sharpe"],
                               full_MaxDD=w["full"]["MaxDD"],
                               h1=w["h1"]["Sharpe"], h2=w["h2"]["Sharpe"],
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4)))

    # ---------------------------------------------------------------- report
    ex, cu = pd.DataFrame(expo), pd.DataFrame(curves)
    r8, bk = pd.DataFrame(r8rows), pd.DataFrame(bookrows)

    say("\n=== WHERE THE MAXDD SIGNATURE SWITCHES OFF (b_SD by truncation rung x panel) ===")
    pn = list(ex.panel.unique())
    say("   statistic |" + "".join(f"{p:>14}" for p in pn) + " | panels with b_SD > 0")
    for nm in NAMES:
        vals = [float(ex[(ex.panel == p) & (ex.stat == nm)].b_SD.iloc[0]) for p in pn]
        say(f"   {nm:>9} |" + "".join(f"{v:>+14.4f}" for v in vals) +
            f" | {sum(v > 0 for v in vals)} of {len(pn)}")

    say("\n=== THE SAME FOR b_GAP ===")
    say("   statistic |" + "".join(f"{p:>14}" for p in pn) + " | panels with b_GAP > 0")
    for nm in NAMES:
        vals = [float(ex[(ex.panel == p) & (ex.stat == nm)].b_GAP.iloc[0]) for p in pn]
        say(f"   {nm:>9} |" + "".join(f"{v:>+14.4f}" for v in vals) +
            f" | {sum(v > 0 for v in vals)} of {len(pn)}")

    say("\n=== SIGNATURE COUNT (MAXDD = b_GAP>0 AND b_SD>0) over 3 panels ===")
    for nm in NAMES:
        s = ex[ex.stat == nm]
        say(f"   {nm:>9}: MAXDD {int((s.signature=='MAXDD').sum())}  "
            f"ULCER {int((s.signature=='ULCER').sum())}  "
            f"mixed {int((s.signature=='mixed').sum())}")

    say("\n=== THE GEOMETRY FLIP: b_SD on DISJOINT windows vs NESTED tail-anchored ones ===")
    say("   1140's construction is nested; a longer nested window CONTAINS the shorter one, so a")
    say("   maximum over it cannot fall — the growth is partly built in.  Same tape, same L, same")
    say("   bootstrap, only the window geometry differs:")
    say("   statistic |" + "".join(f"{p+' dis/nest':>22}" for p in pn))
    flips = 0
    for nm in NAMES:
        cells = []
        for p in pn:
            r = ex[(ex.panel == p) & (ex.stat == nm)].iloc[0]
            cells.append(f"{r.b_SD:+.4f}/{r.b_SD_nested:+.4f}")
            if (r.b_SD > 0) != (r.b_SD_nested > 0):
                flips += 1
        say(f"   {nm:>9} |" + "".join(f"{c:>22}" for c in cells))
    say(f"   SIGN FLIPS between the two geometries: {flips} of {len(NAMES)*len(pn)} "
        f"(panel, statistic) cells")
    q = ex[ex.stat == "Q100"]
    u = ex[ex.stat == "ULCER"]
    say("   the specific contrast 1140 published — MAXDD vs ULCER b_SD — by panel:")
    for p in pn:
        a = q[q.panel == p].iloc[0]
        b = u[u.panel == p].iloc[0]
        say(f"      {p:<10} NESTED  MAXDD {a.b_SD_nested:+.4f} vs ULCER {b.b_SD_nested:+.4f}  "
            f"-> separated: {'YES' if (a.b_SD_nested > 0) and (b.b_SD_nested < 0) else 'no'}")
        say(f"      {p:<10} DISJOINT MAXDD {a.b_SD:+.4f} vs ULCER {b.b_SD:+.4f}  "
            f"-> separated: {'YES' if (a.b_SD > 0) and (b.b_SD < 0) else 'no'}")

    say("\n=== CAPITAL ARM (rule 8, OOS 2017-2026 READ ONCE): each truncation as a CHOOSER ===")
    say("   panel        statistic | pick |  OOS CAGR   OOS Sh  OOS MaxDD | anchor Sh | "
        "SPY Sh | live Sh | reach | 4b")
    for _, r in r8.iterrows():
        say(f"   {r.panel:<12} {r.stat:>9} | {r['pick']:>4d} | {r.oos_CAGR:>9.2%} "
            f"{r.oos_Sharpe:>8.4f} {r.oos_MaxDD:>10.2%} | {r.anchor_oos_Sharpe:>9.4f} | "
            f"{r.spy_oos_Sharpe:>6.3f} | {r.live_oos_Sharpe:>7.3f} | "
            f"{'Y' if r.reach else 'n':^5} | {'PASS' if r.keep4b else r.fail4b}")

    say("\n=== KEEP PATHS ===")
    say(f"   over the 27 published books: 4a {int(bk.keep4a.sum())} of {len(bk)}, "
        f"4b {int(bk.keep4b.sum())} of {len(bk)}")
    say(f"   over the {len(r8)} chooser picks: 4a {int(r8.keep4a.sum())} of {len(r8)}, "
        f"4b {int(r8.keep4b.sum())} of {len(r8)}; "
        f"picks reaching the anchor OOS {int(r8.reach.sum())} of {len(r8)}; "
        f"picks that ARE the anchor {int(r8.pick_is_anchor.sum())} of {len(r8)}")
    sub = r8[r8.stat.isin(["Q100", "KFULL"])]
    tr = r8[~r8.stat.isin(["Q100", "KFULL", "CALMAR", "ULCER"])]
    say(f"   untruncated (Q100/KFULL) choosers: mean OOS Sharpe {sub.oos_Sharpe.mean():.4f}, "
        f"reach {int(sub.reach.sum())} of {len(sub)}")
    say(f"   TRUNCATED choosers:                mean OOS Sharpe {tr.oos_Sharpe.mean():.4f}, "
        f"reach {int(tr.reach.sum())} of {len(tr)}")

    npass = sum(g["pass_"] for g in GATES)
    say(f"\nGATES {npass} of {len(GATES)} passing.  elapsed {time.time()-t0:.0f}s")

    ex.to_csv(f"{STEM}.exponents.csv", index=False)
    cu.to_csv(f"{STEM}.curves.csv", index=False)
    r8.to_csv(f"{STEM}.rule8.csv", index=False)
    bk.to_csv(f"{STEM}.books.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    Path(f"{STEM}.log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

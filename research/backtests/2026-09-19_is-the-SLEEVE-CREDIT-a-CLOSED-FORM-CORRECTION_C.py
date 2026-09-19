#!/usr/bin/env python3
"""
Idea 1551 (lane C, 2026-09-19) — is the SLEEVE CREDIT a CLOSED-FORM CORRECTION?

THE CLAIM UNDER TEST.  Idea 1358's memo (clause 2) says the credit from paying the de-grossed
residual a coupon instead of 0% "is not alpha, it is a measurement correction ... and it scales
with (1 - gross)".  Idea 1498 re-found the same credit on an independent grid.  The queue's
wording of THIS idea is exact and is what is tested first:

    measured dCAGR  ==?  realised-mean-sleeve-weight  x  CAGR(sleeve)

If some closed form reproduces the credit, the whole (SLEEVE, GROSS) axis retires as ARITHMETIC:
no future run need spend a backtest on it.  If it does not, the axis stays empirical and every
future de-grossed book still has to be re-run with its sleeve.

FOUR CANDIDATE FORMS, A LADDER FROM CHEAPEST TO EXACT.  None has a free parameter; nothing is
fitted, so PROTOCOL rule 4's 2-parameter budget is untouched (the two published dials are SLEEVE
and GROSS, as in idea 1358).

  F_A  NOMINAL      dCAGR ~ (1 - g) * CAGR_sleeve
                    the memo's literal "scales with (1 - gross)".  Needs one scalar.
  F_B  REALISED     dCAGR ~ sbar * CAGR_sleeve,  sbar = realised mean daily sleeve weight
                    the queue's literal wording.  Needs one scalar the cash book already knows.
  F_C  COMPOUNDED   dCAGR ~ (1 + CAGR_cash) * sbar * CAGR_sleeve - d(drag)
                    F_B plus the two terms arithmetic says must be there: the credit compounds
                    on top of the book it is added to, and the sleeve leg pays its own 10 bps.
  F_E  GROWTH-RATE  the same as F_C in LOG space, plus the term a fixed-weight mix must carry:
                    dlog = (1-g)*log(1+CAGR_s) + g*(1-g)*(var_s/2 - cov(core, sleeve)).  Every
                    input is readable off the CASH book and the sleeve series; no sleeve book.
  F_D  MIX IDENTITY the (SLEEVE, GROSS) book IS, exactly, the weekly-rebalanced TWO-ASSET MIX of
                    (i) the CORE book at gross 1.00 and (ii) the sleeve, held at (g, 1-g), with
                    costs charged on the mix's own turnover vector.  Needs no scalar at all: it
                    reconstructs the whole daily return path, hence CAGR, Sharpe AND MaxDD.

F_D is the decisive one.  F_A / F_B / F_C are scalar summaries and can only ever be approximate;
F_D either reproduces the direct run to machine precision or it does not.  It is implemented as a
SEPARATE RUNNER that never touches the panel's price matrix except through two stored objects per
rebalance window (the core's target vector and its drifted proportion vector) plus the sleeve's
own return series — i.e. exactly the information a future run would have WITHOUT re-running the
book.  Its residual against the direct runner is gate G3.

THE BOOK, OTHERWISE FROZEN (idea 1358's, unchanged).  3-leg rank composite ((21,252), (0,126),
(0,63)) x the 0.5 + 0.5*above-200d tilt; eligibility = above the 200d MA AND vol20 < 0.60;
N = 15 equal-weighted names; minimum hold H = 126 trading days; weekly cadence; decisions lagged
one row and applied at t+1 (rule 2); 10 bps per unit turnover on EVERY leg including the sleeve.

THE GRID, EVERY CELL PUBLISHED.  SLEEVE {CASH, SHY, IEF, TLT} x GROSS {0.40, 0.50, 0.60, 0.75,
0.90} on PANEL {U56, B136, SMALL} = 60 cells.  0.60 and CASH are the frozen incumbent's values.
GROSS reaches wider than idea 1358's {0.50, 0.60, 0.75} deliberately: a closed form that only
holds over a 25-point window of gross is not a closed form.

THE CAPITAL ARM (this is not a census).  All 60 cells are real books scored on both KEEP paths,
full sample and OOS, against SPY, the live RULES v2 baseline and the frozen (CASH, 0.60)
incumbent.  Rule 8 is run three ways, and the third is the idea's own operational question:

  C_GRID   pick (SLEEVE, GROSS) on warm-up..2016 by IS Sharpe over all 60 DIRECT books.
  C_RECON  the same pick made from F_D's reconstructions only — 3 core books and 3 sleeve series
           instead of 60 books.  If it picks the same cell, the axis is retired OPERATIONALLY.
  C_CHEAP  the same pick made from the CASH ladder plus F_B alone, with the sleeve assumed to
           leave vol untouched: Sharpe ~ (CAGR_cash + sbar*CAGR_sleeve) / vol_cash.
All three are read on 2017-2026 ONCE and scored against doing nothing (the frozen incumbent).

COMPARANDS (rule 3): live RULES v2 at 10 bps weekly, SPY buy-and-hold, frozen (CASH, 0.60).
PROTOCOL: rule 1 (>=10y), rule 2 (t+1, 10 bps, no leverage/shorting), rule 3, rule 4 (both KEEP
paths, no tuned parameter), rule 8 (walk-forward), rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G1 cross-script replay of idea 1358/1296/1346's committed (CASH, 0.60) anchor on all
three panels.  G2 no leverage (weight sum never exceeds 1).  G3 F_D vs the direct runner, daily
returns, all 60 cells.  G4 the CASH cells' F_D residual specifically (the sleeve-is-a-0%-asset
degenerate case).  G5 sbar's own identity check against the nominal (1-g).  G6 tape stamp / rule 1.
G7 the sleeve standalone series joined onto each panel is that panel's own column where priced.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_is-the-SLEEVE-CREDIT-a-CLOSED-FORM-CORRECTION_C.py
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
SLUG = "is-the-SLEEVE-CREDIT-a-CLOSED-FORM-CORRECTION"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H = 15, 126
COST = 10.0
CADENCE = "W"
SLEEVES = ["CASH", "SHY", "IEF", "TLT"]
GROSSES = [0.40, 0.50, 0.60, 0.75, 0.90]
ANCHOR_SLV, ANCHOR_G = "CASH", 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# Committed by lane cloud's idea-1296 / idea-1346 / idea-1358 scripts.  Cross-script gate G1.
C_ANCHOR = {
    "U56": dict(CAGR=0.1367020011892825, Sharpe=1.17166235540161, MaxDD=-0.163814812515476,
                H1=1.2526855979053693, H2=1.121880836109541, turn=2.463043347965852),
    "B136": dict(CAGR=0.1343474037905223, Sharpe=1.0630027470342966, MaxDD=-0.1597051532314095,
                 H1=1.2318389322712402, H2=0.9406397253110836, turn=2.6461090252500337),
    "SMALL": dict(CAGR=0.0753535266944089, Sharpe=0.5569518940285322, MaxDD=-0.3263346826561878,
                  H1=0.8125393414921002, H2=0.358407645038224, turn=3.407055866031751),
}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=value, target="published, not asserted", pass_=True))


# ----------------------------------------------------------------------------- the frozen book
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


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad).shift(1, fill_value=False).values.copy()
    m[0] = True
    return np.flatnonzero(m)


class Panel:
    def __init__(self, name, px, invest, sleeve_px):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.reb = cadence_rows(px.index, CADENCE)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        s = sleeve_px.reindex(px.index, method="ffill")
        self.sret = {c: s[c].pct_change().fillna(0.0).values for c in s.columns}
        self.sret["CASH"] = np.zeros(len(px.index))
        # cached cumulative products for the DIRECT runner (built once per panel)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def build1(pan, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0 (rule 2 lag).  Independent of the
    gross and of the sleeve, which is exactly why (SLEEVE, GROSS) is a clean pair of dials."""
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


def run_direct(pan, frame, gross, sname):
    """GROUND TRUTH.  Idea 1358's runner, verbatim in behaviour: residual (1 - gross) goes to a
    0% cash line when sname == 'CASH', otherwise to the sleeve, which is an ordinary long asset —
    it drifts, it is rebalanced on the same weekly grid and it pays the same 10 bps on its own
    turnover.  Weights never sum above 1 (no leverage, no shorting).

    Returns (gross daily return, turnover, weight-sum at rebalances, daily sleeve weight)."""
    rets = pan.rets
    T, M = rets.shape
    cash_leg = (sname == "CASH")
    sret = None if cash_leg else np.asarray(pan.sret[sname], float)
    if cash_leg:
        C, Cp = pan.C, pan.Cp
        extra = 0
    else:
        sc = np.cumprod(1.0 + sret)
        C = np.hstack([pan.C, sc.reshape(-1, 1)])
        Cp = np.vstack([np.ones((1, M + 1)), C[:-1]])
        aug_last = sret
        extra = 1
    aug = rets if cash_leg else np.hstack([rets, aug_last.reshape(-1, 1)])
    turn = np.zeros(T)
    out = np.zeros(T)
    wsum = np.zeros(T)
    slw = np.zeros(T)
    curw = np.zeros(M + extra)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = np.zeros(M + extra)
        w0[:M] = gross * frame[i0]
        if extra:
            w0[M] = 1.0 - gross
        wsum[i0] = w0.sum()
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * aug[i0:i1]).sum(axis=1)
        # realised daily weight of the RESIDUAL: the sleeve column when there is one, and the
        # 0% cash line c0 when there is not, so sbar is defined at every cell on the grid.
        slw[i0:i1] = (A[:, M] / V) if extra else (c0 / V)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, wsum, slw


# ------------------------------------------------------- F_D: the two-asset MIX reconstruction
def core_object(pan, frame):
    """Everything F_D is allowed to know about the panel, extracted from ONE run of the CORE
    book at gross 1.00.  Per rebalance window: the target vector (sparse), the drifted proportion
    vector at window end (sparse), the core's within-window NAV factor path (start-of-day) and
    its end-of-window factor.  Plus the core's own daily return and turnover at gross 1.00.

    No price matrix, no score, no eligibility, no min-hold state leaves this function."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    cdaily = np.zeros(T)
    Gpath = np.ones(T)          # core NAV factor at the START of day t, rebased each window
    wins = []
    for i0, i1 in zip(reb, ends):
        w0 = frame[i0]
        idx = np.flatnonzero(w0)
        if len(idx) == 0:
            wins.append(dict(i0=int(i0), i1=int(i1), tidx=np.empty(0, np.int64),
                             tw=np.empty(0), pidx=np.empty(0, np.int64), pw=np.empty(0),
                             Gend=1.0, invested=False))
            Gpath[i0:i1] = 1.0
            continue
        base = Cp[i0, idx]
        A = w0[idx][None, :] * (Cp[i0:i1, idx] / base[None, :])
        V = A.sum(axis=1)
        cdaily[i0:i1] = (A * rets[i0:i1, idx]).sum(axis=1) / V
        Gpath[i0:i1] = V
        Ae = w0[idx] * (C[i1 - 1, idx] / base)
        wins.append(dict(i0=int(i0), i1=int(i1), tidx=idx.copy(), tw=w0[idx].copy(),
                         pidx=idx.copy(), pw=(Ae / Ae.sum()).copy(),
                         Gend=float(Ae.sum()), invested=True))
    return dict(cdaily=cdaily, Gpath=Gpath, wins=wins, T=T)


def run_recon(core, sret, gross, cash_leg=False):
    """F_D.  The (SLEEVE, GROSS) book rebuilt as the weekly two-asset mix of the CORE book and
    the sleeve at (g, 1-g), charging 10 bps on the mix's own turnover vector.  Touches the panel
    only through `core` (built once, sleeve- and gross-free) and the sleeve's return series.

    cash_leg=True is the incumbent's convention and NOT a free choice: a 0% cash line is not a
    traded instrument, so the record's runner charges no turnover on it, while a bond-ETF sleeve
    is traded and pays the same 10 bps as everything else.  The mix identity has to carry that
    asymmetry or it is reconstructing a different book."""
    T = core["T"]
    g = float(gross)
    sret = np.asarray(sret, float)
    sc = np.cumprod(1.0 + sret)
    scp = np.concatenate([[1.0], sc[:-1]])
    out = np.zeros(T)
    turn = np.zeros(T)
    slw = np.zeros(T)
    prev_idx, prev_w, prev_s = np.empty(0, np.int64), np.empty(0), 0.0
    for w in core["wins"]:
        i0, i1 = w["i0"], w["i1"]
        Gc = core["Gpath"][i0:i1]                       # core NAV factor, start of day
        Gs = scp[i0:i1] / scp[i0]                       # sleeve factor, start of day
        vc, vs = g * Gc, (1.0 - g) * Gs
        nav = vc + vs
        out[i0:i1] = (vc * core["cdaily"][i0:i1] + vs * sret[i0:i1]) / nav
        slw[i0:i1] = vs / nav
        # turnover of the mix at the rebalance that OPENS this window
        tgt_i, tgt_w = w["tidx"], g * w["tw"]
        tt = 0.0
        if len(prev_idx) or len(tgt_i):
            allc = np.union1d(prev_idx, tgt_i)
            a = np.zeros(len(allc))
            b = np.zeros(len(allc))
            if len(tgt_i):
                a[np.searchsorted(allc, tgt_i)] = tgt_w
            if len(prev_idx):
                b[np.searchsorted(allc, prev_idx)] = prev_w
            tt = float(np.abs(a - b).sum())
        if not cash_leg:
            tt += abs((1.0 - g) - prev_s)     # the sleeve is traded; a 0% cash line is not
        turn[i0] = tt
        # drifted NAV-normalised weights at the END of this window, for the next rebalance
        Gce = w["Gend"] if w["invested"] else 1.0
        Gse = sc[i1 - 1] / scp[i0]
        vce, vse = g * Gce, (1.0 - g) * Gse
        nave = vce + vse
        prev_s = vse / nave
        if w["invested"]:
            prev_idx, prev_w = w["pidx"], (vce / nave) * w["pw"]
        else:
            prev_idx, prev_w = np.empty(0, np.int64), np.empty(0)
    return out, turn, slw


# ------------------------------------------------------------------------------------ measures
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


def annvol(r):
    return float(np.std(np.asarray(r, float), ddof=0) * np.sqrt(252))


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


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


BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919


def paired_block_dcagr(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    """SE of (CAGR(a) - CAGR(b)) under a PAIRED circular block bootstrap (identical block starts
    for both series, so the pairing survives).  Returns (observed, SE, t)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def cg(X):
        return np.exp(np.log1p(X).sum(axis=1) * 252.0 / n) - 1.0

    d = cg(A) - cg(B)
    obs = float(cagr(a) - cagr(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


# ---------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 126)
    say("IDEA 1551 (lane C, 2026-09-19) — is the SLEEVE CREDIT a CLOSED-FORM CORRECTION?")
    say("FORMS: F_A (1-g)*CAGR_s | F_B sbar*CAGR_s | F_C (1+CAGR_cash)*sbar*CAGR_s - d(drag) | "
        "F_D exact two-asset MIX identity.  No fitted parameter.")
    say("DIALS (published, not tuned): SLEEVE {CASH,SHY,IEF,TLT} x GROSS "
        "{0.40,0.50,0.60,0.75,0.90} on 3 panels = 60 cells.")
    say("=" * 126)

    raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
    sleeve_px = raw[["SHY", "IEF", "TLT"]].ffill()

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = ROOT / "data" / "small_meta.csv"
    if meta.exists():
        md = pd.read_csv(meta)
        col = "ticker" if "ticker" in md.columns else md.columns[0]
        bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
        say(f"  SMALL filter: data/small_meta.csv drops {len(bad)} tickers with "
            f"max_1d_move >= 1.0 (protocol-mandated).")
    else:
        bad = set()
        say("  SMALL filter: data/small_meta.csv absent; in-panel max |1d move| >= 1.0 screen.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"], sleeve_px),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"], sleeve_px),
              Panel("SMALL", pxS, inv, sleeve_px)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a "
        "sub-$2B screen carried back to 2010, so its LEVELS are an upper bound.  This run reads "
        "CONTRASTS (sleeve minus cash at the same gross) and a RESIDUAL (measured minus "
        "predicted), both of which difference the survivorship term away.  The sleeve tickers "
        "SHY/IEF/TLT are survivorship-free.")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}",
                f"{len(p.idx)} rows, {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G6 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    devs = {}
    for pn in panels:
        d = [float(np.nanmax(np.abs(pn.px[c].pct_change().fillna(0.0).values - pn.sret[c])))
             for c in ["SHY", "IEF", "TLT"] if c in pn.px.columns]
        devs[pn.name] = max(d) if d else None
    gate("G7a joined sleeve returns == U56's own columns (same source file, must be exact)",
         f"{devs['U56']:.3e}", "< 1e-12", devs["U56"] < 1e-12)
    gate("G7b B136's own sleeve columns are the same instruments at a different cache vintage "
         "(idea 353's standing finding: data/prices_broad.csv is a raw yf.download)",
         f"{devs['B136']:.3e}", "< 1e-3 (bounded, not zero)", devs["B136"] < 1e-3)
    publish("G7c SMALL prices no sleeve ticker (no overlap to check)", str(devs["SMALL"]))

    say("\n  THE SLEEVES THEMSELVES (buy-and-hold, each panel's own window, post-warm-up) — the "
        "CAGR_s that every closed form multiplies:")
    sleeve_cagr = {}
    for p in panels:
        i_oos = int(np.searchsorted(p.idx.values, np.datetime64(OOS_START)))
        for c in ["SHY", "IEF", "TLT"]:
            r = p.sret[c][WARMUP:]
            m = triple(r)
            mo = triple(p.sret[c][i_oos:])
            sleeve_cagr[(p.name, c)] = (m["CAGR"], mo["CAGR"])
            say(f"    {p.name:>6} {c}: CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:7.4f} MaxDD "
                f"{m['MaxDD']:7.2%} vol {annvol(r):5.2%}  |  OOS (2017+, contains 2022) "
                f"{mo['CAGR']:6.2%}/{mo['Sharpe']:7.4f}/{mo['MaxDD']:7.2%}")
            publish(f"SLEEVE STANDALONE {p.name} {c}",
                    f"CAGR {m['CAGR']:.6f} OOS_CAGR {mo['CAGR']:.6f}")
        sleeve_cagr[(p.name, "CASH")] = (0.0, 0.0)

    SPY_CAGR = {}
    grid, cf_rows, wf_rows, recon_rows = [], [], [], []
    max_wsum = 0.0
    max_recon_all, max_recon_cash = 0.0, 0.0

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = i_oos                                    # IS = warm-up .. 2016-12-31
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        SPY_CAGR[pan.name] = spy["CAGR"]
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        frame = build1(pan, I_N, I_H)
        core = core_object(pan, frame)

        say(f"\n  [{pan.name}]  SPY full {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%},"
            f" CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.4f}/{live['H2']:.4f}  |  OOS SPY "
            f"{spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  OOS live "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        cells = {}
        say(f"    {'sleeve':>6} {'gross':>5} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} "
            f"{'H2':>6} | {'sbar':>6} {'turn':>5} {'drag':>6} | {'OOSCAGR':>8} {'OOSShrp':>7} "
            f"{'OOSMaxDD':>8} | {'ISShrp':>7} | {'F_Dres':>9} | 4a 4b  fail-legs")
        for slv in SLEEVES:
            for g_ in GROSSES:
                gg, tu, wsum, slw = run_direct(pan, frame, g_, slv)
                rr = gg - tu * COST / 1e4
                # F_D: the same book rebuilt from the core object + the sleeve series alone
                gg2, tu2, slw2 = run_recon(core, pan.sret[slv], g_, cash_leg=(slv == "CASH"))
                rr2 = gg2 - tu2 * COST / 1e4
                res_d = float(np.max(np.abs(rr - rr2)))
                max_recon_all = max(max_recon_all, res_d)
                if slv == "CASH":
                    max_recon_cash = max(max_recon_cash, res_d)
                act = wsum[np.asarray(pan.reb, dtype=np.int64)]
                max_wsum = max(max_wsum, float(np.max(act)))

                r, rO = rr[WARMUP:], rr[i_oos:]
                k4a, k4b, m, h1, h2, legs = keep_paths(r, spy, live)
                k4aO, k4bO, mO, h1O, h2O, legsO = keep_paths(rO, spyO, liveO)
                sbar = float(np.mean(slw[WARMUP:]))
                turn = annturn(tu, WARMUP, n)
                row = dict(panel=pan.name, sleeve=slv, gross=g_,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           vol=annvol(r), sbar=sbar, sbar_oos=float(np.mean(slw[i_oos:])),
                           turn=turn, drag_bp=turn * COST,
                           OOS_CAGR=mO["CAGR"], OOS_Sharpe=mO["Sharpe"], OOS_MaxDD=mO["MaxDD"],
                           IS_Sharpe=sharpe(rr[WARMUP:i_is]), IS_CAGR=cagr(rr[WARMUP:i_is]),
                           IS_vol=annvol(rr[WARMUP:i_is]),
                           IS_sbar=float(np.mean(slw[WARMUP:i_is])),
                           keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                           fail_legs=",".join(k for k, v in legs.items() if not v) or "-",
                           fail_legs_oos=",".join(k for k, v in legsO.items() if not v) or "-",
                           FD_resid_daily=res_d,
                           FD_CAGR=float(cagr(rr2[WARMUP:])),
                           FD_dCAGR=float(cagr(rr2[WARMUP:]) - m["CAGR"]),
                           FD_dSharpe=float(sharpe(rr2[WARMUP:]) - m["Sharpe"]),
                           FD_dMaxDD=float(mdd(rr2[WARMUP:]) - m["MaxDD"]),
                           script=f"{DATE}_{SLUG}_C.py")
                grid.append(row)
                recon_rows.append(dict(panel=pan.name, sleeve=slv, gross=g_,
                                       max_abs_daily_resid=res_d,
                                       dCAGR=row["FD_dCAGR"], dSharpe=row["FD_dSharpe"],
                                       dMaxDD=row["FD_dMaxDD"],
                                       turnover_direct=turn,
                                       turnover_recon=annturn(tu2, WARMUP, n)))
                cells[(slv, g_)] = dict(row=row, net=rr)
                say(f"    {slv:>6} {g_:5.2f} | {m['CAGR']:6.2%} {m['Sharpe']:7.4f} "
                    f"{m['MaxDD']:7.2%} {h1:6.3f} {h2:6.3f} | {sbar:6.3f} {turn:5.2f} "
                    f"{turn*COST:5.1f}b | {mO['CAGR']:7.2%} {mO['Sharpe']:7.4f} "
                    f"{mO['MaxDD']:7.2%} | {row['IS_Sharpe']:7.4f} | {res_d:9.2e} | "
                    f"{'Y' if k4a else 'n'}  {'Y' if k4b else 'n'}   {row['fail_legs']}")

        # ---- G1 cross-script replay of the frozen anchor -------------------------------------
        a = cells[(ANCHOR_SLV, ANCHOR_G)]["row"]
        ca = C_ANCHOR[pan.name]
        dev = max(abs(a["CAGR"] - ca["CAGR"]), abs(a["Sharpe"] - ca["Sharpe"]),
                  abs(a["MaxDD"] - ca["MaxDD"]), abs(a["H1"] - ca["H1"]),
                  abs(a["H2"] - ca["H2"]), abs(a["turn"] - ca["turn"]))
        gate(f"G1 {pan.name} (CASH, 0.60) replays ideas 1296/1346/1358's committed anchor",
             f"{dev:.3e}", "< 5e-6", dev < 5e-6)

        # ---- the closed forms, cell by cell --------------------------------------------------
        say(f"\n    CLOSED FORMS on {pan.name} — measured dCAGR (sleeve cell minus the CASH cell "
            f"at the SAME gross) against each prediction, in pp/yr:")
        say(f"    {'sleeve':>6} {'gross':>5} | {'measured':>9} {'F_A':>9} {'F_B':>9} {'F_C':>9} "
            f"{'F_E':>9} {'F_D':>9} | {'errA':>8} {'errB':>8} {'errC':>8} {'errE':>8} "
            f"{'errD':>9} | {'SE(dCAGR)':>9} {'|t|':>6} | {'errB/SE':>8}")
        for slv in SLEEVES:
            if slv == "CASH":
                continue
            for g_ in GROSSES:
                cell, base = cells[(slv, g_)], cells[("CASH", g_)]
                rC, rS = base["net"][WARMUP:], cell["net"][WARMUP:]
                meas = cagr(rS) - cagr(rC)
                cs, cs_oos = sleeve_cagr[(pan.name, slv)]
                sbar = cell["row"]["sbar"]
                ddrag = (cell["row"]["turn"] - base["row"]["turn"]) * COST / 1e4
                fa = (1.0 - g_) * cs
                fb = sbar * cs
                fc = (1.0 + cagr(rC)) * sbar * cs - ddrag
                # F_D's prediction is RECONSTRUCTED minus RECONSTRUCTED: neither term needs a
                # direct run of the sleeve book, only the core object and the sleeve series.
                fd = cell["row"]["FD_CAGR"] - base["row"]["FD_CAGR"]
                # F_E: the growth-rate form.  A book held at fixed weights (g, 1-g) does not
                # earn the weighted average of its legs' CAGRs; it earns the weighted average of
                # their LOG growth rates, which adds g*(1-g)*(var_s/2 - cov) against the cash
                # book whose residual has zero variance.  All inputs come from the CASH book and
                # the sleeve series: sig_core = vol(cash book)/g, cov(core, sleeve) =
                # cov(cash book, sleeve)/g.  Nothing here needs the sleeve book to be run.
                srr = pan.sret[slv][WARMUP:]
                var_s = float(np.var(srr, ddof=0) * 252.0)
                cov_cs = float(np.cov(rC, srr, ddof=0)[0, 1] * 252.0 / g_) if g_ > 0 else 0.0
                inc = ((1.0 - g_) * np.log1p(cs)
                       + g_ * (1.0 - g_) * (var_s / 2.0 - cov_cs))
                fe = float(np.expm1(np.log1p(cagr(rC)) + inc)) - cagr(rC) - ddrag
                obs, se, tt = paired_block_dcagr(rS, rC)
                # OOS leg of the same test
                iO = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
                rCo, rSo = base["net"][iO:], cell["net"][iO:]
                measO = cagr(rSo) - cagr(rCo)
                sbarO = cell["row"]["sbar_oos"]
                ddragO = (annturn(np.zeros(1), 0, 1) if False else
                          (cell["row"]["turn"] - base["row"]["turn"]) * COST / 1e4)
                faO = (1.0 - g_) * cs_oos
                fbO = sbarO * cs_oos
                fcO = (1.0 + cagr(rCo)) * sbarO * cs_oos - ddragO
                d = dict(panel=pan.name, sleeve=slv, gross=g_,
                         sbar=sbar, nominal_resid=1.0 - g_, CAGR_sleeve=cs,
                         measured_dCAGR=meas, F_A=fa, F_B=fb, F_C=fc, F_E=fe, F_D=fd,
                         err_A=fa - meas, err_B=fb - meas, err_C=fc - meas, err_E=fe - meas,
                         err_D=fd - meas,
                         sleeve_vol=float(np.std(srr, ddof=0) * np.sqrt(252.0)),
                         var_term=g_ * (1.0 - g_) * (var_s / 2.0 - cov_cs),
                         cov_core_sleeve=cov_cs, d_drag=ddrag,
                         SE_dCAGR=se, t_dCAGR=tt,
                         errB_over_SE=(fb - meas) / se if se > 0 else np.nan,
                         errC_over_SE=(fc - meas) / se if se > 0 else np.nan,
                         measured_dSharpe=sharpe(rS) - sharpe(rC),
                         measured_dMaxDD=mdd(rS) - mdd(rC),
                         OOS_measured_dCAGR=measO, OOS_F_A=faO, OOS_F_B=fbO, OOS_F_C=fcO,
                         OOS_err_A=faO - measO, OOS_err_B=fbO - measO, OOS_err_C=fcO - measO,
                         OOS_measured_dSharpe=sharpe(rSo) - sharpe(rCo),
                         script=f"{DATE}_{SLUG}_C.py")
                cf_rows.append(d)
                say(f"    {slv:>6} {g_:5.2f} | {meas*100:8.3f}p {fa*100:8.3f}p {fb*100:8.3f}p "
                    f"{fc*100:8.3f}p {fe*100:8.3f}p {fd*100:8.3f}p | {(fa-meas)*100:7.3f}p "
                    f"{(fb-meas)*100:7.3f}p {(fc-meas)*100:7.3f}p {(fe-meas)*100:7.4f}p "
                    f"{(fd-meas)*100:8.4f}p | {se*100:8.3f}p {abs(tt):6.2f} | "
                    f"{abs((fb-meas)/se) if se>0 else np.nan:8.2f}")

        # ---- rule 8: three choosers, 2017-2026 read ONCE -------------------------------------
        gr = pd.DataFrame([c["row"] for c in cells.values()])
        anchor = cells[(ANCHOR_SLV, ANCHOR_G)]["row"]

        # C_GRID: IS Sharpe over all 20 DIRECT books
        pick_grid = gr.loc[gr["IS_Sharpe"].idxmax()]
        # C_RECON: IS Sharpe from F_D reconstructions only (3 core objects + 3 sleeve series)
        rec_is = {}
        for slv in SLEEVES:
            for g_ in GROSSES:
                gg2, tu2, _ = run_recon(core, pan.sret[slv], g_, cash_leg=(slv == "CASH"))
                rr2 = gg2 - tu2 * COST / 1e4
                rec_is[(slv, g_)] = sharpe(rr2[WARMUP:i_is])
        pick_recon_k = max(rec_is, key=lambda k: rec_is[k])
        # C_CHEAP: CASH ladder + F_B only, vol assumed untouched by the sleeve
        cheap = {}
        for slv in SLEEVES:
            for g_ in GROSSES:
                b = cells[("CASH", g_)]["row"]
                cs_is = cagr(pan.sret[slv][WARMUP:i_is])
                cheap[(slv, g_)] = ((b["IS_CAGR"] + b["IS_sbar"] * cs_is) / b["IS_vol"]
                                    if b["IS_vol"] > 0 else np.nan)
        pick_cheap_k = max(cheap, key=lambda k: cheap[k])

        for cname, key in [("C_GRID", (pick_grid["sleeve"], float(pick_grid["gross"]))),
                           ("C_RECON", pick_recon_k), ("C_CHEAP", pick_cheap_k)]:
            pr = cells[key]["row"]
            wf_rows.append(dict(panel=pan.name, chooser=cname, pick_sleeve=key[0],
                                pick_gross=key[1],
                                OOS_CAGR=pr["OOS_CAGR"], OOS_Sharpe=pr["OOS_Sharpe"],
                                OOS_MaxDD=pr["OOS_MaxDD"],
                                anchor_OOS_CAGR=anchor["OOS_CAGR"],
                                anchor_OOS_Sharpe=anchor["OOS_Sharpe"],
                                anchor_OOS_MaxDD=anchor["OOS_MaxDD"],
                                d_OOS_Sharpe=pr["OOS_Sharpe"] - anchor["OOS_Sharpe"],
                                d_OOS_CAGR=pr["OOS_CAGR"] - anchor["OOS_CAGR"],
                                spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                                spy_OOS_MaxDD=spyO["MaxDD"],
                                live_OOS_Sharpe=liveO["Sharpe"],
                                keep4b_oos=pr["keep4b_oos"], keep4a_oos=pr["keep4a_oos"],
                                script=f"{DATE}_{SLUG}_C.py"))
        # ex-post best OOS cell, for the record (never a claim)
        best_oos = gr.loc[gr["OOS_Sharpe"].idxmax()]
        wf_rows.append(dict(panel=pan.name, chooser="EX-POST BEST OOS (not a claim)",
                            pick_sleeve=best_oos["sleeve"], pick_gross=float(best_oos["gross"]),
                            OOS_CAGR=best_oos["OOS_CAGR"], OOS_Sharpe=best_oos["OOS_Sharpe"],
                            OOS_MaxDD=best_oos["OOS_MaxDD"],
                            anchor_OOS_CAGR=anchor["OOS_CAGR"],
                            anchor_OOS_Sharpe=anchor["OOS_Sharpe"],
                            anchor_OOS_MaxDD=anchor["OOS_MaxDD"],
                            d_OOS_Sharpe=best_oos["OOS_Sharpe"] - anchor["OOS_Sharpe"],
                            d_OOS_CAGR=best_oos["OOS_CAGR"] - anchor["OOS_CAGR"],
                            spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                            spy_OOS_MaxDD=spyO["MaxDD"], live_OOS_Sharpe=liveO["Sharpe"],
                            keep4b_oos=best_oos["keep4b_oos"], keep4a_oos=best_oos["keep4a_oos"],
                            script=f"{DATE}_{SLUG}_C.py"))

        say(f"\n    RULE 8 on {pan.name} (IS = warm-up..2016, OOS = 2017-2026 read once; anchor "
            f"= frozen (CASH, 0.60) OOS {anchor['OOS_CAGR']:.2%}/{anchor['OOS_Sharpe']:.4f}/"
            f"{anchor['OOS_MaxDD']:.2%}):")
        for w in wf_rows[-4:]:
            say(f"      {w['chooser']:>28}  picks ({w['pick_sleeve']}, {w['pick_gross']:.2f})  "
                f"OOS {w['OOS_CAGR']:6.2%}/{w['OOS_Sharpe']:7.4f}/{w['OOS_MaxDD']:7.2%}  "
                f"dSharpe vs doing nothing {w['d_OOS_Sharpe']:+7.4f}  4b_oos "
                f"{'Y' if w['keep4b_oos'] else 'n'}")

    # ------------------------------------------------------------------------------ the gates
    say("\n" + "=" * 126)
    gate("G2 no leverage: max weight sum at any rebalance", f"{max_wsum:.12f}", "<= 1 + 1e-9",
         max_wsum <= 1.0 + 1e-9)
    gate("G3 F_D (two-asset MIX) vs the DIRECT runner, max |daily net return| over ALL 60 cells",
         f"{max_recon_all:.3e}", "< 1e-12", max_recon_all < 1e-12)
    gate("G4 F_D on the CASH cells specifically (sleeve = a 0% asset, the degenerate case)",
         f"{max_recon_cash:.3e}", "< 1e-12", max_recon_cash < 1e-12)

    G = pd.DataFrame(grid)
    CF = pd.DataFrame(cf_rows)
    WF = pd.DataFrame(wf_rows)
    RC = pd.DataFrame(recon_rows)

    sb = G[G.sleeve != "CASH"]
    dev_sbar = float((sb["sbar"] - (1.0 - sb["gross"])).abs().max())
    gate("G5 sbar is NOT the nominal (1-g): max |sbar - (1-g)| across the 45 sleeve cells",
         f"{dev_sbar:.4f}", "published; > 0 means the nominal form F_A is already wrong",
         True)

    # ------------------------------------------------------------------------------ the answer
    say("\n" + "=" * 126)
    say("ANSWER")
    say("=" * 126)
    for c, lab in [("err_A", "F_A  (1-g)*CAGR_s                          "),
                   ("err_B", "F_B  sbar*CAGR_s        [the queue's form]  "),
                   ("err_C", "F_C  (1+CAGR_cash)*sbar*CAGR_s - d(drag)    "),
                   ("err_E", "F_E  growth-rate form, + g(1-g)(var_s/2-cov) "),
                   ("err_D", "F_D  two-asset MIX identity                 ")]:
        e = CF[c].values
        say(f"  {lab} MAE {np.mean(np.abs(e))*100:7.4f} pp/yr  MAX {np.max(np.abs(e))*100:7.4f} "
            f"pp/yr  MEAN {np.mean(e)*100:+7.4f} pp  |  inside its own paired-bootstrap SE at "
            f"{int(np.sum(np.abs(e) < CF['SE_dCAGR'].values))} of {len(e)} cells")
    for c, lab in [("OOS_err_A", "F_A"), ("OOS_err_B", "F_B"), ("OOS_err_C", "F_C")]:
        e = CF[c].values
        say(f"  OOS {lab}: MAE {np.mean(np.abs(e))*100:7.4f} pp/yr  MAX "
            f"{np.max(np.abs(e))*100:7.4f} pp/yr  MEAN {np.mean(e)*100:+7.4f} pp")
    r2 = np.corrcoef(CF["var_term"].values, -CF["err_C"].values)[0, 1] ** 2
    say(f"  WHAT THE SCALAR FORMS OMIT: F_C's shortfall is the fixed-weight mix's variance term. "
        f"corr^2(g(1-g)(var_s/2 - cov), -err_C) = {r2:.4f} over the 45 cells; the shortfall runs "
        f"{CF.groupby('sleeve')['err_C'].mean().reindex(['SHY','IEF','TLT']).mul(-100).round(4).to_dict()} "
        f"pp/yr by sleeve against sleeve vols "
        f"{CF.groupby('sleeve')['sleeve_vol'].mean().reindex(['SHY','IEF','TLT']).mul(100).round(2).to_dict()}%.")
    flip = 0
    for _, q in CF.iterrows():
        base = G[(G.panel == q.panel) & (G.sleeve == 'CASH') & (G.gross == q.gross)].iloc[0]
        cell = G[(G.panel == q.panel) & (G.sleeve == q.sleeve) & (G.gross == q.gross)].iloc[0]
        floor = cell['CAGR'] - 0.0
        # the 4b CAGR leg re-read with the PREDICTED CAGR instead of the measured one
        bar = CAGR_FLOOR * SPY_CAGR[q.panel]
        flip += int((cell['CAGR'] >= bar) != ((base['CAGR'] + q.F_B) >= bar))
    say(f"  DECISION IMPACT: re-reading the 4b CAGR leg with F_B's predicted CAGR instead of the "
        f"measured one flips the leg at {flip} of {len(CF)} sleeve cells.")
    say(f"  SIGN: F_A over-predicts the credit at {int((CF.err_A>0).sum())} of {len(CF)} cells, "
        f"F_B at {int((CF.err_B>0).sum())}, F_C at {int((CF.err_C>0).sum())}.")
    say(f"  The record's own resolution on this axis: mean paired-bootstrap SE of dCAGR = "
        f"{CF['SE_dCAGR'].mean()*100:.4f} pp/yr; the frozen incumbent's 4b CAGR margin and DD "
        f"margin are the bars any error has to stay under to be ignorable.")
    say(f"  4a: {int(G.keep4a.sum())} of {len(G)} cells FULL, "
        f"{int((G.keep4a & G.keep4a_oos).sum())} FULL and OOS.")
    say(f"  4b: {int(G.keep4b.sum())} of {len(G)} cells FULL, "
        f"{int((G.keep4b & G.keep4b_oos).sum())} FULL and OOS.")
    agree = WF[WF.chooser.isin(["C_GRID", "C_RECON"])].groupby("panel").apply(
        lambda d: (d[d.chooser == "C_GRID"][["pick_sleeve", "pick_gross"]].values ==
                   d[d.chooser == "C_RECON"][["pick_sleeve", "pick_gross"]].values).all())
    say(f"  RULE 8 / OPERATIONAL: C_RECON reproduces C_GRID's pick on {int(agree.sum())} of "
        f"{len(agree)} panels (it uses 3 core books instead of 60).  Mean OOS dSharpe vs doing "
        f"nothing: C_GRID {WF[WF.chooser=='C_GRID'].d_OOS_Sharpe.mean():+.4f}, C_RECON "
        f"{WF[WF.chooser=='C_RECON'].d_OOS_Sharpe.mean():+.4f}, C_CHEAP "
        f"{WF[WF.chooser=='C_CHEAP'].d_OOS_Sharpe.mean():+.4f}.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    CF.to_csv(f"{OUT}.closedform.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    RC.to_csv(f"{OUT}.recon.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(pd.DataFrame(GATES)["pass_"].sum())
    say(f"\n  GATES {npass}/{len(GATES)} pass (asserted + published).")
    say(f"  Wrote {OUT.name}.grid.csv ({len(G)} cells), .closedform.csv ({len(CF)}), "
        f".walkforward.csv ({len(WF)}), .recon.csv ({len(RC)}), .gates.csv ({len(GATES)}).")
    say(f"  Elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

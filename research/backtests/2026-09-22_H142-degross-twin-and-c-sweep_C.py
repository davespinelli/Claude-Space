#!/usr/bin/env python3
"""
Idea 1472 (lane C, 2026-09-22) -- does U56 H = 142 survive a DE-GROSS TWIN and a c SWEEP,
or is it THE BAND AGAIN?

THE PREMISE.  Idea 1461 refined 1444's min-hold ladder and, incidentally, published ONE
KEEP-4b candidate: the beta-tilted band book on U56 at H = 142, c = 0.50 (full 15.47% /
1.2103 / -19.47%; OOS 17.25% / 1.2350 / -19.47%), picked by BOTH of its rule-8 choosers.
That cell passes 4b only WITH the band: its own c = 0 anchor fails the DD leg by -1.15 pp.

But SIX consecutive 2026-09-19 runs found the same thing about every OTHER drawdown-buying
device in this record: at MATCHED CAGR a plain DE-GROSS (hold the same names, just less of
them) buys at least as much drawdown as the device does, i.e. the device is a re-discovery of
one scalar -- exposure.  1472 asks whether the beta band is the seventh, or the first exception.

  IF the CAGR-matched de-gross twin matches or beats the band cell on MaxDD (and on Sharpe),
     the candidate is DEAD ON ARRIVAL: it is the exposure scalar wearing a band's clothes.
  IF the band cell beats its twin on BOTH axes, it is the FIRST band cell in the record that
     is not, and the 4b pass is worth a memo.
  A rank-PERMUTATION twin (same weight multiset, beta ORDER destroyed) separates the two
  candidate mechanisms: DISPERSION (the multiset alone) from BETA INFORMATION (the ordering).

THE RULE under test (identical to 1429 / 1444 / 1461, re-used verbatim so the runs compare):
    hold the N = 20 names the live composite selects under a min-hold H;
    rank them by trailing beta to SPY over B = 126 rows, ASCENDING;
    z_i = 1 - 2*(rank_i - 0.5)/n  in [-1, +1] with sum z = 0 EXACTLY;
    w_i = (G/n) * (1 + c*z_i),  G = 0.75.  LOWEST beta takes the CAP side.  c = 0 is inert.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  H  {126, 142}                      DIAL 1 -- the frozen incumbent's min-hold and 1461's argmin.
  c  {0.00, 0.25, 0.50, 0.75, 1.00}  DIAL 2 -- the band half-width.  c = 0.00 is the ANCHOR.

NOT DIALS, REPORTED AT EVERY VALUE, NEVER SELECTED ON:
  PANEL {U56, B136, SMALL} (rule 9);  COST RUNG {0, 5, 10, 25, 50} bps (PROTOCOL's own rung is
  10 and every verdict below is read there);  CADENCE W;  N = 20;  G = 0.75;  B = 126.

THE TWO TWINS, BOTH PRE-REGISTERED:
  TWIN-D (de-gross, the record's convention):  that H's OWN c = 0 anchor scaled by a CONSTANT
    k chosen so its NET CAGR EQUALS the band cell's NET CAGR at that SAME cost rung.  Same
    names, same days, same turnover shape -- ONLY exposure differs.  Achieved match is gate G4.
  TWIN-P (rank permutation):  the IDENTICAL weight multiset assigned to the held names in a
    SEED-DRAWN RANDOM order instead of the beta order.  Same dispersion, same gross, same
    turnover shape, ZERO beta information.  20 seeds; mean and SE published.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  The band cell SURVIVES only if, at
the live 10 bps rung on U56 (the candidate's own cell, H = 142 / c = 0.50):
  (i)   MaxDD(cell) > MaxDD(TWIN-D)        -- it buys MORE drawdown protection at matched CAGR;
  (ii)  Sharpe(cell) > Sharpe(TWIN-D)      -- and is not paying for it elsewhere;
  (iii) it still clears 4b FULL and OOS;
  (iv)  a legal IS-ONLY chooser (rule 8) can REACH it.
Failing (i) is "the scalar wins again -- dead on arrival".  Passing (i)-(iii) and failing (iv)
is PARK, not KEEP.  This run proposes NO rules change either way.

COMPARANDS (rule 3): the live RULES v2 baseline at the same cost rung and cadence, SPY
buy-and-hold, and the FROZEN (H = 126, c = 0) 2026-09-04 incumbent anchor.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, cost charged on turnover, no leverage, no shorting);
rule 3 (RULES v2 AND SPY); rule 4 (both KEEP paths at EVERY grid point, exactly 2 tuned dials);
rule 7 (a KILL is reported as one); rule 8 (walk-forward: (H, c) chosen on warm-up..2016-12-31
ONLY, 2017-2026 read ONCE) under FOUR pre-registered choosers, one of them ZERO-PARAMETER;
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of idea 1461's two committed U56 cells
(anchor H=126 c=0: 15.80% / 1.1537 / -19.13%, OOS Sharpe 1.1857; candidate H=142 c=0.50:
15.47% / 1.2103 / -19.47%, OOS 17.25% / 1.2350 / -19.47%).  G2 the c = 0 cell at each H is
BIT-IDENTICAL to that H's anchor.  G3 every rebalance's weight sum == G (no leverage leak).
G4 TWIN-D's achieved CAGR match < 1e-6 at every (cell, cost).  G5 exposure channel SHUT: mean
realised gross EQUAL across c at fixed (panel, H).  G6 TWIN-P at c = 0 is BIT-IDENTICAL to the
anchor (permuting an inert multiset is a no-op).  G7 selection depends on H ONLY: identical
name sets across every c at a given (panel, H).  G8 the band widens monotonically with c
(max weight strictly increasing, min strictly decreasing).  G9 the choosers read NO row on or
after 2017-01-01.  G10 exactly two tuned dials.  G11 beta uses trailing rows only.
G12 TWIN-D is a PURE SCALAR: its turnover / k matches the anchor's.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-22_H142-degross-twin-and-c-sweep_C.py
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
from engine import backtest, rebalance_mask           # noqa: E402

DATE = "2026-09-22"
SLUG = "H142-degross-twin-and-c-sweep"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_G, I_B = 20, 0.75, 126
CADENCE = "W"
HS = [126, 142]                              # DIAL 1
CS = [0.00, 0.25, 0.50, 0.75, 1.00]          # DIAL 2
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]         # reported, never selected
COST_LIVE = 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
PERM_SEEDS = 20
SEED0 = 20260922
K_MAX = 1.0 / I_G                            # gross 1.00 -- PROTOCOL rule 2, no leverage
K_LADDER = np.round(np.linspace(0.10, K_MAX, 51), 6)
# idea 1461's committed U56 numbers, for the cross-script replay gate G1
C1461_ANCH = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
C1461_CAND = dict(CAGR=0.1547, Sharpe=1.2103, MaxDD=-0.1947,
                  oCAGR=0.1725, oSharpe=1.2350, oMaxDD=-0.1947)

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


# ---------------------------------------------------------------- mechanics
def mech(q):
    """The live selection mechanics (baseline.score's 3-leg composite, incumbent convention)."""
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def rolling_beta(R, y, B):
    """Trailing beta of every column to the benchmark over B TRAILING rows (gate G11)."""
    ey = y.rolling(B).mean()
    vy = (y * y).rolling(B).mean() - ey * ey
    ex = R.rolling(B).mean()
    exy = R.mul(y, axis=0).rolling(B).mean()
    cov = exy.sub(ex.mul(ey, axis=0))
    return cov.div(vy.replace(0.0, np.nan), axis=0).values


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
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.beta = rolling_beta(px[invest].pct_change(), px["SPY"].pct_change(), I_B)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.oos = np.flatnonzero(px.index >= pd.Timestamp(OOS_START))
        self.is_rows = np.arange(WARMUP, int(self.oos[0]))


def segments(pan, N, H, lag=1):
    """The min-hold selection frame.  Depends on H ONLY (not c, not the twin), so it is built
    ONCE per (panel, H) and every book at that H holds the IDENTICAL names on the IDENTICAL
    rows (gate G7)."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    segs = []
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(x) for x in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for x in keep:
                k[x] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(x) for x in order[:need] if np.isfinite(k[x])]
        new = np.full(K, -1, dtype=np.int64)
        for x in keep:
            new[x] = cur[x]
        for x in take:
            new[x] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy()))
    return segs


def band_multiset(n, c, gross=I_G):
    """The weight multiset for n names at band half-width c, in CAP-FIRST order."""
    if n == 0:
        return np.zeros(0)
    ranks = np.arange(1, n + 1, dtype=float)
    z = 1.0 - 2.0 * (ranks - 0.5) / n          # sums to EXACTLY 0
    return (gross / n) * (1.0 + c * z)


def cell_weights(pan, segs, c, gross=I_G, perm_rng=None):
    """Per-segment weights summing to `gross`.  LOWEST trailing beta takes the CAP side.
    perm_rng != None -> TWIN-P: identical multiset, order drawn at RANDOM (beta ignored)."""
    BE = pan.beta
    ws = []
    for (t, stop, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        m = band_multiset(n, c, gross)
        if c == 0.0:
            order = np.arange(n)
        elif perm_rng is not None:
            order = perm_rng.permutation(n)
        else:
            b = BE[ts, sel].astype(float)
            fin = np.isfinite(b)
            if not fin.all():
                med = np.nanmedian(b[fin]) if fin.any() else 1.0
                b = np.where(fin, b, med)
            order = np.argsort(b, kind="stable")   # ascending beta -> cap first
        w = np.empty(n)
        w[order] = m
        ws.append(w)
    return ws


def run_book(pan, segs, ws):
    """One book.  Weights applied at row i0, drifting inside the segment (engine convention).
    Returns GROSS daily returns and the turnover path, so every cost rung is read from ONE run."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gross_path = np.zeros(T)
    curw = np.zeros(M)
    wsum_max, wsum_min = 0.0, np.inf
    mx, mn = [], []
    for (i0, i1, ts, sel), wv in zip(segs, ws):
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv
            mx.append(float(wv.max()))
            mn.append(float(wv.min()))
        s = float(w0.sum())
        if len(sel):                       # empty warm-up segments hold nothing by construction
            wsum_max, wsum_min = max(wsum_max, s), min(wsum_min, s)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - s
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gross_path[i0:i1] = s
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    if not np.isfinite(wsum_min):
        wsum_max = wsum_min = float(ws[0].sum()) if len(ws) and len(ws[0]) else 0.0
    return dict(g=out, turn=turn, gross=gross_path, wsum_max=wsum_max, wsum_min=wsum_min,
                maxw=float(np.mean(mx)) if mx else np.nan,
                minw=float(np.mean(mn)) if mn else np.nan)


def net_of(bk, cost):
    return bk["g"] - bk["turn"] * cost / 1e4


# ---------------------------------------------------------------- metrics
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


def pack(r, n_oos):
    """r is the WARMUP-trimmed series; its last n_oos rows are the OOS window."""
    h1, h2 = halves(r)
    m, o = triple(r), triple(r[-n_oos:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def keep_paths(m, spy, live):
    k4a = bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(m["H1"] > spy["H1"]), H2=bool(m["H2"] > spy["H2"]),
                OOS=bool(m["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                DD=bool(m["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    return k4a, bool(all(legs.values())), legs


def keep4b_oos(m_oos, spy_oos):
    """4b read on the OOS window alone (the rule-8 reading)."""
    h1, h2 = m_oos["H1"], m_oos["H2"]
    return bool(h1 > spy_oos["H1"] and h2 > spy_oos["H2"]
                and m_oos["MaxDD"] >= DD_CAP * spy_oos["MaxDD"]
                and m_oos["CAGR"] >= CAGR_FLOOR * spy_oos["CAGR"])


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 136)
    say(f"IDEA 1472 (lane C, run 21) -- {DATE} -- does U56 H = 142 survive a DE-GROSS TWIN "
        f"and a c SWEEP, or is it THE BAND AGAIN?")
    say(f"  TUNED DIALS (exactly 2): H {HS} x c {CS}.")
    say(f"  REPORTED, NEVER SELECTED: panel {{U56, B136, SMALL}} x cost {COSTS} bps; "
        f"cadence {CADENCE}; N={I_N}; G={I_G}; B={I_B}.")
    say(f"  PRE-REGISTERED BAR (stated before any number was read): the candidate SURVIVES only "
        f"if at 10 bps on U56, H=142/c=0.50 -- (i) MaxDD > TWIN-D's, (ii) Sharpe > TWIN-D's, "
        f"(iii) 4b clears FULL and OOS, (iv) a legal IS-only chooser REACHES it.")
    say("=" * 136)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one.  What this run READS is a CONTRAST between books built "
        "over the SAME names on the SAME days -- which the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances;  "
            f"OOS {len(p.oos)} rows from {p.idx[p.oos[0]].date()}")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G10 exactly two tuned dials", "H x c", "2", True)
    gate("G11 beta uses trailing rows only (pandas rolling is backward-looking, stamped at the "
         "t-1 decision row)", "by construction", "no look-ahead", True)

    grid, twinp_rows, wf_rows = [], [], []
    g2_dev = g3_dev = g5_dev = g6_dev = 0.0
    g7_ok, g8_ok = True, True
    g_lev = 0.0
    n_infeas = 0
    g4_worst, g12_dev = 0.0, 0.0

    for pan in panels:
        n_oos = len(pan.oos)
        sp = pan.spy[WARMUP:]
        spy = pack(sp, n_oos)
        spy_is = dict(zip(("H1", "H2"), halves(pan.spy[pan.is_rows])))
        spy_is.update(triple(pan.spy[pan.is_rows]))
        spy_oos = dict(zip(("H1", "H2"), halves(pan.spy[pan.oos])))
        spy_oos.update(triple(pan.spy[pan.oos]))

        # live RULES v2 baseline, same cadence, at each cost rung
        bw = rules_v2_weights(pan.px)
        live_by_cost = {}
        for cst in COSTS:
            lr = backtest(pan.px, bw, cost_bps=cst, freq=CADENCE)["returns"].values[WARMUP:]
            live_by_cost[cst] = pack(lr, n_oos)
        say(f"\n-- {pan.name} -- SPY full {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / "
            f"{spy['MaxDD']:.2%}  (halves {spy['H1']:.3f}/{spy['H2']:.3f}; "
            f"OOS {spy['OOS_CAGR']:.2%} / {spy['OOS_Sharpe']:.4f} / {spy['OOS_MaxDD']:.2%})")
        say(f"   4b bar on {pan.name}: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%};  "
            f"RULES v2 @10bps {live_by_cost[COST_LIVE]['CAGR']:.2%} / "
            f"{live_by_cost[COST_LIVE]['Sharpe']:.4f} / {live_by_cost[COST_LIVE]['MaxDD']:.2%}")

        for H in HS:
            segs = segments(pan, I_N, H)
            names_ref = [tuple(s[3]) for s in segs]
            anchor = run_book(pan, segs, cell_weights(pan, segs, 0.0))
            # k-ladder on the anchor: one run per k, reused for every (cell, cost) twin solve
            kbooks = {}
            for k in K_LADDER:
                kbooks[float(k)] = run_book(pan, segs, cell_weights(pan, segs, 0.0, gross=I_G * k))

            def twin_at(k):
                k = float(np.clip(k, K_LADDER[0], K_LADDER[-1]))
                return run_book(pan, segs, cell_weights(pan, segs, 0.0, gross=I_G * k))

            for c in CS:
                ws = cell_weights(pan, segs, c)
                bk = run_book(pan, segs, ws)
                # G7: selection depends on H only
                if [tuple(s[3]) for s in segs] != names_ref:
                    g7_ok = False
                # G3 / no leverage
                g3_dev = max(g3_dev, abs(bk["wsum_max"] - I_G), abs(bk["wsum_min"] - I_G))
                g_lev = max(g_lev, bk["wsum_max"])
                # G2: c = 0 is bit-identical to the anchor
                if c == 0.0:
                    g2_dev = max(g2_dev, float(np.abs(bk["g"] - anchor["g"]).max()))
                # G5: exposure channel shut
                g5_dev = max(g5_dev, abs(float(bk["gross"][WARMUP:].mean())
                                         - float(anchor["gross"][WARMUP:].mean())))

                for cst in COSTS:
                    r = net_of(bk, cst)[WARMUP:]
                    m = pack(r, n_oos)
                    live = live_by_cost[cst]
                    k4a, k4b, legs = keep_paths(m, spy, live)
                    m_oos = dict(CAGR=m["OOS_CAGR"], Sharpe=m["OOS_Sharpe"], MaxDD=m["OOS_MaxDD"])
                    h1o, h2o = halves(net_of(bk, cst)[pan.oos])
                    m_oos.update(H1=h1o, H2=h2o)
                    k4b_oos = keep4b_oos(m_oos, spy_oos)

                    # ---- TWIN-D: anchor scaled to MATCH this cell's net CAGR at this rung
                    if c == 0.0:
                        kk, tw, terr = 1.0, anchor, 0.0
                    else:
                        cg = np.array([cagr(net_of(kbooks[float(k)], cst)[WARMUP:])
                                       for k in K_LADDER])
                        tgt = m["CAGR"]
                        o = np.argsort(cg)
                        kk = float(np.interp(tgt, cg[o], K_LADDER[o]))
                        tw = twin_at(kk)
                        terr = abs(cagr(net_of(tw, cst)[WARMUP:]) - tgt)
                        lo, hi = max(K_LADDER[0], kk * 0.9), min(K_LADDER[-1], kk * 1.1)
                        for _ in range(45):                    # bisection refinement
                            if terr < 1e-9:
                                break
                            mid = 0.5 * (lo + hi)
                            tm = twin_at(mid)
                            fm = cagr(net_of(tm, cst)[WARMUP:]) - tgt
                            if abs(fm) < terr:
                                kk, tw, terr = mid, tm, abs(fm)
                            if fm > 0:
                                hi = mid
                            else:
                                lo = mid
                    feasible = bool(c == 0.0 or (kk < K_LADDER[-1] - 1e-9 and terr < 1e-6))
                    if feasible:
                        g4_worst = max(g4_worst, terr)
                    else:
                        n_infeas += 1
                    tr = net_of(tw, cst)[WARMUP:]
                    tm_ = pack(tr, n_oos)
                    t4a, t4b, tlegs = keep_paths(tm_, spy, live)
                    tmo = dict(CAGR=tm_["OOS_CAGR"], Sharpe=tm_["OOS_Sharpe"],
                               MaxDD=tm_["OOS_MaxDD"])
                    th1o, th2o = halves(net_of(tw, cst)[pan.oos])
                    tmo.update(H1=th1o, H2=th2o)
                    t4b_oos = keep4b_oos(tmo, spy_oos)
                    if c > 0:
                        g12_dev = max(g12_dev, abs(
                            float(tw["turn"][WARMUP:].sum()) / kk
                            - float(anchor["turn"][WARMUP:].sum())) /
                            max(1e-9, float(anchor["turn"][WARMUP:].sum())))

                    row = dict(panel=pan.name, H=H, c=c, cost_bps=cst)
                    for pre, mm in (("cell", m), ("twin", tm_), ("v2", live), ("spy", spy)):
                        row.update({f"{pre}_{k2}": v for k2, v in mm.items()})
                    row.update(
                        cell_4a=k4a, cell_4b=k4b, cell_4b_OOS=k4b_oos,
                        twin_4a=t4a, twin_4b=t4b, twin_4b_OOS=t4b_oos,
                        twin_k=kk, twin_cagr_err=terr, twin_feasible=feasible,
                        dMaxDD_pp=100.0 * (m["MaxDD"] - tm_["MaxDD"]),
                        dSharpe=m["Sharpe"] - tm_["Sharpe"],
                        dMaxDD_OOS_pp=100.0 * (m["OOS_MaxDD"] - tm_["OOS_MaxDD"]),
                        dSharpe_OOS=m["OOS_Sharpe"] - tm_["OOS_Sharpe"],
                        beats_twin_dd=bool(feasible and m["MaxDD"] > tm_["MaxDD"]),
                        beats_twin_sharpe=bool(feasible and m["Sharpe"] > tm_["Sharpe"]),
                        beats_twin_both=bool(feasible and m["MaxDD"] > tm_["MaxDD"]
                                             and m["Sharpe"] > tm_["Sharpe"]),
                        leg_H1=legs["H1"], leg_H2=legs["H2"], leg_OOS=legs["OOS"],
                        leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                        mean_gross=float(bk["gross"][WARMUP:].mean()),
                        turnover_yr=float(bk["turn"][WARMUP:].sum()
                                          / (len(bk["turn"][WARMUP:]) / 252)),
                        mean_maxw=bk["maxw"], mean_minw=bk["minw"],
                    )
                    grid.append(row)

                # ---- TWIN-P: identical multiset, beta ORDER destroyed (live rung only)
                if c > 0.0:
                    ps = []
                    for s in range(PERM_SEEDS):
                        rng = np.random.default_rng(SEED0 + 977 * s + 13 * H + int(100 * c))
                        pb = run_book(pan, segs, cell_weights(pan, segs, c, perm_rng=rng))
                        pr_ = net_of(pb, COST_LIVE)[WARMUP:]
                        pm = pack(pr_, n_oos)
                        ps.append((pm["CAGR"], pm["Sharpe"], pm["MaxDD"], pm["OOS_Sharpe"]))
                    P = np.array(ps)
                    ref = [g for g in grid if g["panel"] == pan.name and g["H"] == H
                           and g["c"] == c and g["cost_bps"] == COST_LIVE][0]
                    twinp_rows.append(dict(
                        panel=pan.name, H=H, c=c, cost_bps=COST_LIVE, seeds=PERM_SEEDS,
                        real_CAGR=ref["cell_CAGR"], real_Sharpe=ref["cell_Sharpe"],
                        real_MaxDD=ref["cell_MaxDD"], real_OOS_Sharpe=ref["cell_OOS_Sharpe"],
                        permP_CAGR=P[:, 0].mean(), permP_Sharpe=P[:, 1].mean(),
                        permP_MaxDD=P[:, 2].mean(), permP_OOS_Sharpe=P[:, 3].mean(),
                        se_CAGR=P[:, 0].std(ddof=1) / np.sqrt(PERM_SEEDS),
                        se_Sharpe=P[:, 1].std(ddof=1) / np.sqrt(PERM_SEEDS),
                        se_MaxDD=P[:, 2].std(ddof=1) / np.sqrt(PERM_SEEDS),
                        se_OOS_Sharpe=P[:, 3].std(ddof=1) / np.sqrt(PERM_SEEDS),
                        t_Sharpe=(ref["cell_Sharpe"] - P[:, 1].mean())
                        / max(1e-12, P[:, 1].std(ddof=1) / np.sqrt(PERM_SEEDS)),
                        t_MaxDD=(ref["cell_MaxDD"] - P[:, 2].mean())
                        / max(1e-12, P[:, 2].std(ddof=1) / np.sqrt(PERM_SEEDS)),
                        frac_perm_dd_better=float((P[:, 2] > ref["cell_MaxDD"]).mean()),
                        frac_perm_sharpe_better=float((P[:, 1] > ref["cell_Sharpe"]).mean()),
                    ))
                else:
                    rng = np.random.default_rng(SEED0)
                    pb = run_book(pan, segs, cell_weights(pan, segs, 0.0, perm_rng=rng))
                    g6_dev = max(g6_dev, float(np.abs(pb["g"] - anchor["g"]).max()))

            # G8: the band widens monotonically with c
            for cst in (COST_LIVE,):
                sub = sorted([g for g in grid if g["panel"] == pan.name and g["H"] == H
                              and g["cost_bps"] == cst], key=lambda z: z["c"])
                mxs = [z["mean_maxw"] for z in sub]
                mns = [z["mean_minw"] for z in sub]
                if not (all(np.diff(mxs) > 0) and all(np.diff(mns) < 0)):
                    g8_ok = False

            # ---------------- rule 8 walk-forward is assembled after the full grid
        say(f"   ...{pan.name} priced ({time.time()-t0:.0f}s)")

    G = pd.DataFrame(grid)
    G4KMAX = float(G.twin_k.max())
    TP = pd.DataFrame(twinp_rows)

    gate("G2 c = 0 cell is BIT-IDENTICAL to that H's anchor", f"max |dr| {g2_dev:.2e}",
         "< 1e-12", g2_dev < 1e-12)
    gate("G3 every rebalance's weight sum == G (no leverage leak)",
         f"max |sum w - {I_G}| {g3_dev:.2e}", "< 1e-12", g3_dev < 1e-12)
    gate("G4 TWIN-D achieved CAGR match (over the FEASIBLE cells)",
         f"worst |err| {g4_worst:.2e}", "< 1e-6", g4_worst < 1e-6)
    gate("G4b no-leverage ceiling honoured: TWIN-D's gross never exceeds 1.00",
         f"max k {G4KMAX:.6f} -> gross {I_G * G4KMAX:.4f}", "<= 1.0000",
         I_G * G4KMAX <= 1.0 + 1e-9)
    gate("G13 no leverage anywhere in the BAND books (max weight sum)",
         f"{g_lev:.6f}", f"<= {I_G:.4f}", g_lev <= I_G + 1e-12)
    gate("G5 exposure channel SHUT (mean realised gross equal across c at fixed panel x H)",
         f"max |d mean gross| {g5_dev:.2e}", "< 1e-12", g5_dev < 1e-12)
    gate("G6 TWIN-P at c = 0 is BIT-IDENTICAL to the anchor (permuting an inert multiset)",
         f"max |dr| {g6_dev:.2e}", "< 1e-12", g6_dev < 1e-12)
    gate("G7 selection depends on H ONLY (identical name sets across every c)",
         "identical" if g7_ok else "DIFFERS", "identical", g7_ok)
    gate("G8 the band widens monotonically with c (max w up, min w down)",
         "monotone" if g8_ok else "NOT monotone", "monotone", g8_ok)
    gate("G12 TWIN-D is a PURE EXPOSURE SCALAR (turnover/k matches the anchor's)",
         f"max rel dev {g12_dev:.3f}", "< 0.05", g12_dev < 0.05)

    # ---- G1: cross-script replay of idea 1461's two committed U56 cells
    a = G[(G.panel == "U56") & (G.H == 126) & (G.c == 0.0) & (G.cost_bps == COST_LIVE)].iloc[0]
    q = G[(G.panel == "U56") & (G.H == 142) & (G.c == 0.50) & (G.cost_bps == COST_LIVE)].iloc[0]
    d1 = max(abs(a.cell_CAGR - C1461_ANCH["CAGR"]), abs(a.cell_Sharpe - C1461_ANCH["Sharpe"]),
             abs(a.cell_MaxDD - C1461_ANCH["MaxDD"]),
             abs(a.cell_OOS_Sharpe - C1461_ANCH["oSharpe"]))
    d2 = max(abs(q.cell_CAGR - C1461_CAND["CAGR"]), abs(q.cell_Sharpe - C1461_CAND["Sharpe"]),
             abs(q.cell_MaxDD - C1461_CAND["MaxDD"]), abs(q.cell_OOS_CAGR - C1461_CAND["oCAGR"]),
             abs(q.cell_OOS_Sharpe - C1461_CAND["oSharpe"]),
             abs(q.cell_OOS_MaxDD - C1461_CAND["oMaxDD"]))
    say(f"\n-- G1 CROSS-SCRIPT REPLAY of idea 1461's committed U56 cells @ {COST_LIVE:.0f} bps --")
    say(f"   anchor    H=126 c=0.00 : {a.cell_CAGR:.2%} / {a.cell_Sharpe:.4f} / "
        f"{a.cell_MaxDD:.2%}  OOS Sharpe {a.cell_OOS_Sharpe:.4f}   "
        f"(committed 15.80% / 1.1537 / -19.13%, OOS 1.1857)")
    say(f"   candidate H=142 c=0.50 : {q.cell_CAGR:.2%} / {q.cell_Sharpe:.4f} / "
        f"{q.cell_MaxDD:.2%}  OOS {q.cell_OOS_CAGR:.2%} / {q.cell_OOS_Sharpe:.4f} / "
        f"{q.cell_OOS_MaxDD:.2%}   (committed 15.47% / 1.2103 / -19.47%; "
        f"OOS 17.25% / 1.2350 / -19.47%)")
    gate("G1 cross-script replay of idea 1461's committed U56 anchor + candidate",
         f"worst dev {max(d1, d2):.2e} (rounding of 4-dp publications)", "<= 6e-4",
         max(d1, d2) <= 6e-4)

    # ---------------------------------------------------------- the answer
    say("\n" + "=" * 136)
    say("THE ANSWER, LEG BY LEG -- does the band beat its own CAGR-MATCHED DE-GROSS TWIN?")
    say("=" * 136)
    Ball = G[G.c > 0].copy()                             # c = 0 is inert (cell IS its twin)
    B = Ball[Ball.twin_feasible].copy()
    INF = Ball[~Ball.twin_feasible]
    say(f"\n  TWIN-D FEASIBILITY.  {len(INF)} of {len(Ball)} biting cells have NO feasible "
        f"CAGR-matched de-gross twin: the band book out-earns the FULLY INVESTED (gross 1.00) "
        f"equal-weight anchor, and matching its CAGR would need LEVERAGE, which PROTOCOL rule 2 "
        f"forbids.  Those cells are EXCLUDED from every 'beats its twin' count below and named "
        f"here rather than silently matched at the ceiling:")
    if len(INF):
        say(INF[["panel", "H", "c", "cost_bps", "cell_CAGR", "twin_CAGR", "twin_k"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n-- dMaxDD (cell minus TWIN-D, pp; POSITIVE = the band buys MORE protection at "
        f"matched CAGR), by panel x cost, over the {len(B)} BITING cells --")
    say(B.pivot_table(index=["panel", "H"], columns="cost_bps", values="dMaxDD_pp",
                      aggfunc="mean").to_string(float_format=lambda x: f"{x:+.3f}"))
    say("\n-- dSharpe (cell minus TWIN-D), by panel x cost --")
    say(B.pivot_table(index=["panel", "H"], columns="cost_bps", values="dSharpe",
                      aggfunc="mean").to_string(float_format=lambda x: f"{x:+.4f}"))
    say(f"\n-- how often the band BEATS its twin, of {len(B)} biting-and-feasible cells --")
    say(B.groupby(["panel", "cost_bps"])[["beats_twin_dd", "beats_twin_sharpe",
                                          "beats_twin_both"]].sum().to_string())
    say(f"   TOTAL: DD {int(B.beats_twin_dd.sum())} of {len(B)};  "
        f"Sharpe {int(B.beats_twin_sharpe.sum())} of {len(B)};  "
        f"BOTH {int(B.beats_twin_both.sum())} of {len(B)}")

    say("\n-- BOTH KEEP PATHS at EVERY grid point (PROTOCOL rule 4) --")
    say(G.groupby(["panel", "cost_bps"])[["cell_4a", "cell_4b", "cell_4b_OOS",
                                          "twin_4a", "twin_4b", "twin_4b_OOS"]].sum().to_string())
    say(f"   TOTAL over {len(G)} cells: cell 4a {int(G.cell_4a.sum())}, "
        f"cell 4b FULL {int(G.cell_4b.sum())}, cell 4b OOS {int(G.cell_4b_OOS.sum())};  "
        f"twin 4a {int(G.twin_4a.sum())}, twin 4b FULL {int(G.twin_4b.sum())}, "
        f"twin 4b OOS {int(G.twin_4b_OOS.sum())}")
    say("\n-- which 4b LEG BINDS on the failures (cells failing 4b FULL) --")
    F = G[~G.cell_4b]
    say("   " + ", ".join(f"{k}: {int((~F['leg_' + k]).sum())} of {len(F)}"
                          for k in ("H1", "H2", "OOS", "DD", "CAGR")))

    say(f"\n-- the CANDIDATE's OWN CELL (U56, H=142, c=0.50) across the whole cost ladder --")
    cc = G[(G.panel == "U56") & (G.H == 142) & (G.c == 0.50)].sort_values("cost_bps")
    say(cc[["cost_bps", "cell_CAGR", "cell_Sharpe", "cell_MaxDD", "cell_OOS_CAGR",
            "cell_OOS_Sharpe", "cell_OOS_MaxDD", "twin_k", "twin_MaxDD", "twin_Sharpe",
            "dMaxDD_pp", "dSharpe", "cell_4a", "cell_4b", "cell_4b_OOS", "twin_4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n-- TWIN-P (rank PERMUTATION, identical multiset, beta ORDER destroyed) @ "
        f"{COST_LIVE:.0f} bps, {PERM_SEEDS} seeds --")
    say(TP[["panel", "H", "c", "real_Sharpe", "permP_Sharpe", "se_Sharpe", "t_Sharpe",
            "real_MaxDD", "permP_MaxDD", "se_MaxDD", "t_MaxDD", "frac_perm_dd_better",
            "frac_perm_sharpe_better"]].to_string(index=False,
                                                  float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------- rule 8
    say("\n" + "=" * 136)
    say("PROTOCOL RULE 8 -- WALK-FORWARD.  (H, c) chosen on warm-up..2016-12-31 ONLY; "
        "2017-2026 read ONCE.  FOUR pre-registered choosers, one ZERO-PARAMETER.")
    say("=" * 136)
    for pan in panels:
        n_oos = len(pan.oos)
        spy_is = dict(zip(("H1", "H2"), halves(pan.spy[pan.is_rows])))
        spy_is.update(triple(pan.spy[pan.is_rows]))
        spy_oos = dict(zip(("H1", "H2"), halves(pan.spy[pan.oos])))
        spy_oos.update(triple(pan.spy[pan.oos]))
        for H in HS:
            segs = segments(pan, I_N, H)
            for c in CS:
                bk = run_book(pan, segs, cell_weights(pan, segs, c))
                for cst in COSTS:
                    r_is = net_of(bk, cst)[pan.is_rows]
                    mi, (h1i, h2i) = triple(r_is), halves(r_is)
                    nlegs = (int(h1i > spy_is["H1"]) + int(h2i > spy_is["H2"])
                             + int(mi["MaxDD"] >= DD_CAP * spy_is["MaxDD"])
                             + int(mi["CAGR"] >= CAGR_FLOOR * spy_is["CAGR"]))
                    r_o = net_of(bk, cst)[pan.oos]
                    mo, (h1o, h2o) = triple(r_o), halves(r_o)
                    wf_rows.append(dict(panel=pan.name, H=H, c=c, cost_bps=cst,
                                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                                        IS_MaxDD=mi["MaxDD"], IS_legs=nlegs,
                                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                        OOS_MaxDD=mo["MaxDD"], OOS_H1=h1o, OOS_H2=h2o,
                                        spy_OOS_CAGR=spy_oos["CAGR"],
                                        spy_OOS_Sharpe=spy_oos["Sharpe"],
                                        spy_OOS_MaxDD=spy_oos["MaxDD"],
                                        OOS_4b=keep4b_oos(dict(CAGR=mo["CAGR"],
                                                               Sharpe=mo["Sharpe"],
                                                               MaxDD=mo["MaxDD"],
                                                               H1=h1o, H2=h2o), spy_oos)))
    W = pd.DataFrame(wf_rows)
    gate("G9 the choosers read NO row on or after 2017-01-01",
         f"IS rows end {panels[0].idx[panels[0].is_rows[-1]].date()}", "< 2017-01-01",
         panels[0].idx[panels[0].is_rows[-1]] < pd.Timestamp(OOS_START))

    # exchange rate, IS only: dMaxDD_pp / dCAGR_pp vs that H's OWN c = 0 anchor (1444's currency)
    picks = []
    for (p_, cst), sub in W.groupby(["panel", "cost_bps"]):
        anc = {h: sub[(sub.H == h) & (sub.c == 0.0)].iloc[0] for h in HS}
        biting = sub[sub.c > 0].copy()
        biting["xrate"] = [
            (100 * (r.IS_MaxDD - anc[r.H].IS_MaxDD)) /
            (100 * (r.IS_CAGR - anc[r.H].IS_CAGR)) if abs(r.IS_CAGR - anc[r.H].IS_CAGR) > 1e-9
            else np.nan for r in biting.itertuples()]
        ch = {
            "C_ISSHARPE": sub.sort_values(["IS_Sharpe"], ascending=False).iloc[0],
            "C_ISLEGS": sub.sort_values(["IS_legs", "IS_Sharpe"], ascending=False).iloc[0],
            "C_STEEP": (biting.sort_values("xrate").iloc[0]
                        if biting.xrate.notna().any() else sub.iloc[0]),
            "C_ZERO (0 params: frozen incumbent H=126 c=0)":
                sub[(sub.H == 126) & (sub.c == 0.0)].iloc[0],
        }
        for nm, row in ch.items():
            picks.append(dict(panel=p_, cost_bps=cst, chooser=nm, pick_H=int(row.H),
                              pick_c=float(row.c), OOS_CAGR=row.OOS_CAGR,
                              OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                              OOS_4b=bool(row.OOS_4b),
                              spy_OOS_Sharpe=row.spy_OOS_Sharpe,
                              spy_OOS_CAGR=row.spy_OOS_CAGR,
                              spy_OOS_MaxDD=row.spy_OOS_MaxDD,
                              picks_the_candidate=bool(p_ == "U56" and row.H == 142
                                                       and row.c == 0.50)))
    P = pd.DataFrame(picks)
    say("\n-- every chooser's PICK and its OOS reading (2017-2026, read ONCE) --")
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n-- mean OOS Sharpe by chooser (over {P.panel.nunique()} panels x "
        f"{P.cost_bps.nunique()} cost rungs) --")
    say(P.groupby("chooser")[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say("-- OOS 4b passes by chooser, and how often each REACHES the 1472 candidate --")
    say(P.groupby("chooser")[["OOS_4b", "picks_the_candidate"]].sum().to_string())
    say(f"   best legal IS-only chooser by mean OOS Sharpe: "
        f"{P.groupby('chooser').OOS_Sharpe.mean().idxmax()}")

    # ---------------------------------------------------------- the bar
    say("\n" + "=" * 136)
    say("THE PRE-REGISTERED BAR, READ AT THE LIVE CELL (U56, H=142, c=0.50, 10 bps)")
    say("=" * 136)
    h = G[(G.panel == "U56") & (G.H == 142) & (G.c == 0.50)
          & (G.cost_bps == COST_LIVE)].iloc[0]
    reach = int(P[(P.panel == "U56") & (P.cost_bps == COST_LIVE)].picks_the_candidate.sum())
    b_i = bool(h.cell_MaxDD > h.twin_MaxDD)
    b_ii = bool(h.cell_Sharpe > h.twin_Sharpe)
    b_iii = bool(h.cell_4b and h.cell_4b_OOS)
    b_iv = reach > 0
    say(f"  (i)   MaxDD {h.cell_MaxDD:.2%} vs TWIN-D {h.twin_MaxDD:.2%} "
        f"(k={h.twin_k:.4f}, matched CAGR {h.cell_CAGR:.2%} vs {h.twin_CAGR:.2%}) "
        f"-> d {h.dMaxDD_pp:+.3f} pp  : {'PASS' if b_i else 'FAIL'}")
    say(f"  (ii)  Sharpe {h.cell_Sharpe:.4f} vs TWIN-D {h.twin_Sharpe:.4f} "
        f"-> d {h.dSharpe:+.4f}  : {'PASS' if b_ii else 'FAIL'}")
    say(f"  (iii) 4b FULL {bool(h.cell_4b)} and 4b OOS {bool(h.cell_4b_OOS)}  "
        f": {'PASS' if b_iii else 'FAIL'}")
    say(f"  (iv)  reached by {reach} of 4 legal IS-only choosers at this cell "
        f": {'PASS' if b_iv else 'FAIL'}")
    survives = b_i and b_ii and b_iii and b_iv
    verdict_txt = ("SURVIVES -- the FIRST band cell in the record that is not the exposure "
                   "scalar" if survives else "DOES NOT SURVIVE the pre-registered bar")
    say(f"\n  ANSWERED: the beta band at U56 H=142 c=0.50 {verdict_txt}.")

    ngates = sum(1 for g in GATES if g["target"] != "published, not asserted")
    npass = sum(1 for g in GATES if g["target"] != "published, not asserted" and g["pass_"])
    say(f"\nGATES: {npass} of {ngates} pass.  Cells published: {len(G)}.  "
        f"Runtime {time.time()-t0:.0f}s.")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    TP.to_csv(f"{OUT}.permtwin.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P.to_csv(f"{OUT}.picks.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"wrote {OUT}.grid.csv / .permtwin.csv / .walkforward.csv / .picks.csv / "
        f".gates.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

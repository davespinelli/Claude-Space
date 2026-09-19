#!/usr/bin/env python3
"""
Idea 1354 (lane cloud, 2026-09-18) — is WEEKLY still the CADENCE ARGMAX at EVERY N, or only at
the incumbent's 15?

THE PREMISE, READ FROM THIS RUN'S OWN FIRST IDEA.  Idea 1335 (committed earlier today) walked
CADENCE {D, W, 2W, M, Q} x COST {0, 10, 25, 50} bps at the frozen incumbent and established two
things: the cadence argmax does NOT move with the cost rung on any of the three panels (0 of 3),
and W is BOTH the full-sample and the out-of-sample Sharpe argmax on U56, the only panel this
family has ever cleared 4b on.  But every one of those 60 cells was measured at the SINGLE
FROZEN WIDTH N = 15.  'Weekly wins' is therefore, on the evidence so far, a statement about one
point of the width dial — and N is the dial this record tunes more often than any other.  If the
cadence argmax moves with N, 1335's headline is an N=15 artifact and so is the incumbent's
inherited cadence.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  N       {10, 15, 20, 30}          DIAL 1 — 15 is the incumbent's value
  CADENCE {D, W, 2W, M, Q}          DIAL 2 — W is PROTOCOL's default and the incumbent's value

  20 cells per panel, 60 in all, EVERY ONE published in `.grid.csv`.

  GROSS is FROZEN at the incumbent's 0.60 and COST at PROTOCOL rule 2's 10 bps — 1335 already
  showed the cadence ranking is invariant to the cost rung on all three panels, so re-sweeping
  it here would add a third dial and no information.

THE BOOK, OTHERWISE FROZEN.  The record's certified incumbent: 3-leg rank composite
((21,252), (0,126), (0,63)) x the `0.5 + 0.5*above-200d` tilt, eligibility = above 200d MA AND
vol20 < 0.60, N names at equal weight, minimum hold H = 126 trading days, gross 0.60, decisions
lagged one row and applied at t+1 (rule 2).

WHAT IS BEING ASKED, PRECISELY.  For each (panel, N) the cadence that maximises Sharpe, and for
each (panel, cadence) the N that maximises it — published as a full 4 x 5 matrix per panel, plus
the SEPARATION of the two dials (how much Sharpe spread each one commands) so the run says which
dial is binding rather than only whether one moved.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; the IS and OOS windows; turnover and its 10 bps drag in bp/yr at every cell.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (N=15, W) incumbent — the book nobody had to choose.

PROTOCOL: rule 1 (>= 10 years, G0); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3
(RULES v2 AND SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: the
(N, CADENCE) PAIR chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored
against PROTOCOL's own (15, W)); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified.

WITHIN-DAY REPLAY (gate G1): the (N=15, W) cell must reproduce idea 1335's committed
`.grid.csv` U56 W/10bps row to < 5e-6 on all of CAGR, Sharpe, MaxDD, both halves, OOS Sharpe, IS
Sharpe and turnover — same tape, same day, so this one IS bit-tight, unlike 1335's own
cross-vintage gate against idea 1305.

TAPE STAMP (the caveat idea 1335 measured and idea 1350 was filed to chase): every panel's row
count and last date are printed and written to `.gates.csv`, because commit 4e19a80 rewrote
data/prices*.csv wholesale earlier today and no committed number in this family carries one.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_is-WEEKLY-still-the-CADENCE-ARGMAX-at-EVERY-N-or-only-at-the-incumbent-s-15_cloud.py
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

DATE = "2026-09-18"
SLUG = "is-WEEKLY-still-the-CADENCE-ARGMAX-at-EVERY-N-or-only-at-the-incumbent-s-15"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_H, I_G = 126, 0.60                              # frozen: min hold, gross
COST = 10.0                                       # frozen: PROTOCOL rule 2's rung
NS = [10, 15, 20, 30]                             # DIAL 1
CADENCES = ["D", "W", "2W", "M", "Q"]             # DIAL 2
ANCHOR_N, ANCHOR_CAD = 15, "W"                    # the incumbent / PROTOCOL default
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# idea 1335's committed .grid.csv, U56 / cadence W / cost 10 bps — within-day replay gate G1
C1335_U56_W = dict(CAGR=0.1367020011892825, Sharpe=1.17166235540161, MaxDD=-0.163814812515476,
                   H1=1.2526855979053693, H2=1.121880836109541,
                   OOS_Sharpe=1.1964884282955432, IS_Sharpe=1.148194160527367,
                   turn=2.463043347965852)

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
    """Identical to idea 1335's: D/W/M/Q from the engine's own mask (decided at the period's
    last close, applied the next row), 2W the W array subsampled every second entry."""
    if cad == "2W":
        return cadence_rows(idx, "W")[::2]
    m = rebalance_mask(idx, cad).shift(1, fill_value=False).values.copy()
    m[0] = True
    return np.flatnonzero(m)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.reb = {c: cadence_rows(px.index, c) for c in CADENCES}
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, reb, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2."""
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


def run_flat(pan, reb, frame, gross=I_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = gross * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


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


def main():
    t0 = time.time()
    say("=" * 112)
    say("IDEA 1354 (lane cloud, 2026-09-18) — is WEEKLY still the CADENCE ARGMAX at EVERY N, or "
        "only at the incumbent's 15?")
    say("DIALS: N {10,15,20,30} x CADENCE {D,W,2W,M,Q} at the frozen incumbent (H=126, gross "
        "0.60, MAXVOL 0.60, MA gate ON, 10 bps, t+1).")
    say("=" * 112)

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
        say("  SMALL filter: data/small_meta.csv absent; falling back to an in-panel "
            "max |1d move| >= 1.0 screen.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a "
        "sub-$2B screen carried back to 2010, so its LEVELS are an upper bound and only its "
        "CONTRASTS across N and cadence are read here.")
    say("  TAPE STAMP (the caveat idea 1335 measured; idea 1350 filed to chase it):")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  rebalances "
            + " / ".join(f"{c} {len(p.reb[c])}" for c in CADENCES))
        GATES.append(dict(gate=f"TAPE STAMP {p.name}",
                          value=f"{len(p.idx)} rows, {p.idx[0].date()}..{p.idx[-1].date()}",
                          target="published, not asserted", pass_=True))
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows, bench = [], [], {}

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY: CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps: CAGR {live['CAGR']:.2%} Sharpe "
            f"{live['Sharpe']:.4f} MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.4f}/"
            f"{live['H2']:.4f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")
        say(f"    {'N':>3} {'cad':>3} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} "
            f"{'H2':>6} | {'turn':>5} {'drag':>6} {'vol':>6} | {'OOSCAGR':>8} {'OOSShrp':>7} "
            f"{'OOSMaxDD':>8} | {'ISShrp':>7} | 4a 4b  fail-legs")
        runs = {}
        for N in NS:
            for cad in CADENCES:
                reb = pan.reb[cad]
                frame = build1(pan, reb, N, I_H)
                g, tu = run_flat(pan, reb, frame)
                rr = g - tu * COST / 1e4
                r = rr[WARMUP:]
                turn = annturn(tu, WARMUP, n)
                ka, kb, m, h1, h2, legs = keep_paths(r, spy, live)
                mo = triple(rr[i_oos:])
                kb_oos = bool(mo["Sharpe"] > spyO["Sharpe"])
                runs[(N, cad)] = rr
                row = dict(panel=pan.name, N=N, cadence=cad,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           vol_real=annvol(r), turn=turn, cost_drag_bp=turn * COST,
                           n_rebal=len(reb),
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           IS_Sharpe=sharpe(rr[WARMUP:i_oos]),
                           SPY_Sharpe=spy["Sharpe"], SPY_CAGR=spy["CAGR"],
                           SPY_MaxDD=spy["MaxDD"], LIVE_Sharpe=live["Sharpe"],
                           LIVE_MaxDD=live["MaxDD"], OOS_SPY_Sharpe=spyO["Sharpe"],
                           OOS_SPY_CAGR=spyO["CAGR"], OOS_SPY_MaxDD=spyO["MaxDD"],
                           OOS_LIVE_Sharpe=liveO["Sharpe"],
                           keep4a=ka, keep4b=kb, keep4b_oos_sharpe=kb_oos,
                           keep4b_and_oos=bool(kb and kb_oos),
                           leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                           leg_CAGR=legs["CAGR"])
                grid.append(row)
                say(f"    {N:>3} {cad:>3} | {m['CAGR']:7.2%} {m['Sharpe']:7.4f} "
                    f"{m['MaxDD']:8.2%} {h1:6.3f} {h2:6.3f} | {turn:5.2f} {turn*COST:6.1f} "
                    f"{annvol(r):6.2%} | {mo['CAGR']:8.2%} {mo['Sharpe']:7.4f} "
                    f"{mo['MaxDD']:8.2%} | {row['IS_Sharpe']:7.4f} | {int(ka)}  {int(kb)}   "
                    + (",".join(k for k, v in legs.items() if not v) or "-"))
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, runs=runs,
                               i_oos=i_oos, n=n)

        if pan.name == "U56":
            a = [r for r in grid if r["panel"] == "U56" and r["N"] == ANCHOR_N
                 and r["cadence"] == ANCHOR_CAD][0]
            for k, v in C1335_U56_W.items():
                gate(f"G1 within-day replay of idea 1335's U56 (N=15, W) @10bps {k}",
                     round(a[k], 10), round(v, 10), abs(a[k] - v) < 5e-6)

    G = pd.DataFrame(grid)

    # ---- 1. the question ------------------------------------------------------------------
    say("\n" + "=" * 112)
    say("1. IS W THE CADENCE ARGMAX AT EVERY N?  (full-sample Sharpe argmax over the 5 cadences, "
        "at each N)")
    say("=" * 112)
    am = []
    for p in G.panel.unique():
        line = []
        for N in NS:
            sub = G[(G.panel == p) & (G.N == N)]
            best = sub.loc[sub.Sharpe.idxmax()]
            wr = sub[sub.cadence == ANCHOR_CAD].iloc[0]
            line.append(f"N={N}->{best.cadence}({best.Sharpe:.4f}; W {wr.Sharpe:.4f}, "
                        f"gap {best.Sharpe-wr.Sharpe:+.4f})")
            am.append(dict(panel=p, N=N, basis="FULL_SHARPE", argmax=best.cadence,
                           argmax_Sharpe=best.Sharpe, W_Sharpe=wr.Sharpe,
                           gap_vs_W=best.Sharpe - wr.Sharpe))
        say(f"    {p:>6}: " + "   ".join(line))
    for p in G.panel.unique():
        a = [r["argmax"] for r in am if r["panel"] == p]
        say(f"      -> {p}: cadence argmax across N {NS} = {a}  "
            f"{'STABLE' if len(set(a)) == 1 else 'MOVES'}")
    moves = sum(len({r['argmax'] for r in am if r['panel'] == p}) > 1 for p in G.panel.unique())
    say(f"    ANSWER: the cadence argmax MOVES WITH N on {moves} of {G.panel.nunique()} panels; "
        f"W is the argmax in {sum(1 for r in am if r['argmax'] == ANCHOR_CAD)} of {len(am)} "
        f"(panel, N) cells.")

    say("\n    ... and the same question the other way round (Sharpe argmax over N, at each "
        "cadence):")
    for p in G.panel.unique():
        line = []
        for cad in CADENCES:
            sub = G[(G.panel == p) & (G.cadence == cad)]
            best = sub.loc[sub.Sharpe.idxmax()]
            line.append(f"{cad}->N={int(best.N)}({best.Sharpe:.4f})")
            am.append(dict(panel=p, N=np.nan, basis="FULL_SHARPE_over_N", argmax=int(best.N),
                           argmax_Sharpe=best.Sharpe, W_Sharpe=np.nan, gap_vs_W=np.nan,
                           cadence=cad))
        say(f"    {p:>6}: " + "   ".join(line))

    say("\n2. WHICH DIAL BINDS?  (mean within-panel Sharpe spread commanded by each dial)")
    for p in G.panel.unique():
        s = G[G.panel == p]
        sp_cad = float(np.mean([s[s.N == N].Sharpe.max() - s[s.N == N].Sharpe.min()
                               for N in NS]))
        sp_n = float(np.mean([s[s.cadence == c].Sharpe.max() - s[s.cadence == c].Sharpe.min()
                             for c in CADENCES]))
        sp_cad_o = float(np.mean([s[s.N == N].OOS_Sharpe.max() - s[s.N == N].OOS_Sharpe.min()
                                 for N in NS]))
        sp_n_o = float(np.mean([s[s.cadence == c].OOS_Sharpe.max()
                                - s[s.cadence == c].OOS_Sharpe.min() for c in CADENCES]))
        say(f"    {p:>6}: full-sample spread  CADENCE {sp_cad:.4f}  vs  N {sp_n:.4f}  "
            f"({sp_cad/sp_n:.2f}x)   |   OOS spread  CADENCE {sp_cad_o:.4f}  vs  N "
            f"{sp_n_o:.4f}  ({sp_cad_o/sp_n_o:.2f}x)   -> binding dial: "
            f"{'CADENCE' if sp_cad > sp_n else 'N'}")

    say("\n3. KEEP PATHS OVER ALL 60 CELLS ----------------------------------------------")
    say(f"    4a (beat the live book): {int(G.keep4a.sum())} of {len(G)}")
    say(f"    4b full-sample: {int(G.keep4b.sum())} of {len(G)};  4b full AND OOS Sharpe > SPY: "
        f"{int(G.keep4b_and_oos.sum())} of {len(G)}")
    for p in G.panel.unique():
        s = G[G.panel == p]
        say(f"      {p:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}"
            f"   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for N in NS:
        s = G[G.N == N]
        say(f"      N={N:>2}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for cad in CADENCES:
        s = G[G.cadence == cad]
        say(f"      cad {cad:>2}: 4a {int(s.keep4a.sum())}/{len(s)}   4b "
            f"{int(s.keep4b.sum())}/{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    say("    Cells that BEAT the frozen (N=15, W) incumbent on full-sample Sharpe AND pass 4b "
        "full+OOS:")
    any_dom = False
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.N == ANCHOR_N) & (G.cadence == ANCHOR_CAD)].iloc[0]
        d = G[(G.panel == p) & (G.Sharpe > anc.Sharpe) & G.keep4b_and_oos]
        if len(d):
            any_dom = True
            for r in d.itertuples():
                say(f"      {p} N={r.N} {r.cadence}: {r.Sharpe:.4f} vs anchor {anc.Sharpe:.4f} "
                    f"(+{r.Sharpe-anc.Sharpe:.4f}), OOS {r.OOS_Sharpe:.4f} vs "
                    f"{anc.OOS_Sharpe:.4f}, MaxDD {r.MaxDD:.2%}")
    if not any_dom:
        say("      NONE on any panel.")

    # ---- rule 8 ---------------------------------------------------------------------------
    say("\n4. RULE 8 WALK-FORWARD — the (N, CADENCE) PAIR chosen on warm-up..2016-12-31 by argmax "
        "IS Sharpe; 2017-2026 read ONCE")
    say("=" * 112)
    for p in G.panel.unique():
        b = bench[p]
        sub = G[G.panel == p]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        anc = sub[(sub.N == ANCHOR_N) & (sub.cadence == ANCHOR_CAD)].iloc[0]
        ro = b["runs"][(int(pick.N), pick.cadence)][b["i_oos"]:]
        h1o, h2o = halves(ro)
        legs_oos = dict(OOS_Sharpe_vs_SPY=bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"]),
                        DD=bool(pick.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                        CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        best_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
        wf = dict(panel=p, IS_pick_N=int(pick.N), IS_pick_cadence=pick.cadence,
                  IS_Sharpe=pick.IS_Sharpe,
                  is_the_incumbent=bool(pick.N == ANCHOR_N and pick.cadence == ANCHOR_CAD),
                  OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                  OOS_H1=h1o, OOS_H2=h2o,
                  ANCHOR_OOS_CAGR=anc.OOS_CAGR, ANCHOR_OOS_Sharpe=anc.OOS_Sharpe,
                  ANCHOR_OOS_MaxDD=anc.OOS_MaxDD,
                  dOOS_Sharpe_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                  dOOS_CAGR_vs_anchor=pick.OOS_CAGR - anc.OOS_CAGR,
                  SPY_OOS_CAGR=b["spyO"]["CAGR"], SPY_OOS_Sharpe=b["spyO"]["Sharpe"],
                  SPY_OOS_MaxDD=b["spyO"]["MaxDD"],
                  LIVE_OOS_CAGR=b["liveO"]["CAGR"], LIVE_OOS_Sharpe=b["liveO"]["Sharpe"],
                  LIVE_OOS_MaxDD=b["liveO"]["MaxDD"],
                  keep4b_oos_all=bool(all(legs_oos.values())),
                  oos_fail_legs=",".join(k for k, v in legs_oos.items() if not v) or "-",
                  best_OOS_N=int(best_oos.N), best_OOS_cadence=best_oos.cadence,
                  best_OOS_Sharpe=best_oos.OOS_Sharpe)
        wf_rows.append(wf)
        say(f"    {p:>6}: IS pick (N={int(pick.N)}, {pick.cadence}) IS Sharpe "
            f"{pick.IS_Sharpe:.4f} -> OOS {pick.OOS_CAGR:7.2%}/{pick.OOS_Sharpe:.4f}/"
            f"{pick.OOS_MaxDD:7.2%}")
        say(f"            vs FROZEN (N=15, W)  {anc.OOS_CAGR:7.2%}/{anc.OOS_Sharpe:.4f}/"
            f"{anc.OOS_MaxDD:7.2%}   d Sharpe {pick.OOS_Sharpe-anc.OOS_Sharpe:+.4f}, d CAGR "
            f"{pick.OOS_CAGR-anc.OOS_CAGR:+.2%}")
        say(f"            vs SPY {b['spyO']['CAGR']:7.2%}/{b['spyO']['Sharpe']:.4f}/"
            f"{b['spyO']['MaxDD']:7.2%}   vs RULES v2 {b['liveO']['CAGR']:7.2%}/"
            f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:7.2%}")
        say(f"            4b on every OOS leg: {int(wf['keep4b_oos_all'])} "
            f"[{wf['oos_fail_legs']}]   | ex-post best OOS cell (N={wf['best_OOS_N']}, "
            f"{wf['best_OOS_cadence']}) {wf['best_OOS_Sharpe']:.4f}")

    WF = pd.DataFrame(wf_rows)
    say(f"\n    The IS chooser lands on the frozen incumbent (N=15, W) in "
        f"{int(WF.is_the_incumbent.sum())} of {len(WF)} panels.")
    say(f"    Mean OOS Sharpe of the IS-chosen PAIR minus the frozen incumbent: "
        f"{WF.dOOS_Sharpe_vs_anchor.mean():+.4f} (min {WF.dOOS_Sharpe_vs_anchor.min():+.4f}, "
        f"max {WF.dOOS_Sharpe_vs_anchor.max():+.4f}); it beats the incumbent in "
        f"{int((WF.dOOS_Sharpe_vs_anchor > 0).sum())} of {len(WF)}.")
    say(f"    Mean OOS CAGR difference: {WF.dOOS_CAGR_vs_anchor.mean():+.2%}")
    say(f"    4b on every OOS leg after rule 8: {int(WF.keep4b_oos_all.sum())} of {len(WF)}.")
    hind = int(((WF.best_OOS_N != WF.IS_pick_N)
                | (WF.best_OOS_cadence != WF.IS_pick_cadence)).sum())
    say(f"    H_HINDSIGHT: the ex-post best OOS cell differs from the IS pick on {hind} of "
        f"{len(WF)} panels.")

    say("\n5. THE CADENCE LADDER AT EVERY N, OOS (2017-2026), for the reader who wants the raw "
        "shape")
    for p in G.panel.unique():
        for N in NS:
            sub = G[(G.panel == p) & (G.N == N)].sort_values("OOS_Sharpe", ascending=False)
            order = list(sub.cadence)
            say(f"    {p:>6} N={N:>2}: "
                + " > ".join(f"{r.cadence}({r.OOS_Sharpe:.4f})" for r in sub.itertuples())
                + f"   -> W ranks {order.index('W')+1} of 5")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(am).to_csv(f"{OUT}.argmax.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {Path(OUT).name}.grid.csv ({len(G)} cells), .walkforward.csv ({len(WF)}), "
        f".argmax.csv, .gates.csv")
    asserted = [g for g in GATES if g["target"] != "published, not asserted"]
    say(f"  GATES: {sum(g['pass_'] for g in asserted)}/{len(asserted)} asserted pass "
        f"(plus {len(GATES)-len(asserted)} published tape stamps)")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

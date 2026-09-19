#!/usr/bin/env python3
"""
Idea 1409 (lane cloud, 2026-09-19, idea 2 of 2) — is the incumbent's 4b DD MARGIN a LOOKBACK-SKIP
ARTEFACT?

THE PREMISE.  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly
Fri-decide / Mon-trade, 10 bps, t+1) passes 4b on ONE leg by ONE margin: MaxDD -19.13% against a
-20.23% cap, **+1.10 pp**.  Idea 1257 priced the composite's leg SUBSETS but froze each leg's own
(skip, length).  The 12-1 leg's **21-day skip** is therefore an UNPRICED DIAL, and it is not a
cosmetic one: the skip decides whether the book buys the names that have just fallen or the names
that have just risen, i.e. whether it runs INTO or AWAY FROM a crash — which is exactly where a
-19.13% is made.  If the DD margin moves more than its own 1.10 pp across that dial, the committed
pass is a LOOKBACK CONVENTION, not a property of the strategy.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  SKIP  {0, 5, 10, 21, 42}   DIAL 1 — 21 is the incumbent's (the "12-1" convention)
  LONG  {189, 252}           DIAL 2 — 252 is the incumbent's (the "12" in 12-1)

  10 cells per panel, 30 in all, EVERY ONE published in .grid.csv.  (21, 252) IS THE FROZEN
  INCUMBENT and is present in the grid as its own cell (gate G1).

WHAT IS AND IS NOT TOUCHED.  Only the composite's FIRST leg moves.  The other two legs stay frozen
at (0, 126) and (0, 63), as do N = 20, H = 126, gross 0.75, MAXVOL 0.60, the 200d MA gate, the
weekly cadence, the 10 bps and the t+1 lag.  The skip is applied the way the live scorer applies
it: `px.shift(SKIP) / px.shift(LONG) - 1`, cross-sectionally rank-transformed, so SKIP < LONG is
enforced by construction and every cell is a legal book.

THE STATISTIC THAT ANSWERS THE QUESTION.  Not the level of MaxDD but the **DD MARGIN**,
`MaxDD - 0.60 x SPY MaxDD`, published at every cell beside the CAGR margin.  The idea's own bar is
pre-registered: **if the U56 DD margin's spread across the 10 cells exceeds 1.10 pp, the committed
pass is a convention.**  That bar is stated here BEFORE the numbers and is not moved afterwards.

RESOLVABILITY, not just sign.  Every cell's Sharpe gap against the frozen (21, 252) anchor is
scored by a PAIRED circular-block bootstrap (400 reps x 63-row blocks, seed 20260919, identical
block starts for both books), full sample and OOS.  |t| > 2 is the record's bar; a gap inside its
own SE is published as UNRESOLVED, not as a finding.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; per-cell name overlap
with the anchor book (how much of the difference is even a different portfolio).

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the frozen
(21, 252) incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (SKIP, LONG) chosen on
warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen anchor);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

GATES.  G1 CROSS-SCRIPT REPLAY: the (21, 252) cell must reproduce the committed U56 anchor
(15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS) to < 5e-3 of Sharpe.  G2 SKIP < LONG
at every published cell.  G3 all 30 cells published.  G4 exactly two tuned parameters.  G5 the
chooser reads no row on or after 2017-01-01.  G6 no leverage: realised weight sum never exceeds
gross.  G7 the legs actually differ: max pairwise |score difference| is published, never asserted
to zero, so a "no effect" reading cannot be a silent no-op.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_lookback-skip-artefact_cloud.py
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
SLUG = "lookback-skip-artefact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
TAIL_LEGS = [(0, 126), (0, 63)]                 # frozen
I_N, I_H, I_G = 20, 126, 0.75                   # the frozen 2026-09-04 incumbent
A_SKIP, A_LONG = 21, 252                        # ... and its 12-1 leg
SKIPS = [0, 5, 10, 21, 42]
LONGS = [189, 252]
COST, CADENCE = 10.0, "W"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
PREREG_BAR = 1.1028                             # the incumbent's own committed DD margin, pp
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


def mech(q, skip, long):
    """The live composite with its FIRST leg at (skip, long); the other two legs are frozen."""
    legs = [(skip, long)] + TAIL_LEGS
    parts = []
    for sk, lk in legs:
        x = (q.shift(sk) / q.shift(lk) - 1.0) if sk else (q / q.shift(lk) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
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
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def build1(pan, rank_key, elig, N, H, lag=1):
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
            k = rank_key[ts].copy()
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
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, frame, gross):
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    wmax = 0.0
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * frame[i0]
        wmax = max(wmax, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = pan.Cp[i0]
        A = w0[None, :] * (pan.Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (pan.C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, wmax


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


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def main():
    t0 = time.time()
    say("=" * 122)
    say("IDEA 1409 (lane cloud, 2026-09-19, idea 2 of 2) — is the incumbent's 4b DD MARGIN a "
        "LOOKBACK-SKIP ARTEFACT?")
    say("DIALS: SKIP {0,5,10,21,42} x LONG {189,252} on the composite's FIRST leg only, at the "
        "frozen incumbent (N=20, H=126, gross 0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1).")
    say(f"PRE-REGISTERED BAR, stated before the numbers: if the U56 DD MARGIN spread across the 10 "
        f"cells exceeds the incumbent's own margin of {PREREG_BAR:.4f} pp, the committed 4b pass is "
        f"a LOOKBACK CONVENTION.")
    say("=" * 122)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level is an UPPER BOUND and every 4b "
        "pass an optimistic one; what this run reads is the SPREAD of one margin across one dial, "
        "on identical names and identical days.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G2 SKIP < LONG at every published cell", f"max skip {max(SKIPS)}, min long {min(LONGS)}",
         "skip < long", max(SKIPS) < min(LONGS))

    grid, wf_rows = [], []
    wmax_global, g1_ok, maxscore_dev = 0.0, None, 0.0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        cells, scores = {}, {}
        for long in LONGS:
            for skip in SKIPS:
                sc, above, vol20 = mech(pan.px[pan.invest], skip, long)
                scores[(skip, long)] = sc
                rank_key = np.where(np.isfinite(sc), -sc, np.inf)
                elig = above & (vol20 < MAXVOL)
                frame = build1(pan, rank_key, elig, I_N, I_H)
                gg, tu, wm = run(pan, frame, I_G)
                wmax_global = max(wmax_global, wm)
                cells[(skip, long)] = dict(r=gg - tu * COST / 1e4, tu=tu, frame=frame)

        base = scores[(A_SKIP, A_LONG)]
        for k, sc in scores.items():
            if k != (A_SKIP, A_LONG):
                d = np.abs(sc[WARMUP:] - base[WARMUP:])
                maxscore_dev = max(maxscore_dev, float(np.nanmax(d)))

        anchor = cells[(A_SKIP, A_LONG)]["r"]
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        af = cells[(A_SKIP, A_LONG)]["frame"]
        say(f"           FROZEN INCUMBENT (skip 21, long 252)  CAGR {am['CAGR']:.2%} Sharpe "
            f"{am['Sharpe']:.4f} MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS "
            f"{ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                         "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                         f"|dSharpe| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        for long in LONGS:
            for skip in SKIPS:
                c = cells[(skip, long)]
                rr = c["r"]
                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
                dsh, se, tst = paired_block_dsharpe(rr[WARMUP:], anchor[WARMUP:])
                dshO, seO, tO = paired_block_dsharpe(rr[i_oos:], anchor[i_oos:])
                n = T - WARMUP
                turn_y = float(np.sum(c["tu"][WARMUP:]) * 252.0 / n)
                f, g = c["frame"][WARMUP:], af[WARMUP:]
                both = ((f > 0) & (g > 0)).sum(axis=1)
                held = np.maximum((g > 0).sum(axis=1), 1)
                grid.append(dict(
                    panel=pan.name, skip=skip, long=long, is_anchor=(skip == A_SKIP and long == A_LONG),
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO,
                    legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                    odd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"]),
                    turn_y=turn_y, drag_bpyr=turn_y * COST,
                    name_overlap=float(np.mean(both / held)),
                    d_sharpe_vs_anchor=dsh, se_vs_anchor=se, t_vs_anchor=tst,
                    d_maxdd_vs_anchor_pp=100 * (m["MaxDD"] - am["MaxDD"]),
                    od_sharpe_vs_anchor=dshO, ose_vs_anchor=seO, ot_vs_anchor=tO,
                    spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"]))

        # rule 8
        i_is0, i_is1 = WARMUP, i_oos
        best, bs = None, -np.inf
        for k, c in cells.items():
            s = sharpe(c["r"][i_is0:i_is1])
            if s > bs:
                bs, best = s, k
        rr = cells[best]["r"]
        k4aO, k4bO, mo, _, _, _ = keep_paths(rr[i_oos:], spyO, liveO)
        wf_rows.append(dict(panel=pan.name, is_skip=best[0], is_long=best[1], is_Sharpe=bs,
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4b_oos=k4bO, keep4a_oos=k4aO,
                            anchor_oCAGR=ao["CAGR"], anchor_oSharpe=ao["Sharpe"],
                            anchor_oMaxDD=ao["MaxDD"],
                            d_oSharpe_vs_anchor=mo["Sharpe"] - ao["Sharpe"],
                            d_oMaxDD_vs_anchor_pp=100 * (mo["MaxDD"] - ao["MaxDD"]),
                            spy_oSharpe=spyO["Sharpe"], spy_oCAGR=spyO["CAGR"],
                            spy_oMaxDD=spyO["MaxDD"], live_oSharpe=liveO["Sharpe"]))

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    gate("G3 all 30 grid cells published", len(G), "== 30", len(G) == 30)
    gate("G4 exactly two tuned parameters (skip, long)", "2", "== 2", True)
    gate("G5 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G6 no leverage: realised weight sum never exceeds gross",
         f"max wsum {wmax_global:.6f}", f"<= {I_G} + 1e-12", wmax_global <= I_G + 1e-12)
    gate("G7 the legs genuinely differ (max |score - anchor score|, published not asserted)",
         f"{maxscore_dev:.4e}", "> 1e-6 (a no-op would read 0)", maxscore_dev > 1e-6)

    say("\n" + "=" * 122)
    say("GRID — every cell.  DD margin = MaxDD - 0.60 x SPY MaxDD (positive = the 4b DD leg "
        "passes).  * marks the FROZEN INCUMBENT.")
    say("=" * 122)
    for pan in ["U56", "B136", "SMALL"]:
        for long in LONGS:
            sub = G[(G.panel == pan) & (G.long == long)]
            say(f"\n  [{pan} / long {long}]")
            say("    skip |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg | 4a 4b | "
                "turn drag | ovlp | dSh vs anchor   SE     t   | dDD pp | OOS CAGR/Sh/DD  oDDmarg")
            for _, r in sub.iterrows():
                mark = "*" if r.is_anchor else " "
                say(f"   {mark}{int(r.skip):3d} | {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} "
                    f"{r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} {r.cagr_margin_pp:+8.2f} | "
                    f"{int(r.keep4a)}  {int(r.keep4b)}  | {r.turn_y:4.2f} {r.drag_bpyr:5.1f} | "
                    f"{r.name_overlap:4.2f} | {r.d_sharpe_vs_anchor:+8.4f} {r.se_vs_anchor:7.4f} "
                    f"{r.t_vs_anchor:+6.2f} | {r.d_maxdd_vs_anchor_pp:+6.2f} | {r.oCAGR:7.2%} "
                    f"{r.oSharpe:6.4f} {r.oMaxDD:7.2%} {r.odd_margin_pp:+7.2f}")

    say("\n" + "=" * 122)
    say("RULE 8 WALK-FORWARD — (SKIP, LONG) chosen by argmax IS Sharpe on warm-up..2016-12-31; "
        "2017-2026 read ONCE.")
    say("=" * 122)
    say("  panel | IS pick (skip,long) IS Sh | OOS CAGR  Sharpe   MaxDD 4b | ANCHOR OOS CAGR "
        "Sharpe MaxDD | dSh | dDD pp | SPY OOS")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | ({int(r.is_skip):3d},{int(r.is_long)}) {r.is_Sharpe:6.4f} | "
            f"{r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%}  {int(r.keep4b_oos)} | "
            f"{r.anchor_oCAGR:7.2%} {r.anchor_oSharpe:7.4f} {r.anchor_oMaxDD:7.2%} | "
            f"{r.d_oSharpe_vs_anchor:+7.4f} | {r.d_oMaxDD_vs_anchor_pp:+6.2f} | "
            f"{r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 122)
    say("HEADLINE — THE PRE-REGISTERED BAR")
    say("=" * 122)
    u = G[G.panel == "U56"]
    spread = float(u.dd_margin_pp.max() - u.dd_margin_pp.min())
    anch = float(u[u.is_anchor].dd_margin_pp.iloc[0])
    say(f"  U56 DD MARGIN across the 10 cells: min {u.dd_margin_pp.min():+.4f} pp "
        f"(skip {int(u.loc[u.dd_margin_pp.idxmin(),'skip'])}, long "
        f"{int(u.loc[u.dd_margin_pp.idxmin(),'long'])}), max {u.dd_margin_pp.max():+.4f} pp "
        f"(skip {int(u.loc[u.dd_margin_pp.idxmax(),'skip'])}, long "
        f"{int(u.loc[u.dd_margin_pp.idxmax(),'long'])}), **SPREAD {spread:.4f} pp**, "
        f"anchor {anch:+.4f} pp.")
    say(f"  PRE-REGISTERED BAR {PREREG_BAR:.4f} pp  ->  "
        f"{'EXCEEDED: the committed 4b pass is a LOOKBACK CONVENTION' if spread > PREREG_BAR else 'NOT exceeded: the margin is ROBUST to the skip'}.")
    say(f"  U56 MaxDD across the 10 cells: {u.MaxDD.min():.2%} .. {u.MaxDD.max():.2%}; "
        f"Sharpe {u.Sharpe.min():.4f} .. {u.Sharpe.max():.4f} (swing "
        f"{u.Sharpe.max()-u.Sharpe.min():.4f}); name overlap with the anchor book "
        f"{u.name_overlap.min():.2f} .. {u.name_overlap.max():.2f}.")
    say(f"  4a: {int(G.keep4a.sum())} of {len(G)}.")
    for pan in ["U56", "B136", "SMALL"]:
        sp = G[G.panel == pan]
        say(f"  4b {pan}: {int(sp.keep4b.sum())} of {len(sp)} cells; DD-leg passes "
            f"{int(sp.legDD.sum())}, CAGR-leg {int(sp.legCAGR.sum())}, H1 {int(sp.legH1.sum())}, "
            f"H2 {int(sp.legH2.sum())}; DD margin spread "
            f"{float(sp.dd_margin_pp.max()-sp.dd_margin_pp.min()):.4f} pp.")
    nb = G[~G.is_anchor]
    res = nb[np.abs(nb.t_vs_anchor) > 2]
    say(f"  RESOLVABILITY: {len(res)} of {len(nb)} non-anchor cells resolve |t| > 2 against the "
        f"anchor (full sample); {int((res.d_sharpe_vs_anchor > 0).sum())} of them BEAT it. "
        f"Median |t| {np.abs(nb.t_vs_anchor).median():.2f}, median dSharpe "
        f"{nb.d_sharpe_vs_anchor.median():+.4f}.")
    say(f"  RULE 8: mean OOS Sharpe of the IS-chosen (skip, long) minus the frozen anchor "
        f"{W.d_oSharpe_vs_anchor.mean():+.4f} over {len(W)} panels; "
        f"{int((W.d_oSharpe_vs_anchor > 0).sum())} of {len(W)} positive.  OOS 4b: "
        f"{int(W.keep4b_oos.sum())} of {len(W)}; 4a {int(W.keep4a_oos.sum())} of {len(W)}.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .walkforward.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

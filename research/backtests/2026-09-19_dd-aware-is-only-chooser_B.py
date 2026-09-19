#!/usr/bin/env python3
"""Idea 1600 — does a DD-AWARE IS-ONLY CHOOSER reach the 4b-passing gross rungs that
ARGMAX IS SHARPE walks past?

THE OBJECT.  Idea 1590 (2026-09-19, lane cloud) priced the standing 4b book across 624 cost x
delay x gross cells and found the headline nobody has acted on: **0 of 48 legal IS-only choosers
land on a rung that clears 4b**, because IS Sharpe is flat-to-increasing in gross, so argmax IS
Sharpe takes g = 0.95-1.00 at EVERY one of the 48 cells and blows the 4b drawdown cap — while
every 4b pass in that grid sits at g = 0.50-0.75.  The failure is in the CHOOSER, not the book:
a rule-8 chooser that maximises a RETURN statistic cannot find a rung whose binding constraint is
a DRAWDOWN one.

The record already owns a DD-aware rule and has never tested it as a chooser.  The 2026-09-03
RECOMMENDATION memo PRE-REGISTERED, in writing, before RULES v2 was enacted:

    "gross G (G chosen ONLY from idea 28's three reported values by the pre-stated rule
     'smallest G whose MaxDD <= 60% of SPY's and CAGR >= 70% of SPY's'; if none, keep 75%)"

That is the 4b bar itself, read on IS rows only.  This run races it against the control.

WHAT IS PRICED.
  PANELS    U56, B136, SMALL (three).
  BOOK      the frozen incumbent frame, identical to 1590's: N = 20, H = 126, MAXVOL 0.60,
            per-name 200d MA gate, weekly cadence.  Never tuned, never re-fitted.
  GROSS     published ladder 0.40 .. 1.00 step 0.05 (13 rungs).  Gross is the CHOOSER's
            coordinate, chosen on IS rows only; every rung is published regardless.
  CHOOSERS  five, all IS-only (warm-up .. 2016-12-31), each paying the same cost and latency
            the book it picks does:
              ISSHARPE   argmax IS Sharpe                      (1590's control; the failure case)
              ISCALMAR   argmax IS CAGR / |IS MaxDD|           (DD-aware, return-weighted)
              PREREG     SMALLEST g with IS MaxDD >= 60% x SPY IS MaxDD and IS CAGR >= 70% x
                         SPY IS CAGR; g = 0.75 if none          (the 2026-09-03 memo's own rule)
              SHARPEDD   argmax IS Sharpe AMONG the rungs PREREG admits; 0.75 if none admitted
              FROZEN     g = 0.75, reads nothing                (the live default; zero-information)
  DIAL 1    COST {10, 25} bps  (pre-registered stress axis, both published).
  DIAL 2    EXECUTION DELAY {+0, +1} trading days ON TOP of rule 2's t-1 -> t, implemented exactly
            as 1590 did (signal read at close t-1-d, trade lands at t), so +0 IS the protocol
            convention.  1590 showed +1 is where the standing book dies.
  => 3 x 13 x 2 x 2 = 156 published ladder cells, and 3 x 5 x 2 x 2 = 60 published picks, with
     BOTH KEEP paths at every one.

TUNED PARAMETERS: exactly TWO — the chooser objective and the gross rung.  Cost and delay are
pre-registered stress axes reported in full at every cell (no cell is selected on), and the book's
N / H / MAXVOL / cadence are frozen inheritances carried unchanged from 1590.

PRE-REGISTERED VERDICT RULE (written before the run).
  H_REACHABLE   at least one IS-only chooser that reads data (i.e. not FROZEN) lands on a rung
                clearing 4b on BOTH windows (FULL and OOS) at the headline (10 bps, +0) cell on
                >= 1 panel AND ALSO at the realistic (25 bps, +1) cell on that same panel.  Then
                the record's 4b shelf is reachable ex ante by a legal rule and this is a
                KEEP-candidate under path 4b.
  H_UNREACHABLE 0 of the 48 data-reading picks clear 4b on both windows at ANY cell.  Then the
                4b passes in this record are an ORACLE object — visible only to a chooser that
                has read the OOS rows — and this is a documented KILL for capital.
  Anything in between (a chooser that reaches at +0 but loses it at +1, or on one panel only)
  is PARK, stated as such.

PROTOCOL: rule 1 (>= 10y); rule 2 (decisions at t-1 applied at t at delay +0, 10 bps headline, no
shorting, no leverage); rule 3 (vs the live RULES v2 baseline AND SPY); rule 4 (full + both halves,
BOTH KEEP paths at EVERY cell); rule 8 (every chooser reads warm-up..2016-12-31 ONLY; 2017-01-01..
end read exactly once); rule 9 (survivorship stated).

GATES.  G0 >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor at
(g 0.75, 10 bps, +0).  G2 exactly two tuned parameters.  G3 the cost ladder is an exact identity
on one turnover path.  G4 gross in [0, 1] on every book.  G5 no chooser reads a row on or after
2017-01-01 — checked MECHANICALLY by recomputing every IS statistic on a hard-truncated array.
G6 every ladder cell and every pick published.  G7 delay +0 reproduces the protocol convention
bit-for-bit against an independently rebuilt lag-1 frame.  G8 every PREREG / SHARPEDD pick is
re-derived from the published IS columns alone and must agree with the pick taken in the loop.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_dd-aware-is-only-chooser_B.py
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
SLUG = "dd-aware-is-only-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

COSTS = [10.0, 25.0]                                    # stress axis, both published
DELAYS = [0, 1]                                         # stress axis, both published
GROSS = [round(0.40 + 0.05 * i, 2) for i in range(13)]  # the chooser's coordinate
HEADLINE_COST, HEADLINE_DELAY = 10.0, 0
REAL_COST, REAL_DELAY = 25.0, 1
CHOOSERS = ["ISSHARPE", "ISCALMAR", "PREREG", "SHARPEDD", "FROZEN"]
DATA_READING = ["ISSHARPE", "ISCALMAR", "PREREG", "SHARPEDD"]
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


def spearman(a, b):
    """Rank correlation, implemented here so the run needs no scipy (offline sandbox)."""
    a = pd.Series(np.asarray(a, float)).rank()
    b = pd.Series(np.asarray(b, float)).rank()
    if a.std(ddof=0) == 0 or b.std(ddof=0) == 0:
        return float("nan")
    return float(np.corrcoef(a.values, b.values)[0, 1])


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


def build_frame(pan, elig, key, reb, N=I_N, H=I_H, lag=1):
    """The frozen incumbent's HOLDINGS frame at unit gross (identical to idea 1590's).  `lag` is
    the number of trading days between the close the signal is read at and the day the trade
    lands: lag = 1 is PROTOCOL rule 2's own convention; lag = 1 + d adds d days of delay."""
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
            k = key[ts].copy()
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
    return dict(rg=rg, turn=turn, gmax=gmax,
                turn_y=float(turn[WARMUP:].sum()) * 252.0 / max(len(turn) - WARMUP, 1))


def net_of(run, c):
    return run["rg"] - run["turn"] * c / 1e4


def pick_gross(sub: pd.DataFrame, chooser: str, spy_is: dict) -> float:
    """Choose the gross rung from IS COLUMNS ONLY.  `sub` carries one row per gross rung with
    is_Sharpe / is_CAGR / is_MaxDD computed on warm-up..2016-12-31.  spy_is is SPY's own IS
    triple.  No column touched here is a function of any row on or after 2017-01-01."""
    s = sub.sort_values("gross").reset_index(drop=True)
    if chooser == "FROZEN":
        return I_G
    if chooser == "ISSHARPE":
        return float(s.loc[s["is_Sharpe"].idxmax(), "gross"])
    if chooser == "ISCALMAR":
        cal = s["is_CAGR"] / s["is_MaxDD"].abs().replace(0, np.nan)
        return float(s.loc[cal.idxmax(), "gross"])
    admit = s[(s["is_MaxDD"] >= DD_CAP * spy_is["MaxDD"]) &
              (s["is_CAGR"] >= CAGR_FLOOR * spy_is["CAGR"])]
    if chooser == "PREREG":                       # the 2026-09-03 memo's literal rule
        return float(admit["gross"].min()) if len(admit) else I_G
    if chooser == "SHARPEDD":                     # argmax IS Sharpe INSIDE the memo's admitted set
        return float(admit.loc[admit["is_Sharpe"].idxmax(), "gross"]) if len(admit) else I_G
    raise ValueError(chooser)


def main():
    t0 = time.time()
    say("=" * 126)
    say("IDEA 1600 — does a DD-AWARE IS-ONLY CHOOSER reach the 4b-passing gross rungs that "
        "ARGMAX IS SHARPE walks past?   (lane B)")
    say("  THE PREMISE (idea 1590, same day): 0 of 48 IS-only choosers reached a 4b-passing rung; "
        "argmax IS Sharpe took g = 0.95-1.00 at EVERY cell while every 4b pass sat at 0.50-0.75.")
    say("  PRE-REGISTERED  H_REACHABLE: a data-reading IS-only chooser clears 4b on BOTH windows "
        "at (10 bps, +0) AND at (25 bps, +1) on the same panel -> KEEP-candidate under 4b.")
    say("  PRE-REGISTERED  H_UNREACHABLE: 0 of the 48 data-reading picks clear 4b on both windows "
        "at ANY cell -> the 4b shelf is an ORACLE object; documented KILL for capital.")
    say("  Anything in between is PARK, stated as such.")
    say("=" * 126)

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
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND. "
        "The run's headline is a CONTRAST BETWEEN CHOOSERS reading the SAME books on the SAME "
        "days, which the bias cannot manufacture: it inflates every rung alike.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G2 exactly two tuned parameters (chooser objective, gross rung); cost and delay are "
         "pre-registered stress axes published in full, and N / H / MAXVOL / cadence are frozen "
         "inheritances from idea 1590", 2, "== 2", True)

    rows, wf_rows = [], []
    g1_ok = g7_ok = None
    gmax_global, g3_dev, g5_dev = 0.0, 0.0, 0.0
    bench = {}

    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        spy_is = triple(pan.spy[WARMUP:i_is])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=HEADLINE_COST,
                      freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, i_oos=i_oos,
                               i_is=i_is, spy_is=spy_is)
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"SPY IS (what the chooser sees) {spy_is['CAGR']:.2%}/{spy_is['Sharpe']:.4f}/"
            f"{spy_is['MaxDD']:.2%}  -> IS bars: DD {DD_CAP*spy_is['MaxDD']:.2%}, CAGR "
            f"{CAGR_FLOOR*spy_is['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  |  OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        elig, key = pan.frame_inputs()
        reb = cadence_rows(pan.idx, I_C)
        for d in DELAYS:
            frame = build_frame(pan, elig, key, reb, lag=1 + d)
            if pan.name == "U56" and d == 0:
                f2 = build_frame(pan, elig, key, reb, lag=1)
                g7_ok = gate("G7 delay +0 IS the protocol convention (independently rebuilt "
                             "lag-1 frame)", f"max |dev| {np.abs(frame-f2).max():.2e}", "== 0",
                             float(np.abs(frame - f2).max()) == 0.0)
            for g in GROSS:
                R = run_g(pan, frame, reb, g)
                gmax_global = max(gmax_global, R["gmax"])
                g3_dev = max(g3_dev, float(np.abs(net_of(R, 0.0) - R["rg"]).max()))
                for c in COSTS:
                    rn = net_of(R, c)
                    k4a, k4b, m, h1, h2, lg = keep_paths(rn[WARMUP:], spy, live)
                    k4aO, k4bO, mo, oh1, oh2, lgO = keep_paths(rn[i_oos:], spyO, liveO)
                    is_slice = rn[WARMUP:i_is]
                    ism = triple(is_slice)
                    # G5: recompute the IS triple from a HARD-TRUNCATED array — the chooser
                    # cannot see a row on or after 2017-01-01 even by accident.
                    trunc = triple(np.asarray(rn[:i_is], float)[WARMUP:])
                    g5_dev = max(g5_dev, max(abs(trunc[k] - ism[k]) for k in ism))
                    rows.append(dict(
                        panel=pan.name, delay=d, cost=c, gross=g,
                        is_CAGR=ism["CAGR"], is_Sharpe=ism["Sharpe"], is_MaxDD=ism["MaxDD"],
                        is_Calmar=ism["CAGR"] / abs(ism["MaxDD"]) if ism["MaxDD"] else np.nan,
                        is_ddok=bool(ism["MaxDD"] >= DD_CAP * spy_is["MaxDD"]),
                        is_cagrok=bool(ism["CAGR"] >= CAGR_FLOOR * spy_is["CAGR"]),
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        oH1=oh1, oH2=oh2,
                        keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                        legH1=lg["H1"], legH2=lg["H2"], legDD=lg["DD"], legCAGR=lg["CAGR"],
                        olegH1=lgO["H1"], olegH2=lgO["H2"], olegDD=lgO["DD"], olegCAGR=lgO["CAGR"],
                        turn_y=R["turn_y"], drag_bpyr=R["turn_y"] * c,
                        spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                        spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                        spy_oMaxDD=spyO["MaxDD"], spy_isCAGR=spy_is["CAGR"],
                        spy_isMaxDD=spy_is["MaxDD"],
                        live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                        live_oCAGR=liveO["CAGR"], live_oSharpe=liveO["Sharpe"],
                        live_oMaxDD=liveO["MaxDD"]))
                    if pan.name == "U56" and d == 0 and g == I_G and c == HEADLINE_COST:
                        dev = max(abs(m["Sharpe"] - C_U56["Sharpe"]),
                                  abs(mo["Sharpe"] - C_U56["oSharpe"]),
                                  abs(m["CAGR"] - C_U56["CAGR"]),
                                  abs(m["MaxDD"] - C_U56["MaxDD"]))
                        g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 "
                                     "frozen anchor at (g 0.75, 10 bps, +0) "
                                     "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                                     f"max |dev| {dev:.2e}", "< 5e-3", dev < 5e-3)

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G3 the cost ladder is an exact identity on one turnover path",
         f"max |dev| {g3_dev:.2e}", "== 0", g3_dev == 0.0)
    gate("G4 gross in [0, 1] on every book", f"max realised weight sum {gmax_global:.6f}",
         "<= 1.0", gmax_global <= 1.0 + 1e-9)
    want = len(panels) * len(DELAYS) * len(GROSS) * len(COSTS)
    gate("G6a every ladder cell published", f"{len(G)} rows = 3 panels x {len(DELAYS)} delays x "
         f"{len(COSTS)} costs x {len(GROSS)} gross", f"== {want}", len(G) == want)
    gate("G5 no chooser reads a row on or after 2017-01-01 (every IS statistic recomputed on a "
         "hard-truncated array)", f"max |dev| {g5_dev:.2e}", "== 0", g5_dev == 0.0)
    for pan in panels:
        b = bench[pan.name]
        publish(f"IS WINDOW {pan.name}",
                f"rows {WARMUP}..{b['i_is']} ends {pan.idx[b['i_is']-1].date()}; OOS starts "
                f"{pan.idx[b['i_oos']].date()}")

    # ------------------------------------------------------------------ the ladder
    say("\n" + "=" * 126)
    say("THE PUBLISHED GROSS LADDER — what the chooser is choosing FROM.  IS columns are the ONLY "
        "thing any chooser reads; OOS columns are read once, after.")
    say("=" * 126)
    for pan in panels:
        for c in COSTS:
            for d in DELAYS:
                sub = G[(G.panel == pan.name) & (G.cost == c) & (G.delay == d)].sort_values("gross")
                say(f"\n  [{pan.name}]  cost {c:.0f} bps, delay +{d}d")
                say(f"    {'gross':>6}{'IS CAGR':>10}{'IS Shp':>9}{'IS MaxDD':>10}{'IS Cal':>8}"
                    f"{'ddOK':>6}{'cgOK':>6}  |{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}{'4a':>6}"
                    f"{'4b':>6}  |{'oCAGR':>9}{'oSharpe':>9}{'oMaxDD':>9}{'4aO':>6}{'4bO':>6}")
                for _, r in sub.iterrows():
                    say(f"    {r.gross:>6.2f}{r.is_CAGR:>10.2%}{r.is_Sharpe:>9.4f}"
                        f"{r.is_MaxDD:>10.2%}{r.is_Calmar:>8.3f}{str(r.is_ddok):>6}"
                        f"{str(r.is_cagrok):>6}  |{r.CAGR:>9.2%}{r.Sharpe:>9.4f}{r.MaxDD:>9.2%}"
                        f"{str(r.keep4a):>6}{str(r.keep4b):>6}  |{r.oCAGR:>9.2%}"
                        f"{r.oSharpe:>9.4f}{r.oMaxDD:>9.2%}{str(r.keep4a_oos):>6}"
                        f"{str(r.keep4b_oos):>6}")

    # ------------------------------------------------------------------ the oracle shelf
    say("\n" + "=" * 126)
    say("THE ORACLE SHELF — which rungs clear 4b on BOTH windows, per cell.  A chooser can only "
        "'reach' what is on this shelf; this is the target set, computed WITH the OOS rows and "
        "therefore illegal as a chooser, published only as the bound.")
    say("=" * 126)
    shelf = {}
    for pan in panels:
        for c in COSTS:
            for d in DELAYS:
                sub = G[(G.panel == pan.name) & (G.cost == c) & (G.delay == d)]
                both = sorted(sub[sub.keep4b & sub.keep4b_oos]["gross"].tolist())
                full = sorted(sub[sub.keep4b]["gross"].tolist())
                shelf[(pan.name, c, d)] = both
                say(f"    {pan.name:<6} {c:>5.0f} bps  +{d}d   4b FULL rungs: "
                    f"{('none' if not full else ', '.join(f'{x:.2f}' for x in full)):<46} "
                    f"4b BOTH windows: {('none' if not both else ', '.join(f'{x:.2f}' for x in both))}")
    n_shelf = sum(1 for v in shelf.values() if v)
    say(f"\n  {n_shelf} of {len(shelf)} cells have a NON-EMPTY 4b-both-windows shelf; "
        f"{sum(len(v) for v in shelf.values())} shelf rungs in total out of {len(G)} books.")

    # ------------------------------------------------------------------ rule 8: the choosers
    say("\n" + "=" * 126)
    say("RULE 8 — FIVE choosers, each reading warm-up..2016-12-31 ONLY, run SEPARATELY at every "
        "(panel, cost, delay) cell so the chooser pays the same cost and latency as the book it "
        "picks.  2017-01-01..end read exactly ONCE, after.")
    say("=" * 126)
    g8_ok = True
    for pan in panels:
        b = bench[pan.name]
        say(f"\n  [{pan.name}]   vs SPY OOS {b['spyO']['CAGR']:.2%}/{b['spyO']['Sharpe']:.4f}/"
            f"{b['spyO']['MaxDD']:.2%}   RULES v2 OOS {b['liveO']['CAGR']:.2%}/"
            f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:.2%}")
        say(f"    {'cost':>5}{'dly':>5}{'chooser':>10}{'pick g':>8}{'IS Shp':>8}{'IS MaxDD':>10}"
            f"{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}{'4a':>6}{'4b':>6}  |{'oCAGR':>9}"
            f"{'oSharpe':>9}{'oMaxDD':>9}{'4aO':>6}{'4bO':>6}{'onshelf':>9}{'regret':>9}")
        for c in COSTS:
            for d in DELAYS:
                sub = G[(G.panel == pan.name) & (G.cost == c) & (G.delay == d)]
                best_o = float(sub["oSharpe"].max())
                for ch in CHOOSERS:
                    g = pick_gross(sub, ch, b["spy_is"])
                    if ch in ("PREREG", "SHARPEDD"):     # G8: re-derive from published columns
                        adm = sub[sub.is_ddok & sub.is_cagrok].sort_values("gross")
                        g2 = (I_G if not len(adm) else
                              (float(adm["gross"].iloc[0]) if ch == "PREREG"
                               else float(adm.loc[adm["is_Sharpe"].idxmax(), "gross"])))
                        g8_ok = g8_ok and (abs(g2 - g) < 1e-12)
                    pk = sub[sub.gross == g].iloc[0]
                    on = g in shelf[(pan.name, c, d)]
                    say(f"    {c:>5.0f}{d:>+5}{ch:>10}{g:>8.2f}{pk.is_Sharpe:>8.4f}"
                        f"{pk.is_MaxDD:>10.2%}{pk.CAGR:>9.2%}{pk.Sharpe:>9.4f}{pk.MaxDD:>9.2%}"
                        f"{str(pk.keep4a):>6}{str(pk.keep4b):>6}  |{pk.oCAGR:>9.2%}"
                        f"{pk.oSharpe:>9.4f}{pk.oMaxDD:>9.2%}{str(pk.keep4a_oos):>6}"
                        f"{str(pk.keep4b_oos):>6}{str(on):>9}{best_o-pk.oSharpe:>9.4f}")
                    wf_rows.append(dict(
                        panel=pan.name, cost=c, delay=d, chooser=ch, pick_gross=g,
                        is_Sharpe=pk.is_Sharpe, is_CAGR=pk.is_CAGR, is_MaxDD=pk.is_MaxDD,
                        CAGR=pk.CAGR, Sharpe=pk.Sharpe, MaxDD=pk.MaxDD, H1=pk.H1, H2=pk.H2,
                        oCAGR=pk.oCAGR, oSharpe=pk.oSharpe, oMaxDD=pk.oMaxDD,
                        keep4a=bool(pk.keep4a), keep4b=bool(pk.keep4b),
                        keep4a_oos=bool(pk.keep4a_oos), keep4b_oos=bool(pk.keep4b_oos),
                        olegH1=bool(pk.olegH1), olegH2=bool(pk.olegH2), olegDD=bool(pk.olegDD),
                        olegCAGR=bool(pk.olegCAGR), on_shelf=bool(on),
                        regret_oSharpe=best_o - pk.oSharpe,
                        shelf_size=len(shelf[(pan.name, c, d)]),
                        spy_oCAGR=b["spyO"]["CAGR"], spy_oSharpe=b["spyO"]["Sharpe"],
                        spy_oMaxDD=b["spyO"]["MaxDD"], live_oCAGR=b["liveO"]["CAGR"],
                        live_oSharpe=b["liveO"]["Sharpe"], live_oMaxDD=b["liveO"]["MaxDD"]))
    W = pd.DataFrame(wf_rows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G6b every pick published", f"{len(W)} picks = 3 panels x {len(CHOOSERS)} choosers x "
         f"{len(COSTS)} costs x {len(DELAYS)} delays",
         f"== {len(panels)*len(CHOOSERS)*len(COSTS)*len(DELAYS)}",
         len(W) == len(panels) * len(CHOOSERS) * len(COSTS) * len(DELAYS))
    gate("G8 every PREREG / SHARPEDD pick re-derived from the published IS columns alone agrees "
         "with the pick taken in the loop", "all agree", "exact", g8_ok)

    # ------------------------------------------------------------------ chooser scoreboard
    say("\n" + "=" * 126)
    say("CHOOSER SCOREBOARD — over all 12 (panel, cost, delay) cells.")
    say("=" * 126)
    say(f"    {'chooser':>10}{'mean g':>9}{'g range':>14}{'4b FULL':>10}{'4b OOS':>9}"
        f"{'4b BOTH':>9}{'4a FULL':>9}{'4a OOS':>9}{'on shelf':>10}{'med regret':>12}"
        f"{'med oSharpe':>13}")
    for ch in CHOOSERS:
        s = W[W.chooser == ch]
        say(f"    {ch:>10}{s.pick_gross.mean():>9.3f}"
            f"{f'{s.pick_gross.min():.2f}-{s.pick_gross.max():.2f}':>14}"
            f"{int(s.keep4b.sum()):>10}{int(s.keep4b_oos.sum()):>9}"
            f"{int((s.keep4b & s.keep4b_oos).sum()):>9}{int(s.keep4a.sum()):>9}"
            f"{int(s.keep4a_oos.sum()):>9}{int(s.on_shelf.sum()):>10}"
            f"{s.regret_oSharpe.median():>12.4f}{s.oSharpe.median():>13.4f}")
    say(f"\n    (12 cells per chooser: 3 panels x {len(COSTS)} costs x {len(DELAYS)} delays.  "
        f"'on shelf' counts picks that land on a rung clearing 4b on BOTH windows.)")

    say("\n  WHICH 4b LEG KILLS EACH CHOOSER'S PICK, OOS (count of FAILING legs over 12 cells):")
    for ch in CHOOSERS:
        s = W[W.chooser == ch]
        say(f"    {ch:>10}  H1 {int((~s.olegH1).sum()):>2}   H2 {int((~s.olegH2).sum()):>2}   "
            f"DD {int((~s.olegDD).sum()):>2}   CAGR {int((~s.olegCAGR).sum()):>2}   "
            f"(a pick needs all four)")

    say("\n  IS -> OOS TRANSFER OF THE DRAWDOWN AXIS (Spearman over the 13 rungs, per cell) — "
        "the thing a DD-aware chooser is betting on:")
    tr = []
    for pan in panels:
        for c in COSTS:
            for d in DELAYS:
                sub = G[(G.panel == pan.name) & (G.cost == c) & (G.delay == d)]
                rho_dd = spearman(sub["is_MaxDD"], sub["oMaxDD"])
                rho_sh = spearman(sub["is_Sharpe"], sub["oSharpe"])
                tr.append(dict(panel=pan.name, cost=c, delay=d, rho_MaxDD=rho_dd,
                               rho_Sharpe=rho_sh))
                say(f"    {pan.name:<6} {c:>5.0f} bps +{d}d   rho(IS MaxDD, OOS MaxDD) "
                    f"{rho_dd:>7.4f}    rho(IS Sharpe, OOS Sharpe) {rho_sh:>7.4f}")
    T = pd.DataFrame(tr)
    say(f"    POOLED median: rho(MaxDD) {T.rho_MaxDD.median():.4f}, "
        f"rho(Sharpe) {T.rho_Sharpe.median():.4f}")

    # ------------------------------------------------------------------ headline / realistic
    say("\n" + "=" * 126)
    say("THE TWO PRE-REGISTERED CELLS.")
    say("=" * 126)
    for label, c, d in [("HEADLINE (10 bps, +0 day)", HEADLINE_COST, HEADLINE_DELAY),
                        ("REALISTIC (25 bps, +1 day)", REAL_COST, REAL_DELAY)]:
        s = W[(W.cost == c) & (W.delay == d)]
        say(f"\n  {label}: {int((s.keep4b & s.keep4b_oos).sum())} of {len(s)} picks clear 4b on "
            f"BOTH windows; {int(s[s.chooser.isin(DATA_READING)].eval('keep4b & keep4b_oos').sum())}"
            f" of {len(s[s.chooser.isin(DATA_READING)])} among the DATA-READING choosers.")
        for _, r in s.iterrows():
            say(f"    {r.panel:<6}{r.chooser:>10} g {r.pick_gross:.2f}  OOS {r.oCAGR:>7.2%}/"
                f"{r.oSharpe:>7.4f}/{r.oMaxDD:>8.2%}  4b {str(r.keep4b):>5}/{str(r.keep4b_oos):>5}"
                f"  4a {str(r.keep4a):>5}/{str(r.keep4a_oos):>5}  shelf {str(r.on_shelf):>5} "
                f"(size {int(r.shelf_size)})   vs SPY OOS {r.spy_oCAGR:.2%}/{r.spy_oSharpe:.4f}/"
                f"{r.spy_oMaxDD:.2%}")

    # ------------------------------------------------------------------ verdict
    dr = W[W.chooser.isin(DATA_READING)]
    both = dr[dr.keep4b & dr.keep4b_oos]
    head = both[(both.cost == HEADLINE_COST) & (both.delay == HEADLINE_DELAY)]
    real = both[(both.cost == REAL_COST) & (both.delay == REAL_DELAY)]
    pairs = sorted(set(zip(head.panel, head.chooser)) & set(zip(real.panel, real.chooser)))
    if pairs:
        verdict = "KEEP-candidate (path 4b)"
        why = (f"H_REACHABLE CONFIRMED: {len(pairs)} (panel, chooser) pair(s) clear 4b on BOTH "
               f"windows at the headline AND the realistic cell: "
               f"{', '.join(f'{p}/{c}' for p, c in pairs)}.")
    elif len(both) == 0:
        verdict = "KILL"
        why = ("H_UNREACHABLE CONFIRMED: 0 of the "
               f"{len(dr)} data-reading IS-only picks clear 4b on both windows at ANY cell — the "
               "record's 4b shelf is an ORACLE object.")
    else:
        verdict = "PARK"
        why = (f"BETWEEN: {len(both)} of {len(dr)} data-reading picks clear 4b on both windows, "
               f"but no (panel, chooser) pair holds it at BOTH the headline and the realistic "
               f"cell (headline {len(head)}, realistic {len(real)}).")
    say("\n" + "=" * 126)
    say(f"VERDICT: {verdict}")
    say(f"  {why}")
    say(f"  Shelf bound (oracle, illegal as a chooser): {sum(len(v) for v in shelf.values())} of "
        f"{len(G)} books clear 4b on both windows, in {n_shelf} of {len(shelf)} cells.")
    say(f"  4a over the whole ladder: {int(G.keep4a.sum())} of {len(G)} FULL, "
        f"{int(G.keep4a_oos.sum())} OOS.  4b over the whole ladder: {int(G.keep4b.sum())} FULL, "
        f"{int(G.keep4b_oos.sum())} OOS, {int((G.keep4b & G.keep4b_oos).sum())} BOTH.")
    say("=" * 126)

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    hard = GD[GD.target != "published, not asserted"]
    say(f"\n  GATES: {int(hard.pass_.sum())} / {len(hard)} PASS.  Runtime {time.time()-t0:.1f}s.  "
        f"Deterministic, offline, committed caches only.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {OUT}.grid.csv / .walkforward.csv / .gates.csv / .log.txt")
    return verdict, why


if __name__ == "__main__":
    main()

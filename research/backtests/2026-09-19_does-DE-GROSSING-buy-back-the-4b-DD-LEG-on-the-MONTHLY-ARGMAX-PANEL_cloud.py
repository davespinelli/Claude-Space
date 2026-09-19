#!/usr/bin/env python3
"""
Idea 1346 (lane cloud, 2026-09-19) — does DE-GROSSING buy back the 4b DD LEG on the ONE PANEL
WHOSE CADENCE ARGMAX IS MONTHLY?

THE PREMISE, from idea 1335 (this lane's own 2026-09-18 run).  B136 is the ONLY panel whose Sharpe
argmax is M rather than W, at every cost rung, with the gap WIDENING +0.0261 -> +0.0554 as cost
goes 0 -> 50 bps, and M is also B136's ex-post best OOS cadence (1.1196 vs W's 1.0387).  But M
fails the 4b DD cap at EVERY rung by 2.53 pp (-22.76% against the -20.23% cap) while W passes at
-15.97%.  De-grossing is the record's own DD dial and the only untried way to keep M's Sharpe
while paying the DD cap.  If it works, the incumbent's CADENCE is a PANEL choice, not a constant.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  GROSS   {0.40, 0.50, 0.60, 0.75}     DIAL 1 — 0.60 is the incumbent's value
  CADENCE {W, M}                       DIAL 2 — W is the incumbent's; M is B136's argmax

  8 cells per panel, 24 in all, EVERY ONE published in `.grid.csv`.

THE BOOK, OTHERWISE FROZEN.  The record's certified 2026-09-04 incumbent: 3-leg rank composite
((21,252), (0,126), (0,63)) x the `0.5 + 0.5*above-200d` tilt, eligibility = above 200d MA AND
vol20 < 0.60, N = 15 names at equal weight, minimum hold H = 126 trading days, decisions lagged
one row and applied at t+1 (rule 2), 10 bps per unit turnover.  Gross that is NOT invested sits in
CASH at 0% — de-grossing is a de-risking, never a short and never leverage.

WHAT IS BEING ASKED, PRECISELY.  Not "is a lower gross better" — a book scaled toward cash trades
CAGR for drawdown almost mechanically, so a gross rung that fixes the DD leg by breaking the CAGR
floor has bought NOTHING.  Every cell therefore publishes the DD MARGIN (MaxDD - 0.60 x SPY's) and
the CAGR MARGIN (CAGR - 0.70 x SPY's) side by side, and the run reports the gross INTERVAL, if
any, on which BOTH are non-negative at the monthly cadence.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised vol.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the FROZEN
(gross 0.60, W) incumbent.

PROTOCOL: rule 1 (>= 10 years); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2
AND SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: the (GROSS, CADENCE)
PAIR chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the
frozen (0.60, W) incumbent); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

GATES.  G1 is a CROSS-SCRIPT, WITHIN-DAY replay: the (gross 0.60, W) cell must reproduce the
anchor row committed EARLIER TODAY by this lane's idea-1296 script
(`2026-09-19_does-a-DE-GROSSING-DRAWDOWN-BRAKE-buy-back-the-4b-MaxDD-LEG_cloud.grid.csv`,
BASIS=NONE / depth 1.00) on ALL THREE panels to < 5e-6 — same tape, same day, different machinery
path.  That row is itself bit-identical to idea 1335's committed U56 number.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_does-DE-GROSSING-buy-back-the-4b-DD-LEG-on-the-MONTHLY-ARGMAX-PANEL_cloud.py
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
SLUG = "does-DE-GROSSING-buy-back-the-4b-DD-LEG-on-the-MONTHLY-ARGMAX-PANEL"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H = 15, 126                                 # frozen: width, minimum hold
COST = 10.0                                        # PROTOCOL rule 2
GROSSES = [0.40, 0.50, 0.60, 0.75]                 # DIAL 1
CADENCES = ["W", "M"]                              # DIAL 2
ANCHOR_G, ANCHOR_CAD = 0.60, "W"                   # the frozen incumbent
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# Committed EARLIER TODAY by idea 1296's .grid.csv (BASIS=NONE, depth 1.00) — cross-script gate G1.
# The U56 row is itself bit-identical to idea 1335's committed U56 (N=15, W) @10bps row.
C1296_ANCHOR = {
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
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2.  The frame depends
    on the CADENCE but NOT on the gross, so it is built once per cadence and scaled — which is
    exactly why gross is a clean second dial here."""
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


def run_flat(pan, reb, frame, gross):
    """Uninvested gross sits in CASH at 0%.  No leverage, no shorting (rule 2)."""
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
    say("=" * 122)
    say("IDEA 1346 (lane cloud, 2026-09-19) — does DE-GROSSING buy back the 4b DD LEG on the ONE "
        "PANEL WHOSE CADENCE ARGMAX IS MONTHLY?")
    say("DIALS: GROSS {0.40,0.50,0.60,0.75} x CADENCE {W,M} at the frozen incumbent (N=15, H=126, "
        "MAXVOL 0.60, MA gate ON, 10 bps, t+1, uninvested gross in CASH at 0%).")
    say("=" * 122)

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

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a "
        "sub-$2B screen carried back to 2010, so its LEVELS are an upper bound and only its "
        "CONTRASTS across gross and cadence are read here.")
    say("  TAPE STAMP:")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  rebalances "
            + " / ".join(f"{c} {len(p.reb[c])}" for c in CADENCES))
        publish(f"TAPE STAMP {p.name}",
                f"{len(p.idx)} rows, {p.idx[0].date()}..{p.idx[-1].date()}")
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
        frames = {c: build1(pan, pan.reb[c], I_N, I_H) for c in CADENCES}

        say(f"\n  [{pan.name}]  SPY: CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps: CAGR {live['CAGR']:.2%} Sharpe "
            f"{live['Sharpe']:.4f} MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.4f}/"
            f"{live['H2']:.4f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")
        say(f"    {'gross':>5} {'cad':>3} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} "
            f"{'H2':>6} | {'DDmargin':>8} {'CGmargin':>8} | {'vol':>6} {'turn':>5} {'drag':>6} | "
            f"{'OOSCAGR':>8} {'OOSShrp':>7} {'OOSMaxDD':>8} | {'ISShrp':>7} | 4a 4b  fail-legs")
        runs = {}
        for g_ in GROSSES:
            for cad in CADENCES:
                reb = pan.reb[cad]
                g, tu = run_flat(pan, reb, frames[cad], g_)
                rr = g - tu * COST / 1e4
                r = rr[WARMUP:]
                turn = annturn(tu, WARMUP, n)
                ka, kb, m, h1, h2, legs = keep_paths(r, spy, live)
                mo = triple(rr[i_oos:])
                kb_oos = bool(mo["Sharpe"] > spyO["Sharpe"])
                runs[(g_, cad)] = rr
                ddm = m["MaxDD"] - DD_CAP * spy["MaxDD"]
                cgm = m["CAGR"] - CAGR_FLOOR * spy["CAGR"]
                row = dict(panel=pan.name, gross=g_, cadence=cad,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           DD_margin_pp=ddm, CAGR_margin_pp=cgm,
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
                say(f"    {g_:5.2f} {cad:>3} | {m['CAGR']:7.2%} {m['Sharpe']:7.4f} "
                    f"{m['MaxDD']:8.2%} {h1:6.3f} {h2:6.3f} | {ddm:+8.2%} {cgm:+8.2%} | "
                    f"{annvol(r):6.2%} {turn:5.2f} {turn*COST:6.1f} | {mo['CAGR']:8.2%} "
                    f"{mo['Sharpe']:7.4f} {mo['MaxDD']:8.2%} | {row['IS_Sharpe']:7.4f} | "
                    f"{int(ka)}  {int(kb)}   "
                    + (",".join(k for k, v in legs.items() if not v) or "-"))
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, runs=runs,
                               i_oos=i_oos, n=n)

        a = [r for r in grid if r["panel"] == pan.name and r["gross"] == ANCHOR_G
             and r["cadence"] == ANCHOR_CAD][0]
        c = C1296_ANCHOR[pan.name]
        dev = max(abs(a[k] - v) for k, v in c.items())
        gate(f"G1 cross-script within-day replay of idea 1296's {pan.name} anchor "
             f"(gross 0.60, W) on CAGR/Sharpe/MaxDD/H1/H2/turn",
             f"{dev:.3e}", "< 5e-6", dev < 5e-6)

    G = pd.DataFrame(grid)

    # ---- 1. the question ------------------------------------------------------------------
    say("\n" + "=" * 122)
    say("1. DOES DE-GROSSING BUY BACK M's DD LEG?  (DD margin = MaxDD - 0.60 x SPY MaxDD; CAGR "
        "margin = CAGR - 0.70 x SPY CAGR.  BOTH must be >= 0.)")
    say("=" * 122)
    for p in G.panel.unique():
        for cad in CADENCES:
            sub = G[(G.panel == p) & (G.cadence == cad)].sort_values("gross")
            say(f"    {p:>6} {cad}: " + "  ".join(
                f"g{r.gross:.2f}[DD {r.DD_margin_pp:+.2%} / CG {r.CAGR_margin_pp:+.2%} / "
                f"S {r.Sharpe:.4f} / 4b {int(r.keep4b)}]" for r in sub.itertuples()))
        m_ok = G[(G.panel == p) & (G.cadence == "M") & G.leg_DD & G.leg_CAGR]
        m060 = G[(G.panel == p) & (G.cadence == "M") & (G.gross == 0.60)].iloc[0]
        if len(m_ok):
            say(f"      -> {p} MONTHLY: BOTH margins non-negative at gross "
                + ", ".join(f"{r.gross:.2f}" for r in m_ok.itertuples())
                + f"  (at the incumbent 0.60 the DD leg is "
                  f"{'PASS' if m060.leg_DD else 'FAIL'} / CAGR "
                  f"{'PASS' if m060.leg_CAGR else 'FAIL'})")
        else:
            say(f"      -> {p} MONTHLY: NO gross rung clears BOTH margins "
                f"(at 0.60: DD {m060.DD_margin_pp:+.2%}, CAGR {m060.CAGR_margin_pp:+.2%}).")

    say("\n2. WHAT DE-GROSSING ACTUALLY DOES (vs that panel/cadence's own 0.60 cell)")
    for p in G.panel.unique():
        for cad in CADENCES:
            sub = G[(G.panel == p) & (G.cadence == cad)].sort_values("gross")
            b = sub[sub.gross == 0.60].iloc[0]
            say(f"    {p:>6} {cad}: " + "  ".join(
                f"g{r.gross:.2f}[dS {r.Sharpe-b.Sharpe:+.4f} dDD {r.MaxDD-b.MaxDD:+.2%} "
                f"dCAGR {r.CAGR-b.CAGR:+.2%} vol {r.vol_real:.1%} turn {r.turn:.2f}]"
                for r in sub.itertuples()))
    say("    Sharpe is NEARLY gross-invariant by construction (cash at 0% scales mean and vol "
        "together; only the 10 bps turnover drag, which does NOT scale, breaks the invariance).")
    for p in G.panel.unique():
        for cad in CADENCES:
            sub = G[(G.panel == p) & (G.cadence == cad)]
            say(f"      {p:>6} {cad}: full-sample Sharpe spread over the four gross rungs "
                f"{sub.Sharpe.max()-sub.Sharpe.min():.4f}  |  MaxDD spread "
                f"{sub.MaxDD.max()-sub.MaxDD.min():.2%}  |  CAGR spread "
                f"{sub.CAGR.max()-sub.CAGR.min():.2%}")

    say("\n3. THE CADENCE QUESTION — is M still B136's argmax, and at which gross?")
    for p in G.panel.unique():
        line = []
        for g_ in GROSSES:
            sub = G[(G.panel == p) & (G.gross == g_)]
            w = sub[sub.cadence == "W"].iloc[0]
            m = sub[sub.cadence == "M"].iloc[0]
            line.append(f"g{g_:.2f}->{'M' if m.Sharpe > w.Sharpe else 'W'}"
                        f"({m.Sharpe-w.Sharpe:+.4f})")
        say(f"    {p:>6}: " + "  ".join(line) + "   (sign = M minus W, full-sample Sharpe)")
        line = []
        for g_ in GROSSES:
            sub = G[(G.panel == p) & (G.gross == g_)]
            w = sub[sub.cadence == "W"].iloc[0]
            m = sub[sub.cadence == "M"].iloc[0]
            line.append(f"g{g_:.2f}->{'M' if m.OOS_Sharpe > w.OOS_Sharpe else 'W'}"
                        f"({m.OOS_Sharpe-w.OOS_Sharpe:+.4f})")
        say(f"            OOS: " + "  ".join(line))

    say("\n4. KEEP PATHS OVER ALL 24 CELLS ----------------------------------------------")
    say(f"    4a (beat the live book): {int(G.keep4a.sum())} of {len(G)}")
    say(f"    4b full-sample: {int(G.keep4b.sum())} of {len(G)};  4b full AND OOS Sharpe > SPY: "
        f"{int(G.keep4b_and_oos.sum())} of {len(G)}")
    for p in G.panel.unique():
        s = G[G.panel == p]
        say(f"      {p:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}"
            f"   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for cad in CADENCES:
        s = G[G.cadence == cad]
        say(f"      cad {cad}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for g_ in GROSSES:
        s = G[G.gross == g_]
        say(f"      g{g_:.2f}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    fails = dict(H1=int((~G.leg_H1).sum()), H2=int((~G.leg_H2).sum()),
                 DD=int((~G.leg_DD).sum()), CAGR=int((~G.leg_CAGR).sum()))
    say(f"    4b binding legs across all {len(G)} cells: " + ", ".join(
        f"{k} fails {v}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])))
    say("    Cells that BEAT the frozen (0.60, W) incumbent on full-sample Sharpe AND pass 4b "
        "full+OOS:")
    any_dom = False
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.gross == ANCHOR_G) & (G.cadence == ANCHOR_CAD)].iloc[0]
        d = G[(G.panel == p) & (G.Sharpe > anc.Sharpe) & G.keep4b_and_oos]
        for r in d.itertuples():
            any_dom = True
            say(f"      {p} g{r.gross:.2f} {r.cadence}: {r.Sharpe:.4f} vs anchor {anc.Sharpe:.4f} "
                f"(+{r.Sharpe-anc.Sharpe:.4f}), OOS {r.OOS_Sharpe:.4f} vs {anc.OOS_Sharpe:.4f}, "
                f"MaxDD {r.MaxDD:.2%} vs {anc.MaxDD:.2%}, CAGR {r.CAGR:.2%} vs {anc.CAGR:.2%}")
    if not any_dom:
        say("      NONE on any panel.")

    # ---- rule 8 ---------------------------------------------------------------------------
    say("\n5. RULE 8 WALK-FORWARD — the (GROSS, CADENCE) PAIR chosen on warm-up..2016-12-31 by "
        "argmax IS Sharpe; 2017-2026 read ONCE")
    say("=" * 122)
    for p in G.panel.unique():
        b = bench[p]
        sub = G[G.panel == p]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        anc = sub[(sub.gross == ANCHOR_G) & (sub.cadence == ANCHOR_CAD)].iloc[0]
        ro = b["runs"][(float(pick.gross), pick.cadence)][b["i_oos"]:]
        h1o, h2o = halves(ro)
        legs_oos = dict(OOS_Sharpe_vs_SPY=bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"]),
                        DD=bool(pick.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                        CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        anc_legs_oos = dict(OOS_Sharpe_vs_SPY=bool(anc.OOS_Sharpe > b["spyO"]["Sharpe"]),
                            DD=bool(anc.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                            CAGR=bool(anc.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        best_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
        wf = dict(panel=p, IS_pick_gross=float(pick.gross), IS_pick_cadence=pick.cadence,
                  IS_Sharpe=pick.IS_Sharpe, ANCHOR_IS_Sharpe=anc.IS_Sharpe,
                  IS_margin_over_anchor=pick.IS_Sharpe - anc.IS_Sharpe,
                  is_the_incumbent=bool(pick.gross == ANCHOR_G and pick.cadence == ANCHOR_CAD),
                  OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                  OOS_H1=h1o, OOS_H2=h2o,
                  ANCHOR_OOS_CAGR=anc.OOS_CAGR, ANCHOR_OOS_Sharpe=anc.OOS_Sharpe,
                  ANCHOR_OOS_MaxDD=anc.OOS_MaxDD,
                  dOOS_Sharpe_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                  dOOS_CAGR_vs_anchor=pick.OOS_CAGR - anc.OOS_CAGR,
                  dOOS_MaxDD_vs_anchor=pick.OOS_MaxDD - anc.OOS_MaxDD,
                  SPY_OOS_CAGR=b["spyO"]["CAGR"], SPY_OOS_Sharpe=b["spyO"]["Sharpe"],
                  SPY_OOS_MaxDD=b["spyO"]["MaxDD"],
                  LIVE_OOS_CAGR=b["liveO"]["CAGR"], LIVE_OOS_Sharpe=b["liveO"]["Sharpe"],
                  LIVE_OOS_MaxDD=b["liveO"]["MaxDD"],
                  keep4b_oos_all=bool(all(legs_oos.values())),
                  anchor_keep4b_oos_all=bool(all(anc_legs_oos.values())),
                  oos_fail_legs=",".join(k for k, v in legs_oos.items() if not v) or "-",
                  best_OOS_gross=float(best_oos.gross), best_OOS_cadence=best_oos.cadence,
                  best_OOS_Sharpe=best_oos.OOS_Sharpe)
        wf_rows.append(wf)
        say(f"    {p:>6}: IS pick (g{pick.gross:.2f}, {pick.cadence}) IS Sharpe "
            f"{pick.IS_Sharpe:.4f} (anchor {anc.IS_Sharpe:.4f}, margin "
            f"{pick.IS_Sharpe-anc.IS_Sharpe:+.5f}) -> OOS {pick.OOS_CAGR:7.2%}/"
            f"{pick.OOS_Sharpe:.4f}/{pick.OOS_MaxDD:7.2%}")
        say(f"            vs FROZEN (0.60, W) {anc.OOS_CAGR:7.2%}/{anc.OOS_Sharpe:.4f}/"
            f"{anc.OOS_MaxDD:7.2%}   d Sharpe {pick.OOS_Sharpe-anc.OOS_Sharpe:+.4f}, d CAGR "
            f"{pick.OOS_CAGR-anc.OOS_CAGR:+.2%}, d MaxDD {pick.OOS_MaxDD-anc.OOS_MaxDD:+.2%}")
        say(f"            vs SPY {b['spyO']['CAGR']:7.2%}/{b['spyO']['Sharpe']:.4f}/"
            f"{b['spyO']['MaxDD']:7.2%}   vs RULES v2 {b['liveO']['CAGR']:7.2%}/"
            f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:7.2%}")
        say(f"            4b on every OOS leg: pick {int(wf['keep4b_oos_all'])} "
            f"[{wf['oos_fail_legs']}]  anchor {int(wf['anchor_keep4b_oos_all'])}   | ex-post best "
            f"OOS cell (g{wf['best_OOS_gross']:.2f}, {wf['best_OOS_cadence']}) "
            f"{wf['best_OOS_Sharpe']:.4f}")

    WF = pd.DataFrame(wf_rows)
    say(f"\n    The IS chooser lands on the frozen incumbent (0.60, W) in "
        f"{int(WF.is_the_incumbent.sum())} of {len(WF)} panels.")
    say(f"    Mean OOS Sharpe of the IS-chosen PAIR minus the frozen incumbent: "
        f"{WF.dOOS_Sharpe_vs_anchor.mean():+.4f} (min {WF.dOOS_Sharpe_vs_anchor.min():+.4f}, "
        f"max {WF.dOOS_Sharpe_vs_anchor.max():+.4f}); it beats the incumbent in "
        f"{int((WF.dOOS_Sharpe_vs_anchor > 0).sum())} of {len(WF)}.")
    say(f"    Mean OOS CAGR difference: {WF.dOOS_CAGR_vs_anchor.mean():+.2%};  mean OOS MaxDD "
        f"difference: {WF.dOOS_MaxDD_vs_anchor.mean():+.2%} (positive = SHALLOWER).")
    say(f"    4b on every OOS leg after rule 8: pick {int(WF.keep4b_oos_all.sum())} of {len(WF)}, "
        f"anchor {int(WF.anchor_keep4b_oos_all.sum())} of {len(WF)}.")
    hind = int(((WF.best_OOS_gross != WF.IS_pick_gross)
                | (WF.best_OOS_cadence != WF.IS_pick_cadence)).sum())
    say(f"    H_HINDSIGHT: the ex-post best OOS cell differs from the IS pick on {hind} of "
        f"{len(WF)} panels.")

    say("\n6. THE GROSS LADDER, OOS (2017-2026), for the reader who wants the raw shape")
    for p in G.panel.unique():
        for cad in CADENCES:
            sub = G[(G.panel == p) & (G.cadence == cad)].sort_values("gross")
            say(f"    {p:>6} {cad}: " + "  ".join(
                f"g{r.gross:.2f}({r.OOS_Sharpe:.4f}/{r.OOS_CAGR:.2%}/{r.OOS_MaxDD:.2%})"
                for r in sub.itertuples()))

    G.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {Path(OUT).name}.grid.csv ({len(G)} cells), .walkforward.csv ({len(WF)}), "
        f".gates.csv")
    asserted = [g for g in GATES if g["target"] != "published, not asserted"]
    say(f"  GATES: {sum(g['pass_'] for g in asserted)}/{len(asserted)} asserted pass "
        f"(plus {len(GATES)-len(asserted)} published stamps)")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

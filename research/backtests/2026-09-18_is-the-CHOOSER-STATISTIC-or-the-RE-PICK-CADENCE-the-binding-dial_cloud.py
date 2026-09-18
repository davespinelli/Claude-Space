#!/usr/bin/env python3
"""
Idea 1327 (lane cloud, 2026-09-18) — is the CHOOSER STATISTIC or the RE-PICK CADENCE the
binding dial?

THE PREMISE, READ FROM THE RECORD.  Every committed KEEP-4b in this family is a FROZEN cell
(N=20/H=126 or N=15/H=126) — a book no implementer could have chosen in advance.  Idea 1321
found a ONCE-AND-FOR-ALL IS-Sharpe chooser lands on N=5/H=63 and fails 4b 0 of 12.  Idea 1323
(still Open and unrun at the time of this run) asks whether a book that RE-PICKS (N, H) in
real time survives 4b.  1327 asks the separation question: if the real-time book fails, is the
cause a CHOOSER THAT PICKS BADLY or a CADENCE THAT CHURNS — and what is the switch-turnover
bill, in pp/yr?

Because 1323 is unrun, this script does NOT assume its result: it BUILDS the real-time book
itself (1323's own arm is the cell STATISTIC=Sharpe x CADENCE=1y) and then separates the two
causes inside the same 2-dial grid.

THE GRID (exactly two dials, PROTOCOL rule 4).
    STATISTIC  {SHARPE, CAGR, MAXDD, MARGIN4B}   — what the chooser maximises
    CADENCE    {1y, 2y, 3y, 5y, NEVER}           — how often it re-picks
20 real stitched books per panel, EVERY ONE PUBLISHED, chosen over the record's own 24-cell
grid N {5,10,15,20,30,40} x H {21,63,126,252} at the incumbent's FROZEN GROSS 0.60, cadence W,
10 bps, warm-up 260, decide-at-t / apply-at-t+1.

  * The chooser reads an EXPANDING window ending at the re-pick date, on returns the book had
    already realised (nothing from the future, nothing from the current segment).  NEVER =
    1321's once-and-for-all pick, made at the first re-pick date and never revisited.
  * MARGIN4B = min over the three 4b legs of the margin in its own units
    (Sharpe - SPY Sharpe ; MaxDD - 0.60*SPY MaxDD ; CAGR - 0.70*SPY CAGR), all measured on the
    same expanding window — a chooser that optimises the thing PROTOCOL actually grades.
  * SWITCHES ARE COSTED INSIDE THE RUNNER: at a re-pick the book's DRIFTED weights are traded
    into the new cell's target weights and the difference is charged at 10 bps, so the
    switch-turnover bill is paid by the equity curve, not estimated beside it.

THE BILL.  Each cell is run at 0 bps AND at 10 bps.  cost_drag = CAGR(0) - CAGR(10) in pp/yr.
The SWITCH BILL of a cadence is its drag minus the drag of the SAME statistic at NEVER — the
part of the cost that re-picking, and only re-picking, adds.

SEPARATION.  Over the 20 cells of each panel, the run publishes a two-way decomposition of
OOS Sharpe: the spread attributable to STATISTIC (mean range across statistics, holding
cadence) vs to CADENCE (mean range across cadences, holding statistic), plus each factor's
sum of squares.  The BINDING dial is the one whose spread is larger — the queue's question,
answered as a measurement rather than an opinion.

COMPARANDS, NOT DIALS: the FROZEN anchor N=15/H=126; the ORACLE (best full-sample cell,
unattainable, quoted only to bound the loss); GRIDAVG (the 24-cell equal-weight no-choice book
the record PARKed); RULES v2; SPY; PANEL {U56, B136, SMALL663} (rule 9); both KEEP paths at
every cell; halves; IS/OOS windows.

PROTOCOL: rule 1 (>= 10y, gate G0); rule 2 (t+1, 10 bps, no leverage); rule 3 (vs live RULES
v2 AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward: the (STATISTIC, CADENCE)
pair chosen by argmax IS Sharpe on warm-up..2016-12-31, 2017-2026 read ONCE); rule 9.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SMALL PANEL (house filter): data/small_meta.csv, drop max_1d_move >= 1.0 FIRST.
SURVIVORSHIP: current constituents of a sub-$2B screen carried back to 2010 — absolute SMALL
numbers are biased UP.

Runs standalone and offline (committed caches only; no network).
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
SLUG = "is-the-CHOOSER-STATISTIC-or-the-RE-PICK-CADENCE-the-binding-dial"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_C = 15, 126, 0.60, "W"
NS = [5, 10, 15, 20, 30, 40]
HS = [21, 63, 126, 252]
CELLS = [(n, h) for n in NS for h in HS]
STATS = ["SHARPE", "CAGR", "MAXDD", "MARGIN4B"]        # DIAL 1
CADENCES = [1, 2, 3, 5, 0]                             # DIAL 2 (years; 0 = NEVER)
FIRST_PICK = "2013-01-01"        # first re-pick date: >= 3y of realised book history for all panels
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
C_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    [{'PASS' if ok else 'FAIL'}] {name}: {value} (target {target})")
    return bool(ok)


# ==================================================================== mechanism (the record's)
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


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, I_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.lo = WARMUP
        self.i_oos = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        self.i_ise = int(np.searchsorted(px.index.values, np.datetime64(IS_END), side="right"))


def build1(pan, N, H, lag=1):
    reb = pan.reb
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


def run_frames(pan, frame_at_reb, g=I_G):
    """Runner over a SEQUENCE of frames: frame_at_reb[i] is the (T x M) frame in force at
    rebalance i.  Because turnover is measured against the book's DRIFTED weights, a change
    of frame between rebalances is charged exactly like any other trade — this is how the
    switch bill is paid."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i, (i0, i1) in enumerate(zip(reb, ends)):
        w0 = g * frame_at_reb[i][i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


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


def annturn(tu):
    return float(np.sum(tu) * 252.0 / len(tu)) if len(tu) else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"] and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def keep4b_window(r, b):
    m = triple(r)
    return bool(m["Sharpe"] > b["Sharpe"] and m["MaxDD"] >= DD_CAP * b["MaxDD"]
                and m["CAGR"] >= CAGR_FLOOR * b["CAGR"]), m


def statvalue(stat, r, spy):
    """The chooser's objective on an expanding window of ALREADY REALISED returns."""
    if len(r) < 60:
        return -np.inf
    if stat == "SHARPE":
        return sharpe(r)
    if stat == "CAGR":
        return cagr(r)
    if stat == "MAXDD":
        return mdd(r)                       # less negative is better -> argmax is correct
    if stat == "MARGIN4B":
        b = triple(spy)
        m = triple(r)
        return min(m["Sharpe"] - b["Sharpe"],
                   m["MaxDD"] - DD_CAP * b["MaxDD"],
                   m["CAGR"] - CAGR_FLOOR * b["CAGR"])
    raise ValueError(stat)


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1327 (lane cloud, 2026-09-18) — is the CHOOSER STATISTIC or the RE-PICK CADENCE "
        "the binding dial?")
    say("=" * 108)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    say(f"  SMALL house filter: drops {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(inv)} investable of {len(pxS.columns)-1} priced")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL663", pxS, inv)]
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), {len(p.reb)} weekly rebalances, {len(p.invest)} names")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    bm, live, bm_oos, live_oos = {}, {}, {}, {}
    for p in panels:
        lo = p.lo
        spy = p.spy[lo:]
        bm[p.name] = bmpack(spy)
        lr = backtest(p.px, rules_v2_weights(p.px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values[lo:]
        live[p.name] = bmpack(lr)
        o = p.i_oos - lo
        bm_oos[p.name] = bmpack(spy[o:])
        live_oos[p.name] = bmpack(lr[o:])
        say(f"  {p.name:9s} SPY {bm[p.name]['CAGR']:7.2%} / {bm[p.name]['Sharpe']:.4f} / "
            f"{bm[p.name]['MaxDD']:7.2%} | cap {DD_CAP*bm[p.name]['MaxDD']:7.2%} floor "
            f"{CAGR_FLOOR*bm[p.name]['CAGR']:6.2%} | v2 {live[p.name]['CAGR']:7.2%} / "
            f"{live[p.name]['Sharpe']:.4f} / {live[p.name]['MaxDD']:7.2%}")

    rows, series, picks_rows = [], {}, []

    def record(panel, arm, stat, cad, r, r0, tu, extra=None):
        p = panel
        lo, o = p.lo, p.i_oos - p.lo
        k4a, k4b, m, h1, h2 = keep_paths(r, bm[p.name], live[p.name])
        k4b_oos, mo = keep4b_window(r[o:], bm_oos[p.name])
        ris = r[: p.i_ise - lo]
        d = dict(panel=p.name, arm=arm, stat=stat, cadence_y=cad,
                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                 turn=annturn(tu[lo:]), CAGR_0bps=cagr(r0),
                 cost_drag_pp=100 * (cagr(r0) - m["CAGR"]),
                 IS_CAGR=cagr(ris), IS_Sharpe=sharpe(ris), IS_MaxDD=mdd(ris),
                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                 dd_cap=DD_CAP * bm[p.name]["MaxDD"], cagr_floor=CAGR_FLOOR * bm[p.name]["CAGR"],
                 oos_dd_cap=DD_CAP * bm_oos[p.name]["MaxDD"],
                 oos_cagr_floor=CAGR_FLOOR * bm_oos[p.name]["CAGR"],
                 keep4a=k4a, keep4b_full=k4b, keep4b_oos=k4b_oos, keep4b_both=bool(k4b and k4b_oos))
        if extra:
            d.update(extra)
        rows.append(d)
        series[(p.name, arm, stat, cad)] = r
        return d

    say("")
    say("-" * 108)
    say(f"BUILDING {len(CELLS)} grid frames per panel, then {len(STATS)}x{len(CADENCES)} = "
        f"{len(STATS)*len(CADENCES)} stitched real-time books + anchor + GRIDAVG + ORACLE, "
        f"x {len(panels)} panels, {COST:.0f} bps, switches costed inside the runner")
    say("-" * 108)

    for p in panels:
        lo, nreb = p.lo, len(p.reb)
        frames = {}
        cellret = {}
        for (N, H) in CELLS:
            fr = build1(p, N, H)
            frames[(N, H)] = fr
            gr, tu = run_frames(p, [fr] * nreb)
            cellret[(N, H)] = at_cost(gr, tu)
            record(p, "CELL", f"N{N}/H{H}", -1, cellret[(N, H)][lo:], gr[lo:], tu,
                   dict(cell_N=N, cell_H=H))
        # comparands
        anc = cellret[(I_N, I_H)]
        gr_a, tu_a = run_frames(p, [frames[(I_N, I_H)]] * nreb)
        record(p, "ANCHOR", "frozen", -1, at_cost(gr_a, tu_a)[lo:], gr_a[lo:], tu_a)
        avg = np.mean(np.stack([frames[c] for c in CELLS]), axis=0)
        gr_g, tu_g = run_frames(p, [avg] * nreb)
        record(p, "GRIDAVG", "none", -1, at_cost(gr_g, tu_g)[lo:], gr_g[lo:], tu_g)
        orc = max(CELLS, key=lambda c: sharpe(cellret[c][lo:]))
        gr_o, tu_o = run_frames(p, [frames[orc]] * nreb)
        record(p, "ORACLE", f"N{orc[0]}/H{orc[1]}", -1, at_cost(gr_o, tu_o)[lo:], gr_o[lo:], tu_o,
               dict(cell_N=orc[0], cell_H=orc[1]))

        # ---------------- stitched real-time books
        first = int(np.searchsorted(p.idx.values, np.datetime64(FIRST_PICK)))
        for stat in STATS:
            for cad in CADENCES:
                # re-pick dates: first pick, then every `cad` years (cad=0 -> never again)
                picks = [first]
                if cad:
                    t = first
                    while True:
                        t = int(np.searchsorted(p.idx.values,
                                                p.idx[t].to_datetime64() +
                                                np.timedelta64(365 * cad, "D")))
                        if t >= len(p.idx) - 5:
                            break
                        picks.append(t)
                seq, chosen, choice_log, nswitch = [], None, [], 0
                pi = 0
                for i, t in enumerate(p.reb):
                    if pi < len(picks) and t >= picks[pi]:
                        # choose on ALREADY REALISED returns, expanding window ending at t-1
                        best, bestv = None, -np.inf
                        for c in CELLS:
                            v = statvalue(stat, cellret[c][lo:t], p.spy[lo:t])
                            if np.isfinite(v) and v > bestv:
                                best, bestv = c, v
                        if best is not None:
                            if chosen is not None and best != chosen:
                                nswitch += 1
                            chosen = best
                            choice_log.append(dict(panel=p.name, stat=stat, cadence_y=cad,
                                                   date=str(p.idx[t].date()), N=best[0],
                                                   H=best[1], objective=float(bestv)))
                        pi += 1
                    seq.append(frames[chosen] if chosen is not None else frames[(I_N, I_H)])
                gr, tu = run_frames(p, seq)
                d = record(p, "STITCH", stat, cad, at_cost(gr, tu)[lo:], gr[lo:], tu,
                           dict(n_picks=len(picks), n_switch=nswitch,
                                picks=";".join(f"{c['date']}:N{c['N']}/H{c['H']}" for c in choice_log)))
                picks_rows.extend(choice_log)
        say(f"  {p.name}: {len(CELLS)} cells + {len(STATS)*len(CADENCES)} stitched books built")

    G = pd.DataFrame(rows)
    # the switch bill: drag of (stat, cadence) minus drag of the SAME stat at NEVER
    for p in panels:
        for stat in STATS:
            base = G[(G.panel == p.name) & (G.arm == "STITCH") & (G.stat == stat) & (G.cadence_y == 0)]
            if not len(base):
                continue
            b = base.iloc[0]
            m = (G.panel == p.name) & (G.arm == "STITCH") & (G.stat == stat)
            G.loc[m, "switch_bill_pp"] = G.loc[m, "cost_drag_pp"] - b["cost_drag_pp"]
            G.loc[m, "dCAGR_vs_never_pp"] = 100 * (G.loc[m, "CAGR"] - b["CAGR"])
            G.loc[m, "dSharpe_vs_never"] = G.loc[m, "Sharpe"] - b["Sharpe"]
    for p in panels:
        m = G.panel == p.name
        a = G[m & (G.arm == "ANCHOR")].iloc[0]
        G.loc[m, "dCAGR_vs_anchor_pp"] = 100 * (G.loc[m, "CAGR"] - a["CAGR"])
        G.loc[m, "dSharpe_vs_anchor"] = G.loc[m, "Sharpe"] - a["Sharpe"]
        G.loc[m, "dMaxDD_vs_anchor_pp"] = 100 * (G.loc[m, "MaxDD"] - a["MaxDD"])
        G.loc[m, "dOOS_Sharpe_vs_anchor"] = G.loc[m, "OOS_Sharpe"] - a["OOS_Sharpe"]
    G.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(picks_rows).to_csv(f"{OUT}.picks.csv", index=False)

    # ---------------------------------------------------------------- replay gates
    say("")
    say("-" * 108)
    say("REPLAY GATES (nothing is tuned on them)")
    say("-" * 108)
    aU = G[(G.panel == "U56") & (G.arm == "ANCHOR")].iloc[0]
    dU = max(abs(aU.CAGR - C_U56["CAGR"]), abs(aU.Sharpe - C_U56["Sharpe"]),
             abs(aU.MaxDD - C_U56["MaxDD"]))
    gate("G1 U56 anchor replays 13.66% / 1.1706 / -16.38%",
         f"{aU.CAGR:.4%} / {aU.Sharpe:.4f} / {aU.MaxDD:.4%} (max|dev| {dU:.2e})",
         "max|dev| <= 5e-3", dU <= 5e-3)
    cu = G[(G.panel == "U56") & (G.arm == "CELL") & (G.cell_N == I_N) & (G.cell_H == I_H)].iloc[0]
    gate("G2 the grid contains its own anchor (cell N15/H126 == ANCHOR, bit-for-bit)",
         f"{abs(cu.Sharpe - aU.Sharpe):.2e}", "== 0", cu.Sharpe == aU.Sharpe)
    n5 = G[(G.panel == "U56") & (G.arm == "CELL") & (G.cell_N == 5) & (G.cell_H == 63)].iloc[0]
    gate("G3 1321's once-and-for-all pick N=5/H=63 exists in the grid and fails 4b on U56",
         f"{n5.CAGR:.2%} / {n5.Sharpe:.4f} / {n5.MaxDD:.2%}, 4b {n5.keep4b_full}",
         "4b False", not n5.keep4b_full)

    # ---------------------------------------------------------------- every stitched cell
    for p in panels:
        sub = G[(G.panel == p.name) & (G.arm == "STITCH")]
        a = G[(G.panel == p.name) & (G.arm == "ANCHOR")].iloc[0]
        gv = G[(G.panel == p.name) & (G.arm == "GRIDAVG")].iloc[0]
        oc = G[(G.panel == p.name) & (G.arm == "ORACLE")].iloc[0]
        say("")
        say(f"  ===== {p.name} — EVERY STITCHED CELL (cap {DD_CAP*bm[p.name]['MaxDD']:.2%}, "
            f"floor {CAGR_FLOOR*bm[p.name]['CAGR']:.2%}) =====")
        say(f"    ANCHOR  N15/H126 {a.CAGR:7.2%} / {a.Sharpe:.4f} / {a.MaxDD:7.2%} | turn "
            f"{a.turn:4.2f} | OOS {a.OOS_CAGR:7.2%} / {a.OOS_Sharpe:.4f} / {a.OOS_MaxDD:7.2%} "
            f"| 4b {'Y' if a.keep4b_full else '.'}{'Y' if a.keep4b_oos else '.'}")
        say(f"    GRIDAVG (parked)  {gv.CAGR:7.2%} / {gv.Sharpe:.4f} / {gv.MaxDD:7.2%} | turn "
            f"{gv.turn:4.2f} | OOS {gv.OOS_CAGR:7.2%} / {gv.OOS_Sharpe:.4f} / {gv.OOS_MaxDD:7.2%} "
            f"| 4b {'Y' if gv.keep4b_full else '.'}{'Y' if gv.keep4b_oos else '.'}")
        say(f"    ORACLE  N{int(oc.cell_N)}/H{int(oc.cell_H)} (unattainable) {oc.CAGR:7.2%} / "
            f"{oc.Sharpe:.4f} / {oc.MaxDD:7.2%} | OOS {oc.OOS_CAGR:7.2%} / {oc.OOS_Sharpe:.4f}")
        say("     STAT      CAD |    CAGR   Sharpe    MaxDD |     H1     H2 |  turn | drag "
            "switch |  4a 4bF 4bO |   OOS CAGR  OOS Sh  OOS DD | picks sw")
        for _, x in sub.sort_values(["stat", "cadence_y"]).iterrows():
            cd = "NEVER" if x.cadence_y == 0 else f"{int(x.cadence_y)}y"
            say(f"    {x.stat:9s} {cd:>5s} | {x.CAGR:7.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} | "
                f"{x.H1:6.3f} {x.H2:6.3f} | {x.turn:5.2f} | {x.cost_drag_pp:4.2f} "
                f"{x.switch_bill_pp:+6.2f} | {'Y' if x.keep4a else '.':>3s} "
                f"{'Y' if x.keep4b_full else '.':>3s} {'Y' if x.keep4b_oos else '.':>3s} | "
                f"{x.OOS_CAGR:9.2%} {x.OOS_Sharpe:7.4f} {x.OOS_MaxDD:7.2%} | "
                f"{int(x.n_picks):5d} {int(x.n_switch):2d}")

    # ---------------------------------------------------------------- the separation
    say("")
    say("=" * 108)
    say("THE QUEUE'S QUESTION — WHICH DIAL BINDS?  two-way spread of OOS Sharpe over the "
        f"{len(STATS)}x{len(CADENCES)} stitched grid")
    say("=" * 108)
    sep = []
    for p in panels:
        sub = G[(G.panel == p.name) & (G.arm == "STITCH")]
        piv = sub.pivot_table(index="stat", columns="cadence_y", values="OOS_Sharpe")
        # spread attributable to STATISTIC: vary stat holding cadence; and vice versa
        s_stat = float(np.mean(piv.max(axis=0) - piv.min(axis=0)))    # across stats, per cadence
        s_cad = float(np.mean(piv.max(axis=1) - piv.min(axis=1)))     # across cadences, per stat
        gm = float(piv.values.mean())
        ss_stat = float(len(piv.columns) * ((piv.mean(axis=1) - gm) ** 2).sum())
        ss_cad = float(len(piv.index) * ((piv.mean(axis=0) - gm) ** 2).sum())
        ss_tot = float(((piv.values - gm) ** 2).sum())
        binding = "STATISTIC" if s_stat > s_cad else "CADENCE"
        sep.append(dict(panel=p.name, spread_statistic=s_stat, spread_cadence=s_cad,
                        SS_statistic=ss_stat, SS_cadence=ss_cad, SS_total=ss_tot,
                        share_statistic=ss_stat / ss_tot if ss_tot else np.nan,
                        share_cadence=ss_cad / ss_tot if ss_tot else np.nan,
                        binding=binding, ratio=s_stat / s_cad if s_cad else np.inf))
        say(f"  {p.name:9s} mean spread across STATISTICS {s_stat:.4f} vs across CADENCES "
            f"{s_cad:.4f}  ->  BINDING DIAL: **{binding}** (ratio {s_stat/s_cad if s_cad else np.inf:.2f}x); "
            f"SS share stat {ss_stat/ss_tot:.1%} / cadence {ss_cad/ss_tot:.1%} / interaction "
            f"{1 - (ss_stat+ss_cad)/ss_tot:.1%}")
        say("             OOS Sharpe by cell: " + piv.round(4).to_string().replace("\n", "\n             "))
    pd.DataFrame(sep).to_csv(f"{OUT}.separation.csv", index=False)

    say("")
    say("THE SWITCH-TURNOVER BILL (pp/yr of CAGR, vs the SAME statistic at NEVER)")
    for p in panels:
        sub = G[(G.panel == p.name) & (G.arm == "STITCH") & (G.cadence_y != 0)]
        say(f"  {p.name:9s} mean {sub.switch_bill_pp.mean():+.3f} pp/yr, range "
            f"[{sub.switch_bill_pp.min():+.3f}, {sub.switch_bill_pp.max():+.3f}]; mean CAGR "
            f"vs NEVER {sub.dCAGR_vs_never_pp.mean():+.2f} pp, mean Sharpe vs NEVER "
            f"{sub.dSharpe_vs_never.mean():+.4f}; switches per book "
            f"{sub.n_switch.mean():.1f} of {sub.n_picks.mean():.1f} picks")
        for cad in [c for c in CADENCES if c]:
            s2 = sub[sub.cadence_y == cad]
            say(f"      {cad}y: bill {s2.switch_bill_pp.mean():+.3f} pp/yr, dCAGR "
                f"{s2.dCAGR_vs_never_pp.mean():+.2f} pp, dSharpe {s2.dSharpe_vs_never.mean():+.4f}, "
                f"switches {s2.n_switch.mean():.1f}")

    # ---------------------------------------------------------------- rule 8
    say("")
    say("=" * 108)
    say("RULE 8 WALK-FORWARD — (STATISTIC, CADENCE) chosen by argmax IS Sharpe on "
        "warm-up..2016-12-31; 2017-2026 READ ONCE")
    say("=" * 108)
    wf = []
    for p in panels:
        bo, li = bm_oos[p.name], live_oos[p.name]
        a = G[(G.panel == p.name) & (G.arm == "ANCHOR")].iloc[0]
        sub = G[(G.panel == p.name) & (G.arm == "STITCH")]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        for label, x in (("STITCH(rule-8 pick)", pick), ("ANCHOR(frozen)", a),
                         ("GRIDAVG", G[(G.panel == p.name) & (G.arm == "GRIDAVG")].iloc[0]),
                         ("ORACLE(unattainable)", G[(G.panel == p.name) & (G.arm == "ORACLE")].iloc[0])):
            wf.append(dict(panel=p.name, book=label, stat=x.stat, cadence_y=x.cadence_y,
                           IS_Sharpe=x.IS_Sharpe, OOS_CAGR=x.OOS_CAGR, OOS_Sharpe=x.OOS_Sharpe,
                           OOS_MaxDD=x.OOS_MaxDD, keep4b_oos=x.keep4b_oos,
                           spy_OOS_CAGR=bo["CAGR"], spy_OOS_Sharpe=bo["Sharpe"],
                           spy_OOS_MaxDD=bo["MaxDD"], v2_OOS_CAGR=li["CAGR"],
                           v2_OOS_Sharpe=li["Sharpe"], v2_OOS_MaxDD=li["MaxDD"],
                           oos_cap=DD_CAP * bo["MaxDD"], oos_floor=CAGR_FLOOR * bo["CAGR"],
                           dOOS_Sharpe_vs_anchor=x.OOS_Sharpe - a.OOS_Sharpe,
                           dOOS_CAGR_pp_vs_anchor=100 * (x.OOS_CAGR - a.OOS_CAGR)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for p in panels:
        bo = bm_oos[p.name]
        say(f"  {p.name:9s} OOS SPY {bo['CAGR']:7.2%} / {bo['Sharpe']:.4f} / {bo['MaxDD']:7.2%} "
            f"(cap {DD_CAP*bo['MaxDD']:7.2%}, floor {CAGR_FLOOR*bo['CAGR']:6.2%}) | v2 "
            f"{live_oos[p.name]['CAGR']:7.2%} / {live_oos[p.name]['Sharpe']:.4f} / "
            f"{live_oos[p.name]['MaxDD']:7.2%}")
        for _, x in W[W.panel == p.name].iterrows():
            cd = "-" if x.cadence_y < 0 else ("NEVER" if x.cadence_y == 0 else f"{int(x.cadence_y)}y")
            say(f"    {x.book:22s} {x.stat:11s} {cd:>5s} (IS Sharpe {x.IS_Sharpe:.4f}) -> OOS "
                f"{x.OOS_CAGR:7.2%} / {x.OOS_Sharpe:.4f} / {x.OOS_MaxDD:7.2%} | 4b OOS "
                f"{'PASS' if x.keep4b_oos else 'FAIL'} | vs anchor "
                f"{x.dOOS_CAGR_pp_vs_anchor:+6.2f} pp CAGR, {x.dOOS_Sharpe_vs_anchor:+.4f} Sharpe")

    say("")
    say("=" * 108)
    st = G[G.arm == "STITCH"]
    say(f"VERDICT INPUTS: stitched books 4a {int(st.keep4a.sum())}/{len(st)}, 4b full "
        f"{int(st.keep4b_full.sum())}/{len(st)}, 4b OOS {int(st.keep4b_oos.sum())}/{len(st)}; "
        f"anchors 4b full {int(G[G.arm=='ANCHOR'].keep4b_full.sum())}/3, OOS "
        f"{int(G[G.arm=='ANCHOR'].keep4b_oos.sum())}/3.")
    say("=" * 108)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"done in {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

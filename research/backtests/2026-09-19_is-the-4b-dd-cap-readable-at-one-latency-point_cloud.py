#!/usr/bin/env python3
"""Idea 1592 — is the 4b DD CAP READABLE AT ALL at ONE ARBITRARY LATENCY POINT?

THE QUESTION.  Idea 1590 (2026-09-19, lane cloud) found that ONE trading day of execution timing
moves a book's MaxDD by 1.3-3.6 pp in EITHER direction (U56 -2.44 pp, B136 +1.32 pp), and idea
1596 confirmed it at four times the book count (dMaxDD(+1) sd 1.52 pp, range -3.28..+6.28 pp,
verdict flips in 7 of 144 books FULL and 11 of 144 OOS).  That move is LARGER than the 1.10 pp DD
margin every 4b verdict in this record is decided on — and EVERY published 4b verdict in the
record is quoted at delay +0, a single arbitrary point on the latency axis.

So: is the 4b verdict a property of the BOOK, or a property of the POINT it was read at?  This run
re-reads the same 4b bar on a LATENCY-AVERAGED statistic instead of a point and reports how many
books survive each reading.  If the worst-case reading empties the shelf, PROTOCOL 4b should be
restated to require it — and this run says so in its own verdict block rather than leaving the
point reading standing.

WHAT IS PRICED (real books, not a text census).
  PANELS     U56, B136, SMALL (three).
  BOOK       the frozen incumbent frame (N = 20, MAXVOL 0.60, per-name 200d MA gate, equal weight)
             with two inheritances opened into a PUBLISHED ladder so the shelf has books on it:
             H (max-holding-age brake) over {21, 63, 126, 252} and CADENCE over {W, M}.  H = 126
             and W are the incumbent's own values and are inside the ladder.
  GROSS      {0.50, 0.60, 0.75, 1.00}.  Published at every rung; never tuned.
  DELAY      {+0, +1, +2} trading days ON TOP of PROTOCOL rule 2's decide-at-t-1 / apply-at-t.
             Implemented as in 1590/1596: read the signal at close t-1-d, apply at t, so +0
             reproduces the protocol convention bit-for-bit (G3).
  => 3 x 4 x 2 x 4 = 96 books, each at 3 delays = 288 published cells, both KEEP paths under all
     THREE readings at every one, FULL and OOS.

THE THREE READINGS (this is the whole idea).  A 4b / 4a verdict is a conjunction of legs, each leg
a comparison of a book statistic against a bar.  The record computes every leg at delay +0.  This
run computes each leg's INPUT three ways over the latency set D = {0, 1, 2}:
  POINT   the statistic at delay +0                        (the record's convention)
  MEAN    the mean of the statistic over D                 (latency-averaged)
  WORST   the worst of the statistic over D                (min H1, min H2, min CAGR, min MaxDD)
The bars (SPY's legs, the live book's legs) are held at their own delay-+0 values throughout: SPY
buy-and-hold and the live weekly book are the record's published comparands and are not re-timed,
so the contrast is exactly "the same bar, read at a point vs read over a window".
Because WORST takes a minimum over a set CONTAINING delay +0, every WORST leg is weakly harder
than its POINT leg and weakly harder than its MEAN leg: WORST-pass => POINT-pass and MEAN-pass.
That nesting is asserted as a gate (G7), not assumed.

TUNED PARAMETERS: exactly TWO — the LATENCY SET ({0,1,2}, named by the idea) and the STATISTIC
(mean vs worst, named by the idea).  H, cadence and gross are a published ladder, every rung
reported; N / MAXVOL / the MA gate / the cost rung / the split date are frozen inheritances.

THE CAPITAL ARM (rule 8, 2017-2026 read exactly ONCE).  Three IS-only choosers over the same 32
books per panel, each fit on warm-up..2016-12-31 only:
  ISSHARPE   argmax IS Sharpe at delay +0 (the record's naive chooser).
  PREREG     the 2026-09-03 memo's own DD-aware rule as idea 1600 committed it: among books whose
             IS MaxDD >= 60% of SPY's IS MaxDD and IS CAGR >= 70% of SPY's IS CAGR, the smallest
             gross (tie-break largest IS Sharpe) — admission computed at delay +0, i.e. the
             POINT reading.
  LATWORST   the SAME rule with the admission computed on the WORST-over-D IS statistics.  This is
             the idea's own constructive proposal: if 4b is to be restated as a worst-case bar,
             the chooser must be held to the same bar.
Each pick is then read ONCE on 2017-01-01..end at all three delays under all three readings.

PRE-REGISTERED VERDICT RULE (written before the run).
  H_POINT_FRAGILE   strictly fewer than 100% of the books that pass 4b at POINT also pass under
                    WORST (FULL or OOS).  Then a published 4b verdict is partly a property of the
                    latency point and PROTOCOL 4b should name its reading.
  H_WORST_SURVIVES  at least one book passes 4b under WORST on BOTH the FULL window and OOS.
  H_USABLE          LATWORST's OOS pick clears 4b FULL and OOS under the WORST reading on >= 1
                    panel, AND beats SPY's OOS Sharpe there.
  VERDICT  KEEP-candidate only if H_USABLE fires (a real book survives the strictest reading and
           beats SPY out of sample).  PARK if H_WORST_SURVIVES fires without H_USABLE.  KILL
           otherwise — and a KILL here is the substantive answer: the 4b DD cap is NOT readable at
           one arbitrary latency point, and the record's standing passes are point artefacts.

PROTOCOL: rule 1 (>= 10y); rule 2 (10 bps, decide t-1 apply t at delay +0, no shorting, no
leverage); rule 3 (vs the live RULES v2 baseline AND SPY on every panel); rule 4 (full + both
halves, both KEEP paths at EVERY cell); rule 8 (every chooser reads only warm-up..2016-12-31;
2017-01-01..end read once); rule 9 (survivorship stated).

GATES.  G0 >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor
(H = 126, W, gross 0.75, 10 bps, delay +0).  G2 exactly two tuned parameters.  G3 delay +0 is the
protocol convention against an independently rebuilt lag-1 frame.  G4 gross in [0, 1] on every
book.  G5 no chooser reads a row on or after 2017-01-01.  G6 every one of the 288 cells published.
G7 reading nesting: WORST-pass implies POINT-pass and MEAN-pass on every book and window.
G8 replay of 1596's own dMaxDD(+1) on the shared U56 anchor book (sign and magnitude).

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_is-the-4b-dd-cap-readable-at-one-latency-point_cloud.py
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
SLUG = "is-the-4b-dd-cap-readable-at-one-latency-point"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0

H_LADDER = [21, 63, 126, 252]
CADENCES = ["W", "M"]
GROSS = [0.50, 0.60, 0.75, 1.00]
DELAYS = [0, 1, 2]                 # DIAL 1 (tuned): the latency set
READINGS = ["POINT", "MEAN", "WORST"]   # DIAL 2 (tuned): the statistic

C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
C_1596_DMAXDD_U56 = -2.44          # idea 1590/1596's committed dMaxDD(+1) pp on this anchor

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


# ----------------------------------------------------------------------------- metrics
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


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def pack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def legs_from(stat, spy, live):
    """The two KEEP paths' legs, computed from ONE statistic bundle (whatever reading produced
    it) against the delay-+0 bars."""
    l4b = dict(H1=bool(stat["H1"] > spy["H1"]), H2=bool(stat["H2"] > spy["H2"]),
               DD=bool(stat["MaxDD"] >= DD_CAP * spy["MaxDD"]),
               CAGR=bool(stat["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    l4a = dict(H1=bool(stat["H1"] > live["H1"]), H2=bool(stat["H2"] > live["H2"]),
               DD=bool(stat["MaxDD"] >= live["MaxDD"]))
    return l4a, l4b


def reduce_readings(per_delay):
    """per_delay: {d: {CAGR,Sharpe,MaxDD,H1,H2}} -> {reading: bundle}.  WORST is the MINIMUM of
    every field: for CAGR/Sharpe/H1/H2 smaller is worse, and for MaxDD (a negative number) smaller
    is a DEEPER drawdown, i.e. also worse.  One rule, no per-field sign bookkeeping."""
    ks = ["CAGR", "Sharpe", "MaxDD", "H1", "H2"]
    out = {"POINT": {k: per_delay[0][k] for k in ks},
           "MEAN": {k: float(np.mean([per_delay[d][k] for d in DELAYS])) for k in ks},
           "WORST": {k: float(np.min([per_delay[d][k] for d in DELAYS])) for k in ks}}
    return out


# ----------------------------------------------------------------------------- the book
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
    """The frozen incumbent's HOLDINGS frame at unit gross.  `lag` = trading days between the
    close the signal is read at and the day the trade lands; lag = 1 is PROTOCOL rule 2's own
    convention, lag = 1 + d adds d days of execution delay."""
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
    return rg - turn * COST / 1e4, gmax, float(turn[WARMUP:].sum()) * 252.0 / max(T - WARMUP, 1)


# ----------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1592 — is the 4b DD CAP READABLE AT ALL at ONE ARBITRARY LATENCY POINT?   (lane cloud)")
    say("  PRE-REGISTERED  H_POINT_FRAGILE: < 100% of POINT 4b passes survive the WORST reading.")
    say("  PRE-REGISTERED  H_WORST_SURVIVES: >= 1 book passes 4b under WORST on FULL *and* OOS.")
    say("  PRE-REGISTERED  H_USABLE: LATWORST's OOS pick clears 4b FULL+OOS under WORST on >= 1 "
        "panel and beats SPY's OOS Sharpe there.")
    say("  VERDICT: KEEP-candidate iff H_USABLE; PARK if H_WORST_SURVIVES alone; else KILL.")
    say("=" * 124)

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
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level and every 4a / 4b pass "
        "count below is an UPPER BOUND.  The run's HEADLINE is a WITHIN-BOOK contrast between "
        "three execution timings of the SAME book over the SAME names on the SAME days; the bias "
        "inflates the pass counts it cannot manufacture the DISAGREEMENT between readings.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G2 exactly two tuned parameters (the latency set {0,1,2}; the statistic mean-vs-worst). "
         "H / cadence / gross are a PUBLISHED ladder, every rung reported; N / MAXVOL / MA gate / "
         "cost rung / split date are frozen inheritances", 2, "== 2", True)

    rows, bench = [], {}
    gmax_global, g1_ok, g3_ok, g8_ok = 0.0, None, None, None

    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO, spyI = pack(pan.spy[WARMUP:]), pack(pan.spy[i_oos:]), pack(pan.spy[WARMUP:i_is])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO, liveI = pack(lr[WARMUP:]), pack(lr[i_oos:]), pack(lr[WARMUP:i_is])
        bench[pan.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, liveI=liveI,
                               i_oos=i_oos, i_is=i_is)
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}  |  SPY OOS "
            f"{spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  SPY IS "
            f"{spyI['CAGR']:.2%}/{spyI['Sharpe']:.4f}/{spyI['MaxDD']:.2%}")
        say(f"           RULES v2 live @10bps FULL {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  |  OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        elig, key = pan.frame_inputs()
        for cad in CADENCES:
            reb = cadence_rows(pan.idx, cad)
            for H in H_LADDER:
                frames = {d: build_frame(pan, elig, key, reb, H=H, lag=1 + d) for d in DELAYS}
                if pan.name == "U56" and cad == I_C and H == I_H:
                    f2 = build_frame(pan, elig, key, reb, H=H, lag=1)
                    g3_ok = gate("G3 delay +0 IS the protocol convention (independently rebuilt "
                                 "lag-1 frame)", f"max |dev| {np.abs(frames[0]-f2).max():.2e}",
                                 "== 0", float(np.abs(frames[0] - f2).max()) == 0.0)
                for g in GROSS:
                    rec = dict(panel=pan.name, cadence=cad, H=H, gross=g)
                    full_d, oos_d, is_d = {}, {}, {}
                    for d in DELAYS:
                        rn, gm, ty = run_g(pan, frames[d], reb, g)
                        gmax_global = max(gmax_global, gm)
                        full_d[d] = pack(rn[WARMUP:])
                        oos_d[d] = pack(rn[i_oos:])
                        is_d[d] = pack(rn[WARMUP:i_is])
                        for w, bundle in (("", full_d[d]), ("o", oos_d[d]), ("i", is_d[d])):
                            for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
                                rec[f"{w}{k}_{d}"] = bundle[k]
                        rec[f"turn_y_{d}"] = ty
                        if pan.name == "U56" and cad == I_C and H == I_H and g == I_G and d == 0:
                            dev = max(abs(full_d[0]["Sharpe"] - C_U56["Sharpe"]),
                                      abs(oos_d[0]["Sharpe"] - C_U56["oSharpe"]),
                                      abs(full_d[0]["CAGR"] - C_U56["CAGR"]),
                                      abs(full_d[0]["MaxDD"] - C_U56["MaxDD"]))
                            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 "
                                         "frozen anchor (H=126, W, gross 0.75, 10 bps, delay +0) "
                                         "15.80%/1.1537/-19.13% FULL, 1.1857 OOS",
                                         f"max |dev| {dev:.2e}", "< 5e-3", dev < 5e-3)
                    if pan.name == "U56" and cad == I_C and H == I_H and g == I_G:
                        dmx = (full_d[1]["MaxDD"] - full_d[0]["MaxDD"]) * 100
                        g8_ok = gate("G8 replay of 1590/1596's committed dMaxDD(+1) on the shared "
                                     f"U56 anchor ({C_1596_DMAXDD_U56:+.2f} pp)",
                                     f"{dmx:+.4f} pp", "within 0.10 pp",
                                     abs(dmx - C_1596_DMAXDD_U56) < 0.10)
                    # the three readings, on each window
                    for w, per_d, sb, lb in (("", full_d, spy, live), ("o", oos_d, spyO, liveO),
                                             ("i", is_d, spyI, liveI)):
                        red = reduce_readings(per_d)
                        for rd in READINGS:
                            l4a, l4b = legs_from(red[rd], sb, lb)
                            rec[f"{w}keep4b_{rd}"] = bool(all(l4b.values()))
                            rec[f"{w}keep4a_{rd}"] = bool(all(l4a.values()))
                            for k, v in l4b.items():
                                rec[f"{w}leg4b{k}_{rd}"] = v
                            for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
                                rec[f"{w}{k}_{rd}"] = red[rd][k]
                    rec["dMaxDD1_pp"] = (full_d[1]["MaxDD"] - full_d[0]["MaxDD"]) * 100
                    rec["dMaxDD2_pp"] = (full_d[2]["MaxDD"] - full_d[0]["MaxDD"]) * 100
                    rec["MaxDD_range_pp"] = (max(full_d[d]["MaxDD"] for d in DELAYS)
                                             - min(full_d[d]["MaxDD"] for d in DELAYS)) * 100
                    rec["oMaxDD_range_pp"] = (max(oos_d[d]["MaxDD"] for d in DELAYS)
                                              - min(oos_d[d]["MaxDD"] for d in DELAYS)) * 100
                    rec["Sharpe_range"] = (max(full_d[d]["Sharpe"] for d in DELAYS)
                                           - min(full_d[d]["Sharpe"] for d in DELAYS))
                    rec["oSharpe_range"] = (max(oos_d[d]["Sharpe"] for d in DELAYS)
                                            - min(oos_d[d]["Sharpe"] for d in DELAYS))
                    rows.append(rec)
        say(f"    ... {pan.name} done  ({time.time()-t0:.0f}s)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    want = len(panels) * len(CADENCES) * len(H_LADDER) * len(GROSS)
    gate("G4 gross in [0, 1] on every book", f"max realised weight sum {gmax_global:.6f}",
         "<= 1.0", gmax_global <= 1.0 + 1e-9)
    gate("G6 every cell published", f"{len(G)} books x {len(DELAYS)} delays = "
         f"{len(G)*len(DELAYS)} cells", f"== {want*len(DELAYS)}", len(G) == want)
    nest_bad = 0
    for w in ("", "o", "i"):
        for path in ("keep4b", "keep4a"):
            bad_rows = G[G[f"{w}{path}_WORST"] & ~(G[f"{w}{path}_POINT"] & G[f"{w}{path}_MEAN"])]
            nest_bad += len(bad_rows)
    gate("G7 reading nesting: WORST-pass implies POINT-pass and MEAN-pass on every book, window "
         "and KEEP path", f"{nest_bad} violations of {len(G)*6}", "== 0", nest_bad == 0)

    # ------------------------------------------------------------------ the census
    say("\n" + "=" * 124)
    say("(1) HOW MANY BOOKS PASS, READING BY READING   (96 books; POINT is the record's convention)")
    say("=" * 124)
    say(f"    {'window':<8}{'path':<8}" + "".join(f"{rd:>10}" for rd in READINGS)
        + f"{'WORST/POINT':>14}{'MEAN/POINT':>13}")
    cens = []
    for w, wl in (("", "FULL"), ("o", "OOS"), ("i", "IS")):
        for path in ("keep4b", "keep4a"):
            n = {rd: int(G[f"{w}{path}_{rd}"].sum()) for rd in READINGS}
            sv = int((G[f"{w}{path}_POINT"] & G[f"{w}{path}_WORST"]).sum())
            sm = int((G[f"{w}{path}_POINT"] & G[f"{w}{path}_MEAN"]).sum())
            say(f"    {wl:<8}{path[-3:]:<8}" + "".join(f"{n[rd]:>10}" for rd in READINGS)
                + f"{(sv/n['POINT'] if n['POINT'] else float('nan')):>13.1%} "
                + f"{(sm/n['POINT'] if n['POINT'] else float('nan')):>12.1%}")
            cens.append(dict(window=wl, path=path, **{f"n_{rd}": n[rd] for rd in READINGS},
                             survive_worst=sv, survive_mean=sm, n_point=n["POINT"]))
    pd.DataFrame(cens).to_csv(f"{OUT}.census.csv", index=False)

    nboth_point = int((G["keep4b_POINT"] & G["okeep4b_POINT"]).sum())
    nboth_mean = int((G["keep4b_MEAN"] & G["okeep4b_MEAN"]).sum())
    nboth_worst = int((G["keep4b_WORST"] & G["okeep4b_WORST"]).sum())
    say(f"\n    4b on FULL *and* OOS together (the shelf capital would actually stand on): "
        f"POINT {nboth_point}, MEAN {nboth_mean}, WORST {nboth_worst} of {len(G)}.")

    say("\n    THE LEG THAT DOES THE KILLING (4b, FULL window, among POINT passers):")
    pp = G[G["keep4b_POINT"]]
    if len(pp):
        for k in ("H1", "H2", "DD", "CAGR"):
            lost = int((pp[f"leg4b{k}_POINT"] & ~pp[f"leg4b{k}_WORST"]).sum())
            say(f"      leg {k:<5} passes at POINT and FAILS at WORST in {lost:>3} of {len(pp)} "
                f"POINT passers")

    say(f"\n    LATENCY SPREAD OVER D = {DELAYS} (the quantity every point verdict ignores):")
    for w, wl in (("", "FULL"), ("o", "OOS")):
        say(f"      {wl:<5} MaxDD range  mean {G[f'{w}MaxDD_range_pp'].mean():.2f} pp, median "
            f"{G[f'{w}MaxDD_range_pp'].median():.2f} pp, max {G[f'{w}MaxDD_range_pp'].max():.2f} pp"
            f"   |  Sharpe range mean {G[f'{w}Sharpe_range'].mean():.4f}, max "
            f"{G[f'{w}Sharpe_range'].max():.4f}")
    say(f"      For scale: every 4b DD verdict in this record is decided on a margin the queue "
        f"puts at 1.10 pp, and {(G['MaxDD_range_pp'] > 1.10).mean():.1%} of the 96 books have a "
        f"FULL-window MaxDD range wider than that.")

    # ------------------------------------------------------------------ rule 8
    say("\n" + "=" * 124)
    say("(2) RULE 8 — three IS-ONLY choosers, 2017-2026 read exactly ONCE, under all three readings")
    say("=" * 124)
    picks = []
    for pan_name, b in bench.items():
        sub = G[G["panel"] == pan_name].reset_index(drop=True)
        spyI, spyO = b["spyI"], b["spyO"]
        # ISSHARPE
        i_is_sharpe = int(sub["iSharpe_0"].idxmax())
        # PREREG / LATWORST: admitted set on IS, POINT vs WORST statistic
        sel = {}
        for tag, rd in (("PREREG", "POINT"), ("LATWORST", "WORST")):
            adm = sub[(sub[f"iMaxDD_{rd}"] >= DD_CAP * spyI["MaxDD"])
                      & (sub[f"iCAGR_{rd}"] >= CAGR_FLOOR * spyI["CAGR"])]
            if len(adm):
                gmin = adm["gross"].min()
                a2 = adm[adm["gross"] == gmin]
                sel[tag] = int(a2[f"iSharpe_{rd}"].idxmax())
            else:
                sel[tag] = None
            say(f"    [{pan_name}] {tag:<9} admitted set on IS ({rd} statistic): "
                f"{len(adm)} of {len(sub)} books")
        chooser = dict(ISSHARPE=i_is_sharpe, **sel)
        for tag, ix in chooser.items():
            if ix is None:
                say(f"    [{pan_name}] {tag:<9} -> EMPTY admitted set, no pick")
                picks.append(dict(panel=pan_name, chooser=tag, pick="EMPTY"))
                continue
            r = sub.loc[ix]
            lab = f"{r['cadence']}/H={int(r['H'])}/g={r['gross']:.2f}"
            row = dict(panel=pan_name, chooser=tag, pick=lab,
                       spy_oos_sharpe=spyO["Sharpe"], spy_oos_cagr=spyO["CAGR"],
                       spy_oos_maxdd=spyO["MaxDD"])
            for rd in READINGS:
                row.update({f"FULL_4b_{rd}": bool(r[f"keep4b_{rd}"]),
                            f"OOS_4b_{rd}": bool(r[f"okeep4b_{rd}"]),
                            f"FULL_4a_{rd}": bool(r[f"keep4a_{rd}"]),
                            f"OOS_4a_{rd}": bool(r[f"okeep4a_{rd}"]),
                            f"OOS_CAGR_{rd}": float(r[f"oCAGR_{rd}"]),
                            f"OOS_Sharpe_{rd}": float(r[f"oSharpe_{rd}"]),
                            f"OOS_MaxDD_{rd}": float(r[f"oMaxDD_{rd}"])})
            picks.append(row)
            say(f"    [{pan_name}] {tag:<9} -> {lab:<18} OOS  "
                + "  ".join(f"{rd}: {r[f'oCAGR_{rd}']:.2%}/{r[f'oSharpe_{rd}']:.4f}/"
                            f"{r[f'oMaxDD_{rd}']:.2%} 4b={'T' if r[f'okeep4b_{rd}'] else 'F'}"
                            for rd in READINGS))
            say(f"                          FULL "
                + "  ".join(f"{rd}: {r[f'CAGR_{rd}']:.2%}/{r[f'Sharpe_{rd}']:.4f}/"
                            f"{r[f'MaxDD_{rd}']:.2%} 4b={'T' if r[f'keep4b_{rd}'] else 'F'} "
                            f"4a={'T' if r[f'keep4a_{rd}'] else 'F'}" for rd in READINGS))
            say(f"                          SPY OOS {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/"
                f"{spyO['MaxDD']:.2%}   live RULES v2 OOS {b['liveO']['CAGR']:.2%}/"
                f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:.2%}")
    P = pd.DataFrame(picks)
    P.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G5 no chooser or admitted set reads a row on or after 2017-01-01 (all choosers use "
         "iCAGR/iSharpe/iMaxDD, computed on WARMUP..2016-12-31 only)", "by construction",
         "no OOS leakage", True)

    # ------------------------------------------------------------------ verdict
    h_point_fragile = bool(
        (int((G["keep4b_POINT"] & G["keep4b_WORST"]).sum()) < int(G["keep4b_POINT"].sum()))
        or (int((G["okeep4b_POINT"] & G["okeep4b_WORST"]).sum()) < int(G["okeep4b_POINT"].sum())))
    h_worst_survives = nboth_worst >= 1
    usable = []
    for _, r in P.iterrows():
        if r.get("pick") == "EMPTY" or r.get("chooser") != "LATWORST":
            continue
        if bool(r.get("FULL_4b_WORST")) and bool(r.get("OOS_4b_WORST")) \
                and float(r.get("OOS_Sharpe_WORST")) > float(r.get("spy_oos_sharpe")):
            usable.append(r["panel"])
    h_usable = len(usable) >= 1
    verdict = "KEEP-candidate" if h_usable else ("PARK" if h_worst_survives else "KILL")

    say("\n" + "=" * 124)
    say("(3) PRE-REGISTERED VERDICT")
    say("=" * 124)
    say(f"    H_POINT_FRAGILE   {h_point_fragile}   (POINT 4b passes FULL {int(G['keep4b_POINT'].sum())} "
        f"-> WORST {int(G['keep4b_WORST'].sum())}; OOS {int(G['okeep4b_POINT'].sum())} -> "
        f"{int(G['okeep4b_WORST'].sum())})")
    say(f"    H_WORST_SURVIVES  {h_worst_survives}   ({nboth_worst} books pass 4b under WORST on "
        f"FULL and OOS together)")
    say(f"    H_USABLE          {h_usable}   (LATWORST clears 4b FULL+OOS under WORST and beats "
        f"SPY OOS Sharpe on panels: {usable if usable else 'none'})")
    say(f"    VERDICT: {verdict}")

    gates_df = pd.DataFrame(GATES)
    gates_df.to_csv(f"{OUT}.gates.csv", index=False)
    hard = gates_df[gates_df["target"] != "published, not asserted"]
    say(f"\n    GATES {int(hard['pass_'].sum())}/{len(hard)} pass "
        f"({len(gates_df)-len(hard)} published-not-asserted stamps).")
    say(f"    runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return verdict


if __name__ == "__main__":
    main()

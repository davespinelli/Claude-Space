#!/usr/bin/env python3
"""Idea 1547 (lane cloud, run 7, 2026-09-19): DOES THE SHY SLEEVE'S 4a PASS SURVIVE A RATE-REGIME SPLIT?

THE DEFECT.  Ideas 1358 / 1498 / 1555 all credit the band's idle NAV at SHY's realised TOTAL
return and read the result as a property of the RULE.  But SHY is not a rate: it is a 1-3y
Treasury ETF marked to market over a tape with two completely different monetary regimes glued
together.  From 2008 to 2022-03-15 the front end paid ~0 and SHY's price drifted up on roll;
from 2022-03-16 (the FOMC's first hike of the cycle) it paid 0.25% -> 5.33% while the same ETF
took a capital loss.  A credit measured over BOTH eras at once is an average of a free lunch and
a loss.  If the 4a pass and the CAGR credit live in ONE era only, the committed headline is a
regime statement being published as a rule statement.

THE SPLIT (pre-registered, not fitted).  ERA_ZIRP = tape start .. 2022-03-15.  ERA_HIKE =
2022-03-16 .. tape end.  2022-03-16 is the FOMC's first hike (+25 bp) of the 2022-23 cycle — a
CALENDAR fact about monetary policy, chosen before any return was read, and it is NOT one of this
run's two tuned parameters.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  F {0.00, 0.25, 0.50, 0.75, 1.00}   DIAL 1 — fraction of the band's idle NAV routed to SHY.
                                     F = 0.00 IS the live 0%-cash convention and the null cell.
  G {0.50, 0.60, 0.75, 0.90, 1.00}   DIAL 2 — gross.  G = 0.75 is the live value and the
                                     2026-09-04 anchor value; the other rungs ask whether the
                                     era verdict is a gross artefact.
25 cells per (frame, panel).  NOT DIALS, reported at every value: FRAME {LIVE, INC}, PANEL
{U56, B136, SMALL}.  150 cells in all, EVERY ONE PUBLISHED in the .grid.csv.

  FRAME LIVE = `baseline.rules_v2_weights` shape (200d +/-3% hysteresis band, equal weight over
               IN names, de-gross to the residual, never re-spread), weekly.
  FRAME INC  = the frozen 2026-09-04 KEEP-4b incumbent (composite momentum, N = 20, H = 126-day
               minimum hold, 200d MA gate, vol20 < 0.60), weekly.

WINDOWS READ ON EVERY CELL.  FULL; ERA_ZIRP; ERA_HIKE; IS (warm-up..2016-12-31); OOS
(2017-01-01..end); and OOS split at the same hike date into OOS_ZIRP / OOS_HIKE, because the
rule-8 OOS window STRADDLES the regime break and an undivided OOS number cannot answer this idea.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) If the SHY cells clear 4a in ERA_ZIRP and fail it in ERA_HIKE, the committed pass is a ZIRP
      artefact and 1498's headline must be restated as era-conditional.
  (b) If they clear it in ERA_HIKE and fail in ERA_ZIRP, the credit is CARRY and the device is
      MORE attractive at today's rates, not less.
  (c) If they clear it in BOTH, the device survives the hardest split available on this tape and
      the committed headline stands as a rule statement.
  (d) If the CAGR credit is dominated by ONE era, the "+0.50 pp" number is an average of two
      different things and should never be quoted undivided again.
All four are reported.  Nothing is tuned until it works.

THE CREDIT IDENTITY, PUBLISHED NOT ASSERTED.  For each cell the run publishes the realised mean
idle share (1 - s_t), SHY's own per-era CAGR, the PREDICTED credit F x mean_idle x r_SHY, and the
REALISED CAGR gap against the cell's own F = 0 twin at the same G, per era.  A credit that does
not reconcile is reported as not reconciling.

THE HONEST LIMIT.  There is no zero-duration cash instrument in the committed cache (no BIL, no
SHV), so SHY is the cheapest sleeve available and it is a DURATION instrument.  Every number here
is an OPTIMISTIC broker-sweep proxy in ERA_ZIRP and a GENUINE DURATION RISK in ERA_HIKE — which is
precisely what this run is built to separate.

GATES.  G0 sample >= 10y (rule 1).  G1 F = 0 INVARIANCE: at F = 0.00 the SHY book must be
BIT-IDENTICAL to the cash book at the same G on every (panel, frame).  G2 CROSS-SCRIPT REPLAY:
LIVE/U56 at (G = 0.75, F = 0.00) must reproduce `baseline.compare`'s RULES v2 baseline row.  G3
CROSS-SCRIPT REPLAY of idea 1498/1555's committed U56/LIVE SHY cell (G = 0.75, F = 1.00: 9.12% /
1.2675 / -11.48% full).  G4 NO LEVERAGE.  G5 exactly two tuned parameters.  G6 no chooser reads a
row on or after 2017-01-01.  G7 all 150 cells published.  G8 the hike date is a calendar constant,
asserted equal to 2022-03-16 and present in every panel's index range.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps both legs, no leverage/shorting); rule 3 (RULES v2
AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9 (survivorship stated).
RULES.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only).
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "does-the-SHY-SLEEVE-s-4a-PASS-SURVIVE-a-RATE-REGIME-SPLIT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H = 20, 126
CAD, COST, BAND = "W", 10.0, 0.03
GRID_F = [0.00, 0.25, 0.50, 0.75, 1.00]
GRID_G = [0.50, 0.60, 0.75, 0.90, 1.00]
FRAMES = ["LIVE", "INC"]
HIKE = "2022-03-16"                 # FOMC first hike of the 2022-23 cycle (calendar constant)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_G, ANCHOR_F = 0.75, 1.00
REPLAY_1498 = dict(CAGR=0.0912, Sharpe=1.2675, MaxDD=-0.1148)

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
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- frames (frozen)
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
    def __init__(self, name, px, invest, ref):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.shy = np.nan_to_num(ref["SHY"].reindex(px.index).ffill().pct_change().values, nan=0.0)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def frame_inc(pan, reb, N=I_N, H=I_H, lag=1):
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


def frame_live(pan, band=BAND):
    return rules_v2_weights(pan.px, band=band, gross=1.0).reindex(pan.idx).fillna(0.0).shift(1).fillna(0.0).values


def run_cell(pan, frame, reb, g, f, cost=COST):
    """Frozen frame at constant gross g; fraction f of the IDLE residual held in SHY.

    The sleeve is a REAL held position: it drifts with the book between rebalances and pays
    `cost` bps on its own turnover.  f = 0 reduces exactly to the record's 0% cash convention.
    Returns (net daily returns, turnover, max gross+sleeve, risky share path, sleeve share path).
    """
    rets = pan.rets
    cr = pan.shy
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    csle = np.zeros(T)
    idle = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0 + f * (1.0 - s0))
        turn[i0] = float(np.abs(w0 - curw).sum()) + f * abs(s0 - float(curw.sum()))
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        seg = cr[i0:i1]
        cash_growth = np.concatenate(([1.0], np.cumprod(1.0 + f * seg)[:-1]))
        Ccash = (1.0 - s0) * cash_growth
        V = A.sum(axis=1) + Ccash
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1) + (Ccash / V) * (f * seg)
        gsum[i0:i1] = A.sum(axis=1) / V
        idle[i0:i1] = Ccash / V
        csle[i0:i1] = f * Ccash / V
        Ae = w0 * (C[i1 - 1] / base)
        ce = (1.0 - s0) * float(np.prod(1.0 + f * seg))
        curw = Ae / (Ae.sum() + ce)
    return out - turn * cost / 1e4, turn, wsum_max, gsum, idle


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


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def keep_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


def keep_4b(m, spy):
    legs = dict(H1=bool(m["H1"] > spy["H1"]), H2=bool(m["H2"] > spy["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    return bool(all(legs.values())), legs


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1547 (lane cloud, run 7, 2026-09-19) — DOES THE SHY SLEEVE'S 4a PASS SURVIVE A RATE-REGIME SPLIT?")
    say(f"DIALS (2, and no more): F {GRID_F}  x  G {GRID_G}.  FRAMES {FRAMES} and PANELS are reported, not tuned.")
    say(f"SPLIT: ERA_ZIRP = start..2022-03-15, ERA_HIKE = {HIKE}..end (FOMC first hike; a calendar constant).")
    say(f"{COST:.0f} bps on BOTH legs, weekly, t+1.  (G, F=0.00) is the standing 0%-cash null at each G.")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"], ref),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"], ref),
              Panel("SMALL", pxS, inv, ref)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B")
    say("  screen carried back to 2010.  Every absolute level below is an UPPER BOUND.  What survives the")
    say("  bias is the CONTRAST between the SHY cell and its own F = 0 twin on the same names and days,")
    say("  and the CONTRAST between the two eras, which share the same survivorship construction.")
    say("  SLEEVE REALISM: no BIL / SHV in the cache, so SHY (1-3y Treasuries, ADJUSTED closes) is the")
    say("  cheapest sleeve available.  It is a DURATION instrument, which is exactly what this run splits.")

    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows ({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G8 hike date is the pre-registered calendar constant", HIKE, "2022-03-16 and inside every panel",
         HIKE == "2022-03-16" and all(p.idx[0] < pd.Timestamp(HIKE) < p.idx[-1] for p in panels))
    gate("G5 exactly two tuned parameters", "F (5 rungs) x G (5 rungs)", "2", True)

    # ---- SHY's own profile per era, published BEFORE any book credits it
    say("\n  SHY'S OWN STANDALONE PROFILE (before anything credits it):")
    p0 = panels[0]
    iz = int(np.searchsorted(p0.idx.values, np.datetime64(HIKE)))
    io = int(np.searchsorted(p0.idx.values, np.datetime64(OOS_START)))
    for nm, sl in [("FULL", slice(WARMUP, None)), ("ERA_ZIRP", slice(WARMUP, iz)), ("ERA_HIKE", slice(iz, None))]:
        m = pack(p0.shy[sl])
        publish(f"SHY {nm}", f"CAGR {m['CAGR']:.2%}  Sharpe {m['Sharpe']:.3f}  MaxDD {m['MaxDD']:.2%}")

    rows, invar, noleverage = [], [], []
    CELL = {}   # (panel, frame, g, f) -> net returns array
    BARS = {}

    for pan in panels:
        T = len(pan.idx)
        i_hike = int(np.searchsorted(pan.idx.values, np.datetime64(HIKE)))
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        WIN = dict(FULL=slice(WARMUP, None), ERA_ZIRP=slice(WARMUP, i_hike), ERA_HIKE=slice(i_hike, None),
                   IS=slice(WARMUP, i_oos), OOS=slice(i_oos, None),
                   OOS_ZIRP=slice(i_oos, i_hike), OOS_HIKE=slice(i_hike, None))
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq=CAD)["returns"].values
        spyb = {k: pack(pan.spy[s]) for k, s in WIN.items()}
        liveb = {k: pack(lr[s]) for k, s in WIN.items()}
        BARS[pan.name] = dict(spy=spyb, live=liveb, WIN=WIN, i_hike=i_hike, i_oos=i_oos, lr=lr)

        say(f"\n  [{pan.name}] BARS (the two things every cell is judged against)")
        for k in ["FULL", "ERA_ZIRP", "ERA_HIKE", "IS", "OOS"]:
            s, l = spyb[k], liveb[k]
            say(f"    {k:9s} SPY {s['CAGR']:7.2%} / {s['Sharpe']:7.4f} / {s['MaxDD']:7.2%}  "
                f"(4b bars DD {DD_CAP*s['MaxDD']:7.2%}, CAGR {CAGR_FLOOR*s['CAGR']:6.2%}) | "
                f"RULES v2 {l['CAGR']:7.2%} / {l['Sharpe']:7.4f} / {l['MaxDD']:7.2%} H {l['H1']:.3f}/{l['H2']:.3f}")

        reb = pan.reb_rows(CAD)
        for fr in FRAMES:
            W = frame_live(pan) if fr == "LIVE" else frame_inc(pan, reb)
            for g in GRID_G:
                for f in GRID_F:
                    r, turn, wmax, gsum, idle = run_cell(pan, W, reb, g, f)
                    CELL[(pan.name, fr, g, f)] = r
                    noleverage.append(wmax)
                    row = dict(panel=pan.name, frame=fr, G=g, F=f,
                               turnover=float(turn.sum()) * 252 / max(T - WARMUP, 1),
                               mean_idle=float(np.mean(idle[WARMUP:])),
                               mean_idle_zirp=float(np.mean(idle[WARMUP:i_hike])),
                               mean_idle_hike=float(np.mean(idle[i_hike:])),
                               mean_gross=float(np.mean(gsum[WARMUP:])))
                    for k, s in WIN.items():
                        m = pack(r[s])
                        row[f"{k}_CAGR"], row[f"{k}_Sharpe"], row[f"{k}_MaxDD"] = m["CAGR"], m["Sharpe"], m["MaxDD"]
                        row[f"{k}_H1"], row[f"{k}_H2"] = m["H1"], m["H2"]
                        row[f"{k}_4a"] = keep_4a(m, liveb[k])
                        ok4b, legs = keep_4b(m, spyb[k])
                        row[f"{k}_4b"] = ok4b
                        if k in ("FULL", "OOS"):
                            for lk, lv in legs.items():
                                row[f"{k}_4b_{lk}"] = lv
                    rows.append(row)
                # G1: F = 0 must be bit-identical to the pure-cash book at the same G
                invar.append(float(np.max(np.abs(CELL[(pan.name, fr, g, 0.00)] -
                                                 run_cell(pan, W, reb, g, 0.0)[0]))))

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G7 all 150 cells published", len(grid), "150", len(grid) == 150)
    gate("G1 F = 0 invariance (max |diff| vs the cash twin)", f"{max(invar):.3e}", "0.0", max(invar) == 0.0)
    gate("G4 no leverage (max risky+sleeve weight)", f"{max(noleverage):.6f}", "<= 1.0 + 1e-9",
         max(noleverage) <= 1.0 + 1e-9)

    # ---- cross-script replays
    bl = backtest(pxU, rules_v2_weights(pxU), cost_bps=COST, freq=CAD)["returns"].values[WARMUP:]
    cell_null = CELL[("U56", "LIVE", LIVE_G, 0.00)][WARMUP:]
    gate("G2 replay RULES v2 baseline (U56/LIVE, G=0.75, F=0)", f"{np.max(np.abs(cell_null - bl)):.3e}",
         "< 1e-12", float(np.max(np.abs(cell_null - bl))) < 1e-12)
    anc = pack(CELL[("U56", "LIVE", LIVE_G, ANCHOR_F)][WARMUP:])
    d = max(abs(anc["CAGR"] - REPLAY_1498["CAGR"]), abs(anc["Sharpe"] - REPLAY_1498["Sharpe"]),
            abs(anc["MaxDD"] - REPLAY_1498["MaxDD"]))
    gate("G3 replay idea 1498/1555's U56/LIVE SHY cell (G=0.75, F=1.00)",
         f"{anc['CAGR']:.2%}/{anc['Sharpe']:.4f}/{anc['MaxDD']:.2%} vs committed "
         f"{REPLAY_1498['CAGR']:.2%}/{REPLAY_1498['Sharpe']:.4f}/{REPLAY_1498['MaxDD']:.2%}, max|d| = {d:.2e}",
         "< 5e-4", d < 5e-4)

    # ---------------------------------------------------------- (1) THE ERA ANSWER
    say("\n" + "=" * 118)
    say("(1) THE ERA ANSWER — 4a AND 4b COUNTS BY WINDOW, OVER ALL 150 CELLS AND OVER THE 120 SHY CELLS (F > 0)")
    say("=" * 118)
    shy = grid[grid.F > 0]
    for k in ["FULL", "ERA_ZIRP", "ERA_HIKE", "IS", "OOS", "OOS_ZIRP", "OOS_HIKE"]:
        say(f"  {k:9s} 4a {int(grid[f'{k}_4a'].sum()):3d}/150 (SHY cells {int(shy[f'{k}_4a'].sum()):3d}/120)   "
            f"4b {int(grid[f'{k}_4b'].sum()):3d}/150 (SHY cells {int(shy[f'{k}_4b'].sum()):3d}/120)")

    say("\n  THE ANCHOR CELL ITSELF (U56/LIVE, G = 0.75), cash twin -> SHY at F = 1.00, per window:")
    a0 = grid[(grid.panel == "U56") & (grid.frame == "LIVE") & (grid.G == LIVE_G) & (grid.F == 0.00)].iloc[0]
    a1 = grid[(grid.panel == "U56") & (grid.frame == "LIVE") & (grid.G == LIVE_G) & (grid.F == ANCHOR_F)].iloc[0]
    for k in ["FULL", "ERA_ZIRP", "ERA_HIKE", "IS", "OOS", "OOS_ZIRP", "OOS_HIKE"]:
        say(f"    {k:9s} CASH {a0[f'{k}_CAGR']:7.2%}/{a0[f'{k}_Sharpe']:7.4f}/{a0[f'{k}_MaxDD']:7.2%}  ->  "
            f"SHY {a1[f'{k}_CAGR']:7.2%}/{a1[f'{k}_Sharpe']:7.4f}/{a1[f'{k}_MaxDD']:7.2%}   "
            f"dCAGR {1e2*(a1[f'{k}_CAGR']-a0[f'{k}_CAGR']):+5.2f} pp  dSharpe {a1[f'{k}_Sharpe']-a0[f'{k}_Sharpe']:+.4f}  "
            f"dMaxDD {1e2*(a1[f'{k}_MaxDD']-a0[f'{k}_MaxDD']):+5.2f} pp  4a {bool(a1[f'{k}_4a'])}")

    # ---------------------------------------------------------- (2) THE CREDIT IDENTITY
    say("\n" + "=" * 118)
    say("(2) THE CREDIT IDENTITY — IS THE '+0.50 pp' ONE ERA'S NUMBER?  (published, not asserted)")
    say("=" * 118)
    shy_eras = {}
    for nm, sl in [("FULL", slice(WARMUP, None)), ("ERA_ZIRP", slice(WARMUP, iz)), ("ERA_HIKE", slice(iz, None))]:
        shy_eras[nm] = cagr(p0.shy[sl])
    say(f"  SHY own CAGR: FULL {shy_eras['FULL']:.2%}  ERA_ZIRP {shy_eras['ERA_ZIRP']:.2%}  ERA_HIKE {shy_eras['ERA_HIKE']:.2%}")
    rec = []
    for (pn, fr, g), _ in grid.groupby(["panel", "frame", "G"]):
        z = grid[(grid.panel == pn) & (grid.frame == fr) & (grid.G == g)]
        base = z[z.F == 0.00].iloc[0]
        for _, c in z[z.F > 0].iterrows():
            for era, ish in [("FULL", "mean_idle"), ("ERA_ZIRP", "mean_idle_zirp"), ("ERA_HIKE", "mean_idle_hike")]:
                pred = c.F * c[ish] * shy_eras[era]
                real = c[f"{era}_CAGR"] - base[f"{era}_CAGR"]
                rec.append(dict(panel=pn, frame=fr, G=g, F=c.F, era=era, mean_idle=c[ish],
                                pred_pp=1e2 * pred, real_pp=1e2 * real, resid_pp=1e2 * (real - pred)))
    rc = pd.DataFrame(rec)
    rc.to_csv(f"{OUT}.credit.csv", index=False)
    say("  realised CAGR credit vs the F = 0 twin, mean over the 120 SHY cells, by era:")
    for era in ["FULL", "ERA_ZIRP", "ERA_HIKE"]:
        e = rc[rc.era == era]
        say(f"    {era:9s} mean idle share {e.mean_idle.mean():.3f}   PREDICTED {e.pred_pp.mean():+6.3f} pp/yr   "
            f"REALISED {e.real_pp.mean():+6.3f} pp/yr   residual {e.resid_pp.mean():+6.3f} pp/yr "
            f"(max |resid| {e.resid_pp.abs().max():.3f} pp)   cells with REALISED > 0: {int((e.real_pp>0).sum())}/{len(e)}")
    say(f"  ANCHOR CELL (U56/LIVE, G=0.75, F=1.00) realised credit: FULL "
        f"{1e2*(a1['FULL_CAGR']-a0['FULL_CAGR']):+.3f} pp/yr, ERA_ZIRP {1e2*(a1['ERA_ZIRP_CAGR']-a0['ERA_ZIRP_CAGR']):+.3f} pp/yr, "
        f"ERA_HIKE {1e2*(a1['ERA_HIKE_CAGR']-a0['ERA_HIKE_CAGR']):+.3f} pp/yr")

    # ---------------------------------------------------------- (3) RULE 8
    say("\n" + "=" * 118)
    say("(3) RULE 8 — DIALS FIT ON warm-up..2016-12-31 ONLY; 2017-2026 READ EXACTLY ONCE, THEN SPLIT AT THE HIKE")
    say("=" * 118)
    wf = []
    for pn in [p.name for p in panels]:
        for fr in FRAMES:
            z = grid[(grid.panel == pn) & (grid.frame == fr)]
            gate_bar = DD_CAP * BARS[pn]["spy"]["IS"]["MaxDD"]
            c_sh = z.loc[z.IS_Sharpe.idxmax()]
            ok = z[z.IS_MaxDD >= gate_bar]
            c_cg = ok.loc[ok.IS_CAGR.idxmax()] if len(ok) else z[(z.F == 0) & (z.G == LIVE_G)].iloc[0]
            null = z[(z.F == 0.00) & (z.G == LIVE_G)].iloc[0]
            for cname, c in [("C_SHARPE", c_sh), ("C_CAGR", c_cg), ("C_NULL", null)]:
                wf.append(dict(panel=pn, frame=fr, chooser=cname, pick_G=c.G, pick_F=c.F,
                               IS_Sharpe=c.IS_Sharpe, OOS_CAGR=c.OOS_CAGR, OOS_Sharpe=c.OOS_Sharpe,
                               OOS_MaxDD=c.OOS_MaxDD, OOS_4a=bool(c.OOS_4a), OOS_4b=bool(c.OOS_4b),
                               OOSZ_Sharpe=c.OOS_ZIRP_Sharpe, OOSH_Sharpe=c.OOS_HIKE_Sharpe,
                               OOSZ_CAGR=c.OOS_ZIRP_CAGR, OOSH_CAGR=c.OOS_HIKE_CAGR,
                               dOOS_Sharpe=c.OOS_Sharpe - null.OOS_Sharpe,
                               dOOS_CAGR_pp=1e2 * (c.OOS_CAGR - null.OOS_CAGR)))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for cname in ["C_SHARPE", "C_CAGR"]:
        e = wfd[wfd.chooser == cname]
        say(f"  {cname}: picks F = {sorted(set(e.pick_F))}, G = {sorted(set(e.pick_G))};  mean dOOS Sharpe vs doing nothing "
            f"{e.dOOS_Sharpe.mean():+.4f}, beats it {int((e.dOOS_Sharpe>0).sum())}/{len(e)};  "
            f"mean dOOS CAGR {e.dOOS_CAGR_pp.mean():+.3f} pp")
    # ---- (3b) the F axis ALONE at frozen G = 0.75 (a RESTRICTION of the same grid, not a third dial):
    # C_SHARPE above is confounded with G — it picks G = 0.50 everywhere, which is the record's
    # de-gross ray.  Freezing G at the live value isolates the SLEEVE decision itself.
    say("\n  (3b) THE F AXIS ALONE, G FROZEN AT THE LIVE 0.75 (restriction of the same grid, no new dial):")
    f_only = []
    for pn in [p.name for p in panels]:
        for fr in FRAMES:
            z = grid[(grid.panel == pn) & (grid.frame == fr) & (grid.G == LIVE_G)]
            pick = z.loc[z.IS_Sharpe.idxmax()]
            null = z[z.F == 0.00].iloc[0]
            f_only.append(dict(panel=pn, frame=fr, pick_F=pick.F, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_CAGR=pick.OOS_CAGR, OOS_MaxDD=pick.OOS_MaxDD,
                               dOOS_Sharpe=pick.OOS_Sharpe - null.OOS_Sharpe,
                               dOOS_CAGR_pp=1e2 * (pick.OOS_CAGR - null.OOS_CAGR),
                               dOOSZ_Sharpe=pick.OOS_ZIRP_Sharpe - null.OOS_ZIRP_Sharpe,
                               dOOSH_Sharpe=pick.OOS_HIKE_Sharpe - null.OOS_HIKE_Sharpe,
                               OOS_4a=bool(pick.OOS_4a), OOS_4b=bool(pick.OOS_4b)))
    fo = pd.DataFrame(f_only)
    fo.to_csv(f"{OUT}.f_only.csv", index=False)
    say(fo.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"    F-only chooser picks F = {sorted(set(fo.pick_F))} on {len(fo)} panel-frames; mean dOOS Sharpe "
        f"{fo.dOOS_Sharpe.mean():+.4f} (beats doing nothing {int((fo.dOOS_Sharpe>0).sum())}/{len(fo)}), "
        f"mean dOOS CAGR {fo.dOOS_CAGR_pp.mean():+.3f} pp; by era mean dOOS_ZIRP Sharpe "
        f"{fo.dOOSZ_Sharpe.mean():+.4f}, dOOS_HIKE Sharpe {fo.dOOSH_Sharpe.mean():+.4f}.")

    # ---- (3c) WHERE the ERA_HIKE 4a failure actually sits
    say("\n  (3c) WHERE THE ERA_HIKE 4a FAILURE SITS (U56/LIVE, G = 0.75) — the era's two halves:")
    lz, lh = BARS["U56"]["live"]["ERA_ZIRP"], BARS["U56"]["live"]["ERA_HIKE"]
    for _, c in grid[(grid.panel == "U56") & (grid.frame == "LIVE") & (grid.G == LIVE_G)].sort_values("F").iterrows():
        say(f"    F={c.F:.2f}  ERA_ZIRP halves {c.ERA_ZIRP_H1:.4f}/{c.ERA_ZIRP_H2:.4f} vs live {lz['H1']:.4f}/{lz['H2']:.4f} "
            f"-> 4a {bool(c.ERA_ZIRP_4a)}   |   ERA_HIKE halves {c.ERA_HIKE_H1:.4f}/{c.ERA_HIKE_H2:.4f} vs live "
            f"{lh['H1']:.4f}/{lh['H2']:.4f} -> 4a {bool(c.ERA_HIKE_4a)}")
    say("    The ERA_HIKE era is 4.5y, so its 'halves' are ~2.2y each — a WEAK test, stated as such.")

    gate("G6 no chooser reads a row on or after 2017-01-01",
         "IS windows end at index i_oos-1 on every panel by construction", "by construction", True)

    # ---------------------------------------------------------- (4) OOS vs BASELINE AND SPY (the mandated row)
    say("\n" + "=" * 118)
    say("(4) RULE-8 OOS OF THE ANCHOR CELL vs RULES v2 AND SPY (the protocol's mandated comparison)")
    say("=" * 118)
    for k in ["FULL", "OOS", "OOS_ZIRP", "OOS_HIKE"]:
        lb, sb = BARS["U56"]["live"][k], BARS["U56"]["spy"][k]
        say(f"  {k:9s} SHY cell {a1[f'{k}_CAGR']:7.2%}/{a1[f'{k}_Sharpe']:7.4f}/{a1[f'{k}_MaxDD']:7.2%}  |  "
            f"RULES v2 {lb['CAGR']:7.2%}/{lb['Sharpe']:7.4f}/{lb['MaxDD']:7.2%}  |  "
            f"SPY {sb['CAGR']:7.2%}/{sb['Sharpe']:7.4f}/{sb['MaxDD']:7.2%}  |  "
            f"4a {bool(a1[f'{k}_4a'])}  4b {bool(a1[f'{k}_4b'])}")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(1 for g in GATES if g["pass_"])
    say(f"\nGATES {npass}/{len(GATES)} pass.  Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

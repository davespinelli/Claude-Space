#!/usr/bin/env python3
"""Idea 1703 (lane B, 2026-09-20): does the BAND BOOK's 4b pass survive DELETING the 20
survivorship-selected single stocks?

WHY THIS IDEA.  Every memo in this record carries the same caveat in the same words -- U56 and
B136 are CURRENT-constituent lists, so every absolute level is an UPPER BOUND -- and then quotes
the 4b pass anyway.  The caveat has never been priced on the book that is actually standing.
Idea 10 (2026-09-04, lane C) came closest: it split `universe.json` into ETF-only and
single-stock panels and found EVERY 4b pass sat in STK20 (the 20 mega-caps) while ETF36 and
ETF24 failed 4b on all five books it ran.  But idea 10 tested the v1/CAND family.  The book the
record has run on since 2026-09-06 -- RULES v2, the 200d +/-c hysteresis band at constant gross
G, de-gross to cash, weekly -- did not exist yet, and neither did the 2026-09-19 CHANGELOG's
rule-8 legitimate pick (U56 weekly, c = 0.10, G = 1.00: FULL 11.72% / 1.1726 / -16.30%, OOS
12.14% / 1.1940 / -16.30%), which is the one book in this repository currently described as
clearing 4b on FULL and OOS at 0 / 10 / 25 / 50 bps.

THE SPLIT IS THE WHOLE POINT.  `universe.json` is 36 ETFs (8 broad + 16 sector/industry + 12
bond/FX/commodity, ex-crypto) and 20 mega-cap single stocks.  The two legs carry COMPLETELY
DIFFERENT survivorship exposure, and the asymmetry is structural, not statistical:

  STK20  AAPL MSFT NVDA AMZN GOOGL META TSLA AVGO BRK-B JPM LLY UNH V XOM COST NFLX AMD CRM
         ORCL PLTR.  Every one of these is in the file BECAUSE IT WON.  A 2009-vintage mega-cap
         list would have held GE, C, PFE, T, INTC, IBM, WFC, MO and XOM at very different
         weights; the ones that fell out are not here.  This leg is maximally flattered.
  ETF36  SPY QQQ IWM DIA EFA EEM VTI RSP / XLK XLF XLV XLE XLI XLY XLP XLU XLB XLRE XLC SMH XBI
         KRE ITB GDX / TLT IEF SHY HYG LQD TIP GLD SLV USO UNG DBC UUP.  NO ETF IS IN THIS FILE
         BECAUSE IT WON.  These are index products that any 2009-vintage list would have named,
         they are not screened on performance, and none of them was dropped for failing -- USO
         and UNG are in the file having lost 80-99% of their value.  This leg is the
         survivorship-CLEAN half of the live universe.

So the question is exact and it is a capital question, not a bookkeeping one: if the band book's
4b pass is a real trend-following phenomenon it should appear, weaker but present, on the clean
leg.  If it appears ONLY on the leg whose names were chosen ex post for winning, then the one
book this repository would put money behind is a survivorship artifact and should be labelled as
one before, not after, capital moves.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  c  {0.00, 0.03, 0.05, 0.10, 0.15}   DIAL 1 -- the 200d band half-width.  0.03 is the LIVE
                                      value; 0.10 is the 2026-09-19 rule-8 pick; 0.00 is the
                                      bare 200d MA gate with no hysteresis.
  G  {0.25, 0.50, 0.75, 1.00}         DIAL 2 -- constant target gross.  0.75 is LIVE; 1.00 is
                                      the rung every committed 4b pass sits at.  Stops at 1.00:
                                      no leverage (rule 2).

20 cells per panel.  NOT DIALS, every value reported: PANEL, cadence (weekly, the live value),
cost (10 bps, the protocol value), window (FULL / H1 / H2 / IS / OOS).

PANELS (not a dial -- the whole grid is run on every one and none is picked on its result):
  U56     all 56 investable names of universe.json ex-crypto           the live universe, control
  ETF36   the 36 ETFs                                                  survivorship-CLEAN leg
  STK20   the 20 mega-cap single stocks                                survivorship-FLATTERED leg
  R20xNN  20 matched-count random draws of 20 names from ETF36, seeds 0..19.  STK20 vs ETF36
          confounds asset class with NAME COUNT (20 vs 36 changes both diversification and the
          gross/N position size).  The random draws hold the count fixed at 20 so the STK20 -
          ETF20 contrast is read at matched breadth.  Draws are made with a FIXED seed from a
          FIXED name list before any return is looked at; all 20 are reported, median and full
          range, none is selected.

23 panels x 20 cells = 460 books, EVERY ONE PUBLISHED in the .grid.csv.  A NO-GATE control
(always-invested equal weight at the same target gross G, i.e. the band removed entirely) is run
for every (panel, G) -- 92 more books -- and published: it is a fixed twin, never a grid cell and
never choosable, and it is what tells the reader whether the gate is doing anything on a panel
at all.

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_SHARPE  argmax IS Sharpe over all 20 cells                       (the record's usual chooser)
  C_MEMO    smallest G whose IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
            ties broken by smallest c; else fall back to (0.03, 0.75) -- the 2026-09-03
            RECOMMENDATION memo's own pre-registered rule
  C_CAGR    argmax IS CAGR among cells whose IS MaxDD <= 0.60 x SPY_IS MaxDD
  C_ANCHOR  (0.03, 0.75), the live book, choosing nothing            (the null)

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN (pre-registered; no tuning after):
  (i)   If ETF36 and the R20 median FAIL 4b at every cell and on every chooser pick while U56
        and/or STK20 pass, then the standing 4b pass is CARRIED BY THE SURVIVORSHIP-SELECTED
        LEG.  Verdict KILL of the capital claim, and the record should say so in the caveat line
        rather than in a footnote.
  (ii)  If ETF36 clears 4b on FULL and OOS at its own rule-8 pick, the pass is survivorship-CLEAN
        and that is a genuine KEEP-4b candidate worth real capital -- the first in this record
        whose universe was not chosen ex post.
  (iii) If STK20 also fails, the pass is neither: it is a 56-name DIVERSIFICATION effect that
        neither leg reproduces alone, and the finding is about breadth, not survivorship.
All three outcomes are reported.  Nothing is re-tuned after reading the answer.

HONEST LIMITS OF THIS TEST, STATED UP FRONT.  Deleting STK20 does NOT remove survivorship bias
from U56 -- it removes the leg that carries most of it.  ETF36 is not bias-free either: the 16
sector/industry ETFs were named in 2026 and a 2009-vintage list might have chosen differently
(though not on realised return), and every ETF price series here is an ADJUSTED close from a
current-listing cache.  What ETF36 removes is the specific and large bias of holding twenty names
that are in the file because they became the twenty largest companies in America.  The contrast
STK20 - ETF36 is therefore a LOWER BOUND on the survivorship content of the pass, not a
measurement of all of it.

GATES.  G0 sample >= 10y (rule 1).  G1 CROSS-SCRIPT REPLAY: the U56 (c=0.03, G=0.75) cell must
reproduce `baseline.rules_v2_weights` through `engine.backtest` to floating-point noise -- that
cell IS the live book.  G2 NO LEVERAGE and no shorting: max target gross <= 1.0.  G3 all 460
grid cells + 92 no-gate controls published.  G4 exactly two tuned parameters.  G5 no chooser
reads a row on or after 2017-01-01 -- asserted by construction AND tested by re-fitting on
hard-truncated arrays.  G6 determinism: a sampled cell recomputes bit-identical.  G7 PUBLISHED,
not asserted: per-panel name counts and composition, realised mean gross, in-band share,
turnover/yr.  G8 PUBLISHED: the no-gate twin at every (panel, G).

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 live
baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 5 (one idea, one script); rule 7
(report honestly); rule 8 (walk-forward); rule 9 (survivorship stated -- it is the subject).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_does-the-band-book-4b-pass-survive-deleting-the-20-single-stocks_B.py
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-20", "does-the-band-book-4b-pass-survive-deleting-the-20-single-stocks"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP = 260
COST = 10.0
CAD = "W"
GRID_C = [0.00, 0.03, 0.05, 0.10, 0.15]
GRID_G = [0.25, 0.50, 0.75, 1.00]
LIVE_C, LIVE_G = 0.03, 0.75            # the live RULES v2 cell
PICK_C, PICK_G = 0.10, 1.00            # the 2026-09-19 CHANGELOG rule-8 pick
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
N_DRAW, DRAW_K = 20, 20                # 20 random draws of 20 ETFs

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


def pack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a against the LIVE book; 4b against SPY.  Returns both verdicts and the 4b legs."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- the book
class Tape:
    """One price frame (U56 ex-crypto, SPY included) + the per-name band states."""

    def __init__(self, px):
        self.px = px
        self.idx = px.index
        self.cols = list(px.columns)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.band = {c: band_state(px, band=c).values for c in GRID_C}
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def targets(tape, names_ix, c, g, gate_on=True):
    """RULES v2 shape restricted to a panel: gross g spread over the names PRICED that day,
    held only where the 200d +/-c band says IN; gated-out weight goes to CASH (never re-spread).
    gate_on=False is the NO-GATE twin (always invested, equal weight, same target gross)."""
    T, M = tape.rets.shape
    W = np.zeros((T, M))
    pr = tape.priced[:, names_ix].astype(float)
    n = pr.sum(axis=1)
    ew = np.zeros_like(pr)
    nz = n > 0
    ew[nz] = g * pr[nz] / n[nz, None]
    if gate_on:
        ew = ew * tape.band[c][:, names_ix]
    W[:, names_ix] = ew
    return W


def run(tape, W, cost=COST):
    """engine.backtest's arithmetic, vectorised per rebalance segment: weights decided at the
    close of the rebalance day are applied the next day, positions drift in between, un-invested
    NAV earns 0.00%, turnover is charged at `cost` bps on both legs."""
    rets = tape.rets
    T, M = rets.shape
    reb = tape.reb
    out = np.zeros(T)
    turn = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wmax = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = tape.C, tape.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = W[i0 - 1] if i0 > 0 else W[0]          # decided at close t-1, applied from t
        s0 = float(w0.sum())
        wmax = max(wmax, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, wmax, gsum


# ---------------------------------------------------------------- choosers (rule 8)
def c_sharpe(cells, isp):
    return max(cells, key=lambda k: (isp[k]["Sharpe"], -k[1], -k[0]))


def c_memo(cells, isp, dd_bar, cagr_bar):
    ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar and isp[k]["CAGR"] >= cagr_bar]
    if not ok:
        return (LIVE_C, LIVE_G), True
    return min(ok, key=lambda k: (k[1], k[0])), False


def c_cagr(cells, isp, dd_bar):
    ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar]
    if not ok:
        return (LIVE_C, LIVE_G), True
    return max(ok, key=lambda k: (isp[k]["CAGR"], -k[1], -k[0])), False


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1703 (lane B, 2026-09-20) — does the BAND BOOK's 4b pass survive DELETING the 20")
    say("survivorship-selected single stocks?  Panels U56 / ETF36 / STK20 / 20 matched-count")
    say(f"random ETF20 draws.  DIALS: c {GRID_C} x G {GRID_G}.  Weekly, {COST:.0f} bps, t+1.")
    say("=" * 118)

    px = load_universe()
    tape = Tape(px)
    cols = tape.cols
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etf = [t for grp in ("broad", "sectors", "bonds_fx_commod") for t in U[grp] if t in cols]
    stk = [t for t in U["megacap"] if t in cols]
    u56 = [t for t in cols]
    say(f"\n  TAPE: {tape.idx[0].date()} .. {tape.idx[-1].date()}  {len(tape.idx)} rows "
        f"({len(tape.idx)/252:.1f}y), {len(cols)} investable columns.")
    gate("G0 min sample >= 10 years (rule 1)", round(len(tape.idx) / 252.0, 2), ">= 10.0",
         len(tape.idx) / 252.0 >= 10.0)
    say(f"  ETF36 ({len(etf)}): {' '.join(etf)}")
    say(f"  STK20 ({len(stk)}): {' '.join(stk)}")
    publish("G7 COMPOSITION ETF36", f"{len(etf)} names: {','.join(etf)}")
    publish("G7 COMPOSITION STK20", f"{len(stk)} names: {','.join(stk)}")
    say("  SURVIVORSHIP (rule 9) — THE SUBJECT OF THIS RUN: U56 is a CURRENT-constituent list, so "
        "every absolute level below is an UPPER BOUND.  STK20 carries the bulk of that bias (its "
        "20 names are in the file because they became the 20 largest US companies); ETF36 carries "
        "far less (no ETF is in the file for having won — USO and UNG are in it having lost "
        "80-99%).  The STK20 - ETF36 contrast is a LOWER BOUND on the pass's survivorship content.")

    rng = np.random.default_rng(1703)
    draws = [sorted(rng.choice(etf, size=DRAW_K, replace=False).tolist()) for _ in range(N_DRAW)]
    panels = [("U56", u56), ("ETF36", etf), ("STK20", stk)]
    panels += [(f"R20x{i:02d}", d) for i, d in enumerate(draws)]
    for i, d in enumerate(draws[:3]):
        say(f"  R20x{i:02d}: {' '.join(d)}")
    publish("G7 RANDOM DRAWS", f"seed 1703, {N_DRAW} draws of {DRAW_K} from ETF36, fixed before "
                               f"any return was read")

    i_oos = int(np.searchsorted(tape.idx.values, np.datetime64(OOS_START)))
    spy_f, spy_i, spy_o = pack(tape.spy[WARMUP:]), pack(tape.spy[WARMUP:i_oos]), pack(tape.spy[i_oos:])
    say(f"\n  SPY FULL {spy_f['CAGR']:.2%} / {spy_f['Sharpe']:.4f} / {spy_f['MaxDD']:.2%} "
        f"H1/H2 {spy_f['H1']:.3f}/{spy_f['H2']:.3f}")
    say(f"      4b bars FULL: Sharpe H1>{spy_f['H1']:.4f}, H2>{spy_f['H2']:.4f}, "
        f"MaxDD >= {DD_CAP*spy_f['MaxDD']:.2%}, CAGR >= {CAGR_FLOOR*spy_f['CAGR']:.2%}")
    say(f"  SPY OOS  {spy_o['CAGR']:.2%} / {spy_o['Sharpe']:.4f} / {spy_o['MaxDD']:.2%}")
    say(f"      4b bars OOS:  MaxDD >= {DD_CAP*spy_o['MaxDD']:.2%}, "
        f"CAGR >= {CAGR_FLOOR*spy_o['CAGR']:.2%}")
    say(f"  SPY IS   {spy_i['CAGR']:.2%} / {spy_i['MaxDD']:.2%}  (the bars C_MEMO and C_CAGR read)")

    # ---- the live book (RULES v2 on U56): the 4a comparand for every panel
    lr = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=CAD)["returns"].values
    live_f, live_o = pack(lr[WARMUP:]), pack(lr[i_oos:])
    say(f"  RULES v2 LIVE (U56) FULL {live_f['CAGR']:.2%} / {live_f['Sharpe']:.4f} / "
        f"{live_f['MaxDD']:.2%} H1/H2 {live_f['H1']:.3f}/{live_f['H2']:.3f}")
    say(f"  RULES v2 LIVE (U56) OOS  {live_o['CAGR']:.2%} / {live_o['Sharpe']:.4f} / {live_o['MaxDD']:.2%}")
    say("  NOTE ON 4a: path 4a asks whether a candidate beats THE BOOK.  The book is RULES v2 as "
        "actually traded, i.e. on U56 — so 4a is judged against that single row on every panel, "
        "not against a panel-local re-fit.  The panel-local (c=0.03, G=0.75) cell is in the grid "
        "for anyone who wants the other reading.")

    ix = {n: np.array([cols.index(t) for t in names]) for n, names in panels}

    # ---- G1 cross-script replay: the U56 live cell IS baseline.rules_v2_weights
    Wlive = targets(tape, ix["U56"], LIVE_C, LIVE_G)
    r_fast, _, _, _ = run(tape, Wlive)
    # engine.backtest shifts AFTER filling, so its rows before the first weekly rebalance are NaN;
    # this runner seeds them with W[0] instead.  Both conventions sit inside the 260-row warm-up
    # that every metric in this file already discards, so the replay is read from WARMUP on and
    # the number of NaN rows engine produces is published rather than hidden.
    n_nan = int(np.isnan(lr).sum())
    d_ret = float(np.max(np.abs(r_fast[WARMUP:] - lr[WARMUP:])))
    publish("G1a engine.backtest NaN warm-up rows (before its first weekly rebalance)",
            f"{n_nan} of {len(lr)}, last at index {int(np.flatnonzero(np.isnan(lr)).max()) if n_nan else -1} "
            f"(warm-up discards the first {WARMUP})")
    gate("G1 replay U56 (c=0.03,G=0.75) vs engine.backtest(baseline.rules_v2_weights), rows >= WARMUP",
         f"{d_ret:.3e}", "< 1e-12", d_ret < 1e-12)

    grid, ctrl = [], []
    RET, ISP = {}, {}
    wmax_global = 0.0
    for pname, names in panels:
        nix = ix[pname]
        for g in GRID_G:
            rr, tu, ws, gs = run(tape, targets(tape, nix, 0.0, g, gate_on=False))
            wmax_global = max(wmax_global, ws)
            m, mo = pack(rr[WARMUP:]), pack(rr[i_oos:])
            k4a, k4b, _, _, _, legs = keep_paths(rr[WARMUP:], spy_f, live_f)
            k4aO, k4bO, _, _, _, legsO = keep_paths(rr[i_oos:], spy_o, live_o)
            ctrl.append(dict(panel=pname, G=g, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=m["H1"], H2=m["H2"], oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                             oMaxDD=mo["MaxDD"], keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO,
                             turnover_yr=float(tu[WARMUP:].sum() / ((len(rr) - WARMUP) / 252.0))))
        for c in GRID_C:
            for g in GRID_G:
                W = targets(tape, nix, c, g)
                rr, tu, ws, gs = run(tape, W)
                wmax_global = max(wmax_global, ws)
                RET[(pname, c, g)] = rr
                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy_f, live_f)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spy_o, live_o)
                isp = dict(Sharpe=sharpe(rr[WARMUP:i_oos]), CAGR=cagr(rr[WARMUP:i_oos]),
                           MaxDD=mdd(rr[WARMUP:i_oos]))
                ISP[(pname, c, g)] = isp
                inband = float(np.mean(tape.band[c][WARMUP:][:, nix]))
                grid.append(dict(panel=pname, n_names=len(names), c=c, G=g,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                 oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                 isCAGR=isp["CAGR"], isSharpe=isp["Sharpe"], isMaxDD=isp["MaxDD"],
                                 mean_gross=float(np.mean(gs[WARMUP:])), in_band_share=inband,
                                 turnover_yr=float(tu[WARMUP:].sum() / ((len(rr) - WARMUP) / 252.0)),
                                 keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                 leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                 leg_CAGR=legs["CAGR"], oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"],
                                 oleg_H1=legsO["H1"], oleg_H2=legsO["H2"]))
    G = pd.DataFrame(grid)
    CT = pd.DataFrame(ctrl)
    gate("G2 no leverage / no shorting: max target gross", f"{wmax_global:.6f}", "<= 1.000001",
         wmax_global <= 1.000001)
    gate("G3 all grid cells published", f"{len(G)} cells + {len(CT)} no-gate controls",
         f"{len(panels)*len(GRID_C)*len(GRID_G)} + {len(panels)*len(GRID_G)}",
         len(G) == len(panels) * len(GRID_C) * len(GRID_G) and len(CT) == len(panels) * len(GRID_G))
    gate("G4 tuned parameters", "2 (c, G)", "<= 2 (rule 4)", True)

    # ---- G6 determinism
    rr2, _, _, _ = run(tape, targets(tape, ix["ETF36"], PICK_C, PICK_G))
    gate("G6 determinism: ETF36 (0.10,1.00) recompute", f"{float(np.max(np.abs(rr2 - RET[('ETF36', PICK_C, PICK_G)]))):.3e}",
         "== 0", bool(np.array_equal(rr2, RET[("ETF36", PICK_C, PICK_G)])))

    # ---------------------------------------------------------------- headline table
    say("\n" + "=" * 118)
    say("THE THREE LEGS AT THE TWO CELLS THAT MATTER — live (c=0.03, G=0.75) and the 2026-09-19")
    say("rule-8 pick (c=0.10, G=1.00).  4b is judged against SPY, 4a against RULES v2 live on U56.")
    say("=" * 118)
    hdr = (f"  {'panel':7s} {'cell':13s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
           f"{'oCAGR':>7s} {'oSharpe':>8s} {'oMaxDD':>8s}  4b(F/O)  4a  legs failing (FULL)")
    say(hdr)
    for pname in ("U56", "ETF36", "STK20"):
        for (c, g) in ((LIVE_C, LIVE_G), (PICK_C, PICK_G)):
            row = G[(G.panel == pname) & (G.c == c) & (G.G == g)].iloc[0]
            fails = [k for k in ("H1", "H2", "DD", "CAGR") if not row[f"leg_{k}"]]
            say(f"  {pname:7s} c={c:.2f} G={g:.2f} {row.CAGR:7.2%} {row.Sharpe:7.4f} {row.MaxDD:8.2%} "
                f"{row.H1:6.3f} {row.H2:6.3f} {row.oCAGR:7.2%} {row.oSharpe:8.4f} {row.oMaxDD:8.2%}  "
                f"{'Y' if row.keep4b else 'n'}/{'Y' if row.keep4b_oos else 'n'}     "
                f"{'Y' if row.keep4a else 'n'}   {','.join(fails) if fails else '(none)'}")

    say("\n  SAME TWO CELLS ON THE 20 MATCHED-COUNT RANDOM ETF20 DRAWS (median [min, max]):")
    for (c, g) in ((LIVE_C, LIVE_G), (PICK_C, PICK_G)):
        R = G[(G.panel.str.startswith("R20x")) & (G.c == c) & (G.G == g)]
        say(f"    c={c:.2f} G={g:.2f}  CAGR {R.CAGR.median():.2%} [{R.CAGR.min():.2%}, {R.CAGR.max():.2%}]  "
            f"Sharpe {R.Sharpe.median():.4f} [{R.Sharpe.min():.4f}, {R.Sharpe.max():.4f}]  "
            f"MaxDD {R.MaxDD.median():.2%} [{R.MaxDD.min():.2%}, {R.MaxDD.max():.2%}]  "
            f"4b FULL {int(R.keep4b.sum())}/{len(R)}  4b OOS {int(R.keep4b_oos.sum())}/{len(R)}  "
            f"4a {int(R.keep4a.sum())}/{len(R)}")

    say("\n  4b / 4a PASS COUNTS OVER THE WHOLE 20-CELL GRID, PER PANEL:")
    say(f"  {'panel':8s} {'4b FULL':>8s} {'4b OOS':>8s} {'4b BOTH':>8s} {'4a FULL':>8s} {'4a OOS':>8s}"
        f"   best-Sharpe cell (FULL)")
    for pname, _ in panels:
        P = G[G.panel == pname]
        both = int((P.keep4b & P.keep4b_oos).sum())
        b = P.loc[P.Sharpe.idxmax()]
        say(f"  {pname:8s} {int(P.keep4b.sum()):8d} {int(P.keep4b_oos.sum()):8d} {both:8d} "
            f"{int(P.keep4a.sum()):8d} {int(P.keep4a_oos.sum()):8d}   c={b.c:.2f} G={b.G:.2f} "
            f"{b.Sharpe:.4f} / {b.CAGR:.2%} / {b.MaxDD:.2%}")

    say("\n  WHICH 4b LEG FAILS, PER PANEL, OVER ALL 20 CELLS (FULL window):")
    for pname, _ in panels[:3]:
        P = G[G.panel == pname]
        say(f"    {pname:8s} H1 fails {int((~P.leg_H1).sum()):2d}/20, H2 {int((~P.leg_H2).sum()):2d}/20, "
            f"DD {int((~P.leg_DD).sum()):2d}/20, CAGR {int((~P.leg_CAGR).sum()):2d}/20")
    Rall = G[G.panel.str.startswith("R20x")]
    say(f"    {'R20 pool':8s} H1 fails {int((~Rall.leg_H1).sum()):3d}/{len(Rall)}, "
        f"H2 {int((~Rall.leg_H2).sum()):3d}/{len(Rall)}, DD {int((~Rall.leg_DD).sum()):3d}/{len(Rall)}, "
        f"CAGR {int((~Rall.leg_CAGR).sum()):3d}/{len(Rall)}")

    # ---------------------------------------------------------------- no-gate controls (G8)
    say("\n  G8 NO-GATE TWIN (always invested, equal weight, same target gross — the band removed):")
    say(f"  {'panel':8s} {'G':>5s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'oSharpe':>8s} {'oMaxDD':>8s}  4b F/O")
    for pname in ("U56", "ETF36", "STK20"):
        for g in GRID_G:
            row = CT[(CT.panel == pname) & (CT.G == g)].iloc[0]
            say(f"  {pname:8s} {g:5.2f} {row.CAGR:7.2%} {row.Sharpe:7.4f} {row.MaxDD:8.2%} "
                f"{row.oSharpe:8.4f} {row.oMaxDD:8.2%}  {'Y' if row.keep4b else 'n'}/"
                f"{'Y' if row.keep4b_oos else 'n'}")
    say("    (the gate's value on a panel is the BAND cell minus this twin at the same G)")
    for pname in ("U56", "ETF36", "STK20"):
        for g in (0.75, 1.00):
            b = G[(G.panel == pname) & (G.c == LIVE_C) & (G.G == g)].iloc[0]
            n = CT[(CT.panel == pname) & (CT.G == g)].iloc[0]
            say(f"    GATE VALUE {pname:6s} G={g:.2f}: dSharpe {b.Sharpe-n.Sharpe:+.4f}, "
                f"dMaxDD {b.MaxDD-n.MaxDD:+.2%}, dCAGR {b.CAGR-n.CAGR:+.2%} (c=0.03 vs no gate)")

    # ---------------------------------------------------------------- rule 8
    say("\n" + "=" * 118)
    say("RULE 8 WALK-FORWARD — (c, G) chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE.")
    say("=" * 118)
    cells = [(c, g) for c in GRID_C for g in GRID_G]
    dd_bar, cagr_bar = DD_CAP * spy_i["MaxDD"], CAGR_FLOOR * spy_i["CAGR"]
    wf = []
    say(f"  {'panel':8s} {'chooser':9s} {'pick':14s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
        f"{'OOS MaxDD':>10s}  4b OOS  4a OOS  vs SPY OOS Sharpe  vs LIVE OOS Sharpe")
    for pname, _ in panels:
        isp = {k: ISP[(pname, k[0], k[1])] for k in cells}
        picks = [("C_SHARPE", c_sharpe(cells, isp), False),
                 ("C_MEMO",) + c_memo(cells, isp, dd_bar, cagr_bar),
                 ("C_CAGR",) + c_cagr(cells, isp, dd_bar),
                 ("C_ANCHOR", (LIVE_C, LIVE_G), False)]
        for nm, k, fb in picks:
            r = RET[(pname, k[0], k[1])]
            k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spy_o, live_o)
            wf.append(dict(panel=pname, chooser=nm, c=k[0], G=k[1], fallback=fb,
                           oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                           keep4b_oos=k4bO, keep4a_oos=k4aO,
                           oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                           oleg_CAGR=legsO["CAGR"]))
            if pname in ("U56", "ETF36", "STK20"):
                say(f"  {pname:8s} {nm:9s} c={k[0]:.2f} G={k[1]:.2f}{'*' if fb else ' '} "
                    f"{mo['CAGR']:9.2%} {mo['Sharpe']:11.4f} {mo['MaxDD']:10.2%}  "
                    f"{'Y' if k4bO else 'n':^6s}  {'Y' if k4aO else 'n':^6s}  "
                    f"{mo['Sharpe']-spy_o['Sharpe']:+.4f}            {mo['Sharpe']-live_o['Sharpe']:+.4f}")
    WF = pd.DataFrame(wf)
    RWF = WF[WF.panel.str.startswith("R20x")]
    for nm in ("C_SHARPE", "C_MEMO", "C_CAGR", "C_ANCHOR"):
        S = RWF[RWF.chooser == nm]
        say(f"  R20 pool {nm:9s} (20 draws)  OOS CAGR med {S.oCAGR.median():.2%}, Sharpe med "
            f"{S.oSharpe.median():.4f} [{S.oSharpe.min():.4f}, {S.oSharpe.max():.4f}], MaxDD med "
            f"{S.oMaxDD.median():.2%}  4b OOS {int(S.keep4b_oos.sum())}/20  4a OOS "
            f"{int(S.keep4a_oos.sum())}/20")
    say("  (* = the chooser's documented fallback fired: no IS cell met the memo's bars)")

    # ---- G5: no chooser reads a 2017+ row (tested on hard-truncated arrays)
    flips = 0
    for pname, _ in panels:
        isp_t = {}
        for k in cells:
            r = RET[(pname, k[0], k[1])][WARMUP:i_oos].copy()      # hard truncation
            isp_t[k] = dict(Sharpe=sharpe(r), CAGR=cagr(r), MaxDD=mdd(r))
        if (c_sharpe(cells, isp_t) != c_sharpe(cells, {k: ISP[(pname, k[0], k[1])] for k in cells})
                or c_memo(cells, isp_t, dd_bar, cagr_bar)[0]
                != c_memo(cells, {k: ISP[(pname, k[0], k[1])] for k in cells}, dd_bar, cagr_bar)[0]):
            flips += 1
    gate("G5 choosers are IS-only (hard-truncation test)", f"{flips} picks changed", "0", flips == 0)

    # ---------------------------------------------------------------- the answer
    say("\n" + "=" * 118)
    u = G[(G.panel == "U56")]; e = G[(G.panel == "ETF36")]; s = G[(G.panel == "STK20")]
    ub, eb, sb = int((u.keep4b & u.keep4b_oos).sum()), int((e.keep4b & e.keep4b_oos).sum()), int((s.keep4b & s.keep4b_oos).sum())
    rb = int((Rall.keep4b & Rall.keep4b_oos).sum())
    say(f"ANSWER — 4b passes on FULL *and* OOS:  U56 {ub}/20   ETF36 {eb}/20   STK20 {sb}/20   "
        f"R20 pool {rb}/{len(Rall)}")
    ewf = WF[(WF.panel == "ETF36")]
    say(f"        ETF36 rule-8 picks clearing 4b OOS: {int(ewf.keep4b_oos.sum())}/4; "
        f"U56 {int(WF[(WF.panel=='U56')].keep4b_oos.sum())}/4; "
        f"STK20 {int(WF[(WF.panel=='STK20')].keep4b_oos.sum())}/4")
    say("=" * 118)

    G.to_csv(f"{OUT}.grid.csv", index=False)
    CT.to_csv(f"{OUT}.nogate.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nWrote {OUT.name}.grid.csv ({len(G)} cells), .nogate.csv ({len(CT)}), "
        f".walkforward.csv ({len(WF)}), .gates.csv ({len(GATES)})")
    say(f"Deterministic, offline, {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

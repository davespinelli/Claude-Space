#!/usr/bin/env python3
"""Idea 2034 (lane cloud, 2026-09-20) — IS THE 4b VERDICT ITSELF A 2020 ARTEFACT ONCE THE SPY BAR
IS HELD FIXED?

THE DEFECT THIS PRICES.  Idea 2022 (lane cloud, same day) re-scored its 420-cell vol-target corpus
on a crash-excised tape and published the census move **4b 187 -> 80 of 420 cells, 4a 40 -> 0**.
Its own text disclosed the confound: excising 2020 moves SPY's FULL-sample MaxDD from -33.72% to
-24.50%, which TIGHTENS the 4b drawdown cap `0.60 x SPY` from -20.23% to -14.70%, while the book's
own MaxDD does not move at all (the deepest book drawdowns sit outside the excised window).  Idea
2038 (lane C) measured the same thing on the OOS legs and called it a BAR SHIFT.  So the published
census move mixes two entirely different effects and the record has never separated them:

    BOOK EFFECT  — what excision does to the BOOK's own statistics.
    BAR EFFECT   — what excision does to the BENCHMARK the book is judged against.

WHAT IS PRICED HERE.  Idea 2022's exact 420-cell corpus is rebuilt (same runners, same panels,
same grid, same sigma convention, same warm-up, same IS/OOS split), and every cell is scored on a
full 3 x 4 CROSS of

    BOOK TAPE  in {FULL, CRASH_PT, CRASH_WIDE}      (which days the BOOK is measured on)
    BAR CONVENTION in {OWN, FULL, ABS}              (which days the BENCHMARK is measured on)

where OWN reads SPY and live RULES v2 on the SAME tape as the book (idea 2022's convention, the
one that produced 187 -> 80), FULL reads them on the panel's FULL tape and FREEZES them against
the excision, and ABS freezes ONE vector of bar levels — U56's FULL-tape SPY and live-RULES-v2
legs — and applies it to every panel and every tape, so the bar cannot move at all.

The 2 x 2 that answers the idea is then read directly off that cross at 10 bps:

    N(book FULL, bar FULL) = 187     the published baseline
    N(book EXC,  bar OWN)  =  80     the published excised census
    N(book FULL, bar EXC)            BAR effect alone   (book untouched, bar moved)
    N(book EXC,  bar FULL)           BOOK effect alone  (bar frozen, book moved)
    interaction = total - bar - book

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  ATTRIBUTION.  Decompose the published -107 cell move at 10 bps into BAR, BOOK and
      INTERACTION parts.  If |BAR| >= 2 x |BOOK| the published census move is PRIMARILY a
      benchmark artefact and "the crash carries the 4b pass" must be restated.  If
      |BOOK| >= 2 x |BAR| it is primarily a book failure and idea 2022's reading stands.  In
      between -> MIXED, and the run reports the split leg by leg.
  V2  LEG ATTRIBUTION.  For each of the five 4b legs, the count of cells whose PASS/FAIL flips
      under BAR-only vs under BOOK-only.  A leg that flips under BAR-only and not under BOOK-only
      is a leg whose excised verdict says nothing about the book.
  V3  BAR-FROZEN SURVIVAL.  With the bar frozen (FULL and ABS), how many of the 187 published 4b
      passes survive the excision, and does the standing KEEP-4b candidate (VOLTGT t=0.10, T=M,
      R=M) survive?  A candidate that survives excision under a frozen bar but not under a moving
      bar was never falsified by 2022.
  V4  CAPITAL.  Both KEEP paths at EVERY cell of the cross against live RULES v2 AND SPY, and
      rule 8 run on every (book tape x bar convention): the pair (t, h) for the DRIFT family and
      (t, R) for the CALENDAR family chosen on 2009-2016 ONLY by two legal IS-only choosers,
      2017-2026 read exactly ONCE.

DIALS.  NOTHING NEW IS TUNED.  `t` (TARGET) and `h` (THRESHOLD) are idea 1799's / 2022's two
inherited dials and the only ones a chooser ever spends; the calendar family spends `t` and `R`.
REPORTED, NOT TUNED (every grid point published in `.grid.csv.gz`): BAR CONVENTION {OWN, FULL,
ABS} (the axis under test), CRASH WINDOW {PT, WIDE}, TRADE cadence T in {W, M}, PANEL {U56, B136,
SMALL}, COST {0, 10, 25, 50} bps.

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel is a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
The BAR-vs-BOOK contrast is same-tape / same-names / same-grid with only the SCORING convention
moved, so it is first-order immune; the PASS COUNTS are not.  Note also the 2026-09-20 data-vintage
finding: the SMALL cache grew 439 -> 665 names, so SMALL-panel counts here are not comparable with
pre-2026-09-20 SMALL numbers.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_4b-verdict-bar-vs-book_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-20", "4b-verdict-bar-vs-book"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
TRADES = ["W", "M"]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0

# REPORTED, not tuned (idea 2022's two windows, verbatim)
CRASH = {"CRASH_PT":   ("2020-02-19", "2020-03-23"),
         "CRASH_WIDE": ("2020-02-19", "2020-04-30")}
TAPES = ["FULL"] + list(CRASH)
BARS = ["FULL", "CRASH_PT", "CRASH_WIDE", "ABS"]   # which days the BENCHMARK is read on
ABS_PANEL = "U56"          # the panel whose FULL-tape bars become the frozen absolute bar
# idea 2022's convention is the DIAGONAL of the cross: bar == book_tape ("OWN")

# the standing KEEP-4b candidate (idea 2038's C_KEEP), tracked cell by cell
STANDING = dict(target=0.10, T_trade="M", family="CAL", cell="R=M")

# committed numbers this run must reproduce (idea 2022's published census + the VOLTGT memo)
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
PUB_2022 = {("FULL", "keep4b_full"): 187, ("FULL", "keep4a"): 40,
            ("CRASH_PT", "keep4b_full"): 80, ("CRASH_PT", "keep4a"): 0,
            ("CRASH_WIDE", "keep4b_full"): 89, ("CRASH_WIDE", "keep4a"): 0}
PUB_BARSHIFT = dict(spy_full_dd=-0.3372, spy_pt_dd=-0.2450)

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ----------------------------------------------------------------------------- panels
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    dropped = len([c for c in pxs.columns if c in bad])
    return ([("U56", px56, list(px56.columns)),
             ("B136", px136, list(px136.columns)),
             (f"SMALL{len(small_cols)}", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio through close
    t-d.  (L, d) = (20, 0) is the standing memo's convention."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------ the two refresh runners (idea 1799 verbatim)
def bt_cal(px_ret, W0, g0, mT, mR):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        if mR[i] or i == 0:
            g_eff = g0[i]
            nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif mR[i]:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


def bt_drift(px_ret, W0, g0, mT, h):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        trig = abs(g0[i] - cur.sum()) > h
        if trig or i == 0:
            g_eff = g0[i]
            nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif trig:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


class Book:
    def __init__(self, px, cols, index):
        self.index = index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((1, ew.shape[1])), ew[:-1]])
        self.SIG = panel_sigma(px, cols)
        self.masks = {}
        for f in ("D", "W", "M", "Q"):
            m = np.asarray(rebalance_mask(index, f).values, bool)
            self.masks[f] = np.concatenate([[False], m[:-1]])

    def g_of(self, tgt):
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([[0.0], g[:-1]])

    def run_cal(self, g0, T, R):
        r, t, gs, nref = bt_cal(self.R, self.W, g0, self.masks[T], self.masks[R])
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)

    def run_drift(self, g0, T, h):
        r, t, gs, nref = bt_drift(self.R, self.W, g0, self.masks[T], h)
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)


# ----------------------------------------------------------------------------- metrics
def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def binding(mar):
    bad = [k for k in LEGS if not (mar[k] > 0)]
    return ("|".join(bad) if bad else "none", len(bad))


def tape_mask(index, tape):
    """Boolean keep-mask for a tape.  FULL keeps everything; a CRASH_* tape drops the window."""
    if tape == "FULL":
        return np.ones(len(index), bool)
    a, b = CRASH[tape]
    return np.asarray(~((index >= pd.Timestamp(a)) & (index <= pd.Timestamp(b))), bool)


def spy_pack(spy):
    """Every SPY quantity the five 4b legs need, read on whatever days `spy` carries."""
    return dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                h1=halves(spy)[0], h2=halves(spy)[1],
                ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1])


def live_pack(r, turn_sum, nyrs):
    return dict(full=mets(r), oos=mets(r.loc[OOS_START:]), h1=halves(r)[0], h2=halves(r)[1],
                turn=float(turn_sum / nyrs))


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2034 (lane cloud, {DATE}) — is the 4b VERDICT a 2020 artefact once the SPY BAR "
        f"is HELD FIXED?")
    log(f"# nothing new is tuned: t {TARGETS} x [ h {[h for h in THRESH if h>0]} | R {REFRESH} ] "
        f"are ideas 1799/2022's two inherited dials.")
    log(f"# REPORTED, not tuned: BAR {BARS} (the axis under test), book tape {TAPES}, trade T "
        f"{TRADES}, panel, cost {COSTS} bps.  sigma FIXED (L={SIG_L}, d={SIG_D}).")
    log(f"# warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")
    for k, (a, b) in CRASH.items():
        log(f"#   {k}: {a} -> {b}")
    log(f"# BAR = the tape the BENCHMARK is read on, INDEPENDENT of the book's tape.")
    log(f"#   bar == book_tape  -> idea 2022's 'OWN' convention (the diagonal of the cross)")
    log(f"#   bar == FULL       -> the benchmark FROZEN against the excision")
    log(f"#   bar == ABS        -> ONE frozen vector, {ABS_PANEL}'s FULL-tape SPY / live-v2 legs,")
    log(f"#                        applied to every panel and every tape")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    # ------------------------------------------------------------- benchmarks, every panel/tape
    SPYP: dict = {}     # (panel, tape) -> spy pack
    LIVEP: dict = {}    # (panel, tape, cost) -> live pack
    excised_days = {}
    START = {}
    for pname, px, cols in PS:
        st = px.index[WARMUP]
        START[pname] = st
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        spy0 = px["SPY"].pct_change().fillna(0.0).loc[st:]
        for tape in TAPES:
            km = tape_mask(lr.index, tape)
            excised_days[(pname, tape)] = int((~km).sum())
            SPYP[(pname, tape)] = spy_pack(spy0[km])
            for c in COSTS:
                r = net(lr, lt, c)[km]
                LIVEP[(pname, tape, c)] = live_pack(r, lt[km].sum(), len(r) / 252.0)
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")
        for tape in TAPES:
            L, S = LIVEP[(pname, tape, COST0)], SPYP[(pname, tape)]
            log(f"   [{tape:10s}] LIVE v2 (W,{COST0}bps) {L['full']['CAGR']:.2%}/"
                f"{L['full']['Sharpe']:.4f}/{L['full']['MaxDD']:.2%}   "
                f"SPY {S['full']['CAGR']:.2%}/{S['full']['Sharpe']:.4f}/{S['full']['MaxDD']:.2%}"
                f" (OOS {S['oos']['CAGR']:.2%}/{S['oos']['Sharpe']:.4f}/{S['oos']['MaxDD']:.2%})"
                f"   [{excised_days[(pname, tape)]} days removed]")

    # the BAR SHIFT idea 2022 disclosed but did not remove, stated explicitly
    log("\n## THE BAR SHIFT, PANEL BY PANEL (this is what BAR=FULL / BAR=ABS freeze)")
    bar_rows = []
    for pname, _, _ in PS:
        for tape in TAPES:
            S = SPYP[(pname, tape)]
            bar_rows.append(dict(panel=pname, tape=tape, spy_MaxDD=S["full"]["MaxDD"],
                                 dd_cap=DD_CAP * S["full"]["MaxDD"],
                                 spy_CAGR=S["full"]["CAGR"],
                                 cagr_floor=CAGR_FLOOR * S["full"]["CAGR"],
                                 spy_H1=S["h1"], spy_H2=S["h2"],
                                 spy_oos_Sharpe=S["oos"]["Sharpe"],
                                 spy_oos_MaxDD=S["oos"]["MaxDD"],
                                 spy_oos_CAGR=S["oos"]["CAGR"],
                                 days_removed=excised_days[(pname, tape)]))
            log(f"   {pname:9s} [{tape:10s}] SPY MaxDD {S['full']['MaxDD']:+.2%} -> DD cap "
                f"{DD_CAP*S['full']['MaxDD']:+.2%} | SPY CAGR {S['full']['CAGR']:.2%} -> floor "
                f"{CAGR_FLOOR*S['full']['CAGR']:.2%} | H1 {S['h1']:.4f} H2 {S['h2']:.4f} "
                f"OOS {S['oos']['Sharpe']:.4f}")
    pd.DataFrame(bar_rows).to_csv(f"{OUT}.barshift.csv", index=False)
    ABS_SPY = SPYP[(ABS_PANEL, "FULL")]
    ABS_LIVE = {c: LIVEP[(ABS_PANEL, "FULL", c)] for c in COSTS}

    def bar_for(pname, bar, c):
        """The benchmark pack a cell is judged against.  Independent of the BOOK tape: that
        independence is exactly what makes the BAR effect and the BOOK effect separable."""
        if bar == "ABS":
            return ABS_SPY, ABS_LIVE[c]
        return SPYP[(pname, bar)], LIVEP[(pname, bar, c)]

    # --------------------------------------------------------------------------- the grid
    rows = []
    g1r = g1t = g2 = g3 = g4 = g9 = 0.0
    g4n = 0
    for pname, px, cols in PS:
        st = START[pname]
        bk = Book(px, cols, px.index)

        if pname in ("U56", "B136"):
            Gp = (TGT_MEMO / bk.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = (eq_weight(px, cols).mul(Gp, axis=0)).fillna(0.0)
            a, at, _, _ = bk.run_cal(bk.g_of(TGT_MEMO), "W", "W")
            b = engine_backtest(px, Wfull, cost_bps=0.0, freq="W")
            g1r = max(g1r, float(np.abs(a.values - b["returns"].values).max()))
            g1t = max(g1t, float(np.abs(at.values - b["turnover"].values).max()))
            for c in (10, 25):
                eb = engine_backtest(px, Wfull, cost_bps=float(c), freq="W")["returns"]
                g2 = max(g2, float(np.abs(net(a, at, c).values - eb.values).max()))

        for tgt in TARGETS:
            g0 = bk.g_of(tgt)
            for T in TRADES:
                cells = ([("CAL", Rc, np.nan) for Rc in REFRESH]
                         + [("DRIFT", "h", h) for h in THRESH])
                cal_ref = {}
                for fam, Rc, h in cells:
                    if fam == "CAL":
                        r0, t0, gs, nref = bk.run_cal(g0, T, Rc)
                        label = f"R={Rc}"
                        cal_ref[Rc] = (r0.copy(), t0.copy())
                    else:
                        r0, t0, gs, nref = bk.run_drift(g0, T, h)
                        label = f"h={h:.2f}"
                        if h == 0.0 and "D" in cal_ref:
                            cr, ct = cal_ref["D"]
                            g4 = max(g4, float(np.abs(r0.values - cr.values).max()),
                                     float(np.abs(t0.values - ct.values).max()))
                            g4n += 1
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    g9 = max(g9, float(gs.max()))
                    for tape in TAPES:
                        km = tape_mask(r0.index, tape)
                        rT, tT, gsT = r0[km], t0[km], gs[km]
                        yrs = len(rT) / 252.0
                        for c in COSTS:
                            r = net(rT, tT, c)
                            mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                            h1, h2 = halves(r)
                            ih1, ih2 = halves(r.loc[:IS_END])
                            base = dict(
                                panel=pname, book_tape=tape, target=tgt, T_trade=T, family=fam,
                                R_refresh=Rc, h=h, cell=label, cost=c,
                                turn_py=float(tT.sum() / yrs),
                                refresh_py=nref / (len(px) / 252.0),
                                gross_mean=float(gsT.mean()), gross_max=float(gsT.max()),
                                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                H1=h1, H2=h2,
                                is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                                is_H1=ih1, is_H2=ih2,
                                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                                oos_MaxDD=mo["MaxDD"])
                            for bar in BARS:
                                S, LV = bar_for(pname, bar, c)
                                mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
                                       "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
                                       "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
                                       "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
                                bl, nbad = binding(mar)
                                k4bf = all(mar[k] > 0 for k in LEGS)
                                k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                        and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                        and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                                k4a = (h1 > LV["h1"] and h2 > LV["h2"]
                                       and mf["MaxDD"] >= LV["full"]["MaxDD"])
                                k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"]
                                        and mo["MaxDD"] >= LV["oos"]["MaxDD"])
                                is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
                                           + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                                           + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
                                is_minleg = min(ih1 - S["ish1"], ih2 - S["ish2"],
                                                mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                                                mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
                                rows.append(dict(base, bar=bar,
                                                 **{k: float(v) for k, v in mar.items()},
                                                 bind=bl, n_fail=nbad,
                                                 is_legs=is_legs, is_minleg=float(is_minleg),
                                                 keep4b_full=k4bf, keep4b_oos=k4bo,
                                                 keep4b=(k4bf and k4bo),
                                                 keep4a=k4a, keep4a_oos=k4ao))
        log(f"   {pname}: grid done ({len([r for r in rows if r['panel']==pname])} scored rows)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    NCELL = len(G[(G.book_tape == "FULL") & (G.bar == "FULL") & (G.cost == COST0)])

    # -------------------------------------------------------------------- replication gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 bt_cal diagonal == engine.backtest (returns / turnover)",
         f"{g1r:.3e} / {g1t:.3e}", "< 1e-12", max(g1r, g1t) < 1e-12)
    gate("G2 cost identity r(c) = r0 - turn*c/1e4 == fresh engine run at 10/25 bps",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    for pn, pub in PUB_MEMO.items():
        row = G[(G.panel == pn) & (G.book_tape == "FULL") & (G.bar == "FULL")
                & (G.target == TGT_MEMO) & (G.T_trade == "W") & (G.family == "CAL")
                & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
        g3 = max(g3, max(abs(row.CAGR - pub["CAGR"]), abs(row.Sharpe - pub["Sharpe"]),
                         abs(row.MaxDD - pub["MaxDD"]), abs(row.oos_CAGR - pub["oCAGR"]),
                         abs(row.oos_Sharpe - pub["oSharpe"])))
    gate("G3 reproduces the standing VOLTGT memo (points 2-4, U56 + B136)",
         f"max|d| = {g3:.3e}", "< 1e-3", g3 < 1e-3)
    gate(f"G4 DRIFT h=0 == CALENDAR R=D, cell by cell ({g4n} cells)",
         f"{g4:.3e}", "< 1e-12", g4 < 1e-12 and g4n == len(TARGETS) * len(TRADES) * len(PS))
    gate("G5 the 420-cell corpus is rebuilt at full size", f"{NCELL} cells", "== 420",
         NCELL == 420)
    # G6: idea 2022's published census reproduced EXACTLY under its own bar convention (OWN)
    g6 = []
    for (tape, col), want in PUB_2022.items():
        got = int(G[(G.book_tape == tape) & (G.bar == tape) & (G.cost == COST0)][col].sum())
        g6.append((tape, col, got, want))
        log(f"      [{tape:10s}] bar==book  {col:12s} = {got:4d}   (idea 2022 published {want})")
    gate("G6 reproduces idea 2022's published census (4b 187 -> 80 / 89, 4a 40 -> 0 / 0)",
         ", ".join(f"{t}/{c}:{g}" for t, c, g, _ in g6), "all exact",
         all(g == w for _, _, g, w in g6))
    dd_f = SPYP[("U56", "FULL")]["full"]["MaxDD"]
    dd_p = SPYP[("U56", "CRASH_PT")]["full"]["MaxDD"]
    gate("G7 reproduces idea 2022's disclosed SPY bar shift (-33.72% -> -24.50%, U56)",
         f"{dd_f:.2%} -> {dd_p:.2%}",
         "|d| < 5e-4 each",
         abs(dd_f - PUB_BARSHIFT["spy_full_dd"]) < 5e-4
         and abs(dd_p - PUB_BARSHIFT["spy_pt_dd"]) < 5e-4)
    gate("G8 gross never levered", f"max gross {g9:.6f}", "<= 1.0 + 1e-9", g9 <= 1.0 + 1e-9)
    for tape in CRASH:
        d = {excised_days[(p, tape)] for p, _, _ in PS}
        gate(f"G9 {tape} removes a non-empty window on every panel", f"{sorted(d)} days",
             "> 0", min(d) > 0)

    # ------------------------------------------------------------------- V1: the 2x2 attribution
    log("\n## V1 — ATTRIBUTION OF THE PUBLISHED CENSUS MOVE (10 bps, 420 cells)")
    log("   book FULL / bar FULL is the published baseline; book EXC / bar EXC is idea 2022's")
    log("   published excised census.  The two off-diagonal cells isolate each effect.")
    C = G[G.cost == COST0]

    def N(book, bar, col="keep4b_full"):
        return int(C[(C.book_tape == book) & (C.bar == bar)][col].sum())

    v1 = []
    for col in ("keep4b_full", "keep4b_oos", "keep4b", "keep4a", "keep4a_oos"):
        base = N("FULL", "FULL", col)
        for tape in CRASH:
            tot = N(tape, tape, col) - base
            bar_e = N("FULL", tape, col) - base          # book untouched, bar moved
            book_e = N(tape, "FULL", col) - base         # bar frozen, book moved
            inter = tot - bar_e - book_e
            abs_e = N(tape, "ABS", col) - N("FULL", "ABS", col)
            v1.append(dict(metric=col, crash=tape, n_cells=NCELL, base=base,
                           excised_own=N(tape, tape, col), total=tot,
                           bar_only=N("FULL", tape, col), bar_effect=bar_e,
                           book_only=N(tape, "FULL", col), book_effect=book_e,
                           interaction=inter, abs_bar_effect=abs_e,
                           bar_share=(abs(bar_e) / (abs(bar_e) + abs(book_e))
                                      if (abs(bar_e) + abs(book_e)) else np.nan)))
            log(f"   {col:12s} [{tape:10s}]  {base:3d} -> {N(tape, tape, col):3d}  "
                f"(total {tot:+4d})  =  BAR {bar_e:+4d}  +  BOOK {book_e:+4d}  +  "
                f"INTERACTION {inter:+4d}   | bar share of |effect| "
                f"{(abs(bar_e)/(abs(bar_e)+abs(book_e)) if (abs(bar_e)+abs(book_e)) else float('nan')):.1%}")
    V1 = pd.DataFrame(v1)
    V1.to_csv(f"{OUT}.attribution.csv", index=False)

    hd = V1[(V1.metric == "keep4b_full")].set_index("crash")
    bar_pt, book_pt = hd.loc["CRASH_PT", "bar_effect"], hd.loc["CRASH_PT", "book_effect"]
    if abs(bar_pt) >= 2 * abs(book_pt):
        v1_verdict = "BENCHMARK-ARTEFACT"
    elif abs(book_pt) >= 2 * abs(bar_pt):
        v1_verdict = "BOOK-FAILURE"
    else:
        v1_verdict = "MIXED"
    log(f"   V1 VERDICT: {v1_verdict}   (CRASH_PT keep4b_full: BAR {bar_pt:+d} vs BOOK {book_pt:+d})")

    # the same attribution at every cost rung, reported not tuned
    log("\n   cost ladder (keep4b_full, CRASH_PT):")
    crows = []
    for c in COSTS:
        Cc = G[G.cost == c]

        def Nc(book, bar):
            return int(Cc[(Cc.book_tape == book) & (Cc.bar == bar)].keep4b_full.sum())
        b0 = Nc("FULL", "FULL")
        crows.append(dict(cost=c, base=b0, excised_own=Nc("CRASH_PT", "CRASH_PT"),
                          bar_only=Nc("FULL", "CRASH_PT"), book_only=Nc("CRASH_PT", "FULL"),
                          bar_effect=Nc("FULL", "CRASH_PT") - b0,
                          book_effect=Nc("CRASH_PT", "FULL") - b0))
        log(f"      {c:2d} bps: {b0:3d} -> {Nc('CRASH_PT','CRASH_PT'):3d}   BAR "
            f"{Nc('FULL','CRASH_PT')-b0:+4d}   BOOK {Nc('CRASH_PT','FULL')-b0:+4d}")
    pd.DataFrame(crows).to_csv(f"{OUT}.costladder.csv", index=False)

    # ------------------------------------------------------------------- V2: leg attribution
    log("\n## V2 — WHICH OF THE FIVE 4b LEGS FLIPS, AND UNDER WHICH EFFECT? (10 bps)")
    KEY = ["panel", "target", "T_trade", "family", "R_refresh", "h", "cell"]
    v2 = []
    for tape in CRASH:
        A = C[(C.book_tape == "FULL") & (C.bar == "FULL")].set_index(KEY).sort_index()
        BARONLY = C[(C.book_tape == "FULL") & (C.bar == tape)].set_index(KEY).sort_index()
        BOOKONLY = C[(C.book_tape == tape) & (C.bar == "FULL")].set_index(KEY).sort_index()
        BOTH = C[(C.book_tape == tape) & (C.bar == tape)].set_index(KEY).sort_index()
        for leg in LEGS:
            pa = (A[leg] > 0)
            f_bar = int((pa & ~(BARONLY[leg] > 0)).sum())
            f_book = int((pa & ~(BOOKONLY[leg] > 0)).sum())
            f_both = int((pa & ~(BOTH[leg] > 0)).sum())
            v2.append(dict(crash=tape, leg=leg, pass_base=int(pa.sum()),
                           lost_bar_only=f_bar, lost_book_only=f_book, lost_both=f_both,
                           mean_d_bar=float((BARONLY[leg] - A[leg]).mean()),
                           mean_d_book=float((BOOKONLY[leg] - A[leg]).mean())))
            log(f"   [{tape:10s}] {leg:8s} passing at base {int(pa.sum()):3d} -> lost by BAR "
                f"alone {f_bar:3d}, by BOOK alone {f_book:3d}, by both {f_both:3d}   "
                f"(mean margin move: bar {float((BARONLY[leg]-A[leg]).mean()):+.4f}, "
                f"book {float((BOOKONLY[leg]-A[leg]).mean()):+.4f})")
    pd.DataFrame(v2).to_csv(f"{OUT}.legs.csv", index=False)

    # ------------------------------------------------------- V3: survival with the bar frozen
    log("\n## V3 — DO THE 187 PUBLISHED 4b PASSES SURVIVE THE EXCISION WITH THE BAR FROZEN?")
    A = C[(C.book_tape == "FULL") & (C.bar == "FULL")].set_index(KEY).sort_index()
    passers = A.index[A.keep4b_full.values]
    v3 = []
    for tape in CRASH:
        for bar in ["FULL", "ABS", tape]:
            Z = C[(C.book_tape == tape) & (C.bar == bar)].set_index(KEY).sort_index()
            surv = int(Z.loc[passers, "keep4b_full"].sum())
            v3.append(dict(crash=tape, bar=("OWN(" + tape + ")" if bar == tape else bar),
                           base=len(passers), survivors=surv, share=surv / len(passers)))
            log(f"   [{tape:10s}] bar={('OWN' if bar == tape else bar):4s}: "
                f"{surv:3d} of {len(passers)} published passes survive ({surv/len(passers):.1%})")
    pd.DataFrame(v3).to_csv(f"{OUT}.survival.csv", index=False)

    log("\n   THE STANDING KEEP-4b CANDIDATE (VOLTGT t=0.10, T=M, R=M), cell by cell:")
    srows = []
    for pn, _, _ in PS:
        for tape in TAPES:
            for bar in BARS:
                q = C[(C.panel == pn) & (C.book_tape == tape) & (C.bar == bar)
                      & (C.target == STANDING["target"]) & (C.T_trade == STANDING["T_trade"])
                      & (C.cell == STANDING["cell"])]
                if not len(q):
                    continue
                r = q.iloc[0]
                srows.append(dict(panel=pn, book_tape=tape, bar=bar, CAGR=r.CAGR,
                                  Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                                  oos_CAGR=r.oos_CAGR, oos_Sharpe=r.oos_Sharpe,
                                  oos_MaxDD=r.oos_MaxDD, bind=r.bind,
                                  keep4b_full=bool(r.keep4b_full), keep4b_oos=bool(r.keep4b_oos),
                                  keep4a=bool(r.keep4a),
                                  **{k: float(r[k]) for k in LEGS}))
                if pn in ("U56", "B136"):
                    log(f"      {pn:9s} book={tape:10s} bar={bar:10s}  "
                        f"4b_full={str(bool(r.keep4b_full)):5s} 4b_oos={str(bool(r.keep4b_oos)):5s}"
                        f" 4a={str(bool(r.keep4a)):5s}  bind={r.bind:20s} "
                        f"CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:.2%}")
    pd.DataFrame(srows).to_csv(f"{OUT}.standing.csv", index=False)

    # --------------------------------------------------------------------------- V4: rule 8
    log("\n## V4 — RULE 8 WALK-FORWARD (parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE)")
    log("   choosers: CH_ISSHARPE = argmax IS Sharpe; CH_ISMINLEG = argmax min IS 4b-leg slack.")
    wrows = []
    for (pn, tape, bar, T, fam), sub in C.groupby(
            ["panel", "book_tape", "bar", "T_trade", "family"]):
        S, LV = bar_for(pn, bar, COST0)
        for ch, col in (("CH_ISSHARPE", "is_Sharpe"), ("CH_ISMINLEG", "is_minleg")):
            pick = sub.loc[sub[col].idxmax()]
            wrows.append(dict(panel=pn, book_tape=tape, bar=bar, T_trade=T, family=fam,
                              chooser=ch, target=pick.target, cell=pick.cell,
                              is_stat=float(pick[col]),
                              oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                              oos_MaxDD=pick.oos_MaxDD,
                              spy_oos_CAGR=S["oos"]["CAGR"], spy_oos_Sharpe=S["oos"]["Sharpe"],
                              spy_oos_MaxDD=S["oos"]["MaxDD"],
                              live_oos_CAGR=LV["oos"]["CAGR"],
                              live_oos_Sharpe=LV["oos"]["Sharpe"],
                              live_oos_MaxDD=LV["oos"]["MaxDD"],
                              keep4b_full=bool(pick.keep4b_full),
                              keep4b_oos=bool(pick.keep4b_oos),
                              keep4b=bool(pick.keep4b), keep4a=bool(pick.keep4a),
                              keep4a_oos=bool(pick.keep4a_oos),
                              is_the_standing_cell=bool(
                                  pick.target == STANDING["target"] and T == STANDING["T_trade"]
                                  and pick.cell == STANDING["cell"])))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    log(f"   {len(W)} picks (panel x book tape x bar x trade cadence x family x chooser)")
    for (tape, bar), s in W.groupby(["book_tape", "bar"]):
        log(f"      book={tape:10s} bar={bar:10s}: 4b FULL {int(s.keep4b_full.sum()):2d}/{len(s)}"
            f"  4b OOS {int(s.keep4b_oos.sum()):2d}/{len(s)}  4b BOTH {int(s.keep4b.sum()):2d}"
            f"/{len(s)}  4a {int(s.keep4a.sum()):2d}/{len(s)}  4a OOS "
            f"{int(s.keep4a_oos.sum()):2d}/{len(s)}  reaches the standing cell "
            f"{int(s.is_the_standing_cell.sum()):2d}/{len(s)}")
    log("\n   every pick that clears 4b FULL *and* OOS (the KEEP-4b test), in full:")
    K = W[W.keep4b]
    if len(K) == 0:
        log("      (none)")
    for _, r in K.iterrows():
        log(f"      {r.panel:9s} book={r.book_tape:10s} bar={r['bar']:10s} T={r.T_trade} "
            f"{r.family:5s} {r.chooser:11s} -> t={r.target:.2f} {r.cell:7s}  OOS "
            f"{r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / {r.oos_MaxDD:7.2%}   vs SPY "
            f"{r.spy_oos_CAGR:7.2%} / {r.spy_oos_Sharpe:.4f} / {r.spy_oos_MaxDD:7.2%}   vs LIVE v2 "
            f"{r.live_oos_CAGR:7.2%} / {r.live_oos_Sharpe:.4f} / {r.live_oos_MaxDD:7.2%}")

    # headline capital table on the FULL tape (the tape real capital would be deployed on)
    log("\n## HEADLINE CAPITAL TABLE — FULL TAPE, 10 bps (the tape capital is deployed on)")
    for pn, _, _ in PS:
        S, LV = bar_for(pn, "FULL", COST0)
        q = C[(C.panel == pn) & (C.book_tape == "FULL") & (C.bar == "FULL")
              & (C.target == STANDING["target"]) & (C.T_trade == STANDING["T_trade"])
              & (C.cell == STANDING["cell"])]
        if not len(q):
            continue
        r = q.iloc[0]
        log(f"   {pn:9s} STANDING  full {r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  "
            f"(H1 {r.H1:.4f} H2 {r.H2:.4f})  OOS {r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / "
            f"{r.oos_MaxDD:7.2%}")
        log(f"   {'':9s} SPY       full {S['full']['CAGR']:7.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:7.2%}  (H1 {S['h1']:.4f} H2 {S['h2']:.4f})  OOS "
            f"{S['oos']['CAGR']:7.2%} / {S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:7.2%}")
        log(f"   {'':9s} LIVE v2   full {LV['full']['CAGR']:7.2%} / {LV['full']['Sharpe']:.4f} / "
            f"{LV['full']['MaxDD']:7.2%}  (H1 {LV['h1']:.4f} H2 {LV['h2']:.4f})  OOS "
            f"{LV['oos']['CAGR']:7.2%} / {LV['oos']['Sharpe']:.4f} / {LV['oos']['MaxDD']:7.2%}")

    log("\n## VERDICT")
    log(f"   V1 {v1_verdict}")
    log(f"   gates: {sum(g['pass_'] for g in _gates)}/{len(_gates)} pass")
    log("   SURVIVORSHIP: U56 / B136 are CURRENT constituents and SMALL is a CURRENT sub-$2B")
    log("   screen, so every LEVEL is optimistic and both 4b bars are easier than on a")
    log("   point-in-time panel.  The BAR-vs-BOOK contrast is same-tape / same-names / same-grid")
    log("   with only the SCORING convention moved, so it is first-order immune; the PASS COUNTS")
    log("   are not.")

    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)


if __name__ == "__main__":
    main()

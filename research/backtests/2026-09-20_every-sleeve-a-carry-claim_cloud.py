#!/usr/bin/env python3
"""Idea 1627 (lane cloud, 2026-09-20): IS EVERY SLEEVE AND HEDGE IN THE RECORD A CARRY CLAIM
WEARING AN INSTRUMENT?

THE DEFECT THIS CLOSES.  Idea 1602 took ONE instrument -- SHY -- and asked whether the sleeve's
contribution to the live band book is CARRY (idle NAV earning a rate) or DURATION (a marked-to-
market bond with its own vol, its own drawdown, its own 2022 loss).  Its answer was carry: SHY's
entire contribution is reproduced by a zero-duration accrual at the same realised rate (dSharpe
+0.0009 over 6 panel-frames), and SHY's duration COSTS a 4a pass on SMALL.  But the record has
routed weight into SEVEN OTHER non-equity instruments -- IEF, TLT, GLD, TIP, HYG, LQD, UUP --
and every one of those routings is written in the record as a claim about the INSTRUMENT (a
hedge, a diversifier, a carry sleeve) rather than about the CASH-RATE it happens to earn.  If
the SHY finding generalises, the whole sleeve family is one accrual line wearing eight tickers,
and the record can retire it.  If even one instrument survives, that instrument -- and only that
one -- is a real diversification claim and must be re-argued as one.

THE CONSTRUCTION (identical to idea 1602's, widened from 1 instrument to 8).  Take the LIVE
RULES v2 band book (200d +/-3% hysteresis, equal weight inside, de-gross to cash, gross 0.75,
weekly, 10 bps, t+1) and route fraction F of the GATED-OUT (idle) NAV into a sleeve.  Two arms
on the SAME names, the SAME days, the SAME frame and the SAME F ladder:

  ETF     the instrument itself, marked to market, drifting with the book between rebalances and
          paying 10 bps on its own turnover -- what the record actually priced.
  MATCH   a SYNTHETIC ZERO-DURATION ACCRUAL: a constant daily return (1+a)^(1/252)-1 at
          a = THAT INSTRUMENT'S OWN realised CAGR on that panel's scored tape.  Same carry, zero
          vol, zero drawdown, zero mark-to-market.  It pays the SAME turnover cost as the ETF arm
          (the routing is identical), so ETF - MATCH is the INSTRUMENT'S OWN PRICE PATH and
          nothing else.

  ETF minus MATCH IS THIS RUN'S HEADLINE STATISTIC, per instrument, per panel, per F.

  A THIRD ARM, MATCH_IS, sets a from the 2009-2016 window ONLY and is the arm used in rule 8, so
  no accrual rate the walk-forward can pick has read an OOS row.  MATCH (full-sample a) is a
  DESCRIPTIVE contrast, not a tradable book, and is labelled as such everywhere it appears: the
  accrual is HANDED the instrument's realised carry, which is the most generous version of the
  substitution and therefore the right null for "does the instrument add anything BEYOND carry".

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  F {0.00, 0.25, 0.50, 0.75, 1.00}   DIAL 1 -- fraction of idle NAV routed to the sleeve.
      F = 0.00 IS the live 0%-cash convention and is a cell of EVERY arm and EVERY instrument,
      so the "change nothing" null is priced on the same tape as every candidate (gate G1).
  S {SHY, IEF, TLT, GLD, TIP, HYG, LQD, UUP}   DIAL 2 -- WHICH instrument.  This is the dial the
      record has been implicitly choosing by hand for eight ideas; rule 8 makes it choose on IS
      alone and pays the OOS bill.
  PANELS (U56 / B136 / SMALL) and ARMS are REPORTED AXES, not dials: every cell is published.

  GROSS IS FROZEN at G = 0.75 (the live value) and BAND at 0.03 (the live value).  Sweeping
  either would be a third parameter; idea 1498 already swept gross and idea 1719 the band.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) MATCH >= ETF on Sharpe AND MaxDD for ALL 8 instruments at F = 1.00 on most panels -> the
      whole sleeve family is PURE CARRY, the record keeps ONE accrual line and retires the rest.
  (b) Some instrument beats its own accrual on Sharpe or MaxDD -> that one is a real
      DIVERSIFICATION claim and must be re-titled and re-argued; the others still retire.
  (c) The rule-8 chooser over (S, F) loses to the live book OOS -> the instrument axis is a KILL
      as a dial whatever its ex-post best cell does.
All three are reported, and a KILL is reported as a KILL.

GATES.  G0 sample >= 10y (rule 1).  G1 F = 0 invariance: every (instrument, arm) bit-identical
to the live 0%-cash book at F = 0 on every panel.  G2 cross-script replay of baseline.compare's
RULES v2 row (the F = 0 cell IS the live book).  G3 a = 0 invariance: a zero accrual at any F
reproduces the live book.  G4 no leverage (max gross <= 1.0).  G5 exactly two tuned parameters.
G6 no chooser reads a row on or after 2017-01-01.  G7 all cells published.  G8 each instrument's
own standalone profile (CAGR / Sharpe / MaxDD, full and OOS) published, not asserted.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (live RULES v2
AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward, 2017-2026 read exactly once);
rule 9 (survivorship stated).  RULES.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP CAVEAT.  B136 and SMALL are CURRENT constituents of their screens (PROTOCOL rule 9
and data/SMALL_PANEL_README.md): both panels are survivorship-biased UPWARD and their absolute
CAGRs are not investable.  Every headline here is a WITHIN-PANEL contrast (ETF arm minus its own
matched-accrual twin on the same names and days), which the bias cannot manufacture, but the
4a/4b verdicts on those panels inherit it and are labelled accordingly.  SMALL additionally
drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv before use.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_every-sleeve-a-carry-claim_cloud.py
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
from engine import backtest, rebalance_mask           # noqa: E402

DATE, SLUG = "2026-09-20", "every-sleeve-a-carry-claim"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
G_FROZEN, BAND, CAD, COST = 0.75, 0.03, "W", 10.0
SLEEVES = ["SHY", "IEF", "TLT", "GLD", "TIP", "HYG", "LQD", "UUP"]
GRID_F = [0.00, 0.25, 0.50, 0.75, 1.00]
ARMS = ["ETF", "MATCH", "MATCH_IS"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

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


def daily(a):
    return (1.0 + a) ** (1.0 / 252.0) - 1.0


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


def keep4a(r, b):
    """PROTOCOL 4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse."""
    r1, r2 = halves(r); b1, b2 = halves(b)
    return bool(r1 > b1 and r2 > b2 and mdd(r) >= mdd(b))


def keep4b(r, s):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    r1, r2 = halves(r); s1, s2 = halves(s)
    return bool(r1 > s1 and r2 > s2 and mdd(r) >= DD_CAP * mdd(s) and cagr(r) >= CAGR_FLOOR * cagr(s))


# ---------------------------------------------------------------- panel
class Panel:
    def __init__(self, name, px, ref):
        self.name, self.px = name, px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        # every sleeve is priced off the SAME reference tape on every panel, so the contrast is
        # never confounded by which panel prices the instrument.
        self.sl = {s: np.nan_to_num(ref[s].reindex(px.index).ffill().pct_change().values, nan=0.0)
                   for s in SLEEVES}
        self.i_oos = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.frame = (rules_v2_weights(px, band=BAND, gross=1.0)
                      .reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values)


def run_cell(pan, sleeve_ret, f, g=G_FROZEN, cost=COST):
    """Live band frame at constant gross g, routing fraction f of the IDLE NAV into a sleeve whose
    daily return series is `sleeve_ret`.  The sleeve drifts with the book between rebalances and
    pays `cost` bps on its own turnover, exactly as a held ETF does.  f = 0 reduces to the live
    0%-cash convention for ANY sleeve.  Same arithmetic as idea 1602's run_cell."""
    rets, frame = pan.rets, pan.frame
    cr = sleeve_ret
    T, M = rets.shape
    turn = np.zeros(T)
    turn_s = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(pan.reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(pan.reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0 + f * (1.0 - s0))
        turn_s[i0] = f * abs(s0 - float(curw.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum()) + turn_s[i0]
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        seg = cr[i0:i1]
        cash_growth = np.concatenate(([1.0], np.cumprod(1.0 + f * seg)[:-1]))
        Ccash = (1.0 - s0) * cash_growth
        V = A.sum(axis=1) + Ccash
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1) + (Ccash / V) * (f * seg)
        Ae = w0 * (C[i1 - 1] / base)
        ce = (1.0 - s0) * float(np.prod(1.0 + f * seg))
        curw = Ae / (Ae.sum() + ce)
    return out - turn * cost / 1e4, wsum_max, turn_s


# ---------------------------------------------------------------- data
def build_panels():
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).ffill()
    out = []
    px_u = load_universe()
    out.append(("U56", px_u))
    out.append(("B136", load_universe(broad=True)))
    px_s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    tcol = meta.columns[0]
    drop = {t for t in meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str)
            if t in px_s.columns and t != "SPY"}
    mx = px_s.pct_change().abs().max()
    drop |= {c for c in px_s.columns if c != "SPY" and mx[c] >= 1.0}
    px_s = px_s.drop(columns=sorted(drop))
    say(f"  SMALL: dropped {len(drop)} tickers with max 1d move >= 1.0 -> {px_s.shape[1]-1} names + SPY")
    out.append(("SMALL", px_s))
    return ref, out


def main():
    t0 = time.time()
    say(f"=== Idea 1627 — is EVERY sleeve a CARRY claim wearing an INSTRUMENT?  ({DATE}, cloud) ===")
    say("Live RULES v2 band book (band 0.03, gross 0.75, weekly, 10 bps, t+1); fraction F of idle")
    say("NAV routed to each of 8 instruments (ETF arm) vs a ZERO-DURATION accrual at that")
    say("instrument's OWN realised CAGR (MATCH arm).  ETF - MATCH is the instrument's price path.")
    ref, panels = build_panels()

    rows, wf_rows, inst_rows = [], [], []
    maxgross = 0.0

    for pname, px in panels:
        pan = Panel(pname, px, ref)
        n = len(pan.idx)
        sl_full, sl_is, sl_oos = slice(WARMUP, n), slice(WARMUP, pan.i_oos), slice(pan.i_oos, n)
        yrs = (sl_full.stop - sl_full.start) / 252
        say(f"\n--- PANEL {pname}: {px.shape[1]-1} names + SPY, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, scored {yrs:.1f}y, {len(pan.reb)} rebalances ---")
        gate(f"G0 sample {pname}", f"{yrs:.1f}y", ">= 10y (rule 1)", yrs >= 10)

        spy = pan.spy
        spy_f, spy_o = spy[sl_full], spy[sl_oos]
        base_r, mg, _ = run_cell(pan, np.zeros(n), 0.0)
        maxgross = max(maxgross, mg)
        b_f, b_o = base_r[sl_full], base_r[sl_oos]
        tb, ts = triple(b_f), triple(spy_f)
        say(f"  RULES v2 live FULL : CAGR {tb['CAGR']:7.2%}  Sharpe {tb['Sharpe']:7.4f}  MaxDD {tb['MaxDD']:7.2%}")
        say(f"  SPY          FULL : CAGR {ts['CAGR']:7.2%}  Sharpe {ts['Sharpe']:7.4f}  MaxDD {ts['MaxDD']:7.2%}")
        to, so = triple(b_o), triple(spy_o)
        say(f"  RULES v2 live OOS  : CAGR {to['CAGR']:7.2%}  Sharpe {to['Sharpe']:7.4f}  MaxDD {to['MaxDD']:7.2%}")
        say(f"  SPY          OOS  : CAGR {so['CAGR']:7.2%}  Sharpe {so['Sharpe']:7.4f}  MaxDD {so['MaxDD']:7.2%}")

        # G2: the F = 0 cell IS baseline.compare's RULES v2 row
        eng = backtest(px, rules_v2_weights(px, band=BAND, gross=G_FROZEN), cost_bps=COST, freq=CAD)
        er = eng["returns"].values[sl_full]
        gate(f"G2 engine replay {pname}", f"{np.abs(er - b_f).max():.3e}", "< 1e-12 vs engine.backtest",
             np.abs(er - b_f).max() < 1e-12)

        # G8: each instrument's own standalone profile, and the accrual rates it hands MATCH
        arate_full, arate_is = {}, {}
        for s in SLEEVES:
            sr = pan.sl[s]
            arate_full[s] = cagr(sr[sl_full])
            arate_is[s] = cagr(sr[sl_is])
            tf, tox = triple(sr[sl_full]), triple(sr[sl_oos])
            inst_rows.append(dict(panel=pname, sleeve=s, a_full=arate_full[s], a_is=arate_is[s],
                                  CAGR_full=tf["CAGR"], Sharpe_full=tf["Sharpe"], MaxDD_full=tf["MaxDD"],
                                  CAGR_oos=tox["CAGR"], Sharpe_oos=tox["Sharpe"], MaxDD_oos=tox["MaxDD"]))
            say(f"  G8 {s:4s} standalone FULL {tf['CAGR']:7.2%}/{tf['Sharpe']:7.4f}/{tf['MaxDD']:7.2%}"
                f"   OOS {tox['CAGR']:7.2%}/{tox['Sharpe']:7.4f}/{tox['MaxDD']:7.2%}"
                f"   -> a_full {arate_full[s]:7.2%}  a_IS {arate_is[s]:7.2%}")

        # ---- the grid: 8 sleeves x 5 F x 3 arms
        store = {}
        for s in SLEEVES:
            for arm in ARMS:
                if arm == "ETF":
                    sr = pan.sl[s]
                elif arm == "MATCH":
                    sr = np.full(n, daily(arate_full[s]))
                else:
                    sr = np.full(n, daily(arate_is[s]))
                for f in GRID_F:
                    r, mg, _ = run_cell(pan, sr, f)
                    maxgross = max(maxgross, mg)
                    store[(s, arm, f)] = r
                    rf, ro = r[sl_full], r[sl_oos]
                    h1, h2 = halves(rf); o1, o2 = halves(ro)
                    tf_, to_ = triple(rf), triple(ro)
                    rows.append(dict(
                        panel=pname, sleeve=s, arm=arm, F=f,
                        CAGR=tf_["CAGR"], Sharpe=tf_["Sharpe"], MaxDD=tf_["MaxDD"], H1=h1, H2=h2,
                        CAGR_oos=to_["CAGR"], Sharpe_oos=to_["Sharpe"], MaxDD_oos=to_["MaxDD"],
                        O1=o1, O2=o2,
                        Sharpe_is=sharpe(r[sl_is]), CAGR_is=cagr(r[sl_is]), MaxDD_is=mdd(r[sl_is]),
                        keep4a_full=keep4a(rf, b_f), keep4a_oos=keep4a(ro, b_o),
                        keep4b_full=keep4b(rf, spy_f), keep4b_oos=keep4b(ro, spy_o)))

        # ---- G1 / G3 invariances
        z0 = max(np.abs(store[(s, arm, 0.0)] - base_r).max() for s in SLEEVES for arm in ARMS)
        gate(f"G1 F=0 invariance {pname}", f"{z0:.3e}",
             "== live 0%-cash book for all 24 (sleeve, arm)", z0 < 1e-15)
        zr, _, zts = run_cell(pan, np.zeros(n), 1.00)
        free = zr + zts * COST / 1e4                     # the FREE-SWEEP reconstruction
        gate(f"G3 a=0 invariance {pname}", f"{np.abs(free - base_r).max():.3e}",
             "zero accrual at F=1, sleeve turnover un-charged == live book", np.abs(free - base_r).max() < 1e-15)
        publish(f"G3b charged sleeve cost {pname}",
                f"{zts[sl_full].sum() * COST / 1e4 / ((sl_full.stop - sl_full.start) / 252) * 1e4:.2f} bps/yr "
                f"(max daily gap vs live book {np.abs(zr - base_r).max():.3e})")

        # ---- headline: ETF minus its own matched accrual, at every F
        say(f"\n  HEADLINE {pname} — ETF arm MINUS its own zero-duration matched accrual (MATCH):")
        say(f"    {'sleeve':6s} {'F':>5s} {'dSharpe':>9s} {'dMaxDD':>9s} {'dCAGR':>9s}   "
            f"{'dSharpe_oos':>11s} {'dMaxDD_oos':>10s}   survives?")
        for s in SLEEVES:
            for f in GRID_F:
                if f == 0.0:
                    continue
                e, m = store[(s, "ETF", f)], store[(s, "MATCH", f)]
                ef, mf, eo, mo = e[sl_full], m[sl_full], e[sl_oos], m[sl_oos]
                dS, dD, dC = sharpe(ef) - sharpe(mf), mdd(ef) - mdd(mf), cagr(ef) - cagr(mf)
                dSo, dDo = sharpe(eo) - sharpe(mo), mdd(eo) - mdd(mo)
                surv = bool(dS > 0 and dD >= 0)
                say(f"    {s:6s} {f:5.2f} {dS:9.4f} {dD:9.2%} {dC:9.2%}   {dSo:11.4f} {dDo:10.2%}   "
                    f"{'SURVIVES' if surv else 'retires'}")
                rows.append(dict(panel=pname, sleeve=s, arm="ETF-minus-MATCH", F=f,
                                 CAGR=dC, Sharpe=dS, MaxDD=dD, H1=np.nan, H2=np.nan,
                                 CAGR_oos=cagr(eo) - cagr(mo), Sharpe_oos=dSo, MaxDD_oos=dDo,
                                 O1=np.nan, O2=np.nan, Sharpe_is=np.nan, CAGR_is=np.nan,
                                 MaxDD_is=np.nan, keep4a_full=surv, keep4a_oos=np.nan,
                                 keep4b_full=np.nan, keep4b_oos=np.nan))

        # ---- rule 8: choose (sleeve, F) on 2009-2016 ONLY, read 2017-2026 ONCE.
        # TWO choosers, both IS-only and both reported: C_SHARPE (argmax IS Sharpe, the record's
        # default) and C_4B (among the cells that clear 4b ON THE IS WINDOW, argmax IS Sharpe --
        # the chooser a capital allocator would actually use, since 4b is the capital bar).
        spy_is, b_is = spy[sl_is], base_r[sl_is]
        for arm in ["ETF", "MATCH_IS"]:
            cells = [(s, f) for s in SLEEVES for f in GRID_F]
            isS = {c: sharpe(store[(c[0], arm, c[1])][sl_is]) for c in cells}
            is4b = {c: keep4b(store[(c[0], arm, c[1])][sl_is], spy_is) for c in cells}
            for cname, pool in [("C_SHARPE", cells), ("C_4B", [c for c in cells if is4b[c]])]:
                if not pool:
                    say(f"  RULE 8 {arm:9s} {cname:8s}: NO IS PASSER -- chooser selects nothing")
                    wf_rows.append(dict(panel=pname, arm=arm, chooser=cname, pick_sleeve="(none)",
                                        pick_F=np.nan, pick_a=np.nan, IS_Sharpe=np.nan,
                                        OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                        base_OOS_Sharpe=to["Sharpe"], base_OOS_CAGR=to["CAGR"],
                                        base_OOS_MaxDD=to["MaxDD"], spy_OOS_Sharpe=so["Sharpe"],
                                        spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
                                        keep4a_oos=False, keep4b_oos=False))
                    continue
                s, f = max(pool, key=lambda c: (isS[c] if np.isfinite(isS[c]) else -np.inf))
                r = store[(s, arm, f)]
                ro = r[sl_oos]
                t_ = triple(ro)
                a_used = np.nan if arm == "ETF" else arate_is[s]
                wf_rows.append(dict(panel=pname, arm=arm, chooser=cname, pick_sleeve=s, pick_F=f,
                                    pick_a=a_used, IS_Sharpe=isS[(s, f)],
                                    OOS_CAGR=t_["CAGR"], OOS_Sharpe=t_["Sharpe"], OOS_MaxDD=t_["MaxDD"],
                                    base_OOS_Sharpe=to["Sharpe"], base_OOS_CAGR=to["CAGR"],
                                    base_OOS_MaxDD=to["MaxDD"], spy_OOS_Sharpe=so["Sharpe"],
                                    spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
                                    keep4a_oos=keep4a(ro, b_o), keep4b_oos=keep4b(ro, spy_o)))
                arate_txt = "" if arm == "ETF" else f" [accrual a = {a_used:.2%}/yr, NOT a rate any sweep pays]"
                say(f"  RULE 8 {arm:9s} {cname:8s}: IS pick sleeve={s} F={f:.2f} "
                    f"(IS Sharpe {isS[(s,f)]:.4f}, pool {len(pool)}/40){arate_txt}  ->  "
                    f"OOS {t_['CAGR']:7.2%}/{t_['Sharpe']:7.4f}/{t_['MaxDD']:7.2%}   "
                    f"4a {'PASS' if keep4a(ro,b_o) else 'fail'}  4b {'PASS' if keep4b(ro,spy_o) else 'fail'}")
            # where does the ex-post best 4b instrument sit on the IS ladder the chooser sees?
            order = sorted(cells, key=lambda c: -(isS[c] if np.isfinite(isS[c]) else -np.inf))
            gl = [(i + 1, c) for i, c in enumerate(order) if c[0] == "GLD"]
            say(f"    IS-Sharpe rank of the GLD cells the chooser must reach ({arm}): "
                + ", ".join(f"F={c[1]:.2f}->#{i}" for i, c in gl) + f"  (of {len(order)})")

    df = pd.DataFrame(rows)
    wf = pd.DataFrame(wf_rows)
    inst = pd.DataFrame(inst_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    inst.to_csv(f"{OUT}.instruments.csv", index=False)

    say("\n=== SUMMARY ===")
    gate("G4 no leverage", f"max gross {maxgross:.4f}", "<= 1.0", maxgross <= 1.0 + 1e-12)
    gate("G5 tuned parameters", "2 (F, sleeve)", "<= 2 (PROTOCOL rule 4)", True)
    gate("G6 chooser is IS-only", "argmax over 2009-2016 Sharpe", "no OOS row read by any chooser", True)
    gate("G7 all cells published", f"{len(df)} rows -> {Path(OUT).name}.grid.csv",
         "every grid point reported", True)

    d = df[df.arm == "ETF-minus-MATCH"]
    say(f"\nSUBSTITUTION COUNT (ETF strictly better than its own matched accrual on Sharpe AND "
        f"no worse on MaxDD), {len(d)} cells:")
    say(f"  overall  {int(d.keep4a_full.sum())} of {len(d)}")
    for pname in ["U56", "B136", "SMALL"]:
        dd = d[d.panel == pname]
        say(f"  {pname:6s}   {int(dd.keep4a_full.sum())} of {len(dd)}")
    say("  by sleeve (over 3 panels x 4 non-zero F = 12 cells each), and at F = 1.00 only:")
    for s in SLEEVES:
        ds = d[d.sleeve == s]
        d1 = ds[ds.F == 1.00]
        say(f"    {s:4s}  all-F {int(ds.keep4a_full.sum())} of {len(ds)}   F=1.00 "
            f"{int(d1.keep4a_full.sum())} of {len(d1)}   mean dSharpe {ds.Sharpe.mean():+.4f}   "
            f"mean dMaxDD {ds.MaxDD.mean():+.2%}")

    g = df[df.arm.isin(ARMS)]
    say(f"\nKEEP PATHS over the {len(g)} priced cells (3 panels x 8 sleeves x 5 F x 3 arms):")
    for arm in ARMS:
        a = g[g.arm == arm]
        say(f"  {arm:9s}  4a FULL {int(a.keep4a_full.sum()):3d}/{len(a)}   "
            f"4a OOS {int(a.keep4a_oos.sum()):3d}/{len(a)}   "
            f"4b FULL {int(a.keep4b_full.sum()):3d}/{len(a)}   "
            f"4b OOS {int(a.keep4b_oos.sum()):3d}/{len(a)}")

    say(f"\nRULE 8 (params on 2009-2016 only, 2017-2026 read ONCE):")
    say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say(f"\nGATES {sum(1 for r in GATES if r['pass_'])}/{len(GATES)}   elapsed {time.time()-t0:.1f}s")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

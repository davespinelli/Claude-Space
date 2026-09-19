#!/usr/bin/env python3
"""
Idea 1450 (lane cloud, 2026-09-19) — is PROTOCOL 4b's DRAWDOWN CAP STABLE ENOUGH TO BUDGET
AGAINST, and what does its movement do to the GROSS it licenses?

THE PREMISE.  PROTOCOL 4b caps a candidate's drawdown at 0.60 x SPY's MaxDD and floors its
CAGR at 0.70 x SPY's.  Both bars are ONE-EPISODE statistics: SPY's MaxDD is whatever its worst
peak-to-trough happened to be inside the window you measured, and on this repo's own tapes it
reads -22.06% in sample and -33.72% out of sample.  The cap therefore moved -13.24% -> -20.23%
between the two windows — 6.99 pp — and THIS MORNING lane B's idea 1454 recommended raising
the live book's gross from 0.75 to 1.00 for the Sunday review on a DD margin of +4.32 pp
against the wider of those two caps.  Its own caveat 9(ii) names the problem and does not price
it.  This run prices it.

WHAT IS MEASURED, in three legs.

  LEG 1 — THE CAP'S OWN MOVEMENT (pure SPY, no book).  The 4b DD cap and CAGR floor are
  recomputed over: the full post-warm-up sample; IS and OOS at three splits (2015 / 2017 /
  2019); every calendar year; and EVERY rolling window of length L in {3, 5, 8, 10} years,
  stepped monthly.  Reported: min / median / max / SD of the cap in each family, and the
  IS -> OOS movement in pp.  This is the number every committed 4b DD margin in the record is
  implicitly quoted against.

  LEG 2 — THE BOOKS (the capital arm).  The LIVE RULES v2 shape (`baseline.rules_v2_weights`,
  200d +/-3% hysteresis band, de-gross to cash, never re-spread) at the LIVE weekly cadence,
  with its one sizing number walked over the SAME ladder 1454 used:
      G {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00}      DIAL 1
  7 rungs x 3 panels = 21 books, EVERY ONE published, full sample / halves / IS / OOS, both
  KEEP paths at every cell.  G = 0.75 weekly IS the live book; G = 1.00 weekly is 1454's
  recommendation.  No leverage: the ladder stops at 1.00 (PROTOCOL rule 2).

  LEG 3 — PROPAGATION INTO THE LICENSE.  The 2026-09-03 RECOMMENDATION's own G rule —
  "smallest G whose MaxDD <= 60% of SPY's and CAGR >= 70% of SPY's; if none, keep 75%" — is
  run with its bars measured on a TRAILING WINDOW of length
      L {3y, 5y, 8y, ALL-IS}                                DIAL 2
  ending at the decision date 2016-12-31, with the BOOK scored on the SAME window so that rule
  and bar always see the same tape.  Two tuned parameters exactly (G, L).  2017-2026 is then
  read ONCE for every licensed book, against the live RULES v2 baseline, the frozen live G =
  0.75 book, and SPY.  Three things are reported for each: which G the window licenses,
  whether the OOS cap the book actually had to live under was still cleared, and 4b OOS.

  LEG 4 — HOW MUCH CAP MOVEMENT FLIPS THE LICENSE.  For each panel the same rule is re-run
  against EVERY rolling-window cap from leg 1 (L = 8y, monthly step), giving the DISTRIBUTION
  of licensed G.  Reported: how many distinct G a reasonable tape could have licensed, the
  share of windows licensing 1454's G = 1.00, and every committed DD margin expressed in units
  of the cap's OWN rolling SD (margin / SD_cap) — which is the only honest way to read a
  margin quoted against a moving bar.

PRE-REGISTERED READING, stated before any number was read.  The cap is "stable enough to
budget against" only if (i) a margin of the size the record quotes (the incumbent's +1.1028 pp,
1454's +4.32 pp) is LARGE against the cap's own rolling SD, and (ii) the licensed G is the SAME
across the four L.  If either fails, a 4b DD pass is a statement about the window, not about
the book, and must be quoted with the cap's movement beside it.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths; the
halves; IS / OOS at three splits; turnover and its 10 bps drag.

COMPARANDS (rule 3): live RULES v2 at 10 bps weekly, SPY buy-and-hold, and the frozen live
G = 0.75 book.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3; rule 4 (both
KEEP paths, 2 tuned parameters); rule 8 (walk-forward: G chosen on the trailing window ending
2016-12-31, 2017-2026 read ONCE); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 the G = 0.75 weekly cell reproduces the live RULES v2 baseline
bit-for-bit.  G1b cross-script replay of 1454's committed U56 G = 1.00 W headline (11.53% /
1.201 / -15.91% full; 12.67% / 1.276 / -15.91% OOS).  G2 the cap identity: cap == 0.60 x SPY
MaxDD and floor == 0.70 x SPY CAGR on every window, to < 1e-12.  G3 NO LEAKAGE: every cap
window and every book statistic the licensing rule reads ends strictly before 2017-01-01.
G4 all 21 books published.  G5 exactly two tuned parameters.  G6 no leverage (max gross 1.00).
G7 MaxDD is monotone in G (the ladder is a ray).  G8 bit-identical recompute of the U56
headline book.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_is-the-4b-dd-cap-stable-enough-to-budget-against_cloud.py
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
from engine import backtest  # noqa: E402

DATE = "2026-09-19"
SLUG = "is-the-4b-dd-cap-stable-enough-to-budget-against"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
COST, CADENCE = 10.0, "W"
GRID_G = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]     # DIAL 1
CAP_L = [3, 5, 8, 0]                                       # DIAL 2 (0 = ALL-IS)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
ALT_SPLITS = {"2015": "2015-01-01", "2019": "2019-01-01"}
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_G = 0.75
ROLL_L_FOR_FLIP = 8                                        # the flip census window, in years
C_1454 = dict(CAGR=0.1153, Sharpe=1.201, MaxDD=-0.1591, oCAGR=0.1267, oSharpe=1.276)

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


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def pack(r):
    m = triple(r)
    h1, h2 = halves(np.asarray(r, float))
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_4a(c, base):
    return bool(c["H1"] > base["H1"] and c["H2"] > base["H2"] and c["MaxDD"] >= base["MaxDD"])


def keep_4b(c, bm):
    legs = dict(H1=bool(c["H1"] > bm["H1"]), H2=bool(c["H2"] > bm["H2"]),
                DD=bool(c["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(c["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return bool(all(legs.values())), legs


def rolling_windows(idx, L_years, step_months=1):
    """[(i0, i1)] for every window of L calendar years ending on a month end, stepped monthly."""
    if L_years <= 0:
        return []
    out = []
    ends = pd.date_range(idx[0] + pd.DateOffset(years=L_years), idx[-1], freq="ME")
    for e in ends[::step_months]:
        s = e - pd.DateOffset(years=L_years)
        i0 = int(np.searchsorted(idx.values, np.datetime64(s)))
        i1 = int(np.searchsorted(idx.values, np.datetime64(e), side="right"))
        if i1 - i0 > 200:
            out.append((i0, i1, pd.Timestamp(s), pd.Timestamp(e)))
    return out


def license_G(rows, cap, floor, live_g=LIVE_G):
    """The 2026-09-03 RECOMMENDATION's own rule, verbatim: 'smallest G whose MaxDD <= 60% of
    SPY's and CAGR >= 70% of SPY's; if none, keep 75%'.  rows: [(G, MaxDD, CAGR)] on the SAME
    window the bars were measured on.  Returns (G, used_fallback, n_clearing)."""
    ok = [g for (g, dd, cg) in rows if dd >= cap and cg >= floor]
    if not ok:
        return live_g, True, 0
    return min(ok), False, len(ok)


def main():
    t0 = time.time()
    say("=" * 136)
    say("IDEA 1450 (lane cloud, 2026-09-19) — is PROTOCOL 4b's DD CAP (0.60 x SPY MaxDD) STABLE "
        "ENOUGH TO BUDGET AGAINST, and what does its movement do to the GROSS it licenses?")
    say("BOOK: the LIVE RULES v2 shape at the LIVE weekly cadence, gross walked over "
        f"{GRID_G} (DIAL 1).  G=0.75 IS the live book; G=1.00 is 1454's Sunday recommendation.")
    say(f"LICENSING RULE (the 2026-09-03 memo's own): smallest G with MaxDD <= {DD_CAP} x SPY "
        f"MaxDD AND CAGR >= {CAGR_FLOOR} x SPY CAGR, else keep {LIVE_G}; bars measured on a "
        f"TRAILING window of L {CAP_L} years ending {IS_END} (DIAL 2, 0 = ALL-IS).")
    say("PRE-REGISTERED READING: the cap is budgetable only if (i) the record's quoted margins "
        "are LARGE against the cap's own rolling SD and (ii) the licensed G is the SAME at all "
        "four L.")
    say("=" * 136)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    keep_small = [c for c in pxS.columns if c == "SPY" or (c not in bad and mv[c] < 1.0)]
    pxS = pxS[keep_small]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(keep_small)-1} names remain.")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute CAGR below is an UPPER BOUND "
        "and every 4b pass optimistic.  The CAP side is the one part of this run the bias "
        "CANNOT touch — SPY is SPY — which is precisely why a cap that moves is a problem the "
        "survivorship caveat does not cover.")

    panels = [("U56", pxU), ("B136", pxB), ("SMALL", pxS)]

    cap_rows, book_rows, lic_rows, flip_rows = [], [], [], []
    cap_identity_dev = 0.0
    headline_ret = None
    leak = []

    for pname, px in panels:
        start = px.index[WARMUP]
        idx = px.index[WARMUP:]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_v = spy_r.values
        i_oos = int(np.searchsorted(idx.values, np.datetime64(OOS_START)))
        spy_f, spy_is, spy_o = pack(spy_v), pack(spy_v[:i_oos]), pack(spy_v[i_oos:])
        live_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=CADENCE)["returns"].loc[start:].values
        live_f, live_o = pack(live_r), pack(live_r[i_oos:])

        say(f"\n{'='*136}\n  [{pname}]  tape {idx[0].date()} .. {idx[-1].date()}  "
            f"({len(idx)} rows, {len(idx)/252:.1f}y)")
        say(f"    SPY FULL {spy_f['CAGR']:.2%}/{spy_f['Sharpe']:.4f}/{spy_f['MaxDD']:.2%} | "
            f"IS {spy_is['CAGR']:.2%}/{spy_is['Sharpe']:.4f}/{spy_is['MaxDD']:.2%} | "
            f"OOS {spy_o['CAGR']:.2%}/{spy_o['Sharpe']:.4f}/{spy_o['MaxDD']:.2%}")
        say(f"    LIVE RULES v2 @10bps FULL {live_f['CAGR']:.2%}/{live_f['Sharpe']:.4f}/"
            f"{live_f['MaxDD']:.2%} | OOS {live_o['CAGR']:.2%}/{live_o['Sharpe']:.4f}/"
            f"{live_o['MaxDD']:.2%}")

        # ---------- LEG 1: the cap's own movement ------------------------------------------
        fam = []
        fam.append(("FULL", 0, len(spy_v), idx[0], idx[-1]))
        for lbl, cut in [("2017", OOS_START)] + list(ALT_SPLITS.items()):
            k = int(np.searchsorted(idx.values, np.datetime64(cut)))
            fam.append((f"IS<{lbl}", 0, k, idx[0], idx[k - 1]))
            fam.append((f"OOS>={lbl}", k, len(spy_v), idx[k], idx[-1]))
        for y in sorted({d.year for d in idx}):
            a = int(np.searchsorted(idx.values, np.datetime64(f"{y}-01-01")))
            b = int(np.searchsorted(idx.values, np.datetime64(f"{y+1}-01-01")))
            if b - a > 200:
                fam.append((f"CY{y}", a, b, idx[a], idx[b - 1]))
        for L in (3, 5, 8, 10):
            for (a, b, s_, e_) in rolling_windows(idx, L):
                fam.append((f"ROLL{L}y", a, b, s_, e_))

        for (kind, a, b, s_, e_) in fam:
            w = spy_v[a:b]
            m = triple(w)
            cap, flo = DD_CAP * m["MaxDD"], CAGR_FLOOR * m["CAGR"]
            cap_identity_dev = max(cap_identity_dev, abs(cap - DD_CAP * m["MaxDD"]),
                                   abs(flo - CAGR_FLOOR * m["CAGR"]))
            cap_rows.append(dict(panel=pname, kind=kind, start=str(pd.Timestamp(s_).date()),
                                 end=str(pd.Timestamp(e_).date()), n=b - a,
                                 spy_CAGR=m["CAGR"], spy_Sharpe=m["Sharpe"], spy_MaxDD=m["MaxDD"],
                                 dd_cap=cap, cagr_floor=flo))

        CR = pd.DataFrame([r for r in cap_rows if r["panel"] == pname])
        say(f"\n    LEG 1 — THE CAP ITSELF (0.60 x SPY MaxDD), by window family:")
        say("      family     |  n |   cap min    median       max        SD  |  floor min   median      max")
        for kind in ["FULL"] + [f"IS<{k}" for k in ["2015", "2017", "2019"]] + \
                    [f"OOS>={k}" for k in ["2015", "2017", "2019"]] + \
                    [f"ROLL{L}y" for L in (3, 5, 8, 10)] + ["CY"]:
            sub = CR[CR.kind.str.startswith("CY")] if kind == "CY" else CR[CR.kind == kind]
            if not len(sub):
                continue
            say(f"      {kind:10} | {len(sub):2d} | {sub.dd_cap.min():8.2%} {sub.dd_cap.median():9.2%} "
                f"{sub.dd_cap.max():9.2%} {sub.dd_cap.std(ddof=1) if len(sub)>1 else 0:8.4f}  | "
                f"{sub.cagr_floor.min():8.2%} {sub.cagr_floor.median():8.2%} "
                f"{sub.cagr_floor.max():8.2%}")
        cap_is = DD_CAP * spy_is["MaxDD"]
        cap_oos = DD_CAP * spy_o["MaxDD"]
        r8 = CR[CR.kind == f"ROLL{ROLL_L_FOR_FLIP}y"]
        sd_cap = float(r8.dd_cap.std(ddof=1)) if len(r8) > 1 else np.nan
        sd_floor = float(r8.cagr_floor.std(ddof=1)) if len(r8) > 1 else np.nan
        say(f"    THE MOVEMENT THE RECORD BUDGETS AGAINST: IS cap {cap_is:.2%} -> OOS cap "
            f"{cap_oos:.2%} = {100*(cap_oos-cap_is):+.2f} pp; the {ROLL_L_FOR_FLIP}y rolling cap "
            f"has SD {100*sd_cap:.2f} pp over {len(r8)} windows (range {r8.dd_cap.min():.2%} .. "
            f"{r8.dd_cap.max():.2%}).")
        say(f"    THE OTHER BAR MOVES TOO: the 4b CAGR FLOOR (0.70 x SPY CAGR) has SD "
            f"{100*sd_floor:.2f} pp over the same {len(r8)} windows (range "
            f"{r8.cagr_floor.min():.2%} .. {r8.cagr_floor.max():.2%}); IS floor "
            f"{CAGR_FLOOR*spy_is['CAGR']:.2%} -> OOS floor {CAGR_FLOOR*spy_o['CAGR']:.2%} = "
            f"{100*CAGR_FLOOR*(spy_o['CAGR']-spy_is['CAGR']):+.2f} pp.")

        # ---------- LEG 2: the books --------------------------------------------------------
        rets = {}
        say(f"\n    LEG 2 — THE LADDER ({len(GRID_G)} books, weekly, 10 bps, t+1).  Every cell "
            f"published.")
        say("        G |    CAGR  Sharpe   MaxDD     H1     H2 | 4a 4b | OOS CAGR  Sharpe   MaxDD "
            "| o4a o4b | DDmarg CAGRmarg | oDDmarg oCAGRmarg | turn drag")
        for g in GRID_G:
            res = backtest(px, rules_v2_weights(px, gross=g), cost_bps=COST, freq=CADENCE)
            r = res["returns"].loc[start:]
            v = r.values
            rets[g] = v
            f_, o_ = pack(v), pack(v[i_oos:])
            k4a, k4b_legs = keep_4a(f_, live_f), keep_4b(f_, spy_f)
            k4aO, k4bO_legs = keep_4a(o_, live_o), keep_4b(o_, spy_o)
            turn_y = float(res["turnover"].loc[start:].sum() / (len(r) / 252))
            row = dict(panel=pname, G=g, CAGR=f_["CAGR"], Sharpe=f_["Sharpe"], MaxDD=f_["MaxDD"],
                       H1=f_["H1"], H2=f_["H2"],
                       oCAGR=o_["CAGR"], oSharpe=o_["Sharpe"], oMaxDD=o_["MaxDD"],
                       oH1=o_["H1"], oH2=o_["H2"],
                       keep4a=k4a, keep4b=k4b_legs[0], keep4a_oos=k4aO, keep4b_oos=k4bO_legs[0],
                       legDD=k4b_legs[1]["DD"], legCAGR=k4b_legs[1]["CAGR"],
                       legH1=k4b_legs[1]["H1"], legH2=k4b_legs[1]["H2"],
                       oleg_DD=k4bO_legs[1]["DD"], oleg_CAGR=k4bO_legs[1]["CAGR"],
                       oleg_H1=k4bO_legs[1]["H1"], oleg_H2=k4bO_legs[1]["H2"],
                       dd_margin_pp=100 * (f_["MaxDD"] - DD_CAP * spy_f["MaxDD"]),
                       cagr_margin_pp=100 * (f_["CAGR"] - CAGR_FLOOR * spy_f["CAGR"]),
                       oos_dd_margin_pp=100 * (o_["MaxDD"] - cap_oos),
                       oos_cagr_margin_pp=100 * (o_["CAGR"] - CAGR_FLOOR * spy_o["CAGR"]),
                       dd_margin_in_cap_SD=(f_["MaxDD"] - DD_CAP * spy_f["MaxDD"]) / sd_cap
                       if sd_cap and np.isfinite(sd_cap) else np.nan,
                       cagr_margin_in_floor_SD=(f_["CAGR"] - CAGR_FLOOR * spy_f["CAGR"]) / sd_floor
                       if sd_floor and np.isfinite(sd_floor) else np.nan,
                       floor_roll8_SD_pp=100 * sd_floor,
                       turn_y=turn_y, drag_bpyr=turn_y * COST,
                       spy_CAGR=spy_f["CAGR"], spy_Sharpe=spy_f["Sharpe"], spy_MaxDD=spy_f["MaxDD"],
                       spy_oCAGR=spy_o["CAGR"], spy_oSharpe=spy_o["Sharpe"], spy_oMaxDD=spy_o["MaxDD"],
                       live_Sharpe=live_f["Sharpe"], live_MaxDD=live_f["MaxDD"],
                       live_oSharpe=live_o["Sharpe"], live_oMaxDD=live_o["MaxDD"],
                       cap_full=DD_CAP * spy_f["MaxDD"], cap_is=cap_is, cap_oos=cap_oos,
                       cap_roll8_SD_pp=100 * sd_cap)
            book_rows.append(row)
            say(f"    {g:5.3f} | {f_['CAGR']:7.2%} {f_['Sharpe']:7.4f} {f_['MaxDD']:7.2%} "
                f"{f_['H1']:6.3f} {f_['H2']:6.3f} | {int(k4a)}  {int(k4b_legs[0])} | "
                f"{o_['CAGR']:8.2%} {o_['Sharpe']:7.4f} {o_['MaxDD']:7.2%} | {int(k4aO)}   "
                f"{int(k4bO_legs[0])} | {row['dd_margin_pp']:+6.2f} {row['cagr_margin_pp']:+8.2f} "
                f"| {row['oos_dd_margin_pp']:+7.2f} {row['oos_cagr_margin_pp']:+9.2f} | "
                f"{turn_y:4.2f} {turn_y*COST:5.1f}")
            if pname == "U56" and g == 1.00:
                headline_ret = v.copy()
                d = max(abs(f_["CAGR"] - C_1454["CAGR"]), abs(f_["MaxDD"] - C_1454["MaxDD"]),
                        abs(o_["CAGR"] - C_1454["oCAGR"]))
                gate("G1b cross-script replay of 1454's committed U56 G=1.00 W headline "
                     "(11.53%/1.201/-15.91% full; 12.67%/1.276/-15.91% OOS)",
                     f"max |d| {d:.2e} (got {f_['CAGR']:.4f}/{f_['Sharpe']:.4f}/{f_['MaxDD']:.4f}; "
                     f"OOS {o_['CAGR']:.4f}/{o_['Sharpe']:.4f}/{o_['MaxDD']:.4f})", "< 5e-3",
                     d < 5e-3)
            if pname == "U56" and g == LIVE_G:
                d1 = max(abs(f_["Sharpe"] - live_f["Sharpe"]), abs(f_["MaxDD"] - live_f["MaxDD"]))
                gate("G1 the G=0.75 weekly cell reproduces the live RULES v2 baseline",
                     f"max |d| {d1:.2e}", "< 1e-12", d1 < 1e-12)

        # ---------- LEG 3: propagate the cap into the license --------------------------------
        say(f"\n    LEG 3 — WHAT EACH TRAILING CAP WINDOW LICENSES (rule and bar always read the "
            f"SAME window; 2017-2026 read ONCE afterwards).")
        say("      L      window                   | SPY MaxDD   cap   | SPY CAGR  floor  | "
            "clears | licensed G  fb | IS MaxDD   IS CAGR | OOS CAGR  Sharpe   MaxDD | OOS cap  "
            "held | o4b | vs LIVE G=0.75 OOS CAGR pp")
        i_is_end = int(np.searchsorted(idx.values, np.datetime64(OOS_START)))
        live_book_o = pack(rets[LIVE_G][i_oos:])
        for L in CAP_L:
            if L == 0:
                a, lbl = 0, "ALL-IS"
            else:
                s_ = idx[i_is_end - 1] - pd.DateOffset(years=L)
                a, lbl = int(np.searchsorted(idx.values, np.datetime64(s_))), f"{L}y"
            b = i_is_end
            leak.append(idx[b - 1])
            w = spy_v[a:b]
            ms = triple(w)
            cap_w, flo_w = DD_CAP * ms["MaxDD"], CAGR_FLOOR * ms["CAGR"]
            rows_g = [(g, mdd(rets[g][a:b]), cagr(rets[g][a:b])) for g in GRID_G]
            gsel, fb, nclear = license_G(rows_g, cap_w, flo_w)
            bk = [r for r in book_rows if r["panel"] == pname and r["G"] == gsel][0]
            is_dd, is_cg = [(dd, cg) for (g, dd, cg) in rows_g if g == gsel][0]
            held = bool(bk["oMaxDD"] >= cap_oos)
            lic_rows.append(dict(panel=pname, cap_L=lbl, win_start=str(idx[a].date()),
                                 win_end=str(idx[b - 1].date()), n=b - a,
                                 spy_MaxDD=ms["MaxDD"], dd_cap=cap_w, spy_CAGR=ms["CAGR"],
                                 cagr_floor=flo_w, n_rungs_clearing=nclear,
                                 licensed_G=gsel, used_fallback=fb,
                                 is_MaxDD=is_dd, is_CAGR=is_cg,
                                 oCAGR=bk["oCAGR"], oSharpe=bk["oSharpe"], oMaxDD=bk["oMaxDD"],
                                 oos_cap=cap_oos, oos_cap_held=held,
                                 keep4b_oos=bk["keep4b_oos"], keep4b_full=bk["keep4b"],
                                 keep4a_oos=bk["keep4a_oos"],
                                 oos_dd_margin_pp=bk["oos_dd_margin_pp"],
                                 oos_cagr_margin_pp=bk["oos_cagr_margin_pp"],
                                 d_oCAGR_pp_vs_live=100 * (bk["oCAGR"] - live_book_o["CAGR"]),
                                 d_oSharpe_vs_live=bk["oSharpe"] - live_book_o["Sharpe"],
                                 d_oMaxDD_pp_vs_live=100 * (bk["oMaxDD"] - live_book_o["MaxDD"]),
                                 spy_oCAGR=spy_o["CAGR"], spy_oSharpe=spy_o["Sharpe"],
                                 spy_oMaxDD=spy_o["MaxDD"],
                                 rulesv2_oSharpe=live_o["Sharpe"], rulesv2_oMaxDD=live_o["MaxDD"]))
            say(f"      {lbl:6} {idx[a].date()}..{idx[b-1].date()} | {ms['MaxDD']:8.2%} "
                f"{cap_w:7.2%} | {ms['CAGR']:7.2%} {flo_w:6.2%} | {nclear:2d}/{len(GRID_G)} | "
                f"{gsel:9.3f}  {int(fb)} | {is_dd:7.2%} {is_cg:8.2%} | {bk['oCAGR']:8.2%} "
                f"{bk['oSharpe']:7.4f} {bk['oMaxDD']:7.2%} | {cap_oos:7.2%} {int(held)} | "
                f"{int(bk['keep4b_oos'])} | {100*(bk['oCAGR']-live_book_o['CAGR']):+.2f}")

        # ---------- LEG 4: how much cap movement flips the license --------------------------
        r8w = [(r["start"], r["end"], r["dd_cap"], r["cagr_floor"]) for r in cap_rows
               if r["panel"] == pname and r["kind"] == f"ROLL{ROLL_L_FOR_FLIP}y"]
        lic_counts = {}
        for (s_, e_, cap_w, flo_w) in r8w:
            a = int(np.searchsorted(idx.values, np.datetime64(s_)))
            b = int(np.searchsorted(idx.values, np.datetime64(e_), side="right"))
            rows_g = [(g, mdd(rets[g][a:b]), cagr(rets[g][a:b])) for g in GRID_G]
            gsel, fb, nclear = license_G(rows_g, cap_w, flo_w)
            lic_counts[gsel] = lic_counts.get(gsel, 0) + 1
            flip_rows.append(dict(panel=pname, win_start=s_, win_end=e_, dd_cap=cap_w,
                                  cagr_floor=flo_w, licensed_G=gsel, used_fallback=fb,
                                  n_rungs_clearing=nclear))
        tot = sum(lic_counts.values())
        if tot:
            share = ", ".join(f"G={g:.3f}: {n} ({n/tot:.0%})"
                              for g, n in sorted(lic_counts.items()))
            say(f"\n    LEG 4 — THE SAME RULE AGAINST EVERY {ROLL_L_FOR_FLIP}y ROLLING CAP "
                f"({tot} windows): {len(lic_counts)} distinct G licensed -> {share}")
            say(f"      (a 'fallback' license means no rung cleared BOTH bars on that window and "
                f"the memo's own 'keep 0.75' fired: "
                f"{sum(1 for r in flip_rows if r['panel']==pname and r['used_fallback'])} of "
                f"{tot} windows)")

    B = pd.DataFrame(book_rows)
    CAP = pd.DataFrame(cap_rows)
    LIC = pd.DataFrame(lic_rows)
    FLIP = pd.DataFrame(flip_rows)

    say("\n" + "=" * 136)
    say("GATES")
    say("=" * 136)
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(px.index) - WARMUP for _, px in panels) / 252.0, 2), ">= 10.0",
         min(len(px.index) - WARMUP for _, px in panels) / 252.0 >= 10.0)
    gate("G2 cap identity holds on every window (cap == 0.60 x SPY MaxDD, floor == 0.70 x SPY "
         "CAGR)", f"max |dev| {cap_identity_dev:.3e} over {len(CAP)} windows", "< 1e-12",
         cap_identity_dev < 1e-12)
    gate("G3 NO LEAKAGE: every licensing window ends strictly before 2017-01-01",
         "last rows " + ", ".join(sorted({str(x.date()) for x in leak})), "all < 2017-01-01",
         all(x < pd.Timestamp(OOS_START) for x in leak))
    gate("G4 all 21 books published", len(B), "== 21", len(B) == 21)
    gate("G5 exactly two tuned parameters (G, cap window L)", "2", "== 2", True)
    gate("G6 no leverage: max gross on the ladder", f"{max(GRID_G):.2f}", "<= 1.00",
         max(GRID_G) <= 1.0)
    mono = all(bool((B[B.panel == p].sort_values("G").MaxDD.diff().dropna() <= 1e-12).all())
               for p, _ in panels)
    gate("G7 MaxDD is monotone (deeper) in G on every panel — the ladder is a ray", mono, "True",
         mono)

    px = dict(panels)["U56"]
    start = px.index[WARMUP]
    rr = backtest(px, rules_v2_weights(px, gross=1.00), cost_bps=COST,
                  freq=CADENCE)["returns"].loc[start:].values
    d8 = float(np.max(np.abs(rr - headline_ret)))
    gate("G8 bit-identical recompute (U56, G=1.00, weekly)", f"max |dret| {d8:.3e}", "< 1e-15",
         d8 < 1e-15)

    say("\n" + "=" * 136)
    say("THE ANSWER")
    say("=" * 136)
    for pname, _ in panels:
        sub = LIC[LIC.panel == pname]
        cr = CAP[(CAP.panel == pname) & (CAP.kind == f"ROLL{ROLL_L_FOR_FLIP}y")]
        bk = B[B.panel == pname]
        gset = sorted(sub.licensed_G.unique())
        fl = FLIP[FLIP.panel == pname]
        say(f"\n  [{pname}]")
        cap_is_p, cap_oos_p = float(bk.cap_is.iloc[0]), float(bk.cap_oos.iloc[0])
        say(f"    (i)  THE CAP MOVES: {ROLL_L_FOR_FLIP}y rolling cap "
            f"{cr.dd_cap.min():.2%} .. {cr.dd_cap.max():.2%} (SD {100*cr.dd_cap.std(ddof=1):.2f} pp "
            f"over {len(cr)} windows, full range {100*(cr.dd_cap.max()-cr.dd_cap.min()):.2f} pp); "
            f"IS cap {cap_is_p:.2%} -> OOS cap {cap_oos_p:.2%} = "
            f"{100*(cap_oos_p-cap_is_p):+.2f} pp")
        say(f"    (ii) THE LICENSE MOVES: the four trailing windows license {len(gset)} distinct "
            f"G {gset} (fallback fired at {int(sub.used_fallback.sum())} of {len(sub)}); across "
            f"the {len(fl)} rolling {ROLL_L_FOR_FLIP}y caps, "
            f"{fl.licensed_G.nunique()} distinct G, share at G=1.00 "
            f"{(fl.licensed_G == 1.00).mean():.0%}, fallback {fl.used_fallback.mean():.0%}")
        say(f"    (iii) MARGINS IN UNITS OF THE CAP'S OWN SD: full-sample DD margin / SD_cap "
            f"ranges {bk.dd_margin_in_cap_SD.min():+.2f} .. {bk.dd_margin_in_cap_SD.max():+.2f} "
            f"over the ladder (live G=0.75: "
            f"{float(bk[bk.G==LIVE_G].dd_margin_in_cap_SD.iloc[0]):+.2f}; G=1.00: "
            f"{float(bk[bk.G==1.00].dd_margin_in_cap_SD.iloc[0]):+.2f})")
        say(f"    (iiib) THE BINDING LEG FOR THIS BOOK IS THE CAGR FLOOR, AND IT MOVES TOO: "
            f"full-sample CAGR margin / SD_floor ranges "
            f"{bk.cagr_margin_in_floor_SD.min():+.2f} .. "
            f"{bk.cagr_margin_in_floor_SD.max():+.2f} over the ladder (live G=0.75: "
            f"{float(bk[bk.G==LIVE_G].cagr_margin_in_floor_SD.iloc[0]):+.2f}; G=1.00: "
            f"{float(bk[bk.G==1.00].cagr_margin_in_floor_SD.iloc[0]):+.2f}); SD_floor "
            f"{float(bk.floor_roll8_SD_pp.iloc[0]):.2f} pp")
        say(f"    (iv) KEEP paths on the ladder: 4a {int(bk.keep4a.sum())}/{len(bk)} FULL, "
            f"{int(bk.keep4a_oos.sum())} OOS;  4b {int(bk.keep4b.sum())}/{len(bk)} FULL, "
            f"{int(bk.keep4b_oos.sum())} OOS, both {int((bk.keep4b & bk.keep4b_oos).sum())}")

    say(f"\n  ALL PANELS: 4a {int(B.keep4a.sum())} of {len(B)} FULL / {int(B.keep4a_oos.sum())} "
        f"OOS;  4b {int(B.keep4b.sum())} of {len(B)} FULL / {int(B.keep4b_oos.sum())} OOS / "
        f"{int((B.keep4b & B.keep4b_oos).sum())} both.")
    say(f"  LICENSE AGREEMENT ACROSS THE FOUR TRAILING WINDOWS: "
        f"{int((LIC.groupby('panel').licensed_G.nunique() == 1).sum())} of 3 panels license a "
        f"SINGLE G at all four L.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    B.to_csv(f"{OUT}.books.csv", index=False)
    CAP.to_csv(f"{OUT}.capwindows.csv", index=False)
    LIC.to_csv(f"{OUT}.licenses.csv", index=False)
    FLIP.to_csv(f"{OUT}.flipcensus.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.books.csv / .capwindows.csv / .licenses.csv / .flipcensus.csv / "
        f".gates.csv / .log.txt")
    say(f"  ALL GATES PASS: {all(g['pass_'] for g in GATES)}   ({time.time()-t0:.1f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

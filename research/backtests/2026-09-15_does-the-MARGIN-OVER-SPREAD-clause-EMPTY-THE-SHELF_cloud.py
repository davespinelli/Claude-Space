#!/usr/bin/env python3
"""Idea 891 - "does-the-MARGIN-OVER-SPREAD-clause-EMPTY-THE-SHELF-on-the-RECORD-s-COMMITTED-4b-PASSES"
(cloud lane, 2026-09-15, idea 1 of 2).

The question
------------
Idea 879 built a synthetic ladder population, walked every book over its rebalance calendar, and
found 18 of 18 of that population's 4b passes flip at least one leg on SOME calendar offset.  It
then proposed a PROTOCOL clause: a 4b leg only counts if the book's MARGIN on that leg is at least
as large as the SPREAD of the same leg across the rebalance calendar,

        min over legs of  ( margin at the published calendar / spread across all calendars )  >= 1

i.e. "your pass must survive the date you happened to rebalance on".  879's population was a
ladder it built itself.  This run prices the same clause on the objects that actually matter: the
record's COMMITTED 4b passes - the memo-backed books the shelf carries - and reports how many
survive.

What is measured, exactly
-------------------------
For each committed book and each rebalance-calendar offset k (the book's own cadence mask shifted
forward k trading days: k = 0..4 weekly, k = 0..20 monthly; k = 0 is the published calendar):

    LEVELS   CAGR, Sharpe, MaxDD, H1 Sharpe, H2 Sharpe, OOS Sharpe, OOS CAGR, OOS MaxDD
    4b LEGS  H1 > SPY_H1, H2 > SPY_H2, OOS > SPY_OOS, MaxDD >= 0.60 x SPY MaxDD,
             CAGR >= 0.70 x SPY CAGR              (rule 8's OOS leg carried as a fifth leg)
    4a LEGS  H1 > v2_H1, H2 > v2_H2, MaxDD >= v2 MaxDD

    MARGIN   the leg's signed slack at k = 0, in the leg's own units (Sharpe points, pp for DD
             and CAGR).  The comparands (SPY, and the LIVE RULES v2 book on its own published
             weekly calendar) are held at their own conventions and are NOT offset with the book -
             SPY has no rebalance calendar at all, and v2's calendar is the live book's, not the
             candidate's.
    SPREAD   max - min of the BOOK's own statistic on that leg across all offsets.
    RATIO    margin / spread.  The clause survives a leg at RATIO >= 1 and the book at
             min-over-legs RATIO >= 1.

Pre-registered hypotheses and bars (fixed before any number below the gates was read)
    H_EMPTY   the clause leaves 0 of the committed 4b passes standing on path 4b.
              PASS = the shelf is emptied, 879's synthetic result reproduces on the real record.
    H_DD      the DD leg is the binding (smallest-ratio) leg for a MAJORITY of the books.
              879 measured the DD leg's calendar spread at 5.8x the CAGR leg's.
    H_MEDIAN  the median min-ratio over the committed passes is < 1.
    H_RUNG    the survivor count is the SAME at 10 bps and at 25 bps.  A clause whose answer
              moves with the cost rung is not a calendar clause.
    H_WF      rule 8: the book an IS-only (2009-2016) min-ratio chooser picks has the same 4b
              verdict out of sample as it has on the full sample.
  Each prints its bar and PASS/FAIL.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. pass set    SHELF (the record's committed, memo-backed 4b passes) - headline;
                   GRID (861's mechanical never-memo-selected ladder) - reported control.
    2. offset grid k over the book's own cadence: 5 weekly, 21 monthly.  ALL points reported.
  Cost rung {10, 25} bps and the 21-sleeve ENSEMBLE book are reported CONTROLS, not dials.

Reproduction gates (printed before any new number is read)
    G1  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G2  the k = 0 offset mask is engine.rebalance_mask, elementwise.
    G3  fast_run at k = 0 reproduces engine.backtest's net returns on a live book.
    G4  the SPY comparand reproduces the record's committed SPY triple.

Data: committed price caches only.  No network, never yfinance.
SURVIVORSHIP: U56 (research/universe.json) and B136 (research/universe_broad.json) are
CURRENT-constituent lists, so every CAGR and MaxDD LEVEL here is optimistic - the books' and the
comparands' alike.  The clause is a statement about a book's margin RELATIVE to its own calendar
spread, and both sides of that ratio are computed on the same biased panel, which is why the ratio
is the reported object and no level below is a capital claim.

Deterministic, standalone.  Modifies nothing.  Proposes no PROTOCOL edit and applies none.
Run: python research/backtests/2026-09-15_does-the-MARGIN-OVER-SPREAD-clause-EMPTY-THE-SHELF_cloud.py
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-15"
SLUG = "does-the-MARGIN-OVER-SPREAD-clause-EMPTY-THE-SHELF"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
LANEC = Path(__file__).resolve().parent / f"{DATE}_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, LAG, MAX_VOL = 260, 1, 0.60
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
OOS_START = "2017-01-01"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
N_OFF = {"W": 5, "M": 21}
LEGS_4B = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGS_4A = ["H1", "H2", "DD"]
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC891", LANEC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load_lane_c()
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def offset_mask(idx, freq, k):
    """The book's own cadence mask, shifted forward k trading days.  k = 0 is the published
    calendar (engine.rebalance_mask); k > 0 rebalances k trading days later each period."""
    m = rebalance_mask(idx, freq)
    if k == 0:
        return m
    return m.shift(k, fill_value=False)


def stats(r, idx, oos0):
    """Full-sample moments (record's COUNT half convention) plus the rule-8 OOS window."""
    cagr, sh, dd = fmet(r)
    h = len(r) // 2
    oos = np.asarray(idx >= pd.Timestamp(oos0))
    ocagr, osh, odd = fmet(r[oos])
    return dict(CAGR=cagr, Sharpe=sh, MaxDD=dd, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
                OOS_CAGR=ocagr, OOS_Sharpe=osh, OOS_MaxDD=odd)


def legs_4b(s, spy):
    """Signed slack on each 4b leg, in the leg's own units (Sharpe points; pp for DD and CAGR)."""
    return dict(H1=s["H1"] - spy["H1"], H2=s["H2"] - spy["H2"],
                OOS=s["OOS_Sharpe"] - spy["OOS_Sharpe"],
                DD=100.0 * (s["MaxDD"] - DDCAP_FRAC * spy["MaxDD"]),
                CAGR=100.0 * (s["CAGR"] - CAGRFLOOR_FRAC * spy["CAGR"]))


def legs_4a(s, base):
    return dict(H1=s["H1"] - base["H1"], H2=s["H2"] - base["H2"],
                DD=100.0 * (s["MaxDD"] - base["MaxDD"]))


def leg_stat(s, leg):
    """The BOOK-side statistic whose calendar spread the clause compares the margin against."""
    return {"H1": s["H1"], "H2": s["H2"], "OOS": s["OOS_Sharpe"],
            "DD": 100.0 * s["MaxDD"], "CAGR": 100.0 * s["CAGR"]}[leg]


def main():
    t0 = time.time()
    P(f"# Idea 891 - does the MARGIN-OVER-SPREAD clause EMPTY THE SHELF on the record's COMMITTED "
      f"4b PASSES?  ({DATE}, cloud lane)")
    P(f"# 2 tuned dials: PASS SET [SHELF, GRID] x OFFSET GRID k (5 weekly / 21 monthly). "
      f"ALL grid points reported.  Cost rung {RUNGS} bps is a reported control.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels; every LEVEL below is optimistic.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}

    # ---------------------------------------------------------------- the committed pass set
    books = C.shelf_books(U, B)                      # 861's shelf, imported not re-typed
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    books["u56-top20-g065-M"] = dict(                # idea 879's own committed 4b pass (2026-09-15)
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    SHELF = list(books)
    GRID = C.grid_books(U, B)

    P(f"SHELF = {len(SHELF)} committed memo-backed 4b passes; GRID = {len(GRID)} never-selected "
      f"ladder books (control).")
    P("")

    # ---------------------------------------------------------------- comparands
    start = {p: PX[p].index[WARMUP] for p in PX}
    spy, v2 = {}, {}
    for p, px in PX.items():
        sr = px["SPY"].pct_change().fillna(0.0).loc[start[p]:]
        spy[p] = {c: stats(sr.values, sr.index, OOS_START) for c in RUNGS}   # SPY has no calendar
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            n = (r - t * c / 1e4).loc[start[p]:]
            v2.setdefault(p, {})[c] = stats(n.values, n.index, OOS_START)

    # ---------------------------------------------------------------- GATES
    P("## Reproduction gates")
    g_rows = []
    ok1 = True
    for nm in SHELF:
        b = books[nm]
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], offset_mask(px.index, b["freq"], 0))
        n = (r - t * RUNG_HEAD / 1e4).loc[start[b["panel"]]:]
        s = stats(n.values, n.index, OOS_START)
        m = b["memo"]
        dc = abs(s["CAGR"] - m[0]) if m[0] is not None else 0.0
        ds = abs(s["Sharpe"] - m[1]) if m[1] is not None else 0.0
        dd = abs(s["MaxDD"] - m[2]) if m[2] is not None else 0.0
        good = dc <= 0.015 and ds <= 0.030 and dd <= 0.015
        ok1 &= good
        g_rows.append(dict(book=nm, memo_CAGR=m[0], got_CAGR=round(s["CAGR"], 4),
                           memo_Sharpe=m[1], got_Sharpe=round(s["Sharpe"], 4),
                           memo_MaxDD=m[2], got_MaxDD=round(s["MaxDD"], 4),
                           dCAGR=round(dc, 4), dSharpe=round(ds, 4), dMaxDD=round(dd, 4),
                           gate="PASS" if good else "FAIL"))
    gdf = pd.DataFrame(g_rows)
    P(gdf.to_string(index=False))
    P(f"G1 every SHELF book reproduces its committed memo triple: {'PASS' if ok1 else 'FAIL'}")

    m0 = offset_mask(U.index, "W", 0)
    ok2 = bool((m0.values == rebalance_mask(U.index, "W").values).all())
    P(f"G2 k=0 mask == engine.rebalance_mask: {'PASS' if ok2 else 'FAIL'}")

    bw = rules_v2_weights(U)
    eng = backtest(U, bw, cost_bps=RUNG_HEAD, freq="W")
    fr, ft = fast_run(U, bw, rebalance_mask(U.index, "W"))
    d3 = float(np.abs((fr - ft * RUNG_HEAD / 1e4).loc[start["U56"]:].values
                      - eng["returns"].loc[start["U56"]:].values).max())
    ok3 = d3 < 1e-10
    P(f"G3 fast_run(k=0) vs engine.backtest max|d ret| = {d3:.3e}: {'PASS' if ok3 else 'FAIL'}")

    sp = spy["U56"][RUNG_HEAD]
    ok4 = abs(sp["CAGR"] - 0.1513) <= 0.004 and abs(sp["Sharpe"] - 0.886) <= 0.02 \
        and abs(sp["MaxDD"] + 0.3372) <= 0.01
    P(f"G4 SPY comparand {sp['CAGR']:.4f} / {sp['Sharpe']:.3f} / {sp['MaxDD']:.4f} vs committed "
      f"0.1513 / 0.886 / -0.3372: {'PASS' if ok4 else 'FAIL'}")
    P(f"   SPY halves {sp['H1']:.3f} / {sp['H2']:.3f}, OOS {sp['OOS_CAGR']:.4f} / "
      f"{sp['OOS_Sharpe']:.3f} / {sp['OOS_MaxDD']:.4f}")
    P(f"GATES {sum([ok1, ok2, ok3, ok4])}/4")
    P("")
    if not (ok1 and ok2 and ok3 and ok4):
        P("!! a gate FAILED - every number below is reported but the run does not claim it.")

    # ---------------------------------------------------------------- the census
    rows = []
    for setname, bset in (("SHELF", books), ("GRID", GRID)):
        for nm, b in bset.items():
            px = PX[b["panel"]]
            nk = N_OFF[b["freq"]]
            for k in range(nk):
                r, t = fast_run(px, b["W"], offset_mask(px.index, b["freq"], k))
                for c in RUNGS:
                    n = (r - t * c / 1e4).loc[start[b["panel"]]:]
                    s = stats(n.values, n.index, OOS_START)
                    L4b = legs_4b(s, spy[b["panel"]][c])
                    L4a = legs_4a(s, v2[b["panel"]][c])
                    rows.append(dict(set=setname, book=nm, panel=b["panel"], freq=b["freq"],
                                     k=k, rung=c, **{f"lvl_{x}": s[x] for x in s},
                                     **{f"m4b_{x}": L4b[x] for x in L4b},
                                     **{f"m4a_{x}": L4a[x] for x in L4a},
                                     pass4b=all(v > 0 for v in L4b.values()),
                                     pass4a=all(v > 0 for v in L4a.values())))
    A = pd.DataFrame(rows)
    A.to_csv(f"{OUT}.arms.csv", index=False)
    P(f"## Census: {len(A)} (set x book x offset x rung) cells -> {Path(OUT).name}.arms.csv")
    P("")

    # ---------------------------------------------------------------- the clause
    cl = []
    for (setname, nm, c), g in A.groupby(["set", "book", "rung"], sort=False):
        k0 = g[g.k == 0].iloc[0]
        rec = dict(set=setname, book=nm, panel=k0.panel, freq=k0.freq, rung=c,
                   n_off=len(g), pass4b_k0=bool(k0.pass4b), pass4a_k0=bool(k0.pass4a),
                   n_off_pass4b=int(g.pass4b.sum()), n_off_pass4a=int(g.pass4a.sum()))
        for path, legs in (("4b", LEGS_4B), ("4a", LEGS_4A)):
            ratios = {}
            for leg in legs:
                margin = float(k0[f"m{path}_{leg}"])
                col = {"H1": "lvl_H1", "H2": "lvl_H2", "OOS": "lvl_OOS_Sharpe",
                       "DD": "lvl_MaxDD", "CAGR": "lvl_CAGR"}[leg]
                sc = 100.0 if leg in ("DD", "CAGR") else 1.0
                spread = sc * float(g[col].max() - g[col].min())
                ratios[leg] = margin / spread if spread > 0 else np.inf
                rec[f"{path}_margin_{leg}"] = margin
                rec[f"{path}_spread_{leg}"] = spread
                rec[f"{path}_ratio_{leg}"] = ratios[leg]
            bind = min(ratios, key=lambda x: ratios[x])
            rec[f"{path}_minratio"] = ratios[bind]
            rec[f"{path}_binding"] = bind
            rec[f"{path}_clause"] = bool(rec[f"pass{path}_k0"] and ratios[bind] >= 1.0)
        cl.append(rec)
    CL = pd.DataFrame(cl)
    CL.to_csv(f"{OUT}.clause.csv", index=False)

    P("## The clause on the record's COMMITTED 4b passes (SHELF), headline rung 10 bps")
    sh = CL[(CL.set == "SHELF") & (CL.rung == RUNG_HEAD)].copy()
    show = sh[["book", "panel", "freq", "n_off", "pass4b_k0", "n_off_pass4b",
               "4b_margin_DD", "4b_spread_DD", "4b_ratio_DD", "4b_minratio", "4b_binding",
               "4b_clause"]]
    P(show.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("")
    P("Per-leg margin / spread / ratio, every leg, every committed pass (10 bps):")
    for _, r in sh.iterrows():
        P(f"  {r.book:36s} " + "  ".join(
            f"{leg}: {r[f'4b_margin_{leg}']:+.3f}/{r[f'4b_spread_{leg}']:.3f}="
            f"{r[f'4b_ratio_{leg}']:.2f}" for leg in LEGS_4B))
    P("")

    # ---------------------------------------------------------------- the ENSEMBLE control
    P("## Control: the record's 21-sleeve calendar ENSEMBLE book (2026-09-15 lane C memo)")
    # MA-DG, the memo's wording: 1/N of NAV per name above its 200d mean, N = names PRICED that
    # day (not names above), so gated-out weight goes to CASH and is never re-spread.
    ab = (U > U.rolling(200).mean()).astype(float)
    nn = U.notna().sum(axis=1).replace(0, np.nan)
    Wmadg = ab.div(nn, axis=0).fillna(0.0)
    ens = {c: None for c in RUNGS}
    for c in RUNGS:
        # ENS-NAV, the memo's own convention: capital is split ONCE into 21 sleeves and the
        # sleeves are never re-equalised, so the ensemble NAV is the MEAN OF THE SLEEVE EQUITY
        # CURVES (not the mean of their daily returns, which re-equalises every day).
        eq = None
        for k in range(21):
            r, t = fast_run(U, Wmadg, offset_mask(U.index, "M", k))
            n = (r - t * c / 1e4).loc[start["U56"]:]
            e_k = np.cumprod(1.0 + n.values)
            eq = e_k / 21.0 if eq is None else eq + e_k / 21.0
        acc = np.diff(np.concatenate([[1.0], eq])) / np.concatenate([[1.0], eq[:-1]])
        ens[c] = stats(acc, n.index, OOS_START)
    e = ens[RUNG_HEAD]
    eL = legs_4b(e, spy["U56"][RUNG_HEAD])
    P(f"  ENSEMBLE full {e['CAGR']:.2%} / {e['Sharpe']:.3f} / {e['MaxDD']:.2%}, halves "
      f"{e['H1']:.3f} / {e['H2']:.3f}, OOS {e['OOS_CAGR']:.2%} / {e['OOS_Sharpe']:.3f} / "
      f"{e['OOS_MaxDD']:.2%}  (committed memo: 11.68% / 1.177 / -19.07%)")
    P(f"  4b legs {', '.join(f'{k} {v:+.3f}' for k, v in eL.items())} -> "
      f"{'PASS' if all(v > 0 for v in eL.values()) else 'FAIL'}")
    P("  The clause is VACUOUS for this book: it holds all 21 calendars at once, so its calendar "
      "spread is 0 by construction and its ratio is infinite on every leg.  That is the only way "
      "a book passes the clause without having a margin bigger than a spread.")
    P("")

    # ---------------------------------------------------------------- hypotheses
    P("## Pre-registered hypotheses")
    surv = int(sh["4b_clause"].sum())
    h_empty = surv == 0
    P(f"H_EMPTY  clause leaves 0 of {len(sh)} committed 4b passes standing on path 4b: "
      f"survivors = {surv} -> {'PASS' if h_empty else 'FAIL'}")

    bind = sh["4b_binding"].value_counts()
    h_dd = bool(bind.get("DD", 0) > len(sh) / 2)
    P(f"H_DD     DD is the binding leg for a majority: {dict(bind)} -> "
      f"{'PASS' if h_dd else 'FAIL'}")

    med = float(sh["4b_minratio"].median())
    h_med = med < 1.0
    P(f"H_MEDIAN median min-ratio < 1: {med:.3f} -> {'PASS' if h_med else 'FAIL'}")

    s25 = CL[(CL.set == "SHELF") & (CL.rung == 25.0)]
    surv25 = int(s25["4b_clause"].sum())
    h_rung = surv == surv25
    P(f"H_RUNG   survivor count same at 10 and 25 bps: {surv} vs {surv25} -> "
      f"{'PASS' if h_rung else 'FAIL'}")
    P(f"         survivors @10bps: {sorted(sh[sh['4b_clause']].book)}")
    P(f"         survivors @25bps: {sorted(s25[s25['4b_clause']].book)}")

    # ---------------------------------------------------------------- rule 8 walk-forward
    P("")
    P("## Rule 8 walk-forward: choose on 2009-2016, evaluate on 2017+ untouched")
    wf = []
    for setname, bset in (("SHELF", books), ("GRID", GRID)):
        for nm, b in bset.items():
            px = PX[b["panel"]]
            nk = N_OFF[b["freq"]]
            per = []
            for k in range(nk):
                r, t = fast_run(px, b["W"], offset_mask(px.index, b["freq"], k))
                n = (r - t * RUNG_HEAD / 1e4).loc[start[b["panel"]]:]
                isr = n.loc[:"2016-12-31"]
                per.append((k, isr))
            ismets = {k: dict(zip(("CAGR", "Sharpe", "MaxDD"), fmet(v.values))) for k, v in per}
            k0 = ismets[0]
            spy_is = PX[b["panel"]]["SPY"].pct_change().fillna(0.0).loc[start[b["panel"]]:"2016-12-31"]
            sc, ss, sd = fmet(spy_is.values)
            h = len(per[0][1]) // 2
            mar = dict(H1=fsharpe(per[0][1].values[:h]) - fsharpe(spy_is.values[:h]),
                       H2=fsharpe(per[0][1].values[h:]) - fsharpe(spy_is.values[h:]),
                       DD=100.0 * (k0["MaxDD"] - DDCAP_FRAC * sd),
                       CAGR=100.0 * (k0["CAGR"] - CAGRFLOOR_FRAC * sc))
            statf = dict(H1=lambda m, v: fsharpe(v.values[:len(v) // 2]),
                         H2=lambda m, v: fsharpe(v.values[len(v) // 2:]),
                         DD=lambda m, v: 100.0 * m["MaxDD"],
                         CAGR=lambda m, v: 100.0 * m["CAGR"])
            ratios = {}
            for leg in ("H1", "H2", "DD", "CAGR"):
                vals = [statf[leg](ismets[k], v) for k, v in per]
                spread = max(vals) - min(vals)
                ratios[leg] = mar[leg] / spread if spread > 0 else np.inf
            wf.append(dict(set=setname, book=nm, panel=b["panel"], freq=b["freq"],
                           IS_CAGR=k0["CAGR"], IS_Sharpe=k0["Sharpe"], IS_MaxDD=k0["MaxDD"],
                           IS_minratio=min(ratios.values()),
                           IS_binding=min(ratios, key=lambda x: ratios[x]),
                           IS_pass4b=all(v > 0 for v in mar.values())))
    WF = pd.DataFrame(wf)
    full = CL[CL.rung == RUNG_HEAD].set_index(["set", "book"])
    WF = WF.join(full[["4b_minratio", "4b_clause", "pass4b_k0"]], on=["set", "book"])
    WF = WF.rename(columns={"4b_minratio": "FULL_minratio", "4b_clause": "FULL_clause",
                            "pass4b_k0": "FULL_pass4b"})
    for nm_ch, key, asc in (("IS-MINRATIO", "IS_minratio", False), ("IS-SHARPE", "IS_Sharpe", False)):
        for setname in ("SHELF", "GRID"):
            sub = WF[WF.set == setname]
            elig = sub[sub.IS_pass4b] if sub.IS_pass4b.any() else sub
            pick = elig.sort_values(key, ascending=asc).iloc[0]
            b = (books if setname == "SHELF" else GRID)[pick.book]
            px = PX[b["panel"]]
            r, t = fast_run(px, b["W"], offset_mask(px.index, b["freq"], 0))
            n = (r - t * RUNG_HEAD / 1e4).loc[start[b["panel"]]:]
            s = stats(n.values, n.index, OOS_START)
            sp = spy[b["panel"]][RUNG_HEAD]
            bs = v2[b["panel"]][RUNG_HEAD]
            oos_4b = (s["OOS_Sharpe"] > sp["OOS_Sharpe"]
                      and s["OOS_MaxDD"] >= DDCAP_FRAC * sp["OOS_MaxDD"]
                      and s["OOS_CAGR"] >= CAGRFLOOR_FRAC * sp["OOS_CAGR"])
            oos_4a = (s["OOS_Sharpe"] > bs["OOS_Sharpe"] and s["OOS_MaxDD"] >= bs["OOS_MaxDD"])
            P(f"  {nm_ch:12s} {setname:5s} picks {pick.book}  (IS min-ratio "
              f"{pick.IS_minratio:.2f}, binding {pick.IS_binding}, IS Sharpe {pick.IS_Sharpe:.3f})")
            P(f"      OOS 2017+  book {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.3f} / "
              f"{s['OOS_MaxDD']:.2%}   SPY {sp['OOS_CAGR']:.2%} / {sp['OOS_Sharpe']:.3f} / "
              f"{sp['OOS_MaxDD']:.2%}   RULES v2 {bs['OOS_CAGR']:.2%} / {bs['OOS_Sharpe']:.3f} / "
              f"{bs['OOS_MaxDD']:.2%}")
            P(f"      OOS 4b {'PASS' if oos_4b else 'FAIL'} | OOS 4a "
              f"{'PASS' if oos_4a else 'FAIL'} | full-sample 4b "
              f"{'PASS' if pick.FULL_pass4b else 'FAIL'} | full-sample CLAUSE "
              f"{'PASS' if pick.FULL_clause else 'FAIL'} (full min-ratio "
              f"{pick.FULL_minratio:.2f})")
            WF.loc[(WF.set == setname) & (WF.book == pick.book), f"pick_{nm_ch}"] = True
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    agree = int(((WF.IS_minratio >= 1.0) == (WF.FULL_minratio >= 1.0)).sum())
    h_wf = agree > len(WF) / 2
    P(f"H_WF     IS and FULL agree on the clause verdict for a majority of books: "
      f"{agree}/{len(WF)} -> {'PASS' if h_wf else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- GRID control
    P("## Control: the same clause on the never-selected GRID ladder (10 bps)")
    gg = CL[(CL.set == "GRID") & (CL.rung == RUNG_HEAD)]
    gp = gg[gg.pass4b_k0]
    P(f"  GRID books {len(gg)}; 4b passes at k=0: {len(gp)}; of those, clause survivors: "
      f"{int(gp['4b_clause'].sum())}")
    if len(gp):
        P(f"  GRID 4b-pass min-ratios: median {gp['4b_minratio'].median():.3f}, "
          f"max {gp['4b_minratio'].max():.3f}; binding legs {dict(gp['4b_binding'].value_counts())}")
    P("")

    # ---------------------------------------------------------------- summary
    P("## Summary")
    P(f"  Committed 4b passes priced: {len(sh)} (SHELF).  Pass 4b at their own published calendar "
      f"k=0: {int(sh.pass4b_k0.sum())}.")
    P(f"  Pass 4b at EVERY offset of their own cadence: "
      f"{int((sh.n_off_pass4b == sh.n_off).sum())} of {len(sh)}.")
    P(f"  Survive the margin/spread >= 1 clause: {surv} of {len(sh)}.")
    P(f"  Median min-ratio {med:.3f}; binding leg census {dict(bind)}.")
    P(f"  4a: passes at k=0 {int(sh.pass4a_k0.sum())}, clause survivors "
      f"{int(sh['4a_clause'].sum())}.")
    P(f"\n[{time.time() - t0:.1f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

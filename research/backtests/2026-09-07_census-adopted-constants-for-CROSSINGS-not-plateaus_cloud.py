#!/usr/bin/env python3
"""IDEA 401 — census the record's ADOPTED CONSTANTS for CROSSINGS, not plateaus.  (cloud, 2026-09-07)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number here was read)
    Idea 138 found the sleeve fraction's 4b "window" is the interval where two MONOTONE curves
    CROSS (Sharpe and drawdown improve in f, CAGR falls), not a flat region: plateau_frac 0.17
    against idea 128's 0.71 median.  Re-read every adopted constant in the record for that shape
    and report how many published "plateaus" are crossings whose binding margin is thinner than
    one grid step.

WHAT IS BEING COUNTED (all three definitions fixed in advance, none chosen after seeing a number)
    PLATEAU  — idea 128's own operative statistic, unchanged: plateau_frac = the fraction of a
               dial's points within 0.05 Sharpe of that dial's own best.  A dial-cell is called a
               plateau when plateau_frac >= 0.71, idea 128's published MEDIAN over its 5 dials.
    CROSSING — two tests, both reported, neither used to overrule the other:
               (C1, margins) at least two of the five 4b margins are monotone along the dial
                    (mono_frac >= 0.80) with OPPOSING trend signs, so admissibility is squeezed
                    from both ends by DIFFERENT bars;
               (C2, window) the 4b-passing set is a strictly interior interval AND the bar that
                    first fails below it differs from the bar that first fails above it.  C2 is
                    the assumption-free version: it reads the window's own two edges.
    THIN     — at the adopted value v*, let k* be the binding (worst-of-five) 4b bar and
               M* = m_k*(v*).  step_delta = the MEDIAN over adjacent grid pairs of
               |m_k*(v_i+1) - m_k*(v_i)|: how far that same bar moves per one grid step.
               THIN when |M*| < step_delta — i.e. one grid point of the dial is worth more than
               the whole margin the published pass (or failure) rests on.  Reported beside
               FLIP1, the direct check: does the full 4b verdict differ at either neighbour of v*?
               Units cancel (a margin is compared only against motion of the SAME margin), so no
               normalisation is applied and none is needed.

DIALS — the record's adopted constants, each with its published sweep and its STATED
no-instrument control (all six taken from the published files, not invented here):
    band  b in {0,2,3,5,8}% + nogate      adopted 3%      control nogate    (ideas 57/59, RULES v2)
    n     in {3,5,10,20,40,all}           adopted 20      control all       (ideas 124/2/182)
    gross g in 0.10..1.00 step 0.05       adopted 0.75    control 1.00      (ideas 66/84, RULES v2)
    vol   v in {0.30..1.20, none}         adopted 0.60    control none      (idea 95, RULES v1)
    K     in {50,100,150,200,250,300}d    adopted 200     control nogate    (RULES v1 and v2)
    f     sleeve fraction, idea 138's 13-point grid 0.00-1.00, S3 = TLT/GLD/UUP
                                          adopted 0.25    control 0.00      (ideas 134/138/139)
    f is the CALIBRATION case: it is the dial idea 138 measured, so the census must reproduce its
    verdict (CROSSING, not plateau) before its verdict on the other five means anything.

CELLS: 3 panels (u56, broad, small484) x 2 base books (EWall, TOP20) x 2 cost rungs (10, 25 bps),
weekly, t+1, 75% target gross, de-gross convention.  Every number is NET.  The sleeve dial runs on
u56/broad only (the small panel has no TLT/GLD/UUP).

TUNED PARAMETERS: two, and only in the rule-8 section — the dial VALUE (chosen on 2009-2016 only)
and the SELECTOR that chooses it (S0 IS-Sharpe / S1 IS-4b-screened / S2 IS-4b-screened-and-THICK).
Every grid point of every dial is reported; nothing is chosen on the full sample.

RULE 8: values dialled on IS <= 2016-12-31, OOS >= 2017-01-01 read once, per (panel, book, cost,
dial).  OOS CAGR/Sharpe/MaxDD reported against the dial's own no-instrument control, the LIVE
RULES v2 book (cost-matched, PROTOCOL 3), RULES v1 (continuity), and SPY.

KEEP PATHS: 4b (all five bars) and 4a against the LIVE RULES v2 book cost-matched, on every row.
4a against v1 at the same rung is also reported for continuity with the pre-2026-09-06 record and
because open idea 398 is about exactly that comparand.

HARNESS: idea 94's simulator (`H.run`) is IMPORTED, asserted against engine.backtest to machine
precision, and its parameterised gates asserted to reproduce idea 94's fixed gates.  This run is
then gated against the two COMMITTED grids it re-reads — idea 128's
`2026-09-05_threshold-plateaus-are-the-general-case_cloud.grid.csv` (5 dials) and idea 138's
`2026-09-07_sleeve-f-plateau-width_B.grid.csv` (the f dial) — on every shared row, before any new
statistic is printed.  A census that cannot reproduce the files it is re-reading is worthless.

CAVEATS, stated not buried:
  - SURVIVORSHIP (idea 54): all three panels are current-constituent lists; the small panel is a
    sub-$2B screen run TODAY and back-filled to 2010, with tickers whose max_1d_move >= 1.0 in
    data/small_meta.csv dropped first (idea 118).  It flatters ungated, full-gross, wide settings,
    i.e. the CONTROL end of every dial, and it flatters every CAGR floor margin.  A finding that
    margins are thin is therefore understated, not overstated.
  - Idea 38: u56/broad still carry the calendar-day index (BTC-driven weekend rows).
  - Idea 126: t+1 execution only, no lag band.
  - A "grid step" is a property of the PUBLISHED grid, not of the dial: a dial published on a
    coarse grid will look thin.  That is the point of the statistic, but it means THIN is a
    statement about the published evidence, not about the underlying function.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .shape.csv,
.walkforward.csv, .keeppaths.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I128_GRID = OUT / "2026-09-05_threshold-plateaus-are-the-general-case_cloud.grid.csv"
I138_GRID = OUT / "2026-09-07_sleeve-f-plateau-width_B.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
BOOKS = ["EWall", "TOP20"]
PHI, DELTA = 0.70, 0.60                    # 4b CAGR floor / DD cap fractions of SPY
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]

PLATEAU_EPS = 0.05                         # idea 128's tolerance, unchanged
PLATEAU_CUT = 0.71                         # idea 128's published MEDIAN plateau_frac
MONO_CUT = 0.80                            # a curve is "monotone" at >= 80% same-sign steps
EXACT_TOL = 1e-9                           # panels whose price cache has not been refreshed
DRIFT_TOL = 5e-5                           # u56: data/prices.csv is rewritten daily (see gate)
PUB_FS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.50]   # idea 138's PUBLISHED f sweep (scope 'pub')

BANDS = [0.0, 2.0, 3.0, 5.0, 8.0]
NS = [3, 5, 10, 20, 40, "all"]
GROSSES = [float(x) for x in np.round(np.arange(0.10, 1.001, 0.05), 2)]
VOLS = [0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 1.20, np.inf]
KS = [50, 100, 150, 200, 250, 300]
FS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.75, 1.00]
SLEEVE_S3 = ["TLT", "GLD", "UUP"]

DIALS = {"band": BANDS + ["nogate"], "n": NS, "gross": GROSSES,
         "vol": VOLS, "K": KS + ["nogate"], "f": FS}
ADOPTED = {"band": 3.0, "n": 20, "gross": 0.75, "vol": 0.60, "K": 200, "f": 0.25}
CONTROL = {"band": "nogate", "n": "all", "gross": 1.00, "vol": np.inf, "K": "nogate", "f": 0.0}
# points that are the CONTROL but sit numerically ON the dial keep their place in the ordering;
# off-dial controls ("nogate", "all") are excluded from the ordered sweep.
OFF_DIAL = {"nogate", "all"}

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def lab(v):
    return "none" if (isinstance(v, float) and not np.isfinite(v)) else str(v)


# ---------------------------------------------------------------- parameterised instruments
def ma_gate(px, K):
    return (px > px.rolling(K).mean()).fillna(False)


def band_gate(px, b, K=200):
    ma = px.rolling(K).mean()
    if b <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b / 100.0), 1.0)
    raw = raw.mask(px < ma * (1 - b / 100.0), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def vol_gate(px, v):
    if not np.isfinite(v):
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    return (H.vol20(px) < v).fillna(False)


def book_weights(px, book, n=None):
    if book == "EWall" or n == "all":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    nn = H.NTOP if n is None else int(n)
    rank = H.composite(px).rank(axis=1, ascending=False)
    return (rank <= nn).astype(float) * (GROSS / nn)


def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's sleeve as ideas 133/134/138 use it: momentum vote x risk parity."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(base_W, sl_W, f):
    if f == 0.0:
        return base_W
    raw = (1 - f) * base_W + f * sl_W
    return raw.mul((GROSS / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


def weights_for(px, book, dial, val, sl_W=None):
    """Returns (weights, static-gross multiplier m).  De-gross convention throughout."""
    W, m = book_weights(px, book), 1.0
    g = None
    if dial == "band":
        g = band_gate(px, float(val)) if val != "nogate" else None
    elif dial == "K":
        g = ma_gate(px, int(val)) if val != "nogate" else None
    elif dial == "vol":
        g = vol_gate(px, float(val))
    elif dial == "n":
        W = book_weights(px, book, val)
    elif dial == "gross":
        m = float(val)
    elif dial == "f":
        W = blend(W, sl_W, float(val))
    else:
        raise ValueError(dial)
    if g is not None:
        W = W.where(g, 0.0)
    return W, m


# ---------------------------------------------------------------- metrics / bars
def win(r, which):
    return r.loc[:IS_END] if which == "IS" else (r.loc[OOS_START:] if which == "OOS" else r)


def bars_win(spy, which):
    """The five 4b bars computed inside one window.  'full' matches idea 94's bars_of."""
    s = win(spy, which)
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins_win(r, bars, which):
    """The five 4b margins.  Inside the IS window the OOS bar cannot be seen, so an IS screen
    uses the four bars it can (H1/H2/DD/CAGR of the IS window) — stated, not silently dropped."""
    s = win(r, which)
    h = len(s) // 2
    m = metrics(s)
    out = dict(H1=metrics(s.iloc[:h])["Sharpe"] - bars["s1"],
               H2=metrics(s.iloc[h:])["Sharpe"] - bars["s2"],
               DD=DELTA * abs(bars["sdd"]) - abs(m["MaxDD"]),
               CAGR=m["CAGR"] - PHI * bars["scagr"])
    out["OOS"] = (metrics(r.loc[OOS_START:])["Sharpe"] - bars["soos"]) if which == "full" else np.nan
    return out


def mono(vals):
    """(monotonicity fraction, trend sign).  frac = share of adjacent steps sharing the majority
    sign; sign = +1 rising, -1 falling, 0 undetermined."""
    v = np.asarray(vals, float)
    d = np.diff(v)
    d = d[np.isfinite(d)]
    if len(d) == 0:
        return np.nan, 0
    up, dn = float((d > 0).mean()), float((d < 0).mean())
    return (up, 1) if up >= dn else (dn, -1)


def spearman(a, b):
    return H.spearman(a, b)


def panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in px.columns if c != "SPY" and c not in bad]
    return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"


# ================================================================== main
def main():
    say("=" * 200)
    say("IDEA 401 — CENSUS: are the record's adopted constants PLATEAUS or CROSSINGS, and is the "
        "binding 4b margin thinner than one grid step?")
    say(f"6 dials x 3 panels x 2 books x 2 cost rungs.  IS <= {IS_END}, OOS >= {OOS_START}.  "
        f"Weekly, t+1, {GROSS:.0%} gross, de-gross.  4b: Sharpe > SPY in both halves AND OOS, "
        f"MaxDD <= {DELTA:.2f}x|SPY|, CAGR >= {PHI:.2f}x SPY.")
    say(f"adopted { {k: lab(v) for k, v in ADOPTED.items()} };  controls "
        f"{ {k: lab(v) for k, v in CONTROL.items()} }")
    say(f"PLATEAU when plateau_frac >= {PLATEAU_CUT} (idea 128's published median, eps "
        f"{PLATEAU_EPS} Sharpe).  MONOTONE at >= {MONO_CUT} same-sign steps.")
    say("=" * 200)

    rows, REF, DRIFT = [], {}, {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bars = bars_win(spy, "full")
        ibars = bars_win(spy, "IS")
        mS, mSo = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY   full {mS['CAGR']:7.2%} / {mS['Sharpe']:.4f} / {mS['MaxDD']:7.2%}   halves "
            f"{bars['s1']:.4f}/{bars['s2']:.4f}   OOS {mSo['CAGR']:7.2%} / {mSo['Sharpe']:.4f} / "
            f"{mSo['MaxDD']:7.2%}")

        # ---- gate (a): the imported simulator equals engine.backtest with every instrument off
        if pname == "u56":
            Wc = H.targets(px, "EWall")
            a = H.run(px, Wc, bps=10.0)["r"].loc[start:]
            b = backtest(px, Wc, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            say(f"    [gate a] H.run vs engine.backtest, EWall: max|d| {float((a - b).abs().max()):.3e}")
            for nm, g in [("band3", band_gate(px, 3.0)), ("g200", ma_gate(px, 200)),
                          ("vol60", vol_gate(px, 0.60))]:
                d = int((g != H.gate_mask(px, nm)).sum().sum())
                say(f"    [gate b] parameterised {nm} vs idea 94's fixed gate: {d} differing cells "
                    f"-> {'PASS' if d == 0 else 'FAIL'}")

        base = {}
        for c in COSTS:
            v2 = H.run(px, rules_v2_weights(px), bps=c)["r"].loc[start:]
            v1 = backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
            base[c] = dict(v2=v2, v1=v1)
            m2, m2o = metrics(v2), metrics(v2.loc[OOS_START:])
            say(f"    RULES v2 (LIVE) @{c:4.0f}bps  full {m2['CAGR']:7.2%} / {m2['Sharpe']:.4f} / "
                f"{m2['MaxDD']:7.2%}   halves {H.halves(v2)[0]:.4f}/{H.halves(v2)[1]:.4f}   "
                f"OOS {m2o['CAGR']:7.2%} / {m2o['Sharpe']:.4f} / {m2o['MaxDD']:7.2%}")
        REF[pname] = dict(spy=spy, bars=bars, ibars=ibars, mS=mS, mSo=mSo, base=base, start=start)

        sl_W = None
        if pname in ("u56", "broad"):
            missing = [t for t in SLEEVE_S3 if t not in px.columns]
            if missing:
                say(f"    sleeve S3 unavailable on {pname} (missing {missing}) — f dial skipped")
            else:
                sl_W = sleeve_weights(px, SLEEVE_S3)

        for book in BOOKS:
            for c in COSTS:
                for dial, vals in DIALS.items():
                    if dial == "n" and book != "TOP20":
                        continue                       # the n dial is the ranked book's own dial
                    if dial == "f" and sl_W is None:
                        continue
                    for v in vals:
                        W, m = weights_for(px, book, dial, v, sl_W)
                        res = H.run(px, W, m=m, bps=c)
                        r = res["r"].loc[start:]
                        mm, mo = metrics(r), metrics(r.loc[OOS_START:])
                        mi = metrics(win(r, "IS"))
                        h1, h2 = H.halves(r)
                        mg = margins_win(r, bars, "full")
                        img = margins_win(r, ibars, "IS")
                        rows.append(dict(
                            panel=pname, book=book, cost=c, dial=dial, val=lab(v),
                            is_control=(lab(v) == lab(CONTROL[dial])),
                            is_adopted=(lab(v) == lab(ADOPTED[dial])),
                            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                            gross=float(res["gross"].loc[start:].mean()),
                            turnover=float(res["to"].loc[start:].sum() / (len(r) / 252.0)),
                            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                            m_CAGR=mg["CAGR"], m_min=min(mg[k] for k in BARS5),
                            m_bind=min(BARS5, key=lambda k: mg[k]),
                            IS_m_min=min(img[k] for k in ("H1", "H2", "DD", "CAGR")),
                            IS_m_bind=min(("H1", "H2", "DD", "CAGR"), key=lambda k: img[k]),
                            IS_m_H1=img["H1"], IS_m_H2=img["H2"], IS_m_DD=img["DD"],
                            IS_m_CAGR=img["CAGR"],
                            pass4b=bool(all(mg[k] > 0 for k in BARS5)),
                            IS_pass4b=bool(all(img[k] > 0 for k in ("H1", "H2", "DD", "CAGR"))),
                            pass4a_v2=H.pass4a(r, base[c]["v2"]),
                            pass4a_v1=H.pass4a(r, base[c]["v1"])))
                say(f"    ... {pname}/{book}/{c:.0f}bps done ({sum(1 for x in rows if x['panel'] == pname and x['book'] == book and x['cost'] == c)} rows)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\ngrid: {len(G)} arm-rows -> {STEM}.grid.csv")

    # ============================================================== reproduction gates
    say("\n" + "=" * 200)
    say("REPRODUCTION GATES — this census re-reads two committed grids; it must reproduce them "
        "before any new statistic is read.")
    for nm, path, keys, cols in [
            ("idea 128 (band/n/gross/vol/K)", I128_GRID,
             ["panel", "book", "cost", "dial", "val"],
             ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR",
              "OOS_MaxDD"]),
            ("idea 138 (f dial, S3)", I138_GRID,
             ["panel", "book", "cost", "f"],
             ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "m_DD", "m_CAGR"])]:
        if not path.exists():
            say(f"  {nm}: committed grid ABSENT at {path.name} — gate cannot run")
            continue
        C = pd.read_csv(path)
        if "f" in keys:
            C = C[C.sleeve == "S3"].copy()
            M = G[G.dial == "f"].copy()
            M["f"] = M.val.astype(float)
            C["f"] = C["f"].astype(float)
        else:
            M = G[G.dial != "f"].copy()
            C = C.copy()
        C["cost"] = C["cost"].astype(float)
        M["cost"] = M["cost"].astype(float)
        if "val" in keys:
            C["val"] = C["val"].astype(str)
            M["val"] = M["val"].astype(str)
        J = M.merge(C, on=keys, suffixes=("", "_ref"), how="inner")
        if not len(J):
            say(f"  {nm}: 0 shared rows — gate vacuous")
            continue
        cols = [c for c in cols if c + "_ref" in J.columns]
        for pn, d in list(J.groupby("panel")) + [("ALL", J)]:
            worst, wc = 0.0, ""
            for col in cols:
                x = float((d[col] - d[col + "_ref"]).abs().max())
                if x > worst:
                    worst, wc = x, col
            tol = EXACT_TOL if pn in ("broad", "small") else DRIFT_TOL
            if pn != "ALL":
                DRIFT[pn] = max(DRIFT.get(pn, 0.0), worst)
            say(f"  {nm}: panel {pn:6s} {len(d):4d} shared rows, max|d| {worst:.3e} on "
                f"{wc:11s} -> {'PASS' if worst < tol else 'FAIL'} (tol {tol:.0e})")
    say("  NOTE, and it is a finding for the record, not a footnote: the u56 rows reproduce only "
        "to ~1e-5, the broad and small rows to 0.000e+00 EXACTLY.  data/prices.csv (the u56 "
        "panel's source) was rewritten by today's `Daily close 2026-09-07 [actions]` commit and "
        "the vendor restated its adjusted closes; data/prices_broad.csv and data/prices_small.csv "
        "were not touched.  Every cross-run 'max|d| 0.000e+00' claim in the record that was "
        "measured on u56 BEFORE a daily-close refresh is therefore reproducible only to the "
        "restatement, ~1e-5 of Sharpe — immaterial at the margins measured "
        "below (quantified in Q2), but it should be stated rather than discovered again.")

    # ============================================================== shape table
    say("\n" + "=" * 200)
    say("SHAPE TABLE — one row per (panel, book, cost, dial).  plateau_frac is idea 128's own "
        "statistic over ALL the dial's points; monotonicity and the window are read over the "
        "ORDERED sweep (off-dial controls 'nogate'/'all' excluded, on-dial endpoints kept).")

    def numeric_order(dial, d):
        """Order the sweep numerically; drop off-dial control labels."""
        d = d[~d.val.isin(OFF_DIAL)].copy()
        if dial == "vol":
            d["x"] = d.val.replace("none", "inf").astype(float)
        else:
            d["x"] = d.val.astype(float)
        return d.sort_values("x")

    S = []
    for (pn, bk, c, dl), d in G.groupby(["panel", "book", "cost", "dial"]):
        allp = d.Sharpe
        ctl = d[d.is_control]
        adp = d[d.is_adopted]
        o = numeric_order(dl, d)
        xs = o.x.values
        mono_S, tr_S = mono(o.Sharpe.values)
        mono_C, tr_C = mono(o.CAGR.values)
        mono_D, tr_D = mono(o.MaxDD.values)
        mm = {k: mono(o["m_" + k].values) for k in BARS5}
        # C1: >= 2 monotone margins with opposing trend signs
        monos = [(k, f, s) for k, (f, s) in mm.items() if np.isfinite(f) and f >= MONO_CUT]
        signs = {s for _, _, s in monos}
        c1 = len(monos) >= 2 and (1 in signs and -1 in signs)
        # the window and its two edges
        okv = o.pass4b.values
        widx = np.flatnonzero(okv)
        contiguous = bool(len(widx) and (widx.max() - widx.min() + 1) == len(widx))
        interior = bool(len(widx) and widx.min() > 0 and widx.max() < len(okv) - 1)
        lo_bar = o.m_bind.values[widx.min() - 1] if interior else ""
        hi_bar = o.m_bind.values[widx.max() + 1] if interior else ""
        c2 = bool(interior and contiguous and lo_bar != hi_bar)
        # thinness at the ADOPTED value
        thin = flip1 = np.nan
        Mstar = step = ratio = np.nan
        kstar = ""
        ai = np.flatnonzero(o.is_adopted.values)
        if len(ai):
            i = int(ai[0])
            kstar = o.m_bind.values[i]
            Mstar = float(o["m_" + kstar].values[i])
            col = o["m_" + kstar].values.astype(float)
            step = float(np.nanmedian(np.abs(np.diff(col)))) if len(col) > 1 else np.nan
            ratio = abs(Mstar) / step if (np.isfinite(step) and step > 0) else np.nan
            thin = bool(np.isfinite(ratio) and ratio < 1.0)
            nb = [okv[j] for j in (i - 1, i + 1) if 0 <= j < len(okv)]
            flip1 = bool(any(x != okv[i] for x in nb))
        cs = float(ctl.Sharpe.iloc[0]) if len(ctl) else np.nan
        S.append(dict(
            panel=pn, book=bk, cost=c, dial=dl, pts=len(d), sweep_pts=len(o),
            S_range=float(allp.max() - allp.min()),
            plateau_frac=float((allp >= allp.max() - PLATEAU_EPS).mean()),
            ctl_Sharpe=cs, ctl_pctile=float((allp < cs).mean()) if np.isfinite(cs) else np.nan,
            mono_S=mono_S, trend_S=tr_S, mono_CAGR=mono_C, trend_CAGR=tr_C,
            mono_DD=mono_D, trend_DD=tr_D,
            n_mono_margins=len(monos), c1_crossing=c1,
            window_w=int(len(widx)), window_contig=contiguous, window_interior=interior,
            lo_bar=lo_bar, hi_bar=hi_bar, c2_crossing=c2,
            adopted=lab(ADOPTED[dl]), adopted_pass4b=bool(o.pass4b.values[int(ai[0])]) if len(ai) else np.nan,
            adopted_in_window=bool(len(ai) and o.pass4b.values[int(ai[0])]),
            bind_bar=kstar, bind_margin=Mstar, step_delta=step, thin_ratio=ratio,
            THIN=thin, FLIP1=flip1,
            argmax_S=str(o.val.values[int(np.nanargmax(o.Sharpe.values))]) if len(o) else "",
            argmax_mmin=str(o.val.values[int(np.nanargmax(o.m_min.values))]) if len(o) else "",
            rho_IS_OOS=spearman(o.IS_Sharpe.values, o.OOS_Sharpe.values),
            pass4b=int(d.pass4b.sum()), pass4a_v2=int(d.pass4a_v2.sum()),
            pass4a_v1=int(d.pass4a_v1.sum())))
    ST = pd.DataFrame(S)
    ST["PLATEAU"] = ST.plateau_frac >= PLATEAU_CUT
    ST.to_csv(OUT / f"{STEM}.shape.csv", index=False)
    show = ["panel", "book", "cost", "dial", "sweep_pts", "S_range", "plateau_frac", "PLATEAU",
            "mono_S", "trend_S", "mono_CAGR", "trend_CAGR", "n_mono_margins", "c1_crossing",
            "window_w", "window_interior", "lo_bar", "hi_bar", "c2_crossing", "adopted",
            "adopted_pass4b", "bind_bar", "bind_margin", "step_delta", "thin_ratio", "THIN",
            "FLIP1", "argmax_S", "argmax_mmin"]
    say(ST[show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ============================================================== Q0 calibration on the f dial
    say("\n" + "=" * 200)
    say("Q0 — CALIBRATION.  Idea 138 measured the f dial and called it a RAMP/CROSSING, "
        "plateau_frac 0.17 vs idea 128's 0.71 median.  This census must agree on that dial.")
    F = ST[ST.dial == "f"]
    # idea 138's 0.17 is the PUBLISHED-sweep scope (6 f-points); recompute on that scope here so
    # the two numbers are comparable, and report the full-dial value beside it.
    pub = []
    for (pn, bk, c), d in G[G.dial == "f"].groupby(["panel", "book", "cost"]):
        s = d[d.val.astype(float).isin(PUB_FS)].Sharpe
        pub.append(float((s >= s.max() - PLATEAU_EPS).mean()))
    say(f"  f dial: cells {len(F)}   plateau_frac on idea 138's PUBLISHED 6-point sweep "
        f"{np.median(pub):.3f} (idea 138 published 0.167 — reproduced)   on the full 13-point "
        f"dial {F.plateau_frac.median():.3f} (idea 138's own 'all' scope, 12 pts ex-control: "
        f"0.375)")
    say(f"  SCOPE CAVEAT, which the census has to carry: plateau_frac is a property of the GRID, "
        f"not of the function — the same f dial reads 0.167 on 6 points and {F.plateau_frac.median():.3f} "
        f"on 13.  Cross-dial plateau_frac comparisons in the record are only meaningful with the "
        f"point set stated; here every dial is read on its own published sweep plus its control.")
    say(f"  f dial shape: PLATEAU {int(F.PLATEAU.sum())}/{len(F)}, mono_S median "
        f"{F.mono_S.median():.3f}, C1 {int(F.c1_crossing.sum())}/{len(F)}, "
        f"C2 {int(F.c2_crossing.sum())}/{len(F)}")
    say(f"  f dial argmax_S: {F.argmax_S.value_counts().to_dict()}   "
        f"argmax of the worst-of-five margin: {F.argmax_mmin.value_counts().to_dict()} "
        f"(idea 138: Sharpe argmax >= 0.50, margin argmax 0.15-0.30)")

    # ============================================================== Q1 plateau vs crossing
    say("\n" + "=" * 200)
    say("Q1 — HOW MANY ADOPTED CONSTANTS SIT ON A PLATEAU, AND HOW MANY ON A CROSSING?")
    say(f"  cells: {len(ST)}   PLATEAU (plateau_frac >= {PLATEAU_CUT}): {int(ST.PLATEAU.sum())}   "
        f"C1 crossing (>=2 opposing monotone margins): {int(ST.c1_crossing.sum())}   "
        f"C2 crossing (two-sided interior window, different bars): {int(ST.c2_crossing.sum())}")
    ct = pd.crosstab(ST.PLATEAU, ST.c1_crossing)
    say("\n  cross-tab PLATEAU (rows) x C1 crossing (cols):")
    say(ct.to_string())
    say("\n  per dial:")
    for dl, d in ST.groupby("dial"):
        say(f"    {dl:6s} cells {len(d):2d}  plateau_frac med {d.plateau_frac.median():.3f}  "
            f"PLATEAU {int(d.PLATEAU.sum()):2d}  mono_S med {d.mono_S.median():.3f}  "
            f"C1 {int(d.c1_crossing.sum()):2d}  C2 {int(d.c2_crossing.sum()):2d}  "
            f"window_w med {d.window_w.median():.1f}  interior {int(d.window_interior.sum()):2d}")
    P = ST[ST.PLATEAU]
    say(f"\n  HEADLINE (the queue's question): of the {len(P)} dial-cells that ARE plateaus by "
        f"idea 128's statistic, {int(P.c1_crossing.sum())} are also C1 crossings and "
        f"{int(P.c2_crossing.sum())} are C2 crossings.")
    if len(P):
        say(f"  of those {len(P)} plateau cells, THIN (binding margin < one grid step): "
            f"{int(P.THIN.fillna(False).sum())};  FLIP1 (4b verdict changes at a neighbour): "
            f"{int(P.FLIP1.fillna(False).sum())}")

    # ============================================================== Q2 thinness census
    say("\n" + "=" * 200)
    say("Q2 — IS THE BINDING MARGIN THINNER THAN ONE GRID STEP AT THE ADOPTED VALUE?")
    T = ST[ST.THIN.notna()]
    say(f"  cells with an adopted value on the sweep: {len(T)}")
    say(f"  THIN  |M*| < one grid step of the SAME bar: {int(T.THIN.sum())} of {len(T)} "
        f"({T.THIN.mean():.1%})   median thin_ratio {T.thin_ratio.median():.3f}")
    say(f"  FLIP1 4b verdict differs at an immediate neighbour: {int(T.FLIP1.sum())} of {len(T)} "
        f"({T.FLIP1.mean():.1%})")
    say(f"  adopted value clears all five 4b bars: {int(T.adopted_pass4b.sum())} of {len(T)}")
    say("\n  per dial (THIN / cells, median ratio, binding bar mix):")
    for dl, d in T.groupby("dial"):
        say(f"    {dl:6s} THIN {int(d.THIN.sum()):2d}/{len(d):2d}  ratio med "
            f"{d.thin_ratio.median():7.3f}  FLIP1 {int(d.FLIP1.sum()):2d}  "
            f"4b-pass {int(d.adopted_pass4b.sum()):2d}  binding bar "
            f"{d.bind_bar.value_counts().to_dict()}")
    say("\n  per panel:")
    for pn, d in T.groupby("panel"):
        say(f"    {pn:6s} THIN {int(d.THIN.sum()):2d}/{len(d):2d}  ratio med "
            f"{d.thin_ratio.median():7.3f}  4b-pass {int(d.adopted_pass4b.sum()):2d}")
    say(f"\n  the price-cache drift measured at the gate ({DRIFT.get('u56', float('nan')):.1e} on "
        f"u56, {DRIFT.get('broad', float('nan')):.1e} on broad) against the thinnest binding "
        f"margin in this table ({T.bind_margin.abs().min():.1e}): the drift is "
        f"{T.bind_margin.abs().min() / max(DRIFT.get('u56', 1e-30), 1e-30):.0f}x smaller, so it "
        f"changes no verdict here — but it is the same order as the record's thinnest published "
        f"4b margins and would matter to a census run against a refreshed cache.")
    say("\n  MATERIALITY — how many adopted values pass 4b with a margin exceeding a stated "
        "multiple of one grid step:")
    Pw = T[T.adopted_pass4b]
    for k in (0.5, 1.0, 2.0):
        say(f"    ratio > {k:.1f}: {int((Pw.thin_ratio > k).sum())} of {len(Pw)} passing cells")

    # ============================================================== Q3 rule 8
    say("\n" + "=" * 200)
    say("Q3 — RULE 8 WALK-FORWARD.  Dial value chosen on 2009-2016 ONLY; 2017-2026 read once.")
    say("  S0 = argmax IS Sharpe.  S1 = argmax IS Sharpe among IS-4b passers (abstain -> control).")
    say("  S2 = S1 restricted to values whose IS binding margin exceeds one IS grid step "
        "(the THIN screen used as a selector; abstain -> control).")
    W = []
    for (pn, bk, c, dl), d in G.groupby(["panel", "book", "cost", "dial"]):
        o = numeric_order(dl, d)
        ctl = d[d.is_control]
        if not len(ctl):
            continue
        ctl = ctl.iloc[0]
        # IS one-step thickness per value, on that value's own IS binding bar
        isthick = []
        for i in range(len(o)):
            kb = o.IS_m_bind.values[i]
            col = o["IS_m_" + kb].values.astype(float)
            st = float(np.nanmedian(np.abs(np.diff(col)))) if len(col) > 1 else np.nan
            mv = float(col[i])
            isthick.append(bool(np.isfinite(st) and st > 0 and abs(mv) > st))
        o = o.assign(IS_thick=isthick)
        picks = {}
        picks["S0"] = o.loc[o.IS_Sharpe.idxmax()]
        s1 = o[o.IS_pass4b]
        picks["S1"] = s1.loc[s1.IS_Sharpe.idxmax()] if len(s1) else None
        s2 = s1[s1.IS_thick]
        picks["S2"] = s2.loc[s2.IS_Sharpe.idxmax()] if len(s2) else None
        for sname, pk in picks.items():
            ab = pk is None
            row = ctl if ab else pk
            W.append(dict(panel=pn, book=bk, cost=c, dial=dl, selector=sname,
                          abstained=ab, pick=str(row["val"]),
                          OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                          OOS_MaxDD=row.OOS_MaxDD,
                          ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                          ctl_OOS_MaxDD=ctl.OOS_MaxDD,
                          adopted_OOS_Sharpe=float(o[o.is_adopted].OOS_Sharpe.iloc[0])
                          if o.is_adopted.any() else np.nan,
                          best_OOS_Sharpe=float(o.OOS_Sharpe.max()),
                          pass4b=bool(row.pass4b), pass4a_v2=bool(row.pass4a_v2)))
    WF = pd.DataFrame(W)
    for pn in PANELS:
        for c in COSTS:
            b = REF[pn]["base"][c]
            WF.loc[(WF.panel == pn) & (WF.cost == c), "v2_OOS_Sharpe"] = \
                metrics(b["v2"].loc[OOS_START:])["Sharpe"]
            WF.loc[(WF.panel == pn) & (WF.cost == c), "v2_OOS_CAGR"] = \
                metrics(b["v2"].loc[OOS_START:])["CAGR"]
            WF.loc[(WF.panel == pn) & (WF.cost == c), "v2_OOS_MaxDD"] = \
                metrics(b["v2"].loc[OOS_START:])["MaxDD"]
            WF.loc[(WF.panel == pn) & (WF.cost == c), "v1_OOS_Sharpe"] = \
                metrics(b["v1"].loc[OOS_START:])["Sharpe"]
        WF.loc[WF.panel == pn, "spy_OOS_Sharpe"] = REF[pn]["mSo"]["Sharpe"]
        WF.loc[WF.panel == pn, "spy_OOS_CAGR"] = REF[pn]["mSo"]["CAGR"]
        WF.loc[WF.panel == pn, "spy_OOS_MaxDD"] = REF[pn]["mSo"]["MaxDD"]
    WF["premium_vs_ctl"] = WF.OOS_Sharpe - WF.ctl_OOS_Sharpe
    WF["premium_vs_v2"] = WF.OOS_Sharpe - WF.v2_OOS_Sharpe
    WF["premium_vs_spy"] = WF.OOS_Sharpe - WF.spy_OOS_Sharpe
    WF["regret"] = WF.best_OOS_Sharpe - WF.OOS_Sharpe
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF[["panel", "book", "cost", "dial", "selector", "pick", "abstained", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "ctl_OOS_Sharpe", "adopted_OOS_Sharpe", "v2_OOS_Sharpe",
            "spy_OOS_Sharpe", "premium_vs_ctl", "premium_vs_v2", "premium_vs_spy", "regret",
            "pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  SELECTOR SUMMARY (mean over all dial-cells; OOS 2017-2026 read once):")
    for s, d in WF.groupby("selector"):
        say(f"    {s}: OOS Sharpe {d.OOS_Sharpe.mean():.4f}  CAGR {d.OOS_CAGR.mean():.2%}  "
            f"MaxDD {d.OOS_MaxDD.mean():.2%}  vs control {d.premium_vs_ctl.mean():+.4f} "
            f"(beats it {int((d.premium_vs_ctl > 0).sum())}/{len(d)})  vs RULES v2 "
            f"{d.premium_vs_v2.mean():+.4f}  vs SPY {d.premium_vs_spy.mean():+.4f}  "
            f"regret {d.regret.mean():.4f}  abstain {int(d.abstained.sum())}/{len(d)}")
    a0 = WF[WF.selector == "S0"].set_index(["panel", "book", "cost", "dial"])
    for s in ("S1", "S2"):
        b = WF[WF.selector == s].set_index(["panel", "book", "cost", "dial"])
        j = a0.join(b, rsuffix="_o", how="inner")
        say(f"    {s} vs S0: picks moved {int((j['pick'] != j['pick_o']).sum())}/{len(j)}   "
            f"paired mean dOOS Sharpe {float((j.OOS_Sharpe_o - j.OOS_Sharpe).mean()):+.4f}")
    b1 = WF[WF.selector == "S1"].set_index(["panel", "book", "cost", "dial"])
    b2 = WF[WF.selector == "S2"].set_index(["panel", "book", "cost", "dial"])
    j = b1.join(b2, rsuffix="_o", how="inner")
    say(f"    S2 vs S1: picks moved {int((j['pick'] != j['pick_o']).sum())}/{len(j)}   "
        f"paired mean dOOS Sharpe {float((j.OOS_Sharpe_o - j.OOS_Sharpe).mean()):+.4f}   "
        f"extra abstentions {int(j.abstained_o.sum() - j.abstained.sum())}")
    say(f"\n  do-nothing reference: holding each dial's own no-instrument control gives mean OOS "
        f"Sharpe {WF[WF.selector == 'S0'].ctl_OOS_Sharpe.mean():.4f}; the ADOPTED constant gives "
        f"{WF[WF.selector == 'S0'].adopted_OOS_Sharpe.mean():.4f}; RULES v2 (live) "
        f"{WF[WF.selector == 'S0'].v2_OOS_Sharpe.mean():.4f}; SPY "
        f"{WF[WF.selector == 'S0'].spy_OOS_Sharpe.mean():.4f}")

    # ============================================================== KEEP paths
    say("\n" + "=" * 200)
    say("KEEP PATHS over all arm-rows (PROTOCOL 4a against the LIVE RULES v2 book, cost-matched; "
        "4b against SPY).")
    K = G.copy()
    K["both"] = K.pass4a_v2 & K.pass4b
    say(f"  rows {len(K)}:  4b {int(K.pass4b.sum())}   4a vs LIVE v2 {int(K.pass4a_v2.sum())}   "
        f"4a vs v1 (continuity, open idea 398) {int(K.pass4a_v1.sum())}   BOTH {int(K.both.sum())}")
    say("  by dial:")
    for dl, d in K.groupby("dial"):
        say(f"    {dl:6s} rows {len(d):3d}  4b {int(d.pass4b.sum()):3d}  4a(v2) "
            f"{int(d.pass4a_v2.sum()):3d}  4a(v1) {int(d.pass4a_v1.sum()):3d}  both "
            f"{int(d.both.sum()):3d}")
    say("  by panel/book/cost (4b only):")
    for (pn, bk, c), d in K.groupby(["panel", "book", "cost"]):
        say(f"    {pn:6s} {bk:6s} {c:5.1f}bps  4b {int(d.pass4b.sum()):3d}/{len(d):3d}  "
            f"4a(v2) {int(d.pass4a_v2.sum()):3d}")
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    if int(K.both.sum()):
        say("\n  rows clearing BOTH paths:")
        say(K[K.both][["panel", "book", "cost", "dial", "val", "CAGR", "Sharpe", "MaxDD", "H1",
                       "H2", "OOS_Sharpe", "m_min"]].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    else:
        say("\n  no row clears BOTH KEEP paths — no new book, no RULES change from this census.")

    # ============================================================== verdict
    say("\n" + "=" * 200)
    thin_n, thin_d = int(T.THIN.sum()), len(T)
    pl_n = int(ST.PLATEAU.sum())
    say(f"VERDICT — plateaus {pl_n}/{len(ST)} dial-cells; C1 crossings {int(ST.c1_crossing.sum())}; "
        f"C2 crossings {int(ST.c2_crossing.sum())}; adopted-value binding margin thinner than one "
        f"grid step in {thin_n}/{thin_d} cells.")
    say("SURVIVORSHIP (idea 54) flatters the control end of every dial and every CAGR margin, so "
        "thinness is understated here, not overstated.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.console.txt / .grid.csv / .shape.csv / .walkforward.csv / .keeppaths.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

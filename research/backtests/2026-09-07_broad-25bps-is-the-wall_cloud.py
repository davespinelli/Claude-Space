#!/usr/bin/env python3
"""IDEA 137 — is broad@25bps a TURNOVER wall or an H2-REGIME wall?   (cloud, 2026-09-07)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number here was read)
    Idea 134 found broad@25bps admits 0 of 442 arm-rows and 0 of 130 ladder points at any sleeve
    fraction, and that the failures there are SHARPE bars (H2 0.791, OOS 0.861 on the best member)
    rather than the CAGR floor or the DD cap, while the same book clears everything at 10 bps.
    Decompose whether the wall is TURNOVER (12.2x/yr on broad vs 8.8x on u56) or the panel's H2
    REGIME, by holding turnover fixed across panels.

THE TEST (fixed in advance)
    D1  EXACT COST DECOMPOSITION.  With no state machine active (no stop, no DD control, no entry
        budget) the simulator's holdings and turnover are independent of the cost rung, so
            r(c) = r_gross - turnover * c / 1e4
        holds to machine precision.  This is ASSERTED against a re-run at 25 bps before it is used.
        Every cost rung is then read off ONE simulation, and the u56-minus-broad Sharpe gap at
        25 bps splits EXACTLY into
            gap(25) = gap(0)                      <- the REGIME term (cost-free)
                    + [gap(25) - gap(0)]          <- the COST-RESPONSE term (turnover)
        reported separately for full-sample, H1, H2 and OOS Sharpe — the bars idea 134 says fail.
    D2  MATCHED TURNOVER (the queue's own instruction).  Turnover is dialled with two instruments,
        both continuous or near-continuous and both reported at every point:
            cadence  in {D, W, M, Q}                    (the structural dial)
            lambda   in {1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10}
                     target_t = lambda * W_t + (1-lambda) * target_{t-1}: partial rebalancing,
                     which scales turnover smoothly without changing the book's selection.
        For each (panel, book, f) the (cadence, lambda) whose realised annual turnover is closest
        to a COMMON target T* is selected, T* being the u56 weekly/lambda=1 book's own turnover —
        stated in advance, not chosen from the results.  The panels are then compared at 25 bps at
        MATCHED turnover.  If broad clears 4b there, the wall is turnover; if it does not, the wall
        is the panel.
    D3  MATCHED COST DRAG.  The second equalisation: give each panel the rung that equates
        turnover x bps (broad's equivalent of u56 @25bps is 25 * to_u56 / to_broad).  Reported
        beside D2 because the two answer the same question with different arithmetic.
    D4  THE H2 REGIME, read directly: each panel's SPY H2 bar, and each book's H2 Sharpe at ZERO
        cost.  A wall that is already there at 0 bps is not a cost wall.

TUNED PARAMETERS: two — cadence and lambda.  Both are swept in full and every grid point is
reported; the rule-8 section is the only place either is CHOSEN, and it chooses on 2009-2016 only.
Cost rungs, panels, books and the sleeve fraction are reported axes, not tuned.

GRID: 3 panels (u56, broad, small484) x 2 base books (EWall, TOP20) x f in {0.00, 0.25} (idea
139's sleeve candidate; u56/broad only, S3 = TLT/GLD/UUP) x 4 cadences x 7 lambdas, read at cost
rungs {0, 5, 10, 15, 25, 50} bps.  75% target gross, t+1, de-gross convention.  Every number NET.

RULE 8: (cadence, lambda) chosen on IS <= 2016-12-31 by IS Sharpe at the 25 bps rung, OOS >=
2017-01-01 read once.  OOS CAGR/Sharpe/MaxDD reported against the LIVE RULES v2 book (cost-matched,
PROTOCOL 3), RULES v1 (continuity) and SPY.

KEEP PATHS: 4b (all five bars) and 4a against the LIVE RULES v2 book cost-matched, on every row.

HARNESS: idea 94's simulator (`H.run`) is IMPORTED and asserted against engine.backtest.  The run
is gated against idea 138's COMMITTED `2026-09-07_sleeve-f-plateau-width_B.grid.csv` on every
shared row (weekly, lambda=1, f in {0.00, 0.25}, S3, 10/25 bps) before any new number is read.

CAVEATS, stated not buried:
  - SURVIVORSHIP (idea 54): all three panels are current-constituent lists; the small panel is a
    sub-$2B screen run TODAY and back-filled to 2010, with tickers whose max_1d_move >= 1.0 in
    data/small_meta.csv dropped first (idea 118).  It flatters low-turnover, buy-and-hold settings,
    i.e. exactly the end of the turnover dial that D2 moves toward, so a finding that matched
    turnover does NOT save broad is understated, not overstated.
  - Idea 38: u56/broad still carry the calendar-day index (BTC-driven weekend rows).
  - Idea 126: t+1 execution only, no lag band.
  - lambda smoothing is an INSTRUMENT as well as a turnover dial: it changes the book's path, not
    only its trading.  D3 (matched cost drag) is reported precisely because it changes nothing
    about the book at all, and the two equalisations are read together.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .decomp.csv,
.matched.csv, .walkforward.csv, .keeppaths.csv next to itself.
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

STEM = "2026-09-07_broad-25bps-is-the-wall_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I138_GRID = OUT / "2026-09-07_sleeve-f-plateau-width_B.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")

GROSS = H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]

PANELS = ["u56", "broad", "small"]
BOOKS = ["EWall", "TOP20"]
FS = [0.00, 0.25]                              # idea 139's candidate sleeve fraction and its control
SLEEVE_S3 = ["TLT", "GLD", "UUP"]
CADENCES = ["D", "W", "M", "Q"]                # tuned parameter 1 — ALL reported
LAMBDAS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10]   # tuned parameter 2 — ALL reported
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]     # reported axis, not tuned
WALL_RUNG = 25.0                               # the rung the queue names
EXACT_TOL = 1e-9                               # panels whose price cache is untouched
DRIFT_TOL = 5e-5                               # u56: data/prices.csv is rewritten daily

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ---------------------------------------------------------------- books
def book_weights(px, book):
    if book == "EWall":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    rank = H.composite(px).rank(axis=1, ascending=False)
    return (rank <= H.NTOP).astype(float) * (GROSS / H.NTOP)


def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(base_W, sl_W, f):
    if f == 0.0:
        return base_W
    raw = (1 - f) * base_W + f * sl_W
    return raw.mul((GROSS / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


def smooth(W, lam):
    """Partial rebalancing: target_t = lam*W_t + (1-lam)*target_{t-1}.  lam=1 is the raw book.
    The gross is restored each day so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    tgt = W.sum(axis=1)
    return S.mul((tgt / g).fillna(0.0), axis=0).fillna(0.0)


# ---------------------------------------------------------------- metrics
def win(r, which):
    return r.loc[:IS_END] if which == "IS" else (r.loc[OOS_START:] if which == "OOS" else r)


def bars_of(spy):
    h = len(spy) // 2
    m = metrics(spy)
    return dict(s1=metrics(spy.iloc[:h])["Sharpe"], s2=metrics(spy.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def margins(r, bars):
    h = len(r) // 2
    m = metrics(r)
    return dict(H1=metrics(r.iloc[:h])["Sharpe"] - bars["s1"],
                H2=metrics(r.iloc[h:])["Sharpe"] - bars["s2"],
                OOS=metrics(r.loc[OOS_START:])["Sharpe"] - bars["soos"],
                DD=DELTA * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * bars["scagr"])


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


def interp_to(df, col_x, col_y, target):
    """Linear interpolation of col_y against a MONOTONE-sorted col_x at x = target.  Returns
    (value, bracketed?) — never extrapolates silently; out-of-range clamps and flags."""
    d = df.sort_values(col_x)
    x, y = d[col_x].values.astype(float), d[col_y].values.astype(float)
    if target <= x[0]:
        return float(y[0]), False
    if target >= x[-1]:
        return float(y[-1]), False
    return float(np.interp(target, x, y)), True


# ================================================================== main
def main():
    say("=" * 200)
    say("IDEA 137 — is the broad@25bps wall TURNOVER or the panel's H2 REGIME?")
    say(f"3 panels x {len(BOOKS)} books x f{FS} x {len(CADENCES)} cadences x {len(LAMBDAS)} "
        f"lambdas, read at rungs {RUNGS} bps.  IS <= {IS_END}, OOS >= {OOS_START}.  "
        f"{GROSS:.0%} gross, t+1, de-gross.")
    say(f"4b: Sharpe > SPY in both halves AND OOS, MaxDD <= {DELTA:.2f}x|SPY|, "
        f"CAGR >= {PHI:.2f}x SPY.  4a vs the LIVE RULES v2 book, cost-matched.")
    say("=" * 200)

    rows, REF = [], {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bars = bars_of(spy)
        mS, mSo = metrics(spy), metrics(spy.loc[OOS_START:])
        h = len(spy) // 2
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY   full {mS['CAGR']:7.2%} / {mS['Sharpe']:.4f} / {mS['MaxDD']:7.2%}   halves "
            f"{bars['s1']:.4f}/{bars['s2']:.4f}   OOS {mSo['CAGR']:7.2%} / {mSo['Sharpe']:.4f} / "
            f"{mSo['MaxDD']:7.2%}")

        base = {}
        for c in RUNGS:
            v2 = H.run(px, rules_v2_weights(px), bps=c)["r"].loc[start:]
            v1 = backtest(px, rules_v1_weights(px), cost_bps=c, freq="W")["returns"].loc[start:]
            base[c] = dict(v2=v2, v1=v1)
        for c in (10.0, 25.0):
            m2, m2o = metrics(base[c]["v2"]), metrics(base[c]["v2"].loc[OOS_START:])
            say(f"    RULES v2 (LIVE) @{c:4.0f}bps  full {m2['CAGR']:7.2%} / {m2['Sharpe']:.4f} / "
                f"{m2['MaxDD']:7.2%}   halves {H.halves(base[c]['v2'])[0]:.4f}/"
                f"{H.halves(base[c]['v2'])[1]:.4f}   OOS {m2o['CAGR']:7.2%} / {m2o['Sharpe']:.4f}")
        REF[pname] = dict(spy=spy, bars=bars, mS=mS, mSo=mSo, base=base, start=start,
                          spy_h1=metrics(spy.iloc[:h])["Sharpe"],
                          spy_h2=metrics(spy.iloc[h:])["Sharpe"])

        sl_W = None
        if pname in ("u56", "broad"):
            missing = [t for t in SLEEVE_S3 if t not in px.columns]
            sl_W = None if missing else sleeve_weights(px, SLEEVE_S3)
            if missing:
                say(f"    sleeve S3 unavailable on {pname} (missing {missing}) — f=0.25 skipped")

        # ---- gate (a): imported simulator == engine.backtest with everything off
        if pname == "u56":
            Wc = book_weights(px, "EWall")
            a = H.run(px, Wc, bps=10.0)["r"].loc[start:]
            b = backtest(px, Wc, cost_bps=10.0, freq="W")["returns"].loc[start:]
            say(f"    [gate a] H.run vs engine.backtest, EWall weekly: max|d| "
                f"{float((a - b).abs().max()):.3e}")

        for book in BOOKS:
            bw = book_weights(px, book)
            for f in FS:
                if f > 0 and sl_W is None:
                    continue
                W0 = blend(bw, sl_W, f)
                for lam in LAMBDAS:
                    Wl = smooth(W0, lam)
                    for cad in CADENCES:
                        res = H.run(px, Wl, bps=0.0, freq=cad)
                        rg = res["r"].loc[start:]              # gross-of-cost returns
                        to = res["to"].loc[start:]
                        yrs = len(rg) / 252.0
                        to_yr = float(to.sum() / yrs)
                        # ---- gate (b): the exact cost decomposition, asserted once per panel
                        if pname == "u56" and book == "EWall" and f == 0.0 and lam == 1.0 and cad == "W":
                            chk = H.run(px, Wl, bps=WALL_RUNG, freq=cad)["r"].loc[start:]
                            der = rg - to * WALL_RUNG / 1e4
                            say(f"    [gate b] derived r(25bps) vs simulated: max|d| "
                                f"{float((der - chk).abs().max()):.3e}")
                        for c in RUNGS:
                            r = rg - to * c / 1e4
                            mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(win(r, "IS"))
                            h1, h2 = H.halves(r)
                            mg = margins(r, bars)
                            rows.append(dict(
                                panel=pname, book=book, f=f, lam=lam, cad=cad, cost=c,
                                turnover=to_yr, gross=float(res["gross"].loc[start:].mean()),
                                CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                H1=h1, H2=h2, IS_Sharpe=mi["Sharpe"],
                                OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                                m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                                m_CAGR=mg["CAGR"], m_min=min(mg[k] for k in BARS5),
                                m_bind=min(BARS5, key=lambda k: mg[k]),
                                pass4b=bool(all(mg[k] > 0 for k in BARS5)),
                                pass4a_v2=H.pass4a(r, base[c]["v2"]),
                                pass4a_v1=H.pass4a(r, base[c]["v1"])))
                say(f"    ... {pname}/{book}/f={f:.2f} done")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\ngrid: {len(G)} arm-rows -> {STEM}.grid.csv")

    # ============================================================== reproduction gate
    say("\n" + "=" * 200)
    say("REPRODUCTION GATE — idea 138's committed grid (weekly, lambda=1, S3, f in {0.00, 0.25}, "
        "10/25 bps).")
    if I138_GRID.exists():
        C = pd.read_csv(I138_GRID)
        C = C[(C.sleeve == "S3") & (C.f.isin(FS))].copy()
        M = G[(G.cad == "W") & (G.lam == 1.0) & (G.cost.isin([10.0, 25.0]))].copy()
        J = M.merge(C, on=["panel", "book", "cost", "f"], suffixes=("", "_ref"), how="inner")
        worst, wc = 0.0, ""
        for col in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR",
                    "OOS_MaxDD", "m_DD", "m_CAGR", "m_H1", "m_H2", "m_OOS", "m_min"]:
            if col + "_ref" in J.columns:
                d = float((J[col] - J[col + "_ref"]).abs().max())
                if d > worst:
                    worst, wc = d, col
        for pn, d in list(J.groupby("panel")) + [("ALL", J)]:
            w2, c2 = 0.0, ""
            for col in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe",
                        "OOS_CAGR", "OOS_MaxDD", "m_DD", "m_CAGR", "m_H1", "m_H2", "m_OOS",
                        "m_min"]:
                if col + "_ref" in d.columns:
                    x = float((d[col] - d[col + "_ref"]).abs().max())
                    if x > w2:
                        w2, c2 = x, col
            tol = EXACT_TOL if pn in ("broad", "small") else DRIFT_TOL
            say(f"  panel {pn:6s} {len(d):3d} shared rows, max|d| {w2:.3e} on {c2:11s} -> "
                f"{'PASS' if w2 < tol else 'FAIL'} (tol {tol:.0e})")
        say(f"  pass4b agreement: {int((J.pass4b == J.pass4b_ref).sum())}/{len(J)}")
        say("  The u56 rows reproduce only to ~1e-5 while the broad rows reproduce EXACTLY: "
            "data/prices.csv (the u56 panel's source) was rewritten by today's `Daily close "
            "2026-09-07 [actions]` commit and the vendor restated its adjusted closes; "
            "data/prices_broad.csv was not touched.  Immaterial here (every margin below is "
            ">= 1e-3) but it is why the tolerance is split by panel.")
    else:
        say("  committed grid ABSENT — gate cannot run")

    # ============================================================== W0 the wall itself
    say("\n" + "=" * 200)
    say("W0 — DOES THE WALL REPRODUCE?  Reference setting: weekly, lambda=1 (no smoothing), the "
        "book idea 134 priced.")
    ref = G[(G.cad == "W") & (G.lam == 1.0)]
    say("  4b passes and the binding bar, by panel x cost rung:")
    for pn, d in ref.groupby("panel"):
        line = []
        for c in RUNGS:
            dc = d[d.cost == c]
            line.append(f"{c:.0f}bps {int(dc.pass4b.sum())}/{len(dc)}")
        say(f"    {pn:6s} " + "   ".join(line))
    say("\n  binding bar mix at the wall rung (25 bps), weekly/lambda=1:")
    for pn, d in ref[ref.cost == WALL_RUNG].groupby("panel"):
        say(f"    {pn:6s} {d.m_bind.value_counts().to_dict()}   best m_min {d.m_min.max():+.4f} "
            f"(binding {d.loc[d.m_min.idxmax(), 'm_bind']})   turnover "
            f"{d.turnover.min():.2f}-{d.turnover.max():.2f}x/yr")
    say("\n  idea 134's named numbers (best broad member @25bps: H2 0.791, OOS 0.861):")
    bb = ref[(ref.panel == "broad") & (ref.cost == WALL_RUNG)]
    if len(bb):
        best = bb.loc[bb.m_min.idxmax()]
        say(f"    best broad@25 here: {best.book}/f={best.f:.2f}  CAGR {best.CAGR:.2%} Sharpe "
            f"{best.Sharpe:.4f} MaxDD {best.MaxDD:.2%}  H1 {best.H1:.4f} H2 {best.H2:.4f} "
            f"OOS {best.OOS_Sharpe:.4f}   SPY bars H1 {REF['broad']['spy_h1']:.4f} H2 "
            f"{REF['broad']['spy_h2']:.4f} OOS {REF['broad']['mSo']['Sharpe']:.4f}")

    # ============================================================== D1 exact cost decomposition
    say("\n" + "=" * 200)
    say("D1 — EXACT DECOMPOSITION of the u56-minus-broad Sharpe gap at 25 bps.")
    say("     gap(25) = gap(0) [REGIME] + (gap(25) - gap(0)) [COST RESPONSE].  Identity is exact.")
    D = []
    key = ["book", "f", "lam", "cad"]
    for k, d in G.groupby(key):
        u = d[d.panel == "u56"]
        b = d[d.panel == "broad"]
        if not len(u) or not len(b):
            continue
        row = dict(zip(key, k))
        for metric in ["Sharpe", "H1", "H2", "OOS_Sharpe"]:
            g0 = float(u[u.cost == 0.0][metric].iloc[0] - b[b.cost == 0.0][metric].iloc[0])
            g25 = float(u[u.cost == WALL_RUNG][metric].iloc[0] - b[b.cost == WALL_RUNG][metric].iloc[0])
            row[f"{metric}_gap0"] = g0
            row[f"{metric}_gap25"] = g25
            row[f"{metric}_cost_term"] = g25 - g0
            row[f"{metric}_regime_share"] = (g0 / g25) if abs(g25) > 1e-12 else np.nan
        row["to_u56"] = float(u.turnover.iloc[0])
        row["to_broad"] = float(b.turnover.iloc[0])
        row["to_ratio"] = row["to_broad"] / row["to_u56"] if row["to_u56"] else np.nan
        D.append(row)
    DD_ = pd.DataFrame(D)
    DD_.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    say(DD_[["book", "f", "lam", "cad", "to_u56", "to_broad", "to_ratio",
             "Sharpe_gap0", "Sharpe_gap25", "Sharpe_cost_term", "Sharpe_regime_share",
             "H2_gap0", "H2_gap25", "H2_cost_term", "H2_regime_share",
             "OOS_Sharpe_gap0", "OOS_Sharpe_gap25", "OOS_Sharpe_cost_term",
             "OOS_Sharpe_regime_share"]].to_string(index=False,
                                                   float_format=lambda x: f"{x:.4f}"))
    say("\n  SUMMARY over all (book, f, lambda, cadence) cells — how much of the 25 bps gap is "
        "already there at ZERO cost:")
    for metric in ["Sharpe", "H1", "H2", "OOS_Sharpe"]:
        s = DD_[f"{metric}_regime_share"]
        say(f"    {metric:11s} gap0 mean {DD_[f'{metric}_gap0'].mean():+.4f}  gap25 mean "
            f"{DD_[f'{metric}_gap25'].mean():+.4f}  cost term mean "
            f"{DD_[f'{metric}_cost_term'].mean():+.4f}  REGIME share median {s.median():.3f} "
            f"(mean {s.mean():.3f})   cells where the regime term alone exceeds the whole gap: "
            f"{int((s > 1).sum())}/{len(s)}")
    ref_cell = DD_[(DD_.cad == "W") & (DD_.lam == 1.0)]
    say("\n  at the reference setting (weekly, lambda=1) only:")
    say(ref_cell[["book", "f", "to_u56", "to_broad", "Sharpe_gap0", "Sharpe_gap25",
                  "H2_gap0", "H2_gap25", "OOS_Sharpe_gap0", "OOS_Sharpe_gap25"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================== D2 matched turnover
    say("\n" + "=" * 200)
    say("D2 — MATCHED TURNOVER.  T* = the u56 weekly/lambda=1 turnover of the SAME (book, f); the "
        "broad and small books are dialled onto it along (cadence, lambda), then read at 25 bps.")
    M = []
    for (book, f), d in G[G.cost == WALL_RUNG].groupby(["book", "f"]):
        u = d[(d.panel == "u56") & (d.cad == "W") & (d.lam == 1.0)]
        if not len(u):
            continue
        T = float(u.turnover.iloc[0])
        for pn, dp in d.groupby("panel"):
            # nearest realised turnover to T* over the whole (cadence, lambda) grid
            i = (dp.turnover - T).abs().idxmin()
            r = dp.loc[i]
            nat = dp[(dp.cad == "W") & (dp.lam == 1.0)]
            nat = nat.iloc[0] if len(nat) else None
            M.append(dict(book=book, f=f, panel=pn, T_star=T,
                          nat_cad="W", nat_lam=1.0,
                          nat_to=float(nat.turnover) if nat is not None else np.nan,
                          nat_Sharpe=float(nat.Sharpe) if nat is not None else np.nan,
                          nat_H2=float(nat.H2) if nat is not None else np.nan,
                          nat_OOS=float(nat.OOS_Sharpe) if nat is not None else np.nan,
                          nat_m_min=float(nat.m_min) if nat is not None else np.nan,
                          nat_pass4b=bool(nat.pass4b) if nat is not None else False,
                          mt_cad=r.cad, mt_lam=r.lam, mt_to=float(r.turnover),
                          to_err=float(r.turnover - T),
                          mt_CAGR=float(r.CAGR), mt_Sharpe=float(r.Sharpe),
                          mt_MaxDD=float(r.MaxDD), mt_H1=float(r.H1), mt_H2=float(r.H2),
                          mt_OOS=float(r.OOS_Sharpe), mt_m_H1=float(r.m_H1),
                          mt_m_H2=float(r.m_H2), mt_m_OOS=float(r.m_OOS),
                          mt_m_DD=float(r.m_DD), mt_m_CAGR=float(r.m_CAGR),
                          mt_m_min=float(r.m_min), mt_bind=r.m_bind,
                          mt_pass4b=bool(r.pass4b), mt_pass4a=bool(r.pass4a_v2)))
    MT = pd.DataFrame(M)
    MT.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    say(MT[["book", "f", "panel", "T_star", "nat_to", "nat_Sharpe", "nat_H2", "nat_OOS",
            "nat_pass4b", "mt_cad", "mt_lam", "mt_to", "to_err", "mt_CAGR", "mt_Sharpe",
            "mt_MaxDD", "mt_H1", "mt_H2", "mt_OOS", "mt_m_min", "mt_bind",
            "mt_pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    br = MT[MT.panel == "broad"]
    say(f"\n  broad @25bps at MATCHED turnover: 4b passes {int(br.mt_pass4b.sum())}/{len(br)} "
        f"(natively {int(br.nat_pass4b.sum())}/{len(br)});  mean dSharpe from matching "
        f"{float((br.mt_Sharpe - br.nat_Sharpe).mean()):+.4f}, dH2 "
        f"{float((br.mt_H2 - br.nat_H2).mean()):+.4f}, dOOS "
        f"{float((br.mt_OOS - br.nat_OOS).mean()):+.4f}")
    say(f"  binding bar for broad at matched turnover: {br.mt_bind.value_counts().to_dict()}")
    say(f"  worst-of-five margin for broad: native mean {br.nat_m_min.mean():+.4f} -> matched "
        f"{br.mt_m_min.mean():+.4f}  (a wall closes only if this crosses 0)")

    # ============================================================== D3 matched cost drag
    say("\n" + "=" * 200)
    say("D3 — MATCHED COST DRAG.  Rung c* = 25 * to_u56 / to_panel, so turnover x bps is equal.  "
        "This changes NOTHING about the book, only the price it pays.")
    for (book, f), d in G[(G.cad == "W") & (G.lam == 1.0)].groupby(["book", "f"]):
        u = d[d.panel == "u56"]
        if not len(u):
            continue
        tu = float(u.turnover.iloc[0])
        for pn, dp in d.groupby("panel"):
            tp = float(dp.turnover.iloc[0])
            cstar = WALL_RUNG * tu / tp if tp else np.nan
            s25, _ = interp_to(dp, "cost", "Sharpe", WALL_RUNG)
            sst, brack = interp_to(dp, "cost", "Sharpe", cstar)
            h2st, _ = interp_to(dp, "cost", "H2", cstar)
            oost, _ = interp_to(dp, "cost", "OOS_Sharpe", cstar)
            mst, _ = interp_to(dp, "cost", "m_min", cstar)
            say(f"    {book:6s} f={f:.2f} {pn:6s}  turnover {tp:5.2f}x/yr  c* {cstar:5.1f}bps "
                f"{'(bracketed)' if brack else '(clamped)'}  Sharpe@25 {s25:.4f} -> Sharpe@c* "
                f"{sst:.4f}   H2 {h2st:.4f}  OOS {oost:.4f}  worst-of-five margin {mst:+.4f}")

    # ============================================================== D4 the H2 regime, at zero cost
    say("\n" + "=" * 200)
    say("D4 — THE H2 REGIME AT ZERO COST.  A wall already standing at 0 bps is not a cost wall.")
    say(f"    SPY H1/H2/OOS bars: " + "   ".join(
        f"{pn} {REF[pn]['spy_h1']:.4f}/{REF[pn]['spy_h2']:.4f}/{REF[pn]['mSo']['Sharpe']:.4f}"
        for pn in PANELS))
    z = G[(G.cost == 0.0) & (G.cad == "W") & (G.lam == 1.0)]
    say("    book Sharpe / H1 / H2 / OOS and 4b margins at ZERO cost (weekly, lambda=1):")
    say(z[["panel", "book", "f", "turnover", "CAGR", "Sharpe", "H1", "H2", "OOS_Sharpe",
           "m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR", "m_min", "m_bind", "pass4b"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n    per panel: how many of the 4b-failing bars at 25 bps ALREADY fail at 0 bps "
        "(weekly/lambda=1, all books):")
    for pn in PANELS:
        a = G[(G.panel == pn) & (G.cad == "W") & (G.lam == 1.0) & (G.cost == WALL_RUNG)]
        b = G[(G.panel == pn) & (G.cad == "W") & (G.lam == 1.0) & (G.cost == 0.0)]
        j = a.merge(b, on=["book", "f"], suffixes=("_25", "_0"))
        fail25 = tot = pre = 0
        for k in BARS5:
            f25 = j[f"m_{k}_25"] <= 0
            f0 = j[f"m_{k}_0"] <= 0
            fail25 += int(f25.sum())
            pre += int((f25 & f0).sum())
            tot += len(j)
        say(f"      {pn:6s} bars failing @25bps {fail25}/{tot}; of those already failing @0bps "
            f"{pre} ({(pre / fail25 if fail25 else float('nan')):.1%})")

    # ============================================================== rule 8
    say("\n" + "=" * 200)
    say("RULE 8 — (cadence, lambda) chosen on IS 2009-2016 by IS Sharpe at 25 bps; OOS 2017-2026 "
        "read once.  Control = the reference setting (weekly, lambda=1), i.e. do-nothing.")
    W = []
    for (pn, book, f), d in G[G.cost == WALL_RUNG].groupby(["panel", "book", "f"]):
        pick = d.loc[d.IS_Sharpe.idxmax()]
        ctl = d[(d.cad == "W") & (d.lam == 1.0)].iloc[0]
        b = REF[pn]["base"][WALL_RUNG]
        v2o, v1o = metrics(b["v2"].loc[OOS_START:]), metrics(b["v1"].loc[OOS_START:])
        W.append(dict(panel=pn, book=book, f=f, pick_cad=pick.cad, pick_lam=pick.lam,
                      pick_to=pick.turnover, OOS_CAGR=pick.OOS_CAGR,
                      OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                      ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                      ctl_OOS_MaxDD=ctl.OOS_MaxDD, best_OOS_Sharpe=float(d.OOS_Sharpe.max()),
                      v2_OOS_Sharpe=v2o["Sharpe"], v2_OOS_CAGR=v2o["CAGR"],
                      v2_OOS_MaxDD=v2o["MaxDD"], v1_OOS_Sharpe=v1o["Sharpe"],
                      spy_OOS_Sharpe=REF[pn]["mSo"]["Sharpe"], spy_OOS_CAGR=REF[pn]["mSo"]["CAGR"],
                      spy_OOS_MaxDD=REF[pn]["mSo"]["MaxDD"],
                      pass4b=bool(pick.pass4b), pass4a_v2=bool(pick.pass4a_v2),
                      m_min=float(pick.m_min), m_bind=pick.m_bind))
    WF = pd.DataFrame(W)
    WF["prem_ctl"] = WF.OOS_Sharpe - WF.ctl_OOS_Sharpe
    WF["prem_v2"] = WF.OOS_Sharpe - WF.v2_OOS_Sharpe
    WF["prem_spy"] = WF.OOS_Sharpe - WF.spy_OOS_Sharpe
    WF["regret"] = WF.best_OOS_Sharpe - WF.OOS_Sharpe
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF[["panel", "book", "f", "pick_cad", "pick_lam", "pick_to", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "ctl_OOS_Sharpe", "v2_OOS_Sharpe", "v2_OOS_CAGR", "spy_OOS_Sharpe",
            "spy_OOS_CAGR", "prem_ctl", "prem_v2", "prem_spy", "regret", "pass4b",
            "m_bind"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  mean OOS Sharpe: IS-chosen {WF.OOS_Sharpe.mean():.4f}  control (weekly/lam=1) "
        f"{WF.ctl_OOS_Sharpe.mean():.4f}  RULES v2 {WF.v2_OOS_Sharpe.mean():.4f}  SPY "
        f"{WF.spy_OOS_Sharpe.mean():.4f}   premium vs control {WF.prem_ctl.mean():+.4f} "
        f"(beats it {int((WF.prem_ctl > 0).sum())}/{len(WF)})   regret {WF.regret.mean():.4f}")
    say(f"  OOS 4b passes among the IS picks: {int(WF.pass4b.sum())}/{len(WF)};  by panel " +
        ", ".join(f"{pn} {int(WF[WF.panel == pn].pass4b.sum())}/{len(WF[WF.panel == pn])}"
                  for pn in PANELS))

    # ============================================================== KEEP paths
    say("\n" + "=" * 200)
    say("KEEP PATHS over all arm-rows (4a vs the LIVE RULES v2 book cost-matched; 4b vs SPY).")
    K = G.copy()
    K["both"] = K.pass4a_v2 & K.pass4b
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(f"  rows {len(K)}:  4b {int(K.pass4b.sum())}   4a vs LIVE v2 {int(K.pass4a_v2.sum())}   "
        f"4a vs v1 (continuity) {int(K.pass4a_v1.sum())}   BOTH {int(K.both.sum())}")
    say("  4b by panel x cost rung:")
    for pn, d in K.groupby("panel"):
        say(f"    {pn:6s} " + "   ".join(
            f"{c:.0f}bps {int(d[d.cost == c].pass4b.sum()):3d}/{len(d[d.cost == c]):3d}"
            for c in RUNGS))
    say("  4b by panel x cadence at 25 bps:")
    for pn, d in K[K.cost == WALL_RUNG].groupby("panel"):
        say(f"    {pn:6s} " + "   ".join(
            f"{cd} {int(d[d.cad == cd].pass4b.sum()):3d}/{len(d[d.cad == cd]):3d}"
            for cd in CADENCES))
    if int(K.both.sum()):
        say("\n  rows clearing BOTH KEEP paths:")
        say(K[K.both][["panel", "book", "f", "lam", "cad", "cost", "turnover", "CAGR", "Sharpe",
                       "MaxDD", "H1", "H2", "OOS_Sharpe", "m_min"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("\n  no row clears BOTH KEEP paths.")
    b25 = K[(K.panel == "broad") & (K.cost == WALL_RUNG)]
    say(f"\n  THE WALL, restated over the whole (cadence, lambda, book, f) grid: broad @25bps "
        f"clears 4b in {int(b25.pass4b.sum())} of {len(b25)} rows; best worst-of-five margin "
        f"{b25.m_min.max():+.4f} (binding {b25.loc[b25.m_min.idxmax(), 'm_bind']}, at "
        f"{b25.loc[b25.m_min.idxmax(), 'cad']}/lam={b25.loc[b25.m_min.idxmax(), 'lam']}, turnover "
        f"{b25.loc[b25.m_min.idxmax(), 'turnover']:.2f}x/yr)")

    say("\n" + "=" * 200)
    say("SURVIVORSHIP (idea 54): current-constituent panels; the small panel is a screen run today "
        "and back-filled. It flatters low-turnover settings, i.e. the end of the dial D2 moves "
        "toward, so a NEGATIVE matched-turnover result is understated, not overstated.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.console.txt / .grid.csv / .decomp.csv / .matched.csv / .walkforward.csv "
        f"/ .keeppaths.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

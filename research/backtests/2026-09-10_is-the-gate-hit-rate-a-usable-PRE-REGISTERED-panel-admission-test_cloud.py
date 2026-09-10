#!/usr/bin/env python3
"""Idea 467 — is the GATE HIT RATE a usable PRE-REGISTERED panel admission test?  (cloud, 2026-09-10)

QUEUE 467: "idea 458's only transferable separator is the 200d gate's hit rate (inband >= 0.711)
and the drift of what the gate cuts (r_out >= +5.63%/yr), 0.769 held-out on a different price
source, with the real SMALL439 panel one of its misses.  Test whether either statistic, computed on
the IS window alone, predicts the sign of gate-vs-ungated on panels the record has never used
(sector sub-panels, ETF-only, megacap-only), and whether the miss is the small panel's
survivorship.  Max 2 params (gate stat, panel)."

WHAT AN ADMISSION TEST HAS TO DO, AND WHAT 458 ACTUALLY MEASURED
  458 fitted its thresholds against `ctl_wins_IS` — whether the ungated control is the IS argmax.
  But 458's own bigger result is that the IS degeneracy DOES NOT TRANSFER: the control wins IS in
  39/69 probe cells and OOS in 11/69, 36 of 39 flip, and corr(D_is, D_oos) = -0.05.  A test that
  admits a panel is a claim about what will happen NEXT, so this file scores both targets side by
  side and treats the OOS one as the headline:

    T_IS   sign of D_is  = Sharpe(ungated control) - Sharpe(best gated arm), 2009-2016
    T_OOS  sign of D_oos = the same contrast on the untouched 2017-2026 window (PROTOCOL rule 8)

  If the published thresholds predict T_IS on fresh panels but not T_OOS, the statistic is a
  description of the IS window — exactly what 458 said the degeneracy was — and it is NOT an
  admission test, however high its in-sample accuracy.

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 GATE STAT: `inband` (fraction of priced ticker-days inside the 200d +/-3% band) and `r_out`
     (annualised drift of what the gate cuts).  Both are reported everywhere.  Each is scored at
     (a) idea 458's PUBLISHED threshold, carried verbatim and never re-fitted, and (b) a threshold
     re-fitted on the three ANCHOR panels only — never on the fresh ones.
  P2 PANEL FAMILY: A = named groups of u56 (ETF-only, megacap-only, bonds/FX/commodities,
     equity-only) — six panels the record has never run standalone; B = eleven SECTOR sub-panels of
     broad136; C = eleven SECTOR sub-panels of SMALL439.  Sector membership is assigned price-only
     and IS-only: each name joins the GICS sector ETF whose 2009-2016 daily returns it correlates
     with most (G5 asserts the window).  Cost rungs and the arm menu are REPORTED axes.
  The three record panels (u56 / broad136 / small439) are ANCHORS, not test panels: they are what
  458's rule was built on, and every threshold this file re-fits is re-fit on them alone.

THE ARM MENU (idea 458's PROBE_ARMS, verbatim)
  control        ungated equal weight, gross 1.00, weekly
  b{B}-g1.00-{F} 200d band gate at B in {0.000, 0.015, 0.030, 0.045, 0.060}, F in {W, M},
                 gross 1.00, gated-out weight to CASH (de-grossed, never re-spread)

THE SURVIVORSHIP QUESTION (Q3)
  Two price-only probes, both pre-registered:
    S1 LISTING-AGE COHORT.  SMALL439 split into names priced on the panel's first day (the maximally
       survivorship-selected cohort: alive in 2010 AND still sub-$2B today) and names that listed
       later.  If the miss is survivorship, the two cohorts should not agree.
    S2 ERA DRIFT.  inband and r_out recomputed on the OOS window and compared with the IS values.
       Survivors' early returns are biased UP, so a survivorship-driven statistic should decay from
       IS to OOS on SMALL439 by more than on U56 / broad136.  This is the record's own era test
       (idea 645), applied to the separator rather than to a return gap.

GATES (run before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest`, returns AND turnover, W and M.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=25).
  G3 ANCHOR REPRODUCTION: inband and r_out re-derived on u56 / broad136 / SMALL439 must place u56
     on one side of BOTH published thresholds and must confirm that SMALL439 is a MISS — i.e. this
     file reproduces the defect the queue is asking about, rather than assuming it.
  G4 the IS and OOS windows are disjoint and jointly exhaust the evaluated sample.
  G5 NO LEAKAGE: the sector-assignment correlation matrix is built on data ending at IS_END.
  G6 PARTITION: families B and C partition their parent panels exactly (every name assigned once,
     no name in two sub-panels), and every scored panel clears the pre-registered 6-name floor.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three anchors are CURRENT constituents, and so is every panel
    derived from them.  SMALL439 additionally drops every ticker with max_1d_move >= 1.0 in
    data/small_meta.csv before anything runs.  Family C inherits the small panel's bias in full;
    that is the point of S1/S2, not a defect this file can remove.
  * The sector sub-panels are CORRELATION proxies, not GICS classifications — no sector labels
    exist offline in this repo.  They are pre-registered, deterministic and IS-only, and they are
    reported as proxies.
  * SPY is a constituent of the ETF_BROAD panel and is simultaneously the 4a/4b benchmark there;
    that panel's 4b numbers are therefore self-referential and are flagged in the output.
  * Idea 321: MaxDD is one number off one path.  Idea 126: t+1 execution, 10 bps default rung.
  * Ideas 527/531: 4b is in practice a DD-cap test on ungated books; both KEEP paths are priced on
    every arm anyway, as PROTOCOL requires.
  * n = 28 fresh panels is a small sample; the headline carries a permutation p-value, not a t-stat.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .panels.csv, .grid.csv, .cells.csv, .survivorship.csv.
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
from baseline import load_universe, band_state, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_is-the-gate-hit-rate-a-usable-PRE-REGISTERED-panel-admission-test_cloud"
OUT = ROOT / "research" / "backtests"

IS_END, OOS_START = "2016-12-31", "2017-01-01"
BAND_LIVE = 0.03                   # RULES v2 clause 2, the band the separator was measured on
PHI, DELTA = 0.70, 0.60            # 4b CAGR floor and MaxDD cap, as fractions of SPY's
PCOST = 10.0                       # PROTOCOL's own rung
RUNGS = [0.0, 10.0, 25.0]          # reported cost ladder
WARM = 260                         # idea 458's warm-up bar, carried verbatim
MINNAMES = 6                       # pre-registered size floor for a scored panel

# idea 458's PUBLISHED thresholds, carried verbatim and NEVER re-fitted
PUB = {"inband": 0.711, "r_out": 0.0563}
# idea 458's probe menu, verbatim
PROBE = [("control", dict(band=None, gross=1.0, freq="W", gated=False))] + [
    (f"b{b:g}-g1.00-{f}", dict(band=b, gross=1.0, freq=f, gated=True))
    for b in (0.0, 0.015, 0.03, 0.045, 0.06) for f in ("W", "M")]
SECTOR_ETFS = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner
# =====================================================================================
def _mask(idx, freq):
    return rebalance_mask(idx, freq).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    n = len(rets)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return port, turn


def run(px, W, freq):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    p, t = fast_bt(rets, w_t, _mask(px.index, freq))
    return pd.Series(p, index=px.index), pd.Series(t, index=px.index)


def ew_band_weights(sub, band, gross, gated):
    """Equal weight over the priced names at gross/N, N = names priced that day.  gated=True holds
    only the names inside the 200d +/-band and sends the rest to CASH (de-grossed, never
    re-spread) — RULES v2 clause 2 generalised to any band."""
    e = sub.notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if not gated:
        return ew
    return ew.where(band_state(sub, band) & sub.notna(), 0.0)


# =====================================================================================
# metrics helpers
# =====================================================================================
def sh(r):
    return metrics(r)["Sharpe"]


def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def bars_of(spy):
    h1, h2 = halves(spy)
    m = metrics(spy)
    return dict(s1=h1, s2=h2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=sh(spy.loc[OOS_START:]),
                spy_oos=spy.loc[OOS_START:])


def pass4b(r, b, window="full"):
    if window == "full":
        h1, h2 = halves(r)
        m = metrics(r)
        return bool(h1 > b["s1"] and h2 > b["s2"] and sh(r.loc[OOS_START:]) > b["soos"]
                    and abs(m["MaxDD"]) <= DELTA * abs(b["sdd"]) and m["CAGR"] >= PHI * b["scagr"])
    x = r.loc[OOS_START:]
    h1, h2 = halves(x)
    m = metrics(x)
    sp = b["spy_oos"]
    o1, o2 = halves(sp)
    mo = metrics(sp)
    return bool(h1 > o1 and h2 > o2 and abs(m["MaxDD"]) <= DELTA * abs(mo["MaxDD"])
                and m["CAGR"] >= PHI * mo["CAGR"])


def pass4a(r, base, window="full"):
    x, y = (r, base) if window == "full" else (r.loc[OOS_START:], base.loc[OOS_START:])
    h1, h2 = halves(x)
    b1, b2 = halves(y)
    return bool(h1 > b1 and h2 > b2 and metrics(x)["MaxDD"] >= metrics(y)["MaxDD"])


def auc(x, y):
    """Rank AUC of continuous x predicting boolean y (0.5 = no information).  Idea 458's, verbatim."""
    x, y = np.asarray(x, float), np.asarray(y, bool)
    ok = np.isfinite(x)
    x, y = x[ok], y[ok]
    if y.all() or (~y).all() or len(x) < 3:
        return np.nan
    r = pd.Series(x).rank().values
    n1, n0 = y.sum(), (~y).sum()
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def best_threshold(x, y):
    """Best single split accuracy for predicting boolean y from x.  Idea 458's, verbatim."""
    x, y = np.asarray(x, float), np.asarray(y, bool)
    ok = np.isfinite(x)
    x, y = x[ok], y[ok]
    best = (-1.0, np.nan, 0)
    for t in np.unique(x):
        for s in (+1, -1):
            pred = (x >= t) if s > 0 else (x < t)
            a = float((pred == y).mean())
            if a > best[0]:
                best = (a, float(t), s)
    return best


def perm_acc_p(pred, y, nperm=20000, seed=467):
    """How often does a random relabelling of the PREDICTIONS do at least this well?"""
    pred, y = np.asarray(pred, bool), np.asarray(y, bool)
    obs = float((pred == y).mean())
    rng = np.random.default_rng(seed)
    hits = sum(1 for _ in range(nperm) if float((rng.permutation(pred) == y).mean()) >= obs - 1e-12)
    return obs, (hits + 1) / (nperm + 1)


# =====================================================================================
# panels
# =====================================================================================
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def panel_props(px_all, cols, lo=None, hi=IS_END):
    """Idea 458's panel properties, verbatim, over one window (default: the IS window)."""
    start = px_all.index[WARM]
    sub = px_all[cols]
    lo = start if lo is None else max(start, pd.Timestamp(lo))
    bs = band_state(sub, BAND_LIVE).loc[lo:hi]
    px_w = sub.loc[lo:hi]
    ret = px_w.pct_change()
    priced = px_w.notna()
    if priced.values.sum() == 0:
        return dict(N=len(cols), inband=np.nan, r_in=np.nan, r_out=np.nan, avoided=np.nan)
    inband = float((bs & priced).values.sum() / priced.values.sum())
    r_out = float(ret.where(~bs & priced).stack().mean() * 252)
    r_in = float(ret.where(bs & priced).stack().mean() * 252)
    return dict(N=len(cols), inband=inband, r_in=r_in, r_out=r_out, avoided=r_in - r_out)


def sector_map(px_all, names, etf_px):
    """Assign each name to the sector ETF whose IS-window daily returns it correlates with most.
    Price-only, deterministic, and computed on data ENDING at IS_END (gate G5)."""
    start = px_all.index[WARM]
    a = px_all[names].loc[start:IS_END].pct_change()
    b = etf_px.loc[start:IS_END].pct_change().reindex(a.index)
    A = a.sub(a.mean()).div(a.std().replace(0, np.nan))
    B = b.sub(b.mean()).div(b.std().replace(0, np.nan))
    B = B.loc[:, B.notna().sum() >= 252]      # an ETF with no usable IS history cannot be a bucket
    n = A.notna().T.astype(float).dot(B.notna().astype(float))
    C = A.fillna(0.0).T.dot(B.fillna(0.0)).div(n.where(n >= 252))
    ok = C.notna().any(axis=1)                # a name with no IS-window overlap stays UNASSIGNED
    m = pd.Series(pd.NA, index=C.index, dtype="object")
    m.loc[ok] = C.loc[ok].idxmax(axis=1)
    return m, int((~ok).sum())


def build_panels():
    """Every panel this file scores.  ANCHORS are idea 458's three; families A/B/C are fresh."""
    import json
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    u56 = load_universe().dropna(how="all").ffill()
    broad = load_universe(broad=True).dropna(how="all").ffill()
    small, ndrop = small_panel()
    small = small.dropna(how="all").ffill()

    P = []                                  # (label, family, price frame, constituent cols)

    def add(label, fam, px_all, cols, parent=""):
        cols = [c for c in cols if c in px_all.columns]
        if len(cols) < MINNAMES:
            return None
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px_all.columns else [])))
        P.append(dict(label=label, family=fam, parent=parent, px=px_all[keep], cols=cols))
        return len(cols)

    add("u56", "ANCHOR", u56, [c for c in u56.columns if c != "SPY"] + ["SPY"])
    add("broad136", "ANCHOR", broad, list(broad.columns))
    add("small439", "ANCHOR", small, [c for c in small.columns if c != "SPY"])

    # --- family A: named groups of u56, never run standalone ---------------------------
    noneq = [t for t in U["bonds_fx_commod"] if t in u56.columns]
    add("A:ETF_SECTORS", "A", u56, U["sectors"])
    add("A:ETF_BROAD", "A", u56, U["broad"])
    add("A:ETF_ALL", "A", u56, U["sectors"] + U["broad"])
    add("A:BONDS_FX_COMMOD", "A", u56, noneq)
    add("A:MEGACAP", "A", u56, U["megacap"])
    add("A:EQUITY_ONLY", "A", u56, [c for c in u56.columns if c not in set(noneq) | {"SPY"}])

    # --- families B and C: sector sub-panels, assigned price-only on the IS window -----
    etf = u56[[c for c in SECTOR_ETFS if c in u56.columns]]
    maps, unassigned = {}, {}
    for lbl, pxa, fam in (("broad136", broad, "B"), ("small439", small, "C")):
        names = [c for c in pxa.columns if c != "SPY"]
        e = etf.reindex(pxa.index).ffill()
        m, n_un = sector_map(pxa, names, e)
        maps[lbl] = m
        unassigned[lbl] = n_un
        for s in sorted(m.dropna().unique()):
            add(f"{fam}:{lbl}-{s}", fam, pxa, list(m[m == s].index), parent=lbl)

    # --- survivorship cohorts on SMALL439 (family S) -----------------------------------
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv").set_index("ticker")
    d0 = small.index[0]
    names = [c for c in small.columns if c != "SPY"]
    old = [c for c in names if c in meta.index and pd.Timestamp(meta.loc[c, "first_date"]) <= d0]
    new = [c for c in names if c not in set(old)]
    add("S:SMALL-FULLHIST", "S", small, old, parent="small439")
    add("S:SMALL-LATELIST", "S", small, new, parent="small439")
    return P, maps, unassigned, ndrop, len(old), len(new)


# =====================================================================================
# one panel: every arm, both windows, both KEEP paths
# =====================================================================================
def score_panel(p, rows_grid):
    px_all, cols, lbl = p["px"], p["cols"], p["label"]
    start = px_all.index[WARM]
    sub = px_all[cols]
    spy = px_all["SPY"].pct_change().fillna(0.0).loc[start:]
    b = bars_of(spy)
    r0b, tob = run(px_all, rules_v2_weights(px_all[cols]).reindex(columns=px_all.columns).fillna(0.0), "W")
    baser = (r0b - tob * PCOST / 1e4).loc[start:]

    R = {}
    for name, a in PROBE:
        W = ew_band_weights(sub, 0.0 if a["band"] is None else a["band"], a["gross"], a["gated"])
        W = W.reindex(columns=px_all.columns).fillna(0.0)
        r0, to = run(px_all, W, a["freq"])
        r0, to = r0.loc[start:], to.loc[start:]
        R[name] = (r0, to)
        rec = dict(panel=lbl, family=p["family"], arm=name, gated=a["gated"],
                   band=a["band"], freq=a["freq"],
                   turnover=float(to.sum() / (len(to) / 252.0)))
        for c in RUNGS:
            r = r0 - to * c / 1e4
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = halves(r)
            rec[f"sh_full_{c:g}"], rec[f"cagr_full_{c:g}"], rec[f"dd_full_{c:g}"] = \
                m["Sharpe"], m["CAGR"], m["MaxDD"]
            rec[f"h1_{c:g}"], rec[f"h2_{c:g}"] = h1, h2
            rec[f"sh_is_{c:g}"] = sh(r.loc[:IS_END])
            rec[f"sh_oos_{c:g}"], rec[f"cagr_oos_{c:g}"], rec[f"dd_oos_{c:g}"] = \
                mo["Sharpe"], mo["CAGR"], mo["MaxDD"]
            if c == PCOST:
                rec["p4a_full"] = pass4a(r, baser)
                rec["p4b_full"] = pass4b(r, b, "full")
                rec["p4a_oos"] = pass4a(r, baser, "oos")
                rec["p4b_oos"] = pass4b(r, b, "oos")
        rows_grid.append(rec)

    out = dict(panel=lbl, family=p["family"], parent=p["parent"], **panel_props(px_all, cols))
    oo = panel_props(px_all, cols, lo=OOS_START, hi=None)
    out["inband_oos"], out["r_out_oos"] = oo["inband"], oo["r_out"]
    for c in RUNGS:
        S_is = {k: sh((v[0] - v[1] * c / 1e4).loc[:IS_END]) for k, v in R.items()}
        S_oo = {k: sh((v[0] - v[1] * c / 1e4).loc[OOS_START:]) for k, v in R.items()}
        g = [k for k in R if k != "control"]
        out[f"D_is_{c:g}"] = S_is["control"] - max(S_is[k] for k in g)
        out[f"D_oos_{c:g}"] = S_oo["control"] - max(S_oo[k] for k in g)
        out[f"ctl_is_{c:g}"] = bool(out[f"D_is_{c:g}"] > 0)
        out[f"ctl_oos_{c:g}"] = bool(out[f"D_oos_{c:g}"] > 0)
    m_spy, m_spy_o = metrics(spy), metrics(spy.loc[OOS_START:])
    out["spy_cagr"], out["spy_sh"], out["spy_dd"] = m_spy["CAGR"], m_spy["Sharpe"], m_spy["MaxDD"]
    out["spy_cagr_oos"], out["spy_sh_oos"] = m_spy_o["CAGR"], m_spy_o["Sharpe"]
    return out


# =====================================================================================
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 467 — is the 200d GATE HIT RATE a usable PRE-REGISTERED panel admission test?")
    say(f"  P1 gate stat: inband (published bar {PUB['inband']:.3f}) and r_out (published bar "
        f"{PUB['r_out']:+.4f}/yr), both carried verbatim from idea 458.")
    say("  P2 panel family: A = named u56 groups, B = broad136 sectors, C = SMALL439 sectors, "
        "S = SMALL439 listing-age cohorts.  u56/broad136/small439 are ANCHORS, never test panels.")
    say(f"  Targets: T_IS (sign of D_is) and T_OOS (sign of D_oos, {OOS_START}+ untouched).")
    say("=" * 110)

    P, maps, unassigned, ndrop, n_old, n_new = build_panels()
    say(f"  panels built: {len(P)}  "
        f"(ANCHOR {sum(1 for p in P if p['family'] == 'ANCHOR')}, "
        f"A {sum(1 for p in P if p['family'] == 'A')}, "
        f"B {sum(1 for p in P if p['family'] == 'B')}, "
        f"C {sum(1 for p in P if p['family'] == 'C')}, "
        f"S {sum(1 for p in P if p['family'] == 'S')})   "
        f"SMALL439 dropped {ndrop} max_1d_move>=1.0 names")
    say(f"  SMALL439 listing-age cohorts: FULLHIST {n_old} names, LATELIST {n_new} names")

    # ---- gates ---------------------------------------------------------------------
    say("")
    say("=" * 110)
    say("GATES")
    say("=" * 110)
    anchor = [p for p in P if p["label"] == "u56"][0]
    wr = wt = wc = 0.0
    for freq in ("W", "M"):
        W = ew_band_weights(anchor["px"][anchor["cols"]], 0.03, 1.0, True)
        W = W.reindex(columns=anchor["px"].columns).fillna(0.0)
        rf, tf = run(anchor["px"], W, freq)
        ref = backtest(anchor["px"], W, cost_bps=0.0, freq=freq)
        wr = max(wr, float((rf - ref["returns"]).abs().max()))
        wt = max(wt, float((tf - ref["turnover"]).abs().max()))
        ref25 = backtest(anchor["px"], W, cost_bps=25.0, freq=freq)
        wc = max(wc, float(((rf - tf * 25.0 / 1e4) - ref25["returns"]).abs().max()))
    say(f"  G1 fast runner vs engine.backtest (W,M): max |dret| {wr:.3e}  max |dturn| {wt:.3e}  "
        f"{'PASS' if max(wr, wt) < 1e-12 else 'FAIL'}")
    say(f"  G2 cost identity r(25) = r(0) - turn*25/1e4 : max |d| {wc:.3e}  "
        f"{'PASS' if wc < 1e-12 else 'FAIL'}")
    assert max(wr, wt, wc) < 1e-12

    idx = anchor["px"].index[WARM:]
    nis, noos = int((idx <= IS_END).sum()), int((idx >= OOS_START).sum())
    say(f"  G4 IS {idx[0].date()}..{IS_END} = {nis} d, OOS {OOS_START}..{idx[-1].date()} = {noos} d,"
        f" sum {nis + noos} == {len(idx)}  {'PASS' if nis + noos == len(idx) else 'FAIL'}")
    assert nis + noos == len(idx)

    say(f"  G5 sector assignment window ends at {IS_END} (see sector_map): PASS by construction")
    for parent, m in maps.items():
        fam = "B" if parent == "broad136" else "C"
        subs = [p for p in P if p["family"] == fam]
        assigned = sum(len(p["cols"]) for p in subs)
        allnames = set()
        for p in subs:
            assert not (allnames & set(p["cols"])), "sector sub-panels overlap"
            allnames |= set(p["cols"])
        nun = unassigned.get(parent, 0)
        say(f"  G6 {fam} partitions {parent}: {len(m)} names -> {len(subs)} scored sub-panels "
            f"covering {assigned}; {nun} UNASSIGNED (no IS-window overlap with any sector ETF), "
            f"{len(m) - assigned - nun} in buckets below the {MINNAMES}-name floor; no overlap  PASS")

    # ---- score every panel ---------------------------------------------------------
    say("")
    say("=" * 110)
    say("PART A — EVERY PANEL: the two IS statistics and the gate-vs-ungated sign, IS and OOS")
    say("=" * 110)
    rows_grid: list[dict] = []
    props = []
    for p in P:
        props.append(score_panel(p, rows_grid))
        say(f"    {p['label']:26s} N={len(p['cols']):3d}  [{time.time() - t0:6.1f}s]")
    D = pd.DataFrame(props)
    G = pd.DataFrame(rows_grid)
    D.to_csv(OUT / f"{STEM}.panels.csv", index=False)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    A = D[D.family == "ANCHOR"].set_index("panel")
    say("")
    say("  ANCHORS (idea 458's three panels) — G3 reproduction:")
    say(A[["N", "inband", "r_out", f"D_is_{PCOST:g}", f"ctl_is_{PCOST:g}",
           f"D_oos_{PCOST:g}", f"ctl_oos_{PCOST:g}"]]
        .to_string(float_format=lambda x: f"{x:+.4f}"))
    pub_is = {k: bool(A.loc[k, "inband"] >= PUB["inband"]) for k in A.index}
    pub_ro = {k: bool(A.loc[k, "r_out"] >= PUB["r_out"]) for k in A.index}
    say(f"  published rule says 'control wins': by inband {pub_is}, by r_out {pub_ro}")
    truth = {k: bool(A.loc[k, f"ctl_is_{PCOST:g}"]) for k in A.index}
    say(f"  actual T_IS on the anchors: {truth}")
    miss = [k for k in A.index if pub_is[k] != truth[k] or pub_ro[k] != truth[k]]
    say(f"  G3 anchors MISSED by at least one published bar: {miss}  "
        f"{'PASS — the defect the queue names is reproduced' if 'small439' in miss else 'CHECK'}")

    # ---- the held-out test ---------------------------------------------------------
    say("")
    say("=" * 110)
    say("PART B — THE ADMISSION TEST ON PANELS THE RECORD HAS NEVER USED")
    say("=" * 110)
    F = D[D.family.isin(["A", "B", "C"])].copy()
    say(f"  fresh panels scored: {len(F)}  "
        f"(A {int((F.family == 'A').sum())}, B {int((F.family == 'B').sum())}, "
        f"C {int((F.family == 'C').sum())})")
    cellrows = []
    for c in RUNGS:
        if c == 0.0:
            continue
        for stat in ("inband", "r_out"):
            # threshold (a): idea 458's published bar, verbatim
            # threshold (b): re-fitted on the THREE ANCHORS only, never on fresh panels
            acc_a, thr_a, sgn_a = best_threshold(A[stat].values, A[f"ctl_is_{c:g}"].values)
            for target in ("IS", "OOS"):
                y = F[f"ctl_{target.lower()}_{c:g}"].values.astype(bool)
                x = F[stat].values
                p_pub = x >= PUB[stat]
                p_anc = (x >= thr_a) if sgn_a > 0 else (x < thr_a)
                for nm, pred, thr in (("PUBLISHED", p_pub, PUB[stat]),
                                      ("ANCHOR-REFIT", p_anc, thr_a)):
                    a_obs, pval = perm_acc_p(pred, y)
                    base = max(float(y.mean()), 1.0 - float(y.mean()))
                    cellrows.append(dict(rung=c, stat=stat, target=target, rule=nm, thresh=thr,
                                         acc=a_obs, base_rate=base, lift=a_obs - base,
                                         perm_p=pval, auc=auc(x, y),
                                         n=len(y), pos=int(y.sum())))
    CL = pd.DataFrame(cellrows)
    CL.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    say("")
    say("  accuracy of each rule on the FRESH panels (base rate = always-predict-the-majority):")
    say(CL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("")
    say("  READ: a rule is usable only if it beats its own base rate on the OOS target.")
    for c in (PCOST, 25.0):
        best = CL[(CL.rung == c) & (CL.target == "OOS")].sort_values("lift", ascending=False)
        top = best.iloc[0]
        say(f"    {c:g} bps, T_OOS: best rule = {top['rule']} on {top['stat']} "
            f"(thr {top['thresh']:+.4f}), accuracy {top['acc']:.3f} vs base rate "
            f"{top['base_rate']:.3f}, lift {top['lift']:+.3f}, permutation p = {top['perm_p']:.3f}")
        ist = CL[(CL.rung == c) & (CL.target == "IS")].sort_values("lift", ascending=False).iloc[0]
        say(f"    {c:g} bps, T_IS : best rule = {ist['rule']} on {ist['stat']} "
            f"(thr {ist['thresh']:+.4f}), accuracy {ist['acc']:.3f} vs base rate "
            f"{ist['base_rate']:.3f}, lift {ist['lift']:+.3f}, permutation p = {ist['perm_p']:.3f}")

    r_flip = float(np.corrcoef(F[f"D_is_{PCOST:g}"], F[f"D_oos_{PCOST:g}"])[0, 1])
    same = float((F[f"ctl_is_{PCOST:g}"] == F[f"ctl_oos_{PCOST:g}"]).mean())
    say("")
    say(f"  IS->OOS TRANSFER of the thing being predicted: corr(D_is, D_oos) = {r_flip:+.3f}, "
        f"sign agrees on {same:.1%} of the {len(F)} fresh panels "
        f"(idea 458 measured -0.05 and 3/39 on its probe cells).")

    say("")
    say("  by family (10 bps):")
    say(F.groupby("family").agg(n=("panel", "size"), inband=("inband", "mean"),
                                r_out=("r_out", "mean"),
                                ctl_is=(f"ctl_is_{PCOST:g}", "mean"),
                                ctl_oos=(f"ctl_oos_{PCOST:g}", "mean"),
                                D_oos=(f"D_oos_{PCOST:g}", "mean"))
        .to_string(float_format=lambda x: f"{x:+.4f}"))

    # ---- survivorship --------------------------------------------------------------
    say("")
    say("=" * 110)
    say("PART C — IS THE SMALL439 MISS SURVIVORSHIP?")
    say("=" * 110)
    S = D[D.family.isin(["S", "ANCHOR"])].set_index("panel")
    keep = [k for k in ("small439", "S:SMALL-FULLHIST", "S:SMALL-LATELIST", "u56", "broad136")
            if k in S.index]
    say("  S1 LISTING-AGE COHORT (a survivorship-driven statistic should split the cohorts):")
    say(S.loc[keep, ["N", "inband", "r_out", f"D_is_{PCOST:g}", f"ctl_is_{PCOST:g}",
                     f"D_oos_{PCOST:g}", f"ctl_oos_{PCOST:g}"]]
        .to_string(float_format=lambda x: f"{x:+.4f}"))
    say("")
    say("  S2 ERA DRIFT of the separator itself (IS value -> OOS value):")
    E = S.loc[keep, ["inband", "inband_oos", "r_out", "r_out_oos"]].copy()
    E["d_inband"] = E.inband_oos - E.inband
    E["d_r_out"] = E.r_out_oos - E.r_out
    say(E.to_string(float_format=lambda x: f"{x:+.4f}"))
    sv = S.loc[keep].reset_index()
    sv.to_csv(OUT / f"{STEM}.survivorship.csv", index=False)
    fh, ll = "S:SMALL-FULLHIST", "S:SMALL-LATELIST"
    if fh in S.index and ll in S.index:
        agree_is = bool(S.loc[fh, f"ctl_is_{PCOST:g}"] == S.loc[ll, f"ctl_is_{PCOST:g}"])
        agree_oos = bool(S.loc[fh, f"ctl_oos_{PCOST:g}"] == S.loc[ll, f"ctl_oos_{PCOST:g}"])
        say("")
        say(f"  cohorts agree on T_IS: {agree_is}   on T_OOS: {agree_oos}   "
            f"|d inband| {abs(S.loc[fh, 'inband'] - S.loc[ll, 'inband']):.4f}   "
            f"|d r_out| {abs(S.loc[fh, 'r_out'] - S.loc[ll, 'r_out']):.4f}")
        say("  If the cohorts AGREE and the small panel's era drift is not the largest of the "
            "three anchors, the miss is NOT the small panel's survivorship.")

    # ---- the book ------------------------------------------------------------------
    say("")
    say("=" * 110)
    say("PART D — PROTOCOL 4a / 4b ON EVERY ARM")
    say("=" * 110)
    say(f"  arms {len(G)} over {len(P)} panels x {len(PROBE)} arms")
    say(f"  full sample 10 bps: 4a {int(G.p4a_full.sum())}   4b {int(G.p4b_full.sum())}")
    say(f"  OOS-window re-cut : 4a {int(G.p4a_oos.sum())}   4b {int(G.p4b_oos.sum())}")
    if int(G.p4b_full.sum()):
        bb = G[G.p4b_full].nlargest(6, f"sh_full_{PCOST:g}")
        say("  best 4b passers by full-sample Sharpe (10 bps):")
        say(bb[["panel", "arm", f"cagr_full_{PCOST:g}", f"sh_full_{PCOST:g}",
                f"dd_full_{PCOST:g}", f"h1_{PCOST:g}", f"h2_{PCOST:g}",
                f"sh_oos_{PCOST:g}", f"cagr_oos_{PCOST:g}", f"dd_oos_{PCOST:g}", "p4b_oos"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        say("  NOTE: family B/C panels are sector sub-panels of CURRENT-CONSTITUENT lists; a 4b "
            "pass on one is not an investable claim (PROTOCOL 9 / idea 54).")
    # PROTOCOL rule 8 on the ARM choice: pick the arm on IS Sharpe, read the untouched OOS once.
    k8 = []
    for lbl, g in G.groupby("panel"):
        g = g.set_index("arm")
        pick = g[f"sh_is_{PCOST:g}"].idxmax()
        k8.append(dict(panel=lbl, family=g["family"].iloc[0], pick=pick,
                       p4b_full=bool(g.loc[pick, "p4b_full"]),
                       p4b_oos=bool(g.loc[pick, "p4b_oos"]),
                       p4a_oos=bool(g.loc[pick, "p4a_oos"]),
                       sh_oos=float(g.loc[pick, f"sh_oos_{PCOST:g}"]),
                       cagr_oos=float(g.loc[pick, f"cagr_oos_{PCOST:g}"]),
                       dd_oos=float(g.loc[pick, f"dd_oos_{PCOST:g}"])))
    K8 = pd.DataFrame(k8)
    say("")
    say(f"  RULE 8 on the arm choice (pick on IS Sharpe, read OOS once): "
        f"4b_oos {int(K8.p4b_oos.sum())}/{len(K8)}   4a_oos {int(K8.p4a_oos.sum())}/{len(K8)}   "
        f"4b_full of the picked arm {int(K8.p4b_full.sum())}/{len(K8)}")
    if int(K8.p4b_oos.sum()):
        say("  rule-8 picks that clear 4b out of sample:")
        say(K8[K8.p4b_oos].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    else:
        say("  no rule-8 pick clears 4b out of sample on any panel.")

    say("")
    say("=" * 110)
    say("VERDICT")
    say("=" * 110)
    oos = CL[(CL.rung == PCOST) & (CL.target == "OOS")]
    isc = CL[(CL.rung == PCOST) & (CL.target == "IS")]
    usable = bool((oos.lift > 0).any() and (oos[oos.lift > 0].perm_p < 0.05).any())
    say(f"  T_IS  (what 458 fitted on): best lift over base rate {isc.lift.max():+.3f} "
        f"(min permutation p {isc.perm_p.min():.3f})")
    say(f"  T_OOS (what an admission test must do): best lift {oos.lift.max():+.3f} "
        f"(min permutation p {oos.perm_p.min():.3f})")
    say(f"  corr(D_is, D_oos) on the fresh panels = {r_flip:+.3f}; sign agrees {same:.1%}")
    say(f"  => the gate hit rate is {'a usable' if usable else 'NOT a usable'} pre-registered "
        "panel admission test.")
    say(f"  PROTOCOL: 4a {int(G.p4a_full.sum())}/{len(G)}, 4b {int(G.p4b_full.sum())}/{len(G)}.")
    say(f"  [{time.time() - t0:.1f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

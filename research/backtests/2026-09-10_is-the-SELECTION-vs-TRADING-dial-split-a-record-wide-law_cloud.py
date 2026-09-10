#!/usr/bin/env python3
"""Idea 624 — is the SELECTION-vs-TRADING dial split a record-wide LAW?   (cloud, 2026-09-10)

QUEUE 624: "idea 621 found a rule-8 pick beats the NO-DIAL control in 11 of 12 cells when the dial
selects HOLDINGS (n, vol cap) and in 20 of 36 when it only changes trading, exposure or gate width
(lambda, cadence, gross, band; band is a net loss), on six dials and 48 cells.  Re-cut the record's
committed rule-8 picks by this two-class split and test whether the CLASS, not the DIAL, predicts
whether the pick survives its own default.  Max 2 params (dial class, control form)."

WHAT IS ACTUALLY BEING TESTED
  Idea 621's number is real (it reproduces here to the cell — see G5).  The question this file asks
  is whether the LABEL carries the information, or whether "SELECTION" is just a name for the two
  dials that happened to win.  Three things have to be true for the split to be a LAW:

    L1  BETWEEN.  The class gap survives on a wider cell population than the 48 it was found on.
    L2  WITHIN.   Dials inside a class must agree.  If n and volcap disagree with each other as
                  much as SELECTION disagrees with TRADING, the predictor is the dial, not the class.
    L3  NOT-A-CONFOUND.  In idea 621 every one of the 12 SELECTION cells sits on the TOP20 (ranked)
                  book, because n and volcap were only ever run there — class is perfectly
                  confounded with BOOK in the original reading.  The gap must survive a
                  BOOK-MATCHED re-cut.

  L3 is why this file cannot be a pure re-read of 621's committed CSV: the confound is un-breakable
  inside that file's own grid.  The fix is one construction change — VOLCAP is defined on the BAND
  book too, using the BAND book's own native exposure mechanism (a capped name's weight goes to
  CASH exactly the way a gated-out name's does, denominator unchanged), so it selects HOLDINGS
  without touching the exposure rule.  G6 asserts the new dial's off-rung is an EXACT no-op against
  idea 621's band_book, so nothing already published is disturbed.  n stays TOP20-only: there is no
  way to cap the count on an un-ranked de-grossing book without also moving its gross, and a dial
  that moves gross is not a clean SELECTION dial.

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 DIAL CLASS: SELECTION = {n, volcap} (changes WHICH names are held) vs TRADING = {lambda,
     cadence, gross, band} (changes only how/when/how much).  The assignment is idea 621's own,
     taken verbatim, and it is the object of study — the permutation test below re-labels it.
  P2 CONTROL FORM: what "no dial" means, both reported everywhere.
       DEFAULT  the record's own live default for that dial ON THAT BOOK (n=20, lambda=1.00,
                cadence=W, gross=0.75, band=0.03, volcap=0.60 on TOP20 but 9.99 on BAND, because
                RULES v2 carries NO vol filter — transplanting 0.60 there would invent a default
                the record never had; the 0.60-on-BAND reading is printed as a sensitivity line);
       MEDIAN   the midpoint rung of the dial's own published ladder.
  Panels (u56 / broad136 / small439), books (TOP20 / BAND), the cadence axis and the cost rungs are
  REPORTED axes, never selected on.  Every grid point is written to .grid.csv.
  The ONLY selection anywhere in this file is PROTOCOL rule 8 itself, which is the object of study.

GATES (run before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest`, returns AND turnover, D and W, 3 panels.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=25).
  G3 the DEFAULT control arm is IN the ladder for every (dial, book).
  G4 the IS and OOS windows are disjoint and jointly exhaust the sample.
  G5 REPRODUCTION: idea 621's committed .cells.csv must give SELECTION 11/12 and TRADING 20/36 at
     the 10 bps rung — re-derived from its CSV, not restated from its prose.
  G6 NO-OP: band_book(volcap=9.99) is EXACTLY idea 621's band_book on all three panels.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents.  SMALL439 additionally drops
    every ticker with max_1d_move >= 1.0 in data/small_meta.csv before anything runs, and is a
    since-2010 panel of names that exist TODAY under $2B — its levels are not investable history
    and only WITHIN-panel arm-minus-arm contrasts are read off it.
  * Idea 412: a cadence has a PHASE.  Cadence rungs are the record's calendar conventions (D/W/M/Q)
    at phase 0 only; the cadence family's OOS numbers carry a phase nuisance (SD 0.0461 for Q).
  * The class populations are UNBALANCED by construction (2 dials vs 4).  Every pooled rate is
    therefore also reported per dial and per book, and the headline test is a permutation over dial
    labels, which is exact under the unbalanced design.
  * Idea 321: MaxDD is one number off one path.  Idea 126: t+1 execution, 10 bps default rung.
  * Ideas 527/531: 4b is in practice a DD-cap test on ungated momentum books; both KEEP paths are
    priced on every arm anyway, as PROTOCOL requires.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .grid.csv, .cells.csv, .walkforward.csv, .perm.csv.
"""
from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_is-the-SELECTION-vs-TRADING-dial-split-a-record-wide-law_cloud"
OUT = ROOT / "research" / "backtests"
I621 = OUT / "2026-09-10_does-any-published-rule-8-pick-survive-the-NO-DIAL-control_cloud.cells.csv"

GROSS = 0.75                       # the record's book gross (idea 94 / 412)
NTOP = 20                          # the record's default concentration
BAND = 0.03                        # RULES v2 clause 2
VOLCAP = 0.60                      # RULES v1 max_vol
NOCAP = 9.99                       # the "no vol filter" rung — RULES v2's own position
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60            # 4b CAGR floor and MaxDD cap as fractions of SPY's
PCOST = 10.0                       # PROTOCOL's own rung
RUNGS = [0.0, 10.0, 25.0, 50.0]    # reported cost ladder

# ---- ladders lifted verbatim from idea 621 --------------------------------------------------
LADDERS = {
    "n":       [5, 10, 15, 20, 30, 40, 60],
    "lambda":  [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06],
    "cadence": ["D", "W", "M", "Q"],
    "gross":   [0.25, 0.50, 0.75, 1.00],
    "band":    [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "volcap":  [0.30, 0.45, 0.60, 0.80, 1.00, NOCAP],
}
DEFAULTS = {"n": NTOP, "lambda": 1.00, "cadence": "W", "gross": GROSS,
            "band": BAND, "volcap": VOLCAP}
# per-(dial, book) default overrides: RULES v2 (the BAND book) carries NO vol filter.
DEFAULT_BOOK = {("volcap", "BAND"): NOCAP}
# P1: idea 621's own class assignment, verbatim.
CLASS = {"n": "SELECTION", "volcap": "SELECTION",
         "lambda": "TRADING", "cadence": "TRADING", "gross": "TRADING", "band": "TRADING"}
# THE construction change vs idea 621: volcap now runs on BAND too, breaking class x book.
BOOKS_FOR = {"n": ["TOP20"], "volcap": ["TOP20", "BAND"],
             "lambda": ["TOP20", "BAND"], "cadence": ["TOP20", "BAND"],
             "gross": ["TOP20", "BAND"], "band": ["BAND"]}
CADENCE_AXIS = ["W", "D"]
PANELS = ["u56", "broad136", "small439"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dflt(dial, book):
    return DEFAULT_BOOK.get((dial, book), DEFAULTS[dial])


# =====================================================================================
# runner — idea 621's segment form, verbatim (gated below)
# =====================================================================================
def _mask(idx, freq):
    return rebalance_mask(idx, freq).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    """engine.backtest's drift algebra, one pass per rebalance SEGMENT."""
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


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: an EWMA of the raw target with gross restored
    daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# =====================================================================================
# books
# =====================================================================================
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20_of(sub):
    return sub.pct_change().rolling(20).std() * np.sqrt(252)


def top_book(comp, n, gross, volcap, v20):
    """Top-n of the composite among SCORED names passing the vol cap, equal weight at gross/n."""
    c = comp.where(v20 < volcap) if volcap < 9.0 else comp
    r = c.rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def band_book_621(sub, comp, band, gross):
    """Idea 621's band_book, COPIED VERBATIM from its committed script, so G6 compares this file's
    extended book against the published one rather than against itself."""
    ma = sub.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=sub.index, columns=sub.columns)
    raw = raw.mask(sub > ma * (1 + band), 1.0).mask(sub < ma * (1 - band), 0.0)
    inn = raw.ffill().fillna(0.0) > 0.5
    e = comp.notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(inn & comp.notna(), 0.0)


def band_book(sub, comp, band, gross, v20=None, volcap=NOCAP):
    """RULES v2 clause 2 on the panel: every name inside the 200d +/-band held at gross/N, gated-out
    weight to CASH (de-grossed, never re-spread).  N = names PRICED that day, so it does not move
    with the gate.  volcap < 9.0 removes a capped name the same way the gate removes an out-of-band
    one — to cash, denominator unchanged — so it selects HOLDINGS without touching the exposure
    rule.  At volcap = 9.99 this is EXACTLY idea 621's band_book (G6)."""
    ma = sub.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=sub.index, columns=sub.columns)
    raw = raw.mask(sub > ma * (1 + band), 1.0).mask(sub < ma * (1 - band), 0.0)
    inn = raw.ffill().fillna(0.0) > 0.5
    e = comp.notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    hold = inn & comp.notna()
    if volcap < 9.0:
        hold = hold & (v20 < volcap)
    return ew.where(hold, 0.0)


def build(book, panel, val_of):
    """Return (weights, cadence) for one grid point.  val_of maps a dial name to its value."""
    px, sub, comp, v20 = panel
    n = int(val_of("n"))
    lam = float(val_of("lambda"))
    g = float(val_of("gross"))
    bd = float(val_of("band"))
    vc = float(val_of("volcap"))
    W = (top_book(comp, n, g, vc, v20) if book == "TOP20"
         else band_book(sub, comp, bd, g, v20, vc))
    W = smooth(W, lam)
    return W.reindex(columns=px.columns).fillna(0.0), str(val_of("cadence"))


# =====================================================================================
# metrics helpers (idea 621's, verbatim)
# =====================================================================================
def sh(r):
    return metrics(r)["Sharpe"]


def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def bars_of(spy):
    h1, h2 = halves(spy)
    m = metrics(spy)
    return dict(s1=h1, s2=h2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=sh(spy.loc[OOS_START:]),
                sdd_oos=metrics(spy.loc[OOS_START:])["MaxDD"],
                scagr_oos=metrics(spy.loc[OOS_START:])["CAGR"])


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


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def panel_of(pk):
    if pk == "u56":
        px, ndrop = load_universe(), 0
    elif pk == "broad136":
        px, ndrop = load_universe(broad=True), 0
    else:
        px, ndrop = small_panel()
    px = px.dropna(how="all").ffill()
    sub = px.drop(columns=["SPY"], errors="ignore")
    return (px, sub, composite(sub), vol20_of(sub)), ndrop


_BASE: dict = {}


def base_of(pk, panel):
    """SPY bars and the live RULES v2 baseline return path for one panel (cached)."""
    if pk not in _BASE:
        px = panel[0]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b = bars_of(spy)
        b["spy_oos"] = spy.loc[OOS_START:]
        r0, to = run(px, rules_v2_weights(px), "W")
        _BASE[pk] = (b, (r0 - to * PCOST / 1e4).loc[start:], spy)
    return _BASE[pk]


# =====================================================================================
# the grid
# =====================================================================================
def grid_rows(pk, panel, dial, book, cad_axis):
    px = panel[0]
    start = px.index[260]
    b, baser, _spy = base_of(pk, panel)
    out = []
    for cad in cad_axis:
        for v in LADDERS[dial]:
            def val_of(name, v=v, cad=cad, book=book):
                if name == dial:
                    return v
                if name == "cadence":
                    return cad
                return dflt(name, book)
            W, freq = build(book, panel, val_of)
            r0, to = run(px, W, freq)
            r0, to = r0.loc[start:], to.loc[start:]
            rec = dict(panel=pk, dial=dial, dial_class=CLASS[dial], book=book, cad_axis=cad,
                       value=str(v), is_default=(v == dflt(dial, book)),
                       turnover=float(to.sum() / (len(to) / 252.0)))
            for c in RUNGS:
                r = r0 - to * c / 1e4
                m, mo = metrics(r), metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                rec[f"sh_full_{c:g}"] = m["Sharpe"]
                rec[f"cagr_full_{c:g}"] = m["CAGR"]
                rec[f"dd_full_{c:g}"] = m["MaxDD"]
                rec[f"h1_{c:g}"], rec[f"h2_{c:g}"] = h1, h2
                rec[f"sh_is_{c:g}"] = sh(r.loc[:IS_END])
                rec[f"sh_oos_{c:g}"] = mo["Sharpe"]
                rec[f"cagr_oos_{c:g}"] = mo["CAGR"]
                rec[f"dd_oos_{c:g}"] = mo["MaxDD"]
                if c == PCOST:
                    rec["p4a_full"] = pass4a(r, baser)
                    rec["p4b_full"] = pass4b(r, b, "full")
                    rec["p4a_oos"] = pass4a(r, baser, "oos")
                    rec["p4b_oos"] = pass4b(r, b, "oos")
            out.append(rec)
    return out


def cells_from(rows, pk, dial, book, cad_axis):
    """PROTOCOL rule 8 per (panel, dial, book, cadence rung, cost rung): choose on IS Sharpe
    (2009-2016), read OOS (2017-2026) once, set against the two no-dial control forms."""
    D = pd.DataFrame(rows)
    cells = []
    for cad in cad_axis:
        sl = D[D.cad_axis == cad]
        for c in RUNGS:
            isc, oosc = f"sh_is_{c:g}", f"sh_oos_{c:g}"
            pick = sl.loc[sl[isc].idxmax()]
            ctl_def = sl[sl.is_default].iloc[0]
            med_v = str(LADDERS[dial][len(LADDERS[dial]) // 2])
            ctl_med = sl[sl.value == med_v].iloc[0]
            oracle = sl.loc[sl[oosc].idxmax()]
            cells.append(dict(
                panel=pk, dial=dial, dial_class=CLASS[dial], book=book, cad=cad, cost=c,
                pick=pick.value, pick_is=pick[isc], pick_oos=pick[oosc],
                def_val=ctl_def.value, def_oos=ctl_def[oosc],
                med_val=ctl_med.value, med_oos=ctl_med[oosc],
                oracle=oracle.value, oracle_oos=oracle[oosc],
                d_def=pick[oosc] - ctl_def[oosc],
                d_med=pick[oosc] - ctl_med[oosc],
                regret=oracle[oosc] - pick[oosc],
                pick_is_default=bool(pick.value == ctl_def.value),
                pick_cagr_oos=pick[f"cagr_oos_{c:g}"], pick_dd_oos=pick[f"dd_oos_{c:g}"],
                def_cagr_oos=ctl_def[f"cagr_oos_{c:g}"], def_dd_oos=ctl_def[f"dd_oos_{c:g}"],
                pick_sh_full=pick[f"sh_full_{c:g}"], pick_h1=pick[f"h1_{c:g}"],
                pick_h2=pick[f"h2_{c:g}"], pick_cagr_full=pick[f"cagr_full_{c:g}"],
                pick_dd_full=pick[f"dd_full_{c:g}"],
                pick_4a=bool(pick.p4a_full), pick_4b=bool(pick.p4b_full),
                def_4a=bool(ctl_def.p4a_full), def_4b=bool(ctl_def.p4b_full),
                pick_4a_oos=bool(pick.p4a_oos), pick_4b_oos=bool(pick.p4b_oos),
                def_4a_oos=bool(ctl_def.p4a_oos), def_4b_oos=bool(ctl_def.p4b_oos),
            ))
    return cells


# =====================================================================================
# the tests
# =====================================================================================
def rate(s):
    return float((s > 0).mean()) if len(s) else float("nan")


def gap_for(P, sel_dials, col="d_def"):
    """Between-class win-rate gap for an arbitrary 2-dial SELECTION labelling."""
    m = P.dial.isin(sel_dials)
    if not m.any() or m.all():
        return float("nan")
    return rate(P.loc[m, col]) - rate(P.loc[~m, col])


def perm_test(P, sel_dials, col="d_def"):
    """EXACT permutation over dial labels: every way to call k of the dials PRESENT IN THIS SCOPE
    "SELECTION", where k is how many of the true SELECTION dials this scope actually carries (2
    pooled and on TOP20, 1 on BAND, where `n` has no instrument).  Respects the clustering of cells
    inside a dial, which a cell-level shuffle does not.  Reports the observed labelling's rank and
    p = #{g >= g_obs} / #labellings."""
    dials = sorted(P.dial.unique())
    sel = sorted(set(sel_dials) & set(dials))
    k = len(sel)
    if k == 0 or k == len(dials):
        return pd.DataFrame(columns=["sel", "gap"]), float("nan"), 0, float("nan"), float("nan")
    rows = [dict(sel=",".join(c), gap=gap_for(P, set(c), col))
            for c in itertools.combinations(dials, k)]
    R = pd.DataFrame(rows).sort_values("gap", ascending=False).reset_index(drop=True)
    obs = gap_for(P, set(sel), col)
    p_one = float((R.gap >= obs - 1e-12).mean())
    p_two = float((R.gap.abs() >= abs(obs) - 1e-12).mean())
    rank = int(R.index[R.sel == ",".join(sel)][0]) + 1
    return R, obs, rank, p_one, p_two


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 624 — is the SELECTION-vs-TRADING dial split a record-wide LAW?   (cloud 2026-09-10)")
    say("=" * 108)

    panels = {}
    for pk in PANELS:
        p, nd = panel_of(pk)
        panels[pk] = p
        px = p[0]
        say(f"  {pk:>9}: {px.shape[1]} cols  {px.index[0].date()} .. {px.index[-1].date()}"
            + (f"  ({nd} dropped for max_1d_move>=1.0)" if nd else ""))

    # ---------------- GATES ----------------
    say("\nGATES")
    ok = True
    for pk, panel in panels.items():
        px = panel[0]
        W, _ = build("TOP20", panel, lambda k: DEFAULTS[k])
        start = px.index[260]
        for f in ("D", "W"):
            rf, tf = run(px, W, f)
            e0 = backtest(px, W, cost_bps=0.0, freq=f)
            dr = float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max())
            dt = float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())
            say(f"  G1 {pk:>9} {f}: max|dr| {dr:.3e}  max|dto| {dt:.3e}")
            ok &= dr < 1e-12 and dt < 1e-12
        rf, tf = run(px, W, "W")
        e25 = backtest(px, W, cost_bps=25.0, freq="W")
        d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G2 {pk:>9}  : rung identity max|dr| {d2:.3e}")
        ok &= d2 < 1e-12
    for d in LADDERS:
        for bk in BOOKS_FOR[d]:
            inlad = dflt(d, bk) in LADDERS[d]
            say(f"  G3 {d:>8} on {bk:>5}: default {dflt(d, bk)} in ladder -> {inlad}")
            ok &= inlad
    say(f"  G4 windows: IS <= {IS_END}, OOS >= {OOS_START}, disjoint and exhaustive -> True")

    say("  G5 REPRODUCTION of idea 621's headline from its own committed .cells.csv:")
    if I621.exists():
        c621 = pd.read_csv(I621)
        p621 = c621[c621.cost == PCOST]
        for cls in ("SELECTION", "TRADING"):
            g = p621[p621.dial.map(CLASS) == cls]
            say(f"     {cls:>9}: {int((g.d_def > 0).sum())}/{len(g)} "
                f"(median {g.d_def.median():+.4f})   target 11/12 and 20/36")
        sel12 = p621[p621.dial.map(CLASS) == "SELECTION"]
        say(f"     CONFOUND CHECK: SELECTION cells on the TOP20 book: "
            f"{int((sel12.book == 'TOP20').sum())}/{len(sel12)} — "
            f"class is {'PERFECTLY confounded with book' if (sel12.book == 'TOP20').all() else 'not confounded'} "
            f"in idea 621's grid")
        g5 = (int((p621[p621.dial.map(CLASS) == "SELECTION"].d_def > 0).sum()) == 11
              and int((p621[p621.dial.map(CLASS) == "TRADING"].d_def > 0).sum()) == 20)
        say(f"     G5 -> {'PASS' if g5 else 'FAIL'}")
        ok &= g5
    else:
        say("     idea 621 .cells.csv NOT PRESENT — reproduction not attempted (reported, not faked)")
        ok = False
    for pk, panel in panels.items():
        _px, sub, comp, v20 = panel
        a = band_book(sub, comp, BAND, GROSS, v20, NOCAP)
        b = band_book_621(sub, comp, BAND, GROSS)
        d6 = float((a - b).abs().to_numpy().max())
        say(f"  G6 {pk:>9}  : band_book(volcap=9.99) vs idea 621's band_book  max|dW| {d6:.3e}")
        ok &= d6 == 0.0
    say(f"  GATES {'PASS' if ok else 'FAIL'}")

    # ---------------- GRID + rule 8 ----------------
    say("\nGRID — every point reported (.grid.csv); rule 8 run per cell (.cells.csv)")
    G, cells = [], []
    for pk, panel in panels.items():
        for dial in LADDERS:
            for book in BOOKS_FOR[dial]:
                cax = ["W"] if dial == "cadence" else CADENCE_AXIS
                rows = grid_rows(pk, panel, dial, book, cax)
                G += rows
                cells += cells_from(rows, pk, dial, book, cax)
                say(f"    {pk:>9} {dial:>8} {book:>5} [{CLASS[dial][:3]}]: {len(rows)} points"
                    f"   [{time.time()-t0:5.0f}s]")
    GD = pd.DataFrame(G)
    CD = pd.DataFrame(cells)
    GD.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    CD.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    CD.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"  grid points {len(GD)}   rule-8 cells {len(CD)}   "
        f"(at {PCOST:g} bps: {len(CD[CD.cost == PCOST])})")

    P = CD[CD.cost == PCOST].copy()

    # ---------------- L1 BETWEEN ----------------
    say("\n" + "=" * 108)
    say("L1 BETWEEN — does the class gap survive the WIDER cell population?  (10 bps rung)")
    say("=" * 108)
    for col, lab in (("d_def", "DEFAULT control"), ("d_med", "MEDIAN-rung control")):
        say(f"  P2 = {lab}")
        t = P.groupby("dial_class").agg(cells=(col, "size"),
                                        wins=(col, lambda s: int((s > 0).sum())),
                                        median=(col, "median"), mean=(col, "mean"))
        t["rate"] = t.wins / t.cells
        say("    " + t.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
        say(f"    GAP (SEL - TRA) in win rate: {gap_for(P, {'n', 'volcap'}, col):+.4f}")

    # ---------------- L2 WITHIN ----------------
    say("\n" + "=" * 108)
    say("L2 WITHIN — do the dials INSIDE a class agree?  (10 bps, DEFAULT control)")
    say("=" * 108)
    d = P.groupby(["dial_class", "dial"]).agg(cells=("d_def", "size"),
                                              wins=("d_def", lambda s: int((s > 0).sum())),
                                              median=("d_def", "median"))
    d["rate"] = d.wins / d.cells
    say(d.to_string(float_format=lambda x: f"{x:.4f}"))
    dr = d.reset_index()
    for cls in ("SELECTION", "TRADING"):
        q = dr[dr.dial_class == cls]
        say(f"  {cls:>9}: per-dial win rate spans {q.rate.min():.3f} .. {q.rate.max():.3f} "
            f"(width {q.rate.max() - q.rate.min():.3f}) over {len(q)} dials")
    within = dr.groupby("dial_class").rate.agg(lambda s: s.max() - s.min())
    between = abs(dr[dr.dial_class == "SELECTION"].rate.mean()
                  - dr[dr.dial_class == "TRADING"].rate.mean())
    say(f"  BETWEEN-class gap of dial-level rates {between:.4f}  vs  max WITHIN-class spread "
        f"{within.max():.4f}   -> {'between > within' if between > within.max() else 'WITHIN SPREAD IS LARGER — the dial, not the class'}")

    # ---------------- L3 NOT-A-CONFOUND ----------------
    say("\n" + "=" * 108)
    say("L3 NOT-A-CONFOUND — the BOOK-MATCHED re-cut  (10 bps, DEFAULT control)")
    say("=" * 108)
    say("  class x book cell counts (idea 621 had SELECTION on TOP20 only):")
    say("    " + pd.crosstab(P.dial_class, P.book).to_string().replace("\n", "\n    "))
    for bk in ("TOP20", "BAND"):
        q = P[P.book == bk]
        if q.empty:
            continue
        t = q.groupby("dial_class").agg(cells=("d_def", "size"),
                                        wins=("d_def", lambda s: int((s > 0).sum())),
                                        median=("d_def", "median"))
        t["rate"] = t.wins / t.cells
        say(f"  within {bk}:")
        say("    " + t.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
        if t.index.nunique() == 2:
            say(f"    book-matched GAP (SEL - TRA): "
                f"{t.loc['SELECTION', 'rate'] - t.loc['TRADING', 'rate']:+.4f}")
    say("  by book, pooled over class (is the BOOK the predictor?):")
    tb = P.groupby("book").agg(cells=("d_def", "size"),
                               wins=("d_def", lambda s: int((s > 0).sum())),
                               median=("d_def", "median"))
    tb["rate"] = tb.wins / tb.cells
    say("    " + tb.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    # ---------------- the permutation test ----------------
    say("\n" + "=" * 108)
    say("EXACT PERMUTATION over dial labels — every same-size SELECTION labelling of the dials")
    say("present in each scope.  If the record's own labelling is not extreme, the CLASS carries no")
    say("information the DIAL identities do not already carry.")
    say("=" * 108)
    perm_all = []
    for col, lab in (("d_def", "DEFAULT"), ("d_med", "MEDIAN")):
        for scope, Q in (("pooled", P), ("TOP20-only", P[P.book == "TOP20"]),
                         ("BAND-only", P[P.book == "BAND"])):
            R, obs, rank, p1, p2 = perm_test(Q, {"n", "volcap"}, col)
            R["control"], R["scope"] = lab, scope
            perm_all.append(R)
            say(f"  {lab:>7} / {scope:>10}: observed gap {obs:+.4f}   rank {rank}/{len(R)}   "
                f"p(one-sided) {p1:.3f}   p(two-sided) {p2:.3f}")
            say("      top-3 labellings: " + "; ".join(
                f"{r.sel} {r.gap:+.3f}" for r in R.head(3).itertuples()))
    PM = pd.concat(perm_all, ignore_index=True)
    PM.to_csv(OUT / f"{STEM}.perm.csv", index=False)

    say("\n  THE COMPETING PREDICTOR — class gap vs book gap on the SAME 54 cells (DEFAULT, 10 bps):")
    say(f"    CLASS (SELECTION - TRADING): {gap_for(P, {'n', 'volcap'}, 'd_def'):+.4f}")
    bg = rate(P.loc[P.book == "TOP20", "d_def"]) - rate(P.loc[P.book == "BAND", "d_def"])
    say(f"    BOOK  (TOP20     - BAND   ): {bg:+.4f}")
    say(f"    -> the BOOK gap is {abs(bg) / max(abs(gap_for(P, {'n', 'volcap'}, 'd_def')), 1e-9):.1f}x "
        f"the CLASS gap")

    # ---------------- reported axes ----------------
    say("\n" + "=" * 108)
    say("REPORTED AXES — cost rung and panel (never selected on)")
    say("=" * 108)
    say("  by cost rung (DEFAULT control):")
    say("    " + CD.groupby(["cost", "dial_class"]).agg(
        cells=("d_def", "size"), wins=("d_def", lambda s: int((s > 0).sum())),
        median=("d_def", "median")).to_string(
            float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    say("  by panel (DEFAULT control, 10 bps):")
    say("    " + P.groupby(["panel", "dial_class"]).agg(
        cells=("d_def", "size"), wins=("d_def", lambda s: int((s > 0).sum())),
        median=("d_def", "median")).to_string(
            float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    say("  SENSITIVITY — if BAND's volcap default were transplanted to 0.60 instead of 9.99:")
    gb = GD[(GD.dial == "volcap") & (GD.book == "BAND")]
    alt = []
    for (pk, cad), sl in gb.groupby(["panel", "cad_axis"]):
        for c in RUNGS:
            isc, oosc = f"sh_is_{c:g}", f"sh_oos_{c:g}"
            pick = sl.loc[sl[isc].idxmax()]
            a = sl[sl.value == "0.6"]
            if a.empty:
                continue
            alt.append(dict(panel=pk, cad=cad, cost=c, d_alt=pick[oosc] - a.iloc[0][oosc]))
    A = pd.DataFrame(alt)
    if not A.empty:
        a10 = A[A.cost == PCOST]
        say(f"    volcap/BAND vs a 0.60 default: {int((a10.d_alt > 0).sum())}/{len(a10)} at 10 bps "
            f"(median {a10.d_alt.median():+.4f});  vs the native 9.99 default: "
            f"{int((P[(P.dial=='volcap') & (P.book=='BAND')].d_def > 0).sum())}/"
            f"{len(P[(P.dial=='volcap') & (P.book=='BAND')])}")

    # ---------------- PROTOCOL 4: levels, halves, OOS, both KEEP paths ----------------
    say("\n" + "=" * 108)
    say("PROTOCOL 4 — LEVELS at 10 bps: rule-8 pick vs NO-DIAL vs RULES v2 vs SPY")
    say("=" * 108)
    for pk, panel in panels.items():
        b, bt, spy = base_of(pk, panel)
        mo_s, mo_b = metrics(spy.loc[OOS_START:]), metrics(bt.loc[OOS_START:])
        mf_s, mf_b = metrics(spy), metrics(bt)
        say(f"  {pk}")
        say(f"    {'SPY':<26} full CAGR {mf_s['CAGR']:7.2%} Sh {mf_s['Sharpe']:6.3f} "
            f"DD {mf_s['MaxDD']:7.2%} | H1/H2 {halves(spy)[0]:6.3f}/{halves(spy)[1]:6.3f} | "
            f"OOS CAGR {mo_s['CAGR']:7.2%} Sh {mo_s['Sharpe']:6.3f} DD {mo_s['MaxDD']:7.2%}")
        say(f"    {'RULES v2 baseline':<26} full CAGR {mf_b['CAGR']:7.2%} Sh {mf_b['Sharpe']:6.3f} "
            f"DD {mf_b['MaxDD']:7.2%} | H1/H2 {halves(bt)[0]:6.3f}/{halves(bt)[1]:6.3f} | "
            f"OOS CAGR {mo_b['CAGR']:7.2%} Sh {mo_b['Sharpe']:6.3f} DD {mo_b['MaxDD']:7.2%}")
        for cls in ("SELECTION", "TRADING"):
            q = P[(P.panel == pk) & (P.dial_class == cls)]
            if q.empty:
                continue
            say(f"    {'pick  [' + cls + '] median':<26} full CAGR {q.pick_cagr_full.median():7.2%} "
                f"Sh {q.pick_sh_full.median():6.3f} DD {q.pick_dd_full.median():7.2%} | "
                f"H1/H2 {q.pick_h1.median():6.3f}/{q.pick_h2.median():6.3f} | "
                f"OOS CAGR {q.pick_cagr_oos.median():7.2%} Sh {q.pick_oos.median():6.3f} "
                f"DD {q.pick_dd_oos.median():7.2%}")
            say(f"    {'no-dial [' + cls + '] median':<26} full CAGR "
                f"{'':7} {'':6} {'':7} | {'':6} {'':6} | "
                f"OOS CAGR {q.def_cagr_oos.median():7.2%} Sh {q.def_oos.median():6.3f} "
                f"DD {q.def_dd_oos.median():7.2%}")

    say("\nKEEP PATHS (PROTOCOL 4, both priced on every arm, 10 bps)")
    say(f"  ALL grid points  : 4a {int(GD.p4a_full.sum())}/{len(GD)}   "
        f"4b {int(GD.p4b_full.sum())}/{len(GD)}   (OOS window: 4a {int(GD.p4a_oos.sum())}/{len(GD)}"
        f"   4b {int(GD.p4b_oos.sum())}/{len(GD)})")
    for cls in ("SELECTION", "TRADING"):
        q = P[P.dial_class == cls]
        say(f"  {cls:>9} picks: 4a {int(q.pick_4a.sum())}/{len(q)}  4b {int(q.pick_4b.sum())}/{len(q)}"
            f"   |  its no-dial controls: 4a {int(q.def_4a.sum())}/{len(q)}  "
            f"4b {int(q.def_4b.sum())}/{len(q)}")
    kb = GD[GD.p4b_full]
    if not kb.empty:
        say("  4b passers (full sample), by panel/book/dial:")
        say("    " + kb.groupby(["panel", "book", "dial"]).size().to_string().replace("\n", "\n    "))

    say(f"\nwrote .grid.csv .cells.csv .walkforward.csv .perm.csv   [{time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 828 - "is-there-a-BOOK-FORM-whose-ENTRY-DATE-pass-share-clears-0.80-at-a-3-YEAR-horizon"
(cloud, 2026-09-12).

WHY THIS RUN EXISTS
-------------------
Idea 829 scored the standing 4b candidate (RULES v2 band 3%, gross 1.00) on every ENTRY DATE
rather than the record's one fixed window and found its joint window-local 4b pass share is
**0.3977 at a 3-year holding horizon**.  Its diagnosis: the candidate's own CAGR is nearly
constant across entry windows (median 10.63%-11.03% at every horizon) while SPY's runs
9.70%-22.15%, so PROTOCOL 4b's `CAGR >= 70% of SPY's` fails precisely when the benchmark runs
hot.  Three years is the realistic capital horizon and NO book in the record has ever been scored
on one.

    THE QUESTION.  Is there a committed BOOK FORM whose entry-window 4b pass share clears 0.80 at
    H = 756 trading days - i.e. a form whose CAGR CO-MOVES with the benchmark instead of being
    flat - and if so, what does it pay for that?

This is not a prose audit.  Every number below is a price series.

The forms (tuned parameter 1 - the whole set is declared here, before the run, and EVERY cell is
reported; no form is dropped after the fact)
    EW         equal weight EVERY priced name at g/N.  No gate at all.  The co-movement ceiling -
               a book that IS the panel must track the benchmark by construction.
    EWALL-RS   idea 28/42/336/399's EWALL: equal weight every name above its own 200d MA with
               vol20 < 0.60, RE-SPREAD to g/E_t so the book is always at gross g.
    EWALL-DG   the same eligibility gate, DE-GROSSED: g/N per eligible name, gated-out weight to
               cash.  (RS and DG are the record's two gross conventions - ideas 562/767/773.)
    MA-DG      RULES v2, the LIVE form: hold every name inside the 200d +/-3% band at g/N,
               gated-out weight to CASH, never re-spread.  At g = 0.75 this IS the live book and
               at g = 1.00 it IS idea 829's standing candidate, so both sit inside the grid.
    MA-RS      the same band membership, gross RE-SPREAD over the in-band names.
    TOP20      the record's first 4b KEEP (2026-09-04): the composite score with NO vol scaler,
               ranked among eligible names, top 20 equal weight at g/20, de-grossed when fewer
               than 20 are eligible.
    LOWVOL20   the 20 lowest-vol20 eligible names, equal weight at g/20, de-grossed.  The record's
               rule-8 IS pick on several panels (idea 823), carried here as a reported control.
    + RULES v1 (the pre-2026-09-06 live book) and SPY, as PROTOCOL 3 comparands.

Tuned parameter 2 - GROSS in {0.50, 0.75, 1.00}, applied to all seven forms.  That is 21 cells,
every one reported at every horizon, spacing, cost rung and panel.  Nothing else is tuned:
horizon, entry spacing, cost, band width and panel are REPORTED axes, fixed at the record's
committed values.

Declared BEFORE the run
    headline cell   panel U56, H = 756d (the queue says "3-year"), entry spacing s = 21d,
                    cost 10 bps (PROTOCOL 2).
    reported        H in {756, 1260}, s in {21, 63}, cost in {10, 25} bps, panels U56 / B136 /
                    SMALL<n>.

Pre-registered hypotheses (each stated so it can fail)
    H_828    THE QUEUE'S.  At least one (form, gross) cell clears joint window-local 4b pass
             share >= 0.80 at the headline cell.
    H_SLOPE  THE MECHANISM.  Regress each cell's window CAGR on SPY's window CAGR across entry
             dates; 4b's floor is a RATIO, so a cell is only safe if the slope b >= 0.70.
             Spearman(b, pass_4b) over the 21 cells >= +0.50.
    H_COST   THE PRICE OF CO-MOVEMENT.  A form that tracks the benchmark also inherits its
             drawdown, and 4b caps MaxDD at 60% of SPY's.  Spearman(b, leg_dd) <= 0.
    H_JOINT  NO FREE LUNCH.  No cell clears BOTH leg_cagr >= 0.80 AND leg_dd >= 0.80 at the
             headline cell.  If H_JOINT fails, that cell is a genuine KEEP-4b candidate for an
             arbitrary entrant and gets a memo.
    H_R8     PROTOCOL RULE 8.  Pick the best cell on IS ENTRY DATES ONLY (entry <= 2016-12-31),
             read it once on OOS entry dates (entry >= 2017-01-01).  Its OOS pass share is within
             0.15 of the OOS-best cell.

Window-local 4b (idea 829's convention, reproduced verbatim so the 0.3977 gate can bind)
    a window PASSES iff  Sharpe > SPY's  AND  both window halves' Sharpe > SPY's halves'
                     AND  MaxDD >= 0.60 * SPY's MaxDD (both negative, so >= is shallower)
                     AND  CAGR >= 0.70 * SPY's CAGR.

Reproduction gates, printed before any new number is read
    G1  fast_backtest == engine.backtest (returns AND turnover), 3 real books x 3 rungs
    G2  fast CAGR/Sharpe/MaxDD == engine.metrics on 200 real series
    G3  idea 829's committed entry-date headline: CAND g=1.00 joint 4b pass share 0.3977 at
        H = 756, s = 21 on U56 - this run's MA-DG g=1.00 cell must land on it
    G4  the committed candidate memo's fixed-window triple (11.52% / 1.1996 / -15.91% full,
        12.66% / 1.2740 / -15.91% OOS) and SPY (15.16% / 0.8860 / -33.72%)
    G5  idea 84's committed EWALL U56 g=0.85 @10bps triple
    G6  panel vintage stamp (data/prices_small.csv.gz is rewritten nightly - ideas 824/826)

SURVIVORSHIP: U56 and B136 are current constituents of `research/universe.json` /
`universe_broad.json`; the SMALL panel is current constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md).  All three bias every book AND every pass share upward, and the
small panel additionally re-states its own history nightly.  Nothing here is investment advice.

Writes: .console.txt .census.csv.gz .grid.csv .slope.csv .fixed.csv .walkforward.csv .result.md
"""
import sys
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import (load_universe, score, band_state, rules_v1_weights,  # noqa: E402
                      rules_v2_weights)
from engine import backtest, metrics, rebalance_mask  # noqa: E402

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

FREQ = "W"
MAX_VOL = 0.60
BAND = 0.03
COSTS = [10.0, 25.0]
COST_HEAD = 10.0
GROSSES = [0.50, 0.75, 1.00]            # tuned param 2
FORMS = ["EW", "EWALL-RS", "EWALL-DG", "MA-DG", "MA-RS", "TOP20", "LOWVOL20"]   # tuned param 1
HORIZONS = [756, 1260]
SPACINGS = [21, 63]
H_HEAD, S_HEAD = 756, 21                # declared before the run: the queue says "3-year"
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
BAR = 0.80
SLOPE_BAR = 0.70

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


def hdr(s):
    log("\n" + "=" * 175)
    log(s)
    log("=" * 175)


# ------------------------------------------------------------------ primitives
_ELIG = {}


def elig_vol(px):
    k = (id(px), px.shape, px.index[0], px.index[-1])
    if k not in _ELIG:
        _, above, vol20 = score(px)
        _ELIG[k] = (above & (vol20 < MAX_VOL), vol20)
    return _ELIG[k]


def _spread(mask, g):
    """RE-SPREAD: g split over the members, so the book is always at gross g."""
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def _degross(mask, priced, g):
    """DE-GROSS: g/N per member with N = instruments priced that day; the rest is CASH."""
    n = priced.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def form_weights(px, form, g):
    elig, vol20 = elig_vol(px)
    elig = elig.astype(float)
    priced = px.notna().astype(float)
    if form == "EW":
        return _degross(priced, priced, g)
    if form == "EWALL-RS":
        return _spread(elig, g)
    if form == "EWALL-DG":
        return _degross(elig, priced, g)
    if form == "MA-DG":
        return rules_v2_weights(px, band=BAND, gross=g)
    if form == "MA-RS":
        return _spread(band_state(px, BAND).astype(float).where(px.notna(), 0.0), g)
    if form == "TOP20":
        comp, _, _ = score(px, vol_scale=False)
        r = comp.where(elig > 0).rank(axis=1, ascending=False)
        return (r <= 20).astype(float) * (g / 20.0)
    if form == "LOWVOL20":
        r = vol20.where(elig > 0).rank(axis=1, ascending=True)
        return (r <= 20).astype(float) * (g / 20.0)
    raise ValueError(form)


def fast_backtest(prices, weights, cost_bps, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = (eq / np.maximum.accumulate(eq) - 1.0).min()
    vol = r.std(ddof=1) * np.sqrt(252.0)
    sh = (r.mean() * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


# ------------------------------------------------------------------ the entry-date census
def window_stats(r, ii, H):
    """(CAGR, Sharpe, h1 Sharpe, h2 Sharpe, MaxDD) for every entry index in ii."""
    eq = np.cumprod(1.0 + r)
    eqp = np.concatenate([[1.0], eq])                       # eqp[k] = value BEFORE day k
    cs = np.concatenate([[0.0], np.cumsum(r)])
    cs2 = np.concatenate([[0.0], np.cumsum(r * r)])
    half = H // 2

    def sh(i, j):
        n = (j - i).astype(float)
        m = (cs[j] - cs[i]) / n
        v = ((cs2[j] - cs2[i]) - n * m * m) / (n - 1.0)
        v = np.where(v > 1e-300, v, np.nan)
        return m * np.sqrt(252.0) / np.sqrt(v)

    jj = ii + H
    cagr = (eqp[jj] / eqp[ii]) ** (252.0 / H) - 1.0
    s_full = sh(ii, jj)
    s_h1 = sh(ii, ii + half)
    s_h2 = sh(ii + half, jj)
    dd = np.empty(len(ii))
    for a, i in enumerate(ii):
        e = eq[i:i + H]
        dd[a] = (e / np.maximum.accumulate(e) - 1.0).min()
    return cagr, s_full, s_h1, s_h2, dd


def run_panel(panel, px, head_panel):
    start = px.index[260]
    eval_idx = px.loc[start:].index
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:].values
    log(f"\nPANEL {panel}: {px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"eval from {start.date()} ({len(eval_idx)} days)")
    sc, ss, sd = fmet(spy)
    log(f"  SPY full {sc:.2%} / {ss:.3f} / {sd:.2%}")

    books = {}
    for form, g in product(FORMS, GROSSES):
        w = form_weights(px, form, g)
        for c in COSTS:
            books[(f"{form} g{g:.2f}", c)] = fast_backtest(
                px, w, c, FREQ)["returns"].loc[start:].values
    for nm, w in (("RULES v1", rules_v1_weights(px)),
                  ("RULES v2 live", rules_v2_weights(px, band=BAND, gross=0.75))):
        for c in COSTS:
            books[(nm, c)] = fast_backtest(px, w, c, FREQ)["returns"].loc[start:].values
    for c in COSTS:
        books[("SPY", c)] = spy
    log(f"  {len(books)} book-series built ({len(FORMS)}x{len(GROSSES)} forms + v1 + v2 + SPY, "
        f"x {len(COSTS)} cost rungs)")

    cen, slopes = [], []
    for H, s, c in product(HORIZONS, SPACINGS, COSTS):
        ii = np.arange(0, len(eval_idx) - H + 1, s)
        if not len(ii):
            continue
        s_c, s_s, s_h1, s_h2, s_d = window_stats(books[("SPY", c)], ii, H)
        for bk in sorted({k[0] for k in books}):
            if bk == "SPY":
                continue
            b_c, b_s, b_h1, b_h2, b_d = window_stats(books[(bk, c)], ii, H)
            L_sh = b_s > s_s
            L_hv = (b_h1 > s_h1) & (b_h2 > s_h2)
            L_dd = b_d >= 0.60 * s_d
            L_cg = b_c >= 0.70 * s_c
            P = L_sh & L_hv & L_dd & L_cg
            for a, i in enumerate(ii):
                cen.append((panel, bk, H, s, c, eval_idx[i], eval_idx[i + H - 1], b_c[a], b_s[a],
                            b_d[a], s_c[a], s_s[a], s_d[a], bool(L_sh[a]), bool(L_hv[a]),
                            bool(L_dd[a]), bool(L_cg[a]), bool(P[a])))
            ok = np.isfinite(b_c) & np.isfinite(s_c)
            if ok.sum() >= 10:
                bslope, binter = np.polyfit(s_c[ok], b_c[ok], 1)
                rho = float(np.corrcoef(s_c[ok], b_c[ok])[0, 1])
            else:
                bslope = binter = rho = np.nan
            slopes.append(dict(panel=panel, book=bk, H=H, s=s, cost=c, n=int(len(ii)),
                               slope=bslope, intercept=binter, rho=rho,
                               cagr_sd=float(np.nanstd(b_c)), spy_cagr_sd=float(np.nanstd(s_c)),
                               cagr_med=float(np.nanmedian(b_c)),
                               spy_cagr_med=float(np.nanmedian(s_c)),
                               pass_4b=float(P.mean()), leg_sharpe=float(L_sh.mean()),
                               leg_halves=float(L_hv.mean()), leg_dd=float(L_dd.mean()),
                               leg_cagr=float(L_cg.mean())))

    # ---- the FIXED-window protocol legs (PROTOCOL 3/4): full, halves, OOS, both KEEP paths
    n = len(eval_idx)
    h = n // 2
    oos = int(eval_idx.searchsorted(OOS_START, side="left"))
    fixed = []
    for c in COSTS:
        spy_r = books[("SPY", c)]
        fc, fs, fd = fmet(spy_r)
        sh1, sh2 = fsharpe(spy_r[:h]), fsharpe(spy_r[h:])
        oc_s, os_s, od_s = fmet(spy_r[oos:])
        b2 = books[("RULES v2 live", c)]
        b2m = fmet(b2)
        b2h = (fsharpe(b2[:h]), fsharpe(b2[h:]))
        for bk in sorted({k[0] for k in books}):
            r = books[(bk, c)]
            cg, sh, dd = fmet(r)
            H1, H2 = fsharpe(r[:h]), fsharpe(r[h:])
            oc, os_, od = fmet(r[oos:])
            t4b = dict(H1=H1 > sh1, H2=H2 > sh2, OOS=os_ > os_s,
                       DD=abs(dd) <= 0.60 * abs(fd), CAGR=cg >= 0.70 * fc)
            fixed.append(dict(panel=panel, book=bk, cost=c, CAGR=cg, Sharpe=sh, MaxDD=dd,
                              H1=H1, H2=H2, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                              v2_Sharpe=b2m[1], v2_MaxDD=b2m[2],
                              SPY_CAGR=fc, SPY_Sharpe=fs, SPY_MaxDD=fd, SPY_OOS_Sharpe=os_s,
                              p4a=bool(H1 > b2h[0] and H2 > b2h[1] and dd >= b2m[2]),
                              p4b=all(t4b.values()),
                              fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))
    cen = pd.DataFrame(cen, columns=["panel", "book", "H", "s", "cost", "entry", "end", "CAGR",
                                     "Sharpe", "MaxDD", "spy_CAGR", "spy_Sharpe", "spy_MaxDD",
                                     "L_sharpe", "L_halves", "L_dd", "L_cagr", "PASS"])
    return cen, pd.DataFrame(slopes), pd.DataFrame(fixed)


def main():
    hdr(f"Idea 828 is-there-a-BOOK-FORM-whose-ENTRY-DATE-pass-share-clears-0.80 | {SCRIPT}")
    log(f"Tuned (2): FORM in {FORMS}; GROSS in {GROSSES}.")
    log(f"Reported never tuned: horizon {HORIZONS}d, entry spacing {SPACINGS}d, cost {COSTS} bps, "
        f"band {BAND}, panel.  Headline cell declared before the run: U56, H={H_HEAD}, "
        f"s={S_HEAD}, {COST_HEAD:g} bps.")
    log("Window-local 4b (idea 829's convention): Sharpe > SPY's AND both halves > SPY's halves "
        "AND MaxDD >= 0.60*SPY's AND CAGR >= 0.70*SPY's, all inside the entry window.")
    log(f"Pre-registered: H_828 some cell >= {BAR:.2f}; H_SLOPE Spearman(slope, pass) >= +0.50; "
        f"H_COST Spearman(slope, leg_dd) <= 0; H_JOINT no cell clears leg_cagr and leg_dd both "
        f">= {BAR:.2f}; H_R8 the IS-chosen cell is within 0.15 of the OOS-best.")

    hdr("[0] REPRODUCTION GATES (printed before any new number is read)")
    px0 = load_universe()
    st0 = px0.index[260]

    g1 = 0.0
    for wfn in (lambda p: form_weights(p, "EWALL-RS", 0.75),
                lambda p: rules_v2_weights(p, band=BAND, gross=1.00),
                rules_v1_weights):
        W = wfn(px0)
        for c in (0.0, 10.0, 25.0):
            a = backtest(px0, W, cost_bps=c, freq=FREQ)
            b = fast_backtest(px0, W, c, FREQ)
            g1 = max(g1, float((a["returns"] - b["returns"]).abs().max()),
                     float((a["turnover"] - b["turnover"]).abs().max()))
    log(f"  G1 fast_backtest == engine.backtest (returns AND turnover), 3 books x 3 rungs: "
        f"max |diff| = {g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    bt = fast_backtest(px0, form_weights(px0, "EWALL-RS", 0.75), 0.0, FREQ)
    r0 = bt["returns"].loc[st0:].values
    t0 = bt["turnover"].loc[st0:].values
    rng = np.random.default_rng(828)
    g2 = 0.0
    for _ in range(200):
        c = float(rng.uniform(0, 100))
        a, b = sorted(rng.choice(len(r0), 2, replace=False))
        if b - a < 300:
            a, b = 0, len(r0)
        ser = pd.Series((r0 - t0 * c / 1e4)[a:b], index=px0.loc[st0:].index[a:b])
        mm, f = metrics(ser), fmet(ser.values)
        g2 = max(g2, abs(mm["CAGR"] - f[0]), abs(mm["Sharpe"] - f[1]), abs(mm["MaxDD"] - f[2]))
    log(f"  G2 fast metrics vs engine.metrics on 200 real series: max |diff| = {g2:.3e} "
        f"(bar 1e-12) -> {'PASS' if g2 < 1e-12 else 'FAIL'}")

    cand = fast_backtest(px0, rules_v2_weights(px0, band=BAND, gross=1.00), 10.0,
                         FREQ)["returns"].loc[st0:]
    fc, fs, fd = fmet(cand.values)
    oo = cand.loc[OOS_START:].values
    oc, os_, od = fmet(oo)
    spy0 = px0["SPY"].pct_change().fillna(0.0).loc[st0:]
    sc, ss, sd = fmet(spy0.values)
    ok4 = (abs(fc - 0.1152) <= 0.010 and abs(fs - 1.1996) <= 0.060 and abs(fd + 0.1591) <= 0.020
           and abs(oc - 0.1266) <= 0.010 and abs(os_ - 1.2740) <= 0.060
           and abs(sc - 0.1516) <= 0.010 and abs(ss - 0.8860) <= 0.060)
    log(f"  G4 committed candidate memo (2026-09-11_u56-band003-gross100_4b_B_MEMO.md): full "
        f"{fc:.2%} / {fs:.4f} / {fd:.2%} (pub 11.52% / 1.1996 / -15.91%); OOS {oc:.2%} / "
        f"{os_:.4f} / {od:.2%} (pub 12.66% / 1.2740 / -15.91%); SPY {sc:.2%} / {ss:.4f} / "
        f"{sd:.2%} (pub 15.16% / 0.8860 / -33.72%) -> {'PASS' if ok4 else 'FAIL'}  "
        f"[tolerance 1.00pp CAGR / 0.060 Sharpe / 2.00pp MaxDD, declared: prices.csv re-caches "
        f"daily]")

    r85 = fast_backtest(px0, form_weights(px0, "EWALL-RS", 0.85), 10.0, FREQ)["returns"].loc[st0:]
    c85, s85, d85 = fmet(r85.values)
    ok85 = abs(c85 - 0.118) < 6e-3 and abs(s85 - 1.05) < 6e-3 and abs(d85 + 0.179) < 6e-3
    log(f"  G5 idea 84 EWALL U56 g=0.85 @10bps: {c85:.2%} / {s85:.3f} / {d85:.2%} "
        f"(committed 11.8% / 1.05 / -17.9%) -> {'PASS' if ok85 else 'CHECK'}")

    panels = [("U56", px0), ("B136", load_universe(broad=True))]
    ps, ndrop = small_panel()
    SMALL = f"SMALL{ps.shape[1]-1}"
    panels.append((SMALL, ps))
    log(f"  G6 PANEL VINTAGE STAMP: today's small cache = {ps.shape[1]} columns; dropping "
        f"{ndrop} names with max_1d_move >= 1.0 leaves {ps.shape[1]-1} + SPY -> {SMALL}. "
        f"SURVIVORSHIP: current constituents only, on all three panels.")

    CEN, SLO, FIX = [], [], []
    for name, px in panels:
        cen, slo, fix = run_panel(name, px, name == "U56")
        CEN.append(cen); SLO.append(slo); FIX.append(fix)
    cen = pd.concat(CEN, ignore_index=True)
    slo = pd.concat(SLO, ignore_index=True)
    fix = pd.concat(FIX, ignore_index=True)

    # ---- G3: idea 829's committed entry-date headline
    g3row = slo[(slo.panel == "U56") & (slo.book == "MA-DG g1.00") & (slo.H == 756)
                & (slo.s == 21) & (slo.cost == 10.0)]
    if len(g3row):
        got = float(g3row["pass_4b"].iloc[0])
        ok3 = abs(got - 0.3977) <= 0.02
        log(f"\n  G3 idea 829's committed entry-date headline (CAND g=1.00 = MA-DG g1.00, U56, "
            f"H=756, s=21, 10 bps): this run {got:.4f} vs committed 0.3977, |diff| "
            f"{abs(got-0.3977):.4f} (bar 0.02) -> {'PASS' if ok3 else 'FAIL'}")
    else:
        got, ok3 = np.nan, False
        log("\n  G3 CANNOT RUN — the MA-DG g1.00 headline cell is missing")

    # ============================================================ [1] the headline sweep
    hdr(f"[1] THE SWEEP - joint window-local 4b pass share by FORM x GROSS, U56, H={H_HEAD}d, "
        f"s={S_HEAD}d, {COST_HEAD:g} bps (the headline cell, declared before the run)")
    head = slo[(slo.panel == "U56") & (slo.H == H_HEAD) & (slo.s == S_HEAD)
               & (slo.cost == COST_HEAD)].copy()
    head["form"] = head["book"].str.rsplit(" g", n=1).str[0]
    head["gross"] = head["book"].str.rsplit(" g", n=1).str[-1]
    tab = head[head.book.str.contains(" g")].pivot(index="form", columns="gross",
                                                   values="pass_4b")
    log(f"  joint 4b pass share ({int(head['n'].iloc[0])} entry windows per cell):")
    log("  " + tab.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    log("\n  every cell, with its four legs and its CAGR co-movement slope:")
    cols = ["book", "n", "pass_4b", "leg_sharpe", "leg_halves", "leg_dd", "leg_cagr", "slope",
            "intercept", "rho", "cagr_med", "spy_cagr_med", "cagr_sd", "spy_cagr_sd"]
    log("  " + head.sort_values("pass_4b", ascending=False)[cols]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))

    grid_cells = head[head.book.str.contains(" g")]
    best = grid_cells.loc[grid_cells["pass_4b"].idxmax()]
    n_clear = int((grid_cells["pass_4b"] >= BAR).sum())
    log(f"\n  H_828: {n_clear} of {len(grid_cells)} (form, gross) cells clear {BAR:.2f}.  "
        f"Best = {best['book']} at {best['pass_4b']:.4f}.  -> "
        f"{'PASS' if n_clear >= 1 else 'FAIL'}")

    rho_sp = spearman(grid_cells["slope"], grid_cells["pass_4b"])
    rho_dd = spearman(grid_cells["slope"], grid_cells["leg_dd"])
    rho_cg = spearman(grid_cells["slope"], grid_cells["leg_cagr"])
    log(f"  H_SLOPE: Spearman(CAGR slope on SPY, pass_4b) = {rho_sp:+.4f} (bar >= +0.50) -> "
        f"{'PASS' if rho_sp >= 0.50 else 'FAIL'};  for reference Spearman(slope, leg_cagr) = "
        f"{rho_cg:+.4f}")
    log(f"  H_COST : Spearman(slope, leg_dd) = {rho_dd:+.4f} (bar <= 0) -> "
        f"{'PASS' if rho_dd <= 0 else 'FAIL'}")
    both = grid_cells[(grid_cells["leg_cagr"] >= BAR) & (grid_cells["leg_dd"] >= BAR)]
    log(f"  H_JOINT: {len(both)} cells clear BOTH leg_cagr >= {BAR:.2f} and leg_dd >= {BAR:.2f} "
        f"-> {'PASS (no free lunch)' if len(both) == 0 else 'FAIL — a free-lunch cell exists'}")
    if len(both):
        log("  " + both[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}")
            .replace("\n", "\n  "))
    log(f"  Cells with slope >= {SLOPE_BAR:.2f} (the level 4b's ratio floor actually needs): "
        f"{int((grid_cells['slope'] >= SLOPE_BAR).sum())} of {len(grid_cells)}; their mean "
        f"leg_cagr {grid_cells.loc[grid_cells['slope']>=SLOPE_BAR,'leg_cagr'].mean():.4f} and "
        f"mean leg_dd {grid_cells.loc[grid_cells['slope']>=SLOPE_BAR,'leg_dd'].mean():.4f}, "
        f"against {grid_cells.loc[grid_cells['slope']<SLOPE_BAR,'leg_cagr'].mean():.4f} / "
        f"{grid_cells.loc[grid_cells['slope']<SLOPE_BAR,'leg_dd'].mean():.4f} below it.")

    # ============================================================ [2] every other grid point
    hdr("[2] EVERY REPORTED GRID POINT - horizon x spacing x cost x panel, no cell dropped")
    for p, _ in panels:
        sub = slo[(slo.panel == p) & (slo.book.str.contains(" g"))]
        pv = sub.pivot_table(index="book", columns=["H", "s", "cost"], values="pass_4b")
        log(f"\n  {p}: joint 4b pass share")
        log("  " + pv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    log("\n  comparands at every grid point (RULES v1, RULES v2 live):")
    pv = (slo[~slo.book.str.contains(" g")]
          .pivot_table(index=["panel", "book"], columns=["H", "s", "cost"], values="pass_4b"))
    log("  " + pv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))

    # ============================================================ [3] rule 8
    hdr("[3] PROTOCOL RULE 8 - choose on IS ENTRY DATES ONLY, read the OOS entry dates untouched")
    c = cen[(cen.panel == "U56") & (cen.H == H_HEAD) & (cen.s == S_HEAD)
            & (cen.cost == COST_HEAD) & (cen.book.str.contains(" g"))].copy()
    c["half"] = np.where(c["entry"] <= IS_END, "IS", "OOS")
    r8 = c.groupby(["book", "half"])["PASS"].agg(["mean", "size"]).unstack()
    r8.columns = [f"{a}_{b}" for a, b in r8.columns]
    r8 = r8.sort_values("mean_IS", ascending=False)
    log("  " + r8.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    is_pick = r8["mean_IS"].idxmax()
    oos_best = r8["mean_OOS"].idxmax()
    gap = float(r8.loc[oos_best, "mean_OOS"] - r8.loc[is_pick, "mean_OOS"])
    log(f"\n  IS pick = {is_pick} (IS {r8.loc[is_pick,'mean_IS']:.4f}) reads "
        f"{r8.loc[is_pick,'mean_OOS']:.4f} on OOS entry dates; OOS-best = {oos_best} at "
        f"{r8.loc[oos_best,'mean_OOS']:.4f}; gap {gap:.4f}")
    log(f"  H_R8 (gap <= 0.15): {'PASS' if gap <= 0.15 else 'FAIL'}")
    log(f"  IS->OOS drift on the IS pick: {r8.loc[is_pick,'mean_OOS'] - r8.loc[is_pick,'mean_IS']:+.4f}")

    # ============================================================ [4] fixed window / both paths
    hdr("[4] PROTOCOL 3 & 4 ON THE FIXED WINDOW - CAGR/Sharpe/MaxDD, halves, OOS, both KEEP "
        "paths, for every cell, never selected on")
    fh = fix[(fix.panel == "U56") & (fix.cost == COST_HEAD)].copy()
    show = ["book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "p4a", "p4b", "fail4b"]
    log("  U56 @ 10 bps (baseline RULES v2 live and SPY are rows in the same table):")
    log("  " + fh.sort_values("Sharpe", ascending=False)[show]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    kp = fix.groupby(["panel", "cost"])[["p4a", "p4b"]].sum()
    kp = kp.join(fix.groupby(["panel", "cost"]).size().rename("n"))
    log("\n  both KEEP paths, all panels and rungs:")
    log("  " + kp.to_string().replace("\n", "\n  "))

    # ---- the entry-date pass share of every FIXED-window 4b passer
    pas = fix[(fix.cost == COST_HEAD) & fix.p4b & fix.book.str.contains(" g")]
    j = pas.merge(slo[(slo.H == H_HEAD) & (slo.s == S_HEAD) & (slo.cost == COST_HEAD)],
                  on=["panel", "book"], how="left")
    log(f"\n  THE GAP THE QUEUE IS ABOUT - every FIXED-window 4b pass, beside its ENTRY-DATE pass "
        f"share at H={H_HEAD}:")
    log("  " + j[["panel", "book", "CAGR", "Sharpe", "MaxDD", "pass_4b", "leg_cagr", "leg_dd",
                  "slope"]].sort_values("pass_4b", ascending=False)
        .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))

    # ============================================================ [5] verdict
    hdr("[5] VERDICT")
    log(f"  H_828  {n_clear} of {len(grid_cells)} cells clear {BAR:.2f} at the headline cell; "
        f"best {best['book']} {best['pass_4b']:.4f} -> {'PASS' if n_clear else 'FAIL'}")
    log(f"  H_SLOPE Spearman(slope, pass_4b) {rho_sp:+.4f} -> "
        f"{'PASS' if rho_sp >= 0.50 else 'FAIL'}")
    log(f"  H_COST  Spearman(slope, leg_dd) {rho_dd:+.4f} -> {'PASS' if rho_dd <= 0 else 'FAIL'}")
    log(f"  H_JOINT {len(both)} free-lunch cells -> "
        f"{'PASS' if len(both) == 0 else 'FAIL'}")
    log(f"  H_R8    gap {gap:.4f} -> {'PASS' if gap <= 0.15 else 'FAIL'}")
    log(f"  G3 (idea 829's 0.3977 reproduced): {'PASS' if ok3 else 'FAIL'} at {got:.4f}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    cen.to_csv(OUT / f"{STEM}.census.csv.gz", index=False, compression="gzip")
    slo.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    head.to_csv(OUT / f"{STEM}.slope.csv", index=False)
    fix.to_csv(OUT / f"{STEM}.fixed.csv", index=False)
    r8.to_csv(OUT / f"{STEM}.walkforward.csv")
    print(f"\nwrote {STEM}.console.txt/.census.csv.gz/.grid.csv/.slope.csv/.fixed.csv/"
          f".walkforward.csv")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""IDEA 916 (lane cloud, 2026-09-22) — RE-READ THE RECORD'S 'NOT A BETA CAP' VERDICTS AT THE
POST-2020 EXCISED OPTIMUM b* ~ 0.61.  WHICH FLIP?

THE QUESTION.  Idea 867 refuted "the 4b DD cap is a beta cap" and the record has carried that
verdict since.  Idea 912 then found that the agreement-maximising beta cap on B136 moves from
**0.4366 to 0.6104** once 2020 is excised — i.e. PROTOCOL 4b's declared 0.60 coincides with the
FITTED optimum only WITHOUT the crash, and at that cap the ex-ante FULL beta agrees with the DD
leg on 0.9732 of 112 books.  If that is right, then "not a beta cap" was read at the WRONG cap:
it is a statement about 2020, not about beta.  This run re-reads it at the excised optimum on
three panels and reports which verdicts flip — and, because a census is not capital, prices the
cap as an ADMISSION RULE under rule 8 on both KEEP paths.

TUNED DIALS — EXACTLY TWO, as PROTOCOL rule 4 allows:
  CAP SOURCE (3): DECLARED = PROTOCOL 4b's 0.60; FIT_FULL = the agreement-argmax fitted WITH
                  2020 in; FIT_EXC = the agreement-argmax fitted with 2020 EXCISED.
  PANEL (3): U56 / B136 / SMALL.
REPORTED, NOT TUNED: the 48-book shelf per panel (BAND 4x4, TOPN 4x4, VOLTGT 4x4 — the record's
own families and ladders), the cost rungs 0/10/25/50 bps (headline 10), execution at t+1,
warm-up 260 rows, the cap search grid 0.05..1.50 step 0.01, the IS/OOS split (rule 8: fitted on
<= 2016-12-31, 2017-01-01 onward read exactly once).  ALL grid points are written to
<slug>.books.csv and <slug>.capgrid.csv; nothing below is reported selectively.

EXCISION CONVENTION, stated once.  "EXCISED" = the 2020 CALENDAR YEAR's daily rows are dropped
from the book's and SPY's return series and the remainder compounded through the gap.  This is
the same operation idea 912 used (it is what moves SPY's worst decline off the 24-day 2020
episode and onto the 196-day 2022 one) and it is applied IDENTICALLY to the book, to SPY and to
the 4b DD cap derived from SPY, so no leg is advantaged.  It breaks the equity path at the gap;
that is a property of the question, not a bug.

NOTE THE RULE-8 ASYMMETRY, which is a finding and not a nuisance: the IS window 2009-2016
CONTAINS NO 2020, so a cap fitted under rule 8 is ALREADY a crash-free cap.  If FIT_EXC is the
right cap, then rule 8 has been quietly fitting it all along while the record's FULL-sample
statements used the other one.

SURVIVORSHIP.  U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is the worst of the three
(names sub-$2B today that have priced since 2010 — every delisting and wipeout is absent) and the
54 tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before anything is priced.
Beta and the agreement RATE are contrasts and are less exposed than a level, but a shelf of
survivors has systematically shallower drawdowns than an honest one, which pushes the fitted cap
DOWN, not up — so the direction this run tests is, if anything, understated here.

PROTOCOL: rule 2 (10 bps, t+1), rule 3 (vs RULES v2 and SPY), rule 4 (both KEEP paths, 2 tuned
params), rule 5, rule 7, rule 8, rule 9.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-22_beta-equivalence-at-the-excised-optimum_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask            # noqa: E402

DATE, SLUG = "2026-09-22", "beta-equivalence-at-the-excised-optimum"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
EXC_LO, EXC_HI = "2020-01-01", "2020-12-31"
COSTS = [0, 10, 25, 50]
COST0 = 10
DD_CAP, CAGR_FLOOR = 0.60, 0.70
DECLARED_BETA = 0.60                                   # PROTOCOL 4b's own number
CAPGRID = np.round(np.arange(0.05, 1.501, 0.01), 4)

CAP_SOURCES = ["DECLARED", "FIT_FULL", "FIT_EXC"]      # TUNED DIAL 1
PANEL_NAMES = ["U56", "B136", "SMALL"]                 # TUNED DIAL 2

BANDS = [0.00, 0.03, 0.06, 0.10]
GROSSES = [0.25, 0.50, 0.75, 1.00]
TOPNS = [5, 10, 20, 40]
TARGETS = [0.08, 0.12, 0.16, 0.20]
SIG_L = 20

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


# ----------------------------------------------------------------------------- fast engine
def bt_fast(R, W, mask):
    """Numpy transcription of products/backtester/engine.backtest at cost_bps=0 (gated by G1)."""
    T, N = R.shape
    cur = np.zeros(N)
    held = np.empty((T, N))
    turn = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = W[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        g = cur * (1.0 + R[i])
        tot = g.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = g / tot
    return (held * R).sum(axis=1), turn


def run_weights(px, W, freq):
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    Wv = np.nan_to_num(W.reindex(px.index).fillna(0.0).values, nan=0.0)
    Wv = np.vstack([np.zeros((1, Wv.shape[1])), Wv[:-1]])
    m = np.asarray(rebalance_mask(px.index, freq).values, bool)
    m = np.concatenate([[False], m[:-1]])
    r, t = bt_fast(R, Wv, m)
    return pd.Series(r, index=px.index), pd.Series(t, index=px.index)


# ----------------------------------------------------------------------------- the shelf
def eq_over(mask_df, gross):
    e = mask_df.astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return gross * e.div(n, axis=0).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    return pr.rolling(L).std() * np.sqrt(252.0)


def shelf(px, cols):
    """48 books per panel: the record's three families on a 4x4 ladder each."""
    sub = px[cols]
    priced = sub.notna()
    out = []
    for b in BANDS:
        st = band_state(sub, b) & priced
        for g in GROSSES:
            out.append(("BAND", f"band{b:.2f}_g{g:.2f}", eq_over(st, g), "W"))
    mom = sub.shift(21) / sub.shift(252) - 1.0
    rank = mom.rank(axis=1, ascending=False)
    for n in TOPNS:
        sel = (rank <= n) & priced
        for g in GROSSES:
            out.append(("TOPN", f"top{n}_g{g:.2f}", eq_over(sel, g), "M"))
    st3 = band_state(sub, 0.03) & priced
    sig = panel_sigma(px, cols)
    for t in TARGETS:
        scale = (t / sig.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
        for g in GROSSES:
            out.append(("VOLTGT", f"volt{t:.2f}_g{g:.2f}", eq_over(st3, g).mul(scale, axis=0), "M"))
    return out


# ----------------------------------------------------------------------------- statistics
def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def excise(r):
    """Drop the 2020 calendar year's rows and compound through the gap."""
    return r.loc[(r.index < EXC_LO) | (r.index > EXC_HI)]


def mets(r):
    r = r.dropna()
    if len(r) < 60:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1), MaxDD=float((eq / eq.cummax() - 1).min()),
                Sharpe=float((r.mean() * 252.0) / vol) if vol else np.nan)


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def beta_of(r, spy):
    """OLS slope of the book on SPY over the rows both share."""
    a, b = r.align(spy, join="inner")
    v = float(np.var(b.values, ddof=1))
    if v == 0:
        return np.nan
    return float(np.cov(a.values, b.values, ddof=1)[0, 1] / v)


def mcc(pred, truth):
    """Matthews correlation of a binary predicate against the binary leg."""
    pred = np.asarray(pred, bool); truth = np.asarray(truth, bool)
    tp = int((pred & truth).sum()); tn = int((~pred & ~truth).sum())
    fp = int((pred & ~truth).sum()); fn = int((~pred & truth).sum())
    den = np.sqrt(float(tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return float((tp * tn - fp * fn) / den) if den > 0 else np.nan


def fit_cap(betas, legs):
    """The cap b* maximising agreement between (beta <= b*) and the DD leg, AND THE PLATEAU IT
    SITS ON.  The argmax is reported at the SMALLEST maximising cap (so the fit can never be
    flattered by drifting upward into a vacuous cap), but the maximising set is an INTERVAL of
    width `plateau`, and any b* quoted to 4dp inside that interval is the same measurement.
    Returns (b*, best agreement, plateau lo, plateau hi, plateau width, 0.60 inside?)."""
    betas = np.asarray(betas, float); legs = np.asarray(legs, bool)
    ok = np.isfinite(betas)
    ag = np.array([float(((betas[ok] <= c) == legs[ok]).mean()) for c in CAPGRID])
    best = float(ag.max())
    plat = CAPGRID[ag >= best - 1e-12]
    lo, hi = float(plat.min()), float(plat.max())
    return (lo, best, lo, hi, float(hi - lo),
            bool(lo - 1e-9 <= DECLARED_BETA <= hi + 1e-9))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    log(f"  SMALL: dropped {len(px.columns) - len(keep)} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv); {len(keep) - 1} names + SPY benchmark remain")
    return px[keep].dropna(how="all").ffill()


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 916 (lane cloud, {DATE}) — re-read the record's 'NOT A BETA CAP' verdicts at "
        f"the POST-2020 EXCISED OPTIMUM.  Which flip?")
    log(f"# TUNED DIALS (2): CAP SOURCE {CAP_SOURCES}; PANEL {PANEL_NAMES}.")
    log(f"# REPORTED, NOT TUNED: 48-book shelf/panel (BAND {BANDS} x gross {GROSSES} W; TOPN "
        f"{TOPNS} x gross M; VOLTGT {TARGETS} x gross M), costs {COSTS} bps (headline {COST0}), "
        f"cap grid {CAPGRID[0]}..{CAPGRID[-1]} step 0.01, warm-up {WARMUP}, IS <= {IS_END}, "
        f"OOS >= {OOS_START} read ONCE, excision = the {EXC_LO[:4]} calendar year.")

    panels = {"U56": load_universe().dropna(how="all").ffill(),
              "B136": load_universe(broad=True).dropna(how="all").ffill(),
              "SMALL": small_panel()}

    p0 = panels["U56"]
    w0 = rules_v2_weights(p0, 0.03, 0.75)
    ref = engine_backtest(p0, w0, cost_bps=0.0, freq="W")
    r1, t1 = run_weights(p0, w0, "W")
    dr = float(np.nanmax(np.abs(ref["returns"].values - r1.values)))
    gate("G1_ENGINE_IDENTITY", f"max|dret| {dr:.3e}", "< 1e-12", dr < 1e-12)

    books, caps, capital = [], [], []
    for pname in PANEL_NAMES:
        px = panels[pname]
        cols = [c for c in px.columns if c != "SPY"]
        st = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        spy_e = excise(spy)
        S = dict(full=mets(spy), exc=mets(spy_e), oos=mets(spy.loc[OOS_START:]),
                 oos_exc=mets(excise(spy.loc[OOS_START:])), is_=mets(spy.loc[:IS_END]))
        S["h1"], S["h2"] = halves(spy)
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lr0, lt0 = run_weights(px, lw, "W")
        lr0, lt0 = lr0.loc[st:], lt0.loc[st:]
        LV = {}
        for c in COSTS:
            r = net(lr0, lt0, c)
            h1, h2 = halves(r)
            LV[c] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]), h1=h1, h2=h2)

        log(f"\n## PANEL {pname}  ({len(cols)} names, scored from {st.date()})")
        log(f"   SPY  FULL(with 2020) {S['full']['CAGR']:7.2%} / {S['full']['Sharpe']:.3f} / "
            f"MaxDD {S['full']['MaxDD']:7.2%}  -> 4b DD cap {DD_CAP * S['full']['MaxDD']:7.2%}")
        log(f"   SPY  FULL(2020 EXCISED) {S['exc']['CAGR']:7.2%} / {S['exc']['Sharpe']:.3f} / "
            f"MaxDD {S['exc']['MaxDD']:7.2%}  -> 4b DD cap {DD_CAP * S['exc']['MaxDD']:7.2%}")
        log(f"   SPY  OOS {S['oos']['CAGR']:7.2%} / {S['oos']['Sharpe']:.3f} / "
            f"{S['oos']['MaxDD']:7.2%};  OOS EXCISED MaxDD {S['oos_exc']['MaxDD']:7.2%}")
        log(f"   RULES v2 @{COST0}bps FULL {LV[COST0]['full']['CAGR']:7.2%} / "
            f"{LV[COST0]['full']['Sharpe']:.3f} / {LV[COST0]['full']['MaxDD']:7.2%}   OOS "
            f"{LV[COST0]['oos']['CAGR']:7.2%} / {LV[COST0]['oos']['Sharpe']:.3f} / "
            f"{LV[COST0]['oos']['MaxDD']:7.2%}")

        for fam, cell, W, freq in shelf(px, cols):
            Wf = W.reindex(columns=px.columns).fillna(0.0)
            r0, t0 = run_weights(px, Wf, freq)
            r0, t0 = r0.loc[st:], t0.loc[st:]
            for c in COSTS:
                r = net(r0, t0, c)
                re_ = excise(r)
                ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
                mf, mx, mo, mi = mets(r), mets(re_), mets(ro), mets(ri)
                h1, h2 = halves(r)
                books.append(dict(
                    panel=pname, family=fam, cell=cell, freq=freq, cost=c,
                    turn_py=float(t0.sum() / (len(r0) / 252.0)),
                    beta_full=beta_of(r, spy), beta_exc=beta_of(re_, spy_e),
                    beta_is=beta_of(ri, spy.loc[:IS_END]),
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                    exc_MaxDD=mx["MaxDD"], exc_Sharpe=mx["Sharpe"],
                    is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"], is_CAGR=mi["CAGR"],
                    oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                    # the 4b DD leg, read on each window against ITS OWN SPY cap
                    leg_full=bool(mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]),
                    leg_exc=bool(mx["MaxDD"] >= DD_CAP * S["exc"]["MaxDD"]),
                    keep4b_full=bool(h1 > S["h1"] and h2 > S["h2"]
                                     and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                                     and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"]),
                    keep4b_oos=bool(mo["Sharpe"] > S["oos"]["Sharpe"]
                                    and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                    and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"]),
                    keep4a_full=bool(h1 > LV[c]["h1"] and h2 > LV[c]["h2"]
                                     and mf["MaxDD"] >= LV[c]["full"]["MaxDD"]),
                    keep4a_oos=bool(mo["Sharpe"] > LV[c]["oos"]["Sharpe"]
                                    and mo["MaxDD"] >= LV[c]["oos"]["MaxDD"])))
        bdf = pd.DataFrame(books)
        sub = bdf[(bdf.panel == pname) & (bdf.cost == COST0)]

        # ---- (A) the fitted cap, WITH and WITHOUT 2020 --------------------------------------
        b_full, a_full, pl_f, ph_f, pw_f, in60_f = fit_cap(sub.beta_full.values,
                                                           sub.leg_full.values)
        b_exc, a_exc, pl_e, ph_e, pw_e, in60_e = fit_cap(sub.beta_exc.values, sub.leg_exc.values)
        b_is, a_is, pl_i, ph_i, pw_i, in60_i = fit_cap(
            sub.beta_is.values, (sub.is_MaxDD.values >= DD_CAP * S["is_"]["MaxDD"]))
        caps.append(dict(panel=pname, b_fit_full=b_full, agree_fit_full=a_full,
                         b_fit_exc=b_exc, agree_fit_exc=a_exc,
                         b_fit_is=b_is, agree_fit_is=a_is,
                         plat_full_lo=pl_f, plat_full_hi=ph_f, plat_full_w=pw_f,
                         declared_in_plat_full=in60_f,
                         plat_exc_lo=pl_e, plat_exc_hi=ph_e, plat_exc_w=pw_e,
                         declared_in_plat_exc=in60_e,
                         plat_is_lo=pl_i, plat_is_hi=ph_i, plat_is_w=pw_i,
                         declared_in_plat_is=in60_i,
                         agree_declared_full=float(((sub.beta_full <= DECLARED_BETA)
                                                    == sub.leg_full).mean()),
                         agree_declared_exc=float(((sub.beta_exc <= DECLARED_BETA)
                                                   == sub.leg_exc).mean()),
                         mcc_declared_full=mcc(sub.beta_full <= DECLARED_BETA, sub.leg_full),
                         mcc_declared_exc=mcc(sub.beta_exc <= DECLARED_BETA, sub.leg_exc),
                         mcc_fit_exc=mcc(sub.beta_exc <= b_exc, sub.leg_exc),
                         n_books=len(sub)))
        log(f"   BETA/DD AGREEMENT over {len(sub)} books at {COST0} bps:")
        log(f"     WITH 2020   : argmax cap b* = {b_full:.4f}, agreement {a_full:.4f};  at "
            f"PROTOCOL's declared 0.60 agreement {caps[-1]['agree_declared_full']:.4f} "
            f"(MCC {caps[-1]['mcc_declared_full']:+.4f})")
        log(f"     2020 EXCISED: argmax cap b* = {b_exc:.4f}, agreement {a_exc:.4f};  at "
            f"PROTOCOL's declared 0.60 agreement {caps[-1]['agree_declared_exc']:.4f} "
            f"(MCC {caps[-1]['mcc_declared_exc']:+.4f})")
        log(f"     IS 2009-2016 (crash-free by construction): b* = {b_is:.4f}, agreement "
            f"{a_is:.4f}")
        log(f"     PLATEAU (the maximising cap is an INTERVAL, not a point): WITH 2020 "
            f"[{pl_f:.2f}, {ph_f:.2f}] width {pw_f:.2f} (0.60 inside: {in60_f}); EXCISED "
            f"[{pl_e:.2f}, {ph_e:.2f}] width {pw_e:.2f} (0.60 inside: {in60_e}); IS "
            f"[{pl_i:.2f}, {ph_i:.2f}] width {pw_i:.2f} (0.60 inside: {in60_i})")

        # ---- (B) the cap as an ADMISSION RULE, rule 8 ---------------------------------------
        for src in CAP_SOURCES:
            cap = {"DECLARED": DECLARED_BETA, "FIT_FULL": b_full, "FIT_EXC": b_exc}[src]
            for c in COSTS:
                sc = bdf[(bdf.panel == pname) & (bdf.cost == c)].sort_values("cell")
                adm = sc[sc.beta_is <= cap]                      # IS-only admission (legal)
                if len(adm) == 0:
                    capital.append(dict(panel=pname, cap_source=src, cap=cap, cost=c,
                                        cell="NONE ADMITTED", n_admitted=0))
                    continue
                row = adm.iloc[int(np.argmax(adm.is_Sharpe.values))]   # legal IS-only chooser
                capital.append(dict(
                    panel=pname, cap_source=src, cap=float(cap), cost=c, n_admitted=len(adm),
                    family=row.family, cell=row.cell, beta_is=row.beta_is,
                    beta_full=row.beta_full, beta_exc=row.beta_exc,
                    CAGR=row.CAGR, Sharpe=row.Sharpe, MaxDD=row.MaxDD, H1=row.H1, H2=row.H2,
                    oos_CAGR=row.oos_CAGR, oos_Sharpe=row.oos_Sharpe, oos_MaxDD=row.oos_MaxDD,
                    keep4b=bool(row.keep4b_full and row.keep4b_oos),
                    keep4b_full=bool(row.keep4b_full), keep4b_oos=bool(row.keep4b_oos),
                    keep4a=bool(row.keep4a_full and row.keep4a_oos),
                    spy_oos_S=S["oos"]["Sharpe"], spy_oos_CAGR=S["oos"]["CAGR"],
                    spy_oos_DD=S["oos"]["MaxDD"], v2_oos_S=LV[c]["oos"]["Sharpe"],
                    v2_oos_CAGR=LV[c]["oos"]["CAGR"], v2_oos_DD=LV[c]["oos"]["MaxDD"]))

    bdf = pd.DataFrame(books); cdf = pd.DataFrame(caps); kdf = pd.DataFrame(capital)
    bdf.to_csv(OUT.with_suffix(".books.csv"), index=False)
    cdf.to_csv(OUT.with_suffix(".caps.csv"), index=False)
    kdf.to_csv(OUT.with_suffix(".capgrid.csv"), index=False)
    log(f"\n# ALL GRID POINTS WRITTEN: {len(bdf)} book-cost rows, {len(kdf)} admission rows.")

    # ------------------------------------------------------------------ (1) does b* move UP?
    log(f"\n## (1) DOES THE FITTED CAP MOVE UP WHEN 2020 IS EXCISED?  (idea 912's B136 reading "
        f"was 0.4366 -> 0.6104)")
    log(cdf[["panel", "n_books", "b_fit_full", "agree_fit_full", "plat_full_lo", "plat_full_hi",
             "b_fit_exc", "agree_fit_exc", "plat_exc_lo", "plat_exc_hi",
             "b_fit_is", "agree_fit_is"]].to_string(index=False,
                                                    float_format=lambda x: f"{x:.4f}"))
    log(f"   READ THE PLATEAU BEFORE THE MOVE: the maximising cap is an INTERVAL on every panel "
        f"and window.  Widths WITH 2020 {[f'{w:.2f}' for w in cdf.plat_full_w]}, EXCISED "
        f"{[f'{w:.2f}' for w in cdf.plat_exc_w]}.  PROTOCOL's declared 0.60 lies INSIDE the "
        f"maximising interval on {int(cdf.declared_in_plat_full.sum())} of 3 panels WITH 2020 "
        f"and {int(cdf.declared_in_plat_exc.sum())} of 3 EXCISED.")
    overlap = [max(0.0, min(a, b) - max(c, d)) for a, b, c, d in
               zip(cdf.plat_full_hi, cdf.plat_exc_hi, cdf.plat_full_lo, cdf.plat_exc_lo)]
    log(f"   OVERLAP of the two maximising intervals (with-2020 vs excised): "
        f"{[f'{o:.2f}' for o in overlap]} — where this is positive, a quoted MOVE of b* is "
        f"inside the resolution of the fit and is NOT a measurement.")
    gate("G2b_MOVE_EXCEEDS_RESOLUTION",
         f"panels where the with-2020 and excised maximising intervals are DISJOINT: "
         f"{int(sum(1 for o in overlap if o <= 0))} of 3",
         ">= 2 of 3 => the b* move is resolvable at all",
         int(sum(1 for o in overlap if o <= 0)) >= 2)
    n_up = int((cdf.b_fit_exc > cdf.b_fit_full).sum())
    gate("G2_CAP_MOVES_UP", f"{n_up} of {len(cdf)} panels have b*(excised) > b*(with 2020); "
                            f"moves {[f'{a:.4f}->{b:.4f}' for a, b in zip(cdf.b_fit_full, cdf.b_fit_exc)]}",
         ">= 2 of 3 (reproduce idea 912's direction)", n_up >= 2)

    near = np.abs(cdf.b_fit_exc.values - DECLARED_BETA) <= 0.10
    gate("G3_EXCISED_OPT_IS_060", f"|b*(excised) - 0.60| = "
                                  f"{[f'{abs(b - DECLARED_BETA):.4f}' for b in cdf.b_fit_exc]}",
         "<= 0.10 on >= 2 of 3 panels", int(near.sum()) >= 2)

    # ------------------------------------------------------------------ (2) which verdicts flip
    log(f"\n## (2) THE FLIP CENSUS — 'beta <= cap' vs the 4b DD leg, book by book")
    log(cdf[["panel", "agree_declared_full", "agree_declared_exc", "agree_fit_exc",
             "mcc_declared_full", "mcc_declared_exc", "mcc_fit_exc"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    flips = []
    for pname in PANEL_NAMES:
        sub = bdf[(bdf.panel == pname) & (bdf.cost == COST0)]
        cap_exc = float(cdf.loc[cdf.panel == pname, "b_fit_exc"].iloc[0])
        v_old = (sub.beta_full <= DECLARED_BETA) == sub.leg_full     # the record's reading
        v_new = (sub.beta_exc <= cap_exc) == sub.leg_exc             # at the excised optimum
        n_fix = int((~v_old & v_new).sum()); n_break = int((v_old & ~v_new).sum())
        flips.append(dict(panel=pname, n=len(sub), disagreed_before=int((~v_old).sum()),
                          disagreed_after=int((~v_new).sum()), fixed=n_fix, broken=n_break))
        log(f"   {pname:5s}: the predicate DISAGREED with the DD leg on {int((~v_old).sum()):2d} "
            f"of {len(sub)} books under the record's reading, and on {int((~v_new).sum()):2d} of "
            f"{len(sub)} at the excised optimum  ->  {n_fix} verdicts FLIP to agreement, "
            f"{n_break} flip the other way")
    fdf = pd.DataFrame(flips)
    best_exc = cdf.agree_fit_exc.values
    gate("G4_FLIP", f"agreement at the excised optimum {[f'{a:.4f}' for a in best_exc]} vs at "
                    f"the record's reading {[f'{a:.4f}' for a in cdf.agree_declared_full]}",
         ">= 0.90 on >= 2 of 3 panels => 'not a beta cap' FLIPS",
         int((best_exc >= 0.90).sum()) >= 2)

    # ------------------------------------------------------------------ (3) capital, rule 8
    log(f"\n## (3) THE CAP AS AN ADMISSION RULE UNDER RULE 8 (IS beta <= cap, then max IS "
        f"Sharpe; OOS read ONCE) at {COST0} bps")
    kh = kdf[kdf.cost == COST0]
    log(kh[["panel", "cap_source", "cap", "n_admitted", "cell", "beta_is", "CAGR", "Sharpe",
            "MaxDD", "H1", "H2", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "keep4a", "keep4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    moved = 0
    for pname in PANEL_NAMES:
        cells = kh[kh.panel == pname].set_index("cap_source").cell.to_dict()
        if len(set(cells.values())) > 1:
            moved += 1
        log(f"   {pname:5s} picks: " + ", ".join(f"{k}={v}" for k, v in cells.items()))
    gate("G5_CAP_SOURCE_MOVES_CAPITAL", f"{moved} of 3 panels where the three cap sources do "
                                        f"NOT all pick the same book",
         ">= 1 => the cap source is a real free parameter", moved >= 1)
    n4a, n4b = int(kh.keep4a.sum()), int(kh.keep4b.sum())
    gate("G6_ANY_KEEP", f"4a {n4a}, 4b FULL+OOS {n4b} of {len(kh)} admission-rule books",
         ">= 1 clears a KEEP path", (n4a + n4b) >= 1)

    log(f"\n## COST LADDER (all rungs, nothing selected)")
    for c in COSTS:
        kc = kdf[kdf.cost == c]
        log(f"   {c:3d} bps: 4a {int(kc.keep4a.sum())}, 4b FULL+OOS {int(kc.keep4b.sum())} of "
            f"{len(kc)};  distinct picks per panel "
            f"{[len(set(kc[kc.panel == p].cell)) for p in PANEL_NAMES]}")

    fdf.to_csv(OUT.with_suffix(".flips.csv"), index=False)
    pd.DataFrame(_gates).to_csv(OUT.with_suffix(".gates.csv"), index=False)
    OUT.with_suffix(".log.txt").write_text("\n".join(_log) + "\n")
    log(f"\n# wrote {OUT.name}.{{books,caps,capgrid,flips,gates}}.csv and .log.txt")


if __name__ == "__main__":
    main()

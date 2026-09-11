#!/usr/bin/env python3
"""Idea 508 — price the 4a MaxDD leg against a VOL-MATCHED cap.

Idea 500's census found that over 244 arm-rows both PROTOCOL-4a Sharpe legs clear the
live RULES v2 book 15 times (6.1%) and the MaxDD leg then cuts 13 of those 15 (86.7%):
4a is a drawdown test wearing a Sharpe test's name.  The queue's complaint is that the
cap is the live book's OWN realised drawdown, and the live book runs at gross 0.75
behind a 200d band, so its drawdown is largely an EXPOSURE fact rather than a skill
fact.  This run re-prices every 4a decision in that corpus with the MaxDD leg restated
as a MATCHED cap and counts how many verdicts flip.

Two tuned parameters, exactly as the queue allows:
    1. MATCHING STATISTIC  s(.)   — 5 grid points, ALL reported
    2. PANEL                      — U56, B136, SMALL439, ALL reported
The cost rung (10 / 25 bps) is a second READING of the same books via the exact cost
decomposition r(c) = r(0) - turnover * c/1e4 (gated below), not a third parameter.

Pre-registered definitions, fixed before any number was read:
  arm corpus   the idea-500 grid, rebuilt: 6 dials (n, band, gross, volcap, quantile,
               cadence) x published + extension values x 3 panels x 2 rungs.
  4a(s)        H1 Sharpe > base H1 AND H2 Sharpe > base H2 AND arm.MaxDD >= CAP(s),
               with CAP(s) = base.MaxDD * (s(arm) / s(base)) over the SAME window the
               MaxDD leg is read on.  s = NONE reproduces PROTOCOL 4a verbatim
               (CAP = base.MaxDD).
  4b(s)        PROTOCOL 4b with its own MaxDD leg matched the same way:
               arm.MaxDD >= 0.6 * SPY.MaxDD * (s(arm)/s(SPY)); Sharpe/OOS-Sharpe/CAGR
               legs untouched.
  FLIP         pass4a(s) != pass4a(NONE) for the same arm-row.
  statistics   NONE     CAP = base.MaxDD                        (the incumbent)
               VOL      annualised stdev of daily returns
               SEMIVOL  annualised stdev of the negative daily returns (downside)
               SQRTVOL  sqrt of the VOL ratio                    (half-matching)
               GROSS    mean daily gross exposure sum|w|         (pure exposure fact)
  Rule 8       PROTOCOL 8: the statistic and the arm are chosen on 2009-2016 ONLY
               (4a(s) evaluated inside the IS window, argmax IS Sharpe among its
               passers), 2017-2026 read once against RULES v2, RULES v1, SPY and the
               EWALL do-nothing control.

Costs 10 bps headline and a 25 bps rung; weekly cadence except on the cadence dial;
weights decided at t applied at t+1 (engine).  No network — panels come from the
committed caches via research/baseline.load_universe.
SURVIVORSHIP: U56 = research/universe.json, B136 = universe_broad.json (current
constituents), SMALL439 = the sub-$2B screen with the 44 tickers whose max_1d_move
>= 1.0 dropped first (idea 500's panel, reproduced).
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = "2026-09-11_price-the-4a-MaxDD-leg-against-a-VOL-MATCHED-cap_B"
OUT = ROOT / "research" / "backtests"
GROSS, BAND = 0.75, 0.03
COSTS = [10, 25]
OOS_START = "2017-01-01"
STATS = ["NONE", "VOL", "SEMIVOL", "SQRTVOL", "GROSS"]

_console: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ---------------------------------------------------------------- fast engine (gated)
def fast_run(prices, weights, freq):
    """Vectorised equivalent of engine.backtest: returns (gross daily returns, turnover,
    daily gross exposure sum|w| actually held).  Gated against engine.backtest below."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    gr = pd.Series((held * rets).sum(axis=1), index=idx)
    return gr, pd.Series(turn, index=idx), pd.Series(np.abs(held).sum(axis=1), index=idx)

def costed(gross_ret, turnover, bps):
    return gross_ret - turnover * bps / 1e4

# ---------------------------------------------------------------- book forms (idea 500, verbatim)
def _ew(px, mask, gross):
    e = mask.astype(float).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def w_topn(px, n, gross=GROSS):
    s, above, _ = score(px)
    r = s.where(above).rank(axis=1, ascending=False)
    return _ew(px, r <= n, gross)

def w_band(px, band, gross=GROSS):   return rules_v2_weights(px, band=band, gross=gross)
def w_gross(px, gross, band=BAND):   return rules_v2_weights(px, band=band, gross=gross)

def w_volcap(px, cap, gross=GROSS):
    _, above, vol20 = score(px)
    return _ew(px, above & (vol20 < cap), gross)

def w_quantile(px, x, gross=GROSS):
    s, above, _ = score(px)
    r = s.where(above).rank(axis=1, ascending=False, pct=True)
    return _ew(px, r <= x, gross)

def w_ewall(px, gross=GROSS):        return _ew(px, px.notna(), gross)

DIALS = {
    "n":        dict(fn=w_topn,     pub=[5, 10, 20, 30, 50],                  ext=[3, 75, 100, 150],  freq="W"),
    "band":     dict(fn=w_band,     pub=[0.00, 0.01, 0.03, 0.05, 0.08, 0.12], ext=[0.16, 0.20, 0.25, 0.35], freq="W"),
    "gross":    dict(fn=w_gross,    pub=[0.25, 0.50, 0.75, 1.00],             ext=[0.10],             freq="W"),
    "volcap":   dict(fn=w_volcap,   pub=[0.30, 0.45, 0.60, 0.90, 9.99],       ext=[0.20, 0.25],       freq="W"),
    "quantile": dict(fn=w_quantile, pub=[0.10, 0.25, 0.50, 0.75, 1.00],       ext=[0.02, 0.05],       freq="W"),
    "cadence":  dict(fn=None,       pub=["D", "W", "M", "Q"],                 ext=[],                 freq=None),
}

def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]

# ---------------------------------------------------------------- metric helpers
def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]

def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())

def ann_vol(r):     return float(r.std() * np.sqrt(252))
def semi_vol(r):
    d = r[r < 0]
    return float(d.std() * np.sqrt(252)) if len(d) > 1 else np.nan

def trio(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]

def split_r8(r):
    m = r.index < pd.Timestamp(OOS_START)
    return r[m], r[~m]

def window_stats(r, gexp):
    """Every number a leg reads on one window: Sharpe/CAGR/MaxDD + the 3 statistics."""
    c, s, d = trio(r)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, VOL=ann_vol(r), SEMIVOL=semi_vol(r),
                GROSS=float(gexp.reindex(r.index).mean()))

def cap_of(stat, base, arm):
    """CAP(s) = base.MaxDD * ratio(s).  base.MaxDD is negative; a higher-vol arm gets a
    proportionally deeper allowance, a lower-vol arm a tighter one."""
    if stat == "NONE":    return base["MaxDD"]
    if stat == "SQRTVOL": ratio = np.sqrt(arm["VOL"] / base["VOL"])
    else:                 ratio = arm[stat] / base[stat]
    return base["MaxDD"] * ratio

# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say(f"# {STAMP}\n")
    say("Question: PROTOCOL 4a's MaxDD leg caps an arm at the LIVE book's own realised")
    say("drawdown, which is an exposure fact.  Restate the cap as MATCHED on a")
    say("statistic s and count how many 4a verdicts flip.  Params: s x panel (all")
    say("reported); rungs 10/25 bps are a second reading of the same books.\n")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    # ---------------- gates, before any new number is read
    say("## Gates")
    pxu = panels["U56"]; start_u = pxu.index[260]
    wv2 = rules_v2_weights(pxu)
    g, tv, ge = fast_run(pxu, wv2, "W")
    eng = backtest(pxu, wv2, cost_bps=10.0, freq="W")
    def _maxabs(a, b):
        d = np.abs(np.asarray(a, float) - np.asarray(b, float))
        ok = np.isfinite(d)
        return float(d[ok].max()), int((~ok).sum())
    g1, g1n = _maxabs(costed(g, tv, 10).values, eng["returns"].values)
    g1t, _ = _maxabs(tv.values, eng["turnover"].values)
    say(f"G1 fast_run vs engine.backtest @10bps (U56, RULES v2): max|dr| {g1:.3e}  "
        f"max|dturnover| {g1t:.3e}  non-finite rows {g1n}")
    assert g1 < 1e-12 and g1t < 1e-12, "fast_run does not reproduce the engine"

    pxs = panels["SMALL439"]
    gs, ts, ges = fast_run(pxs, w_band(pxs, 0.05), "W")
    engs = backtest(pxs, w_band(pxs, 0.05), cost_bps=25.0, freq="W")
    g2, g2n = _maxabs(costed(gs, ts, 25).values, engs["returns"].values)
    say(f"G2 cost-rung identity r(25) = r(0) - turnover*25/1e4 (SMALL439, band 0.05): "
        f"max|dr| {g2:.3e}  non-finite rows {g2n}")
    assert g2 < 1e-12

    lv = costed(g, tv, 10).loc[start_u:]
    h1, h2 = halves(lv)
    say(f"G3 RULES v2 on U56 @10bps: CAGR {trio(lv)[0]:.2%} Sharpe {trio(lv)[1]:.4f} "
        f"MaxDD {trio(lv)[2]:.2%} halves {trio(h1)[1]:.4f}/{trio(h2)[1]:.4f}"
        "   (idea 500 published 8.66% / 1.2056 / -12.05% / 1.2259 / 1.1908)")
    ss = costed(gs, ts, 10).loc[pxs.index[260]:]
    sh1, sh2 = halves(ss)
    say(f"G4 idea 270R SMALL439 band=0.05 @10bps: CAGR {trio(ss)[0]:.2%} Sharpe {trio(ss)[1]:.4f} "
        f"MaxDD {trio(ss)[2]:.2%} halves {trio(sh1)[1]:.4f}/{trio(sh2)[1]:.4f}"
        "   (published 4.18% / 0.6183 / -14.6% / 0.6385 / 0.6031)")
    b_none = dict(MaxDD=-0.12, VOL=1.0, SEMIVOL=1.0, GROSS=1.0)
    a_any = dict(MaxDD=-0.30, VOL=2.0, SEMIVOL=2.0, GROSS=2.0)
    say(f"G5 CAP identity: NONE cap {cap_of('NONE', b_none, a_any):.4f} == base.MaxDD; "
        f"VOL cap at a 2x-vol arm {cap_of('VOL', b_none, a_any):.4f} (= 2 x base.MaxDD)")
    assert abs(cap_of("NONE", b_none, a_any) - b_none["MaxDD"]) < 1e-15
    assert abs(cap_of("VOL", b_none, a_any) - 2 * b_none["MaxDD"]) < 1e-15
    say("")

    # ---------------- the corpus
    rows = []
    for pname, px in panels.items():
        start = px.index[260]
        nnames = px.shape[1] - 1
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy_g = pd.Series(1.0, index=px.index)      # SPY buy-and-hold is 100% gross
        say(f"## Panel {pname}: {nnames} names + SPY, {px.index[0].date()}..{px.index[-1].date()}")

        books = {}
        for dname, D in DIALS.items():
            for v in list(D["pub"]) + list(D["ext"]):
                if dname == "n" and v > nnames:
                    continue
                if dname == "cadence":
                    w, freq = rules_v2_weights(px, band=BAND, gross=GROSS), v
                else:
                    w, freq = D["fn"](px, v), D["freq"]
                gr, tu, ge = fast_run(px, w, freq)
                books[(dname, v)] = (gr.loc[start:], tu.loc[start:], ge.loc[start:],
                                     int(v in D["pub"]))
        for nm, wfn, fq in [("RULES v2 (live)", rules_v2_weights(px), "W"),
                            ("RULES v1", rules_v1_weights(px), "W"),
                            ("EWALL control", w_ewall(px), "W")]:
            gr, tu, ge = fast_run(px, wfn, fq)
            books[("_comparand", nm)] = (gr.loc[start:], tu.loc[start:], ge.loc[start:], 0)

        for (dname, v), (gr, tu, ge, pub) in books.items():
            for cost in COSTS:
                r = costed(gr, tu, cost)
                is_r, oos_r = split_r8(r)
                a, b = halves(r)
                row = dict(panel=pname, dial=dname, arm=v, cost=cost, published=pub,
                           turnover_yr=float(tu.sum() / (len(tu) / 252)))
                for tag, rr in [("FULL", r), ("H1", a), ("H2", b), ("IS", is_r), ("OOS", oos_r)]:
                    for k, val in window_stats(rr, ge).items():
                        row[f"{tag}_{k}"] = val
                # the IS window's own halves — rule 8 reads 4a inside 2009-2016
                ia, ib = halves(is_r)
                row["ISH1_Sharpe"], row["ISH2_Sharpe"] = trio(ia)[1], trio(ib)[1]
                rows.append(row)
        for cost in COSTS:                                    # SPY, cost-free by construction
            is_r, oos_r = split_r8(spy_r); a, b = halves(spy_r)
            row = dict(panel=pname, dial="_comparand", arm="SPY", cost=cost, published=0,
                       turnover_yr=0.0)
            for tag, rr in [("FULL", spy_r), ("H1", a), ("H2", b), ("IS", is_r), ("OOS", oos_r)]:
                for k, val in window_stats(rr, spy_g).items():
                    row[f"{tag}_{k}"] = val
            ia, ib = halves(is_r)
            row["ISH1_Sharpe"], row["ISH2_Sharpe"] = trio(ia)[1], trio(ib)[1]
            rows.append(row)

    A = pd.DataFrame(rows)
    arms = A[A.dial != "_comparand"].copy()
    say(f"\nCorpus: {len(arms)} arm-rows ({arms[arms.published == 1].shape[0]} published, "
        f"{arms[arms.published == 0].shape[0]} extension) + {len(A) - len(arms)} comparand rows.")

    # ---------------- re-price both KEEP paths under every statistic
    def cmp_of(panel, cost, who):
        m = A[(A.panel == panel) & (A.dial == "_comparand") & (A.arm == who) & (A.cost == cost)]
        return m.iloc[0]

    out = []
    for _, a in arms.iterrows():
        b = cmp_of(a.panel, a.cost, "RULES v2 (live)"); s = cmp_of(a.panel, a.cost, "SPY")
        base_full = dict(MaxDD=b.FULL_MaxDD, VOL=b.FULL_VOL, SEMIVOL=b.FULL_SEMIVOL, GROSS=b.FULL_GROSS)
        arm_full = dict(MaxDD=a.FULL_MaxDD, VOL=a.FULL_VOL, SEMIVOL=a.FULL_SEMIVOL, GROSS=a.FULL_GROSS)
        spy_full = dict(MaxDD=s.FULL_MaxDD, VOL=s.FULL_VOL, SEMIVOL=s.FULL_SEMIVOL, GROSS=s.FULL_GROSS)
        sharpe4a = bool(a.H1_Sharpe > b.H1_Sharpe and a.H2_Sharpe > b.H2_Sharpe)
        sharpe4b = bool(a.H1_Sharpe > s.H1_Sharpe and a.H2_Sharpe > s.H2_Sharpe
                        and a.OOS_Sharpe > s.OOS_Sharpe)
        cagr4b = bool(a.FULL_CAGR >= 0.7 * s.FULL_CAGR)
        rec = dict(a)
        rec.update(sharpe4a=int(sharpe4a), sharpe4b=int(sharpe4b), cagr4b=int(cagr4b),
                   base_MaxDD=b.FULL_MaxDD, base_VOL=b.FULL_VOL, base_H1=b.H1_Sharpe,
                   base_H2=b.H2_Sharpe, spy_MaxDD=s.FULL_MaxDD, spy_VOL=s.FULL_VOL)
        for st in STATS:
            cap = cap_of(st, base_full, arm_full)
            rec[f"cap4a_{st}"] = cap
            rec[f"dd4a_{st}"] = int(a.FULL_MaxDD >= cap)
            rec[f"pass4a_{st}"] = int(sharpe4a and a.FULL_MaxDD >= cap)
            cap_b = 0.6 * spy_full["MaxDD"] if st == "NONE" else \
                0.6 * cap_of(st, dict(spy_full), arm_full)
            rec[f"cap4b_{st}"] = cap_b
            rec[f"pass4b_{st}"] = int(sharpe4b and cagr4b and a.FULL_MaxDD >= cap_b)
        out.append(rec)
    G = pd.DataFrame(out)
    G.to_csv(OUT / f"{STAMP}.arms.csv", index=False)

    # ---------------- headline: idea 500's numbers, then the flips
    say("\n## 1. Reproduction of idea 500's leg count, then the re-pricing")
    n_rows = len(G); n_sh = int(G.sharpe4a.sum())
    n_cut = int(((G.sharpe4a == 1) & (G.pass4a_NONE == 0)).sum())
    say(f"arm-rows {n_rows}; both 4a Sharpe legs clear the live book {n_sh} times "
        f"({n_sh/n_rows:.1%}); the MaxDD leg then cuts {n_cut} of those {n_sh} "
        f"({(n_cut/n_sh if n_sh else float('nan')):.1%})"
        "   (idea 500 published 244 / 15 / 6.1% / 13 / 86.7%)")

    lines = []
    for st in STATS:
        p = int(G[f"pass4a_{st}"].sum())
        up = int(((G[f"pass4a_{st}"] == 1) & (G.pass4a_NONE == 0)).sum())
        dn = int(((G[f"pass4a_{st}"] == 0) & (G.pass4a_NONE == 1)).sum())
        ddrate = (G.loc[G.sharpe4a == 1, f"dd4a_{st}"].mean() if n_sh else np.nan)
        b4 = int(G[f"pass4b_{st}"].sum())
        b_up = int(((G[f"pass4b_{st}"] == 1) & (G.pass4b_NONE == 0)).sum())
        b_dn = int(((G[f"pass4b_{st}"] == 0) & (G.pass4b_NONE == 1)).sum())
        lines.append(dict(stat=st, pass4a=p, flip_up=up, flip_dn=dn,
                          dd_leg_survival_among_sharpe_clears=ddrate,
                          pass4b=b4, b_flip_up=b_up, b_flip_dn=b_dn))
    F = pd.DataFrame(lines).set_index("stat")
    F.to_csv(OUT / f"{STAMP}.flips.csv")
    say("\n### 4a and 4b pass counts and FLIPS, whole corpus (n=%d arm-rows)" % n_rows)
    say(F.to_string(float_format=lambda x: f"{x:.3f}"))

    # per panel x statistic
    pp = []
    for pn, sub in G.groupby("panel"):
        for st in STATS:
            pp.append(dict(panel=pn, stat=st, n=len(sub), sharpe4a=int(sub.sharpe4a.sum()),
                           pass4a=int(sub[f"pass4a_{st}"].sum()),
                           flip_up=int(((sub[f"pass4a_{st}"] == 1) & (sub.pass4a_NONE == 0)).sum()),
                           flip_dn=int(((sub[f"pass4a_{st}"] == 0) & (sub.pass4a_NONE == 1)).sum()),
                           pass4b=int(sub[f"pass4b_{st}"].sum())))
    P = pd.DataFrame(pp)
    P.to_csv(OUT / f"{STAMP}.bypanel.csv", index=False)
    say("\n### by PANEL x STATISTIC")
    say(P.to_string(index=False))

    # per dial x statistic (4a only)
    dd = []
    for dn_, sub in G.groupby("dial"):
        row = dict(dial=dn_, n=len(sub), sharpe4a=int(sub.sharpe4a.sum()))
        for st in STATS:
            row[f"4a_{st}"] = int(sub[f"pass4a_{st}"].sum())
        dd.append(row)
    Dd = pd.DataFrame(dd)
    Dd.to_csv(OUT / f"{STAMP}.bydial.csv", index=False)
    say("\n### by DIAL x STATISTIC (4a passes)")
    say(Dd.to_string(index=False))

    # ---------------- who flips, named
    say("\n## 2. Every arm-row whose 4a verdict FLIPS under at least one statistic")
    flip_any = G[[c for c in G.columns if c.startswith("pass4a_") and c != "pass4a_NONE"]].apply(
        lambda c: c != G.pass4a_NONE).any(axis=1)
    FL = G[flip_any][["panel", "dial", "arm", "cost", "published", "FULL_CAGR", "FULL_Sharpe",
                      "FULL_MaxDD", "FULL_VOL", "base_MaxDD", "base_VOL", "H1_Sharpe", "H2_Sharpe",
                      "base_H1", "base_H2"] + [f"pass4a_{s}" for s in STATS]].copy()
    FL["DDoverVOL"] = FL.FULL_MaxDD / FL.FULL_VOL
    FL["base_DDoverVOL"] = FL.base_MaxDD / FL.base_VOL
    FL.to_csv(OUT / f"{STAMP}.flippers.csv", index=False)
    if len(FL) == 0:
        say("NONE — no arm-row changes its 4a verdict under any matched cap.")
    else:
        say(f"{len(FL)} arm-rows flip.  MaxDD/VOL is the scale-free reading of the VOL cap "
            f"(pass iff arm DD/VOL >= base DD/VOL).")
        say(FL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- is the DD leg an exposure fact? the corpus regression
    say("\n## 3. How much of the MaxDD leg is an exposure fact")
    reg = []
    for pn, sub in G[G.cost == 10].groupby("panel"):
        x = sub.FULL_VOL.values; y = -sub.FULL_MaxDD.values
        ok = np.isfinite(x) & np.isfinite(y)
        sl, ic = np.polyfit(x[ok], y[ok], 1)
        r2 = np.corrcoef(x[ok], y[ok])[0, 1] ** 2
        xg = sub.FULL_GROSS.values
        r2g = np.corrcoef(xg[ok], y[ok])[0, 1] ** 2
        reg.append(dict(panel=pn, n=int(ok.sum()), slope_DD_on_VOL=sl, intercept=ic,
                        R2_VOL=r2, R2_GROSS=r2g,
                        DDoverVOL_min=float(np.nanmin(y[ok] / x[ok])),
                        DDoverVOL_med=float(np.nanmedian(y[ok] / x[ok])),
                        DDoverVOL_max=float(np.nanmax(y[ok] / x[ok]))))
    R = pd.DataFrame(reg)
    R.to_csv(OUT / f"{STAMP}.exposure.csv", index=False)
    say("|MaxDD| regressed on realised VOL across the corpus, 10 bps rung:")
    say(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- rule 8
    say("\n## 4. PROTOCOL 8 walk-forward — statistic AND arm chosen on 2009-2016 only")
    wf = []
    for pname in panels:
        for cost in COSTS:
            sub = G[(G.panel == pname) & (G.cost == cost)]
            b = cmp_of(pname, cost, "RULES v2 (live)"); s = cmp_of(pname, cost, "SPY")
            v1 = cmp_of(pname, cost, "RULES v1"); ew = cmp_of(pname, cost, "EWALL control")
            base_is = dict(MaxDD=b.IS_MaxDD, VOL=b.IS_VOL, SEMIVOL=b.IS_SEMIVOL, GROSS=b.IS_GROSS)
            for st in STATS:
                elig = []
                for _, a in sub.iterrows():
                    arm_is = dict(MaxDD=a.IS_MaxDD, VOL=a.IS_VOL, SEMIVOL=a.IS_SEMIVOL, GROSS=a.IS_GROSS)
                    if (a.ISH1_Sharpe > b.ISH1_Sharpe and a.ISH2_Sharpe > b.ISH2_Sharpe
                            and a.IS_MaxDD >= cap_of(st, base_is, arm_is)):
                        elig.append(a)
                row = dict(panel=pname, cost=cost, stat=st, n_IS_4a=len(elig))
                if elig:
                    E = pd.DataFrame(elig)
                    k = E.IS_Sharpe.idxmax(); pick = E.loc[k]
                    row.update(pick_dial=pick.dial, pick_arm=pick.arm, IS_Sharpe=pick.IS_Sharpe,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD)
                else:
                    row.update(pick_dial=None, pick_arm=None, IS_Sharpe=np.nan,
                               OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan)
                # unconditional IS-Sharpe chooser (idea 500's reference number)
                kk = sub.IS_Sharpe.idxmax(); free = sub.loc[kk]
                row.update(free_dial=free.dial, free_arm=free.arm,
                           free_OOS_Sharpe=free.OOS_Sharpe, free_OOS_CAGR=free.OOS_CAGR,
                           free_OOS_MaxDD=free.OOS_MaxDD,
                           base_OOS_CAGR=b.OOS_CAGR, base_OOS_Sharpe=b.OOS_Sharpe, base_OOS_MaxDD=b.OOS_MaxDD,
                           spy_OOS_CAGR=s.OOS_CAGR, spy_OOS_Sharpe=s.OOS_Sharpe, spy_OOS_MaxDD=s.OOS_MaxDD,
                           v1_OOS_Sharpe=v1.OOS_Sharpe, ew_OOS_Sharpe=ew.OOS_Sharpe)
                wf.append(row)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    cols = ["panel", "cost", "stat", "n_IS_4a", "pick_dial", "pick_arm", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "base_OOS_Sharpe", "spy_OOS_Sharpe", "base_OOS_CAGR", "spy_OOS_CAGR",
            "base_OOS_MaxDD", "spy_OOS_MaxDD"]
    say(W[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    beat_b = W.dropna(subset=["OOS_Sharpe"])
    say(f"\nrule-8 cells with a pick: {len(beat_b)} of {len(W)}; picks beating RULES v2 OOS Sharpe: "
        f"{int((beat_b.OOS_Sharpe > beat_b.base_OOS_Sharpe).sum())}; beating SPY OOS Sharpe: "
        f"{int((beat_b.OOS_Sharpe > beat_b.spy_OOS_Sharpe).sum())}")
    say(f"unconditional IS-Sharpe chooser (no 4a filter) OOS Sharpe by panel@10bps: " +
        ", ".join(f"{r.panel} {r.free_OOS_Sharpe:.4f} ({r.free_dial}={r.free_arm})"
                  for _, r in W[(W.cost == 10) & (W.stat == "NONE")].iterrows()))

    # ---------------- both KEEP paths, headline verdict
    say("\n## 5. Both KEEP paths at the 10 bps headline rung")
    for st in STATS:
        a4 = G[(G.cost == 10) & (G[f"pass4a_{st}"] == 1)]
        b4 = G[(G.cost == 10) & (G[f"pass4b_{st}"] == 1)]
        both = G[(G.cost == 10) & (G[f"pass4a_{st}"] == 1) & (G[f"pass4b_{st}"] == 1)]
        say(f"  s={st:8s} 4a {len(a4):3d}/{len(G[G.cost==10])}  4b {len(b4):3d}  BOTH {len(both):3d}")

    say(f"\nruntime {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()

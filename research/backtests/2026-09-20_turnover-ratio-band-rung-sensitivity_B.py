#!/usr/bin/env python3
"""Idea 267 (lane B, 2026-09-20) — IS THE 1.2x-1.4x TURNOVER-RATIO BAND THE RUNG-SENSITIVITY
BOUNDARY, OFF THE NULL ARMS?

THE PRE-REGISTERED CLAIM (verbatim from idea 267 / idea 262's null ladder).  For a pair of
books x, y differing on ONE dial, let R = max(T_x, T_y) / min(T_x, T_y) be the ratio of their
annualised turnovers.  Idea 262 measured the Sharpe breakeven cost c* on the record's NULL arms
only and found it sits ABOVE the whole 0-25 bps rung range when R < ~1.2 and INSIDE it when
R > ~1.4.  Idea 267 asks whether the band is a property of TURNOVER or an artefact of NULL arms,
by re-testing it on the record's REAL one-dial arm pairs: cadence, gross, band, count, vol scaler.

TWO TUNED PARAMETERS, BOTH PRE-STATED BEFORE THE RUN (protocol rule 4):
  P1  ordering statistic = SHARPE.  (Idea 262's own law is a Sharpe law:
      c* = dSharpe(0) * 1e4 / (T_x/vol_x - T_y/vol_y).)  CAGR is reported at every point as a
      SECOND AXIS, not as an alternative choice.
  P2  rung range top = 25 bps.  (Idea 267's own words: "above the whole 0-25 bps range".)
The band edges 1.2 / 1.4 are INHERITED from idea 267's text, not fitted here; the full
R -> flip curve is published for every pair so the boundary can be read rather than chosen.

WHAT IS MEASURED.  Costs enter the engine only as `port = gross_ret - turnover * c / 1e4`, so
every arm is backtested ONCE at 0 bps and re-priced EXACTLY at any rung.  Identity is asserted
against the engine at 10 bps (max |d| printed).

  V1  CLASSIFICATION.  For all 38 real one-dial pairs (19 per panel x U56 / B136): R, dSharpe(0),
      dSharpe(25), empirical c* on a 0.5-bps grid, the law's c*, whether the ordering FLIPS inside
      [0, 25].  Band prediction: R < 1.2 -> NO FLIP, R > 1.4 -> FLIP, 1.2-1.4 -> undecided.
      Scored on ALL pairs and on the CONTESTABLE subset (the high-turnover arm leads at 0 bps, so
      a flip is possible at all).
  V2  THE SAME CURVE ON CAGR, and per-dial (cadence / gross / band / count / volscaler).
  V3  CAPITAL ARM + RULE 8.  The band read as a SCREENING RULE over real books: for each
      (panel x dial) ladder, C_BAND keeps the IS-Sharpe winner unless its turnover ratio to the
      ladder's lowest-turnover arm exceeds 1.4, in which case it takes the low-turnover arm.
      Controls: C_ISSHARPE (no screen), C_LOWTURN, C_HIGHTURN.  All choices made on 2009-2016
      ONLY; 2017-2026 read once.  Every picked book scored FULL / halves / OOS at 0/10/25/50 bps
      on BOTH KEEP paths against live RULES v2 and SPY.

SURVIVORSHIP: universe.json and universe_broad.json are CURRENT constituents, so every absolute
level here is optimistic.  The pairwise read (V1/V2) is a within-panel difference and is much
less exposed than the V3 levels.
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, score  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 220)

# ---- pre-registered constants -------------------------------------------------------------
STAT = "Sharpe"          # P1
RUNG_TOP = 25.0          # P2 (bps)
BAND_LO, BAND_HI = 1.2, 1.4          # inherited from idea 267, NOT fitted
COST_RUNGS = [0.0, 10.0, 25.0, 50.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CGRID = np.arange(0.0, 100.0001, 0.5)   # empirical breakeven grid
_CURVE_ERR = []                          # re-pricing identity: |curve(c) - metrics(c)|


# ---- arm catalogue (real one-dial books, no nulls) -----------------------------------------
def w_ew(px, band=0.03, gross=0.75):
    return rules_v2_weights(px, band=band, gross=gross)


def w_topn(px, n=20, gross=0.75, vol_scale=False):
    s, above, vol20 = score(px, vol_scale)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def arm_catalogue():
    """dial -> list of (label, weights_fn, freq). One dial moves inside each list."""
    return {
        "CADENCE":   [(f"EW_b03_g75_{f}", lambda px: w_ew(px), f) for f in ("D", "W", "M", "Q")],
        "GROSS":     [(f"EW_b03_g{int(g*100):02d}_W", (lambda g: lambda px: w_ew(px, gross=g))(g), "W")
                      for g in (0.50, 0.75, 1.00)],
        "BAND":      [(f"EW_b{int(b*100):02d}_g75_W", (lambda b: lambda px: w_ew(px, band=b))(b), "W")
                      for b in (0.00, 0.03, 0.08)],
        "COUNT":     [(f"TOP{n}_g75_W", (lambda n: lambda px: w_topn(px, n=n))(n), "W")
                      for n in (5, 10, 20, 40)],
        "VOLSCALER": [("TOP20_noVS_W", lambda px: w_topn(px, n=20, vol_scale=False), "W"),
                      ("TOP20_VS_W",   lambda px: w_topn(px, n=20, vol_scale=True),  "W")],
    }


# ---- run every arm once at 0 bps, keep (gross returns, turnover) ---------------------------
def run_arms(px, panel):
    """One entry per (panel, dial, label, freq).  An arm shared by two dials (EW_b03_g75_W is
    the CADENCE, GROSS and BAND ladders' common rung) is backtested ONCE and reused, but it
    stays a member of every ladder it belongs to."""
    start = px.index[260]
    cache, out = {}, {}
    for dial, arms in arm_catalogue().items():
        for label, fn, freq in arms:
            ck = (label, freq)
            if ck not in cache:
                res = backtest(px, fn(px), cost_bps=0.0, freq=freq)
                cache[ck] = (res["returns"].loc[start:], res["turnover"].loc[start:])
            r0, to = cache[ck]
            out[(panel, dial, label, freq)] = dict(r0=r0, to=to, dial=dial, label=label,
                                                   freq=freq, panel=panel)
    print(f"[arms] {panel}: {len(out)} ladder slots over {len(cache)} distinct books")
    return out


def at_cost(a, c, lo=None, hi=None):
    return _slice(a["r0"] - a["to"] * c / 1e4, lo, hi)


def stats(a, c, lo=None, hi=None):
    r = at_cost(a, c, lo, hi)
    m = metrics(r)
    yrs = len(r) / 252
    to = _slice(a["to"], lo, hi).sum() / yrs if yrs else np.nan
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"], TO=to)


def _slice(s, lo, hi):
    if lo is not None:
        s = s.loc[lo:]
    if hi is not None:
        s = s.loc[:hi]
    return s


def stat_curve(a, stat, lo, hi, cs):
    """stat(c) for every c in cs, computed exactly but without re-running the engine.
    Sharpe uses moment algebra (identical to engine.metrics); CAGR uses a cumprod per rung."""
    r0 = _slice(a["r0"], lo, hi).values
    to = _slice(a["to"], lo, hi).values
    if stat == "Sharpe":
        n = len(r0)
        m0, mt = r0.mean(), to.mean()
        v0 = r0.var(ddof=1); vt = to.var(ddof=1)
        cv = np.cov(r0, to, ddof=1)[0, 1]
        k = cs / 1e4
        mean = m0 - k * mt
        var = v0 - 2 * k * cv + k ** 2 * vt
        vol = np.sqrt(np.maximum(var, 1e-300)) * np.sqrt(252)
        return mean * 252 / vol
    yrs = len(r0) / 252
    out = np.empty(len(cs))
    for i, c in enumerate(cs):
        eq = np.prod(1.0 + (r0 - to * c / 1e4))
        out[i] = eq ** (1 / yrs) - 1
    return out


# ---- harness identity check ----------------------------------------------------------------
def identity_check(px, panel):
    res0 = backtest(px, w_ew(px), cost_bps=0.0, freq="W")
    res10 = backtest(px, w_ew(px), cost_bps=10.0, freq="W")
    d = (res0["returns"] - res0["turnover"] * 10.0 / 1e4) - res10["returns"]
    print(f"[identity] {panel}: max|re-priced(10bps) - engine(10bps)| = {np.abs(d).max():.3e}")


# ---- V1/V2: pairwise rung sensitivity -------------------------------------------------------
def pair_table(arms, stat, window):
    lo, hi = {"FULL": (None, None), "IS": (None, IS_END), "OOS": (OOS_START, None)}[window]
    rows = []
    by_dial = {}
    for k, a in arms.items():
        by_dial.setdefault((a["panel"], a["dial"]), []).append(k)
    for (panel, dial), keys in by_dial.items():
        for kx, ky in itertools.combinations(sorted(keys), 2):
            ax, ay = arms[kx], arms[ky]
            sx0, sy0 = stats(ax, 0.0, lo, hi), stats(ay, 0.0, lo, hi)
            # orient: x = higher annualised turnover
            if sx0["TO"] < sy0["TO"]:
                ax, ay, sx0, sy0 = ay, ax, sy0, sx0
            R = sx0["TO"] / sy0["TO"] if sy0["TO"] > 0 else np.inf
            d0 = sx0[stat] - sy0[stat]
            sxT, syT = stats(ax, RUNG_TOP, lo, hi), stats(ay, RUNG_TOP, lo, hi)
            dT = sxT[stat] - syT[stat]
            # empirical breakeven on the 0.5 bps grid
            dd = stat_curve(ax, stat, lo, hi, CGRID) - stat_curve(ay, stat, lo, hi, CGRID)
            _CURVE_ERR.append(max(abs(dd[0] - d0), abs(dd[int(RUNG_TOP / 0.5)] - dT)))
            sgn = np.sign(dd)
            idx = np.where(sgn[:-1] * sgn[1:] < 0)[0]
            cstar = float(CGRID[idx[0]] + 0.5 * abs(dd[idx[0]]) / (abs(dd[idx[0]]) + abs(dd[idx[0] + 1]))) \
                if len(idx) else np.inf
            # idea 262's law (Sharpe only)
            law = (d0 * 1e4 / (sx0["TO"] / sx0["Vol"] - sy0["TO"] / sy0["Vol"])) \
                if stat == "Sharpe" and (sx0["TO"] / sx0["Vol"] - sy0["TO"] / sy0["Vol"]) != 0 else np.nan
            flip = bool(np.sign(d0) != np.sign(dT))
            pred = "FLIP" if R > BAND_HI else ("NOFLIP" if R < BAND_LO else "GREY")
            rows.append(dict(panel=panel, dial=dial, window=window, stat=stat,
                             hi_arm=ax["label"] + "|" + ax["freq"], lo_arm=ay["label"] + "|" + ay["freq"],
                             TO_hi=sx0["TO"], TO_lo=sy0["TO"], R=R, d0=d0, d25=dT,
                             cstar=cstar, cstar_law=law, flip=flip, pred=pred,
                             contestable=bool(d0 > 0)))
    return pd.DataFrame(rows)


def score_band(df, label):
    dec = df[df.pred != "GREY"]
    hit = (dec.pred == np.where(dec.flip, "FLIP", "NOFLIP"))
    base = max(dec.flip.mean(), 1 - dec.flip.mean()) if len(dec) else float("nan")
    print(f"  {label}: decisive n={len(dec)}  correct={int(hit.sum())}  "
          f"acc={hit.mean() if len(dec) else float('nan'):.3f}  "
          f"MAJORITY-CLASS base rate={base:.3f}  lift={(hit.mean()-base) if len(dec) else float('nan'):+.3f}"
          f"   (grey n={int((df.pred=='GREY').sum())}, of which flip={int(df[df.pred=='GREY'].flip.sum())})")
    if len(dec):
        ct = pd.crosstab(dec.pred, dec.flip)
        print(ct.to_string().replace("\n", "\n    ").rjust(4))
    return (int(hit.sum()), len(dec))


# ---- V3: capital arm -------------------------------------------------------------------------
def keep_verdicts(bk, base, spy):
    """bk/base/spy: dict with FULL/H1/H2/OOS metric dicts. Returns (4a, 4b, legs)."""
    a = (bk["H1"]["Sharpe"] > base["H1"]["Sharpe"] and bk["H2"]["Sharpe"] > base["H2"]["Sharpe"]
         and bk["FULL"]["MaxDD"] >= base["FULL"]["MaxDD"])
    legs = dict(
        L1_H1=bk["H1"]["Sharpe"] > spy["H1"]["Sharpe"],
        L2_H2=bk["H2"]["Sharpe"] > spy["H2"]["Sharpe"],
        L3_OOS=bk["OOS"]["Sharpe"] > spy["OOS"]["Sharpe"],
        L4_DD=bk["FULL"]["MaxDD"] >= 0.60 * spy["FULL"]["MaxDD"],
        L5_CAGR=bk["FULL"]["CAGR"] >= 0.70 * spy["FULL"]["CAGR"])
    return a, all(legs.values()), legs


def windowed(r):
    h = len(r) // 2
    return {"FULL": metrics(r), "H1": metrics(r.iloc[:h]), "H2": metrics(r.iloc[h:]),
            "OOS": metrics(r.loc[OOS_START:])}


def main():
    panels = {}
    for name, kw in (("U56", {}), ("B136", {"broad": True})):
        px = load_universe(**kw)
        identity_check(px, name)
        panels[name] = px

    arms = {}
    for name, px in panels.items():
        arms.update(run_arms(px, name))
    print(f"\n[arms] {len(arms)} ladder slots in total, each book backtested once at 0 bps.\n")

    # ---------------- V1 / V2 -----------------
    all_pairs = []
    for stat in ("Sharpe", "CAGR"):
        for window in ("FULL", "IS", "OOS"):
            all_pairs.append(pair_table(arms, stat, window))
    P = pd.concat(all_pairs, ignore_index=True)
    print(f"[identity] max|stat_curve(c) - engine metrics(c)| over {len(_CURVE_ERR)} checks = "
          f"{max(_CURVE_ERR):.3e}")
    P.to_csv(Path(__file__).with_suffix(".pairs.csv"), index=False)

    print("=" * 110)
    print("V1 — ALL GRID POINTS: every real one-dial pair, primary statistic SHARPE, FULL sample")
    print("=" * 110)
    show = P[(P.stat == "Sharpe") & (P.window == "FULL")].sort_values("R")
    print(show[["panel", "dial", "hi_arm", "lo_arm", "TO_hi", "TO_lo", "R", "d0", "d25",
                "cstar", "cstar_law", "flip", "pred", "contestable"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    lawok = show[np.isfinite(show.cstar) & np.isfinite(show.cstar_law)]
    if len(lawok):
        err = (lawok.cstar - lawok.cstar_law).abs()
        print(f"\n[262's law check] n={len(lawok)}  median |c*_emp - c*_law| = {err.median():.3f} bps, "
              f"max {err.max():.3f} bps")

    print("\nBAND SCORE (pre-registered: R<1.2 -> NOFLIP, R>1.4 -> FLIP), SHARPE:")
    tot = {}
    for window in ("FULL", "IS", "OOS"):
        d = P[(P.stat == "Sharpe") & (P.window == window)]
        tot[("Sharpe", window, "all")] = score_band(d, f"SHARPE {window} — all pairs")
        tot[("Sharpe", window, "cont")] = score_band(d[d.contestable], f"SHARPE {window} — contestable only")

    print("\nV2 — SECOND AXIS: CAGR")
    for window in ("FULL", "IS", "OOS"):
        d = P[(P.stat == "CAGR") & (P.window == window)]
        tot[("CAGR", window, "all")] = score_band(d, f"CAGR   {window} — all pairs")
        tot[("CAGR", window, "cont")] = score_band(d[d.contestable], f"CAGR   {window} — contestable only")

    print("\nV2b — PER-DIAL (SHARPE, FULL, all pairs): does any single dial carry the band?")
    d = P[(P.stat == "Sharpe") & (P.window == "FULL")]
    for dial in sorted(d.dial.unique()):
        dd = d[(d.dial == dial) & (d.pred != "GREY")]
        hit = (dd.pred == np.where(dd.flip, "FLIP", "NOFLIP"))
        print(f"  {dial:10s} decisive n={len(dd):2d}  correct={int(hit.sum()):2d}  "
              f"R range {d[d.dial==dial].R.min():.2f}-{d[d.dial==dial].R.max():.2f}  "
              f"flip rate {d[d.dial==dial].flip.mean():.3f}")

    print("\nV2c — WHERE IS THE BOUNDARY REALLY? (diagnostic, NOT a tuned parameter)")
    d = P[(P.stat == "Sharpe") & (P.window == "FULL")].sort_values("R")
    print("  R sorted with flip flag:",
          " ".join(f"{r:.2f}{'F' if f else '.'}" for r, f in zip(d.R, d.flip)))
    fl, nf = d[d.flip].R, d[~d.flip].R
    print(f"  flips:    n={len(fl)}  R median {fl.median():.2f}  min {fl.min():.2f}  max {fl.max():.2f}")
    print(f"  no-flips: n={len(nf)}  R median {nf.median():.2f}  min {nf.min():.2f}  max {nf.max():.2f}")
    if len(fl) and len(nf):
        best = max(((t, ((d.R > t) == d.flip).mean()) for t in np.arange(1.0, 4.01, 0.05)),
                   key=lambda z: z[1])
        print(f"  best single threshold on THIS data: R* = {best[0]:.2f} (acc {best[1]:.3f}) "
              f"vs the pre-registered 1.2/1.4 band")

    # ---------------- V3 capital arm -----------------
    print("\n" + "=" * 110)
    print("V3 — CAPITAL ARM: the band as an IS-only SCREENING RULE over real books (rule 8)")
    print("=" * 110)
    base_stats, spy_stats = {}, {}
    for pname, px in panels.items():
        start = px.index[260]
        b = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
        base_stats[pname] = dict(r0=b["returns"].loc[start:], to=b["turnover"].loc[start:])
        spy_stats[pname] = px["SPY"].pct_change().fillna(0).loc[start:]

    cap_rows = []
    for pname in panels:
        spy_w = windowed(spy_stats[pname])
        for dial in arm_catalogue():
            keys = [k for k, a in arms.items() if a["panel"] == pname and a["dial"] == dial]
            if len(keys) < 2:
                continue
            # --- all choices made on 2009-2016 ONLY ---
            is_sh = {k: stats(arms[k], 10.0, None, IS_END)["Sharpe"] for k in keys}
            is_to = {k: stats(arms[k], 10.0, None, IS_END)["TO"] for k in keys}
            k_is = max(keys, key=lambda k: is_sh[k])
            k_lo = min(keys, key=lambda k: is_to[k])
            k_hi = max(keys, key=lambda k: is_to[k])
            R_is = is_to[k_is] / is_to[k_lo] if is_to[k_lo] > 0 else np.inf
            k_band = k_lo if R_is > BAND_HI else k_is
            picks = {"C_ISSHARPE": k_is, "C_BAND": k_band, "C_LOWTURN": k_lo, "C_HIGHTURN": k_hi}
            for cname, k in picks.items():
                for c in COST_RUNGS:
                    bk = windowed(at_cost(arms[k], c))
                    bs = windowed(base_stats[pname]["r0"] - base_stats[pname]["to"] * c / 1e4)
                    a4, b4, legs = keep_verdicts(bk, bs, spy_w)
                    cap_rows.append(dict(panel=pname, dial=dial, chooser=cname, pick=arms[k]["label"],
                                         freq=arms[k]["freq"], cost=c, R_is=R_is,
                                         screened=int(cname == "C_BAND" and k != k_is),
                                         CAGR=bk["FULL"]["CAGR"], Sharpe=bk["FULL"]["Sharpe"],
                                         MaxDD=bk["FULL"]["MaxDD"], H1=bk["H1"]["Sharpe"],
                                         H2=bk["H2"]["Sharpe"], oCAGR=bk["OOS"]["CAGR"],
                                         oSharpe=bk["OOS"]["Sharpe"], oMaxDD=bk["OOS"]["MaxDD"],
                                         KEEP4a=a4, KEEP4b=b4,
                                         fails="|".join(n for n, v in legs.items() if not v)))
    C = pd.DataFrame(cap_rows)
    C.to_csv(Path(__file__).with_suffix(".capital.csv"), index=False)

    print("\nALL CAPITAL GRID POINTS (4 choosers x 5 dials x 2 panels x 4 cost rungs = "
          f"{len(C)} rows):")
    print(C[["panel", "dial", "chooser", "pick", "freq", "cost", "R_is", "screened",
             "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD",
             "KEEP4a", "KEEP4b", "fails"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\nCHOOSER SUMMARY (10 cells = 2 panels x 5 dials):")
    for c in COST_RUNGS:
        s = C[C.cost == c].groupby("chooser").agg(
            n=("KEEP4b", "size"), pass4b=("KEEP4b", "sum"), pass4a=("KEEP4a", "sum"),
            oSharpe=("oSharpe", "mean"), oCAGR=("oCAGR", "mean"), oMaxDD=("oMaxDD", "mean"))
        print(f"\n  cost {c:.0f} bps")
        print(s.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    n_screen = C[(C.chooser == "C_BAND") & (C.cost == 10.0)].screened.sum()
    print(f"\n[screen activity] the 1.4x screen fires on {n_screen} of "
          f"{len(C[(C.chooser=='C_BAND') & (C.cost==10.0)])} (panel x dial) cells.")

    pk = C.pivot_table(index=["panel", "dial"], columns="chooser", values="pick", aggfunc="first")
    print("\nPICKS (IS window only, 2009-2016):")
    print(pk.to_string())
    print(f"\n[screen is not information] C_BAND == C_LOWTURN on "
          f"{int((pk.C_BAND == pk.C_LOWTURN).sum())} of {len(pk)} cells; "
          f"C_BAND == C_ISSHARPE on {int((pk.C_BAND == pk.C_ISSHARPE).sum())}.")

    print("\n4b PASSING CELLS (all cost rungs):")
    pas = C[C.KEEP4b]
    print(pas[["panel", "dial", "chooser", "pick", "cost", "CAGR", "Sharpe", "MaxDD",
               "H1", "H2", "oCAGR", "oSharpe", "oMaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}") if len(pas) else "  none")
    print(f"\n4a: {int(C.KEEP4a.sum())} of {len(C)} rows.  Binding-leg census over the "
          f"{len(C) - int(C.KEEP4b.sum())} 4b failures:")
    print(C[~C.KEEP4b].fails.value_counts().to_string().replace("\n", "\n    "))

    print("\nCOMPARANDS (FULL / halves / OOS at 10 bps):")
    for pname in panels:
        bs = windowed(base_stats[pname]["r0"] - base_stats[pname]["to"] * 10.0 / 1e4)
        sw = windowed(spy_stats[pname])
        print(f"  {pname} RULES v2: FULL {bs['FULL']['CAGR']:.2%} / {bs['FULL']['Sharpe']:.4f} / "
              f"{bs['FULL']['MaxDD']:.2%}  halves {bs['H1']['Sharpe']:.4f}/{bs['H2']['Sharpe']:.4f}  "
              f"OOS {bs['OOS']['CAGR']:.2%} / {bs['OOS']['Sharpe']:.4f} / {bs['OOS']['MaxDD']:.2%}")
        print(f"  {pname} SPY     : FULL {sw['FULL']['CAGR']:.2%} / {sw['FULL']['Sharpe']:.4f} / "
              f"{sw['FULL']['MaxDD']:.2%}  halves {sw['H1']['Sharpe']:.4f}/{sw['H2']['Sharpe']:.4f}  "
              f"OOS {sw['OOS']['CAGR']:.2%} / {sw['OOS']['Sharpe']:.4f} / {sw['OOS']['MaxDD']:.2%}")

    print("\nDONE. pairs -> *.pairs.csv, capital grid -> *.capital.csv")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 355 (cloud, 2026-09-07): why-does-the-grid-ORDERING-invert-on-B136-at-0-bps-only.

QUESTION (queue text): idea 39 found the (n,g) grid's Sharpe ORDERING has rank correlation
+1.000 with the corrected tape in 6/18 cells but -0.538 (CALENDAR) / -0.322 (SANDBOX) on
B136 at 0 bps, recovering to +0.972 / +0.434 at 10 bps.  "An ordering that only inverts
when costs are switched OFF suggests the zero-cost ranking on the broad panel is decided
by something with no economic content.  Decompose the 0-bps B136 ordering into turnover,
breadth and vol terms."

DESIGN
------
Same four index regimes as idea 39 (all reproducible offline from the committed caches):
  CORRECTED : trading days, 2008-01-02 ->     (today's cache; the truth)
  TRUNC     : trading days, 2014-09-17 ->     (start effect only)
  CALENDAR  : calendar days, 2008-01-02 ->    (index effect only)
  SANDBOX   : calendar days, 2014-09-17 ->    (the pre-fix cache)
plus one MECHANISM arm that is not a tape at all:
  SHRUNK    : the CORRECTED tape with every score lookback multiplied by 252/365,
              i.e. the corrected tape scored with the number of TRADING days a
              calendar-day window actually spans.  No tuned parameter: 252/365 is
              the calendar's own duty cycle, not a fitted constant.

TUNED PARAMETERS: 2 (book width n in {3,5,10,20}, gross g in {0.75,0.85,1.00}) -> the same
12-point grid idea 39 ordered.  ALL 12 points reported at every regime x panel x rung.

THE DECOMPOSITION.  For any book b on any tape, with r_b the GROSS portfolio return series
and tau_b the per-row turnover series, the net Sharpe at cost rung c (bps) is EXACTLY

    S_b(c) = ( G_b - (c/1e4) * T_b ) / V_b(c)
    G_b = mean(r_b) * 252            annualised gross return term
    T_b = mean(tau_b) * 252          annualised turnover term
    V_b(c) = std(r_b - tau_b*c/1e4) * sqrt(252)     vol term

because engine.backtest's held weights and turnover do not depend on cost_bps.  That is a
3-term identity (gated below against a direct backtest call), so the ordering of the 12
books is a function of exactly three numbers per book, and each can be SUBSTITUTED from
the corrected tape one at a time to see which term carries the inversion.  At c = 0 the
turnover term drops out of the key algebraically - which is the whole shape of the puzzle.

BREADTH is reported beside them: mean eligible count E_t, and the share of days E_t < n
(the only channel through which breadth can move a top-n book's weights at all).

RULE 8 (walk-forward): (n,g) chosen on IS Sharpe to 2016-12-31, read once on 2017-2026.
Chosen TWICE - on the corrected tape, and on the calendar tape (what an analyst on the
pre-fix cache would have picked) - but SCORED both times on the corrected tape, because
reality is the corrected tape whatever the analyst was looking at.  That prices the
ordering inversion in OOS Sharpe.  Both KEEP paths (4a vs RULES v2, 4b vs SPY) reported.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_why-does-the-grid-ORDERING-invert-on-B136-at-0-bps-only_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)

SANDBOX_START = "2014-09-17"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
RUNGS = [0, 10, 25]
NS, GS = [3, 5, 10, 20], [0.75, 0.85, 1.00]          # the only two tuned axes
GRID = [(n, g) for n in NS for g in GS]
GNAME = lambda n, g: f"TOP{n}_g{g:.2f}"
DUTY = 252.0 / 365.0                                  # trading days per calendar day
OUT = ROOT / "research" / "backtests" / "2026-09-07_why-does-the-grid-ORDERING-invert-on-B136-at-0-bps-only_cloud"


# ------------------------------------------------------------------ tapes
def to_calendar(px):
    idx = pd.date_range(px.index[0], px.index[-1], freq="D")
    return px.reindex(idx).ffill()


def tapes(px):
    return {"CORRECTED": px, "TRUNC": px.loc[SANDBOX_START:],
            "CALENDAR": to_calendar(px), "SANDBOX": to_calendar(px.loc[SANDBOX_START:])}


# ------------------------------------------------------------------ scoring
def score_shrunk(px, k=DUTY):
    """baseline.score with every lookback scaled by k (SHRUNK arm only)."""
    L = lambda w: max(2, int(round(w * k)))
    mom = px.shift(L(21)) / px.shift(L(252)) - 1
    r6 = px / px.shift(L(126)) - 1
    r3 = px / px.shift(L(63)) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(L(200)).mean()
    vol20 = px.pct_change().rolling(L(20)).std() * np.sqrt(252)
    s = comp * (0.5 + 0.5 * above.astype(float)) / vol20.clip(lower=0.08) ** 0.5
    return s, above, vol20


def eligibility(px, shrunk=False):
    s, above, vol20 = (score_shrunk(px) if shrunk else score(px))
    elig = s.where(above & (vol20 < 0.60))
    return elig, (above & (vol20 < 0.60))


def topn_weights(elig, n, g):
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0) * g


# ------------------------------------------------------------------ engine (cost-free once)
def run_book(px, w, start):
    """One backtest at 0 bps; every rung is derived EXACTLY (held weights are cost-free)."""
    res = backtest(px, w, cost_bps=0, freq="W")
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(rg, tau, c):
    return rg - tau * c / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    o = r.loc[OOS_START:]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS=metrics(o)["Sharpe"] if len(o) > 60 else np.nan,
                OOS_CAGR=metrics(o)["CAGR"] if len(o) > 60 else np.nan,
                OOS_MaxDD=metrics(o)["MaxDD"] if len(o) > 60 else np.nan)


# ------------------------------------------------------------------ main sweep
def sweep(px, panel):
    rows, keep = [], {}
    arms = {k: (v, False) for k, v in tapes(px).items()}
    arms["SHRUNK"] = (px, True)                      # corrected tape, compressed windows
    for rname, (rpx, shrunk) in arms.items():
        start = rpx.index[260]
        elig, ok = eligibility(rpx, shrunk)
        spy = rpx["SPY"].pct_change().fillna(0).loc[start:]
        E = ok.sum(axis=1).loc[start:]
        # controls
        ctl = {"RULESv2": rules_v2_weights(rpx), "RULESv1": rules_v1_weights(rpx)}
        books = {GNAME(n, g): topn_weights(elig, n, g) for n, g in GRID}
        books.update(ctl)
        for bname, w in books.items():
            rg, tau = run_book(rpx, w, start)
            yrs = len(rg) / 252
            G = rg.mean() * 252
            T = tau.mean() * 252
            nm = int(bname[3:].split("_")[0]) if bname.startswith("TOP") else np.nan
            for c in RUNGS:
                rn = net(rg, tau, c)
                V = rn.std() * np.sqrt(252)
                d = dict(panel=panel, regime=rname, book=bname, n=nm, bps=c,
                         G=G, T=T, V=V, S_ident=(G - c / 1e4 * T) / V,
                         E_mean=E.mean(), E_binds=float((E < nm).mean()) if nm == nm else np.nan,
                         nrows=len(rg), years=yrs)
                d.update(stats(rn))
                rows.append(d)
            keep[(rname, bname)] = (rg, tau)
        rows.extend([dict(panel=panel, regime=rname, book="SPY", n=np.nan, bps=c,
                          G=spy.mean() * 252, T=0.0, V=spy.std() * np.sqrt(252),
                          S_ident=spy.mean() * 252 / (spy.std() * np.sqrt(252)),
                          E_mean=E.mean(), E_binds=np.nan, nrows=len(spy), years=len(spy) / 252,
                          **stats(spy)) for c in RUNGS])
        print(f"  [{panel}/{rname}] {len(rpx)} rows {rpx.index[0].date()}->{rpx.index[-1].date()} "
              f"eval from {start.date()}  mean eligible {E.mean():.1f}")
    return pd.DataFrame(rows), keep


# ------------------------------------------------------------------ ordering analysis
def spearman(a, b):
    return pd.Series(a).rank().corr(pd.Series(b).rank())


def ordering_table(df, panel):
    g = df[(df.panel == panel) & (df.book.str.startswith("TOP"))]
    corr = g[g.regime == "CORRECTED"].set_index(["book", "bps"])
    out = []
    for rg in ["TRUNC", "CALENDAR", "SANDBOX", "SHRUNK"]:
        alt = g[g.regime == rg].set_index(["book", "bps"])
        for c in RUNGS:
            bk = [GNAME(n, gg) for n, gg in GRID]
            Sc = np.array([corr.loc[(b, c), "Sharpe"] for b in bk])
            Ga = np.array([alt.loc[(b, c), "G"] for b in bk])
            Ta = np.array([alt.loc[(b, c), "T"] for b in bk])
            Va = np.array([alt.loc[(b, c), "V"] for b in bk])
            Gc = np.array([corr.loc[(b, c), "G"] for b in bk])
            Tc = np.array([corr.loc[(b, c), "T"] for b in bk])
            Vc = np.array([corr.loc[(b, c), "V"] for b in bk])
            Sa = (Ga - c / 1e4 * Ta) / Va
            key = lambda G_, T_, V_: (G_ - c / 1e4 * T_) / V_
            # OLS of alt Sharpe on corrected Sharpe (levels, not ranks)
            b1 = np.polyfit(Sc, Sa, 1)
            resid = Sa - np.polyval(b1, Sc)
            out.append(dict(panel=panel, regime=rg, bps=c,
                            rho=spearman(Sc, Sa),
                            rho_sub_G=spearman(Sc, key(Gc, Ta, Va)),
                            rho_sub_T=spearman(Sc, key(Ga, Tc, Va)),
                            rho_sub_V=spearman(Sc, key(Ga, Ta, Vc)),
                            sd_S_corr=Sc.std(ddof=1), sd_S_alt=Sa.std(ddof=1),
                            slope=b1[0], R2=1 - resid.var() / Sa.var(),
                            resid_sd=resid.std(ddof=1),
                            spread_G_corr=Gc.std(ddof=1) / abs(Gc.mean()),
                            spread_V_corr=Vc.std(ddof=1) / abs(Vc.mean()),
                            spread_T_corr=Tc.std(ddof=1) / abs(Tc.mean()),
                            cost_share=abs(c / 1e4 * Tc).std(ddof=1) / max(abs(Gc - c / 1e4 * Tc).std(ddof=1), 1e-12)))
    return pd.DataFrame(out)


# ------------------------------------------------------------------ rule 8
def walkforward(keep, panel, df):
    """Choose (n,g) by IS Sharpe on <=2016 on a CHOOSER tape; score OOS on CORRECTED."""
    rows = []
    bk = [GNAME(n, g) for n, g in GRID]
    for chooser in ["CORRECTED", "CALENDAR", "SANDBOX"]:
        for c in RUNGS:
            IS = {}
            for b in bk:
                rg, tau = keep[(chooser, b)]
                rn = net(rg, tau, c).loc[:IS_END]
                IS[b] = metrics(rn)["Sharpe"] if len(rn) > 60 else np.nan
            pick = max(IS, key=lambda k: IS[k])
            rg, tau = keep[("CORRECTED", pick)]
            oos = net(rg, tau, c).loc[OOS_START:]
            m = metrics(oos)
            rows.append(dict(panel=panel, chooser=chooser, bps=c, pick=pick,
                             IS_Sharpe=IS[pick], OOS_Sharpe=m["Sharpe"],
                             OOS_CAGR=m["CAGR"], OOS_MaxDD=m["MaxDD"]))
    return pd.DataFrame(rows)


def keep_paths(df, panel):
    """4a vs RULES v2, 4b vs SPY - CORRECTED tape only (the truth), every rung."""
    g = df[(df.panel == panel) & (df.regime == "CORRECTED")]
    rows = []
    for c in RUNGS:
        s = g[g.bps == c].set_index("book")
        v2, spy = s.loc["RULESv2"], s.loc["SPY"]
        for b in [GNAME(n, gg) for n, gg in GRID] + ["RULESv1"]:
            r = s.loc[b]
            a = bool(r.H1 > v2.H1 and r.H2 > v2.H2 and r.MaxDD >= v2.MaxDD)
            bars = [("H1", r.H1 > spy.H1), ("H2", r.H2 > spy.H2), ("OOS", r.OOS > spy.OOS),
                    ("DD", abs(r.MaxDD) <= 0.60 * abs(spy.MaxDD)),
                    ("CAGR", r.CAGR >= 0.70 * spy.CAGR)]
            rows.append(dict(panel=panel, bps=c, book=b, CAGR=r.CAGR, Sharpe=r.Sharpe,
                             MaxDD=r.MaxDD, H1=r.H1, H2=r.H2, OOS=r.OOS,
                             v4a=a, v4b=all(x for _, x in bars),
                             fail4b=next((k for k, x in bars if not x), "")))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ main
def main():
    print("=" * 110)
    print("IDEA 355 - why does the (n,g) grid ORDERING invert on B136 at 0 bps only?")
    print("=" * 110)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        print(f"{k}: {v.shape}  {v.index[0].date()} -> {v.index[-1].date()}  "
              f"weekend rows={int((v.index.dayofweek >= 5).sum())}")

    frames, keeps, wfs = [], {}, []
    for name, px in panels.items():
        d, keep = sweep(px, name)
        frames.append(d); keeps[name] = keep
        wfs.append(walkforward(keep, name, d))
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(f"{OUT}.grid.csv", index=False)

    # ---- GATE 0: the 3-term identity is exact against a direct costed backtest
    print("\n" + "=" * 110)
    print("GATE 0 - S = (G - c*T)/V reproduces engine.backtest(cost_bps=c) exactly")
    print("=" * 110)
    px = panels["B136"]; start = px.index[260]
    elig, _ = eligibility(px)
    err = []
    for n, g in [(3, 0.75), (20, 1.00), (10, 0.85)]:
        w = topn_weights(elig, n, g)
        for c in RUNGS:
            direct = metrics(backtest(px, w, cost_bps=c, freq="W")["returns"].loc[start:])["Sharpe"]
            ident = df[(df.panel == "B136") & (df.regime == "CORRECTED") &
                       (df.book == GNAME(n, g)) & (df.bps == c)].S_ident.iloc[0]
            err.append(abs(direct - ident))
    print(f"max |identity - direct backtest| over 9 checks: {max(err):.3e}   (exact if ~1e-15)")

    # ---- GATE 1a: bit-for-bit against idea 39's committed grid CSV
    print("\n" + "=" * 110)
    print("GATE 1a - every shared cell equals idea 39's committed grid CSV")
    print("=" * 110)
    ref = ROOT / "research" / "backtests" / "2026-09-07_rerun-sandbox-rows-corrected_B_grid.csv"
    if ref.exists():
        a = pd.read_csv(ref).set_index(["panel", "regime", "book", "bps"])
        b = df.set_index(["panel", "regime", "book", "bps"])
        idx = a.index.intersection(b.index)
        dmax = {c: float(np.abs(a.loc[idx, c] - b.loc[idx, c]).max()) for c in
                ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS", "OOS_CAGR", "OOS_MaxDD"]}
        dmax["turnover"] = float(np.abs(a.loc[idx, "turn"] - b.loc[idx, "T"]).max())
        print(f"{len(idx)} shared cells; max abs diff per column: "
              + "  ".join(f"{k} {v:.2e}" for k, v in dmax.items()))
    else:
        print("idea 39 grid CSV not present - gate skipped")

    # ---- GATE 1: reproduce idea 39's published rank correlations
    ords = pd.concat([ordering_table(df, p) for p in panels], ignore_index=True)
    ords.to_csv(f"{OUT}.ordering.csv", index=False)
    print("\n" + "=" * 110)
    print("GATE 1 - reproduce idea 39's published rho (B136 @0bps: CALENDAR -0.538, SANDBOX -0.322;")
    print("         @10bps: +0.972 / +0.434)")
    print("=" * 110)
    chk = ords[(ords.panel == "B136") & (ords.regime.isin(["CALENDAR", "SANDBOX"])) & (ords.bps.isin([0, 10]))]
    print(chk[["regime", "bps", "rho"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- 1. the full ordering table, every regime x rung x panel (ALL reported)
    print("\n" + "=" * 110)
    print("1. ORDERING vs the corrected tape, and the SUBSTITUTION test")
    print("   rho          = Spearman(corrected Sharpe, alt Sharpe) over the 12 (n,g) books")
    print("   rho_sub_X    = same, with term X taken from the CORRECTED tape and the other two from the alt")
    print("   cost_share   = sd(cost drag) / sd(net return term) across the 12 books, corrected tape")
    print("=" * 110)
    print(ords.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- 2. the decomposition on the cell in question
    print("\n" + "=" * 110)
    print("2. B136 @ 0 bps - the 12 grid points, term by term (CORRECTED vs CALENDAR)")
    print("=" * 110)
    for c in [0, 10]:
        a = df[(df.panel == "B136") & (df.regime == "CORRECTED") & (df.bps == c)].set_index("book")
        b = df[(df.panel == "B136") & (df.regime == "CALENDAR") & (df.bps == c)].set_index("book")
        bk = [GNAME(n, g) for n, g in GRID]
        t = pd.DataFrame({
            "G_corr": a.loc[bk, "G"], "G_cal": b.loc[bk, "G"],
            "V_corr": a.loc[bk, "V"], "V_cal": b.loc[bk, "V"],
            "T_corr": a.loc[bk, "T"], "T_cal": b.loc[bk, "T"],
            "S_corr": a.loc[bk, "Sharpe"], "S_cal": b.loc[bk, "Sharpe"],
            "rank_corr": a.loc[bk, "Sharpe"].rank(ascending=False),
            "rank_cal": b.loc[bk, "Sharpe"].rank(ascending=False)})
        print(f"\n--- B136 @ {c} bps ---")
        print(t.to_string(float_format=lambda x: f"{x:.4f}"))
        print(f"cross-book sd: S_corr {t.S_corr.std(ddof=1):.4f}  S_cal {t.S_cal.std(ddof=1):.4f}   "
              f"|rank change| mean {abs(t.rank_corr - t.rank_cal).mean():.2f}")

    # ---- 3. breadth
    print("\n" + "=" * 110)
    print("3. BREADTH term - mean eligible count E_t per regime, and how often it binds (E_t < n)")
    print("=" * 110)
    br = df[df.book.str.startswith("TOP") & (df.bps == 0)].groupby(
        ["panel", "regime"]).agg(E_mean=("E_mean", "first"), nrows=("nrows", "first"),
                                 years=("years", "first"), E_binds_max=("E_binds", "max"))
    print(br.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- 4. rule 8
    wf = pd.concat(wfs, ignore_index=True)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    print("\n" + "=" * 110)
    print("4. RULE 8 walk-forward - (n,g) chosen on IS<=2016 on each CHOOSER tape, scored OOS on CORRECTED")
    print("=" * 110)
    spy_ref = {}
    for p, px in panels.items():
        start = px.index[260]
        s = px["SPY"].pct_change().fillna(0).loc[start:]
        m, mo = metrics(s), metrics(s.loc[OOS_START:])
        h = len(s) // 2
        spy_ref[p] = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                          H1=metrics(s.iloc[:h])["Sharpe"], H2=metrics(s.iloc[h:])["Sharpe"],
                          OOS=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"])
        v2 = df[(df.panel == p) & (df.regime == "CORRECTED") & (df.book == "RULESv2") & (df.bps == 10)].iloc[0]
        print(f"\n{p}: SPY full {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%} "
              f"halves {spy_ref[p]['H1']:.3f}/{spy_ref[p]['H2']:.3f} OOS {mo['Sharpe']:.3f} "
              f"({mo['CAGR']:.2%}/{mo['MaxDD']:.2%})   |   RULES v2 @10bps "
              f"{v2.CAGR:.2%}/{v2.Sharpe:.3f}/{v2.MaxDD:.2%} halves {v2.H1:.3f}/{v2.H2:.3f} OOS {v2.OOS:.3f}")
    print()
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for p in panels:
        for c in RUNGS:
            a = wf[(wf.panel == p) & (wf.chooser == "CORRECTED") & (wf.bps == c)].iloc[0]
            for ch in ["CALENDAR", "SANDBOX"]:
                b = wf[(wf.panel == p) & (wf.chooser == ch) & (wf.bps == c)].iloc[0]
                print(f"  {p} @{c:>2}bps  {ch:<8} pick {b['pick']:<12} vs CORRECTED pick {a['pick']:<12} "
                      f"dOOS_Sharpe {b.OOS_Sharpe - a.OOS_Sharpe:+.4f}  dOOS_CAGR {b.OOS_CAGR - a.OOS_CAGR:+.2%}")

    # ---- 5. both KEEP paths
    kp = pd.concat([keep_paths(df, p) for p in panels], ignore_index=True)
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)
    print("\n" + "=" * 110)
    print("5. BOTH KEEP PATHS on the corrected tape - all 12 grid points x 2 panels x 3 rungs")
    print("=" * 110)
    print(kp.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n4a TRUE: {int(kp.v4a.sum())}/{len(kp)}    4b TRUE: {int(kp.v4b.sum())}/{len(kp)}")
    print("first failing 4b bar, counts:", kp[~kp.v4b].fail4b.value_counts().to_dict())
    print("\nfiles written:", f"{OUT}.grid.csv / .ordering.csv / .walkforward.csv / .keeppaths.csv")


if __name__ == "__main__":
    main()

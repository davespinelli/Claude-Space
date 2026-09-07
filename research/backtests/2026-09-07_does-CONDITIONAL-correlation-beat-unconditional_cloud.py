#!/usr/bin/env python3
"""QUEUE idea 358 — does-CONDITIONAL-correlation-beat-unconditional (cloud, 2026-09-07).

Question (QUEUE.md wording)
---------------------------
"idea 103's axis is full-window daily correlation, which cannot see a sleeve whose
correlation FALLS in crises (the only time a diversifier earns its keep).  Rebuild the
ladder's x-axis as correlation measured on the worst-decile SPY days only, and re-run idea
103's regression against it.  Max 2 params (crisis-day quantile, f)."

What idea 103 established, and what this run must answer
-------------------------------------------------------
Idea 103 built an 11-sleeve ladder (cash null, S4 = TLT/GLD/DBC/UUP, the five equity ETFs
added one at a time along a forward and a reverse path to the shared S9 endpoint) and
regressed idea 100's convexity statistic on the sleeve's realised UNCONDITIONAL daily
correlation to the book.  Two findings:
  (a) the curve is monotone (spearman -0.624 over 360 points), and
  (b) the design variable is FALSIFIED: adding equity ETFs raises the sleeve's own standalone
      Sharpe, which sits inside the linear blend conv_per_pp subtracts; residualise on it and
      the relationship collapses to spearman -0.056 (idea 106 later re-stated the corrected
      figure as -0.339 at natural gross).
Idea 103 also reported that the negative end of the axis DOES NOT EXIST: the realised span is
0.000..0.744, so "diversifier" in this record has never meant negative correlation.

This run replaces the x-axis with correlation measured only on the worst-q SPY days and asks
three separate questions, so a partial answer cannot be read as a whole one:
  Q1 (descriptive)  Does the crisis axis reach the negative end the unconditional axis cannot?
  Q2 (statistical)  Does the crisis axis survive the own-standalone-Sharpe control that killed
                    the unconditional one?  Same regression, same residualisation, same points.
  Q3 (capital)      Rule 8.  Pre-register three IS-only choosers over the SAME ladder --
                    lowest unconditional corr, lowest crisis corr, highest IS Sharpe -- and
                    compare their untouched OOS Sharpe.  A design variable that cannot pick
                    better out of sample is not a design variable however good its regression.

Design (PROTOCOL rules 1-9)
---------------------------
Panels      : load_universe() (u56) and load_universe(broad=True) (136).  SURVIVORSHIP: both
              are current constituents, so equity levels are biased up; the sleeve assets are
              ETFs and are not exposed to it.  The bias hits every arm identically.
TUNED (2)   : crisis-day quantile q in {0.05, 0.10, 0.20} (0.10 = the queue's "worst decile",
              pre-registered as the headline) x f in {0, .25, .50, .75, 1.00}.
              The 11-sleeve ladder is the regression's x-AXIS, not a tuned dial: every rung is
              reported, and the only place a sleeve is ever CHOSEN is inside rule 8, where the
              choice is made on 2009-2016 alone by a pre-registered rule.
CONTROLS    : book in {v1, top20, ewall}, universe in {u56, broad}, gross convention in
              {natural, matched}, cost in {0,5,10,15,20,25} bps.  Reported, never selected on.
              Held at incumbent values: GROSS 0.75, cadence W, 60d vol window, (252,126,63)
              momentum lags, 10 bps headline cost, next-day execution (engine shifts weights).
STATISTICS  : conv_per_pp = (Sharpe(f) - linear blend) / pp of CAGR surrendered  [idea 100's]
              raw_per_pp  = (Sharpe(f) - Sharpe(0)) / pp of CAGR surrendered     [idea 359's]
              Both regressed on both axes, with and without the own-Sharpe control.
KEEP paths  : 4a and 4b evaluated on every one of the 660 grid points, both reported.
Rule 8      : parameters chosen on 2009-2016 only; 2017-2026 evaluated untouched.

COST NOTE: engine.backtest applies costs as gross_returns - turnover * bps/1e4 with a
bps-independent holdings path, so each weight matrix is run ONCE at 0 bps and every rung of
the ladder derived exactly.  Asserted against a direct 10 bps run at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
It hits every arm, the baseline and SPY identically.  It matters MORE here than usual and is
handled explicitly: a zero-return SPY weekend row is not a crisis day, but it does sit in the
left tail's denominator, so the crisis-day selection below is taken over NON-ZERO SPY rows
only and the count of dropped rows is printed.

Deterministic, standalone:
    python research/backtests/2026-09-07_does-CONDITIONAL-correlation-beat-unconditional_cloud.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

COST_BPS, FREQ, GROSS = 10, "W", 0.75
COST_LADDER = (0, 5, 10, 15, 20, 25)
MOM_LAGS, VOL_WINDOW = (252, 126, 63), 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
QGRID = [0.05, 0.10, 0.20]
Q_STAR = 0.10                       # the queue's pre-registered "worst decile"
SPLIT, IS_END = "2017-01-01", "2016-12-31"
CORE4 = ["TLT", "GLD", "DBC", "UUP"]
FWD = ["SPY", "QQQ", "IWM", "EFA", "EEM"]
REV = ["EEM", "EFA", "IWM", "QQQ", "SPY"]
OUT = Path(__file__).with_suffix("")


def build_ladder():
    """idea 103's ladder verbatim: cash null, core, both add paths, shared S9 endpoint."""
    L = {"SCASH": [], "S4": list(CORE4)}
    for i in range(1, len(FWD)):
        L[f"S{4+i}f"] = CORE4 + FWD[:i]
    for i in range(1, len(REV)):
        L[f"S{4+i}r"] = CORE4 + REV[:i]
    L["S9"] = CORE4 + FWD
    return L


SLEEVES = build_ladder()


# ---------------------------------------------------------------- sleeves / books
def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if not assets:
        return out
    sub = px[assets]
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def book_v1(px):
    return rules_v1_weights(px)


def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < 0.60)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def book_ewall(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = (above & (vol20 < 0.60) & s.notna()).astype(float)
    k = elig.sum(axis=1)
    return elig.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": book_v1, "top20": book_top20, "ewall": book_ewall}


def blend(E, S, f, conv):
    """natural = (1-f)E + fS as-is; matched = the same rescaled per row to E's own gross."""
    w = (1 - f) * E + f * S
    if conv == "natural":
        return w
    g, ge = w.sum(axis=1), E.sum(axis=1)
    return w.mul((ge / g.where(g > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- helpers
def run0(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(gr, to, bps=COST_BPS):
    return gr - to * bps / 1e4


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    ic, is_, _ = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2, IS_CAGR=ic, IS_Sharpe=is_,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan, np.nan, np.nan, 0
    b = np.polyfit(x, y, 1)
    yh = np.polyval(b, x)
    ss = ((y - y.mean()) ** 2).sum()
    return float(b[0]), float(b[1]), float(1 - ((y - yh) ** 2).sum() / ss if ss > 0 else np.nan), int(len(x))


def resid_on(y, z):
    """y residualised on z (least squares, NaNs held out and returned as NaN)."""
    y, z = np.asarray(y, float), np.asarray(z, float)
    ok = np.isfinite(y) & np.isfinite(z)
    out = np.full(len(y), np.nan)
    if ok.sum() >= 3:
        b = np.polyfit(z[ok], y[ok], 1)
        out[ok] = y[ok] - np.polyval(b, z[ok])
    return out


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


def crisis_mask(spy_r, q, window=None):
    """Worst-q SPY days, taken over NON-ZERO rows only (calendar-index weekends are zeros
    and are not crises).  window, if given, restricts the quantile to that slice."""
    src = spy_r if window is None else spy_r.loc[window]
    live = src[src != 0.0]
    thr = live.quantile(q)
    return (spy_r <= thr) & (spy_r != 0.0)


# ---------------------------------------------------------------- main
def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}

    px0 = universes["u56"]
    st0 = px0.index[260]
    w0 = book_top20(px0)
    gr0, to0 = run0(px0, w0, st0)
    direct = backtest(px0, w0, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st0:]
    err = float((net(gr0, to0) - direct).abs().max())
    print(f"[gate] cost linearity max |derived - direct| at {COST_BPS} bps = {err:.3e}")
    assert err < 1e-12, "cost is not linear in this engine — ladder derivation invalid"

    print(f"[ladder] {len(SLEEVES)} sleeves x {len(BOOKS)} books x 2 conventions x "
          f"{len(FGRID)} f x {len(universes)} universes = "
          f"{len(SLEEVES)*len(BOOKS)*2*len(FGRID)*len(universes)} points")
    for k, v in SLEEVES.items():
        print(f"   {k:6s} {len(v)} assets: {'CASH (holds nothing)' if not v else ' '.join(v)}")

    records, corr_rows, refs, cache, ret_cache = [], [], {}, {}, {}
    for tag, px in universes.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        print("\n" + "=" * 118)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> "
              f"{px.index[-1].date()} | eval from {start.date()} | {len(spy_r)} rows")
        zero = int((spy_r == 0.0).sum())
        print(f"    SPY zero-return rows (calendar-index weekends + holidays): {zero} "
              f"({zero/len(spy_r):.1%}) — excluded from every crisis-day quantile")

        bgr, bto = run0(px, rules_v2_weights(px), start)
        base = full_row(net(bgr, bto))
        v1gr, v1to = run0(px, rules_v1_weights(px), start)
        v1 = full_row(net(v1gr, v1to))
        spy = full_row(spy_r)
        refs[tag] = (base, v1, spy)
        print("\nReference rows (same days, same 10 bps):")
        print(fmt(pd.DataFrame({"RULES v2 (live baseline)": base, "RULES v1": v1, "SPY": spy}).T))
        print(f"4b bars: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / OOS "
              f"{spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60*spy['MaxDD']:.1%} · "
              f"CAGR >= {0.70*spy['CAGR']:.2%}")

        # crisis-day thresholds, printed so the axis is auditable
        for q in QGRID:
            m = crisis_mask(spy_r, q)
            print(f"    q={q:.2f}: threshold {spy_r[spy_r!=0].quantile(q):+.4%}, "
                  f"{int(m.sum())} crisis days, mean SPY {spy_r[m].mean():+.4%}")

        S_w = {s: sleeve_weights(px, a) for s, a in SLEEVES.items()}
        S_r, B_r = {}, {}
        for s in SLEEVES:
            gr, to = run0(px, S_w[s], start)
            S_r[s] = net(gr, to)
        for b, bfn in BOOKS.items():
            gr, to = run0(px, bfn(px), start)
            B_r[b] = net(gr, to)

        # ------- the two axes, per (sleeve, book) -------
        for s in SLEEVES:
            for b in BOOKS:
                x, y = S_r[s], B_r[b]
                unc = 0.0 if s == "SCASH" else float(np.corrcoef(x, y)[0, 1])
                row = dict(universe=tag, sleeve=s, book=b, n_assets=len(SLEEVES[s]),
                           corr_uncond=unc)
                for q in QGRID:
                    m = crisis_mask(spy_r, q)
                    row[f"corr_crisis_q{int(q*100):02d}"] = (
                        0.0 if s == "SCASH" else float(np.corrcoef(x[m], y[m])[0, 1]))
                # IS-only versions (rule 8 choosers may only see 2009-2016)
                isw = slice(None, IS_END)
                row["corr_uncond_IS"] = (0.0 if s == "SCASH"
                                         else float(np.corrcoef(x.loc[isw], y.loc[isw])[0, 1]))
                mIS = crisis_mask(spy_r, Q_STAR, window=isw) & (spy_r.index <= pd.Timestamp(IS_END))
                row["corr_crisis_IS"] = (0.0 if s == "SCASH"
                                         else float(np.corrcoef(x[mIS], y[mIS])[0, 1]))
                corr_rows.append(row)

        # ------- the grid -------
        for bname, bfn in BOOKS.items():
            E = bfn(px)
            for conv in ("natural", "matched"):
                for sname in SLEEVES:
                    for f in FGRID:
                        w = blend(E, S_w[sname], f, conv)
                        gr, to = run0(px, w, start)
                        cache[(tag, bname, conv, sname, f)] = (gr, to)
                        r = net(gr, to)
                        ret_cache[(tag, bname, conv, sname, f)] = r
                        row = full_row(r)
                        row["Turn_yr"] = to.sum() / (len(r) / 252)
                        row["Gross"] = w.loc[start:].sum(axis=1).mean()
                        row["p4a"] = keep_4a(row, base)
                        row["p4b"] = keep_4b(row, spy)
                        records.append(dict(universe=tag, book=bname, conv=conv, sleeve=sname,
                                            n_assets=len(SLEEVES[sname]), f=f, **row))
        print(f"    grid done: {len([r for r in records if r['universe']==tag])} points")

    G = pd.DataFrame(records)
    C = pd.DataFrame(corr_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.axes.csv", index=False)

    # ---------------------------------------------------------- reproduction gates
    print("\n" + "=" * 118)
    print("### REPRODUCTION GATES (idea 103's published numbers, recomputed here)")
    g1 = G[(G.sleeve == "SCASH") & (G.conv == "matched")]
    spread = g1.groupby(["universe", "book"])["Sharpe"].agg(lambda v: v.max() - v.min()).max()
    print(f"  matched cash sleeve is algebraically the book: max Sharpe spread across f = "
          f"{spread:.3e}  {'PASS' if spread < 1e-9 else 'FAIL'}")
    for (u, b, cv, s, f), label in [(("u56", "top20", "natural", "S4", 0.25), "idea 100 u56/top20 S4 f=0.25 natural"),
                                    (("u56", "top20", "matched", "S4", 0.25), "same, matched"),
                                    (("u56", "top20", "natural", "S4", 0.50), "idea 100 u56/top20 S4 f=0.50 natural"),
                                    (("u56", "top20", "natural", "S9", 1.00), "S9 standalone (idea 26 control)")]:
        r = G[(G.universe == u) & (G.book == b) & (G.conv == cv) & (G.sleeve == s) & (G.f == f)].iloc[0]
        print(f"  {label:44s} {r.CAGR:6.1%} / {r.Sharpe:.2f} / {r.MaxDD:6.1%} / "
              f"{r.H1:.2f} / {r.H2:.2f}")

    print("\n  idea 103's unconditional axis, reproduced (mean corr over books x universes):")
    print(fmt(C.groupby("sleeve")["corr_uncond"].mean().sort_values().to_frame("corr_uncond").T))

    # ---------------------------------------------------------- Q1: the axes
    print("\n" + "=" * 118)
    print("### Q1 — DOES THE CRISIS AXIS REACH THE NEGATIVE END THE UNCONDITIONAL ONE CANNOT?")
    print("  Idea 103: realised unconditional span 0.000..0.744, no negative end exists.")
    print("  If crisis-day correlation is a DIFFERENT variable it must (a) move the ordering and")
    print("  (b) plausibly go negative for a real diversifier.\n")
    axes = ["corr_uncond"] + [f"corr_crisis_q{int(q*100):02d}" for q in QGRID]
    lad = C.groupby("sleeve")[axes].mean().sort_values("corr_uncond")
    print(fmt(lad))
    print("\n  span of each axis over the 11 sleeves (mean over books x universes):")
    print(fmt(pd.DataFrame({"min": lad.min(), "max": lad.max(), "span": lad.max() - lad.min()}).T))
    print("\n  rank correlation of each crisis axis against the unconditional axis "
          "(over all sleeve x book x universe points):")
    for a in axes[1:]:
        print(f"    {a}: spearman vs corr_uncond = {spearman(C['corr_uncond'], C[a]):+.4f}, "
              f"pearson = {np.corrcoef(C['corr_uncond'], C[a])[0,1]:+.4f}, "
              f"mean shift = {(C[a]-C['corr_uncond']).mean():+.4f}")
    lad.to_csv(f"{OUT}.ladder.csv")

    # ---------------------------------------------------------- the statistics
    print("\n" + "=" * 118)
    print("### THE CONVEXITY STATISTICS (idea 100's conv_per_pp and idea 359's raw_per_pp)")
    D = []
    for (u, b, cv, s), sub in G.groupby(["universe", "book", "conv", "sleeve"]):
        sub = sub.set_index("f")
        sh, cg = sub["Sharpe"], sub["CAGR"]
        crow = C[(C.universe == u) & (C.sleeve == s) & (C.book == b)].iloc[0]
        for f in FGRID[1:]:
            giveup = 100.0 * (cg[0.0] - cg[f])
            lin = (1 - f) * sh[0.0] + f * sh[1.00]
            D.append(dict(universe=u, book=b, conv=cv, sleeve=s, f=f,
                          n_assets=len(SLEEVES[s]),
                          corr_uncond=crow.corr_uncond,
                          **{a: crow[a] for a in axes[1:]},
                          dSharpe=sh[f] - sh[0.0], dCAGR_pp=-giveup,
                          conv_per_pp=(sh[f] - lin) / max(giveup, 1e-9),
                          raw_per_pp=((sh[f] - sh[0.0]) / giveup) if giveup > 1e-6 else np.nan,
                          sleeve_Sharpe=sh[1.00]))
    D = pd.DataFrame(D)
    D.to_csv(f"{OUT}.convexity.csv", index=False)
    ok = D[D.sleeve != "SCASH"].copy()      # SCASH's f=1 Sharpe is undefined by construction
    print(f"  {len(D)} statistic points ({len(ok)} excluding the cash null).")
    print(f"  corr(sleeve standalone Sharpe, corr_uncond) = "
          f"{np.corrcoef(ok.corr_uncond, ok.sleeve_Sharpe)[0,1]:+.4f}")
    for a in axes[1:]:
        print(f"  corr(sleeve standalone Sharpe, {a}) = "
              f"{np.corrcoef(ok[a], ok.sleeve_Sharpe)[0,1]:+.4f}")

    # ---------------------------------------------------------- Q2: the regression
    print("\n" + "=" * 118)
    print("### Q2 — THE REGRESSION, RAW AND AFTER THE OWN-SHARPE CONTROL")
    print("  This is idea 103's exact test with the x-axis swapped.  The control is the one that")
    print("  falsified the unconditional axis: residualise the statistic on the sleeve's own")
    print("  standalone Sharpe (the term inside conv_per_pp's linear-blend benchmark) and re-fit.")
    print("  A conditional axis 'beats' the unconditional one only if its controlled relationship")
    print("  is materially stronger, on the SAME points.\n")
    reg = []
    for stat in ("conv_per_pp", "raw_per_pp"):
        for scope, sub in [("all (natural+matched)", ok),
                           ("natural only", ok[ok.conv == "natural"]),
                           ("matched only", ok[ok.conv == "matched"])]:
            for a in axes:
                sl, ic, r2, n = ols(sub[a], sub[stat])
                rho = spearman(sub[a], sub[stat])
                res = resid_on(sub[stat], sub["sleeve_Sharpe"])
                sl2, _, r22, n2 = ols(sub[a], res)
                rho2 = spearman(sub[a], res)
                reg.append(dict(stat=stat, scope=scope, axis=a, n=n, slope=sl, R2=r2, spearman=rho,
                                slope_ctrl=sl2, R2_ctrl=r22, spearman_ctrl=rho2,
                                retained=abs(rho2) / abs(rho) if rho and np.isfinite(rho) else np.nan))
    R = pd.DataFrame(reg)
    R.to_csv(f"{OUT}.regression.csv", index=False)
    for stat in ("conv_per_pp", "raw_per_pp"):
        print(f"  --- {stat}")
        print(fmt(R[R.stat == stat].set_index(["scope", "axis"])[
            ["n", "slope", "R2", "spearman", "slope_ctrl", "R2_ctrl", "spearman_ctrl", "retained"]]))
        print()

    print("  HEADLINE COMPARISON (conv_per_pp, all points, q=0.10 = the queue's worst decile):")
    for a in ("corr_uncond", "corr_crisis_q10"):
        r = R[(R.stat == "conv_per_pp") & (R.scope == "all (natural+matched)") & (R.axis == a)].iloc[0]
        print(f"    {a:20s} spearman {r.spearman:+.4f} -> after control {r.spearman_ctrl:+.4f} "
              f"(R2 {r.R2:.4f} -> {r.R2_ctrl:.4f}, {r.retained:.1%} of |rho| retained)")

    # within-cell monotonicity, both axes
    print("\n  Within-cell (universe x book x conv x f) spearman, mean over cells:")
    mono = []
    for (u, b, cv, f), ss in ok.groupby(["universe", "book", "conv", "f"]):
        row = dict(universe=u, book=b, conv=cv, f=f)
        for a in axes:
            row[a] = spearman(ss[a], ss.conv_per_pp)
            row[a + "_raw"] = spearman(ss[a], ss.raw_per_pp)
        mono.append(row)
    M = pd.DataFrame(mono)
    M.to_csv(f"{OUT}.monotonicity.csv", index=False)
    print(fmt(M[[c for c in M.columns if c.startswith("corr_")]].mean().to_frame("mean_within_cell_rho").T))
    print("  fraction of cells with the expected NEGATIVE sign:")
    print(fmt((M[[c for c in M.columns if c.startswith("corr_")]] < 0).mean().to_frame("share_negative").T))

    # ---------------------------------------------------------- Q3: rule 8
    print("\n" + "=" * 118)
    print("### Q3 — RULE 8.  THREE PRE-REGISTERED IS-ONLY CHOOSERS OVER THE SAME LADDER")
    print("  Each chooser sees 2009-2016 ONLY and picks one (sleeve, f) per cell; 2017-2026 is")
    print("  evaluated untouched.  CORR_UNCOND / CORR_CRISIS pick the lowest IS correlation at the")
    print("  pre-registered f=0.50; IS_SHARPE picks the joint IS-Sharpe argmax over (sleeve, f).")
    print("  Anchors: the no-sleeve control (f=0), RULES v2, RULES v1, SPY — all OOS.\n")
    wf = []
    for (u, b, cv), sub in G.groupby(["universe", "book", "conv"]):
        base, v1, spy = refs[u]
        ctrl = sub[(sub.f == 0.0) & (sub.sleeve == "S4")].iloc[0]
        cand = sub[sub.sleeve != "SCASH"]
        picks = {}
        c_u = C[C.universe == u].set_index(["sleeve", "book"])
        f05 = cand[cand.f == 0.50]
        for nm, col in (("CORR_UNCOND", "corr_uncond_IS"), ("CORR_CRISIS", "corr_crisis_IS")):
            key = f05.sleeve.map(lambda s: c_u.loc[(s, b), col])
            picks[nm] = f05.iloc[int(np.argmin(key.values))]
        picks["IS_SHARPE"] = cand.iloc[int(np.argmax(cand.IS_Sharpe.values))]
        for nm, p in picks.items():
            wf.append(dict(universe=u, book=b, conv=cv, chooser=nm, sleeve=p.sleeve, f=p.f,
                           IS_Sharpe=p.IS_Sharpe, OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                           OOS_MaxDD=p.OOS_MaxDD, full_Sharpe=p.Sharpe, full_CAGR=p.CAGR,
                           full_MaxDD=p.MaxDD, H1=p.H1, H2=p.H2, p4a=p.p4a, p4b=p.p4b,
                           ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                           spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                           spy_OOS_MaxDD=spy["OOS_MaxDD"],
                           v2_OOS_Sharpe=base["OOS_Sharpe"], v1_OOS_Sharpe=v1["OOS_Sharpe"],
                           best_OOS_in_cell=cand.OOS_Sharpe.max()))
    W = pd.DataFrame(wf)
    W["regret"] = W.OOS_Sharpe - W.best_OOS_in_cell
    W["vs_ctrl"] = W.OOS_Sharpe - W.ctrl_OOS_Sharpe
    W["vs_spy"] = W.OOS_Sharpe - W.spy_OOS_Sharpe
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(fmt(W.set_index(["universe", "book", "conv", "chooser"])[
        ["sleeve", "f", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "ctrl_OOS_Sharpe", "spy_OOS_Sharpe", "vs_ctrl", "vs_spy", "regret"]]))
    print("\n  CHOOSER SUMMARY (12 cells each):")
    summ = W.groupby("chooser").agg(
        n=("OOS_Sharpe", "size"), mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
        mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
        mean_vs_ctrl=("vs_ctrl", "mean"), wins_vs_ctrl=("vs_ctrl", lambda v: int((v > 0).sum())),
        mean_vs_spy=("vs_spy", "mean"), wins_vs_spy=("vs_spy", lambda v: int((v > 0).sum())),
        mean_regret=("regret", "mean"), p4b=("p4b", "sum"), p4a=("p4a", "sum"))
    print(fmt(summ))
    d = (W[W.chooser == "CORR_CRISIS"].set_index(["universe", "book", "conv"]).OOS_Sharpe
         - W[W.chooser == "CORR_UNCOND"].set_index(["universe", "book", "conv"]).OOS_Sharpe)
    print(f"\n  CRISIS minus UNCONDITIONAL, OOS Sharpe: mean {d.mean():+.4f}, "
          f"wins {int((d>0).sum())}/{len(d)}, ties {int((d==0).sum())}/{len(d)}")
    print(f"  cells where the two choosers picked DIFFERENT sleeves: "
          f"{int((W[W.chooser=='CORR_CRISIS'].sleeve.values != W[W.chooser=='CORR_UNCOND'].sleeve.values).sum())}/{len(d)}")

    # ---------------------------------------------------------- KEEP paths + cost ladder
    print("\n" + "=" * 118)
    print(f"### KEEP PATHS over all {len(G)} grid points (both reported, neither selected on)")
    kp = G.groupby(["universe", "conv"]).agg(n=("p4b", "size"), p4a=("p4a", "sum"),
                                             p4b=("p4b", "sum"))
    print(fmt(kp))
    p4b = G[G.p4b]
    if len(p4b):
        print(f"\n  {len(p4b)} points clear 4b.  By (sleeve, f):")
        print(fmt(p4b.groupby(["sleeve", "f"]).size().to_frame("n_4b")))
        print("\n  best 4b point per universe by OOS Sharpe:")
        print(fmt(p4b.sort_values("OOS_Sharpe", ascending=False).groupby("universe").head(2).set_index(
            ["universe", "book", "conv", "sleeve", "f"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "Turn_yr"]]))
    else:
        print("  no point clears 4b.")
    kp.to_csv(f"{OUT}.keeppaths.csv")

    print("\n  COST LADDER on the rule-8 picks (4b pass/fail by bps, all rungs reported):")
    cl = []
    for r in W.itertuples():
        base, v1, spy = refs[r.universe]
        gr, to = cache[(r.universe, r.book, r.conv, r.sleeve, r.f)]
        for bps in COST_LADDER:
            row = full_row(net(gr, to, bps))
            cl.append(dict(universe=r.universe, book=r.book, conv=r.conv, chooser=r.chooser,
                           sleeve=r.sleeve, f=r.f, bps=bps, Sharpe=row["Sharpe"],
                           OOS_Sharpe=row["OOS_Sharpe"], CAGR=row["CAGR"],
                           p4b=keep_4b(row, spy), p4a=keep_4a(row, base)))
    CL = pd.DataFrame(cl)
    CL.to_csv(f"{OUT}.costladder.csv", index=False)
    print(fmt(CL.groupby(["chooser", "bps"]).agg(p4b=("p4b", "sum"), p4a=("p4a", "sum"),
                                                 mean_OOS_Sharpe=("OOS_Sharpe", "mean")).unstack("bps")))

    print("\n" + "=" * 118)
    print("### ARTEFACTS")
    for s in (".grid.csv", ".axes.csv", ".ladder.csv", ".convexity.csv", ".regression.csv",
              ".monotonicity.csv", ".walkforward.csv", ".keeppaths.csv", ".costladder.csv"):
        print(f"   {OUT.name}{s}")


if __name__ == "__main__":
    main()

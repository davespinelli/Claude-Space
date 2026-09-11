#!/usr/bin/env python3
"""Idea 573 - "is-the-4b-PASS-RATE-a-PANEL-OF-ORIGIN-statistic-everywhere" (cloud, 2026-09-11).

The question
------------
Idea 569 found 57 of its 60 draw-level 4b passers are BONLY draws, across five characteristics
and at matched levels: the panel a draw came FROM, not what the draw looks like, decided the
KEEP count.  The queue asks whether that origin effect is a general property of the record's
draw-level 4b counts.

SCOPE, STATED HONESTLY.  The queue's literal instruction is a CENSUS of committed runs that
report 4b passes over draws.  Those counts are prose and per-file CSV schemas, not runnable
objects, and a census of them carries no price leg, so it can satisfy neither PROTOCOL rule 8
nor either KEEP path.  This run therefore REBUILDS the object the census was meant to
adjudicate - draw-level 4b pass rates split by panel of origin - as a single pre-registered
grid, run once, with every cell published:

    3 SOURCE PANELS (U56, B136, SMALL439) x 3 WIDTHS k x 3 BOOK FAMILIES x 40 DRAWS
    = 1,080 draw books, all at gross 0.75, weekly, 10 bps, next-day execution.

That is a replication of the origin effect on a construction idea 569 never used, which is
the stronger reading of "everywhere"; it is NOT a restatement of the record's committed
counts, and nothing here retires a published number.

Construction
------------
DRAWS: k names drawn WITHOUT replacement from the source panel's investable columns (SPY is
excluded from every draw and used only as the benchmark), seed 573 + draw index, so the draw
sets are a declared function of (panel, k, draw) and reproducible.
BOOK FAMILIES, each built on the drawn names ALONE:
    BAND   the RULES v2 form on the draw: every name inside its 200d +/-3% band at gross/N,
           gated-out weight to cash (de-gross, never re-spread)
    TOP10  top-10 by the record's composite with NO vol scaler, above-200d and vol20 < 0.60,
           gross/10 per name (the 2026-09-04 KEEP-4b family)
    EWALL  equal weight on every drawn name priced that day at gross 0.75 (no gate at all)
WINDOWS: warm-up px.index[260]; IS <= 2016-12-31; OOS >= 2017-01-01 (PROTOCOL rule 8).

KEEP paths (PROTOCOL rule 4), scored for every one of the 1,080 draw books:
    4a  Sharpe > RULES v2 ON THE FULL SOURCE PANEL in BOTH halves AND MaxDD no worse
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of |SPY MaxDD|, CAGR >= 70% of SPY
IS_4b is the same predicate read on the IS window ALONE: the two half-Sharpe legs are the
halves of the IS window against IS SPY's halves, the third ("OOS") leg is the IS SECOND HALF
against IS SPY's second half, and the DD cap and CAGR floor are read against IS SPY.  It is
declared here, before any count was read, purely so rule 8 has an IS-only objective.

Tuned parameters (PROTOCOL rule 4: at most two).  Every grid point published.
    1. k - the draw width, in {12, 24, 36}
    2. BOOK FAMILY - in {BAND, TOP10, EWALL}
The source panel is the QUESTION, not a tuned dial: all three are always reported.

Pre-registered gates (printed before any count is read)
-------------------------------------------------------
G1  fast_backtest reproduces engine.backtest on a probe draw book (< 1e-12).
G2  band_book(0.03, 0.75) == baseline.rules_v2_weights on a full panel (0.0).
G3  SMALL: the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST.
G4  DRAWS: re-drawing at the same seed reproduces the same name sets exactly; no draw
    contains SPY; every draw has exactly k distinct names from its own panel.
G5  CAUSALITY: a probe draw's IS statistics recomputed on a frame TRUNCATED at IS_END must
    equal the IS statistics read off the full frame (0.0).

Pre-registered bars
-------------------
B1  IS THE ORIGIN EFFECT EVERYWHERE?  PASS iff the same source panel holds the highest 4b
    pass rate in ALL 9 (family, k) cells.  PARTIAL iff it does in a strict majority.
B2  IS IT AN ORIGIN EFFECT OR A CONSTRUCTION EFFECT?  Report the spread of the 4b pass rate
    ACROSS panels at fixed (family, k) against the spread ACROSS families at fixed (panel, k).
    The larger spread names the governing variable.
B3  RULE 8.  The cell with the highest IS 4b pass rate is chosen on IS alone; its OOS pass
    rate and the OOS statistics of its declared acted book (the draw with the MEDIAN IS
    Sharpe - a fixed, non-peeking tie-break) are read ONCE against RULES v2 and SPY.

CAVEATS.  (i) SURVIVORSHIP (idea 54): all three panels are current constituents with no
delistings, so every CAGR level is inflated and both KEEP columns inherit that; SMALL439 is
the current sub-$2B screen with the 44 max_1d_move >= 1.0 names dropped.  (ii) OVERLAP (idea
719): U56 and B136 share 55 of 56 names, so they are ONE independent reading, not two;
SMALL439 is disjoint from both.  Any "three panels agree" statement here is really two.
(iii) 40 draws per cell put the pass-rate standard error near 0.08 at 50%, so differences
below ~0.16 are not resolvable (idea 528's point), and that bar is applied below.
(iv) One OOS window, read once.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state, score          # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

OUT = Path(__file__).with_suffix("")
STEM = OUT.name
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARM, COST0, FREQ0, GROSS0, BAND0, VOLCAP = 260, 10.0, "W", 0.75, 0.03, 0.60
KS, FAMILIES, NDRAW, SEED = [12, 24, 36], ["BAND", "TOP10", "EWALL"], 40, 573
SE_BAR = 0.16          # idea 528: ~2 SE at 40 draws; differences below this are not resolvable

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


# ------------------------------------------------------------------ machinery (record's own)
def fast_backtest(prices, weights, freq="W", cost_bps=10.0):
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(pr - turn * cost_bps / 1e4, index=prices.index)


def M0(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan, Sharpe=M0(r),
                MaxDD=(eq / eq.cummax() - 1).min(), H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band=BAND0, gross=GROSS0):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def topn_book(px, n=10, gross=GROSS0, volcap=VOLCAP):
    sc, above, vol20 = score(px, vol_scale=False)
    r = sc.where(above & (vol20 < volcap)).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def make_book(fam, sub):
    if fam == "BAND":  return band_book(sub)
    if fam == "TOP10": return topn_book(sub, 10)
    if fam == "EWALL": return ew_gross(sub, GROSS0)
    raise ValueError(fam)


def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    panels["SMALL439"] = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    return panels, len(sm.columns) - len([c for c in sm.columns if c == "SPY" or c not in bad])


def draw_names(px, k, d, seed=SEED):
    """k distinct names drawn WITHOUT replacement, SPY excluded; a pure function of (k, d)."""
    cols = sorted([c for c in px.columns if c != "SPY"])
    rng = np.random.default_rng(seed * 100000 + k * 1000 + d)
    return sorted(rng.choice(cols, size=k, replace=False).tolist())


def pass4a(m, mb):
    return bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])


def pass4b(m, oos_s, ms, spy_oos_s):
    return bool(m["H1"] > ms["H1"] and m["H2"] > ms["H2"] and oos_s > spy_oos_s
                and abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]) and m["CAGR"] >= 0.70 * ms["CAGR"])


def main():
    P("=" * 100); P(f"IDEA 573 -- {STEM}"); P("=" * 100)
    panels, n_dropped = load_panels()

    # ------------------------------------------------------------- gates
    P("\n(A) PRE-REGISTERED GATES -- run before any count is read")
    ok = True
    px = panels["U56"]; start = px.index[WARM]
    g2 = float(np.abs(band_book(px).values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights        : {g2:.3e}  {'PASS' if g2 == 0 else 'FAIL'}")
    ok &= g2 == 0.0
    probe = px[draw_names(px, 24, 0)]
    wprobe = band_book(probe)
    slow = backtest(probe, wprobe, cost_bps=COST0, freq=FREQ0)["returns"]
    fast = fast_backtest(probe, wprobe, FREQ0, COST0)
    g1 = float(np.abs(slow.loc[start:].values - fast.loc[start:].values).max())
    P(f"  G1 fast_backtest == engine.backtest (probe draw)   : {g1:.3e}  {'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12
    P(f"  G3 SMALL dropped max_1d_move>=1.0 tickers          : {n_dropped} dropped -> "
      f"{panels['SMALL439'].shape[1]} cols  {'PASS' if n_dropped == 44 else 'FAIL'}")
    ok &= n_dropped == 44
    g4 = True
    for pn, p in panels.items():
        for k in KS:
            for d in (0, 7, 39):
                a, b = draw_names(p, k, d), draw_names(p, k, d)
                g4 &= (a == b) and len(set(a)) == k and "SPY" not in a and set(a) <= set(p.columns)
    P(f"  G4 draws reproducible, SPY-free, k distinct names  : {'PASS' if g4 else 'FAIL'}")
    ok &= g4
    tp = probe.loc[:IS_END]
    g5 = float(np.abs(fast.loc[start:IS_END].values
                      - fast_backtest(tp, band_book(tp), FREQ0, COST0).loc[start:].values).max())
    P(f"  G5 IS statistics on a TRUNCATED frame              : {g5:.3e}  {'PASS' if g5 == 0 else 'FAIL'}")
    ok &= g5 == 0.0
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- results below are not to be trusted'}")

    # ------------------------------------------------------------- comparands
    P("\n(B) COMPARANDS -- RULES v2 and SPY on each FULL source panel (the 4a / 4b bars)")
    bars = {}
    for pn, p in panels.items():
        s = p.index[WARM]
        spy = p["SPY"].pct_change().fillna(0).loc[s:]
        inc = fast_backtest(p, band_book(p), FREQ0, COST0).loc[s:]
        bars[pn] = dict(spy=M(spy), spy_oos=M(spy.loc[OOS_START:]), spy_is=M(spy.loc[:IS_END]),
                        inc=M(inc), inc_oos=M(inc.loc[OOS_START:]), inc_is=M(inc.loc[:IS_END]))
        b = bars[pn]
        P(f"  {pn:9s} RULES v2 CAGR {b['inc']['CAGR']:.2%} Sharpe {b['inc']['Sharpe']:.4f} "
          f"MaxDD {b['inc']['MaxDD']:.2%} H1/H2 {b['inc']['H1']:.3f}/{b['inc']['H2']:.3f} "
          f"OOS {b['inc_oos']['CAGR']:.2%}/{b['inc_oos']['Sharpe']:.4f} || SPY CAGR "
          f"{b['spy']['CAGR']:.2%} Sharpe {b['spy']['Sharpe']:.4f} MaxDD {b['spy']['MaxDD']:.2%} "
          f"H1/H2 {b['spy']['H1']:.3f}/{b['spy']['H2']:.3f} OOS {b['spy_oos']['Sharpe']:.4f}")

    # ------------------------------------------------------------- the 1,080 draw books
    P(f"\n(C) THE GRID -- {len(panels)} panels x {len(KS)} widths x {len(FAMILIES)} families x "
      f"{NDRAW} draws = {len(panels)*len(KS)*len(FAMILIES)*NDRAW} draw books")
    rows = []
    for pn, p in panels.items():
        s = p.index[WARM]; b = bars[pn]
        for k in KS:
            for d in range(NDRAW):
                sub = p[draw_names(p, k, d)]
                for fam in FAMILIES:
                    r = fast_backtest(sub, make_book(fam, sub), FREQ0, COST0).loc[s:]
                    m, mo, mi = M(r), M(r.loc[OOS_START:]), M(r.loc[:IS_END])
                    rows.append(dict(
                        panel=pn, k=k, family=fam, draw=d,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        p4a=pass4a(m, b["inc"]),
                        p4b=pass4b(m, mo["Sharpe"], b["spy"], b["spy_oos"]["Sharpe"]),
                        IS_p4b=pass4b(mi, mi["H2"], b["spy_is"], b["spy_is"]["H2"]),
                        OOS_p4b_leg=bool(mo["Sharpe"] > b["spy_oos"]["Sharpe"]
                                         and abs(mo["MaxDD"]) <= 0.60 * abs(b["spy_oos"]["MaxDD"])
                                         and mo["CAGR"] >= 0.70 * b["spy_oos"]["CAGR"])))
        P(f"  {pn} done ({len(rows)} rows)")
    g = pd.DataFrame(rows)
    g.to_csv(OUT.with_suffix(".draws.csv"), index=False)

    # ------------------------------------------------------------- the answer
    P("\n(D) 4b PASS RATE BY PANEL OF ORIGIN -- every (family, k) cell published")
    piv = g.pivot_table(index=["family", "k"], columns="panel", values="p4b", aggfunc="mean")
    piv = piv[["U56", "B136", "SMALL439"]]
    piv["winner"] = piv.idxmax(axis=1); piv["spread"] = piv[["U56", "B136", "SMALL439"]].max(axis=1) - \
        piv[["U56", "B136", "SMALL439"]].min(axis=1)
    P("\n  " + piv.to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    P("\n  same table for 4a:")
    pa = g.pivot_table(index=["family", "k"], columns="panel", values="p4a", aggfunc="mean")[
        ["U56", "B136", "SMALL439"]]
    P("\n  " + pa.to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    P("\n  OOS-only 4b legs (Sharpe/DD/CAGR vs SPY on 2017+ alone):")
    po = g.pivot_table(index=["family", "k"], columns="panel", values="OOS_p4b_leg", aggfunc="mean")[
        ["U56", "B136", "SMALL439"]]
    P("\n  " + po.to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))

    P("\n(E) BARS")
    wins = piv["winner"].value_counts()
    top = wins.idxmax(); b1 = int(wins.max()) == len(piv)
    P(f"  B1 origin holds the top 4b rate in ALL 9 cells     : "
      f"{'PASS' if b1 else 'PARTIAL' if wins.max() > len(piv)/2 else 'FAIL'} "
      f"-- winners {dict(wins)} (top: {top} in {int(wins.max())} of {len(piv)})")
    across_panel = float(piv["spread"].mean())
    fam_spread = (g.pivot_table(index=["panel", "k"], columns="family", values="p4b", aggfunc="mean")
                   .agg(lambda r: r.max() - r.min(), axis=1))
    across_family = float(fam_spread.mean())
    P(f"  B2 mean 4b spread ACROSS PANELS at fixed (family,k): {across_panel:.3f}")
    P(f"     mean 4b spread ACROSS FAMILIES at fixed (panel,k): {across_family:.3f}")
    P(f"     governing variable by spread                     : "
      f"{'PANEL OF ORIGIN' if across_panel > across_family else 'BOOK FAMILY'}"
      f"   (resolution bar at 40 draws ~{SE_BAR:.2f})")
    P(f"  overall 4b pass rate by panel: " +
      ", ".join(f"{p}={g[g.panel==p].p4b.mean():.3f}" for p in ["U56", "B136", "SMALL439"]) +
      f" | by family: " + ", ".join(f"{f}={g[g.family==f].p4b.mean():.3f}" for f in FAMILIES) +
      f" | by k: " + ", ".join(f"{k}={g[g.k==k].p4b.mean():.3f}" for k in KS))
    P(f"  overall 4a pass rate by panel: " +
      ", ".join(f"{p}={g[g.panel==p].p4a.mean():.3f}" for p in ["U56", "B136", "SMALL439"]))

    # ------------------------------------------------------------- rule 8
    P("\n(F) RULE 8 -- the cell chosen on IS ALONE, OOS read ONCE")
    isr = g.groupby(["panel", "family", "k"]).agg(
        IS_p4b_rate=("IS_p4b", "mean"), OOS_p4b_rate=("p4b", "mean"),
        IS_Sharpe_med=("IS_Sharpe", "median"), OOS_Sharpe_med=("OOS_Sharpe", "median"),
        OOS_CAGR_med=("OOS_CAGR", "median"), OOS_MaxDD_med=("OOS_MaxDD", "median")).reset_index()
    isr = isr.sort_values(["IS_p4b_rate", "IS_Sharpe_med"], ascending=False)
    isr.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P("\n  " + isr.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    pick = isr.iloc[0]
    P(f"\n  IS pick (highest IS 4b rate, ties to median IS Sharpe): panel={pick.panel} "
      f"family={pick.family} k={int(pick.k)}  IS 4b rate {pick.IS_p4b_rate:.3f} -> "
      f"OOS 4b rate {pick.OOS_p4b_rate:.3f}")
    cell = g[(g.panel == pick.panel) & (g.family == pick.family) & (g.k == pick.k)]
    acted = cell.sort_values("IS_Sharpe", kind="mergesort").iloc[len(cell) // 2]
    b = bars[pick.panel]
    P(f"  ACTED BOOK (declared tie-break: the MEDIAN IS Sharpe draw, #{int(acted.draw)}):")
    P(f"    full   CAGR {acted.CAGR:.2%} Sharpe {acted.Sharpe:.4f} MaxDD {acted.MaxDD:.2%} "
      f"H1/H2 {acted.H1:.4f}/{acted.H2:.4f}")
    P(f"    OOS    CAGR {acted.OOS_CAGR:.2%} Sharpe {acted.OOS_Sharpe:.4f} MaxDD {acted.OOS_MaxDD:.2%}")
    P(f"    vs RULES v2 OOS  CAGR {b['inc_oos']['CAGR']:.2%} Sharpe {b['inc_oos']['Sharpe']:.4f} "
      f"MaxDD {b['inc_oos']['MaxDD']:.2%}")
    P(f"    vs SPY      OOS  CAGR {b['spy_oos']['CAGR']:.2%} Sharpe {b['spy_oos']['Sharpe']:.4f} "
      f"MaxDD {b['spy_oos']['MaxDD']:.2%}")
    P(f"    4a {bool(acted.p4a)}   4b {bool(acted.p4b)}")
    rho = isr[["IS_p4b_rate", "OOS_p4b_rate"]].corr(method="spearman").iloc[0, 1]
    P(f"  IS->OOS transport of the 4b rate over the 27 cells : Spearman {rho:+.4f}")
    P(f"  B3 rule-8 pick clears 4b                           : "
      f"{'YES' if bool(acted.p4b) else 'NO'}; cell OOS 4b rate {pick.OOS_p4b_rate:.3f}")

    piv.to_csv(OUT.with_suffix(".bypanel.csv"))
    OUT.with_suffix(".console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

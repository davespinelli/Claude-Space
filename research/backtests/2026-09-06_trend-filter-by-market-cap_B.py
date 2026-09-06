#!/usr/bin/env python3
"""IDEA 51  trend-filter-by-market-cap   (lane B, 2026-09-06)

QUESTION (QUEUE idea 51, verbatim)
    Idea 49 showed the 200d/vol20 eligibility filter *destroys* 5.4 pp/yr of CAGR at
    zero cost on sub-$2B names while it is the whole edge on universe.json.  Isolate
    the filter alone (EW-all-eligible vs EW-all-names, no ranking, same gross) on all
    three universes and, if a cap column can be built, by cap decile within the small
    panel.  Where does trend-following stop working, and does that boundary belong in
    RULES as a universe clause?

DESIGN
    Treatment is the ELIGIBILITY FILTER ONLY.  No ranking anywhere: every book is
    equal-weight over a set of names, so the only thing that varies is WHICH names are
    in the set and how the gated-out weight is handled.  Four filter arms per panel,
    each against its own no-filter control at the SAME gross:

        EWall        gross g spread equally over every priced tradable name  (CONTROL)
        MA-RS        gross g spread equally over names with px > 200d MA     (RESPREAD)
        MA-DG        weight g/N on those names, N = ALL priced names; rest CASH (DEGROSS)
        MAVOL-RS     eligibility = px > 200d MA AND vol20 < 0.60 (the literal v1 filter)
        MAVOL-DG     same, de-grossed

    The RS/DG pair is the whole point of splitting the filter two ways: idea 49's
    -5.4 pp/yr was measured under ONE convention, and the record (ideas 81 / 121 / 297)
    has repeatedly found that de-grossing prices in a cash drag that has nothing to do
    with selection.  RS isolates SELECTION; DG = selection + exposure.

    Panels (three universes, exactly as the record builds them):
        U56       research/universe.json,  all columns tradable (SPY is a constituent)
        B136      research/universe_broad.json (survivorship: current constituents)
        SMALL439  data/prices_small.csv, stocks only, max_1d_move < 1.0 screen applied
                  per data/SMALL_PANEL_README.md; SPY joined as BENCHMARK, not tradable.
                  SURVIVORSHIP: current constituents of a sub-$2B screen only.

    Cap deciles inside the small panel — TWO size columns, because neither alone is
    honest:
        capQ   STATIC market cap from research/deepvalue/universe_under2b.csv (mktcap,
               as screened 2026-09).  This is a TODAY cap applied to 2010 data: it is a
               look-ahead CLASSIFIER (not a look-ahead signal — no return information
               enters it).  Stated, not hidden.
        advQ   DYNAMIC trailing-60d median dollar volume, ranked cross-sectionally each
               day, name assigned to its decile on the rebalance date.  Fully causal.
               Deciles are time-varying membership.
        If the two disagree about where trend-following dies, the boundary is not a
        cap boundary.

TUNED PARAMETERS (2, per PROTOCOL rule 4)
        g        gross, in {0.50, 0.75, 1.00}
        cadence  in {W, M}
    MA window (200), vol cap (0.60) and cost (10 bps) are inherited from RULES, not
    tuned.  ALL 6 grid points are reported for every arm.  Decile work is run at the
    single pre-registered point g = 0.75, weekly, so the decile ladder cannot be tuned.

RULE 8 WALK-FORWARD (required)
    g and cadence are chosen by IS Sharpe on 2010-2016 INSIDE EACH (panel, arm) — both
    the treatment and its control re-select on their own IS window — and 2017-2026 is
    read once.  OOS CAGR/Sharpe/MaxDD reported against the live RULES v2 baseline OOS
    and SPY OOS.

KEEP PATHS: 4a and 4b evaluated for every book (they are filter diagnostics, not
    capital candidates, but the protocol asks for both).  Q5 then asks whether those
    verdicts mean anything: none of these books is levered, so g is a pure scalar on an
    unchanged position vector.  If Sharpe is invariant in g while CAGR and MaxDD scale,
    4b's CAGR FLOOR and DD CAP are two LEVEL tests on one dial, the fixed 3-point ladder
    is a grid-resolution artefact, and the honest question is whether the admissible
    g-band is non-empty.  Q5 solves that band per book-form and RUNS its midpoint.

Outputs (committed):  .console.txt  .grid.csv  .deciles.csv  .walkforward.csv
                      .grossband.csv  .summary.csv  .zerocost.csv  .result.md
Deterministic; no network; ~150 backtests.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STAMP = "2026-09-06_trend-filter-by-market-cap_B"
OUT = Path(__file__).resolve().parent
COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN, VOL_CAP = 200, 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PIN_G, PIN_FREQ = 0.75, "W"          # pre-registered single point for the decile ladder
NDEC = 10

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ------------------------------------------------------------------------- books
def _priced(px, tradable):
    """1.0 where a tradable name has a price that day, else 0."""
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e

def _ew(mask, g):
    """Equal weight g over the True cells of `mask`; all-cash on empty rows."""
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)

def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()

def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)

def make_books(px, tradable, g):
    """The five arms at one gross.  Returns {name: weights DataFrame}."""
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    mv = ma & (vol20(px) < VOL_CAP)
    n_all = e.sum(axis=1).replace(0, np.nan)          # DEGROSS denominator = ALL names
    return {
        "EWall":    _ew(e, g),
        "MA-RS":    _ew(ma, g),
        "MA-DG":    (g * ma.astype(float)).div(n_all, axis=0).fillna(0.0),
        "MAVOL-RS": _ew(mv, g),
        "MAVOL-DG": (g * mv.astype(float)).div(n_all, axis=0).fillna(0.0),
    }


# ------------------------------------------------------------------------- metrics
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def run(px, w, freq, cost=COST):
    return backtest(px, w, cost_bps=cost, freq=freq)

def rowify(r, tn=None):
    m = metrics(r); h1, h2 = halves(r)
    ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ris), metrics(roos)
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d

def keep_4a(r, b):
    """Sharpe > baseline in BOTH halves and MaxDD no worse."""
    a1, a2 = halves(r); b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])

def keep_4b(r, spy, roos, spyoos):
    a1, a2 = halves(r); s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return bool(a1 > s1 and a2 > s2 and metrics(roos)["Sharpe"] > metrics(spyoos)["Sharpe"]
                and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"])


# ------------------------------------------------------------------------- panels
def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    s_stk = [c for c in s_all if c not in bad]
    P(f"  SMALL: {len(s_all)} names in panel, dropped {len(s_all) - len(s_stk)} with "
      f"max_1d_move >= 1.0 (README: unreversed level steps) -> {len(s_stk)} tradable")
    return {
        "U56":  (px56.dropna(how="all").ffill(), set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill(), set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), set(s_stk)),
    }


# ------------------------------------------------------------------------- size columns
def static_cap(cols):
    """mktcap from the deep-value screen file (TODAY's cap; a look-ahead CLASSIFIER)."""
    f = ROOT / "research" / "deepvalue" / "universe_under2b.csv"
    u = pd.read_csv(f, usecols=["ticker", "mktcap"]).dropna()
    u = u[u.mktcap > 0].drop_duplicates("ticker").set_index("ticker")["mktcap"]
    return u.reindex(cols).dropna()

def dyn_dollar_vol(px, cols):
    """Trailing 60d MEDIAN dollar volume per name.  Causal, no look-ahead."""
    vol = load_volume(small=True).reindex(px.index).reindex(columns=px.columns)
    dv = (px * vol)[cols]
    return dv.rolling(60, min_periods=30).median()


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 51  trend-filter-by-market-cap   (lane B, 2026-09-06)")
    P("=" * 112)
    P("Treatment = the ELIGIBILITY FILTER ALONE.  No ranking in any book.  Every arm is")
    P("equal-weight; RS pins gross at g (selection only), DG sends gated weight to CASH")
    P("(selection + exposure).  Control is EWall at the SAME g.  Costs 10 bps, t+1 fills.")

    panels = build_panels()
    SMALL = [k for k in panels if k.startswith("SMALL")][0]
    for nm, (px, tr) in panels.items():
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, "
          f"{px.index[0].date()} -> {px.index[-1].date()}")

    # ---------------------------------------------------------------- reference rows
    P("\n" + "=" * 112)
    P("REFERENCE  live RULES v2 baseline, RULES v1, SPY  (per panel, common sample)")
    P("=" * 112)
    ref = {}
    for nm, (px, tr) in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        b2 = run(px, rules_v2_weights(px), "W")["returns"].loc[st:]
        b1 = run(px, rules_v1_weights(px), "W")["returns"].loc[st:]
        ref[nm] = dict(start=st, spy=spy, v2=b2, v1=b1)
        for lbl, r in (("RULES v2 (live)", b2), ("RULES v1", b1), ("SPY", spy)):
            m = metrics(r); h1, h2 = halves(r); mo = metrics(r.loc[OOS_START:])
            P(f"  {nm:9s} {lbl:16s} CAGR {m['CAGR']:7.2%}  Sharpe {m['Sharpe']:6.3f} "
              f"(H1 {h1:5.3f} / H2 {h2:5.3f})  MaxDD {m['MaxDD']:7.2%}  "
              f"OOS Sharpe {mo['Sharpe']:6.3f}")

    # ---------------------------------------------------------------- Q1 the 6-point grid
    P("\n" + "=" * 112)
    P("Q1  THE FILTER ALONE, all 3 panels x 5 arms x 3 gross x 2 cadence = 90 books")
    P("    dCAGR / dSharpe are vs EWall at the SAME (g, cadence).  ALL grid points shown.")
    P("=" * 112)
    grid = []
    for pnm, (px, tr) in panels.items():
        st = ref[pnm]["start"]; spy = ref[pnm]["spy"]
        spyo = spy.loc[OOS_START:]; b2 = ref[pnm]["v2"]
        for g in GROSS:
            books = make_books(px, tr, g)
            for freq in CADENCE:
                res = {k: run(px, w, freq) for k, w in books.items()}
                rets = {k: v["returns"].loc[st:] for k, v in res.items()}
                ctl = rets["EWall"]; mc = metrics(ctl)
                for k in books:
                    r = rets[k]
                    row = dict(panel=pnm, arm=k, gross=g, cadence=freq)
                    row.update(rowify(r, res[k]["turnover"].loc[st:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    row["keep4a"] = keep_4a(r, b2)
                    row["keep4b"] = keep_4b(r, spy, r.loc[OOS_START:], spyo)
                    grid.append(row)
        P(f"  {pnm} done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)

    P("")
    hdr = (f"  {'panel':9s} {'arm':9s} {'g':>5s} {'cad':>4s} {'CAGR':>8s} {'Sharpe':>7s} "
           f"{'MaxDD':>8s} {'H1':>6s} {'H2':>6s} {'dCAGR':>8s} {'dSharpe':>8s} {'turn':>6s} 4a 4b")
    P(hdr); P("  " + "-" * (len(hdr) - 2))
    for _, x in G.iterrows():
        P(f"  {x.panel:9s} {x.arm:9s} {x.gross:5.2f} {x.cadence:>4s} {x.CAGR:8.2%} "
          f"{x.Sharpe:7.3f} {x.MaxDD:8.2%} {x.H1:6.3f} {x.H2:6.3f} "
          f"{x.dCAGR_vs_EWall:+8.2%} {x.dSharpe_vs_EWall:+8.3f} {x.turnover:6.2f} "
          f"{'Y' if x.keep4a else '.':>2s} {'Y' if x.keep4b else '.':>2s}")

    P("\n  --- the headline: mean filter cost by panel and convention (over 6 (g,cad) points)")
    P(f"  {'panel':9s} {'arm':9s} {'mean dCAGR':>11s} {'mean dSharpe':>13s} "
      f"{'dCAGR<0':>8s} {'dSh<0':>7s}")
    tab = []
    for pnm in panels:
        for arm in ["MA-RS", "MA-DG", "MAVOL-RS", "MAVOL-DG"]:
            s = G[(G.panel == pnm) & (G.arm == arm)]
            t = dict(panel=pnm, arm=arm, mean_dCAGR=s.dCAGR_vs_EWall.mean(),
                     mean_dSharpe=s.dSharpe_vs_EWall.mean(),
                     n_dCAGR_neg=int((s.dCAGR_vs_EWall < 0).sum()),
                     n_dSharpe_neg=int((s.dSharpe_vs_EWall < 0).sum()), n=len(s))
            tab.append(t)
            P(f"  {pnm:9s} {arm:9s} {t['mean_dCAGR']:+11.2%} {t['mean_dSharpe']:+13.3f} "
              f"{t['n_dCAGR_neg']:5d}/{t['n']:<2d} {t['n_dSharpe_neg']:4d}/{t['n']:<2d}")
    TAB = pd.DataFrame(tab)

    # ---------------------------------------------------------------- Q2 zero-cost replay
    P("\n" + "=" * 112)
    P("Q2  IDEA 49's CLAIM AT ITS OWN COST RUNG: the -5.4 pp/yr was measured at ZERO cost.")
    P("    Re-price the filter at 0 bps so the comparison is like for like.")
    P("=" * 112)
    z = []
    for pnm, (px, tr) in panels.items():
        st = ref[pnm]["start"]
        books = make_books(px, tr, PIN_G)
        rz = {k: run(px, w, PIN_FREQ, cost=0.0)["returns"].loc[st:] for k, w in books.items()}
        c = metrics(rz["EWall"])
        for k in ["MA-RS", "MA-DG", "MAVOL-RS", "MAVOL-DG"]:
            m = metrics(rz[k])
            z.append(dict(panel=pnm, arm=k, dCAGR0=m["CAGR"] - c["CAGR"],
                          dSharpe0=m["Sharpe"] - c["Sharpe"]))
    Z = pd.DataFrame(z)
    P(f"  g = {PIN_G}, cadence {PIN_FREQ}, 0 bps")
    P(f"  {'panel':9s} {'arm':9s} {'dCAGR@0bps':>11s} {'dSharpe@0bps':>13s}")
    for _, x in Z.iterrows():
        P(f"  {x.panel:9s} {x.arm:9s} {x.dCAGR0:+11.2%} {x.dSharpe0:+13.3f}")

    # ---------------------------------------------------------------- Q3 cap deciles
    P("\n" + "=" * 112)
    P("Q3  CAP DECILES INSIDE THE SMALL PANEL  (pre-registered single point g=0.75, weekly)")
    P("    capQ = STATIC 2026 mktcap (look-ahead CLASSIFIER, no return info).")
    P("    advQ = DYNAMIC trailing-60d median dollar volume, causal, membership varies.")
    P("=" * 112)
    pxs, str_ = panels[SMALL]
    cols = sorted(str_)
    st = ref[SMALL]["start"]; spy = ref[SMALL]["spy"]; spyo = spy.loc[OOS_START:]
    b2 = ref[SMALL]["v2"]

    cap = static_cap(cols)
    P(f"  capQ covers {len(cap)}/{len(cols)} tradable names "
      f"(median ${cap.median()/1e6:.0f}M, range ${cap.min()/1e6:.0f}M-${cap.max()/1e6:.0f}M)")
    dv = dyn_dollar_vol(pxs, cols)
    P(f"  advQ built from data/volume_small.csv on {dv.shape[1]} names; "
      f"panel-median 60d dollar volume ${dv.stack().median()/1e6:.2f}M")

    dec_rows = []
    e_all = _priced(pxs, str_) > 0
    ma_all = above_ma(pxs) & e_all

    # --- capQ: static membership
    q_static = pd.qcut(cap.rank(method="first"), NDEC, labels=False) + 1
    # --- advQ: dynamic cross-sectional decile each day
    rk = dv.rank(axis=1, pct=True)

    for scheme in ["capQ", "advQ"]:
        for d in range(1, NDEC + 1):
            if scheme == "capQ":
                names = list(q_static[q_static == d].index)
                memb = pd.DataFrame(False, index=pxs.index, columns=pxs.columns)
                memb[names] = True
                size_lbl = f"${cap[names].median()/1e6:.0f}M cap"
                nsz = len(names)
            else:
                lo, hi = (d - 1) / NDEC, d / NDEC
                memb = pd.DataFrame(False, index=pxs.index, columns=pxs.columns)
                sel = (rk > lo) & (rk <= hi) if d > 1 else (rk >= 0) & (rk <= hi)
                memb.loc[:, sel.columns] = sel.fillna(False).values
                size_lbl = f"${dv.where(sel).stack().median()/1e6:.2f}M adv"
                nsz = int(sel.sum(axis=1).mean())
            e = e_all & memb
            ma = ma_all & memb
            if e.sum(axis=1).loc[st:].min() < 1:
                pass  # empty rows go to cash by construction in _ew
            n_all_d = e.sum(axis=1).replace(0, np.nan)
            books = {"EWall": _ew(e, PIN_G),
                     "MA-RS": _ew(ma, PIN_G),
                     "MA-DG": (PIN_G * ma.astype(float)).div(n_all_d, axis=0).fillna(0.0)}
            rets = {k: run(pxs, w, PIN_FREQ)["returns"].loc[st:] for k, w in books.items()}
            rets0 = {k: run(pxs, w, PIN_FREQ, cost=0.0)["returns"].loc[st:]
                     for k, w in books.items()}
            c, c0 = metrics(rets["EWall"]), metrics(rets0["EWall"])
            for k in ["EWall", "MA-RS", "MA-DG"]:
                r = rets[k]
                row = dict(scheme=scheme, decile=d, n_names=nsz, size=size_lbl, arm=k)
                row.update(rowify(r))
                row["dCAGR_vs_EWall"] = row["CAGR"] - c["CAGR"]
                row["dSharpe_vs_EWall"] = row["Sharpe"] - c["Sharpe"]
                row["dCAGR0_vs_EWall"] = metrics(rets0[k])["CAGR"] - c0["CAGR"]
                row["keep4a"] = keep_4a(r, b2)
                row["keep4b"] = keep_4b(r, spy, r.loc[OOS_START:], spyo)
                dec_rows.append(row)
        P(f"  {scheme} done ({time.time()-t0:.0f}s)")
    D = pd.DataFrame(dec_rows)
    D.to_csv(OUT / f"{STAMP}.deciles.csv", index=False)

    for scheme in ["capQ", "advQ"]:
        P(f"\n  --- {scheme}: does the 200d filter's cost shrink as size rises?")
        P(f"  {'dec':>3s} {'size':>13s} {'n':>4s} {'EWall CAGR':>10s} {'EWall Sh':>8s} "
          f"{'MA-RS dCAGR':>11s} {'MA-RS dSh':>9s} {'MA-DG dCAGR':>11s} {'MA-DG dSh':>9s} "
          f"{'MA-RS dCAGR@0':>13s}")
        for d in range(1, NDEC + 1):
            s = D[(D.scheme == scheme) & (D.decile == d)].set_index("arm")
            P(f"  {d:3d} {s.loc['EWall','size']:>13s} {int(s.loc['EWall','n_names']):4d} "
              f"{s.loc['EWall','CAGR']:10.2%} {s.loc['EWall','Sharpe']:8.3f} "
              f"{s.loc['MA-RS','dCAGR_vs_EWall']:+11.2%} {s.loc['MA-RS','dSharpe_vs_EWall']:+9.3f} "
              f"{s.loc['MA-DG','dCAGR_vs_EWall']:+11.2%} {s.loc['MA-DG','dSharpe_vs_EWall']:+9.3f} "
              f"{s.loc['MA-RS','dCAGR0_vs_EWall']:+13.2%}")
        for arm in ["MA-RS", "MA-DG"]:
            s = D[(D.scheme == scheme) & (D.arm == arm)].sort_values("decile")
            rho = float(np.corrcoef(s.decile, s.dSharpe_vs_EWall)[0, 1])
            rhc = float(np.corrcoef(s.decile, s.dCAGR_vs_EWall)[0, 1])
            P(f"      {arm}: corr(decile, dSharpe) = {rho:+.3f}, corr(decile, dCAGR) = {rhc:+.3f}, "
              f"dSharpe>0 in {int((s.dSharpe_vs_EWall>0).sum())}/{NDEC} deciles")

    # ---------------------------------------------------------------- Q4 rule 8
    P("\n" + "=" * 112)
    P("Q4  RULE 8 WALK-FORWARD  ((g, cadence) chosen on IS 2010-2016 Sharpe inside each")
    P("    (panel, arm); the CONTROL re-selects on its own IS window too; 2017-2026 read once)")
    P("=" * 112)
    wf = []
    for pnm in panels:
        spy = ref[pnm]["spy"]; spyo = spy.loc[OOS_START:]
        b2o = ref[pnm]["v2"].loc[OOS_START:]
        ms, mb2 = metrics(spyo), metrics(b2o)
        for arm in ["EWall", "MA-RS", "MA-DG", "MAVOL-RS", "MAVOL-DG"]:
            s = G[(G.panel == pnm) & (G.arm == arm)]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            ctl = G[(G.panel == pnm) & (G.arm == "EWall")]
            cpick = ctl.loc[ctl.IS_Sharpe.idxmax()]
            wf.append(dict(panel=pnm, arm=arm, g=pick.gross, cadence=pick.cadence,
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           ctl_g=cpick.gross, ctl_cadence=cpick.cadence,
                           ctl_OOS_CAGR=cpick.OOS_CAGR, ctl_OOS_Sharpe=cpick.OOS_Sharpe,
                           dOOS_CAGR=pick.OOS_CAGR - cpick.OOS_CAGR,
                           dOOS_Sharpe=pick.OOS_Sharpe - cpick.OOS_Sharpe,
                           spy_OOS_Sharpe=ms["Sharpe"], spy_OOS_CAGR=ms["CAGR"],
                           spy_OOS_MaxDD=ms["MaxDD"],
                           v2_OOS_Sharpe=mb2["Sharpe"], v2_OOS_CAGR=mb2["CAGR"],
                           v2_OOS_MaxDD=mb2["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(f"  {'panel':9s} {'arm':9s} {'IS pick':>10s} {'OOS CAGR':>9s} {'OOS Sh':>7s} "
      f"{'OOS MaxDD':>10s} {'dOOS CAGR':>10s} {'dOOS Sh':>8s}")
    for _, x in W.iterrows():
        P(f"  {x.panel:9s} {x.arm:9s} {f'g{x.g:.2f}/{x.cadence}':>10s} {x.OOS_CAGR:9.2%} "
          f"{x.OOS_Sharpe:7.3f} {x.OOS_MaxDD:10.2%} {x.dOOS_CAGR:+10.2%} {x.dOOS_Sharpe:+8.3f}")
    for pnm in panels:
        x = W[W.panel == pnm].iloc[0]
        P(f"  {pnm:9s} OOS references: SPY {x.spy_OOS_CAGR:.2%}/{x.spy_OOS_Sharpe:.3f}/"
          f"{x.spy_OOS_MaxDD:.2%}   RULES v2 {x.v2_OOS_CAGR:.2%}/{x.v2_OOS_Sharpe:.3f}/"
          f"{x.v2_OOS_MaxDD:.2%}")

    # ---------------------------------------------------------------- Q5 gross is a scalar
    P("\n" + "=" * 112)
    P("Q5  IS THE KEEP-PATH VERDICT A GROSS-DIAL PLACEMENT?")
    P("    None of these books is levered: gross g is a scalar on an otherwise identical")
    P("    position vector, the remainder sits in cash at 0%.  So Sharpe should be INVARIANT")
    P("    in g while CAGR and MaxDD scale ~linearly.  If so, 4b's CAGR FLOOR and DD CAP are")
    P("    two LEVEL tests on the same dial and the verdict is decided by where the dial sits,")
    P("    not by the arm.  Measured, then the implied admissible g-band is solved and RUN.")
    P("=" * 112)
    sp = G.groupby(["panel", "arm", "cadence"]).Sharpe.agg(["min", "max"])
    sp["span"] = sp["max"] - sp["min"]
    P(f"  Sharpe span across g within each (panel, arm, cadence): max {sp.span.max():.4f}, "
      f"mean {sp.span.mean():.4f}  over {len(sp)} cells")
    pc = G.pivot_table(index=["panel", "arm", "cadence"], columns="gross", values="CAGR")
    pd_ = G.pivot_table(index=["panel", "arm", "cadence"], columns="gross", values="MaxDD")
    P(f"  CAGR  g1.00/g0.50 ratio: mean {(pc[1.0]/pc[0.5]).mean():.3f} "
      f"[{(pc[1.0]/pc[0.5]).min():.3f}, {(pc[1.0]/pc[0.5]).max():.3f}]  (2.000 = exact scalar)")
    P(f"  MaxDD g1.00/g0.50 ratio: mean {(pd_[1.0]/pd_[0.5]).mean():.3f} "
      f"[{(pd_[1.0]/pd_[0.5]).min():.3f}, {(pd_[1.0]/pd_[0.5]).max():.3f}]")

    P("\n  Solving the 4b level tests for g on the 0.75 anchor (linear scaling), then RUNNING")
    P("  the band midpoint so the verdict is measured, not extrapolated:")
    P(f"  {'panel':9s} {'arm':9s} {'cad':>4s} {'g_lo(CAGR)':>10s} {'g_hi(DD)':>9s} "
      f"{'band':>6s} {'g*':>5s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'OOS Sh':>7s} 4b")
    band_rows = []
    for pnm, (px, tr) in panels.items():
        st = ref[pnm]["start"]; spy = ref[pnm]["spy"]; spyo = spy.loc[OOS_START:]
        ms = metrics(spy)
        cagr_floor, dd_cap = 0.70 * ms["CAGR"], 0.60 * ms["MaxDD"]
        for arm in ["EWall", "MA-RS", "MA-DG", "MAVOL-RS", "MAVOL-DG"]:
            for freq in CADENCE:
                a = G[(G.panel == pnm) & (G.arm == arm) & (G.cadence == freq)
                      & (G.gross == 0.75)].iloc[0]
                g_lo = 0.75 * cagr_floor / a.CAGR if a.CAGR > 0 else np.inf
                g_hi = 0.75 * dd_cap / a.MaxDD
                ok = g_lo <= g_hi and g_lo > 0
                gstar = float(np.clip((g_lo + g_hi) / 2, 0.05, 2.0)) if ok else np.nan
                row = dict(panel=pnm, arm=arm, cadence=freq, g_lo=g_lo, g_hi=g_hi,
                           band_nonempty=bool(ok), gstar=gstar)
                if ok:
                    w = make_books(px, tr, gstar)[arm]
                    r = run(px, w, freq)["returns"].loc[st:]
                    m = metrics(r)
                    row.update(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                               OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                               keep4b=keep_4b(r, spy, r.loc[OOS_START:], spyo),
                               keep4a=keep_4a(r, ref[pnm]["v2"]))
                    P(f"  {pnm:9s} {arm:9s} {freq:>4s} {g_lo:10.3f} {g_hi:9.3f} "
                      f"{'yes':>6s} {gstar:5.2f} {m['CAGR']:8.2%} {m['Sharpe']:7.3f} "
                      f"{m['MaxDD']:8.2%} {row['OOS_Sharpe']:7.3f} "
                      f"{'Y' if row['keep4b'] else '.':>2s}")
                else:
                    row.update(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, OOS_Sharpe=np.nan,
                               keep4b=False, keep4a=False)
                    P(f"  {pnm:9s} {arm:9s} {freq:>4s} {g_lo:10.3f} {g_hi:9.3f} "
                      f"{'EMPTY':>6s} {'-':>5s} {'-':>8s} {'-':>7s} {'-':>8s} {'-':>7s}  .")
                band_rows.append(row)
    B = pd.DataFrame(band_rows)
    B.to_csv(OUT / f"{STAMP}.grossband.csv", index=False)
    P(f"\n  Band non-empty in {int(B.band_nonempty.sum())}/{len(B)} book-forms; of those, 4b "
      f"passes at the solved g* in {int(B.keep4b.sum())}.  On the fixed 3-point ladder the same "
      f"forms produced {int(G.keep4b.sum())}/{len(G)} passes.")
    for pnm in panels:
        s = B[B.panel == pnm]
        P(f"    {pnm:9s} band non-empty {int(s.band_nonempty.sum())}/{len(s)}, "
          f"4b at g* {int(s.keep4b.sum())}/{len(s)}")

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 112)
    P("VERDICT")
    P("=" * 112)
    n4a = int(G.keep4a.sum()); n4b = int(G.keep4b.sum())
    P(f"  4a passes {n4a}/{len(G)} of the panel grid; 4b passes {n4b}/{len(G)}.")
    P(f"  Decile grid: 4a {int(D.keep4a.sum())}/{len(D)}, 4b {int(D.keep4b.sum())}/{len(D)}.")
    if n4b:
        P("  4b passers:")
        for _, x in G[G.keep4b].iterrows():
            P(f"    {x.panel}/{x.arm}/g{x.gross:.2f}/{x.cadence}  CAGR {x.CAGR:.2%} "
              f"Sharpe {x.Sharpe:.3f} MaxDD {x.MaxDD:.2%} OOS Sharpe {x.OOS_Sharpe:.3f}")
    if n4a:
        P("  4a passers:")
        for _, x in G[G.keep4a].iterrows():
            P(f"    {x.panel}/{x.arm}/g{x.gross:.2f}/{x.cadence}  Sharpe {x.Sharpe:.3f} "
              f"(H1 {x.H1:.3f}/H2 {x.H2:.3f}) MaxDD {x.MaxDD:.2%}")
    P(f"\n  runtime {time.time()-t0:.0f}s")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    TAB.to_csv(OUT / f"{STAMP}.summary.csv", index=False)
    Z.to_csv(OUT / f"{STAMP}.zerocost.csv", index=False)
    return G, D, W, TAB, Z, B


if __name__ == "__main__":
    main()

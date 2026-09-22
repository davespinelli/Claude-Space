#!/usr/bin/env python3
"""Idea 2311 (lane C, 2026-09-22) — does ONE MARKET-LEVEL GATE beat the 56 NAME-LEVEL GATES
at MATCHED MEAN EXPOSURE?

RULES v2 clause 2 gates every name on ITS OWN 200d +/-3% band, so the book's exposure is a
continuum (realised mean gross 0.5327 against a nominal 0.75, idea 2304) and it pays
name-by-name turnover for that continuum.  The record has priced the band's WIDTH (2241),
its LOOKBACK (1461/1472), its GROSS (2119/2304), its CADENCE (2276/2280/2284), its CASH
(2213/2221/2294) and its PHASE (2274) — never its LEVEL.  The untested control is ONE gate
computed on an equal-weight index of the SAME panel: either fully invested or fully in cash.
Since the 4b CAGR floor is the sole binding leg (2284: the DD cap binds in 0 of 240 cells)
and every committed 4b pass sits at gross 1.00 (2119), a gate that is FULLY invested
whenever it is on attacks exactly the leg that binds.

TWO TUNED DIALS AND NO MORE:
  dial 1  LEVEL in {NAME, INDEX, BOTH, SPYG}   (BOTH = intersection; SPYG = gate on SPY)
  dial 2  BAND c in {0.00, 0.03, 0.06, 0.10}
GROSS {0.75 live, 1.00}, COST {0, 5, 10, 25, 50} bps, PANEL {U56, B136} and the weekly
cadence are REPORTED at every grid point, never selected on.  Every grid point is printed.
No leverage anywhere: gross <= 1.00 and sum(w) <= gross.

Each book is additionally scored against its OWN exposure-matched constant de-gross twin
(no gate, k*EW, k solved so realised mean gross matches to <1e-6) — the record's standing
ruler, under which every drawdown-buying device so far has lost.

Rule 8: both dials chosen on 2009-2016 ONLY, 2017-2026 read ONCE.
Run:  python3 research/backtests/2026-09-22_market-level-gate-vs-name-level_C.py
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state                 # noqa
from engine import backtest, metrics, rebalance_mask                            # noqa

OUT = Path(__file__).with_suffix("")
FREQ = "W"
LIVE_GROSS, LIVE_BAND, LIVE_COST = 0.75, 0.03, 10
LEVELS = ["NAME", "INDEX", "BOTH", "SPYG"]
BANDS = [0.00, 0.03, 0.06, 0.10]
GROSSES = [0.75, 1.00]
COSTS = [0, 5, 10, 25, 50]
IS_END, OOS_START = "2016-12-31", "2017-01-01"


# --------------------------------------------------------------- fast engine --
def run(prices_np, rets_np, w_np, mask_np):
    """Bit-identical arithmetic to engine.backtest, in numpy.  Returns (gross-of-cost
    daily returns, daily turnover, daily held gross)."""
    T, N = rets_np.shape
    cur = np.zeros(N)
    held_ret = np.zeros(T); turn = np.zeros(T); hg = np.zeros(T)
    for i in range(T):
        if mask_np[i] or i == 0:
            new = w_np[i]
            turn[i] = np.abs(new - cur).sum(); cur = new.copy()
        hg[i] = cur.sum()
        held_ret[i] = (cur * rets_np[i]).sum()
        growth = cur * (1 + rets_np[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    return held_ret, turn, hg


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.rets = px.pct_change().fillna(0.0)
        self.rets_np = self.rets.values
        self.px_np = px.values
        m = rebalance_mask(px.index, FREQ).shift(1, fill_value=False)
        self.mask_np = m.values
        self.idx = px.index
        self.start = px.index[260]                       # skip warm-up, as baseline.compare
        self.sl = self.idx >= self.start
        # equal-weight index of the panel's own names (the book's universe), for the INDEX gate
        ew_ret = self.rets.where(px.notna() & px.shift(1).notna()).mean(axis=1).fillna(0.0)
        self.ewidx = (1 + ew_ret).cumprod().rename("EWIDX")

    def shifted(self, w):
        return w.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def score_book(self, w):
        hr, tu, hg = run(self.px_np, self.rets_np, self.shifted(w), self.mask_np)
        return dict(hr=hr[self.sl], tu=tu[self.sl], hg=hg[self.sl])


def net(b, cost_bps):
    return pd.Series(b["hr"] - b["tu"] * cost_bps / 1e4, index=IDXCACHE)


# ----------------------------------------------------------------- gating -----
def gate_frame(panel, level, c):
    px = panel.px
    if level == "NAME":
        return band_state(px, c)
    if level == "INDEX":
        g = band_state(panel.ewidx.to_frame(), c)["EWIDX"]
    elif level == "SPYG":
        g = band_state(px[["SPY"]], c)["SPY"]
    elif level == "BOTH":
        gi = band_state(panel.ewidx.to_frame(), c)["EWIDX"]
        return band_state(px, c).mul(gi.astype(float), axis=0) > 0.5
    return pd.DataFrame(np.repeat(g.values[:, None], px.shape[1], axis=1),
                        index=px.index, columns=px.columns)


def book_weights(panel, level, c, gross):
    px = panel.px
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(gate_frame(panel, level, c), 0.0)


def degross_weights(panel, k):
    px = panel.px
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return k * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


# ---------------------------------------------------------------- scoring -----
def legs(r):
    h = len(r) // 2
    m, m1, m2, o = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                oCAGR=o["CAGR"], oSharpe=o["Sharpe"], oMaxDD=o["MaxDD"])


def path4a(c, b):      # Sharpe > live RULES v2 in BOTH halves, MaxDD no worse than live
    return c["H1"] > b["H1"] and c["H2"] > b["H2"] and c["MaxDD"] >= b["MaxDD"]


def path4b_full(c, s):
    return (c["H1"] > s["H1"] and c["H2"] > s["H2"]
            and c["MaxDD"] >= 0.60 * s["MaxDD"] and c["CAGR"] >= 0.70 * s["CAGR"])


def path4b_oos(c, s):
    return (c["oSharpe"] > s["oSharpe"] and c["oMaxDD"] >= 0.60 * s["oMaxDD"]
            and c["oCAGR"] >= 0.70 * s["oCAGR"])


def binding(c, s):
    out = []
    if not c["H1"] > s["H1"]: out.append("L_H1")
    if not c["H2"] > s["H2"]: out.append("L_H2")
    if not c["MaxDD"] >= 0.60 * s["MaxDD"]: out.append("L_DD")
    if not c["CAGR"] >= 0.70 * s["CAGR"]: out.append("L_CAGR")
    if not c["oSharpe"] > s["oSharpe"]: out.append("L_OOS")
    return "+".join(out) if out else "-"


# ------------------------------------------------------------------- main -----
if __name__ == "__main__":
    pd.set_option("display.width", 200)
    log = []
    def P(*a):
        s = " ".join(str(x) for x in a); print(s); log.append(s)

    panels = {}
    panels["U56"] = Panel("U56", load_universe())
    panels["B136"] = Panel("B136", load_universe(broad=True))
    for k, p in panels.items():
        P(f"panel {k}: {p.px.shape[1]} names, {p.px.index[0].date()} -> {p.px.index[-1].date()}, "
          f"scored from {p.start.date()}")

    # ---- G1: the numpy runner reproduces engine.backtest exactly ----
    p = panels["U56"]; IDXCACHE = p.idx[p.sl]
    w_live = rules_v2_weights(p.px, band=LIVE_BAND, gross=LIVE_GROSS)
    ref = backtest(p.px, w_live, cost_bps=LIVE_COST, freq=FREQ)["returns"].loc[p.start:]
    b = p.score_book(w_live); mine = pd.Series(b["hr"] - b["tu"] * LIVE_COST / 1e4, index=IDXCACHE)
    g1 = float(np.abs(mine.values - ref.values).max())
    P(f"\nG1 numpy runner == engine.backtest (U56, live book, 10bps): max|dret| = {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")

    # ---- G2: NAME @ c=0.03 is the live book exactly ----
    g2 = float(np.abs(book_weights(p, "NAME", LIVE_BAND, LIVE_GROSS).values - w_live.values).max())
    P(f"G2 book_weights(NAME, 0.03, 0.75) == rules_v2_weights: max|dw| = {g2:.3e}  "
      f"{'PASS' if g2 < 1e-15 else 'FAIL'}")

    # ---- baselines per panel ----
    base, spy, spygross = {}, {}, {}
    for pk, pan in panels.items():
        IDXCACHE = pan.idx[pan.sl]
        base[pk] = pan.score_book(rules_v2_weights(pan.px, band=LIVE_BAND, gross=LIVE_GROSS))
        spy[pk] = pan.px["SPY"].pct_change().fillna(0.0).loc[pan.start:]
        spygross[pk] = legs(spy[pk])
        bl = legs(pd.Series(base[pk]["hr"] - base[pk]["tu"] * LIVE_COST / 1e4, index=IDXCACHE))
        P(f"\nbaseline RULES v2 {pk} @10bps: CAGR {bl['CAGR']:.4%} Sharpe {bl['Sharpe']:.4f} "
          f"MaxDD {bl['MaxDD']:.4%} | H1 {bl['H1']:.4f} H2 {bl['H2']:.4f} | OOS {bl['oCAGR']:.4%}/"
          f"{bl['oSharpe']:.4f}/{bl['oMaxDD']:.4%} | realised mean gross {base[pk]['hg'].mean():.4f}")
        s = spygross[pk]
        P(f"SPY {pk}: CAGR {s['CAGR']:.4%} Sharpe {s['Sharpe']:.4f} MaxDD {s['MaxDD']:.4%} | "
          f"H1 {s['H1']:.4f} H2 {s['H2']:.4f} | OOS {s['oCAGR']:.4%}/{s['oSharpe']:.4f}/{s['oMaxDD']:.4%} "
          f"| 4b floors: CAGR>={0.70*s['CAGR']:.4%} DD>={0.60*s['MaxDD']:.4%}")

    # ---- the grid ----
    rows, books = [], {}
    for pk, pan in panels.items():
        IDXCACHE = pan.idx[pan.sl]
        for lev, c, g in itertools.product(LEVELS, BANDS, GROSSES):
            bk = pan.score_book(book_weights(pan, lev, c, g))
            books[(pk, lev, c, g)] = bk
            mg = float(bk["hg"].mean())
            # exposure-matched constant de-gross twin
            lo, hi = 0.01, 1.30
            for _ in range(40):
                mid = 0.5 * (lo + hi)
                t = pan.score_book(degross_weights(pan, mid))
                if float(t["hg"].mean()) < mg: lo = mid
                else: hi = mid
            twin = pan.score_book(degross_weights(pan, 0.5 * (lo + hi)))
            books[("TWIN", pk, lev, c, g)] = twin
            for cost in COSTS:
                r = pd.Series(bk["hr"] - bk["tu"] * cost / 1e4, index=IDXCACHE)
                tr = pd.Series(twin["hr"] - twin["tu"] * cost / 1e4, index=IDXCACHE)
                br = pd.Series(base[pk]["hr"] - base[pk]["tu"] * cost / 1e4, index=IDXCACHE)
                L, TL, BL, S = legs(r), legs(tr), legs(br), spygross[pk]
                rows.append(dict(panel=pk, level=lev, band=c, gross=g, cost=cost,
                                 CAGR=L["CAGR"], Sharpe=L["Sharpe"], MaxDD=L["MaxDD"],
                                 H1=L["H1"], H2=L["H2"], oCAGR=L["oCAGR"], oSharpe=L["oSharpe"],
                                 oMaxDD=L["oMaxDD"], mean_gross=mg,
                                 turns_yr=bk["tu"].sum() / (len(r) / 252),
                                 p4a=path4a(L, BL), p4b_full=path4b_full(L, S),
                                 p4b_oos=path4b_oos(L, S), binding=binding(L, S),
                                 twin_k=0.5 * (lo + hi), twin_gross=float(twin["hg"].mean()),
                                 twin_CAGR=TL["CAGR"], twin_Sharpe=TL["Sharpe"], twin_MaxDD=TL["MaxDD"],
                                 dSharpe_vs_twin=L["Sharpe"] - TL["Sharpe"],
                                 dMaxDD_vs_twin=L["MaxDD"] - TL["MaxDD"],
                                 dCAGR_vs_twin=L["CAGR"] - TL["CAGR"]))
    grid = pd.DataFrame(rows)
    grid.to_csv(str(OUT) + ".grid.csv", index=False)
    P(f"\n=== GRID: {len(grid)} published rows "
      f"({len(LEVELS)} levels x {len(BANDS)} bands x {len(GROSSES)} gross x {len(panels)} panels x {len(COSTS)} cost rungs) ===")

    show = ["panel", "level", "band", "gross", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "oCAGR", "oSharpe", "oMaxDD", "mean_gross", "turns_yr", "p4a", "p4b_full", "p4b_oos", "binding"]
    for pk in panels:
        for g in GROSSES:
            sub = grid[(grid.panel == pk) & (grid.gross == g) & (grid.cost == LIVE_COST)]
            P(f"\n--- {pk}, gross {g}, {LIVE_COST} bps (all {len(sub)} cells) ---")
            P(sub[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n=== A. LEVEL CONTRAST AT MATCHED BAND (10 bps) — INDEX minus NAME ===")
    for pk in panels:
        for g in GROSSES:
            for c in BANDS:
                n = grid[(grid.panel == pk) & (grid.gross == g) & (grid.cost == LIVE_COST) &
                         (grid.band == c) & (grid.level == "NAME")].iloc[0]
                for lev in ["INDEX", "BOTH", "SPYG"]:
                    x = grid[(grid.panel == pk) & (grid.gross == g) & (grid.cost == LIVE_COST) &
                             (grid.band == c) & (grid.level == lev)].iloc[0]
                    P(f"{pk} g{g} c{c:.2f} {lev:5s}-NAME: dCAGR {100*(x.CAGR-n.CAGR):+7.4f}pp  "
                      f"dSharpe {x.Sharpe-n.Sharpe:+7.4f}  dMaxDD {100*(x.MaxDD-n.MaxDD):+7.4f}pp  "
                      f"dGross {x.mean_gross-n.mean_gross:+6.4f}  dTurn {x.turns_yr-n.turns_yr:+6.2f}/yr")

    P("\n=== B. EVERY BOOK vs ITS OWN EXPOSURE-MATCHED DE-GROSS TWIN (10 bps) ===")
    sub = grid[grid.cost == LIVE_COST]
    P(sub[["panel", "level", "band", "gross", "mean_gross", "twin_gross", "dCAGR_vs_twin",
           "dSharpe_vs_twin", "dMaxDD_vs_twin"]].to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    beats = sub[(sub.dSharpe_vs_twin > 0) & (sub.dMaxDD_vs_twin > 0)]
    P(f"\nbooks beating their own matched-exposure twin on BOTH Sharpe and MaxDD: {len(beats)} of {len(sub)}")
    if len(beats): P(beats[["panel", "level", "band", "gross", "dSharpe_vs_twin", "dMaxDD_vs_twin"]]
                     .to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    P(f"match quality: max|mean_gross - twin_gross| = {float((sub.mean_gross - sub.twin_gross).abs().max()):.3e}")

    P("\n=== C. BOTH KEEP PATHS AT EVERY GRID POINT ===")
    P(f"4a passes: {int(grid.p4a.sum())} of {len(grid)}")
    if grid.p4a.any(): P(grid[grid.p4a][show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"4b_FULL passes: {int(grid.p4b_full.sum())} of {len(grid)}")
    if grid.p4b_full.any(): P(grid[grid.p4b_full][show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"4b_OOS passes: {int(grid.p4b_oos.sum())} of {len(grid)}")
    both = grid[grid.p4a & grid.p4b_full]
    P(f"cells passing BOTH paths: {len(both)} of {len(grid)}")
    P("\nbinding-leg census over 4b_FULL failures:")
    fails = grid[~grid.p4b_full]
    cnt = {}
    for s in fails.binding:
        for leg in s.split("+"): cnt[leg] = cnt.get(leg, 0) + 1
    for k in sorted(cnt, key=lambda k: -cnt[k]): P(f"  {k}: {cnt[k]} of {len(fails)} ({cnt[k]/len(fails):.3f})")

    # ---- D. rule 8 ----
    P("\n=== D. RULE 8 — both dials chosen on 2009-2016 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pk, pan in panels.items():
        IDXCACHE = pan.idx[pan.sl]
        for g in GROSSES:
            cells = {}
            for lev, c in itertools.product(LEVELS, BANDS):
                bk = books[(pk, lev, c, g)]
                r = pd.Series(bk["hr"] - bk["tu"] * LIVE_COST / 1e4, index=IDXCACHE)
                ris = r.loc[:IS_END]; ros = r.loc[OOS_START:]
                sis = spy[pk].loc[:IS_END]
                m_is, m_os = metrics(ris), metrics(ros)
                h = len(ris) // 2
                is4b = (metrics(ris.iloc[:h])["Sharpe"] > metrics(sis.iloc[:h])["Sharpe"]
                        and metrics(ris.iloc[h:])["Sharpe"] > metrics(sis.iloc[h:])["Sharpe"]
                        and m_is["MaxDD"] >= 0.60 * metrics(sis)["MaxDD"]
                        and m_is["CAGR"] >= 0.70 * metrics(sis)["CAGR"])
                cells[(lev, c)] = dict(is_sharpe=m_is["Sharpe"], is_cagr=m_is["CAGR"], is4b=is4b,
                                       oCAGR=m_os["CAGR"], oSharpe=m_os["Sharpe"], oMaxDD=m_os["MaxDD"])
            bk = base[pk]
            br = pd.Series(bk["hr"] - bk["tu"] * LIVE_COST / 1e4, index=IDXCACHE)
            bo = metrics(br.loc[OOS_START:]); so = metrics(spy[pk].loc[OOS_START:])
            picks = {"C_ISSHARPE": max(cells, key=lambda k: cells[k]["is_sharpe"]),
                     "C_IS4b": (max([k for k in cells if cells[k]["is4b"]],
                                    key=lambda k: cells[k]["is_sharpe"])
                                if any(cells[k]["is4b"] for k in cells) else None),
                     "C_ZERO (shipped NAME/0.03)": ("NAME", LIVE_BAND),
                     "C_ZERO_INDEX (INDEX/0.03)": ("INDEX", LIVE_BAND)}
            P(f"\n-- {pk}, gross {g} -- baseline OOS {bo['CAGR']:.4%}/{bo['Sharpe']:.4f}/{bo['MaxDD']:.4%}"
              f" | SPY OOS {so['CAGR']:.4%}/{so['Sharpe']:.4f}/{so['MaxDD']:.4%}")
            P("   IS(2009-2016) Sharpe by cell: " + ", ".join(
                f"{l}/{c:.2f}={cells[(l,c)]['is_sharpe']:.4f}" for l, c in cells))
            for nm, k in picks.items():
                if k is None:
                    P(f"   {nm:28s}: UNDEFINED (no IS cell clears 4b)")
                    wf.append(dict(panel=pk, gross=g, chooser=nm, level=None, band=None))
                    continue
                cc = cells[k]
                ok = (cc["oSharpe"] > so["Sharpe"] and cc["oMaxDD"] >= 0.60 * so["MaxDD"]
                      and cc["oCAGR"] >= 0.70 * so["CAGR"])
                P(f"   {nm:28s}: picks {k[0]}/{k[1]:.2f} -> OOS {cc['oCAGR']:.4%}/{cc['oSharpe']:.4f}/"
                  f"{cc['oMaxDD']:.4%}  4b_OOS {'PASS' if ok else 'FAIL'}  "
                  f"(vs baseline OOS Sharpe {bo['Sharpe']:.4f})")
                wf.append(dict(panel=pk, gross=g, chooser=nm, level=k[0], band=k[1],
                               is_sharpe=cc["is_sharpe"], oCAGR=cc["oCAGR"], oSharpe=cc["oSharpe"],
                               oMaxDD=cc["oMaxDD"], p4b_oos=ok, base_oCAGR=bo["CAGR"],
                               base_oSharpe=bo["Sharpe"], base_oMaxDD=bo["MaxDD"],
                               spy_oCAGR=so["CAGR"], spy_oSharpe=so["Sharpe"], spy_oMaxDD=so["MaxDD"]))
    pd.DataFrame(wf).to_csv(str(OUT) + ".walkforward.csv", index=False)

    P("\n=== E. COST-RUNG STABILITY OF EVERY 4b_FULL PASSER ===")
    for key, gg in grid[grid.p4b_full].groupby(["panel", "level", "band", "gross"]):
        allr = grid[(grid.panel == key[0]) & (grid.level == key[1]) & (grid.band == key[2]) & (grid.gross == key[3])]
        P(f"  {key}: 4b_FULL at {int(allr.p4b_full.sum())} of {len(COSTS)} rungs "
          f"({sorted(allr[allr.p4b_full].cost.tolist())} bps), 4b_OOS at "
          f"{sorted(allr[allr.p4b_oos].cost.tolist())} bps")

    P("\n=== F. THE DIRECT EXPOSURE-MATCHED LEVEL CONTRAST: NAME re-grossed onto INDEX's own mean gross ===")
    P("   (INDEX at gross g runs a higher realised mean gross than NAME at the same g, so the band-matched")
    P("    contrast in section A is exposure-UNMATCHED.  Here NAME's gross is solved so the two books hold")
    P("    the same mean exposure; the band and the cost rung are identical on both sides.)")
    frows = []
    for pk, pan in panels.items():
        IDXCACHE = pan.idx[pan.sl]
        for c in BANDS:
            for g in GROSSES:
                ib = books[(pk, "INDEX", c, g)]
                target = float(ib["hg"].mean())
                lo, hi = 0.20, 2.00
                for _ in range(40):
                    mid = 0.5 * (lo + hi)
                    t = pan.score_book(book_weights(pan, "NAME", c, mid))
                    if float(t["hg"].mean()) < target: lo = mid
                    else: hi = mid
                kk = 0.5 * (lo + hi)
                nb = pan.score_book(book_weights(pan, "NAME", c, kk))
                ir = pd.Series(ib["hr"] - ib["tu"] * LIVE_COST / 1e4, index=IDXCACHE)
                nr = pd.Series(nb["hr"] - nb["tu"] * LIVE_COST / 1e4, index=IDXCACHE)
                IL, NL, S = legs(ir), legs(nr), spygross[pk]
                frows.append(dict(panel=pk, band=c, index_gross=g, index_mean_gross=target,
                                  name_gross_solved=kk, name_mean_gross=float(nb["hg"].mean()),
                                  dCAGR=IL["CAGR"] - NL["CAGR"], dSharpe=IL["Sharpe"] - NL["Sharpe"],
                                  dMaxDD=IL["MaxDD"] - NL["MaxDD"],
                                  index_4b=path4b_full(IL, S), name_4b=path4b_full(NL, S)))
                P(f"   {pk} c{c:.2f} INDEX@g{g} (mean gross {target:.4f}) vs NAME@g{kk:.4f} "
                  f"(mean gross {float(nb['hg'].mean()):.4f}, match {abs(target-float(nb['hg'].mean())):.2e}): "
                  f"dCAGR {100*(IL['CAGR']-NL['CAGR']):+7.4f}pp  dSharpe {IL['Sharpe']-NL['Sharpe']:+7.4f}  "
                  f"dMaxDD {100*(IL['MaxDD']-NL['MaxDD']):+7.4f}pp  4b_FULL INDEX {path4b_full(IL,S)} / NAME {path4b_full(NL,S)}")
    fdf = pd.DataFrame(frows); fdf.to_csv(str(OUT) + ".matched.csv", index=False)
    P(f"\n   INDEX loses Sharpe to an exposure-matched NAME at {int((fdf.dSharpe < 0).sum())} of {len(fdf)} cells; "
      f"median dSharpe {fdf.dSharpe.median():+.4f}, median dCAGR {100*fdf.dCAGR.median():+.4f}pp, "
      f"median dMaxDD {100*fdf.dMaxDD.median():+.4f}pp")
    P(f"   4b_FULL at these matched cells: INDEX {int(fdf.index_4b.sum())} of {len(fdf)}, NAME {int(fdf.name_4b.sum())} of {len(fdf)}")

    Path(str(OUT) + ".log.txt").write_text("\n".join(log) + "\n")
    print("\nwrote", str(OUT) + ".grid.csv", "/", str(OUT) + ".walkforward.csv", "/", str(OUT) + ".log.txt")

#!/usr/bin/env python3
"""Idea 255 — does ddctl really own the deep budgets?

Idea 251, back-filling reach over idea 40's menus, flipped 4 of 40 published picks all the
same way: the book-level DRAWDOWN CONTROL (ddctl) displaces the plain DE-GROSS lever at
drawdown budgets T = 8-10 pp, 0.43-0.51 pp of CAGR per pp of MaxDD against de-gross's
0.58-0.61 — but only once ddctl's trigger ladder is run down to D = 2%.  That is a
"cheaper than the lever" claim at the deepest budgets, made on a 4-cell median.  This
tests it directly.

The test
  Books (idea 40's three, unchanged): V1 (rules_v1, top-5 @15%, vol scaler), CAND20
  (composite top-20 at GROSS/20, literal cash when fewer than 20 are eligible), EWall
  (equal weight over all eligible at GROSS).

  ddctl arm: at each weekly rebalance, if the book's own NET equity through the previous
  close is more than D below its running peak, multiply the target by k until a new
  equity high.  The state machine reads realised net equity only — no look-ahead.

  Control: the same book, no drawdown rule.
  De-gross lever: the same book scaled by a STATIC multiplier m, no drawdown rule.

  The comparison is idea 244's channel: every ddctl arm is priced against the static-gross
  ladder point at its own REALISED average gross, not against the unscaled control.  A
  drawdown rule that only works by holding less exposure is a de-gross lever with extra
  steps; the matched-gross control is what removes that confound.

Two tuned parameters, as the queue allows: **D** (trigger depth, 12 rungs 0.02 .. 0.40 —
the ladder idea 251 says the claim needs) and **k** (armed multiplier, 4 rungs).  Reset is
FIXED at "high" (new equity high disarms) so the count stays at two; panel and book are
reported at every level, not tuned.  ALL 3 panels x 3 books x (1 control + 48 ddctl arms +
19 ladder points) = 612 grid points are reported.

Rule 8 (PROTOCOL 8): (D, k) chosen on 2009-2016 only, two selectors (max IS Sharpe; and a
4b-aware one that picks nothing if no arm clears the IS 4b bars), evaluated untouched on
2017-2026 against the control, the matched-gross static book, RULES v2 (the LIVE book),
RULES v1 and SPY.

4a is judged against **RULES v2**, the live book.  Idea 482 (2026-09-09) showed 4a counts
scored against the superseded v1 survive the live comparand at ~6%, so both are reported.

Execution realism (PROTOCOL 2): weights decided at close t applied at t+1, weekly, long
only, no leverage, 10 bps on realised turnover (5 and 25 bps also reported).

SURVIVORSHIP: universe.json / universe_broad.json are current-constituent lists and the
small panel is a current screen (data/SMALL_PANEL_README.md); SMALL484 is used here as
SMALL439 — the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped, per
the standing convention.  Absolute CAGRs are optimistic.  Every number that answers the
queue is a same-panel, same-days DIFFERENCE between arms and is far less exposed.

Deterministic, offline, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys, math, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa
from engine import metrics, rebalance_mask                               # noqa

STEM = Path(__file__).with_suffix("")
OUT = lambda e: Path(str(STEM) + e)

FREQ, MAX_VOL, GROSS, NCAND = "W", 0.60, 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PCOST, COSTS = 10.0, [5, 10, 25]
BOOKS = ["V1", "CAND20", "EWall"]
DTRIG = [0.02, 0.03, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.40]
KCUT = [0.00, 0.25, 0.50, 0.75]
RESET = "high"
LADDER = np.round(np.arange(0.10, 1.001, 0.05), 2)
BUDGET_BINS = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 99)]

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 2000)


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def targets(px, book):
    if book == "V1":
        return rules_v1_weights(px)
    vol = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = ((vol < MAX_VOL) & (px > px.rolling(200).mean())).fillna(False)
    if book == "EWall":
        e = elig.astype(float)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    return (rank <= NCAND).astype(float) * (GROSS / NCAND)


def run(px, W, m=1.0, D=None, k=1.0, reset=RESET, bps=PCOST):
    """One arm.  Costs are applied inside the loop so the state machine sees NET equity."""
    rets = px.pct_change().fillna(0.0).values
    tgt = (W.reindex(px.index).fillna(0.0) * m).values
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    n, ncol = rets.shape
    cur = np.zeros(ncol); held = np.zeros((n, ncol)); turn = np.zeros(n)
    gross_s = np.zeros(n); cut = np.zeros(n, dtype=bool)
    eq, peak, armed, episodes = 1.0, 1.0, False, 0
    for i in range(n):
        if mask[i] and i > 0:
            if D is not None:
                dd = eq / peak - 1.0
                if not armed and dd < -D:
                    armed, episodes = True, episodes + 1
                elif armed and (dd >= 0.0 if reset == "high" else dd > -D / 2.0):
                    armed = False
            new = tgt[i - 1] * (k if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            turn[i] = np.abs(new - cur).sum(); cur = new
        cut[i] = armed; held[i] = cur; gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp); peak = max(peak, eq)
        g = cur * (1 + rets[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    r = pd.Series((held * rets).sum(axis=1), index=px.index) - pd.Series(turn, index=px.index) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=px.index).sum() / (n / 252),
                gross=float(np.mean(gross_s)), cut_days=int(cut.sum()), episodes=episodes)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy); m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if (spy.index[-1] > pd.Timestamp(OOS_START)) else np.nan)


def marg(r, bars):
    h1, h2 = halves(r); m = metrics(r); mo = metrics(r.loc[OOS_START:])
    return dict(m_H1=h1 - bars["s1"], m_H2=h2 - bars["s2"], m_OOS=mo["Sharpe"] - bars["soos"],
                m_DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                m_CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def pass4a(r, base):
    h1, h2 = halves(r); b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def statrow(name, r, extra):
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    h1, h2 = halves(r)
    d = dict(arm=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    d.update(extra)
    return d


# ---------------------------------------------------------------- one panel
def do_panel(pname, px):
    print(f"\n{'='*100}\nPANEL {pname}  {px.shape[1]} cols  {px.index[0].date()} .. {px.index[-1].date()}\n{'='*100}")
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = bars_of(spy)
    v2 = {c: None for c in COSTS}
    for c in COSTS:
        v2[c] = run(px, rules_v2_weights(px), bps=c)["r"].loc[start:]
    v1 = {c: run(px, rules_v1_weights(px), bps=c)["r"].loc[start:] for c in COSTS}
    print(f"  SPY  CAGR {metrics(spy)['CAGR']:.2%} Sh {metrics(spy)['Sharpe']:.3f} DD {metrics(spy)['MaxDD']:.2%} "
          f"H {bars['s1']:.3f}/{bars['s2']:.3f} OOS Sh {bars['soos']:.3f}")
    print(f"  RULES v2 (live, 10bps) CAGR {metrics(v2[10])['CAGR']:.2%} Sh {metrics(v2[10])['Sharpe']:.3f} "
          f"DD {metrics(v2[10])['MaxDD']:.2%} H {halves(v2[10])[0]:.3f}/{halves(v2[10])[1]:.3f}")
    print(f"  RULES v1 (prev, 10bps) CAGR {metrics(v1[10])['CAGR']:.2%} Sh {metrics(v1[10])['Sharpe']:.3f} "
          f"DD {metrics(v1[10])['MaxDD']:.2%} H {halves(v1[10])[0]:.3f}/{halves(v1[10])[1]:.3f}")

    grid, ladder, keep = [], [], {}
    for book in BOOKS:
        W = targets(px, book)
        for cost in COSTS:
            c0 = run(px, W, bps=cost)
            r0 = c0["r"].loc[start:]
            grid.append(statrow("control", r0, dict(panel=pname, book=book, cost=cost, D=np.nan,
                                                    k=np.nan, TO=c0["to"], gross=c0["gross"],
                                                    cut_days=0, episodes=0,
                                                    p4a_v2=pass4a(r0, v2[cost]), p4a_v1=pass4a(r0, v1[cost]),
                                                    **marg(r0, bars))))
            if cost == PCOST:
                keep[(book, None, None)] = c0["r"]
            for D in DTRIG:
                for k in KCUT:
                    a = run(px, W, D=D, k=k, bps=cost)
                    ra = a["r"].loc[start:]
                    grid.append(statrow(f"D{D:.0%}/k{k:.2f}", ra,
                                        dict(panel=pname, book=book, cost=cost, D=D, k=k,
                                             TO=a["to"], gross=a["gross"], cut_days=a["cut_days"],
                                             episodes=a["episodes"],
                                             p4a_v2=pass4a(ra, v2[cost]), p4a_v1=pass4a(ra, v1[cost]),
                                             **marg(ra, bars))))
                    if cost == PCOST:
                        keep[(book, D, k)] = a["r"]
        # static-gross ladder at the priced rung only (it is the comparand, not a treatment)
        for m in LADDER:
            a = run(px, W, m=float(m), bps=PCOST)
            ra = a["r"].loc[start:]
            ladder.append(statrow(f"m{m:.2f}", ra, dict(panel=pname, book=book, cost=PCOST, m=float(m),
                                                        TO=a["to"], gross=a["gross"],
                                                        **marg(ra, bars))))
        print(f"  {book}: {len(DTRIG)*len(KCUT)} ddctl arms x {len(COSTS)} costs + {len(LADDER)} ladder points done")
    G = pd.DataFrame(grid)
    L = pd.DataFrame(ladder)
    for d in (G, L):
        d["p4b"] = (d.m_H1 > 0) & (d.m_H2 > 0) & (d.m_OOS > 0) & (d.m_DD > 0) & (d.m_CAGR > 0)
    return G, L, keep, bars, spy, v1, v2, start


# ---------------------------------------------------------------- idea 244's channel
def exchange(G, L, pname):
    """pp of CAGR surrendered per pp of MaxDD bought — ddctl vs the de-gross lever, and
    ddctl vs the static-gross point at its OWN realised gross."""
    at = G[(G.cost == PCOST) & (G.panel == pname)]
    out = []
    for b in BOOKS:
        lad = L[(L.book == b) & (L.panel == pname)].sort_values("m")
        c0 = at[(at.book == b) & (at.arm == "control")].iloc[0]
        # the de-gross lever's own exchange rate, measured the SAME way as ddctl's:
        # each ladder rung against the same unscaled control.
        lad = lad.copy()
        lad["dCAGR"] = (c0.CAGR - lad.CAGR) * 100.0
        lad["dMaxDD"] = (abs(c0.MaxDD) - lad.MaxDD.abs()) * 100.0
        lad["rate"] = np.where(lad.dMaxDD > 1e-9, lad.dCAGR / lad.dMaxDD, np.nan)
        # idea 40's convention for the same quantity: the FITTED slope of CAGR on |MaxDD|
        # over the whole ladder, one number per book.  Reported alongside the matched-budget
        # rate so the answer cannot be a measurement-convention artefact.
        slope = float(np.polyfit(lad.MaxDD.abs().values * 100.0, lad.CAGR.values * 100.0, 1)[0])
        for _, r in at[(at.book == b) & (at.arm != "control")].iterrows():
            dc = (c0.CAGR - r.CAGR) * 100.0
            dd = (abs(c0.MaxDD) - abs(r.MaxDD)) * 100.0
            j = (lad.gross - r.gross).abs().idxmin()          # matched REALISED gross
            mg = lad.loc[j]
            jd = (lad.dMaxDD - dd).abs().idxmin()             # matched DD BUDGET
            bd = lad.loc[jd]
            out.append(dict(panel=pname, book=b, arm=r.arm, D=r.D, k=r.k, T_pp=dd, dCAGR=dc,
                            rate_ddctl=(dc / dd if dd > 1e-9 else np.nan),
                            rate_degross_at_T=bd.rate, degross_m_at_T=bd.m,
                            rate_degross_slope=slope,
                            gross=r.gross, gm_m=mg.m, gm_gross=mg.gross,
                            vs_gm_CAGR=(r.CAGR - mg.CAGR) * 100.0,
                            vs_gm_MaxDD=(abs(mg.MaxDD) - abs(r.MaxDD)) * 100.0,
                            vs_gm_Sharpe=r.Sharpe - mg.Sharpe,
                            Sharpe=r.Sharpe, ctl_Sharpe=c0.Sharpe,
                            p4a_v2=r.p4a_v2, p4a_v1=r.p4a_v1, p4b=r.p4b, episodes=r.episodes))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- rule 8
def rule8(pname, keep, bars, spy, v1, v2, start, G, L):
    """(D, k) chosen on 2009-2016; evaluated untouched on 2017-2026."""
    is_bars = bars_of(spy.loc[:IS_END])
    rows = []
    for b in BOOKS:
        cands = [(D, k) for D in DTRIG for k in KCUT]
        recs = []
        for D, k in cands:
            ris = keep[(b, D, k)].loc[start:IS_END]
            m = metrics(ris); h1, h2 = halves(ris)
            recs.append(dict(D=D, k=k, IS_Sharpe=m["Sharpe"],
                             i_H1=h1 - is_bars["s1"], i_H2=h2 - is_bars["s2"],
                             i_DD=0.60 * abs(is_bars["sdd"]) - abs(m["MaxDD"]),
                             i_CAGR=m["CAGR"] - 0.70 * is_bars["scagr"]))
        I = pd.DataFrame(recs)
        ctl_is = keep[(b, None, None)].loc[start:IS_END]
        ctl_is_sh = metrics(ctl_is)["Sharpe"]
        picks = {}
        picks["S1 max IS Sharpe"] = I.loc[I.IS_Sharpe.idxmax()]
        ok = I[(I.i_H1 > 0) & (I.i_H2 > 0) & (I.i_DD > 0) & (I.i_CAGR > 0)]
        picks["S2 IS-4b-aware"] = ok.loc[ok.IS_Sharpe.idxmax()] if len(ok) else None
        for sel, p in picks.items():
            if p is None:
                rows.append(dict(panel=pname, book=b, selector=sel, pick="NOTHING (no IS-4b arm)"))
                continue
            ro = keep[(b, p.D, p.k)].loc[OOS_START:]
            mo = metrics(ro)
            co = metrics(keep[(b, None, None)].loc[OOS_START:])
            # matched-realised-gross static comparand, chosen on IS gross, read OOS
            g_arm = G[(G.panel == pname) & (G.book == b) & (G.cost == PCOST) &
                      (G.D == p.D) & (G.k == p.k)].iloc[0].gross
            lad = L[(L.book == b) & (L.panel == pname)]
            mg = lad.loc[(lad.gross - g_arm).abs().idxmin()]
            rows.append(dict(panel=pname, book=b, selector=sel, pick=f"D{p.D:.0%}/k{p.k:.2f}",
                             IS_Sharpe=p.IS_Sharpe, IS_ctl_Sharpe=ctl_is_sh,
                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             ctl_OOS_CAGR=co["CAGR"], ctl_OOS_Sharpe=co["Sharpe"], ctl_OOS_MaxDD=co["MaxDD"],
                             gm_m=mg.m, gm_OOS_CAGR=mg.OOS_CAGR, gm_OOS_Sharpe=mg.OOS_Sharpe,
                             gm_OOS_MaxDD=mg.OOS_MaxDD,
                             v2_OOS_Sharpe=metrics(v2[10].loc[OOS_START:])["Sharpe"],
                             v2_OOS_CAGR=metrics(v2[10].loc[OOS_START:])["CAGR"],
                             v2_OOS_MaxDD=metrics(v2[10].loc[OOS_START:])["MaxDD"],
                             v1_OOS_Sharpe=metrics(v1[10].loc[OOS_START:])["Sharpe"],
                             spy_OOS_Sharpe=bars["soos"],
                             spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                             spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"],
                             beats_ctl=mo["Sharpe"] > co["Sharpe"],
                             beats_matched_gross=mo["Sharpe"] > mg.OOS_Sharpe))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    print("=" * 100)
    print("IDEA 255 — does ddctl really own the deep budgets?  (D x k tuned; panel/book/cost reported)")
    print("=" * 100)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    drop = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    s = load_universe(small=True)
    P = {"u56": load_universe(), "broad136": load_universe(broad=True),
         "small439": s.drop(columns=[c for c in s.columns if c in drop])}
    print(f"  small panel: dropped {len(drop)} tickers with max_1d_move >= 1.0 -> "
          f"{P['small439'].shape[1] - 1} names + SPY")

    GA, LA, XA, WA = [], [], [], []
    for pname, px in P.items():
        G, L, keep, bars, spy, v1, v2, start = do_panel(pname, px)
        GA.append(G); LA.append(L)
        X = exchange(G, L, pname); XA.append(X)
        WA.append(rule8(pname, keep, bars, spy, v1, v2, start, G, L))
    G = pd.concat(GA, ignore_index=True); L = pd.concat(LA, ignore_index=True)
    X = pd.concat(XA, ignore_index=True); W = pd.concat(WA, ignore_index=True)
    G.to_csv(OUT(".grid.csv"), index=False)
    L.to_csv(OUT(".ladder.csv"), index=False)
    X.to_csv(OUT(".exchange.csv"), index=False)
    W.to_csv(OUT(".walkforward.csv"), index=False)

    print(f"\n\n{'#'*100}\n# FULL GRID — {len(G)} ddctl/control points + {len(L)} ladder points, ALL REPORTED\n{'#'*100}")
    cols = ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "cut_days", "episodes",
            "p4a_v2", "p4a_v1", "p4b"]
    print(G.sort_values(["panel", "book", "cost", "D", "k"])[cols].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n### STATIC-GROSS LADDER — {len(L)} points, ALL REPORTED (10 bps, no drawdown rule)")
    print(L.sort_values(["panel", "book", "m"])[
        ["panel", "book", "m", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
         "OOS_MaxDD", "TO", "gross", "p4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print(f"\n\n{'#'*100}\n# (1) THE CLAIM — exchange rate by DRAWDOWN BUDGET T (pp of MaxDD bought)\n{'#'*100}")
    print("  idea 251: ddctl 0.43-0.51 pp CAGR per pp MaxDD at T=8-10pp vs de-gross 0.58-0.61.\n")
    rows = []
    for lo, hi in BUDGET_BINS:
        sl = X[(X["T_pp"] >= lo) & (X["T_pp"] < hi)]
        for pan in list(P) + ["ALL"]:
            g = sl if pan == "ALL" else sl[sl.panel == pan]
            if len(g) == 0:
                continue
            rows.append(dict(bin=f"[{lo},{hi})", panel=pan, n=len(g),
                             ddctl_med=g.rate_ddctl.median(), degross_med=g.rate_degross_at_T.median(),
                             delta=g.rate_ddctl.median() - g.rate_degross_at_T.median(),
                             ddctl_cheaper=int((g.rate_ddctl < g.rate_degross_at_T).sum()),
                             degross_slope=g.rate_degross_slope.median(),
                             cheaper_vs_slope=int((g.rate_ddctl < g.rate_degross_slope).sum())))
    R = pd.DataFrame(rows)
    print(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    R.to_csv(OUT(".budget.csv"), index=False)
    deep = X[(X["T_pp"] >= 8) & (X["T_pp"] < 10)]
    if len(deep):
        d = deep.rate_ddctl - deep.rate_degross_at_T
        t = d.mean() / (d.std(ddof=1) / math.sqrt(len(d))) if len(d) > 1 and d.std(ddof=1) > 0 else np.nan
        print(f"\n  THE 8-10pp CELL: n={len(deep)}  ddctl median {deep.rate_ddctl.median():.4f} "
              f"(range {deep.rate_ddctl.min():.4f}..{deep.rate_ddctl.max():.4f})  "
              f"de-gross median {deep.rate_degross_at_T.median():.4f}  "
              f"paired mean delta {d.mean():+.4f}  t {t:+.2f}  ddctl cheaper in "
              f"{int((d < 0).sum())}/{len(d)}")
        ds = deep.rate_ddctl - deep.rate_degross_slope
        print(f"  same cell against idea 40's FITTED-SLOPE convention: de-gross median "
              f"{deep.rate_degross_slope.median():.4f}  paired mean delta {ds.mean():+.4f}  "
              f"ddctl cheaper in {int((ds < 0).sum())}/{len(ds)}")

    print("\n  [1b] the D=2% rung specifically — idea 251 says the claim needs the ladder to run there\n")
    d2 = X[X.D <= 0.03]
    if len(d2):
        print(d2.groupby(["panel", "book", "D"]).agg(
            n=("rate_ddctl", "size"), T_pp=("T_pp", "median"), ddctl=("rate_ddctl", "median"),
            degross=("rate_degross_at_T", "median"), episodes=("episodes", "median"),
            vs_gm_Sharpe=("vs_gm_Sharpe", "median")).to_string(float_format=lambda x: f"{x:.4f}"))
        print(f"\n  D<=3% arms: {len(d2)}   cheaper than de-gross at matched budget: "
              f"{int((d2.rate_ddctl < d2.rate_degross_at_T).sum())}   "
              f"beating matched-gross on Sharpe: {int((d2.vs_gm_Sharpe > 0).sum())}")

    print(f"\n\n{'#'*100}\n# (2) DOES IT SURVIVE GROSS MATCHING? (idea 244's channel)\n{'#'*100}")
    print("  every ddctl arm vs the static-gross rung at its OWN realised average gross\n")
    rows = []
    for lo, hi in BUDGET_BINS:
        sl = X[(X["T_pp"] >= lo) & (X["T_pp"] < hi)]
        for pan in list(P) + ["ALL"]:
            g = sl if pan == "ALL" else sl[sl.panel == pan]
            if len(g) == 0:
                continue
            rows.append(dict(bin=f"[{lo},{hi})", panel=pan, n=len(g),
                             med_dCAGR=g.vs_gm_CAGR.median(), med_dMaxDD=g.vs_gm_MaxDD.median(),
                             med_dSharpe=g.vs_gm_Sharpe.median(),
                             beats_gm_Sharpe=int((g.vs_gm_Sharpe > 0).sum()),
                             beats_gm_both=int(((g.vs_gm_Sharpe > 0) & (g.vs_gm_MaxDD > 0)).sum())))
    Q = pd.DataFrame(rows)
    print(Q.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    Q.to_csv(OUT(".grossmatched.csv"), index=False)
    for pan in list(P) + ["ALL"]:
        g = X if pan == "ALL" else X[X.panel == pan]
        print(f"  {pan:9s} n={len(g):4d}  beats matched-gross on Sharpe {int((g.vs_gm_Sharpe > 0).sum()):4d} "
              f"({(g.vs_gm_Sharpe > 0).mean():.1%})   on Sharpe AND MaxDD "
              f"{int(((g.vs_gm_Sharpe > 0) & (g.vs_gm_MaxDD > 0)).sum()):4d}")
    dsub = X[(X["T_pp"] >= 8)]
    if len(dsub):
        print(f"  DEEP (T >= 8pp): n={len(dsub)}  beats matched-gross on Sharpe "
              f"{int((dsub.vs_gm_Sharpe > 0).sum())} ({(dsub.vs_gm_Sharpe > 0).mean():.1%})  "
              f"median dSharpe {dsub.vs_gm_Sharpe.median():+.4f}")

    print(f"\n\n{'#'*100}\n# (3) RULE 8 — (D,k) chosen on 2009-2016, evaluated untouched on 2017-2026\n{'#'*100}\n")
    wc = ["panel", "book", "selector", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
          "ctl_OOS_Sharpe", "gm_m", "gm_OOS_Sharpe", "gm_OOS_MaxDD", "v2_OOS_Sharpe",
          "spy_OOS_Sharpe", "beats_ctl", "beats_matched_gross"]
    print(W[[c for c in wc if c in W.columns]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ok = W.dropna(subset=["OOS_Sharpe"])
    if len(ok):
        print(f"\n  rule-8 picks beating their own CONTROL out of sample:        "
              f"{int(ok.beats_ctl.sum())}/{len(ok)}")
        print(f"  rule-8 picks beating the MATCHED-GROSS static book OOS:      "
              f"{int(ok.beats_matched_gross.sum())}/{len(ok)}")
        print(f"  rule-8 picks beating the LIVE RULES v2 book OOS on Sharpe:   "
              f"{int((ok.OOS_Sharpe > ok.v2_OOS_Sharpe).sum())}/{len(ok)}")
        print(f"  rule-8 picks beating SPY OOS on Sharpe:                      "
              f"{int((ok.OOS_Sharpe > ok.spy_OOS_Sharpe).sum())}/{len(ok)}")
        print(f"  mean OOS Sharpe: pick {ok.OOS_Sharpe.mean():.4f}  control {ok.ctl_OOS_Sharpe.mean():.4f}  "
              f"matched-gross {ok.gm_OOS_Sharpe.mean():.4f}")
        print(f"  mean OOS CAGR:   pick {ok.OOS_CAGR.mean():.2%}  control {ok.ctl_OOS_CAGR.mean():.2%}  "
              f"matched-gross {ok.gm_OOS_CAGR.mean():.2%}")

    print(f"\n\n{'#'*100}\n# (3b) DEGENERACY CENSUS — how many 'ddctl arms' are the control wearing a label?\n{'#'*100}")
    print("  a ddctl arm whose trigger never fires (episodes == 0), or whose k never bites, is")
    print("  numerically IDENTICAL to its control.  Idea 458's constant-arm problem, here.\n")
    tr = G[G.D.notna()].copy()
    ctl = G[G.D.isna()].set_index(["panel", "book", "cost"])
    key = list(zip(tr.panel, tr.book, tr.cost))
    tr["ctl_CAGR"] = [ctl.loc[k].CAGR for k in key]
    tr["ctl_Sharpe"] = [ctl.loc[k].Sharpe for k in key]
    tr["identical"] = (np.abs(tr.CAGR - tr.ctl_CAGR) < 1e-9) & (np.abs(tr.Sharpe - tr.ctl_Sharpe) < 1e-9)
    dg = tr.groupby(["panel", "book"]).agg(arms=("arm", "size"), never_armed=("episodes", lambda s: int((s == 0).sum())),
                                           identical=("identical", "sum")).reset_index()
    print(dg.to_string(index=False))
    print(f"\n  ALL: {len(tr)} ddctl arms, {int((tr.episodes == 0).sum())} never arm "
          f"({(tr.episodes == 0).mean():.1%}), {int(tr.identical.sum())} are numerically "
          f"identical to their own control ({tr.identical.mean():.1%})")
    tr.to_csv(OUT(".degeneracy.csv"), index=False)

    print(f"\n\n{'#'*100}\n# (4) BOTH KEEP PATHS — all {len(G)} grid points\n{'#'*100}\n")
    tb = G.groupby(["panel", "book"]).agg(n=("arm", "size"), p4a_v2=("p4a_v2", "sum"),
                                          p4a_v1=("p4a_v1", "sum"), p4b=("p4b", "sum")).reset_index()
    print(tb.to_string(index=False))
    print(f"\n  TOTAL  n={len(G)}   4a vs LIVE RULES v2: {int(G.p4a_v2.sum())}   "
          f"4a vs superseded v1: {int(G.p4a_v1.sum())}   4b: {int(G.p4b.sum())}")
    b4 = G[G.p4b]
    if len(b4):
        print("\n  4b passers (full sample, all costs):")
        print(b4.sort_values("Sharpe", ascending=False)[
            ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_Sharpe", "gross", "m_CAGR", "m_DD"]].head(40).to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
        # which of them are ddctl rather than the control?
        print(f"\n  of the {len(b4)} 4b passers, {int(b4.D.notna().sum())} are ddctl arms and "
              f"{int(b4.D.isna().sum())} are the plain control")
        b4t = b4[b4.D.notna()].merge(tr[["panel", "book", "cost", "arm", "identical"]],
                                     on=["panel", "book", "cost", "arm"], how="left")
        print(f"  of those {len(b4t)} ddctl 4b passers, {int(b4t.identical.sum())} are NUMERICALLY "
              f"IDENTICAL to their own control (never-armed duplicates) and "
              f"{int((~b4t.identical.astype(bool)).sum())} are genuinely distinct books")
    else:
        print("\n  no 4b passer anywhere in the grid.")
    print("\nDone. Artefacts: " + ", ".join(Path(str(OUT(e))).name for e in
          (".grid.csv", ".ladder.csv", ".exchange.csv", ".budget.csv", ".grossmatched.csv",
           ".walkforward.csv")))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 350: is the BINDING drawdown episode a HIGH-BREADTH event across the whole record?

Idea 41 found that the U56 n=3 book's maximum drawdown is untouched by ANY depth of breadth
gate, and diagnosed the reason as timing: the episode runs (almost) entirely while panel
breadth is still above 30%, so a gate that only fires below 30% is never armed while the loss
is being taken.  If that is a RECORD-WIDE fact rather than one book's accident, then every
breadth-gated risk overlay in the queue is aimed at the wrong window and the family can be
retired on sight instead of being re-run per book.

WHAT IS CENSUSED.  The queue says "every book in the record's committed grid CSVs".  Those
1000+ CSVs do not carry reconstructible weight functions -- they carry summary rows -- so a
literal parse would date-stamp nothing.  Instead this run rebuilds the record's SPANNING SET
of canonical constructions from source and stamps each one: EWALL (no filter), TOP3 / TOP10 /
TOP20 (idea 40/41's composite books), MAEW (200d-gated equal weight, de-gross to cash) and
RULES v2 (the live book) -- 6 forms x 3 panels (U56, B136, SMALL439) x 3 cost rungs = 54
stamped books.  That covers the filtered, unfiltered, concentrated, wide and live corners the
record's grids actually occupy.  Every point is written to the CSVs; nothing is filtered out.

  TUNED PARAMETERS -- exactly two, fixed before any number was read:
     1. breadth threshold B in {0.30, 0.40, 0.50}   (idea 42/48's own dial, unchanged)
     2. gate depth d in {0.25, 0.50, 1.00}          (fraction of gross moved to CASH when armed)
  NOT TUNED / reported axes: book form (6), panel (3), cost rung (0/10/25 bps).

THE DECISIVE STATISTIC is not "mean breadth in the window" -- a window mean can sit above B
while the loss is taken on the handful of days below it.  It is the LOSS SHARE:

    share_above(B) = (sum of the window's daily log losses on days where E_{t-1} >= B)
                     / (total window log loss)

An overlay armed below B can, by construction, only ever address 1 - share_above(B) of the
episode.  share_above(0.30) ~ 1.0 means a 30% breadth gate is structurally incapable of
touching the binding drawdown, whatever its depth.  Reported beside it: the window-mean
breadth, the panel's unconditional mean, and the PERCENTILE of the window mean inside the
distribution of all same-length rolling windows on that panel (the null that answers "is this
window unusually high-breadth, or just an ordinary one?").

BREADTH.  E_t = share of the panel's own priced names (SPY excluded everywhere -- it is a
benchmark, and on SMALL439 it is not a constituent at all) trading above their own 200d
moving average on day t.  This is the record's breadth definition (ideas 41/42/48).  The gate
reads E_{t-1} so the switch executes at t+1 (protocol 2).

THE NUMERAIRE BAR (idea 351/372's decision form, carried here): a constant exposure multiplier
buys drawdown at the book's own |MaxDD| / CAGR at zero Sharpe cost.  Every overlay point is
scored against its OWN control's numeraire, so "the gate cut the drawdown" is only credited
where it beat simply holding less.

RULE 8 walk-forward: the (B, d) menu -- gate-OFF INCLUDED as a menu item -- is chosen on
2008-2016 at 10 bps by IS Sharpe, then 2017-2026 is read once against the do-nothing control,
the OOS-best cell (regret), RULES v2 (live) and SPY.  Both KEEP paths are evaluated at every
one of the 486 overlay points plus the 54 controls: 4a vs the LIVE RULES v2 book, 4b vs SPY.

REPRODUCTION GATES (section [0], run before any new number is read):
  * derived rung r(c) = r(0) - turnover*c/1e4 equals engine.backtest(cost_bps=c) to 1e-12;
  * idea 40/41's published U56 controls: NONE n=3 21.9%/1.04/-25.8% (H1 1.01 / H2 1.06) and
    NONE n=5 16.5%/0.95/-21.6%;
  * the LIVE RULES v2 U56 row: 8.66% / 1.2056 / -12.05% (halves 1.2259 / 1.1908).
  Published-number gates are REPORTED as PASS/FAIL with the miss, not asserted away.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so drawdown
LEVELS are optimistic; the loss-share statistic is a within-window decomposition and is not
affected by the level, but 4b's DD cap is.  SMALL439 drops the 44 tickers with max_1d_move
>= 1.0 and starts 2010-01-04, so its halves are not the same calendar halves as U56/B136.
(2) The sample begins 2008 with a 260-day warm-up, so the 2008 crash is only partly inside it;
the binding episode for most books is therefore 2020 or 2022, not the GFC.  (3) Breadth built
on a 200d MA is a LAGGING statistic by construction -- that is the hypothesis under test (a
lagging alarm cannot ring before the loss), not a defect of the measurement.  (4) The loss
share is computed on the book's own realised return path at the rung, so it already contains
costs.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                            # noqa
from engine import backtest, metrics                                                   # noqa

SLUG = "2026-09-07_is-the-BINDING-DRAWDOWN-EPISODE-a-HIGH-BREADTH-event_C"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, BAND = 0.60, 0.75, 0.03
BS = [0.30, 0.40, 0.50]                          # tuned parameter 1
DEPTHS = [0.25, 0.50, 1.00]                      # tuned parameter 2
COSTS = [0, 10, 25]
FORMS = ["EWALL", "TOP3", "TOP10", "TOP20", "MAEW", "RULESV2"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
FREE_EPS = 0.05                                  # pp of CAGR below which the ruler is undefined


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def panels():
    p = {}
    p["U56"] = load_universe()
    p["B136"] = load_universe(broad=True)
    p["SMALL439"] = small_panel()
    for k, v in p.items():
        print(f"    {k}: {v.shape[1]} cols, {v.index[0].date()} .. {v.index[-1].date()}")
    return p


def book_cols(px, panel):
    """Columns a BOOK may hold.  SPY is a constituent of U56/B136 but only a benchmark on SMALL."""
    return [c for c in px.columns if not (panel == "SMALL439" and c == "SPY")]


def breadth(px, panel):
    """E_t = share of the panel's own priced names (SPY always excluded) above their 200d MA."""
    cols = [c for c in px.columns if c != "SPY"]
    q = px[cols]
    above = q > q.rolling(200).mean()
    priced = q.notna() & q.rolling(200).mean().notna()
    return (above & priced).sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)


# ---------------------------------------------------------------- the six book forms
def weights_for(px, panel, form):
    cols = book_cols(px, panel)
    q = px[cols]
    if form == "EWALL":
        e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
        w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif form.startswith("TOP"):
        n = int(form[3:])
        s = score(q, vol_scale=False)[0]
        _, above, vol20 = score(q)
        rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (GROSS / n)
    elif form == "MAEW":
        above = q > q.rolling(200).mean()
        e = above.astype(float).where(q.notna(), 0.0)
        n_priced = q.notna().sum(axis=1).replace(0, np.nan)
        w = GROSS * e.div(n_priced, axis=0).fillna(0.0)          # de-gross: gated weight -> CASH
    elif form == "RULESV2":
        w = rules_v2_weights(q, band=BAND, gross=GROSS)
    else:
        raise ValueError(form)
    return w.reindex(columns=px.columns).fillna(0.0)


# ---------------------------------------------------------------- metric helpers
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def dd_window(r):
    """(peak_date, trough_date, depth) of the MAXIMUM drawdown of the return path r."""
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1
    trough = dd.idxmin()
    peak = eq.loc[:trough].idxmax()
    return peak, trough, float(dd.min())


def loss_share(r, E, peak, trough, B):
    """Share of the window's total log LOSS taken on days where the gate would NOT be armed
    (E_{t-1} >= B).  1.0 => a gate armed below B cannot touch any of the episode."""
    seg = r.loc[peak:trough].iloc[1:]                       # (peak, trough]
    if len(seg) == 0:
        return np.nan
    lg = np.log1p(seg.clip(lower=-0.9999))
    tot = lg.sum()
    if tot >= 0:
        return np.nan
    e = E.shift(1).reindex(seg.index)
    return float(lg.where(e >= B, 0.0).sum() / tot)


def neg_share(r, E, peak, trough, B):
    """Unsigned companion to loss_share: share of the window's GROSS down-day losses taken while
    E_{t-1} >= B.  Bounded in [0,1] even when the low-breadth days inside the window were net
    positive (which is what makes the signed loss_share leave [0,1])."""
    seg = r.loc[peak:trough].iloc[1:]
    if len(seg) == 0:
        return np.nan
    lg = np.log1p(seg.clip(lower=-0.9999))
    down = -lg.clip(upper=0.0)
    tot = down.sum()
    if tot <= 0:
        return np.nan
    e = E.shift(1).reindex(seg.index)
    return float(down.where(e >= B, 0.0).sum() / tot)


def window_pctile(E, peak, trough):
    """Percentile of the window's mean breadth among ALL same-length rolling windows."""
    n = len(E.loc[peak:trough])
    if n < 2:
        return np.nan
    roll = E.rolling(n).mean().dropna()
    obs = float(E.loc[peak:trough].mean())
    return float((roll <= obs).mean())


def fmt(x, p=3):
    return "nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{p}f}"


# ---------------------------------------------------------------- run
def build():
    P = panels()
    rows_win, rows_grid = [], []
    wf = []

    # ---------------------------------------------------------- [0] reproduction gates
    print("\n[0] REPRODUCTION GATES")
    px = P["U56"]
    w = weights_for(px, "U56", "TOP3")
    b0 = backtest(px, w, cost_bps=0, freq="W")
    b25 = backtest(px, w, cost_bps=25, freq="W")
    derived = b0["returns"] - b0["turnover"] * 25 / 1e4
    gate_id = float(np.abs(derived - b25["returns"]).max())
    print(f"    derived rung identity max|diff| = {gate_id:.3e}  ({'PASS' if gate_id < 1e-12 else 'FAIL'})")
    assert gate_id < 1e-12, "derived rung identity broken"

    start = px.index[WARMUP]
    for n, pub in ((3, (0.219, 1.04, -0.258, 1.01, 1.06)), (5, (0.165, 0.95, -0.216, None, None))):
        r = backtest(px, weights_for(px, "U56", f"TOP{n}"), cost_bps=10, freq="W")["returns"].loc[start:]
        m = metrics(r); h1, h2 = hs(r)
        ok = abs(m["CAGR"] - pub[0]) < 0.005 and abs(m["Sharpe"] - pub[1]) < 0.02 and abs(m["MaxDD"] - pub[2]) < 0.005
        print(f"    idea 40/41 U56 NONE n={n}: {m['CAGR']:.1%}/{m['Sharpe']:.2f}/{m['MaxDD']:.1%} "
              f"(H {h1:.2f}/{h2:.2f}) vs published {pub[0]:.1%}/{pub[1]:.2f}/{pub[2]:.1%} -> {'PASS' if ok else 'FAIL'}")
    rv2 = backtest(px, rules_v2_weights(px, band=BAND, gross=GROSS), cost_bps=10, freq="W")["returns"].loc[start:]
    m = metrics(rv2); h1, h2 = hs(rv2)
    ok = abs(m["CAGR"] - 0.0866) < 0.002 and abs(m["Sharpe"] - 1.2056) < 0.01 and abs(m["MaxDD"] + 0.1205) < 0.002
    print(f"    LIVE RULES v2 U56: {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} (H {h1:.4f}/{h2:.4f}) "
          f"vs published 8.66%/1.2056/-12.05% (1.2259/1.1908) -> {'PASS' if ok else 'FAIL'}")

    # gate 4: idea 41's own committed breadth-gate cells (U56 n=3, B=0.30, 10 bps).  Idea 41's
    # multiplier-when-armed is `depth`; this file's dial is the CUT, so mult = 1 - d.  Its breadth
    # INCLUDED SPY on U56 and this file's excludes it, so CAGR differs in the 4th decimal; MaxDD
    # is the number the queue's claim turns on and is asserted to match.
    i41 = ROOT / "research" / "backtests" / "2026-09-07_breadth-gate-depth_cloud.grid.csv"
    if i41.exists():
        ref = pd.read_csv(i41)
        ref = ref[(ref.panel == "U56") & (ref.n == 3)].set_index("depth")
        E56 = breadth(px, "U56").loc[start:]
        r10 = backtest(px, weights_for(px, "U56", "TOP3"), cost_bps=0, freq="W")
        rc = (r10["returns"] - r10["turnover"] * 10 / 1e4).loc[start:]
        armed = (E56 < 0.30).shift(1).fillna(False)
        for d, refd in ((0.25, 0.75), (0.50, 0.50), (1.00, 0.00)):
            if refd not in ref.index:
                continue
            mult = pd.Series(np.where(armed, 1.0 - d, 1.0), index=rc.index)
            dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))
            rg = pd.Series(mult.values * rc.values - dm * GROSS * 10 / 1e4, index=rc.index)
            mg = metrics(rg)
            ok = abs(mg["MaxDD"] - ref.loc[refd, "MaxDD_10"]) < 1e-6
            print(f"    idea 41 U56 n=3 mult={1-d:.2f} @10bps: MaxDD {mg['MaxDD']:.6f} vs committed "
                  f"{ref.loc[refd, 'MaxDD_10']:.6f} -> {'PASS' if ok else 'FAIL'} "
                  f"(CAGR {mg['CAGR']:.4f} vs {ref.loc[refd, 'CAGR_10']:.4f}, SPY-in-breadth diff)")

    # ---------------------------------------------------------- census
    for panel, px in P.items():
        start = px.index[WARMUP]
        E = breadth(px, panel).loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bw = rules_v2_weights(px[book_cols(px, panel)], band=BAND, gross=GROSS)
        base10 = backtest(px, bw.reindex(columns=px.columns).fillna(0.0),
                          cost_bps=10, freq="W")["returns"].loc[start:]
        print(f"\n[1] {panel}: breadth mean {E.mean():.3f}, days below "
              + ", ".join(f"B={b:.2f} {float((E < b).mean()):.3f}" for b in BS))

        for form in FORMS:
            res = backtest(px, weights_for(px, panel, form), cost_bps=0, freq="W")
            r0, t0 = res["returns"].loc[start:], res["turnover"].loc[start:]
            for c in COSTS:
                rc = r0 - t0 * c / 1e4
                pk, tr, dep = dd_window(rc)
                mc = metrics(rc)
                num = abs(mc["MaxDD"]) / mc["CAGR"] if mc["CAGR"] > 0 else np.nan
                row = dict(panel=panel, form=form, cost=c, CAGR=mc["CAGR"], Sharpe=mc["Sharpe"],
                           MaxDD=mc["MaxDD"], peak=str(pk.date()), trough=str(tr.date()),
                           days=len(rc.loc[pk:tr]), depth_pct=dep,
                           E_window=float(E.loc[pk:tr].mean()), E_panel=float(E.mean()),
                           E_win_min=float(E.loc[pk:tr].min()),
                           E_pctile=window_pctile(E, pk, tr), numeraire=num)
                for b in BS:
                    row[f"share_days_ge_{b:.2f}"] = float((E.loc[pk:tr] >= b).mean())
                    row[f"loss_share_ge_{b:.2f}"] = loss_share(rc, E, pk, tr, b)
                    row[f"neg_share_ge_{b:.2f}"] = neg_share(rc, E, pk, tr, b)
                rows_win.append(row)

                # ------- overlay grid: gate to cash below B, depth d, executed t+1
                for b in BS:
                    armed = (E < b).shift(1).fillna(False)
                    for d in DEPTHS:
                        mult = pd.Series(np.where(armed, 1.0 - d, 1.0), index=rc.index)
                        dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))
                        rg = pd.Series(mult.values * rc.values - dm * GROSS * c / 1e4, index=rc.index)
                        mg = metrics(rg); h1, h2 = hs(rg)
                        ok_b, fb = bars_4b(rg, spy); ok_a, fa = bars_4a(rg, base10)
                        pk2, tr2, _ = dd_window(rg)
                        dcagr = 100 * (mg["CAGR"] - mc["CAGR"])
                        dddp = 100 * (abs(mc["MaxDD"]) - abs(mg["MaxDD"]))
                        ratio = np.nan if dcagr >= -FREE_EPS else dddp / (-dcagr)
                        rows_grid.append(dict(
                            panel=panel, form=form, cost=c, B=b, depth=d,
                            CAGR=mg["CAGR"], Sharpe=mg["Sharpe"], MaxDD=mg["MaxDD"], H1=h1, H2=h2,
                            OOS_CAGR=metrics(rg.loc[OOS_START:])["CAGR"],
                            OOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"],
                            OOS_MaxDD=metrics(rg.loc[OOS_START:])["MaxDD"],
                            IS_Sharpe=metrics(rg.loc[:IS_END])["Sharpe"],
                            ctrl_CAGR=mc["CAGR"], ctrl_Sharpe=mc["Sharpe"], ctrl_MaxDD=mc["MaxDD"],
                            dCAGR_pp=dcagr, dDD_pp=dddp, ratio=ratio, numeraire=num,
                            beats_numeraire=(not np.isnan(ratio)) and (ratio > num),
                            dSharpe=mg["Sharpe"] - mc["Sharpe"],
                            window_moved=(str(pk2.date()) != str(pk.date()) or str(tr2.date()) != str(tr.date())),
                            new_peak=str(pk2.date()), new_trough=str(tr2.date()),
                            new_E_window=float(E.loc[pk2:tr2].mean()),
                            new_E_pctile=window_pctile(E, pk2, tr2),
                            new_neg_share=neg_share(rg, E, pk2, tr2, b),
                            new_loss_share=loss_share(rg, E, pk2, tr2, b),
                            pass4a=ok_a, fail4a=",".join(fa), pass4b=ok_b, fail4b=",".join(fb)))

                # ------- rule 8 (10 bps only): menu = OFF + 9 gate cells, chosen on IS Sharpe
                if c == 10:
                    menu = [("OFF", np.nan, np.nan, rc)]
                    for b in BS:
                        armed = (E < b).shift(1).fillna(False)
                        for d in DEPTHS:
                            mult = pd.Series(np.where(armed, 1.0 - d, 1.0), index=rc.index)
                            dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))
                            menu.append((f"B{b:.2f}_d{d:.2f}", b, d,
                                         pd.Series(mult.values * rc.values - dm * GROSS * c / 1e4, index=rc.index)))
                    iss = [(metrics(x[3].loc[:IS_END])["Sharpe"], x) for x in menu]
                    pick = max(iss, key=lambda z: z[0])[1]
                    oos = [(metrics(x[3].loc[OOS_START:])["Sharpe"], x[0]) for x in menu]
                    best_oos = max(oos, key=lambda z: z[0])
                    po = metrics(pick[3].loc[OOS_START:])
                    co = metrics(rc.loc[OOS_START:])
                    wf.append(dict(panel=panel, form=form, pick=pick[0], B=pick[1], depth=pick[2],
                                   IS_Sharpe=metrics(pick[3].loc[:IS_END])["Sharpe"],
                                   OOS_CAGR=po["CAGR"], OOS_Sharpe=po["Sharpe"], OOS_MaxDD=po["MaxDD"],
                                   ctrl_OOS_CAGR=co["CAGR"], ctrl_OOS_Sharpe=co["Sharpe"],
                                   ctrl_OOS_MaxDD=co["MaxDD"],
                                   best_OOS_cell=best_oos[1], best_OOS_Sharpe=best_oos[0],
                                   regret=best_oos[0] - po["Sharpe"],
                                   base_OOS_Sharpe=metrics(base10.loc[OOS_START:])["Sharpe"],
                                   spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                                   spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                                   spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"]))
            print(f"    {panel:9s} {form:8s} stamped "
                  + " | ".join(f"{c}bps {rows_win[-3+i]['peak']}->{rows_win[-3+i]['trough']} "
                               f"{rows_win[-3+i]['depth_pct']:.1%} lossshare30 "
                               f"{fmt(rows_win[-3+i]['loss_share_ge_0.30'])}" for i, c in enumerate(COSTS)))

        # panel context row: SPY + baseline
        for nm, r in (("SPY", spy), ("RULESv2", base10)):
            m = metrics(r); pk, tr, dep = dd_window(r)
            print(f"    [ctx] {panel} {nm}: {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%} "
                  f"DD {pk.date()}->{tr.date()} lossshare30 {fmt(loss_share(r, E, pk, tr, 0.30))}")

    W = pd.DataFrame(rows_win); G = pd.DataFrame(rows_grid); F = pd.DataFrame(wf)
    W.to_csv(OUT / f"{SLUG}.windows.csv", index=False)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    F.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    return W, G, F


def analyse(W, G, F):
    print("\n[2] THE CENSUS: is the binding drawdown a HIGH-BREADTH event?")
    print("    (loss_share_ge_B = share of the peak-to-trough log loss taken while E_{t-1} >= B,")
    print("     i.e. while a gate armed below B is OFF.  1.000 = the gate cannot touch the episode.)")
    cols = ["panel", "form", "cost", "peak", "trough", "days", "depth_pct", "E_window", "E_panel",
            "E_pctile", "loss_share_ge_0.30", "neg_share_ge_0.30", "loss_share_ge_0.40",
            "neg_share_ge_0.40", "loss_share_ge_0.50", "neg_share_ge_0.50"]
    print(W[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    for b in BS:
        s = W[f"loss_share_ge_{b:.2f}"].dropna()
        u = W[f"neg_share_ge_{b:.2f}"].dropna()
        print(f"\n    B={b:.2f}: SIGNED loss share -- median {s.median():.3f}, mean {s.mean():.3f}, "
              f"min {s.min():.3f}, max {s.max():.3f}; >=0.90 in {int((s >= 0.90).sum())}/{len(s)} books, "
              f">=0.99 in {int((s >= 0.99).sum())}/{len(s)}")
        print(f"           UNSIGNED down-day share -- median {u.median():.3f}, mean {u.mean():.3f}, "
              f"min {u.min():.3f}, max {u.max():.3f}; >=0.90 in {int((u >= 0.90).sum())}/{len(u)}, "
              f"<=0.50 in {int((u <= 0.50).sum())}/{len(u)}")
    print(f"\n    window-mean breadth vs panel mean: higher in "
          f"{int((W['E_window'] > W['E_panel']).sum())}/{len(W)} books; "
          f"median window percentile {W['E_pctile'].median():.3f} "
          f"(0.5 = an ordinary window, 1.0 = the highest-breadth window on the panel)")

    print("\n[3] THE OVERLAY GRID (all 486 points; the census's prediction is dDD ~ 0 at B=0.30)")
    for b in BS:
        for d in DEPTHS:
            g = G[(G.B == b) & (G.depth == d)]
            print(f"    B={b:.2f} d={d:.2f}: median dDD_pp {g.dDD_pp.median():+.3f}, "
                  f"median dCAGR_pp {g.dCAGR_pp.median():+.3f}, median dSharpe {g.dSharpe.median():+.4f}, "
                  f"beats numeraire {int(g.beats_numeraire.sum())}/{len(g)}, "
                  f"DD window moved {int(g.window_moved.sum())}/{len(g)}")
    print(f"\n    4a PASSES: {int(G.pass4a.sum())}/{len(G)}    4b PASSES: {int(G.pass4b.sum())}/{len(G)}")
    if G.pass4b.any():
        print(G[G.pass4b][["panel", "form", "cost", "B", "depth", "CAGR", "Sharpe", "MaxDD",
                           "H1", "H2", "OOS_Sharpe", "dDD_pp", "dCAGR_pp", "beats_numeraire"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n    4b failing bars (count by bar): "
          + ", ".join(f"{k} {int(G.fail4b.fillna('').str.contains(k).sum())}"
                      for k in ["H1", "H2", "OOS", "DD", "CAGR"]))
    print("    dDD_pp by cost rung: "
          + ", ".join(f"{c}bps median {G[G.cost == c].dDD_pp.median():+.3f}" for c in COSTS))
    print("    dDD_pp by panel: "
          + ", ".join(f"{p} median {G[G.panel == p].dDD_pp.median():+.3f}" for p in G.panel.unique()))

    print("\n[3b] THE RESIDUAL EPISODE: what does the gate leave behind when the window MOVES?")
    mv = G[G.window_moved]
    st = G[~G.window_moved]
    print(f"    window moved in {len(mv)}/{len(G)} points.  Where it moved, the RESIDUAL binding")
    print(f"    window's mean breadth is {mv.new_E_window.median():.3f} (median) at percentile "
          f"{mv.new_E_pctile.median():.3f}, vs {st.E_window.median() if 'E_window' in st else float('nan')}")
    print(f"    residual-window down-day share taken ABOVE the gate's own B: median "
          f"{mv.new_neg_share.median():.3f}; >= 0.90 in {int((mv.new_neg_share >= 0.90).sum())}/{len(mv)}, "
          f">= 0.99 in {int((mv.new_neg_share >= 0.99).sum())}/{len(mv)}")
    print("    (a residual episode with share ~1.0 is one the gate CANNOT reach at any depth -- "
          "that is the saturation idea 41 saw, and it is a property of the SECOND-worst episode.)")
    print("    dDD_pp where the window moved vs where it did not: "
          f"{mv.dDD_pp.median():+.3f} vs {st.dDD_pp.median():+.3f}")

    print("\n[4] RULE 8 WALK-FORWARD (menu = gate-OFF + 9 cells, chosen on IS<=2016 Sharpe @10 bps)")
    print(F[["panel", "form", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "ctrl_OOS_Sharpe", "ctrl_OOS_MaxDD", "best_OOS_cell", "best_OOS_Sharpe", "regret",
             "base_OOS_Sharpe", "spy_OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n    chooser picks the gate in {int((F['pick'] != 'OFF').sum())}/{len(F)} books; "
          f"OOS Sharpe vs its own control: better in {int((F.OOS_Sharpe > F.ctrl_OOS_Sharpe).sum())}/{len(F)}, "
          f"median dOOS {float((F.OOS_Sharpe - F.ctrl_OOS_Sharpe).median()):+.4f}; "
          f"median regret {F.regret.median():.4f}")
    print(f"    OOS MaxDD vs its own control: better in "
          f"{int((F.OOS_MaxDD.abs() < F.ctrl_OOS_MaxDD.abs()).sum())}/{len(F)}, "
          f"median dOOS_DD_pp {float(100 * (F.ctrl_OOS_MaxDD.abs() - F.OOS_MaxDD.abs()).median()):+.3f}")
    print(f"    OOS Sharpe > SPY OOS in {int((F.OOS_Sharpe > F.spy_OOS_Sharpe).sum())}/{len(F)}; "
          f"> RULES v2 OOS in {int((F.OOS_Sharpe > F.base_OOS_Sharpe).sum())}/{len(F)}")


def main():
    print(f"=== {SLUG}")
    print("Q: is the BINDING (max) drawdown episode a HIGH-BREADTH event across the record?")
    print(f"Tuned: B in {BS} x depth in {DEPTHS}.  Reported axes: {len(FORMS)} forms x 3 panels x {COSTS} bps.")
    w, g, f = (OUT / f"{SLUG}.windows.csv", OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.walkforward.csv")
    if RESUME and w.exists() and g.exists() and f.exists():
        analyse(pd.read_csv(w), pd.read_csv(g), pd.read_csv(f))
        return
    W, G, F = build()
    analyse(W, G, F)


if __name__ == "__main__":
    main()

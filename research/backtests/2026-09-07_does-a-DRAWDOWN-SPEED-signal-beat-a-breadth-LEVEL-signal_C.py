#!/usr/bin/env python3
"""Idea 376: does a breadth-SPEED signal beat a breadth-LEVEL signal on the same 54 books?

Idea 350 (committed, same lane) censused 54 canonical books and found that the binding
drawdown window is a LOW-breadth window in 54 of 54 cases, but that a gate armed on the LEVEL
of breadth is LATE: the median share of the window's down-day loss booked while a B=0.30 gate
is still OFF is 0.793.  Breadth built on a 200d moving average is lagging by construction, so
the queue's follow-up asks the obvious question: replace the LEVEL trigger with breadth's own
RATE OF CHANGE (idea 315's dial, E_t against its own L-day mean), hold the ARMED-DAY FREQUENCY
fixed so the two triggers spend the same number of days in cash, and report whether the
loss-share statistic MOVES -- i.e. whether a speed trigger reaches the loss the level trigger
misses.

WHAT IS COMPARED.  The same spanning set idea 350 stamped: EWALL / TOP3 / TOP10 / TOP20 /
MAEW / RULES v2 x U56 / B136 / SMALL439 x 0 / 10 / 25 bps = 54 books, rebuilt from source.

  TUNED PARAMETERS -- exactly two, fixed before any number was read:
     1. speed lookback L in {10, 20, 40}   (E_t minus its own L-day mean; 20 is idea 315's)
     2. arming quantile q in {0.10, 0.20, 0.30}  (share of days the gate is armed)
  NOT TUNED / reported axes, every point printed: trigger family (LEVEL / SPEED-L), gate depth
  (0.50 and 1.00), book form (6), panel (3), cost rung (0/10/25 bps).

MATCHED ARMED-DAY FREQUENCY is the whole point of the design, so BOTH families are armed by
the SAME rule on their own signal:

    LEVEL   signal  S_t = E_t                          (arm when breadth is low)
    SPEED-L signal  S_t = E_t - mean(E_{t-L+1..t})     (arm when breadth is falling)
    armed_t = 1[ S_{t-1} < Q_q(S_{..t-1}) ],  Q_q = CAUSAL expanding q-quantile, min 252 obs

so each family targets q armed days per unit time by construction and neither gets a free
exposure discount.  (Idea 350's fixed absolute B=0.30/0.40/0.50 arms 7 / 12 / 17% of U56 days
but 26 / 52 / 84% of SMALL439's -- idea 336's complaint -- which is exactly why the matched
quantile form is used here for both arms.)  The gate reads S_{t-1} and executes at t+1
(protocol rule 2); switching the multiplier costs |dmult| * GROSS * c bps.

THE DECISIVE STATISTIC (idea 350's, unchanged, so the two runs are comparable):

    off_share(gate) = (down-day log loss inside the CONTROL book's binding drawdown window
                       taken on days when this gate is OFF) / (total down-day log loss)

1.0 means the gate is structurally incapable of touching the episode; 0.0 means it is armed
through all of it.  Idea 350's committed median at B=0.30 is 0.793 -- reproduced here as gate
[0.4] before any new number is read.  The queue's question is whether the SPEED family's
off_share is lower AT MATCHED q, and whether that translates into drawdown.

Both KEEP paths are evaluated at all 1296 overlay points (4a vs the LIVE RULES v2 book, 4b vs
SPY), and rule 8 is run with THREE choosers (OFF+LEVEL only, OFF+SPEED only, OFF+both) so the
head-to-head is decided out of sample as well as in it.

REPRODUCTION GATES (section [0], run and printed as PASS/FAIL before any new number is read):
  * derived rung identity r(c) = r(0) - turnover*c/1e4 vs engine.backtest(cost_bps=25);
  * idea 40/41's published U56 controls (NONE n=3 21.9%/1.04/-25.8%, n=5 16.5%/0.95/-21.6%);
  * the LIVE RULES v2 U56 row 8.66%/1.2056/-12.05% (halves 1.2259/1.1908);
  * idea 350's own committed windows.csv: peak/trough dates and neg_share at B=0.30/0.40/0.50
    for all 54 books, asserted to 1e-6.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so drawdown
LEVELS are optimistic and 4b's DD cap is a level test; the off_share decomposition is
within-window and unaffected.  (2) SMALL439 drops the 44 tickers with max_1d_move >= 1.0 and
starts 2010-01-04, so its halves are not the same calendar halves as U56/B136.  (3) The sample
starts 2009-01-13 (260-day warm-up) so the GFC is only partly inside it and the binding episode
is 2020 or 2022 for most books.  (4) A speed signal is NOT lag-free either: E_t is itself built
on a 200d MA, so "speed" here is the rate of change of a slow statistic, which is the strongest
form of the queue's proposal that the record's breadth definition admits.

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

SLUG = "2026-09-07_does-a-DRAWDOWN-SPEED-signal-beat-a-breadth-LEVEL-signal_C"
OUT = ROOT / "research" / "backtests"
I350 = OUT / "2026-09-07_is-the-BINDING-DRAWDOWN-EPISODE-a-HIGH-BREADTH-event_C.windows.csv"
MAX_VOL, GROSS, BAND = 0.60, 0.75, 0.03
LOOKBACKS = [10, 20, 40]                         # tuned parameter 1
QS = [0.10, 0.20, 0.30]                          # tuned parameter 2
DEPTHS = [0.50, 1.00]                            # reported axis, not tuned
COSTS = [0, 10, 25]
FORMS = ["EWALL", "TOP3", "TOP10", "TOP20", "MAEW", "RULESV2"]
ABS_B = [0.30, 0.40, 0.50]                       # idea 350's absolute thresholds, gate only
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP, MINQ = 260, 252
FREE_EPS = 0.05


# ---------------------------------------------------------------- panels (idea 350's, verbatim)
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def panels():
    p = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    for k, v in p.items():
        print(f"    {k}: {v.shape[1]} cols, {v.index[0].date()} .. {v.index[-1].date()}")
    return p


def book_cols(px, panel):
    return [c for c in px.columns if not (panel == "SMALL439" and c == "SPY")]


def breadth(px, panel):
    cols = [c for c in px.columns if c != "SPY"]
    q = px[cols]
    above = q > q.rolling(200).mean()
    priced = q.notna() & q.rolling(200).mean().notna()
    return (above & priced).sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)


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
        w = GROSS * e.div(n_priced, axis=0).fillna(0.0)
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
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1
    trough = dd.idxmin()
    peak = eq.loc[:trough].idxmax()
    return peak, trough, float(dd.min())


def off_share(r, off_mask, peak, trough, signed=False):
    """Share of the (peak, trough] window's loss taken while the gate is OFF (not armed).
    signed=False -> down-day (unsigned) log loss, bounded in [0,1]; signed=True -> net log loss."""
    seg = r.loc[peak:trough].iloc[1:]
    if len(seg) == 0:
        return np.nan
    lg = np.log1p(seg.clip(lower=-0.9999))
    m = off_mask.reindex(seg.index).fillna(True).astype(bool)
    if signed:
        tot = lg.sum()
        return np.nan if tot >= 0 else float(lg.where(m, 0.0).sum() / tot)
    down = -lg.clip(upper=0.0)
    tot = down.sum()
    return np.nan if tot <= 0 else float(down.where(m, 0.0).sum() / tot)


def window_pctile(E, peak, trough):
    n = len(E.loc[peak:trough])
    if n < 2:
        return np.nan
    roll = E.rolling(n).mean().dropna()
    return float((roll <= float(E.loc[peak:trough].mean())).mean())


def spearman(a, b):
    d = pd.DataFrame({"a": np.asarray(a, float), "b": np.asarray(b, float)}).dropna()
    if len(d) < 3:
        return np.nan
    return float(d["a"].rank().corr(d["b"].rank()))


def fmt(x, p=3):
    return "nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{p}f}"


# ---------------------------------------------------------------- the two trigger families
def signals(E):
    """name -> signal series (LOW = arm)."""
    s = {"LEVEL": E.copy()}
    for L in LOOKBACKS:
        s[f"SPEED{L}"] = E - E.rolling(L).mean()
    return s


def armed_series(E):
    """(arm_name, q) -> boolean armed mask, already shifted for t+1 execution.
    Threshold is the CAUSAL expanding q-quantile of the signal's own history (min 252 obs),
    so LEVEL and SPEED are armed on the same fraction of days by construction."""
    out = {}
    for nm, s in signals(E).items():
        for q in QS:
            thr = s.expanding(min_periods=MINQ).quantile(q)
            out[(nm, q)] = (s < thr).shift(1).fillna(False).astype(bool)
    return out


def gated(rc, armed, depth, cost):
    mult = pd.Series(np.where(armed.reindex(rc.index).fillna(False), 1.0 - depth, 1.0), index=rc.index)
    dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))
    return pd.Series(mult.values * rc.values - dm * GROSS * cost / 1e4, index=rc.index)


# ---------------------------------------------------------------- run
def build():
    P = panels()
    rows_win, rows_grid, wf = [], [], []

    # ---------------------------------------------------------- [0] reproduction gates
    print("\n[0] REPRODUCTION GATES (printed before any new number is read)")
    px = P["U56"]
    w3 = weights_for(px, "U56", "TOP3")
    b0 = backtest(px, w3, cost_bps=0, freq="W")
    b25 = backtest(px, w3, cost_bps=25, freq="W")
    gid = float(np.abs((b0["returns"] - b0["turnover"] * 25 / 1e4) - b25["returns"]).max())
    print(f"    [0.1] derived rung identity max|diff| = {gid:.3e}  ({'PASS' if gid < 1e-12 else 'FAIL'})")
    assert gid < 1e-12

    start = px.index[WARMUP]
    for n, pub in ((3, (0.219, 1.04, -0.258)), (5, (0.165, 0.95, -0.216))):
        r = backtest(px, weights_for(px, "U56", f"TOP{n}"), cost_bps=10, freq="W")["returns"].loc[start:]
        m = metrics(r); h1, h2 = hs(r)
        ok = abs(m["CAGR"] - pub[0]) < 0.005 and abs(m["Sharpe"] - pub[1]) < 0.02 and abs(m["MaxDD"] - pub[2]) < 0.005
        print(f"    [0.2] idea 40/41 U56 NONE n={n}: {m['CAGR']:.1%}/{m['Sharpe']:.2f}/{m['MaxDD']:.1%} "
              f"(H {h1:.2f}/{h2:.2f}) vs published {pub[0]:.1%}/{pub[1]:.2f}/{pub[2]:.1%} -> {'PASS' if ok else 'FAIL'}")
    rv2 = backtest(px, rules_v2_weights(px, band=BAND, gross=GROSS), cost_bps=10, freq="W")["returns"].loc[start:]
    m = metrics(rv2); h1, h2 = hs(rv2)
    ok = abs(m["CAGR"] - 0.0866) < 0.002 and abs(m["Sharpe"] - 1.2056) < 0.01 and abs(m["MaxDD"] + 0.1205) < 0.002
    print(f"    [0.3] LIVE RULES v2 U56: {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} (H {h1:.4f}/{h2:.4f}) "
          f"vs published 8.66%/1.2056/-12.05% (1.2259/1.1908) -> {'PASS' if ok else 'FAIL'}")

    ref350 = pd.read_csv(I350).set_index(["panel", "form", "cost"]) if I350.exists() else None
    gate4 = {"n": 0, "bad_dates": 0, "max_diff": 0.0}

    # ---------------------------------------------------------- census
    for panel, px in P.items():
        start = px.index[WARMUP]
        E = breadth(px, panel).loc[start:]
        A = armed_series(E)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bw = rules_v2_weights(px[book_cols(px, panel)], band=BAND, gross=GROSS)
        base10 = backtest(px, bw.reindex(columns=px.columns).fillna(0.0),
                          cost_bps=10, freq="W")["returns"].loc[start:]
        print(f"\n[1] {panel}: breadth mean {E.mean():.3f}; realised armed-day share "
              + ", ".join(f"{nm}@q{q:.2f} {float(A[(nm, q)].mean()):.3f}"
                          for nm in ("LEVEL", "SPEED20") for q in QS))
        ov = {q: float((A[("LEVEL", q)] & A[("SPEED20", q)]).sum()
                       / max(1, (A[("LEVEL", q)] | A[("SPEED20", q)]).sum())) for q in QS}
        print(f"    LEVEL vs SPEED20 armed-day Jaccard overlap: "
              + ", ".join(f"q{q:.2f} {v:.3f}" for q, v in ov.items()))

        for form in FORMS:
            res = backtest(px, weights_for(px, panel, form), cost_bps=0, freq="W")
            r0, t0 = res["returns"].loc[start:], res["turnover"].loc[start:]
            for c in COSTS:
                rc = r0 - t0 * c / 1e4
                pk, tr, dep = dd_window(rc)
                mc = metrics(rc)
                num = abs(mc["MaxDD"]) / mc["CAGR"] if mc["CAGR"] > 0 else np.nan

                # ---- gate [0.4]: idea 350's committed window + absolute-B off shares
                if ref350 is not None and (panel, form, c) in ref350.index:
                    ref = ref350.loc[(panel, form, c)]
                    gate4["n"] += 1
                    if str(pk.date()) != ref["peak"] or str(tr.date()) != ref["trough"]:
                        gate4["bad_dates"] += 1
                    for b in ABS_B:
                        mine = off_share(rc, ~((E < b).shift(1).fillna(False).astype(bool)), pk, tr)
                        gate4["max_diff"] = max(gate4["max_diff"], abs(mine - ref[f"neg_share_ge_{b:.2f}"]))

                base_row = dict(panel=panel, form=form, cost=c, CAGR=mc["CAGR"], Sharpe=mc["Sharpe"],
                                MaxDD=mc["MaxDD"], peak=str(pk.date()), trough=str(tr.date()),
                                days=len(rc.loc[pk:tr]), depth_pct=dep,
                                E_window=float(E.loc[pk:tr].mean()), E_panel=float(E.mean()),
                                E_pctile=window_pctile(E, pk, tr), numeraire=num)

                for (nm, q), armed in A.items():
                    offm = ~armed
                    ws = dict(base_row, arm=nm, q=q,
                              armed_frac=float(armed.mean()),
                              armed_frac_window=float(armed.loc[pk:tr].mean()),
                              off_share=off_share(rc, offm, pk, tr),
                              off_share_signed=off_share(rc, offm, pk, tr, signed=True))
                    rows_win.append(ws)

                    for d in DEPTHS:
                        rg = gated(rc, armed, d, c)
                        mg = metrics(rg); h1, h2 = hs(rg)
                        ok_b, fb = bars_4b(rg, spy); ok_a, fa = bars_4a(rg, base10)
                        pk2, tr2, _ = dd_window(rg)
                        dcagr = 100 * (mg["CAGR"] - mc["CAGR"])
                        dddp = 100 * (abs(mc["MaxDD"]) - abs(mg["MaxDD"]))
                        ratio = np.nan if dcagr >= -FREE_EPS else dddp / (-dcagr)
                        rows_grid.append(dict(
                            panel=panel, form=form, cost=c, arm=nm, q=q, depth=d,
                            armed_frac=float(armed.mean()), off_share=ws["off_share"],
                            CAGR=mg["CAGR"], Sharpe=mg["Sharpe"], MaxDD=mg["MaxDD"], H1=h1, H2=h2,
                            IS_Sharpe=metrics(rg.loc[:IS_END])["Sharpe"],
                            OOS_CAGR=metrics(rg.loc[OOS_START:])["CAGR"],
                            OOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"],
                            OOS_MaxDD=metrics(rg.loc[OOS_START:])["MaxDD"],
                            ctrl_CAGR=mc["CAGR"], ctrl_Sharpe=mc["Sharpe"], ctrl_MaxDD=mc["MaxDD"],
                            dCAGR_pp=dcagr, dDD_pp=dddp, dSharpe=mg["Sharpe"] - mc["Sharpe"],
                            ratio=ratio, numeraire=num,
                            beats_numeraire=(not np.isnan(ratio)) and (ratio > num),
                            window_moved=(str(pk2.date()) != str(pk.date()) or str(tr2.date()) != str(tr.date())),
                            new_peak=str(pk2.date()), new_trough=str(tr2.date()),
                            new_off_share=off_share(rg, ~armed, pk2, tr2),
                            pass4a=ok_a, fail4a=",".join(fa), pass4b=ok_b, fail4b=",".join(fb)))

                # ---- rule 8 at 10 bps: three choosers on the same book
                if c == 10:
                    menu = [("OFF", "OFF", np.nan, np.nan, rc)]
                    for (nm, q), armed in A.items():
                        for d in DEPTHS:
                            menu.append((f"{nm}_q{q:.2f}_d{d:.2f}", nm, q, d, gated(rc, armed, d, c)))
                    co = metrics(rc.loc[OOS_START:])
                    rec = dict(panel=panel, form=form,
                               ctrl_OOS_CAGR=co["CAGR"], ctrl_OOS_Sharpe=co["Sharpe"],
                               ctrl_OOS_MaxDD=co["MaxDD"],
                               base_OOS_Sharpe=metrics(base10.loc[OOS_START:])["Sharpe"],
                               spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                               spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                               spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"])
                    for tag, sub in (("ALL", menu),
                                     ("LEVEL", [x for x in menu if x[1] in ("OFF", "LEVEL")]),
                                     ("SPEED", [x for x in menu if x[1] != "LEVEL"])):
                        pick = max(sub, key=lambda x: metrics(x[4].loc[:IS_END])["Sharpe"])
                        oos = [(metrics(x[4].loc[OOS_START:])["Sharpe"], x[0]) for x in sub]
                        bo = max(oos, key=lambda z: z[0])
                        po = metrics(pick[4].loc[OOS_START:])
                        rec.update({f"{tag}_pick": pick[0],
                                    f"{tag}_IS_Sharpe": metrics(pick[4].loc[:IS_END])["Sharpe"],
                                    f"{tag}_OOS_CAGR": po["CAGR"], f"{tag}_OOS_Sharpe": po["Sharpe"],
                                    f"{tag}_OOS_MaxDD": po["MaxDD"],
                                    f"{tag}_best_OOS": bo[1], f"{tag}_best_OOS_Sharpe": bo[0],
                                    f"{tag}_regret": bo[0] - po["Sharpe"]})
                    wf.append(rec)
            print(f"    {panel:9s} {form:8s} stamped; 10bps window {base_row['peak']}->{base_row['trough']} "
                  f"off_share LEVEL@q0.20 {fmt([r for r in rows_win if r['form']==form and r['cost']==10 and r['arm']=='LEVEL' and r['q']==0.20][-1]['off_share'])} "
                  f"SPEED20@q0.20 {fmt([r for r in rows_win if r['form']==form and r['cost']==10 and r['arm']=='SPEED20' and r['q']==0.20][-1]['off_share'])}")

    print(f"\n    [0.4] idea 350 windows.csv cross-check on {gate4['n']} books: "
          f"peak/trough mismatches {gate4['bad_dates']}, max |neg_share diff| {gate4['max_diff']:.3e} "
          f"-> {'PASS' if gate4['bad_dates'] == 0 and gate4['max_diff'] < 1e-6 else 'FAIL'}")

    W, G, F = pd.DataFrame(rows_win), pd.DataFrame(rows_grid), pd.DataFrame(wf)
    W.to_csv(OUT / f"{SLUG}.windows.csv", index=False)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    F.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    return W, G, F


def analyse(W, G, F):
    print("\n[2] DOES THE LOSS-SHARE STATISTIC MOVE?  off_share = share of the CONTROL book's")
    print("    binding-window down-day loss booked while the gate is OFF (1.0 = unreachable).")
    print("    Idea 350's committed reference at fixed B=0.30 is a median of 0.793 over 54 books.")
    hdr = f"    {'arm':9s} " + " ".join(f"{'q='+format(q,'.2f'):>26s}" for q in QS)
    print(hdr)
    for nm in ["LEVEL"] + [f"SPEED{L}" for L in LOOKBACKS]:
        cells = []
        for q in QS:
            s = W[(W.arm == nm) & (W.q == q)]["off_share"].dropna()
            cells.append(f"med {s.median():.3f} n>=.9 {int((s >= 0.90).sum()):2d}/{len(s)}")
        print(f"    {nm:9s} " + " ".join(f"{c:>26s}" for c in cells))
    print("\n    head-to-head at MATCHED (book, rung, q): SPEED off_share BELOW LEVEL's in")
    piv = W.pivot_table(index=["panel", "form", "cost", "q"], columns="arm", values="off_share")
    for L in LOOKBACKS:
        col = f"SPEED{L}"
        d = piv[[col, "LEVEL"]].dropna()
        print(f"      {col:8s} {int((d[col] < d['LEVEL']).sum()):3d}/{len(d)} points, "
              f"median difference {float((d[col] - d['LEVEL']).median()):+.3f} "
              f"(negative = the speed trigger reaches more of the loss)")
    print("\n    by panel (SPEED20 - LEVEL, median off_share difference): "
          + ", ".join(f"{p} {float((piv.xs(p, level='panel')['SPEED20'] - piv.xs(p, level='panel')['LEVEL']).median()):+.3f}"
                      for p in W.panel.unique()))
    print("    armed-day frequency actually realised (should match q for both families): "
          + ", ".join(f"q{q:.2f} LEVEL {W[(W.arm=='LEVEL')&(W.q==q)].armed_frac.mean():.3f} / "
                      f"SPEED20 {W[(W.arm=='SPEED20')&(W.q==q)].armed_frac.mean():.3f}" for q in QS))
    print("    share of the binding WINDOW's days armed: "
          + ", ".join(f"q{q:.2f} LEVEL {W[(W.arm=='LEVEL')&(W.q==q)].armed_frac_window.median():.3f} / "
                      f"SPEED20 {W[(W.arm=='SPEED20')&(W.q==q)].armed_frac_window.median():.3f}" for q in QS))

    print(f"\n[3] THE OVERLAY GRID -- all {len(G)} points (4 arms x 3 q x 2 depths x 54 books)")
    print(f"    {'arm':9s} {'q':>5s} {'depth':>6s} {'dDD_pp':>9s} {'dCAGR_pp':>9s} {'dSharpe':>9s} "
          f"{'dSh>0':>8s} {'numeraire':>10s} {'4a':>6s} {'4b':>6s}")
    for nm in ["LEVEL"] + [f"SPEED{L}" for L in LOOKBACKS]:
        for q in QS:
            for d in DEPTHS:
                g = G[(G.arm == nm) & (G.q == q) & (G.depth == d)]
                print(f"    {nm:9s} {q:5.2f} {d:6.2f} {g.dDD_pp.median():+9.3f} {g.dCAGR_pp.median():+9.3f} "
                      f"{g.dSharpe.median():+9.4f} {int((g.dSharpe > 0).sum()):4d}/{len(g)} "
                      f"{int(g.beats_numeraire.sum()):5d}/{len(g)} {int(g.pass4a.sum()):3d}/{len(g)} "
                      f"{int(g.pass4b.sum()):3d}/{len(g)}")
    print(f"\n    TOTALS: 4a {int(G.pass4a.sum())}/{len(G)}, 4b {int(G.pass4b.sum())}/{len(G)}; "
          f"beats numeraire {int(G.beats_numeraire.sum())}/{len(G)}")
    print("    4b failing bars: " + ", ".join(
        f"{k} {int(G.fail4b.fillna('').str.contains(k).sum())}" for k in ["H1", "H2", "OOS", "DD", "CAGR"]))
    if G.pass4b.any():
        print(G[G.pass4b][["panel", "form", "cost", "arm", "q", "depth", "CAGR", "Sharpe", "MaxDD",
                           "H1", "H2", "OOS_Sharpe", "dDD_pp", "dSharpe", "beats_numeraire"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n[3b] SPEED vs LEVEL head-to-head on the SAME book at matched (q, depth, rung)")
    pv = G.pivot_table(index=["panel", "form", "cost", "q", "depth"], columns="arm",
                       values=["dDD_pp", "dSharpe", "dCAGR_pp"])
    for L in LOOKBACKS:
        c = f"SPEED{L}"
        dd = pv["dDD_pp"][[c, "LEVEL"]].dropna(); sh = pv["dSharpe"][[c, "LEVEL"]].dropna()
        cg = pv["dCAGR_pp"][[c, "LEVEL"]].dropna()
        print(f"    {c:8s} dDD better {int((dd[c] > dd['LEVEL']).sum()):3d}/{len(dd)} "
              f"(median diff {float((dd[c] - dd['LEVEL']).median()):+.3f} pp) | "
              f"dSharpe better {int((sh[c] > sh['LEVEL']).sum()):3d}/{len(sh)} "
              f"(median {float((sh[c] - sh['LEVEL']).median()):+.4f}) | "
              f"dCAGR {float((cg[c] - cg['LEVEL']).median()):+.3f} pp")

    print("\n[3c] IS THE off_share STATISTIC STILL PREDICTIVE OF dDD?  (idea 350: -0.53/-0.55/-0.40)")
    for nm in ["LEVEL"] + [f"SPEED{L}" for L in LOOKBACKS]:
        cells = []
        for q in QS:
            g = G[(G.arm == nm) & (G.q == q)]
            cells.append(f"q{q:.2f} {spearman(g.off_share, g.dDD_pp):+.3f}")
        print(f"    Spearman(off_share, dDD_pp)  {nm:9s} " + "  ".join(cells))

    print("\n[4] RULE 8 WALK-FORWARD (IS <= 2016 Sharpe picks the cell; 2017-2026 read once, 10 bps)")
    cols = ["panel", "form", "ALL_pick", "ALL_OOS_Sharpe", "LEVEL_pick", "LEVEL_OOS_Sharpe",
            "SPEED_pick", "SPEED_OOS_Sharpe", "ctrl_OOS_Sharpe", "spy_OOS_Sharpe", "base_OOS_Sharpe"]
    print(F[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for tag in ("ALL", "LEVEL", "SPEED"):
        p, s, dd = F[f"{tag}_pick"], F[f"{tag}_OOS_Sharpe"], F[f"{tag}_OOS_MaxDD"]
        print(f"\n    [{tag:5s}] chooser takes a gate in {int((p != 'OFF').sum())}/{len(F)} books; "
              f"OOS Sharpe > own control in {int((s > F.ctrl_OOS_Sharpe).sum())}/{len(F)} "
              f"(median d {float((s - F.ctrl_OOS_Sharpe).median()):+.4f}); "
              f"OOS MaxDD better in {int((dd.abs() < F.ctrl_OOS_MaxDD.abs()).sum())}/{len(F)} "
              f"(median {float(100 * (F.ctrl_OOS_MaxDD.abs() - dd.abs()).median()):+.3f} pp)")
        print(f"            OOS Sharpe > SPY in {int((s > F.spy_OOS_Sharpe).sum())}/{len(F)}; "
              f"> RULES v2 OOS in {int((s > F.base_OOS_Sharpe).sum())}/{len(F)}; "
              f"median regret {F[f'{tag}_regret'].median():.4f}; "
              f"median OOS CAGR {F[f'{tag}_OOS_CAGR'].median():.2%}")
    print(f"\n    SPEED chooser beats LEVEL chooser out of sample in "
          f"{int((F.SPEED_OOS_Sharpe > F.LEVEL_OOS_Sharpe).sum())}/{len(F)} books "
          f"(median difference {float((F.SPEED_OOS_Sharpe - F.LEVEL_OOS_Sharpe).median()):+.4f} Sharpe); "
          f"OOS MaxDD better in {int((F.SPEED_OOS_MaxDD.abs() < F.LEVEL_OOS_MaxDD.abs()).sum())}/{len(F)}")


def main():
    print(f"=== {SLUG}")
    print("Q: does a breadth-SPEED trigger reach the loss a breadth-LEVEL trigger misses,")
    print("   at MATCHED armed-day frequency, on idea 350's own 54 books?")
    print(f"Tuned: lookback L in {LOOKBACKS} x arming quantile q in {QS}.")
    print(f"Reported axes: arm family (LEVEL + {len(LOOKBACKS)} speeds) x depth {DEPTHS} x "
          f"{len(FORMS)} forms x 3 panels x {COSTS} bps.")
    paths = [OUT / f"{SLUG}.{k}.csv" for k in ("windows", "grid", "walkforward")]
    if RESUME and all(p.exists() for p in paths):
        analyse(*[pd.read_csv(p) for p in paths])
        return
    analyse(*build())


if __name__ == "__main__":
    main()

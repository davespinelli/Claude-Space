#!/usr/bin/env python3
"""Idea 375: is the LOSS-SHARE statistic a usable PRE-SCREEN for gate ideas?

Idea 350 measured, IN ITS OWN CORPUS, Spearman(neg_share_ge_B, dMaxDD) = -0.53 / -0.55 / -0.40
at B = 0.30 / 0.40 / 0.50 over 486 gated points, and proposed the statistic as a cheap ranker:
compute, on a book you have NOT gated, the share of its binding drawdown's down-day loss taken
while breadth was still ABOVE the gate threshold; a high share means an overlay armed below B
is structurally incapable of touching the episode.  An in-corpus correlation is not a screen.
This run tests it OUT OF CORPUS.

DESIGN (fit on idea 350's books, score on books it never gated)
  IN  = idea 350's 6 canonical forms  EWALL / TOP3 / TOP10 / TOP20 / MAEW / RULESV2
  OUT = 8 forms idea 350 never gated, chosen to span shapes its set does not reach:
          TOP5, TOP40        - the count dial either side of its TOP3/TOP10/TOP20 rungs
          IVOL               - inverse-vol weights over ALL priced names, no filter
          LOWVOL20           - the 20 LOWEST-vol admitted names (risk-ranked, not momentum)
          MOM20              - top-20 by raw 12-1 momentum only (no composite, no vol scale)
          MAEW_RS            - MAEW's gate RESPREAD (gross pinned) instead of de-grossed to cash
          V2B12              - RULES v2 with a 12% hysteresis band instead of 3%
          EWALL_M            - EWALL at MONTHLY cadence
  Both sets: 3 panels (U56 / B136 / SMALL439) x 3 cost rungs (0/10/25 bps) x the gate dial.
  IN 54 controls x 9 cells = 486 points (idea 350's grid, rebuilt from source, not re-read);
  OUT 72 controls x 9 cells = 648 points.  Every point is written to the CSVs.

  TUNED PARAMETERS -- exactly two, idea 350's own dial, unchanged and NOT re-picked here:
     1. breadth threshold B in {0.30, 0.40, 0.50}
     2. gate depth d in {0.25, 0.50, 1.00}   (fraction of gross moved to CASH while armed)
  Reported, not tuned: book form (14), panel (3), cost rung (3), predictor (4).

THE FOUR PREDICTORS ARE PRE-REGISTERED -- written down and fixed before any OUT number was
read.  Each predicts dDD_pp = (|ctrl MaxDD| - |gated MaxDD|) * 100, positive = the gate helped:
     A NAIVE      pred = mean(dDD_pp) over the IN corpus.  The do-nothing control every other
                  predictor has to beat; a screen with no skill scores exactly this.
     B SHARE      OLS dDD_pp ~ 1 + neg_share, fitted on IN, applied to OUT.  The literal
                  reading of idea 350's headline correlation.
     C SHARExD    OLS dDD_pp ~ 1 + neg_share + d + neg_share*d, fitted on IN.  The gate's own
                  depth is known before the backtest too, so a fair screen may use it.
     D BOUND      pred = d * (1 - neg_share) * |ctrl MaxDD| * 100.  ZERO fitted parameters:
                  the mechanical ceiling implied by idea 350's argument -- the deepest cut a
                  gate of depth d could make if it removed the whole addressable share of the
                  episode and nothing else moved.
  SCORED on OUT by: Spearman(pred, actual), sign accuracy, MAE, RMSE, and the skill score
  1 - MAE/MAE_naive (>0 = beats predicting the corpus mean).  A screen that cannot beat A is
  not a screen.

RULE 8 runs TWICE, because this idea has two things to walk forward:
  (a) THE BOOK: for every (panel, form, rung) the (B,d) menu -- gate-OFF INCLUDED -- is chosen
      on 2008-2016 by IS Sharpe and 2017-2026 is read ONCE against the do-nothing control, the
      OOS-best cell (regret), the LIVE RULES v2 book and SPY.
  (b) THE SCREEN: predictors B/C/D are re-fitted on IS-WINDOW drawdowns only (each control's
      binding episode INSIDE 2008-2016, its own neg_share, its own dDD) and scored on the
      OOS-WINDOW episodes (2017-2026), in corpus AND out of corpus.  A statistic that only
      ranks inside the window it was fitted on is a description, not a screen.

BOTH KEEP PATHS are evaluated at every one of the 1134 overlay points and 126 controls:
4a against the LIVE RULES v2 book on the same panel, 4b against SPY (Sharpe > SPY in both
halves AND OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70% of SPY's).

CONVENTIONS carried verbatim from idea 350 so the two corpora are comparable:
  * breadth E_t = share of the panel's own priced names (SPY always excluded) above their own
    200d MA; the gate reads E_{t-1}, so the switch executes at t+1 (protocol 2);
  * a gated path is built from the control's rung path as rg = mult*rc - |d mult|*GROSS*c/1e4
    with mult = 1-d while armed.  This is idea 350's overlay convention: the multiplier scales
    the control's ALREADY-COSTED path, so the arm re-scales the control's own cost by mult as
    well as its return.  It is kept here EXACTLY (an "improved" convention would make the two
    corpora incomparable and would break the reproduction gate below), and the resulting
    overstatement is bounded by mult*turnover*c/1e4 <= 0.25*turnover*25/1e4;
  * costs are derived, r(c) = r(0) - turnover*c/1e4, asserted against a live backtest;
  * gross 0.75, vol cap 0.60, weekly cadence except EWALL_M, 260-bar warm-up.

REPRODUCTION GATES (section [0], run and PRINTED before any new number is read):
  * derived rung identity vs engine.backtest(cost_bps=25) to 1e-12;
  * idea 40/41's published U56 controls: TOP3 21.9%/1.04/-25.8% (H1 1.01 / H2 1.06),
    TOP5 16.5%/0.95/-21.6%;
  * the LIVE RULES v2 U56 row 8.66%/1.2056/-12.05% (halves 1.2259/1.1908);
  * idea 350's COMMITTED grid.csv and windows.csv: this run rebuilds all 486 of its overlay
    points and all 54 of its windows from source and prints max|diff| on dDD_pp, dCAGR_pp,
    neg_share and the window dates.  Its published Spearman -0.53/-0.55/-0.40 is re-derived
    from the rebuild, not copied.
  Published-number gates are REPORTED as PASS/FAIL with the miss, never asserted away.

CAVEATS.  (1) All three panels are CURRENT-CONSTITUENT lists -- SURVIVORSHIP -- so drawdown
LEVELS and CAGRs are optimistic and 4b's DD cap and CAGR floor are read against an inflated
book; the loss share is a within-window decomposition and the predictor scores are rank/error
statistics over books that all share the bias, so the SCREEN result is the more robust half of
this run and the KEEP verdicts the weaker.  SMALL439 additionally drops the 44 tickers with
max_1d_move >= 1.0 from data/small_meta.csv and starts 2010-01-04, so its halves are not the
same calendar halves as U56/B136.  (2) "Out of corpus" here means outside IDEA 350's six
forms; the record at large has gated top-n books at other n, so TOP5/TOP40 are the weakest two
OUT rows and every score below is reported with and without them.  (3) The sample starts 2008
with a 260-bar warm-up, so the binding episode is 2020 or 2022 for most books, not the GFC --
the OUT set inherits that concentration and the OOS-window scores rest largely on ONE episode
per control.  (4) Breadth on a 200d MA is a lagging statistic by construction; that is the
hypothesis, not a defect.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                            # noqa
from engine import backtest, metrics                                                   # noqa

SLUG = "2026-09-07_is-the-LOSS-SHARE-statistic-a-usable-PRE-SCREEN-for-gate-ideas_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, BAND = 0.60, 0.75, 0.03
BS = [0.30, 0.40, 0.50]                          # tuned parameter 1 (idea 350's, unchanged)
DEPTHS = [0.25, 0.50, 1.00]                      # tuned parameter 2 (idea 350's, unchanged)
COSTS = [0, 10, 25]
IN_FORMS = ["EWALL", "TOP3", "TOP10", "TOP20", "MAEW", "RULESV2"]
OUT_FORMS = ["TOP5", "TOP40", "IVOL", "LOWVOL20", "MOM20", "MAEW_RS", "V2B12", "EWALL_M"]
WEAK_OUT = {"TOP5", "TOP40"}                     # count dial: nearest to idea 350's own set
FREQ = {"EWALL_M": "M"}                          # everything else weekly
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260

_tee = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _tee.append(s)


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    say(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def panels():
    p = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    for k, v in p.items():
        say(f"    {k}: {v.shape[1]} cols, {v.index[0].date()} .. {v.index[-1].date()}")
    return p


def book_cols(px, panel):
    """Columns a BOOK may hold.  SPY is a constituent of U56/B136, benchmark-only on SMALL."""
    return [c for c in px.columns if not (panel == "SMALL439" and c == "SPY")]


def breadth(px, panel):
    cols = [c for c in px.columns if c != "SPY"]
    q = px[cols]
    above = q > q.rolling(200).mean()
    priced = q.notna() & q.rolling(200).mean().notna()
    return (above & priced).sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)


# ---------------------------------------------------------------- book forms
def _topn(q, n):
    s = score(q, vol_scale=False)[0]
    _, above, vol20 = score(q)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def weights_for(px, panel, form):
    """IN forms are idea 350's verbatim; OUT forms are new to this run."""
    cols = book_cols(px, panel)
    q = px[cols]
    if form == "EWALL" or form == "EWALL_M":
        e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
        w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif form.startswith("TOP"):
        w = _topn(q, int(form[3:]))
    elif form == "MAEW":                                   # de-gross: gated weight -> CASH
        above = q > q.rolling(200).mean()
        e = above.astype(float).where(q.notna(), 0.0)
        w = GROSS * e.div(q.notna().sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif form == "MAEW_RS":                                # RESPREAD: gross pinned at GROSS
        above = q > q.rolling(200).mean()
        e = above.astype(float).where(q.notna(), 0.0)
        w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif form == "RULESV2":
        w = rules_v2_weights(q, band=BAND, gross=GROSS)
    elif form == "V2B12":
        w = rules_v2_weights(q, band=0.12, gross=GROSS)
    elif form == "IVOL":
        vol20 = q.pct_change().rolling(20).std() * np.sqrt(252)
        iv = (1.0 / vol20.clip(lower=0.08)).where(q.notna() & vol20.notna())
        w = GROSS * iv.div(iv.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif form == "LOWVOL20":
        above = q > q.rolling(200).mean()
        vol20 = q.pct_change().rolling(20).std() * np.sqrt(252)
        rank = vol20.where(above & q.notna()).rank(axis=1, ascending=True)
        w = (rank <= 20).astype(float) * (GROSS / 20)
    elif form == "MOM20":
        mom = q.shift(21) / q.shift(252) - 1
        rank = mom.where(q.notna()).rank(axis=1, ascending=False)
        w = (rank <= 20).astype(float) * (GROSS / 20)
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


def neg_share(r, E, peak, trough, B):
    """Share of the window's GROSS down-day log loss taken while E_{t-1} >= B (gate DISARMED).
    1.0 => an overlay armed below B cannot touch any of the episode."""
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


def loss_share(r, E, peak, trough, B):
    seg = r.loc[peak:trough].iloc[1:]
    if len(seg) == 0:
        return np.nan
    lg = np.log1p(seg.clip(lower=-0.9999))
    tot = lg.sum()
    if tot >= 0:
        return np.nan
    e = E.shift(1).reindex(seg.index)
    return float(lg.where(e >= B, 0.0).sum() / tot)


def window_pctile(E, peak, trough):
    n = len(E.loc[peak:trough])
    if n < 2:
        return np.nan
    roll = E.rolling(n).mean().dropna()
    return float((roll <= float(E.loc[peak:trough].mean())).mean())


def gate_path(rc, E, B, d, c):
    """idea 350's overlay convention, verbatim."""
    armed = (E < B).shift(1).fillna(False).reindex(rc.index).fillna(False)
    mult = pd.Series(np.where(armed.values, 1.0 - d, 1.0), index=rc.index)
    dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))
    return pd.Series(mult.values * rc.values - dm * GROSS * c / 1e4, index=rc.index)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    rx = pd.Series(x[m]).rank().values; ry = pd.Series(y[m]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def ols(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float)
    m = np.isfinite(y) & np.isfinite(X).all(axis=1)
    return np.linalg.lstsq(X[m], y[m], rcond=None)[0]


# ---------------------------------------------------------------- run
def build():
    P = panels()

    # ---------------------------------------------------------- [0] reproduction gates
    say("\n[0] REPRODUCTION GATES")
    px = P["U56"]
    w = weights_for(px, "U56", "TOP3")
    b0 = backtest(px, w, cost_bps=0, freq="W")
    b25 = backtest(px, w, cost_bps=25, freq="W")
    gid = float(np.abs((b0["returns"] - b0["turnover"] * 25 / 1e4) - b25["returns"]).max())
    say(f"    derived rung identity max|diff| = {gid:.3e}  ({'PASS' if gid < 1e-12 else 'FAIL'})")
    assert gid < 1e-12

    start = px.index[WARMUP]
    for n, pub in ((3, (0.219, 1.04, -0.258)), (5, (0.165, 0.95, -0.216))):
        r = backtest(px, weights_for(px, "U56", f"TOP{n}"), cost_bps=10, freq="W")["returns"].loc[start:]
        m = metrics(r); h1, h2 = hs(r)
        ok = abs(m["CAGR"] - pub[0]) < 0.005 and abs(m["Sharpe"] - pub[1]) < 0.02 and abs(m["MaxDD"] - pub[2]) < 0.005
        say(f"    idea 40/41 U56 TOP{n}: {m['CAGR']:.1%}/{m['Sharpe']:.2f}/{m['MaxDD']:.1%} (H {h1:.2f}/{h2:.2f})"
            f" vs published {pub[0]:.1%}/{pub[1]:.2f}/{pub[2]:.1%} -> {'PASS' if ok else 'FAIL'}")
    rv2 = backtest(px, rules_v2_weights(px, band=BAND, gross=GROSS), cost_bps=10, freq="W")["returns"].loc[start:]
    m = metrics(rv2); h1, h2 = hs(rv2)
    ok = abs(m["CAGR"] - 0.0866) < 0.002 and abs(m["Sharpe"] - 1.2056) < 0.01 and abs(m["MaxDD"] + 0.1205) < 0.002
    say(f"    LIVE RULES v2 U56: {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} (H {h1:.4f}/{h2:.4f})"
        f" vs published 8.66%/1.2056/-12.05% (1.2259/1.1908) -> {'PASS' if ok else 'FAIL'}")

    # ---------------------------------------------------------- corpus build (IN then OUT)
    rows, wins, wf = [], [], []
    for tag, forms in (("IN", IN_FORMS), ("OUT", OUT_FORMS)):
        for panel, px in P.items():
            start = px.index[WARMUP]
            E = breadth(px, panel).loc[start:]
            spy = px["SPY"].pct_change().fillna(0).loc[start:]
            bw = rules_v2_weights(px[book_cols(px, panel)], band=BAND, gross=GROSS)
            live = backtest(px, bw.reindex(columns=px.columns).fillna(0.0),
                            cost_bps=10, freq="W")["returns"].loc[start:]
            for form in forms:
                res = backtest(px, weights_for(px, panel, form), cost_bps=0, freq=FREQ.get(form, "W"))
                r0, t0 = res["returns"].loc[start:], res["turnover"].loc[start:]
                for c in COSTS:
                    rc = r0 - t0 * c / 1e4
                    mc = metrics(rc); ch1, ch2 = hs(rc)
                    pk, tr, dep = dd_window(rc)
                    stat = {b: neg_share(rc, E, pk, tr, b) for b in BS}
                    lsh = {b: loss_share(rc, E, pk, tr, b) for b in BS}
                    num = abs(mc["MaxDD"]) / mc["CAGR"] if mc["CAGR"] > 0 else np.nan
                    p4a, f4a = bars_4a(rc, live); p4b, f4b = bars_4b(rc, spy)
                    # per-window (rule 8b) control episodes
                    win = {}
                    for wname, seg in (("IS", rc.loc[:IS_END]), ("OOS", rc.loc[OOS_START:])):
                        if len(seg) < 60:
                            win[wname] = None; continue
                        p2, t2, d2 = dd_window(seg)
                        win[wname] = (p2, t2, d2, {b: neg_share(seg, E, p2, t2, b) for b in BS})
                    wins.append(dict(set=tag, panel=panel, form=form, cost=c, CAGR=mc["CAGR"],
                                     Sharpe=mc["Sharpe"], MaxDD=mc["MaxDD"], H1=ch1, H2=ch2,
                                     peak=pk.date(), trough=tr.date(),
                                     days=len(rc.loc[pk:tr]), E_window=float(E.loc[pk:tr].mean()),
                                     E_panel=float(E.mean()), E_pctile=window_pctile(E, pk, tr),
                                     numeraire=num, ctrl_4a=p4a, ctrl_4b=p4b,
                                     **{f"neg_share_ge_{b:.2f}": stat[b] for b in BS},
                                     **{f"loss_share_ge_{b:.2f}": lsh[b] for b in BS},
                                     IS_MaxDD=(win["IS"][2] if win["IS"] else np.nan),
                                     OOS_MaxDD=(win["OOS"][2] if win["OOS"] else np.nan)))
                    for b in BS:
                        for d in DEPTHS:
                            rg = gate_path(rc, E, b, d, c)
                            mg = metrics(rg); h1, h2 = hs(rg)
                            dDD = (abs(mc["MaxDD"]) - abs(mg["MaxDD"])) * 100
                            dCA = (mg["CAGR"] - mc["CAGR"]) * 100
                            ratio = dDD / -dCA if dCA < 0 else np.inf
                            g4a, gf4a = bars_4a(rg, live); g4b, gf4b = bars_4b(rg, spy)
                            row = dict(set=tag, panel=panel, form=form, cost=c, B=b, depth=d,
                                       CAGR=mg["CAGR"], Sharpe=mg["Sharpe"], MaxDD=mg["MaxDD"],
                                       H1=h1, H2=h2,
                                       IS_Sharpe=metrics(rg.loc[:IS_END])["Sharpe"],
                                       OOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"],
                                       OOS_CAGR=metrics(rg.loc[OOS_START:])["CAGR"],
                                       ctrl_CAGR=mc["CAGR"], ctrl_Sharpe=mc["Sharpe"],
                                       ctrl_MaxDD=mc["MaxDD"], dCAGR_pp=dCA, dDD_pp=dDD,
                                       dSharpe=mg["Sharpe"] - mc["Sharpe"], ratio=ratio,
                                       numeraire=num, beats_numeraire=bool(ratio > num),
                                       neg_share=stat[b], loss_share=lsh[b],
                                       pass4a=g4a, fail4a=",".join(gf4a),
                                       pass4b=g4b, fail4b=",".join(gf4b))
                            for wname in ("IS", "OOS"):
                                if win[wname] is None:
                                    row[f"{wname}_dDD_pp"] = np.nan; row[f"{wname}_neg_share"] = np.nan
                                    continue
                                p2, t2, d2, s2 = win[wname]
                                seg = rg.loc[:IS_END] if wname == "IS" else rg.loc[OOS_START:]
                                row[f"{wname}_dDD_pp"] = (abs(d2) - abs(dd_window(seg)[2])) * 100
                                row[f"{wname}_neg_share"] = s2[b]
                                row[f"{wname}_ctrl_MaxDD"] = d2
                            rows.append(row)
                    # ------ rule 8a: menu incl. gate-OFF chosen on IS by IS Sharpe
                    if c == 10:
                        menu = [("OFF", np.nan, np.nan, rc)]
                        menu += [(f"B{b:.2f}_d{d:.2f}", b, d, gate_path(rc, E, b, d, c))
                                 for b in BS for d in DEPTHS]
                        iss = [(metrics(x[3].loc[:IS_END])["Sharpe"], x) for x in menu]
                        pick = max(iss, key=lambda z: z[0])[1]
                        oos = {k: metrics(v[3].loc[OOS_START:])["Sharpe"] for k, v in
                               ((x[0], x) for x in menu)}
                        best = max(oos, key=oos.get)
                        po = metrics(pick[3].loc[OOS_START:])
                        wf.append(dict(set=tag, panel=panel, form=form, IS_pick=pick[0],
                                       IS_Sharpe=metrics(pick[3].loc[:IS_END])["Sharpe"],
                                       OOS_CAGR=po["CAGR"], OOS_Sharpe=po["Sharpe"],
                                       OOS_MaxDD=po["MaxDD"],
                                       ctrl_OOS_Sharpe=oos["OFF"], best_cell=best,
                                       best_OOS_Sharpe=oos[best],
                                       regret=oos["OFF"] - po["Sharpe"],
                                       regret_vs_best=oos[best] - po["Sharpe"],
                                       live_OOS_Sharpe=metrics(live.loc[OOS_START:])["Sharpe"],
                                       spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                                       picked_gate=pick[0] != "OFF"))
                say(f"    [{tag}] {panel} {form}: control MaxDD "
                    + ", ".join(f"{c}bps {wins[-3+i]['MaxDD']:.1%}" for i, c in enumerate(COSTS)))

    G = pd.DataFrame(rows); W = pd.DataFrame(wins); WF = pd.DataFrame(wf)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    W.to_csv(OUT / f"{SLUG}.windows.csv", index=False)
    WF.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    return P, G, W, WF


# ---------------------------------------------------------------- [1] gate on idea 350
def gate_on_parent(G, W):
    say("\n[1] REPRODUCTION OF IDEA 350's COMMITTED CORPUS (rebuilt from source, not re-read)")
    pg = OUT / "2026-09-07_is-the-BINDING-DRAWDOWN-EPISODE-a-HIGH-BREADTH-event_C.grid.csv"
    pw = OUT / "2026-09-07_is-the-BINDING-DRAWDOWN-EPISODE-a-HIGH-BREADTH-event_C.windows.csv"
    if not pg.exists():
        say("    parent CSVs absent -- gate SKIPPED (reported, not asserted)"); return
    A = pd.read_csv(pg); B = G[G["set"] == "IN"]
    k = ["panel", "form", "cost", "B", "depth"]
    M = A.merge(B, on=k, suffixes=("_p", "_n"))
    say(f"    matched {len(M)} of {len(A)} parent grid rows")
    for col in ("dDD_pp", "dCAGR_pp", "CAGR", "Sharpe", "MaxDD", "dSharpe"):
        d = float(np.abs(M[f"{col}_p"] - M[f"{col}_n"]).max())
        say(f"      max|d {col}| = {d:.3e}  ({'PASS' if d < 1e-9 else 'FAIL'})")
    AW = pd.read_csv(pw); BW = W[W["set"] == "IN"]
    MW = AW.merge(BW, on=["panel", "form", "cost"], suffixes=("_p", "_n"))
    same = int((MW["peak_p"].astype(str) == MW["peak_n"].astype(str)).sum())
    say(f"    windows: {same}/{len(MW)} peak dates identical, "
        f"{int((MW['trough_p'].astype(str) == MW['trough_n'].astype(str)).sum())}/{len(MW)} troughs")
    for b in BS:
        d = float(np.abs(MW[f"neg_share_ge_{b:.2f}_p"] - MW[f"neg_share_ge_{b:.2f}_n"]).max())
        say(f"      max|d neg_share_ge_{b:.2f}| = {d:.3e}  ({'PASS' if d < 1e-9 else 'FAIL'})")
    say("    idea 350's published Spearman(neg_share, dMaxDD), RE-DERIVED from this rebuild:")
    for b in BS:
        s = B[B["B"] == b]
        say(f"      B={b:.2f}: {spearman(s['neg_share'], s['dDD_pp']):+.3f} over {len(s)} points"
            f"   (published {-0.53 if b == 0.30 else -0.55 if b == 0.40 else -0.40:+.2f})")


# ---------------------------------------------------------------- [2] the screen, out of corpus
def score_screen(G):
    IN, OU = G[G["set"] == "IN"], G[G["set"] == "OUT"]
    say(f"\n[2] THE SCREEN OUT OF CORPUS  (fit on {len(IN)} IN points, scored on {len(OU)} OUT points)")

    def fit(df):
        f = {}
        f["A"] = float(np.nanmean(df["dDD_pp"]))
        f["B"] = ols(np.c_[np.ones(len(df)), df["neg_share"]], df["dDD_pp"])
        f["C"] = ols(np.c_[np.ones(len(df)), df["neg_share"], df["depth"],
                           df["neg_share"] * df["depth"]], df["dDD_pp"])
        return f

    def predict(f, df):
        ns, dp = df["neg_share"].values, df["depth"].values
        return {"A_NAIVE": np.full(len(df), f["A"]),
                "B_SHARE": f["B"][0] + f["B"][1] * ns,
                "C_SHARExD": f["C"][0] + f["C"][1] * ns + f["C"][2] * dp + f["C"][3] * ns * dp,
                "D_BOUND": dp * (1 - ns) * np.abs(df["ctrl_MaxDD"].values) * 100}

    f = fit(IN)
    say(f"    fitted on IN: A mean dDD = {f['A']:+.4f} pp;"
        f"  B: dDD = {f['B'][0]:+.4f} {f['B'][1]:+.4f}*share;"
        f"  C: {f['C'][0]:+.4f} {f['C'][1]:+.4f}*share {f['C'][2]:+.4f}*d {f['C'][3]:+.4f}*share*d")
    say("    (D_BOUND has no fitted parameters)")

    out_rows = []
    subsets = [("OUT all", OU), ("OUT minus TOP5/TOP40", OU[~OU["form"].isin(WEAK_OUT)]),
               ("IN (in-corpus, for reference)", IN)]
    for pan in sorted(G["panel"].unique()):
        subsets.append((f"OUT {pan}", OU[OU["panel"] == pan]))
    for b in BS:
        subsets.append((f"OUT B={b:.2f}", OU[OU["B"] == b]))
    for lbl, S in subsets:
        if len(S) == 0:
            continue
        pr = predict(f, S); act = S["dDD_pp"].values
        mae_n = float(np.nanmean(np.abs(act - pr["A_NAIVE"])))
        for pname, p in pr.items():
            mae = float(np.nanmean(np.abs(act - p)))
            rmse = float(np.sqrt(np.nanmean((act - p) ** 2)))
            sgn = float(np.nanmean(np.sign(p) == np.sign(act)))
            out_rows.append(dict(subset=lbl, n=len(S), predictor=pname,
                                 spearman=spearman(p, act), sign_acc=sgn, MAE=mae, RMSE=rmse,
                                 skill_vs_naive=(1 - mae / mae_n) if mae_n > 0 else np.nan,
                                 mean_pred=float(np.nanmean(p)), mean_act=float(np.nanmean(act))))
    R = pd.DataFrame(out_rows)
    for lbl in R["subset"].unique():
        s = R[R["subset"] == lbl]
        say(f"    {lbl}  (n={s['n'].iloc[0]}, mean actual dDD {s['mean_act'].iloc[0]:+.3f} pp)")
        for _, x in s.iterrows():
            say(f"       {x['predictor']:<10} rho {x['spearman']:+.3f}  sign {x['sign_acc']:.3f}"
                f"  MAE {x['MAE']:.3f}  RMSE {x['RMSE']:.3f}  skill {x['skill_vs_naive']:+.3f}")
    say("\n    per-form OUT detail (rho / sign / skill of the best fitted predictor B_SHARE):")
    frows = []
    for form in OUT_FORMS:
        S = OU[OU["form"] == form]
        pr = predict(f, S); act = S["dDD_pp"].values
        mae_n = float(np.nanmean(np.abs(act - pr["A_NAIVE"])))
        for pname, p in pr.items():
            mae = float(np.nanmean(np.abs(act - p)))
            frows.append(dict(form=form, predictor=pname, n=len(S), spearman=spearman(p, act),
                              sign_acc=float(np.nanmean(np.sign(p) == np.sign(act))), MAE=mae,
                              skill_vs_naive=(1 - mae / mae_n) if mae_n > 0 else np.nan,
                              mean_act=float(np.nanmean(act))))
        b = [x for x in frows if x["form"] == form and x["predictor"] == "B_SHARE"][0]
        say(f"       {form:<9} n={b['n']:<3} rho {b['spearman']:+.3f}  sign {b['sign_acc']:.3f}"
            f"  skill {b['skill_vs_naive']:+.3f}  mean actual dDD {b['mean_act']:+.3f} pp")
    F = pd.DataFrame(frows)
    pd.concat([R.assign(cut="subset"), F.assign(cut="form")]).to_csv(OUT / f"{SLUG}.score.csv", index=False)
    return R, F, f


# ---------------------------------------------------------------- [3] rule 8b: screen walk-forward
def screen_walkforward(G):
    say("\n[3] RULE 8b -- THE SCREEN WALKED FORWARD (fit on 2008-2016 episodes, scored on 2017-2026)")
    IN, OU = G[G["set"] == "IN"], G[G["set"] == "OUT"]
    fi = IN.dropna(subset=["IS_dDD_pp", "IS_neg_share"])
    if len(fi) < 20:
        say("    too few IS episodes -- SKIPPED"); return pd.DataFrame()
    a = float(np.nanmean(fi["IS_dDD_pp"]))
    bco = ols(np.c_[np.ones(len(fi)), fi["IS_neg_share"]], fi["IS_dDD_pp"])
    cco = ols(np.c_[np.ones(len(fi)), fi["IS_neg_share"], fi["depth"],
                    fi["IS_neg_share"] * fi["depth"]], fi["IS_dDD_pp"])
    say(f"    IS fit on {len(fi)} IN points: A {a:+.4f};  B {bco[0]:+.4f}{bco[1]:+.4f}*share;"
        f"  C {cco[0]:+.4f}{cco[1]:+.4f}*share{cco[2]:+.4f}*d{cco[3]:+.4f}*share*d")
    rows = []
    for lbl, S in (("IN OOS-window", IN), ("OUT OOS-window", OU),
                   ("OUT OOS-window minus TOP5/TOP40", OU[~OU["form"].isin(WEAK_OUT)])):
        S = S.dropna(subset=["OOS_dDD_pp", "OOS_neg_share"])
        if len(S) == 0:
            continue
        ns, dp = S["OOS_neg_share"].values, S["depth"].values
        act = S["OOS_dDD_pp"].values
        pr = {"A_NAIVE": np.full(len(S), a), "B_SHARE": bco[0] + bco[1] * ns,
              "C_SHARExD": cco[0] + cco[1] * ns + cco[2] * dp + cco[3] * ns * dp,
              "D_BOUND": dp * (1 - ns) * np.abs(S["OOS_ctrl_MaxDD"].values) * 100}
        mae_n = float(np.nanmean(np.abs(act - pr["A_NAIVE"])))
        say(f"    {lbl} (n={len(S)}, mean actual {np.nanmean(act):+.3f} pp)")
        for p, v in pr.items():
            mae = float(np.nanmean(np.abs(act - v)))
            rows.append(dict(subset=lbl, n=len(S), predictor=p, spearman=spearman(v, act),
                             sign_acc=float(np.nanmean(np.sign(v) == np.sign(act))), MAE=mae,
                             skill_vs_naive=(1 - mae / mae_n) if mae_n > 0 else np.nan))
            say(f"       {p:<10} rho {rows[-1]['spearman']:+.3f}  sign {rows[-1]['sign_acc']:.3f}"
                f"  MAE {mae:.3f}  skill {rows[-1]['skill_vs_naive']:+.3f}")
    D = pd.DataFrame(rows)
    D.to_csv(OUT / f"{SLUG}.screen_wf.csv", index=False)
    return D


# ---------------------------------------------------------------- [4] rule 8a + KEEP paths
def report_book(G, W, WF):
    say("\n[4] RULE 8a -- THE BOOK WALKED FORWARD (menu incl. gate-OFF, chosen on IS Sharpe @10bps)")
    for tag in ("IN", "OUT"):
        S = WF[WF["set"] == tag]
        say(f"    {tag}: gate picked in {int(S['picked_gate'].sum())}/{len(S)} cells;"
            f" mean OOS Sharpe pick {S['OOS_Sharpe'].mean():.4f} vs control {S['ctrl_OOS_Sharpe'].mean():.4f}"
            f" (mean regret vs do-nothing {S['regret'].mean():+.4f}, vs OOS-best {S['regret_vs_best'].mean():+.4f});"
            f" beats control in {int((S['OOS_Sharpe'] > S['ctrl_OOS_Sharpe']).sum())}/{len(S)}")
        say(f"       vs LIVE RULES v2 OOS Sharpe: pick wins {int((S['OOS_Sharpe'] > S['live_OOS_Sharpe']).sum())}/{len(S)};"
            f" vs SPY OOS Sharpe: {int((S['OOS_Sharpe'] > S['spy_OOS_Sharpe']).sum())}/{len(S)}")
    say("\n[5] KEEP PATHS over every point")
    for tag in ("IN", "OUT"):
        S = G[G["set"] == tag]; C = W[W["set"] == tag]
        say(f"    {tag} overlays: 4a {int(S['pass4a'].sum())}/{len(S)}   4b {int(S['pass4b'].sum())}/{len(S)}")
        say(f"    {tag} controls: 4a {int(C['ctrl_4a'].sum())}/{len(C)}   4b {int(C['ctrl_4b'].sum())}/{len(C)}")
        p = S[S["pass4b"]]
        if len(p):
            say(f"      4b passes ({tag}), all listed:")
            for _, x in p.sort_values("Sharpe", ascending=False).iterrows():
                say(f"        {x['panel']} {x['form']} c={x['cost']} B={x['B']:.2f} d={x['depth']:.2f}: "
                    f"{x['CAGR']:.2%}/{x['Sharpe']:.4f}/{x['MaxDD']:.2%} H {x['H1']:.3f}/{x['H2']:.3f} "
                    f"OOS {x['OOS_Sharpe']:.3f}  dDD {x['dDD_pp']:+.2f}pp  ctrl4b={bool(C[(C.panel==x['panel'])&(C.form==x['form'])&(C.cost==x['cost'])]['ctrl_4b'].iloc[0])}")
        say(f"      beats own numeraire: {int(S['beats_numeraire'].sum())}/{len(S)}")


def main():
    P, G, W, WF = build()
    gate_on_parent(G, W)
    score_screen(G)
    screen_walkforward(G)
    report_book(G, W, WF)
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {SLUG}.grid.csv / .windows.csv / .walkforward.csv / .score.csv / .screen_wf.csv")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

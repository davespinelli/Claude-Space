#!/usr/bin/env python3
"""QUEUE idea 153 — does-book-share-of-the-panel-price-a-tilt  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 153)
    "idea 81 found the vol tilt's realised gain does NOT track the cross-sectional slope's t
     (u56 slope +0.0045 pays nothing, broad +0.0029 pays +2.5..+5.2pp/yr) but does track how
     small a slice of the panel the book holds (INV-vs-NONE name overlap 69.4% on u56 at n=20
     vs 42.5% on broad).  Test it directly: sweep n so that book share is matched across
     panels, and regress realised dSharpe on overlap.  Would say when ANY cross-sectional key
     is worth ranking on.  Max 2 params."

WHAT IS AT STAKE.  Every ranking result the project has ever produced compares books at a
    matched NAME COUNT (n=5, n=20) across panels of 37, 91 and 141 mean-eligible names.  If
    the realised value of a cross-sectional key is governed by what FRACTION of the eligible
    panel the book holds — because a book holding half the panel cannot express any ranking,
    whatever the key's t-statistic — then matched-n comparisons across panels have been
    comparing different experiments, and idea 81's central puzzle (a STRONGER slope on u56
    paying LESS than a weaker one on broad) dissolves into an artefact of book share.  The
    output is a number PROTOCOL can state: the book share below which ranking on any key is
    worth doing, and above which it is arithmetic noise.

    The competing explanation is that the panels simply differ (u56's slope is real but its
    names are too correlated for the tilt to separate them; broad's is real and separable).
    The two make opposite predictions about what happens at MATCHED share, which is why the
    share sweep, not another t-statistic, is the decisive measurement.

CORPUS
    3 panels (u56 37.5 / broad 91.5 / small 141.2 mean eligible names) x 7 target book shares
    x 3 tilts x 2 cost rungs, weekly, t+1, no shorting, no leverage = 126 books; plus a
    63-book gross-normalised control at 10 bps (reported axis, see CONFOUND below).

TUNED PARAMETERS — exactly two, both swept exhaustively, ALL 21 grid points per (panel, cost)
reported:
    1. the target BOOK SHARE m in {0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00}, realised as
       n = max(2, round(m x mean weekly eligible count of that panel)).  m = 0.53 reproduces
       idea 81's u56 n=20 anchor exactly; m = 0.20 lands broad on n=18, one name off its
       n=20 anchor.  Share, not n, is the parameter — that is the whole idea.
    2. the vol tilt, 3 values (idea 81's, verbatim):
           INV  = composite / sqrt(vol20)   (RULES v1's live tilt)
           NONE = composite                 (no tilt: the control)
           POS  = composite * sqrt(vol20)
    Panels, cost rungs, the construction axis, the OOS window and every diagnostic are
    REPORTED axes, never selected on.  The 200d gate and vol20 < 0.60 stay at v1's values.

DEPENDENT VARIABLE, fixed before any number was read
    The tilt's realised gain over its own no-tilt control at matched (panel, m, cost, cost
    construction): dSharpe = Sharpe(tilt) - Sharpe(NONE) and dCAGR likewise.  The pre-
    registered regressand is |dSharpe| and |dCAGR| — overlap can only govern the MAGNITUDE a
    tilt is able to express; the SIGN is set by the panel's own vol premium (idea 81 found
    the sign matches the panel's premium 3 of 3).  Signed values are reported alongside.

CONFOUND, declared before the result
    (i) At m -> 1.00 the INV and NONE books hold the same eligible set by construction, so
        overlap -> 100% and dSharpe -> 0 MECHANICALLY.  That endpoint is not evidence.  Every
        regression below is therefore run twice: on the full grid and on m <= 0.53 only.
    (ii) idea 73/81's de-grossing: the literal GROSS/n book invests less than 0.75 whenever
        fewer than n names are eligible, which bites hardest at large m.  Realised mean gross
        is a printed column, and the whole grid is re-run at 10 bps with weights normalised to
        0.75 across the names actually held, as a control on both the overlap curve and the
        matched-share comparison.

REPRODUCTION, asserted before any new number is read
    [a] INV/m=0.53 on u56 must be n=20 and its INV-vs-NONE daily name overlap must come back
        at idea 81's published 69.4%; broad at n=20 at 42.5%.  Overlap is computed by idea
        81's own definition (mean over daily rows of |A n B| / |A u B|).
    [b] the NONE/n=20/u56@10bps book must equal idea 81's committed grid row cell-for-cell
        (CAGR, Sharpe, MaxDD, halves), so the control arm here is literally its control arm.
    [c] idea 80's Fama-MacBeth is IMPORTED and called verbatim; its bivariate vol20 slopes
        (+0.0045 t +3.90 on u56, +0.0029 t +3.19 on broad) are the competing regressor and
        must reproduce before they are used as one.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  Reproduction [a]-[c] holds.
    P2  Overlap is monotone increasing in book share within every panel, and at MATCHED share
        the three panels' overlaps agree far better than at matched n: the cross-panel spread
        of INV-vs-NONE overlap at matched m is under half its spread at matched n=20.
    P3  |dCAGR| falls monotonically as overlap rises, pooled across panels; the pooled OLS
        slope of |dSharpe| on overlap is NEGATIVE with |t| > 2 on the m <= 0.53 subgrid.
    P4  Overlap explains more of |dSharpe| than the panel's Fama-MacBeth slope t does
        (higher pooled R^2), i.e. HOW MUCH OF THE PANEL YOU HOLD prices a tilt better than
        HOW STRONG THE KEY IS.
    P5  Idea 81's puzzle dissolves: at matched share, u56's tilt payoff and broad's agree in
        sign and are within a factor of 2 of each other, where at matched n=20 they differ by
        more than 5x.
    P6  Nothing here is a KEEP: 0 of 126 books pass 4b on more than one panel.

WALK-FORWARD (PROTOCOL rule 8), selection rules fixed BEFORE any OOS number is read
    S1 plain IS Sharpe, S2 the 4b-aware IS screen (IS halves, IS drawdown, IS CAGR bars).
    Parameters (m, tilt) chosen on 2009-2016 only (2011-2016 on the small panel), the pick
    read ONCE on 2017-01-01..2026, reported as OOS CAGR/Sharpe/MaxDD against RULES v1 (same
    panel, same cost) and SPY.  Both KEEP paths (4a and 4b) are evaluated at every one of the
    126 books, on the full sample and again on the OOS window alone.

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54); the small panel
      drops the 44 tickers with max_1d_move >= 1.0 and its SPY is a held-out benchmark.
    * Idea 49/39: the eligibility gate is INVERTED on the small panel, so its numbers are
      about a gate that does not work there; they are reported, not traded.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's.
    * Mean eligible count is measured on the whole evaluation sample, so m is a sample-average
      share, not a point-in-time one; the realised weekly share is printed as n_held/n_elig.

HARNESS
    `baseline` (the live rules), idea 94's window/halves/4a machinery, idea 129's panel and 4b
    bar machinery and idea 80's Fama-MacBeth are IMPORTED, so the control arm, the bars and
    the competing regressor are literally the committed ones.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .overlap.csv, .matched.csv,
.regression.csv, .walkforward.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_does-book-share-price-a-tilt_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I80P = OUT / "2026-09-04_prox-inverted-signal_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
I80 = _load(I80P, "i80")

FREQ = "W"
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
OOS_START = H.OOS_START
PHI0, DELTA0 = 0.70, 0.60
GROSS, MAX_VOL = 0.75, 0.60

SHARES = [0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00]   # tuned parameter 1
TILTS = ["INV", "NONE", "POS"]                        # tuned parameter 2
CONSTR = ["lit", "norm"]                              # reported axis (see CONFOUND ii)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the book (idea 81 verbatim)
def parts(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    v = px.pct_change().rolling(20).std() * np.sqrt(252)
    return comp * (0.5 + 0.5 * above.astype(float)), above, v


_SC = {}


def score_of(px, tilt, pk):
    key = (pk, tilt)
    if key not in _SC:
        s, above, v = parts(px)
        vv = v.clip(lower=0.08) ** 0.5
        _SC[key] = ({"INV": s / vv, "NONE": s, "POS": s * vv}[tilt], above, v)
    return _SC[key]


def held_mask(px, tilt, n, pk):
    s, above, v = score_of(px, tilt, pk)
    rank = s.where(above & (v < MAX_VOL)).rank(axis=1, ascending=False)
    return rank <= n


def weights(px, tilt, n, pk, constr="lit", fixedw=None):
    m = held_mask(px, tilt, n, pk).astype(float)
    if fixedw is not None:
        return m * fixedw
    if constr == "lit":
        return m * (GROSS / n)
    k = m.sum(axis=1).replace(0, np.nan)
    return m.div(k, axis=0).fillna(0.0) * GROSS


def eligible_mask(px, pk):
    _, above, v = score_of(px, "NONE", pk)
    return above & (v < MAX_VOL)


def overlap(A, B):
    """Idea 81's definition: mean over daily rows of |A n B| / |A u B| of the held sets."""
    inter = (A & B).sum(axis=1)
    un = (A | B).sum(axis=1).replace(0, np.nan)
    return float((inter / un).mean())


def ols(y, X, names):
    """Plain OLS with an intercept; returns coef, t, R2."""
    X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X])
    y = np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(len(y) - X.shape[1], 1)
    s2 = resid @ resid / dof
    xtx = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.maximum(np.diag(xtx) * s2, 1e-30))
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (resid @ resid) / ss_tot if ss_tot > 0 else np.nan
    return dict(zip(["const"] + names, beta)), dict(zip(["const"] + names, beta / se)), r2


def main():
    say("=" * 190)
    say(f"IDEA 153 — does-book-share-of-the-panel-price-a-tilt   ({STEM})")
    say("Does the fraction of the eligible panel a book holds price a cross-sectional tilt "
        "better than the tilt's own slope t?")
    say("=" * 190)

    ok, rows, ov_rows, fm_rows, ref, rets = {}, [], [], [], {}, {}
    nmap = {}

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        el = eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        ref[pk] = dict(px=px, start=start, spy=ms, spy_oos=mso, bfull=bfull, bIS=bIS,
                       bOOS=bOOS, v1=v1, n_elig=n_elig, desc=desc, el=el)
        nmap[pk] = {m: max(2, int(round(m * n_elig))) for m in SHARES}

        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}, mean "
            f"weekly eligible names {n_elig:.1f}")
        say(f"    book share -> n:  " + ", ".join(f"m={m:.2f}->n={nmap[pk][m]}" for m in SHARES))
        say(f"    SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}"
            f"/{mso['MaxDD']:.2%}")
        for c in COSTS:
            m_, mo_ = metrics(v1[c]), metrics(v1[c].loc[OOS_START:])
            say(f"    RULES v1 @{int(c)}bps: {m_['CAGR']:.2%}/{m_['Sharpe']:.3f}/"
                f"{m_['MaxDD']:.2%} | OOS {mo_['CAGR']:.2%}/{mo_['Sharpe']:.3f}/{mo_['MaxDD']:.2%}")

        # ---------- [a] reproduction of idea 81's overlap anchors, and the overlap curve
        for m in SHARES:
            n = nmap[pk][m]
            Msk = {t: held_mask(px, t, n, pk).loc[start:] for t in TILTS}
            nh = float(Msk["NONE"].sum(axis=1).mean())
            ov_rows.append(dict(panel=pk, m=m, n=n, n_elig=n_elig, n_held=nh,
                                realised_share=nh / n_elig,
                                ov_INV_NONE=overlap(Msk["INV"], Msk["NONE"]),
                                ov_POS_NONE=overlap(Msk["POS"], Msk["NONE"]),
                                ov_INV_POS=overlap(Msk["INV"], Msk["POS"])))
        if pk in ("u56", "broad"):                      # idea 81's own n=20 anchor
            Msk = {t: held_mask(px, t, 20, pk).loc[start:] for t in TILTS}
            o = overlap(Msk["INV"], Msk["NONE"])
            pub = 0.694 if pk == "u56" else 0.425
            ok[f"a:{pk}"] = abs(o - pub) < 0.006
            say(f"[a] {pk} n=20 INV-vs-NONE overlap: idea 81 published {pub:.1%}, this run "
                f"{o:.1%} -> {'MATCH' if ok[f'a:{pk}'] else 'MISMATCH'}")

        # ---------- [c] the competing regressor
        fm = I80.fama_macbeth(px, I80.eligible_mask(px), start)
        fm_rows.append(dict(panel=pk, slope_biv=fm["vol20_biv"][0], t_biv=fm["vol20_biv"][1],
                            slope_uni=fm["vol20_uni"][0], t_uni=fm["vol20_uni"][1]))
        say(f"[c] idea 80's Fama-MacBeth (verbatim): bivariate vol20 slope "
            f"{fm['vol20_biv'][0]:+.5f} (t {fm['vol20_biv'][1]:+.2f}), univariate "
            f"{fm['vol20_uni'][0]:+.5f} (t {fm['vol20_uni'][1]:+.2f})")

        # ---------- the grid
        for m in SHARES:
            n = nmap[pk][m]
            for t in TILTS:
                for cn in CONSTR:
                    W = weights(px, t, n, pk, constr=cn)
                    for c in COSTS:
                        if cn == "norm" and c != 10.0:
                            continue
                        res = backtest(px, W, cost_bps=c, freq=FREQ)
                        r = res["returns"].loc[start:]
                        rets[(pk, m, t, c, cn)] = r
                        mm, mo, mi = metrics(r), metrics(H.window(r, "OOS")), metrics(H.window(r, "IS"))
                        h1, h2 = H.halves(r)
                        ih1, ih2 = H.halves(H.window(r, "IS"))
                        mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                        mgo = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                        mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                        rows.append(dict(
                            panel=pk, m=m, n=n, tilt=t, cost=c, constr=cn,
                            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=ih1, IS_H2=ih2,
                            TO=res["turnover"].loc[start:].sum() / mm["Years"],
                            gross=float(W.loc[start:].sum(axis=1).mean()),
                            pass4a=H.pass4a(r, v1[c]),
                            pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-",
                            pass4b_oos=all(mgo[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                            IS_adm=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR"))))

    df = pd.DataFrame(rows)
    OVL = pd.DataFrame(ov_rows)
    FM = pd.DataFrame(fm_rows).set_index("panel")
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    OVL.to_csv(OUT / f"{STEM}.overlap.csv", index=False)

    # ---------- [b] idea 81's control arm, cell for cell
    prev = OUT / "2026-09-05_vol20-as-the-hidden-ranking-key_cloud.grid.csv"
    if prev.exists():
        g81 = pd.read_csv(prev)
        a = g81[(g81.panel == "u56") & (g81.scaler == "NONE") & (g81.n == 20) & (g81.cost == 10.0)].iloc[0]
        b = df[(df.panel == "u56") & (df.tilt == "NONE") & (df.n == 20) & (df.cost == 10.0)
               & (df.constr == "lit")]
        if len(b):
            b = b.iloc[0]
            same = all(abs(a[k] - b[k]) < 1e-9 for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"))
            ok["b"] = same
            say(f"\n[b] NONE/n=20/u56@10bps vs idea 81's committed grid row: "
                f"{b.CAGR:.5%}/{b.Sharpe:.5f}/{b.MaxDD:.5%} halves {b.H1:.5f}/{b.H2:.5f} vs "
                f"{a.CAGR:.5%}/{a.Sharpe:.5f}/{a.MaxDD:.5%} halves {a.H1:.5f}/{a.H2:.5f} -> "
                f"{'IDENTICAL' if same else 'DIFFERENT — unsafe'}")
        else:
            ok["b"] = False
            say("\n[b] u56 n=20 is not on this run's share grid at m=0.53 — check skipped, "
                "NOT quietly passed")
    for pk_, (sl, t_) in {"u56": (0.0045, 3.90), "broad": (0.0029, 3.19)}.items():
        g = FM.loc[pk_]
        hit = abs(g.slope_biv - sl) < 5e-4 and abs(g.t_biv - t_) < 0.30
        ok[f"c:{pk_}"] = hit
        say(f"[c] {pk_}: idea 80 published {sl:+.4f} (t {t_:+.2f}), this run {g.slope_biv:+.5f}"
            f" (t {g.t_biv:+.2f}) -> {'MATCH' if hit else 'MISMATCH'}")

    if not all(ok.values()):
        say("\n[WARNING] a pre-check did not hold; read what follows with that in mind.")

    # =============================================================== the grid
    say("\n" + "=" * 190)
    say("THE GRID — 2 tuned parameters (book share m x tilt) = 21 points, EVERY one reported, "
        "on 3 panels x 2 cost rungs (literal GROSS/n book)")
    say("=" * 190)
    cols = ["m", "n", "tilt", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "TO", "gross", "pass4a", "pass4b", "fail4b", "pass4b_oos"]
    for pk in PANELS:
        for c in COSTS:
            s = df[(df.panel == pk) & (df.cost == c) & (df.constr == "lit")].sort_values(["m", "tilt"])
            b = ref[pk]
            say(f"\n  {pk} @ {int(c)} bps  (SPY {b['spy']['CAGR']:.2%}/{b['spy']['Sharpe']:.3f}/"
                f"{b['spy']['MaxDD']:.2%}; RULES v1 {metrics(b['v1'][c])['CAGR']:.2%}/"
                f"{metrics(b['v1'][c])['Sharpe']:.3f}/{metrics(b['v1'][c])['MaxDD']:.2%})")
            say(s[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # =============================================================== P2 — the overlap curve
    say("\n" + "=" * 190)
    say("P2 — overlap vs book share, and the cross-panel spread at matched share vs matched n")
    say("=" * 190)
    say(OVL.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    mono = all(OVL[OVL.panel == pk].sort_values("m").ov_INV_NONE.is_monotonic_increasing
               for pk in PANELS)
    ok["P2a"] = mono
    say(f"\n    overlap monotone increasing in m within every panel: "
        f"{'HELD' if mono else 'FAILED'}")
    sp_m = OVL.groupby("m").ov_INV_NONE.agg(lambda x: x.max() - x.min())
    say("    cross-panel spread of INV-vs-NONE overlap at each matched share m:")
    say(sp_m.to_string(float_format=lambda x: f"{x:.3f}"))
    n20 = {}
    for pk in PANELS:
        px, start = ref[pk]["px"], ref[pk]["start"]
        Ms = {t: held_mask(px, t, 20, pk).loc[start:] for t in TILTS}
        n20[pk] = overlap(Ms["INV"], Ms["NONE"])
    sp_n = max(n20.values()) - min(n20.values())
    mean_sp_m = float(sp_m.mean())
    ok["P2b"] = mean_sp_m < 0.5 * sp_n
    say(f"    spread at matched n=20: {sp_n:.3f} ({', '.join(f'{k} {v:.1%}' for k, v in n20.items())})"
        f" | mean spread at matched m: {mean_sp_m:.3f} -> P2b "
        f"{'HELD' if ok['P2b'] else 'FAILED'} (needed < {0.5 * sp_n:.3f})")

    # =============================================================== P3/P4 — the regression
    say("\n" + "=" * 190)
    say("P3/P4 — regress the tilt's realised gain on overlap, against the slope-t explanation")
    say("=" * 190)
    dr = []
    for (pk, m, c, cn), _ in df.groupby(["panel", "m", "cost", "constr"]):
        s = df[(df.panel == pk) & (df.m == m) & (df.cost == c) & (df.constr == cn)].set_index("tilt")
        if len(s) < 3:
            continue
        o = OVL[(OVL.panel == pk) & (OVL.m == m)].iloc[0]
        for t in ("INV", "POS"):
            dr.append(dict(panel=pk, m=m, n=int(s.loc[t, "n"]), cost=c, constr=cn, tilt=t,
                           overlap=o.ov_INV_NONE if t == "INV" else o.ov_POS_NONE,
                           share=o.realised_share,
                           dSharpe=s.loc[t, "Sharpe"] - s.loc["NONE", "Sharpe"],
                           dCAGR=s.loc[t, "CAGR"] - s.loc["NONE", "CAGR"],
                           dMaxDD=s.loc[t, "MaxDD"] - s.loc["NONE", "MaxDD"],
                           t_biv=FM.loc[pk, "t_biv"], slope_biv=FM.loc[pk, "slope_biv"]))
    D = pd.DataFrame(dr)
    D["absdS"], D["absdC"] = D.dSharpe.abs(), D.dCAGR.abs()
    D.to_csv(OUT / f"{STEM}.regression.csv", index=False)
    say(D[D.constr == "lit"].sort_values(["panel", "cost", "tilt", "m"])
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    reg_rows = []
    for label, sub in [("ALL 84 rows", D), ("literal only", D[D.constr == "lit"]),
                       ("literal, m<=0.53", D[(D.constr == "lit") & (D.m <= 0.53)]),
                       ("gross-normalised", D[D.constr == "norm"]),
                       ("gross-normalised, m<=0.53", D[(D.constr == "norm") & (D.m <= 0.53)])]:
        for yn in ("absdS", "absdC"):
            bo, to, r2o = ols(sub[yn], [sub.overlap], ["overlap"])
            bt, tt, r2t = ols(sub[yn], [sub.t_biv], ["t_biv"])
            bb, tb, r2b = ols(sub[yn], [sub.overlap, sub.t_biv], ["overlap", "t_biv"])
            reg_rows.append(dict(sample=label, n_rows=len(sub), y=yn,
                                 b_overlap=bo["overlap"], t_overlap=to["overlap"], R2_overlap=r2o,
                                 b_tbiv=bt["t_biv"], t_tbiv=tt["t_biv"], R2_tbiv=r2t,
                                 b_overlap_joint=bb["overlap"], t_overlap_joint=tb["overlap"],
                                 t_tbiv_joint=tb["t_biv"], R2_joint=r2b))
    R = pd.DataFrame(reg_rows)
    say("\n  univariate and joint OLS (y = magnitude of the tilt's realised gain):")
    say(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    key = R[(R["sample"] == "literal, m<=0.53") & (R.y == "absdS")].iloc[0]
    ok["P3"] = bool(key.b_overlap < 0 and abs(key.t_overlap) > 2)
    ok["P4"] = bool(key.R2_overlap > key.R2_tbiv)
    say(f"\n    P3 (|dSharpe| falls with overlap on m<=0.53, |t|>2): slope "
        f"{key.b_overlap:+.4f} (t {key.t_overlap:+.2f}) -> {'HELD' if ok['P3'] else 'FAILED'}")
    say(f"    P4 (overlap explains more than the slope t): R2 overlap {key.R2_overlap:.3f} vs "
        f"R2 t_biv {key.R2_tbiv:.3f} -> {'HELD' if ok['P4'] else 'FAILED'}")
    say("    within-panel Spearman(overlap, |dSharpe|), literal book:")
    for pk in PANELS:
        s = D[(D.panel == pk) & (D.constr == "lit")]
        say(f"      {pk}: {H.spearman(s.overlap.values, s.absdS.values):+.3f} "
            f"(n={len(s)}), on m<=0.53 "
            f"{H.spearman(s[s.m <= 0.53].overlap.values, s[s.m <= 0.53].absdS.values):+.3f}")

    # =============================================================== P5 — the matched-share test
    say("\n" + "=" * 190)
    say("P5 — idea 81's puzzle at matched n=20 vs at matched book share (10 bps, literal)")
    say("=" * 190)
    mrows = []
    for pk in PANELS:
        px, start = ref[pk]["px"], ref[pk]["start"]
        for t in TILTS:
            W = weights(px, t, 20, pk)
            r = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            mm = metrics(r)
            mrows.append(dict(basis="matched n=20", panel=pk, n=20, tilt=t,
                              CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                              share=20 / ref[pk]["n_elig"]))
    M20 = pd.DataFrame(mrows)
    piv20 = M20.pivot_table(index="panel", columns="tilt", values=["CAGR", "Sharpe"])
    say("  matched n=20 (idea 81's comparison):")
    say(M20.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    d20 = {pk: (piv20.loc[pk, ("CAGR", "POS")] - piv20.loc[pk, ("CAGR", "NONE")]) for pk in PANELS}
    say("  tilt payoff dCAGR(POS-NONE) at matched n=20: "
        + ", ".join(f"{k} {v:+.2%}" for k, v in d20.items()))

    say("\n  matched book share (10 bps, literal), dCAGR(POS-NONE) and dCAGR(INV-NONE):")
    ms = D[(D.constr == "lit") & (D.cost == 10.0)].pivot_table(index="m", columns=["tilt", "panel"],
                                                               values="dCAGR")
    say(ms.to_string(float_format=lambda x: f"{x:+.2%}"))
    ms.to_csv(OUT / f"{STEM}.matched.csv")
    anchor = 0.20  # broad's n=20 share, pre-registered as the comparison point
    row = D[(D.constr == "lit") & (D.cost == 10.0) & (D.m == anchor) & (D.tilt == "POS")].set_index("panel")
    u, b = row.loc["u56", "dCAGR"], row.loc["broad", "dCAGR"]
    r20 = abs(d20["broad"] / d20["u56"]) if abs(d20["u56"]) > 1e-9 else np.inf
    rm = abs(b / u) if abs(u) > 1e-9 else np.inf
    ok["P5"] = bool(np.sign(u) == np.sign(b) and rm < 2.0 and r20 > 5.0)
    say(f"\n    at matched n=20 broad/u56 payoff ratio = {r20:.1f}x; at matched share "
        f"m={anchor} (u56 n={int(row.loc['u56', 'n'])}, broad n={int(row.loc['broad', 'n'])}): "
        f"u56 {u:+.2%}, broad {b:+.2%}, ratio {rm:.1f}x, signs "
        f"{'agree' if np.sign(u) == np.sign(b) else 'DISAGREE'} -> P5 "
        f"{'HELD' if ok['P5'] else 'FAILED'}")

    # =============================================================== the transfer check
    say("\n" + "=" * 190)
    say("TRANSFER CHECK (zero free parameters) — carry the STANDING 4b KEEP's own book share, "
        "not its name count, from u56 to broad")
    say("The standing KEEP (2026-09-04) is top-20 equal-weight, no vol scaler, on u56.  Idea 44 "
        "found the same NAME COUNT fails 4b's H2 on broad.  Nothing below is tuned: the share is "
        "read off the incumbent and multiplied by broad's own eligible count.")
    say("=" * 190)
    s_nom = 20 / ref["u56"]["n_elig"]
    s_real = float(OVL[(OVL.panel == "u56") & (OVL.m == 0.53)].iloc[0].realised_share)
    say(f"    incumbent share on u56: nominal 20/{ref['u56']['n_elig']:.1f} = {s_nom:.3f}; "
        f"realised (mean names held / mean eligible) = {s_real:.3f}")
    trows = []
    for pk in ("broad", "small"):
        px, start = ref[pk]["px"], ref[pk]["start"]
        ns = sorted({20, max(2, int(round(s_nom * ref[pk]["n_elig"]))),
                     max(2, int(round(s_real * ref[pk]["n_elig"])))})
        say(f"    {pk}: name-count transfer n=20 (share {20 / ref[pk]['n_elig']:.3f}); "
            f"share transfer n={ns}")
        for n in ns:
            for c in COSTS:
                r = backtest(px, weights(px, "NONE", n, pk), cost_bps=c, freq=FREQ)["returns"].loc[start:]
                mm, mo = metrics(r), metrics(H.window(r, "OOS"))
                h1, h2 = H.halves(r)
                mg = C.margins_at(r, ref[pk]["bfull"], PHI0, DELTA0, "full")
                trows.append(dict(panel=pk, n=n, share=n / ref[pk]["n_elig"], cost=c,
                                  kind="name-count" if n == 20 else "share",
                                  CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                  H1=h1, H2=h2, OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-"))
    TR = pd.DataFrame(trows)
    TR.to_csv(OUT / f"{STEM}.transfer.csv", index=False)
    say(TR.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    b10 = TR[(TR.panel == "broad") & (TR.cost == 10.0)]
    say(f"\n    broad @10bps: the name-count transfer (n=20) passes 4b "
        f"{bool(b10[b10.n == 20].pass4b.iloc[0])}; the share transfer passes 4b in "
        f"{int(b10[b10.kind == 'share'].pass4b.sum())} of {int((b10.kind == 'share').sum())} of "
        f"its (rounding-equivalent) n values")

    # =============================================================== KEEP paths
    say("\n" + "=" * 190)
    say("BOTH KEEP PATHS on all 126 literal books (4a vs the live rules, 4b vs SPY)")
    say("=" * 190)
    lit = df[df.constr == "lit"]
    kp = lit.groupby(["m", "tilt"]).agg(pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"),
                                        pass4b_oos=("pass4b_oos", "sum"), cells=("panel", "size"))
    say(kp.to_string())
    say(f"\n    total: 4a {int(lit.pass4a.sum())} of {len(lit)}, 4b {int(lit.pass4b.sum())} of "
        f"{len(lit)}, 4b on the OOS window alone {int(lit.pass4b_oos.sum())} of {len(lit)}")
    xu = lit[lit.pass4b].groupby(["m", "tilt"]).panel.nunique()
    say("    cross-universe 4b ((m, tilt) passing on >1 panel): "
        + (", ".join(f"m={k[0]}/{k[1]} on {v} panels" for k, v in xu.items()) if len(xu) else "NONE"))
    ok["P6"] = (not (xu > 1).any()) if len(xu) else True
    say(f"    P6 -> {'HELD' if ok['P6'] else 'FAILED — a cross-universe KEEP exists, see above'}")
    if lit.pass4b.any():
        say("\n    the 4b passes (single-panel):")
        say(lit[lit.pass4b][["panel", "cost", "m", "n", "tilt", "CAGR", "Sharpe", "MaxDD",
                             "H1", "H2", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # =============================================================== rule 8
    say("\n" + "=" * 190)
    say("RULE 8 WALK-FORWARD — (m, tilt) chosen on the IS window (<= 2016-12-31) only, read "
        "ONCE on 2017-01-01..2026")
    say("=" * 190)
    wrows = []
    for pk in PANELS:
        for c in COSTS:
            s = lit[(lit.panel == pk) & (lit.cost == c)].reset_index(drop=True)
            v1o = metrics(ref[pk]["v1"][c].loc[OOS_START:])
            sp = ref[pk]["spy_oos"]
            picks = {"S1_ISSharpe": s.loc[s.IS_Sharpe.idxmax()]}
            adm = s[s.IS_adm]
            picks["S2_4bAware"] = adm.loc[adm.IS_Sharpe.idxmax()] if len(adm) else None
            # the pre-registered control: no tilt at all, at the IS-best share
            ctl = s[s.tilt == "NONE"]
            picks["S3_NONE_only"] = ctl.loc[ctl.IS_Sharpe.idxmax()]
            for nm, r in picks.items():
                if r is None:
                    wrows.append(dict(panel=pk, cost=c, sel=nm, tilt="NOTHING ADMISSIBLE",
                                      m=np.nan, n=np.nan, v1_OOS_Sharpe=v1o["Sharpe"],
                                      spy_OOS_Sharpe=sp["Sharpe"]))
                    continue
                wrows.append(dict(panel=pk, cost=c, sel=nm, tilt=r.tilt, m=r.m, n=int(r.n),
                                  IS_Sharpe=r.IS_Sharpe, IS_MaxDD=r.IS_MaxDD,
                                  OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                  OOS_MaxDD=r.OOS_MaxDD, pass4b_oos=r.pass4b_oos,
                                  v1_OOS_CAGR=v1o["CAGR"], v1_OOS_Sharpe=v1o["Sharpe"],
                                  v1_OOS_MaxDD=v1o["MaxDD"], spy_OOS_CAGR=sp["CAGR"],
                                  spy_OOS_Sharpe=sp["Sharpe"], spy_OOS_MaxDD=sp["MaxDD"]))
    Wf = pd.DataFrame(wrows)
    Wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(Wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pk_ = Wf[Wf.tilt != "NOTHING ADMISSIBLE"]
    say(f"\n    tilt picked by rule 8: " + ", ".join(f"{k} {v}" for k, v in pk_.tilt.value_counts().items()))
    say(f"    share picked by rule 8: " + ", ".join(f"m={k} {v}" for k, v in pk_.m.value_counts().sort_index().items()))
    s1 = Wf[Wf.sel == "S1_ISSharpe"]
    s3 = Wf[Wf.sel == "S3_NONE_only"]
    say(f"    mean OOS Sharpe: S1 (tilt allowed) {s1.OOS_Sharpe.mean():.3f} vs S3 (no tilt "
        f"allowed) {s3.OOS_Sharpe.mean():.3f} vs RULES v1 {s1.v1_OOS_Sharpe.mean():.3f} vs SPY "
        f"{s1.spy_OOS_Sharpe.mean():.3f}   (the tilt's OOS value to a rule-8 user)")

    say("\n" + "=" * 190)
    say("PRE-REGISTERED PREDICTIONS — outcome")
    say("=" * 190)
    for k_, v_ in ok.items():
        say(f"    {k_}: {'HELD/OK' if v_ else 'FAILED'}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

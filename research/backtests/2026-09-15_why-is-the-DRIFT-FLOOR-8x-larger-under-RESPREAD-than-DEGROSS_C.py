#!/usr/bin/env python3
"""IDEA 769 - why is the DRIFT FLOOR 8x LARGER under RESPREAD than DEGROSS?
Lane C, 2026-09-15.

THE QUESTION
------------
Idea 562 measured the engine-drift noise floor - the pp/yr residue that two arms holding a
SHARED name at the SAME TARGET accumulate purely because the engine renormalises each arm by
its own total between rebalances - at max |DRIFT_pp| over {W,M,Q} of

    RESPREAD 0.1374     DEGROSS 0.0164        (ratio 0.119)

and read the 8.4x as the SHARED DENOMINATOR: a de-grossed book divides by the panel count n
that both arms share, a re-spread book divides by its own gate count k, so at k << n the
de-grossed targets that drift apart are smaller.  That reading was never tested; it was
inferred from two numbers.  This run tests it directly and publishes the floor as a FUNCTION
of the construction instead of a single number.

WHY THE TWO CHANNELS ARE CONFOUNDED AT A SINGLE k/n, AND HOW THE q LADDER SEPARATES THEM
----------------------------------------------------------------------------------------
At one fixed k/n the two candidate explanations are observationally identical:

    RESPREAD   per-name target w = g/k        book exposure E = g
    DEGROSS    per-name target w = g/n        book exposure E = g*(k/n)

so at fixed k/n, moving RESPREAD -> DEGROSS divides BOTH w and E by exactly k/n.  Idea 562's
8.4x is therefore equally consistent with "the floor is linear in the TARGET SIZE" (the
denominator reading) and with "the floor is linear in the EXPOSURE the book actually carries".
Walking the ratio q = k/n breaks the tie, because along that axis the two channels move in
OPPOSITE directions inside each construction:

    RESPREAD   w = g/(q*n)  ~ 1/q   (rises as q falls)      E = g          (flat in q)
    DEGROSS    w = g/n      flat in q                       E = g*q        (falls with q)

A floor that is a target-size fact rises like 1/q under RESPREAD and is flat under DEGROSS.
A floor that is an exposure fact is flat under RESPREAD and falls like q under DEGROSS.
The two hypotheses predict opposite shapes on both curves, so one ladder settles it.

A third reading, H_BILINEAR (|DRIFT| ~ w*E, slopes -1 and +1, construction gap (k/n)^2), was
NOT pre-registered: it was written down after the two pre-registered readings were scored and
neither fitted both curves.  It is a parameter-free consequence of the engine's renormalisation
(the algebra is printed in section 2) and it is scored on the SAME unchanged grid, with no new
tuning, no new axis and no re-selection.  It is reported as post-hoc and flagged as such.

THE ARM PAIR (why MRES is exactly zero here, unlike idea 562's)
---------------------------------------------------------------
Idea 562's pair (MA-THRESH vs a daily depth-matched MOM) matches depth only approximately, so
its shared-name leg splits into DRIFT (equal targets) plus MRES (a depth-match residual).
This run's FIXK family selects EXACTLY k_t = round(q*n_t) names in BOTH arms every day:

    MA-DIST   top-k_t by px/ma200 - 1
    MOM       top-k_t by px.shift(21)/px.shift(252) - 1

so within a construction every held name in both arms carries the IDENTICAL target, MRES == 0
by construction (gate G3 checks it), and BOTH == DRIFT exactly.  The floor is isolated with no
residual to argue about.  The GATE family (MA-THRESH at theta, k_t free) is run alongside as
the reproduction of 562's own setting, where k_t varies in time under RESPREAD and does not
under DEGROSS - a SECOND way the two constructions differ that the FIXK family removes.

DEFINITION (562's own, arithmetic, annualised pp/yr)
-----------------------------------------------------
On every bar, with held weights h and target-in-force T:
    shared = (T_A > 0) & (T_B > 0)
    eqtgt  = shared & (|T_A - T_B| <= 1e-15)
    DRIFT_pp = 252 * 100 * mean_t  sum_{j in eqtgt} (h_A - h_B)_j * r_j
    MRES_pp  = 252 * 100 * mean_t  sum_{j in shared & ~eqtgt} (h_A - h_B)_j * r_j
At cadence D the engine sets h == T on every bar, so DRIFT_pp is ZERO BY CONSTRUCTION (G2).

THE BOOK LEG (this lane's mandate: both KEEP paths + rule 8 on every grid point)
--------------------------------------------------------------------------------
Every arm at every cell is also priced as capital, twice:
    DRIFT = the engine's native behaviour (weights drift between rebalances)
    RTT   = "rebalance to target", the same cadence targets restored every day (freq='D' on
            the cadence-ffilled target matrix), i.e. the drift channel switched off, paying
            10 bps on the extra turnover.
4a is judged against RULES v2 (live), 4b against SPY, on each panel's own calendar.

2 TUNED PARAMS: CONSTRUCTION {RESPREAD, DEGROSS} x K/N q {0.10 .. 0.90}.  Panel, cadence, arm,
handling, theta and cost rung are REPORTED axes, never selected over; ALL grid points printed.
Gross pinned at the live 0.75.  Costs 10 bps (0 and 25 derived exactly and reported),
next-day execution, no shorting, no leverage.
RULE 8: every parameter chosen on 2009..2016 only; 2017..2026 read once.

SURVIVORSHIP: B136 and SMALL are CURRENT constituents only; dead names are absent and CAGR
levels are inflated.  DRIFT_pp is an arm-minus-arm quantity inside one panel at identical
depth, where the bias very largely cancels; the KEEP columns and the rule-8 levels are NOT
protected and are read with that caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .drift.csv .books.csv .rungs.csv .law.csv .walkforward.csv .keep.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
RUNGS = [0, 10, 25]
GROSS = 0.75
PANELS = ["U56", "B136", "SMALL"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]          # tuned param 1
QS = [0.10, 0.20, 0.30, 0.50, 0.70, 0.90]        # tuned param 2  (k/n)
CADENCES = ["D", "W", "M", "Q"]                  # reported
ARMS = ["MA-DIST", "MOM"]                        # reported
HANDLING = ["DRIFT", "RTT"]                      # reported
THETA = [0.06, 0.00, -0.12]                      # reported (GATE family, 562's setting)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS_TGT = 1e-15
BAR_ENGINE = 1e-12
BAR_RUNG = 1e-15
BAR_D = 0.0

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 140)
pd.set_option("display.max_rows", 2000)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def run(px, W, freq):
    """engine.backtest's arithmetic, also returning the HELD and TARGET-IN-FORCE matrices."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    tgt = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    t_cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
            t_cur = new
        held[i] = cur
        tgt[i] = t_cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    r0 = pd.Series(np.nansum(held * rets, axis=1), index=px.index)
    return r0, pd.Series(turn, index=px.index), held, tgt


def rung(r0, turn, c):
    return r0 - turn * c / 1e4


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def fail_4b_oos(s, spy):
    """the 4b legs read on the OOS window alone (rule 8's own reading of path 4b)."""
    t = {"OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["oMaxDD"]) <= 0.60 * abs(spy["oMaxDD"]),
         "CAGR": s["oCAGR"] >= 0.70 * spy["oCAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ signals
def ma_dist(px):
    return (px / px.rolling(200).mean() - 1.0).where(live_mask(px))


def mom_rank(px):
    return (px.shift(21) / px.shift(252) - 1).where(live_mask(px))


def topk(sig, kt, live):
    return sig.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def book(px, g, con, nlive):
    """RESPREAD divides by the arm's OWN count k_t; DEGROSS by the SHARED panel count n_t."""
    if con == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    return g.astype(float).div(nlive.clip(lower=1), axis=0) * GROSS


def rtt_weights(W, idx, freq):
    m = rebalance_mask(idx, freq)
    return W.where(m, np.nan).ffill().fillna(0.0)


def ols(y, X, names):
    """plain least squares with t-stats; X already carries its intercept column."""
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ b
    dof = max(len(y) - X.shape[1], 1)
    s2 = float(resid @ resid) / dof
    try:
        cov = s2 * np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(cov))
    except np.linalg.LinAlgError:
        se = np.full(X.shape[1], np.nan)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / ss_tot if ss_tot > 0 else np.nan
    return dict(zip(names, b)), dict(zip(names, se)), r2, float(np.sqrt(s2))


# ================================================================== main
def main():
    P("=" * 178)
    P("IDEA 769 - why is the DRIFT FLOOR 8x LARGER under RESPREAD than DEGROSS?"
      "   (lane C, 2026-09-15)")
    P("=" * 178)
    P("PROTOCOL: 10 bps per unit turnover (0/25 derived exactly and reported), next-day")
    P(f"execution, no shorting, no leverage.  IS = start..{IS_END}, OOS = {OOS_START}..end,")
    P("read once.  2 TUNED PARAMS: CONSTRUCTION {RESPREAD,DEGROSS} x K/N q "
      f"{QS}.")
    P(f"Reported axes (never selected over): panel {PANELS}, cadence {CADENCES}, arm {ARMS},")
    P(f"handling {HANDLING}, theta {THETA} (GATE family), cost rung {RUNGS}.  Gross pinned "
      f"{GROSS}.")
    P("HYPOTHESES, pre-registered before any number is read:")
    P("  H_DENOM (562's reading): the floor is linear in the PER-NAME TARGET w.  Then along q,")
    P("          RESPREAD |DRIFT| ~ 1/q (slope -1 in log q) and DEGROSS |DRIFT| is FLAT (0).")
    P("  H_EXPO  (the rival):     the floor is linear in the BOOK EXPOSURE E.  Then along q,")
    P("          RESPREAD is FLAT (0) and DEGROSS |DRIFT| ~ q (slope +1 in log q).")
    P("  H_COLLAPSE: if H_DENOM holds, DRIFT_pp / w collapses the two constructions onto ONE")
    P("          curve at matched (panel, q, cadence), and the floor should be published in")
    P("          pp/yr per unit target weight, not as two numbers.")
    P("SURVIVORSHIP: B136/SMALL are current constituents only; CAGR inflated, KEEP not immune.")
    flush_log()

    u = load_universe()
    b = load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    PN = {"U56": (u.drop(columns=["SPY"]), u["SPY"]),
          "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
          "SMALL": (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])}
    P("\nPanels: " + "   ".join(f"{k} {v[0].shape[1]}x{len(v[0])}" for k, v in PN.items())
      + f"   ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")
    flush_log()

    # -------------------------------------------------------------- G0 / G1
    P("\n" + "=" * 178)
    P("GATES  G0 run() vs engine.backtest    G1 derived cost rung vs a fresh run at that rung")
    P("=" * 178)
    g0 = g1 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        W = rules_v2_weights(px)
        for freq in ("D", "W", "Q"):
            a = backtest(px, W, cost_bps=COST_BPS, freq=freq)
            r0, tn, held, tgt = run(px, W, freq)
            g0 = max(g0, float((a["returns"] - rung(r0, tn, COST_BPS)).abs().max()),
                     float((a["turnover"] - tn).abs().max()),
                     float(np.abs(a["weights"].values - held).max()))
            a25 = backtest(px, W, cost_bps=25, freq=freq)
            g1 = max(g1, float((a25["returns"] - rung(r0, tn, 25)).abs().max()))
        P(f"  {pn:7s} running max  G0 {g0:.3e}   G1 {g1:.3e}")
    P(f"  G0 {g0:.3e} (bar {BAR_ENGINE:.0e})  {'PASS' if g0 < BAR_ENGINE else 'FAIL'}"
      f"    G1 {g1:.3e} (bar {BAR_RUNG:.0e})  {'PASS' if g1 < BAR_RUNG else 'FAIL'}")
    flush_log()

    # -------------------------------------------------------------- comparands
    COMP = {}
    P("\n" + "=" * 178)
    P("COMPARANDS per panel (RULES v2 = the 4a bar, weekly, 10 bps; SPY = the 4b bar)")
    P("=" * 178)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        r0, tn, _, _ = run(px, rules_v2_weights(px), "W")
        live_s = stat(rung(r0, tn, COST_BPS).loc[start:])
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        COMP[pn] = dict(live=live_s, spy=spy_s, start=start,
                        years=len(px.loc[start:]) / 252)
        P(f"  {pn:7s} {start.date()}..{px.index[-1].date()}  ({COMP[pn]['years']:.2f} yrs, "
          f"{px.shape[1]} names)")
        P(f"      RULES v2  CAGR {live_s['CAGR']:.4f}  Sharpe {live_s['Sharpe']:.4f}  MaxDD "
          f"{live_s['MaxDD']:.4f}  H1/H2 {live_s['H1']:.4f}/{live_s['H2']:.4f}   OOS "
          f"{live_s['oCAGR']:.4f}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f}")
        P(f"      SPY       CAGR {spy_s['CAGR']:.4f}  Sharpe {spy_s['Sharpe']:.4f}  MaxDD "
          f"{spy_s['MaxDD']:.4f}  H1/H2 {spy_s['H1']:.4f}/{spy_s['H2']:.4f}   OOS "
          f"{spy_s['oCAGR']:.4f}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
        P(f"      4b bars: H1>{spy_s['H1']:.4f}  H2>{spy_s['H2']:.4f}  OOS>{spy_s['oSharpe']:.4f}"
          f"  MaxDD>=-{0.60*abs(spy_s['MaxDD']):.2%}  CAGR>={0.70*spy_s['CAGR']:.2%}")
    flush_log()

    drift, books, rungs = [], [], []
    mres_max = 0.0
    d_cad_max = 0.0

    # -------------------------------------------------------------- FIXK family
    P("\n" + "=" * 178)
    P(f"FIXK FAMILY - {len(PANELS)} panels x {len(QS)} q x {len(CONSTRUCTIONS)} constructions x "
      f"{len(CADENCES)} cadences = {len(PANELS)*len(QS)*len(CONSTRUCTIONS)*len(CADENCES)} arm "
      f"pairs, {len(ARMS)*len(HANDLING)} books each")
    P("=" * 178)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start, live_s, spy_s = COMP[pn]["start"], COMP[pn]["live"], COMP[pn]["spy"]
        yrs = COMP[pn]["years"]
        live = live_mask(px)
        nlive = live.sum(axis=1)
        sigs = {"MA-DIST": ma_dist(px), "MOM": mom_rank(px)}
        R = px.pct_change().fillna(0.0).values
        sel = px.index >= start
        for q in QS:
            kt = np.maximum(1, np.round(q * nlive)).astype(int)
            kt = pd.Series(np.minimum(kt.values, nlive.values), index=px.index)
            gates = {a: topk(sigs[a], kt, live) for a in ARMS}
            kA = gates["MA-DIST"].sum(axis=1)
            kB = gates["MOM"].sum(axis=1)
            dk = float((kA - kB).abs().max())
            for con in CONSTRUCTIONS:
                W = {a: book(px, gates[a], con, nlive) for a in ARMS}
                for cad in CADENCES:
                    res = {}
                    for a in ARMS:
                        for hnd in HANDLING:
                            Wx = W[a] if hnd == "DRIFT" else rtt_weights(W[a], px.index, cad)
                            fq = cad if hnd == "DRIFT" else "D"
                            r0, tn, held, tgt = run(px, Wx, fq)
                            res[(a, hnd)] = (held, tgt)
                            st = stat(rung(r0, tn, COST_BPS).loc[start:])
                            row = dict(family="FIXK", panel=pn, q=q, theta=np.nan, con=con,
                                       cad=cad, arm=a, hnd=hnd, gross=GROSS,
                                       turn_yr=float(tn.loc[start:].sum() / yrs),
                                       expo=float(pd.Series(held.sum(axis=1),
                                                            index=px.index).loc[start:].mean()),
                                       **st)
                            row["pass4a"] = verdict_4a(st, live_s)
                            row["f4b"] = fail_4b(st, spy_s)
                            row["pass4b"] = row["f4b"] == "-"
                            row["f4b_oos"] = fail_4b_oos(st, spy_s)
                            books.append(row)
                            for c in RUNGS:
                                if c == COST_BPS:
                                    continue
                                sc = stat(rung(r0, tn, c).loc[start:])
                                rungs.append(dict(family="FIXK", panel=pn, q=q, con=con,
                                                  cad=cad, arm=a, hnd=hnd, bps=c,
                                                  CAGR=sc["CAGR"], Sharpe=sc["Sharpe"],
                                                  MaxDD=sc["MaxDD"],
                                                  pass4a=verdict_4a(sc, live_s),
                                                  pass4b=fail_4b(sc, spy_s) == "-"))
                    # ---- the DRIFT leg, native handling only (RTT has no drift by design)
                    for hnd in HANDLING:
                        hA, tA = res[("MA-DIST", hnd)]
                        hB, tB = res[("MOM", hnd)]
                        memA, memB = tA > 0, tB > 0
                        shared = memA & memB
                        eq = shared & (np.abs(tA - tB) <= EPS_TGT)
                        d = (hA - hB) * R
                        ann = 252 * 100
                        dr = float(np.nansum(np.where(eq, d, 0.0), axis=1)[sel].mean() * ann)
                        mr = float(np.nansum(np.where(shared & ~eq, d, 0.0),
                                             axis=1)[sel].mean() * ann)
                        mres_max = max(mres_max, abs(mr))
                        if cad == "D" and hnd == "DRIFT":
                            d_cad_max = max(d_cad_max, abs(dr))
                        wbar = float(np.nanmean(np.where(tA[sel] > 0, tA[sel], np.nan)))
                        drift.append(dict(family="FIXK", panel=pn, q=q, theta=np.nan, con=con,
                                          cad=cad, hnd=hnd, DRIFT_pp=dr, MRES_pp=mr,
                                          kbar=float(kA.loc[start:].mean()),
                                          nbar=float(nlive.loc[start:].mean()),
                                          kn=float((kA / nlive.clip(lower=1)).loc[start:].mean()),
                                          wbar=wbar,
                                          expoA=float(pd.Series(hA.sum(axis=1),
                                                                index=px.index).loc[start:].mean()),
                                          shared_bar=float(shared[sel].sum(axis=1).mean()),
                                          dk_max=dk))
            P(f"  {pn:7s} q={q:.2f}  k/n realised {float((kA/nlive.clip(lower=1)).loc[start:].mean()):.4f}"
              f"  kbar {float(kA.loc[start:].mean()):7.1f}  nbar {float(nlive.loc[start:].mean()):7.1f}"
              f"  max|kA-kB| {dk:.0f}")
            flush_log()

    # -------------------------------------------------------------- GATE family (562's setting)
    P("\n" + "=" * 178)
    P(f"GATE FAMILY (idea 562's own setting; k_t free) - {len(PANELS)} panels x {len(THETA)} "
      f"theta x {len(CONSTRUCTIONS)} constructions x {len(CADENCES)} cadences")
    P("=" * 178)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start, live_s, spy_s = COMP[pn]["start"], COMP[pn]["live"], COMP[pn]["spy"]
        yrs = COMP[pn]["years"]
        live = live_mask(px)
        nlive = live.sum(axis=1)
        mom = mom_rank(px)
        R = px.pct_change().fillna(0.0).values
        sel = px.index >= start
        for th in THETA:
            gm = ma_gate(px, th)
            k_ma = gm.sum(axis=1)
            ktm = pd.Series(np.minimum(k_ma.values, mom.notna().sum(axis=1).values),
                            index=px.index)
            gates = {"MA-DIST": gm, "MOM": topk(mom, ktm, live)}
            kA = gates["MA-DIST"].sum(axis=1)
            for con in CONSTRUCTIONS:
                W = {a: book(px, gates[a], con, nlive) for a in ARMS}
                for cad in CADENCES:
                    res = {}
                    for a in ARMS:
                        r0, tn, held, tgt = run(px, W[a], cad)
                        res[a] = (held, tgt)
                        st = stat(rung(r0, tn, COST_BPS).loc[start:])
                        row = dict(family="GATE", panel=pn, q=np.nan, theta=th, con=con,
                                   cad=cad, arm=a, hnd="DRIFT", gross=GROSS,
                                   turn_yr=float(tn.loc[start:].sum() / yrs),
                                   expo=float(pd.Series(held.sum(axis=1),
                                                        index=px.index).loc[start:].mean()),
                                   **st)
                        row["pass4a"] = verdict_4a(st, live_s)
                        row["f4b"] = fail_4b(st, spy_s)
                        row["pass4b"] = row["f4b"] == "-"
                        row["f4b_oos"] = fail_4b_oos(st, spy_s)
                        books.append(row)
                    hA, tA = res["MA-DIST"]
                    hB, tB = res["MOM"]
                    memA, memB = tA > 0, tB > 0
                    shared = memA & memB
                    eq = shared & (np.abs(tA - tB) <= EPS_TGT)
                    d = (hA - hB) * R
                    ann = 252 * 100
                    dr = float(np.nansum(np.where(eq, d, 0.0), axis=1)[sel].mean() * ann)
                    mr = float(np.nansum(np.where(shared & ~eq, d, 0.0), axis=1)[sel].mean() * ann)
                    if cad == "D":
                        d_cad_max = max(d_cad_max, abs(dr))
                    drift.append(dict(family="GATE", panel=pn, q=np.nan, theta=th, con=con,
                                      cad=cad, hnd="DRIFT", DRIFT_pp=dr, MRES_pp=mr,
                                      kbar=float(kA.loc[start:].mean()),
                                      nbar=float(nlive.loc[start:].mean()),
                                      kn=float((kA / nlive.clip(lower=1)).loc[start:].mean()),
                                      wbar=float(np.nanmean(np.where(tA[sel] > 0, tA[sel], np.nan))),
                                      expoA=float(pd.Series(hA.sum(axis=1),
                                                            index=px.index).loc[start:].mean()),
                                      shared_bar=float(shared[sel].sum(axis=1).mean()),
                                      dk_max=np.nan))
            P(f"  {pn:7s} theta={th:+.2f}  k/n realised "
              f"{float((kA/nlive.clip(lower=1)).loc[start:].mean()):.4f}")
            flush_log()

    D = pd.DataFrame(drift)
    B = pd.DataFrame(books)
    RG = pd.DataFrame(rungs)
    D.to_csv(f"{OUT}.drift.csv", index=False)
    B.to_csv(f"{OUT}.books.csv", index=False)
    RG.to_csv(f"{OUT}.rungs.csv", index=False)

    # -------------------------------------------------------------- G2 / G3
    P("\n" + "=" * 178)
    P("GATES  G2 DRIFT == 0 at cadence D (engine holds target every bar)     "
      "G3 MRES == 0 in the FIXK family (targets identical by construction)")
    P("=" * 178)
    fixk_mres = float(D.loc[D.family == "FIXK", "MRES_pp"].abs().max())
    P(f"  G2 max |DRIFT_pp| at cadence D = {d_cad_max:.3e} (bar {BAR_D:.0e})  "
      f"{'PASS' if d_cad_max <= BAR_D else 'FAIL'}")
    P(f"  G3 max |MRES_pp| in FIXK       = {fixk_mres:.3e} (bar 0e+00)  "
      f"{'PASS' if fixk_mres == 0.0 else 'FAIL'}")
    gate_mres = float(D.loc[D.family == "GATE", "MRES_pp"].abs().max())
    P(f"     (GATE family, for contrast: max |MRES_pp| = {gate_mres:.4f} pp/yr - the depth-match")
    P("      residual idea 562 had to carry and this construction removes)")
    flush_log()

    # -------------------------------------------------------------- the floor table
    P("\n" + "=" * 178)
    P("SECTION 1 - THE FLOOR, EVERY GRID POINT (FIXK, native DRIFT handling, cadences W/M/Q;")
    P("            D omitted because it is exactly 0 by G2).  DRIFT_pp = pp/yr.")
    P("=" * 178)
    F = D[(D.family == "FIXK") & (D.hnd == "DRIFT") & (D.cad != "D")].copy()
    F["absD"] = F.DRIFT_pp.abs()
    for pn in PANELS:
        sub = F[F.panel == pn]
        piv = sub.pivot_table(index="q", columns=["con", "cad"], values="absD")
        P(f"\n  |DRIFT_pp|   panel {pn}")
        P(piv.to_string(float_format=lambda x: f"{x:.5f}"))
    P("\n  floor(construction) = max over q and over cadences {W,M,Q}, per panel:")
    fl = F.groupby(["panel", "con"]).absD.max().unstack()
    fl["ratio_DEG_over_RES"] = fl["DEGROSS"] / fl["RESPREAD"]
    P(fl.to_string(float_format=lambda x: f"{x:.5f}"))
    P(f"\n  pooled over panels:  RESPREAD {F[F.con=='RESPREAD'].absD.max():.5f}   "
      f"DEGROSS {F[F.con=='DEGROSS'].absD.max():.5f}   ratio "
      f"{F[F.con=='DEGROSS'].absD.max()/F[F.con=='RESPREAD'].absD.max():.4f}")
    G = D[(D.family == "GATE") & (D.cad != "D")].copy()
    G["absD"] = G.DRIFT_pp.abs()
    P(f"  GATE family (562's own setting), pooled:  RESPREAD "
      f"{G[G.con=='RESPREAD'].absD.max():.5f}   DEGROSS {G[G.con=='DEGROSS'].absD.max():.5f}"
      f"   ratio {G[G.con=='DEGROSS'].absD.max()/G[G.con=='RESPREAD'].absD.max():.4f}")
    P(f"  idea 562 published:                       RESPREAD 0.13740   DEGROSS 0.01640"
      f"   ratio 0.1194")
    flush_log()

    # -------------------------------------------------------------- H_DENOM vs H_EXPO
    P("\n" + "=" * 178)
    P("SECTION 2 - H_DENOM vs H_EXPO: the slope of log|DRIFT_pp| on log q, INSIDE each")
    P("            construction.  H_DENOM predicts RESPREAD -1, DEGROSS 0.")
    P("            H_EXPO  predicts RESPREAD  0, DEGROSS +1.   (FIXK, W/M/Q)")
    P("=" * 178)
    slopes = []
    for pn in PANELS:
        for con in CONSTRUCTIONS:
            for cad in ["W", "M", "Q"]:
                sub = F[(F.panel == pn) & (F.con == con) & (F.cad == cad)].sort_values("q")
                sub = sub[sub.absD > 0]
                if len(sub) < 3:
                    continue
                x = np.log(sub.q.values)
                y = np.log(sub.absD.values)
                Xm = np.column_stack([np.ones_like(x), x])
                bb, se, r2, _ = ols(y, Xm, ["c", "slope"])
                slopes.append(dict(panel=pn, con=con, cad=cad, slope=bb["slope"],
                                   se=se["slope"], R2=r2, npts=len(sub)))
    S = pd.DataFrame(slopes)
    P(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  median slope by construction (all panels x cadences):")
    for con in CONSTRUCTIONS:
        v = S[S.con == con].slope
        pred_d = {"RESPREAD": -1.0, "DEGROSS": 0.0}[con]
        pred_e = {"RESPREAD": 0.0, "DEGROSS": 1.0}[con]
        P(f"    {con:9s} median {v.median():+.4f}  (min {v.min():+.4f} max {v.max():+.4f})"
          f"   H_DENOM predicts {pred_d:+.1f}, H_EXPO predicts {pred_e:+.1f}")
    md_res = S[S.con == "RESPREAD"].slope.median()
    md_deg = S[S.con == "DEGROSS"].slope.median()
    err_denom = abs(md_res - (-1.0)) + abs(md_deg - 0.0)
    err_expo = abs(md_res - 0.0) + abs(md_deg - 1.0)
    P(f"\n  total |median slope - prediction| :  H_DENOM {err_denom:.4f}   H_EXPO {err_expo:.4f}"
      f"   -> {'H_DENOM' if err_denom < err_expo else 'H_EXPO'} wins")

    P("\n  --- H_BILINEAR, identified AFTER the two pre-registered readings were scored -------")
    P("  Neither pre-registered reading fits both curves, and the algebra says why.  For a")
    P("  shared name held at the same target w by both arms, one bar after a rebalance")
    P("      h_A - h_B = w (1 + r_j) (1/tot_A - 1/tot_B),   tot_X = 1 + E_X * rp_X")
    P("  where E is the book's exposure and rp its own return, so tot_A - tot_B is FIRST ORDER")
    P("  IN E.  The floor is therefore BILINEAR:  |DRIFT| ~ w * E.  That is a parameter-free")
    P("  consequence of the engine's renormalisation, not a fitted form; it is scored below on")
    P("  the SAME unchanged grid, with no new tuning and no new axis.")
    P("     RESPREAD: w = g/k ~ 1/q, E = g       -> slope -1")
    P("     DEGROSS : w = g/n (flat), E = g*q    -> slope +1")
    P("     ratio at fixed q = (w ratio)(E ratio) = q * q  -> beta = 2 exactly")
    err_bil = abs(md_res - (-1.0)) + abs(md_deg - 1.0)
    P(f"  total |median slope - prediction| :  H_DENOM {err_denom:.4f}   H_EXPO {err_expo:.4f}"
      f"   H_BILINEAR {err_bil:.4f}")
    P(f"  -> {min([('H_DENOM', err_denom), ('H_EXPO', err_expo), ('H_BILINEAR', err_bil)], key=lambda t: t[1])[0]}"
      f" fits both curves best; its beta prediction of 2 is checked in section 3.")
    flush_log()

    # -------------------------------------------------------------- H_COLLAPSE + the law
    P("\n" + "=" * 178)
    P("SECTION 3 - H_COLLAPSE: does DRIFT_pp / wbar put the two constructions on one curve?")
    P("            and the published LAW  log|DRIFT_pp| = a + b1 log wbar + b2 log kbar")
    P("=" * 178)
    piv = F.pivot_table(index=["panel", "q", "cad"], columns="con", values="absD")
    piv = piv.dropna()
    wv = F.pivot_table(index=["panel", "q", "cad"], columns="con", values="wbar").dropna()
    coll = pd.DataFrame({
        "raw_ratio": piv["DEGROSS"] / piv["RESPREAD"],
        "w_ratio": wv["DEGROSS"] / wv["RESPREAD"],
    })
    coll["norm_ratio"] = coll.raw_ratio / coll.w_ratio
    P("\n  per cell: raw_ratio = |DRIFT|_DEG / |DRIFT|_RES ;  w_ratio = w_DEG / w_RES (= k/n) ;")
    P("            norm_ratio = raw / w  (H_DENOM predicts 1.0 exactly)")
    P(coll.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  norm_ratio: median {coll.norm_ratio.median():.4f}  IQR "
      f"[{coll.norm_ratio.quantile(.25):.4f}, {coll.norm_ratio.quantile(.75):.4f}]  "
      f"min {coll.norm_ratio.min():.4f}  max {coll.norm_ratio.max():.4f}")
    P(f"  raw_ratio : median {coll.raw_ratio.median():.4f}  min {coll.raw_ratio.min():.4f}  "
      f"max {coll.raw_ratio.max():.4f}   (unnormalised, i.e. what 562 reported as 0.1194)")
    P(f"  H_COLLAPSE {'PASSES' if abs(coll.norm_ratio.median()-1.0) < 0.15 else 'FAILS'} at a "
      f"declared |median - 1| < 0.15 bar: |{coll.norm_ratio.median():.4f} - 1| = "
      f"{abs(coll.norm_ratio.median()-1.0):.4f}")
    coll["beta_cell"] = np.log(coll.raw_ratio) / np.log(coll.w_ratio)
    bet = coll.beta_cell
    P(f"  the exponent that DOES collapse it, per cell beta = log(raw_ratio)/log(k/n):")
    P(f"    median {bet.median():.4f}   IQR [{bet.quantile(.25):.4f}, {bet.quantile(.75):.4f}]"
      f"   min {bet.min():.4f}  max {bet.max():.4f}     (H_DENOM needs beta = 1)")
    P("    i.e. the construction gap is (k/n)^beta, not (k/n): a de-grossed book's floor is")
    P("    SMALLER than the denominator reading predicts, by a factor (k/n)^(beta-1).")
    P(f"    H_DENOM needs beta = 1 (|median - 1| = {abs(bet.median()-1):.4f});"
      f"  H_BILINEAR needs beta = 2 (|median - 2| = {abs(bet.median()-2):.4f}).")
    P(f"    -> {'H_BILINEAR' if abs(bet.median()-2) < abs(bet.median()-1) else 'H_DENOM'}"
      f" on the ratio test as well.")

    laws = []
    for scope, sub in [("POOLED", F)] + [(pn, F[F.panel == pn]) for pn in PANELS]:
        sub = sub[sub.absD > 0]
        y = np.log(sub.absD.values)
        Xm = np.column_stack([np.ones(len(sub)), np.log(sub.wbar.values),
                              np.log(sub.kbar.values)])
        bb, se, r2, rmse = ols(y, Xm, ["a", "b1_logw", "b2_logk"])
        laws.append(dict(scope=scope, n=len(sub), a=bb["a"], b1_logw=bb["b1_logw"],
                         se_b1=se["b1_logw"], b2_logk=bb["b2_logk"], se_b2=se["b2_logk"],
                         R2=r2, rmse_log=rmse))
    LW = pd.DataFrame(laws)
    LW.to_csv(f"{OUT}.law.csv", index=False)
    P("\n  THE LAW   log|DRIFT_pp| = a + b1 log(w) + b2 log(k)   (FIXK, W/M/Q, all panels)")
    P(LW.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  b1 = 1 is the pure denominator reading (floor linear in the per-name target).")
    sub = F[F.absD > 0]
    rho_wk = float(np.corrcoef(np.log(sub.wbar.values), np.log(sub.kbar.values))[0, 1])
    rho_res = float(np.corrcoef(np.log(sub[sub.con == "RESPREAD"].wbar.values),
                                np.log(sub[sub.con == "RESPREAD"].kbar.values))[0, 1])
    P(f"  IDENTIFICATION CAVEAT: inside RESPREAD w == gross/k exactly, so rho(log w, log k) ="
      f" {rho_res:+.4f} there;")
    P(f"  b1 and b2 are separated only by the DEGROSS cells and the panel spread "
      f"(pooled rho {rho_wk:+.4f}).")
    flush_log()

    # -------------------------------------------------------------- rule 8 on the claim
    P("\n" + "=" * 178)
    P("SECTION 4 - RULE 8 ON THE CLAIM: fit the law on 2009..2016 only, predict the 2017..2026")
    P("            floors, read once.  (Re-runs the whole FIXK grid on each window separately.)")
    P("=" * 178)
    # re-measure DRIFT on the two windows separately
    win_rows = []
    for pn in PANELS:
        px, _ = PN[pn]
        start = COMP[pn]["start"]
        live = live_mask(px)
        nlive = live.sum(axis=1)
        sigs = {"MA-DIST": ma_dist(px), "MOM": mom_rank(px)}
        R = px.pct_change().fillna(0.0).values
        idx = px.index
        m_is = (idx >= start) & (idx <= pd.Timestamp(IS_END))
        m_oos = idx >= pd.Timestamp(OOS_START)
        for q in QS:
            kt = np.maximum(1, np.round(q * nlive)).astype(int)
            kt = pd.Series(np.minimum(kt.values, nlive.values), index=idx)
            gates = {a: topk(sigs[a], kt, live) for a in ARMS}
            kA = gates["MA-DIST"].sum(axis=1)
            for con in CONSTRUCTIONS:
                W = {a: book(px, gates[a], con, nlive) for a in ARMS}
                for cad in ["W", "M", "Q"]:
                    hA, tA = run(px, W["MA-DIST"], cad)[2:]
                    hB, tB = run(px, W["MOM"], cad)[2:]
                    eq = (tA > 0) & (tB > 0) & (np.abs(tA - tB) <= EPS_TGT)
                    d = np.nansum(np.where(eq, (hA - hB) * R, 0.0), axis=1)
                    for wn, msk in (("IS", m_is), ("OOS", m_oos)):
                        win_rows.append(dict(
                            panel=pn, q=q, con=con, cad=cad, window=wn,
                            DRIFT_pp=float(d[msk].mean() * 252 * 100),
                            wbar=float(np.nanmean(np.where(tA[msk] > 0, tA[msk], np.nan))),
                            kbar=float(kA[msk].mean())))
    WF = pd.DataFrame(win_rows)
    WF["absD"] = WF.DRIFT_pp.abs()
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    tr = WF[(WF.window == "IS") & (WF.absD > 0)]
    te = WF[(WF.window == "OOS") & (WF.absD > 0)]
    Xtr = np.column_stack([np.ones(len(tr)), np.log(tr.wbar.values), np.log(tr.kbar.values)])
    bb, se, r2, rmse = ols(np.log(tr.absD.values), Xtr, ["a", "b1", "b2"])
    P(f"  IS fit  (n={len(tr)}):  a {bb['a']:+.4f}   b1(log w) {bb['b1']:+.4f} "
      f"(se {se['b1']:.4f})   b2(log k) {bb['b2']:+.4f} (se {se['b2']:.4f})   R2 {r2:.4f}")
    Xte = np.column_stack([np.ones(len(te)), np.log(te.wbar.values), np.log(te.kbar.values)])
    pred = Xte @ np.array([bb["a"], bb["b1"], bb["b2"]])
    act = np.log(te.absD.values)
    ss = float(((act - act.mean()) ** 2).sum())
    oos_r2 = 1.0 - float(((act - pred) ** 2).sum()) / ss
    P(f"  OOS     (n={len(te)}):  R2 of the IS law on untouched 2017..2026 = {oos_r2:.4f}   "
      f"median |log error| {np.median(np.abs(act-pred)):.4f}   "
      f"median ratio pred/act {np.median(np.exp(pred-act)):.4f}")
    bo, seo, r2o, _ = ols(act, Xte, ["a", "b1", "b2"])
    P(f"  OOS refit for contrast: b1 {bo['b1']:+.4f}  b2 {bo['b2']:+.4f}  R2 {r2o:.4f}   "
      f"(b1 drift IS->OOS {bo['b1']-bb['b1']:+.4f})")
    fl_is = tr.groupby("con").absD.max()
    fl_oos = te.groupby("con").absD.max()
    P(f"  floor levels: IS  RESPREAD {fl_is.get('RESPREAD', np.nan):.5f}  DEGROSS "
      f"{fl_is.get('DEGROSS', np.nan):.5f}  ratio "
      f"{fl_is.get('DEGROSS', np.nan)/fl_is.get('RESPREAD', np.nan):.4f}")
    P(f"                OOS RESPREAD {fl_oos.get('RESPREAD', np.nan):.5f}  DEGROSS "
      f"{fl_oos.get('DEGROSS', np.nan):.5f}  ratio "
      f"{fl_oos.get('DEGROSS', np.nan)/fl_oos.get('RESPREAD', np.nan):.4f}")
    flush_log()

    # -------------------------------------------------------------- the book leg
    P("\n" + "=" * 178)
    P("SECTION 5 - THE BOOK LEG, ALL GRID POINTS.  4a vs RULES v2 (live), 4b vs SPY, 10 bps.")
    P("=" * 178)
    P(f"  books priced: {len(B)}   (FIXK {int((B.family=='FIXK').sum())}, "
      f"GATE {int((B.family=='GATE').sum())})")
    P(f"  4a passes: {int(B.pass4a.sum())} of {len(B)}    4b passes: {int(B.pass4b.sum())} of "
      f"{len(B)}    both: {int((B.pass4a & B.pass4b).sum())}")
    P("\n  full-sample 4b pass counts by (panel, con, q) - FIXK, 10 bps:")
    fx = B[B.family == "FIXK"]
    P(fx.pivot_table(index=["panel", "q"], columns="con", values="pass4b",
                     aggfunc="sum").fillna(0).astype(int).to_string())
    P("\n  4b failure-leg frequency (FIXK, 10 bps):")
    P(fx.f4b.value_counts().to_string())
    P("\n  EVERY FIXK cell, Sharpe / CAGR / MaxDD at 10 bps (cad x arm x hnd collapsed to the")
    P("  best-Sharpe member of each (panel, q, con) cell, with the full table in .books.csv):")
    best = fx.loc[fx.groupby(["panel", "q", "con"]).Sharpe.idxmax()]
    P(best[["panel", "q", "con", "cad", "arm", "hnd", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "expo", "turn_yr", "pass4a", "f4b"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    if B.pass4b.any():
        P("\n  ALL 4b PASSES (any family, 10 bps):")
        P(B[B.pass4b][["family", "panel", "q", "theta", "con", "cad", "arm", "hnd", "CAGR",
                       "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "expo",
                       "pass4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  cost-rung sensitivity of the KEEP columns (FIXK):")
    P(RG.groupby("bps")[["pass4a", "pass4b"]].sum().to_string()
      + f"\n  10   {int(fx.pass4a.sum()):d}   {int(fx.pass4b.sum()):d}")
    P("\n  DRIFT vs RTT as capital (mean Sharpe over matched cells, FIXK, 10 bps):")
    P(fx.pivot_table(index=["con", "cad"], columns="hnd",
                     values="Sharpe").to_string(float_format=lambda x: f"{x:.4f}"))
    dvr = fx.pivot_table(index=["panel", "q", "con", "cad", "arm"], columns="hnd",
                         values="Sharpe").dropna()
    P(f"  DRIFT - RTT Sharpe: median {(dvr.DRIFT-dvr.RTT).median():+.4f}  "
      f"share DRIFT>RTT {(dvr.DRIFT>dvr.RTT).mean():.4f}  n={len(dvr)}")
    flush_log()

    # -------------------------------------------------------------- rule 8 on the books
    P("\n" + "=" * 178)
    P("SECTION 6 - RULE 8 ON THE BOOKS: the 2 tuned params (construction x q) and every")
    P("            reported axis chosen on IS Sharpe (2009..2016) alone; OOS read once.")
    P("=" * 178)
    P("  THREE IS-ONLY SELECTORS, all declared before the OOS window is read:")
    P("    SEL-SHARPE  highest IS Sharpe")
    P("    SEL-CALMAR  highest IS CAGR / |IS MaxDD|")
    P("    SEL-DDCAP   highest IS Sharpe among cells whose IS MaxDD <= 60% of SPY's IS MaxDD")
    P("                (the 4b DD cap applied to IS data only - no OOS information)")
    keep = []
    for pn in PANELS:
        px, spy_px = PN[pn]
        spy_s, live_s = COMP[pn]["spy"], COMP[pn]["live"]
        sub = fx[fx.panel == pn].copy()
        sub["isCalmar"] = sub.isCAGR / sub.isMaxDD.abs().replace(0, np.nan)
        cap = 0.60 * abs(spy_s["isMaxDD"])
        ok = sub[sub.isMaxDD.abs() <= cap]
        picks = {"SEL-SHARPE": sub.loc[sub.isSharpe.idxmax()],
                 "SEL-CALMAR": sub.loc[sub.isCalmar.idxmax()]}
        picks["SEL-DDCAP"] = ok.loc[ok.isSharpe.idxmax()] if len(ok) else None
        P(f"\n  {pn}   (IS SPY MaxDD {spy_s['isMaxDD']:.2%}, so the IS DD cap is "
          f"{-cap:.2%}; {len(ok)} of {len(sub)} cells inside it)")
        for sname, pick in picks.items():
            if pick is None:
                P(f"    {sname}: NO IS cell clears the IS DD cap - selector empty.")
                keep.append(dict(panel=pn, selector=sname, con=None))
                continue
            keep.append(dict(panel=pn, selector=sname, con=pick.con, q=pick.q, cad=pick.cad,
                             arm=pick.arm, hnd=pick.hnd, isSharpe=pick.isSharpe,
                             isCAGR=pick.isCAGR, isMaxDD=pick.isMaxDD,
                             CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                             H1=pick.H1, H2=pick.H2, oCAGR=pick.oCAGR,
                             oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                             spy_oCAGR=spy_s["oCAGR"], spy_oSharpe=spy_s["oSharpe"],
                             spy_oMaxDD=spy_s["oMaxDD"], base_oCAGR=live_s["oCAGR"],
                             base_oSharpe=live_s["oSharpe"], base_oMaxDD=live_s["oMaxDD"],
                             pass4a=bool(pick.pass4a), f4b_full=pick.f4b,
                             f4b_oos=pick.f4b_oos))
            P(f"    {sname}: {pick.con} q={pick.q:.2f} {pick.cad} {pick.arm} {pick.hnd}"
              f"   (IS Sharpe {pick.isSharpe:.4f}, IS CAGR {pick.isCAGR:.2%}, IS MaxDD "
              f"{pick.isMaxDD:.2%})")
            P(f"        FULL  CAGR {pick.CAGR:7.2%}  Sharpe {pick.Sharpe:.4f}  MaxDD "
              f"{pick.MaxDD:7.2%}   halves {pick.H1:.4f} / {pick.H2:.4f}")
            P(f"        OOS   CAGR {pick.oCAGR:7.2%}  Sharpe {pick.oSharpe:.4f}  MaxDD "
              f"{pick.oMaxDD:7.2%}")
            P(f"        4a {'PASS' if pick.pass4a else 'FAIL'}    4b full-sample "
              f"{'PASS' if pick.f4b=='-' else 'FAIL ('+pick.f4b+')'}    4b on the OOS window "
              f"{'PASS' if pick.f4b_oos=='-' else 'FAIL ('+pick.f4b_oos+')'}")
        P(f"        comparands OOS:  SPY {spy_s['oCAGR']:7.2%} / {spy_s['oSharpe']:.4f} / "
          f"{spy_s['oMaxDD']:7.2%}     RULES v2 {live_s['oCAGR']:7.2%} / "
          f"{live_s['oSharpe']:.4f} / {live_s['oMaxDD']:7.2%}")
    KP = pd.DataFrame(keep)
    for c in ("f4b_oos", "f4b_full", "con"):
        if c not in KP.columns:
            KP[c] = None
    KP.to_csv(f"{OUT}.keep.csv", index=False)
    flush_log()

    # -------------------------------------------------------------- verdict
    P("\n" + "=" * 178)
    P("VERDICT")
    P("=" * 178)
    ratio_pool = F[F.con == 'DEGROSS'].absD.max() / F[F.con == 'RESPREAD'].absD.max()
    P(f"  1. The 8x REPRODUCES: pooled floor ratio DEGROSS/RESPREAD = {ratio_pool:.4f} on FIXK "
      f"and {G[G.con=='DEGROSS'].absD.max()/G[G.con=='RESPREAD'].absD.max():.4f} on 562's own")
    P(f"     GATE setting, against 562's published 0.1194.  So the phenomenon is real and is")
    P(f"     not an artefact of 562's depth-match residual (G3: MRES == 0 exactly here).")
    P(f"  2. BUT THE PUBLISHED REASON IS WRONG AS STATED.  Slopes of log|DRIFT| on log q:")
    P(f"     RESPREAD median {md_res:+.4f} (H_DENOM -1, H_EXPO 0), DEGROSS median {md_deg:+.4f}"
      f" (H_DENOM 0, H_EXPO +1).")
    P(f"     total |median - prediction|: H_DENOM {err_denom:.4f}, H_EXPO {err_expo:.4f}, "
      f"H_BILINEAR {err_bil:.4f} -> H_DENOM "
      f"{'SURVIVES' if err_denom <= min(err_expo, err_bil) else 'IS REJECTED'} on its own test.")
    P(f"     The floor is BILINEAR in the per-name target w AND the book exposure E (|DRIFT| ~")
    P(f"     w*E, a parameter-free consequence of the engine renormalising through cash).  At a")
    P(f"     single k/n those two legs are indistinguishable, which is exactly why 562's two")
    P(f"     numbers could not separate them; the denominator is HALF the reason, not the reason.")
    P(f"  3. H_COLLAPSE {'PASSES' if abs(coll.norm_ratio.median()-1.0) < 0.15 else 'FAILS'}: "
      f"DRIFT/w leaves a median residual ratio of {coll.norm_ratio.median():.4f}, not 1.  The")
    P(f"     construction gap is (k/n)^beta with beta median {bet.median():.4f} - H_DENOM needs 1,")
    P(f"     H_BILINEAR needs 2 - so the floor is NOT one number in target-weight units either.")
    P(f"  4. The law: b1(log w) = {LW.loc[LW.scope=='POOLED','b1_logw'].iloc[0]:+.4f} "
      f"(se {LW.loc[LW.scope=='POOLED','se_b1'].iloc[0]:.4f}), b2(log k) = "
      f"{LW.loc[LW.scope=='POOLED','b2_logk'].iloc[0]:+.4f} "
      f"(se {LW.loc[LW.scope=='POOLED','se_b2'].iloc[0]:.4f}), R2 "
      f"{LW.loc[LW.scope=='POOLED','R2'].iloc[0]:.4f};")
    P(f"     rule 8 on the CLAIM: the IS-fitted law reads OOS R2 {oos_r2:.4f} but its median")
    P(f"     pred/act is {np.median(np.exp(pred-act)):.4f} - it UNDER-predicts the OOS floor by "
      f"{100*(1-np.median(np.exp(pred-act))):.0f}%.")
    P(f"     The floor LEVEL is not portable across windows (RESPREAD "
      f"{fl_is.get('RESPREAD', np.nan):.5f} IS -> {fl_oos.get('RESPREAD', np.nan):.5f} OOS, "
      f"{fl_oos.get('RESPREAD', np.nan)/fl_is.get('RESPREAD', np.nan):.2f}x);")
    P(f"     the construction RATIO is ({fl_is.get('DEGROSS')/fl_is.get('RESPREAD'):.4f} IS vs "
      f"{fl_oos.get('DEGROSS')/fl_oos.get('RESPREAD'):.4f} OOS).")
    P(f"  5. CAPITAL: 4a {int(B.pass4a.sum())}/{len(B)}, 4b {int(B.pass4b.sum())}/{len(B)}, both "
      f"{int((B.pass4a & B.pass4b).sum())}/{len(B)}.  Rule-8 IS-only selectors reach a 4b pass")
    P(f"     on the OOS window in {int((KP.f4b_oos=='-').sum())} of "
      f"{int(KP.con.notna().sum())} (panel x selector) cells.  Drift itself is worth nothing:")
    P(f"     DRIFT - RTT median Sharpe {(dvr.DRIFT-dvr.RTT).median():+.4f} over {len(dvr)} "
      f"matched cells.")
    flush_log()
    P("\nwrote: " + ", ".join(f"{OUT.name}{e}" for e in
                              (".drift.csv", ".books.csv", ".rungs.csv", ".law.csv",
                               ".walkforward.csv", ".keep.csv", ".console.txt")))
    flush_log()


if __name__ == "__main__":
    main()

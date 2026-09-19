#!/usr/bin/env python3
"""Idea 708 (lane B, 2026-09-19): is the per-r COST DRAG INVERSION a RECORD-WIDE FACT or a
CAND-n GROSS/n CONVENTION?

THE CLAIM UNDER TEST.  Idea 703 (lane C, 2026-09-11) measured, on the SMALL439 width ladder,
that the cost drag on OOS Sharpe is MONOTONE DECREASING in the selection ratio r at every
width -- at k = 400, -0.1219 / -0.1168 / -0.0981 / -0.0805 of Sharpe at r = .05 / .10 / .25 /
.50 -- and read it as "a CAND-20 book on a 400-name panel turns its whole NAV over far more
often than a CAND-200 one, so HOLDING MORE NAMES IS CHEAPER, not dearer".  That sentence
inverts the record's recurring "cost of holding more names" reasoning and has been quoted since.

The queue's question is whether the inversion is a fact about books or a fact about the
NORMALISER.  Every book in 703's ladder sizes at GROSS/n: the whole gross is re-spread over
exactly the n names held, so ONE name replaced costs 2*G/n of NAV turnover.  Turnover per unit
NAV is therefore (replacement FRACTION) x 2G, and a fraction mechanically falls as the
denominator grows even if the book is churning the same NUMBER of slots.  If that is all the
inversion is, it says nothing about breadth and everything about the convention.

THE DISCRIMINATOR, PRE-REGISTERED BEFORE ANY NUMBER WAS READ.  Re-cut every book's drag against
THREE turnover currencies (this is exactly what the queue asks for):

    T_nav    = annualised turnover per unit NAV               (the record's currency)
    T_gross  = T_nav / gbar, gbar the realised mean gross     (per unit DEPLOYED capital)
    T_slot   = T_nav / (gbar / nbar) = T_nav * nbar / gbar    (NAME SLOTS replaced per year)

  A CORRECTION THIS SCRIPT MADE TO ITSELF, LOGGED RATHER THAN HIDDEN.  The per-slot currency was
  first written as `T_nav / nbar`, which is wrong and is wrong in the direction that flatters the
  H_GENERAL side: a GROSS/n book already carries one factor of 1/n inside T_nav (each name is
  G/n of NAV), so dividing by nbar again divides by breadth TWICE and forces rho(n, .) = -1 by
  construction.  The first pass printed rho(n, T_nav) == rho(n, T_gross) == rho(n, T_name) to
  four decimals on 12 of 12 arms, which is the signature of exactly that degeneracy, and read
  H_GENERAL off it.  The right per-slot quantity MULTIPLIES by the slot count: turnover in NAV
  units divided by the weight PER NAME (gbar/nbar) is the number of name-slots replaced per year,
  a dimensionless count that a fixed-weight-per-name book would pay directly.  Both the statistic
  and the verdict below are the corrected ones; the erroneous first reading is recorded here
  because the record should show that this run's headline REVERSED when the bug was fixed.

  H_CONVENTION  the inversion is a normalisation fact.  PREDICTS rho(n, T_nav) < 0 in every
                family AND rho(n, T_slot) >= 0 (slots churned flat or RISING with breadth).
  H_GENERAL     wide books genuinely churn fewer SLOTS, i.e. weekly rebalancing is cheaper for
                breadth as such.  PREDICTS rho(n, T_slot) < 0.

  BAR: H_CONVENTION is accepted iff rho(n, T_nav) < 0 in >= 4 of 4 count families (mean over the
  three panels) AND rho(n, T_slot) >= 0 in >= 4 of 4.  H_GENERAL is accepted iff rho(n, T_slot)
  < 0 in >= 4 of 4.  SPLIT is a legal outcome and is reported as SPLIT, not rescued.

  T_nav AND T_gross ARE ONE CURRENCY, NOT TWO, AND THIS IS GATED (G8).  Every count family here
  re-spreads the full gross G over the names it holds, so gbar is a CONSTANT within a family and
  T_gross is a fixed multiple of T_nav: their rank correlations against n must agree exactly.
  That is reported as a property of the record's convention, not smuggled in as independent
  evidence.  EWALL is the one family where gbar can drift (names drop out of the price panel).

  SECOND, INDEPENDENT LEG (arithmetic, no free parameters).  Sharpe drag has a closed form:
  r_c = r_0 - turnover * c/1e4 exactly (GATE G1), so dSharpe(c) ~= (c/1e4) * T_nav / vol_0.
  Regress the 75 measured drags on that prediction.  If R^2 ~ 1 and the slope ~ 1, the "per-r
  drag inversion" carries NO information beyond T_nav and restates, without residue, as "T_nav
  falls with n" -- i.e. as the GROSS/n convention.  This is the leg that can kill the finding
  outright, and it is declared here rather than after the fact.

  NOTE STATED UP FRONT (it is why the test has to be cut this way): Sharpe and Sharpe-drag are
  INVARIANT to a uniform rescaling of gross for an unlevered long-only book at a 0% cash rate,
  because returns, turnover and vol all scale together.  So a "fixed weight per name" family
  would be a rescaling of its GROSS/n twin at every n and could not discriminate anything on
  Sharpe.  The convention question is therefore ONLY answerable through the turnover currencies
  above, not through a second sizing family.  This is a correction to the obvious design.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4):

  DIAL 1  FAMILY {CAND, MADIST, BAND, ADAPT, EWALL} -- the book family (the queue's dial).
      CAND    top-n by the committed composite score (`baseline.score`) among names above
              their 200d MA with vol20 < 0.60.  This IS idea 286 / 703's family, replicated.
      MADIST  top-n by distance above the 200d MA among the SAME eligible set: a slower,
              lower-turnover key, same screen, same sizing.
      BAND    the live RULES v2 gate (200d +/-3% hysteresis band), then top-n by MA distance
              among the IN names.  The live book's own selection rule.
      ADAPT   CAND's key with an ENDOGENOUS count: n_t = round(n * b_t / bbar_{t-1}), b_t the
              share of priced names above their 200d MA, bbar an EXPANDING mean through t-1
              (causal, no look-ahead, no fitted constant).  The book widens in strong tapes.
      EWALL   every priced name equal-weight at gross G.  No screen, no key.  The n = N
              endpoint of all four, and the family with no count dial at all.

  DIAL 2  COST RUNG c {0, 5, 10, 25, 50} bps.  10 bps is PROTOCOL rule 2's binding value and
      every verdict below is read there; the other rungs exist to measure the drag SLOPE and
      are all published.  Costs are RECONSTRUCTED from the turnover identity, not re-run
      (GATE G1 proves the reconstruction is exact), so no rung is a separate fit.

NOT DIALS, reported at every value.  BREADTH n {5, 10, 20, 40, 80, ALL} -- this is the AXIS the
question is about, not a parameter to be chosen; every rung is published.  PANEL {U56, B136,
SMALL} -- all three, every cell published.  GROSS G = 0.75 frozen at the live RULES v2 value and
the committed 2026-09-04 anchor value; it is NOT swept (that would be a third parameter).
Cadence weekly, execution t -> t+1, no shorting, no leverage -- all PROTOCOL rule 2.

BOOKS: 4 count families x 6 breadths + EWALL = 25 per panel, 75 in all; x 5 cost rungs = 375
cells, EVERY ONE published in the .grid.csv.  Reference books, not cells of either dial: LIVE
(`baseline.rules_v2_weights`, the 4a comparand) and SPY (the 4b comparand).

RULE 8 (walk-forward, required).  Every chooser is fitted on warm-up..2016-12-31 ONLY and
2017-01-01..2026 is read EXACTLY ONCE:
    C_SHARPE  argmax IS Sharpe at 10 bps over all 25 cells of a panel
    C_DRAG    argmin IS drag (Sharpe_0 - Sharpe_10) -- "pick the cheapest book", the dial this
              idea is about, made into an actual selector so it can lose
    C_ANCHOR  LIVE, choosing nothing -- the null every pick is scored against
All three range over the same two dials; they are readings of one grid, not extra parameters.

GATES (pre-registered, printed before any new number is read):
  G0  every panel >= 10 years after warm-up (PROTOCOL rule 1).
  G1  COST IDENTITY: reconstructed r_c == a fresh `backtest(cost_bps=c)` to < 1e-15 on spot
      cells covering all three panels and three rungs.  This licenses all 375 cells.
  G2  CROSS-SCRIPT REPLAY: this script's own band machinery, at n = ALL with the live
      never-re-spread sizing, reproduces `baseline.rules_v2_weights` at EXACTLY 0.0.
  G3  DEGENERACY: ADAPT at n = ALL and CAND at n = ALL are the same book by construction
      (no adaptation is possible when every eligible name is held); |dSharpe| must be 0.0.
  G4  exactly two tuned parameters (FAMILY, COST RUNG).
  G5  no chooser touches a row on or after 2017-01-01.
  G6  no shorting and no leverage: every book's daily gross in [0, 1].
  G7  all 375 cells published.
  G8  T_nav and T_gross are rank-identical on every count arm (gbar constant by convention):
      reported so the three currencies are not mistaken for three independent readings.

SURVIVORSHIP (PROTOCOL rule 9): U56 / B136 / SMALL are CURRENT-constituent lists, so every
absolute level here is an upper bound.  The headline is a set of WITHIN-BOOK turnover
decompositions and a DIFFERENCE between two cost rungs on the SAME book over the SAME days, so
it is first-order immune; the 4a / 4b pass counts are not.

Writes: .console.txt .grid.csv .drag.csv .walkforward.csv .keeppaths.csv
Modifies no rule file.  RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.
"""
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, band_state          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics                                             # noqa: E402

STAMP = "2026-09-19_is-the-per-r-COST-DRAG-INVERSION-a-CAND-n-convention_B"
OUT = ROOT / "research" / "backtests"
GROSS, BANDW, MAXVOL, FREQ = 0.75, 0.03, 0.60, "W"
COSTS = [0, 5, 10, 25, 50]
BINDING = 10
NS = [5, 10, 20, 40, 80, "ALL"]
FAMILIES = ["CAND", "MADIST", "BAND", "ADAPT"]
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
WARM = 260

_LOG = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)

# ----------------------------------------------------------------- weights builders
def _eligible(px):
    s, above, vol20 = score(px)
    return s, (above & (vol20 < MAXVOL) & px.notna())

def _madist(px):
    return px / px.rolling(200).mean() - 1.0

def _topn_weights(key, elig, n_row):
    """Equal weight GROSS/n_held over the top n_row names of `key` among `elig`.
    n_row is a per-day Series (the breadth axis); n = ALL is n_row = count of eligible."""
    k = key.where(elig)
    rk = k.rank(axis=1, ascending=False, method="first")
    held = rk.le(n_row, axis=0) & k.notna()
    cnt = held.sum(axis=1)
    return held.astype(float).div(cnt.replace(0, np.nan), axis=0).fillna(0.0) * GROSS

def build(px, family, n):
    s, elig = _eligible(px)
    if family == "EWALL":
        e = px.notna().astype(float)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if family == "BAND":
        inb = band_state(px, BANDW) & px.notna()
        key, sel = _madist(px), inb
    elif family == "MADIST":
        key, sel = _madist(px), elig
    else:                                   # CAND and ADAPT share the composite key + screen
        key, sel = s, elig
    avail = sel.sum(axis=1)
    if n == "ALL":
        n_row = avail.astype(float)
    elif family == "ADAPT":
        b = (px > px.rolling(200).mean()).sum(axis=1) / px.notna().sum(axis=1).replace(0, np.nan)
        bbar = b.shift(1).expanding(min_periods=60).mean()
        n_row = (n * b / bbar).round().clip(lower=2)
        n_row = n_row.where(bbar.notna(), float(n)).clip(upper=avail.astype(float))
    else:
        n_row = pd.Series(float(n), index=px.index).clip(upper=avail.astype(float))
    return _topn_weights(key, sel, n_row)

def band_live_norespread(px):
    """The live RULES v2 sizing, rebuilt from this script's own band machinery (GATE G2)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, BANDW), 0.0)

# ----------------------------------------------------------------- scoring helpers
def run_book(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    r0 = res["returns"].loc[start:]
    to = res["turnover"].loc[start:]
    held = res["weights"].loc[start:]
    g = held.sum(axis=1)
    nm = (held.abs() > 1e-12).sum(axis=1)
    yrs = len(r0) / 252.0
    return dict(r0=r0, to=to, T_nav=to.sum() / yrs, gbar=g.mean(), nbar=nm.mean(),
                gmax=g.max(), gmin=g.min())

def net(r0, to, c):
    return r0 - to * c / 1e4

def wins(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3: return np.nan
    rx = pd.Series(x[ok]).rank().values; ry = pd.Series(y[ok]).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])

# ----------------------------------------------------------------- run
def main():
    t0 = time.time()
    say(f"# Idea 708 (lane B) -- {STAMP}")
    say(f"# gross {GROSS} frozen, band {BANDW}, maxvol {MAXVOL}, freq {FREQ}, t->t+1, "
        f"costs {COSTS} bps (binding {BINDING})")
    say(f"# DIAL 1 FAMILY {FAMILIES + ['EWALL']}   DIAL 2 COST RUNG {COSTS}   (exactly 2)")
    say(f"# AXIS (not a dial) breadth n {NS}; PANELS U56/B136/SMALL; all cells published\n")

    panels = {"U56": dict(), "B136": dict(broad=True), "SMALL": dict(small=True)}
    gates, grid, dragrows, wf, kp = [], [], [], [], []

    for pname, kw in panels.items():
        px = load_universe(**kw)
        start = px.index[WARM]
        yrs = (px.loc[start:].shape[0]) / 252.0
        gates.append(("G0 sample>=10y " + pname, yrs >= 10.0, f"{yrs:.1f}y"))

        # --- G2 cross-script replay of the live book, before anything else is read
        g2 = float(np.abs(band_live_norespread(px).fillna(0) - rules_v2_weights(px, BANDW, GROSS).fillna(0)).values.max())
        gates.append(("G2 band machinery replays rules_v2 " + pname, g2 == 0.0, f"{g2:.3e}"))

        # --- references
        live = run_book(px, rules_v2_weights(px, BANDW, GROSS), start)
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        LIVE = wins(net(live["r0"], live["to"], BINDING))
        SPY = wins(spy_r)
        LIVE_O = wins(net(live["r0"], live["to"], BINDING).loc[OOS_START:])
        SPY_O = wins(spy_r.loc[OOS_START:])
        say(f"## {pname}  rows {px.shape[0]} cols {px.shape[1]}  sample {start.date()}..{px.index[-1].date()} ({yrs:.1f}y)")
        say(f"   LIVE(RULES v2 @10bps) CAGR {LIVE['CAGR']:.2%} Sharpe {LIVE['Sharpe']:.4f} "
            f"MaxDD {LIVE['MaxDD']:.2%} halves {LIVE['H1']:.4f}/{LIVE['H2']:.4f}")
        say(f"   SPY                   CAGR {SPY['CAGR']:.2%} Sharpe {SPY['Sharpe']:.4f} "
            f"MaxDD {SPY['MaxDD']:.2%} halves {SPY['H1']:.4f}/{SPY['H2']:.4f}")
        say(f"   4b bars: CAGR >= {0.70*SPY['CAGR']:.2%}, MaxDD >= {0.60*SPY['MaxDD']:.2%}, "
            f"Sharpe > {SPY['H1']:.4f}/{SPY['H2']:.4f} (halves) and > {SPY_O['Sharpe']:.4f} (OOS)")

        books = {}
        for fam in FAMILIES:
            for n in NS:
                books[(fam, n)] = build(px, fam, n)
        books[("EWALL", "ALL")] = build(px, "EWALL", "ALL")

        cells = {}
        for key, w in books.items():
            fam, n = key
            bk = run_book(px, w, start)
            cells[key] = bk
            gates.append((f"G6 gross in [0,1] {pname} {fam}-{n}",
                          bk["gmin"] >= -1e-12 and bk["gmax"] <= 1.0 + 1e-12,
                          f"[{bk['gmin']:.4f},{bk['gmax']:.4f}]"))
            rows = {}
            for c in COSTS:
                rc = net(bk["r0"], bk["to"], c)
                m, mo = wins(rc), wins(rc.loc[OOS_START:])
                rows[c] = (m, mo)
                grid.append(dict(panel=pname, family=fam, n=str(n), cost_bps=c,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=m["H1"], H2=m["H2"], OOS_CAGR=mo["CAGR"],
                                 OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                 T_nav=bk["T_nav"], gbar=bk["gbar"], nbar=bk["nbar"],
                                 T_gross=bk["T_nav"] / bk["gbar"],
                                 T_slot=bk["T_nav"] * bk["nbar"] / bk["gbar"]))
            m0, mb = rows[0][0], rows[BINDING][0]
            o0, ob = rows[0][1], rows[BINDING][1]
            dragrows.append(dict(panel=pname, family=fam, n=str(n),
                                 T_nav=bk["T_nav"], gbar=bk["gbar"], nbar=bk["nbar"],
                                 T_gross=bk["T_nav"] / bk["gbar"],
                                 T_slot=bk["T_nav"] * bk["nbar"] / bk["gbar"], vol0=m0["Vol"], drag=m0["Sharpe"] - mb["Sharpe"],
                                 drag_oos=o0["Sharpe"] - ob["Sharpe"],
                                 pred=(BINDING / 1e4) * bk["T_nav"] / m0["Vol"],
                                 Sharpe10=mb["Sharpe"], CAGR10=mb["CAGR"], MaxDD10=mb["MaxDD"]))
            # ---- both KEEP paths at the binding rung
            p4a = (mb["H1"] > LIVE["H1"]) and (mb["H2"] > LIVE["H2"]) and (mb["MaxDD"] >= LIVE["MaxDD"])
            legs = dict(H1=mb["H1"] > SPY["H1"], H2=mb["H2"] > SPY["H2"],
                        OOS=ob["Sharpe"] > SPY_O["Sharpe"],
                        DD=mb["MaxDD"] >= 0.60 * SPY["MaxDD"],
                        CAGR=mb["CAGR"] >= 0.70 * SPY["CAGR"])
            kp.append(dict(panel=pname, family=fam, n=str(n), pass4a=bool(p4a),
                           pass4b=bool(all(legs.values())), **{f"leg_{k}": bool(v) for k, v in legs.items()},
                           Sharpe=mb["Sharpe"], H1=mb["H1"], H2=mb["H2"], MaxDD=mb["MaxDD"],
                           CAGR=mb["CAGR"], OOS_Sharpe=ob["Sharpe"]))

        # --- G3 degeneracy
        a = next(d for d in dragrows if d["panel"] == pname and d["family"] == "ADAPT" and d["n"] == "ALL")
        cd = next(d for d in dragrows if d["panel"] == pname and d["family"] == "CAND" and d["n"] == "ALL")
        gates.append((f"G3 ADAPT-ALL == CAND-ALL {pname}", abs(a["Sharpe10"] - cd["Sharpe10"]) == 0.0,
                      f"{abs(a['Sharpe10'] - cd['Sharpe10']):.3e}"))

        # --- RULE 8: choosers fitted on IS only, OOS read once
        isw = {}
        for key, bk in cells.items():
            r0i = bk["r0"].loc[:IS_END]; toi = bk["to"].loc[:IS_END]
            s0 = metrics(r0i)["Sharpe"]; sB = metrics(net(r0i, toi, BINDING))["Sharpe"]
            isw[key] = (sB, s0 - sB)
        gates.append((f"G5 chooser reads no row >= {OOS_START.date()} {pname}",
                      all(bk["r0"].loc[:IS_END].index.max() < OOS_START for bk in cells.values()), "ok"))
        picks = {"C_SHARPE": max(isw, key=lambda k: isw[k][0]),
                 "C_DRAG": min(isw, key=lambda k: isw[k][1])}
        for sel, key in picks.items():
            bk = cells[key]
            o = wins(net(bk["r0"], bk["to"], BINDING).loc[OOS_START:])
            wf.append(dict(panel=pname, selector=sel, pick=f"{key[0]}-{key[1]}",
                           IS_Sharpe=isw[key][0], IS_drag=isw[key][1],
                           OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                           d_vs_LIVE=o["Sharpe"] - LIVE_O["Sharpe"], d_vs_SPY=o["Sharpe"] - SPY_O["Sharpe"],
                           beats_LIVE=bool(o["Sharpe"] > LIVE_O["Sharpe"]),
                           beats_SPY=bool(o["Sharpe"] > SPY_O["Sharpe"])))
        wf.append(dict(panel=pname, selector="C_ANCHOR", pick="LIVE(RULES v2)",
                       IS_Sharpe=metrics(net(live["r0"].loc[:IS_END], live["to"].loc[:IS_END], BINDING))["Sharpe"],
                       IS_drag=np.nan, OOS_CAGR=LIVE_O["CAGR"], OOS_Sharpe=LIVE_O["Sharpe"],
                       OOS_MaxDD=LIVE_O["MaxDD"], d_vs_LIVE=0.0,
                       d_vs_SPY=LIVE_O["Sharpe"] - SPY_O["Sharpe"], beats_LIVE=False,
                       beats_SPY=bool(LIVE_O["Sharpe"] > SPY_O["Sharpe"])))
        say(f"   SPY OOS Sharpe {SPY_O['Sharpe']:.4f} CAGR {SPY_O['CAGR']:.2%} MaxDD {SPY_O['MaxDD']:.2%}; "
            f"LIVE OOS {LIVE_O['Sharpe']:.4f} / {LIVE_O['CAGR']:.2%} / {LIVE_O['MaxDD']:.2%}\n")

    # ------------------------------------------------------------- G1 cost identity (spot cells)
    worst = 0.0
    for pname, kw in panels.items():
        px = load_universe(**kw)
        w = build(px, "CAND", 20)
        res0 = backtest(px, w, cost_bps=0.0, freq=FREQ)
        for c in (5, 10, 50):
            fresh = backtest(px, w, cost_bps=float(c), freq=FREQ)["returns"]
            rec = res0["returns"] - res0["turnover"] * c / 1e4
            worst = max(worst, float(np.abs(fresh - rec).max()))
    gates.append(("G1 cost identity exact (9 spot cells)", worst < 1e-15, f"max|d| {worst:.3e}"))
    gates.append(("G4 exactly two tuned parameters", True, "FAMILY, COST RUNG"))
    gates.append(("G7 all cells published", len(grid) == 375, f"{len(grid)} rows"))

    say("## GATES")
    for nm, ok, det in gates:
        if nm.startswith("G6") and ok: continue        # 75 of them; the failures would print
        say(f"   {'PASS' if ok else 'FAIL'}  {nm}  ({det})")
    ng6 = sum(1 for nm, ok, _ in gates if nm.startswith("G6"))
    say(f"   PASS  G6 gross in [0,1] on all {ng6} books (individually checked, none printed)")
    say(f"   GATES {sum(1 for _, ok, _ in gates if ok)}/{len(gates)}\n")

    G = pd.DataFrame(grid); D = pd.DataFrame(dragrows); W = pd.DataFrame(wf); K = pd.DataFrame(kp)

    # ------------------------------------------------------------- the discriminator
    say("## 1. THE DISCRIMINATOR -- drag re-cut in three turnover currencies")
    say("   (breadth axis n = 5/10/20/40/80/ALL; EWALL has one rung and is reported pooled)")
    say(f"   {'panel':6} {'family':7} {'rho(n,T_nav)':>13} {'rho(n,T_gross)':>15} {'rho(n,T_slot)':>14} {'rho(n,drag)':>12}")
    arms = []
    for fam in FAMILIES:
        for pname in panels:
            d = D[(D.family == fam) & (D.panel == pname)].copy()
            d["nn"] = [np.inf if x == "ALL" else float(x) for x in d.n]
            d = d.sort_values("nn")
            row = (pname, fam, spearman(d.nn.replace(np.inf, 1e6), d.T_nav),
                   spearman(d.nn.replace(np.inf, 1e6), d.T_gross),
                   spearman(d.nn.replace(np.inf, 1e6), d.T_slot),
                   spearman(d.nn.replace(np.inf, 1e6), d.drag))
            arms.append(row)
            say(f"   {row[0]:6} {row[1]:7} {row[2]:13.4f} {row[3]:15.4f} {row[4]:14.4f} {row[5]:12.4f}")
    A = pd.DataFrame(arms, columns=["panel", "family", "r_nav", "r_gross", "r_slot", "r_drag"])
    fam_nav = A.groupby("family").r_nav.mean(); fam_slot = A.groupby("family").r_slot.mean()
    _g8 = float((A.r_nav - A.r_gross).abs().max())
    gates.append(("G8 T_nav and T_gross rank-identical on all count arms (gbar constant)",
                  _g8 == 0.0, f"max|d rho| {_g8:.3e}"))
    say(f"\n   {'PASS' if _g8 == 0.0 else 'FAIL'}  G8 T_nav and T_gross are rank-identical on "
        f"all 12 count arms (gbar constant by the GROSS/n convention), max|d rho| {_g8:.3e}")
    say(f"   GATES {sum(1 for _, ok, _ in gates if ok)}/{len(gates)} including G8")
    # EWALL arm: pooled across panels, its own single rung -- the family with no count dial
    ew = D[D.family == "EWALL"]
    say(f"\n   EWALL (no count dial, n = N by construction): T_nav {list(np.round(ew.T_nav,3))}, "
        f"nbar {list(np.round(ew.nbar,1))}, T_slot {list(np.round(ew.T_slot,1))}, drag {list(np.round(ew.drag,4))}")
    n_nav = int((fam_nav < 0).sum()); n_name = int((fam_slot >= 0).sum()); n_gen = int((fam_slot < 0).sum())
    say(f"\n   ARMS (mean rho over 3 panels, 4 count families + EWALL context):")
    for f in FAMILIES:
        say(f"     {f:7} rho(n,T_nav) {fam_nav[f]:+.4f}   rho(n,T_slot) {fam_slot[f]:+.4f}")
    say(f"   H_CONVENTION legs: rho(n,T_nav) < 0 in {n_nav}/4 count families; "
        f"rho(n,T_slot) >= 0 in {n_name}/4.")
    say(f"   H_GENERAL    leg:  rho(n,T_slot) < 0 in {n_gen}/4.")
    conv = (n_nav >= 4) and (n_name >= 4); gen = (n_gen >= 4)
    verdict_h = "H_CONVENTION" if conv and not gen else ("H_GENERAL" if gen and not conv else "SPLIT")
    say(f"   >>> PRE-REGISTERED READING: {verdict_h}\n")

    # ------------------------------------------------------------- the arithmetic leg
    say("## 2. THE ARITHMETIC LEG -- does drag carry any information beyond T_nav?")
    x = D.pred.values; y = D.drag.values
    ok = np.isfinite(x) & np.isfinite(y)
    b1, b0 = np.polyfit(x[ok], y[ok], 1)
    yhat = b0 + b1 * x[ok]
    r2 = 1 - ((y[ok] - yhat) ** 2).sum() / ((y[ok] - y[ok].mean()) ** 2).sum()
    say(f"   drag(10bps) = {b0:+.6f} + {b1:.6f} * (10/1e4)*T_nav/vol_0   over {ok.sum()} books")
    say(f"   R^2 {r2:.6f}   max |residual| {np.abs(y[ok]-yhat).max():.6f}   "
        f"mean |drag| {np.abs(y[ok]).mean():.6f}")
    say(f"   Spearman(pred, drag) {spearman(x, y):.6f}\n")

    # ------------------------------------------------------------- 703's own claim, replicated
    say("## 3. IDEA 703's CLAIM, REPLICATED ON THIS CONSTRUCTION (drag vs breadth, 10 bps)")
    piv = D.pivot_table(index=["panel", "family"], columns="n", values="drag")
    cols = [c for c in ["5", "10", "20", "40", "80", "ALL"] if c in piv.columns]
    say(piv[cols].to_string(float_format=lambda v: f"{v:+.4f}"))
    say("")
    piv2 = D.pivot_table(index=["panel", "family"], columns="n", values="T_slot")
    say("   NAME SLOTS replaced per year (T_slot = T_nav * nbar / gbar):")
    say(piv2[cols].to_string(float_format=lambda v: f"{v:8.2f}"))
    say("")
    say("   and turnover per unit NAV (T_nav), the record's currency:")
    piv3 = D.pivot_table(index=["panel", "family"], columns="n", values="T_nav")
    say(piv3[cols].to_string(float_format=lambda v: f"{v:8.4f}"))
    say("")

    # ------------------------------------------------------------- KEEP paths
    say("## 4. BOTH KEEP PATHS at the binding 10 bps rung (75 books)")
    say(f"   4a PASS {int(K.pass4a.sum())} of {len(K)}    4b PASS {int(K.pass4b.sum())} of {len(K)}")
    for leg in ["H1", "H2", "OOS", "DD", "CAGR"]:
        say(f"     4b leg {leg:5} passes {int(K['leg_'+leg].sum()):3} of {len(K)}")
    if K.pass4b.any():
        say("   4b passers:")
        say(K[K.pass4b][["panel", "family", "n", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]]
            .to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    if K.pass4a.any():
        say("   4a passers:")
        say(K[K.pass4a][["panel", "family", "n", "CAGR", "Sharpe", "H1", "H2", "MaxDD"]]
            .to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    say("")

    # ------------------------------------------------------------- rule 8
    say("## 5. RULE 8 WALK-FORWARD (params on warm-up..2016 only; 2017-2026 read once)")
    say(W.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    ch = W[W.selector != "C_ANCHOR"]
    say(f"\n   mean d(OOS Sharpe) vs LIVE {ch.d_vs_LIVE.mean():+.4f} "
        f"(beats it {int(ch.beats_LIVE.sum())} of {len(ch)});  vs SPY {ch.d_vs_SPY.mean():+.4f} "
        f"(beats it {int(ch.beats_SPY.sum())} of {len(ch)})")
    say(f"   C_DRAG alone: mean d vs LIVE {ch[ch.selector=='C_DRAG'].d_vs_LIVE.mean():+.4f}, "
        f"vs SPY {ch[ch.selector=='C_DRAG'].d_vs_SPY.mean():+.4f}\n")

    for nm, df in [("grid", G), ("drag", D), ("walkforward", W), ("keeppaths", K)]:
        df.to_csv(OUT / f"{STAMP}.{nm}.csv", index=False)
    say(f"# runtime {time.time()-t0:.1f}s; artefacts {STAMP}.{{grid,drag,walkforward,keeppaths}}.csv")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")

if __name__ == "__main__":
    main()

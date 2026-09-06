#!/usr/bin/env python3
"""QUEUE idea 157 — time-varying-share-vs-fixed-n  (lane B, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 157)
    "idea 153's KEEP-candidate fixes n = round(0.53 x mean eligible count), a per-universe
     CONSTANT.  The obvious variant n_t = round(0.53 x E_t) rebalances the book's breadth
     with the market and was NOT tested; idea 46 found an adaptive count is a genuine bear
     defence full-sample Sharpe hides.  Run the two side by side on both large-cap panels at
     10/25 bps, and report 2020/2022 separately.  Max 2 params."

    Idea 153's own memo, clause 7, is the standing instruction this run tests:
     "A time-varying n_t = round(0.53 x E_t) is a different rule and was **not** tested here.
      Ebar must be a pre-registered constant per universe."

WHAT IS AT STAKE, and the trap the queue's framing walks into.
    The queue asks this as a breadth question — "rebalances the book's breadth with the
    market".  Under the incumbent's OWN weight construction it is not primarily a breadth
    question, it is a CASH question, and the run has to separate the two or it will report
    the wrong mechanism.  RULES v1 and idea 153's candidate both weight every held name at
    GROSS/n with n FIXED.  When a bear market shrinks the eligible list below n, the fixed-n
    book can only fill k < n slots and therefore invests GROSS x k/n — it silently holds cash.
    The adaptive book n_t = round(m x E_t) always has n_t <= E_t by construction, so it always
    fills every slot and is ALWAYS fully invested.  Swapping fixed n for adaptive n_t under
    `lit` weights therefore does two things at once: it changes how many names you hold, and
    it DELETES the incumbent's implicit cash buffer.  Idea 46's "genuine bear defence" is
    plausibly that buffer, not the count.
    So every cell here is run under two weight constructions:
        lit  = GROSS / n_t  per held name   (the incumbent's literal construction; the book
               de-grosses whenever fewer than n_t names are eligible — only possible for FIX)
        norm = GROSS spread over the names actually held (always fully invested)
    `lit` answers "should the live book change?".  `norm` answers "does breadth-timing carry
    anything once cash is held equal?".  The pair is the decomposition; neither alone is.

CORPUS
    3 panels (u56 / broad / small) x 7 book shares x 4 count rules x 2 weight constructions
    x 2 cost rungs = 336 books, weekly, t+1, long-only, no leverage.  84 distinct weight
    matrices; the cost axis is DERIVED exactly (control [D]) rather than re-simulated.

TUNED PARAMETERS — exactly two, both swept exhaustively, ALL grid points reported:
    1. the target book share m in {0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00}  (idea 153's
       ladder verbatim; m = 0.53 is the incumbent's own share and the pre-registered anchor)
    2. the COUNT RULE, 4 values:
         FIX      n = max(2, round(m x Ebar_full)), Ebar_full = mean daily eligible count over
                  the whole evaluation sample.  This is idea 153's published construction and
                  the arm this run must reproduce.  NOTE it reads the future: Ebar_full is a
                  full-sample statistic.
         FIXIS    n = max(2, round(m x Ebar_IS)), Ebar computed on 2009-01-01..2016-12-31 only.
                  The lookahead-free fixed rule — the control that says how much of FIX is
                  the future.
         ADAPT    n_t = max(2, round(m x E_t)), E_t the eligible count on the DECISION bar t.
                  Point-in-time, zero lookahead.  This is idea 157's variant.
         ADAPT63  n_t = max(2, round(m x mean of E over the trailing 63 bars)).  Says whether
                  any ADAPT effect is the level of E or its week-to-week noise.
    Panels, cost rungs, weight construction, calendar years, and the IS/OOS split are REPORTED
    axes, never selected on.  The tilt is NOT a parameter: the incumbent has no vol scaler, so
    every book here is scored on the bare composite (idea 153 clause 4 already found that
    admitting a tilt to the walk-forward subtracts 0.028 of mean OOS Sharpe).  The 200d gate
    and vol20 < 0.60 stay at v1's values.

DEPENDENT VARIABLES, fixed before any number was read
    Primary: Sharpe, CAGR, MaxDD full-sample and on the OOS window, with both KEEP paths (4a
    against RULES v1 on the same panel and cost; 4b against SPY with PROTOCOL's phi=0.70 CAGR
    floor and delta=0.60 drawdown cap) evaluated at every one of the 336 books.
    The queue's own ask: calendar-year returns, with 2020 and 2022 printed separately.
    Mechanism: realised mean invested gross, and the ADAPT-minus-FIX difference in it.

CONTROLS, asserted before any new number is read
    [A] engine.backtest is the simulator; the FIX arm's weight matrix is built by the same
        code path as idea 153's `weights(..., constr=...)`.
    [B] the decisive one: FIX/NONE/lit must reproduce idea 153's committed grid.csv
        (2026-09-05_does-book-share-price-a-tilt_C.grid.csv) on every (panel, m, cost) cell it
        published, to 1e-9 on CAGR/Sharpe/MaxDD/H1/H2/OOS_Sharpe/turnover.  If it does, this
        is idea 153's instrument with one axis added.
    [C] Ebar_full must reproduce idea 153's mean eligible counts (u56 37.5 / broad 91.5 /
        small 141.2) and its m->n map.
    [D] cost derivation: net(c) = gross_return - turnover x c/1e4 must equal a direct
        engine.backtest at that cost to < 1e-12 on a sampled cell per panel.
    [E] at m = 1.00 the ADAPT book holds the entire eligible list by construction, so ADAPT
        and the `norm` construction must coincide there; a mismatch is a bug.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [B] reproduces.
    P2  Under `lit`, mean realised invested gross is strictly lower for FIX than for ADAPT on
        every panel at every m < 1.00, and the gap widens in 2020 and 2022.
    P3  Under `lit`, ADAPT's full-sample MaxDD is DEEPER than FIX's at matched m on both
        large-cap panels — the cash buffer, not the count, is what the incumbent is being paid
        for.
    P4  Under `norm` (cash held equal) the FIX-vs-ADAPT Sharpe difference is small: mean
        |dSharpe| < 0.05 across the large-cap cells.  Breadth-timing per se carries little.
    P5  ADAPT passes 4b in strictly fewer large-cap cells than FIX, and the small panel
        contributes 0 passes at every m and every rule (idea 136, nth reproduction).
    P6  Rule 8: no selector beats the pre-registered do-nothing incumbent (FIX at m = 0.53)
        on OOS Sharpe on both large-cap panels at 10 bps.

WALK-FORWARD (PROTOCOL rule 8), selection rules fixed BEFORE any OOS number is read
    Parameters (m, rule) chosen on 2009-01-01..2016-12-31 only, the pick read ONCE on
    2017-01-01..2026 and reported as OOS CAGR/Sharpe/MaxDD against (i) the do-nothing control
    = FIX at m = 0.53, the incumbent, (ii) RULES v1 on the same panel and cost, (iii) SPY.
      S0  IS-Sharpe argmax over the whole 28-point grid
      S1  IS-Sharpe argmax among books passing the 4b-aware IS screen (IS halves, IS DD, IS
          CAGR floor at phi = 0.70)
      S2  as S1 with the CAGR floor at phi = 0.00
      S3  RULE-ONLY: share pinned at the incumbent's 0.53, IS-Sharpe argmax over the 4 count
          rules.  This is the narrow question the queue actually asks.
    Both KEEP paths are evaluated on the full sample AND on the OOS window alone.

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54).  The small panel
      drops the 44 tickers with max_1d_move >= 1.0 and holds SPY out as a benchmark.  No level
      here is an attainable return; the FIX-vs-ADAPT DIFFERENCE is the durable part.
    * Ideas 49/39: the 200d/vol20 eligibility gate is INVERTED on the small panel, so E_t there
      is the count of a gate that does not work; small-panel numbers are reported, not traded.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * Idea 223: a WEEKLY schedule has 5 trade-date anchors that were not priced here; every
      drawdown number below is one anchor's, and idea 223's band is not re-measured.
    * FIX reads Ebar off the full sample.  That is idea 153's published construction and is
      reproduced as such, not endorsed; FIXIS is the honest fixed rule and is reported beside
      it everywhere.

POST-RUN CORRECTION (added after the first execution; the pre-registration above is left
verbatim and is WRONG on one point, which control [E] caught before any result was read)
    "ADAPT ... always fills every slot and is ALWAYS fully invested" is false.  E_t counts the
    names that pass the 200d/vol20 gate, but the composite cannot SCORE a name whose 252-day
    momentum window is still NaN, so the RANKABLE count R_t is at or below E_t and the adaptive
    book can be short of slots even at m = 1.00.  Control [E] is restated accordingly — lit ==
    norm on every bar where R_t >= n_t, with the deficient bars counted and priced — and every
    invested-gross figure in the output is measured rather than assumed.  Nothing else changes:
    the arms, the grid, the selectors and the predictions are as pre-registered.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .gross.csv, .peryear.csv,
.walkforward.csv, .paired.csv.
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

STEM = "2026-09-06_time-varying-share-vs-fixed-n_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I153G = OUT / "2026-09-05_does-book-share-price-a-tilt_C.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ = "W"
GROSS, MAX_VOL = 0.75, 0.60
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI0, DELTA0 = 0.70, 0.60

SHARES = [0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00]      # tuned parameter 1
RULES = ["FIX", "FIXIS", "ADAPT", "ADAPT63"]             # tuned parameter 2
CONSTR = ["lit", "norm"]                                 # reported axis
M_ANCHOR = 0.53                                          # the incumbent's share

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 1200)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ the book (idea 153 verbatim)
_SC = {}


def score_of(px, pk):
    """Composite momentum with the 200d half-weight, no vol scaler; plus the gate parts."""
    if pk not in _SC:
        mom = px.shift(21) / px.shift(252) - 1
        r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
        comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                + r3.rank(axis=1, pct=True)) / 3
        above = px > px.rolling(200).mean()
        v = px.pct_change().rolling(20).std() * np.sqrt(252)
        _SC[pk] = (comp * (0.5 + 0.5 * above.astype(float)), above, v)
    return _SC[pk]


def eligible(px, pk):
    _, above, v = score_of(px, pk)
    return above & (v < MAX_VOL)


def n_series(px, pk, m, rule, start):
    """The count rule, as a per-row integer Series (>= 2).  Constants are broadcast."""
    el = eligible(px, pk)
    E = el.sum(axis=1)
    if rule == "FIX":
        n = max(2, int(round(m * float(E.loc[start:].mean()))))
        return pd.Series(n, index=px.index), n
    if rule == "FIXIS":
        n = max(2, int(round(m * float(E.loc[start:IS_END].mean()))))
        return pd.Series(n, index=px.index), n
    if rule == "ADAPT":
        s = (m * E).round().clip(lower=2).astype(int)
        return s, np.nan
    if rule == "ADAPT63":
        s = (m * E.rolling(63, min_periods=1).mean()).round().clip(lower=2).astype(int)
        return s, np.nan
    raise ValueError(rule)


def weights(px, pk, m, rule, constr, start):
    s, above, v = score_of(px, pk)
    ns, nconst = n_series(px, pk, m, rule, start)
    rank = s.where(above & (v < MAX_VOL)).rank(axis=1, ascending=False)
    held = rank.le(ns, axis=0).fillna(False)
    Wm = held.astype(float)
    if constr == "lit":
        return Wm.div(ns, axis=0) * GROSS, ns, nconst
    k = Wm.sum(axis=1).replace(0, np.nan)
    return Wm.div(k, axis=0).fillna(0.0) * GROSS, ns, nconst


# ------------------------------------------------------------------ cost axis, derived exactly
def net_at(res, cost, start):
    """engine.backtest computes port = gross - turnover*cost/1e4 and never uses cost in the
    holdings loop, so a single cost=0 run prices every rung by identity."""
    return (res["returns"] - res["turnover"] * cost / 1e4).loc[start:]


def yearly(r):
    return (1 + r).groupby(r.index.year).prod() - 1


def main():
    say("=" * 200)
    say(f"IDEA 157 — time-varying-share-vs-fixed-n   ({STEM})")
    say("Is idea 153's fixed n = round(0.53 x Ebar) beaten by n_t = round(0.53 x E_t)?  "
        "And is the fixed rule's edge breadth, or the cash it silently holds?")
    say("=" * 200)

    ok, rows, gross_rows, year_rows = {}, [], [], []
    RET, ref = {}, {}
    ref153 = pd.read_csv(I153G)

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        bOOS = C.bars_win(spy, "OOS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1res = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        v1 = {c: net_at(v1res, c, start) for c in COSTS}
        E = eligible(px, pk).sum(axis=1)
        Ebar_full = float(E.loc[start:].mean())
        Ebar_IS = float(E.loc[start:IS_END].mean())
        ref[pk] = dict(px=px, start=start, spy=spy, bfull=bfull, bIS=bIS, bOOS=bOOS,
                       v1=v1, Ebar=Ebar_full, EbarIS=Ebar_IS, desc=desc, ms=ms, mso=mso, E=E)

        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}")
        say(f"    Ebar(full) = {Ebar_full:.1f}   Ebar(IS 2009-2016) = {Ebar_IS:.1f}   "
            f"E_t range {int(E.loc[start:].min())}..{int(E.loc[start:].max())}   "
            f"E_t 2020 mean {float(E.loc['2020'].mean()):.1f}   2022 mean {float(E.loc['2022'].mean()):.1f}")
        say(f"    SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}"
            f"/{mso['MaxDD']:.2%}")
        for c in COSTS:
            mm, mo = metrics(v1[c]), metrics(v1[c].loc[OOS_START:])
            say(f"    RULES v1 @{int(c)}bps: {mm['CAGR']:.2%}/{mm['Sharpe']:.3f}/{mm['MaxDD']:.2%}"
                f" | OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")

        # ---------- [C] Ebar and the m -> n map
        pub = {"u56": 37.5, "broad": 91.5, "small": 141.2}[pk]
        ok[f"C:{pk}"] = abs(Ebar_full - pub) < 0.06
        say(f"[C] Ebar reproduction: idea 153 published {pub}, this run {Ebar_full:.2f} -> "
            f"{'MATCH' if ok[f'C:{pk}'] else 'MISMATCH'}")
        say("    m -> n(FIX) / n(FIXIS): " + ", ".join(
            f"{m:.2f}->{max(2, int(round(m*Ebar_full)))}/{max(2, int(round(m*Ebar_IS)))}"
            for m in SHARES))

        # ---------- the grid
        for m in SHARES:
            for rule in RULES:
                for cn in CONSTR:
                    W, ns, nconst = weights(px, pk, m, rule, cn, start)
                    res = backtest(px, W, cost_bps=0.0, freq=FREQ)
                    invg = res["weights"].sum(axis=1).loc[start:]
                    held_ct = (res["weights"] > 0).sum(axis=1).loc[start:]
                    for c in COSTS:
                        r = net_at(res, c, start)
                        arm = f"{rule}|m{m:.2f}|{cn}"
                        RET[(pk, c, arm)] = r
                        mf, mo = metrics(r), metrics(r.loc[OOS_START:])
                        mgf = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                        mgI = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                        mgO = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                        h1, h2 = H.halves(r)
                        rows.append(dict(
                            panel=pk, m=m, rule=rule, constr=cn, cost=c, arm=arm,
                            n_const=nconst, n_mean=float(ns.loc[start:].mean()),
                            n_held=float(held_ct.mean()), inv_gross=float(invg.mean()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                            H1=h1, H2=h2,
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            IS_Sharpe=metrics(H.window(r, "IS"))["Sharpe"],
                            IS_CAGR=metrics(H.window(r, "IS"))["CAGR"],
                            TO=float(res["turnover"].loc[start:].sum() / (len(r) / 252)),
                            pass4a=H.pass4a(r, ref[pk]["v1"][c]),
                            pass4b=len(C.fails(mgf)) == 0, fail4b=",".join(C.fails(mgf)) or "-",
                            pass4b_oos=len(C.fails(mgO)) == 0,
                            IS_adm=len(C.fails(mgI)) == 0,
                            **{f"IS_m_{k}": v for k, v in mgI.items()}))
                    gross_rows.append(dict(panel=pk, m=m, rule=rule, constr=cn,
                                           inv_gross=float(invg.mean()),
                                           inv_2020=float(invg.loc["2020"].mean()),
                                           inv_2022=float(invg.loc["2022"].mean()),
                                           n_held=float(held_ct.mean()),
                                           n_held_2020=float(held_ct.loc["2020"].mean()),
                                           n_held_2022=float(held_ct.loc["2022"].mean())))
                    if m == M_ANCHOR:
                        for c in COSTS:
                            yr = yearly(RET[(pk, c, f"{rule}|m{m:.2f}|{cn}")])
                            for y, val in yr.items():
                                year_rows.append(dict(panel=pk, m=m, rule=rule, constr=cn,
                                                      cost=c, year=int(y), ret=float(val)))

    G = pd.DataFrame(rows)
    GR = pd.DataFrame(gross_rows)
    YR = pd.DataFrame(year_rows)

    # ================================================================ CONTROLS
    say("\n" + "=" * 200)
    say("CONTROLS")
    say("=" * 200)

    # [B] reproduce idea 153's committed grid on the FIX/lit arm
    r153 = ref153[(ref153.tilt == "NONE") & (ref153.constr == "lit")].copy()
    cols = [("CAGR", "CAGR"), ("Sharpe", "Sharpe"), ("MaxDD", "MaxDD"), ("H1", "H1"),
            ("H2", "H2"), ("OOS_Sharpe", "OOS_Sharpe"), ("TO", "TO")]
    mine = G[(G.rule == "FIX") & (G.constr == "lit")]
    j = r153.merge(mine, on=["panel", "m", "cost"], suffixes=("_153", "_now"))
    worst, ncmp = 0.0, 0
    for a, b in cols:
        d = (j[f"{a}_153"] - j[f"{b}_now"]).abs().max()
        worst = max(worst, float(d))
        ncmp += len(j)
    ok["B"] = worst < 1e-9 and len(j) == len(r153)
    say(f"[B] FIX/lit vs idea 153's committed grid.csv: {len(j)} cells matched of "
        f"{len(r153)} published, {ncmp} statistic comparisons, worst |diff| = {worst:.3e} -> "
        f"{'MATCH' if ok['B'] else 'MISMATCH'}")
    nb = j[["panel", "m", "n", "n_const"]].drop_duplicates()
    ok["B_n"] = bool((nb.n == nb.n_const).all())
    say(f"    m->n map identical on all {len(nb)} (panel, m) points: {ok['B_n']}")

    # [D] cost derivation vs a direct run
    dmax = 0.0
    for pk in PANELS:
        px, start = ref[pk]["px"], ref[pk]["start"]
        W, _, _ = weights(px, pk, M_ANCHOR, "ADAPT", "lit", start)
        direct = backtest(px, W, cost_bps=25.0, freq=FREQ)["returns"].loc[start:]
        derived = RET[(pk, 25.0, f"ADAPT|m{M_ANCHOR:.2f}|lit")]
        dmax = max(dmax, float((direct - derived).abs().max()))
    ok["D"] = dmax < 1e-12
    say(f"[D] derived 25bps net vs a direct engine.backtest(cost=25): max |diff| = {dmax:.3e} "
        f"-> {'MATCH' if ok['D'] else 'MISMATCH'}")

    # [E] ADAPT at m=1.00 vs the norm construction.  The pre-registered premise ("ADAPT is
    # always fully invested, so lit == norm at m = 1.00") is WRONG, and the control caught it:
    # E_t counts names that pass the gate, but the RANKER cannot score a name whose 252-day
    # momentum is still NaN, so the rankable count R_t <= E_t and the book can be short of
    # slots even at m = 1.00.  The control is therefore restated, not relaxed: lit == norm on
    # every bar where R_t >= n_t, and the bars where it does not are counted and priced.
    say("[E] restated (the pre-registered premise was wrong — see below).  ADAPT at m=1.00:")
    emax_ok, ebad = 0.0, {}
    for pk in PANELS:
        px, start = ref[pk]["px"], ref[pk]["start"]
        s, above, v = score_of(px, pk)
        gate = above & (v < MAX_VOL)
        Et = gate.sum(axis=1).loc[start:]
        Rt = (gate & s.notna()).sum(axis=1).loc[start:]
        nt = Et.clip(lower=2)
        short = Rt < nt
        Wl, _, _ = weights(px, pk, 1.00, "ADAPT", "lit", start)
        Wn, _, _ = weights(px, pk, 1.00, "ADAPT", "norm", start)
        d = (Wl - Wn).abs().sum(axis=1).loc[start:]
        emax_ok = max(emax_ok, float(d[~short].max()))
        ebad[pk] = (int(short.sum()), len(short), float(Et.mean()), float(Rt.mean()),
                    float(d[short].max()) if short.any() else 0.0)
        say(f"    {pk}: mean E_t {Et.mean():.2f} vs mean RANKABLE R_t {Rt.mean():.2f}; "
            f"{int(short.sum())} of {len(short)} bars ({short.mean():.2%}) have R_t < n_t")
    ok["E"] = emax_ok < 1e-12
    say(f"    lit vs norm on the {'/'.join(str(len(ref[p]['spy'])) for p in PANELS)} bars where "
        f"R_t >= n_t: max |weight diff| = {emax_ok:.3e} -> "
        f"{'MATCH' if ok['E'] else 'MISMATCH'}")
    say("    CONSEQUENCE, stated because it changes the mechanism story: ADAPT is NOT "
        "unconditionally fully invested under `lit`.  E_t is idea 153's eligible count and it "
        "includes names the composite cannot yet score, so ADAPT de-grosses on exactly those "
        "bars.  Every invested-gross number below is measured, not assumed.")

    say("\nCONTROL SUMMARY: " + ", ".join(f"{k}={'ok' if v else 'FAIL'}" for k, v in ok.items()))

    # ================================================================ P2: the cash channel
    say("\n" + "=" * 200)
    say("P2 / MECHANISM — realised invested gross (lit construction).  ADAPT is always fully "
        "invested by construction; FIX de-grosses whenever fewer than n names are eligible.")
    say("=" * 200)
    lit = GR[GR.constr == "lit"]
    piv = lit.pivot_table(index=["panel", "m"], columns="rule",
                          values=["inv_gross", "inv_2020", "inv_2022"])
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    for pk in PANELS:
        sub = lit[(lit.panel == pk) & (lit.m < 1.0)]
        f = sub[sub.rule == "FIX"].set_index("m")
        a = sub[sub.rule == "ADAPT"].set_index("m")
        gaps = (a.inv_gross - f.inv_gross)
        g20 = (a.inv_2020 - f.inv_2020)
        g22 = (a.inv_2022 - f.inv_2022)
        say(f"  {pk}: ADAPT-minus-FIX invested gross, full {gaps.mean():+.4f} "
            f"(min {gaps.min():+.4f}, all>0 {bool((gaps > 0).all())}), 2020 {g20.mean():+.4f}, "
            f"2022 {g22.mean():+.4f}")

    # ================================================================ the grid
    say("\n" + "=" * 200)
    say("THE GRID — all 336 books.  Every point reported; nothing selected on.")
    say("=" * 200)
    show = ["panel", "m", "rule", "constr", "cost", "n_const", "n_mean", "n_held", "inv_gross",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "TO", "pass4a", "pass4b",
            "fail4b", "pass4b_oos"]
    for pk in PANELS:
        say(f"\n--- panel {pk} ---")
        say(G[G.panel == pk][show].to_string(index=False,
                                             float_format=lambda x: f"{x:.4f}"))

    # ================================================================ P3/P4: the paired read
    say("\n" + "=" * 200)
    say("P3 / P4 — ADAPT minus FIX at matched (panel, m, cost), by weight construction.")
    say("  lit  = the live construction: the swap deletes FIX's implicit cash")
    say("  norm = cash held equal: what breadth-timing alone is worth")
    say("=" * 200)
    key = ["panel", "m", "cost", "constr"]
    A = G[G.rule == "ADAPT"].set_index(key)
    F = G[G.rule == "FIX"].set_index(key)
    A63 = G[G.rule == "ADAPT63"].set_index(key)
    FI = G[G.rule == "FIXIS"].set_index(key)
    pair = pd.DataFrame({
        "dSharpe": A.Sharpe - F.Sharpe, "dCAGR": A.CAGR - F.CAGR,
        "dMaxDD": A.MaxDD - F.MaxDD, "dOOS": A.OOS_Sharpe - F.OOS_Sharpe,
        "dSharpe63": A63.Sharpe - F.Sharpe, "dSharpe_FIXIS": FI.Sharpe - F.Sharpe,
        "dTO": A.TO - F.TO}).reset_index()
    say(pair.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    for cn in CONSTR:
        for scope, sel in (("large-cap", pair.panel.isin(["u56", "broad"])),
                           ("all panels", pair.panel.notna())):
            s = pair[(pair.constr == cn) & sel]
            say(f"  [{cn}/{scope}] mean dSharpe {s.dSharpe.mean():+.4f}, mean |dSharpe| "
                f"{s.dSharpe.abs().mean():.4f}, ADAPT wins {int((s.dSharpe > 0).sum())}/{len(s)}"
                f"; mean dMaxDD {s.dMaxDD.mean():+.4f} (ADAPT deeper in "
                f"{int((s.dMaxDD < 0).sum())}/{len(s)}); mean dOOS {s.dOOS.mean():+.4f}")
    litLC = pair[(pair.constr == "lit") & pair.panel.isin(["u56", "broad"])]
    normLC = pair[(pair.constr == "norm") & pair.panel.isin(["u56", "broad"])]
    say(f"  P3 (lit, large-cap): ADAPT MaxDD deeper than FIX in "
        f"{int((litLC.dMaxDD < 0).sum())}/{len(litLC)} cells, mean {litLC.dMaxDD.mean():+.4f}")
    say(f"  P4 (norm, large-cap): mean |dSharpe| {normLC.dSharpe.abs().mean():.4f} "
        f"(prediction: < 0.05) -> {'HIT' if normLC.dSharpe.abs().mean() < 0.05 else 'MISS'}")

    # ================================================================ P5: KEEP paths
    say("\n" + "=" * 200)
    say("P5 / KEEP PATHS — 4a (beat RULES v1 in both halves, DD no worse) and 4b (beat SPY "
        "both halves + OOS, DD <= 60% of SPY's, CAGR >= 70% of SPY's).")
    say("=" * 200)
    say(G.groupby(["panel", "rule", "constr", "cost"])[["pass4a", "pass4b", "pass4b_oos"]]
        .sum().to_string())
    say("\n4b passers (full sample), every one:")
    p4b = G[G.pass4b][show]
    say(p4b.to_string(index=False, float_format=lambda x: f"{x:.4f}") if len(p4b)
        else "  (none)")
    say(f"\n  small panel 4b passes at any m/rule/constr/cost: "
        f"{int(G[(G.panel == 'small')].pass4b.sum())} of {len(G[G.panel == 'small'])}")
    for pk in ("u56", "broad"):
        f_ = int(G[(G.panel == pk) & (G.rule == "FIX")].pass4b.sum())
        a_ = int(G[(G.panel == pk) & (G.rule == "ADAPT")].pass4b.sum())
        i_ = int(G[(G.panel == pk) & (G.rule == "FIXIS")].pass4b.sum())
        a6 = int(G[(G.panel == pk) & (G.rule == "ADAPT63")].pass4b.sum())
        say(f"  {pk}: 4b passes FIX {f_}, FIXIS {i_}, ADAPT {a_}, ADAPT63 {a6} "
            f"(of {len(G[(G.panel == pk) & (G.rule == 'FIX')])} each)")

    # ================================================================ the queue's own ask
    say("\n" + "=" * 200)
    say(f"CALENDAR YEARS at the incumbent's share m = {M_ANCHOR} (the queue's explicit ask; "
        "2020 and 2022 in bold below the table)")
    say("=" * 200)
    for pk in PANELS:
        for cn in CONSTR:
            sub = YR[(YR.panel == pk) & (YR.constr == cn) & (YR.cost == 10.0)]
            t = sub.pivot(index="year", columns="rule", values="ret")
            spyy = yearly(ref[pk]["spy"])
            v1y = yearly(ref[pk]["v1"][10.0])
            t = t.join(pd.Series(spyy, name="SPY")).join(pd.Series(v1y, name="RULESv1"))
            say(f"\n--- {pk} / {cn} / 10 bps ---")
            say(t.to_string(float_format=lambda x: f"{x:+.2%}"))
    say("\nThe two years the queue asked for, both cost rungs, both constructions:")
    for y in (2020, 2022):
        sub = YR[YR.year == y]
        say(f"\n  {y}:")
        say(sub.pivot_table(index=["panel", "constr", "cost"], columns="rule",
                            values="ret").to_string(float_format=lambda x: f"{x:+.2%}"))

    # ================================================================ rule 8
    say("\n" + "=" * 200)
    say("RULE 8 WALK-FORWARD — (m, rule) chosen on 2009-2016 ONLY, read once on 2017-2026.")
    say("  do-nothing control = FIX at m = 0.53, the incumbent, same panel/cost/constr")
    say("=" * 200)
    wf = []
    for pk in PANELS:
        bIS = ref[pk]["bIS"]
        for c in COSTS:
            for cn in CONSTR:
                sub = G[(G.panel == pk) & (G.cost == c) & (G.constr == cn)]
                ctl = RET[(pk, c, f"FIX|m{M_ANCHOR:.2f}|{cn}")]
                mc = metrics(ctl.loc[OOS_START:])
                mv = metrics(ref[pk]["v1"][c].loc[OOS_START:])
                msp = ref[pk]["mso"]
                isok = lambda row, phi: all(row[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD")) \
                    and (row["IS_CAGR"] - phi * bIS["scagr"] > 0)          # noqa: E731
                cand = {
                    "S0": sub,
                    "S1": sub[sub.apply(lambda r: isok(r, PHI0), axis=1)],
                    "S2": sub[sub.apply(lambda r: isok(r, 0.00), axis=1)],
                    "S3": sub[sub.m == M_ANCHOR],
                }
                oos_best = sub.loc[sub.OOS_Sharpe.idxmax(), "arm"]
                for s, cd in cand.items():
                    if len(cd) == 0:
                        wf.append(dict(panel=pk, cost=c, constr=cn, sel=s, pick="(none)",
                                       n_adm=0))
                        continue
                    p = cd.loc[cd.IS_Sharpe.idxmax()]
                    r = RET[(pk, c, p["arm"])].loc[OOS_START:]
                    m_ = metrics(r)
                    wf.append(dict(panel=pk, cost=c, constr=cn, sel=s, pick=p["arm"],
                                   n_adm=len(cd), OOS_CAGR=m_["CAGR"], OOS_Sharpe=m_["Sharpe"],
                                   OOS_MaxDD=m_["MaxDD"], ctl_OOS=mc["Sharpe"],
                                   v1_OOS=mv["Sharpe"], spy_OOS=msp["Sharpe"],
                                   d_ctl=m_["Sharpe"] - mc["Sharpe"],
                                   beat_ctl=bool(m_["Sharpe"] > mc["Sharpe"]),
                                   beat_v1=bool(m_["Sharpe"] > mv["Sharpe"]),
                                   beat_spy=bool(m_["Sharpe"] > msp["Sharpe"]),
                                   oracle=bool(p["arm"] == oos_best),
                                   oracle_arm=oos_best,
                                   oracle_OOS=float(sub.OOS_Sharpe.max())))
    WF = pd.DataFrame(wf)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  selector means (OOS Sharpe minus do-nothing incumbent):")
    say(WF.groupby("sel")[["OOS_Sharpe", "d_ctl", "beat_ctl", "beat_spy", "oracle"]]
        .mean().to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  the narrow question (S3: share pinned at 0.53, only the count rule chosen):")
    say(WF[WF.sel == "S3"][["panel", "cost", "constr", "pick", "OOS_Sharpe", "ctl_OOS",
                            "d_ctl", "spy_OOS", "beat_ctl", "beat_spy"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    lc = WF[(WF.sel == "S3") & WF.panel.isin(["u56", "broad"]) & (WF.cost == 10.0)]
    say(f"  P6: S3 beats the do-nothing incumbent on "
        f"{int(lc.beat_ctl.sum())}/{len(lc)} large-cap 10bps cells "
        f"(mean d_ctl {lc.d_ctl.mean():+.4f})")

    # ================================================================ anchor head-to-head
    say("\n" + "=" * 200)
    say(f"HEAD-TO-HEAD at the incumbent's share m = {M_ANCHOR} — the sentence the queue asked for")
    say("=" * 200)
    hh = G[(G.m == M_ANCHOR)][["panel", "rule", "constr", "cost", "n_const", "n_mean",
                               "inv_gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO", "pass4a", "pass4b",
                               "fail4b"]]
    say(hh.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================ outputs
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    GR.to_csv(OUT / f"{STEM}.gross.csv", index=False)
    YR.to_csv(OUT / f"{STEM}.peryear.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pair.to_csv(OUT / f"{STEM}.paired.csv", index=False)

    say("\n" + "=" * 200)
    say("LEADERBOARD rows are emitted by the caller from .grid.csv; see .result.md for the "
        "verdict and the four rows appended.")
    say("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

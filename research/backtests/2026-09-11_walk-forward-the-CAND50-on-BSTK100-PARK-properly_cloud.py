#!/usr/bin/env python3
"""Idea 702 - "walk-forward-the-CAND50-on-BSTK100-PARK-properly" (cloud, 2026-09-11).

The question
------------
Idea 694 (cloud) reported that CAND50 on the WHOLE BSTK100 pool - a de-grossing book,
because n = 50 is run against a mean eligible count of ~31 - clears PROTOCOL 4b:

    CAGR 11.66%  Sharpe 1.0634  MaxDD -18.71%  halves 1.1481 / 0.9856
    OOS 12.10% / 1.0778 / -18.71%      against SPY 14.13% / 0.8616 / -33.72%

and in the same breath that its own IS-only n-picker does NOT take n = 50: it takes
n = 15, whose OOS Sharpe is 0.9318 and which is not a 4b pass.  That is the whole of the
PARK: the 4b row exists on the grid but nobody showed that an honest rule can REACH it.

This run asks the queue's question directly: **on a pre-registered (n, gross) grid, with the
de-grossing written down rather than hidden inside `GROSS/n`, does ANY selector that sees the
in-sample window ONLY land on a cell that clears 4b?**

Design - one pool, one book family, two dials
--------------------------------------------
PANEL  BSTK100: `universe_broad.json` minus every ETF in `universe.json`
       (broad / sectors / bonds_fx_commod) = 100 large-cap stocks, plus SPY as the
       benchmark column only (never tradable).  ONE fixed pool, no draws - the queue asks
       about "the whole BSTK100 pool", not about sub-panels.
CALENDAR  idea 694's own: the intersection of the small panel's and the broad panel's
       trading days (2010-01-04 .. 2026-09-04), so GATE 0 can reproduce the published row
       exactly.  The panel's NATIVE calendar (2008-01-02 ..) is re-run as a reported
       appendix - it is not a tuned axis, both are published.
BOOK   CAND-n at gross g: RULES v1 eligibility (close > 200d MA AND 20d realised vol
       < 0.60, `score(..., vol_scale=False)` ranking - idea 276's `cand_weights`), hold the
       top n eligible names at g/n of NAV each.  When fewer than n names are eligible the
       book HOLDS CASH: realised gross = g * min(n_elig, n) / n.  That de-grossing is the
       mechanism idea 694 flagged and GATE 2 pins it to an identity.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. n     in {5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100}   (11 rungs; 100 = the whole
             pool, i.e. the capacity-bound EWall limit of the family)
    2. gross in {0.50, 0.75, 1.00}                             (3 rungs; 0.75 is live)
    33 cells.  Cost (10 / 25 / 50 bps), cadence (W), execution lag (t+1), the 260-day
    warm-up skip, the eligibility thresholds and the IS/OOS boundary are INHERITED from the
    record and are reported axes, never tuned.

Rule 8 walk-forward (PROTOCOL rule 8) - the point of the run
-----------------------------------------------------------
IS = ..2016-12-31, OOS = 2017-01-01..  Every selector below sees IS ONLY; its pick is then
read ONCE on the untouched OOS window.  Pre-registered here before any OOS number was read:

    S1 PICK-n  @ g=0.75  argmax over n of IS Sharpe          (idea 694's own selector)
    S2 PICK-n  @ g=0.75  argmax over n of IS Calmar
    S3 PICK-(n,g)        argmax over all 33 cells of IS Sharpe
    S4 PICK-(n,g)        argmax over all 33 cells of IS Calmar
    S5 PICK-4b-IS        among cells that clear a 4b test computed on the IS WINDOW ONLY,
                         argmax IS Sharpe; reported as NONE if the IS-4b set is empty
    S6 PICK-DD           argmax over all 33 cells of IS MaxDD (the shallowest IS drawdown)
    ORACLE               argmax OOS Sharpe - NOT honest, published as the ceiling only
    RECORD               n=50, g=0.75 - idea 694's headline cell, for contrast

VERDICTS - both KEEP paths, and 4b read two ways
    4a-REC / 4b-REC : PROTOCOL 4a / 4b exactly as the record's `keep_paths` computes them
                      (halves and MaxDD/CAGR on the FULL sample, Sharpe on the OOS window).
    4a-OOS / 4b-OOS : the same two clauses restated on the OOS WINDOW ALONE (halves of the
                      OOS window, OOS MaxDD, OOS CAGR).  A selector that only sees IS can
                      only honestly claim this one: the REC reading scores a book partly on
                      the window its own dials were fitted in.
    A cell is "reachable" only if some IS-only selector lands on it.  The run's answer is
    the pair (does any honest selector clear 4b-REC, does any clear 4b-OOS).

Gates, asserted before any new number is read
    G0  REPRODUCTION: CAND50 @ g=0.75 on this panel and calendar reads idea 694's published
        CAGR 0.1166 / Sharpe 1.0634 / MaxDD -0.1871 / H1 1.1481 / H2 0.9856 /
        OOS 0.1210 / 1.0778 / -0.1871, and SPY reads 0.1413 / 0.8616 / -0.3372, at 5e-4;
        and idea 694's IS n-picker claim (n=15, OOS Sharpe 0.9318) reproduces at 5e-4.
    G1  ENVELOPE: SPY is never held; every weight >= 0; max daily gross <= g * (1 + 3/n).
        The slack is not a licence: idea 276's `cand_weights` ranks with pandas' default
        AVERAGE tie method, so on a day when two names tie at the n-th rank BOTH clear
        `rank <= n` and the book holds n+1 (up to n+2 at n=10) lots of g/n.  That is a property of the
        inherited book, not of this run; the tie-day count is printed for every cell and
        every cell's own max gross is published.
    G2  DE-GROSSING IDENTITY: mean realised gross over rebalance days equals
        g * mean(held count) / n to 1e-12 for every one of the 33 cells, and the
        capacity reading g * mean(min(n_elig, n)) / n is published beside it with its
        (tie-driven) residual, so the de-grossing is written down rather than implied.
    G3  CONTROL: a ZERO-SIGNAL book (the same de-grossing envelope, names drawn at random
        from the eligible set instead of ranked) is run on the same grid at one seed, so the
        4b counts below can be read against a no-information base rate rather than against 0.

SURVIVORSHIP (idea 54): BSTK100 is the CURRENT constituent list of `universe_broad.json`
minus ETFs - names that left the large-cap universe over 2010-2026 are absent, so every
LEVEL here (the book's and SPY's alike) is optimistic and the book's more so, since the gate
holds only names that are above their own 200d MA.  This biases a level, not the within-grid
comparison of one selector against another, which is what the run adjudicates.

CAPACITY (reported, not tuned): n above the panel's mean eligible count Ebar makes CAND-n an
EWall book that de-grosses; n/Ebar and the realised fill are printed for every cell.

Outputs: .grid.csv .walkforward.csv .costappendix.csv .native.csv .console.txt .result.md
"""
import json, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask                 # noqa: E402

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

FREQ = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]      # tuned param 1
GS = [0.50, 0.75, 1.00]                                # tuned param 2
COSTS = [10, 25, 50]                                   # reported axis, 10 bps is PROTOCOL
SEED = 702

# idea 694's published cell, to be reproduced before it is decomposed (GATE 0)
PUB = dict(CAGR=0.1166, Sharpe=1.0634, MaxDD=-0.1871, H1=1.1481, H2=0.9856,
           OOS_CAGR=0.1210, OOS_Sharpe=1.0778, OOS_MaxDD=-0.1871)
PUB_SPY = dict(CAGR=0.1413, Sharpe=0.8616, MaxDD=-0.3372)
PUB_ISPICK_N, PUB_ISPICK_OOS_S = 15, 0.9318
GATE_TOL = 5e-4


# ------------------------------------------------------------------ panel
def bstk100(common_calendar=True):
    """BSTK100 = universe_broad.json minus every ETF, + SPY as benchmark column only."""
    pxb = load_universe(broad=True)
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    cols = [c for c in pxb.columns if c != "SPY" and c not in etfs]
    if common_calendar:                                  # idea 694's calendar, for GATE 0
        idx = load_universe(small=True).index.intersection(pxb.index)
        pxb = pxb.reindex(idx).ffill()
    return pxb[cols + ["SPY"]].dropna(how="all").ffill(), cols


# ------------------------------------------------------------------ books
def eligible(px, cols):
    sub = px[cols]
    above = sub > sub.rolling(200).mean()
    vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)
    return above & (vol20 < 0.60)


def cand_weights(n, g):
    """idea 276's CAND-n at an explicit gross: top n of the eligible set at g/n each.
    Fewer than n eligible -> the remainder is CASH (this is the de-grossing under test)."""
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        s, above, vol20 = score(px[tr], vol_scale=False)
        elig = s.where(above & (vol20 < 0.60))
        rank = elig.rank(axis=1, ascending=False)
        return ((rank <= n).astype(float) * (g / n)).reindex(columns=px.columns).fillna(0.0)
    return f


def random_weights(n, g, seed):
    """GATE 3 zero-signal control: the SAME envelope (top n of the eligible set at g/n,
    cash otherwise) with the ranking replaced by a fixed random score per name-day."""
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        rng = np.random.default_rng(seed)
        noise = pd.DataFrame(rng.random((len(px), len(tr))), index=px.index, columns=tr)
        elig = noise.where(eligible(px, tr))
        rank = elig.rank(axis=1, ascending=False)
        return ((rank <= n).astype(float) * (g / n)).reindex(columns=px.columns).fillna(0.0)
    return f


# ------------------------------------------------------------------ scoring
def seg(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(x); return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def full_row(tag, r):
    """The record's row (idea 286's `full_row`) plus the OOS-window halves this run needs."""
    h = len(r) // 2
    o = r.loc[OOS_START:]; ho = len(o) // 2
    i = r.loc[:IS_END]; hi_ = len(i) // 2
    d, do, di = seg(r), seg(r, OOS_START), seg(r, None, IS_END)
    return dict(tag=tag, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS_CAGR=do["CAGR"], OOS_Sharpe=do["Sharpe"], OOS_MaxDD=do["MaxDD"],
                OOS_H1=metrics(o.iloc[:ho])["Sharpe"], OOS_H2=metrics(o.iloc[ho:])["Sharpe"],
                IS_CAGR=di["CAGR"], IS_Sharpe=di["Sharpe"], IS_MaxDD=di["MaxDD"],
                IS_H1=metrics(i.iloc[:hi_])["Sharpe"], IS_H2=metrics(i.iloc[hi_:])["Sharpe"])


def keep_rec(row, spy, v2):
    """PROTOCOL 4a / 4b exactly as the record's `keep_paths` computes them."""
    a = (row["H1"] > v2["H1"] and row["H2"] > v2["H2"] and row["MaxDD"] >= v2["MaxDD"])
    b = (row["H1"] > spy["H1"] and row["H2"] > spy["H2"]
         and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def keep_win(row, spy, v2, pre):
    """The same two clauses restated on ONE window (pre = 'OOS_' or 'IS_')."""
    S, C, D = pre + "Sharpe", pre + "CAGR", pre + "MaxDD"
    H1, H2 = pre + "H1", pre + "H2"
    a = (row[H1] > v2[H1] and row[H2] > v2[H2] and row[D] >= v2[D])
    b = (row[H1] > spy[H1] and row[H2] > spy[H2] and row[S] > spy[S]
         and row[D] >= 0.60 * spy[D] and row[C] >= 0.70 * spy[C])
    return bool(a), bool(b)


def run_cell(px, wfn, cost, st):
    return backtest(px, wfn(px), cost_bps=cost, freq=FREQ)["returns"].loc[st:]


# ------------------------------------------------------------------ grid
def build_grid(px, cols, cost, label, gate_envelope=False, control_seed=None):
    """Every (n, g) cell on one panel at one cost.  Returns the rows plus the comparands."""
    st = px.index[260]
    spy = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
    v2 = full_row("RULESv2", run_cell(px, lambda p: rules_v2_weights(p)
                                      .drop(columns=["SPY"], errors="ignore")
                                      .reindex(columns=p.columns).fillna(0.0), cost, st))
    el = eligible(px, cols)
    mask = rebalance_mask(px.index, FREQ)
    nel = el.loc[mask.values].sum(axis=1).loc[st:]
    Ebar = float(nel.mean())
    rows, envelope_bad = [], []
    for g in GS:
        for n in NS:
            wfn = cand_weights(n, g) if control_seed is None else random_weights(n, g, control_seed)
            w = wfn(px)
            held = (w.drop(columns=["SPY"]) > 0).sum(axis=1).loc[mask.values].loc[st:]
            gmax = float(w.sum(axis=1).max())
            if gate_envelope:
                if float(w["SPY"].abs().max()) != 0.0: envelope_bad.append((n, g, "SPY held"))
                if float(w.min().min()) < 0.0: envelope_bad.append((n, g, "negative weight"))
                if gmax > g * (1 + 3.0 / n) + 1e-12: envelope_bad.append((n, g, "gross"))
            r = run_cell(px, wfn, cost, st)
            row = full_row(f"CAND{n}@{g:.2f}", r)
            a_r, b_r = keep_rec(row, spy, v2)
            a_o, b_o = keep_win(row, spy, v2, "OOS_")
            a_i, b_i = keep_win(row, spy, v2, "IS_")
            gross_obs = float(w.sum(axis=1).loc[mask.values].loc[st:].mean())
            fill = float(held.mean()) / n                      # realised fill
            cap_fill = float(np.minimum(nel, n).mean()) / n    # capacity reading
            rows.append(dict(panel=label, cost=cost, n=n, gross=g, Ebar=Ebar,
                             n_over_Ebar=n / Ebar, fill=fill, cap_fill=cap_fill,
                             tie_days=int((held > n).sum()), max_gross=gmax,
                             realised_gross=gross_obs, identity=abs(gross_obs - g * fill),
                             cap_residual=abs(fill - cap_fill),
                             **{k: v for k, v in row.items() if k != "tag"},
                             pass4a_rec=a_r, pass4b_rec=b_r,
                             pass4a_oos=a_o, pass4b_oos=b_o,
                             pass4a_is=a_i, pass4b_is=b_i))
    return pd.DataFrame(rows), spy, v2, envelope_bad, Ebar


# ------------------------------------------------------------------ selectors
def selectors(df):
    """Every IS-only selector, pre-registered in the docstring.  ORACLE is not honest."""
    at75 = df[np.isclose(df.gross, 0.75)]
    out = []
    def add(name, sub, key, honest=True, maximise=True):
        if sub is None or len(sub) == 0:
            out.append(dict(selector=name, honest=honest, n=np.nan, gross=np.nan,
                            choice_set=0)); return
        i = sub[key].idxmax() if maximise else sub[key].idxmin()
        r = df.loc[i]
        out.append(dict(selector=name, honest=honest, n=int(r.n), gross=float(r.gross),
                        choice_set=len(sub), IS_Sharpe=r.IS_Sharpe, IS_CAGR=r.IS_CAGR,
                        IS_MaxDD=r.IS_MaxDD,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                        fill=r.fill, n_over_Ebar=r.n_over_Ebar,
                        pass4a_rec=bool(r.pass4a_rec), pass4b_rec=bool(r.pass4b_rec),
                        pass4a_oos=bool(r.pass4a_oos), pass4b_oos=bool(r.pass4b_oos)))
    d = df.copy()
    d["IS_Calmar"] = d.IS_CAGR / d.IS_MaxDD.abs()
    a75 = d[np.isclose(d.gross, 0.75)]
    add("S1 PICK-n @g=0.75 by IS Sharpe", a75, "IS_Sharpe")
    add("S2 PICK-n @g=0.75 by IS Calmar", a75, "IS_Calmar")
    add("S3 PICK-(n,g) by IS Sharpe", d, "IS_Sharpe")
    add("S4 PICK-(n,g) by IS Calmar", d, "IS_Calmar")
    add("S5 PICK-4b-IS then IS Sharpe", d[d.pass4b_is], "IS_Sharpe")
    add("S6 PICK-(n,g) by IS MaxDD", d, "IS_MaxDD")
    add("ORACLE argmax OOS Sharpe", d, "OOS_Sharpe", honest=False)
    rec = d[(d.n == 50) & np.isclose(d.gross, 0.75)]
    add("RECORD n=50 g=0.75 (idea 694)", rec, "IS_Sharpe", honest=False)
    return pd.DataFrame(out), at75


def fmt(df, cols, nd=4):
    return df[cols].to_string(index=False,
                              float_format=lambda x: f"{x:.{nd}f}")


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 702 - walk-forward-the-CAND50-on-BSTK100-PARK-properly   (cloud, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED (docstring, fixed before any number below was read):")
    P(f"  grid  n in {NS}  x  gross in {GS}  = {len(NS) * len(GS)} cells, ALL reported")
    P("  selectors S1..S6 see the IS window ONLY; ORACLE and RECORD are labelled not-honest")
    P("  4b read two ways: 4b-REC (the record's full-sample clauses) and 4b-OOS (OOS window")
    P("  alone).  The run's answer is whether any HONEST selector clears either.")
    P(f"  costs {COSTS} bps (10 is PROTOCOL; 25/50 are a reported appendix, not tuned)")

    px, cols = bstk100(common_calendar=True)
    P(f"\nPANEL BSTK100: {len(cols)} stocks + SPY (benchmark only); calendar "
      f"{px.index[0].date()} .. {px.index[-1].date()} ({len(px)} days), "
      f"scored from {px.index[260].date()} after the 260-day warm-up skip")
    P("  (idea 694's calendar: broad-panel days intersected with the small panel's)")

    # ------------------------------------------------------------ headline grid
    P("\n" + "=" * 100)
    P("THE GRID at 10 bps, weekly, t+1")
    P("=" * 100)
    grid, spy, v2, bad, Ebar = build_grid(px, cols, 10, "BSTK100", gate_envelope=True)

    P("\n--- GATE 1: envelope ---")
    assert not bad, f"GATE 1 FAILED: {bad[:5]}"
    P(f"  GATE 1 PASS - all {len(grid)} cells: SPY never held, no negative weight, "
      "daily gross never above g x (1 + 3/n).")
    P(f"  tie days (book holds n+1 lots because two names share the n-th rank): "
      f"{int(grid.tie_days.sum())} cell-days over {len(grid)} cells x "
      f"{int(rebalance_mask(px.index, FREQ).loc[px.index >= px.index[260]].sum())} rebalance "
      f"days; worst single cell {int(grid.tie_days.max())}, worst max gross overshoot "
      f"{float((grid.max_gross / grid.gross - 1).max()):.4f} of g.")

    P("\n--- GATE 2: de-grossing identity  realised gross == g * mean(held)/n ---")
    worst = float(grid.identity.max())
    assert worst < 1e-12, f"GATE 2 FAILED: worst |realised - g*fill| = {worst:.3e}"
    P(f"  GATE 2 PASS - worst |realised gross - g x fill| over {len(grid)} cells "
      f"= {worst:.2e} (bar 1e-12)")
    P(f"  capacity reading g x mean(min(n_elig,n))/n differs from the realised fill by at "
      f"most {float(grid.cap_residual.max()):.2e} (the tie days above), so 'de-grossing "
      "because fewer than n names are eligible' is the whole of the gap.")
    P(f"  Ebar (mean eligible names on a rebalance day) = {Ebar:.2f} of {len(cols)}; "
      f"n > Ebar for n >= {min([n for n in NS if n > Ebar])}, i.e. "
      f"{sum(1 for n in NS if n > Ebar)} of {len(NS)} rungs are capacity-bound and DE-GROSS.")

    P("\n--- GATE 0: reproduce idea 694's published cell before decomposing it ---")
    cell = grid[(grid.n == 50) & np.isclose(grid.gross, 0.75)].iloc[0]
    dev = {k: abs(float(cell[k]) - v) for k, v in PUB.items()}
    sdev = {k: abs(float(spy[k]) - v) for k, v in PUB_SPY.items()}
    for k, v in PUB.items():
        P(f"    CAND50  {k:11s} published {v:+.4f}  here {float(cell[k]):+.4f}  "
          f"|d| {dev[k]:.2e}")
    for k, v in PUB_SPY.items():
        P(f"    SPY     {k:11s} published {v:+.4f}  here {float(spy[k]):+.4f}  "
          f"|d| {sdev[k]:.2e}")
    pick_is = grid[np.isclose(grid.gross, 0.75)].set_index("n").IS_Sharpe.idxmax()
    oos_of_pick = float(grid[(grid.n == pick_is) & np.isclose(grid.gross, 0.75)].OOS_Sharpe.iloc[0])
    P(f"    IS n-picker @g=0.75: published n={PUB_ISPICK_N} OOS Sharpe {PUB_ISPICK_OOS_S:.4f}; "
      f"here n={pick_is} OOS Sharpe {oos_of_pick:.4f}")
    allmax = max(list(dev.values()) + list(sdev.values()))
    assert allmax < GATE_TOL, f"GATE 0 FAILED: worst deviation {allmax:.3e}"
    assert pick_is == PUB_ISPICK_N and abs(oos_of_pick - PUB_ISPICK_OOS_S) < GATE_TOL, \
        "GATE 0 FAILED: the IS n-picker claim does not reproduce"
    P(f"  GATE 0 PASS - worst deviation {allmax:.2e} against a {GATE_TOL:.0e} bar; the "
      "PARK's two published facts both reproduce on this run's own code.")

    P("\n--- every grid point, 10 bps (the run's full report; nothing dropped) ---")
    show = ["n", "gross", "n_over_Ebar", "fill", "realised_gross", "IS_Sharpe", "IS_CAGR",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "pass4a_rec", "pass4b_rec", "pass4a_oos", "pass4b_oos"]
    P(grid[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P(f"\nCOMPARANDS on the same panel and calendar (10 bps):")
    for nm, rr in (("RULES v2 (live baseline)", v2), ("SPY buy-and-hold", spy)):
        P(f"  {nm:26s} CAGR {rr['CAGR']:+.4f}  Sharpe {rr['Sharpe']:.4f}  "
          f"MaxDD {rr['MaxDD']:+.4f}  halves {rr['H1']:.4f}/{rr['H2']:.4f}  |  "
          f"OOS {rr['OOS_CAGR']:+.4f}/{rr['OOS_Sharpe']:.4f}/{rr['OOS_MaxDD']:+.4f}  "
          f"OOS halves {rr['OOS_H1']:.4f}/{rr['OOS_H2']:.4f}")

    P(f"\nKEEP-path counts over the {len(grid)} cells at 10 bps:")
    for c, lab in (("pass4a_rec", "4a (record reading)"), ("pass4b_rec", "4b (record reading)"),
                   ("pass4a_oos", "4a (OOS window only)"), ("pass4b_oos", "4b (OOS window only)"),
                   ("pass4b_is", "4b (IS window only)")):
        P(f"  {lab:24s} {int(grid[c].sum()):3d} / {len(grid)}")
    for c, lab in (("pass4b_rec", "4b-REC"), ("pass4b_oos", "4b-OOS")):
        s = grid[grid[c]]
        P(f"  {lab} passers: " + (", ".join(f"n={int(r.n)}@g={r.gross:.2f}"
                                            for _, r in s.iterrows()) if len(s) else "none"))

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - dials chosen on 2010..2016 ONLY, read once on 2017..2026")
    P("=" * 100)
    wf, _ = selectors(grid)
    for r in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"):
        wf[f"spy_{r}"] = spy[r]; wf[f"v2_{r}"] = v2[r]
    wf["beats_spy_OOS_S"] = wf.OOS_Sharpe > spy["OOS_Sharpe"]
    wf["beats_v2_OOS_S"] = wf.OOS_Sharpe > v2["OOS_Sharpe"]
    P("\n  pick, then OOS - against SPY OOS "
      f"{spy['OOS_CAGR']:+.4f}/{spy['OOS_Sharpe']:.4f}/{spy['OOS_MaxDD']:+.4f} and "
      f"RULES v2 OOS {v2['OOS_CAGR']:+.4f}/{v2['OOS_Sharpe']:.4f}/{v2['OOS_MaxDD']:+.4f}")
    P(fmt(wf, ["selector", "honest", "n", "gross", "choice_set", "IS_Sharpe",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "beats_spy_OOS_S", "beats_v2_OOS_S",
               "pass4b_rec", "pass4b_oos", "pass4a_rec"]))

    hon = wf[wf.honest]
    reach_rec = hon[hon.pass4b_rec.fillna(False)]
    reach_oos = hon[hon.pass4b_oos.fillna(False)]
    P(f"\n  HONEST selectors: {len(hon)}.  Reaching 4b-REC: {len(reach_rec)}.  "
      f"Reaching 4b-OOS: {len(reach_oos)}.")
    P(f"  Distinct cells the honest selectors land on: "
      f"{sorted({(int(r.n), round(float(r.gross), 2)) for _, r in hon.iterrows() if np.isfinite(r.n)})}")
    P(f"  Is n=50 @ g=0.75 among them? "
      f"{'YES' if ((hon.n == 50) & np.isclose(hon.gross.fillna(-1), 0.75)).any() else 'NO'}")

    # ------------------------------------------------------------ gate 3 control
    P("\n" + "=" * 100)
    P("GATE 3 - ZERO-SIGNAL CONTROL (same de-grossing envelope, random names)")
    P("=" * 100)
    ctrl, cspy, cv2, _, _ = build_grid(px, cols, 10, "BSTK100-control", control_seed=SEED)
    P(f"  control 4b-REC {int(ctrl.pass4b_rec.sum())}/{len(ctrl)}, "
      f"4b-OOS {int(ctrl.pass4b_oos.sum())}/{len(ctrl)}, "
      f"4a-REC {int(ctrl.pass4a_rec.sum())}/{len(ctrl)}  "
      f"(signal book: {int(grid.pass4b_rec.sum())}/{int(grid.pass4b_oos.sum())}/"
      f"{int(grid.pass4a_rec.sum())})")
    cwf, _ = selectors(ctrl)
    chon = cwf[cwf.honest]
    P(f"  control honest selectors reaching 4b-REC: "
      f"{int(chon.pass4b_rec.fillna(False).sum())}/{len(chon)}; 4b-OOS: "
      f"{int(chon.pass4b_oos.fillna(False).sum())}/{len(chon)}")
    P("  control mean OOS Sharpe %.4f vs signal %.4f" %
      (ctrl.OOS_Sharpe.mean(), grid.OOS_Sharpe.mean()))

    # ------------------------------------------------------------ cost appendix
    P("\n" + "=" * 100)
    P("COST APPENDIX - the same 33 cells at 25 and 50 bps (reported axis, not tuned)")
    P("=" * 100)
    apx = [grid]
    for c in COSTS[1:]:
        gc, sc, vc, _, _ = build_grid(px, cols, c, "BSTK100")
        apx.append(gc)
        wfc, _ = selectors(gc)
        hc = wfc[wfc.honest]
        P(f"  {c:2d} bps: 4b-REC {int(gc.pass4b_rec.sum()):2d}/{len(gc)}, "
          f"4b-OOS {int(gc.pass4b_oos.sum()):2d}/{len(gc)}; honest selectors reaching "
          f"4b-REC {int(hc.pass4b_rec.fillna(False).sum())}/{len(hc)}, "
          f"4b-OOS {int(hc.pass4b_oos.fillna(False).sum())}/{len(hc)}; "
          f"S1 picks n={int(hc.iloc[0].n)} OOS S {hc.iloc[0].OOS_Sharpe:.4f}; "
          f"n=50@0.75 OOS S "
          f"{float(gc[(gc.n == 50) & np.isclose(gc.gross, 0.75)].OOS_Sharpe.iloc[0]):.4f}")
    cost_df = pd.concat(apx, ignore_index=True)

    # ------------------------------------------------------------ native calendar
    P("\n" + "=" * 100)
    P("APPENDIX - the SAME grid on BSTK100's NATIVE calendar (2008-01-02 .., +2 years)")
    P("=" * 100)
    pxn, colsn = bstk100(common_calendar=False)
    P(f"  {pxn.index[0].date()} .. {pxn.index[-1].date()} ({len(pxn)} days), scored from "
      f"{pxn.index[260].date()}")
    gn, sn, vn, _, En = build_grid(pxn, colsn, 10, "BSTK100-native")
    wn, _ = selectors(gn)
    hn = wn[wn.honest]
    P(f"  Ebar {En:.2f}; 4b-REC {int(gn.pass4b_rec.sum())}/{len(gn)}, "
      f"4b-OOS {int(gn.pass4b_oos.sum())}/{len(gn)}, 4a-REC {int(gn.pass4a_rec.sum())}/{len(gn)}")
    P(f"  SPY here: {sn['CAGR']:+.4f}/{sn['Sharpe']:.4f}/{sn['MaxDD']:+.4f}; "
      f"n=50@0.75: {float(gn[(gn.n == 50) & np.isclose(gn.gross, 0.75)].Sharpe.iloc[0]):.4f} Sharpe")
    P(fmt(hn, ["selector", "n", "gross", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
               "pass4b_rec", "pass4b_oos"]))
    P(f"  honest selectors reaching 4b-REC {int(hn.pass4b_rec.fillna(False).sum())}/{len(hn)}, "
      f"4b-OOS {int(hn.pass4b_oos.fillna(False).sum())}/{len(hn)}")

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 100)
    reach = len(reach_rec) > 0 or len(reach_oos) > 0
    nat_reach = int(hn.pass4b_rec.fillna(False).sum()) + int(hn.pass4b_oos.fillna(False).sum())
    P(f"ANSWER: honest (IS-only) selectors reaching the 4b row on the record's calendar: "
      f"4b-REC {len(reach_rec)}/{len(hon)}, 4b-OOS {len(reach_oos)}/{len(hon)}; "
      f"on the native calendar {nat_reach} in total.")
    P("=" * 100)

    grid.to_csv(f"{OUT}.grid.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    cost_df.to_csv(f"{OUT}.costappendix.csv", index=False)
    gn.to_csv(f"{OUT}.native.csv", index=False)
    ctrl.to_csv(f"{OUT}.control.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {OUT.name}.{{grid,walkforward,costappendix,native,control}}.csv  "
      f"({time.time() - t0:.1f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

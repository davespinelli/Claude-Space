#!/usr/bin/env python3
"""Idea 503 - is-the-4b-PASS-SHARE-a-monotone-function-of-n  (lane B, 2026-09-11)

THE QUESTION
  Idea 486 published a 4b pass share of 747/3000 at book size n=20 and 61/3000 at n=5 on the
  SAME 3,000 B136 sub-panel draws, every other dial fixed - a 12x gap from the book-size dial
  alone.  The queue asks: sweep n in {5,10,15,20,30,40} over those committed draws and report
  the 4b pass share, the median Sharpe and the median MaxDD at each n, on B136 and SMALL484.
  If the share is monotone in n, the record's 4b counts are not comparable across books of
  different size and every published count needs its n.

TWO TUNED PARAMETERS (PROTOCOL rule 4, max 2 - the queue's own)
  n      book size in {5, 10, 15, 20, 30, 40}
  panel  {B136, SMALL484}
  ALL 12 grid points are printed and written to .grid.csv.  The sub-panel width k in {20,40,80}
  and the BOOK FORM (see below) are REPORTING axes, not tuned: every point is published.

THE BOOK FORM AXIS (why it has to be here)
  Idea 78/83/486's CAND-n book is  w = GROSS / n  on the top-n ranked eligible names.  When
  fewer than n names are eligible on a rebalance day the book holds n_elig * GROSS/n < GROSS:
  the n dial is also a GROSS dial.  At k=20 the n=40 book can never exceed gross 0.375.  Any
  "pass share rises with n" read on that form is confounded with exposure (the record's own
  gross loophole, ideas 311/657).  So every number below is published twice:
    NOM    w = GROSS/n                       (idea 486's form, verbatim - the gate reproduces it)
    MATCH  w = GROSS/min(n, n_elig_t)        (same names, same ranks, gross held at GROSS)
  If the monotonicity survives MATCH it is a book-size fact; if it does not, it is an exposure fact.

STRUCTURE
  Gate 0   fast_backtest vs engine.backtest; the live RULES v2 line; and a DIGIT gate - this
           run's n=5 and n=20 NOM metrics against idea 486's committed 6,000-row grid.
  PART A   the 12-point grid: 4b pass share, median Sharpe, median MaxDD, median CAGR, realised
           gross, per n per panel; pooled and per k cell; Spearman and strict-monotonicity test.
  PART B   which 4b leg binds at each n, and the 4a / BOTH counts against the LIVE RULES v2.
  PART C   RULE 8 walk-forward - n chosen on 2009-2016 IS pass share ONLY, 2017-2026 read once.
  PART D   both KEEP paths on the rule-8 picked books, full sample, 10 bps.

Costs 10 bps, weekly, next-day execution, no shorting, no leverage.  Deterministic.
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT modified by this script.
SURVIVORSHIP (PROTOCOL rule 9): B136 and SMALL484 are current constituents; the random
sub-panel draws inherit that bias in full.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics, rebalance_mask                          # noqa

# ---- idea 78/83/252/484/486's constants, imported verbatim -----------------------
COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
KS = [20, 40, 80]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_B = 78_500                       # idea 486's draw seed base: per cell = SEED_B + k
D_MAX = 1000                          # idea 486's draw depth per k cell
PANELS = ["B136", "SMALL484"]

# ---- this run's axes -------------------------------------------------------------
NS = [5, 10, 15, 20, 30, 40]          # tuned axis 1 (every point published)
FORMS = ["NOM", "MATCH"]              # reporting axis

SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]
REF486 = OUT / "2026-09-09_census-every-published-N-EQUALS-50-model-comparison-in-the-record_C.grid.csv.gz"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)

def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ================================================================== book helpers (idea 486's)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    """Vectorised equivalent of engine.backtest's return series (gated at [a])."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * cost_bps / 1e4, index=idx)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def panel_defs():
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    return {
        "B136": (px136, [c for c in px136.columns]),
        "SMALL484": (pxs, [c for c in pxs.columns if c != "SPY"]),
    }


def draw_books(px, names, k, d_hi, seed, startb):
    """Idea 486's draw_books, extended over NS and both book forms.  Draw d is the d-th name
    set from the generator seeded once per (panel, k), so draws 0..999 ARE idea 486's own."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in range(d_hi):
        cols = list(rng.choice(names, size=k, replace=False))
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop: elig[drop] = False
        rank = s.where(elig).rank(axis=1, ascending=False)
        ne_t = elig.sum(axis=1)                       # eligible count per day
        wm = rebalance_mask(p.index, FREQ).values
        rec = dict(k=k, draw=d, n_elig=float(ne_t[wm].loc[startb:].mean()))
        for nb in NS:
            sel = (rank <= nb).astype(float)
            for form in FORMS:
                if form == "NOM":
                    w = sel * (GROSS / nb)
                else:
                    denom = np.minimum(ne_t, nb).replace(0, np.nan)
                    w = sel.div(denom, axis=0).mul(GROSS).fillna(0.0)
                r = fast_backtest(p, w).loc[startb:]
                m = metrics(r); h1, h2 = half_sharpes(r)
                ris = r.loc[:IS_END]; roo = r.loc[OOS_START:]
                mis, moo = metrics(ris), metrics(roo)
                hi1, hi2 = half_sharpes(ris)
                t = f"{form}{nb}"
                rec.update({
                    f"CAGR_{t}": m["CAGR"], f"Sharpe_{t}": m["Sharpe"], f"MaxDD_{t}": m["MaxDD"],
                    f"H1_{t}": h1, f"H2_{t}": h2,
                    f"gross_{t}": float(w[wm].loc[startb:].sum(axis=1).mean()),
                    f"CAGR_IS_{t}": mis["CAGR"], f"Sharpe_IS_{t}": mis["Sharpe"],
                    f"MaxDD_IS_{t}": mis["MaxDD"], f"H1IS_{t}": hi1, f"H2IS_{t}": hi2,
                    f"CAGR_OOS_{t}": moo["CAGR"], f"Sharpe_OOS_{t}": moo["Sharpe"],
                    f"MaxDD_OOS_{t}": moo["MaxDD"],
                })
        rows.append(rec)
    return rows


# ================================================================== PROTOCOL bars
def bars_4b(spy_r, spy_is, spy_oos):
    """PROTOCOL 4b on a return window: Sharpe > SPY in BOTH halves and OOS, MaxDD <= 60% of
    SPY's, CAGR >= 70% of SPY's.  Returns the five bar levels for that window."""
    h1, h2 = half_sharpes(spy_r)
    m = metrics(spy_r)
    return dict(H1=h1, H2=h2, OOS=metrics(spy_oos)["Sharpe"],
                DD=0.60 * abs(m["MaxDD"]), CAGR=0.70 * m["CAGR"])


def pass_4b(row, t, bars, oos_field="Sharpe_OOS_"):
    return (row[f"H1_{t}"] > bars["H1"] and row[f"H2_{t}"] > bars["H2"]
            and row[f"{oos_field}{t}"] > bars["OOS"]
            and abs(row[f"MaxDD_{t}"]) <= bars["DD"] and row[f"CAGR_{t}"] >= bars["CAGR"])


def slack_4b(G, t, bars):
    """Signed slack on each leg (positive = clears).  Vectorised over the grid frame."""
    return pd.DataFrame({
        "H1": G[f"H1_{t}"] - bars["H1"],
        "H2": G[f"H2_{t}"] - bars["H2"],
        "OOS": G[f"Sharpe_OOS_{t}"] - bars["OOS"],
        "DD": bars["DD"] - G[f"MaxDD_{t}"].abs(),
        "CAGR": G[f"CAGR_{t}"] - bars["CAGR"],
    })


def spearman(a, b):
    a = pd.Series(a).rank(); b = pd.Series(b).rank()
    if a.std() == 0 or b.std() == 0: return np.nan
    return float(np.corrcoef(a, b)[0, 1])


# ================================================================== MAIN
def main():
    t_start = time.time()
    P("=" * 200)
    P("IDEA 503 - IS THE 4b PASS SHARE A MONOTONE FUNCTION OF n?   (lane B, 2026-09-11)")
    P("=" * 200)
    P(__doc__.strip().split("STRUCTURE")[0])

    panels = panel_defs()
    ctx = {}
    P("\n" + "=" * 200)
    P("GATE 0 - the object under test")
    P("=" * 200)
    for pan in PANELS:
        px, names = panels[pan]
        startb = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[startb:]
        b2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        b1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        bars = bars_4b(spy, spy.loc[:IS_END], spy.loc[OOS_START:])
        bars_oos = bars_4b(spy.loc[OOS_START:], spy.loc[OOS_START:], spy.loc[OOS_START:])
        ctx[pan] = dict(px=px, names=names, startb=startb, spy=spy, b2=b2, b1=b1,
                        bars=bars, bars_oos=bars_oos)
        ms, m2 = metrics(spy), metrics(b2)
        s1, s2 = half_sharpes(spy); v1, v2 = half_sharpes(b2)
        P(f"\n  {pan}: {len(names)} tradable names, {startb.date()} -> {px.index[-1].date()} ({len(spy)} days)")
        P(f"    SPY          {ms['CAGR']:.4%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.4%}  halves {s1:.4f}/{s2:.4f}"
          f"  OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.4f}")
        P(f"    RULES v2     {m2['CAGR']:.4%} / {m2['Sharpe']:.4f} / {m2['MaxDD']:.4%}  halves {v1:.4f}/{v2:.4f}"
          f"  OOS {metrics(b2.loc[OOS_START:])['Sharpe']:.4f}   (live baseline, the 4a comparand)")
        P(f"    4b bars      H1 > {bars['H1']:.4f}, H2 > {bars['H2']:.4f}, OOS Sharpe > {bars['OOS']:.4f}, "
          f"|MaxDD| <= {bars['DD']:.4%}, CAGR >= {bars['CAGR']:.4%}")

    # [a] fast_backtest vs engine.backtest
    px136 = panels["B136"][0]; sb = ctx["B136"]["startb"]
    rng = np.random.default_rng(SEED_B + 40)
    gmax = 0.0
    for _ in range(6):
        cols = list(rng.choice(panels["B136"][1], size=40, replace=False))
        keep = list(dict.fromkeys(cols + ["SPY"]))
        p = px136[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        elig[[c for c in p.columns if c not in set(cols)]] = False
        w = (s.where(elig).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
        a = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[sb:]
        b = fast_backtest(p, w).loc[sb:]
        gmax = max(gmax, float((a - b).abs().max()))
    ok_a = gmax < 1e-12
    P(f"\n  [a] fast_backtest vs engine.backtest, 6 books: max |dret| {gmax:.3e}   {'PASS' if ok_a else 'FAIL'}")

    # ---- the draws -------------------------------------------------------------
    P("\n" + "=" * 200)
    P(f"BUILDING THE GRID - {len(PANELS)} panels x {len(KS)} k cells x {D_MAX} draws x {len(NS)} n x {len(FORMS)} forms")
    P("=" * 200)
    frames = []
    for pan in PANELS:
        c = ctx[pan]
        for k in KS:
            t0 = time.time()
            rows = draw_books(c["px"], c["names"], k, D_MAX, SEED_B + k, c["startb"])
            df = pd.DataFrame(rows); df.insert(0, "panel", pan)
            frames.append(df)
            P(f"    {pan} k={k:3d}  {len(df)} draws  {time.time()-t0:6.1f}s")
    G = pd.concat(frames, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    P(f"  grid: {G.shape[0]} draw-rows x {G.shape[1]} columns -> {STEM}.grid.csv.gz")

    # [b] DIGIT GATE against idea 486's committed grid
    P("\n  [b] DIGIT GATE - this run's NOM n=5 / n=20 metrics vs idea 486's committed 6,000-row grid")
    ok_b = False
    if REF486.exists():
        R = pd.read_csv(REF486)
        M = G.merge(R, on=["panel", "k", "draw"], suffixes=("", "_ref"))
        P(f"      matched rows: {len(M)} of {len(G)}")
        worst = 0.0; lines = []
        for nb in (5, 20):
            for col, ref in [(f"CAGR_NOM{nb}", f"CAGR{nb}"), (f"Sharpe_NOM{nb}", f"Sharpe{nb}"),
                             (f"MaxDD_NOM{nb}", f"MaxDD{nb}"), (f"H1_NOM{nb}", f"H1_{nb}"),
                             (f"H2_NOM{nb}", f"H2_{nb}"), (f"Sharpe_OOS_NOM{nb}", f"Sharpe_OOS{nb}"),
                             (f"CAGR_OOS_NOM{nb}", f"CAGR_OOS{nb}"), (f"MaxDD_OOS_NOM{nb}", f"MaxDD_OOS{nb}")]:
                d = float((M[col] - M[ref]).abs().max()); worst = max(worst, d)
                lines.append(f"      n={nb:2d} {ref:>14s}  max |d| {d:.3e}")
        for l in lines: P(l)
        ok_b = worst < 1e-12
        P(f"      WORST {worst:.3e}   GATE [b] {'PASS' if ok_b else 'FAIL'} - the draws ARE idea 486's.")
    else:
        P("      idea 486's grid not found - GATE [b] NOT RUNNABLE")

    # [c] reproduce idea 486's published counts 747/3000 (n=20) and 61/3000 (n=5) on B136
    P("\n  [c] COUNT GATE - idea 486's published B136 4b counts, CAND-n NOM form")
    cB = ctx["B136"]
    GB = G[G.panel == "B136"]
    rep = {}
    for nb in (5, 20):
        t = f"NOM{nb}"
        s = slack_4b(GB, t, cB["bars"])
        rep[nb] = int((s > 0).all(axis=1).sum())
    P(f"      n=5  this run {rep[5]:4d} / 3000    idea 486 published   61")
    P(f"      n=20 this run {rep[20]:4d} / 3000    idea 486 published  747")
    ok_c = (rep[5] == 61 and rep[20] == 747)
    P(f"      GATE [c] {'PASS' if ok_c else 'FAIL'}")

    if not ok_a:
        P("\n  ABORT: the backtester does not reproduce the engine.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n"); return

    # ============================================================ PART A - the 12-point grid
    P("\n" + "=" * 200)
    P("PART A - THE GRID.  4b pass share, median Sharpe, median MaxDD at each n.  ALL 12 TUNED POINTS.")
    P("=" * 200)
    rows = []
    for pan in PANELS:
        c = ctx[pan]; sub = G[G.panel == pan]
        for nb in NS:
            for form in FORMS:
                t = f"{form}{nb}"
                s = slack_4b(sub, t, c["bars"])
                ok = (s > 0).all(axis=1)
                # 4a vs the LIVE RULES v2
                bh1, bh2 = half_sharpes(c["b2"]); bdd = abs(metrics(c["b2"])["MaxDD"])
                ok4a = ((sub[f"H1_{t}"] > bh1) & (sub[f"H2_{t}"] > bh2)
                        & (sub[f"MaxDD_{t}"].abs() <= bdd))
                rows.append(dict(panel=pan, n=nb, form=form, N=len(sub),
                                 pass4b=int(ok.sum()), share4b=ok.mean(),
                                 pass4a_v2=int(ok4a.sum()), both=int((ok & ok4a).sum()),
                                 med_Sharpe=sub[f"Sharpe_{t}"].median(),
                                 med_MaxDD=sub[f"MaxDD_{t}"].median(),
                                 med_CAGR=sub[f"CAGR_{t}"].median(),
                                 med_gross=sub[f"gross_{t}"].median(),
                                 med_OOS_Sharpe=sub[f"Sharpe_OOS_{t}"].median()))
    A = pd.DataFrame(rows)
    A.to_csv(OUT / f"{STEM}.grid_summary.csv", index=False)
    for form in FORMS:
        P(f"\n  BOOK FORM {form}" + ("   (idea 486's own: w = GROSS/n, de-grosses when n_elig < n)"
                                     if form == "NOM" else
                                     "   (gross held at 0.75: w = GROSS/min(n, n_elig_t))"))
        show = A[A.form == form].set_index(["panel", "n"])[
            ["N", "pass4b", "share4b", "med_Sharpe", "med_MaxDD", "med_CAGR", "med_gross",
             "med_OOS_Sharpe", "pass4a_v2", "both"]]
        P(fmt(show))

    P("\n  MONOTONICITY in n (pass share), pooled over the three k cells:")
    mono = []
    for pan in PANELS:
        for form in FORMS:
            v = A[(A.panel == pan) & (A.form == form)].sort_values("n")
            sh = v.share4b.values
            strict = bool(np.all(np.diff(sh) > 0))
            weak = bool(np.all(np.diff(sh) >= 0))
            mono.append(dict(panel=pan, form=form, spearman=spearman(v.n.values, sh),
                             strict_increasing=strict, weakly_increasing=weak,
                             share_min=sh.min(), share_max=sh.max(),
                             ratio=(sh.max() / sh.min()) if sh.min() > 0 else np.inf,
                             argmax_n=int(v.n.values[int(np.argmax(sh))])))
    MO = pd.DataFrame(mono)
    P(fmt(MO.set_index(["panel", "form"])))
    MO.to_csv(OUT / f"{STEM}.monotonicity.csv", index=False)

    P("\n  PER k CELL (the reporting axis) - 4b pass share out of 1000 draws per cell:")
    cells = []
    for pan in PANELS:
        c = ctx[pan]
        for k in KS:
            sub = G[(G.panel == pan) & (G.k == k)]
            r = dict(panel=pan, k=k, n_elig=sub.n_elig.mean())
            for form in FORMS:
                for nb in NS:
                    t = f"{form}{nb}"
                    r[f"{form}{nb}"] = float((slack_4b(sub, t, c["bars"]) > 0).all(axis=1).mean())
            cells.append(r)
    CE = pd.DataFrame(cells)
    P(fmt(CE.set_index(["panel", "k"])))
    CE.to_csv(OUT / f"{STEM}.percell.csv", index=False)

    P("\n  REALISED GROSS per cell (NOM form) - the confound, stated as a number:")
    gr = []
    for pan in PANELS:
        for k in KS:
            sub = G[(G.panel == pan) & (G.k == k)]
            gr.append(dict(panel=pan, k=k, n_elig=sub.n_elig.mean(),
                           **{f"n{nb}": sub[f"gross_NOM{nb}"].mean() for nb in NS}))
    GR = pd.DataFrame(gr)
    P(fmt(GR.set_index(["panel", "k"])))
    GR.to_csv(OUT / f"{STEM}.gross.csv", index=False)

    # ============================================================ PART B - which leg binds
    P("\n" + "=" * 200)
    P("PART B - WHICH 4b LEG BINDS AT EACH n (argmin of the signed slack, raw units), all draws")
    P("=" * 200)
    binds = []
    for pan in PANELS:
        c = ctx[pan]; sub = G[G.panel == pan]
        for form in FORMS:
            for nb in NS:
                s = slack_4b(sub, f"{form}{nb}", c["bars"])
                # standardise each leg by its own cross-draw sd so legs are comparable
                z = s / s.std().replace(0, np.nan)
                amin_raw = s.idxmin(axis=1).value_counts(normalize=True)
                amin_z = z.idxmin(axis=1).value_counts(normalize=True)
                row = dict(panel=pan, form=form, n=nb)
                for leg in ["H1", "H2", "OOS", "DD", "CAGR"]:
                    row[f"raw_{leg}"] = float(amin_raw.get(leg, 0.0))
                    row[f"z_{leg}"] = float(amin_z.get(leg, 0.0))
                row["fail_share"] = float((s <= 0).any(axis=1).mean())
                binds.append(row)
    BI = pd.DataFrame(binds)
    BI.to_csv(OUT / f"{STEM}.binding.csv", index=False)
    for form in FORMS:
        P(f"\n  {form}: share of draws whose NEAREST bar is each leg (raw units | draw-sd units)")
        P(fmt(BI[BI.form == form].set_index(["panel", "n"])[
            ["raw_H1", "raw_H2", "raw_OOS", "raw_DD", "raw_CAGR",
             "z_H1", "z_H2", "z_OOS", "z_DD", "z_CAGR", "fail_share"]], 3))

    # ============================================================ PART C - RULE 8
    P("\n" + "=" * 200)
    P("PART C - RULE 8 WALK-FORWARD.  n chosen on 2009-2016 IS pass share ONLY; 2017-2026 read once.")
    P("=" * 200)
    P("  IS bars are SPY 2009-2016 restated on that window (halves of the IS window, OOS leg = IS Sharpe).")
    wf = []
    for pan in PANELS:
        c = ctx[pan]; sub = G[G.panel == pan]
        spy_is = c["spy"].loc[:IS_END]
        h1i, h2i = half_sharpes(spy_is); mis = metrics(spy_is)
        bars_is = dict(H1=h1i, H2=h2i, OOS=mis["Sharpe"], DD=0.60 * abs(mis["MaxDD"]),
                       CAGR=0.70 * mis["CAGR"])
        spy_oos = c["spy"].loc[OOS_START:]
        h1o, h2o = half_sharpes(spy_oos); moo = metrics(spy_oos)
        bars_oo = dict(H1=h1o, H2=h2o, OOS=moo["Sharpe"], DD=0.60 * abs(moo["MaxDD"]),
                       CAGR=0.70 * moo["CAGR"])
        b2oos = c["b2"].loc[OOS_START:]; m2o = metrics(b2oos)
        for form in FORMS:
            isr = []
            for nb in NS:
                t = f"{form}{nb}"
                s_is = pd.DataFrame({
                    "H1": sub[f"H1IS_{t}"] - bars_is["H1"], "H2": sub[f"H2IS_{t}"] - bars_is["H2"],
                    "OOS": sub[f"Sharpe_IS_{t}"] - bars_is["OOS"],
                    "DD": bars_is["DD"] - sub[f"MaxDD_IS_{t}"].abs(),
                    "CAGR": sub[f"CAGR_IS_{t}"] - bars_is["CAGR"]})
                isr.append(((s_is > 0).all(axis=1)).mean())
            pick = NS[int(np.argmax(isr))]
            t = f"{form}{pick}"
            s_oo = pd.DataFrame({
                "H1": sub[f"H1_{t}"] - bars_oo["H1"], "H2": sub[f"H2_{t}"] - bars_oo["H2"],
                "OOS": sub[f"Sharpe_OOS_{t}"] - bars_oo["OOS"],
                "DD": bars_oo["DD"] - sub[f"MaxDD_OOS_{t}"].abs(),
                "CAGR": sub[f"CAGR_OOS_{t}"] - bars_oo["CAGR"]})
            oos_share = float(((s_oo > 0).all(axis=1)).mean())
            # the IS-argmax DRAW inside the picked n, read once OOS
            s_is_pick = pd.DataFrame({
                "H1": sub[f"H1IS_{t}"] - bars_is["H1"], "H2": sub[f"H2IS_{t}"] - bars_is["H2"],
                "OOS": sub[f"Sharpe_IS_{t}"] - bars_is["OOS"],
                "DD": bars_is["DD"] - sub[f"MaxDD_IS_{t}"].abs(),
                "CAGR": sub[f"CAGR_IS_{t}"] - bars_is["CAGR"]})
            bestdraw = sub.loc[sub[f"Sharpe_IS_{t}"].idxmax()]
            wf.append(dict(panel=pan, form=form,
                           IS_shares=" ".join(f"{n}:{v:.3f}" for n, v in zip(NS, isr)),
                           pick_n=pick, IS_share=max(isr), OOS_share=oos_share,
                           med_OOS_CAGR=sub[f"CAGR_OOS_{t}"].median(),
                           med_OOS_Sharpe=sub[f"Sharpe_OOS_{t}"].median(),
                           med_OOS_MaxDD=sub[f"MaxDD_OOS_{t}"].median(),
                           beat_SPY_OOS=float((sub[f"Sharpe_OOS_{t}"] > moo["Sharpe"]).mean()),
                           beat_v2_OOS=float((sub[f"Sharpe_OOS_{t}"] > m2o["Sharpe"]).mean()),
                           pick_draw_k=int(bestdraw.k), pick_draw_d=int(bestdraw.draw),
                           pick_draw_OOS_CAGR=bestdraw[f"CAGR_OOS_{t}"],
                           pick_draw_OOS_Sharpe=bestdraw[f"Sharpe_OOS_{t}"],
                           pick_draw_OOS_MaxDD=bestdraw[f"MaxDD_OOS_{t}"],
                           spy_OOS_Sharpe=moo["Sharpe"], spy_OOS_CAGR=moo["CAGR"],
                           spy_OOS_MaxDD=moo["MaxDD"],
                           v2_OOS_Sharpe=m2o["Sharpe"], v2_OOS_CAGR=m2o["CAGR"],
                           v2_OOS_MaxDD=m2o["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\n  IS pass share by n (the only thing the chooser sees), then the OOS read:")
    P(fmt(WF.set_index(["panel", "form"])[
        ["IS_shares", "pick_n", "IS_share", "OOS_share", "med_OOS_CAGR", "med_OOS_Sharpe",
         "med_OOS_MaxDD", "beat_SPY_OOS", "beat_v2_OOS"]]))
    P("\n  The IS-argmax DRAW inside the picked n, read once out of sample, vs the OOS comparands:")
    P(fmt(WF.set_index(["panel", "form"])[
        ["pick_n", "pick_draw_k", "pick_draw_d", "pick_draw_OOS_CAGR", "pick_draw_OOS_Sharpe",
         "pick_draw_OOS_MaxDD", "spy_OOS_Sharpe", "v2_OOS_Sharpe"]]))

    # ============================================================ PART D - both KEEP paths
    P("\n" + "=" * 200)
    P("PART D - BOTH KEEP PATHS on the rule-8 picked books, FULL SAMPLE, 10 bps")
    P("=" * 200)
    kp = []
    for _, w in WF.iterrows():
        pan = w.panel; c = ctx[pan]; t = f"{w.form}{w.pick_n}"
        row = G[(G.panel == pan) & (G.k == w.pick_draw_k) & (G.draw == w.pick_draw_d)].iloc[0]
        bh1, bh2 = half_sharpes(c["b2"]); bdd = abs(metrics(c["b2"])["MaxDD"])
        p4a = bool(row[f"H1_{t}"] > bh1 and row[f"H2_{t}"] > bh2 and abs(row[f"MaxDD_{t}"]) <= bdd)
        b = c["bars"]
        p4b = bool(pass_4b(row, t, b))
        kp.append(dict(panel=pan, book=f"CAND-{w.pick_n} {w.form}", k=int(w.pick_draw_k),
                       draw=int(w.pick_draw_d), CAGR=row[f"CAGR_{t}"], Sharpe=row[f"Sharpe_{t}"],
                       MaxDD=row[f"MaxDD_{t}"], H1=row[f"H1_{t}"], H2=row[f"H2_{t}"],
                       OOS_Sharpe=row[f"Sharpe_OOS_{t}"], pass4a_v2=p4a, pass4b=p4b,
                       slack_DD=b["DD"] - abs(row[f"MaxDD_{t}"]),
                       slack_CAGR=row[f"CAGR_{t}"] - b["CAGR"]))
    KP = pd.DataFrame(kp)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    P(fmt(KP.set_index(["panel", "book"])))
    tot = len(KP)
    P(f"\n  4a {int(KP.pass4a_v2.sum())}/{tot}   4b {int(KP.pass4b.sum())}/{tot}   "
      f"BOTH {int((KP.pass4a_v2 & KP.pass4b).sum())}/{tot}")
    P(f"  Over ALL {len(A)} grid points x their draws: "
      f"4a {int(A.pass4a_v2.sum())}/{int(A.N.sum())}, 4b {int(A.pass4b.sum())}/{int(A.N.sum())}, "
      f"BOTH {int(A.both.sum())}/{int(A.N.sum())}")

    P("\n" + "=" * 200)
    P(f"DONE in {time.time()-t_start:.0f}s.  Gates: [a] {'PASS' if ok_a else 'FAIL'}  "
      f"[b] {'PASS' if ok_b else 'FAIL'}  [c] {'PASS' if ok_c else 'FAIL'}")
    P("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

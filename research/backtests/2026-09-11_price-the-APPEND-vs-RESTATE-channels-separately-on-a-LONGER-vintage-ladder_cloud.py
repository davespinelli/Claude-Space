#!/usr/bin/env python3
"""
IDEA 519 -- price-the-APPEND-vs-RESTATE-channels-separately-on-a-LONGER-vintage-ladder (cloud)
==============================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  idea 514 could only reach one real vintage step (a shallow 50-commit clone) and modelled the
  rest by TRUNCATION, which is the APPEND channel alone; the RESTATEMENT channel was measured at
  max |d| 3.000e-04 over 23,055 cells but never priced into a book.  Simulate restatement
  directly (perturb the panel within the observed restatement envelope, N draws) and report the
  4a/4b flip rate against the truncation ladder's 3-in-192.  Max 2 params (envelope, draws).

WHAT THIS IS ACTUALLY ASKING
-----------------------------
  Every number the record publishes is read off ONE vintage of data/prices.csv.  That file moves
  in two ways: APPEND (new days arrive at the right edge -- idea 514's truncation ladder priced
  this, 3 verdict flips in 192) and RESTATE (the vendor silently rewrites cells already
  published -- idea 514 bounded the moves at max |d| 3.000e-04 but never asked what a book does
  when they happen).  If a 4a/4b verdict flips under a restatement the record cannot even see,
  then "passes 4b" is partly a statement about a data vintage, not about a strategy.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL 4, "no more than 2 tuned parameters")
-----------------------------------------------------------------------------
  TUNED (2)  : ENVELOPE (the restatement model and its width) and DRAWS (N).  All 5 envelopes
               are reported at all 3 draw counts -- 15 points, no exceptions.
  NOT TUNED  : cost 10 bps (PROTOCOL 2); cadence W (RULES v2) except BAND03_M whose cadence IS
               its definition; band 0.03 / 0.08; n in {5,10,20}; vol cap 0.60; gross {0.75, 1.00}
               (the live constant and full exposure); warm-up 260 rows; IS/OOS split
               2016-12-31 / 2017-01-01 (PROTOCOL 8).  Every book family is one the record has
               already committed (idea 670's arm list), restated, never chosen by outcome.

THE RESTATEMENT MODEL
----------------------
  A draw multiplies EVERY cell of the panel -- the SPY benchmark column included, because SPY is
  restated by the same vendor in the same file -- by (1 + u):

    IID   eps : u ~ Uniform(-eps, +eps), independent per (day, ticker).  This is the ADVERSARIAL
                shape at a given envelope: independent cell moves inject ~eps*sqrt(2/3)*sqrt(2)
                of noise into EVERY daily return, so it is the worst case for a return-based
                statistic and the right stress for a Sharpe/CAGR verdict.
    BLOCK eps : one u per (ticker, calendar month), held flat across that month's days.  This is
                the GENTLE shape: it moves price LEVELS but leaves all within-month returns
                untouched, and is closer to how a real restatement (a corrected split or
                dividend factor) actually lands.

  Reporting both shapes at the observed 3.000e-04 envelope is what makes the answer a RANGE and
  not an artefact of one arbitrary noise model.  Draws are seeded (seed = hash of envelope+draw),
  so every number below is reproducible; G4 asserts it.

PANELS (PROTOCOL 9 survivorship -- stated, not waved at)
---------------------------------------------------------
  U56  research/universe.json        B136  research/universe_broad.json
  Both are TODAY'S constituents, so every LEVEL below is biased upward.  This run's claim is a
  FLIP RATE -- how often a verdict changes when the same panel is restated -- which is a
  within-panel stability statistic and is biased far less than a level.  No level here is a
  tradeable estimate.

PRE-REGISTERED GATES (run and printed BEFORE any new number is read)
---------------------------------------------------------------------
  G1  fast_backtest == engine.backtest on returns, @10 bps, U56 BAND03        bar 1e-12
  G1b engine.backtest NaN rows all fall inside the discarded 260-row warm-up
  G2  eps = 0 reproduces the unperturbed book EXACTLY (the identity gate)     bar 0.0 exact
  G3  the realised perturbation envelope equals the requested eps             bar 1e-12
  G4  the same (envelope, draw) seed reproduces its panel bit-for-bit         bar 0.0 exact
  G4b seed_of is crc32-based and therefore stable ACROSS interpreters (Python str hash() is not)
  G4c different draws produce different panels (a constant seed would pass G4 trivially)
  G5  band_book(0.03, 0.75) == baseline.rules_v2_weights                      bar 0.0 exact
  G6  BLOCK leaves within-month returns untouched (only month-boundary days move)

VERDICT DISCIPLINE
------------------
  Both KEEP paths are evaluated on EVERY draw and all points are reported.  PROTOCOL 8 is run on
  every draw with a chooser that reads the IS half ONLY.  Nothing is promoted on a stability
  result.  A documented KILL / ANSWERED is the expected outcome.
"""
import sys
import warnings
import zlib
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

COST = 10.0                      # PROTOCOL 2
FREQ0 = "W"
BAND0, BAND1 = 0.03, 0.08
MAXVOL = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# PARAM 1 -- the envelope (shape, width).  3.000e-04 is idea 514's OBSERVED restatement bound.
ENVELOPES = [("IID", 1e-4), ("IID", 3e-4), ("IID", 1e-3), ("IID", 3e-3), ("BLOCK", 3e-4)]
# PARAM 2 -- draw counts, NESTED (the first 6 draws ARE the N=6 row), so this is a convergence
# report and not a second grid.
DRAW_COUNTS = [6, 12, 24]
NDRAW = max(DRAW_COUNTS)

IDEA514_TRUNC_FLIPS, IDEA514_TRUNC_N = 3, 192     # the comparand the queue names
IDEA514_OBSERVED_ENVELOPE = 3.000e-04

FAMILIES = ["BAND03", "BAND08", "BAND03_M", "CAND20", "CAND10", "CAND05", "EWELIG", "SPYBH"]
FAM_FREQ = {f: ("M" if f == "BAND03_M" else FREQ0) for f in FAMILIES}
GROSSES = [0.75, 1.00]

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==============================================================================================
# 1.  ENGINE
# ==============================================================================================
def fast_parts(prices, weights, freq=FREQ0):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * COST / 1e4, index=idx)


def M0(r):
    vol = r.std() * np.sqrt(252)
    return (r.mean() * 252) / vol if vol else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan,
                MaxDD=(eq / eq.cummax() - 1).min(), H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


# ==============================================================================================
# 2.  BOOKS (idea 670's committed families, restated)
# ==============================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ranked_book(px, sc, above, vol20, n, g, max_vol=MAXVOL):
    rank = sc.where(above & (vol20 < max_vol)).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(g / k, axis=0).fillna(0.0)


def elig_ew_book(px, above, vol20, g):
    sel = (above & (vol20 < MAXVOL) & px.notna()).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(g / k, axis=0).fillna(0.0)


def spy_book(px, g):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["SPY"] = float(g)
    return w.where(px.notna(), 0.0)


def prep(px):
    sc_n, above, vol20 = score(px, vol_scale=False)
    return sc_n, above, vol20


def fam_weights(px, pre, fam, g):
    sc_n, above, vol20 = pre
    if fam in ("BAND03", "BAND03_M"):
        return band_book(px, BAND0, g)
    if fam == "BAND08":
        return band_book(px, BAND1, g)
    if fam == "CAND20":
        return ranked_book(px, sc_n, above, vol20, 20, g)
    if fam == "CAND10":
        return ranked_book(px, sc_n, above, vol20, 10, g)
    if fam == "CAND05":
        return ranked_book(px, sc_n, above, vol20, 5, g)
    if fam == "EWELIG":
        return elig_ew_book(px, above, vol20, g)
    if fam == "SPYBH":
        return spy_book(px, g)
    raise KeyError(fam)


# ==============================================================================================
# 3.  THE RESTATEMENT MODEL
# ==============================================================================================
def seed_of(shape, eps, draw):
    """Deterministic ACROSS PROCESSES.  Python's str hash() is salted per interpreter
    (PYTHONHASHSEED), so it must not be used here -- crc32 of a canonical string is."""
    return zlib.crc32(f"{shape}|{float(eps):.12e}|{int(draw)}".encode()) % (2 ** 31)


def restate(px, shape, eps, draw):
    """px * (1+u).  eps == 0 returns px untouched (gate G2)."""
    if eps == 0.0:
        return px.copy()
    rng = np.random.default_rng(seed_of(shape, eps, draw))
    if shape == "IID":
        u = rng.uniform(-eps, eps, size=px.shape)
    elif shape == "BLOCK":
        key = px.index.to_period("M")
        codes, _ = pd.factorize(key, sort=True)
        ub = rng.uniform(-eps, eps, size=(codes.max() + 1, px.shape[1]))
        u = ub[codes]
    else:
        raise KeyError(shape)
    return px * (1.0 + u)


# ==============================================================================================
# 4.  VERDICTS
# ==============================================================================================
def verdicts(r, base, spy):
    m, mb, ms = M(r), M(base), M(spy)
    oos_s, oos_b = M0(r.loc[OOS_START:]), M0(spy.loc[OOS_START:])
    p4b = bool(m["H1"] > ms["H1"] and m["H2"] > ms["H2"] and oos_s > oos_b
               and abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]) and m["CAGR"] >= 0.70 * ms["CAGR"])
    p4a = bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])
    return p4a, p4b, m


def run_panel(px, books):
    """One (possibly restated) panel -> verdict + metrics for every book, plus the rule-8 pick."""
    pre = prep(px)
    start = px.index[WARM]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base = fast_parts(px, rules_v2_weights(px), FREQ0).loc[start:]
    out, cand = {}, []
    for fam, g in books:
        r = fast_parts(px, fam_weights(px, pre, fam, g), FAM_FREQ[fam]).loc[start:]
        p4a, p4b, m = verdicts(r, base, spy)
        out[(fam, g)] = dict(pass4a=p4a, pass4b=p4b, **m)
        if fam != "SPYBH":
            cand.append((M(r.loc[:IS_END])["Sharpe"], fam, g, r))
    is_sh, pf, pg, pr = max(cand, key=lambda t: t[0])
    mo, mbo, mso = M(pr.loc[OOS_START:]), M(base.loc[OOS_START:]), M(spy.loc[OOS_START:])
    pick = dict(pick=f"{pf}@g{pg:.2f}", is_Sharpe=is_sh,
                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                base_oos_CAGR=mbo["CAGR"], base_oos_Sharpe=mbo["Sharpe"], base_oos_MaxDD=mbo["MaxDD"],
                spy_oos_CAGR=mso["CAGR"], spy_oos_Sharpe=mso["Sharpe"], spy_oos_MaxDD=mso["MaxDD"])
    return out, pick


def main():
    P("=" * 98)
    P(f"IDEA 519  price-the-APPEND-vs-RESTATE-channels-separately  (cloud)  {pd.Timestamp.today().date()}")
    P("=" * 98)
    PX = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in PX.items():
        P(f"  panel {k:5s} {v.shape[0]} rows x {v.shape[1]} cols   {v.index[0].date()} .. {v.index[-1].date()}")
    BOOKS = [(f, g) for f, g in product(FAMILIES, GROSSES)]
    P(f"  books: {len(FAMILIES)} committed families x gross {GROSSES} = {len(BOOKS)} per panel")
    P(f"  envelopes (PARAM 1): {ENVELOPES}")
    P(f"  draws (PARAM 2, nested): {DRAW_COUNTS}")

    # ---------------- GATES ------------------------------------------------------------------
    P("\n" + "-" * 98)
    P("PRE-REGISTERED GATES")
    P("-" * 98)
    gates = []
    px = PX["U56"]
    w = rules_v2_weights(px)
    eng = backtest(px, w, cost_bps=COST, freq=FREQ0)["returns"]
    fin = np.isfinite(eng.values)
    d1 = float(np.abs(fast_parts(px, w, FREQ0).values[fin] - eng.values[fin]).max())
    gates.append(("G1 fast_backtest == engine.backtest (U56 BAND03 @10bps)", d1, 1e-12, d1 < 1e-12))
    nanp = int(np.flatnonzero(~fin).max()) if (~fin).any() else -1
    gates.append(("G1b engine NaNs all inside the discarded warm-up (row < 260)", nanp, WARM, nanp < WARM))
    # the panels carry NaN cells (names that start late), so every gate below uses nan-aware
    # reductions and asserts the NaN MASK is preserved rather than silently filled.
    z = restate(px, "IID", 0.0, 0)
    d2 = float(np.nanmax(np.abs(z.values - px.values)))
    mask_ok = bool((z.isna().values == px.isna().values).all())
    gates.append(("G2 eps=0 reproduces the panel EXACTLY (identity)", d2, 0.0, d2 == 0.0 and mask_ok))
    pe = restate(px, "IID", 3e-4, 0)
    real = float(np.nanmax(np.abs(pe.values / px.values - 1.0)))
    gates.append(("G3 realised IID envelope == requested 3.000e-04", real, 3e-4, real <= 3e-4 + 1e-12))
    d4 = float(np.nanmax(np.abs(restate(px, "IID", 3e-4, 0).values - pe.values)))
    gates.append(("G4 same (envelope, draw) seed is bit-for-bit reproducible", d4, 0.0, d4 == 0.0))
    # G4b pins the seed itself: crc32 is stable across interpreters, Python's str hash() is not.
    s4b = seed_of("IID", 3e-4, 0)
    gates.append(("G4b seed_of('IID',3e-4,0) is the pinned cross-process value", s4b, 1026344283,
                  s4b == 1026344283))
    # G4c: different draws must actually differ (a constant seed would pass G4 trivially).
    d4c = float(np.nanmax(np.abs(restate(px, "IID", 3e-4, 1).values - pe.values)))
    gates.append(("G4c draw 1 differs from draw 0 (seeds are not constant)", d4c, 0.0, d4c > 0.0))
    d5 = float(np.abs(band_book(px, BAND0, 0.75).values - w.values).max())
    gates.append(("G5 band_book(0.03,0.75) == rules_v2_weights", d5, 0.0, d5 == 0.0))
    pb = restate(px, "BLOCK", 3e-4, 0)
    rr0, rr1 = px.pct_change().values[1:], pb.pct_change().values[1:]
    same_month = (px.index.to_period("M")[1:] == px.index.to_period("M")[:-1])
    d6 = float(np.nanmax(np.abs(rr1[same_month] - rr0[same_month])))
    gates.append(("G6 BLOCK leaves within-month returns untouched", d6, 1e-15, d6 <= 1e-15))
    for nm, got, bar, ok in gates:
        P(f"  [{'PASS' if ok else 'FAIL'}] {nm:60s} got {got:.6g}  bar {bar:g}")
    if not all(g[3] for g in gates):
        P("\n  *** A GATE FAILED -- results below are NOT to be read. ***")
        return

    # ---------------- BASELINE (unperturbed) VERDICTS ----------------------------------------
    P("\n" + "-" * 98)
    P("UNPERTURBED REFERENCE (the vintage the record actually published on)")
    P("-" * 98)
    REF, REFPICK = {}, {}
    for pname, p in PX.items():
        REF[pname], REFPICK[pname] = run_panel(p, BOOKS)
        n4a = sum(v["pass4a"] for v in REF[pname].values())
        n4b = sum(v["pass4b"] for v in REF[pname].values())
        P(f"  {pname}: 4a {n4a}/{len(BOOKS)}   4b {n4b}/{len(BOOKS)}   rule-8 pick {REFPICK[pname]['pick']}")

    # ---------------- THE DRAWS ---------------------------------------------------------------
    P("\n" + "-" * 98)
    P(f"RESTATEMENT DRAWS: 2 panels x {len(ENVELOPES)} envelopes x {NDRAW} draws x {len(BOOKS)} books "
      f"= {2*len(ENVELOPES)*NDRAW*len(BOOKS)} book-runs")
    P("-" * 98)
    rows, picks = [], []
    for pname, p in PX.items():
        for shape, eps in ENVELOPES:
            for d in range(NDRAW):
                res, pk = run_panel(restate(p, shape, eps, d), BOOKS)
                for (fam, g), v in res.items():
                    ref = REF[pname][(fam, g)]
                    rows.append(dict(panel=pname, shape=shape, eps=eps, draw=d, family=fam, gross=g,
                                     pass4a=v["pass4a"], pass4b=v["pass4b"],
                                     ref4a=ref["pass4a"], ref4b=ref["pass4b"],
                                     flip4a=v["pass4a"] != ref["pass4a"],
                                     flip4b=v["pass4b"] != ref["pass4b"],
                                     dSharpe=v["Sharpe"] - ref["Sharpe"], dCAGR=v["CAGR"] - ref["CAGR"],
                                     dMaxDD=v["MaxDD"] - ref["MaxDD"],
                                     Sharpe=v["Sharpe"], CAGR=v["CAGR"], MaxDD=v["MaxDD"]))
                picks.append(dict(panel=pname, shape=shape, eps=eps, draw=d,
                                  pick_flip=pk["pick"] != REFPICK[pname]["pick"],
                                  ref_pick=REFPICK[pname]["pick"], **pk))
            P(f"  {pname} {shape} eps={eps:.0e}: {NDRAW} draws done")
    G = pd.DataFrame(rows)
    K = pd.DataFrame(picks)
    dump(G, "draws")
    dump(K, "picks")

    # ---------------- RESULT 1: flip rates, per envelope, per draw count ----------------------
    P("\n" + "=" * 98)
    P("RESULT 1 -- 4a / 4b VERDICT FLIP RATE under restatement, vs idea 514's APPEND channel")
    P(f"            (comparand: truncation ladder = {IDEA514_TRUNC_FLIPS} flips in {IDEA514_TRUNC_N} "
      f"= {IDEA514_TRUNC_FLIPS/IDEA514_TRUNC_N*100:.2f}%)")
    P("=" * 98)
    fr = []
    for (shape, eps), N in product(ENVELOPES, DRAW_COUNTS):
        sub = G[(G["shape"] == shape) & (G.eps == eps) & (G.draw < N)]
        fr.append(dict(shape=shape, eps=eps, draws=N, n=len(sub),
                       flip4a=int(sub.flip4a.sum()), rate4a=float(sub.flip4a.mean()),
                       flip4b=int(sub.flip4b.sum()), rate4b=float(sub.flip4b.mean()),
                       max_abs_dSharpe=float(sub.dSharpe.abs().max()),
                       max_abs_dCAGR=float(sub.dCAGR.abs().max()),
                       max_abs_dMaxDD=float(sub.dMaxDD.abs().max())))
    FR = pd.DataFrame(fr)
    dump(FR, "fliprates")
    P(f"  {'envelope':>16s} {'draws':>6s} {'n':>6s} | {'4a flips':>16s} {'4b flips':>16s} | "
      f"{'max|dSharpe|':>12s} {'max|dCAGR|':>11s} {'max|dMaxDD|':>12s}")
    P("  " + "-" * 108)
    for _, r in FR.iterrows():
        P(f"  {r['shape']+' '+f'{r.eps:.0e}':>16s} {int(r.draws):6d} {int(r.n):6d} | "
          f"{int(r.flip4a):5d} ({r.rate4a*100:5.2f}%) {int(r.flip4b):5d} ({r.rate4b*100:5.2f}%) | "
          f"{r.max_abs_dSharpe:12.4f} {r.max_abs_dCAGR:10.3%} {r.max_abs_dMaxDD:11.3%}")

    # ---------------- RESULT 2: which books flip ---------------------------------------------
    P("\n" + "=" * 98)
    P("RESULT 2 -- WHICH BOOKS FLIP (at the OBSERVED 3.000e-04 envelope, both shapes, 24 draws)")
    P("=" * 98)
    obs = G[(G.eps == IDEA514_OBSERVED_ENVELOPE)]
    for shape in ("IID", "BLOCK"):
        s = obs[obs["shape"] == shape]
        P(f"\n  shape {shape}:  4a flips {int(s.flip4a.sum())}/{len(s)} ({s.flip4a.mean()*100:.2f}%)   "
          f"4b flips {int(s.flip4b.sum())}/{len(s)} ({s.flip4b.mean()*100:.2f}%)")
        fl = s[s.flip4a | s.flip4b]
        if len(fl) == 0:
            P("    no book flipped either verdict on any draw.")
            continue
        g2 = fl.groupby(["panel", "family", "gross"]).agg(
            n4a=("flip4a", "sum"), n4b=("flip4b", "sum"), ref4b=("ref4b", "first")).reset_index()
        for _, r in g2.sort_values(["n4b", "n4a"], ascending=False).iterrows():
            P(f"    {r['panel']:5s} {r['family']:9s} g{r['gross']:.2f}  4a flips {int(r.n4a):2d}/24  "
              f"4b flips {int(r.n4b):2d}/24  (unperturbed 4b = {r.ref4b})")

    # ---------------- RESULT 3: PROTOCOL 8 walk-forward under restatement ---------------------
    P("\n" + "=" * 98)
    P("RESULT 3 -- PROTOCOL 8: the rule-8 PICK is chosen on 2008-2016 ONLY, on each RESTATED panel,")
    P("            and evaluated on 2017-2026 untouched.  Does restatement move the pick?")
    P("=" * 98)
    pk = K.groupby(["panel", "shape", "eps"]).agg(
        pick_flips=("pick_flip", "sum"), n=("pick_flip", "size"),
        oos_CAGR_mean=("oos_CAGR", "mean"), oos_CAGR_min=("oos_CAGR", "min"), oos_CAGR_max=("oos_CAGR", "max"),
        oos_Sharpe_mean=("oos_Sharpe", "mean"), oos_Sharpe_min=("oos_Sharpe", "min"),
        oos_Sharpe_max=("oos_Sharpe", "max"), oos_MaxDD_mean=("oos_MaxDD", "mean"),
        oos_MaxDD_min=("oos_MaxDD", "min")).reset_index()
    dump(pk, "pickstability")
    for pname in PX:
        ref = REFPICK[pname]
        P(f"\n  {pname}  unperturbed rule-8 pick = {ref['pick']}")
        P(f"    {'':26s} {'CAGR':>9s} {'Sharpe':>9s} {'MaxDD':>9s}")
        P(f"    {'PICK (OOS 2017-26)':26s} {ref['oos_CAGR']:8.2%} {ref['oos_Sharpe']:9.3f} {ref['oos_MaxDD']:8.2%}")
        P(f"    {'RULES v2 baseline':26s} {ref['base_oos_CAGR']:8.2%} {ref['base_oos_Sharpe']:9.3f} {ref['base_oos_MaxDD']:8.2%}")
        P(f"    {'SPY':26s} {ref['spy_oos_CAGR']:8.2%} {ref['spy_oos_Sharpe']:9.3f} {ref['spy_oos_MaxDD']:8.2%}")
        P(f"    {'envelope':>16s} {'pickflips':>10s} | {'OOS CAGR [min,max]':>26s} {'OOS Sharpe [min,max]':>26s}")
        for _, r in pk[pk.panel == pname].iterrows():
            P(f"    {r['shape']+' '+f'{r.eps:.0e}':>16s} {int(r.pick_flips):4d}/{int(r.n):<5d} | "
              f"  [{r.oos_CAGR_min:7.2%}, {r.oos_CAGR_max:7.2%}]        "
              f"[{r.oos_Sharpe_min:6.3f}, {r.oos_Sharpe_max:6.3f}]")

    # ---------------- RESULT 4: the answer ----------------------------------------------------
    P("\n" + "=" * 98)
    P("RESULT 4 -- APPEND vs RESTATE, priced side by side")
    P("=" * 98)
    o_iid = G[(G.eps == IDEA514_OBSERVED_ENVELOPE) & (G["shape"] == "IID")]
    o_blk = G[(G.eps == IDEA514_OBSERVED_ENVELOPE) & (G["shape"] == "BLOCK")]
    ap = IDEA514_TRUNC_FLIPS / IDEA514_TRUNC_N
    P(f"  APPEND  (idea 514 truncation ladder)          {IDEA514_TRUNC_FLIPS:4d} / {IDEA514_TRUNC_N:4d}  = {ap*100:5.2f}%")
    P(f"  RESTATE (this run, IID   @3.000e-04, 24 draws) {int(o_iid.flip4b.sum()):4d} / {len(o_iid):4d}  = {o_iid.flip4b.mean()*100:5.2f}%   (4b)")
    P(f"  RESTATE (this run, BLOCK @3.000e-04, 24 draws) {int(o_blk.flip4b.sum()):4d} / {len(o_blk):4d}  = {o_blk.flip4b.mean()*100:5.2f}%   (4b)")
    P(f"  RESTATE (this run, IID   @3.000e-04, 24 draws) {int(o_iid.flip4a.sum()):4d} / {len(o_iid):4d}  = {o_iid.flip4a.mean()*100:5.2f}%   (4a)")
    P(f"  RESTATE (this run, BLOCK @3.000e-04, 24 draws) {int(o_blk.flip4a.sum()):4d} / {len(o_blk):4d}  = {o_blk.flip4a.mean()*100:5.2f}%   (4a)")
    P("")
    P("  Envelope needed before 4b starts flipping (IID shape, 24 draws, both panels pooled):")
    for shape, eps in ENVELOPES:
        if shape != "IID":
            continue
        s = G[(G["shape"] == "IID") & (G.eps == eps)]
        P(f"    eps {eps:.0e}:  4b flips {int(s.flip4b.sum()):3d}/{len(s)} ({s.flip4b.mean()*100:5.2f}%)   "
          f"4a flips {int(s.flip4a.sum()):3d}/{len(s)} ({s.flip4a.mean()*100:5.2f}%)   "
          f"max|dSharpe| {s.dSharpe.abs().max():.4f}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    P(f"\n  wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

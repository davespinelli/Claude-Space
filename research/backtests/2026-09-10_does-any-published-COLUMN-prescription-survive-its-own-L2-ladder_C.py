#!/usr/bin/env python3
"""Idea 617 — does any published COLUMN prescription survive its own L2 ladder?  (lane C, 2026-09-10)

QUEUE 617: "idea 613 found drag beats turnover as a width predictor at L4/L6 but LOSES at
L2 = [10, 25] bps, the only rung pair the record routinely publishes, so the prescription is
right in principle and wrong where it would be used.  Re-run the record's other proposed columns
against the rung pair they would actually be applied on and report which survive.  Max 2 params
(column, rung ladder)."

WHAT IS ACTUALLY BEING TESTED
  H0  (premise)  L2 = [10, 25] really is the record's published rung pair.  Falsifiable by a
                 census of the rung multisets actually written into committed CSVs: if the modal
                 published ladder is L1 or L4, 613's L2 finding is about a ladder nobody uses and
                 the whole idea is mis-aimed.
  H1  (the ask)  For each of the record's OTHER column prescriptions (239 EWall control, 471
                 matched-gross twin, 583 gross on CAGR claims, 604 block placebo, 607 crossing
                 cost, with 613 DRAG as the published control), does the PRESCRIBED column beat
                 the INCUMBENT column it replaces, on ladder L, at predicting what a reader wants
                 the column for?  SURVIVES on L iff |rho(target, prescribed)| > |rho(target,
                 incumbent)| on L's pooled rows.
  H2  (target)   The uniform target is the arm's REALISED OUT-OF-SAMPLE Sharpe (2017-2026) at the
                 same rung, with every column computed IN SAMPLE (2009-2016).  That is the
                 reader's actual decision problem and it is not circular: no column is a function
                 of the OOS window.  A second target (OOS d-Sharpe vs the full-gross control) is
                 reported beside it and never chosen between.
  H3  (613 form) 613's own test replicated on a NEW dial: the 4b window width over the BAND grid,
                 with drag vs turnover as the two orders.  If 613's L2 reversal is a fact about
                 ladders it should reappear on a dial 613 never ran; if it is a fact about the
                 sleeve dial it should not.
  H4  (vacuity)  A prescription can fail at L2 for a second reason 613 did not have to face:
                 being UNDEFINED there.  607's crossing cost needs a slope, so it needs >= 2
                 rungs; at L1 it does not exist at all.  Counted, not asserted.

AXES AND WHAT IS SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
  The queue names the two tuned parameters and both are swept in full with every point reported:
    P1 column      : 239 EWALL / 471 TWIN / 583 GROSS-on-CAGR / 604 PLACEBO / 607 CSTAR, with
                     613 DRAG as the already-published control.  Six, all reported.
    P2 rung ladder : L1 = [10], L2 = [10, 25], L4 = [0, 10, 25, 50],
                     L6 = [0, 5, 10, 15, 25, 50] bps.  Four, all reported.
  The fresh leg's dials are BAND (6 points, 0.00-0.08) and GROSS (3 points, 0.50/0.75/1.00),
  fully enumerated, reported at every point, and NEVER chosen.  Panels, books, forms and rungs
  are reported axes.  The only selection anywhere is PROTOCOL rule 8, where (band, gross) is
  picked on 2009-2016 alone by eight pre-registered column selectors and 2017-2026 is read once.

GATES (run before any new number is read)
  G1 the vectorised runner vs `engine.backtest` on the evaluated slice, returns AND turnover.
  G2 the rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
     This licenses reading six rungs off one simulation, and it is also why the question is well
     posed: turnover reaches a return series ONLY through cost.
  G3 the TWIN matches the ARM's realised mean gross (the thing 471/583 prescribe).
  G4 idea 616's committed `.grid.csv` reproduced row for row on the shared arm space.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are current constituents.  SMALL439 additionally
    drops the 44 tickers with max_1d_move >= 1.0 from data/small_meta.csv before anything runs.
  * The census reads COMMITTED CSVs only; a rung ladder quoted in prose is invisible to it.
  * UNIVERSE CONVENTION: SPY is the benchmark and is dropped from the investable set on EVERY
    panel here (idea 613's convention).  Idea 616 kept SPY investable on u56/broad, which is why
    G4a gates only on the small panel and G4b re-derives the u56 gap from the convention alone.
  * MaxDD is one number off one path (idea 321); the 4b DD cap turns on exactly that number.
  * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
  * Idea 612: the correlation population is stated and identical across all six columns
    (TOP20 arms only, because 239's EWall control is degenerate on an EWALL arm).  The EWALL
    arms are reported separately and never pooled in.
  * c*(L) is constant within a cell, so on the POOLED reading its x-column repeats within a
    ladder; the CELL reading (both are reported) does not have that property.
  * The block placebo is one seed (617); it is a comparand, not a distribution.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .rungcensus.csv, .grid.csv,
.columns.csv, .survive.csv, .width.csv, .wf.csv next to itself.
"""
from __future__ import annotations

import csv
import glob
import importlib.util
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-any-published-COLUMN-prescription-survive-its-own-L2-ladder_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I616_GRID = OUT / "2026-09-10_is-the-RE-PRICEABLE-set-empty-on-every-published-COLUMN-prescription_C.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")                       # idea 94's harness: composite / vol20
FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60                     # 4b CAGR floor / DD cap fractions of SPY

PANELS = ["u56", "broad", "small"]
BOOKS = ["TOP20", "EWALL"]                  # ranked book / the record's un-ranked control (239)
BANDS = [0.00, 0.01, 0.02, 0.04, 0.06, 0.08]        # the clause dial, fully enumerated
GROSSES = [0.50, 0.75, 1.00]                        # the exposure dial, fully enumerated
NTOP = 20
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]
LADDERS = {"L1": [10.0], "L2": [10.0, 25.0], "L4": [0.0, 10.0, 25.0, 50.0], "L6": list(RUNGS)}
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
BLOCK = 21                                  # placebo block length in trading days
SEED = 617
WF_RUNG = 10.0                              # PROTOCOL's own rung, for the rule-8 evaluation

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# vectorised runner (segment-exact reproduction of engine.backtest at zero cost) — idea 613
# =====================================================================================
def fast_bt(px: pd.DataFrame, W: pd.DataFrame, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    idx = px.index
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# =====================================================================================
# books, gates, controls  (idea 616's forms, verbatim)
# =====================================================================================
def book_weights(px, book, investable, gross):
    sub = px[investable]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    else:
        rank = H.composite(sub).rank(axis=1, ascending=False)
        W = (rank <= NTOP).astype(float) * (gross / NTOP)
    return W.reindex(columns=px.columns).fillna(0.0)


def band_gate(px, band):
    """RULES v2 clause 2 verbatim: 200d MA with hysteresis.  band=0.0 is the plain MA gate.
    Gated-out weight goes to CASH — de-gross, never re-spread."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def block_shuffle(mask: pd.DataFrame, seed=SEED, block=BLOCK):
    """BLOCK placebo (idea 602/604's form): permute contiguous `block`-day slabs of the gate in
    TIME with a fixed seed.  Preserves the gate's on-share and its whole cross-section; destroys
    only WHEN it fires."""
    n = len(mask)
    starts = list(range(0, n, block))
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(starts))
    rows = [np.arange(s, min(s + block, n)) for s in (starts[k] for k in order)]
    idx = np.concatenate(rows)[:n]
    return pd.DataFrame(mask.values[idx], index=mask.index, columns=mask.columns)


# =====================================================================================
# metric helpers
# =====================================================================================
def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or len(set(a[ok])) < 2 or len(set(b[ok])) < 2:
        return np.nan
    return float(np.corrcoef(pd.Series(a[ok]).rank(), pd.Series(b[ok]).rank())[0, 1])


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    h = len(spy) // 2
    m = metrics(spy)
    return dict(s1=metrics(spy.iloc[:h])["Sharpe"], s2=metrics(spy.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def margins(r, b):
    h = len(r) // 2
    m = metrics(r)
    return dict(H1=metrics(r.iloc[:h])["Sharpe"] - b["s1"],
                H2=metrics(r.iloc[h:])["Sharpe"] - b["s2"],
                OOS=metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"],
                DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * b["scagr"])


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def contiguous_width(flags):
    """Longest contiguous run of True over an ordered dial grid, in GRID POINTS."""
    best = cur = 0
    for ok in flags:
        cur = cur + 1 if ok else 0
        best = max(best, cur)
    return best


def crossing_cost(costs, deltas):
    """c* = the rung where a linear fit of delta(c) crosses zero.  Needs >= 2 distinct rungs;
    returns NaN when the ladder cannot support a slope (H4), +inf when the fit never crosses
    downward (the arm does not lose as cost rises)."""
    c = np.asarray(costs, float)
    d = np.asarray(deltas, float)
    ok = np.isfinite(c) & np.isfinite(d)
    c, d = c[ok], d[ok]
    if len(set(c.tolist())) < 2:
        return np.nan                       # UNDEFINED on this ladder
    b, a = np.polyfit(c, d, 1)              # d = a + b*c
    if b >= 0:
        return np.inf
    x = -a / b
    return float(x)


# =====================================================================================
# panels
# =====================================================================================
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def get_panels():
    P = {}
    P["u56"] = load_universe()
    P["broad"] = load_universe(broad=True)
    sp, ndrop = small_panel()
    P["small"] = sp
    say(f"panels: u56 {P['u56'].shape}, broad {P['broad'].shape}, "
        f"small {P['small'].shape} (dropped {ndrop} max_1d_move>=1.0 names)")
    return P


# =====================================================================================
# LEG 0 — GATES
# =====================================================================================
def gates(panels):
    say("\n" + "=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    for name, px in panels.items():
        inv = [c for c in px.columns if c != "SPY"]
        W = book_weights(px, "TOP20", inv, 0.75).where(band_gate(px, 0.02), 0.0)
        start = px.index[260]
        r_fast, t_fast = fast_bt(px, W)
        eng = backtest(px, W, cost_bps=0.0, freq=FREQ)
        dr = float((r_fast.loc[start:] - eng["returns"].loc[start:]).abs().max())
        dt = float((t_fast.loc[start:] - eng["turnover"].loc[start:]).abs().max())
        eng25 = backtest(px, W, cost_bps=25.0, freq=FREQ)
        ident = (r_fast - t_fast * 25.0 / 1e4).loc[start:]
        d2 = float((ident - eng25["returns"].loc[start:]).abs().max())
        say(f"  G1 {name:6s} max|dr| {dr:.3e}   max|dturnover| {dt:.3e}")
        say(f"  G2 {name:6s} rung identity vs engine(25bps) max|dr| {d2:.3e}")
        ok &= (dr < 1e-12 and dt < 1e-12 and d2 < 1e-12)
    say(f"  G1/G2 verdict: {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# LEG A — CENSUS: what rung ladder does the record actually publish?  (H0)
# =====================================================================================
RUNG_COL = re.compile(r"(?:^|_)(cost|cost_bps|bps|rung|c_bps|costbps)(?:$|_)", re.I)
NOT_A_RUNG = re.compile(r"(cost_of|crossing|c_star|cstar|breakeven|drag|spearman|rho|auc|"
                        r"share|rate|frac|pass|flag|delta|slope|beat)", re.I)


def rung_census():
    say("\n" + "=" * 100)
    say("LEG A — H0.  Which rung ladder does the record ACTUALLY publish?")
    say("=" * 100)
    files = sorted(glob.glob(str(ROOT / "research" / "**" / "*.csv"), recursive=True)) + \
        sorted(glob.glob(str(ROOT / "research" / "**" / "*.csv.gz"), recursive=True))
    files = [f for f in files if STEM not in f]
    rows = []
    for f in files:
        try:
            d = pd.read_csv(f, nrows=4000)
        except Exception:
            continue
        cols = [c for c in d.columns if RUNG_COL.search(str(c)) and not NOT_A_RUNG.search(str(c))]
        for c in cols:
            v = pd.to_numeric(d[c], errors="coerce").dropna()
            v = v[(v >= 0) & (v <= 200)]                 # a cost rung in bps, physically
            if len(v) == 0:
                continue
            u = sorted(set(round(float(x), 3) for x in v.unique()))
            if len(u) > 12:
                continue                                  # a continuous sweep, not a rung ladder
            rows.append(dict(file=os.path.relpath(f, ROOT), col=str(c), n_rungs=len(u),
                             ladder="|".join(f"{x:g}" for x in u)))
    C = pd.DataFrame(rows)
    if C.empty:
        say("  no rung columns found — H0 cannot be read")
        return C
    say(f"  {len(files)} committed CSVs scanned; {C['file'].nunique()} carry a rung column "
        f"({len(C)} columns).")
    byn = C.groupby("n_rungs")["file"].nunique().sort_index()
    say("\n  files by NUMBER of distinct rungs published:")
    for k, v in byn.items():
        say(f"    {k:2d} rungs : {v:5d} files  ({v / C['file'].nunique():6.1%})")
    top = C.drop_duplicates(["file", "ladder"]).groupby("ladder")["file"].nunique().sort_values(ascending=False)
    say("\n  the 12 most-published rung LADDERS:")
    for lad, v in top.head(12).items():
        tag = ""
        for nm, L in LADDERS.items():
            if lad == "|".join(f"{x:g}" for x in L):
                tag = f"   <== {nm}"
        say(f"    {v:5d} files : [{lad}]{tag}")
    # how many files publish >=2 rungs including both 10 and 25
    has = C.drop_duplicates(["file", "ladder"])
    l2 = has[has["ladder"].apply(lambda s: {"10", "25"} <= set(s.split("|")))]["file"].nunique()
    only10 = has[has["ladder"] == "10"]["file"].nunique()
    say(f"\n  files whose ladder CONTAINS both 10 and 25 bps : {l2}")
    say(f"  files whose ladder is exactly [10]              : {only10}")
    return C


# =====================================================================================
# LEG B — the fresh grid
# =====================================================================================
def build_grid(panels):
    say("\n" + "=" * 100)
    say("LEG B — the fresh grid (3 panels x 2 books x 3 grosses x 6 bands x 4 forms)")
    say("=" * 100)
    rows = []
    t0 = time.time()
    nsim = 0
    for pname, px in panels.items():
        inv = [c for c in px.columns if c != "SPY"]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        B = bars_of(spy)
        v2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        v2r, v2t = v2["returns"].fillna(0.0), v2["turnover"]
        gates_cache = {b: band_gate(px, b) for b in BANDS}
        shuf_cache = {b: block_shuffle(gates_cache[b]) for b in BANDS}
        for book in BOOKS:
            for g in GROSSES:
                base = book_weights(px, book, inv, g)
                bg_mean = float(base.sum(axis=1).loc[start:].mean())
                for band in BANDS:
                    W_arm = base.where(gates_cache[band], 0.0)
                    W_plc = base.where(shuf_cache[band], 0.0)
                    ag = float(W_arm.sum(axis=1).loc[start:].mean())
                    scale = ag / bg_mean if bg_mean > 0 else 0.0
                    forms = {"ARM": W_arm, "CTRL": base, "TWIN": base * scale, "PLACEBO": W_plc}
                    for form, W in forms.items():
                        r0, tt = fast_bt(px, W)
                        nsim += 1
                        r0, tt = r0.loc[start:], tt.loc[start:]
                        mg = float(W.sum(axis=1).loc[start:].mean())
                        on = float((W.sum(axis=1).loc[start:] > 1e-12).mean())
                        to_ann = float(tt.sum() / (len(tt) / 252.0))
                        for c in RUNGS:
                            r = r0 - tt * c / 1e4
                            vb = v2r - v2t * c / 1e4
                            m = metrics(r)
                            mm = margins(r, B)
                            ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
                            mis, mos = metrics(ris), metrics(ros)
                            rows.append(dict(
                                panel=pname, book=book, gross=g, band=band, form=form, cost=c,
                                mean_gross=mg, on_share=on, arm_to=to_ann,
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                H1=halves(r)[0], H2=halves(r)[1],
                                OOS_Sharpe=mos["Sharpe"], OOS_CAGR=mos["CAGR"],
                                OOS_MaxDD=mos["MaxDD"],
                                IS_Sharpe=mis["Sharpe"], IS_CAGR=mis["CAGR"],
                                IS_MaxDD=mis["MaxDD"], IS_to=float(tt.loc[:IS_END].sum() /
                                                                   (len(tt.loc[:IS_END]) / 252.0)),
                                m_H1=mm["H1"], m_H2=mm["H2"], m_OOS=mm["OOS"], m_DD=mm["DD"],
                                m_CAGR=mm["CAGR"], m_min=min(mm[k] for k in BARS5),
                                pass4b=bool(min(mm[k] for k in BARS5) > 0),
                                pass4a=pass4a(r, vb),
                                SPY_OOS_Sharpe=B["soos"]))
        say(f"  {pname}: {nsim} sims cumulative, {time.time() - t0:.0f}s")
    G = pd.DataFrame(rows)
    say(f"  grid: {len(G)} arm-rows from {nsim} simulations in {time.time() - t0:.0f}s")
    return G


def gate_twin(G):
    """G3 — the TWIN matches the ARM's realised mean gross."""
    k = ["panel", "book", "gross", "band", "cost"]
    a = G[G.form == "ARM"].set_index(k)["mean_gross"]
    t = G[G.form == "TWIN"].set_index(k)["mean_gross"]
    d = float((a - t).abs().max())
    say(f"  G3 TWIN vs ARM realised mean gross: max|d| {d:.3e}  "
        f"{'PASS' if d < 1e-10 else 'FAIL'}")
    return d < 1e-10


def gate_616(G):
    """G4 — reproduce idea 616's committed grid on the shared rows.

    The PLACEBO form is EXCLUDED from the gate by construction: 616's block shuffle carries
    seed 616 and this run carries seed 617, so the two placebos are different draws of the same
    operator and are not expected to agree.  Its delta is printed, not gated.
    """
    if not I616_GRID.exists():
        say("  G4 SKIP — idea 616 grid not committed")
        return True
    P = pd.read_csv(I616_GRID)
    k = ["panel", "book", "gross", "band", "form", "cost"]
    m = G.merge(P, on=k, suffixes=("", "_616"))
    if m.empty:
        say("  G4 SKIP — no shared rows")
        return True
    worst = 0.0
    for (pn, form), d in m.groupby(["panel", "form"]):
        ds = float((d["Sharpe"] - d["Sharpe_616"]).abs().max())
        dc = float((d["CAGR"] - d["CAGR_616"]).abs().max())
        dg = float((d["mean_gross"] - d["mean_gross_616"]).abs().max())
        tag = ""
        gated = (pn == "small" and form != "PLACEBO")
        if form == "PLACEBO":
            tag = "  (seed 617 vs 616 — NOT gated)"
        elif pn != "small":
            tag = "  (SPY-in-universe convention — NOT gated, see G4b)"
        say(f"  G4a {pn:6s} {form:8s} {len(d):4d} rows: max|dSharpe| {ds:.3e}, "
            f"max|dCAGR| {dc:.3e}, max|dgross| {dg:.3e}{tag}")
        if gated:
            worst = max(worst, ds, dc, dg)
    say(f"  G4a verdict (small panel, ARM/CTRL/TWIN — the slice where the two runs' universe "
        f"conventions coincide): max {worst:.3e}  {'PASS' if worst < 1e-12 else 'FAIL'}")
    return worst < 1e-12


def gate_616b(panels):
    """G4b — the u56/broad delta in G4a is the UNIVERSE CONVENTION and nothing else.

    Idea 616 keeps SPY in the investable set on u56 and broad (it drops it only on the small
    panel); this run drops the benchmark from every panel, which is idea 613's convention and
    the stricter one.  Rebuilding one u56 cell under 616's convention must reproduce 616 EXACTLY.
    """
    if not I616_GRID.exists():
        say("  G4b SKIP — idea 616 grid not committed")
        return True
    P = pd.read_csv(I616_GRID)
    px = panels["u56"]
    inv616 = list(px.columns)                    # 616's convention: SPY stays investable
    start = px.index[260]
    worst = 0.0
    for book, g, band in (("TOP20", 0.75, 0.02), ("EWALL", 1.00, 0.06)):
        base = M_book(px, book, inv616, g)
        W = base.where(band_gate(px[inv616], band).reindex(columns=px.columns).fillna(False), 0.0)
        r0, tt = fast_bt(px, W)
        r0, tt = r0.loc[start:], tt.loc[start:]
        for c in (0.0, 10.0, 25.0):
            r = r0 - tt * c / 1e4
            row = P[(P.panel == "u56") & (P.book == book) & (P.gross == g) & (P.band == band) &
                    (P.form == "ARM") & (P.cost == c)]
            if row.empty:
                continue
            worst = max(worst, abs(metrics(r)["Sharpe"] - float(row["Sharpe"].iloc[0])),
                        abs(float(W.loc[start:].sum(axis=1).mean()) - float(row["mean_gross"].iloc[0])))
    say(f"  G4b u56 rebuilt under 616's OWN universe convention: max|d| {worst:.3e}  "
        f"{'PASS' if worst < 1e-12 else 'FAIL'}  "
        f"(so the G4a u56/broad gap is the convention, not the machinery)")
    return worst < 1e-12


M_book = book_weights                            # alias used by G4b


# =====================================================================================
# LEG C — the columns, per (cell, rung)
# =====================================================================================
def build_columns(G):
    """One row per (panel, book, gross, band, cost).  Every column IN SAMPLE; every target OOS."""
    say("\n" + "=" * 100)
    say("LEG C — the six columns (all IN SAMPLE) and the two targets (both OUT OF SAMPLE)")
    say("=" * 100)
    k = ["panel", "book", "gross", "band", "cost"]
    idx = ["panel", "book", "gross", "band", "cost"]
    piv = {f: G[G.form == f].set_index(idx) for f in ["ARM", "CTRL", "TWIN", "PLACEBO"]}
    # the un-ranked EWall control: same panel, same gross, same cost, book=EWALL, form=CTRL
    # the CTRL form does not depend on the band, so it is written once per (panel, gross, cost)
    ew = (G[(G.form == "CTRL") & (G.book == "EWALL")]
          .drop_duplicates(["panel", "gross", "cost"])
          .set_index(["panel", "gross", "cost"]).sort_index())
    rows = []
    for key, a in piv["ARM"].iterrows():
        pname, book, g, band, c = key
        ctrl, twin, plc = piv["CTRL"].loc[key], piv["TWIN"].loc[key], piv["PLACEBO"].loc[key]
        e = ew.loc[(pname, g, c)]
        rows.append(dict(
            panel=pname, book=book, gross=g, band=band, cost=c,
            # ---- columns (IN SAMPLE) ----
            X0_dS_ctrl=a["IS_Sharpe"] - ctrl["IS_Sharpe"],       # the published incumbent
            X0_dC_ctrl=a["IS_CAGR"] - ctrl["IS_CAGR"],           # the published incumbent (CAGR)
            X_TWIN=a["IS_Sharpe"] - twin["IS_Sharpe"],           # 471
            X_GROSSC=a["IS_CAGR"] - twin["IS_CAGR"],             # 583 (CAGR family)
            X_PLAC=a["IS_Sharpe"] - plc["IS_Sharpe"],            # 604
            X_EWALL=a["IS_Sharpe"] - e["IS_Sharpe"],             # 239
            X_TO=a["IS_to"],                                     # 613 incumbent
            X_DRAG=a["IS_to"] * c / 1e4,                         # 613 proposal
            dS_twin_c=a["IS_Sharpe"] - twin["IS_Sharpe"],        # for 607's slope fit
            # ---- targets (OUT OF SAMPLE, never used to build a column) ----
            T_OOS=a["OOS_Sharpe"],
            T_OOS_dctrl=a["OOS_Sharpe"] - ctrl["OOS_Sharpe"],
            # ---- carried ----
            pass4b=a["pass4b"], pass4a=a["pass4a"], mean_gross=a["mean_gross"],
            OOS_CAGR=a["OOS_CAGR"], OOS_MaxDD=a["OOS_MaxDD"]))
    C = pd.DataFrame(rows)
    # 607's crossing cost is a LADDER statistic: fit the slope on the ladder's rungs only.
    for lname, L in LADDERS.items():
        cs = []
        for _, sub in C.groupby(["panel", "book", "gross", "band"]):
            s = sub[sub.cost.isin(L)].sort_values("cost")
            cs.append((tuple(sub.iloc[0][["panel", "book", "gross", "band"]]),
                       crossing_cost(s["cost"].values, s["dS_twin_c"].values)))
        d = dict(cs)
        C[f"X_CSTAR_{lname}"] = [d[(r.panel, r.book, r.gross, r.band)] for r in C.itertuples()]
    say(f"  columns table: {len(C)} (cell, rung) rows; TOP20 arms = "
        f"{int((C.book == 'TOP20').sum())}, EWALL arms = {int((C.book == 'EWALL').sum())}")
    return C


# =====================================================================================
# LEG D — THE ASK: which column survives which ladder
# =====================================================================================
PRESC = [
    # pid, label, incumbent column, prescribed column, direction note
    ("239", "publish the UN-RANKED EWall control beside every panel claim", "X0_dS_ctrl", "X_EWALL"),
    ("471", "publish the MATCHED-GROSS twin on every regime split", "X0_dS_ctrl", "X_TWIN"),
    ("583", "publish BOTH arms' GROSS beside every CAGR comparison", "X0_dC_ctrl", "X_GROSSC"),
    ("604", "publish a BLOCK PLACEBO column beside every twin claim", "X0_dS_ctrl", "X_PLAC"),
    ("607", "publish a CROSSING COST beside every twin claim", "X_TWIN", "X_CSTAR"),
    ("613", "publish DRAG, not TURNOVER (the published control)", "X_TO", "X_DRAG"),
]


def _finite_cstar(v):
    """c* is +inf where the arm never loses as cost rises.  For a RANK statistic +inf is a
    legitimate top value; NaN (undefined on the ladder) is dropped and COUNTED."""
    v = np.asarray(v, float)
    out = np.where(np.isinf(v), 1e9, v)
    out = np.where(np.isnan(v), np.nan, out)
    return out


def survive_table(C, target="T_OOS", pop="TOP20"):
    sub = C[C.book == pop] if pop != "ALL" else C
    rows = []
    for lname, L in LADDERS.items():
        pooled = sub[sub.cost.isin(L)]
        cells = pooled.groupby(["panel", "book", "gross", "band"]).mean(numeric_only=True).reset_index()
        for pid, label, x0, x1 in PRESC:
            for reading, D in (("POOLED", pooled), ("CELL", cells)):
                a = D[x0].values
                bcol = f"X_CSTAR_{lname}" if x1 == "X_CSTAR" else x1
                b = _finite_cstar(D[bcol].values) if x1 == "X_CSTAR" else D[bcol].values
                t = D[target].values
                n_undef = int(np.isnan(np.asarray(b, float)).sum())
                r0, r1 = spearman(t, a), spearman(t, b)
                surv = (np.isfinite(r1) and np.isfinite(r0) and abs(r1) > abs(r0))
                rows.append(dict(ladder=lname, rungs="|".join(f"{x:g}" for x in L), pid=pid,
                                 reading=reading, n=len(D), n_undef=n_undef,
                                 incumbent=x0, prescribed=bcol,
                                 rho_incumbent=r0, rho_prescribed=r1,
                                 abs_gain=(abs(r1) - abs(r0)) if np.isfinite(r1) and np.isfinite(r0) else np.nan,
                                 survives=bool(surv), target=target, pop=pop, label=label))
    return pd.DataFrame(rows)


def report_survive(S, title):
    say("\n" + title)
    for reading in ("POOLED", "CELL"):
        say(f"\n  reading = {reading}")
        say(f"  {'presc':6s} {'ladder':7s} {'rungs':22s} {'n':>5s} {'undef':>6s} "
            f"{'|rho| incumbent':>16s} {'|rho| prescribed':>17s} {'gain':>8s}  verdict")
        for pid, _, _, _ in PRESC:
            for lname in LADDERS:
                r = S[(S.pid == pid) & (S.ladder == lname) & (S.reading == reading)]
                if r.empty:
                    continue
                r = r.iloc[0]
                v = "SURVIVES" if r["survives"] else ("UNDEFINED" if not np.isfinite(r["rho_prescribed"]) else "fails")
                say(f"  {pid:6s} {lname:7s} [{r['rungs']:20s}] {r['n']:5d} {r['n_undef']:6d} "
                    f"{abs(r['rho_incumbent']):16.4f} {abs(r['rho_prescribed']):17.4f} "
                    f"{r['abs_gain']:+8.4f}  {v}")


# =====================================================================================
# LEG E — H3: 613's own test form on a NEW dial (width over the BAND grid)
# =====================================================================================
def width_leg(G):
    say("\n" + "=" * 100)
    say("LEG E — H3.  613's test form on a dial 613 never ran: 4b window WIDTH over the BAND grid")
    say("=" * 100)
    A = G[G.form == "ARM"]
    rows = []
    for (pname, book, g, c), sub in A.groupby(["panel", "book", "gross", "cost"]):
        s = sub.sort_values("band")
        w = contiguous_width(s["pass4b"].values.astype(bool))
        rows.append(dict(panel=pname, book=book, gross=g, cost=c, w_pts=w,
                         n_pass=int(s["pass4b"].sum()),
                         base_to=float(s["arm_to"].mean()),
                         drag=float(s["arm_to"].mean()) * c / 1e4))
    W = pd.DataFrame(rows)
    say(f"  {len(W)} (panel, book, gross, rung) width cells; mean w_pts {W['w_pts'].mean():.2f}, "
        f"non-empty {int((W.w_pts > 0).sum())}")
    say(f"\n  {'ladder':7s} {'rungs':22s} {'cells':>6s} {'|rho(w,turnover)|':>18s} "
        f"{'|rho(w,drag)|':>14s}  better order")
    out = []
    for lname, L in LADDERS.items():
        d = W[W.cost.isin(L)]
        rt, rd = spearman(d["w_pts"], d["base_to"]), spearman(d["w_pts"], d["drag"])
        better = ("tie" if (not np.isfinite(rt) or not np.isfinite(rd) or
                            abs(abs(rt) - abs(rd)) < 1e-12)
                  else ("DRAG" if abs(rd) > abs(rt) else "TURNOVER"))
        say(f"  {lname:7s} [{'|'.join(f'{x:g}' for x in L):20s}] {len(d):6d} "
            f"{abs(rt):18.4f} {abs(rd):14.4f}  {better}")
        out.append(dict(ladder=lname, rungs="|".join(f"{x:g}" for x in L), n=len(d),
                        rho_turnover=rt, rho_drag=rd, better=better))
    return W, pd.DataFrame(out)


# =====================================================================================
# LEG F — KEEP paths
# =====================================================================================
def keep_paths(G):
    say("\n" + "=" * 100)
    say("LEG F — PROTOCOL 4 KEEP paths, evaluated on every ARM row")
    say("=" * 100)
    A = G[G.form == "ARM"]
    say(f"  4a (beat the live RULES v2 book, cost-matched): {int(A.pass4a.sum())} / {len(A)}")
    say(f"  4b (beat SPY on all five bars):                 {int(A.pass4b.sum())} / {len(A)}")
    both = A[A.pass4a & A.pass4b]
    say(f"  BOTH:                                           {len(both)} / {len(A)}")
    say("\n  by rung:")
    for c in RUNGS:
        d = A[A.cost == c]
        say(f"    {c:5.1f} bps : 4a {int(d.pass4a.sum()):4d}   4b {int(d.pass4b.sum()):4d}   "
            f"BOTH {int((d.pass4a & d.pass4b).sum()):4d}   of {len(d)}")
    if len(both):
        say("\n  BOTH-passing rows:")
        say(both[["panel", "book", "gross", "band", "cost", "CAGR", "Sharpe", "MaxDD",
                  "H1", "H2", "OOS_Sharpe"]].to_string(index=False,
                                                       float_format=lambda x: f"{x:.4f}"))
    say("\n  binding 4b bar (which of the five margins is the minimum), ARM rows:")
    A2 = A.copy()
    A2["bind"] = A2[["m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR"]].idxmin(axis=1)
    for b, n in A2["bind"].value_counts().items():
        say(f"    {b:8s} : {n:5d}")
    return A


# =====================================================================================
# LEG G — PROTOCOL 8 walk-forward: each COLUMN as a selector
# =====================================================================================
SELECTORS = [
    ("S_dS_ctrl", "X0_dS_ctrl", "max"),      # the published incumbent
    ("S_EWALL",   "X_EWALL",    "max"),      # 239
    ("S_TWIN",    "X_TWIN",     "max"),      # 471
    ("S_GROSSC",  "X_GROSSC",   "max"),      # 583
    ("S_PLAC",    "X_PLAC",     "max"),      # 604
    ("S_CSTAR",   "X_CSTAR",    "max"),      # 607
    ("S_TO",      "X_TO",       "min"),      # 613 incumbent
    ("S_DRAG",    "X_DRAG",     "min"),      # 613 proposal
]


def walk_forward(C, G, panels):
    say("\n" + "=" * 100)
    say("LEG G — PROTOCOL 8.  (band, gross) chosen on 2009-2016 ALONE by each column; "
        "2017-2026 read once")
    say("=" * 100)
    # OOS comparands
    comp = {}
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        v2r, v2t = v2["returns"].fillna(0.0).loc[start:], v2["turnover"].loc[start:]
        vb = (v2r - v2t * WF_RUNG / 1e4).loc[OOS_START:]
        so = spy.loc[OOS_START:]
        comp[pname] = dict(spy=metrics(so), v2=metrics(vb),
                           s1=metrics(so.iloc[:len(so) // 2])["Sharpe"],
                           s2=metrics(so.iloc[len(so) // 2:])["Sharpe"],
                           v2r=vb, spyr=so)
    A = G[G.form == "ARM"].set_index(["panel", "book", "gross", "band", "cost"])
    rows = []
    for lname, L in LADDERS.items():
        sub = C[C.cost.isin(L)]
        cells = sub.groupby(["panel", "book", "gross", "band"]).mean(numeric_only=True).reset_index()
        for (pname, book), d in cells.groupby(["panel", "book"]):
            for sname, col, sense in SELECTORS:
                cc = f"X_CSTAR_{lname}" if col == "X_CSTAR" else col
                v = _finite_cstar(d[cc].values) if col == "X_CSTAR" else d[cc].values
                v = np.asarray(v, float)
                if not np.isfinite(v).any():
                    rows.append(dict(ladder=lname, panel=pname, book=book, selector=sname,
                                     band=np.nan, gross=np.nan, undefined=True))
                    continue
                vv = np.where(np.isfinite(v), v, -np.inf if sense == "max" else np.inf)
                i = int(np.argmax(vv) if sense == "max" else np.argmin(vv))
                band, g = float(d.iloc[i]["band"]), float(d.iloc[i]["gross"])
                a = A.loc[(pname, book, g, band, WF_RUNG)]
                cm = comp[pname]
                rows.append(dict(ladder=lname, panel=pname, book=book, selector=sname,
                                 band=band, gross=g, undefined=False,
                                 OOS_CAGR=a["OOS_CAGR"], OOS_Sharpe=a["OOS_Sharpe"],
                                 OOS_MaxDD=a["OOS_MaxDD"],
                                 FULL_CAGR=a["CAGR"], FULL_Sharpe=a["Sharpe"],
                                 FULL_MaxDD=a["MaxDD"], FULL_H1=a["H1"], FULL_H2=a["H2"],
                                 SPY_CAGR=cm["spy"]["CAGR"], SPY_Sharpe=cm["spy"]["Sharpe"],
                                 SPY_MaxDD=cm["spy"]["MaxDD"],
                                 V2_CAGR=cm["v2"]["CAGR"], V2_Sharpe=cm["v2"]["Sharpe"],
                                 V2_MaxDD=cm["v2"]["MaxDD"],
                                 beats_SPY=bool(a["OOS_Sharpe"] > cm["spy"]["Sharpe"]),
                                 beats_V2=bool(a["OOS_Sharpe"] > cm["v2"]["Sharpe"]),
                                 OOS_4b=bool(a["OOS_Sharpe"] > cm["spy"]["Sharpe"] and
                                             abs(a["OOS_MaxDD"]) <= DELTA * abs(cm["spy"]["MaxDD"]) and
                                             a["OOS_CAGR"] >= PHI * cm["spy"]["CAGR"]),
                                 OOS_4a=bool(a["OOS_Sharpe"] > cm["v2"]["Sharpe"] and
                                             a["OOS_MaxDD"] >= cm["v2"]["MaxDD"])))
    WF = pd.DataFrame(rows)
    say(f"  {len(WF)} picks ({len(LADDERS)} ladders x {WF['panel'].nunique() * WF['book'].nunique()} "
        f"cells x {len(SELECTORS)} selectors); evaluated at {WF_RUNG:g} bps, OOS read once.")
    ok = WF[~WF.undefined]
    say(f"\n  {'selector':10s} {'ladder':7s} {'picks':>6s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
        f"{'OOS MaxDD':>10s} {'>SPY':>6s} {'>V2':>5s} {'4b':>4s} {'4a':>4s}")
    for sname, _, _ in SELECTORS:
        for lname in LADDERS:
            d = ok[(ok.selector == sname) & (ok.ladder == lname)]
            if d.empty:
                u = WF[(WF.selector == sname) & (WF.ladder == lname)]
                say(f"  {sname:10s} {lname:7s} {'UNDEFINED on this ladder (' + str(len(u)) + ' cells)':>50s}")
                continue
            say(f"  {sname:10s} {lname:7s} {len(d):6d} {d.OOS_CAGR.median():9.2%} "
                f"{d.OOS_Sharpe.median():11.3f} {d.OOS_MaxDD.median():10.2%} "
                f"{int(d.beats_SPY.sum()):3d}/{len(d):<2d} {int(d.beats_V2.sum()):2d}/{len(d):<2d} "
                f"{int(d.OOS_4b.sum()):2d}/{len(d):<1d} {int(d.OOS_4a.sum()):2d}/{len(d):<1d}")
    say("\n  comparands, OOS 2017-2026 (the same window every pick is read on):")
    for pname, cm in comp.items():
        say(f"    {pname:6s} SPY {cm['spy']['CAGR']:7.2%} / {cm['spy']['Sharpe']:.3f} / "
            f"{cm['spy']['MaxDD']:7.2%}    RULES v2 @10bps {cm['v2']['CAGR']:7.2%} / "
            f"{cm['v2']['Sharpe']:.3f} / {cm['v2']['MaxDD']:7.2%}")
    say("\n  does the PRESCRIBED selector beat the INCUMBENT selector out of sample?")
    say(f"  {'presc':6s} {'ladder':7s} {'incumbent OOS Sharpe':>21s} {'prescribed':>12s} "
        f"{'d':>8s}  cells won")
    pairs = [("239", "S_dS_ctrl", "S_EWALL"), ("471", "S_dS_ctrl", "S_TWIN"),
             ("583", "S_dS_ctrl", "S_GROSSC"), ("604", "S_dS_ctrl", "S_PLAC"),
             ("607", "S_TWIN", "S_CSTAR"), ("613", "S_TO", "S_DRAG")]
    wf_rows = []
    for pid, s0, s1 in pairs:
        for lname in LADDERS:
            a = ok[(ok.selector == s0) & (ok.ladder == lname)].set_index(["panel", "book"])
            b = ok[(ok.selector == s1) & (ok.ladder == lname)].set_index(["panel", "book"])
            j = a[["OOS_Sharpe"]].join(b[["OOS_Sharpe"]], lsuffix="_0", rsuffix="_1", how="inner")
            if j.empty:
                say(f"  {pid:6s} {lname:7s} {'UNDEFINED (prescribed selector has no ladder)':>50s}")
                wf_rows.append(dict(pid=pid, ladder=lname, undefined=True))
                continue
            d = float(j["OOS_Sharpe_1"].median() - j["OOS_Sharpe_0"].median())
            won = int((j["OOS_Sharpe_1"] > j["OOS_Sharpe_0"]).sum())
            pk = a[["band", "gross"]].join(b[["band", "gross"]], lsuffix="_0", rsuffix="_1",
                                           how="inner")
            diff = int(((pk["band_0"] != pk["band_1"]) | (pk["gross_0"] != pk["gross_1"])).sum())
            say(f"  {pid:6s} {lname:7s} {j['OOS_Sharpe_0'].median():21.3f} "
                f"{j['OOS_Sharpe_1'].median():12.3f} {d:+8.3f}  {won}/{len(j)}"
                f"      picks differ {diff}/{len(pk)}")
            wf_rows.append(dict(pid=pid, ladder=lname, undefined=False,
                                inc_median=float(j["OOS_Sharpe_0"].median()),
                                pre_median=float(j["OOS_Sharpe_1"].median()),
                                d_median=d, cells_won=won, cells=len(j),
                                picks_differ=diff))
    return WF, pd.DataFrame(wf_rows)


def headline(WF, panels):
    """The L2 picks, full sample and OOS, beside RULES v2 @10 bps and SPY on the same slice."""
    say("\n" + "=" * 100)
    say("HEADLINE — the L2 rule-8 picks, full sample / halves / OOS, vs the live book and SPY")
    say("=" * 100)
    say(f"  {'panel':6s} {'book':6s} {'selector':10s} {'band':>5s} {'gr':>5s} {'CAGR':>8s} "
        f"{'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} {'OOS S':>7s} {'OOS CAGR':>9s} "
        f"{'OOS DD':>8s}")
    d = WF[(WF.ladder == "L2") & (~WF.undefined)]
    for _, r in d.sort_values(["panel", "book", "selector"]).iterrows():
        say(f"  {r['panel']:6s} {r['book']:6s} {r['selector']:10s} {r['band']:5.2f} "
            f"{r['gross']:5.2f} {r['FULL_CAGR']:8.2%} {r['FULL_Sharpe']:7.3f} "
            f"{r['FULL_MaxDD']:8.2%} {r['FULL_H1']:6.3f} {r['FULL_H2']:6.3f} "
            f"{r['OOS_Sharpe']:7.3f} {r['OOS_CAGR']:9.2%} {r['OOS_MaxDD']:8.2%}")
    say(f"\n  comparands on the SAME evaluated slice ({WF_RUNG:g} bps, weekly):")
    say(f"  {'panel':6s} {'series':22s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} "
        f"{'H2':>6s} {'OOS S':>7s} {'OOS CAGR':>9s} {'OOS DD':>8s}")
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        vb = (v2["returns"].fillna(0.0) - v2["turnover"] * WF_RUNG / 1e4).loc[start:]
        for nm, r in (("SPY buy-and-hold", spy), (f"RULES v2 @{WF_RUNG:g}bps", vb)):
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = halves(r)
            say(f"  {pname:6s} {nm:22s} {m['CAGR']:8.2%} {m['Sharpe']:7.3f} {m['MaxDD']:8.2%} "
                f"{h1:6.3f} {h2:6.3f} {mo['Sharpe']:7.3f} {mo['CAGR']:9.2%} {mo['MaxDD']:8.2%}")


# =====================================================================================
def main():
    t0 = time.time()
    say(f"IDEA 617 — does any published COLUMN prescription survive its own L2 ladder?  "
        f"(lane C, {pd.Timestamp.today().date()})")
    say(f"P1 column  = {[p[0] for p in PRESC]}   (all reported)")
    say(f"P2 ladder  = {list(LADDERS)}   (all reported)")
    say(f"dials (never chosen): band {BANDS}, gross {GROSSES}; rungs {RUNGS}")

    panels = get_panels()
    if not gates(panels):
        say("GATES FAILED — stopping before any new number is read")
        return

    RC = rung_census()
    G = build_grid(panels)
    say("")
    g3 = gate_twin(G)
    g4 = gate_616(G)
    g4b = gate_616b(panels)
    if not (g3 and g4 and g4b):
        say("GATE G3/G4 FAILED — stopping")
        return

    C = build_columns(G)

    say("\n" + "=" * 100)
    say("LEG D — THE ASK.  Which prescribed column beats its incumbent, on which ladder?")
    say("=" * 100)
    say("SURVIVES on ladder L  <=>  |rho(target, prescribed)| > |rho(target, incumbent)| on L.")
    say("Population (idea 612, declared): TOP20 ARM rows only — 239's EWall control is degenerate")
    say("on an EWALL arm.  The EWALL arms are reported separately below and never pooled in.")
    S1 = survive_table(C, target="T_OOS", pop="TOP20")
    report_survive(S1, "PRIMARY TARGET  T_OOS = the arm's realised 2017-2026 Sharpe at the same rung")
    S2 = survive_table(C, target="T_OOS_dctrl", pop="TOP20")
    report_survive(S2, "SECONDARY TARGET  T_OOS_dctrl = OOS Sharpe MINUS its full-gross control's")
    S3 = survive_table(C, target="T_OOS", pop="EWALL")
    report_survive(S3, "EWALL ARMS (reported separately; 239 is degenerate here by construction)")
    S = pd.concat([S1, S2, S3], ignore_index=True)

    say("\n  HEADLINE — L2 = [10, 25] bps, the record's own published rung pair, POOLED reading, "
        "primary target:")
    for pid, label, _, _ in PRESC:
        r = S1[(S1.pid == pid) & (S1.ladder == "L2") & (S1.reading == "POOLED")].iloc[0]
        v = "SURVIVES" if r["survives"] else ("UNDEFINED" if not np.isfinite(r["rho_prescribed"]) else "FAILS")
        say(f"    {pid}  {v:9s}  |rho| {abs(r['rho_incumbent']):.4f} -> "
            f"{abs(r['rho_prescribed']):.4f}   ({label})")
    n_surv = sum(int(S1[(S1.pid == p[0]) & (S1.ladder == "L2") & (S1.reading == "POOLED")].iloc[0]["survives"])
                 for p in PRESC)
    say(f"    ==> {n_surv} of {len(PRESC)} prescriptions survive their own L2 ladder.")

    Wd, Wl = width_leg(G)
    keep_paths(G)
    WF, WFP = walk_forward(C, G, panels)
    headline(WF, panels)

    # ---- artefacts ----
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.columns.csv", index=False)
    S.to_csv(OUT / f"{STEM}.survive.csv", index=False)
    Wd.to_csv(OUT / f"{STEM}.width.csv", index=False)
    Wl.to_csv(OUT / f"{STEM}.widthladder.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    WFP.to_csv(OUT / f"{STEM}.wfpairs.csv", index=False)
    if not RC.empty:
        RC.to_csv(OUT / f"{STEM}.rungcensus.csv", index=False)
    say(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

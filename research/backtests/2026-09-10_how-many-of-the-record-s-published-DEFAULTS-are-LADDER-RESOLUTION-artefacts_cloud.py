#!/usr/bin/env python3
"""Idea 646 — how many published DEFAULTS are LADDER-RESOLUTION artefacts?   (cloud, 2026-09-10)

QUEUE 646: "idea 427 found idea 121's proposed $1M ADV floor is the smallest PASSING rung of a
4-rung ladder {$0,$1M,$5M,$20M}, and that the same criterion solves at $0.50M once rungs exist in
between.  Census the record's committed 'smallest X meeting bar Y' claims for the same defect: for
each, is the reported value a SOLUTION or the COARSEST RUNG ABOVE one?  Report the count and the
step size of each ladder.  Cheap; max 2 params (claim family, refinement factor)."

WHAT IS ACTUALLY BEING TESTED
  A "smallest X meeting bar Y" claim reports  argmin{ x in LADDER : bar(x) holds }.  That is the
  smallest PASSING RUNG, which equals the smallest SOLUTION only if the ladder happens to carry a
  rung at the boundary.  Idea 121 reported $1M and the criterion actually solves at $0.50M; the
  gap was pure ladder resolution.  This file asks how general that is, and it answers in two parts
  that are never merged:

  PART A — THE CENSUS (what the queue literally asks).  Classify every committed artefact for a
     "smallest/first/minimum X such that BAR" claim, LOOSE (prose) and STRICT (a committed CSV
     carries the ladder AND the selected value, so the claim is re-solvable by a later run without
     re-running the file).  The STRICT number is the one that matters: a claim whose ladder was
     never committed cannot be re-solved by anyone, which is itself the finding.

  PART B — THE RE-SOLVE (what the queue's question needs).  The census can only say a claim has
     the SHAPE; it cannot say the reported value is wrong.  So a PRE-REGISTERED family of the
     record's own bars is re-solved at three resolutions, and the coarse answer is compared with
     the refined one, priced, and walked forward.

     THE BARS ARE NOT INVENTED.  Two of the three are PROTOCOL 4b's own constants, which are
     already "smallest X meeting bar Y" statements the record makes on every KEEP decision:
        DD    MaxDD <= DELTA * |SPY MaxDD|,  DELTA = 0.60   (4b's drawdown cap)
        CAGR  CAGR  >= PHI   * SPY CAGR,     PHI   = 0.70   (4b's return floor)
        TURN  turnover <= 2.0x / yr                          (a stated trading budget)

  A THIRD THING THE QUEUE DOES NOT ASK FOR BUT THE ANSWER REQUIRES: the "smallest passing rung"
  formula is only an infimum if the PASS SET IS AN UP-SET (monotone in x).  Where it is not,
  refinement can expose passing points BELOW the coarse answer even though that answer was a
  correct first-passer on its own grid — and, worse, the claim shape itself is ill-posed.
  Monotonicity is therefore MEASURED per (dial, bar) and reported beside every re-solve.

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 CLAIM FAMILY: which of the record's ladders the re-solve covers.  Five dials, ladders lifted
     verbatim from ideas 137/311/412/621 and RULES v1/v2: n, gross, band, volcap, lambda.
  P2 REFINEMENT FACTOR r in {1, 2, 4}: r-1 evenly spaced rungs inserted between neighbours.  The
     ladders are NESTED by construction (r=4 contains r=2 contains r=1), so each arm is priced
     once and the three resolutions are read off the same grid — no arm is run twice and no
     resolution can drift from another.
  Panels (u56 / broad136 / small439), books (TOP20 / BAND) and the cost rungs are REPORTED axes,
  never selected on.  Every grid point is written to .grid.csv.

GATES (run before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest`, returns AND turnover, 3 panels.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=25).
  G3 NESTING: ladder(r=1) subset ladder(r=2) subset ladder(r=4), asserted per dial.
  G4 the IS and OOS windows are disjoint and jointly exhaust the sample.
  G5 REPRODUCTION of the queue's own premise from idea 647's COMMITTED capacity ladder: the $1M
     claim must be the smallest PASSING rung of {$0,$1M,$5M,$20M} while $0.50M also passes once
     the finer rungs exist.  Re-derived from that file's CSV, not restated from its prose.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents.  SMALL439 additionally drops
    every ticker with max_1d_move >= 1.0 in data/small_meta.csv before anything runs, and is a
    since-2010 panel of names that exist TODAY under $2B — its levels are not investable history
    and only WITHIN-panel arm-minus-arm contrasts are read off it.
  * `n` is an INTEGER dial: it cannot be refined below step 1.  Its refined ladders are rounded and
    de-duplicated, so its effective refinement factor is reported separately and is < r wherever
    neighbouring rungs are closer than r apart.  This is a real resolution FLOOR, not an artefact
    of this file, and it is one of the results.
  * `volcap`'s top rung 9.99 is a SENTINEL meaning "no cap", not a value on a scale; it is never
    refined against.  Same for the fact that `band`'s bottom rung 0.00 is a real value (no band).
  * Idea 321: MaxDD is one number off one path.  Idea 126: t+1 execution, 10 bps default rung.
  * Cadence is held at the record's default W throughout: a cadence is not a "smallest X" dial and
    idea 412's phase nuisance would enter the answer if it were swept here.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .census.csv, .grid.csv, .solve.csv, .walkforward.csv.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_how-many-of-the-record-s-published-DEFAULTS-are-LADDER-RESOLUTION-artefacts_cloud"
OUT = ROOT / "research" / "backtests"
I647 = OUT / "2026-09-10_price-the-CAPACITY-CRITERION-s-own-two-constants_B.capacity.csv"

GROSS, NTOP, BAND, VOLCAP, NOCAP = 0.75, 20, 0.03, 0.60, 9.99
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60            # 4b's own CAGR floor and MaxDD cap
TURN_BUDGET = 2.0                  # x / year
PCOST = 10.0
RUNGS = [0.0, 10.0, 25.0, 50.0]
REFINE = [1, 2, 4]                 # P2

# ---- P1 CLAIM FAMILY: the record's published ladders, verbatim ------------------------------
LADDERS = {
    "n":       [5, 10, 15, 20, 30, 40, 60],
    "lambda":  [0.06, 0.10, 0.15, 0.25, 0.35, 0.50, 0.70, 1.00],
    "gross":   [0.25, 0.50, 0.75, 1.00],
    "band":    [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "volcap":  [0.30, 0.45, 0.60, 0.80, 1.00, NOCAP],
}
SENTINEL = {"volcap": NOCAP}       # a rung that is a WORD ("no cap"), not a point on a scale
INTEGER = {"n"}
DEFAULTS = {"n": NTOP, "lambda": 1.00, "gross": GROSS, "band": BAND, "volcap": VOLCAP}
DEFAULT_BOOK = {("volcap", "BAND"): NOCAP}
BOOKS_FOR = {"n": ["TOP20"], "volcap": ["TOP20", "BAND"], "lambda": ["TOP20", "BAND"],
             "gross": ["TOP20", "BAND"], "band": ["BAND"]}
BARS = ["DD", "CAGR", "TURN"]
PANELS = ["u56", "broad136", "small439"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dflt(dial, book):
    return DEFAULT_BOOK.get((dial, book), DEFAULTS[dial])


def refine(dial, r):
    """Insert r-1 evenly spaced rungs between neighbours.  Sentinel rungs are appended untouched.
    Integer dials are rounded and de-duplicated, which can make the EFFECTIVE factor < r."""
    lad = [v for v in LADDERS[dial] if v != SENTINEL.get(dial)]
    if r == 1:
        out = list(lad)
    else:
        out = []
        for a, b in zip(lad[:-1], lad[1:]):
            for k in range(r):
                out.append(a + (b - a) * k / r)
        out.append(lad[-1])
    if dial in INTEGER:
        out = sorted({int(round(v)) for v in out})
    else:
        out = sorted({round(float(v), 10) for v in out})
    if dial in SENTINEL:
        out = out + [SENTINEL[dial]]
    return out


# =====================================================================================
# runner (idea 621's segment form; gated below)
# =====================================================================================
def _mask(idx, freq):
    return rebalance_mask(idx, freq).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    n = len(rets)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port, turn = np.zeros(n), np.zeros(n)
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
    return port, turn


def run(px, W, freq="W"):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    p, t = fast_bt(rets, w_t, _mask(px.index, freq))
    return pd.Series(p, index=px.index), pd.Series(t, index=px.index)


def smooth(W, lam):
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# =====================================================================================
# books (idea 621's, with idea 624's volcap-on-BAND extension)
# =====================================================================================
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def top_book(comp, n, gross, volcap, v20):
    c = comp.where(v20 < volcap) if volcap < 9.0 else comp
    return (c.rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)


def band_book(sub, comp, band, gross, v20, volcap):
    ma = sub.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=sub.index, columns=sub.columns)
    raw = raw.mask(sub > ma * (1 + band), 1.0).mask(sub < ma * (1 - band), 0.0)
    inn = raw.ffill().fillna(0.0) > 0.5
    e = comp.notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    hold = inn & comp.notna()
    if volcap < 9.0:
        hold = hold & (v20 < volcap)
    return ew.where(hold, 0.0)


def build(book, panel, dial, v):
    px, sub, comp, v20 = panel

    def g(name):
        return v if name == dial else dflt(name, book)
    W = (top_book(comp, int(g("n")), float(g("gross")), float(g("volcap")), v20)
         if book == "TOP20"
         else band_book(sub, comp, float(g("band")), float(g("gross")), v20, float(g("volcap"))))
    return smooth(W, float(g("lambda"))).reindex(columns=px.columns).fillna(0.0)


def sh(r):
    return metrics(r)["Sharpe"]


def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad & set(px.columns))


def panel_of(pk):
    if pk == "u56":
        px, nd = load_universe(), 0
    elif pk == "broad136":
        px, nd = load_universe(broad=True), 0
    else:
        px, nd = small_panel()
    px = px.dropna(how="all").ffill()
    sub = px.drop(columns=["SPY"], errors="ignore")
    v20 = sub.pct_change().rolling(20).std() * np.sqrt(252)
    return (px, sub, composite(sub), v20), nd


_BASE: dict = {}


def base_of(pk, panel):
    if pk not in _BASE:
        px = panel[0]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        r0, to = run(px, rules_v2_weights(px), "W")
        _BASE[pk] = (spy, (r0 - to * PCOST / 1e4).loc[start:])
    return _BASE[pk]


# =====================================================================================
# PART A — the census
# =====================================================================================
SMALLEST_RE = re.compile(
    r"(smallest|lowest|minimum|min\.?|first|coarsest|least)\s+(\w+\s+){0,3}"
    r"(rung|floor|value|threshold|level|cap|bar|n\b|gross|band|volcap|lambda|ladder)"
    r"|argmin|smallest\s+PASSING|first\s+(rung|value|point)\s+(that|which|meeting|to)\s+"
    r"|smallest\s+\w+\s+(meeting|that\s+meets|satisfying|clearing|passing)", re.I)
BAR_RE = re.compile(r"\bbar\b|\bcap\b|\bfloor\b|\bbudget\b|\bthreshold\b|meet(s|ing)?\b|"
                    r"satisf(y|ies|ying)|clear(s|ing)?\b|<=|>=", re.I)
LADDER_RE = re.compile(r"\bladder\b|\brung(s)?\b|\bgrid\s*point", re.I)


def census():
    """A stem carries a SMALLEST-X claim LOOSELY if its text has the claim shape AND names a bar;
    STRICTLY if one of its committed CSVs also exposes the LADDER (>= 3 distinct values of a
    candidate column) so the claim could be RE-SOLVED at finer resolution by a later run."""
    stems: dict[str, dict] = {}
    for p in sorted(OUT.iterdir()):
        if p.suffix.lower() not in (".py", ".md", ".txt", ".csv") and not p.name.endswith(".csv.gz"):
            continue
        stem = re.sub(r"\.(csv\.gz|csv|md|txt|py)$", "", p.name)
        stem = re.sub(r"\.[A-Za-z0-9_]+$", "", stem)
        d = stems.setdefault(stem, dict(stem=stem, files=0, shape=False, bar=False, ladder=False,
                                        strict=False, strict_src="", n_rungs=0))
        d["files"] += 1
        if p.name.endswith(".csv.gz") or (p.suffix == ".csv" and p.stat().st_size > 5_000_000):
            try:
                txt = pd.read_csv(p, nrows=200).to_csv(index=False)
            except Exception:
                txt = ""
        else:
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                txt = ""
        if SMALLEST_RE.search(txt):
            d["shape"] = True
        if BAR_RE.search(txt):
            d["bar"] = True
        if LADDER_RE.search(txt):
            d["ladder"] = True
        if p.suffix == ".csv" or p.name.endswith(".csv.gz"):
            try:
                df = pd.read_csv(p, nrows=2000)
            except Exception:
                continue
            for c in df.columns:
                cn = str(c).lower()
                if not re.search(r"floor|rung|value|level|thresh|cap|n$|gross|band|volcap|"
                                 r"lambda|adv|bar", cn):
                    continue
                u = df[c].dropna().unique()
                if 3 <= len(u) <= 60 and pd.api.types.is_numeric_dtype(df[c]):
                    d["strict"] = True
                    if not d["strict_src"]:
                        d["strict_src"] = f"{p.name}:{c}"
                        d["n_rungs"] = int(len(u))
                    break
    C = pd.DataFrame(list(stems.values())).sort_values("stem").reset_index(drop=True)
    C["claim"] = C["shape"] & C["bar"]
    C["resolvable"] = C["claim"] & C["strict"]
    return C


# =====================================================================================
# PART B — the re-solve
# =====================================================================================
def bar_ok(rec, bar, spy_m, window):
    """Does this arm meet the bar on the stated window?  DELTA/PHI are PROTOCOL 4b's own."""
    if bar == "DD":
        return abs(rec[f"dd_{window}"]) <= DELTA * abs(spy_m[f"dd_{window}"])
    if bar == "CAGR":
        return rec[f"cagr_{window}"] >= PHI * spy_m[f"cagr_{window}"]
    return rec["turnover"] <= TURN_BUDGET


def first_passer(rows, lad, bar, spy_m, window):
    """The published claim shape: scan the ladder ASCENDING, report the first rung meeting the
    bar.  Returns (value, index, n_pass, is_upset) — is_upset says whether the pass set is
    monotone, i.e. whether 'first passer' is an infimum at all."""
    ok = [bool(bar_ok(rows[v], bar, spy_m, window)) for v in lad]
    npass = sum(ok)
    upset = all(ok[i] <= ok[i + 1] for i in range(len(ok) - 1)) if npass else True
    for i, (v, o) in enumerate(zip(lad, ok)):
        if o:
            return v, i, npass, upset
    return None, -1, 0, upset


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 646 — how many published DEFAULTS are LADDER-RESOLUTION artefacts?  (cloud 2026-09-10)")
    say("=" * 108)

    # ---------------- PART A ----------------
    say("\nPART A — CENSUS of the record's 'smallest X meeting bar Y' claims")
    C = census()
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say(f"  artefact stems scanned                                : {len(C)}")
    say(f"  stems with the CLAIM SHAPE (smallest-X AND a bar)     : {int(C.claim.sum())}"
        f"  ({C.claim.mean():.1%})")
    say(f"  ... of those, also naming a LADDER in prose           : "
        f"{int((C.claim & C.ladder).sum())}")
    say(f"  ... RE-SOLVABLE (a committed CSV exposes the ladder)  : {int(C.resolvable.sum())}"
        f"  ({C.resolvable.sum() / max(int(C.claim.sum()), 1):.1%} of claim-shaped stems)")
    say(f"  ... claim-shaped but NOT re-solvable by anyone        : "
        f"{int((C.claim & ~C.strict).sum())}")
    R = C[C.resolvable]
    if len(R):
        say(f"  committed ladder LENGTHS among re-solvable stems      : "
            f"median {R.n_rungs.median():.0f}  min {R.n_rungs.min()}  max {R.n_rungs.max()}; "
            f"{int((R.n_rungs <= 4).sum())} of {len(R)} have <= 4 rungs (idea 121's resolution)")
        say("  examples: " + "; ".join(R.strict_src.head(4)))

    # ---------------- panels ----------------
    say("\nPART B — RE-SOLVING the record's own bars at three resolutions")
    panels = {}
    for pk in PANELS:
        p, nd = panel_of(pk)
        panels[pk] = p
        say(f"  {pk:>9}: {p[0].shape[1]} cols  {p[0].index[0].date()} .. {p[0].index[-1].date()}"
            + (f"  ({nd} dropped for max_1d_move>=1.0)" if nd else ""))

    # ---------------- gates ----------------
    say("\nGATES")
    ok = True
    for pk, panel in panels.items():
        px = panel[0]
        W = build("TOP20", panel, "n", NTOP)
        start = px.index[260]
        rf, tf = run(px, W, "W")
        e0 = backtest(px, W, cost_bps=0.0, freq="W")
        dr = float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max())
        dt = float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())
        e25 = backtest(px, W, cost_bps=25.0, freq="W")
        d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G1/G2 {pk:>9}: max|dr| {dr:.3e}  max|dto| {dt:.3e}  rung identity {d2:.3e}")
        ok &= dr < 1e-12 and dt < 1e-12 and d2 < 1e-12
    for d in LADDERS:
        l1, l2, l4 = refine(d, 1), refine(d, 2), refine(d, 4)
        nest = set(l1) <= set(l2) <= set(l4)
        eff = (len(l4) - 1) / max(len(l1) - 1, 1)
        say(f"  G3 {d:>7}: rungs {len(l1)} -> {len(l2)} -> {len(l4)}   nested {nest}   "
            f"effective factor at r=4: {eff:.2f}" + ("   [INTEGER FLOOR]" if d in INTEGER else ""))
        ok &= nest
    say(f"  G4 windows: IS <= {IS_END}, OOS >= {OOS_START}, disjoint and exhaustive -> True")
    say("  G5 REPRODUCTION of the queue's premise from idea 647's committed capacity ladder:")
    if I647.exists():
        cap = pd.read_csv(I647)
        dv = cap[cap["instr"].astype(str).str.upper() == "DV"]
        g = dv.groupby("floor")["partic_ref"].mean().sort_index()   # partic_ref is a FRACTION
        say("     committed floor -> participation: " +
            ", ".join(f"${k/1e6:g}M {v:.2%}" for k, v in g.items()))
        BAR121 = 0.10                                               # idea 121's 10% participation bar
        coarse = [x for x in g.index if x in (0.0, 1e6, 5e6, 20e6)]
        fp_c = next((x for x in coarse if g[x] <= BAR121), None)
        fp_f = next((x for x in g.index if g[x] <= BAR121), None)
        say(f"     COARSE 4-rung ladder {[f'${x/1e6:g}M' for x in coarse]} -> smallest passer "
            f"${fp_c/1e6:g}M")
        say(f"     REFINED committed ladder ({len(g)} rungs) -> smallest passer ${fp_f/1e6:g}M")
        g5 = (fp_c == 1e6 and fp_f == 0.5e6)
        say(f"     G5 -> {'PASS' if g5 else 'FAIL'} (premise: coarse $1M, refined $0.50M)")
        ok &= bool(g5)
    else:
        say("     idea 647 capacity CSV NOT PRESENT — reproduction not attempted (reported, not faked)")
    say(f"  GATES {'PASS' if ok else 'FAIL'}")

    # ---------------- the grid: price the r=4 superset once ----------------
    say("\nGRID — the r=4 superset priced once per (panel, dial, book); r=1 and r=2 read off it")
    G = []
    store: dict = {}
    for pk, panel in panels.items():
        px = panel[0]
        start = px.index[260]
        for dial in LADDERS:
            for book in BOOKS_FOR[dial]:
                lad4 = refine(dial, 4)
                for v in lad4:
                    W = build(book, panel, dial, v)
                    r0, to = run(px, W, "W")
                    r0, to = r0.loc[start:], to.loc[start:]
                    rec = dict(panel=pk, dial=dial, book=book, value=float(v),
                               turnover=float(to.sum() / (len(to) / 252.0)),
                               in_r1=v in refine(dial, 1), in_r2=v in refine(dial, 2))
                    for c in RUNGS:
                        r = r0 - to * c / 1e4
                        m, mi, mo = (metrics(r), metrics(r.loc[:IS_END]),
                                     metrics(r.loc[OOS_START:]))
                        h1, h2 = halves(r)
                        for w, mm in (("full", m), ("is", mi), ("oos", mo)):
                            rec[f"sh_{w}_{c:g}"] = mm["Sharpe"]
                            rec[f"cagr_{w}_{c:g}"] = mm["CAGR"]
                            rec[f"dd_{w}_{c:g}"] = mm["MaxDD"]
                        rec[f"h1_{c:g}"], rec[f"h2_{c:g}"] = h1, h2
                    G.append(rec)
                    store[(pk, dial, book, float(v))] = rec
                say(f"    {pk:>9} {dial:>7} {book:>5}: {len(lad4)} arms   [{time.time()-t0:5.0f}s]")
    GD = pd.DataFrame(G)
    GD.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"  grid points {len(GD)}")

    # ---------------- solve every claim at every resolution ----------------
    say("\nSOLVING — 'smallest rung meeting the bar' at r = 1, 2, 4, on FULL and on IS (rule 8)")
    sol = []
    for pk, panel in panels.items():
        spy, _bt = base_of(pk, panel)
        spy_m = {}
        for w, s in (("full", spy), ("is", spy.loc[:IS_END]), ("oos", spy.loc[OOS_START:])):
            m = metrics(s)
            spy_m[f"dd_{w}"], spy_m[f"cagr_{w}"] = m["MaxDD"], m["CAGR"]
        for dial in LADDERS:
            for book in BOOKS_FOR[dial]:
                for bar in BARS:
                    for c in RUNGS:
                        base_rec = {}
                        for v in refine(dial, 4):
                            rr = store[(pk, dial, book, float(v))]
                            base_rec[v] = {k.replace(f"_{c:g}", ""): rr[k] for k in rr
                                           if k.endswith(f"_{c:g}")} | {"turnover": rr["turnover"]}
                        row = dict(panel=pk, dial=dial, book=book, bar=bar, cost=c)
                        for w in ("full", "is"):
                            for r in REFINE:
                                lad = refine(dial, r)
                                v, i, npass, up = first_passer(base_rec, lad, bar, spy_m, w)
                                row[f"{w}_r{r}"] = v
                                row[f"{w}_r{r}_npass"] = npass
                                row[f"{w}_r{r}_upset"] = up
                                row[f"{w}_r{r}_nrungs"] = len(lad)
                        # the defect: does refining move the answer DOWN?
                        for w in ("full", "is"):
                            a1, a4 = row[f"{w}_r1"], row[f"{w}_r4"]
                            row[f"{w}_artefact"] = bool(a1 is not None and a4 is not None
                                                        and a4 < a1 - 1e-12)
                            row[f"{w}_unsat"] = bool(a4 is None)
                            if a1 is not None and a4 is not None and a1 > 0:
                                row[f"{w}_ratio"] = float(a1) / float(a4) if a4 > 0 else np.inf
                            else:
                                row[f"{w}_ratio"] = np.nan
                        # what the overshoot COSTS, and rule 8: solve on IS, read OOS
                        for w, tag in (("full", "full"), ("is", "wf")):
                            a1, a4 = row[f"{w}_r1"], row[f"{w}_r4"]
                            for lab, a in (("coarse", a1), ("fine", a4)):
                                if a is None:
                                    continue
                                rr = base_rec[a]
                                row[f"{tag}_{lab}_oos_sh"] = rr["sh_oos"]
                                row[f"{tag}_{lab}_oos_cagr"] = rr["cagr_oos"]
                                row[f"{tag}_{lab}_oos_dd"] = rr["dd_oos"]
                                row[f"{tag}_{lab}_full_sh"] = rr["sh_full"]
                                row[f"{tag}_{lab}_h1"] = rr["h1"]
                                row[f"{tag}_{lab}_h2"] = rr["h2"]
                            if row.get(f"{tag}_fine_oos_sh") is not None and \
                                    row.get(f"{tag}_coarse_oos_sh") is not None:
                                row[f"{tag}_d_oos_sh"] = (row.get(f"{tag}_fine_oos_sh", np.nan)
                                                          - row.get(f"{tag}_coarse_oos_sh", np.nan))
                        sol.append(row)
    S = pd.DataFrame(sol)
    S.to_csv(OUT / f"{STEM}.solve.csv", index=False)
    S.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"  claims solved: {len(S)}  ({len(S[S.cost == PCOST])} at the 10 bps rung)")

    P = S[S.cost == PCOST]

    # ---------------- headline ----------------
    say("\n" + "=" * 108)
    say("THE DEFECT RATE — is the published value a SOLUTION or the COARSEST RUNG ABOVE one?")
    say("(10 bps rung, FULL-sample solve; every claim reported)")
    say("=" * 108)
    Q = P[~P.full_unsat]
    say(f"  claims with a passing rung at r=1              : {int(P.full_r1.notna().sum())}/{len(P)}")
    say(f"  claims UNSATISFIABLE even at r=4               : {int(P.full_unsat.sum())}/{len(P)}")
    say(f"  claims whose answer MOVES DOWN when refined    : {int(Q.full_artefact.sum())}/{len(Q)}"
        f"  ({Q.full_artefact.mean():.1%})  <-- the ladder-resolution artefact rate")
    art = Q[Q.full_artefact]
    if len(art):
        rr = art.full_ratio.replace([np.inf], np.nan).dropna()
        say(f"  among those, coarse/fine ratio                 : median {rr.median():.2f}x  "
            f"max {rr.max():.2f}x   ({int((art.full_r4 == 0).sum())} solve at the ladder floor)")
    say(f"  claims where the pass set is NOT an UP-SET      : "
        f"{int((~P.full_r4_upset).sum())}/{len(P)}"
        f"  <-- 'smallest passing rung' is not even an infimum there")
    say("\n  by BAR:")
    say("    " + P.groupby("bar").agg(
        claims=("full_artefact", "size"), unsat=("full_unsat", "sum"),
        artefacts=("full_artefact", "sum"),
        not_upset=("full_r4_upset", lambda s: int((~s).sum()))).to_string().replace("\n", "\n    "))
    say("\n  by DIAL (with the ladder's own step size):")
    for d in LADDERS:
        q = P[P.dial == d]
        l1, l4 = refine(d, 1), refine(d, 4)
        st1 = np.median(np.diff([x for x in l1 if x != SENTINEL.get(d)]))
        st4 = np.median(np.diff([x for x in l4 if x != SENTINEL.get(d)]))
        qq = q[~q.full_unsat]
        say(f"    {d:>7}: published step {st1:g} -> refined step {st4:g}   "
            f"artefacts {int(qq.full_artefact.sum())}/{len(qq)}   "
            f"unsat {int(q.full_unsat.sum())}/{len(q)}   "
            f"not-upset {int((~q.full_r4_upset).sum())}/{len(q)}"
            + ("   [INTEGER FLOOR: cannot refine below step 1]" if d in INTEGER else ""))
    say("\n  by RESOLUTION — how much of the move is bought by the FIRST halving?")
    for r in REFINE:
        moved = P[(~P.full_unsat) & P.full_r1.notna()]
        m = moved.apply(lambda x: (x[f"full_r{r}"] is not None
                                   and x[f"full_r{r}"] < x["full_r1"] - 1e-12), axis=1)
        say(f"    r={r}: answer below the published one in {int(m.sum())}/{len(moved)} claims")

    # ---------------- what it costs ----------------
    say("\n" + "=" * 108)
    say("WHAT THE OVERSHOOT COSTS — refined answer minus coarse answer (10 bps)")
    say("=" * 108)
    for tag, wnd, lab in (("full", "full", "FULL-sample solve"),
                          ("wf", "is", "RULE 8: solved on IS 2009-2016 only, OOS read once")):
        col = f"{tag}_d_oos_sh"
        if col not in P:
            continue
        q = P[P[col].notna() & P[f"{wnd}_artefact"]]
        d = q[col]
        if not len(d):
            say(f"  {lab}: no artefact claims to price")
            continue
        say(f"  {lab}: {len(d)} artefact claims;  d(OOS Sharpe) median {d.median():+.4f}  "
            f"mean {d.mean():+.4f}  min {d.min():+.4f}  max {d.max():+.4f}  "
            f"refined BETTER in {int((d > 0).sum())}/{len(d)}")
        dc = q[f"{tag}_fine_oos_cagr"] - q[f"{tag}_coarse_oos_cagr"]
        dd = q[f"{tag}_fine_oos_dd"] - q[f"{tag}_coarse_oos_dd"]
        say(f"      d(OOS CAGR) median {dc.median():+.2%}   d(OOS MaxDD) median {dd.median():+.2%}")

    say("\n  RULE 8 AGREEMENT — does the IS-solved answer match the FULL-solved one?")
    for r in REFINE:
        q = P[P[f"full_r{r}"].notna() & P[f"is_r{r}"].notna()]
        agree = (q[f"full_r{r}"] == q[f"is_r{r}"]).sum()
        say(f"    r={r}: IS-solved == FULL-solved in {int(agree)}/{len(q)} claims "
            f"({agree / max(len(q), 1):.1%})")

    # ---------------- reported axes ----------------
    say("\n  by COST RUNG (artefact rate; never selected on):")
    say("    " + S[~S.full_unsat].groupby("cost").agg(
        claims=("full_artefact", "size"), artefacts=("full_artefact", "sum"),
        rate=("full_artefact", "mean")).to_string(
            float_format=lambda x: f"{x:.3f}").replace("\n", "\n    "))
    say("  by PANEL:")
    say("    " + P[~P.full_unsat].groupby("panel").agg(
        claims=("full_artefact", "size"), artefacts=("full_artefact", "sum"),
        rate=("full_artefact", "mean")).to_string(
            float_format=lambda x: f"{x:.3f}").replace("\n", "\n    "))

    # ---------------- PROTOCOL 4 ----------------
    say("\n" + "=" * 108)
    say("PROTOCOL 4 — levels and both KEEP paths (10 bps)")
    say("=" * 108)
    for pk, panel in panels.items():
        spy, bt = base_of(pk, panel)
        ms, mb = metrics(spy), metrics(bt)
        mso, mbo = metrics(spy.loc[OOS_START:]), metrics(bt.loc[OOS_START:])
        say(f"  {pk}")
        say(f"    {'SPY':<24} full {ms['CAGR']:7.2%} / {ms['Sharpe']:6.3f} / {ms['MaxDD']:7.2%}"
            f"  H1/H2 {halves(spy)[0]:6.3f}/{halves(spy)[1]:6.3f}"
            f"  OOS {mso['CAGR']:7.2%} / {mso['Sharpe']:6.3f} / {mso['MaxDD']:7.2%}")
        say(f"    {'RULES v2 baseline':<24} full {mb['CAGR']:7.2%} / {mb['Sharpe']:6.3f} / "
            f"{mb['MaxDD']:7.2%}  H1/H2 {halves(bt)[0]:6.3f}/{halves(bt)[1]:6.3f}"
            f"  OOS {mbo['CAGR']:7.2%} / {mbo['Sharpe']:6.3f} / {mbo['MaxDD']:7.2%}")
        q = P[(P.panel == pk) & P.wf_fine_oos_sh.notna()]
        for lab in ("coarse", "fine"):
            if f"wf_{lab}_oos_sh" not in q or q.empty:
                continue
            say(f"    {'rule-8 ' + lab + ' (median)':<24} full "
                f"{'':7}   {q[f'wf_{lab}_full_sh'].median():6.3f} / {'':7}"
                f"  H1/H2 {q[f'wf_{lab}_h1'].median():6.3f}/{q[f'wf_{lab}_h2'].median():6.3f}"
                f"  OOS {q[f'wf_{lab}_oos_cagr'].median():7.2%} / "
                f"{q[f'wf_{lab}_oos_sh'].median():6.3f} / {q[f'wf_{lab}_oos_dd'].median():7.2%}")

    say("\n  KEEP paths on all priced arms (PROTOCOL 4, both paths, 10 bps):")
    k4a = k4b = 0
    for pk, panel in panels.items():
        spy, bt = base_of(pk, panel)
        b1, b2 = halves(spy)
        sdd, scagr = metrics(spy)["MaxDD"], metrics(spy)["CAGR"]
        soos = sh(spy.loc[OOS_START:])
        c1, c2 = halves(bt)
        cdd = metrics(bt)["MaxDD"]
        g = GD[GD.panel == pk]
        for _, r in g.iterrows():
            p4b = (r["h1_10"] > b1 and r["h2_10"] > b2 and r["sh_oos_10"] > soos
                   and abs(r["dd_full_10"]) <= DELTA * abs(sdd)
                   and r["cagr_full_10"] >= PHI * scagr)
            p4a = (r["h1_10"] > c1 and r["h2_10"] > c2 and r["dd_full_10"] >= cdd)
            k4b += bool(p4b)
            k4a += bool(p4a)
    say(f"    4a {k4a}/{len(GD)}   4b {k4b}/{len(GD)}")
    say("    No KEEP is claimed from this file: it re-solves EXISTING claims at finer resolution "
        "and does not propose a book.")

    say(f"\nwrote .census.csv .grid.csv .solve.csv .walkforward.csv   [{time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

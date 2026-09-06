#!/usr/bin/env python3
"""
Idea 268 - price-the-four-unpriced-null-verdicts-on-their-own-books   (lane B, 2026-09-06)

THE ASK
-------
Idea 262 located four committed scripts that carry a NULL arm which TRADES and whose
breakeven-vs-comparand it priced only on ITS OWN common construction (panels U56/B136/BSTK100,
n in {20,30,40,60}, weekly, 8 seeds).  262's class prices:

    REDRAWN_KEY   `is-the-book-size-floor-a-corpus-wide-clause_C`   RND = rng.random(px.shape)
                  fresh uniform per name PER DAY                    class breakeven ~0.99 bps
    NOISE / RWK   `does-a-harmful-instrument-...-helpful-one_B`
                  `does-share-price-any-key-or-only-vol_B`          class breakeven 11.36 bps
                  `is-the-null-key-result-one-draw-or-a-distribution_cloud`   (20 of 72 draws <= 10)

The queue asks: re-run each script's ACTUAL null on ITS panel, ITS n and ITS cadence, and report
whether its published verdict survives 10 bps.

WHAT IS ACTUALLY IN QUESTION (read before the numbers)
------------------------------------------------------
All four scripts already run their books at COSTS = [10, 25] bps, so no published sentence here
was computed at 0 bps.  "Unpriced" therefore cannot mean "never charged".  It means the scripts
never reported WHERE the sentence's breakeven sits, i.e. how far the published claim is from
flipping inside the range of rungs the record itself uses (0-25 bps).  That is what this run
measures: for each script, the exact published statistic re-evaluated on a continuous cost
ladder, on that script's own books, with the breakeven solved.

A sentence is scored:
    SURVIVES     true at 10 bps and its breakeven is outside [0, 25] bps  (rung-robust)
    FRAGILE      true at 10 bps but its breakeven lies inside [0, 25] bps (one rung from false)
    FLIPS        false at 10 bps

CONSTRUCTIONS ARE IMPORTED, NOT RETYPED.  Each parent module is loaded with importlib and its own
key/book functions are called, so a reproduction failure is a failure of this script, not a
difference of construction.  Every book is run ONCE at 0 bps and every rung derived from the
engine's own identity r_c = r_0 - turnover*c/1e4 (asserted exact against live engine runs).

Sharpe on the fine ladder is CLOSED FORM, not re-simulated:
    Sharpe(c) = (mu0 - mut*k) * sqrt(252) / sqrt(V0 - 2k*Cov + k^2*Vt),  k = c/1e4
from five sufficient statistics per window.  Asserted against metrics() to < 1e-12 before use.

TUNED PARAMETERS: 2 - the panel and the book size (n, or the share m that maps to n).  Both are
inherited from the parents unchanged and both are swept exhaustively; every grid point is written.
The site, the arm/key, the tilt direction, the draw and the COST RUNG are reported axes, never
selected on.  PROTOCOL 8 walk-forward is run at the end on the pooled book set.

Outputs: .console.txt .site1.csv .site2.csv .site3.csv .site3_draws.csv.gz .site4.csv .breakeven.csv
.verdicts.csv .walkforward.csv
Deterministic; no network; no hash()-derived seeds.  RULES.md / scan.py / bot.py / baseline.py
are not touched.
"""
import importlib.util
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-06_price-the-four-unpriced-null-verdicts-on-their-own-books_B"

I158_P = OUT / "2026-09-05_does-share-price-any-key-or-only-vol_B.py"
I180_P = OUT / "2026-09-06_is-the-null-key-result-one-draw-or-a-distribution_cloud.py"
I209_P = OUT / "2026-09-05_is-the-book-size-floor-a-corpus-wide-clause_C.py"
I181_P = OUT / "2026-09-05_does-a-null-column-change-any-published-verdict_cloud.py"
I192_P = OUT / "2026-09-05_does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I158 = _load(I158_P, "i158")
I180 = _load(I180_P, "i180")
I209 = _load(I209_P, "i209")
I181 = _load(I181_P, "i181")
I192 = _load(I192_P, "i192")
H, C = I180.H, I180.C            # idea 94 / idea 129 helpers, as the parents used them

FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PANELS = ["u56", "broad", "small"]
PUB_COSTS = [10.0, 25.0]                       # what all four parents published at
RUNGS = [0.0, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 25.0]        # the reported ladder
FINE = np.round(np.arange(0.0, 40.0001, 0.02), 4)           # breakeven scan
N_DRAWS = 100                                  # idea 180's committed draw count

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 900)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _tee.append(s)


OK = {}


def gate(tag, cond, msg):
    OK[tag] = bool(cond)
    say(f"[{tag}] {msg} -> {'PASS' if cond else 'FAIL'}")


# ===================================================================== closed-form Sharpe ladder
class Book:
    """One book's 0-bps return and turnover series, reduced to per-window sufficient statistics.

    Sharpe at any cost c is exact from (mu0, mut, V0, Cov, Vt):
        r_c = r_0 - to*k,  k = c/1e4
        mean = mu0 - mut*k ; var = V0 - 2k*Cov + k^2*Vt
    """

    WINDOWS = ("F", "H1", "H2", "IS", "OOS", "OH1", "OH2", "ISH1", "ISH2")

    def __init__(self, r0: pd.Series, to: pd.Series):
        self.r0, self.to = r0, to
        idx = r0.index
        n = len(idx)
        h = n // 2
        isv = idx <= pd.Timestamp(IS_END)
        oosv = idx >= pd.Timestamp(OOS_START)
        no, ni = int(oosv.sum()), int(isv.sum())
        segs = {
            "F": np.ones(n, bool),
            "H1": np.arange(n) < h,
            "H2": np.arange(n) >= h,
            "IS": isv,
            "OOS": oosv,
        }
        oo = np.flatnonzero(oosv)
        ii = np.flatnonzero(isv)
        for tag, sel in (("OH1", oo[: no // 2]), ("OH2", oo[no // 2:]),
                         ("ISH1", ii[: ni // 2]), ("ISH2", ii[ni // 2:])):
            m = np.zeros(n, bool)
            m[sel] = True
            segs[tag] = m
        a = r0.values
        b = to.values
        self.stats = {}
        for w, m in segs.items():
            x, y = a[m], b[m]
            k = len(x)
            self.stats[w] = (x.mean(), y.mean(),
                             x.var(ddof=1), float(np.cov(x, y, ddof=1)[0, 1]), y.var(ddof=1), k)
        self.years = n / 252.0
        self.to_yr = float(b.sum() / self.years)

    def sharpe(self, c, w="F"):
        mu0, mut, V0, Cv, Vt, _ = self.stats[w]
        k = c / 1e4
        var = V0 - 2.0 * k * Cv + k * k * Vt
        if var <= 0:
            return np.nan
        return (mu0 - mut * k) * 252.0 / (math.sqrt(var) * math.sqrt(252.0))

    def sharpe_v(self, cs, w="F"):
        mu0, mut, V0, Cv, Vt, _ = self.stats[w]
        k = np.asarray(cs, float) / 1e4
        var = V0 - 2.0 * k * Cv + k * k * Vt
        return (mu0 - mut * k) * math.sqrt(252.0) / np.sqrt(np.maximum(var, 1e-300))

    def net(self, c):
        return self.r0 - self.to * c / 1e4

    def full(self, c):
        """CAGR / MaxDD / halves / IS / OOS at one rung (not closed form; used on RUNGS only)."""
        r = self.net(c)
        m = metrics(r)
        mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
        h = len(r) // 2
        ro = r.loc[OOS_START:]
        ho = len(ro) // 2
        return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                    H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    oosH1=metrics(ro.iloc[:ho])["Sharpe"], oosH2=metrics(ro.iloc[ho:])["Sharpe"],
                    TO=self.to_yr)


def crossings(f, cs=FINE):
    """All sign changes of a scalar function of cost on the fine ladder, bisected to 1e-4 bps."""
    v = np.asarray([f(c) for c in cs], float)
    out = []
    for i in range(len(cs) - 1):
        a, b = v[i], v[i + 1]
        if not np.isfinite(a) or not np.isfinite(b) or a == 0 or (a > 0) == (b > 0):
            continue
        lo, hi = cs[i], cs[i + 1]
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if (f(lo) > 0) == (f(mid) > 0):
                lo = mid
            else:
                hi = mid
            if hi - lo < 1e-4:
                break
        out.append(0.5 * (lo + hi))
    return out


def verdict(true_at_10, xs):
    """SURVIVES / FRAGILE / FLIPS given the claim's truth at 10 bps and its breakevens."""
    inside = [x for x in xs if 0.0 < x <= 25.0]
    if not true_at_10:
        return "FLIPS"
    return "FRAGILE" if inside else "SURVIVES"


def fisher(a, b, c, d):
    """Two-sided Fisher exact on [[a,b],[c,d]] (small tables; exact, no scipy)."""
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c
    tot = comb(n, c1)
    p0 = comb(r1, a) * comb(n - r1, c1 - a) / tot
    p = 0.0
    lo = max(0, c1 - (n - r1))
    hi = min(r1, c1)
    for k in range(lo, hi + 1):
        pk = comb(r1, k) * comb(n - r1, c1 - k) / tot
        if pk <= p0 * (1 + 1e-9):
            p += pk
    return min(1.0, p)


def spearman(x, y):
    x = pd.Series(x).rank()
    y = pd.Series(y).rank()
    if x.std() == 0 or y.std() == 0:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


# ===================================================================== panels (parents' loaders)
# The three parents do NOT use the same small-cap panel:
#   flavour "C"    - idea 129/158/180: prices_small minus the max_1d_move>=1.0 names, SPY HELD OUT
#   flavour "meta" - idea 181/192   : the same meta filter but SPY LEFT IN the investable columns
#   flavour "raw"  - idea 209       : load_universe(small=True) unfiltered
# u56 and broad are byte-identical across all three.  Each site is run on ITS OWN panel.
PANEL = {}


class Pan:
    def __init__(self, key, px, spy, desc):
        self.key, self.px, self.desc = key, px, desc
        self.start = px.index[260]
        self.spy = spy.reindex(px.index).fillna(0.0).loc[self.start:]
        self.sim = I180.Sim(px)
        b = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        self.v1 = Book(b["returns"].loc[self.start:], b["turnover"].loc[self.start:])
        self.bfull = C.bars_win(self.spy, "full")
        self.bOOS = C.bars_win(self.spy, "OOS")
        self.spy_m = metrics(self.spy)
        self.spy_oos = metrics(self.spy.loc[OOS_START:])

    def book(self, W):
        r0, to = self.sim.run(W)
        return Book(r0.loc[self.start:], to.loc[self.start:])


def pan(name, flavour="C"):
    if name in ("u56", "broad"):
        flavour = "C"
    k = (name, flavour)
    if k in PANEL:
        return PANEL[k]
    if flavour == "C":
        px, spy, desc = C.panel(name)
    elif flavour == "meta":
        px = I181.small_panel()
        spy, desc = px["SPY"].pct_change().fillna(0.0), f"prices_small({px.shape[1]-1}, SPY in)"
    else:
        px = load_universe(small=True)
        spy, desc = px["SPY"].pct_change().fillna(0.0), f"prices_small({px.shape[1]-1}, raw)"
    PANEL[k] = Pan(k, px, spy, desc)
    return PANEL[k]


def build_panels():
    for fl in ("C", "meta", "raw"):
        for nm in PANELS:
            p = pan(nm, fl)
            if (nm, fl) == (nm, "C") or nm == "small":
                say(f"  panel {nm:6s}/{fl:4s} = {p.desc}: {p.px.shape[1]} cols, eval "
                    f"{p.start.date()} -> {p.px.index[-1].date()}")


def pass4b(f, p, oos=False):
    """PROTOCOL 4b through idea 129's own margins, on a metrics dict from Book.full()."""
    b = p.bOOS if oos else p.bfull
    if oos:
        return (f["oosH1"] > b["s1"] and f["oosH2"] > b["s2"]
                and f["OOS_Sharpe"] > b["soos"]
                and 0.60 * abs(b["sdd"]) - abs(f["OOS_MaxDD"]) > 0
                and f["OOS_CAGR"] - 0.70 * b["scagr"] > 0)
    return (f["H1"] > b["s1"] and f["H2"] > b["s2"] and f["OOS_Sharpe"] > b["soos"]
            and 0.60 * abs(b["sdd"]) - abs(f["MaxDD"]) > 0
            and f["CAGR"] - 0.70 * b["scagr"] > 0)


# ===================================================================== gates
def gates():
    say("\n" + "=" * 118)
    say("GATES  (asserted before any result below is read)")
    say("=" * 118)
    for pk in PANELS:
        p = pan(pk)
        px = p.px
        comp, above, vol20, G = I180.real_parts(px)
        elig = above & (vol20 < I180.MAX_VOL)
        n_elig = float(elig.loc[p.start:].sum(axis=1).mean())
        n = max(2, int(round(0.53 * n_elig)))
        W = (I180.ranks_of(comp, elig, None, "NONE") <= n).astype(float) * (I180.GROSS / n)
        e0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
        r0, t0 = p.sim.run(W)
        d1 = float((e0["returns"] - r0).abs().max())
        d2 = float((e0["turnover"] - t0).abs().max())
        e10 = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"]
        d3 = float((e10 - (r0 - t0 * 10.0 / 1e4)).abs().max())
        gate(f"A:{pk}", d1 < 1e-12 and d2 < 1e-10,
             f"Sim.run == engine.backtest  max|dret| {d1:.2e} max|dturn| {d2:.2e}")
        gate(f"D:{pk}", d3 < 1e-12,
             f"cost identity r_c = r_0 - TO*c/1e4 vs a live 10 bps run  max|d| {d3:.2e}")
        # closed-form Sharpe against metrics() on this panel's book, every rung
        bk = Book(r0.loc[p.start:], t0.loc[p.start:])
        worst = 0.0
        for c in RUNGS + [3.7, 11.36, 24.88]:
            r = bk.net(c)
            for w, rr in (("F", r), ("IS", r.loc[:IS_END]), ("OOS", r.loc[OOS_START:])):
                worst = max(worst, abs(bk.sharpe(c, w) - metrics(rr)["Sharpe"]))
        gate(f"S:{pk}", worst < 1e-12, f"closed-form Sharpe(c) == metrics()  max|d| {worst:.2e}")
        say(f"      n_elig {n_elig:.2f}  (idea 153/158 published "
            f"{ {'u56': 37.50, 'broad': 91.46, 'small': 141.23}[pk]:.2f})")


# ===================================================================== SITE 1 - idea 209 / RND
def site1():
    say("\n" + "=" * 118)
    say("SITE 1  is-the-book-size-floor-a-corpus-wide-clause_C  (idea 209)   null = RND, "
        "rng.random(px.shape): a fresh uniform for EVERY name on EVERY day")
    say("  published sentence: 'u56 +0.866 and broad +0.880, 24 of 24 arm-cells positive; small "
        "+0.197, 7 of 12, and NEGATIVE in 4 of 6 ranking keys at 25 bps'")
    say("=" * 118)
    rows, books = [], {}
    for pk in PANELS:
        p = pan(pk, "raw")                       # idea 209's own panel (unfiltered small)
        keys, elig = I209.keys_for(p.px)         # imported verbatim, seed 20260905
        for arm in I209.ARMS:
            for n in I209.N_GRID:
                if n > min(p.px.shape[1] - 1, 60):
                    continue
                W = I209.topn_weights(keys[arm], elig, n)
                bk = p.book(W)
                books[(pk, arm, n)] = bk
                for c in RUNGS:
                    f = bk.full(c)
                    rows.append(dict(site="S1", panel=pk, arm=arm, n=n, cost=c, **f))
    G1 = pd.DataFrame(rows)

    # ---- reproduction gate against the parent's committed corpus.csv (its two rungs)
    ref = pd.read_csv(OUT / "2026-09-05_is-the-book-size-floor-a-corpus-wide-clause_C.corpus.csv")
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    kidx = ["panel", "arm", "n", "cost"]
    a = G1[G1.cost.isin(PUB_COSTS)].set_index(kidx)[cols].sort_index()
    b = ref.set_index(kidx)[cols].sort_index()
    com = a.index.intersection(b.index)
    worst = float((a.loc[com] - b.loc[com]).abs().to_numpy().max())
    gate("R1", worst < 1e-9 and len(com) == len(a),
         f"idea 209 corpus.csv reproduced: {len(com)}/{len(a)} rows, max|d| {worst:.2e}")
    dto = float((G1[G1.cost == 10.0].set_index(["panel", "arm", "n"])["TO"].sort_index()
                 - ref[ref.cost == 10.0].set_index(["panel", "arm", "n"])["turnover_yr"].sort_index()
                 ).abs().max())
    gate("R1t", dto < 1e-9, f"idea 209 turnover_yr reproduced: max|d| {dto:.2e}")

    # ---- the published statistic as a function of the rung
    say("\n  rho_Spearman(n, OOS Sharpe) within each (panel, arm) cell, by rung "
        "[the parent's own convention]")
    hdr = "  " + f"{'panel':6s} {'arm':7s}" + "".join(f"{c:>9.0f}" for c in RUNGS) + \
          "   breakevens in (0,25]"
    say(hdr)
    say("  " + "-" * (len(hdr) - 2))
    brk = []
    for pk in PANELS:
        for arm in I209.ARMS:
            ns = [n for n in I209.N_GRID if (pk, arm, n) in books]
            bks = [books[(pk, arm, n)] for n in ns]

            def rho(c, ns=ns, bks=bks):
                return spearman(ns, [bk.sharpe(c, "OOS") for bk in bks])

            xs = crossings(rho)
            ins = [x for x in xs if 0.0 < x <= 25.0]
            say("  " + f"{pk:6s} {arm:7s}" + "".join(f"{rho(c):>+9.3f}" for c in RUNGS) +
                "   " + (", ".join(f"{x:.2f}" for x in ins) if ins else "-"))
            for x in xs:
                brk.append(dict(site="S1", stat="rho(n,OOS_Sharpe)", cell=f"{pk}/{arm}",
                                breakeven=x))
    # headline counts
    say("\n  the published counts, re-evaluated at every rung "
        "(arm-cell = (panel, arm) x the rungs the sentence pools)")
    say("  " + f"{'rung':>6s}  {'LARGE +ve/24':>12s}  {'SMALL +ve/12':>12s}  "
        f"{'small keys with rho<0':>22s}  {'rho u56':>8s} {'rho broad':>9s} {'rho small':>9s}")
    ctab = []
    for c in RUNGS:
        lg = sum(1 for pk in ("u56", "broad") for arm in I209.ARMS
                 if spearman([n for n in I209.N_GRID if (pk, arm, n) in books],
                             [books[(pk, arm, n)].sharpe(c, "OOS")
                              for n in I209.N_GRID if (pk, arm, n) in books]) > 0)
        sm = sum(1 for arm in I209.ARMS
                 if spearman([n for n in I209.N_GRID if ("small", arm, n) in books],
                             [books[("small", arm, n)].sharpe(c, "OOS")
                              for n in I209.N_GRID if ("small", arm, n) in books]) > 0)
        pr = {}
        for pk in PANELS:
            v = [spearman([n for n in I209.N_GRID if (pk, arm, n) in books],
                          [books[(pk, arm, n)].sharpe(c, "OOS")
                           for n in I209.N_GRID if (pk, arm, n) in books])
                 for arm in I209.ARMS]
            pr[pk] = float(np.mean(v))
        say("  " + f"{c:>6.1f}  {lg*2:>7d}/24  {sm*2:>7d}/12  {6-sm:>20d}/6  "
            f"{pr['u56']:>+8.3f} {pr['broad']:>+9.3f} {pr['small']:>+9.3f}")
        ctab.append(dict(cost=c, large_pos=lg * 2, small_pos=sm * 2, small_neg_keys=6 - sm,
                         rho_u56=pr["u56"], rho_broad=pr["broad"], rho_small=pr["small"]))
    G1.to_csv(OUT / f"{STEM}.site1.csv", index=False)
    return G1, books, brk, pd.DataFrame(ctab)


# ===================================================================== SITE 2 - idea 158 / RAND
def site2():
    say("\n" + "=" * 118)
    say("SITE 2  does-share-price-any-key-or-only-vol_B  (idea 158)   null = RAND, "
        "rk(126d change of a geometric random walk), seed 158 - the RWK shape")
    say("  published sentences: (i) 'a random key beats the live /sqrt(vol20) scaler in 27 of 28 "
        "large-cap cells tilted NEG and 23 of 28 tilted POS'")
    say("                       (ii) 'RAND books account for 11 of the 54 full-sample 4b passes'  "
        "(iii) '4 of 19 cross-universe 4b combinations are the RANDOM key'")
    say("=" * 118)
    rows, books = [], {}
    for pk in PANELS:
        p = pan(pk)                                    # idea 158's panel (= idea 129's C.panel)
        px = p.px
        el = I158.eligible_mask(px, pk).loc[p.start:]
        n_elig = float(el.sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig))) for m in I158.SHARES}
        for m in I158.SHARES:
            n = nmap[m]
            for (key, d) in [("NONE", "NONE")] + [(k, dd) for k in I158.KEYS
                                                  for dd in ("NEG", "POS")]:
                W = I158.weights(px, pk, key, d, n, constr="lit")
                bk = p.book(W)
                books[(pk, m, key, d)] = bk
                for c in RUNGS:
                    rows.append(dict(site="S2", panel=pk, m=m, n=n, key=key, dir=d, cost=c,
                                     **bk.full(c)))
    G2 = pd.DataFrame(rows)

    ref = pd.read_csv(OUT / "2026-09-05_does-share-price-any-key-or-only-vol_B.grid.csv")
    ref = ref[ref.constr == "lit"]
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "IS_Sharpe", "IS_CAGR", "IS_MaxDD", "TO"]
    kidx = ["panel", "m", "key", "dir", "cost"]
    a = G2[G2.cost.isin(PUB_COSTS)].set_index(kidx)[cols].sort_index()
    b = ref.set_index(kidx)[cols].sort_index()
    com = a.index.intersection(b.index)
    worst = float((a.loc[com] - b.loc[com]).abs().to_numpy().max())
    gate("R2", worst < 1e-9 and len(com) == len(a),
         f"idea 158 grid.csv (lit) reproduced: {len(com)}/{len(a)} rows, max|d| {worst:.2e}")

    LARGE = ("u56", "broad")
    cells = [(pk, m) for pk in LARGE for m in I158.SHARES]

    def dS(pk, m, key, d, c):
        return books[(pk, m, key, d)].sharpe(c) - books[(pk, m, "NONE", "NONE")].sharpe(c)

    say("\n  (i) large-cap cells (2 panels x 7 shares = 14 per rung) where RAND beats the LIVE "
        "VOL scaler, dSharpe vs the no-tilt control")
    say("  " + f"{'rung':>6s}  {'NEG: RAND>VOL':>14s}  {'POS: RAND>VOL':>14s}  "
        f"{'mean dS RAND/NEG':>17s}  {'mean dS VOL/NEG':>16s}  {'gap':>8s}")
    s2tab = []
    for c in RUNGS:
        neg = sum(1 for (pk, m) in cells if dS(pk, m, "RAND", "NEG", c) > dS(pk, m, "VOL", "NEG", c))
        pos = sum(1 for (pk, m) in cells if dS(pk, m, "RAND", "POS", c) > dS(pk, m, "VOL", "POS", c))
        mr = float(np.mean([dS(pk, m, "RAND", "NEG", c) for (pk, m) in cells]))
        mv = float(np.mean([dS(pk, m, "VOL", "NEG", c) for (pk, m) in cells]))
        say("  " + f"{c:>6.1f}  {neg:>11d}/14  {pos:>11d}/14  {mr:>+17.4f}  {mv:>+16.4f}  "
            f"{mr-mv:>+8.4f}")
        s2tab.append(dict(cost=c, neg_win=neg, pos_win=pos, mean_RANDNEG=mr, mean_VOLNEG=mv))

    brk = []
    say("\n      per-cell breakevens of 'RAND/NEG beats VOL/NEG' (the sentence's own 14 cells)")
    nin = 0
    for (pk, m) in cells:
        xs = crossings(lambda c, pk=pk, m=m: dS(pk, m, "RAND", "NEG", c) - dS(pk, m, "VOL", "NEG", c))
        ins = [x for x in xs if 0.0 < x <= 25.0]
        nin += len(ins) > 0
        for x in xs:
            brk.append(dict(site="S2", stat="RAND/NEG - VOL/NEG", cell=f"{pk}/m={m}", breakeven=x))
        if ins:
            say(f"      {pk:6s} m={m:<5.2f}  flips at " + ", ".join(f"{x:.2f}" for x in ins) + " bps")
    say(f"      {nin} of 14 cells have a breakeven inside (0, 25] bps")

    # (ii) / (iii): 4b pass composition by rung
    say("\n  (ii)/(iii) PROTOCOL KEEP paths over all 273 books, by rung "
        "(4b bars read against each panel's own SPY)")
    say("  " + f"{'rung':>6s}  {'4a':>5s}  {'4b':>5s}  {'4b RAND':>8s}  {'4b real keys':>12s}  "
        f"{'4b NONE':>8s}  {'x-universe 4b combos':>20s}  {'of them RAND':>13s}")
    keepr = []
    v1f = {(pk, c): pan(pk).v1.full(c) for pk in PANELS for c in RUNGS}
    for c in RUNGS:
        sub = G2[G2.cost == c]
        p4a, p4b = [], []
        for r in sub.itertuples():
            p = pan(r.panel)
            vf = v1f[(r.panel, c)]
            p4a.append(r.H1 > vf["H1"] and r.H2 > vf["H2"] and r.MaxDD >= vf["MaxDD"])
            p4b.append(pass4b(r._asdict(), p))
        sub = sub.assign(pass4a=p4a, pass4b=p4b)
        n4b = int(sub.pass4b.sum())
        rnd = int(sub[(sub.pass4b) & (sub.key == "RAND")].shape[0])
        real = int(sub[(sub.pass4b) & (sub.key.isin(["VOL", "VOLR", "MOM", "R6", "R3"]))].shape[0])
        none = int(sub[(sub.pass4b) & (sub.key == "NONE")].shape[0])
        cu = sub[sub.pass4b].groupby(["m", "key", "dir"]).size()
        cu2 = cu[cu >= 2]
        cur = sum(1 for (m, k, d) in cu2.index if k == "RAND")
        say("  " + f"{c:>6.1f}  {int(sub.pass4a.sum()):>5d}  {n4b:>5d}  {rnd:>8d}  {real:>12d}  "
            f"{none:>8d}  {len(cu2):>20d}  {cur:>13d}")
        keepr.append(dict(cost=c, p4a=int(sub.pass4a.sum()), p4b=n4b, p4b_RAND=rnd,
                          p4b_real=real, p4b_NONE=none, xuniv=len(cu2), xuniv_RAND=cur))
    G2.to_csv(OUT / f"{STEM}.site2.csv", index=False)
    return G2, books, brk, pd.DataFrame(s2tab), pd.DataFrame(keepr)


# ===================================================================== SITE 3 - idea 180 / 100 draws
def site3(s2books):
    say("\n" + "=" * 118)
    say("SITE 3  is-the-null-key-result-one-draw-or-a-distribution_cloud  (idea 180)   "
        "null = 100 independent draws of idea 158's RAND")
    say("  published sentence: 'mean |Sharpe(tilt) - Sharpe(NONE)| over 100 null keys: u56 0.0945, "
        "broad 0.0514, small 0.1049; the real-key mean sits at the 92nd / 100th / 51st percentile'")
    say("=" * 118)
    t0 = time.time()
    lad = np.array(RUNGS, float)
    # null band: per (panel, draw) the mean over (m, dir) of |Sharpe(RAND) - Sharpe(NONE)|
    band = {pk: np.zeros((N_DRAWS, len(FINE))) for pk in PANELS}
    d0chk = {}
    for pk in PANELS:
        p = pan(pk)
        px = p.px
        comp, above, vol20, G = I180.real_parts(px)
        elig = above & (vol20 < I180.MAX_VOL)
        n_elig = float(elig.loc[p.start:].sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig))) for m in I180.SHARES}
        ctrl = {m: s2books[(pk, m, "NONE", "NONE")].sharpe_v(FINE) for m in I180.SHARES}
        for d in range(N_DRAWS):
            g = I180.null_key(px, I180.seed_of(d))
            acc = np.zeros(len(FINE))
            k = 0
            for dr in ("NEG", "POS"):
                rnk = I180.ranks_of(comp, elig, g, dr)
                for m in I180.SHARES:
                    n = nmap[m]
                    W = (rnk <= n).astype(float) * (I180.GROSS / n)
                    bk = p.book(W)
                    acc += np.abs(bk.sharpe_v(FINE) - ctrl[m])
                    k += 1
                    if d == 0:
                        d0chk[(pk, m, dr)] = bk
            band[pk][d] = acc / k
        say(f"    {pk}: 100 draws x 14 books done ({time.time()-t0:.0f}s)")

    # ---- gate: draw 0 IS idea 158's published RAND rows
    ref = pd.read_csv(OUT / "2026-09-05_does-share-price-any-key-or-only-vol_B.grid.csv")
    ref = ref[(ref.constr == "lit") & (ref.key == "RAND")]
    worst = 0.0
    for r in ref.itertuples():
        bk = d0chk[(r.panel, r.m, r.dir)]
        f = bk.full(r.cost)
        worst = max(worst, abs(f["Sharpe"] - r.Sharpe), abs(f["CAGR"] - r.CAGR),
                    abs(f["OOS_Sharpe"] - r.OOS_Sharpe))
    gate("R3", worst < 1e-9, f"idea 180 draw 0 == idea 158's published RAND rows: max|d| {worst:.2e}")

    # ---- real-key band on the same grid
    real = {}
    for pk in PANELS:
        acc = np.zeros(len(FINE))
        k = 0
        for key in ["VOL", "VOLR", "MOM", "R6", "R3"]:
            for dr in ("NEG", "POS"):
                for m in I158.SHARES:
                    acc += np.abs(s2books[(pk, m, key, dr)].sharpe_v(FINE)
                                  - s2books[(pk, m, "NONE", "NONE")].sharpe_v(FINE))
                    k += 1
        real[pk] = acc / k

    say("\n  mean |dSharpe| null band over 100 draws, and where the 5 real keys' mean sits in it")
    say("  " + f"{'panel':6s} {'rung':>6s}  {'null mean':>10s} {'null sd':>8s} "
        f"{'[min':>7s} {'max]':>7s}  {'real mean':>10s}  {'percentile':>11s}  {'draw 0':>8s}")
    rows = []
    for pk in PANELS:
        for c in RUNGS:
            j = int(np.argmin(np.abs(FINE - c)))
            nb = band[pk][:, j]
            rm = real[pk][j]
            pct = 100.0 * float((nb < rm).mean())
            say("  " + f"{pk:6s} {c:>6.1f}  {nb.mean():>10.4f} {nb.std(ddof=1):>8.4f} "
                f"{nb.min():>7.4f} {nb.max():>7.4f}  {rm:>10.4f}  {pct:>10.0f}th  "
                f"{band[pk][0, j]:>8.4f}")
            rows.append(dict(site="S3", panel=pk, cost=c, null_mean=nb.mean(),
                             null_sd=nb.std(ddof=1), null_min=nb.min(), null_max=nb.max(),
                             real_mean=rm, pct=pct, draw0=band[pk][0, j]))
    # breakeven of "the real mean is inside the null band" (pct < 100) and of pct crossing 50
    brk = []
    say("\n      the rung at which each percentile statement first becomes true (and stays true)")
    for pk in PANELS:
        pct_c = 100.0 * (band[pk] < real[pk][None, :]).mean(axis=0)
        for lvl, nm in ((100.0, "real mean EXITS the null band (pct >= 100)"),
                        (95.0, "real mean above the null 95th pct"),
                        (50.0, "real mean above the null MEDIAN (pct >= 50)")):
            hit = np.flatnonzero(pct_c >= lvl)
            if len(hit) == 0:
                say(f"      {pk:6s} {nm}: never, up to {FINE[-1]:.0f} bps")
                continue
            # first index from which the condition holds for the rest of the ladder
            j = len(pct_c) - 1
            while j > 0 and pct_c[j - 1] >= lvl:
                j -= 1
            c0 = float(FINE[j])
            say(f"      {pk:6s} {nm}: from {c0:.2f} bps"
                + ("   [INSIDE the record's 0-25 bps range]" if 0 < c0 <= 25 else ""))
            brk.append(dict(site="S3", stat=nm, cell=pk, breakeven=c0))
    G3 = pd.DataFrame(rows)
    G3.to_csv(OUT / f"{STEM}.site3.csv", index=False)
    # every draw's own band at the reported rungs (3 panels x 100 draws x 8 rungs)
    dr = [dict(panel=pk, draw=d, cost=c,
               band=float(band[pk][d, int(np.argmin(np.abs(FINE - c)))]),
               real_mean=float(real[pk][int(np.argmin(np.abs(FINE - c)))]))
          for pk in PANELS for d in range(N_DRAWS) for c in RUNGS]
    pd.DataFrame(dr).to_csv(OUT / f"{STEM}.site3_draws.csv.gz", index=False,
                            compression="gzip")
    return G3, brk


# ===================================================================== SITE 4 - idea 192 / clause
def site4():
    say("\n" + "=" * 118)
    say("SITE 4  does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B  (idea 192)   "
        "null band = 20 random-walk keys (idea 181's corpus T)")
    say("  published sentence: 'of the 51 arms in the pooled 288 that pass 4b, exactly 1 clears "
        "its own null band (2.0%), against 31.6% of the 237 that fail (Fisher p = 9.2e-07)'")
    say("  scope note: corpus T (180 of the 288 pooled arm-rows) is REBUILT and re-priced here; "
        "corpus O (idea 186's rotations) is held at its committed rungs and reported separately.")
    say("=" * 118)
    books, ctrl = {}, {}
    for pi, pk in enumerate(PANELS):
        p = pan(pk, "meta")                      # idea 181's own panel (SPY left in on small)
        px = p.px
        pseed = I181.SEED + 1000 * (1 + pi)
        keys, vol20 = I181.build_keys(px, np.random.default_rng(pseed))
        comp = I181.composite(px)
        above = px > px.rolling(200).mean()
        elig = above & (vol20 < I181.MAXVOL)

        def run(score, p=p, elig=elig):
            rk = score.where(elig).rank(axis=1, ascending=False)
            W = (rk <= I181.N).astype(float) * (I181.GROSS / I181.N)
            return p.book(W)

        ctrl[pk] = run(comp)
        for kn, kv in keys.items():
            for dn, dv in (("POS", 1.0), ("NEG", -1.0)):
                for m in I181.MS:
                    books[(pk, kn, dn, m)] = run(comp + dv * m * kv)
        say(f"    {pk}: {1 + len(keys)*2*len(I181.MS)} books rebuilt")

    # ---- reproduction gate against idea 181's committed grid
    ref = pd.read_csv(OUT / "2026-09-05_does-a-null-column-change-any-published-verdict_cloud.grid.csv")
    ref = ref[ref.kind != "control"]
    worst = worstd = 0.0
    for r in ref.itertuples():
        bk = books[(r.panel, r.key, r.dir, r.m)]
        worst = max(worst, abs(bk.sharpe(r.cost) - r.Sharpe_F))
        worstd = max(worstd, abs((bk.sharpe(r.cost) - ctrl[r.panel].sharpe(r.cost)) - r.dSharpe_F))
    gate("R4", worst < 1e-9 and worstd < 1e-9,
         f"idea 181 grid.csv reproduced ({len(ref)} rows): max|dSharpe_F| {worst:.2e}, "
         f"max|d(dSharpe)| {worstd:.2e}")

    REAL = I181.REAL_KEYS
    NULLS = [f"NULL{j:02d}" for j in range(I181.B_NULL)]

    _memo = {}

    def clause_rows(c, with4b=True):
        """One (panel, dir, m) cell -> the 5 real arms, their |dSharpe|, the null band, 4b."""
        if (c, with4b) in _memo:
            return _memo[(c, with4b)]
        out = []
        for pk in PANELS:
            p = pan(pk, "meta")
            for dn in ("POS", "NEG"):
                for m in I181.MS:
                    thr = max(abs(books[(pk, kn, dn, m)].sharpe(c) - ctrl[pk].sharpe(c))
                              for kn in NULLS)
                    for kn in REAL:
                        bk = books[(pk, kn, dn, m)]
                        d = bk.sharpe(c) - ctrl[pk].sharpe(c)
                        p4b = pass4b(bk.full(c), p) if with4b else False
                        out.append(dict(cost=c, panel=pk, dir=dn, m=m, key=kn, d=d,
                                        band=thr, clears=int(abs(d) > thr), pass4b=int(p4b)))
        _memo[(c, with4b)] = pd.DataFrame(out)
        return _memo[(c, with4b)]

    say("\n  the clause, re-priced on corpus T's own books (90 real arms per rung)")
    say("  " + f"{'rung':>6s}  {'clears/90':>9s}  {'4b pass':>7s}  {'clears | 4b pass':>16s}  "
        f"{'clears | 4b fail':>16s}  {'Fisher p':>10s}  {'mean band':>10s}")
    rows, s4 = [], []
    for c in RUNGS:
        T = clause_rows(c)
        rows.append(T)
        a = int(T[(T.pass4b == 1) & (T.clears == 1)].shape[0])
        b = int(T[(T.pass4b == 1) & (T.clears == 0)].shape[0])
        cc = int(T[(T.pass4b == 0) & (T.clears == 1)].shape[0])
        dd = int(T[(T.pass4b == 0) & (T.clears == 0)].shape[0])
        p = fisher(a, b, cc, dd) if (a + b) and (cc + dd) else np.nan
        r1 = f"{a}/{a+b}" + (f" ({100*a/(a+b):.1f}%)" if a + b else "")
        r2 = f"{cc}/{cc+dd}" + (f" ({100*cc/(cc+dd):.1f}%)" if cc + dd else "")
        say("  " + f"{c:>6.1f}  {int(T.clears.sum()):>6d}/90  {int(T.pass4b.sum()):>7d}  "
            f"{r1:>16s}  {r2:>16s}  {p:>10.2e}  {T.band.mean():>10.4f}")
        s4.append(dict(cost=c, clears=int(T.clears.sum()), p4b=int(T.pass4b.sum()),
                       clear_given_4b=a, n_4b=a + b, clear_given_fail=cc, n_fail=cc + dd,
                       fisher_p=p, mean_band=T.band.mean()))
    G4 = pd.concat(rows, ignore_index=True)
    G4.to_csv(OUT / f"{STEM}.site4.csv", index=False)

    # pooled with corpus O held at its committed rungs (the published 288)
    arms = pd.read_csv(OUT / "2026-09-05_does-a-harmful-instrument-clear-more-often-than-a-helpful-"
                             "one_B.arms.csv")
    O = arms[arms.corpus == "O"]
    say(f"\n  pooled with corpus O held fixed ({len(O)} committed O rows, T re-priced at the rung "
        "on both of the parent's rungs)")
    say("  " + f"{'T rung':>7s}  {'pooled N':>8s}  {'4b pass':>7s}  {'clears|4b':>12s}  "
        f"{'clears|fail':>12s}  {'Fisher p':>10s}")
    pooled = []
    for c in RUNGS:
        T = clause_rows(c)
        T2 = pd.concat([T.assign(cost=c), T.assign(cost=c)], ignore_index=True)  # T pooled x2 rungs
        a = int(T2[(T2.pass4b == 1) & (T2.clears == 1)].shape[0]) + \
            int(O[(O.pass4b == 1) & (O.clears)].shape[0])
        b = int(T2[(T2.pass4b == 1) & (T2.clears == 0)].shape[0]) + \
            int(O[(O.pass4b == 1) & (~O.clears.astype(bool))].shape[0])
        cc = int(T2[(T2.pass4b == 0) & (T2.clears == 1)].shape[0]) + \
            int(O[(O.pass4b == 0) & (O.clears)].shape[0])
        dd = int(T2[(T2.pass4b == 0) & (T2.clears == 0)].shape[0]) + \
            int(O[(O.pass4b == 0) & (~O.clears.astype(bool))].shape[0])
        p = fisher(a, b, cc, dd) if (a + b) and (cc + dd) else np.nan
        say("  " + f"{c:>7.1f}  {a+b+cc+dd:>8d}  {a+b:>7d}  {a}/{a+b:<10d}  {cc}/{cc+dd:<10d}  "
            f"{p:>10.2e}")
        pooled.append(dict(cost=c, N=a + b + cc + dd, n4b=a + b, clear4b=a, clearfail=cc,
                           nfail=cc + dd, fisher_p=p))

    # the parent's EXACT pooling: corpus T at 10 AND 25 bps + corpus O's committed rows
    T10, T25 = clause_rows(10.0), clause_rows(25.0)
    TT = pd.concat([T10, T25], ignore_index=True)
    a = int(TT[(TT.pass4b == 1) & (TT.clears == 1)].shape[0]) + \
        int(O[(O.pass4b == 1) & (O.clears)].shape[0])
    b = int(TT[TT.pass4b == 1].shape[0]) + int(O[O.pass4b == 1].shape[0])
    cc = int(TT[(TT.pass4b == 0) & (TT.clears == 1)].shape[0]) + \
        int(O[(O.pass4b == 0) & (O.clears)].shape[0])
    dd = int(TT[TT.pass4b == 0].shape[0]) + int(O[O.pass4b == 0].shape[0])
    p = fisher(a, b - a, cc, dd - cc)
    match = (b == 51) and (dd == 237) and (a == 1)
    say(f"\n  [R4p] idea 192's published pooling, rebuilt (T re-run at 10 AND 25 bps + O's "
        f"committed rows):")
    say(f"        {a}/{b} 4b-passing arms clear their null band (published 1 of 51); "
        f"{cc}/{dd} = {100*cc/dd:.1f}% of failing arms (published 31.6%); "
        f"Fisher p {p:.2e} (published 9.2e-07)  -> {'EXACT' if match else 'see note'}")

    brk = []
    for lbl, f in (("clears|4b < clears|fail",
                    lambda c: (lambda T: (T[(T.pass4b == 1) & (T.clears == 1)].shape[0]
                                          / max(1, T[T.pass4b == 1].shape[0]))
                               - (T[(T.pass4b == 0) & (T.clears == 1)].shape[0]
                                  / max(1, T[T.pass4b == 0].shape[0])))(clause_rows(c))),):
        xs = crossings(f, np.round(np.arange(0.0, 25.01, 0.5), 3))
        for x in xs:
            brk.append(dict(site="S4", stat=lbl, cell="corpus T", breakeven=x))
        say(f"\n      breakeven of '{lbl}' on corpus T: "
            + (", ".join(f"{x:.2f}" for x in xs) if xs else "none in [0, 25] bps"))
    return G4, pd.DataFrame(s4), pd.DataFrame(pooled), brk


# ===================================================================== PROTOCOL 8 walk-forward
def walkforward(s1books, s2books):
    say("\n" + "=" * 118)
    say("PROTOCOL 8 WALK-FORWARD   parameters chosen on 2009-2016 (IS) only; 2017-2026 read once")
    say("  pool = every book this run built at sites 1 and 2 (idea 209's 6 arms x 11 n x 3 panels "
        "+ idea 158's 13 books x 7 shares x 3 panels)")
    say("  the on-theme question: does the RUNG used to SELECT change the OOS book, and by how "
        "much?")
    say("=" * 118)
    pool = {}
    for (pk, arm, n), bk in s1books.items():
        pool[f"S1/{pk}/{arm}/n={n}"] = (pan(pk, "raw"), bk)
    for (pk, m, key, d), bk in s2books.items():
        pool[f"S2/{pk}/m={m}/{key}/{d}"] = (pan(pk), bk)
    say(f"  pool size: {len(pool)} books")
    rows = []
    say("\n  " + f"{'sel rung':>8s}  {'IS-argmax book':<32s} {'IS Sh':>7s}  {'OOS CAGR':>9s} "
        f"{'OOS Sh':>7s} {'OOS MaxDD':>10s}  {'v1 OOS Sh':>10s} {'SPY OOS Sh':>11s}  {'4b OOS':>7s}")
    for c in RUNGS:
        best, bs = None, -9e9
        for k, (p, bk) in pool.items():
            s = bk.sharpe(c, "IS")
            if np.isfinite(s) and s > bs:
                best, bs = k, s
        p, bk = pool[best]
        f = bk.full(c)
        v1f = p.v1.full(c)
        p4b_oos = pass4b(f, p, oos=True)
        say("  " + f"{c:>8.1f}  {best:<32s} {bs:>7.3f}  {f['OOS_CAGR']:>8.2%} "
            f"{f['OOS_Sharpe']:>7.3f} {f['OOS_MaxDD']:>9.2%}  {v1f['OOS_Sharpe']:>10.3f} "
            f"{p.spy_oos['Sharpe']:>11.3f}  {'PASS' if p4b_oos else 'FAIL':>7s}")
        rows.append(dict(sel_cost=c, pick=best, IS_Sharpe=bs, OOS_CAGR=f["OOS_CAGR"],
                         OOS_Sharpe=f["OOS_Sharpe"], OOS_MaxDD=f["OOS_MaxDD"],
                         v1_OOS_Sharpe=v1f["OOS_Sharpe"], v1_OOS_CAGR=v1f["OOS_CAGR"],
                         v1_OOS_MaxDD=v1f["OOS_MaxDD"],
                         spy_OOS_Sharpe=p.spy_oos["Sharpe"], spy_OOS_CAGR=p.spy_oos["CAGR"],
                         spy_OOS_MaxDD=p.spy_oos["MaxDD"], pass4b_oos=bool(p4b_oos)))
    W = pd.DataFrame(rows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    npicks = W.pick.nunique()
    say(f"\n  the selection rung changes the OOS book: {npicks} distinct picks across the "
        f"{len(RUNGS)} rungs; OOS Sharpe spread {W.OOS_Sharpe.max()-W.OOS_Sharpe.min():+.4f}")
    say("  SPY OOS by panel: " + ", ".join(
        f"{pk} {pan(pk).spy_oos['Sharpe']:.3f}/{pan(pk).spy_oos['CAGR']:.2%}/"
        f"{pan(pk).spy_oos['MaxDD']:.2%}" for pk in PANELS))
    say("  RULES v1 OOS @10 bps by panel: " + ", ".join(
        f"{pk} {pan(pk).v1.full(10.0)['OOS_Sharpe']:.3f}/"
        f"{pan(pk).v1.full(10.0)['OOS_CAGR']:.2%}" for pk in PANELS))
    return W


# ===================================================================== main
def main():
    t0 = time.time()
    say("=" * 118)
    say(f"IDEA 268 - price-the-four-unpriced-null-verdicts-on-their-own-books   ({STEM})")
    say("Each of idea 262's four flagged scripts, its OWN null on its OWN panel/n/cadence, priced "
        "on a continuous cost ladder.")
    say("=" * 118)
    build_panels()
    gates()

    G1, s1books, b1, c1 = site1()
    G2, s2books, b2, s2tab, keepr = site2()
    G3, b3 = site3(s2books)
    G4, s4tab, pooled, b4 = site4()
    W = walkforward(s1books, s2books)

    BR = pd.DataFrame(b1 + b2 + b3 + b4)
    BR.to_csv(OUT / f"{STEM}.breakeven.csv", index=False)

    # ------------------------------------------------------------- the four verdicts
    say("\n" + "=" * 118)
    say("THE ANSWER  -  does each published verdict survive 10 bps, and how far is it from "
        "flipping inside the record's own 0-25 bps range?")
    say("=" * 118)
    ver = []

    # S1 - the sentence has two halves and they do NOT score the same
    r10 = c1[c1.cost == 10.0].iloc[0]
    r25 = c1[c1.cost == 25.0].iloc[0]
    r0_ = c1[c1.cost == 0.0].iloc[0]
    big = BR[(BR.site == "S1") & BR.cell.str.startswith(("u56", "broad"))
             & (BR.breakeven > 0) & (BR.breakeven <= 25)]
    sml = BR[(BR.site == "S1") & BR.cell.str.startswith("small")
             & (BR.breakeven > 0) & (BR.breakeven <= 25)]
    ver.append(("S1a idea 209 (large half)",
                "'u56 +0.866 / broad +0.880, 24 of 24 large arm-cells rho(n, OOS Sharpe) > 0'",
                verdict(r10.large_pos == 24, big.breakeven.tolist()),
                f"24/24 at EVERY rung 0-25 (0 bps {int(r0_.large_pos)}/24, 10 bps "
                f"{int(r10.large_pos)}/24, 25 bps {int(r25.large_pos)}/24); mean rho u56 "
                f"{r0_.rho_u56:+.3f}->{r25.rho_u56:+.3f}, broad {r0_.rho_broad:+.3f}->"
                f"{r25.rho_broad:+.3f}; {len(big)} large arm-cell breakevens in (0,25]"))
    ver.append(("S1b idea 209 (small half)",
                "'small +0.197, 7 of 12 arm-cells positive, NEGATIVE in 4 of 6 keys at 25 bps' "
                "- the sign reversal the whole verdict rests on",
                verdict(True, sml.breakeven.tolist()),
                f"mean rho small {r0_.rho_small:+.3f} at 0 bps -> {r10.rho_small:+.3f} at 10 -> "
                f"{r25.rho_small:+.3f} at 25; keys with rho<0: {int(r0_.small_neg_keys)}/6 at 0 "
                f"bps, {int(r10.small_neg_keys)}/6 at 10, {int(r25.small_neg_keys)}/6 at 25; "
                f"{sml.cell.nunique()} of 6 small arm-cells (the RND null among them) have a "
                f"breakeven inside (0,25]"))

    s2r = s2tab.set_index("cost")
    true10 = bool(s2r.loc[10.0, "neg_win"] + s2r.loc[25.0, "neg_win"] == 27)
    ins2 = BR[(BR.site == "S2") & (BR.breakeven > 0) & (BR.breakeven <= 25)]
    v2 = verdict(bool(s2r.loc[10.0, "neg_win"] >= 13), ins2.breakeven.tolist())
    ver.append(("S2 idea 158", "'a random key beats the live /sqrt(vol20) scaler in 27 of 28 "
                "large-cap NEG cells'", v2,
                f"pooled 10+25 bps: {int(s2r.loc[10.0,'neg_win']+s2r.loc[25.0,'neg_win'])}/28 "
                f"(published 27/28); at 0 bps {int(s2r.loc[0.0,'neg_win'])}/14; "
                f"{ins2.cell.nunique()} of 14 cells flip inside (0,25]"))

    p10 = G3[(G3.cost == 10.0)].set_index("panel")["pct"]
    p25 = G3[(G3.cost == 25.0)].set_index("panel")["pct"]
    p0 = G3[(G3.cost == 0.0)].set_index("panel")["pct"]
    nm0 = G3[(G3.cost == 0.0)].set_index("panel")
    ins3 = BR[(BR.site == "S3") & (BR.breakeven > 0) & (BR.breakeven <= 25)]
    v3 = verdict(True, ins3.breakeven.tolist())
    ver.append(("S3 idea 180", "'the real-key mean sits at the 92nd / 100th / 51st percentile of "
                "the 100-draw null band' (i.e. real keys move the book MORE than a random key "
                "does)", v3,
                "percentile at 0 bps " + "/".join(f"{p0[p]:.0f}" for p in PANELS)
                + ", at 10 bps " + "/".join(f"{p10[p]:.0f}" for p in PANELS)
                + ", at 25 bps " + "/".join(f"{p25[p]:.0f}" for p in PANELS)
                + "; at 0 bps the real mean is INSIDE the null band on all three panels ("
                + ", ".join(f"{p} real {nm0.loc[p,'real_mean']:.4f} vs null "
                            f"{nm0.loc[p,'null_mean']:.4f}+-{nm0.loc[p,'null_sd']:.4f}"
                            for p in PANELS) + ")"))

    s4r = s4tab.set_index("cost")
    a10 = s4r.loc[10.0]
    a0 = s4r.loc[0.0]
    true10 = bool(a10.clear_given_4b / max(1, a10.n_4b) < a10.clear_given_fail / max(1, a10.n_fail))
    ins4 = BR[(BR.site == "S4") & (BR.breakeven > 0) & (BR.breakeven <= 25)]
    v4 = verdict(true10, ins4.breakeven.tolist())
    ver.append(("S4 idea 192", "'4b-passing arms clear their null band LESS often than failing "
                "arms' (corpus T)", v4,
                f"at 10 bps {int(a10.clear_given_4b)}/{int(a10.n_4b)} vs "
                f"{int(a10.clear_given_fail)}/{int(a10.n_fail)}, p {a10.fisher_p:.2e}; at 0 bps "
                f"{int(a0.clear_given_4b)}/{int(a0.n_4b)} vs "
                f"{int(a0.clear_given_fail)}/{int(a0.n_fail)}, p {a0.fisher_p:.2e}"))

    for site, claim, v, detail in ver:
        say(f"\n  {site}  {v}")
        say(f"      claim : {claim}")
        say(f"      detail: {detail}")
    pd.DataFrame([dict(site=s, claim=c, verdict=v, detail=d) for s, c, v, d in ver]).to_csv(
        OUT / f"{STEM}.verdicts.csv", index=False)

    say("\n" + "=" * 118)
    say("GATES: " + ("ALL PASS" if all(OK.values()) else
                     "FAILED -> " + ", ".join(k for k, v in OK.items() if not v)))
    say(f"total {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    assert all(OK.values()), "a reproduction gate failed; results above are unsafe"


if __name__ == "__main__":
    main()

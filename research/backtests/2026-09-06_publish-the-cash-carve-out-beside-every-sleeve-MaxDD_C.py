#!/usr/bin/env python3
"""QUEUE idea 213 — publish-the-cash-carve-out-beside-every-sleeve-MaxDD  (lane C, 2026-09-06).

QUESTION (verbatim from QUEUE.md idea 213)
    "idea 190 found a cash carve-out at matched f reproduces 98.4% of the static sleeve's
     drawdown gain (93.7/94.8/104.6% at f=0.10/0.20/0.50) while contributing -0.0017 of
     Sharpe.  527 LEADERBOARD rows mention a sleeve.  Back-fill the matched-f cash control
     wherever the row is recoverable and report how many sleeve drawdown claims survive it.
     Max 2 params."

WHAT A "SLEEVE DRAWDOWN CLAIM" IS, AND WHAT SURVIVING IT MEANS
    A sleeve arm is any published book of the form  (1-f) x EQUITY + f x SLEEVE  (with or
    without a re-gross), whose own f=0 arm is published beside it in the same grid.  The
    arm makes a DRAWDOWN CLAIM iff its MaxDD is shallower than that f=0 control's, i.e.
    dD_sleeve = |MaxDD_base| - |MaxDD_sleeve| > 0.
    The control the record never published is idea 190's:
        CASH-f  =  (1-f) x (the arm's own f=0 weights), NOT rescaled.
    It holds the same fraction f out of the equity book and puts it in cash — no asset
    choice, no timing, no signal, zero incremental turnover on the sleeve leg.  Its gain is
        dD_cash = |MaxDD_base| - |MaxDD_cash|,   retention = dD_cash / dD_sleeve.
    A claim SURVIVES at bar b iff dD_sleeve > 0 AND retention < b.  Three bars are reported
    for every row (b = 1.00 "the sleeve is merely better than cash", 0.75, 0.50 "cash
    reproduces less than half"); no bar is chosen after the fact.

    SECOND CONTROL, because CASH-f is not the only reading.  For a GROSS-MATCHED sleeve arm
    (the blend rescaled back to the equity book's own gross) the sleeve cannot be a
    de-grossing in disguise — the exposure is identical by construction — yet CASH-f still
    de-grosses.  So CASH-GM is also run: m x (f=0 weights) with m set to the SLEEVE arm's
    own realised mean gross over its rebalance dates divided by the base's (idea 135's
    matched-mean-gross control).  Under a matched-gross convention CASH-GM degenerates to
    the base and its retention is ~0 by construction; that degeneracy is the finding for
    those rows, and is reported rather than hidden.  Reading the two together:
        CASH-f retains the gain  -> the claim is "hold less equity", available for free;
        CASH-GM retains it too   -> the claim is an exposure claim outright;
        neither retains it       -> the claim is about the sleeve ASSETS, and survives.

TUNED PARAMETERS — exactly two, both swept and fully reported, neither selected on:
    1. the cash-control convention: {CASH-f, CASH-GM}
    2. the survival bar b in {1.00, 0.75, 0.50}
    Everything else (panels, books, sleeve sets, f, cost rungs, conventions) is inherited
    from the parent rows being back-filled and is never re-chosen here.

CORPUS — every sleeve claim recoverable from a committed grid CSV
    A  idea 190   2026-09-05_is-the-conditional-sleeve-anything-at-all_B    (the parent; it
                  published CASH-f itself, so it is the reproduction anchor for the control)
    B  idea 134   2026-09-05_sleeve-f-that-clears-the-floor_cloud           (ungated control
                  arm only; the 16 overlay arms change the base and are declared out of scope)
    C  idea 105   2026-09-05_which-asset-carries-S4_C
    D1 idea 103   2026-09-05_sleeve-with-a-real-diversifier_cloud
    D2 idea 103   2026-09-05_sleeve-with-a-real-diversifier_B               (the same corpus
                  run in a second lane; the overlap is counted once and reported)
    E  idea 18    2026-09-04_ensemble-plus-momentum_C
    F  idea 106   2026-09-05_sleeve-G-is-2013_cloud
    G  idea 15    2026-09-04_crypto-sleeve_C            (cap-funded, not f-funded: the matched
                  f is the arm's own REALISED mean sleeve share of gross, f_hat, measured on
                  the rebalance dates and printed on every row)
    H  idea 14    2026-09-04_rsi2-sleeve_cloud          (a STRATEGY sleeve; f is explicit and
                  the sleeve sits in cash whenever no name signals, so CASH-f is the exact
                  degenerate case of the sleeve itself)
    Every parent's own published MaxDD/Sharpe/CAGR is re-derived here before any new number
    is read; a parent that does not reproduce is dropped from the corpus, not patched.

    COVERAGE IS REPORTED, NOT ASSUMED.  The census counts every LEADERBOARD row mentioning a
    sleeve, attributes it to its script, and states which are covered by an adapter, which
    are recoverable-in-principle but not covered, and which committed no grid CSV at all.

WALK-FORWARD (PROTOCOL rule 8, mandatory; selectors fixed in writing before any OOS read)
    In every (parent, panel, book, conv, cost) cell the record's own selector — argmax IS
    Sharpe on 2009-01..2016-12 over that cell's sleeve arms — picks (f*, sleeve*).  Then
    2017-01..2026 is read ONCE for four arms: SLEEVE(f*), CASH-f*, CASH-GM(f*) and BASE
    (do-nothing), against RULES v1 and SPY on the same panel.  Reported: OOS CAGR / Sharpe /
    MaxDD for each, the paired SLEEVE-minus-CASH differences with t-stats, and the share of
    cells in which the sleeve's OOS drawdown advantage over its base survives the cash arm.

PRE-REGISTERED PREDICTIONS (written before any number in the back-fill was read)
    P1  Median CASH-f retention over the whole corpus is >= 0.75 (idea 190 got 0.984 on its
        own 36 points; if that generalises, most of the record's sleeve drawdown is exposure).
    P2  retention >= 1.00 (cash strictly beats the sleeve) is MORE common under the natural
        convention than under the gross-matched one.
    P3  Retention increases with f.
    P4  Of the sleeve arms that pass 4b's drawdown cap, at least half have their own CASH-f
        control passing that cap too.
    P5  Rule 8: |OOS MaxDD(SLEEVE) - OOS MaxDD(CASH-f)| < 2pp in the majority of cells.

CAVEATS carried, not buried
    * Survivorship: u56 and broad are current-constituent lists (idea 54).  The equity leg is
      inflated more than the ETF sleeve, which biases retention DOWNWARD (it makes the sleeve
      look better), so a high retention here is a conservative reading.
    * Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so any IS
      drawdown screen is measured on a window that cannot express a deep drawdown.
    * Idea 126: every row is t+1 execution.
    * Idea 223/182B: MaxDD is sensitive to the trade-date anchor; every row here is quoted at
      its parent's own anchor, so the back-fill is a within-anchor comparison and inherits
      whatever anchor draw the parent took.  The cash arm shares the anchor, so the RATIO is
      far less exposed than either level.
    * A retention >= 1 does NOT say the sleeve is worthless — it says the DRAWDOWN half of
      the claim is not the sleeve's.  Sharpe and CAGR are reported beside it on every row.

Deterministic, standalone, no network.  Imports research/baseline.py and the parent scripts
by value.  Writes .console.txt, .backfill.csv, .census.csv, .survival.csv, .keep.csv and
.walkforward.csv next to itself.  Modifies nothing.
"""
import importlib.util
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_publish-the-cash-carve-out-beside-every-sleeve-MaxDD_C"
OUT = ROOT / "research" / "backtests"
LB = ROOT / "research" / "LEADERBOARD.md"

FREQ = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60
BARS = [1.00, 0.75, 0.50]                 # tuned parameter 2 — all reported
CONTROLS = ["CASH-f", "CASH-GM"]          # tuned parameter 1 — both reported
TOL = 5e-4                                # reproduction tolerance on a published statistic

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

_tee = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(stem, name):
    path = OUT / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- parents
S_190 = "2026-09-05_is-the-conditional-sleeve-anything-at-all_B"
S_134 = "2026-09-05_sleeve-f-that-clears-the-floor_cloud"
S_105 = "2026-09-05_which-asset-carries-S4_C"
S_103c = "2026-09-05_sleeve-with-a-real-diversifier_cloud"
S_103b = "2026-09-05_sleeve-with-a-real-diversifier_B"
S_018 = "2026-09-04_ensemble-plus-momentum_C"
S_106 = "2026-09-05_sleeve-G-is-2013_cloud"
S_015 = "2026-09-04_crypto-sleeve_C"
S_014 = "2026-09-04_rsi2-sleeve_cloud"

M190 = _load(S_190, "i190")
M134 = M190.SF                    # idea 134, already loaded by idea 190
M105 = _load(S_105, "i105")
M103c = _load(S_103c, "i103c")
M103b = _load(S_103b, "i103b")
M018 = _load(S_018, "i018")
M106 = _load(S_106, "i106")
M015 = _load(S_015, "i015")
M014 = _load(S_014, "i014")

fast_backtest = M190.fast_backtest


# ---------------------------------------------------------------- panels
class Panel:
    """One price panel plus everything every adapter needs from it, built once."""

    def __init__(self, key):
        self.key = key
        if key == "u56x":                      # ideas 106/15 load u56 WITH the crypto columns
            self.px = load_universe(exclude=set())
        elif key == "broadx":                  # idea 15's broad panel: broad + the crypto columns
            b = load_universe(broad=True)
            c = load_universe(exclude=set())
            self.px = pd.concat([b.drop(columns=["BTC-USD", "ETH-USD"], errors="ignore"),
                                 c[["BTC-USD", "ETH-USD"]]], axis=1)
        else:
            self.px = load_universe(broad=(key == "broad"))
        self.start = self.px.index[260]
        self.spy = self.px["SPY"].pct_change().fillna(0.0).loc[self.start:]
        self.reb = np.flatnonzero(rebalance_mask(self.px.index, FREQ).values)
        self.v1 = {}
        self._cache = {}

    def v1_at(self, c):
        if c not in self.v1:
            self.v1[c] = backtest(self.px, rules_v1_weights(self.px), cost_bps=c,
                                  freq=FREQ)["returns"].loc[self.start:]
        return self.v1[c]

    def cached(self, key, fn):
        if key not in self._cache:
            self._cache[key] = fn()
        return self._cache[key]


PANELS = {}


def panel(key):
    if key not in PANELS:
        PANELS[key] = Panel(key)
    return PANELS[key]


# ---------------------------------------------------------------- metrics
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def full_stats(r):
    m, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"], IS_CAGR=mi["CAGR"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def fail4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail4b(r, spy):
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= PHI * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def dd_cap_ok(r, spy):
    return abs(metrics(r)["MaxDD"]) <= DELTA * abs(metrics(spy)["MaxDD"])


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


# ---------------------------------------------------------------- run cache
_RUNS = {}
_NBT = [0]


def gross_run(pan, W, tag):
    """0 bps returns + turnover for a weight frame, cached by tag."""
    if tag not in _RUNS:
        _RUNS[tag] = fast_backtest(pan.px, W, 0.0, FREQ)
        _NBT[0] += 1
    return _RUNS[tag]


def net_at(res, c, start):
    return (res["returns"] - res["turnover"] * c / 1e4).loc[start:]


def arm_series(cl):
    """Net return series for the four arms of one claim.  Weight-based claims are run here;
    a claim that carries its own `rets` (idea 14's two-leg capital split, where a cash sleeve
    is the blend itself with a zero-return leg) supplies them directly."""
    if cl.get("rets") is not None:
        r = cl["rets"]
        return r["sleeve"], r["base"], r["cashf"], r["cashgm"], np.nan
    pan = panel(cl["panel"])
    c, f = cl["cost"], cl["f"]
    tag = (cl["parent"], cl["panel"], cl["book"], cl["conv"], cl["sleeve"], round(f, 6))
    rs = net_at(gross_run(pan, cl["w_sleeve"], ("S",) + tag), c, pan.start)
    rb = net_at(gross_run(pan, cl["w_base"], ("B", cl["parent"], cl["panel"], cl["book"])),
                c, pan.start)
    rcf = net_at(gross_run(pan, (1 - f) * cl["w_base"],
                           ("CF", cl["parent"], cl["panel"], cl["book"], round(f, 6))),
                 c, pan.start)
    gs, gb = mean_gross(pan, cl["w_sleeve"]), mean_gross(pan, cl["w_base"])
    m = gs / gb if gb > 1e-12 else 1.0
    rgm = net_at(gross_run(pan, m * cl["w_base"],
                           ("GM", cl["parent"], cl["panel"], cl["book"], round(m, 6))), c, pan.start)
    return rs, rb, rcf, rgm, m


def mean_gross(pan, W):
    g = W.reindex(pan.px.index).fillna(0.0).sum(axis=1).values[pan.reb]
    g = g[g > 1e-12]
    return float(g.mean()) if len(g) else 0.0


# ================================================================ adapters
# Each adapter returns a list of claim dicts:
#   parent, panel, book, conv, sleeve, f, cost, w_sleeve, w_base, pub (published stats)
CLAIMS = []


def add(parent, pan_key, book, conv, sleeve, f, cost, w_sleeve, w_base, pub):
    CLAIMS.append(dict(parent=parent, panel=pan_key, book=book, conv=conv, sleeve=sleeve,
                       f=float(f), cost=float(cost), w_sleeve=w_sleeve, w_base=w_base, pub=pub))


def _grid(stem, suffix="grid.csv"):
    return pd.read_csv(OUT / f"{stem}.{suffix}")


# ---- A: idea 190 -------------------------------------------------------
def adapter_190():
    g = _grid(S_190)
    pans = {k: panel(k) for k in ["u56", "broad"]}
    sl = g[(g.kind == "real") & (g.draw == -1)]
    n = 0
    for _, r in sl.iterrows():
        pan = pans[r.panel]
        assets = M190.SETS[r.set_]
        wb = pan.cached(("i190rank", r.n), lambda n=r.n: M134.ranked(pan.px, int(n)))
        ws = M190.blend(wb, pan.cached(("sl134", tuple(assets)),
                                       lambda a=assets: M134.sleeve_weights(pan.px, a)), r.f)
        add("A/idea190", r.panel, f"R{int(r.n)}", "g0.75", r.set_, r.f, r.bps, ws, wb,
            dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD))
        n += 1
    return n


# ---- B: idea 134 (ungated control arm only) ----------------------------
def adapter_134():
    g = _grid(S_134)
    g = g[(g.kind == "ctl") & (g.arm == "control")] if "arm" in g.columns else g[g.kind == "ctl"]
    pans = {k: panel(k) for k in ["u56", "broad"]}
    n = 0
    for _, r in g.iterrows():
        if r.book == "R20":
            continue
        pan = pans[r.panel]
        wb = pan.cached(("i134book", "R20"), lambda: M134.book_weights(pan.px, "R20"))
        ws = pan.cached(("i134book", r.book), lambda b=r.book: M134.book_weights(pan.px, b))
        add("B/idea134", r.panel, "R20", "g0.75", r.book.split("-")[0], r.f, r.cost, ws, wb,
            dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD))
        n += 1
    return n


# ---- the natural/matched family: C, D1, D2, E --------------------------
def _family(parent, stem, mod, sleeve_col, sleeve_map, conv_natural, conv_other, cost):
    g = _grid(stem)
    pans = {}
    n = 0
    for _, r in g.iterrows():
        if float(r.f) == 0.0:
            continue
        key = {"u56": "u56", "broad": "broad"}[r.universe]
        pan = pans.setdefault(key, panel(key))
        bname = r.book
        wb = pan.cached((parent, "book", bname), lambda b=bname: mod.BOOKS[b](pan.px))
        sname = r[sleeve_col] if sleeve_col else "S"
        assets = sleeve_map[sname]
        S = pan.cached((parent, "sl", tuple(assets)),
                       lambda a=assets: mod.sleeve_weights(pan.px, a))
        matched = (r.conv != conv_natural)
        if parent.startswith("C/"):
            ws = mod.blend(wb, S, float(r.f), r.conv)
        else:
            ws = mod.blend(wb, S, float(r.f), matched)
        conv = "natural" if not matched else conv_other
        add(parent, key, bname, conv, sname, r.f, cost, ws, wb,
            dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD))
        n += 1
    return n


def adapter_105():
    return _family("C/idea105", S_105, M105, "sleeve", M105.SLEEVES, "natural", "g1.00", 10.0)


def adapter_103c():
    return _family("D1/idea103c", S_103c, M103c, "sleeve", M103c.SLEEVES, "natural", "gE", 10.0)


def adapter_103b():
    return _family("D2/idea103b", S_103b, M103b, "sleeve", M103b.SLEEVES, "natural", "gE", 10.0)


def adapter_018():
    g = _grid(S_018)
    pans = {}
    n = 0
    assets = list(M018.SLEEVE_ASSETS) if hasattr(M018, "SLEEVE_ASSETS") else list(M018.MACRO)
    for _, r in g.iterrows():
        if float(r.f) == 0.0:
            continue
        pan = pans.setdefault(r.universe, panel(r.universe))
        wb = pan.cached(("E", "book", r.book), lambda b=r.book: M018.BOOKS[b](pan.px))
        S = pan.cached(("E", "sl", tuple(assets)), lambda: M018.sleeve_weights(pan.px))
        matched = (r.conv != "natural")
        ws = M018.blend(wb, S, float(r.f), matched)
        add("E/idea018", r.universe, r.book, "natural" if not matched else "gE",
            "ENS", r.f, 10.0, ws, wb, dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD))
        n += 1
    return n


# ---- F: idea 106 (sleeve-G-is-2013) ------------------------------------
def adapter_106():
    g = _grid(S_106)
    g = g[g.variant != "FLAT4"]            # FLAT4 is a zero-return panel control, not a book
    pans = {}
    n = 0
    for _, r in g.iterrows():
        if float(r.f) == 0.0:
            continue
        # idea 106 builds u56 with load_universe(exclude=set()) — the crypto columns are IN
        pk = "u56x" if r.universe == "u56" else r.universe
        pan = pans.setdefault(pk, panel(pk))
        assets = M106.VARIANTS[r.variant]
        wb = pan.cached(("F", "book", r.book),
                        lambda b=r.book: M106.sleeve_overlay(pan.px, b, assets, 0.0))
        ws = M106.sleeve_overlay(pan.px, r.book, assets, float(r.f))
        add("F/idea106", pk, r.book, "g1.00", r.variant, r.f, r.cost_bps, ws, wb,
            dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD))
        n += 1
    return n


# ---- G: idea 15 (crypto sleeve; cap-funded, so f is the arm's own realised share) ------
def adapter_015():
    g = _grid(S_015)
    g = g[g.cap > 0]
    pans = {}
    n = 0
    for _, r in g.iterrows():
        pk = "u56x" if r.universe == "universe.json" else "broadx"
        pan = pans.setdefault(pk, panel(pk))
        px = pan.px
        px_eq = px.drop(columns=M015.CRYPTO)
        pxc = px[M015.CRYPTO]
        wb = pan.cached(("G", "book", r.book),
                        lambda b=r.book: M015.combined_weights(px, px_eq, pxc, b, 0.0, "same", "matched"))
        ws = M015.combined_weights(px, px_eq, pxc, r.book, float(r.cap), r.gate, r.fund)
        # matched f: the arm's OWN realised mean sleeve share of gross on its rebalance dates
        leg = ws[M015.CRYPTO].sum(axis=1)
        tot = ws.sum(axis=1)
        sh = (leg.values[pan.reb] / np.where(tot.values[pan.reb] > 1e-12, tot.values[pan.reb], np.nan))
        f_hat = float(np.nanmean(sh))
        add("G/idea015", pk, r.book, r.fund, f"cap{r.cap:.2f}-{r.gate}", f_hat, 10.0, ws, wb,
            dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD))
        n += 1
    return n


# ---- H: idea 14 (RSI(2) STRATEGY sleeve; two-leg capital split) ------------------------
def adapter_014():
    g = _grid(S_014)
    g = g[(g.f > 0) & (g.core != "-")]
    n = 0
    for _, r in g.iterrows():
        pk = "u56" if r.tag.startswith("universe.json") else "broad"
        pan = panel(pk)
        px = pan.px
        pxs = px[[t for t in M014.SECTORS if t in px.columns]]
        wk = rebalance_mask(px.index, "W")
        core = pan.cached(("H", "core", r.core), lambda b=r.core: (
            lambda res: (res["returns"].loc[pan.start:], res["turnover"].loc[pan.start:]))(
                backtest(px, M014.CORES[b](px), cost_bps=0.0, freq="W")))
        slv = pan.cached(("H", "slv", int(r.thr)), lambda t=int(r.thr): (
            lambda res: (res["returns"].reindex(px.index).fillna(0.0).loc[pan.start:],
                         res["turnover"].reindex(px.index).fillna(0.0).loc[pan.start:]))(
                backtest(pxs, M014.sleeve_weights(pxs, t), cost_bps=0.0, freq="D")))
        gc, tc = core
        gs, ts = slv
        z = gs * 0.0
        f, c = float(r.f), 10.0
        rets = dict(
            sleeve=M014.blend(gc, tc, gs, ts, f, c, wk),
            base=M014.blend(gc, tc, gs, ts, 0.0, c, wk),
            cashf=M014.blend(gc, tc, z, z, f, c, wk),      # the sleeve leg replaced by CASH
            cashgm=None)                                   # gross is not the lever here
        CLAIMS.append(dict(parent="H/idea014", panel=pk, book=r.core, conv="split",
                           sleeve=f"rsi2-thr{int(r.thr)}", f=f, cost=c,
                           w_sleeve=None, w_base=None, rets=rets,
                           pub=dict(CAGR=r.cagr, Sharpe=r.sharpe, MaxDD=r.dd)))
        n += 1
    return n


ADAPTERS = [("A/idea190", adapter_190), ("B/idea134", adapter_134), ("C/idea105", adapter_105),
            ("D1/idea103c", adapter_103c), ("D2/idea103b", adapter_103b),
            ("E/idea018", adapter_018), ("F/idea106", adapter_106),
            ("G/idea015", adapter_015), ("H/idea014", adapter_014)]


# ================================================================ census
SLEEVE_SCRIPTS = {S_190: "A/idea190", S_134: "B/idea134", S_105: "C/idea105",
                  S_103c: "D1/idea103c", S_103b: "D2/idea103b", S_018: "E/idea018",
                  S_106: "F/idea106", S_015: "G/idea015", S_014: "H/idea014"}


def census():
    txt = LB.read_text().split("\n")
    rows = []
    for ln in txt:
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.split("|")[1:-1]]
        if len(cells) < 9 or cells[0] in ("Date", "---"):
            continue
        if "sleeve" not in ln.lower():
            continue
        script = re.sub(r"^research/backtests/", "", cells[-1]).strip()
        stem = script[:-3] if script.endswith(".py") else script
        has_grid = (OUT / f"{stem}.grid.csv").exists()
        rows.append(dict(date=cells[0], idea=cells[1][:70], script=script, stem=stem,
                         covered=SLEEVE_SCRIPTS.get(stem, ""), has_grid=has_grid))
    return pd.DataFrame(rows)


# ================================================================ main
def main():
    t0 = time.time()
    P("=== idea 213  publish-the-cash-carve-out-beside-every-sleeve-MaxDD  (lane C, 2026-09-06) ===")
    P(f"tuned params: control convention {CONTROLS} x survival bar {BARS} — all reported, "
      f"nothing selected on.  Costs, panels, books, sleeve sets and f are inherited.")

    # ---------------- census ----------------
    C = census()
    P(f"\n[CENSUS] LEADERBOARD rows mentioning a sleeve: {len(C)}")
    tab = (C.groupby("stem").agg(rows=("stem", "size"), grid=("has_grid", "first"),
                                 adapter=("covered", "first")).sort_values("rows", ascending=False))
    P(tab.head(30).to_string())
    cov = int((C.covered != "").sum())
    P(f"    covered by an adapter in this run: {cov}/{len(C)} rows "
      f"({cov/len(C):.1%}); rows whose script committed a grid CSV: "
      f"{int(C.has_grid.sum())}/{len(C)} ({C.has_grid.mean():.1%}); "
      f"rows with NO grid CSV (unrecoverable without re-running the parent): "
      f"{int((~C.has_grid).sum())}")
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)

    # ---------------- build the corpus ----------------
    P("\n[CORPUS] building sleeve claims from committed grid CSVs")
    for name, fn in ADAPTERS:
        try:
            k = fn()
            P(f"    {name:14s} {k:5d} sleeve arms")
        except Exception as e:                      # a parent that will not rebuild is DROPPED
            P(f"    {name:14s} FAILED to rebuild ({type(e).__name__}: {e}) — DROPPED from corpus")
    P(f"    total sleeve arms in corpus: {len(CLAIMS)}")

    # ---------------- reproduction, before any new number ----------------
    P("\n[REPRODUCTION] every parent's own published row re-derived here, before the control is read")
    a = panel("u56")
    Wt = M134.ranked(a.px, 20)
    e = backtest(a.px, Wt, cost_bps=10.0, freq=FREQ)
    f_ = fast_backtest(a.px, Wt, 10.0, FREQ)
    d = float((e["returns"] - f_["returns"]).abs().max())
    P(f"  [a] fast_backtest vs engine.backtest on u56/R20: max|dret| {d:.3e} -> "
      f"{'PASS' if d < 1e-12 else 'FAIL'}")
    assert d < 1e-12

    rep = {}
    ser = {}
    REPDEV = {}
    for cl in CLAIMS:
        r = arm_series(cl)[0]
        m = metrics(r)
        cl["mine"] = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])
        d = {k: abs(m[k] - float(cl["pub"][k])) for k in ("CAGR", "Sharpe", "MaxDD")}
        rep.setdefault(cl["parent"], []).append(d)
        if d["Sharpe"] > ser.get(cl["parent"], (0.0, None))[0]:
            ser[cl["parent"]] = (d["Sharpe"], cl)
    ok_parents = set()
    for p_, v in sorted(rep.items()):
        R = pd.DataFrame(v)
        mx = {k: float(R[k].max()) for k in R.columns}
        good = max(mx.values()) < TOL
        REPDEV[p_] = mx
        P(f"  [b] {p_:14s} {len(v):4d} rows vs its committed grid.csv: max|dCAGR| "
          f"{mx['CAGR']:.3e}  max|dSharpe| {mx['Sharpe']:.3e}  max|dMaxDD| {mx['MaxDD']:.3e} -> "
          f"{'PASS' if good else 'CAGR/Sharpe off — see [d]'}")
        if good:
            ok_parents.add(p_)

    # [d] a parent that ran BEFORE data/prices.csv was last extended sees a longer panel here.
    #     engine.backtest is causal, so the shorter run is a strict PREFIX of this one: truncating
    #     the return series to the parent's own last bar must restore the published numbers.
    for p_ in sorted(set(rep) - ok_parents):
        arms_p = [c for c in CLAIMS if c["parent"] == p_]
        rr = [(arm_series(c)[0], c["pub"]) for c in arms_p]
        best = (np.inf, None)
        for D in rr[0][0].index[-10:]:
            e = max(abs(metrics(r.loc[:D])[k] - float(pub[k]))
                    for r, pub in rr for k in ("CAGR", "Sharpe", "MaxDD"))
            if e < best[0]:
                best = (e, D)
        e, D = best
        r = rr[0][0]
        P(f"  [d] {p_:14s} truncation probe over ALL {len(rr)} rows: max|d| falls to {e:.3e} at "
          f"end-of-sample {D.date()} (this run's panel ends {r.index[-1].date()}) -> "
          f"{'PASS — sample-extension only, parent KEPT' if e < TOL else 'FAIL — parent DROPPED'}")
        if e < TOL:
            ok_parents.add(p_)
        # every arm of a kept parent is quoted on THIS run's panel, so the back-fill stays
        # a within-panel comparison; only the parent's published levels are dated.
    kept = [c for c in CLAIMS if c["parent"] in ok_parents]
    P(f"    corpus after reproduction: {len(kept)} sleeve arms from {len(ok_parents)} parents "
      f"({len(CLAIMS) - len(kept)} dropped)")

    # idea 190's own CASH rows are the anchor for the control's definition
    g190 = _grid(S_190)
    cash190 = g190[g190.kind == "cash"]
    dmax = 0.0
    for _, r in cash190.iterrows():
        pan = panel(r.panel)
        wb = pan.cached(("i190rank", r.n), lambda n=r.n: M134.ranked(pan.px, int(n)))
        rr = net_at(gross_run(pan, (1 - r.f) * wb, ("CF190", r.panel, r.n, r.f)), r.bps, pan.start)
        m = metrics(rr)
        dmax = max(dmax, abs(m["MaxDD"] - r.MaxDD), abs(m["Sharpe"] - r.Sharpe))
    P(f"  [c] CASH-f as defined here vs idea 190's own {len(cash190)} committed cash rows: "
      f"max|d| {dmax:.3e} -> {'PASS' if dmax < TOL else 'FAIL'}")
    assert dmax < TOL, "the control does not reproduce its parent — nothing below is trustworthy"

    # ---------------- the back-fill ----------------
    P("\n[BACKFILL] every surviving sleeve arm gets its matched-f cash control")

    def backfill(claim_list):
      rows = []
      for cl in claim_list:
        pan = panel(cl["panel"])
        f, c = cl["f"], cl["cost"]
        rs, rb, rcf, rgm, m = arm_series(cl)
        ms, mb, mcf = metrics(rs), metrics(rb), metrics(rcf)
        mgm = metrics(rgm) if rgm is not None else {"MaxDD": np.nan, "Sharpe": np.nan,
                                                    "CAGR": np.nan}
        dD_s = abs(mb["MaxDD"]) - abs(ms["MaxDD"])
        dD_cf = abs(mb["MaxDD"]) - abs(mcf["MaxDD"])
        dD_gm = abs(mb["MaxDD"]) - abs(mgm["MaxDD"])
        row = dict(parent=cl["parent"], panel=cl["panel"], book=cl["book"], conv=cl["conv"],
                   sleeve=cl["sleeve"], f=f, cost=c, f_hat=1.0 - m,
                   MaxDD_base=mb["MaxDD"], MaxDD_sleeve=ms["MaxDD"],
                   MaxDD_cashf=mcf["MaxDD"], MaxDD_cashgm=mgm["MaxDD"],
                   dD_sleeve=dD_s, dD_cashf=dD_cf, dD_cashgm=dD_gm,
                   Sharpe_base=mb["Sharpe"], Sharpe_sleeve=ms["Sharpe"],
                   Sharpe_cashf=mcf["Sharpe"], Sharpe_cashgm=mgm["Sharpe"],
                   CAGR_base=mb["CAGR"], CAGR_sleeve=ms["CAGR"], CAGR_cashf=mcf["CAGR"],
                   claim=dD_s > 0,
                   ret_cashf=dD_cf / dD_s if dD_s > 0 else np.nan,
                   ret_cashgm=dD_gm / dD_s if dD_s > 0 else np.nan,
                   dd_cap_sleeve=dd_cap_ok(rs, pan.spy), dd_cap_cashf=dd_cap_ok(rcf, pan.spy),
                   dd_cap_base=dd_cap_ok(rb, pan.spy),
                   fail4a_sleeve=fail4a(rs, pan.v1_at(c)), fail4b_sleeve=fail4b(rs, pan.spy),
                   fail4a_cashf=fail4a(rcf, pan.v1_at(c)), fail4b_cashf=fail4b(rcf, pan.spy))
        rows.append(row)
      return pd.DataFrame(rows)

    B = backfill(kept)
    B.to_csv(OUT / f"{STEM}.backfill.csv", index=False)
    P(f"    {len(B)} sleeve arms back-filled; {_NBT[0]} distinct backtests")

    # ---------------- survival ----------------
    CLM = B[B.claim].copy()
    P(f"\n[SURVIVAL]  sleeve arms that make a DRAWDOWN CLAIM (MaxDD shallower than their own "
      f"f=0 control): {len(CLM)}/{len(B)} ({len(CLM)/len(B):.1%})")
    P(f"    median CASH-f retention  {CLM.ret_cashf.median():+.3f}   "
      f"mean {CLM.ret_cashf.mean():+.3f}   "
      f"share with retention >= 1.00 (cash strictly better than the sleeve): "
      f"{(CLM.ret_cashf >= 1.0).mean():.1%}")
    P(f"    median CASH-GM retention {CLM.ret_cashgm.median():+.3f}   "
      f"mean {CLM.ret_cashgm.mean():+.3f}")
    P(f"    mean dSharpe vs base: sleeve {(CLM.Sharpe_sleeve-CLM.Sharpe_base).mean():+.4f}   "
      f"CASH-f {(CLM.Sharpe_cashf-CLM.Sharpe_base).mean():+.4f}   "
      f"(sleeve's Sharpe better than cash's in "
      f"{(CLM.Sharpe_sleeve > CLM.Sharpe_cashf).mean():.1%} of claims)")
    P(f"    mean dCAGR  vs base: sleeve {(CLM.CAGR_sleeve-CLM.CAGR_base).mean():+.4%}   "
      f"CASH-f {(CLM.CAGR_cashf-CLM.CAGR_base).mean():+.4%}")

    dedup = CLM[CLM.parent != "D2/idea103b"]
    P(f"    D1/D2 are the same corpus run in two lanes; counting it once leaves "
      f"{len(dedup)} claims, median CASH-f retention {dedup.ret_cashf.median():+.3f}, "
      f"retention >= 1.00 in {(dedup.ret_cashf >= 1.0).mean():.1%}")

    surv = []
    for ctrl, col in [("CASH-f", "ret_cashf"), ("CASH-GM", "ret_cashgm")]:
        for b in BARS:
            k = int((CLM[col] < b).sum())
            surv.append(dict(control=ctrl, bar=b, claims=len(CLM), survive=k,
                             rate=k / len(CLM) if len(CLM) else np.nan))
    SV = pd.DataFrame(surv)
    P("\n    SURVIVAL TABLE — all 2 x 3 grid points reported")
    P(SV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    SV.to_csv(OUT / f"{STEM}.survival.csv", index=False)

    P("\n    by parent (CASH-f):")
    by = CLM.groupby("parent").agg(claims=("claim", "size"), med_ret=("ret_cashf", "median"),
                                   surv100=("ret_cashf", lambda s: (s < 1.0).mean()),
                                   surv50=("ret_cashf", lambda s: (s < 0.5).mean()))
    P(by.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n    by gross convention (P2):")
    bc = CLM.assign(kind=np.where(CLM.conv == "natural", "natural", "gross-matched"))
    P(bc.groupby("kind").agg(claims=("claim", "size"), med_ret_cashf=("ret_cashf", "median"),
                             ge1=("ret_cashf", lambda s: (s >= 1.0).mean()),
                             med_ret_cashgm=("ret_cashgm", "median")).to_string(
                                 float_format=lambda x: f"{x:.4f}"))

    P("\n    by sleeve fraction f (P3):")
    P(CLM.groupby(CLM.f.round(2)).agg(claims=("claim", "size"),
                                      med_ret_cashf=("ret_cashf", "median"),
                                      med_ret_cashgm=("ret_cashgm", "median")).to_string(
                                          float_format=lambda x: f"{x:.4f}"))

    P("\n    by panel:")
    P(CLM.groupby("panel").agg(claims=("claim", "size"), med_ret_cashf=("ret_cashf", "median"),
                               ge1=("ret_cashf", lambda s: (s >= 1.0).mean())).to_string(
                                   float_format=lambda x: f"{x:.4f}"))

    # ---------------- 4b drawdown cap consequence (P4) ----------------
    cap = B[B.dd_cap_sleeve]
    P(f"\n[4b DD CAP]  sleeve arms passing 4b's cap (|MaxDD| <= {DELTA:.2f} x SPY's): "
      f"{len(cap)}/{len(B)}")
    if len(cap):
        P(f"    of those, the SAME arm's CASH-f control also passes the cap: "
          f"{int(cap.dd_cap_cashf.sum())}/{len(cap)} ({cap.dd_cap_cashf.mean():.1%})  (P4)")
        P(f"    and the arm's own f=0 BASE already passes it: "
          f"{int(cap.dd_cap_base.sum())}/{len(cap)} ({cap.dd_cap_base.mean():.1%})")
    P(f"    full 4b pass (all five bars): sleeve {int((B.fail4b_sleeve=='-').sum())}/{len(B)}   "
      f"CASH-f {int((B.fail4b_cashf=='-').sum())}/{len(B)}")
    P(f"    4a pass: sleeve {int((B.fail4a_sleeve=='-').sum())}/{len(B)}   "
      f"CASH-f {int((B.fail4a_cashf=='-').sum())}/{len(B)}")
    keep = B[(B.fail4b_sleeve == "-") | (B.fail4a_sleeve == "-")]
    keep.to_csv(OUT / f"{STEM}.keep.csv", index=False)

    # ------ LABELLED APPENDIX: parents that reproduce on MaxDD but not on CAGR/Sharpe ------
    appendix = [c for c in CLAIMS if c["parent"] not in ok_parents
                and REPDEV.get(c["parent"], {}).get("MaxDD", 1.0) < 1e-4]
    if appendix:
        A = backfill(appendix)
        AC = A[A.claim]
        P(f"\n[APPENDIX — NOT IN ANY HEADLINE COUNT]  {len(A)} arms from parents whose MaxDD "
          f"re-derives to <1e-4 but whose CAGR/Sharpe do not, so they failed [b]/[d] and are "
          f"excluded above.  Their retention is printed only so the number exists:")
        P(A.groupby("parent").agg(arms=("claim", "size"), claims=("claim", "sum")).to_string())
        if len(AC):
            P(f"    median CASH-f retention {AC.ret_cashf.median():+.3f}, "
              f"retention >= 1.00 in {(AC.ret_cashf >= 1.0).mean():.1%} of {len(AC)} claims")

    # ---------------- rule 8 ----------------
    P("\n[RULE 8]  walk-forward: f* and sleeve* chosen on 2009-01..2016-12 IS Sharpe only; "
      "2017-01..2026 read once")
    cells, wf = {}, []
    for cl in kept:
        key = (cl["parent"], cl["panel"], cl["book"], cl["conv"], cl["cost"])
        cells.setdefault(key, []).append(cl)
    for key, arms in sorted(cells.items()):
        p_, pk, bk, cv, c = key
        pan = panel(pk)
        best, bs = None, -np.inf
        for cl in arms:
            s = metrics(arm_series(cl)[0].loc[:IS_END])["Sharpe"]
            if s > bs:
                bs, best = s, cl
        f = best["f"]
        rs, rb, rcf, rgm, _m = arm_series(best)
        if rgm is None:
            rgm = rb
        o = {k: metrics(v.loc[OOS_START:]) for k, v in
             [("SLEEVE", rs), ("BASE", rb), ("CASHF", rcf), ("CASHGM", rgm),
              ("V1", pan.v1_at(c)), ("SPY", pan.spy)]}
        wf.append(dict(parent=p_, panel=pk, book=bk, conv=cv, cost=c, f_star=f,
                       sleeve_star=best["sleeve"], IS_Sharpe=bs,
                       **{f"OOS_{k}_{s}": o[k][s] for k in o for s in ("CAGR", "Sharpe", "MaxDD")}))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"    {len(W)} (parent, panel, book, conv, cost) cells")
    agg = pd.DataFrame({
        arm: dict(CAGR=W[f"OOS_{arm}_CAGR"].mean(), Sharpe=W[f"OOS_{arm}_Sharpe"].mean(),
                  MaxDD=W[f"OOS_{arm}_MaxDD"].mean())
        for arm in ["SLEEVE", "CASHF", "CASHGM", "BASE", "V1", "SPY"]}).T
    P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    dS = (W.OOS_SLEEVE_Sharpe - W.OOS_CASHF_Sharpe)
    dD = (W.OOS_SLEEVE_MaxDD.abs() - W.OOS_CASHF_MaxDD.abs())
    dSb = (W.OOS_SLEEVE_Sharpe - W.OOS_BASE_Sharpe)
    dDb = (W.OOS_SLEEVE_MaxDD.abs() - W.OOS_BASE_MaxDD.abs())
    P(f"    paired SLEEVE - CASH-f :  dSharpe {dS.mean():+.4f} (t {tstat(dS):+.2f}, "
      f"{int((dS>0).sum())}/{len(dS)} wins)   dMaxDD {dD.mean():+.4%} "
      f"(t {tstat(dD):+.2f}, sleeve shallower in {int((dD<0).sum())}/{len(dD)})")
    P(f"    paired SLEEVE - BASE   :  dSharpe {dSb.mean():+.4f} (t {tstat(dSb):+.2f})   "
      f"dMaxDD {dDb.mean():+.4%} (t {tstat(dDb):+.2f})")
    within2 = (dD.abs() < 0.02).mean()
    P(f"    |OOS MaxDD(SLEEVE) - OOS MaxDD(CASH-f)| < 2pp in {within2:.1%} of cells  (P5)")
    oos_claim = W[W.OOS_SLEEVE_MaxDD.abs() < W.OOS_BASE_MaxDD.abs()]
    if len(oos_claim):
        srv = (oos_claim.OOS_SLEEVE_MaxDD.abs() < oos_claim.OOS_CASHF_MaxDD.abs()).mean()
        P(f"    cells whose sleeve improves OOS drawdown over its base: {len(oos_claim)}/{len(W)}; "
          f"of those the sleeve still beats CASH-f in {srv:.1%}")

    # ---------------- predictions ----------------
    P("\n[PREDICTIONS] scored against the pre-registered wording")
    med = CLM.ret_cashf.median()
    P(f"    P1 median CASH-f retention >= 0.75: {med:.3f} -> {'HIT' if med >= 0.75 else 'MISS'}")
    nat = CLM[CLM.conv == "natural"].ret_cashf
    mat = CLM[CLM.conv != "natural"].ret_cashf
    p2 = bool((nat >= 1.0).mean() > (mat >= 1.0).mean()) if len(nat) and len(mat) else False
    P(f"    P2 retention>=1 more common under natural ({(nat>=1.0).mean():.1%}, n={len(nat)}) "
      f"than gross-matched ({(mat>=1.0).mean():.1%}, n={len(mat)}) -> "
      f"{'HIT' if p2 else 'MISS'}")
    byf = CLM.groupby(CLM.f.round(2)).ret_cashf.median()
    p3 = bool(byf.is_monotonic_increasing)
    P(f"    P3 retention increases with f (median by f): "
      f"{ {k: round(v,3) for k, v in byf.items()} } -> {'HIT' if p3 else 'MISS'}")
    p4 = bool(cap.dd_cap_cashf.mean() >= 0.5) if len(cap) else False
    P(f"    P4 >=50% of DD-cap passers have their CASH-f passing too: "
      f"{cap.dd_cap_cashf.mean():.1%} -> {'HIT' if p4 else 'MISS'}")
    P(f"    P5 |dOOS MaxDD| < 2pp in a majority of cells: {within2:.1%} -> "
      f"{'HIT' if within2 > 0.5 else 'MISS'}")

    P(f"\n[done] {time.time()-t0:.1f}s, {_NBT[0]} backtests")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

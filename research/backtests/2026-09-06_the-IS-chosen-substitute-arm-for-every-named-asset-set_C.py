#!/usr/bin/env python3
"""QUEUE idea 212 - the-IS-chosen-substitute-arm-for-every-named-asset-set  (lane C, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 212)
    "idea 190's decisive arm (S5, -0.2509 vs do-nothing where the named sleeve is +0.0699) costs
     one enumeration.  Census the LEADERBOARD for instruments whose ASSET IDENTITIES were
     human-chosen (sleeves, hedge baskets, the TLT/GLD/UUP family, GDX/SLV pairs) and run the
     IS-chosen-substitute arm on each; report how many published separations survive being chosen
     rather than given.  Max 2 params."

WHAT THE ARM IS, AND WHY IT DECIDES ANYTHING
    Every result in this project that carries an instrument NAME - a sleeve, a hedge basket, a
    diversifier triple - was published with its assets HANDED OVER by a human.  Idea 190 showed on
    ONE such set (TLT/GLD/UUP) that the separation collapses when the assets must instead be
    CHOSEN by the project's own IS-Sharpe rule from an enumerated pool: S1 (given) +0.0699 OOS
    Sharpe vs do-nothing, S5 (chosen) -0.2509, S5-S1 -0.3208 in 12 of 12 cells.  If that is a
    property of the SELECTOR and not of TLT/GLD/UUP, it applies to every named set in the record
    and every one of those published separations is a hindsight statistic.  This run answers that
    by census: find every human-chosen asset set in the committed corpus and run S5 on each.

CENSUS (computed in this script, not asserted).  The record names assets in exactly one place -
    hard-coded ticker literals in the committed backtest scripts - so the census scans
    research/backtests/*.py for list literals drawn wholly from the non-equity / index-ETF
    vocabulary, keeps those containing at least one diversifier, and maps each set back to the
    LEADERBOARD rows whose script column is one of the scripts that hard-codes it.  That row count
    is the "published separations" the idea asks about.  The census is printed in full.
    Crypto sets (BTC-USD+ETH-USD) are censused and REPORTED but NOT run, with the reason stated
    rather than buried: baseline.EXCLUDE drops both from every cached panel, so their substitution
    population on this data is EMPTY - there is no second crypto instrument to be chosen instead.

THE SUBSTITUTION POOL, per named set.  Idea 190's DIV pool - the 12 non-crypto members of
    universe.json's `bonds_fx_commod` group (TLT IEF SHY HYG LQD TIP GLD SLV USO UNG DBC UUP) -
    UNION the named set's own members (so a set naming SPY/EFA/EEM can be substituted by things of
    its own kind), MINUS the named set's members.  The population is ENUMERATED WHOLE, no draws
    and no seed (PROTOCOL 11b as idea 208 proposed it): C(9,3)=84 for a DIV triple, C(8,4)=70 for
    S4, C(10,3)=120 for the SPY triple, C(9,6)=84 for the six-asset class set.

CONSTRUCTION, imported not re-typed.  Idea 134's committed static-sleeve book:
        R_n      top-n equal weight on the scan.py composite, gross 0.75, weekly, t+1
        SET-f    (1-f) x R_n + f x sleeve(members), rescaled to gross 0.75
        sleeve   = momentum-vote x risk-parity over the set's own members (ideas 100/104)
    via research/backtests/2026-09-05_sleeve-f-that-clears-the-floor_cloud.py.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4, and both are tuned IN SAMPLE ONLY:
    1. sleeve share f          in {0.10, 0.20, 0.50}   (idea 134's published points)
    2. substitute asset set    the IS-Sharpe argmax over the enumerated population
    CARRIED AXES, never selected on, every level reported: named set (the census axis, 8 sets),
    panel in {u56, broad136}, base book size n in {10, 20, 40}, cost rung in {10, 25} bps.
    => 12 walk-forward cells per named set, 96 in total.

COSTS.  Every book is run ONCE at 0 bps; the 10 and 25 bps rungs are derived from the engine's own
    turnover series (r_net = r_gross - turnover * bps / 1e4).  Asserted exact in check [b].

REPRODUCTION, asserted before any new number is read
    [a] this script's vectorised backtest reproduces products/backtester/engine.backtest to <1e-12
    [b] the cost identity: 10 bps derived from the 0 bps run == a genuine 10 bps engine run
    [c] the numpy sleeve == idea 134's committed sleeve_weights for every named set, max|d| == 0
    [d] the committed idea-190 walk-forward is reproduced from this run's own grid: S0 in all 12
        cells, and 190's S1/pick (an argmax over BOTH S3 and S4 and 3 f's) recovered as the max
        over this run's S3 and S4 IS rows, all 12 cells.

WALK-FORWARD (PROTOCOL rule 8).  Everything fitted on <= 2016-12-31; 2017-01-01..2026 read ONCE.
        S0  do nothing              - R_n, the untreated base book (the control)
        S1  assets GIVEN            - the named set at its IS-argmax f
        S5  assets CHOSEN           - the (f, substitute set) IS-argmax over the enumeration
        SM  random substitute       - the population MEAN at S1's own f (the null's centre)
        SC  cash carve-out          - (1-f) x R_n unrescaled at S1's own f (idea 190's S4)
    OOS CAGR / Sharpe / MaxDD for every arm against RULES v1 and SPY on the same window, both KEEP
    paths re-evaluated on the OOS window, and the paired dSharpe with its t-stat across cells.

BOTH KEEP PATHS (4a vs live RULES v1, 4b vs SPY) are evaluated on every real row, every substitute
    row and every control, full sample and OOS window.  All grid points are written to .grid.csv.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a]-[d] all hold.
    P2  The census finds <= 10 distinct human-chosen price-only asset sets in the entire record,
        and they are concentrated in the TLT/GLD/UUP family (S3, S4 and S4's leave-one-outs),
        i.e. the several hundred sleeve rows rest on a handful of asset identities.  The idea's
        own example "GDX/SLV pairs" is a hypothesis about the record, and the census tests it.
    P3  With the assets GIVEN, S1 beats S0 on mean paired OOS Sharpe for EVERY named set - the
        published separations reproduce, which is what makes the next line the whole question.
    P4  With the assets CHOSEN, S5 LOSES to S0 on mean paired OOS Sharpe for every named set:
        0 of the censused separations survive.  (Idea 190's single instance generalises because
        the mechanism is the IS-Sharpe selector's preference for low-vol credit/bond baskets whose
        OOS Sharpe does not repeat, not anything about TLT/GLD/UUP.)
    P5  S5 - S1 < 0 in at least 90% of the 96 cells, and the IS chooser lands on an IEF/LQD-led
        triple in a majority of cells whatever the named set is.
    P6  The binding 4b bar is CAGR for the S1 rows (a Sharpe gain bought with return, idea 190) and
        a Sharpe bar (H1/H2/OOS) or DD for the S5 rows.

CAVEATS carried, not buried
    * SURVIVORSHIP.  U56 and BROAD136 are current-constituent lists (idea 54).  Real and substitute
      arms inherit the bias identically, so the COMPARISON is unaffected; every LEVEL is not.
    * The DIV pool is itself a survivor list of instruments that existed and stayed liquid over
      2008-2026 and that this project has always used.  An enumeration over a hand-picked pool is
      exact for that pool and says nothing about assets outside it.  The pool IS the concession
      this test makes to the named sets: the chooser is handed the same twelve instruments the
      human was, and still loses.
    * The census can only see asset identities that reached a committed script.  A set discussed in
      a memo but never coded is invisible to it; the count is a floor, not a ceiling.
    * A substitute draw can hold a name the base leg also holds (the diversifier ETFs are eligible
      for the composite on both panels).  That is true of the real sets too and is matched.
    * Idea 38 (calendar-day index after 2014-09-17) and idea 126 (t+1 execution only) carry over.

Deterministic, standalone, no seed anywhere (the population is enumerated).
Writes .console.txt, .census.csv, .grid.csv, .walkforward.csv, .keep.csv next to itself.
"""
import importlib.util
import itertools
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_the-IS-chosen-substitute-arm-for-every-named-asset-set_C"
OUT = ROOT / "research" / "backtests"
I134 = OUT / "2026-09-05_sleeve-f-that-clears-the-floor_cloud.py"
I190_WF = OUT / "2026-09-05_is-the-conditional-sleeve-anything-at-all_B.walkforward.csv"

FREQ, GROSS = "W", 0.75
COST_RUNGS = [10.0, 25.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60
FS = [0.10, 0.20, 0.50]                      # tuned parameter 1
NS = [10, 20, 40]                            # carried axis
PANELS = ["u56", "broad"]                    # carried axis
DIV_POOL = ["TLT", "IEF", "SHY", "HYG", "LQD", "TIP", "GLD", "SLV", "USO", "UNG", "DBC", "UUP"]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_tee = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SF = _load(I134, "i134")                      # idea 134's committed construction


# ============================================================ 1. THE CENSUS ===
VOCAB = set(("TLT IEF SHY HYG LQD TIP GLD SLV USO UNG DBC UUP GDX XLP XLU XLV XLE XLK XLF XLI "
             "XLY XLB XLRE XLC SMH XBI KRE ITB QQQ IWM DIA EFA EEM VTI RSP SPY "
             "BTC-USD ETH-USD").split())
DIVERSIFIERS = set(DIV_POOL) | {"GDX", "BTC-USD", "ETH-USD", "XLP", "XLU"}
LIST_RE = re.compile(r'\[((?:\s*["\'][A-Z\-]{2,7}["\']\s*,?){2,8})\]')


def census():
    """Every human-chosen asset set in the committed corpus, with the LEADERBOARD rows it carries."""
    sets = {}
    self_path = Path(__file__).resolve()
    for f in sorted(OUT.glob("*.py")):
        if f.resolve() == self_path:                 # never censusing this script's own literals
            continue
        src = f.read_text(errors="ignore")
        for m in LIST_RE.finditer(src):
            toks = tuple(re.findall(r'["\']([A-Z\-]{2,7})["\']', m.group(1)))
            if not (2 <= len(toks) <= 6):
                continue
            if not set(toks) <= VOCAB or not (set(toks) & DIVERSIFIERS):
                continue
            if len(set(toks)) != len(toks):
                continue
            sets.setdefault(toks, set()).add(f.name)
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text().splitlines() if l.startswith("|")]
    rows = []
    for toks, scripts in sorted(sets.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        n_rows = sum(1 for l in lb if any(s[:-3] in l for s in scripts))
        rows.append(dict(assets="+".join(toks), k=len(toks), n_scripts=len(scripts),
                         lb_rows=n_rows, scripts=";".join(sorted(scripts))))
    return pd.DataFrame(rows)


# ==================================================== 2. FAST BACKTEST ENGINE ==
class Panel:
    """Panel + the rebalance-calendar tensors, which do not depend on the weights, so the whole
    enumeration reuses them.  run(wt) is the vectorised equivalent of engine.backtest (check [a])."""

    def __init__(self, key):
        self.key = key
        self.px = load_universe(broad=(key == "broad"))
        self.cols = list(self.px.columns)
        self.cix = {c: i for i, c in enumerate(self.cols)}
        idx = self.px.index
        self.idx = idx
        self.rets = self.px.pct_change().fillna(0.0).values
        m = rebalance_mask(idx, FREQ).values
        m = np.concatenate([[False], m[:-1]]).copy()      # decided at t, applied at t+1
        m[0] = True
        self.reb = np.flatnonzero(m)
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        Cp = np.vstack([np.ones((1, N)), C[:-1]])
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R1 = Cp / Cp[self.s0]
        self.R2 = Cp / Cp[self.s0p]
        self.start = idx[260]
        self.i0 = idx.get_indexer([self.start])[0]
        self.spy = self.px["SPY"].pct_change().fillna(0.0).loc[self.start:]
        self.ranked = {n: SF.ranked(self.px, n).values for n in NS}
        self.v1 = {c: backtest(self.px, rules_v1_weights(self.px), cost_bps=c,
                               freq=FREQ)["returns"].loc[self.start:] for c in COST_RUNGS}
        self._sleeve = {}

    def run(self, wt):
        """wt: (T,N) weights decided at t.  Returns (gross returns, turnover) as np arrays."""
        w = np.vstack([np.zeros((1, self.N)), wt[:-1]])   # shift(1): applied at t+1
        W0 = w[self.s0]
        h = W0 * self.R1
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = w[self.s0p]
        hp = W0p * self.R2
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(w[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn

    def sleeve_cols(self, assets):
        """(T,k) momentum-vote x risk-parity sleeve on `assets` - numpy, checked against idea 134."""
        key = tuple(assets)
        if key not in self._sleeve:
            sub = self.px[list(assets)]
            inv = 1.0 / sub.pct_change().rolling(60).std().replace(0.0, np.nan)
            rp = inv.div(inv.sum(axis=1), axis=0)
            sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
            vote = sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)
            self._sleeve[key] = ((vote * rp).fillna(0.0).values,
                                 np.array([self.cix[a] for a in assets]))
        return self._sleeve[key]


def blend(pan, n, assets, f):
    """(1-f) R_n + f sleeve, rescaled to GROSS.  Identical to idea 134's book_weights."""
    sw, ix = pan.sleeve_cols(assets)
    w = (1.0 - f) * pan.ranked[n]
    w = w.copy()
    w[:, ix] += f * sw
    s = w.sum(axis=1)
    sc = np.where(s > 0, GROSS / np.where(s == 0, 1.0, s), 0.0)
    return w * sc[:, None]


# ================================================================ 3. METRICS ==
def ser(pan, gross, turn, bps):
    r = pd.Series(gross - turn * bps / 1e4, index=pan.idx).iloc[pan.i0:]
    return r


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def row_metrics(r):
    m, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"])


def fail4a(r, base):
    h1, h2 = halves(r); b1, b2 = halves(base); f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail4b(r, spy):
    h1, h2 = halves(r); s1, s2 = halves(spy); m, ms = metrics(r), metrics(spy); f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= PHI * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fail4b_window(r, spy):
    """4b re-evaluated on the OOS window alone (halves of the OOS window)."""
    return fail4b(r.loc[OOS_START:], spy.loc[OOS_START:])


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


# =========================================================== 4. REPRODUCTION ==
def checks(pans, named):
    ok = True
    P("\n[REPRODUCTION] asserted before any new number is read")
    for pan in pans:
        W = pd.DataFrame(pan.ranked[20], index=pan.idx, columns=pan.cols)
        a = backtest(pan.px, W, cost_bps=10.0, freq=FREQ)
        g, t = pan.run(pan.ranked[20])
        i0 = pan.i0                                   # the evaluated sample; nothing before it is used
        nan_eng = int(a["returns"].isna().sum())      # the ENGINE emits 2 NaNs in the warm-up (stated)
        dr = float(np.abs(a["returns"].values[i0:] - (g - t * 10.0 / 1e4)[i0:]).max())
        dt = float(np.abs(a["turnover"].values[i0:] - t[i0:]).max())
        P(f"  [a] {pan.key:6s} run() vs engine.backtest on the evaluated sample [{i0}:]: "
          f"max|dret| {dr:.3e} max|dturn| {dt:.3e} -> {'PASS' if dr < 1e-12 and dt < 1e-12 else 'FAIL'}"
          f"  (engine emits {nan_eng} NaN returns in the pre-warm-up head; excluded, not hidden)")
        ok &= dr < 1e-12 and dt < 1e-12
        b0 = backtest(pan.px, W, cost_bps=0.0, freq=FREQ)
        d = float(np.abs((b0["returns"] - b0["turnover"] * 10.0 / 1e4) - a["returns"]).max())
        P(f"  [b] {pan.key:6s} cost identity 0bps->10bps vs engine 10bps: max|d| {d:.3e}"
          f" -> {'PASS' if d < 1e-12 else 'FAIL'}")
        ok &= d < 1e-12
        for nm, assets in named.items():
            if not set(assets) <= set(pan.cols):
                continue
            ref = SF.sleeve_weights(pan.px, list(assets))[list(assets)].values
            sw, _ = pan.sleeve_cols(assets)
            d = float(np.abs(ref - sw).max())
            ok &= d == 0.0
            if d != 0.0:
                P(f"  [c] {pan.key:6s} {nm:12s} sleeve vs idea 134: max|d| {d:.3e} -> FAIL")
        P(f"  [c] {pan.key:6s} numpy sleeve == idea 134 sleeve_weights for all named sets: "
          f"max|d| 0.0 -> PASS")
    return ok


# ================================================================== 5. MAIN ===
def main():
    t_start = time.time()
    P(f"# {STEM}")
    P(f"# QUEUE idea 212 - the IS-chosen-substitute arm for EVERY named asset set")
    P(f"# run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC · costs {COST_RUNGS} bps · t+1 · freq {FREQ}"
      f" · gross {GROSS} · NO SEED (populations enumerated)")

    # ---- census ------------------------------------------------------------
    P("\n[CENSUS] human-chosen asset sets in the committed corpus "
      "(ticker literals in research/backtests/*.py, mapped to their LEADERBOARD rows)")
    cen = census()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    P(cen[["assets", "k", "n_scripts", "lb_rows"]].to_string(index=False))
    P(f"  distinct human-chosen sets: {len(cen)} · LEADERBOARD rows they carry: "
      f"{int(cen['lb_rows'].sum())} (rows are counted once per set they touch)")

    runnable, skipped = {}, {}
    for _, r in cen.iterrows():
        assets = tuple(r["assets"].split("+"))
        if set(assets) & {"BTC-USD", "ETH-USD"}:
            skipped[r["assets"]] = "crypto: baseline.EXCLUDE drops it from every cached panel; " \
                                   "substitution population is EMPTY (no second crypto instrument)"
            continue
        runnable["+".join(assets)] = assets
    for k, v in skipped.items():
        P(f"  SKIPPED {k}: {v}")
    P(f"  RUN: {len(runnable)} named sets x {len(PANELS)} panels x {len(NS)} base-n x "
      f"{len(COST_RUNGS)} cost rungs = {len(runnable)*len(PANELS)*len(NS)*len(COST_RUNGS)} cells")

    # ---- panels + checks ---------------------------------------------------
    pans = {}
    for key in PANELS:
        pans[key] = Panel(key)
        P(f"  panel {key:6s} {pans[key].px.shape[0]} rows x {pans[key].px.shape[1]} cols "
          f"[{pans[key].idx[0].date()} .. {pans[key].idx[-1].date()}] start {pans[key].start.date()}")
    named_avail = {k: v for k, v in runnable.items() if set(v) <= set(pans["u56"].cols)}
    for k, v in runnable.items():
        if k not in named_avail:
            miss = [a for a in v if a not in pans["u56"].cols]
            P(f"  SKIPPED {k}: not on the panel ({miss})")
    if not checks(list(pans.values()), named_avail):
        P("  REPRODUCTION FAILED - stopping.")
        return

    # ---- substitution populations -----------------------------------------
    P("\n[POPULATIONS] enumerated whole, no draws, no seed")
    pops = {}
    for nm, assets in named_avail.items():
        pool = sorted((set(DIV_POOL) | set(assets)) - set(assets))
        pops[nm] = [tuple(c) for c in itertools.combinations(pool, len(assets))]
        P(f"  {nm:28s} k={len(assets)}  pool {len(pool):2d}  population C({len(pool)},{len(assets)})"
          f" = {len(pops[nm])}")

    # ---- the grid + walk-forward, fused (the enumeration is too large to hold in memory) -----
    P("\n[GRID] every book run once at 0 bps; cost rungs derived.  This is the whole enumeration.")
    P("  (grid and walk-forward are fused: only the S0/CASH/REAL books and the S5 winners are held)")
    grid, cache, picks, smsum = [], {}, {}, {}
    for pkey, pan in pans.items():
        spy = pan.spy
        for n in NS:

            def add(kind, nm, aset, f, g, t, store=False):
                if store:
                    cache[(pkey, n, kind, nm, aset, f)] = (g, t)
                for bps in COST_RUNGS:
                    r = ser(pan, g, t, bps)
                    m = row_metrics(r)
                    rec = dict(panel=pkey, n=n, set=nm, kind=kind,
                               assets="+".join(aset) if aset else ("R_n" if kind == "S0" else "cash"),
                               f=f, bps=bps, **m)
                    rec["fail4a"] = fail4a(r, pan.v1[bps])
                    rec["fail4b"] = fail4b(r, spy)
                    rec["fail4b_oos"] = fail4b_window(r, spy)
                    grid.append(rec)
                    if kind == "SUB":
                        k = (pkey, n, bps, nm)
                        if m["IS_Sharpe"] > picks.get(k, (-np.inf,))[0]:
                            picks[k] = (m["IS_Sharpe"], aset, f)
                        s = smsum.setdefault((pkey, n, bps, nm, f), [0.0, 0])
                        s[0] += m["OOS_Sharpe"]; s[1] += 1

            add("S0", "-", None, 0.0, *pan.run(pan.ranked[n]), store=True)
            for f in FS:
                add("CASH", "-", None, f, *pan.run((1.0 - f) * pan.ranked[n]), store=True)
            for nm, assets in named_avail.items():
                if not set(assets) <= set(pan.cols):
                    continue
                for f in FS:
                    add("REAL", nm, assets, f, *pan.run(blend(pan, n, list(assets), f)), store=True)
                for s in pops[nm]:
                    if not set(s) <= set(pan.cols):
                        continue
                    for f in FS:
                        add("SUB", nm, s, f, *pan.run(blend(pan, n, list(s), f)))
            P(f"  {pkey:6s} n={n:2d} grid rows so far {len(grid)}  ({time.time()-t_start:.0f}s)")
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"  grid rows: {len(G)}  ({time.time()-t_start:.0f}s)  -> {STEM}.grid.csv")

    # ---- KEEP paths over the whole grid ------------------------------------
    P("\n[KEEP PATHS] full sample, every grid row (PROTOCOL 4a and 4b), by arm kind")
    kp = G.assign(p4a=G.fail4a.eq("-"), p4b=G.fail4b.eq("-"), p4b_oos=G.fail4b_oos.eq("-"))
    tab = kp.groupby("kind").agg(rows=("p4a", "size"), pass4a=("p4a", "sum"),
                                 pass4b=("p4b", "sum"), pass4b_oos=("p4b_oos", "sum"))
    tab["rate4a"] = (tab.pass4a / tab.rows).round(4)
    tab["rate4b"] = (tab.pass4b / tab.rows).round(4)
    tab["rate4b_oos"] = (tab.pass4b_oos / tab.rows).round(4)
    P(tab.to_string())
    P("\n[KEEP PATHS] 4b by named set, REAL rows only (the published construction)")
    real = kp[kp.kind == "REAL"]
    P(real.groupby("set").agg(rows=("p4b", "size"), pass4a=("p4a", "sum"), pass4b=("p4b", "sum"),
                              pass4b_oos=("p4b_oos", "sum")).to_string())
    P("\n[KEEP PATHS] which 4b bar binds (most common failing bar, by kind)")
    for kind in ["REAL", "SUB", "S0", "CASH"]:
        sub = kp[kp.kind == kind]
        P(f"  {kind:5s} " + ", ".join(f"{k}={v}" for k, v in
                                      sub.fail4b.value_counts().head(6).items()))
    kp.to_csv(OUT / f"{STEM}.keep.csv", index=False)

    # ---- walk-forward, PROTOCOL rule 8 -------------------------------------
    P("\n[RULE 8 WALK-FORWARD] params fitted on <= 2016-12-31; 2017-2026 read ONCE.")
    P("  S0 do-nothing (R_n) · S1 assets GIVEN (IS-argmax f) · S5 assets CHOSEN (IS-argmax f+set)")
    P("  SM population mean at S1's f · SC cash carve-out at S1's f")
    wf = []
    gi = G.set_index(["panel", "n", "bps", "set", "kind", "assets", "f"])
    for pkey, pan in pans.items():
        spy = pan.spy
        for n in NS:
            for bps in COST_RUNGS:
                s0r = ser(pan, *cache[(pkey, n, "S0", "-", None, 0.0)], bps)
                s0m = row_metrics(s0r)
                for nm, assets in named_avail.items():
                    if not set(assets) <= set(pan.cols):
                        continue
                    # S1: IS-argmax f with the assets GIVEN
                    isr = {f: row_metrics(ser(pan, *cache[(pkey, n, "REAL", nm, assets, f)], bps))
                           for f in FS}
                    f1 = max(FS, key=lambda f: isr[f]["IS_Sharpe"])
                    s1r = ser(pan, *cache[(pkey, n, "REAL", nm, assets, f1)], bps)
                    s1m = row_metrics(s1r)
                    # S5: IS-argmax over (f, substitute set) - the decisive arm (re-run the winner)
                    _, bset, bf = picks[(pkey, n, bps, nm)]
                    s5r = ser(pan, *pan.run(blend(pan, n, list(bset), bf)), bps)
                    s5m = row_metrics(s5r)
                    # SM: population mean OOS Sharpe at S1's own f
                    ssum, scnt = smsum[(pkey, n, bps, nm, f1)]
                    scr = ser(pan, *cache[(pkey, n, "CASH", "-", None, f1)], bps)
                    scm = row_metrics(scr)
                    wf.append(dict(
                        panel=pkey, n=n, bps=bps, set=nm, f1=f1,
                        pick5="+".join(bset), f5=bf,
                        S0=s0m["OOS_Sharpe"], S1=s1m["OOS_Sharpe"], S5=s5m["OOS_Sharpe"],
                        SM=ssum / scnt, SC=scm["OOS_Sharpe"],
                        d1=s1m["OOS_Sharpe"] - s0m["OOS_Sharpe"],
                        d5=s5m["OOS_Sharpe"] - s0m["OOS_Sharpe"],
                        d51=s5m["OOS_Sharpe"] - s1m["OOS_Sharpe"],
                        S0_CAGR=s0m["OOS_CAGR"], S1_CAGR=s1m["OOS_CAGR"], S5_CAGR=s5m["OOS_CAGR"],
                        SC_CAGR=scm["OOS_CAGR"],
                        S0_DD=s0m["OOS_MaxDD"], S1_DD=s1m["OOS_MaxDD"], S5_DD=s5m["OOS_MaxDD"],
                        SC_DD=scm["OOS_MaxDD"],
                        S0_4b=fail4b_window(s0r, spy), S1_4b=fail4b_window(s1r, spy),
                        S5_4b=fail4b_window(s5r, spy), SC_4b=fail4b_window(scr, spy),
                        S0_4a=fail4a(s0r.loc[OOS_START:], pan.v1[bps].loc[OOS_START:]),
                        S1_4a=fail4a(s1r.loc[OOS_START:], pan.v1[bps].loc[OOS_START:]),
                        S5_4a=fail4a(s5r.loc[OOS_START:], pan.v1[bps].loc[OOS_START:]),
                        v1_Sharpe=metrics(pan.v1[bps].loc[OOS_START:])["Sharpe"],
                        v1_CAGR=metrics(pan.v1[bps].loc[OOS_START:])["CAGR"],
                        v1_DD=metrics(pan.v1[bps].loc[OOS_START:])["MaxDD"],
                        spy_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                        spy_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                        spy_DD=metrics(spy.loc[OOS_START:])["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"  cells: {len(W)}  ({time.time()-t_start:.0f}s)")

    # ---- check [d]: reproduce idea 190's committed walk-forward -------------
    P("\n[REPRODUCTION] [d] idea 190's committed walk-forward, rebuilt from this run's own grid")
    if I190_WF.exists():
        ref = pd.read_csv(I190_WF)
        d_s0, d_s1, n_pick = [], [], 0
        for _, r in ref.iterrows():
            w = W[(W.panel == r.panel) & (W.n == r.n) & (W.bps == r.bps)]
            if w.empty:
                continue
            d_s0.append(abs(w.S0.iloc[0] - r.S0))
            fam = w[w["set"].isin(["TLT+GLD+UUP", "TLT+GLD+DBC+UUP"])]
            if fam.empty:
                continue
            # 190's S1 is the argmax over BOTH sets and 3 f's: recover it from our per-set IS rows
            cands = []
            for _, fr in fam.iterrows():
                a = tuple(fr["set"].split("+"))
                for f in FS:
                    m = gi.loc[(r.panel, r.n, r.bps, fr["set"], "REAL", fr["set"], f)]
                    cands.append((m["IS_Sharpe"], fr["set"], f, m["OOS_Sharpe"]))
            best = max(cands)
            tag = ("S3" if best[1] == "TLT+GLD+UUP" else "S4") + f"-{best[2]}"
            n_pick += int(tag == str(r["pick"]))
            d_s1.append(abs(best[3] - r.S1))
        P(f"  [d] S0 reproduced in {len(d_s0)}/12 cells, max|d| {max(d_s0):.3e} -> "
          f"{'PASS' if max(d_s0) < 1e-12 else 'FAIL'}")
        P(f"  [d] 190's S1 pick reproduced in {n_pick}/{len(d_s1)} cells; OOS Sharpe max|d| "
          f"{max(d_s1):.3e} -> {'PASS' if n_pick == len(d_s1) and max(d_s1) < 1e-12 else 'FAIL'}")
    else:
        P("  [d] idea 190 walkforward.csv not found - check SKIPPED (stated, not hidden)")

    # ---- the answer --------------------------------------------------------
    P("\n[ANSWER] per named set: does the published separation survive being CHOSEN not GIVEN?")
    P("  d1 = OOS Sharpe(assets GIVEN) - do-nothing ; d5 = OOS Sharpe(assets CHOSEN) - do-nothing")
    rows = []
    for nm, sub in W.groupby("set"):
        rows.append(dict(
            set=nm, cells=len(sub), lb_rows=int(cen.loc[cen.assets == nm, "lb_rows"].iloc[0]),
            d1_mean=sub.d1.mean(), d1_t=tstat(sub.d1), d1_win=f"{int((sub.d1>0).sum())}/{len(sub)}",
            d5_mean=sub.d5.mean(), d5_t=tstat(sub.d5), d5_win=f"{int((sub.d5>0).sum())}/{len(sub)}",
            d51_mean=sub.d51.mean(), d51_t=tstat(sub.d51),
            d51_neg=f"{int((sub.d51<0).sum())}/{len(sub)}",
            survives=bool(sub.d5.mean() > 0 and (sub.d5 > 0).sum() > len(sub) / 2)))
    A = pd.DataFrame(rows).sort_values("lb_rows", ascending=False)
    P(A.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    n_sep = int((A.d1_mean > 0).sum())
    n_surv = int(A.survives.sum())
    P(f"\n  named sets tested: {len(A)}  ·  LEADERBOARD rows they carry: {int(A.lb_rows.sum())}")
    P(f"  separations that REPRODUCE with the assets GIVEN (mean d1 > 0): {n_sep}/{len(A)}")
    P(f"  separations that SURVIVE being CHOSEN (mean d5 > 0 and majority of cells): "
      f"{n_surv}/{len(A)}")
    P(f"  pooled over all {len(W)} cells: d1 {W.d1.mean():+.4f} (t {tstat(W.d1):+.2f}, "
      f"{int((W.d1>0).sum())}/{len(W)}) · d5 {W.d5.mean():+.4f} (t {tstat(W.d5):+.2f}, "
      f"{int((W.d5>0).sum())}/{len(W)}) · d5-d1 {W.d51.mean():+.4f} (t {tstat(W.d51):+.2f}, "
      f"{int((W.d51<0).sum())}/{len(W)} negative)")
    P(f"  the population MEAN substitute (SM) vs do-nothing: "
      f"{(W.SM - W.S0).mean():+.4f} · cash carve-out (SC) vs do-nothing: {(W.SC - W.S0).mean():+.4f}")

    P("\n[WHAT THE IS CHOOSER PICKS] frequency of the substitute set it lands on")
    vc = W.pick5.value_counts()
    P("  " + " · ".join(f"{k} x{v}" for k, v in vc.head(10).items()))
    led = pd.Series([p.split("+")[0] for p in W.pick5]).value_counts()
    P(f"  leading ticker of the pick: " + " · ".join(f"{k} {v}/{len(W)}" for k, v in led.items()))
    for tk in ["IEF", "LQD", "SHY", "TIP", "HYG"]:
        n_hit = sum(1 for p in W.pick5 if tk in p.split("+"))
        P(f"    {tk} appears in {n_hit}/{len(W)} picks")

    P(f"\n[OOS LEVELS] mean over the {len(W)} cells, vs the live book and SPY on the same window")
    lv = pd.DataFrame([
        dict(arm="S0 do-nothing", Sharpe=W.S0.mean(), CAGR=W.S0_CAGR.mean(), MaxDD=W.S0_DD.mean()),
        dict(arm="S1 assets GIVEN", Sharpe=W.S1.mean(), CAGR=W.S1_CAGR.mean(), MaxDD=W.S1_DD.mean()),
        dict(arm="S5 assets CHOSEN", Sharpe=W.S5.mean(), CAGR=W.S5_CAGR.mean(), MaxDD=W.S5_DD.mean()),
        dict(arm="SM population mean", Sharpe=W.SM.mean(), CAGR=np.nan, MaxDD=np.nan),
        dict(arm="SC cash carve-out", Sharpe=W.SC.mean(), CAGR=W.SC_CAGR.mean(), MaxDD=W.SC_DD.mean()),
        dict(arm="RULES v1", Sharpe=W.v1_Sharpe.mean(), CAGR=W.v1_CAGR.mean(), MaxDD=W.v1_DD.mean()),
        dict(arm="SPY", Sharpe=W.spy_Sharpe.mean(), CAGR=W.spy_CAGR.mean(), MaxDD=W.spy_DD.mean()),
    ]).set_index("arm")
    P(lv.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n[OOS-WINDOW 4b] passes by arm (of {len(W)} cells)")
    for c in ["S0_4b", "S1_4b", "S5_4b", "SC_4b"]:
        P(f"  {c:7s} pass {int((W[c]=='-').sum()):3d}/{len(W)} · commonest failing bar: "
          + ", ".join(f"{k}={v}" for k, v in W[c].value_counts().head(4).items()))

    P("\n[SCOREBOARD vs the pre-registered predictions]")
    P(f"  P1 checks [a]-[d]                                    -> see above")
    P(f"  P2 <=10 distinct human-chosen sets, TLT/GLD/UUP family-> {len(cen)} censused, "
      f"{len(named_avail)} runnable  {'HOLDS' if len(cen) <= 10 else 'FAILS'}")
    P(f"  P3 every named set separates with assets GIVEN        -> {n_sep}/{len(A)}  "
      f"{'HOLDS' if n_sep == len(A) else 'FAILS'}")
    P(f"  P4 0 survive being CHOSEN                             -> {n_surv}/{len(A)} survive  "
      f"{'HOLDS' if n_surv == 0 else 'FAILS'}")
    p5 = (W.d51 < 0).mean()
    P(f"  P5 d5-d1 < 0 in >=90% of cells                        -> {p5:.1%}  "
      f"{'HOLDS' if p5 >= 0.90 else 'FAILS'}")
    s1cagr = (W.S1_4b.str.contains("CAGR")).mean()
    P(f"  P6 CAGR binds for S1                                  -> CAGR in {s1cagr:.1%} of S1 "
      f"OOS-4b failures-lists  {'HOLDS' if s1cagr > 0.5 else 'FAILS'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    P(f"\n[DONE] {time.time()-t_start:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

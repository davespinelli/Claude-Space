#!/usr/bin/env python3
"""QUEUE idea 147 — scale-free-as-a-corpus-eligibility-rule  (research sprint lane C, 2026-09-05)

QUESTION (pre-registered, verbatim from QUEUE.md idea 147)
    "Idea 144 showed 72 of 306 books are not closed under rescaling at all (ddctl/ebud swing
    Sharpe up to 0.292 along their own gross family and lose CAGR monotonicity in 45 of 72),
    while scale-free arms move <= 0.013.  Test whether re-parameterising those instruments in
    RELATIVE units (a drawdown trigger as a multiple of the book's own trailing vol; a turnover
    budget as a fraction of gross) restores closure, which would make the whole corpus
    rescale-safe instead of 76% of it."

WHAT IS BEING ADJUDICATED
    Idea 144 adopted the convention "a static rescaling of a book is the SAME book" as a
    REPORTING convention, but had to restrict it to scale-free instruments: an 8%-drawdown
    trigger on a book run at half gross is a different rule, because that book can no longer
    fall 8%.  That restriction is a wart on the convention — it means 24% of the corpus
    (72 of 306 books) cannot be scored the way the other 76% is.

    Idea 147 tests the obvious repair.  Both offending parameters are ABSOLUTE quantities that
    can be restated in units of the book itself:

        ddctl   D = 8% of equity            ->  D_t = c x (the book's own trailing vol)
        ebud    B = 0.10 of weight per week ->  B   = beta x (the book's own target gross)

    If the repair works, "rescale = same book" holds for the WHOLE corpus and PROTOCOL can
    state a corpus-eligibility rule: every instrument carried in the corpus must be
    parameterised in units that scale with the book.  If it does not work, the restriction in
    idea 144's convention is intrinsic and must stay in the wording.

PRE-REGISTERED SUCCESS BAR (written before any number was read; rule 7 — nothing tuned to fit)
    The PURE (scale-free) class is the yardstick, not zero: idea 144 measured PURE at CAGR
    monotone 228/234, |MaxDD| monotone 234/234, max Sharpe range 0.0130.  The compounding /
    cash-drift non-linearity in run() is common to every arm, so a perfect repair lands there,
    not at exact invariance.  The repair SUCCEEDS iff, over the same 72 scale-dependent books:
        (S1) max Sharpe range over the gross family falls below 0.05
             (an order of magnitude below 0.2924, and inside the cross-book Sharpe sd 0.319);
        (S2) CAGR-monotone and |MaxDD|-monotone both reach >= 90% of books (65 of 72),
             from 27/72 and 35/72.
    Anything less is PARK (partial repair) or KILL (the units are not the mechanism).

TUNED PARAMETERS — exactly two (PROTOCOL rule 4), both swept and ALL grid points reported
    c   ddctl relative trigger, as a multiple of trailing annualised vol
        c in {0.4, 0.7, 1.0, 1.3, 1.6}
        The grid was fixed by ARITHMETIC before any result was read: mean trailing-60d
        annualised vol of these books at m=1.00 runs ~7-16%, so the grid brackets the
        published 8% trigger on every panel and book (c=1.0 is ~8% on the median book).
    L   the trailing-vol lookback in trading days
        L in {60, 120}
    The turnover budget's relative form carries NO free parameter: a budget stated as a
    fraction of target gross is exactly `ebud x m`, which reproduces the published arm at
    m = 1.00 by construction.  Likewise the analytic relative drawdown trigger `D x m`.
    Reset (`recover` / `high`) and budget level (0.10 / 0.20) are ARM dimensions, reported in
    full, never selected over — exactly as idea 94 treated them.

CORPUS (nothing new invented; idea 144's frame, restricted to the class under repair)
    3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 2 cost rungs = 18 cells.
    Arms per cell (32):
        PURE reference (4)  control, g200-dg, band3-dg, stop15    -- the closure yardstick
        ABS (4)             ddctl-8%/recover, ddctl-8%/high, ebud-0.10, ebud-0.20  (published)
        REL-M (4)           the same four with D -> D x m and B -> B x m  (analytic rescale)
        REL-V (20)          ddctl with D_t = c x vol_L, c x L x {recover, high}
    Gross family: m in {0.10, 0.15, ..., 1.30} = 25 points, identical to idea 144.
    18 x 32 x 25 = 14,400 backtests.  Weekly, t+1, 75% target gross at m=1.00, 10 and 25 bps.
    IS <= 2016-12-31, OOS >= 2017-01-01.

REPRODUCTION CHECKS (all must pass before any new number is read)
    (a) run2() with every relative feature off == idea 94's H.run to machine precision;
    (b) run2() == engine.backtest on the ungated EWall u56 control;
    (c) idea 144's Q1 census on the ABS arms: 72 books, CAGR monotone 27/72,
        |MaxDD| monotone 35/72, max Sharpe range 0.2924; PURE max range <= 0.0130;
    (d) REL-M at m = 1.00 == ABS at m = 1.00 exactly (the relative form is a
        reparameterisation, not a new rule).

BOTH KEEP PATHS (PROTOCOL rule 4) are evaluated on every book: 4a against live RULES v1 on the
same panel and cost rung, 4b as POINT-4b (m = 1.00) and as FAMILY-4b (some m of the family).

WALK-FORWARD (PROTOCOL rule 8) — selection fixed before any OOS number was read
    In each of the 18 cells, three MATCHED selectors, each choosing over 4 arms x 25 m:
        A   ABS       the published absolute-unit arms
        B   REL-M     the analytic relative rescale of the same four
        C   REL-V     ddctl at the pre-registered (c, L) = (1.0, 60) + the REL-M ebud arms
    Rule: among family points clearing the IS 4b bars (H1/H2/DD/CAGR on 2009-2016 with the IS
    window's own SPY reference), take argmax IS Sharpe; if the cell admits none, fall back to
    the unscreened IS argmax (both readings reported).  OOS 2017-2026 read ONCE.
    Controls: the no-instrument `control` arm at m = 1.00, live RULES v1, SPY.
    Also reported: OOS Sharpe REGRET of the m-pick (best OOS Sharpe in the family minus the
    OOS Sharpe of the IS pick) — the number that says whether closure makes the family screen's
    extra freedom safe.

CAVEATS carried, not buried
    - Survivorship (idea 54): all three panels are current-constituent lists.
    - Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so every IS
      drawdown cap admits too much.  This biases all three selectors identically.
    - Idea 38 (u56/broad are on a calendar-day index) and idea 126 (t+1 only) carry over.
    - REL-V reads the book's own realised vol through t-1 only; no look-ahead.  Before 20
      observations exist the trigger cannot arm.

RUNNING IT
    `--panel u56` / `--panel broad` / `--panel small` compute and cache one panel's grid
    (deterministic, 4-way multiprocessing); running with no argument reads the three caches and
    prints every number in this file.  The split is an execution convenience only — the corpus,
    the arms and the m-grid are identical to a single-process run.

Deterministic, standalone.  Imports research/baseline.py and idea 94's harness; modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_scale-free-as-a-corpus-eligibility-rule_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = H.BOOKS
PANELS = ["u56", "broad", "small"]

MGRID = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.05)]    # 25 construction points
MCEIL = [1.00, 1.30]
PHI0, DELTA0 = 0.70, 0.60                                       # published 4b coefficients

CGRID = [0.4, 0.7, 1.0, 1.3, 1.6]                               # tuned param 1
LGRID = [60, 120]                                               # tuned param 2
CSTAR, LSTAR = 1.0, 60          # pre-registered focal point: a drawdown of one
#                                 annualised-vol unit; nearest the published 8% on the median book

BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS_IS = ("H1", "H2", "DD", "CAGR")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 3000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ================================================================= simulator
def run2(px, W, m=1.0, stop=None, D=None, k=1.0, reset="recover", ebud=None,
         dvol=None, bps=PCOST, freq=FREQ):
    """Idea 94's run() with ONE addition: `dvol=(c, L)` replaces the absolute drawdown trigger
    D with a relative one, D_t = c x (annualised std of the book's own NET daily returns over
    the last L days, through t-1).  Everything else is byte-identical to H.run, and the
    equivalence is asserted below.  With dvol=None this function IS H.run.
    """
    pxv = px.values
    rets = px.pct_change().fillna(0.0).values
    tgt = (W.reindex(px.index).fillna(0.0) * m).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape

    cur = np.zeros(ncol)
    peak_p = np.full(ncol, np.nan)
    pending = np.zeros(ncol, dtype=bool)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    cut = np.zeros(nrow, dtype=bool)
    rp_hist = np.zeros(nrow)
    dthr = np.full(nrow, np.nan)
    eq, pk, armed, episodes, n_stops = 1.0, 1.0, False, 0, 0
    c_v, L_v = (dvol if dvol is not None else (None, None))

    for i in range(nrow):
        if pending.any():
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        if mask[i] and i > 0:
            D_i = D
            if dvol is not None:
                lo = max(0, i - L_v)
                h = rp_hist[lo:i]
                D_i = c_v * float(h.std()) * np.sqrt(252.0) if len(h) >= 20 else None
                if D_i is not None and (not np.isfinite(D_i) or D_i <= 0.0):
                    D_i = None
                dthr[i] = D_i if D_i is not None else np.nan
            if D_i is not None:
                dd = eq / pk - 1.0                   # equity through close i-1: no look-ahead
                if not armed and dd < -D_i:
                    armed, episodes = True, episodes + 1
                elif armed and (dd >= 0.0 if reset == "high" else dd > -D_i / 2.0):
                    armed = False
            new = tgt[i - 1] * (k if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            if ebud is not None:
                d = new - cur
                up = np.clip(d, 0.0, None).sum()
                if up > ebud:
                    new = cur + np.clip(d, None, 0.0) + np.clip(d, 0.0, None) * (ebud / up)
            turn[i] += np.abs(new - cur).sum()
            cur = new
        cut[i] = armed
        held[i] = cur
        gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        rp_hist[i] = rp
        eq *= (1.0 + rp)
        pk = max(pk, eq)
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
        if stop is not None:
            alive = cur > 1e-9
            p = pxv[i]
            peak_p = np.where(alive, np.fmax(np.where(np.isnan(peak_p), -np.inf, peak_p), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak_p * (1 - stop))
            if hit.any():
                pending |= hit
                n_stops += int(hit.sum())

    r = pd.Series((held * rets).sum(axis=1), index=px.index) - pd.Series(turn, index=px.index) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                cut=pd.Series(cut, index=px.index), episodes=episodes, n_stops=n_stops,
                dthr=pd.Series(dthr, index=px.index))


# ================================================================= arms
def arm_specs():
    """(name, kind, family, (gate, conv), kwargs-of-m).  Order is the print order."""
    A = [("control", "ctl", "PURE", (None, "dg"), lambda m: {}),
         ("g200-dg", "gate", "PURE", ("g200", "dg"), lambda m: {}),
         ("band3-dg", "gate", "PURE", ("band3", "dg"), lambda m: {}),
         ("stop15", "stop", "PURE", (None, "dg"), lambda m: dict(stop=0.15))]
    for rs in ("recover", "high"):
        A.append((f"ddctl-abs-8/{rs}", "dd", "ABS", (None, "dg"),
                  lambda m, r=rs: dict(D=0.08, k=0.5, reset=r)))
    for b in (0.10, 0.20):
        A.append((f"ebud-abs-{b:.2f}", "bud", "ABS", (None, "dg"),
                  lambda m, b=b: dict(ebud=b)))
    for rs in ("recover", "high"):
        A.append((f"ddctl-relM-8/{rs}", "dd", "REL-M", (None, "dg"),
                  lambda m, r=rs: dict(D=0.08 * m, k=0.5, reset=r)))
    for b in (0.10, 0.20):
        A.append((f"ebud-relM-{b:.2f}", "bud", "REL-M", (None, "dg"),
                  lambda m, b=b: dict(ebud=b * m)))
    for c in CGRID:
        for L in LGRID:
            for rs in ("recover", "high"):
                A.append((f"ddctl-relV-c{c:.2f}-L{L}/{rs}", "dd", "REL-V", (None, "dg"),
                          lambda m, c=c, L=L, r=rs: dict(dvol=(c, L), k=0.5, reset=r)))
    return A


ARMS = arm_specs()
ABS_ARMS = [a[0] for a in ARMS if a[2] == "ABS"]
RELM_ARMS = [a[0] for a in ARMS if a[2] == "REL-M"]
RELV_MATCHED = [f"ddctl-relV-c{CSTAR:.2f}-L{LSTAR}/recover",
                f"ddctl-relV-c{CSTAR:.2f}-L{LSTAR}/high",
                "ebud-relM-0.10", "ebud-relM-0.20"]

# the one-to-one map used by the "same rule, other units" comparison
PAIRS = [("ddctl-abs-8/recover", "ddctl-relM-8/recover"),
         ("ddctl-abs-8/high", "ddctl-relM-8/high"),
         ("ebud-abs-0.10", "ebud-relM-0.10"),
         ("ebud-abs-0.20", "ebud-relM-0.20")]


# ================================================================= panels (idea 144 verbatim)
_PCACHE, _WCACHE = {}, {}


def panel(name):
    if name not in _PCACHE:
        _PCACHE[name] = _panel(name)
    return _PCACHE[name]


def _panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


def targets_cached(pname, px, book, gate, conv):
    key = (pname, book, gate, conv)
    if key not in _WCACHE:
        _WCACHE[key] = H.targets(px, book, gate, conv)
    return _WCACHE[key]


def bars_win(spy, which):
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


def stats_of(r, which):
    w = H.window(r, which) if which != "full" else r
    m = metrics(w)
    h1, h2 = H.halves(w)
    oos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=oos)


def bar_ok(D, phi, delta, which="full"):
    if which == "full":
        return pd.DataFrame(dict(
            H1=D.H1 - D.b_s1 > 0, H2=D.H2 - D.b_s2 > 0,
            OOS=D.OOS_Sharpe_full - D.b_soos > 0,
            DD=delta * D.b_sdd.abs() - D.MaxDD.abs() > 0,
            CAGR=D.CAGR - phi * D.b_scagr > 0), index=D.index)
    return pd.DataFrame(dict(
        H1=D.IS_H1 - D.bi_s1 > 0, H2=D.IS_H2 - D.bi_s2 > 0,
        DD=delta * D.bi_sdd.abs() - D.IS_MaxDD.abs() > 0,
        CAGR=D.IS_CAGR - phi * D.bi_scagr > 0), index=D.index)


# ================================================================= per-panel compute
# The panel grids are computed one panel at a time (`--panel <name>`) and cached to
# <STEM>.grid.<panel>.csv.gz; `--analyze` reads the three caches and produces every number below.
# Splitting is purely an execution convenience — the corpus, the arms and the grid are identical
# to the single-process version, and the cached CSVs are deterministic.
_PX = _SPY = _START = None
_WT = {}


def _task(spec):
    book, cost, ai = spec
    arm, kind, fam, (gate, conv), kwf = ARMS[ai]
    W = _WT[(book, gate, conv)]
    out = []
    for m_ in MGRID:
        res = run2(_PX, W, m=m_, bps=cost, **kwf(m_))
        r = res["r"].loc[_START:]
        g = res["gross"].loc[_START:]
        sf, si = stats_of(r, "full"), stats_of(r, "IS")
        so = metrics(H.window(r, "OOS"))
        out.append(dict(
            book=book, cost=cost, arm=arm, kind=kind, family=fam, m=m_,
            CAGR=sf["CAGR"], Sharpe=sf["Sharpe"], MaxDD=sf["MaxDD"],
            H1=sf["H1"], H2=sf["H2"], OOS_Sharpe_full=sf["OOS_Sharpe"],
            IS_CAGR=si["CAGR"], IS_Sharpe=si["Sharpe"], IS_MaxDD=si["MaxDD"],
            IS_H1=si["H1"], IS_H2=si["H2"],
            OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
            gross=float(g.mean()), episodes=res["episodes"],
            dthr=float(np.nanmean(res["dthr"].values))
            if np.isfinite(res["dthr"].values).any() else np.nan,
            pass4a=H.pass4a(r, _V1[cost]),
            TO=float(res["to"].loc[_START:].sum() / (len(r) / 252))))
    return out


def compute_panel(pname, nproc=4):
    global _PX, _SPY, _START, _WT, _V1
    import multiprocessing as mp
    import time
    px, spy, desc = panel(pname)
    _PX = px
    _START = px.index[260]
    _SPY = spy.loc[_START:]
    _V1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[_START:]
           for c in COSTS}
    _WT = {}
    for book in BOOKS:
        for gate, conv in {(a[3][0], a[3][1]) for a in ARMS}:
            _WT[(book, gate, conv)] = H.targets(px, book, gate, conv)
    specs = [(b, c, i) for b in BOOKS for c in COSTS for i in range(len(ARMS))]
    t0 = time.time()
    with mp.Pool(nproc) as pool:
        chunks = pool.map(_task, specs, chunksize=1)
    rows = [r for ch in chunks for r in ch]
    D = pd.DataFrame(rows)
    D.insert(0, "panel", pname)
    D.to_csv(OUT / f"{STEM}.grid.{pname}.csv.gz", index=False)
    print(f"panel {pname} ({desc}): {len(D)} rows in {time.time()-t0:.0f}s -> "
          f"{STEM}.grid.{pname}.csv.gz", flush=True)


# ================================================================= main
def main():
    say("=" * 200)
    say("IDEA 147 — scale-free-as-a-corpus-eligibility-rule.  Under test: does re-stating the "
        "two absolute-unit instruments")
    say("            (ddctl's 8% trigger, ebud's 0.10 budget) in RELATIVE units restore closure "
        "under rescaling?")
    say(f"corpus = 18 cells x {len(ARMS)} arms x {len(MGRID)} gross points = "
        f"{18*len(ARMS)*len(MGRID)} backtests. m in [{MGRID[0]}, {MGRID[-1]}].")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, {GROSS:.0%} target gross at m=1.00, "
        f"costs {COSTS} bps.  4b bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|.")
    say(f"TUNED (2): c in {CGRID} (vol multiple), L in {LGRID} (lookback).  ALL 10 reported. "
        f"Matched point for the walk-forward pre-registered at c={CSTAR}, L={LSTAR}.")
    say("PRE-REGISTERED SUCCESS BAR: max Sharpe range < 0.05 AND both monotonicity counts "
        ">= 65/72.  PURE yardstick: 228/234, 234/234, 0.0130.")
    say("=" * 200)

    FR, V1, SPY, BARS = [], {}, {}, {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        SPY[pname] = spy
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        BARS[pname] = (bfull, bIS)
        say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} | "
            f"eval from {start.date()}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%}  Sharpe {metrics(spy)['Sharpe']:.3f}  "
            f"MaxDD {bfull['sdd']:.2%}  halves {bfull['s1']:.3f}/{bfull['s2']:.3f}  "
            f"OOS Sharpe {bfull['soos']:.3f}")
        say(f"    published bars: CAGR floor {PHI0*bfull['scagr']:.2%}/yr   DD cap "
            f"{-DELTA0*abs(bfull['sdd']):.2%}   |   IS SPY: CAGR {bIS['scagr']:.2%} "
            f"MaxDD {bIS['sdd']:.2%} halves {bIS['s1']:.3f}/{bIS['s2']:.3f}")
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        V1[pname] = v1
        say(f"    live RULES v1 @10bps: CAGR {metrics(v1[10.0])['CAGR']:.2%}  "
            f"Sharpe {metrics(v1[10.0])['Sharpe']:.3f}  MaxDD {metrics(v1[10.0])['MaxDD']:.2%}")

        cache = OUT / f"{STEM}.grid.{pname}.csv.gz"
        if not cache.exists():
            raise SystemExit(f"missing {cache.name} — run `--panel {pname}` first")
        D = pd.read_csv(cache)
        FR.append(D)
        say(f"    ... {pname} grid loaded ({len(D)} rows)")

    F = pd.concat(FR, ignore_index=True)
    for key, idx in (("b_s1", "s1"), ("b_s2", "s2"), ("b_soos", "soos"),
                     ("b_sdd", "sdd"), ("b_scagr", "scagr")):
        F[key] = F.panel.map({p: BARS[p][0][idx] for p in PANELS})
    for key, idx in (("bi_s1", "s1"), ("bi_s2", "s2"), ("bi_sdd", "sdd"), ("bi_scagr", "scagr")):
        F[key] = F.panel.map({p: BARS[p][1][idx] for p in PANELS})
    F["book_id"] = F.panel + "|" + F.book + "|" + F.cost.astype(str) + "|" + F.arm
    B5 = bar_ok(F, PHI0, DELTA0, "full")
    F["ok4b"] = B5[list(BARS5)].all(axis=1)
    F["okIS"] = bar_ok(F, PHI0, DELTA0, "IS")[list(BARS_IS)].all(axis=1)
    say(f"\nfull frame: {len(F)} rows = {F.book_id.nunique()} books x {len(MGRID)} m-points")

    # ============================================================ reproduction checks
    say("\n" + "=" * 200)
    say("REPRODUCTION CHECKS (all four must pass before any new number is read)")
    px56, spy56, _ = panel("u56")
    s56 = px56.index[260]
    ew = H.targets(px56, "EWall")
    worst_a = 0.0
    for kw in (dict(), dict(stop=0.15), dict(D=0.08, k=0.5, reset="recover"),
               dict(D=0.08, k=0.5, reset="high"), dict(ebud=0.10), dict(ebud=0.20)):
        a = run2(px56, ew, m=0.55, bps=PCOST, **kw)["r"].loc[s56:]
        b = H.run(px56, ew, m=0.55, bps=PCOST, **kw)["r"].loc[s56:]
        worst_a = max(worst_a, float((a - b).abs().max()))
    say(f"  (a) run2 vs idea-94 H.run, 6 instrument settings at m=0.55: max|diff| = {worst_a:.2e} "
        f"-> {'PASS' if worst_a < 1e-15 else 'FAIL'}")

    a = run2(px56, ew, bps=PCOST)["r"].loc[s56:]
    b = backtest(px56, ew, cost_bps=PCOST, freq=FREQ)["returns"].loc[s56:]
    d_b = float((a - b).abs().max())
    say(f"  (b) run2 control vs engine.backtest, ungated EWall u56: max|diff| = {d_b:.2e} -> "
        f"{'PASS' if d_b < 1e-12 else 'FAIL'}")

    # (c) idea 144's Q1 census, on this run's ABS and PURE arms
    def closure(sub):
        out = []
        for (pn, bk, c, arm), g in sub.groupby(["panel", "book", "cost", "arm"], sort=False):
            g = g.sort_values("m")
            s = g.Sharpe.values
            out.append(dict(panel=pn, book=bk, cost=c, arm=arm, kind=g.kind.iloc[0],
                            family=g.family.iloc[0],
                            sharpe_range=float(np.nanmax(s) - np.nanmin(s)),
                            sharpe_at_1=float(g.loc[g.m == 1.00, "Sharpe"].iloc[0]),
                            cagr_mono=bool(np.all(np.diff(g.CAGR.values) > -1e-12)),
                            dd_mono=bool(np.all(np.diff(np.abs(g.MaxDD.values)) > -1e-12)),
                            cagr_range=float(g.CAGR.max() - g.CAGR.min()),
                            dd_range=float(g.MaxDD.abs().max() - g.MaxDD.abs().min()),
                            mean_TO=float(g.TO.mean()), mean_eps=float(g.episodes.mean())))
        return pd.DataFrame(out)

    CL = closure(F)
    CL.to_csv(OUT / f"{STEM}.closure.csv", index=False)
    abs_cl = CL[CL.family == "ABS"]
    pure_cl = CL[CL.family == "PURE"]
    c_ok = (len(abs_cl) == 72 and int(abs_cl.cagr_mono.sum()) == 27
            and int(abs_cl.dd_mono.sum()) == 35
            and abs(abs_cl.sharpe_range.max() - 0.2924) < 5e-4)
    say(f"  (c) idea 144 Q1 census on the ABS arms: n={len(abs_cl)} (expect 72), CAGR monotone "
        f"{int(abs_cl.cagr_mono.sum())}/72 (expect 27), |MaxDD| monotone "
        f"{int(abs_cl.dd_mono.sum())}/72 (expect 35), max Sharpe range "
        f"{abs_cl.sharpe_range.max():.4f} (expect 0.2924) -> {'PASS' if c_ok else 'FAIL'}")
    say(f"      PURE yardstick on this run's 4 pure arms (n={len(pure_cl)}): CAGR monotone "
        f"{int(pure_cl.cagr_mono.sum())}/{len(pure_cl)}, |MaxDD| monotone "
        f"{int(pure_cl.dd_mono.sum())}/{len(pure_cl)}, max Sharpe range "
        f"{pure_cl.sharpe_range.max():.4f} (idea 144 full PURE class: 228/234, 234/234, 0.0130)")

    # (d) REL-M at m=1.00 must equal ABS at m=1.00
    P1 = F[F.m == 1.00].set_index(["panel", "book", "cost", "arm"])
    dmax = 0.0
    for a_, r_ in PAIRS:
        for col in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"):
            x = P1.xs(a_, level="arm")[col]
            y = P1.xs(r_, level="arm")[col]
            dmax = max(dmax, float((x - y).abs().max()))
    say(f"  (d) REL-M == ABS at m=1.00 over 4 pairs x 4 metrics x 18 cells: max|diff| = "
        f"{dmax:.2e} -> {'PASS' if dmax < 1e-12 else 'FAIL'}")

    # ============================================================ Q1 — does the repair restore closure?
    say("\n" + "=" * 200)
    say("Q1 — DOES RELATIVE PARAMETERISATION RESTORE CLOSURE?  (the whole question)")
    say("    A rescale must leave Sharpe alone and move CAGR and |MaxDD| monotonically in m.")
    t = CL.groupby("family").agg(n=("arm", "size"),
                                 sharpe_rng_mean=("sharpe_range", "mean"),
                                 sharpe_rng_p90=("sharpe_range", lambda s: s.quantile(0.9)),
                                 sharpe_rng_max=("sharpe_range", "max"),
                                 cagr_mono=("cagr_mono", "sum"),
                                 dd_mono=("dd_mono", "sum"))
    t["cagr_mono_pct"] = t.cagr_mono / t.n
    t["dd_mono_pct"] = t.dd_mono / t.n
    say("\n  by parameterisation family (books = panel x book x cost x arm):")
    say(t.reindex(["PURE", "ABS", "REL-M", "REL-V"]).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  by instrument kind within each family:")
    t2 = CL.groupby(["family", "kind"]).agg(n=("arm", "size"),
                                            sharpe_rng_max=("sharpe_range", "max"),
                                            cagr_mono=("cagr_mono", "sum"),
                                            dd_mono=("dd_mono", "sum"))
    say(t2.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  MATCHED PAIRS — the same rule in two unit systems, 18 cells each:")
    pr = []
    for a_, r_ in PAIRS:
        A_ = CL[CL.arm == a_].set_index(["panel", "book", "cost"])
        R_ = CL[CL.arm == r_].set_index(["panel", "book", "cost"])
        pr.append(dict(rule=a_.split("-abs")[0] + a_.split("/")[-1] if "/" in a_ else a_,
                       abs_arm=a_, rel_arm=r_, n=len(A_),
                       abs_rng_max=A_.sharpe_range.max(), rel_rng_max=R_.sharpe_range.max(),
                       abs_rng_med=A_.sharpe_range.median(), rel_rng_med=R_.sharpe_range.median(),
                       abs_cagr_mono=int(A_.cagr_mono.sum()), rel_cagr_mono=int(R_.cagr_mono.sum()),
                       abs_dd_mono=int(A_.dd_mono.sum()), rel_dd_mono=int(R_.dd_mono.sum())))
    PRD = pd.DataFrame(pr)
    say(PRD.drop(columns=["rule"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  REL-V full 2-parameter grid (c x L), ALL 10 points, both resets, 18 cells each:")
    gv = CL[CL.family == "REL-V"].copy()
    gv["c"] = gv.arm.str.extract(r"c([0-9.]+)-").astype(float)
    gv["L"] = gv.arm.str.extract(r"-L(\d+)/").astype(int)
    gv["reset"] = gv.arm.str.split("/").str[-1]
    gt = gv.groupby(["c", "L", "reset"]).agg(n=("arm", "size"),
                                             sharpe_rng_max=("sharpe_range", "max"),
                                             sharpe_rng_med=("sharpe_range", "median"),
                                             cagr_mono=("cagr_mono", "sum"),
                                             dd_mono=("dd_mono", "sum"),
                                             mean_eps=("mean_eps", "mean"))
    say(gt.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  8 largest Sharpe swings along a family, by parameterisation:")
    for fam in ("ABS", "REL-M", "REL-V"):
        w = CL[CL.family == fam].nlargest(4, "sharpe_range")[
            ["panel", "book", "cost", "arm", "sharpe_range", "cagr_mono", "dd_mono"]]
        say(f"   -- {fam}")
        say(w.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # scale-dependent class as idea 147 defined it: the 72 ABS books, and their repairs
    rel_all = CL[CL.family.isin(["REL-M"])]
    relv_all = CL[CL.family == "REL-V"]
    relv_star = relv_all[relv_all.arm.str.contains(f"c{CSTAR:.2f}-L{LSTAR}/")]
    say("\n" + "-" * 200)
    say("  PRE-REGISTERED SUCCESS BAR — (S1) max Sharpe range < 0.05 ; (S2) both monotonicity "
        "counts >= 90% of books")
    for nm, d in (("ABS (published, 72 books)", abs_cl),
                  ("REL-M (analytic rescale, 72 books)", rel_all),
                  (f"REL-V @ c={CSTAR},L={LSTAR} (36 books)", relv_star),
                  ("REL-V (all 10 grid points, 360 books)", relv_all)):
        s1 = d.sharpe_range.max() < 0.05
        s2 = (d.cagr_mono.mean() >= 0.90) and (d.dd_mono.mean() >= 0.90)
        say(f"    {nm:42s} max range {d.sharpe_range.max():.4f} "
            f"({'PASS' if s1 else 'FAIL'})   CAGR mono {int(d.cagr_mono.sum())}/{len(d)} "
            f"({d.cagr_mono.mean():.0%})  DD mono {int(d.dd_mono.sum())}/{len(d)} "
            f"({d.dd_mono.mean():.0%})  -> S2 {'PASS' if s2 else 'FAIL'}")
    say(f"    {'PURE yardstick (72 books, this run)':42s} max range "
        f"{pure_cl.sharpe_range.max():.4f}   CAGR mono {int(pure_cl.cagr_mono.sum())}/"
        f"{len(pure_cl)}  DD mono {int(pure_cl.dd_mono.sum())}/{len(pure_cl)}")
    say("-" * 200)

    # ============================================================ Q2 — corpus consequence
    say("\n" + "=" * 200)
    say("Q2 — WHAT THE REPAIR DOES TO THE CORPUS: 4b and 4a verdicts, POINT vs FAMILY")

    def verdicts(sub, mmax):
        s = sub[sub.m <= mmax + 1e-9]
        g = s.groupby("book_id")
        return pd.DataFrame(dict(passed=g.ok4b.any(), n_m=g.ok4b.sum()))

    q2 = []
    for fam in ("PURE", "ABS", "REL-M", "REL-V"):
        sub = F[F.family == fam]
        nb = sub.book_id.nunique()
        pt = sub[sub.m == 1.00]
        row = dict(family=fam, books=nb,
                   POINT_4b=int(pt.ok4b.sum()), POINT_4a=int(pt.pass4a.sum()))
        for mm in MCEIL:
            v = verdicts(sub, mm)
            row[f"FAMILY_4b_m{mm:.2f}"] = int(v.passed.sum())
            row[f"FAMILY_4b_pct_m{mm:.2f}"] = v.passed.mean()
            s = sub[sub.m <= mm + 1e-9]
            row[f"FAMILY_4a_m{mm:.2f}"] = int(s.groupby("book_id").pass4a.any().sum())
        q2.append(row)
    Q2 = pd.DataFrame(q2)
    say("\n  admissions by parameterisation (POINT = m=1.00 only; FAMILY = some m of the family):")
    say(Q2.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n  matched pairs — does the repair change a 4b verdict for the SAME rule? (18 cells each)")
    mv = []
    for a_, r_ in PAIRS:
        for mm in MCEIL:
            va = F[(F.arm == a_) & (F.m <= mm + 1e-9)].groupby("book_id").ok4b.any()
            vr = F[(F.arm == r_) & (F.m <= mm + 1e-9)].groupby("book_id").ok4b.any()
            key = lambda s: s.rename(index=lambda x: "|".join(x.split("|")[:3]))
            va, vr = key(va), key(vr)
            j = pd.concat([va.rename("abs"), vr.rename("rel")], axis=1)
            mv.append(dict(rule=a_, m_max=mm, n=len(j),
                           abs_pass=int(j["abs"].sum()), rel_pass=int(j["rel"].sum()),
                           flips_to_pass=int((~j["abs"] & j["rel"]).sum()),
                           flips_to_fail=int((j["abs"] & ~j["rel"]).sum())))
    MV = pd.DataFrame(mv)
    say(MV.to_string(index=False))

    # admitted-set OOS quality
    say("\n  quality of what each parameterisation admits (FAMILY-4b at m<=1.30, "
        "best-m row per book by IS Sharpe, OOS 2017-2026):")
    qual = []
    for fam in ("PURE", "ABS", "REL-M", "REL-V"):
        s = F[(F.family == fam) & (F.m <= 1.30 + 1e-9) & F.ok4b]
        if len(s) == 0:
            qual.append(dict(family=fam, admitted=0))
            continue
        pick = s.sort_values("IS_Sharpe", ascending=False).groupby("book_id").head(1)
        qual.append(dict(family=fam, admitted=int(pick.book_id.nunique()),
                         OOS_CAGR=pick.OOS_CAGR.mean(), OOS_Sharpe=pick.OOS_Sharpe.mean(),
                         OOS_MaxDD=pick.OOS_MaxDD.mean(), mean_m=pick.m.mean(),
                         also_4a=int(pick.pass4a.sum())))
    say(pd.DataFrame(qual).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ Q3 — rule 8 walk-forward
    say("\n" + "=" * 200)
    say("Q3 — RULE 8 WALK-FORWARD.  Parameters chosen on 2009-2016 ONLY; OOS 2017-2026 read once.")
    say("    Three MATCHED selectors, each over 4 arms x 25 m: A=ABS, B=REL-M, "
        f"C=REL-V(c={CSTAR}, L={LSTAR}) + REL-M ebud.")
    say("    Rule: among family points clearing the IS 4b bars take argmax IS Sharpe; if none, "
        "fall back to the unscreened IS argmax.")

    SELS = {"A_ABS": ABS_ARMS, "B_RELM": RELM_ARMS, "C_RELV": RELV_MATCHED}
    wf = []
    for pname in PANELS:
        for book in BOOKS:
            for cost in COSTS:
                cell = F[(F.panel == pname) & (F.book == book) & (F.cost == cost)
                         & (F.m <= 1.30 + 1e-9)]
                ctl = cell[(cell.arm == "control") & (cell.m == 1.00)].iloc[0]
                v1 = V1[pname][cost]
                v1o = metrics(H.window(v1, "OOS"))
                spyo = metrics(H.window(SPY[pname], "OOS"))
                for sname, arms in SELS.items():
                    cand = cell[cell.arm.isin(arms)]
                    pool = cand[cand.okIS]
                    screened = len(pool) > 0
                    src = pool if screened else cand
                    pick = src.sort_values(["IS_Sharpe", "arm", "m"], ascending=[False, True, True]).iloc[0]
                    best_oos = cand.OOS_Sharpe.max()
                    wf.append(dict(panel=pname, book=book, cost=cost, selector=sname,
                                   screened=screened, arm=pick.arm, m=pick.m,
                                   IS_Sharpe=pick.IS_Sharpe,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                   OOS_MaxDD=pick.OOS_MaxDD,
                                   regret=best_oos - pick.OOS_Sharpe,
                                   ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                                   ctl_OOS_MaxDD=ctl.OOS_MaxDD,
                                   v1_OOS_Sharpe=v1o["Sharpe"], v1_OOS_CAGR=v1o["CAGR"],
                                   v1_OOS_MaxDD=v1o["MaxDD"],
                                   spy_OOS_Sharpe=spyo["Sharpe"], spy_OOS_CAGR=spyo["CAGR"],
                                   spy_OOS_MaxDD=spyo["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say("\n  per-cell picks (all 54 rows: 18 cells x 3 selectors):")
    say(WF[["panel", "book", "cost", "selector", "screened", "arm", "m", "IS_Sharpe",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "regret"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  AGGREGATE (mean over 18 cells; 'paired' = cells where all three selectors were "
        "IS-screened):")
    piv = WF.pivot_table(index=["panel", "book", "cost"], columns="selector", values="screened")
    paired_cells = piv[piv.all(axis=1)].index
    agg = []
    for sname in SELS:
        s = WF[WF.selector == sname]
        p = s.set_index(["panel", "book", "cost"]).loc[
            [i for i in paired_cells if i in s.set_index(["panel", "book", "cost"]).index]]
        agg.append(dict(selector=sname, cells=len(s), screened=int(s.screened.sum()),
                        OOS_CAGR=s.OOS_CAGR.mean(), OOS_Sharpe=s.OOS_Sharpe.mean(),
                        OOS_MaxDD=s.OOS_MaxDD.mean(), regret=s.regret.mean(),
                        mean_m=s.m.mean(), sd_m=s.m.std(),
                        p_cells=len(p), p_OOS_CAGR=p.OOS_CAGR.mean(),
                        p_OOS_Sharpe=p.OOS_Sharpe.mean(), p_OOS_MaxDD=p.OOS_MaxDD.mean(),
                        p_regret=p.regret.mean(),
                        beat_ctl=int((s.OOS_Sharpe > s.ctl_OOS_Sharpe).sum()),
                        beat_spy=int((s.OOS_Sharpe > s.spy_OOS_Sharpe).sum()),
                        beat_v1=int((s.OOS_Sharpe > s.v1_OOS_Sharpe).sum())))
    AGG = pd.DataFrame(agg)
    say(AGG.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    c0 = WF[WF.selector == "A_ABS"]
    say(f"\n  CONTROLS (mean over the same 18 cells): no-instrument `control` m=1.00 -> "
        f"OOS CAGR {c0.ctl_OOS_CAGR.mean():.2%}, Sharpe {c0.ctl_OOS_Sharpe.mean():.3f}, "
        f"MaxDD {c0.ctl_OOS_MaxDD.mean():.2%}")
    say(f"                                       live RULES v1 -> OOS CAGR "
        f"{c0.v1_OOS_CAGR.mean():.2%}, Sharpe {c0.v1_OOS_Sharpe.mean():.3f}, "
        f"MaxDD {c0.v1_OOS_MaxDD.mean():.2%}")
    say(f"                                       SPY           -> OOS CAGR "
        f"{c0.spy_OOS_CAGR.mean():.2%}, Sharpe {c0.spy_OOS_Sharpe.mean():.3f}, "
        f"MaxDD {c0.spy_OOS_MaxDD.mean():.2%}")

    say("\n  m-CHOICE STABILITY — the risk the family convention introduces.  Spearman(IS Sharpe, "
        "OOS Sharpe) across the 25 m of the PICKED arm:")
    ms = []
    for sname, arms in SELS.items():
        rs, mdiff = [], []
        for pname in PANELS:
            for book in BOOKS:
                for cost in COSTS:
                    cell = F[(F.panel == pname) & (F.book == book) & (F.cost == cost)
                             & (F.m <= 1.30 + 1e-9)]
                    row = WF[(WF.panel == pname) & (WF.book == book) & (WF.cost == cost)
                             & (WF.selector == sname)].iloc[0]
                    fam = cell[cell.arm == row.arm].sort_values("m")
                    rs.append(H.spearman(fam.IS_Sharpe.values, fam.OOS_Sharpe.values))
                    mdiff.append(abs(row.m - fam.loc[fam.OOS_Sharpe.idxmax(), "m"]))
        ms.append(dict(selector=sname, mean_rho=np.nanmean(rs), median_rho=np.nanmedian(rs),
                       mean_abs_m_error=np.mean(mdiff)))
    say(pd.DataFrame(ms).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ outputs
    F.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False)
    Q2.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
    MV.to_csv(OUT / f"{STEM}.pairflips.csv", index=False)
    gt.reset_index().to_csv(OUT / f"{STEM}.cLgrid.csv", index=False)
    AGG.to_csv(OUT / f"{STEM}.wfagg.csv", index=False)

    # ============================================================ verdict
    say("\n" + "=" * 200)
    say("VERDICT")
    relm_s1 = rel_all.sharpe_range.max() < 0.05
    relm_s2 = (rel_all.cagr_mono.mean() >= 0.90) and (rel_all.dd_mono.mean() >= 0.90)
    relv_s1 = relv_star.sharpe_range.max() < 0.05
    relv_s2 = (relv_star.cagr_mono.mean() >= 0.90) and (relv_star.dd_mono.mean() >= 0.90)
    say(f"  REL-M: S1 {'PASS' if relm_s1 else 'FAIL'}  S2 {'PASS' if relm_s2 else 'FAIL'}")
    say(f"  REL-V: S1 {'PASS' if relv_s1 else 'FAIL'}  S2 {'PASS' if relv_s2 else 'FAIL'}")
    say("  (no book is promoted by this run: it re-parameterises an existing corpus, and the "
        "object adjudicated is the CORPUS-ELIGIBILITY RULE, not a trading book.)")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.console.txt / .grid.csv.gz / .closure.csv / .cLgrid.csv / .verdicts.csv "
        f"/ .pairflips.csv / .walkforward.csv / .wfagg.csv")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--panel":
        for pn in args[1:]:
            compute_panel(pn)
    else:
        main()

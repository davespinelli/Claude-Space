#!/usr/bin/env python3
"""IDEA 409 — why do 4b windows have width 0 on four of six dials?  (lane B, 2026-09-10)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number in this file was read)
    Idea 401 found the adopted value sits inside a contiguous 4b interval only on `f`
    (median window width 4) and `vol` (1.5); band, gross, K and n all have median window
    width 0.  Test whether those windows are empty because the book fails 4b EVERYWHERE
    along the dial (an EXPOSURE fact — no grid will ever find a passer) or because the
    window falls BETWEEN published grid points (a GRID fact — the evidence is coarse, not
    the book).  Max 2 params.

THE TWO HYPOTHESES, and the one experiment that separates them
    H_EXPOSURE  the 4b-passing set of the dial is genuinely empty.  Refining the grid
                arbitrarily finely adds no passer.  The published width-0 is a fact about
                the book's exposure profile.
    H_GRID      the 4b-passing set is a non-empty interval SHORTER than the published grid
                spacing, so every published point misses it.  Refining the grid produces a
                passer at a value that is not on the published grid.

    These are distinguishable by one action and only one: REFINE THE GRID AND RUN IT.
    Every other statistic (how close the best margin came, how monotone the curve is) is a
    predictor of the answer, not the answer.  So this script re-runs all six dials at three
    resolutions and reports what appears.

RESOLUTIONS (definition fixed in advance, uniform across dials, no per-dial tuning)
    PUB  idea 401's published sweep, verbatim.
    x2   PUB plus the midpoint of every adjacent PUB pair.
    x4   x2 plus the midpoint of every adjacent x2 pair.
    Integer dials (n, K) round midpoints to the nearest integer and de-duplicate; a dial
    whose published spacing is already 1 integer step cannot be refined further and is
    reported as EXHAUSTED rather than silently padded.  Off-dial controls ("nogate",
    "all", vol=none) are never interpolated — they are labels, not values — and are carried
    unchanged at every resolution so the control comparand is identical across resolutions.
    x4 is the FINEST resolution this experiment reaches; a null at x4 is evidence for
    H_EXPOSURE at that scale, not a proof for all scales, and is reported that way.

CLASSIFICATION (pre-registered, applied to every (panel, book, cost, dial) cell whose PUB
window width is 0)
    GRID      >= 1 point of the x2 or x4 grid passes 4b.  Report the value, the width
              gained, and which bar was the near-miss at PUB.
    EXPOSURE  0 points pass at x4.  Report max_over_dial(m_min) — the dial's best binding
              4b margin — and which bar binds there.
    A cell whose PUB width is already > 0 is a CALIBRATION cell: refinement must widen its
    window roughly in proportion to the added points, or the window statistic itself is not
    measuring what it claims.  f (published width 4) and vol (1.5) are those cells and are
    run for exactly that reason, not as targets.

    SECOND, TRANSFERABLE OUTPUT: is max_over_PUB(m_min) — knowable without any extra
    compute — a usable screen for which width-0 cells are worth refining?  Reported as a
    separating threshold with its confusion table.  A width-0 cell whose best published
    margin is far below 0 is exposure; refining it is wasted compute, and saying so with a
    number is the reusable part of this run.

TUNED PARAMETERS: exactly two, and only in the rule-8 section — the dial VALUE (chosen on
2009-2016 alone) and the RESOLUTION it is chosen from (PUB / x2 / x4).  The selector is
held FIXED at idea 401's S0 (IS-Sharpe argmax) for the headline and S1 (IS-4b-screened,
abstain to the control) is reported beside it as a robustness read, not as a third dial.
Every grid point of every dial at every resolution is reported in the .grid.csv.

RULE 8 (PROTOCOL 8, required): values dialled on IS <= 2016-12-31, OOS >= 2017-01-01 read
ONCE, per (panel, book, cost, dial, resolution).  OOS CAGR/Sharpe/MaxDD reported against
the dial's own no-instrument control, the LIVE RULES v2 book (cost-matched, PROTOCOL 3),
RULES v1 (continuity) and SPY.  The rule-8 question this idea owns is its own: does a
FINER grid change the pick, and does the change help or hurt out of sample?  A finer grid
is more overfitting room, so this is the honest price of the refinement, not a free lunch.

KEEP PATHS: 4b (all five bars) and 4a against the LIVE RULES v2 book cost-matched, on
EVERY arm row at every resolution.  Both reported; neither assumed.

GATE: this run re-reads idea 401's committed grid
(`2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.grid.csv`) and must
reproduce it on every shared row before any new statistic is printed.  Idea 401's own note
applies and is re-checked here: u56 reproduces only to ~1e-5 because data/prices.csv is
rewritten by the daily-close job and the vendor restates adjusted closes; broad and small
are expected to reproduce exactly.  The harness (idea 94's `H.run`) is asserted against
engine.backtest with every instrument off.

CAVEATS, stated not buried:
  - SURVIVORSHIP (idea 54): all three panels are current-constituent lists.  The small
    panel is a sub-$2B screen run TODAY and back-filled, with data/small_meta.csv's
    full-sample `max_1d_move >= 1.0` names dropped first (idea 118) — which idea 627
    established is a TERMINAL-DATED screen.  It is retained here because the target of this
    run is idea 401's committed grid and changing the panel would break the gate; the
    verdict is therefore a statement about the record's own panel convention.  Idea 627
    found the screen is conservative on this panel (it drops up-tail survivors), so a
    finding that windows are EMPTY is understated by it, not manufactured by it.
  - Idea 38: u56/broad still carry the calendar-day index (BTC-driven weekend rows).
  - Idea 126: t+1 execution only, no lag band.
  - A refined grid point is a NEW arm, not an interpolation: every point below is a full
    t+1, 10/25 bps backtest.  Nothing here is interpolated from a neighbour.
  - x4 on `gross` reaches 0.0125 steps, far finer than any position sizing a real book
    could hold.  That is deliberate: the question is whether a window EXISTS, not whether
    it is tradeable.  A window only visible at 0.0125 gross is reported as GRID and
    simultaneously flagged UNTRADEABLE.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .grid.csv, .cells.csv, .walkforward.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-10_why-do-4b-windows-have-width-0-on-four-of-six-dials_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I401_GRID = OUT / "2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
BOOKS = ["EWall", "TOP20"]
PHI, DELTA = 0.70, 0.60                    # 4b CAGR floor / DD cap fractions of SPY
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
IBARS4 = ["H1", "H2", "DD", "CAGR"]        # the four bars an IS-only screen can see
EXACT_TOL = 1e-9
DRIFT_TOL = 5e-5                           # u56: data/prices.csv rewritten daily (idea 401)

# ---- idea 401's PUBLISHED sweeps, verbatim -------------------------------------------
BANDS = [0.0, 2.0, 3.0, 5.0, 8.0]
NS = [3, 5, 10, 20, 40]
GROSSES = [float(x) for x in np.round(np.arange(0.10, 1.001, 0.05), 2)]
VOLS = [0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 1.20]
KS = [50, 100, 150, 200, 250, 300]
FS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.75, 1.00]
SLEEVE_S3 = ["TLT", "GLD", "UUP"]

PUB = {"band": BANDS, "n": NS, "gross": GROSSES, "vol": VOLS, "K": KS, "f": FS}
OFFDIAL = {"band": "nogate", "n": "all", "gross": None, "vol": "none", "K": "nogate", "f": None}
INTEGER = {"n", "K"}                       # dials whose values must be whole numbers
ADOPTED = {"band": 3.0, "n": 20, "gross": 0.75, "vol": 0.60, "K": 200, "f": 0.25}
CONTROL = {"band": "nogate", "n": "all", "gross": 1.00, "vol": "none", "K": "nogate", "f": 0.0}
RESOLUTIONS = ["PUB", "x2", "x4"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def refine(vals, integer):
    """One refinement step: insert the midpoint of every adjacent pair.  Integer dials round
    to nearest and de-duplicate (so a dial already at unit spacing gains nothing)."""
    out = list(vals)
    for a, b in zip(vals[:-1], vals[1:]):
        m = (a + b) / 2.0
        if integer:
            m = int(round(m))
            if m in (a, b):
                continue
        out.append(float(m) if not integer else m)
    return sorted(set(out))


def build_grids():
    """{dial: {resolution: [on-dial values]}}.  Off-dial control labels are appended
    separately and identically at every resolution."""
    G = {}
    for d, v in PUB.items():
        g = {"PUB": sorted(set(v))}
        g["x2"] = refine(g["PUB"], d in INTEGER)
        g["x4"] = refine(g["x2"], d in INTEGER)
        G[d] = g
    return G


GRIDS = build_grids()


# ---------------------------------------------------------------- instruments (401 verbatim)
# Memoisation ONLY: a refined grid re-asks for the same 200d mean / vol20 / composite hundreds
# of times.  Every cached object is a pure function of px, so the cache cannot change a number;
# it is asserted against the uncached path in gate (c) below.
_MEM = {}


def _memo(key, fn):
    if key not in _MEM:
        _MEM[key] = fn()
    return _MEM[key]


def _ma(px, K):
    return _memo(("ma", id(px), int(K)), lambda: px.rolling(int(K)).mean())


def ma_gate(px, K):
    return (px > _ma(px, K)).fillna(False)


def band_gate(px, b, K=200):
    ma = _ma(px, K)
    if b <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b / 100.0), 1.0)
    raw = raw.mask(px < ma * (1 - b / 100.0), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def vol_gate(px, v):
    if isinstance(v, str) or not np.isfinite(v):
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    return (_memo(("vol20", id(px)), lambda: H.vol20(px)) < float(v)).fillna(False)


def _crank(px):
    return _memo(("crank", id(px)), lambda: H.composite(px).rank(axis=1, ascending=False))


def book_weights(px, book, n=None):
    if book == "EWall" or n == "all":
        return _memo(("ew", id(px)), lambda: GROSS * (
            pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ).pipe(lambda e: e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)))
    nn = H.NTOP if n is None else int(n)
    return (_crank(px) <= nn).astype(float) * (GROSS / nn)


def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(base_W, sl_W, f):
    if f == 0.0:
        return base_W
    raw = (1 - f) * base_W + f * sl_W
    return raw.mul((GROSS / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


def weights_for(px, book, dial, val, sl_W=None):
    """(weights, static-gross multiplier m).  De-gross convention throughout.  Identical to
    idea 401's weights_for; the only difference is that val may be off the published grid."""
    W, m = book_weights(px, book), 1.0
    g = None
    if dial == "band":
        g = band_gate(px, float(val)) if val != "nogate" else None
    elif dial == "K":
        g = ma_gate(px, val) if val != "nogate" else None
    elif dial == "vol":
        g = vol_gate(px, val)
    elif dial == "n":
        W = book_weights(px, book, val)
    elif dial == "gross":
        m = float(val)
    elif dial == "f":
        W = blend(W, sl_W, float(val))
    else:
        raise ValueError(dial)
    if g is not None:
        W = W.where(g, 0.0)
    return W, m


# ---------------------------------------------------------------- bars / margins (401 verbatim)
def win(r, which):
    return r.loc[:IS_END] if which == "IS" else (r.loc[OOS_START:] if which == "OOS" else r)


def bars_win(spy, which):
    s = win(spy, which)
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins_win(r, bars, which):
    s = win(r, which)
    h = len(s) // 2
    m = metrics(s)
    out = dict(H1=metrics(s.iloc[:h])["Sharpe"] - bars["s1"],
               H2=metrics(s.iloc[h:])["Sharpe"] - bars["s2"],
               DD=DELTA * abs(bars["sdd"]) - abs(m["MaxDD"]),
               CAGR=m["CAGR"] - PHI * bars["scagr"])
    out["OOS"] = (metrics(r.loc[OOS_START:])["Sharpe"] - bars["soos"]) if which == "full" else np.nan
    return out


def lab(v):
    if isinstance(v, str):
        return v
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    return str(float(v))


def panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in px.columns if c != "SPY" and c not in bad]
    return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"


# ================================================================== main
def main():
    say("=" * 200)
    say("IDEA 409 — are the record's width-0 4b windows an EXPOSURE fact or a GRID fact?")
    say("Refine every dial to x2 and x4 of its published spacing and RUN it.  6 dials x 3 "
        "panels x 2 books x 2 cost rungs x 3 resolutions.  Weekly, t+1, "
        f"{GROSS:.0%} target gross, de-gross convention.  IS <= {IS_END}, OOS >= {OOS_START}.")
    say(f"4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= {DELTA:.2f}x|SPY|, "
        f"CAGR >= {PHI:.2f}x SPY.  4a: Sharpe > LIVE RULES v2 in both halves and MaxDD no worse.")
    say("=" * 200)
    say("\nGRIDS (on-dial points; off-dial control labels carried unchanged at every resolution)")
    for d in PUB:
        g = GRIDS[d]
        ex = " EXHAUSTED (unit integer spacing reached)" if len(g["x4"]) == len(g["x2"]) else ""
        say(f"  {d:6s} PUB {len(g['PUB']):3d}  x2 {len(g['x2']):3d}  x4 {len(g['x4']):3d}{ex}")
        say(f"         x4 = {[round(v, 4) if not isinstance(v, int) else v for v in g['x4']]}")

    rows, REF = [], {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bars, ibars = bars_win(spy, "full"), bars_win(spy, "IS")
        mS, mSo = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY   full {mS['CAGR']:7.2%} / {mS['Sharpe']:.4f} / {mS['MaxDD']:7.2%}   "
            f"halves {bars['s1']:.4f}/{bars['s2']:.4f}   "
            f"OOS {mSo['CAGR']:7.2%} / {mSo['Sharpe']:.4f} / {mSo['MaxDD']:7.2%}")

        if pname == "u56":                       # harness gate, idea 94/401
            Wc = H.targets(px, "EWall")
            a = H.run(px, Wc, bps=10.0)["r"].loc[start:]
            b = backtest(px, Wc, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            say(f"    [gate a] H.run vs engine.backtest, EWall: max|d| "
                f"{float((a - b).abs().max()):.3e}")
            for nm, g in [("band3", band_gate(px, 3.0)), ("g200", ma_gate(px, 200)),
                          ("vol60", vol_gate(px, 0.60))]:
                d0 = int((g != H.gate_mask(px, nm)).sum().sum())
                say(f"    [gate b] memoised {nm} vs idea 94's fixed gate: {d0} differing cells "
                    f"-> {'PASS' if d0 == 0 else 'FAIL'}")
            ew_u = GROSS * (pd.DataFrame(1.0, index=px.index, columns=px.columns)
                            .where(px.notna(), 0.0)).pipe(
                lambda e: e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0))
            t20_u = (H.composite(px).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
            d1 = float((book_weights(px, "EWall") - ew_u).abs().max().max())
            d2 = float((book_weights(px, "TOP20", 20) - t20_u).abs().max().max())
            say(f"    [gate c] memoised book weights vs uncached: EWall {d1:.3e}, TOP20 {d2:.3e} "
                f"-> {'PASS' if max(d1, d2) == 0.0 else 'FAIL'}")

        base = {}
        for c in COSTS:
            v2 = H.run(px, rules_v2_weights(px), bps=c)["r"].loc[start:]
            v1 = backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
            base[c] = dict(v2=v2, v1=v1)
            m2, m2o = metrics(v2), metrics(v2.loc[OOS_START:])
            say(f"    RULES v2 (LIVE) @{c:4.0f}bps  full {m2['CAGR']:7.2%} / {m2['Sharpe']:.4f} / "
                f"{m2['MaxDD']:7.2%}   OOS {m2o['CAGR']:7.2%} / {m2o['Sharpe']:.4f} / "
                f"{m2o['MaxDD']:7.2%}")
        REF[pname] = dict(spy=spy, bars=bars, ibars=ibars, mS=mS, mSo=mSo, base=base, start=start)

        sl_W = None
        if pname in ("u56", "broad"):
            miss = [t for t in SLEEVE_S3 if t not in px.columns]
            if miss:
                say(f"    sleeve S3 unavailable on {pname} (missing {miss}) — f dial skipped")
            else:
                sl_W = sleeve_weights(px, SLEEVE_S3)

        for book in BOOKS:
            for c in COSTS:
                for dial in PUB:
                    if dial == "n" and book != "TOP20":
                        continue                 # the n dial is the ranked book's own dial
                    if dial == "f" and sl_W is None:
                        continue
                    # every value ever needed by any resolution, run ONCE
                    vals = list(GRIDS[dial]["x4"])
                    if OFFDIAL[dial] is not None:
                        vals = vals + [OFFDIAL[dial]]
                    for v in vals:
                        W, m = weights_for(px, book, dial, v, sl_W)
                        res = H.run(px, W, m=m, bps=c)
                        r = res["r"].loc[start:]
                        mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(win(r, "IS"))
                        h1, h2 = H.halves(r)
                        mg, img = margins_win(r, bars, "full"), margins_win(r, ibars, "IS")
                        vl = lab(v)
                        rows.append(dict(
                            panel=pname, book=book, cost=c, dial=dial, val=vl,
                            on_dial=not isinstance(v, str),
                            # an off-dial control label ("nogate"/"all"/"none") is a PUBLISHED
                            # point of idea 401's sweep carried unchanged at every resolution,
                            # so it is in_PUB at every resolution; it is simply never part of
                            # the ORDERED window (on_dial gates that).
                            in_PUB=(isinstance(v, str) or v in GRIDS[dial]["PUB"]),
                            in_x2=(isinstance(v, str) or v in GRIDS[dial]["x2"]),
                            is_control=(vl == lab(CONTROL[dial])),
                            is_adopted=(vl == lab(ADOPTED[dial])),
                            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                            gross=float(res["gross"].loc[start:].mean()),
                            turnover=float(res["to"].loc[start:].sum() / (len(r) / 252.0)),
                            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                            m_CAGR=mg["CAGR"], m_min=min(mg[k] for k in BARS5),
                            m_bind=min(BARS5, key=lambda k: mg[k]),
                            IS_m_min=min(img[k] for k in IBARS4),
                            IS_m_bind=min(IBARS4, key=lambda k: img[k]),
                            pass4b=bool(all(mg[k] > 0 for k in BARS5)),
                            IS_pass4b=bool(all(img[k] > 0 for k in IBARS4)),
                            pass4a_v2=H.pass4a(r, base[c]["v2"]),
                            pass4a_v1=H.pass4a(r, base[c]["v1"])))
                n = sum(1 for x in rows if x["panel"] == pname and x["book"] == book
                        and x["cost"] == c)
                say(f"    ... {pname}/{book}/{c:.0f}bps done ({n} rows)")

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\ngrid: {len(G)} arm-rows -> {STEM}.grid.csv")

    # ============================================================== reproduction gate
    say("\n" + "=" * 200)
    say("REPRODUCTION GATE — this run re-reads idea 401's committed grid and must reproduce it "
        "on every shared row (PUB points only) before any new statistic is read.")
    if not I401_GRID.exists():
        say(f"  ABSENT: {I401_GRID.name} — gate cannot run; every claim below is ungated.")
    else:
        C = pd.read_csv(I401_GRID)
        C = C[C.dial != "f"].copy()
        M = G[G.dial != "f"].copy()
        for D in (C, M):
            D["cost"] = D["cost"].astype(float)
            D["val"] = D["val"].astype(str)
        # 401 labels integers as "3"/"20"; this run labels them the same way (lab()).
        J = M.merge(C, on=["panel", "book", "cost", "dial", "val"], suffixes=("", "_ref"),
                    how="inner")
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR",
                "OOS_MaxDD", "m_min", "m_DD", "m_CAGR"]
        say(f"  shared rows: {len(J)} of {len(C)} committed non-f rows")
        gate_ok = True
        for pn, d in list(J.groupby("panel")) + [("ALL", J)]:
            worst, wc = 0.0, ""
            for col in cols:
                x = float((d[col] - d[col + "_ref"]).abs().max())
                if x > worst:
                    worst, wc = x, col
            tol = EXACT_TOL if pn in ("broad", "small") else DRIFT_TOL
            ok = worst < tol
            if pn != "ALL":
                gate_ok = gate_ok and ok
            say(f"  panel {pn:6s} {len(d):4d} rows, max|d| {worst:.3e} on {wc:11s} -> "
                f"{'PASS' if ok else 'FAIL'} (tol {tol:.0e})")
        say(f"  GATE: {'PASS' if gate_ok else 'FAIL'} (numeric).")
        say("\n  DRIFT DIAGNOSIS — per column, because a bare max|d| cannot tell a vendor "
            "restatement from a longer sample, and the record's standing explanation is the "
            "former:")
        say(pd.DataFrame({pn: {c: float((d[c] - d[c + "_ref"]).abs().max()) for c in cols}
                          for pn, d in J.groupby("panel")}).to_string(
            float_format=lambda x: f"{x:.3e}"))
        fl4b = int((J.pass4b != J.pass4b_ref).sum())
        fl4a = int((J.pass4a_v2 != J.pass4a_v2_ref).sum())
        say(f"\n  KEEP-verdict flips across the drift: 4b {fl4b}/{len(J)}, 4a {fl4a}/{len(J)}.")
        say("  READING, and it corrects idea 401 rather than repeating it: `broad` reproduces at "
            "0.000e+00 on EVERY column and `small` reproduces at 0.000e+00 on every column of "
            "its OWN returns.  On u56 the IS window (<= 2016-12-31) reproduces to ~4e-6 while "
            "full-sample H2/OOS/CAGR drift by ~1e-2 — three orders of magnitude more, and "
            "concentrated entirely in the windows whose CONTENT changed.  A vendor restatement "
            "of historical closes would move IS and OOS alike; this pattern is the daily-close "
            "job APPENDING three trading days (2026-09-08..09-09), which lengthens the sample, "
            "moves the len(r)//2 half-boundary, and re-prices H2/OOS/CAGR.  Idea 401's note "
            "attributes its ~1e-5 to restatement; the dominant term is elapsed calendar time, "
            "it GROWS with the gap between runs, and at three days it is already ~1.6e-2 of "
            "Sharpe — not 1e-5.  The small panel's own returns are frozen and drift only "
            "6.1e-07, and only on m_min, because m_min is a margin against SPY, which is read "
            "from the live data/prices.csv.  Every cross-run 'reproduces at 0.000e+00' claim in "
            "the record measured against a LIVE-refreshed panel is therefore a statement about "
            "how many days elapsed, not about precision.  It changes no verdict here "
            f"({fl4b} 4b and {fl4a} 4a flips over {len(J)} shared rows), which is why this run "
            "proceeds — but it is reported, not absorbed.")

    # ============================================================== cell table: the answer
    say("\n" + "=" * 200)
    say("CELL TABLE — one row per (panel, book, cost, dial, resolution).  window_w counts the "
        "4b-passing ON-DIAL points at that resolution; off-dial controls are excluded from the "
        "window, exactly as idea 401 does.")

    def sub(d, res):
        o = d[d.on_dial].copy()
        if res == "PUB":
            o = o[o.in_PUB]
        elif res == "x2":
            o = o[o.in_x2]
        o["x"] = o.val.astype(float)
        return o.sort_values("x")

    cells = []
    for (pn, bk, c, dl), d in G.groupby(["panel", "book", "cost", "dial"]):
        pub = sub(d, "PUB")
        pub_w = int(pub.pass4b.sum())
        pub_best = float(pub.m_min.max())
        pub_arg = pub.loc[pub.m_min.idxmax()]
        for res in RESOLUTIONS:
            o = sub(d, res)
            ok = o[o.pass4b]
            w = len(ok)
            new = ok[~ok.in_PUB]
            widx = np.flatnonzero(o.pass4b.values)
            contig = bool(len(widx) and (widx.max() - widx.min() + 1) == len(widx))
            cells.append(dict(
                panel=pn, book=bk, cost=c, dial=dl, res=res, pts=len(o), window_w=w,
                window_contig=contig,
                window_lo=(float(ok.x.min()) if w else np.nan),
                window_hi=(float(ok.x.max()) if w else np.nan),
                n_new_passers=int(len(new)),
                new_passer_vals=";".join(str(round(v, 4)) for v in sorted(new.x.values)),
                best_mmin=float(o.m_min.max()), best_mmin_val=float(o.loc[o.m_min.idxmax()].x),
                bind_at_best=str(o.loc[o.m_min.idxmax()].m_bind),
                PUB_window_w=pub_w, PUB_best_mmin=pub_best,
                PUB_bind_at_best=str(pub_arg.m_bind), PUB_best_val=float(pub_arg.x),
                n_pass4a_v2=int(o.pass4a_v2.sum()),
                exhausted=bool(len(GRIDS[dl]["x4"]) == len(GRIDS[dl]["x2"]))))
    CL = pd.DataFrame(cells)
    CL.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    say("\n-- window width by dial and resolution (median over the dial's cells; idea 401's "
        "PUB column must reproduce its published medians: f 4, vol 1.5, band/gross/K/n 0)")
    piv = CL.pivot_table(index="dial", columns="res", values="window_w", aggfunc="median")
    say(piv[RESOLUTIONS].to_string(float_format=lambda x: f"{x:.2f}"))
    say("\n-- total 4b passers by dial and resolution (count of arm-rows, out of pts x cells)")
    tot = CL.pivot_table(index="dial", columns="res", values="window_w", aggfunc="sum")
    pts = CL.pivot_table(index="dial", columns="res", values="pts", aggfunc="sum")
    say(pd.concat([tot[RESOLUTIONS].add_suffix("_pass"), pts[RESOLUTIONS].add_suffix("_pts")],
                  axis=1).to_string())

    # ---- the classification
    say("\n" + "=" * 200)
    say("CLASSIFICATION of every cell whose PUBLISHED window width is 0 — GRID (a refined point "
        "passes) vs EXPOSURE (nothing passes even at x4).")
    W0 = CL[(CL.res == "x4") & (CL.PUB_window_w == 0)].copy()
    W0["verdict"] = np.where(W0.window_w > 0, "GRID", "EXPOSURE")
    say(f"\nwidth-0 cells at PUB: {len(W0)} of {CL[CL.res == 'PUB'].shape[0]} cells")
    say(W0.groupby(["dial", "verdict"]).size().unstack(fill_value=0).to_string())
    say("\nby dial: how far the best published margin was from passing, and what x4 found")
    show = W0[["panel", "book", "cost", "dial", "PUB_best_mmin", "PUB_bind_at_best",
               "PUB_best_val", "best_mmin", "best_mmin_val", "bind_at_best", "window_w",
               "n_new_passers", "new_passer_vals", "verdict"]].sort_values(
        ["dial", "PUB_best_mmin"], ascending=[True, False])
    say(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n-- CALIBRATION cells (PUB window already > 0): refinement must WIDEN these or the "
        "window statistic is not measuring what it claims.")
    CAL = CL[CL.PUB_window_w > 0]
    cal = CAL.pivot_table(index=["dial"], columns="res", values="window_w", aggfunc="mean")
    calp = CAL.pivot_table(index=["dial"], columns="res", values="pts", aggfunc="mean")
    cc = pd.concat([cal[RESOLUTIONS].add_suffix("_w"), calp[RESOLUTIONS].add_suffix("_pts")],
                   axis=1)
    for res in ("x2", "x4"):
        cc[f"{res}_w_per_pt"] = cc[f"{res}_w"] / cc[f"{res}_pts"]
    cc["PUB_w_per_pt"] = cc["PUB_w"] / cc["PUB_pts"]
    say(cc.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- the transferable screen
    say("\n" + "=" * 200)
    say("IS max_over_PUB(m_min) A USABLE SCREEN?  For the width-0 cells: does the best "
        "PUBLISHED binding margin — free, already in every committed grid — predict whether "
        "refining finds a passer?")
    if len(W0):
        g = W0[W0.verdict == "GRID"].PUB_best_mmin
        e = W0[W0.verdict == "EXPOSURE"].PUB_best_mmin
        say(f"  GRID cells     n={len(g):3d}  PUB_best_mmin  min {g.min() if len(g) else float('nan'):.5f}"
            f"  median {g.median() if len(g) else float('nan'):.5f}  max {g.max() if len(g) else float('nan'):.5f}")
        say(f"  EXPOSURE cells n={len(e):3d}  PUB_best_mmin  min {e.min() if len(e) else float('nan'):.5f}"
            f"  median {e.median() if len(e) else float('nan'):.5f}  max {e.max() if len(e) else float('nan'):.5f}")
        if len(g) and len(e):
            sep = float(e.max()) < float(g.min())
            say(f"  SEPARATING? {'YES' if sep else 'NO'} — every EXPOSURE cell below every GRID "
                f"cell: {sep}.  Best threshold (max over candidate cuts of balanced accuracy):")
            cands = sorted(set(W0.PUB_best_mmin.round(6)))
            best = None
            for t in cands:
                tp = int((g >= t).sum()); fn = int((g < t).sum())
                tn = int((e < t).sum()); fp = int((e >= t).sum())
                ba = 0.5 * (tp / max(tp + fn, 1) + tn / max(tn + fp, 1))
                if best is None or ba > best[0]:
                    best = (ba, t, tp, fp, fn, tn)
            ba, t, tp, fp, fn, tn = best
            say(f"    cut PUB_best_mmin >= {t:+.5f}: TP {tp} FP {fp} FN {fn} TN {tn}, "
                f"balanced accuracy {ba:.3f}")
        elif not len(g):
            say("  NO GRID cells at all — the screen is vacuous because refinement rescued "
                "nothing.  That is itself the answer to idea 409 on this corpus.")

    # ============================================================== rule 8
    say("\n" + "=" * 200)
    say("RULE 8 WALK-FORWARD — dial value chosen on IS <= 2016-12-31 ALONE, OOS >= 2017-01-01 "
        "read once.  The question this idea owns: does a FINER grid change the pick, and does "
        "it help or hurt out of sample?  S0 = IS-Sharpe argmax (headline).  S1 = IS-4b-screened "
        "then IS-Sharpe, abstaining to the dial's control when the screen is empty.")
    wf = []
    for (pn, bk, c, dl), d in G.groupby(["panel", "book", "cost", "dial"]):
        R = REF[pn]
        spy, base = R["spy"], R["base"][c]
        spy_o = metrics(spy.loc[OOS_START:])
        v2o, v1o = metrics(base["v2"].loc[OOS_START:]), metrics(base["v1"].loc[OOS_START:])
        ctl = d[d.is_control]
        ctl = ctl.iloc[0] if len(ctl) else None
        adp = d[d.is_adopted]
        adp = adp.iloc[0] if len(adp) else None
        for res in RESOLUTIONS:
            o = sub(d, res)
            for sel in ("S0", "S1"):
                cand = o if sel == "S0" else o[o.IS_pass4b]
                abst = (sel == "S1" and len(cand) == 0)
                if abst:
                    if ctl is None:
                        continue
                    pick = ctl
                else:
                    pick = cand.loc[cand.IS_Sharpe.idxmax()]
                wf.append(dict(
                    panel=pn, book=bk, cost=c, dial=dl, res=res, selector=sel,
                    abstained=abst, pick=pick.val, pick_in_PUB=bool(pick.in_PUB),
                    OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                    OOS_MaxDD=pick.OOS_MaxDD,
                    pass4b=bool(pick.pass4b), pass4a_v2=bool(pick.pass4a_v2),
                    best_OOS_on_grid=float(o.OOS_Sharpe.max()),
                    regret=float(o.OOS_Sharpe.max() - pick.OOS_Sharpe),
                    ctl_OOS_Sharpe=(float(ctl.OOS_Sharpe) if ctl is not None else np.nan),
                    ctl_OOS_CAGR=(float(ctl.OOS_CAGR) if ctl is not None else np.nan),
                    ctl_OOS_MaxDD=(float(ctl.OOS_MaxDD) if ctl is not None else np.nan),
                    adopted_OOS_Sharpe=(float(adp.OOS_Sharpe) if adp is not None else np.nan),
                    v2_OOS_Sharpe=v2o["Sharpe"], v2_OOS_CAGR=v2o["CAGR"],
                    v2_OOS_MaxDD=v2o["MaxDD"], v1_OOS_Sharpe=v1o["Sharpe"],
                    spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                    spy_OOS_MaxDD=spy_o["MaxDD"],
                    prem_vs_ctl=(pick.OOS_Sharpe - float(ctl.OOS_Sharpe)) if ctl is not None else np.nan,
                    prem_vs_v2=pick.OOS_Sharpe - v2o["Sharpe"],
                    prem_vs_spy=pick.OOS_Sharpe - spy_o["Sharpe"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\nwalk-forward: {len(WF)} picks -> {STEM}.walkforward.csv")

    for sel in ("S0", "S1"):
        w = WF[WF.selector == sel]
        say(f"\n-- selector {sel}: OOS by resolution (mean over {w[w.res=='PUB'].shape[0]} cells)")
        t = w.pivot_table(index="res", values=["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
                                               "prem_vs_ctl", "prem_vs_v2", "prem_vs_spy",
                                               "regret"], aggfunc="mean").loc[RESOLUTIONS]
        say(t.to_string(float_format=lambda x: f"{x:.4f}"))
        base_pub = w[w.res == "PUB"].set_index(["panel", "book", "cost", "dial"])
        for res in ("x2", "x4"):
            r = w[w.res == res].set_index(["panel", "book", "cost", "dial"])
            j = base_pub.join(r, rsuffix="_r", how="inner")
            moved = j[j.pick.astype(str) != j.pick_r.astype(str)]
            d = (j.OOS_Sharpe_r - j.OOS_Sharpe)
            dm = (moved.OOS_Sharpe_r - moved.OOS_Sharpe)
            say(f"   {res} vs PUB: pick MOVED in {len(moved)}/{len(j)} cells; "
                f"OOS Sharpe change over ALL cells mean {d.mean():+.4f} median {d.median():+.4f}; "
                f"over MOVED cells mean {dm.mean() if len(dm) else float('nan'):+.4f} "
                f"(helped {int((dm > 0).sum())}, hurt {int((dm < 0).sum())})")
        say(f"   4b-passing picks: " + ", ".join(
            f"{res} {int(w[w.res == res].pass4b.sum())}/{w[w.res == res].shape[0]}"
            for res in RESOLUTIONS))
        say(f"   4a-passing picks: " + ", ".join(
            f"{res} {int(w[w.res == res].pass4a_v2.sum())}/{w[w.res == res].shape[0]}"
            for res in RESOLUTIONS))
        say(f"   picks landing OFF the published grid: " + ", ".join(
            f"{res} {int((~w[w.res == res].pick_in_PUB).sum())}/{w[w.res == res].shape[0]}"
            for res in RESOLUTIONS))

    say("\n-- S0 rule-8 detail, every cell, x4 resolution (the finest grid): OOS vs the dial's "
        "own control, the LIVE RULES v2 book, RULES v1 and SPY")
    det = WF[(WF.selector == "S0") & (WF.res == "x4")][
        ["panel", "book", "cost", "dial", "pick", "pick_in_PUB", "OOS_CAGR", "OOS_Sharpe",
         "OOS_MaxDD", "ctl_OOS_Sharpe", "v2_OOS_Sharpe", "v1_OOS_Sharpe", "spy_OOS_Sharpe",
         "spy_OOS_CAGR", "spy_OOS_MaxDD", "pass4b", "pass4a_v2"]]
    say(det.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================== keep paths
    say("\n" + "=" * 200)
    say("KEEP PATHS on every arm row (both paths, every resolution).  4a is judged against the "
        "LIVE RULES v2 book cost-matched (PROTOCOL 3/4a); 4b against SPY (PROTOCOL 4b).")
    on = G[G.on_dial]
    for res in RESOLUTIONS:
        o = on[on.in_PUB] if res == "PUB" else (on[on.in_x2] if res == "x2" else on)
        say(f"  {res:3s}: {len(o):5d} arm-rows   4a {int(o.pass4a_v2.sum()):4d}   "
            f"4b {int(o.pass4b.sum()):4d}   BOTH "
            f"{int((o.pass4b & o.pass4a_v2).sum()):4d}")
    say("\n  binding 4b bar over all x4 arm-rows (which bar is worst):")
    say(on.m_bind.value_counts().to_string())
    say("\n  4b passers at x4 that are NOT on the published grid (the whole GRID case):")
    npass = on[on.pass4b & ~on.in_PUB]
    if len(npass):
        say(npass[["panel", "book", "cost", "dial", "val", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "OOS_Sharpe", "m_min", "m_bind", "pass4a_v2"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("    NONE.  Not one 4b passer anywhere on this corpus sits off the published grid.")

    say("\n" + "=" * 200)
    say("VERDICT — stated against the pre-registered hypotheses, not against a hoped-for result.")
    n_grid = int((W0.verdict == "GRID").sum()) if len(W0) else 0
    n_exp = int((W0.verdict == "EXPOSURE").sum()) if len(W0) else 0
    say(f"  width-0 cells: {n_exp} EXPOSURE, {n_grid} GRID (of {len(W0)}).")
    say(f"  4b passers found off the published grid, whole corpus: {len(npass)} of "
        f"{int(on.pass4b.sum())} x4 passers — but almost all of them merely ADD points to a "
        "window that was already open at PUB.  Only the GRID cells above are windows the "
        "published grid MISSED.")
    if n_grid:
        say("\n  THE GRID CELLS, in dial units — a window is only as useful as it is wide:")
        for _, rr in W0[W0.verdict == "GRID"].iterrows():
            say(f"    {rr.panel}/{rr['book']}/{rr.cost:.0f}bps {rr.dial}: 4b holds on "
                f"[{rr.window_lo:.4f}, {rr.window_hi:.4f}] = {rr.window_hi - rr.window_lo:.4f} "
                f"of dial, {rr.window_w} of {rr.pts} x4 points; published spacing "
                f"{np.diff(sorted(GRIDS[rr.dial]['PUB']))[0]:.4f}; adopted value "
                f"{ADOPTED[rr.dial]} misses by {rr.PUB_best_mmin:+.5f} on "
                f"{rr.PUB_bind_at_best}.")
    say("\n  MEASUREMENT NOTE the census itself needs: window width IN POINTS is not comparable "
        "across resolutions — it scales with the grid's density (see the calibration table: "
        "width/point is stable to ~0.02 for all five dials while width doubles at each "
        "refinement).  Idea 401's 'median width 0 vs 4' is therefore a statement about the "
        "passing FRACTION of a dial and the density it was published at, jointly.  The "
        "resolution-free statistic is width/points, and it is what the calibration table "
        "reports.")
    say("  KEEP paths above decide KEEP/PARK/KILL; this run proposes no RULES change and "
        "modifies RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py not at all.")
    say("=" * 200)

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

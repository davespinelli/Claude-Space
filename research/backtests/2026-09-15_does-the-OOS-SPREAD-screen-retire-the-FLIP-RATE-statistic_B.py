#!/usr/bin/env python3
"""
IDEA 669 -- does-the-OOS-SPREAD-screen-retire-the-FLIP-RATE-statistic            (lane B)
=========================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  idea 668 found the pick-flip rate is ~0.5-0.8 on all five dials (no dial below 664's
  0.500) and uncorrelated with flatness (Spearman -0.15..-0.10), while the dial's OOS
  rung-to-rung spread predicts the worst-case cost of a misread at Spearman +0.83 and its
  curvature at +0.96.  Re-read the record's committed rule-8 picks with the OOS spread
  published beside each, and report how many picks were decisions rather than coin flips.
  If most were not, rule 8 needs the spread as a required field.
  Max 2 params (pick set, spread bar).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL 4, "no more than 2 tuned parameters")
-----------------------------------------------------------------------------
  TUNED (2)  : PICK SET   in {CORE5, EXT9}     -- which dials the census covers
               SPREAD BAR in {0.01,0.02,0.05,0.10,0.20,0.30,0.50}  -- ALL rungs reported
  NOT TUNED  : cost 10 bps (PROTOCOL 2), next-day execution (engine), cadence W except on
               the CADENCE dial, band 0.03, gross 0.75, n 20, MA window 200, vol exponent
               0.5, lag 1, warm-up 260 rows, IS/OOS split 2016-12-31 | 2017-01-01
               (PROTOCOL 8), tie-break = smallest rung index, misread channels and levels
               copied verbatim from idea 668.  Every one of these is the record's own live
               constant, imported or restated, never chosen by looking at an outcome.

THE THREE THINGS THIS RUN MEASURES
----------------------------------
  Q1 RETIREMENT.  Does publishing the OOS SPREAD make the FLIP RATE redundant?  For every
      pick site we publish, side by side: flip rate (668's statistic), OOS spread (the
      candidate replacement), and the quantity both are supposed to be about -- WORST COST,
      = max over honest-but-different reads of  OOS Sharpe(honest pick) - OOS Sharpe(misread
      pick).  Retirement is a CONDITIONAL claim, so it is tested conditionally: Spearman of
      each against worst cost, and the PARTIAL Spearman of flip rate given OOS spread.

  Q2 THE CENSUS.  How many committed picks were DECISIONS rather than COIN FLIPS?  A pick is
      a decision at bar b if the dial's OOS spread >= b: there was something at stake.  Every
      bar on the ladder is reported; no bar is preferred.

  Q3 IS THE SCREEN EVEN IMPLEMENTABLE?  The OOS spread is a LOOK-AHEAD quantity -- it cannot
      be known when the pick is made, so as a "required field" it can only ever be a
      REPORTING field unless its in-sample twin proxies it.  We therefore publish the IS
      spread beside it, correlate the two, and score the classification agreement at every
      bar.  The price leg (below) uses the IS spread ONLY, because that is the only version a
      book could have traded.

THE PRICE LEG (PROTOCOL 8, mandatory)
-------------------------------------
  Parameters fitted on 2009..2016 only; 2017..2026 read once.  Per panel and pick set:
    PLAIN     = equal-weight blend of each dial's rule-8 pick (argmax IS Sharpe)
    SCREENED  = same, except a dial whose IS SPREAD < bar is judged to have no decision in
                it and is replaced by that dial's LIVE CONSTANT rung (band 0.03 / n 20 /
                gross 0.75 / cadence W / vol cap OFF / MA 200 / q 0.10 / exponent 0.5 /
                lag 1).  This is what "rule 8 needs the spread as a required field" means
                operationally, and it is decidable at pick time.
    LIVE      = every dial at its live constant (the no-dial control)
  Reported against RULES v2 (the live book) and SPY on the OOS window, both halves, and
  both KEEP paths at EVERY grid point.

PANELS
------
  U56      research/universe.json ETF/mega-cap panel          baseline.load_universe()
  B136     research/universe_broad.json large caps            baseline.load_universe(broad=True)
  SMALL483 data/prices_small.csv sub-$2B panel                baseline.load_universe(small=True)
  SURVIVORSHIP (PROTOCOL 9): B136 and SMALL483 are TODAY'S constituents; names delisted or
  dropped from the screen are absent, so every level on those panels is biased upward.  The
  claims here are about WITHIN-SITE rank statistics (spreads, flip rates, partial rhos),
  which survivorship biases far less than it biases a level, but no level below is tradeable.

PRE-REGISTERED GATES (run and printed BEFORE any new number is read)
--------------------------------------------------------------------
  G1  fast_backtest == engine.backtest at 10 bps                              bar 1e-12
  G2  band_book(0.03,0.75) == baseline.rules_v2_weights                       bar 0.0 exact
  G3  band_state_w(px,0.03,200) == baseline.band_state(px,0.03)               bar 0.0 exact
  G4  score_e(px,0.5) == baseline.score(px, vol_scale=True)                   bar 1e-12
  G5a the CORE5 IS ladder LEVELS reproduce idea 668's COMMITTED curvature.csv
      (is_best, spread, margin, curv, is_sd on U56 and B136)   bar 5e-4, vintage-swept
  G5b the CORE5 PICKS reproduce idea 668's COMMITTED grid.csv control rows      exact
      (G5b is the BINDING gate: every statistic here is a within-site rank quantity)
  G6  every dial ladder contains the live constant it varies

VERDICT DISCIPLINE
------------------
  Both KEEP paths are evaluated at every grid point and all points are reported.  Nothing is
  promoted on a correlation result.  A documented KILL is the expected outcome.
"""
import sys, warnings, itertools
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score       # noqa: E402
from engine import backtest, rebalance_mask                                   # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------
COST = 10.0                     # PROTOCOL 2
FREQ0 = "W"                     # RULES v2 cadence
BAND0 = 0.03                    # RULES v2 clause 2
GROSS0 = 0.75                   # RULES v2 clause 3
N0 = 20                         # the 2026-09-04 KEEP-4b candidate's book width
MAW0 = 200                      # RULES v2 / scan.py MA window
VOLE0 = 0.5                     # baseline.score vol exponent
Q0 = 0.10                       # quantile-book live width
LAG0 = 1                        # PROTOCOL 2 next-day execution
CAP0 = 9.99                     # vol cap OFF (RULES v2 has no vol filter)
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"

BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
NS = [3, 5, 10, 15, 20, 30, 40, 50]
GROSSES = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]
VOLCAPS = [0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 9.99]
CADENCES = ["D", "W", "M", "Q"]
MAWINS = [50, 100, 150, 200, 250]          # all <= WARM so every rung is warm at the start
QUANTS = [0.02, 0.05, 0.10, 0.15, 0.25, 0.40, 0.60]
VOLEXPS = [0.00, 0.25, 0.50, 0.75, 1.00]
LAGS = [1, 2, 3, 4, 5]

CORE5 = ["BAND", "N", "GROSS", "VOLCAP", "CADENCE"]          # idea 668's committed dial set
EXT4 = ["MAWIN", "QUANT", "VOLEXP", "LAG"]
PICKSETS = {"CORE5": CORE5, "EXT9": CORE5 + EXT4}
LIVE_RUNG = {"BAND": BAND0, "N": N0, "GROSS": GROSS0, "VOLCAP": CAP0, "CADENCE": FREQ0,
             "MAWIN": MAW0, "QUANT": Q0, "VOLEXP": VOLE0, "LAG": LAG0}

CHANNELS = {"ROUND": [10, 3, 2, 1, 0],
            "WINDOW": ["IS", "IS_H2", "TRAIL5Y", "TRAIL3Y", "FULL"],
            "BOOK": [0, 1, 2, 3, -1]}
CTRL = {"ROUND": 10, "WINDOW": "IS", "BOOK": 0}
CHEAT = {"FULL"}                # a read window past IS_END is look-ahead: flagged, excluded

BARS = [0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50]

_I668 = "2026-09-10_is-the-PICK-FLIP-rate-of-0.50-a-property-of-the-BAND-LADDER-or-of-every-dial_cloud"
IDEA668_CURV = OUT / f"{_I668}.curvature.csv"
IDEA668_GRID = OUT / f"{_I668}.grid.csv"

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# =========================================================================================
# 1.  ENGINE (vectorised equivalent of engine.backtest; asserted against it in G1)
# =========================================================================================
def fast_backtest(prices, weights, freq=FREQ0, cost=None):
    cost = COST if cost is None else cost          # module-level COST, so the ladder can move it
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
    gross_r = (held * rets).sum(axis=1)
    return pd.Series(gross_r - turn * cost / 1e4, index=idx)


def S(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    v = r.std() * np.sqrt(252)
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / v if v else np.nan,
                MaxDD=(eq / eq.cummax() - 1).min(),
                H1=S(r.iloc[:h]), H2=S(r.iloc[h:]))


# =========================================================================================
# 2.  THE BOOKS
# =========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_state_w(px, band, win):
    """baseline.band_state generalised in the MA window (win=200 is the live constant)."""
    ma = px.rolling(win).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def band_book(px, band, gross, win=MAW0):
    return ew_gross(px, gross).where(band_state_w(px, band, win) & px.notna(), 0.0)


def score_e(px, e):
    """baseline.score generalised in the vol exponent (e=0.5 is the live constant)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    s = comp * (0.5 + 0.5 * above.astype(float))
    if e > 0:
        s = s / vol20.clip(lower=0.08) ** e
    return s, above, vol20


def ranked_book(px, sc, above, vol20, n, gross, max_vol):
    elig = sc.where(above & (vol20 < max_vol))
    sel = (elig.rank(axis=1, ascending=False) <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(gross / k, axis=0).fillna(0.0)


def quantile_book(px, sc, above, vol20, q, gross):
    """Hold the top q FRACTION of eligible names (the record's quantile-width family)."""
    elig = sc.where(above & (vol20 < CAP0))
    n_elig = elig.notna().sum(axis=1)
    want = np.maximum(1, np.round(q * n_elig).astype(int))
    rk = elig.rank(axis=1, ascending=False)
    sel = rk.le(pd.Series(want, index=px.index), axis=0).astype(float)
    sel = sel.where(elig.notna(), 0.0)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(gross / k, axis=0).fillna(0.0)


def build_dials(px, want):
    """{dial: (rungs, {rung: OOS-window-ready daily return series})} for one panel."""
    start = px.index[WARM]
    sc, above, vol20 = score_e(px, VOLE0)
    D = {}
    if "BAND" in want:
        D["BAND"] = (BANDS, {r: fast_backtest(px, band_book(px, r, GROSS0)).loc[start:]
                             for r in BANDS})
    if "N" in want:
        D["N"] = (NS, {r: fast_backtest(px, ranked_book(px, sc, above, vol20, r, GROSS0, CAP0)
                                        ).loc[start:] for r in NS})
    if "GROSS" in want:
        D["GROSS"] = (GROSSES, {r: fast_backtest(px, band_book(px, BAND0, r)).loc[start:]
                                for r in GROSSES})
    if "VOLCAP" in want:
        D["VOLCAP"] = (VOLCAPS, {r: fast_backtest(px, ranked_book(px, sc, above, vol20, N0,
                                                                  GROSS0, r)).loc[start:]
                                 for r in VOLCAPS})
    if "CADENCE" in want:
        w = band_book(px, BAND0, GROSS0)
        D["CADENCE"] = (CADENCES, {r: fast_backtest(px, w, r).loc[start:] for r in CADENCES})
    if "MAWIN" in want:
        D["MAWIN"] = (MAWINS, {r: fast_backtest(px, band_book(px, BAND0, GROSS0, r)).loc[start:]
                               for r in MAWINS})
    if "QUANT" in want:
        D["QUANT"] = (QUANTS, {r: fast_backtest(px, quantile_book(px, sc, above, vol20, r,
                                                                  GROSS0)).loc[start:]
                               for r in QUANTS})
    if "VOLEXP" in want:
        bk = {}
        for r in VOLEXPS:
            s2, a2, v2 = score_e(px, r)
            bk[r] = fast_backtest(px, ranked_book(px, s2, a2, v2, N0, GROSS0, CAP0)).loc[start:]
        D["VOLEXP"] = (VOLEXPS, bk)
    if "LAG" in want:
        w = band_book(px, BAND0, GROSS0)
        D["LAG"] = (LAGS, {r: fast_backtest(px, w.shift(r - 1)).loc[start:] for r in LAGS})
    return D


# =========================================================================================
# 3.  THE CHOOSER AND ITS MISREADS  (channels copied verbatim from idea 668)
# =========================================================================================
def win_slice(r, w, start):
    return {"IS": r.loc[start:IS_END], "IS_H2": r.loc["2013-01-01":IS_END],
            "TRAIL5Y": r.loc["2012-01-01":IS_END], "TRAIL3Y": r.loc["2014-01-01":IS_END],
            "FULL": r.loc[start:]}[w]


def reads_for(rungs, books, channel, level, start):
    out = {}
    for i, rg in enumerate(rungs):
        if channel == "WINDOW":
            out[rg] = S(win_slice(books[rg], level, start))
        elif channel == "ROUND":
            out[rg] = round(S(win_slice(books[rg], "IS", start)), int(level))
        else:
            j = int(np.clip(i + int(level), 0, len(rungs) - 1))
            out[rg] = S(win_slice(books[rungs[j]], "IS", start))
    return out


def argmax_pick(rungs, rd):
    """argmax of the read, ties to the SMALLEST RUNG INDEX (idea 668's convention)."""
    best, bi = -np.inf, None
    for i, rg in enumerate(rungs):
        if rd[rg] > best + 1e-15:
            best, bi = rd[rg], i
    return rungs[bi], bi, best


def keeppaths(r, base, spy):
    """PROTOCOL 4a and 4b, verbatim, on the full common sample (4b's OOS leg included)."""
    m, mb, ms = M(r), M(base), M(spy)
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"])
           and (S(r.loc[OOS_START:]) > S(spy.loc[OOS_START:]))
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b), m


# =========================================================================================
# 4.  RANK STATISTICS  (statistic and n named beside every number -- open idea 564)
# =========================================================================================
def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan, int(ok.sum())
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan, int(ok.sum())
    return float(np.corrcoef(ra, rb)[0, 1]), int(ok.sum())


def partial_spearman(y, x, z):
    """Spearman(y, x | z): correlate the rank residuals of y and x after OLS on rank(z)."""
    y, x, z = (np.asarray(v, float) for v in (y, x, z))
    ok = np.isfinite(y) & np.isfinite(x) & np.isfinite(z)
    if ok.sum() < 4:
        return np.nan, int(ok.sum())
    ry, rx, rz = (pd.Series(v[ok]).rank().values for v in (y, x, z))
    Z = np.column_stack([np.ones(len(rz)), rz])
    ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
    ex = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
    if ey.std() == 0 or ex.std() == 0:
        return np.nan, int(ok.sum())
    return float(np.corrcoef(ey, ex)[0, 1]), int(ok.sum())


def r2(y, X):
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[ok], X[ok]
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ b
    ss = ((y - y.mean()) ** 2).sum()
    return float(1 - (res ** 2).sum() / ss) if ss > 0 else np.nan


# =========================================================================================
# 5.  GATES
# =========================================================================================
def gates(panels):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]

    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == baseline.rules_v2_weights      : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= (g2 == 0.0)

    g3 = int((band_state_w(px, BAND0, MAW0).values != band_state(px, BAND0).values).sum())
    P(f"  G3 band_state_w(.,0.03,200) == baseline.band_state         : {g3} cells differ  "
      f"{'PASS' if g3 == 0 else 'FAIL'}")
    ok &= (g3 == 0)

    s_mine, a_mine, v_mine = score_e(px, VOLE0)
    s_base, a_base, v_base = score(px, vol_scale=True)
    g4 = float(np.nanmax(np.abs(s_mine.values - s_base.values)))
    P(f"  G4 score_e(.,0.5) == baseline.score(vol_scale=True)        : {g4:.3e}  "
      f"{'PASS' if g4 < 1e-12 else 'FAIL'}")
    ok &= (g4 < 1e-12)

    slow = backtest(px, w, cost_bps=COST, freq=FREQ0)["returns"]
    fast = fast_backtest(px, w)
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast_backtest == engine.backtest @10 bps                : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= (g1 < 1e-12)

    P(f"  G6 every dial ladder contains its live constant            : "
      f"{all(LIVE_RUNG[d] in {'BAND': BANDS, 'N': NS, 'GROSS': GROSSES, 'VOLCAP': VOLCAPS, 'CADENCE': CADENCES, 'MAWIN': MAWINS, 'QUANT': QUANTS, 'VOLEXP': VOLEXPS, 'LAG': LAGS}[d] for d in LIVE_RUNG)}")
    ok &= all(LIVE_RUNG[d] in {"BAND": BANDS, "N": NS, "GROSS": GROSSES, "VOLCAP": VOLCAPS,
                               "CADENCE": CADENCES, "MAWIN": MAWINS, "QUANT": QUANTS,
                               "VOLEXP": VOLEXPS, "LAG": LAGS}[d] for d in LIVE_RUNG)
    return ok


def gate5(dials, panels):
    """G5a -- the CORE5 IS ladder LEVELS vs idea 668's committed curvature.csv (bar 5e-4),
       tried on today's tape and on truncations (the record's vintage convention, idea 671).
       G5b -- the CORE5 PICKS vs idea 668's committed grid.csv control rows (exact).
       G5b is the gate this run's claims actually stand on: every statistic below is a
       within-site RANK quantity, which depends on the pick and the ORDER of the ladder, not
       on the third decimal of a level."""
    if not (IDEA668_CURV.exists() and IDEA668_GRID.exists()):
        P("  G5 MISSING idea 668's committed CSVs -- gate cannot run, stated not hidden.")
        return False, pd.DataFrame()
    ref = pd.read_csv(IDEA668_CURV)
    grid = pd.read_csv(IDEA668_GRID)
    grid = grid[(grid.channel == "ROUND") & (grid.level.astype(str) == "10")]

    P("  G5a CORE5 IS ladder LEVELS vs idea 668's committed curvature.csv (bar 5e-4),")
    P("      tried on today's tape AND on truncations; the best vintage is named.")
    rows, oka = [], True
    VINTAGES = [None, "2026-09-11", "2026-09-10", "2026-09-09"]
    for (pn, dl), g in ref.groupby(["panel", "dial"]):
        if pn not in dials or dl not in dials[pn]:
            continue
        e = g.iloc[0]
        best, best_v, best_d = np.inf, None, None
        for v in VINTAGES:
            if v is None:
                rungs, books, start = dials[pn][dl]
            else:
                q = panels[pn].loc[:v]
                if len(q) < WARM + 500:
                    continue
                start = q.index[WARM]
                D = build_dials(q, [dl])
                rungs, books = D[dl]
            x = np.array([S(win_slice(books[r], "IS", start)) for r in rungs], float)
            srt = np.sort(x)[::-1]
            mine = dict(is_best=srt[0], spread=srt[0] - srt[-1], margin=srt[0] - srt[1],
                        curv=float(np.abs(np.diff(np.diff(x))).mean()),
                        is_sd=float(x.std(ddof=0)))
            d = {k: abs(mine[k] - float(e[k])) for k in mine}
            if max(d.values()) < best:
                best, best_v, best_d = max(d.values()), (v or "today"), d
        rows.append(dict(panel=pn, dial=dl, vintage=best_v,
                         **{f"d_{k}": v for k, v in best_d.items()},
                         worst=best, pass_=bool(best < 5e-4)))
        oka &= best < 5e-4
    df = pd.DataFrame(rows)
    P(f"      {int(df['pass_'].sum())} of {len(df)} sites reproduce at 5e-4; worst residual "
      f"{df['worst'].max():.3e}  {'PASS' if oka else 'FAIL'}")
    for _, r in df.sort_values("worst", ascending=False).iterrows():
        P(f"        {r['panel']:<9s} {r['dial']:<8s} worst {r['worst']:.3e}  "
          f"({r['vintage']})  {'pass' if r['pass_'] else 'FAIL'}")

    P("  G5b CORE5 PICKS vs idea 668's committed grid.csv control rows (exact match).")
    npk, tot = 0, 0
    pk_rows = []
    for _, e in grid.iterrows():
        pn, dl = e["panel"], e["dial"]
        if pn not in dials or dl not in dials[pn]:
            continue
        rungs, books, start = dials[pn][dl]
        rd = reads_for(rungs, books, "ROUND", 10, start)
        pk, pi, _ = argmax_pick(rungs, rd)
        same = (str(pk) == str(e["pick"])) and (pi == int(e["pick_i"]))
        d_oos = abs(S(books[pk].loc[OOS_START:]) - float(e["OOS_Sharpe"]))
        pk_rows.append(dict(panel=pn, dial=dl, mine=str(pk), committed=str(e["pick"]),
                            same=bool(same), d_OOS_Sharpe=d_oos))
        npk += int(same)
        tot += 1
    pk = pd.DataFrame(pk_rows)
    okb = (npk == tot)
    P(f"      {npk} of {tot} committed picks reproduce EXACTLY  {'PASS' if okb else 'FAIL'}; "
      f"max |d OOS Sharpe| on those picks {pk.d_OOS_Sharpe.max():.3e}")
    df = df.merge(pk[["panel", "dial", "mine", "committed", "same", "d_OOS_Sharpe"]],
                  on=["panel", "dial"], how="left")
    return okb, df          # G5b is binding; G5a is reported and read as a vintage statement


# =========================================================================================
# 6.  MAIN
# =========================================================================================
def main():
    P(f"IDEA 669  does-the-OOS-SPREAD-screen-retire-the-FLIP-RATE-statistic   (lane B, "
      f"{pd.Timestamp.today().date()})")
    P(f"cost {COST:.0f} bps | next-day execution | IS <= {IS_END} | OOS >= {OOS_START} | "
      f"warm-up {WARM} rows | tie-break = smallest rung index")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True),
              "SMALL483": load_universe(small=True)}
    for k, v in panels.items():
        P(f"  panel {k:<9s} {v.shape[1]:>4d} cols  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} rows)")
    P("")

    ok = gates(panels)

    # ---- build every dial on every panel -------------------------------------------------
    dials, spy, base = {}, {}, {}
    for pn, px in panels.items():
        start = px.index[WARM]
        D = build_dials(px, PICKSETS["EXT9"])
        dials[pn] = {d: (r, b, start) for d, (r, b) in D.items()}
        spy[pn] = px["SPY"].pct_change().fillna(0).loc[start:]
        base[pn] = fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0)).loc[start:]

    g5ok, g5df = gate5(dials, panels)
    ok &= g5ok
    P(f"  GATES: {'ALL PASS' if ok else 'AT LEAST ONE FAIL -- read every number below with that in mind'}")
    if len(g5df):
        dump(g5df, "gates")
    P("")

    # ---- (B) every rung of every dial, with 4a/4b ----------------------------------------
    P("=" * 100)
    P("(B) EVERY RUNG OF EVERY DIAL -- the full grid, all points reported (PROTOCOL 4)")
    P("=" * 100)
    cells = []
    for pn in panels:
        for dl, (rungs, books, start) in dials[pn].items():
            for i, rg in enumerate(rungs):
                r = books[rg]
                p4a, p4b, m = keeppaths(r, base[pn], spy[pn])
                oos = r.loc[OOS_START:]
                cells.append(dict(panel=pn, dial=dl, rung=str(rg), rung_i=i,
                                  IS_Sharpe=S(win_slice(r, "IS", start)),
                                  CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                  H1=m["H1"], H2=m["H2"], OOS_CAGR=M(oos)["CAGR"],
                                  OOS_Sharpe=S(oos), OOS_MaxDD=M(oos)["MaxDD"],
                                  pass4a=p4a, pass4b=p4b,
                                  is_live=(rg == LIVE_RUNG[dl])))
    cells = pd.DataFrame(cells)
    dump(cells, "cells")
    P(f"  {len(cells)} (panel x dial x rung) cells.  4a passes {int(cells.pass4a.sum())}, "
      f"4b passes {int(cells.pass4b.sum())} at 10 bps.")
    P("")

    # ---- (C) the misread grid: flip rate and worst cost per site -------------------------
    P("=" * 100)
    P("(C) THE PICK SITES -- flip rate (668's statistic) and OOS spread, side by side")
    P("=" * 100)
    flips, sites = [], []
    for pn in panels:
        for dl, (rungs, books, start) in dials[pn].items():
            ctl_rd = reads_for(rungs, books, "ROUND", CTRL["ROUND"], start)
            ctl_pick, ctl_i, _ = argmax_pick(rungs, ctl_rd)
            ctl_oos = S(books[ctl_pick].loc[OOS_START:])
            is_x = np.array([S(win_slice(books[r], "IS", start)) for r in rungs], float)
            oos_x = np.array([S(books[r].loc[OOS_START:]) for r in rungs], float)
            srt = np.sort(is_x)[::-1]
            n_lv, n_fl, costs = 0, 0, []
            for ch, levels in CHANNELS.items():
                for lv in levels:
                    cheat = lv in CHEAT
                    if lv == CTRL[ch]:
                        continue
                    rd = reads_for(rungs, books, ch, lv, start)
                    pk, pi, _ = argmax_pick(rungs, rd)
                    d = S(books[pk].loc[OOS_START:]) - ctl_oos
                    flips.append(dict(panel=pn, dial=dl, channel=ch, level=str(lv),
                                      cheat=cheat, flip=bool(pk != ctl_pick), pick=str(pk),
                                      ctl_pick=str(ctl_pick), d_OOS_Sharpe=d))
                    if not cheat:
                        n_lv += 1
                        n_fl += int(pk != ctl_pick)
                        costs.append(-d)            # cost = honest OOS - misread OOS
            sites.append(dict(
                panel=pn, dial=dl, n_rungs=len(rungs), pick=str(ctl_pick), pick_i=ctl_i,
                live_rung=str(LIVE_RUNG[dl]), pick_is_live=bool(ctl_pick == LIVE_RUNG[dl]),
                is_best=srt[0], is_margin=srt[0] - srt[1], is_spread=srt[0] - srt[-1],
                is_sd=float(is_x.std(ddof=0)),
                oos_spread=float(np.nanmax(oos_x) - np.nanmin(oos_x)),
                oos_sd=float(np.nanstd(oos_x)),
                oos_pick=ctl_oos, oos_best=float(np.nanmax(oos_x)),
                regret_vs_best=float(np.nanmax(oos_x)) - ctl_oos,
                oos_vs_median=ctl_oos - float(np.nanmedian(oos_x)),
                n_levels=n_lv, n_flips=n_fl, flip_rate=n_fl / n_lv if n_lv else np.nan,
                worst_cost=float(np.nanmax(costs)) if costs else np.nan,
                mean_cost=float(np.nanmean(costs)) if costs else np.nan))
    flips = pd.DataFrame(flips)
    sites = pd.DataFrame(sites)
    dump(flips, "flips")
    dump(sites, "sites")

    cols = ["panel", "dial", "pick", "is_margin", "is_spread", "oos_spread", "flip_rate",
            "worst_cost", "regret_vs_best"]
    P("")
    P("  THE TABLE THE QUEUE ASKED FOR -- every committed pick site with its OOS SPREAD:")
    P(sites[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---- (D) Q1 retirement ---------------------------------------------------------------
    P("=" * 100)
    P("(D) Q1 -- DOES THE OOS SPREAD RETIRE THE FLIP RATE?")
    P("=" * 100)
    corr = []
    for ps, dl_set in PICKSETS.items():
        sub = sites[sites.dial.isin(dl_set)]
        for tgt in ["worst_cost", "mean_cost", "regret_vs_best"]:
            r_sp, n1 = spearman(sub[tgt], sub.oos_spread)
            r_fl, _ = spearman(sub[tgt], sub.flip_rate)
            r_is, _ = spearman(sub[tgt], sub.is_spread)
            r_mg, _ = spearman(sub[tgt], sub.is_margin)
            pr_fl, _ = partial_spearman(sub[tgt], sub.flip_rate, sub.oos_spread)
            pr_sp, _ = partial_spearman(sub[tgt], sub.oos_spread, sub.flip_rate)
            corr.append(dict(pickset=ps, target=tgt, n=n1, statistic="Spearman",
                             rho_oos_spread=r_sp, rho_flip_rate=r_fl, rho_is_spread=r_is,
                             rho_is_margin=r_mg,
                             partial_flip_given_spread=pr_fl,
                             partial_spread_given_flip=pr_sp,
                             R2_spread=r2(sub[tgt], [sub.oos_spread]),
                             R2_flip=r2(sub[tgt], [sub.flip_rate]),
                             R2_both=r2(sub[tgt], [sub.oos_spread, sub.flip_rate])))
    corr = pd.DataFrame(corr)
    dump(corr, "correlations")
    P(corr.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    for ps in PICKSETS:
        r = corr[(corr.pickset == ps) & (corr.target == "worst_cost")].iloc[0]
        P(f"  {ps:<6s} n={int(r['n'])}: worst cost vs OOS spread Spearman {r.rho_oos_spread:+.4f}; "
          f"vs flip rate {r.rho_flip_rate:+.4f};")
        P(f"         PARTIAL flip|spread {r.partial_flip_given_spread:+.4f}, "
          f"PARTIAL spread|flip {r.partial_spread_given_flip:+.4f}; "
          f"R2 spread {r.R2_spread:.4f} / flip {r.R2_flip:.4f} / both {r.R2_both:.4f} "
          f"(incremental {r.R2_both - r.R2_spread:+.4f})")
    P("")

    # ---- (E) Q2 the census ---------------------------------------------------------------
    P("=" * 100)
    P("(E) Q2 -- HOW MANY COMMITTED PICKS WERE DECISIONS RATHER THAN COIN FLIPS?")
    P("=" * 100)
    cen = []
    for ps, dl_set in PICKSETS.items():
        sub = sites[sites.dial.isin(dl_set)]
        for b in BARS:
            d_oos = (sub.oos_spread >= b)
            d_is = (sub.is_spread >= b)
            cen.append(dict(pickset=ps, bar=b, n=len(sub),
                            decisions_OOSspread=int(d_oos.sum()),
                            share_OOSspread=d_oos.mean(),
                            decisions_ISspread=int(d_is.sum()),
                            share_ISspread=d_is.mean(),
                            agree=int((d_oos == d_is).sum()),
                            agree_share=(d_oos == d_is).mean(),
                            mean_cost_decisions=float(sub.loc[d_oos, "worst_cost"].mean())
                            if d_oos.any() else np.nan,
                            mean_cost_coinflips=float(sub.loc[~d_oos, "worst_cost"].mean())
                            if (~d_oos).any() else np.nan))
    cen = pd.DataFrame(cen)
    dump(cen, "census")
    P(cen.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---- (F) Q3 is the screen implementable? --------------------------------------------
    P("=" * 100)
    P("(F) Q3 -- THE OOS SPREAD IS A LOOK-AHEAD FIELD.  DOES ITS IS TWIN PROXY IT?")
    P("=" * 100)
    prox = []
    for ps, dl_set in PICKSETS.items():
        sub = sites[sites.dial.isin(dl_set)]
        r_s, n1 = spearman(sub.oos_spread, sub.is_spread)
        r_m, _ = spearman(sub.oos_spread, sub.is_margin)
        r_sd, _ = spearman(sub.oos_spread, sub.is_sd)
        prox.append(dict(pickset=ps, n=n1, statistic="Spearman",
                         rho_oos_vs_is_spread=r_s, rho_oos_vs_is_margin=r_m,
                         rho_oos_vs_is_sd=r_sd,
                         mean_is_spread=sub.is_spread.mean(),
                         mean_oos_spread=sub.oos_spread.mean(),
                         ratio=sub.oos_spread.mean() / sub.is_spread.mean()))
    prox = pd.DataFrame(prox)
    dump(prox, "proxy")
    P(prox.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---- (G) PROTOCOL 8 walk-forward, the price leg -------------------------------------
    P("=" * 100)
    P("(G) RULE 8 WALK-FORWARD -- parameters fitted on IS only, 2017-2026 read ONCE")
    P("=" * 100)
    wf = []
    for pn in panels:
        b_oos = base[pn].loc[OOS_START:]
        s_oos = spy[pn].loc[OOS_START:]
        mb, ms = M(b_oos), M(s_oos)
        for ps, dl_set in PICKSETS.items():
            have = [d for d in dl_set if d in dials[pn]]
            picks, live = {}, {}
            for dl in have:
                rungs, books, start = dials[pn][dl]
                rd = reads_for(rungs, books, "ROUND", CTRL["ROUND"], start)
                pk, _, _ = argmax_pick(rungs, rd)
                picks[dl] = books[pk]
                live[dl] = books[LIVE_RUNG[dl]]
            arms = {"PLAIN": sum(picks[d] for d in have) / len(have),
                    "LIVE": sum(live[d] for d in have) / len(have)}
            for b in BARS:
                sel = {d: (picks[d] if float(sites[(sites.panel == pn) & (sites.dial == d)]
                                             .is_spread.iloc[0]) >= b else live[d])
                       for d in have}
                arms[f"SCREEN@{b:.2f}"] = sum(sel[d] for d in have) / len(have)
            for nm, r in arms.items():
                p4a, p4b, m = keeppaths(r, base[pn], spy[pn])
                o = r.loc[OOS_START:]
                mo = M(o)
                p4b_oos = ((S(o) > S(s_oos))
                           and (abs(mo["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
                           and (mo["CAGR"] >= 0.70 * ms["CAGR"]))
                p4a_oos = (S(o) > S(b_oos)) and (mo["MaxDD"] >= mb["MaxDD"])
                wf.append(dict(panel=pn, pickset=ps, arm=nm, n_dials=len(have),
                               FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"],
                               FULL_MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=S(o), OOS_MaxDD=mo["MaxDD"],
                               BASE_OOS_CAGR=mb["CAGR"], BASE_OOS_Sharpe=S(b_oos),
                               BASE_OOS_MaxDD=mb["MaxDD"], SPY_OOS_CAGR=ms["CAGR"],
                               SPY_OOS_Sharpe=S(s_oos), SPY_OOS_MaxDD=ms["MaxDD"],
                               pass4a_full=p4a, pass4b_full=p4b,
                               pass4a_oos=bool(p4a_oos), pass4b_oos=bool(p4b_oos)))
    wf = pd.DataFrame(wf)
    dump(wf, "walkforward")
    show = ["panel", "pickset", "arm", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "H1", "H2", "pass4a_full", "pass4b_full", "pass4a_oos", "pass4b_oos"]
    P(wf[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    for pn in panels:
        r = wf[wf.panel == pn].iloc[0]
        P(f"  {pn:<9s} OOS comparands -- RULES v2 {r.BASE_OOS_CAGR:.2%}/{r.BASE_OOS_Sharpe:.4f}/"
          f"{r.BASE_OOS_MaxDD:.2%}   SPY {r.SPY_OOS_CAGR:.2%}/{r.SPY_OOS_Sharpe:.4f}/"
          f"{r.SPY_OOS_MaxDD:.2%}")
    P("")
    dd = wf[wf.arm.str.startswith("SCREEN")].merge(
        wf[wf.arm == "PLAIN"][["panel", "pickset", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]],
        on=["panel", "pickset"], suffixes=("", "_plain"))
    dd["d_OOS_Sharpe"] = dd.OOS_Sharpe - dd.OOS_Sharpe_plain
    dd["d_OOS_CAGR"] = dd.OOS_CAGR - dd.OOS_CAGR_plain
    dd["d_OOS_MaxDD"] = dd.OOS_MaxDD - dd.OOS_MaxDD_plain
    dump(dd[["panel", "pickset", "arm", "d_OOS_Sharpe", "d_OOS_CAGR", "d_OOS_MaxDD"]],
         "screen_delta")
    P("  SCREENED minus PLAIN, OOS (the whole point of making the spread a required field):")
    P(dd[["panel", "pickset", "arm", "d_OOS_Sharpe", "d_OOS_CAGR", "d_OOS_MaxDD"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("")
    P(f"  SCREEN arms that move OOS Sharpe at all (|d| > 1e-12): "
      f"{int((dd.d_OOS_Sharpe.abs() > 1e-12).sum())} of {len(dd)}; "
      f"best {dd.d_OOS_Sharpe.max():+.4f}, worst {dd.d_OOS_Sharpe.min():+.4f}")
    P(f"  4b OOS passes: PLAIN {int(wf[wf.arm=='PLAIN'].pass4b_oos.sum())} of "
      f"{len(wf[wf.arm=='PLAIN'])}, LIVE {int(wf[wf.arm=='LIVE'].pass4b_oos.sum())} of "
      f"{len(wf[wf.arm=='LIVE'])}, SCREEN {int(dd.pass4b_oos.sum())} of {len(dd)}")
    P(f"  4a OOS passes: PLAIN {int(wf[wf.arm=='PLAIN'].pass4a_oos.sum())}, "
      f"LIVE {int(wf[wf.arm=='LIVE'].pass4a_oos.sum())}, SCREEN {int(dd.pass4a_oos.sum())}")
    P("")

    # ---- (H) cost ladder robustness ------------------------------------------------------
    P("=" * 100)
    P("(H) COST LADDER -- does the Q1 answer survive 0/5/10/25/50 bps?")
    P("=" * 100)
    lad = []
    for c in [0.0, 5.0, 10.0, 25.0, 50.0]:
        rows = []
        for pn, px in panels.items():
            start = px.index[WARM]
            D = build_dials_cost(px, PICKSETS["EXT9"], c)
            for dl, (rungs, books) in D.items():
                ctl_rd = {r: S(win_slice(books[r], "IS", start)) for r in rungs}
                pk, _, _ = argmax_pick(rungs, ctl_rd)
                ctl_oos = S(books[pk].loc[OOS_START:])
                oos_x = np.array([S(books[r].loc[OOS_START:]) for r in rungs], float)
                is_x = np.array([ctl_rd[r] for r in rungs], float)
                costs, nfl, nlv = [], 0, 0
                for ch, levels in CHANNELS.items():
                    for lv in levels:
                        if lv == CTRL[ch] or lv in CHEAT:
                            continue
                        rd = reads_for(rungs, books, ch, lv, start)
                        p2, _, _ = argmax_pick(rungs, rd)
                        costs.append(ctl_oos - S(books[p2].loc[OOS_START:]))
                        nlv += 1
                        nfl += int(p2 != pk)
                rows.append(dict(panel=pn, dial=dl, oos_spread=oos_x.max() - oos_x.min(),
                                 is_spread=is_x.max() - is_x.min(),
                                 flip_rate=nfl / nlv, worst_cost=max(costs)))
        rw = pd.DataFrame(rows)
        for ps, dl_set in PICKSETS.items():
            s2 = rw[rw.dial.isin(dl_set)]
            a, n1 = spearman(s2.worst_cost, s2.oos_spread)
            b2, _ = spearman(s2.worst_cost, s2.flip_rate)
            pf, _ = partial_spearman(s2.worst_cost, s2.flip_rate, s2.oos_spread)
            pi, _ = spearman(s2.oos_spread, s2.is_spread)
            lad.append(dict(cost_bps=c, pickset=ps, n=n1, rho_spread=a, rho_flip=b2,
                            partial_flip_given_spread=pf, rho_oos_vs_is_spread=pi,
                            mean_flip_rate=s2.flip_rate.mean(),
                            mean_worst_cost=s2.worst_cost.mean()))
    lad = pd.DataFrame(lad)
    dump(lad, "costladder")
    P(lad.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


def build_dials_cost(px, want, cost):
    """build_dials at an arbitrary cost rung (cost ladder only)."""
    global COST
    old = COST
    COST = cost
    try:
        D = build_dials(px, want)
    finally:
        COST = old
    return {d: (r, b) for d, (r, b) in D.items()}


if __name__ == "__main__":
    main()

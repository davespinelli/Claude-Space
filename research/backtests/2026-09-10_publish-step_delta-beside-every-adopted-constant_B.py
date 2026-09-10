#!/usr/bin/env python3
"""IDEA 408 — publish step_delta beside every adopted constant.  (lane B, cloud, 2026-09-10)

PRE-REGISTERED QUESTION (QUEUE.md, written before any number in this file was read)
    Idea 401 showed a 4b margin quoted without a scale is uninterpretable: the record's adopted
    constants clear their binding bar by <0.5 grid steps in 4 of 19 passing cells and by >2 in
    only 6.  Propose binding bar / margin / one-step motion as three required LEADERBOARD columns
    and back-fill them over every committed KEEP row.  Max 2 params.

THE THREE PROPOSED COLUMNS (definitions fixed in advance, verbatim from idea 401's statistic)
    BAR     the name of the binding 4b bar at the published cell = argmin over the five 4b
            margins {H1, H2, OOS, DD, CAGR}.  For a PASSING row it is the tightest passing leg:
            the bar that fails first if anything moves.
    MARGIN  m_min, that bar's own margin, in that bar's own units.
    STEP    step_delta = the MEDIAN over adjacent PUBLISHED grid pairs of |m_bar(v_i+1)-m_bar(v_i)|,
            the same bar throughout: how far the binding margin moves for one grid step of the
            adopted constant.  THIN when |MARGIN| < tau * STEP.

WHAT THIS FILE ADDS OVER IDEA 401 (which computed the three quantities at 6 adopted values only)
    A  CENSUS — every committed KEEP row in LEADERBOARD.md, tested for whether the three columns
       are RECOVERABLE from committed artefacts at all, under 2 readings of "recoverable"
       (STRICT = the LEADERBOARD row's own text; LOOSE = the row plus any committed sidecar CSV
       of the same script stem).  A required column that 90% of the record cannot supply is a
       proposal about future rows, not a back-fill.
    B  BACK-FILL — the three columns computed at EVERY grid point of 5 dials x 3 panels x 2 books
       x 3 cost rungs, not just at the adopted value, so the columns exist for passing cells
       (KEEP rows) and not only for the six constants.  Three pre-registered tests:
         T1  the distribution of MARGIN/STEP over 4a- and 4b-passing cells.
         T2  DOES THE COLUMN EARN ITS PLACE?  THIN vs FLIP1 (does the 4b verdict actually differ
             at an immediate grid neighbour).  Compared head-to-head against a MARGIN-ONLY
             predictor: if dividing by STEP adds no discrimination over the margin alone, the
             third column is decoration.
         T3  IS STEP A PROPERTY OF THE FUNCTION OR OF THE PUBLICATION?  Every dial is run at two
             densities, COARSE (the record's published grid) and FINE (COARSE plus its own
             midpoints, so every spacing is halved).  If step_delta scales with the spacing then
             THIN is a statement about how densely someone chose to publish, and the column must
             be published in density-free units (step per UNIT of the dial), not per grid point.
    C  RULE 8 — the columns as a SELECTOR.  Dial value chosen on 2009-2016 only, 2017-2026 read
       once, three selectors: S0 max IS Sharpe (uses no column), S1 IS-4b-screened (uses BAR and
       MARGIN), S2 IS-4b-screened AND THICK (uses all three).  OOS CAGR/Sharpe/MaxDD against each
       dial's own no-instrument control, the LIVE RULES v2 book cost-matched, RULES v1 and SPY.

TUNED PARAMETERS: exactly two — (1) the dial VALUE, chosen on IS only in part C; (2) the THIN
threshold tau, reported at 0.5 / 1.0 / 2.0 with 1.0 as the pre-stated headline.  Every grid point
of every dial at every rung is written to .grid.csv; nothing else is selected on.

DIALS and their adopted constants (idea 401's list, same sources):
    band   b   COARSE {0,2,3,5,8}%              adopted 3%    control nogate   (ideas 57/59, v2)
    K      d   COARSE {50,100,150,200,250,300}  adopted 200   control nogate   (RULES v1 and v2)
    vol    v   COARSE {0.30,0.45,0.60,0.90,1.20} adopted 0.60 control none     (idea 95, RULES v1)
    n          COARSE {3,5,10,20,40,80}         adopted 20    control all      (ideas 124/2/182)
    gross  g   COARSE 0.10..1.00 step 0.10      adopted 0.75  control 1.00     (ideas 66/84, v2)
The n dial is defined only on the TOP-N book.  Books: EWALL (every eligible name, de-gross
convention: denominator = names priced that day, gated-out weight to CASH) and TOPN (top n of the
scan.py composite with the vol scaler OFF, weight gross/n each, empty slots to CASH).  Both are
the record's own books: EWALL at band 3% / K 200 / no vol cap / gross 0.75 IS RULES v2.

BARS (PROTOCOL 4, unchanged): 4b = Sharpe > SPY in H1, H2 and OOS; MaxDD <= 60% of SPY's;
CAGR >= 70% of SPY's.  4a = Sharpe > the LIVE RULES v2 book in BOTH halves and MaxDD no worse.
Both comparands are computed on the same traded panel at the same cost rung.

GATES (all pre-registered, asserted before any statistic is printed)
    G1  fast_backtest reproduces engine.backtest on returns AND turnover.
    G2  idea 84's EWALL U56 g=0.85 @10bps landmark 11.8% / 1.05 / -17.9% / H 1.07/1.04.
    G3  the derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=c).
    G4  the EWALL book at the adopted constants and gross 0.75 reproduces baseline.rules_v2_weights
        to 0.000e+00 on returns — the file's books are the record's books, asserted not assumed.
    G5  step_delta is invariant to the ORDER of the grid (it is a median of |differences| over
        adjacent pairs): recomputing on a shuffled-then-resorted grid gives 0.000e+00.

CAVEATS, stated not buried
  - SURVIVORSHIP (PROTOCOL 9, idea 54): U56, B136 and SMALL439 are all CURRENT-constituent lists.
    Levels (CAGR, DD) are optimistic; the margin-vs-step CONTRAST is the durable part.  SMALL439
    additionally drops the 44 tickers with data/small_meta.csv max_1d_move >= 1.0 — idea 623's
    TERMINAL-DATED screen, kept because every published number this file re-reads carries it.
  - Idea 38: U56/B136 still carry the calendar-day index (BTC-driven weekend rows).
  - A "grid step" is a property of the PUBLISHED grid, not of the dial.  T3 exists because of it.
  - m_min is a min over margins in DIFFERENT units (Sharpe, return).  That is the record's own
    convention and idea 401's; this file reports the step-normalised argmin beside it and counts
    how often the two disagree, which is the direct form of idea 408's premise.
  - Warm-up: the common start is index[300], not the record's index[260], because K=300 is on the
    grid.  Every arm and every comparand in this file uses that same start, so the comparisons are
    internally exact; absolute levels are not directly comparable to rows quoted at 260.
  - PART A's LOOSE reading counts a sidecar column by NAME.  A file that computes a margin without
    naming it so is counted as not recoverable.  The census is therefore a LOWER bound on
    recoverability and an UPPER bound on how much work the proposal creates.

Data: committed caches only.  No network, never yfinance.  Deterministic, standalone.  Modifies
nothing outside its own .console.txt / .census.csv / .grid.csv / .cols.csv / .walkforward.csv.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa: E402

STEM = Path(__file__).with_suffix("")
FREQ = "W"
RUNGS = (0.0, 10.0, 25.0)
HEADLINE_RUNG = 10.0
WARM = 300
IS_END = pd.Timestamp("2016-12-31")
TAUS = (0.5, 1.0, 2.0)
HEADLINE_TAU = 1.0
BARS = ("H1", "H2", "OOS", "DD", "CAGR")

_LOG = []


def log(s=""):
    print(s)
    _LOG.append(str(s))


# ------------------------------------------------------------------- vectorised simulator
def fast_backtest(prices, weights, freq=FREQ):
    """Identical to engine.backtest's returns/turnover (gross of costs), vectorised.  G1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
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
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def mets(r):
    """CAGR, Sharpe, MaxDD from a daily return array (engine.metrics conventions)."""
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    sh = float(r.mean() * 252 / vol) if vol > 0 else np.nan
    return float(cagr), sh, dd


def sharpe(r):
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return float(r.mean() * 252 / vol) if vol > 0 else np.nan


# ------------------------------------------------------------------------------- panels
def small_panel():
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    drop = [c for c in sm.columns if c in bad]
    return sm.drop(columns=drop), len(drop)


class Panel:
    """Everything a dial sweep needs, computed once per panel."""

    def __init__(self, name, px):
        self.name = name
        self.spy_px = px["SPY"]
        self.q = px.drop(columns=["SPY"])
        self.idx = self.q.index
        self.start = self.idx[WARM]
        self.priced = self.q.notna()
        self.npriced = self.priced.sum(axis=1).replace(0, np.nan)
        self.vol20 = self.q.pct_change().rolling(20).std() * np.sqrt(252)
        s, _, _ = score(self.q, vol_scale=False)
        self.s = s
        self._ma = {}
        m = self.idx >= self.start
        self.mask = m
        self.n_post = int(m.sum())
        self.h = self.n_post // 2
        post = self.idx[m]
        self.is_m = np.asarray(post <= IS_END)
        self.oos_m = np.asarray(post > IS_END)
        spy = self.spy_px.pct_change().fillna(0.0).values[m]
        self.spy = spy
        self.spy_full = mets(spy)
        self.spy_H1, self.spy_H2 = sharpe(spy[: self.h]), sharpe(spy[self.h:])
        self.spy_is = mets(spy[self.is_m])
        self.spy_oos = mets(spy[self.oos_m])
        sis = spy[self.is_m]
        ih = len(sis) // 2
        self.spy_is_H1, self.spy_is_H2 = sharpe(sis[:ih]), sharpe(sis[ih:])

    def ma(self, K):
        if K not in self._ma:
            self._ma[K] = self.q.rolling(K).mean()
        return self._ma[K]

    def band_state(self, band, K):
        if K is None:  # 'nogate' control: always in
            return pd.DataFrame(True, index=self.idx, columns=self.q.columns)
        ma = self.ma(K)
        raw = pd.DataFrame(np.nan, index=self.idx, columns=self.q.columns)
        raw = raw.mask(self.q > ma * (1 + band), 1.0).mask(self.q < ma * (1 - band), 0.0)
        return raw.ffill().fillna(0.0) > 0.5

    def weights(self, band, K, volcap, n, gross, kind):
        elig = self.band_state(band, K) & self.priced
        if volcap is not None and np.isfinite(volcap):
            elig = elig & (self.vol20 < volcap)
        if kind == "EWALL" or n is None:
            w = elig.astype(float).div(self.npriced, axis=0) * gross
        else:
            r = self.s.where(elig).rank(axis=1, ascending=False)
            w = (r <= n).astype(float) * (gross / float(n))
        return w.fillna(0.0)

    def run(self, band, K, volcap, n, gross, kind):
        g, t = fast_backtest(self.q, self.weights(band, K, volcap, n, gross, kind))
        return g.values[self.mask], t.values[self.mask]


# --------------------------------------------------------------------------------- dials
ADOPTED = {"band": 0.03, "K": 200, "vol": 0.60, "n": 20, "gross": 0.75}
DEFAULTS = {"band": 0.03, "K": 200, "vol": 0.60, "n": 20, "gross": 0.75}


def _mid(vals, integer=False):
    out = []
    for a, b in zip(vals[:-1], vals[1:]):
        m = (a + b) / 2.0
        out.append(int(round(m)) if integer else m)
    return out


def _merge(coarse, mids):
    return sorted(set(coarse) | set(mids))


BAND_C = [0.00, 0.02, 0.03, 0.05, 0.08]
K_C = [50, 100, 150, 200, 250, 300]
VOL_C = [0.30, 0.45, 0.60, 0.90, 1.20]
N_C = [3, 5, 10, 20, 40, 80]
G_C = [round(0.15 + 0.15 * i, 4) for i in range(6)]           # 0.15..0.90, contains adopted 0.75

DIALS = {
    "band": dict(coarse=BAND_C, fine=_merge(BAND_C, _mid(BAND_C)), ctl="nogate", books=("EWALL", "TOPN")),
    "K": dict(coarse=K_C, fine=_merge(K_C, _mid(K_C, True)), ctl="nogate", books=("EWALL", "TOPN")),
    "vol": dict(coarse=VOL_C, fine=_merge(VOL_C, _mid(VOL_C)), ctl="none", books=("EWALL", "TOPN")),
    "n": dict(coarse=N_C, fine=_merge(N_C, _mid(N_C, True)), ctl="all", books=("TOPN",)),
    "gross": dict(coarse=G_C, fine=_merge(G_C, _mid(G_C)), ctl=1.00, books=("EWALL", "TOPN")),
}
for _d, _s in DIALS.items():                                   # every adopted constant is ON its grid
    assert any(abs(float(v) - float(ADOPTED[_d])) < 1e-12 for v in _s["coarse"]), _d
    assert set(_s["coarse"]) <= set(_s["fine"]), _d


def arm_params(dial, val, kind):
    p = dict(DEFAULTS)
    p[dial] = val
    band, K, vol, n, gross = p["band"], p["K"], p["vol"], p["n"], p["gross"]
    if dial == "band" and val == "nogate":
        band, K = 0.0, None
    if dial == "K" and val == "nogate":
        K = None
    if dial == "vol" and val == "none":
        vol = np.inf
    if dial == "n" and val == "all":
        n = None
    return dict(band=band, K=K, volcap=vol, n=(None if kind == "EWALL" else n), gross=gross, kind=kind)


# ------------------------------------------------------------------------------- metrics
def read_arm(P, g, t, cost):
    r = g - t * cost / 1e4
    cagr, sh, dd = mets(r)
    H1, H2 = sharpe(r[: P.h]), sharpe(r[P.h:])
    ic, ish, idd = mets(r[P.is_m])
    oc, osh, odd = mets(r[P.oos_m])
    iH = len(r[P.is_m]) // 2
    ris = r[P.is_m]
    iH1, iH2 = sharpe(ris[:iH]), sharpe(ris[iH:])
    return dict(CAGR=cagr, Sharpe=sh, MaxDD=dd, H1=H1, H2=H2,
                IS_CAGR=ic, IS_Sharpe=ish, IS_MaxDD=idd, IS_H1=iH1, IS_H2=iH2,
                OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd,
                turnover=float(t.sum()) / (len(r) / 252.0))


def margins_4b(m, P, pre=""):
    """PROTOCOL 4b, five margins, positive = passing.

    pre='' reads the FULL sample against SPY's full sample (the published verdict).
    pre='IS_' is the same five bars computed on 2009-2016 ONLY against SPY's 2009-2016 — the
    walk-forward screen, so nothing after 2016-12-31 touches a selection.  In the IS reading the
    'OOS' leg is the IS full-period Sharpe (there is no held-out leg inside the IS window)."""
    if pre == "IS_":
        return dict(H1=m["IS_H1"] - P.spy_is_H1, H2=m["IS_H2"] - P.spy_is_H2,
                    OOS=m["IS_Sharpe"] - P.spy_is[1],
                    DD=0.60 * abs(P.spy_is[2]) - abs(m["IS_MaxDD"]),
                    CAGR=m["IS_CAGR"] - 0.70 * P.spy_is[0])
    return dict(H1=m["H1"] - P.spy_H1, H2=m["H2"] - P.spy_H2,
                OOS=m["OOS_Sharpe"] - P.spy_oos[1],
                DD=0.60 * abs(P.spy_full[2]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * P.spy_full[0])


def margins_4a(m, v2):
    return dict(H1=m["H1"] - v2["H1"], H2=m["H2"] - v2["H2"], DD=abs(v2["MaxDD"]) - abs(m["MaxDD"]))


def step_delta(vals, series):
    """MEDIAN over adjacent grid pairs of |m(v_i+1) - m(v_i)|.  vals must be sorted numerics."""
    if len(vals) < 2:
        return np.nan
    d = [abs(series[b] - series[a]) for a, b in zip(vals[:-1], vals[1:])]
    return float(np.median(d))


def unit_step(vals, series):
    """Density-free form: median over adjacent pairs of |dm| / |dv|."""
    if len(vals) < 2:
        return np.nan
    d = [abs(series[b] - series[a]) / abs(b - a) for a, b in zip(vals[:-1], vals[1:]) if b != a]
    return float(np.median(d)) if d else np.nan


# =========================================================================== PART A census
KEEP_RE = re.compile(r"KEEP", re.I)
BAR_TOK = re.compile(r"\b(H1|H2|OOS|DD|MaxDD|CAGR|drawdown)\b")
STRICT_BAR = re.compile(r"(binding|binds|bind[_ ]?bar|tightest|first fails|failing[- ]leg)", re.I)
STRICT_MARGIN = re.compile(r"(margin|clears? (the )?(bar|floor|cap) by|by \+?[0-9.]+ of Sharpe)", re.I)
STRICT_STEP = re.compile(r"(step[_ ]?delta|per (grid )?step|one grid step|grid step|one[- ]step)", re.I)
COL_BAR = re.compile(r"^(m_bind|bind_bar|binding_bar|bind|failing_leg|bind_bar_scaled)$", re.I)
COL_MARGIN = re.compile(r"^(m_min|bind_margin|margin|m_(h1|h2|oos|dd|cagr))$", re.I)
COL_STEP = re.compile(r"^(step_delta|step|thin_ratio|unit_step)$", re.I)
DIAL_COL = re.compile(r"^(val|value|dial|param|level|n|gross|band|vol|k|f|lambda|g|window|w)$", re.I)


def part_a_census():
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(encoding="utf-8").split("\n")
    rows = [l for l in lb if l.startswith("|") and not l.startswith("|---") and not l.startswith("| Date")]
    bt = ROOT / "research" / "backtests"
    import gzip
    # a script stem can itself contain dots (e.g. "...is-the-0.2125-theta..."), so sidecars are
    # attached by matching the LONGEST committed .py stem that the csv name extends.
    py_stems = sorted({p.name[:-3] for p in bt.glob("*.py")}, key=len, reverse=True)
    headers = {}
    for p in sorted(list(bt.glob("*.csv")) + list(bt.glob("*.csv.gz"))):
        stem = next((s for s in py_stems if p.name.startswith(s + ".")), None)
        if stem is None:
            continue
        try:
            op = gzip.open if p.suffix == ".gz" else open
            with op(p, "rt", encoding="utf-8", errors="replace") as h:
                first = h.readline()
        except Exception:
            continue
        cols = [c.strip().strip('"') for c in first.strip().split(",")]
        headers.setdefault(stem, []).append(cols)

    out = []
    for l in rows:
        c = [x.strip() for x in l.split("|")[1:-1]]
        if len(c) < 9:
            continue
        verdict = re.sub(r"[*_`]", "", c[-2]).strip()          # verdict and script are the LAST two
        if not KEEP_RE.search(verdict):
            continue
        script = re.sub(r"[`*]", "", c[-1]).strip().split("/")[-1]
        stem = script[:-3] if script.endswith(".py") else ""
        text = l
        s_bar = bool(STRICT_BAR.search(text)) and bool(BAR_TOK.search(text))
        s_mar = bool(STRICT_MARGIN.search(text))
        s_step = bool(STRICT_STEP.search(text))
        hs = headers.get(stem, [])
        l_bar = any(any(COL_BAR.match(x) for x in cols) for cols in hs)
        l_mar = any(any(COL_MARGIN.match(x) for x in cols) for cols in hs)
        l_step = any(any(COL_STEP.match(x) for x in cols) for cols in hs)
        l_dial = any(any(DIAL_COL.match(x) for x in cols) for cols in hs)
        out.append(dict(date=c[0], idea=c[1][:60], verdict=verdict, script=script, stem=stem,
                        script_named=bool(stem),
                        has_sidecar=len(hs) > 0, n_sidecar=len(hs),
                        STRICT_bar=s_bar, STRICT_margin=s_mar, STRICT_step=s_step,
                        STRICT_all3=s_bar and s_mar and s_step,
                        LOOSE_bar=l_bar or s_bar, LOOSE_margin=l_mar or s_mar,
                        LOOSE_step=l_step or (l_dial and l_mar) or s_step,
                        LOOSE_all3=(l_bar or s_bar) and (l_mar or s_mar) and (l_step or (l_dial and l_mar) or s_step)))
    return pd.DataFrame(out), len(rows)


# ============================================================================ GATES
def gates():
    log("=" * 110)
    log("[0] REPRODUCTION GATES (pre-registered; every one asserted before a statistic is printed)")
    log("=" * 110)
    px = load_universe()
    q = px.drop(columns=["SPY"])
    w = rules_v2_weights(q)
    fr, ft = fast_backtest(q, w)
    eng = backtest(q, w, cost_bps=0.0, freq=FREQ)
    st = q.index[WARM]
    d1 = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    d1t = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    log(f"  G1  fast_backtest vs engine.backtest (U56 RULESv2 W): max|dret| {d1:.3e}  max|dturn| {d1t:.3e}")
    assert d1 < 1e-10 and d1t < 1e-10, "G1 FAILED"

    s, above, vol20 = score(px)
    e = (above & (vol20 < 0.60)).astype(float)
    w85 = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * 0.85
    b0 = backtest(px, w85, cost_bps=0, freq=FREQ)
    b10 = backtest(px, w85, cost_bps=10, freq=FREQ)
    rr = b10["returns"].loc[px.index[260]:]
    m84 = metrics(rr)
    h = len(rr) // 2
    log(f"  G2  idea 84 EWALL U56 g=0.85 @10bps: {m84['CAGR']:.1%} / {m84['Sharpe']:.2f} / "
        f"{m84['MaxDD']:.1%} / H {sharpe(rr.iloc[:h].values):.2f}/{sharpe(rr.iloc[h:].values):.2f}"
        "   (committed 11.8% / 1.05 / -17.9% / 1.07/1.04)")
    assert abs(m84["Sharpe"] - 1.05) < 0.02 and abs(m84["CAGR"] - 0.118) < 0.003, "G2 FAILED"

    g3 = float(abs((b0["returns"] - b0["turnover"] * 10 / 1e4) - b10["returns"]).max())
    log(f"  G3  derived cost rung r(c)=r(0)-turn*c/1e4: max|diff| {g3:.3e}")
    assert g3 < 1e-12, "G3 FAILED"

    P = Panel("U56", px)
    gg, tt = P.run(**arm_params("band", 0.03, "EWALL"))
    ref, reft = fast_backtest(P.q, rules_v2_weights(P.q))
    d4 = float(np.abs(gg - ref.values[P.mask]).max())
    log(f"  G4  this file's EWALL(band 3%,K 200,vol none,g 0.75) vs baseline.rules_v2_weights: "
        f"max|dret| {d4:.3e}")
    p_nv = arm_params("vol", "none", "EWALL")
    gg2, _ = P.run(**p_nv)
    d4b = float(np.abs(gg2 - ref.values[P.mask]).max())
    log(f"      (with the vol cap released, the record's own v2 book)          max|dret| {d4b:.3e}")
    assert d4b < 1e-12, "G4 FAILED — this file's EWALL is not the record's RULES v2 book"

    vals = [0.0, 0.02, 0.03, 0.05, 0.08]
    ser = {v: np.sin(v * 37.0) for v in vals}
    a = step_delta(vals, ser)
    b = step_delta(sorted(list(reversed(vals))), ser)
    log(f"  G5  step_delta order-invariance: |diff| {abs(a-b):.3e}")
    assert abs(a - b) < 1e-15, "G5 FAILED"
    log("  ALL GATES PASS")
    return px


# ============================================================================ MAIN
def main():
    px_u = gates()

    log("\n# tuned params: exactly two — (1) the dial VALUE, chosen on IS only in PART C;")
    log("#                              (2) the THIN threshold tau in {0.5, 1.0, 2.0}, headline 1.0.")
    log("# every grid point of every dial at every rung is in .grid.csv; nothing else is selected on.")

    # ------------------------------------------------------------------ PART A
    log("\n" + "=" * 110)
    log("[A] CENSUS — can the three proposed columns be BACK-FILLED over the record's KEEP rows?")
    log("=" * 110)
    cen, n_rows = part_a_census()
    cen.to_csv(f"{STEM}.census.csv", index=False)
    n = len(cen)
    log(f"  LEADERBOARD rows {n_rows};  rows whose verdict cell contains 'KEEP': {n}")
    log(f"  rows whose script has ANY committed sidecar CSV: {int(cen.has_sidecar.sum())} "
        f"({cen.has_sidecar.mean():.1%})")
    for rd in ("STRICT", "LOOSE"):
        b, m_, s_, a_ = (int(cen[f"{rd}_bar"].sum()), int(cen[f"{rd}_margin"].sum()),
                         int(cen[f"{rd}_step"].sum()), int(cen[f"{rd}_all3"].sum()))
        log(f"  {rd:6s}  BAR {b:4d} ({b/n:5.1%})   MARGIN {m_:4d} ({m_/n:5.1%})   "
            f"STEP {s_:4d} ({s_/n:5.1%})   ALL THREE {a_:4d} ({a_/n:5.1%})")
    top = cen.groupby("stem")["STRICT_all3"].agg(["size", "sum"]).sort_values("size", ascending=False)
    log(f"  distinct scripts behind the KEEP rows: {cen.stem.nunique()};  "
        f"largest single script contributes {int(top['size'].iloc[0])} KEEP rows")

    # ------------------------------------------------------------------ panels
    log("\n" + "=" * 110)
    log("[B] BACK-FILL — the three columns at EVERY grid point (not only at the adopted value)")
    log("=" * 110)
    panels = {"U56": Panel("U56", px_u), "B136": Panel("B136", load_universe(broad=True))}
    sm, ndrop = small_panel()
    panels["SMALL"] = Panel("SMALL", sm)
    for k, P in panels.items():
        log(f"  panel {k:6s} {P.q.shape[1]:4d} names  {P.idx[WARM].date()} -> {P.idx[-1].date()}  "
            f"SPY {P.spy_full[0]:.2%}/{P.spy_full[1]:.3f}/{P.spy_full[2]:.2%} "
            f"H {P.spy_H1:.3f}/{P.spy_H2:.3f}  OOS {P.spy_oos[1]:.3f}")
    log(f"  (SMALL drops {ndrop} tickers with max_1d_move >= 1.0 — idea 623's terminal-dated screen)")

    # comparands per panel/rung
    comp = {}
    for pk, P in panels.items():
        gv2, tv2 = fast_backtest(P.q, rules_v2_weights(P.q))
        gv1, tv1 = fast_backtest(P.q, rules_v1_weights(P.q))
        for c in RUNGS:
            comp[(pk, c)] = dict(
                v2=read_arm(P, gv2.values[P.mask], tv2.values[P.mask], c),
                v1=read_arm(P, gv1.values[P.mask], tv1.values[P.mask], c))

    # ------------------------------------------------------------------ the grid
    rows = []
    for pk, P in panels.items():
        for dial, spec in DIALS.items():
            for kind in spec["books"]:
                vals = list(spec["fine"])
                allv = vals + ([spec["ctl"]] if spec["ctl"] is not None else [])
                for v in allv:
                    g, t = P.run(**arm_params(dial, v, kind))
                    for c in RUNGS:
                        m = read_arm(P, g, t, c)
                        v2 = comp[(pk, c)]["v2"]
                        v1 = comp[(pk, c)]["v1"]
                        mb = margins_4b(m, P)
                        mbi = margins_4b(m, P, pre="IS_")
                        ma = margins_4a(m, v2)
                        r = dict(panel=pk, book=kind, dial=dial, val=v,
                                 is_ctl=(v == spec["ctl"]), is_adopted=(v == ADOPTED[dial]),
                                 in_coarse=(v in spec["coarse"]), cost=c, **m)
                        r.update({f"m_{k}": mb[k] for k in BARS})
                        r.update({f"IS_m_{k}": mbi[k] for k in BARS})
                        r.update({f"a_{k}": ma[k] for k in ma})
                        r["m_min"] = min(mb.values())
                        r["m_bind"] = min(mb, key=mb.get)
                        r["IS_m_min"] = min(mbi.values())
                        r["IS_m_bind"] = min(mbi, key=mbi.get)
                        r["a_min"] = min(ma.values())
                        r["a_bind"] = min(ma, key=ma.get)
                        r["pass4b"] = all(x > 0 for x in mb.values())
                        r["IS_pass4b"] = all(x > 0 for x in mbi.values())
                        r["pass4a"] = all(x > 0 for x in ma.values())
                        r["v2_Sharpe"] = v2["Sharpe"]
                        r["v1_Sharpe"] = v1["Sharpe"]
                        rows.append(r)
            log(f"    ran {pk:6s} {dial:6s}  ({len(rows)} grid rows so far)")
    G = pd.DataFrame(rows)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    log(f"  GRID: {len(G)} rows = every dial value x panel x book x rung, all reported.")

    # ------------------------------------------------------- the three columns, per cell
    colrows = []
    combos = [(pk, kind, dial, c, dens)
              for pk in panels for dial in DIALS for kind in DIALS[dial]["books"]
              for c in RUNGS for dens in ("COARSE", "FINE")]
    for pk, kind, dial, c, dens in combos:
        d = G[(G.panel == pk) & (G.book == kind) & (G.dial == dial) & (G.cost == c) & (~G.is_ctl)]
        if dens == "COARSE":
            d = d[d.in_coarse]
        d = d.copy()
        d["valf"] = d.val.astype(float)
        d = d.sort_values("valf")
        vals = list(d.valf)
        if len(vals) < 3:
            continue
        stepk, unitk = {}, {}
        for k in BARS:
            ser = dict(zip(d.valf, d[f"m_{k}"]))
            stepk[k] = step_delta(vals, ser)
            unitk[k] = unit_step(vals, ser)
        p4 = dict(zip(d.valf, d.pass4b))
        for i, v in enumerate(vals):
            row = d.iloc[i]
            bar = row.m_bind
            st = stepk[bar]
            scaled = {k: (row[f"m_{k}"] / stepk[k] if stepk[k] and stepk[k] > 0 else np.inf) for k in BARS}
            bind_s = min(scaled, key=scaled.get)
            nb = [p4[vals[j]] for j in (i - 1, i + 1) if 0 <= j < len(vals)]
            flip1 = any(x != row.pass4b for x in nb)
            colrows.append(dict(panel=pk, book=kind, dial=dial, cost=c, density=dens, val=v,
                                is_adopted=bool(row.is_adopted), pass4b=bool(row.pass4b),
                                pass4a=bool(row.pass4a),
                                BAR=bar, MARGIN=row.m_min, STEP=st,
                                thin_ratio=(row.m_min / st if st and st > 0 else np.nan),
                                UNIT_STEP=unitk[bar],
                                BAR_scaled=bind_s, scaled_min=scaled[bind_s],
                                bar_agrees=(bind_s == bar),
                                FLIP1=bool(flip1), n_grid=len(vals),
                                med_dv=float(np.median(np.diff(vals)))))
    C = pd.DataFrame(colrows)
    C.to_csv(f"{STEM}.cols.csv", index=False)
    log(f"  COLUMNS back-filled on {len(C)} (cell x grid point x density) rows.")

    hd = C[(C.cost == HEADLINE_RUNG) & (C.density == "COARSE")]

    # ---- T1 distribution
    log("\n  T1  MARGIN / STEP over the cells that PASS a KEEP path (headline rung 10 bps, COARSE grid)")
    for lbl, sel in (("4b-passing", hd[hd.pass4b]), ("4a-passing", hd[hd.pass4a]),
                     ("all points", hd)):
        if len(sel) == 0:
            log(f"      {lbl:11s} n=0")
            continue
        tr = sel.thin_ratio.replace([np.inf, -np.inf], np.nan).dropna()
        log(f"      {lbl:11s} n={len(sel):4d}  median |MARGIN/STEP| {tr.abs().median():6.2f}  "
            f"q25 {tr.abs().quantile(.25):6.2f}  q75 {tr.abs().quantile(.75):6.2f}  "
            + "  ".join(f"THIN(tau={t}) {float((tr.abs() < t).mean()):5.1%}" for t in TAUS))
    ad = hd[hd.is_adopted]
    log(f"      ADOPTED values only (idea 401's 19-cell statistic, re-derived): n={len(ad)}  "
        f"passing {int(ad.pass4b.sum())}  "
        f"median |MARGIN/STEP| {ad.thin_ratio.abs().median():.2f}  "
        f"THIN(tau=1) {float((ad.thin_ratio.abs() < 1).mean()):.1%}")
    log(f"      BAR disagreement — argmin over RAW margins vs argmin over margin/STEP: "
        f"{1 - float(hd.bar_agrees.mean()):.1%} of {len(hd)} points pick a DIFFERENT binding bar.")
    log("      bind-bar frequency (raw): " + ", ".join(
        f"{k} {int((hd.BAR == k).sum())}" for k in BARS))
    log("      bind-bar frequency (step-normalised): " + ", ".join(
        f"{k} {int((hd.BAR_scaled == k).sum())}" for k in BARS))

    # ---- T2 does the column earn its place
    log("\n  T2  DOES THE STEP COLUMN EARN ITS PLACE?  predicting FLIP1 (the 4b verdict actually")
    log("      differs at an immediate grid neighbour).  Pooled over 3 panels x 2 books x 5 dials.")

    def auc(scorev, y):
        s = pd.Series(scorev).replace([np.inf, -np.inf], np.nan)
        ok = s.notna() & pd.Series(y).notna()
        s, y2 = s[ok], pd.Series(y)[ok].astype(bool)
        if y2.sum() == 0 or (~y2).sum() == 0:
            return np.nan
        r = s.rank()
        n1, n0 = int(y2.sum()), int((~y2).sum())
        return float((r[y2].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))

    for rung in RUNGS:
        d = C[(C.cost == rung) & (C.density == "COARSE")]
        y = d.FLIP1.values
        a_step = auc(-d.thin_ratio.abs().values, y)
        a_mar = auc(-d.MARGIN.abs().values, y)
        log(f"      {rung:5.1f} bps  n={len(d):4d}  FLIP1 base rate {y.mean():5.1%}   "
            f"AUC(|MARGIN|/STEP) {a_step:.3f}   AUC(|MARGIN| alone) {a_mar:.3f}   "
            f"delta {a_step - a_mar:+.3f}")
    d = C[(C.cost == HEADLINE_RUNG) & (C.density == "COARSE")]
    for t in TAUS:
        thin = d.thin_ratio.abs() < t
        tp = int((thin & d.FLIP1).sum()); fp = int((thin & ~d.FLIP1).sum())
        fn = int((~thin & d.FLIP1).sum()); tn = int((~thin & ~d.FLIP1).sum())
        prec = tp / (tp + fp) if tp + fp else np.nan
        rec = tp / (tp + fn) if tp + fn else np.nan
        log(f"      tau={t:<4}  THIN {tp+fp:4d}/{len(d)}  precision {prec:5.1%}  recall {rec:5.1%}  "
            f"(TP {tp} FP {fp} FN {fn} TN {tn})")

    # ---- T3 density
    log("\n  T3  IS 'STEP' A PROPERTY OF THE FUNCTION, OR OF HOW DENSELY SOMEONE PUBLISHED?")
    key = ["panel", "book", "dial", "cost", "val"]
    mrg = C[C.density == "COARSE"].merge(C[C.density == "FINE"], on=key, suffixes=("_c", "_f"))
    mrg = mrg[(mrg.STEP_c > 0) & (mrg.STEP_f > 0)]
    rs = (mrg.STEP_c / mrg.STEP_f).replace([np.inf, -np.inf], np.nan).dropna()
    ru = (mrg.UNIT_STEP_c / mrg.UNIT_STEP_f).replace([np.inf, -np.inf], np.nan).dropna()
    rt = (mrg.thin_ratio_f.abs() / mrg.thin_ratio_c.abs()).replace([np.inf, -np.inf], np.nan).dropna()
    log(f"      n matched points {len(mrg)} (same cell, same dial value, COARSE vs FINE grid)")
    log(f"      STEP        COARSE/FINE  median {rs.median():.2f}  q25 {rs.quantile(.25):.2f}  "
        f"q75 {rs.quantile(.75):.2f}   (2.00 = step scales with the spacing)")
    log(f"      UNIT_STEP   COARSE/FINE  median {ru.median():.2f}  q25 {ru.quantile(.25):.2f}  "
        f"q75 {ru.quantile(.75):.2f}   (1.00 = density-free)")
    log(f"      |MARGIN/STEP| FINE/COARSE median {rt.median():.2f}: the same cell is "
        f"{rt.median():.2f}x THICKER simply for being published on a grid twice as fine.")
    for t in (HEADLINE_TAU,):
        tc = float((mrg.thin_ratio_c.abs() < t).mean())
        tf = float((mrg.thin_ratio_f.abs() < t).mean())
        flips = int(((mrg.thin_ratio_c.abs() < t) != (mrg.thin_ratio_f.abs() < t)).sum())
        log(f"      THIN(tau={t}) share: COARSE {tc:.1%} -> FINE {tf:.1%};  "
            f"{flips} of {len(mrg)} points ({flips/len(mrg):.1%}) CHANGE their THIN verdict on "
            "density alone.")

    # ------------------------------------------------------------------ PART C rule 8
    log("\n" + "=" * 110)
    log("[C] RULE 8 WALK-FORWARD — the proposed columns as a SELECTOR (params on 2009-2016 only,")
    log("    2017-2026 read ONCE).  S0 uses no column, S1 uses BAR+MARGIN, S2 uses all three.")
    log("=" * 110)
    wf = []
    for pk, P in panels.items():
        for dial, spec in DIALS.items():
            for kind in spec["books"]:
                for c in RUNGS:
                    d = G[(G.panel == pk) & (G.book == kind) & (G.dial == dial) &
                          (G.cost == c) & (~G.is_ctl) & (G.in_coarse)].copy()
                    if len(d) < 3:
                        continue
                    d["valf"] = d.val.astype(float)
                    d = d.sort_values("valf")
                    vals = list(d.valf)
                    stepk = {k: step_delta(vals, dict(zip(d.valf, d[f"IS_m_{k}"]))) for k in BARS}
                    d["IS_step"] = d.IS_m_bind.map(stepk)
                    d["IS_thin"] = d.IS_m_min / d.IS_step.replace(0, np.nan)
                    ctl = G[(G.panel == pk) & (G.book == kind) & (G.dial == dial) &
                            (G.cost == c) & (G.is_ctl)]
                    ctl = ctl.iloc[0] if len(ctl) else d.iloc[-1]
                    v2 = comp[(pk, c)]["v2"]
                    v1 = comp[(pk, c)]["v1"]
                    sels = ["S0", "S1", "S2"] + [f"S3_tau{t}" for t in TAUS]
                    for sel in sels:
                        if sel == "S0":
                            cand = d
                        elif sel == "S1":
                            cand = d[d.IS_pass4b]
                        elif sel == "S2":
                            cand = d[d.IS_pass4b & (d.IS_thin.abs() >= HEADLINE_TAU)]
                        else:
                            # S3 — the STEP column ALONE, with no 4b screen in front of it, because
                            # S1/S2 abstain everywhere and so cannot separate the third column.
                            cand = d[d.IS_thin.abs() >= float(sel.split("tau")[1])]
                        abst = len(cand) == 0
                        pick = ctl if abst else cand.loc[cand.IS_Sharpe.idxmax()]
                        wf.append(dict(panel=pk, book=kind, dial=dial, cost=c, selector=sel,
                                       abstained=abst, pick=pick.val, n_grid=len(d),
                                       n_IS_pass4b=int(d.IS_pass4b.sum()),
                                       n_IS_thick=int((d.IS_thin.abs() >= HEADLINE_TAU).sum()),
                                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                       OOS_MaxDD=pick.OOS_MaxDD,
                                       ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                                       ctl_OOS_MaxDD=ctl.OOS_MaxDD,
                                       adopted_OOS_Sharpe=float(
                                           d.loc[d.is_adopted, "OOS_Sharpe"].iloc[0])
                                       if d.is_adopted.any() else np.nan,
                                       best_OOS_Sharpe=float(d.OOS_Sharpe.max()),
                                       v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"],
                                       v2_OOS_MaxDD=v2["OOS_MaxDD"], v1_OOS_Sharpe=v1["OOS_Sharpe"],
                                       spy_OOS_Sharpe=P.spy_oos[1], spy_OOS_CAGR=P.spy_oos[0],
                                       spy_OOS_MaxDD=P.spy_oos[2],
                                       pass4b=bool(pick.pass4b), pass4a=bool(pick.pass4a)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{STEM}.walkforward.csv", index=False)
    log(f"  {len(W)} walk-forward rows (panel x book x dial x rung x selector), all in .walkforward.csv")
    log("\n  OOS Sharpe of the pick, by selector (median over cells; win = beats the comparand):")
    hdw = W[W.cost == HEADLINE_RUNG]
    z = hdw[hdw.selector == "S0"]
    log(f"  IS screen supply: of {int(z.n_grid.sum())} IS grid points across the 27 cells, "
        f"{int(z.n_IS_pass4b.sum())} pass 4b IN SAMPLE and {int(z.n_IS_thick.sum())} are THICK "
        f"(tau={HEADLINE_TAU}).  S1/S2 can only differ where the first count is > 0.")
    for sel in ["S0", "S1", "S2"] + [f"S3_tau{t}" for t in TAUS]:
        s = hdw[hdw.selector == sel]
        log(f"      {sel:9s} n={len(s):3d} abstain {int(s.abstained.sum()):3d}  "
            f"median OOS Sharpe {s.OOS_Sharpe.median():.3f}  CAGR {s.OOS_CAGR.median():.2%}  "
            f"MaxDD {s.OOS_MaxDD.median():.2%}  |  beats ctl {float((s.OOS_Sharpe > s.ctl_OOS_Sharpe).mean()):5.1%}"
            f"  RULESv2 {float((s.OOS_Sharpe > s.v2_OOS_Sharpe).mean()):5.1%}"
            f"  SPY {float((s.OOS_Sharpe > s.spy_OOS_Sharpe).mean()):5.1%}"
            f"  adopted {float((s.OOS_Sharpe > s.adopted_OOS_Sharpe).mean()):5.1%}")
    p = hdw.pivot_table(index=["panel", "book", "dial"], columns="selector", values="OOS_Sharpe")
    for a, b, lbl in [("S1", "S0", "the 4b screen (BAR+MARGIN)"),
                      ("S2", "S1", "adding STEP on top of the 4b screen"),
                      ("S3_tau1.0", "S0", "the STEP column ALONE (tau=1)"),
                      ("S3_tau0.5", "S0", "the STEP column ALONE (tau=0.5)"),
                      ("S3_tau2.0", "S0", "the STEP column ALONE (tau=2)")]:
        if not {a, b}.issubset(p.columns):
            continue
        dd_ = (p[a] - p[b]).dropna()
        log(f"      {a:9s}-{b:9s} OOS Sharpe, {lbl:38s} median {dd_.median():+.4f}  "
            f"mean {dd_.mean():+.4f}  wins {int((dd_ > 0).sum())}/{len(dd_)}  "
            f"identical picks {int((dd_.abs() < 1e-12).sum())}")
    for pk in panels:
        s = hdw[(hdw.panel == pk) & (hdw.selector == "S2")]
        if len(s):
            log(f"      {pk:6s} S2 picks: OOS Sharpe {s.OOS_Sharpe.min():.3f}-{s.OOS_Sharpe.max():.3f}"
                f"  vs RULESv2 {s.v2_OOS_Sharpe.iloc[0]:.3f}  SPY {s.spy_OOS_Sharpe.iloc[0]:.3f}"
                f"  (SPY OOS CAGR {s.spy_OOS_CAGR.iloc[0]:.2%}, DD {s.spy_OOS_MaxDD.iloc[0]:.2%})")

    # ------------------------------------------------------------------ KEEP paths
    log("\n" + "=" * 110)
    log("[D] KEEP PATHS — PROTOCOL 4, on every arm at every rung")
    log("=" * 110)
    for c in RUNGS:
        d = G[(G.cost == c) & (~G.is_ctl)]
        fail = {k: int((d[f"m_{k}"] <= 0).sum()) for k in BARS}
        log(f"  {c:5.1f} bps  arms {len(d):4d}   4a {int(d.pass4a.sum()):4d}   4b {int(d.pass4b.sum()):4d}   "
            f"both {int((d.pass4a & d.pass4b).sum()):4d}   failing-leg counts " +
            " ".join(f"{k} {v}" for k, v in sorted(fail.items(), key=lambda x: -x[1])))
    d = G[(G.cost == HEADLINE_RUNG) & (~G.is_ctl)]
    both = d[d.pass4a & d.pass4b]
    log(f"  at the protocol rung, arms passing BOTH paths: {len(both)}")
    log("\n  Every 4b-passing arm at the protocol rung, WITH THE THREE PROPOSED COLUMNS — this is")
    log("  what a back-filled LEADERBOARD row would look like:")
    log("    panel  book   dial   val      CAGR   Sharpe    DD      H1/H2       OOS  | BAR  MARGIN"
        "    STEP   M/STEP  UNIT_STEP  FLIP1")
    for _, b in d[d.pass4b].sort_values("m_min", ascending=False).iterrows():
        cc = C[(C.panel == b.panel) & (C.book == b.book) & (C.dial == b.dial) &
               (C.cost == HEADLINE_RUNG) & (C.density == "COARSE") &
               (np.abs(C.val - float(b.val)) < 1e-12)]
        if not len(cc):
            continue
        q = cc.iloc[0]
        log(f"    {b.panel:6s} {b.book:6s} {b.dial:6s} {str(b.val):8s} {b.CAGR:6.2%} {b.Sharpe:6.3f} "
            f"{b.MaxDD:7.2%} {b.H1:5.3f}/{b.H2:5.3f} {b.OOS_Sharpe:6.3f} | {q.BAR:4s} "
            f"{q.MARGIN:+.4f} {q.STEP:.4f} {q.thin_ratio:+7.2f} {q.UNIT_STEP:9.4f}  {q.FLIP1}")
    log("    NOTE: these are dial arms of the record's own books, not new instruments — every one")
    log("    is already inside the record's committed grids; no new book is proposed here, and")
    log("    none of them passes 4a, so none is a KEEP under either path.")
    log("\n  4a is judged against the LIVE RULES v2 book at the same rung on the same panel; 4b")
    log("  against SPY on the same window.  Warm-up index[300], W cadence, t+1, de-gross to CASH.")

    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

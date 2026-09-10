#!/usr/bin/env python3
"""Idea 648 — restate idea 621's SPLIT as an EFFECT-SIZE law and price it.   (cloud, 2026-09-10)

QUEUE 648: "idea 624 killed the frequency form (a-priori cut ranks 31 of 35 partitions, p=0.886)
but found the measured membership distance orders the SIZE of the surviving edge at Spearman +0.884
over 8 dials and +0.388 over 96 cells.  Fit and walk forward the one-line rule 'expected dSharpe =
f(JAC)' on a fresh set of dials and report whether an IS-fitted f predicts OOS edge size well enough
to be a screening rule for which dials are worth a parameter at all.  Max 2 params (f form, dial
set)."

WHAT IS ACTUALLY BEING TESTED
  A screening rule has to be usable BEFORE the parameter is spent.  That imposes two things idea
  624's correlation never had to satisfy:

    S1  JAC MUST BE IS-ONLY.  624 measured membership distance over the whole sample.  A screen
        computed on data the decision has not seen yet is not a screen.  Here JAC is measured on
        rebalance days inside the IS window (<= 2016-12-31) alone, and JAC_FULL is reported beside
        it so the reader can see how much that costs.
    S2  f MUST BE FITTED ON ONE DIAL SET AND READ ON ANOTHER.  A rule fitted and read on the same
        8 dials is a description of those 8 dials.  Six FRESH dials, written down before any return
        was read, are the held-out set; the 8 dials of idea 624 are the training set.

  So the claim under test is the strong one: an f fitted on the record's own dials, using only the
  IS window, predicts the SIZE of the OOS chooser edge on dials it has never seen.  Everything is
  doubly out of sample — new dials AND the untouched 2017-2026 window (PROTOCOL rule 8).

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 f FORM: CONST (the null: predict the training mean), LIN (dSharpe ~ a + b*JAC), SQRT
     (~ a + b*sqrt(JAC), the compressive form 624's rank correlation is agnostic between), STEP
     (two group means split at the TRAINING median JAC).  All four are reported at every rung on
     both sets; none is chosen on test data.
  P2 DIAL SET: TRAIN = idea 624's eight dials verbatim; TEST = six fresh dials.  The split is
     pre-registered and is the object of study.
  Panels (u56 / broad136 / small439), cost rungs and the control form are REPORTED axes, never
  selected on.  Every grid point is written to .grid.csv.  The only selection anywhere in this file
  is PROTOCOL rule 8 itself, which is the object of study.

THE SIX FRESH DIALS (pre-registered, with their a-priori membership content)
  MOVES MEMBERSHIP   mafilt  [OFF,50,100,200,300]        eligibility MA filter      default OFF
                     revfilt [OFF,5,10,21,42]            drop top-decile k-day run  default OFF
                     bufn    [0,5,10,20,40]              rank buffer on the held set default 0
  CANNOT MOVE IT     spow    [0.0,0.5,1.0,1.5,2.0]       weight ~ score^p (weights) default 0.0
                     cash    [0.00,0.05,0.10,0.20,0.35]  fixed cash sleeve (exposure) default 0.00
                     lag     [1,2,3,4,5]                 execution delay (timing)   default 1
  The last three are constructed to have JAC == 0 at every rung; G5 asserts it rather than assuming
  it, and they are what gives the held-out set any spread in the regressor at all.

GATES (run before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest`, returns AND turnover, D and W, 3 panels.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=25).
  G3 the DEFAULT rung is IN the ladder of every one of the 14 dials.
  G4 the IS and OOS windows are disjoint and jointly exhaust the evaluated sample.
  G5 CONSTRUCTION: spow / cash / lag carry JAC exactly 0 at every rung on every panel; mafilt /
     revfilt / bufn carry JAC > 0 somewhere.  A held-out set whose regressor is degenerate would
     make the whole test vacuous, so this is a gate, not an observation.
  G6 REPRODUCTION: idea 624's +0.884 is re-derived on the TRAINING dials from this file's own grid
     (per-dial JAC vs per-dial median chooser edge), not restated from its prose.  A different
     warm-up bar and an IS-only JAC mean it need not match to the digit; the gate is the SIGN and
     the ordering, and the measured value is printed either way.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents.  SMALL439 additionally drops
    every ticker with max_1d_move >= 1.0 in data/small_meta.csv before anything runs, and is a
    since-2010 panel of names that exist TODAY under $2B — its levels are not investable history
    and only WITHIN-panel arm-minus-arm contrasts are read off it.
  * Warm-up is px.index[310], not the record's [260]: mafilt=300 and look=252-on-a-21d-skip both
    need more closes than 260.  Every arm in this file starts on the same day, so the anchors'
    levels differ slightly from ideas 621/624.
  * Idea 412: a cadence has a PHASE.  `phase` is carried here as a TRAINING dial, as in 624.
  * Idea 321: MaxDD is one number off one path.  Idea 126: t+1 execution, 10 bps default rung.
  * Ideas 527/531: 4b is in practice a DD-cap test on ungated momentum books; both KEEP paths are
    priced on every arm anyway, as PROTOCOL requires.
  * n = 18 held-out cells at a rung is a small sample and is reported as one: the headline carries
    a permutation p-value, not a t-statistic.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .grid.csv, .cells.csv, .taxonomy.csv, .fit.csv.
"""
from __future__ import annotations

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

STEM = "2026-09-10_restate-idea-621-s-SPLIT-as-an-EFFECT-SIZE-law-and-price-it_cloud"
OUT = ROOT / "research" / "backtests"

IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60            # 4b CAGR floor and MaxDD cap, as fractions of SPY's
PCOST = 10.0                       # PROTOCOL's own rung
RUNGS = [0.0, 10.0, 25.0, 50.0]    # reported cost ladder
CELL_RUNGS = [10.0, 25.0]          # the rungs the chooser cells are cut on (idea 621's pair)
WARM = 310                         # common warm-up bar for every arm in this file
PANELS = ["u56", "broad136", "small439"]

# ---- TRAIN: idea 624's eight dials, verbatim ------------------------------------------------
LAD_TRAIN = {
    "n":       [5, 10, 15, 20, 30, 40, 60],
    "volcap":  [0.30, 0.45, 0.60, 0.80, 1.00, 9.99],
    "look":    ["REC", 63, 126, 189, 252],
    "skip":    ["REC", 0, 5, 21, 42],
    "gross":   [0.25, 0.50, 0.75, 1.00],
    "lambda":  [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06],
    "wscheme": ["EW", "INVVOL", "SQRTIV", "RANKLIN"],
    "phase":   ["W", "MON", "TUE", "WED", "THU"],
}
# ---- TEST: six fresh dials, pre-registered --------------------------------------------------
LAD_TEST = {
    "mafilt":  ["OFF", 50, 100, 200, 300],
    "revfilt": ["OFF", 5, 10, 21, 42],
    "bufn":    [0, 5, 10, 20, 40],
    "spow":    [0.0, 0.5, 1.0, 1.5, 2.0],
    "cash":    [0.00, 0.05, 0.10, 0.20, 0.35],
    "lag":     [1, 2, 3, 4, 5],
}
LADDERS = {**LAD_TRAIN, **LAD_TEST}
DEFAULTS = {"n": 20, "volcap": 0.60, "look": "REC", "skip": "REC", "gross": 0.75,
            "lambda": 1.00, "wscheme": "EW", "phase": "W",
            "mafilt": "OFF", "revfilt": "OFF", "bufn": 0, "spow": 0.0, "cash": 0.00, "lag": 1}
TRAIN = list(LAD_TRAIN)
TEST = list(LAD_TEST)
DIALS = TRAIN + TEST
# a-priori membership content of the six fresh dials (used only by gate G5)
ZERO_JAC = {"spow", "cash", "lag"}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner (idea 613/621/624's segment form; gated against engine.backtest below)
# =====================================================================================
def mask_of(idx, phase):
    if phase in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, phase).shift(1, fill_value=False).values
    wd = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4}[phase]
    return pd.Series(idx.weekday == wd, index=idx).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    """engine.backtest's drift algebra, one pass per rebalance SEGMENT."""
    n = len(rets)
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
    return port, turn


def run(px, W, phase, lag=1):
    """lag = 1 is the record's t+1 execution.  lag = k applies the target k days after it is
    decided; the target frame itself is unchanged, so this is a pure TIMING dial."""
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(int(lag)).fillna(0.0).values
    p, t = fast_bt(rets, w_t, mask_of(px.index, phase))
    return pd.Series(p, index=px.index), pd.Series(t, index=px.index)


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: an EWMA of the raw target with gross restored
    daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# =====================================================================================
# the book
# =====================================================================================
def comp_rec(sub):
    mom = sub.shift(21) / sub.shift(252) - 1
    r6, r3 = sub / sub.shift(126) - 1, sub / sub.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def comp_look(sub, J):
    return (sub.shift(21) / sub.shift(21 + int(J)) - 1).rank(axis=1, pct=True)


def comp_skip(sub, s):
    s = int(s)
    mom = sub.shift(s) / sub.shift(s + 231) - 1
    r6 = sub.shift(s) / sub.shift(s + 126) - 1
    r3 = sub.shift(s) / sub.shift(s + 63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


class Panel:
    def __init__(self, key):
        if key == "u56":
            px, self.ndrop = load_universe(), 0
        elif key == "broad136":
            px, self.ndrop = load_universe(broad=True), 0
        else:
            px, self.ndrop = small_panel()
        self.key = key
        self.px = px.dropna(how="all").ffill()
        self.sub = self.px.drop(columns=["SPY"], errors="ignore")
        self.v20 = self.sub.pct_change().rolling(20).std() * np.sqrt(252)
        self.start = self.px.index[WARM]
        self._comp: dict = {}
        self._ma: dict = {}
        self._rev: dict = {}

    def comp(self, look, skip):
        k = (str(look), str(skip))
        if k not in self._comp:
            if look != "REC":
                c = comp_look(self.sub, look)
            elif skip != "REC":
                c = comp_skip(self.sub, skip)
            else:
                c = comp_rec(self.sub)
            self._comp[k] = c
        return self._comp[k]

    def ma_ok(self, k):
        if k not in self._ma:
            self._ma[k] = self.sub > self.sub.rolling(int(k)).mean()
        return self._ma[k]

    def rev_ok(self, k):
        """False for names in the top cross-sectional decile of trailing k-day return."""
        if k not in self._rev:
            rt = self.sub / self.sub.shift(int(k)) - 1
            self._rev[k] = rt.rank(axis=1, pct=True) < 0.90
        return self._rev[k]


def buffered_sel(rank, n, buf):
    """Rank buffer: a held name stays while rank <= n+buf; the book is refilled to exactly n from
    the best-ranked non-held names.  Stateful over calendar days, deterministic."""
    R = rank.values
    T, K = R.shape
    out = np.zeros((T, K), dtype=bool)
    held = np.zeros(K, dtype=bool)
    fin = np.isfinite(R)
    for i in range(T):
        r = R[i]
        ok = fin[i]
        keep = held & ok & (r <= n + buf)
        need = n - int(keep.sum())
        if need > 0:
            cand = np.flatnonzero(ok & ~keep)
            if cand.size:
                keep[cand[np.argsort(r[cand], kind="stable")][:need]] = True
        elif need < 0:
            idx = np.flatnonzero(keep)
            keep[idx[np.argsort(-r[idx], kind="stable")][:(-need)]] = False
        out[i] = keep
        held = keep
    return pd.DataFrame(out, index=rank.index, columns=rank.columns)


def _raw_weights(scheme, spow, sel, rank, score, v20, n):
    """Positive raw weights on the SELECTED set only.  Every scheme is strictly positive on the
    selected names, so MEMBERSHIP is identical across schemes/powers by construction (G5)."""
    if float(spow) > 0.0:
        raw = (score.clip(lower=1e-6) ** float(spow)).where(sel)
    elif scheme == "EW":
        raw = sel.astype(float)
    elif scheme == "INVVOL":
        raw = (1.0 / v20.clip(lower=0.08)).where(sel)
    elif scheme == "SQRTIV":
        raw = (1.0 / np.sqrt(v20.clip(lower=0.08))).where(sel)
    elif scheme == "RANKLIN":
        raw = (float(n) + 1.0 - rank).clip(lower=1e-9).where(sel)
    else:
        raise ValueError(scheme)
    return raw.where(sel, 0.0).fillna(0.0)


def target(panel: Panel, vals: dict):
    """Target weights before the lambda / phase / lag timing dials."""
    c = panel.comp(vals["look"], vals["skip"])
    vc = float(vals["volcap"])
    c = c.where(panel.v20 < vc) if vc < 9.0 else c.where(panel.v20.notna())
    if vals["mafilt"] != "OFF":
        c = c.where(panel.ma_ok(vals["mafilt"]))
    if vals["revfilt"] != "OFF":
        c = c.where(panel.rev_ok(vals["revfilt"]))
    rank = c.rank(axis=1, ascending=False)
    n = int(vals["n"])
    buf = int(vals["bufn"])
    sel = buffered_sel(rank, n, buf) if buf > 0 else (rank <= n)
    raw = _raw_weights(vals["wscheme"], vals["spow"], sel, rank, c, panel.v20, n)
    tot = raw.sum(axis=1).replace(0, np.nan)
    g = float(vals["gross"]) * (1.0 - float(vals["cash"]))
    return (g * raw.div(tot, axis=0)).fillna(0.0)


def arm(panel: Panel, dial: str, value):
    """Weights, rebalance phase and execution lag for one grid point."""
    vals = dict(DEFAULTS)
    vals[dial] = value
    W = smooth(target(panel, vals), float(vals["lambda"]))
    return W, str(vals["phase"]), int(vals["lag"])


# =====================================================================================
# metrics helpers (idea 621/624's, verbatim)
# =====================================================================================
def sh(r):
    return metrics(r)["Sharpe"]


def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def bars_of(spy):
    h1, h2 = halves(spy)
    m = metrics(spy)
    return dict(s1=h1, s2=h2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=sh(spy.loc[OOS_START:]),
                spy_oos=spy.loc[OOS_START:])


def pass4b(r, b, window="full"):
    if window == "full":
        h1, h2 = halves(r)
        m = metrics(r)
        return bool(h1 > b["s1"] and h2 > b["s2"] and sh(r.loc[OOS_START:]) > b["soos"]
                    and abs(m["MaxDD"]) <= DELTA * abs(b["sdd"]) and m["CAGR"] >= PHI * b["scagr"])
    x = r.loc[OOS_START:]
    h1, h2 = halves(x)
    m = metrics(x)
    sp = b["spy_oos"]
    o1, o2 = halves(sp)
    mo = metrics(sp)
    return bool(h1 > o1 and h2 > o2 and abs(m["MaxDD"]) <= DELTA * abs(mo["MaxDD"])
                and m["CAGR"] >= PHI * mo["CAGR"])


def pass4a(r, base, window="full"):
    x, y = (r, base) if window == "full" else (r.loc[OOS_START:], base.loc[OOS_START:])
    h1, h2 = halves(x)
    b1, b2 = halves(y)
    return bool(h1 > b1 and h2 > b2 and metrics(x)["MaxDD"] >= metrics(y)["MaxDD"])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# =====================================================================================
# GATES
# =====================================================================================
def gates(panels: dict):
    say("=" * 110)
    say("GATES")
    say("=" * 110)
    # G3 — the default rung is in every ladder
    bad = [d for d in DIALS if DEFAULTS[d] not in LADDERS[d]]
    say(f"  G3 default rung present in every one of {len(DIALS)} ladders : "
        f"{'PASS' if not bad else 'FAIL ' + str(bad)}")
    assert not bad

    worst_r = worst_t = worst_c = 0.0
    for pk, P in panels.items():
        px = P.px
        for phase in ("W", "D"):
            W, _, _ = arm(P, "n", 20)
            W = W.reindex(columns=px.columns).fillna(0.0)
            r_f, t_f = run(px, W, phase)
            ref = backtest(px, W, cost_bps=0.0, freq=phase)
            worst_r = max(worst_r, float((r_f - ref["returns"]).abs().max()))
            worst_t = max(worst_t, float((t_f - ref["turnover"]).abs().max()))
            if phase == "W":
                ref25 = backtest(px, W, cost_bps=25.0, freq=phase)
                worst_c = max(worst_c, float(((r_f - t_f * 25.0 / 1e4) - ref25["returns"]).abs().max()))
    say(f"  G1 fast runner vs engine.backtest, 3 panels x (W,D): max |dret| {worst_r:.3e}   "
        f"max |dturn| {worst_t:.3e}   {'PASS' if max(worst_r, worst_t) < 1e-12 else 'FAIL'}")
    say(f"  G2 cost identity r(25) = r(0) - turn*25/1e4        : max |d| {worst_c:.3e}   "
        f"{'PASS' if worst_c < 1e-12 else 'FAIL'}")
    assert max(worst_r, worst_t) < 1e-12 and worst_c < 1e-12

    P = panels["u56"]
    idx = P.px.loc[P.start:].index
    nis, noos = int((idx <= IS_END).sum()), int((idx >= OOS_START).sum())
    say(f"  G4 IS {idx[0].date()}..{IS_END} = {nis} days, OOS {OOS_START}..{idx[-1].date()} = "
        f"{noos} days, sum {nis + noos} == {len(idx)}  "
        f"{'PASS' if nis + noos == len(idx) and nis > 0 and noos > 0 else 'FAIL'}")
    assert nis + noos == len(idx)


# =====================================================================================
# PART A — the PRE-RETURN taxonomy: JAC on the IS window alone
# =====================================================================================
def taxonomy(P: Panel, dial: str):
    """Membership (Jaccard) distance of each rung's TARGET holdings from the default rung's, on
    rebalance days.  Reported IS-only (the screen) and full-sample (idea 624's form)."""
    Wd, _, _ = arm(P, dial, DEFAULTS[dial])
    idx = P.px.index
    days = idx[np.flatnonzero(mask_of(idx, "W"))]
    days = days[days >= P.start]
    is_m = days <= pd.Timestamp(IS_END)
    A = (Wd.reindex(idx).fillna(0.0).loc[days].values > 1e-12)
    rows = []
    for v in LADDERS[dial]:
        Wv, _, _ = arm(P, dial, v)
        B = (Wv.reindex(idx).fillna(0.0).loc[days].values > 1e-12)
        inter = (A & B).sum(axis=1).astype(float)
        union = (A | B).sum(axis=1).astype(float)
        jac = np.where(union > 0, 1.0 - inter / np.maximum(union, 1e-12), 0.0)
        rows.append(dict(panel=P.key, dial=dial, dial_set=("TRAIN" if dial in TRAIN else "TEST"),
                         value=str(v), is_default=(v == DEFAULTS[dial]),
                         JAC_IS=float(np.nanmean(jac[is_m])), JAC_FULL=float(np.nanmean(jac))))
    return rows


# =====================================================================================
# PART B — the grid
# =====================================================================================
def grid_rows(P: Panel, dial: str, b, baser):
    out = []
    for v in LADDERS[dial]:
        W, phase, lag = arm(P, dial, v)
        r0, to = run(P.px, W.reindex(columns=P.px.columns).fillna(0.0), phase, lag)
        r0, to = r0.loc[P.start:], to.loc[P.start:]
        rec = dict(panel=P.key, dial=dial, dial_set=("TRAIN" if dial in TRAIN else "TEST"),
                   value=str(v), is_default=(v == DEFAULTS[dial]),
                   turnover=float(to.sum() / (len(to) / 252.0)))
        for c in RUNGS:
            r = r0 - to * c / 1e4
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = halves(r)
            rec[f"sh_full_{c:g}"], rec[f"cagr_full_{c:g}"], rec[f"dd_full_{c:g}"] = \
                m["Sharpe"], m["CAGR"], m["MaxDD"]
            rec[f"h1_{c:g}"], rec[f"h2_{c:g}"] = h1, h2
            rec[f"sh_is_{c:g}"] = sh(r.loc[:IS_END])
            rec[f"sh_oos_{c:g}"], rec[f"cagr_oos_{c:g}"], rec[f"dd_oos_{c:g}"] = \
                mo["Sharpe"], mo["CAGR"], mo["MaxDD"]
            if c == PCOST:
                rec["p4a_full"] = pass4a(r, baser)
                rec["p4b_full"] = pass4b(r, b, "full")
                rec["p4a_oos"] = pass4a(r, baser, "oos")
                rec["p4b_oos"] = pass4b(r, b, "oos")
        out.append(rec)
    return out


def cells(G, TX):
    """PROTOCOL rule 8 on every (panel, dial, rung): choose on the IS half, read the OOS half,
    against the dial's own DEFAULT rung (the record's NO-DIAL control) and against MEDIAN."""
    rows = []
    for pk in PANELS:
        for dial in DIALS:
            g = G[(G.panel == pk) & (G.dial == dial)].set_index("value")
            lad = [str(v) for v in LADDERS[dial]]
            g = g.loc[lad]
            jj = TX[(TX.panel == pk) & (TX.dial == dial) & (~TX.is_default)]
            for c in CELL_RUNGS:
                pick = g[f"sh_is_{c:g}"].idxmax()
                oracle = g[f"sh_oos_{c:g}"].idxmax()
                for form, ctl in (("DEFAULT", str(DEFAULTS[dial])), ("MEDIAN", lad[len(lad) // 2])):
                    rows.append(dict(
                        panel=pk, dial=dial, dial_set=("TRAIN" if dial in TRAIN else "TEST"),
                        rung=c, form=form, control=ctl, pick=pick, oracle=oracle,
                        JAC_IS=float(jj.JAC_IS.mean()), JAC_FULL=float(jj.JAC_FULL.mean()),
                        d_oos=float(g.loc[pick, f"sh_oos_{c:g}"] - g.loc[ctl, f"sh_oos_{c:g}"]),
                        d_is=float(g.loc[pick, f"sh_is_{c:g}"] - g.loc[ctl, f"sh_is_{c:g}"]),
                        d_full=float(g.loc[pick, f"sh_full_{c:g}"] - g.loc[ctl, f"sh_full_{c:g}"]),
                        d_cagr_oos=float(g.loc[pick, f"cagr_oos_{c:g}"] - g.loc[ctl, f"cagr_oos_{c:g}"]),
                        d_dd_oos=float(g.loc[pick, f"dd_oos_{c:g}"] - g.loc[ctl, f"dd_oos_{c:g}"]),
                        abstain=bool(pick == ctl)))
    return pd.DataFrame(rows)


# =====================================================================================
# PART C — f(JAC): fit on TRAIN, read on TEST
# =====================================================================================
def _ols(x, y):
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return coef


def fit_forms(jtr, ytr):
    """The four P1 forms, each fitted on the TRAINING cells only."""
    F = {}
    F["CONST"] = (lambda j, m=float(np.mean(ytr)): np.full(np.shape(j), m))
    a, b = _ols(jtr, ytr)
    F["LIN"] = (lambda j, a=a, b=b: a + b * np.asarray(j, float))
    a2, b2 = _ols(np.sqrt(jtr), ytr)
    F["SQRT"] = (lambda j, a=a2, b=b2: a2 + b2 * np.sqrt(np.asarray(j, float)))
    tau = float(np.median(jtr))
    hi = ytr[jtr > tau]
    lo = ytr[jtr <= tau]
    mh = float(np.mean(hi)) if hi.size else float(np.mean(ytr))
    ml = float(np.mean(lo)) if lo.size else float(np.mean(ytr))
    F["STEP"] = (lambda j, t=tau, h=mh, l=ml: np.where(np.asarray(j, float) > t, h, l))
    return F, dict(lin_a=a, lin_b=b, sqrt_a=a2, sqrt_b=b2, tau=tau, step_hi=mh, step_lo=ml)


def score_forms(F, j, y):
    out = {}
    for k, f in F.items():
        p = np.asarray(f(j), float)
        out[k] = dict(RMSE=float(np.sqrt(np.mean((p - y) ** 2))),
                      MAE=float(np.mean(np.abs(p - y))),
                      rho=spearman(p, y),
                      sign_acc=float(np.mean(np.sign(p) == np.sign(y))))
    return out


def screen_value(pred, y, thresh=0.0, label=">0"):
    """The screening decision: spend the parameter only where f's prediction clears `thresh`.
    thresh = 0 is 'only where a positive edge is predicted'; thresh = the TRAIN median prediction
    is the non-degenerate 'spend on the better half' form (a fitted f whose intercept is positive
    everywhere cannot screen at 0 at all, which is itself a result)."""
    pred = np.asarray(pred, float)
    y = np.asarray(y, float)
    adm = pred > thresh
    return dict(rule=label, n_admit=int(adm.sum()), n_total=int(len(y)),
                mean_admit=float(np.mean(y[adm])) if adm.any() else np.nan,
                mean_reject=float(np.mean(y[~adm])) if (~adm).any() else np.nan,
                mean_all=float(np.mean(y)),
                lift=(float(np.mean(y[adm]) - np.mean(y)) if adm.any() else np.nan))


def perm_dial_p(df, jcol="JAC_IS", ycol="d_oos", seed=648, cap=40320):
    """Permutation test that respects the nesting: the regressor is a DIAL property, so the null
    shuffles JAC across DIAL LABELS, not across cells.  Exact when the dial count allows."""
    import itertools as it
    dials = sorted(df.dial.unique())
    jm = df.groupby("dial")[jcol].mean()
    obs = spearman(df[jcol].values, df[ycol].values)
    if not np.isfinite(obs):
        return obs, np.nan, 0, "n/a"
    perms = list(it.permutations(range(len(dials))))
    exact = len(perms) <= cap
    if not exact:
        rng = np.random.default_rng(seed)
        perms = [tuple(rng.permutation(len(dials))) for _ in range(cap)]
    hits = 0
    base = df.dial.values
    for p in perms:
        mp = {dials[i]: float(jm.iloc[p[i]]) for i in range(len(dials))}
        jj = np.array([mp[d] for d in base])
        r = spearman(jj, df[ycol].values)
        if np.isfinite(r) and abs(r) >= abs(obs) - 1e-12:
            hits += 1
    return obs, hits / len(perms), len(perms), ("exact" if exact else "sampled")


# =====================================================================================
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 648 — 'expected dSharpe = f(JAC)' as a PRE-SPEND SCREENING RULE")
    say("  P1 f form: CONST / LIN / SQRT / STEP.   P2 dial set: TRAIN = idea 624's 8, "
        "TEST = 6 fresh.")
    say(f"  JAC measured on the IS window ({IS_END} and earlier) ONLY.  OOS = {OOS_START}+, "
        "untouched by fit or chooser.")
    say("=" * 110)

    panels = {}
    for pk in PANELS:
        P = Panel(pk)
        panels[pk] = P
        say(f"  panel {pk:9s} {P.sub.shape[1]:4d} names  {P.px.index[0].date()}.."
            f"{P.px.index[-1].date()}  start {P.start.date()}"
            + (f"  (dropped {P.ndrop} max_1d_move>=1.0)" if P.ndrop else ""))

    gates(panels)

    # ---- taxonomy -----------------------------------------------------------------
    say("")
    say("=" * 110)
    say("PART A — PRE-RETURN TAXONOMY (target weights only; no return is read here)")
    say("=" * 110)
    tx = []
    for pk, P in panels.items():
        for d in DIALS:
            tx += taxonomy(P, d)
    TX = pd.DataFrame(tx)
    TX.to_csv(OUT / f"{STEM}.taxonomy.csv", index=False)

    nd = TX[~TX.is_default]
    zmax = float(nd[nd.dial.isin(ZERO_JAC)].JAC_IS.abs().max())
    nzmin = float(nd[nd.dial.isin(set(TEST) - ZERO_JAC)].groupby("dial").JAC_IS.max().min())
    say(f"  G5 fresh JAC=0 dials {sorted(ZERO_JAC)}: max |JAC_IS| over all rungs/panels "
        f"= {zmax:.3e}  {'PASS' if zmax < 1e-12 else 'FAIL'}")
    say(f"     fresh membership dials {sorted(set(TEST) - ZERO_JAC)}: min over dials of max JAC_IS "
        f"= {nzmin:.4f}  {'PASS' if nzmin > 0.01 else 'FAIL'}")
    assert zmax < 1e-12 and nzmin > 0.01

    per = (nd.groupby(["dial_set", "dial"])[["JAC_IS", "JAC_FULL"]].mean()
           .sort_values(["dial_set", "JAC_IS"], ascending=[True, False]))
    say("")
    say("  mean membership distance from the dial's own default rung (non-default rungs, 3 panels):")
    say(per.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"  Spearman(JAC_IS, JAC_FULL) over all {len(per)} dials : "
        f"{spearman(per.JAC_IS.values, per.JAC_FULL.values):+.3f}  (S1: the IS-only screen keeps "
        "the ordering)")

    # ---- grid ---------------------------------------------------------------------
    say("")
    say("=" * 110)
    say("PART B — THE GRID (every arm, every rung; PROTOCOL 4a and 4b priced on all of them)")
    say("=" * 110)
    rows = []
    for pk, P in panels.items():
        px = P.px
        spy = px["SPY"].pct_change().fillna(0.0).loc[P.start:]
        b = bars_of(spy)
        r0, to = run(px, rules_v2_weights(px), "W")
        baser = (r0 - to * PCOST / 1e4).loc[P.start:]
        mb, mo = metrics(baser), metrics(baser.loc[OOS_START:])
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"  {pk:9s} SPY   full CAGR {ms['CAGR']:6.2%} Sh {ms['Sharpe']:5.2f} DD {ms['MaxDD']:7.1%}"
            f" | OOS CAGR {mso['CAGR']:6.2%} Sh {mso['Sharpe']:5.2f} DD {mso['MaxDD']:7.1%}")
        say(f"  {pk:9s} RULESv2 full CAGR {mb['CAGR']:6.2%} Sh {mb['Sharpe']:5.2f} DD {mb['MaxDD']:7.1%}"
            f" | OOS CAGR {mo['CAGR']:6.2%} Sh {mo['Sharpe']:5.2f} DD {mo['MaxDD']:7.1%}")
        for d in DIALS:
            rows += grid_rows(P, d, b, baser)
            say(f"    {pk:9s} {d:8s} {len(LADDERS[d])} rungs done  [{time.time() - t0:6.1f}s]")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say("")
    say(f"  arms {len(G)}   PROTOCOL 4a passes {int(G.p4a_full.sum())}   "
        f"4b passes {int(G.p4b_full.sum())}   (10 bps, full sample)")
    say(f"  OOS-window re-cut:        4a {int(G.p4a_oos.sum())}   4b {int(G.p4b_oos.sum())}")

    C = cells(G, TX)
    C.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    # ---- G6 reproduction ----------------------------------------------------------
    say("")
    say("=" * 110)
    say("PART C — f(JAC): FITTED ON THE 8 TRAINING DIALS, READ ON THE 6 FRESH ONES")
    say("=" * 110)
    # G6 uses idea 624's OWN pooling: FULL leg, both control forms, both cost rungs, per-dial
    # median chooser edge.  That is 8 x 3 x 2 x 2 = 96 training cells — 624's own n.
    TRC = C[C.dial_set == "TRAIN"]
    TEC = C[C.dial_set == "TEST"]
    tr_dial = TRC.groupby("dial").agg(JAC=("JAC_IS", "mean"), med=("d_oos", "median"),
                                      win=("d_oos", lambda s: float((s > 0).mean())))
    r_med = spearman(tr_dial.JAC.values, tr_dial.med.values)
    r_win = spearman(tr_dial.JAC.values, tr_dial.win.values)
    r_cell = spearman(TRC.JAC_IS.values, TRC.d_oos.values)
    say("  G6 REPRODUCTION on the TRAINING dials, pooled idea 624's own way "
        f"(n={len(TRC)} cells; 624 published n=96):")
    say(f"     Spearman(JAC_IS, per-dial MEDIAN edge) = {r_med:+.3f}   (624: +0.884)")
    say(f"     Spearman(JAC_IS, per-dial WIN RATE)    = {r_win:+.3f}   (624: +0.284)")
    say(f"     Spearman(JAC_IS, edge) at CELL level   = {r_cell:+.3f}   (624: +0.388)")
    say(f"     {'SIGN AND ORDERING REPRODUCE' if r_med > 0 else 'DOES NOT REPRODUCE — sign flips'}"
        "; warm-up 310, an IS-only JAC and six extra dials in the panel mean the digits need not "
        "match, but the SIZE of the drop is itself the first result of this file.")
    o_tr, p_tr, n_tr, kd_tr = perm_dial_p(TRC)
    say(f"     dial-label permutation on the TRAINING cells: rho {o_tr:+.3f}, p = {p_tr:.3f} "
        f"({kd_tr}, {n_tr} labellings) — the number 648 is asked to walk forward is ITSELF "
        f"{'significant' if p_tr < 0.05 else 'NOT significant'} against its own dial-label null.")

    say("")
    say("  HEADLINE (pooled, held-out): f fitted on the 8 TRAINING dials, read on the 6 FRESH ones")
    jtr_p, ytr_p = TRC.JAC_IS.values, TRC.d_oos.values
    jte_p, yte_p = TEC.JAC_IS.values, TEC.d_oos.values
    Fp, parp = fit_forms(jtr_p, ytr_p)
    s_trp, s_tep = score_forms(Fp, jtr_p, ytr_p), score_forms(Fp, jte_p, yte_p)
    say(f"     fitted: LIN dSharpe = {parp['lin_a']:+.4f} {parp['lin_b']:+.4f}*JAC")
    say(f"     {'form':6s} {'RMSE_tr':>9s} {'RMSE_te':>9s} {'MAE_te':>9s} {'rho_te':>8s}"
        f" {'sign_te':>8s}   vs CONST")
    for k in ("CONST", "LIN", "SQRT", "STEP"):
        dlt = s_tep[k]["RMSE"] - s_tep["CONST"]["RMSE"]
        say(f"     {k:6s} {s_trp[k]['RMSE']:9.4f} {s_tep[k]['RMSE']:9.4f} {s_tep[k]['MAE']:9.4f} "
            f"{s_tep[k]['rho']:+8.3f} {s_tep[k]['sign_acc']:8.2f}   {dlt:+.4f} "
            f"{'(better)' if dlt < 0 else '(worse)' if dlt > 0 else ''}")
    o_te, p_te_p, n_te, kd_te = perm_dial_p(TEC)
    say(f"     held-out cells n={len(TEC)}: Spearman(JAC_IS, OOS edge) = {o_te:+.3f}, "
        f"dial-label permutation p = {p_te_p:.3f} ({kd_te}, {n_te} labellings)")
    for k in ("LIN", "SQRT", "STEP"):
        pr_te = np.asarray(Fp[k](jte_p), float)
        thr = float(np.median(np.asarray(Fp[k](jtr_p), float)))
        for sv in (screen_value(pr_te, yte_p, 0.0, ">0"),
                   screen_value(pr_te, yte_p, thr, "top-half")):
            say(f"     SCREEN[{k:4s} {sv['rule']:8s}] admits {sv['n_admit']:3d}/{sv['n_total']}: "
                f"edge admitted {sv['mean_admit']:+.4f}  rejected {sv['mean_reject']:+.4f}  "
                f"spend-everywhere {sv['mean_all']:+.4f}  LIFT {sv['lift']:+.4f}")

    fitrows = []
    for c in CELL_RUNGS:
        for form in ("DEFAULT", "MEDIAN"):
            D = C[(C.rung == c) & (C.form == form)]
            tr, te = D[D.dial_set == "TRAIN"], D[D.dial_set == "TEST"]
            jtr, ytr = tr.JAC_IS.values, tr.d_oos.values
            jte, yte = te.JAC_IS.values, te.d_oos.values
            F, par = fit_forms(jtr, ytr)
            s_tr, s_te = score_forms(F, jtr, ytr), score_forms(F, jte, yte)
            say("")
            say(f"  --- rung {c:g} bps, control = {form} "
                f"(TRAIN n={len(tr)} cells, TEST n={len(te)} cells) ---")
            say(f"      fitted on TRAIN:  LIN dSharpe = {par['lin_a']:+.4f} "
                f"{par['lin_b']:+.4f}*JAC    SQRT = {par['sqrt_a']:+.4f} "
                f"{par['sqrt_b']:+.4f}*sqrt(JAC)    STEP tau={par['tau']:.4f} "
                f"(hi {par['step_hi']:+.4f} / lo {par['step_lo']:+.4f})")
            hdr = f"      {'form':6s} {'RMSE_tr':>9s} {'RMSE_te':>9s} {'MAE_te':>9s} " \
                  f"{'rho_te':>8s} {'sign_te':>8s}   vs CONST"
            say(hdr)
            for k in ("CONST", "LIN", "SQRT", "STEP"):
                delta = s_te[k]["RMSE"] - s_te["CONST"]["RMSE"]
                say(f"      {k:6s} {s_tr[k]['RMSE']:9.4f} {s_te[k]['RMSE']:9.4f} "
                    f"{s_te[k]['MAE']:9.4f} {s_te[k]['rho']:+8.3f} {s_te[k]['sign_acc']:8.2f}   "
                    f"{delta:+.4f} {'(better)' if delta < 0 else '(worse)' if delta > 0 else ''}")
                fitrows.append(dict(rung=c, form=form, f_form=k, RMSE_train=s_tr[k]["RMSE"],
                                    RMSE_test=s_te[k]["RMSE"], MAE_test=s_te[k]["MAE"],
                                    rho_test=s_te[k]["rho"], sign_test=s_te[k]["sign_acc"],
                                    **{f"p_{kk}": vv for kk, vv in par.items()}))
            rho_tr = spearman(jtr, ytr)
            rho_te, p_te, np_te, kd = perm_dial_p(te)
            say(f"      direct Spearman(JAC_IS, OOS edge): TRAIN {rho_tr:+.3f} (n={len(tr)})   "
                f"TEST {rho_te:+.3f} (n={len(te)}), dial-label p = {p_te:.3f} ({kd})")
            for k in ("LIN", "SQRT", "STEP"):
                pr = np.asarray(F[k](jte), float)
                thr = float(np.median(np.asarray(F[k](jtr), float)))
                for sv in (screen_value(pr, yte, 0.0, ">0"),
                           screen_value(pr, yte, thr, "top-half")):
                    say(f"      SCREEN[{k:4s} {sv['rule']:8s}] admits {sv['n_admit']:2d}/"
                        f"{sv['n_total']}: edge admitted {sv['mean_admit']:+.4f}  rejected "
                        f"{sv['mean_reject']:+.4f}  spend-everywhere {sv['mean_all']:+.4f}  "
                        f"LIFT {sv['lift']:+.4f}")
                    fitrows.append(dict(rung=c, form=form, f_form=f"SCREEN_{k}", **sv))
    pd.DataFrame(fitrows).to_csv(OUT / f"{STEM}.fit.csv", index=False)

    # ---- per-dial held-out detail -------------------------------------------------
    say("")
    say("  held-out dials, 10 bps, DEFAULT control — what the screen was asked to predict:")
    te = C[(C.rung == PCOST) & (C.form == "DEFAULT") & (C.dial_set == "TEST")]
    tbl = te.groupby("dial").agg(JAC_IS=("JAC_IS", "mean"), d_oos_med=("d_oos", "median"),
                                 d_oos_mean=("d_oos", "mean"),
                                 wins=("d_oos", lambda s: int((s > 0).sum())),
                                 abstain=("abstain", "sum")).sort_values("JAC_IS", ascending=False)
    say(tbl.to_string(float_format=lambda x: f"{x:+.4f}"))

    # ---- the ABSTENTION decomposition ---------------------------------------------
    # A chooser that picks the control produces d_oos == 0 EXACTLY.  A dial whose rungs barely move
    # the book abstains often, so its edge is pinned at zero — which would make "JAC orders the
    # edge" a statement about how often the chooser moves at all, not about what it wins when it
    # does.  Split the correlation on exactly that.
    say("")
    say("  DECOMPOSITION — is the law an EDGE law or an ABSTENTION law?")
    for lbl, D in (("TRAIN", TRC), ("TEST", TEC)):
        ab = D.groupby("dial").agg(JAC=("JAC_IS", "mean"), abst=("abstain", "mean"))
        mv = D[~D.abstain]
        r_ab = spearman(ab.JAC.values, ab.abst.values)
        r_mv = spearman(mv.JAC_IS.values, mv.d_oos.values)
        o_mv, p_mv, _, kd_mv = perm_dial_p(mv) if mv.dial.nunique() > 2 else (np.nan, np.nan, 0, "n/a")
        say(f"    {lbl:5s} abstention rate {float(D.abstain.mean()):.1%} of {len(D)} cells;  "
            f"Spearman(JAC, per-dial ABSTENTION rate) = {r_ab:+.3f}")
        say(f"    {lbl:5s} among the {len(mv)} cells where the chooser actually MOVED: "
            f"Spearman(JAC, OOS edge) = {r_mv:+.3f}"
            + (f", dial-label p = {p_mv:.3f} ({kd_mv})" if np.isfinite(p_mv) else ""))
    say("    (If the abstention correlation is strongly negative and the moved-cell correlation "
        "collapses, the 'effect-size law' is an artefact of how often a dial's rungs differ at all.)")

    # ---- PART D — the book, as PROTOCOL requires -----------------------------------
    say("")
    say("=" * 110)
    say("PART D — PROTOCOL 4a / 4b ON EVERY ARM, AND RULE 8 ON THE CHOOSER'S OWN PICK")
    say("=" * 110)
    say(f"  full-sample 10 bps: 4a {int(G.p4a_full.sum())}/{len(G)}   4b {int(G.p4b_full.sum())}/{len(G)}")
    say(f"  OOS-window re-cut : 4a {int(G.p4a_oos.sum())}/{len(G)}   4b {int(G.p4b_oos.sum())}/{len(G)}")
    if int(G.p4b_full.sum()):
        by = (G[G.p4b_full].groupby(["panel", "dial"]).size().rename("n_4b").reset_index())
        say("  4b passers by (panel, dial):")
        say(by.to_string(index=False))
    # rule 8 on the KEEP question itself: pick on IS Sharpe, then read 4b on the untouched OOS
    k8 = []
    for pk in PANELS:
        for d in DIALS:
            g = G[(G.panel == pk) & (G.dial == d)].set_index("value")
            pick = g[f"sh_is_{PCOST:g}"].idxmax()
            k8.append(dict(panel=pk, dial=d, pick=pick,
                           p4b_oos=bool(g.loc[pick, "p4b_oos"]),
                           p4a_oos=bool(g.loc[pick, "p4a_oos"]),
                           cagr_oos=float(g.loc[pick, f"cagr_oos_{PCOST:g}"]),
                           sh_oos=float(g.loc[pick, f"sh_oos_{PCOST:g}"]),
                           dd_oos=float(g.loc[pick, f"dd_oos_{PCOST:g}"])))
    K8 = pd.DataFrame(k8)
    say(f"  rule-8 picks (choose on IS, read OOS): 4b_oos {int(K8.p4b_oos.sum())}/{len(K8)}   "
        f"4a_oos {int(K8.p4a_oos.sum())}/{len(K8)}")
    say("  per-panel OOS medians of the rule-8 picks (10 bps):")
    say(K8.groupby("panel")[["cagr_oos", "sh_oos", "dd_oos"]].median()
        .to_string(float_format=lambda x: f"{x:.3f}"))

    say("")
    say("=" * 110)
    say("VERDICT")
    say("=" * 110)
    beat = [k for k in ("LIN", "SQRT", "STEP") if s_tep[k]["RMSE"] < s_tep["CONST"]["RMSE"]]
    best = min(("LIN", "SQRT", "STEP"), key=lambda k: s_tep[k]["RMSE"])
    gain = 1.0 - s_tep[best]["RMSE"] / s_tep["CONST"]["RMSE"]
    ok = bool(beat) and np.isfinite(p_te_p) and p_te_p < 0.05 and o_te > 0
    say(f"  TRAINING correlation, 624's own pooling : per-dial median {r_med:+.3f} "
        f"(624 published +0.884), cell level {r_cell:+.3f} (624 published +0.388), "
        f"dial-label p = {p_tr:.3f}")
    say(f"  HELD-OUT (6 fresh dials, {len(TEC)} cells)   : Spearman {o_te:+.3f}, "
        f"dial-label permutation p = {p_te_p:.3f}")
    say(f"  forms beating the CONST null on held-out RMSE: {beat or 'NONE'}; best {best} cuts RMSE "
        f"by {gain:+.1%} ({s_tep['CONST']['RMSE']:.4f} -> {s_tep[best]['RMSE']:.4f})")
    say(f"  mean OOS chooser edge across all held-out cells: {float(np.mean(yte_p)):+.4f} Sharpe; "
        f"the spread f is asked to explain has SD {float(np.std(yte_p)):.4f}.")
    say(f"  => f(JAC) is {'a usable' if ok else 'NOT a usable'} pre-spend screening rule.")
    say(f"  PROTOCOL: 4a {int(G.p4a_full.sum())}/{len(G)}, 4b {int(G.p4b_full.sum())}/{len(G)}; "
        f"no arm in this file is proposed for capital.")
    say(f"  [{time.time() - t0:.1f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

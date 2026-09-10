#!/usr/bin/env python3
"""Idea 631 -- re-cut the record's WINDOW-WIDTH claims as width per point.  (lane C, 2026-09-10)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number in this file was read)
    Idea 409 showed window width in POINTS scales with grid density (width/point stable to
    ~0.02 across x1/x2/x4 on all five non-empty dials), so idea 401's "median width 0 vs 4"
    conflates a dial's passing fraction with the density it happened to be published at.
    Census every committed window/plateau width in the record, restate it as width/points,
    and report how many published width COMPARISONS between dials survive the change of units.

THE THREE UNITS A WIDTH CAN BE WRITTEN IN, and what each is a fact about
    PTS    the number of GRID POINTS in the window.  Depends on the publisher's spacing:
           double the density and it roughly doubles.  This is the unit idea 401 published in.
    FRAC   PTS divided by the number of points in the sweep -- the queue's "width per point".
           Density-free, but it is a share of the SWEPT RANGE, so it depends on where the
           publisher put the two endpoints, which is a second free choice nobody declares.
    UNITS  the span in the dial's own units (band percentage points, gross, names, days).
           Density-free AND endpoint-free, but INCOMMENSURABLE BETWEEN DIALS: 4 percentage
           points of band and 4 names of n are not the same width of anything.
    So a BETWEEN-DIAL width comparison has no unit that is simultaneously density-free,
    endpoint-free and commensurable.  Whether that abstract point has teeth is an empirical
    question -- how many published comparisons actually change reading -- and this file
    answers it by counting, not by arguing.

    PART A  CENSUS.  Every committed research/backtests/*.csv column whose name matches the
            width family, classified by UNIT and by whether a denominator is recoverable.
            The inclusion rule is mechanical and every exclusion is written out with its
            reason, so the corpus boundary is auditable rather than hand-picked.
    PART B  RESTATEMENT.  Every in-scope PTS-unit width re-read as FRAC (and, where the
            dial's step is recoverable, as UNITS).
    PART C  COMPARISONS.  Every published between-dial width comparison the record contains,
            at CELL level (within one panel/book/cost) and at CLAIM level (the per-dial
            median idea 401 actually published), re-read in each unit.  AGREE / FLIP /
            TIE-BROKEN / TIE-CREATED.  Run in both directions: the window family, published
            in PTS, re-read in FRAC; and the plateau family, published in FRAC, re-read in
            PTS -- so the test is not rigged to the unit that happens to win.
    PART D  DENSITY.  A fresh grid whose spacing THIS FILE controls (x1/x2/x4), to measure
            which of the three units is actually density-free rather than assuming it.
    PART E  RULE 8 (PROTOCOL 8) + BOTH KEEP PATHS on every fresh grid point: does the unit a
            width is written in change which dial value a rule-8 chooser picks, and what that
            pick earns out of sample against the live baseline and SPY.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    STATISTIC in {PTS, FRAC, UNITS}       the unit a width is read in (parts B, C, E)
    CLAIMSET  in {ALL, WINDOW, PLATEAU}   which committed width family the claim is read over
Everything else is a corpus axis held identical across cells and reported in full: panel
{U56, B136, SMALL439}, book {EWall, TOP20}, cost {10, 25} bps, dial {band, gross, n, K, vol,
f}, resolution {x1, x2, x4}.  Every grid point of every sweep is written to .grid.csv; every
censused column to .census.csv; every restated claim to .claims.csv; every comparison to
.pairs.csv; the density read to .density.csv; rule 8 to .walkforward.csv.

PROTOCOL-fixed: weights decided at close t, applied at t+1; 10 bps per unit turnover (25 bps
carried as a corpus axis in the census only); long only, no leverage; warm-up 260 rows
dropped; halves at len(r)//2; rule 8 split at 2016-12-31.
SURVIVORSHIP (PROTOCOL 9): B136 and SMALL439 are CURRENT constituent lists -- they exclude
names that were delisted, acquired or fell out of the screen, so their absolute levels are
biased UP and no CAGR/Sharpe from them is a tradable estimate.  Only the WITHIN-panel
contrasts this file reports (which unit a width is read in) are meant to survive that.
SMALL439 drops the 44 names with data/small_meta.csv max_1d_move >= 1.0 before anything else.

Run:  python3 research/backtests/2026-09-10_re-cut-the-record-s-WINDOW-WIDTH-claims-as-width-per-point_C.py
"""
import itertools, re, sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights          # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics                            # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)
OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST_BPS, WARMUP, FREQ = 10.0, 260, "W"
PHI, DELTA = 0.70, 0.60                      # PROTOCOL 4b CAGR floor / DD cap vs SPY
PLATEAU_EPS = 0.05                           # idea 128's tolerance, unchanged
STATISTICS = ["PTS", "FRAC", "UNITS"]
CLAIMSETS = ["ALL", "WINDOW", "PLATEAU"]
EPS = 1e-12
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ==================================================================== PART A: census machinery
WIDTH_RE = re.compile(r"width|plateau_frac|window_w", re.I)
PTS_RE = re.compile(r"^(pts|n_pts|n_points|points|sweep_pts|npts|scale_pts|bc_points|"
                    r"oos_points|ctl_pts|sharpe_pts)$", re.I)


def lohi_candidates(col):
    """Pre-registered list of lo/hi column-name partners for a width column.

    A width that equals hi - lo on its own row is a span in the DIAL'S OWN UNITS; that is the
    only mechanical way to tell a units-width from a points-width without reading the script.
    """
    stem = re.sub(r"width$", "", col)
    return [(stem + "lo", stem + "hi"), (stem + "_lo", stem + "_hi"),
            ("lo", "hi"), ("g_lo", "g_hi"), ("m_lo", "m_hi"),
            (stem + "g_lo", stem + "g_hi"), (stem + "run_lo", stem + "run_hi"),
            ("run_lo", "run_hi"), (stem + "ind_lo", stem + "ind_hi"),
            (stem + "_ind_lo", stem + "_ind_hi")]


def classify(df, col):
    """UNIT of one width column, decided mechanically and in a fixed order.

    FRAC   the name says so (it is already a share -- density-free as published).
    UNITS  the value reproduces hi - lo on >90% of its own rows, or the name carries the
           dial's unit as a suffix (_pp, _vol_pts).
    PTS    everything else that is integer-valued on every non-null row.
    REAL   non-integer with no lo/hi partner -- a width of something, but not a point count;
           reported and excluded rather than guessed at.
    """
    v = pd.to_numeric(df[col], errors="coerce")
    if v.notna().sum() == 0:
        return "EMPTY", ""
    lc = col.lower()
    if "frac" in lc:
        return "FRAC", "name"
    if lc.endswith("_pp") or lc.endswith("_vol_pts"):
        return "UNITS", "name-suffix"
    for lo, hi in lohi_candidates(col):
        if lo in df.columns and hi in df.columns:
            d = pd.to_numeric(df[hi], errors="coerce") - pd.to_numeric(df[lo], errors="coerce")
            ok = np.isclose(d.values, v.values, rtol=1e-6, atol=1e-9, equal_nan=True)
            if np.nanmean(ok) > 0.90:
                return "UNITS", f"{hi}-{lo}"
    iv = v.dropna().values
    if len(iv) and np.allclose(iv, np.round(iv)):
        return "PTS", "integer-valued"
    return "REAL", "non-integer, no lo/hi partner"


def has_dial_axis(df):
    """IN-SCOPE test: is this column a width of a set along a SWEPT DIAL?

    A width column qualifies only if its own file carries a swept-dial axis -- a `dial`
    column, a point-count column, or a lo/hi pair.  Without one, a column called `width` is
    some other quantity (a synthetic panel's width parameter, a prediction interval, a
    bandwidth) and is recorded OUT-OF-SCOPE with that reason rather than silently censused.
    """
    if "dial" in df.columns:
        return True, "dial column"
    pc = [c for c in df.columns if PTS_RE.match(c)]
    if pc:
        return True, "point-count column " + ";".join(pc)
    for c in df.columns:
        if WIDTH_RE.search(c):
            for lo, hi in lohi_candidates(c):
                if lo in df.columns and hi in df.columns:
                    return True, f"lo/hi pair {lo}/{hi}"
    return False, "no dial axis (no dial column, no point count, no lo/hi pair)"


def census():
    rows, ncsv = [], 0
    for f in sorted(BT.glob("*.csv")):
        ncsv += 1
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception as e:                                   # unreadable artefact
            rows.append(dict(file=f.name, col="", unit="UNREADABLE", reason=str(e)[:60],
                             n=0, in_scope=0, denom="", denom_src="", has_dial=0))
            continue
        wc = [c for c in df.columns if WIDTH_RE.search(c)]
        if not wc:
            continue
        ok, why = has_dial_axis(df)
        pc = [c for c in df.columns if PTS_RE.match(c)]
        for c in wc:
            unit, ev = classify(df, c)
            v = pd.to_numeric(df[c], errors="coerce")
            denom, dsrc = "", ""
            if unit == "PTS":
                # prefer the SWEPT point count (controls excluded) over the raw one
                for cand in ("sweep_pts", "pts", "n_pts", "n_points", "points", "ctl_pts"):
                    if cand in df.columns:
                        denom, dsrc = cand, "in-row"
                        break
            rows.append(dict(file=f.name, col=c, unit=unit, reason=(ev if ok else why),
                             n=int(v.notna().sum()), in_scope=int(ok), denom=denom,
                             denom_src=dsrc, has_dial=int("dial" in df.columns)))
    return pd.DataFrame(rows), ncsv


# ============================================================== PART C: comparison machinery
def sgn(a, b, tol=1e-12):
    if not (np.isfinite(a) and np.isfinite(b)):
        return np.nan
    if abs(a - b) <= tol:
        return 0
    return 1 if a > b else -1


def compare_pairs(tbl, wcol, dcol, key, label, denom_col, lohi=None):
    """Every unordered dial pair inside every `key` group, read in each of the 3 units.

    tbl        one committed CSV
    wcol       the published width column (PTS units)
    dcol       the dial column
    key        the cell key the record groups by (panel, book, cost, ...)
    denom_col  the point count for FRAC
    lohi       (lo_col, hi_col) naming the window's DIAL-VALUE edges, where the file committed
               them.  UNITS = hi - lo.  Where a file did not commit the edges, UNITS is NaN
               and the pair is simply absent from the UNITS counts -- never imputed from a
               nominal step, because idea 401's band sweep (0/2/3/5/8) is not uniform and a
               nominal step would silently invent the number.
    """
    out = []
    for kv, g in tbl.groupby(key, dropna=False):
        g = g.dropna(subset=[wcol])
        for da, db in itertools.combinations(sorted(g[dcol].astype(str).unique()), 2):
            ra, rb = g[g[dcol].astype(str) == da], g[g[dcol].astype(str) == db]
            if len(ra) != 1 or len(rb) != 1:
                continue
            ra, rb = ra.iloc[0], rb.iloc[0]
            wa, wb = float(ra[wcol]), float(rb[wcol])
            na, nb = float(ra[denom_col]), float(rb[denom_col])
            fa = wa / na if na > 0 else np.nan
            fb = wb / nb if nb > 0 else np.nan
            ua = ub = np.nan
            if lohi and lohi[0] in tbl.columns and lohi[1] in tbl.columns:
                # an EMPTY window has no edges; its units-width is 0, not missing
                ua = 0.0 if wa == 0 else float(ra[lohi[1]]) - float(ra[lohi[0]])
                ub = 0.0 if wb == 0 else float(rb[lohi[1]]) - float(rb[lohi[0]])
            s_p, s_f, s_u = sgn(wa, wb), sgn(fa, fb), sgn(ua, ub)
            out.append(dict(source=label, cell="|".join(map(str, kv)) if isinstance(kv, tuple) else str(kv),
                            dial_a=da, dial_b=db, pts_a=na, pts_b=nb,
                            w_pts_a=wa, w_pts_b=wb, w_frac_a=fa, w_frac_b=fb,
                            w_units_a=ua, w_units_b=ub,
                            sign_PTS=s_p, sign_FRAC=s_f, sign_UNITS=s_u,
                            same_density=int(abs(na - nb) < 1e-9)))
    return pd.DataFrame(out)


def verdict_table(P, a="sign_PTS", b="sign_FRAC"):
    d = P.dropna(subset=[a, b]).copy()
    sa, sb = d[a].astype(int), d[b].astype(int)
    return dict(n=len(d),
                agree=int(((sa == sb)).sum()),
                flip=int(((sa * sb) < 0).sum()),
                tie_broken=int(((sa == 0) & (sb != 0)).sum()),
                tie_created=int(((sa != 0) & (sb == 0)).sum()))


# ============================================================ PART D/E: fresh grid machinery
def fast_backtest(prices, weights, freq=FREQ):
    """Vectorised equivalent of engine.backtest; asserted identical by gate G1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


DIALS = dict(
    band=dict(c0=0.03, step=0.01, lo=0.00, hi=0.12, host="V2", integer=False),
    # gross stops at 1.00: PROTOCOL 2 forbids leverage unless the idea asks for it, and this
    # idea is about UNITS, not about exposure.  A 1.20 ceiling would have handed the sweep
    # idea 311's g-band loophole and every 4b count below would have been about that instead.
    gross=dict(c0=0.75, step=0.05, lo=0.30, hi=1.00, host="V2", integer=False),
    n=dict(c0=20, step=4, lo=4, hi=40, host="V1", integer=True),
)
RES = {"x1": 1, "x2": 2, "x4": 4}


class Panel:
    def __init__(self, px):
        q = px.drop(columns=["SPY"]); self.px, self.q = px, q
        mom = q.shift(21) / q.shift(252) - 1
        r6 = q / q.shift(126) - 1
        r3 = q / q.shift(63) - 1
        self.comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                     + r3.rank(axis=1, pct=True)) / 3
        self.vol20 = q.pct_change().rolling(20).std() * np.sqrt(252)
        self.notna = q.notna()
        self.ma200 = q.rolling(200).mean()
        self.above = q > self.ma200
        self._band = {}
        spy = px["SPY"].pct_change().fillna(0.0)
        self.spy = legs(spy)

    def band_state(self, band):
        k = round(float(band), 8)
        if k not in self._band:
            raw = pd.DataFrame(np.nan, index=self.q.index, columns=self.q.columns)
            raw = raw.mask(self.q > self.ma200 * (1 + k), 1.0).mask(self.q < self.ma200 * (1 - k), 0.0)
            self._band[k] = raw.ffill().fillna(0.0) > 0.5
        return self._band[k]

    def w_v2(self, band, gross):
        e = self.notna.astype(float)
        ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(self.band_state(band), 0.0)

    def w_v1(self, n, w=0.15, vol=0.60):
        s = self.comp * (0.5 + 0.5 * self.above.astype(float))
        s = s / self.vol20.clip(lower=0.08) ** 0.5
        elig = s.where(self.above & (self.vol20 < vol))
        return (elig.rank(axis=1, ascending=False) <= n).astype(float) * w

    def book(self, dial, c):
        if DIALS[dial]["host"] == "V2":
            return self.w_v2(c if dial == "band" else DIALS["band"]["c0"],
                             c if dial == "gross" else DIALS["gross"]["c0"])
        return self.w_v1(int(round(c)))


def grid_for(dial, res):
    """The dial's sweep at resolution `res`.  x1 is this file's published spacing; x2/x4 halve
    and quarter it.  Endpoints are IDENTICAL at every resolution, so FRAC's second free choice
    (where the sweep stops) is held fixed and only the density moves.  An integer dial whose
    step has reached 1 is EXHAUSTED and is carried unrefined rather than silently padded."""
    d = DIALS[dial]
    h = d["step"] / RES[res]
    exhausted = False
    if d["integer"]:
        h = int(round(h))
        if h < 1:
            h, exhausted = 1, True
        g = list(range(int(d["lo"]), int(d["hi"]) + 1, h))
        return sorted(set(g)), float(h), exhausted
    nlo = int(round((d["c0"] - d["lo"]) / h)); nhi = int(round((d["hi"] - d["c0"]) / h))
    return [round(d["c0"] + i * h, 10) for i in range(-nlo, nhi + 1)], h, exhausted


def legs(r):
    r = r.iloc[WARMUP:] if len(r) > WARMUP else r
    h = len(r) // 2
    f, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    hi = len(ri) // 2
    i, i1, i2, o = metrics(ri), metrics(ri.iloc[:hi]), metrics(ri.iloc[hi:]), metrics(ro)
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_CAGR=i["CAGR"], IS_Sharpe=i["Sharpe"], IS_MaxDD=i["MaxDD"],
                IS_H1=i1["Sharpe"], IS_H2=i2["Sharpe"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def m4b_full(L, S):
    """The five PROTOCOL-4b bars over the full sample, signed; >= 0 passes."""
    return dict(H1=L["H1"] - S["H1"], H2=L["H2"] - S["H2"], OOS=L["OOS_Sharpe"] - S["OOS_Sharpe"],
                DD=L["MaxDD"] - DELTA * S["MaxDD"], CAGR=L["CAGR"] - PHI * S["CAGR"])


def m4b_is(L, S):
    """The same five bars read INSIDE the IS window only -- rule 8's choosing side.  The OOS
    slot becomes the IS-window full Sharpe, because no OOS data may be read to choose."""
    return dict(H1=L["IS_H1"] - S["IS_H1"], H2=L["IS_H2"] - S["IS_H2"],
                OOS=L["IS_Sharpe"] - S["IS_Sharpe"], DD=L["IS_MaxDD"] - DELTA * S["IS_MaxDD"],
                CAGR=L["IS_CAGR"] - PHI * S["IS_CAGR"])


def pass4a(L, B):
    return int(L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"])


def widest_run(flags, vals, step):
    """Longest contiguous run of True in `flags` along the ordered dial.

    Returns (width_in_points, width_in_dial_units, lo, hi).  A run of k points spans
    (k-1)*step in dial units; a single passing point has PTS width 1 and UNITS width 0, and
    that asymmetry is exactly why the two units are not rescalings of each other."""
    best = (0, np.nan, np.nan)
    i = 0
    while i < len(flags):
        if flags[i]:
            j = i
            while j + 1 < len(flags) and flags[j + 1]:
                j += 1
            if (j - i + 1) > best[0]:
                best = (j - i + 1, vals[i], vals[j])
            i = j + 1
        else:
            i += 1
    k, lo, hi = best
    return k, ((hi - lo) if k > 0 else np.nan), lo, hi


# ======================================================================================= gates
def gate_g1(P):
    w = P.w_v2(0.03, 0.75)
    fr, ft = fast_backtest(P.q, w)
    eng = backtest(P.q, w, cost_bps=0.0, freq=FREQ)
    st = P.q.index[WARMUP]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    say(f"G1  fast_backtest vs engine.backtest:  max|dret| {dr:.3e}   max|dturn| {dt:.3e}")
    assert dr < 1e-10 and dt < 1e-10, "G1 FAILED"


def gate_g2(P):
    d2 = float((P.w_v2(0.03, 0.75) - rules_v2_weights(P.q, 0.03, 0.75)).abs().max().max())
    d1 = float((P.w_v1(20) - rules_v1_weights(P.q, n=20, w=0.15, max_vol=0.60)).abs().max().max())
    say(f"G2  host V2 vs baseline.rules_v2_weights {d2:.3e};  host V1 vs rules_v1_weights {d1:.3e}")
    assert d2 < 1e-12 and d1 < 1e-12, "G2 FAILED"


def gate_g3():
    """G3  the arithmetic the whole file turns on, checked before any real number is read.

    Halving a grid's spacing takes a k-point window to 2k-1 points, leaves the DIAL-UNIT span
    exactly fixed, and leaves FRAC fixed only up to the endpoint convention (both counts gain
    the same +1 for the closing endpoint, so FRAC moves by O(1/pts) and not by the density).
    That residual is the reason FRAC is checked empirically in PART D rather than assumed."""
    vals1 = np.arange(0, 12.001, 1.0)
    vals2 = np.arange(0, 12.001, 0.5)
    f1 = (vals1 >= 3) & (vals1 <= 7)
    f2 = (vals2 >= 3) & (vals2 <= 7)
    k1, u1, _, _ = widest_run(f1, vals1, 1.0)
    k2, u2, _, _ = widest_run(f2, vals2, 0.5)
    say(f"G3  synthetic window [3,7] on a 1.0 grid vs a 0.5 grid: "
        f"PTS {k1} -> {k2} (x{k2/k1:.2f});  FRAC {k1/len(vals1):.4f} -> {k2/len(vals2):.4f};  "
        f"UNITS {u1:.2f} -> {u2:.2f}")
    assert k2 == 2 * k1 - 1 and abs(u1 - u2) < 1e-12, "G3 FAILED"


def gate_g0(shape):
    """G0  reproduce idea 401's published per-dial MEDIAN window width from its own committed
    artefact before re-reading it.  If the file does not say what the record says it says,
    nothing downstream means anything."""
    med = shape.groupby("dial").window_w.median().sort_index()
    say("G0  idea 401 committed per-dial median window_w (PTS), read from its own .shape.csv:")
    say("    " + "  ".join(f"{k}={v:g}" for k, v in med.items()))
    return med


# ==================================================================================== loaders
def load_panels():
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    drop = [c for c in sm.columns if c in bad]
    P["SMALL439"] = sm.drop(columns=drop)
    say(f"    SMALL: dropped {len(drop)} names with max_1d_move >= 1.0 -> {P['SMALL439'].shape[1]-1} names")
    return P


# ======================================================================================= main
def main():
    say("=" * 100)
    say("IDEA 631  re-cut the record's WINDOW-WIDTH claims as width per point   (lane C, 2026-09-10)")
    say("=" * 100)

    # ------------------------------------------------------------------ PART A  CENSUS
    say("\n=== PART A  CENSUS of every committed width-family column ===")
    CEN, ncsv = census()
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  scanned {ncsv} committed research/backtests/*.csv; "
        f"{CEN.file.nunique()} carry a width-family column; {len(CEN)} columns in total")
    say("\n  by UNIT and scope (values = non-null committed numbers):")
    piv = CEN.groupby(["unit", "in_scope"]).agg(cols=("col", "size"), values=("n", "sum")).reset_index()
    say(piv.to_string(index=False))
    IN = CEN[(CEN.in_scope == 1) & (CEN.unit != "EMPTY")].copy()
    OUTS = CEN[(CEN.in_scope == 0) | (CEN.unit == "EMPTY")].copy()
    say(f"\n  IN SCOPE  {len(IN)} columns / {int(IN.n.sum())} committed values")
    say(f"  EXCLUDED  {len(OUTS)} columns / {int(OUTS.n.sum())} values, every one with its reason:")
    for _, r in OUTS.iterrows():
        say(f"    - {r.file}::{r.col}  [{r.unit}]  {r.reason}")

    pts = IN[IN.unit == "PTS"]
    say(f"\n  DENSITY-DEPENDENT (PTS) columns: {len(pts)} / {int(pts.n.sum())} values")
    say(f"  of which a denominator is recoverable IN-ROW: "
        f"{int((pts.denom != '').sum())} columns / {int(pts.loc[pts.denom != '', 'n'].sum())} values")
    for _, r in pts.iterrows():
        say(f"    {r.file}::{r.col:16s} n={r.n:5d}  denom={r.denom or 'NONE'}")
    say(f"\n  ALREADY DENSITY-FREE as published:  FRAC {int(IN.loc[IN.unit=='FRAC','n'].sum())} values, "
        f"UNITS {int(IN.loc[IN.unit=='UNITS','n'].sum())} values")

    # ------------------------------------------------- PART B  RESTATEMENT of every PTS width
    say("\n=== PART B  RESTATEMENT: every in-scope PTS width re-read as width/points ===")
    claims = []
    for _, r in pts.iterrows():
        if not r.denom:
            continue
        d = pd.read_csv(BT / r.file, low_memory=False)
        w = pd.to_numeric(d[r.col], errors="coerce")
        nn = pd.to_numeric(d[r.denom], errors="coerce")
        fr = w / nn.replace(0, np.nan)
        for i in range(len(d)):
            claims.append(dict(file=r.file, col=r.col, row=i,
                               dial=(d["dial"].iloc[i] if "dial" in d.columns else ""),
                               panel=(d["panel"].iloc[i] if "panel" in d.columns else ""),
                               book=(d["book"].iloc[i] if "book" in d.columns else ""),
                               cost=(d["cost"].iloc[i] if "cost" in d.columns else np.nan),
                               res=(d["res"].iloc[i] if "res" in d.columns else ""),
                               grid=(d["grid"].iloc[i] if "grid" in d.columns else ""),
                               w_pts=w.iloc[i], pts=nn.iloc[i], w_frac=fr.iloc[i]))
    CL = pd.DataFrame(claims)
    CL.to_csv(f"{OUT}.claims.csv", index=False)
    say(f"  restated {len(CL)} committed PTS width values across {CL.file.nunique()} files")
    say("\n  distribution of the SAME claims in the two units:")
    say(CL[["w_pts", "pts", "w_frac"]].describe().T.to_string(float_format=lambda x: f"{x:.4f}"))
    nz = CL[CL.w_pts > 0]
    bad = CL[~(CL.pts > 0)]
    good = CL[CL.pts > 0]
    say(f"\n  non-zero widths: {len(nz)} of {len(CL)}.  Sweep length `pts` over the "
        f"{len(good)} restatable rows ranges {int(good.pts.min())}..{int(good.pts.max())} "
        f"-- a {good.pts.max()/good.pts.min():.1f}x spread in the denominator alone, which is "
        f"the entire size of the unit problem.")
    if len(bad):
        say(f"  {len(bad)} rows publish a width against a ZERO point count and cannot be "
            f"restated at all: " + "; ".join(sorted(set(bad.file + '::' + bad.col))))

    # ---------------------------------------------- PART C  BETWEEN-DIAL COMPARISONS
    say("\n=== PART C  every published BETWEEN-DIAL width comparison, re-read ===")
    shape = pd.read_csv(BT / "2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.shape.csv")
    med401 = gate_g0(shape)

    # C1  cell-level pairs on idea 401's window family (published in PTS)
    P401 = compare_pairs(shape, "window_w", "dial", ["panel", "book", "cost"],
                         "401-window-cell", "sweep_pts")
    # C2  cell-level pairs on idea 409's re-run of the same cells at 3 resolutions
    cells = pd.read_csv(BT / "2026-09-10_why-do-4b-windows-have-width-0-on-four-of-six-dials_B.cells.csv")
    P409 = compare_pairs(cells, "window_w", "dial", ["panel", "book", "cost", "res"],
                         "409-window-cell", "pts", lohi=("window_lo", "window_hi"))
    # C3  cell-level pairs on the PLATEAU family, published as a FRACTION (the mirror test:
    #     what would have flipped had idea 128 published points instead of shares?)
    plat = pd.read_csv(BT / "2026-09-05_threshold-plateaus-are-the-general-case_cloud.plateaus.csv")
    plat = plat.assign(plateau_pts=(plat.plateau_frac * plat.pts).round())
    PPL = compare_pairs(plat, "plateau_pts", "dial", ["panel", "book", "cost"],
                        "128-plateau-cell", "pts")

    PAIRS = pd.concat([P401, P409, PPL], ignore_index=True)
    PAIRS.to_csv(f"{OUT}.pairs.csv", index=False)

    say("\n  CELL-LEVEL between-dial pairs, PTS vs FRAC:")
    rows = []
    for src, g in PAIRS.groupby("source"):
        v = verdict_table(g); v["source"] = src
        v["survive_%"] = 100.0 * v["agree"] / max(v["n"], 1)
        v["same_density_pairs"] = int(g.same_density.sum())
        rows.append(v)
    v = verdict_table(PAIRS); v["source"] = "ALL"; v["survive_%"] = 100.0 * v["agree"] / max(v["n"], 1)
    v["same_density_pairs"] = int(PAIRS.same_density.sum())
    rows.append(v)
    VC = pd.DataFrame(rows)[["source", "n", "agree", "flip", "tie_broken", "tie_created",
                             "survive_%", "same_density_pairs"]]
    say(VC.to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    sd = PAIRS[PAIRS.same_density == 1]
    chg = PAIRS[(PAIRS.sign_PTS.notna()) & (PAIRS.sign_FRAC.notna())
                & (PAIRS.sign_PTS != PAIRS.sign_FRAC)]
    say(f"\n  {len(sd)} of {len(PAIRS)} published between-dial pairs ({100.0*len(sd)/len(PAIRS):.1f}%) "
        f"compare two dials swept at the SAME number of points; the other "
        f"{100.0*(1-len(sd)/len(PAIRS)):.1f}% compare dials whose grids differ.")
    say(f"  of the {len(chg)} pairs that change reading, {int((chg.same_density==1).sum())} are "
        f"same-density -- the arithmetic says this must be 0, and it is the control on the "
        f"whole count.")
    say("\n  UNITS is reported only where the file committed the window's dial-value edges; "
        "between-dial")
    say("  UNITS comparisons are recorded but are NOT well posed -- 4 percentage points of "
        "band and 4")
    say("  names of n are not the same width of anything -- and the disagreement rate below "
        "is a")
    say("  DEMONSTRATION of that, not a result about the record.")

    # C4  CLAIM level -- the per-dial MEDIAN that idea 401 actually published
    say("\n  CLAIM-LEVEL: idea 401's published per-dial median, in each unit")
    sh = shape.copy()
    sh["w_frac"] = sh.window_w / sh.sweep_pts
    med = sh.groupby("dial").agg(sweep_pts=("sweep_pts", "median"),
                                 med_w_pts=("window_w", "median"),
                                 med_w_frac=("w_frac", "median"),
                                 cells=("window_w", "size")).sort_values("med_w_pts", ascending=False)
    say(med.to_string(float_format=lambda x: f"{x:.4f}"))
    claim_rows = []
    for da, db in itertools.combinations(med.index, 2):
        claim_rows.append(dict(source="401-window-claim", cell="MEDIAN-over-12-cells",
                               dial_a=da, dial_b=db,
                               pts_a=med.loc[da, "sweep_pts"], pts_b=med.loc[db, "sweep_pts"],
                               w_pts_a=med.loc[da, "med_w_pts"], w_pts_b=med.loc[db, "med_w_pts"],
                               w_frac_a=med.loc[da, "med_w_frac"], w_frac_b=med.loc[db, "med_w_frac"],
                               w_units_a=np.nan, w_units_b=np.nan,
                               sign_PTS=sgn(med.loc[da, "med_w_pts"], med.loc[db, "med_w_pts"]),
                               sign_FRAC=sgn(med.loc[da, "med_w_frac"], med.loc[db, "med_w_frac"]),
                               sign_UNITS=np.nan,
                               same_density=int(med.loc[da, "sweep_pts"] == med.loc[db, "sweep_pts"])))
    CLM = pd.DataFrame(claim_rows)
    vc = verdict_table(CLM)
    say(f"\n  the {vc['n']} between-dial median comparisons idea 401 published: "
        f"agree {vc['agree']}, flip {vc['flip']}, tie broken {vc['tie_broken']}, "
        f"tie created {vc['tie_created']}  ->  {100.0*vc['agree']/max(vc['n'],1):.1f}% survive")
    for _, r in CLM.iterrows():
        mark = "OK  " if r.sign_PTS == r.sign_FRAC else "CHG "
        say(f"    {mark}{r.dial_a:>5s}({int(r.pts_a):2d}pts) vs {r.dial_b:>5s}({int(r.pts_b):2d}pts): "
            f"PTS {r.w_pts_a:5.2f} vs {r.w_pts_b:5.2f} -> {int(r.sign_PTS):+d};  "
            f"FRAC {r.w_frac_a:.3f} vs {r.w_frac_b:.3f} -> {int(r.sign_FRAC):+d}")
    PAIRS = pd.concat([PAIRS, CLM], ignore_index=True)
    PAIRS.to_csv(f"{OUT}.pairs.csv", index=False)

    # C5  CLAIMSET (tuned parameter 2) x STATISTIC (tuned parameter 1)
    say("\n  the two tuned parameters, crossed.  Rows = CLAIMSET, cols = the unit pair read:")
    sets = {"ALL": PAIRS,
            "WINDOW": PAIRS[PAIRS.source.str.contains("window")],
            "PLATEAU": PAIRS[PAIRS.source.str.contains("plateau")]}
    grid_rows = []
    for cs, g in sets.items():
        r = {"CLAIMSET": cs, "pairs": len(g)}
        for a, b in [("sign_PTS", "sign_FRAC"), ("sign_PTS", "sign_UNITS"), ("sign_FRAC", "sign_UNITS")]:
            v = verdict_table(g, a, b)
            r[f"{a[5:]}->{b[5:]}"] = f"{v['agree']}/{v['n']}" if v["n"] else "n/a"
        grid_rows.append(r)
    say(pd.DataFrame(grid_rows).to_string(index=False))

    # ------------------------------------------------------------- PART D  DENSITY (fresh grid)
    say("\n=== PART D  FRESH GRID: which unit is actually density-free? (spacing controlled here) ===")
    PX = load_panels()
    PAN = {k: Panel(v) for k, v in PX.items()}
    gate_g1(PAN["U56"]); gate_g2(PAN["U56"]); gate_g3()

    grid_rows, dens_rows = [], []
    for pname, P in PAN.items():
        S = P.spy
        base_r, base_t = fast_backtest(P.q, rules_v2_weights(P.q, 0.03, 0.75))
        B = legs(base_r - COST_BPS / 1e4 * base_t)
        for dial in DIALS:
            for res in RES:
                vals, step, exh = grid_for(dial, res)
                recs = []
                for c in vals:
                    r, t = fast_backtest(P.q, P.book(dial, c))
                    L = legs(r - COST_BPS / 1e4 * t)
                    mf, mi = m4b_full(L, S), m4b_is(L, S)
                    rec = dict(panel=pname, dial=dial, res=res, step=step, val=c,
                               CAGR=L["CAGR"], Sharpe=L["Sharpe"], MaxDD=L["MaxDD"],
                               H1=L["H1"], H2=L["H2"], OOS_Sharpe=L["OOS_Sharpe"],
                               OOS_CAGR=L["OOS_CAGR"], OOS_MaxDD=L["OOS_MaxDD"],
                               IS_Sharpe=L["IS_Sharpe"],
                               m_min=min(mf.values()), bind=min(mf, key=mf.get),
                               IS_m_min=min(mi.values()),
                               pass4b=int(min(mf.values()) >= 0), pass4a=pass4a(L, B),
                               turn_yr=float(t.iloc[WARMUP:].sum() / (len(t) - WARMUP) * 252))
                    rec.update({f"m_{k}": v for k, v in mf.items()})
                    recs.append(rec)
                G = pd.DataFrame(recs)
                grid_rows.append(G)
                smax = G.Sharpe.max()
                plat_flag = (G.Sharpe >= smax - PLATEAU_EPS).values
                p4b = (G.pass4b == 1).values
                is4b = (G.IS_m_min >= 0).values
                for fam, fl in [("4b_window", p4b), ("plateau", plat_flag), ("IS_4b_window", is4b)]:
                    k, u, lo, hi = widest_run(fl, G.val.values, step)
                    dens_rows.append(dict(panel=pname, dial=dial, res=res, family=fam,
                                          pts=len(vals), step=step, exhausted=int(exh),
                                          w_pts=k, w_frac=k / len(vals), w_units=u,
                                          lo=lo, hi=hi, n_pass=int(fl.sum())))
    GR = pd.concat(grid_rows, ignore_index=True)
    GR.to_csv(f"{OUT}.grid.csv", index=False)
    DN = pd.DataFrame(dens_rows)
    DN.to_csv(f"{OUT}.density.csv", index=False)
    say(f"  {len(GR)} fresh grid points committed across "
        f"{GR.panel.nunique()} panels x {GR.dial.nunique()} dials x {GR.res.nunique()} resolutions")

    say("\n  x4 / x1 ratio of each width statistic (a density-free unit reads 1.00):")
    rat = []
    for (pn, dl, fam), g in DN.groupby(["panel", "dial", "family"]):
        g = g.set_index("res")
        if not {"x1", "x4"} <= set(g.index):
            continue
        a, b = g.loc["x1"], g.loc["x4"]
        if a.w_pts == 0 and b.w_pts == 0:
            continue
        rat.append(dict(panel=pn, dial=dl, family=fam, exhausted=int(b.exhausted),
                        pts_x1=a.pts, pts_x4=b.pts, dens_ratio=b.pts / a.pts,
                        PTS=b.w_pts / a.w_pts if a.w_pts else np.inf,
                        FRAC=b.w_frac / a.w_frac if a.w_frac else np.inf,
                        UNITS=b.w_units / a.w_units if a.w_units else np.inf))
    RT = pd.DataFrame(rat)
    if len(RT):
        say(RT.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        fin = RT.replace([np.inf, -np.inf], np.nan)
        say("\n  median |ratio - 1| over the non-degenerate cells "
            "(0.000 = perfectly density-free):")
        for c in ["PTS", "FRAC", "UNITS"]:
            say(f"    {c:6s} {np.nanmedian((fin[c] - 1).abs()):.4f}   "
                f"(n={int(fin[c].notna().sum())})")
        say(f"    density itself moved x{np.nanmedian(fin.dens_ratio):.2f}")
    else:
        say("  no non-degenerate cell: every window is empty at both resolutions.")

    # -------------------------------------------------- PART E  RULE 8 + BOTH KEEP PATHS
    say("\n=== PART E  RULE 8 (choose on 2009-2016 only, evaluate 2017-2026 untouched) ===")
    say("  WITHIN one sweep the three units are ALGEBRAICALLY the same chooser: on a uniform")
    say("  grid the widest run in points, in share and in dial units is the same run, so no")
    say("  experiment there can separate them.  The unit can only bite where a width is")
    say("  compared ACROSS sweeps -- which is exactly the between-dial comparison PART C")
    say("  censused.  So the chooser here is given a MENU of sweeps and must pick one:")
    say("    1. take the widest IS-4b window on each sweep in the menu, measured in STATISTIC")
    say("    2. adopt the winning sweep's dial, held at that run's midpoint")
    say("    3. if no sweep in the menu has an IS window, ABSTAIN to RULES v2 (band .03,")
    say("       gross .75) -- abstention is a pick and is scored like every other one")
    say("  MENU is a corpus axis, not a third tuned parameter: X1 = the three dials at this")
    say("  file's published spacing; ALL = the same three dials at all three resolutions.")

    # per-sweep IS window, in all three units
    sw = []
    for (pn, dl, res), g in GR.groupby(["panel", "dial", "res"]):
        g = g.sort_values("val").reset_index(drop=True)
        step = float(g.step.iloc[0])
        k, u, lo, hi = widest_run((g.IS_m_min >= 0).values, g.val.values, step)
        sw.append(dict(panel=pn, dial=dl, res=res, pts=len(g), step=step,
                       IS_w_pts=k, IS_w_frac=k / len(g), IS_w_units=(0.0 if k == 0 else u),
                       # SPAN convention: a k-point run spans (k-1)*step, so a lone passing
                       # point has zero span.  COVER convention: the same run covers k*step,
                       # each point owning its own cell.  Both are defensible and they differ
                       # by exactly one step, so the COVER reading is carried alongside and
                       # the headline is reported under both -- see the sensitivity below.
                       IS_w_units_cover=k * step,
                       lo=lo, hi=hi))
    SW = pd.DataFrame(sw)
    SW.to_csv(f"{OUT}.sweeps.csv", index=False)
    say("\n  the menu, as the chooser sees it (IS 4b window per sweep, three units):")
    say(SW.sort_values(["panel", "dial", "res"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    STATCOL = {"PTS": "IS_w_pts", "FRAC": "IS_w_frac", "UNITS": "IS_w_units",
               "UNITS_COVER": "IS_w_units_cover"}
    wf = []
    for pn, Gp in GR.groupby("panel"):
        S = PAN[pn].spy
        base_r, base_t = fast_backtest(PAN[pn].q, rules_v2_weights(PAN[pn].q, 0.03, 0.75))
        B = legs(base_r - COST_BPS / 1e4 * base_t)
        for menu, resset in [("X1", ["x1"]), ("ALL", list(RES))]:
            M = SW[(SW.panel == pn) & (SW.res.isin(resset))]
            for stat in STATISTICS + ["UNITS_COVER"]:
                col = STATCOL[stat]
                if M[col].max() <= 0:
                    row = Gp[(Gp.dial == "band") & (Gp.res == "x1")].iloc[
                        (Gp[(Gp.dial == "band") & (Gp.res == "x1")].val - 0.03).abs().values.argmin()]
                    dl, res, how, pick = "band", "x1", "ABSTAIN(no IS window on the menu)", row.val
                else:
                    # deterministic tie-break: widest, then fewer points, then dial name
                    w = M.sort_values([col, "pts", "dial"], ascending=[False, True, True]).iloc[0]
                    dl, res = w.dial, w.res
                    g = Gp[(Gp.dial == dl) & (Gp.res == res)].sort_values("val")
                    inrun = g[(g.val >= w.lo) & (g.val <= w.hi)]
                    pick = float(inrun.val.median())
                    if DIALS[dl]["integer"]:
                        pick = float(int(round(pick)))
                    row = g.iloc[(g.val - pick).abs().values.argmin()]
                    how = f"widest IS window on the menu ({col})"
                wf.append(dict(panel=pn, MENU=menu, STATISTIC=stat, dial=dl, res=res,
                               pick=row.val, how=how,
                               IS_w_pts=float(M[M.dial.eq(dl) & M.res.eq(res)].IS_w_pts.iloc[0]) if how[0] == "w" else 0.0,
                               OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                               base_OOS_Sharpe=B["OOS_Sharpe"], base_OOS_CAGR=B["OOS_CAGR"],
                               base_OOS_MaxDD=B["OOS_MaxDD"],
                               spy_OOS_Sharpe=S["OOS_Sharpe"], spy_OOS_CAGR=S["OOS_CAGR"],
                               spy_OOS_MaxDD=S["OOS_MaxDD"],
                               d_base_Sharpe=row.OOS_Sharpe - B["OOS_Sharpe"],
                               d_spy_Sharpe=row.OOS_Sharpe - S["OOS_Sharpe"],
                               pass4a=row.pass4a, pass4b=row.pass4b,
                               full_CAGR=row.CAGR, full_Sharpe=row.Sharpe, full_MaxDD=row.MaxDD,
                               H1=row.H1, H2=row.H2))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("\n  does the UNIT change the rule-8 pick?  (same panel and menu, three units)")
    WF["choice"] = WF.dial + "@" + WF.res + "=" + WF.pick.round(4).astype(str)
    H = WF[WF.STATISTIC.isin(STATISTICS)]
    dis = H.pivot_table(index=["panel", "MENU"], columns="STATISTIC", values="choice",
                        aggfunc="first")
    ndis = int((dis.nunique(axis=1) > 1).sum())
    say(dis.to_string())
    say(f"\n    {ndis} of {len(dis)} (panel, menu) cells pick a DIFFERENT book depending on "
        f"the unit the width is read in")
    dis2 = WF.pivot_table(index=["panel", "MENU"], columns="STATISTIC", values="choice",
                          aggfunc="first")
    ndis2 = int((dis2[["PTS", "FRAC", "UNITS_COVER"]].nunique(axis=1) > 1).sum())
    say(f"    SENSITIVITY to the span-vs-cover convention: under COVER (a k-point run is "
        f"k*step wide,")
    say(f"    so a lone passing point is visible rather than zero-width) the count is "
        f"{ndis2} of {len(dis2)}.")
    say(f"    The UNITS column disagrees with PTS/FRAC in "
        f"{int((dis2.UNITS != dis2.PTS).sum())} cells under SPAN and "
        f"{int((dis2.UNITS_COVER != dis2.PTS).sum())} under COVER, so this particular "
        f"disagreement is a")
    say(f"    CONVENTION artefact, not a fact about the dials -- and that is itself the "
        f"finding: a")
    say(f"    between-dial width comparison in dial units has a free choice nobody declares.")

    say("\n  every rule-8 pick, OOS 2017-2026 vs the live baseline and vs SPY:")
    say(WF[["panel", "MENU", "STATISTIC", "dial", "res", "pick", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "base_OOS_Sharpe", "spy_OOS_Sharpe", "d_base_Sharpe", "d_spy_Sharpe",
            "pass4a", "pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  OOS by unit, pooled over every (panel, menu) cell (mean; baseline = RULES v2 live):")
    agg = WF.groupby("STATISTIC").agg(cells=("pick", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                                      OOS_CAGR=("OOS_CAGR", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                                      vs_base=("d_base_Sharpe", "mean"), vs_spy=("d_spy_Sharpe", "mean"),
                                      beats_base=("d_base_Sharpe", lambda s: int((s > 0).sum())),
                                      beats_spy=("d_spy_Sharpe", lambda s: int((s > 0).sum())),
                                      n_pass4b=("pass4b", "sum"), n_pass4a=("pass4a", "sum"))
    say(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    ref = WF.drop_duplicates("panel").set_index("panel")[
        ["base_OOS_Sharpe", "base_OOS_CAGR", "base_OOS_MaxDD",
         "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD"]]
    say("\n  the two reference books, OOS 2017-2026:")
    say(ref.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  BOTH KEEP PATHS over every fresh grid point (full sample, not just the picks):")
    kp = []
    for (pn, dl), g in GR.groupby(["panel", "dial"]):
        kp.append(dict(panel=pn, dial=dl, points=len(g),
                       n_4a=int(g.pass4a.sum()), n_4b=int(g.pass4b.sum()),
                       best_m_min=float(g.m_min.max()),
                       bind_at_best=g.loc[g.m_min.idxmax(), "bind"],
                       best_Sharpe=float(g.Sharpe.max())))
    KP = pd.DataFrame(kp)
    KP.to_csv(f"{OUT}.keeppaths.csv", index=False)
    say(KP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  4a passers: {int(KP.n_4a.sum())} / {len(GR)} grid points.  "
        f"4b passers: {int(KP.n_4b.sum())} / {len(GR)}.")

    # ------------------------------------------------------------------------ verdict
    say("\n" + "=" * 100)
    vall = verdict_table(PAIRS)
    vwin = verdict_table(sets["WINDOW"])
    vpl = verdict_table(sets["PLATEAU"])
    say(f"ANSWER  {vall['agree']} of {vall['n']} committed between-dial width comparisons "
        f"({100.0*vall['agree']/max(vall['n'],1):.1f}%) read the same way in width/points as in "
        f"points; {vall['flip']} flip outright and {vall['tie_broken']+vall['tie_created']} "
        f"gain or lose a tie.  WINDOW family {vwin['agree']}/{vwin['n']}, "
        f"PLATEAU family {vpl['agree']}/{vpl['n']}.")
    say(f"        The headline idea 401 actually published -- the 15 per-dial MEDIAN "
        f"comparisons -- survives {verdict_table(CLM)['agree']}/15.")
    n4b_pick = int(WF.pass4b.sum())
    say(f"KEEP    {'4b candidate among the rule-8 picks' if n4b_pick else 'none'}: "
        f"{n4b_pick} of {len(WF)} rule-8 picks pass 4b, {int(WF.pass4a.sum())} pass 4a; "
        f"{int(KP.n_4b.sum())}/{len(GR)} raw grid points pass 4b before rule 8. "
        f"No RULES change is proposed by this file either way -- it is a units audit, and "
        f"PROTOCOL 6 puts any rules change at the Sunday review.")
    say("=" * 100)

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(PAIRS=PAIRS, CEN=CEN, WF=WF, KP=KP, DN=DN, VC=VC, CLM=CLM, med=med)


if __name__ == "__main__":
    main()

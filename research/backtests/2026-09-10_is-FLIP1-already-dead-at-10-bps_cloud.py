#!/usr/bin/env python3
"""Idea 633 -- is FLIP1 already dead at 10 bps?

Idea 408R measured FLIP1 (a grid point whose 4b verdict differs from an adjacent point's
verdict on the same dial sweep) at 16.0% / 6.7% / 0.0% of 150 points across the 0 / 10 /
25 bps cost rungs, and concluded that the step column "does not earn its place at the
protocol rung".  The queue's reading is that every fragility statistic the record computes
-- THIN (margin/step), plateau width, 4b window width -- is measuring a phenomenon that
costs have already removed by 10 bps.

This run tests that reading and finds it is HALF right, in a way that reverses the
practical conclusion.  FLIP1 is a RATE OVER ALL POINTS, so it is bounded above by the 4b
PASS RATE: a sweep on which nothing passes cannot contain a flip.  Idea 408R's own
committed file shows the pass rate falling 20.7% -> 3.3% -> 0.0% over the same three rungs,
i.e. the denominator collapses at exactly the speed of the numerator.  The question this
file answers is therefore not "does FLIP1 fall?" (it must) but "conditional on a verdict
existing at all, are the record's 4b passes MORE or LESS marginal at the protocol rung?".

    PART A  CENSUS.  Every committed research/backtests/*.csv that publishes a 4b pass
            column and a swept dial: FLIP1 by cost rung, and the two rate-corrected
            statistics -- flips per PASSING point, and the observed/null ratio against a
            seeded random re-arrangement of the same verdicts on the same sweep.
    PART B  FRESH GRID.  Six dials x three panels x six cost rungs, every point committed.
            The rung is DERIVED (r(c) = r(0) - turnover * c/1e4) from one no-cost run per
            book, so the six rungs share an identical book by construction (gate G3).
    PART C  THE FRAGILITY CLAIMS.  Which committed files carry a THIN / plateau / window
            column, at which rung they computed it, and whether the claim survives being
            re-read at 10 bps inside its own file.
    PART D  RULE 8 (PROTOCOL 8) + both KEEP paths on every fresh grid point.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    RUNG        in {0, 5, 10, 15, 25, 50} bps
    GRID FAMILY in {band, gross, K, n, f, vol}   (idea 408's six adopted constants)
PANEL is a reported axis, not a tuned one: every statistic is reported for all three.

PROTOCOL-fixed: weights decided at close t, applied at t+1; long only, no leverage;
warm-up 260 rows dropped; halves at len(r)//2; rule 8 split 2016-12-31.  The headline rung
is 10 bps (PROTOCOL 2); the other five rungs are the tuned axis of this idea.

SURVIVORSHIP (PROTOCOL 9): B136 and SMALL439 are CURRENT constituent lists, so their
absolute CAGR/Sharpe levels are biased upward and none is a tradable estimate; SMALL439
additionally drops the 44 names with data/small_meta.csv max_1d_move >= 1.0.  Every claim
here is a within-panel contrast between cost rungs on identical books, which the bias
cannot move.

Run:  python3 research/backtests/2026-09-10_is-FLIP1-already-dead-at-10-bps_cloud.py
"""
import gzip, re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 250)
STEM = str(Path(__file__).with_suffix(""))
BT = ROOT / "research" / "backtests"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP, FREQ = 260, "W"
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]          # tuned axis 1
HEADLINE = 10.0
SEED = 633
_LOG = []


def log(s=""):
    print(s)
    _LOG.append(str(s))


# ---------------------------------------------------------------- vectorised engine
def fast_backtest(prices, weights, freq=FREQ):
    """Zero-cost returns and per-day turnover; identical to engine.backtest (gate G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            float(held.sum(axis=1)[WARMUP:].mean()))


# ================================================ the six adopted constants (idea 408's)
DIALS = {
    "band":  dict(c0=0.03, step=0.01, lo=0.00, hi=0.12, host="V2"),
    "gross": dict(c0=0.75, step=0.05, lo=0.30, hi=1.20, host="V2"),
    "K":     dict(c0=200,  step=25,   lo=50,   hi=350,  host="V2"),
    "n":     dict(c0=5,    step=4,    lo=1,    hi=29,   host="V1"),
    "f":     dict(c0=0.5,  step=0.1,  lo=0.0,  hi=1.0,  host="V1"),
    "vol":   dict(c0=0.60, step=0.05, lo=0.30, hi=0.90, host="V1"),
}


def grid_for(dial):
    d = DIALS[dial]; h = d["step"]
    if dial in ("K", "n"):
        h = int(h)
        g = list(range(int(d["c0"]), int(d["lo"]) - 1, -h))[::-1] + \
            list(range(int(d["c0"]) + h, int(d["hi"]) + 1, h))
        return sorted(set(g))
    lo, hi, c0 = d["lo"], d["hi"], d["c0"]
    nlo, nhi = int(round((c0 - lo) / h)), int(round((hi - c0) / h))
    return [round(c0 + i * h, 8) for i in range(-nlo, nhi + 1)]


class Panel:
    def __init__(self, px):
        self.px = px
        q = px.drop(columns=["SPY"])
        self.q = q
        mom = q.shift(21) / q.shift(252) - 1
        r6 = q / q.shift(126) - 1
        r3 = q / q.shift(63) - 1
        self.comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                     + r3.rank(axis=1, pct=True)) / 3
        self.vol20 = q.pct_change().rolling(20).std() * np.sqrt(252)
        self.notna = q.notna()
        self._ma, self._above, self._band = {}, {}, {}

    def ma(self, K):
        if K not in self._ma: self._ma[K] = self.q.rolling(int(K)).mean()
        return self._ma[K]

    def above(self, K):
        if K not in self._above: self._above[K] = self.q > self.ma(K)
        return self._above[K]

    def band_state(self, K, band):
        key = (int(K), round(float(band), 6))
        if key not in self._band:
            ma = self.ma(K)
            raw = pd.DataFrame(np.nan, index=self.q.index, columns=self.q.columns)
            raw = raw.mask(self.q > ma * (1 + band), 1.0).mask(self.q < ma * (1 - band), 0.0)
            self._band[key] = raw.ffill().fillna(0.0) > 0.5
        return self._band[key]

    def w_v2(self, band, gross, K):
        e = self.notna.astype(float)
        ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(self.band_state(K, band), 0.0)

    def w_v1(self, n, f, vol, K, w=0.15):
        s = self.comp * ((1.0 - f) + f * self.above(K).astype(float))
        s = s / self.vol20.clip(lower=0.08) ** 0.5
        elig = s.where(self.above(K) & (self.vol20 < vol))
        rank = elig.rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * w

    def book(self, dial, c):
        if DIALS[dial]["host"] == "V2":
            return self.w_v2(c if dial == "band" else DIALS["band"]["c0"],
                             c if dial == "gross" else DIALS["gross"]["c0"],
                             int(c) if dial == "K" else int(DIALS["K"]["c0"]))
        return self.w_v1(int(c) if dial == "n" else int(DIALS["n"]["c0"]),
                         c if dial == "f" else DIALS["f"]["c0"],
                         c if dial == "vol" else DIALS["vol"]["c0"],
                         int(c) if dial == "K" else int(DIALS["K"]["c0"]))


# ------------------------------------------------------------------ metric readings
def legs(r):
    r = r.iloc[WARMUP:]
    h = len(r) // 2
    f, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins, oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS=ins["Sharpe"], OOS=oos["Sharpe"],
                OOS_CAGR=oos["CAGR"], OOS_DD=oos["MaxDD"])


def margins_4b(L, S):
    """PROTOCOL 4b's five bars as SIGNED margins in their own units (>=0 passes)."""
    return dict(H1=L["H1"] - S["H1"], H2=L["H2"] - S["H2"], OOS=L["OOS"] - S["OOS"],
                DD=L["MaxDD"] - 0.60 * S["MaxDD"], CAGR=L["CAGR"] - 0.70 * S["CAGR"])


def v4a(L, B):
    return int(L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"])


# ======================================================= flip statistics (the whole idea)
def flip_flags(order_vals, verdicts):
    """FLIP1 exactly as idea 408R defines it: does either neighbour on the sorted sweep
    carry a different verdict."""
    v = list(verdicts)
    return [any(v[j] != v[i] for j in (i - 1, i + 1) if 0 <= j < len(v)) for i in range(len(v))]


def null_flip_rate(v):
    """EXACT expected FLIP1 rate if the SAME number of passes were re-arranged at random on
    the same sweep.  This is the denominator idea 408R's rate is missing: a sweep with 1
    pass in 25 points has a low flip rate however fragile that pass is.

    A point is NOT a flip iff every neighbour carries its own verdict.  Under a uniformly
    random arrangement of k passes in L slots the two endpoints have one neighbour each and
    the L-2 interior points have two, so
        E[flip rate] = 1 - [(L-2) * P3 + 2 * P2] / L
    with P3 = [k(k-1)(k-2) + m(m-1)(m-2)] / [L(L-1)(L-2)], P2 = [k(k-1) + m(m-1)]/[L(L-1)]
    and m = L - k.  Checked against a seeded Monte-Carlo in gate G4.
    """
    v = np.asarray(v, dtype=bool)
    L, k = len(v), int(v.sum())
    m = L - k
    if L < 3 or k == 0 or k == L:
        return 0.0
    p3 = (k * (k - 1) * (k - 2) + m * (m - 1) * (m - 2)) / (L * (L - 1) * (L - 2))
    p2 = (k * (k - 1) + m * (m - 1)) / (L * (L - 1))
    return 1.0 - ((L - 2) * p3 + 2 * p2) / L


def mc_flip_rate(v, rng, draws=20000):
    """Monte-Carlo version of null_flip_rate, used only by gate G4."""
    v = np.asarray(v, dtype=bool)
    L, k = len(v), int(v.sum())
    if L < 3 or k == 0 or k == L:
        return 0.0
    tot = 0
    for _ in range(draws):
        w = np.zeros(L, dtype=bool); w[rng.permutation(L)[:k]] = True
        d = w[1:] != w[:-1]
        f = np.zeros(L, dtype=bool); f[:-1] |= d; f[1:] |= d
        tot += f.sum()
    return tot / (draws * L)


def block_stats(vals, verdicts):
    """All the rate-corrected fragility statistics for one (sweep x rung) block."""
    o = np.argsort(np.asarray(vals, dtype=float))
    v = np.asarray(verdicts, dtype=bool)[o]
    L, k = len(v), int(v.sum())
    fl = flip_flags(np.asarray(vals, dtype=float)[o], v)
    nfl = int(np.sum(fl))
    nul = null_flip_rate(v)
    # widest contiguous run of passes (the record's "window width", in points)
    best = cur = 0
    for x in v:
        cur = cur + 1 if x else 0
        best = max(best, cur)
    return dict(n_pts=L, n_pass=k, pass_rate=k / L, n_flip=nfl, flip_rate=nfl / L,
                flips_per_pass=(nfl / k if k else np.nan),
                null_flip_rate=nul, flip_ratio=(nfl / L / nul if nul > 0 else np.nan),
                mixed=int(0 < k < L), window_pts=best,
                window_frac=best / L, isolated=int(k > 0 and best == 1))


# ==================================================================== GATES
def gate_g1(P):
    w = P.w_v2(0.03, 0.75, 200)
    fr, ft, _ = fast_backtest(P.q, w)
    eng = backtest(P.q, w, cost_bps=0.0, freq=FREQ)
    st = P.q.index[WARMUP]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt_ = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    log(f"G1  fast_backtest vs engine.backtest: max|dret| {dr:.3e}  max|dturn| {dt_:.3e}")
    assert dr < 1e-10 and dt_ < 1e-10, "G1 FAILED"


def gate_g2(P):
    d2 = float((P.w_v2(0.03, 0.75, 200) - rules_v2_weights(P.q, band=0.03, gross=0.75)).abs().max().max())
    d1 = float((P.w_v1(5, 0.5, 0.60, 200)
                - rules_v1_weights(P.q, n=5, w=0.15, max_vol=0.60, vol_scale=True)).abs().max().max())
    log(f"G2  host V2 vs baseline.rules_v2_weights {d2:.3e};  host V1 vs rules_v1_weights {d1:.3e}")
    assert d2 < 1e-12 and d1 < 1e-12, "G2 FAILED"


def gate_g3(P):
    """The derived cost rung must equal a re-run of engine.backtest at that rung, or the
    six rungs are not sharing one book."""
    w = P.w_v2(0.03, 0.75, 200)
    r0, t0, _ = fast_backtest(P.q, w)
    worst = 0.0
    for c in RUNGS:
        eng = backtest(P.q, w, cost_bps=c, freq=FREQ)["returns"]
        d = float(((r0 - t0 * c / 1e4) - eng).abs().max())
        worst = max(worst, d)
    log(f"G3  derived rung r(c) = r(0) - turn*c/1e4 vs engine.backtest at 6 rungs: max {worst:.3e}")
    assert worst < 1e-12, "G3 FAILED"


def gate_g4():
    """G4  the analytic random-arrangement null equals a seeded Monte-Carlo of the same
    thing, so the denominator this file adds is not itself an artefact."""
    rng = np.random.default_rng(SEED)
    worst = 0.0
    for L in (5, 9, 13, 19, 25):
        for k in range(0, L + 1):
            v = np.zeros(L, dtype=bool); v[:k] = True
            worst = max(worst, abs(null_flip_rate(v) - mc_flip_rate(v, rng, draws=4000)))
    log(f"G4  analytic null vs seeded Monte-Carlo over 5 sweep lengths x every pass count: "
        f"max |diff| {worst:.4f}")
    assert worst < 0.02, "G4 FAILED"


def gate_g0():
    """G0  reproduce idea 408R's published FLIP1 base rates from ITS OWN committed file
    before re-reading them.  16.0% / 6.7% / 0.0% at 0 / 10 / 25 bps, COARSE grid."""
    f = BT / "2026-09-10_publish-step_delta-beside-every-adopted-constant_B.cols.csv"
    d = pd.read_csv(f)
    hd = d[d.density == "COARSE"]
    got = {c: float(hd[hd.cost == c].FLIP1.mean()) for c in (0.0, 10.0, 25.0)}
    pub = {0.0: 0.160, 10.0: 0.067, 25.0: 0.000}
    log(f"G0  idea 408R committed FLIP1 (COARSE): "
        + "  ".join(f"{int(c)}bps {got[c]:.4f} (published {pub[c]:.3f})" for c in got))
    for c in got:
        assert abs(got[c] - pub[c]) < 0.001, "G0 FAILED"
    # and the denominator the published rate does not carry
    pr = {c: float(hd[hd.cost == c].pass4b.mean()) for c in (0.0, 10.0, 25.0)}
    log(f"G0b THE MISSING DENOMINATOR, from the same file: 4b PASS rate "
        + "  ".join(f"{int(c)}bps {pr[c]:.4f}" for c in pr)
        + f"   -> flips per PASSING point "
        + "  ".join(f"{int(c)}bps {(got[c]/pr[c] if pr[c] else float('nan')):.3f}" for c in pr))
    return got, pr


# ============================================================ PART A: the record census
PASS_COLS = ["pass4b", "p4b", "keep4b", "v4b", "pass_4b", "is4b", "IS4b", "KEEP4b", "four_b"]
COST_COLS = ["cost", "bps", "cost_bps", "rung", "cost_rung", "c_bps"]
METRIC_RE = re.compile(
    r"^(cagr|sharpe|maxdd|calmar|sortino|vol|turnover|gross|equity|total|years|winrate|"
    r"h1|h2|is|oos|oos_cagr|oos_dd|margin|m_[a-z0-9_]*|d[a-z]*sharpe|t_?stat|pval|p_value|"
    r"se|sd|mean|median|std|n|count|rows|seed|idx|index|auc|r2|rho|slope|intercept|"
    r"step|step_delta|steps|unit_step|thin.*|width.*|nobs|realised.*|real_.*|w|weight|"
    r"turn|ann_turn|.*_sharpe|.*_cagr|.*_dd|.*_maxdd|.*_ret|ret|rets|excess|lift|delta|"
    r"d_.*|drawdown|beta|alpha|corr|z|zscore|rank|score|pass.*|fail.*|flip.*|keep.*|v4a|pass4a)$",
    re.I)
FRAG_RE = re.compile(r"(thin|plateau|window|width|steps|step_delta|unit_step|flip)", re.I)
# names that ARE dials even though the metric blacklist would otherwise swallow them
# ("n" is deliberately NOT here: in this record it is a sample count far more often than the
#  holdings dial, so admitting it would hijack the block detection in files that are not sweeps.)
DIAL_NAMES = {"gross", "band", "k", "f", "vol", "q", "theta", "level", "val", "value",
              "c", "x", "param", "lam", "lambda", "tau", "phi", "quantile", "top_n", "nsel",
              "n_names", "ntop", "cap", "floor", "thresh", "threshold"}


def _read_csv(f, max_mb=40):
    try:
        if f.stat().st_size > max_mb * 1e6:
            return None
        if f.suffix == ".gz":
            with gzip.open(f, "rt") as fh:
                return pd.read_csv(fh, low_memory=False)
        return pd.read_csv(f, low_memory=False)
    except Exception:
        return None


def _pass_series(s):
    """A committed 4b column read as 0/1, or None if it is not a clean verdict flag."""
    if s.dtype == bool:
        return s.astype(int)
    if s.dtype == object:
        m = s.astype(str).str.strip().str.lower().map(
            {"true": 1, "false": 0, "1": 1, "0": 0, "1.0": 1, "0.0": 0,
             "yes": 1, "no": 0, "pass": 1, "fail": 0})
        return m.astype("Int64").astype(float) if m.notna().all() else None
    v = pd.to_numeric(s, errors="coerce")
    if v.isna().all():
        return None
    if set(np.unique(v.dropna().values)) - {0.0, 1.0}:
        return None
    return v.fillna(0)


def census():
    log("\n=== PART A  CENSUS: FLIP1 on every committed grid that publishes a 4b verdict ===")
    files = sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz")))
    rows, inv = [], []
    t0 = time.time()
    for f in files:
        d = _read_csv(f)
        if d is None or len(d) < 3 or len(d) > 200000:
            continue
        pc = next((c for c in d.columns if c in PASS_COLS), None)
        if pc is None:
            continue
        pv = _pass_series(d[pc])
        if pv is None:
            continue
        d = d.assign(_p=pv.astype(int))
        cc = next((c for c in d.columns if c in COST_COLS), None)
        num = [c for c in d.columns
               if c not in (pc, cc, "_p") and pd.api.types.is_numeric_dtype(d[c])
               and (str(c).lower() in DIAL_NAMES or not METRIC_RE.match(str(c)))
               and d[c].nunique(dropna=True) >= 3][:8]
        if not num:
            inv.append(dict(file=f.name, rows=len(d), pass_col=pc, cost_col=cc or "",
                            dial_col="", reason="no dial candidate"))
            continue
        skey = d.astype(str)
        best = None
        for dcol in num:
            keys = [c for c in d.columns
                    if c not in (dcol, pc, "_p")
                    and (not pd.api.types.is_numeric_dtype(d[c]) or c in num or c == cc)
                    and d[c].nunique(dropna=True) <= max(40, len(d) // 3)]
            g = [((), d)] if not keys else list(d.groupby([skey[k] for k in keys], dropna=False))
            blocks = [(k, b) for k, b in g if len(b) >= 3 and b[dcol].nunique() == len(b)]
            usable = sum(len(b) for _, b in blocks)
            if best is None or usable > best[0]:
                best = (usable, dcol, keys, blocks)
        usable, dcol, keys, blocks = best
        if usable < 3:
            inv.append(dict(file=f.name, rows=len(d), pass_col=pc, cost_col=cc or "",
                            dial_col=dcol, reason="no block with 3 distinct dial values"))
            continue
        inv.append(dict(file=f.name, rows=len(d), pass_col=pc, cost_col=cc or "",
                        dial_col=dcol, reason=f"OK ({len(blocks)} blocks, {usable} rows)"))
        for k, b in blocks:
            rung = np.nan
            if cc is not None:
                u = pd.to_numeric(b[cc], errors="coerce").dropna().unique()
                if len(u) == 1:
                    rung = float(u[0])
            st = block_stats(b[dcol].values, b["_p"].values)
            st.update(file=f.name, dial_col=dcol, rung=rung,
                      block=str(k)[:120], pass_col=pc, cost_col=cc or "")
            rows.append(st)
    C = pd.DataFrame(rows)
    pd.DataFrame(inv).to_csv(f"{STEM}.inventory.csv", index=False)
    C.to_csv(f"{STEM}.census.csv", index=False)
    log(f"  scanned {len(files)} committed CSVs in {time.time()-t0:.0f}s; "
        f"{sum(1 for i in inv if i['reason'].startswith('OK'))} carry a usable sweep; "
        f"{len(C)} (sweep x block) blocks, {int(C.n_pts.sum())} grid points.")

    def summarise(sub, label):
        if len(sub) == 0:
            log(f"    {label:22s} n_blocks=0"); return
        pts = sub.n_pts.sum(); fl = sub.n_flip.sum(); ps = sub.n_pass.sum()
        mixed = sub.mixed.sum()
        iso = sub[sub.n_pass > 0].isolated.mean() if (sub.n_pass > 0).any() else np.nan
        log(f"    {label:22s} blocks {len(sub):5d}  pts {int(pts):6d}  "
            f"4b pass rate {ps/pts:6.2%}  FLIP1 {fl/pts:6.2%}  "
            f"flips/pass {(fl/ps if ps else np.nan):6.3f}  "
            f"mixed blocks {mixed/len(sub):6.2%}  isolated-pass blocks {iso:6.2%}")

    log("\n  A1  by cost rung as published (blocks whose file states one rung for the block)")
    for r in sorted(C.rung.dropna().unique()):
        if (C.rung == r).sum() >= 5:
            summarise(C[C.rung == r], f"{r:g} bps")
    summarise(C[C.rung.isna()], "rung UNSTATED")
    log("\n  A2  everything pooled")
    summarise(C, "ALL blocks")
    rr = C.dropna(subset=["rung"])
    if len(rr) > 20:
        g = rr.groupby("rung").apply(
            lambda s: pd.Series(dict(pts=s.n_pts.sum(), pas=s.n_pass.sum(), fl=s.n_flip.sum())),
            include_groups=False)
        g["pass_rate"] = g.pas / g.pts; g["flip_rate"] = g.fl / g.pts
        g["flips_per_pass"] = g.fl / g.pas.replace(0, np.nan)
        gg = g[g.pts >= 50]
        if len(gg) >= 3:
            log("\n  A3  rank correlation across published rungs (Spearman over rungs with >=50 pts)")
            for col in ("pass_rate", "flip_rate", "flips_per_pass"):
                x = gg.index.values.astype(float); y = gg[col].values.astype(float)
                ok = ~np.isnan(y)
                if ok.sum() >= 3:
                    rho = float(pd.Series(x[ok]).rank().corr(pd.Series(y[ok]).rank()))
                    log(f"      rho(rung, {col:15s}) = {rho:+.3f}   values "
                        + " ".join(f"{v:.3f}" for v in y[ok]))
        g.to_csv(f"{STEM}.census_by_rung.csv")
    return C


def fragility_claims(C):
    """PART C.  Which committed files publish a fragility column, at what rung."""
    log("\n=== PART C  the record's FRAGILITY COLUMNS: at which rung were they computed? ===")
    files = sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz")))
    rows = []
    for f in files:
        try:
            if f.suffix == ".gz":
                with gzip.open(f, "rt") as fh: hdr = fh.readline().strip().split(",")
            else:
                with open(f) as fh: hdr = fh.readline().strip().split(",")
        except Exception:
            continue
        frag = [c for c in hdr if FRAG_RE.search(c)]
        if not frag:
            continue
        cc = next((c for c in hdr if c in COST_COLS), None)
        rungs = ""
        if cc:
            d = _read_csv(f)
            if d is not None and cc in d.columns:
                u = sorted(pd.to_numeric(d[cc], errors="coerce").dropna().unique())
                rungs = ";".join(f"{v:g}" for v in u[:8])
        rows.append(dict(file=f.name, frag_cols=";".join(frag[:6]), n_frag=len(frag),
                         cost_col=cc or "", rungs=rungs,
                         has_0=("0" in rungs.split(";")), has_10=("10" in rungs.split(";")),
                         states_rung=bool(rungs)))
    F = pd.DataFrame(rows)
    F.to_csv(f"{STEM}.fragility_files.csv", index=False)
    if len(F) == 0:
        log("  no fragility columns found."); return F
    log(f"  {len(F)} committed CSVs publish at least one fragility-family column "
        f"(thin/plateau/window/width/step/flip).")
    log(f"    of these, {int(F.states_rung.sum())} state a cost rung in the file at all "
        f"({F.states_rung.mean():.1%}); {int(F.has_0.sum())} contain 0-bps rows; "
        f"{int(F.has_10.sum())} contain 10-bps rows.")
    both = F[F.has_0 & F.has_10]
    log(f"    {len(both)} carry BOTH 0 and 10 bps and can be re-read inside their own file.")
    return F


# ==================================================== PARTS B / D: the fresh grid
def fresh_grid(panels):
    log("\n=== PART B  FRESH GRID: 6 dials x 3 panels x 6 derived cost rungs ===")
    rows = []
    spy_cache, base_cache = {}, {}
    for pk, P in panels.items():
        spy = P.px["SPY"].pct_change().fillna(0.0)
        spy_cache[pk] = legs(spy)
        wb = P.w_v2(0.03, 0.75, 200)
        rb, tb, gb = fast_backtest(P.q, wb)
        base_cache[pk] = {c: legs(rb - tb * c / 1e4) for c in RUNGS}
        for dial in DIALS:
            for c in grid_for(dial):
                w = P.book(dial, c)
                r0, t0, gross = fast_backtest(P.q, w)
                ann_turn = float(t0.iloc[WARMUP:].sum() / (len(t0.iloc[WARMUP:]) / 252))
                for rung in RUNGS:
                    L = legs(r0 - t0 * rung / 1e4)
                    S, B = spy_cache[pk], base_cache[pk][rung]
                    m = margins_4b(L, S)
                    p4b = int(all(v >= 0 for v in m.values()))
                    rows.append(dict(panel=pk, dial=dial, val=c, rung=rung,
                                     pass4b=p4b, pass4a=v4a(L, B),
                                     m_bind=min(m, key=m.get), m_min=min(m.values()),
                                     gross=gross, ann_turn=ann_turn,
                                     **{f"m_{k}": v for k, v in m.items()}, **L))
    G = pd.DataFrame(rows)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    log(f"  {len(G)} grid rows committed ({G.groupby(['panel','dial']).ngroups} sweeps x {len(RUNGS)} rungs).")

    # ---- flip statistics per (panel, dial, rung)
    brows = []
    for (pk, dial, rung), b in G.groupby(["panel", "dial", "rung"]):
        st = block_stats(b.val.values, b.pass4b.values)
        st.update(panel=pk, dial=dial, rung=rung, kind="4b")
        brows.append(st)
        st2 = block_stats(b.val.values, b.pass4a.values)
        st2.update(panel=pk, dial=dial, rung=rung, kind="4a")
        brows.append(st2)
    Bk = pd.DataFrame(brows)
    Bk.to_csv(f"{STEM}.blocks.csv", index=False)

    log("\n  B1  the queue's statistic and its missing denominator, by rung (4b, 18 sweeps/rung)")
    log(f"    {'rung':>6} {'pts':>5} {'4b pass':>8} {'FLIP1':>8} {'flips/pass':>11} "
        f"{'null FLIP1':>11} {'obs/null':>9} {'mixed':>7} {'window pts':>11}")
    for rung in RUNGS:
        s = Bk[(Bk.kind == "4b") & (Bk.rung == rung)]
        pts, ps, fl = s.n_pts.sum(), s.n_pass.sum(), s.n_flip.sum()
        nul = float((s.null_flip_rate * s.n_pts).sum() / pts)
        wmix = s[s.n_pass > 0]
        log(f"    {rung:6.0f} {int(pts):5d} {ps/pts:8.2%} {fl/pts:8.2%} "
            f"{(fl/ps if ps else np.nan):11.3f} {nul:11.2%} "
            f"{(fl/pts/nul if nul>0 else np.nan):9.3f} {s.mixed.mean():7.2%} "
            f"{(wmix.window_pts.mean() if len(wmix) else np.nan):11.2f}")

    log("\n  B2  the same, per panel (4b pass rate / FLIP1 / flips per pass)")
    for pk in panels:
        parts = []
        for rung in RUNGS:
            s = Bk[(Bk.kind == "4b") & (Bk.rung == rung) & (Bk.panel == pk)]
            pts, ps, fl = s.n_pts.sum(), s.n_pass.sum(), s.n_flip.sum()
            parts.append(f"{rung:g}bps {ps/pts:.1%}/{fl/pts:.1%}/"
                         f"{(fl/ps if ps else float('nan')):.2f}")
        log(f"    {pk:9s} " + "  ".join(parts))

    log("\n  B3  per dial family (the second tuned axis), pooled over panels")
    for dial in DIALS:
        parts = []
        for rung in RUNGS:
            s = Bk[(Bk.kind == "4b") & (Bk.rung == rung) & (Bk.dial == dial)]
            pts, ps, fl = s.n_pts.sum(), s.n_pass.sum(), s.n_flip.sum()
            parts.append(f"{rung:g} {ps/pts:.0%}/{fl/pts:.0%}")
        log(f"    {dial:6s} pass/FLIP1 by rung:  " + "  ".join(parts))

    log("\n  B4  4a (against the LIVE RULES v2 book) for the same sweeps")
    for rung in RUNGS:
        s = Bk[(Bk.kind == "4a") & (Bk.rung == rung)]
        pts, ps, fl = s.n_pts.sum(), s.n_pass.sum(), s.n_flip.sum()
        log(f"    {rung:5.0f} bps  4a pass {ps/pts:6.2%}  FLIP1 {fl/pts:6.2%}  "
            f"flips/pass {(fl/ps if ps else np.nan):6.3f}")
    return G, Bk, base_cache, spy_cache


def rule8(panels, G, base_cache, spy_cache):
    """PART D.  PROTOCOL 8: choose the dial value on 2008-2016 only, read 2017-2026 once.
    The idea under test is whether a FRAGILITY SCREEN (refuse a point that is FLIP1 at the
    chooser's own rung) improves the pick -- that is what the record's fragility columns
    are for, if they are for anything."""
    log("\n=== PART D  RULE 8 (choose on IS 2008-2016, OOS 2017-2026 read once) ===")
    picks = []
    for (pk, dial, rung), b in G.groupby(["panel", "dial", "rung"]):
        b = b.sort_values("val").reset_index(drop=True)
        # IS-side flip flags: verdicts computed on the IS window alone would need an IS 4b;
        # the record's own screen is the FULL-SAMPLE FLIP1 column, so both are reported.
        fl = flip_flags(b.val.values, b.pass4b.values)
        for screen, sel in (("NONE", b),
                            ("NO-FLIP1", b[[not x for x in fl]] if any(fl) else b)):
            if len(sel) == 0:
                sel = b
            i = int(sel.IS.astype(float).idxmax())
            r = b.loc[i] if i in b.index else sel.loc[i]
            picks.append(dict(panel=pk, dial=dial, rung=rung, screen=screen, val=r.val,
                              IS=r.IS, OOS=r.OOS, OOS_CAGR=r.OOS_CAGR, OOS_DD=r.OOS_DD,
                              CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                              pass4b=int(r.pass4b), pass4a=int(r.pass4a)))
    Pk = pd.DataFrame(picks)
    Pk.to_csv(f"{STEM}.wf.csv", index=False)
    log(f"  {len(Pk)} picks ({Pk.groupby(['panel','dial','rung']).ngroups} cells x 2 screens).")

    log("\n  D1  does the record's fragility screen change the walk-forward pick?")
    for rung in RUNGS:
        a = Pk[(Pk.rung == rung) & (Pk.screen == "NONE")].set_index(["panel", "dial"])
        c = Pk[(Pk.rung == rung) & (Pk.screen == "NO-FLIP1")].set_index(["panel", "dial"])
        diff = (a.val != c.reindex(a.index).val).sum()
        log(f"    {rung:5.0f} bps  screen changes the pick in {diff:2d} of {len(a)} cells; "
            f"mean OOS Sharpe NONE {a.OOS.mean():.4f}  NO-FLIP1 {c.OOS.mean():.4f}  "
            f"delta {c.OOS.mean()-a.OOS.mean():+.4f}")

    log("\n  D2  the headline rung (10 bps): every pick against its own panel's comparands")
    log(f"    {'panel':9s} {'dial':6s} {'screen':9s} {'val':>7} {'OOS Sh':>8} {'OOS CAGR':>9} "
        f"{'OOS DD':>8} | {'v2 OOS':>7} {'SPY OOS':>8}")
    for _, r in Pk[Pk.rung == HEADLINE].sort_values(["panel", "dial", "screen"]).iterrows():
        B = base_cache[r.panel][HEADLINE]; S = spy_cache[r.panel]
        log(f"    {r.panel:9s} {r.dial:6s} {r.screen:9s} {r.val:7g} {r.OOS:8.4f} "
            f"{r.OOS_CAGR:9.2%} {r.OOS_DD:8.2%} | {B['OOS']:7.4f} {S['OOS']:8.4f}")
    log("\n    comparands (OOS 2017-2026, 10 bps):")
    for pk in base_cache:
        B, S = base_cache[pk][HEADLINE], spy_cache[pk]
        log(f"      {pk:9s} RULES v2  {B['OOS_CAGR']:7.2%} / {B['OOS']:.4f} / {B['OOS_DD']:7.2%}"
            f"   SPY  {S['OOS_CAGR']:7.2%} / {S['OOS']:.4f} / {S['OOS_DD']:7.2%}")
    return Pk


def keep_paths(G, base_cache, spy_cache):
    log("\n=== BOTH KEEP PATHS on every fresh grid point (PROTOCOL 4) ===")
    for rung in RUNGS:
        s = G[G.rung == rung]
        log(f"    {rung:5.0f} bps  4b {int(s.pass4b.sum()):4d}/{len(s)}   "
            f"4a {int(s.pass4a.sum()):3d}/{len(s)}   BOTH {int((s.pass4b & s.pass4a).sum()):3d}")
    h = G[G.rung == HEADLINE]
    if h.pass4b.sum():
        log("\n  the 4b passers at the headline rung (all reported):")
        cols = ["panel", "dial", "val", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS",
                "m_bind", "m_min", "gross"]
        log(h[h.pass4b == 1][cols].to_string(index=False,
            float_format=lambda x: f"{x:.4f}"))
    else:
        log("  no point passes 4b at the headline rung.")
    fails = h[h.pass4b == 0]
    if len(fails):
        log("\n  binding 4b bar over the headline-rung failures: "
            + ", ".join(f"{k} {v}" for k, v in fails.m_bind.value_counts().items()))


# ============================================================================== main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 633  is-FLIP1-already-dead-at-10-bps   (cloud, 2026-09-10)")
    log("=" * 100)
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px["SMALL439"] = sm.drop(columns=[c for c in sm.columns if c in bad])
    log(f"panels: " + "  ".join(f"{k} {v.shape[1]-1} names x {len(v)} rows "
                                f"[{v.index[0].date()}..{v.index[-1].date()}]"
                                for k, v in px.items()))
    panels = {k: Panel(v) for k, v in px.items()}

    log("\n=== GATES ===")
    gate_g0()
    gate_g1(panels["U56"])
    gate_g2(panels["U56"])
    gate_g3(panels["U56"])
    gate_g4()

    C = census()
    G, Bk, base_cache, spy_cache = fresh_grid(panels)
    F = fragility_claims(C)
    Pk = rule8(panels, G, base_cache, spy_cache)
    keep_paths(G, base_cache, spy_cache)
    log(f"\ndone in {time.time()-t0:.0f}s")
    Path(f"{STEM}.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

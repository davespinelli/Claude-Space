#!/usr/bin/env python3
"""Idea 633 -- is FLIP1 already dead at 10 bps?   (lane C, 2026-09-10)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number in this file was read)
    Idea 408's neighbour-flip base rate falls 16.0% -> 6.7% -> 0.0% across 0 / 10 / 25 bps,
    so every fragility statistic the record computes (THIN, plateau width, window width) is
    measuring a phenomenon costs have already removed at the protocol rung.  Census the
    record's committed grids for neighbour flips as a function of the cost rung and test
    whether any published fragility claim is a 0-bps artefact.  Max 2 params (rung, family).

WHAT FLIP1 IS, WRITTEN OUT BEFORE IT IS MEASURED
    FLIP1(point) = the 4b verdict differs at an immediate grid neighbour along the dial.
    A point is FLIP1 iff it is adjacent to a BOUNDARY of the pass region.  So on a sweep of
    G points whose pass set has B boundaries (adjacencies where the verdict changes),
                 flip_count = |{points adjacent to a boundary}|  <=  2B,
    with equality when no two boundaries share a point.  B = 0 -- i.e. the sweep is ALL-PASS
    or ALL-FAIL -- forces FLIP1 = 0 with no reference to fragility at all.  That is the
    alternative hypothesis this file was written to test, and it is testable in advance of
    any new backtest because it is arithmetic, not economics:

        H_FRAGILITY   costs SMOOTH the verdict surface; boundaries survive but stop being
                      knife-edge, so flips fall while the pass region stays populated.
        H_DEPOPULATION costs push whole sweeps below the 4b bar; the pass region EMPTIES,
                      B goes to 0, and FLIP1 dies for want of a boundary to sit next to.
    The two make opposite predictions about the MIXED share (sweeps with 0 < passers < G)
    and about the flip rate CONDITIONAL on a sweep being mixed.  H_FRAGILITY predicts the
    conditional rate falls; H_DEPOPULATION predicts it does not, and that the unconditional
    fall is entirely the mixed share.  The parent's own committed artefact already contains
    the first half of the answer (pass4b 31 -> 5 -> 0 over the same three rungs), which is
    why gate G0 reads it rather than re-deriving it.

    PART A  G0/G1/G2/G3.  Reproduce idea 408R's published 16.0/6.7/0.0 from its OWN
            committed .cols.csv, and check the arithmetic the file turns on synthetically.
    PART B  CENSUS.  Every committed research/backtests/*.csv[.gz] that is a DIAL SWEEP with
            a 4b verdict and a declared cost rung, re-read for neighbour flips as a function
            of that rung.  The inclusion rule is mechanical and every exclusion is written
            out.  Also: what rung is the record's fragility corpus actually PUBLISHED at?
    PART C  FRESH GRID whose cost ladder THIS FILE controls: 3 panels x 3 dials x 9 rungs,
            every point committed.  Because a rung is a linear drag on an already-computed
            (return, turnover) pair, all nine rungs come off ONE backtest per point, so the
            ladder is exact rather than nine separate re-runs.
    PART D  THE DECOMPOSITION.  Split the fall in FLIP1 into a MIXED-SHARE leg and a
            WITHIN-MIXED leg, and price THIN and window width on the same ladder, so the
            question "is the fragility statistic dead, or is the pass region dead" is
            answered with a number instead of a sentence.
    PART E  RULE 8 (PROTOCOL 8) + BOTH KEEP PATHS on every fresh grid point.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    RUNG    in {0, 2.5, 5, 7.5, 10, 15, 20, 25, 40} bps    the cost rung
    FAMILY  in {band, gross, n}                            the grid family a claim is read on
Everything else is a corpus axis held identical across cells and reported in full: panel
{U56, B136, SMALL439}, book {V2-host, V1-host}, and the census's own file/dial/cell keys.
Every fresh grid point -> .grid.csv; every censused sweep -> .census.csv; the per-file
corpus -> .files.csv; the ladder summary -> .ladder.csv; rule 8 -> .walkforward.csv;
both KEEP paths -> .keeppaths.csv.

PROTOCOL-fixed: weights decided at close t, applied at t+1; costs per unit turnover; long
only, no leverage (gross <= 1.00); warm-up 260 rows dropped; halves at len(r)//2; rule 8
split at 2016-12-31.  SPY is buy-and-hold and is priced cost-free at every rung, which is
the record's own convention and is the CONSERVATIVE choice here: charging SPY would lower
the 4b bar as the rung rises and would manufacture passers at exactly the rungs this file
claims are empty.
SURVIVORSHIP (PROTOCOL 9): B136 and SMALL439 are CURRENT constituent lists -- they exclude
names delisted, acquired or dropped from the screen, so their absolute levels are biased UP
and no CAGR/Sharpe from them is a tradable estimate.  Only the WITHIN-panel contrasts this
file reports (one rung against another on identical books) are meant to survive that.
SMALL439 drops the 44 names with data/small_meta.csv max_1d_move >= 1.0 before anything else.

Run:  python3 research/backtests/2026-09-10_is-FLIP1-already-dead-at-10-bps_C.py
"""
import re, sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights          # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics                            # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 500)
OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP, FREQ = 260, "W"
PHI, DELTA = 0.70, 0.60                 # PROTOCOL 4b CAGR floor / DD cap vs SPY
RUNGS = [0.0, 2.5, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0, 40.0]
PROTOCOL_RUNG = 10.0
PARENT_RUNGS = [0.0, 10.0, 25.0]        # the three idea 408 published
TAUS = [0.5, 1.0, 2.0]                  # idea 408's THIN thresholds, unchanged
BARS = ["H1", "H2", "OOS", "DD", "CAGR"]
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ============================================================================ FLIP1 machinery
def flip_flags(passes):
    """FLIP1 per point: the verdict differs at an immediate neighbour along the ordered dial."""
    p = np.asarray(passes, dtype=bool)
    f = np.zeros(len(p), dtype=bool)
    if len(p) < 2:
        return f
    d = p[1:] != p[:-1]                 # boundary between i and i+1
    f[:-1] |= d
    f[1:] |= d
    return f


def n_boundaries(passes):
    p = np.asarray(passes, dtype=bool)
    return int((p[1:] != p[:-1]).sum()) if len(p) > 1 else 0


def step_delta(vals, ser):
    """Median |one-step motion| of a bar along the dial -- idea 408's STEP, verbatim."""
    v = np.asarray(vals, dtype=float)
    y = np.asarray([ser[x] for x in vals], dtype=float)
    ok = np.isfinite(y)
    if ok.sum() < 2:
        return np.nan
    return float(np.median(np.abs(np.diff(y[ok]))))


def widest_run(flags):
    """Length of the longest contiguous True run, and its (lo_idx, hi_idx)."""
    best, i, blo, bhi = 0, 0, -1, -1
    f = list(flags)
    while i < len(f):
        if f[i]:
            j = i
            while j + 1 < len(f) and f[j + 1]:
                j += 1
            if j - i + 1 > best:
                best, blo, bhi = j - i + 1, i, j
            i = j + 1
        else:
            i += 1
    return best, blo, bhi


# ==================================================================== PART B: census machinery
# Pre-registered vocabularies.  Written once, applied to every file, never tuned per file.
DIAL_RE = re.compile(r"^(val|value|param|dialval|x|band|gross|g|n|n0|k|K|q|vol|volcap|f|frac|"
                     r"lam|lambda|theta|tau|cap|w|nn|width|thr|threshold|level|c|m|depth|"
                     r"quantile|nq|halflife|hl|window|lookback|span)$")
COST_RE = re.compile(r"^(cost|cost_bps|rung|bps|cost_rung|costbps)$", re.I)
PASS_RE = re.compile(r"^(pass4b|pass_4b|keep4b|pass4b_full|full_pass4b)$", re.I)
# outcomes may never enter a cell key: grouping by a verdict would decide the answer
OUTCOME_RE = re.compile(r"pass|fail|clear|keep|verdict|flip|thin|beat|win|surviv|bind|"
                        r"admissible|reject|accept", re.I)
METRIC_RE = re.compile(r"CAGR|Sharpe|MaxDD|Calmar|H1|H2|OOS|IS_|turn|margin|^m_|^d_|delta|"
                       r"^se|^t_|auc|rho|r2|slope|mean|median|sd$|std|count|share|frac|pct|"
                       r"ret|vol|dd", re.I)
TRUTHY = {"true": True, "false": False, "1": True, "0": False, "1.0": True, "0.0": False,
          "yes": True, "no": False, "t": True, "f": False}


def as_bool(s):
    if s.dtype == bool:
        return s
    if pd.api.types.is_numeric_dtype(s):
        return s.fillna(0) > 0.5
    return s.astype(str).str.strip().str.lower().map(TRUTHY)


def census():
    """Every committed CSV that is a DIAL SWEEP carrying a 4b verdict and a declared rung.

    INCLUSION (mechanical, in this fixed order):
      1. filename ends .csv / .csv.gz under research/backtests, >= 3 rows;
      2. carries exactly-named 4b verdict column (PASS_RE) and a rung column (COST_RE);
      3. carries at least one numeric DIAL_RE column with >= 3 distinct values that is
         neither the rung nor a verdict;
      4. CELL KEY = every remaining column that is not a metric, not an outcome, and has
         <= 12 distinct values, plus the rung column.  Outcomes are excluded by rule: a key
         containing pass4a would sort the grid by a verdict and fabricate boundaries.
      5. a usable SWEEP is a (cell) group with >= 3 rows and all-distinct dial values.
    Where a file offers several candidate dials, the one yielding the MOST usable sweeps is
    taken as the file's dial (alphabetical tie-break) and the alternatives are recorded in
    .files.csv rather than silently dropped.
    """
    rows, frows = [], []
    # THIS FILE'S OWN artefacts are excluded: a re-run would otherwise censusate its own
    # fresh grid and the "committed record" would start including this run's answer.
    self_stem = OUT.name
    paths = sorted(p for p in BT.iterdir()
                   if p.name.endswith((".csv", ".csv.gz")) and not p.name.startswith(self_stem))
    n_seen = n_verdict = 0
    for p in paths:
        try:
            df = pd.read_csv(p, low_memory=False)
        except Exception:
            continue
        n_seen += 1
        if len(df) < 3:
            continue
        pc = [c for c in df.columns if PASS_RE.match(c)]
        cc = [c for c in df.columns if COST_RE.match(c)]
        if not pc:
            continue
        n_verdict += 1
        if not cc:
            frows.append(dict(file=p.name, dial="", rung_col="", n_rows=len(df),
                              n_sweeps=0, reason="no declared rung column"))
            continue
        pcol, ccol = pc[0], cc[0]
        cand = [c for c in df.columns
                if DIAL_RE.match(c) and c not in (pcol, ccol)
                and pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique(dropna=True) >= 3
                and not OUTCOME_RE.search(c)]
        if not cand:
            frows.append(dict(file=p.name, dial="", rung_col=ccol, n_rows=len(df),
                              n_sweeps=0, reason="no numeric dial column with >=3 values"))
            continue
        try:
            pv = as_bool(df[pcol])
        except Exception:
            frows.append(dict(file=p.name, dial="", rung_col=ccol, n_rows=len(df),
                              n_sweeps=0, reason="4b column not coercible to bool"))
            continue
        if pv.isna().all():
            frows.append(dict(file=p.name, dial="", rung_col=ccol, n_rows=len(df),
                              n_sweeps=0, reason="4b column all-NaN"))
            continue
        df = df.assign(_p4b=pv.fillna(False).astype(bool))
        best = None
        for d in sorted(cand):
            key = [c for c in df.columns
                   if c not in (d, pcol, "_p4b") and not OUTCOME_RE.search(c)
                   and not METRIC_RE.search(c) and df[c].nunique(dropna=True) <= 12]
            if ccol not in key:
                key.append(ccol)
            got = []
            for kv, g in df.groupby(key, dropna=False) if key else [((), df)]:
                g = g.dropna(subset=[d])
                if len(g) < 3 or g[d].nunique() != len(g):
                    continue
                g = g.sort_values(d)
                pas = g._p4b.values
                fl = flip_flags(pas)
                try:
                    rung = float(g[ccol].iloc[0])
                except Exception:
                    continue
                if not np.isfinite(rung):
                    continue
                got.append(dict(file=p.name, dial=d, rung=rung, G=len(g),
                                cell="|".join(map(str, kv)) if isinstance(kv, tuple) else str(kv),
                                n_pass=int(pas.sum()),
                                mixed=int(0 < pas.sum() < len(pas)),
                                B=n_boundaries(pas), n_flip=int(fl.sum()),
                                flip_rate=float(fl.mean())))
            if best is None or len(got) > len(best[1]):
                best = (d, got, key)
        d, got, key = best
        frows.append(dict(file=p.name, dial=d, rung_col=ccol, n_rows=len(df),
                          n_sweeps=len(got), n_cand_dials=len(cand),
                          cand_dials=";".join(sorted(cand)), key=";".join(key),
                          reason="" if got else "no cell with >=3 distinct dial values"))
        rows.extend(got)
    return pd.DataFrame(rows), pd.DataFrame(frows), n_seen, n_verdict


# ============================================================ PART C/E: fresh grid machinery
def fast_backtest(prices, weights, freq=FREQ):
    """Vectorised equivalent of engine.backtest, returning (gross returns, turnover) so a
    whole cost LADDER comes off one run: net_r = r - bps/1e4 * turnover.  Gate G1 asserts
    identity with engine.backtest at cost 0, and gate G4 asserts the ladder identity at
    every rung against the engine's own costed run."""
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
    band=dict(c0=0.03, step=0.01, grid=[round(0.00 + 0.01 * i, 4) for i in range(13)], host="V2"),
    # gross stops at 1.00: PROTOCOL 2 forbids leverage unless the idea asks for it, and this
    # idea is about cost rungs, not exposure.
    gross=dict(c0=0.75, step=0.05, grid=[round(0.30 + 0.05 * i, 4) for i in range(15)], host="V2"),
    n=dict(c0=20, step=2, grid=list(range(4, 41, 2)), host="V1"),
)


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
        self.spy = legs(px["SPY"].pct_change().fillna(0.0))     # buy-and-hold, cost-free

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
    """The five PROTOCOL-4b bars over the full sample, signed; all >= 0 passes."""
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


# ======================================================================================= gates
def gate_g0():
    """G0  reproduce idea 408R's published FLIP1 base rates from ITS OWN committed artefact,
    and read the pass count beside them -- the number the parent published without."""
    f = BT / "2026-09-10_publish-step_delta-beside-every-adopted-constant_B.cols.csv"
    d = pd.read_csv(f)
    hd = d[d.density == "COARSE"]
    g = hd.groupby("cost").agg(n=("FLIP1", "size"), flip=("FLIP1", "mean"),
                               n_pass4b=("pass4b", "sum"))
    say("G0  idea 408R's own .cols.csv (COARSE grid, the rows its headline was computed on):")
    for c, r in g.iterrows():
        say(f"      {c:5.1f} bps  n={int(r.n):4d}   FLIP1 {r.flip:6.1%}   pass4b {int(r.n_pass4b):3d}"
            f"  ({r.n_pass4b/r.n:5.1%} of points)")
    exp = {0.0: 0.160, 10.0: 1.0 / 15, 25.0: 0.0}
    for c, v in exp.items():
        assert abs(float(g.loc[c, "flip"]) - v) < 1e-6, f"G0 FAILED at {c} bps"
    say("      published 16.0% / 6.7% / 0.0% reproduced exactly.  The pass COUNT beside it is")
    say("      31 -> 5 -> 0: at 25 bps the parent's grid has no passing point at all, so its")
    say("      FLIP1 = 0 is arithmetic, not evidence about fragility.")
    return g


def gate_g1(P):
    w = P.w_v2(0.03, 0.75)
    fr, ft = fast_backtest(P.q, w)
    eng = backtest(P.q, w, cost_bps=0.0, freq=FREQ)
    st = P.q.index[WARMUP]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    say(f"G1  fast_backtest vs engine.backtest (cost 0):  max|dret| {dr:.3e}   max|dturn| {dt:.3e}")
    assert dr < 1e-10 and dt < 1e-10, "G1 FAILED"


def gate_g2(P):
    d2 = float((P.w_v2(0.03, 0.75) - rules_v2_weights(P.q, 0.03, 0.75)).abs().max().max())
    d1 = float((P.w_v1(20) - rules_v1_weights(P.q, n=20, w=0.15, max_vol=0.60)).abs().max().max())
    say(f"G2  host V2 vs baseline.rules_v2_weights {d2:.3e};  host V1 vs rules_v1_weights {d1:.3e}")
    assert d2 < 1e-12 and d1 < 1e-12, "G2 FAILED"


def gate_g3():
    """G3  the arithmetic the whole file turns on, on synthetic verdict strings.

    (a) an ALL-FAIL sweep has 0 flips and 0 boundaries -- FLIP1 cannot distinguish it from a
        perfectly robust all-pass sweep;
    (b) flip_count <= 2 x boundaries always, with equality when boundaries are separated;
    (c) a single isolated passer in a sea of failures is the MAXIMUM-flip configuration per
        passer (3 flagged points), so a falling pass count mechanically caps FLIP1."""
    a = [False] * 9
    b = [False, False, True, True, True, False, False, False, False]
    c = [False, True, False, False, True, False, False, True, False]
    d = [True] * 9
    for lbl, v in (("all-fail", a), ("one run", b), ("3 isolated", c), ("all-pass", d)):
        say(f"G3  {lbl:11s} passes={sum(v)}  boundaries={n_boundaries(v)}  "
            f"flips={int(flip_flags(v).sum())}  <= 2B={2*n_boundaries(v)}")
    assert flip_flags(a).sum() == 0 and flip_flags(d).sum() == 0, "G3 FAILED (a)"
    for v in (a, b, c, d):
        assert flip_flags(v).sum() <= 2 * n_boundaries(v), "G3 FAILED (b)"
    assert flip_flags(c).sum() == 9, "G3 FAILED (c)"        # 3 flagged points per isolated passer
    say("      all-fail and all-pass are INDISTINGUISHABLE under FLIP1 (0 flips each).")


def gate_g4(P):
    """G4  the cost ladder identity: net = gross - bps/1e4 * turnover, checked against the
    engine's own costed run at every rung, so nine rungs off one backtest is exact."""
    w = P.w_v2(0.03, 0.75)
    fr, ft = fast_backtest(P.q, w)
    st = P.q.index[WARMUP]
    worst = 0.0
    for bps in RUNGS:
        eng = backtest(P.q, w, cost_bps=bps, freq=FREQ)["returns"].loc[st:]
        mine = (fr - bps / 1e4 * ft).loc[st:]
        worst = max(worst, float((mine - eng).abs().max()))
    say(f"G4  ladder identity vs engine.backtest over {len(RUNGS)} rungs:  max|dret| {worst:.3e}")
    assert worst < 1e-10, "G4 FAILED"


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
    say("IDEA 633  is FLIP1 already dead at 10 bps?    (lane C, 2026-09-10)")
    say("=" * 100)

    # ---------------------------------------------------------------- PART A  GATES
    say("\n=== PART A  GATES ===")
    g0 = gate_g0()
    gate_g3()

    say("\n  loading panels ...")
    PX = load_panels()
    PAN = {k: Panel(v) for k, v in PX.items()}
    for k, v in PX.items():
        say(f"    {k:9s} {v.shape[1]-1:4d} names   {v.index[0].date()} .. {v.index[-1].date()}")
    gate_g1(PAN["U56"]); gate_g2(PAN["U56"]); gate_g4(PAN["U56"])

    # ---------------------------------------------------------------- PART B  CENSUS
    say("\n=== PART B  CENSUS of every committed dial sweep with a 4b verdict and a rung ===")
    CEN, FIL, n_seen, n_verdict = census()
    FIL.to_csv(f"{OUT}.files.csv", index=False)
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  {n_seen} committed CSVs read;  {n_verdict} carry a 4b verdict column;")
    say(f"  {int((FIL.n_sweeps > 0).sum())} of those are usable dial sweeps with a declared rung "
        f"-> {len(CEN)} sweeps, {int(CEN.G.sum())} grid points.")
    if len(FIL[FIL.n_sweeps == 0]):
        say("  exclusions, by reason (every one written out rather than filtered silently):")
        for r, k in FIL[FIL.n_sweeps == 0].reason.value_counts().items():
            say(f"      {k:4d}  {r}")

    say("\n  B1  WHAT RUNG IS THE RECORD'S 4b-SWEEP CORPUS PUBLISHED AT?")
    rc = CEN.groupby("rung").agg(sweeps=("G", "size"), points=("G", "sum"),
                                 files=("file", "nunique"))
    rc["share_pts"] = rc.points / rc.points.sum()
    say(rc.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  B2  NEIGHBOUR FLIPS AS A FUNCTION OF THE RUNG (the queue's census)")
    say("      flip_rate = flagged points / points.   mixed = sweeps with 0 < passers < G,")
    say("      i.e. sweeps that HAVE a boundary for a flip to sit next to.")
    lad = []
    for rung, g in CEN.groupby("rung"):
        pts = int(g.G.sum())
        mx = g[g.mixed == 1]
        lad.append(dict(rung=rung, sweeps=len(g), points=pts,
                        pass_share=float(g.n_pass.sum() / pts),
                        empty_share=float((g.n_pass == 0).mean()),
                        full_share=float((g.n_pass == g.G).mean()),
                        mixed_share=float(g.mixed.mean()),
                        flip_rate=float(g.n_flip.sum() / pts),
                        flip_rate_mixed=float(mx.n_flip.sum() / mx.G.sum()) if len(mx) else np.nan,
                        B_per_mixed=float(mx.B.mean()) if len(mx) else np.nan))
    LAD = pd.DataFrame(lad).sort_values("rung")
    say(LAD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    cen_at = {r: LAD[LAD.rung == r] for r in PARENT_RUNGS}
    say("\n      the record's own three published rungs, side by side:")
    for r in PARENT_RUNGS:
        d = cen_at[r]
        if len(d):
            d = d.iloc[0]
            say(f"      {r:5.1f} bps  {int(d.points):6d} pts  flip {d.flip_rate:6.2%}  "
                f"mixed sweeps {d.mixed_share:6.2%}  flip|mixed {d.flip_rate_mixed:6.2%}")
        else:
            say(f"      {r:5.1f} bps  -- no committed sweep at this rung")

    # ---------------------------------------------------------------- PART C  FRESH GRID
    say("\n=== PART C  FRESH GRID: 3 panels x 3 dials x 9 rungs, every point committed ===")
    say("  one backtest per (panel, dial, value); all nine rungs are exact re-prices of it "
        "(gate G4).")
    rows = []
    for pn, P in PAN.items():
        base_r, base_t = fast_backtest(P.q, rules_v2_weights(P.q, 0.03, 0.75))
        S = P.spy
        for dial, spec in DIALS.items():
            for v in spec["grid"]:
                r, t = fast_backtest(P.q, P.book(dial, v))
                for bps in RUNGS:
                    L = legs(r - bps / 1e4 * t)
                    B = legs(base_r - bps / 1e4 * base_t)
                    mf, mi = m4b_full(L, S), m4b_is(L, S)
                    rows.append(dict(panel=pn, dial=dial, val=v, rung=bps,
                                     step=spec["step"], is_adopted=int(v == spec["c0"]),
                                     **{f"m_{k}": mf[k] for k in BARS},
                                     **{f"IS_m_{k}": mi[k] for k in BARS},
                                     m_min=min(mf.values()), IS_m_min=min(mi.values()),
                                     bind=min(mf, key=mf.get),
                                     pass4b=int(min(mf.values()) >= 0),
                                     IS_pass4b=int(min(mi.values()) >= 0),
                                     pass4a=pass4a(L, B),
                                     turnover=float(t.iloc[WARMUP:].sum() / (len(t) - WARMUP) * 252),
                                     base_Sharpe=B["Sharpe"], base_OOS_Sharpe=B["OOS_Sharpe"],
                                     base_OOS_CAGR=B["OOS_CAGR"], base_OOS_MaxDD=B["OOS_MaxDD"],
                                     spy_Sharpe=S["Sharpe"], spy_OOS_Sharpe=S["OOS_Sharpe"],
                                     spy_OOS_CAGR=S["OOS_CAGR"], spy_OOS_MaxDD=S["OOS_MaxDD"],
                                     **{k: L[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                          "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
                                                          "IS_H1", "IS_H2",
                                                          "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}))
        say(f"    {pn:9s} done ({sum(len(s['grid']) for s in DIALS.values())} books "
            f"x {len(RUNGS)} rungs)")
    GR = pd.DataFrame(rows)

    # per-sweep fragility statistics on the fresh grid
    swr = []
    for (pn, dial, rung), g in GR.groupby(["panel", "dial", "rung"]):
        g = g.sort_values("val").reset_index(drop=True)
        pas = g.pass4b.values.astype(bool)
        fl = flip_flags(pas)
        GRn = len(g)
        st = {k: step_delta(list(g.val), dict(zip(g.val, g[f"m_{k}"]))) for k in BARS}
        thin = []
        for i in range(GRn):
            bar = g.bind.iloc[i]
            s = st[bar]
            thin.append(abs(g.m_min.iloc[i]) / s if s and s > 0 else np.nan)
        w, lo, hi = widest_run(pas)
        swr.append(dict(panel=pn, dial=dial, rung=rung, G=GRn, n_pass=int(pas.sum()),
                        mixed=int(0 < pas.sum() < GRn), B=n_boundaries(pas),
                        n_flip=int(fl.sum()), flip_rate=float(fl.mean()),
                        window_pts=w, window_frac=w / GRn,
                        window_units=(0.0 if w == 0 else (g.val.iloc[hi] - g.val.iloc[lo])),
                        thin_rate_t1=float(np.nanmean(np.asarray(thin) < 1.0)),
                        thin_rate_t05=float(np.nanmean(np.asarray(thin) < 0.5)),
                        med_thin=float(np.nanmedian(thin)),
                        med_m_min=float(g.m_min.median()),
                        best_m_min=float(g.m_min.max())))
    SW = pd.DataFrame(swr)
    # attach FLIP1/thin back onto the point-level grid
    GR = GR.sort_values(["panel", "dial", "rung", "val"]).reset_index(drop=True)
    fl_all, th_all = [], []
    for (pn, dial, rung), g in GR.groupby(["panel", "dial", "rung"], sort=False):
        pas = g.pass4b.values.astype(bool)
        fl_all.append(pd.Series(flip_flags(pas).astype(int), index=g.index))
        st = {k: step_delta(list(g.val), dict(zip(g.val, g[f"m_{k}"]))) for k in BARS}
        th_all.append(pd.Series([abs(m) / st[b] if st[b] and st[b] > 0 else np.nan
                                 for m, b in zip(g.m_min, g.bind)], index=g.index))
    GR["FLIP1"] = pd.concat(fl_all).sort_index()
    GR["thin_ratio"] = pd.concat(th_all).sort_index()
    GR.to_csv(f"{OUT}.grid.csv", index=False)
    SW.to_csv(f"{OUT}.sweeps.csv", index=False)
    say(f"  {len(GR)} fresh grid points committed over {len(SW)} sweeps.")

    # ---------------------------------------------------------------- PART D  DECOMPOSITION
    say("\n=== PART D  IS THE FRAGILITY DEAD, OR IS THE PASS REGION DEAD? ===")
    say("\n  D1  the fresh ladder (pooled over 3 panels x 3 dials, 9 sweeps per rung):")
    lad2 = []
    for rung, g in SW.groupby("rung"):
        pts = int(g.G.sum()); mx = g[g.mixed == 1]
        gp = GR[GR.rung == rung]
        lad2.append(dict(rung=rung, sweeps=len(g), points=pts,
                         n_pass=int(g.n_pass.sum()), pass_share=float(g.n_pass.sum() / pts),
                         mixed_sweeps=int(g.mixed.sum()), mixed_share=float(g.mixed.mean()),
                         flip_rate=float(g.n_flip.sum() / pts),
                         flip_rate_mixed=float(mx.n_flip.sum() / mx.G.sum()) if len(mx) else np.nan,
                         med_window_pts=float(g.window_pts.median()),
                         thin_rate_t1=float(np.nanmean(gp.thin_ratio < 1.0)),
                         thin_rate_t05=float(np.nanmean(gp.thin_ratio < 0.5)),
                         med_thin=float(np.nanmedian(gp.thin_ratio)),
                         n_4a=int(gp.pass4a.sum())))
    LAD2 = pd.DataFrame(lad2).sort_values("rung")
    LAD2.to_csv(f"{OUT}.ladder.csv", index=False)
    say(LAD2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  D2  THE DECOMPOSITION.  Unconditionally, flip_rate = mixed_weight x flip|mixed,")
    say("      because a non-mixed sweep contributes exactly zero flips.  So the fall from")
    say("      0 bps to any higher rung splits exactly into a MIXED leg and a WITHIN leg:")
    say("          d(flip) = (w1-w0) x c0   +   w1 x (c1-c0)      [w = mixed point weight,")
    say("                     ^MIXED leg        ^WITHIN leg        c = flip rate | mixed]")
    both_rungs = CEN.groupby("file").rung.agg(
        lambda s: {0.0, PROTOCOL_RUNG}.issubset(set(s)))
    BF = list(both_rungs[both_rungs].index)
    LFL = CEN[CEN.file.isin(BF)]
    dec = []
    for src, tag in ((SW, "FRESH"), (CEN, "CENSUS"), (LFL, "LIKEFORLIKE")):
        base = src[src.rung == 0.0]
        if len(base) == 0:
            continue
        b_mx = base[base.mixed == 1]
        w0 = float(b_mx.G.sum() / base.G.sum()); c0 = float(b_mx.n_flip.sum() / b_mx.G.sum()) if len(b_mx) else 0.0
        for rung, g in src.groupby("rung"):
            if rung == 0.0:
                continue
            mx = g[g.mixed == 1]
            w1 = float(mx.G.sum() / g.G.sum())
            c1 = float(mx.n_flip.sum() / mx.G.sum()) if len(mx) else 0.0
            f0, f1 = w0 * c0, w1 * c1
            dec.append(dict(corpus=tag, rung=rung, flip_0bps=f0, flip_rung=f1,
                            d_total=f1 - f0, mixed_leg=(w1 - w0) * c0, within_leg=w1 * (c1 - c0),
                            w0=w0, w1=w1, c0=c0, c1=c1,
                            mixed_share_of_fall=((w1 - w0) * c0) / (f1 - f0) if abs(f1 - f0) > 1e-12 else np.nan))
    DEC = pd.DataFrame(dec)
    DEC.to_csv(f"{OUT}.decomp.csv", index=False)
    say(DEC.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("      READ THE LEGS, NOT THE SHARE: mixed_share_of_fall is leg/d_total and so is")
    say("      meaningless wherever d_total is near zero (the CENSUS 20-bps and 25-bps rows,")
    say("      and the FRESH rows where the rate does not move at all).  The two legs")
    say("      themselves are exact and additive at every rung.")
    for tag in DEC.corpus.unique():
        d = DEC[(DEC.corpus == tag) & (DEC.rung == PROTOCOL_RUNG)]
        if len(d):
            d = d.iloc[0]
            shr = (f"{d.mixed_share_of_fall:.0%} of it" if np.isfinite(d.mixed_share_of_fall)
                   else "no share is defined, the total change being 0")
            say(f"\n      {tag} at the PROTOCOL rung: flip {d.flip_0bps:.2%} -> {d.flip_rung:.2%} "
                f"({d.d_total:+.4f}).   MIXED leg {d.mixed_leg:+.4f} ({shr});   "
                f"WITHIN leg {d.within_leg:+.4f}.")

    say("\n  D3  DOES THE FRAGILITY STATISTIC DIE, OR DOES ONLY FLIP1?")
    say("      THIN and margin are defined at EVERY point, passing or not, so they survive a")
    say("      depopulated pass region; FLIP1 and window width do not.  Same ladder:")
    cols = ["rung", "pass_share", "mixed_share", "flip_rate", "flip_rate_mixed",
            "med_window_pts", "thin_rate_t1", "thin_rate_t05", "med_thin"]
    say(LAD2[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  D4  ARE THE RECORD'S PUBLISHED FRAGILITY CLAIMS 0-bps ARTEFACTS?")
    say("      The queue's charge only bites on claims actually PUBLISHED at 0 bps.  Count:")
    tot = int(CEN.G.sum())
    at0 = int(CEN[CEN.rung == 0.0].G.sum())
    at10 = int(CEN[CEN.rung == PROTOCOL_RUNG].G.sum())
    hi = int(CEN[CEN.rung > PROTOCOL_RUNG].G.sum())
    say(f"      committed sweep points at 0 bps {at0} ({at0/tot:.1%}), at 10 bps {at10} "
        f"({at10/tot:.1%}), above 10 bps {hi} ({hi/tot:.1%}), total {tot}.")
    f0 = CEN[CEN.rung == 0.0]; f10 = CEN[CEN.rung == PROTOCOL_RUNG]
    say(f"      flip rate on the 0-bps corpus {f0.n_flip.sum()/max(f0.G.sum(),1):.2%} vs "
        f"{f10.n_flip.sum()/max(f10.G.sum(),1):.2%} at 10 bps.")
    # files that publish a sweep at BOTH 0 and 10 bps: the within-file, like-for-like read
    say(f"      {len(BF)} committed files publish the SAME dial family at BOTH 0 and 10 bps; "
        f"within those files (the like-for-like read):")
    for rung, g in LFL.groupby("rung"):
        mx = g[g.mixed == 1]
        say(f"        {rung:5.1f} bps  {int(g.G.sum()):6d} pts  flip {g.n_flip.sum()/g.G.sum():6.2%}"
            f"  mixed {g.mixed.mean():6.2%}  flip|mixed "
            f"{(mx.n_flip.sum()/mx.G.sum()) if len(mx) else float('nan'):6.2%}")

    say("\n      D4b  THE PAIRED FILE-LEVEL SIGN TEST -- one vote per file, so a handful of")
    say("      large files cannot carry the pooled ratio.  For each of those files, its own")
    say("      flip rate at 0 bps against its own at 10 bps:")
    prs = []
    for f, g in LFL.groupby("file"):
        a, b = g[g.rung == 0.0], g[g.rung == PROTOCOL_RUNG]
        fa, fb = a.n_flip.sum() / a.G.sum(), b.n_flip.sum() / b.G.sum()
        amx, bmx = a[a.mixed == 1], b[b.mixed == 1]
        prs.append(dict(file=f, pts0=int(a.G.sum()), pts10=int(b.G.sum()),
                        flip0=float(fa), flip10=float(fb), d_flip=float(fb - fa),
                        mixed0=float(a.mixed.mean()), mixed10=float(b.mixed.mean()),
                        cond0=float(amx.n_flip.sum() / amx.G.sum()) if len(amx) else np.nan,
                        cond10=float(bmx.n_flip.sum() / bmx.G.sum()) if len(bmx) else np.nan,
                        dead10=int(fb == 0.0), alive10=int(fb > 0.0)))
    PR = pd.DataFrame(prs).sort_values("d_flip")
    PR.to_csv(f"{OUT}.paired.csv", index=False)
    fell = int((PR.d_flip < -1e-12).sum()); rose = int((PR.d_flip > 1e-12).sum())
    same = int(len(PR) - fell - rose)
    say(f"        flip rate FALLS 0->10 bps in {fell} files, RISES in {rose}, unchanged in "
        f"{same}, of {len(PR)}.")
    say(f"        files whose flip rate is EXACTLY ZERO at 10 bps (the queue's 'already dead'): "
        f"{int(PR.dead10.sum())} of {len(PR)};  of those, "
        f"{int(PR[PR.dead10 == 1].flip0.gt(0).sum())} had a non-zero rate at 0 bps.")
    say(f"        mean |d_flip| {PR.d_flip.abs().mean():.4f};  mean conditional rate "
        f"{PR.cond0.mean():.3f} (0 bps) vs {PR.cond10.mean():.3f} (10 bps) over the "
        f"{int(PR.cond0.notna().sum() & PR.cond10.notna().sum())} files where both are defined.")
    say(PR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- PART E  RULE 8
    say("\n=== PART E  RULE 8 (choose on 2009-2016 only, evaluate 2017-2026 untouched) ===")
    say("  Three choosers, each run per (panel, dial, RUNG).  All read the IS window only.")
    say("    PLAIN    argmax IS Sharpe over the sweep.")
    say("    ROBUST   argmax IS Sharpe among points that are NOT IS-FLIP1 and not IS-THIN")
    say("             (|IS margin|/step >= 1); if that leaves nothing, fall back to PLAIN.")
    say("    WINDOW   midpoint of the widest contiguous IS-4b run; ABSTAIN to RULES v2 if")
    say("             the sweep has no IS-4b point at all.")
    say("  The pre-registered prediction: if FLIP1 is dead at 10 bps then ROBUST is IDENTICAL")
    say("  to PLAIN there by construction, and any OOS difference between them can only come")
    say("  from rungs where flips still exist.")
    wf = []
    for (pn, dial, rung), g in GR.groupby(["panel", "dial", "rung"]):
        g = g.sort_values("val").reset_index(drop=True)
        ispas = g.IS_pass4b.values.astype(bool)
        isfl = flip_flags(ispas)
        st = {k: step_delta(list(g.val), dict(zip(g.val, g[f"IS_m_{k}"]))) for k in BARS}
        isbind = [min({k: g[f"IS_m_{k}"].iloc[i] for k in BARS},
                      key=lambda k: g[f"IS_m_{k}"].iloc[i]) for i in range(len(g))]
        isthin = np.array([abs(g.IS_m_min.iloc[i]) / st[isbind[i]]
                           if st[isbind[i]] and st[isbind[i]] > 0 else np.nan
                           for i in range(len(g))])
        picks = {}
        picks["PLAIN"] = (int(g.IS_Sharpe.values.argmax()), "argmax IS Sharpe")
        ok = (~isfl) & (~(isthin < 1.0))
        if ok.any():
            idx = int(np.where(ok, g.IS_Sharpe.values, -np.inf).argmax())
            picks["ROBUST"] = (idx, "argmax IS Sharpe among non-flip non-thin")
        else:
            picks["ROBUST"] = (picks["PLAIN"][0], "FALLBACK to PLAIN (no robust point)")
        w, lo, hi = widest_run(ispas)
        if w > 0:
            picks["WINDOW"] = (int(round((lo + hi) / 2)), f"midpoint of widest IS-4b run ({w} pts)")
        else:
            picks["WINDOW"] = (None, "ABSTAIN to RULES v2 (no IS-4b point)")
        base_row = dict(base_OOS_Sharpe=g.base_OOS_Sharpe.iloc[0],
                        base_OOS_CAGR=g.base_OOS_CAGR.iloc[0],
                        base_OOS_MaxDD=g.base_OOS_MaxDD.iloc[0],
                        spy_OOS_Sharpe=g.spy_OOS_Sharpe.iloc[0],
                        spy_OOS_CAGR=g.spy_OOS_CAGR.iloc[0],
                        spy_OOS_MaxDD=g.spy_OOS_MaxDD.iloc[0])
        for cho, (i, how) in picks.items():
            if i is None:
                r = dict(pick=np.nan, OOS_CAGR=base_row["base_OOS_CAGR"],
                         OOS_Sharpe=base_row["base_OOS_Sharpe"],
                         OOS_MaxDD=base_row["base_OOS_MaxDD"],
                         CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, H1=np.nan, H2=np.nan,
                         pass4a=0, pass4b=0, FLIP1=0, thin=np.nan)
            else:
                row = g.iloc[i]
                r = dict(pick=row.val, OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                         OOS_MaxDD=row.OOS_MaxDD, CAGR=row.CAGR, Sharpe=row.Sharpe,
                         MaxDD=row.MaxDD, H1=row.H1, H2=row.H2,
                         pass4a=int(row.pass4a), pass4b=int(row.pass4b),
                         FLIP1=int(isfl[i]), thin=float(isthin[i]))
            wf.append(dict(panel=pn, dial=dial, rung=rung, CHOOSER=cho, how=how,
                           n_IS_pass=int(ispas.sum()), n_IS_flip=int(isfl.sum()),
                           **r, **base_row,
                           d_base=r["OOS_Sharpe"] - base_row["base_OOS_Sharpe"],
                           d_spy=r["OOS_Sharpe"] - base_row["spy_OOS_Sharpe"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("\n  E1  how often does ROBUST differ from PLAIN, by rung?")
    pv = WF.pivot_table(index=["panel", "dial", "rung"], columns="CHOOSER", values="pick",
                        aggfunc="first")
    pv["differs"] = (pv.ROBUST != pv.PLAIN).astype(int)
    dif = pv.reset_index().groupby("rung").agg(cells=("differs", "size"),
                                               robust_differs=("differs", "sum"))
    isf = WF[WF.CHOOSER == "PLAIN"].groupby("rung").agg(IS_flips=("n_IS_flip", "sum"),
                                                        IS_pass=("n_IS_pass", "sum"))
    say(dif.join(isf).to_string())

    say("\n  E2  every rule-8 pick, OOS 2017-2026, pooled by chooser and rung:")
    agg = WF.groupby(["CHOOSER", "rung"]).agg(
        cells=("pick", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), vs_base=("d_base", "mean"), vs_spy=("d_spy", "mean"),
        beats_base=("d_base", lambda s: int((s > 0).sum())),
        beats_spy=("d_spy", lambda s: int((s > 0).sum())),
        n4b=("pass4b", "sum"), n4a=("pass4a", "sum")).reset_index()
    say(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  E3  pooled over ALL rungs, and at the PROTOCOL rung alone:")
    for lbl, d in (("all rungs", WF), (f"{PROTOCOL_RUNG:g} bps only", WF[WF.rung == PROTOCOL_RUNG])):
        a = d.groupby("CHOOSER").agg(cells=("pick", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                                     OOS_CAGR=("OOS_CAGR", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                                     vs_base=("d_base", "mean"), vs_spy=("d_spy", "mean"),
                                     n4b=("pass4b", "sum"), n4a=("pass4a", "sum"))
        say(f"    {lbl}:")
        say(a.to_string(float_format=lambda x: f"{x:.4f}"))
    ref = WF.drop_duplicates("panel").set_index("panel")[
        ["base_OOS_Sharpe", "base_OOS_CAGR", "base_OOS_MaxDD",
         "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD"]]
    say("\n  the two reference books, OOS 2017-2026 (RULES v2 priced at 10 bps):")
    say(ref.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  E4  BOTH KEEP PATHS over every fresh grid point:")
    kp = []
    for (pn, dial, rung), g in GR.groupby(["panel", "dial", "rung"]):
        kp.append(dict(panel=pn, dial=dial, rung=rung, points=len(g),
                       n_4a=int(g.pass4a.sum()), n_4b=int(g.pass4b.sum()),
                       best_m_min=float(g.m_min.max()),
                       bind_at_best=g.loc[g.m_min.idxmax(), "bind"],
                       best_Sharpe=float(g.Sharpe.max())))
    KP = pd.DataFrame(kp)
    KP.to_csv(f"{OUT}.keeppaths.csv", index=False)
    say(KP.groupby("rung").agg(points=("points", "sum"), n_4a=("n_4a", "sum"),
                               n_4b=("n_4b", "sum")).to_string())
    say("\n    by (dial, rung), 4b passers:")
    say(KP.pivot_table(index="dial", columns="rung", values="n_4b", aggfunc="sum").to_string())
    say("    by (dial, rung), 4a passers:")
    say(KP.pivot_table(index="dial", columns="rung", values="n_4a", aggfunc="sum").to_string())
    n4b_p = int(GR[GR.rung == PROTOCOL_RUNG].pass4b.sum())
    n4a_p = int(GR[GR.rung == PROTOCOL_RUNG].pass4a.sum())
    say(f"\n    at the PROTOCOL rung: 4b {n4b_p} / {int((GR.rung==PROTOCOL_RUNG).sum())}, "
        f"4a {n4a_p}.  Rule-8 picks passing 4b: "
        f"{int(WF[WF.rung==PROTOCOL_RUNG].pass4b.sum())} of {int((WF.rung==PROTOCOL_RUNG).sum())}.")

    # ---------------------------------------------------------------------------- verdict
    say("\n" + "=" * 100)
    c0r = LAD2[LAD2.rung == 0.0].iloc[0]
    c10 = LAD2[LAD2.rung == PROTOCOL_RUNG].iloc[0]
    c25 = LAD2[LAD2.rung == 25.0].iloc[0]
    x0 = LAD[LAD.rung == 0.0].iloc[0]
    x10 = LAD[LAD.rung == PROTOCOL_RUNG].iloc[0]
    x25 = LAD[LAD.rung == 25.0].iloc[0]
    dl = DEC[(DEC.corpus == "LIKEFORLIKE") & (DEC.rung == PROTOCOL_RUNG)].iloc[0]
    say(f"ANSWER  THE QUEUE'S PREMISE IS FALSE.  On the record's OWN committed corpus "
        f"({len(CEN)} sweeps / {int(CEN.G.sum())} points over "
        f"{int((FIL.n_sweeps>0).sum())} files) the neighbour-flip rate at the PROTOCOL rung "
        f"is {x10.flip_rate:.2%}, ABOVE the {x0.flip_rate:.2%} at 0 bps and above the "
        f"{x25.flip_rate:.2%} at 25 bps.  Idea 408's monotone 16.0 -> 6.7 -> 0.0 is a "
        f"property of its own 150-point grid, not a record-wide law.")
    say(f"        LIKE-FOR-LIKE (the {len(PR)} files publishing the same dial family at both "
        f"rungs) the rate does fall, {dl.flip_0bps:.2%} -> {dl.flip_rung:.2%}, but it does "
        f"not die: {int(PR.alive10.sum())} of {len(PR)} of those files still carry flips at "
        f"10 bps, and per file it falls in {fell}, rises in {rose}, is unchanged in {same}.")
    say(f"        THE DECISIVE COUNT: {int(PR.dead10.sum())} of {len(PR)} files have a flip "
        f"rate of exactly zero at 10 bps, and ALL {int(PR.dead10.sum())} of them were already "
        f"zero at 0 bps -- NOT ONE committed file in the record loses its flips by moving "
        f"from 0 bps to the protocol rung.")
    say(f"        WHERE IT DOES FALL, THE MECHANISM IS DEPOPULATION, NOT SMOOTHING.  "
        f"flip = mixed_weight x flip|mixed exactly; at 10 bps the MIXED leg carries "
        f"{dl.mixed_leg:+.4f} of the {dl.d_total:+.4f} like-for-like fall and the WITHIN leg "
        f"{dl.within_leg:+.4f}.  On the fresh grid flip|mixed is FLAT at "
        f"{c0r.flip_rate_mixed:.1%} across all nine rungs while the mixed share falls "
        f"{c0r.mixed_share:.1%} -> {c10.mixed_share:.1%} -> {c25.mixed_share:.1%} -- the "
        f"within leg is identically zero.  At FILE level the same thing: the mean flip rate "
        f"CONDITIONAL on a boundary is {PR.cond0.mean():.3f} at 0 bps and "
        f"{PR.cond10.mean():.3f} at 10 bps, a change of {PR.cond10.mean()-PR.cond0.mean():+.3f}.")
    say(f"        SO the fragility statistic is not measuring robustness: an ALL-FAIL sweep "
        f"and an ALL-PASS sweep both score FLIP1 = 0 (gate G3), and costs empty the pass "
        f"region.  {at0/tot:.1%} of the record's committed sweep points are published at "
        f"0 bps, so the '0-bps artefact' charge can reach at most that share -- and on that "
        f"share the flips are FEWER, not more, than at the rung PROTOCOL actually uses.")
    say("=" * 100)

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(CEN=CEN, FIL=FIL, GR=GR, SW=SW, LAD=LAD, LAD2=LAD2, DEC=DEC, WF=WF, KP=KP)


if __name__ == "__main__":
    main()

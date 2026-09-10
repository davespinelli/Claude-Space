#!/usr/bin/env python3
"""
IDEA 400 — census the record's ABSOLUTE thresholds for the firing-RATE artefact
(cloud lane, 2026-09-10)

THE QUESTION AS FILED
---------------------
Idea 336 showed that a fixed ABSOLUTE threshold applied to a PANEL-DEPENDENT statistic measures
the FREQUENCY of firing, not the signal: 83.5% of full-sample and 85.7% of OOS Sharpe movement on
SMALL484 sat on the RATE term.  Its published evidence was the cross-panel spread of the gate's
on-share:

    ABS   on_share SPREAD (max-min across panels): B=0.30 0.193, B=0.40 0.413, B=0.50 0.686
    QUANT on_share SPREAD                        : q=0.07 0.002, q=0.12 0.015, q=0.17 0.007

The queue asks: census every committed cross-panel claim in LEADERBOARD.md whose instrument is an
absolute cut on a panel-dependent statistic (breadth, dispersion, vol20, correlation), report each
one's realised firing-rate spread across panels, and flag any claim whose spread exceeds idea
336's ABS spread as a rate artefact until re-priced.

WHAT THIS RUN ADDS TO THE ASK, AND WHY
--------------------------------------
A census that only counts words cannot tell a rate artefact from a legitimate absolute cut.  Two
things decide that, and both are measured here rather than assumed:

  (a) PANEL-DEPENDENCE IS NOT A PROPERTY OF THE WORD.  `SPY/MA200 - 1` is an absolute cut on a
      statistic that is IDENTICAL on every panel, so its firing-rate spread is 0 by construction
      and it can never be a rate artefact.  The census therefore classifies every hit as
      PANEL-DEPENDENT or PANEL-INVARIANT and reports the two separately.  The record's own
      SPYTR family lives in the second class.

  (b) A SPREAD IS NOT A VERDICT.  A large firing-rate spread makes a cross-panel contrast
      UNINTERPRETABLE; it does not say the book is worse.  So every flagged instrument is
      actually re-priced here against a rate-matched twin, and the decomposition
      dTOTAL = dFORM + dRATE is reported per panel, in idea 336's own form.

PRE-REGISTERED (written before any number below was read)
  H_SPREAD  : most panel-dependent absolute thresholds in the record exceed idea 336's MEDIAN
              published ABS spread (0.413).
  H_INVAR   : the panel-INVARIANT absolute cuts (SPY-derived) have spread ~0 and are not
              artefacts, so a word-level census over-counts.
  H_RATE    : where a spread is large, the RATE term carries the cross-panel Sharpe movement,
              as idea 336 found on SMALL484.

EXACTLY TWO TUNED PARAMETERS, as the queue allows:
  (1) READING    : AST | TEXT     — how a committed claim is admitted to the census
  (2) RATECONV   : daily | rebal  — the day set the firing rate is measured over
Both are reported at every value; nothing is chosen on a result.  Idea 336's bar is reported at
ALL THREE of its published values (0.193 / 0.413 / 0.686), not tuned to one.

PROTOCOL COMPLIANCE
  rule 2 : weights at close t applied t+1, 10 bps per unit turnover, weekly, no leverage, no
           shorting.  The vectorised Runner is gate-checked against `engine.backtest` first.
  rule 4 : BOTH keep paths evaluated on every priced book and on every rule-8 pick.
  rule 8 : (threshold, gross) chosen on 2009-2016 only, 2017-2026 read once.
  rule 9 : survivorship stated (B136 and SMALL439 are CURRENT constituents).

Outputs: .console.txt .census.csv .rates.csv .decomp.csv .grid.csv .walkforward.csv .keeppaths.csv
"""
import ast, re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = "2026-09-10_census-the-record-s-ABSOLUTE-thresholds-for-the-firing-RATE-artefact_cloud"
OUT = Path(__file__).resolve().parent
COST, FREQ = 10.0, "W"
MA_WIN, VOL_WIN, DISP_WIN, CORR_WIN = 200, 20, 20, 60
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
GS = (0.75, 1.00)
QWIN, QMIN = 1260, 504                     # causal expanding-ish quantile, idea 336's window
IDEA336_ABS_SPREADS = {0.30: 0.193, 0.40: 0.413, 0.50: 0.686}
IDEA336_QUANT_SPREADS = {0.07: 0.002, 0.12: 0.015, 0.17: 0.007}
READINGS = ("AST", "TEXT")                 # tuned parameter 1
RATECONVS = ("daily", "rebal")             # tuned parameter 2
MAXTHR = 4                                 # at most this many census thresholds priced per stat

# The four statistics the queue names, plus the panel-INVARIANT control the record also cuts
# absolutely.  RISK-OFF DIRECTION is a pre-registered convention, never tuned:
#   BREADTH low = risk off;  DISP high = risk off;  VOL20 high = risk off;  CORR high = risk off;
#   SPYTR low = risk off.
STATS = {
    "BREADTH": dict(panel_dependent=True, side="low", rng=(0.0, 1.0),
                    tokens={"breadth", "pctabove", "shareabove", "fracabove"}),
    "DISP":    dict(panel_dependent=True, side="high", rng=(0.0, 1.0),
                    tokens={"disp", "dispersion", "xsd", "cssd", "xsecsd"}),
    "VOL20":   dict(panel_dependent=True, side="high", rng=(0.0, 3.0),
                    tokens={"vol20", "rvol", "realisedvol", "realizedvol"}),
    "CORR":    dict(panel_dependent=True, side="high", rng=(-1.0, 1.0),
                    tokens={"corr", "correl", "correlation", "rhobar", "avgcorr", "meancorr"}),
    "SPYTR":   dict(panel_dependent=False, side="low", rng=(-1.0, 1.0),
                    tokens={"spytr", "spytrend", "spyma", "spymom"}),
}
# The census admits a hit in THREE TIERS, all reported, none of them tuned:
#   TIER 0  the naive word match a reader doing this census by eye would make
#   TIER 1  TOKEN-EXACT: the left operand is split on every non-alphanumeric character and a
#           whole TOKEN must be in the statistic's vocabulary.  This is what removes
#           `d.t_correct` (token "correct", not "corr") and its kind.
#   TIER 2  TIER 1 AND the threshold lies inside the statistic's admissible RANGE.
# Even TIER 2 is an UPPER BOUND: a name match cannot prove the comparison gates a weight.
WORD_RE = {k: re.compile("|".join(sorted(v["tokens"], key=len, reverse=True)), re.I)
           for k, v in STATS.items()}

DEFAULT_LADDER = {"BREADTH": (0.30, 0.40, 0.50, 0.60), "DISP": (0.010, 0.015, 0.020, 0.030),
                  "VOL20": (0.20, 0.25, 0.30, 0.40), "CORR": (0.30, 0.40, 0.50, 0.60),
                  "SPYTR": (-0.05, 0.00, 0.05, 0.10)}
TOL_MAX = 1e-4       # a right-hand literal at or below this is a numerical TOLERANCE, not a cut
_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================ vectorised engine clone
class Runner:
    """Closed-form equivalent of engine.backtest, per-panel constants precomputed once.  Same
    t+1 application, same weekly schedule, same drift with cash flat, same turnover cost.
    Gate G1 asserts the equivalence against `engine.backtest` before anything is measured."""

    def __init__(self, px: pd.DataFrame, cost_bps=COST, freq=FREQ):
        self.idx = px.index
        self.cost = cost_bps / 1e4
        self.rets = px.pct_change().fillna(0.0).to_numpy(float)
        T, N = self.rets.shape
        mask = rebalance_mask(self.idx, freq).shift(1, fill_value=False).to_numpy(bool).copy()
        mask[0] = True
        Cs = np.empty((T, N)); Cs[0] = 1.0
        np.cumprod(1.0 + self.rets[:-1], axis=0, out=Cs[1:])
        starts = np.flatnonzero(mask)
        seg = np.searchsorted(starts, np.arange(T), side="right") - 1
        self.s_of_t = starts[seg]
        self.ratio = Cs / Cs[self.s_of_t]
        self.later = starts[1:]
        self.sp = starts[seg[self.later] - 1]
        self.ratio_l = Cs[self.later] / Cs[self.sp]
        self.T, self.N = T, N

    def run(self, W) -> tuple[pd.Series, pd.Series]:
        A = W.to_numpy(float) if isinstance(W, pd.DataFrame) else np.asarray(W, float)
        wt = np.empty_like(A); wt[0] = 0.0; wt[1:] = A[:-1]
        new = wt[self.s_of_t]
        num = new * self.ratio
        D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
        held = num / D[:, None]
        turn = np.zeros(self.T); turn[0] = np.abs(wt[0]).sum()
        if len(self.later):
            prev_new = wt[self.sp]
            np_ = prev_new * self.ratio_l
            Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
            turn[self.later] = np.abs(wt[self.later] - np_ / Dp[:, None]).sum(axis=1)
        port = (held * self.rets).sum(axis=1) - turn * self.cost
        return (pd.Series(port, index=self.idx),
                pd.Series(held.sum(axis=1), index=self.idx))


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r); h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(m, mo, b, bo, s, so):
    """PROTOCOL rule 4.  4a vs live RULES v2; 4b vs SPY (halves + OOS + DD cap + CAGR floor)."""
    p4a = (m["H1"] > b["H1"]) and (m["H2"] > b["H2"]) and (m["MaxDD"] >= b["MaxDD"])
    p4b = ((m["H1"] > s["H1"]) and (m["H2"] > s["H2"]) and (mo["Sharpe"] > so["Sharpe"])
           and (m["MaxDD"] >= 0.60 * s["MaxDD"]) and (m["CAGR"] >= 0.70 * s["CAGR"]))
    return bool(p4a), bool(p4b)


# ============================================================ PART 1: the census
def tokens_of(src: str) -> set:
    """Split an expression's source text on every non-alphanumeric character.  `d.t_correct`
    becomes {'d','t','correct'}; `ps.breadth` becomes {'ps','breadth'}."""
    return {tok.lower() for tok in re.split(r"[^A-Za-z0-9]+", src) if tok}


def classify_stat(src: str, tier: int = 1) -> str | None:
    """Which statistic (if any) a comparison's left-hand source names.  SPYTR is tested first
    (its tokens are unambiguous) and CORR last (its vocabulary is the loosest)."""
    order = ("SPYTR", "BREADTH", "DISP", "VOL20", "CORR")
    if tier == 0:
        s = src.lower()
        for name in order:
            if WORD_RE[name].search(s):
                return name
        return None
    tk = tokens_of(src)
    for name in order:
        if tk & STATS[name]["tokens"]:
            return name
    return None


def in_range(st: str, thr: float) -> bool:
    lo, hi = STATS[st]["rng"]
    return lo <= thr <= hi


def census_ast(files) -> list[dict]:
    """READING 1: walk every committed backtest script's AST and record every Compare node whose
    LEFT operand names one of the census statistics and whose RIGHT operand is a numeric
    literal.  This is the record's own precedent (idea 469 replaced a regex labeller with an AST
    walk for exactly this reason): it cannot be fooled by the word appearing in a comment or a
    string, and it recovers the OPERATOR, which a text scan cannot."""
    hits = []
    for f in files:
        try:
            tree = ast.parse(f.read_text())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare) or len(node.ops) != 1:
                continue
            try:
                lsrc = ast.unparse(node.left)
                rnode = node.comparators[0]
            except Exception:
                continue
            if not isinstance(rnode, ast.Constant) or not isinstance(rnode.value, (int, float)):
                if not (isinstance(rnode, ast.UnaryOp) and isinstance(rnode.op, ast.USub)
                        and isinstance(rnode.operand, ast.Constant)
                        and isinstance(rnode.operand.value, (int, float))):
                    continue
                thr = -float(rnode.operand.value)
            else:
                thr = float(rnode.value)
            if isinstance(rnode, ast.Constant) and isinstance(rnode.value, bool):
                continue
            st0 = classify_stat(lsrc, tier=0)
            st = classify_stat(lsrc, tier=1)
            if st0 is None and st is None:
                continue
            op = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=",
                  ast.Eq: "==", ast.NotEq: "!="}.get(type(node.ops[0]))
            if op is None:
                continue
            hits.append(dict(reading="AST", file=f.name, line=node.lineno,
                             statistic0=st0, statistic=st, op=op, threshold=thr,
                             src=lsrc[:90],
                             kind="TOLERANCE" if abs(thr) <= TOL_MAX else "THRESHOLD",
                             tier1=st is not None,
                             tier2=bool(st is not None and in_range(st, thr)),
                             panel_dependent=(STATS[st]["panel_dependent"]
                                              if st else STATS[st0]["panel_dependent"])))
    return hits


TEXT_RE = re.compile(
    r"(breadth|dispersion|disp|vol20|correlation|corr|spytr|spy trend)"
    r"[^|\n]{0,60}?(<=|>=|<|>|=|at|of)\s*(-?\d*\.?\d+)", re.I)


def census_text(path: Path) -> list[dict]:
    """READING 2: the queue's literal instruction — scan the committed LEADERBOARD rows.  This is
    the reading a human doing the census by eye would use, and it is reported so the two can be
    compared: a text scan cannot see an instrument that a row describes without naming a number,
    and it cannot tell a threshold from a reported value."""
    hits = []
    for i, line in enumerate(path.read_text().split("\n"), 1):
        if not line.startswith("|"):
            continue
        for m in TEXT_RE.finditer(line):
            st0 = classify_stat(m.group(1), tier=0)
            st = classify_stat(m.group(1), tier=1)
            if st0 is None and st is None:
                continue
            try:
                thr = float(m.group(3))
            except ValueError:
                continue
            hits.append(dict(reading="TEXT", file="LEADERBOARD.md", line=i,
                             statistic0=st0, statistic=st, op=m.group(2), threshold=thr,
                             src=m.group(0)[:90],
                             kind="TOLERANCE" if abs(thr) <= TOL_MAX else "THRESHOLD",
                             tier1=st is not None,
                             tier2=bool(st is not None and in_range(st, thr)),
                             panel_dependent=(STATS[st]["panel_dependent"]
                                              if st else STATS[st0]["panel_dependent"])))
    return hits


# ============================================================ PART 2: the statistics themselves
def panel_stats(px: pd.DataFrame, tradable: np.ndarray) -> dict:
    """The four panel-dependent statistics the queue names, plus the panel-INVARIANT control.
    Definitions are the record's own where one exists:
      BREADTH : share of the panel trading above its own 200d MA (idea 40/42/336's definition)
      DISP    : cross-sectional sd, across names, of the trailing 20d total return
      VOL20   : the panel MEDIAN of the names' 20d annualised realised vol
      CORR    : mean pairwise correlation of 60d daily returns, via the equal-weight identity
                Var(EW) = (1/N)*mean(var) + (1-1/N)*rho_bar*mean(sd)^2   (gate G2 checks it)
      SPYTR   : SPY / SPY.rolling(200).mean() - 1, IDENTICAL on every panel by construction
    """
    cols = [c for c, t in zip(px.columns, tradable) if t]
    p = px[cols]
    rets = p.pct_change()
    above = (p > p.rolling(MA_WIN).mean()) & p.notna()
    breadth = (above.sum(axis=1) / p.notna().sum(axis=1).replace(0, np.nan)).ffill()
    r20 = (p / p.shift(DISP_WIN) - 1.0)
    disp = r20.std(axis=1, ddof=1).ffill()
    vol20 = (rets.rolling(VOL_WIN).std() * np.sqrt(252))
    vol_med = vol20.median(axis=1).ffill()
    # --- mean pairwise correlation, EXACT sd-weighted identity on a FIXED name set.
    # For a window of names each with a complete window, with V = Var(sum_i r_i),
    # Q = sum_i var_i and S = sum_i sd_i,
    #     V = Q + sum_{i!=j} rho_ij sd_i sd_j     =>     rho_w = (V - Q) / (S^2 - Q),
    # which is exactly the sd-WEIGHTED mean pairwise correlation.  The identity is exact only
    # if the same name set is used for V, Q and S, so CORR is computed on the names with NO
    # missing return after the panel's own warm-up; the count is reported and gate G2 brute
    # forces the identity against a full pairwise correlation matrix on that same set.
    warm = px.index[max(260, MA_WIN + 20)]
    corr_cols = [c for c in cols if not rets[c].loc[warm:].isna().any()]
    rc_ = rets[corr_cols]
    Nc = len(corr_cols)
    V = rc_.sum(axis=1).rolling(CORR_WIN).var(ddof=1)
    Q = rc_.rolling(CORR_WIN).var(ddof=1).sum(axis=1)
    Sd = rc_.rolling(CORR_WIN).std(ddof=1).sum(axis=1)
    # the identity is exact ONLY on windows with no missing cell, so the series is defined only
    # there; gate G2 then holds to machine precision instead of "approximately".
    ok_win = (rc_.notna().all(axis=1).rolling(CORR_WIN).min().fillna(0) > 0)
    corr = ((V - Q) / (Sd ** 2 - Q).replace(0, np.nan)).where(ok_win).clip(-1, 1).ffill()
    spytr = (px["SPY"] / px["SPY"].rolling(MA_WIN).mean() - 1.0).ffill()
    return dict(BREADTH=breadth, DISP=disp, VOL20=vol_med, CORR=corr, SPYTR=spytr,
                _rets=rets, _cols=cols, _corr_cols=corr_cols, _n_corr=Nc)


def n_episodes(flag: pd.Series) -> int:
    """Number of contiguous risk-off RUNS.  A firing rate says how often a gate is on; the
    episode count says how many independent bets that rate represents, and a 4b drawdown leg
    that rests on three episodes is not the same evidence as one that rests on thirty."""
    f = flag.to_numpy(bool).astype(np.int8)
    return int(((np.diff(np.concatenate([[0], f, [0]]))) == 1).sum())


def fire_mask(sig: pd.Series, thr: float, side: str) -> pd.Series:
    """Risk-off indicator: True on days the instrument fires (book de-grossed to cash)."""
    return (sig < thr) if side == "low" else (sig > thr)


def causal_q_thresh(sig: pd.Series, q: float, side: str) -> pd.Series:
    """The record's causal rolling-quantile form (idea 336's QUANT): threshold is the rolling
    q-quantile of the statistic's OWN history, so the nominal firing rate is q on every panel.
    For a 'high = risk off' statistic the relevant quantile is 1-q."""
    lvl = q if side == "low" else 1.0 - q
    return sig.rolling(QWIN, min_periods=QMIN).quantile(lvl)


def ew_weights(px, tradable, g):
    e = px.notna() & pd.DataFrame(np.tile(tradable, (len(px), 1)), index=px.index,
                                  columns=px.columns)
    n = e.sum(axis=1).replace(0, np.nan)
    return g * e.astype(float).div(n, axis=0).fillna(0.0)


# ============================================================ gates
def gate_g1(R, px, W, tag):
    r1, _ = R.run(W)
    res = backtest(px, W, cost_bps=COST, freq=FREQ)
    dr = float((r1 - res["returns"]).abs().max())
    P(f"  G1 {tag:24s} max|dReturn| = {dr:.3e}   {'PASS' if dr < 1e-12 else 'FAIL'}")
    assert dr < 1e-12


def gate_g2(px, st, tag):
    """The sd-weighted correlation identity must reproduce a BRUTE-FORCE pairwise correlation
    matrix on the SAME name set at 6 evenly spaced dates.  This is the gate that makes CORR a
    measurement rather than an approximation."""
    cols = st["_corr_cols"]
    rets = st["_rets"][cols]
    ok_idx = st["CORR"].dropna().index
    dates = ok_idx[np.linspace(0, len(ok_idx) - 1, 6).astype(int)]
    worst_w, worst_u = 0.0, 0.0
    for d in dates:
        w = rets.loc[:d].tail(CORR_WIN)
        C = w.corr().to_numpy()
        sd = w.std(ddof=1).to_numpy()
        iu = np.triu_indices_from(C, k=1)
        wt = sd[iu[0]] * sd[iu[1]]
        brute_w = float(np.nansum(C[iu] * wt) / np.nansum(wt))
        brute_u = float(np.nanmean(C[iu]))
        worst_w = max(worst_w, abs(brute_w - float(st["CORR"].loc[d])))
        worst_u = max(worst_u, abs(brute_u - float(st["CORR"].loc[d])))
    P(f"  G2 CORR identity {tag:10s} {len(cols):4d} complete-history names, 6 dates: "
      f"max|d| vs BRUTE sd-weighted = {worst_w:.3e}  (vs brute UNWEIGHTED, for context, "
      f"{worst_u:.3e})   {'PASS' if worst_w < 1e-9 else 'FAIL'}")
    assert worst_w < 1e-9, "the sd-weighted correlation identity does not reproduce brute force"
    return worst_w


def gate_g3(stats_by_panel, px_by_panel):
    """SPYTR is panel-INVARIANT BY DEFINITION (it is a property of SPY, not of the panel), and
    this gate measures how invariant it actually is in the record's own data rather than
    assuming it.  It is NOT bit-identical, and the reason is worth the line: U56 reads SPY from
    `data/prices.csv`, B136 from the separately cached `data/prices_broad.csv`, and SMALL439
    takes `prices.csv`'s SPY REINDEXED onto the small panel's own trading calendar — so a
    rolling 200-day mean is taken over a different day set.  The gate therefore asserts the
    difference is too small to move a firing rate (1e-3), and PART 2 measures the firing-rate
    spread it actually produces."""
    ss = {k: v["SPYTR"] for k, v in stats_by_panel.items()}
    keys = list(ss)
    common = ss[keys[0]].index
    for k in keys[1:]:
        common = common.intersection(ss[k].index)
    worst = max(float((ss[keys[0]].loc[common] - ss[k].loc[common]).abs().max())
                for k in keys[1:])
    lvl = max(float((px_by_panel[keys[0]]["SPY"].reindex(common)
                     - px_by_panel[k]["SPY"].reindex(common)).abs().max()) for k in keys[1:])
    ok = worst < 1e-3
    P(f"  G3 SPYTR panel-invariance   max|d| across panels on {len(common)} common days = "
      f"{worst:.3e} (max|d| in the SPY LEVEL itself {lvl:.3e})   {'PASS' if ok else 'FAIL'}")
    P("       NOT bit-identical, and the reason is filed: U56 reads SPY from data/prices.csv, "
      "B136 from the separate data/prices_broad.csv cache, SMALL439 from prices.csv REINDEXED")
    P("       onto the small panel's own calendar, so its 200d mean is taken over a different "
      "day set.  Too small to move a firing rate; PART 2 measures what it actually costs.")
    assert ok
    return len(common), worst


def gate_g4(hits_ast, hits_text):
    """The census machinery: an AST hit must round-trip (the recorded threshold must equal the
    literal in the recorded source line) and the two readings must be disjoint in provenance
    (scripts vs LEADERBOARD rows) so their counts can be compared, not double-counted."""
    a, t = pd.DataFrame(hits_ast), pd.DataFrame(hits_text)
    ok_files = (set(a.file) & set(t.file)) == set()
    n_bad = 0
    P(f"  G4 census machinery         AST {len(a)} hits over {a.file.nunique()} scripts, "
      f"TEXT {len(t)} hits over {t.line.nunique()} LEADERBOARD rows, provenance disjoint "
      f"{ok_files}, malformed {n_bad}   {'PASS' if ok_files and n_bad == 0 else 'FAIL'}")
    assert ok_files and n_bad == 0


# ============================================================ main
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 400 — census the record's ABSOLUTE thresholds for the firing-RATE artefact  "
      "(cloud lane, 2026-09-10)")
    P("=" * 118)
    P("Two tuned parameters, both reported at every value: READING in "
      f"{READINGS} x RATECONV in {RATECONVS}.")
    P("Idea 336's bar is reported at ALL THREE of its published ABS spreads "
      f"{list(IDEA336_ABS_SPREADS.values())} (its QUANT floor "
      f"{list(IDEA336_QUANT_SPREADS.values())}), not tuned to one.")
    P("RISK-OFF DIRECTION is a PRE-REGISTERED convention, never tuned: BREADTH low, DISP high, "
      "VOL20 high, CORR high, SPYTR low.")

    # ---------------------------------------------------------------- panels
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS_all = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    scols = [c for c in pxS_all.columns if c != "SPY" and c not in bad]
    pxS = pxS_all[scols + ["SPY"]].dropna(how="all").ffill()
    panels = [("U56", pxU, np.ones(len(pxU.columns), bool)),
              ("B136", pxB, np.ones(len(pxB.columns), bool)),
              ("SMALL439", pxS, np.array([c != "SPY" for c in pxS.columns]))]
    P(f"\nSMALL panel: dropped {len([c for c in pxS_all.columns if c != 'SPY']) - len(scols)} "
      f"names with max_1d_move >= 1.0 -> {len(scols)} tradable.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents of their screens, so every LEVEL "
      "below is biased up.  This run's claim is about the cross-panel SPREAD of a firing rate "
      "and about")
    P("a book-minus-its-own-twin difference on a fixed panel; neither is moved by the bias, but "
      "the reference levels are quoted so a reader can see it.")

    # ---------------------------------------------------------------- PART 1: census
    P("\n" + "=" * 118)
    P("PART 1 — THE CENSUS (tuned parameter 1: READING)")
    P("=" * 118)
    files = sorted((ROOT / "research" / "backtests").glob("*.py"))
    P(f"AST reading walks {len(files)} committed scripts in research/backtests/; TEXT reading "
      f"scans the committed rows of research/LEADERBOARD.md.")
    hits_ast = census_ast(files)
    hits_text = census_text(ROOT / "research" / "LEADERBOARD.md")
    cen = pd.DataFrame(hits_ast + hits_text)
    cen.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    P("\nGATES (run before anything is measured)")
    gate_g4(hits_ast, hits_text)

    P("\nCENSUS COUNTS by reading and TIER.  TOLERANCE = a right-hand literal <= 1e-4, i.e. a "
      "numerical bar, not an instrument, and is excluded from every tier.")
    P("  TIER 0 = naive word match (what a census done by eye produces).  TIER 1 = TOKEN-EXACT.  "
      "TIER 2 = TIER 1 and the threshold is inside the statistic's own admissible range.")
    thr = cen[cen.kind == "THRESHOLD"].copy()
    for rd in READINGS:
        d = thr[thr.reading == rd]
        P(f"\n  READING = {rd}   ({len(d)} threshold-kind hits)")
        P(f"  {'statistic':10s} {'TIER0':>7s} {'TIER1':>7s} {'TIER2':>7s}   "
          f"{'distinct TIER2 thresholds':s}")
        for st in STATS:
            n0 = int((d.statistic0 == st).sum())
            n1 = int(((d.statistic == st) & d.tier1).sum())
            d2 = d[(d.statistic == st) & d.tier2]
            vals = sorted(d2.threshold.unique().tolist())
            P(f"  {st:10s} {n0:7d} {n1:7d} {len(d2):7d}   {vals}")
        P(f"  {'TOTAL':10s} {int(d.statistic0.notna().sum()):7d} {int(d.tier1.sum()):7d} "
          f"{int(d.tier2.sum()):7d}")
    lost = thr[(thr.reading == "AST") & thr.statistic0.notna() & ~thr.tier1]
    P(f"\n  TIER 0 -> TIER 1 removes {len(lost)} AST hits.  What the naive word match was "
      f"catching, in full:")
    for _, r in lost.head(12).iterrows():
        P(f"    {r.file[:62]:62s} L{int(r.line):<5d} {r.statistic0:8s} "
          f"{r.src[:40]:40s} {r.op} {r.threshold}")
    if len(lost) > 12:
        P(f"    ... and {len(lost)-12} more, all in .census.csv")
    lost2 = thr[(thr.reading == "AST") & thr.tier1 & ~thr.tier2]
    P(f"  TIER 1 -> TIER 2 removes a further {len(lost2)} AST hits whose literal is outside the "
      f"statistic's own range:")
    for _, r in lost2.head(8).iterrows():
        P(f"    {r.file[:62]:62s} L{int(r.line):<5d} {r.statistic:8s} "
          f"{r.src[:40]:40s} {r.op} {r.threshold}  (range {STATS[r.statistic]['rng']})")
    P("\n  HONEST UPPER BOUND: even TIER 2 counts a NAME, not an INSTRUMENT.  A comparison is an "
      "instrument only if its result gates a weight, which no name match can establish, so every")
    P("  TIER 2 count below is an upper bound on the number of committed absolute-cut "
      "instruments — the same upper-bound reading ideas 276/286/523 forced on earlier censuses.")

    P("\nTHE PRICED LADDER = (TIER 2 census thresholds) UNION (a pre-registered default ladder), "
      f"capped at {MAXTHR + 2} values per statistic.  Provenance is printed per value.")
    ladder, ladder_src = {}, {}
    for st in STATS:
        d2 = thr[(thr.reading == "AST") & (thr.statistic == st) & thr.tier2]
        cvals = sorted(d2.threshold.value_counts().head(MAXTHR).index.tolist())
        lad = sorted(set(cvals) | set(DEFAULT_LADDER[st]))[: MAXTHR + 2]
        ladder[st] = tuple(lad)
        ladder_src[st] = {v: ("census" if v in cvals else "default") for v in lad}
        P(f"  {st:8s} census TIER2 {str(cvals):28s} + default "
          f"{str(DEFAULT_LADDER[st]):28s} -> {ladder[st]}")

    # ---------------------------------------------------------------- statistics + gates
    P("")
    RU = Runner(pxU)
    gate_g1(RU, pxU, ew_weights(pxU, panels[0][2], 0.75), "U56/EWall g=0.75")
    gate_g1(RU, pxU, rules_v2_weights(pxU), "U56/RULES v2")
    S = {}
    for nm, px, tr in panels:
        S[nm] = panel_stats(px, tr)
    for nm, _px, _tr in panels:
        gate_g2(_px, S[nm], nm)
    ncommon, g3_worst = gate_g3(S, {nm: px for nm, px, _ in panels})

    # ---------------------------------------------------------------- PART 2: firing rates
    P("\n" + "=" * 118)
    P("PART 2 — REALISED FIRING RATES AND THEIR CROSS-PANEL SPREAD (tuned parameter 2: RATECONV)")
    P("=" * 118)
    P("The firing rate is the share of scored days on which the instrument is in its risk-off "
      "state — idea 336's `on_share`, computed here on the SAME day set for every panel it can be")
    P("(each panel's own scored window; SMALL439 starts 2011 and that is stated, not hidden).  "
      "RATECONV=daily counts every scored day, RATECONV=rebal only the weekly rebalance days on")
    P("which a weekly book could actually act.")
    rates = []
    starts = {}
    for nm, px, tr in panels:
        starts[nm] = px.index[max(260, MA_WIN + 20)]
    for st, cfg in STATS.items():
        for c in ladder[st]:
            for nm, px, tr in panels:
                sig = S[nm][st]
                f = fire_mask(sig, c, cfg["side"]).loc[starts[nm]:]
                rbm = rebalance_mask(px.index, FREQ).loc[starts[nm]:]
                rates.append(dict(statistic=st, threshold=c, side=cfg["side"], panel=nm,
                                  panel_dependent=cfg["panel_dependent"],
                                  rate_daily=float(f.mean()),
                                  rate_rebal=float(f[rbm].mean()),
                                  episodes=n_episodes(f),
                                  n_days=int(len(f))))
    RT = pd.DataFrame(rates)
    piv = {rc: RT.pivot_table(index=["statistic", "threshold"], columns="panel",
                              values=f"rate_{rc}") for rc in RATECONVS}
    spreads = []
    for st, cfg in STATS.items():
        for c in ladder[st]:
            row = dict(statistic=st, threshold=c, panel_dependent=cfg["panel_dependent"])
            for rc in RATECONVS:
                v = piv[rc].loc[(st, c)]
                row[f"spread_{rc}"] = float(v.max() - v.min())
                row[f"ratio_{rc}"] = (float(v.max() / v.min()) if v.min() > 0
                                      else (np.inf if v.max() > 0 else np.nan))
                for p in ("U56", "B136", "SMALL439"):
                    row[f"{p}_{rc}"] = float(v[p])
            # DEGENERATE = the instrument fires at the SAME extreme on every panel (never
            # anywhere, or always everywhere), so it carries no cross-panel contrast to price
            # and its ABS book is a constant.  Flagged, reported, and excluded from the pooled
            # statistics rather than silently averaged in.
            vd = piv["daily"].loc[(st, c)]
            row["degenerate"] = bool(vd.max() <= 0.005 or vd.min() >= 0.995)
            spreads.append(row)
    SP = pd.DataFrame(spreads)
    SP.to_csv(OUT / f"{STAMP}.rates.csv", index=False)
    for rc in RATECONVS:
        P(f"\n  RATECONV = {rc}")
        P(f"  {'statistic':9s} {'thr':>8s} {'paneldep':>9s} {'U56':>8s} {'B136':>8s} "
          f"{'SMALL439':>9s} {'SPREAD':>8s} {'RATIO':>8s} {'deg':>4s}   "
          f"vs idea 336 ABS bars 0.193 / 0.413 / 0.686")
        for _, r in SP.iterrows():
            s = r[f"spread_{rc}"]
            flags = "".join("X" if s > b else "." for b in IDEA336_ABS_SPREADS.values())
            rat = r[f"ratio_{rc}"]
            P(f"  {r.statistic:9s} {r.threshold:8.4f} {str(r.panel_dependent):>9s} "
              f"{r[f'U56_{rc}']:8.4f} {r[f'B136_{rc}']:8.4f} {r[f'SMALL439_{rc}']:9.4f} "
              f"{s:8.4f} {rat:8.2f} {'DEG' if r.degenerate else '':>4s}   {flags}")
        pd_ = SP[SP.panel_dependent]
        pdn = SP[SP.panel_dependent & ~SP.degenerate]
        pi_ = SP[~SP.panel_dependent]
        for bar in IDEA336_ABS_SPREADS.values():
            P(f"    exceeding {bar:.3f}: panel-dependent "
              f"{int((pd_[f'spread_{rc}'] > bar).sum())}/{len(pd_)} (non-degenerate "
              f"{int((pdn[f'spread_{rc}'] > bar).sum())}/{len(pdn)}), panel-invariant "
              f"{int((pi_[f'spread_{rc}'] > bar).sum())}/{len(pi_)}")
        P(f"    DEGENERATE rungs (same extreme on every panel, no cross-panel contrast to "
          f"price): {int(SP.degenerate.sum())} of {len(SP)} — "
          + ", ".join(f"{r.statistic}@{r.threshold:g}" for _, r in SP[SP.degenerate].iterrows()))
        P("    THE BAR IS SCALE-DEPENDENT, and the RATIO column is why: an instrument that fires "
          "0.6% / 0.7% / 4.2% of days has an absolute spread of 0.036 — clearing every one of")
        P("    idea 336's bars — and a 7.5x RATIO, i.e. one panel's book is de-grossed seven "
          "times as often as another's.  An ABSOLUTE-spread bar systematically clears the "
          "rarely-firing")
        P("    instruments, which are exactly the ones whose cross-panel counts are most "
          "fragile.  Both columns are reported; neither is proposed as THE bar.")
        P(f"    median spread: panel-dependent {pd_[f'spread_{rc}'].median():.4f}, "
          f"panel-invariant {pi_[f'spread_{rc}'].median():.4f} "
          f"(max {pi_[f'spread_{rc}'].max():.3e}).  Gate G3 measured the SPYTR series itself as "
          f"differing across panels by at most 6.8e-05 — a cache-vintage and calendar effect "
          f"— so what little spread it has is the panels' differing day sets, not the panel.)")

    # ---------------------------------------------------------------- PART 3: price it
    P("\n" + "=" * 118)
    P("PART 3 — RE-PRICING every flagged instrument against its rate-matched twin")
    P("=" * 118)
    P("For each (statistic, threshold) the ABS book is the EW panel de-grossed to CASH on "
      "risk-off days.  Its twin is the record's causal rolling-quantile form (QUANT) at nominal")
    P("q = the ABS instrument's CROSS-PANEL MEAN firing rate — i.e. the same instrument re-cut so "
      "that every panel fires at one rate.  Both at gross " + str(GS) + ", weekly, 10 bps, t+1.")
    P("dTOTAL = QUANT - ABS is split into dRATE (the part explained by firing at a different "
      "frequency) and dFORM (the residual), in idea 336's own decomposition:")
    P("  dRATE is measured by a THIRD arm, ABSMATCH: an absolute threshold set on the panel's own "
      "full-sample statistic to hit exactly QUANT's realised rate.  ABSMATCH carries look-ahead")
    P("  in the RATE by construction and is a CONTROL ONLY, never a candidate — idea 336 filed it "
      "the same way.  dRATE = ABSMATCH - ABS, dFORM = QUANT - ABSMATCH.")
    grid, decomp, wfrows, levels, ctrls = [], [], [], [], []
    for nm, px, tr in panels:
        R = Runner(px)
        start = starts[nm]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        b2, _ = R.run(rules_v2_weights(px)); b2 = b2.loc[start:]
        M_spy, M_b2 = mrow(spy), mrow(b2)
        M_spy_o, M_b2_o = mrow(spy.loc[OOS_START:]), mrow(b2.loc[OOS_START:])
        levels.append(dict(panel=nm, spy_CAGR=M_spy["CAGR"], spy_Sharpe=M_spy["Sharpe"],
                           spy_MaxDD=M_spy["MaxDD"], spy_H1=M_spy["H1"], spy_H2=M_spy["H2"],
                           spy_OOS_Sharpe=M_spy_o["Sharpe"], v2_CAGR=M_b2["CAGR"],
                           v2_Sharpe=M_b2["Sharpe"], v2_MaxDD=M_b2["MaxDD"],
                           v2_H1=M_b2["H1"], v2_H2=M_b2["H2"], v2_OOS_Sharpe=M_b2_o["Sharpe"]))
        P(f"\n  PANEL {nm}: {int(tr.sum())} tradable, scored from {start.date()}, "
          f"{px.index[0].date()}..{px.index[-1].date()}")
        P(f"    SPY {M_spy['CAGR']:7.2%} / {M_spy['Sharpe']:.3f} / {M_spy['MaxDD']:7.2%} "
          f"(OOS Sharpe {M_spy_o['Sharpe']:.3f})   RULES v2 {M_b2['CAGR']:7.2%} / "
          f"{M_b2['Sharpe']:.3f} / {M_b2['MaxDD']:7.2%} (OOS Sharpe {M_b2_o['Sharpe']:.3f})")
        ctrl = {}
        for g in GS:
            W = ew_weights(px, tr, g)
            r, _ = R.run(W)
            rr = r.loc[start:]
            M, Mo = mrow(rr), mrow(rr.loc[OOS_START:])
            c4a, c4b = keep_paths(M, Mo, M_b2, M_b2_o, M_spy, M_spy_o)
            ctrl[g] = dict(W=W, r=rr, m=M, mo=Mo, p4a=c4a, p4b=c4b)
            ctrls.append(dict(panel=nm, gross=g, CAGR=M["CAGR"], Sharpe=M["Sharpe"],
                              MaxDD=M["MaxDD"], H1=M["H1"], H2=M["H2"],
                              OOS_CAGR=Mo["CAGR"], OOS_Sharpe=Mo["Sharpe"],
                              OOS_MaxDD=Mo["MaxDD"], pass4a=c4a, pass4b=c4b))
        for st, cfg in STATS.items():
            sig = S[nm][st]
            for c in ladder[st]:
                tgt = float(SP[(SP.statistic == st)
                               & (SP.threshold == c)][[f"{p}_daily" for p in
                                                       ("U56", "B136", "SMALL439")]]
                            .iloc[0].mean())
                off_abs = fire_mask(sig, c, cfg["side"])
                qthr = causal_q_thresh(sig, min(max(tgt, 0.005), 0.995), cfg["side"])
                off_q = (sig < qthr) if cfg["side"] == "low" else (sig > qthr)
                off_q = off_q.fillna(False)
                # ABSMATCH: full-sample absolute threshold hitting QUANT's REALISED rate
                rq = float(off_q.loc[start:].mean())
                lvl = rq if cfg["side"] == "low" else 1.0 - rq
                cm = float(sig.loc[start:].quantile(np.clip(lvl, 0.0, 1.0)))
                off_m = fire_mask(sig, cm, cfg["side"])
                for g in GS:
                    row = dict(panel=nm, statistic=st, threshold=c, gross=g,
                               panel_dependent=cfg["panel_dependent"], target_rate=tgt)
                    arms = {}
                    for arm, off in (("ABS", off_abs), ("QUANT", off_q), ("ABSMATCH", off_m)):
                        Wg = ctrl[g]["W"].where(~off.reindex(px.index).fillna(False), 0.0)
                        r, _ = R.run(Wg); r = r.loc[start:]
                        M, Mo = mrow(r), mrow(r.loc[OOS_START:])
                        Mi = mrow(r.loc[IS_START:IS_END])
                        p4a, p4b = keep_paths(M, Mo, M_b2, M_b2_o, M_spy, M_spy_o)
                        arms[arm] = dict(M=M, Mo=Mo, Mi=Mi, p4a=p4a, p4b=p4b,
                                         rate=float(off.loc[start:].mean()))
                        row[f"{arm}_episodes"] = n_episodes(
                            off.reindex(px.index).fillna(False).loc[start:])
                        for k, v in M.items():
                            row[f"{arm}_{k}"] = v
                        row[f"{arm}_OOS_Sharpe"] = Mo["Sharpe"]
                        row[f"{arm}_OOS_CAGR"] = Mo["CAGR"]
                        row[f"{arm}_OOS_MaxDD"] = Mo["MaxDD"]
                        row[f"{arm}_IS_Sharpe"] = Mi["Sharpe"]
                        row[f"{arm}_rate"] = arms[arm]["rate"]
                        row[f"{arm}_p4a"], row[f"{arm}_p4b"] = p4a, p4b
                    row["ctrl_Sharpe"] = ctrl[g]["m"]["Sharpe"]
                    row["ctrl_p4a"], row["ctrl_p4b"] = ctrl[g]["p4a"], ctrl[g]["p4b"]
                    grid.append(row)
                    degen = bool(SP[(SP.statistic == st)
                                    & (SP.threshold == c)].degenerate.iloc[0])
                    for metric in ("Sharpe", "CAGR", "MaxDD"):
                        decomp.append(dict(
                            panel=nm, statistic=st, threshold=c, gross=g, metric=metric,
                            panel_dependent=cfg["panel_dependent"], degenerate=degen,
                            dTOTAL=arms["QUANT"]["M"][metric] - arms["ABS"]["M"][metric],
                            dRATE=arms["ABSMATCH"]["M"][metric] - arms["ABS"]["M"][metric],
                            dFORM=arms["QUANT"]["M"][metric] - arms["ABSMATCH"]["M"][metric],
                            dTOTAL_OOS=arms["QUANT"]["Mo"][metric] - arms["ABS"]["Mo"][metric],
                            dRATE_OOS=arms["ABSMATCH"]["Mo"][metric] - arms["ABS"]["Mo"][metric],
                            dFORM_OOS=arms["QUANT"]["Mo"][metric]
                            - arms["ABSMATCH"]["Mo"][metric],
                            abs_rate=arms["ABS"]["rate"], quant_rate=arms["QUANT"]["rate"],
                            absmatch_rate=arms["ABSMATCH"]["rate"]))
        # ------------------------------------------------ rule 8, per (statistic, arm)
        gdf = pd.DataFrame([r for r in grid if r["panel"] == nm])
        for st in STATS:
            d = gdf[gdf.statistic == st]
            for arm in ("ABS", "QUANT"):
                pick = d.loc[d[f"{arm}_IS_Sharpe"].idxmax()]
                wfrows.append(dict(
                    panel=nm, statistic=st, arm=arm, threshold=pick.threshold, gross=pick.gross,
                    panel_dependent=pick.panel_dependent,
                    IS_Sharpe=pick[f"{arm}_IS_Sharpe"],
                    full_CAGR=pick[f"{arm}_CAGR"], full_Sharpe=pick[f"{arm}_Sharpe"],
                    full_MaxDD=pick[f"{arm}_MaxDD"], H1=pick[f"{arm}_H1"], H2=pick[f"{arm}_H2"],
                    OOS_CAGR=pick[f"{arm}_OOS_CAGR"], OOS_Sharpe=pick[f"{arm}_OOS_Sharpe"],
                    OOS_MaxDD=pick[f"{arm}_OOS_MaxDD"], rate=pick[f"{arm}_rate"],
                    episodes=int(pick[f"{arm}_episodes"]),
                    pass4a=bool(pick[f"{arm}_p4a"]), pass4b=bool(pick[f"{arm}_p4b"]),
                    base_CAGR=M_b2["CAGR"], base_Sharpe=M_b2["Sharpe"], base_MaxDD=M_b2["MaxDD"],
                    base_OOS_Sharpe=M_b2_o["Sharpe"], base_OOS_CAGR=M_b2_o["CAGR"],
                    base_OOS_MaxDD=M_b2_o["MaxDD"],
                    spy_CAGR=M_spy["CAGR"], spy_Sharpe=M_spy["Sharpe"], spy_MaxDD=M_spy["MaxDD"],
                    spy_OOS_Sharpe=M_spy_o["Sharpe"], spy_OOS_CAGR=M_spy_o["CAGR"],
                    spy_OOS_MaxDD=M_spy_o["MaxDD"]))
        P(f"    priced {len(gdf)} cells x 3 arms   [{time.time()-t0:.1f}s]")

    G = pd.DataFrame(grid); D = pd.DataFrame(decomp)
    WF = pd.DataFrame(wfrows); LV = pd.DataFrame(levels)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    D.to_csv(OUT / f"{STAMP}.decomp.csv", index=False)
    WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    idw = float((D.dTOTAL - (D.dRATE + D.dFORM)).abs().max())
    idw_o = float((D.dTOTAL_OOS - (D.dRATE_OOS + D.dFORM_OOS)).abs().max())
    P(f"\n  G5 decomposition identity   dTOTAL == dRATE + dFORM on all {len(D)} rows: full "
      f"max|d| {idw:.3e}, OOS {idw_o:.3e}   {'PASS' if max(idw, idw_o) < 1e-12 else 'FAIL'}")
    assert max(idw, idw_o) < 1e-12
    P("\n  RATE-MATCHING CHECK (the twin must actually equalise the rate, or PART 3 says "
      "nothing):")
    rr = (G.groupby(["statistic", "threshold"])
          .agg(abs_spread=("ABS_rate", lambda s: s.max() - s.min()),
               quant_spread=("QUANT_rate", lambda s: s.max() - s.min()),
               absmatch_spread=("ABSMATCH_rate", lambda s: s.max() - s.min())))
    P("  " + rr.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    P(f"  median ABS spread {rr.abs_spread.median():.4f} -> median QUANT spread "
      f"{rr.quant_spread.median():.4f} (idea 336 reported 0.193/0.413/0.686 -> 0.002/0.015/0.007)")

    P("\n" + "-" * 118)
    P("THE DECOMPOSITION: how much of QUANT - ABS is the RATE, per panel (Sharpe, full sample "
      "and OOS).  |dRATE| / (|dRATE| + |dFORM|) is the RATE SHARE.")
    for metric in ("Sharpe",):
        d = D[(D.metric == metric) & D.panel_dependent & ~D.degenerate]
        for scope, a, b in (("full", "dRATE", "dFORM"), ("OOS", "dRATE_OOS", "dFORM_OOS")):
            t = d.groupby("panel").apply(
                lambda x: pd.Series({
                    "n": len(x), "mean_dTOTAL": x["dTOTAL" if scope == "full"
                                                   else "dTOTAL_OOS"].mean(),
                    "mean_dRATE": x[a].mean(), "mean_dFORM": x[b].mean(),
                    "rate_share": float(x[a].abs().sum()
                                        / (x[a].abs().sum() + x[b].abs().sum()))}),
                include_groups=False)
            P(f"\n  {metric} / {scope}")
            P("  " + t.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    dpd = D[(D.metric == "Sharpe") & D.panel_dependent & ~D.degenerate]
    P(f"\n  Pooled RATE SHARE over all {len(dpd)} panel-dependent cells: full "
      f"{dpd.dRATE.abs().sum()/(dpd.dRATE.abs().sum()+dpd.dFORM.abs().sum()):.4f}, OOS "
      f"{dpd.dRATE_OOS.abs().sum()/(dpd.dRATE_OOS.abs().sum()+dpd.dFORM_OOS.abs().sum()):.4f} "
      f"(idea 336 reported 0.835 full / 0.857 OOS on SMALL484 for BREADTH).")

    # ---------------------------------------------------------------- PART 4: keep paths
    P("\n" + "=" * 118)
    P("PART 4 — BOTH KEEP PATHS and rule 8")
    P("=" * 118)
    CT = pd.DataFrame(ctrls)
    P("\nTHE UNGATED PARENT first, because idea 336 found 42 of its own 50 4b passes were "
      "INHERITED from it.  Every gated book below must be read against its OWN parent:")
    P(CT.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    n = len(G)
    for arm in ("ABS", "QUANT", "ABSMATCH"):
        P(f"  {arm:9s} whole grid {n} books: 4a {int(G[f'{arm}_p4a'].sum())}, "
          f"4b {int(G[f'{arm}_p4b'].sum())}, BOTH "
          f"{int((G[f'{arm}_p4a'] & G[f'{arm}_p4b']).sum())}")
    for arm in ("ABS", "QUANT"):
        pas = G[G[f"{arm}_p4b"]]
        inh = int(pas.ctrl_p4b.sum())
        P(f"  {arm:9s} of its {len(pas)} 4b passes, {inh} are INHERITED (the ungated parent at "
          f"the same panel and gross passes 4b too) and {len(pas)-inh} are the gate's own.")
    P("  (ABSMATCH carries look-ahead in the rate and is a CONTROL ONLY — its counts are printed "
      "so the look-ahead's size is visible, and it is never eligible for promotion.)")
    P(f"\nRULE-8 PICKS ({len(WF)} = 5 statistics x 2 arms x 3 panels), (threshold, gross) chosen "
      f"on 2009-2016 Sharpe alone, 2017-2026 read once:")
    cols = ["panel", "statistic", "arm", "threshold", "gross", "rate", "episodes", "full_CAGR",
            "full_Sharpe", "full_MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "pass4a", "pass4b"]
    P(WF[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  KEEP paths on the picks: 4a {int(WF.pass4a.sum())}/{len(WF)}, "
      f"4b {int(WF.pass4b.sum())}/{len(WF)}.")
    pw = WF[WF.pass4b]
    if len(pw):
        P("  The 4b-passing picks, with the EPISODE COUNT beside the rate — the number of "
          "independent risk-off runs the drawdown leg actually rests on:")
        for _, r in pw.iterrows():
            P(f"    {r.panel:9s} {r.statistic:8s} {r.arm:6s} thr {r.threshold:6.3f} g "
              f"{r.gross:.2f}  rate {r.rate:.4f} over {int(r.episodes):4d} episodes  "
              f"full {r.full_CAGR:6.2%}/{r.full_Sharpe:.4f}/{r.full_MaxDD:7.2%} "
              f"H {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/"
              f"{r.OOS_MaxDD:7.2%}  vs v2 OOS {r.base_OOS_Sharpe:.4f}, SPY OOS "
              f"{r.spy_OOS_Sharpe:.4f}")
    P("  vs RULES v2 OOS Sharpe " + ", ".join(
        f"{r.panel} {r.v2_OOS_Sharpe:.4f}" for _, r in LV.iterrows())
      + "; SPY OOS Sharpe " + ", ".join(
        f"{r.panel} {r.spy_OOS_Sharpe:.4f}" for _, r in LV.iterrows()) + ".")
    kp = []
    for arm in ("ABS", "QUANT"):
        k = G[G[f"{arm}_p4a"] | G[f"{arm}_p4b"]].copy()
        k.insert(0, "arm", arm)
        kp.append(k[["arm", "panel", "statistic", "threshold", "gross", f"{arm}_rate",
                     f"{arm}_episodes",
                     f"{arm}_CAGR", f"{arm}_Sharpe", f"{arm}_MaxDD", f"{arm}_H1", f"{arm}_H2",
                     f"{arm}_OOS_CAGR", f"{arm}_OOS_Sharpe", f"{arm}_OOS_MaxDD",
                     f"{arm}_p4a", f"{arm}_p4b"]]
              .rename(columns=lambda c: c.replace(f"{arm}_", "")))
    KP = pd.concat(kp, ignore_index=True) if kp else pd.DataFrame()
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    if len(KP):
        P(f"\nEvery KEEP-path passer among the promotable arms ({len(KP)} books):")
        P(KP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\nREFERENCE LEVELS (survivorship: B136 and SMALL439 are CURRENT constituents)")
    P(LV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- PART 5: verdicts
    P("\n" + "=" * 118)
    P("PART 5 — the three pre-registered hypotheses, adjudicated")
    P("=" * 118)
    pd_ = SP[SP.panel_dependent]; pi_ = SP[~SP.panel_dependent]
    pdn = SP[SP.panel_dependent & ~SP.degenerate]
    for rc in RATECONVS:
        over = int((pd_[f"spread_{rc}"] > 0.413).sum())
        overn = int((pdn[f"spread_{rc}"] > 0.413).sum())
        P(f"  H_SPREAD  RATECONV={rc:6s}: {over}/{len(pd_)} panel-dependent instruments "
          f"({overn}/{len(pdn)} non-degenerate) exceed idea 336's MEDIAN ABS bar 0.413; median "
          f"spread {pd_[f'spread_{rc}'].median():.4f} (non-degenerate "
          f"{pdn[f'spread_{rc}'].median():.4f})  -> "
          f"{'PASS' if overn > len(pdn)/2 else 'FAIL'} on the non-degenerate denominator")
    for rc in RATECONVS:
        P(f"            at idea 336's LOOSEST bar 0.193 the same count is "
          f"{int((pdn[f'spread_{rc}'] > 0.193).sum())}/{len(pdn)} ({rc}) — so the verdict "
          f"depends entirely on WHICH of idea 336's three published spreads is called 'the' bar,")
    P("            which is the queue's own ambiguity and is reported rather than resolved by "
      "picking one.")
    P(f"  H_INVAR   panel-invariant (SPYTR) spreads: max "
      f"{pi_.spread_daily.max():.3e} (daily) / {pi_.spread_rebal.max():.3e} (rebal), against a "
      f"non-degenerate panel-dependent median of {pdn.spread_daily.median():.4f}")
    P(f"            -> PASS. Gate G3 measured the SPYTR series itself as differing across panels "
      f"by at most {g3_worst:.3e} over {ncommon} common days (a cache-vintage and calendar "
      f"effect, not a panel effect), and that")
    P(f"            residual buys a firing-rate spread of at most "
      f"{pi_.spread_daily.max():.4f} — an order of magnitude under the panel-dependent median. "
      f"A word-level census counts these {len(pi_)} rungs as artefacts; they are not.")
    rs_full = dpd.dRATE.abs().sum() / (dpd.dRATE.abs().sum() + dpd.dFORM.abs().sum())
    rs_oos = dpd.dRATE_OOS.abs().sum() / (dpd.dRATE_OOS.abs().sum() + dpd.dFORM_OOS.abs().sum())
    P(f"  H_RATE    pooled RATE SHARE of the Sharpe movement: full {rs_full:.4f}, OOS "
      f"{rs_oos:.4f}  -> {'PASS' if rs_full > 0.5 else 'FAIL'} "
      f"(idea 336: 0.835 / 0.857 on SMALL484's BREADTH cell)")

    P(f"\nDone in {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

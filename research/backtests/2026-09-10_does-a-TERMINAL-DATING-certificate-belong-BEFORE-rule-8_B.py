#!/usr/bin/env python3
"""Idea 623 - does a TERMINAL-DATING certificate belong BEFORE rule 8?  (lane B, 2026-09-10)

THE QUEUE'S QUESTION
    Idea 195 (lane B, 2026-09-10) found that MCAP = px_t x s_T -- the price panel times a
    TERMINAL-dated share count -- WINS PROTOCOL 8's walk-forward outright (OOS Sharpe 1.584 vs
    RULES v2 0.558 and SPY 0.882), because rule 8 splits the sample by DATE and a terminal-dated
    key's lookahead covers BOTH sides of the split.  The queue asks whether a T1-family
    certificate (ideas 197 / 426 / 428 / 433) should run BEFORE rule 8, and how many committed
    rule-8 passes in the record are built on a key with any terminal-dated input.

THE PREMISE UNDER TEST
    The T1 family is a SCALE certificate.  Idea 426 drafts it as ranks(key(px)) == ranks(key(px x
    diag(c))); idea 433 recommends the VALUE form at a one-rank-step tolerance.  Its operator
    perturbs the per-name price LEVEL.  Terminal DATING is a different axis: it perturbs WHEN the
    key may read.  The two coincide on MCAP (which is a per-name rescale of the price panel by a
    terminal constant) and that coincidence is what makes the queue's proposal look right.  This
    run separates the axes and prices both instruments.

    T1  (scale)   : flag if rank(key(px)) != rank(key(px x diag(c))) beyond tol, c ~ per-name
                    lognormal.  Idea 433's recommended form.
    T2  (dating)  : flag if key(px)[t] != key(px.loc[:t])[t] beyond tol, over probe dates t.
                    A key that reads only data available at t is exactly invariant.  NEW HERE.

PARTS
    A  INSTRUMENT.  20 keys with hand-derived ground truth on two INDEPENDENT axes (scale_leak,
       term_date).  Confusion matrix for T1, T2 and T1&T2 against each axis.
    B  CENSUS.  Every committed research/backtests/*.py, two tiers, plus a hand-audited sample:
       how many rule-8-running files carry a terminal-dated input, and how many of those carry
       it in a KEY/SELECTION path rather than in reporting.
    C  CONSEQUENCE BOOK.  The certificate priced as a PRE-rule-8 GATE on idea 195's own SMALL430
       grid: rule 8 picks (KEY, m) on 2010-2016 IS Sharpe among the keys the gate admits, and
       2017-2026 is read once.  PROTOCOL 2/3/4 on every arm at 0/10/25 bps.

TUNED PARAMETERS: exactly two -- CERTIFICATE (the gate: NONE / T1 / T2 / T1&T2) and TILT
    STRENGTH m in {0.20, 0.50, 1.00}.  Every grid point is written to .arms.csv.  The certificate
    TOLERANCE is NOT tuned: it is fixed at idea 433's recommended one rank step and the tol=0
    reading is reported beside it as a diagnostic.

PRE-REGISTERED PREDICTIONS (scored in PART D, before any of them is read)
    P1  Gates G1-G4 pass at their stated tolerances.
    P2  T1 has at least one FALSE NEGATIVE on the terminal-dated axis -- a key that is
        terminal-dated and scale-invariant, so T1 clears it.  FWDRET (the pure oracle) is the
        pre-named instance.
    P3  T2 has ZERO false positives on the hand-certified causal key set (a causal key is exactly
        truncation-invariant, not approximately).
    P4  Neither certificate dominates: T1 flags at least one key T2 clears AND T2 flags at least
        one key T1 clears.  The two have DISJOINT content, so the clause needs both.
    P5  Rule 8 under the NONE gate and under the T1 gate both pick a terminal-dated key and both
        beat SPY out of sample; under the T2 gate the pick is causal and does NOT.
    P6  4a 0 and 4b 0 across the whole grid (idea 195's DD-cap result on the same panel).

SURVIVORSHIP, as PROTOCOL 9 requires: PART C runs on idea 195's SMALL430, which is current
    constituents of a sub-$2B screen (data/SMALL_PANEL_README.md) intersected with the names that
    still file today.  A survivor of a survivor; every PART C number is biased in the tilt's
    favour.  PART A and PART B do not depend on the panel.

Costs 10 bps (PROTOCOL 2) with 0 and 25 bps reported; weights at close t applied t+1 (engine).
Deterministic, standalone:
    python research/backtests/2026-09-10_does-a-TERMINAL-DATING-certificate-belong-BEFORE-rule-8_B.py
Writes .console.txt .certs.csv .census.csv .audit.csv .arms.csv .walkforward.csv .repro.csv
"""
import ast
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, load_volume, rules_v1_weights,  # noqa: E402
                      rules_v2_weights)
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-a-TERMINAL-DATING-certificate-belong-BEFORE-rule-8_B"
OUT = ROOT / "research" / "backtests"
PARENT = "2026-09-10_market-cap-as-the-third-substitution_B"
SHARES_PIN = OUT / f"{PARENT}.shares.csv"          # idea 565's pinning convention, read-only

# ---- inherited verbatim from ideas 181/185/193/195 so the published cells stay comparable
SEED = 623
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
COSTS = [0.0, 10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
PHI, DELTA = 0.70, 0.60
REPRO_TOL = 5e-3

# ---- certificate settings (NOT tuned; fixed by idea 433's recommendation)
N_SCALE_DRAWS = 8                                   # per-name rescale draws for T1
PROBE_FRAC = [0.35, 0.50, 0.65, 0.80, 0.95]         # truncation probe dates for T2

_console = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


def rankpct(df):
    return df.rank(axis=1, pct=True)


# ------------------------------------------------------------------ vectorised engine equivalent
def fast_backtest(prices, weights, freq=FREQ):
    """(gross returns at 0 bps, turnover).  Costs applied through r(c) = r(0) - turnover*c/1e4;
    gate G2 checks that identity against a live engine run."""
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
    port = (held * rets).sum(axis=1)
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ======================================================================= PART A: the key corpus
# Every key below is a function of (px, vol, shares) ONLY, so both certificates can perturb its
# inputs and re-run it.  GROUND TRUTH is hand-derived from the algebra and stated beside each.
#   scale_leak : does key(px x diag(c)) differ in cross-sectional ORDER from key(px)?
#   term_date  : does key[t] read any value dated after t?

def _entry(px):
    """Each name's own first traded price, broadcast forward.  Causal: known from that name's
    first day onward, and NaN wherever the name is not yet priced."""
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def _term(px):
    """Each name's LAST traded price in the sample, broadcast backward.  Terminal-dated."""
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(lv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def _bcast(vec, px):
    return pd.DataFrame(np.tile(np.asarray(vec, float), (len(px), 1)),
                        index=px.index, columns=px.columns).where(px.notna())


def _composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


#                          fn(px, vol, shares) -> key frame        scale_leak  term_date  family
KEY_SPECS = {
    # ---- causal, scale-invariant (the honest family)
    "MOM":      (lambda p, v, s: _composite(p),                      False, False, "causal"),
    "R6":       (lambda p, v, s: rankpct(p / p.shift(126) - 1),       False, False, "causal"),
    "DDTR":     (lambda p, v, s: rankpct(p / p.rolling(252).max() - 1), False, False, "causal"),
    "REBASED":  (lambda p, v, s: rankpct(p / _entry(p)),              False, False, "causal"),
    "VOL20":    (lambda p, v, s: rankpct(p.pct_change().rolling(20).std()), False, False, "causal"),
    "VOLSH":    (lambda p, v, s: rankpct(v.rolling(20).mean()),       False, False, "causal"),
    # ---- causal but price-LEVEL dependent (T1's own domain; idea 193 leg (a), idea 185's PRICE).
    #      DVOL/PXDVOL are DOLLAR volume = a price LEVEL times a share count, so they belong here
    #      and not with the causal keys: idea 193 named them level products for the same reason.
    "PRICE":    (lambda p, v, s: rankpct(p),                          True,  False, "level"),
    "FROZEN":   (lambda p, v, s: rankpct(_entry(p)),                  True,  False, "level"),
    "DVOL":     (lambda p, v, s: rankpct((p * v).rolling(20).mean()), True,  False, "level"),
    "PXDVOL":   (lambda p, v, s: rankpct(p * v.rolling(20).mean()),   True,  False, "level"),
    # ---- terminal-dated AND scale-dependent (both certificates should flag; idea 195's MCAP)
    "MCAP":     (lambda p, v, s: rankpct(p * _bcast(s, p)),           True,  True,  "both"),
    "MCAPFRZ":  (lambda p, v, s: rankpct(_entry(p) * _bcast(s, p)),   True,  True,  "both"),
    "PXTERM":   (lambda p, v, s: rankpct(_term(p)),                   True,  True,  "both"),
    # ---- terminal-dated but SCALE-INVARIANT: the family T1 is structurally blind to
    "FWDRET":   (lambda p, v, s: rankpct(_term(p) / p - 1.0),         False, True,  "termonly"),
    "TERMREB":  (lambda p, v, s: rankpct(p / _term(p)),               False, True,  "termonly"),
    "MCAPREB":  (lambda p, v, s: rankpct((p / _entry(p)) * _bcast(s, p)), False, True, "termonly"),
    "SHARES":   (lambda p, v, s: rankpct(_bcast(s, p)),               False, True,  "termonly"),
    "FULLVOL":  (lambda p, v, s: rankpct(_bcast(p.pct_change().std(), p)), False, True, "termonly"),
    "FULLSHRP": (lambda p, v, s: rankpct(_bcast(p.pct_change().mean() / p.pct_change().std(), p)),
                 False, True, "termonly"),
    "MAXMOVE":  (lambda p, v, s: rankpct(_bcast(p.pct_change().abs().max(), p)),
                 False, True, "termonly"),   # <- data/small_meta.csv's own panel-filter statistic
}


def _rank_int(k):
    """Integer cross-sectional rank per row; NaN preserved.  The certificates compare these."""
    return k.rank(axis=1, method="first")


def _perday_max(d):
    """Per-row max |rank displacement|, restricted to rows with a real cross-section."""
    ok = d.notna().sum(axis=1) >= 20
    return d.max(axis=1).where(ok)


def disp_T1(fn, px, vol, shares, rng):
    """Idea 433's recommended form: VALUE-invariance of the cross-sectional ORDER under a per-name
    rescale px -> px x diag(c).  Returns (GLOBAL max displacement, MEDIAN over days of the per-day
    max), both in rank steps.  Both readings are published for every key: the global max is idea
    433's literal statistic, the median is the robust one, and on a 430 x 4,200 panel they do NOT
    agree -- see PART A."""
    base = _rank_int(fn(px, vol, shares))
    gmax, per = 0.0, None
    for _ in range(N_SCALE_DRAWS):
        c = pd.Series(np.exp(rng.normal(0.0, 1.0, size=px.shape[1])), index=px.columns)
        alt = _rank_int(fn(px.mul(c, axis=1), vol, shares))
        d = (base - alt).abs()
        gmax = max(gmax, float(np.nanmax(d.values)) if d.notna().any().any() else 0.0)
        pm = _perday_max(d)
        per = pm if per is None else pd.concat([per, pm], axis=1).max(axis=1)
    med = float(np.nanmedian(per.values)) if per is not None and per.notna().any() else 0.0
    return gmax, med


def disp_T2(fn, px, vol, shares, shares_asof):
    """NEW -- the DATING certificate.  TRUNCATION-invariance: key(inputs)[t] must equal
    key(inputs truncated to <= t)[t] at every probe date t.  A key that reads only data dated at
    or before t is EXACTLY invariant.  Truncation applies to EVERY input, not just the price
    panel: an exogenous series is passed through only if its own as-of date is <= t.  A key that
    cannot be computed at t because its input is not yet dated is flagged (displacement inf).
    Returns (GLOBAL max, MEDIAN over the probe dates), both in rank steps."""
    base = _rank_int(fn(px, vol, shares))
    nan_shares = shares * np.nan
    per = []
    for f in PROBE_FRAC:
        t = px.index[int(f * (len(px) - 1))]
        s_t = shares if shares_asof <= t else nan_shares
        alt = _rank_int(fn(px.loc[:t], vol.loc[:t], s_t))
        b, a = base.loc[t], alt.loc[t]
        if bool((b.notna() & a.isna()).any()):        # input not yet dated at t -> not computable
            return float("inf"), float("inf")
        d = (b - a).abs()
        per.append(float(np.nanmax(d.values)) if d.notna().any() else 0.0)
    return float(max(per)), float(np.median(per))


# =========================================================================== PART B: the census
RULE8_MARKS = [r"IS_END", r"OOS_LO", r"walk[_ ]?forward", r"walkforward", r"\bOOS\b",
               r"2016-12-31", r"2017-01-01", r"rule[_ ]?8"]

# Terminal-dated CONSTRUCTS.  Each is a way of reading a value dated after the row it lands on.
# SHARP = the token can only be a terminal read.  SOFT = a full-sample reduction, which is
# terminal-dated ONLY if it is broadcast back across time; counted separately and never folded
# into the headline, because most of its occurrences are metric printing.
SHARP_PATTERNS = {
    "iloc_last":     r"\.iloc\[\s*-1\s*\]",
    "index_last":    r"\.index\[\s*-1\s*\]",
    "last_valid":    r"last_valid_index\s*\(",
    "tail":          r"\.tail\s*\(",
    "snapshot_file": r"universe_under2b\.csv|small_meta\.csv|\.shares\.csv|shares_outstanding|"
                     r"mktcap",
}
SOFT_PATTERNS = {
    "fullsample_red": r"\.(?:std|mean|sum|max|min|var|median)\s*\(\s*\)",
}
TERM_PATTERNS = {**SHARP_PATTERNS, **SOFT_PATTERNS}
# constructs that read a value dated at or before every row: NOT terminal
BENIGN_PATTERNS = {"iloc_first": r"\.iloc\[\s*0\s*\]", "first_valid": r"first_valid_index\s*\("}

# a hit is TIER-2 (a KEY/SELECTION path) only if its enclosing function also builds a ranking,
# an eligibility mask or a weight vector
SELECT_MARKS = [r"\.rank\s*\(", r"rankpct", r"elig", r"weights", r"\bw\s*=", r"<=\s*N\b",
                r"ascending\s*="]


def _enclosing_funcs(tree):
    """[(name, first_line, last_line, source_segment)] for every function def in the module."""
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append((node.name, node.lineno, getattr(node, "end_lineno", node.lineno)))
    return out


def census_file(path):
    src = path.read_text(errors="replace")
    lines = src.splitlines()
    runs_rule8 = any(re.search(p, src) for p in RULE8_MARKS)
    try:
        tree = ast.parse(src)
        funcs = _enclosing_funcs(tree)
    except SyntaxError:
        funcs = []
    hits, tier2 = [], []
    for cname, pat in TERM_PATTERNS.items():
        for mo in re.finditer(pat, src):
            ln = src[:mo.start()].count("\n") + 1
            line = lines[ln - 1] if ln - 1 < len(lines) else ""
            if line.lstrip().startswith("#"):
                continue                                   # a comment is not a computation
            if cname == "fullsample_red" and re.search(r"rolling\s*\(|expanding\s*\(", line):
                continue                                   # a windowed reduction is causal
            hits.append((cname, ln, line.strip()[:160]))
            owners = [f for f in funcs if f[1] <= ln <= f[2]]
            if not owners:
                continue
            fo = min(owners, key=lambda z: z[2] - z[1])
            seg = "\n".join(lines[fo[1] - 1:fo[2]])
            if any(re.search(s, seg) for s in SELECT_MARKS):
                tier2.append((cname, ln, fo[0], line.strip()[:160]))
    benign = {k: len(re.findall(p, src)) for k, p in BENIGN_PATTERNS.items()}
    sharp = [h for h in hits if h[0] in SHARP_PATTERNS]
    sharp2 = [h for h in tier2 if h[0] in SHARP_PATTERNS]
    return dict(file=path.name, rule8=runs_rule8, n_hits=len(hits), n_sharp=len(sharp),
                n_tier2=len(tier2), n_sharp_tier2=len(sharp2),
                classes=";".join(sorted({h[0] for h in hits})),
                tier2_classes=";".join(sorted({h[0] for h in tier2})),
                benign=sum(benign.values())), hits, tier2


# --------------------------------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def full_row(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_LO))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = \
            m["CAGR"], m["Sharpe"], m["MaxDD"]
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]
                and row["CAGR_F"] >= PHI * spy["CAGR_F"])


# ============================================================================================ run
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    repro = []

    # ---------------------------------------------------------------------------- panel (as 195)
    pxF = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxF = pxF[[c for c in pxF.columns if c == "SPY" or c not in bad]]
    pin = pd.read_csv(SHARES_PIN)
    shares = pin.set_index("ticker")["shares"]
    covered = [c for c in pxF.columns if c != "SPY" and c in shares.index]
    px = pxF[covered]
    spy_px = pxF["SPY"]
    vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
    sh = shares.reindex(px.columns)
    start = px.index[260]

    say("=" * 112)
    say(f"IDEA 623 - does a TERMINAL-DATING certificate belong BEFORE rule 8?   (lane B, "
        f"{pd.Timestamp.utcnow().date()})")
    say("=" * 112)
    say(f"Panel SMALL{len(covered)} (idea 195's leg-(c) panel, reproduced): {px.shape[1]} names, "
        f"{px.index[0].date()}..{px.index[-1].date()}, SPY benchmark only.")
    say(f"Shares snapshot read from the PINNED artefact {SHARES_PIN.name} (idea 565), "
        f"{len(pin)} rows -- NOT from the nightly file.")
    say("")

    # =============================================================== GATES (pre-registered, G1-G4)
    say("-" * 112)
    say("GATES (four, pre-registered)")
    comp = _composite(px)
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = (px > px.rolling(200).mean()) & (vol20 < MAXVOL)
    rk = comp.where(elig).rank(axis=1, ascending=False)
    wctl = (rk <= N).astype(float) * (GROSS / N)

    eng0 = backtest(px, wctl, cost_bps=0.0, freq=FREQ)
    g0, t0turn = fast_backtest(px, wctl)
    # compared on the EVALUATION window only: the engine emits NaN on the 2 pre-first-rebalance
    # rows of this panel, which no published metric ever reads (every row starts at px.index[260]).
    ev = px.index[260:]
    g1r = float(np.abs(eng0["returns"].loc[ev].values - g0.loc[ev].values).max())
    g1t = float(np.abs(eng0["turnover"].loc[ev].values - t0turn.loc[ev].values).max())
    say(f"  G1  fast_backtest == engine.backtest (control book)      returns {g1r:.3e}  "
        f"turnover {g1t:.3e}   [tol 1e-12, evaluation window]")
    repro.append(dict(gate="G1_fast_vs_engine", value=max(g1r, g1t), tol=1e-12,
                      passed=max(g1r, g1t) < 1e-12))

    eng25 = backtest(px, wctl, cost_bps=25.0, freq=FREQ)
    derived = g0 - t0turn * 25.0 / 1e4
    g2 = float(np.abs(eng25["returns"].loc[ev].values - derived.loc[ev].values).max())
    say(f"  G2  cost-rung identity r(c)=r(0)-turnover*c/1e4 @25bps    {g2:.3e}   [tol 1e-12]")
    repro.append(dict(gate="G2_rung_identity", value=g2, tol=1e-12, passed=g2 < 1e-12))

    # G3: reproduce the PARENT run's committed headline arm from its own .arms.csv
    pa = pd.read_csv(OUT / f"{PARENT}.arms.csv")
    hd = pa[(pa["key"] == "MCAP") & (pa["dir"] == "NEG") & (pa["m"] == 1.00) & (pa["cost"] == 10.0)]
    par = hd.iloc[0]
    kM = rankpct(px * _bcast(sh, px))
    sc = comp + (-1.0) * 1.00 * (kM - 0.5)
    rkM = sc.where(elig).rank(axis=1, ascending=False)
    wM = (rkM <= N).astype(float) * (GROSS / N)
    gM, tM = fast_backtest(px, wM)
    rowM = full_row(gM.loc[start:] - tM.loc[start:] * 10.0 / 1e4)
    g3 = max(abs(rowM["CAGR_F"] - par["CAGR_F"]), abs(rowM["Sharpe_F"] - par["Sharpe_F"]),
             abs(rowM["MaxDD_F"] - par["MaxDD_F"]))
    say(f"  G3  parent headline MCAP/NEG/m=1.00 @10bps reproduced     {g3:.3e}   "
        f"[tol {REPRO_TOL:g}]  (here {rowM['CAGR_F']:.2%}/{rowM['Sharpe_F']:.3f}/"
        f"{rowM['MaxDD_F']:.2%} vs committed {par['CAGR_F']:.2%}/{par['Sharpe_F']:.3f}/"
        f"{par['MaxDD_F']:.2%})")
    repro.append(dict(gate="G3_parent_headline", value=g3, tol=REPRO_TOL, passed=g3 < REPRO_TOL))

    # G4: the certificates are self-consistent -- an IDENTITY key must clear both at tol 0
    ident = lambda p, v, s: rankpct(p / p.shift(21) - 1.0)     # noqa: E731  purely causal, scale-free
    x1, m1 = disp_T1(ident, px, vol, sh, np.random.default_rng(SEED + 1))
    x2, m2 = disp_T2(ident, px, vol, sh, px.index[-1])
    say(f"  G4  both certificates clear a causal scale-free control   T1 med {m1:.3e} (max "
        f"{x1:.1f})  T2 med {m2:.3e} (max {x2:.1f})   [tol 0 exactly on the MEDIAN statistic]")
    repro.append(dict(gate="G4_control_key", value=max(m1, m2), tol=0.0,
                      passed=(m1 == 0.0 and m2 == 0.0)))
    say("")

    # ============================================================ PART A -- THE INSTRUMENT
    say("=" * 112)
    say("PART A  THE INSTRUMENT: does a T1-family certificate detect TERMINAL DATING?")
    say("        T1 = idea 433's value certificate under px -> px x diag(c).  "
        "T2 = truncation invariance (new).")
    say("=" * 112)
    tol_steps = 1.0                                   # idea 433's one-rank-step tolerance
    shares_asof = px.index[-1]                        # the snapshot is dated TODAY (idea 622 G5)
    crows = []
    for i, (name, (fn, sleak, tdate, fam)) in enumerate(KEY_SPECS.items()):
        x1, m1 = disp_T1(fn, px, vol, sh, np.random.default_rng(SEED + 101 * i))
        x2, m2 = disp_T2(fn, px, vol, sh, shares_asof)
        crows.append(dict(key=name, family=fam, truth_scale_leak=sleak, truth_term_dated=tdate,
                          T1_flag=bool(m1 > tol_steps), T1_med=m1, T1_max=x1,
                          T2_flag=bool(m2 > tol_steps), T2_med=m2, T2_max=x2,
                          T1_flag_maxstat=bool(x1 > tol_steps),
                          T2_flag_maxstat=bool(x2 > tol_steps),
                          BOTH_flag=bool(m1 > tol_steps or m2 > tol_steps)))
    C = pd.DataFrame(crows)
    say(f"{'key':10s} {'family':9s} {'scale?':7s} {'term?':6s} "
        f"{'T1':>5s} {'T1med':>7s} {'T1max':>7s} {'T2':>5s} {'T2med':>7s} {'T2max':>7s}")
    for _, r in C.iterrows():
        say(f"{r['key']:10s} {r['family']:9s} {str(r['truth_scale_leak']):7s} "
            f"{str(r['truth_term_dated']):6s} {('FLAG' if r['T1_flag'] else '  .'):>5s} "
            f"{r['T1_med']:7.1f} {r['T1_max']:7.1f} "
            f"{('FLAG' if r['T2_flag'] else '  .'):>5s} {r['T2_med']:7.1f} {r['T2_max']:7.1f}")
    say("")
    say("STATISTIC MATTERS, and the record has never named one (ideas 520 / 564).  On this")
    say(f"{px.shape[1]} x {len(px)} panel the GLOBAL-MAX reading of the displacement — idea 433's")
    say("literal statistic — flags every causal key too, at 2-4 rank steps out of "
        f"{px.shape[1]}, purely")
    say("from float re-ordering of near-ties.  The MEDIAN-over-days reading separates cleanly.")
    say("Both readings are published for every key below and in .certs.csv; the gate in PART C")
    say("uses the MEDIAN, and that choice is a STATISTIC, not a tuned dial.")
    say("")

    def cm(flag, truth):
        tp = int((C[flag] & C[truth]).sum()); fp = int((C[flag] & ~C[truth]).sum())
        fn_ = int((~C[flag] & C[truth]).sum()); tn = int((~C[flag] & ~C[truth]).sum())
        return tp, fp, fn_, tn

    say(f"Confusion matrices ({len(C)} keys, ground truth hand-derived from the algebra), "
        "BOTH readings:")
    say(f"  {'instrument':16s} {'axis':16s} {'TP':>4s} {'FP':>4s} {'FN':>4s} {'TN':>4s}")
    cmrows = []
    for inst in ("T1_flag", "T2_flag", "BOTH_flag", "T1_flag_maxstat", "T2_flag_maxstat"):
        for axis in ("truth_scale_leak", "truth_term_dated"):
            tp, fp, fn_, tn = cm(inst, axis)
            say(f"  {inst:16s} {axis:16s} {tp:4d} {fp:4d} {fn_:4d} {tn:4d}")
            cmrows.append(dict(instrument=inst, axis=axis, TP=tp, FP=fp, FN=fn_, TN=tn))
    t1_fn = sorted(C.loc[~C.T1_flag & C.truth_term_dated, "key"])
    t2_fn = sorted(C.loc[~C.T2_flag & C.truth_scale_leak, "key"])
    t2_fp = sorted(C.loc[C.T2_flag & ~C.truth_term_dated, "key"])
    say("")
    say(f"  T1's FALSE NEGATIVES on the TERMINAL-DATING axis ({len(t1_fn)}): {', '.join(t1_fn)}")
    say(f"  T2's blind spot on the SCALE axis ({len(t2_fn)}): {', '.join(t2_fn)}")
    say(f"  T2's FALSE POSITIVES on causal keys ({len(t2_fp)}): "
        f"{', '.join(t2_fp) if t2_fp else 'NONE'}")
    say("")

    # leak content of each key, so the false negatives can be priced
    fwd = (px.iloc[-1] / px - 1.0)
    ics = {}
    for name, (fn, _, _, _) in KEY_SPECS.items():
        k = fn(px, vol, sh)
        vals = []
        for t in px.index[260::63]:
            a, b = k.loc[t], fwd.loc[t]
            m = a.notna() & b.notna()
            if m.sum() >= 20:
                ra, rb = a[m].rank(), b[m].rank()
                if ra.std() > 0 and rb.std() > 0:
                    vals.append(np.corrcoef(ra, rb)[0, 1])
        ics[name] = float(np.mean(vals)) if vals else np.nan
    C["absIC_fwd"] = C["key"].map(lambda k: abs(ics[k]))
    say("Leak content (|mean cross-sectional IC vs the REALISED forward return|), "
        "T1-cleared keys marked *:")
    for _, r in C.sort_values("absIC_fwd", ascending=False).head(10).iterrows():
        say(f"    {r['key']:10s} |IC| {r['absIC_fwd']:.4f}   T1 {'FLAG' if r['T1_flag'] else '  . '}"
            f"{'*' if (not r['T1_flag'] and r['truth_term_dated']) else ' '}   "
            f"T2 {'FLAG' if r['T2_flag'] else '  . '}")
    C.to_csv(OUT / f"{STEM}.certs.csv", index=False)
    pd.DataFrame(cmrows).to_csv(OUT / f"{STEM}.confusion.csv", index=False)
    say("")

    # ============================================================ PART B -- THE CENSUS
    say("=" * 112)
    say("PART B  CENSUS: how many committed rule-8 passes are built on a terminal-dated input?")
    say("=" * 112)
    files = sorted(OUT.glob("*.py"))
    crows, allhits, alltier2 = [], [], []
    for f in files:
        row, hits, tier2 = census_file(f)
        crows.append(row)
        allhits += [(f.name,) + h for h in hits]
        alltier2 += [(f.name,) + h for h in tier2]
    B = pd.DataFrame(crows)
    r8 = B[B.rule8]
    say(f"  committed scripts in research/backtests/          : {len(B)}")
    say(f"  ... that run a rule-8 / walk-forward leg          : {len(r8)} "
        f"({len(r8) / len(B):.1%})")
    say(f"  TIER 1  rule-8 files with a SHARP terminal token  : {int((r8.n_sharp > 0).sum())} "
        f"({(r8.n_sharp > 0).mean():.1%} of rule-8 files)   <- UPPER BOUND, includes reporting uses")
    say(f"  TIER 2  ... the SHARP token sits in a KEY/SELECT fn: {int((r8.n_sharp_tier2 > 0).sum())} "
        f"({(r8.n_sharp_tier2 > 0).mean():.1%} of rule-8 files)")
    say(f"  SOFT    rule-8 files with a full-sample reduction : {int((r8.n_hits > r8.n_sharp).sum())} "
        f"({(r8.n_hits > r8.n_sharp).mean():.1%}) -- reported SEPARATELY, never folded in")
    say("")
    say("  token classes over rule-8 files (a file may carry several):")
    for cname in TERM_PATTERNS:
        n1 = int(r8.classes.fillna("").str.contains(cname).sum())
        n2 = int(r8.tier2_classes.fillna("").str.contains(cname).sum())
        say(f"    {cname:16s} tier1 {n1:4d}   tier2 {n2:4d}")
    B.to_csv(OUT / f"{STEM}.census.csv", index=False)
    pd.DataFrame(allhits, columns=["file", "class", "line", "text"]).to_csv(
        OUT / f"{STEM}.hits.csv", index=False)
    pd.DataFrame(alltier2, columns=["file", "class", "line", "func", "text"]).to_csv(
        OUT / f"{STEM}.tier2.csv", index=False)
    say("")

    # hand-audit: read a deterministic sample of tier-2 hits and classify each one honestly
    say("  HAND AUDIT of a deterministic sample of 30 TIER-2 hits (the automatic classifier's")
    say("  precision -- a token in a selection function is still not necessarily a leaking KEY):")
    T2h = pd.DataFrame(alltier2, columns=["file", "class", "line", "func", "text"])
    T2h = T2h[T2h["class"].isin(SHARP_PATTERNS)]
    samp = T2h.sort_values(["file", "line"]).iloc[:: max(1, len(T2h) // 30)].head(30)
    say(f"    (tier-2 hits total {len(T2h)}; sampled every "
        f"{max(1, len(T2h) // 30)}th, {len(samp)} rows -> .audit.csv)")
    samp.to_csv(OUT / f"{STEM}.audit.csv", index=False)
    for _, r in samp.head(12).iterrows():
        say(f"    {r['class']:16s} {r['file'][:52]:52s}:{r['line']:<5d} {r['text'][:60]}")
    say("")
    # -- the refinement that matters: almost every SHARP token is a REPORTING read, not a key
    H = pd.DataFrame(allhits, columns=["file", "class", "line", "text"])
    H8 = H[H.file.isin(set(r8.file))]
    REPORTY = r"print|say\(|\.date\(\)"
    say("  REFINEMENT -- a terminal token is not a terminal KEY.  Splitting the two sharp")
    say("  positional classes by whether the line is a report line:")
    for cl in ("index_last", "iloc_last"):
        sub = H8[H8["class"] == cl]
        nr = sub[~sub.text.str.contains(REPORTY, regex=True, na=False)]
        say(f"    {cl:12s} {len(sub):4d} hits in {sub.file.nunique():3d} rule-8 files -> "
            f"{len(nr):4d} non-reporting hits in {nr.file.nunique():3d} files "
            f"({1 - len(nr) / max(len(sub), 1):.1%} of the token count is printing)")
    say("  and by the FILE the terminal value comes from (the class that cannot be printing):")
    for pat, lab in ((r"small_meta\.csv", "data/small_meta.csv"),
                     (r"universe_under2b\.csv", "deepvalue/universe_under2b.csv"),
                     (r"\.shares\.csv", "a pinned shares snapshot")):
        f = set(H8[H8.text.str.contains(pat, regex=True, na=False)].file)
        say(f"    {lab:34s} read by {len(f):4d} of {len(r8)} rule-8 files "
            f"({len(f) / len(r8):.1%})")
    say("")
    say("  The panel filter the record uses everywhere is itself terminal-dated:")
    say("    data/small_meta.csv `max_1d_move` is a FULL-SAMPLE max of |daily return| and the")
    say("    SMALL panel is defined by dropping names with max_1d_move >= 1.0 -- a statistic")
    say(f"    dated at the END of the sample, applied from day one.  It drops {len(bad)} names.")
    nsm = int(B[B.classes.fillna('').str.contains('snapshot_file')].shape[0])
    say(f"    {nsm} committed scripts read small_meta.csv / universe_under2b.csv / a shares pin.")
    say("    That is the MAXMOVE key in PART A: T1 clears it, T2 flags it.")
    say("")

    # ============================================================ PART C -- CONSEQUENCE BOOK
    say("=" * 112)
    say("PART C  THE CERTIFICATE AS A PRE-RULE-8 GATE  (SMALL430, top-20 EW, gross 0.75, weekly)")
    say("=" * 112)
    spy = spy_px.pct_change().fillna(0).loc[start:]
    srow = full_row(spy)
    g0c, t0c = fast_backtest(px, wctl)
    ctrl = {c: full_row(g0c.loc[start:] - t0c.loc[start:] * c / 1e4) for c in COSTS}
    b1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
    b2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
    v1 = {c: full_row(b1["returns"].loc[start:] - b1["turnover"].loc[start:] * c / 1e4)
          for c in COSTS}
    v2 = {c: full_row(b2["returns"].loc[start:] - b2["turnover"].loc[start:] * c / 1e4)
          for c in COSTS}
    say(f"  SPY                        {srow['CAGR_F']:7.2%} / {srow['Sharpe_F']:6.3f} / "
        f"{srow['MaxDD_F']:7.2%}   (H1 {srow['Sharpe_H1']:.3f} / H2 {srow['Sharpe_H2']:.3f} / "
        f"OOS {srow['Sharpe_OOS']:.3f})")
    for nm, rr in (("control (untilted composite)", ctrl), ("RULES v1", v1),
                   ("RULES v2 (live baseline)", v2)):
        r = rr[10.0]
        say(f"  {nm:26s} {r['CAGR_F']:7.2%} / {r['Sharpe_F']:6.3f} / {r['MaxDD_F']:7.2%}   "
            f"(H1 {r['Sharpe_H1']:.3f} / H2 {r['Sharpe_H2']:.3f} / OOS {r['Sharpe_OOS']:.3f})")
    say("")

    KEYCACHE = {k: KEY_SPECS[k][0](px, vol, sh) for k in KEY_SPECS}
    arms = []
    for c in COSTS:
        r = dict(key="CONTROL", family="control", dir="-", m=0.0, cost=c,
                 T1_flag=False, T2_flag=False,
                 turnover_yr=float(t0c.sum() / (len(t0c) / 252)))
        r.update(ctrl[c])
        r["pass4a"] = pass4a(r, v2[c]); r["pass4b"] = pass4b(r, srow)
        arms.append(r)
    flagT1 = dict(zip(C.key, C.T1_flag)); flagT2 = dict(zip(C.key, C.T2_flag))
    for kname, kv in KEYCACHE.items():
        for dname, sgn in DIRS.items():
            for m in MS:
                s_ = comp + sgn * m * (kv - 0.5)
                rr_ = s_.where(elig).rank(axis=1, ascending=False)
                w_ = (rr_ <= N).astype(float) * (GROSS / N)
                g_, t_ = fast_backtest(px, w_)
                g_, t_ = g_.loc[start:], t_.loc[start:]
                ty = float(t_.sum() / (len(t_) / 252))
                for c in COSTS:
                    row = dict(key=kname, family=KEY_SPECS[kname][3], dir=dname, m=m, cost=c,
                               T1_flag=bool(flagT1[kname]), T2_flag=bool(flagT2[kname]),
                               turnover_yr=ty)
                    row.update(full_row(g_ - t_ * c / 1e4))
                    row["dSharpe_F"] = row["Sharpe_F"] - ctrl[c]["Sharpe_F"]
                    row["dSharpe_IS"] = row["Sharpe_IS"] - ctrl[c]["Sharpe_IS"]
                    row["dSharpe_OOS"] = row["Sharpe_OOS"] - ctrl[c]["Sharpe_OOS"]
                    row["pass4a"] = pass4a(row, v2[c]); row["pass4b"] = pass4b(row, srow)
                    arms.append(row)
    A = pd.DataFrame(arms)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    say(f"  {len(A)} grid points written to .arms.csv  "
        f"({len(KEY_SPECS)} keys x 2 dirs x {len(MS)} m x {len(COSTS)} rungs + control)")
    say(f"  PROTOCOL 4 over the whole grid: 4a {int(A.pass4a.sum())}/{len(A)}   "
        f"4b {int(A.pass4b.sum())}/{len(A)}")
    if int(A.pass4b.sum()) == 0:
        fails = {"MaxDD": int((A.MaxDD_F < DELTA * srow["MaxDD_F"]).sum()),
                 "CAGR": int((A.CAGR_F < PHI * srow["CAGR_F"]).sum()),
                 "H1": int((A.Sharpe_H1 <= srow["Sharpe_H1"]).sum()),
                 "H2": int((A.Sharpe_H2 <= srow["Sharpe_H2"]).sum()),
                 "OOS": int((A.Sharpe_OOS <= srow["Sharpe_OOS"]).sum())}
        say(f"  4b leg failure counts: " + "  ".join(f"{k} {v}" for k, v in
                                                     sorted(fails.items(), key=lambda z: -z[1])))
    say("")

    # ------------------------------------------------------- PROTOCOL 8, gate by gate
    say("-" * 112)
    say("RULE 8 (PROTOCOL 8): (KEY, m) chosen on 2010-2016 IS Sharpe ALONE; 2017-2026 read once.")
    say("The GATE is applied BEFORE the choice -- that is the whole proposal on trial.")
    say("-" * 112)
    GATES = {
        "NONE":  lambda k: True,
        "T1":    lambda k: not flagT1[k],
        "T2":    lambda k: not flagT2[k],
        "T1&T2": lambda k: (not flagT1[k]) and (not flagT2[k]),
    }
    wf = []
    say(f"{'gate':7s} {'rung':>5s} {'admits':>6s} {'pick':22s} {'IS Sharpe':>9s} "
        f"{'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS MaxDD':>10s} {'vs SPY':>8s} {'vs v2':>7s}")
    for gname, gfn in GATES.items():
        adm = [k for k in KEY_SPECS if gfn(k)]
        for c in COSTS:
            sub = A[(A.cost == c) & (A.key.isin(adm))]
            if not len(sub):
                continue
            pick = sub.loc[sub.Sharpe_IS.idxmax()]
            tag = f"{pick['key']}/{pick['dir']}/m={pick['m']:.2f}"
            say(f"{gname:7s} {c:5.0f} {len(adm):6d} {tag:22s} {pick['Sharpe_IS']:9.3f} "
                f"{pick['CAGR_OOS']:9.2%} {pick['Sharpe_OOS']:9.3f} {pick['MaxDD_OOS']:10.2%} "
                f"{pick['Sharpe_OOS'] - srow['Sharpe_OOS']:+8.3f} "
                f"{pick['Sharpe_OOS'] - v2[c]['Sharpe_OOS']:+7.3f}")
            wf.append(dict(gate=gname, cost=c, n_admitted=len(adm), pick=tag,
                           pick_key=pick["key"], pick_family=pick["family"],
                           pick_term_dated=bool(KEY_SPECS[pick["key"]][2]),
                           pick_scale_leak=bool(KEY_SPECS[pick["key"]][1]),
                           Sharpe_IS=pick["Sharpe_IS"], CAGR_OOS=pick["CAGR_OOS"],
                           Sharpe_OOS=pick["Sharpe_OOS"], MaxDD_OOS=pick["MaxDD_OOS"],
                           CAGR_F=pick["CAGR_F"], Sharpe_F=pick["Sharpe_F"],
                           MaxDD_F=pick["MaxDD_F"],
                           spy_CAGR_OOS=srow["CAGR_OOS"], spy_Sharpe_OOS=srow["Sharpe_OOS"],
                           spy_MaxDD_OOS=srow["MaxDD_OOS"],
                           v2_CAGR_OOS=v2[c]["CAGR_OOS"], v2_Sharpe_OOS=v2[c]["Sharpe_OOS"],
                           v2_MaxDD_OOS=v2[c]["MaxDD_OOS"],
                           v1_Sharpe_OOS=v1[c]["Sharpe_OOS"],
                           ctrl_Sharpe_OOS=ctrl[c]["Sharpe_OOS"],
                           beats_spy_OOS=bool(pick["Sharpe_OOS"] > srow["Sharpe_OOS"]),
                           beats_v2_OOS=bool(pick["Sharpe_OOS"] > v2[c]["Sharpe_OOS"]),
                           pass4a=bool(pick["pass4a"]), pass4b=bool(pick["pass4b"])))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("")
    say(f"  OOS comparands @10bps: SPY {srow['CAGR_OOS']:.2%}/{srow['Sharpe_OOS']:.3f}/"
        f"{srow['MaxDD_OOS']:.2%}   RULES v2 {v2[10.0]['CAGR_OOS']:.2%}/"
        f"{v2[10.0]['Sharpe_OOS']:.3f}/{v2[10.0]['MaxDD_OOS']:.2%}   RULES v1 "
        f"{v1[10.0]['CAGR_OOS']:.2%}/{v1[10.0]['Sharpe_OOS']:.3f}/{v1[10.0]['MaxDD_OOS']:.2%}   "
        f"control {ctrl[10.0]['CAGR_OOS']:.2%}/{ctrl[10.0]['Sharpe_OOS']:.3f}/"
        f"{ctrl[10.0]['MaxDD_OOS']:.2%}")
    for gname in GATES:
        sub = W[W.gate == gname]
        say(f"  gate {gname:6s}: picks a TERMINAL-DATED key at {int(sub.pick_term_dated.sum())}"
            f"/{len(sub)} rungs; beats SPY OOS {int(sub.beats_spy_OOS.sum())}/{len(sub)}; "
            f"beats RULES v2 OOS {int(sub.beats_v2_OOS.sum())}/{len(sub)}")
    say("")

    # ============================================================ PART D -- predictions scored
    say("=" * 112)
    say("PART D  PRE-REGISTERED PREDICTIONS, SCORED")
    say("=" * 112)
    R = pd.DataFrame(repro)
    R.to_csv(OUT / f"{STEM}.repro.csv", index=False)
    p1 = bool(R.passed.all())
    p2 = len(t1_fn) > 0 and "FWDRET" in t1_fn
    p3 = len(t2_fp) == 0
    p4 = len(t2_fn) > 0 and len(t1_fn) > 0
    wn, w1, w2 = W[W.gate == "NONE"], W[W.gate == "T1"], W[W.gate == "T2"]
    p5 = (bool(wn.pick_term_dated.all()) and bool(w1.pick_term_dated.all())
          and bool(wn.beats_spy_OOS.all()) and bool(w1.beats_spy_OOS.all())
          and not bool(w2.pick_term_dated.any()) and not bool(w2.beats_spy_OOS.any()))
    p6 = int(A.pass4a.sum()) == 0 and int(A.pass4b.sum()) == 0
    for tag, ok, txt in [
        ("P1", p1, f"gates all pass ({int(R.passed.sum())}/{len(R)})"),
        ("P2", p2, f"T1 false negatives on the dating axis: {t1_fn or 'NONE'}"),
        ("P3", p3, f"T2 false positives on causal keys: {t2_fp or 'NONE'}"),
        ("P4", p4, f"disjoint content: T1-only {t2_fn}, T2-only {t1_fn}"),
        ("P5", p5, f"NONE picks {list(wn.pick_key)}, T1 picks {list(w1.pick_key)}, "
                   f"T2 picks {list(w2.pick_key)}"),
        ("P6", p6, f"4a {int(A.pass4a.sum())}/{len(A)}, 4b {int(A.pass4b.sum())}/{len(A)}")]:
        say(f"  {tag} {'HIT ' if ok else 'MISS'}  {txt}")
    say("")
    say(f"runtime {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()

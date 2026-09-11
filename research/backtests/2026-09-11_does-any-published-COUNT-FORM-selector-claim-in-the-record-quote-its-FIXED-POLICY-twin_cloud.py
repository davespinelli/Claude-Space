#!/usr/bin/env python3
"""
IDEA 693 -- does-any-published-COUNT-FORM-selector-claim-in-the-record-quote-its-FIXED-POLICY-twin
==================================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 688 found the 5 count-form MAX selectors it tested are pick-for-pick identical to
  "take the widest" (K-MAX agreement 1.000 at every ceiling) and that the record carries 18
  count-form selector sites across 6 criteria (IS_bought, Ebar_IS, width, OOS_bought,
  n_elig_IS, bought_pp).  Re-read each of those committed claims with its fixed-policy twin
  computed beside it and report how many published "selected" results are really constants.
  Max 2 params (claim set, twin definition).

WHY THIS IS NOT A REPEAT OF 688
-------------------------------
  688 measured the pathology on SUB-PANEL DRAWS from SMALL439 with the panel WIDTH k as the
  free axis -- a setting where `argmax(extensive criterion) == argmax k` is close to an
  identity and the agreement of 1.000 is nearly forced.  The record's committed sites do NOT
  select over panel width; they select over BOOK dials (n, gate strictness) on a FIXED panel.
  On those dials an extensive criterion can SATURATE: once n exceeds the number of eligible
  names the book stops growing, so `argmax IS_bought` need not be `argmax n` and the twin can
  in principle break.  This run asks whether it ever does, on the record's own panels and
  dials, and -- the part 688 never priced -- whether QUOTING THE TWIN INSTEAD OF THE SELECTOR
  WOULD CHANGE ANY PUBLISHED VERDICT (rule 8 OOS, both KEEP paths).

DESIGN
------
  LEG A -- CENSUS OF THE RECORD (deterministic, code not prose).  Every `research/backtests/
  *.py` is parsed with `ast`; every selection site (idxmax / argmax / argmin / nlargest /
  sort_values-then-head / max(..., key=) over a named criterion) is extracted with its
  criterion token.  Tokens are classified EXTENSIVE (count-form: a sum or a count over panel
  or book members -- `bought`, `n_elig`, `Ebar`, `width`, `k`, `count`, `n_names`, `nsel`,
  `n_rows`) vs INTENSIVE (a rate, share, ratio or risk-adjusted number) vs UNCLASSIFIED, by a
  FIXED lexicon printed in full below.  For every count-form site the file is then searched
  for whether it computes a fixed-policy twin beside the claim (a K-MAX / widest / constant /
  twin control).  Headline number: count-form sites, and how many of them quote a twin.

  LEG B -- RESTATEMENT WITH THE TWIN BESIDE IT (price, the part that carries the verdict).
  On three FULL panels a pre-registered 2-dial book grid is built and every count-form
  criterion in the queue's list is run as a selector over it, beside its fixed-policy twin.

    BOOKS   CAND-n through the record's RULES v1 gate (above the 200d MA and vol20 < VOLCAP),
            composite score with NO vol scaler (the 2026-09-04 KEEP-4b construction), a FIXED
            0.75/n per name -- so a book with fewer than n eligible names de-grosses to cash,
            which is exactly the saturation channel this run is looking for.
    DIAL 1  n in {5, 10, 15, 20, 30, 40, 50}                                      (7 rungs)
    DIAL 2  gate strictness VOLCAP in {0.40, 0.60, 0.90}, 0.60 is live            (3 rungs)
            -> 21 books per panel x 3 panels = 63 books, ALL reported.
    TUNED (2)  CLAIM SET (the 6 criteria the queue names) x TWIN DEFINITION (K-MAX "take the
            widest n" vs LOOSEST "take the loosest gate" vs CORNER "widest n AND loosest
            gate").  All 3 twin definitions are reported for all 6 criteria on all 3 panels.
    FIXED   gross 0.75, cadence W, cost 10 bps (PROTOCOL rule 2), t+1 execution (engine),
            260-row warm-up skip, IS <= 2016-12-31 / OOS >= 2017-01-01 (PROTOCOL rule 8).
            None of these was chosen by outcome.
    COST    10 bps carries every verdict.  A 0/25 bps appendix is printed and written as a
            LABELLED ROBUSTNESS table; no verdict is taken from it, it is not a third axis.

  RULE 8 (PROTOCOL 8).  Every selector chooses ONE grid point per panel using IS rows ONLY;
  the pick is then scored on 2017-2026 read once, against SPY OOS and live RULES v2 OOS.
  OOS_bought is in the queue's list but is a PEEKING criterion (it reads OOS rows); it is run,
  labelled PEEKING, and excluded from every verdict.  Reference selectors carried beside the
  count-form ones: IS-SHARPE-MAX (the record's dominant intensive criterion), K-MAX and
  LOOSEST (calibration controls that MUST pin at 1.000 against their own twin), and RANDOM
  (seeded, measures this test's own false-positive rate).

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  fast_backtest == engine.backtest @10 bps                                    bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          bar 0.0
  G3  SMALL: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G4  EXTENSIVITY IDENTITY: IS_bought == bought_pp * (number of IS rebalance periods)  1e-9
  G5  CAUSALITY: w(px[:d])  is a value-for-value prefix of w(px)[:d]              bar 0.0
  G6  IS-ONLY: every selector statistic recomputed from a price frame TRUNCATED at IS_END
      reproduces the statistic computed on the full frame and sliced                bar 1e-9
  G7  The grid's n=20 / VOLCAP=0.60 cell reproduces the standing 2026-09-04 KEEP-4b
      incumbent's published U56 numbers 12.66% / 1.0921 / -18.31%                 bar 5e-3

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents and SMALL is the CURRENT sub-$2B screen only (see
  data/SMALL_PANEL_README.md): names acquired, delisted or grown out of the screen are absent,
  so every LEVEL on those two panels is biased upward and none is a tradeable estimate.  U56
  carries the same bias in milder form.  This run's headline quantities are AGREEMENT RATES
  and WITHIN-PANEL pick differences, to which the bias applies identically on both sides.
"""
import ast
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

COST0 = 10.0
COSTS_APPENDIX = [0.0, 25.0]
FREQ = "W"
BAND0, GROSS0 = 0.03, 0.75
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [5, 10, 15, 20, 30, 40, 50]
VOLCAPS = [0.40, 0.60, 0.90]
SEED = 693
KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)

# ---- the FIXED lexicon used by LEG A (printed in the console before any count is read) ----
EXT_TOKENS = ["bought", "n_elig", "nelig", "ebar", "width", "count", "n_names", "nsel",
              "n_rows", "n_files", "n_sites", "nobs", "n_obs", "total", "sum", "_k", "k_",
              "npick", "n_pick", "size", "depth", "reach"]
INT_TOKENS = ["sharpe", "cagr", "maxdd", "dd", "calmar", "vol", "breadth", "share", "rate",
              "ratio", "pct", "frac", "mean", "median", "premium", "prem", "margin", "corr",
              "rho", "auc", "slope", "t_stat", "tstat", "pp", "per", "avg", "score", "ic"]
TWIN_MARKS = ["k-max", "kmax", "k_max", "widest", "fixed-policy", "fixed policy", "twin",
              "constant policy", "take the widest", "degenerate", "tautolog"]

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# machinery
# ==========================================================================================
def fast_backtest(prices, weights, freq=FREQ, cost=COST0):
    """Vectorised equivalent of engine.backtest's return stream (G1 pins it at 1e-12)."""
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
    return pd.Series((held * rets).sum(axis=1) - turn * cost / 1e4, index=idx)


def M0(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def eligibility(px, volcap):
    """The record's RULES v1 gate: above the 200d MA and vol20 < volcap.  Score carries NO
    vol scaler (the 2026-09-04 KEEP-4b construction, pinned by G7)."""
    sc, above, vol20 = score(px, vol_scale=False)
    return sc, (above & (vol20 < volcap))


def cand_book(sc, elig, n, gross=GROSS0):
    """Top-n by composite among eligible names at a FIXED gross/n per name.  Fewer than n
    eligible names -> the book de-grosses to cash.  This is the saturation channel."""
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def keeppaths(m, oos_s, mb, ms, spy_oos):
    """PROTOCOL rule 4.  4a: Sharpe > live book in BOTH halves and MaxDD no worse.
       4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b)


def fail4b(m, oos_s, ms, spy_oos):
    f = []
    if not m["H1"] > ms["H1"]: f.append("H1")
    if not m["H2"] > ms["H2"]: f.append("H2")
    if not oos_s > spy_oos: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return "+".join(f) if f else "-"


# ==========================================================================================
# LEG A -- census of the record's committed selector sites
# ==========================================================================================
SEL_CALLS = {"idxmax", "idxmin", "argmax", "argmin", "nlargest", "nsmallest"}


def _token_of(node):
    """Best-effort criterion token for a selection site: the subscript key or attribute the
    selector is applied to, e.g. df['IS_bought'].idxmax() -> 'IS_bought'."""
    v = getattr(node.func, "value", None)
    while v is not None:
        if isinstance(v, ast.Subscript):
            s = v.slice
            if isinstance(s, ast.Constant) and isinstance(s.value, str):
                return s.value
            if isinstance(s, ast.Index) and isinstance(getattr(s, "value", None), ast.Constant):
                return s.value.value
            v = v.value
            continue
        if isinstance(v, ast.Attribute):
            return v.attr
        if isinstance(v, ast.Name):
            return v.id
        if isinstance(v, ast.Call):
            for kw in v.keywords:
                if kw.arg in ("by", "key", "columns") and isinstance(kw.value, ast.Constant):
                    return str(kw.value.value)
            v = getattr(v.func, "value", None)
            continue
        break
    return ""


def classify(tok):
    t = tok.lower()
    ext = any(k in t for k in EXT_TOKENS)
    itn = any(k in t for k in INT_TOKENS)
    if ext and not itn: return "EXTENSIVE"
    if itn and not ext: return "INTENSIVE"
    if ext and itn: return "MIXED"
    return "UNCLASSIFIED"


def census():
    P("=" * 100)
    P("(B) LEG A -- CENSUS OF THE RECORD'S COMMITTED SELECTOR SITES (ast, not prose)")
    P("=" * 100)
    P("  FIXED LEXICON (declared before any count is read)")
    P(f"    EXTENSIVE tokens ({len(EXT_TOKENS)}): {', '.join(EXT_TOKENS)}")
    P(f"    INTENSIVE tokens ({len(INT_TOKENS)}): {', '.join(INT_TOKENS)}")
    P(f"    TWIN marks    ({len(TWIN_MARKS)}): {', '.join(TWIN_MARKS)}")
    rows = []
    files = sorted((ROOT / "research" / "backtests").glob("*.py"))
    parsed = failed = 0
    for f in files:
        try:
            src = f.read_text(errors="replace")
            tree = ast.parse(src)
            parsed += 1
        except Exception:
            failed += 1
            continue
        low = src.lower()
        twin_here = any(m in low for m in TWIN_MARKS)
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            if node.func.attr not in SEL_CALLS:
                continue
            tok = _token_of(node)
            if not tok:
                continue
            rows.append(dict(file=f.name, line=node.lineno, call=node.func.attr,
                             criterion=tok, kind=classify(tok), twin_in_file=twin_here))
    df = pd.DataFrame(rows)
    P(f"  files parsed {parsed}   unparseable {failed}   selection sites {len(df)}")
    if df.empty:
        return df
    k = df.kind.value_counts()
    for name in ("EXTENSIVE", "INTENSIVE", "MIXED", "UNCLASSIFIED"):
        P(f"    {name:<13} {int(k.get(name, 0)):5d} sites   "
          f"{int(k.get(name, 0)) / len(df):6.1%}")
    ext = df[df.kind == "EXTENSIVE"]
    P(f"  COUNT-FORM (EXTENSIVE) sites               : {len(ext)} "
      f"in {ext.file.nunique()} files, {ext.criterion.nunique()} distinct criteria")
    q = ext.twin_in_file.sum()
    P(f"  ...of which the FILE computes a twin/control: {int(q)} "
      f"({q / max(len(ext), 1):.1%})   -> NO TWIN QUOTED: {len(ext) - int(q)}")
    P("  top count-form criteria by site count:")
    for c, v in ext.criterion.value_counts().head(12).items():
        sub = ext[ext.criterion == c]
        P(f"    {c:<24} {v:4d} sites   twin quoted in {int(sub.twin_in_file.sum()):3d}")
    dump(df, "census")
    return df


# ==========================================================================================
# LEG B -- the price restatement
# ==========================================================================================
def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL"] = sm[keep]
    return panels, len(sm.columns) - len(keep), sorted(bad)


def build_grid(px, panel, cost=COST0):
    """Every (n, volcap) cell: the book, its criterion statistics, and its performance."""
    idx = px.index
    start = idx[WARM]
    is_mask = (idx >= start) & (idx <= pd.Timestamp(IS_END))
    oos_mask = idx >= pd.Timestamp(OOS_START)
    reb = rebalance_mask(idx, FREQ).values
    is_reb = int((reb & is_mask).sum())
    rows, books = [], {}
    for vc in VOLCAPS:
        sc, elig = eligibility(px, vc)
        nel = elig.sum(axis=1)
        for n in NS:
            w = cand_book(sc, elig, n)
            held = (w > 0).sum(axis=1)
            r = fast_backtest(px, w, FREQ, cost).loc[start:]
            m = M(r)
            m_oos = M(r.loc[OOS_START:])
            m_is = M(r.loc[:IS_END])
            rows.append(dict(
                panel=panel, n=n, volcap=vc,
                # --- the queue's six count-form criteria, IS rows only unless marked ---
                IS_bought=float(held[is_mask & reb].sum()),
                bought_pp=float(held[is_mask & reb].mean()),
                n_elig_IS=float(nel[is_mask].mean()),
                Ebar_IS=float(nel[is_mask].sum()),
                width=float(n),
                OOS_bought=float(held[oos_mask & reb].sum()),          # PEEKING, labelled
                # --- reference / calibration criteria ---
                IS_Sharpe=m_is["Sharpe"], IS_CAGR=m_is["CAGR"],
                sat=float((held[is_mask & reb] < n).mean()),           # saturation share
                # --- performance, full sample and the rule-8 windows ---
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                is_reb=is_reb))
            books[(vc, n)] = w
    return pd.DataFrame(rows), books, start


CRITERIA = [("IS_bought", False), ("bought_pp", False), ("n_elig_IS", False),
            ("Ebar_IS", False), ("width", False), ("OOS_bought", True)]
REFERENCE = [("IS_Sharpe", False)]


def pick(g, col, seed=None):
    """Deterministic argmax with a FIXED tie-break: ties go to the smallest n, then the
    strictest gate.  (Declared, not chosen by outcome -- the conservative direction, since
    every result below is about selectors drifting toward the WIDE corner.)"""
    if col == "RANDOM":
        rng = np.random.default_rng(seed)
        return int(g.index[rng.integers(len(g))])
    s = g[col].round(12)
    best = s.max()
    cand = g[s == best].sort_values(["n", "volcap"])
    return int(cand.index[0])


TWINS = {
    "K-MAX(widest n)":       lambda g: int(g.sort_values(["n", "volcap"], ascending=[False, True]).index[0]),
    "LOOSEST(gate)":         lambda g: int(g.sort_values(["volcap", "n"], ascending=[False, True]).index[0]),
    "CORNER(widest+loosest)": lambda g: int(g.sort_values(["n", "volcap"], ascending=[False, False]).index[0]),
}


def main():
    P("=" * 100)
    P(f"IDEA 693 -- {STEM}")
    P("=" * 100)
    panels, n_dropped, bad = load_panels()

    # ---------------------------------------------------------------- gates
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]
    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights      : {g2:.3e}  {'PASS' if g2 == 0 else 'FAIL'}")
    ok &= g2 == 0.0

    slow = backtest(px, w, cost_bps=COST0, freq=FREQ)["returns"]
    fast = fast_backtest(px, w, FREQ, COST0)
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast_backtest == engine.backtest @10 bps      : {g1:.3e}  {'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    P(f"  G3 SMALL: dropped max_1d_move>=1.0 tickers       : {n_dropped} dropped "
      f"-> {panels['SMALL'].shape[1]} cols  {'PASS' if n_dropped > 0 else 'FAIL'}")
    ok &= n_dropped > 0

    # G5 causality: truncating the price frame truncates the weights, value for value
    sc, el = eligibility(px, 0.60)
    wfull = cand_book(sc, el, 20)
    cut = px.index[int(len(px) * 0.7)]
    sc_t, el_t = eligibility(px.loc[:cut], 0.60)
    wtr = cand_book(sc_t, el_t, 20)
    g5 = float(np.abs(wtr.values - wfull.loc[:cut, wtr.columns].values).max())
    P(f"  G5 CAUSALITY w(px[:d]) prefix of w(px)           : {g5:.3e}  {'PASS' if g5 == 0 else 'FAIL'}")
    ok &= g5 == 0.0

    # ---------------------------------------------------------------- leg B grid
    grids, starts = {}, {}
    for name, p in panels.items():
        grids[name], _, starts[name] = build_grid(p, name)

    gg = grids["U56"]
    g4 = float(np.abs(gg.IS_bought - gg.bought_pp * gg.is_reb).max())
    P(f"  G4 IS_bought == bought_pp * IS periods           : {g4:.3e}  {'PASS' if g4 < 1e-9 else 'FAIL'}")
    ok &= g4 < 1e-9

    # G6 IS-only: recompute IS statistics on a TRUNCATED frame
    tr = panels["U56"].loc[:IS_END]
    sct, elt = eligibility(tr, 0.60)
    nelt = elt.sum(axis=1)
    ist = (tr.index >= tr.index[WARM]) & (tr.index <= pd.Timestamp(IS_END))
    ref = float(nelt[ist].mean())
    got = float(gg.loc[(gg.n == 20) & (gg.volcap == 0.60), "n_elig_IS"].iloc[0])
    g6 = abs(ref - got)
    P(f"  G6 IS stats from a TRUNCATED frame reproduce     : {g6:.3e}  {'PASS' if g6 < 1e-9 else 'FAIL'}")
    ok &= g6 < 1e-9

    inc = gg.loc[(gg.n == 20) & (gg.volcap == 0.60)].iloc[0]
    d7 = max(abs(inc.CAGR - KEEP4B_INCUMBENT["CAGR"]),
             abs(inc.Sharpe - KEEP4B_INCUMBENT["Sharpe"]),
             abs(inc.MaxDD - KEEP4B_INCUMBENT["MaxDD"]))
    P(f"  G7 n=20/vc=0.60 reproduces the 2026-09-04 KEEP-4b: "
      f"{inc.CAGR:.4f}/{inc.Sharpe:.4f}/{inc.MaxDD:.4f} vs "
      f"{KEEP4B_INCUMBENT['CAGR']:.4f}/{KEEP4B_INCUMBENT['Sharpe']:.4f}/"
      f"{KEEP4B_INCUMBENT['MaxDD']:.4f}  max|d| {d7:.3e}  {'PASS' if d7 < 5e-3 else 'FAIL'}")
    ok &= d7 < 5e-3
    P(f"  GATES: {'ALL PASS' if ok else 'AT LEAST ONE FAILED -- results below are NOT publishable'}")
    if not ok:
        P("  ABORTING: a pre-registered gate failed.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return 1

    census()

    # ---------------------------------------------------------------- comparands
    P("=" * 100)
    P("(C) LEG B -- THE GRID, ITS COMPARANDS, AND BOTH KEEP PATHS ON ALL 63 CELLS")
    P("=" * 100)
    comp = {}
    for name, p in panels.items():
        st = starts[name]
        spy = p["SPY"].pct_change().fillna(0).loc[st:]
        base = fast_backtest(p, rules_v2_weights(p), FREQ, COST0).loc[st:]
        comp[name] = dict(ms=M(spy), mb=M(base),
                          spy_oos=M0(spy.loc[OOS_START:]), base_oos=M0(base.loc[OOS_START:]),
                          spy_oos_m=M(spy.loc[OOS_START:]), base_oos_m=M(base.loc[OOS_START:]))
        c = comp[name]
        P(f"  {name:<6} rows {len(p):5d} cols {p.shape[1]:4d}  "
          f"SPY  CAGR {c['ms']['CAGR']:6.2%} Sharpe {c['ms']['Sharpe']:.4f} "
          f"MaxDD {c['ms']['MaxDD']:7.2%} H1/H2 {c['ms']['H1']:.4f}/{c['ms']['H2']:.4f} "
          f"OOS S {c['spy_oos']:.4f}")
        P(f"  {'':<6} {'':<16}  RULESv2 CAGR {c['mb']['CAGR']:6.2%} Sharpe {c['mb']['Sharpe']:.4f} "
          f"MaxDD {c['mb']['MaxDD']:7.2%} H1/H2 {c['mb']['H1']:.4f}/{c['mb']['H2']:.4f} "
          f"OOS S {c['base_oos']:.4f}")

    allrows = []
    for name, g in grids.items():
        c = comp[name]
        for i, r in g.iterrows():
            m = dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2)
            p4a, p4b = keeppaths(m, r.OOS_Sharpe, c["mb"], c["ms"], c["spy_oos"])
            g.loc[i, "pass4a"] = p4a
            g.loc[i, "pass4b"] = p4b
            g.loc[i, "fail4b"] = fail4b(m, r.OOS_Sharpe, c["ms"], c["spy_oos"])
        allrows.append(g)
    grid = pd.concat(allrows, ignore_index=True)
    P("")
    P("  ALL 63 GRID POINTS (PROTOCOL rule 5: every point reported)")
    P(f"  {'panel':<6} {'n':>3} {'vcap':>5} | {'CAGR':>7} {'Shrp':>7} {'MaxDD':>8} "
      f"{'H1':>6} {'H2':>6} | {'oCAGR':>7} {'oShrp':>7} {'oDD':>8} | "
      f"{'sat':>5} {'IS_bght':>8} {'nelIS':>6} | {'4a':>3} {'4b':>3} {'fail4b':<12}")
    for _, r in grid.iterrows():
        P(f"  {r.panel:<6} {int(r.n):>3} {r.volcap:>5.2f} | {r.CAGR:>7.2%} {r.Sharpe:>7.4f} "
          f"{r.MaxDD:>8.2%} {r.H1:>6.3f} {r.H2:>6.3f} | {r.OOS_CAGR:>7.2%} "
          f"{r.OOS_Sharpe:>7.4f} {r.OOS_MaxDD:>8.2%} | {r.sat:>5.2f} {r.IS_bought:>8.0f} "
          f"{r.n_elig_IS:>6.1f} | {str(bool(r.pass4a)):>3} {str(bool(r.pass4b)):>3} {r.fail4b:<12}")
    P(f"  4a passes {int(grid.pass4a.sum())}/{len(grid)}   4b passes {int(grid.pass4b.sum())}/{len(grid)}")
    dump(grid, "grid")

    # ---------------------------------------------------------------- selectors vs twins
    P("=" * 100)
    P("(D) EVERY COUNT-FORM SELECTOR BESIDE ITS FIXED-POLICY TWIN  (3 twin definitions)")
    P("=" * 100)
    sel_rows = []
    sel_list = ([(c, pk, "count-form") for c, pk in CRITERIA]
                + [(c, False, "intensive-reference") for c, _ in REFERENCE]
                + [("RANDOM", False, "control")])
    for name, g in grids.items():
        gi = g.reset_index(drop=True)
        c = comp[name]
        for crit, peeking, kind in sel_list:
            si = pick(gi, crit, seed=SEED + hash(name) % 1000)
            srow = gi.loc[si]
            for tname, tfn in TWINS.items():
                ti = tfn(gi)
                trow = gi.loc[ti]
                sel_rows.append(dict(
                    panel=name, criterion=crit, kind=kind, peeking=peeking, twin=tname,
                    sel_n=int(srow.n), sel_vc=srow.volcap, twin_n=int(trow.n), twin_vc=trow.volcap,
                    same=bool(si == ti),
                    sel_OOS_Sharpe=srow.OOS_Sharpe, twin_OOS_Sharpe=trow.OOS_Sharpe,
                    d_OOS_Sharpe=srow.OOS_Sharpe - trow.OOS_Sharpe,
                    sel_OOS_CAGR=srow.OOS_CAGR, twin_OOS_CAGR=trow.OOS_CAGR,
                    sel_OOS_MaxDD=srow.OOS_MaxDD, twin_OOS_MaxDD=trow.OOS_MaxDD,
                    sel_4b=bool(srow.pass4b), twin_4b=bool(trow.pass4b),
                    sel_4a=bool(srow.pass4a), twin_4a=bool(trow.pass4a),
                    spy_oos=c["spy_oos"], base_oos=c["base_oos"]))
    sel = pd.DataFrame(sel_rows)
    for tname in TWINS:
        sub = sel[sel.twin == tname]
        P(f"  TWIN DEFINITION: {tname}")
        P(f"    {'criterion':<12} {'kind':<20} {'agreement':>10}  "
          f"{'median dOOS Sharpe':>19}  {'verdict flips (4b)':>19}")
        for crit in sub.criterion.unique():
            s2 = sub[sub.criterion == crit]
            flips = int((s2.sel_4b != s2.twin_4b).sum())
            P(f"    {crit:<12} {s2.kind.iloc[0]:<20} {s2.same.mean():>9.3f}  "
              f"{s2.d_OOS_Sharpe.median():>19.4f}  {flips:>19d}"
              + ("   [PEEKING -- excluded from verdicts]" if bool(s2.peeking.iloc[0]) else ""))
        P("")
    dump(sel, "selectors")

    # ---------------------------------------------------------------- rule 8
    P("=" * 100)
    P("(E) PROTOCOL RULE 8 -- pick on IS (<= 2016-12-31), read 2017-2026 ONCE")
    P("=" * 100)
    wf = []
    P(f"  {'panel':<6} {'selector':<22} {'pick(n,vcap)':<14} | {'OOS CAGR':>9} {'OOS Shrp':>9} "
      f"{'OOS MaxDD':>10} | {'SPY oC':>8} {'SPY oS':>8} {'v2 oS':>8} | {'4a':>4} {'4b':>4} {'fail4b':<12}")
    for name, g in grids.items():
        gi = g.reset_index(drop=True)
        c = comp[name]
        rows = ([(crit, peek) for crit, peek in CRITERIA] + [("IS_Sharpe", False),
                ("RANDOM", False)] + [(t, False) for t in TWINS])
        for crit, peek in rows:
            i = TWINS[crit](gi) if crit in TWINS else pick(gi, crit, seed=SEED + hash(name) % 1000)
            r = gi.loc[i]
            wf.append(dict(panel=name, selector=crit, peeking=peek, n=int(r.n), volcap=r.volcap,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           SPY_OOS_CAGR=c["spy_oos_m"]["CAGR"], SPY_OOS_Sharpe=c["spy_oos"],
                           SPY_OOS_MaxDD=c["spy_oos_m"]["MaxDD"],
                           BASE_OOS_CAGR=c["base_oos_m"]["CAGR"], BASE_OOS_Sharpe=c["base_oos"],
                           pass4a=bool(r.pass4a), pass4b=bool(r.pass4b), fail4b=r.fail4b,
                           CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2))
            P(f"  {name:<6} {crit:<22} n={int(r.n):<3} vc={r.volcap:<5.2f} | {r.OOS_CAGR:>9.2%} "
              f"{r.OOS_Sharpe:>9.4f} {r.OOS_MaxDD:>10.2%} | {c['spy_oos_m']['CAGR']:>8.2%} "
              f"{c['spy_oos']:>8.4f} {c['base_oos']:>8.4f} | {str(bool(r.pass4a)):>4} "
              f"{str(bool(r.pass4b)):>4} {r.fail4b:<12}"
              + ("  [PEEKING]" if peek else ""))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")
    live = wfd[~wfd.peeking]
    P(f"  OOS picks beating SPY OOS Sharpe : {int((live.OOS_Sharpe > live.SPY_OOS_Sharpe).sum())}/{len(live)}")
    P(f"  OOS picks beating RULES v2 OOS   : {int((live.OOS_Sharpe > live.BASE_OOS_Sharpe).sum())}/{len(live)}")
    P(f"  4a passes {int(live.pass4a.sum())}/{len(live)}   4b passes {int(live.pass4b.sum())}/{len(live)}")

    # ---------------------------------------------------------------- cost appendix
    P("=" * 100)
    P("(F) LABELLED ROBUSTNESS -- cost appendix (NO verdict is taken from this table)")
    P("=" * 100)
    app = []
    for cst in COSTS_APPENDIX:
        for name, p in panels.items():
            g2d, _, _ = build_grid(p, name, cost=cst)
            gi = g2d.reset_index(drop=True)
            for crit in ["IS_bought", "Ebar_IS", "width", "IS_Sharpe"]:
                i = pick(gi, crit)
                t = TWINS["K-MAX(widest n)"](gi)
                app.append(dict(cost_bps=cst, panel=name, criterion=crit,
                                same_as_KMAX=bool(i == t),
                                OOS_Sharpe=gi.loc[i].OOS_Sharpe,
                                twin_OOS_Sharpe=gi.loc[t].OOS_Sharpe))
    appd = pd.DataFrame(app)
    P(f"  agreement with K-MAX at 0 bps  : {appd[appd.cost_bps == 0].same_as_KMAX.mean():.3f}")
    P(f"  agreement with K-MAX at 25 bps : {appd[appd.cost_bps == 25].same_as_KMAX.mean():.3f}")
    dump(appd, "costappendix")

    P("=" * 100)
    P("(G) SURVIVORSHIP CAVEAT (PROTOCOL 9)")
    P("=" * 100)
    P("  B136 = today's constituents; SMALL = the CURRENT sub-$2B screen only.  Names that were")
    P("  acquired, delisted or grew out of the screen are absent, so every LEVEL on those two")
    P("  panels is biased upward and none of them is a tradeable estimate.  U56 carries the same")
    P("  bias in milder form.  This run's headline is an AGREEMENT RATE and a WITHIN-PANEL pick")
    P("  difference, to which the same bias applies on both sides of every comparison.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""QUEUE idea 459 — is-the-DD-CAP-the-only-thing-4b-ever-tests-on-a-ranked-book  (cloud, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 239's 16 ten-bps 4b passes are all RANKED arms with NEGATIVE Sharpe excess over their own
control; they pass because MaxDD lands inside SPY's 60% bar while the control's does not.  Census
every 4b pass in LEADERBOARD.md and report how many clear on the DD cap alone with no Sharpe edge
over an un-ranked control.  Max 2 params."

What is on trial.  Not a book: PROTOCOL 4b's own DISCRIMINATION.  4b has four bars (H1 Sharpe >
SPY, H2 Sharpe > SPY, OOS Sharpe > SPY, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's — five
readings of four quantities).  The queue's charge is that on RANKED books only the DD cap ever
BINDS, i.e. ranking buys admission through the drawdown bar while giving back Sharpe against the
un-ranked control it should be judged against.  If true, every ranked 4b pass in the record is a
statement about concentration's drawdown path and not about the ranking key.

TWO PARTS, because the queue asks for a census and a census alone cannot answer it.

PART A  CENSUS of the committed record (READ, never re-simulated).  LEADERBOARD.md prose is not
        machine-countable at this precision, so the census runs over the committed CSVs that
        carry a machine 4b verdict column (pass4b / p4b / keep4b) — the same substrate idea 239
        used — and LEADERBOARD.md is counted separately and coarsely, labelled as coarse.
  A1  COVERAGE.  Files and rows carrying a 4b verdict; passes; what fraction of passing rows can
      be classified RANKED vs UN-RANKED from their own labels.  Unclassifiable rows are COUNTED,
      never guessed.
  A2  MATCHED CONTROL.  For each passing RANKED row, an un-ranked row in the SAME file at the
      same panel / gross / cost.  Report how many passes have one at all (idea 239: 319 of 634
      multi-panel files publish no un-ranked control).
  A3  THE QUEUE'S STATISTIC.  Over matched pairs: Sharpe excess of the ranked pass over its
      control, the fraction <= 0, and of those how many have a control whose `fail4b` reason is
      EXACTLY `DD` — the operational meaning of "clears on the DD cap alone".
  A4  BINDING-BAR CENSUS.  Over every committed row that FAILS 4b, how often DD is the sole
      named reason, ranked and un-ranked separately.  This is the census the queue asks for,
      read from the record's own reason strings.

PART B  FRESH CORPUS in which the control exists BY CONSTRUCTION (the real test).  Every ranked
        arm is built beside its own un-ranked control on the same panel, the same gross, the same
        cadence and the same cost rung, so no pass can go unmatched.
  B1  GATES.  `fast_bt` vs `engine.backtest` on returns AND turnover; the cost-rung identity
      net(c) = net(0) - turnover*c/1e4 against a live `backtest(cost_bps=25)`; TOP-n nesting of
      `baseline.rules_v1_weights` and the EWALL control's nesting of `rules_v2_weights`' form.
  B2  4b, ALL FOUR BARS SEPARATELY, on every arm; plus two counterfactual screens —
      4b\\DD (the DD cap deleted) and 4b+X (an un-ranked-control Sharpe-excess clause added).
  B3  THE HEADLINE.  Of ranked arms passing 4b: how many have Sharpe excess <= 0 over their own
      matched control AND a control that fails 4b on DD alone.
  B4  RULE 8.  (n, g) chosen on IS <= 2016-12-31 by IS Sharpe, read ONCE on 2017-2026; OOS
      CAGR / Sharpe / MaxDD vs the live RULES v2 baseline and vs SPY, on every panel.
  B5  BOTH KEEP PATHS (PROTOCOL 4a and 4b) reported on every grid point, both cost rungs.
  B6  POST-HOC DIAGNOSTIC, declared as such and carrying no verdict: a 9-step scan of g that
      locates the interval of gross clearing each 4b bar, ranked and un-ranked.  Written and run
      AFTER the pre-registered grid above was read; it explains the headline, it does not
      re-state it, and no prediction is scored on it.

THE TWO TUNED PARAMETERS (PROTOCOL 4): n (book width, 6 values incl. the un-ranked control at
n = ALL) and g (nominal gross, 3 values).  Cadence is FIXED at weekly (the live convention) and
the cost rung is a REPORTED dimension, not a dial.  All 18 grid points per panel are reported.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
  P1  Coverage is the census's limiting factor: FEWER THAN HALF of the record's committed 4b
      passes have a matched un-ranked control in their own file.
  P2  The queue's statistic replicates in the record: among matched ranked passes, a MAJORITY
      have Sharpe excess <= 0 over their control.
  P3  In the fresh corpus, DD is the MODAL sole binding bar for un-ranked controls (the control
      fails 4b on DD and nothing else) on at least 2 of 3 panels.
  P4  Deleting the DD cap (4b\\DD) ADMITS more arms than 4b does, and adding the control-excess
      clause (4b+X) admits FEWER than half of 4b's ranked passes.
  P5  Under rule 8 the IS chooser picks a RANKED width (n < ALL) on at least 2 of 3 panels, and
      its OOS Sharpe does NOT beat the un-ranked control's OOS Sharpe on a majority of panels.

CAVEATS carried, not buried
  * SURVIVORSHIP (idea 54).  U56, B136 and the sub-$2B panel are CURRENT-constituent lists with
    no delistings and no dead names.  Every arm inherits it equally, so the PAIRED ranked-minus-
    control contrasts that carry this run's answer are largely protected; every LEVEL (CAGR,
    Sharpe, MaxDD, and therefore every 4b verdict quoted here) is biased upward and none is a
    tradable estimate.  The small panel additionally drops the 44 names with max_1d_move >= 1.0
    per data/small_meta.csv before anything is priced.
  * The census rows are NOT independent: they share books, panels and cost rungs across files,
    and many files publish several rungs of one simulation.  Counts are counts; no p-value is
    computed over them and none should be.
  * A 4b verdict is a function of SPY's own numbers over the SAME window, so verdicts from files
    with different samples are not strictly commensurable.  Part B fixes the window per panel and
    quotes SPY's three bars beside every arm.
  * Idea 144: a re-dialled book is the same book.  Nothing here proposes a new signal.

Deterministic, standalone.  Writes .console.txt .census_files.csv .census_pairs.csv
.census_bars.csv .grid.csv .bars.csv .walkforward.csv .params.csv
"""
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, rebalance_mask                                     # noqa: E402

STEM = "2026-09-08_is-the-DD-CAP-the-only-thing-4b-ever-tests-on-a-ranked-book_cloud"
OUT = ROOT / "research" / "backtests"

N_GRID = [5, 10, 20, 30, 40, "ALL"]          # tuned parameter 1 (ALL = the un-ranked control)
G_GRID = [0.50, 0.75, 1.00]                  # tuned parameter 2
RUNGS = [10, 25]                             # reported dimension, not a dial
FREQ = "W"                                   # fixed: the live cadence
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

RANKED_PAT = re.compile(
    r"(top-?\d|topn|top_?n|rank|ranked|v1[a-z]?\b|rules.?v1|n=\d|k=\d|conc|sel|best)", re.I)
UNRANKED_PAT = re.compile(
    r"(ewall|ew_all|ew-all|eqw|equal|ewelig|ew_elig|unranked|un-ranked|control|band|v2|ma200|"
    r"nofilt|no-?filter|ew\b)", re.I)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


T0 = time.time()
P("=" * 118)
P("IDEA 459  is-the-DD-CAP-the-only-thing-4b-ever-tests-on-a-ranked-book   (cloud, 2026-09-08)")
P("=" * 118)

# =====================================================================================
# PART A — CENSUS of the committed record
# =====================================================================================
P("\n" + "-" * 118)
P("A1  COVERAGE — every committed CSV carrying a machine 4b verdict column")
P("-" * 118)

VERDICT_COLS = ["pass4b", "p4b", "keep4b", "is4b", "b4b"]
FAIL_COLS = ["fail4b", "fail_4b", "why4b", "bind4b"]
SHARPE_COLS = ["Sharpe", "sharpe", "OOS_Sharpe", "S", "full_Sharpe"]
LABEL_COLS = ["book", "arm", "family", "kind", "name", "conv", "variant", "form", "label",
              "dial", "pick", "selector", "rule", "strategy"]
KEY_COLS = ["panel", "universe", "cost", "cost_bps", "bps", "rung", "gross", "g", "freq",
            "cadence", "conv"]


def truthy(v):
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, float, np.integer, np.floating)):
        return bool(v) and not (isinstance(v, float) and np.isnan(v))
    s = str(v).strip().lower()
    return s in {"true", "yes", "y", "pass", "1", "1.0", "keep", "t"}


def classify(text):
    """RANKED / UNRANKED / UNKNOWN from a row's own labels.  Never guesses."""
    t = str(text)
    r, u = bool(RANKED_PAT.search(t)), bool(UNRANKED_PAT.search(t))
    if r and not u:
        return "RANKED"
    if u and not r:
        return "UNRANKED"
    return "UNKNOWN"


files = [f for f in sorted(OUT.glob("*.csv")) + sorted(OUT.glob("*.csv.gz"))
         if not f.name.startswith(STEM)]      # never census this run's own outputs
frows, pair_rows, bar_rows = [], [], []
tot_rows = tot_pass = 0
cls_counts = {"RANKED": 0, "UNRANKED": 0, "UNKNOWN": 0}
n_with_verdict = n_with_fail = 0
for f in files:
    try:
        head = pd.read_csv(f, nrows=0)
    except Exception:
        continue
    cols = list(head.columns)
    vc = next((c for c in VERDICT_COLS if c in cols), None)
    if vc is None:
        continue
    try:
        d = pd.read_csv(f)
    except Exception:
        continue
    n_with_verdict += 1
    fc = next((c for c in FAIL_COLS if c in cols), None)
    if fc:
        n_with_fail += 1
    sc = next((c for c in SHARPE_COLS if c in cols), None)
    labs = [c for c in LABEL_COLS if c in cols]
    keys = [c for c in KEY_COLS if c in cols and c not in labs]
    d = d.loc[:, ~d.columns.duplicated()]
    lab = pd.Series([""] * len(d), index=d.index)
    for c in labs:
        lab = lab + " " + d[c].astype(str)
    cl = lab.map(classify)
    pas = d[vc].map(truthy)
    tot_rows += len(d)
    tot_pass += int(pas.sum())
    for k in cls_counts:
        cls_counts[k] += int((cl[pas] == k).sum())
    frows.append(dict(file=f.name, rows=len(d), passes=int(pas.sum()), verdict_col=vc,
                      fail_col=fc or "-", sharpe_col=sc or "-",
                      label_cols="|".join(labs), key_cols="|".join(keys),
                      pass_ranked=int((cl[pas] == "RANKED").sum()),
                      pass_unranked=int((cl[pas] == "UNRANKED").sum()),
                      pass_unknown=int((cl[pas] == "UNKNOWN").sum())))

    # ---- A2/A3 matched control inside this file
    if sc is not None and keys:
        kk = pd.Series([""] * len(d), index=d.index)
        for c in keys:
            kk = kk + "|" + d[c].astype(str)
        for i in np.flatnonzero((pas & (cl == "RANKED")).values):
            same = np.flatnonzero(((kk == kk.iloc[i]) & (cl == "UNRANKED")).values)
            if len(same) == 0:
                pair_rows.append(dict(file=f.name, row=int(i), key=kk.iloc[i],
                                      label=lab.iloc[i][:80], matched=0,
                                      dS=np.nan, ctrl_pass=np.nan, ctrl_fail=""))
                continue
            js = same[np.argsort(-d[sc].values[same])]      # best control = hardest test
            j = int(js[0])
            ds = float(d[sc].values[i]) - float(d[sc].values[j])
            pair_rows.append(dict(file=f.name, row=int(i), key=kk.iloc[i],
                                  label=lab.iloc[i][:80], matched=1, dS=ds,
                                  ctrl_pass=int(truthy(d[vc].values[j])),
                                  ctrl_fail=str(d[fc].values[j]) if fc else ""))

    # ---- A4 binding-bar census over FAILING rows
    if fc:
        for i in np.flatnonzero((~pas).values):
            bar_rows.append(dict(file=f.name, cls=cl.iloc[i],
                                 reason=str(d[fc].values[i]).strip()))

FC = pd.DataFrame(frows)
FC.to_csv(OUT / f"{STEM}.census_files.csv", index=False)
PR = pd.DataFrame(pair_rows)
PR.to_csv(OUT / f"{STEM}.census_pairs.csv", index=False)
BR = pd.DataFrame(bar_rows)
BR.to_csv(OUT / f"{STEM}.census_bars.csv", index=False)

P(f"  committed CSVs scanned: {len(files)};  carrying a 4b verdict column: {n_with_verdict};"
  f"  of those carrying a fail-reason column: {n_with_fail}")
P(f"  rows under a 4b verdict: {tot_rows:,};  4b PASSES: {tot_pass:,} "
  f"({tot_pass / max(tot_rows, 1):.1%} of rows)")
P(f"  passes classifiable from their own labels: RANKED {cls_counts['RANKED']:,} / "
  f"UNRANKED {cls_counts['UNRANKED']:,} / UNKNOWN {cls_counts['UNKNOWN']:,} "
  f"(UNKNOWN counted, never guessed)")

# LEADERBOARD.md, coarse and labelled as coarse
lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
lb_rows = [l for l in lb if l.startswith("|") and l.count("|") > 6]
lb_4b = [l for l in lb_rows if re.search(r"4b", l)]
lb_4b_pass = [l for l in lb_4b if re.search(r"4b[^.|]{0,40}(PASS|KEEP)", l, re.I)]
lb_ctrl = [l for l in lb_4b_pass if re.search(r"(ewall|EW_ALL|control|un-?ranked)", l, re.I)]
P(f"  [coarse] LEADERBOARD.md: {len(lb_rows):,} table rows, {len(lb_4b):,} name 4b, "
  f"{len(lb_4b_pass):,} claim a 4b PASS/KEEP in prose, of which {len(lb_ctrl):,} "
  f"({len(lb_ctrl) / max(len(lb_4b_pass), 1):.0%}) also name an un-ranked control.  Prose counts "
  f"are indicative only; every number below comes from the machine columns.")

P("\n" + "-" * 118)
P("A2/A3  MATCHED CONTROL and the queue's statistic")
P("-" * 118)
if len(PR):
    m = PR[PR.matched == 1]
    P(f"  ranked 4b passes with a machine-comparable file (Sharpe + key columns): {len(PR):,}")
    P(f"  of those, a matched UN-RANKED control at the same panel/gross/cost exists for "
      f"{len(m):,} ({len(m) / len(PR):.1%}) -> P1 predicted < 50%: "
      f"{'HIT' if len(m) / len(PR) < 0.5 else 'MISS'}")
    if len(m):
        neg = m.dS <= 0
        P(f"  Sharpe excess over the control: mean {m.dS.mean():+.4f}, median "
          f"{m.dS.median():+.4f}, sd {m.dS.std():.4f}, min {m.dS.min():+.4f}, "
          f"max {m.dS.max():+.4f}")
        P(f"  ranked passes with excess <= 0: {int(neg.sum()):,} of {len(m):,} "
          f"({neg.mean():.1%}) -> P2 predicted a majority: "
          f"{'HIT' if neg.mean() > 0.5 else 'MISS'}")
        dd_only = m[neg & m.ctrl_fail.astype(str).str.fullmatch(r"\s*DD\s*", na=False)]
        P(f"  ... AND whose control fails 4b on DD ALONE: {len(dd_only):,} "
          f"({len(dd_only) / len(m):.1%} of matched passes) — the queue's exact claim, "
          f"machine-counted over the committed record")
        P(f"  ... control ALSO passes 4b in {int((m.ctrl_pass == 1).sum()):,} of "
          f"{int(m.ctrl_pass.notna().sum()):,} matched pairs")
else:
    P("  no machine-comparable pairs found")

P("\n" + "-" * 118)
P("A4  BINDING-BAR CENSUS — over every committed row that FAILS 4b")
P("-" * 118)
if len(BR):
    BR["norm"] = (BR.reason.str.replace(r"[+,;/ ]+", "|", regex=True)
                  .str.strip("|").str.upper())
    BR["nbars"] = BR.norm.apply(lambda s: 0 if s in ("", "-", "NAN", "NONE") else len(s.split("|")))
    sole = BR[BR.nbars == 1]
    P(f"  failing rows with a reason string: {len(BR):,}  "
      f"(sole-reason rows {len(sole):,} = {len(sole) / len(BR):.1%})")
    P("  sole binding bar, all rows:")
    for k, v in sole.norm.value_counts().head(8).items():
        P(f"      {k:<12} {v:>7,}  ({v / len(sole):.1%} of sole-reason rows)")
    for c in ("RANKED", "UNRANKED", "UNKNOWN"):
        s2 = sole[sole.cls == c]
        if len(s2):
            top = s2.norm.value_counts()
            dd = int(top.get("DD", 0))
            P(f"  {c:<9}: {len(s2):>7,} sole-reason rows; DD alone {dd:>6,} ({dd / len(s2):.1%}); "
              f"modal bar {top.index[0]} ({top.iloc[0] / len(s2):.1%})")
    allbars = BR[BR.nbars > 0].norm.str.split("|").explode().value_counts()
    P("  bar APPEARANCE among all failing rows (a row may name several): "
      + ", ".join(f"{k} {v:,}" for k, v in allbars.head(6).items()))
else:
    P("  no committed fail-reason strings found")

# =====================================================================================
# PART B — FRESH CORPUS
# =====================================================================================
P("\n" + "-" * 118)
P("B0  PANELS")
P("-" * 118)


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    return px[keep]


PANELS = {}
PANELS["u56"] = load_universe()
PANELS["broad136"] = load_universe(broad=True)
PANELS["small439"] = small_panel()
for k, v in PANELS.items():
    P(f"  {k:<9} {v.shape[1]:>4} cols x {len(v):,} days  {v.index[0].date()} -> {v.index[-1].date()}"
      + ("   [44 max_1d_move>=1.0 names dropped]" if k == "small439" else ""))
P("  SURVIVORSHIP: all three are current-constituent lists.  Levels biased up; paired contrasts "
  "(ranked minus its own control) are the load-bearing numbers here.")


def fast_bt(px, w, cost_bps=10.0, freq=FREQ):
    """engine.backtest, vectorised over names.  Returns (net returns, turnover)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    T, N = rets.shape
    cur = np.zeros(N)
    held = np.empty((T, N))
    turn = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    gross_r = (held * rets).sum(axis=1)
    idx = px.index
    return (pd.Series(gross_r - turn * cost_bps / 1e4, index=idx),
            pd.Series(turn, index=idx))


def mets(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    return (float(eq.iloc[-1] ** (1 / yrs) - 1), float(r.mean() * 252 / vol) if vol else np.nan,
            float((eq / eq.cummax() - 1).min()))


def topn_weights(px, n, g):
    s, above, vol20 = score(px, vol_scale=True)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return sel * (g / n)


def ewall_weights(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


P("\n" + "-" * 118)
P("B1  GATES — nothing below is read until these pass")
P("-" * 118)
gpx = PANELS["u56"]
w_test = topn_weights(gpx, 20, 0.75)
r_fast, t_fast = fast_bt(gpx, w_test, 10.0)
eng = backtest(gpx, w_test, cost_bps=10.0, freq=FREQ)
g1 = float(np.abs(r_fast - eng["returns"]).max())
g2 = float(np.abs(t_fast - eng["turnover"]).max())
P(f"  fast_bt vs engine.backtest @10bps: returns max|diff| {g1:.3e};  turnover max|diff| {g2:.3e}")
eng25 = backtest(gpx, w_test, cost_bps=25.0, freq=FREQ)
r0, t0 = fast_bt(gpx, w_test, 0.0)
g3 = float(np.abs((r0 - t0 * 25 / 1e4) - eng25["returns"]).max())
P(f"  cost-rung identity net(25) = net(0) - turnover*25/1e4 vs live backtest(25): {g3:.3e}")
w_v1 = rules_v1_weights(gpx)
g4 = float(np.abs(topn_weights(gpx, 5, 5 * 0.15).fillna(0) - w_v1.fillna(0)).max().max())
P(f"  TOP-n nests baseline.rules_v1_weights (n=5, g=0.75): max|diff| {g4:.3e}")
w_v2 = rules_v2_weights(gpx, band=0.03, gross=0.75)
w_ew = ewall_weights(gpx, 0.75)
g5 = float(np.abs(w_ew.where(w_v2 > 0, 0.0) - w_v2).max().max())
P(f"  EWALL control nests RULES v2's un-ranked weighting off the band gate: max|diff| {g5:.3e}")
GATES_OK = max(g1, g2, g3, g4, g5) < 1e-12
P(f"  GATES {'PASS' if GATES_OK else 'FAIL'}")
assert GATES_OK, "gate failure — nothing below may be read"

P("\n" + "-" * 118)
P("B2  THE GRID — 3 panels x 6 widths (incl. the un-ranked control) x 3 gross x 2 rungs, "
  "weekly, next-day")
P("-" * 118)
rows = []
for pname, px in PANELS.items():
    spy = px["SPY"].pct_change().fillna(0.0)
    start = px.index[260]
    spy = spy.loc[start:]
    h = len(spy) // 2
    sC, sS, sD = mets(spy)
    sH1 = mets(spy.iloc[:h])[1]
    sH2 = mets(spy.iloc[h:])[1]
    sO = mets(spy.loc[OOS_START:])[1]
    sOC = mets(spy.loc[OOS_START:])[0]
    sOD = mets(spy.loc[OOS_START:])[2]
    P(f"  [{pname}] SPY over the common sample: CAGR {sC:.2%}  Sharpe {sS:.3f} "
      f"(H1 {sH1:.3f} / H2 {sH2:.3f})  MaxDD {sD:.2%};  OOS(2017+) Sharpe {sO:.3f} "
      f"CAGR {sOC:.2%} MaxDD {sOD:.2%}")
    base_r, _ = fast_bt(px, rules_v2_weights(px), 0.0)
    base_t = fast_bt(px, rules_v2_weights(px), 0.0)[1]
    for n in N_GRID:
        for g in G_GRID:
            w = ewall_weights(px, g) if n == "ALL" else topn_weights(px, n, g)
            r0, t0 = fast_bt(px, w, 0.0)
            for c in RUNGS:
                r = (r0 - t0 * c / 1e4).loc[start:]
                C, S, D = mets(r)
                H1 = mets(r.iloc[:h])[1]
                H2 = mets(r.iloc[h:])[1]
                oo = r.loc[OOS_START:]
                OC, OS_, OD = mets(oo)
                bars = dict(H1=H1 > sH1, H2=H2 > sH2, OOS=OS_ > sO,
                            DD=D >= 0.6 * sD, CAGR=C >= 0.7 * sC)
                fails = "|".join(k for k, v in bars.items() if not v) or "-"
                bl = (base_r - base_t * c / 1e4).loc[start:]
                bC, bS, bD = mets(bl)
                bH1, bH2 = mets(bl.iloc[:h])[1], mets(bl.iloc[h:])[1]
                rows.append(dict(panel=pname, n=str(n), gross=g, cost=c,
                                 ranked=(n != "ALL"), CAGR=C, Sharpe=S, MaxDD=D, H1=H1, H2=H2,
                                 OOS_Sharpe=OS_, OOS_CAGR=OC, OOS_MaxDD=OD,
                                 turnover=float(t0.loc[start:].sum() / (len(r) / 252)),
                                 pass4b=all(bars.values()), fail4b=fails,
                                 pass4b_noDD=all(v for k, v in bars.items() if k != "DD"),
                                 pass4a=(H1 > bH1 and H2 > bH2 and D >= bD),
                                 spy_CAGR=sC, spy_Sharpe=sS, spy_MaxDD=sD,
                                 spy_H1=sH1, spy_H2=sH2, spy_OOS_Sharpe=sO,
                                 base_Sharpe=bS, base_MaxDD=bD, base_CAGR=bC))
G = pd.DataFrame(rows)
ctrl = (G[~G.ranked].set_index(["panel", "gross", "cost"])
        [["Sharpe", "OOS_Sharpe", "MaxDD", "CAGR", "pass4b", "fail4b"]]
        .rename(columns=lambda c: "ctrl_" + c))
G = G.join(ctrl, on=["panel", "gross", "cost"])
G["dSharpe_ctrl"] = G.Sharpe - G.ctrl_Sharpe
G["dOOS_ctrl"] = G.OOS_Sharpe - G.ctrl_OOS_Sharpe
G["pass4b_X"] = G.pass4b & (G.dSharpe_ctrl > 0)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
P(f"  grid points: {len(G)} (all reported in {STEM}.grid.csv)")
for pname in PANELS:
    sub = G[(G.panel == pname) & (G.cost == 10)]
    P(f"\n  [{pname} @10bps]  n      g     CAGR   Sharpe    MaxDD     H1     H2    OOS   "
      f"4b   4b\\DD  4a   dS vs control   fail4b")
    for _, r in sub.iterrows():
        P(f"                  {r['n']:>4} {r.gross:5.2f} {r.CAGR:7.2%} {r.Sharpe:7.3f} "
          f"{r.MaxDD:8.2%} {r.H1:6.3f} {r.H2:6.3f} {r.OOS_Sharpe:6.3f}   "
          f"{'Y' if r.pass4b else 'n'}    {'Y' if r.pass4b_noDD else 'n'}    "
          f"{'Y' if r.pass4a else 'n'}   {r.dSharpe_ctrl:+8.4f}       {r.fail4b}")

P("\n" + "-" * 118)
P("B3  THE HEADLINE — what does 4b actually test on a ranked book?")
P("-" * 118)
rk = G[G.ranked]
P(f"  ranked grid points: {len(rk)};  4b passes {int(rk.pass4b.sum())};  "
  f"4b\\DD (cap deleted) passes {int(rk.pass4b_noDD.sum())};  "
  f"4b+X (control-excess clause) passes {int(rk.pass4b_X.sum())}")
P(f"  P4 predicted 4b\\DD admits MORE than 4b: "
  f"{'HIT' if rk.pass4b_noDD.sum() > rk.pass4b.sum() else 'MISS'};  and 4b+X admits fewer than "
  f"half of 4b's ranked passes: "
  f"{'HIT' if rk.pass4b_X.sum() < 0.5 * max(rk.pass4b.sum(), 1) else 'MISS'}")
pk = rk[rk.pass4b]
if len(pk):
    neg = pk.dSharpe_ctrl <= 0
    dd_only = pk[neg & (~pk.ctrl_pass4b) & (pk.ctrl_fail4b == "DD")]
    P(f"  of the {len(pk)} ranked 4b passes: {int(neg.sum())} ({neg.mean():.0%}) have Sharpe "
      f"excess <= 0 over their OWN matched un-ranked control")
    P(f"  of the {len(pk)} ranked 4b passes: {len(dd_only)} ({len(dd_only) / len(pk):.0%}) clear "
      f"on the DD cap ALONE — excess <= 0 AND the control fails 4b on DD and nothing else")
    P(f"  control ALSO passes 4b beside {int(pk.ctrl_pass4b.sum())} of {len(pk)} ranked passes")
    P(f"  Sharpe excess over control among ranked passes: mean {pk.dSharpe_ctrl.mean():+.4f}, "
      f"median {pk.dSharpe_ctrl.median():+.4f}, range [{pk.dSharpe_ctrl.min():+.4f}, "
      f"{pk.dSharpe_ctrl.max():+.4f}]")
else:
    P("  NO ranked arm passes 4b anywhere on this grid — the queue's premise cannot be tested "
      "on it, and that is itself the answer for this corpus.")
un = G[~G.ranked]
P(f"  un-ranked controls: {len(un)} points, 4b passes {int(un.pass4b.sum())} "
  f"({un.pass4b.mean():.0%})")
bars_rows = []
for cls, sub in (("RANKED", rk), ("UNRANKED", un)):
    fl = sub[~sub.pass4b].fail4b
    sole = fl[fl.str.count(r"\|") == 0]
    vc = sole.value_counts()
    P(f"  {cls:<9} failing points {len(fl)};  sole-bar failures {len(sole)}"
      + (f";  modal sole bar {vc.index[0]} ({vc.iloc[0]}/{len(sole)})" if len(sole) else "")
      + f";  DD alone {int((sole == 'DD').sum())}")
    for k, v in fl.str.split("|").explode().value_counts().items():
        bars_rows.append(dict(cls=cls, bar=k, appearances=int(v), failing_points=len(fl)))
pd.DataFrame(bars_rows).to_csv(OUT / f"{STEM}.bars.csv", index=False)
p3 = 0
for pname in PANELS:
    s = un[(un.panel == pname) & (~un.pass4b)]
    sole = s.fail4b[s.fail4b.str.count(r"\|") == 0]
    ok = len(sole) and sole.value_counts().index[0] == "DD"
    p3 += int(bool(ok))
    P(f"  [{pname}] control sole-bar failures {len(sole)}"
      + (f", modal {sole.value_counts().index[0]}" if len(sole) else "")
      + f"; all control failures name: {sorted(set(s.fail4b))}")
P(f"  P3 (DD modal sole bar for controls on >=2 of 3 panels): {'HIT' if p3 >= 2 else 'MISS'} "
  f"({p3}/3)")

P("\n" + "-" * 118)
P("B4  RULE 8 — (n, g) chosen on IS <= 2016-12-31 by IS Sharpe, read ONCE on 2017-2026")
P("-" * 118)
wf = []
for pname, px in PANELS.items():
    spy = px["SPY"].pct_change().fillna(0.0).loc[px.index[260]:]
    for c in RUNGS:
        cand = []
        for n in N_GRID:
            for g in G_GRID:
                w = ewall_weights(px, g) if n == "ALL" else topn_weights(px, n, g)
                r0, t0 = fast_bt(px, w, 0.0)
                r = (r0 - t0 * c / 1e4).loc[px.index[260]:]
                cand.append((n, g, mets(r.loc[:IS_END])[1], r))
        pick = max(cand, key=lambda x: x[2])
        ctrl_best = max([x for x in cand if x[0] == "ALL"], key=lambda x: x[2])
        oo = pick[3].loc[OOS_START:]
        co = ctrl_best[3].loc[OOS_START:]
        so = spy.loc[OOS_START:]
        br0, bt0 = fast_bt(px, rules_v2_weights(px), 0.0)
        bo = (br0 - bt0 * c / 1e4).loc[px.index[260]:].loc[OOS_START:]
        C, S, D = mets(oo)
        cC, cS, cD = mets(co)
        bC, bS, bD = mets(bo)
        sC, sS, sD = mets(so)
        wf.append(dict(panel=pname, cost=c, pick_n=str(pick[0]), pick_g=pick[1],
                       IS_Sharpe=pick[2], OOS_CAGR=C, OOS_Sharpe=S, OOS_MaxDD=D,
                       ctrl_n=str(ctrl_best[0]), ctrl_g=ctrl_best[1],
                       ctrl_OOS_Sharpe=cS, ctrl_OOS_CAGR=cC, ctrl_OOS_MaxDD=cD,
                       base_OOS_Sharpe=bS, base_OOS_CAGR=bC, base_OOS_MaxDD=bD,
                       spy_OOS_Sharpe=sS, spy_OOS_CAGR=sC, spy_OOS_MaxDD=sD,
                       ranked_pick=(pick[0] != "ALL"),
                       beats_ctrl=(S > cS), beats_spy=(S > sS), beats_base=(S > bS)))
        P(f"  [{pname} @{c}bps] IS pick n={pick[0]} g={pick[1]:.2f} (IS Sharpe {pick[2]:.3f})"
          f" -> OOS {C:7.2%} / {S:.3f} / {D:7.2%}  |  best un-ranked control "
          f"n=ALL g={ctrl_best[1]:.2f} -> {cC:7.2%} / {cS:.3f} / {cD:7.2%}  |  RULES v2 "
          f"{bC:7.2%} / {bS:.3f} / {bD:7.2%}  |  SPY {sC:7.2%} / {sS:.3f} / {sD:7.2%}")
WF = pd.DataFrame(wf)
WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
r10 = WF[WF.cost == 10]
p5 = (int(r10.ranked_pick.sum()) >= 2) and (int(r10.beats_ctrl.sum()) <= 1)
P(f"  @10bps: ranked pick on {int(r10.ranked_pick.sum())}/3 panels; the pick beats its control "
  f"OOS on {int(r10.beats_ctrl.sum())}/3, beats SPY on {int(r10.beats_spy.sum())}/3, beats "
  f"RULES v2 on {int(r10.beats_base.sum())}/3")
P(f"  P5 {'HIT' if p5 else 'MISS'}")

P("\n" + "-" * 118)
P("B6  POST-HOC DIAGNOSTIC (declared: NOT pre-registered, no verdict is restated on it) — the")
P("    4b WINDOW IN g.  Sharpe is gross-invariant, so only the DD cap and the CAGR floor can")
P("    move with g.  A finer g scan locates, per (panel, width, rung), the interval of g that")
P("    clears each bar.  If the DD cap were 'the only thing 4b tests', the CAGR floor would")
P("    never bind and every window would run down to g = 0.")
P("-" * 118)
G_FINE = [round(0.20 + 0.10 * i, 2) for i in range(9)]      # 0.20 .. 1.00
wrows = []
for pname, px in PANELS.items():
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    sC, sS, sD = mets(spy)
    for n in N_GRID:
        for c in RUNGS:
            okDD, okCAGR, ok4b = [], [], []
            for g in G_FINE:
                w = ewall_weights(px, g) if n == "ALL" else topn_weights(px, n, g)
                r0, t0 = fast_bt(px, w, 0.0)
                r = (r0 - t0 * c / 1e4).loc[start:]
                C, S, D = mets(r)
                h = len(r) // 2
                H1, H2 = mets(r.iloc[:h])[1], mets(r.iloc[h:])[1]
                OS_ = mets(r.loc[OOS_START:])[1]
                sH1, sH2 = mets(spy.iloc[:h])[1], mets(spy.iloc[h:])[1]
                sO = mets(spy.loc[OOS_START:])[1]
                dd_ok, cagr_ok = (D >= 0.6 * sD), (C >= 0.7 * sC)
                sh_ok = (H1 > sH1) and (H2 > sH2) and (OS_ > sO)
                if dd_ok:
                    okDD.append(g)
                if cagr_ok:
                    okCAGR.append(g)
                if dd_ok and cagr_ok and sh_ok:
                    ok4b.append(g)
                wrows.append(dict(panel=pname, n=str(n), cost=c, gross=g, CAGR=C, Sharpe=S,
                                  MaxDD=D, H1=H1, H2=H2, OOS_Sharpe=OS_, dd_ok=dd_ok,
                                  cagr_ok=cagr_ok, sharpe_ok=sh_ok,
                                  pass4b=(dd_ok and cagr_ok and sh_ok)))
            P(f"  [{pname} @{c}bps n={str(n):>3}]  DD cap clears at g<= "
              f"{max(okDD) if okDD else float('nan'):.2f}"
              f"   CAGR floor clears at g>= {min(okCAGR) if okCAGR else float('nan'):.2f}"
              f"   Sharpe bars {'PASS' if wrows[-1]['sharpe_ok'] else 'fail'}"
              f"   4b window {('[%.2f, %.2f], %d of 9 steps' % (min(ok4b), max(ok4b), len(ok4b))) if ok4b else 'EMPTY'}")
WIN = pd.DataFrame(wrows)
WIN.to_csv(OUT / f"{STEM}.window.csv", index=False)
nb = WIN.groupby(["panel", "n", "cost"]).pass4b.sum().reset_index()
ctrl_cells = nb[nb.n == "ALL"]
P(f"  windows non-empty: {int((nb.pass4b > 0).sum())} of {len(nb)} (panel x width x rung) cells; "
  f"un-ranked control cells non-empty {int((ctrl_cells.pass4b > 0).sum())} of {len(ctrl_cells)}")

P("\n" + "-" * 118)
P("B5  BOTH KEEP PATHS on every grid point")
P("-" * 118)
for c in RUNGS:
    s = G[G.cost == c]
    P(f"  @{c}bps: 4a passes {int(s.pass4a.sum())}/{len(s)} "
      f"(ranked {int(s[s.ranked].pass4a.sum())}/{len(s[s.ranked])}, "
      f"un-ranked {int(s[~s.ranked].pass4a.sum())}/{len(s[~s.ranked])});  "
      f"4b passes {int(s.pass4b.sum())}/{len(s)} "
      f"(ranked {int(s[s.ranked].pass4b.sum())}, un-ranked {int(s[~s.ranked].pass4b.sum())});  "
      f"BOTH paths {int((s.pass4a & s.pass4b).sum())}")
pd.DataFrame([dict(param="n", values=str(N_GRID)), dict(param="gross", values=str(G_GRID)),
              dict(param="cost_bps (reported, not tuned)", values=str(RUNGS)),
              dict(param="freq (fixed)", values=FREQ),
              dict(param="IS_END", values=IS_END)]).to_csv(
    OUT / f"{STEM}.params.csv", index=False)

P("\n" + "=" * 118)
P(f"done in {time.time() - T0:.1f}s")
P("=" * 118)
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")

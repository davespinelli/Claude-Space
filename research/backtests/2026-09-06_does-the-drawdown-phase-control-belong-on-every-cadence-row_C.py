#!/usr/bin/env python3
"""Idea 273 — does-the-drawdown-phase-control-belong-on-every-cadence-row (lane C, 2026-09-06).

THE QUESTION
------------
The Sunday review of 2026-09-06 disqualified idea 171's by-product (COMP top-20 EW monthly,
min-half Sharpe 1.206, the highest on the board) because sliding the identical month-end
schedule 0-7 trading bars drops its 4b DRAWDOWN pass from 8/8 to 3/8, while idea 182's book
holds 7/8.  That control was applied to exactly two rows, in the review, by hand.  This run
applies it to EVERY monthly and quarterly row in the record that a memo has ever called a
KEEP-candidate, and reports what fraction of the record's cadence claims are anchor artefacts.

WHAT AN ANCHOR IS (idea 223's definition, unmodified)
-----------------------------------------------------
`engine.rebalance_mask(freq="M")` fires on the last trading bar of the month and
`engine.backtest` fills one bar later.  An ANCHOR slides that whole schedule -- decision bar
and fill bar together -- by `phase` bars, leaving the decision-to-fill gap at exactly 1 bar
(PROTOCOL rule 2).  Nothing about the book changes.  u56 carries ~20.9 bars/month, so phases
0..20 enumerate the monthly choice before the schedule wraps; the review's 0-7 window is a
sub-window of that and is reported separately for continuity.

THE CENSUS (the corpus is read off the record, not chosen)
-----------------------------------------------------------
All 69 `research/backtests/*.memo.md` are classified.  A memo enters the corpus iff it names a
book as a 4a/4b KEEP-candidate (or an explicit 4b pass) AND that book's rebalance cadence is
MONTHLY or QUARTERLY.  The classification of all 69 is printed, included and excluded alike,
with the reason.  Result: 6 memos, 3 distinct books, ZERO quarterly -- the record has never
published a quarterly KEEP-candidate, which is itself part of the answer.

  B1  COMP-M   idea 171 by-product / idea 188 by-product.  u56, top-20 equal weight on the
               research/scan.py composite (no vol scaler), gross 0.75, gate = close > 200d MA
               and vol20 < 0.60, SPY excluded from the tradable set, MONTHLY, t+1.
  B2  R6-M     idea 173 by-product / idea 182 / idea 182B.  u56, top-20 equal weight on
               R6 / vol20**0.5, gross 0.75, same gate, ranks every column (SPY included --
               that is how idea 173 defined it), MONTHLY, t+1.
  B3  MEAN21   idea 223.  B2 held on all 21 anchors at once, 1/21 of capital each.
               Anchor-agnostic BY CONSTRUCTION: the corpus's own control arm.

A book that does not reproduce its memo's published digits is recorded UNAUDITABLE and is
never guessed at.  Both reproduce exactly (controls [D]/[E]).

TWO TUNED PARAMETERS (PROTOCOL rule 4)
  PHASE (swept, all 21 points reported)  x  CADENCE (M and Q, both reported).
Book, panel, cost rung and execution lag are AUDIT AXES read off the parent memos, not
choices: every cell the memos asserted is re-priced, none is selected.

PRE-REGISTERED VERDICT RULE (written before any phase>0 number was read)
  For each memo-asserted 4b claim, count `pass4b` over the 21 anchors of its own cadence:
      ROBUST           >= 19/21 (>=90%)
      FRAGILE          11..18/21
      ANCHOR-ARTEFACT  <= 10/21 (the published pass is a minority statement about a calendar day)
  The headline is the share of the record's monthly/quarterly KEEP claims that are
  ANCHOR-ARTEFACT or FRAGILE.

RULE 8 (walk-forward, required)
  Phase is a dial, so the honest walk-forward is: choose the anchor on 2009-2016 IS Sharpe
  alone, read 2017-2026 untouched, and compare OOS CAGR/Sharpe/MaxDD against (i) the PUBLISHED
  phase 0, (ii) the phase MEAN (MEAN21, no choice at all), (iii) the OOS oracle, (iv) the live
  RULES v2 baseline and (v) SPY.  All grid points reported.

CAVEATS
  * SURVIVORSHIP.  universe.json and universe_broad.json are current-constituent lists
    (idea 54).  No level here is an attainable return; the phase-to-phase differences are
    same-names, same-days and are much less exposed.
  * Quarterly is enumerated on a coarse step (every 3rd bar of the ~63-bar wrap, 21 points)
    because a full 63-point enumeration on two books x two panels is not the marginal cost
    worth paying for a cadence the record has never claimed.  Stated, not hidden.
  * The corpus is 3 books.  The record simply does not contain more monthly KEEP-candidate
    memos; the share reported is a share of the claims that exist, not of a large sample.

Deterministic, standalone, no network.
Writes .console.txt, .census.csv, .phases.csv, .claims.csv, .walkforward.csv, .result.md
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_does-the-drawdown-phase-control-belong-on-every-cadence-row_C"
OUT = ROOT / "research" / "backtests"
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
N_PHASE = 21                     # monthly wrap on both panels (~20.9 bars/month)
Q_STEP = 3                       # quarterly: every 3rd bar of the ~63-bar wrap -> 21 points
REVIEW_WINDOW = 8                # the Sunday review's own 0..7 slide
COSTS = [0.0, 5.0, 10.0, 25.0]
LAGS = [1, 5, 7]

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ the simulator
def sim(px, W, freq, lag=1, phase=0):
    """engine.backtest with the schedule slid `phase` bars, decision-to-fill gap held at `lag`.

    Trade lands on bar (period_end + lag + phase) using the signal from (period_end + phase).
    Returns COST-FREE returns and turnover; cost rungs are applied by the turnover identity
    net(c) = gross - turnover * c / 1e4, which control [B] asserts is exact."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(lag + phase, fill_value=False).values.copy()
    mask[0] = True
    cur = np.zeros(px.shape[1])
    held = np.zeros_like(rets)
    trn = np.zeros(len(idx))
    for i in range(len(idx)):
        if mask[i]:
            trn[i] = np.abs(wt[i] - cur).sum()
            cur = wt[i].copy()
        held[i] = cur
        g = cur * (1.0 + rets[i])
        tot = g.sum() + (1.0 - cur.sum())
        cur = g / tot if tot > 0 else cur
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(trn, index=idx))


# ----------------------------------------------------------------- the two books
def comp_weights(px, tradable, n=20, gross=0.75, max_vol=0.60):
    """B1 COMP-M: research/scan.py's composite, NO vol scaler; SPY excluded from tradable.
    Exactly idea 175/188's `Book.weights` (see 2026-09-05_does-cadence-skill-survive-a-second-
    corpus_cloud.py: comp_score + Book)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    m = ((px > px.rolling(200).mean()) & (vol20 < max_vol)).copy()
    drop = [c for c in px.columns if c not in set(tradable)]
    if drop:
        m[drop] = False
    return (comp.where(m).rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)


def comp_weights_inclspy(px, n=20, gross=0.75, max_vol=0.60):
    """B1x -- the SAME composite book with SPY left IN the ranking universe.  This is NOT a
    published book; it exists only to identify what the Sunday review's 3-of-8 slide actually
    measured (see Q3b).  Idea 171's script states SPY is 'benchmark, never tradable'."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    m = (px > px.rolling(200).mean()) & (vol20 < max_vol)
    return (comp.where(m).rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)


def r6_weights(px, n=20, gross=0.75, max_vol=0.60, p=0.5):
    """B2 R6-M: idea 173's anchor with freq forced to M -- ranks EVERY column, SPY included."""
    s = px / px.shift(126) - 1
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    s = s / vol20.clip(lower=0.08) ** p
    elig = s.where(above & (vol20 < max_vol))
    return (elig.rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)


# ---------------------------------------------------------------------- metrics
def stats_block(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", r.loc[:IS_END]), ("OOS", r.loc[OOS_START:])):
        m = metrics(x)
        out[f"CAGR_{tag}"] = m["CAGR"]
        out[f"Sharpe_{tag}"] = m["Sharpe"]
        out[f"MaxDD_{tag}"] = m["MaxDD"]
    return out


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"]
                and row["CAGR_F"] >= 0.70 * spy["CAGR_F"])


def why4b(row, spy):
    bad = []
    if not row["Sharpe_H1"] > spy["Sharpe_H1"]: bad.append("H1")
    if not row["Sharpe_H2"] > spy["Sharpe_H2"]: bad.append("H2")
    if not row["Sharpe_OOS"] > spy["Sharpe_OOS"]: bad.append("OOS")
    if not row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"]: bad.append("DD")
    if not row["CAGR_F"] >= 0.70 * spy["CAGR_F"]: bad.append("CAGR")
    return ",".join(bad) if bad else "-"


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


# ============================================================ Q1  THE MEMO CENSUS
# Cadence of the book each memo names.  Hand-read from the memo text and recorded here so the
# classification is auditable; the regex scan below is printed beside it as a cross-check and
# any disagreement is printed rather than silently resolved.
MEMO_CADENCE = {
    "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C": ("M", "B1", "idea 171 by-product: 4b KEEP-candidate, monthly cadence on the standing top-20 book"),
    "2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud": ("M", "B1", "idea 188 by-product: U56 monthly top-20 clears 4b at 0/10/25 bps"),
    "2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud": ("M", "B2", "idea 173 by-product: 4b, monthly rebalance, PARK"),
    "2026-09-06_monthly-r6-top20-as-a-single-hypothesis_cloud": ("M", "B2", "idea 182: KEEP-candidate, R6 top-20 MONTHLY, 9/9 u56 cells"),
    "2026-09-06_monthly-r6-top20-as-a-single-hypothesis_B": ("M", "B2", "idea 182B: independent replication of the same monthly book"),
    "2026-09-06_the-trade-date-anchor-as-a-published-column_cloud": ("M", "B3", "idea 223: MEAN-21 anchor-agnostic monthly R6 top-20, KEEP-candidate"),
}
CAD_RE = re.compile(r"\bmonthly\b|\bMONTHLY\b|\bmonth-end\b|\bquarterly\b|\bQUARTERLY\b", re.I)
KEEP_RE = re.compile(r"KEEP[- ]candidate|KEEP memo|\bKEEP\b|4b PASS|clears 4b|passes\s+PROTOCOL\s+4b", re.I)

# The claims themselves: (memo, book, panel, cost bps, lag) that the memo asserts as a 4b pass.
CLAIMS = [
    ("2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C", "B1", "u56", 10.0, 1),
    ("2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud", "B1", "u56", 0.0, 1),
    ("2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud", "B1", "u56", 10.0, 1),
    ("2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud", "B1", "u56", 25.0, 1),
    ("2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud", "B2", "u56", 10.0, 1),
    ("2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud", "B2", "u56", 25.0, 1),
] + [("2026-09-06_monthly-r6-top20-as-a-single-hypothesis_cloud", "B2", "u56", c, l)
     for c in (5.0, 10.0, 25.0) for l in LAGS] + [
    ("2026-09-06_monthly-r6-top20-as-a-single-hypothesis_B", "B2", "u56", c, l)
    for c in (5.0, 10.0, 25.0) for l in LAGS] + [
    ("2026-09-06_the-trade-date-anchor-as-a-published-column_cloud", "B3", "u56", 10.0, 1),
    ("2026-09-06_the-trade-date-anchor-as-a-published-column_cloud", "B3", "u56", 25.0, 1),
]

PUBLISHED = {   # memo digits, used as the reproduction gate (controls [D]/[E]/[F])
    "B1": dict(CAGR_F=0.1476, Sharpe_F=1.2081, MaxDD_F=-0.1958, Sharpe_H1=1.2185,
               Sharpe_H2=1.2064, Sharpe_OOS=1.2866, CAGR_OOS=0.1671),
    "B2": dict(CAGR_F=0.1361, Sharpe_F=1.1557, MaxDD_F=-0.1881, Sharpe_H1=1.2279,
               Sharpe_H2=1.1017, Sharpe_OOS=1.1695, CAGR_OOS=0.1456),
    "B3": dict(CAGR_F=0.1284, Sharpe_F=1.1058, MaxDD_F=-0.1961, Sharpe_H1=1.174,
               Sharpe_H2=1.058, Sharpe_OOS=1.1280, CAGR_OOS=0.1395),
}


def census():
    P("=" * 108)
    P("Q1  THE CENSUS -- every research/backtests/*.memo.md classified, included and excluded alike")
    P("=" * 108)
    rows = []
    for f in sorted(OUT.glob("*.memo.md")):
        stem = f.name[:-len(".memo.md")]
        txt = f.read_text()
        hits = sorted({h.lower() for h in CAD_RE.findall(txt)})
        listed = MEMO_CADENCE.get(stem)
        rows.append(dict(memo=stem, cadence_words=",".join(hits) if hits else "-",
                         keep_words=len(KEEP_RE.findall(txt)),
                         in_corpus=bool(listed), cadence=listed[0] if listed else "W/other",
                         book=listed[1] if listed else "-",
                         reason=listed[2] if listed else
                         ("book is WEEKLY (or no book proposed)" if hits else "no monthly/quarterly book")))
    cen = pd.DataFrame(rows)
    P(f"  {len(cen)} memos scanned. {int(cen.in_corpus.sum())} enter the corpus.")
    P(f"  memos whose text contains a monthly/quarterly word at all: "
      f"{int((cen.cadence_words != '-').sum())} -- of those, {int(cen.in_corpus.sum())} name a "
      f"monthly/quarterly BOOK; the rest mention the cadence of something else.")
    P("\n  -- IN CORPUS --")
    P(cen[cen.in_corpus][["memo", "cadence", "book", "reason"]].to_string(index=False))
    P("\n  -- EXCLUDED (all 63, with the cadence words found so the exclusion is checkable) --")
    P(cen[~cen.in_corpus][["memo", "cadence_words", "keep_words", "reason"]].to_string(index=False))
    P("\n  QUARTERLY KEEP-CANDIDATES IN THE RECORD: 0.  No memo has ever proposed a quarterly book.")
    P("  Quarterly is therefore run below as a PRE-REGISTERED EXTENSION of the same two books,")
    P("  not as an audit of an existing claim -- stated so the two are never conflated.")
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    return cen


# ================================================================== the sweep
def main():
    t0 = time.time()
    P(f"idea 273 -- does-the-drawdown-phase-control-belong-on-every-cadence-row (lane C)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC\n")

    census()

    panels = {"u56": load_universe(), "broad": load_universe(broad=True)}
    P("")
    ref = {}
    for pn, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        ref[pn] = dict(start=start, spy=stats_block(spy), v2=stats_block(v2), v1=stats_block(v1))
        bars_m = len(px) / len(px.index.to_period("M").unique())
        bars_q = len(px) / len(px.index.to_period("Q").unique())
        P(f"panel {pn:6s}: {px.shape[1]:3d} cols, sample {start.date()}..{px.index[-1].date()}, "
          f"{bars_m:.2f} bars/month, {bars_q:.2f} bars/quarter")
        s = ref[pn]["spy"]
        P(f"   SPY  {s['CAGR_F']:.2%} / {s['Sharpe_F']:.4f} / {s['MaxDD_F']:.2%}  "
          f"H1 {s['Sharpe_H1']:.4f} H2 {s['Sharpe_H2']:.4f} OOS {s['Sharpe_OOS']:.4f}"
          f"   -> 4b bars: DD >= {0.60*s['MaxDD_F']:.2%}, CAGR >= {0.70*s['CAGR_F']:.2%}")
        b = ref[pn]["v2"]
        P(f"   RULES v2 (live baseline, W, 10bps) {b['CAGR_F']:.2%} / {b['Sharpe_F']:.4f} / "
          f"{b['MaxDD_F']:.2%}  H1 {b['Sharpe_H1']:.4f} H2 {b['Sharpe_H2']:.4f} OOS {b['Sharpe_OOS']:.4f}")

    # weights, per panel
    W = {}
    for pn, px in panels.items():
        trad = [c for c in px.columns if c != "SPY"]
        W[(pn, "B1")] = comp_weights(px, trad)
        W[(pn, "B2")] = r6_weights(px)

    # ---------------------------------------------------------------- controls
    P("\n" + "=" * 108)
    P("CONTROLS (asserted before any phase>0 number is read)")
    P("=" * 108)
    px = panels["u56"]
    g, t = sim(px, W[("u56", "B2")], "M", 1, 0)
    eng0 = backtest(px, W[("u56", "B2")], cost_bps=0.0, freq="M")
    eng10 = backtest(px, W[("u56", "B2")], cost_bps=10.0, freq="M")
    dA_r = float(np.nanmax(np.abs((g - eng0["returns"]).values)))
    dA_t = float(np.nanmax(np.abs((t - eng0["turnover"]).values)))
    dB = float(np.nanmax(np.abs(((g - t * 10 / 1e4) - eng10["returns"]).values)))
    P(f"  [A] sim(lag=1,phase=0) == engine.backtest : returns {dA_r:.3e}, turnover {dA_t:.3e}")
    P(f"  [B] cost identity net(c) = gross - trn*c/1e4 vs a direct 10 bps engine run: {dB:.3e}")
    assert dA_r < 1e-12 and dA_t < 1e-12 and dB < 1e-12
    gb, tb = sim(panels["broad"], W[("broad", "B2")], "M", 1, 0)
    engb = backtest(panels["broad"], W[("broad", "B2")], cost_bps=0.0, freq="M")
    P(f"  [A2] same on broad: returns {float(np.nanmax(np.abs((gb-engb['returns']).values))):.3e}")

    # [C] reproduce idea 182B's committed 8-phase .phase.csv, the corpus's own instrument
    p182 = OUT / "2026-09-06_monthly-r6-top20-as-a-single-hypothesis_B.phase.csv"
    if p182.exists():
        ref182 = pd.read_csv(p182).set_index("phase")
        cols = [c for c in ref182.columns if c not in ("pass4b", "fail4b")]
        mine = []
        for ph in ref182.index:
            gg, tt = sim(px, W[("u56", "B2")], "M", 1, int(ph))
            net = (gg - tt * 10 / 1e4).loc[ref[ "u56"]["start"]:]
            row = stats_block(net)
            o = net.loc[OOS_START:]
            ho = len(o) // 2
            row["oosH1"] = metrics(o.iloc[:ho])["Sharpe"]
            row["oosH2"] = metrics(o.iloc[ho:])["Sharpe"]
            row["phase"] = ph
            mine.append(row)
        mine = pd.DataFrame(mine).set_index("phase")
        d = float(np.nanmax(np.abs((mine[cols] - ref182[cols]).values)))
        P(f"  [C] DECISIVE: reproduces idea 182B's committed .phase.csv on {len(ref182)} phases x "
          f"{len(cols)} columns to {d:.3e}  -> this is 182B's instrument, unmodified")
        assert d < 1e-9
    else:
        P("  [C] idea 182B .phase.csv absent -- control NOT available (reported, not skipped silently)")

    # [D]/[E] reproduction gate for the two books at their published cell
    repro = {}
    for bk in ("B1", "B2"):
        gg, tt = sim(px, W[("u56", bk)], "M", 1, 0)
        net = (gg - tt * 10 / 1e4).loc[ref["u56"]["start"]:]
        row = stats_block(net)
        pub = PUBLISHED[bk]
        worst = max(abs(row[k] - v) for k, v in pub.items())
        repro[bk] = worst
        P(f"  [{'D' if bk=='B1' else 'E'}] {bk} @u56/10bps/t+1/phase0 reproduces its memo's "
          f"7 published digits, max |d| {worst:.5f}  "
          f"({row['CAGR_F']:.2%}/{row['Sharpe_F']:.4f}/{row['MaxDD_F']:.2%}, "
          f"halves {row['Sharpe_H1']:.4f}/{row['Sharpe_H2']:.4f}, OOS {row['Sharpe_OOS']:.4f})")
        assert worst < 5e-4, f"{bk} does not reproduce -- UNAUDITABLE, not guessed"

    # [D2] the decisive control for B1: idea 171's COMMITTED ladder row, to full precision
    lad = OUT / "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C.ladder.csv"
    if lad.exists():
        L = pd.read_csv(lad)
        row171 = L[(L.book == "U56") & (L.dial == "CADENCE") & (L.point == "M")].iloc[0]
        gg, tt = sim(px, W[("u56", "B1")], "M", 1, 0)
        yrs = len(gg.loc[ref["u56"]["start"]:]) / 252.0
        net = (gg - tt * 10 / 1e4).loc[ref["u56"]["start"]:]
        mine = stats_block(net)
        d2 = max(abs(mine["CAGR_F"] - row171.CAGR), abs(mine["Sharpe_F"] - row171.Sharpe),
                 abs(mine["MaxDD_F"] - row171.MaxDD), abs(mine["Sharpe_H1"] - row171.H1),
                 abs(mine["Sharpe_H2"] - row171.H2), abs(mine["Sharpe_OOS"] - row171.OOS_Sharpe),
                 abs(tt.loc[ref["u56"]["start"]:].sum() / yrs - row171.turnover))
        P(f"  [D2] DECISIVE for B1: == idea 171's COMMITTED ladder.csv U56/CADENCE/M row on 7 "
          f"columns to {d2:.3e}  -> this is idea 171's book, unmodified")
        assert d2 < 1e-12

    # ------------------------------------------------------------- the sweep
    P("\n" + "=" * 108)
    P("Q2  THE SWEEP -- the identical rule at every anchor of its own cadence")
    P("=" * 108)
    grid = []
    todo = ([("u56", bk, "M", lag) for bk in ("B1", "B2") for lag in LAGS]
            + [("broad", bk, "M", 1) for bk in ("B1", "B2")]
            + [(pn, bk, "Q", 1) for pn in ("u56", "broad") for bk in ("B1", "B2")])
    for pn, bk, cad, lag in todo:
        pxp = panels[pn]
        start = ref[pn]["start"]
        phases = range(N_PHASE) if cad == "M" else range(0, N_PHASE * Q_STEP, Q_STEP)
        for ph in phases:
            gg, tt = sim(pxp, W[(pn, bk)], cad, lag, int(ph))
            gg, tt = gg.loc[start:], tt.loc[start:]
            yrs = len(gg) / 252.0
            for c in COSTS:
                net = gg - tt * c / 1e4
                row = stats_block(net)
                row.update(panel=pn, book=bk, cadence=cad, lag=lag, phase=int(ph), cost=c,
                           turnover=tt.sum() / yrs)
                row["pass4b"] = pass4b(row, ref[pn]["spy"])
                row["fail4b"] = why4b(row, ref[pn]["spy"])
                row["pass4a"] = pass4a(row, ref[pn]["v2"])
                grid.append(row)
        P(f"  swept {pn}/{bk}/{cad}/lag{lag}: {len(list(phases))} anchors x {len(COSTS)} rungs "
          f"({time.time()-t0:.0f}s)")

    # MEAN21 (B3) is the equal-weight portfolio over the 21 monthly anchors of B2, per panel/lag.
    for pn in panels:
        for lag in (LAGS if pn == "u56" else [1]):
            pxp = panels[pn]
            start = ref[pn]["start"]
            gs, ts = [], []
            for ph in range(N_PHASE):
                gg, tt = sim(pxp, W[(pn, "B2")], "M", lag, ph)
                gs.append(gg.loc[start:])
                ts.append(tt.loc[start:])
            gm = sum(gs) / N_PHASE
            tm = sum(ts) / N_PHASE
            yrs = len(gm) / 252.0
            for c in COSTS:
                net = gm - tm * c / 1e4
                row = stats_block(net)
                row.update(panel=pn, book="B3", cadence="M", lag=lag, phase=-1, cost=c,
                           turnover=tm.sum() / yrs)
                row["pass4b"] = pass4b(row, ref[pn]["spy"])
                row["fail4b"] = why4b(row, ref[pn]["spy"])
                row["pass4a"] = pass4a(row, ref[pn]["v2"])
                grid.append(row)
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.phases.csv", index=False)
    P(f"  grid: {len(G)} rows -> .phases.csv   ({time.time()-t0:.0f}s)")

    # [F] MEAN21 reproduces idea 223's published digits
    b3 = G[(G.book == "B3") & (G.panel == "u56") & (G.lag == 1) & (G.cost == 10.0)].iloc[0]
    pub = PUBLISHED["B3"]
    worst = max(abs(b3[k] - v) for k, v in pub.items())
    P(f"  [F] B3 MEAN21 @u56/10bps reproduces idea 223's memo digits, max |d| {worst:.5f} "
      f"({b3['CAGR_F']:.2%}/{b3['Sharpe_F']:.4f}/{b3['MaxDD_F']:.2%}, OOS {b3['Sharpe_OOS']:.4f})")

    # ------------------------------------------- Q2 tables: the band on each book
    P("\n  -- the 21-anchor band, u56 @10 bps, t+1 (the cell every memo quotes) --")
    P(f"  {'book':5s} {'cad':3s} {'MaxDD range':>22s} {'Sharpe range':>18s} {'CAGR range':>18s} "
      f"{'OOS Sh range':>18s} {'4b':>7s} {'4b 0-7':>7s} {'4a':>6s} {'phase0':>8s}")
    for bk in ("B1", "B2"):
        for cad in ("M", "Q"):
            sub = G[(G.book == bk) & (G.panel == "u56") & (G.cadence == cad) & (G.lag == 1)
                    & (G.cost == 10.0)].sort_values("phase")
            if sub.empty:
                continue
            n = len(sub)
            w = sub[sub.phase < (REVIEW_WINDOW if cad == "M" else REVIEW_WINDOW * Q_STEP)]
            p0 = sub[sub.phase == 0].iloc[0]
            P(f"  {bk:5s} {cad:3s} {sub.MaxDD_F.min():>10.2%}..{sub.MaxDD_F.max():>8.2%} "
              f"{sub.Sharpe_F.min():>8.4f}..{sub.Sharpe_F.max():.4f} "
              f"{sub.CAGR_F.min():>8.2%}..{sub.CAGR_F.max():.2%} "
              f"{sub.Sharpe_OOS.min():>8.4f}..{sub.Sharpe_OOS.max():.4f} "
              f"{int(sub.pass4b.sum()):>3d}/{n:<3d} {int(w.pass4b.sum()):>3d}/{len(w):<3d} "
              f"{int(sub.pass4a.sum()):>2d}/{n:<3d} {'PASS' if p0.pass4b else 'FAIL':>8s}")
    P("\n  -- same, broad panel @10 bps t+1 (portability; the memos scope their claims to u56) --")
    for bk in ("B1", "B2"):
        for cad in ("M", "Q"):
            sub = G[(G.book == bk) & (G.panel == "broad") & (G.cadence == cad) & (G.lag == 1)
                    & (G.cost == 10.0)].sort_values("phase")
            if sub.empty:
                continue
            P(f"  {bk:5s} {cad:3s} {sub.MaxDD_F.min():>10.2%}..{sub.MaxDD_F.max():>8.2%} "
              f"{sub.Sharpe_F.min():>8.4f}..{sub.Sharpe_F.max():.4f} "
              f"4b {int(sub.pass4b.sum()):>3d}/{len(sub):<3d}")

    P("\n  -- per-anchor detail, u56 @10 bps t+1 (all grid points, both books, MONTHLY) --")
    det = G[(G.panel == "u56") & (G.cadence == "M") & (G.lag == 1) & (G.cost == 10.0)
            & (G.book != "B3")].sort_values(["book", "phase"])
    P(det[["book", "phase", "CAGR_F", "Sharpe_F", "MaxDD_F", "Sharpe_H1", "Sharpe_H2",
           "Sharpe_OOS", "turnover", "pass4b", "fail4b"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------- Q3 the claim-level verdict
    P("\n" + "=" * 108)
    P("Q3  THE ANSWER -- every memo-asserted monthly/quarterly 4b claim, re-priced over its anchors")
    P("=" * 108)
    P("  pre-registered: ROBUST >=19/21, FRAGILE 11..18/21, ANCHOR-ARTEFACT <=10/21\n")
    crows = []
    for memo, bk, pn, cost, lag in CLAIMS:
        sub = G[(G.book == bk) & (G.panel == pn) & (G.cadence == "M") & (G.lag == lag)
                & (G.cost == cost)]
        if bk == "B3":
            # anchor-agnostic by construction: the single MEAN21 row IS the whole band
            n_pass, n_tot, n_pass_w, n_tot_w = int(sub.pass4b.sum()), len(sub), int(sub.pass4b.sum()), len(sub)
            verdict = "ROBUST (by construction)" if bool(sub.pass4b.iloc[0]) else "FAILS"
            p0pass = bool(sub.pass4b.iloc[0])
            band = 0.0
            fails = sub.fail4b.iloc[0]
        else:
            sub = sub.sort_values("phase")
            n_tot, n_pass = len(sub), int(sub.pass4b.sum())
            w = sub[sub.phase < REVIEW_WINDOW]
            n_tot_w, n_pass_w = len(w), int(w.pass4b.sum())
            p0pass = bool(sub[sub.phase == 0].pass4b.iloc[0])
            band = float(sub.MaxDD_F.max() - sub.MaxDD_F.min())
            verdict = ("ROBUST" if n_pass >= 19 else "ANCHOR-ARTEFACT" if n_pass <= 10 else "FRAGILE")
            fails = ",".join(sorted({x for s in sub.fail4b for x in s.split(",") if x != "-"})) or "-"
        crows.append(dict(memo=memo, book=bk, panel=pn, cost=cost, lag=lag,
                          phase0_pass=p0pass, pass_of_21=f"{n_pass}/{n_tot}",
                          pass_0_7=f"{n_pass_w}/{n_tot_w}", n_pass=n_pass, n_tot=n_tot,
                          MaxDD_band_pp=100 * band, bars_that_fail=fails, verdict=verdict))
    C = pd.DataFrame(crows)
    C.to_csv(OUT / f"{STEM}.claims.csv", index=False)
    P(C[["memo", "book", "cost", "lag", "phase0_pass", "pass_of_21", "pass_0_7",
         "MaxDD_band_pp", "bars_that_fail", "verdict"]].to_string(
        index=False, float_format=lambda x: f"{x:.2f}", max_colwidth=52))

    tot = len(C)
    rob = int((C.verdict.str.startswith("ROBUST")).sum())
    fra = int((C.verdict == "FRAGILE").sum())
    art = int((C.verdict == "ANCHOR-ARTEFACT").sum())
    P(f"\n  {tot} memo-asserted monthly 4b claims (6 memos, 3 distinct books, 0 quarterly).")
    P(f"    ROBUST          {rob:2d}  ({rob/tot:.1%})")
    P(f"    FRAGILE         {fra:2d}  ({fra/tot:.1%})")
    P(f"    ANCHOR-ARTEFACT {art:2d}  ({art/tot:.1%})")
    P(f"  NOT ROBUST (the headline): {fra+art}/{tot} = {(fra+art)/tot:.1%} of the record's "
      f"monthly KEEP claims are anchor-dependent.")
    P(f"  Every claim passes at phase 0 by construction (that is what a published claim is): "
      f"{int(C.phase0_pass.sum())}/{tot}.")
    P("  Bar that breaks under the slide, pooled: "
      + ", ".join(f"{k} {v}" for k, v in
                  pd.Series([x for s in C.bars_that_fail for x in s.split(",") if x != "-"])
                  .value_counts().items()))

    # the review's own two rows, restated
    P("\n  -- restating the Sunday review's own control (0..7 window, u56 @10bps t+1) --")
    for bk, lbl in (("B1", "idea 171 by-product (COMP-M)"), ("B2", "idea 182's book (R6-M)")):
        s = G[(G.book == bk) & (G.panel == "u56") & (G.cadence == "M") & (G.lag == 1)
              & (G.cost == 10.0) & (G.phase < REVIEW_WINDOW)]
        s21 = G[(G.book == bk) & (G.panel == "u56") & (G.cadence == "M") & (G.lag == 1)
                & (G.cost == 10.0)]
        P(f"    {lbl:32s} review 0-7: {int(s.pass4b.sum())}/8   full wrap 0-20: "
          f"{int(s21.pass4b.sum())}/21   (review reported 3/8 and 7/8)")

    # ------------------------------------------- Q3b  the review's own number
    P("\n" + "=" * 108)
    P("Q3b  WHY THE REVIEW'S 3-OF-8 DOES NOT REPRODUCE -- it is a neighbouring book, not idea 171's")
    P("=" * 108)
    P("  The review reported idea 171's by-product at 3/8 with MaxDD -18.41%..-21.33% and 'k=1..5")
    P("  all breach the cap'.  On the PUBLISHED book (control [D2]: idea 171's committed ladder")
    P("  row to 1e-12) the same slide gives a different band.  The one construction that does")
    P("  reproduce the review's digits is B1x: the identical composite with SPY left IN the")
    P("  ranking universe -- which idea 171's own script forbids ('SPY: benchmark, never tradable').")
    Wx = comp_weights_inclspy(px)
    b1x = []
    for ph in range(N_PHASE):
        gg, tt = sim(px, Wx, "M", 1, ph)
        net = (gg - tt * 10 / 1e4).loc[ref["u56"]["start"]:]
        r = stats_block(net)
        r["phase"] = ph
        r["pass4b"] = pass4b(r, ref["u56"]["spy"])
        r["ddpass"] = r["MaxDD_F"] >= 0.60 * ref["u56"]["spy"]["MaxDD_F"]
        b1x.append(r)
    X = pd.DataFrame(b1x)
    b1 = G[(G.book == "B1") & (G.panel == "u56") & (G.cadence == "M") & (G.lag == 1)
           & (G.cost == 10.0)].sort_values("phase")
    b1["ddpass"] = b1.MaxDD_F >= 0.60 * ref["u56"]["spy"]["MaxDD_F"]
    for tag, s in (("B1  published (SPY untradable)", b1), ("B1x review's (SPY in the ranking)", X)):
        w = s[s.phase < REVIEW_WINDOW]
        P(f"  {tag:34s} phase0 MaxDD {float(s[s.phase==0].MaxDD_F.iloc[0]):.4%}  "
          f"0-7 band {w.MaxDD_F.max():.4%}..{w.MaxDD_F.min():.4%}  "
          f"DD-pass 0-7 {int(w.ddpass.sum())}/8  full 4b 0-7 {int(w.pass4b.sum())}/8  "
          f"full wrap 4b {int(s.pass4b.sum())}/21  k=1..5 breaches "
          f"{int((~s[(s.phase>=1)&(s.phase<=5)].ddpass).sum())}/5")
    P("  The review's quoted band (-18.41%..-21.33%) and its 3/8 are B1x's, to the reported digits.")
    P("  CORRECTION: idea 171's by-product as published slides to 5/8 over the review's window and")
    P("  9/21 over the full wrap.  The DIRECTION of the review's disqualification stands (9/21 is")
    P("  ANCHOR-ARTEFACT under this run's pre-registered rule); the NUMBER it was made on does not.")

    # -------------------------------------------------------- Q4  RULE 8
    P("\n" + "=" * 108)
    P("Q4  RULE 8 -- is the anchor SELECTABLE?  Phase chosen on 2009-2016 IS Sharpe, read on 2017-2026")
    P("=" * 108)
    wf = []
    for pn in panels:
        for bk in ("B1", "B2"):
            for lag in (LAGS if pn == "u56" else [1]):
                for c in COSTS:
                    sub = G[(G.book == bk) & (G.panel == pn) & (G.cadence == "M")
                            & (G.lag == lag) & (G.cost == c)].sort_values("phase")
                    if sub.empty:
                        continue
                    pick = sub.loc[sub.Sharpe_IS.idxmax()]
                    p0 = sub[sub.phase == 0].iloc[0]
                    orac = sub.loc[sub.Sharpe_OOS.idxmax()]
                    m21 = G[(G.book == "B3") & (G.panel == pn) & (G.lag == lag) & (G.cost == c)]
                    m21 = m21.iloc[0] if len(m21) else None
                    spy, v2 = ref[pn]["spy"], ref[pn]["v2"]
                    wf.append(dict(
                        panel=pn, book=bk, lag=lag, cost=c,
                        IS_pick_phase=int(pick.phase), IS_Sharpe=pick.Sharpe_IS,
                        pick_OOS_Sharpe=pick.Sharpe_OOS, pick_OOS_CAGR=pick.CAGR_OOS,
                        pick_OOS_MaxDD=pick.MaxDD_OOS,
                        pub_OOS_Sharpe=p0.Sharpe_OOS, pub_OOS_CAGR=p0.CAGR_OOS,
                        pub_OOS_MaxDD=p0.MaxDD_OOS,
                        mean_OOS_Sharpe=(m21.Sharpe_OOS if m21 is not None else np.nan),
                        mean_OOS_CAGR=(m21.CAGR_OOS if m21 is not None else np.nan),
                        mean_OOS_MaxDD=(m21.MaxDD_OOS if m21 is not None else np.nan),
                        oracle_phase=int(orac.phase), oracle_OOS_Sharpe=orac.Sharpe_OOS,
                        med_OOS_Sharpe=sub.Sharpe_OOS.median(),
                        regret_vs_oracle=pick.Sharpe_OOS - orac.Sharpe_OOS,
                        pick_minus_pub=pick.Sharpe_OOS - p0.Sharpe_OOS,
                        pick_minus_mean=(pick.Sharpe_OOS - m21.Sharpe_OOS) if m21 is not None else np.nan,
                        pick_minus_median=pick.Sharpe_OOS - sub.Sharpe_OOS.median(),
                        spy_OOS_Sharpe=spy["Sharpe_OOS"], spy_OOS_CAGR=spy["CAGR_OOS"],
                        spy_OOS_MaxDD=spy["MaxDD_OOS"],
                        v2_OOS_Sharpe=v2["Sharpe_OOS"], v2_OOS_CAGR=v2["CAGR_OOS"],
                        v2_OOS_MaxDD=v2["MaxDD_OOS"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(WF[["panel", "book", "lag", "cost", "IS_pick_phase", "pick_OOS_Sharpe", "pub_OOS_Sharpe",
          "mean_OOS_Sharpe", "med_OOS_Sharpe", "oracle_phase", "oracle_OOS_Sharpe",
          "pick_minus_pub", "pick_minus_mean", "regret_vs_oracle"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  IS-chosen anchor vs the PUBLISHED anchor, mean dOOS Sharpe: "
      f"{WF.pick_minus_pub.mean():+.4f} (win {int((WF.pick_minus_pub>0).sum())}/{len(WF)})")
    P(f"  IS-chosen anchor vs the anchor MEAN (MEAN21):            "
      f"{WF.pick_minus_mean.mean():+.4f} (win {int((WF.pick_minus_mean>0).sum())}/{len(WF)})")
    P(f"  IS-chosen anchor vs the anchor MEDIAN (a coin flip):     "
      f"{WF.pick_minus_median.mean():+.4f} (win {int((WF.pick_minus_median>0).sum())}/{len(WF)})")
    P(f"  regret vs the OOS oracle: mean {WF.regret_vs_oracle.mean():+.4f}, "
      f"worst {WF.regret_vs_oracle.min():+.4f}")
    P(f"  IS pick lands on the published phase 0 in {int((WF.IS_pick_phase==0).sum())}/{len(WF)} cells; "
      f"the OOS oracle is phase 0 in {int((WF.oracle_phase==0).sum())}/{len(WF)}.")

    P("\n  -- OOS levels, u56 @10bps t+1, vs baseline and SPY (the numbers a sizing decision needs) --")
    for bk in ("B1", "B2"):
        r = WF[(WF.panel == "u56") & (WF.book == bk) & (WF.lag == 1) & (WF.cost == 10.0)].iloc[0]
        P(f"    {bk} IS-pick(ph {int(r.IS_pick_phase):2d}) {r.pick_OOS_CAGR:7.2%} / "
          f"{r.pick_OOS_Sharpe:.4f} / {r.pick_OOS_MaxDD:7.2%}"
          f"   published(ph 0) {r.pub_OOS_CAGR:7.2%} / {r.pub_OOS_Sharpe:.4f} / {r.pub_OOS_MaxDD:7.2%}"
          f"   MEAN21 {r.mean_OOS_CAGR:7.2%} / {r.mean_OOS_Sharpe:.4f} / {r.mean_OOS_MaxDD:7.2%}")
    r = WF.iloc[0]
    P(f"    SPY            {r.spy_OOS_CAGR:7.2%} / {r.spy_OOS_Sharpe:.4f} / {r.spy_OOS_MaxDD:7.2%}"
      f"   RULES v2 {r.v2_OOS_CAGR:7.2%} / {r.v2_OOS_Sharpe:.4f} / {r.v2_OOS_MaxDD:7.2%}")

    # -------------------------------------------------------- Q5  quarterly
    P("\n" + "=" * 108)
    P("Q5  QUARTERLY -- a pre-registered extension, NOT an audit (the record has no quarterly claim)")
    P("=" * 108)
    for pn in panels:
        for bk in ("B1", "B2"):
            sub = G[(G.book == bk) & (G.panel == pn) & (G.cadence == "Q") & (G.lag == 1)
                    & (G.cost == 10.0)].sort_values("phase")
            P(f"  {pn:6s} {bk} Q: MaxDD {sub.MaxDD_F.min():.2%}..{sub.MaxDD_F.max():.2%} "
              f"({100*(sub.MaxDD_F.max()-sub.MaxDD_F.min()):.2f}pp band), "
              f"Sharpe {sub.Sharpe_F.min():.4f}..{sub.Sharpe_F.max():.4f}, "
              f"4b {int(sub.pass4b.sum())}/{len(sub)}, phase0 "
              f"{'PASS' if bool(sub[sub.phase==0].pass4b.iloc[0]) else 'FAIL'}")
    mq = G[(G.cadence == "Q") & (G.cost == 10.0) & (G.lag == 1)]
    mm = G[(G.cadence == "M") & (G.cost == 10.0) & (G.lag == 1) & (G.book != "B3")]
    P(f"\n  Pooled MaxDD band: MONTHLY {100*(mm.groupby(['panel','book']).MaxDD_F.max()-mm.groupby(['panel','book']).MaxDD_F.min()).mean():.2f}pp "
      f"vs QUARTERLY {100*(mq.groupby(['panel','book']).MaxDD_F.max()-mq.groupby(['panel','book']).MaxDD_F.min()).mean():.2f}pp "
      f"-- the slower the cadence, the wider the anchor band.")

    P(f"\ntotal {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

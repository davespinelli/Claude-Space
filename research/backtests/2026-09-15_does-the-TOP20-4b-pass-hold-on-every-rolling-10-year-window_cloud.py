#!/usr/bin/env python3
"""QUEUE idea 898 — does-the-TOP20-4b-pass-hold-on-EVERY-ROLLING-10-YEAR-WINDOW  (cloud, 2026-09-15).

QUESTION (pre-registered, verbatim from QUEUE.md idea 898)
    "every committed 4b verdict on this book is read on the one 2009-2026 window plus its 2017+
     tail; a book worth real capital should clear the bars on windows that start somewhere else
     too.  Report the 4b pass rate over all rolling windows at monthly starts, both KEEP paths
     per window.  Max 2 params (window length, start step)."

THE HYPOTHESES, written out in full BEFORE any number below was read
    H_ROBUST  the 4b pass is a property of the book, not of the one window it was read on: the
              book clears PROTOCOL 4b on >= 80% of rolling 10-year windows at monthly starts.
    H_LEG     if it does not, the failures are carried by ONE leg (the same leg the record's
              other 4b kills keep landing on — the CAGR floor), not spread across all four.
    H_START   the pass/fail is a START-DATE fact: the failing windows cluster in a contiguous
              block of start months rather than alternating.
    Declared before running: H_ROBUST is the one that matters for capital.  A book that clears
    4b on the one published window and fails most others is a window artefact, not an edge.

THE BOOK B*, IMPORTED not re-typed (2026-09-04 shelf KEEP 4b, as re-published by idea 879 lane B
and re-used verbatim by idea 897)
    signal    baseline.score(px, vol_scale=False) — mean of the cross-sectional percentile ranks
              of (px[t-21]/px[t-252]-1), (px/px[t-126]-1), (px/px[t-63]-1), times 1.0 if the close
              is above its 200d mean and 0.5 if not.  NO vol scaler.
    gate      px > 200d MA  AND  vol20 (annualised, 20d) < 0.60
    book      top 20 eligible by signal (pandas rank(ascending=False) <= 20, the record's own
              convention), equal weight g/20, shortfall to CASH, NEVER respread
    cadence   MONTHLY (engine's calendar-month-end mask), fills t+1, 10 bps
    gross     g = 0.65 IMPORTED from idea 879's published pass rung; NOT tuned here.
              g = 0.75 (the 2026-09-04 shelf's own rung) is carried as a reported AUDIT axis.
    Nothing about the book is chosen in this run.  This run only changes the WINDOW it is read on.

THE TWO TUNED PARAMETERS (the only two; every value of both is reported)
    LENGTH L  {5, 7, 10, 12} years.  L = 10 is the idea's pre-registered headline; the others are
              reported so the answer is not a single-length artefact.
    STEP      {1, 3} months between window starts.  1 month is the idea's pre-registered value.
    AUDIT axes (printed in full, never selected on): GROSS {0.65, 0.75}, COST {10, 25} bps.

PER-WINDOW VERDICT MECHANICS (stated before the run)
    A window w = [t0, t0 + L years).  Inside w, and using ONLY data inside w:
      4b_w   Sharpe(book) > Sharpe(SPY) in BOTH halves of w
             AND MaxDD_w >= 0.60 * MaxDD_w(SPY)      (i.e. no worse than 60% of SPY's)
             AND CAGR_w  >= 0.70 * CAGR_w(SPY)
      4a_w   Sharpe(book) > Sharpe(RULES v2 live) in BOTH halves of w
             AND MaxDD_w >= MaxDD_w(RULES v2)
    The out-of-sample leg of 4b (rule 8) is a whole-sample construct and cannot be read inside a
    rolling window; it is read ONCE, separately, in the rule-8 block below.  Every per-window 4b
    here is therefore the THREE-LEG in-window reading, and is labelled as such — it is a weaker
    bar than the full 4b, so a failure rate measured here is a LOWER bound on the true one.
    DEGENERATE FLOOR: in a window where SPY's CAGR is <= 0, "CAGR >= 70% of SPY's" is not a floor
    at all (a negative bar is cleared by anything above it, including losses).  Those windows are
    counted and the pass rate is reported both with and without them.

PROTOCOL rule 8 walk-forward (required, read once)
    IS = 2009-01-13 .. 2016-12-31, OOS = 2017-01-01 .. end, untouched until the selector fired.
    IS-PICK (declared here, before the run): among the lengths whose windows fit ENTIRELY inside
    IS — L in {5, 7} — take the L with the highest IS three-leg 4b pass rate at step = 1 month,
    ties broken by the LARGER L (the more demanding window).  The OOS pass rate at that L, over
    windows lying entirely in OOS, is then read ONCE.
    The book's own OOS triple (CAGR / Sharpe / MaxDD) is also read once against RULES v2 and SPY,
    with both KEEP paths evaluated on the OOS window.

GATES, printed before any hypothesis is read
    G1  the book reproduces its own committed triple from idea 879's memo (12.69% / 1.201 /
        -17.11% at g = 0.65, 10 bps, monthly) to within 0.02 pp / 0.01.
    G2  the full-sample window (L = whole sample) reproduces the record's published full-sample
        three-leg 4b verdict for this book (PASS).
    G3  window bookkeeping: window count is non-increasing in L, every window holds >= 0.95 * L *
        252 trading rows, and the first window's start equals the first post-warm-up date.

CAVEATS carried, not buried
    * SURVIVORSHIP.  research/universe.json is the CURRENT constituent list (idea 54), so every
      level here is optimistic and BOTH 4b level bars (DD cap, CAGR floor) are easier on this
      panel than on a point-in-time one.  A rolling-window pass rate measured on a survivorship-
      biased panel is an UPPER bound on the real one.
    * Rolling windows overlap heavily (a 10-year window at monthly starts shares 119/120 months
      with its neighbour), so the pass rate is NOT 93 independent trials and carries no p-value
      here.  It is a sensitivity reading, not a test.
    * 2020 and 2022 are the only real stress episodes in the panel; windows are not independent
      draws over regimes.
    * Rule 6: nothing here is a rules change; a rules change is a Sunday-review decision.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

SLUG = "2026-09-15_does-the-TOP20-4b-pass-hold-on-every-rolling-10-year-window_cloud"
pd.set_option("display.width", 220)

N_BOOK, MAX_VOL = 20, 0.60
LENGTHS = [5, 7, 10, 12]          # years  (10 = pre-registered headline)
STEPS = [1, 3]                    # months between window starts (1 = pre-registered)
GROSSES = [0.65, 0.75]
COSTS = [10, 25]
G_HEAD, C_HEAD, L_HEAD, S_HEAD = 0.65, 10, 10, 1
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---------------------------------------------------------------- the book
px = load_universe()
comp, above, vol20 = score(px, vol_scale=False)
elig = comp.where(above & (vol20 < MAX_VOL))
rank = elig.rank(axis=1, ascending=False)
_m = pd.Series(px.index.to_period("M"), index=px.index)
REBAL_DATES = px.index[(_m != _m.shift(-1)).values]


def book_weights(gross):
    W = ((rank <= N_BOOK).astype(float) * (gross / N_BOOK)).loc[REBAL_DATES]
    return W.reindex(px.index).ffill().fillna(0.0)


START = px.index[260]                                   # skip warm-up, as baseline.compare does
SPY = px["SPY"].pct_change().fillna(0.0).loc[START:]
BOOK = {(g, c): backtest(px, book_weights(g), cost_bps=c, freq="M")["returns"].loc[START:]
        for g in GROSSES for c in COSTS}
RV2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].loc[START:]
       for c in COSTS}


def legs(r, spy, base):
    """Three-leg in-window 4b against SPY, and 4a against the live book."""
    h = len(r) // 2
    a, s, b = metrics(r), metrics(spy), metrics(base)
    a1, a2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    s1, s2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    b1, b2 = metrics(base.iloc[:h])["Sharpe"], metrics(base.iloc[h:])["Sharpe"]
    L = dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=a1, H2=a2,
             spyCAGR=s["CAGR"], spySharpe=s["Sharpe"], spyMaxDD=s["MaxDD"],
             b_h1=a1 > s1, b_h2=a2 > s2,
             b_dd=a["MaxDD"] >= 0.60 * s["MaxDD"], b_cagr=a["CAGR"] >= 0.70 * s["CAGR"],
             a_h1=a1 > b1, a_h2=a2 > b2, a_dd=a["MaxDD"] >= b["MaxDD"],
             spy_cagr_neg=s["CAGR"] <= 0)
    L["4b"] = L["b_h1"] and L["b_h2"] and L["b_dd"] and L["b_cagr"]
    L["4a"] = L["a_h1"] and L["a_h2"] and L["a_dd"]
    return L


def windows(L_years, step_months):
    """Window starts every step_months from START; keep only windows fully inside the sample."""
    first = START.to_period("M").to_timestamp()
    last_start = px.index[-1] - pd.DateOffset(years=L_years)
    starts, t = [], first
    while t <= last_start:
        starts.append(t)
        t = t + pd.DateOffset(months=step_months)
    out = []
    for t0 in starts:
        t1 = t0 + pd.DateOffset(years=L_years)
        idx = SPY.loc[t0:t1].index
        if len(idx) >= int(0.95 * L_years * 252):
            out.append((max(t0, START), t1, idx))
    return out


def sweep(g, c, L_years, step):
    r, spy, base = BOOK[(g, c)], SPY, RV2[c]
    rows = []
    for t0, t1, idx in windows(L_years, step):
        d = legs(r.loc[idx], spy.loc[idx], base.loc[idx])
        d["start"] = t0.date(); d["end"] = idx[-1].date(); d["ndays"] = len(idx)
        rows.append(d)
    return pd.DataFrame(rows)


print("=" * 104)
print("GATES (printed before any hypothesis is read)")
print("=" * 104)
mh = metrics(BOOK[(G_HEAD, C_HEAD)])
g1 = (abs(mh["CAGR"] - 0.1269) <= 0.0002 and abs(mh["Sharpe"] - 1.201) <= 0.01
      and abs(mh["MaxDD"] + 0.1711) <= 0.0002)
print(f"G1 committed triple  got {mh['CAGR']:.2%} / {mh['Sharpe']:.3f} / {mh['MaxDD']:.2%}"
      f"   vs memo 12.69% / 1.201 / -17.11%   -> {'PASS' if g1 else 'FAIL'}")
full = legs(BOOK[(G_HEAD, C_HEAD)], SPY, RV2[C_HEAD])
print(f"G2 full-sample three-leg 4b  h1 {full['b_h1']} h2 {full['b_h2']} dd {full['b_dd']} "
      f"cagr {full['b_cagr']} -> 4b {full['4b']}   (4a {full['4a']})"
      f"   -> {'PASS' if full['4b'] else 'FAIL'}")
counts = [len(windows(L, 1)) for L in LENGTHS]
g3a = all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1))
w0 = windows(L_HEAD, 1)[0]
g3b = w0[0] == START.to_period("M").to_timestamp() or w0[0] == START
print(f"G3 window counts (step 1M) by L {dict(zip(LENGTHS, counts))}  non-increasing {g3a}; "
      f"first window starts {w0[0].date()} (sample starts {START.date()}) -> "
      f"{'PASS' if g3a and g3b else 'FAIL'}")

print()
print("=" * 104)
print("FULL GRID — three-leg in-window 4b and 4a pass rates over rolling windows")
print("(every (L, step, gross, cost) cell reported; nothing selected)")
print("=" * 104)
grid = []
cache = {}
for g in GROSSES:
    for c in COSTS:
        for L in LENGTHS:
            for s in STEPS:
                df = sweep(g, c, L, s)
                cache[(g, c, L, s)] = df
                n = len(df)
                grid.append(dict(gross=g, cost=c, L=L, step=s, n_win=n,
                                 pass4b=df["4b"].mean(), pass4a=df["4a"].mean(),
                                 fail_h1=(~df["b_h1"]).sum(), fail_h2=(~df["b_h2"]).sum(),
                                 fail_dd=(~df["b_dd"]).sum(), fail_cagr=(~df["b_cagr"]).sum(),
                                 degen=df["spy_cagr_neg"].sum(),
                                 pass4b_nd=df.loc[~df["spy_cagr_neg"], "4b"].mean()))
G = pd.DataFrame(grid)
print(G.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

print()
print("=" * 104)
print(f"HEADLINE CELL  L = {L_HEAD}y, step = {S_HEAD}M, gross = {G_HEAD}, cost = {C_HEAD} bps")
print("=" * 104)
H = cache[(G_HEAD, C_HEAD, L_HEAD, S_HEAD)]
print(f"windows {len(H)}   three-leg 4b pass {H['4b'].mean():.1%}   4a pass {H['4a'].mean():.1%}")
print("leg failure counts (of {n}):  H1 {h1}  H2 {h2}  DD {dd}  CAGR {cg}".format(
    n=len(H), h1=(~H["b_h1"]).sum(), h2=(~H["b_h2"]).sum(),
    dd=(~H["b_dd"]).sum(), cg=(~H["b_cagr"]).sum()))
only = {leg: int(((~H[f"b_{leg}"]) & H[[f"b_{o}" for o in ("h1", "h2", "dd", "cagr") if o != leg]].all(axis=1)).sum())
        for leg in ("h1", "h2", "dd", "cagr")}
print("windows failing EXACTLY one leg, by leg:", only)
show = H[["start", "end", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "spyCAGR", "spySharpe",
          "spyMaxDD", "b_h1", "b_h2", "b_dd", "b_cagr", "4b", "4a"]]
print(show.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# contiguity of the failing block (H_START)
fails = H.index[~H["4b"]].to_numpy()
blocks = 0
for i, k in enumerate(fails):
    if i == 0 or k != fails[i - 1] + 1:
        blocks += 1
print(f"\nH_START: {len(fails)} failing windows in {blocks} contiguous block(s) of start months"
      + (f"; first failing start {H.loc[fails[0], 'start']}, last {H.loc[fails[-1], 'start']}"
         if len(fails) else ""))

print()
print("=" * 104)
print("PROTOCOL rule 8 walk-forward (selector declared before the run, OOS read once)")
print("=" * 104)
is_rate = {}
for L in (5, 7):
    df = sweep(G_HEAD, C_HEAD, L, 1)
    inside = df[[pd.Timestamp(e) <= pd.Timestamp(IS_END) for e in df["end"]]]
    is_rate[L] = (inside["4b"].mean() if len(inside) else np.nan, len(inside))
    print(f"IS  L={L}y  windows ending <= {IS_END}: n={len(inside)}  4b pass "
          f"{is_rate[L][0]:.1%}" if len(inside) else f"IS L={L}y: no windows fit")
valid = {L: v for L, v in is_rate.items() if v[1] > 0}
L_PICK = max(valid, key=lambda L: (valid[L][0], L))
print(f"IS-PICK -> L = {L_PICK}y (highest IS 4b pass rate, ties to the larger L)")

oos_df = sweep(G_HEAD, C_HEAD, L_PICK, 1)
oos = oos_df[[pd.Timestamp(s) >= pd.Timestamp(OOS_START) for s in oos_df["start"]]]
print(f"OOS windows starting >= {OOS_START} at L={L_PICK}y: n={len(oos)}  "
      f"three-leg 4b pass {oos['4b'].mean():.1%}  4a pass {oos['4a'].mean():.1%}")
print("  leg failures: H1 {h1}  H2 {h2}  DD {dd}  CAGR {cg}".format(
    h1=(~oos["b_h1"]).sum(), h2=(~oos["b_h2"]).sum(),
    dd=(~oos["b_dd"]).sum(), cg=(~oos["b_cagr"]).sum()))

print(f"\nOOS window {OOS_START}..{px.index[-1].date()} — the book's own triple, read once:")
o = slice(pd.Timestamp(OOS_START), None)
ol = legs(BOOK[(G_HEAD, C_HEAD)].loc[o], SPY.loc[o], RV2[C_HEAD].loc[o])
mb, ms = metrics(RV2[C_HEAD].loc[o]), metrics(SPY.loc[o])
tbl = pd.DataFrame({
    "BOOK B* (top20, g=0.65, M)": [ol["CAGR"], ol["Sharpe"], ol["MaxDD"], ol["H1"], ol["H2"]],
    "RULES v2 (live, W)": [mb["CAGR"], mb["Sharpe"], mb["MaxDD"],
                           metrics(RV2[C_HEAD].loc[o].iloc[:len(RV2[C_HEAD].loc[o]) // 2])["Sharpe"],
                           metrics(RV2[C_HEAD].loc[o].iloc[len(RV2[C_HEAD].loc[o]) // 2:])["Sharpe"]],
    "SPY": [ms["CAGR"], ms["Sharpe"], ms["MaxDD"],
            metrics(SPY.loc[o].iloc[:len(SPY.loc[o]) // 2])["Sharpe"],
            metrics(SPY.loc[o].iloc[len(SPY.loc[o]) // 2:])["Sharpe"]]},
    index=["CAGR", "Sharpe", "MaxDD", "H1 Sharpe", "H2 Sharpe"])
print(tbl.to_string(float_format=lambda x: f"{x:.4f}"))
print(f"OOS three-leg 4b {ol['4b']}  (h1 {ol['b_h1']} h2 {ol['b_h2']} dd {ol['b_dd']} "
      f"cagr {ol['b_cagr']});  OOS 4a {ol['4a']}")

print()
print("=" * 104)
print("FULL SAMPLE — the one window every committed verdict on this book is read on")
print("=" * 104)
fs = pd.DataFrame({
    "BOOK B*": [full["CAGR"], full["Sharpe"], full["MaxDD"], full["H1"], full["H2"]],
    "RULES v2 (live)": [metrics(RV2[C_HEAD])["CAGR"], metrics(RV2[C_HEAD])["Sharpe"],
                        metrics(RV2[C_HEAD])["MaxDD"],
                        metrics(RV2[C_HEAD].iloc[:len(RV2[C_HEAD]) // 2])["Sharpe"],
                        metrics(RV2[C_HEAD].iloc[len(RV2[C_HEAD]) // 2:])["Sharpe"]],
    "SPY": [full["spyCAGR"], full["spySharpe"], full["spyMaxDD"],
            metrics(SPY.iloc[:len(SPY) // 2])["Sharpe"], metrics(SPY.iloc[len(SPY) // 2:])["Sharpe"]]},
    index=["CAGR", "Sharpe", "MaxDD", "H1 Sharpe", "H2 Sharpe"])
print(fs.to_string(float_format=lambda x: f"{x:.4f}"))

print()
print("=" * 104)
print("HYPOTHESES")
print("=" * 104)
hr = H["4b"].mean()
print(f"H_ROBUST (>= 80% of 10y windows clear three-leg 4b): {hr:.1%} -> "
      f"{'SUPPORTED' if hr >= 0.80 else 'FALSIFIED'}")
worst = max(only, key=lambda k: only[k]) if sum(only.values()) else None
print(f"H_LEG (one leg carries the failures): exactly-one-leg failures {only} -> "
      f"{'SUPPORTED, leg=' + worst if worst and only[worst] == sum(only.values()) and only[worst] > 0 else 'see counts'}")
print(f"H_START (failures form ONE contiguous block of starts): {blocks} block(s) -> "
      f"{'SUPPORTED' if blocks <= 1 else 'FALSIFIED'}")
print(f"\nturnover / yr at the headline cell: "
      f"{backtest(px, book_weights(G_HEAD), cost_bps=C_HEAD, freq='M')['turnover'].loc[START:].sum() / (len(SPY) / 252):.2f}x")
print("\nSURVIVORSHIP: universe.json is the current constituent list; every level above is "
      "optimistic and the rolling pass rate is an UPPER bound.")

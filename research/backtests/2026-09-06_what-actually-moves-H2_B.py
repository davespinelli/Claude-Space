#!/usr/bin/env python3
"""QUEUE idea 70 — what-actually-moves-H2 (lane B, 2026-09-06).

Question
--------
Idea 66 (`2026-09-04_gross-exposure-is-the-error_B.py`) left one number unexplained.
On universe_broad.json, the ranked book `top20-200d` at gross 0.75, weekly, 10 bps has a
SECOND-HALF Sharpe of **0.814 against SPY's 0.837** — the single bar that fails 4b.  Idea
66 showed gross moves it by 0.001 (it is a pure scale lever) and idea 63's 25% SPY core
moves it by +0.047 at t < 1.  So neither cash drag nor the passive sleeve explains it.

The queued question: **decompose broad H2 excess by sector and by top-10 mega-cap weight,
and test whether the shortfall is a handful of names or a regime.**

Why the framing has to change before any number is read
-------------------------------------------------------
The failing bar is a *Sharpe* bar, and Sharpe is scale-free, so a decomposition of raw
excess return cannot address it: in H2 the book runs 11.46%/14.67% vol against SPY's
15.05%/18.90%, and 26% of the book sits in cash.  Raw excess is dominated by that cash,
which idea 66 already proved is Sharpe-neutral.  This run therefore decomposes the
**vol-matched** active return

    a_t = k * r_book,t - r_spy,t ,      k = sigma_spy,H2 / sigma_book,H2   (a constant)

for which the identity  S_book - S_spy = 252 * mean(a) / sigma_spy  holds EXACTLY, so an
additive split of a_t is an additive split of the 0.023 Sharpe gap.  Per name,

    a_t = sum_i [ k * held_i,t * ret_i,t ] - k * cost_t - r_spy,t

which gives a per-name Sharpe contribution A_i with  sum_i A_i + COST + BENCH = dS exactly.
The identity is asserted to 1e-10 below rather than assumed.

Attribution ranks; it does not answer.  The answer needs counterfactual BOOKS, so every
name-level claim here is backed by a full re-run of the book with that name removed from
the eligible panel (rank recomputed, 135 names) — 136 real backtests, not a re-weighting.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe_broad.json via load_universe(broad=True), 136 names incl.
           SPY, sector/bond/commodity ETFs.  SURVIVORSHIP: current constituents only, so
           absolute CAGR/Sharpe are optimistic.  Every comparison here is between arms
           drawn from the SAME panel on the SAME days, which is far less exposed.
Book     : `top20-200d` at gross 0.75, core 0, weekly, 10 bps — imported verbatim from
           idea 66 (composite = mean pct-rank of 12-1/6m/3m with NO /sqrt(vol20); gate =
           vol20 < 0.60 AND price > 200d MA; equal weight g/20; cash if fewer than 20
           qualify).  NOTHING about the book is tuned here; it is the parent's arm.
Repro    : the run asserts idea 66's PUBLISHED broad numbers (13.1% / 0.958 / -20.1%,
           halves 1.125 / 0.814, SPY H2 0.837) BEFORE any new number is computed.  Prices
           are truncated at 2026-09-03, the parent's last eval day, so the halves split on
           the same date.
Sectors  : a FIXED 20-class taxonomy (11 GICS-ish equity sectors + 4 ETF classes), written
           once before any result was read, constant over the whole sample — no
           point-in-time GICS, so the 2023 reclassifications (V/MA to Financials, ADP to
           Industrials) are deliberately NOT applied.  Every ticker is asserted covered.
Mega-cap : MEGA10 is the 2026 top-10 US mega-caps present in the panel.  This is a
           HINDSIGHT list and is stated as such: it makes the concentration hypothesis
           EASIER to confirm, so a null result on it is the robust direction.
Params   : exactly 2 tuned — (1) exclusion size k in {0,1,2,3,5,10}, (2) exclusion
           granularity in {name, sector}.  All 12 grid points reported, in-sample and
           out-of-sample.  L in {21, 63, 126} is a diagnostic reporting axis (all values
           printed, nothing selected on it), not a tuned parameter.
Costs    : 10 bps (PROTOCOL rung), applied by the engine.
Baseline : 4a is judged against the LIVE book, which is RULES v2 as of the 2026-09-06
           Sunday review (200d +/-3% band, EW at 0.75/N, gated weight to cash, weekly).
           The RULES v1 verdict is carried alongside in brackets for continuity with the
           pre-v2 record.  NOTE: v2 is defined on universe.json (56 names); it is run here
           on the broad panel so that the comparand and the arms see the same days and the
           same instruments, which is the only way the halves line up.
Execution: weekly, weights decided at close t applied at t+1 (engine), long-only, no
           leverage.
Rule 8   : the exclusion set is fitted on 2009-2016 ONLY and 2017-2026 evaluated untouched.
           This is the load-bearing test: H2 (from 2017-11-03) is almost exactly the OOS
           window, so any exclusion fitted ON H2 is hindsight by construction.  If the
           shortfall is "a handful of names", the names that hurt in-sample must keep
           hurting out-of-sample; if it is a regime, they will not.

The null this run has to defeat: for a 20-of-136 ranked book, the worst few names in any
window are a selection artefact of that window.  A drop-k rule fitted in-sample that does
nothing out-of-sample is the null, and it is tested directly, not assumed.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

SCRIPT = "research/backtests/2026-09-06_what-actually-moves-H2_B.py"
STEM = ROOT / "research" / "backtests" / "2026-09-06_what-actually-moves-H2_B"

FREQ = "W"
COST = 10
MAX_VOL = 0.60
NPOS = 20
GROSS = 0.75
END = "2026-09-03"            # idea 66's last eval day, so the halves split identically
IS_END, OOS_START = "2016-12-31", "2017-01-01"
KGRID = [0, 1, 2, 3, 5, 10]   # tuned param 1
GRANS = ["name", "sector"]    # tuned param 2
LGRID = [21, 63, 126]         # diagnostic axis, nothing selected on it
NDRAW = 2000
SEED = 70

# ------------------------------------------------------------------ taxonomy
SECTOR = {}
for t in "AAPL ACN ADBE ADI ADP AMAT AMD ANET AVGO CRM CSCO IBM INTU KLAC LRCX MA MSFT MU NOW NVDA ORCL PANW PLTR QCOM TXN V".split(): SECTOR[t] = "InfoTech"
for t in "GOOGL META NFLX T".split(): SECTOR[t] = "CommSvcs"
for t in "AMZN BKNG CMG HD LOW MCD SBUX TJX TSLA UBER".split(): SECTOR[t] = "ConsDisc"
for t in "COST KO MDLZ MO PEP PG PM WMT".split(): SECTOR[t] = "ConsStap"
for t in "ABBV ABT AMGN BSX CI DHR GILD ISRG JNJ LLY MDT MRK PFE REGN SYK TMO UNH VRTX ZTS".split(): SECTOR[t] = "HealthCare"
for t in "AXP BAC BLK BRK-B C CB GS ICE JPM MMC MS PGR SCHW SPGI WFC".split(): SECTOR[t] = "Financials"
for t in "BA CAT DE ETN GE HON LMT RTX UNP".split(): SECTOR[t] = "Industrials"
for t in "COP CVX XOM".split(): SECTOR[t] = "Energy"
for t in "LIN SHW".split(): SECTOR[t] = "Materials"
for t in "DUK NEE SO".split(): SECTOR[t] = "Utilities"
for t in "PLD".split(): SECTOR[t] = "RealEstate"
for t in "DIA EEM EFA IWM QQQ RSP SPY VTI".split(): SECTOR[t] = "ETF-Index"
for t in "GDX ITB KRE SMH XBI XLB XLC XLE XLF XLI XLK XLP XLRE XLU XLV XLY".split(): SECTOR[t] = "ETF-Sector"
for t in "HYG IEF LQD SHY TIP TLT".split(): SECTOR[t] = "ETF-Bond"
for t in "DBC GLD SLV UNG USO UUP".split(): SECTOR[t] = "ETF-Cmdty"

MEGA10 = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "BRK-B", "LLY"]

# --------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def top20_weights(px, drop=()):
    """Idea 66's `top20-200d` at gross 0.75, with `drop` removed from the eligible panel.

    Dropping is done at the ELIGIBILITY stage, so the rank is recomputed over the
    surviving names and the book still holds 20 of them — a real alternative book, not a
    re-weighting of the parent's holdings.
    """
    elig = (vol20(px) < MAX_VOL) & (px > px.rolling(200).mean())
    if drop:
        keep = [c for c in px.columns if c not in set(drop)]
        elig = elig & pd.Series(px.columns.isin(keep), index=px.columns)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def run(px, drop=()):
    return backtest(px, top20_weights(px, drop), cost_bps=COST, freq=FREQ)


def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def fmt3(r):
    c, s, dd = m3(r)
    return f"{c:6.2%} {s:6.3f} {dd:7.2%}"


# ------------------------------------------------------------------ KEEP paths
def path4a(r, base):
    """Sharpe > live rules in BOTH halves AND MaxDD no worse than the live rules."""
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(base.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(base.iloc[h:])["Sharpe"]: bad.append("H2")
    if metrics(r)["MaxDD"] < metrics(base)["MaxDD"]: bad.append("DD")
    return bad


def path4b(r, spy, oos_s, spy_oos_s):
    """Sharpe > SPY in BOTH halves AND OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's."""
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(spy.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(spy.iloc[h:])["Sharpe"]: bad.append("H2")
    if oos_s <= spy_oos_s: bad.append("OOS")
    if abs(metrics(r)["MaxDD"]) > 0.60 * abs(metrics(spy)["MaxDD"]): bad.append("DD")
    if metrics(r)["CAGR"] < 0.70 * metrics(spy)["CAGR"]: bad.append("CAGR")
    return bad


def verdict(r, base, spy, oos_s, spy_oos_s, base_old=None):
    """4a is judged against the LIVE book (RULES v2 since the 2026-09-06 Sunday review);
    the v1 verdict is carried alongside for continuity with the pre-v2 record."""
    a, b = path4a(r, base), path4b(r, spy, oos_s, spy_oos_s)
    out = ("KEEP 4a" if not a else "KILL 4a(" + ",".join(a) + ")") + " / " + \
          ("KEEP 4b" if not b else "KILL 4b(" + ",".join(b) + ")")
    if base_old is not None:
        ao = path4a(r, base_old)
        out += "  [v1: " + ("KEEP 4a" if not ao else "KILL 4a(" + ",".join(ao) + ")") + "]"
    return out


# ==================================================================== main
def main():
    px = load_universe(broad=True).loc[:END]
    missing = [c for c in px.columns if c not in SECTOR]
    assert not missing, f"unclassified tickers: {missing}"
    print(f"universe_broad.json: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"sector taxonomy: {len(set(SECTOR[c] for c in px.columns))} classes, all {px.shape[1]} tickers covered")

    parent = run(px)
    start = px.index[260]
    r = parent["returns"].loc[start:]
    held = parent["weights"].loc[start:]
    turn = parent["turnover"].loc[start:]
    rets = px.pct_change().fillna(0.0).loc[start:]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    base_v2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    h = len(r) // 2
    H2 = slice(h, None)

    # ------------------------------------------------------ reproduction gate
    print("\n" + "=" * 92)
    print("REPRODUCTION GATE — idea 66's published broad `top20-200d` g=0.75 core=0 @10bps")
    print("=" * 92)
    got = dict(CAGR=metrics(r)["CAGR"], Sharpe=metrics(r)["Sharpe"], MaxDD=metrics(r)["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
               SPY_H2=metrics(spy.iloc[h:])["Sharpe"])
    want = dict(CAGR=0.131, Sharpe=0.958, MaxDD=-0.201, H1=1.125, H2=0.814, SPY_H2=0.837)
    ok = True
    for kk in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "SPY_H2"):
        tol = 5e-4 if kk in ("CAGR", "MaxDD") else 5e-4
        hit = abs(got[kk] - want[kk]) <= tol
        ok &= hit
        print(f"  {kk:8s} published {want[kk]:8.3f}   reproduced {got[kk]:8.4f}   {'EXACT' if hit else 'MISMATCH'}")
    print(f"  eval window {r.index[0].date()} -> {r.index[-1].date()}   H2 window {r.index[h].date()} -> {r.index[-1].date()} ({len(r)-h} days)")
    print(f"  REPRODUCTION: {'6/6 EXACT' if ok else 'FAILED'}")
    assert ok, "reproduction gate failed — refusing to read new numbers"

    print(f"\n  H2 book  {fmt3(r.iloc[H2])}  vol {metrics(r.iloc[H2])['Vol']:.2%}   mean gross {held.iloc[H2].sum(axis=1).mean():.4f}")
    print(f"  H2 SPY   {fmt3(spy.iloc[H2])}  vol {metrics(spy.iloc[H2])['Vol']:.2%}")
    print(f"  NOTE: H2 starts {r.index[h].date()}; the rule-8 OOS window starts {OOS_START}. "
          f"H2 IS the OOS window (overlap {((r.index[h:] >= OOS_START).mean()):.1%}), so anything fitted on H2 is hindsight.")

    # ================================================== RESULT 1 — exact split
    print("\n" + "=" * 92)
    print("RESULT 1 — the 0.023 H2 Sharpe gap, split EXACTLY by name and by sector")
    print("=" * 92)
    rb, rs = r.iloc[H2], spy.iloc[H2]
    sig_b, sig_s = rb.std() * np.sqrt(252), rs.std() * np.sqrt(252)
    k = sig_s / sig_b
    S_b, S_s = metrics(rb)["Sharpe"], metrics(rs)["Sharpe"]
    dS = S_b - S_s
    scale = 252.0 / sig_s
    contrib = (held.iloc[H2] * rets.iloc[H2])                 # per-name daily contribution
    A = contrib.mean() * k * scale                            # per-name Sharpe contribution
    COSTT = -turn.iloc[H2].mean() * COST / 1e4 * k * scale
    BENCH = -rs.mean() * scale
    ident = A.sum() + COSTT + BENCH
    print(f"  vol ratio k = sigma_SPY/sigma_book = {sig_s:.4%}/{sig_b:.4%} = {k:.4f}")
    print(f"  identity check: sum_i A_i {A.sum():+.6f}  + COST {COSTT:+.6f}  + BENCH {BENCH:+.6f}  = {ident:+.6f}   vs dS = {dS:+.6f}   |err| {abs(ident-dS):.2e}")
    assert abs(ident - dS) < 1e-10, "Sharpe decomposition identity broken"
    print(f"  So the whole question is a {dS:+.3f} Sharpe gap. Cost alone is {COSTT:+.3f} of it.")

    sec = pd.Series({c: SECTOR[c] for c in px.columns})
    secA = A.groupby(sec).sum().sort_values()
    secW = held.iloc[H2].T.groupby(sec).sum().T.mean()
    print("\n  H2 Sharpe contribution by SECTOR (sums to sum_i A_i; 'active' = A_s - k*wbar_s*S_SPY):")
    print(f"  {'sector':<12} {'meanwt':>8} {'A_s':>9} {'active':>9}")
    rows = []
    for s_ in secA.index:
        act = secA[s_] - k * secW.get(s_, 0.0) * S_s
        rows.append((s_, secW.get(s_, 0.0), secA[s_], act))
        print(f"  {s_:<12} {secW.get(s_,0.0):8.4f} {secA[s_]:+9.4f} {act:+9.4f}")
    pd.DataFrame(rows, columns=["sector", "mean_weight", "A_sector", "active"]).to_csv(f"{STEM}.sectors.csv", index=False)
    resid = k * secW.sum() - 1.0
    print(f"  vol-matched investment residual: k*gross - 1 = {resid:+.4f}  ->  {resid*S_s:+.4f} Sharpe (this is ALL the cash drag is worth here)")

    print("\n  10 most negative and 10 most positive NAME contributions A_i:")
    Asort = A.sort_values()
    for lbl, part in (("worst", Asort.head(10)), ("best", Asort.tail(10)[::-1])):
        print(f"    {lbl:5s}: " + ", ".join(f"{t}({SECTOR[t][:4]}) {v:+.4f}" for t, v in part.items()))
    A.rename("A_i").to_frame().assign(sector=[SECTOR[t] for t in A.index],
                                      mean_weight=held.iloc[H2].mean()).to_csv(f"{STEM}.names.csv")

    # ============================== RESULT 2 — leave-one-out, 136 real re-runs
    print("\n" + "=" * 92)
    print("RESULT 2 — leave-one-out: 136 real books, each with one name removed from the panel")
    print("=" * 92)
    loo = {}
    for i, t in enumerate(px.columns):
        if t == "SPY":                       # SPY is the benchmark column; drop it anyway for symmetry
            pass
        rr = run(px, drop=(t,))["returns"].loc[start:]
        loo[t] = metrics(rr.iloc[H2])["Sharpe"]
    loo = pd.Series(loo).sort_values(ascending=False)
    n_flip = int((loo > S_s).sum())
    print(f"  parent H2 Sharpe {S_b:.4f}; SPY {S_s:.4f}; gap {dS:+.4f}")
    print(f"  names whose REMOVAL alone lifts H2 Sharpe above SPY: {n_flip} of {len(loo)}")
    print(f"  best 8 removals : " + ", ".join(f"{t} {v:.4f}" for t, v in loo.head(8).items()))
    print(f"  worst 8 removals: " + ", ".join(f"{t} {v:.4f}" for t, v in loo.tail(8).items()))
    print(f"  spread of LOO H2 Sharpe: {loo.min():.4f} .. {loo.max():.4f} (sd {loo.std():.4f})")
    print(f"  rank correlation LOO-gain vs attribution -A_i: Spearman "
          f"{pd.Series(loo).rank().corr(( -A).rank()):+.3f}")
    loo.rename("H2_Sharpe_without").to_frame().to_csv(f"{STEM}.loo.csv")

    # drop-k ladder using the HINDSIGHT (H2-fitted) ranking — the ceiling, not a rule
    print("\n  drop-k ladder, exclusion chosen ON H2 (pure hindsight — this is the CEILING, not a rule):")
    print(f"  {'k':>3} {'names':<34} {'H2 Sharpe':>10} {'vs SPY':>8}")
    hind_order = A.sort_values().index.tolist()
    for kk in KGRID:
        drop = tuple(hind_order[:kk])
        rr = run(px, drop=drop)["returns"].loc[start:]
        s2 = metrics(rr.iloc[H2])["Sharpe"]
        print(f"  {kk:3d} {','.join(drop)[:34]:<34} {s2:10.4f} {s2-S_s:+8.4f}")

    # concentration of the shortfall across names, vs a random-k null
    rng = np.random.default_rng(SEED)
    print("\n  is the gap 'a handful of names'? share of |dS| recovered by dropping k names,")
    print("  hindsight-best k vs the mean of 2000 random k-subsets (attribution-based, exact):")
    print(f"  {'k':>3} {'best-k':>9} {'random-k':>9} {'pctile':>7}")
    negA = A.sort_values()
    for kk in [x for x in KGRID if x > 0]:
        best = -negA.head(kk).sum()
        draws = np.array([-A.sample(kk, random_state=int(rng.integers(1e9))).sum() for _ in range(NDRAW)])
        print(f"  {kk:3d} {best:+9.4f} {draws.mean():+9.4f} {(draws < best).mean()*100:6.1f}%")

    # ==================================== RESULT 3 — time concentration (regime)
    print("\n" + "=" * 92)
    print("RESULT 3 — or is it a regime? time-concentration of the vol-matched active return")
    print("=" * 92)
    a_t = k * rb - rs
    print(f"  mean(a_t)*252/sigma_SPY = {a_t.mean()*scale:+.4f} = dS (check {abs(a_t.mean()*scale - dS):.2e})")
    print(f"  {'L':>4} {'worst L-day sum':>16} {'share of |dS|':>14} {'dS ex-window':>13} {'perm pctile':>12}")
    for L in LGRID:
        roll = a_t.rolling(L).sum()
        j = int(np.nanargmin(roll.values))
        lo = max(0, j - L + 1)
        worst = roll.iloc[j]
        mask = np.ones(len(a_t), bool); mask[lo:j + 1] = False
        ex = a_t[mask].mean() * scale
        perm = np.array([pd.Series(rng.permutation(a_t.values)).rolling(L).sum().min() for _ in range(200)])
        print(f"  {L:4d} {worst:16.4f} {worst/abs(a_t.sum()):13.1%} {ex:+13.4f} {(perm < worst).mean()*100:11.1f}%"
              f"   [{a_t.index[lo].date()} -> {a_t.index[j].date()}]")
    print("  ('dS ex-window' = the Sharpe gap with the single worst L-day window deleted;")
    print("   'perm pctile' = where that window sits in 200 permutations of the same daily returns.)")

    yr = pd.DataFrame({"book": rb, "spy": rs}).groupby(rb.index.year).apply(lambda x: (1 + x).prod() - 1)
    yr["excess"] = yr["book"] - yr["spy"]
    print("\n  H2 by calendar year (2017 is a partial year, from 2017-11-03):")
    print("  " + "  ".join(f"{int(y)}" for y in yr.index))
    print("  " + "  ".join(f"{v:+5.1%}" for v in yr["excess"]))
    print(f"  years the book beat SPY: {(yr['excess'] > 0).sum()} of {len(yr)}")
    yr.to_csv(f"{STEM}.years.csv")

    # ==================================== RESULT 4 — mega-cap weight regression
    print("\n" + "=" * 92)
    print("RESULT 4 — does the book's MEGA10 weight explain the H2 gap?  (MEGA10 is a HINDSIGHT list)")
    print("=" * 92)
    mega = [t for t in MEGA10 if t in px.columns]
    wm = held.iloc[H2][mega].sum(axis=1)
    print(f"  MEGA10 = {','.join(mega)}")
    print(f"  book mean MEGA10 weight in H2: {wm.mean():.4f} of {held.iloc[H2].sum(axis=1).mean():.4f} gross "
          f"({wm.mean()/held.iloc[H2].sum(axis=1).mean():.1%} of the book); range {wm.min():.3f}..{wm.max():.3f}")
    for lag, xs in (("same-day", wm), ("lag-1", wm.shift(1).fillna(wm.mean()))):
        x = (xs - xs.mean()).values; y = a_t.values
        beta = float(np.dot(x, y) / np.dot(x, x))
        resid_ = y - beta * x
        se = float(np.sqrt((resid_ ** 2).sum() / (len(y) - 2) / np.dot(x, x)))
        r2 = 1 - resid_.var() / y.var()
        print(f"  a_t on MEGA10 weight ({lag:8s}): beta {beta:+.4f}  t {beta/se:+.2f}  R2 {r2:.4f}")
    mega_share = A[mega].sum()
    print(f"  MEGA10's share of the book's H2 Sharpe: {mega_share:+.4f} of {A.sum():+.4f} "
          f"({mega_share/A.sum():.1%}) — the mega-caps are the book's biggest POSITIVE, not its hole"
          if mega_share > 0 else f"  MEGA10 A-sum {mega_share:+.4f}")
    rr = run(px, drop=tuple(mega))["returns"].loc[start:]
    print(f"  counterfactual: the same book with all 10 mega-caps banned -> H2 {fmt3(rr.iloc[H2])} "
          f"(Sharpe {metrics(rr.iloc[H2])['Sharpe']:+.4f} vs parent {S_b:.4f})")

    # =============================== RESULT 5 — rule 8: the honest, tradable test
    print("\n" + "=" * 92)
    print("RULE 8 — exclusion fitted on 2009-2016 ONLY, 2017-2026 evaluated untouched")
    print("=" * 92)
    is_r = r.loc[:IS_END]
    is_contrib = (held.loc[:IS_END] * rets.loc[:IS_END])
    A_is = is_contrib.mean()                     # in-sample per-name contribution (IS only)
    A_is_sec = A_is.groupby(sec).sum()
    oos_slice = slice(OOS_START, None)
    spy_oos = spy.loc[oos_slice]
    v1_oos = base_v1.loc[oos_slice]
    par_oos = r.loc[oos_slice]
    spy_oos_s = metrics(spy_oos)["Sharpe"]
    print(f"  IS  {is_r.index[0].date()} -> {is_r.index[-1].date()}   OOS {par_oos.index[0].date()} -> {par_oos.index[-1].date()}")
    print(f"  IS-worst names  : {', '.join(A_is.sort_values().head(10).index)}")
    print(f"  IS-worst sectors: {', '.join(A_is_sec.sort_values().head(3).index)}")
    print()
    print(f"  {'gran':<7} {'k':>3} {'excluded':<30} | {'OOS CAGR':>9} {'OOS Sh':>7} {'OOS DD':>8} | {'full CAGR':>9} {'Sh':>6} {'DD':>7} {'H1/H2':>13} | verdict")
    grid = []
    for gran in GRANS:
        order = (A_is.sort_values().index.tolist() if gran == "name"
                 else A_is_sec.sort_values().index.tolist())
        for kk in KGRID:
            if gran == "name":
                drop = tuple(order[:kk])
                label = ",".join(drop) if drop else "(none)"
            else:
                secs = order[:kk]
                drop = tuple(t for t in px.columns if SECTOR[t] in secs and t != "SPY")
                label = ",".join(secs) if secs else "(none)"
            rr = run(px, drop=drop)["returns"].loc[start:]
            ro = rr.loc[oos_slice]
            oc, os_, od = m3(ro)
            fc, fs, fd = m3(rr)
            hh = len(rr) // 2
            h1, h2 = metrics(rr.iloc[:hh])["Sharpe"], metrics(rr.iloc[hh:])["Sharpe"]
            vd = verdict(rr, base_v2, spy, os_, spy_oos_s, base_old=base_v1)
            grid.append(dict(gran=gran, k=kk, excluded=label, oos_cagr=oc, oos_sharpe=os_, oos_dd=od,
                             cagr=fc, sharpe=fs, maxdd=fd, h1=h1, h2=h2, verdict=vd))
            print(f"  {gran:<7} {kk:3d} {label[:30]:<30} | {oc:9.2%} {os_:7.3f} {od:8.2%} | "
                  f"{fc:9.2%} {fs:6.3f} {fd:7.2%} {h1:6.3f}/{h2:6.3f} | {vd}")
    pd.DataFrame(grid).to_csv(f"{STEM}.grid.csv", index=False)

    print()
    for nm, s_ in (("RULES v2 (live book)", base_v2), ("RULES v1 (previous)", base_v1), ("SPY", spy)):
        so = s_.loc[oos_slice]
        hh = len(s_) // 2
        print(f"  {nm:<20} OOS {fmt3(so)} | full {fmt3(s_)} "
              f"H1 {metrics(s_.iloc[:hh])['Sharpe']:.3f} / H2 {metrics(s_.iloc[hh:])['Sharpe']:.3f}")

    g = pd.DataFrame(grid)
    n4a = int(g["verdict"].str.startswith("KEEP 4a").sum())          # vs the LIVE book (v2)
    n4a_v1 = int(g["verdict"].str.contains(r"\[v1: KEEP 4a\]", regex=True).sum())
    n4b = int(g["verdict"].str.contains("KEEP 4b").sum())
    best = g.loc[g["oos_sharpe"].idxmax()]
    print(f"\n  grid points: {len(g)};  4a passes {n4a} vs the LIVE book RULES v2 ({n4a_v1} against the retired v1);  4b passes {n4b}")
    print(f"  best OOS Sharpe on the grid: {best['gran']} k={best['k']} -> {best['oos_sharpe']:.3f} "
          f"vs parent k=0 {g[(g.k==0)&(g.gran=='name')]['oos_sharpe'].iloc[0]:.3f}, SPY {spy_oos_s:.3f}")
    print(f"  IS-fitted drop-k OOS Sharpe spread over k: name "
          f"{g[g.gran=='name']['oos_sharpe'].min():.3f}..{g[g.gran=='name']['oos_sharpe'].max():.3f}, sector "
          f"{g[g.gran=='sector']['oos_sharpe'].min():.3f}..{g[g.gran=='sector']['oos_sharpe'].max():.3f}")

    # does the IS ranking predict the OOS ranking of names at all?
    A_oos = (held.loc[oos_slice] * rets.loc[oos_slice]).mean()
    common = A_is.index.intersection(A_oos.index)
    sp = A_is[common].rank().corr(A_oos[common].rank())
    print(f"  PERSISTENCE: Spearman(IS per-name contribution, OOS per-name contribution) = {sp:+.3f} over {len(common)} names")
    print(f"  overlap of IS-worst-10 and OOS-worst-10: "
          f"{len(set(A_is.sort_values().head(10).index) & set(A_oos.sort_values().head(10).index))} of 10")
    print(f"  overlap of IS-worst-3 sectors and OOS-worst-3 sectors: "
          f"{len(set(A_is_sec.sort_values().head(3).index) & set((held.loc[oos_slice]*rets.loc[oos_slice]).mean().groupby(sec).sum().sort_values().head(3).index))} of 3")

    print("\n" + "=" * 92)
    print(f"artifacts: {Path(STEM).name}.{{sectors,names,loo,years,grid}}.csv")
    print("=" * 92)


if __name__ == "__main__":
    main()

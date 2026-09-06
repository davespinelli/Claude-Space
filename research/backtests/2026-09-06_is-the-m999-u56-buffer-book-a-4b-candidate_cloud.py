#!/usr/bin/env python3
"""QUEUE idea 280 — is-the-m=999-u56-buffer-book-a-4b-candidate-in-its-own-right (cloud, 2026-09-06).

Question
--------
Idea 273's TRANSFER arm (`2026-09-06_turnover-budget-the-broad-ranked-book_B.py`) reports, on
u56, a `top20-200d` book with the rank buffer wide open (m=999: a holding is sold only when it
leaves the 200d/vol gate) at **11.90% / 1.142 / -12.79%, 3.49x/yr, OOS 1.210 vs SPY 0.884** —
which clears 4b.  But every one of the 45 u56 cells clears 4b, the UN-budgeted parent included,
and Spearman(IS, OOS) there is +0.010.  The queue asks: price that arm against the live RULES v2
(1.2056 / -12.05%) and against the record's standing u56 candidate (idea 2's `top20`, 12.660% /
1.0921 / -18.308%) **on matched realised gross and matched turnover**, and decide whether it is a
book or a re-labelling of `top20-200d`.

Note the standing u56 candidate and idea 273's parent are the SAME series (12.66% / 1.092 /
-18.31%); gate 1 asserts that before anything else is read.  So the comparison has exactly three
comparands: the parent, the live book, and SPY.

Instrument (imported verbatim in construction from idea 273; re-implemented here so the script
stands alone, and asserted equal to the published numbers at both ends of the m dial)
------------------------------------------------------------------------------------------
`band_weights(px, m, j)`: entry bar rank <= NPOS(=20); a still-eligible holding is sold only once
its composite rank passes NPOS + m, at most j rank-driven replacements per rebalance; gate exits
(below 200d MA, or vol20 >= 0.60) are forced and never capped.  Weight GROSS/NPOS per name, rest
cash.  Two tuned parameters, m and j, and nothing else: cost rung is reported at both values and
never selected on, and the cadence used in TEST B is chosen by TURNOVER DISTANCE to the buffer,
not by any performance number (pre-registered below).

The three tests, pre-registered before any new number was read
--------------------------------------------------------------
TEST A — MATCHED REALISED GROSS.  The buffer does not hold the parent's book size: when the
eligible top-20 shrinks, retained names ranked past 20 are not dropped, so held count (and gross)
can exceed the parent's.  4b's CAGR floor and drawdown cap are SCALE bars, so any gross gap is a
free pass.  Every arm is therefore re-run scaled by a constant c = gross_parent / gross_arm and
4b is re-read at matched exposure.  Idea 274's finding (Sharpe flat in gross) predicts Sharpe
survives and the SCALE bars are the ones that move; that prediction is checked, not assumed.

TEST B — MATCHED TURNOVER.  If a slower CADENCE on the plain parent buys the same turnover cut,
the buffer is a re-labelling.  The parent is run at D/W/M/Q and at k-week schedules k in
{2,3,4,6,8}; the arm whose realised turnover is CLOSEST to the buffer's is the comparand.  The
choice rule is |turnover - turnover_buffer| and is fixed here, in the source, before any Sharpe
on that ladder is printed.

TEST C — IS IT A DIFFERENT BOOK AT ALL.  Mean Jaccard overlap of the held sets on rebalance
dates, correlation of daily returns, and the share of rebalance dates on which the two books hold
an identical set, buffer vs parent and buffer vs the turnover-matched cadence arm.

Rule 8 (required): (m, j) chosen on 2009-2016 by IS Sharpe alone, evaluated untouched on
2017-2026 against parent / RULES v2 / SPY.  Pre-registered caveat repeated from idea 111: on this
sample 2017-2026 is very nearly H2, so the rule-8 OOS bar and 4b's H2 bar overlap and the OOS
number is weaker evidence than it looks.

SURVIVORSHIP: u56 = research/universe.json, current constituents, so absolute CAGR/Sharpe are
optimistic for every arm.  All comparisons here are between arms on the same panel and same days.

Outputs: `.console.txt` (this log), `.grid.csv` (all 45 cells x 2 rungs, literal and gross-matched),
`.cadence.csv` (TEST B ladder), `.walkforward.csv` (rule 8).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask                    # noqa: E402

NPOS, GROSS, MAX_VOL, FREQ = 20, 0.75, 0.60, "W"
END = "2026-09-03"                 # idea 273's last eval day, so the halves split identically
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MGRID = [0, 2, 5, 10, 15, 20, 30, 50, 999]     # tuned param 1: no-trade band width
JGRID = [1, 2, 3, 5, 999]                      # tuned param 2: replacements per rebalance
RUNGS = [10, 25]                               # reporting axis, not tuned
KWEEKS = [2, 3, 4, 6, 8]                       # TEST B cadence ladder (matched, not tuned)
OUT = Path(__file__).with_suffix("")

_LINES = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


# --------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def eligible(px):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (vol20 < MAX_VOL) & (px > px.rolling(200).mean())


def parent_weights(px):
    """Idea 2 / idea 66's stateless `top20-200d` at gross 0.75."""
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def kweek_mask(idx, k):
    """True on the last trading day of every k-th ISO week present in the index."""
    w = rebalance_mask(idx, "W").values
    out = np.zeros(len(idx), dtype=bool)
    c = 0
    for i in range(len(idx)):
        if w[i]:
            c += 1
            if c % k == 0:
                out[i] = True
    return pd.Series(out, index=idx)


def band_weights(px, m, j, mask=None):
    """Idea 273's rank no-trade band, verbatim (see gate 2).  `mask` overrides the schedule."""
    comp = composite(px)
    elig = eligible(px)
    rank_all = comp.where(elig).rank(axis=1, ascending=False)
    if mask is None:
        mask = rebalance_mask(px.index, FREQ)
    dates = px.index[mask.values]
    cols = list(px.columns)
    pos = {c: i for i, c in enumerate(cols)}
    W = np.zeros((len(px.index), len(cols)))
    rk = rank_all.values
    didx = {d: i for i, d in enumerate(px.index)}
    held = []
    row = np.zeros(len(cols))
    prev_i = 0
    for d in dates:
        i = didx[d]
        W[prev_i:i] = row
        r = rk[i]
        held = [t for t in held if not np.isnan(r[pos[t]])]              # forced gate exits
        breach = sorted([t for t in held if r[pos[t]] > NPOS + m], key=lambda t: -r[pos[t]])
        for t in breach[:j]:
            held.remove(t)
        npos_t = int(np.nansum(r <= NPOS))                               # the parent's own set size
        need = npos_t - len(held)
        if need > 0:
            hs = set(held)
            cand = [(r[pos[c]], c) for c in cols
                    if c not in hs and not np.isnan(r[pos[c]]) and r[pos[c]] <= NPOS]
            cand.sort()
            held += [c for _, c in cand[:need]]
        row = np.zeros(len(cols))
        for t in held:
            row[pos[t]] = GROSS / NPOS
        W[i] = row
        prev_i = i + 1
    W[prev_i:] = row
    return pd.DataFrame(W, index=px.index, columns=px.columns)


# ------------------------------------------------------------------ KEEP paths
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def path4a(r, base):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(base.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(base.iloc[h:])["Sharpe"]: bad.append("H2")
    if metrics(r)["MaxDD"] < metrics(base)["MaxDD"]: bad.append("DD")
    return bad


def path4b(r, spy, oos_s, spy_oos_s):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(spy.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(spy.iloc[h:])["Sharpe"]: bad.append("H2")
    if oos_s <= spy_oos_s: bad.append("OOS")
    if abs(metrics(r)["MaxDD"]) > 0.60 * abs(metrics(spy)["MaxDD"]): bad.append("DD")
    if metrics(r)["CAGR"] < 0.70 * metrics(spy)["CAGR"]: bad.append("CAGR")
    return bad


def vstr(bad, tag):
    return f"KEEP {tag}" if not bad else f"KILL {tag}(" + ",".join(bad) + ")"


def run(px, w, bps, freq=FREQ):
    return backtest(px, w, cost_bps=bps, freq=freq)


def backtest_mask(prices, weights, cost_bps, mask):
    """engine.backtest with an arbitrary boolean rebalance mask instead of freq in {D,W,M,Q}.

    Line-for-line the engine's loop (weights decided at t applied at t+1, drift between
    rebalances, cost_bps per unit turnover); gate 4 asserts it is bit-identical to
    engine.backtest on the weekly schedule, so the k-week rungs of TEST B are priced under the
    same execution model as everything else in the record.
    """
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    msk = mask.shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns))
    turnover = pd.Series(0.0, index=prices.index)
    for i, d in enumerate(prices.index):
        if msk.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            turnover.iloc[i] = np.abs(new - cur).sum()
            cur = new
        held.iloc[i] = cur
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "equity": (1 + port).cumprod(), "weights": held, "turnover": turnover}


# ==================================================================== main
def main():
    pd.set_option("display.width", 220)
    px = load_universe().loc[:END]
    P(f"u56 (research/universe.json): {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    start = px.index[260]
    spy_full = px["SPY"].pct_change().fillna(0.0)
    spy = spy_full.loc[start:]
    n = len(spy); h = n // 2; yrs = n / 252.0
    oos = spy.loc[OOS_START:].index
    spy_oos_s = metrics(spy.loc[oos])["Sharpe"]

    def stats(res, bps):
        r = res["returns"].loc[start:]
        c, s, dd = m3(r)
        oc, os_, odd = m3(r.loc[oos])
        return dict(CAGR=c, Sharpe=s, MaxDD=dd,
                    H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                    IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                    OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                    turn=res["turnover"].loc[start:].sum() / yrs,
                    gross=res["weights"].loc[start:].sum(axis=1).mean(), bps=bps, r=r)

    # ------------------------------------------------------ reproduction gates
    pw = parent_weights(px)
    par = {b: stats(run(px, pw, b), b) for b in RUNGS}
    buf = {b: stats(run(px, band_weights(px, 999, 999), b), b) for b in RUNGS}

    P("\n" + "=" * 108)
    P("REPRODUCTION GATE 1 — idea 2's standing u56 KEEP == idea 273's u56 parent (m=0, j=inf) @10bps")
    P("=" * 108)
    want1 = dict(CAGR=0.1267, Sharpe=1.093, MaxDD=-0.1831)     # idea 273's u56 parent, END=2026-09-03
    ok1 = True
    for k, v in want1.items():
        hit = abs(par[10][k] - v) <= 5e-4
        ok1 &= hit
        P(f"  {k:8s} idea 273 {v:9.4f}   reproduced {par[10][k]:9.4f}   {'EXACT' if hit else 'MISMATCH'}")
    older = dict(CAGR=0.12660, Sharpe=1.0921, MaxDD=-0.18308)  # idea 72's cite of idea 2, earlier END
    P("  cross-check against idea 72's earlier cite of the SAME book (different last eval day, so a "
      "gate on it would be wrong):")
    for k, v in older.items():
        P(f"    {k:8s} idea 72 {v:9.5f}   here {par[10][k]:9.5f}   delta {par[10][k]-v:+.5f}")
    P(f"  eval window {par[10]['r'].index[0].date()} -> {par[10]['r'].index[-1].date()}   "
      f"H2 from {par[10]['r'].index[h].date()}   OOS from {oos[0].date()}")
    P(f"  GATE 1: {'3/3 EXACT' if ok1 else 'FAILED'}")
    assert ok1, "gate 1 failed — refusing to read new numbers"

    P("\n" + "=" * 108)
    P("REPRODUCTION GATE 2 — idea 273's published u56 m=999 transfer arm")
    P("=" * 108)
    want2 = dict(CAGR=0.1190, Sharpe=1.142, MaxDD=-0.1279, OOS_Sharpe=1.210, H1=1.198, H2=1.098, turn=3.49)
    tol = dict(CAGR=5e-4, Sharpe=5e-4, MaxDD=5e-4, OOS_Sharpe=5e-4, H1=5e-4, H2=5e-4, turn=5e-3)
    ok2 = True
    for k, v in want2.items():
        hit = abs(buf[10][k] - v) <= tol[k]
        ok2 &= hit
        P(f"  {k:10s} published {v:9.4f}   reproduced {buf[10][k]:9.4f}   {'EXACT' if hit else 'MISMATCH'}")
    P(f"  GATE 2: {'7/7 EXACT' if ok2 else 'FAILED'}")
    assert ok2, "gate 2 failed — refusing to read new numbers"

    P("\n" + "=" * 108)
    P("REPRODUCTION GATE 3 — the state machine at (m=0, j=inf) IS the stateless parent")
    P("=" * 108)
    w0 = band_weights(px, 0, 999)
    mask = rebalance_mask(px.index, FREQ)
    dw = (w0 - pw).abs().loc[mask.values].to_numpy().max()
    dr = (run(px, w0, 10)["returns"].loc[start:] - par[10]["r"]).abs().max()
    P(f"  max|weight diff| on rebalance rows : {dw:.3e}")
    P(f"  max|daily return diff|             : {dr:.3e}")
    P(f"  GATE 3: {'EXACT' if dw == 0.0 and dr == 0.0 else 'FAILED'}")
    assert dw == 0.0 and dr == 0.0, "gate 3 failed"

    P("\n" + "=" * 108)
    P("REPRODUCTION GATE 4 — the local mask backtester IS engine.backtest on the weekly schedule")
    P("=" * 108)
    dm = (backtest_mask(px, pw, 10, rebalance_mask(px.index, FREQ))["returns"]
          - run(px, pw, 10)["returns"]).abs().max()
    P(f"  max|daily return diff| : {dm:.3e}")
    P(f"  GATE 4: {'EXACT' if dm == 0.0 else 'FAILED'}")
    assert dm == 0.0, "gate 4 failed"

    # ------------------------------------------------------------- comparands
    v2 = {b: stats(run(px, rules_v2_weights(px), b), b) for b in RUNGS}
    v1 = {b: stats(run(px, rules_v1_weights(px), b), b) for b in RUNGS}
    P("\n" + "=" * 108)
    P("REFERENCE ROWS (u56, weekly, t+1)")
    P("=" * 108)
    hdr = (f"{'row':34s} {'bps':>4s} {'gross':>6s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
           f"{'H1':>7s} {'H2':>7s} {'OOSCAGR':>8s} {'OOSShrp':>8s} {'OOS DD':>8s} {'turn/yr':>8s}")
    P(hdr)

    def refrow(name, d):
        P(f"{name:34s} {d['bps']:4d} {d['gross']:6.3f} {d['CAGR']:7.2%} {d['Sharpe']:7.3f} "
          f"{d['MaxDD']:8.2%} {d['H1']:7.3f} {d['H2']:7.3f} {d['OOS_CAGR']:8.2%} "
          f"{d['OOS_Sharpe']:8.3f} {d['OOS_MaxDD']:8.2%} {d['turn']:8.2f}")

    for b in RUNGS:
        refrow("buffer m=999 (the candidate)", buf[b])
    for b in RUNGS:
        refrow("parent top20-200d (idea 2 KEEP)", par[b])
    for b in RUNGS:
        refrow("RULES v2 baseline (live)", v2[b])
    for b in RUNGS:
        refrow("RULES v1 (previous)", v1[b])
    sc, ss, sdd = m3(spy)
    soc, sos, sodd = m3(spy.loc[oos])
    P(f"{'SPY buy & hold':34s} {0:4d} {1.000:6.3f} {sc:7.2%} {ss:7.3f} {sdd:8.2%} "
      f"{metrics(spy.iloc[:h])['Sharpe']:7.3f} {metrics(spy.iloc[h:])['Sharpe']:7.3f} "
      f"{soc:8.2%} {sos:8.3f} {sodd:8.2%} {0.0:8.2f}")
    P(f"\n  4b bars on this sample: H1 > {metrics(spy.iloc[:h])['Sharpe']:.4f}, "
      f"H2 > {metrics(spy.iloc[h:])['Sharpe']:.4f}, OOS > {spy_oos_s:.4f}, "
      f"MaxDD >= {-0.60*abs(sdd):.2%}, CAGR >= {0.70*sc:.2%}")
    P(f"  4a bars (vs live RULES v2 @10bps): H1 > {v2[10]['H1']:.4f}, H2 > {v2[10]['H2']:.4f}, "
      f"MaxDD >= {v2[10]['MaxDD']:.2%}")

    # ================================================== the 45-cell grid, both rungs
    P("\n" + "=" * 108)
    P("THE FULL GRID — 9 m x 5 j x 2 cost rungs = 90 cells, every one printed (LITERAL gross)")
    P("=" * 108)
    P(f"{'m':>4s} {'j':>4s} {'bps':>4s} {'gross':>6s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'H1':>7s} {'H2':>7s} {'turn/yr':>7s} {'OOSShrp':>8s}  verdicts")
    rows = []
    cache = {}
    for m in MGRID:
        for j in JGRID:
            w = band_weights(px, m, j)
            cache[(m, j)] = w
            for b in RUNGS:
                d = stats(run(px, w, b), b)
                a = path4a(d["r"], v2[b]["r"])
                bb = path4b(d["r"], spy, d["OOS_Sharpe"], spy_oos_s)
                P(f"{m:4d} {j:4d} {b:4d} {d['gross']:6.3f} {d['CAGR']:7.2%} {d['Sharpe']:7.3f} "
                  f"{d['MaxDD']:8.2%} {d['H1']:7.3f} {d['H2']:7.3f} {d['turn']:7.2f} "
                  f"{d['OOS_Sharpe']:8.3f}  {vstr(a,'4a')} / {vstr(bb,'4b')}")
                rows.append(dict(scale="literal", m=m, j=j, bps=b,
                                 **{k: d[k] for k in ("gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                      "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
                                                      "OOS_MaxDD", "turn")},
                                 keep4a=not a, keep4b=not bb,
                                 fail4a=",".join(a), fail4b=",".join(bb)))
    g = pd.DataFrame(rows)
    for b in RUNGS:
        s = g[(g.bps == b) & (g.scale == "literal")]
        P(f"\n  @{b}bps LITERAL: 4a {int(s.keep4a.sum())}/45, 4b {int(s.keep4b.sum())}/45; "
          f"gross span {s.gross.min():.4f}-{s.gross.max():.4f} "
          f"(parent {par[b]['gross']:.4f}); turnover span {s.turn.min():.2f}-{s.turn.max():.2f}x/yr; "
          f"corr(turnover, Sharpe) = {s.turn.corr(s.Sharpe):+.3f}")

    # ============================================================ TEST A — matched gross
    P("\n" + "=" * 108)
    P("TEST A — MATCHED REALISED GROSS.  Every cell rescaled by c = gross_parent / gross_cell,")
    P("         so no arm can clear a SCALE bar (4b's CAGR floor, 4b/4a's drawdown cap) on exposure.")
    P("=" * 108)
    P(f"  target gross = parent's realised mean gross = {par[10]['gross']:.4f}")
    P(f"{'m':>4s} {'j':>4s} {'bps':>4s} {'c':>6s} {'gross':>6s} {'CAGR':>7s} {'Sharpe':>7s} "
      f"{'MaxDD':>8s} {'H1':>7s} {'H2':>7s} {'turn/yr':>7s} {'OOSShrp':>8s}  verdicts (matched)")
    mrows = []
    for m in MGRID:
        for j in JGRID:
            w = cache[(m, j)]
            for b in RUNGS:
                lit = g[(g.m == m) & (g.j == j) & (g.bps == b) & (g.scale == "literal")].iloc[0]
                c = par[b]["gross"] / lit["gross"]
                d = stats(run(px, w * c, b), b)
                a = path4a(d["r"], v2[b]["r"])
                bb = path4b(d["r"], spy, d["OOS_Sharpe"], spy_oos_s)
                P(f"{m:4d} {j:4d} {b:4d} {c:6.4f} {d['gross']:6.3f} {d['CAGR']:7.2%} {d['Sharpe']:7.3f} "
                  f"{d['MaxDD']:8.2%} {d['H1']:7.3f} {d['H2']:7.3f} {d['turn']:7.2f} "
                  f"{d['OOS_Sharpe']:8.3f}  {vstr(a,'4a')} / {vstr(bb,'4b')}")
                mrows.append(dict(scale="gross_matched", m=m, j=j, bps=b, c=c,
                                  **{k: d[k] for k in ("gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                       "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
                                                       "OOS_MaxDD", "turn")},
                                  keep4a=not a, keep4b=not bb,
                                  fail4a=",".join(a), fail4b=",".join(bb)))
    gm = pd.DataFrame(mrows)
    grid = pd.concat([g, gm], ignore_index=True)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    for b in RUNGS:
        s = gm[gm.bps == b]
        lit = g[(g.bps == b)]
        P(f"\n  @{b}bps MATCHED: 4a {int(s.keep4a.sum())}/45, 4b {int(s.keep4b.sum())}/45 "
          f"(literal was 4a {int(lit.keep4a.sum())}/45, 4b {int(lit.keep4b.sum())}/45); "
          f"mean |dSharpe| literal->matched = {(s.sort_values(['m','j']).Sharpe.values - lit.sort_values(['m','j']).Sharpe.values).__abs__().mean():.4f}")
    cand = gm[(gm.m == 999) & (gm.j == 999) & (gm.bps == 10)].iloc[0]
    candl = g[(g.m == 999) & (g.j == 999) & (g.bps == 10) & (g.scale == "literal")].iloc[0]
    P(f"\n  THE CANDIDATE (m=999, j=inf) @10bps:")
    P(f"    literal        gross {candl['gross']:.4f}  {candl['CAGR']:7.2%} {candl['Sharpe']:7.3f} "
      f"{candl['MaxDD']:8.2%}  4b {'KEEP' if candl['keep4b'] else 'KILL ('+candl['fail4b']+')'}")
    P(f"    gross-matched  gross {cand['gross']:.4f}  {cand['CAGR']:7.2%} {cand['Sharpe']:7.3f} "
      f"{cand['MaxDD']:8.2%}  4b {'KEEP' if cand['keep4b'] else 'KILL ('+cand['fail4b']+')'}")
    P(f"    parent         gross {par[10]['gross']:.4f}  {par[10]['CAGR']:7.2%} {par[10]['Sharpe']:7.3f} "
      f"{par[10]['MaxDD']:8.2%}")

    # ========================================================= TEST B — matched turnover
    P("\n" + "=" * 108)
    P("TEST B — MATCHED TURNOVER.  Does a slower CADENCE on the plain parent buy the same cut?")
    P("         Comparand chosen by |turnover - turnover_buffer|; no performance number selects it.")
    P("=" * 108)
    tgt = buf[10]["turn"]
    P(f"  buffer turnover to match: {tgt:.2f}x/yr   (RULES v2 runs at "
      f"{v2[10]['turn']:.2f}x/yr, the parent at {par[10]['turn']:.2f}x/yr)")
    P(f"{'cadence':>10s} {'bps':>4s} {'gross':>6s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'H1':>7s} {'H2':>7s} {'turn/yr':>7s} {'OOSShrp':>8s} {'|dturn|':>8s}  verdicts")
    crows = []
    ladder = [("D", rebalance_mask(px.index, "D")), ("W", rebalance_mask(px.index, "W"))]
    ladder += [(f"{k}W", kweek_mask(px.index, k)) for k in KWEEKS]
    ladder += [("M", rebalance_mask(px.index, "M")), ("Q", rebalance_mask(px.index, "Q"))]
    for nm, msk in ladder:
        # the parent held on that schedule: stateless top-20, traded only on the schedule
        w = band_weights(px, 0, 999, mask=msk)
        for b in RUNGS:
            d = stats(backtest_mask(px, w, b, msk), b)
            a = path4a(d["r"], v2[b]["r"])
            bb = path4b(d["r"], spy, d["OOS_Sharpe"], spy_oos_s)
            P(f"{nm:>10s} {b:4d} {d['gross']:6.3f} {d['CAGR']:7.2%} {d['Sharpe']:7.3f} {d['MaxDD']:8.2%} "
              f"{d['H1']:7.3f} {d['H2']:7.3f} {d['turn']:7.2f} {d['OOS_Sharpe']:8.3f} "
              f"{abs(d['turn']-tgt):8.2f}  {vstr(a,'4a')} / {vstr(bb,'4b')}")
            crows.append(dict(cadence=nm, bps=b,
                              **{k: d[k] for k in ("gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                   "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
                                                   "OOS_MaxDD", "turn")},
                              dturn=abs(d["turn"] - tgt), keep4a=not a, keep4b=not bb,
                              fail4a=",".join(a), fail4b=",".join(bb)))
    cad = pd.DataFrame(crows)
    cad.to_csv(f"{OUT}.cadence.csv", index=False)
    pick = cad[cad.bps == 10].sort_values("dturn").iloc[0]
    P(f"\n  turnover-matched comparand: parent at cadence {pick['cadence']} "
      f"({pick['turn']:.2f}x/yr vs the buffer's {tgt:.2f}x/yr, gap {pick['dturn']:.2f})")
    P(f"    {'series':32s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} {'OOSShrp':>8s}")
    P(f"    {'buffer m=999 (candidate)':32s} {buf[10]['CAGR']:7.2%} {buf[10]['Sharpe']:7.3f} "
      f"{buf[10]['MaxDD']:8.2%} {buf[10]['H1']:7.3f} {buf[10]['H2']:7.3f} {buf[10]['OOS_Sharpe']:8.3f}")
    P(f"    {'parent @'+str(pick['cadence'])+' (turnover-matched)':32s} {pick['CAGR']:7.2%} "
      f"{pick['Sharpe']:7.3f} {pick['MaxDD']:8.2%} {pick['H1']:7.3f} {pick['H2']:7.3f} "
      f"{pick['OOS_Sharpe']:8.3f}")
    P(f"    dSharpe (buffer - matched parent) = {buf[10]['Sharpe']-pick['Sharpe']:+.4f}; "
      f"dCAGR {buf[10]['CAGR']-pick['CAGR']:+.2%}; dMaxDD {buf[10]['MaxDD']-pick['MaxDD']:+.2%}; "
      f"dOOS Sharpe {buf[10]['OOS_Sharpe']-pick['OOS_Sharpe']:+.4f}")
    best_cad = cad[cad.bps == 10].sort_values("Sharpe").iloc[-1]
    P(f"    (for context only, never selected on: the cadence ladder's own best Sharpe is "
      f"{best_cad['cadence']} at {best_cad['Sharpe']:.3f}, {best_cad['turn']:.2f}x/yr)")

    # ============================================== TEST C — is it a different book at all
    P("\n" + "=" * 108)
    P("TEST C — OVERLAP.  Held sets on rebalance dates: buffer vs parent, buffer vs matched parent.")
    P("=" * 108)
    wmask = rebalance_mask(px.index, FREQ).values

    def overlap(wa, wb, msk):
        A = (wa.loc[msk] > 0).values
        B = (wb.loc[msk] > 0).values
        inter = (A & B).sum(axis=1).astype(float)
        union = (A | B).sum(axis=1).astype(float)
        jac = np.where(union > 0, inter / np.maximum(union, 1), np.nan)
        ident = float(np.nanmean((A == B).all(axis=1)))
        return float(np.nanmean(jac)), ident

    wbuf = cache[(999, 999)]
    pick_mask = dict(ladder)[pick["cadence"]]
    wmatched = band_weights(px, 0, 999, mask=pick_mask)
    wmask_s = rebalance_mask(px.index, FREQ)
    for nm, wo, msk_o in (("parent top20-200d (weekly)", pw, wmask_s),
                          (f"parent @{pick['cadence']} (turnover-matched)", wmatched, pick_mask),
                          ("RULES v2 (live book)", rules_v2_weights(px), wmask_s)):
        jac, ident = overlap(wbuf, wo, wmask)
        rb = buf[10]["r"]
        ro = stats(backtest_mask(px, wo, 10, msk_o), 10)["r"]
        P(f"  buffer vs {nm:38s}  mean Jaccard {jac:.3f}   identical-set share {ident:.3f}   "
          f"corr(daily returns) {rb.corr(ro):.4f}")
    hb = (wbuf.loc[wmask] > 0).sum(axis=1)
    hp = (pw.loc[wmask] > 0).sum(axis=1)
    P(f"  mean held count: buffer {hb.mean():.2f}, parent {hp.mean():.2f} "
      f"(buffer holds MORE on {float((hb>hp).mean()):.1%} of rebalance dates, "
      f"fewer on {float((hb<hp).mean()):.1%})")

    # ==================================================================== rule 8
    P("\n" + "=" * 108)
    P("RULE 8 WALK-FORWARD — (m, j) chosen on 2009-2016 by IS Sharpe alone, 2017-2026 untouched")
    P("=" * 108)
    wf = []
    for b in RUNGS:
        for scale in ("literal", "gross_matched"):
            s = grid[(grid.bps == b) & (grid.scale == scale)]
            ip = s.loc[s.IS_Sharpe.idxmax()]
            pr_ = s[(s.m == 0) & (s.j == 999)].iloc[0]
            rho = s.IS_Sharpe.rank().corr(s.OOS_Sharpe.rank())   # Spearman via ranks (no scipy in sandbox)
            P(f"\n  @{b}bps [{scale}] IS pick m={int(ip['m'])}, j={int(ip['j'])} "
              f"(IS Sharpe {ip['IS_Sharpe']:.4f} vs parent's {pr_['IS_Sharpe']:.4f}); "
              f"Spearman(IS, OOS) over 45 cells = {rho:+.3f}; "
              f"IS-best is OOS-best: {bool(s.OOS_Sharpe.idxmax() == s.IS_Sharpe.idxmax())}")
            P(f"    {'series':34s} {'OOSCAGR':>8s} {'OOSShrp':>8s} {'OOS DD':>8s}")
            P(f"    {'IS-picked cell':34s} {ip['OOS_CAGR']:8.2%} {ip['OOS_Sharpe']:8.3f} {ip['OOS_MaxDD']:8.2%}")
            cd = s[(s.m == 999) & (s.j == 999)].iloc[0]
            P(f"    {'the candidate (m=999, j=inf)':34s} {cd['OOS_CAGR']:8.2%} {cd['OOS_Sharpe']:8.3f} "
              f"{cd['OOS_MaxDD']:8.2%}")
            P(f"    {'parent top20-200d':34s} {pr_['OOS_CAGR']:8.2%} {pr_['OOS_Sharpe']:8.3f} "
              f"{pr_['OOS_MaxDD']:8.2%}")
            P(f"    {'RULES v2 baseline (live)':34s} {v2[b]['OOS_CAGR']:8.2%} {v2[b]['OOS_Sharpe']:8.3f} "
              f"{v2[b]['OOS_MaxDD']:8.2%}")
            P(f"    {'SPY':34s} {soc:8.2%} {sos:8.3f} {sodd:8.2%}")
            P(f"    dOOS Sharpe: pick-parent {ip['OOS_Sharpe']-pr_['OOS_Sharpe']:+.4f}, "
              f"pick-v2 {ip['OOS_Sharpe']-v2[b]['OOS_Sharpe']:+.4f}, pick-SPY {ip['OOS_Sharpe']-sos:+.4f}, "
              f"candidate-v2 {cd['OOS_Sharpe']-v2[b]['OOS_Sharpe']:+.4f}")
            wf.append(dict(bps=b, scale=scale, m=int(ip["m"]), j=int(ip["j"]),
                           IS_Sharpe=ip["IS_Sharpe"], OOS_CAGR=ip["OOS_CAGR"],
                           OOS_Sharpe=ip["OOS_Sharpe"], OOS_MaxDD=ip["OOS_MaxDD"],
                           parent_OOS_Sharpe=pr_["OOS_Sharpe"], cand_OOS_Sharpe=cd["OOS_Sharpe"],
                           v2_OOS_Sharpe=v2[b]["OOS_Sharpe"], spy_OOS_Sharpe=sos, spearman=rho,
                           is_best_is_oos_best=bool(s.OOS_Sharpe.idxmax() == s.IS_Sharpe.idxmax())))
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n  Pre-registered caveat (idea 111): 2017-2026 is very nearly H2 on this sample, so the")
    P("  rule-8 OOS bar and 4b's H2 bar overlap; the OOS pass is weaker evidence than it looks.")

    # =================================================================== verdict
    P("\n" + "=" * 108)
    P("VERDICT")
    P("=" * 108)
    P(f"  candidate @10bps literal      : 4b {'KEEP' if candl['keep4b'] else 'KILL ('+candl['fail4b']+')'}, "
      f"4a {'KEEP' if candl['keep4a'] else 'KILL ('+candl['fail4a']+')'}")
    P(f"  candidate @10bps gross-matched: 4b {'KEEP' if cand['keep4b'] else 'KILL ('+cand['fail4b']+')'}, "
      f"4a {'KEEP' if cand['keep4a'] else 'KILL ('+cand['fail4a']+')'}")
    c25 = gm[(gm.m == 999) & (gm.j == 999) & (gm.bps == 25)].iloc[0]
    P(f"  candidate @25bps gross-matched: 4b {'KEEP' if c25['keep4b'] else 'KILL ('+c25['fail4b']+')'}, "
      f"4a {'KEEP' if c25['keep4a'] else 'KILL ('+c25['fail4a']+')'}")
    P(f"  vs the turnover-matched parent: dSharpe {buf[10]['Sharpe']-pick['Sharpe']:+.4f}, "
      f"dOOS {buf[10]['OOS_Sharpe']-pick['OOS_Sharpe']:+.4f}, "
      f"dMaxDD {buf[10]['MaxDD']-pick['MaxDD']:+.2%}")
    P(f"  vs the live RULES v2         : dSharpe {buf[10]['Sharpe']-v2[10]['Sharpe']:+.4f}, "
      f"dOOS {buf[10]['OOS_Sharpe']-v2[10]['OOS_Sharpe']:+.4f}, "
      f"dMaxDD {buf[10]['MaxDD']-v2[10]['MaxDD']:+.2%}, "
      f"turnover {buf[10]['turn']:.2f}x vs {v2[10]['turn']:.2f}x/yr")

    Path(f"{OUT}.console.txt").write_text("\n".join(_LINES) + "\n")


if __name__ == "__main__":
    main()

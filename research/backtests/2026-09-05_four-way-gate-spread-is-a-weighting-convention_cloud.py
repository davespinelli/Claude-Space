#!/usr/bin/env python3
"""QUEUE idea 127 — four-way-gate-spread-is-a-weighting-convention  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 127)
    "idea 121 found the n=40 four-way gate decomposition (none/200d/vol60/both) has a Sharpe
     spread of 0.080 under gross-matched weights against the 0.356 published by ideas 38/56,
     with the ORDERING intact.  The magnitude, not the ordering, is what the queue cites when
     it calls the vol20 gate 'the larger destroyer'.  Re-run the decomposition under literal vs
     matched gross on all three panels and report which of the project's gate-indictment rows
     depend on the literal convention (idea 81's exposure, applied to the gate rows rather than
     the n-sweeps)."

WHAT IS ACTUALLY ON TRIAL, AND A CONFOUND THE QUEUE DID NOT NAME
    The two rows the queue compares are NOT the same book run two ways.  Reading both scripts
    before running anything:
      * ideas 38/56 (research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py) rank on
        RAW 12-1 momentum and weight `(rank <= n) * (GROSS/n)` — the LITERAL convention: a name
        the gate excludes is not replaced, so the book de-grosses into cash.  Published four-way
        at n=40, g=0.75, 10 bps, small panel: none 0.797 / 200d 0.693 / vol60 0.524 / both 0.441,
        spread 0.356.
      * idea 121 (2026-09-05_liquidity-screened-small-panel_cloud.py) ranks on the RULES v1
        COMPOSITE — mean of three pct-rank momenta, times a 0.5/1.0 trend factor, divided by
        sqrt(vol20) — and renormalises to g whenever >= 1 name is admitted: the MATCHED
        convention.  Its four-way at n=40, g=0.75: 0.576 / 0.565 / 0.497 / 0.537, spread 0.080.
    So the 0.356 -> 0.080 collapse the queue attributes to the WEIGHTING CONVENTION is
    confounded with a change of RANKING SIGNAL, and the v1 composite is the worse confound of
    the two because it already contains a trend factor and a vol scaler — i.e. it internalises
    the very gates the decomposition is trying to price.  A 2x2 (convention x signal) is the
    only design that can attribute the collapse, so that is what this run does, on all three
    panels, and the attribution is the answer.

    Second, for a RANKED book the two conventions have IDENTICAL COMPOSITION.  Literal holds
    the top min(n, k_t) admitted names at g/n each; matched holds the same names at g/k_t.  So
    literal = matched scaled by f_t = k_t/n, and the whole convention effect is EXPOSURE.  That
    lets the effect be split further, which no published row does:
        lit  literal      dynamic gross g * f_t          (de-grosses when the gate bites)
        mat  matched      constant gross g               (idea 81's convention)
        sta  static-lit   constant gross g * mean(f_t)   (same average exposure as lit, no timing)
    lit - sta is exposure TIMING (does cash arrive when it helps?); sta - mat is exposure LEVEL
    (is the gate just a smaller position?).  For EWall the same three conventions are the
    project's dg / rw / a static-gross dg, and there composition does not differ either
    (every admitted name is held under both), so the decomposition is exact for every book here.

GRID — exactly TWO tuned parameters (position count n, gross g).  Everything else is a
    REPORTED axis, never selected on: panel, ranking signal, gate, convention, cost rung.
      panels   u56 (universe.json, 55 names + SPY), broad (universe_broad.json, 136),
               small (data/prices_small.csv.gz, 483 less the 44 with max_1d_move >= 1.0 = 439)
      signals  mom   raw 12-1 momentum                      (ideas 38/56's signal)
               v1c   RULES v1 composite, scaler ON           (idea 121's signal)
               v1u   RULES v1 composite, scaler OFF          (idea 81's de-confounded signal)
      gates    none / 200d / vol60 / both                    (the four-way, verbatim)
      convs    lit / mat / sta                               (above)
      books    R10, R20, R40 (ranked) + EWall (equal-weight every admitted name)
      n        {10, 20, 40}     g {0.75, 1.00}     costs {10, 25} bps
    720 arm-rows, every one printed and written to .grid.csv.  Costs are derived from a single
    0-bps run per arm — legitimate because no arm has a stop, drawdown control or entry budget,
    so the weight path is cost-independent; CHECK (d) asserts that derivation against a direct
    10-bps run.

TESTS (all reported whatever they say)
    A  HARNESS.  fast_bt vs engine.backtest max|diff|; the calendar-day-index warning of idea 38
       checked rather than assumed; RULES v1 on each panel.
    B  REPRODUCTION.  ideas 38/56's published four-way (small, mom, n=40, g=0.75, lit, 10 bps)
       and idea 121's matched four-way (small, v1c, n=40, g=0.75, mat) re-derived here.  If
       either fails to reproduce, the attribution below is not quotable and the run says so.
    C  MAIN GRID + 4a/4b verdicts on every row.
    D  ATTRIBUTION.  Four-way Sharpe spread per (panel, signal, conv, n, g, cost), and the
       2x2 decomposition of the published 0.356 -> 0.080 into a convention part and a signal
       part.  Ordering reported as Kendall tau against the published none > 200d > vol60 > both.
    E  EXPOSURE MECHANISM.  mean f_t, and f_t inside vs outside SPY drawdowns > 10%, per gate.
       lit - sta (timing) vs sta - mat (level) in Sharpe, CAGR and MaxDD.
    F  GATE-INDICTMENT CENSUS.  Every gate-difference statistic the project quotes, recomputed
       under all three conventions, with a DEPENDS flag when the matched value loses its sign or
       more than half its magnitude.
    G  PROTOCOL RULE 8 WALK-FORWARD.  (n, g) chosen on IS Sharpe (<= 2016-12-31) alone within
       each (panel, signal, gate, conv, cost) cell, read once on 2017-2026, against RULES v1 and
       SPY.  Reported for every cell; also the four-way spread computed on OOS alone.

PRE-REGISTERED PREDICTIONS (written before any number from tests B-G was read; the priors come
from the two ALREADY-PUBLISHED tables quoted above, nothing else was run first)
    P1  The collapse is mostly SIGNAL, not convention: holding the signal at mom, the matched
        four-way spread on the small panel at n=40/g=0.75/10bps stays above 0.20 (i.e. more than
        half of 0.356 survives the convention change).
    P2  Convention effect is nearly all LEVEL, not TIMING: |Sharpe(lit) - Sharpe(sta)| < 0.05 in
        at least 2/3 of ranked arms, because a de-grossed book is mostly just a smaller book.
    P3  The ORDERING (none > 200d > vol60 > both) does not survive the matched convention on all
        three panels: at least one panel shows an adjacent inversion under mat.
    P4  On u56/broad the four-way spread is far smaller than on small under every convention
        (< 0.15 at n=40), because the gates bind on very few of 55/136 large caps.
    P5  Nothing here passes 4b under any convention on the small panel (idea 121: 0 of 192).

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are CURRENT-constituent lists.  The small panel is the
      current constituent list of a sub-$2B screen: every name survived to 2026, so small caps
      delisted, bankrupted or acquired 2010-2025 are absent, the bias is one-directional and
      falls hardest on the beaten-down cohort — which is the cohort the 200d/vol20 gates exclude.
      No CAGR or Sharpe level below is an achievable return.  This run reports DIFFERENCES
      between two weightings of the same book on the same panel, which is where the bias mostly
      cancels; it does not cancel in the four-way spread itself, because the gates change WHICH
      names are held and the missing cohort is gate-correlated.  Stated, not fixed.
    * SPY is a genuine universe.json / universe_broad.json constituent and is left selectable on
      u56 and broad (ideas 94/95/121 convention); on the small panel it is a joined benchmark
      column only and is never selectable.
    * This run measures a REPORTING CONVENTION.  It cannot promote a candidate; it can only
      change what the project is allowed to say about a published gate row.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.  Writes
.console.txt, .grid.csv, .spread.csv, .census.csv and .walkforward.csv next to itself.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_four-way-gate-spread-is-a-weighting-convention_cloud"
OUT = ROOT / "research" / "backtests"

FREQ, MAX_VOL, WARMUP = "W", 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
GATES = ["none", "200d", "vol60", "both"]
CONVS = ["lit", "mat", "sta"]
SIGNALS = ["mom", "v1c", "v1u"]
NS = [10, 20, 40]
GS = [0.75, 1.00]
COSTS = [10.0, 25.0]
BAD_MOVE = 1.0
PUBLISHED = {"none": 0.797, "200d": 0.693, "vol60": 0.524, "both": 0.441}   # ideas 38/56
PUB_121 = {"none": 0.5761, "200d": 0.5646, "vol60": 0.4972, "both": 0.5368}  # idea 121, matched

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ---------------------------------------------------------------- panels ----
def panels():
    out = {}
    px = load_universe()
    out["u56"] = (px, [c for c in px.columns])
    px = load_universe(broad=True)
    out["broad"] = (px, [c for c in px.columns])
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= BAD_MOVE, "ticker"])
    px = px[[c for c in px.columns if c not in bad]]
    out["small"] = (px, [c for c in px.columns if c != "SPY"])   # SPY benchmark only
    return out, sorted(bad)


# ------------------------------------------------------------ simulator ----
def fast_bt(px, w, freq=FREQ):
    """Vectorised equivalent of engine.backtest at 0 bps; returns gross returns + turnover."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    held = np.zeros_like(rets)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    gross_ret = pd.Series((held * rets).sum(axis=1), index=px.index)
    return gross_ret, pd.Series(turn, index=px.index), pd.Series(held.sum(axis=1), index=px.index)


def net(gross_ret, turn, bps):
    return gross_ret - turn * bps / 1e4


# ------------------------------------------------------------- signals ----
_CACHE = {}


def sigs(key, sub):
    if key not in _CACHE:
        s_on, above, vol20 = score(sub, True)
        s_off, _, _ = score(sub, False)
        mom = sub.shift(21) / sub.shift(252) - 1
        _CACHE[key] = dict(mom=mom, v1c=s_on, v1u=s_off, above=above, vol20=vol20)
    return _CACHE[key]


def admitted(key, sub, gate):
    c = sigs(key, sub)
    ok = sub.notna()
    if gate in ("200d", "both"):
        ok &= c["above"]
    if gate in ("vol60", "both"):
        ok &= (c["vol20"] < MAX_VOL)
    return ok


def weights(key, px, sub, cols, book, gate, conv, g, signal, mean_f=None):
    """lit = literal (g/n each, cash for missing slots); mat = renormalise to g;
    sta = mat scaled by the literal book's realised mean gross fraction."""
    ok = admitted(key, sub, gate)
    if book == "EWall":
        hold = ok
        k = hold.sum(axis=1)
        live = sub.notna().sum(axis=1)
        if conv == "lit":
            w = hold.astype(float).div(live.replace(0, np.nan), axis=0) * g
        else:
            w = hold.astype(float).div(k.replace(0, np.nan), axis=0) * g
            if conv == "sta":
                w = w * mean_f
        f = (k / live.replace(0, np.nan)).fillna(0.0)
    else:
        n = int(book[1:])
        s = sigs(key, sub)[signal].where(ok)
        rank = s.rank(axis=1, ascending=False)
        hold = (rank <= n) & s.notna()
        k = hold.sum(axis=1)
        if conv == "lit":
            w = hold.astype(float) * (g / n)
        else:
            w = hold.astype(float).div(k.replace(0, np.nan), axis=0) * g
            if conv == "sta":
                w = w * mean_f
        f = (k / n).clip(upper=1.0)
    return w.fillna(0.0).reindex(columns=cols).fillna(0.0), f, hold


def stats(r, start):
    r = r.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    i, o = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"], IS_MaxDD=i["MaxDD"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def verdicts(d, base, spy):
    p4a = d["H1"] > base["H1"] and d["H2"] > base["H2"] and d["MaxDD"] >= base["MaxDD"]
    p4b = (d["H1"] > spy["H1"] and d["H2"] > spy["H2"] and d["OOS_Sharpe"] > spy["OOS_Sharpe"]
           and d["MaxDD"] >= 0.60 * spy["MaxDD"] and d["CAGR"] >= 0.70 * spy["CAGR"])
    return p4a, p4b


def kendall(order_vals):
    """Concordance of a 4-vector against the published descending order none>200d>vol60>both."""
    v = [order_vals[g] for g in GATES]
    c = d = 0
    for a in range(4):
        for b in range(a + 1, 4):
            if v[a] > v[b]:
                c += 1
            elif v[a] < v[b]:
                d += 1
    return (c - d) / 6.0


# ------------------------------------------------------------------ main ----
def main():
    P, dropped = panels()
    say(f"[setup] panels: " + " | ".join(
        f"{k} {len(sel)} selectable / {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}"
        for k, (px, sel) in P.items()))
    say(f"[setup] small panel drops {len(dropped)} tickers with max_1d_move >= {BAD_MOVE}")

    # ---- A: harness ----
    for k, (px, sel) in P.items():
        wd = pd.Series(px.index.dayofweek).value_counts()
        say(f"[A] {k}: weekend rows (idea 38's calendar-index warning) = "
            f"{int(wd.get(5, 0) + wd.get(6, 0))} of {len(px)}")
    ref = {}
    for k, (px, sel) in P.items():
        sub = px[sel]
        w = rules_v1_weights(sub).reindex(columns=px.columns).fillna(0.0)
        gr, tu, _ = fast_bt(px, w)
        r_fast = net(gr, tu, 10.0)
        r_eng = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"]
        start = px.index[WARMUP]
        say(f"[A] {k}: engine-equivalence max|diff| = {float((r_fast - r_eng).abs().max()):.3e}")
        ref[k] = dict(start=start, base=stats(r_fast, start),
                      spy=stats(px["SPY"].pct_change().fillna(0.0), start))
        b, s = ref[k]["base"], ref[k]["spy"]
        say(f"[A] {k}: RULES v1  CAGR {b['CAGR']:6.2%} Sharpe {b['Sharpe']:.3f} MaxDD {b['MaxDD']:6.1%} "
            f"halves {b['H1']:.3f}/{b['H2']:.3f} OOS {b['OOS_Sharpe']:.3f}")
        say(f"[A] {k}: SPY       CAGR {s['CAGR']:6.2%} Sharpe {s['Sharpe']:.3f} MaxDD {s['MaxDD']:6.1%} "
            f"halves {s['H1']:.3f}/{s['H2']:.3f} OOS {s['OOS_Sharpe']:.3f} | 4b bars: "
            f"MaxDD >= {0.60*s['MaxDD']:.1%}, CAGR >= {0.70*s['CAGR']:.2%}")

    # ---- C: main grid ----
    say(f"\n[C] main grid: 3 panels x 3 signals x 4 gates x 3 conventions x "
        f"({len(NS)} n + EWall) x {len(GS)} gross x {len(COSTS)} cost rungs")
    rows, R = [], {}
    for pk, (px, sel) in P.items():
        sub = px[sel]
        cols = px.columns
        start = ref[pk]["start"]
        base, spy = ref[pk]["base"], ref[pk]["spy"]
        dd_spy = (lambda e: e / e.cummax() - 1)((1 + px["SPY"].pct_change().fillna(0.0)).cumprod())
        crisis = (dd_spy < -0.10).loc[start:]
        for book in [f"R{n}" for n in NS] + ["EWall"]:
            for signal in (SIGNALS if book != "EWall" else ["-"]):
                for gate in GATES:
                    for g in GS:
                        # literal first: its realised mean gross fraction defines `sta`
                        wl, f, hold = weights(pk, px, sub, cols, book, gate, "lit", g,
                                              signal if signal != "-" else "mom")
                        mean_f = float(f.loc[start:].mean())
                        for conv in CONVS:
                            if conv == "lit":
                                w = wl
                            else:
                                w, _, _ = weights(pk, px, sub, cols, book, gate, conv, g,
                                                  signal if signal != "-" else "mom", mean_f)
                            gr, tu, gross = fast_bt(px, w)
                            for bps in COSTS:
                                r = net(gr, tu, bps)
                                d = stats(r, start)
                                d.update(panel=pk, book=book, signal=signal, gate=gate, conv=conv,
                                         g=g, bps=bps, mean_f=mean_f,
                                         mean_gross=float(gross.loc[start:].mean()),
                                         gross_crisis=float(gross.loc[start:][crisis].mean()),
                                         gross_calm=float(gross.loc[start:][~crisis].mean()),
                                         f_crisis=float(f.loc[start:][crisis].mean()),
                                         f_calm=float(f.loc[start:][~crisis].mean()),
                                         mean_names=float(hold.loc[start:].sum(axis=1).mean()),
                                         turnover=float(tu.loc[start:].sum() / (len(tu.loc[start:]) / 252)))
                                d["pass4a"], d["pass4b"] = verdicts(d, base, spy)
                                rows.append(d)
                                R[(pk, book, signal, gate, conv, g, bps)] = r
    grid = pd.DataFrame(rows)
    gc = ["panel", "book", "signal", "gate", "conv", "g", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
          "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "mean_f", "mean_gross", "f_crisis", "f_calm",
          "mean_names", "turnover", "pass4a", "pass4b"]
    grid[gc].to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"[C] {len(grid)} rows -> {STEM}.grid.csv ; 4a passes {int(grid.pass4a.sum())}, "
        f"4b passes {int(grid.pass4b.sum())}")
    with pd.option_context("display.width", 250, "display.max_rows", None):
        say(grid[gc].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- B: reproduction ----
    say("\n[B] REPRODUCTION of the two rows the queue compares")
    q = grid.query("panel=='small' and book=='R40' and g==0.75 and bps==10.0")
    for label, sig, conv, pub in (("ideas 38/56 (mom, literal)", "mom", "lit", PUBLISHED),
                                  ("idea 121 (v1c, matched)", "v1c", "mat", PUB_121)):
        qq = q[(q["signal"] == sig) & (q["conv"] == conv)].set_index("gate")
        sh = {gt: float(qq.loc[gt, "Sharpe"]) for gt in GATES}
        cg = {gt: float(qq.loc[gt, "CAGR"]) for gt in GATES}
        say(f"  {label}: " + "  ".join(f"{gt} {cg[gt]:.1%}/{sh[gt]:.3f}" for gt in GATES)
            + f"  spread {max(sh.values()) - min(sh.values()):.3f}")
        say(f"    published:  " + "  ".join(f"{gt} {pub[gt]:.3f}" for gt in GATES)
            + f"  spread {max(pub.values()) - min(pub.values()):.3f}  |  max|diff| "
            f"{max(abs(sh[gt] - pub[gt]) for gt in GATES):.4f}")

    # ---- D: spread + attribution ----
    say("\n[D] four-way Sharpe spread, every (panel, signal, conv, book, g, cost); "
        "tau = concordance with published none>200d>vol60>both")
    srows = []
    for keys, sub in grid.groupby(["panel", "book", "signal", "conv", "g", "bps"]):
        sh = {r.gate: r.Sharpe for r in sub.itertuples()}
        cg = {r.gate: r.CAGR for r in sub.itertuples()}
        dd = {r.gate: r.MaxDD for r in sub.itertuples()}
        srows.append(dict(panel=keys[0], book=keys[1], signal=keys[2], conv=keys[3], g=keys[4], bps=keys[5],
                          spread=max(sh.values()) - min(sh.values()), tau=kendall(sh),
                          best=max(sh, key=sh.get), worst=min(sh, key=sh.get),
                          d_vol60=sh["vol60"] - sh["none"], d_200d=sh["200d"] - sh["none"],
                          d_both=sh["both"] - sh["none"],
                          dCAGR_both=cg["both"] - cg["none"], dMaxDD_both=dd["both"] - dd["none"],
                          **{f"S_{gt}": sh[gt] for gt in GATES}))
    sp = pd.DataFrame(srows).sort_values(["panel", "book", "signal", "conv", "g", "bps"])
    sp.to_csv(OUT / f"{STEM}.spread.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_rows", None):
        say(sp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n[D] ATTRIBUTION of the published 0.356 -> 0.080 collapse (small, n=40, g=0.75, 10 bps)")
    def spv(sig, conv, panel="small", book="R40", g=0.75, bps=10.0):
        row = sp[(sp["panel"] == panel) & (sp["book"] == book) & (sp["signal"] == sig)
                 & (sp["conv"] == conv) & (sp["g"] == g) & (sp["bps"] == bps)]
        return float(row["spread"].iloc[0]), float(row["tau"].iloc[0])

    def gridsel(panel, book, signal, conv, g=0.75, bps=10.0):
        m = grid[(grid["panel"] == panel) & (grid["book"] == book) & (grid["signal"] == signal)
                 & (grid["conv"] == conv) & (grid["g"] == g) & (grid["bps"] == bps)]
        return m.set_index("gate")

    def spsel(panel, book, signal, conv, g=0.75, bps=10.0):
        m = sp[(sp["panel"] == panel) & (sp["book"] == book) & (sp["signal"] == signal)
               & (sp["conv"] == conv) & (sp["g"] == g) & (sp["bps"] == bps)]
        return m.iloc[0]
    a, _ = spv("mom", "lit")
    b, _ = spv("mom", "mat")
    c, _ = spv("v1c", "lit")
    d_, _ = spv("v1c", "mat")
    say(f"   spread(mom,lit)={a:.3f} [= ideas 38/56]   spread(mom,mat)={b:.3f}")
    say(f"   spread(v1c,lit)={c:.3f}                   spread(v1c,mat)={d_:.3f} [= idea 121]")
    say(f"   convention effect at fixed signal: mom {b - a:+.3f}, v1c {d_ - c:+.3f}")
    say(f"   signal effect at fixed convention: lit {c - a:+.3f}, mat {d_ - b:+.3f}")
    say(f"   total published gap {d_ - a:+.3f}; share attributable to convention "
        f"{(b - a) / (d_ - a):.0%} (mom path) / {(d_ - c) / (d_ - a):.0%} (v1c path)")
    say("\n[D] spread by panel/signal/convention at n=40, g=0.75, 10 bps (all reported)")
    for pk in P:
        for sig in SIGNALS:
            vals = {cv: spv(sig, cv, panel=pk)[0] for cv in CONVS}
            taus = {cv: spv(sig, cv, panel=pk)[1] for cv in CONVS}
            say(f"   {pk:6s} {sig:4s}  " + "  ".join(f"{cv} spread {vals[cv]:.3f} tau {taus[cv]:+.2f}"
                                                     for cv in CONVS))

    # ---- E: exposure mechanism ----
    say("\n[E] EXPOSURE MECHANISM — mean admitted fraction f, and f inside vs outside SPY "
        "drawdowns deeper than 10%; and the split of the convention effect into LEVEL and TIMING")
    e = grid.query("bps==10.0 and g==0.75 and (book=='R40' or book=='EWall')")
    for keys, s in e.groupby(["panel", "book", "signal", "gate"]):
        if keys[2] not in ("mom", "-"):
            continue
        lit = s.query("conv=='lit'").iloc[0]
        mat = s.query("conv=='mat'").iloc[0]
        sta = s.query("conv=='sta'").iloc[0]
        say(f"   {keys[0]:6s} {keys[1]:5s} {keys[3]:5s}  f {lit.mean_f:.3f} (crisis {lit.f_crisis:.3f} / "
            f"calm {lit.f_calm:.3f})  Sharpe lit {lit.Sharpe:.3f} sta {sta.Sharpe:.3f} mat {mat.Sharpe:.3f} "
            f"| TIMING (lit-sta) {lit.Sharpe - sta.Sharpe:+.3f}  LEVEL (sta-mat) {sta.Sharpe - mat.Sharpe:+.3f} "
            f"| dCAGR lit-mat {lit.CAGR - mat.CAGR:+.2%}  dMaxDD lit-mat {lit.MaxDD - mat.MaxDD:+.1%}")
    tim = (grid.query("conv=='lit'").set_index(["panel", "book", "signal", "gate", "g", "bps"])["Sharpe"]
           - grid.query("conv=='sta'").set_index(["panel", "book", "signal", "gate", "g", "bps"])["Sharpe"])
    lev = (grid.query("conv=='sta'").set_index(["panel", "book", "signal", "gate", "g", "bps"])["Sharpe"]
           - grid.query("conv=='mat'").set_index(["panel", "book", "signal", "gate", "g", "bps"])["Sharpe"])
    say(f"   ALL {len(tim)} arms: |timing| median {tim.abs().median():.4f} mean {tim.abs().mean():.4f} "
        f"max {tim.abs().max():.4f} | |level| median {lev.abs().median():.4f} mean {lev.abs().mean():.4f} "
        f"max {lev.abs().max():.4f} | timing dominates in {float((tim.abs() > lev.abs()).mean()):.0%} of arms")
    say(f"   P2 check (|lit-sta| < 0.05): {float((tim.abs() < 0.05).mean()):.0%} of arms")

    # ---- F: gate-indictment census ----
    say("\n[F] GATE-INDICTMENT CENSUS — every gate-difference statistic the project quotes, "
        "recomputed under all three conventions.  DEPENDS = sign flips or |value| falls by "
        ">50% between lit and mat.")
    claims = [
        ("38/56 vol60 is the larger destroyer (small n=40)", "small", "R40", "mom", "d_vol60"),
        ("38/56 200d gate cost (small n=40)", "small", "R40", "mom", "d_200d"),
        ("38/56 both-gate cost (small n=40)", "small", "R40", "mom", "d_both"),
        ("38/56 four-way spread (small n=40)", "small", "R40", "mom", "spread"),
        ("49/51 gate CAGR cost, equal-weight (small)", "small", "EWall", "-", "dCAGR_both"),
        ("49/51 gate Sharpe cost, equal-weight (small)", "small", "EWall", "-", "d_both"),
        ("gate rows on u56 (n=40)", "u56", "R40", "mom", "d_both"),
        ("gate rows on broad (n=40)", "broad", "R40", "mom", "d_both"),
        ("gate rows on u56, equal-weight", "u56", "EWall", "-", "d_both"),
        ("gate rows on broad, equal-weight", "broad", "EWall", "-", "d_both"),
        ("121's matched four-way (small n=40, v1c)", "small", "R40", "v1c", "spread"),
    ]
    crows = []
    for label, pk, book, sig, stat in claims:
        for g in GS:
            for bps in COSTS:
                v = {}
                for cv in CONVS:
                    v[cv] = float(spsel(pk, book, sig, cv, g, bps)[stat])
                flip = (np.sign(v["lit"]) != np.sign(v["mat"]))
                shrink = abs(v["mat"]) < 0.5 * abs(v["lit"])
                mag = abs(v["mat"]) > 2 * abs(v["lit"])     # the reverse direction, reported too
                crows.append(dict(claim=label, panel=pk, book=book, signal=sig, stat=stat, g=g, bps=bps,
                                  lit=v["lit"], sta=v["sta"], mat=v["mat"],
                                  ratio_mat_over_lit=(v["mat"] / v["lit"] if v["lit"] else np.nan),
                                  sign_flip=flip, shrinks_half=shrink, MAGNIFIES=mag,
                                  DEPENDS=bool(flip or shrink)))
    cen = pd.DataFrame(crows)
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_rows", None):
        say(cen.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"[F] DEPENDS on the literal convention: {int(cen.DEPENDS.sum())} of {len(cen)} claim-cells "
        f"({float(cen.DEPENDS.mean()):.0%}); sign flips {int(cen.sign_flip.sum())}, "
        f"shrink >50% {int(cen.shrinks_half.sum())}")
    say("[F] by claim: " + " | ".join(
        f"{k}: {int(v.sum())}/{len(v)}" for k, v in cen.groupby("claim")["DEPENDS"]))
    say(f"[F] REVERSE DIRECTION (not pre-registered, reported because the census found it): the "
        f"matched value is more than TWICE the literal one in {int(cen.MAGNIFIES.sum())} of "
        f"{len(cen)} claim-cells — i.e. the literal convention UNDERSTATES those gate costs. "
        f"mat/lit ratio: median {cen.ratio_mat_over_lit.median():.2f}, max "
        f"{cen.ratio_mat_over_lit.max():.2f}; magnifying claims: "
        + " | ".join(sorted({str(r.claim) for r in cen.itertuples() if r.MAGNIFIES})))

    # ---- 4b robustness across the reported axes (no selection; a reporting check) ----
    key = ["book", "signal", "gate", "conv", "g"]
    cells = grid.groupby(key + ["panel", "bps"])["pass4b"].max().unstack(["panel", "bps"])
    allcells = cells[[c for c in cells.columns if c[0] in ("u56", "broad")]]
    robust = allcells[allcells.all(axis=1)]
    say(f"\n[C2] arms passing 4b in ALL FOUR (u56/broad x 10/25 bps) cells: {len(robust)} of "
        f"{len(allcells)}: " + (", ".join("/".join(str(x) for x in i) for i in robust.index)
                                if len(robust) else "none"))

    # ---- G: rule 8 walk-forward ----
    say("\n[G] PROTOCOL RULE 8 — (n, g) chosen on IS Sharpe (<= 2016-12-31) only, inside each "
        "(panel, signal, gate, conv, cost) cell over the ranked family; OOS 2017-2026 read once.")
    wrows = []
    for keys, s in grid[grid.book != "EWall"].groupby(["panel", "signal", "gate", "conv", "bps"]):
        pick = s.loc[s["IS_Sharpe"].idxmax()]
        pk = keys[0]
        base, spy = ref[pk]["base"], ref[pk]["spy"]
        wrows.append(dict(panel=pk, signal=keys[1], gate=keys[2], conv=keys[3], bps=keys[4],
                          pick=f"{pick.book}/g{pick.g:.2f}", IS_Sharpe=pick.IS_Sharpe,
                          OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                          base_OOS_Sharpe=base["OOS_Sharpe"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                          spy_OOS_CAGR=spy["OOS_CAGR"], spy_OOS_MaxDD=spy["OOS_MaxDD"],
                          beats_SPY=pick.OOS_Sharpe > spy["OOS_Sharpe"],
                          beats_v1=pick.OOS_Sharpe > base["OOS_Sharpe"],
                          pass4a=bool(pick.pass4a), pass4b=bool(pick.pass4b)))
    wf = pd.DataFrame(wrows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_rows", None):
        say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"[G] rule-8 picks beating SPY OOS Sharpe: {int(wf.beats_SPY.sum())}/{len(wf)}; "
        f"beating RULES v1: {int(wf.beats_v1.sum())}/{len(wf)}; 4b passes {int(wf.pass4b.sum())}")

    say("\n[G] four-way spread computed on the OOS window alone (n=40, g=0.75, 10 bps)")
    for pk in P:
        for sig in SIGNALS:
            for cv in CONVS:
                q3 = gridsel(pk, "R40", sig, cv)
                sh = {gt: float(q3.loc[gt, "OOS_Sharpe"]) for gt in GATES}
                say(f"   {pk:6s} {sig:4s} {cv}  " + "  ".join(f"{gt} {sh[gt]:.3f}" for gt in GATES)
                    + f"  spread {max(sh.values()) - min(sh.values()):.3f} tau {kendall(sh):+.2f}")

    # ---- predictions ----
    say("\n[P] PRE-REGISTERED PREDICTIONS, scored")
    p1 = spv("mom", "mat")[0]
    say(f"   P1 matched spread at fixed mom signal > 0.20: {p1:.3f} -> {'HELD' if p1 > 0.20 else 'FAILED'}")
    p2 = float((tim.abs() < 0.05).mean())
    say(f"   P2 |lit-sta| < 0.05 in >= 2/3 of arms: {p2:.0%} -> {'HELD' if p2 >= 2/3 else 'FAILED'}")
    inv = {}
    for pk in P:
        row = spsel(pk, "R40", "mom", "mat")
        inv[pk] = kendall({gt: float(row[f"S_{gt}"]) for gt in GATES})
    say(f"   P3 an adjacent inversion under mat on >= 1 panel: tau by panel "
        f"{ {k: round(v, 2) for k, v in inv.items()} } -> "
        f"{'HELD' if any(v < 1.0 for v in inv.values()) else 'FAILED'}")
    p4 = {pk: max(spv("mom", cv, panel=pk)[0] for cv in CONVS) for pk in ("u56", "broad")}
    say(f"   P4 u56/broad spread < 0.15 at n=40 under every convention: "
        f"{ {k: round(v, 3) for k, v in p4.items()} } -> "
        f"{'HELD' if all(v < 0.15 for v in p4.values()) else 'FAILED'}")
    p5 = int(grid.query("panel=='small'").pass4b.sum())
    say(f"   P5 nothing passes 4b on the small panel: {p5} passes -> {'HELD' if p5 == 0 else 'FAILED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()

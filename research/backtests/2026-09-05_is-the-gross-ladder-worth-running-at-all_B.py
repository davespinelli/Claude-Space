#!/usr/bin/env python3
"""QUEUE idea 184 — is-the-gross-ladder-worth-running-at-all  (lane B, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 184)
    "idea 173 found the mean OOS Sharpe range across the whole gross ladder is 0.003
     (0.720-0.721 over 0.45-1.35) on 18 book-cells, that its argmax buys +0.0002 at t=0.42,
     and that GROSS carries 46 of the project's 104 argmax claims.  Ideas 172/174 point the
     same way from the 4b side.  Test the strong form: does ANY published gross-ladder verdict
     change if gross is fixed at 0.75 everywhere?  If not, PROTOCOL should retire the gross
     sweep and spend the runs on cadence."

WHAT "A GROSS-LADDER VERDICT" IS, MADE FALSIFIABLE
    A swept gross ladder is used by this project for exactly two things, and they are not the
    same claim:
      (SEL) SELECTION — "the argmax is g*".  A ladder point is chosen (by IS Sharpe, the
            incumbent selector) and reported as the book.  Idea 173 already showed the OOS
            Sharpe surface is FLAT in gross, so this half should be worthless.
      (ADM) ADMISSION — "this book passes 4a / 4b".  A row is published as a pass if SOME
            ladder point clears the bars.  Two of 4b's five bars are LEVELS, not ratios
            (CAGR >= 0.70 x SPY, MaxDD <= 0.60 x SPY), and idea 174 measured c ~= 0.856 x gross,
            so admission is mechanically gross-dependent even when Sharpe is not.
    The strong form of idea 184 requires BOTH halves to be inert under g := 0.75.  This run
    prices them separately, and the honest answer can therefore be a SPLIT.

CORPUS — 27 book-cells x 9 gross points = 243 GENUINE engine runs, 486 ladder points
    3 panels   u56 (research/universe.json), broad (universe_broad.json, 136 large caps),
               small (data/prices_small.csv sub-$2B, tickers with max_1d_move >= 1.0 dropped)
    3 signals  COMP (RULES v1's composite), MOM (12-1), R6 (6-month return)
    3 counts   n = 10, 20, 40
    9 gross    g = 0.20 0.35 0.50 0.65 0.75 0.90 1.05 1.20 1.35   (anchor 0.75 is rank 5 of 9,
               deliberately INTERIOR — idea 183's anchor-position caveat)
    2 cost rungs 10 bps (PROTOCOL) and 25 bps, derived EXACTLY from the zero-cost run and the
               engine's own turnover series (port_c = port_0 - turnover * c / 1e4).  Verified
               against a genuine 10 bps run in the reproduction block below.
    => 54 books (book-cell x cost rung), each with a full 9-point ladder.
    NO RESCALING ANYWHERE: idea 176 showed a rescaled ladder is not a genuine one, and this
    run measures that error directly instead of relying on it.

TUNED PARAMETERS — one
    GROSS is the only dial varied and the only thing ever selected on.  Panel, signal, count,
    cadence (W), max_vol (0.60), vol power (0.5) and the cost rung are REPORTED AXES: every
    one of the 486 points is written to .grid.csv and none is chosen on.  The second budgeted
    parameter is the SELECTOR (IS-Sharpe argmax / IS-4b-admission / fixed 0.75 / oracle), and
    all four are reported for every book.

BOOK CONSTRUCTION — idea 127's "literal" convention, unchanged
    w = (rank <= n) * g / n over names passing (px > 200d MA) & (vol20 < 0.60), score
    s = signal / vol20**0.5; unfilled slots are cash.  Weights decided at close t, applied at
    t+1 by the engine (PROTOCOL 2).  No sleeve, no overlay, no renormalisation.

WALK-FORWARD (PROTOCOL rule 8) — required, and central here
    IS  = sample start .. 2016-12-31 (read by the selectors).
    OOS = 2017-01-01 .. end, read ONCE per book.
    Four arms per book: FIX075 (do-nothing), ISSHARPE (argmax IS Sharpe), IS4B (lowest g whose
    IS window clears 4b's five bars computed on the IS window; falls back to 0.75 if none),
    ORACLE (best OOS Sharpe, not implementable).  Reported against RULES v1 on the same panel
    at the same cost rung and against SPY buy-and-hold, both KEEP paths evaluated.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  SELECTION is inert: mean OOS Sharpe of ISSHARPE minus FIX075 is < 0.02 with |t| < 2.
    P2  The three SHARPE bars of 4b are gross-invariant: in >= 90% of books each of H1, H2 and
        OOS holds the same pass/fail at all 9 gross points.
    P3  ADMISSION is NOT inert: >= 25% of books have at least one ladder point passing full-
        sample 4b while g=0.75 fails (or the reverse).
    P4  The flips are carried by the CAGR floor and the DD cap, not by Sharpe.
    P5  4b pass rate is 0 at every g <= 0.50 on every panel (idea 174's c ~= 0.856 x g).
    P6  A rescaled ladder (idea 176) mislabels at least one point's 4b verdict.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54).  All three panels are CURRENT constituents; the small panel is
      today's sub-$2B screen with delisted/acquired names absent.  Every CAGR here is
      optimistic and every MaxDD flattering, so the 4b region looks MORE reachable than it is.
    * WINDOW COMPOSITION (idea 111).  The IS window holds fewer SPY-drawdown years than the
      OOS window; the small panel's IS window is only 2011-2016.
    * This run audits the GROSS ladder as this corpus builds it.  It does not re-run every
      committed leaderboard row (that is idea 176's audit); its claim about the published
      record is a claim about what a gross ladder CAN do, priced on 486 fresh points.
    * t+1 execution, 10 or 25 bps, no shorting, no leverage.

Deterministic (seed 184), standalone, no network.
Writes .grid.csv (486 points), .books.csv (54), .walkforward.csv (54), .bars.csv,
.rescale.csv, .result.md and .console.txt.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_is-the-gross-ladder-worth-running-at-all_B"
OUT = ROOT / "research" / "backtests"
SEED = 184
IS_END = pd.Timestamp("2016-12-31")

GROSS = [0.20, 0.35, 0.50, 0.65, 0.75, 0.90, 1.05, 1.20, 1.35]
ANCHOR_G = 0.75
SIGNALS = ["COMP", "MOM", "R6"]
COUNTS = [10, 20, 40]
COSTS = [10.0, 25.0]
FREQ, MAX_VOL, VOLPOW = "W", 0.60, 0.5

_console: list[str] = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _console.append(line)


# ----------------------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"small panel: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(keep) - 1} names + SPY benchmark remain")
    return px[keep]


# ----------------------------------------------------------------------------- signals
_CACHE: dict = {}


def raw_signal(px, sig):
    key = (id(px), sig)
    if key in _CACHE:
        return _CACHE[key]
    if sig == "COMP":
        mom = px.shift(21) / px.shift(252) - 1
        r6 = px / px.shift(126) - 1
        r3 = px / px.shift(63) - 1
        s = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elif sig == "MOM":
        s = px.shift(21) / px.shift(252) - 1
    elif sig == "R6":
        s = px / px.shift(126) - 1
    else:
        raise ValueError(sig)
    _CACHE[key] = s
    return s


def gates(px):
    key = (id(px), "_gates")
    if key not in _CACHE:
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        _CACHE[key] = (above, vol20)
    return _CACHE[key]


def weights(px, sig, n, g):
    s = raw_signal(px, sig)
    above, vol20 = gates(px)
    s = s / vol20.clip(lower=0.08) ** VOLPOW
    elig = s.where(above & (vol20 < MAX_VOL))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


# ----------------------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def oos_halves(r):
    o = win(r, lo=IS_END + pd.Timedelta(days=1))
    h = len(o) // 2
    return metrics(o.iloc[:h])["Sharpe"], metrics(o.iloc[h:])["Sharpe"]


def is_halves(r):
    i = win(r, hi=IS_END)
    h = len(i) // 2
    return metrics(i.iloc[:h])["Sharpe"], metrics(i.iloc[h:])["Sharpe"]


def full_row(r):
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:len(r) // 2]), ("H2", r.iloc[len(r) // 2:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=IS_END + pd.Timedelta(days=1)))):
        c, s, d = stats(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = c, s, d
    out["oosH1"], out["oosH2"] = oos_halves(r)
    out["isH1"], out["isH2"] = is_halves(r)
    return out


# ------- the five 4b bars, reported one by one so a flip can be attributed to a bar
def bars4b(row, spy, w="F"):
    """Pass/fail of each 4b bar on window w in {F (full sample), OOS (OOS window alone)}."""
    if w == "F":
        return dict(H1=row["Sharpe_H1"] > spy["Sharpe_H1"], H2=row["Sharpe_H2"] > spy["Sharpe_H2"],
                    OOS=row["Sharpe_OOS"] > spy["Sharpe_OOS"],
                    DD=row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"],
                    CAGR=row["CAGR_F"] >= 0.70 * spy["CAGR_F"])
    if w == "OOS":
        return dict(H1=row["oosH1"] > spy["oosH1"], H2=row["oosH2"] > spy["oosH2"],
                    OOS=row["Sharpe_OOS"] > spy["Sharpe_OOS"],
                    DD=row["MaxDD_OOS"] >= 0.60 * spy["MaxDD_OOS"],
                    CAGR=row["CAGR_OOS"] >= 0.70 * spy["CAGR_OOS"])
    if w == "IS":
        return dict(H1=row["isH1"] > spy["isH1"], H2=row["isH2"] > spy["isH2"],
                    OOS=row["Sharpe_IS"] > spy["Sharpe_IS"],
                    DD=row["MaxDD_IS"] >= 0.60 * spy["MaxDD_IS"],
                    CAGR=row["CAGR_IS"] >= 0.70 * spy["CAGR_IS"])
    raise ValueError(w)


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def tstat(d):
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=float)
    if len(d) < 2 or d.std(ddof=1) == 0:
        return np.nan
    return float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))


def spearman(a, b):
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    if ra.std(ddof=0) == 0 or rb.std(ddof=0) == 0:
        return np.nan
    return float(np.corrcoef(ra.values, rb.values)[0, 1])


# ----------------------------------------------------------------------------- run
def main():
    t0 = time.time()
    panels = {"u56": load_universe(), "broad": load_universe(broad=True), "small": small_panel()}

    ref = {}
    for pn, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        b0 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        ref[pn] = dict(start=start, spy=spy, spy_row=full_row(spy),
                       b_ret=b0["returns"].loc[start:], b_trn=b0["turnover"].loc[start:])
        say(f"panel {pn}: {px.shape[1]} cols, sample {start.date()}..{px.index[-1].date()}, "
            f"IS rows {len(win(spy, hi=IS_END))}, OOS rows {len(win(spy, lo=IS_END))}, "
            f"SPY F {ref[pn]['spy_row']['CAGR_F']:.2%}/{ref[pn]['spy_row']['Sharpe_F']:.4f}/"
            f"{ref[pn]['spy_row']['MaxDD_F']:.2%}")

    # ======================================================================= REPRODUCTION
    say("\n=== REPRODUCTION / INTEGRITY ===")
    rep = []
    for pn in panels:
        px = panels[pn]
        w = weights(px, "COMP", 20, 0.75)
        r0 = backtest(px, w, cost_bps=0.0, freq=FREQ)
        genuine = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"].loc[ref[pn]["start"]:]
        derived = (r0["returns"] - r0["turnover"] * 10.0 / 1e4).loc[ref[pn]["start"]:]
        err = float((genuine - derived).abs().max())
        rep.append(dict(check=f"cost identity {pn}", value=err))
        say(f"  cost-derivation identity {pn:6s}: max |genuine(10bps) - derived| = {err:.3e}")
    b_self = ref["u56"]["b_ret"] - ref["u56"]["b_trn"] * 10.0 / 1e4
    say(f"  RULES v1 u56 @10bps: CAGR {metrics(b_self)['CAGR']:.2%} Sharpe {metrics(b_self)['Sharpe']:.4f} "
        f"MaxDD {metrics(b_self)['MaxDD']:.2%}")

    # ======================================================================= THE 243 RUNS
    say("\n=== GRID: 27 book-cells x 9 gross = 243 genuine engine runs ===")
    grid = []
    raw_by_cell: dict = {}     # (panel, signal, n) -> {g: (r0, trn)}
    n_runs = 0
    for pn, px in panels.items():
        start = ref[pn]["start"]
        for sig in SIGNALS:
            for n in COUNTS:
                cell = {}
                for g in GROSS:
                    res = backtest(px, weights(px, sig, n, g), cost_bps=0.0, freq=FREQ)
                    r0, trn = res["returns"].loc[start:], res["turnover"].loc[start:]
                    cell[g] = (r0, trn)
                    n_runs += 1
                    for c in COSTS:
                        r = r0 - trn * c / 1e4
                        row = dict(panel=pn, signal=sig, n=n, cost=c, gross=g,
                                   rank=GROSS.index(g) + 1,
                                   turnover_yr=float(trn.sum() / (len(trn) / 252)))
                        row.update(full_row(r))
                        base = ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4
                        brow = full_row(base)
                        spy = ref[pn]["spy_row"]
                        row["pass4a"] = int(pass4a(row, brow))
                        bF, bO = bars4b(row, spy, "F"), bars4b(row, spy, "OOS")
                        row["pass4b"] = int(all(bF.values()))
                        row["pass4b_oos"] = int(all(bO.values()))
                        for k, v in bF.items():
                            row[f"bF_{k}"] = int(v)
                        for k, v in bO.items():
                            row[f"bO_{k}"] = int(v)
                        grid.append(row)
                raw_by_cell[(pn, sig, n)] = cell
                say(f"  {pn:6s} {sig:4s} n={n:<3d} done ({n_runs} runs, {time.time() - t0:.0f}s)")
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"{n_runs} genuine engine runs -> {len(G)} ladder points written to .grid.csv "
        f"({time.time() - t0:.0f}s)")

    # ======================================================================= RESCALE TEST (idea 176)
    say("\n=== IS A RESCALED LADDER THE SAME LADDER?  (idea 176's exposure, measured) ===")
    resc = []
    for (pn, sig, n), cell in raw_by_cell.items():
        r075, t075 = cell[ANCHOR_G]
        for g in GROSS:
            if g == ANCHOR_G:
                continue
            k = g / ANCHOR_G
            fake = r075 * k
            faketrn = t075 * k
            for c in COSTS:
                gen = full_row(cell[g][0] - cell[g][1] * c / 1e4)
                fk = full_row(fake - faketrn * c / 1e4)
                spy = ref[pn]["spy_row"]
                resc.append(dict(panel=pn, signal=sig, n=n, cost=c, gross=g,
                                 dSharpe=fk["Sharpe_F"] - gen["Sharpe_F"],
                                 dMaxDD_pp=100 * (fk["MaxDD_F"] - gen["MaxDD_F"]),
                                 dCAGR_pp=100 * (fk["CAGR_F"] - gen["CAGR_F"]),
                                 v_gen=int(all(bars4b(gen, spy, "F").values())),
                                 v_fake=int(all(bars4b(fk, spy, "F").values()))))
    R = pd.DataFrame(resc)
    R["mislabel"] = (R.v_gen != R.v_fake).astype(int)
    R.to_csv(OUT / f"{STEM}.rescale.csv", index=False)
    say(f"  {len(R)} rescaled-vs-genuine comparisons: max |dSharpe| {R.dSharpe.abs().max():.4f}, "
        f"max |dMaxDD| {R.dMaxDD_pp.abs().max():.2f}pp, max |dCAGR| {R.dCAGR_pp.abs().max():.2f}pp")
    say(f"  4b verdict MISLABELLED by rescaling in {int(R.mislabel.sum())} of {len(R)} points "
        f"({R.mislabel.mean():.1%})  [P6]")

    # ======================================================================= M0 flatness (idea 173)
    say("\n=== M0  REPRODUCE IDEA 173: is the gross ladder flat in Sharpe? ===")
    by_g = G.groupby("gross")[["Sharpe_OOS", "Sharpe_F", "CAGR_F", "MaxDD_F", "turnover_yr"]].mean()
    for g, r in by_g.iterrows():
        say(f"  g={g:<5.2f} meanOOS Sharpe {r.Sharpe_OOS:.4f}  full Sharpe {r.Sharpe_F:.4f}  "
            f"CAGR {r.CAGR_F:.2%}  MaxDD {r.MaxDD_F:.2%}  turnover {r.turnover_yr:.1f}x")
    say(f"  RANGE across the ladder: OOS Sharpe {by_g.Sharpe_OOS.max() - by_g.Sharpe_OOS.min():.4f}, "
        f"full Sharpe {by_g.Sharpe_F.max() - by_g.Sharpe_F.min():.4f}, "
        f"CAGR {100 * (by_g.CAGR_F.max() - by_g.CAGR_F.min()):.2f}pp, "
        f"MaxDD {100 * (by_g.MaxDD_F.max() - by_g.MaxDD_F.min()):.2f}pp")
    # within-book ranges
    bk = G.groupby(["panel", "signal", "n", "cost"])
    rng = bk.agg(Sharpe_rng=("Sharpe_F", lambda x: x.max() - x.min()),
                 CAGR_rng=("CAGR_F", lambda x: 100 * (x.max() - x.min())),
                 DD_rng=("MaxDD_F", lambda x: 100 * (x.max() - x.min())),
                 rho=("Sharpe_F", lambda x: np.nan)).reset_index()
    rhos = [spearman(d.gross.values, d.Sharpe_F.values) for _, d in bk]
    rng["rho"] = rhos
    say(f"  within-book (54 books): median Sharpe range {rng.Sharpe_rng.median():.4f} "
        f"(max {rng.Sharpe_rng.max():.4f}); median CAGR range {rng.CAGR_rng.median():.2f}pp; "
        f"median MaxDD range {rng.DD_rng.median():.2f}pp")
    say(f"  Spearman(gross, full Sharpe) within book: mean {np.nanmean(rhos):+.3f}, "
        f"positive in {int(np.sum(np.array(rhos) > 0))} of {len(rhos)}")

    # ======================================================================= M1 the strong form
    say("\n=== M1  THE STRONG FORM: does any verdict change if gross is fixed at 0.75? ===")
    books = []
    for (pn, sig, n, c), d in bk:
        d = d.sort_values("gross")
        at = d[d.gross == ANCHOR_G].iloc[0]
        row = dict(panel=pn, signal=sig, n=n, cost=c)
        for v in ("pass4a", "pass4b", "pass4b_oos"):
            row[f"{v}_at075"] = int(at[v])
            row[f"{v}_any"] = int(d[v].max())
            row[f"{v}_count"] = int(d[v].sum())
            row[f"{v}_flip"] = int(d[v].max() != at[v])
        # which bars are constant along the ladder
        for tag in ("bF", "bO"):
            for b in ("H1", "H2", "OOS", "DD", "CAGR"):
                row[f"const_{tag}_{b}"] = int(d[f"{tag}_{b}"].nunique() == 1)
        row["gmax_4b"] = float(d.loc[d.pass4b == 1, "gross"].max()) if d.pass4b.max() else np.nan
        row["gmin_4b"] = float(d.loc[d.pass4b == 1, "gross"].min()) if d.pass4b.max() else np.nan
        books.append(row)
    B = pd.DataFrame(books)
    B.to_csv(OUT / f"{STEM}.books.csv", index=False)
    for v, lab in (("pass4a", "4a"), ("pass4b", "4b full-sample"), ("pass4b_oos", "4b OOS-window")):
        say(f"  {lab:16s}: passes at g=0.75 in {int(B[f'{v}_at075'].sum()):2d} of 54 books; "
            f"SOME ladder point passes in {int(B[f'{v}_any'].sum()):2d}; "
            f"**verdict FLIPS for {int(B[f'{v}_flip'].sum())} books** "
            f"({B[f'{v}_flip'].mean():.1%})")
    # per-point relabelling
    pts = []
    for (pn, sig, n, c), d in bk:
        at = d[d.gross == ANCHOR_G].iloc[0]
        for _, p in d.iterrows():
            pts.append(dict(gross=p.gross,
                            same4a=int(p.pass4a == at.pass4a), same4b=int(p.pass4b == at.pass4b),
                            same4bo=int(p.pass4b_oos == at.pass4b_oos)))
    P = pd.DataFrame(pts)
    say(f"  per-point: of {len(P)} ladder points, the verdict differs from its own book's "
        f"g=0.75 verdict in {int((1 - P.same4a).sum())} (4a), {int((1 - P.same4b).sum())} (4b), "
        f"{int((1 - P.same4bo).sum())} (4b-OOS)")
    say("  4b pass rate by gross rung  [P5]:")
    for g, d in G.groupby("gross"):
        say(f"    g={g:<5.2f}  4a {d.pass4a.mean():5.1%}  4b {d.pass4b.mean():5.1%}  "
            f"4b-OOS {d.pass4b_oos.mean():5.1%}   (n={len(d)})")

    # ======================================================================= M2 bar attribution
    say("\n=== M2  WHICH BAR MOVES ALONG THE LADDER?  (gross-invariance, per bar) ===")
    barrows = []
    for tag, lab in (("bF", "full-sample"), ("bO", "OOS-window")):
        for b in ("H1", "H2", "OOS", "DD", "CAGR"):
            const = B[f"const_{tag}_{b}"].mean()
            barrows.append(dict(window=lab, bar=b, const_share=const,
                                books_constant=int(B[f"const_{tag}_{b}"].sum())))
            say(f"  {lab:11s} {b:4s}: same pass/fail at all 9 gross points in "
                f"{int(B[f'const_{tag}_{b}'].sum()):2d} of 54 books ({const:5.1%})")
    pd.DataFrame(barrows).to_csv(OUT / f"{STEM}.bars.csv", index=False)
    # among the 4b failures at each point, which bar is sole binding
    fails = G[G.pass4b == 0]
    solo = {}
    for b in ("H1", "H2", "OOS", "DD", "CAGR"):
        others = [f"bF_{x}" for x in ("H1", "H2", "OOS", "DD", "CAGR") if x != b]
        solo[b] = int(((fails[f"bF_{b}"] == 0) & (fails[others].min(axis=1) == 1)).sum())
    viol = {b: int((fails[f"bF_{b}"] == 0).sum()) for b in ("H1", "H2", "OOS", "DD", "CAGR")}
    say(f"  of {len(fails)} full-sample 4b failures: violated {viol}; sole binding {solo}")

    # ======================================================================= M3 rule 8
    say("\n=== M3  RULE 8 WALK-FORWARD: four ways to use the ladder, read ONCE on 2017-> ===")
    wf = []
    for (pn, sig, n, c), d in bk:
        d = d.sort_values("gross").reset_index(drop=True)
        spy = ref[pn]["spy_row"]
        base = full_row(ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4)
        picks = {}
        picks["FIX075"] = ANCHOR_G
        picks["ISSHARPE"] = float(d.loc[d.Sharpe_IS.idxmax(), "gross"])
        adm = [float(r.gross) for _, r in d.iterrows()
               if all(bars4b(r, spy, "IS").values())]
        picks["IS4B"] = min(adm) if adm else ANCHOR_G
        picks["ORACLE"] = float(d.loc[d.Sharpe_OOS.idxmax(), "gross"])
        rec = dict(panel=pn, signal=sig, n=n, cost=c, n_IS_admissible=len(adm))
        for arm, g in picks.items():
            r = d[d.gross == g].iloc[0]
            rec[f"{arm}_g"] = g
            rec[f"{arm}_oosCAGR"] = r.CAGR_OOS
            rec[f"{arm}_oosSharpe"] = r.Sharpe_OOS
            rec[f"{arm}_oosMaxDD"] = r.MaxDD_OOS
            rec[f"{arm}_4bOOS"] = int(r.pass4b_oos)
            rec[f"{arm}_4b"] = int(r.pass4b)
            rec[f"{arm}_4a"] = int(r.pass4a)
        rec["base_oosSharpe"] = base["Sharpe_OOS"]
        rec["base_oosCAGR"] = base["CAGR_OOS"]
        rec["base_oosMaxDD"] = base["MaxDD_OOS"]
        rec["spy_oosSharpe"] = spy["Sharpe_OOS"]
        rec["spy_oosCAGR"] = spy["CAGR_OOS"]
        rec["spy_oosMaxDD"] = spy["MaxDD_OOS"]
        wf.append(rec)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"  {len(W)} books.  arm: mean OOS CAGR / Sharpe / MaxDD, 4b-OOS passes, mean picked g")
    for arm in ("FIX075", "ISSHARPE", "IS4B", "ORACLE"):
        say(f"    {arm:9s} {W[f'{arm}_oosCAGR'].mean():6.2%} / {W[f'{arm}_oosSharpe'].mean():.4f} / "
            f"{W[f'{arm}_oosMaxDD'].mean():7.2%}   4b-OOS {int(W[f'{arm}_4bOOS'].sum()):2d}/54   "
            f"4b {int(W[f'{arm}_4b'].sum()):2d}/54   4a {int(W[f'{arm}_4a'].sum()):2d}/54   "
            f"mean g {W[f'{arm}_g'].mean():.3f}")
    say(f"    {'RULES v1':9s} {W.base_oosCAGR.mean():6.2%} / {W.base_oosSharpe.mean():.4f} / "
        f"{W.base_oosMaxDD.mean():7.2%}")
    say(f"    {'SPY':9s} {W.spy_oosCAGR.mean():6.2%} / {W.spy_oosSharpe.mean():.4f} / "
        f"{W.spy_oosMaxDD.mean():7.2%}")
    for arm in ("ISSHARPE", "IS4B", "ORACLE"):
        dS = (W[f"{arm}_oosSharpe"] - W["FIX075_oosSharpe"]).values
        say(f"  paired vs FIX075: {arm:9s} dOOS Sharpe {dS.mean():+.4f} (t {tstat(dS):+.2f}), "
            f"better in {int((dS > 0).sum())}/54, picked g != 0.75 in "
            f"{int((W[f'{arm}_g'] != ANCHOR_G).sum())}/54  [P1]")

    # ======================================================================= KEEP paths
    say("\n=== BOTH KEEP PATHS, all 486 points ===")
    say(f"  4a {int(G.pass4a.sum())}/{len(G)};  4b full-sample {int(G.pass4b.sum())}/{len(G)};  "
        f"4b OOS-window {int(G.pass4b_oos.sum())}/{len(G)};  both 4a and 4b "
        f"{int(((G.pass4a == 1) & (G.pass4b == 1)).sum())}")
    for pn, d in G.groupby("panel"):
        say(f"    {pn:6s}: 4a {int(d.pass4a.sum()):3d}/{len(d)}  4b {int(d.pass4b.sum()):3d}  "
            f"4b-OOS {int(d.pass4b_oos.sum()):3d}")
    both = G[(G.pass4b == 1) & (G.pass4b_oos == 1)]
    if len(both):
        b = both.sort_values("Sharpe_F", ascending=False).iloc[0]
        say(f"  best point clearing 4b full AND OOS-window: {b.panel} {b.signal} n={int(b.n)} "
            f"g={b.gross} @{int(b.cost)}bps -> {b.CAGR_F:.2%} / {b.Sharpe_F:.4f} / {b.MaxDD_F:.2%} "
            f"(H1 {b.Sharpe_H1:.4f} H2 {b.Sharpe_H2:.4f}, OOS {b.CAGR_OOS:.2%}/{b.Sharpe_OOS:.4f}/"
            f"{b.MaxDD_OOS:.2%}, turnover {b.turnover_yr:.1f}x)")
        say(f"  BUT it is 1 of {len(both)} unpriced ladder selections -- reported, not proposed.")
    else:
        say("  no point clears both windows.")

    say(f"\ntotal runtime {time.time() - t0:.0f}s, {n_runs} genuine engine runs")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")
    return G, B, W, R


if __name__ == "__main__":
    main()
